# Repository map

This repository is the reusable bootstrap's source. Application adoption installs selected reusable files under `.aws-workflow/` and supplies a manifest mapping to actual project records. It does not copy the bootstrap's own active work.

| Source path | Responsibility | Adoption |
| --- | --- | --- |
| `AGENTS.md` | Consultant entry, route selection, authority and tool use | Installer appends a smaller mapped instruction block to existing instructions. |
| `workflows/` | Consultation, features, bugfixes, adoption, reconciliation, review, release and incidents | Reusable guidance. |
| `guide/` | Start, AWS boundaries, first feature, release, adoption and interview examples | Reusable guidance. |
| `templates/` | Original planning, review, release and handoff formats; machine work template | Instantiate only relevant records. |
| `workflow_engine/` | Versioned work parsing, context, phase gates and evidence validation | Installed Python package. |
| `scripts/workflow.py` | CLI entry point | Installed under the reusable layer. |
| `scripts/bootstrap.py` | Safe source-to-application installation | Run from the bootstrap source. |
| `scripts/codex_hooks.py` | Read-only lifecycle handler | Code supplied; activation remains optional. |
| `.codex/hooks.json` | Native definitions for this source checkout | Not copied or trusted by installation. |
| `.codex/workflow.json` | Active work selection | Never copied; created explicitly for application work. |
| `project/` and `delivery/` | This bootstrap's context and handoff | Excluded; map existing app records or create fresh records. |
| `specs/0001-workflow-foundation/` | Historical delivery and broader automation backlog | Excluded from application active work. |
| `specs/0002-consultant-workflow/` | Current executable consultant workflow slice | Excluded from application active work. |
| `docs/reference/` | Actual contracts, AWS boundaries and official sources | Selected reusable references. |
| `docs/workflow-architecture.md` | Code/model/delivery responsibilities | Design reference. |
| `docs/adapter-contracts.md` | Further execution integration boundaries | Future design reference. |
| `docs/implementation-plan.md` | Framework evolution priorities | Framework maintenance only. |
| `examples/` | Fictional consultation and traceability demonstrations | Examples, never application evidence. |
| `runbooks/`, `costs/`, `security/`, `infrastructure/` | Delivery responsibilities and templates | Preserve the application's existing controls. |
| `tests/` and `scripts/check_repository.py` | Offline implementation fixtures and bootstrap file-link checks | Source maintenance; not adopter application tests. |
| `evidence/` | Historical and current framework observations | Excluded from app evidence. |
| `evaluations/` | Future model-behavior evaluation protocol | Evaluation reference. |

For each application work item, canonical requirements or bugfix, design and tasks live in the declared work paths. Evidence points to actual observations and input identities. A handoff references that state instead of maintaining a second checklist. See [workflow tooling](reference/workflow-tooling.md) and [adoption mappings](reference/bootstrap.md) for exact resolution behavior.
