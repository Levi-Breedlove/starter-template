#!/usr/bin/env python3
"""Measure frozen context-rendering fixtures; no model, network, or AWS calls.

An optional baseline directory must contain trusted prior codex_hooks.py and
workflow.py scripts extracted from the recorded repository revision. Importing
those scripts executes their Python module definitions; inspect them first.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def frozen_reports():
    base = {
        "schema_version": 1, "id": "fixture-work", "title": "Known bounded change",
        "mode": "brownfield", "route": "quick", "phase": "implementation",
        "artifacts": {name: f"specs/fixture-work/{name}.md" for name in ("requirements", "design", "tasks")},
        "context_files": ["project/brief.md", "delivery/current-handoff.md"],
        "known_facts": [{"id": "F-001", "kind": "supplied", "statement": "Preserve the existing architecture.", "source": "project/brief.md"}],
        "answered_questions": [{"id": "Q-001", "status": "answered", "prompt": "Who uses it?", "answer": "Existing staff users.", "source": "project/brief.md"}],
        "open_questions": [], "next_questions": [], "deferred_questions": [],
        "reviews": {"requirements": {"status": "missing"}, "design": {"status": "missing"}, "tasks": {"status": "accepted", "decision_ref": "docs/decisions/001.md"}},
        "tasks": [{"id": "T-001", "title": "Implement the bounded change", "checked": False, "dependencies": [], "requirements": ["REQ-001"], "design": ["DES-001"], "checks": ["CHK-001"], "blocked_reason": "", "completion_valid": False}],
        "checks": [{"id": "CHK-001", "requirements": ["REQ-001"], "tasks": ["T-001"], "method": "Inspect the required behavior."}],
        "evidence": {}, "dependency_ready_tasks": ["T-001"], "eligible_tasks": ["T-001"],
        "issues": [], "consultant_instructions": ["Reuse known answers; inspect required sources; verify the accepted outcome."],
    }
    history = deepcopy(base)
    history["title"], history["phase"] = "Large completed work history", "complete"
    history["tasks"] = [{**base["tasks"][0], "id": f"T-{i:03d}", "title": f"Completed outcome {i}", "checked": True, "completion_valid": True} for i in range(1, 501)]
    history["known_facts"] = [{"id": f"F-{i:03d}", "kind": "supplied", "statement": "Saved context " + "x" * 180, "source": "project/brief.md"} for i in range(1, 61)]
    history["answered_questions"] = [{"id": f"Q-{i:03d}", "status": "answered", "prompt": "Previously settled decision", "answer": "Confirmed answer " + "y" * 180, "source": "project/brief.md"} for i in range(1, 61)]
    history["eligible_tasks"], history["dependency_ready_tasks"] = [], []
    error = deepcopy(base)
    error["title"] = "L" * 20000
    error["issues"] = [{"severity": "error", "code": "stale-evidence", "message": "The recorded source changed; inspect the receipt before claiming completion.", "path": "evidence/fixture-work/check.md"}]
    error["eligible_tasks"] = []
    return {"bounded_work": base, "large_history": history, "long_title_with_error": error}


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def measure(text):
    return {"characters": len(text), "utf8_bytes": len(text.encode("utf-8")), "retains_stale_error": "stale-evidence" in text}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-dir", type=Path, help="Trusted prior renderer scripts; no fetching is performed")
    args = parser.parse_args()
    from workflow_engine.context import build_context_packet, render_context_packet, prompt_pulse
    prior_hook = prior_cli = None
    identities = {}
    if args.baseline_dir:
        for filename in ("codex_hooks.py", "workflow.py"):
            path = args.baseline_dir / filename
            identities[filename] = hashlib.sha256(path.read_bytes()).hexdigest()
        prior_hook = load_module(args.baseline_dir / "codex_hooks.py", "prior_workflow_hooks")
        prior_cli = load_module(args.baseline_dir / "workflow.py", "prior_workflow_cli")
    observations = {}
    for name, report in frozen_reports().items():
        packet = build_context_packet(report)
        row = {
            "fixture_sha256": hashlib.sha256(json.dumps(report, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
            "current_startup": measure(render_context_packet(packet)),
            "current_refresh": measure(prompt_pulse(report)),
        }
        if prior_hook:
            row["prior_startup_and_refresh"] = measure(prior_hook.context_text(report))
            row["prior_full_cli_context"] = measure(prior_cli.render(report, context=True))
        observations[name] = row
    print(json.dumps({"scope": "Frozen renderer fixtures; characters and bytes only; no tokenizer, model, cost or client activation benchmark", "baseline_sha256": identities, "observations": observations}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
