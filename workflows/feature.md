# Feature

## Trigger

Use this procedure for new or changed functionality that benefits from an explicit specification. Use [Bugfix](bugfix.md) for a defect. Keep an obvious minor edit proportionate to its risk.

## Inputs

- The scoped goal, saved consultation answers, established constraints, and relevant decisions.
- Current code, existing contracts, the project brief, and current handoff at their mapped project paths.
- Brownfield evidence and preservation obligations where applicable.
- `specs/<work-id>/`, authorized implementation scope, and available verification environments.

## Stages

### 1. Select the route from the work

| Route | Sequence and review boundary |
| --- | --- |
| Requirements-First | Interview and draft observable requirements; analyze and review them; develop and review the design; generate and check the task graph. |
| Design-First | Inspect the established architecture or supplied design; investigate and review the proposed design; derive and review requirements against the user's goal; generate and check tasks. Revisit the design when a missing user need exposes a gap. |
| Quick Spec | Resolve material questions up front; draft requirements, design, and tasks in sequence without separate approval pauses; analyze their consistency and review the combined scope before dependent implementation. |
| Plan-led | Investigate a bounded change and prepare a concise plan with outcome, affected surface, checks, and remaining decisions. Review it and continue under existing implementation authority. Use a full specification when uncertainty or impact justifies one. |

Choose the route; do not ask the user to interpret process labels unless they have a preference. Quick Spec suits understood scope, not unresolved consequential architecture or product policy. Follow the sequence in the table: the sections below describe what each phase must accomplish, not a requirement to write requirements before a Design-First design. A route names this repository's procedure; it does not automatically switch the Codex application's mode. Respect an actual read-only planning mode. Persist its plan at an authorized write handoff. The CLI's Plan route ends at `planned`; start and link implementation work when execution needs its own tracked stages.

### 2. Interview and make behavior precise

Use [Consult](consult.md) throughout planning, not only at project initialization. Read existing answers before asking one to three material questions at a time. Derive engineering implications, research technical uncertainty, and recommend defaults with rationale. Save answers and useful drafts after every round.

Give requirements stable IDs. Describe actors, triggering conditions, required results, measurable limits, failure cases, and preserved behavior. Conditional wording such as "When a valid request is retried, the system must return the original result without creating another reservation" makes a claim checkable. Do not invent business thresholds to fill a template.

Analyze the requirement set for contradictory limits, ambiguous terms, unstated preconditions, dependencies, and concurrency or partial-failure gaps. Record material findings and their resolution. Resolve supported engineering questions directly; return genuine product decisions to the user with a recommendation. A known blocker prevents dependent work from being ready.

### 3. Design the implementation and its evidence

Cover component responsibilities, interfaces, data ownership and lifecycle, request/event paths, errors, security boundaries, operations, costs, and verification at the depth the change needs. Link accepted decisions rather than copying them. Research material AWS guidance through [the existing official toolkit route](../guide/02-aws-guidance-and-access.md). Record sources and estimate assumptions.

For brownfield work, identify the smallest changed surface, compatibility obligations, and any migration/recovery steps. Retain the existing architecture, source layout, IaC ownership, and pipeline unless a separate justified decision changes them.

Express useful correctness properties as observable invariants with preconditions. Select examples, property-based tests, contracts, integrations, infrastructure checks, or operational observations according to the claim. Property-based testing is optional as a technique; **required acceptance outcomes still need appropriate checks**. A mock or emulator does not establish AWS IAM, networking, service behavior, or deployment success.

### 4. Perform the route's reviews

For each review boundary in the route table, inspect the actual artifact and the requirements it must satisfy. Record the artifact revision or content identity, reviewer, findings, outcome, and authority supporting the next transition. Summarize material scope, assumptions, and unresolved decisions for the user.

An explicit user decision can establish product acceptance. An authorized technical review can establish technical readiness. Prior authorization may delegate routine design choices and implementation; continue within it without requesting approval for each file. Do not record a generated document, silence, or author self-check as user acceptance or independent review. If the user reserved a decision or a consequential product gap remains, present the concrete alternatives and pause only dependent work.

For Quick Spec, one combined review covers the three drafted artifacts; do not insert requirements and design approval stops. For a standard route, do not skip its reviews just because task drafting is convenient. Reviews may be performed within existing authority, but they must actually occur and identify who performed them.

### 5. Generate and check the task graph

In `tasks.md`, give each task an independently reviewable outcome, requirement/design links, scope, real dependencies, checks, and completion evidence. Include migration, integration, operations, and verification work where the contract needs them. Mark optional scope explicitly; do not make required tests optional to obtain completion.

Check that all required acceptance conditions are covered, prerequisites exist, dependency cycles are absent, and each next task is implementable. Assign one integration owner when multiple contributors work. Parallelize separate investigations or bounded implementations only when dependencies and file ownership permit it.

### 6. Implement, verify, and review the candidate

Read the relevant specification before each task. Implement small reviewable changes, run checks for the actual risk, and record the tested candidate and environment. Complete a task only when its outcome, required checks, and applicable review are satisfied. Preserve blocked or unverified work visibly.

Use [Reconcile](reconcile.md) when implementation changes the contract or a design assumption. Do not silently weaken requirements to fit the code. Use [Review](review.md) on the integrated candidate, resolve blocking findings, and rerun affected checks. A fresh independent reviewer must actually be separate from the author and receive the candidate and acceptance contract.

## Outputs

- Connected specification documents appropriate to the route, with consultation decisions and phase reviews.
- Scoped implementation, infrastructure, and documentation changes; evidence under `evidence/<work-id>/` or linked CI.
- A current handoff with the candidate, remaining obligations, and next eligible action.

## Completion evidence

Every required acceptance outcome has applicable evidence. An explicit remaining obligation means that outcome is pending, even if the local coding work is finished. Task status matches the inspected candidate and review results. Planning readiness, implementation completion, release readiness, successful deployment, and verified service behavior are separate claims.

## Continue, pause, and resume

Continue authorized implementation and routine checks without repeated permissions. Pause dependent work for unresolved material decisions, changed authorization boundaries, or required inaccessible evidence. On resume, inspect current files and task state, verify that phase reviews and results still apply, and continue the next unblocked task. Proceed to [Release](release.md) when deployment is authorized and its conditions are met.
