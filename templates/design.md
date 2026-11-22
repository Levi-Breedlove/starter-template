# Design: <work ID and title>

**State:** Proposed; not independently reviewed.
**Contract:** <requirements.md or bugfix.md and its accepted revision>
**Accepted constraints:** <architecture, interfaces, tooling, and decisions>

## DES-001 — Selected approach

<Explain the implementation, why it fits the contract, and meaningful alternatives. Separate selected decisions from unresolved choices.>

Requirement links: <REQ IDs, or defect and preservation IDs>.

## DES-002 — Interfaces, data, and control flow

- Components and responsibilities: <ownership>.
- Inputs, outputs, and error contract: <interfaces>.
- Data model, lifecycle, and consistency: <ownership and persistence>.
- Request or event sequence: <including retries and concurrency>.
- Identity, trust boundaries, network paths, and encryption: <applicable controls>.

Use a compact diagram when it explains interactions better than prose. Link shared architecture rather than copying it into every feature.

## DES-003 — Failure and preservation behavior

| Scenario | Required result | Mechanism | Verification |
| --- | --- | --- | --- |
| <timeout, duplicate, conflict, dependency failure, or recovery> | <contract ID and result> | <chosen approach> | <CHK ID> |
| <unaffected behavior> | <preserved contract> | <compatibility approach> | <CHK ID> |

## DES-004 — Verification and operations

| Property | Requirement | Statement and preconditions | Planned task and verification |
| --- | --- | --- | --- |
| PROP-001 | <REQ IDs> | For <valid inputs and conditions>, <observable invariant> holds. | <T ID and CHK ID> |

Use this table when properties clarify the contract. A requirement depending on external state may need an integration or example-based check instead. Do not substitute a weak property for the actual acceptance criterion.

- Local verification: <checks and required fixtures>.
- Cloud proof obligations: <what needs an explicitly authorized AWS environment>.
- Observability: <signals, useful diagnostics, and sensitive-data exclusions>.
- Cost impact: <link to assumptions and estimate>.
- Migration and rollout: <compatibility, order, and target-specific configuration>.
- Recovery: <rollback or forward recovery, including data implications>.

## Design review and readiness

Review identity and revision: <not reviewed / evidence reference>.

Unresolved consequential choices: <decision, owner, and affected tasks>. Routine implementation details may remain with the implementer; required behavior and material architecture choices must be clear.

Task generation is ready when the contract, selected approach, interfaces, verification obligations, and genuine dependencies are sufficient. Planning readiness does not establish execution or deployment authorization.
