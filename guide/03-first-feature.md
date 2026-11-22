# Deliver the first feature

Use the [feature procedure](../workflows/feature.md) as the operating contract. This guide explains how its artifacts fit together.

## Select the route

| Starting point | Route | First artifact |
| --- | --- | --- |
| User outcome is clear; implementation needs design | Requirements-First | Observable requirements and acceptance criteria. |
| Existing architecture or a technical change constrains the solution | Design-First | The proposed design within established constraints, followed by checked requirements. |
| A bounded feature is understood after a few material questions | Quick Spec | Requirements, design, and tasks drafted together. |
| A defect has current, expected, and preserved behavior | Bugfix | Reproduction and behavior-preservation analysis. |
| A small change needs limited exploration | Plan-led or direct work | A proportionate plan and verification record. |

These routes are grounded in [Kiro's documented specification variants](../docs/reference/kiro-capabilities.md). They are instructions for Codex, not activation of Kiro UI controls or hidden Codex modes.

## Build the specification

Create a stable work directory under `specs/`. Start from the [requirements](../templates/requirements.md), [design](../templates/design.md), and [tasks](../templates/tasks.md) templates, or the [bugfix template](../templates/bugfix.md). Correct copied relative links for their destination.

Requirements describe externally observable behavior, including relevant failure and concurrency conditions. Review ambiguity, contradictory limits, unstated preconditions, and dependencies before investing in implementation. EARS-style wording can make conditions precise; the wording alone does not guarantee a complete requirement.

The design explains components, contracts, data, failure handling, operational constraints, and verification. Link decisions instead of maintaining duplicate architectural explanations. For a brownfield change, state which interfaces, data, resource ownership, and established behavior remain protected.

Tasks form a dependency graph. Each task identifies the requirement it serves, the files or interfaces it owns, its prerequisite work, and the evidence needed for completion. Keep optional or deferred scope explicit. A failed required check cannot be relabeled optional to finish the task.

## Execute and review

Read the relevant specification before each task. Implement small, reviewable outcomes. Parallelize independent investigations or isolated file scopes when it provides value; integrate results before testing the combined candidate. Shared context and shared filesystem access do not by themselves establish independent review.

Record actual checks in the task verification matrix and [evidence area](../evidence/README.md). A result identifies the candidate, relevant configuration, environment, method, and observation. If implementation changes a requirement or invalidates a design assumption, run [Reconcile](../workflows/reconcile.md) and update affected tasks and evidence.

Use [Review](../workflows/review.md) on the concrete candidate. Give reviewers the acceptance contract and change, not an instruction to endorse the author's conclusion. Resolve substantive findings and rerun affected checks. Final validation returns to the original accepted outcome and preservation requirements; it does not merely confirm that the task list is checked.

## Finish at the right boundary

When implementation is complete, report the achieved behavior and evidence. If deployment is outside scope, finish with a deployable candidate and an honest limitation. If deployment is authorized, continue through [maintenance and release](04-maintain-and-release.md), the release contract, and the project's real pipeline.

The [booking retries example](../examples/booking-retries/README.md) demonstrates traceability and preservation without claiming to be a running application.

