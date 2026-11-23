# Current handoff

**Active work:** 0004-developer-workflow.  
**State:** Implementation and combined local verification complete; exact source publication is in progress.  
**Base:** `200016c62f10fe1a7eb164584f3b7ab794450a41`.

Read the [execution plan](../specs/0004-developer-workflow/exec-plan.md), [contract](../specs/0004-developer-workflow/requirements.md) and canonical [tasks](../specs/0004-developer-workflow/tasks.md). Setup, complete adoption, structured analysis/properties, reconciliation, phase-aware context and bounded task execution are implemented. The actual aggregate run passed 183 tests; seven independent material review findings are closed. [Observed local result](../evidence/0004-developer-workflow/verification.md)

The older consultant/context records were deliberately reconciled because shared inputs changed. Fresh current local evidence has been appended; their historical receipts remain unchanged. Their publication checks will be completed only after actual source readback. No real native model invocation, client trust change, plugin installation or AWS account operation occurred in this slice.

The remaining behavioral acceptance is T-008. Its [prepared pilot](../evaluations/native-pilot-plan.md) fixes two disposable scenarios, seven direct native calls and one controller worker, sequentially, with a 900-second per-invocation limit and no retries. This is not a hard credit cap. It is NOT RUN and needs the user's actual approval under the standing instruction for additional credit-consuming model execution. After approval, use that exact scope, record observations and judge the rubric before closing T-008. Do not treat fixture results or this handoff as native approval.
