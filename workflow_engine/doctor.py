"""Read-only onboarding inspection and optional hook configuration preview.

No subprocess is launched. Executable presence does not establish login, model
access, native hook trust, plugin loading or AWS authority.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import sys

from .engine import CONTEXT_DEFAULTS, WorkflowError, inspect_work, safe_path


RUNTIME_FILES = (
    "scripts/workflow.py", "workflow_engine/__init__.py", "workflow_engine/engine.py",
    "workflow_engine/context.py", "workflow_engine/specifications.py",
    "workflow_engine/runner.py", "workflow_engine/doctor.py",
)
GUIDANCE_FILES = (
    "workflows/consult.md", "workflows/brownfield.md", "workflows/feature.md",
    "workflows/bugfix.md", "workflows/reconcile.md", "templates/project-brief.md",
    "templates/requirements.md", "templates/bugfix.md", "templates/design.md",
    "templates/tasks.md", "guide/00-quickstart.md",
    "docs/reference/specification-operations.md", "docs/reference/task-execution.md",
)
MANIFEST = ".aws-workflow/manifest.json"
MAX_METADATA_BYTES = 1_048_576
INSTRUCTION_BEGIN = "<!-- codex-aws-workflow:start -->"
INSTRUCTION_END = "<!-- codex-aws-workflow:end -->"


def _root(value):
    root = Path(value).absolute()
    if any(path.is_symlink() for path in (root, *root.parents)):
        raise WorkflowError("Setup inspection requires an ordinary directory without symlink components.")
    if not root.is_dir():
        raise WorkflowError("Setup inspection requires an existing project directory.")
    return root.resolve()


def _regular_file(root, relative):
    path = safe_path(root, relative)
    if not path.is_file():
        raise WorkflowError(f"Required local file is missing: {relative}")
    if path.stat().st_size > MAX_METADATA_BYTES:
        raise WorkflowError(f"Local setup file exceeds the inspection size limit: {relative}")
    return path


def _json(root, relative):
    path = _regular_file(root, relative)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise WorkflowError(f"Cannot parse local setup file: {relative}") from exc
    if not isinstance(value, dict):
        raise WorkflowError(f"Local setup file must contain an object: {relative}")
    return value


def _layout(root):
    """Select the installed namespace before considering the source layout."""
    manifest_path = safe_path(root, MANIFEST)
    if manifest_path.exists() or safe_path(root, ".aws-workflow").exists():
        manifest = _json(root, MANIFEST)
        if manifest.get("identity") != "codex-aws-workflow" or type(manifest.get("schema_version")) is not int or manifest["schema_version"] != 1:
            raise WorkflowError("The installed manifest has an unknown identity or schema version.")
        if not isinstance(manifest.get("paths"), dict) or not isinstance(manifest.get("managed_files"), dict):
            raise WorkflowError("The installed manifest needs paths and managed_files objects.")
        return "adopted", ".aws-workflow/", manifest
    if safe_path(root, "scripts/workflow.py").is_file():
        return "source", "", None
    return "uninstalled", "", None


def inspect_environment(root, *, executable_lookup=None):
    """Inspect local setup without commands, authentication probes or work selection."""
    root = _root(root)
    lookup = executable_lookup or shutil.which
    checks = []

    def add(key, status, detail, *, required=False, next_action=""):
        item = {"id": key, "status": status, "required": required, "detail": detail}
        if next_action:
            item["next_action"] = next_action
        checks.append(item)

    python_ready = sys.version_info >= (3, 10)
    add("python", "ready" if python_ready else "missing", f"Running Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}; Python 3.10 or newer is required.", required=True)
    kind, prefix, manifest = "uninstalled", "", None
    try:
        kind, prefix, manifest = _layout(root)
        if kind == "uninstalled":
            add("package", "missing", "No source or adopted runtime was found.", required=True, next_action="Preview and apply the bootstrap into this application before using its workflow commands.")
        else:
            missing, changed = [], []
            for relative in (*RUNTIME_FILES, *GUIDANCE_FILES):
                installed = prefix + relative
                try:
                    path = _regular_file(root, installed)
                    if manifest is not None:
                        expected = manifest["managed_files"].get(installed)
                        if not isinstance(expected, str) or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                            changed.append(installed)
                except (WorkflowError, OSError):
                    missing.append(installed)
            if missing or changed:
                add("package", "invalid", "Required runtime or guidance is incomplete or differs from the installation manifest.", required=True, next_action="Review missing/changed package files and use an explicit update or restoration; do not force an overwrite.")
                checks[-1]["missing_files"], checks[-1]["changed_files"] = missing, changed
            else:
                add("package", "ready", "Required runtime and consultation guidance are present" + (" and match their recorded installation hashes." if manifest else ". Source presence is not a runtime test."), required=True)
    except (WorkflowError, OSError) as exc:
        add("package", "invalid", str(exc), required=True, next_action="Repair or explicitly merge the installation manifest before using the package.")

    try:
        instructions = _regular_file(root, "AGENTS.md")
        if manifest is not None:
            content = instructions.read_text(encoding="utf-8")
            if content.count(INSTRUCTION_BEGIN) != 1 or content.count(INSTRUCTION_END) != 1:
                raise WorkflowError("The adopted instruction block is missing or ambiguous; review the project instructions.")
            block = content[content.index(INSTRUCTION_BEGIN):content.index(INSTRUCTION_END) + len(INSTRUCTION_END)]
            if hashlib.sha256(block.encode()).hexdigest() != manifest.get("agent_block_sha256"):
                raise WorkflowError("The adopted instruction block differs from its manifest; review the intended merge.")
        add("instructions", "ready", "Root project instructions are present; actual client loading has not been observed.", required=True)
    except (WorkflowError, OSError, UnicodeError) as exc:
        add("instructions", "invalid", str(exc), required=True)

    mapped = manifest["paths"] if manifest else CONTEXT_DEFAULTS
    missing_records = []
    for key in CONTEXT_DEFAULTS:
        relative = mapped.get(key)
        try:
            if not isinstance(relative, str):
                raise WorkflowError("Missing context path")
            _regular_file(root, relative)
        except (WorkflowError, OSError):
            missing_records.append(key)
    add("project-context", "missing" if missing_records else "ready", "Missing or unsafe mapped records: " + ", ".join(missing_records) if missing_records else "Mapped brief, handoff, adoption and capability records are present.", required=True)

    active = None
    try:
        pointer = safe_path(root, ".codex/workflow.json")
        if not pointer.exists():
            add("active-work", "not-selected", "No work is selected. This is expected immediately after adoption.", next_action="Read the mapped context and begin consultation; create and activate a work item after its scope is understood.")
        else:
            report = inspect_work(root)
            active = {"id": report["id"], "phase": report["phase"]}
            errors = [item for item in report["issues"] if item["severity"] == "error"]
            add("active-work", "invalid" if errors else "ready", f"Selected {report['id']} in phase {report['phase']}.", required=True, next_action="Reconcile workflow issues before treating this work as ready." if errors else "")
            checks[-1]["issues"] = report["issues"]
    except (WorkflowError, OSError, UnicodeError) as exc:
        add("active-work", "invalid", str(exc), required=True, next_action="Inspect the pointer and canonical work; do not replace or recreate it blindly.")

    for executable in ("git", "codex"):
        found = bool(lookup(executable))
        add(executable + "-executable", "available" if found else "missing", f"{executable} is " + ("present on PATH; it was not executed." if found else "not present on PATH. It is optional for the current conversational session."))
    git_present = os.path.lexists(root / ".git")
    add("git-project", "present" if git_present else "missing", "Git metadata entry " + ("is present; HEAD, worktree cleanliness and effective ignore rules remain untested." if git_present else "is absent. Native task execution requires a clean committed Git project."))
    try:
        ignore = _regular_file(root, ".gitignore").read_text(encoding="utf-8")
        rule_present = any(line.strip() in ("/.workflow-state/", ".workflow-state/") for line in ignore.splitlines())
        add("runtime-ignore", "present" if rule_present else "missing", "Runtime ignore rule " + ("is present; later negation or Git configuration can change its effective behavior, which the runner checks." if rule_present else "is missing; native run state must be ignored before execution."))
    except (WorkflowError, OSError, UnicodeError):
        add("runtime-ignore", "missing", "No readable runtime ignore rule was found; current-session consultation can still begin.")
    try:
        _regular_file(root, prefix + "scripts/codex_hooks.py")
        hook_detail = "Handler is present. Selected-client support, configuration, trust and event delivery have not been tested."
    except (WorkflowError, OSError):
        hook_detail = "Optional hook handler is absent. Use explicit context and validation commands."
    add("native-hooks", "not-tested", hook_detail)
    add("aws-plugins", "not-tested", "Official plugin availability, installation, loading and public-call behavior were not inspected. No account or credential operation was performed.")
    ready = all(item["status"] == "ready" for item in checks if item["required"])
    return {
        "schema_version": 1, "layout": kind, "status": "ready" if ready else "needs-attention",
        "session_ready": ready, "active_work": active, "checks": checks,
        "next_action": ("Resume the selected work with context --compact." if active else "Read the mapped brief/handoff and describe the project goal to begin consultation.") if ready else "Resolve required local setup findings; optional native or AWS findings do not prevent consultation.",
        "limits": "File inspection and executable presence only; no subprocess, login/auth probe, model call, native trust change, plugin installation or AWS access.",
    }


def hook_preview(root):
    """Return a POSIX/Git hook proposal; never write configuration or trust it."""
    root = _root(root)
    kind, prefix, _ = _layout(root)
    if kind == "uninstalled":
        raise WorkflowError("Install the workflow before preparing its hook configuration.")
    _regular_file(root, prefix + "scripts/codex_hooks.py")
    command = 'python3 "$(git rev-parse --show-toplevel)/' + prefix + 'scripts/codex_hooks.py"'
    startup = {"type": "command", "command": command, "timeout": 5, "statusMessage": "Loading project consultation context", "additionalContextLimit": 2500}
    prompt = {"type": "command", "command": command, "timeout": 5, "statusMessage": "Refreshing project consultation context", "additionalContextLimit": 1000}
    stop = {"type": "command", "command": command, "timeout": 5, "statusMessage": "Checking recorded completion claims"}
    configuration = {"description": "Read-only project consultation context and completion reminders", "hooks": {
        "SessionStart": [{"matcher": "^(startup|resume|clear|compact|fork)$", "hooks": [startup]}],
        "UserPromptSubmit": [{"hooks": [prompt]}], "Stop": [{"hooks": [stop]}],
    }}
    existing_status = "absent"
    existing = safe_path(root, ".codex/hooks.json")
    if existing.exists():
        try:
            current = _json(root, ".codex/hooks.json")
            existing_status = "equivalent" if current.get("hooks") == configuration["hooks"] else "merge-required"
        except WorkflowError:
            existing_status = "invalid"
    return {
        "schema_version": 1, "status": "preview", "layout": kind,
        "target": ".codex/hooks.json", "existing_configuration": existing_status,
        "configuration": configuration,
        "next_action": "Review and merge only missing definitions into the selected client's chosen configuration source, then use its supported trust flow. Existing equivalent definitions must not be duplicated.",
        "requirements": ["Supported native hook surface", "POSIX shell with python3 and Git", "Git checkout, or a separately reviewed platform-specific absolute command", "Actual client review/trust and observed event test"],
        "limits": "Preview only. No file, registration, client setting, plugin or trust state was changed. Other configuration sources were not inspected.",
    }
