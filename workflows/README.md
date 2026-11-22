# Workflow contracts

These Markdown procedures give Codex usable instructions for consultation, specification, implementation, review, and release. Start with the repository's `AGENTS.md` and ask Codex to follow the matching contract. They are **not executable recipes, installed skills, native Codex commands, or active automation**. Event-driven integrations must be implemented and verified separately.

The procedures are independently designed from the official Kiro lifecycle. They do not depend on private planning skills, agency agents, or a previous application's architecture.

## Choose the procedure

| Procedure | Use it when | Main result |
| --- | --- | --- |
| [Brownfield intake](brownfield.md) | Adopt these practices in an existing application or infrastructure repository. | An evidence-based adoption report that preserves existing ownership and behavior. |
| [Consult](consult.md) | Scope, constraints, feasibility, or architecture needs definition. | A grounded recommendation and selected work route. |
| [Feature](feature.md) | New or changed functionality needs implementation. | Requirements/design/tasks and verified changes, using the appropriate route. |
| [Bugfix](bugfix.md) | A defect requires diagnosis and preservation of existing behavior. | Reproduction, scoped correction, and regression evidence. |
| [Reconcile](reconcile.md) | Specifications, code, tasks, or evidence have diverged. | An explained, consistent current state and next action. |
| [Review](review.md) | A concrete candidate needs scrutiny before integration or release. | Findings tied to the exact reviewed revision. |
| [Release](release.md) | A verified candidate is being prepared for or deployed to AWS. | Separate readiness, deployment, and operational verification records. |
| [Incident](incident.md) | A running service has an operational problem. | Authorized mitigation, recovery evidence, and follow-up work. |

Feature work supports Requirements-First, Design-First, Quick Spec, and a lighter Plan-led route. Bugfix work has its own contract. A trivial, understood edit can use proportionate review and verification without creating a full feature specification. See [the capability reference](../docs/reference/kiro-capabilities.md) for the actual Kiro behavior and surface limits behind these choices.

**Greenfield:** begin with [Consult](consult.md), establish users and constraints, select the specification route, then implement the first accepted scope. **Brownfield:** begin with [Brownfield intake](brownfield.md), establish the existing baseline, and change only the accepted scope. Neither route requires moving an existing repository into this skeleton's layout.

## Artifact ownership

| Artifact | Canonical location |
| --- | --- |
| Project purpose, scope, constraints | `project/brief.md` |
| Existing-system baseline and adoption decisions | `project/adoption-report.md` |
| Work requirements or defect analysis | `specs/<work-id>/requirements.md` or `bugfix.md` |
| Work design and executable task breakdown | `specs/<work-id>/design.md` and `tasks.md` |
| Task checkboxes and acceptance traceability | The relevant `tasks.md` |
| Architecture decisions | `docs/decisions/` |
| Cost assumptions and estimates | `costs/` |
| Security constraints and review material | `security/` |
| Operating and recovery procedures | `runbooks/` |
| Lightweight verification records and external CI links | `evidence/<work-id>/` |
| Release record | `delivery/releases/<release-id>.md` |
| Current continuation point | `delivery/current-handoff.md` |

For this scaffold's own implementation, the canonical backlog is `specs/0001-workflow-foundation/tasks.md`. `docs/implementation-plan.md` provides a roadmap and links to that backlog; it does not own another checklist. Application work belongs in separate work specifications.

## Rules shared by every procedure

1. Read the relevant project instructions and current handoff. Preserve accepted architecture and existing work. Inspect the current branch, revision, and uncommitted changes before editing.
2. State what is established, assumed, proposed, and still unverified. A document or checked box is not a runtime result.
3. Use the existing official AWS Core and AWS Data Analytics plugins for relevant AWS guidance when skill use is allowed. Discover skills on demand and retrieve exact returned identifiers. For documentation-only research or a skill opt-out, use current official documentation directly. Public consultation needs no account access. These documents grant no AWS or spending authority.
4. Keep task dependencies visible. Parallel work needs separable scope and an integration owner; do not have multiple agents edit the same artifact without coordination.
5. Record verification against the requirement version, candidate revision, environment, check, and result. Changed inputs invalidate affected evidence until reassessed and, where needed, rerun.
6. Call a review independent only when a fresh reviewer actually inspected the candidate without authoring it. Report self-review or reused context honestly.
7. Continue within existing authorization. Ask only for a material unresolved decision, missing authority, or access needed to proceed. State the exact blocker and smallest next action; avoid repeated approvals for already authorized work.
8. Update the current handoff when work pauses or ownership changes. Include completed work, remaining checks, relevant evidence, blocker, and next step. Preserve history through version control rather than competing current-state files.

## Completion means evidence

Each contract names its own completion evidence. If a check cannot run, record the limitation and leave its claim unverified. Required acceptance checks cannot become optional merely because Kiro offers optional property-based tests or a runner can skip tasks. A release can be ready without having been deployed, and a deployment can complete without proving that the user-facing service works.

## What works as instructions, and what needs an implementation

| Behavior | Current scaffold mechanism | Automation status |
| --- | --- | --- |
| Select a work route and follow its phases | Codex reads the relevant contract and project context. | Usable as repository instructions. |
| Maintain requirements, design, tasks, and evidence | Codex edits the canonical files and reports the resulting diff. | Usable as repository instructions; no automatic synchronization engine is claimed. |
| Reconcile changed specs or resume work | Codex follows the reconciliation contract and current handoff. | Explicit procedure. |
| Run independent tasks concurrently | A capable execution environment may delegate separable tasks within authorization. | No scheduler is supplied by these Markdown files. |
| Trigger hooks, enforce CI gates, display a native spec UI | Requires supported product configuration and tested integration. | Future implementation; consult the roadmap and capability reference. |
