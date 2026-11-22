# Consulting and delivery contract

This repository supplies a conversational procedure plus deterministic local tooling. The procedure guides judgment; the tool checks records and allowed transitions. Follow the actual project's authority, scope and review policy.

## Entry and phase routes

| Route | Entry | Ordered work | Review behavior |
| --- | --- | --- | --- |
| Requirements-first | Desired outcome or new behavior | Consultation → requirements → design → tasks → implementation → verification | Review requirements before design and design before tasks. |
| Design-first | Technical proposal that needs behavioral definition | Consultation → design → requirements → tasks → implementation → verification | Review design first, then requirements; reconcile both before tasks. |
| Quick | Bounded change with low uncertainty | Necessary questions → connected requirements/design/tasks → implementation → verification | No separate document approval pauses; retain actual project gates. |
| Bugfix | Fault or incident follow-up | Reproduction/current behavior → expected and preserved behavior → change design → tasks → regression checks | Review the fault contract and material change at the depth the project requires. |
| Plan | Consultation or planning request | Interview and planning artifacts at the requested depth | Stop at the requested planning outcome; a plan does not authorize execution. |
| Direct | Small, understood edit | Inspect → edit → proportionate verification | No unnecessary specification ceremony. |

The exact machine phase names, transition rules and CLI arguments are defined in [the tooling reference](workflow-tooling.md). Route labels are implementation details; Codex recommends the appropriate path from the user's intent.

## Interview loop

Read existing facts and decisions first. Identify the next decision that materially changes the requirements or architecture. Derive technical implications and research current guidance before asking. Ask one to three short questions with a reason and a useful recommendation; save each answer in the canonical brief or contract. Repeat only while consequential uncertainty remains.

For greenfield work, explore user outcomes, roles, journeys, data, external systems, scale, costs, security, reliability and operations as relevant. For brownfield work, start with existing behavior, ownership, constraints and preserved interfaces. Do not ask every topic mechanically or force the user to choose service names. See the [interview guide](../../guide/06-consultation-interview.md).

## Artifacts and checks

| Artifact | Authority | Code-assisted check |
| --- | --- | --- |
| Brief and current contract | Facts, answers, assumptions and accepted scope | Referenced source exists; answered questions stay separate from open ones. |
| Requirements / bugfix | Observable behavior and preservation obligations | Stable IDs resolve in task/check references. |
| Design | Implementation choices, interfaces, costs, security and operations | Revision-bound review freshness. |
| Tasks | Prerequisites and completion state | Duplicate IDs, dangling dependencies, cycles, check coverage and false completion. |
| `work.json` | Indexed context, phase and references to reviews/evidence | Schema, safe paths and declared input hashes. |
| Review / evidence | Actual decision or observed result and its scope | Referenced record exists; declared file identities still match. |
| Handoff | Where to resume | Active work can be selected and inspected again. |

Passing a structural check does not prove semantic completeness or truthful observations. Codex must inspect the evidence and actual candidate. Native hooks add context and reminders; they do not enforce IAM or run an autonomous delivery service.

## Handling change

If a requirement, implementation input or decision changes, identify the affected tasks and reviews. Preserve historical results but stop presenting stale evidence as current. Reconcile the contract, rerun affected checks, and obtain a new review only when the changed decision requires it. Continue within already granted authority; do not manufacture repeated approval gates.
