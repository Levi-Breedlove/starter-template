# Implementation priorities

The current delivery follows the [complete developer workflow execution plan](../specs/0004-developer-workflow/exec-plan.md). Its [canonical tasks](../specs/0004-developer-workflow/tasks.md) own completion. [Focused context](../specs/0003-efficient-context/tasks.md) and [consultant workflow](../specs/0002-consultant-workflow/tasks.md) retain the underlying contracts; the [original foundation backlog](../specs/0001-workflow-foundation/tasks.md) records broader ambitions and historical work. This roadmap does not maintain a duplicate checklist.

## Current slice

The implementation adds setup checks before active work, a complete developer quickstart, explicit structured requirements, recorded semantic analysis and properties, deliberate reconciliation and a bounded foreground task controller. The installer includes the complete reusable runtime and preserves existing application authority. The current [verification receipt](../evidence/0004-developer-workflow/verification.md) states actual regression and review scope.

The source is usable for ordinary Codex-session consultation and delivery. Native execution is implemented and exercised with fake model backends in real temporary Git/process environments. A selected real native client must still demonstrate its behavior before the corresponding acceptance item can close. This distinction stays visible in the canonical tasks and [prepared pilot plan](../evaluations/native-pilot-plan.md).

## Next useful work

| Priority | Deliverable | Why it matters | Acceptance evidence |
| --- | --- | --- | --- |
| 1 | Execute the prepared, separately approved native pilot | Observe actual consultation, useful specifications/tasks, reconciliation and resume | Frozen inputs, actual client/model, artifacts, questions, checks, corrections and fresh review. |
| 2 | Selected-client hook and public official-toolkit trial | Establish installed/loaded/tested status beyond fixture correctness | Actual event observations and public responses without account access. |
| 3 | Existing-project mapping extension if required | Integrate an established tracker/layout without competing authority | Positive and conflicting mapping fixtures; user edits preserved. |
| 4 | Optional CI check in the project's existing pipeline | Make deterministic record validation repeatable at review time | Required check exercises actual candidate and fails seeded stale claims. |
| 5 | Further orchestration only if a measured project need remains after the foreground runner | Avoid adding a service before its operational need is demonstrated | Explicit event/recovery/usage contract and real scenario evidence. |
| 6 | One authorized AWS release and recovery exercise | Establish real operational evidence | Named environment, candidate, service checks, recovery and cost/cleanup outcome. |

## Language recommendation

Keep the Python implementation: it uses the standard library, is inspectable, and has a stable CLI/JSON seam. It now implements the requested deterministic mechanics, including bounded worker coordination. Choose a compiled implementation when distribution as a single binary or measured runtime requirements justify the migration. Preserve contracts and failure tests if the language changes. A port alone does not improve the model's requirements judgment or evidence honesty.

The next useful investment is observed behavior on the frozen fixtures. Native permissions, existing project controls and real user authority remain in force throughout. Actual AWS releases remain project-specific work with named targets and operational evidence.
