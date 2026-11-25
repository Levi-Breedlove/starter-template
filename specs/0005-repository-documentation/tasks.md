# v1.0.1 documentation work

### T-001 — Supply editable repository conventions

- [x] T-001 complete
- Activity: complete
- Contract / design: REQ-001, REQ-002 / DES-001
- Prerequisites: none
- Scope and exclusions: Update the existing structure Markdown seed and its adoption verification. Preserve the existing manifest, installer ownership and directory layout.
- Acceptance: New projects receive the agreed conventions. Existing brownfield and v1.0.0 stock or customized records retain their original path and bytes.
- Verification: CHK-001
- Evidence / review: [Adoption and upgrade observations](../../evidence/0005-repository-documentation/walkthrough-review.md#candidate-verification).
- Blocker: none

### T-002 — Document and verify the packaged developer experience

- [x] T-002 complete
- Activity: complete
- Contract / design: REQ-003, REQ-004, REQ-005, REQ-006 / DES-002
- Prerequisites: T-001
- Scope and exclusions: Developer-facing README, concise maintainer README, patch changelog and local verification. Remote publication, native invocations and AWS actions are outside this task.
- Acceptance: The packaged README describes the actual tree, consultation, onboarding and permissions. It teaches each of the six artifacts with its full name and prefix, plain-language meaning and question, usual location, concrete example and relationships. Descriptive diagram labels and one explicitly illustrative appointment-booking retry connect intended behavior, technical approach, implementation work, verification procedure and observed evidence. The verified candidate has reproducible distribution bytes, passing regressions and correct local documentation links and anchors. The owner can evaluate promotion from the current evidence.
- Verification: CHK-002
- Evidence / review: [README and distribution verification](../../evidence/0005-repository-documentation/walkthrough-review.md#walkthrough-review).
- Blocker: none

## Verification matrix

| Check | Requirements | Task | Method and expected result | Evidence |
| --- | --- | --- | --- | --- |
| CHK-001 | REQ-001, REQ-002 | T-001 | Inspect generated conventions in a fresh template and greenfield app. Compare conventional and mapped brownfield records and stock and customized v1.0.0 records before and after upgrade, including repeat adoption. | [Revised candidate verification](../../evidence/0005-repository-documentation/walkthrough-review.md) |
| CHK-002 | REQ-003, REQ-004, REQ-005, REQ-006 | T-002 | Inspect the generated tree and README. Walk the same illustrative appointment-booking retry through all six named artifacts. Check every prefix, plain-language explanation and question, storage location, practical example, relationship and descriptive diagram label. Confirm the verification procedure and observed result are distinct, and illustrative outcomes are labeled separately from actual candidate evidence. Exercise the documented entry points offline. Compare two builds and run source and package checkers, local link and anchor checks and the full regression suite. | [Revised candidate verification](../../evidence/0005-repository-documentation/walkthrough-review.md) |
