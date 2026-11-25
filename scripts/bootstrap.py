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
SCRIPT_FILES = ("scripts/workflow.py", "scripts/bootstrap.py", "scripts/codex_hooks.py", "scripts/check_repository.py")
REQUIRED = (
    "workflows/consult.md", "workflows/brownfield.md", "workflows/feature.md",
    "workflows/bugfix.md", "workflows/reconcile.md", "templates/project-brief.md",
    "templates/requirements.md", "templates/bugfix.md", "templates/design.md", "templates/tasks.md",
    "guide/00-quickstart.md", "guide/02-aws-guidance-and-access.md", "guide/08-aws-emulator.md",
    "docs/reference/specification-operations.md", "docs/reference/task-execution.md",
    "scripts/workflow.py", "scripts/check_repository.py", "workflow_engine/__init__.py", "workflow_engine/engine.py",
    "workflow_engine/context.py", "workflow_engine/specifications.py", "workflow_engine/runner.py", "workflow_engine/doctor.py", "workflow_engine/native_preflight.py",
)
FOUNDATIONS = {
    "brief": "project/brief.md",
    "requirements": "project/requirements.md",
    "tech": "project/tech.md",
    "structure": "project/structure.md",
    "architecture": "project/architecture.md",
}
LOGICAL = {
    **FOUNDATIONS,
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
    if not path.parts or not value or "\\" in value or path.is_absolute() or any(part in (".", "..") for part in value.split("/")):
        raise BootstrapError(f"Expected a contained relative path, received: {value!r}")
    if any(ord(char) < 32 for char in value) or any(part.casefold() == ".git" for part in path.parts):
        raise BootstrapError(f"Reserved or invalid path: {value!r}")
    return path.as_posix()


def no_symlinks(path: Path) -> None:
    for part in (path, *path.parents):
        if part.is_symlink():
            raise BootstrapError(f"Symlink paths are not supported: {part}")


def root_path(value: str | Path) -> Path:
    raw = Path(value).expanduser()
    absolute = Path(os.path.abspath(raw))
    if ".." in raw.parts or any(part.casefold() == ".git" for part in absolute.parts):
        raise BootstrapError(f"Use a root path outside Git metadata and without '..' components: {value}")
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
During `start`, progressively record confirmed project-wide decisions in the
mapped foundations. Use {local_link(paths['brief'])} for the product, users and
scope, {local_link(paths['requirements'])} for system requirements,
{local_link(paths['tech'])} for accepted technologies and standards,
{local_link(paths['structure'])} for repository conventions and ownership, and
{local_link(paths['architecture'])} for the system design and trust boundaries.
Read only foundations material to the current decision. Keep open choices
visible until resolved. Preserve existing mapped records, ADRs and diagrams.
Feature and defect specifications link to applicable foundations and describe
the change and its acceptance criteria. Add relevant mapped paths to the work's
`context_files` or cite them in sourced facts or answers. Reuse settled decisions
on return.

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

On the first user-initiated application consultation, greet warmly and briefly as the AWS consultant. If the user has supplied a goal, summarize it and the known constraints; otherwise ask what outcome they want and who will use it. Recommend the next direction using the available evidence. Do not repeat settled questions, invent facts, or require a ceremonial interview. Save the actual discussion in the mapped brief and handoff. When consultation or selected work already exists, resume it rather than restarting the welcome. No unsolicited message, background task, extra native invocation, or deployment is authorized by onboarding.

### Natural-language entry shortcuts

Treat the following standalone user messages (case-insensitive), or their clear natural-language equivalents, as conversational requests, not shell commands or mandatory syntax. A supplied goal or scope takes precedence. Use the current session and the mapped workflow paths; do not silently switch or abandon active work.

| Shortcut | Expected action |
| --- | --- |
| `start` | Run local setup inspection, read the mapped context, and begin a warm first consultation or continue the saved work. Infer greenfield or brownfield from adoption and evidence; ask only material unresolved questions. |
| `resume` | Inspect the handoff, current work and changed inputs; reconcile as needed and continue the next eligible authorized action. If no work exists, continue the saved consultation or begin it. |
| `status` | Read-only summary of the actual project state, phase, task/evidence progress, blockers and next action. Do not change files or start implementation. |
| `feature` | Inspect existing context, establish the desired new behavior, and choose the appropriate specification route. Preserve existing work and accepted architecture. |
| `bugfix` | Establish observed faulty behavior, expected behavior and what must remain unchanged; use the bugfix procedure and its verification obligations. |
| `review` | Inspect the actual selected specification or implementation candidate against its requirements, risks and evidence; report findings without manufacturing acceptance. |
| `release` | Prepare the release and verification/recovery plan under existing controls. Deployment or other external operations require actual scoped authority; the word alone grants none. |

A shortcut does not grant additional authority, accept a future artifact, launch a separate native model, or authorize account access or deployment. Retain the existing rules for local work, evidence and review. The manifest identifies this application's canonical project records.

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

Use the relevant official Agent Toolkit for AWS plugins available on this
Codex surface and current official public documentation. Follow
[{NAMESPACE}/guide/02-aws-guidance-and-access.md]({NAMESPACE}/guide/02-aws-guidance-and-access.md)
for exact official skill discovery and retrieval. When local integration tests
would benefit, assess the workload's AWS operations and plan isolated tests via
[{NAMESPACE}/guide/08-aws-emulator.md]({NAMESPACE}/guide/08-aws-emulator.md).
Preserve existing supported tests. Honor skill opt-outs and distinguish installed,
available, loaded, and tested capabilities.
Consult the current official plugin catalog on demand. Use AWS Core
`search_documentation` with topic `agent_skills`, then `retrieve_skill` with
the exact returned identifier. Check material guidance against official AWS
documentation and upstream. Assess authentication per operation. Continue
credential-free consultation, development and local verification with available
public tools. Defer an authenticated operation to its authorized cloud stage.
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
        paths["requirements"]: b"# Project requirements\n\n## Outcomes and system-wide acceptance criteria\n\n## Constraints and open decisions\n",
        paths["tech"]: b"# Technology and engineering standards\n\n## Accepted stack, services and tools\n\n## Standards and decision references\n",
        paths["structure"]: b"""# Repository structure

Use this foundation to record where work belongs, who owns each component and
which conventions the project has accepted. Preserve established brownfield
paths, tooling and ownership. Consult `.aws-workflow/manifest.json` for mapped
records when their locations differ from the template defaults.

## Components and ownership

| Default location | What belongs here |
| --- | --- |
| `project/` | Shared brief, system requirements, technology, structure and architecture decisions that guide work across features. |
| `src/` and `tests/` | Application components and their verification. Follow the layout expected by the language, framework and test runner. |
| `infrastructure/` and `security/` | Infrastructure as code and environment ownership, plus security boundaries, controls and review responsibilities. |
| `costs/` and `runbooks/` | Cost assumptions, estimates and controls, plus operational, incident and recovery procedures. |
| `docs/decisions/` and `docs/diagrams/` | Architecture decision records and diagrams. Reference these from the relevant foundation or specification. |
| `specs/<work-id>/` | Scoped requirements or defect contract, design, tasks and workflow records. |
| `evidence/` and `delivery/` | Verification receipts, and the current handoff, release and recovery records that refer to them. |
| `.aws-workflow/` | Installed workflow, reusable guidance and manifest. |

## Layout and naming conventions

For new project-owned directories and ordinary Markdown files, prefer lowercase
kebab-case, such as `booking-api/` and `retry-policy.md`. Keep conventional root
filenames `README.md`, `AGENTS.md`, `CHANGELOG.md`, `CONTRIBUTING.md` and
`SECURITY.md`. Name source files, tests and symbols according to the language
and tools selected for the application.

The structured CLI requires a work ID of 1 to 80 characters. Start with a
lowercase ASCII letter or digit, then use lowercase ASCII letters, digits or
hyphens. A numbered descriptive ID such as `0001-booking-retries` is a useful
default. The ID in `work.json` must match its directory under `specs/`.
Artifact paths in that record are relative to the work directory. Usual names
are `requirements.md` (or `bugfix.md`), `design.md` and `tasks.md`. Recorded
analysis and correctness properties use `analysis.json` and `properties.json`.

Keep identifiers stable within each specification. For example, trace
`REQ-001` to design `DES-001`, correctness property `PROP-001`, task `T-001`
and check `CHK-001`. These identifiers use their uppercase prefix and at least
three digits. Across specifications, cite the work ID or artifact path together
with the identifier, such as `specs/0001-booking-retries/tasks.md` and `T-001`.
For a check receipt under `evidence/<work-id>/`, identify the candidate, check,
method, environment, observation time, inputs and actual result.

## Project decisions and exceptions

Record the actual owner, path and any local exception as decisions are agreed.
Link to the existing decision or tool configuration when it owns the rule.
For a new versioned public interface, consider Semantic Versioning (SemVer).
Its `MAJOR.MINOR.PATCH` components signal incompatible changes, backward-compatible features
and backward-compatible fixes, respectively. Record the project's accepted
release policy and tag convention here or reference its existing release guide.
""",
        paths["architecture"]: b"# System architecture\n\n## Components, interfaces and data flows\n\n## Infrastructure and trust boundaries\n\n## Architecture decisions and diagrams\n",
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
    action: str = "create"


@dataclass
class Plan:
    target: Path
    writes: list[Write] = field(default_factory=list)
    preserved: list[str] = field(default_factory=list)
    omitted_references: list[str] = field(default_factory=list)
    paths: dict[str, str] = field(default_factory=dict)
    mode: str = ""
    verified: dict[str, str] = field(default_factory=dict)

    def summary(self, applied: bool = False) -> dict[str, object]:
        return {
            "status": "applied" if applied and self.writes else "unchanged" if not self.writes else "preview",
            "target": str(self.target), "mode": self.mode,
            "changes": [{"path": write.relative, "action": write.action} for write in self.writes],
            "preserved": sorted(self.preserved), "paths": self.paths,
            "omitted_template_references": self.omitted_references,
        }


def read_manifest(path: Path) -> dict:
    try:
        manifest = json.loads(text_file(path))
    except json.JSONDecodeError as exc:
        raise BootstrapError("Existing installation manifest is invalid; review it manually") from exc
    if (not isinstance(manifest, dict) or manifest.get("identity") != IDENTITY
            or type(manifest.get("schema_version")) is not int or manifest["schema_version"] not in (1, 2)):
        raise BootstrapError("Existing namespace belongs to an unknown installation")
    paths = manifest.get("paths")
    managed = manifest.get("managed_files")
    if not isinstance(paths, dict) or not isinstance(managed, dict):
        raise BootstrapError("Installation path map and managed inventory must be objects")
    required = {"brief", "handoff", "adoption_report", "environment_capabilities", "specifications", "evidence", "decisions"}
    if manifest["schema_version"] == 2:
        required.update(FOUNDATIONS)
    if not required <= paths.keys() or not all(isinstance(v, str) for v in paths.values()):
        raise BootstrapError("Installation manifest has incomplete or invalid context paths")
    for value in paths.values():
        relative_path(value)
    if sorted(paths[k] for k in LOGICAL if k in paths) != manifest.get("editable_project_records"):
        raise BootstrapError("Installation editable records differ from the mapped project records")
    if not all(isinstance(k, str) and relative_path(k).startswith(NAMESPACE + "/")
               and isinstance(h, str) and re.fullmatch(r"[0-9a-f]{64}", h) for k, h in managed.items()):
        raise BootstrapError("Invalid managed file inventory")
    omitted = manifest.get("omitted_template_references")
    if not isinstance(omitted, list) or not all(isinstance(item, str) for item in omitted):
        raise BootstrapError("Invalid omitted reference inventory")
    if not isinstance(manifest.get("source_digest"), str) or not re.fullmatch(r"[0-9a-f]{64}", manifest["source_digest"]):
        raise BootstrapError("Invalid installation source digest")
    return manifest


def build_plan(source: str | Path, target: str | Path, mode: str, name: str | None = None,
               brief: str | None = None, handoff: str | None = None, authorities: list[str] | None = None,
               *, requirements: str | None = None, tech: str | None = None, structure: str | None = None,
               architecture: str | None = None, upgrade: bool = False, visible_records: bool = False) -> Plan:
    source, target = root_path(source), root_path(target)
    own_package = source == target / NAMESPACE and contained(source, "manifest.json").is_file()
    if not own_package and (source == target or source in target.parents or target in source.parents):
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
        old = read_manifest(manifest_path)
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
    overrides = {"brief": brief, "handoff": handoff, "requirements": requirements, "tech": tech,
                 "structure": structure, "architecture": architecture}
    if visible_records and mode != "greenfield":
        raise BootstrapError("Visible distribution records require a greenfield project")
    if upgrade and not old:
        raise BootstrapError("--upgrade requires an existing installation manifest")
    for key, logical in LOGICAL.items():
        requested = overrides.get(key)
        visible = visible_records or key in FOUNDATIONS or contained(target, logical).exists()
        default = logical if visible else f"{NAMESPACE}/{logical}"
        mapped = requested or persisted.get(key) or default
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
    packed = read_manifest(contained(source, "manifest.json")) if source.name == NAMESPACE else None
    fingerprint = source_digest(assets)
    if packed:
        inventory = {f"{NAMESPACE}/{path}": digest(content) for path, content in assets.items()}
        inventory[f"{NAMESPACE}/README.md"] = digest(read_file(contained(source, "README.md")))
        if inventory != packed["managed_files"]:
            raise BootstrapError("Packaged source files differ from their manifest; review the source installation")
        fingerprint = packed["source_digest"]
    if old:
        if (old.get("mode") != mode or old.get("project_name") != project_name
                or old.get("existing_authorities") != established
                or any(paths.get(key) != value for key, value in persisted.items())):
            raise BootstrapError("Existing mappings, project identity or authorities differ; review an explicit update/merge")
        if not upgrade and (old["source_digest"] != fingerprint or old["schema_version"] != 2):
            raise BootstrapError("Installed source differs. Review an explicit update/merge with --upgrade")
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
    link_map = mapping
    if packed:
        omitted.update(packed.get("omitted_template_references", []))
        # Links in an installed guide already use the source application's mapped
        # paths. Resolve at that application's root, then map to this target.
        link_map = {f"{NAMESPACE}/{relative}": dest for relative, dest in mapping.items()}
        link_map.update({packed["paths"][key]: dest for key, dest in paths.items() if key in packed["paths"]})
        link_map["AGENTS.md"] = "AGENTS.md"
    outputs = {}
    for relative, content in assets.items():
        if relative.endswith(".md"):
            try:
                original = f"{NAMESPACE}/{relative}" if packed else relative
                content = rewrite_links(content.decode("utf-8"), original, mapping[relative], link_map, omitted).encode()
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
naturally. Open the application in Codex and type **`start`**.
Describe the outcome if you already know it. Codex runs the setup check and
continues saved consultation or work when present. To check setup manually, run:

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
For updates, preview the candidate source with `--upgrade`. Inspect the plan
before applying it. Local changes to managed files require a reviewed merge.
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
            if digest(actual.encode()) != old.get("agent_block_sha256") or (actual != block and not upgrade):
                raise BootstrapError("Managed instruction block changed; review and merge without replacing existing instructions")
            agent_content = agent_text.replace(actual, block, 1).encode()
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
            if actual != IGNORE_BLOCK or digest(actual.encode()) != old.get("runtime_ignore_block_sha256"):
                raise BootstrapError("Managed runtime ignore block changed; review an explicit merge")
            ignore_content = existing_ignore
        elif old:
            raise BootstrapError("Installed runtime ignore block is missing; review an explicit update/merge")
        else:
            separator = "" if ignore_text.endswith("\n\n") else "\n" if ignore_text.endswith("\n") else "\n\n"
            ignore_content = existing_ignore + (separator + IGNORE_BLOCK + "\n").encode()
    managed = {path: digest(content) for path, content in sorted(outputs.items())}
    installed = old.get("managed_files", {})
    if installed.keys() - managed.keys():
        raise BootstrapError("A previously managed path would be removed; review an explicit update/merge")
    if old and not upgrade and installed != managed:
        raise BootstrapError("Installed file inventory differs; an explicit update/merge is required")
    collisions = []
    for relative, content in sorted(outputs.items()):
        path = contained(target, relative)
        if not path.exists():
            if relative in installed:
                collisions.append(relative + " (installed file missing)")
            else:
                plan.writes.append(Write(relative, content))
            continue
        current = read_file(path)
        if relative in installed and digest(current) != installed[relative]:
            collisions.append(relative)
        elif current == content and (not old or relative in installed):
            plan.preserved.append(relative)
            if old:
                plan.verified[relative] = digest(current)
        elif upgrade and relative in installed:
            plan.writes.append(Write(relative, content, current, "update managed file"))
        else:
            collisions.append(relative)
    editable = initial_records(project_name, mode, paths, established)
    for relative, content in editable.items():
        if relative in outputs or relative in (MANIFEST, "AGENTS.md", ".gitignore"):
            raise BootstrapError(f"Project context collides with workflow package: {relative}")
        path = contained(target, relative)
        if path.exists():
            read_file(path)
            plan.preserved.append(relative)
        elif relative in old.get("editable_project_records", []):
            collisions.append(relative + " (project record missing)")
        elif not relative.startswith(NAMESPACE + "/") and relative not in LOGICAL.values():
            raise BootstrapError(f"Mapped existing context is missing: {relative}")
        else:
            plan.writes.append(Write(relative, content))
    if collisions:
        raise BootstrapError("Content collisions; no files written:\n- " + "\n- ".join(collisions))
    if agent_content != existing_agent:
        action = "create" if existing_agent is None else "append managed instructions"
        if old:
            action = "update managed instructions"
        plan.writes.append(Write("AGENTS.md", agent_content, existing_agent, action))
    else:
        plan.preserved.append("AGENTS.md")
        plan.verified["AGENTS.md"] = digest(agent_content)
    if ignore_content != existing_ignore:
        action = "create" if existing_ignore is None else "append managed runtime ignore"
        plan.writes.append(Write(".gitignore", ignore_content, existing_ignore, action))
    else:
        plan.preserved.append(".gitignore")
        plan.verified[".gitignore"] = digest(ignore_content)
    manifest = {
        "schema_version": 2, "identity": IDENTITY, "mode": mode, "project_name": project_name,
        "source_digest": fingerprint, "paths": paths, "existing_authorities": established,
        "managed_files": managed, "editable_project_records": sorted(editable),
        "agent_block_sha256": digest(block.encode()), "runtime_ignore_block_sha256": digest(IGNORE_BLOCK.encode()), "omitted_template_references": sorted(omitted),
    }
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    if old:
        previous = read_file(manifest_path)
        if set(old) != set(manifest):
            raise BootstrapError("Installation manifest fields changed; review it before reapplying")
        if previous == manifest_bytes:
            plan.preserved.append(MANIFEST)
        elif upgrade:
            plan.writes.append(Write(MANIFEST, manifest_bytes, previous, "update installation manifest"))
        else:
            raise BootstrapError("Installation manifest changed; review it before reapplying")
    else:
        # Commit the manifest last; an incomplete transaction is never a valid install.
        plan.writes.append(Write(MANIFEST, manifest_bytes))
    if own_package and plan.writes:
        raise BootstrapError("An in-place installed package may only verify an unchanged installation; use a separate source to upgrade")
    plan.omitted_references = sorted(omitted)
    return plan


def apply_plan(plan: Plan) -> None:
    """Apply preflighted additive writes; roll back only this transaction's files."""
    created_directories: list[Path] = []
    completed: list[Write] = []
    # Recheck every expected output before the first write, including AGENTS bytes.
    for relative, expected in plan.verified.items():
        if digest(read_file(contained(plan.target, relative))) != expected:
            raise BootstrapError(f"File changed since preview: {relative}")
    for write in plan.writes:
        path = contained(plan.target, write.relative)
        if write.before is None and path.exists():
            raise BootstrapError(f"Target changed since preview: {write.relative}")
        if write.before is not None and (not path.exists() or read_file(path) != write.before):
            raise BootstrapError(f"Existing file changed since preview: {write.relative}")
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
                        raise BootstrapError(f"Existing file changed while applying the plan: {write.relative}")
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
    parser.add_argument("--source", required=True, help="Workflow template source root or installed .aws-workflow package")
    parser.add_argument("--target", required=True, help="Application root; no '..' or symlink components")
    parser.add_argument("--mode", required=True, choices=("greenfield", "brownfield"))
    parser.add_argument("--name", help="Application display name; defaults to target directory name")
    for key in FOUNDATIONS:
        parser.add_argument(f"--{key}", help=f"Existing canonical project {key}, relative to the application root")
    parser.add_argument("--handoff", help="Existing canonical handoff, relative to the application root")
    parser.add_argument("--authority", action="append", help="Existing authority file/directory to preserve and consult; repeatable")
    parser.add_argument("--upgrade", action="store_true", help="Preview an existing installation upgrade, preserving editable records and verifying old managed bytes")
    parser.add_argument("--apply", action="store_true", help="Write this additive plan; otherwise preview only")
    parser.add_argument("--json", action="store_true", help="Print machine-readable plan/result")
    arguments = parser.parse_args(argv)
    try:
        plan = build_plan(arguments.source, arguments.target, arguments.mode, arguments.name,
                          handoff=arguments.handoff, authorities=arguments.authority, upgrade=arguments.upgrade,
                          **{key: getattr(arguments, key) for key in FOUNDATIONS})
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
