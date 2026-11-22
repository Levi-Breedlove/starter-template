# Requirements: <work ID and title>

**State:** Draft; not accepted.
**Owner / acceptance reference:** <owner; not yet recorded>
**Related project context:** <brief and accepted decisions>
**Route:** <Requirements-First / Design-First / Quick Spec>

For Design-First work, link the starting design and derive requirements without assuming the design already proves feasibility. For Quick Spec, record the initial clarification and generate the connected artifacts without adding unnecessary intermediate gates.

## Goal and scope

<Describe the problem, affected users, and observable outcome.>

- Included: <scope>.
- Excluded: <non-goals>.
- Existing behavior to preserve: <contracts and accepted architecture>.
- Assumptions: <each assumption, its consequence, and how it will be resolved>.

## Behavioral contract

| ID | Condition and required outcome | Acceptance criterion | Required or deferred |
| --- | --- | --- | --- |
| REQ-001 | When <condition>, the system must <observable outcome>. | <result that can be checked, including limits> | Required |
| REQ-002 | When <failure or concurrent condition>, the system must <defined behavior>. | <observable failure or concurrency behavior> | Required |
| REQ-003 | For <unaffected use>, the system must continue to <existing behavior>. | <preservation check> | Required |

Name relevant authorization, validation, concurrency, retry, timeout, and partial-failure behavior. Specify units and boundaries where they matter; replace terms such as “fast” with a defined measurement or mark the threshold unresolved.

## Requirements analysis

| Finding | Affected requirements | Impact | Resolution or decision needed |
| --- | --- | --- | --- |
| <contradiction, ambiguity, gap, or assumption> | <IDs> | <implementation consequence> | <resolved finding or owner decision> |

Analysis result: <not performed / findings resolved / named open issues>. Do not write “no issues” unless the analysis occurred. A known blocking contradiction prevents the dependent implementation from being ready.

## Acceptance and change handling

Acceptance decision: <not recorded / exact decision reference and accepted revision>.

The verification matrix belongs in [tasks.md](tasks.md). Each required requirement must have a check and evidence or a clearly stated remaining obligation. After a material change, revise [design.md](design.md), reconcile affected tasks, and mark invalidated evidence before continuing dependent work. Preserve completed work whose acceptance remains valid.
