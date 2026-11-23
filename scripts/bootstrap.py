#!/usr/bin/env python3
"""Install an additive, offline AWS project workflow. Preview is the default."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import stat
import sys
import tempfile
from urllib.parse import quote, unquote, urlsplit


IDENTITY = "codex-aws-workflow"
NAMESPACE = ".aws-workflow"
MANIFEST = f"{NAMESPACE}/manifest.json"
BEGIN = "<!-- codex-aws-workflow:start -->"
END = "<!-- codex-aws-workflow:end -->"
IGNORE_BEGIN = "# codex-aws-workflow:runtime-start"
IGNORE_END = "# codex-aws-workflow:runtime-end"
IGNORE_BLOCK = f"{IGNORE_BEGIN}\n/.workflow-state/\n{IGNORE_END}"
MAX_FILE_BYTES = 1_048_576
MAX_FILES = 350
DOC_TREES = ("workflows", "templates", "guide", "runbooks", "costs", "security", "infrastructure", "docs/reference", "examples/consultation", "examples/booking-retries")
DOC_FILES = ("docs/workflow-architecture.md", "docs/adapter-contracts.md", "docs/repository-map.md", "specs/README.md", "evidence/README.md", "delivery/README.md", "scripts/README.md", "evaluations/README.md")
SCRIPT_FILES = ("scripts/workflow.py", "scripts/bootstrap.py", "scripts/codex_hooks.py")
REQUIRED = (
    "workflows/consult.md", "workflows/brownfield.md", "workflows/feature.md",
    "workflows/bugfix.md", "workflows/reconcile.md", "templates/project-brief.md",
    "templates/requirements.md", "templates/bugfix.md", "templates/design.md", "templates/tasks.md",
    "guide/00-quickstart.md", "docs/reference/specification-operations.md", "docs/reference/task-execution.md",
    "scripts/workflow.py", "workflow_engine/__init__.py", "workflow_engine/engine.py",
    "workflow_engine/context.py", "workflow_engine/specifications.py", "workflow_engine/runner.py", "workflow_engine/doctor.py",
)
LOGICAL = {
    "brief": "project/brief.md",
    "handoff": "delivery/current-handoff.md",
    "adoption_report": "project/adoption-report.md",
    "environment_capabilities": "delivery/environment-capabilities.md",
}
LINK = re.compile(r"(?<!!)\[([^\]]+)\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)")


class BootstrapError(Exception):
    """A plan cannot safely be applied."""


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def relative_path(value: str) -> str:
    path = PurePosixPath(value)
    if not value or "\\" in value or path.is_absolute() or any(part in (".", "..") for part in value.split("/")):
        raise BootstrapError(f"Expected a contained relative path, received: {value!r}")
    if any(ord(char) < 32 for char in value) or path.parts[0] == ".git":
        raise BootstrapError(f"Reserved or invalid path: {value!r}")
    return path.as_posix()


def no_symlinks(path: Path) -> None:
    for part in (path, *path.parents):
        if part.is_symlink():
            raise BootstrapError(f"Symlink paths are not supported: {part}")


def root_path(value: str | Path) -> Path:
    raw = Path(value).expanduser()
    if ".." in raw.parts:
        raise BootstrapError(f"Use a root path without '..' components: {value}")
    absolute = Path(os.path.abspath(raw))
    no_symlinks(absolute)
    return absolute


def contained(root: Path, relative: str) -> Path:
    path = root / relative_path(relative)
    no_symlinks(path)
    for parent in path.parents:
        if parent == root.parent:
            break
        if parent.exists() and not parent.is_dir():
            raise BootstrapError(f"A file blocks an output directory: {parent}")
    return path


def read_file(path: Path) -> bytes:
    no_symlinks(path)
    if not path.is_file() or not stat.S_ISREG(path.stat().st_mode):
        raise BootstrapError(f"Expected a regular file: {path}")
    if path.stat().st_size > MAX_FILE_BYTES:
        raise BootstrapError(f"File exceeds the {MAX_FILE_BYTES}-byte limit: {path}")
    return path.read_bytes()


def text_file(path: Path) -> str:
    try:
        return read_file(path).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise BootstrapError(f"Expected UTF-8 text: {path}") from exc


def source_assets(source: Path) -> dict[str, bytes]:
    """Select reusable guidance and implementation; never copy active work."""
    assets: dict[str, bytes] = {}

    def inventory_error(error: OSError) -> None:
        raise BootstrapError(f"Cannot completely inventory reusable source: {error}") from error

    for folder in (*DOC_TREES, "workflow_engine"):
        directory = contained(source, folder)
        if not directory.exists():
            continue
        if not directory.is_dir():
            raise BootstrapError(f"Expected source directory: {directory}")
        for current, directories, files in os.walk(directory, followlinks=False, onerror=inventory_error):
            directories[:] = sorted(name for name in directories if name != "__pycache__")
            for name in (*directories, *files):
                no_symlinks(Path(current) / name)
            for name in sorted(files):
                path = Path(current) / name
                accepted = path.suffix == ".py" if folder == "workflow_engine" else path.suffix in (".md", ".json")
                if accepted:
                    assets[path.relative_to(source).as_posix()] = read_file(path)
                    if len(assets) > MAX_FILES:
                        raise BootstrapError("Reusable source exceeds the bounded file limit")
    for relative in (*DOC_FILES, *SCRIPT_FILES):
        path = contained(source, relative)
        if path.exists():
            assets[relative] = read_file(path)
    missing = [name for name in REQUIRED if name not in assets]
    if missing:
        raise BootstrapError("Source is not a complete workflow template; missing: " + ", ".join(missing))
    return assets


def source_digest(assets: dict[str, bytes]) -> str:
    return digest("\n".join(f"{path}\0{digest(content)}" for path, content in sorted(assets.items())).encode())


def local_link(path: str) -> str:
    label = path.replace("[", "\\[").replace("]", "\\]")
    return f"[{label}]({quote(path, safe='/._-')})"


def rewrite_links(content: str, original: str, output: str, mapping: dict[str, str], omitted: set[str]) -> str:
    """Remap selected local links; excluded maintenance references become prose."""
    def replace(match: re.Match[str]) -> str:
        label, reference = match.groups()
        parts = urlsplit(reference)
        if parts.scheme or parts.netloc or not parts.path:
            return match.group(0)
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(original), unquote(parts.path)))
        destination = mapping.get(resolved)
        if destination is None:
            omitted.add(f"{original}: {reference}")
            return f"{label} (template reference omitted)"
        rewritten = quote(posixpath.relpath(destination, posixpath.dirname(output)), safe="/._-")
        if parts.fragment:
            rewritten += "#" + parts.fragment
        return f"[{label}]({rewritten})"

    rewritten = LINK.sub(replace, content)
    # The CLI resolves application state from --root / cwd, never its own package.
    return re.sub(r"(?<![\w/.-])scripts/(workflow|codex_hooks)\.py", rf"{NAMESPACE}/scripts/\1.py", rewritten)


def agent_block(paths: dict[str, str], authorities: list[str]) -> str:
    established = ", ".join(f"`{path}`" for path in authorities) or "the repository's existing instructions, design, and task authorities"
    return f"""{BEGIN}
## AWS project consultation and delivery

Read {local_link(MANIFEST)} for this project's actual context paths. Start with
{local_link(paths['brief'])} and {local_link(paths['handoff'])};
inspect the current repository before making architectural recommendations.
Preserve {established}. This additive workflow does not replace existing scoped
instructions, architecture, IaC ownership, delivery controls, or task authority.

Use [{NAMESPACE}/workflows/consult.md]({NAMESPACE}/workflows/consult.md) to guide the
user as an AWS consultant. Infer established answers from the repository and
conversation. Ask only the next one to three material questions, explain a
recommendation and its tradeoffs, and persist the answers and unresolved choices.
For existing applications, establish the preserved baseline through
[{NAMESPACE}/workflows/brownfield.md]({NAMESPACE}/workflows/brownfield.md) first.
Select the appropriate requirements-first, design-first, quick, bugfix, or plan
route; prepare requirements, design, traceable tasks, and verification according
to that route and authority already granted. Do not make the user design the
system through a questionnaire or create fictional approvals or test results.

Reusable guidance is under `{NAMESPACE}/`. Project files are identified by the
manifest; prose paths such as `project/brief.md` are logical defaults resolved
through that map. Work specifications belong to this application's selected
authority. The optional structured CLI uses application-root `specs/<work-id>/`;
map any existing authority during intake before adopting its metadata. It never
imports an existing backlog or marks tasks complete automatically.

Before selecting active work, consult the mapped brief/handoff and lead the
conversation. Run `python3 {NAMESPACE}/scripts/workflow.py --root . doctor` for
read-only local setup findings; missing active work is normal before consultation.
Use the packaged tooling reference when a concrete work item is
ready for `new --activate`. After that selection, run
`python3 {NAMESPACE}/scripts/workflow.py --root . context --compact` from this application
root to resume structured work. No active work was created by adoption. Keep one
canonical task completion record, preserve accepted decisions, and record current
evidence and the next action at the mapped handoff path.

Use the packaged specification operations to analyze requirements, derive
correctness properties, and reconcile changed work. Distinguish deterministic
diagnostics from the semantic review you actually perform. For task execution,
the current session can implement eligible tasks directly. The separate native
runner previews work by default and requires explicit execution authority,
reviewed commands and limits before any additional model process is started.

Use the smallest workflow depth that establishes the required outcome. Reuse
loaded facts and sources while their content and scope remain current; load only
additional references needed for the next task. A matching context fingerprint
does not establish that unread files or external state are unchanged. Current
user steering takes precedence. Delegate bounded independent work only when it
improves quality or elapsed time, with clear ownership and concise findings.
Run affected checks and required integration gates; repeat for changed inputs,
reproduced failures or a required gate. Stop optional work once sufficient
evidence exists. Compare efficiency only after correctness, preservation and
authority requirements pass; report actual measurements and unknown usage.

For AWS, use the existing official hosted AWS Core / AWS Data Analytics plugins
when relevant and available, and current official public documentation. Honor
skill opt-outs. Distinguish installed, available, loaded, and tested capabilities.
Public guidance checks must not touch AWS accounts, credentials, or resources.
Account operations, deployment, cost, and destructive actions require actual
task authority and project limits. Adoption grants none of these permissions.
Do not duplicate plugins, install skills, enable hooks, or change client trust
as a side effect of this repository's instructions.
{END}"""


def initial_records(name: str, mode: str, paths: dict[str, str], authorities: list[str]) -> dict[str, bytes]:
    authority_text = ", ".join(f"`{path}`" for path in authorities) or "Inspect the repository and record existing authorities before selecting new ones."
    return {
        paths["brief"]: f"""# Project brief: {name}

**State:** Consultation has not started. **Entry mode:** {mode}.

## Outcome and scope

Establish the intended users, first useful result, observable success, and scope
from the user's request and existing evidence. No application requirements,
architecture, AWS account, region, budget, or deployment authority are assumed.

## Established facts and decisions

The reusable workflow was adopted locally. Existing authority: {authority_text}
Inspect source, instructions, architecture, IaC ownership, tests, and delivery
controls before recommendations. Preserve accepted choices in existing projects.

## Consultation record

Record known facts with sources, each material question and answer, consultant
recommendations, accepted decisions, assumptions, and unresolved blockers.
Ask one to three next questions after reading available context.

## First delivery and verification

No application work item or active backlog has been selected. Prepare the first
reviewable scope and route; continue implementation only within actual task
authority. Establish acceptance criteria and the evidence required to verify them.
""".encode(),
        paths["handoff"]: f"""# Current handoff: {name}

**State:** Local workflow adopted; application consultation is next.
**Entry mode:** {mode}. No active application specification was created.

Read `{paths['brief']}` and `.aws-workflow/manifest.json`, inspect the repository,
then guide the next material consultation questions. For an existing system,
record its baseline and preservation obligations first.

No application implementation, tests, AWS calls, deployments, plugin setup,
hook activation, or trust changes have been performed by the bootstrap helper.
Update this record with actual authority, selected work, evidence, open questions,
and a concrete next action as work proceeds.
""".encode(),
        paths["adoption_report"]: f"""# Adoption assessment: {name}

**Entry mode:** {mode}. **State:** Additive files installed; assessment pending.

Existing files were preserved. Appending the managed root instruction block does
not establish compatibility with all existing instructions or approve an
architecture, migration, tracker conversion, or AWS operation.

## Repository baseline

Record the inspected revision/worktree, source layout, instruction hierarchy,
application architecture, tests, delivery pipeline, and IaC/state ownership.
Distinguish repository evidence from live AWS state; no account inventory is implied.

## Existing authority and preservation obligations

{authority_text}

Map requirement, design, task, evidence, and decision locations before creating
new work. Use one canonical backlog and record any required agent-assisted merge
for explicit review. Existing architecture and operational controls remain authoritative.

## First bounded change

Record the chosen outcome, preserved behavior, verification, open decisions,
and any remaining adoption gaps. Do not import or migrate infrastructure here.
""".encode(),
        paths["environment_capabilities"]: f"""# Environment capabilities: {name}

**State:** Not assessed. The bootstrap helper uses only local Python file I/O.

Record available Codex surface/version, repository access, local verification
commands, and capability evidence when observed. Distinguish installed, available,
loaded, and tested plugins. Public documentation checks do not need account access.

No AWS credentials, accounts, permissions, regions, resources, deployment access,
native hooks, or model orchestration are configured or tested by adoption.
Preserve existing `.codex` configuration and check supported setup documentation
before a separately authorized capability change.
""".encode(),
    }


@dataclass
class Write:
    relative: str
    content: bytes
    before: bytes | None = None


@dataclass
class Plan:
    target: Path
    writes: list[Write] = field(default_factory=list)
    preserved: list[str] = field(default_factory=list)
    omitted_references: list[str] = field(default_factory=list)
    paths: dict[str, str] = field(default_factory=dict)
    mode: str = ""

    def summary(self, applied: bool = False) -> dict[str, object]:
        return {
            "status": "applied" if applied and self.writes else "unchanged" if not self.writes else "preview",
            "target": str(self.target), "mode": self.mode,
            "changes": [{"path": write.relative, "action": ("append managed runtime ignore" if write.relative == ".gitignore" else "append managed instructions") if write.before is not None else "create"} for write in self.writes],
            "preserved": sorted(self.preserved), "paths": self.paths,
            "omitted_template_references": self.omitted_references,
        }


def build_plan(source: str | Path, target: str | Path, mode: str, name: str | None = None,
               brief: str | None = None, handoff: str | None = None, authorities: list[str] | None = None) -> Plan:
    source, target = root_path(source), root_path(target)
    if source == target or source in target.parents or target in source.parents:
        raise BootstrapError("Source and target must be separate, non-overlapping roots")
    if not source.is_dir():
        raise BootstrapError("Source must be an existing workflow template directory")
    if mode not in ("greenfield", "brownfield"):
        raise BootstrapError("Mode must be greenfield or brownfield")
    if target.exists() and not target.is_dir():
        raise BootstrapError("Target must be a directory")
    if not target.exists() and (mode == "brownfield" or not target.parent.is_dir()):
        raise BootstrapError("Brownfield needs an existing target; a new target needs an existing parent directory")
    manifest_path = contained(target, MANIFEST)
    old: dict = {}
    if manifest_path.exists():
        try:
            old = json.loads(text_file(manifest_path))
        except (json.JSONDecodeError, TypeError) as exc:
            raise BootstrapError("Existing installation manifest is invalid; review it manually") from exc
        if not isinstance(old, dict) or old.get("identity") != IDENTITY or old.get("schema_version") != 1:
            raise BootstrapError("Existing namespace belongs to an unknown installation")
    elif contained(target, NAMESPACE).exists():
        raise BootstrapError("Reserved .aws-workflow namespace already exists without an installation manifest")
    if mode == "greenfield" and target.exists() and not old:
        existing = [path.name for path in target.iterdir() if path.name != ".git"]
        if existing:
            raise BootstrapError("Greenfield target is not empty; use brownfield to preserve and adopt an existing application")
    project_name = name or old.get("project_name") or target.name
    if not isinstance(project_name, str) or not project_name.strip() or any(ord(char) < 32 for char in project_name) or len(project_name) > 200:
        raise BootstrapError("Project name must be a short single-line string")
    paths = {}
    persisted = old.get("paths", {})
    if not isinstance(persisted, dict):
        raise BootstrapError("Installation path map must be an object")
    for key, logical in LOGICAL.items():
        requested = {"brief": brief, "handoff": handoff}.get(key)
        mapped = requested or persisted.get(key) or (logical if contained(target, logical).exists() else f"{NAMESPACE}/{logical}")
        if not isinstance(mapped, str):
            raise BootstrapError("Installation paths must be strings")
        paths[key] = relative_path(mapped)
        if requested and not contained(target, mapped).is_file():
            raise BootstrapError(f"Mapped existing {key} must be a regular file: {mapped}")
    if len(set(paths.values())) != len(paths):
        raise BootstrapError("Each project record needs a distinct path")
    paths.update({"specifications": "specs", "evidence": "evidence", "decisions": "docs/decisions"})
    established = authorities if authorities is not None else old.get("existing_authorities", [])
    if not isinstance(established, list) or not all(isinstance(path, str) for path in established):
        raise BootstrapError("Existing authorities must be a list of relative paths")
    established = sorted(set(relative_path(path) for path in established))
    for path in established:
        if not contained(target, path).exists():
            raise BootstrapError(f"Existing authority was not found: {path}")
    assets = source_assets(source)
    fingerprint = source_digest(assets)
    if old and any(old.get(key) != value for key, value in {
        "source_digest": fingerprint, "mode": mode, "project_name": project_name,
        "paths": paths, "existing_authorities": established,
    }.items()):
        raise BootstrapError("Installed source or adoption choices differ. Review an explicit update/merge; this helper never overwrites an installation")
    mapping = {relative: f"{NAMESPACE}/{relative}" for relative in assets}
    mapping.update({logical: paths[key] for key, logical in LOGICAL.items()})
    mapping.update({"AGENTS.md": "AGENTS.md", "README.md": f"{NAMESPACE}/README.md"})
    # Directory links only resolve when the package contains something in them.
    for relative in list(assets):
        for parent in PurePosixPath(relative).parents:
            if str(parent) != ".":
                mapping.setdefault(parent.as_posix(), f"{NAMESPACE}/{parent.as_posix()}")
    plan = Plan(target=target, paths=paths, mode=mode)
    omitted: set[str] = set()
    outputs = {}
    for relative, content in assets.items():
        if relative.endswith(".md"):
            try:
                content = rewrite_links(content.decode("utf-8"), relative, mapping[relative], mapping, omitted).encode()
            except UnicodeDecodeError as exc:
                raise BootstrapError(f"Source documentation is not UTF-8: {relative}") from exc
        outputs[mapping[relative]] = content
    outputs[f"{NAMESPACE}/README.md"] = f"""# AWS project workflow: {project_name}

This is a reusable guidance and tooling package. Application context paths are
recorded in [manifest.json](manifest.json); they preserve existing project records
or point to fresh records created for this application. No source-template brief,
active specification, backlog, evidence receipt, or `.codex` settings were copied.

Start with [the application brief]({quote(posixpath.relpath(paths['brief'], NAMESPACE), safe='/._-')})
and [the current handoff]({quote(posixpath.relpath(paths['handoff'], NAMESPACE), safe='/._-')}), then use
[Consult](workflows/consult.md). In brownfield work, assess existing authority
before adopting structured specification metadata. The manifest maps logical
context paths in reusable prose to the application's actual files.

Before selecting work, read the mapped brief/handoff and start the consultation
naturally. Read-only local setup inspection works before any selection:

```sh
python3 .aws-workflow/scripts/workflow.py --root . doctor
```

After consultation chooses a bounded work item and route, create it
from the application root, then load its context. For example:

```sh
python3 .aws-workflow/scripts/workflow.py --root . new 0100-first-capability --title "First useful capability" --mode {mode} --route requirements-first --activate
python3 .aws-workflow/scripts/workflow.py --root . context --compact
```

Select the route and title for the actual agreed scope; the command above is an
example, not an automatically selected backlog. For an already selected work item,
run only `context`. It requires a selected work record; adoption itself selects
none. Inspect `--help` for supported options. Adoption does not enable hooks, install
plugins, start models, authenticate, access AWS, or authorize deployment. Native
execution state is excluded from Git through the additive managed `.gitignore`
block. The runner verifies the effective ignore rule before native execution.

Packaged reference material may describe maintenance of the source template.
Those sections do not create application obligations. Excluded source-template
links become labeled prose; the installation preview lists each omitted reference.
For updates, compare a fresh preview against the original template and perform
an explicitly reviewed merge. This helper intentionally has no force/overwrite mode.
""".encode()
    block = agent_block(paths, established)
    agent_path = contained(target, "AGENTS.md")
    existing_agent = read_file(agent_path) if agent_path.exists() else None
    if existing_agent is None:
        if old:
            raise BootstrapError("Installed AGENTS.md is missing; review restoration before continuing")
        agent_content = ("# Project instructions\n\n" + block + "\n").encode()
    else:
        try:
            agent_text = existing_agent.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise BootstrapError("Existing AGENTS.md must be UTF-8; manual instruction merge required") from exc
        if BEGIN in agent_text or END in agent_text:
            if not old or agent_text.count(BEGIN) != 1 or agent_text.count(END) != 1:
                raise BootstrapError("Existing managed instruction markers are ambiguous; manual merge required")
            actual = agent_text[agent_text.index(BEGIN):agent_text.index(END) + len(END)]
            if actual != block:
                raise BootstrapError("Managed instruction block changed; review and merge without replacing existing instructions")
            agent_content = existing_agent
        elif old:
            raise BootstrapError("Installed instruction block is missing; manual merge required")
        else:
            separator = "" if agent_text.endswith("\n\n") else "\n" if agent_text.endswith("\n") else "\n\n"
            agent_content = existing_agent + (separator + block + "\n").encode()
    ignore_path = contained(target, ".gitignore")
    existing_ignore = read_file(ignore_path) if ignore_path.exists() else None
    if existing_ignore is None:
        if old:
            raise BootstrapError("Installed .gitignore is missing; review restoration before continuing")
        ignore_content = (IGNORE_BLOCK + "\n").encode()
    else:
        try:
            ignore_text = existing_ignore.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise BootstrapError("Existing .gitignore must be UTF-8; manual ignore merge required") from exc
        if IGNORE_BEGIN in ignore_text or IGNORE_END in ignore_text:
            if not old or ignore_text.count(IGNORE_BEGIN) != 1 or ignore_text.count(IGNORE_END) != 1:
                raise BootstrapError("Existing runtime ignore markers are ambiguous; manual merge required")
            actual = ignore_text[ignore_text.index(IGNORE_BEGIN):ignore_text.index(IGNORE_END) + len(IGNORE_END)]
            if actual != IGNORE_BLOCK:
                raise BootstrapError("Managed runtime ignore block changed; review an explicit merge")
            ignore_content = existing_ignore
        elif old:
            raise BootstrapError("Installed runtime ignore block is missing; review an explicit update/merge")
        else:
            separator = "" if ignore_text.endswith("\n\n") else "\n" if ignore_text.endswith("\n") else "\n\n"
            ignore_content = existing_ignore + (separator + IGNORE_BLOCK + "\n").encode()
    managed = {path: digest(content) for path, content in sorted(outputs.items())}
    if old and old.get("managed_files") != managed:
        raise BootstrapError("Installed file inventory differs; an explicit update/merge is required")
    collisions = []
    for relative, content in sorted(outputs.items()):
        path = contained(target, relative)
        if path.exists():
            if read_file(path) != content:
                collisions.append(relative)
            else:
                plan.preserved.append(relative)
        elif old:
            collisions.append(relative + " (installed file missing)")
        else:
            plan.writes.append(Write(relative, content))
    editable = initial_records(project_name, mode, paths, established)
    for relative, content in editable.items():
        if relative in outputs or relative in (MANIFEST, "AGENTS.md", ".gitignore"):
            raise BootstrapError(f"Project context collides with workflow package: {relative}")
        path = contained(target, relative)
        if path.exists():
            read_file(path)
            plan.preserved.append(relative)
        elif old:
            collisions.append(relative + " (project record missing)")
        elif not relative.startswith(NAMESPACE + "/"):
            raise BootstrapError(f"Mapped existing context is missing: {relative}")
        else:
            plan.writes.append(Write(relative, content))
    if collisions:
        raise BootstrapError("Content collisions; no files written:\n- " + "\n- ".join(collisions))
    if agent_content != existing_agent:
        plan.writes.append(Write("AGENTS.md", agent_content, existing_agent))
    else:
        plan.preserved.append("AGENTS.md")
    if ignore_content != existing_ignore:
        plan.writes.append(Write(".gitignore", ignore_content, existing_ignore))
    else:
        plan.preserved.append(".gitignore")
    manifest = {
        "schema_version": 1, "identity": IDENTITY, "mode": mode, "project_name": project_name,
        "source_digest": fingerprint, "paths": paths, "existing_authorities": established,
        "managed_files": managed, "editable_project_records": sorted(editable),
        "agent_block_sha256": digest(block.encode()), "runtime_ignore_block_sha256": digest(IGNORE_BLOCK.encode()), "omitted_template_references": sorted(omitted),
    }
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    if old:
        if read_file(manifest_path) != manifest_bytes:
            raise BootstrapError("Installation manifest changed; review it before reapplying")
        plan.preserved.append(MANIFEST)
    else:
        # Commit the manifest last; an incomplete transaction is never a valid install.
        plan.writes.append(Write(MANIFEST, manifest_bytes))
    plan.omitted_references = sorted(omitted)
    return plan


def apply_plan(plan: Plan) -> None:
    """Apply preflighted additive writes; roll back only this transaction's files."""
    created_directories: list[Path] = []
    completed: list[Write] = []
    # Recheck every expected output before the first write, including AGENTS bytes.
    for write in plan.writes:
        path = contained(plan.target, write.relative)
        if write.before is None and path.exists():
            raise BootstrapError(f"Target changed since preview: {write.relative}")
        if write.before is not None and (not path.exists() or read_file(path) != write.before):
            raise BootstrapError(f"Existing instructions changed since preview: {write.relative}")
    try:
        for write in plan.writes:
            path = contained(plan.target, write.relative)
            missing = []
            parent = path.parent
            while not parent.exists():
                missing.append(parent)
                parent = parent.parent
            if plan.target not in (parent, *parent.parents) and parent != plan.target.parent:
                raise BootstrapError("A parent directory outside the target disappeared")
            for directory in reversed(missing):
                no_symlinks(directory)
                directory.mkdir()
                created_directories.append(directory)
            no_symlinks(path)
            mode = stat.S_IMODE(path.stat().st_mode) if write.before is not None else 0o644
            temporary: str | None = None
            try:
                fd, temporary = tempfile.mkstemp(prefix=".bootstrap-", dir=path.parent)
                with os.fdopen(fd, "wb") as stream:
                    stream.write(write.content)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.chmod(temporary, mode)
                no_symlinks(path)
                if write.before is None:
                    os.link(temporary, path, follow_symlinks=False)
                else:
                    if read_file(path) != write.before:
                        raise BootstrapError("Existing instructions changed while applying the plan")
                    os.replace(temporary, path)
                    temporary = None
                completed.append(write)
            finally:
                if temporary is not None:
                    Path(temporary).unlink(missing_ok=True)
    except (OSError, BootstrapError) as exc:
        leftovers = []
        for write in reversed(completed):
            path = plan.target / write.relative
            try:
                if read_file(path) != write.content:
                    leftovers.append(write.relative)
                elif write.before is None:
                    path.unlink()
                else:
                    path.write_bytes(write.before)
            except (OSError, BootstrapError):
                leftovers.append(write.relative)
        for directory in reversed(created_directories):
            try:
                directory.rmdir()
            except OSError:
                pass
        suffix = " Review concurrent changes at: " + ", ".join(leftovers) if leftovers else " This transaction's writes were rolled back."
        raise BootstrapError(f"Could not apply the plan: {exc}.{suffix}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="Separate original workflow template root")
    parser.add_argument("--target", required=True, help="Application root; no '..' or symlink components")
    parser.add_argument("--mode", required=True, choices=("greenfield", "brownfield"))
    parser.add_argument("--name", help="Application display name; defaults to target directory name")
    parser.add_argument("--brief", help="Existing canonical brief, relative to the application root")
    parser.add_argument("--handoff", help="Existing canonical handoff, relative to the application root")
    parser.add_argument("--authority", action="append", help="Existing authority file/directory to preserve and consult; repeatable")
    parser.add_argument("--apply", action="store_true", help="Write this additive plan; otherwise preview only")
    parser.add_argument("--json", action="store_true", help="Print machine-readable plan/result")
    arguments = parser.parse_args(argv)
    try:
        plan = build_plan(arguments.source, arguments.target, arguments.mode, arguments.name, arguments.brief, arguments.handoff, arguments.authority)
        if arguments.apply:
            apply_plan(plan)
        result = plan.summary(arguments.apply)
        if arguments.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"{result['status'].upper()}: {plan.target} ({plan.mode})")
            for change in result["changes"]:
                print(f"  {change['action']}: {change['path']}")
            print(f"Preserved: {len(plan.preserved)} existing files. No active application work was created.")
            if plan.omitted_references:
                print("Excluded template reference links (retained as labeled prose):")
                for reference in plan.omitted_references:
                    print("  " + reference)
            if not arguments.apply and plan.writes:
                print("Preview only; rerun the same command with --apply to write these files.")
        return 0
    except (BootstrapError, OSError) as exc:
        if arguments.json:
            print(json.dumps({"status": "blocked", "error": str(exc)}))
        else:
            print(f"Bootstrap blocked: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
