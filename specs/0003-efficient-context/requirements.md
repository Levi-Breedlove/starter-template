# Requirements: focused context and measured efficiency

**Route:** Quick, with one combined technical review.  
**Scope source:** The user requested the most efficient effective workflow available for the Codex AWS template.  
**Authority:** Improve this repository and verify locally. Existing boundaries for account operations, client trust and paid/background trials remain in force.

## Goal

Reduce unnecessary context and repeated work while preserving required outcomes, authority, source inspection and evidence. A local improvement must have observable results; no global-best or model-quality ranking is implied.

## Behavioral contract

| ID | Required outcome | Acceptance criterion | Required or deferred |
| --- | --- | --- | --- |
| REQ-001 | Offer bounded, actionable context without removing full inspection. | `context --compact` and startup summaries obey a 6000-character cap; full context/status/JSON remains compatible and complete. | Required |
| REQ-002 | Avoid repeating full startup context every prompt. | Refresh text obeys a 1200-character cap, reports a stable full-report fingerprint and tells the agent when to reload; no persistent hook cache or skipped inspection. | Required |
| REQ-003 | Preserve the most consequential context under pressure. | Long titles, paths and old task history cannot displace current errors; omissions have counts/references; next tasks include relevant dependency/contract/check identifiers. | Required |
| REQ-004 | Suggest the next action according to current route and phase. | Quick work does not invent separate review gates; planned/complete states do not authorize more execution; current blockers outrank future questions and normal work. | Required |
| REQ-005 | Apply a concise, quality-first efficiency policy in source and adopted projects. | Entry instructions use compact context, selective loading, useful bounded delegation, affected checks and real required gates; correctness/authority failures cannot be offset by cheap output. | Required |
| REQ-006 | Preserve read-only behavior, safe adoption and prior workflow semantics. | Regression suite and actual-source adoption pass; missing new runtime modules block before writes; native responses do not mutate state or force model continuation. | Required |
| REQ-007 | Report measured improvements with honest limits. | Compare old/new renderer payloads on identical frozen fixtures, keep exact source identities and distinguish characters from tokens/cost/real model behavior; publish and read back the current tree. | Required |

## Existing decisions

The local tool remains standard-library Python. This slice adds one focused projection and an operating policy, not a worker daemon, replacement AWS plugin or language rewrite. User steering always takes precedence over reuse hints. A report fingerprint does not establish unchanged unread source files or external state.

[Design](design.md) · [Tasks and verification](tasks.md) · [Review](../../evidence/0003-efficient-context/review.md)
