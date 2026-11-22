# Bugfix analysis: <work ID and title>

**State:** Draft; cause and correction unverified.
**Observed source/environment:** <exact known revision and environment, or unknown>
**Evidence:** <reproduction or diagnostic reference>

## DEF-001 — Observed defect

- Trigger and reproduction steps: <inputs, sequence, and relevant conditions>.
- Actual result: <observed behavior; distinguish reports from reproduced facts>.
- Impact and scope: <affected users or components>.
- Frequency and uncertainty: <what is known and unknown>.

## FIX-001 — Expected correction

When <condition>, the system must <observable correct result>.

Acceptance: <specific result demonstrating the correction>.

## Preservation contract

| ID | Behavior that must continue | Relevant evidence or acceptance |
| --- | --- | --- |
| KEEP-001 | Under <unaffected condition>, the system continues to <behavior>. | <checkable result> |
| KEEP-002 | <accepted interface, security control, data behavior, or architecture constraint> | <checkable result> |

## Investigation

| Hypothesis | Supporting or conflicting evidence | Next bounded check | Result |
| --- | --- | --- | --- |
| <candidate cause> | <facts, not certainty> | <check> | Not investigated |

Root cause: <unconfirmed / evidence-backed explanation>.

## Correction scope and readiness

Record the selected correction in [design.md](design.md) and its tasks and verification in [tasks.md](tasks.md). Include proof that the defect exists where practical, that the correction works, and that required preserved behavior remains valid.

If reproduction is unavailable, name the exact missing input or access and specify the best available check without claiming reproduction. Continue independent authorized investigation. An unrelated refactor or changed contract is a separate scope decision.
