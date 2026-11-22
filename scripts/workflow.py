#!/usr/bin/env python3
"""Command-line interface for the offline Codex AWS workflow ledger."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Inspection must not create cache files in a newly adopted source package.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from workflow_engine import WorkflowError, inspect_work
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
    for name in ("context", "status", "validate", "review", "advance", "evidence"):
        command = commands.add_parser(name)
        command.add_argument("work_id", nargs="?", help="Work ID; omitted selects .codex/workflow.json active_work.")
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
    new.add_argument("--json", action="store_true")
    return result


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
        if args.command == "new":
            report = new_work(args.root, args.work_id, args.title, args.mode, args.route, args.idea, args.activate)
        elif args.command == "review":
            report = record_review(args.root, args.work_id, args.artifact, args.outcome, args.decision_ref, args.reviewer, args.authority)
        elif args.command == "advance":
            report = advance(args.root, args.work_id, args.target)
        elif args.command == "evidence":
            report = record_evidence(args.root, args.work_id, args.check, args.receipt, args.result, args.method, args.environment, args.candidate, args.observed_at, args.inputs)
        else:
            report = inspect_work(args.root, args.work_id)
        print(json.dumps(report, indent=2, ensure_ascii=False) if args.json else render(report, args.command == "context"))
        return int(args.command == "validate" and any(item["severity"] == "error" for item in report["issues"]))
    except (WorkflowError, OSError) as exc:
        print(f"Workflow error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
