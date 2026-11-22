"""Small, offline workflow ledger. Markdown owns task completion.

This module never executes commands, calls a model, or contacts a service.
Recorded decisions/results are assertions by their author, not authenticated
approvals or independently executed tests.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

SCHEMA_VERSION = 1
WORK_ID = re.compile(r"[a-z0-9][a-z0-9-]{0,79}\Z")
REF_ID = re.compile(r"\b(?:REQ|DEF|FIX|KEEP|DES|T|CHK)-[0-9]{3,}\b")
CONTRACT_ID = re.compile(r"(?:REQ|DEF|FIX|KEEP)-[0-9]{3,}\Z")
ROUTES = {
    "requirements-first": ["consultation", "requirements", "design", "tasks", "implementation", "verification", "complete"],
    "design-first": ["consultation", "design", "requirements", "tasks", "implementation", "verification", "complete"],
    "quick": ["consultation", "tasks", "implementation", "verification", "complete"],
    "bugfix": ["consultation", "requirements", "design", "tasks", "implementation", "verification", "complete"],
    "plan": ["consultation", "requirements", "design", "tasks", "planned"],
}
ARTIFACTS = ("requirements", "design", "tasks")
CONTEXT_DEFAULTS = {
    "brief": "project/brief.md",
    "handoff": "delivery/current-handoff.md",
    "adoption_report": "project/adoption-report.md",
    "environment_capabilities": "delivery/environment-capabilities.md",
}
FACT_KINDS = {"supplied", "observed", "derived", "assumption", "proposed", "conflicting"}
PHASES = set().union(*map(set, ROUTES.values()))
HASH = re.compile(r"[0-9a-f]{64}\Z")
PLACEHOLDER = re.compile(r"<[^>\n]+>|\b(?:TBD|TODO)\b")

CONSULTANT_INSTRUCTIONS = [
    "Read the project's existing instructions, context files, canonical contract, design, and tasks before proposing changes.",
    "Extract supplied facts and accepted decisions first; keep each source. Reuse answered questions. Do not invent missing answers or reopen an unchanged accepted decision.",
    "Distinguish supplied/observed facts, derived implications, assumptions, proposals, and conflicting evidence. Resolve conflicts explicitly.",
    "Ask at most three consequential unanswered questions at a time. Explain why each matters and recommend an option when evidence supports it. If sufficient information is supplied, draft or advance without an interview ritual.",
    "Research technical uncertainties using current official documentation. Ask the user about business intent, constraints, tradeoffs, and authority rather than outsourcing routine technical research to them.",
    "For brownfield work, discover the accepted baseline, ownership, interfaces, data, and preservation requirements before proposing replacement or migration.",
    "Record actual prior authorization or delegation once and bind reviews to the reviewed artifacts. A local review record cannot grant authority. Quick uses a combined review; it does not invent consent.",
    "Keep tasks.md as the sole task completion authority. Reconcile changed contracts, task links, and affected evidence; report blocked or unverified work accurately.",
    "Use existing official AWS plugins when relevant and available. This offline tool neither connects to AWS nor authorizes account actions or deployment.",
]


class WorkflowError(ValueError):
    """An unsafe path, unusable selection, or rejected state mutation."""


def digest_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def digest_file(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def digest_value(value) -> str:
    return digest_bytes(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def _plan_digest(path: Path) -> str:
    """Hash the plan while excluding its explicitly mutable progress fields."""
    lines = []
    for line in _clean_markdown(path.read_text(encoding="utf-8")).splitlines():
        if re.match(r"^\s*-\s+(?:Activity:|Evidence(?:\s*/\s*review)?:|Blocker(?: and resolver, if any)?:)", line, re.I):
            continue
        line = re.sub(r"^(\s*-\s+)\[[ xX]\](\s+T-[0-9]{3,}\s+complete\.?)\s*$", r"\1[ ]\2", line)
        if re.match(r"^\s*\|\s*CHK-", line):
            line = "|".join(part.strip() for part in line.strip().strip("|").split("|")[:4])
        lines.append(line.rstrip())
    return digest_bytes("\n".join(lines).encode())


def _next_id(records: list[dict], prefix: str) -> str:
    numbers = [int(record["id"].split("-")[1]) for record in records
               if isinstance(record.get("id"), str) and re.fullmatch(prefix + r"-[0-9]{3,}", record["id"])]
    return f"{prefix}-{max(numbers, default=0) + 1:03d}"


def safe_path(root: Path, relative: str) -> Path:
    """Resolve a portable relative path without symlink or Git redirection."""
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise WorkflowError("Paths must be nonempty POSIX paths relative to the selected root.")
    pure = PurePosixPath(relative)
    if pure.is_absolute() or any(part in {"..", "."} for part in relative.split("/")):
        raise WorkflowError(f"Unsafe relative path: {relative!r}")
    if any(part.casefold() == ".git" for part in root.resolve().parts + pure.parts):
        raise WorkflowError("Workflow paths cannot read or write Git metadata.")
    cursor = root
    for part in pure.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise WorkflowError(f"Workflow paths cannot follow symlink components: {relative!r}")
    candidate = root.joinpath(*pure.parts).resolve()
    if not candidate.is_relative_to(root.resolve()) or candidate == root.resolve():
        raise WorkflowError(f"Path escapes its selected root: {relative!r}")
    return candidate


def _read_json(path: Path):
    try:
        if not path.is_file():
            raise WorkflowError(f"Metadata must be a regular file: {path.name}")
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise WorkflowError(f"Cannot read {path.name}: {exc}") from exc


def _select(root: Path, work_id: str | None) -> tuple[Path, str, dict]:
    root = root.resolve()
    if not root.is_dir():
        raise WorkflowError("The selected project root must be an existing directory.")
    if work_id is None:
        pointer = _read_json(safe_path(root, ".codex/workflow.json"))
        if not isinstance(pointer, dict) or type(pointer.get("schema_version")) is not int or pointer.get("schema_version") != SCHEMA_VERSION:
            raise WorkflowError("The active work pointer must use schema_version 1.")
        active = pointer.get("active_work", "")
        if not isinstance(active, str) or not re.fullmatch(r"specs/[a-z0-9][a-z0-9-]{0,79}", active):
            raise WorkflowError("active_work must be a project-relative specs/<work-id> path.")
        work_id = active.removeprefix("specs/")
    if not isinstance(work_id, str) or not WORK_ID.fullmatch(work_id):
        raise WorkflowError("Work IDs use lowercase letters, digits, and hyphens, up to 80 characters.")
    work = safe_path(root, f"specs/{work_id}")
    data = _read_json(safe_path(work, "work.json"))
    if not isinstance(data, dict):
        raise WorkflowError("work.json must contain an object.")
    return work, work_id, data


def atomic_json(path: Path, value) -> None:
    """Replace one JSON document atomically; never truncate a live document."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, prefix=".workflow-", delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(value, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _clean_markdown(content: str) -> str:
    """Ignore fenced examples; this is intentionally a documented subset."""
    lines, fence = [], None
    for line in content.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            token = match.group(1)
            if fence is None:
                fence = token[0]
            elif token[0] == fence:
                fence = None
            lines.append("")
        else:
            lines.append(line if fence is None else "")
    return "\n".join(lines)


def _ids(text: str, prefixes: tuple[str, ...]) -> list[str]:
    return list(dict.fromkeys(item for item in REF_ID.findall(text) if item.split("-")[0] in prefixes))


def _definitions(content: str, prefixes: tuple[str, ...], issue, path: str) -> dict[str, bool]:
    definitions = {}
    status_column = None
    for line in _clean_markdown(content).splitlines():
        cells = [part.strip() for part in line.strip().strip("|").split("|")] if line.lstrip().startswith("|") else []
        if cells and not re.fullmatch(r"[A-Z]+-[^\s|]+", cells[0]) and not all(re.fullmatch(r":?-+:?", cell.replace(" ", "")) for cell in cells):
            status_column = next((index for index, cell in enumerate(cells) if re.fullmatch(r"required\s*(?:or|/)\s*deferred", cell, re.I)), None)
        elif not cells and line.strip():
            status_column = None
        match = re.match(r"^\s*(?:#{1,6}\s+|\|\s*)([A-Z]+-[^\s|]+)", line)
        if not match or match.group(1).split("-")[0] not in prefixes:
            continue
        key = match.group(1)
        if not re.fullmatch(r"(?:" + "|".join(prefixes) + r")-[0-9]{3,}", key):
            issue("error", "invalid-id", f"Invalid definition ID {key!r}.", path)
        elif key in definitions:
            issue("error", "duplicate-id", f"Duplicate definition {key}.", path)
        else:
            explicitly_deferred = bool(cells and status_column is not None and status_column < len(cells) and cells[status_column].casefold() == "deferred")
            definitions[key] = not explicitly_deferred
    return definitions


def _field(block: str, names: tuple[str, ...]) -> str | None:
    pattern = r"^\s*-\s+(?:" + "|".join(re.escape(name) for name in names) + r"):\s*(.*?)\s*$"
    match = re.search(pattern, block, re.M | re.I)
    return match.group(1) if match else None


def _parse_tasks(content: str, issue, path: str) -> tuple[dict, dict]:
    content = _clean_markdown(content)
    headings = list(re.finditer(r"^#{2,4}\s+(T-[^\s]+)(?:\s+[—–-]\s*|\s+)(.*?)\s*$", content, re.M))
    tasks, checks = {}, {}
    for index, heading in enumerate(headings):
        task_id, title = heading.group(1), heading.group(2)
        if not re.fullmatch(r"T-[0-9]{3,}", task_id):
            issue("error", "invalid-id", f"Invalid task ID {task_id!r}.", path)
            continue
        if task_id in tasks:
            issue("error", "duplicate-id", f"Duplicate task {task_id}.", path)
            continue
        block = content[heading.end(): headings[index + 1].start() if index + 1 < len(headings) else len(content)]
        # Later section headings (matrix, evidence, etc.) are not part of a task.
        boundary = re.search(r"^#{1,3}\s+(?!T-)", block, re.M)
        if boundary:
            block = block[:boundary.start()]
        boxes = re.findall(r"^\s*-\s+\[([ xX])\]\s+(T-[^\s]+)\s+complete\.?\s*$", block, re.M)
        if len(boxes) != 1 or boxes[0][1] != task_id:
            issue("error", "task-checkbox", f"{task_id} requires exactly one matching '- [ ] {task_id} complete' checkbox.", path)
        checked = len(boxes) == 1 and boxes[0][1] == task_id and boxes[0][0].lower() == "x"
        contract = _field(block, ("Contract / design", "Requirements/design", "Contract", "Requirements"))
        dependency = _field(block, ("Prerequisites", "Dependencies", "Depends on"))
        verification = _field(block, ("Verification", "Checks"))
        for name, value in (("Contract / design", contract), ("Prerequisites", dependency), ("Verification", verification)):
            if value is None:
                issue("error", "missing-task-field", f"{task_id} needs an explicit '{name}:' field.", path)
        dependencies = _ids(dependency or "", ("T",))
        if dependency is not None and not dependencies and dependency.strip().lower().rstrip(".") != "none":
            issue("error", "unresolved-prerequisite", f"{task_id} prerequisites must name T IDs or 'none'; record external blockers explicitly.", path)
        activity = _field(block, ("Activity",)) or ""
        if (activity.lower().rstrip(".") == "complete") != checked and activity.lower().rstrip(".") == "complete":
            issue("error", "false-completion", f"{task_id} says complete but its canonical checkbox is unchecked.", path)
        if checked and activity and activity.lower().rstrip(".") != "complete":
            issue("error", "false-completion", f"{task_id} is checked but Activity is {activity!r}.", path)
        blocker = _field(block, ("Blocker", "Blocker and resolver, if any")) or ""
        if blocker.lower().rstrip(".") in {"none", "not applicable", "n/a"}:
            blocker = ""
        if activity.lower().startswith("blocked") and not blocker:
            blocker = activity
        stable = [line.strip() for line in block.splitlines() if line.strip()
                  and not re.match(r"^\s*-\s+(?:\[[ xX]\]\s+T-[0-9]{3,}\s+complete\.?\s*$|Activity:|Evidence(?:\s*/\s*review)?:|Blocker(?: and resolver, if any)?:)", line, re.I)]
        tasks[task_id] = {"id": task_id, "title": title, "checked": checked,
                          "dependencies": dependencies,
                          "requirements": _ids(contract or "", ("REQ", "DEF", "FIX", "KEEP")),
                          "design": _ids(contract or "", ("DES",)),
                          "checks": _ids(verification or "", ("CHK",)),
                          "blocked_reason": blocker, "signature": digest_value([title, stable]),
                          "completion_valid": False}
    all_boxes = re.findall(r"^\s*-\s+\[[ xX]\]\s+(T-[^\s]+)\s+complete\.?\s*$", content, re.M)
    for box_id in set(all_boxes):
        if box_id not in tasks or all_boxes.count(box_id) != 1:
            issue("error", "task-checkbox", f"{box_id} has an orphan or duplicate task checkbox.", path)
    for line in content.splitlines():
        if not re.match(r"^\s*\|\s*CHK-", line):
            continue
        cells = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            issue("error", "check-row", "A check row needs ID, requirements, tasks, and method columns.", path)
            continue
        check_id = cells[0]
        if not re.fullmatch(r"CHK-[0-9]{3,}", check_id):
            issue("error", "invalid-id", f"Invalid check ID {check_id!r}.", path)
        elif check_id in checks:
            issue("error", "duplicate-id", f"Duplicate check {check_id}.", path)
        else:
            checks[check_id] = {"id": check_id, "requirements": _ids(cells[1], ("REQ", "DEF", "FIX", "KEEP")),
                                "tasks": _ids(cells[2], ("T",)), "method": cells[3]}
    return tasks, checks


def _snapshot_paths(route: str, artifact: str, artifacts: dict) -> list[str]:
    if artifact == "tasks":
        return [artifacts[key] for key in ARTIFACTS if key in artifacts]
    if artifact == "design" and route != "design-first":
        return [artifacts[key] for key in ("requirements", "design") if key in artifacts]
    if artifact == "requirements" and route == "design-first":
        return [artifacts[key] for key in ("design", "requirements") if key in artifacts]
    return [artifacts[artifact]] if artifact in artifacts else []


def _timestamp_valid(value) -> bool:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.tzinfo is not None
    except (ValueError, TypeError, AttributeError):
        return False


def _inspect(root: Path, work: Path, work_id: str, data: dict) -> dict:
    issues = []

    def issue(severity, code, message, path=None):
        entry = {"severity": severity, "code": code, "message": message}
        if path:
            entry["path"] = path
        if entry not in issues:
            issues.append(entry)

    def string(value):
        return isinstance(value, str) and bool(value.strip())

    def records(key):
        value = data.get(key)
        if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
            issue("error", "schema", f"{key} must be an array of objects.")
            return []
        return value

    if type(data.get("schema_version")) is not int or data.get("schema_version") != SCHEMA_VERSION:
        issue("error", "schema", "work.json must use integer schema_version 1.")
    if data.get("id") != work_id:
        issue("error", "schema", "work.json id must match its selected directory.")
    if not string(data.get("title")):
        issue("error", "schema", "A nonempty title is required.")
    mode, route, phase = data.get("mode"), data.get("route"), data.get("phase")
    if mode not in ("greenfield", "brownfield"):
        issue("error", "schema", "mode must be greenfield or brownfield.")
    if not isinstance(route, str) or route not in ROUTES:
        issue("error", "schema", "Unknown route.")
        route = "requirements-first"
    if not isinstance(phase, str) or phase not in ROUTES[route]:
        issue("error", "schema", "phase must belong to the selected route.")
        phase = "consultation"
    sequence = ROUTES[route]
    phase_index = sequence.index(phase)
    coverage_severity = "error" if phase_index > sequence.index("tasks") else "warning"
    artifacts, contents = {}, {}
    raw_artifacts = data.get("artifacts")
    if not isinstance(raw_artifacts, dict):
        raw_artifacts = {}
    for key in ARTIFACTS:
        try:
            path = safe_path(work, raw_artifacts.get(key))
            relative = path.relative_to(root).as_posix()
            if relative in artifacts.values():
                issue("error", "schema", "Canonical artifact paths must be distinct.")
            artifacts[key] = relative
            if path.is_file():
                contents[key] = path.read_text(encoding="utf-8")
        except (WorkflowError, OSError, UnicodeError) as exc:
            issue("error", "artifact-path", f"{key}: {exc}")
    context_files = data.get("context_files")
    if not isinstance(context_files, list) or any(not isinstance(value, str) for value in context_files):
        issue("error", "schema", "context_files must be an array of project-relative file paths.")
        context_files = []
    for relative in context_files:
        try:
            if not safe_path(root, relative).is_file():
                issue("warning", "missing-context", "Context file is not present; do not invent its contents.", relative)
        except WorkflowError as exc:
            issue("error", "context-path", str(exc))

    facts, questions = records("facts"), records("questions")
    seen_ids = set()
    for kind, entries, prefix in (("fact", facts, "F"), ("question", questions, "Q")):
        for entry in entries:
            entry_id = entry.get("id")
            if not isinstance(entry_id, str) or not re.fullmatch(prefix + r"-[0-9]{3,}", entry_id):
                issue("error", "invalid-id", f"Invalid {kind} ID.")
            elif entry_id in seen_ids:
                issue("error", "duplicate-id", f"Duplicate {entry_id}.")
            else:
                seen_ids.add(entry_id)
            if kind == "fact":
                if not isinstance(entry.get("kind"), str) or entry.get("kind") not in FACT_KINDS or not string(entry.get("statement")) or not string(entry.get("source")):
                    issue("error", "schema", f"{entry_id}: facts need kind, statement, and source.")
                if entry.get("kind") == "conflicting":
                    issue("warning", "unresolved-conflict", f"{entry_id}: conflicting evidence needs an explicit resolution.")
            else:
                if not string(entry.get("prompt")) or not string(entry.get("why")) or not isinstance(entry.get("recommendation", ""), str):
                    issue("error", "schema", f"{entry_id}: questions need prompt, why, and an optional recommendation.")
                if entry.get("status") not in ("open", "answered", "deferred"):
                    issue("error", "schema", f"{entry_id}: unknown question status.")
                blocks = entry.get("blocks")
                if not isinstance(blocks, list) or any(not isinstance(value, str) or value not in ARTIFACTS + ("implementation", "verification") for value in blocks):
                    issue("error", "schema", f"{entry_id}: blocks must name workflow boundaries.")
                if entry.get("status") == "answered" and (not string(entry.get("answer")) or not string(entry.get("source"))):
                    issue("error", "missing-answer-source", f"{entry_id}: an answered question needs its actual answer and source.")
                if entry.get("status") == "open" and entry.get("answer"):
                    issue("error", "question-conflict", f"{entry_id}: an open question also has an answer; reconcile the record.")
                if entry.get("status") == "deferred" and blocks:
                    issue("error", "question-conflict", f"{entry_id}: a deferred question cannot remain a blocking prerequisite.")

    contract = _definitions(contents.get("requirements", ""), ("REQ", "DEF", "FIX", "KEEP"), issue, artifacts.get("requirements", ""))
    designs = _definitions(contents.get("design", ""), ("DES",), issue, artifacts.get("design", ""))
    tasks, checks = _parse_tasks(contents.get("tasks", ""), issue, artifacts.get("tasks", ""))
    for task in tasks.values():
        for key, existing in (("dependencies", tasks), ("requirements", contract), ("design", designs), ("checks", checks)):
            for target in task[key]:
                if target not in existing:
                    issue("error", "dangling-reference", f"{task['id']} references unknown {target}.", artifacts.get("tasks"))
        if not task["requirements"] or not task["checks"]:
            issue(coverage_severity, "missing-coverage", f"{task['id']} needs explicit contract and check links.", artifacts.get("tasks"))
    visiting, visited = set(), set()

    def visit(task_id):
        if task_id in visiting:
            issue("error", "dependency-cycle", f"Dependency cycle includes {task_id}.", artifacts.get("tasks"))
            return
        if task_id in visited or task_id not in tasks:
            return
        visiting.add(task_id)
        for other in tasks[task_id]["dependencies"]:
            visit(other)
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in tasks:
        visit(task_id)
    for check in checks.values():
        if not check["requirements"] or not check["tasks"] or not check["method"]:
            issue(coverage_severity, "missing-coverage", f"{check['id']} needs explicit requirement, task, and method fields.", artifacts.get("tasks"))
        for target in check["requirements"] + check["tasks"]:
            if target not in contract and target not in tasks:
                issue("error", "dangling-reference", f"{check['id']} references unknown {target}.", artifacts.get("tasks"))
        linked_requirements = set()
        for task_id in check["tasks"]:
            if task_id in tasks:
                linked_requirements.update(tasks[task_id]["requirements"])
                if check["id"] not in tasks[task_id]["checks"]:
                    issue("error", "inconsistent-check-link", f"{check['id']} names {task_id}, but that task does not name the check.", artifacts.get("tasks"))
        if set(check["requirements"]) - linked_requirements:
            issue("error", "inconsistent-check-link", f"{check['id']} covers requirements absent from its linked tasks.", artifacts.get("tasks"))
        check["signature"] = digest_value([check, {task_id: tasks[task_id]["signature"] for task_id in check["tasks"] if task_id in tasks}])
    for task in tasks.values():
        for check_id in task["checks"]:
            if check_id in checks and task["id"] not in checks[check_id]["tasks"]:
                issue("error", "inconsistent-check-link", f"{task['id']} names {check_id}, but the check does not name the task.", artifacts.get("tasks"))
    covered = {requirement for check in checks.values() for requirement in check["requirements"]}
    required = {key for key, required in contract.items() if required and not key.startswith("DEF-")}
    if "tasks" in contents:
        for missing in sorted(required - covered):
            issue(coverage_severity, "missing-coverage", f"{missing} has no verification check.", artifacts.get("tasks"))

    def hashes_current(values, plan=False):
        if not isinstance(values, dict) or not values:
            return False
        current = True
        for relative, expected in values.items():
            try:
                path = safe_path(root, relative)
                if not isinstance(expected, str) or not HASH.fullmatch(expected) or not path.is_file():
                    current = False
                elif (_plan_digest(path) if plan and relative == artifacts.get("tasks") else digest_file(path)) != expected:
                    current = False
            except (WorkflowError, OSError, UnicodeError):
                current = False
        return current

    review_records = records("reviews")
    reviews = {key: {"status": "missing"} for key in ARTIFACTS}
    for record in review_records:
        artifact = record.get("artifact")
        if artifact not in ARTIFACTS:
            issue("error", "invalid-review", "Review artifact must be requirements, design, or tasks.")
            continue
        record_id = record.get("id")
        if not isinstance(record_id, str) or not re.fullmatch(r"REV-[0-9]{3,}", record_id) or not all(string(record.get(key)) for key in ("reviewer", "decision_ref")) or record.get("authority") not in ("user", "delegated") or record.get("outcome") not in ("accepted", "changes-requested") or not _timestamp_valid(record.get("recorded_at")) or record.get("snapshot_policy") != "canonical-plan-v1":
            issue("error", "invalid-review", f"Incomplete review provenance for {artifact}.")
        if isinstance(record_id, str) and record_id in seen_ids:
            issue("error", "duplicate-id", f"Duplicate review ID {record.get('id')}.")
        elif isinstance(record.get("id"), str):
            seen_ids.add(record["id"])
        hashes = record.get("hashes")
        expected = set(_snapshot_paths(route, artifact, artifacts))
        paired = (artifact == "design" and route != "design-first") or (artifact == "requirements" and route == "design-first")
        shape_valid = isinstance(hashes, dict) and set(hashes) == expected and len(expected) == (3 if artifact == "tasks" else 2 if paired else 1)
        if not shape_valid:
            issue("error", "invalid-review", f"{artifact} review lacks its complete artifact snapshot.")
        current = shape_valid and hashes_current(hashes, plan=True)
        reviews[artifact] = {"status": record.get("outcome") if current else "stale", "id": record.get("id"), "reviewer": record.get("reviewer"), "authority": record.get("authority"), "decision_ref": record.get("decision_ref")}

    needed_reviews = []
    if route == "quick":
        if phase_index > sequence.index("tasks"):
            needed_reviews = ["tasks"]
    else:
        needed_reviews = [key for key in ARTIFACTS if phase_index > sequence.index(key)]
    for artifact, review in reviews.items():
        if review["status"] == "stale":
            issue("error" if artifact in needed_reviews else "warning", "stale-review", f"The {artifact} review no longer identifies the current artifact snapshot.", artifacts.get(artifact))
        elif artifact in needed_reviews and review["status"] != "accepted":
            issue("error", "missing-review", f"The current {phase} phase needs a current accepted {artifact} review referencing real authority.", artifacts.get(artifact))
    needed_artifacts = list(ARTIFACTS) if "tasks" in needed_reviews else needed_reviews
    for artifact in needed_artifacts:
        if artifact in contents and PLACEHOLDER.search(_clean_markdown(contents[artifact])):
            issue("error", "unfinished-artifact", f"The completed {artifact} boundary still contains draft placeholders.", artifacts.get(artifact))
    if "requirements" in needed_artifacts and not required:
        issue("error", "missing-contract", "The reviewed contract has no required behavioral IDs.", artifacts.get("requirements"))
    if "design" in needed_artifacts and not designs:
        issue("error", "missing-design", "The reviewed design has no DES IDs.", artifacts.get("design"))
    if "tasks" in needed_artifacts and not tasks:
        issue("error", "missing-tasks", "The reviewed task plan contains no canonical tasks.", artifacts.get("tasks"))
    for question in questions:
        if question.get("status") != "open" or not isinstance(question.get("blocks"), list):
            continue
        for boundary in question["blocks"]:
            if boundary in needed_reviews or (phase in ("verification", "complete") and boundary == "implementation") or (phase == "complete" and boundary == "verification"):
                issue("error", "unresolved-question", f"{question.get('id')} still blocks the completed {boundary} boundary.")

    evidence_records, evidence = records("evidence"), {}
    for record in evidence_records:
        check_id = record.get("check")
        record_id = record.get("id")
        valid = isinstance(record_id, str) and bool(re.fullmatch(r"EV-[0-9]{3,}", record_id))
        duplicate = isinstance(record_id, str) and record_id in seen_ids
        if not valid or duplicate:
            issue("error", "duplicate-id" if duplicate else "invalid-id", "Invalid or duplicate evidence ID.")
            valid = False
        if isinstance(record_id, str):
            seen_ids.add(record_id)
        if not isinstance(check_id, str) or check_id not in checks:
            issue("error", "dangling-reference", f"Evidence references unknown check {check_id!r}.")
            continue
        if record.get("result") not in ("pass", "fail", "not-run") or not all(string(record.get(key)) and not PLACEHOLDER.search(record[key]) for key in ("record", "method", "environment", "candidate")) or not all(_timestamp_valid(record.get(key)) for key in ("observed_at", "recorded_at")):
            issue("error", "invalid-evidence", f"{record_id} lacks actual result provenance.")
            valid = False
        inputs = record.get("inputs")
        if not isinstance(inputs, dict) or not isinstance(record.get("record"), str) or record.get("record") not in inputs or len(inputs) < 2:
            issue("error", "invalid-evidence", f"{record_id} must identify its receipt and at least one tested input.")
            valid = False
        expected_artifacts = {artifacts[key] for key in ("requirements", "design") if key in artifacts}
        artifact_hashes = record.get("artifacts")
        if not isinstance(artifact_hashes, dict) or set(artifact_hashes) != expected_artifacts or len(expected_artifacts) != 2:
            issue("error", "invalid-evidence", f"{record_id} lacks the current contract and design identity.")
            valid = False
        current = valid and hashes_current(inputs) and hashes_current(artifact_hashes) and record.get("check_signature") == checks[check_id]["signature"]
        evidence[check_id] = {"id": record_id, "result": record.get("result"), "current": current, "record": record.get("record")}
    for check_id, result in evidence.items():
        if not result["current"]:
            issue("warning", "stale-evidence", f"{result['id']} no longer identifies all current inputs, artifacts, and check definition.", result.get("record"))

    resolving = set()

    def completion(task_id):
        task = tasks[task_id]
        if task_id in resolving:
            return False
        resolving.add(task_id)
        result = task["checked"] and bool(task["checks"]) and bool(task["requirements"]) and not task["blocked_reason"]
        result = result and all(check_id in evidence and evidence[check_id]["current"] and evidence[check_id]["result"] == "pass" for check_id in task["checks"])
        result = result and all(other in tasks and completion(other) for other in task["dependencies"])
        resolving.remove(task_id)
        task["completion_valid"] = bool(result)
        return bool(result)

    for task_id, task in tasks.items():
        if task["checked"] and not completion(task_id):
            issue("error", "false-completion", f"{task_id} is checked without current passing evidence, valid completed prerequisites, or a resolved blocker.", artifacts.get("tasks"))
    if phase == "complete" and (not tasks or not all(task["completion_valid"] for task in tasks.values())):
        issue("error", "false-completion", "Complete requires every canonical task to be validly complete.", artifacts.get("tasks"))
    for key in needed_artifacts:
        if key not in contents:
            issue("error", "missing-artifact", f"A completed boundary is missing {key}.", artifacts.get(key))
    next_questions = [question for question in questions if question.get("status") == "open"]
    next_questions.sort(key=lambda question: (phase not in question.get("blocks", []) if isinstance(question.get("blocks"), list) else True, str(question.get("id", ""))))
    dependency_ready = [task_id for task_id, task in tasks.items() if not task["checked"] and not task["blocked_reason"] and all(other in tasks and tasks[other]["completion_valid"] for other in task["dependencies"])]
    no_errors = not any(item["severity"] == "error" for item in issues)
    current_blocked = any(phase in question.get("blocks", []) for question in next_questions if isinstance(question.get("blocks"), list))
    eligible = dependency_ready if phase in ("implementation", "verification") and no_errors and not current_blocked else []
    return {"schema_version": SCHEMA_VERSION, "id": work_id, "title": data.get("title"), "mode": mode, "route": route, "phase": phase,
            "artifacts": artifacts, "context_files": context_files, "known_facts": facts,
            "answered_questions": [question for question in questions if question.get("status") == "answered"],
            "open_questions": next_questions, "next_questions": next_questions[:3],
            "deferred_questions": [question for question in questions if question.get("status") == "deferred"],
            "reviews": reviews, "tasks": list(tasks.values()), "checks": list(checks.values()), "evidence": evidence,
            "dependency_ready_tasks": dependency_ready, "eligible_tasks": eligible, "issues": issues,
            "consultant_instructions": CONSULTANT_INSTRUCTIONS}


def inspect_work(root: str | Path, work_id: str | None = None) -> dict:
    """Read-only inspection; unfinished consultation is a valid state."""
    root = Path(root).resolve()
    work, selected_id, data = _select(root, work_id)
    return _inspect(root, work, selected_id, data)


def _load_mutable(root, work_id):
    root = Path(root).resolve()
    work, selected_id, data = _select(root, work_id)
    return root, work, selected_id, data


def _initial_context(root: Path) -> list[str]:
    """Retain actual adopted context paths without interpreting their content."""
    manifest_relative = ".aws-workflow/manifest.json"
    manifest_path = safe_path(root, manifest_relative)
    if not manifest_path.exists():
        return [relative for relative in CONTEXT_DEFAULTS.values() if safe_path(root, relative).is_file()]
    manifest = _read_json(manifest_path)
    if not isinstance(manifest, dict) or type(manifest.get("schema_version")) is not int or manifest.get("schema_version") != 1 or manifest.get("identity") != "codex-aws-workflow" or not isinstance(manifest.get("paths"), dict):
        raise WorkflowError("The adoption manifest must identify the codex-aws-workflow schema-1 path map.")
    context = [manifest_relative]
    for key in CONTEXT_DEFAULTS:
        relative = manifest["paths"].get(key)
        if not isinstance(relative, str):
            raise WorkflowError(f"The adoption manifest needs a project-relative {key} path.")
        if not safe_path(root, relative).is_file():
            raise WorkflowError(f"The mapped {key} is missing or not a regular file: {relative}")
        if relative not in context:
            context.append(relative)
    return context


def _assert_clean(report, ignore=()):
    problems = [item["message"] for item in report["issues"] if item["severity"] == "error" and item["code"] not in ignore]
    if problems:
        raise WorkflowError("Resolve invalid state first: " + "; ".join(problems))


def _assert_artifact_ready(root, report, artifact):
    required = ARTIFACTS if artifact == "tasks" else (artifact,)
    for key in required:
        relative = report["artifacts"].get(key)
        if not relative or not safe_path(root, relative).is_file():
            raise WorkflowError(f"Create the canonical {key} artifact before reviewing its boundary.")
        content = safe_path(root, relative).read_text(encoding="utf-8")
        if not content.strip() or PLACEHOLDER.search(_clean_markdown(content)):
            raise WorkflowError(f"Resolve draft placeholders in {key} before recording acceptance.")
    if artifact == "requirements":
        contract_text = safe_path(root, report["artifacts"]["requirements"]).read_text(encoding="utf-8")
        definitions = _definitions(contract_text, ("REQ", "DEF", "FIX", "KEEP"), lambda *args: None, "")
        if not any(not key.startswith("DEF-") for key in definitions):
            raise WorkflowError("The contract needs explicit behavioral requirement IDs before acceptance.")
        if report["route"] == "bugfix" and not all(any(key.startswith(prefix + "-") for key in definitions) for prefix in ("DEF", "FIX", "KEEP")):
            raise WorkflowError("A bugfix contract needs defect, correction, and preservation IDs.")
    if artifact == "design":
        design_text = safe_path(root, report["artifacts"]["design"]).read_text(encoding="utf-8")
        if not _definitions(design_text, ("DES",), lambda *args: None, ""):
            raise WorkflowError("The design needs explicit DES IDs before acceptance.")
    if artifact == "tasks":
        _assert_artifact_ready(root, report, "requirements")
        _assert_artifact_ready(root, report, "design")
        if not report["tasks"] or any(item["code"] == "missing-coverage" for item in report["issues"]):
            raise WorkflowError("Tasks need complete requirement/task/check coverage before acceptance.")
    blocked = [question["id"] for question in report["open_questions"] if artifact in question.get("blocks", []) or artifact == "tasks" and any(key in question.get("blocks", []) for key in ARTIFACTS)]
    if blocked:
        raise WorkflowError("Resolve the actual blocking questions first: " + ", ".join(blocked))
    if any(fact.get("kind") == "conflicting" for fact in report["known_facts"]):
        raise WorkflowError("Resolve recorded conflicting facts before accepting an artifact boundary.")


def new_work(root, work_id, title, mode="greenfield", route="requirements-first", idea="", activate=False):
    root = Path(root).resolve()
    if not root.is_dir() or not WORK_ID.fullmatch(work_id) or not title.strip() or mode not in ("greenfield", "brownfield") or route not in ROUTES:
        raise WorkflowError("Provide an existing project root, valid ID, title, mode, and route.")
    work = safe_path(root, f"specs/{work_id}")
    pointer = safe_path(root, ".codex/workflow.json") if activate else None
    if pointer is not None:
        if pointer.exists() and not pointer.is_file():
            raise WorkflowError("The active pointer destination exists but is not a file; repair it before creating activated work.")
        parent = pointer.parent
        while parent != root:
            if parent.exists() and not parent.is_dir():
                raise WorkflowError("The active pointer parent is not a directory; repair it before creating activated work.")
            parent = parent.parent
    if work.exists():
        raise WorkflowError("The work directory already exists; new never overwrites it.")
    requirements_name = "bugfix.md" if route == "bugfix" else "requirements.md"
    data = {"schema_version": SCHEMA_VERSION, "id": work_id, "title": title, "mode": mode, "route": route, "phase": "consultation",
            "artifacts": {"requirements": requirements_name, "design": "design.md", "tasks": "tasks.md"},
            "context_files": _initial_context(root),
            "facts": [{"id": "F-001", "kind": "supplied", "statement": idea, "source": "User-provided initialization (--idea)."}] if idea else [],
            "questions": [], "reviews": [], "evidence": []}
    heading = "Bugfix analysis" if route == "bugfix" else "Requirements"
    draft = f"# {heading}: {work_id} — {title}\n\n**State:** Consultation; no review recorded.\n\n## Supplied goal\n\n{idea or 'No goal captured yet. Read the user request and existing project context.'}\n\n## Consultation notes\n\nCapture supplied facts, preserved constraints, and consequential unknowns before drafting the behavioral contract. Do not treat this scaffold as approved requirements.\n"
    work.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".workflow-new-", dir=work.parent) as temporary:
        staged = Path(temporary) / "work"
        staged.mkdir()
        atomic_json(staged / "work.json", data)
        (staged / requirements_name).write_text(draft, encoding="utf-8")
        if work.exists():
            raise WorkflowError("The work directory was created concurrently; nothing was overwritten.")
        os.rename(staged, work)
    if pointer is not None:
        try:
            atomic_json(pointer, {"schema_version": SCHEMA_VERSION, "active_work": f"specs/{work_id}"})
        except OSError as exc:
            raise WorkflowError(f"Work {work_id!r} was created at specs/{work_id}, but activation failed: {exc}. Inspect it using its explicit ID and repair the active pointer; do not recreate the work directory.") from exc
    return inspect_work(root, work_id)


def record_review(root, work_id, artifact, outcome, decision_ref, reviewer, authority):
    root, work, selected_id, data = _load_mutable(root, work_id)
    report = _inspect(root, work, selected_id, data)
    _assert_clean(report, ("missing-review", "stale-review"))
    if artifact not in ARTIFACTS or outcome not in ("accepted", "changes-requested") or authority not in ("user", "delegated") or not reviewer.strip() or not decision_ref.strip() or PLACEHOLDER.search(decision_ref):
        raise WorkflowError("A review needs an artifact, outcome, actual reviewer, authority, and real decision reference.")
    if outcome == "accepted":
        _assert_artifact_ready(root, report, artifact)
    snapshots = {}
    for relative in _snapshot_paths(report["route"], artifact, report["artifacts"]):
        path = safe_path(root, relative)
        if not path.is_file():
            raise WorkflowError(f"Cannot review a missing artifact: {relative}")
        snapshots[relative] = _plan_digest(path) if relative == report["artifacts"].get("tasks") else digest_file(path)
    data["reviews"].append({"id": _next_id(data["reviews"], "REV"), "artifact": artifact, "outcome": outcome,
                            "decision_ref": decision_ref, "reviewer": reviewer, "authority": authority,
                            "recorded_at": datetime.now(timezone.utc).isoformat(), "snapshot_policy": "canonical-plan-v1", "hashes": snapshots})
    atomic_json(safe_path(work, "work.json"), data)
    return inspect_work(root, selected_id)


def advance(root, work_id, target):
    root, work, selected_id, data = _load_mutable(root, work_id)
    report = _inspect(root, work, selected_id, data)
    _assert_clean(report)
    sequence = ROUTES[report["route"]]
    position = sequence.index(report["phase"])
    if position + 1 >= len(sequence) or target != sequence[position + 1]:
        raise WorkflowError("Advance only to the next phase on the selected route; reconcile earlier work explicitly.")
    if report["phase"] in ARTIFACTS:
        _assert_artifact_ready(root, report, report["phase"])
        if report["reviews"][report["phase"]]["status"] != "accepted":
            raise WorkflowError("Record the actual existing user/delegated review for this artifact before advancing.")
    for question in report["open_questions"]:
        if report["phase"] in question.get("blocks", []):
            raise WorkflowError(f"{question['id']} still blocks this phase boundary.")
    data["phase"] = target
    candidate = _inspect(root, work, selected_id, data)
    _assert_clean(candidate)
    atomic_json(safe_path(work, "work.json"), data)
    return candidate


def record_evidence(root, work_id, check, receipt, result, method, environment, candidate, observed_at, inputs):
    root, work, selected_id, data = _load_mutable(root, work_id)
    report = _inspect(root, work, selected_id, data)
    # A new result may legitimately repair a stale checked task; structural faults cannot.
    _assert_clean(report, ("false-completion", "stale-review", "missing-review"))
    checks = {item["id"]: item for item in report["checks"]}
    if check not in checks or result not in ("pass", "fail", "not-run") or not all(isinstance(value, str) and value.strip() and not PLACEHOLDER.search(value) for value in (method, environment, candidate)) or not _timestamp_valid(observed_at):
        raise WorkflowError("Evidence needs a defined check, actual result/method/environment/candidate, and observed-at timestamp with timezone.")
    if not inputs or not any(relative != receipt for relative in inputs):
        raise WorkflowError("Evidence must identify at least one tested input in addition to its receipt.")
    snapshots, artifact_hashes = {}, {}
    for relative in dict.fromkeys([receipt, *inputs]):
        path = safe_path(root, relative)
        if not path.is_file():
            raise WorkflowError(f"Evidence input does not exist: {relative}")
        snapshots[relative] = digest_file(path)
    for key in ("requirements", "design"):
        relative = report["artifacts"].get(key)
        if not relative or not safe_path(root, relative).is_file():
            raise WorkflowError("Evidence requires the current contract and design artifacts.")
        artifact_hashes[relative] = digest_file(safe_path(root, relative))
    data["evidence"].append({"id": _next_id(data["evidence"], "EV"), "check": check, "result": result,
                             "record": receipt, "method": method, "environment": environment, "candidate": candidate,
                             "observed_at": observed_at, "recorded_at": datetime.now(timezone.utc).isoformat(),
                             "inputs": snapshots, "artifacts": artifact_hashes, "check_signature": checks[check]["signature"]})
    atomic_json(safe_path(work, "work.json"), data)
    return inspect_work(root, selected_id)
