# Design: Codex AWS workflow foundation

**Historical foundation scope:** The initial scaffold and broader program are described here. Current executable behavior is specified in [0002](../0002-consultant-workflow/requirements.md); use its tasks and receipt for current claims.

**Work ID:** 0001-workflow-foundation.  
**Contract:** [Requirements](requirements.md).  
**State:** Document/procedure implementation with planned runtime adapters.

## Design decomposition

| Design ID | Responsibility | Requirements | Location |
| --- | --- | --- | --- |
| DES-01 | Research/evidence provenance and capability truth | REQ-001, REQ-002 | `docs/research/`, `docs/reference/` |
| DES-02 | Project context, route selection, greenfield/brownfield adoption | REQ-003, REQ-004, REQ-016 | `AGENTS.md`, `project/`, `guide/`, `workflows/` |
| DES-03 | Specification, task, decision, review, and verification contracts | REQ-005, REQ-006, REQ-008 | `templates/`, `specs/`, `evidence/` |
| DES-04 | Reconciliation, candidate identity, evidence freshness | REQ-006, REQ-009 | Reconcile procedure; later work/evidence validator. |
| DES-05 | Official AWS adapter and release/operations boundary | REQ-010, REQ-011 | AWS guide, costs, security, infrastructure, delivery, runbooks. |
| DES-06 | Native events, context and worker adapters | REQ-007, REQ-008, REQ-012 | `.codex/README.md`, adapter contracts; active configurations later. |
| DES-07 | Durable controller, limits, recovery, PR events | REQ-007, REQ-013, REQ-014, REQ-015 | Proposed `workflow_engine/`; no runner supplied now. |
| DES-08 | Bootstrap quality and comparative evaluations | REQ-017, REQ-018 | Offline checker/tests, evaluation catalog, evidence. |

The complete behavioral architecture is in [workflow architecture](../../docs/workflow-architecture.md). Machine interfaces and recovery semantics are in [adapter contracts](../../docs/adapter-contracts.md). Those documents are referenced here to avoid another competing design copy.

## Immediate implementation

Use Markdown for human-reviewable authority and ordinary Codex repository instructions. Provide focused procedure contracts and original templates. Keep product-specific facts in cited research and reference documents. Provide one standard-library checker for local file links and core scaffold paths with fixture tests; do not call that semantic verification.

No runtime dependency, deployment configuration, or actual skill package is needed for this initial delivery. The `.codex/` and `.agents/skills/` README files describe extension boundaries. No external recipe schema is represented as native Codex configuration.

## Later implementation sequence

First implement deterministic work/evidence parsing and context manifests. Then test native hook and worker mappings on a selected Codex surface. Only then add persistence/scheduling/recovery around the tested worker interface. Keep PR/CI integration optional and reuse the established project mechanism. Run greenfield and brownfield evaluation fixtures before any scoped AWS deployment trial.

## Invariants

- One declared work authority; runtime records are execution history and projections.
- A required outcome is complete only with relevant current evidence.
- Source, input, configuration, and artifact identity are available at verification and release boundaries.
- Unknown or failed review/operation outcomes do not become success by default.
- Resume preserves counters and reconciles effects; it does not create authority or promise exactly-once remote actions.
- Existing project architecture, user work, IaC ownership, and operational boundaries survive adoption.

These are design obligations to test. The initial scaffold does not enforce all of them automatically.

## Tradeoffs and risks

The conversational path is easy to adopt but relies on agent adherence and review. Native hooks improve repetition but differ by surface and require trust/coverage tests. A durable controller can improve recovery while adding state-management and maintenance work. Copying every document into every prompt can dilute context; use the router and relevant references.

Brownfield adoption risks competing authority and stale baselines. Map existing sources and record known gaps before adding files. AWS preview/import/testing tools have service-specific limits, so a generic “validated” field is inadequate. See [AWS delivery guidance](../../docs/reference/aws-delivery.md).

## Validation

Use the [task verification matrix](tasks.md) for actual status and evidence. The [workflow contract](../../docs/reference/workflow-contract.md) and [evaluation catalog](../../evaluations/README.md) define future behavioral proof, including failure and interruption cases. Publication verification compares the repository's returned file identities with the final local manifest.

