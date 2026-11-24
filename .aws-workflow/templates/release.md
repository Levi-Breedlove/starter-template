# Release: <release ID>

**State:** Proposed; no deployment performed.
**Scope:** <work IDs and release outcome>
**Owner / executor:** <responsibilities>

Apply the selected project's release process. Mark an artifact, preview, or review **not applicable** only with an explicit reason and supporting evidence. This cannot waive a required project gate, review, or acceptance check. Always establish exact source, configuration, target, and authorization; record meaningful verification after execution.

## Candidate and target

| Field | Value or remaining obligation |
| --- | --- |
| Source revision | <exact commit; not selected> |
| Application artifact | <immutable version or digest when the release includes a built artifact; otherwise justified not applicable> |
| Target environment | <development/staging/production; not selected> |
| AWS account, Region, and role | <approved environment reference; do not inspect to fill this without authorization> |
| Environment configuration | <reviewed identity or digest> |
| Infrastructure preview | <exact reviewed plan/change-set reference and inputs when infrastructure changes or project controls require it; otherwise justified not applicable> |
| Existing execution authority | <actual authorization reference, scope, limits, and exclusions; absent until provided> |
| Required checks and reviews | <specific task and project-required CI/review evidence; independent review when required> |

When promoting a built application artifact, use the same reviewed artifact. Review target configuration and applicable infrastructure plans for their own environment. A changed candidate or target requires checking whether the existing authorization and evidence still apply.

## Impact and recovery

- Resource additions, modifications, removals, and replacements: <reviewed impact>.
- Identity, network exposure, data, and retention changes: <impact>.
- Estimated cost and assumptions: <cost record>.
- Migrations and compatibility: <sequence and backward/forward compatibility>.
- Recovery procedure and trigger: <runbook reference, including data recovery>.
- Health and smoke checks: <procedure and expected observations>.
- Observation period and owner: <project-selected criteria>.
- Temporary resource cleanup: <scope and retention rules>.

## Release decision

Candidate readiness: <not assessed / ready within stated limits / blocked>.

Authorization: <not granted / existing task authorization covers this exact scope / actual new decision reference>. Prepare reviewable evidence before requesting a missing consequential decision. Do not ask again when the same scope is already authorized.

## Actual outcome

- Accepted execution/run and deployed source/configuration, plus any applicable artifact: Not run.
- Infrastructure result: Not observed.
- Workload verification and telemetry: Not observed.
- Recovery or remaining obligations: Not assessed.
- Reconciled tasks, runbooks, cost records, and current handoff: Not updated for a deployment.

Record actual results after execution. A preview, accepted review, merged PR, or successful platform operation alone does not establish verified workload behavior.
