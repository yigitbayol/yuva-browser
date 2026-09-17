"""Küçük yerel Git depolarıyla gerçek getirme/doğrulama ve kesinti sınırlarını dener."""

import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.yuva_dev.common import ROOT, ToolError
from scripts.yuva_dev.lockfile import expected_lock
from scripts.yuva_dev.metadata import load_versions
from scripts.yuva_dev.sources import HOOKS_NAME, LEASE_NAME, STATE_NAME, git, isolated_environment, prepare_roots
from scripts.yuva_dev.sources import write_state


class SourceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.root = self.base / "yuva"
        self.workspace = self.base / "workspace"
        self.root.mkdir()
        (self.root / "config").mkdir()
        (self.root / "patches").mkdir()
        (self.base / HOOKS_NAME).mkdir()
        self.versions = load_versions()
        self.sources = {}
        deps = b"# Sentetik DEPS; asla calistirilmaz.\n"
        for name in ("chromium", "depot_tools"):
            source = self.base / name
            source.mkdir()
            git(source, "init", "--quiet", f"--template={self.base / HOOKS_NAME}")
            git(source, "config", "user.name", "Fixture")
            git(source, "config", "user.email", "fixture@example.invalid")
            if name == "chromium":
                (source / "DEPS").write_bytes(deps)
                (source / "chrome").mkdir()
                parts = self.versions["chromium_version"].split(".")
                content = "\n".join(f"{key}={value}" for key, value in zip(("MAJOR", "MINOR", "BUILD", "PATCH"), parts)) + "\n"
                (source / "chrome/VERSION").write_text(content, encoding="utf-8")
            else:
                (source / "gclient.py").write_bytes(b"raise RuntimeError('Bu dosya calistirilmamali')\n")
            git(source, "add", ".")
            git(source, "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "Sentetik kaynak")
            self.versions[f"{name}_revision"] = git(source, "rev-parse", "HEAD")
            self.sources[name] = source
        self.versions["chromium_deps_sha256"] = hashlib.sha256(deps).hexdigest()
        (self.root / "patches/series.json").write_bytes((ROOT / "patches/series.json").read_bytes())
        self.write_lock()
        self.fetches = []

    def write_lock(self):
        (self.root / "config/versions.json").write_text(json.dumps(self.versions), encoding="utf-8")
        (self.root / "config/upstream.lock.json").write_text(json.dumps(expected_lock(self.versions, self.root)), encoding="utf-8")

    def local_fetch(self, directory, url, revision):
        self.fetches.append((url, revision))
        name = "depot_tools" if directory.name == "depot_tools" else "chromium"
        # Yerel taşıma yalnız test enjeksiyonudur; üretim komutu file:// kabul etmez.
        git(directory, "-c", "protocol.file.allow=always", "fetch", "--quiet", "--depth=1", "--no-tags", self.sources[name].as_uri(), revision)

    def prepare(self):
        with patch("scripts.yuva_dev.sources.fetch_commit", side_effect=self.local_fetch):
            return prepare_roots(self.workspace, self.versions, self.root)

    def test_prepares_exact_roots_and_reuses_without_fetch_or_hooks(self):
        result = self.prepare()
        self.assertEqual(result["phase"], "roots_ready")
        self.assertFalse(result["build_ready"])
        self.assertEqual(len(self.fetches), 2)
        before = (self.workspace / STATE_NAME).read_bytes()
        index_before = (self.workspace / "src/.git/index").read_bytes()
        again = self.prepare()
        self.assertTrue(again["reused"])
        self.assertEqual(len(self.fetches), 2)
        self.assertEqual((self.workspace / STATE_NAME).read_bytes(), before)
        self.assertEqual((self.workspace / "src/.git/index").read_bytes(), index_before)
        self.assertFalse((self.workspace / LEASE_NAME).exists())
        self.assertFalse((self.workspace / ".gclient").exists())

    def test_rejects_existing_unowned_directory_and_preserves_data(self):
        self.workspace.mkdir()
        document = self.workspace / "important.txt"
        document.write_bytes(b"keep")
        with self.assertRaises(ToolError):
            self.prepare()
        self.assertEqual(document.read_bytes(), b"keep")
        self.assertEqual(list(self.workspace.iterdir()), [document])
        self.assertFalse(self.fetches)

    def test_failed_fetch_leaves_failed_state_and_cannot_resume_silently(self):
        def interrupted(directory, url, revision):
            if directory.name == "src":
                raise ToolError("Sentetik ağ kesintisi")
            self.local_fetch(directory, url, revision)
        with patch("scripts.yuva_dev.sources.fetch_commit", side_effect=interrupted):
            with self.assertRaises(ToolError):
                prepare_roots(self.workspace, self.versions, self.root)
        state = json.loads((self.workspace / STATE_NAME).read_text(encoding="utf-8"))
        self.assertEqual(state["phase"], "failed")
        with self.assertRaises(ToolError):
            self.prepare()
        self.assertTrue((self.workspace / "depot_tools/gclient.py").exists())
        self.assertEqual(len(self.fetches), 1)

    def test_changed_deps_hash_never_becomes_ready(self):
        self.versions["chromium_deps_sha256"] = "0" * 64
        self.write_lock()
        with self.assertRaises(ToolError):
            self.prepare()
        self.assertEqual(json.loads((self.workspace / STATE_NAME).read_text(encoding="utf-8"))["phase"], "failed")

    def test_wrong_fetched_commit_is_rejected(self):
        def wrong_fetch(directory, url, revision):
            git(directory, "-c", "protocol.file.allow=always", "fetch", "--quiet", self.sources["chromium"].as_uri(), self.versions["chromium_revision"])
        with patch("scripts.yuva_dev.sources.fetch_commit", side_effect=wrong_fetch):
            with self.assertRaisesRegex(ToolError, "beklenen revizyon"):
                prepare_roots(self.workspace, self.versions, self.root)

    def test_dirty_checkout_is_not_overwritten(self):
        self.prepare()
        path = self.workspace / "src/DEPS"
        path.write_bytes(b"user changes")
        with self.assertRaises(ToolError):
            self.prepare()
        self.assertEqual(path.read_bytes(), b"user changes")

    def test_changed_origin_or_git_configuration_blocks_reuse(self):
        self.prepare()
        git(self.workspace / "src", "config", "core.worktree", str(self.sources["chromium"]))
        with self.assertRaisesRegex(ToolError, "yapılandırması"):
            self.prepare()

    def test_lock_change_during_fetch_cannot_create_success_receipt(self):
        def changed_lock(directory, url, revision):
            self.local_fetch(directory, url, revision)
            if directory.name == "src":
                path = self.root / "config/upstream.lock.json"
                path.write_bytes(path.read_bytes() + b"\n")
        with patch("scripts.yuva_dev.sources.fetch_commit", side_effect=changed_lock):
            with self.assertRaisesRegex(ToolError, "İşlem sırasında"):
                prepare_roots(self.workspace, self.versions, self.root)
        state = json.loads((self.workspace / STATE_NAME).read_text(encoding="utf-8"))
        self.assertEqual(state["phase"], "failed")

    def test_disk_error_cannot_mark_roots_ready(self):
        def full_disk(workspace, state):
            if state["phase"] == "roots_ready":
                raise OSError(28, "Sentetik disk dolması")
            write_state(workspace, state)
        with patch("scripts.yuva_dev.sources.write_state", side_effect=full_disk):
            with self.assertRaises(OSError):
                self.prepare()
        state = json.loads((self.workspace / STATE_NAME).read_text(encoding="utf-8"))
        self.assertEqual(state["phase"], "failed")
        self.assertFalse((self.workspace / LEASE_NAME).exists())

    def test_active_or_crashed_lease_is_preserved(self):
        self.workspace.mkdir()
        lease = self.workspace / LEASE_NAME
        lease.write_bytes(b"another process")
        with self.assertRaises(ToolError):
            self.prepare()
        self.assertEqual(lease.read_bytes(), b"another process")

    def test_linked_destination_is_rejected(self):
        target = self.base / "elsewhere"
        target.mkdir()
        try:
            self.workspace.symlink_to(target, target_is_directory=True)
        except OSError:
            self.skipTest("Bu ortamda sembolik bağlantı yetkisi yok.")
        with self.assertRaises(ToolError):
            self.prepare()
        self.assertEqual(list(target.iterdir()), [])

    def test_ambient_git_configuration_is_removed(self):
        with patch.dict(os.environ, {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "core.hooksPath", "GIT_CONFIG_VALUE_0": "/bad/hooks", "GIT_DIR": "/bad/repo"}):
            environment = isolated_environment()
            self.assertNotIn("GIT_CONFIG_COUNT", environment)
            self.assertNotIn("GIT_DIR", environment)
            self.assertEqual(environment["GIT_CONFIG_GLOBAL"], os.devnull)
            self.prepare()


if __name__ == "__main__":
    unittest.main()
