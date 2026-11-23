# Implementation priorities

The current slice improves focused context and makes efficiency measurable. Its canonical checklist is [0003 focused context](../specs/0003-efficient-context/tasks.md); [0002 consultant workflow](../specs/0002-consultant-workflow/tasks.md) retains the underlying implementation scope; the [original foundation backlog](../specs/0001-workflow-foundation/tasks.md) records broader ambitions and historical work. This roadmap does not maintain a duplicate checklist.

## Current slice

The existing consultation, state/evidence tooling and safe adoption remain. The current slice adds one bounded action-oriented context projection, a smaller fingerprint refresh for each prompt, and a quality-first operating/evaluation policy. The current [verification receipt](../evidence/0003-efficient-context/verification.md) reports actual payload measurements and regression results separately from future model trials.

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
