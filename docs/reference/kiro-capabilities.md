# Kiro workflow reference

This reference separates documented Kiro behavior from the repository procedures proposed here. It is based on public official documentation reviewed on **2026-11-21**. This repository has not been tested as a native Kiro or Codex integration.

The goal is to reproduce useful engineering practices in Codex: grounded consultation, explicit specifications, traceable tasks, meaningful verification, and controlled release. Creating similarly named Markdown files does not create Kiro's interface, execution engine, or enforcement mechanisms.

## The complete development loop

| Stage | Documented Kiro behavior | Procedure to preserve in this repository |
| --- | --- | --- |
| Ground the project | Generate Steering Docs analyzes the repository for product purpose, technology, and structure. | Inspect the existing project and accepted decisions before proposing work. Keep established facts separate from assumptions. |
| Select the route | Feature Specs support Requirements-First and Design-First. Quick Spec, Bugfix Specs, and Plan mode serve different needs. | Choose the smallest route that provides enough clarity and evidence for this change. |
| Specify behavior | Feature requirements use user stories, acceptance criteria, and EARS-style conditions and outcomes. | Give each material requirement an identifier and an observable acceptance check. |
| Challenge requirements | Analyze Requirements checks interactions, ambiguities, conflicting constraints, assumptions, and missing cases. | Resolve material contradictions before implementation; record deliberately deferred questions. |
| Develop the design | Design covers components, interfaces, data, interactions, failures, and testing. | Explain how the design satisfies requirements and fits accepted architecture. |
| Define correctness | The correctness feature derives testable properties and links them to requirements and tasks. | Identify important invariants before implementation; choose suitable verification methods. |
| Plan and execute tasks | Tasks have dependencies and required/optional status; independent tasks can execute in waves. | Record dependencies, scope, and acceptance checks before concurrent work. |
| Reconcile change | Sync Files updates tasks after specification changes and can identify implemented work. | Reconcile specification, implementation, task status, and evidence after material changes. |
| Review and recover | Local checkpoints and conversation forks support development recovery. | Review the exact candidate revision and use separate procedures for AWS or data recovery. |

Sources: [First project](https://kiro.dev/docs/getting-started/first-project/), [Specs](https://kiro.dev/docs/specs/), [Feature Specs](https://kiro.dev/docs/specs/feature-specs/), [Correctness](https://kiro.dev/docs/specs/correctness/), [Spec best practices](https://kiro.dev/docs/specs/best-practices/).

Kiro also provides native specification review controls, task-status UI, and `#spec` context selection. The repository equivalent is explicit review, canonical Markdown records, and instructions to load the selected specification. Those practices are usable by Codex immediately; they do not claim to reproduce Kiro's native interface or automatic event handling.

## Greenfield and brownfield entry points

For greenfield work, [Requirements-First](https://kiro.dev/docs/specs/feature-specs/requirements-first/) establishes intended behavior before choosing its implementation. For brownfield work, [Design-First](https://kiro.dev/docs/specs/feature-specs/tech-design-first/) accommodates existing architecture, and [Bugfix Specs](https://kiro.dev/docs/specs/bugfix-specs/) formalizes behavior that must be preserved.

This scaffold adds an explicit [brownfield intake](../../workflows/brownfield.md) to establish the current baseline, data obligations, and infrastructure ownership before a target specification. It retains existing repository conventions by default. A bootstrap skeleton supplies a starting structure for a new project; an existing project can adopt the same workflow through links and incremental changes.

## Choose the appropriate specification path

| Route | Entry point and sequence | Important distinction |
| --- | --- | --- |
| Requirements-First | Desired behavior → reviewed requirements → design → tasks. | Useful when implementation choices can adapt to user needs. |
| Design-First | Accepted architecture or technical constraints → reviewed design → derived requirements → tasks. | Useful for an existing system. Validate feasibility; a generated design is not proof. |
| Quick Spec | Clarifying questions → requirements, design, and tasks generated in sequence → task review. | Omits intermediate phase approvals; the artifacts can still be reviewed and revised. |
| Bugfix Spec | Reproduction and behavior analysis → root cause and scoped fix → implementation and regression checks. | `bugfix.md` distinguishes incorrect, expected, and preserved behavior. |
| Plan mode | Questions and read-only exploration → conversational implementation plan → execution handoff. | Does not generate the formal specification files. Its documented tools exclude writing, commands, and MCP. |
| Direct change | A straightforward, understood edit and proportionate verification. | Formal feature specifications are unnecessary for every minor change. |

Sources: [Requirements-First](https://kiro.dev/docs/specs/feature-specs/requirements-first/), [Design-First](https://kiro.dev/docs/specs/feature-specs/tech-design-first/), [Quick Spec](https://kiro.dev/docs/specs/quick-spec/), [Bugfix Specs](https://kiro.dev/docs/specs/bugfix-specs/), [Plan mode](https://kiro.dev/docs/specs/plan/).

## Capabilities have surface limits

The current [Specs matrix](https://kiro.dev/docs/specs/) documents Feature Specs, Bugfix Specs, Quick Spec, and parallel task execution across IDE, CLI, Web, and Mobile. It lists **Analyze Requirements on IDE and CLI**, and the integrated **correctness/property-based testing feature on IDE only**. These are product-interface limits; ordinary generated test code is a separate concern.

[Analyze Requirements](https://kiro.dev/docs/specs/analyze-requirements/) operates on feature specs and specs without a recorded type. It rejects other known types, including Bugfix Specs. The analysis is optional for small, well-understood work. It examines relationships between requirements and updates them as questions are resolved.

[Property-based testing](https://kiro.dev/docs/specs/correctness/) generates varied inputs to challenge a stated invariant. Kiro marks these tests optional by default. Passing them increases confidence; it does not prove correctness. External integrations and nondeterministic behavior may need other checks. In this repository, the verification needed to establish an accepted requirement remains required even when a particular testing technique is optional.

## Context, tools, and automation

| Mechanism | What it contributes | What it does not establish |
| --- | --- | --- |
| Steering / `AGENTS.md` | Persistent project conventions and context; steering supports selective inclusion. | An enforced security boundary or a successful verification result. |
| Skills | Reusable instructions loaded when relevant, with supporting resources as needed. | Authority to perform an action or proof that the instructions were followed. |
| Powers / MCP | Bundled expertise and connections to external tools. | Account authorization, correct configuration, or availability on a different client. |
| Hooks | Event-triggered commands or prompts; some pre-tool hooks can block actions. | Equivalent behavior in Codex, required CI checks, or permission to incur costs. |

Sources: [Steering](https://kiro.dev/docs/steering/), [Skills](https://kiro.dev/docs/skills/), [Powers](https://kiro.dev/docs/powers/), [MCP](https://kiro.dev/docs/mcp/), [Hooks](https://kiro.dev/docs/hooks/), [Hook actions](https://kiro.dev/docs/hooks/actions/).

Use the existing official **AWS Core** and **AWS Data Analytics** plugins for AWS expertise when skill use is allowed. Discover relevant official skills through Core `search_documentation` with `agent_skills`, then retrieve the exact returned skill identifier. Read references as needed. For documentation-only research or a skill opt-out, use current official documentation directly. Do not copy AWS guidance into these workflow contracts, install duplicate connections, or assume a plugin verified in one environment is verified in another.

## The harness and workflow runtime

[How Kiro works](https://kiro.dev/docs/how-kiro-works/) describes a shared harness that assembles context, consults the model, checks tool permissions, executes tools, feeds results back, and compacts context when needed. Its interfaces have capability-specific availability. The repository adaptation uses Codex's own supported execution surface; it does not attempt to reproduce the harness or ACP protocol.

[Workflows](https://kiro.dev/docs/workflows/) is a separate runtime mechanism. Saved recipes declare steps and control flow; steps use isolated sessions and explicit outputs. This is a meaningful part of the current workflow beyond specification files. [Authoring](https://kiro.dev/docs/workflows/authoring/) documents sequence, repeat, parallel and watch nodes, agent selection, conditions, and handoffs. A Kiro recipe is not native Codex configuration.

| Kiro runtime concern | Codex adaptation contract | Present repository status |
| --- | --- | --- |
| Isolated steps and handoffs | Bounded worker inputs, outputs, candidate identity, fresh review context. | Documented; native delegation can be used where available, controller unimplemented. |
| Parallel branches and joins | Dependency eligibility, file ownership, combined-candidate checks. | Procedure supplied; scheduler unimplemented. |
| Bounded correction loops | Explicit stop conditions, retained attempts and usage limits. | Contract supplied; automated loop unimplemented. |
| External waits and PR feedback | Supported event source, deduplicated events, current-head checks, idle without model turns. | Design supplied; no watcher or schedule enabled. |
| Pause, stop, retry and resume | Durable state and unknown-outcome reconciliation. | Manual continuation supplied; persistent controller unimplemented. |
| Runtime progress and artifacts | Status projection from actual attempts and evidence, separate from canonical tasks. | Handoff/evidence conventions supplied; no native dashboard claimed. |

[Workflow management](https://kiro.dev/docs/workflows/manage/) distinguishes run controls and persisted progress. Retry can preserve completed siblings but does not undo workspace edits. This motivates explicit partial-state inspection in the Codex design. Web task queues and [Crew Task Runner](https://kiro.dev/docs/crew/features/task-runner/) have their own lifecycles; they are not silently folded into ordinary Specs.

The [runtime research](../research/runtime-parity.md) and [adapter contracts](../adapter-contracts.md) specify these gaps and their planned acceptance cases.

## Synchronization and evidence are separate concerns

[Spec best practices](https://kiro.dev/docs/specs/best-practices/) describes updating requirements and design in the order appropriate to the chosen route, then synchronizing tasks. Sync Files can also mark already implemented work. Treat that as task reconciliation. Acceptance still requires evidence of the intended behavior.

This repository adds a proposed evidence rule: when a requirement, design, implementation, environment, or relevant dependency changes, assess its impact and mark affected evidence stale. Preserve prior evidence as history. Retain unaffected claims only with an explicit rationale, then rerun the checks needed for the new candidate revision.

## Development recovery is not AWS rollback

[Checkpoints](https://kiro.dev/docs/checkpoints/) restore agent-edited files and associated conversation context. A conversation fork leaves files alone. Checkpoints do not track changes made through shell commands or MCP tools, and restoring a snapshotted file can overwrite later manual changes. Availability also differs by surface.

These features cannot undo AWS API effects or database changes. Release and incident procedures therefore require their own rollback, forward-recovery, data-protection, and verification decisions.

Kiro Web can separately [assume a configured IAM role](https://kiro.dev/docs/web/sandbox/environment-configuration/) and supply short-lived credentials to its sandbox. That does not establish the same authentication route in Codex or authorize account operations in this project. Public consultation requires no AWS credentials. Any later account access remains subject to explicit task authorization and project limits.

## What this scaffold claims

- **Documented:** the Kiro capabilities linked above, within their stated surface limits.
- **Proposed:** repository workflow contracts that adapt useful practices to Codex.
- **Not yet verified:** automatic loading, task orchestration, hook execution, CI enforcement, plugin parity, or AWS deployment for this repository.

Before implementing integration behavior, verify the exact Codex surface and current official documentation. Record the tested version, environment, operation, result, and remaining limitation. Keep the application's existing tools and accepted architecture unless a reviewed decision changes them.
