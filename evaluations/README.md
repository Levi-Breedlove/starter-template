# Behavioral evaluation protocol

Measure useful completed work against its actual requirements. Local fixtures establish tool behavior; real model consultation, native-client integration and AWS outcomes need distinct observations. The [current handoff](../delivery/current-handoff.md) identifies implemented work and its receipts. The [consultation examples](../examples/consultation/README.md) illustrate expected interaction; they are not executed model trials.

## Quality gates come first

A scenario passes only when its required outcomes and applicable checks are established, consequential unknowns are resolved or explicitly bounded, and the result preserves accepted constraints. A passing run has zero fabricated completion/review claims and zero unauthorized operations. Brownfield checks must preserve protected behavior, user edits, infrastructure ownership and delivery controls.

Compare efficiency only among runs meeting those gates. Lower time, usage or document volume cannot compensate for a correctness or authority failure. This follows OpenAI's guidance to use task-specific evaluations and calibrate automated metrics with human judgment. [Evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices)

## Select representative scenarios

For a workflow evaluation, pin the fixture, input decisions, acceptance criteria, allowed operations and available time in advance. Choose scenarios relevant to the project. Preserve all attempts.

| Pilot | Fixed inputs and useful variants | What to assess |
| --- | --- | --- |
| Greenfield booking workflow | Freeze the user goal, business rules, tool access, limits and acceptance rubric. Test both a rough idea and a brief containing the same established answers. | Consequential questions, supported recommendations, saved decisions, connected requirements/design/tasks and meaningful verification. Compare route-appropriate review without invented permission pauses. |
| Brownfield correction | Freeze an existing repository snapshot, protected interface, accepted stack, dirty user file, known defect and expected result. Include a changed requirement and an interrupted/resumed session. | Baseline preservation, reproduction/fix/regression evidence, stale-claim handling, correct continuation and no repeated discovery of settled facts. |

Run each configuration against the same input variant and rubric. Record client/model/settings, source revision, available tools, actual limits and observation time. Use fresh reviewer context and repeat scenarios enough to expose variation; do not generalize one successful trial into a universal ranking. A planning-only variant must finish as a plan, not claim implementation.

## Record comparable measurements

| Measure | Operational definition |
| --- | --- |
| Unnecessary questions | Questions already answered by available, unchanged authoritative context, or routine engineering research unnecessarily delegated to the user. Record justified reconfirmation separately. |
| Corrective interventions | User corrections needed for an unsupported assumption, incorrect artifact or process detour. |
| Context characters | Actual emitted packet length and omitted-item counts. Character reduction alone does not establish token savings, cost savings or better model behavior. |
| Repeated reads | Identical file-content reads with no new purpose, where tool traces permit measurement. Changed content and necessary recovery reads are separate. |
| Repeated checks | Same check and relevant input identities rerun without changed inputs, reproduction need or a required final gate. |
| Time | Elapsed time to the same accepted outcome; record pauses and scope differences. |
| Usage and cost | Observable totals across all agents, with model and settings. Unknown values remain unknown; do not substitute character counts or treat missing telemetry as zero. |

Report each measure alongside quality findings. Avoid a combined score that hides a failed requirement behind a cheaper run. Add observed failures to the existing fixtures and rubric rather than creating a second evaluation process.

## Separate implementation proof from behavioral proof

The compact-context interface publishes a bounded startup summary and prompt refresh. Record the observed size, work selection, deferred details and freshness when evaluating it. Compare runs on the same source, client and fixture. [Efficient operation](../docs/reference/efficient-operation.md)

Actual hook trust/loading, public official-toolkit availability and authorized cloud delivery retain separate checks. An AWS trial must observe the chosen candidate, target, service behavior and applicable recovery within its actual scope. This protocol does not authorize paid/model runs, native-client activation, account access, deployment or background evaluation; those actions use their own explicit task authority and limits.

For a native controller observation, identify the applied base, actual client, candidate diff and test receipts. Verify the original application stayed intact through review and record the actual apply result. A later project release needs its own evidence against its selected delivery environment.
