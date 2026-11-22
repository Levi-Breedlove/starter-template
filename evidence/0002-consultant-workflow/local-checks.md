# Local checks: executable consultant workflow

**Observed UTC interval:** 2026-11-22T11:01:27.466732+00:00 to 2026-11-22T11:01:30.391807+00:00.  
**Environment:** Python 3.12.14 on the local Linux implementation workspace; standard library; temporary projects.  
**Candidate:** Base `a08ad8d6486eece5d79a783f451778246c866821` plus the local source identities below. This was an uncommitted candidate at execution.

## Actual checks

| Check | Observed procedure and result |
| --- | --- |
| CHK-001 | Root integration review of router, consultation guide, route procedures, templates and both fictional roleplays against supplied requirements and actual CLI. The documents preserve known decisions, derive technical recommendations, ask only material gaps and save answers. Scope and real review authority are distinguished. PASS for document consistency; no behavioral model trial. |
| CHK-002 | Workflow subset: 44 fixtures passed, including independently reproduced false-completion, stale-review, required-coverage, mutation-path and partial-state cases. |
| CHK-003 | Bootstrap subset: 20 fixtures passed. Actual-source greenfield and brownfield integration passed: preview preserves bytes, install preserves user files/configuration, packaged new/context/status/validate work, mapped brief/handoff survive resume, links resolve and rerun has zero changes. |
| CHK-004 | Hook subset: 9 fixtures passed. Actual packaged hook command ran from a nested Git directory for all three events, returned expected JSON/context and left the snapshot unchanged. This does not prove native Codex event loading. |
| CHK-005 local portion | Full suite: 89 tests passed (44 workflow, 20 bootstrap, 9 hook, 14 repository checker, 2 integration). Repository scan found zero link/structure issues; current path/content naming scan found zero prohibited-name matches. Publication readback is a separate observation. |

Exact test output: [local-tests.txt](local-tests.txt). Commands:

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/check_repository.py
```

The local file check reported: PASS: 79 Markdown files; 251 local links; 19 required core files; 0 issues.

## Independent findings closed

Reviewers inspected implementation they did not author and reproduced the material failures in temporary fixtures. Fixes and targeted regressions close: substantive extra task checkbox escaping freshness checks; design-first requirements not binding the prior design; invalid activation destination creating confusing partial work; pointer/specification symlinks redirecting writes; required behavior containing a deferral word losing coverage; malformed hook event type crashing; incomplete runtime source installing successfully; and unreadable source inventory silently omitting guidance. Actual-source integration additionally caught and corrected missing adoption-manifest context on resume.

The root integration reviewer authored some documentation and the hook adapter; that review is not labeled independent. Independent code reviews had bounded scopes and do not establish complete security assurance.

## Tested source identities

| File | SHA-256 |
| --- | --- |
| `scripts/bootstrap.py` | `943c3dbc5dbfd4d8b1a6c825ef4b43a22539f1497bf86327d4d23f6fb6d60daa` |
| `scripts/check_repository.py` | `3070c5f54c1b4ee9a7789f77606914cf5db81c5ecd6dc33f1e41cb00721ce139` |
| `scripts/codex_hooks.py` | `0f4f6137366e02d0444da2e473ad424bcf91aa9c0049cc5eb2c9c3ba9aff5314` |
| `scripts/workflow.py` | `6446b75c11c4d63b4af45dfb9de9a2ce3ac04b863244b232e953deddda0bd464` |
| `tests/test_bootstrap.py` | `0af272bc4e8e9dc82b5094938d187c28cd76eda6ea959c216a2ed036146ee62c` |
| `tests/test_codex_hooks.py` | `39dd26af64ae316483984960b6872fa3377d4ff635268946d5cbe220d793c279` |
| `tests/test_integration.py` | `c32089a5eb41460309ae262eb873878307e7e504150e0816377433cca2958324` |
| `tests/test_repository_checks.py` | `acf6669ad654fc794c1a8c1799a41b7b9e606247fa688e525d3221f6a6f10c0b` |
| `tests/test_workflow.py` | `9eba162a6d7fd5407336bd053c1ac6fa7cd15109ea40c5ffd55673e0d47bb98e` |
| `workflow_engine/__init__.py` | `d2fd7c6cc44a0eb7b39b1b7dc996f3943b7ad3cdd73dda42ecbb177fbc1b4bd2` |
| `workflow_engine/engine.py` | `2527a061f489c5869bb361122cd482842b91fe02c4070a10af7371fab9fa9f44` |

## Limits

The engine validates declared structure and file identities, not requirements quality, authentic human approval or actual test execution. The installer preserves files but does not semantically merge conflicting project instructions. Fixture receipts are simulated inside tests. The system has no durable autonomous worker scheduler, hosted plugin update proof, live model interview benchmark, native client trust/loading observation, AWS account observation or deployment result. No credentials, accounts, resources, plugins or paid background service were accessed or installed for these checks.
