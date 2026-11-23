"""Offline fixtures for additive adoption, collision boundaries, and recovery."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "bootstrap.py"
SPEC = importlib.util.spec_from_file_location("project_bootstrap", SCRIPT)
bootstrap = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = bootstrap
SPEC.loader.exec_module(bootstrap)


def write(root, relative, content):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def snapshot(root):
    if not root.exists():
        return None
    return {path.relative_to(root).as_posix(): ("symlink", str(path.readlink())) if path.is_symlink()
            else ("file", path.read_bytes()) if path.is_file() else ("directory",)
            for path in sorted(root.rglob("*"))}


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.source = self.base / "template"
        self.target = self.base / "application"
        self.source.mkdir()
        for relative, content in {
            "workflows/consult.md": "# Consult\nRead [brief](../project/brief.md), [route](brownfield.md), and [template](../templates/project-brief.md).\n",
            "workflows/brownfield.md": "# Brownfield\nPreserve existing ownership.\n",
            "templates/project-brief.md": "# Project brief template\n",
            "templates/work.json": '{"schema_version": 1}\n',
            "workflow_engine/__init__.py": '"""Fixture package; not a runtime integration test."""\n',
            "workflow_engine/engine.py": "# Required fixture implementation module\n",
            "workflow_engine/context.py": "# Required fixture context projection module\n",
            "workflow_engine/specifications.py": "# Required fixture specification operations module\n",
            "workflow_engine/runner.py": "# Required fixture execution module\n",
            "workflow_engine/doctor.py": "# Required fixture local setup module\n",
            "workflow_engine/cli.py": "VALUE = 1\n",
            "scripts/workflow.py": "# Fixture wrapper\n",
            "scripts/codex_hooks.py": "# Optional read-only adapter\n",
            "docs/reference/native-hooks.md": "# Hook setup\nSeparate opt-in.\n",
            "guide/06-consultation-interview.md": "# Interview\npython3 scripts/workflow.py --root . context\n",
            "project/brief.md": "DO NOT COPY TEMPLATE PURPOSE\n",
            "delivery/current-handoff.md": "DO NOT COPY TEMPLATE HANDOFF\n",
            "specs/0001-foundation/tasks.md": "DO NOT COPY TEMPLATE BACKLOG\n",
            "evidence/0001-foundation/result.md": "DO NOT COPY TEMPLATE EVIDENCE\n",
            "docs/research/notes.md": "DO NOT COPY RESEARCH\n",
            ".codex/hooks.json": '{"enabled": true}\n',
            ".codex/config.toml": 'trust = "template-only"\n',
            ".codex/workflow.json": '{"active_work": "specs/0001-foundation"}\n',
            ".git/HEAD": "template revision\n",
        }.items():
            write(self.source, relative, content)
        for relative in bootstrap.REQUIRED:
            if not (self.source / relative).exists():
                write(self.source, relative, "# Required guidance fixture\n")

    def plan(self, mode="greenfield", **kwargs):
        return bootstrap.build_plan(self.source, self.target, mode, **kwargs)

    def install(self, mode="greenfield", **kwargs):
        plan = self.plan(mode, **kwargs)
        bootstrap.apply_plan(plan)
        return plan

    def test_greenfield_preview_has_no_effect_and_apply_starts_fresh(self):
        before_source = snapshot(self.source)
        plan = self.plan()
        self.assertFalse(self.target.exists())
        self.assertEqual(snapshot(self.source), before_source)
        self.assertEqual(plan.summary()["status"], "preview")
        bootstrap.apply_plan(plan)
        self.assertTrue((self.target / ".aws-workflow/workflow_engine/cli.py").is_file())
        self.assertFalse((self.target / "specs").exists())
        self.assertFalse((self.target / ".codex").exists())
        self.assertIn("/.workflow-state/", (self.target / ".gitignore").read_text())
        contents = "\n".join(path.read_text() for path in self.target.rglob("*") if path.is_file())
        self.assertNotIn("DO NOT COPY", contents)
        manifest = json.loads((self.target / bootstrap.MANIFEST).read_text())
        self.assertEqual(manifest["paths"]["brief"], ".aws-workflow/project/brief.md")
        self.assertEqual(manifest["identity"], "codex-aws-workflow")
        self.assertIn("Consultation has not started", (self.target / manifest["paths"]["brief"]).read_text())
        self.assertEqual(snapshot(self.source), before_source)

    def test_existing_git_directory_survives_greenfield(self):
        write(self.target, ".git/HEAD", "ref: refs/heads/main\n")
        self.install()
        self.assertEqual((self.target / ".git/HEAD").read_text(), "ref: refs/heads/main\n")

    def test_brownfield_preserves_instructions_code_state_and_configuration(self):
        originals = {
            "AGENTS.md": "# Existing instructions\r\nUse the established architecture.\r\n",
            "README.md": "Existing project\n", "src/main.py": "local_dirty_change = 1\n",
            "infrastructure/state.tfstate": '{"serial": 72}\n',
            ".github/workflows/release.yml": "name: Existing release\n",
            ".codex/config.toml": "existing = true\n", ".codex/hooks.json": '{"existing": true}\n',
            ".codex/workflow.json": '{"active_work": "specs/existing"}\n',
            "project/brief.md": "Existing canonical requirements and architecture\n",
            "delivery/current-handoff.md": "Existing continuation point\n",
        }
        for path, content in originals.items():
            write(self.target, path, content)
        saved = {path: (self.target / path).read_bytes() for path in originals}
        plan = self.install("brownfield")
        for path, content in saved.items():
            actual = (self.target / path).read_bytes()
            self.assertTrue(actual.startswith(content) if path == "AGENTS.md" else actual == content, path)
        self.assertEqual(plan.paths["brief"], "project/brief.md")
        self.assertFalse((self.target / ".aws-workflow/project/brief.md").exists())
        linked = (self.target / ".aws-workflow/workflows/consult.md").read_text()
        self.assertIn("../../project/brief.md", linked)

    def test_custom_authority_paths_are_mapped_without_migration(self):
        write(self.target, "architecture/product.md", "Existing product authority\n")
        write(self.target, "operations/resume.md", "Existing handoff\n")
        write(self.target, "backlog/README.md", "Existing canonical tasks\n")
        plan = self.install("brownfield", brief="architecture/product.md", handoff="operations/resume.md", authorities=["backlog"])
        self.assertEqual(plan.paths["brief"], "architecture/product.md")
        self.assertIn("`backlog`", (self.target / "AGENTS.md").read_text())
        self.assertEqual(self.plan("brownfield").writes, [])
        self.assertFalse((self.target / "specs").exists())

    def test_rerun_is_idempotent_and_preserves_project_edits(self):
        plan = self.install()
        write(self.target, plan.paths["brief"], "Now contains accepted application decisions.\n")
        with (self.target / "AGENTS.md").open("a") as stream:
            stream.write("\nAdditional project instruction.\n")
        before = snapshot(self.target)
        repeated = self.plan()
        self.assertEqual(repeated.writes, [])
        bootstrap.apply_plan(repeated)
        self.assertEqual(snapshot(self.target), before)
        self.assertEqual(repeated.summary()["status"], "unchanged")

    def test_changed_managed_file_blocks_without_side_effects(self):
        self.install()
        write(self.target, ".aws-workflow/workflows/consult.md", "Local customization\n")
        before = snapshot(self.target)
        with self.assertRaisesRegex(bootstrap.BootstrapError, "Content collisions"):
            self.plan()
        self.assertEqual(snapshot(self.target), before)

    def test_missing_managed_file_is_not_silently_recreated(self):
        self.install()
        (self.target / ".aws-workflow/workflows/consult.md").unlink()
        before = snapshot(self.target)
        with self.assertRaisesRegex(bootstrap.BootstrapError, "installed file missing"):
            self.plan()
        self.assertEqual(snapshot(self.target), before)

    def test_source_updates_require_explicit_review(self):
        self.install()
        write(self.source, "workflows/consult.md", "Updated workflow\n")
        before = snapshot(self.target)
        with self.assertRaisesRegex(bootstrap.BootstrapError, "explicit update/merge"):
            self.plan()
        self.assertEqual(snapshot(self.target), before)

    def test_missing_required_runtime_module_blocks_before_writes(self):
        for name in ("engine.py", "context.py", "specifications.py", "runner.py", "doctor.py"):
            with self.subTest(module=name):
                path = self.source / "workflow_engine" / name
                original = path.read_bytes()
                path.unlink()
                with self.assertRaisesRegex(bootstrap.BootstrapError, "workflow_engine/" + name):
                    self.plan()
                self.assertFalse(self.target.exists())
                path.write_bytes(original)

    def test_missing_required_consultation_guidance_blocks_before_writes(self):
        (self.source / "workflows/feature.md").unlink()
        before = snapshot(self.target)
        with self.assertRaisesRegex(bootstrap.BootstrapError, "workflows/feature.md"):
            self.plan()
        self.assertEqual(snapshot(self.target), before)

    def test_runtime_ignore_appends_preserving_bytes_and_project_edits(self):
        original = b"# Existing project ignores\r\nnode_modules/\r\n.env"
        self.target.mkdir()
        (self.target / ".gitignore").write_bytes(original)
        self.install("brownfield")
        actual = (self.target / ".gitignore").read_bytes()
        self.assertTrue(actual.startswith(original))
        self.assertEqual(actual.count(bootstrap.IGNORE_BEGIN.encode()), 1)
        with (self.target / ".gitignore").open("ab") as stream:
            stream.write(b"\n# User addition\nartifacts/\n")
        before = snapshot(self.target)
        self.assertEqual(self.plan("brownfield").writes, [])
        self.assertEqual(snapshot(self.target), before)

    def test_modified_runtime_ignore_requires_merge_without_writes(self):
        self.install()
        path = self.target / ".gitignore"
        path.write_text(path.read_text().replace("/.workflow-state/", "!/runtime/"))
        before = snapshot(self.target)
        with self.assertRaisesRegex(bootstrap.BootstrapError, "runtime ignore block changed"):
            self.plan()
        self.assertEqual(snapshot(self.target), before)

    def test_unowned_runtime_ignore_markers_block_adoption(self):
        write(self.target, ".gitignore", bootstrap.IGNORE_BLOCK + "\n")
        before = snapshot(self.target)
        with self.assertRaisesRegex(bootstrap.BootstrapError, "ignore markers are ambiguous"):
            self.plan("brownfield")
        self.assertEqual(snapshot(self.target), before)

    def test_runtime_ignore_concurrent_edit_is_preserved(self):
        write(self.target, ".gitignore", ".env\n")
        plan = self.plan("brownfield")
        write(self.target, ".gitignore", ".env\n# Concurrent change\n")
        before = snapshot(self.target)
        with self.assertRaisesRegex(bootstrap.BootstrapError, "changed since preview"):
            bootstrap.apply_plan(plan)
        self.assertEqual(snapshot(self.target), before)

    def test_source_inventory_error_cannot_silently_omit_guidance(self):
        actual_walk = bootstrap.os.walk

        def denied_walk(directory, *, followlinks=False, onerror=None):
            if Path(directory) == self.source / "guide":
                error = PermissionError("fixture: selected guidance cannot be listed")
                if onerror is not None:
                    onerror(error)
                return iter(())
            return actual_walk(directory, followlinks=followlinks, onerror=onerror)

        before = snapshot(self.source)
        with mock.patch.object(bootstrap.os, "walk", side_effect=denied_walk):
            with self.assertRaisesRegex(bootstrap.BootstrapError, "completely inventory"):
                self.plan()
        self.assertEqual(snapshot(self.source), before)
        self.assertFalse(self.target.exists())

    def test_instruction_marker_conflict_blocks_before_any_writes(self):
        write(self.target, "AGENTS.md", "User content\n" + bootstrap.BEGIN + "\ncustom block\n" + bootstrap.END)
        before = snapshot(self.target)
        with self.assertRaisesRegex(bootstrap.BootstrapError, "manual merge required"):
            self.plan("brownfield")
        self.assertEqual(snapshot(self.target), before)

    def test_existing_namespace_is_not_claimed_or_overwritten(self):
        write(self.target, ".aws-workflow/local.md", "User-owned namespace\n")
        before = snapshot(self.target)
        with self.assertRaisesRegex(bootstrap.BootstrapError, "already exists"):
            self.plan("brownfield")
        self.assertEqual(snapshot(self.target), before)

    def test_greenfield_does_not_adopt_a_populated_application(self):
        write(self.target, "README.md", "Existing project\n")
        before = snapshot(self.target)
        with self.assertRaisesRegex(bootstrap.BootstrapError, "not empty"):
            self.plan()
        self.assertEqual(snapshot(self.target), before)

    def test_traversal_and_overlapping_roots_are_rejected(self):
        for source, target in ((self.source, self.source), (self.source, self.source / "child"),
                               (self.source, self.base), (self.source, self.base / "unused/../escape")):
            with self.subTest(source=source, target=target):
                with self.assertRaises(bootstrap.BootstrapError):
                    bootstrap.build_plan(source, target, "greenfield")
        self.target.mkdir()
        for kwargs in ({"brief": "../outside.md"}, {"handoff": "/tmp/outside.md"}, {"authorities": [".git/HEAD"]}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(bootstrap.BootstrapError):
                    self.plan("brownfield", **kwargs)
        self.assertEqual(snapshot(self.target), {})

    def test_symlink_target_or_source_asset_is_rejected(self):
        outside = self.base / "outside"
        outside.mkdir()
        self.target.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(bootstrap.BootstrapError, "Symlink"):
            self.plan("brownfield")
        self.target.unlink()
        self.target.mkdir()
        (self.target / "AGENTS.md").symlink_to(self.source / "project/brief.md")
        with self.assertRaisesRegex(bootstrap.BootstrapError, "Symlink"):
            self.plan("brownfield")
        (self.target / "AGENTS.md").unlink()
        (self.source / "templates/external.md").symlink_to(self.source / "project/brief.md")
        with self.assertRaisesRegex(bootstrap.BootstrapError, "Symlink"):
            self.plan("brownfield")
        self.assertEqual(snapshot(outside), {})

    def test_dangling_symlink_output_parent_is_rejected(self):
        self.target.mkdir()
        (self.target / "project").symlink_to(self.base / "missing", target_is_directory=True)
        before = snapshot(self.target)
        with self.assertRaisesRegex(bootstrap.BootstrapError, "Symlink"):
            self.plan("brownfield")
        self.assertEqual(snapshot(self.target), before)

    def test_existing_target_changes_between_preview_and_apply_are_preserved(self):
        write(self.target, "AGENTS.md", "Original\n")
        plan = self.plan("brownfield")
        write(self.target, "AGENTS.md", "Concurrent user change\n")
        before = snapshot(self.target)
        with self.assertRaisesRegex(bootstrap.BootstrapError, "changed since preview"):
            bootstrap.apply_plan(plan)
        self.assertEqual(snapshot(self.target), before)

    def test_write_failure_rolls_back_additions_and_restores_instructions(self):
        write(self.target, "AGENTS.md", "Exact original content\n")
        write(self.target, ".gitignore", ".env\n# Existing ignore bytes\n")
        write(self.target, "src/main.py", "Preserved dirty code\n")
        before = snapshot(self.target)
        plan = self.plan("brownfield")
        actual_link = bootstrap.os.link

        def fail_manifest(source, destination, **kwargs):
            if Path(destination).name == "manifest.json":
                raise OSError("simulated final write failure")
            return actual_link(source, destination, **kwargs)

        with mock.patch.object(bootstrap.os, "link", side_effect=fail_manifest):
            with self.assertRaisesRegex(bootstrap.BootstrapError, "rolled back"):
                bootstrap.apply_plan(plan)
        self.assertEqual(snapshot(self.target), before)

    def test_link_rewrite_preserves_local_targets_and_records_excluded_references(self):
        write(self.source, "guide/sample.md", "[Application](../project/brief.md)\n[Framework backlog](../specs/0001-foundation/tasks.md)\n[Public](https://docs.aws.amazon.com/)\n")
        plan = self.install()
        copied = (self.target / ".aws-workflow/guide/sample.md").read_text()
        self.assertIn("[Application](../project/brief.md)", copied)
        self.assertIn("Framework backlog (template reference omitted)", copied)
        self.assertIn("[Public](https://docs.aws.amazon.com/)", copied)
        self.assertEqual(plan.omitted_references, ["guide/sample.md: ../specs/0001-foundation/tasks.md"])
        commands = (self.target / ".aws-workflow/guide/06-consultation-interview.md").read_text()
        self.assertIn("python3 .aws-workflow/scripts/workflow.py", commands)

    def test_cli_is_dry_run_by_default_and_json_errors_are_bounded(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--source", str(self.source), "--target", str(self.target), "--mode", "greenfield", "--json"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "preview")
        self.assertFalse(self.target.exists())
        failure = subprocess.run([sys.executable, str(SCRIPT), "--source", str(self.source), "--target", str(self.target), "--mode", "brownfield", "--json"], capture_output=True, text=True)
        self.assertEqual(failure.returncode, 1)
        self.assertEqual(json.loads(failure.stdout)["status"], "blocked")
        self.assertFalse(self.target.exists())


if __name__ == "__main__":
    unittest.main()
