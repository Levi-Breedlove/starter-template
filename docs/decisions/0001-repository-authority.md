# Decision 0001: Repository authority and adaptation boundaries

**Status:** Implemented scaffold organization; not an assertion of owner approval of every future runtime choice.  
**Date:** 2026-11-21 (America/Los_Angeles).  
**Scope:** The requested Codex AWS bootstrap repository.

## Context

Kiro combines context, specifications, tools, automation, and runtime behavior. Copying its directory names into a Codex repository would leave important behavior unspecified and could imply nonexistent native compatibility. Existing AWS projects also differ in stack, layout, task authority, and delivery system.

## Decision

Use a concise root `AGENTS.md` to route Codex to explicit workflow procedures. Keep behavior, design, tasks, and evidence connected through stable work identifiers. Use one canonical task record for each work item and a handoff that links to it. Keep current framework requirements separate from an adopting application's work.

Store native Codex adapter plans separately from active configuration. Add hooks, machine schemas, runners, or optional local skill packaging only through their implementation tasks and supported product mechanisms. Do not duplicate canonical specifications under `.kiro/`.

Use the official AWS toolkit as the AWS adapter. Preserve existing official plugin identities and each project's chosen IaC/delivery system. Keep greenfield and brownfield entry procedures explicit. In an existing project, map these responsibilities onto existing authority before changing paths or trackers.

## Consequences

The scaffold is useful as instructions now and honest about its runtime gaps. The tradeoff is that advanced parity needs implementation and maintenance rather than being implied by a file layout. A future importer, dashboard, or tracker integration must reconcile with the declared authority instead of creating a competing state source.

## Alternatives considered

| Alternative | Reason not selected for this delivery |
| --- | --- |
| Copy `.kiro/` files verbatim | Does not create Codex event/runtime semantics and risks duplicated authority. |
| Reuse the owner's private skills | Conflicts with the explicit request for independent research and design. |
| Build a full runner before validating the workflow | Adds integration complexity before the behavioral contracts and evaluation cases are established. |
| Mandate one AWS architecture/pipeline | Makes a general greenfield/brownfield bootstrap less useful and can disrupt existing systems. |

## References

[Research synthesis](../research/README.md), [workflow architecture](../workflow-architecture.md), [adapter contracts](../adapter-contracts.md), and [foundation specification](../../specs/0001-workflow-foundation/requirements.md).

