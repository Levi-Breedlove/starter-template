# Start an AWS project

For the shortest complete installation-to-first-task path, begin with the
[quickstart](00-quickstart.md). This guide explains the decisions behind that path.

Describe the outcome you want. Codex should inspect existing context, lead a focused consultation, recommend an approach, and develop requirements, design, and tasks. You should not need to arrive with a completed specification or choose AWS services before the engineering assessment.

There are two entry paths. Greenfield work establishes a new product and architecture. Brownfield work starts from the system's evidence and preserves its accepted architecture, source layout, IaC ownership, and delivery controls. Both use the same implementation, verification, and release loop.

## 1. Open the application

For a new repository created with **Use this template**, open its GitHub
Codespace, open Codex at the repository root and type `start`. The installed
instructions and manifest identify the project records. For an existing
application, preview and apply the additive installer to that application, then
open its root in Codex. Preserve its instruction hierarchy, source, IaC,
pipeline and task authorities. [Quickstart](00-quickstart.md) · [Brownfield adoption](05-brownfield-adoption.md)

## 2. Start with an ordinary request

A standalone `start` is sufficient. You may also include the outcome in your first message.

For a new application:

> I want to build [outcome] on AWS. Inspect what is here, consult with me on the material gaps, recommend an approach, and create the first implementation plan. Ask a few useful questions at a time and save our decisions. Keep this to planning and local work for now.

For an existing application:

> Add [outcome] to this project. Read the existing requirements, code, tests, infrastructure, and pipeline first. Keep the accepted architecture. Interview me only about decisions that the repository and existing requirements do not answer, then create the appropriate work specification and continue the implementation I have authorized.

Codex reads the mapped brief, handoff, instructions, and actual repository before responding. Its first useful answer explains what it understands, its provisional recommendation, and the next one to three consequential questions, if any. It records answers as the discussion develops. See [the consultation guide](06-consultation-interview.md).

## 3. Establish context and capabilities

Use the manifest to find the project brief, overall requirements, technology choices, repository structure, architecture and handoff. Update the relevant foundation when a decision is made. Feature and defect specifications link to shared decisions and describe their own changes. Preserve existing mapped brownfield records.

Record available tools and verification environments using the [environment capabilities template](../templates/environment-capabilities.md). Use [AWS guidance and access](02-aws-guidance-and-access.md) for official Agent Toolkit for AWS guidance. Capability inspection and public research do not require account access. Preserve the user's existing skill preferences and plugin installations.

Local and hosted Codex environments may expose different tools. Record what is actually available, installed, loaded, and tested. Explain the smallest missing setup step if a necessary capability is unavailable.

Run `python3 .aws-workflow/scripts/workflow.py --root . doctor` for read-only local
setup findings. It works before active work exists. Optional executable presence
is separate from login, native execution, hook trust/loading and AWS tool behavior;
the command performs no subprocess or credential probe.

## 4. Create a focused work item

Codex can handle a small, understood change directly. For scoped specification work it chooses requirements-first, design-first, quick, bugfix or planning-only based on the requested outcome. The local workflow CLI provides a durable skeleton and structural state checks; Codex conducts the interview, writes the substantive specification, and performs the reviews.

From an adopted application root, an initial work item can be created with:

```bash
python3 .aws-workflow/scripts/workflow.py --root . new 0100-first-capability --title "First capability" --mode greenfield --route requirements-first --idea "Describe the intended outcome" --activate
python3 .aws-workflow/scripts/workflow.py --root . context --compact
```

Inside the bootstrap itself, the equivalent tool path is `scripts/workflow.py`. Do not create a second work item when the current handoff already identifies the work to resume. The [first-feature guide](03-first-feature.md) explains the planning routes and reviews.

## 5. Begin implementation when ready

A first task is ready when its required behavior is clear, the design and dependencies support it, the relevant reviews have occurred, and implementation is within existing authority. Define the evidence needed before coding. Keep AWS-dependent checks pending until the authorized environment is available; an emulator cannot establish live service behavior.

Continue already authorized work without asking permission for each file. If the request is planning only, finish with a reviewable scope, design, task graph, and exact continuation point. Later use [maintenance and release](04-maintain-and-release.md) for the actual pipeline and deployment boundary.
