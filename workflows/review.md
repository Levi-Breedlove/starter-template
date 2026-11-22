# Review

## Trigger

Use this procedure when a concrete specification, implementation candidate, or release package is ready for scrutiny. Specify which kind of review is being requested; a design review cannot establish deployed behavior.

## Inputs

- The exact candidate revision and relevant comparison/base revision, or a clearly identified document draft.
- Accepted requirements, design, scope, and authorization boundaries.
- Actual diff, task record, verification evidence, and relevant cost/security/runbook changes.
- Known limitations and unresolved findings; the author's explanation is useful context, not proof.

## Stages

1. **Declare the review basis.** Record reviewer identity/role, candidate, scope, and access limitations. Use a fresh reviewer who did not author the candidate when an independent review is required. Supply the accepted contract, actual diff, and evidence for direct inspection.
2. **Inspect behavior and fit.** Evaluate whether the change meets requirements, preserves intended behavior, fits accepted architecture, and handles failures. Check the design/implementation boundary rather than reviewing file style alone.
3. **Assess evidence.** Inspect check results and their revision/environment. Identify missing critical cases or stale results. Run focused permitted checks only when they resolve a material uncertainty; do not claim they ran when only their definition was inspected.
4. **Record actionable findings.** Each finding should identify the affected behavior, supporting evidence, impact, and recommended correction. Separate blocking defects from suggestions and uncertainty. Avoid speculative issues without a plausible path to impact.
5. **Resolve and recheck.** The implementer fixes accepted findings. Review the resulting candidate and rerun affected checks. Material changes to the specification or implementation require [Reconcile](reconcile.md); old review evidence does not automatically apply to a new candidate.
6. **State the outcome.** Record remaining limitations and whether the reviewed scope is ready to proceed. A passing review does not establish deployment success or grant authority to deploy.

## Outputs

- A lightweight review record in `evidence/<work-id>/`, or a link to the authoritative PR review.
- Findings and resolution evidence tied to the final candidate revision.
- Any necessary task updates and a handoff to integration or release preparation.

## Completion evidence

The named reviewer inspected the stated candidate and the relevant evidence. Blocking findings are resolved or an authorized decision explicitly addresses them. The record states whether review was independent, assisted, or self-review; a second prompt from the author is not automatically independent review.

## Continue, pause, and resume

Continue authorized fixes and focused rechecks. If an independent reviewer is unavailable, report the review actually performed and leave the independence claim pending; do not fabricate a reviewer or result. Pause only if a required review gate cannot be satisfied or a material decision remains. Resume using the latest candidate and finding list.

## Related contracts

[Feature](feature.md), [Bugfix](bugfix.md), [Reconcile](reconcile.md), and [Release](release.md). This review contract is a proposed repository control, not a claim that either product automatically enforces it.
