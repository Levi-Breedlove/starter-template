# v1.0.1 appointment-booking walkthrough review

The v1.0.1 candidate includes the beginner terminology revision within T-002. The verified maintenance source is `c77daaec117d7b572582addb7d8382f41ed17458`. The revised application commit is `eb9e4ba5cc09038fc175bfec4653a1cfcc55c201`. Two builds matched tree `34a1aaeff6fbbcd42738037f99168bd3fd0205ec` across all 102 files. The distribution differs from the previous local candidate only in its README. [Verification receipts](walkthrough-verification.json) · [Approved plan revision](plan-review-revised.md) · [Task ledger](../../specs/0005-repository-documentation/tasks.md)

## Walkthrough review

The README starts with one patient retrying an appointment after a lost response. The example traces intended behavior through the design and the rule it must preserve, then shows how the task connects implementation to the verification check and its result. Each of the six artifacts has a name and identifier prefix, purpose, question, location, and example linked to the same appointment-booking work item. The table labels the demonstrated appointment ID and result as illustrative. A checked heading link leads to the section reporting actual template verification.

Mermaid 11.17.0 parsed the exact README flowchart in the local VS Code distribution. The independent review verified all nine labels and nine edges, including the six descriptive labels with identifiers. The parser rejected malformed syntax in a negative control. This establishes grammar and graph structure. GitHub rendering and browser layout remain unverified. All 26 local README links resolved, including its verification heading link. The maintenance and application repository checkers passed.

## Candidate verification

All 207 offline regressions passed. Seven local application scenarios passed on the revised distribution, including unchanged structure bytes during stock and customized v1.0.0 upgrades, mapped and conventional brownfield adoption, and repeat installations. The packaged README matches its canonical source byte for byte.

The earlier v1.0.1 verification remains tied to the previous candidate. A reviewed reconciliation reopened both checks because their shared specification inputs changed. The new receipts establish the two checks on the revised candidate. The eight-stage pilot and 87-second first-use observation retain their v1.0.0 scope. The revised candidate awaits patch approval. [Earlier candidate review](candidate-review.md)
