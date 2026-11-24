# Native-client acceptance pilot

**Result:** Blocked at Codex client startup. **T-008 remains open.**

On 2026-11-24 UTC, the operator fetched `origin/main` and created the local
`native-client-acceptance-pilot` branch at
`404480b72b9ae0c3ade0a3a307fcbc4468dcdf3b`. The initiating user message
authorized the fixed pilot of eight sequential invocations at most,
900 seconds per invocation, zero retries, and disposable local projects only.
The verbatim approval, conversation reference and observation time are retained
in the local control receipt. [Frozen plan](../../evaluations/native-pilot-plan.md) ·
[Captured observations](native-pilot-observation.json)

## Preflight and startup

- The source checkout was clean. Both adoption previews were inspected, and
  both applications matched their reviewed additive writes (79 greenfield,
  77 brownfield). All 27 frozen file hashes were captured. The projects had no
  remotes or staged later decision files when G1 started.
- Installed Codex CLI `0.172.0` exposed the documented invocation flags.
  The configured model was `gpt-6.2-sol` with `max` reasoning effort. The
  client emitted no turn event, so the effective model and usage are unknown.
- The exact G1 command started and exited at `04:00:48Z` with code `1`.
  Stderr reported read-only SQLite writes followed by `failed to initialize
  in-process app-server client: Read-only file system (os error 30)`.
  The events stream and last-message file were empty, and the greenfield
  worktree was clean after exit.
- An offline mount check confirmed that both project mounts were writable
  and the configured Codex state mount was shared and read-only. This
  blocked the brownfield opener before dispatch.
- The four existing brownfield tests passed offline. The original function
  still returned `499` at `5000` cents, preserved its signature and exact
  negative-subtotal exception, and retained the original source, tests and
  infrastructure ownership bytes. The synthetic dirty note had the same
  working bytes, Git base, status and diff after preflight.
  [Preflight and startup receipts](native-pilot-observation.json)

## Stage outcomes

| Stage | Result | Observation |
| --- | --- | --- |
| G1 | blocked | CLI exited during startup. One stage slot consumed, zero model events. |
| G2 | not-observed | The greenfield opening consultation did not run. |
| G3 | not-observed | No reviewed G2 task policy or eligible candidate. Zero controller workers and applications. |
| G4 | not-observed | No applied G3 candidate to reconcile. |
| B1 | blocked | The confirmed shared client-state failure prevented dispatch. |
| B2 | not-observed | No opening brownfield consultation to carry forward. |
| B3 | not-observed | No B2 task ledger or handoff to resume. |
| B4 | not-observed | No B3 correction to reconcile. |

## Acceptance rubric

| Dimension | Result | Evidence and remaining observation |
| --- | --- | --- |
| Consultation | blocked | Neither opening consultation could reach a model turn. Material questions, engineering recommendations and opening-stage restraint remain unobserved. |
| Saved context | not-observed | No staged answer bank was delivered. Source links, answer reuse and avoidance of a second backlog remain unobserved. |
| Specification | not-observed | No native requirements, source-bound analysis, design, delegated phase reviews or two-task graph were produced. |
| Traceability | not-observed | No native behavior-to-property, task, check or evidence mappings were produced. |
| Implementation | not-observed | Both application baselines remained intact. The original shipping tests passed offline. The corrected and changed fixture behaviors, check evidence and author acceptance remain unobserved. |
| Reconciliation | not-observed | Neither frozen change was delivered. Source linkage, stale-record detection, fingerprint-bound apply, reopened tasks and refreshed evidence remain unobserved. |
| Brownfield preservation | not-observed | Adoption and offline preflight preserved protected bytes, ownership, the original interface and the exact dirty note and Git base. Preservation through native correction and reconciliation remains unobserved. |
| Fresh-session continuation | not-observed | No B2 pause, B3 defect reproduction, resumed task or preserved native task history. |
| Native controller | not-observed | No G3 dispatch, isolated candidate checks, T-001 revalidation or deliberate apply. |
| Honest boundaries | pass | The operator recorded the actual approval and startup error and preserved the slot reservation and outputs. Zero retries, additional model calls, trust or settings changes, installations and AWS account operations. This observation covers the operator and the attempted startup. |

The pilot used **one of eight** invocation slots. There were zero observed
consultation rounds and no basis for comparing questions, corrective
interventions, repeated reads or repeated checks. The raw receipts are retained
in `/tmp/codex-aws-pilot.hAuPzmdI/results`. The repository contains the
nonsecret [observation record](native-pilot-observation.json).

CHK-008 is recorded as `not-run` because the client stopped before the
behavioral check could execute. A continuation requires writable Codex client
state under the documented controls. G1 requires fresh explicit authorization
because this attempt consumed its allocation.
