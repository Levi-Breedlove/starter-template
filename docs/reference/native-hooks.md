# Optional native Codex hooks

The bootstrap supplies [a hook definition](../../.codex/hooks.json) and [a read-only handler](../../scripts/codex_hooks.py). They use documented Codex events. The definition is present; trust and actual loading in the adopter's client remain separate observations. [Official hook documentation](https://learn.chatgpt.com/docs/hooks)

| Event | Handler behavior |
| --- | --- |
| `SessionStart` | Inject a compact summary capped at 6000 characters: current problems first, next action, relevant tasks, sourced answers and references. Includes resume/compaction sources. |
| `UserPromptSubmit` | Send a refresh capped at 1200 characters with the report fingerprint, current problems and next action. Reload compact context if no packet is loaded or the fingerprint changes. |
| `Stop` | Show a warning for structural validation errors. Never force another model turn or block a legitimate interview pause. |

The handler reads the active pointer and workflow records. It does not run tests, shell commands, model calls, AWS calls, migrations, installs, or task mutations. No active pointer means no arbitrary work selection. Errors remain visible; they are not converted to passing validation. Input/output sizes and execution time are bounded. Packet limits count serialized JSON characters, including escaping; the CLI's terminal newline is separate.

## Enable on a selected client

For a Git checkout of this bootstrap, `.codex/hooks.json` resolves the handler from the Git root so nested working directories work. Review the actual script and hook definitions using the client's supported `/hooks` flow. Codex requires trust in the exact definition; changed definitions can need review again. Do not bypass trust or duplicate the same hooks in another configuration source.

The adoption helper deliberately does not modify `.codex` or client trust. In an adopted Git repository, merge the three definitions into the project's chosen hook configuration source only after reviewing existing hooks. Change each handler command to:

```json
"python3 \"$(git rev-parse --show-toplevel)/.aws-workflow/scripts/codex_hooks.py\""
```

Keep the `timeout` at 5 seconds. The supplied definitions use `additionalContextLimit` 2500 for startup and 1000 for prompt refresh; these are host token thresholds, separate from the handler's character caps. For a non-Git directory, use a reviewed absolute script path. The supplied command targets a POSIX shell with `python3`; Windows or hosted clients need a verified equivalent and supported hook surface. Do not claim activation from the presence of a configuration file.

The refresh has no persistent cache and does not skip validation. Its fingerprint identifies the inspection report, not all repository files or external state. Read required sources before using them, inspect changed inputs, and apply the current user request even when the fingerprint matches. Full `context`, `status` and JSON reports remain available for deliberate inspection. See [efficient operation](efficient-operation.md).

## Verify without using a model

The event contract is exercised by `tests/test_codex_hooks.py`: valid JSON, no-active-work behavior, saved answers, bounded context, wrong-workspace rejection, invalid input and nonrecursive completion reminders. Full integration tests additionally exercise actual workflow records in a temporary repository.

A real selected-client trial should show the configured source, trusted definition, received context and expected warning behavior. It has not been substituted by these fixture results. Record the actual client/version and observations in the environment-capability record.

Without native hooks, the workflow remains usable: `AGENTS.md` directs Codex to run `workflow.py context --compact` at entry/resume and `workflow.py validate` before completion claims. Hooks are convenience and feedback, not an authorization or security boundary.
