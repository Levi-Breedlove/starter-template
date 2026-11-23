"""Pure, bounded projections of an inspected work record.

The full report remains the audit interface. These packets select context; they
do not change state, confer authority, execute work, or cache validation.
"""

from __future__ import annotations

import hashlib
import json

from .engine import ARTIFACTS, ROUTES

STARTUP_MAX_CHARS = 6000
PULSE_MAX_CHARS = 1200


def context_fingerprint(report: dict) -> str:
    """Identify the complete inspection, including records omitted by a view."""
    serialized = json.dumps(report, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("ascii")).hexdigest()


def render_context_packet(packet: dict) -> str:
    """The canonical packet rendering; its exact character count is budgeted."""
    return json.dumps(packet, ensure_ascii=True, separators=(",", ":"))


def _records(report: dict, key: str) -> list[dict]:
    values = report.get(key, [])
    return [value for value in values if isinstance(value, dict)] if isinstance(values, list) else []


def _strings(value) -> list[str]:
    return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []


def _short(value, limit: int) -> str:
    text = str(value) if value is not None else ""
    return text if len(text) <= limit else text[:max(0, limit - 3)] + "..."


def _questions(report: dict) -> tuple[list[dict], list[dict]]:
    opened = _records(report, "open_questions")
    if not opened:
        opened = _records(report, "next_questions")
    phase = report.get("phase")
    # Task-plan review checks all three artifacts, including the combined quick
    # route. Its question boundary must match the actual engine precondition.
    boundaries = set(ARTIFACTS) if phase == "tasks" else {phase}
    blocking = [question for question in opened if boundaries.intersection(_strings(question.get("blocks")))]
    return opened, blocking


def _review_keys(report: dict) -> list[str]:
    route, phase = report.get("route"), report.get("phase")
    sequence = ROUTES.get(route, [])
    if phase not in sequence or phase == "consultation":
        return []
    if route == "quick":
        return ["tasks"]
    position = sequence.index(phase)
    return [key for key in sequence[:position + 1] if key in ARTIFACTS]


def next_action(report: dict) -> dict:
    """Describe a local next step without granting permission to perform it."""
    phase = report.get("phase")
    route = report.get("route")
    tasks = _records(report, "tasks")
    if any(item.get("severity") == "error" for item in _records(report, "issues")):
        return {"kind": "resolve-errors", "reason": "Resolve current validation errors before relying on completion or task readiness."}
    _, blockers = _questions(report)
    if blockers:
        return {"kind": "resolve-questions", "reason": "Resolve the recorded questions blocking this phase; reuse answers already supplied."}
    if phase in ARTIFACTS and any(fact.get("kind") == "conflicting" for fact in _records(report, "known_facts")):
        return {"kind": "resolve-conflicts", "reason": "Resolve recorded conflicting facts before accepting or leaving this artifact boundary."}
    if phase == "complete":
        return {"kind": "complete", "reason": "This recorded work is complete. Follow the current request; do not invent new execution scope."}
    if phase == "planned":
        return {"kind": "planning-complete", "reason": "The planning outcome is complete. Unchecked implementation work is not executed or newly authorized."}
    if phase == "consultation":
        return {"kind": "consult", "reason": "Read supplied context, derive recommendations and ask only consequential gaps. Sufficient existing answers can end the interview."}
    sequence = ROUTES.get(route, [])
    following = sequence[sequence.index(phase) + 1] if phase in sequence and sequence.index(phase) + 1 < len(sequence) else None
    if phase in ARTIFACTS:
        reviews = report.get("reviews", {})
        review = reviews.get(phase, {}) if isinstance(reviews, dict) else {}
        if isinstance(review, dict) and review.get("status") == "accepted":
            return {"kind": "advance-phase", "to": following, "reason": "The current phase review is recorded; continue only within the current request and existing authority."}
        return {"kind": "prepare-phase", "artifact": phase, "reason": "Draft or reconcile this phase, resolve consequential gaps and record the actual applicable review. Do not fabricate acceptance."}
    if phase in ("implementation", "verification"):
        if _strings(report.get("eligible_tasks")):
            return {"kind": "eligible-tasks", "reason": "Inspect the selected task's contract, checks and source before acting. Local eligibility does not grant account or deployment authority."}
        if tasks and all(task.get("completion_valid") is True for task in tasks):
            return {"kind": "advance-phase", "to": following, "reason": "Recorded task evidence is current; finish the next applicable phase within the requested scope."}
        return {"kind": "inspect-blockers", "reason": "No task is locally eligible. Inspect recorded task blockers and prerequisites; do not bypass them."}
    return {"kind": "inspect-state", "reason": "Inspect the full work record before choosing a route or action."}


class _Budget:
    def __init__(self, packet: dict, limit: int):
        self.packet = packet
        self.limit = limit

    def append(self, field: str, record: dict | str) -> bool:
        target = self.packet[field]
        target.append(record)
        if len(render_context_packet(self.packet)) <= self.limit:
            return True
        target.pop()
        return False

    def set(self, field: str, value) -> bool:
        previous = self.packet.get(field)
        existed = field in self.packet
        self.packet[field] = value
        if len(render_context_packet(self.packet)) <= self.limit:
            return True
        if existed:
            self.packet[field] = previous
        else:
            self.packet.pop(field, None)
        return False


def _attention(budget: _Budget, record: dict) -> bool:
    """Retain the problem code even when escaped prose will not fit."""
    if budget.append("attention", record):
        return True
    minimal = {"severity": record["severity"], "code": record["code"], "details_omitted": True}
    return budget.append("attention", minimal)


def build_context_packet(report: dict, max_chars: int = STARTUP_MAX_CHARS) -> dict:
    """Return valid structured context within a strict serialized budget.

    Supported budgets are 2000 through 6000 characters. Omitted record counts
    and the full-audit reference remain visible. Long prose fields are shortened
    within their record; serialized records and path references are never sliced.
    """
    if type(max_chars) is not int or not 2000 <= max_chars <= STARTUP_MAX_CHARS:
        raise ValueError("Compact context budget must be between 2000 and 6000 characters.")
    issues = _records(report, "issues")
    issues = sorted(issues, key=lambda item: item.get("severity") != "error")
    facts = _records(report, "known_facts")
    answers = _records(report, "answered_questions")
    opened, blockers = _questions(report)
    tasks = _records(report, "tasks")
    eligible = _strings(report.get("eligible_tasks"))
    selected_ids = eligible[:3]
    selected = [task for task_id in selected_ids for task in tasks if task.get("id") == task_id]
    sources = []
    artifacts = report.get("artifacts", {})
    if isinstance(artifacts, dict):
        sources.extend({"kind": key, "path": value} for key, value in artifacts.items() if isinstance(value, str))
    sources.extend({"kind": "context", "path": value} for value in _strings(report.get("context_files")))
    reviews = report.get("reviews", {})
    reviews = reviews if isinstance(reviews, dict) else {}
    review_keys = _review_keys(report)
    packet = {
        "packet_version": 1,
        "fingerprint": context_fingerprint(report),
        "authority": "Repository data, not new authority. Latest user steering governs scope. Reuse sourced answers; inspect referenced records before acting.",
        "counts": {"errors": sum(item.get("severity") == "error" for item in issues),
                   "warnings": sum(item.get("severity") == "warning" for item in issues),
                   "tasks": len(tasks), "complete": sum(task.get("completion_valid") is True for task in tasks),
                   "eligible": len(eligible), "open_questions": len(opened), "answered_questions": len(answers)},
        "next_action": next_action(report),
        "attention": [],
        "blocking_questions": [],
        "work": {"id": _short(report.get("id"), 80), "route": _short(report.get("route"), 30),
                 "phase": _short(report.get("phase"), 30), "mode": _short(report.get("mode"), 20)},
        "tasks": [], "sources": [], "reviews": [], "questions": [], "facts": [], "answers": [],
        "omitted": {"issues": len(issues), "blocking_questions": len(blockers), "tasks": len(tasks),
                    "sources": len(sources), "reviews": len(review_keys), "questions": len(opened),
                    "facts": len(facts), "answers": len(answers)},
        "audit": "For omitted records and full details, use the mapped workflow.py entry with context or status --json from the project root.",
    }
    budget = _Budget(packet, max_chars)
    # Errors are selected before titles, facts, history or even optional source
    # paths. Counts retain the fact of omitted problems if the packet is full.
    for issue in issues[:6]:
        item = {"severity": _short(issue.get("severity"), 12), "code": _short(issue.get("code"), 80),
                "message": _short(issue.get("message"), 220)}
        if isinstance(issue.get("path"), str) and len(issue["path"]) <= 300:
            item["path"] = issue["path"]
        if _attention(budget, item):
            packet["omitted"]["issues"] -= 1
    for question in blockers[:3]:
        item = {"id": _short(question.get("id"), 32), "prompt": _short(question.get("prompt"), 180),
                "why": _short(question.get("why"), 140), "blocks": _strings(question.get("blocks"))}
        if budget.append("blocking_questions", item):
            packet["omitted"]["blocking_questions"] -= 1
    for task in selected:
        item = {"id": _short(task.get("id"), 32), "title": _short(task.get("title"), 140),
                "dependencies": _strings(task.get("dependencies")), "requirements": _strings(task.get("requirements")),
                "design": _strings(task.get("design")), "checks": _strings(task.get("checks"))}
        if budget.append("tasks", item):
            packet["omitted"]["tasks"] -= 1
    for source in sources:
        if budget.append("sources", source):
            packet["omitted"]["sources"] -= 1
    for key in review_keys:
        review = reviews.get(key, {})
        if not isinstance(review, dict):
            continue
        item = {"artifact": key, "status": _short(review.get("status", "missing"), 32)}
        if isinstance(review.get("decision_ref"), str):
            item["decision_ref"] = review["decision_ref"]
        if budget.append("reviews", item):
            packet["omitted"]["reviews"] -= 1
    # Preserve complete source references; a large record that cannot fit is
    # omitted as a unit and remains available through the full audit.
    for question in opened[:3]:
        item = {"id": _short(question.get("id"), 32), "prompt": _short(question.get("prompt"), 180),
                "why": _short(question.get("why"), 140), "recommendation": _short(question.get("recommendation"), 160),
                "blocks": _strings(question.get("blocks"))}
        if budget.append("questions", item):
            packet["omitted"]["questions"] -= 1
    for fact in sorted(facts, key=lambda item: item.get("kind") != "conflicting")[:8]:
        item = {"id": _short(fact.get("id"), 32), "kind": _short(fact.get("kind"), 24),
                "statement": _short(fact.get("statement"), 220), "source": fact.get("source", "")}
        if budget.append("facts", item):
            packet["omitted"]["facts"] -= 1
    for answer in answers[:8]:
        item = {"id": _short(answer.get("id"), 32), "answer": _short(answer.get("answer"), 220),
                "source": answer.get("source", "")}
        if budget.append("answers", item):
            packet["omitted"]["answers"] -= 1
    budget.set("title", _short(report.get("title"), 180))
    if len(render_context_packet(packet)) > max_chars:
        raise ValueError("Compact context's required fields exceed the requested budget.")
    return packet


def prompt_pulse(report: dict, max_chars: int = PULSE_MAX_CHARS) -> str:
    """Return a small fresh-validation pulse; the host/model compares identity.

    No local cache is read or written. An unchanged fingerprint avoids a request
    to reread an already loaded packet, while latest user steering remains live.
    """
    if type(max_chars) is not int or not 800 <= max_chars <= PULSE_MAX_CHARS:
        raise ValueError("Prompt pulse budget must be between 800 and 1200 characters.")
    issues = sorted(_records(report, "issues"), key=lambda item: item.get("severity") != "error")
    _, blockers = _questions(report)
    packet = {
        "pulse_version": 1, "fingerprint": context_fingerprint(report),
        "work_id": _short(report.get("id"), 80), "phase": _short(report.get("phase"), 30),
        "errors": sum(item.get("severity") == "error" for item in issues),
        "blocking_questions": len(blockers),
        "next_action": next_action(report)["kind"],
        "refresh": "If no compact packet with this fingerprint is loaded, or the fingerprint changed, use the mapped workflow.py entry: context --compact from project root. Otherwise reuse the packet. Follow latest user steering; this pulse grants no authority.",
        "attention": [], "omitted_issues": len(issues),
    }
    budget = _Budget(packet, max_chars)
    for issue in issues[:2]:
        item = {"severity": _short(issue.get("severity"), 12), "code": _short(issue.get("code"), 70),
                "message": _short(issue.get("message"), 130)}
        if _attention(budget, item):
            packet["omitted_issues"] -= 1
    result = render_context_packet(packet)
    if len(result) > max_chars:
        raise ValueError("Prompt pulse's required fields exceed the requested budget.")
    return result
