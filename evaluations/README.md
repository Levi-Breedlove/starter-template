# Evaluation plan: parity and improvement

**All behavioral scenarios here are planned and unexecuted.** The delivered checker tests validate only the checker. They are not a Kiro-versus-Codex benchmark. Implementation completion belongs in the [foundation backlog](../specs/0001-workflow-foundation/tasks.md).

## What to measure

| Measure | Definition | Proposed success condition |
| --- | --- | --- |
| Critical outcome coverage | Required critical outcomes with relevant current evidence / all critical outcomes. | Every critical outcome evidenced or explicitly unfinished; no false completion. |
| Preservation | Established behavior required to remain unchanged. | Required brownfield regression/compatibility checks pass on the integrated candidate. |
| Evidence freshness | Acceptance records tied to actual source, inputs, configuration, environment, artifact. | Mutating an input invalidates affected results; unrelated results retain their bounded scope. |
| Recovery correctness | Work after interruption compared with its actual partial state. | Completed siblings preserved, unknown outcomes reconciled, no blind duplicated effect. |
| Review quality | Findings and incomplete reviews against a seeded ground truth. | Substantive seeded defects detected; failed review never becomes a pass. |
| Event correctness | Replayed events, stale heads, and generated-output events. | No duplicate dispatch, false readiness, or recursive uncontrolled work. |
| Human intervention | Material decisions versus repeated reminders or avoidable recovery prompts. | Lower unnecessary intervention with no loss of legitimate authority. |
| Efficiency | Active elapsed time, model usage, retries, and infrastructure cost where actually available. | Report distributions and tradeoffs; no invented costs from incomplete telemetry. |

Targets are this repository's design goals. They are not statements that a particular Kiro release fails them.

## Scenario set

Use the 14 [runtime parity scenarios](../docs/research/runtime-parity.md) and the 12 AWS-focused metrics in [AWS integration research](../docs/research/aws-integration.md). Add two representative project fixtures:

1. A small greenfield capability with clear acceptance, one meaningful invariant, and a realistic failure path.
2. A brownfield change with an existing architecture, dirty user work, a protected interface, a known baseline failure, and established IaC/pipeline ownership.

The [booking retries example](../examples/booking-retries/README.md) can become one fixture after an actual application and tests are implemented. Its current documents are not executable proof.

## Test the controller without spending first

Use fake worker/tool adapters and temporary repositories for graph, state, evidence, event, and crash behavior. Simulate interruption between dispatch, effect, and persistence. Use a fake external operation with an observable receipt to prove uncertainty is reconciled before retry. These tests should fail when the relevant invariant is deliberately broken.

Then run a bounded real Codex trial on the chosen surface with documented versions, inputs, authority, limits, and outputs. Native hook trust and event support require real client evidence. A model-free fixture test cannot establish them.

AWS integration trials require separately established target/action limits and resource cleanup ownership. Public documentation/plugin checks remain account-free. Record local, native-client, and AWS observations as distinct evidence levels.

## Fair Kiro comparison

Use the same initial repository revisions, acceptance contract, allowed tools/data, task scope, and operational limits. Record the exact product surface, version, model selection, reasoning settings where visible, installed capabilities, and human interventions. Randomize run order or repeat scenarios when variability could change the conclusion. Disclose whether either system received extra contextual help.

An evaluator who did not author the candidate should judge against the same acceptance suite and seeded-defect rubric. Compare successful outcomes and preserved behavior before optimizing speed or usage. Account for failed/retried attempts and distinguish measured billing, reported usage, and unknown cost.

Publish per-scenario results and limitations. A result on one feature does not establish superiority across projects, models, surfaces, or architectures. Use a claim such as “this configuration reduced repeated context prompts on these fixtures” only after the corresponding result exists.

## Evidence record

Store a sanitized report under `evidence/<evaluation-id>/` with fixture/source identity, contract and tooling versions, environment, procedure, observations, raw-result references, exclusions, evaluator, and conclusion. Keep secrets, customer data, and raw account inventory outside the repository. Link the report from the actual implementation task it evaluates.

