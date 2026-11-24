# Integration contracts

The executable surface includes adoption, setup, specification operations, workflow state, read-only hooks and a bounded foreground task controller. Exact schemas are in [workflow tooling](reference/workflow-tooling.md), [bootstrap](reference/bootstrap.md), [specification operations](reference/specification-operations.md), [task execution](reference/task-execution.md) and [native hooks](reference/native-hooks.md). This document separates implemented interfaces from further automation.

## Existing adapters

| Adapter | Input | Output | Evidence boundary |
| --- | --- | --- | --- |
| Adoption | Source, target, mode, optional existing authority paths | Preview or additive package plus manifest | Local fixtures establish file preservation and collisions. |
| Context | Project root and work ID or active pointer | Known answers, questions, reviews, tasks and issues | References and structural consistency; not truth of business facts. |
| Workflow | Canonical artifacts and indexed metadata | Validated phase change, review or evidence record | Declared hashes and traceability; not execution of a test. |
| Specification analysis | Reviewed inputs, actual sourced response and policy | Retained findings/properties and current/stale/mapping state | Syntax/schema/freshness checks; semantic quality remains the reviewer responsibility. |
| Reconciliation | Current changes and expected preview fingerprint | Necessary completion/phase changes and preserved history | Declared file/context impact; external state requires inspection. |
| Native task run | Explicit execution policy, current accepted work and clean Git original | Isolated candidate, real check receipts and retained outcomes | Offline process/Git fixtures; actual model behavior needs a real-client trial. |
| Native events | Documented event JSON | Bounded context or warning | Offline event behavior; actual client trust/loading recorded separately. |
| AWS guidance | Relevant public question and existing official plugin | Source-backed recommendation | Public documentation; no implicit account observation. |

## Implemented foreground controller

The controller uses `codex exec` with structured final output and a workspace-write sandbox, preserving native permissions/configuration. No daemon, App Server, queue or unattended service is enabled. The selected client must actually support the documented invocation; local help and a fake executable do not prove model success. [Official interfaces](reference/sources.md)

Each **run** persists its work/base identity, policy identity, authority reference, limits, attempts, candidate and observations. A **step request** names a task, allowed write scope, contract/check references and remaining time. The backend returns a strict task result; the controller validates the actual Git patch and runs the configured task/integration checks. Missing model usage remains unknown, not zero. Limits bound tasks, concurrency, attempts and elapsed time; they are not a hard monetary cap.

Task completion is recorded only in the verified candidate's canonical ledger. Worker acceptance is labeled author acceptance; it is not an independent review. `run-apply` uses the expected original head and checks ignored-file collisions, candidate freshness and observed application effects. A changed original requires deliberate integration; a post-merge hook's edits are preserved as a review-needed outcome.

## Scheduling and review

Only eligible tasks dispatch. Separate worker worktrees run one dependency wave at a time; overlapping scopes serialize. Each task gets one attempt per run, with no automatic retries. The original application is preserved until explicit apply. Review the actual combined candidate in a fresh context before claiming independent review. An incomplete reviewer or timeout cannot pass.

## Durable recovery and events

The controller persists intent before dispatch/application and the observed outcome afterward. Interrupted runs remain inspectable with their worktrees and counters. Reusing a run ID cannot reset attempts; inspected abandonment retains history. A new invocation requires a deliberate decision after reconciliation. There is no automatic resume/replay or exactly-once guarantee for external effects.

Future PR/CI integration needs repository/head identity, stable event IDs, processed dispositions and terminal stop conditions. Old-head checks cannot validate a new candidate; duplicate feedback cannot repeat effects. Idle waits must not run model turns. No scheduled job, feedback bot, public message, merge or cloud action is enabled by this design.

## Enablement evidence

Use disposable Git fixtures and the local test backend for deterministic acceptance checks. To verify native behavior, inspect the actual selected client’s output and the reviewed candidate under the approved limits. For cloud verification, record the authorized target, observed result and recovery ownership. [Evaluation guidance](../evaluations/README.md)
