# Research: runtime orchestration and behavioral parity

Research date: **2026-11-21, America/Los_Angeles** (2026-11-22 UTC). Scope: current public official Kiro and OpenAI documentation, one official Kiro video description, and read-only discovery of the Codex CLI installed in this research environment. No Kiro runner, hook, scheduled task, AWS operation, or deployment was executed.

## Finding

The repository needs two layers to reproduce the useful Kiro experience: **a coherent development contract** and **a runtime that carries it out reliably**. The templates and workflow documents supply the first layer. They do not create the second merely by existing on disk.

Kiro's current [Workflows documentation](https://kiro.dev/docs/workflows/) describes runtime-managed steps with separate sessions, explicit handoffs, parallel branches, repeat loops, external waits, and background operation. Current Codex has substantial building blocks, including [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [hooks](https://learn.chatgpt.com/docs/hooks), [non-interactive execution](https://learn.chatgpt.com/docs/non-interactive-mode), and a [SDK](https://learn.chatgpt.com/docs/codex-sdk). The cited Codex interfaces do not establish compatibility with Kiro's recipe schema. A compatible orchestration adapter would be repository implementation work, with its own tests and maintenance cost.

The practical recommendation is to make the explicit conversational workflow useful first, then implement only the automation whose behavior can be demonstrated. Keep native capabilities where they fit. Do not publish Kiro YAML or JSON under a Codex directory and call it an installed runner.

## 1. Separate the product mechanisms

| Mechanism | Documented Kiro behavior | Consequence for this scaffold |
| --- | --- | --- |
| [Specs](https://kiro.dev/docs/specs/) | Connects requirements or bug analysis, design, and tasks. Running a spec can infer dependencies and execute independent tasks in sequential waves. | The task file is the work contract. A future scheduler must respect its dependencies and required/deferred distinction. |
| [Workflows](https://kiro.dev/docs/workflows/) | Coordinates agents and reusable recipes; steps have separate sessions and explicit communication. | Review, implementation, and final validation need deliberately controlled contexts and handoffs. |
| [Hooks](https://kiro.dev/docs/hooks/) | Runs commands or agent prompts on supported events. | Automate small checks or context updates at real events; a hook is not the complete delivery workflow. |
| [Kiro Web tasks](https://kiro.dev/docs/web/using-the-agent/creating-tasks/) | Has its own queue, active, attention, completed, and cancelled lifecycle; feedback can restart work. | Do not equate a web task's state with a spec checkbox, successful test, or production release. |
| [Crew Task Runner](https://kiro.dev/docs/crew/features/task-runner/) | Separately documents a longer-running decomposition, execution, test, review, retry, and checkpoint loop. | Crew's defaults are not ordinary Spec behavior and are not automatically the right Codex design. |

The [workflow authoring reference](https://kiro.dev/docs/workflows/authoring/) defines `step`, `sequence`, `repeat`, `parallel`, and `watch` nodes. It also defines outcome signaling, captured output, artifact references, and loop conditions. These are actual runtime semantics. A prompt asking an agent to remember the same order is a weaker mechanism until observed behavior proves otherwise.

## 2. What Codex already supplies, and what remains to be built

| Concern | Official Codex foundation | Exact remaining contract |
| --- | --- | --- |
| Independent work | [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) can delegate and collect parallel work. | Choose eligible tasks, prevent conflicting writers, and reconcile the joined candidate. Delegation alone does not prove dependency scheduling. |
| Structured execution | [`codex exec`](https://learn.chatgpt.com/docs/non-interactive-mode) emits JSONL events and can request a final response matching a JSON Schema. | Validate outputs against observed artifacts and checks. `turn.completed` is not business acceptance or deployment success. |
| Continuing work | The [Codex SDK](https://learn.chatgpt.com/docs/codex-sdk) starts, continues, and resumes threads. | Persist work identity, dependencies, attempt outcomes, input identities, and remaining authority outside a lossy conversation summary. |
| Custom control interface | [App Server](https://learn.chatgpt.com/docs/app-server) exposes thread start/resume/fork, history, events, and turn controls. | An optional future controller must implement its own scheduling, recovery, and presentation. It is not required for the first usable scaffold. |
| Workspace isolation | [Worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees) isolate concurrent chats' checkouts. | Select the correct base, protect dirty work, own file ranges, and test the integrated result after joining branches. |
| Lifecycle automation | [Hooks](https://learn.chatgpt.com/docs/hooks) supports command and MCP-tool handlers, subject to trust and event coverage. | Translate event/action behavior explicitly and test it on the actual client. Native Kiro and Codex formats are not interchangeable. |
| PR review | [GitHub integration](https://learn.chatgpt.com/docs/third-party/github) supports requested or configured code review. | Reviewing a diff does not create a complete feedback-fix-check-re-review loop or establish all feature acceptance criteria. |
| Background triggers | [Scheduled tasks](https://learn.chatgpt.com/docs/automations) documents surface-dependent scheduled and app-event execution. | Select one supported trigger source, deduplicate events, bound work, and persist continuation. No schedule is created by this scaffold. |

**Local observation, not deployment proof:** this research environment returned `codex-cli 0.172.0-alpha.2` for `codex --version`. Read-only `--help` queries exposed `exec`, `review`, `resume`, `fork`, `--worktree`, `--json`, and `--output-schema`. This identifies the installed research CLI and its advertised interface. It does not verify the user's desktop installation, plugin state, hook operation, credentials, model access, or an end-to-end run. No authentication or user configuration was read.

## 3. Hook parity requires event-level mapping

The current [Kiro trigger reference](https://kiro.dev/docs/hooks/types/) lists file and spec-task events for IDE and CLI V3, with a smaller Web event set. Compaction and permission events have additional version conditions. Consult that event-level table rather than inferring that every client supports every trigger from an overview checkmark.

Current [Codex hook documentation](https://learn.chatgpt.com/docs/hooks) lists session, prompt, tool, compaction, subagent, model-request, stop, and interrupt events. Its `prompt` and `agent` handler types are parsed but skipped; command and `mcp_tool` handlers are supported. Non-managed hooks require review of their current definitions. Tool hooks do not cover every possible tool path, and post-tool hooks cannot undo completed effects. Background hook completion does not start a new user turn.

The proposed adapter should therefore make these mappings explicit:

| Desired behavior | Proposed implementation boundary | Proof needed |
| --- | --- | --- |
| Restore the active work context | A supported session/compaction hook reads a small durable handoff. | Correct task and constraints survive resume without introducing new instructions or resetting completed work. |
| Check a spec task before/after execution | The task controller emits its own task boundary events. | Exactly the intended task produces the event, including retries and blocked outcomes. Do not rename an unrelated tool event as a native task hook. |
| Check changed files | A supported tool event or controller checkpoint determines the actual changed paths. | Edits through different supported paths are covered, output-only edits do not recurse, and no-change events do no work. |
| Ask an agent to respond to an event | An explicitly selected controller/trigger launches a scoped Codex turn. | Handler availability, duplicate suppression, allowed actions, and termination are verified. An unsupported handler must be reported, not silently treated as active. |

Hook files in this repository remain future implementation. Review, trust, and execution controls are product-specific; no instruction document can override them. For AWS, the enforcing boundary must also be the authorized identity and environment permissions, not merely a regular expression over shell commands.

## 4. Proposed runtime contracts

These are original implementation recommendations for Codex, not claims about either product's internal architecture.

### Task selection and outcome ownership

Read one canonical task record. A task is eligible only when its real prerequisites are satisfied, its required inputs exist, and the requested action is within the established scope. Parallelize independent reads and isolated changes; use a single integration owner for shared artifacts and task completion. A worker returns a result, not permission to mark the entire feature complete.

The execution log records attempts and events; it is not another editable task list. Any dashboard or external tracker derives its status from the declared authority. Keep activity such as running, blocked, or awaiting verification separate from the durable completion checkbox. Deferred work remains visible and does not become passed work.

### Handoff and evidence

Each step receives the relevant requirement/design/task references, selected source revision, allowed files or worktree, required inputs, actual authorization reference, and verification obligations. It returns changed artifacts, actual checks, findings, unresolved questions, and limitations.

Bind results to source or base-plus-patch identity, tested artifact digest when applicable, spec revision, environment, fixture/input identities, configuration, tool/procedure, result, and time. A later change triggers an impact assessment: invalidate affected coverage while retaining valid unrelated evidence and historical records. Final validation evaluates the integrated candidate against every required outcome, including preservation behavior.

### Independent review

Start a fresh reviewer context with the original contract, exact candidate/diff, relevant surrounding source, and test evidence. Do not use the author's conversation or conclusion as the reviewer’s proof. A second agent name alone does not establish independent review when it inherits the author's detailed reasoning.

Review must distinguish a finding, no finding within the reviewed scope, and inability to complete review. Missing context, timeout, or a crashed reviewer cannot be recorded as passed. This is a deliberate improvement over the specific [Crew Task Runner behavior](https://kiro.dev/docs/crew/features/task-runner/) that documents review exceptions as non-fatal and treated as passed; it is not asserted as general Kiro behavior.

### Resume, retries, and interruption

Persist a stable work/task identity and a distinct attempt identity. Before retry, inspect the actual workspace and any prior execution receipts. A process crash after an effect but before recording success creates an unknown outcome; reconcile it before considering another attempt. Never assume that conversation resume implies safe replay of external effects.

[Kiro's runtime management reference](https://kiro.dev/docs/workflows/manage/) explicitly preserves completed sibling work during retry while resetting the retry target's runtime data; it also says retry does not undo workspace edits. Its pause, stop, retry, and extra-iteration controls have different meanings. The Codex adapter needs equivalent distinctions and tests, rather than one generic restart action.

Caps should cover task attempts, identical failures, plan revisions, elapsed time, total model usage, and concurrent workers. Choose limits for the project, account for every attempt, and surface the exact exhausted limit. A resumed run does not silently replenish its budget. New scope or increased budget uses the actual authority already established, or needs a concrete decision when outside it.

### PR feedback and external waits

The [Kiro workflow authoring reference](https://kiro.dev/docs/workflows/authoring/) documents PR watches with activity deduplication, check results tied to a head commit, terminal conditions, and idle polling without model turns. That is a useful behavior to reproduce, not evidence that a general-purpose agent chat watches PRs indefinitely.

A future Codex adapter should store the PR identity, head revision, processed event identities, feedback disposition, check status, and stop condition. Wake only for material new input. Classify requested changes against scope; address authorized feedback; verify the new candidate; then seek the required review. Re-fetch state before declaring readiness. Merge, deployment, and messages to other people retain their own actual authorization; a green PR does not confer it. Do not add a polling service or new integration where the project's existing CI/event mechanism can fulfill the contract.

### Local recovery and AWS recovery

[Kiro checkpoints](https://kiro.dev/docs/checkpoints/) distinguish restoring tracked file changes from forking a conversation. Codex worktree/session operations likewise must not be presented as a rollback of cloud resources, external data, or sent messages.

For this repository, consultation and public AWS guidance use the official Agent Toolkit route. Account inspection, imports, state migration, deployment, and cleanup need the project's explicit operational scope and limits. A local lifecycle event must never silently trigger these operations. After an uncertain authorized AWS operation, recover from recorded resource/workflow state and service-specific evidence; do not blindly repeat it. The [AWS integration research](aws-integration.md) supplies the separate knowledge and authorization model.

## 5. Concrete parity tests to implement

This table is an **acceptance catalog**, not a second task backlog. All cases are **planned and unexecuted**. Implementation tasks and completion belong in the framework's canonical `specs/0001-workflow-foundation/tasks.md`.

| ID | Scenario | Required observation |
| --- | --- | --- |
| RP-01 | Start a small greenfield feature. | Selected route produces coherent records, explicit unknowns, and a useful first deliverable; no AWS account call occurs. |
| RP-02 | Adopt an existing project with an accepted stack and dirty files. | Existing architecture, paths, decisions, and user changes are preserved; only missing records are added and baseline gaps remain explicit. |
| RP-03 | Execute tasks A and B independently; C depends on both. | A/B may overlap within the limit; C starts only after both prerequisite outcomes are valid. Shared-file conflicts are prevented or reconciled before C. |
| RP-04 | Finish implementation without running one required check. | The task remains unfinished or needs verification; worker completion alone cannot check it off. |
| RP-05 | Edit a requirement, fixture, configuration, or source after a pass. | Affected evidence is invalidated with a reason; unrelated valid completion remains. |
| RP-06 | Interrupt after a file write and before result persistence. | Resume inspects partial edits, preserves completed siblings, and reconciles the uncertain attempt without duplicate changes. |
| RP-07 | Repeat the same failed check or hit an iteration/time/usage cap. | The loop terminates or requests a bounded decision; resume does not reset the counters. |
| RP-08 | Give the author an incorrect assumption, then start review. | Reviewer receives contract and actual candidate without author reasoning; it can identify the error. A reviewer timeout yields incomplete review. |
| RP-09 | Replay an event; emit another event from hook-generated output. | No duplicate task execution or recursive hook loop; unsupported/untrusted handlers remain visibly inactive. |
| RP-10 | Receive duplicate PR feedback and stale CI for an old head. | Events are processed once and old checks cannot establish current readiness; merge/closed state stops the loop. |
| RP-11 | Receive no external change during a wait. | The selected waiting mechanism spends no model turns while idle and stops at its configured deadline. |
| RP-12 | Attempt deployment from a file-save event during planning. | No AWS side effect occurs; the missing operational scope is reported without acquiring new credentials or broadening access. |
| RP-13 | Run no-key, cross-customer, retry, and concurrent cases in the fictional feature after real implementation. | Every requirement, including unchanged behavior, has relevant result evidence; generated properties do not stand in for database atomicity checks. |
| RP-14 | Rejoin parallel branches and run final validation. | Validation covers the integrated revision and original required contract, rather than relying solely on each branch's earlier pass. |

## 6. Official video evidence and limits

[Working With Kiro workflows](https://kiro.dev/videos/b4U9PlBI5qM/) is an official Kiro video published **2026-10-15**, duration **7:20**. Its published description covers generating or choosing a workflow, inspecting agents and conditions, running it, and saving a reusable recipe. The description and metadata were read. Direct retrieval of the YouTube watch page was disabled; no transcript or video playback was inspected in this research. The runtime behavior above is grounded in documentation, not inferred from unobserved video content.

The companion [specification and demonstration research](specs-and-demos.md) distinguishes published visual transcripts from descriptions and documents the earlier project-grounding phases. Neither research document claims that a product demo, a Markdown scaffold, or one successful local run proves production readiness.
