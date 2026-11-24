# GitHub Codespaces readiness

Codespaces is a first-class development environment for this workflow. Keep the
existing configured Codex client, official AWS toolkit and project controls.
The ordinary in-session consultation works even when optional nested native
execution is unavailable. This template does not provision or authenticate a
client, install packages, alter trust, or create a background process.

## Check the correct execution context

Open a **regular VS Code integrated terminal in Codespaces**, rather than a shell
command launched by a running agent. The process that starts Codex must have
the supported access to its existing state directories. Do not elevate privileges,
remount protected paths, copy credentials into the workspace, or disable sandbox
or approval controls.

From the template checkout (or use the installed path in the application):

```sh
python3 scripts/workflow.py --root . native-check --pilot
# In an adopted application:
python3 .aws-workflow/scripts/workflow.py --root . native-check --pilot
```

This is a read-only metadata check, not a model invocation. The command returns
1 on a missing prerequisite, an apparently nonwritable state directory, or an
unresolved metadata check. A zero exit means **no known blocker**, not proven
native startup. The default native runner also checks these observable
prerequisites before reserving a run or dispatching a model. Ordinary
`doctor` still checks package and mapped context, independently of native
execution readiness.

Review the actual client version and available command options in that same
ordinary terminal:

```sh
codex --version
codex exec --help
```

Confirm the actual configured state locations in your existing supported client
configuration, without printing secret files or modifying the settings. Codex
defaults its state home to `~/.codex` unless `CODEX_HOME` is set. SQLite state
may use `CODEX_SQLITE_HOME`, but a configured `sqlite_home` takes precedence.
Other settings such as `log_dir` may also affect startup. The metadata check does
not read configuration or authenticate, cannot see configured overrides, and
cannot prove file-specific write access or policy permission. Relative environment
overrides require operator review; the preflight conservatively refuses them.

| Observation | Smallest useful next step |
| --- | --- |
| Ordinary terminal shows no known blocker; nested agent shell reports read-only state | Use the ordinary terminal for the separately authorized native trial, preserving the documented sandbox and approval settings. Do not launch it recursively from the restricted agent. |
| Ordinary terminal also reports read-only state | Stop. Have the environment owner restore supported client state access or use an existing authorized configured client. Do not bypass a managed mount. |
| Client or required executable missing | Use the official setup instructions through the user's normal installation process. Do not install as a side effect of preflight. |
| State directories appear writable but startup fails | Retain the actual sanitized startup error; review actual configured locations and client controls with the environment owner. Do not repeat an allocated pilot stage. |

For the frozen native pilot, run the preflight **before any stage reservation**,
from the actual launching terminal and project directory. If it reports a
blocker, stop without consuming another invocation allocation. Also verify the
actual client interface and operator-controlled authorization required by
the original pilot plan. A previously failed launch is still a consumed slot.
Any replacement needs fresh explicit authorization; do not reset the prior
stage ledger, modify the frozen prompts, or add automatic retries.

## Start the natural consultation

Open the adopted application root in Codex and type **`start`** (or say
“Start my AWS project”). Codex checks local setup and reads the mapped context
using the [quickstart](00-quickstart.md). On first use, it should welcome the
developer, reflect known intent and ask only material questions. For example:

> Welcome! I'll be your AWS consultant and delivery partner. I'll help turn
> your idea into a practical design, requirements, tasks, and verified work.
> What outcome are you trying to deliver, and who will use it?

If a goal or existing project is supplied, reuse it and explain the next
recommendation instead of asking again. Save actual answers in the mapped
records. Resume saved consultation or implementation on later turns.
Installation and hooks do not send unsolicited messages or authorize model
runs or AWS operations. The native pilot is needed to observe actual client
behavior; this greeting is guidance, not a guaranteed client UI feature.

Official references:
[Codex environment variables](https://learn.chatgpt.com/docs/config-file/environment-variables),
[configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference),
[GitHub Codespaces persistence](https://docs.github.com/en/codespaces/developing-in-a-codespace/persisting-environment-variables-and-temporary-files).
