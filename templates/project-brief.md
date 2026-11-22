# Project brief: <project name>

**State:** Draft; decisions and operational authorization are not established by this template.
**Owner:** <owner>
**Reviewed revision:** <revision or not reviewed>
**Entry mode:** <greenfield or brownfield>

For brownfield work, begin with the existing repository and [brownfield assessment](brownfield-assessment.md); preserve accepted choices and map only the affected change. For greenfield work, record architecture and delivery choices as unresolved until selected. Correct this template link when copying the record to its target location.

## Purpose and outcome

- Problem and affected users: <describe the actual need>.
- Observable success: <what the user can do, and how success is measured>.
- Scope: <included capabilities>.
- Exclusions: <work deliberately outside this project or release>.

## Current facts and constraints

| Topic | Established fact or accepted constraint | Evidence or decision reference | Unknowns |
| --- | --- | --- | --- |
| Existing system and architecture | <new project or established design> | <reference> | <unknowns> |
| Application and infrastructure tools | <selected tools or undecided> | <reference> | <unknowns> |
| Delivery pipeline | <existing selection or undecided> | <reference> | <unknowns> |
| Data, security, and reliability | <requirements> | <reference> | <unknowns> |
| Costs and environment lifetime | <assumptions and limits, not invented amounts> | <cost record> | <unknowns> |

## Authorities and workflow

- Technical requirements and design: <canonical locations>.
- Task completion: `specs/<work-id>/tasks.md`, unless an existing project declares another authority.
- Priorities and tracker projection: <tracker and synchronization responsibility, or none>.
- Decisions: <who decides consequential scope, architecture, access, and cost changes>.
- Release and operational acceptance: <owner and existing controls>.
- Current execution scope: <actual authorization reference, environments, limits, and exclusions; otherwise planning only>.

Preserve authorization already granted within its scope. Raise a new decision only when work exceeds that scope or a consequential assumption changes.

## Proposed first delivery

- Work type and reason: <feature, design-constrained work, defect, investigation, or small edit>.
- First independently useful result: <outcome>.
- Verification approach: <local checks and any later authorized AWS proof>.
- Open decisions that block this result: <decision, consequence, owner>.
- Deferred work: <explicit exclusions and reason>.

## Consultation outcome

Record the recommendation, alternatives that materially differ, assumptions, and the owner's actual decision. An accepted design, permission to implement, and permission to deploy are distinct facts; record each only when established.
