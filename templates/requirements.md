# Requirements: <work ID and title>

**State:** Draft; acceptance has not been recorded.
**Route:** <Requirements-First / Design-First / Quick Spec>
**Project context:** <brief, accepted decisions, and existing contracts>
**Baseline:** <source revision and relevant evidence>

For Design-First work, link the starting design and check derived requirements against the original user goal. For Quick Spec, resolve material questions up front and draft the connected documents without intermediate approval stops. Remove instructional placeholders when creating real work.

## Goal and scope

<Describe the problem, affected users, and observable outcome.>

- Included: <scope>.
- Excluded or deferred: <non-goals and reason>.
- Existing behavior and architecture to preserve: <contracts and accepted constraints>.
- Planning assumptions: <assumption, consequence, and how it will be checked>.

## Consultation decisions

| ID | Gap and consequence | Answer or proposed default | Source / status | Affected requirements |
| --- | --- | --- | --- | --- |
| Q-001 | <actual material ambiguity> | <answer, deferral, or unresolved> | <source; answered, proposed, or unresolved> | <explicit REQ IDs> |

Keep feature-specific answers here and link project-wide decisions from the brief. Inspect known context, derive engineering implications, and recommend an approach before asking one to three unresolved material questions. Update the draft after each answer. A proposed default is not an accepted product decision; record any superseded answer explicitly.

## Behavioral contract

| ID | Condition and required outcome | Acceptance criterion | Required or deferred |
| --- | --- | --- | --- |
| REQ-001 | WHEN <trigger>, THE <named system> SHALL <observable outcome>. | <checkable result, relevant units, and limits> | Required |
| REQ-002 | IF <unwanted condition>, THEN THE <named system> SHALL <defined response>. | <observable failure, retry, or concurrency result> | Required |
| REQ-003 | WHILE <preserved operating state>, THE <named system> SHALL CONTINUE TO <existing behavior>. | <preservation check> | Required |

Include authorization, validation, concurrency, retries, timeouts, and partial failures where they affect this feature. Replace vague claims such as "fast" with a sourced or decided measure, or mark the threshold unresolved. Do not invent retention periods, availability promises, or spending limits to complete the table.

Use the EARS pattern that fits the behavior: ubiquitous (`THE ... SHALL ...`), event (`WHEN`), state (`WHILE`), unwanted condition (`IF ..., THEN`), optional capability (`WHERE`), or an ordered combination. Optional capability describes behavior when a feature exists; it does not make a required acceptance check optional. The [specification operations reference](../docs/reference/specification-operations.md) gives all six original examples and the supported authoring subset. Existing projects can explicitly retain their established format; do not rewrite their contracts just to match a template.

## Requirements analysis

| Finding | Affected requirements | Implementation consequence | Resolution, owner, and source |
| --- | --- | --- | --- |
| <contradiction, ambiguity, missing case, or assumption> | <explicit IDs> | <why it matters> | <derived resolution or actual decision still needed> |

Analysis performed: <not yet / reviewer and actual scope>.

Review interactions across the set, including conflicting constraints and prerequisites. Resolve supported engineering issues directly. Bring unresolved product policy back as a focused question with a suggested resolution. Do not write "no issues" unless analysis occurred. A material blocker prevents dependent implementation from being ready.

For structured new work, run `scripts/workflow.py analyze <work-id>`. Read the returned sources, perform the semantic review, save actual review notes and a response matching `response_schema`, then record it with `analyze <work-id> --record <project-relative-response.json>`. The request's syntax diagnostics do not perform semantic analysis. Save the response before changing reviewed inputs; a stale response is rejected. Keep actual decision sources separate from the generated response and operation history.

## Requirements review

- Artifact identity: <reviewed revision or content digest; not reviewed initially>.
- Reviewer and scope: <actual actor and checks performed>.
- Findings and outcome: <pending / changes needed / ready, with evidence>.
- Product decision source: <actual acceptance or delegated scope; otherwise unresolved>.
- Next transition authority: <existing authorization and limits, or specific decision needed>.

This record describes an actual review. Do not infer user acceptance from silence or document generation. For Quick Spec, link the combined review recorded with the task plan instead of claiming a separate requirements approval. Prior delegated authority can cover continuation; identify it honestly.

In the standard route, present the concrete scope and acceptance behavior for the user's confirmation before design, unless actual prior authority delegates that decision. A recorded analysis is evidence for review; it does not itself approve the requirements. Quick work can generate the connected artifacts and perform the combined technical review without an intermediate user approval pause.

## Change and verification links

The verification matrix belongs in [tasks.md](tasks.md). Every required outcome needs an applicable check and evidence; a required check not run remains pending. Material changes require [design.md](design.md), tasks, reviews, and affected evidence to be reconciled. Preserve unaffected work and historical decisions.
