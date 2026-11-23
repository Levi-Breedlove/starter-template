# Work specifications

A scoped work item has one canonical contract, design and task list, normally under `specs/<work-id>/`. A bugfix contract uses `bugfix.md`; a small direct edit can use proportionate records. The local CLI creates a consultation draft and indexes it in `work.json`; it does not invent completed requirements or create a second task checklist.

Stable requirement, task and check IDs connect the work to verification. Evidence records actual observations and declared input identities. A review records a real decision and its scope. See [the tooling contract](../docs/reference/workflow-tooling.md) before using machine validation.

New CLI work uses EARS behavioral statements and requires recorded current analysis before contract acceptance plus mapped correctness properties before task acceptance. Operation histories identify their reviewed sources; they do not fabricate semantic judgments or test execution. Deliberate reconciliation previews stale conclusions and reopens only affected state. Established work is not silently migrated into new gates.

The [foundation](0001-workflow-foundation/requirements.md), [consultant workflow](0002-consultant-workflow/requirements.md), [focused context](0003-efficient-context/requirements.md), and [developer workflow](0004-developer-workflow/requirements.md) are framework maintenance work. The latest [execution plan](0004-developer-workflow/exec-plan.md) explains the delivery sequence. Adoption excludes this maintenance backlog; applications create their own brief, work and evidence. Existing trackers/layouts need explicit authority mapping.
