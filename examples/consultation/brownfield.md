# Brownfield example: duplicate order submissions

This fictional dialogue concerns an existing service. Assume repository inspection finds a Python API, PostgreSQL schema, ECS infrastructure declared in Terraform, and an established build/deployment pipeline. Existing API documentation requires an idempotency key, but neither documentation nor tests specify how a reused key with a changed payload should behave. These are scenario facts, not observations of a real account.

## 1. Inspect and preserve the established system

**User:** “Retries sometimes create duplicate orders. Fix that without redesigning the service.”

**Codex:** “The repository establishes the Python service, PostgreSQL persistence, Terraform ownership, and existing delivery pipeline. I will preserve those. The retry contract promises one order for the same request, so I will investigate the request-key handling and transaction boundary rather than add a new queue or database.

“I found one contract gap: the same key can arrive with a different order payload. I recommend returning a conflict without changing the original order; reusing the key should not silently replace a previous purchase. Is that the intended product behavior?”

**User:** “Yes. Return a conflict for a changed payload. Same payload and key should return the original order. You can implement and test locally; do not access AWS.”

The agent records the answer in the defect contract and references it from the adoption report. The message also defines local implementation authority. It does not create deployment or account-inspection authority.

## 2. Build the defect contract from the baseline

The work uses Bugfix because the requested change repairs a documented promise. Its `bugfix.md` distinguishes:

| Contract | Expected record |
| --- | --- |
| Defect | Repeating an equivalent order request can create another order. Reproduction still needs to establish the failing path. |
| Correct behavior | Reusing the same key and payload returns the original order without creating another. |
| Changed-payload policy | Reusing the key with a different payload returns a conflict and preserves the original order. |
| Preserved behavior | Distinct valid requests, authorization, validation, existing response compatibility, and established data/infra ownership remain intact. |

**Codex:** “I have recorded that policy and checked it against the existing retry promise. I can continue the contract review and local diagnosis within your authorization. I will first reproduce the duplicate path and identify the cause; the reported symptom alone does not establish which transaction boundary is wrong.”

This is an actual review step within the fictional session, not an invented additional user approval. Its record identifies the inspected contract, user decision, reviewer, and remaining diagnostic work.

## 3. Let evidence guide the fix design

Suppose the subsequent local investigation demonstrates a race between checking for an existing request and inserting an order. The hypothetical result supports that cause; it must not be assumed before investigation.

**Codex:** “The local reproduction shows the gap between the request lookup and order creation. I recommend a database-enforced uniqueness/transaction strategy within the existing schema and service. The design will make the request identity, payload comparison, and returned order result consistent, including concurrent attempts and transaction failure.

“I will inspect the migration against existing data and preserve the response contract. If duplicate historical data creates a remediation choice, I will show the evidence and ask about that specific decision before modifying it.”

The design review checks the diagnosis, proposed correction, preservation obligations, migration impact, and verification. It uses existing delegated implementation authority for routine engineering decisions. A discovered data-remediation policy would be a new consequential decision, not permission to delete or rewrite history.

## 4. Generate a scoped task graph

| Task | Outcome | Prerequisite | Required evidence |
| --- | --- | --- | --- |
| T-001 | Establish the defect and baseline preservation checks. | None | A real local reproduction and baseline observations. |
| T-002 | Implement the reviewed request-key and transaction correction. | T-001 | Same-key replay, changed-payload conflict, and concurrency checks. |
| T-003 | Assess and implement any necessary compatible migration. | T-001 | Local migration evidence and explicit unresolved data decisions. |
| T-004 | Integrate, rerun relevant checks, and review the candidate. | T-002, T-003 | Corrected behavior and preserved contracts for the same candidate. |

The migration task is retained only if the investigated design needs it. The real task record links explicit defect, preservation, and check IDs. A local reproduction is not evidence of the deployed revision or actual AWS configuration.

Because local implementation is authorized, Codex continues unblocked tasks after the actual contract, design, and task-plan reviews. It does not ask “May I edit this file?” repeatedly. It stops only the work dependent on a material unresolved decision or unavailable required environment.

## 5. Resume from evidence rather than restart

If a later session changes the response contract, Codex reads the handoff and current code, identifies the affected requirement and design, and uses [Reconcile](../../workflows/reconcile.md). It revisits relevant reviews and checks; it does not automatically discard the completed correction or claim that old evidence still covers the new contract.

A final local report distinguishes the patch, actual executed checks, independent review if one occurred, and pending deployment/integration evidence. The existing pipeline remains the delivery path. No account operation is inferred from the request to fix the service locally.

## What this illustrates

Repository evidence answered the stack and ownership questions. One unresolved product policy needed the user's answer. Codex supplied the diagnostic plan and engineering recommendation, preserved the existing architecture, and made the fix's completion depend on actual correction and regression evidence.
