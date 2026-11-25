"""Offline native-readiness checks using synthetic directories; no client launch."""
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from workflow_engine.native_preflight import inspect_native


class NativePreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / "state"
        self.home.mkdir()
        env = patch.dict(os.environ, {"CODEX_HOME": str(self.home), "CODESPACES": "true"}, clear=True)
        env.start()
        self.addCleanup(env.stop)
        lookup = patch("workflow_engine.native_preflight.shutil.which", return_value="/synthetic/executable")
        lookup.start()
        self.addCleanup(lookup.stop)
        platform = patch("workflow_engine.native_preflight.sys.platform", "linux")
        platform.start()
        self.addCleanup(platform.stop)

    def test_writable_is_not_verified_startup(self):
        report = inspect_native()
        self.assertEqual(report["status"], "no-known-blocker")
        self.assertFalse(report["native_startup_verified"])
        self.assertTrue(report["codespaces_environment"])
        self.assertEqual(list(self.home.iterdir()), [])

    def test_read_only_mount_blocks_even_if_access_appears_allowed(self):
        with patch("os.statvfs", return_value=SimpleNamespace(f_flag=os.ST_RDONLY)), patch("os.access", return_value=True):
            report = inspect_native()
        self.assertEqual(report["status"], "blocked")
        self.assertEqual(report["state_locations"]["CODEX_HOME"]["status"], "read-only-mount")

    def test_access_failure_blocks(self):
        with patch("os.access", return_value=False):
            self.assertEqual(inspect_native()["state_locations"]["CODEX_HOME"]["status"], "not-writable")

    def test_missing_directory_blocks_without_creating_it(self):
        self.home.rmdir()
        self.assertEqual(inspect_native()["status"], "blocked")
        self.assertFalse(self.home.exists())

    def test_non_directory_blocks(self):
        self.home.rmdir()
        self.home.write_text("synthetic")
        self.assertEqual(inspect_native()["state_locations"]["CODEX_HOME"]["status"], "not-directory")

    def test_relative_override_blocks(self):
        os.environ["CODEX_SQLITE_HOME"] = "relative-state"
        self.assertEqual(inspect_native()["state_locations"]["CODEX_SQLITE_HOME"]["status"], "relative-path")

    def test_separate_sqlite_location_is_checked(self):
        os.environ["CODEX_SQLITE_HOME"] = str(self.home / "missing")
        report = inspect_native()
        self.assertEqual(report["status"], "blocked")
        self.assertEqual(report["state_locations"]["CODEX_SQLITE_HOME"]["source"], "environment")

    def test_missing_pilot_utility_blocks_pilot_only(self):
        with patch("workflow_engine.native_preflight.shutil.which", side_effect=lambda name: None if name == "timeout" else "/synthetic/executable"):
            self.assertEqual(inspect_native()["status"], "no-known-blocker")
            self.assertEqual(inspect_native(pilot=True)["status"], "blocked")

    def test_unknown_metadata_blocks(self):
        with patch("os.statvfs", side_effect=PermissionError("synthetic")):
            self.assertEqual(inspect_native()["status"], "blocked")

    def test_no_file_reads_or_subprocesses(self):
        marker = self.home / "auth.json"
        marker.write_text("synthetic-secret-marker")
        before = marker.read_bytes()
        with patch("pathlib.Path.open", side_effect=AssertionError("file read")), patch("subprocess.Popen", side_effect=AssertionError("subprocess")):
            report = inspect_native()
        self.assertNotIn("synthetic-secret-marker", str(report))
        self.assertEqual(marker.read_bytes(), before)
