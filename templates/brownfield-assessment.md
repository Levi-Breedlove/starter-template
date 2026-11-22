# Brownfield assessment: <existing project>

**State:** Draft assessment; no infrastructure changes authorized by this document.
**Assessment scope:** <requested change, repository paths, and supplied evidence>
**Source revision:** <branch/commit and known uncommitted work>
**Existing owner and instructions:** <project owner and applicable repository guidance>

## 1. Map the existing system from available evidence

Read the repository, infrastructure definitions, build manifests, tests, diagrams, decisions, runbooks, and supplied deployment records first. Link existing records in place. Do not copy or move the codebase to fit this skeleton.

| Area | Existing location or evidence | What it establishes | State and remaining uncertainty |
| --- | --- | --- | --- |
| Application and interfaces | <paths> | <behavior visible in source> | <observed source / reported / intended / unknown> |
| Infrastructure and state ownership | <IaC paths and existing management model> | <declared configuration and owner> | <deployed state not inferred> |
| Delivery and environments | <pipeline definitions and supplied result records> | <configured process or particular historical execution> | <current operation unknown unless evidenced> |
| Data and migration history | <schema/migrations/runbooks> | <contracts and recovery assumptions> | <unknowns> |
| Security and network boundaries | <policies/configuration/design> | <intended controls and known tests> | <enforcement proof still needed> |
| Costs and resource lifetime | <estimates or supplied records> | <documented assumptions or measured period> | <current cost unknown unless evidenced> |

Use **observed source**, **observed execution**, **reported**, **accepted target**, **proposed**, and **unknown** accurately. An IaC file describes intent; it does not alone establish the live resource configuration or absence of drift.

## 2. Preservation contract

| ID | Existing behavior or constraint to preserve | Baseline evidence | Check needed for this change |
| --- | --- | --- | --- |
| KEEP-001 | <user-visible behavior, interface, data invariant, or security boundary> | <existing test/result, or not supplied> | <targeted verification> |

Name compatibility requirements and accepted tools. Mark unavailable baseline evidence honestly. The absence of a test does not authorize changing the existing contract.

## 3. Ownership and migration risks

- Existing infrastructure owner and source of truth: <IaC stack/state/manual ownership; unknown where unproven>.
- Resources or data that must not be recreated: <references and reasons>.
- Import, adoption, or state migration implications: <risk, planned analysis, and required evidence>.
- Schema and API compatibility: <consumers and migration order>.
- Rollback or forward recovery: <existing procedure and gaps>.
- Concurrent writers and active deployments: <known ownership and safe integration point>.

Do not run imports, apply state changes, replace resources, or move ownership as part of assessment. Any necessary live inspection must have an explicit scope and authorization; a documentation request alone does not grant account access.

## 4. Remaining AWS proof

| Question | Why repository evidence is insufficient | Minimum authorized observation needed | Affected decision |
| --- | --- | --- | --- |
| <live configuration, drift, permission, integration, or cost question> | <gap> | <bounded read or test; not executed> | <dependent work> |

Use the official AWS Agent Toolkit guidance route to research the question without account access first. Describe operational proof separately and obtain it only within the project's actual authorization and limits.

## 5. Smallest useful adoption

- Selected work route: <Design-First, Requirements-First, Bugfix, Plan, or direct task, with reason>.
- Reused project records: <canonical links>.
- Missing records to add: <only those necessary for the requested outcome>.
- Affected requirements, design, tasks, tests, costs, and runbooks: <change map>.
- First bounded outcome: <result and completion evidence>.
- Deferred repository reorganization: <none, or an explicit separate proposal>.

This assessment supports specification and planning. It does not claim the system is production-ready or convert a reported target into an observed deployment.

Use the [brownfield procedure](../workflows/brownfield.md) to reconcile this assessment with the existing project's canonical documents and delivery ownership.
