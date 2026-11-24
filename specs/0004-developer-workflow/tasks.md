# Tasks: complete developer workflow

**Contract:** [Requirements](requirements.md).  
**Design:** [Design](design.md).  
**Execution plan:** [Concrete plan and acceptance boundaries](exec-plan.md).  
**Authority:** Requested repository work; external native execution remains a separately approved trial.

### T-001 — Establish the execution plan and connected contract

- [ ] T-001 complete
- Activity: needs verification
- Contract / design: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-010 / DES-001, DES-002, DES-003, DES-004, DES-005, DES-006
- Prerequisites: none
- Scope and exclusions: The named outcome within repository authority; no AWS account operations.
- Acceptance: Concrete scope, API ownership, actual authority and acceptance are documented.
- Verification: CHK-001
- Evidence / review: [Actual plan review](../../evidence/0004-developer-workflow/plan-review.md).
- Blocker: none

### T-002 — Implement specification analysis, properties and reconciliation

- [ ] T-002 complete
- Activity: needs verification
- Contract / design: REQ-002, REQ-003, REQ-004, REQ-007 / DES-002, DES-004
- Prerequisites: T-001
- Scope and exclusions: The named outcome within repository authority; no AWS account operations.
- Acceptance: Structured source-bound operations reject malformed/stale findings, preserve phase semantics and expose unresolved decisions.
- Verification: CHK-002
- Evidence / review: [Current readiness evidence](../../evidence/0004-developer-workflow/codespaces-stabilization.md).
- Blocker: none

### T-003 — Implement bounded task execution and candidate application

- [ ] T-003 complete
- Activity: needs verification
- Contract / design: REQ-005, REQ-006 / DES-003
- Prerequisites: T-001
- Scope and exclusions: The named outcome within repository authority; no AWS account operations.
- Acceptance: Dependency/scoped worktree execution, real verification, bounded outcomes and expected-state application preserve the original application.
- Verification: CHK-003
- Evidence / review: [Current readiness evidence](../../evidence/0004-developer-workflow/codespaces-stabilization.md).
- Blocker: none

### T-004 — Complete setup, adoption and user entry

- [ ] T-004 complete
- Activity: needs verification
- Contract / design: REQ-001, REQ-008 / DES-001, DES-005
- Prerequisites: T-001
- Scope and exclusions: The named outcome within repository authority; no AWS account operations.
- Acceptance: Setup works before active work; correct reusable module set and guides are installed without destroying user context.
- Verification: CHK-004
- Evidence / review: [Current readiness evidence](../../evidence/0004-developer-workflow/codespaces-stabilization.md).
- Blocker: none

### T-005 — Integrate commands, phase checks and current context

- [ ] T-005 complete
- Activity: needs verification
- Contract / design: REQ-002, REQ-003, REQ-004, REQ-005, REQ-007, REQ-008 / DES-002, DES-003, DES-004, DES-005
- Prerequisites: T-002, T-003, T-004
- Scope and exclusions: The named outcome within repository authority; no AWS account operations.
- Acceptance: All documented operations work through the installed CLI; new policy is enforced without silently breaking legacy records.
- Verification: CHK-005
- Evidence / review: [Current readiness evidence](../../evidence/0004-developer-workflow/codespaces-stabilization.md).
- Blocker: none

### T-006 — Verify and review the combined developer workflow

- [ ] T-006 complete
- Activity: needs verification
- Contract / design: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009 / DES-006
- Prerequisites: T-005
- Scope and exclusions: The named outcome within repository authority; no AWS account operations.
- Acceptance: Meaningful regressions and actual-source integration pass; independent concrete findings resolved; evidence limits accurate.
- Verification: CHK-006
- Evidence / review: [Current readiness evidence](../../evidence/0004-developer-workflow/codespaces-stabilization.md).
- Blocker: none

### T-007 — Publish the candidate and reconcile current evidence

- [ ] T-007 complete
- Activity: needs verification
- Contract / design: REQ-009 / DES-006
- Prerequisites: T-006
- Scope and exclusions: The named outcome within repository authority; no AWS account operations.
- Acceptance: Source/evidence remain current and every remote file identity matches the delivered candidate using expected-head publication.
- Verification: CHK-007
- Evidence / review: [Current readiness evidence](../../evidence/0004-developer-workflow/codespaces-stabilization.md).
- Blocker: none

### T-008 — Observe the bounded native-client workflow trials

- [ ] T-008 complete
- Activity: needs verification
- Contract / design: REQ-010 / DES-006
- Prerequisites: T-006
- Scope and exclusions: The named outcome within repository authority; no AWS account operations.
- Acceptance: Approved selected-client greenfield/brownfield, changed-requirement and resume trials have actual observations and reviewed results.
- Verification: CHK-008
- Evidence / review: [Accepted frozen native observations](../../evidence/0004-developer-workflow/native-pilot-closeout.md).
- Blocker: none

## Verification matrix

| Check | Requirement | Task | Method and expected result | Evidence |
| --- | --- | --- | --- | --- |
| CHK-001 | REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-010 | T-001 | Review exact scoped contracts, ownership and authority before implementation. | [Observed result](../../evidence/0004-developer-workflow/plan-review.md) |
| CHK-002 | REQ-002, REQ-003, REQ-004, REQ-007 | T-002 | Run source-bound analysis/property/reconciliation fixtures including malformed, stale and blocking cases. | [Observed readiness result](../../evidence/0004-developer-workflow/codespaces-stabilization.md) |
| CHK-003 | REQ-005, REQ-006 | T-003 | Use real temporary Git worktrees, fake model responses and actual subprocess checks to exercise isolation, joins, failures, bounds and application. | [Observed readiness result](../../evidence/0004-developer-workflow/codespaces-stabilization.md) |
| CHK-004 | REQ-001, REQ-008 | T-004 | Run setup/bootstrap preservation, collision, mapping, hook-preview and missing-module tests. | [Observed readiness result](../../evidence/0004-developer-workflow/codespaces-stabilization.md) |
| CHK-005 | REQ-002, REQ-003, REQ-004, REQ-005, REQ-007, REQ-008 | T-005 | Exercise documented CLI operations on an adopted package and legacy/new phase gates. | [Observed readiness result](../../evidence/0004-developer-workflow/codespaces-stabilization.md) |
| CHK-006 | REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009 | T-006 | Run combined suite, independent concrete review, source identities, naming and local-link scans. | [Observed readiness result](../../evidence/0004-developer-workflow/codespaces-stabilization.md) |
| CHK-007 | REQ-009 | T-007 | Reconcile changed claims and verify complete remote paths, modes and blob identities. | [Observed readiness result](../../evidence/0004-developer-workflow/codespaces-stabilization.md) |
| CHK-008 | REQ-010 | T-008 | Run the separately approved native-client trial plan and review actual behavior against fixed rubrics. | [Reviewed final observation](../../evidence/0004-developer-workflow/native-pilot-closeout.md) |

## Release gates after the frozen pilot

T-008 covers the observed pilot on its pinned framework revision. The changed application distribution has its own release gates.

- Activity: Clean distribution and offline verification are pending for the exact release source. Check both adoption modes, schema upgrades, project foundations, consultation shortcuts, official AWS guidance, optional emulator guidance, and fresh-session continuation.
- Activity: The final distribution's literal `start` observation requires a separately authorized single native invocation.
- Activity: Promotion requires a verified clean template branch, PR review and merge controls, default-branch readback and the release tag.
