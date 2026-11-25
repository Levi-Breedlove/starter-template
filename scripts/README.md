# Local tools

Python 3.10 or newer; standard library only. Setup, context, analysis requests and execution previews do not call a model or access AWS. Explicit `workflow.py run --execute` invokes the configured native model backend and trusted verification commands; `run-apply` integrates a verified candidate. These are deliberate effects with their own project authority. No tool installs packages or enables a background service.

| Entry point | Purpose | Reference |
| --- | --- | --- |
| `bootstrap.py` | Preview/apply a reusable layer to a separate application | [Adoption](../docs/reference/bootstrap.md) |
| `workflow.py` | Setup, specifications, state/evidence, reconciliation and explicit bounded execution | [CLI](../docs/reference/workflow-tooling.md) |
| `codex_hooks.py` | Read-only JSON lifecycle adapter | [Native hooks](../docs/reference/native-hooks.md) |
| `check_repository.py` | Required paths for the selected layout and explicit Markdown file destinations | Scope below |

## Repository checker scope

From an application root, run:

```sh
python3 .aws-workflow/scripts/check_repository.py
```

The checker inspects required paths for the detected application or maintenance layout and checks local Markdown file destinations. Use `--root` to inspect another repository. It reports missing files, paths escaping the selected root and incomplete scans. Remote sites, anchors, HTML links, document semantics, workflow evidence and application behavior each require their own appropriate checks. Run the project's actual tests for the changed behavior.
