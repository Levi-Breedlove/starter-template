# Design: EX-001 — Safe booking retries

**State:** Illustrative proposal; no selected application or storage implementation has been tested.
**Contract:** [requirements.md](requirements.md).

## DES-001 — Request identity and replay contract

Derive the operation identity from the authenticated customer, booking-creation operation, and submitted idempotency key. Compare a canonical representation of validated booking fields when resolving an existing record. Store the original successful business result needed for a replay, subject to the project's data minimization and retention decision.

An existing completed record with matching fields returns its saved result (`REQ-001`). Different fields for the same identity return the agreed conflict (`REQ-002`). Authentication and customer scope are applied before lookup (`REQ-006`). The exact response fields and error codes remain part of the API contract to accept in T-001.

## DES-002 — Atomic booking outcome

For the first request, propose one transaction that enforces existing booking-conflict rules and records the booking plus completed idempotency result. Uniqueness on the scoped operation identity must prevent two committed outcomes. A concurrent request must either observe the completed result or receive the agreed retryable in-progress response (`REQ-003`).

This is a design requirement for the selected persistence system, not a statement that every database supports the same transaction semantics. Implementation must verify the selected mechanism before relying on it. If it cannot provide the required behavior, revise the design instead of weakening acceptance silently.

## DES-003 — Failure and preserved behavior

| Scenario | Proposed behavior | Requirements | Checks |
| --- | --- | --- | --- |
| Response is lost after commit | Replay the saved result on a matching retry. | REQ-001, REQ-004 | CHK-001, CHK-004 |
| Failure before transaction commit | Roll back the booking and idempotency changes together; allow a later retry. | REQ-004 | CHK-004 |
| Concurrent same-key requests | At most one committed booking; completed replay or retryable pending result. | REQ-003 | CHK-003 |
| Key reused with changed fields | Return conflict without altering the original outcome. | REQ-002 | CHK-002 |
| No key supplied | Follow the established booking path and its controls. | REQ-005 | CHK-005 |
| Different authenticated customer | Use a separate identity scope; preserve access control. | REQ-006 | CHK-006 |

## DES-004 — Verification and operations

**PROP-001:** Any permitted sequence of matching requests for one retained scoped key commits at most one booking. This connects REQ-001, REQ-003, and REQ-004 to T-002/T-004 and CHK-003/CHK-004. Generated retry sequences can exercise this property. Actual concurrent database transactions and the failure points above also require integration checks; a mocked storage result is insufficient evidence for atomicity.

Proposed diagnostics count replay, conflict, and in-progress outcomes without logging sensitive booking fields or raw reusable keys. Evaluate retained-record volume and cleanup cost after the retention decision. Introduce any schema change compatibly and define recovery before releasing to an environment.

No AWS service, region, account, role, capacity, cost amount, or deployment pipeline is selected by this example. A real implementation must use its project's accepted architecture and release controls.

## Pending decisions

T-001 must settle the retention and response contract. T-002 must validate the chosen persistence mechanism. No implementation review, owner acceptance, or deployment authorization is recorded.
