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

WHEN <condition>, THE <named system> SHALL <observable correct result>.

Acceptance: <specific result demonstrating the correction>.

## Preservation contract

| ID | Behavior that must continue | Relevant evidence or acceptance |
| --- | --- | --- |
| KEEP-001 | WHILE <unaffected state>, THE <named system> SHALL CONTINUE TO <behavior>. | <checkable result> |
| KEEP-002 | WHEN <preserved interaction>, THE <named system> SHALL <accepted interface, security, data, or architecture behavior>. | <checkable result> |

## Investigation

| Hypothesis | Supporting or conflicting evidence | Next bounded check | Result |
| --- | --- | --- | --- |
| <candidate cause> | <facts, not certainty> | <check> | Not investigated |

Root cause: <unconfirmed / evidence-backed explanation>.

## Correction scope and readiness

Record the selected correction in [design.md](design.md) and its tasks and verification in [tasks.md](tasks.md). Include proof that the defect exists where practical, that the correction works, and that required preserved behavior remains valid.

If reproduction is unavailable, name the exact missing input or access and specify the best available check without claiming reproduction. Continue independent authorized investigation. An unrelated refactor or changed contract is a separate scope decision.

Use `analyze` to inspect the defect/correction/preservation set and record real findings, then `properties` to derive the reproduction, correction and preservation checks. A `DEF` entry records an observation and is not forced into a normative EARS sentence. Required `FIX` and `KEEP` behavior uses a supported EARS pattern for newly structured work. Choose generated-input tests where they add evidence; example, contract, integration or operational checks may fit other claims. See [specification operations](../docs/reference/specification-operations.md).
