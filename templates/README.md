# Reusable project records

Copy only the records needed for the work. Replace angle-bracket placeholders, correct relative links after copying, and retain existing project identifiers. A template is an unapproved starting point; it does not grant execution or deployment authority.

These are independently authored repository templates for Codex. They implement the documented Kiro concepts below as plain project records; they are not copied user skills, official Kiro templates, or executable workflow recipes.

| Template | Use | Suggested destination |
| --- | --- | --- |
| [Project brief](project-brief.md) | Establish goals, constraints, authorities, and unresolved choices. | `project/brief.md` |
| [Brownfield assessment](brownfield-assessment.md) | Map an existing system and the behaviors a change must preserve. | `project/brownfield-assessment.md` |
| [Requirements](requirements.md) | Describe a feature's observable behavior and acceptance. | `specs/<work-id>/requirements.md` |
| [Design](design.md) | Explain the selected implementation and verification approach. | `specs/<work-id>/design.md` |
| [Tasks](tasks.md) | Own implementation checkboxes, dependencies, and verification references. | `specs/<work-id>/tasks.md` |
| [Bugfix analysis](bugfix.md) | Define a defect, its correction, and behavior to preserve. | `specs/<work-id>/bugfix.md`, instead of `requirements.md` |
| [Decision](decision.md) | Record a consequential choice and the evidence behind it. | `docs/decisions/<decision-id>.md` |
| [Review](review.md) | Evaluate a fixed revision against the accepted contract. | `evidence/<work-id>/<review-id>.md` |
| [Release](release.md) | Describe a specific release candidate and its actual result. | `delivery/releases/<release-id>.md` |
| [Handoff](handoff.md) | Maintain one concise current continuation record. | `delivery/current-handoff.md` |
| [Environment capabilities](environment-capabilities.md) | Distinguish documented capability from observed availability. | `delivery/environment-capabilities.md` |

## Choose a small record set

- **Greenfield:** begin with the project brief and explicitly select the initial architecture and delivery approach.
- **Brownfield:** begin with the existing records and the brownfield assessment. Add or link missing workflow records in place; do not move existing code just to match this skeleton.
- **Requirements-First feature:** requirements, design, tasks, in that order.
- **Design-First feature:** begin with an existing or proposed design, derive and validate the requirements, then create tasks.
- **Quick Spec:** resolve material questions up front, then draft requirements, design, and tasks together. Do not invent a new approval interruption between each generated file.
- **Defect:** bugfix analysis, design, tasks.
- **Plan or small edit:** a conversational plan or existing work record can be sufficient. Kiro Plan mode itself does not create formal spec files; persist a record here when the project needs durable continuation.
- **Release:** link existing task and review evidence from a release record; do not copy the complete specification again.

Use requirement IDs such as `REQ-001`, design references such as `DES-001`, task IDs such as `T-001`, and verification IDs such as `CHK-001` within a work item. Refer to the work ID when a reference crosses work items.

`tasks.md` owns task completion. Its verification matrix connects requirements, tasks, and result references. Keep detailed sanitized output in `evidence/<work-id>/` or the existing CI artifact system. Linear or another tracker can project status and link to these records under the project's declared authority; it should not become a second independently edited specification.

The [booking retry example](../examples/booking-retries/README.md) shows how these records fit together. It is a fictional planning example, with no implementation or passing test claims.

## Official Kiro basis

- [Feature Specs](https://kiro.dev/docs/specs/feature-specs/) describes Requirements-First, Design-First, and structured behavioral requirements.
- [Quick Spec](https://kiro.dev/docs/specs/quick-spec/) describes generation of the three artifacts after initial clarification.
- [Plan mode](https://kiro.dev/docs/specs/plan/) distinguishes a conversational plan from persisted Specs.
- [Bugfix Specs](https://kiro.dev/docs/specs/bugfix-specs/) describes current, expected, and unchanged behavior.
- [Correctness](https://kiro.dev/docs/specs/correctness/) connects requirements, properties, tasks, and tests. Its integrated Kiro feature is surface-dependent and does not establish that this scaffold executes property tests.
- [Spec best practices](https://kiro.dev/docs/specs/best-practices/) describes importing existing designs and reconciling requirements, design, and tasks as work changes.

The identifiers, evidence fields, paths, and activity labels here are proposed repository conventions. Product features, actual execution results, and these conventions remain distinct.
