# Tasks and verification: <work ID and title>

**Contract:** <requirements.md or bugfix.md and reviewed revision>
**Design:** [design.md](design.md), <reviewed revision or proposed>
**Route / planning review:** <route and actual review evidence>
**Execution scope:** <existing authorization reference and limits, or planning only>

This is the canonical task list. Keep dependencies and completion here; other summaries and metadata link to it. An unchecked box means the outcome is unfinished. A checked box requires its acceptance, relevant verification, and applicable review to be satisfied. Replace instructional placeholders with the actual work.

Allowed activity labels are `ready`, `in progress`, `blocked`, `needs verification`, and `complete`. Use `complete` only with a checked box. Starting work and later waiting does not erase progress. Deferred work is separate and is not silently counted as complete.

## Planning and task review

- Reviewed artifacts and identity: <requirements/design/tasks revisions or content digests>.
- Reviewer and scope: <actual actor; coverage, prerequisites, cycles, sequencing, and verification>.
- Findings and outcome: <pending / changes needed / ready, with evidence>.
- Authority to continue: <actual request, phase decision, or delegated scope; no invented approval>.
- Remaining consequential questions: <only actual blockers, source, and dependent tasks>.

For Quick Spec, this is the combined review after upfront clarification and drafting all three artifacts. Standard routes link their earlier phase reviews and check the task graph here. Preserve existing implementation authority rather than requesting permission for each task. Use `work.json`, where present, as an index to actual source and review evidence, not a second task tracker.

## Implementation tasks

### T-001 — <independently reviewable outcome>

- [ ] T-001 complete

- Activity: ready.
- Type / required: implementation / required.
- Contract / design: REQ-001, REQ-002, REQ-003 / DES-001, DES-002, DES-003, DES-004.
- Prerequisites: none.
- Scope and exclusions: <bounded change>.
- Acceptance: <observable outcome>.
- Verification: CHK-001, CHK-002, CHK-003.
- Evidence / review: <not recorded; later exact result and review references>.
- Blocker and resolver, if any: <actual condition and smallest next action>.

Duplicate the task section for each actual outcome and update its identifiers and links. Preserve the heading, checkbox, `Prerequisites`, `Contract / design`, and `Verification` field names so local tooling can inspect the task graph. List each dependency and ID explicitly; do not use ranges or words such as "all" as substitutes. `none` means no task prerequisite. Record non-task decisions as blockers and link their source.

## Verification matrix

| Check | Requirement or preservation contract | Task | Method and expected result | Evidence and coverage |
| --- | --- | --- | --- | --- |
| CHK-001 | REQ-001 | T-001 | <command/procedure and observable pass condition> | Not run; no evidence |
| CHK-002 | REQ-002 | T-001 | <failure, concurrency, retry, or integration check> | Not run; no evidence |
| CHK-003 | REQ-003 | T-001 | <preservation check> | Not run; no evidence |

Map every required behavior to an appropriate check. Optional property testing does not make acceptance optional. Include cloud verification as pending when it needs an authorized environment; local mocks do not satisfy a real-service claim.

## Evidence record requirements

Store a compact sanitized result in `evidence/<work-id>/` or link the existing CI artifact. Each result identifies:

- Check ID, actual command/procedure, observation, result, and timestamp.
- Source revision and relevant input, fixture, and configuration identities.
- Execution environment and artifact digest when a built artifact was tested.
- Limitations, failed checks, and checks not executed.
- Review identity, scope, findings, and outcome when review is required.

For local uncommitted work, record the base revision and patch identity rather than implying a commit identifies all tested changes. Never label author self-review as independent review. A tool's structural validation does not establish requirement quality, actual approval, or successful runtime behavior.

## Reconciliation and deferred work

When answers, requirements, design, code, inputs, or environment assumptions change, assess affected reviews, checks, and evidence. Preserve applicable results; reopen invalidated completion. Keep old results as history with their original scope and add new evidence separately.

Deferred: <item, reason, impact, and actual decision reference>. Next eligible work follows dependencies and this task list. Keep one current handoff pointing here; do not create a second independently maintained status register.
