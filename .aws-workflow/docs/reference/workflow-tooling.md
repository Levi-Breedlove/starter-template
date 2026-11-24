# Workflow tooling

The Codex AWS workflow keeps its behavioral contract, design, and task plan in Markdown. Standard-library Python checks structure, prepares consultation context, records supplied review and result provenance, detects stale claims, and coordinates explicitly selected task execution. Inspection and specification preparation are read-only; only explicit mutation/execution commands perform their documented effects. The optional native runner is a foreground operation, with its own scope and authority.

Codex supplies the judgment: reading the existing project, researching technical questions, interviewing adaptively, explaining recommendations, and writing useful specifications. The tool supplies consistent inspection and bounded execution mechanics. A structurally valid plan can still be a poor plan; the tool cannot evaluate business meaning or authenticate a human decision.

## Start with the idea you have

From the project root, using Python 3.10 or newer:

```sh
python3 .aws-workflow/scripts/workflow.py new 0100-record-service \
  --title "Safe record retries" \
  --mode greenfield \
  --route requirements-first \
  --idea "Customers should be able to retry a request safely." \
  --activate
python3 .aws-workflow/scripts/workflow.py context
```

After installing the reusable package inside an existing application, use its script path and select the application root explicitly:

```sh
python3 .aws-workflow/scripts/workflow.py --root . context
```

`new` creates `specs/0100-record-service/work.json` and a draft `requirements.md`; the bugfix route creates `bugfix.md` instead. It starts at `consultation`. It does not invent requirements, an interview questionnaire, a design, tasks, reviews, or verification results. Supplying `--idea` records exactly that supplied goal with its initialization source. Codex should read already supplied requirements and known context before deciding that any question is necessary.

The CLI defaults to `--spec-format ears`: explicit EARS behavioral statements and `specification_policy` requiring current analysis before contract acceptance and current fully mapped correctness properties before task acceptance. Use `analyze` and `properties` to prepare exact review requests; Codex performs the review and records the actual response with `--record`. The [specification operations reference](specification-operations.md) defines patterns, response schemas, history and traceability. `--spec-format existing` deliberately preserves an established contract's prior gates. Existing records and callers of the Python `new_work` API are not silently migrated.

Before selecting any work, `doctor` checks setup and mapped records. `hooks` previews the appropriate optional native configuration without writing it or granting trust. See the [quickstart](../../guide/00-quickstart.md).

When `.aws-workflow/manifest.json` identifies a valid schema-1 adoption, `new` carries its actual mapped brief, handoff, adoption report, and environment-capability paths into `context_files`, along with the manifest itself. Those mappings must name existing regular files under the project root and satisfy the same path restrictions. Without an adoption manifest, it includes whichever of the four conventional root context files already exist. It does not copy template-maintainer facts into application work or interpret context files as new authority.

`--activate` explicitly writes `.codex/workflow.json` with `schema_version: 1` and `active_work: "specs/0100-record-service"`. Omitting it leaves the active selection unchanged. `new` refuses an existing work directory. The selected root always defaults to the current working directory, including when the script is packaged elsewhere. No project-global configuration is required before creating a work item.

## Focused context for normal work

Use `context --compact` for entry and resume. It projects the full inspection report into a bounded action summary: errors and current blockers first, the next useful action, up to three eligible tasks with their references, applicable review state, selected sourced context, and omission counts. Completed history becomes counts. `context --compact --json` exposes the compact object. The original full `context`, `status`, and `--json` outputs remain available for audits and diagnostics.

The compact text and native startup view are capped at 6000 characters. Native prompt refresh is capped at 1200 characters and carries a stable report fingerprint. Reuse a loaded packet when that report is unchanged; reload when it changes or no packet is loaded. A fingerprint cannot prove unchanged unread source files or external state. Current user steering, actual source inspection and required validation still apply. No context cache is written, and no new phase or authorization is created by the suggestion.

Omissions are explicit: a compact view is an index into canonical records, not permission to ignore a required source. Errors cannot be displaced by a long title or old completed task history. These character ceilings are not tokenizer measurements or a model-quality benchmark. See [efficient operation](efficient-operation.md).

## Commands and write boundaries

All commands accept `--root PATH` **before** the subcommand. A work ID after an existing-work command is optional; without one, the active pointer selects the work item. All commands accept `--json` after the subcommand.

| Command | Purpose | Writes |
| --- | --- | --- |
| `doctor` | Inspect local setup, mappings and optional capabilities, before or after work selection. | None; no programs, models, credentials or services called. |
| `hooks` | Preview hook configuration and report equivalence/merge needs. | None; no trust change. |
| `new ID --title TEXT` | Start a consultation draft; `--mode`, `--route`, `--idea`, `--spec-format`, and `--activate` refine it. | New work directory; active pointer only with `--activate`. |
| `context [ID]` | Show known facts, sourced answers, up to three suggested unresolved questions, canonical paths, and consultant instructions. | None. |
| `status [ID]` | Derive checkbox state, dependency readiness, current review/evidence state, and issues. | None. |
| `validate [ID]` | Inspect the same structure and claims; exit 1 on validation errors. | None. |
| `review [ID] ...` | Record an actual supplied review outcome and the current artifact identity. | Append review record to `work.json`. |
| `advance [ID] --to PHASE` | Move to the next phase if the boundary being left is satisfied. | Update the phase in `work.json`. |
| `evidence [ID] ...` | Record provenance for an already executed check and hash its declared inputs. | Append evidence record to `work.json`. |
| `analyze [ID]` | Prepare requirements review request and syntax findings. | None; does not call a model. |
| `properties [ID]` | Prepare observable property/verification planning request. | None; does not generate or run tests. |
| `analyze [ID] --record RESPONSE` or `properties [ID] --record RESPONSE` | Validate an actual response against its reviewed inputs and retain provenance. | Append operation history under the work directory. |
| `sync [ID] [--changed PATH]` | Preview changed-input impact and review/completion consequences. | None. |
| `sync [ID] --apply --expected-fingerprint HASH --reason TEXT` | Apply the current inspected reconciliation; repeat any preview `--changed` arguments. | Necessary completion/phase updates and reconciliation history; prior observations retained. |
| `execution-template [ID]` | Return a draft policy containing actual task/check IDs. | None; authority, commands and scopes must be derived. |
| `run-plan [ID] [--task TASK]` or `run [ID] [--task TASK]` | Preview prerequisites, scope and dependency waves. | None; no model call. |
| `run [ID] --execute [--task TASK]` | Execute the explicitly authorized bounded candidate. | Ignored run state, Git worktrees, candidate source/evidence/commits; invokes a model and trusted checks. |
| `run-status RUN_ID` | Inspect persisted result and whether an interrupted operation is unknown. | None. |
| `run-apply RUN_ID` | Integrate the ready candidate against an unchanged original. | Fast-forward original and persist the observed application outcome. |
| `run-abandon RUN_ID --reason TEXT` | Record an inspected failed/interrupted run's disposition. | Persist disposition; retain worktrees/evidence. |

An inspectable draft returns exit 0 for `context` and `status`, even if its report includes issues. `validate` returns exit 0 without errors and exit 1 with errors. Unsafe paths, missing selections, unreadable metadata, and rejected mutations return exit 2. Ordinary unfinished consultation does not require an error or a repeated user approval.

`doctor` returns 1 for required setup problems. Native `run --execute` returns 1 unless its candidate is ready; `run-apply` returns 1 unless the observed application is exact and clean. A post-merge hook's preserved changes are reported as `applied-needs-review`, not success. An exception can leave recorded application intent with an unknown outcome; inspect state before retrying. New setup/specification/execution operations always emit JSON. Preview output may contain blockers while the inspection itself returns 0. The full [execution contract](task-execution.md) defines configuration, clean-Git requirements, POSIX process control, isolation, limits and recovery.

JSON replacement is atomic. A newly prepared work directory is staged before being installed. The tool rejects a known invalid active-pointer destination before creating the work directory. The optional active-pointer write is a separate atomic write, so an unexpected activation failure can leave a valid work directory without selecting it. The command reports that partial success explicitly; inspect the created work using its ID and repair the active pointer instead of recreating the directory. There is no concurrent-writer merge protocol. Finish or coordinate one metadata edit before another.

## Routes and actual authority

| Route | Phase order | Review boundary |
| --- | --- | --- |
| `requirements-first` | consultation → requirements → design → tasks → implementation → verification → complete | Review the contract, design, and executable task plan against actual scope and authority. |
| `design-first` | consultation → design → requirements → tasks → implementation → verification → complete | Review the initial design, derive the contract, then reconcile the connected task plan. |
| `quick` | consultation → tasks → implementation → verification → complete | One combined task-plan review covers the contract, design, and tasks. Separate contract/design reviews are optional. |
| `bugfix` | consultation → requirements → design → tasks → implementation → verification → complete | The `requirements` artifact is the defect/correction/preservation contract in `bugfix.md`. |
| `plan` | consultation → requirements → design → tasks → planned | Finish a reviewed plan. Unchecked implementation tasks remain unfinished; `planned` never means deployed or implemented. |

The `mode` is independently `greenfield` or `brownfield`. Brownfield work uses the existing system's baseline and preservation constraints; it does not need a separate hard-coded phase sequence.

A review record is a receipt for a real decision, including a decision already made under valid delegated authority. It is not a request for a new approval every time a command runs. A current unchanged record remains usable. The tool never infers acceptance from silence, a model statement, a skill, or successful validation, and cannot itself grant deployment authority.

For example, after recording the actual review discussion in the project's decision notes and finalizing the reviewed artifact:

```sh
python3 .aws-workflow/scripts/workflow.py advance 0100-record-service --to requirements
python3 .aws-workflow/scripts/workflow.py review 0100-record-service \
  --artifact requirements \
  --outcome accepted \
  --decision-ref "docs/decisions/0042-record-contract.md#review" \
  --reviewer "Project owner" \
  --authority user
python3 .aws-workflow/scripts/workflow.py advance 0100-record-service --to design
```

The example reference must identify your actual decision; the tool does not create that decision note or verify who authored it. New structured work also needs its actual current analysis before the illustrated acceptance. Use `--authority delegated` and the actual reviewer/reference when prior user authorization delegates the decision. `changes-requested` records a review that did not accept the artifact, including when unresolved semantic findings block acceptance. It cannot satisfy the next boundary. A later review supersedes the earlier outcome for readiness, while the earlier record remains history.

The tool does not approve architecture or choose AWS targets. Execution authority and account limits remain explicit project decisions. A task that is eligible according to its local dependencies may still require an independently authorized deployment or account action.

## Metadata schema

[`templates/work.json`](../../templates/work.json) is the minimal schema-1 document. The work ID must match its directory. Artifact paths are relative to that directory; context and evidence paths are relative to the selected project root. Referenced paths cannot use traversal, any symlink component, or a `.git` component. This conservative policy also prevents writes from replacing an unrelated file through an in-project symlink. The explicitly selected project root itself is resolved once before inspection. Use ordinary project files for ledger inputs.

```json
{
  "schema_version": 1,
  "id": "0100-record-service",
  "title": "Safe record retries",
  "mode": "brownfield",
  "route": "requirements-first",
  "phase": "consultation",
  "artifacts": {
    "requirements": "requirements.md",
    "design": "design.md",
    "tasks": "tasks.md"
  },
  "context_files": ["project/brief.md", "project/adoption-report.md"],
  "facts": [
    {
      "id": "F-001",
      "kind": "supplied",
      "statement": "The existing public API response must be preserved.",
      "source": "project/brief.md#preserved-contract"
    }
  ],
  "questions": [
    {
      "id": "Q-001",
      "prompt": "How long must a completed request remain replayable?",
      "why": "Retention changes the replay contract and storage estimate.",
      "recommendation": "Use the existing business retry window if the owner confirms it is still suitable.",
      "status": "open",
      "answer": "",
      "source": "",
      "blocks": ["requirements"]
    }
  ],
  "reviews": [],
  "evidence": []
}
```

Fact kinds are `supplied`, `observed`, `derived`, `assumption`, `proposed`, and `conflicting`. Every fact has a statement and a source, including the basis of a derived implication or an assumption's origin. This vocabulary distinguishes information quality; it does not make a claim true. A conflict remains visible until Codex records the explicit resolution.

Questions are `open`, `answered`, or `deferred`. An answered question needs its actual answer and source. An open question cannot also contain an answer. A deferred question cannot remain a blocking prerequisite. Use `why` to preserve its impact and deferral rationale. `blocks` names any affected `requirements`, `design`, `tasks`, `implementation`, or `verification` boundary. An open question does not prevent drafting that phase; it prevents accepting or leaving the affected boundary, and an unresolved execution question suppresses task eligibility in that phase.

Codex edits these facts/questions and the canonical documents during the conversation. The CLI does not extract meaning from prose, automatically answer questions, or decide that every supplied requirement is adequate. Empty `questions` means no open questions have been recorded, not a proof that no unknowns exist. If the supplied requirements are sufficient, Codex should proceed directly rather than create questions to fill a fixed questionnaire.

## Canonical Markdown conventions

The parser supports the explicit conventions in the templates, not arbitrary Markdown. Fenced examples are ignored. Define `REQ-001`, `FIX-001`, `KEEP-001`, `DEF-001`, or `DES-001` in a heading or the first cell of a table row. IDs use their exact uppercase prefix and at least three digits. Duplicate and malformed definitions are errors. A contract table row whose `Required or deferred` column is exactly `Deferred` is excluded from required coverage. The word “deferred” in behavioral prose does not change its status. Rows without this explicit status column remain required; observed `DEF` entries are distinct from required correction/preservation behavior.

Each task has a heading, one matching checkbox, and explicit fields:

```markdown
### T-001 — Store the record once

- [ ] T-001 complete
- Activity: ready
- Contract / design: REQ-001 / DES-001
- Prerequisites: none
- Scope and exclusions: Change the existing record operation only.
- Acceptance: A repeated valid request produces exactly one stored record.
- Verification: CHK-001
- Evidence / review: none
- Blocker: none

## Verification matrix

| Check | Requirement | Task | Method and expected result | Evidence |
| --- | --- | --- | --- | --- |
| CHK-001 | REQ-001 | T-001 | Repeat a request and assert one stored record. | Not run |
```

List every referenced ID explicitly. Use `REQ-001, REQ-002` instead of ranges or `all`. The first four check columns are check ID, requirement IDs, task IDs, and method/expected result; the optional final column is a human-readable evidence summary. Avoid literal unescaped table separators inside cells. Task headings use level 2–4; the usual template uses level 3. Keep task fields before the next non-task level 1–3 heading.

`Prerequisites` contains task IDs or `none`. Put an external readiness constraint in `Blocker` and/or the question ledger; do not hide it in free-form dependency prose. `Dependencies` and `Depends on` are accepted field aliases. `Verification` can also be spelled `Checks`. Existing `Requirements/design` is accepted for the contract/design field, but explicit template fields are preferable.

Task-to-check links and the matrix must be reciprocal. Every required behavioral contract ID needs check coverage, and each check's requirements must be accounted for by its linked tasks. Dependencies must exist and be acyclic. `Activity` is explanatory, not a separate status authority: `complete` must agree with the checkbox. A checked box requires current passing results for all its listed checks, validly completed prerequisites, and no unresolved task blocker. Deferred work belongs outside canonical task headings/checkboxes until it is committed to the plan.

## Artifact identity and stale results

Each review record contains `id`, `artifact`, `outcome`, `decision_ref`, `reviewer`, `authority`, `recorded_at`, `snapshot_policy: "canonical-plan-v1"`, and `hashes` keyed by project-relative paths. Requirements and design use raw file SHA-256. A standard design review includes the contract plus design; an initial design-first review includes the design, and its subsequent requirements review includes both design and contract. Changing the upstream design therefore invalidates the derived contract review even if its prose has not yet been reconciled. A tasks review includes all three canonical artifacts.

The tasks hash represents the **plan projection** of `tasks.md`: the canonical task-completion checkbox state is normalized, explicit Activity/Evidence/Blocker progress fields are excluded, and a check matrix's evidence summary is excluded. This permits ordinary progress updates without repeating the same review. Other checkbox wording remains substantive task content, so adding acceptance work cannot inherit an old passing result. Task scope, acceptance, prerequisites, contract links, check method, and other substantive plan changes invalidate the accepted plan. Update review notes before recording a review snapshot; editing a reviewed contract's state text afterward also changes its raw hash.

Evidence adds a narrower check signature containing the check definition and its linked tasks' stable acceptance/scope/dependency content. It automatically includes the current contract and design hashes, the receipt hash, and every explicitly declared tested input hash. Checking a task box or adding its evidence summary does not stale the result. Changing a captured source file, receipt, contract, design, check, or relevant task content does.

The most recent recorded result for a check is its current result. A failed or not-run result does not fall back to an older pass. Historical records remain in the ledger. A stale result attached to unfinished work is visible; using it to support a checked task is a false-completion error. Changing an unrelated input that was never declared cannot be detected, so Codex must identify all relevant source, fixture, configuration, and built artifact inputs. Remote state, IAM changes, external dependencies, live AWS drift, and test execution itself are not proven by file hashes.

## Record already executed verification

First run the real project check through the appropriate authorized environment and save a sanitized result receipt. Then record exactly what happened:

```sh
python3 .aws-workflow/scripts/workflow.py evidence 0100-record-service \
  --check CHK-001 \
  --record evidence/0100-record-service/retry-check.md \
  --result pass \
  --method "The actual command or manual procedure that was executed" \
  --environment "The actual isolated execution environment" \
  --candidate "The actual revision plus uncommitted patch identity, if any" \
  --observed-at 2026-11-22T12:00:00+00:00 \
  --input src/record-service.py \
  --input tests/test_record_service.py
```

These values are illustrative; substitute your real execution details and timestamp. The tool hashes files when the record is created. It does not retroactively prove those files were used by the earlier execution. Capture immediately against the same candidate, preserve the receipt, and use trustworthy CI/artifact attestations when the project requires stronger provenance. Never turn a planned command into a passing result record.

An evidence record contains `id`, `check`, `result`, `record`, `method`, `environment`, `candidate`, `observed_at`, `recorded_at`, `inputs`, `artifacts`, and `check_signature`. `observed_at` is the supplied actual observation time; `recorded_at` is when the ledger was written. A timestamp includes a timezone. Results are `pass`, `fail`, or `not-run`. At least one tested input distinct from the receipt is required. The CLI never marks the task complete; update the canonical checkbox only after acceptance, relevant checks, dependencies, and applicable review are satisfied.

## Read-only integration API

```python
from pathlib import Path
from workflow_engine import WorkflowError, inspect_work

report = inspect_work(Path.cwd(), "0100-record-service")
```

The report includes `schema_version`, `id`, `title`, `mode`, `route`, `phase`, project-relative `artifacts`, `context_files`, `known_facts`, `answered_questions`, `open_questions`, up to three `next_questions`, `deferred_questions`, `reviews`, derived `tasks`, `checks`, current `evidence`, `dependency_ready_tasks`, `eligible_tasks`, `issues`, and `consultant_instructions`. Each issue has `severity`, `code`, `message`, and optionally `path`.

Work using specification format, policy or operation histories also includes `spec_format`, `specification_policy` and `specification`. The latter reports each operation as missing/current/stale/invalid, property mapping and blocking findings. Legacy reports without those features retain the previous key set. Compact context selects analysis or property mapping when required at the current boundary; errors and consequential unresolved questions keep priority.

`dependency_ready_tasks` reflects unfinished tasks whose local prerequisites are validly complete. `eligible_tasks` additionally requires an implementation/verification phase without structural errors or a current phase-blocking question. Neither array grants account or deployment authority. Review statuses are `missing`, `accepted`, `changes-requested`, or `stale`. Each task's `checked` value comes only from Markdown; `completion_valid` reports whether the recorded checks/dependencies support that checkbox.

Missing selection or unreadable metadata raises `WorkflowError`; ordinary inspectable drafts return a report. Integrations should surface exact problems and preserve legitimate incomplete work. A stop-time check should distinguish a false completion claim from an ordinary consultation awaiting an answer. The tool is a local workflow ledger, not a mandatory unattended scheduler, semantic verifier, or substitute for native Codex authorization controls.

## Verify a project

Run `doctor` after adoption and `validate` on each selected work item. Execute the project's actual checks against the candidate and retain the observed outputs, working tree identity and relevant configuration. Use the [evidence guide](../../evidence/README.md) to record the scope of each result.
