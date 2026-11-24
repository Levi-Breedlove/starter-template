# Lead a consultation that produces an implementable plan

Codex should act as the engineering consultant: understand the goal, inspect existing evidence, identify the consequences, investigate AWS options, recommend an approach, and ask only for missing decisions that matter. The interview builds the specification as it proceeds. It is neither a fixed questionnaire nor a single response that guesses all missing business rules.

Use [Consult](../workflows/consult.md) as the procedure and [Feature](../workflows/feature.md) or [Bugfix](../workflows/bugfix.md) for the selected delivery route. [Greenfield and brownfield examples](../examples/consultation/README.md) show the expected interaction.

## Begin with what is already known

Read the user's request and previous decisions, the mapped project brief and handoff, relevant specifications, and actual code/tests/infrastructure. In an existing project, complete the relevant [brownfield baseline](05-brownfield-adoption.md). Do not ask questions answered by this evidence.

Classify the important information before choosing the next question:

| Kind | What Codex does | Example |
| --- | --- | --- |
| Established fact or accepted constraint | Reuse it and cite its source. Resolve a conflict only if evidence differs. | The project already uses Python, PostgreSQL, Terraform, and its existing pipeline. |
| Engineering implication | Derive it, explain it when useful, and design appropriate checks. | Preventing duplicate reservations requires an authoritative concurrency mechanism and a retry contract. |
| Researched recommendation or planning assumption | Investigate, recommend, state the tradeoff, and label uncertainty. | Recommend a managed runtime for the actual workload; estimate using an explicit traffic range. |
| Missing product or authority decision | Ask a focused question with its consequence and a recommended answer when supported. | Does a booking confirm immediately, or require a staff decision? |

The first response should briefly state the understood outcome and constraints, the proposed direction, and the next consequential uncertainty. If the request is too vague to identify a user or outcome, ask that foundational question first. Do not research an elaborate architecture for an undefined product.

## Conduct adaptive rounds

Ask **one to three material questions at a time**. Choose the questions that unblock the next useful artifact or resolve the most consequential uncertainty. Explain why the answer changes the product, design, cost, or permitted action. Offer a recommendation with its rationale; allow a free-form answer or correction.

After each reply:

1. Record the actual answer and its source in the authoritative brief or work contract.
2. Update the draft requirements, design assumptions, or proposed scope affected by it.
3. Derive new engineering implications and research technical questions.
4. Check whether any remaining uncertainty materially blocks the next stage.
5. Ask the next small batch only if needed; otherwise move to the appropriate review.

This is a loop, not a prescribed number of rounds. A detailed request may need none. A novel product may need several short rounds. A correction can reopen an earlier decision. Do not keep asking after the first useful scope is adequately defined.

When the user says “you decide,” decide the engineering details within their delegated scope and record the rationale. That delegation does not supply unknown business policy or authorize a new account operation. A deferral remains a deferral: explain which work can proceed and which outcome depends on it.

## Investigate the right areas without sending a checklist

The following areas help Codex find gaps. They are not a list of questions the user must answer.

| Area | Inspect or derive first | Ask when the missing answer changes the contract |
| --- | --- | --- |
| Users and outcome | Existing journeys, roles, scope, and acceptance evidence. | The primary user, success condition, or first-release priority is unclear. |
| Business behavior | Existing validation, state transitions, permissions, retries, and errors. | Approval, cancellation, conflict, or eligibility rules remain ambiguous. |
| Data and compatibility | Schemas, consumers, retention decisions, privacy/security requirements, migrations. | A missing retention or compatibility promise changes data handling. |
| Reliability and recovery | Existing objectives, failure paths, operations, and realistic mechanisms. | The business must choose a consequential recovery or availability tradeoff. |
| Workload and cost | Known traffic, service limits, current official pricing, and a range of assumptions. | A spending limit or demand scenario is necessary for a material commitment. |
| Delivery and operation | Established pipeline, release controls, environment policy, and ownership. | A required owner, target, access scope, or release decision is unresolved. |

Do not ask “Lambda or containers?” as a substitute for analysis. Establish the workload, preserve selected architecture, research relevant official guidance, and recommend the mechanism. Surface a choice when its business or operational consequence warrants one. Likewise, do not invent arbitrary retention periods, recovery commitments, budgets, or authorization to make a document look complete.

For public AWS consultation, use the existing official Core/Data Analytics capabilities described in [AWS guidance and access](02-aws-guidance-and-access.md). Honor a documentation-only or no-skills instruction by consulting official documentation directly. Cite material service guidance and estimate assumptions in the design or decision record. Account-specific facts remain unknown until supplied evidence or an authorized observation establishes them.

## Save answers and drafts continuously

Keep project-wide decisions in the mapped project brief. Keep feature decisions in `specs/<work-id>/requirements.md`; keep defect decisions in `bugfix.md`. An answer has an ID when needed for traceability, its consequence, actual source, status, affected requirements, and a superseded-answer reference when applicable. Avoid storing a full chat transcript when a concise decision is enough.

`work.json` indexes context, facts, questions, reviews, and evidence for the local workflow tools. Keep its summaries and source references aligned with the authoritative documents. It does not replace the requirements or create a second task tracker. Task dependencies and completion are read from `tasks.md`.

Save useful drafts while decisions remain open. A handoff records the work ID, current artifacts, exact pending question, reason it matters, what can continue, and the next action. Resume from those records and current code. Reconcile conflicts before reusing stale answers or evidence.

## Analyze and review in the selected order

Requirements need observable conditions and outcomes, relevant limits, failure behavior, and preservation obligations. Read them together for contradictory constraints, undefined terms, unstated preconditions, and missing boundary or concurrent cases. Resolve technical findings from evidence. A product conflict becomes a focused follow-up question with the affected requirements and a proposed resolution.

For new structured work, draft explicit EARS statements and use `analyze` to prepare a source-bound review request. Supply the actual findings and decision sources, then record the response. Derive observable correctness properties from requirements/design with `properties`, choosing verification strategies that fit each claim. Map properties to real task/check IDs before accepting tasks. Those operations preserve the reasoning outcome; they do not replace the conversation or grant acceptance. [Specification operations](../docs/reference/specification-operations.md)

| Route | What is actually reviewed |
| --- | --- |
| Requirements-First | Review the analyzed requirements; then the design against them; then task coverage and dependencies. |
| Design-First | Review the proposed architecture or technical change; derive requirements and review them against user intent; reconcile any design gap; review the task plan. |
| Quick Spec | Clarify material gaps up front; create requirements, design, and tasks together; review their combined consistency and scope before implementation. No per-document approval stops. |
| Bugfix | Review incorrect, expected, and preserved behavior; investigate and review the correction; review reproduction, fix, and regression tasks. |
| Plan-led | Review a concise investigated plan. The CLI records planning completion as `planned`; execution is a distinct handoff. |

A real review records the inspected artifacts and their identities, actual reviewer, findings, outcome, and the source of acceptance or delegation. Product acceptance, technical readiness, permission to implement, and permission to deploy are different facts. The workflow should not ask for the same permission again when existing authority covers the next action.

For a reserved decision, present the concrete result and ask for the missing decision. Under actual delegated authority, perform the review and continue, identifying the reviewer and delegation accurately. Never record the user's acceptance because they were silent or because Codex generated a document. Author self-review must not be labeled independent review. A separate reviewer must actually inspect the current candidate with enough independent context to challenge it.

## Use the local state tools honestly

From an adopted application root, `context`, `status`, and `validate` are read-only:

```bash
python3 .aws-workflow/scripts/workflow.py --root . context --compact
python3 .aws-workflow/scripts/workflow.py --root . status
python3 .aws-workflow/scripts/workflow.py --root . validate
```

Codex conducts the consultation and edits the substantive artifacts. The CLI makes recorded state and structural problems visible; it does not conduct an interview, authenticate a reviewer, or establish that requirements are good.

At a fresh application start, `doctor` works without active work. During drafting, compact context identifies required analysis/property work before the applicable acceptance boundary. After a consequential change, use the `sync` preview to assess affected reviews and completion, then deliberately apply its exact current fingerprint. Reuse still-current answers and outcomes.

After an actual review, `review` records an artifact, `accepted` or `changes-requested`, a real `--decision-ref`, the actual `--reviewer`, and `--authority user` or `--authority delegated`. Write the review evidence before recording it so the snapshot identifies the reviewed content. `advance --to <next-phase>` checks the stage being left; it does not create acceptance. See [tool usage](../scripts/README.md) for the supported syntax and fields.

Quick Spec's combined task review binds all three specification documents. Standard reviews bind the relevant phase artifacts. The task-plan snapshot excludes routine checkbox, activity, and evidence updates; substantive changes to scope, acceptance, dependencies, or checks still invalidate it. Use [Reconcile](../workflows/reconcile.md) to assess the impact, revisit the affected review, and refresh relevant evidence. Never edit a completion claim simply to bypass a failed prerequisite.

## Turn the result into useful tasks

Stop the interview for the current scope when the goal, critical behavior, constraints, preserved obligations, and verification are sufficiently clear. Uncertainty may remain as an explicit safe assumption with a validation task; a consequential unresolved product or authority decision continues to block dependent work.

Create tasks with independently reviewable outcomes, explicit dependencies, requirement/design links, acceptance conditions, and evidence obligations. Include integration, migration, operations, and verification work only where the scope requires them. Required checks cannot be deferred merely to mark implementation complete. Select test techniques to match the claim; property-based testing is useful in some cases, not mandatory for every change.

The first implementation action should follow directly from the task graph. Continue if authorized. If the task is planning only, finish with the reviewable specification, task plan, remaining decisions, and exact next step. If required cloud evidence is unavailable, report that obligation as pending while completing the authorized local work.
