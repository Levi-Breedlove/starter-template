# Native Codex integration boundary

This directory currently contains documentation only. It does not activate project configuration, hooks, custom agents, a workflow runner, or permissions.

The [root instructions](../AGENTS.md) and [workflow procedures](../workflows/README.md) are the immediate operating layer. The [adapter contracts](../docs/adapter-contracts.md) specify deeper behavior and the [foundation tasks](../specs/0001-workflow-foundation/tasks.md) own its implementation.

## Proposed native mapping

| Need | Supported product foundation to verify | Project implementation |
| --- | --- | --- |
| Persistent project guidance | Root and scoped AGENTS instructions | Keep the root router concise; load relevant contract and accepted decisions. |
| Lifecycle checks | Trusted `.codex/hooks.json` or supported inline config | Choose one source per layer; implement bounded deterministic handlers. |
| Specialized execution | Supported custom agents and subagents | Investigator, designer, implementer, reviewer, and verifier with bounded scopes. |
| Machine worker interface | Non-interactive exec or SDK; App Server if justified | Validate requests/results, candidate identity, limits, and actual artifact evidence. |
| Continuation | Native session resume plus repository handoff | Preserve work state and assess freshness; later add durable run state. |
| AWS knowledge/tools | Existing official AWS plugins | Verify actual availability without duplicating installation identity. |

Suggested roles are responsibilities, not registered agent names. The reviewer must receive a fresh context and the concrete candidate. The AWS release role, if added, cannot infer operational authority from its name or tools.

## Capability verification

Before creating active configuration, read current official [hooks](https://learn.chatgpt.com/docs/hooks), [subagent](https://learn.chatgpt.com/docs/agent-configuration/subagents), and [configuration guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md). Confirm the actual client's schema and support. Record the result in the project's environment-capability record.

Do not use a trust-bypass flag to make an unreviewed hook run. A project file cannot confer model budget, tool authority, AWS permission, or a hosted feature entitlement. Local support does not prove hosted support.

