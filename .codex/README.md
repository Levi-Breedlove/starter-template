# Native Codex integration

This directory includes `hooks.json`, a concrete read-only lifecycle adapter definition. It also may contain `workflow.json`, which selects active work for the local workflow tool. The two files have different purposes: one configures supported Codex events, the other is this project's own data format.

See [native hook setup](../docs/reference/native-hooks.md) for behavior, exact trust requirements and adoption. Offline tests verify the handler; they do not prove that the current client loaded or trusted it. The adoption helper does not copy this directory into application projects.

The [root instructions](../AGENTS.md) provide an explicit fallback: load active context and validate recorded claims through the CLI when hooks are unavailable. This repository does not replace Codex's model, sandbox, permission controls or native user interface.
