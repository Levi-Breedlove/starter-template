# Reconcile

## Trigger

Use this procedure after changed requirements or design, work completed in another session, review findings, an implementation discovery, or a mismatch between task status and evidence. Also use it when resuming work after the repository or target environment has changed.

## Inputs

- The current brief, decisions, specification, task record, code revision, and handoff.
- The change that prompted reconciliation and the last verified baseline.
- Relevant acceptance evidence, review records, and external CI/deployment links.

## Stages

1. **Establish the current baseline.** Inspect the actual branch/revision and uncommitted work. Determine which records are authoritative and which are historical. Preserve other contributors' changes.
2. **Identify the mismatch.** Classify it as changed intent, changed design, missing implementation, previously completed work, stale task status, or stale/insufficient evidence. Do not assume that code automatically defines the intended requirement.
3. **Resolve the direction.** For Requirements-First, update accepted requirements, then design, then tasks. For Design-First, revise the accepted design, validate derived requirements, then tasks. If the change is still proposed, retain that status and seek only the material decision needed.
4. **Assess impact.** Trace affected requirements through components, tasks, tests, cost/security records, runbooks, and releases. Mark affected evidence stale. Preserve old results as history; retain unaffected evidence only with a reason it remains applicable.
5. **Repair the task record.** Reuse valid completed work. Add or revise only affected tasks and dependencies. A detected implementation can satisfy a task's coding step while its acceptance checks remain outstanding. Reopen completion claims that no longer hold.
6. **Reverify and hand off.** Run the necessary available checks for the new candidate, update evidence links, and request [Review](review.md) where the changed scope warrants it. Save one current continuation point.

## Outputs

- An explained specification/design/task diff and any required decision record.
- A record of which claims remain valid, became stale, or were reverified.
- Updated task dependencies and `delivery/current-handoff.md`.

## Completion evidence

The authoritative artifacts agree on current intent and implementation status. Each required claim is supported by applicable evidence or is visibly pending. No previously completed task is silently dropped, and no unverified code is treated as a verified result.

## Continue, pause, and resume

Reconcile routine changes without restarting the entire project plan. Pause only where conflicting authoritative decisions require a choice or a required check needs unavailable access. On resume, use the saved baseline and impact assessment, confirm what changed since, then continue the next affected task.

## Reference

[Kiro spec best practices](https://kiro.dev/docs/specs/best-practices/) describes Sync Files and the different update order for Requirements-First and Design-First. This repository implements the practice through explicit review and edits; it does not provide a native Sync Files command.
