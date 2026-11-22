# Review: <review ID and work ID>

**Review type:** <requirements / design / implementation / final acceptance / release readiness>
**Reviewer:** <identity and whether independent of the author>
**Reviewed source:** <commit, or base revision plus patch identity>
**Reviewed contract and configuration:** <exact specification revision and relevant input/config identities>
**Result:** Not reviewed / changes required / accepted for stated scope.

## Review scope

- Required behavior and constraints: <contract IDs>.
- Material reviewed: <files, diff, design, checks, and evidence>.
- Exclusions and unavailable evidence: <limits>.

For final acceptance, return to the original required outcomes. Following an implementation plan alone does not establish that those outcomes were achieved.

## Findings

| Finding | Severity and consequence | Location or contract | Required resolution | Disposition and evidence |
| --- | --- | --- | --- | --- |
| <ID and concrete issue> | <impact> | <reference> | <fix or explicit decision> | Open |

Record “no findings within scope” only after the review occurs. Distinguish verified defects from questions and recommendations.

## Coverage and decision

- Acceptance checks assessed: <CHK IDs and evidence references>.
- Security, failure, concurrency, cost, and recovery concerns: <applicable findings>.
- Deferred findings and owner decisions: <references>.
- Result and rationale: <actual assessment>.
- Conditions before next stage: <specific unresolved obligations>.

Review acceptance applies to this source and scope. If subsequent changes affect the reviewed behavior or evidence, reassess only that coverage and record the new reviewed identity. Technical review does not grant deployment authority or automatically close a broader owner acceptance gate.
