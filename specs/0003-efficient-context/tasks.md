# Tasks: focused context and measured efficiency

**Contract:** [Requirements](requirements.md).  
**Design:** [Design](design.md).  
**Authority:** Requested repository improvement and offline verification. One canonical completion checklist lives here.

### T-001 — Implement bounded context and event-specific refresh

- [ ] T-001 complete
- Activity: needs verification
- Contract / design: REQ-001, REQ-002, REQ-003, REQ-004, REQ-006 / DES-001, DES-002
- Prerequisites: none
- Scope and exclusions: Shared projection, CLI option, native adapter integration and meaningful regressions; no worker execution or client trust change.
- Acceptance: Strict limits retain current problems and actionable references while preserving full audit output and read-only behavior.
- Verification: CHK-001
- Evidence / review: [Current readiness evidence](../../evidence/0004-developer-workflow/codespaces-stabilization.md).
- Blocker: none

### T-002 — Integrate efficient operating policy and safe packaging

- [ ] T-002 complete
- Activity: needs verification
- Contract / design: REQ-005, REQ-006 / DES-003
- Prerequisites: T-001
- Scope and exclusions: Root/adopted instructions, required package module, entry docs and one evaluation protocol.
- Acceptance: Actual adoption includes the working compact CLI; incomplete packages fail before writes; policy preserves meaningful questions, checks and real authority.
- Verification: CHK-002
- Evidence / review: [Current readiness evidence](../../evidence/0004-developer-workflow/codespaces-stabilization.md).
- Blocker: none

### T-003 — Verify measured improvement and reconcile evidence

- [ ] T-003 complete
- Activity: needs verification
- Contract / design: REQ-001, REQ-002, REQ-003, REQ-004, REQ-006, REQ-007 / DES-004
- Prerequisites: T-001, T-002
- Scope and exclusions: Frozen old/new renderer measurements, aggregate regression suite, source identities and current evidence reconciliation; no native model or cloud trial.
- Acceptance: Quality cases pass, payload changes are measured honestly, declared-input freshness remains accurate, and the current source tree is verified on publication.
- Verification: CHK-003
- Evidence / review: [Current readiness evidence](../../evidence/0004-developer-workflow/codespaces-stabilization.md).
- Blocker: none

## Verification matrix

| Check | Requirement | Task | Method and expected result | Evidence |
| --- | --- | --- | --- | --- |
| CHK-001 | REQ-001, REQ-002, REQ-003, REQ-004, REQ-006 | T-001 | Projection/CLI/hook regressions preserve errors, strict caps, next action, full inspection and read-only behavior. | [Observed readiness result](../../evidence/0004-developer-workflow/codespaces-stabilization.md) |
| CHK-002 | REQ-005, REQ-006 | T-002 | Inspect root/generated operating policy and run bootstrap plus actual-source integration; missing projection module must block. | [Observed readiness result](../../evidence/0004-developer-workflow/codespaces-stabilization.md) |
| CHK-003 | REQ-001, REQ-002, REQ-003, REQ-004, REQ-006, REQ-007 | T-003 | Run combined local suite, compare identical prior/current renderer fixtures, reconcile changed evidence inputs, scan current content/links and verify published file identities. | [Observed readiness result](../../evidence/0004-developer-workflow/codespaces-stabilization.md) |

## Deferred evidence

Actual model consultations, selected-client hook loading and AWS operations remain separate trials with their own scope and authority. Character-size improvements are not a model-quality, tokenizer or cost benchmark.
