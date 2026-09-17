"""Sabit sürüm ve yama girişlerindeki tahrif/kaçış durumlarını sınar."""

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts.yuva_dev.common import ROOT, ToolError
from scripts.yuva_dev.metadata import load_patches, load_versions, read_json


class MetadataTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        (self.root / "config").mkdir()
        (self.root / "patches").mkdir()
        self.versions = json.loads((ROOT / "config/versions.json").read_text())
        self.write_versions()

    def write_versions(self):
        (self.root / "config/versions.json").write_text(json.dumps(self.versions))

    def make_patch(self, identifier="first", dependencies=None):
        payload = b"diff --git a/file.txt b/file.txt\n"
        name = f"patches/{identifier}.patch"
        (self.root / name).write_bytes(payload)
        return {
            "id": identifier, "file": name, "sha256": hashlib.sha256(payload).hexdigest(),
            "purpose": "Deneme", "security_impact": "Sentetik veri", "privacy_impact": "Veri yok",
            "upstream_conflict_risk": "low", "feature": "development_tools",
            "tests": ["synthetic_patch"], "components": ["components/example"], "depends_on": dependencies or [],
            "owner": "test-owner", "backup_owner": "test-backup", "license": "BSD-3-Clause",
            "source": "Sentetik test verisi", "removal_condition": "Test tamamlanınca kaldırılır",
            "upstream_revision": self.versions["chromium_revision"],
        }

    def write_series(self, patches, version=None):
        data = {"schema_version": 1, "patchset_version": version or self.versions["patchset_version"], "patches": patches}
        (self.root / "patches/series.json").write_text(json.dumps(data))

    def test_rejects_ambiguous_source_revision(self):
        self.versions["chromium_revision"] = "latest"
        self.write_versions()
        with self.assertRaises(ToolError):
            load_versions(self.root)

    def test_rejects_unknown_fields_and_boolean_schema(self):
        for field, value in (("execute", "unsafe"), ("schema_version", True)):
            with self.subTest(field=field):
                original = dict(self.versions)
                self.versions[field] = value
                self.write_versions()
                with self.assertRaises(ToolError):
                    load_versions(self.root)
                self.versions = original

    def test_rejects_duplicate_json_keys(self):
        path = self.root / "duplicate.json"
        path.write_text('{"version": 1, "version": 2}')
        with self.assertRaises(ToolError):
            read_json(path)

    def test_rejects_oversized_metadata(self):
        path = self.root / "large.json"
        path.write_bytes(b" " * (1024 * 1024 + 1))
        with self.assertRaises(ToolError):
            read_json(path)

    def test_rejects_changed_patch_bytes(self):
        patch = self.make_patch()
        self.write_series([patch])
        (self.root / patch["file"]).write_text("Değiştirildi")
        with self.assertRaises(ToolError):
            load_patches(self.versions, self.root)

    def test_rejects_patch_traversal(self):
        patch = self.make_patch()
        patch["file"] = "patches/../outside.patch"
        self.write_series([patch])
        with self.assertRaises(ToolError):
            load_patches(self.versions, self.root)

    def test_rejects_symlink_patch(self):
        patch = self.make_patch()
        original = self.root / patch["file"]
        target = self.root / "target.patch"
        original.rename(target)
        try:
            original.symlink_to(target)
        except OSError:
            self.skipTest("Bu test ortamında sembolik bağlantı oluşturma yetkisi yok.")
        self.write_series([patch])
        with self.assertRaises(ToolError):
            load_patches(self.versions, self.root)

    def test_rejects_missing_dependency_and_version_mismatch(self):
        self.write_series([self.make_patch(dependencies=["missing"])])
        with self.assertRaises(ToolError):
            load_patches(self.versions, self.root)
        self.write_series([], self.versions["patchset_version"] + 1)
        with self.assertRaises(ToolError):
            load_patches(self.versions, self.root)

    def test_ordered_patch_chain_is_accepted(self):
        patches = [self.make_patch(), self.make_patch("second", ["first"])]
        self.write_series(patches)
        self.assertEqual(load_patches(self.versions, self.root), patches)

    def test_rejects_missing_ownership_and_ambiguous_review_revision(self):
        for field, value in (("owner", ""), ("license", ""), ("upstream_revision", "main")):
            with self.subTest(field=field):
                patch = self.make_patch()
                patch[field] = value
                self.write_series([patch])
                with self.assertRaises(ToolError):
                    load_patches(self.versions, self.root)


if __name__ == "__main__":
    unittest.main()
