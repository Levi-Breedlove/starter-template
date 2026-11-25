# v1.0.1 documentation work

### T-001 — Supply editable repository conventions

- [ ] T-001 complete
- Activity: ready
- Contract / design: REQ-001, REQ-002 / DES-001
- Prerequisites: none
- Scope and exclusions: Update the existing structure Markdown seed and its adoption verification. Preserve the existing manifest, installer ownership and directory layout.
- Acceptance: New projects receive the agreed conventions. Existing brownfield and v1.0.0 stock or customized records retain their original path and bytes.
- Verification: CHK-001
- Evidence / review: Pending local adoption and upgrade observations.
- Blocker: none

### T-002 — Document and verify the packaged developer experience

- [ ] T-002 complete
- Activity: ready
- Contract / design: REQ-003, REQ-004, REQ-005, REQ-006 / DES-002
- Prerequisites: T-001
- Scope and exclusions: Developer-facing README, concise maintainer README, patch changelog and local verification. Remote publication, native invocations and AWS actions are outside this task.
- Acceptance: The packaged README describes the actual tree and illustrates future work, consultation, traceability, onboarding and permissions. The verified candidate has reproducible distribution bytes, passing regressions and correct local documentation links and anchors. The owner can evaluate promotion from the current evidence.
- Verification: CHK-002
- Evidence / review: Pending candidate-specific documentation and offline release verification.
- Blocker: none

## Verification matrix

| Check | Requirements | Task | Method and expected result | Evidence |
| --- | --- | --- | --- | --- |
| CHK-001 | REQ-001, REQ-002 | T-001 | Inspect generated conventions in a fresh template and greenfield app. Compare conventional and mapped brownfield records and stock and customized v1.0.0 records before and after upgrade, including repeat adoption. | Pending |
| CHK-002 | REQ-003, REQ-004, REQ-005, REQ-006 | T-002 | Inspect the generated README, tree and example against the requirements. Exercise the documented entry points offline. Compare two builds and run source and package checkers, local link and anchor checks and the full regression suite. | Pending |
