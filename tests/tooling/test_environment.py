"""Hazır olmayan veya depo içine taşan ortamların hazır sayılmasını önler."""

import tempfile
import unittest
import plistlib
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from scripts.yuva_dev.environment import inspect_environment, workspace_problem


class EnvironmentTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.root = self.base / "yuva-browser"
        self.root.mkdir()

    def test_rejects_overlapping_workspace(self):
        for workspace in (self.root, self.root / "src", self.base):
            with self.subTest(workspace=workspace):
                self.assertIsNotNone(workspace_problem(workspace, self.root))

    def test_allows_absent_external_workspace_without_creating_it(self):
        workspace = self.base / "external"
        self.assertIsNone(workspace_problem(workspace, self.root))
        self.assertFalse(workspace.exists())

    def test_rejects_whitespace_and_file_destination(self):
        self.assertIsNotNone(workspace_problem(self.base / "with space", self.root))
        destination = self.base / "file"
        destination.write_text("Veri")
        self.assertIsNotNone(workspace_problem(destination, self.root))

    @patch("scripts.yuva_dev.environment.run_command", return_value=None)
    @patch("scripts.yuva_dev.environment.platform.machine", return_value="arm64")
    @patch("scripts.yuva_dev.environment.platform.system", return_value="Darwin")
    def test_missing_xcode_never_reports_ready(self, *mocks):
        report = inspect_environment(self.base / "external", self.root)
        self.assertFalse(report["preflight_ready"])
        self.assertFalse(report["build_verified"])
        self.assertTrue(any(item["id"] == "xcode" and item["status"] == "blocked" for item in report["checks"]))

    @patch("scripts.yuva_dev.environment.run_command", return_value=None)
    @patch("scripts.yuva_dev.environment.platform.machine", return_value="x86_64")
    @patch("scripts.yuva_dev.environment.platform.system", return_value="Linux")
    @patch("scripts.yuva_dev.environment.linux_identity", return_value={"ID": "pardus", "VERSION_ID": "25.2"})
    def test_pardus_is_distinct_and_not_implicitly_qualified(self, *mocks):
        report = inspect_environment(self.base / "external", self.root)
        self.assertEqual(report["platform"], "pardus")
        self.assertFalse(report["preflight_ready"])
        self.assertTrue(any(item["id"] == "pardus_release" for item in report["checks"]))

    @patch("scripts.yuva_dev.environment.run_command", return_value=None)
    @patch("scripts.yuva_dev.environment.platform.machine", return_value="x86_64")
    @patch("scripts.yuva_dev.environment.platform.system", return_value="Linux")
    @patch("scripts.yuva_dev.environment.linux_identity", return_value={"ID": "debian", "ID_LIKE": "pardus"})
    def test_generic_linux_does_not_count_as_pardus(self, *mocks):
        report = inspect_environment(self.base / "external", self.root)
        self.assertEqual(report["platform"], "linux")

    @patch("scripts.yuva_dev.environment.platform.machine", return_value="arm64")
    @patch("scripts.yuva_dev.environment.platform.system", return_value="Darwin")
    def test_apfs_is_checked_on_device_instead_of_regular_directory(self, *mocks):
        def probe(arguments, **kwargs):
            if arguments[0] == "df":
                return SimpleNamespace(returncode=0, stdout="Filesystem Blocks Used Available Capacity Mounted\n/dev/disk9s1 100 10 90 10% /Volumes/Fixture\n")
            if arguments == ["diskutil", "info", "-plist", "/dev/disk9s1"]:
                return SimpleNamespace(returncode=0, stdout=plistlib.dumps({"FilesystemType": "apfs"}).decode())
            return None
        with patch("scripts.yuva_dev.environment.run_command", side_effect=probe):
            report = inspect_environment(self.base / "external", self.root)
        self.assertTrue(any(item["id"] == "filesystem" and item["status"] == "pass" for item in report["checks"]))


if __name__ == "__main__":
    unittest.main()
