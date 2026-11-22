# Verification scope

The delivered tests exercise the offline repository checker with temporary fixtures. Run:

~~~sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
~~~

The fixtures address actual failure modes: missing links, escaping targets, symlinks, Markdown examples, incomplete scans, and CLI behavior. They use Python's standard library and make no network or AWS calls.

Passing these tests establishes the checker behavior covered by those cases. It does not verify the workflow runner, native Codex hooks, the fictional example application, or a deployment. Future behavioral acceptance belongs in the [evaluation catalog](../evaluations/README.md) and the [foundation backlog](../specs/0001-workflow-foundation/tasks.md).

An adopting application keeps its actual test framework and existing tests. Add characterization, regression, contract, integration, performance, or operational checks according to the accepted requirements and remaining risk.

