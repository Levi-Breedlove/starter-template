# Start a project with the bootstrap

The bootstrap has two entry paths. A greenfield project establishes its purpose and selects its architecture. A brownfield project starts with evidence about the existing system and the behavior that must survive. Both then use the same specification, implementation, verification, and release loop.

## 1. Choose the right use

If you are improving this bootstrap, retain its [brief](../project/brief.md) and [foundation backlog](../specs/0001-workflow-foundation/tasks.md).

If you are starting an application, use a separate repository or working branch. Copy the reusable files identified in the [repository map](../docs/repository-map.md). A copy is a starting artifact: it does not install a plugin, enable hooks, or register commands. Keep the research as reference, and archive or omit the framework's own specification from the application's active backlog.

If an application already exists, follow [brownfield adoption](05-brownfield-adoption.md) before copying files. Do not replace its root instructions or source layout.

## 2. Establish the project context

Ask Codex to inspect what exists and create the project brief using the [brief template](../templates/project-brief.md). Capture users, outcome, scope, constraints, existing decisions, and unresolved questions. Separate observed facts from proposals. Do not select CDK, Terraform, serverless, containers, a database, CI provider, region, or budget just because a template mentions them.

Kiro's product, technology, and structure steering serve three distinct questions. In this scaffold, answer them through the brief, accepted design/decisions, and an actual source map. Keep `AGENTS.md` as the concise router rather than duplicating every project document in its always-loaded context. Add scoped instructions only where repeated mistakes or a concrete subsystem need justify them.

## 3. Check the execution environment without touching AWS

Use the [environment capabilities template](../templates/environment-capabilities.md). Record the Codex surface/version where observable, repository access, available tools, local test commands, and plugin capability states. Check current official AWS guidance using [the AWS guide](02-aws-guidance-and-access.md). This is a capability inventory, not a request to authenticate, upgrade, install, or query an account.

Keep local and hosted environments separate. A local plugin, hook, credential provider, or filesystem path is not automatically available in a cloud execution environment. State the minimum next step if a required tool is unavailable.

## 4. Consult on the first useful result

Use [Consult](../workflows/consult.md) to define the smallest delivery that demonstrates value. Compare only meaningful architectural alternatives, with operational and cost consequences. Record accepted decisions, and leave unresolved material choices visible.

Create a focused work specification, for example `specs/0100-first-capability/`. Select Requirements-First, Design-First, Quick Spec, bugfix, or a small Plan-led route according to the actual work. The [first-feature guide](03-first-feature.md) explains how to move from intent to traceable tasks.

## 5. Establish verification before implementation

For each critical requirement, identify what observation would demonstrate it. Select tests appropriate to the risk: examples, properties, integration, contract, infrastructure, performance, or operational checks. Mark cloud-dependent checks as not run until the target environment and authority exist. Mock results do not establish AWS IAM, networking, or managed-service behavior.

The specification can be ready while deployment is still outside scope. Continue authorized local implementation and review. Prepare the exact release candidate before seeking a consequential deployment decision where one is still needed.

## Ready to start

A project is ready for its first implementation when its outcome and scope are clear, consequential constraints are established, the selected design supports them, the next task is unblocked, and the required verification is feasible or its remaining limitation is explicit. Do not demand approval of each file if the user already authorized the work.

Suggested first prompt:

> Initialize this copied bootstrap for my project: [objective]. Inspect the repository, create the project brief, identify material unknowns, and choose the appropriate specification route. Keep the current stack where one exists. Prepare a reviewable first scope and continue any implementation I have already authorized. Record the continuation point in delivery/current-handoff.md.

