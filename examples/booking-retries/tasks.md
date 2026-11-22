# Tasks and verification: EX-001 — Safe booking retries

**State:** Illustrative planning only. No tasks have been executed.
**Contract:** [requirements.md](requirements.md). **Design:** [design.md](design.md).

This is the example's canonical task list. Every box is intentionally unchecked. The prerequisites describe the proposed work order, not authorization to execute it.

## Task list

### T-001 — Accept the retention and API response contract

- [ ] T-001 complete

Activity: blocked pending project decisions. Type: decision and specification; required. Prerequisites: a real project's owner and existing API baseline.

Acceptance: select retention and expiry behavior, canonical business fields, conflict and in-progress responses, and preserved baseline behavior. Reconcile all affected requirements and DES-001. Verify with CHK-000. Evidence: none.

### T-002 — Implement and verify atomic persistence

- [ ] T-002 complete

Activity: blocked by T-001 and selection of an actual persistence system. Type: implementation; required. Contract: REQ-001 through REQ-004 and REQ-006. Design: DES-001 and DES-002.

Acceptance: implement the scoped identity, replay record, transaction behavior, and uniqueness mechanism without changing existing booking-conflict rules. Verify relevant storage behavior with CHK-002, CHK-003, CHK-004, and CHK-006. Evidence: none.

### T-003 — Integrate the API behavior and preservation path

- [ ] T-003 complete

Activity: blocked by T-002. Type: implementation; required. Contract: REQ-001 through REQ-006. Design: DES-001 and DES-003.

Acceptance: expose the accepted response contract and retain the established no-key behavior and authorization checks. Run CHK-001, CHK-002, CHK-005, and CHK-006 against the integrated behavior. Evidence: none.

### T-004 — Validate the contract and review the complete change

- [ ] T-004 complete

Activity: blocked by T-002 and T-003. Type: verification and independent review; required. Contract: all requirements. Design: DES-004.

Acceptance: run all required checks on the same candidate, assess the change against the original requirements, resolve material findings, and record explicit limitations. Independent review requires a distinct reviewer. Evidence: none; review not performed.

## Verification matrix

| Check | Requirement | Task | Method and expected result | Current evidence |
| --- | --- | --- | --- | --- |
| CHK-000 | All; pending contract decisions | T-001 | Requirements and interface review resolves blocking ambiguity and preserves baseline scope. | Not performed |
| CHK-001 | REQ-001 | T-003, T-004 | Repeat a successful identical request and verify one booking and stable original result. | Not run |
| CHK-002 | REQ-002 | T-002, T-003, T-004 | Change validated fields while retaining the key; verify defined conflict and unchanged booking. | Not run |
| CHK-003 | REQ-003 | T-002, T-004 | Use concurrent transactions and varied duplicate-request sequences; assert at most one committed booking. | Not run |
| CHK-004 | REQ-001, REQ-004 | T-002, T-004 | Inject failure before commit and response loss after commit; verify rollback/retry and replay respectively. | Not run |
| CHK-005 | REQ-005 | T-003, T-004 | Run established no-key validation, authentication, and booking-conflict checks. | No baseline supplied; not run |
| CHK-006 | REQ-006 | T-002, T-003, T-004 | Reuse the text key across two customers and attempt unauthorized access; verify isolation and rejection. | Not run |

## Evidence, reconciliation, and release boundary

Real result records must identify the source revision or patch, artifact if built, environment, fixtures/configuration, actual check, result, and review scope. This example has none of those results.

A change to identity scope, canonical fields, transaction mechanism, retention, or response semantics must trigger affected-spec reconciliation and coverage review. Earlier results can remain historical; only valid coverage can support completion of the current candidate.

Deferred: load and capacity targets, live AWS integration, deployment, and operational acceptance. They require a selected real project, appropriate acceptance criteria, and the relevant execution authorization. Completing these example implementation tasks would not by itself authorize or verify an AWS release.
