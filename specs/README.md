# Work specifications

Use one stable directory per useful change: `specs/<work-id>/`. A feature normally has `requirements.md`, `design.md`, and `tasks.md`. A defect uses `bugfix.md` for current, expected, and preserved behavior, with design/tasks as warranted. Small direct changes can use proportionate records rather than a full package.

The task file owns completion and its verification matrix. Evidence belongs under the matching work ID in `evidence/` or links to an existing durable CI artifact. Keep stable requirement/task/check IDs through revisions and record deferred work explicitly.

The [foundation specification](0001-workflow-foundation/requirements.md) is for improving this bootstrap. Adopting applications create their own work specification and project brief. The [templates](../templates/README.md) and [worked example](../examples/booking-retries/README.md) show the shape.

