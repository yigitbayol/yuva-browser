"""Uzak meta veri tahrifini ve sıralı yama çakışmalarını sentetik verilerle sınar."""

import base64
import hashlib
import json
import subprocess
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from scripts.yuva_dev.common import ToolError
from scripts.yuva_dev.metadata import load_versions
from scripts.yuva_dev.upstream import NoRedirect, RELEASE_URL, SOURCE_BASE, TOOLS_BASE, check_patches, fetch_bytes, verify_network


class NetworkTests(unittest.TestCase):
    def setUp(self):
        self.versions = load_versions()
        self.deps = b"Sentetik DEPS; calistirilmaz."
        self.versions["chromium_deps_sha256"] = hashlib.sha256(self.deps).hexdigest()
        self.now = datetime(2026, 9, 18, tzinfo=timezone.utc)
        self.release = {
            "version": self.versions["chromium_version"], "channel": "Stable", "platform": "Mac",
            "time": int(self.now.timestamp() * 1000), "hashes": {"chromium": self.versions["chromium_revision"]},
        }
        self.platform_overrides = {}
        version, revision = self.versions["chromium_version"], self.versions["chromium_revision"]
        self.tag_url = f"{SOURCE_BASE}/+/refs/tags/{version}?format=JSON"
        self.deps_url = f"{SOURCE_BASE}/+/{revision}/DEPS?format=TEXT"
        self.payloads = {
            self.tag_url: b")]}'\n" + json.dumps({"commit": revision}).encode(),
            self.deps_url: base64.b64encode(self.deps),
            f"{TOOLS_BASE}/+/{self.versions['depot_tools_revision']}?format=JSON": b")]}'\n" + json.dumps({"commit": self.versions["depot_tools_revision"]}).encode(),
        }

    def fetch(self, url):
        if url.startswith("https://chromiumdash.appspot.com/"):
            target = parse_qs(urlsplit(url).query)["platform"][0]
            record = dict(self.release, platform=target)
            record.update(self.platform_overrides.get(target, {}))
            return json.dumps([record]).encode()
        return self.payloads[url]

    def verify(self):
        return verify_network(self.versions, self.fetch, self.now)

    def test_accepts_matching_source_without_executing_deps(self):
        self.assertFalse(self.verify()["update_available"])

    def test_detects_new_release_without_changing_pin(self):
        previous = dict(self.versions)
        parts = self.release["version"].split(".")
        parts[-1] = str(int(parts[-1]) + 1)
        self.release["version"] = ".".join(parts)
        self.release["hashes"]["chromium"] = "b" * 40
        self.assertTrue(self.verify()["update_available"])
        self.assertEqual(self.versions, previous)

    def test_detects_windows_only_security_update(self):
        parts = self.release["version"].split(".")
        parts[-1] = str(int(parts[-1]) + 1)
        self.platform_overrides["Windows"] = {"version": ".".join(parts), "hashes": {"chromium": "b" * 40}}
        result = self.verify()
        self.assertTrue(result["update_available"])
        self.assertEqual(len(result["platform_releases"]), 3)

    def test_rejects_tag_commit_mismatch(self):
        self.payloads[self.tag_url] = b")]}'\n" + json.dumps({"commit": "0" * 40}).encode()
        with self.assertRaises(ToolError):
            self.verify()

    def test_rejects_deps_tampering(self):
        self.payloads[self.deps_url] = base64.b64encode(b"Degistirildi")
        with self.assertRaises(ToolError):
            self.verify()

    def test_rejects_old_or_future_release_time(self):
        for offset in (-15, 2):
            self.release["time"] = int((self.now.timestamp() + offset * 86400) * 1000)
            with self.subTest(offset=offset), self.assertRaises(ToolError):
                self.verify()

    def test_rejects_wrong_channel_and_same_version_equivocation(self):
        self.release["channel"] = "Canary"
        with self.assertRaises(ToolError):
            self.verify()
        self.release["channel"] = "Stable"
        self.release["hashes"]["chromium"] = "0" * 40
        with self.assertRaises(ToolError):
            self.verify()

    def test_blocks_unapproved_origin_and_redirect(self):
        with self.assertRaises(ToolError):
            fetch_bytes("https://chromium.googlesource.com.evil.example/data")
        with self.assertRaises(ToolError):
            NoRedirect().redirect_request(None, None, 302, None, None, "http://example.test")


class PatchTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.root, self.source = self.base / "yuva", self.base / "source"
        self.root.mkdir()
        self.source.mkdir()
        (self.root / "patches").mkdir()
        self.git("init", "-q")
        self.git("config", "core.autocrlf", "false")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("remote", "add", "origin", SOURCE_BASE + ".git")
        (self.source / "value.txt").write_bytes(b"original\n")
        self.git("add", "value.txt")
        self.git("commit", "-qm", "Sentetik taban")
        self.revision = self.git("rev-parse", "HEAD").strip()

    def git(self, *arguments):
        result = subprocess.run(["git", *arguments], cwd=self.source, capture_output=True, text=True, check=True)
        return result.stdout

    def patch(self, identifier, before, after):
        name = f"patches/{identifier}.patch"
        text = f"diff --git a/value.txt b/value.txt\n--- a/value.txt\n+++ b/value.txt\n@@ -1 +1 @@\n-{before}\n+{after}\n"
        (self.root / name).write_bytes(text.encode())
        return {"id": identifier, "file": name, "components": ["components/example"]}

    def test_sequential_patches_do_not_change_checkout_or_real_index(self):
        patches = [self.patch("first", "original", "second"), self.patch("second", "second", "third")]
        index_before = (self.source / ".git/index").read_bytes()
        objects_before = sorted(str(path) for path in (self.source / ".git/objects").rglob("*"))
        results = check_patches(self.source, self.revision, patches, self.root)
        self.assertEqual([item["status"] for item in results], ["applies", "applies"])
        self.assertEqual((self.source / "value.txt").read_bytes(), b"original\n")
        self.assertEqual((self.source / ".git/index").read_bytes(), index_before)
        self.assertEqual(sorted(str(path) for path in (self.source / ".git/objects").rglob("*")), objects_before)
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_conflict_stops_later_patch_and_reports_component(self):
        patches = [self.patch("first", "absent", "second"), self.patch("second", "original", "third")]
        results = check_patches(self.source, self.revision, patches, self.root)
        self.assertEqual([item["status"] for item in results], ["conflict", "not_checked"])
        self.assertEqual(results[0]["components"], ["components/example"])

    def test_missing_target_is_not_fetched(self):
        with self.assertRaises(ToolError):
            check_patches(self.source, "0" * 40, [], self.root)

    def test_partial_clone_is_rejected_before_patch_evaluation(self):
        self.git("config", "remote.origin.promisor", "true")
        with self.assertRaises(ToolError):
            check_patches(self.source, self.revision, [], self.root)


if __name__ == "__main__":
    unittest.main()
