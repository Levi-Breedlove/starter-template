# Initial template stabilization

**Offline verification passed. Native-client acceptance remains open.** The
isolated readiness branch verified source `26f21269460366a7743814461fa126c3bfbd7bdd`, published as a fast-forward
from `b9e1f15c1d2f479f42f36a172b4356f16bfa8ed6`. GitHub returned the same source revision and tree, with all
153 path, mode, type, and object identities matching. The original checkout's
five uncommitted files were checked byte-for-byte. Both previous pilot receipts
were preserved. [Structured observation](codespaces-stabilization-observation.json) ·
[Original G1 observation](native-pilot.md)

## Execution checklist

| Gate | Observed result |
| --- | --- |
| Inspect and isolate | Fetched the exact draft PR head, compared its three initial commits and used a separate readiness worktree. |
| Correct and review | Kept falsy injected backends, made a missing preflight module fail structure checks, and pinned the selected native executable across worker directories without collapsing symlink traversal. Focused regressions reproduced the issues and passed after correction. A separate reviewer confirmed the final launcher fix. |
| Verify and reconcile | All 197 regression tests passed in 47.976 seconds on Linux/Python 3.14.2. The source link and structure check passed with 108 Markdown files, 415 local links, and 32 core files. Fingerprint-checked reconciliation reopened the affected checks. Contracts, phase reviews, and recorded analysis/property mappings remained current. |
| Deliver and freeze | The tested source is on the private readiness branch. The release freeze awaits actual native acceptance and the existing PR review and merge controls. |

[Actual regression output](codespaces-stabilization-tests.txt) ·
[Requirements and task ledger](../../specs/0004-developer-workflow/tasks.md)

## What a developer does

1. From this checkout, preview and apply adoption into the application directory.
   Choose greenfield for an empty directory or brownfield for an existing project.
2. Open the application root in Codex in Codespaces and type `start`. Codex
   checks setup and mapped context and starts or resumes the consultation.
3. Follow the scoped work through research, requirements, design, tasks,
   implementation, verification, review, and separately authorized delivery.
   Use `resume` to continue saved work.

Both actual adoptions matched preview and repeated cleanly. Brownfield preserved
instructions, source, ownership, pipeline, existing configuration, and its
uncommitted note. Both installed setups were ready for ordinary consultation
while optional native execution was blocked. The seven case-insensitive shortcut
definitions matched source instructions, generated instructions, and the
quickstart. The installed CLI exercised all five routes with fixture review
responses and recovered context in fresh processes. Plan-only ended at
`planned` with no eligible implementation tasks. Model behavior on a literal
first-use `start` has yet to be observed. [Quickstart](../../guide/00-quickstart.md)

The lifecycle incorporates design, security, networking, reliability, costs and
IaC choices, with local tests and authorized cloud checks at their respective
boundaries. Release and recovery follow the application's established pipeline
and runbooks. The frozen context fixture comparison reproduced the previous
character counts for the same inputs. [AWS guidance](../../guide/02-aws-guidance-and-access.md) ·
[Infrastructure and local emulation](../../infrastructure/README.md) ·
[Costs](../../costs/README.md) · [Release and recovery](../../guide/04-maintain-and-release.md)

## Codespaces and AWS guidance

Within the agent sandbox, the new preflight exited 1 and reported read-only
client state. The user previously confirmed the same directory was on an
`rw` mount and passed `test -w` from the ordinary Codespaces terminal. The
synthetic direct and controller guards stopped before reservation. The
readiness probe uses directory metadata and executable discovery. The ordinary
terminal's full probe output and actual client startup remain pending.
Use the exact commands in the Codespaces guide from the launching terminal.
[Codespaces preflight](../../guide/07-codespaces.md)

The current Codex surface exposes AWS Core and AWS Data Analytics. AWS Core
returned public skill discovery and retrieved `aws-serverless`, and AWS Data
Analytics returned public documentation. The regular/native client's installed
and loaded plugin state is unverified. The official AWS quickstart and upstream
toolkit confirm the setup route. Local emulation and CDK preview boundaries were
cross-checked against official guidance. Zero AWS account or resource operations
ran. [AWS Toolkit quickstart](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/quick-start.html) ·
[Official toolkit](https://github.com/aws/agent-toolkit-for-aws) ·
[Lambda testing](https://docs.aws.amazon.com/lambda/latest/dg/testing-guide.html) ·
[CDK diff](https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-diff.html)

## Reuse and distribution

The additive installer supplies the reusable runtime and excludes maintenance
specifications, prior evidence, and active client state. Its existing collision
checks require a deliberate merge for an upgrade. The package needs Python
3.10+ and uses the standard library. Native execution requires POSIX process
controls and its documented executables. This pass ran on Linux Codespaces.

GitHub reports a private repository with template generation disabled.
Private adoption can use a pinned source revision and the installer. GitHub's
template feature copies repository files and would also copy maintenance
records from the selected branch. No release tag or distribution license is
declared. Contribution checks are documented in the repository's PR template.
[GitHub template behavior](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository) ·
[Contribution checklist](../../.github/pull_request_template.md)

## Native acceptance

The original G1 startup failure consumed one allocation. Seven original slots
remain unused, and this pass used zero native invocations. CHK-008 is recorded
as `not-run`, and T-008 remains open. Next, confirm the full no-model preflight
and selected client settings in the regular Codespaces terminal. A replacement
G1 requires explicit authorization. Retain the original reservation and receipts
while executing the separately authorized frozen stages, then assess every
criterion. A native controller result, actual consultation and continuation,
and live AWS operations remain unverified within the current evidence.
[Owned continuation and authorization](../../delivery/current-handoff.md) ·
[Frozen plan](../../evaluations/native-pilot-plan.md)
