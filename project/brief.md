# Project brief: Codex AWS Consulting and Delivery Bootstrap

**Current use:** Framework maintenance.  
**Owner:** Repository owner.  
**Scope basis:** The user's request for a complete, independent AWS consulting/specification/delivery template, with adaptive interviewing, greenfield and brownfield support, official AWS tooling, executable workflow support and neutral repository content.

## Desired outcome

A developer can give Codex a rough idea or existing project. Codex leads the consultation, reuses known answers, recommends technical choices from requirements, creates a coherent design and task plan, implements authorized work and reports meaningful verification. Saved context should support continuation without repeated discovery.

## Confirmed constraints

| Topic | Established decision |
| --- | --- |
| Agent | Codex; guided consultation is the default. |
| Questions | Ask only consequential gaps, at most three per turn; save answers as work develops. |
| AWS | Existing official AWS Core and AWS Data Analytics identities; no duplicate/private replacement installation. |
| Research | Current official sources; independent of personal skills. |
| Adoption | Greenfield and brownfield; preserve existing architecture, tools, files and delivery authority. |
| Implementation | Deterministic state/checks in local code; model judgment in concise instructions and reusable procedures. |
| Content | Standalone neutral workflow; no third-party workflow product names or domains. |
| Authority | Repository work and offline verification authorized; no AWS account/resource access or paid unattended service authorized. |

## Current work and remaining choices

The [consultant workflow specification](../specs/0002-consultant-workflow/requirements.md) owns the current implementation slice. Python is the local tool implementation, not a choice of application runtime. No application stack, region, IaC framework, pipeline, budget or deployment target is selected by this bootstrap.

Real-client behavior, actual hook loading, public toolkit availability on an adopter's surface, and cloud deployment need their own observed trials. No comparative model/product benchmark has been run. Future controller language and execution interface should follow a measured need.

## Continuation

[Current handoff](../delivery/current-handoff.md) · [Current tasks](../specs/0002-consultant-workflow/tasks.md) · [Historical foundation](../specs/0001-workflow-foundation/tasks.md)
