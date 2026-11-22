# Feature

## Trigger

Use this procedure for new or changed functionality whose scope benefits from an explicit specification and task record. Use [Bugfix](bugfix.md) for a defect and proportionate direct work for a trivial, understood change.

## Inputs

- The scoped objective and selected route from [Consult](consult.md), or an equivalent existing decision.
- For an existing system, the [brownfield adoption report](brownfield.md), including behavior, data, and infrastructure ownership that must be preserved.
- The brief, accepted architecture, current code, relevant contracts, and current handoff.
- `specs/<work-id>/` and linked cost, security, decision, and operating records.
- Authorized implementation scope and the verification environments actually available.

## Stages

### 1. Select and record the route

| Route | Procedure |
| --- | --- |
| Requirements-First | Define observable behavior and acceptance criteria; resolve material ambiguities; design an implementation that satisfies them; generate tasks. |
| Design-First | Inspect and preserve the accepted architecture; clarify the proposed design change; derive requirements within its constraints; check that user needs were not lost; generate tasks. |
| Quick Spec | Ask material clarifying questions up front; draft requirements, design, and tasks together; review the resulting scope before implementation. Do not add per-file approval pauses. |
| Plan-led | Explore the code and formulate a small implementation plan. On an authorized implementation handoff, save the accepted plan in the work's task record and link its requirement/design context. Promote it to a full specification if uncertainty or impact warrants it. |

The chosen route describes this repository's process. It does not activate a native Codex mode or cause Codex to interpret Kiro metadata. Kiro's own Plan mode stores a conversational plan rather than the formal spec files.

### 2. Make the behavior precise

Give material requirements stable identifiers. State the triggering condition, expected result, failure behavior, and applicable measurable limits. Include security and operational outcomes that affect acceptance. Review interactions between requirements, including concurrency, retry, and conflicting constraints. Record the resolution of material findings.

### 3. Establish design and verification

Describe component responsibilities, interfaces, data, request/event paths, error handling, and testing. Link existing decisions instead of duplicating them. For brownfield work, identify the smallest changed surface and compatibility or migration obligations; do not reorganize the repository by default. Consult official AWS guidance on demand where the design needs it.

Identify important invariants and select appropriate checks: examples, property-based tests, integration tests, infrastructure validation, or operational checks. Property-based testing is a technique, not a universal requirement. **The checks needed to establish accepted behavior remain required.** Do not equate a local emulator result with a verified AWS identity, network, availability, or deployment result.

### 4. Build a task graph

In `tasks.md`, record each task's scope, linked requirements, dependencies, acceptance checks, and completion evidence. Make optional scope explicit. Assign one integration owner. Run independent work concurrently only when its files and assumptions can be coordinated safely.

### 5. Implement and verify

Work in small reviewable changes. Read the relevant specification before each task. Run checks that address the actual remaining risk and record their result against the candidate revision. Mark a task complete only when its stated completion conditions are met; preserve blocked or unverified checks visibly.

If implementation reveals a material specification change, use [Reconcile](reconcile.md) before relying on old acceptance evidence. Keep useful prior work; do not silently change requirements to fit the implementation.

### 6. Review and hand off

Use [Review](review.md) on the concrete candidate. Resolve blocking findings and rerun affected checks. Update operating documentation when behavior changes. Hand off to [Release](release.md) only if deployment is in scope; otherwise report the implementation and verification status accurately.

## Outputs

- Updated `requirements.md`, `design.md`, and `tasks.md` as appropriate to the recorded route.
- Code, infrastructure, and documentation changes within the agreed scope.
- Lightweight evidence under `evidence/<work-id>/`, with CI links where applicable.
- A current handoff naming the revision, remaining work, and next action.

## Completion evidence

Every required acceptance condition has a result or an explicit unresolved limitation. Task status agrees with inspected code and evidence. Review covers the current candidate. A completed feature does not by itself claim a successful AWS deployment.

## Continue, pause, and resume

Continue authorized implementation and routine verification without repeated approval requests. Pause for unresolved material contradictions, a changed authorization boundary, or missing access needed for a required check. On resume, inspect current code and task state, assess evidence freshness, and continue the next unblocked task.

## References

[Requirements-First](https://kiro.dev/docs/specs/feature-specs/requirements-first/), [Design-First](https://kiro.dev/docs/specs/feature-specs/tech-design-first/), [Quick Spec](https://kiro.dev/docs/specs/quick-spec/), [Plan mode](https://kiro.dev/docs/specs/plan/), [Analyze Requirements](https://kiro.dev/docs/specs/analyze-requirements/), and [Correctness](https://kiro.dev/docs/specs/correctness/).
