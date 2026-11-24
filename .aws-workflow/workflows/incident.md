# Incident

## Trigger

Use this procedure when a running service is failing, degraded, exposing unexpected behavior, or violating a meaningful operational threshold. A suspected issue is not yet a confirmed cause.

## Inputs

- Observed symptoms, times, affected users/paths, environment, and known recent changes.
- The current release record, approved operating/recovery runbooks, and available evidence links.
- Explicit incident authority: permitted account access, changes, recovery actions, cost limits, and escalation owner.
- Relevant requirements and service acceptance thresholds.

## Stages

1. **Establish impact and authority.** Record what is observed and what remains unknown. Identify the service/environment and permitted response actions. Use the current handoff and runbooks; do not improvise access or permissions.
2. **Collect focused evidence.** Inspect available signals within scope and build a timestamped timeline. Consult current official AWS guidance through the existing plugins where needed. Store concise findings and protected external links rather than secrets, personal data, or raw log dumps.
3. **Form and test hypotheses.** Compare symptoms with recent changes and known failure modes. Prefer diagnostic actions that distinguish plausible causes. Separate correlation, reproduction, and verified causation.
4. **Select mitigation.** Use an applicable approved runbook or prepare a concrete recovery action with expected effect, risks, cost, and verification. Recovery may be rollback, forward correction, traffic change, or another project-specific action; document why it fits the observed failure.
5. **Execute within authority and verify.** Perform only authorized actions. Observe the actual service outcome against recovery criteria and check for secondary effects. A command completing is not evidence that users recovered.
6. **Stabilize and follow through.** Record the incident outcome and unresolved risk. Use [Bugfix](bugfix.md) for the durable correction and [Reconcile](reconcile.md) for changed specifications or invalid evidence. Update the runbook with verified learning and create bounded follow-up tasks.

## Outputs

- A concise incident record under `evidence/<work-id>/`, with timeline, impact, hypotheses, actions, and recovery evidence.
- Updated `delivery/current-handoff.md` and relevant release/runbook links.
- Scoped repair and prevention tasks with explicit acceptance criteria.

## Completion evidence

The agreed recovery criteria are observed for the defined validation period, or the remaining impairment is explicitly handed off. The record distinguishes mitigation from verified root cause and permanent correction. Prior release/acceptance claims affected by the incident are reassessed rather than silently retained.

## Continue, pause, and resume

Act promptly within existing incident authority. Escalate only the decision or access needed for the next consequential action; do not repeat already granted permissions. If blocked, preserve observed state and the safest useful next diagnostic step. Resume from the current incident timeline, checking for changes made by other responders.

## Recovery boundary

Repository checkpoints and conversation rewind do not reverse AWS effects or restore database state. Follow the project's actual operating procedures and verify data recovery separately.
