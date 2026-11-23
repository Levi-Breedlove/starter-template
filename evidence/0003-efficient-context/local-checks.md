# Local checks: focused context and efficient operation

**Observed UTC interval:** 2026-11-23T05:26:49.597354+00:00 to 2026-11-23T05:26:52.721622+00:00.  
**User-local date:** 2026-11-22, America/Los_Angeles.  
**Environment:** Python 3.12.14; local Linux; standard library; temporary fixture projects.  
**Candidate:** Published base `851505af9f54916da60fd8d4922eaddddedf38e5` plus the exact executable and fixture SHA-256 identities in [run-observation.json](run-observation.json). This candidate was not yet published when these commands ran.

## Observed results

The aggregate command `python3 -m unittest discover -s tests -p 'test_*.py' -v` passed **105 tests**: 44 workflow, 20 bootstrap, 15 context, 10 hook, 14 repository-checker and 2 actual-source integration tests. See the complete [test output](local-tests.txt).

| Scope | Actual procedure and result |
| --- | --- |
| Current CHK-001 | Context/CLI/hook fixtures exercise serialized budgets, escaped Unicode, oversized titles and paths, retained errors, omission counts, task references, fingerprint changes in omitted records, quick/design-first/planning states, full-report compatibility and read-only events. Passed. |
| Current CHK-002 | Root review of root/generated operating policy and related guidance, 20 bootstrap fixtures and 2 actual-source integration tests. Greenfield/brownfield packages include the projection, preserve existing files/configuration, work from a nested directory, resolve mapped context and reject a missing runtime module before target writes. Passed. |
| Current CHK-003 local portion | Combined 105-test run and frozen prior/current renderer comparison. Exact fixture/output identities are linked below. Source naming/links and publication readback are recorded in the separate publication receipt. |
| Earlier consultant CHK-001 | Root reviewed the changed entry/interview/tooling/efficiency guidance against the unchanged consultation contract and prior document findings. Accepted decisions, adaptive questions, recommendation-led consultation, real authority and one completion record remain consistent. This is document consistency evidence, not a model consultation trial. |
| Earlier consultant CHK-002 | All 44 existing workflow fixtures pass with the new shared module and CLI; 15 context fixtures additionally establish the bounded projection without replacing the full inspection contract. |
| Earlier consultant CHK-003 | The current actual-source adoption integration and bootstrap suite pass with the updated required runtime module, compact entry and generated policy. Prior adoption receipts remain historical; this receipt supports the current source. |
| Earlier consultant CHK-004 | All 10 hook fixtures and packaged-event integration pass. Startup and prompt have different bounded payloads, completion remains warning-only, and fixture execution leaves project snapshots unchanged. Native host trust/loading remains unobserved. |

## Frozen payload comparison

The prior scripts were captured from the tested published base before edits. Their hashes match the earlier source receipt; this run imports only their inspected renderer definitions. The frozen report generator is [context_payloads.py](../../evaluations/context_payloads.py); exact fixture, baseline and output measurements are in [context-payloads.json](context-payloads.json).

| Fixture | Prior startup and every prompt | Current startup | Current prompt refresh | Prior full CLI context |
| --- | ---: | ---: | ---: | ---: |
| Bounded work | 1,364 | 1,721 | 503 | 996 |
| Large history: 500 completed tasks, 60 facts, 60 answered questions | 4,771 | 5,533 | 491 | 63,982 |
| 20,000-character title plus current stale-evidence error | 16,040; error omitted | 1,859; error retained | 636; error retained | 21,074; error retained |

All table values are serialized **characters**, excluding a terminal newline. UTF-8 bytes are also recorded. Ordinary prompt refresh is 63.1% smaller and large-history refresh 89.7% smaller than the old repeated hook payload. The startup packet is larger in the first two fixtures because it supplies action/task references and omission information. Full CLI output remains available; compact large-history startup is 91.4% smaller than that full view. These numbers establish payload behavior only, not token cost, model quality, elapsed project time or a universal ranking.

The 6,000-character startup and 1,200-character refresh caps are tested including JSON escaping and fallback error codes. A fingerprint covers the complete inspection report; it does not identify every source file, external state or the current prompt.

## Review and boundaries

A separate reviewer who did not author the change inspected the concrete projection, CLI and handler; independently ran 71 relevant tests; and exercised additional temporary Unicode/history/blocking-question fixtures. No blocking finding remained. Its four reviewed executable identities match the source tested here. Root authored integration documentation and packaging changes; the combined technical review is explicitly not an independent specification approval. See [review.md](review.md).

No model consultation benchmark, token/cost measurement, paid run, native hook trust/loading test, AWS account observation, plugin installation/update or cloud deployment occurred. The full local suite tests implementation behavior; hashes alone cannot prove the truth of an observation or semantic quality of an AWS architecture.
