# Adopt the workflow in an existing project

Start from the system that exists. The initial adoption should improve one real change without disrupting working code, documentation, delivery controls, or infrastructure ownership.

## Repository-first baseline

Follow [Brownfield intake](../workflows/brownfield.md) and use the [assessment template](../templates/brownfield-assessment.md). Inspect the current instructions, source structure, dependencies, tests, CI, IaC, runbooks, architecture decisions, and task authority. Record actual file and revision evidence, established decisions, and unresolved contradictions.

Separate three kinds of knowledge: what the repository declares, what authorized environment inspection later observes, and what remains an assumption. Source code alone does not prove which version is deployed. An IaC declaration alone does not prove live resource ownership or configuration.

## Adopt through a small reviewed overlay

| Existing situation | Adoption action |
| --- | --- |
| Root `AGENTS.md` already exists | Propose a focused patch that references the selected procedures. Preserve its accepted rules and authority. |
| Existing architecture and delivery documents | Reference them from the brief and adoption report; avoid duplicating their contents. |
| Existing specification or tracker authority | Map stable identifiers and evidence to it. Record any deliberate authority change; do not introduce a competing backlog. |
| Existing test suite | Establish its baseline and isolate known failures before changing behavior. |
| Existing application directories | Keep their paths. The bootstrap's `src/`, `tests/`, and `infrastructure/` layout is optional. |
| Existing CDK, CloudFormation, Terraform, or other IaC | Preserve ownership and state. Plan imports, migrations, or tool changes as explicit separate work. |
| Existing CI and deployment pipeline | Add missing checks through its established process; do not replace it as a side effect of adoption. |

Copy only the workflow documents and templates that help the chosen change. If names collide, use a temporary namespace or prepare a merge diff rather than overwriting files. Update references and the repository map to the adopted locations. The bootstrap's own research and foundation backlog are optional reference material, not required application runtime files.

## Protect existing behavior

Choose one representative change. Capture its affected interfaces, compatibility obligations, data lifecycle, consumer expectations, security boundaries, and current operational assumptions. Add characterization or regression checks where needed to establish behavior that existing tests do not document. Distinguish intentional changes from preserved behavior.

For infrastructure changes, determine declared state ownership, deployment mechanism, stack boundaries, and unmanaged dependencies before considering import or replacement. Public guidance can explain import and drift limitations; actual account inspection requires its own authorized scope. See [AWS integration research](../docs/research/aws-integration.md) and [infrastructure guidance](../infrastructure/README.md).

## Verify adoption

The first adoption is successful when Codex can locate current authority, explain the existing architecture from evidence, implement the bounded change, and demonstrate both the new outcome and required preserved behavior. The repository remains usable by its existing pipeline and team. Compare before/after files and checks; the presence of more documents is not a success measure.

Record the adopted path map, known gaps, evidence, and next task in the project report and handoff. Expand scoped instructions or automation only after a repeated need becomes clear.

