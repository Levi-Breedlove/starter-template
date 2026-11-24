# Incident runbook template

**Status:** Planned. Populate service-specific signals, owners, and recovery actions before operational use.

## Incident record

- Identifier and start time: `<incident reference and time>`.
- Affected service/environment and user impact: `<observed scope>`.
- Owner and authorized actions: `<person, inspection scope, mitigation scope>`.
- Signals and evidence location: `<alarms, logs, traces, user reports, sanitized references>`.
- Current status and next update: `<state and agreed update point>`.

## Response

1. Establish the observed impact, onset, recent changes, and healthy comparison. Separate facts from hypotheses.
2. Inspect only authorized resources using the project’s scoped identity. A read-only investigation still needs account authorization; existing authorization persists within its scope.
3. Preserve useful evidence and construct a short timeline. Avoid collecting unnecessary sensitive data or placing credentials in logs.
4. Test the leading hypothesis with the smallest useful check. Record what each result establishes and what remains uncertain.
5. Apply an authorized prepared mitigation, such as the [recovery procedure](rollback.md). Request a specific decision if the required action exceeds scope; do not broaden permissions to bypass the blocker.
6. Verify recovery through user-visible behavior and relevant telemetry for `<observation window>`. Do not infer recovery solely from a command’s exit status.
7. Record the cause where established, contributing conditions, residual risk, and follow-up tasks with acceptance criteria.

## Communication and follow-up

Draft status updates from observed facts. Sending messages to other people requires explicit authorization. The incident record should link the affected specification, release, code change, and verification evidence. Update runbooks or checks when the incident exposes a concrete gap; preserve unresolved questions rather than inventing a root cause.

## Reference

- [AWS Well-Architected operational excellence](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html)

