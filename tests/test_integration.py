"""Exercise the real reusable package and event command, without Codex or AWS."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_repository


def snapshot(root):
    return {path.relative_to(root).as_posix(): path.read_bytes()
            for path in root.rglob("*") if path.is_file()}


class PackageIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def run_tool(self, script, arguments, cwd):
        result = subprocess.run([sys.executable, str(script), *arguments], cwd=cwd,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        return json.loads(result.stdout)

    def install(self, target, mode):
        arguments = ["--source", str(ROOT), "--target", str(target), "--mode", mode, "--json"]
        self.run_tool(ROOT / "scripts/bootstrap.py", arguments + ["--apply"], ROOT)
        return arguments

    def test_real_package_context_links_preservation_and_idempotence(self):
        for mode in ("greenfield", "brownfield"):
            with self.subTest(mode=mode):
                target = self.base / mode
                target.mkdir()
                if mode == "brownfield":
                    (target / "AGENTS.md").write_text("# Existing instructions\nPreserve our architecture.\n")
                    (target / "application.txt").write_text("Uncommitted user work\n")
                    (target / ".codex").mkdir()
                    (target / ".codex/config.toml").write_text("# Existing client configuration\n")
                original = snapshot(target)
                arguments = ["--source", str(ROOT), "--target", str(target), "--mode", mode, "--json"]
                self.run_tool(ROOT / "scripts/bootstrap.py", arguments, ROOT)
                self.assertEqual(snapshot(target), original)
                self.install(target, mode)
                self.assertFalse((target / ".codex/hooks.json").exists())
                self.assertFalse((target / "specs").exists())
                for path, content in original.items():
                    if path == "AGENTS.md":
                        self.assertTrue((target / path).read_bytes().startswith(content))
                    else:
                        self.assertEqual((target / path).read_bytes(), content)
                manifest = json.loads((target / ".aws-workflow/manifest.json").read_text())
                cli = target / ".aws-workflow/scripts/workflow.py"
                self.run_tool(cli, ["--root", str(target), "new", "0100-example", "--title", "Example scope", "--mode", mode,
                                    "--route", "quick", "--idea", "The actual supplied outcome", "--activate", "--json"], target)
                after_create = snapshot(target)
                for command in ("context", "status", "validate"):
                    report = self.run_tool(cli, ["--root", str(target), command, "--json"], target)
                    self.assertEqual(report["id"], "0100-example")
                    self.assertIn(manifest["paths"]["brief"], report["context_files"])
                    self.assertIn(manifest["paths"]["handoff"], report["context_files"])
                    self.assertEqual(report["phase"], "consultation")
                compact = self.run_tool(cli, ["--root", str(target), "context", "--compact", "--json"], target)
                self.assertEqual(compact["work"]["id"], "0100-example")
                self.assertIn({"kind": "context", "path": manifest["paths"]["brief"]}, compact["sources"])
                self.assertEqual(snapshot(target), after_create)
                rerun = self.run_tool(ROOT / "scripts/bootstrap.py", arguments + ["--apply"], ROOT)
                self.assertEqual(rerun["changes"], [])
                self.assertEqual(snapshot(target), after_create)
                with patch.object(check_repository, "REQUIRED_CORE_PATHS", ()):
                    report = check_repository.check_repository(target)
                self.assertEqual(report.issues, [], str(report.issues))

    @unittest.skipUnless(shutil.which("git"), "The supplied native command requires Git")
    def test_documented_git_root_hook_command_from_nested_adopted_directory(self):
        target = self.base / "app"
        self.install(target, "greenfield")
        subprocess.run(["git", "init", "--quiet", str(target)], check=True, capture_output=True)
        cli = target / ".aws-workflow/scripts/workflow.py"
        self.run_tool(cli, ["--root", str(target), "new", "0100-example", "--title", "Example scope", "--route", "quick", "--activate", "--json"], target)
        nested = target / "src" / "nested"
        nested.mkdir(parents=True)
        config = json.loads((ROOT / ".codex/hooks.json").read_text())
        before = snapshot(target)
        startup_fingerprint = None
        for event in ("SessionStart", "UserPromptSubmit", "Stop"):
            command = config["hooks"][event][0]["hooks"][0]["command"].replace("/scripts/codex_hooks.py", "/.aws-workflow/scripts/codex_hooks.py")
            result = subprocess.run(command, shell=True, cwd=nested, input=json.dumps({"hook_event_name": event, "cwd": str(nested)}),
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            output = json.loads(result.stdout)
            if event != "Stop":
                context = output["hookSpecificOutput"]["additionalContext"]
                self.assertIn("0100-example", context)
                packet = json.loads(context)
                if event == "SessionStart":
                    startup_fingerprint = packet["fingerprint"]
                    paths = json.loads((target / ".aws-workflow/manifest.json").read_text())["paths"]
                    selected = {source["path"] for source in packet["sources"]}
                    self.assertIn(paths["brief"], selected)
                    self.assertIn(paths["handoff"], selected)
                    self.assertLessEqual(len(context), 6000)
                else:
                    self.assertEqual(packet["fingerprint"], startup_fingerprint)
                    self.assertIn("context --compact", packet["refresh"])
                    self.assertLessEqual(len(context), 1200)
            self.assertNotIn("decision", output)
            self.assertNotIn("continue", output)
        self.assertEqual(snapshot(target), before)


if __name__ == "__main__":
    unittest.main()
