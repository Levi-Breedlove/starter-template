# AWS Starter Template v1.0.1 documentation candidate

The local candidate is ready for patch review. The verified maintenance source is `b9c581f05f7273393a90dedaa6257367049e7686`. The distributable commit is `73eef0d138670e5b13c573ea2ca7cf78a35fb04a`, a child of v1.0.0. Two builds reproduced its tree `e42888f9e0628d13840539623ab8b84897369af3`. [Task ledger](../../specs/0005-repository-documentation/tasks.md) · [Receipts and hashes](verification.json)

## T-001 · Repository conventions

The new editable structure record describes file placement and ownership, the CLI work-ID grammar, the recommended numbered naming scheme, traceability, and how to record accepted conventions. The installer changes only the structure Markdown literal. Comparing the full installer syntax tree after substituting an identical value for that literal produced identical results.

Seven application scenarios passed on the exact candidate tree. A fresh distribution copy and a standalone greenfield install received the new conventions. An existing application without a structure record received the new default. Both a conventional and an explicitly mapped existing structure file kept their exact path and bytes. The stock and customized v1.0.0 upgrades preserved their own structure records byte for byte. All seven applications passed their installed setup and repository checks. Every repeated installation or upgrade returned zero writes. [Scenario details](verification.json)

## T-002 · Developer README

Reviewed first use, requirements and design, semantic traceability, project conventions, AWS boundaries, and preservation of existing authority against the installed commands and guides. The review clarified that the example uses illustrative IDs and identified the distinct frozen pilot and v1.0.0 first-use candidates. The two README files specify the commands relevant to their respective roots. The distributed README is a byte-for-byte copy of its source. Its initial tree matches the Git package at the root and each expanded directory. All 26 distributed README links and 12 maintenance README links resolved locally. The local links use file destinations with zero heading fragments.

All **207** regressions passed in Codespaces. The source checker passed 464 local links and the distribution checker passed 265. Both builds produced 102 tracked files and 76 verified managed hashes. Compared with v1.0.0, five file contents changed in the distribution:

- `README.md` and `CHANGELOG.md`
- `project/structure.md`
- `.aws-workflow/scripts/bootstrap.py`, whose only change is the Markdown seed
- `.aws-workflow/manifest.json`, which updates the bootstrap hash and package source digest

## Evidence scope and approval

Earlier maintenance inputs changed in four places. Read-only `sync` previews identify affected historical checks across items 0002–0004. Their evidence continues to describe the candidates those checks verified. The v1.0.1 task receipts establish the documentation and offline behavior of this candidate. The original eight-stage pilot ran on frozen source `64875ee`, and the separate 87-second `start` smoke ran on released distribution `895a9b9`. Optional AWS Emulator runtime and live AWS behavior remain unverified for this patch. [Frozen pilot](../0004-developer-workflow/native-pilot-closeout.md) · [v1.0.0 first-use observation](../0004-developer-workflow/native-first-use.json)

The patch awaits owner review. GitHub still uses v1.0.0 as the default distribution. After approval, submit the maintenance branch through the established review control, rebuild and verify the approved tree, and promote the matching distribution and tag under the existing release procedure. [Distribution and release procedure](../../docs/distribution.md)
