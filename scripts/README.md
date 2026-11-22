# Local tools

Python 3.10 or newer; standard library only. Run the bootstrap's tests from its root. Tools do not install packages, call a model, connect to AWS or launch deployment commands.

| Entry point | Purpose | Reference |
| --- | --- | --- |
| `bootstrap.py` | Preview/apply a reusable layer to a separate application | [Adoption](../docs/reference/bootstrap.md) |
| `workflow.py` | Work initialization, context, status, validation, reviews, transitions and evidence | [CLI](../docs/reference/workflow-tooling.md) |
| `codex_hooks.py` | Read-only JSON lifecycle adapter | [Native hooks](../docs/reference/native-hooks.md) |
| `check_repository.py` | Bootstrap core paths and explicit Markdown file destinations | Scope below |

## Repository checker scope

```bash
python3 scripts/check_repository.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The checker resolves its source root by default; `--root` selects another tree. It checks required bootstrap paths and explicit local Markdown links, including reference definitions. It skips remote URLs and recognizable template placeholders. It reports missing/escaping targets and incomplete scans rather than passing a partial inspection.

It is not a complete Markdown parser: heading anchors, undefined reference labels, HTML links and document semantics are outside scope. Workflow consistency belongs to the dedicated engine. The bootstrap required-path list is for this source repository; it is not an application adoption requirement.
