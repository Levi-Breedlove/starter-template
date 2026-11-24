# Current handoff

**Active work** 0004-developer-workflow

**State** The native pilot used the frozen readiness source `64875eeeb24e615a2fa92d5b9c02503fab7a01be` and Codex CLI 0.172.0. The Codespaces host preflight passed. B1–B4 completed. The operator verified and applied the G3 controller candidate `dc9d26da24ef6e447505b74e43775995e80c5595` in the disposable greenfield repository.

**Release gate** G4 implemented its changed booking contract and passed all 16 tests. It exited 124 at the 900-second deadline without updating the mapped handoff or returning its final structured response. T-008 and CHK-008 remain open. Eleven launches consumed eight original slots and three explicitly authorized replacements. [Pilot results](../evidence/0004-developer-workflow/native-pilot-results.md) · [Canonical task ledger](../specs/0004-developer-workflow/tasks.md)

**Next action** Preserve the partial greenfield result, test receipts, historical handoff, Git bundles, and all reservations. A further native G4 observation requires explicit authority under the frozen limits. A successful observation must update the mapped handoff and produce a completed turn and final stage result as well as passing the local checks. Review the evidence before marking T-008 complete. [Execution plan](../specs/0004-developer-workflow/exec-plan.md)

The repository is `Levi-Breedlove/starter-template`. Maintenance work belongs on `codespaces-readiness`, the head of draft PR #1 targeting `main`. The original local pilot checkout has preserved uncommitted evidence. The future clean distribution and v1.0.0 release are pending.

## Earlier offline stabilization

**State** Offline stabilization passed on `26f21269460366a7743814461fa126c3bfbd7bdd` in the
`codespaces-readiness` worktree. The source fast-forward and full
GitHub tree readback matched. All 197 regression tests and the source structure
check passed. Both adoption modes, the installed CLI, and all five routes were
exercised. The original checkout and both startup receipts were verified
byte-for-byte. [Readiness assessment](../evidence/0004-developer-workflow/codespaces-stabilization.md) ·
[Canonical tasks](../specs/0004-developer-workflow/tasks.md)

Fingerprint-checked reconciliation refreshed the affected evidence in 0002,
0003, and 0004. The requirements, design, phase reviews, and recorded analysis
and properties continue to identify their accepted inputs.
[Execution plan](../specs/0004-developer-workflow/exec-plan.md)
