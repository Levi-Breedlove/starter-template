# Requirements: Codex AWS workflow foundation

**Historical foundation scope:** The initial scaffold and broader program are described here. Current executable behavior is specified in [0002](../0002-consultant-workflow/requirements.md); use its tasks and receipt for current claims.

**Work ID:** 0001-workflow-foundation.  
**Route:** Requirements-First with public product research.  
**Scope:** Requested research and bootstrap now; explicitly planned native/runtime improvements later.  
**Decision state:** The user requested the goal and repository delivery. Future implementation choices and AWS operations are not approved by this specification's existence.

## User outcome

An AWS developer can give Codex a project or change, have it follow a guided specification and delivery lifecycle, preserve context and accepted decisions, and obtain a result supported by meaningful verification. The same foundation works for new projects and existing systems without imposing an application architecture.

## Requirements and acceptance

| ID | Requirement | Acceptance condition |
| --- | --- | --- |
| REQ-001 | Ground the design in current official Codex and AWS sources and primary workflow demonstration material. | Source ledger and research identify URLs, dates where available, inspected evidence levels, surface differences, and unresolved facts. No unviewed footage is claimed as watched. |
| REQ-002 | Distinguish instructions, supported native primitives, proposed adapters, and verified results. | Every capability status is accurate; Markdown recipes/config plans cannot be reported as active automation. |
| REQ-003 | Establish project context before proposing implementation. | Greenfield intake identifies outcome/constraints; brownfield intake cites existing code/decisions and records unknown live state. |
| REQ-004 | Support Requirements-First, Design-First, Quick Spec, bugfix, and proportionate small work. | The route can be selected from actual uncertainty/constraints without unnecessary repeated phase approvals. |
| REQ-005 | Challenge requirements and define appropriate verification. | Material ambiguities/conflicts and important invariants are addressed; critical outcomes have checks; optional PBT does not make acceptance optional. |
| REQ-006 | Connect requirements, design, tasks, dependencies, and evidence. | Stable IDs and one task authority support end-to-end traceability; missing references and cycles are detectable in the later validator. |
| REQ-007 | Execute eligible work with coordinated ownership. | Planned controller prevents dependent tasks from starting early and prevents conflicting writers; joined candidates receive relevant checks. |
| REQ-008 | Review concrete candidates and validate original outcomes. | Review records scope/candidate; independent review uses fresh nonauthor context; incomplete review is not a pass. |
| REQ-009 | Reconcile changed assumptions and invalidate affected evidence. | Requirement/source/config/input changes trigger an impact record; stale outcomes cannot complete dependent work while unaffected evidence remains scoped. |
| REQ-010 | Use the official AWS toolkit within actual availability and authorization. | No copied AWS skill collection or duplicate plugin identity; public consultation makes no account calls; later operations name scope and limits. |
| REQ-011 | Prepare releases with reproducible identities and operational proof. | Source/patch, configuration, target, checks, recovery and observed outcome are separately recorded, with applicable artifact/preview identity or justified N/A; required project gates remain; local results are not labeled cloud proof. |
| REQ-012 | Map automation to real supported events and handlers. | Native event/action compatibility is documented and tested; unsupported or untrusted hooks remain visibly inactive; duplicate/recursive events are bounded. |
| REQ-013 | Resume reliably after interruption. | Planned runner preserves completed work and counters, inspects uncertain effects, and avoids blind replay; file/session recovery is separate from AWS recovery. |
| REQ-014 | Bound automation cost and repeated work. | Concurrency, iteration, retry, time, and available usage limits are recorded and survive resume; new paid background work is not implicitly enabled. |
| REQ-015 | Integrate PR/CI feedback without stale acceptance. | Planned event adapter deduplicates feedback, ties checks to current head, stops on terminal conditions, and does not assume merge/deploy/message authority. |
| REQ-016 | Support nondestructive adoption of existing projects. | Existing instructions, architecture, paths, user edits, test baseline, IaC ownership/state, and delivery controls are preserved or explicitly changed by decision. |
| REQ-017 | Make improvements measurable. | Evaluation cases disclose baseline, versions, scope, evidence, limitations, and cost; no superiority claim precedes a comparative result. |
| REQ-018 | Deliver a usable, reviewable skeleton in the requested repository. | Core instructions, guides, templates, example, runnable offline checker, plan, and handoff exist; local checks pass and publication is read back. |

## Constraints

Use official primary technical sources. Do not use the owner's personal skills as the methodology. No AWS account access, plugin installation/update, resources, credentials, scheduled jobs, or deployed application is part of this delivery. Preserve existing operational authority and the owner's repository visibility.

Application technologies, runtime language for a future controller, budget amounts, named AWS environments, and CI provider are not prescribed. Python standard library is used only for the delivered offline checker; it does not select the application's stack.

## Verification boundary

The initial scaffold can satisfy the document/procedure portions and its actual checker tests. Runtime behavior in REQ-006–009 and REQ-012–015 requires later implementation and fault tests. AWS release behavior requires later scoped cloud evidence. The task list records these as unfinished, rather than treating a documented requirement as completed implementation.

## References

[Current sources](../../docs/reference/sources.md), [architecture](../../docs/workflow-architecture.md), [design](design.md), and [tasks](tasks.md).

