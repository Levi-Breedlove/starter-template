# Repository publication observation

**Observed UTC:** 2026-11-22T11:03:58.027523+00:00.  
**Check:** CHK-005; repository delivery portion.  
**Branch:** `main`.  
**Published snapshot:** `ee1294e4a123aa929c7f7cf178e326562cad5e9d`.  
**Tree:** `df97fdf8d6e61d961dd99e048018c35cafa8599f`.

The branch update used the previously observed head as an expected value, with no force update. A recursive remote tree was retrieved without truncation. All 98 remote file paths, modes and Git blob identities matched the prepared local manifest. There were zero missing, unexpected or mismatched files. The observed main head matched the published commit, and repository visibility remained private.

The local portion is recorded in [local checks](local-checks.md): 89 passing fixtures, zero link/structure issues, and zero prohibited-name matches in the observed current tree. Exact tested Python input identities are retained there.

This receipt identifies the observed source snapshot. A following completion-record commit adds this receipt and updates task/evidence/handoff state; it does not alter executable source or test files. The delivery process compares that final remote tree too, and reports the final commit to the user. The receipt does not claim a commit contains its own future hash.

Native client activation, behavioral model evaluation and AWS outcomes remain outside these observations. Existing repository identity and historical Git objects were preserved; neutral naming applies to current content and relative file paths.
