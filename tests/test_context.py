"""Context selection, strict budgets, advisory actions and audit preservation."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from workflow_engine import build_context_packet, context_fingerprint, inspect_work, prompt_pulse, render_context_packet
from workflow_engine.engine import new_work


def report_fixture():
    return {
        "schema_version": 1, "id": "0100-context", "title": "Preserve known context",
        "mode": "brownfield", "route": "quick", "phase": "implementation",
        "artifacts": {"requirements": "specs/0100-context/requirements.md", "design": "specs/0100-context/design.md", "tasks": "specs/0100-context/tasks.md"},
        "context_files": ["project/brief.md", "delivery/current-handoff.md"],
        "known_facts": [{"id": "F-001", "kind": "supplied", "statement": "Preserve the existing database.", "source": "project/brief.md"}],
        "answered_questions": [{"id": "Q-001", "status": "answered", "answer": "Keep the public API stable.", "source": "project/brief.md"}],
        "open_questions": [{"id": "Q-002", "status": "open", "prompt": "Which authorized environment will be used for the later operational check?", "why": "The verification target remains undecided.", "recommendation": "Reuse the existing test environment if authorized.", "blocks": ["verification"]}],
        "next_questions": [],
        "reviews": {"requirements": {"status": "missing"}, "design": {"status": "missing"}, "tasks": {"status": "accepted", "decision_ref": "evidence/review.md"}},
        "tasks": [
            {"id": "T-000", "title": "Characterize the current interface", "checked": True, "completion_valid": True, "dependencies": [], "requirements": ["REQ-001"], "design": ["DES-001"], "checks": ["CHK-000"]},
            {"id": "T-001", "title": "Implement the bounded change", "checked": False, "completion_valid": False, "dependencies": ["T-000"], "requirements": ["REQ-001"], "design": ["DES-001"], "checks": ["CHK-001"]},
            {"id": "T-002", "title": "Verify the integrated behavior", "checked": False, "completion_valid": False, "dependencies": ["T-001"], "requirements": ["REQ-001"], "design": ["DES-001"], "checks": ["CHK-002"]},
        ],
        "checks": [], "evidence": {}, "dependency_ready_tasks": ["T-001"], "eligible_tasks": ["T-001"],
        "issues": [], "consultant_instructions": ["Read the canonical records before acting."],
    }


class CompactContextTests(unittest.TestCase):
    def test_long_title_and_history_cannot_hide_current_error(self):
        report = report_fixture()
        report["title"] = "An oversized title " * 20000
        report["known_facts"] *= 500
        report["issues"] = [{"severity": "warning", "code": "older-warning", "message": "A small warning"},
                            {"severity": "error", "code": "false-completion", "message": "The checked task has stale evidence."}]
        packet = build_context_packet(report)
        text = render_context_packet(packet)
        self.assertLessEqual(len(text), 6000)
        self.assertEqual(json.loads(text), packet)
        self.assertEqual(packet["attention"][0]["code"], "false-completion")
        self.assertEqual(packet["next_action"]["kind"], "resolve-errors")
        self.assertGreater(packet["omitted"]["facts"], 0)
        self.assertIn("specs/0100-context/tasks.md", text)
        self.assertLess(text.index("false-completion"), text.index('"title"'))

    def test_large_completed_history_is_counted_without_repeating_tasks(self):
        report = report_fixture()
        report["phase"] = "complete"
        report["eligible_tasks"] = []
        report["tasks"] = [{"id": f"T-{number:03}", "title": "A completed task", "checked": True, "completion_valid": True}
                           for number in range(1, 501)]
        report["known_facts"] = [{"id": f"F-{number:03}", "kind": "supplied", "statement": "Known " + "x" * 500, "source": "project/brief.md"}
                                 for number in range(1, 61)]
        report["answered_questions"] = [{"id": f"Q-{number:03}", "answer": "Answered " + "y" * 500, "source": "project/brief.md"}
                                        for number in range(1, 61)]
        packet = build_context_packet(report)
        self.assertLessEqual(len(render_context_packet(packet)), 6000)
        self.assertEqual(packet["counts"]["complete"], 500)
        self.assertEqual(packet["tasks"], [])
        self.assertEqual(packet["omitted"]["tasks"], 500)
        self.assertEqual(packet["next_action"]["kind"], "complete")
        self.assertIn("full details", packet["audit"])

    def test_selected_tasks_keep_dependencies_contract_checks_and_sources(self):
        packet = build_context_packet(report_fixture())
        self.assertEqual([task["id"] for task in packet["tasks"]], ["T-001"])
        task = packet["tasks"][0]
        self.assertEqual(task["dependencies"], ["T-000"])
        self.assertEqual(task["requirements"], ["REQ-001"])
        self.assertEqual(task["design"], ["DES-001"])
        self.assertEqual(task["checks"], ["CHK-001"])
        self.assertIn({"kind": "tasks", "path": "specs/0100-context/tasks.md"}, packet["sources"])
        self.assertEqual(packet["counts"]["complete"], 1)
        self.assertEqual(packet["next_action"]["kind"], "eligible-tasks")

    def test_at_most_three_eligible_tasks_are_selected(self):
        report = report_fixture()
        report["tasks"] = [{"id": f"T-{number:03}", "title": "Ready", "checked": False, "completion_valid": False,
                            "dependencies": [], "requirements": ["REQ-001"], "design": ["DES-001"], "checks": ["CHK-001"]}
                           for number in range(1, 30)]
        report["eligible_tasks"] = [task["id"] for task in report["tasks"]]
        packet = build_context_packet(report)
        self.assertEqual([task["id"] for task in packet["tasks"]], ["T-001", "T-002", "T-003"])
        self.assertEqual(packet["omitted"]["tasks"], 26)

    def test_future_question_does_not_displace_current_eligible_work(self):
        report = report_fixture()
        packet = build_context_packet(report)
        self.assertEqual(packet["blocking_questions"], [])
        self.assertEqual(packet["next_action"]["kind"], "eligible-tasks")
        report["open_questions"][0]["blocks"] = ["implementation"]
        packet = build_context_packet(report)
        self.assertEqual(packet["next_action"]["kind"], "resolve-questions")
        self.assertEqual(packet["blocking_questions"][0]["id"], "Q-002")

    def test_combined_task_review_respects_upstream_question_blockers(self):
        report = report_fixture()
        report["phase"] = "tasks"
        for boundary in ("requirements", "design", "tasks"):
            report["open_questions"][0]["blocks"] = [boundary]
            self.assertEqual(build_context_packet(report)["next_action"]["kind"], "resolve-questions")

    def test_quick_review_does_not_invent_separate_missing_gates(self):
        packet = build_context_packet(report_fixture())
        self.assertEqual(packet["reviews"], [{"artifact": "tasks", "status": "accepted", "decision_ref": "evidence/review.md"}])
        self.assertNotIn("missing", render_context_packet(packet))

    def test_design_first_review_order_and_conflicting_facts(self):
        report = report_fixture()
        report.update(route="design-first", phase="design", eligible_tasks=[])
        report["reviews"]["design"] = {"status": "accepted", "decision_ref": "evidence/design-review.md"}
        packet = build_context_packet(report)
        self.assertEqual([review["artifact"] for review in packet["reviews"]], ["design"])
        self.assertEqual(packet["next_action"]["to"], "requirements")
        report["known_facts"][0]["kind"] = "conflicting"
        self.assertEqual(build_context_packet(report)["next_action"]["kind"], "resolve-conflicts")

    def test_plan_completion_never_implies_implementation(self):
        report = report_fixture()
        report.update(route="plan", phase="planned", eligible_tasks=[])
        packet = build_context_packet(report)
        self.assertEqual(packet["next_action"]["kind"], "planning-complete")
        self.assertIn("not executed or newly authorized", packet["next_action"]["reason"])
        self.assertEqual(packet["tasks"], [])

    def test_oversized_source_reference_is_omitted_whole(self):
        report = report_fixture()
        reference = "context/" + "long/" * 3000 + "brief.md"
        report["context_files"] = [reference]
        packet = build_context_packet(report)
        self.assertNotIn(reference, render_context_packet(packet))
        self.assertEqual(packet["omitted"]["sources"], 1)
        self.assertTrue(all(source["path"] in report["artifacts"].values() for source in packet["sources"]))

    def test_fingerprint_covers_omitted_records_and_is_order_stable_for_objects(self):
        report = report_fixture()
        report["known_facts"] = [{"id": f"F-{number:03}", "kind": "supplied", "statement": "Established", "source": "project/brief.md"}
                                 for number in range(1, 101)]
        first = build_context_packet(report)
        self.assertEqual(first["fingerprint"], context_fingerprint(dict(reversed(list(report.items())))))
        changed = copy.deepcopy(report)
        changed["known_facts"][-1]["statement"] = "The last omitted statement changed."
        second = build_context_packet(changed)
        self.assertEqual(first["facts"], second["facts"])
        self.assertNotEqual(first["fingerprint"], second["fingerprint"])

    def test_projection_and_pulse_leave_input_unchanged(self):
        report = report_fixture()
        before = copy.deepcopy(report)
        build_context_packet(report)
        prompt_pulse(report)
        self.assertEqual(report, before)

    def test_pulse_is_strictly_bounded_fresh_and_preserves_steering(self):
        report = report_fixture()
        report["title"] = "x" * 100000
        report["issues"] = [{"severity": "error", "code": "false-completion", "message": "x" * 10000} for _ in range(100)]
        output = prompt_pulse(report)
        pulse = json.loads(output)
        self.assertLessEqual(len(output), 1200)
        self.assertEqual(pulse["fingerprint"], context_fingerprint(report))
        self.assertEqual(pulse["attention"][0]["code"], "false-completion")
        self.assertGreater(pulse["omitted_issues"], 0)
        self.assertIn("Otherwise reuse", pulse["refresh"])
        self.assertIn("latest user steering", pulse["refresh"])
        self.assertIn("context --compact", pulse["refresh"])
        self.assertNotIn("facts", pulse)
        self.assertNotIn("answers", pulse)

    def test_smaller_supported_budgets_count_all_serialized_characters(self):
        report = report_fixture()
        report["title"] = "\u732b" * 5000
        report["issues"] = [{"severity": "error", "code": "false-completion", "message": "\u732b" * 1000}]
        packet = build_context_packet(report, 2000)
        pulse = json.loads(prompt_pulse(report, 800))
        self.assertLessEqual(len(render_context_packet(packet)), 2000)
        self.assertLessEqual(len(render_context_packet(pulse)), 800)
        self.assertEqual(packet["attention"][0]["code"], "false-completion")
        self.assertEqual(pulse["attention"][0]["code"], "false-completion")
        self.assertTrue(packet["attention"][0]["details_omitted"])
        self.assertTrue(pulse["attention"][0]["details_omitted"])
        for invalid in (1999, 6001, True):
            with self.assertRaises(ValueError):
                build_context_packet(report, invalid)

    def test_compact_cli_is_read_only_and_preserves_full_audit_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            new_work(root, "0100-example", "A rough idea", idea="Keep the established product intent.", activate=True)
            before = {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            full = inspect_work(root)
            for tail in (["context", "--compact"], ["context", "--compact", "--json"], ["context", "--json"], ["status", "--json"]):
                run = subprocess.run([sys.executable, str(ROOT / "scripts/workflow.py"), "--root", str(root), *tail], capture_output=True, text=True)
                self.assertEqual(run.returncode, 0, run.stderr)
                result = json.loads(run.stdout)
                if "--compact" in tail:
                    self.assertLessEqual(len(run.stdout.rstrip("\n")), 6000)
                    self.assertEqual(result["fingerprint"], context_fingerprint(full))
                    self.assertEqual(result["next_action"]["kind"], "consult")
                else:
                    self.assertEqual(result, full)
            after = {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
