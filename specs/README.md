# Work specifications

A scoped work item has one canonical contract, design and task list, normally under `specs/<work-id>/`. A bugfix contract uses `bugfix.md`; a small direct edit can use proportionate records. The local CLI creates a consultation draft and indexes it in `work.json`; it does not invent completed requirements or create a second task checklist.

Stable requirement, task and check IDs connect the work to verification. Evidence records actual observations and declared input identities. A review records a real decision and its scope. See [the tooling contract](../docs/reference/workflow-tooling.md) before using machine validation.

New CLI work uses EARS behavioral statements and requires recorded current analysis before contract acceptance plus mapped correctness properties before task acceptance. Operation histories identify their reviewed sources; they do not fabricate semantic judgments or test execution. Deliberate reconciliation previews stale conclusions and reopens only affected state. Established work is not silently migrated into new gates.

For a new feature or defect, link the applicable project foundations and describe what changes for this work. Brownfield adoption preserves the existing tracker or task authority. Use the [brownfield guide](../guide/05-brownfield-adoption.md) to settle its relationship to the local task ledger.
