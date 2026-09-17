"""Planın yan etkisiz kalmasını ve eksik hazırlığın başarıya dönüşmemesini sınar."""

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.yuva_dev.bootstrap import main
from scripts.yuva_dev.common import ToolError


class BootstrapTests(unittest.TestCase):
    def invoke(self, arguments):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = main([*arguments, "--format", "json"])
        return status, json.loads(output.getvalue())

    def test_plan_does_not_prepare_source_or_inspect_host(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "absent-workspace"
            with patch("scripts.yuva_dev.bootstrap.inspect_environment") as inspect:
                status, report = self.invoke(["--plan", "--workspace", str(workspace)])
                inspect.assert_not_called()
            self.assertEqual(status, 0)
            self.assertFalse(report["source_prepared"])
            self.assertFalse(report["plan"]["downloads_enabled"])
            self.assertFalse(workspace.exists())

    def test_ready_host_cannot_mask_unimplemented_preparation(self):
        with patch("scripts.yuva_dev.bootstrap.inspect_environment", return_value={"checks": [], "preflight_ready": True}):
            status, report = self.invoke([])
        self.assertEqual(status, 1)
        self.assertFalse(report["source_prepared"])
        self.assertEqual(report["checks"][-1]["id"], "source_preparation")

    def test_invalid_metadata_stops_before_host_inspection(self):
        with patch("scripts.yuva_dev.bootstrap.load_versions", side_effect=ToolError("Geçersiz kimlik")):
            with patch("scripts.yuva_dev.bootstrap.inspect_environment") as inspect:
                status, report = self.invoke([])
                inspect.assert_not_called()
        self.assertEqual(status, 1)
        self.assertFalse(report["source_prepared"])


if __name__ == "__main__":
    unittest.main()
