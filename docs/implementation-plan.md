# Implementation roadmap

The requested research/bootstrap is the first deliverable. Runtime parity is a separate implementation program grounded in the [requirements](../specs/0001-workflow-foundation/requirements.md) and [adapter contracts](adapter-contracts.md). The [foundation tasks](../specs/0001-workflow-foundation/tasks.md) are the sole completion checklist; this roadmap owns no task status.

## Delivery phases

| Phase | Purpose and concrete output | Task IDs | Exit evidence |
| --- | --- | --- | --- |
| 0 — Research and usable skeleton | Official evidence, guides, operating instructions, templates, worked example, offline quality check. | T-001–T-003 | Source/access ledger; coherent file map; passing checker/tests; repository readback. |
| 1 — Deterministic work contracts | Parse tasks/requirements, validate traceability/dependencies, bind evidence identities, select bounded context. | T-010–T-012 | Fixture failures are detected; changed inputs invalidate only affected claims; authority conflicts reported. |
| 2 — Native Codex integration | Test event mappings and specialized worker/reviewer contexts on the chosen client. | T-020–T-021 | Hook trust/coverage and fresh-review behavior observed; inactive capabilities reported accurately. |
| 3 — Durable execution | Persist runs, schedule dependencies, join outputs, recover unknown outcomes, bound loops, handle PR events. | T-030–T-033 | Interruption, duplicate event, stale head, cap, and partial-write tests pass. |
| 4 — Adoption and AWS trials | Exercise greenfield and brownfield paths, public toolkit diagnostics, then a separately scoped cloud delivery. | T-040–T-043 | Recorded adoption outcomes, preservation checks, actual environment capability evidence, release/recovery evidence where authorized. |
| 5 — Comparative evaluation | Compare repeatable outcomes with a documented Kiro baseline and choose a support level. | T-050 | Matched scope, disclosed versions/limits, independent acceptance, costs/time/interventions, limitations. |

## First implementation slice after this skeleton

Implement a small deterministic work validator before a daemon or dashboard. It should read stable IDs/dependencies and evidence identities, catch a missing required check, detect a cycle, and identify stale evidence. This resolves a concrete source of false completion while keeping the execution model simple.

Then verify one supported Codex hook that invokes a bounded offline check, and one fresh reviewer workflow. If those provide sufficient value, keep the conversational path. Add a controller only when persisted scheduling and recovery are needed. This limits maintenance and avoids building a competing agent platform unnecessarily.

## Choices to make at the relevant phase

| Choice | When it becomes necessary | Decision criteria |
| --- | --- | --- |
| Machine representation for work/evidence | Phase 1 | Preserve readable Markdown authority; deterministic parsing; migration/versioning. |
| Codex execution interface | Phase 2–3 | Required events/controls, stable supported schema, testability, user's actual environment. |
| Controller language/storage | Phase 3 | Existing project/runtime, atomicity/recovery needs, deployment burden; do not infer from the checker language. |
| PR event source | Phase 3 | Reuse existing CI/integration, deduplication, stop conditions, idle cost. |
| AWS trial architecture and environment | Phase 4 | User outcome, scoped authority, resources/costs, cleanup ownership, recovery. |
| Support and compatibility policy | Phase 5 | Verified surfaces/versions and maintenance capacity. |

## Explicitly deferred extensions

Optional packaging as repository skills, a native spec dashboard, Kiro recipe import/export, cross-repository coordination, enterprise policy distribution, and scheduled/background operation. None is required to use the initial procedures. Add one only when a concrete need and its acceptance evidence justify it.

## Implementation discipline

Preserve the owner's official AWS plugins and existing project choices. Prepare concrete results before seeking a new consequential decision, and continue within already granted scope. Do not use the roadmap as standing authorization for model spending, AWS operations, messages to others, or deployment.

The [current handoff](../delivery/current-handoff.md) names the next work; the [evaluation catalog](../evaluations/README.md) specifies what would justify claims of parity or improvement.

