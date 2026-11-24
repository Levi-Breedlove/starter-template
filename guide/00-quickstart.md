# Quickstart: your first AWS project

Use this bootstrap to give Codex a persistent consulting and specification workflow.
Describe an outcome, answer the consequential gaps, and review the first useful
delivery. Local tools keep the resulting records connected as work proceeds.

## 1. Choose the application directory

Keep the bootstrap checkout separate from the application. Python 3.10 or newer
is required; the local tools use the standard library. You need a Codex surface
that can read application files and run its permitted local commands.

| Starting point | Choose |
| --- | --- |
| An absent or empty application directory | `--mode greenfield` |
| An existing application, IaC repository or populated directory | `--mode brownfield` |

From the bootstrap checkout, preview the installation. Use an absolute target
path whose parent exists:

```sh
python3 scripts/bootstrap.py --source . --target /absolute/path/my-aws-app --mode greenfield
```

Inspect the proposed additions and preserved files, then apply the intended plan:

```sh
python3 scripts/bootstrap.py --source . --target /absolute/path/my-aws-app --mode greenfield --apply
```

For brownfield work, change the mode and target. Existing architecture,
instructions, source, state and pipelines stay in place. Use explicit mappings
when the current brief, handoff or task authority lives elsewhere.
[Adoption details](../docs/reference/bootstrap.md)

The application receives `.aws-workflow/`, a bounded addition to `AGENTS.md`, and
a managed `.gitignore` block for local execution state. No active application
specification, AWS account access, plugin installation or hook trust is created.

## 2. Open the application in Codex and check local setup

Open the adopted application root in Codex. The `start` prompt in the next
step directs Codex to run the read-only setup check. For manual diagnosis, use:

```sh
python3 .aws-workflow/scripts/workflow.py --root . doctor
```

`doctor` inspects required runtime/guidance files, mapped records, instructions and any active
selection. Optional executable presence is separate from actual native execution
or AWS integration. A missing active work item is normal after adoption; begin
consultation before creating one. Missing optional Codex CLI or native hooks does
not prevent using the workflow in the current agent session.

The command does not run programs, inspect credentials, authenticate, call a model
or access AWS. The selected client's instruction loading and tool availability
still need actual observations. [AWS setup boundary](02-aws-guidance-and-access.md)

For GitHub Codespaces, use the [Codespaces readiness guide](07-codespaces.md). The separate native-check command tests observable startup prerequisites from the terminal that will launch Codex; this is not required for ordinary in-session consultation.

## 3. Give Codex the outcome

For either a new or an existing application, type **`start`** (or say “Start my AWS project”). Codex should offer a brief welcome as your AWS consultant and lead with known context or ask for the desired outcome. If saved consultation or work already exists, it should resume instead of restarting. No model call is started automatically by installation or setup.

Use these optional conversational shortcuts directly in Codex:

| Shortcut | Expected action |
| --- | --- |
| `start` | Run local setup inspection, read the mapped context, and begin a warm first consultation or continue the saved work. Infer greenfield or brownfield from adoption and evidence; ask only material unresolved questions. |
| `resume` | Inspect the handoff, current work and changed inputs; reconcile as needed and continue the next eligible authorized action. If no work exists, continue the saved consultation or begin it. |
| `status` | Read-only summary of the actual project state, phase, task/evidence progress, blockers and next action. Do not change files or start implementation. |
| `feature` | Inspect existing context, establish the desired new behavior, and choose the appropriate specification route. Preserve existing work and accepted architecture. |
| `bugfix` | Establish observed faulty behavior, expected behavior and what must remain unchanged; use the bugfix procedure and its verification obligations. |
| `review` | Inspect the actual selected specification or implementation candidate against its requirements, risks and evidence; report findings without manufacturing acceptance. |
| `release` | Prepare the release and verification/recovery plan under existing controls. Deployment or other external operations require actual scoped authority; the word alone grants none. |

These are not terminal commands. No shortcut grants additional authority or starts an extra model invocation. Existing work and instructions remain authoritative.

For a more specific start:

> I want to deliver [outcome] on AWS for [users]. Lead the consultation, inspect
> the existing project context, and recommend the technical approach. Save our
> decisions, ask only consequential unanswered questions, and prepare the first
> useful delivery. Keep this initial scope to planning and authorized local work.

For an existing project:

> We need [change] in this project. Inspect the current implementation, tests,
> infrastructure and delivery process first. Preserve the accepted architecture
> and interfaces. Ask about unresolved business rules, recommend the smallest
> supported change, and continue the local work I have authorized.

Codex should explain what it understands, recommend a direction and ask no more
than three consequential questions in a round. It should reuse settled answers.
You provide business intent and material choices; Codex investigates the technical
implications. [Consultation guide](06-consultation-interview.md)

## 4. Follow the work as the artifacts develop

| Stage | Codex's next useful action | Durable result |
| --- | --- | --- |
| Intake | Inspect known context and establish the existing baseline. | Mapped brief, adoption findings and capability observations. |
| Consultation | Recommend, ask material gaps and save answers. | Decisions, assumptions, open questions and first delivery scope. |
| Requirements | Draft observable behavior and analyze gaps/conflicts. | `specs/<work-id>/requirements.md`, or `bugfix.md`. |
| Design | Explain components, properties, costs, security, operations and recovery. | `design.md` and significant decisions. |
| Tasks | Connect outcomes to requirements, prerequisites and checks. | `tasks.md`; its checkboxes own completion. |
| Delivery | Implement eligible work and verify the actual candidate. | Source, tests, scoped evidence and reviews. |
| Continuation | Reconcile changed inputs and save the next action. | Current handoff and workflow metadata. |

Codex chooses requirements-first, design-first, quick, bugfix or planning-only
from the work. It records actual reviews and uses existing delegated authority;
routine steps do not need repeated permission. Costs and runbooks become
project-specific as design and implementation establish their real inputs.

The CLI `new` operation creates a consultation draft. Codex writes the substantive
documents through the interview; draft placeholders are not accepted requirements.
Analysis and properties operations provide explicit review requests and validate
recorded responses, with semantic findings supplied by the actual reviewing agent.
[Specification operations](../docs/reference/specification-operations.md)

## 5. Choose how eligible tasks execute

The current Codex session can implement tasks directly using its available tools.
For a separately authorized batch, the native runner offers a preview and a
bounded execution path. Review task scopes, commands, limits and the authority
record before native execution, which can consume model credits.

Native execution also needs a supported Codex CLI, a clean committed Git project
and effectively ignored runtime state. It uses isolated candidates and preserves
the original application until its explicit apply step. See [task execution](../docs/reference/task-execution.md)
for implemented commands, preflight, failure handling and candidate review.
Generated execution configuration does not establish spending or AWS authority.

## 6. Resume and release at the right boundary

After selecting work, these read-only commands expose its current state:

```sh
python3 .aws-workflow/scripts/workflow.py --root . context --compact
python3 .aws-workflow/scripts/workflow.py --root . status
python3 .aws-workflow/scripts/workflow.py --root . validate
```

At the next session, say: “Read the handoff, inspect changed state and continue the
next eligible task.” Codex should reuse saved answers and reconcile affected
evidence. An uncertain external operation needs status inspection before replay.

For AWS delivery, establish the target, release identity, permissions, cost limits,
pipeline and recovery procedure. Use existing release controls and verify the
user-facing behavior after deployment. Local checks do not establish live AWS
behavior. [Release guide](04-maintain-and-release.md)

## Optional native hooks

Preview the correct source or adopted-project configuration:

```sh
python3 .aws-workflow/scripts/workflow.py --root . hooks --json
```

The result contains a `configuration` object and reports whether an existing
project configuration is equivalent or needs a merge. It writes nothing. Review
the handler, merge only missing definitions into one chosen configuration source,
and use the supported client trust flow. The conversational workflow can start
before this optional setup. [Native hooks](../docs/reference/native-hooks.md)

## Common first-use findings

| Finding | Smallest useful action |
| --- | --- |
| No active work | Start consultation; create and activate work after understanding its scope. |
| Missing or changed runtime or required guidance | Inspect the package and perform an explicit restoration or reviewed update. |
| Existing task authority uses a different layout | Map that authority before introducing structured work. |
| A package update or managed-file edit blocks rerun | Compare a fresh installation and merge deliberately; there is no force overwrite. |
| Native preflight rejects a dirty project | Preserve changes and create the intended reviewed commit; never stash or discard them automatically. |
| AWS plugin availability is unresolved | Check the existing official identity on the chosen surface using public guidance only. |

Begin with one bounded feature or correction and retain its actual observations.
The [evaluation protocol](../evaluations/README.md) separates implementation tests,
real consultation quality, native integration and authorized AWS outcomes.
