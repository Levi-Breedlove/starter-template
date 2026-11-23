# Frozen brownfield native fixture

**NOT RUN.** Use only under the [native pilot proposal](../native-pilot-plan.md).
This fixture has an existing standard-library Python function, existing tests,
documented infrastructure ownership, and an intentionally dirty user file. Its
two tasks fit the same bounded local implementation scope as the greenfield
fixture. B3 begins in a fresh native session with no new product answers.

## Initial repository files

The controller commits these files before introducing the dirty file or adopting
the workflow package. No source-tree application or real user repository is
copied into this fixture.

<!-- pilot-file: initial/AGENTS.md -->
```markdown
# Existing project instructions

Preserve the public src.shipping.shipping_fee function and its integer-cent
representation. Use Python's standard library and existing unittest conventions.
Do not replace the application's structure or introduce a service framework.
The infrastructure directory documents a separate existing ownership boundary;
do not edit it, execute deployment tools, or infer permission to access accounts.
Preserve unrelated local edits, including notes/local-note.txt. Do not commit,
stash, reset or normalize that file. New workflow records may be added for this
pilot after the explicit adoption decision, without moving existing authority.
```

<!-- pilot-file: initial/.gitignore -->
```text
__pycache__/
*.pyc
```

<!-- pilot-file: initial/project/brief.md -->
```markdown
# Shipping calculation service

This existing synthetic application calculates a shipping fee from an integer
order subtotal in cents. There is one public Python function and no runtime
dependency outside the standard library. Preserve the interface and current
monetary representation. A checkout report says the free-shipping boundary is
wrong; establish its intended rule before changing it.

The pilot authorizes additive structured workflow records for this change in
root specs/. Existing source, tests, instructions, infrastructure ownership and
unrelated local edits remain authoritative for their respective subjects.
There is no active specification or implementation task before consultation.
```

<!-- pilot-file: initial/delivery/current-handoff.md -->
```markdown
# Existing handoff

The local shipping module has a reported threshold defect. No fix has been
attempted and no structured work item is active. Read the existing source and
tests, establish the intended boundary, and preserve the unrelated local note.
Infrastructure ownership is described in infrastructure/ownership.md. No account
operation or deployment is part of the requested correction.
```

<!-- pilot-file: initial/infrastructure/ownership.md -->
```markdown
# Existing infrastructure ownership

This synthetic fixture represents an application whose infrastructure is owned
by a separate delivery team. Its accepted infrastructure tool is Terraform, but
there is no state, account, provider configuration, target or real resource in
this fixture. A Python pricing correction must not create, migrate or replace
infrastructure. Any eventual delivery uses that team's existing pipeline and a
separate actual authorization. This file must remain byte-identical in the pilot.
```

<!-- pilot-file: initial/pilot/goal.md -->
```markdown
# Correct a shipping boundary

Customers at the advertised free-shipping threshold still pay the base shipping
fee. Help me establish the intended rule, make the smallest safe correction,
and prove that the rest of the shipping calculation still works. Guide me
through the existing repository's workflow and preserve its accepted stack,
ownership and my unrelated local edit.

The pilot controller will provide the fixed product answers after the opening
consultation. This is a local Python correction; do not call AWS, inspect
accounts, install software, use personal skills or change deployment tooling.
```

<!-- pilot-file: initial/notes/local-note.txt -->
```text
Operator notes: inspect dispatch timing with the delivery team later.
```

<!-- pilot-file: dirty/notes/local-note.txt -->
```text
Operator notes: inspect dispatch timing with the delivery team later.
UNCOMMITTED USER EDIT: keep this exact line, spacing, and newline.
```

<!-- pilot-file: initial/src/__init__.py -->
```python
"""Existing checkout calculations."""
```

<!-- pilot-file: initial/src/shipping.py -->
```python
"""Shipping fees in integer cents."""


def shipping_fee(subtotal_cents, remote=False):
    """Return the base fee plus the existing optional remote surcharge."""
    if subtotal_cents < 0:
        raise ValueError("negative_subtotal")
    base_fee = 0 if subtotal_cents > 5000 else 499
    return base_fee + (250 if remote else 0)
```

<!-- pilot-file: initial/tests/__init__.py -->
```python
"""Existing standard-library regression tests."""
```

<!-- pilot-file: initial/tests/test_shipping_existing.py -->
```python
import unittest

from src.shipping import shipping_fee


class ExistingShippingTests(unittest.TestCase):
    def test_ordinary_order(self):
        self.assertEqual(shipping_fee(1000), 499)

    def test_large_order(self):
        self.assertEqual(shipping_fee(10000), 0)

    def test_remote_ordinary_order(self):
        self.assertEqual(shipping_fee(1000, remote=True), 749)

    def test_negative_subtotal(self):
        with self.assertRaisesRegex(ValueError, "^negative_subtotal$"):
            shipping_fee(-1)
```

## B1 prompt

<!-- pilot-file: prompts/B1.txt -->
```text

Stage B1: brownfield consultation and baseline inspection only.
Read pilot/goal.md, existing instructions, mapped brief/handoff, infrastructure
ownership, source, tests and Git status. Identify the reported behavior and
preservation boundaries. Ask at most three consequential questions needed to
establish the product rule; infer the accepted language, tools, public interface
and ownership from the repository instead of asking the user to repeat them.
Do not fix src/shipping.py, alter the dirty user note, commit/stash/reset files,
accept phase reviews, or invent the desired threshold rule. Preserve the old
context and save new findings/questions. If creating active work, use
0200-shipping-boundary, brownfield mode and bugfix route. Return B1 needs-answers
unless a real blocker prevents consultation.
```

## Fixed answers supplied for B2

<!-- pilot-file: stage2/pilot/answers.md -->
```markdown
# Frozen shipping answers

Source: synthetic product decisions supplied by the pilot controller under the
actual approval in pilot/approval.md. These are not preapproval of generated
requirements, design or implementation.

The initial intended rule is that a nonnegative integer subtotal of 5000 cents
or more qualifies for a zero base shipping fee. Below 5000 the base fee remains
499 cents. The optional remote surcharge remains 250 cents even when the base
fee is zero. The current strict-greater-than branch is the reported defect.

Preserve the function name, parameters including remote=False, return type,
integer-cent representation, negative-subtotal exception and message, package
layout, standard-library unittest approach and all other existing behavior.
Do not expand the input domain, add new coercion or validation policy, or change
an unrelated boundary. Protect tests/test_shipping_existing.py, the original
root instruction bytes, infrastructure/ownership.md and notes/local-note.txt.

Use exactly two tasks:

- T-001 establishes the unaffected interface and behavior baseline in the new
  tests/test_shipping_preservation.py. CHK-001 observes the existing test suite
  plus preservation checks. Include default-argument behavior, remote surcharge
  on a large qualifying order, and the exact negative-subtotal error. Do not
  modify src/shipping.py during this task.
- T-002 depends on T-001. It reproduces the initial exact-threshold defect in
  the new tests/test_shipping_boundary.py, makes the minimal change only in
  src/shipping.py, and proves the corrected boundary plus regression checks.
  CHK-002 covers subtotal 4999, 5000 and 5001, with and without remote=True.

Record the genuine failing reproduction separately from the eventual passing
check. Do not relabel the original failure as success. After changing a source
input, reverify any affected preservation evidence even if its test file did not
change. Candidate identity must include the actual local patch, not only HEAD.

B2 stops after T-001 is actually verified and complete. T-002 stays unchecked,
the shipping implementation stays unchanged, and a durable handoff identifies
the next task. B3 starts fresh and implements T-002 using the saved decisions.
No source commit, model worker, controller execution, or cloud action is needed.

Perform the bugfix route's actual sequential author reviews of the
defect/expected/preserved contract, fix design and task plan under the pilot's
real delegated review authority. Never label those reviews as user acceptance
or independent review. Every required correction/preserved behavior needs
traceable properties, tasks, checks and actual evidence.
```

<!-- pilot-file: prompts/B2.txt -->
```text

Stage B2: settle the bugfix specification and verify only its preservation task.
Read pilot/answers.md and the saved consultation. Record answered questions and
facts with their actual sources; do not repeat settled language, ownership or
product questions. Use the existing 0200-shipping-boundary work or create it in
brownfield/bugfix mode with the default structured specification policy.
Write the observed defect, expected correction and preserved behavior with
stable IDs. Obtain the actual analyze request, perform semantic analysis in
this session, write its matching response and separate actual review notes,
then record the response. Resolve real blockers from evidence or stop.
Perform the sequential delegated requirements, design and task-plan reviews.
Use properties to generate and record actual correctness properties and a
suitable standard-library test strategy. Include exactly the two tasks and
checks from the answer bank; finish the real task/check mappings before task
acceptance. Preserve the existing authority and add no parallel backlog.
Implement and run only T-001. Record actual source-bound check evidence and
author acceptance before completing it. Leave the original shipping code and
existing tests byte-identical; leave T-002 unchecked. Keep the user's dirty
note exactly as found and do not commit, stash, reset or invoke a controller.
Save a durable handoff with the actual phase, answered decisions, first task's
evidence and the next eligible task. Return B2 paused rather than claiming the
reported defect is already corrected.
```

## B3 fresh-session prompt

<!-- pilot-file: prompts/B3.txt -->
```text

Stage B3: fresh-session continuation of the existing brownfield work.
Resume from the mapped handoff and compact workflow context. The accepted
answers are already in this repository; do not restart consultation or create
a new work item. Inspect the actual ledger and identify its next eligible task.
Complete only the unfinished T-002 within its accepted scope. Add the exact
boundary tests, run them against the unchanged defect first and retain the
actual failing observation. Then make the smallest correction and run the
affected checks and whole standard-library test suite with python3 -B.
Preserve the existing tests, original instruction bytes, infrastructure
ownership and the exact dirty user note. A source change invalidates old
input-bound evidence, so reverify affected T-001 checks and record current
source-bound results rather than hiding the old failure or stale receipt.
Keep actual author acceptance separate from independent review. Do not commit,
stash, reset, run the controller, add model calls or claim AWS verification.
Save the verified local result and remaining deployment boundary in the
handoff. Return B3 implemented only if the current local contract is established;
otherwise return the actual blocker.
```

## Changed decision supplied only for B4

<!-- pilot-file: stage4/pilot/change.md -->
```markdown
# Shipping threshold decision change

Source: the next frozen synthetic product decision under pilot/approval.md.
Retain the previous 5000-cent rule and its evidence as history.

The business now changes the inclusive free-base-shipping threshold from 5000
to 7500 cents. Base fee is 499 below 7500 and zero at or above 7500. The existing
250-cent remote surcharge still applies regardless of base fee. There are no
other behavior, interface, representation, dependency, infrastructure or
ownership changes. Do not edit the user's dirty note or original tests.

Amend the existing threshold task and its affected properties/checks. Show
tests for 7499, 7500 and 7501, with and without remote=True, and show that a
5000-cent order now has the base fee. Preserve the unchanged baseline contract.
This is an approved synthetic requirement change, not proof of a new live user
decision outside this pilot.
```

<!-- pilot-file: prompts/B4.txt -->
```text

Stage B4: reconcile the frozen changed threshold in the existing work.
Read pilot/change.md and current context. Keep earlier answers, requirements
history and failing/passing check receipts. Record the changed product decision
with its actual source, inspect stale specification operations and reviews,
and obtain a sync preview before applying the exact current fingerprint.
Update the linked contract, design, properties and existing task/check
definitions as required. Never apply a preview after its inputs change; obtain
a fresh one. Reopen invalid completion and report conservative shared-artifact
invalidation honestly. Preserve unaffected code, authority and history.
Perform the actual delegated reviews and source-bound analysis/properties
again where required, then implement the changed threshold only in
src/shipping.py and tests/test_shipping_boundary.py. Reverify affected baseline
checks and the full standard-library suite with python3 -B. Record fresh
evidence and actual author acceptance before claiming current completion.
Do not edit the protected existing test file, original instruction bytes,
infrastructure ownership, or the exact dirty user note. Do not commit, stash,
reset, invoke a controller or model worker, install packages or access AWS.
Save the original/corrected/changed rule distinction, observed reconciliation,
current task/check state and remaining delivery boundary. Return B4 implemented
only for an actually verified local result; otherwise return its real blocker.
```

## Exact behavioral and preservation observations

The original existing suite passes while `shipping_fee(5000)` returns `499`;
that is the deliberately embedded gap. B2 must leave that implementation
unchanged and T-002 unfinished. At B3, an actual test expecting `0` at `5000`
must fail before the fix. Afterward require these exact observations:

| Subtotal cents | Local fee at B3 | Remote fee at B3 |
| --- | --- | --- |
| 4999 | 499 | 749 |
| 5000 | 0 | 250 |
| 5001 | 0 | 250 |

After B4, require:

| Subtotal cents | Local fee at B4 | Remote fee at B4 |
| --- | --- | --- |
| 5000 | 499 | 749 |
| 7499 | 499 | 749 |
| 7500 | 0 | 250 |
| 7501 | 0 | 250 |

At every stage, `shipping_fee(-1)` retains the exact existing exception and
message. The function signature, baseline existing test file, infrastructure
ownership file, and original AGENTS.md prefix remain unchanged. The dirty
`notes/local-note.txt` retains its exact bytes and its original Git base version;
it must still appear as the same unrelated uncommitted modification at the end.
The whole test suite must execute actual tests; an empty suite is not a pass.

The user-facing result must distinguish the observed original defect, its first
correction, and the later requirement change. No assertion in this fixture is a
recorded native observation or a live AWS result.
