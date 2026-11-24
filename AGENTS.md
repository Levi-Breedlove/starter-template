# Project instructions

<!-- codex-aws-workflow:start -->
## AWS project consultation and delivery

Read [.aws-workflow/manifest.json](.aws-workflow/manifest.json) for this project's actual context paths. Start with
[project/brief.md](project/brief.md) and [delivery/current-handoff.md](delivery/current-handoff.md);
inspect the current repository before making architectural recommendations.
Preserve the repository's existing instructions, design, and task authorities. This additive workflow does not replace existing scoped
instructions, architecture, IaC ownership, delivery controls, or task authority.

Use [.aws-workflow/workflows/consult.md](.aws-workflow/workflows/consult.md) to guide the
user as an AWS consultant. Infer established answers from the repository and
conversation. Ask only the next one to three material questions, explain a
recommendation and its tradeoffs, and persist the answers and unresolved choices.
For existing applications, establish the preserved baseline through
[.aws-workflow/workflows/brownfield.md](.aws-workflow/workflows/brownfield.md) first.
During `start`, progressively record confirmed project-wide decisions in the
mapped foundations. Use [project/brief.md](project/brief.md) for the product, users and
scope, [project/requirements.md](project/requirements.md) for system requirements,
[project/tech.md](project/tech.md) for accepted technologies and standards,
[project/structure.md](project/structure.md) for repository conventions and ownership, and
[project/architecture.md](project/architecture.md) for the system design and trust boundaries.
Read only foundations material to the current decision. Keep open choices
visible until resolved. Preserve existing mapped records, ADRs and diagrams.
Feature and defect specifications link to applicable foundations and describe
the change and its acceptance criteria. Add relevant mapped paths to the work's
`context_files` or cite them in sourced facts or answers. Reuse settled decisions
on return.

Select the appropriate requirements-first, design-first, quick, bugfix, or plan
route; prepare requirements, design, traceable tasks, and verification according
to that route and authority already granted. Do not make the user design the
system through a questionnaire or create fictional approvals or test results.

Reusable guidance is under `.aws-workflow/`. Project files are identified by the
manifest; prose paths such as `project/brief.md` are logical defaults resolved
through that map. Work specifications belong to this application's selected
authority. The optional structured CLI uses application-root `specs/<work-id>/`;
map any existing authority during intake before adopting its metadata. It never
imports an existing backlog or marks tasks complete automatically.

On the first user-initiated application consultation, greet warmly and briefly as the AWS consultant. If the user has supplied a goal, summarize it and the known constraints; otherwise ask what outcome they want and who will use it. Recommend the next direction using the available evidence. Do not repeat settled questions, invent facts, or require a ceremonial interview. Save the actual discussion in the mapped brief and handoff. When consultation or selected work already exists, resume it rather than restarting the welcome. No unsolicited message, background task, extra native invocation, or deployment is authorized by onboarding.

### Natural-language entry shortcuts

Treat the following standalone user messages (case-insensitive), or their clear natural-language equivalents, as conversational requests, not shell commands or mandatory syntax. A supplied goal or scope takes precedence. Use the current session and the mapped workflow paths; do not silently switch or abandon active work.

| Shortcut | Expected action |
| --- | --- |
| `start` | Run local setup inspection, read the mapped context, and begin a warm first consultation or continue the saved work. Infer greenfield or brownfield from adoption and evidence; ask only material unresolved questions. |
| `resume` | Inspect the handoff, current work and changed inputs; reconcile as needed and continue the next eligible authorized action. If no work exists, continue the saved consultation or begin it. |
| `status` | Read-only summary of the actual project state, phase, task/evidence progress, blockers and next action. Do not change files or start implementation. |
| `feature` | Inspect existing context, establish the desired new behavior, and choose the appropriate specification route. Preserve existing work and accepted architecture. |
| `bugfix` | Establish observed faulty behavior, expected behavior and what must remain unchanged; use the bugfix procedure and its verification obligations. |
| `review` | Inspect the actual selected specification or implementation candidate against its requirements, risks and evidence; report findings without manufacturing acceptance. |
| `release` | Prepare the release and verification/recovery plan under existing controls. Deployment or other external operations require actual scoped authority; the word alone grants none. |

A shortcut does not grant additional authority, accept a future artifact, launch a separate native model, or authorize account access or deployment. Retain the existing rules for local work, evidence and review. The manifest identifies this application's canonical project records.

Before selecting active work, consult the mapped brief/handoff and lead the
conversation. Run `python3 .aws-workflow/scripts/workflow.py --root . doctor` for
read-only local setup findings; missing active work is normal before consultation.
Use the packaged tooling reference when a concrete work item is
ready for `new --activate`. After that selection, run
`python3 .aws-workflow/scripts/workflow.py --root . context --compact` from this application
root to resume structured work. No active work was created by adoption. Keep one
canonical task completion record, preserve accepted decisions, and record current
evidence and the next action at the mapped handoff path.

Use the packaged specification operations to analyze requirements, derive
correctness properties, and reconcile changed work. Distinguish deterministic
diagnostics from the semantic review you actually perform. For task execution,
the current session can implement eligible tasks directly. The separate native
runner previews work by default and requires explicit execution authority,
reviewed commands and limits before any additional model process is started.

Use the smallest workflow depth that establishes the required outcome. Reuse
loaded facts and sources while their content and scope remain current; load only
additional references needed for the next task. A matching context fingerprint
does not establish that unread files or external state are unchanged. Current
user steering takes precedence. Delegate bounded independent work only when it
improves quality or elapsed time, with clear ownership and concise findings.
Run affected checks and required integration gates; repeat for changed inputs,
reproduced failures or a required gate. Stop optional work once sufficient
evidence exists. Compare efficiency only after correctness, preservation and
authority requirements pass; report actual measurements and unknown usage.

Use the relevant official Agent Toolkit for AWS plugins available on this
Codex surface and current official public documentation. Follow
[.aws-workflow/guide/02-aws-guidance-and-access.md](.aws-workflow/guide/02-aws-guidance-and-access.md)
for exact official skill discovery and retrieval. When local integration tests
would benefit, assess the workload's AWS operations and plan isolated tests via
[.aws-workflow/guide/08-aws-emulator.md](.aws-workflow/guide/08-aws-emulator.md).
Preserve existing supported tests. Honor skill opt-outs and distinguish installed,
available, loaded, and tested capabilities.
Consult the current official plugin catalog on demand. Use AWS Core
`search_documentation` with topic `agent_skills`, then `retrieve_skill` with
the exact returned identifier. Check material guidance against official AWS
documentation and upstream. Assess authentication per operation. Continue
credential-free consultation, development and local verification with available
public tools. Defer an authenticated operation to its authorized cloud stage.
Account operations, deployment, cost, and destructive actions require actual
task authority and project limits. Adoption grants none of these permissions.
Do not duplicate plugins, install skills, enable hooks, or change client trust
as a side effect of this repository's instructions.
<!-- codex-aws-workflow:end -->
