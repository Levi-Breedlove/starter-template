# Scaffold verification receipt

**Work/checks:** 0001-workflow-foundation; CHK-001–CHK-004.  
**Date:** 2026-11-21 (America/Los_Angeles).  
**Scope:** Research/procedure consistency, offline checker behavior, repository file links and required structure.  
**Environment:** Local Python 3.12.14 with standard library only; no network or AWS calls from the checks.

## Observed local results

| Check | Method | Observed result |
| --- | --- | --- |
| CHK-001 | Review official-source ledger, capability map, research and video-access labels. | Documentation, two published visual transcripts, and five description/metadata-only video listings distinguished. Proposed behavior and untested runtime claims labeled. |
| CHK-002 | Cross-document review of root instructions, both adoption paths, templates, release/runbook contracts, roadmap and foundation specification. | Skill opt-out and conditional release prerequisites corrected; existing project authority and scope preserved. Later automation/trials remain unfinished. |
| CHK-003 | `python3 -m unittest discover -s tests -p 'test_*.py' -v` | 14 tests passed. Fixture scope covers valid/missing/escaping targets, source symlinks, incomplete scans, comments/fences/escapes, placeholders and CLI behavior. |
| CHK-004 | `python3 scripts/check_repository.py` | PASS with zero issues on the assembled scaffold. This validates links/structure only. Final publication readback is pending at this receipt's initial creation. |

## Code identity for the observed test run

| File | SHA-256 |
| --- | --- |
| `scripts/check_repository.py` | `3070c5f54c1b4ee9a7789f77606914cf5db81c5ecd6dc33f1e41cb00721ce139` |
| `tests/test_repository_checks.py` | `acf6669ad654fc794c1a8c1799a41b7b9e606247fa688e525d3221f6a6f10c0b` |

The checked files were uncommitted at the initial local run. These content identities bind the observed fixture results. The repository commit created during publication supplies the complete snapshot identity; remote verification is recorded below after it occurs.

## Review findings and closure

A scoped reviewer who did not author the checker reproduced two false-success cases: an unreadable noncore directory was silently omitted, and a fence delimiter inside a comment hid a subsequent real broken link. Both were fixed with regression fixtures. The reviewer reran the original reproductions and observed explicit `unreadable-directory` and `missing-target` failures respectively. Escaped delimiters were also covered by the resulting 14-test suite.

Document review found that skill opt-out needed propagation beyond the root instructions and that release artifacts/previews/review forms should follow actual project applicability. Those instructions were aligned, with justified N/A preserving required project gates. Root integration review also aligned the AWS acceptance metric and framework release requirement.

This was scoped cross-document and checker review, not a claim that every source document received independent review or that an AWS application was tested.

## Publication evidence

Pending repository write and readback. The publishing task will compare every returned Git blob identity with the local manifest and preserve the repository's existing private visibility. This receipt does not claim that step succeeded before it is observed.

## Practical limits

The checker is a bounded Markdown file-target parser. It does not validate all Markdown syntax, heading anchors, undefined reference labels, semantic traceability, native Codex loading, hook execution, scheduling, recovery, CI enforcement, official plugin operation, or AWS behavior. The example application and behavioral evaluation scenarios remain unimplemented/unexecuted.

No full playback of the five description-only videos, head-to-head Kiro benchmark, account inspection, credential access, plugin installation, paid automation, or cloud deployment occurred for this scaffold delivery.

