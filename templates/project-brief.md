# Project brief: <project name>

**State:** Draft; this template does not establish a decision or operational authorization.
**Owner:** <owner>
**Entry mode:** <greenfield or brownfield>
**Context baseline:** <repository revision and inspected sources, or new project>

Use this brief for project-wide facts and decisions. Put work-specific answers in the corresponding specification and link them here only when useful. For brownfield work, begin with the existing repository and [assessment template](brownfield-assessment.md). Correct relative links when copying a template to its project location.

## Purpose and first outcome

- Problem and affected users: <actual need>.
- Observable success: <what a user can do and what evidence demonstrates it>.
- First delivery: <smallest independently useful scope>.
- Exclusions and deferred scope: <work outside this delivery and why>.

## Established context

| Topic | Established fact or accepted constraint | Source / decision reference | Material unknown |
| --- | --- | --- | --- |
| Existing system and architecture | <new project or inspected design> | <evidence> | <unknown or none> |
| Application, IaC, and delivery tools | <existing or selected tools; undecided if new> | <evidence> | <unknown or none> |
| Data and compatibility | <data owners, behavior and contracts to preserve> | <evidence> | <unknown or none> |
| Reliability, security, and operations | <established outcomes and constraints> | <evidence> | <unknown or none> |
| Costs and environment lifetime | <accepted limits and planning assumptions> | <cost record> | <unknown or none> |

These topics guide investigation; they are not a questionnaire to send to the user. Read existing evidence first. Remove irrelevant rows and add only what the project needs.

## Engineering recommendations and assumptions

| ID | Implication or recommendation | Basis and rationale | Status / consequence if wrong |
| --- | --- | --- | --- |
| <ID> | <derived obligation, proposed default, or estimated quantity> | <requirement, evidence, official source, and meaningful tradeoff> | <derived / proposed / assumed / selected; validation needed> |

Derive technical decisions from requirements and current official guidance. Preserve accepted choices. A recommendation does not become a user decision simply because it appears here. Keep traffic, regional pricing, and service assumptions explicit in a cost estimate; an estimate is not a spending authorization.

## Consultation record

| Question / decision ID | Material gap and consequence | Answer, deferral, or proposed default | Source and status | Affected outcome / superseded record |
| --- | --- | --- | --- | --- |
| Q-001 | <only an actual unresolved decision> | <actual answer or unresolved> | <conversation/decision reference; answered, deferred, or unresolved> | <work/requirement/decision IDs; previous answer if changed> |

Ask one to three consequential questions at a time after inspecting what is known. Save the answer and update the draft before the next round. Skip questions already answered, inferable engineering decisions, and later-scope issues. Retain superseded decisions as history without treating them as current. Do not store credentials or sensitive transcripts.

## Authorities and operating scope

- Requirements and design: <canonical project locations>.
- Task completion: <existing authority; otherwise specs/<work-id>/tasks.md>.
- Tracker projection, if any: <tracker and synchronization responsibility>.
- Product decisions and architecture exceptions: <owner or actual delegation reference>.
- Implementation scope: <actual request/authorization and boundaries; otherwise planning only>.
- Account/environment operations: <actual authorization, target, limits, and exclusions; otherwise not authorized>.
- Release and operational acceptance: <owner and existing controls>.

Preserve authorization already granted within its scope. Product acceptance, technical readiness, implementation permission, and deployment permission are separate facts. Record each only when established; do not create a new approval requirement for every document.

## First work item and continuation

- Work ID / route: <ID and Requirements-First, Design-First, Quick Spec, Bugfix, or Plan-led; reason>.
- Contract and design: <links to current artifacts>.
- Verification: <required local evidence and any later authorized AWS obligations>.
- Material blockers: <decision or evidence, consequence, owner, and smallest next action>.
- Review outcome: <what was actually reviewed, reviewer, revision, findings, outcome, and authority>.
- Next action: <interview question, review, or next eligible task>.

Keep the current continuation point in the mapped project handoff. Link the canonical task record rather than maintaining a second backlog in this brief.
