# Codespaces startup and onboarding correction candidate

Base source: `404480b72b9ae0c3ade0a3a307fcbc4468dcdf3b`. This is a separately reviewed change candidate, not a
native pilot result or proof that the original local evidence is current for this
changed tree.

The user reported a G1 startup failure (exit 1, read-only client-state mount,
no model event), one consumed invocation slot, no B1 launch, no retries or AWS
operations, and successful adoption checks. The reported pilot branch and its
uncommitted evidence were not accessible through the remote repository. No
existing pilot evidence or branch was altered; those observations need to be
preserved by the operator. T-008/CHK-008 remain open.

This candidate adds a read-only native startup prerequisite check, integrates
it before default native execution, and provides first-use consultant guidance
in both root and generated instructions. The setup check is deliberately not
a claim of effective client startup or a substitute for the actual trial.

Ten focused offline tests passed in a separate Linux Python 3.13.5 test directory.
The helper and test file were the only files executed in that test run.
Tested Git blob identities:
- `workflow_engine/native_preflight.py`: `abf12880f039dab6b9316fd4713a3583018fc4e1`.
- `tests/test_native_preflight.py`: `abcef6b6704b37d4ab34bf87a6a5e25c6aa06fb5`.

Additional installed-package, runner, and onboarding regressions are included
but require the full repository test suite. No full suite, actual client
startup, native model behavior, or AWS execution was tested in this change
session. Reconcile the affected review and evidence records against the actual
integrated candidate after running the full suite, before merging. Do not
mark T-008 complete until the approved native trial is actually observed.
