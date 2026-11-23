# Design: complete developer workflow

**Contract:** [Requirements](requirements.md).  
**Route:** Requirements-first; technical implementation/review delegated by the repository owner's request.

## DES-001 — One application entry

A read-only doctor inspects local package completeness, mapped context and selection state, plus executable availability. It does not inspect credentials, authenticate, invoke a model or contact AWS. Hook configuration is generated as a preview; client trust remains a native control. The additive installer includes every required runtime module and a bounded ignore block for private execution state.

## DES-002 — Specification operations

A dedicated module supplies EARS pattern diagnostics, source-bound requirements-analysis requests, property-derivation requests and validated append-only result records. Codex performs semantic reasoning in its current session, or an explicitly selected external invocation. The tool validates identities, fields, references and unresolved blockers. Static diagnostics and semantic review are separate observations. New CLI work opts into the structured contract; older schema-1 work remains compatible.

Analysis binds the contract and material consultation context; it must not become stale merely because downstream design/tasks are authored. Properties bind contract/design and validate task links when the task plan exists. Review requirements are phase-aware and preserve design-first sequencing. Quick work avoids separate requirements/design approval pauses while retaining combined readiness and actual authority.

## DES-003 — Bounded execution and candidate isolation

An execution configuration maps existing task/check IDs to explicit write scopes, verification argv and input paths. It adds limits and a real authority reference without becoming another completion tracker. Planning is read-only. Foreground execution is an explicit opt-in through the installed Codex CLI adapter; no model invocation runs during ordinary context/status operations.

A clean committed Git project is required for native execution. The controller creates a separate candidate worktree and isolated worker worktrees. Independent tasks with disjoint scopes may run concurrently; overlapping scopes serialize. Worker statements are claims. The controller observes process exit, validates structured output and patch scope, executes the declared checks, integrates into the candidate and records current evidence. The original application remains unchanged until an explicit apply against its expected clean identity.

Persist dispatch intent, outcome and consumed limits. A crash or uncertain subprocess effect is visible as unknown and is never automatically replayed. Failures remain inspectable. No automatic retry, unlimited loop, forced stash, force overwrite, sandbox bypass, trust bypass or credential configuration is allowed. Configuration commands are trusted executable project policy, not a security sandbox; native permissions and IAM remain authoritative.

## DES-004 — Reconciliation and continuation

A reconciliation preview identifies changed snapshots, stale reviews and invalid task/check outcomes, plus regeneration instructions. Applying the same reviewed fingerprint reopens affected completion and rewinds the phase to the earliest necessary boundary. Stable task IDs, unaffected work and previous receipts remain. A semantic change is resolved by Codex with source review, not guessed by a hashing function.

## DES-005 — Integration and developer experience

The existing CLI gains setup, analysis, property, synchronization and runner commands. Existing full inspection commands keep their contracts. Hooks/compact context expose material new blockers without unbounded history. Root/adopted entry instructions guide the ordinary conversation and use executable operations where deterministic support exists. The quickstart names prerequisites, both adoption paths, actual artifacts, operator choices and the difference between local checks and native/cloud observations.

## DES-006 — Evidence and delivery

Use fake model backends with real temporary Git worktrees/process checks to test success, dependencies, parallel scope conflicts, stale candidates, failed verification, timeouts and interrupted state. Actual-source application tests cover package completeness and CLI wiring. A reviewer outside the implementation scopes inspects concrete code and challenges authority/freshness assumptions. Preserve historical receipts and reconcile affected current claims using new observations.

The native integration trial is a distinct acceptance task. Prepare exact commands, fixture inputs, invocation limits, expected observations and credit implications before requesting its approval. No live AWS deployment is needed to establish the repository's local spec workflow; cloud outcome claims require a separately authorized concrete project.

[Execution plan](exec-plan.md) · [Tasks](tasks.md)
