# Workflow procedures

These procedures guide Codex from consultation through verified delivery. The local CLI supports context, phase and evidence consistency; it does not replace the agent's judgment or the project's delivery controls. See [the workflow contract](../docs/reference/workflow-contract.md).

| Intent | Procedure | Main result |
| --- | --- | --- |
| Explore an idea or choose an architecture | [Consult](consult.md) | Saved answers, recommendations and a useful work scope. |
| Adopt an existing project | [Brownfield](brownfield.md) | Existing authority, baseline, preserved behavior and gaps. |
| Add or change behavior | [Feature](feature.md) | Connected requirements, design, tasks and evidence. |
| Correct a defect | [Bugfix](bugfix.md) | Current fault, expected behavior and preservation checks. |
| Continue after changed input | [Reconcile](reconcile.md) | Current artifacts and scoped evidence freshness. |
| Review a candidate | [Review](review.md) | Findings tied to the actual candidate and acceptance contract. |
| Prepare or execute an authorized release | [Release](release.md) | Concrete release readiness and actual operational results where executed. |
| Handle an incident | [Incident](incident.md) | Bounded response, observed recovery and follow-up work. |

Start with the user's desired outcome and existing facts. Recommend the route without making the user learn process labels. A rough idea calls for an adaptive interview; a detailed accepted specification should not trigger the same questions again. Ask at most three consequential unresolved questions at a time and persist each answer in its canonical source.

Requirements-first and design-first routes preserve their respective artifact review order. Quick work drafts the connected artifacts after necessary clarification without separate document gates. A planning request does not imply implementation authorization. Small understood changes may use proportionate direct work.

For structured work, [workflow.py](../docs/reference/workflow-tooling.md) creates and inspects the work record, checks phase changes, and projects eligible tasks from the canonical checklist. Codex should use it during the procedure rather than asking the user to operate every command. Existing trackers/layouts need an explicit authority mapping before adding a second work record.

Real review and acceptance evidence remain necessary at the project's required depth. A CLI record does not prove a review occurred, a test passed, or a cloud operation succeeded. Continue within already granted scope; pause only for a consequential unknown, unavailable capability or actual authority boundary. Keep the mapped handoff current when work pauses.
