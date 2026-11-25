"""Specification requests, bounded syntax checks, and deliberate reconciliation.

Semantic findings and properties are authored by a reviewer. This module does
not call a model, run tests, authenticate a reviewer, or approve a phase.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import tempfile

from .engine import (
    ARTIFACTS, ROUTES, WorkflowError, _clean_markdown, _plan_digest,
    _select, _timestamp_valid, atomic_json, digest_file, digest_value, inspect_work,
    safe_path,
)

OPERATIONS = {"analyze": "analysis.json", "properties": "properties.json"}
MAX_JSON_BYTES = 2_097_152
ID = re.compile(r"(?:REQ|DEF|FIX|KEEP)-[0-9]{3,}\Z")
PROPERTY_ID = re.compile(r"PROP-[0-9]{3,}\Z")
FINDING_ID = re.compile(r"ANA-[0-9]{3,}\Z")
HASH = re.compile(r"[0-9a-f]{64}\Z")
PATTERNS = {
    "ubiquitous": "THE service SHALL retain an audit event for each accepted operation.",
    "event": "WHEN a customer retries a completed request, THE service SHALL return its original result.",
    "state": "WHILE maintenance mode is active, THE service SHALL reject new writes with a documented error.",
    "unwanted": "IF an upstream request times out, THEN THE service SHALL return the documented retryable error.",
    "optional": "WHERE reminder delivery is enabled, THE service SHALL enqueue one reminder for a confirmed booking.",
    "combined": "WHERE reminders are enabled, WHILE a booking is confirmed, WHEN its reminder time arrives, THE service SHALL enqueue its reminder once.",
}


def _read_json(path):
    if not path.is_file() or path.stat().st_size > MAX_JSON_BYTES:
        raise WorkflowError(f"Expected a regular JSON file of at most {MAX_JSON_BYTES} bytes: {path.name}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise WorkflowError(f"Cannot read {path.name}: {exc}") from exc


def _text(value):
    return isinstance(value, str) and bool(value.strip()) and not re.search(r"<[^>\n]+>|\b(?:TBD|TODO)\b", value)


def _source_path(root, reference):
    if not _text(reference):
        raise WorkflowError("A source must name actual project evidence, without draft placeholders.")
    path = safe_path(root, reference.split("#", 1)[0])
    if not path.is_file():
        raise WorkflowError(f"Referenced evidence is not a file: {reference}")
    return path


def _requirements(content):
    """Extract the documented table/heading subset, never infer requirements."""
    lines = _clean_markdown(content).splitlines()
    records, duplicate_ids = {}, []
    state_column = None
    for index, line in enumerate(lines):
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")] if line.lstrip().startswith("|") else []
        if cells and cells[0] == "ID":
            state_column = next((n for n, value in enumerate(cells) if re.fullmatch(r"Required\s*(?:or|/)\s*deferred", value, re.I)), None)
        match = re.match(r"^\s*#{1,6}\s+((?:REQ|DEF|FIX|KEEP)-[0-9]{3,})(?:\s|$)", line)
        key = cells[0] if cells and ID.fullmatch(cells[0]) else match.group(1) if match else None
        if key is None:
            continue
        if key in records:
            duplicate_ids.append(key)
            continue
        if cells:
            statement = cells[1] if len(cells) > 1 else ""
            required = not (state_column is not None and state_column < len(cells) and cells[state_column].casefold() == "deferred")
        else:
            paragraph = []
            started = False
            for following in lines[index + 1:]:
                if re.match(r"^\s*#{1,6}\s", following):
                    break
                if not following.strip():
                    if started:
                        break
                    continue
                if following.lstrip().startswith(("- ", "|")):
                    if started:
                        break
                    continue
                paragraph.append(following.strip())
                started = True
            statement = " ".join(paragraph)
            required = True
        records[key] = {"id": key, "statement": statement, "required": required and not key.startswith("DEF-"), "line": index + 1}
    return records, duplicate_ids


def ears_pattern(statement):
    """Recognize a documented EARS sentence shape, not its truth or adequacy."""
    sentence = " ".join(statement.split())
    match = re.fullmatch(r"(?:(.+?),\s*(?:THEN\s+)?)?THE\s+(.+?)\s+SHALL\s+(.+?)[.!]?", sentence, re.I)
    if not match or any(not part.strip() for part in match.groups()[1:]):
        return None
    prefix = match.group(1)
    if prefix is None:
        return "ubiquitous"
    conditions = re.findall(r"(?:^|,\s*)(WHERE|WHILE|WHEN|IF)\s+(.+?)(?=,\s*(?:WHERE|WHILE|WHEN|IF)\s+|$)", prefix, re.I)
    rebuilt = ", ".join(f"{kind} {value}" for kind, value in conditions)
    if not conditions or re.sub(r"\s+", " ", rebuilt).casefold() != re.sub(r"\s+", " ", prefix).casefold():
        return None
    kinds = [kind.upper() for kind, value in conditions]
    if any(not value.strip() for kind, value in conditions) or len(set(kinds)) != len(kinds):
        return None
    if "IF" in kinds and not re.search(r",\s*THEN\s+THE\s", sentence, re.I):
        return None
    if len(kinds) == 1:
        return {"WHEN": "event", "WHILE": "state", "IF": "unwanted", "WHERE": "optional"}[kinds[0]]
    if ("WHEN" in kinds and "IF" in kinds) or kinds != sorted(kinds, key={"WHERE": 0, "WHILE": 1, "WHEN": 2, "IF": 2}.get):
        return None
    return "combined"


def lint_ears(content):
    """Return conservative syntax errors and review hints for explicit IDs."""
    records, duplicates = _requirements(content)
    findings = []

    def finding(severity, code, message, requirements):
        findings.append({"id": f"LINT-{len(findings) + 1:03d}", "severity": severity, "code": code,
                         "message": message, "requirement_ids": requirements})

    for key in duplicates:
        finding("error", "duplicate-requirement", "The same requirement ID is defined more than once.", [key])
    if not any(record["required"] for record in records.values()):
        finding("error", "missing-behavior", "Define at least one required observable behavioral requirement.", [])
    for key, record in records.items():
        if key.startswith("DEF-") or not record["required"]:
            record["pattern"] = "observed-defect" if key.startswith("DEF-") else "deferred"
            continue
        statement = record["statement"]
        record["pattern"] = ears_pattern(statement)
        if not _text(statement):
            finding("error", "unfinished-requirement", "Replace the missing statement or draft placeholder with actual behavior.", [key])
        elif record["pattern"] is None:
            finding("error", "ears-shape", "Use an explicit EARS condition, system, SHALL response, and THEN for an unwanted condition.", [key])
        if re.search(r"\b(?:fast|quickly|scalable|user-friendly|as appropriate|as needed)\b", statement, re.I):
            finding("warning", "ambiguous-language", "Check the qualitative phrase against a measurable acceptance criterion; this hint is not a semantic finding.", [key])
    return {"requirements": list(records.values()), "findings": findings,
            "scope": "Sentence shape and limited language hints only; no semantic completeness, consistency, or approval claim."}


def _load(root, work_id):
    root = Path(root).resolve()
    work, selected_id, data = _select(root, work_id)
    return root, work, data, inspect_work(root, selected_id)


def _context(data):
    return {"facts": data.get("facts", []), "questions": data.get("questions", [])}


def _inputs(root, report, data, operation):
    paths = []
    for key in ("requirements", "design") if operation == "properties" else ("requirements",):
        relative = report["artifacts"].get(key)
        if not relative or not safe_path(root, relative).is_file():
            raise WorkflowError(f"Create the actual {key} artifact before requesting {operation}.")
        paths.append(relative)
    # Source-backed decisions matter; unrelated handoff/progress changes do not.
    if any(not isinstance(data.get(key, []), list) for key in ("facts", "questions")):
        raise WorkflowError("Repair the fact/question arrays before requesting specification review.")
    for entry in [*data.get("facts", []), *data.get("questions", [])]:
        if not isinstance(entry, dict) or not isinstance(entry.get("source"), str):
            continue
        relative = entry["source"].split("#", 1)[0]
        if relative in {f"specs/{report['id']}/{name}" for name in OPERATIONS.values()}:
            raise WorkflowError("Decision sources must be separate from mutable operation histories; reference the actual decision notes.")
        try:
            path = safe_path(root, relative)
        except WorkflowError:
            continue
        if path.is_file() and relative not in paths and not relative.endswith("/work.json"):
            paths.append(relative)
    hashes = dict(report.get("foundation_sources", {}))
    for relative, identity in hashes.items():
        if identity is None:
            raise WorkflowError(f"Selected project foundation is missing: {relative}")
    for relative in paths:
        if relative not in hashes:
            hashes[relative] = digest_file(safe_path(root, relative))
    return dict(sorted(hashes.items()))


def _schema(request, ids):
    string = {"type": "string"}
    array = lambda item: {"type": "array", "items": item}
    object_schema = lambda props: {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}
    id_schema = {"type": "string", "enum": sorted(ids)} if ids else string
    base = {
        "schema_version": {"type": "integer", "const": 1},
        "operation": {"type": "string", "const": request["operation"]},
        "request_id": {"type": "string", "const": request["request_id"]},
        "input_hashes": object_schema({path: {"type": "string", "const": value} for path, value in request["input_hashes"].items()}),
        "context_fingerprint": {"type": "string", "const": request["context_fingerprint"]},
        "reviewer": string, "review_ref": string, "observed_at": string, "summary": string,
    }
    if request["operation"] == "analyze":
        base["findings"] = array(object_schema({
            "id": string, "requirement_ids": array(id_schema),
            "severity": {"type": "string", "enum": ["blocker", "warning", "info"]},
            "category": {"type": "string", "enum": ["contradiction", "ambiguity", "constraint", "assumption", "missing-case", "format", "other"]},
            "statement": string, "state": {"type": "string", "enum": ["open", "resolved"]},
            "resolution": string, "source": string,
        }))
    else:
        base["properties"] = array(object_schema({
            "id": string, "requirement_ids": array(id_schema), "statement": string,
            "preconditions": string, "strategy": {"type": "string", "enum": ["property-based", "example", "contract", "integration", "operational"]},
            "verification": string, "task_ids": array(string), "check_ids": array(string), "source": string,
        }))
    return object_schema(base)


def _request(root, report, data, operation):
    if operation not in OPERATIONS:
        raise WorkflowError("Specification operation must be analyze or properties.")
    hashes = _inputs(root, report, data, operation)
    content = safe_path(root, report["artifacts"]["requirements"]).read_text(encoding="utf-8")
    lint = lint_ears(content)
    context = _context(data)
    identity = {"schema_version": 1, "operation": operation, "work_id": report["id"],
                "input_hashes": hashes, "context_fingerprint": digest_value(context)}
    request = {**identity, "request_id": digest_value(identity), "route": report["route"],
               "requirements": lint["requirements"], "context": context,
               "deterministic_findings": lint["findings"], "ears_patterns": PATTERNS,
               "artifacts": report["artifacts"],
               "task_references": [{"id": task["id"], "requirements": task["requirements"], "checks": task["checks"]} for task in report["tasks"]],
               "check_references": [{"id": check["id"], "requirements": check["requirements"], "tasks": check["tasks"]} for check in report["checks"]],
               "writes": False, "model_called": False,
               "response_schema": {}}
    if operation == "analyze":
        request["instructions"] = [
            "Read every input and the actual user decision sources before reviewing. Analyze the requirement set together: contradictions, ambiguous thresholds, incompatible constraints, undefined assumptions, missing edges, concurrency and failure behavior.",
            "Research engineering questions where authorized; ask only unresolved product/authority decisions. Do not invent answers. Report each finding with affected IDs, severity, state, source and actual resolution.",
            "Save actual review notes in a project-relative file, then author JSON matching response_schema and name that file in review_ref. Empty findings means a performed review found none; this request alone proves no review occurred.",
            "This operation does not record product acceptance or advance a phase. Standard routes retain the user's actual review decisions or explicit prior delegation; quick work has no intermediate artifact approval pauses.",
        ]
    else:
        request["instructions"] = [
            "Read the requirements, accepted decisions and design. Derive observable correctness properties and their preconditions. Cover every required behavioral ID with a suitable verification strategy; a property-based test is optional, the required behavior is not.",
            "Include reproduction, correction and preserved-behavior checks for a defect. Explain a proposed generated-input domain and failure example when property-based tests fit. Use real-service checks for claims that local mocks cannot establish.",
            "Map properties to proposed task/check IDs; if tasks already exist, use their exact IDs and matching requirement coverage. Empty task/check arrays are allowed during design and must be mapped before accepting the task plan.",
            "Save actual derivation notes and author the response. When implementing, create the chosen executable tests and run the relevant checks; a property record is a plan and does not claim a test has run.",
        ]
    request["response_schema"] = _schema(request, {item["id"] for item in lint["requirements"]})
    return request


def analyze_requirements(root, work_id=None):
    root, work, data, report = _load(root, work_id)
    return _request(root, report, data, "analyze")


def derive_properties(root, work_id=None):
    root, work, data, report = _load(root, work_id)
    return _request(root, report, data, "properties")


def _exact_keys(value, keys, label):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise WorkflowError(f"{label} must contain exactly: {', '.join(keys)}.")


def _ids(values, pattern, allowed, label, required=True):
    if not isinstance(values, list) or (required and not values) or len(set(value for value in values if isinstance(value, str))) != len(values) or any(not isinstance(value, str) or not pattern.fullmatch(value) or allowed is not None and value not in allowed for value in values):
        raise WorkflowError(f"{label} needs distinct, valid referenced IDs.")


def _validate_response(root, report, request, response, require_mapping=False):
    operation = request["operation"]
    entries_key = "findings" if operation == "analyze" else "properties"
    base_keys = ["schema_version", "operation", "request_id", "input_hashes", "context_fingerprint", "reviewer", "review_ref", "observed_at", "summary", entries_key]
    _exact_keys(response, base_keys, "Review response")
    if type(response["schema_version"]) is not int or response["schema_version"] != 1 or any(response[key] != request[key] for key in ("operation", "request_id", "input_hashes", "context_fingerprint")):
        raise WorkflowError("The response must identify this exact current request and its input hashes; regenerate a stale request before reviewing.")
    if not all(_text(response[key]) for key in ("reviewer", "review_ref", "summary")) or not _timestamp_valid(response["observed_at"]):
        raise WorkflowError("A response needs an actual reviewer, review notes, summary and timezone-qualified observation time.")
    _source_path(root, response["review_ref"])
    if not isinstance(response[entries_key], list) or any(not isinstance(item, dict) for item in response[entries_key]):
        raise WorkflowError(f"{entries_key} must be an array of records.")
    definitions = {item["id"] for item in request["requirements"]}
    seen, covered = set(), set()
    tasks = {task["id"]: task for task in report["tasks"]}
    checks = {check["id"]: check for check in report["checks"]}
    for item in response[entries_key]:
        keys = (["id", "requirement_ids", "severity", "category", "statement", "state", "resolution", "source"] if operation == "analyze"
                else ["id", "requirement_ids", "statement", "preconditions", "strategy", "verification", "task_ids", "check_ids", "source"])
        _exact_keys(item, keys, entries_key)
        pattern = FINDING_ID if operation == "analyze" else PROPERTY_ID
        if not isinstance(item["id"], str) or not pattern.fullmatch(item["id"]) or item["id"] in seen:
            raise WorkflowError("Finding/property IDs must be valid and unique.")
        seen.add(item["id"])
        _ids(item["requirement_ids"], ID, definitions, "Requirement references")
        if not _text(item["statement"]):
            raise WorkflowError("Findings/properties need an actual statement.")
        _source_path(root, item["source"])
        covered.update(item["requirement_ids"])
        if operation == "analyze":
            if item["severity"] not in ("blocker", "warning", "info") or item["category"] not in ("contradiction", "ambiguity", "constraint", "assumption", "missing-case", "format", "other") or item["state"] not in ("open", "resolved") or not isinstance(item["resolution"], str):
                raise WorkflowError("Findings need a supported severity, category, state and resolution string.")
            if item["state"] == "resolved" and not _text(item["resolution"]):
                raise WorkflowError("A resolved finding needs the actual resolution and its evidence source.")
        else:
            if item["strategy"] not in ("property-based", "example", "contract", "integration", "operational") or not all(_text(item[key]) for key in ("preconditions", "verification")):
                raise WorkflowError("A property needs preconditions, a supported strategy and an observable verification plan.")
            _ids(item["task_ids"], re.compile(r"T-[0-9]{3,}\Z"), set(tasks) if tasks else None, "Task references", required=require_mapping)
            _ids(item["check_ids"], re.compile(r"CHK-[0-9]{3,}\Z"), set(checks) if checks else None, "Check references", required=require_mapping)
            if tasks and item["task_ids"]:
                linked = {req for task in item["task_ids"] for req in tasks[task]["requirements"]}
                if set(item["requirement_ids"]) - linked:
                    raise WorkflowError("Property requirements must be covered by their linked tasks.")
            if checks and item["check_ids"]:
                linked = {req for check in item["check_ids"] for req in checks[check]["requirements"]}
                if set(item["requirement_ids"]) - linked:
                    raise WorkflowError("Property requirements must be covered by their linked checks.")
                if tasks and item["task_ids"] and any(not set(checks[check]["tasks"]) & set(item["task_ids"]) for check in item["check_ids"]):
                    raise WorkflowError("Property checks must connect to the property's linked tasks.")
    if operation == "properties":
        required = {item["id"] for item in request["requirements"] if item["required"]}
        if not required or required - covered:
            raise WorkflowError("Properties must cover every required behavioral requirement with an appropriate verification strategy.")


def _history(root, report, operation):
    path = safe_path(root, f"specs/{report['id']}/{OPERATIONS[operation]}")
    if not path.exists():
        return path, {"schema_version": 1, "operation": operation, "work_id": report["id"], "records": []}
    value = _read_json(path)
    if not isinstance(value, dict) or type(value.get("schema_version")) is not int or value.get("schema_version") != 1 or value.get("operation") != operation or value.get("work_id") != report["id"] or not isinstance(value.get("records"), list) or any(not isinstance(record, dict) for record in value["records"]):
        raise WorkflowError(f"Invalid {operation} history; preserve it and resolve its schema before continuing.")
    return path, value


def record_specification_result(root, work_id, operation, response_path):
    """Record an already performed review; never synthesize reviewer conclusions."""
    root, work, data, report = _load(root, work_id)
    request = _request(root, report, data, operation)
    response_file = safe_path(root, response_path)
    response = _read_json(response_file)
    _validate_response(root, report, request, response)
    path, history = _history(root, report, operation)
    if response_file == path:
        raise WorkflowError("A response must be separate from its operation history.")
    review_file = _source_path(root, response["review_ref"])
    if review_file == response_file:
        raise WorkflowError("Response JSON and actual review notes must be separate files.")
    if review_file == path:
        raise WorkflowError("Review notes must be separate from the operation history.")
    receipt_inputs = {response_path: digest_file(response_file), review_file.relative_to(root).as_posix(): digest_file(review_file)}
    if any(relative in request["input_hashes"] for relative in receipt_inputs):
        raise WorkflowError("Response and review notes must be separate from reviewed source inputs.")
    for item in response["findings" if operation == "analyze" else "properties"]:
        source_file = _source_path(root, item["source"])
        if source_file == response_file or source_file in {safe_path(work, name) for name in OPERATIONS.values()}:
            raise WorkflowError("Finding/property sources must identify evidence separate from the response and mutable operation histories.")
        relative = source_file.relative_to(root).as_posix()
        if relative not in request["input_hashes"]:
            receipt_inputs[relative] = digest_file(source_file)
    if history["records"] and history["records"][-1].get("response") == response and history["records"][-1].get("receipt_inputs") == receipt_inputs:
        return specification_status(root, report)
    record = {"id": f"{operation.upper()}-{len(history['records']) + 1:04d}", "recorded_at": datetime.now(timezone.utc).isoformat(),
              "response": response, "response_path": response_path, "receipt_inputs": receipt_inputs}
    # Re-read relevant state before the one-file commit; no silent stale import.
    current_data = _select(root, report["id"])[2]
    if _request(root, inspect_work(root, report["id"]), current_data, operation)["request_id"] != request["request_id"]:
        raise WorkflowError("Specification inputs changed during recording; review the new request.")
    history["records"].append(record)
    if len(json.dumps(history).encode("utf-8")) > MAX_JSON_BYTES:
        raise WorkflowError("The operation history exceeds the bounded JSON size; archive deliberately before adding another record.")
    atomic_json(path, history)
    return specification_status(root, inspect_work(root, report["id"]))


def specification_status(root, report):
    """Inspect optional operation records without recursively inspecting work."""
    root = Path(root).resolve()
    data = _read_json(safe_path(root, f"specs/{report['id']}/work.json"))
    result = {"issues": [], "blocking_findings": [], "operations": {}, "lint_findings": []}
    contract = report.get("artifacts", {}).get("requirements")
    if contract and safe_path(root, contract).is_file():
        result["lint_findings"] = lint_ears(safe_path(root, contract).read_text(encoding="utf-8"))["findings"]
    sequence = ROUTES.get(report.get("route"), [])
    boundary = "tasks" if report.get("route") == "quick" else "requirements"
    past_contract = report.get("phase") in sequence and boundary in sequence and sequence.index(report["phase"]) > sequence.index(boundary)
    accepted = report.get("reviews", {}).get("requirements", {}).get("status") == "accepted" or report.get("route") == "quick" and report.get("reviews", {}).get("tasks", {}).get("status") == "accepted"
    if data.get("spec_format") == "ears" and (past_contract or accepted):
        for finding in result["lint_findings"]:
            result["issues"].append({"severity": finding["severity"], "code": finding["code"], "message": finding["message"] + " " + ", ".join(finding["requirement_ids"]), "path": contract})
    for operation in OPERATIONS:
        relative = f"specs/{report['id']}/{OPERATIONS[operation]}"
        status = {"status": "missing", "path": relative}
        result["operations"][operation] = status
        try:
            path, history = _history(root, report, operation)
            if not history["records"]:
                continue
            record = history["records"][-1]
            response = record.get("response")
            status.update({"record_id": record.get("id"), "reviewer": response.get("reviewer") if isinstance(response, dict) else None})
            if not _timestamp_valid(record.get("recorded_at")) or not isinstance(record.get("receipt_inputs"), dict) or not record["receipt_inputs"]:
                raise WorkflowError("Operation record needs a timestamp and receipt identities.")
            if not isinstance(record.get("response_path"), str) or record["response_path"] not in record["receipt_inputs"]:
                raise WorkflowError("Operation record must identify its actual response file.")
            for relative, expected in record["receipt_inputs"].items():
                safe_path(root, relative)
                if not isinstance(expected, str) or not HASH.fullmatch(expected):
                    raise WorkflowError("Operation receipt identities must be project-relative paths and SHA-256 values.")
            request = _request(root, report, data, operation)
            stale = any(not isinstance(expected, str) or not HASH.fullmatch(expected) or not safe_path(root, name).is_file() or digest_file(safe_path(root, name)) != expected for name, expected in record["receipt_inputs"].items())
            if not isinstance(response, dict):
                raise WorkflowError("Operation record has no response object.")
            response_file = safe_path(root, record["response_path"])
            if response_file.is_file() and digest_file(response_file) == record["receipt_inputs"][record["response_path"]] and _read_json(response_file) != response:
                raise WorkflowError("Recorded response differs from the identified response file.")
            stale = stale or any(response.get(key) != request[key] for key in ("request_id", "input_hashes", "context_fingerprint"))
            # An unresolved recorded blocker survives source changes until a new
            # actual analysis resolves or supersedes it.
            if operation == "analyze" and isinstance(response.get("findings"), list):
                for finding in response["findings"]:
                    if isinstance(finding, dict) and finding.get("severity") == "blocker" and finding.get("state") == "open":
                        result["blocking_findings"].append({**finding, "current": not stale})
                        result["issues"].append({"severity": "error", "code": "specification-blocker", "message": f"{finding.get('id')}: {finding.get('statement')} Resolve it in a current analysis record.", "path": relative})
            if stale:
                status["status"] = "stale"
                result["issues"].append({"severity": "warning", "code": "stale-specification-review", "message": f"The {operation} response or its reviewed inputs changed; its conclusions are historical.", "path": relative})
                continue
            _validate_response(root, report, request, response)
            status.update({"status": "current", "request_id": request["request_id"], "summary": response["summary"], "count": len(response["findings" if operation == "analyze" else "properties"])})
            if operation == "properties":
                status["properties"] = response["properties"]
                try:
                    _validate_response(root, report, request, response, require_mapping=True)
                    status["task_mapping"] = "complete"
                except WorkflowError as exc:
                    status["task_mapping"] = "incomplete"
                    status["mapping_issue"] = str(exc)
        except (WorkflowError, OSError, UnicodeError, TypeError, ValueError) as exc:
            status["status"] = "invalid"
            result["issues"].append({"severity": "error", "code": "invalid-specification-review", "message": str(exc), "path": relative})
    return result


def plan_reconciliation(root, work_id=None, changed_paths=()):
    """Preview impact from declared identities and explicit changed paths."""
    root, work, data, report = _load(root, work_id)
    if not isinstance(changed_paths, (list, tuple)) or any(not isinstance(value, str) for value in changed_paths):
        raise WorkflowError("Changed paths must be a list of project-relative paths.")
    explicit = sorted(set(changed_paths))
    for relative in explicit:
        safe_path(root, relative)
    watched = {f"specs/{report['id']}/work.json", *report["artifacts"].values(), *explicit}
    changed = set(explicit)
    affected_artifacts = set()
    for record in data.get("reviews", []):
        for relative, expected in record.get("hashes", {}).items():
            watched.add(relative)
    latest_reviews = {record.get("artifact"): record for record in data.get("reviews", [])}
    for record in latest_reviews.values():
        for relative, expected in record.get("hashes", {}).items():
            path = safe_path(root, relative)
            actual = _plan_digest(path) if relative == report["artifacts"].get("tasks") and path.is_file() else digest_file(path) if path.is_file() else None
            if actual != expected:
                changed.add(relative)
    latest_checks = {record.get("check"): record for record in data.get("evidence", [])}
    affected_checks = {check for check, evidence in report["evidence"].items() if not evidence["current"]}
    for check, record in latest_checks.items():
        for relative, expected in record.get("inputs", {}).items():
            watched.add(relative)
            path = safe_path(root, relative)
            if not path.is_file() or digest_file(path) != expected:
                changed.add(relative)
            if relative in explicit:
                affected_checks.add(check)
    changed_context, operation_refreshes = [], set()
    for operation in OPERATIONS:
        relative = f"specs/{report['id']}/{OPERATIONS[operation]}"
        watched.add(relative)
        _, history = _history(root, report, operation)
        if history["records"]:
            for relative, expected in history["records"][-1].get("receipt_inputs", {}).items():
                watched.add(relative)
                path = safe_path(root, relative)
                if not path.is_file() or digest_file(path) != expected:
                    changed.add(relative)
                    operation_refreshes.add(operation)
            response = history["records"][-1].get("response", {})
            if response.get("context_fingerprint") != digest_value(_context(data)):
                changed_context.append(operation)
                operation_refreshes.add(operation)
            previous_inputs = response.get("input_hashes", {})
            if report.get("specification", {}).get("operations", {}).get(operation, {}).get("status") == "stale":
                # Selection can change even when all formerly selected files have
                # the same bytes. Bind additions/removals to the sync preview too.
                current_inputs = _inputs(root, report, data, operation)
                selection_changes = previous_inputs.keys() ^ current_inputs.keys()
                if selection_changes:
                    watched.update(selection_changes)
                    changed.update(selection_changes)
                    operation_refreshes.add(operation)
            for relative, expected in previous_inputs.items():
                watched.add(relative)
                path = safe_path(root, relative)
                if not path.is_file() or digest_file(path) != expected:
                    changed.add(relative)
                    operation_refreshes.add(operation)
    affected_artifacts.update(key for key, relative in report["artifacts"].items() if relative in changed)
    if affected_artifacts & {"requirements", "design"}:
        affected_checks.update(check["id"] for check in report["checks"])
    affected_tasks = {task["id"] for task in report["tasks"] if task["checked"] and not task["completion_valid"] or set(task["checks"]) & affected_checks}
    if "tasks" in affected_artifacts:
        affected_tasks.update(task["id"] for task in report["tasks"] if task["checked"] and not task["completion_valid"])
    expanded = True
    while expanded:
        before = len(affected_tasks)
        affected_tasks.update(task["id"] for task in report["tasks"] if set(task["dependencies"]) & affected_tasks)
        expanded = len(affected_tasks) != before
    reopen = [task["id"] for task in report["tasks"] if task["checked"] and task["id"] in affected_tasks]
    route, phase = report["route"], report["phase"]
    sequence = ROUTES[route]
    target = phase
    candidates = ["tasks" if route == "quick" else key for key in affected_artifacts]
    candidates.extend("tasks" if route == "quick" else "requirements" if operation == "analyze" else "design" for operation in operation_refreshes)
    if affected_tasks:
        candidates.append("tasks" if route == "plan" else "implementation")
    if candidates:
        target = min([phase, *candidates], key=sequence.index)
    identities = {relative: digest_file(safe_path(root, relative)) if safe_path(root, relative).is_file() else None for relative in sorted(watched)}
    body = {"schema_version": 1, "work_id": report["id"], "route": route, "phase": phase, "target_phase": target,
            "changed_paths": sorted(changed), "explicit_changed_paths": explicit, "affected_artifacts": sorted(affected_artifacts),
            "affected_reviews": [name for name, review in report["reviews"].items() if review["status"] == "stale"],
            "affected_checks": sorted(affected_checks), "affected_tasks": sorted(affected_tasks), "reopen_tasks": reopen,
            "changed_decision_context": changed_context, "operation_refreshes": sorted(operation_refreshes), "input_hashes": identities}
    return {**body, "fingerprint": digest_value(body), "writes": False,
            "instructions": [
                "Read changed inputs and actual decisions; preserve unrelated user edits and accepted architecture. Resolve semantic impact before regenerating dependent prose.",
                "Update requirements then design for requirements-first, design then derived requirements for design-first, or the connected set for quick work. Preserve stable IDs and required behavior.",
                "Regenerate only affected task/check definitions and verification plans. Existing code is not proof that the changed contract is satisfied. Historical reviews/results remain historical.",
                "Applying this preview only reopens listed completion and rewinds the phase; it does not rewrite a contract, approve changes, run a test or grant authority. Review and reverify affected outcomes afterward.",
            ]}


def _atomic_text(path, content):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile("w", dir=path.parent, prefix=".workflow-sync-", encoding="utf-8", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def apply_reconciliation(root, work_id, expected_fingerprint, reason, changed_paths=()):
    """Apply a reviewed preview without inventing new requirements or evidence."""
    if not _text(reason):
        raise WorkflowError("Reconciliation needs the actual reason and decision context.")
    plan = plan_reconciliation(root, work_id, changed_paths)
    if not isinstance(expected_fingerprint, str) or expected_fingerprint != plan["fingerprint"]:
        raise WorkflowError("The reconciliation preview is stale; inspect the current preview before applying it.")
    root = Path(root).resolve()
    work, selected_id, data = _select(root, plan["work_id"])
    report = inspect_work(root, selected_id)
    metadata_path = safe_path(work, "work.json")
    tasks_path = safe_path(root, report["artifacts"]["tasks"])
    before_metadata = metadata_path.read_text(encoding="utf-8")
    before_tasks = tasks_path.read_text(encoding="utf-8") if tasks_path.is_file() else None
    after_tasks = before_tasks
    for task_id in plan["reopen_tasks"]:
        pattern = re.compile(r"(^#{2,4}\s+" + re.escape(task_id) + r"(?:\s+[—–-]\s*|\s+).*?)(?=^#{1,4}\s|\Z)", re.M | re.S)

        def reopen(match):
            block = match.group(1)
            block, count = re.subn(r"^(\s*-\s+)\[[xX]\](\s+" + re.escape(task_id) + r"\s+complete\.?)\s*$", r"\1[ ]\2", block, flags=re.M)
            if count != 1:
                raise WorkflowError(f"Cannot safely reopen {task_id}; repair its canonical checkbox first.")
            block = re.sub(r"^(\s*-\s+Activity:)\s*.*$", r"\1 needs verification", block, flags=re.M | re.I)
            return block

        after_tasks, count = pattern.subn(reopen, after_tasks)
        if count != 1:
            raise WorkflowError(f"Cannot locate exactly one task block for {task_id}.")
    previous = data.get("reconciliations", [])
    if not isinstance(previous, list):
        raise WorkflowError("Reconciliation history must be an array; preserve and repair the record.")
    data = deepcopy(data)
    data["phase"] = plan["target_phase"]
    data["reconciliations"] = previous + [{"id": f"SYNC-{len(previous) + 1:04d}", "observed_at": datetime.now(timezone.utc).isoformat(),
                                          "reason": reason, "preview_fingerprint": plan["fingerprint"],
                                          "from_phase": plan["phase"], "to_phase": plan["target_phase"],
                                          "changed_paths": plan["changed_paths"], "reopened_tasks": plan["reopen_tasks"]}]
    after_metadata = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if plan_reconciliation(root, selected_id, changed_paths)["fingerprint"] != plan["fingerprint"]:
        raise WorkflowError("The project changed during reconciliation; no updates were applied.")
    writes = []
    if before_tasks is not None and after_tasks != before_tasks:
        writes.append((tasks_path, before_tasks, after_tasks))
    writes.append((metadata_path, before_metadata, after_metadata))
    completed = []
    try:
        for path, before, after in writes:
            if path.read_text(encoding="utf-8") != before:
                raise WorkflowError("A concurrent edit changed a reconciliation target.")
            _atomic_text(path, after)
            completed.append((path, before, after))
    except (OSError, WorkflowError) as exc:
        leftovers = []
        for path, before, after in reversed(completed):
            try:
                if path.read_text(encoding="utf-8") != after:
                    raise OSError("Concurrent edit prevents rollback")
                _atomic_text(path, before)
            except OSError:
                leftovers.append(path.relative_to(root).as_posix())
        suffix = " Review concurrent changes in: " + ", ".join(leftovers) if leftovers else " This operation's completed writes were rolled back."
        raise WorkflowError(f"Reconciliation could not finish: {exc}.{suffix}") from exc
    return {"applied": True, "plan": plan, "report": inspect_work(root, selected_id)}
