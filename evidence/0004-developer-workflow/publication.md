# Publication: developer workflow

**Observed result:** Expected-head source publication and complete remote-tree
readback passed. Observation time: 2026-11-23 08:26:03 UTC.

| Identity | Observed value |
| --- | --- |
| Expected parent | `200016c62f10fe1a7eb164584f3b7ab794450a41` |
| Published source commit | `491aafc276d268eab443c5be9547ad902a16bf0b` |
| Published source tree | `019d9fd83a062b3f973495e5db102a0227654782` |
| Branch | `main` |
| Files compared | 147 |
| Missing, extra or mismatched paths/modes/blob identities | 0 |
| Tree truncation | False |
| Repository visibility | Private, preserved |

The integrator compared the prepared candidate tree against every local file
identity before moving the branch. The branch update used the exact expected
parent and `force: false`. After the update succeeded, the integrator reread the
branch, full recursive tree and repository visibility. All 147 file paths, modes
and Git blob identities matched the prepared source snapshot.

## Local source checks

The [source-check observation](source-checks.json) records the actual prepublication
scan: 105 Markdown files, 395 explicit local links, 31 required core paths, zero
link/structure issues, zero prohibited-name findings in current relative paths or
text, and no changed tested executable/fixture identity. That observation scanned
146 existing files before writing its own receipt, which became the 147th file.

The [aggregate observation](run-observation.json) and [independent review](review.md)
identify the tested/reviewed source. Publication proves delivery of those bytes;
it does not upgrade fake model fixtures into actual native/client/AWS results.

## Completion records and freshness

This receipt is written after the observed source publication. The following
records-only commit updates task/evidence state, the verification summary and
handoff. Tested executable and fixture identities stay unchanged. Its complete
remote tree is compared again during final delivery; its own identifier is
reported externally to avoid a self-referential commit claim.

The source publication checks in the consultant/context slices are reconciled to
this new actual observation. Historical receipts remain unchanged. Current input
snapshots exclude mutable active selection, work metadata, task progress, handoff
and verification summary so completion-record updates do not invalidate the
source observation they document. Exact full-tree comparisons still include those
files at each observed revision.

T-007 records completed source delivery. T-008 remains unchecked and blocked on
actual approval and observation of the [native pilot](../../evaluations/native-pilot-plan.md).
No real model invocation, AWS account/resource operation, trust change, plugin
installation or repository visibility change occurred in this delivery.
