# Verification: focused context and efficient operation

**Local result:** Implemented and verified; 105 combined tests passed.  
**Candidate identity:** Exact tested executable/fixture hashes, observation interval and base commit are in [run-observation.json](run-observation.json).  
**Publication result:** Recorded separately in [publication.md](publication.md), after actual remote readback.

The change adds a shared bounded context projection, a compact CLI option, smaller prompt refresh and a concise operating policy in source and adopted projects. Full inspection and prior workflow semantics remain available. [Local checks](local-checks.md) explain scope, preserved behavior and independent review; [raw tests](local-tests.txt) contain the aggregate result.

## Measured result

Frozen ordinary-work refresh fell from 1,364 to 503 characters; large-history refresh from 4,771 to 491. A 20,000-character title no longer displaces a stale-evidence error. Startup is larger in the ordinary/history fixtures because it supplies action/task references and omission details. See [exact measurements](context-payloads.json).

The 6,000/1,200 limits count serialized characters including JSON escaping, not model tokens. Measurements do not establish a model-quality or cost ranking. Earlier receipts stay historical; current consultant evidence is appended against the new run when shared inputs change.

## Remaining evidence boundaries

Real greenfield/brownfield model consultations, selected-client hook trust/loading and authorized AWS outcomes remain unobserved. The [evaluation protocol](../../evaluations/README.md) defines comparable pilots and quality gates. Durable workers, CI execution and schedules are outside this implemented slice. No account operation, paid model trial, plugin installation or trust change occurred.
