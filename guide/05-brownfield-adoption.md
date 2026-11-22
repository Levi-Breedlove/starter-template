# Adopt the workflow in an existing project

Start with the system that exists. The first adoption should help deliver one real change while preserving working code, documentation authority, infrastructure ownership, and the established pipeline.

## Inspect before interviewing or installing

Follow [Brownfield intake](../workflows/brownfield.md) and the [assessment template](../templates/brownfield-assessment.md). Inspect instructions, source structure, dependencies, tests, specifications, decisions, IaC, CI, runbooks, and task authority. Record actual evidence and unresolved contradictions.

Codex should begin consultation with those findings and a recommendation. It should not ask the user to restate the language, framework, database, IaC tool, or pipeline already established by the project. Ask one to three focused questions when missing product intent or ownership materially changes the proposed work. Save answers in the mapped brief or work contract. See [the interview guide](06-consultation-interview.md) and [brownfield example](../examples/consultation/brownfield.md).

Separate what the repository declares, what supplied or authorized environment evidence demonstrates, and what remains unknown. An IaC file does not prove live ownership; source code does not prove the deployed revision.

## Preview an additive adoption

From the bootstrap checkout:

```bash
python3 scripts/bootstrap.py --source . --target /path/to/existing-app --mode brownfield
```

The default is a dry run. Inspect the proposed file additions and root-instruction change. Add `--apply` when the adoption is authorized and the concrete changes are appropriate. The helper installs reusable guidance and tools beneath `.aws-workflow/`; it preserves source layout, IaC, pipeline configuration, and existing root instructions.

`.aws-workflow/manifest.json` records actual paths for the brief, handoff, adoption report, environment capability record, specifications, evidence, and decisions. Existing `project/brief.md` and `delivery/current-handoff.md` are used when present; otherwise fresh context files live under `.aws-workflow/`. If the project already uses other paths, map them with `--brief` and `--handoff`. Record other existing authoritative relative paths with `--authority` instead of silently replacing their role.

The bootstrap's own brief, foundation backlog, and implementation evidence are not application context and are not copied. Native hooks and AWS plugin setup are separate capabilities; adoption does not enable or install them implicitly. If existing files conflict, inspect and resolve the concrete conflict without overwriting user work.

## Map existing authority and preserve behavior

| Existing situation | Adoption action |
| --- | --- |
| Root instructions already exist | Keep them; add the bounded workflow entry that links the manifest and procedures. |
| Architecture and delivery documents already exist | Reference them from the brief/report; avoid duplicate explanations with independent status. |
| Existing specification or tracker authority | Map it explicitly. Agree on an authority change only if necessary; do not introduce a competing backlog. |
| Existing test suite | Establish applicable baseline evidence and distinguish pre-existing failures. |
| Existing application directories | Retain their paths and conventions. |
| Existing IaC and state | Preserve tools, stack/module boundaries, ownership, and state. Plan import or migration as separate work. |
| Existing CI and deployment pipeline | Use its established artifact and release process; add missing checks only as scoped work. |

Choose one representative change. Capture affected interfaces, consumer expectations, data lifecycle, compatibility, security boundaries, and operational obligations. Add characterization checks where current behavior is insufficiently documented. Distinguish the intentional change from what must remain intact.

For infrastructure work, inspect declared resource/state ownership and unmanaged dependencies before proposing replacement or import. [AWS guidance and access](02-aws-guidance-and-access.md) and [infrastructure guidance](../infrastructure/README.md) define the public research and account-operation boundaries. Account inspection is not implied by repository adoption.

## Create the first bounded work item

Resolve task authority before creating another record. The helper records existing authority paths; it does not synchronize a tracker or migrate its tasks. If an existing tracker remains authoritative, define how the local specification and task view relate to it and who maintains the projection. Do not create two independent completion records.

From the adopted application root, use the installed tool and the route suited to the change when the local task record is the selected authority:

```bash
python3 .aws-workflow/scripts/workflow.py --root . new 0100-first-change --title "First bounded change" --mode brownfield --route design-first --activate
python3 .aws-workflow/scripts/workflow.py --root . context
```

A defect uses `--route bugfix`; a new behavior may justify Requirements-First. The mode does not force one route. Carry the inspected baseline and saved answers forward, then conduct the relevant phase reviews. Do not replace established decisions with template defaults.

## Verify the adoption through useful work

Adoption succeeds when Codex can locate current authority, explain the existing system from evidence, consult on a genuine gap, and deliver a bounded change with required preservation checks. The existing repository and pipeline remain usable. More documents alone are not evidence of improvement.

Record the mapped paths, actual review outcome, known gaps, evidence, and next action in the project report and handoff. Resume by comparing the current revision with that baseline. Expand instructions or automation when a repeated need justifies it.
