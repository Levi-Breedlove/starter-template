# Bugfix

## Trigger

Use this procedure for a defect whose cause, impact, or regression risk warrants explicit analysis. Begin with [Incident](incident.md) if service restoration is urgent. An obvious minor correction can use a shorter record with proportionate verification.

## Inputs

- Reproduction steps, observed symptoms, expected outcome, and affected versions/environments.
- Relevant specifications, logs or external evidence links, recent changes, and current handoff.
- Constraints on data, compatibility, architecture, and behavior that must remain intact.
- Authorized diagnostic and change scope. Account-specific inspection requires its own authorization.

## Stages

1. **Define the defect.** In `specs/<work-id>/bugfix.md`, describe current incorrect behavior, expected behavior, and explicitly preserved behavior. Separate observations from hypotheses.
2. **Establish reproduction.** Reproduce in an appropriate permitted environment or document why reproduction is unavailable. Capture a failing check or equivalent evidence without publishing secrets or raw sensitive logs.
3. **Find the cause.** Inspect the actual code/configuration path and test competing explanations. Use official AWS guidance when relevant. A plausible explanation is not a verified root cause.
4. **Design the smallest adequate correction.** Record the cause, changed behavior, affected components, risks, and verification approach in `design.md`. If substantial new capability is necessary, create linked feature work rather than hiding it inside the fix.
5. **Implement and test.** Generate scoped tasks with dependencies and checks that demonstrate the defect, the correction, and preserved behavior. Use property-based tests only where useful. Do not weaken a legitimate acceptance condition merely to obtain a passing test.
6. **Review and reconcile.** Review the actual candidate; resolve material findings; update specifications and task evidence. If deployment is requested, use [Release](release.md) with the appropriate recovery plan.

## Outputs

- `bugfix.md`, `design.md`, and `tasks.md` with linked evidence and explicit preservation conditions.
- A scoped patch and relevant regression checks.
- Updated runbook or incident follow-up when the defect changes operational guidance.

## Completion evidence

The recorded evidence supports the cause and correction, and required preservation checks pass for the candidate revision. If the original defect could not be reproduced, state that limitation and the evidence supporting the proposed fix. Code completion and deployed recovery remain distinct claims.

## Continue, pause, and resume

Continue routine diagnosis and reversible work within scope. Pause when a necessary action exceeds authorization, the cause is too uncertain to justify a consequential change, or required evidence is inaccessible. Save the strongest observations, rejected hypotheses, candidate revision, and next diagnostic step in the handoff. Recheck environmental assumptions when resuming.

## References

[Kiro Bugfix Specs](https://kiro.dev/docs/specs/bugfix-specs/) document defect, expected, and unchanged behavior. [Spec best practices](https://kiro.dev/docs/specs/best-practices/) distinguish complex fixes from small direct changes. The integrated correctness feature has the limits described in [the capability reference](../docs/reference/kiro-capabilities.md).
