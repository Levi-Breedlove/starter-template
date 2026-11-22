# Repository map and artifact lifecycle

This table describes delivered locations and their responsibilities. It is the layout reference, not an independent status tracker. Follow the [canonical foundation tasks](../specs/0001-workflow-foundation/tasks.md) for automation implementation status.

## Reusable operating layer

| Path | Purpose | Adoption treatment |
| --- | --- | --- |
| `AGENTS.md` | Concise Codex context and procedure router. | Adapt to the project; merge with existing instructions. |
| `guide/` | Start, AWS access, first feature, maintenance, brownfield guides. | Keep relevant guides or link to a maintained bootstrap copy. |
| `workflows/` | Eight explicit procedure contracts. | Reuse and map to the project's actual paths. |
| `templates/` | Original document templates. | Instantiate selectively; correct copied links. |
| `project/brief.md` | Current project's goal, constraints, choices, authority. | Replace framework context with application facts. |
| `project/adoption-report.md` | Existing-system baseline and uncertainties. | Required for meaningful brownfield adoption; greenfield may record not applicable. |
| `specs/<work-id>/` | Requirements or bugfix analysis, design, tasks and verification matrix. | Create a focused folder per useful change. |
| `docs/decisions/` | Consequential architecture/workflow decisions. | Preserve existing decision records and numbering. |
| `evidence/<work-id>/` | Sanitized check observations and CI links. | Identify candidate and environment; never store secrets/raw account dumps. |
| `delivery/current-handoff.md` | Current continuation summary. | Update as work pauses or changes ownership. |
| `delivery/releases/<release-id>.md` | Concrete release and operational result. | Instantiate only for actual release work. |
| `costs/` | Cost assumptions, estimates, ongoing/retained costs. | Fill from the chosen design and current pricing evidence. |
| `security/` | Security constraints and evidence responsibilities. | Link to the established project controls. |
| `runbooks/` | Deploy, rollback, incident, teardown contracts. | Turn into executable project-specific procedures before use. |
| `infrastructure/` | Guidance for IaC ownership and project choice. | Keep an existing infrastructure layout; no stack is supplied. |

## Reference and maintenance layer

| Path | Purpose | Adoption treatment |
| --- | --- | --- |
| `docs/research/` | Documentation and demonstration synthesis, exact evidence access levels. | Optional reference; do not load it all into every agent turn. |
| `docs/reference/` | Kiro capability map and official source ledger. | Consult when behavior or compatibility matters. |
| `docs/workflow-architecture.md` | Complete proposed behavioral design. | Reference for extending the bootstrap. |
| `docs/adapter-contracts.md` | Native integration, events, persistence, recovery contracts. | Planned implementation specification. |
| `docs/implementation-plan.md` | Phased roadmap. | Framework maintenance reference. |
| `specs/0001-workflow-foundation/` | Framework's requirements/design/canonical backlog. | Archive or omit from active application work. |
| `examples/booking-retries/` | Fictional traceability example. | Learning material; no application or test result. |
| `evaluations/` | Proposed parity/improvement measurements. | Framework evaluation reference; scenarios are unexecuted. |
| `scripts/check_repository.py` | Offline Markdown file-link and core-structure checker. | Adjust required path set if deliberately adopting another layout. |
| `tests/test_repository_checks.py` | Fixture tests of the checker. | Keep when maintaining the checker. |
| `.github/pull_request_template.md` | Prompts for problem, behavior, evidence, and limitations. | Merge with existing PR template. |
| `.codex/README.md` | Native adapter/configuration plan. | No active configuration is installed by this file. |
| `.agents/skills/README.md` | Optional future packaging boundary. | No skill is loaded or installed from this README. |
| `src/README.md` | Workload code placement guidance. | Application source belongs in its chosen layout. |

There is no active CI workflow, credential file, IaC deployment, model-runner daemon, or scheduled job in this skeleton. Empty future directories are described here rather than populated with misleading executables.

## Planned implementation locations

| Future location | Responsibility | Trigger for adding it |
| --- | --- | --- |
| `scripts/validate_work.py` | Deterministic task IDs, dependencies, traceability, evidence checks. | Implement and test the corresponding foundation task. |
| `.codex/hooks.json` or one supported inline configuration | Reviewed lifecycle hooks. | Client compatibility and hook behavior verified. |
| Supported Codex custom-agent configuration | Bounded investigator, designer, implementer, reviewer roles. | Actual schema and isolation tested. |
| `workflow_engine/` | Optional scheduler, worker adapter, run/evidence/event storage. | Durable orchestration selected and implemented. |
| `schemas/` | Versioned machine contracts for controller data. | Actual parser/storage implementation exists. |
| `.workflow-state/` | Ignored transient run state and event cursors. | Runtime installed and deliberately invoked. |
| Existing CI/event configuration | Required project checks and optional feedback wakeups. | Project's actual pipeline selected and authorized. |

Do not create duplicate authoritative `.kiro/specs/` files just to resemble Kiro. If interoperability is later required, define an import/export adapter with conflict detection and one declared source of truth.

## How artifacts change

Intent enters the brief and a work contract. Design references that contract. Tasks reference the requirements and design. Evidence references the candidate and check. Review examines the same candidate. A release references the verified artifact/configuration. The handoff points to the next eligible work.

On change, identify the affected edges and reopen only the outcomes no longer established. Version control preserves history; the current documents describe the current state. Detailed records should reference, not copy, shared architectural facts.

