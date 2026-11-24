"""Specification request/record/reconciliation fixtures; no model or cloud run."""

from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from workflow_engine.context import build_context_packet
from workflow_engine.engine import WorkflowError, advance, inspect_work, new_work, record_evidence, record_review
from workflow_engine.specifications import (
    PATTERNS, analyze_requirements, apply_reconciliation, derive_properties,
    ears_pattern, lint_ears, plan_reconciliation, record_specification_result,
    specification_status,
)


CONTRACT = """# Requirements

| ID | Condition and required outcome | Acceptance criterion | Required or deferred |
| --- | --- | --- | --- |
| REQ-001 | WHEN a request repeats, THE service SHALL return the original result. | One stored result. | Required |
| REQ-002 | WHILE maintenance is active, THE service SHALL reject new writes. | Existing reads continue. | Required |
"""

DESIGN = """# Design

## DES-001 — Preserve the interface

Use an atomic record and the existing maintenance configuration.
"""


def task_plan():
    rows = []
    text = "# Task plan\n\n"
    for n, requirements, dependency in ((1, "REQ-001", "none"), (2, "REQ-002", "none"), (3, "REQ-001", "T-001")):
        text += f"""### T-{n:03d} — Verify outcome {n}

- [ ] T-{n:03d} complete
- Activity: ready
- Contract / design: {requirements} / DES-001
- Prerequisites: {dependency}
- Scope and exclusions: Only the declared operation.
- Acceptance: Preserve the required result.
- Verification: CHK-{n:03d}
- Evidence / review: none
- Blocker: none

"""
        rows.append(f"| CHK-{n:03d} | {requirements} | T-{n:03d} | Exercise the stated outcome. | Not run |")
    return text + "## Verification matrix\n\n| Check | Requirement | Task | Method | Evidence |\n| --- | --- | --- | --- | --- |\n" + "\n".join(rows) + "\n"


class SpecificationFixtures(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.work_id = "0100-fixture"
        new_work(self.root, self.work_id, "Fixture", activate=True)
        self.work = self.root / "specs" / self.work_id
        (self.work / "requirements.md").write_text(CONTRACT)
        (self.root / "notes").mkdir()
        (self.root / "first.py").write_text("first = 1\n")
        (self.root / "second.py").write_text("second = 1\n")

    def data(self, **changes):
        path = self.work / "work.json"
        value = json.loads(path.read_text())
        value.update(changes)
        path.write_text(json.dumps(value))
        return value

    def response(self, operation="analyze", blocker=False, mapping=True):
        request = analyze_requirements(self.root) if operation == "analyze" else derive_properties(self.root)
        reference = f"notes/{operation}-review.md"
        (self.root / reference).write_text("Fixture-only simulated review; no model or application behavior was exercised.\n")
        value = {key: deepcopy(request[key]) for key in ("schema_version", "operation", "request_id", "input_hashes", "context_fingerprint")}
        value.update(reviewer="Fixture reviewer", review_ref=reference, observed_at="2026-11-22T12:00:00+00:00", summary="Fixture-only semantic review response.")
        if operation == "analyze":
            value["findings"] = [{"id": "ANA-001", "requirement_ids": ["REQ-001"], "severity": "blocker", "category": "ambiguity", "statement": "The retry boundary needs a business decision.", "state": "open", "resolution": "", "source": f"specs/{self.work_id}/requirements.md"}] if blocker else []
        else:
            value["properties"] = [{"id": f"PROP-{n:03d}", "requirement_ids": [f"REQ-{n:03d}"], "statement": f"Required invariant {n} remains true.", "preconditions": "A valid request and the documented operating state.", "strategy": "example", "verification": "Exercise the stated condition and observe the required result.", "task_ids": [f"T-{n:03d}"] if mapping else [], "check_ids": [f"CHK-{n:03d}"] if mapping else [], "source": f"specs/{self.work_id}/requirements.md"} for n in (1, 2)]
        return value

    def record(self, value):
        relative = f"notes/{value['operation']}-response.json"
        (self.root / relative).write_text(json.dumps(value))
        return record_specification_result(self.root, self.work_id, value["operation"], relative)

    def implementation(self, route="requirements-first"):
        self.data(route=route)
        (self.work / "design.md").write_text(DESIGN)
        (self.work / "tasks.md").write_text(task_plan())
        stages = ("tasks",) if route == "quick" else ("design", "requirements", "tasks") if route == "design-first" else ("requirements", "design", "tasks")
        for phase in stages:
            advance(self.root, self.work_id, phase)
            record_review(self.root, self.work_id, phase, "accepted", "Fixture-only delegated decision", "Fixture reviewer", "delegated")
        advance(self.root, self.work_id, "implementation")

    def complete_all(self):
        self.implementation()
        for n in (1, 2, 3):
            receipt = f"notes/check-{n}.md"
            (self.root / receipt).write_text("Fixture-only simulated passing check.\n")
            record_evidence(self.root, self.work_id, f"CHK-{n:03d}", receipt, "pass", "Fixture simulation", "Temporary project", "Fixture candidate", "2026-11-22T12:00:00+00:00", ["second.py" if n == 2 else "first.py"])
            path = self.work / "tasks.md"
            text = path.read_text().replace(f"- [ ] T-{n:03d} complete\n- Activity: ready", f"- [x] T-{n:03d} complete\n- Activity: complete")
            path.write_text(text)
        advance(self.root, self.work_id, "verification")
        advance(self.root, self.work_id, "complete")

    def test_all_six_ears_patterns_and_multiline(self):
        for pattern, sentence in PATTERNS.items():
            with self.subTest(pattern=pattern):
                self.assertEqual(ears_pattern(sentence), pattern)
        self.assertEqual(ears_pattern("WHEN a request arrives,\n THE service SHALL respond."), "event")

    def test_malformed_unwanted_and_combined_conditions_are_visible(self):
        for sentence in ("IF a call fails, THE service SHALL retry.", "WHEN a call arrives, WHERE an option exists, THE service SHALL respond.", "The service should be fast.", "THE service SHALL"):
            self.assertIsNone(ears_pattern(sentence), sentence)
        self.assertEqual(lint_ears(CONTRACT)["findings"], [])
        result = lint_ears(CONTRACT.replace("return the original result", "respond quickly"))
        self.assertTrue(any(f["code"] == "ambiguous-language" and f["severity"] == "warning" for f in result["findings"]))

    def test_defect_observations_and_explicit_deferred_rows_are_not_required_ears(self):
        content = """# Bug

## DEF-001 — Observed error

A retry duplicated the record in the supplied reproduction.

## FIX-001 — Correction

WHEN a request repeats, THE service SHALL return the original result.

| ID | Behavior | Acceptance | Required or deferred |
| --- | --- | --- | --- |
| KEEP-001 | WHILE maintenance is active, THE service SHALL preserve reads. | Reads pass. | Required |
| REQ-099 | Future idea is unresolved. | Later. | Deferred |
"""
        lint = lint_ears(content)
        self.assertEqual(lint["findings"], [])
        self.assertEqual({r["id"] for r in lint["requirements"] if r["required"]}, {"FIX-001", "KEEP-001"})

    def test_request_does_not_create_reviews_or_claim_semantic_execution(self):
        before = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        request = analyze_requirements(self.root)
        self.assertFalse(request["writes"])
        self.assertFalse(request["model_called"])
        self.assertEqual(request["deterministic_findings"], [])
        self.assertIn("response_schema", request)
        self.assertEqual(before, {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        self.assertEqual(json.loads((self.work / "work.json").read_text())["reviews"], [])

    def test_only_selected_foundations_affect_review_identity_and_reconciliation(self):
        manifest = ".aws-workflow/manifest.json"
        paths = {"brief": "notes/product.md", "requirements": "notes/system.md", "tech": "notes/stack.md",
                 "structure": "notes/ownership.md", "architecture": "notes/architecture.md",
                 "handoff": "notes/handoff.md", "adoption_report": "notes/intake.md",
                 "environment_capabilities": "notes/environment.md"}
        for relative in paths.values():
            (self.root / relative).write_text("Existing project decision.\n")
        (self.root / manifest).parent.mkdir()
        (self.root / manifest).write_text(json.dumps({"schema_version": 2, "identity": "codex-aws-workflow", "paths": paths}))
        selected = [manifest, paths["brief"], paths["handoff"], paths["requirements"]]
        self.data(context_files=selected)
        request = analyze_requirements(self.root)
        self.assertIn(paths["requirements"], request["input_hashes"])
        self.assertNotIn(paths["architecture"], request["input_hashes"])
        fingerprint = build_context_packet(inspect_work(self.root))["fingerprint"]
        (self.root / paths["requirements"]).write_text("Updated system requirement.\n")
        self.assertNotEqual(build_context_packet(inspect_work(self.root))["fingerprint"], fingerprint)
        request = analyze_requirements(self.root)
        self.record(self.response())
        (self.root / paths["architecture"]).write_text("Architecture outside this work changed.\n")
        self.assertEqual(analyze_requirements(self.root)["request_id"], request["request_id"])
        self.assertEqual(plan_reconciliation(self.root)["operation_refreshes"], [])

        self.data(context_files=[*selected, paths["architecture"]])
        preview = plan_reconciliation(self.root)
        self.assertIn(paths["architecture"], preview["changed_paths"])
        self.assertEqual(preview["operation_refreshes"], ["analyze"])
        self.record(self.response())
        (self.root / paths["architecture"]).write_text("Changed accepted trust boundary.\n")
        self.assertIn(paths["architecture"], plan_reconciliation(self.root)["changed_paths"])
        self.record(self.response())
        self.data(context_files=selected)
        self.assertIn(paths["architecture"], plan_reconciliation(self.root)["changed_paths"])

    def test_record_keeps_real_provenance_and_idempotent_import(self):
        value = self.response()
        result = self.record(value)
        self.assertEqual(result["operations"]["analyze"]["status"], "current")
        self.record(value)
        history = json.loads((self.work / "analysis.json").read_text())
        self.assertEqual(len(history["records"]), 1)
        self.assertEqual(history["records"][0]["response"]["reviewer"], "Fixture reviewer")
        self.assertEqual(json.loads((self.work / "work.json").read_text())["reviews"], [])

    def test_changed_requirement_or_actual_decision_source_rejects_import(self):
        for change in ("contract", "decision"):
            with self.subTest(change=change):
                (self.root / "notes/decision.md").write_text("One supplied business decision.\n")
                self.data(facts=[{"id": "F-001", "kind": "supplied", "statement": "Use the recorded policy.", "source": "notes/decision.md"}])
                value = self.response()
                path = self.work / "requirements.md" if change == "contract" else self.root / "notes/decision.md"
                path.write_text(path.read_text() + "\nChanged actual input.\n")
                with self.assertRaisesRegex(WorkflowError, "exact current request"):
                    self.record(value)
        self.assertFalse((self.work / "analysis.json").exists())

    def test_later_design_and_task_progress_do_not_stale_requirement_analysis(self):
        self.record(self.response())
        (self.work / "design.md").write_text(DESIGN)
        (self.work / "tasks.md").write_text(task_plan())
        self.data(phase="requirements")
        result = specification_status(self.root, inspect_work(self.root))
        self.assertEqual(result["operations"]["analyze"]["status"], "current")

    def test_blocking_findings_persist_until_a_current_response_resolves_them(self):
        value = self.response(blocker=True)
        self.record(value)
        result = specification_status(self.root, inspect_work(self.root))
        self.assertEqual(len(result["blocking_findings"]), 1)
        self.assertTrue(any(i["code"] == "specification-blocker" for i in result["issues"]))
        (self.work / "requirements.md").write_text(CONTRACT + "\nDecision clarified in the contract.\n")
        result = specification_status(self.root, inspect_work(self.root))
        self.assertEqual(result["operations"]["analyze"]["status"], "stale")
        self.assertEqual(len(result["blocking_findings"]), 1)
        updated = self.response(blocker=True)
        updated["findings"][0].update(state="resolved", resolution="The actual clarified retry policy is now recorded in the contract.")
        result = self.record(updated)
        self.assertEqual(result["blocking_findings"], [])
        self.assertEqual(len(json.loads((self.work / "analysis.json").read_text())["records"]), 2)

    def test_unknown_duplicate_and_unresolved_response_claims_rejected(self):
        original = self.response(blocker=True)
        variants = []
        unknown = deepcopy(original); unknown["findings"][0]["requirement_ids"] = ["REQ-999"]; variants.append(unknown)
        duplicate = deepcopy(original); duplicate["findings"].append(deepcopy(duplicate["findings"][0])); variants.append(duplicate)
        unresolved = deepcopy(original); unresolved["findings"][0]["state"] = "resolved"; variants.append(unresolved)
        extra = deepcopy(original); extra["approved"] = True; variants.append(extra)
        for value in variants:
            with self.assertRaises(WorkflowError):
                self.record(value)
        self.assertFalse((self.work / "analysis.json").exists())

    def test_history_cannot_hide_a_changed_or_different_response(self):
        self.record(self.response(blocker=True))
        path = self.work / "analysis.json"
        history = json.loads(path.read_text()); history["records"][-1]["response"]["findings"] = []; path.write_text(json.dumps(history))
        result = specification_status(self.root, inspect_work(self.root))
        self.assertEqual(result["operations"]["analyze"]["status"], "invalid")
        self.assertTrue(any("differs" in issue["message"] for issue in result["issues"]))

    def test_resolved_finding_and_property_external_sources_are_bound(self):
        (self.work / "design.md").write_text(DESIGN)
        for operation in ("analyze", "properties"):
            with self.subTest(operation=operation):
                path = self.root / f"notes/{operation}-decision.md"
                path.write_text("Fixture decision or inspected evidence.\n")
                value = self.response(operation, blocker=True)
                entries = value["findings" if operation == "analyze" else "properties"]
                entries[0]["source"] = path.relative_to(self.root).as_posix() + "#actual-decision"
                if operation == "analyze":
                    entries[0].update(state="resolved", resolution="Use the actual separately recorded decision.")
                self.record(value)
                path.write_text("The decision or inspected evidence changed.\n")
                result = specification_status(self.root, inspect_work(self.root))
                self.assertEqual(result["operations"][operation]["status"], "stale")

    def test_malformed_history_receipt_identity_is_invalid(self):
        self.record(self.response())
        path = self.work / "analysis.json"
        original = json.loads(path.read_text())
        for relative, digest in (("../outside.md", "0" * 64), ("notes/review.md", 7)):
            with self.subTest(relative=relative):
                value = deepcopy(original)
                value["records"][-1]["receipt_inputs"][relative] = digest
                path.write_text(json.dumps(value))
                result = specification_status(self.root, inspect_work(self.root))
                self.assertEqual(result["operations"]["analyze"]["status"], "invalid")

    def test_property_coverage_and_actual_task_links(self):
        (self.work / "design.md").write_text(DESIGN)
        (self.work / "tasks.md").write_text(task_plan())
        value = self.response("properties")
        result = self.record(value)
        self.assertEqual(result["operations"]["properties"]["task_mapping"], "complete")
        for mutate in (lambda v: v["properties"].pop(), lambda v: v["properties"][0].update(check_ids=["CHK-002"]), lambda v: v["properties"][0].update(task_ids=["T-999"])):
            bad = deepcopy(value); mutate(bad)
            with self.assertRaises(WorkflowError):
                self.record(bad)

    def test_properties_can_precede_tasks_but_mapping_must_be_completed(self):
        (self.work / "design.md").write_text(DESIGN)
        result = self.record(self.response("properties", mapping=False))
        self.assertEqual(result["operations"]["properties"]["task_mapping"], "incomplete")
        (self.work / "tasks.md").write_text(task_plan())
        result = specification_status(self.root, inspect_work(self.root))
        self.assertEqual(result["operations"]["properties"]["status"], "current")
        self.assertEqual(result["operations"]["properties"]["task_mapping"], "incomplete")
        result = self.record(self.response("properties", mapping=True))
        self.assertEqual(result["operations"]["properties"]["task_mapping"], "complete")

    def test_property_proposed_ids_are_validated_when_tasks_arrive(self):
        (self.work / "design.md").write_text(DESIGN)
        value = self.response("properties")
        value["properties"][0]["task_ids"] = ["T-999"]
        self.record(value)
        (self.work / "tasks.md").write_text(task_plan())
        result = specification_status(self.root, inspect_work(self.root))
        self.assertEqual(result["operations"]["properties"]["status"], "invalid")

    def test_spec_format_is_opt_in_and_lint_does_not_claim_semantics(self):
        self.implementation()
        (self.work / "requirements.md").write_text(CONTRACT.replace("THE service SHALL", "the service should"))
        legacy = specification_status(self.root, inspect_work(self.root))
        self.assertFalse(any(i["code"] == "ears-shape" for i in legacy["issues"]))
        self.data(spec_format="ears")
        opted = specification_status(self.root, inspect_work(self.root))
        self.assertTrue(any(i["code"] == "ears-shape" for i in opted["issues"]))

    def test_sync_reopens_affected_descendants_and_preserves_valid_sibling(self):
        self.complete_all()
        old = json.loads((self.work / "work.json").read_text())
        (self.root / "first.py").write_text("first = 2\n")
        before_tasks = (self.work / "tasks.md").read_bytes()
        plan = plan_reconciliation(self.root)
        self.assertEqual(plan["reopen_tasks"], ["T-001", "T-003"])
        self.assertEqual(plan["target_phase"], "implementation")
        self.assertEqual((self.work / "tasks.md").read_bytes(), before_tasks)
        result = apply_reconciliation(self.root, None, plan["fingerprint"], "A source dependency changed; repeat affected acceptance checks.")
        tasks = {t["id"]: t for t in result["report"]["tasks"]}
        self.assertFalse(tasks["T-001"]["checked"])
        self.assertFalse(tasks["T-003"]["checked"])
        self.assertTrue(tasks["T-002"]["completion_valid"])
        now = json.loads((self.work / "work.json").read_text())
        self.assertEqual(now["reviews"], old["reviews"])
        self.assertEqual(now["evidence"], old["evidence"])
        self.assertEqual(now["reconciliations"][0]["from_phase"], "complete")

    def test_sync_rewinds_changed_contract_to_route_boundary(self):
        for route, expected in (("requirements-first", "requirements"), ("design-first", "design"), ("quick", "tasks")):
            with self.subTest(route=route):
                self.data(route="requirements-first", phase="consultation", reviews=[], evidence=[])
                self.implementation(route)
                path = self.work / ("design.md" if route == "design-first" else "requirements.md")
                path.write_text(path.read_text() + "\nSubstantive changed constraint.\n")
                plan = plan_reconciliation(self.root)
                self.assertEqual(plan["target_phase"], expected)

    def test_changed_decision_context_rewinds_review_even_without_prose_change(self):
        self.record(self.response())
        self.implementation()
        self.data(facts=[{"id": "F-001", "kind": "supplied", "statement": "The owner supplied a new relevant constraint.", "source": "User conversation: fixture"}])
        plan = plan_reconciliation(self.root)
        self.assertEqual(plan["changed_decision_context"], ["analyze"])
        self.assertEqual(plan["target_phase"], "requirements")

    def test_context_reassessment_preserves_completions_without_identified_contract_change(self):
        self.complete_all()
        self.record(self.response())
        self.data(facts=[{"id": "F-001", "kind": "supplied", "statement": "A newly supplied constraint needs assessment.", "source": "User conversation: fixture"}])
        plan = plan_reconciliation(self.root)
        self.assertEqual(plan["target_phase"], "requirements")
        self.assertEqual(plan["reopen_tasks"], [])
        result = apply_reconciliation(self.root, None, plan["fingerprint"], "Assess the new constraint before changing the contract.")
        self.assertTrue(all(task["completion_valid"] for task in result["report"]["tasks"]))

    def test_changed_analysis_receipt_or_external_evidence_rewinds_without_erasing_valid_tasks(self):
        self.complete_all()
        value = self.response(blocker=True)
        (self.root / "notes/resolution.md").write_text("Fixture resolution evidence.\n")
        value["findings"][0].update(state="resolved", resolution="Use the recorded actual decision.", source="notes/resolution.md")
        self.record(value)
        for relative in ("notes/analyze-review.md", "notes/resolution.md"):
            with self.subTest(relative=relative):
                path = self.root / relative
                before = path.read_text()
                path.write_text(before + "\nUpdated observation.\n")
                plan = plan_reconciliation(self.root)
                self.assertEqual(plan["operation_refreshes"], ["analyze"])
                self.assertEqual(plan["target_phase"], "requirements")
                self.assertEqual(plan["reopen_tasks"], [])
                self.assertIn(relative, plan["changed_paths"])
                path.write_text(before)

    def test_stale_preview_and_unsafe_paths_preserve_bytes(self):
        self.complete_all()
        (self.root / "first.py").write_text("first = 2\n")
        plan = plan_reconciliation(self.root)
        (self.root / "second.py").write_text("second = 2\n")
        before = {p.name: p.read_bytes() for p in self.work.iterdir() if p.is_file()}
        with self.assertRaisesRegex(WorkflowError, "preview is stale"):
            apply_reconciliation(self.root, None, plan["fingerprint"], "Actual source changes.")
        with self.assertRaises(WorkflowError):
            plan_reconciliation(self.root, changed_paths=["../outside"])
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.work.iterdir() if p.is_file()})

    def test_reconciliation_rolls_back_its_task_edit_on_metadata_failure(self):
        self.complete_all()
        (self.root / "first.py").write_text("first = 2\n")
        plan = plan_reconciliation(self.root)
        before = {p.name: p.read_bytes() for p in self.work.iterdir() if p.is_file()}
        from workflow_engine import specifications
        original = specifications._atomic_text
        failed = False

        def fail_metadata(path, text):
            nonlocal failed
            if path.name == "work.json" and not failed:
                failed = True
                raise OSError("Fixture write failure")
            return original(path, text)

        with patch.object(specifications, "_atomic_text", side_effect=fail_metadata):
            with self.assertRaisesRegex(WorkflowError, "rolled back"):
                apply_reconciliation(self.root, None, plan["fingerprint"], "Actual source change.")
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.work.iterdir() if p.is_file()})

    def test_symlink_response_and_missing_review_notes_are_rejected(self):
        value = self.response()
        (self.root / "notes/actual.json").write_text(json.dumps(value))
        (self.root / "notes/linked.json").symlink_to(self.root / "notes/actual.json")
        with self.assertRaises(WorkflowError):
            record_specification_result(self.root, self.work_id, "analyze", "notes/linked.json")
        value["review_ref"] = "notes/absent.md"
        with self.assertRaises(WorkflowError):
            self.record(value)

    def test_operation_history_cannot_be_its_own_decision_source(self):
        self.record(self.response())
        self.data(facts=[{"id": "F-001", "kind": "supplied", "statement": "Use a recorded decision.", "source": f"specs/{self.work_id}/analysis.json"}])
        with self.assertRaisesRegex(WorkflowError, "mutable operation histories"):
            analyze_requirements(self.root)


if __name__ == "__main__":
    unittest.main()
