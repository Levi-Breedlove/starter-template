# Behavioral evaluation protocol

Measure useful completed work against its actual requirements. Local fixtures establish tool behavior; real model consultation, native-client integration and AWS outcomes need distinct observations. The [current handoff](../delivery/current-handoff.md) identifies implemented work and its receipts. The [consultation examples](../examples/consultation/README.md) illustrate expected interaction; they are not executed model trials.

## Quality gates come first

A scenario passes only when its required outcomes and applicable checks are established, consequential unknowns are resolved or explicitly bounded, and the result preserves accepted constraints. A passing run has zero fabricated completion/review claims and zero unauthorized operations. Brownfield checks must preserve protected behavior, user edits, infrastructure ownership and delivery controls.

Compare efficiency only among runs meeting those gates. Lower time, usage or document volume cannot compensate for a correctness or authority failure. This follows OpenAI's guidance to use task-specific evaluations and calibrate automated metrics with human judgment. [Evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices)

## Use two frozen pilots

The [native pilot plan](native-pilot-plan.md) supplies concrete disposable inputs, prompts, invocation limits, checkpoints and acceptance rubrics. It is a prepared proposal, not an observation. Its current execution status is recorded in the developer-workflow task ledger; only actual approved results can close that boundary.

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

The compact-context implementation provides `context --compact`, a startup packet of at most 6,000 serialized characters and a prompt-refresh packet of at most 1,200. Its work receipt records fixture evidence for those bounds, meaningful selection, visible omissions and freshness handling. A matching report fingerprint can support context reuse; it does not establish unchanged external state or authenticate source claims. See [efficient operation](../docs/reference/efficient-operation.md).

Run `python3 evaluations/context_payloads.py` for the frozen renderer fixtures. To compare a prior revision, supply `--baseline-dir` with inspected, trusted prior `codex_hooks.py` and `workflow.py` scripts; the utility imports their definitions and records their hashes. It performs no fetching or model invocation. Use the same fixture hashes when comparing results, and report startup increases as well as refresh reductions.

Actual hook trust/loading, public official-toolkit availability and authorized cloud delivery retain separate checks. An AWS trial must observe the chosen candidate, target, service behavior and applicable recovery within its actual scope. This protocol does not authorize paid/model runs, native-client activation, account access, deployment or background evaluation; those actions use their own explicit task authority and limits.

The foreground task controller already has real local Git/process fixture coverage with fake authors, including preservation and uncertain outcomes. A real selected-client run must separately show that the native backend can deliver and apply a valid candidate under the fixed limits. A successful native pilot still does not establish loaded hooks, working AWS accounts or universal comparative superiority.
