# Work specifications

A scoped work item has one canonical contract, design and task list, normally under `specs/<work-id>/`. A bugfix contract uses `bugfix.md`; a small direct edit can use proportionate records. The local CLI creates a consultation draft and indexes it in `work.json`; it does not invent completed requirements or create a second task checklist.

Stable requirement, task and check IDs connect the work to verification. Evidence records actual observations and declared input identities. A review records a real decision and its scope. See [the tooling contract](../docs/reference/workflow-tooling.md) before using machine validation.

The [foundation](0001-workflow-foundation/requirements.md), [consultant workflow](0002-consultant-workflow/requirements.md), and [focused context](0003-efficient-context/requirements.md) are framework maintenance work. The adoption helper excludes them from application work; applications create their own brief, work and evidence. Existing trackers/layouts need an explicit authority mapping rather than a competing checklist.
