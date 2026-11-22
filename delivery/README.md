# Delivery

**Status:** Delivery contract only. CI/CD provider, runnable workflows, environment protection, and cloud identities remain unconfigured.

This area connects reviewed implementation to a verified release. Preserve the project’s selected delivery system. A greenfield project must record its provider and promotion strategy before runnable automation is added. The framework’s implementation backlog is [the workflow foundation task list](../specs/0001-workflow-foundation/tasks.md); delivery records do not duplicate that task authority.

Keep resumable working state in [current-handoff.md](current-handoff.md). Create each `releases/<release-id>.md` from [the release template](../templates/release.md), linking compact records in `evidence/<work-id>/` and external CI evidence.

## Adopt an existing delivery system

For brownfield work, inventory the current source-to-build-to-deploy path, artifact registry, environment configuration, identities, required checks, approvals, and rollback procedure. Record evidence and unknowns before proposing a change. Repository adoption alone does not authorize a release or replacement pipeline.

Use existing check commands and delivery entry points where they remain suitable. Plan any change to pipeline ownership, artifact format, state backend, environment mapping, or trigger behavior as a scoped migration. Evaluate duplicate deployment triggers, mismatched artifact/configuration revisions, and the ability to recover using the previous path. Do not enable a second pipeline against the same environment as an unreviewed side effect of installing this scaffold.

## Release contract

Apply this contract to the selected project and release. Record an explicit reason and supporting evidence for any item marked **not applicable**. This does not waive a required project gate, review, or acceptance check. Preserve exact source, configuration, and target identities.

Each release identifies:

1. The requirement/specification and task, plus the PR or other review record required by the project.
2. The full source commit and, when the release includes a built artifact, its immutable version or image digest.
3. Required check results and build provenance when a build is part of the release.
4. The versioned environment configuration and secret references.
5. Target environment/account/region, deployment identity, and accepted execution path.
6. The reviewed plan/change-set identity and its source revision, inputs, and creation time when infrastructure changes or project controls require a preview.
7. Cost impact, migration/recovery conditions, authorization, and post-deployment evidence.

Promote the reviewed artifact. If the selected architecture requires environment-specific builds or configuration, record the mapping and verify exactly what is released. Do not rebuild silently after approval or treat a mutable image tag as sufficient release identity.

## Planned stages

| Stage | Required output |
| --- | --- |
| Validate | Relevant static, unit, integration, and policy-check evidence |
| Build | Immutable artifact and provenance tied to the reviewed commit, when a build is part of the release |
| Preview | Target-specific infrastructure/configuration change evidence when applicable; otherwise a reason and supporting evidence |
| Review | Project-required review completed, with findings resolved or explicitly recorded and recovery/cost impact assessed; independent review when required |
| Release decision | Applicable project gate satisfied for the concrete release |
| Deploy | Actual pipeline/run result and resulting version |
| Verify | Critical journey, integration, telemetry, migration, and health observations |
| Reconcile | Updated task/release record and runbooks; explicit remaining work |

A preview is not universally read-only or account-free, and it does not guarantee deployment success. Account inspection, preview creation, asset publication, execution, and post-deployment probes have distinct permissions and effects. See [AWS access](../guide/02-aws-guidance-and-access.md).

## Future automation requirements

When automation is implemented, document event triggers, trusted inputs, permissions, target selection, concurrency, time/retry limits, cancellation, evidence retention, and failure handling. Use temporary identities and protected release boundaries supported by the chosen provider. Give untrusted PR checks no deployment identity.

Make deterministic checks enforceable in CI; use the agent to interpret evidence and fix scoped failures. Agent review, an unchecked checkbox, or a successful command alone cannot satisfy a missing acceptance test. Require a recorded reason for a skipped check.

Routine authorized repository work should proceed without repeated approval. Complete the release package before a required deployment decision. Material changes to the target, artifact, configuration, cost, or destructive effects require reevaluating the scope and relevant gate.

## Operational handoff

Use the [deployment](../runbooks/deploy.md), [rollback](../runbooks/rollback.md), [incident](../runbooks/incident.md), and [teardown](../runbooks/teardown.md) procedures. Record what was planned, implemented, tested, deployed, and observed as separate states.

## References

- [CloudFormation change sets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html)
- [AWS credentials action and short-lived OIDC](https://github.com/aws-actions/configure-aws-credentials)
- [AWS CodePipeline concepts](https://docs.aws.amazon.com/codepipeline/latest/userguide/concepts.html)

