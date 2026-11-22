# Design: <work ID and title>

**State:** Proposed; review has not been recorded.
**Route:** <Requirements-First / Design-First / Quick Spec / Bugfix>
**Contract:** <requirements.md or bugfix.md, revision, and review reference>
**Accepted constraints:** <architecture, interfaces, tooling, and decisions>

In Design-First work, identify the supplied architecture and provisional user goal first; link derived requirements when available and check that they still satisfy the original need. Use only sections that clarify this change.

## DES-001 — Recommended approach and decision

<Explain the proposed implementation, why it satisfies the contract, and alternatives with materially different consequences. Record the selected decision separately from the recommendation.>

- Requirement links: <explicit REQ IDs or defect and preservation IDs>.
- Evidence and research: <inspected code, relevant official documentation, date, and constraints>.
- Assumptions: <what remains unverified and the consequence>.
- Decision source: <actual acceptance or delegated design authority; otherwise proposed>.

For AWS choices, consult the existing official toolkit and current official documentation. Preserve accepted tools and delivery controls. Do not ask the user to choose between services before doing the engineering assessment.

## DES-002 — Components, interfaces, data, and control flow

- Components and responsibilities: <ownership and affected surface>.
- Inputs, outputs, and error contract: <interfaces and compatibility>.
- Data model, lifecycle, and consistency: <ownership, persistence, and retention decision>.
- Request or event sequence: <including retries, concurrency, and partial completion>.
- Identity, trust boundaries, network paths, and encryption: <applicable controls>.

Use a compact diagram when interactions need one. Link shared architecture instead of copying it. For brownfield work, identify preserved components, source layout, IaC state/ownership, pipeline, and any explicit migration decision.

## DES-003 — Failure and preservation behavior

| Scenario | Required result | Mechanism | Verification |
| --- | --- | --- | --- |
| <timeout, duplicate, conflict, dependency failure, or recovery> | <contract ID and outcome> | <chosen approach> | <CHK ID> |
| <unaffected behavior> | <preservation ID and outcome> | <compatibility approach> | <CHK ID> |

## DES-004 — Correctness, verification, and operations

| Property | Requirement | Statement and preconditions | Planned task and check |
| --- | --- | --- | --- |
| PROP-001 | <explicit REQ IDs> | For <valid inputs and conditions>, <observable invariant> holds. | <T ID and CHK ID> |

Use properties where they clarify the contract. Property-based tests are one verification technique, not a substitute for the accepted behavior. Choose example, contract, integration, or operational checks when they better establish a claim. Keep required acceptance checks required.

- Local verification: <checks, fixtures, and limitations>.
- Cloud proof obligations: <claims requiring an authorized AWS environment>.
- Observability: <signals, useful diagnostics, and sensitive-data exclusions>.
- Cost impact: <estimate with workload, regional, and pricing assumptions>.
- Migration and rollout: <compatibility, sequence, delivery mechanism, and target configuration>.
- Recovery: <rollback or forward recovery and data consequences>.

## Design review and readiness

- Artifact identity: <reviewed revision or content digest; not reviewed initially>.
- Reviewer and scope: <actual actor; requirements, feasibility, preservation, and verification assessed>.
- Findings and outcome: <pending / changes needed / ready, with evidence>.
- Decision and next transition authority: <actual acceptance or existing delegation and limits>.
- Material open decisions: <decision, consequence, owner, and dependent work>.

For Quick Spec, link the combined specification review instead of inventing a separate design approval. An author self-check is not independent review. A reasoned design still needs implementation evidence; a diagram does not prove feasibility or live AWS state.

Task generation is ready when the contract, selected approach, interfaces, checks, and dependencies are sufficiently clear. Planning readiness does not grant account access or deployment authority. If new information changes this design, reconcile affected requirements, tasks, phase reviews, and evidence before relying on them.
