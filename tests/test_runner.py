"""Controller integration fixtures use fake authors and actual local Git/checks."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from workflow_engine.engine import WorkflowError, advance, inspect_work, new_work, record_review
from workflow_engine.runner import (CodexBackend, abandon_run, apply_run, execute_run,
                                    execution_template, inspect_run, plan_run)
from workflow_engine.runner import _process


def git(root, *argv):
    result = subprocess.run(["git", "-C", str(root), *argv], text=True, capture_output=True)
    if result.returncode:
        raise AssertionError(result.stderr)
    return result.stdout.strip()


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.work_id = "0100-runner-fixture"
        (self.root / ".gitignore").write_text(".workflow-state/\n__pycache__/\n*.pyc\nignored/\n")
        (self.root / "README.md").write_text("Preserve this application.\n")
        (self.root / "authority.md").write_text("Fixture only: simulated owner authorizes local implementation and checks.\n")
        (self.root / "src").mkdir()
        for letter in "abc":
            (self.root / "src" / f"{letter}.txt").write_text("0")
        new_work(self.root, self.work_id, "Runner fixture", route="quick", activate=True)
        self.work = self.root / "specs" / self.work_id
        (self.work / "requirements.md").write_text("# Requirements\n\n| ID | Outcome |\n| --- | --- |\n| REQ-001 | Produce the declared local results and preserve unrelated files. |\n")
        (self.work / "design.md").write_text("# Design\n\n## DES-001 — Local files\n\nUse isolated task edits and verify the integrated values.\n")
        sections = []
        for index, letter in enumerate("abc", 1):
            key = f"T-{index:03d}"
            deps = "T-001, T-002" if index == 3 else "none"
            sections.append(f"""### {key} — Set result {letter}

- [ ] {key} complete
- Activity: ready
- Contract / design: REQ-001 / DES-001
- Prerequisites: {deps}
- Scope and exclusions: Change the declared local file only.
- Acceptance: The declared value is present and earlier values remain valid.
- Verification: CHK-{index:03d}
- Evidence / review: none
- Blocker: none
""")
        matrix = "\n## Verification matrix\n\n| Check | Requirement | Task | Method | Evidence |\n| --- | --- | --- | --- | --- |\n"
        for index in range(1, 4):
            matrix += f"| CHK-{index:03d} | REQ-001 | T-{index:03d} | Read the declared value and assert its expected content. | Not run |\n"
        (self.work / "tasks.md").write_text("# Task fixture\n\n" + "\n".join(sections) + matrix)
        advance(self.root, self.work_id, "tasks")
        record_review(self.root, self.work_id, "tasks", "accepted", "authority.md", "Fixture author", "delegated")
        advance(self.root, self.work_id, "implementation")
        self.config = {
            "schema_version": 1, "authority_ref": "authority.md",
            "limits": {"max_workers": 2, "max_tasks": 3, "timeout_seconds": 20, "check_timeout_seconds": 3},
            "tasks": {}, "integration_checks": [
                {"name": "preserved-readme", "argv": [sys.executable, "-c", "from pathlib import Path; assert Path('README.md').read_text() == 'Preserve this application.\\n'"], "inputs": ["README.md"]}
            ],
        }
        for index, letter in enumerate("abc", 1):
            self.config["tasks"][f"T-{index:03d}"] = {
                "write_paths": [f"src/{letter}.txt"],
                "checks": [{"id": f"CHK-{index:03d}", "argv": [sys.executable, "-c", f"from pathlib import Path; assert Path('src/{letter}.txt').read_text().startswith('{letter.upper()}')"], "inputs": [f"src/{letter}.txt"]}],
            }
        self.write_config()
        git(self.root, "init", "-q")
        git(self.root, "config", "user.name", "Fixture")
        git(self.root, "config", "user.email", "fixture@example.invalid")
        git(self.root, "config", "commit.gpgsign", "false")
        self.commit()

    def write_config(self):
        (self.work / "execution.json").write_text(json.dumps(self.config, indent=2) + "\n")

    def commit(self):
        git(self.root, "add", "--all")
        git(self.root, "commit", "-qm", "Fixture candidate")

    def backend(self, request):
        index = int(request["task_id"].split("-")[1]) - 1
        root = Path(request["workspace"])
        if index == 2:
            self.assertEqual((root / "src/a.txt").read_text(), "A")
            self.assertEqual((root / "src/b.txt").read_text(), "B")
        (root / f"src/{'abc'[index]}.txt").write_text("ABC"[index])
        return {"task_id": request["task_id"], "status": "ready", "summary": "Fixture author supplied the requested local edit.", "acceptance": "satisfied"}

    def test_draft_has_explicit_empty_authority_commands_and_scopes(self):
        draft = execution_template(self.root)
        self.assertEqual(draft["authority_ref"], "")
        self.assertEqual(draft["tasks"]["T-001"]["write_paths"], [])
        self.assertEqual(draft["tasks"]["T-001"]["checks"][0]["argv"], [])
        self.assertFalse((self.root / ".workflow-state").exists())

    def test_preview_is_read_only_and_never_invokes_backend(self):
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        plan = execute_run(self.root, backend=lambda _: self.fail("Preview invoked backend"))
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertTrue(plan["ready"], plan)
        self.assertEqual(plan["waves"], [["T-001", "T-002"], ["T-003"]])
        self.assertEqual(plan["model_calls"], 0)

    def test_parallel_wave_and_dependency_execute_in_isolated_candidate(self):
        barrier = threading.Barrier(2)
        spaces = []

        def concurrent(request):
            spaces.append(request["workspace"])
            if request["task_id"] in ("T-001", "T-002"):
                barrier.wait(timeout=3)
            return self.backend(request)

        original = git(self.root, "rev-parse", "HEAD")
        result = execute_run(self.root, execute=True, backend=concurrent, run_id="parallel-fixture")
        self.assertEqual(result["status"], "ready", result.get("failure"))
        self.assertEqual(len(set(spaces)), 3)
        self.assertEqual(result["attempts_started"], 3)
        self.assertEqual(git(self.root, "rev-parse", "HEAD"), original)
        self.assertEqual((self.root / "src/a.txt").read_text(), "0")
        report = inspect_work(Path(result["candidate_path"]), self.work_id)
        self.assertTrue(all(task["completion_valid"] for task in report["tasks"]))
        self.assertEqual(report["issues"], [])
        applied = apply_run(self.root, "parallel-fixture")
        self.assertEqual(applied["status"], "applied")
        self.assertEqual((self.root / "src/c.txt").read_text(), "C")
        self.assertEqual(git(self.root, "status", "--porcelain"), "")

    def test_overlapping_scopes_serialize_independent_tasks(self):
        self.config["tasks"]["T-001"]["write_paths"] = ["src/"]
        self.write_config()
        self.commit()
        self.assertEqual(plan_run(self.root)["waves"], [["T-001"], ["T-002"], ["T-003"]])

    def test_single_task_does_not_run_unfinished_prerequisites(self):
        self.assertFalse(plan_run(self.root, task_id="T-003")["ready"])
        result = execute_run(self.root, task_id="T-001", execute=True, backend=self.backend)
        self.assertEqual(result["status"], "ready", result.get("failure"))
        self.assertEqual(result["completed_tasks"], ["T-001"])

    def test_native_preflight_blocks_before_run_reservation(self):
        with patch("workflow_engine.native_preflight.inspect_native", return_value={"status": "blocked", "blockers": ["CODEX_HOME: read-only-mount"]}), patch("workflow_engine.runner.CodexBackend", side_effect=AssertionError("native launch")):
            with self.assertRaisesRegex(WorkflowError, "read-only-mount"):
                execute_run(self.root, task_id="T-001", execute=True, run_id="blocked-native")
        self.assertFalse((self.root / ".workflow-state").exists())

    def test_default_backend_pins_the_launcher_codex_path(self):
        relative_executable = "linked-bin/../selected-bin/codex"
        launcher_executable = Path.cwd() / relative_executable

        def fake_author(backend, request):
            self.assertEqual(Path(backend.executable), launcher_executable)
            self.assertNotEqual(Path(request["workspace"]), Path.cwd())
            return self.backend(request)

        with (
            patch("workflow_engine.native_preflight.inspect_native", return_value={"status": "no-known-blocker"}),
            patch("shutil.which", return_value=relative_executable),
            patch.object(CodexBackend, "__call__", fake_author),
        ):
            result = execute_run(self.root, task_id="T-001", execute=True)
        self.assertEqual(result["status"], "ready", result.get("failure"))

    def test_falsy_injected_backend_is_used_without_native_dispatch(self):
        backend = MagicMock(side_effect=self.backend)
        backend.__bool__.return_value = False
        with patch.object(CodexBackend, "__call__", side_effect=AssertionError("Native dispatch attempted")) as native:
            result = execute_run(self.root, task_id="T-001", execute=True, backend=backend)
        self.assertEqual(result["status"], "ready", result.get("failure"))
        backend.assert_called_once()
        native.assert_not_called()

    def test_dirty_original_blocks_without_touching_user_work(self):
        path = self.root / "README.md"
        path.write_text("User edit")
        with self.assertRaisesRegex(WorkflowError, "clean committed"):
            execute_run(self.root, execute=True, backend=lambda _: self.fail("Blocked run launched"))
        self.assertEqual(path.read_text(), "User edit")
        self.assertFalse((self.root / ".workflow-state").exists())

    def test_missing_ignore_rule_blocks_execution(self):
        (self.root / ".gitignore").write_text("__pycache__/\n")
        self.commit()
        self.assertFalse(plan_run(self.root)["ready"])

    def test_draft_and_unsafe_configurations_fail_before_dispatch(self):
        mutations = [
            lambda: self.config.update(authority_ref=""),
            lambda: self.config["tasks"]["T-001"].update(write_paths=["../escape"]),
            lambda: self.config["tasks"]["T-001"].update(write_paths=["specs/"]),
            lambda: self.config["tasks"]["T-001"]["checks"][0].update(argv="echo unsafe"),
            lambda: self.config["tasks"]["T-001"]["checks"][0].update(inputs=[]),
            lambda: self.config["limits"].update(max_workers=0),
        ]
        original = json.loads(json.dumps(self.config))
        for change in mutations:
            with self.subTest(change=change):
                self.config = json.loads(json.dumps(original))
                change()
                self.write_config()
                with self.assertRaises(WorkflowError):
                    plan_run(self.root)

    def test_no_implementation_authority_in_planning_phase(self):
        path = self.work / "work.json"
        data = json.loads(path.read_text())
        data["phase"] = "tasks"
        path.write_text(json.dumps(data))
        self.commit()
        with self.assertRaisesRegex(WorkflowError, "implementation/verification"):
            execute_run(self.root, execute=True, backend=self.backend)

    def test_scope_violation_never_integrates_or_marks_completion(self):
        def bad(request):
            result = self.backend(request)
            (Path(request["workspace"]) / "README.md").write_text("Unauthorized change")
            return result
        result = execute_run(self.root, task_id="T-001", execute=True, backend=bad)
        self.assertEqual(result["status"], "failed")
        self.assertIn("outside declared scope", result["failure"])
        self.assertEqual((self.root / "README.md").read_text(), "Preserve this application.\n")
        self.assertFalse(inspect_work(Path(result["candidate_path"]))["tasks"][0]["checked"])

    def test_malformed_or_blocked_worker_never_passes(self):
        for identifier, result in (("invalid-worker", {"task_id": "T-001", "status": "ready"}),
                                   ("blocked-worker", {"task_id": "T-001", "status": "blocked", "summary": "Missing input", "acceptance": "not-established"})):
            with self.subTest(identifier=identifier):
                run = execute_run(self.root, task_id="T-001", execute=True, backend=lambda _: result, run_id=identifier)
                self.assertEqual(run["status"], "failed")
                self.assertEqual(run["completed_tasks"], [])
                with self.assertRaises(WorkflowError):
                    apply_run(self.root, identifier)

    def test_failed_check_cannot_complete_task_or_change_original(self):
        self.config["tasks"]["T-001"]["checks"][0]["argv"] = [sys.executable, "-c", "raise SystemExit(7)"]
        self.write_config()
        self.commit()
        result = execute_run(self.root, task_id="T-001", execute=True, backend=self.backend)
        self.assertEqual(result["status"], "failed")
        self.assertIn("Verification failed", result["failure"])
        self.assertNotIn("ready", result)
        candidate = Path(result["candidate_path"])
        self.assertFalse(inspect_work(candidate)["tasks"][0]["checked"])
        self.assertFalse(inspect_work(candidate)["evidence"])
        self.assertEqual((self.root / "src/a.txt").read_text(), "0")

    def test_integration_failure_blocks_even_after_task_check_passes(self):
        self.config["integration_checks"][0]["argv"] = [sys.executable, "-c", "raise SystemExit(8)"]
        self.write_config()
        self.commit()
        result = execute_run(self.root, task_id="T-001", execute=True, backend=self.backend)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["completed_tasks"], [])
        self.assertFalse(inspect_work(Path(result["candidate_path"]))["evidence"])

    def test_check_cannot_modify_undeclared_source_during_verification(self):
        self.config["tasks"]["T-001"]["checks"][0]["argv"] = [sys.executable, "-c", "from pathlib import Path; Path('src/b.txt').write_text('hidden')"]
        self.write_config()
        self.commit()
        result = execute_run(self.root, task_id="T-001", execute=True, backend=self.backend)
        self.assertEqual(result["status"], "failed")
        self.assertIn("changed source", result["failure"])

    def test_check_timeout_is_bounded_and_does_not_pass(self):
        self.config["limits"]["check_timeout_seconds"] = 1
        self.config["tasks"]["T-001"]["checks"][0]["argv"] = [sys.executable, "-c", "import time; time.sleep(10)"]
        self.write_config()
        self.commit()
        result = execute_run(self.root, task_id="T-001", execute=True, backend=self.backend)
        self.assertEqual(result["status"], "failed")
        self.assertIn("timeout", result["failure"])
        self.assertLess(result["elapsed_seconds"], 5)

    @unittest.skipUnless(os.name == "posix", "Process-group behavior is POSIX-specific")
    def test_exited_leader_does_not_leave_descendant_running_or_report_pass(self):
        marker = self.root / ".workflow-state/late-child.txt"
        marker.parent.mkdir()
        child = "import time; from pathlib import Path; time.sleep(0.3); Path(" + repr(str(marker)) + ").write_text('late write')"
        parent = "import subprocess,sys; subprocess.Popen([sys.executable, '-c', " + repr(child) + "])"
        result = _process([sys.executable, "-c", parent], self.root, 1, marker.parent / "process.log")
        self.assertEqual(result["returncode"], 0)
        self.assertEqual(result["termination"], "descendants-active")
        time.sleep(0.4)
        self.assertFalse(marker.exists())

    def test_later_edits_refresh_prior_completed_task_evidence(self):
        self.config["tasks"]["T-003"]["write_paths"] = ["src/a.txt", "src/c.txt"]
        self.write_config()
        self.commit()

        def later(request):
            result = self.backend(request)
            if request["task_id"] == "T-003":
                (Path(request["workspace"]) / "src/a.txt").write_text("A preserved and extended")
            return result

        result = execute_run(self.root, execute=True, backend=later)
        self.assertEqual(result["status"], "ready", result.get("failure"))
        candidate = Path(result["candidate_path"])
        state = json.loads((candidate / f"specs/{self.work_id}/work.json").read_text())
        self.assertEqual(len([item for item in state["evidence"] if item["check"] == "CHK-001"]), 2)
        self.assertTrue(all(task["completion_valid"] for task in inspect_work(candidate)["tasks"]))

    def test_apply_refuses_changed_original_and_changed_candidate(self):
        result = execute_run(self.root, task_id="T-001", execute=True, backend=self.backend)
        candidate = Path(result["candidate_path"])
        (self.root / "src/a.txt").write_text("User change")
        with self.assertRaisesRegex(WorkflowError, "clean committed"):
            apply_run(self.root, result["run_id"])
        self.assertEqual((self.root / "src/a.txt").read_text(), "User change")
        git(self.root, "restore", "src/a.txt")
        (candidate / "src/a.txt").write_text("Unverified candidate change")
        with self.assertRaisesRegex(WorkflowError, "changed after verification"):
            apply_run(self.root, result["run_id"])

    def test_run_id_never_resets_attempts(self):
        result = execute_run(self.root, task_id="T-001", execute=True, backend=lambda _: {}, run_id="failed-once")
        self.assertEqual(result["attempts_started"], 1)
        with self.assertRaisesRegex(WorkflowError, "already exists"):
            execute_run(self.root, task_id="T-001", execute=True, backend=self.backend, run_id="failed-once")
        self.assertEqual(inspect_run(self.root, "failed-once")["attempts_started"], 1)

    def test_apply_preserves_ignored_user_file_at_rename_destination(self):
        with (self.root / ".gitignore").open("a") as stream:
            stream.write("src/renamed.txt\n")
        self.config["tasks"]["T-001"]["write_paths"] = ["src/a.txt", "src/renamed.txt"]
        check = self.config["tasks"]["T-001"]["checks"][0]
        check.update(argv=[sys.executable, "-c", "from pathlib import Path; assert Path('src/renamed.txt').read_text() == '0'"], inputs=["src/renamed.txt"])
        self.write_config()
        self.commit()
        (self.root / "src/renamed.txt").write_text("User-owned ignored content")

        def rename(request):
            git(Path(request["workspace"]), "mv", "src/a.txt", "src/renamed.txt")
            return {"task_id": "T-001", "status": "ready", "summary": "Fixture renamed the scoped file.", "acceptance": "satisfied"}

        result = execute_run(self.root, task_id="T-001", execute=True, backend=rename)
        self.assertEqual(result["status"], "ready", result.get("failure"))
        with self.assertRaisesRegex(WorkflowError, "ignored application file"):
            apply_run(self.root, result["run_id"])
        self.assertEqual((self.root / "src/renamed.txt").read_text(), "User-owned ignored content")
        self.assertTrue((self.root / "src/a.txt").is_file())

    def test_commit_hook_cannot_silently_change_verified_candidate(self):
        hook = self.root / ".git/hooks/pre-commit"
        hook.write_text("#!/bin/sh\nprintf changed-by-hook > src/a.txt\ngit add src/a.txt\n")
        hook.chmod(0o755)
        result = execute_run(self.root, task_id="T-001", execute=True, backend=self.backend)
        self.assertEqual(result["status"], "failed")
        self.assertIn("commit hook changed", result["failure"])
        self.assertEqual((self.root / "src/a.txt").read_text(), "0")

    def test_worker_symlink_is_rejected_before_integration(self):
        def symlink(request):
            target = Path(request["workspace"]) / "src/a.txt"
            target.unlink()
            target.symlink_to("../README.md")
            return {"task_id": "T-001", "status": "ready", "summary": "Fixture symlink attempt", "acceptance": "satisfied"}
        result = execute_run(self.root, task_id="T-001", execute=True, backend=symlink)
        self.assertEqual(result["status"], "failed")
        self.assertIn("symlink", result["failure"])
        self.assertFalse((self.root / "src/a.txt").is_symlink())

    def test_post_merge_hook_changes_are_preserved_and_need_review(self):
        result = execute_run(self.root, task_id="T-001", execute=True, backend=self.backend)
        self.assertEqual(result["status"], "ready", result.get("failure"))
        hook = self.root / ".git/hooks/post-merge"
        hook.write_text("#!/bin/sh\nprintf changed-after-merge > README.md\n")
        hook.chmod(0o755)
        invoked = subprocess.run([sys.executable, str(ROOT / "scripts/workflow.py"), "--root", str(self.root), "run-apply", result["run_id"], "--json"], text=True, capture_output=True)
        self.assertEqual(invoked.returncode, 1, invoked.stdout + invoked.stderr)
        applied = json.loads(invoked.stdout)
        self.assertEqual(applied["status"], "applied-needs-review")
        self.assertFalse(applied["application"]["worktree_clean"])
        self.assertEqual(applied["application"]["observed_head"], result["candidate_commit"])
        self.assertEqual((self.root / "README.md").read_text(), "changed-after-merge")
        self.assertTrue(any(event["event"] == "apply-intent" for event in applied["events"]))
        with self.assertRaisesRegex(WorkflowError, "cannot be abandoned"):
            abandon_run(self.root, result["run_id"], "Do not silently undo hook effects.")

    def test_total_deadline_includes_final_git_commit_hook(self):
        self.config["limits"].update(timeout_seconds=1, check_timeout_seconds=1)
        self.write_config()
        self.commit()
        hook = self.root / ".git/hooks/pre-commit"
        hook.write_text("#!/bin/sh\nsleep 5\n")
        hook.chmod(0o755)
        started = time.monotonic()
        result = execute_run(self.root, task_id="T-001", execute=True, backend=self.backend)
        self.assertNotEqual(result["status"], "ready")
        self.assertIn(result["status"], ("failed", "unknown"))
        self.assertTrue("timeout" in result["failure"] or "deadline" in result["failure"] or "budget" in result["failure"], result)
        self.assertLess(time.monotonic() - started, 2.5)
        self.assertEqual((self.root / "src/a.txt").read_text(), "0")
        with self.assertRaises(WorkflowError):
            apply_run(self.root, result["run_id"])

    def test_dead_owner_is_unknown_and_explicit_abandonment_preserves_counters(self):
        result = execute_run(self.root, task_id="T-001", execute=True, backend=lambda _: {}, run_id="interrupted")
        path = self.root / ".workflow-state/runs/interrupted/run.json"
        record = json.loads(path.read_text())
        record.update(status="running", owner={"pid": 999999999})
        path.write_text(json.dumps(record))
        lock = self.root / ".workflow-state/execution.lock"
        lock.write_text(json.dumps({"run_id": "interrupted", "owner": {"pid": 999999999}}))
        self.assertEqual(inspect_run(self.root, "interrupted")["effective_status"], "unknown")
        abandoned = abandon_run(self.root, "interrupted", "Fixture inspected retained worktree and no live operation remains.")
        self.assertEqual(abandoned["status"], "abandoned")
        self.assertEqual(abandoned["attempts_started"], result["attempts_started"])
        self.assertFalse(lock.exists())

    @unittest.skipUnless(os.name == "posix", "Native adapter currently requires POSIX")
    def test_native_adapter_uses_structured_supported_flags_without_bypass(self):
        directory = self.root / ".workflow-state/native-fixture"
        directory.mkdir(parents=True)
        observed = []

        def fake_process(argv, cwd, timeout, output, prompt=None):
            observed.append(argv)
            destination = Path(argv[argv.index("--output-last-message") + 1])
            destination.write_text(json.dumps({"task_id": "T-001", "status": "blocked", "summary": "Fixture only", "acceptance": "not-established"}))
            return {"returncode": 0, "termination": None}

        with patch("workflow_engine.runner._process", fake_process):
            result = CodexBackend()({"attempt_directory": str(directory), "workspace": str(self.root), "timeout_seconds": 3, "prompt": "Fixture prompt"})
        argv = observed[0]
        self.assertEqual(argv[:3], ["codex", "exec", "--json"])
        self.assertEqual(argv[argv.index("--sandbox") + 1], "workspace-write")
        self.assertFalse(any("bypass" in item or item == "--trust" for item in argv))
        self.assertEqual(result["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
