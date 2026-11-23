#!/usr/bin/env python3
"""Specification workflow, local inspection, and explicit bounded execution."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Inspection must not create cache files in a newly adopted source package.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from workflow_engine import WorkflowError, build_context_packet, inspect_work, render_context_packet
from workflow_engine.engine import ARTIFACTS, ROUTES, advance, new_work, record_evidence, record_review


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--root", default=".", help="Project root (default: current directory, including when this script is packaged).")
    commands = result.add_subparsers(dest="command", required=True)
    new = commands.add_parser("new", help="Create a consultation draft without inventing requirements or questions.")
    new.add_argument("work_id")
    new.add_argument("--title", required=True)
    new.add_argument("--mode", choices=("greenfield", "brownfield"), default="greenfield")
    new.add_argument("--route", choices=ROUTES, default="requirements-first")
    new.add_argument("--idea", default="")
    new.add_argument("--activate", action="store_true", help="Explicitly select this work in .codex/workflow.json.")
    new.add_argument("--spec-format", choices=("ears", "existing"), default="ears",
                     help="New work uses structured requirements and recorded analysis; existing preserves a separately selected legacy contract.")
    for name in ("context", "status", "validate", "review", "advance", "evidence"):
        command = commands.add_parser(name)
        command.add_argument("work_id", nargs="?", help="Work ID; omitted selects .codex/workflow.json active_work.")
        if name == "context":
            command.add_argument("--compact", action="store_true", help="Emit bounded actionable context; full inspection remains available without this flag.")
        if name == "review":
            command.add_argument("--artifact", choices=ARTIFACTS, required=True)
            command.add_argument("--outcome", choices=("accepted", "changes-requested"), required=True)
            command.add_argument("--decision-ref", required=True)
            command.add_argument("--reviewer", required=True)
            command.add_argument("--authority", choices=("user", "delegated"), required=True)
        if name == "advance":
            command.add_argument("--to", dest="target", required=True)
        if name == "evidence":
            command.add_argument("--check", required=True)
            command.add_argument("--record", dest="receipt", required=True)
            command.add_argument("--result", choices=("pass", "fail", "not-run"), required=True)
            command.add_argument("--method", required=True)
            command.add_argument("--environment", required=True)
            command.add_argument("--candidate", required=True)
            command.add_argument("--observed-at", required=True)
            command.add_argument("--input", dest="inputs", action="append", required=True)
        command.add_argument("--json", action="store_true", help="Emit the stable inspection object.")
    for name in ("doctor", "hooks"):
        command = commands.add_parser(name, help="Read-only setup inspection." if name == "doctor" else "Preview native hook configuration without changing trust or files.")
        command.add_argument("--json", action="store_true")
    for name in ("analyze", "properties"):
        command = commands.add_parser(name, help="Prepare a source-bound agent review, or record its actual structured response.")
        command.add_argument("work_id", nargs="?")
        command.add_argument("--record", metavar="RESPONSE", help="Validate and record an actual response JSON file relative to the project root.")
        command.add_argument("--json", action="store_true")
    sync = commands.add_parser("sync", help="Preview changed specification impact; apply only the reviewed fingerprint.")
    sync.add_argument("work_id", nargs="?")
    sync.add_argument("--changed", action="append", default=[], help="Changed project-relative input; repeat as needed.")
    sync.add_argument("--apply", action="store_true")
    sync.add_argument("--expected-fingerprint")
    sync.add_argument("--reason")
    sync.add_argument("--json", action="store_true")
    for name in ("execution-template", "run-plan", "run"):
        command = commands.add_parser(name, help="Prepare execution settings or preview/run a bounded isolated candidate.")
        command.add_argument("work_id", nargs="?")
        if name != "execution-template":
            command.add_argument("--task", help="Select one task; omitted selects the configured remaining task plan.")
        if name == "run":
            command.add_argument("--execute", action="store_true", help="Explicitly invoke Codex and the configured verification commands; may consume credits.")
            command.add_argument("--run-id", help="Optional unique run identifier; existing attempts are never silently replayed.")
        command.add_argument("--json", action="store_true")
    for name in ("run-status", "run-apply", "run-abandon"):
        command = commands.add_parser(name, help="Inspect, explicitly apply, or abandon an isolated run.")
        command.add_argument("run_id")
        if name == "run-abandon":
            command.add_argument("--reason", required=True)
        command.add_argument("--json", action="store_true")
    new.add_argument("--json", action="store_true")
    return result


def operation(args):
    """Dispatch explicit operations without loading a model backend for inspection."""
    if args.command in ("doctor", "hooks"):
        from workflow_engine.doctor import hook_preview, inspect_environment
        return (inspect_environment if args.command == "doctor" else hook_preview)(args.root)
    if args.command in ("analyze", "properties"):
        from workflow_engine.specifications import analyze_requirements, derive_properties, record_specification_result
        if args.record:
            return record_specification_result(args.root, args.work_id, args.command, args.record)
        return (analyze_requirements if args.command == "analyze" else derive_properties)(args.root, args.work_id)
    if args.command == "sync":
        from workflow_engine.specifications import apply_reconciliation, plan_reconciliation
        if args.apply:
            if not args.expected_fingerprint or not args.reason:
                raise WorkflowError("Applying reconciliation requires the preview's --expected-fingerprint and an actual --reason.")
            return apply_reconciliation(args.root, args.work_id, args.expected_fingerprint, args.reason, changed_paths=args.changed)
        if args.expected_fingerprint or args.reason:
            raise WorkflowError("--expected-fingerprint and --reason apply only with --apply; preview first.")
        return plan_reconciliation(args.root, args.work_id, changed_paths=args.changed)
    from workflow_engine.runner import abandon_run, apply_run, execute_run, execution_template, inspect_run, plan_run
    if args.command == "execution-template":
        return execution_template(args.root, args.work_id)
    if args.command == "run-plan":
        return plan_run(args.root, args.work_id, task_id=args.task)
    if args.command == "run":
        return execute_run(args.root, args.work_id, task_id=args.task, execute=args.execute, run_id=args.run_id)
    if args.command == "run-status":
        return inspect_run(args.root, args.run_id)
    if args.command == "run-apply":
        return apply_run(args.root, args.run_id)
    if args.command == "run-abandon":
        return abandon_run(args.root, args.run_id, args.reason)
    raise WorkflowError("Unknown operation.")


def render(report, context=False):
    lines = [f"{report['id']}: {report['title']}", f"Mode: {report['mode']} | Route: {report['route']} | Phase: {report['phase']}"]
    if context:
        lines += ["", "Known facts (retain these sources):"]
        lines += [f"- {fact.get('id')} [{fact.get('kind')}]: {fact.get('statement')} Source: {fact.get('source')}" for fact in report["known_facts"]] or ["- None recorded; read the supplied request and existing context before asking."]
        lines += ["", "Answered questions (reuse answers):"]
        lines += [f"- {question.get('id')}: {question.get('answer')} Source: {question.get('source')}" for question in report["answered_questions"]] or ["- None recorded."]
        lines += ["", "Next consequential questions (at most three):"]
        for question in report["next_questions"]:
            lines.append(f"- {question.get('id')}: {question.get('prompt')} Why: {question.get('why')} Recommendation: {question.get('recommendation') or 'Research or clarify before recommending.'}")
        if not report["next_questions"]:
            lines.append("- No open questions recorded. Infer from existing context whether any consequential gap remains; do not force an interview.")
        lines += ["", "Consultant instructions:", *[f"- {item}" for item in report["consultant_instructions"]]]
        lines += ["", "Context files:", *[f"- {path}" for path in report["context_files"]], *[f"- {key}: {path}" for key, path in report["artifacts"].items()]]
    lines += ["", "Reviews: " + ", ".join(f"{key}={value['status']}" for key, value in report["reviews"].items()),
              "Dependency-ready tasks: " + (", ".join(report["dependency_ready_tasks"]) or "none"),
              "Eligible in the current workflow phase: " + (", ".join(report["eligible_tasks"]) or "none")]
    if report["phase"] == "planned":
        lines.append("Planning is complete; implementation checkboxes remain authoritative and may be unfinished.")
    for task in report["tasks"]:
        lines.append(f"- [{'x' if task['checked'] else ' '}] {task['id']} {task['title']} (completion evidence: {'current pass' if task['completion_valid'] else 'unfinished or unverified'})")
    lines += [f"{item['severity'].upper()} {item['code']}: {item['message']}" for item in report["issues"]]
    return "\n".join(lines)


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command in {"doctor", "hooks", "analyze", "properties", "sync", "execution-template", "run-plan", "run", "run-status", "run-apply", "run-abandon"}:
            outcome = operation(args)
            print(json.dumps(outcome, indent=2, ensure_ascii=False))
            if args.command == "doctor":
                return int(not outcome.get("session_ready", False))
            if args.command == "run" and args.execute:
                return int(outcome.get("status") != "ready")
            if args.command == "run-apply":
                return int(outcome.get("status") != "applied")
            return 0
        if args.command == "new":
            options = {"spec_format": "ears", "specification_policy": {"analysis": "required", "properties": "required"}} if args.spec_format == "ears" else {}
            report = new_work(args.root, args.work_id, args.title, args.mode, args.route, args.idea, args.activate, **options)
        elif args.command == "review":
            report = record_review(args.root, args.work_id, args.artifact, args.outcome, args.decision_ref, args.reviewer, args.authority)
        elif args.command == "advance":
            report = advance(args.root, args.work_id, args.target)
        elif args.command == "evidence":
            report = record_evidence(args.root, args.work_id, args.check, args.receipt, args.result, args.method, args.environment, args.candidate, args.observed_at, args.inputs)
        else:
            report = inspect_work(args.root, args.work_id)
        if args.command == "context" and args.compact:
            # Both forms use the same strict-budget JSON packet. --json remains
            # accepted for callers that explicitly request machine output.
            print(render_context_packet(build_context_packet(report)))
        else:
            print(json.dumps(report, indent=2, ensure_ascii=False) if args.json else render(report, args.command == "context"))
        return int(args.command == "validate" and any(item["severity"] == "error" for item in report["issues"]))
    except (WorkflowError, OSError) as exc:
        print(f"Workflow error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
