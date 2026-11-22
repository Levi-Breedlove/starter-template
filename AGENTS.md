# Working in this repository

## Start with the actual project

Read `project/brief.md` and `delivery/current-handoff.md`, then inspect the current worktree and relevant code before proposing changes. Follow applicable existing instructions. The brief currently describes the bootstrap itself; application adoption must replace it with application context and start a separate work specification.

Use `docs/repository-map.md` to find artifacts. Load only the guidance relevant to the task. Existing project architecture, tools, IaC ownership, and delivery controls remain authoritative until an actual decision changes them. Do not derive facts about a running AWS system from repository files alone.

## Choose a procedure

| Work | Procedure |
| --- | --- |
| New project, consultation, or architecture question | `workflows/consult.md` |
| Existing repository or infrastructure adoption | `workflows/brownfield.md` |
| New or changed behavior | `workflows/feature.md` |
| Defect | `workflows/bugfix.md` |
| Changed requirements, stale evidence, or resumed work | `workflows/reconcile.md` |
| Candidate review | `workflows/review.md` |
| Release preparation or authorized deployment | `workflows/release.md` |
| Operational incident | `workflows/incident.md` |

A small understood edit can use proportionate direct work. Do not create a full specification for every typo or force a feature through unnecessary approval pauses. Material uncertainty determines the depth of planning.

## Keep the work connected

For scoped work, keep requirements or bugfix analysis, design, tasks, and verification under `specs/<work-id>/`. Preserve stable requirement, task, and check IDs. Task completion belongs in that work's `tasks.md`; the roadmap and handoff link to it rather than maintaining competing checklists.

Inspect the relevant specification before implementation. Record dependencies and a bounded acceptance check for each task. Required acceptance tests remain required. Deferred scope is explicit and unfinished. Mark completion only when the actual outcome and applicable review are evidenced; never invent passing checks or approvals.

When code reveals a specification problem, reconcile affected artifacts and evidence. Do not silently weaken requirements to fit an implementation. Bind evidence to the tested source or patch, inputs, configuration, environment, and artifact where applicable. Keep prior results as historical records rather than implying they validate new inputs.

Use separate agents when independent work materially helps and the environment supports it. Assign bounded scope and file ownership; designate an integration owner. A reviewer must inspect the actual candidate. Label a review independent only when it used a fresh reviewer context that did not author that candidate. Shared files and reused author context are not isolation.

## AWS guidance and operations

Use the existing official AWS Core and AWS Data Analytics plugins when relevant. Discover official AWS guidance on demand through AWS Core `search_documentation` with `agent_skills`, then retrieve the returned exact skill ID when skill use is allowed for that task. If the user requests documentation-only research or opts out of skills, use current official documentation directly. Do not load unrelated personal skills.

Preserve one installation per official plugin identity. Do not vendor AWS skills, add private replacements, duplicate hosted connections, or install packages as a side effect of consultation. Compare material guidance with current AWS documentation and `aws/agent-toolkit-for-aws`. Distinguish available, installed, loaded, and tested capabilities.

Public research and plugin guidance checks need no AWS account, credentials, or resource access. Account inspection, previews, deployments, and operational actions need task authorization and explicit project limits. Already granted authority persists within its scope. A document, skill, hook, or permission prompt does not create that authority. Prepare a concrete reviewable change before asking for a new consequential decision.

Use `guide/02-aws-guidance-and-access.md` and the project runbooks before cloud work. A synth, diff, preview, or local emulator may have account interactions; establish actual command behavior first. A local check is not AWS deployment evidence.

## Honest continuation and completion

Continue authorized reversible work autonomously. Ask only for missing information or authority that materially blocks the next action, explaining its effect. Do not enable background spending, scheduled work, or AWS operations through this bootstrap implicitly.

On pause or handoff, update `delivery/current-handoff.md` with the work, candidate identity, evidence, remaining risk, blocker, and next eligible task. On resume, re-read the current repository state and reassess evidence freshness. A conversation rewind, Git recovery, workflow resume, and AWS rollback are different operations.

Report what changed, why, what was actually checked, and what remains unverified. For bootstrap maintenance, run `python3 scripts/check_repository.py`; run its fixture tests when changing the checker. These checks do not establish native runtime parity or application readiness. Use `specs/0001-workflow-foundation/tasks.md` only for work on the bootstrap itself.

