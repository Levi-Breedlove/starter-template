# Implementation priorities

The current slice moves deterministic workflow responsibilities into code. Its canonical checklist is [0002 consultant workflow](../specs/0002-consultant-workflow/tasks.md); the [original foundation backlog](../specs/0001-workflow-foundation/tasks.md) records broader ambitions and historical work. This roadmap does not maintain a duplicate checklist.

## Current slice

Adaptive interview procedures; saved fact and question provenance; route-specific review and phase validation; dependency and traceability checks; declared-input evidence freshness; safe greenfield/brownfield installation; and read-only native hook adapters. The current [verification receipt](../evidence/0002-consultant-workflow/verification.md) reports exactly what ran.

## Next useful work

| Priority | Deliverable | Why it matters | Acceptance evidence |
| --- | --- | --- | --- |
| 1 | Bounded real Codex trial on two disposable project fixtures | Determine whether actual consultation avoids repeated questions and creates useful requirements/tasks | Recorded input, client/model, artifacts, questions, corrections and independent review. |
| 2 | Selected-client hook and public official-toolkit trial | Establish installed/loaded/tested status beyond fixture correctness | Actual event observations and public responses without account access. |
| 3 | Existing-project mapping extension if required | Integrate an established tracker/layout without competing authority | Positive and conflicting mapping fixtures; user edits preserved. |
| 4 | Optional CI check in the project's existing pipeline | Make deterministic record validation repeatable at review time | Required check exercises actual candidate and fails seeded stale claims. |
| 5 | Bounded worker controller only when the project needs unattended multi-step execution | Persist attempts and reconcile interrupted operations | Fake-worker crash/retry/cap tests followed by a scoped client trial. |
| 6 | One authorized AWS release and recovery exercise | Establish real operational evidence | Named environment, candidate, service checks, recovery and cost/cleanup outcome. |

## Language recommendation

Keep the current Python implementation while validating behavior: it uses the standard library, is small enough to inspect, and has a stable CLI/JSON seam. Choose a compiled implementation when distribution as a single binary, concurrency, long-running reliability or measured performance creates a concrete need. Preserve the contracts and tests if the language changes. A port alone does not improve the model's requirements judgment or evidence honesty.

Avoid adding a daemon, dashboard or several execution interfaces before observing a real gap. The useful progression is deterministic core, actual behavioral trials, then justified orchestration. Native permissions, existing project controls and real user authority remain in force throughout.
