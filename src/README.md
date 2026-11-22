# Application source

The bootstrap does not select an application language or framework. A greenfield project places its workload code here or in the selected framework's conventional layout. A brownfield project keeps its existing layout.

The optional future workflow controller belongs in a distinct `workflow_engine/` package if implemented, so framework machinery is not confused with application code. No controller or deployed workload exists in this skeleton.

Record the actual source map in the project brief/design when adopting the bootstrap. See [the repository map](../docs/repository-map.md).

