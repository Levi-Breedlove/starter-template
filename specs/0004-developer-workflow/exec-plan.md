# Execution plan: complete developer workflow

## Goal and completion rule

Deliver a practical reusable workflow for AWS developers using Codex: first-use setup, adaptive consultation, formal specifications, requirements analysis, correctness properties, task execution, change reconciliation and continuation. Keep the source neutral and retain the user's selected AWS plugins and project authority.

The canonical completion checklist is [tasks.md](tasks.md). This plan explains sequencing and decisions; it is not a second status register. The full target includes an observed native-client trial. Local implementation can be delivered independently, but that does not close native behavior or comparative claims.

## Baseline and concrete gaps

Base revision: `200016c62f10fe1a7eb164584f3b7ab794450a41`. Existing capabilities include additive adoption, consultant instructions, phase/review/evidence checks and bounded context. The gaps are explicit EARS patterns, first-class recorded semantic operations, property generation/traceability, a bounded task execution controller, deliberate reconciliation commands, and a complete first-user entry with setup diagnostics.

The existing 105-test receipt remains historical. Its passing observations are not relabeled as testing new code. Earlier work items are revalidated only where shared inputs change.

## Work sequence and ownership

| Step | Concrete deliverable | Owner and integration seam | Exit evidence |
| --- | --- | --- | --- |
| 1 | Requirements, design, task graph and this plan | Root integrator; existing task authority | Actual scoped technical review |
| 2A | EARS diagnostics, analysis/property requests and result records, reconciliation | Specification module owner; pure/read-only requests and explicit mutations | Focused source/freshness/semantic-boundary tests |
| 2B | Foreground bounded native adapter, isolated candidate/worker worktrees, verification and apply | Execution module owner; plan/execute/status/apply API | Fake-backend tests using real Git/process behavior |
| 2C | Doctor, hook preview, complete package mapping, fresh developer guide | Onboarding owner; setup APIs and additive installer | Greenfield/brownfield preservation and packaging tests |
| 3 | CLI wiring, new-work policy, context/phase integration, root documentation | Root integrator after stable APIs | Actual installed-package command flow |
| 4 | Independent review and combined verification | Fresh reviewer plus root integration | Concrete findings resolved; current source identities |
| 5 | Expected-head publication and full file readback | Root integrator | Observed source and completion-record identities |
| 6 | Bounded native-client pilot | Approved operator in selected client | Actual model/client behavior; no fixture substitution |

Parallel writers have disjoint files. The integrating owner controls CLI, engine changes and final contract coherence. No worker may claim independent review of its own code.

## User experience to implement

1. Preview/apply the reusable workflow into a separate new or existing application.
2. Run a read-only setup check, then describe the desired outcome in ordinary conversation.
3. Codex reads mapped project records, preserves existing decisions, recommends an approach and asks only consequential gaps.
4. Codex saves answers, selects a work route and drafts requirements in explicit structured patterns.
5. The analysis operation prepares a precise review request; Codex supplies semantic findings with sources and the tool validates/records them.
6. Design and correctness properties connect requirements to tasks and verification. Reviews use actual user or delegated authority.
7. Continue in the current Codex session, or preview a bounded execution configuration and explicitly choose native foreground execution.
8. Native execution works in isolated candidates; declared checks and integration determine readiness. Application is a separate expected-state action.
9. Requirement/source changes produce an impact preview and deliberate reconciliation. Resume uses current records and does not repeat uncertain operations.
10. Project-specific release and AWS observations follow existing project controls; the template does not silently provision accounts or deploy.

## Design decisions and tradeoffs

Use standard-library Python and the existing CLI/JSON interface. A language rewrite would not supply semantic judgment or prove workflow equivalence. Separate read-only preparation from effects. Static EARS checks validate form, while model/human analysis validates meaning. Persistent operation results identify inputs and findings; they never invent review authority.

Use a foreground task controller rather than a daemon. Its execution configuration names trusted verification commands and explicit scopes. Isolated candidate worktrees make failure/review inspectable and preserve the original application. Require a clean committed project for this optional mode; ordinary conversation can still work with an existing dirty tree under normal care.

Do not auto-enable hooks, overwrite client configuration, bypass trust, install duplicate plugins or use account credentials for setup. Run all offline verification first. A real native model trial can consume the user's credit balance and therefore requires their previously specified manual approval; prepare its exact scope before that final decision.

## Verification strategy

Test meaningful failure modes: malformed/spec-stale responses; unaddressed blocking findings; nonexistent references; design-first and quick sequencing; changed input state; overlapping write scopes; worker failure/timeout; missing verification; interrupted dispatch; integration failure; dirty original tree; symlinks and path escapes; incomplete packaged runtime; and no-active-work startup.

Use real temporary projects, Git worktrees and local verification subprocesses with a fake model adapter. These prove controller behavior but cannot establish model quality. Exercise the actual adopted package and documented entry commands. Review source and provenance, then run required combined checks once the integrated candidate is stable.

The native pilot uses two disposable projects with fixed goals and rubrics, one greenfield feature and one brownfield defect. Include a changed requirement and session interruption. Record selected client/model, actual invoked commands, limit consumption, inputs, artifacts, useful questions, corrections, check outcomes and continuation. No AWS account access is needed for this pilot. AWS release/recovery is a later project-specific task with a named environment.

## Checkpoints and recovery

After each independent scope, record API behavior and actual tests. Keep a current handoff and immutable local receipt. If an execution outcome is unknown, inspect retained state; do not replay it blindly. If the remote branch moves, reconcile against the new head instead of forcing publication. Leave every unperformed acceptance item visibly open.

## Initial release for starter-template

The readiness candidate is tracked in the existing `codespaces-readiness`
pull request. Keep this plan and [the task ledger](tasks.md) as the delivery
authority. Native observations identify the pinned source and client. Any
later change to reusable instructions or files needs matching offline
verification and a decision about the scope of prior native observations.

1. Complete the frozen pilot within its recorded authority. Review all
   outcomes and keep T-008 open while a required observation is unresolved.
2. Verify the existing official AWS toolkit and optional AWS Emulator guidance
   with public sources. Record actual installed/runtime capability separately
   from the guidance and its offline checks.
3. Inspect the default-branch snapshot GitHub would copy. Produce and verify
   a clean, initialized local candidate with the existing bootstrap. Keep
   maintenance records and native receipts in their original history. Review
   the distribution choice before changing the repository default branch or
   creating another remote repository.
4. Verify the exact candidate with clean greenfield initialization, additive
   brownfield adoption, installed workflow scenarios, the complete regression
   suite and repository checks. Reconcile the affected checks and handoff.
5. Update the existing pull request against its expected head. Release and
   freeze v1.0.0 after the required native observations, distribution,
   exact-candidate proof, and applicable GitHub reviews are accepted.


For packaging, generate one editable project brief plus project requirements, technology, structure, and system architecture. Preserve mapped brownfield sources and earlier installs. Each feature or defect links to the applicable foundations. Test source-bound reconciliation, accurate first-use and continuation, and the seven conversational shortcuts on the distributed tree.

Keep the development history on `main` and generate a clean `template` branch in this private repository. The final native observation uses one literal `start` against the exact distributed tree, a 360-second cap and zero retries. Obtain its separate authorization before launch. The operator verifies both adoption modes, the exact Git tree, the default branch, the release tag and review controls. [Distribution procedure](../../docs/distribution.md)
