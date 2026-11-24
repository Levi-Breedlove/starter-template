# Deployment runbook template

**Status:** Planned; no target, pipeline, or deploy command is selected. Start the release record from [the release template](../templates/release.md) and store it under `delivery/releases/<release-id>.md`.

Apply the selected project's release process. Mark an item **not applicable** only with an explicit reason and supporting evidence; this cannot waive a required gate, review, or acceptance check. Always establish the exact source, configuration, target, authority, and meaningful post-deployment verification.

## Release identity

| Field | Value |
| --- | --- |
| Specification / task / review | `<references; PR or other review record as required by the project>` |
| Source commit | `<full reviewed commit SHA>` |
| Built artifact | `<immutable artifact version or image digest, when the release includes a built artifact>` |
| Build provenance | `<build run and evidence, when a build is part of the release>` |
| Configuration source | `<versioned configuration reference and secret references>` |
| Target environment/account/region | `<explicit approved target>` |
| Deployment identity / pipeline | `<role and selected pipeline>` |
| Preview identity | `<change-set/plan identifier, source revision, time, target, when a preview applies>` |
| Authorization | `<existing decision and exact authorized scope>` |

## Prepare the reviewable release

1. Confirm the requirement and acceptance criteria, supported test results, project-required reviews, and unresolved risks. Use an independent reviewer when required by the project or release scope.
   For a brownfield release, identify the current version and ownership, existing pipeline, stateful dependencies, and any adoption/migration prerequisites.
2. When infrastructure changes or project controls require a preview, generate it through the selected tool under authorized access. Review applicable replacements, deletions, identity changes, public exposure, and data migration effects. If a preview does not apply, record the reason and evidence.
3. Record estimated cost changes, recovery procedure, last known good artifact/configuration, and required backups.
4. Bind any applicable preview and artifact to the source, configuration, and target above. If those inputs change or evidence is stale, refresh the affected evidence and obtain any materially changed release decision.
5. Complete the project’s release gate using this evidence. Do not ask again when the release remains within an already granted authorization and the actual control permits execution.

## Execute and observe

1. Verify the target and effective identity within the authorized scope. Avoid logging credentials.
2. Run `<approved pipeline action or exact reviewed command>`. This placeholder is deliberately not executable.
3. Follow the deployment to a terminal state and record the actual run identifier and result.
4. Verify `<health endpoint or user journey>`, `<authorization behavior>`, `<critical integration>`, and `<telemetry/alarm checks>`. Specify any synthetic transaction’s data effect and cleanup.
5. Compare the observed release and configuration with the intended identity. Apply the [rollback procedure](rollback.md) if its trigger is met and the recovery action is authorized.

## Completion evidence

Record deployed artifact/configuration identity, infrastructure result, smoke-test results, observation window, alarm state, migration outcome, costs/cleanup follow-up, and remaining limitations. Link compact sanitized evidence from `evidence/<work-id>/` and external CI results. A successful build, deployment command, or PR is insufficient evidence of working service. Close the task in `specs/<work-id>/tasks.md` only when its acceptance criteria are supported; otherwise report the exact incomplete criterion. Refresh [the current handoff](../../delivery/current-handoff.md).

## References

- [Delivery contract](../delivery/README.md)
- [CloudFormation change-set behavior and limits](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html)

