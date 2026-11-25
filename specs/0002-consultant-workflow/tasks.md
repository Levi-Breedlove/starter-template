# Tasks and verification: executable consultant workflow

**Contract:** [Requirements](requirements.md).  
**Design:** [Design](design.md).  
**Route:** Quick; combined review under actual delegated repository-maintenance authority.  
**Completion authority:** This file; metadata and handoff reference it.

## Implementation tasks

### T-001 — Make consultation an adaptive persisted procedure

- [x] T-001 complete
- Activity: complete
- Contract / design: REQ-001, REQ-002, REQ-007 / DES-001
- Prerequisites: none
- Scope and exclusions: Entry instructions, procedures, templates and two fictional consultation examples; no claim of a real model trial.
- Acceptance: Known answers are reused; unresolved product decisions are separated from engineering recommendations; review order and continuation authority are explicit.
- Verification: CHK-001
- Evidence / review: [Release candidate verification](../../evidence/0004-developer-workflow/release-reconciliation.md).
- Blocker: none

### T-002 — Implement work state, context and evidence validation

- [x] T-002 complete
- Activity: complete
- Contract / design: REQ-002, REQ-003, REQ-004, REQ-009 / DES-002
- Prerequisites: none
- Scope and exclusions: Local Python engine/CLI, schema and fixtures; no worker execution or semantic-proof claim.
- Acceptance: Routes, traceability, stale evidence, false completion, unsafe paths and malformed state are handled under the documented contract.
- Verification: CHK-002
- Evidence / review: [Release candidate verification](../../evidence/0004-developer-workflow/release-reconciliation.md).
- Blocker: none

### T-003 — Package safe application adoption

- [x] T-003 complete
- Activity: complete
- Contract / design: REQ-005, REQ-007 / DES-003
- Prerequisites: T-002
- Scope and exclusions: Additive installer, manifest, source copy map and fixtures; no native config or plugin installation.
- Acceptance: Existing data/instructions/configuration remain intact; fresh app context excludes the framework backlog; complete packaged tooling runs in a temporary app; repeat application makes no changes.
- Verification: CHK-003
- Evidence / review: [Release candidate verification](../../evidence/0004-developer-workflow/release-reconciliation.md).
- Blocker: none

### T-004 — Supply bounded read-only native hook feedback

- [x] T-004 complete
- Activity: complete
- Contract / design: REQ-003, REQ-006, REQ-007 / DES-004
- Prerequisites: T-002
- Scope and exclusions: Event handler, concrete definitions, optional setup and fake-event tests; no claim of native client loading or trust.
- Acceptance: Context includes saved answers and real next questions; invalid input stays visible; Stop never forces continuation; actual packaged context is read without writes.
- Verification: CHK-004
- Evidence / review: [Release candidate verification](../../evidence/0004-developer-workflow/release-reconciliation.md).
- Blocker: none

### T-005 — Integrate neutral source, records and verification

- [x] T-005 complete
- Activity: complete
- Contract / design: REQ-008, REQ-009 / DES-004
- Prerequisites: T-001, T-002, T-003, T-004
- Scope and exclusions: Neutral current tree, linked docs, updated source records, local suite and publication verification; historic Git objects and repository identity are outside the content rename.
- Acceptance: Current file content/paths meet naming constraints; local links and full fixture suite pass; exact checks and review limits are recorded; final remote tree is compared during delivery.
- Verification: CHK-005
- Evidence / review: [Release candidate verification](../../evidence/0004-developer-workflow/release-reconciliation.md).
- Blocker: none

## Verification matrix

| Check | Requirement | Task | Method and expected result | Evidence |
| --- | --- | --- | --- | --- |
| CHK-001 | REQ-001, REQ-002, REQ-007 | T-001 | Review the consultation guide, router, route procedures, templates and two roleplays against the supplied outcomes and actual CLI. | [Release candidate verification](../../evidence/0004-developer-workflow/release-reconciliation.md) |
| CHK-002 | REQ-002, REQ-003, REQ-004, REQ-009 | T-002 | Run workflow fixtures and independently reproduced path, state, phase and stale-evidence regressions. | [Release candidate verification](../../evidence/0004-developer-workflow/release-reconciliation.md) |
| CHK-003 | REQ-005, REQ-007 | T-003 | Run installer fixtures and actual-source temporary greenfield/brownfield packaging, CLI, link and rerun checks. | [Release candidate verification](../../evidence/0004-developer-workflow/release-reconciliation.md) |
| CHK-004 | REQ-003, REQ-006, REQ-007 | T-004 | Run hook fixtures, malformed-event regressions and Git-root command with actual temporary work metadata; assert no writes. | [Release candidate verification](../../evidence/0004-developer-workflow/release-reconciliation.md) |
| CHK-005 | REQ-008, REQ-009 | T-005 | Scan current content/paths, check local links and run all local fixtures; compare the published tree during repository delivery. | [Release candidate verification](../../evidence/0004-developer-workflow/release-reconciliation.md) |

## Remaining broader work

Real model consultation trials, selected-client hook loading, actual public toolkit operation, durable worker scheduling and authorized cloud delivery remain separate work. See [implementation priorities](../../docs/implementation-plan.md). Their absence is not disguised as a local fixture pass.
