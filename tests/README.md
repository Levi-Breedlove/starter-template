# Verification scope

Run from the bootstrap source root:

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/check_repository.py
```

The standard-library fixtures exercise repository links, workflow state/phase/dependency/evidence rules, bounded context and refresh, additive application installation and read-only native event responses. They use temporary projects and simulated decision/check receipts. They do not invoke a model, inspect an AWS account or deploy a workload.

Independent review reproductions become targeted regression cases. The final combined run and source identities belong in the [current verification receipt](../evidence/0003-efficient-context/verification.md). A fixture's fake pass proves that the validator handles the record as specified; it does not establish the example business outcome.

Actual model consultation, native host activation and cloud delivery follow the separate [evaluation protocol](../evaluations/README.md). Adopting applications retain their existing tests and add checks appropriate to their own accepted requirements.
