# Maintain, release, and continue

A useful workflow remains coherent when requirements change, a session stops, review finds a defect, or an AWS release fails. Use the existing delivery system and strengthen missing evidence rather than replacing the pipeline by default.

## Change an existing specification

Use [Reconcile](../workflows/reconcile.md). Identify the changed requirement, assumption, source, or environment. Update its downstream design and tasks, preserve stable identifiers, and reassess only the affected evidence. Keep valid prior results with their actual scope. Do not treat a regenerated task list as proof that code now matches a changed specification.

## Resume a session

Read the current handoff, relevant tasks, worktree state, latest candidate, and evidence. Determine whether a previous action completed before repeating it. Continue the next unblocked task within existing authorization. If an external operation's outcome is unknown, inspect its status using authorized access; do not replay it merely because the conversation lost its response.

The planned durable adapter will record node state and operation identifiers. Until implemented, continuation is an explicit repository procedure. Git protects versioned file history; a chat checkpoint or conversation fork is not infrastructure recovery.

## Prepare the release candidate

Use [Release](../workflows/release.md) and the [release template](../templates/release.md). Identify the source or patch, built artifact, environment configuration, IaC candidate, target scope, verification, review, and recovery method. Prepare cost assumptions and operational acceptance before asking for a consequential decision that has not already been made.

Distinguish a locally validated template, a connected preview, an applied deployment, and a working service. AWS diff and synth commands can access accounts or publish artifacts depending on their mode. Follow [AWS guidance and access](02-aws-guidance-and-access.md) and the actual [deployment runbook](../runbooks/deploy.md).

If a pipeline already enforces required reviews and checks, retain that authority. A local report does not replace a required CI result. After authorized deployment, check the user-facing behavior and relevant metrics, then record the observation and limitations. Do not mark a release successful solely because a deployment command exited successfully.

## Recover and learn

Use the [rollback](../runbooks/rollback.md) and [incident](../runbooks/incident.md) runbooks for their actual targets. Data migrations, irreversible changes, replacement resources, and stateful dependencies may require roll-forward or restoration rather than a previous application build. Define those choices in the design before relying on them.

Record follow-up work as a focused bugfix or feature, update runbooks where observations changed them, and update the current handoff. Cleanup follows the [teardown contract](../runbooks/teardown.md) and ownership records; it does not infer deletion authority from a bootstrap label.

