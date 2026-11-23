# Frozen greenfield native fixture

**NOT RUN.** This is input to the [native pilot proposal](../native-pilot-plan.md),
not a completed example or a grant of authority. The controller stages only
`initial/` before G1, `stage2/` before G2, and `stage4/` before G4. Later answers
and changes stay outside the model's project until their stage begins.

## Initial files

<!-- pilot-file: initial/pilot/goal.md -->
```markdown
# Workshop booking prototype

I want a booking service for a community workshop, eventually hosted on AWS.
For this first slice, help me work out the booking rules and implement a small,
local Python prototype. I want you to guide the consultation and turn the
answers into a specification, design, tasks and verified code.

Use Python 3.10 or newer and its standard library. The first slice is one
process, one workshop session, and an in-memory domain model. There is no web
API, database, persistence, authentication, account discovery or deployment in
this pilot. Do not select AWS services without a delivery requirement for them;
record any later hosting questions as deferred work. No packages are needed.

The fixture owner will supply the remaining product rules after your opening
consultation. Preserve these technical and scope constraints when recommending
the next steps. Record consequential questions rather than inventing answers.
```

<!-- pilot-file: initial/src/__init__.py -->
```python
"""Local workshop booking domain."""
```

<!-- pilot-file: initial/tests/__init__.py -->
```python
"""Standard-library tests for the local prototype."""
```

## G1 prompt

<!-- pilot-file: prompts/G1.txt -->
```text

Stage G1: opening consultation only.
Read pilot/goal.md, the adoption manifest and mapped project context. Inspect
whether adoption produced usable instructions and an empty application work
ledger. Explain your recommended first slice and ask at most three material
questions needed to settle its business behavior. Do not ask for a service,
language or tool choice already settled by the supplied scope. Do not implement
code, accept phase reviews, or invent product answers. Save your findings and
questions to the mapped project context and handoff. If you create an active
work item, use ID 0100-booking, greenfield mode and requirements-first route.
Return stage G1 with needs-answers unless a real blocker prevents consultation.
```

## Fixed answers supplied for G2

These answers are deliberately withheld from G1. They constitute the same fixed
product-owner response regardless of the opening questions' wording. If an
important new question cannot be answered from these inputs or routine local
engineering judgment, record a blocker instead of changing the scenario.

<!-- pilot-file: stage2/pilot/answers.md -->
```markdown
# Frozen booking answers

Source: synthetic fixture decisions supplied by the pilot controller under the
actual approval recorded in pilot/approval.md. These are product inputs, not a
claim that a user has reviewed future generated artifacts.

## Capacity and scope

There is one workshop session per BookingBook instance. Capacity is an integer
from 1 through 100; booleans are not integers for this contract. The first
examples use capacity 2. No concurrent threads, persistence or distributed
guarantee is required. Do not imply that these local rules establish an atomic
AWS booking system.

The public helper is src.capacity.remaining_capacity(capacity, confirmed).
It returns capacity minus confirmed. Confirmed must be an integer, excluding
booleans, from 0 through capacity. Invalid capacity raises
ValueError("invalid_capacity"); invalid confirmed count raises
ValueError("invalid_confirmed"). Neither input is silently coerced.

## Booking contract

The public class is src.booking.BookingBook(capacity). Its constructor uses the
same capacity rule. reserve(request_id, attendee_id) accepts strings with at
least one non-whitespace character, preserving the exact supplied strings as
identities. Invalid values raise ValueError("invalid_request") before mutation.

Each newly confirmed request returns a plain dict with exactly booking_id,
attendee_id and status. Status is "confirmed". Booking IDs are B0001, B0002 and
so on within the instance. Only a new confirmed booking consumes an ID or seat.

Repeating a request_id with the same attendee_id returns an equal result without
consuming a seat or changing the original booking. Returned dictionaries must
not let a caller mutate the stored record. Reusing a request_id with a different
attendee_id raises ValueError("idempotency_conflict") without changing state.
Handle an existing request before checking whether the workshop is full, so a
successful retry continues to work after the final seat is taken.

At this initial stage, a new request_id for an already booked attendee is a new
booking and consumes a seat. Do not add an unrequested uniqueness rule.
A new request when capacity is exhausted raises ValueError("slot_full") and
does not reserve an ID or create a booking. Failed requests do not alter state.

snapshot() returns a fresh plain dict with exactly capacity, confirmed and
remaining. Confirmed counts bookings. Remaining uses the public capacity
helper. Snapshot mutation must not alter the booking book.

## Fixed delivery split

There are exactly two implementation tasks:

- T-001 delivers the independent capacity helper and tests in src/capacity.py
  and tests/test_capacity.py. CHK-001 covers its valid boundaries and invalid
  inputs. It has no dependency on T-002.
- T-002 depends on T-001 and delivers the BookingBook implementation and tests
  in src/booking.py and tests/test_booking.py. CHK-002 covers booking, capacity,
  retry, conflict, state-preservation and returned-object isolation.

Use distinct requirement and design links appropriate to each task. Every
required behavior needs a correctness property and a fitting check. Finite
example/contract tests are suitable; no external testing package is authorized.
The combined standard-library test discovery is the integration check.

G2 ends after T-001 is actually verified and complete, with T-002 unfinished,
an implementation-phase handoff, and the exact execution policy staged by the
controller. G3 executes only T-002 using the bounded task controller. Do not
start that controller or another model from G2.

Sequential author review of requirements, design, and tasks is delegated only
within these frozen decisions by the real pilot approval. Perform each review,
record actual findings, and identify it as delegated author review. Do not
record authority=user or assert independent review.
```

<!-- pilot-file: stage2/pilot/execution-policy.json -->
```json
{
  "schema_version": 1,
  "authority_ref": "pilot/approval.md",
  "limits": {
    "max_workers": 1,
    "max_tasks": 1,
    "timeout_seconds": 900,
    "check_timeout_seconds": 60
  },
  "tasks": {
    "T-001": {
      "write_paths": ["src/capacity.py", "tests/test_capacity.py"],
      "checks": [
        {
          "id": "CHK-001",
          "argv": ["python3", "-B", "-m", "unittest", "discover", "-s", "tests", "-p", "test_capacity.py"],
          "inputs": ["src/capacity.py", "tests/test_capacity.py"]
        }
      ]
    },
    "T-002": {
      "write_paths": ["src/booking.py", "tests/test_booking.py"],
      "checks": [
        {
          "id": "CHK-002",
          "argv": ["python3", "-B", "-m", "unittest", "discover", "-s", "tests", "-p", "test_booking.py"],
          "inputs": ["src/capacity.py", "src/booking.py", "tests/test_booking.py"]
        }
      ]
    }
  },
  "integration_checks": [
    {
      "name": "booking-regression",
      "argv": ["python3", "-B", "-m", "unittest", "discover", "-s", "tests"],
      "inputs": ["src/", "tests/"]
    }
  ]
}
```

<!-- pilot-file: prompts/G2.txt -->
```text

Stage G2: settle the specification and complete only its independent first task.
Read pilot/answers.md and the saved consultation. Reuse all supplied answers,
record their actual sources, and resolve only remaining material gaps. Use the
existing 0100-booking item or create it with greenfield mode, requirements-first
route and the CLI's default structured specification policy. Do not create a
second ledger or relax required analysis/properties.
Author substantive requirements. Use the analyze operation to obtain its actual
request, perform semantic analysis in this session, write a response matching
that request's response_schema and a separate honest review note, then record
the response. Resolve blocking findings from the frozen sources or stop.
Perform and record the actual delegated requirements review before continuing
to design. Author and review design. Use properties to derive and record actual
traceable correctness properties and suitable test strategies. Create exactly
T-001/CHK-001 and T-002/CHK-002 as defined by the answer bank; finish their real
task/check mappings and perform the delegated task-plan review before advancing.
Implement only T-001 in its two declared files. Run its meaningful local check
with python3 -B, record actual source-bound evidence and author acceptance, and
mark it complete only when valid. Leave T-002 unchecked and unimplemented.
Copy pilot/execution-policy.json byte-for-byte to
specs/0100-booking/execution.json. Inspect status and run-plan for T-002 without
execution; a dirty-worktree preflight blocker is expected until the operator
reviews and commits this stage. Do not commit, invoke run --execute, install
anything, or start another model. Save the exact next task, accepted answers,
check results and remaining operator handoff. Return G2 paused, not complete.
```

## G3 controller stage

There is no G3 direct prompt or extra model call. The controller receives the
actual reviewed T-002 contract, its declared file scopes, the implementation
context, and its own strict worker-result schema. The operator follows the
proposal's exact preflight, commit, run, inspect and apply sequence. The engine
must still enforce its own prerequisites; this text cannot grant an exception.

## Changed decision supplied only for G4

<!-- pilot-file: stage4/pilot/change.md -->
```markdown
# Booking decision change

Source: the next frozen synthetic product decision under pilot/approval.md.
This deliberately replaces one initial rule in pilot/answers.md. Keep that
earlier source and its historical evidence intact.

Within a BookingBook, an attendee now has at most one confirmed booking.
For a new request_id with an attendee_id that is already confirmed, return the
same booking result, consume no seat and allocate no booking ID. Register this
new request_id as an alias for the original attendee, including when full.
Later reusing either request_id with a different attendee must still raise
ValueError("idempotency_conflict") without mutation.

The first successful confirmation order still controls B0001, B0002, etc.
All input validation, snapshot, copy-isolation, capacity, existing-request retry
and full-capacity rejection behavior remains as previously specified. The
independent capacity helper's contract is unchanged. No new API, task, storage,
AWS resource or dependency is requested.
```

<!-- pilot-file: prompts/G4.txt -->
```text

Stage G4: reconcile the supplied change after the inspected G3 result.
Resume 0100-booking from saved context and actual repository/controller state.
Read pilot/change.md and preserve pilot/answers.md as history. Record the new
decision with its real source. Inspect stale analysis/properties/reviews and
obtain a sync preview before applying its exact fingerprint. Resolve semantic
impact before editing the linked requirements, design, properties and task
acceptance. Preserve stable IDs and old review/evidence history. Obtain another
fresh preview when edits change the first preview; never apply a stale token.
Use the actual delegated review sequence and fresh source-bound analysis and
properties. Reopen affected completion and retain valid work when the tool's
declared identities permit it. Shared-artifact invalidation can conservatively
reopen more than one check; report this accurately and reverify as required.
Implement the changed attendee rule in T-002's declared files. Do not rewrite
src/capacity.py or its unchanged tests merely to make the diff look complete.
Run the affected tests and required integrated verification using python3 -B;
record actual current evidence and author acceptance. Save a handoff describing
the original rule, changed rule, observed reconciliation, final task state,
checks, and deferred AWS deployment. Do not invoke the controller or another
model. Return G4 implemented only if the local changed contract is established;
otherwise return the observed blocker without inventing completion.
```

## Exact behavioral observations

At G3, require helper boundaries `(1, 0) -> 1`, `(2, 2) -> 0`, and `(100, 99) -> 1`,
plus invalid capacities `0`, `101`, `True` and invalid confirmed values `-1`,
`capacity + 1`, `True`. Require the precise `ValueError` codes from the contract.

For a capacity-2 book, `reserve("r1", "a")` returns B0001 and a replay returns an
equal result. `reserve("r1", "b")` conflicts without mutation. Initially,
`reserve("r2", "a")` creates B0002; a new third request is full. Replays continue
to work after the second booking. Fresh invalid requests and mutation of returned
dictionaries must not change the stored result or snapshot. Tests must examine
these outcomes rather than merely assert that a method was called.

After G4, `reserve("r1", "a")` and `reserve("r2", "a")` return the same B0001;
confirmed stays 1. `reserve("r3", "b")` creates B0002. A new alias for attendee
`a` still succeeds while full, but reusing that alias for `b` conflicts. A new
attendee still receives `slot_full`. The capacity-helper source and tests remain
byte-identical to their inspected G2 version. Historical original-rule evidence
remains identifiable; only current checks support final completion.

These are future assertions for the reviewer. This document records no observed
passing check, accepted artifact, native invocation, or AWS outcome.
