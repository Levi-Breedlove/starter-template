# Local checks: developer workflow

**Observed result:** 183 tests passed; aggregate exit status 0. The suite took
29.821 seconds. The combined test/measurement operation took 30.159 seconds.
The tested source identities were identical before and after execution.

The exact UTC interval, Python version, commands, base revision and SHA-256
identities are in [run-observation.json](run-observation.json). The actual
[test output](local-tests.txt) is retained unchanged. This is a new run against
the delivered implementation; earlier 89-test and 105-test receipts remain history.

## Actual aggregate command and coverage

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

| Area | Cases | Established scope |
| --- | ---: | --- |
| Workflow engine | 44 | Phase/review/dependency/traceability/evidence rules, stale claims, source/path handling and legacy behavior. |
| Bootstrap | 25 | Additive greenfield/brownfield adoption, mappings, required package inputs, collision/concurrency handling and managed ignore preservation. |
| Context | 15 | Required selection, strict serialized limits, omissions, fingerprints, error priority and read-only full audit compatibility. |
| Native event adapter | 10 | Event input/output handling, bounded context and completion feedback without automatic continuation. |
| Repository checker | 14 | Required files, supported explicit Markdown destinations, path escapes and incomplete scans. |
| Actual package integration | 2 | Actual-source adoption, CLI/context, mapped links, rerun preservation and Git-root hook command in temporary projects. |
| Setup doctor | 14 | Readiness before selection, runtime/guidance identities, editable project records, optional capabilities and no subprocess/credential probes. |
| Specification operations | 25 | EARS patterns, source-bound responses, blocker persistence, property mapping, stale sources and expected-fingerprint reconciliation. |
| Task controller | 26 | Real Git worktrees/process checks with fake authors; dependencies/scopes, candidate verification, preservation, time limits and uncertain outcomes. |
| Developer CLI workflow | 8 | Installed commands, default analysis/property gates, design-first/quick paths, actual rejection, legacy selection and changed-contract reconciliation. |

All model/decision responses in fixtures are explicitly simulated. Local checks
inside controller fixtures actually execute; they establish only their local
fixture behavior. No test authenticates a reviewer or proves live AWS behavior.

## Independent review and corrections

The fresh reviewer inspected the actual source, independently reproduced defects
and verified corrections. Its [authored receipt](review.md) records seven closed
findings: ignored rename destinations, surviving child processes, post-merge
divergence, total time limits through Git hooks, recording real review rejection,
required consultation guidance, and misleading inherited execution fields.

The reviewer also exercised the installed brownfield CLI through planning,
execution, status and explicit application using a temporary fake executable
named `codex`. The original file remained unchanged until application. This is
package/native-adapter wiring evidence, not a real native model trial.

## Connected specification and developer guidance

The integrating author inspected the final quickstart, consultation/feature
guides, workflow reference, bootstrap boundary, specification operations and
execution reference against the implemented commands. The path/CLI examples
distinguish source and adopted projects. The architecture and roadmap now describe
the implemented foreground controller and the remaining native/cloud observations.

The maintenance work itself deliberately adopts the new EARS and required
analysis/property policy. Its [actual author review](specification-review.md)
explains the judgment and qualifications. The operation records are current,
and ten properties resolve to actual task/check IDs. This is a performed author
review within the current session; it is not independent or user acceptance.

The [native pilot proposal](../../evaluations/native-pilot-plan.md) has two frozen
synthetic scenarios, exact file blocks/prompts, a schema/policy and bounded command
sequence. Its author validated extraction of 27 unique blocks, JSON/Python syntax
and syntax-only shell parsing. That preparation did not run the scenarios or a
model. T-008 remains unfinished until approved actual observations exist.

## Context regression measurements

The actual command `python3 evaluations/context_payloads.py --baseline-dir
TRUSTED_PRIOR_RENDERERS` compared the frozen inputs against the previously
inspected renderer definitions. [Exact measurements](context-payloads.json)
retain both baseline hashes and fixture identities.

Ordinary refresh remains 503 characters versus the prior 1,364; large-history
refresh remains 491 versus 4,771. Startup is larger for those fixtures because it
contains selected task/action references and omission information. The long-title
fixture retains the stale-evidence error in both current views. The 6,000/1,200
limits count serialized characters, including escaping; they are not token,
cost, model-quality or product-comparison measurements.

## Current claims and scope limits

Shared inputs changed, so the completed consultant/context slices are reconciled
using these new observations and the actual publication receipt. Their earlier
records are preserved. Declared source identities establish freshness, not
external state or the truth of an assertion. Canonical task completion remains in
each work's Markdown and is not duplicated in these receipts.

The runner is a bounded foreground coordinator, not a hostile-code sandbox or
an exactly-once external-effects service. Native process behavior was exercised
on Linux; configured native model behavior and other platforms remain separate
observations. Trusted commands/hooks and native/IAM controls keep their own roles.
No real model invocation, account/credential access, AWS operation, plugin
installation, hook activation, client trust change or background service occurred.

Final link/naming and full remote-tree observations are recorded separately in
[publication.md](publication.md). They must not be inferred from this local pass.
