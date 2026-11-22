# Deliver the first feature

The [feature procedure](../workflows/feature.md) is the operating contract. Codex owns the investigation and engineering recommendations; the user resolves product or authority decisions that cannot be established from existing evidence.

## Choose a route and preserve context

| Starting point | Route | Review sequence |
| --- | --- | --- |
| New user behavior drives the solution | Requirements-First | Requirements, design, then task plan. |
| Established architecture or a supplied design constrains the change | Design-First | Design, derived requirements checked against the goal, then task plan. |
| Bounded scope is understood after initial clarification | Quick Spec | Draft all three documents, then review the combined scope. |
| Existing behavior is defective | Bugfix | Defect/expected/preserved contract, fix design, then task plan. |
| A bounded change needs exploration before a decision | Plan-led | Concise plan with outcomes, affected surface, checks, and remaining decisions. |

The selected route is recorded with the work. It does not automatically change the Codex application's mode. The CLI's `plan` route ends with a planning result, `planned`; link subsequent implementation work when it needs tracked execution stages. Respect any actual read-only mode and persist at an authorized write handoff.

Read the mapped project brief, existing answers, relevant code, and handoff before opening a new item. A work directory under `specs/` contains substantive Markdown plus `work.json` indexing context, questions, artifact identities, review decisions, and evidence. Dependencies and task completion remain authoritative in `tasks.md`.

## Build the specification through consultation

Use the [consultation interview](06-consultation-interview.md). Ask one to three material questions per round, save answers, and refine drafts as you go. Do not ask which service or database to use when requirements and research support an engineering recommendation. Label reversible planning assumptions and expose decisions with real business consequences.

Start from the [requirements](../templates/requirements.md), [design](../templates/design.md), and [tasks](../templates/tasks.md) templates, or the [bugfix template](../templates/bugfix.md). Correct relative links when copying. The CLI creates an initial skeleton; it does not supply missing product policy or prove that a design is sound.

Requirements identify the actor, condition, observable outcome, relevant limit, failure behavior, and preserved contracts. Analyze the whole set for contradictions, undefined terms, incompatible limits, unstated prerequisites, and concurrent or partial-failure cases. Resolve technical findings from evidence; ask the user only about the remaining material decisions.

Design explains components, contracts, data, errors, security boundaries, operating consequences, cost assumptions, and verification. Link established decisions and research material AWS claims through [official guidance](02-aws-guidance-and-access.md). For brownfield work, specify the smallest changed surface and preserve existing architecture and ownership.

## Perform and record actual phase reviews

Follow the route's review sequence. A review inspects the current artifact and records findings, outcome, reviewer, and the decision or delegation supporting continuation. Standard routes retain their phase reviews; Quick Spec uses one combined review after upfront clarification and drafting all three artifacts.

Present the material scope and tradeoffs in plain language. When an actual decision is needed, ask about that concrete result. When existing authorization delegates the choice, perform the review and continue under that authority. Do not turn every phase into a new permission request. Do not translate silence, generated text, or author self-review into user acceptance or an independent review.

The local `review` command records an actual decision and binds it to the current artifacts. Its `accepted` outcome may record a user decision or a review under real delegated authority; it does not authenticate either. Write the review notes first, then record their source with the CLI. A substantive change can make the recorded snapshot stale and require reconciliation. Task-plan snapshots exclude routine completion, activity, and evidence updates so recording progress does not itself invalidate the plan.

## Generate an implementable task graph

Every task needs a bounded outcome, explicit requirement/design links, prerequisites, scope, acceptance, checks, and evidence obligations. Preserve the template's task heading, checkbox, and labeled fields. List each ID explicitly rather than using "all" or a range. Check that prerequisites exist, no dependency cycle exists, and every required requirement is covered.

Optional techniques and optional product scope are distinct from required outcomes. Property-based testing may be useful for an invariant, but example, integration, contract, or operational checks may be more appropriate. A required behavior still needs evidence whichever technique is chosen.

Run read-only local checks from the adopted project root:

```bash
python3 .aws-workflow/scripts/workflow.py --root . context
python3 .aws-workflow/scripts/workflow.py --root . status
python3 .aws-workflow/scripts/workflow.py --root . validate
```

These inspect the recorded workflow, task graph, coverage, and phase evidence. They do not independently establish requirement quality, real approval, test success, or AWS behavior. The separate repository checker validates local Markdown links and required structure only. See [tool usage](../scripts/README.md) for exact supported commands.

## Implement, review, and finish at the correct boundary

Read the relevant contract before each task. Work in small changes and parallelize only separable scopes with a clear integration owner. Record actual results against the candidate revision, configuration, and environment. A local patch needs a patch identity in addition to its base commit. Shared files and shared conversation history do not make a review independent.

Use [Reconcile](../workflows/reconcile.md) when answers, design, implementation, or environment assumptions materially change. Reopen invalidated completion and refresh affected reviews and evidence. Preserve useful completed work whose acceptance is still valid.

Use [Review](../workflows/review.md) on the integrated candidate and resolve blocking findings. Finish with achieved behavior and its evidence, plus explicit pending obligations. If deployment is authorized, continue through [maintenance and release](04-maintain-and-release.md). A reviewed specification, completed implementation, release-ready artifact, successful deployment, and verified user outcome are separate states.

See [consultation examples](../examples/consultation/README.md) for the discussion that creates a spec, and [booking retries](../examples/booking-retries/README.md) for acceptance traceability.
