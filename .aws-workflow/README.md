# AWS project workflow: AWS project

This is a reusable guidance and tooling package. Application context paths are
recorded in [manifest.json](manifest.json); they preserve existing project records
or point to fresh records created for this application. No source-template brief,
active specification, backlog, evidence receipt, or `.codex` settings were copied.

Start with [the application brief](../project/brief.md)
and [the current handoff](../delivery/current-handoff.md), then use
[Consult](workflows/consult.md). In brownfield work, assess existing authority
before adopting structured specification metadata. The manifest maps logical
context paths in reusable prose to the application's actual files.

Before selecting work, read the mapped brief/handoff and start the consultation
naturally. Open the application in Codex and type **`start`**.
Describe the outcome if you already know it. Codex runs the setup check and
continues saved consultation or work when present. To check setup manually, run:

```sh
python3 .aws-workflow/scripts/workflow.py --root . doctor
```

After consultation chooses a bounded work item and route, create it
from the application root, then load its context. For example:

```sh
python3 .aws-workflow/scripts/workflow.py --root . new 0100-first-capability --title "First useful capability" --mode greenfield --route requirements-first --activate
python3 .aws-workflow/scripts/workflow.py --root . context --compact
```

Select the route and title for the actual agreed scope; the command above is an
example, not an automatically selected backlog. For an already selected work item,
run only `context`. It requires a selected work record; adoption itself selects
none. Inspect `--help` for supported options. Adoption does not enable hooks, install
plugins, start models, authenticate, access AWS, or authorize deployment. Native
execution state is excluded from Git through the additive managed `.gitignore`
block. The runner verifies the effective ignore rule before native execution.

Packaged reference material may describe maintenance of the source template.
Those sections do not create application obligations. Excluded source-template
links become labeled prose; the installation preview lists each omitted reference.
For updates, preview the candidate source with `--upgrade`. Inspect the plan
before applying it. Local changes to managed files require a reviewed merge.
