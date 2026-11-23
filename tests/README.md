# Verification scope

Run from the bootstrap source root:

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/check_repository.py
```

The standard-library fixtures exercise repository links, workflow state/phase/dependency/evidence rules, bounded context, additive installation, setup, native event responses, source-bound analysis/properties and reconciliation. Task-controller tests use real temporary Git repositories/worktrees and actual local subprocess checks with simulated model authors. Installed-package tests exercise public command dispatch. They do not invoke a real model, inspect an AWS account or deploy a workload.

Independent review reproductions become targeted regression cases. The final combined run and source identities belong in the [current verification receipt](../evidence/0004-developer-workflow/verification.md). A fixture's fake pass proves record handling; actual local subprocess results establish only the declared local fixture behavior. Neither establishes real model judgment or AWS outcomes.

Actual model consultation, native host activation and cloud delivery follow the separate [evaluation protocol](../evaluations/README.md). Adopting applications retain their existing tests and add checks appropriate to their own accepted requirements.
