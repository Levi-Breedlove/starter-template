# Independent review: complete developer workflow

**Work:** 0004-developer-workflow.  
**Reviewer:** Independent review agent, separate from the implementation owners.  
**Recorded:** 2026-11-23T08:17:18.212530+00:00.  
**Disposition:** All material findings raised by this review are closed in the source identities below. No unresolved material finding remains in the reviewed local implementation scope.

This is an actual code review and local verification record. The reviewer inspected code, reproduced defects in disposable local projects, communicated findings to their owners, and verified the corrected behavior. The reviewer made no implementation edits. The only repository file authored by the reviewer is this receipt, following the integration owner's explicit request.

The integration owner's aggregate candidate run, final naming/link checks, publication and remote readback remain separate evidence. This receipt does not close the native-client acceptance task, claim model quality, or establish end-to-end runtime equivalence.

## Scope and review basis

The reviewer read `AGENTS.md` and this work's requirements, design, execution plan and tasks. The review covered complete bootstrap, doctor, specification-operation and execution-controller sources; the new CLI dispatch, engine policy/review integration and context next-action behavior; and the repository checker's expanded required-path inventory. For the checker, the new 31-path inventory and associated fixture-directory adjustment were reviewed, rather than re-auditing its entire pre-existing Markdown parser.

The principal questions were preservation of existing work, path and collision handling, honest setup and execution readiness, optional versus required capabilities, phase compatibility, review and evidence freshness, reconciliation, bounded process behavior, candidate application, and authority boundaries. Legacy contracts were evaluated separately from new CLI work's explicit EARS and analysis/property policy.

## Findings, fixes and rechecks

### IR-001 — Ignored user file could be overwritten by a rename

**Severity:** High. **Status:** Closed.

The original apply collision check used `git diff --diff-filter=A`. Git represented an exact rename as `R100`, so the destination was omitted from the check. In a disposable fixture, the original application contained an ignored `src/renamed.txt` with user-owned bytes. A fake worker ran `git mv src/a.txt src/renamed.txt` within its configured scope. The declared local check passed, the run became ready, and explicit application overwrote the ignored file with `0`.

The corrected addition inventory disables rename detection before filtering added paths. The durable `test_apply_preserves_ignored_user_file_at_rename_destination` regression passes in the final runner suite. Application now rejects this collision and preserves the original ignored bytes.

### IR-002 — A successful parent left executing descendants behind

**Severity:** High. **Status:** Closed.

The original cleanup skipped process-group termination after the leader exited. A local parent process spawned a same-group child that waited 0.3 seconds and wrote a marker, then exited successfully. With a 0.1-second timeout, the parent was reported successful in approximately 0.041 seconds, but the child wrote after the reported completion.

Cleanup now checks and terminates the owned group even after leader exit. A live leftover descendant produces `descendants-active`, which cannot pass verification. Linux zombie-only groups are distinguished from processes that can still act. The final independent reproduction returned `descendants-active` and produced no late marker. The corresponding child-survival regression passes.

### IR-003 — Post-merge effects were reported as an ordinary successful application

**Severity:** Medium. **Status:** Closed.

A disposable project's `post-merge` hook changed `README.md`. The original apply path returned `applied` while the resulting original worktree was dirty. The verified candidate commit did not describe those hook edits.

Application now records intent before the merge, inspects the resulting original HEAD and worktree, and preserves hook effects. Divergence produces `applied-needs-review`; uncertain application produces `application-unknown` instead of enabling automatic replay. The public CLI returns a nonzero exit status unless application is `applied`. The final `test_post_merge_hook_changes_are_preserved_and_need_review` regression invokes the actual root CLI and verifies exit status 1 and preserved hook edits.

### IR-004 — The total deadline excluded the final Git commit

**Severity:** Medium. **Status:** Closed.

The original Git wrapper used an independent fixed timeout, and no total-budget check followed the final commit. A one-second execution configuration with a temporary `pre-commit` hook that slept 1.5 seconds returned `ready` after 1.786 seconds.

The deadline now propagates through controller, worker, native/check and Git operations, including final commit and readiness checks. Git subprocess groups are bounded, and uncertain stopped mutations remain inspectable. On the final source, the same independent fixture stopped with `unknown` after 1.004 seconds for a one-second budget. The original application's source remained `0`; the run did not become ready or apply. `test_total_deadline_includes_final_git_commit_hook` passes.

### IR-005 — A real rejection could not be recorded while a semantic blocker was open

**Severity:** Medium. **Status:** Closed.

In new quick-route work at the tasks phase, a current analysis contained an open `ANA-001` blocker. Recording an actual `changes-requested` decision failed because the generic clean-state gate ran before distinguishing acceptance from rejection. This prevented recording the rejection precisely when the review requested changes.

The engine now permits a sourced non-accepting decision while semantic work remains pending, retaining structural, path, provenance and artifact-snapshot checks. Acceptance remains blocked. The installed-package regression `test_actual_rejection_can_be_recorded_without_accepting_a_semantic_blocker` passes.

### IR-006 — Missing required consultation guidance was reported as ready

**Severity:** Medium. **Status:** Closed.

After an actual bootstrap, deleting `.aws-workflow/workflows/consult.md` left doctor reporting `session_ready: true` and package readiness. The bootstrap and entry instructions treated that guidance as required, but doctor inspected only runtime modules.

Doctor now validates required reusable guidance as well as runtime modules, including installed content hashes. Bootstrap requires the matching source set before writing an installation. Final focused regressions cover missing/changed consultation guidance and an incomplete source package. In the independent installed-package recheck, deleting `consult.md` returned exit status 1, `session_ready: false`, and the exact missing path. Restoring that guidance and deleting only the optional hook handler left conversational setup ready. Editable project records remain editable.

### IR-007 — Preview fields leaked misleading execution claims

**Severity:** Medium. **Status:** Closed.

Static review identified that the initial execution record inherited `model_calls: 0` and preview `ready: true`. Those fields could misleadingly describe a real native run or a subsequently failed execution. No real model was invoked to establish this code-path finding.

The final execution record drops preview readiness. Native model calls and usage are reported as unknown (`null`); preview and injected local fixtures retain only their known zero-call observation. The final installed CLI fixture confirmed that execution and run-status output did not retain preview readiness and that model-call usage remained unknown for the native adapter class, even though the reviewer knew its temporary executable was fake.

## Specification and phase observations

The final specification module was independently inspected for source identities, structured response validation, actual review-note references, property-to-requirement/task/check mapping, blocker handling and deliberate reconciliation. All 25 focused fixtures passed. Requirements analysis remains current when downstream design/tasks are authored; required analysis/property gates are enforced for new structured work; design-first and quick phase behavior remains compatible; legacy work retains its selected contract behavior.

The operation owner identified and fixed an external-evidence reconciliation gap during the review. The final reviewer recheck changed property review notes without changing the canonical contract. The preview identified a property refresh, rewound to design, retained still-valid completion, and left the property result visibly stale. The module also binds separate response files, review notes and external finding/property sources, rejects stale import identities, and preserves historical records. This is deterministic freshness and linkage validation; semantic adequacy remains a performed human/model review obligation.

## Local verification observed by this reviewer

Each listed command returned exit status 0. Counts refer to the final relevant focused invocation, not cumulative reruns or a substitute for the integration owner's aggregate suite.

| Command | Cases | Result |
| --- | ---: | --- |
| `python3 -m unittest discover -s tests -p 'test_bootstrap.py' -v` | 25 | Pass |
| `python3 -m unittest discover -s tests -p 'test_doctor.py' -v` | 14 | Pass |
| `python3 -m unittest discover -s tests -p 'test_specifications.py' -v` | 25 | Pass |
| `python3 -m unittest discover -s tests -p 'test_runner.py' -v` | 26 | Pass |
| `python3 -m unittest discover -s tests -p 'test_context.py' -v` | 15 | Pass |
| `python3 -m unittest discover -s tests -p 'test_developer_workflow.py' -v` | 8 | Pass |
| `python3 -m unittest discover -s tests -p 'test_repository_checks.py' -v` | 14 | Pass |

These seven focused invocations cover 127 test cases. Individual adversarial reproductions and the installed CLI observation below were additional local checks. Older repository receipts were not relabeled as testing this implementation.

## Actual installed CLI observation with a temporary fake executable

The reviewer created a disposable committed Git application using the runner fixture, applied the actual source package in brownfield mode, and committed the additive installation. A temporary executable named `codex` was placed first on that subprocess's PATH. Its entire behavior was a small local Python fixture: read the prompt, write `A` to the scoped `src/a.txt`, and emit the required structured task result. It did not contact a model, service or account.

The reviewer invoked the installed entry at `.aws-workflow/scripts/workflow.py` with `--root` set to that temporary application and `--json`, using these exact operation arguments:

| Operation arguments | Exit status | Observed result | Original application value |
| --- | ---: | --- | --- |
| `run-plan --task T-001` | 0 | Preview ready; zero model calls | `0` |
| `run --execute --task T-001 --run-id review-installed-cli` | 0 | Isolated candidate ready; no inherited preview-ready field | `0` |
| `run-status review-installed-cli` | 0 | Candidate still ready | `0` |
| `run-apply review-installed-cli` | 0 | Applied after explicit invocation | `A` |

This sequence was repeated against the final frozen runtime and bootstrap identities below after the deadline and guidance fixes. It verifies package imports, CLI dispatch, native-adapter subprocess wiring with a fake executable, actual local verification, candidate isolation and explicit application. It is not a selected-client or real-model trial.

## Evidence limits and remaining acceptance

No real model execution, native hook activation, login, real credential access, plugin installation, client trust change, AWS account inspection or deployment occurred in this review. Credential-like files used by tests were disposable fixture markers. Git and subprocess commands operated in local disposable projects.

EARS diagnostics establish the supported sentence shape, not semantic correctness. Structured review imports establish declared provenance, source identities and references, not an authenticated reviewer or proof that reasoning occurred. Fixture review/acceptance statements are explicitly simulated. Passing declared local checks does not prove every application behavior, model judgment or AWS outcome.

Deadline and process-group outcomes were observed on this Linux environment. The controller is not a hostile-code sandbox; project commands, hooks, native controls and actual task authority retain their separate roles. This review does not establish other-platform behavior or selected-client interoperability.

The native-client acceptance task remains open until its concrete credit-consuming scope receives the required approval and the trial is actually observed. The final aggregate candidate run, publication and complete remote readback must be recorded by the integration owner before claiming those outcomes.

## Reviewed source identities

The following SHA-256 identities were re-read after final rechecks and verified again immediately before writing this receipt. They identify the reviewed files; the scope statement above defines how each was reviewed.

| Source | SHA-256 |
| --- | --- |
| `scripts/bootstrap.py` | `3772c12965653d5822651ba31e2940fe916d90bd69ae471021e06f4f5420ff14` |
| `workflow_engine/doctor.py` | `cc271f625bc85f79ae40de0b495e716fca2a27ee62e60d7227eb08a16d5073e7` |
| `workflow_engine/engine.py` | `9f878a215e8cd50eada8da0945510d3087d8b7b89dd400f0e4e69b89589f1b50` |
| `workflow_engine/context.py` | `7c86c897fa6b99b74d79dcaa8d06209c0475b1bbeb7d351592cb325c404aba71` |
| `workflow_engine/specifications.py` | `e944c657ed36d3e93903aca4b3ab4cd519a5dbeddc20c149cbbe8126992bb22f` |
| `workflow_engine/runner.py` | `10974db209e4ce6d3a9fd6a66751e2b5f8ca989f68b6224d838e33e3c48b8d95` |
| `scripts/workflow.py` | `f62cdac02f91f3f46cb3a5a556557cf5207ff687588401f0f347b65f796bf987` |
| `scripts/check_repository.py` | `6ef5c1e91eaeb0c52076a9265887429689c3008cbc3df592dc12e5a71e70095a` |

## Verification fixture identities

| Fixture | SHA-256 |
| --- | --- |
| `tests/test_bootstrap.py` | `a1705042f2594708e04a56c7919ae23008e8e69ef86589fc83fc81c8d1ce7326` |
| `tests/test_doctor.py` | `1a09173f45df58338843abca7c81717c1ce29daf4dbdaad8b5e789d5acdbc682` |
| `tests/test_specifications.py` | `a22d04f12b434fd53aba323e37cfd4c46b7da95a1d4e66e8aeb0332e5290e58e` |
| `tests/test_runner.py` | `e84b17eca22b77fc5083af52dd5679d72c2734b8a462d852d34b70676460a863` |
| `tests/test_context.py` | `b3f9b201aa85b0ad8f018ea7713abafa582b7021067ac4036c17d753e0399835` |
| `tests/test_developer_workflow.py` | `22ff01ed809e2db3a9fde5c6422f2903f4f8e5ec05d6630f772f44f3639719fb` |
| `tests/test_repository_checks.py` | `00517af12f0187f5e615b4eb42b2683866f08ec672f972628168b72acd9954c2` |
