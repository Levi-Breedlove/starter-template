# Codex adapter contracts

**Status: proposed implementation design.** None of the adapters below is active merely because this document exists. The offline repository checker is the only executable utility delivered in this bootstrap. Native features must be checked on the actual Codex surface/version. Sources and observed interfaces are recorded in [runtime research](research/runtime-parity.md).

## Build on native capabilities

Use repository instructions for routing and the current tool/session interface for ordinary work. Implement a local controller only when repeatable task execution, event handling, or durable recovery needs it. Prefer supported `codex exec`/SDK interfaces for a small controller; consider App Server only when a persistent custom control interface is justified. Select and test one integration boundary before supporting several.

Do not interpret `.kiro/workflows/` recipes as Codex configuration. If recipe import becomes useful, it needs explicit parsing, validation, feature coverage, unsupported-node errors, and behavior tests. It is optional compatibility work, separate from the core process.

## Adapter inventory

| Adapter | Input | Output | Completion proof |
| --- | --- | --- | --- |
| Context | Work ID, paths, brief, decisions, current candidate | Bounded context manifest with provenance | Correct relevant constraints loaded; conflicting/unknown facts visible. |
| Specification | Current requirements/design/tasks and intended change | Coherent candidate documents and impact report | Required identifiers resolve; coverage and changed assumptions reviewed. |
| Task controller | Canonical task graph, capabilities, scope, limits | Eligible task dispatches and attempt records | Dependencies enforced; conflicting writers prevented. |
| Codex execution | Structured step request and isolated working scope | Candidate artifacts, observations, unresolved questions | Returned data validates and matches actual files/results. |
| Review | Exact candidate and original acceptance contract | Findings or explicit incomplete result | Fresh reviewer context; current candidate; meaningful scope. |
| Evidence | Check result and input identities | Immutable evidence record and coverage projection | Changed inputs cannot reuse affected stale acceptance. |
| Hook/event | Supported native event or controller task event | One bounded requested action | Trust, coverage, deduplication, timeout, recursion behavior tested. |
| PR/CI | Repository/PR/head and processed event cursor | Feedback disposition and current readiness | No old-head checks, duplicated response, or assumed merge authority. |
| AWS | Official toolkit plus task-authorized target/action | Guidance or bounded operational receipt | Identity/action/environment match actual authorization; unknown outcomes reconciled. |

## Minimal data contracts

These field lists define semantics for later machine schemas. They are not executable JSON/YAML or an advertised Codex API schema.

**Run:** schema version, run ID, work ID, recipe version/digest, repository identity, base/candidate identity, selected surface/version, context manifest, actual authorization reference, configured limits, consumed limits, state, timestamps, and parent run when applicable.

**Step request:** stable node/task ID, attempt ID, dependency outcomes, referenced requirement/design revisions, input/artifact identities, permitted scope and output paths, worker role, check obligations, side-effect classification, and stop conditions. Include only relevant context and sanitized references.

**Step result:** attempt ID, candidate identity, changed files/artifacts, check observations, findings, unresolved questions, usage when observable, status, and external operation receipts where applicable. Unknown usage remains unknown rather than zero. A model-declared success is a claim to validate.

**Evidence:** check ID, requirement IDs, task ID, source or base-plus-patch identity, relevant spec/fixture/configuration identities, tool/procedure version, environment, artifact digest if applicable, timestamps, observed result, coverage, limitations, and output location. Never persist credential values or raw sensitive dumps.

**Event:** stable event ID, source, work/run/task IDs where known, candidate identity, causal event ID, event time, normalized event type, and processed disposition. A process restart cannot treat the same event as new work.

**Authorization reference:** a reference to the user's actual instruction or established project authority, with allowed action/target/environment and relevant limits. This record documents authority; it does not grant it or override IAM, client policy, branch protection, or the user's latest instruction.

## Hooks: translate behavior explicitly

| Desired Kiro-style behavior | Codex candidate mapping | Required caveat |
| --- | --- | --- |
| Load current project/work context | Supported `SessionStart` and relevant compaction handling | Verify the client's lifecycle and keep context bounded. |
| Validate before a tool action | Supported `PreToolUse` | Event coverage is not universal enforcement; authorization remains separate. |
| React to changed files | Supported `PostToolUse` plus observed diff, or a controller boundary | Tool output alone does not prove which paths changed; no recursive generated-output loop. |
| Check task entry/completion | Controller-owned task events | Do not invent native Codex spec-task hooks. |
| Run checks when a turn ends | Supported `Stop`/worker boundary | A stop event is not acceptance and must not create unbounded re-entry. |
| Agent-prompt hook action | Explicit supported controller turn | Current documented Codex `prompt`/`agent` handler types are skipped; do not label them active. |
| Persist continuation | Supported lifecycle boundary plus durable state | A crash can occur between a side effect and persistence; reconcile uncertainty. |

Choose one hook configuration source per project layer to avoid duplicate execution. Trust changes through the supported product interface; do not bypass hook trust. Hooks must use bounded execution, parse their documented input, produce limited output, and avoid running arbitrary shell derived from untrusted document text.

## Scheduling, isolation, and joins

Validate the task graph for missing IDs and cycles. A node starts only when its prerequisites have valid outcomes. Keep task activity separate from acceptance completion. Deferred optional work is not represented as a successful required dependency.

Use distinct worktrees for concurrent writers where practical. If the environment shares a working directory, enforce disjoint file ownership and an integration owner. Aggregate findings from independent reviewers without suppressing disagreement. Re-run affected checks on the combined candidate; branch-level passes do not prove the merge.

Store limits for workers, attempts, repeated failures, iteration depth, elapsed time, and usage where available. The project chooses values appropriate to the task. Persist the consumed counters across restarts. Do not infer additional paid background authority from a higher configured number.

## Persistence and recovery

The initial proposed controller can use a versioned local state directory, `.workflow-state/`, with atomic record replacement and an append-only event log. It is ignored by Git because it can contain transient execution metadata; publish compact sanitized evidence and handoffs separately. Select a transactional store later only if concurrency and recovery tests justify it.

Persist dispatch intent before launch and the outcome after validation. If recovery sees dispatched work without a known outcome, mark it unknown and inspect actual files/receipts. Exactly-once external effects cannot be promised by a local log. Use service-supported idempotency where applicable and reconcile state before retrying.

Pause stops scheduling at a safe boundary. Stop cancels pending work and handles active work through the supported client. Retry targets failed/unknown work only after reconciliation, preserving completed siblings and prior limits. A specification change invalidates dependent outcomes instead of silently reusing them under a new contract.

## Event-driven PR work

Use the existing CI or supported event integration where possible. Track repository, PR, head commit, event IDs, processed findings, required checks, and stop conditions. Ignore duplicated events, reject stale readiness from a previous head, and stop when the PR closes or the authorized scope ends.

Idle waiting should not consume model turns. A polling timer still has execution and possible hosting costs; choose a bounded supported mechanism and record it. No polling service, schedule, public comment, merge, or deployment is enabled by this design.

## Validation before enablement

Start with fake tool/worker adapters and temporary repositories. Exercise interruption, stale inputs, duplicate events, failed reviews, graph conflicts, partial writes, and caps without model or AWS calls. Then run a bounded real Codex trial in a disposable project within actual authorization. Enable trusted hooks only after their behavior is demonstrated on the selected client.

AWS trials come later with explicit target/action limits and cleanup ownership. Report local, integrated, and cloud evidence separately. The [evaluation catalog](../evaluations/README.md) and [foundation tasks](../specs/0001-workflow-foundation/tasks.md) define the acceptance path.

