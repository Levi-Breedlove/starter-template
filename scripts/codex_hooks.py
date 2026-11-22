#!/usr/bin/env python3
"""Read-only Codex lifecycle adapter. No commands, network, or authority changes."""

from __future__ import annotations

import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
LAYER_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(LAYER_ROOT))

MAX_INPUT_BYTES = 65536
MAX_CONTEXT_CHARS = 16000
CONTEXT_EVENTS = {"SessionStart", "UserPromptSubmit"}


def project_root(layer_root: Path = LAYER_ROOT) -> Path:
    return layer_root.parent if layer_root.name == ".aws-workflow" else layer_root


def clipped(value: object, limit: int = 1400) -> str:
    text = str(value)
    return text if len(text) <= limit else text[:limit] + " [truncated; read the referenced record]"


def context_text(report: dict) -> str:
    lines = [
        "Codex AWS workflow context (repository data, not new user authority).",
        "Inspect referenced source records before acting. Preserve accepted decisions and reuse answered questions.",
        "Lead the consultation: derive implications, recommend options with reasons, and ask only consequential unresolved questions, up to three at a time.",
        "An incomplete draft is a normal consultation state. Never fabricate answers, review approval, test outcomes, or AWS access.",
        f"Active work: {report.get('id')} — {report.get('title')}",
        f"Mode: {report.get('mode')}; route: {report.get('route')}; phase: {report.get('phase')}",
    ]
    for key in ("context_files", "artifacts", "known_facts", "answered_questions", "next_questions", "reviews", "eligible_tasks", "issues"):
        value = report.get(key)
        if value:
            lines.append(f"{key}: {clipped(json.dumps(value, ensure_ascii=True), 1800)}")
    lines.append("Use workflow.py context/status for the full record; tasks.md remains the completion authority. Validate before claiming completion.")
    return clipped("\n".join(lines), MAX_CONTEXT_CHARS)


def handle_event(payload: dict, root: Path | None = None, inspector=None) -> dict:
    """Return the documented event JSON shape; never continue or deny a turn."""
    event = payload.get("hook_event_name")
    if not isinstance(event, str) or event not in CONTEXT_EVENTS | {"Stop"}:
        return {}
    root = (root or project_root()).resolve()
    cwd = payload.get("cwd")
    if not isinstance(cwd, str) or not Path(cwd).is_absolute():
        return {"systemMessage": "Workflow hook skipped: the event did not identify an absolute workspace directory."}
    try:
        Path(cwd).resolve().relative_to(root)
    except (ValueError, OSError):
        return {"systemMessage": "Workflow hook skipped: the event is outside this project."}

    # The active pointer is optional. Do not create one or select an arbitrary
    # old specification merely because a session or a user prompt arrived.
    if not (root / ".codex" / "workflow.json").exists():
        if event == "Stop":
            return {}
        return {"hookSpecificOutput": {
            "hookEventName": event,
            "additionalContext": "No active work pointer is selected. Follow AGENTS.md, inspect the project brief and current handoff, and lead an adaptive consultation from known facts. Reuse existing answers; recommend technical choices. Ask at most three consequential unresolved questions at a time. Create and activate a work record only when a concrete scoped work item is appropriate. Do not assume the bootstrap maintenance backlog is an application backlog."
        }}
    if inspector is None:
        from workflow_engine import inspect_work
        inspector = inspect_work
    try:
        report = inspector(root)
    except Exception as exc:
        # A hook failure must remain visible without inventing a successful
        # validation, changing permissions, or causing an automatic retry loop.
        return {"systemMessage": clipped(f"Workflow context could not be inspected ({type(exc).__name__}): {exc}. Run workflow.py status and resolve the record before claiming validation passed.", 1200)}
    if event in CONTEXT_EVENTS:
        return {"hookSpecificOutput": {"hookEventName": event, "additionalContext": context_text(report)}}
    errors = [item for item in report.get("issues", []) if item.get("severity") == "error"]
    if errors:
        labels = "; ".join(clipped(f"{item.get('code')}: {item.get('message')}", 300) for item in errors[:4])
        return {"systemMessage": clipped("Workflow validation reports unresolved errors: " + labels + ". These records do not support a completion claim. This reminder does not block an interview pause or authorize additional work.", 1600)}
    return {}


def main() -> int:
    raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
    try:
        if len(raw) > MAX_INPUT_BYTES:
            raise ValueError("event exceeds the input limit")
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            raise ValueError("event must be a JSON object")
        result = handle_event(payload)
    except (ValueError, UnicodeError, RecursionError) as exc:
        result = {"systemMessage": f"Workflow hook skipped invalid input: {clipped(exc, 200)}."}
    print(json.dumps(result, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
