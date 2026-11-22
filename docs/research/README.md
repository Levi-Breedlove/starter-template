# Research synthesis: making Codex work like Kiro

**Reviewed:** 2026-11-21 (America/Los_Angeles).  
**Method:** Current official Kiro, OpenAI/Codex, and AWS documentation; official demonstration pages and available published visual transcripts; bounded read-only discovery of the research environment's Codex CLI. No custom user skills were used as the design method. No Kiro runtime or AWS deployment was executed for this research.

## Main conclusion

The useful Kiro experience is a connected engineering system: context, specifications, execution, feedback, and recovery. A Codex adaptation needs both a coherent process and tested runtime integrations. The repository now supplies the process, templates, maps, and implementation contracts. It does not claim that naming three Markdown files reproduces the native product.

The most useful implementation order is to establish a readable source of truth, add deterministic traceability/evidence checks, verify native Codex hooks and worker contexts, then add durable orchestration only where it materially improves the work. AWS remains a separate official capability layer and an actual workload delivery responsibility.

## What the research changed in the design

### 1. Begin with evidence about the project

The official [steering visual transcript](https://kiro.dev/transcripts/kiro-steering/) describes repository reads before guidance generation. The [spec-start visual transcript](https://kiro.dev/transcripts/specs-start/) describes steering inclusion and workspace search before requirements creation. They support a concrete design principle: inspect the project before drafting its supposed facts.

The bootstrap therefore has separate greenfield and brownfield intake. Existing code, tests, IaC, and delivery evidence inform the latter; an empty or inaccessible AWS view is recorded as unknown, not assumed compliant or absent.

### 2. Use several specification routes

Current Kiro documentation describes [Requirements-First](https://kiro.dev/docs/specs/feature-specs/requirements-first/), [Design-First](https://kiro.dev/docs/specs/feature-specs/tech-design-first/), [Quick Spec](https://kiro.dev/docs/specs/quick-spec/), [Bugfix Specs](https://kiro.dev/docs/specs/bugfix-specs/), and [Plan mode](https://kiro.dev/docs/specs/plan/). A single rigid sequence would misrepresent that flexibility.

The repository chooses depth by uncertainty and consequence. Bugfixes explicitly protect established behavior. Quick work avoids unnecessary per-file approval pauses. Design-constrained work still checks that user outcomes survive the technical choices.

### 3. Analysis and verification belong before and after implementation

[Analyze Requirements](https://kiro.dev/docs/specs/analyze-requirements/) checks interactions and ambiguity. [Correctness](https://kiro.dev/docs/specs/correctness/) connects properties to requirements and tasks, with surface and optionality limits. These are useful techniques, not automatic evidence that a deployed system satisfies its contract.

The adaptation adds an explicit verification matrix, required/deferred distinction, exact candidate identity, and preservation checks. A task remains unfinished when required acceptance is unverified. Evidence is scoped to the inputs actually tested.

### 4. Separate Specs, Workflows, Hooks, Web tasks, and Crew

[Specs](https://kiro.dev/docs/specs/) organize work. [Workflows](https://kiro.dev/docs/workflows/) provide isolated steps, handoffs, control flow, and recovery. [Hooks](https://kiro.dev/docs/hooks/) react to events. Web task queues and [Crew Task Runner](https://kiro.dev/docs/crew/features/task-runner/) are additional mechanisms with their own states and defaults.

The proposed controller models these responsibilities explicitly. It does not copy Crew behavior into ordinary feature work or claim a chat prompt creates a durable scheduler. The [runtime study](runtime-parity.md) details the distinction and proposed fault tests.

### 5. Codex already has substantial native building blocks

Current official documentation supports [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [hooks](https://learn.chatgpt.com/docs/hooks), and structured [non-interactive execution](https://learn.chatgpt.com/docs/non-interactive-mode). The research environment's CLI help corroborated some advertised interfaces, but did not test them end to end.

The right gap analysis is at the event, state, and evidence level. For example, supported Codex lifecycle hooks do not establish native Kiro spec-task events or Kiro recipe compatibility. Unsupported handler types and untrusted hooks must remain visibly inactive. See [adapter contracts](../adapter-contracts.md).

### 6. Recovery requires more than a saved conversation

Kiro documents [durable workflow progress](https://kiro.dev/docs/workflows/manage/) separately from [file checkpoints and conversation forks](https://kiro.dev/docs/checkpoints/). These distinctions matter when work partially completes before a response is lost.

The adaptation requires partial-state inspection, preserved counters, and unknown-outcome reconciliation. It separates workspace recovery from application/data/AWS recovery. Retry is a decision about observed effects, not a synonym for restarting the whole task.

### 7. The AWS toolkit is an adapter, not the entire lifecycle

AWS's [official repository](https://github.com/aws/agent-toolkit-for-aws) and [setup guide](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/quick-start.html) support agent integration and public guidance. Operational calls still use the caller's actual permissions and task scope. The toolkit does not replace specifications, testing, release identity, or the workload's pipeline.

The [AWS study](aws-integration.md) verifies material deployment and brownfield limits: connected previews may perform account operations; import/drift checks have coverage limits; local emulation differs from cloud evidence; budget alerts are not hard spending caps. The runbooks reflect these facts without imposing an application stack.

### 8. “Better” needs measured outcomes

Proposed improvements are traceability, evidence freshness, truthful failure states, bounded retries, reduced duplicated context, and preservation of existing behavior. They are original design targets, not claims that Kiro lacks every equivalent capability. A fair comparison must use matched tasks, inputs, access, budgets, and acceptance checks.

The [evaluation catalog](../../evaluations/README.md) defines the comparison. No performance, cost, or quality superiority has been measured in this delivery.

## Demonstration evidence inventory

| Material | Date / duration when published | What was actually inspected |
| --- | --- | --- |
| [Generating steering documents in Kiro](https://kiro.dev/transcripts/kiro-steering/) | Undated | Official short visual transcript; not full playback. |
| [Creating a spec in Kiro](https://kiro.dev/transcripts/specs-start/) | Undated | Official short visual transcript; not full playback. |
| [How Granular Should Your Specs Be?](https://kiro.dev/videos/4TBKvkG-WwA/) | 2025-08-28; 29:24 | Official description and metadata only. |
| [Introducing Agent Toolkit for AWS](https://www.youtube.com/watch?v=d1GHVtEFy2A) | 2026-05-06 | AWS Developers description/chapter metadata; direct playback/transcript unavailable. |
| [AWS Tech Tales: Catching Up with Kiro](https://www.youtube.com/watch?v=w-fn-vELIEs) | 2026-05-04 | AWS Events description only; useful brownfield research lead. |
| [Ship Without the Guesswork — Kiro + Agent Toolkit](https://kiro.dev/videos/jv3dsOpDeH4/) | 2026-09-30; 7:28 | Official description and metadata only. |
| [Working With Kiro workflows](https://kiro.dev/videos/b4U9PlBI5qM/) | 2026-10-15; 7:20 | Official description and metadata only. |

Descriptions establish what the publisher presents, not every demonstrated step or successful outcome. Earlier videos can show older product behavior. Detailed claims in this repository use current written documentation when accessible transcripts do not cover them. No full-video viewing or private workflow visibility is claimed.

## Read the detailed studies

- [Specification workflow and demonstration evidence](specs-and-demos.md)
- [Runtime, events, review, recovery, and parity scenarios](runtime-parity.md)
- [AWS toolkit, deployment, brownfield, and cost evidence](aws-integration.md)
- [Capability reference](../reference/kiro-capabilities.md)
- [Official source ledger](../reference/sources.md)
- [Resulting architecture](../workflow-architecture.md) and [implementation roadmap](../implementation-plan.md)

## Remaining uncertainty

Actual client versions, hosted plugin release availability, event coverage, native task UI integration, automation cost, and end-to-end recovery remain implementation evidence to collect. The repository does not infer the owner's installed state from documentation or this research environment. Future changes should refresh the affected official sources and preserve the distinction between documented capability and observed operation.

