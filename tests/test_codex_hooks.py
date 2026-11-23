"""Event and scope tests; these do not claim native-client hook activation."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("workflow_hooks", ROOT / "scripts" / "codex_hooks.py")
HOOKS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HOOKS)


class HookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def event(self, event="SessionStart", **extra):
        return {"hook_event_name": event, "cwd": str(self.root), **extra}

    def activate(self):
        (self.root / ".codex").mkdir()
        (self.root / ".codex" / "workflow.json").write_text("{}")

    def test_no_active_work_preserves_interview_and_writes_nothing(self):
        out = HOOKS.handle_event(self.event(), self.root)
        self.assertIn("No active work", out["hookSpecificOutput"]["additionalContext"])
        self.assertEqual(list(self.root.iterdir()), [])
        self.assertEqual(HOOKS.handle_event(self.event("Stop"), self.root), {})

    def test_context_carries_existing_answers_and_bounded_questions(self):
        self.activate()
        report = {"id": "work", "title": "Feature", "phase": "consultation", "known_facts": [{"id": "F-001", "source": "brief.md"}], "answered_questions": [{"id": "Q-001", "answer": "Use the established rule", "source": "brief.md"}], "next_questions": [{"id": "Q-002"}], "issues": []}
        outputs = {}
        for event in ("SessionStart", "UserPromptSubmit"):
            out = HOOKS.handle_event(self.event(event), self.root, lambda root: report)
            self.assertEqual(out["hookSpecificOutput"]["hookEventName"], event)
            context = out["hookSpecificOutput"]["additionalContext"]
            outputs[event] = json.loads(context)
            self.assertLessEqual(len(context), HOOKS.MAX_CONTEXT_CHARS if event == "SessionStart" else HOOKS.MAX_PULSE_CHARS)
            self.assertNotIn("decision", out)
        self.assertEqual(outputs["SessionStart"]["answers"][0]["id"], "Q-001")
        self.assertEqual(outputs["SessionStart"]["questions"][0]["id"], "Q-002")
        self.assertEqual(outputs["SessionStart"]["fingerprint"], outputs["UserPromptSubmit"]["fingerprint"])
        self.assertNotIn("answers", outputs["UserPromptSubmit"])
        self.assertIn("Otherwise reuse", outputs["UserPromptSubmit"]["refresh"])

    def test_stop_warns_but_never_restarts_an_interview(self):
        self.activate()
        report = {"issues": [{"severity": "error", "code": "false-completion", "message": "No current evidence"}]}
        for already_continued in (False, True):
            out = HOOKS.handle_event(self.event("Stop", stop_hook_active=already_continued), self.root, lambda root: report)
            self.assertIn("false-completion", out["systemMessage"])
            self.assertNotIn("decision", out)
            self.assertNotIn("continue", out)
        report["issues"][0]["severity"] = "warning"
        self.assertEqual(HOOKS.handle_event(self.event("Stop"), self.root, lambda root: report), {})

    def test_wrong_workspace_does_not_read_metadata(self):
        def forbidden(root):
            self.fail("inspector must not run outside root")
        out = HOOKS.handle_event({"hook_event_name": "SessionStart", "cwd": str(self.root.parent)}, self.root, forbidden)
        self.assertIn("outside", out["systemMessage"])
        out = HOOKS.handle_event({"hook_event_name": "Stop", "cwd": "relative"}, self.root, forbidden)
        self.assertIn("absolute", out["systemMessage"])

    def test_bad_metadata_is_visible_without_false_success(self):
        self.activate()
        def broken(root):
            raise ValueError("bad active record")
        out = HOOKS.handle_event(self.event(), self.root, broken)
        self.assertIn("could not be inspected", out["systemMessage"])
        self.assertNotIn("hookSpecificOutput", out)

    def test_context_output_is_bounded(self):
        out = HOOKS.context_text({"title": "x" * 100000, "known_facts": [{"statement": "x" * 100000}], "answered_questions": [{"answer": "y" * 100000}], "issues": [{"severity": "error", "code": "false-completion", "message": "Evidence is stale"}]})
        self.assertLessEqual(len(out), HOOKS.MAX_CONTEXT_CHARS)
        self.assertEqual(json.loads(out)["attention"][0]["code"], "false-completion")

    def test_prompt_refresh_changes_identity_without_creating_cache(self):
        self.activate()
        before = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        report = {"id": "work", "title": "Feature", "phase": "consultation", "issues": []}
        first = HOOKS.handle_event(self.event("UserPromptSubmit"), self.root, lambda root: report)
        report["issues"] = [{"severity": "error", "code": "stale-review", "message": "Review no longer matches"}]
        second = HOOKS.handle_event(self.event("UserPromptSubmit"), self.root, lambda root: report)
        a = json.loads(first["hookSpecificOutput"]["additionalContext"])
        b = json.loads(second["hookSpecificOutput"]["additionalContext"])
        self.assertNotEqual(a["fingerprint"], b["fingerprint"])
        self.assertEqual(b["attention"][0]["code"], "stale-review")
        after = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(after, before)

    def test_bad_and_large_inputs_return_valid_json(self):
        for payload in ("not json", "[]", "x" * (HOOKS.MAX_INPUT_BYTES + 1), "[" * 2000 + "]" * 2000):
            result = subprocess.run([sys.executable, str(ROOT / "scripts" / "codex_hooks.py")], input=payload, capture_output=True, text=True, check=True)
            self.assertIn("invalid input", json.loads(result.stdout)["systemMessage"])

    def test_wrong_event_types_are_ignored_with_valid_json(self):
        for event in ([], {}, 1, None):
            result = subprocess.run([sys.executable, str(ROOT / "scripts" / "codex_hooks.py")], input=json.dumps(self.event(event)), capture_output=True, text=True, check=True)
            self.assertEqual(json.loads(result.stdout), {})

    def test_adopted_layer_selects_application_root(self):
        self.assertEqual(HOOKS.project_root(self.root / ".aws-workflow"), self.root)
        self.assertEqual(HOOKS.project_root(self.root), self.root)


if __name__ == "__main__":
    unittest.main()
