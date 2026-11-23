# Repository map

This repository is the reusable bootstrap's source. Application adoption installs selected reusable files under `.aws-workflow/` and supplies a manifest mapping to actual project records. It does not copy the bootstrap's own active work.

| Source path | Responsibility | Adoption |
| --- | --- | --- |
| `AGENTS.md` | Consultant entry, route selection, authority and tool use | Installer appends a smaller mapped instruction block to existing instructions. |
| `workflows/` | Consultation, features, bugfixes, adoption, reconciliation, review, release and incidents | Reusable guidance. |
| `guide/` | Complete first-project quickstart, AWS boundaries, feature/release/adoption and interviews | Reusable guidance. |
| `templates/` | Original planning, review, release and handoff formats; machine work template | Instantiate only relevant records. |
| `workflow_engine/` | Work parsing, context, setup, semantic-operation records, reconciliation and bounded task execution | Installed Python package. |
| `scripts/workflow.py` | CLI entry point | Installed under the reusable layer. |
| `scripts/bootstrap.py` | Safe source-to-application installation | Run from the bootstrap source. |
| `scripts/codex_hooks.py` | Read-only lifecycle handler | Code supplied; activation remains optional. |
| `.codex/hooks.json` | Native definitions for this source checkout | Not copied or trusted by installation. |
| `.codex/workflow.json` | Active work selection | Never copied; created explicitly for application work. |
| `project/` and `delivery/` | This bootstrap's context and handoff | Excluded; map existing app records or create fresh records. |
| `specs/0001-workflow-foundation/` | Historical delivery and broader automation backlog | Excluded from application active work. |
| `specs/0002-consultant-workflow/` | Underlying executable consultant workflow contract | Excluded from application active work. |
| `specs/0003-efficient-context/` | Focused context and measurable efficiency slice | Excluded from application active work. |
| `specs/0004-developer-workflow/` | Complete developer workflow, execution plan and acceptance boundaries | Excluded from application active work. |
| `docs/reference/` | Actual contracts, AWS boundaries and official sources | Selected reusable references. |
| `docs/workflow-architecture.md` | Code/model/delivery responsibilities | Design reference. |
| `docs/adapter-contracts.md` | Implemented interfaces and further integration boundaries | Architecture reference. |
| `docs/implementation-plan.md` | Framework evolution priorities | Framework maintenance only. |
| `examples/` | Fictional consultation and traceability demonstrations | Examples, never application evidence. |
| `runbooks/`, `costs/`, `security/`, `infrastructure/` | Delivery responsibilities and templates | Preserve the application's existing controls. |
| `tests/` and `scripts/check_repository.py` | Offline fixtures, real local Git/process tests with fake models, and file-link checks | Source maintenance; not adopter application tests. |
| `evidence/` | Historical and current framework observations | Excluded from app evidence. |
| `evaluations/` | Fixed behavioral pilot plan, frozen inputs and measurement protocol | Evaluation reference; no automatic execution. |

For each application work item, canonical requirements or bugfix, design and tasks live in the declared work paths. `analysis.json` and `properties.json` retain sourced review history. `execution.json` defines optional trusted execution policy. Ignored `.workflow-state/` retains run worktrees/counters; sanitized acceptance evidence remains versioned. A handoff references those records without duplicating task completion. See [workflow tooling](reference/workflow-tooling.md) and [adoption mappings](reference/bootstrap.md).
