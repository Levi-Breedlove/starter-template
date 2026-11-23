# Tasks: focused context and measured efficiency

**Contract:** [Requirements](requirements.md).  
**Design:** [Design](design.md).  
**Authority:** Requested repository improvement and offline verification. One canonical completion checklist lives here.

### T-001 — Implement bounded context and event-specific refresh

- [x] T-001 complete
- Activity: complete
- Contract / design: REQ-001, REQ-002, REQ-003, REQ-004, REQ-006 / DES-001, DES-002
- Prerequisites: none
- Scope and exclusions: Shared projection, CLI option, native adapter integration and meaningful regressions; no worker execution or client trust change.
- Acceptance: Strict limits retain current problems and actionable references while preserving full audit output and read-only behavior.
- Verification: CHK-001
- Evidence / review: [Local checks](../../evidence/0003-efficient-context/local-checks.md) and [combined review](../../evidence/0003-efficient-context/review.md).
- Blocker: none

### T-002 — Integrate efficient operating policy and safe packaging

- [x] T-002 complete
- Activity: complete
- Contract / design: REQ-005, REQ-006 / DES-003
- Prerequisites: T-001
- Scope and exclusions: Root/adopted instructions, required package module, entry docs and one evaluation protocol.
- Acceptance: Actual adoption includes the working compact CLI; incomplete packages fail before writes; policy preserves meaningful questions, checks and real authority.
- Verification: CHK-002
- Evidence / review: [Actual package and policy verification](../../evidence/0003-efficient-context/local-checks.md).
- Blocker: none

### T-003 — Verify measured improvement and reconcile evidence

- [x] T-003 complete
- Activity: complete
- Contract / design: REQ-001, REQ-002, REQ-003, REQ-004, REQ-006, REQ-007 / DES-004
- Prerequisites: T-001, T-002
- Scope and exclusions: Frozen old/new renderer measurements, aggregate regression suite, source identities and current evidence reconciliation; no native model or cloud trial.
- Acceptance: Quality cases pass, payload changes are measured honestly, declared-input freshness remains accurate, and the current source tree is verified on publication.
- Verification: CHK-003
- Evidence / review: [Local observations](../../evidence/0003-efficient-context/local-checks.md) and [actual source readback](../../evidence/0003-efficient-context/publication.md).
- Blocker: none

## Verification matrix

| Check | Requirement | Task | Method and expected result | Evidence |
| --- | --- | --- | --- | --- |
| CHK-001 | REQ-001, REQ-002, REQ-003, REQ-004, REQ-006 | T-001 | Projection/CLI/hook regressions preserve errors, strict caps, next action, full inspection and read-only behavior. | [Local checks](../../evidence/0003-efficient-context/local-checks.md) |
| CHK-002 | REQ-005, REQ-006 | T-002 | Inspect root/generated operating policy and run bootstrap plus actual-source integration; missing projection module must block. | [Local checks](../../evidence/0003-efficient-context/local-checks.md) |
| CHK-003 | REQ-001, REQ-002, REQ-003, REQ-004, REQ-006, REQ-007 | T-003 | Run combined local suite, compare identical prior/current renderer fixtures, reconcile changed evidence inputs, scan current content/links and verify published file identities. | [Local checks](../../evidence/0003-efficient-context/local-checks.md), [source readback](../../evidence/0003-efficient-context/publication.md) |

## Deferred evidence

Actual model consultations, selected-client hook loading and AWS operations remain separate trials with their own scope and authority. Character-size improvements are not a model-quality, tokenizer or cost benchmark.
