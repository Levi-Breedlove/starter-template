# Bootstrap and adopt an AWS project

`scripts/bootstrap.py` installs a small, additive workflow package into a separate
application repository. It uses Python 3.10 or newer and the standard library. It
previews every planned change by default; `--apply` writes the reviewed plan.
The helper runs offline and never executes the copied runtime, installs packages,
configures plugins, enables hooks, changes trust, or accesses AWS.

## Greenfield: start a new application

Run these commands from the original template repository. Choose an absolute
application path whose parent directory already exists. The target may be absent
or empty; an existing `.git` entry is preserved.

```sh
python3 scripts/bootstrap.py --source . --target /path/to/my-application --mode greenfield
python3 scripts/bootstrap.py --source . --target /path/to/my-application --mode greenfield --apply
```

Open the application repository in Codex. Its root instructions point to the
application's new consultation records and packaged workflows. Start with:

> Help me deliver [outcome] on AWS. Inspect this repository, establish what is
> already known, and guide me through the next material questions. Recommend the
> appropriate approach, record our decisions, then prepare the requirements,
> design, and tasks for the first useful delivery.

Adoption creates no active work specification. Codex first consults on the actual
application, then selects a work item and route. The packaged workflow CLI always
uses the application's root for work state, even though its implementation lives
inside `.aws-workflow/`:

```sh
python3 .aws-workflow/scripts/workflow.py --root . new 0100-first-capability --title "First useful capability" --mode greenfield --route requirements-first --idea "The user outcome agreed during consultation" --activate
python3 .aws-workflow/scripts/workflow.py --root . context --compact
```

Run these examples after that scope is established; they are not an automatic part
of adoption. For an already selected work item, run only `context`. Before any
selection, read the mapped brief/handoff and start the natural consultation;
`context` reports the missing selection and creates nothing. See
[workflow tooling](workflow-tooling.md) for the
metadata, review, task, and evidence contract.

## Brownfield: preserve an existing application

Use the brownfield mode for an existing application or infrastructure repository.
Review its instruction hierarchy and proposed additive block before applying.
The helper can preserve bytes; the consultant must assess the meaning of existing
instructions and resolve any conflicting authority before following the new flow.

```sh
python3 scripts/bootstrap.py --source . --target /path/to/existing-application --mode brownfield
python3 scripts/bootstrap.py --source . --target /path/to/existing-application --mode brownfield --apply
```

Existing `project/brief.md`, `delivery/current-handoff.md`,
`project/adoption-report.md`, and `delivery/environment-capabilities.md` remain
authoritative when present. If absent, fresh application-specific records are
created under `.aws-workflow/project/` and `.aws-workflow/delivery/`.
Map a nonstandard brief or handoff explicitly, and identify existing authority
files or directories without moving them:

```sh
python3 scripts/bootstrap.py --source . --target /path/to/existing-application --mode brownfield --brief architecture/product.md --handoff operations/resume.md --authority architecture --authority backlog
```

Repeat the same command with `--apply` after inspecting the preview. Each mapped
file or authority must already exist within the target. The helper does not
translate trackers, create a second backlog, import infrastructure, migrate state,
or change the delivery pipeline. Ask Codex to map existing specification and task
authority during brownfield intake. Structured CLI work uses root `specs/`; if an
existing system stores its canonical work elsewhere, establish an explicit
adoption decision before introducing structured work there.

## What is installed

| Location | Purpose and ownership |
| --- | --- |
| `.aws-workflow/workflows/`, `templates/`, `guide/` | Reusable consultation, specification, review, and delivery guidance. |
| `.aws-workflow/docs/`, `runbooks/`, `costs/`, `security/`, `infrastructure/` | Selected reusable reference material and example records; no assumed application architecture. |
| `.aws-workflow/scripts/workflow.py`, `workflow_engine/` | Local workflow state, validation, and context tooling. |
| `.aws-workflow/scripts/codex_hooks.py`, when supplied by the source | Optional adapter code only; no hook registration or configuration. |
| `.aws-workflow/manifest.json` | Installation identity, source digest, file hashes, mapped context paths, and declared existing authorities. |
| Mapped project brief, handoff, adoption report, and capability record | Editable application records; existing files are preserved, missing defaults are created inside the namespace. |
| A bounded block appended to root `AGENTS.md` | Routes Codex to actual project context and reusable procedures while preserving all previous instruction bytes. |

The helper excludes the source template's own project context, active
specifications, foundation backlog, evidence receipts, research tree, `.git`,
`.codex`, source code, CI configuration, tests, and installed skills. Selected
`README.md` files explain conventions without copying active work. Source-local
documentation links are rewritten to installed locations or mapped application
records. Excluded source-template links become labeled prose and are listed in
the preview and manifest; they do not become broken links to phantom active work.

The source copy map is deliberately bounded. It selects Markdown/JSON under the
declared guidance trees, Python under `workflow_engine/`, and named scripts and
reference files. It does not recursively copy the repository.
Missing required runtime modules or an unreadable selected source tree block the
plan before writes; the helper does not install a silently incomplete package.

## Manifest and path resolution

The manifest uses `schema_version: 1` and the identity `codex-aws-workflow`.
`paths` identifies `brief`, `handoff`, `adoption_report`, and
`environment_capabilities`, plus the structured CLI defaults `specifications`,
`evidence`, and `decisions`. Resolve logical paths mentioned in reusable prose
through this map. `existing_authorities` records the repeatable `--authority`
arguments. No credentials, account metadata, source-machine paths, active work
pointer, or assumed approval is stored.

`managed_files` records hashes for reusable package files; application records are
listed separately in `editable_project_records`. Their content is intentionally
editable. The installation preserves unrelated text before and after the bounded
root instruction block. Keep changes to reusable workflows separate from project
context: changing a managed file means a later rerun needs an explicit merge.

## Repeating, changing, and recovering adoption

Re-running the same command against the same source and installation is a no-op.
Changes to application records and unrelated root instructions are preserved.
The original mode and path choices remain in force; omitted `--brief`,
`--handoff`, and `--authority` arguments reuse the existing manifest's mapping.

A different source digest, changed managed file, missing installed file, changed
managed instruction block, or conflicting namespace blocks before any write.
There is no force or overwrite option. To update, preview a fresh adoption in a
separate temporary target and review the difference against the application;
merge the selected changes and installation records deliberately. The helper
does not claim to automate semantic instruction merges or source upgrades.

Paths with `..` components, overlapping source/target roots, symlink roots,
symlink selected assets, and symlink destination components are rejected. Existing
unrelated symlinks in an application are not traversed. Run against a stable
working tree: the helper rechecks planned outputs before writing, uses exclusive
creation for additions and atomic replacement for the instruction append, and
rolls back its own completed writes on an I/O failure. It does not provide a
cross-process lock or recovery from abrupt process/power loss. If a concurrent
change prevents rollback, the error identifies remaining files for review.

Use `--json` to inspect the planned changes, preserved paths, actual path map,
and omitted reference links without parsing human prose. A blocked plan exits
with status `1`; success and a no-op exit with status `0`.

## Verification boundary

The fixture suite exercises dry-run behavior, fresh application context,
brownfield preservation, custom authorities, reruns, content collisions, source
changes, path hazards, stale previews, and rollback after a simulated final write
failure. Required-runtime and source-inventory failures also block before writes.
Run it from the source template:

```sh
python3 -m unittest discover -s tests -p 'test_bootstrap.py'
```

These are local file-system checks. They do not establish that Codex loaded the
new instructions, that a particular hosted plugin is available, that optional
native hooks are enabled, or that an application deploys successfully to AWS.
