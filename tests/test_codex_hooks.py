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
        report = {"id": "work", "title": "Feature", "phase": "consultation", "known_facts": [{"id": "F-1", "source": "brief.md"}], "answered_questions": [{"id": "Q-1", "answer_source": "brief.md"}], "next_questions": [{"id": "Q-2"}], "issues": []}
        for event in ("SessionStart", "UserPromptSubmit"):
            out = HOOKS.handle_event(self.event(event), self.root, lambda root: report)
            self.assertEqual(out["hookSpecificOutput"]["hookEventName"], event)
            context = out["hookSpecificOutput"]["additionalContext"]
            self.assertIn("answered_questions", context)
            self.assertIn("Q-2", context)
            self.assertNotIn("decision", out)

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
        out = HOOKS.context_text({"known_facts": ["x" * 100000], "answered_questions": ["y" * 100000]})
        self.assertLessEqual(len(out), HOOKS.MAX_CONTEXT_CHARS + 50)

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
