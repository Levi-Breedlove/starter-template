# Repository map

Open the application at its root. The root instructions and the installed manifest identify its canonical documents. A template-created repository starts with the following layout. An adopted brownfield project can map established documents and use its own application, infrastructure and delivery directories.

| Location | Purpose |
| --- | --- |
| `AGENTS.md` | Project instructions and conversational shortcuts |
| `project/` | Product brief, project requirements, technology choices, repository structure, system architecture and adoption assessment |
| `specs/<work-id>/` | Scoped requirements or defect contract, design, tasks, analysis and correctness properties |
| `docs/decisions/`, `docs/diagrams/` | Consequential decisions and supporting diagrams |
| `src/`, `tests/`, `infrastructure/` | Application implementation, tests and infrastructure as code |
| `security/`, `costs/`, `runbooks/` | Project-specific access controls, estimates, operations and recovery procedures |
| `delivery/`, `evidence/` | Current handoff, environment capability observations, release records and verified results |
| `.aws-workflow/` | Installed CLI, guidance, workflows, templates and manifest |
| `.codex/workflow.json` | Optional pointer created when work is first selected |
| `.workflow-state/` | Ignored local state for optional native task execution |

For an in-place template project, begin with `start`. The [adoption guide](reference/bootstrap.md) explains how to install the same workflow into an existing project and map its own records. The [workflow CLI reference](reference/workflow-tooling.md) describes structured work and verification.

In the maintenance checkout, the reusable package sources are at the repository root. The source README and the maintenance handoff identify the current framework work.
