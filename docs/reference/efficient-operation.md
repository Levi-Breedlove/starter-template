# Efficient operation

Aim for the least unnecessary work that still establishes the requested outcome. The [evaluation protocol](../../evaluations/README.md) measures that claim; no unmeasured worldwide-best or model-superiority claim follows from the template's design.

## Match depth to the work

| Depth | Use when | Expected work |
| --- | --- | --- |
| Direct | A small change is understood and has no consequential ambiguity. | Inspect the relevant context, make the change and perform proportionate verification. |
| Quick | A bounded change needs connected planning but its material questions can be resolved up front. | Clarify, draft the connected artifacts and conduct the combined review. |
| Standard | Uncertainty, dependencies or consequential tradeoffs need staged investigation. | Follow the selected requirements-first or design-first sequence, with the actual reviews and evidence required by the project. |

Bugfix and planning-only work retain their specific contracts. Route names should not become another questionnaire. Reuse accepted decisions and ask only the next consequential gap. Apply stronger reasoning to ambiguity, architecture, difficult failures and consequential review; use a lighter approach for bounded work only when the resulting quality is sufficient. Do not change the selected model or settings merely because a generic ranking suggests it.

## Keep context actionable

Use `context --compact`: a startup packet capped at 6,000 serialized characters and a prompt-refresh packet capped at 1,200. The limits include JSON escaping and exclude the CLI's terminal newline. Current implementation verification belongs to the work receipt linked from the [handoff](../../delivery/current-handoff.md). These are character limits, not measured token or cost claims.

Use the packet to find the current phase, consequential questions, blocking issues and next eligible work. Read required source records that have not been inspected. Reuse already loaded context when the report fingerprint and relevant sources remain current; do not reread every guide on every turn. A matching fingerprint means the report is unchanged, not that external systems or every source file are unchanged. A changed request, source conflict or unavailable evidence requires reassessment.

Keep full status/audit inspection available for detail and make omitted information visible. Compact output must not silently turn blocked or stale work into readiness. OpenAI recommends concise hook/plugin context because accumulated output can impair performance. [Hook output guidance](https://learn.chatgpt.com/docs/hooks)

## Delegate and verify for a reason

Use separate agents for bounded independent investigation, implementation scopes or fresh review when the expected quality or elapsed-time benefit justifies coordination. Give each agent a concrete question, relevant inputs, write ownership and a completion condition. Return findings and evidence references instead of raw logs. Keep one integrating owner and verify the combined candidate.

Subagents perform additional model/tool work. Official guidance highlights read-heavy parallel tasks and cautions that concurrent editing adds conflict and coordination costs. Agent count is therefore not a measure of effectiveness. [Subagent guidance](https://learn.chatgpt.com/docs/agent-configuration/subagents)

Run checks affected by the actual change, then required integration gates. Repeat checks for changed inputs, a reproduced failure or a required gate. Once the evidence resolves the concrete risk and requirements, finish delivery rather than adding optional tests or documentation. A missing required result remains unfinished.

## Use code for exact rules

The local engine checks identifiers, dependencies, phase preconditions and declared evidence freshness. The installer checks paths and collisions. Codex supplies interpretation, recommendations and meaningful verification. A hash cannot authenticate a review or prove a test ran. Use the existing [tooling contract](workflow-tooling.md); do not create a parallel task tracker or bypass actual client, CI or AWS controls.

Measure improvements with the frozen greenfield/brownfield pilots in the existing evaluation protocol. This document starts no paid/model/native-client/AWS trial, installs no plugin and enables no background service. Continue within actual task authority and report unobserved results as unobserved.
