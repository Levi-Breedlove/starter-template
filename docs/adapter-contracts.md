# Integration contracts

The current executable surface is the bootstrap installer, local workflow CLI and read-only native hook adapter. Exact implemented schemas are in [workflow tooling](reference/workflow-tooling.md), [bootstrap](reference/bootstrap.md) and [native hooks](reference/native-hooks.md). This document specifies the boundary for further automation; it does not declare a scheduler implemented.

## Existing adapters

| Adapter | Input | Output | Evidence boundary |
| --- | --- | --- | --- |
| Adoption | Source, target, mode, optional existing authority paths | Preview or additive package plus manifest | Local fixtures establish file preservation and collisions. |
| Context | Project root and work ID or active pointer | Known answers, questions, reviews, tasks and issues | References and structural consistency; not truth of business facts. |
| Workflow | Canonical artifacts and indexed metadata | Validated phase change, review or evidence record | Declared hashes and traceability; not execution of a test. |
| Native events | Documented event JSON | Bounded context or warning | Offline event behavior; actual client trust/loading recorded separately. |
| AWS guidance | Relevant public question and existing official plugin | Source-backed recommendation | Public documentation; no implicit account observation. |

## Future worker controller

Use a supported Codex exec/SDK boundary for a bounded worker if actual demand justifies it. Select App Server only when persistent interactive control is needed. Verify the selected client's current schema; do not infer it from a repository directory name. [Official interfaces](reference/sources.md)

A future **run** needs a version, work ID, candidate identity, selected recipe, context, actual authority reference, limits and consumed counters. A **step request** needs a task and attempt ID, prerequisite outcomes, input identities, allowed write scope, expected checks and stop conditions. A **result** needs actual artifact identities, observations, findings, unresolved questions and externally observed receipts where applicable. Missing usage remains unknown, not zero.

The controller must validate returned records against actual artifacts. A model-declared success is a claim. Task status remains in the canonical work contract; run history records attempts rather than becoming a second completion tracker.

## Scheduling and review

Dispatch only eligible tasks. Use separate worktrees or disjoint shared write scopes, with one integration owner. Bound workers, attempts, repeated failures, elapsed time and usage where observable; persist consumed limits across restarts. Review the actual combined candidate in a fresh context before claiming independent review. An incomplete reviewer or timeout cannot pass.

## Durable recovery and events

Persist intent before dispatch and validated outcome after completion. If a process stops between a side effect and its receipt, mark the outcome unknown and reconcile before retrying. A local log cannot promise exactly-once external effects. Use service-supported idempotency where applicable.

Future PR/CI integration needs repository/head identity, stable event IDs, processed dispositions and terminal stop conditions. Old-head checks cannot validate a new candidate; duplicate feedback cannot repeat effects. Idle waits must not run model turns. No scheduled job, feedback bot, public message, merge or cloud action is enabled by this design.

## Enablement evidence

Start with fake workers and temporary repositories: crash windows, stale inputs, duplicate events, failed reviews, shared-file conflicts and cap exhaustion. Then conduct a bounded real-client trial under actual task scope. Cloud trials require a concrete project, authorized targets and cleanup/recovery ownership. The [implementation plan](implementation-plan.md) and [evaluation catalog](../evaluations/README.md) define the remaining work.
