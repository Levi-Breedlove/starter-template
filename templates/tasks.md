# Tasks and verification: <work ID and title>

**Contract:** <requirements.md or bugfix.md and accepted revision>
**Design:** [design.md](design.md), <accepted revision or proposed>
**Execution scope:** <existing authorization reference and limits, or planning only>

This is the canonical task list. Keep task state here; other summaries link to it. An unchecked box means the outcome is unfinished. A checked box requires its acceptance, relevant verification, and applicable review to be satisfied.

Allowed activity labels are `ready`, `in progress`, `blocked`, `needs verification`, and `complete`. Use `complete` only with a checked box. Starting work and later waiting does not erase its progress. Deferred work is listed separately and is not silently counted as complete.

## Implementation tasks

### T-001 — <independently reviewable outcome>

- [ ] T-001 complete

- Activity: <ready or named current state>.
- Type / required: <implementation, verification, documentation, or investigation> / <required or deferred>.
- Contract / design: <REQ IDs or defect/preservation IDs> / <DES references>.
- Prerequisites: <real task or decision IDs; none if independent>.
- Scope and exclusions: <bounded change>.
- Acceptance: <observable outcome>.
- Verification: <CHK IDs and project commands or procedure>.
- Evidence / review: <not recorded; later exact result and review references>.
- Blocker and resolver, if any: <actual condition and smallest next step>.

## Verification matrix

| Check | Requirement or preservation contract | Task | Method and expected result | Evidence and coverage |
| --- | --- | --- | --- | --- |
| CHK-001 | <REQ-001> | T-001 | <command/procedure; observable pass condition> | Not run; no evidence |
| CHK-002 | <REQ-002> | <task> | <concurrency/failure/integration check> | Not run; no evidence |

Record each required behavior here. A property test is one possible method; it does not replace a relevant real-service integration check.

## Evidence record requirements

Store a compact sanitized result in `evidence/<work-id>/` or link the existing CI artifact. Each result identifies:

- Check ID, actual command or procedure, result, and timestamp.
- Source revision and relevant input, fixture, and configuration identities.
- Execution environment; artifact digest when a built artifact was tested.
- Observed result, limitations, and any check not executed.
- Review identity, scope, and result when review is required.

For local uncommitted work, record the base revision and patch identity rather than implying a commit identifies the tested changes. Never label author self-review as independent review.

## Reconciliation and deferred work

When requirements, design, source, inputs, or environment assumptions change, identify affected checks and evidence. Preserve unaffected results; reopen only invalidated outcomes. Keep old results as history with their original scope and add current results separately.

Deferred: <item, reason, impact, and decision reference>. Next eligible work is derived from dependencies and this task list; do not create a second independently maintained status register.
