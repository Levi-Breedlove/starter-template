# Consult

## Trigger

Use this procedure for a new project, a substantial change, or uncertainty that affects the next delivery. Codex leads an adaptive interview and turns its findings into requirements, a reasoned design, and actionable tasks. The user supplies product intent and decisions only they can make; Codex does the engineering investigation.

For greenfield work, establish product and operating constraints before committing to services. For brownfield work, begin with [Brownfield intake](brownfield.md) and preserve the accepted architecture. Public consultation does not require AWS credentials.

## Inputs

- The user's request, supplied material, and decisions already made in this conversation.
- The project brief, relevant specifications and decisions, and current handoff; use the adopted project's mapped paths when they differ from this bootstrap.
- Actual repository structure, implementation, tests, and the adoption report where applicable.
- Existing implementation and access authorization, with any cost or environment limits.

## Stages

### 1. Read before interviewing

Inspect the available context and relevant code. Classify each material point as an established fact, an engineering implication, a proposed default, or a genuine unresolved decision. Cite its local evidence or decision source. Reuse known answers; ask again only when evidence conflicts or a new circumstance changes their consequence.

Begin with a brief account of the intended outcome, constraints already understood, and the next uncertainty to resolve. A very vague request may need a product question before deeper research. A well-specified request may need no interview questions.

### 2. Investigate and lead with a recommendation

Derive technical obligations from the behavior: consistency, authorization, retries, failure handling, migration, recovery, and verification where relevant. Use the existing official AWS Core/Data Analytics route described in [AWS guidance and access](../guide/02-aws-guidance-and-access.md). Honor a documentation-only or no-skills instruction by using official documentation directly. Research is public unless account inspection has separately been authorized.

Recommend an approach and explain why it fits the known requirements. Compare alternatives only when they materially change cost, operations, delivery, or risk. Preserve the established stack. Separate current-source facts, assumptions used for estimates, recommendations, and actual decisions. Never invent an AWS bill, service quota, live configuration, or accepted budget.

### 3. Interview in small adaptive rounds

Ask **one to three material questions per round**, selected from the remaining uncertainty. Explain the consequence of each and offer a reasoned recommendation when possible. Accept free-form answers, corrections, and a justified deferral. Do not send a fixed questionnaire or ask the user to choose AWS services that Codex can evaluate from the requirements.

Questions usually concern missing user journeys, business rules, sensitive data, compatibility promises, delivery priorities, recovery expectations, or spending/access authority. These are areas to investigate, not mandatory questions. Inspect existing answers and research technical facts first. Workload quantities may begin as labeled planning assumptions when safe to revise; a new spending limit or business policy cannot be silently assumed.

After each answer, update the authoritative brief or work contract, refine the current draft, and identify whether the answer creates a new material dependency. Continue only with the questions still needed. Stop interviewing when the next scope can be specified and verified; defer questions belonging to a later delivery.

### 4. Persist the consultation as it develops

Keep project-wide answers in the project brief; keep feature-specific answers in `requirements.md`, and defect-specific answers in `bugfix.md`. Link to the authoritative answer instead of maintaining duplicate transcripts. Each consequential answer records the question, answer or deferral, source, affected requirement or decision, and any superseded answer. Record recommendations separately from accepted choices.

Save useful drafts even while a decision is pending. The current handoff names the unresolved question, why it matters, what can continue, and the exact next action. Do not leave the project's only durable knowledge in chat.

### 5. Build and review the connected specification

Choose the route in [Feature](feature.md) or [Bugfix](bugfix.md). Draft testable requirements with stable identifiers; analyze interactions, contradictions, ambiguous terms, boundary conditions, and assumptions. Resolve engineering findings directly where supported. Bring a product conflict back as a focused question with a proposed resolution.

Follow the route's actual review order: requirements then design; design then derived requirements; or the combined Quick Spec review after drafting all three documents. A review records what was inspected, its revision, findings, reviewer, and outcome. Existing delegated authority may cover the next transition; it never permits fabricating user acceptance. See [the interview guide](../guide/06-consultation-interview.md) for the distinction.

### 6. Generate tasks and continue within scope

Create bounded tasks with requirements, dependencies, acceptance checks, and evidence obligations once the route's planning conditions are satisfied. Identify the first unblocked task and which checks require a later authorized environment. Continue implementation when already authorized. A planning-only request finishes with a concrete reviewable plan and continuation point.

## Outputs

- An updated brief and work contract with decisions, assumptions, sources, and material unanswered questions.
- A selected route, connected requirements/design/tasks, and actual phase review records.
- Relevant cost, security, decision, and operating references without duplicated task authority.
- A current handoff that resumes the interview or the next eligible task.

## Completion evidence

The scope answers the user's objective. Required behavior is observable; the design addresses it; the task graph and checks cover it. Each material unresolved decision has an owner and consequence. Actual acceptance and authorization have sources. Drafted documents and public research do not establish implementation, deployment, or live AWS verification.

## Continue, pause, and resume

Continue useful research, drafting, and authorized work while unrelated questions remain open. Pause dependent work for a consequential unresolved decision, a real approval control, or missing authority/access. Ask only for the smallest missing decision and explain why it is necessary. Resume from saved answers, drafts, current code, and evidence; use [Reconcile](reconcile.md) if they have changed. Do not restart the interview or request the same authorization again.
