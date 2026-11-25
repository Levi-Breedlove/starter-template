# v1.0.1 documentation work

### T-001 — Supply editable repository conventions

- [x] T-001 complete
- Activity: complete
- Contract / design: REQ-001, REQ-002 / DES-001
- Prerequisites: none
- Scope and exclusions: Update the existing structure Markdown seed and its adoption verification. Preserve the existing manifest, installer ownership and directory layout.
- Acceptance: New projects receive the agreed conventions. Existing brownfield and v1.0.0 stock or customized records retain their original path and bytes.
- Verification: CHK-001
- Evidence / review: [Verified closeout candidate](../../evidence/0005-repository-documentation/closeout-review.md).
- Blocker: none

### T-002 — Document and verify the packaged developer experience

- [x] T-002 complete
- Activity: complete
- Contract / design: REQ-003, REQ-004, REQ-005, REQ-006 / DES-002
- Prerequisites: T-001
- Scope and exclusions: Developer-facing README, first-feature guide, concise maintainer README, patch changelog, presentation asset cleanup and local verification. Review branches carry the candidate. Owner approval controls release promotion. Native invocations and AWS actions are outside scope.
- Acceptance: The packaged README matches the approved concise source and resolves all six guide links. The packaged first-feature guide preserves the illustrative appointment-booking walkthrough. The 102-file distribution is reproducible and clean of inherited work. Existing regressions and adoption checks pass. The candidate awaits owner release approval.
- Verification: CHK-002
- Evidence / review: [Verified closeout candidate](../../evidence/0005-repository-documentation/closeout-review.md).
- Blocker: none

## Verification matrix

| Check | Requirements | Task | Method and expected result | Evidence |
| --- | --- | --- | --- | --- |
| CHK-001 | REQ-001, REQ-002 | T-001 | Inspect generated conventions in a fresh template and greenfield app. Compare conventional and mapped brownfield records and stock and customized v1.0.0 records before and after upgrade, including repeat adoption. | [Closeout verification](../../evidence/0005-repository-documentation/closeout-review.md) |
| CHK-002 | REQ-003, REQ-004, REQ-005, REQ-006 | T-002 | Compare the approved source and generated README, check its six guide links and initial tree, and verify the relocated illustrative walkthrough. Compare two distribution builds and run full regressions, both repository checkers and local adoption checks. | [Closeout verification](../../evidence/0005-repository-documentation/closeout-review.md) |
