"""Behavioral fixtures for the offline workflow, including refusal paths."""

import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from workflow_engine import WorkflowError, inspect_work
from workflow_engine.engine import advance, atomic_json, new_work, record_evidence, record_review


CONTRACT = """# Requirements: fixture

| ID | Condition and required outcome | Acceptance criterion | Required or deferred |
| --- | --- | --- | --- |
| REQ-001 | When a user submits a valid record, the service stores one record. | A repeat request yields the same record. | Required |
| REQ-002 | When another user requests the record, access is denied. | The unauthorized caller receives no record. | Required |
"""

DESIGN = """# Design: fixture

## DES-001 — Storage and authorization

Preserve the established interface. Check identity before looking up a record.
Use the existing atomic repository operation and return its canonical identifier.
"""

TASKS = """# Tasks: fixture

## Implementation tasks

### T-001 — Store the record once

- [ ] T-001 complete
- Activity: ready
- Contract / design: REQ-001 / DES-001
- Prerequisites: none
- Scope and exclusions: Change the record operation only.
- Acceptance: Repeating a request produces exactly one record.
- Verification: CHK-001
- Evidence / review: none
- Blocker: none

### T-002 — Preserve authorization

- [ ] T-002 complete
- Activity: ready
- Contract / design: REQ-002 / DES-001
- Prerequisites: T-001
- Scope and exclusions: Keep the established caller identity model.
- Acceptance: Another caller cannot read the stored record.
- Verification: CHK-002
- Evidence / review: none
- Blocker: none

## Verification matrix

| Check | Requirement | Task | Method and expected result | Evidence |
| --- | --- | --- | --- | --- |
| CHK-001 | REQ-001 | T-001 | Repeat a request; assert one stored record. | Not run |
| CHK-002 | REQ-002 | T-002 | Read as another caller; assert denial. | Not run |
"""

BUGFIX = """# Bugfix analysis

## DEF-001 — Reported duplicate record

A repeated request currently creates two records in the supplied reproduction.

## FIX-001 — Correct retry

When the same valid request repeats, return the first record without another write.

## Preservation contract

| ID | Preserved behavior | Acceptance |
| --- | --- | --- |
| KEEP-001 | Another caller cannot read the record. | Existing authorization check passes. |
"""


class WorkflowFixtures(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.work_id = "0100-record-service"
        new_work(self.root, self.work_id, "Record service", idea="Keep booking retries safe.", activate=True)
        self.work = self.root / "specs" / self.work_id

    def metadata(self, **changes):
        path = self.work / "work.json"
        data = json.loads(path.read_text())
        data.update(changes)
        path.write_text(json.dumps(data))
        return data

    def artifacts(self, route="requirements-first"):
        self.metadata(route=route)
        (self.work / "requirements.md").write_text(CONTRACT)
        (self.work / "design.md").write_text(DESIGN)
        (self.work / "tasks.md").write_text(TASKS)
        (self.root / "service.py").write_text("def lookup(key):\n    return key\n")

    def review(self, artifact):
        return record_review(self.root, self.work_id, artifact, "accepted",
                             "Fixture-only decision: authorized test owner delegates the described review.",
                             "Fixture reviewer", "delegated")

    def implementation(self, route="requirements-first"):
        self.artifacts(route)
        if route == "quick":
            advance(self.root, self.work_id, "tasks")
        else:
            order = ("design", "requirements") if route == "design-first" else ("requirements", "design")
            advance(self.root, self.work_id, order[0])
            self.review(order[0])
            advance(self.root, self.work_id, order[1])
            self.review(order[1])
            advance(self.root, self.work_id, "tasks")
        self.review("tasks")
        return advance(self.root, self.work_id, "implementation")

    def evidence(self, check="CHK-001", result="pass"):
        receipt = f"evidence/{check.lower()}-{result}.md"
        path = self.root / receipt
        path.parent.mkdir(exist_ok=True)
        path.write_text(f"Fixture receipt; simulated outcome {result}; no external service was used.\n")
        return record_evidence(self.root, self.work_id, check, receipt, result,
                               "Fixture simulation of the named check", "temporary local fixture", "fixture source plus current patch",
                               "2026-11-22T00:00:00+00:00", ["service.py"])

    def complete_task(self, task_id):
        path = self.work / "tasks.md"
        text = path.read_text().replace(f"- [ ] {task_id} complete", f"- [x] {task_id} complete")
        start = text.index(f"### {task_id}")
        split = text.find("\n### T-", start + 1)
        end = split if split != -1 else len(text)
        text = text[:start] + text[start:end].replace("- Activity: ready", "- Activity: complete") + text[end:]
        path.write_text(text)

    def errors(self, report=None):
        return [item for item in (report or inspect_work(self.root))["issues"] if item["severity"] == "error"]

    def codes(self, report=None):
        return {item["code"] for item in (report or inspect_work(self.root))["issues"]}

    def test_rough_idea_is_valid_before_requirements_or_interview(self):
        report = inspect_work(self.root)
        self.assertEqual(report["phase"], "consultation")
        self.assertEqual(report["known_facts"][0]["statement"], "Keep booking retries safe.")
        self.assertEqual(report["next_questions"], [])
        self.assertFalse((self.work / "design.md").exists())
        self.assertFalse(self.errors(report))

    def test_new_work_carries_adopted_manifest_context_into_resume(self):
        mappings = {"brief": "business/project.md", "handoff": ".aws-workflow/delivery/current-handoff.md",
                    "adoption_report": ".aws-workflow/project/adoption-report.md",
                    "environment_capabilities": ".aws-workflow/delivery/environment-capabilities.md"}
        for relative in mappings.values():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# Preserved application context\n\nRead the actual source before deciding.\n")
        manifest = self.root / ".aws-workflow/manifest.json"
        manifest.write_text(json.dumps({"schema_version": 1, "identity": "codex-aws-workflow", "paths": mappings}))
        report = new_work(self.root, "0200-adopted", "Adopted work", mode="brownfield", activate=True)
        self.assertEqual(report["context_files"], [".aws-workflow/manifest.json", *mappings.values()])
        self.assertEqual(inspect_work(self.root)["context_files"], report["context_files"])
        self.assertEqual(report["known_facts"], [])
        self.assertFalse(self.errors(report))

    def test_foundation_enabled_feature_and_defect_link_selected_brownfield_records(self):
        mappings = {
            "brief": "docs/product overview.md", "requirements": "standards/system rules.md",
            "tech": "standards/stack.md", "structure": "standards/layout.md",
            "architecture": "standards/production.md", "handoff": "delivery/current.md",
            "adoption_report": "intake.md", "environment_capabilities": "tools.md",
        }
        for relative in mappings.values():
            path = self.root / relative
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_text("Existing application-owned decisions.\n")
        manifest = self.root / ".aws-workflow/manifest.json"
        manifest.parent.mkdir()
        manifest.write_text(json.dumps({"schema_version": 2, "identity": "codex-aws-workflow", "paths": mappings}))
        for route, contract in (("requirements-first", "requirements.md"), ("bugfix", "bugfix.md")):
            with self.subTest(route=route):
                report = new_work(self.root, route, route, mode="brownfield", route=route)
                self.assertEqual(list(report["foundation_sources"]), [mappings["requirements"]])
                self.assertNotIn(mappings["architecture"], report["context_files"])
                self.assertIn(mappings["brief"], report["context_files"])
                draft = (self.root / "specs" / route / contract).read_text()
                self.assertIn("(../../docs/product%20overview.md)", draft)
                self.assertIn("(../../standards/system%20rules.md)", draft)
                self.assertNotIn("Existing application-owned decisions", draft)

    def test_new_work_uses_existing_root_context_without_an_adoption_manifest(self):
        for relative in ("project/brief.md", "delivery/current-handoff.md"):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# Existing project context\n")
        report = new_work(self.root, "0200-existing", "Existing context")
        self.assertEqual(report["context_files"], ["project/brief.md", "delivery/current-handoff.md"])

    def test_unsafe_adoption_mapping_is_rejected_before_creating_work(self):
        manifest = self.root / ".aws-workflow/manifest.json"
        manifest.parent.mkdir()
        manifest.write_text(json.dumps({"schema_version": 1, "identity": "codex-aws-workflow", "paths": {"brief": "../outside.md"}}))
        with self.assertRaises(WorkflowError):
            new_work(self.root, "0200-unsafe", "Unsafe mapping")
        self.assertFalse((self.root / "specs/0200-unsafe").exists())

    def test_supplied_requirements_and_answers_do_not_create_redundant_questions(self):
        self.artifacts()
        self.metadata(facts=[{"id": "F-001", "kind": "supplied", "statement": "Use the existing identity model.", "source": "project/brief.md#constraints"}],
                      questions=[{"id": "Q-001", "prompt": "Which identity model?", "why": "Preserve callers.", "recommendation": "", "status": "answered",
                                  "answer": "The established identity model.", "source": "specs/0100-record-service/design.md#des-001", "blocks": ["design"]}])
        report = inspect_work(self.root)
        self.assertEqual(report["next_questions"], [])
        self.assertEqual(report["answered_questions"][0]["answer"], "The established identity model.")
        self.assertFalse(self.errors(report))

    def test_conflicting_and_unknown_information_is_retained_not_filled_in(self):
        questions = [{"id": f"Q-{index:03d}", "prompt": f"Which explicit business choice {index}?", "why": "It changes the acceptance contract.",
                      "recommendation": "", "status": "open", "answer": "", "source": "", "blocks": ["requirements"]} for index in range(1, 5)]
        self.metadata(facts=[{"id": "F-001", "kind": "conflicting", "statement": "Two sources disagree about retention.", "source": "User messages 1 and 2."}], questions=questions)
        report = inspect_work(self.root)
        self.assertEqual(len(report["next_questions"]), 3)
        self.assertEqual(len(report["open_questions"]), 4)
        self.assertIn("unresolved-conflict", self.codes(report))
        self.assertTrue(all(question["answer"] == "" for question in report["open_questions"]))
        (self.work / "requirements.md").write_text(CONTRACT)
        with self.assertRaises(WorkflowError):
            self.review("requirements")

    def test_answered_question_requires_answer_and_source(self):
        self.metadata(questions=[{"id": "Q-001", "prompt": "Which region?", "why": "Residency.", "status": "answered", "answer": "", "source": "", "blocks": ["requirements"]}])
        self.assertIn("missing-answer-source", self.codes())

    def test_context_status_and_validate_do_not_write_files(self):
        before = {path.relative_to(self.root): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        for command in ("context", "status", "validate"):
            process = subprocess.run([sys.executable, str(ROOT / "scripts/workflow.py"), "--root", str(self.root), command, "--json"], capture_output=True, text=True)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(json.loads(process.stdout)["id"], self.work_id)
        after = {path.relative_to(self.root): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual(before, after)

    def test_cannot_advance_past_requirement_without_actual_review_record(self):
        self.artifacts()
        advance(self.root, self.work_id, "requirements")
        before = (self.work / "work.json").read_bytes()
        with self.assertRaises(WorkflowError):
            advance(self.root, self.work_id, "design")
        self.assertEqual(before, (self.work / "work.json").read_bytes())

    def test_prior_delegated_review_is_reused_without_extra_review(self):
        report = self.implementation()
        self.assertFalse(self.errors(report))
        self.assertEqual(report["eligible_tasks"], ["T-001"])
        data = json.loads((self.work / "work.json").read_text())
        self.assertEqual(len(data["reviews"]), 3)
        self.assertEqual(report["reviews"]["requirements"]["authority"], "delegated")
        self.assertEqual(len(data["reviews"]), len(json.loads((self.work / "work.json").read_text())["reviews"]))

    def test_quick_route_uses_one_combined_review(self):
        report = self.implementation("quick")
        self.assertFalse(self.errors(report))
        data = json.loads((self.work / "work.json").read_text())
        self.assertEqual(len(data["reviews"]), 1)
        self.assertEqual(set(data["reviews"][0]["hashes"]), {f"specs/{self.work_id}/{name}.md" for name in ("requirements", "design", "tasks")})
        self.assertEqual(report["reviews"]["requirements"]["status"], "missing")

    def test_design_first_does_not_require_an_early_requirements_review(self):
        report = self.implementation("design-first")
        self.assertFalse(self.errors(report))
        data = json.loads((self.work / "work.json").read_text())
        self.assertEqual(data["reviews"][0]["artifact"], "design")
        self.assertEqual(len(data["reviews"][0]["hashes"]), 1)
        self.assertEqual(len(data["reviews"][1]["hashes"]), 2)

    def test_design_first_changed_upstream_design_invalidates_requirements_review(self):
        self.implementation("design-first")
        with (self.work / "design.md").open("a") as stream:
            stream.write("\nThe selected write mechanism now requires an outbox transaction.\n")
        report = self.review("design")
        self.assertEqual(report["reviews"]["design"]["status"], "accepted")
        self.assertEqual(report["reviews"]["requirements"]["status"], "stale")
        self.assertEqual(report["eligible_tasks"], [])

    def test_plan_route_finishes_planning_without_claiming_implementation(self):
        self.artifacts("plan")
        for phase, next_phase in (("requirements", "design"), ("design", "tasks"), ("tasks", "planned")):
            if phase == "requirements":
                advance(self.root, self.work_id, phase)
            self.review(phase)
            report = advance(self.root, self.work_id, next_phase)
        self.assertEqual(report["phase"], "planned")
        self.assertFalse(any(task["checked"] for task in report["tasks"]))
        self.assertEqual(report["eligible_tasks"], [])
        self.assertFalse(self.errors(report))

    def test_bugfix_contract_has_defect_correction_and_preservation_ids(self):
        self.artifacts("bugfix")
        (self.work / "bugfix.md").write_text(BUGFIX)
        self.metadata(artifacts={"requirements": "bugfix.md", "design": "design.md", "tasks": "tasks.md"})
        (self.work / "tasks.md").write_text(TASKS.replace("REQ-001", "FIX-001").replace("REQ-002", "KEEP-001"))
        self.review("requirements")
        self.assertFalse(self.errors())

    def test_review_becomes_stale_on_contract_change(self):
        self.implementation()
        with (self.work / "requirements.md").open("a") as stream:
            stream.write("\nChanged the retention requirement.\n")
        report = inspect_work(self.root)
        self.assertEqual(report["reviews"]["requirements"]["status"], "stale")
        self.assertIn("stale-review", self.codes(report))
        self.assertEqual(report["eligible_tasks"], [])

    def test_checkbox_activity_and_evidence_updates_preserve_plan_review(self):
        self.implementation()
        self.evidence()
        self.complete_task("T-001")
        path = self.work / "tasks.md"
        path.write_text(path.read_text().replace("| Not run |", "| Recorded in current result ledger |", 1).replace("- Evidence / review: none", "- Evidence / review: EV-001", 1))
        report = inspect_work(self.root)
        self.assertEqual(report["reviews"]["tasks"]["status"], "accepted")
        self.assertTrue(report["evidence"]["CHK-001"]["current"])
        self.assertEqual(report["eligible_tasks"], ["T-002"])
        self.assertFalse(self.errors(report))

    def test_dependency_cannot_be_skipped_even_with_passing_result(self):
        self.implementation()
        self.evidence("CHK-002")
        self.complete_task("T-002")
        report = inspect_work(self.root)
        self.assertIn("false-completion", self.codes(report))
        self.assertFalse(report["tasks"][1]["completion_valid"])

    def test_complete_requires_all_tasks_and_current_results(self):
        self.implementation()
        advance(self.root, self.work_id, "verification")
        with self.assertRaises(WorkflowError):
            advance(self.root, self.work_id, "complete")
        self.evidence("CHK-001")
        self.complete_task("T-001")
        self.evidence("CHK-002")
        self.complete_task("T-002")
        report = advance(self.root, self.work_id, "complete")
        self.assertFalse(self.errors(report))
        self.assertTrue(all(task["completion_valid"] for task in report["tasks"]))

    def test_changed_source_invalidates_completion(self):
        self.implementation()
        self.evidence()
        self.complete_task("T-001")
        (self.root / "service.py").write_text("def lookup(key):\n    return None\n")
        report = inspect_work(self.root)
        self.assertIn("stale-evidence", self.codes(report))
        self.assertIn("false-completion", self.codes(report))

    def test_changed_receipt_invalidates_completion(self):
        self.implementation()
        self.evidence()
        self.complete_task("T-001")
        (self.root / "evidence/chk-001-pass.md").write_text("Edited result text.\n")
        self.assertIn("false-completion", self.codes())

    def test_changed_check_or_acceptance_invalidates_result_and_task_review(self):
        self.implementation()
        self.evidence()
        self.complete_task("T-001")
        path = self.work / "tasks.md"
        path.write_text(path.read_text().replace("assert one stored record", "assert two replicated records"))
        report = inspect_work(self.root)
        self.assertIn("false-completion", self.codes(report))
        self.assertEqual(report["reviews"]["tasks"]["status"], "stale")

    def test_additional_task_checkbox_is_substantive_content_for_evidence(self):
        self.implementation()
        self.evidence()
        self.complete_task("T-001")
        path = self.work / "tasks.md"
        path.write_text(path.read_text().replace("- Activity: complete", "- [ ] Encrypt every persisted record with the newly required key.\n- Activity: complete", 1))
        report = inspect_work(self.root)
        self.assertFalse(report["evidence"]["CHK-001"]["current"])
        self.assertFalse(report["tasks"][0]["completion_valid"])
        self.assertIn("false-completion", self.codes(report))
        with self.assertRaises(WorkflowError):
            self.review("tasks")

    def test_latest_failed_result_supersedes_old_pass(self):
        self.implementation()
        self.evidence()
        self.complete_task("T-001")
        self.evidence(result="fail")
        report = inspect_work(self.root)
        self.assertEqual(report["evidence"]["CHK-001"]["result"], "fail")
        self.assertIn("false-completion", self.codes(report))

    def test_duplicate_contract_task_and_check_ids_are_errors(self):
        self.artifacts()
        for name, extra in (("requirements.md", "\n## REQ-001 — Duplicate\n"),
                            ("tasks.md", "\n### T-001 — Duplicate\n- [ ] T-001 complete\n")):
            with self.subTest(name=name):
                path = self.work / name
                original = path.read_text()
                path.write_text(original + extra)
                self.assertIn("duplicate-id", self.codes())
                path.write_text(original)
        path = self.work / "tasks.md"
        path.write_text(path.read_text() + "\n| CHK-001 | REQ-001 | T-001 | Duplicate | none |\n")
        self.assertIn("duplicate-id", self.codes())

    def test_dependency_cycle_and_dangling_reference_are_errors(self):
        self.artifacts()
        path = self.work / "tasks.md"
        path.write_text(path.read_text().replace("- Prerequisites: none", "- Prerequisites: T-002"))
        self.assertIn("dependency-cycle", self.codes())
        path.write_text(TASKS.replace("- Prerequisites: T-001", "- Prerequisites: T-999"))
        self.assertIn("dangling-reference", self.codes())

    def test_missing_coverage_blocks_plan_acceptance(self):
        self.artifacts()
        path = self.work / "requirements.md"
        path.write_text(path.read_text() + "\n| REQ-003 | Delete on request. | Removal is observable. | Required |\n")
        with self.assertRaises(WorkflowError):
            self.review("tasks")

    def test_deferred_word_in_required_behavior_does_not_remove_coverage(self):
        self.artifacts()
        path = self.work / "requirements.md"
        path.write_text(path.read_text() + "| REQ-003 | When a notification is deferred, retry delivery. | Eventual delivery succeeds. | Required |\n")
        self.assertIn("missing-coverage", self.codes())
        with self.assertRaises(WorkflowError):
            self.review("tasks")

    def test_only_explicit_deferred_status_removes_required_coverage(self):
        self.artifacts()
        path = self.work / "requirements.md"
        path.write_text(path.read_text() + "| REQ-003 | Retain a separate audit export. | Export exists. | Deferred |\n")
        self.assertNotIn("missing-coverage", self.codes())
        self.review("tasks")

    def test_task_and_check_links_must_be_reciprocal(self):
        self.artifacts()
        path = self.work / "tasks.md"
        path.write_text(path.read_text().replace("| CHK-001 | REQ-001 | T-001 |", "| CHK-001 | REQ-001 | T-002 |"))
        self.assertIn("inconsistent-check-link", self.codes())

    def test_invalid_ids_and_fake_activity_completion_are_errors(self):
        self.artifacts()
        path = self.work / "tasks.md"
        path.write_text(path.read_text().replace("- Activity: ready", "- Activity: complete", 1))
        self.assertIn("false-completion", self.codes())
        path.write_text(TASKS.replace("T-001", "T-1"))
        self.assertIn("invalid-id", self.codes())

    def test_unsafe_ids_artifact_paths_and_symlink_escapes_are_rejected(self):
        with self.assertRaises(WorkflowError):
            new_work(self.root, "../escape", "Escape")
        self.metadata(artifacts={"requirements": "../../outside.md", "design": "design.md", "tasks": "tasks.md"})
        self.assertIn("artifact-path", self.codes())
        with tempfile.TemporaryDirectory() as external:
            (self.root / "outside").symlink_to(external, target_is_directory=True)
            self.metadata(context_files=["outside/secret.md"])
            self.assertIn("context-path", self.codes())

    def test_activation_cannot_replace_an_in_root_symlink_referent(self):
        protected = self.root / "existing-state.json"
        protected.write_text('{"important":"preserve"}\n')
        pointer = self.root / ".codex/workflow.json"
        pointer.unlink()
        pointer.symlink_to(protected)
        before = protected.read_bytes()
        with self.assertRaises(WorkflowError):
            new_work(self.root, "0200-second", "Second", activate=True)
        self.assertEqual(protected.read_bytes(), before)
        self.assertTrue(pointer.is_symlink())
        self.assertFalse((self.root / "specs/0200-second").exists())

    def test_new_work_cannot_follow_specs_symlink_into_git_metadata(self):
        with tempfile.TemporaryDirectory() as another_root:
            target = Path(another_root)
            objects = target / ".git/objects"
            objects.mkdir(parents=True)
            (target / "specs").symlink_to(objects, target_is_directory=True)
            with self.assertRaises(WorkflowError):
                new_work(target, "0100-test", "Test")
            self.assertEqual(list(objects.iterdir()), [])

    def test_all_mutations_reject_symlink_work_metadata(self):
        self.implementation()
        self.evidence()
        metadata = self.work / "work.json"
        protected = self.root / "existing-ledger.json"
        metadata.rename(protected)
        metadata.symlink_to(protected)
        before = protected.read_bytes()
        actions = (
            lambda: self.review("tasks"),
            lambda: advance(self.root, self.work_id, "verification"),
            lambda: record_evidence(self.root, self.work_id, "CHK-001", "evidence/chk-001-pass.md", "pass", "Recorded test", "local", "fixture", "2026-11-22T00:00:00+00:00", ["service.py"]),
        )
        for action in actions:
            with self.subTest(action=action):
                with self.assertRaises(WorkflowError):
                    action()
                self.assertEqual(protected.read_bytes(), before)
                self.assertTrue(metadata.is_symlink())

    def test_direct_git_artifact_reference_is_rejected(self):
        self.metadata(artifacts={"requirements": ".git/config", "design": "design.md", "tasks": "tasks.md"})
        self.assertIn("artifact-path", self.codes())

    def test_malformed_record_types_return_validation_errors(self):
        self.metadata(facts=[{"id": [], "kind": [], "statement": None, "source": None}],
                      questions=[{"id": [], "prompt": None, "why": None, "status": [], "blocks": None}],
                      reviews=[{"id": [], "artifact": "tasks", "hashes": [], "reviewer": []}],
                      evidence=[{"id": [], "check": []}])
        self.assertTrue(self.errors())

    def test_interrupted_state_never_appears_complete(self):
        self.metadata(phase="complete")
        (self.work / "requirements.md").unlink()
        self.assertIn("false-completion", self.codes())
        self.assertIn("missing-artifact", self.codes())
        (self.work / "work.json").write_text('{"schema_version":')
        with self.assertRaises(WorkflowError):
            inspect_work(self.root)

    def test_unreadable_task_text_returns_issues_instead_of_a_hashing_crash(self):
        self.implementation()
        (self.work / "tasks.md").write_bytes(b"\xff\xfe corrupted task text")
        report = inspect_work(self.root)
        self.assertIn("artifact-path", self.codes(report))
        self.assertIn("stale-review", self.codes(report))
        self.assertEqual(report["eligible_tasks"], [])

    def test_new_never_overwrites_existing_work(self):
        before = (self.work / "work.json").read_bytes()
        with self.assertRaises(WorkflowError):
            new_work(self.root, self.work_id, "Replacement")
        self.assertEqual(before, (self.work / "work.json").read_bytes())

    def test_invalid_active_pointer_destination_is_rejected_before_new_work(self):
        pointer = self.root / ".codex/workflow.json"
        pointer.unlink()
        pointer.mkdir()
        with self.assertRaises(WorkflowError):
            new_work(self.root, "0200-second", "Second work", activate=True)
        self.assertFalse((self.root / "specs/0200-second").exists())

    def test_activation_write_failure_reports_preserved_partial_success(self):
        pointer = self.root / ".codex/workflow.json"
        before = pointer.read_bytes()

        def write_with_pointer_failure(path, value):
            if path == pointer:
                raise PermissionError("fixture rejects pointer write")
            atomic_json(path, value)

        with patch("workflow_engine.engine.atomic_json", side_effect=write_with_pointer_failure):
            with self.assertRaisesRegex(WorkflowError, "was created.*activation failed"):
                new_work(self.root, "0200-second", "Second work", activate=True)
        self.assertEqual(pointer.read_bytes(), before)
        self.assertEqual(inspect_work(self.root, "0200-second")["phase"], "consultation")

    def test_evidence_needs_actual_provenance_and_a_tested_input(self):
        self.artifacts()
        with self.assertRaises(WorkflowError):
            record_evidence(self.root, self.work_id, "CHK-001", "receipt.md", "pass", "", "fixture", "fixture", "today", [])

    def test_blocking_execution_question_prevents_eligibility(self):
        self.implementation()
        self.metadata(questions=[{"id": "Q-001", "prompt": "Which explicitly authorized target?", "why": "Execution scope is unresolved.",
                                  "recommendation": "", "status": "open", "answer": "", "source": "", "blocks": ["implementation"]}])
        report = inspect_work(self.root)
        self.assertEqual(report["dependency_ready_tasks"], ["T-001"])
        self.assertEqual(report["eligible_tasks"], [])


if __name__ == "__main__":
    unittest.main()
