# Design: executable consultant workflow

**Route:** Quick, assembled and reviewed as one connected contract.  
**Contract:** [Requirements](requirements.md).  
**Decision basis:** Authorized repository maintenance; the agent makes reversible technical implementation choices within the user's stated constraints.

## DES-001 — Guided consultation with saved decisions

Root instructions route Codex into an adaptive interview. The agent reads known context, derives engineering implications, researches technical uncertainty and recommends a next step before asking up to three consequential questions. Project-wide answers stay in the brief; work-specific decisions stay in the contract. Metadata indexes their sources. Both greenfield and brownfield examples illustrate this behavior without claiming an executed model trial.

Routes use distinct artifact review order. The quick route has one combined review; prior delegated decisions remain usable within scope. Brownfield entry preserves existing code, layout, infrastructure ownership, pipeline and document authority. Official AWS guidance remains the service expertise layer, separate from task authorization.

## DES-002 — Deterministic local workflow core

A standard-library Python package and CLI operate on schema-1 `work.json` plus canonical Markdown. Read-only inspection derives task status, ready dependencies, question state, review freshness and issues. Mutations create work, record supplied review/result provenance and check phase advancement. No command launches a model, test, shell or AWS operation.

The parser accepts documented ID/field conventions rather than arbitrary Markdown. Canonical task checkboxes own completion. Review snapshots bind meaningful artifact revisions; task progress fields are normalized so a routine checkbox update does not require another plan review. Evidence binds contract/design, the relevant task/check definition, receipt and declared tested inputs. Required coverage and dependency results are checked before completion.

Safe-path checks reject unsafe destinations and Git metadata. Atomic file replacement limits partial JSON writes; no concurrent-writer merge is promised. Recording a result is not execution proof. The agent must supply complete relevant inputs and truthful observations.

## DES-003 — Additive application adoption

The source helper previews a deliberate copy map and installs `.aws-workflow/` plus a bounded root instruction block. Existing project records are mapped; missing records receive fresh application context. Source framework specs, evidence and native client configuration are excluded. A manifest records identities and paths, enabling exact reruns and collision detection.

Preflight rejects overlapping roots, traversal, symlink hazards, changed managed content and ambiguous existing markers. Write failure rolls back the helper's own completed writes where possible. Cross-process mutation and abrupt process/power-loss recovery remain outside this helper's transaction guarantee; semantic instruction merging remains the consultant's responsibility.

## DES-004 — Native feedback and integration

The native adapter consumes documented JSON and imports the read-only engine. Session start and user prompt events provide bounded context; stop events provide warnings without restarting the turn. Missing active work leaves selection to the consultation. Malformed input and inaccessible metadata produce visible, bounded responses. The supplied POSIX/Git command is a fixture-tested definition, not a declaration of client trust or loading.

Framework integration replaces obsolete references with standalone contracts, retains historical receipts under their original scope, and updates current capabilities/handoff. Tests use temporary local projects and fake receipts. The release verification compares the full published tree to the prepared manifest without accessing AWS.

## Tradeoff and next evidence

Python keeps the current runtime easy to inspect and run. A future compiled distribution can preserve the CLI and JSON contract if packaging, concurrency or measured performance justifies it. The next behavioral evidence should be a bounded real-client greenfield/brownfield trial, followed by a separately authorized AWS exercise where needed. No language choice can authenticate a model's claim by itself.

[Implementation tasks](tasks.md) · [Combined review](../../evidence/0002-consultant-workflow/review.md) · [Verification](../../evidence/0002-consultant-workflow/verification.md)
