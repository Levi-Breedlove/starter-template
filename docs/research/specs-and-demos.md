# Research: specifications, project context, and official demonstrations

Research date: **2026-11-21**. Scope: public official Kiro documentation, published video transcripts, and official video pages relevant to a Codex bootstrap for **greenfield and brownfield AWS projects**.

## Findings that shape the scaffold

Kiro's useful development behavior extends beyond producing three Markdown files. It establishes project context, selects a work route, examines requirements, connects design to testable behavior, executes dependent tasks, and updates the specification when intent or implementation changes. The scaffold adopts that lifecycle as explicit Codex instructions. Native UI, event handling, scheduling, and enforcement require separate implementation and verification.

The strongest demonstration evidence retrieved here shows **repository inspection before steering generation** and **steering plus workspace search before requirements creation**. That supports treating project grounding as a real phase. The detailed lifecycle after requirements is established by current documentation; the short demonstration transcripts do not show a complete build, test, or deployment.

## Evidence access levels

| Level | What was inspected | What it can support |
| --- | --- | --- |
| Published visual transcript | The official text description of visible actions in a demonstration. | Only the actions that text describes. It is not a claim of full video playback or a complete spoken transcript. |
| Official video metadata and description | The publisher's title, date, duration, and description. | The stated subject and demonstration scope; not independently observed execution or outcomes. |
| Current product documentation | The relevant official workflow or capability page. | Documented behavior and surface limits, subject to version changes. |

No full video playback or audiovisual analysis was performed for this research. Direct retrieval of the two YouTube watch pages attempted for the catalog demonstrations was throttled or disabled. No accessible task-execution or hook video transcript was retrieved. Those limits are retained below rather than replaced by inferred observations.

## Four official demonstrations inspected

| ID | Demonstration and exact source | Published date / duration | Access obtained |
| --- | --- | --- | --- |
| DEMO-01 | [Generating steering documents in Kiro](https://kiro.dev/transcripts/kiro-steering/) · [official video asset](https://kiro.dev/videos/kiro-steering.mp4) | Transcript undated; duration not stated. | Published visual transcript read. |
| DEMO-02 | [Creating a spec in Kiro](https://kiro.dev/transcripts/specs-start/) · [official video asset](https://kiro.dev/videos/specs-start.mp4) | Transcript undated; duration not stated. | Published visual transcript read. |
| DEMO-03 | [How Granular Should Your Specs Be?](https://kiro.dev/videos/4TBKvkG-WwA/) | 2025-08-28 · 29:24 | Official metadata and description read; full transcript/playback unavailable in this research. |
| DEMO-04 | [Ship Without the Guesswork — Kiro + Agent Toolkit](https://kiro.dev/videos/jv3dsOpDeH4/) | 2026-09-30 · 7:28 | Official metadata and description read; full transcript/playback unavailable in this research. |

The first two are linked from [Your first project](https://kiro.dev/docs/getting-started/first-project/), whose displayed update date was 2026-11-12. That guide's update date is **not** asserted as either video's publication date. Its [official Markdown version](https://kiro.dev/docs/getting-started/first-project.md) exposes the video asset URLs.

### DEMO-01: grounding before steering

The published description shows the user requesting generated steering and the agent reading repository files, including a package manifest, README, build configuration, and application/context source. It ends while work is in progress. It does not expose the final steering content or prove that every generated convention was accurate.

**Design inference:** brownfield adoption should inspect representative source and configuration before writing project context. Generated summaries require reconciliation with accepted intent. For greenfield work, unknown conventions must be established through consultation rather than invented from an empty repository. See [Brownfield intake](../../workflows/brownfield.md) and [Consult](../../workflows/consult.md).

### DEMO-02: specification creation is grounded in the project

The transcript describes a product-review feature request. The agent includes steering, searches the workspace, and creates a requirements document; a new specification appears in the sidebar while processing continues. It does not demonstrate a completed design, implementation, test suite, or release.

**Design inference:** route selection should cause Codex to load the chosen project's conventions and relevant implementation evidence before authoring requirements. A newly created specification is a draft work artifact, not a claim that the work is accepted or complete. See [Feature](../../workflows/feature.md).

### DEMO-03: granularity is a decision

The official description identifies two subjects: how narrowly to scope requirement documentation and how to handle multiple requested features. Its description alone does not establish the presenters' complete recommendations or a specific task-sizing rule.

**Design inference, supported independently by current docs:** keep specifications focused on coherent changes and choose an appropriate route. The current [best-practices page](https://kiro.dev/docs/specs/best-practices/) recommends multiple feature-specific specs and permits direct fixes for straightforward small issues. The scaffold therefore avoids one enormous project spec and avoids requiring a full spec for every minor edit.

### DEMO-04: AWS knowledge is a separate input to the workflow

The official page describes a greenfield portfolio-site walkthrough using Kiro with Agent Toolkit for AWS. It presents current AWS documentation and deployment guidance as inputs to the coding agent. The description does not expose the full permissions, resulting infrastructure, account costs, or successful operational checks.

**Design inference:** a reusable AWS bootstrap should connect its workflow to official AWS expertise on demand. It should record the source and tool availability, then verify the produced design and implementation. The publisher's promotional claims about correctness are not acceptance evidence. The scaffold does not infer authorization to access AWS or incur spending from this demonstration.

## Current documents supply the full specification lifecycle

### 1. Start from the actual project

[Your first project](https://kiro.dev/docs/getting-started/first-project/) describes generating context for product purpose, technology, and structure. [Steering](https://kiro.dev/docs/steering/) distinguishes persistent conventions from selectively included guidance. This supports a small stable instruction entry point with links to relevant project records, instead of copying every document into permanent context.

### 2. Match the route to the starting point

| Route | Documented sequence | Scaffold application |
| --- | --- | --- |
| [Requirements-First](https://kiro.dev/docs/specs/feature-specs/requirements-first/) | Behavior and acceptance criteria, design, then tasks. | Default starting point when user needs drive a new feature. |
| [Design-First](https://kiro.dev/docs/specs/feature-specs/tech-design-first/) | Architecture or technical constraints, derived requirements, then tasks. | Preserve a known brownfield design while defining the requested change. |
| [Quick Spec](https://kiro.dev/docs/specs/quick-spec/) | Clarify up front; produce requirements, design, and tasks without intermediate approvals. | Batch familiar bounded planning; keep required verification. |
| [Bugfix Spec](https://kiro.dev/docs/specs/bugfix-specs/) | Defect, intended result, preserved behavior, cause/fix design, and tests. | Diagnose a defect without silently expanding it into a redesign. |
| [Plan mode](https://kiro.dev/docs/specs/plan/) | Read-only exploration and questions, conversational plan, then execution handoff. | A lighter route when durable formal specifications would add little value. |

Kiro's Plan mode is not its formal Specs workflow: the documentation says it does not write the three spec artifacts and does not provide command execution or MCP tools. Codex behavior must be verified separately; this repository does not transfer those product restrictions by analogy.

### 3. Challenge requirements before trusting them

[Analyze Requirements](https://kiro.dev/docs/specs/analyze-requirements/) evaluates relationships and conflicts across the requirement set, not just grammar. It can identify missing cases and unclear constraints and can be rerun after edits. It applies to feature/untyped specs, not known Bugfix Specs. The [capability matrix](https://kiro.dev/docs/specs/) lists IDE/CLI availability.

The repository contract makes the relevant reasoning explicit: identify the affected requirements, explain why they conflict or remain ambiguous, resolve material findings, and retain intentionally deferred decisions. The result must still reflect the user's actual intent.

### 4. Connect design to observable correctness

[Correctness](https://kiro.dev/docs/specs/correctness/) links requirements, testable properties, tasks, and generated test cases. The integrated feature is documented for IDE only, with PBT tasks optional by default. It supplies evidence, not a mathematical guarantee.

The scaffold distinguishes a testing method from an acceptance obligation. Property-based testing can be optional when another method adequately verifies the requirement. A required behavioral outcome cannot disappear because the task runner skips optional tests. External AWS behavior needs appropriate environment-specific checks; local examples do not prove IAM, networking, availability, or recovery behavior.

### 5. Execute the dependency graph and reconcile changes

[Specs](https://kiro.dev/docs/specs/) describes task dependencies and waves of parallel work. [Best practices](https://kiro.dev/docs/specs/best-practices/) says Run all Tasks processes incomplete required tasks and explains Sync Files after specification changes or work completed elsewhere.

The repository adapts those practices through task IDs, dependency records, scoped implementation, and [Reconcile](../../workflows/reconcile.md). The task record must say whether work is implemented, verified, blocked, or awaiting a decision. A changed contract or candidate revision requires an impact assessment before reusing old evidence.

## Greenfield and brownfield consequences

| Concern | Greenfield | Brownfield |
| --- | --- | --- |
| Grounding | Establish users, data, constraints, success measures, and initial architecture decisions. | Inventory existing source, accepted architecture, deployment ownership, data, and evidence. |
| Requirements | Describe the desired system and important failure behavior. | Identify changed behavior and explicitly preserved behavior. |
| Design | Choose a justified architecture with costs and operations in view. | Identify the smallest adequate change, integration points, and migration obligations. |
| Task generation | Plan a first coherent deliverable and its dependencies. | Reuse valid implemented work; do not treat an existing codebase as empty. |
| Verification | Establish a meaningful baseline and target-environment checks. | Compare against the baseline and verify compatibility/preservation as well as the new behavior. |
| Adoption | Use the bootstrap's initial organization. | Link existing authoritative artifacts and adapt incrementally; no default file or IaC-state migration. |

These are engineering recommendations derived from the lifecycle, not claims that a short demo automatically performs every activity. They are implemented as [workflow contracts](../../workflows/README.md), supported by templates and the root instructions.

## What the demonstrations cannot establish

- Native Kiro/Codex feature parity, identical permission models, or the same plugin availability across clients.
- Automatic enforcement of repository procedures by Markdown alone.
- That a generated task list has complete acceptance coverage or that all optional checks ran.
- That a deployment succeeded, a cost estimate matches a bill, or a running service meets its operational requirements.
- That restoring a local checkpoint reverses AWS or database effects; [checkpoint documentation](https://kiro.dev/docs/checkpoints/) explicitly limits what file changes are tracked.

The next implementation step is to test the scaffold on one contained greenfield change and one contained brownfield change, recording exact inputs, revisions, observed behavior, and remaining gaps. Until then, the workflow is documented and usable as instructions; automated orchestration remains a separately tracked implementation claim.

## Additional official demonstration for orchestration research

[Working With Kiro workflows](https://kiro.dev/videos/b4U9PlBI5qM/) was published **2026-10-15**, duration **7:20**. Its official description covers generating or selecting a workflow, inspecting steps/agents/models/conditions, running it, and saving a reusable recipe. Only that metadata and description were inspected here. It supports locating the runtime research topic; it does not establish that this repository has an equivalent runner.
