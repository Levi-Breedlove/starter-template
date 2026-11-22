# Codex AWS Workflow Bootstrap

A reusable repository foundation for **Kiro-style engineering with Codex and the official Agent Toolkit for AWS**, for greenfield and brownfield projects.

This repository maps the complete development loop: understand the project, select the right specification route, challenge requirements, design, plan dependencies, implement, verify, review, reconcile changes, release, and operate. Its design comes from current official Kiro, Codex, and AWS documentation and accessible official demonstration material, reviewed on **2026-11-21 (America/Los_Angeles)**. It does not depend on the owner's personal skills or a particular application's architecture.

## Start here

| Your situation | Start with | Result |
| --- | --- | --- |
| You want to understand the research | [Research findings](docs/research/README.md) | Evidence, demonstration coverage, gaps, and design implications. |
| You are starting a new AWS project | [Start here](guide/01-start-here.md) | Project context and a first scoped specification. |
| You have an existing codebase or AWS estate | [Brownfield adoption](guide/05-brownfield-adoption.md) | A baseline, preservation requirements, and a small adoption change. |
| You want Codex to perform a feature or fix | [Workflow procedures](workflows/README.md) | A repeatable process with concrete artifacts and verification. |
| You want the complete repository design | [Architecture](docs/workflow-architecture.md) and [repository map](docs/repository-map.md) | Behavior, responsibilities, lifecycle, and file locations. |
| You want to implement deeper automation | [Implementation roadmap](docs/implementation-plan.md) | Ordered work backed by the [canonical backlog](specs/0001-workflow-foundation/tasks.md). |

## What is usable now

- A root [AGENTS.md](AGENTS.md) that routes Codex through the project context and relevant procedure.
- Procedures for consultation, brownfield intake, features, bugfixes, reconciliation, review, release, and incidents.
- Original templates for requirements, design, tasks, decisions, reviews, release evidence, continuation, environment capabilities, and adoption.
- AWS guidance, cost, security, infrastructure, deployment, rollback, and teardown contracts that preserve the project's actual tool choices.
- A worked [booking retry example](examples/booking-retries/README.md), explicitly fictional and unimplemented.
- An offline link and structure checker with fixture tests:

~~~sh
python3 scripts/check_repository.py
python3 -m unittest discover -s tests -p 'test_*.py'
~~~

The checker validates repository links and structure. It does not prove application correctness, native Codex configuration, or AWS readiness.

## What still needs implementation

The [native adapter design](docs/adapter-contracts.md) covers scoped context loading, trusted Codex hooks, specialized agents, deterministic task/evidence checks, and a durable orchestration adapter. These are planned capabilities. This bootstrap does not contain an active hook configuration, scheduled agents, a deployment pipeline, or a Kiro-compatible workflow engine.

Codex already supplies useful native building blocks, including repository instructions, tools, reviews, subagents, and current local lifecycle hooks. Kiro's saved workflow recipes and task events are not a portable Codex configuration format. The [capability comparison](docs/reference/kiro-capabilities.md) and [runtime research](docs/research/runtime-parity.md) identify what can be mapped and what must be built and tested.

## Use with Codex

Open the repository in your supported Codex environment and give it a concrete outcome. For example:

> Read AGENTS.md. We are adopting this bootstrap for a greenfield AWS project. Follow guide/01-start-here.md, establish the project brief from my objective, and prepare the first specification. Use current official AWS guidance. Keep unresolved architecture decisions visible. My objective is: …

For an existing application:

> Read this repository's existing instructions first. Follow the bootstrap's brownfield procedure. Inspect the code and delivery configuration, map the current architecture and behavior, and propose the smallest adoption change. Preserve existing instructions, IaC ownership, tests, and pipeline. Account inspection is outside this repository-only intake.

These are ordinary prompts, not registered slash commands. Once scope and implementation are authorized, the procedures continue without repeated permission questions. Cloud operations use the project's actual authorization and environment limits.

## Two distinct uses of this repository

The files under `specs/0001-workflow-foundation/` plan improvements to this bootstrap itself. When using the bootstrap for an application, create a new application brief and work specification; do not treat the framework's backlog as your application's work. The adoption guides explain what to copy, adapt, and retain as reference.

For greenfield, the project chooses its stack, IaC, pipeline, environments, and operational targets. For brownfield, the existing system is the starting point. No framework, AWS service, repository reorganization, or infrastructure import is imposed by this scaffold.

## What “better” means here

It is a testable goal, not an achieved benchmark: fewer lost decisions, complete critical-requirement traceability, stale-evidence detection, safe resumption, accurate capability reporting, and preserved brownfield behavior. The [evaluation plan](evaluations/README.md) defines scenarios and measurements. No head-to-head runtime result or performance advantage over Kiro is claimed.

## Research and operating references

- [Research synthesis and videos](docs/research/README.md)
- [Official source ledger](docs/reference/sources.md)
- [First feature](guide/03-first-feature.md)
- [AWS guidance and access](guide/02-aws-guidance-and-access.md)
- [Maintenance and release](guide/04-maintain-and-release.md)
- [Current handoff](delivery/current-handoff.md)

