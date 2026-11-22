# Requirements: EX-001 — Safe booking retries

**State:** Illustrative draft; not accepted or implemented.
**Users:** An authenticated customer and a client that may retry a request after losing a response.

## Scope and assumptions

The proposed feature applies to creation of a booking with an idempotency key scoped to the authenticated customer and the booking-creation operation. It assumes an existing authenticated booking API and persistence system, neither of which exists in this repository.

The service compares a canonical representation of validated business fields. Authentication context and response timing are not part of that representation. Existing validation, customer isolation, and availability/conflict rules remain authoritative.

The idempotency retention duration is unresolved. Requirements below apply while an idempotency record is retained. The exact duration and behavior after expiry must be accepted before production implementation; this example does not invent a value.

## Behavioral contract

| ID | Required outcome | Acceptance criterion |
| --- | --- | --- |
| REQ-001 | An identical successful request retried with the same scoped key returns the original booking identifier and business result. | Repeated sequential requests produce one booking and the same result. |
| REQ-002 | Reusing the scoped key with different validated business fields returns a defined conflict and creates no additional booking. | The original booking is unchanged; the conflict response has a stable error code. |
| REQ-003 | Concurrent identical requests with the same scoped key create at most one booking. | One request completes; others receive the completed result or a documented retryable in-progress response. |
| REQ-004 | A failure before the booking transaction commits leaves no partially committed booking outcome for that key. | A later valid retry can complete once; an interrupted response after commit can be replayed. |
| REQ-005 | Requests without an idempotency key retain existing validation, authentication, and booking-conflict behavior. | The established baseline behavior checks continue to pass. |
| REQ-006 | One customer's key does not expose, conflict with, or replay another customer's booking. | Two customers using the same text key remain isolated; unauthorized access is rejected. |

All six requirements are required for this feature's proposed scope. Offline client caching, payment behavior, cross-region writes, and changing the project's architecture are excluded.

## Requirements analysis to perform

- Select the retention duration and expiry behavior with the product and operational owner.
- Specify the precise retryable response contract and client backoff responsibility.
- Verify that the chosen storage system can preserve booking rules and idempotency atomically, or revise the design and its proof obligations.

These are identified planning questions, not completed consultation findings. [Tasks](tasks.md) owns the verification matrix and all task completion state.
