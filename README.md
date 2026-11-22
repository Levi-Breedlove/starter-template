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

Review the proposed files, then repeat with `--apply`. For an existing application use `--mode brownfield`. The installer adds a reusable `.aws-workflow/` layer and a bounded block in `AGENTS.md`; it preserves existing application files, instructions, active work, IaC, and delivery ownership. It does not copy this framework's backlog into the application. See [bootstrap behavior](docs/reference/bootstrap.md) for collision checks and reruns.

Open the application root in Codex and use the prompt above, followed by your idea. For example:

> I want an appointment service for three clinics. Patients book online and receive reminders. Please lead the consultation from here.

For an existing system:

> Assess this repository before proposing changes. Preserve our accepted architecture and deployment ownership. We need to prevent duplicate bookings. Establish the current behavior, ask about unresolved business rules, and plan the smallest supported change.

## What happens next

| Stage | Codex's responsibility | Durable result |
| --- | --- | --- |
| Discover | Inspect the brief, existing decisions, repository and handoff; distinguish observed facts from assumptions. | Existing context reused; adoption findings for brownfield work. |
| Interview | Ask up to three consequential questions per turn, recommend defaults, explain why answers matter, and save answers as the work develops. | Brief, unresolved questions, decision provenance. |
| Specify | Turn outcomes into observable behavior, edge cases, constraints, and acceptance criteria. | Requirements or bugfix contract. |
| Design | Derive AWS choices, research material guidance, compare relevant alternatives, and cover costs, security, operations and recovery. | Design and significant decision records. |
| Plan | Connect every task to requirements, prerequisites, and a verification check. | One canonical task list and check matrix. |
| Deliver | Implement eligible tasks, run meaningful checks, reconcile changes, review the actual candidate, and prepare any authorized release. | Source, tests, review and scoped evidence. |
| Continue | Reload the active work and its evidence; expose stale or missing records before making claims. | Current handoff and next eligible work. |

Requirements-first and design-first routes review the two documents in their chosen order before task generation. A quick route produces the three connected artifacts together after necessary clarification. Bugfix work separates faulty, expected, and preserved behavior. Small understood edits stay proportionate. [Workflow contract](docs/reference/workflow-contract.md) · [Interview guide](guide/06-consultation-interview.md) · [Roleplays](examples/consultation/README.md)

## What is executable

| Component | Implemented responsibility |
| --- | --- |
| `scripts/bootstrap.py` | Preview and safely apply the reusable layer to greenfield or brownfield repositories. |
| `scripts/workflow.py` and `workflow_engine/` | Create work, reload context, report status, validate dependencies and traceability, record revision-bound reviews and evidence, and check phase advancement. |
| `scripts/codex_hooks.py` | Read-only lifecycle context and completion reminders using documented Codex hook events. |
| `scripts/check_repository.py` | Check this bootstrap's required files and explicit local Markdown destinations. |

In an adopted project, Codex invokes the CLI at `.aws-workflow/scripts/workflow.py` with the application as `--root`. You can inspect the same record directly:

```bash
python3 .aws-workflow/scripts/workflow.py --root . context
python3 .aws-workflow/scripts/workflow.py --root . status
python3 .aws-workflow/scripts/workflow.py --root . validate
```

The active work is selected in `.codex/workflow.json`; Markdown remains the human-readable contract and completion authority. Machine metadata references those documents instead of storing a second task checklist. See the [CLI reference](docs/reference/workflow-tooling.md).

The template includes native hook definitions for its own checkout. The installer leaves an adopter's client configuration untouched. Hooks require support and review/trust on the selected client; [native integration instructions](docs/reference/native-hooks.md) explain the optional setup. Fixture tests establish adapter behavior, not that another user's client has loaded or trusted it.

## AWS integration

Reuse the existing official AWS Core and AWS Data Analytics plugins. Discover relevant official guidance on demand where available and allowed. Public consultation does not require account access. Actual account assessment or deployment follows the project's authorized targets, actions, cost limits, and existing delivery controls. No plugin, account access, infrastructure, or background service is installed by this template. [AWS guide](guide/02-aws-guidance-and-access.md) · [Delivery reference](docs/reference/aws-delivery.md)

## Working on the bootstrap

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/check_repository.py
```

The current implementation is specified in [consultant workflow work](specs/0002-consultant-workflow/requirements.md); its [tasks](specs/0002-consultant-workflow/tasks.md) and [verification receipt](evidence/0002-consultant-workflow/verification.md) state the tested scope. The [original foundation](specs/0001-workflow-foundation/tasks.md) retains historical delivery and broader, unfinished automation work.

The model still conducts the interview, reasons about architecture, writes code and judges semantic quality. Deterministic tools catch record inconsistencies and stale claims; they cannot prove that a requirement is wise, that an observation is truthful, or that a workload works in AWS. Durable autonomous scheduling and real client/cloud trials remain separate work. [Architecture](docs/workflow-architecture.md) · [Repository map](docs/repository-map.md) · [Next implementation work](docs/implementation-plan.md)
