# Specification operations

The local CLI makes specification analysis, correctness-property planning and change reconciliation explicit operations. Codex performs semantic reasoning against the supplied source. Python checks sentence shapes, identities, references, recorded blockers and safe state changes. No command in this reference calls a model, reads credentials, invokes a test, changes client trust or accesses AWS.

Run the examples from the project root using the indicated workflow entry point. Omit a work ID only after selecting active work. All three operations emit structured JSON; `--json` is accepted explicitly.

## Connect a feature or defect to project decisions

The application manifest maps the five project foundations. New specification drafts link the mapped brief and system requirements. Keep the feature's observable acceptance criteria, defect reproduction or implementation choices in its own specification. Link the relevant foundation sections for shared standards and decisions.

In a foundation-enabled installation, `work.json` uses `context_files` to select the project requirements and any applicable technology, structure or architecture record. Add the actual mapped path when it becomes a dependency and link its section in the feature contract or design. Compact context lists the selected paths. Analysis and properties identify their file hashes, so a relevant edit appears in `sync`. The brief and handoff provide session context. For a decision from the brief, cite its actual path and optional section as a fact or answered-question source to bind its identity. Older installations retain their existing mappings and review inputs.

## Write observable EARS requirements

EARS means Easy Approach to Requirements Syntax. Its sentence patterns make the triggering condition, system and required response explicit. This implementation supports the following patterns, case-insensitively:

| Pattern | Original example |
| --- | --- |
| Ubiquitous | THE service SHALL retain an audit event for each accepted operation. |
| Event | WHEN a customer retries a completed request, THE service SHALL return its original result. |
| State | WHILE maintenance mode is active, THE service SHALL reject new writes with a documented error. |
| Unwanted condition | IF an upstream request times out, THEN THE service SHALL return the documented retryable error. |
| Optional capability | WHERE reminder delivery is enabled, THE service SHALL enqueue one reminder for a confirmed booking. |
| Combined | WHERE reminders are enabled, WHILE a booking is confirmed, WHEN its reminder time arrives, THE service SHALL enqueue its reminder once. |

For combinations, use optional capability, then state, then one event or unwanted condition. An unwanted `IF` condition needs `THEN`. `WHERE` describes the behavior when a capability exists; it does not waive a required check. Put explicit IDs in a requirement table or heading, following the [tooling conventions](workflow-tooling.md). In a heading, put the behavioral sentence in the first ordinary paragraph. Keep observation-only `DEF` entries separate from normative `FIX` and `KEEP` behavior. Explicitly deferred table rows are not required acceptance behavior.

The linter catches missing sentence structure, unfinished statements and duplicate IDs. It also gives conservative wording hints. A syntactically valid requirement can still be wrong, contradictory or incomplete; those judgments belong to actual analysis. Existing schema-1 work keeps its established contract format unless deliberately migrated. New CLI work defaults to `spec_format: ears`; `--spec-format existing` is for an explicit existing-format adoption decision, not a way to bypass unresolved work.

## Analyze requirements

```sh
python3 .aws-workflow/scripts/workflow.py analyze 0100-first-capability
```

The response is a review request, not a completed analysis. It contains:

- The exact requirement source hashes, known fact/question context fingerprint and deterministic request ID.
- Extracted requirement IDs, statements, syntax findings and applicable authoring patterns.
- Instructions to reason across contradictions, ambiguity, constraints, assumptions and missing cases.
- A `response_schema` for the actual reviewer result.

Codex reads the named inputs and actual decision sources, performs the analysis, and saves actual review notes plus a JSON response conforming to that schema. Use existing project evidence paths; the files need not follow a fixed filename convention. Record the result afterward:

```sh
python3 .aws-workflow/scripts/workflow.py analyze 0100-first-capability --record evidence/0100-first-capability/analysis-response.json
```

Common response fields are `schema_version`, `operation`, `request_id`, `input_hashes`, `context_fingerprint`, `reviewer`, `review_ref`, `observed_at` and `summary`. Copy identity fields from the current request. `review_ref` is an existing project-relative review-notes file, optionally with a heading fragment; it must be separate from the response, reviewed inputs and mutable operation history. `observed_at` identifies the actual observation with a timezone. These fields record an assertion and its evidence; they cannot authenticate a reviewer or prove the reasoning occurred.

An analysis also supplies `findings`. Every finding has an `ANA` ID, affected `requirement_ids`, `severity` (`blocker`, `warning`, `info`), `category`, `statement`, `state` (`open`, `resolved`), `resolution` and an actual project evidence `source`. Categories cover contradiction, ambiguity, constraint, assumption, missing case, format and other. A resolved finding needs its actual resolution and source. An empty array is appropriate only after a performed review found no issue within its stated scope.

The importer rejects stale identities, unknown IDs, invalid provenance and malformed responses. An open blocker remains visible until a new current analysis resolves or supersedes it; editing a source file alone does not silently erase it. No imported analysis counts as product acceptance or changes a phase.

## Derive correctness properties and verification

```sh
python3 .aws-workflow/scripts/workflow.py properties 0100-first-capability
python3 .aws-workflow/scripts/workflow.py properties 0100-first-capability --record evidence/0100-first-capability/properties-response.json
```

The first command prepares a request tied to requirements, design and actual decision sources. Codex derives the properties and writes the response before the second command records it. Each property has a `PROP` ID, `requirement_ids`, observable `statement`, `preconditions`, `strategy`, `verification`, `task_ids`, `check_ids` and evidence `source`.

Strategies are `property-based`, `example`, `contract`, `integration` or `operational`. Cover every required behavioral ID using a suitable strategy. For property-based tests, describe the generated-input domain and expected invariant, then implement the chosen executable checks during the task. For bugfix work, consider proof of reproduction, proof of correction and unchanged behavior separately. A local mock cannot establish live IAM, service, networking or deployment behavior.

Properties can be drafted after both requirements and design exist in either phase route. Task/check IDs may be proposed or empty during design. Once the task plan exists, references must resolve to its actual IDs and matching requirement coverage. Before accepting tasks in new structured work, mapping must be complete. If a mapping is incomplete, repair the references and record the updated response; the requirements/design identity can remain unchanged.

Property planning does not imply tests were generated or executed. Codex creates those test files in the implementation tasks, and actual results use the normal evidence command. Optional test technique and required product behavior remain separate decisions.

## Freshness, history and review boundaries

Operation histories live at `specs/<work-id>/analysis.json` and `properties.json`, each with schema version 1, operation, work ID and versioned records. Records retain the response, response-file identity, review-note identity, all separately referenced finding/property sources and timestamp. Existing history is retained; importing an identical current response is a no-op.

Analysis binds requirements and the sourced decision context. Properties additionally bind design. Future design generation does not invalidate a requirements-only analysis, and routine task checkbox changes do not invalidate the specification records. Actual task/check mappings are checked against the current task graph. An edited requirement, relevant decision, review note, response or referenced source makes its old conclusion historical. Decision sources must be separate from mutable operation histories to avoid a record invalidating itself as it is saved.

New structured work records `specification_policy` with required analysis and properties. The engine requires current analysis before accepting requirements, and current fully mapped properties before accepting tasks. Standard routes retain their actual requirements/design review decisions; use the user's confirmation where needed and honor actual prior delegation. Quick work has no intermediate document approval pauses and uses the combined planning review. Existing work with no policy is not silently migrated into new mandatory gates.

`status` exposes missing, current, stale or invalid operation state and any blocking finding. `validate` reports applicable errors. Review-source hashes establish identity and detect change; they do not guarantee honest observations or semantic adequacy.

## Reconcile changed specifications and evidence

```sh
python3 .aws-workflow/scripts/workflow.py sync 0100-first-capability
```

The preview compares declared review/evidence identities, specification operation inputs and task dependencies. It identifies changed inputs, affected artifacts/reviews/checks/tasks, completion that must reopen, the earliest affected route boundary and regeneration instructions. Add repeated `--changed project/relative/path` arguments when an actual changed input should be assessed explicitly. Deleted paths can be named; traversal and symlink paths are rejected.

Codex inspects the actual changes, resolves semantic impact and applies the reviewed preview using its returned fingerprint:

```sh
python3 .aws-workflow/scripts/workflow.py sync 0100-first-capability --apply --expected-fingerprint EXACT_PREVIEW_FINGERPRINT --reason "The accepted retry contract changed; reconcile its implementation and checks."
```

Repeat any `--changed` arguments used for the preview. A changed preview is rejected before writes. Application updates only the necessary completion checkboxes/activity, phase and a reconciliation history entry. It retains requirements, design, implementation, prior review/evidence records and unaffected valid tasks. Changed decision context can reopen the review boundary without discarding completed work before a contract consequence has been identified.

Codex then updates the affected prose, task/check definitions and generated test work, obtains any actually required review and reruns affected checks. The code does not silently choose new business rules, rewrite requirements, grant authority or record a passing test. Undeclared external changes still require engineering assessment and appropriate evidence; a file inventory cannot observe cloud state.

Apply reconciliation on a stable working tree. The operation rechecks identities and rolls back its own completed writes on ordinary write failure. If concurrent edits prevent rollback it reports the affected files. There is no cross-process metadata lock, merge protocol or power-loss transaction guarantee.

## Python interface and verification

`workflow_engine.specifications` exposes `lint_ears`, `ears_pattern`, `analyze_requirements`, `derive_properties`, `record_specification_result`, `specification_status`, `plan_reconciliation` and `apply_reconciliation`. The status helper accepts an existing inspection report and does not recursively inspect work, supporting engine integration. Request/record separation also permits a future supported model adapter without changing the provenance contract.

The local fixture suite exercises EARS patterns, exact request identities, malformed/stale responses, blocker preservation, external source changes, property coverage/mapping, conservative reconciliation, stale previews and write-failure rollback. These tests use explicitly simulated review responses. They establish the tool contract; real consultation quality, independent semantic review and generated-test behavior require actual agent observations.
