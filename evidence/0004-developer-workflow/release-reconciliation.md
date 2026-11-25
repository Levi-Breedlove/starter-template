# Release candidate verification

All 207 offline regressions passed on the published maintenance source `98a4de0b0158130573e2ff5281321bb4a57a7bc6`. The clean application candidate is `895a9b9efae5c5a4a10ee533ec84dbc1ac95d4a1`, tree `7d6583a62dd152d6a849d14b54b5d4240c593c4c`. Two builds from the same source produced those distribution bytes. These observations predate any native first-use observation on the packaged candidate. [Full regression output](release-reconciliation.tests.txt) · [Distribution procedure](../../docs/distribution.md)

## Local verification on the candidate

| Check | Actual observation |
| --- | --- |
| Regression and repository checks | Python unittest discovery ran 207 tests in 52.755 seconds, exit 0. The maintenance checker found 118 Markdown files, 454 local links and 32 required files. The distributed checker found 78 Markdown files, 247 local links and 12 required files. Both reported zero issues. |
| Direct and brownfield adoption | Distribution and real-package fixtures exercised copied Git files, clean first use, preserved instructions, dirty application content, IaC and pipeline files, mapped foundations, installed CLI use and idempotence. Bootstrap tests also exercised schema-1 upgrades and drifted managed files. |
| Consultation and saved work | Source and generated instructions define seven conversational shortcuts. First-use consultation distinguishes project foundations from feature work and consults settled decisions on return. Installed route checks created requirements-first, design-first, quick, bugfix and plan work, then recovered each work ID in a fresh CLI process. Direct work remains available for small, understood changes. |
| Specification, execution and evidence | Workflow and specification fixtures exercised route order, analysis, correctness properties, dependencies, evidence freshness and changed-input reconciliation. Runner fixtures exercised bounded execution, failure, isolation and explicit application. The native-check executable observed available prerequisites in Codespaces. |
| AWS integration | The public capability record names the official guidance and actual hosted operations exercised. Installed instructions distinguish public tools from individual authenticated operations and establish optional workload-specific local emulator checks. This release has no emulator runtime or live AWS verification. [Public capability observations](public-aws-capabilities.md) |
| Concrete candidate review | Review identified nested Git metadata and alias mapping hazards, missing AWS guides, maintenance instructions entering the distributable package, and checker gaps. Revisions and preservation-focused regression cases addressed the findings. |
| Neutrality and publication | A scan of all 171 tracked paths and their contents found zero prohibited name matches. GitHub reported the expected readiness head. An independent readback on November 24, 2026 at 23:31 UTC matched all 171 paths, modes, types and object IDs in tree `6d79b64257d1a5e287a222283a3255bdbeac61a6`. The recursive tree was complete. |

The bounded context evaluation used the same three frozen fixture identities and the same baseline scripts from `ee1294e4a123aa929c7f7cf178e326562cad5e9d`. The character counts below measure local renderer output. The long-title case retained its stale-evidence error in the new startup and refresh. [Measurement script](../../evaluations/context_payloads.py)

| Frozen report | Prior startup and refresh | Current startup | Current refresh |
| --- | ---: | ---: | ---: |
| Bounded work | 1,364 | 1,721 | 503 |
| Large history | 4,771 | 5,533 | 491 |
| Long title and error | 16,040 | 1,859 | 636 |

## Reconciled maintenance checks

Each work ledger retained its earlier receipts. New receipts bind the checks affected by packaging to this source and its verification. The reviewed sync previews, their applied fingerprints and the release task-plan review are preserved. [Reconciliation records](release-reconciliation.json)

| Work | Checks covered |
| --- | --- |
| Consultant workflow, 0002 | Consultation procedures, state and path validation, adoption, bounded hook feedback, neutral source and publication. |
| Efficient context, 0003 | Compact/refresh behavior, actual adoption and safety, measured fixture comparison and published source. |
| Developer workflow, 0004 | Reviewed release plan and scope, semantic specification operations, adoption and setup, installed CLI operation, integrated review and published source. The existing bounded-controller and frozen native observations retained their source identities. |

The frozen greenfield and brownfield acceptance remains scoped to `64875eeeb24e615a2fa92d5b9c02503fab7a01be`. G4 closed with a current handoff, schema-valid final response and verified task completions. Reopening dependent maintenance checkboxes during source reconciliation did not consume another pilot slot. The packaged literal-`start` observation and promotion have separate release gates in the task ledger. [Frozen acceptance](native-pilot-closeout.md) · [Release gates](../../specs/0004-developer-workflow/tasks.md)
