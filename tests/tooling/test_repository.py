"""Git indeksindeki gerçek içeriğin, ignore kurallarından bağımsız denetlenmesini sınar."""

import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.yuva_dev.repository import MAX_FILE_BYTES, inspect_index


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)

    def stage(self, name, payload=b"Yuva\n"):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        subprocess.run(["git", "add", "--", name], cwd=self.root, check=True, capture_output=True)
        return path

    def test_accepts_small_yuva_sources_and_packaging_definitions(self):
        self.stage("components/yuva_kalkan/policy.cc")
        self.stage("build/packaging/pardus/debian/control")
        self.assertTrue(inspect_index(self.root)["passed"])

    def test_rejects_source_tree_and_build_output(self):
        self.stage("vendor/chromium/third_party/blink/example.cc")
        self.stage("out/Default/Yuva.app/executable")
        report = inspect_index(self.root)
        self.assertFalse(report["passed"])
        self.assertEqual(len(report["checks"]), 2)

    def test_checks_staged_blob_even_if_worktree_was_shrunk(self):
        path = self.stage("fixture.txt", b"a" * (MAX_FILE_BYTES + 1))
        path.write_text("Küçük çalışma kopyası")
        self.assertFalse(inspect_index(self.root)["passed"])

    def test_accepts_staged_removal_of_forbidden_file(self):
        self.stage("depot_tools/tool.py")
        subprocess.run(["git", "rm", "--cached", "--", "depot_tools/tool.py"], cwd=self.root, check=True, capture_output=True)
        self.assertTrue(inspect_index(self.root)["passed"])


if __name__ == "__main__":
    unittest.main()
