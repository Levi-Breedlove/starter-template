# Codex AWS Consulting and Delivery Bootstrap

Turn a rough idea or an existing AWS project into an interviewed brief, testable requirements, an explained design, ordered implementation tasks, and evidence of the result. Codex leads the consultation; local code keeps the work records consistent between sessions.

The default experience is conversational:

> Act as my AWS consultant. Read the project context first, help me refine the idea, and ask the next few questions that materially affect the requirements. Recommend the technical choices and explain their tradeoffs. Save our decisions, then guide me through requirements, design, tasks, implementation, and verification.

You do not need to arrive with an architecture or learn a command vocabulary. Codex should infer what it can from the requirements, research current AWS guidance, and ask about the business decisions it cannot safely infer. Existing answers and accepted architecture remain part of the project record.

## Start a project

Keep this bootstrap checkout separate from your application. Python 3.10 or newer is required; the tools use only the standard library. From this checkout, preview an installation into an empty project directory:

```bash
python3 scripts/bootstrap.py --source . --target /path/to/my-app --mode greenfield
```

Review the proposed files, then repeat with `--apply`. For an existing application use `--mode brownfield`. The installer adds a reusable `.aws-workflow/` layer, a bounded block in `AGENTS.md`, and a managed ignore rule for local execution state. It preserves existing application files, instructions, active work, IaC, and delivery ownership. It does not copy this framework's backlog into the application. See the [complete quickstart](guide/00-quickstart.md) and [adoption contract](docs/reference/bootstrap.md).

Before an application work item exists, check the installed layer from that application's root:

```sh
python3 .aws-workflow/scripts/workflow.py --root . doctor
```

No active work is expected immediately after adoption. This read-only check identifies package and mapping problems without calling a model or accessing AWS. Codex can then begin the consultation in your existing session.

For Codespaces, use the ordinary VS Code integrated terminal to check the selected native client's state before a native run. See [Codespaces readiness](guide/07-codespaces.md); native execution is optional for conversational delivery.

Open the application root in Codex and type **`start`** (or “Start my AWS project”). Codex should inspect readiness and context, welcome you on the first consultation, or resume saved work. The [conversation shortcuts](guide/00-quickstart.md#3-give-codex-the-outcome) also include `resume`, `status`, `feature`, `bugfix`, `review`, and `release`. These are natural-language requests, not shell commands or extra execution authority. You can also use the prompt above, followed by your idea. For example:

> I want an appointment service for three clinics. Patients book online and receive reminders. Please lead the consultation from here.

For an existing system:

> Assess this repository before proposing changes. Preserve our accepted architecture and deployment ownership. We need to prevent duplicate bookings. Establish the current behavior, ask about unresolved business rules, and plan the smallest supported change.

## What happens next

| Stage | Codex's responsibility | Durable result |
| --- | --- | --- |
| Discover | Inspect the brief, existing decisions, repository and handoff; distinguish observed facts from assumptions. | Existing context reused; adoption findings for brownfield work. |
| Interview | Ask up to three consequential questions per turn, recommend defaults, explain why answers matter, and save answers as the work develops. | Brief, unresolved questions, decision provenance. |
| Specify | Turn outcomes into observable behavior using structured requirements; analyze ambiguity, conflicts and missing cases. | Requirements or bugfix contract plus sourced analysis. |
| Design | Derive AWS choices, research material guidance, compare relevant alternatives, and cover costs, security, operations and recovery. | Design, correctness properties and significant decisions. |
| Plan | Connect every task to requirements, prerequisites, and a verification check. | One canonical task list and check matrix. |
| Deliver | Implement eligible tasks in the current session or an explicitly selected bounded run; verify the integrated candidate. | Source, tests, review and scoped evidence. |
| Continue | Reload saved answers and evidence; preview and reconcile changed inputs before relying on old conclusions. | Current handoff and next eligible work. |

Requirements-first and design-first routes review the two documents in their chosen order before task generation. A quick route produces the three connected artifacts together after necessary clarification. Bugfix work separates faulty, expected, and preserved behavior. Small understood edits stay proportionate. [Workflow contract](docs/reference/workflow-contract.md) · [Interview guide](guide/06-consultation-interview.md) · [Roleplays](examples/consultation/README.md)

## What is executable

| Component | Implemented responsibility |
| --- | --- |
| `scripts/bootstrap.py` | Preview and safely apply the reusable layer to greenfield or brownfield repositories. |
| Workflow CLI and engine | Create work, load context, check dependencies/traceability, record revision-bound reviews/evidence, and enforce applicable phase conditions. |
| `doctor` and `hooks` | Inspect setup before active work and preview the correct optional hook configuration. |
| `analyze` and `properties` | Prepare exact agent review requests; validate and retain actual sourced analysis/property responses. |
| `sync` | Preview changed-input impact; deliberately reopen affected work using the current preview fingerprint. |
| `run-plan`, `run`, and run management | Plan dependency waves, explicitly execute bounded tasks in Git worktrees, verify the combined candidate, and apply it against the expected original state. |
| `scripts/codex_hooks.py` | Read-only lifecycle context and completion reminders using documented Codex hook events. |
| `scripts/check_repository.py` | Check this bootstrap's required files and explicit local Markdown destinations. |

In an adopted project, Codex invokes the CLI at `.aws-workflow/scripts/workflow.py` with the application as `--root`. You can inspect the same record directly:

```bash
python3 .aws-workflow/scripts/workflow.py --root . context --compact
python3 .aws-workflow/scripts/workflow.py --root . status
python3 .aws-workflow/scripts/workflow.py --root . validate
```

The active work is selected in `.codex/workflow.json`; Markdown remains the human-readable contract and completion authority. Machine metadata references those documents instead of storing a second task checklist. New CLI work requires structured requirements, current analysis before contract acceptance, and mapped correctness properties before task-plan acceptance. Existing work is not silently migrated. See the [CLI reference](docs/reference/workflow-tooling.md) and [specification operations](docs/reference/specification-operations.md).

Analysis prepares a precise request; the reviewing agent supplies the semantic judgment and records its response. It does not produce a fictional analysis pass. Properties name observable behavior and the checks that will verify it; their existence does not claim those tests ran.

For optional native execution, Codex first derives `execution.json` from the accepted task plan. `run-plan` and `run` without `--execute` are previews. Explicit execution needs a clean committed Git project, a supported configured Codex CLI and actual authority for the model invocation. It uses separate candidate/worker worktrees, bounds attempts and time, runs declared checks, and preserves the original application until explicit application. Native process control currently targets Linux, macOS or WSL. [Execution contract](docs/reference/task-execution.md)

The compact view prioritizes current blockers and the next useful task, with source references and disclosed omissions. Startup context is capped at 6000 characters; prompt refresh at 1200. Full reports remain available. Efficiency is evaluated only after required quality, preservation and authority conditions pass; context size is measured separately from token cost and model performance. [Efficient operation](docs/reference/efficient-operation.md)

The template includes native hook definitions for its own checkout. The installer leaves an adopter's client configuration untouched. Hooks require support and review/trust on the selected client; [native integration instructions](docs/reference/native-hooks.md) explain the optional setup. Fixture tests establish adapter behavior, not that another user's client has loaded or trusted it.

## AWS integration

Reuse the existing official AWS Core and AWS Data Analytics plugins. Discover relevant official guidance on demand where available and allowed. Public consultation does not require account access. Actual account assessment or deployment follows the project's authorized targets, actions, cost limits, and existing delivery controls. No plugin, account access, infrastructure, or background service is installed by this template. [AWS guide](guide/02-aws-guidance-and-access.md) · [Delivery reference](docs/reference/aws-delivery.md)

## Working on the bootstrap

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/check_repository.py
```

The current delivery follows the [developer workflow execution plan](specs/0004-developer-workflow/exec-plan.md). Its [canonical tasks](specs/0004-developer-workflow/tasks.md) and [verification receipt](evidence/0004-developer-workflow/verification.md) identify completed implementation and any remaining behavioral trial. The [focused context](specs/0003-efficient-context/requirements.md) and [consultant workflow](specs/0002-consultant-workflow/requirements.md) retain the underlying contracts. The [original foundation](specs/0001-workflow-foundation/tasks.md) retains historical delivery and broader automation work.

The model conducts the interview, reasons about architecture, writes code and judges semantic quality. The code detects inconsistent records, stale conclusions and invalid execution outcomes. Offline tests use real temporary projects/processes with simulated model responses. Actual native-client behavior, hook activation and AWS delivery require separately observed trials; this source does not claim exact product equivalence or superior model performance. [Architecture](docs/workflow-architecture.md) · [Repository map](docs/repository-map.md) · [Remaining evidence](docs/implementation-plan.md)
