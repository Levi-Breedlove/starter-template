# Bugfix

## Trigger

Use this procedure when a defect's cause, impact, or regression risk warrants explicit analysis. Begin with [Incident](incident.md) when restoration is urgent. An obvious minor correction can use a shorter record and proportionate checks.

## Inputs

- The reported symptom, reproduction information, expected result, and affected versions/environments.
- Relevant requirements, current code, recent changes, existing evidence, and the current handoff.
- Behavior, data, compatibility, architecture, and resource ownership that must be preserved.
- Actual authorization for diagnosis and changes; public AWS guidance does not authorize account inspection.

## Stages

1. **Inspect before asking.** Read the report, relevant contracts, implementation, and existing checks. Separate observed failure from hypotheses and intended behavior. Recover known answers from evidence. Ask one to three focused questions only when missing business intent, an inaccessible symptom, or another material gap blocks diagnosis. Explain what the answer changes; save it in `bugfix.md`.
2. **Define and review the defect contract.** In `specs/<work-id>/bugfix.md`, record current incorrect behavior, expected behavior, and explicitly preserved behavior with stable identifiers. Describe affected and unaffected inputs. Review this contract against the report and available evidence before designing the fix. Record the reviewed revision, findings, reviewer, and actual acceptance or delegated authority; do not invent confirmation.
3. **Establish reproduction and cause.** Reproduce in a permitted environment or state precisely why reproduction is unavailable. Capture a failing check or equivalent sanitized evidence. Inspect the actual code/configuration path and test competing explanations. Consult [official AWS guidance](../guide/02-aws-guidance-and-access.md) when relevant. Record rejected hypotheses and the evidence supporting the cause; a plausible story alone is not verification.
4. **Design and review the correction.** In `design.md`, describe the smallest adequate change, affected components, risks, and checks demonstrating the defect, correction, and preserved behavior. If new functionality is needed, link separate feature work. Review the design against the defect contract and preservation obligations; record its revision, findings, outcome, and transition authority.
5. **Generate tasks and implement.** Create bounded tasks with dependencies and reproduction, correction, and regression checks. Check coverage before implementation. Use property-based tests where they strengthen relevant claims; the technique is optional, required behavior is not. Continue authorized local work after the actual reviews without per-file permission requests.
6. **Review the candidate and reconcile.** Run [Review](review.md), resolve blocking findings, and rerun affected checks. If new evidence changes the expected behavior or fix approach, use [Reconcile](reconcile.md) and revisit only affected reviews. Update operating guidance when needed. Use [Release](release.md) for an authorized deployment.

The [specification operations](../docs/reference/specification-operations.md) support this sequence directly. `analyze` prepares a source-bound review of the defect, correction and preservation contract; Codex supplies and records actual findings. `properties` asks Codex to derive reproduction, correction and preservation checks from the contract/design and validates the returned task/check mapping. It supports a generated-input strategy when useful, while preserving other appropriate test techniques. Neither operation runs a test or turns an unconfirmed cause into a fact.

## Outputs

- `bugfix.md`, `design.md`, and `tasks.md` with diagnostic answers, actual review records, and preservation checks.
- A scoped patch and applicable evidence, with hypotheses distinguished from verified observations.
- Updated runbook or incident follow-up where operational guidance changes.

## Completion evidence

The evidence supports the correction and required preservation checks for the current candidate. If the original failure could not be reproduced, state that limitation and the alternative evidence supporting the fix; do not claim a passing before/after experiment. Unperformed required checks remain pending. Code completion and verified deployed recovery remain distinct.

## Continue, pause, and resume

Continue routine diagnosis and reversible work within scope. Pause only dependent work when an action exceeds authorization, the cause is too uncertain for a consequential change, an actual review decision is unresolved, or necessary evidence is inaccessible. Save answers, strongest observations, rejected hypotheses, candidate identity, and the next diagnostic step. Resume by checking changed assumptions instead of repeating the entire interview.
