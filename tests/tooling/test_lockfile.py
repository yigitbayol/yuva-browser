"""Kilit kaydının kaynak/yama kimliklerinden ve güvenli kapsamdan kopmasını sınar."""

import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.yuva_dev.common import ROOT, ToolError
from scripts.yuva_dev.lockfile import expected_lock, load_lock
from scripts.yuva_dev.metadata import load_versions


class LockTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        for name in ("config/versions.json", "patches/series.json"):
            path = self.root / name
            path.parent.mkdir(exist_ok=True)
            path.write_bytes((ROOT / name).read_bytes())
        self.data = expected_lock(load_versions(self.root), self.root)
        self.write(self.data)

    def write(self, data):
        (self.root / "config/upstream.lock.json").write_text(json.dumps(data), encoding="utf-8")

    def test_valid_lock_explicitly_keeps_unresolved_stages(self):
        data = load_lock(self.root)
        self.assertEqual(data["scope"], "source_roots")
        self.assertIn("dependency_graph", data["pending_stages"])
        self.assertIn("pardus-23-x86_64", data["targets"])
        self.assertIn("pardus-25-x86_64", data["targets"])

    def test_source_and_patch_changes_require_lock_review(self):
        for name in ("config/versions.json", "patches/series.json"):
            path = self.root / name
            original = path.read_bytes()
            with self.subTest(name=name):
                path.write_bytes(original + b"\n")
                with self.assertRaises(ToolError):
                    load_lock(self.root)
                path.write_bytes(original)

    def test_rejects_changed_origin_revision_and_directory(self):
        for key, value in (("url", "https://evil.example/source"), ("revision", "main"), ("directory", "../outside")):
            with self.subTest(key=key):
                data = copy.deepcopy(self.data)
                data["roots"][0][key] = value
                self.write(data)
                with self.assertRaises(ToolError):
                    load_lock(self.root)

    def test_cannot_erase_pending_gates_or_claim_full_build(self):
        for key, value in (("pending_stages", []), ("scope", "full_build"), ("schema_version", True), ("targets", ["linux-x86_64"])):
            with self.subTest(key=key):
                data = dict(self.data, **{key: value})
                self.write(data)
                with self.assertRaises(ToolError):
                    load_lock(self.root)
