# Bounded task execution

The workflow can execute one task or a dependency-ordered set of tasks through the
installed Codex CLI. The default is a read-only plan. Native execution is an
explicit foreground operation that can consume model credits; the repository
does not start it during adoption, context loading, or validation.

Execution creates a separate candidate Git worktree. Independent tasks use their
own worker worktrees, and overlapping write scopes are serialized. The original
application stays unchanged until the developer explicitly applies the verified
candidate. The controller records attempts and check observations; `tasks.md`
remains the sole task completion authority.

## Prerequisites

Use the application Git root, with a committed `HEAD`, clean tracked/untracked
work, and `.workflow-state/` effectively ignored by Git. Preserve and reconcile
existing edits; the controller never stashes, discards, or force-commits them.
The reviewed work must be in implementation or verification, with current
requirements/design/task reviews and no applicable blocker.

The selected environment needs Git, Python 3.10+, and the application dependencies
needed by its declared checks. Worktrees contain committed project files; they do
not copy a working directory's ignored virtual environments, build output, or
uncommitted dependencies. Choose reproducible check commands for that environment.
Native model execution additionally needs an already configured Codex CLI and
actual authority for that invocation. Setup and authentication remain outside
these commands.

Native process-tree timeout/cancellation currently targets a POSIX environment
(Linux/macOS, or WSL on Windows). Other platforms can use the normal Codex session
workflow and read-only planning; the native backend refuses to claim equivalent
process-tree control there.

The native adapter uses documented `codex exec` structured output and a
`workspace-write` sandbox. It preserves client approval, trust, and configuration
controls. A blocked native operation stops visibly. Source implementation and
mocked invocation tests do not establish that the selected client has executed a
real task successfully. [Official non-interactive interface](https://learn.chatgpt.com/docs/non-interactive-mode)

## Define the execution policy

Create `specs/<work-id>/execution.json` after requirements, design, tasks and their
actual reviews are ready. The CLI can return an execution template with known task
and check IDs. Its authority, scopes and commands are deliberately empty: Codex
must derive these from the accepted work and inspect them before execution.

For example, a single-task policy can look like this once the referenced project
files, decision, checks and command actually exist:

```json
{
  "schema_version": 1,
  "authority_ref": "docs/decisions/local-implementation.md",
  "limits": {
    "max_workers": 2,
    "max_tasks": 8,
    "timeout_seconds": 1200,
    "check_timeout_seconds": 120
  },
  "tasks": {
    "T-001": {
      "write_paths": ["src/booking.py", "tests/test_booking.py"],
      "checks": [
        {
          "id": "CHK-001",
          "argv": ["python3", "-m", "unittest", "tests.test_booking"],
          "inputs": ["src/booking.py", "tests/test_booking.py"]
        }
      ]
    }
  },
  "integration_checks": [
    {
      "name": "application-regression",
      "argv": ["python3", "-m", "unittest", "discover", "-s", "tests"],
      "inputs": ["src/", "tests/"]
    }
  ]
}
```

This is an illustrative policy, not a command to run against the bootstrap itself.
The authority reference identifies an existing nonempty project decision. The
file cannot grant permission or authenticate the decision's author. All commands
are trusted project code: an argv array avoids shell interpolation, but cannot
prove that a Python program, test, Git hook, or model tool has no external effects.
Review the actual commands and preserve native permissions, IAM and delivery
controls. Keep credentials out of the policy and evidence.

| Field | Contract |
| --- | --- |
| `write_paths` | Exact project-relative files or directory prefixes ending in `/`; no traversal, globs, symlink components, workflow ledger, installed package or client-control paths. These constrain integrated Git-visible patches, not the operating system. |
| `checks` | Each selected task's exact canonical check IDs, with explicit argv and source/fixture inputs. Already completed tasks also need mappings so later changes can revalidate their evidence. Automated task checks need distinct IDs; shared checks belong in integration checks. |
| `inputs` | Existing files or directories at verification time. Directories expand to Git-tracked/staged files; ignored build output is excluded. Include every relevant input needed to support the claim. |
| `integration_checks` | At least one named check for the combined candidate. It runs after each wave before any new task is marked complete. |
| `limits` | 1–4 workers, 1–100 selected tasks, total runtime 1–7200 seconds, and each check 1–600 seconds. There is one attempt per task in a run, with no automatic retry. |

Time and task limits do not create a hard monetary or token cap. The controller
records invocation intent and actual local observations; unknown usage remains
unknown. Model stdout and check output are bounded and kept in ignored runtime
state. Git-visible source changes and declared inputs must remain unchanged
during checks. Ignored local build output is not imported into the candidate.
The shared total deadline also bounds Git operations, including candidate commit
hooks. A timed-out mutation remains unknown until its retained state is inspected.
Same-process-group descendants left behind after a successful parent exit are
terminated and make that process result unsuccessful. This is process-group
cleanup, not containment of deliberately detached processes or external effects.

## Plan, execute, inspect, and apply

From the application root, use the installed CLI path:

```sh
python3 .aws-workflow/scripts/workflow.py --root . run-plan
python3 .aws-workflow/scripts/workflow.py --root . run --task T-001
```

Both commands above are previews. Omitting `--task` selects all unfinished tasks.
The plan reports explicit blockers and dependency waves. A single-task request
does not silently execute an unfinished prerequisite. The plan performs no model
call and creates no runtime state.

Only when the execution policy, chosen scope and model invocation are authorized:

```sh
python3 .aws-workflow/scripts/workflow.py --root . run --execute
```

The controller then:

1. Rechecks the clean original candidate and records intent before dispatch.
2. Creates a detached candidate worktree and independent worker worktrees.
3. Dispatches at most the configured worker count for one dependency wave.
4. Validates each structured result and checks its patch against the declared
   write scope. A blocked/malformed result, changed Git control state, unsafe
   path, unsupported file type or oversized patch stops the run.
5. Applies compatible patches to the separate candidate and independently runs
   the exact local task checks and integrated-candidate checks.
6. Rechecks previously completed tasks because later changes can invalidate their
   declared inputs. Each wave gets new immutable check receipts; older receipts
   remain history.
7. Records actual check evidence and the worker's explicitly labeled author
   acceptance, updates the candidate's canonical checkboxes, and validates the
   combined ledger. Author acceptance is not independent review.
8. Commits the candidate with the explicit `Workflow Controller` identity. Existing
   Git hooks/signing policy remain in force; a hook changing the verified source
   causes a stop requiring inspection and reverification.

Inspect the returned run ID and candidate before applying it:

```sh
python3 .aws-workflow/scripts/workflow.py --root . run-status RUN_ID
python3 .aws-workflow/scripts/workflow.py --root . run-apply RUN_ID
```

Replace `RUN_ID` with the actual returned ID. Application requires a ready
candidate, current task evidence, an unchanged clean original `HEAD`, and no
collision with an original ignored file newly tracked by the candidate. It uses a
fast-forward merge; it never force-updates, rebases, or discards user work. A
changed candidate must be reverified. A changed original requires a deliberate
integration decision.

Apply intent is recorded before the merge. The controller then checks the actual
original `HEAD` and worktree. A post-merge hook that changes files is preserved and
reported as `applied-needs-review`; it is not silently rolled back or reported as
the exact verified result. An interruption or error after apply intent is
`application-unknown` (or an interrupted `applying` record). Inspect the original
Git state and effects before continuing; never replay application automatically.

Task completion in a candidate does not finish every project review or authorize
deployment. Follow the [review procedure](../../workflows/review.md), required CI
checks and actual release controls, then advance the workflow phase when its real
conditions are satisfied.

## Failure, interruption, and continuation

`run-status` distinguishes a recorded result from an interrupted controller. If a
record says running/applying but its original process is gone, the effective status is
`unknown`. Inspect its worktrees, check output and any effects before deciding the
next action. The same run ID cannot be reused to reset attempts or replay work.

For an inspected failed or interrupted run, record the disposition explicitly:

```sh
python3 .aws-workflow/scripts/workflow.py --root . run-abandon RUN_ID --reason "Actual inspection and reconciliation outcome"
```

Abandonment retains the worktrees, receipts, counters and history. It does not
undo external effects, delete files or claim recovery. A live controller cannot
be abandoned through this command. Failed candidates cannot be applied through
`run-apply`. Preserve useful changes through a reviewed manual integration or a
new scoped run after the cause is understood. A new run is a new explicitly
authorized operation, never an automatic retry of an uncertain one.

Runtime files live under `.workflow-state/runs/<run-id>/`; they are separate from
versioned sanitized acceptance receipts. Worktree cleanup is deliberately manual
after inspection; do not remove active worktrees or unknown operation records.

## Verification scope

`tests/test_runner.py` exercises real temporary Git repositories/worktrees and
local subprocess checks with an injected fake author. It covers parallel and
dependent work, overlapping scopes, user-file preservation, invalid policies,
worker failures, check/integration failures, time bounds, source mutation,
evidence freshness, candidate application, and interrupted-run disposition. The
native adapter's argv and structured result contract are tested without invoking
a model. Actual native client operation, model quality and AWS outcomes remain
distinct observations in the [evaluation protocol](../../evaluations/README.md).

## Calling-shell startup prerequisites

Run `workflow.py --root . native-check` from the same ordinary authorized
terminal that will launch the native runner. The default native backend checks
observable client-state directory access and executable presence before reserving
a run. Known read-only mounts, missing state or unknown access stop execution.
The result is metadata-only, not a successful client startup or a permission
check for configured overrides. For Codespaces and the frozen pilot, see
[Codespaces readiness](../../guide/07-codespaces.md). Current-session task
implementation does not require optional native worker execution.
