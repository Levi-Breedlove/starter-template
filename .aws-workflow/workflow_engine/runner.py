"""Bounded foreground task execution in isolated Git worktrees.

Planning is read-only. Native model execution requires an explicit execute=True.
Worker claims are checked against changed paths and independent local commands;
the canonical task ledger is updated only in the separate candidate worktree.
This controller is not a sandbox, an authority source, or a background service.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import signal
import subprocess
import tempfile
import time
import uuid

from .engine import WorkflowError, atomic_json, digest_file, inspect_work, record_evidence, safe_path


STATE = ".workflow-state"
MAX_OUTPUT = 2_000_000
MAX_PATCH = 8_000_000
RUN_ID = re.compile(r"[a-z0-9][a-z0-9-]{0,79}\Z")
DEADLINE = ContextVar("workflow_execution_deadline", default=None)
RESULT_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["task_id", "status", "summary", "acceptance"],
    "properties": {
        "task_id": {"type": "string"},
        "status": {"type": "string", "enum": ["ready", "blocked"]},
        "summary": {"type": "string"},
        "acceptance": {"type": "string", "enum": ["satisfied", "not-established"]},
    },
}


class _UnknownOperation(WorkflowError):
    """A bounded process stopped around a mutation; its actual outcome needs inspection."""


def _time_left(limit):
    deadline = DEADLINE.get()
    value = min(limit, deadline - time.monotonic()) if deadline is not None else limit
    if value <= 0:
        raise WorkflowError("The total run deadline is exhausted; no further operation was dispatched.")
    return value


@contextmanager
def _deadline(at):
    token = DEADLINE.set(at)
    try:
        yield
    finally:
        DEADLINE.reset(token)


def _now():
    return datetime.now(timezone.utc).isoformat()


def _json(path):
    if not path.is_file() or path.stat().st_size > MAX_OUTPUT:
        raise WorkflowError(f"Missing or oversized JSON record: {path.name}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError, OSError) as exc:
        raise WorkflowError(f"Cannot read {path.name}: {exc}") from exc
    if not isinstance(value, dict):
        raise WorkflowError(f"{path.name} must contain an object.")
    return value


def _relative(root, value, *, directory=False):
    if not isinstance(value, str) or not value or any(ord(c) < 32 for c in value):
        raise WorkflowError("Execution paths must be nonempty, portable relative paths.")
    raw = value[:-1] if directory and value.endswith("/") else value
    path = safe_path(root, raw)
    if any(c in raw for c in "*?[") or raw.endswith("/"):
        raise WorkflowError("Execution paths use exact files or directory prefixes, not globs.")
    return raw + ("/" if directory and value.endswith("/") else ""), path


def _scope(root, value):
    name, path = _relative(root, value, directory=True)
    first = name.rstrip("/").split("/")[0]
    if first in {".git", STATE, ".aws-workflow", ".codex", "specs", "evidence"} or name == "AGENTS.md":
        raise WorkflowError(f"Workers cannot own workflow/control records: {name}")
    if path.is_dir() and not name.endswith("/"):
        raise WorkflowError("A directory write scope must end with '/'.")
    return name


def _matches(path, scopes):
    return any(path == scope or scope.endswith("/") and path.startswith(scope) for scope in scopes)


def _overlap(left, right):
    return any(a == b or a.endswith("/") and b.startswith(a) or b.endswith("/") and a.startswith(b)
               for a in left for b in right)


def _git(root, *args, data=None):
    timeout = _time_left(30)
    try:
        with tempfile.TemporaryFile() as incoming, tempfile.TemporaryFile() as outgoing, tempfile.TemporaryFile() as errors:
            if data is not None:
                incoming.write(data)
                incoming.seek(0)
            process = subprocess.Popen(["git", "-C", str(root), *args], stdin=incoming, stdout=outgoing, stderr=errors,
                                       start_new_session=os.name == "posix", env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})
            started, reason = time.monotonic(), None
            try:
                while process.poll() is None:
                    if time.monotonic() - started >= timeout:
                        reason = "timeout"
                        _terminate(process)
                    elif os.fstat(outgoing.fileno()).st_size + os.fstat(errors.fileno()).st_size > MAX_PATCH:
                        reason = "output-limit"
                        _terminate(process)
                    else:
                        time.sleep(0.01)
            finally:
                if _terminate(process) and reason is None:
                    reason = "descendants-active"
            outgoing.seek(0)
            errors.seek(0)
            output, diagnostic = outgoing.read(MAX_PATCH + 1), errors.read(MAX_PATCH + 1)
            if reason or len(output) + len(diagnostic) > MAX_PATCH:
                raise _UnknownOperation(f"Git operation stopped with {reason or 'output-limit'}; inspect its actual state before retrying.")
            if process.returncode:
                raise WorkflowError("Git operation failed: " + diagnostic.decode(errors="replace")[:1500].strip())
            return output
    except OSError as exc:
        raise WorkflowError(f"Git operation unavailable: {exc}") from exc


def _head(root):
    return _git(root, "rev-parse", "HEAD").decode().strip()


def _status(root):
    return _git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")


def _git_preflight(root):
    top = _git(root, "rev-parse", "--show-toplevel").decode().strip()
    if Path(top).resolve() != root:
        raise WorkflowError("Execution requires the application's Git root as --root.")
    head = _head(root)
    if _status(root):
        raise WorkflowError("Execution requires a clean committed application; preserve and commit/reconcile existing work first.")
    try:
        _git(root, "check-ignore", "--quiet", f"{STATE}/probe")
    except WorkflowError as exc:
        raise WorkflowError(f"Add {STATE}/ to the project's ignored paths before execution.") from exc
    return head


def execution_template(root, work_id=None):
    """Return an unexecutable draft; never guess commands, authority, or scopes."""
    report = inspect_work(root, work_id)
    return {
        "schema_version": 1, "authority_ref": "",
        "limits": {"max_workers": 1, "max_tasks": 20, "timeout_seconds": 1800, "check_timeout_seconds": 120},
        "tasks": {task["id"]: {"write_paths": [], "checks": [
            {"id": check, "argv": [], "inputs": []} for check in task["checks"]]}
            for task in report["tasks"]},
        "integration_checks": [{"name": "integrated-candidate", "argv": [], "inputs": []}],
    }


def _check_config(root, config, report, selected):
    if config.get("schema_version") != 1 or set(config) - {"schema_version", "authority_ref", "limits", "tasks", "integration_checks"}:
        raise WorkflowError("execution.json needs schema_version 1 and only documented fields.")
    _, authority = _relative(root, config.get("authority_ref"))
    if not authority.is_file() or not authority.read_text(encoding="utf-8").strip():
        raise WorkflowError("authority_ref must identify an existing nonempty decision record; it cannot grant authority.")
    limits = config.get("limits")
    ranges = {"max_workers": (1, 4), "max_tasks": (1, 100), "timeout_seconds": (1, 7200), "check_timeout_seconds": (1, 600)}
    if not isinstance(limits, dict) or set(limits) != set(ranges):
        raise WorkflowError("Execution limits must explicitly name max_workers, max_tasks, timeout_seconds and check_timeout_seconds.")
    for key, (low, high) in ranges.items():
        if type(limits[key]) is not int or not low <= limits[key] <= high:
            raise WorkflowError(f"{key} must be an integer from {low} to {high}.")
    if len(selected) > limits["max_tasks"]:
        raise WorkflowError("Selected task count exceeds the explicit total run limit.")
    tasks = config.get("tasks")
    if not isinstance(tasks, dict) or set(tasks) - {t["id"] for t in report["tasks"]}:
        raise WorkflowError("Execution task mappings must name existing canonical tasks.")
    used_checks = set()

    def validate_check(item, key):
        if not isinstance(item, dict) or set(item) != {key, "argv", "inputs"} or not isinstance(item.get(key), str) or not item[key].strip():
            raise WorkflowError("Each check needs exactly its id/name, argv and inputs.")
        argv, inputs = item["argv"], item["inputs"]
        if not isinstance(argv, list) or not argv or any(not isinstance(arg, str) or not arg or "\0" in arg for arg in argv):
            raise WorkflowError("Checks require a nonempty argv array; no shell command string or guessed command.")
        if not isinstance(inputs, list) or not inputs or len(set(inputs)) != len(inputs):
            raise WorkflowError("Checks must declare distinct actual input files/directories.")
        for value in inputs:
            _relative(root, value, directory=True)

    validation_tasks = [task for task in report["tasks"] if task["completion_valid"] or task in selected]
    for task in validation_tasks:
        entry = tasks.get(task["id"])
        if not isinstance(entry, dict) or set(entry) != {"write_paths", "checks"}:
            raise WorkflowError(f"{task['id']} needs write_paths and checks in execution.json.")
        scopes = entry["write_paths"]
        if not isinstance(scopes, list) or not scopes or len(set(scopes)) != len(scopes):
            raise WorkflowError(f"{task['id']} needs distinct explicit write scopes.")
        for value in scopes:
            _scope(root, value)
        checks = entry["checks"]
        if not isinstance(checks, list):
            raise WorkflowError("Task checks must be an array.")
        for check in checks:
            validate_check(check, "id")
            if check["id"] in used_checks:
                raise WorkflowError("Automated tasks need distinct check IDs; keep shared checks as integration checks.")
            used_checks.add(check["id"])
        if {c["id"] for c in checks} != set(task["checks"]):
            raise WorkflowError(f"{task['id']} execution checks must exactly cover its canonical checks.")
    integration = config.get("integration_checks")
    if not isinstance(integration, list) or not integration:
        raise WorkflowError("At least one explicit integrated-candidate check is required.")
    names = set()
    for check in integration:
        validate_check(check, "name")
        if check["name"] in names:
            raise WorkflowError("Integration check names must be unique.")
        names.add(check["name"])


def plan_run(root, work_id=None, task_id=None):
    """Inspect tasks/config and compute waves, without writes or model calls."""
    root = Path(root).resolve()
    report = inspect_work(root, work_id)
    config_path = safe_path(root, f"specs/{report['id']}/execution.json")
    config = _json(config_path)
    tasks = {task["id"]: task for task in report["tasks"]}
    if task_id is not None and task_id not in tasks:
        raise WorkflowError(f"Unknown canonical task: {task_id}")
    selected = [task for task in report["tasks"] if not task["completion_valid"] and (task_id is None or task["id"] == task_id)]
    _check_config(root, config, report, selected)
    blockers = [item["message"] for item in report["issues"] if item["severity"] == "error"]
    if report["phase"] not in ("implementation", "verification"):
        blockers.append("Enter the reviewed implementation/verification phase before executing tasks.")
    blockers += [f"{q['id']} blocks {report['phase']}." for q in report["open_questions"] if report["phase"] in q.get("blocks", [])]
    blockers += [f"{task['id']}: {task['blocked_reason']}" for task in selected if task["blocked_reason"]]
    done = {task["id"] for task in report["tasks"] if task["completion_valid"]}
    pending = {task["id"]: task for task in selected}
    waves = []
    while pending:
        wave, scopes = [], []
        for key, task in pending.items():
            own = config["tasks"][key]["write_paths"]
            if set(task["dependencies"]) <= done and not _overlap(scopes, own) and len(wave) < config["limits"]["max_workers"]:
                wave.append(key)
                scopes.extend(own)
        if not wave:
            blockers.append("Selected tasks have unresolved prerequisites: " + ", ".join(pending))
            break
        waves.append(wave)
        done.update(wave)
        for key in wave:
            del pending[key]
    head = None
    try:
        head = _git_preflight(root)
    except WorkflowError as exc:
        blockers.append(str(exc))
    return {"schema_version": 1, "work_id": report["id"], "task_id": task_id,
            "base_commit": head, "configuration": config_path.relative_to(root).as_posix(),
            "configuration_sha256": digest_file(config_path), "authority_ref": config["authority_ref"],
            "waves": waves, "selected_tasks": [task["id"] for task in selected],
            "limits": config["limits"], "ready": bool(selected) and not blockers,
            "blockers": blockers, "mode": "preview", "model_calls": 0,
            "note": "A plan is not execution, verified authority, or a security boundary."}


def _run_dir(root, run_id):
    if not isinstance(run_id, str) or not RUN_ID.fullmatch(run_id):
        raise WorkflowError("Run IDs use lowercase letters, digits and hyphens, up to 80 characters.")
    return safe_path(root, f"{STATE}/runs/{run_id}")


def _owner():
    value = {"pid": os.getpid()}
    stat = Path(f"/proc/{os.getpid()}/stat")
    if stat.is_file():
        value["process_start"] = stat.read_text().rsplit(")", 1)[1].split()[19]
    return value


def _alive(owner):
    try:
        pid = int(owner["pid"])
        os.kill(pid, 0)
        if "process_start" in owner:
            return Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[19] == owner["process_start"]
        return True
    except (OSError, ValueError, KeyError, IndexError):
        return False


def inspect_run(root, run_id):
    root = Path(root).resolve()
    record = _json(_run_dir(root, run_id) / "run.json")
    record["effective_status"] = "unknown" if record.get("status") in ("running", "applying") and not _alive(record.get("owner", {})) else record.get("status")
    record["candidate_path"] = str(_run_dir(root, run_id) / "candidate")
    return record


@contextmanager
def _lock(root, run_id):
    path = safe_path(root, f"{STATE}/execution.lock")
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8") as stream:
            json.dump({"run_id": run_id, "owner": _owner()}, stream)
    except FileExistsError as exc:
        raise WorkflowError("Another run owns the execution lock; inspect it and reconcile/abandon an interrupted run explicitly.") from exc
    try:
        yield
    finally:
        path.unlink(missing_ok=True)


def _group_live_members(group):
    """Distinguish Linux zombie-only groups from processes that can still act.

    A successful killpg alone is insufficient: an exited child's zombie can
    keep its group visible until its new parent reaps it. Other POSIX systems
    retain the conservative unknown result rather than assuming quiescence.
    """
    proc = Path("/proc")
    if not proc.is_dir():
        return None
    found, uncertain = False, False
    try:
        entries = list(proc.iterdir())
    except OSError:
        return None
    for entry in entries:
        if not entry.name.isdigit():
            continue
        try:
            fields = (entry / "stat").read_text().rsplit(")", 1)[1].split()
            if int(fields[2]) == group:
                found = True
                if fields[0] not in {"Z", "X"}:
                    return True
        except FileNotFoundError:
            continue  # A process can disappear between enumeration and read.
        except (OSError, ValueError, IndexError):
            uncertain = True
    return False if found and not uncertain else None


def _terminate(process):
    killed = False
    if os.name == "posix":
        live = True if process.poll() is None else _group_live_members(process.pid)
        try:
            os.killpg(process.pid, signal.SIGKILL)
            killed = live is not False
        except ProcessLookupError:
            pass
    elif process.poll() is None:
        process.kill()
        killed = True
    if process.poll() is None:
        process.wait()
    return killed


def _process(argv, cwd, timeout, output, prompt=None):
    """Bound time/output; argv is never interpreted through a shell."""
    timeout = _time_left(timeout)
    start = time.monotonic()
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as stream, tempfile.TemporaryFile() as incoming:
        if prompt is not None:
            incoming.write(prompt.encode())
            incoming.seek(0)
        try:
            process = subprocess.Popen(argv, cwd=cwd, stdin=incoming if prompt is not None else subprocess.DEVNULL,
                                       stdout=stream, stderr=subprocess.STDOUT, start_new_session=os.name == "posix")
        except OSError as exc:
            raise WorkflowError(f"Cannot start executable {argv[0]!r}: {exc}") from exc
        reason = None
        try:
            while process.poll() is None:
                if time.monotonic() - start >= timeout:
                    reason = "timeout"
                    _terminate(process)
                elif output.stat().st_size > MAX_OUTPUT:
                    reason = "output-limit"
                    _terminate(process)
                else:
                    time.sleep(0.02)
        finally:
            if _terminate(process) and reason is None:
                reason = "descendants-active"
    if output.stat().st_size > MAX_OUTPUT:
        reason = "output-limit"
        with output.open("r+b") as stream:
            stream.truncate(MAX_OUTPUT)
    return {"returncode": process.returncode, "termination": reason,
            "elapsed_seconds": round(time.monotonic() - start, 3), "output_sha256": digest_file(output)}


class CodexBackend:
    """The opt-in native adapter; constructing it performs no operation."""

    def __init__(self, executable="codex"):
        self.executable = executable

    def __call__(self, request):
        if os.name != "posix":
            raise WorkflowError("Bounded native execution requires a POSIX process-group environment; use WSL or the session-driven workflow on this platform.")
        directory = Path(request["attempt_directory"])
        schema, result = directory / "result-schema.json", directory / "result.json"
        atomic_json(schema, RESULT_SCHEMA)
        observed = _process([self.executable, "exec", "--json", "--sandbox", "workspace-write", "--cd", request["workspace"],
                             "--output-schema", str(schema), "--output-last-message", str(result), "-"],
                            request["workspace"], request["timeout_seconds"], directory / "model-events.log", request["prompt"])
        if observed["returncode"] or observed["termination"]:
            raise _UnknownOperation(f"Model process did not complete: {observed}")
        return _json(result)


def _worker_result(result, task_id):
    if not isinstance(result, dict) or set(result) != {"task_id", "status", "summary", "acceptance"}:
        raise WorkflowError("Worker returned an invalid result shape.")
    if result["task_id"] != task_id or result["status"] not in ("ready", "blocked") or result["acceptance"] not in ("satisfied", "not-established"):
        raise WorkflowError("Worker result does not identify this task and its actual disposition.")
    if not isinstance(result["summary"], str) or not result["summary"].strip() or len(result["summary"]) > 8000:
        raise WorkflowError("Worker result needs a bounded, nonempty summary.")
    if result["status"] == "ready" and result["acceptance"] != "satisfied":
        raise WorkflowError("Worker cannot request integration without an explicit author acceptance assessment.")
    return result


def _input_hashes(root, values):
    found = {}
    for value in values:
        _, path = _relative(root, value, directory=True)
        candidates = [root / item.decode("utf-8") for item in _git(root, "ls-files", "-z", "--", value.rstrip("/")).split(b"\0") if item] if path.is_dir() else [path]
        for candidate in candidates:
            relative = candidate.relative_to(root).as_posix()
            safe_path(root, relative)
            if candidate.is_file():
                found[relative] = digest_file(candidate)
        if not path.exists():
            raise WorkflowError(f"Verification input is missing: {value}")
    if not found:
        raise WorkflowError("Verification inputs contain no regular files.")
    return found


def _worker(root, run_directory, candidate_commit, task, config, backend, deadline):
    with _deadline(deadline):
        return _worker_body(root, run_directory, candidate_commit, task, config, backend)


def _worker_body(root, run_directory, candidate_commit, task, config, backend):
    task_id = task["id"]
    directory = run_directory / "attempts" / task_id
    directory.mkdir(parents=True)
    workspace = directory / "workspace"
    _git(root, "worktree", "add", "--detach", str(workspace), candidate_commit)
    metadata = digest_file(workspace / ".git")
    instruction = (
        f"Implement only canonical task {task_id} in work {config['work_id']}. Read AGENTS.md and the canonical "
        "requirements/bugfix, design and tasks first. Preserve all accepted constraints. Your authorized write paths are "
        + json.dumps(config["task"]["write_paths"]) + ". Do not edit workflow records, task checkboxes, evidence, Git metadata, "
        "client configuration or other files. Do not commit, deploy, inspect AWS accounts, install plugins, change trust, "
        "or start nested workers. Local implementation only. Run useful permitted checks. Report an honest author "
        "assessment: ready/satisfied only when the task's acceptance is achieved; otherwise blocked/not-established. "
        "The controller independently runs the reviewed configured checks. Never describe this author assessment as independent review."
    )
    request = {"task_id": task_id, "workspace": str(workspace), "attempt_directory": str(directory),
               "timeout_seconds": _time_left(7200), "prompt": instruction, "task": task, "configuration": config["task"]}
    result = _worker_result(backend(request), task_id)
    atomic_json(directory / "worker-result.json", result)
    if digest_file(workspace / ".git") != metadata or _head(workspace) != candidate_commit:
        raise WorkflowError(f"{task_id}: worker changed Git control state.")
    if result["status"] != "ready":
        raise WorkflowError(f"{task_id}: worker reported blocked: {result['summary']}")
    changed = _git(workspace, "diff", "--name-only", "-z", "HEAD").split(b"\0")
    changed += _git(workspace, "ls-files", "--others", "--exclude-standard", "-z").split(b"\0")
    names = sorted({value.decode("utf-8") for value in changed if value})
    for name in names:
        safe_path(workspace, name)
        if not _matches(name, config["task"]["write_paths"]):
            raise WorkflowError(f"{task_id}: write outside declared scope: {name}")
    _git(workspace, "add", "--all")
    modes = _git(workspace, "diff", "--cached", "--raw", "HEAD").decode()
    if "120000" in modes or "160000" in modes:
        raise WorkflowError("Automated workers cannot introduce symlinks or submodules.")
    patch = _git(workspace, "diff", "--cached", "--binary", "HEAD")
    if len(patch) > MAX_PATCH:
        raise WorkflowError(f"{task_id}: patch exceeds the bounded integration limit.")
    (directory / "change.patch").write_bytes(patch)
    return {"task_id": task_id, "result": result, "patch": patch, "paths": names}


def _commit(root, message):
    _git(root, "add", "--all")
    expected_tree = _git(root, "write-tree").strip()
    _git(root, "-c", "user.name=Workflow Controller", "-c", "user.email=workflow@local.invalid",
         "commit", "--allow-empty", "-m", message)
    if _git(root, "rev-parse", "HEAD^{tree}").strip() != expected_tree or _status(root):
        raise WorkflowError("A commit hook changed the candidate after verification; inspect and reverify it.")
    return _head(root)


def _mark_complete(candidate, report, task_id):
    path = safe_path(candidate, report["artifacts"]["tasks"])
    text = path.read_text(encoding="utf-8")
    expression = re.compile(r"(^#{2,4}\s+" + re.escape(task_id) + r"(?:\s+[—–-]\s*|\s+).*?)(?=^#{2,4}\s+T-|\Z)", re.M | re.S)
    match = expression.search(text)
    if not match:
        raise WorkflowError(f"Cannot locate canonical task {task_id}.")
    block = match.group(0)
    block, count = re.subn(r"^(\s*-\s+)\[ \](\s+" + re.escape(task_id) + r"\s+complete\.?)\s*$", r"\1[x]\2", block, flags=re.M)
    if count != 1:
        raise WorkflowError("Completion must update exactly one canonical checkbox.")
    if re.search(r"^\s*-\s+Activity:", block, re.M):
        block = re.sub(r"^(\s*-\s+Activity:)\s*.*$", r"\1 complete", block, flags=re.M)
    path.write_text(text[:match.start()] + block + text[match.end():], encoding="utf-8")


def _tree_state(root):
    """Identify tracked/untracked source edits; ignored build output is separate."""
    value = hashlib.sha256(_head(root).encode() + _git(root, "diff", "--binary", "HEAD") + _status(root))
    for item in _git(root, "ls-files", "--others", "--exclude-standard", "-z").split(b"\0"):
        if item:
            path = safe_path(root, item.decode("utf-8"))
            value.update(item)
            value.update(path.read_bytes())
    return value.hexdigest()


def _verify(candidate, check, directory, timeout):
    before = _input_hashes(candidate, check["inputs"])
    source = _tree_state(candidate)
    observation = _process(check["argv"], candidate, timeout, directory)
    after = _input_hashes(candidate, check["inputs"])
    if before != after or source != _tree_state(candidate):
        raise WorkflowError("A verification command changed source or its declared tested inputs.")
    observation.update({"argv": check["argv"], "inputs": before, "observed_at": _now()})
    if observation["returncode"] or observation["termination"]:
        raise WorkflowError(f"Verification failed for {check.get('id', check.get('name'))}: {observation}")
    return observation


def execute_run(root, work_id=None, task_id=None, *, execute=False, backend=None, run_id=None):
    """Run selected tasks in a separate candidate. Default is a pure preview.

    There is one attempt per selected task. Failed/unknown attempts are never
    replayed by this API; inspect the retained candidate and receipts first.
    """
    root = Path(root).resolve()
    plan = plan_run(root, work_id, task_id)
    if not execute:
        return plan
    if not plan["ready"]:
        raise WorkflowError("Execution is blocked: " + "; ".join(plan["blockers"] or ["No unfinished selected task."]))
    # The default native backend must pass the read-only prerequisite check
    # before creating a run record or dispatching a model. Injected test backends
    # are not native launches through the public CLI.
    if backend is None:
        from .native_preflight import inspect_native
        startup = inspect_native()
        if startup["status"] != "no-known-blocker":
            raise WorkflowError("Native startup preflight blocked: " + "; ".join(startup["blockers"]))
        executable = shutil.which("codex")
        if executable is None:
            raise WorkflowError("The selected Codex executable is unavailable before run reservation.")
        backend = CodexBackend(str(Path(executable).absolute()))
    run_id = run_id or datetime.now(timezone.utc).strftime("run-%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:8]
    directory = _run_dir(root, run_id)
    if directory.exists():
        raise WorkflowError("Run ID already exists; inspect it instead of resetting attempts or replaying work.")
    config = _json(safe_path(root, plan["configuration"]))
    started = time.monotonic()
    record = {**plan, "mode": "execution", "run_id": run_id, "status": "running", "owner": _owner(),
              "started_at": _now(), "attempts_started": 0, "completed_tasks": [], "events": [],
              "candidate_commit": None, "backend": "native-codex" if isinstance(backend, CodexBackend) else "injected-backend"}
    record.pop("ready", None)  # Preview eligibility is not execution readiness.
    record["model_calls"] = None if isinstance(backend, CodexBackend) else 0
    record["usage"] = None

    def save(event, **details):
        record["events"].append({"at": _now(), "event": event, **details})
        record["elapsed_seconds"] = round(time.monotonic() - started, 3)
        atomic_json(directory / "run.json", record)

    def remaining():
        value = config["limits"]["timeout_seconds"] - (time.monotonic() - started)
        if value <= 0:
            raise WorkflowError("The persistent total run time budget is exhausted.")
        return value

    with _lock(root, run_id), _deadline(started + config["limits"]["timeout_seconds"]):
        directory.mkdir(parents=True)
        save("intent-recorded")
        candidate = directory / "candidate"
        try:
            if _git_preflight(root) != plan["base_commit"] or digest_file(safe_path(root, plan["configuration"])) != plan["configuration_sha256"]:
                raise WorkflowError("The application candidate or execution policy changed after preview.")
            _git(root, "worktree", "add", "--detach", str(candidate), plan["base_commit"])
            candidate_commit = plan["base_commit"]
            for index, wave in enumerate(plan["waves"], 1):
                current = inspect_work(candidate, plan["work_id"])
                if not set(wave) <= set(current["eligible_tasks"]):
                    raise WorkflowError("The next wave is no longer eligible; reconcile current work and evidence.")
                task_map = {task["id"]: task for task in current["tasks"]}
                record["attempts_started"] += len(wave)
                save("dispatch-intent", wave=index, tasks=wave, candidate=candidate_commit)
                remaining()
                with ThreadPoolExecutor(max_workers=len(wave)) as pool:
                    futures = [pool.submit(_worker, root, directory, candidate_commit, task_map[key],
                                           {"work_id": plan["work_id"], "task": config["tasks"][key]}, backend,
                                           started + config["limits"]["timeout_seconds"]) for key in wave]
                    outcomes = [future.result() for future in futures]
                remaining()
                if _head(candidate) != candidate_commit or _status(candidate):
                    raise WorkflowError("The candidate changed concurrently; no worker patch was integrated.")
                for outcome in outcomes:
                    if outcome["patch"]:
                        _git(candidate, "apply", "--check", "--index", "-", data=outcome["patch"])
                        _git(candidate, "apply", "--index", "-", data=outcome["patch"])
                observations = []
                # Recheck already completed tasks too: later writes may touch an
                # earlier declared input. Do not preserve stale completion.
                verify_ids = [task["id"] for task in current["tasks"] if task["completion_valid"] or task["id"] in wave]
                for key in verify_ids:
                    for check in config["tasks"][key]["checks"]:
                        observation = _verify(candidate, check, directory / "checks" / f"wave-{index}-{key}-{check['id']}.log",
                                              min(remaining(), config["limits"]["check_timeout_seconds"]))
                        observations.append((key, check, observation))
                integrated = []
                for number, check in enumerate(config["integration_checks"]):
                    integrated.append(_verify(candidate, check, directory / "checks" / f"wave-{index}-integration-{number}.log",
                                              min(remaining(), config["limits"]["check_timeout_seconds"])))
                for key, check, observation in observations:
                    receipt = f"evidence/{plan['work_id']}/runs/{run_id}/wave-{index}/{key}-{check['id']}.json"
                    path = safe_path(candidate, receipt)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    payload = {"schema_version": 1, "run_id": run_id, "task_id": key, "check_id": check["id"],
                               "base_candidate": candidate_commit, "observation": observation,
                               "author_acceptance": "Worker reported satisfied; this is not independent review.",
                               "integration_checks": integrated, "execution_policy_sha256": plan["configuration_sha256"]}
                    atomic_json(path, payload)
                    record_evidence(candidate, plan["work_id"], check["id"], receipt, "pass",
                                    "Controller independently executed the exact declared local argv and integrated-candidate checks",
                                    "Isolated local candidate Git worktree", f"Base {candidate_commit} plus recorded tested-input SHA-256 identities",
                                    observation["observed_at"], [*observation["inputs"], plan["configuration"], config["authority_ref"]])
                for outcome in outcomes:
                    _mark_complete(candidate, current, outcome["task_id"])
                checked = inspect_work(candidate, plan["work_id"])
                if any(item["severity"] == "error" for item in checked["issues"]):
                    raise WorkflowError("Integrated candidate does not satisfy the canonical workflow ledger.")
                candidate_commit = _commit(candidate, f"Complete verified workflow tasks: {', '.join(wave)}")
                remaining()
                if _status(candidate) or any(item["severity"] == "error" for item in inspect_work(candidate, plan["work_id"])["issues"]):
                    raise WorkflowError("Commit hooks changed or invalidated the verified candidate; inspect it before continuing.")
                record["completed_tasks"].extend(wave)
                record["candidate_commit"] = candidate_commit
                save("wave-verified", wave=index, tasks=wave, candidate=candidate_commit)
            remaining()
            record["status"] = "ready"
            save("candidate-ready", candidate=record["candidate_commit"])
        except Exception as exc:
            record["status"] = "unknown" if isinstance(exc, _UnknownOperation) else "failed"
            record["failure"] = f"{type(exc).__name__}: {exc}"
            save("stopped", reason=record["failure"])
        except BaseException:
            record["status"] = "unknown"
            save("interrupted", reason="An operation may have completed without a reconciled receipt; do not replay.")
            raise
    return inspect_run(root, run_id)


def apply_run(root, run_id):
    """Explicitly fast-forward an unchanged clean original to a verified candidate."""
    root = Path(root).resolve()
    record = inspect_run(root, run_id)
    if record.get("status") != "ready" or not record.get("candidate_commit"):
        raise WorkflowError("Only a ready, verified candidate may be applied.")
    directory = _run_dir(root, run_id)
    candidate = directory / "candidate"
    with _lock(root, run_id):
        if _git_preflight(root) != record["base_commit"]:
            raise WorkflowError("The original application changed; review and integrate the candidate manually.")
        if _head(candidate) != record["candidate_commit"] or _status(candidate):
            raise WorkflowError("The candidate changed after verification; it must be reverified.")
        report = inspect_work(candidate, record["work_id"])
        valid = {task["id"] for task in report["tasks"] if task["completion_valid"]}
        if any(item["severity"] == "error" for item in report["issues"]) or not set(record["selected_tasks"]) <= valid:
            raise WorkflowError("Candidate evidence is no longer current.")
        additions = _git(root, "diff", "--no-renames", "--diff-filter=A", "--name-only", "-z", record["base_commit"], record["candidate_commit"])
        for value in additions.split(b"\0"):
            if value and safe_path(root, value.decode("utf-8")).exists():
                raise WorkflowError("A newly tracked candidate file would overwrite an existing ignored application file.")
        record.pop("effective_status", None)
        record.pop("candidate_path", None)
        record["status"] = "applying"
        record["owner"] = _owner()
        record["events"].append({"at": _now(), "event": "apply-intent", "base": record["base_commit"], "candidate": record["candidate_commit"]})
        atomic_json(directory / "run.json", record)
        try:
            _git(root, "merge", "--ff-only", "--no-edit", record["candidate_commit"])
            actual_head, clean = _head(root), not bool(_status(root))
            record["status"] = "applied" if actual_head == record["candidate_commit"] and clean else "applied-needs-review"
            record["application"] = {"observed_head": actual_head, "worktree_clean": clean, "observed_at": _now()}
            record["events"].append({"at": _now(), "event": record["status"], **record["application"]})
        except BaseException as exc:
            record["status"] = "application-unknown"
            record["events"].append({"at": _now(), "event": "application-unknown", "reason": f"{type(exc).__name__}: {exc}"})
            atomic_json(directory / "run.json", record)
            raise
        atomic_json(directory / "run.json", record)
    return inspect_run(root, run_id)


def abandon_run(root, run_id, reason):
    """Record explicit reconciliation; retain worktrees and receipts for inspection."""
    root = Path(root).resolve()
    if not isinstance(reason, str) or not reason.strip():
        raise WorkflowError("Abandonment needs the actual inspection/reconciliation reason.")
    record = inspect_run(root, run_id)
    if record.get("status") in ("applied", "applied-needs-review", "applying", "application-unknown"):
        raise WorkflowError("An applied or uncertain application cannot be abandoned or rolled back by this command; inspect the original repository.")
    if record.get("status") == "running" and _alive(record.get("owner", {})):
        raise WorkflowError("The controller is still running; stop it and inspect actual effects first.")
    lock = safe_path(root, f"{STATE}/execution.lock")
    if lock.exists():
        owner = _json(lock)
        if owner.get("run_id") != run_id or _alive(owner.get("owner", {})):
            raise WorkflowError("A live or different run owns the lock.")
        lock.unlink()
    record.pop("effective_status", None)
    record.pop("candidate_path", None)
    record["status"] = "abandoned"
    record["events"].append({"at": _now(), "event": "explicit-abandonment", "reason": reason})
    atomic_json(_run_dir(root, run_id) / "run.json", record)
    return inspect_run(root, run_id)
