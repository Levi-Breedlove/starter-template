# Worked planning example: booking retries

This is a fictional, unapproved feature specification used to demonstrate the repository workflow. No application code, database, AWS environment, deployment, or passing checks are supplied or claimed. All implementation tasks remain unchecked.

The example defines a narrow API behavior: repeated identical booking requests with one idempotency key should resolve to one booking outcome. It illustrates a concurrency-sensitive requirement without selecting an AWS architecture for another project.

Read the records in order:

1. [Requirements](requirements.md) describes behavior, preservation, and unresolved choices.
2. [Design](design.md) proposes an implementation contract and failure handling.
3. [Tasks and verification](tasks.md) connects every requirement to tasks and expected checks.

## Practice exercise

Ask Codex to review the requirements for ambiguity and then inspect whether the design and verification matrix cover them. It should identify the unresolved retention duration and the need to validate transaction behavior for the selected persistence system. It should not mark tasks complete or create cloud resources.

After selecting a real project and accepting its decisions, copy only the needed records to `specs/<work-id>/`, adapt their assumptions, and create real implementation and evidence. This example's task status should remain illustrative.

## What the example demonstrates

- Explicit duplicate, conflict, concurrency, failure, and preservation behavior.
- Requirement IDs connected to design sections, tasks, and check IDs.
- Required verification and named deferred work.
- A design change that invalidates affected evidence, rather than silently preserving old completion claims.

The example is not a claim about the implementation or current state of Levi's Appointments Scheduler.
