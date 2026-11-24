"""Read-only setup findings and optional hook preview, with no external probes."""

import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

from workflow_engine.doctor import GUIDANCE_FILES, INSTRUCTION_BEGIN, INSTRUCTION_END, RUNTIME_FILES, hook_preview, inspect_environment
from workflow_engine.engine import CONTEXT_DEFAULTS, WorkflowError, new_work


def write(root, relative, content):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file() and not p.is_symlink()}


class DoctorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "application"
        self.root.mkdir()

    def source(self):
        for relative in (*RUNTIME_FILES, *GUIDANCE_FILES):
            write(self.root, relative, "# Local fixture; never imported by doctor\n")
        write(self.root, "scripts/codex_hooks.py", "# Local fixture hook\n")
        write(self.root, "AGENTS.md", "# Project instructions\n")
        for relative in CONTEXT_DEFAULTS.values():
            write(self.root, relative, "# Existing project context\n")
        return self.root

    def adopted(self):
        managed = {}
        for relative in (*RUNTIME_FILES, *GUIDANCE_FILES, "scripts/codex_hooks.py"):
            path = write(self.root, ".aws-workflow/" + relative, "# Local fixture\n")
            managed[path.relative_to(self.root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        paths = {key: ".aws-workflow/" + relative for key, relative in CONTEXT_DEFAULTS.items()}
        for relative in paths.values():
            write(self.root, relative, "# Application context\n")
        paths.update({"specifications": "specs", "evidence": "evidence", "decisions": "docs/decisions"})
        block = INSTRUCTION_BEGIN + "\nFixture entry instructions\n" + INSTRUCTION_END
        write(self.root, ".aws-workflow/manifest.json", json.dumps({"schema_version": 1, "identity": "codex-aws-workflow", "paths": paths, "managed_files": managed, "agent_block_sha256": hashlib.sha256(block.encode()).hexdigest()}))
        write(self.root, "AGENTS.md", "# Project instructions\n" + block + "\n")
        return paths

    def inspect(self):
        return inspect_environment(self.root, executable_lookup=lambda name: None)

    def test_empty_application_reports_required_setup_and_no_selection(self):
        report = self.inspect()
        self.assertFalse(report["session_ready"])
        self.assertEqual(report["layout"], "uninstalled")
        self.assertIsNone(report["active_work"])
        self.assertEqual(next(c for c in report["checks"] if c["id"] == "active-work")["status"], "not-selected")
        self.assertEqual(list(self.root.iterdir()), [])

    def test_source_ready_without_git_codex_hooks_or_active_work(self):
        self.source()
        before = snapshot(self.root)
        report = self.inspect()
        self.assertTrue(report["session_ready"])
        self.assertIsNone(report["active_work"])
        self.assertEqual(next(c for c in report["checks"] if c["id"] == "codex-executable")["status"], "missing")
        self.assertEqual(next(c for c in report["checks"] if c["id"] == "native-hooks")["status"], "not-tested")
        self.assertEqual(snapshot(self.root), before)

    def test_adopted_records_and_runtime_hashes_are_checked(self):
        paths = self.adopted()
        (self.root / ".aws-workflow/guide/08-aws-emulator.md").unlink()
        self.assertTrue(self.inspect()["session_ready"])
        write(self.root, paths["brief"], "# User-edited real project brief\n")
        self.assertTrue(self.inspect()["session_ready"])
        write(self.root, ".aws-workflow/workflow_engine/runner.py", "# Changed package\n")
        report = self.inspect()
        self.assertFalse(report["session_ready"])
        package = next(c for c in report["checks"] if c["id"] == "package")
        self.assertEqual(package["changed_files"], [".aws-workflow/workflow_engine/runner.py"])

    def test_foundation_mappings_checked_on_first_use_and_unsafe_paths_reported(self):
        self.adopted()
        manifest_path = self.root / ".aws-workflow/manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["schema_version"] = 2
        for key in ("requirements", "tech", "structure", "architecture"):
            manifest["paths"][key] = f"established/{key}.md"
            write(self.root, manifest["paths"][key], "# Existing project decision\n")
        manifest_path.write_text(json.dumps(manifest))
        before = snapshot(self.root)
        report = self.inspect()
        self.assertTrue(report["session_ready"])
        self.assertIsNone(report["active_work"])
        context = next(item for item in report["checks"] if item["id"] == "project-context")
        self.assertEqual(context["paths"]["architecture"], "established/architecture.md")
        self.assertEqual(snapshot(self.root), before)

        for key in ("02-aws-guidance-and-access", "08-aws-emulator"):
            relative = f".aws-workflow/guide/{key}.md"
            guide = self.root / relative
            original = guide.read_bytes()
            guide.write_bytes(original + b"edited")
            package = next(item for item in self.inspect()["checks"] if item["id"] == "package")
            self.assertEqual(package["changed_files"], [relative])
            guide.unlink()
            package = next(item for item in self.inspect()["checks"] if item["id"] == "package")
            self.assertEqual(package["missing_files"], [relative])
            guide.write_bytes(original)

        for path in ("../outside.md", "missing.md", manifest["paths"]["brief"], "established//tech.md"):
            with self.subTest(path=path):
                manifest["paths"]["architecture"] = path
                manifest_path.write_text(json.dumps(manifest))
                report = self.inspect()
                self.assertFalse(report["session_ready"])
                self.assertEqual(next(item for item in report["checks"] if item["id"] == "project-context")["status"], "missing")

    def test_missing_runtime_module_and_mapped_context_report_exact_gaps(self):
        paths = self.adopted()
        (self.root / ".aws-workflow/workflow_engine/specifications.py").unlink()
        (self.root / paths["handoff"]).unlink()
        report = self.inspect()
        self.assertFalse(report["session_ready"])
        self.assertIn("handoff", next(c for c in report["checks"] if c["id"] == "project-context")["detail"])
        self.assertIn(".aws-workflow/workflow_engine/specifications.py", next(c for c in report["checks"] if c["id"] == "package")["missing_files"])

    def test_required_consultation_guidance_cannot_be_missing_or_silently_changed(self):
        self.adopted()
        relative = ".aws-workflow/workflows/consult.md"
        path = self.root / relative
        path.unlink()
        report = self.inspect()
        self.assertFalse(report["session_ready"])
        self.assertIn(relative, next(c for c in report["checks"] if c["id"] == "package")["missing_files"])
        path.write_text("# Unreviewed replacement procedure\n")
        report = self.inspect()
        self.assertFalse(report["session_ready"])
        self.assertIn(relative, next(c for c in report["checks"] if c["id"] == "package")["changed_files"])

    def test_changed_managed_instructions_require_review_but_external_edits_do_not(self):
        self.adopted()
        path = self.root / "AGENTS.md"
        path.write_text(path.read_text() + "\n# User instruction outside the managed block\n")
        self.assertTrue(self.inspect()["session_ready"])
        path.write_text(path.read_text().replace("Fixture entry instructions", "Different managed instructions"))
        report = self.inspect()
        self.assertFalse(report["session_ready"])
        self.assertEqual(next(c for c in report["checks"] if c["id"] == "instructions")["status"], "invalid")

    def test_invalid_or_unsafe_manifest_is_reported_without_reading_outside(self):
        paths = self.adopted()
        path = self.root / ".aws-workflow/manifest.json"
        data = json.loads(path.read_text())
        data["paths"]["brief"] = "../outside.md"
        path.write_text(json.dumps(data))
        self.assertFalse(self.inspect()["session_ready"])
        path.write_text("{invalid")
        self.assertFalse(self.inspect()["session_ready"])
        self.assertEqual(next(c for c in self.inspect()["checks"] if c["id"] == "package")["status"], "invalid")

    def test_active_draft_is_detected_and_invalid_pointer_is_not_replaced(self):
        self.source()
        new_work(self.root, "0100-example", "Example", activate=True)
        report = self.inspect()
        self.assertEqual(report["active_work"], {"id": "0100-example", "phase": "consultation"})
        self.assertTrue(report["session_ready"])
        pointer = self.root / ".codex/workflow.json"
        pointer.write_text('{"schema_version":1,"active_work":"../escape"}')
        before = snapshot(self.root)
        self.assertFalse(self.inspect()["session_ready"])
        self.assertEqual(snapshot(self.root), before)

    def test_symlink_runtime_and_instruction_files_are_not_followed(self):
        self.source()
        outside = Path(self.temp.name) / "outside.py"
        outside.write_text("Outside content must remain untouched\n")
        path = self.root / "workflow_engine/runner.py"
        path.unlink()
        path.symlink_to(outside)
        self.assertFalse(self.inspect()["session_ready"])
        self.assertEqual(outside.read_text(), "Outside content must remain untouched\n")

    def test_no_subprocess_or_credential_configuration_reads(self):
        self.source()
        secrets = {".codex/config.toml", ".aws/credentials", ".env"}
        for relative in secrets:
            write(self.root, relative, "fixture-secret-marker")
        actual_read = Path.read_text

        def guarded_read(path, *args, **kwargs):
            self.assertNotIn(path.relative_to(self.root).as_posix(), secrets)
            return actual_read(path, *args, **kwargs)

        names = []
        with mock.patch.object(Path, "read_text", guarded_read), mock.patch.object(subprocess, "Popen", side_effect=AssertionError("No subprocess allowed")):
            report = inspect_environment(self.root, executable_lookup=lambda name: names.append(name) or "/fixture/bin/" + name)
        self.assertTrue(report["session_ready"])
        self.assertEqual(names, ["git", "codex"])
        self.assertNotIn("fixture-secret-marker", json.dumps(report))

    def test_runtime_ignore_is_presence_only_not_effective_git_proof(self):
        self.source()
        write(self.root, ".gitignore", "/.workflow-state/\n!/.workflow-state/\n")
        rule = next(c for c in self.inspect()["checks"] if c["id"] == "runtime-ignore")
        self.assertEqual(rule["status"], "present")
        self.assertIn("negation", rule["detail"])

    def test_hook_preview_uses_installed_path_without_creating_config(self):
        self.adopted()
        before = snapshot(self.root)
        preview = hook_preview(self.root)
        self.assertEqual(preview["existing_configuration"], "absent")
        command = preview["configuration"]["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        self.assertIn("/.aws-workflow/scripts/codex_hooks.py", command)
        self.assertEqual(snapshot(self.root), before)
        self.assertFalse((self.root / ".codex").exists())

    def test_existing_equivalent_or_different_hooks_require_no_blind_write(self):
        self.source()
        proposal = hook_preview(self.root)["configuration"]
        path = write(self.root, ".codex/hooks.json", json.dumps(proposal))
        self.assertEqual(hook_preview(self.root)["existing_configuration"], "equivalent")
        path.write_text('{"hooks":{"OtherEvent":[]}}')
        before = snapshot(self.root)
        self.assertEqual(hook_preview(self.root)["existing_configuration"], "merge-required")
        self.assertEqual(snapshot(self.root), before)
        path.write_text("{bad")
        self.assertEqual(hook_preview(self.root)["existing_configuration"], "invalid")

    def test_hook_preview_requires_an_installed_handler(self):
        with self.assertRaises(WorkflowError):
            hook_preview(self.root)
        self.source()
        (self.root / "scripts/codex_hooks.py").unlink()
        with self.assertRaisesRegex(WorkflowError, "missing"):
            hook_preview(self.root)


if __name__ == "__main__":
    unittest.main()
