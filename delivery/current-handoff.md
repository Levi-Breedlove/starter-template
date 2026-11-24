# Current handoff

**Active work** 0004-developer-workflow

**State** Offline stabilization passed on `26f21269460366a7743814461fa126c3bfbd7bdd` in the
`codespaces-readiness` worktree. The source fast-forward and full
GitHub tree readback matched. All 197 regression tests and the source structure
check passed. Both adoption modes, the installed CLI, and all five routes were
exercised. The original checkout and both startup receipts were verified
byte-for-byte. [Readiness assessment](../evidence/0004-developer-workflow/codespaces-stabilization.md) ·
[Canonical tasks](../specs/0004-developer-workflow/tasks.md)

Fingerprint-checked reconciliation refreshed the affected evidence in 0002,
0003, and 0004. The requirements, design, phase reviews, and recorded analysis
and properties continue to identify their accepted inputs.
[Execution plan](../specs/0004-developer-workflow/exec-plan.md)

## Next action

GitHub Codespaces is the primary environment. From the regular Codespaces
terminal in the verified readiness checkout, run the read-only checks below:

```sh
python3 scripts/workflow.py --root . native-check --pilot
codex --version
codex exec --help
```

The agent sandbox reported a read-only mount for the configured client state.
The user's earlier regular-terminal mount check showed that same state directory
as writable. Confirm the effective configured state paths and existing client
controls in the regular terminal. The full native-check output and a native
startup from that terminal remain unobserved. [Codespaces guide](../guide/07-codespaces.md)

T-008 and CHK-008 remain open. G1 consumed one original allocation during the
recorded startup failure. Seven original slots remain unused. Obtain explicit
authorization for a replacement G1 before dispatching any native stage. Keep the
original reservation and results. Use the frozen scenarios, sequential bounds,
and zero retries under the actual approved allocation. Score every criterion
against actual observations before completing T-008. [G1 receipt](../evidence/0004-developer-workflow/native-pilot.md) ·
[Frozen pilot plan](../evaluations/native-pilot-plan.md)
