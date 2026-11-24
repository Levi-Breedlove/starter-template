# Runbooks

These are **procedure templates**, not executable automation or evidence of a deployed system. Fill in the selected project’s targets, commands, identity, preconditions, and verification before use. Keep placeholders visibly unresolved.

| Procedure | Purpose |
| --- | --- |
| [Deploy](deploy.md) | Release a reviewed artifact and verify operation |
| [Rollback](rollback.md) | Recover from a failed release or choose a forward fix |
| [Incident](incident.md) | Investigate and restore service within authorized scope |
| [Teardown](teardown.md) | Remove scoped resources while preserving required data |

Each completed run records who authorized it, the relevant scope, start/end time, release or incident identifier, actions, observed results, and unresolved items. Link sanitized `evidence/<work-id>/` records to `specs/<work-id>/tasks.md` and the release under `delivery/releases/`. Reuse existing authorization; a runbook does not grant additional authority.

Maintain runbooks alongside implementation and update them when behavior changes. Validate recovery procedures in an appropriate authorized environment before describing them as tested.

