# Brownfield intake

## Trigger

Use this procedure before adopting the scaffold in an existing application, infrastructure repository, or service. The first result is an evidence-based adoption plan, not an automatic repository restructure or infrastructure migration.

## Inputs

- The existing repository and the user's requested outcome.
- Existing project instructions, requirements, architecture decisions, delivery configuration, runbooks, and task sources.
- Available source revisions, test results, release records, and other supplied evidence.
- Known behavior/data compatibility constraints and the scope of authorized inspection.

## Stages

1. **Inventory without disturbing work.** Inspect the current branch/revision, uncommitted changes, instructions, layout, applications, tests, infrastructure definitions, CI/CD, and operating documentation. Record inaccessible areas. Do not overwrite project instructions or move files to match this skeleton.
2. **Separate current state from intent.** Identify what code and evidence demonstrate, what documents claim, what architecture is accepted, and what the user wants changed. Code can reveal existing behavior; it does not prove that every behavior is intended or correct.
3. **Establish preservation obligations.** Record public interfaces, compatibility, important user behavior, data ownership and retention, migration constraints, identity/network boundaries, and operating requirements. Link source evidence. Use the Bugfix preservation model when diagnosing a defect.
4. **Identify infrastructure ownership.** Inspect the declared IaC tools, stacks/modules, state/backend references, pipeline responsibilities, environments, and ownership boundaries. Separate repository evidence from claims about live resources. Do not query accounts, import resources, bootstrap environments, move state, or change ownership during public/repository intake.
5. **Assess the verification baseline.** Inventory existing test and deployment evidence with its revision and environment. Run permitted local checks only when needed to resolve a concrete uncertainty. Document gaps, including cases where local behavior does not establish AWS behavior.
6. **Map incremental adoption.** In `project/adoption-report.md`, identify which existing artifacts remain authoritative, which scaffold conventions can be linked or adapted, and which changes need a decision. Choose a contained first work item. Avoid duplicate task authorities, blanket refactors, and copying all historical documentation into agent context.
7. **Select the next route.** Use Design-First when established architecture constrains the change, Requirements-First when new behavior drives it, Quick Spec for familiar bounded work, Plan-led work for a small exploration, or [Bugfix](bugfix.md) for a defect. Feed the accepted baseline into [Consult](consult.md) or the selected implementation contract.

## Outputs

- `project/adoption-report.md` with baseline revision, evidence inventory, preservation obligations, infrastructure ownership, uncertainty, adoption decisions, and the first proposed work item.
- An updated brief and links to existing canonical artifacts.
- A current handoff identifying the next action and any material unanswered question.

## Completion evidence

The report distinguishes observed implementation, accepted intent, proposed changes, and unknown live state. Existing task and document authority is explicit. Preservation and migration concerns are recorded. The first work item is bounded and its verification path is clear. No account access or repository reorganization is implied by completion of the report.

## Continue, pause, and resume

Continue repository inspection and authorized documentation work. Pause only when a necessary next action requires account access, spending, a consequential ownership/migration decision, or unavailable evidence. Explain the exact gap and smallest next action. On resume, compare the current revision with the saved baseline and use [Reconcile](reconcile.md) if other work has changed it.

## References

Kiro's [Design-First workflow](https://kiro.dev/docs/specs/feature-specs/tech-design-first/), [spec import and synchronization guidance](https://kiro.dev/docs/specs/best-practices/), and [Bugfix Specs](https://kiro.dev/docs/specs/bugfix-specs/) support adoption into an existing system. The baseline and ownership report is this repository's explicit AWS adoption procedure; it is not an automatic Kiro migration feature.
