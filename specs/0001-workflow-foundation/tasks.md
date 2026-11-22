# Tasks and verification: workflow foundation

**Work:** 0001-workflow-foundation.  
**Contract:** [Requirements](requirements.md).  
**Design:** [Design](design.md).  
**Authority:** This is the sole framework implementation checklist. The roadmap, research acceptance catalogs, and handoff reference it.

Activity labels describe progress. A checked box means that task's stated outcome is evidenced; it does not imply that all requirements in the larger framework are implemented. The present authorization covers research, the bootstrap, offline checks, and repository delivery. Later runtime trials, paid/background activity, and AWS operations use their actual task authorization and limits.

## Phase 0 — Research and usable skeleton

### T-001 — Research and map the complete Kiro workflow

- [ ] T-001 complete

- Activity: needs verification.
- Requirements/design: REQ-001, REQ-002, REQ-017 / DES-01, DES-08.
- Dependencies: none.
- Scope: Official Kiro/Codex/AWS sources, accessible official video material, mechanism and surface distinctions, exact gaps and proposed improvements.
- Acceptance: Auditable source/access ledger; documented versus observed versus proposed claims remain separate; no private-skill dependency or unviewed-video claim.
- Verification: CHK-001; review the cited evidence and capability mapping.
- Evidence: Research documents and final scaffold verification receipt when recorded.

### T-002 — Deliver the reusable instruction and artifact skeleton

- [ ] T-002 complete

- Activity: needs verification.
- Requirements/design: REQ-002–REQ-005, REQ-008–REQ-011, REQ-016, REQ-018 / DES-02–DES-05.
- Dependencies: T-001.
- Scope: Root router, all procedure contracts, both adoption guides, original templates, project records, worked example, architecture, roadmap and handoff.
- Acceptance: A reader can follow an end-to-end change and find every artifact; brownfield authority/layout are preserved; application/runtime status is honest; requested repository contains the delivered files.
- Verification: CHK-002, CHK-004; cross-document review and publication readback.
- Evidence: Final scaffold verification receipt and resulting repository commit.

### T-003 — Supply and verify the bounded offline checker

- [ ] T-003 complete

- Activity: needs verification.
- Requirements/design: REQ-018 / DES-08.
- Dependencies: T-002's file structure; can implement independently while documents are drafted.
- Scope: Standard-library local Markdown file-target/core-path checks and relevant fixtures.
- Acceptance: Missing/outside-root targets and incomplete scans fail visibly; examples and placeholders are handled within documented scope; no remote calls.
- Verification: CHK-003, CHK-004; reviewer findings reproduced and fixed, fixture suite and final scan pass.
- Evidence: Final scaffold verification receipt.

## Phase 1 — Deterministic work contracts

### T-010 — Validate work IDs, dependencies, and traceability

- [ ] T-010 complete

- Activity: ready after Phase 0.
- Requirements/design: REQ-005, REQ-006 / DES-03, DES-04.
- Dependencies: T-001–T-003.
- Scope: Versioned parser/representation for stable requirement/task/check IDs, required/deferred state, dependencies, and evidence references.
- Acceptance: Detect missing/duplicate IDs, dangling dependencies, cycles, unverified required outcomes, and conflicting authority. Do not demand a new layout from brownfield projects.
- Verification: CHK-010; positive/negative temporary fixtures with deliberately broken contracts.
- Evidence: Not implemented or run.

### T-011 — Bind evidence and invalidate affected outcomes

- [ ] T-011 complete

- Activity: blocked by T-010.
- Requirements/design: REQ-006, REQ-009, REQ-011 / DES-04.
- Dependencies: T-010.
- Scope: Source/patch, spec, fixture, configuration, artifact, environment, and procedure identities; impact and freshness rules.
- Acceptance: Changing each relevant input invalidates affected claims and descendants; unaffected evidence retains scope; old observations are preserved.
- Verification: CHK-011; mutation fixtures, incomplete metadata, stale artifact and same-source/different-config cases.
- Evidence: Not implemented or run.

### T-012 — Implement bounded context selection and authority mapping

- [ ] T-012 complete

- Activity: blocked by T-010.
- Requirements/design: REQ-003, REQ-004, REQ-016 / DES-02, DES-06.
- Dependencies: T-010.
- Scope: Context manifests, relevant instruction/reference selection, existing authority/path maps, current handoff recovery.
- Acceptance: Load relevant accepted constraints, identify conflicts and unknown facts, preserve adopted authority, and avoid loading unrelated personal skills or the entire research corpus.
- Verification: CHK-012; greenfield and conflicting brownfield fixtures with changed/dirty files.
- Evidence: Not implemented or run.

## Phase 2 — Native integration

### T-020 — Implement and verify supported Codex event adapters

- [ ] T-020 complete

- Activity: blocked by Phase 1 and a selected client.
- Requirements/design: REQ-002, REQ-012, REQ-014 / DES-06.
- Dependencies: T-010–T-012.
- Scope: One supported hook configuration source, deterministic handlers, event parsing, trust and capability reporting.
- Acceptance: Only supported/trusted events run; duplicate/recursive events and timeouts are bounded; no implicit AWS or paid background operation.
- Verification: CHK-020; fake-event tests followed by an authorized bounded native-client trial.
- Evidence: No active hook configuration or native trial.

### T-021 — Verify worker and reviewer isolation

- [ ] T-021 complete

- Activity: blocked by Phase 1 and a selected client/interface.
- Requirements/design: REQ-007, REQ-008 / DES-06.
- Dependencies: T-010–T-012.
- Scope: Structured worker requests/results, scoped files/worktrees, fresh review context, final integrated-candidate validation.
- Acceptance: Reviewer can challenge a seeded author assumption; timeout/incomplete review cannot pass; observed results match artifacts; conflicting writers are controlled.
- Verification: CHK-021; fake-worker fixtures and a bounded real-client exercise within actual authorization.
- Evidence: Not implemented or run.

## Phase 3 — Durable execution

### T-030 — Persist run/attempt state and validated results

- [ ] T-030 complete

- Activity: blocked by T-011 and T-021.
- Requirements/design: REQ-006, REQ-013 / DES-07.
- Dependencies: T-011, T-021.
- Scope: Select controller interface/language, versioned contracts, atomic persistence, append-only event history and sanitized evidence export.
- Acceptance: Crash windows preserve recoverable intent/outcome and unknown state; runtime history does not become a competing task authority.
- Verification: CHK-030; fault injection around dispatch, effect, validation, and persistence.
- Evidence: Not implemented or run.

### T-031 — Schedule dependencies, bounded loops, and joins

- [ ] T-031 complete

- Activity: blocked by T-030.
- Requirements/design: REQ-007, REQ-008, REQ-014 / DES-07.
- Dependencies: T-010, T-021, T-030.
- Scope: Eligible-node selection, ownership, worker limits, review/correction loops, aggregation and integrated validation.
- Acceptance: Dependencies and limits hold; independent branches may overlap; failed/incomplete prerequisites block descendants; final validation uses the joined candidate.
- Verification: CHK-031; dependency, shared-file, repeated-failure and cap scenarios.
- Evidence: Not implemented or run.

### T-032 — Reconcile uncertain outcomes and resume safely

- [ ] T-032 complete

- Activity: blocked by T-030–T-031.
- Requirements/design: REQ-009, REQ-013, REQ-014 / DES-04, DES-07.
- Dependencies: T-011, T-030, T-031.
- Scope: Pause/stop/retry distinctions, partial edits, external receipt inspection, preserved counters, changed-input resumption.
- Acceptance: No blind replay of an unknown effect; completed siblings survive; counters do not reset; changed contracts invalidate dependent outcomes.
- Verification: CHK-032; process interruption and fake external-operation receipts across restart boundaries.
- Evidence: Not implemented or run.

### T-033 — Integrate bounded PR/CI feedback events

- [ ] T-033 complete

- Activity: blocked by T-030–T-032 and a selected existing integration.
- Requirements/design: REQ-012, REQ-014, REQ-015 / DES-07.
- Dependencies: T-020, T-030–T-032.
- Scope: Event IDs/cursors, PR/head identity, disposition, current checks, terminal stop rules, supported idle waits.
- Acceptance: Duplicate feedback does not repeat work; stale checks cannot pass a new head; closed/merged scope stops; no model turns while idle; message/merge/deploy authority is not inferred.
- Verification: CHK-033; replay, old-head, no-event, close/reopen and deadline fixtures before any authorized live integration.
- Evidence: Not implemented or run.

## Phase 4 — Adoption and AWS evidence

### T-040 — Exercise a complete greenfield change

- [ ] T-040 complete

- Activity: ready for a separately scoped conversational trial; automated trial depends on adapters.
- Requirements/design: REQ-003–REQ-009, REQ-017 / DES-02–DES-04, DES-08.
- Dependencies: T-002 for conversational trial; T-010–T-032 for automated claims.
- Scope: Representative application feature with a clear failure path and invariant.
- Acceptance: Original outcomes, actual code/tests, independent review where selected, reconciliation, and handoff agree; no fabricated cloud evidence.
- Verification: CHK-040; recorded fixture/candidate and acceptance results.
- Evidence: Not run; example documents are not a trial.

### T-041 — Exercise brownfield adoption and preserved behavior

- [ ] T-041 complete

- Activity: ready for a separately scoped conversational trial; automated trial depends on adapters.
- Requirements/design: REQ-003, REQ-008, REQ-009, REQ-016 / DES-02–DES-04, DES-08.
- Dependencies: T-002 for conversational trial; applicable adapters for automated claims.
- Scope: Existing layout, user edits, test baseline, protected interface, and IaC/pipeline ownership.
- Acceptance: A bounded change preserves required behavior, dirty work, actual authority, architecture and delivery controls; declared/observed/unknown state remain distinct.
- Verification: CHK-041; baseline versus candidate comparison and preservation checks.
- Evidence: Not run.

### T-042 — Verify public official toolkit capabilities on the selected surface

- [ ] T-042 complete

- Activity: needs selected surface and an authorized public capability check.
- Requirements/design: REQ-002, REQ-010 / DES-05, DES-06.
- Dependencies: T-002.
- Scope: Availability/installation/loading/public-call evidence, official identity, documented release and task skill preference.
- Acceptance: Public path works without account probing; unavailable updates/tools are reported; no duplicate/private plugin replacement or credential access.
- Verification: CHK-042; bounded public documentation response and capability record.
- Evidence: Documentation researched; actual adopter capability trial not run.

### T-043 — Verify one scoped AWS release and recovery

- [ ] T-043 complete

- Activity: blocked by a concrete project, named environment, and actual operational authorization.
- Requirements/design: REQ-010, REQ-011, REQ-013 / DES-05, DES-08.
- Dependencies: T-040 or T-041, T-042, project release readiness.
- Scope: Existing pipeline/IaC, applicable preview/artifact, target limits, meaningful cloud acceptance, recovery and cleanup ownership.
- Acceptance: Full applicable release identity and observations; missing/nonapplicable evidence explicit; recovery observed within scope; no claimed blanket parity.
- Verification: CHK-043; project-specific approved procedure and actual results.
- Evidence: No AWS operations performed for the initial bootstrap.

## Phase 5 — Comparative evaluation

### T-050 — Evaluate parity and publish supported claims

- [ ] T-050 complete

- Activity: blocked by implemented capabilities and comparable recorded trials.
- Requirements/design: REQ-001, REQ-002, REQ-017 / DES-01, DES-08.
- Dependencies: Relevant completed adapters/trials for each claim; T-043 only for cloud claims.
- Scope: Matched fixtures, acceptance, access, product/model versions, limits and evaluators; quality, interventions, time and actual cost where observable.
- Acceptance: Per-scenario results support bounded conclusions; unknowns and variability disclosed; no generalized superiority claim from one success.
- Verification: CHK-050; [evaluation protocol](../../evaluations/README.md) and repeatable evidence.
- Evidence: No benchmark run.

## Verification matrix

| Check | Tasks | Method / expected evidence | Current result |
| --- | --- | --- | --- |
| CHK-001 | T-001 | Source/access review; product mechanism, surface, video and proposal distinctions. | Final review pending. |
| CHK-002 | T-002 | Cross-document review of adoption, authority, scope, template traceability, truthful capability status. | Final review pending. |
| CHK-003 | T-003 | `python3 -m unittest discover -s tests -p 'test_*.py' -v`; meaningful checker fixtures pass. | Final run pending. |
| CHK-004 | T-002, T-003 | `python3 scripts/check_repository.py`; final local links/core paths pass; remote file identities checked at publication. | Final run/publication pending. |
| CHK-010–012 | T-010–T-012 | Work graph/traceability, changed-input freshness, and context/authority fixtures. | Not implemented or run. |
| CHK-020–021 | T-020–T-021 | Native event trust/coverage and worker/reviewer context evidence. | Not implemented or run. |
| CHK-030–033 | T-030–T-033 | Crash/retry/state/limit/event fixtures and later scoped integration evidence. | Not implemented or run. |
| CHK-040–043 | T-040–T-043 | Real adoption/public-toolkit/project-cloud trials with exact scope. | Not run. |
| CHK-050 | T-050 | Matched comparison under the evaluation protocol. | Not run. |

## Deferred optional extensions

Repository skill packaging, Kiro recipe interchange, a native spec dashboard, multi-repository portfolio coordination, and scheduled/unattended service operation remain deferred. They are not prerequisites for the usable conversational workflow and are not counted as completed work.

