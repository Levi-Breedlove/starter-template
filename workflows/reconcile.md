# Reconcile

## Trigger

Use this procedure when a consultation answer, requirement, design, implementation, review finding, environment assumption, or evidence record changes. Use it on resume when another session may have changed the baseline. Synchronization is an explicit inspection and update, not an assumption that documents agree because they exist.

## Inputs

- The current brief, saved answers, decisions, specification, tasks, code, and handoff.
- The triggering change and last reviewed or verified baseline.
- Relevant phase reviews, checks, and external CI/deployment evidence.

## Executable preview and application

Run `scripts/workflow.py sync <work-id>` for an impact preview based on declared review/evidence identities, recorded analysis/property inputs, task dependencies and any explicitly supplied `--changed <path>` values. The result identifies affected artifacts, reviews, checks and tasks; it includes regeneration instructions and an exact preview fingerprint. Inspect the actual changed sources before deciding what the prose should become.

Use `sync <work-id> --apply --expected-fingerprint <value> --reason <actual-reason>` only after that inspection. Repeating `--changed` on application must match the preview. The tool checks freshness again, reopens invalid completion, rewinds the appropriate route boundary and retains history. It does not regenerate prose, weaken scope, discard implementation, approve a decision or claim a check passed. A stale preview fails without applying it.

An updated decision index may require renewed analysis before a contract change is justified. In that case, review is reopened while still-valid completed work remains preserved. If the resulting requirements/design actually change, preview again to identify the downstream verification impact. Reconcile on a stable working tree; there is no cross-process metadata merge or promise of recovery from power loss. See [the operation contract](../docs/reference/specification-operations.md).

## Stages

1. **Establish the current baseline.** Inspect actual revisions and uncommitted work, identify current authority, and preserve other contributors' changes. Read the latest answers and authorization before asking anything again.
2. **Classify the mismatch.** Distinguish changed product intent, changed design, implementation discovery, already completed work, stale task status, and insufficient or stale evidence. Code alone does not define intended behavior; a previous answer may have been superseded.
3. **Resolve the direction.** For Requirements-First, revise requirements, then design, then tasks. For Design-First, revise design, check derived requirements against user needs, then tasks. For Quick Spec, assess the connected set together. For Bugfix, preserve the defect/expected/preserved distinction. Keep a proposed decision proposed until actual authority resolves it.
4. **Interview only material conflicts.** Derive or research technical resolutions first. Present the conflicting evidence, a recommended resolution, and one to three consequential questions if a product or authority decision remains. Record the new answer and which previous decision it supersedes; do not erase the history or restart an intake checklist.
5. **Assess impact on reviews and evidence.** Trace the changed contract through design, tasks, checks, costs, security, operations, and releases. Identify the affected phase reviews and results that no longer support the candidate. Preserve old records as history. Retain unaffected evidence only with a reason it remains applicable.
6. **Repair the task graph and revisit affected reviews.** Reuse valid implementation, update dependencies and checks, and reopen invalid completion claims. Already present code may satisfy a coding step while verification remains outstanding. Review the changed requirements/design or combined Quick Spec at the appropriate boundary. Record who reviewed what and the actual outcome; do not translate prior approval into approval of an unreviewed material change.
7. **Reverify and hand off.** Run available checks needed for the new candidate and use [Review](review.md) where the changed scope warrants it. Record remaining obligations and one current continuation point. Continue within surviving authorization; request a new decision only for a changed boundary or an actual unresolved control.

## Outputs

- An explained diff of the affected answers, requirements, design, tasks, and decisions.
- A record of phase reviews and evidence that remain applicable, became stale, or were refreshed.
- Corrected dependencies, honest task completion, and the current handoff.

## Completion evidence

The authoritative artifacts agree on current intent and work status. Every current completion claim is supported by applicable evidence. Required unverified outcomes are visibly pending. No valid work is discarded merely to restart the process, and no superseded acceptance is presented as current.

## Continue, pause, and resume

Reconcile routine changes without restarting the project plan. Pause dependent work only for conflicting decisions requiring a choice or unavailable required evidence/access. Resume from the saved baseline and impact assessment, inspect subsequent changes, and continue the next unblocked task.
