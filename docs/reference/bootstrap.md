# Adopt or upgrade the AWS project workflow

A repository created with **Use this template** already contains the initialized application. Open its root in Codex and type `start`. Use the bootstrap helper to adopt the same workflow into another project or upgrade an existing installation. It requires Python 3.10 or newer, uses the standard library, and runs offline. [First-use guide](../../guide/00-quickstart.md)

## Install into a separate application

Run these commands from the root of a project created from the template. Set `app` to the target application directory. Choose `brownfield` for an existing project, or `greenfield` for a new or empty target. Greenfield accepts an existing Git directory. The target's parent must exist.

```sh
app=/absolute/path/to/application
python3 .aws-workflow/scripts/bootstrap.py --source .aws-workflow --target "$app" --mode brownfield
python3 .aws-workflow/scripts/bootstrap.py --source .aws-workflow --target "$app" --mode brownfield --apply
```

The first command previews the exact paths and actions. Inspect the preview before applying it. In a framework maintenance checkout, use `scripts/bootstrap.py --source .` with the same target arguments. The installed package can itself serve as a source after its managed-file inventory has been verified against its manifest.

In the adopted application, open Codex and type `start`. For a manual setup check, run:

```sh
python3 .aws-workflow/scripts/workflow.py --root . doctor
```

A fresh application begins with consultation. Once the outcome and scope are known, select work with the installed CLI. On return, the handoff and compact context identify the next action. [Workflow tooling](workflow-tooling.md)

## Existing project foundations

The consultant reads the brief and handoff, then consults the project-wide foundations relevant to the current decision. New installations create editable project documents at these defaults.

| Path | Canonical content | Existing-file option |
| --- | --- | --- |
| `project/brief.md` | Product purpose, users, scope and decisions | `--brief` |
| `project/requirements.md` | System-wide outcomes and acceptance criteria | `--requirements` |
| `project/tech.md` | Accepted stack, services, tools and standards | `--tech` |
| `project/structure.md` | Component layout, conventions and ownership | `--structure` |
| `project/architecture.md` | System design, interfaces, data flows and trust boundaries | `--architecture` |

Keep existing canonical files at their established locations. The helper discovers the default paths above. To map other locations, add options such as `--brief docs/product.md --tech docs/stack.md --architecture docs/system.md --handoff operations/resume.md` to the preview and apply commands. Mapped files must exist inside the target. Supply `--authority backlog --authority docs/decisions` if those existing locations own tasks and decisions. Repeated installation uses the saved mappings.

Record decisions progressively during consultation. Keep work-specific acceptance criteria, design, analysis, properties, tasks and evidence under the work's existing authority. Reference relevant foundations from each work item. Preserve accepted architecture, IaC, pipelines, instructions and application changes during brownfield adoption.

## Files and ownership

| Location | Contents |
| --- | --- |
| `AGENTS.md` | The helper adds one bounded block to the existing project instructions. |
| `.aws-workflow/` | Reusable guidance, templates, references and local scripts. `manifest.json` identifies the source digest, managed file hashes, editable paths and existing authorities. |
| Mapped brief, requirements, tech, structure, architecture, handoff, adoption and capabilities records | Editable project-owned files. Existing files are preserved. Local adoption creates missing handoff and supporting records under the package namespace when their conventional paths are absent. |
| `.gitignore` | A bounded block excludes `/.workflow-state/`, which can hold local candidate worktrees and run state. |

The published application package contains reusable source and blank project records. Adoption selects a bounded list of guidance, templates and runtime files, excluding active specifications, framework receipts, project code, user configuration and skills. Local Markdown links resolve to installed guidance or mapped project records. The manifest lists excluded source references.

## Upgrade and recovery

Use the helper **from the target release**, point it at the existing application, and add `--upgrade`. Retain the original adoption mode. For example, preview an upgrade from a template project:

```sh
python3 .aws-workflow/scripts/bootstrap.py --source .aws-workflow --target "$app" --mode brownfield --upgrade
```

Review the paths and changes, then repeat with `--apply`. The helper accepts schema-1 and schema-2 manifests and writes schema 2. A schema-1 upgrade keeps the original mapped brief, including `.aws-workflow/project/brief.md`. It adds the four new foundation mappings and preserves application-edited content and surrounding instruction text. Supply existing foundation locations when previewing this first upgrade. Upgrade never moves an existing canonical document.

Each previously managed file and the instruction and ignore blocks must match their recorded identities. Local edits, missing files, an unowned file at a new managed destination, or removal of a previously managed path require a reviewed merge. Inspect the reported paths, preserve local changes and resolve ownership before applying an update. Repeating an unchanged installation is a no-op. Add `--json` for a machine-readable plan and status.

Run the helper against a stable worktree. It rejects unsafe paths and symlinks, rechecks expected contents, creates new files exclusively, and rolls back completed writes after an ordinary I/O failure. Following an interruption or power loss, inspect Git changes and the manifest before continuing. Git supplies history and recovery for tracked files. Initializing and upgrading a project use no model invocations, AWS accounts, deployment, hook registration or trust changes.
