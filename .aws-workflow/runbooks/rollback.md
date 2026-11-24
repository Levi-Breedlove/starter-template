# Rollback and recovery runbook template

**Status:** Planned. The project must select and validate its recovery method.

## Prepare

| Field | Value |
| --- | --- |
| Failed release / target | `<release and explicitly scoped environment>` |
| Recovery trigger | `<observable failure and decision threshold>` |
| Decision owner / authorization | `<owner and existing recovery authority>` |
| Last known good artifact/configuration | `<immutable identities>` |
| Recovery method | `<redeploy, traffic switch, restore, or forward fix>` |
| Data compatibility / backup | `<migration constraints and verified restore reference>` |
| Recovery objectives | `<agreed service recovery time and acceptable data loss>` |

## Procedure

1. Preserve the failure evidence and identify the deployed artifact, configuration, and infrastructure state.
   For adoption or migration, include the previous pipeline/state ownership and whether the old deployment path remains usable.
2. Determine whether application rollback is compatible with the current database and external effects. A backward-incompatible migration may require a forward fix or an explicit restore decision.
3. Select the least disruptive prepared recovery action within existing authority. If authority or a necessary prerequisite is missing, report the exact blocker and decision needed.
4. Execute `<reviewed recovery action>` through the selected mechanism. Observe the complete result; do not assume automatic infrastructure rollback succeeded.
5. Verify the critical user journey, data integrity, access controls, and telemetry. Record the actual resulting version and remaining degradation.
6. Update the incident/release record and create bounded follow-up work for the cause and missing prevention checks.

## Recovery boundaries

Git revert and agent file checkpoints recover source/workspace state. They do not undo AWS resources, database migrations, published messages, or other external side effects. Infrastructure rollback also does not imply application-data restoration. Keep these recovery responsibilities explicit.

## References

- [CloudFormation rollback troubleshooting](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/troubleshooting.html)

