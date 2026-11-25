# Evidence and its scope

Store compact sanitized observations under `evidence/<work-id>/`, or link the project's existing durable CI records. Evidence supports a specific claim about identified inputs; a saved file is not automatically proof of acceptance.

## Minimum record

| Field | Meaning |
| --- | --- |
| Claim/check and contract IDs | Which requirement or preserved behavior this establishes. |
| Candidate | Commit, or base revision plus patch identity for uncommitted work. |
| Relevant inputs | Specification, fixtures, dependencies, configuration, and tool/procedure versions. |
| Environment | Local, native client, CI, emulator, or an actually authorized cloud target. |
| Artifact | Digest/immutable identity when a built artifact is tested. |
| Method and observation | Actual command/procedure, result, time, useful output, limits and skipped checks. |
| Review | Reviewer, candidate/scope, findings, independence level, or incomplete status. |

Keep raw credentials, customer information, account inventories, session transcripts with secrets, binary artifacts, and large logs outside the repository. Link authorized storage where necessary. Public guidance citations and brief sanitized outputs normally suffice for research and static checks.

## Freshness

When inputs change, assess affected claims and reopen their acceptance until reassessed or rerun. Retain old records with their original identity and scope. Do not edit a prior failed result to make it appear successful. A later pass is a new observation.

At release, link the actual passing, failing or deferred checks from the [current handoff](../delivery/current-handoff.md). A new application begins with no acceptance observations.
