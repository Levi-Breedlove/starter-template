# Repository documentation design

## DES-001 — Project-owned conventions

Use the existing editable structure-record seed in `scripts/bootstrap.py`. Its default application path is `project/structure.md`; an adoption can map an existing location. Draft practical conventions that a team can adopt or revise. Include code and language exceptions, component ownership, work-scoped ID references and the evidence needed to identify the candidate, inputs, method and result. The bootstrap already distinguishes initial records from managed package bytes. Keep that ownership rule for upgrades, including documents that still contain the old default text.

Check the seed by building the distribution and adopting the workflow into a new application. For conventional and custom brownfield paths, compare the original bytes before and after adoption. For upgrades, use a genuine v1.0.0 installation with the old stock content and a separate installation with a user edit. Verify the same canonical record survives each upgrade and a repeated install remains idempotent.

## DES-002 — Application README and release preparation

Edit `distribution/README.md.in`, which the packager copies to the application root. Keep maintainer details in the source README and the release record in the changelog. Describe the actual initial tree, then label the populated example separately. Show how a developer begins consultation, records decisions and traces one booking behavior through its feature specification, task, verification and evidence. Explain tool availability, local emulation, authorized cloud execution and the project's choice of task authority. Use the existing [adoption procedure](../../docs/reference/bootstrap.md) and [distribution contract](../../docs/distribution.md).

Build twice from the same maintenance candidate into unused local directories. Compare tracked application trees, check the package contains blank project work and review the decoded local links and README anchors on the resulting files. Exercise the documented brownfield commands in a disposable project and run the source suite and repository checkers. Record the source revision or base-plus-patch identity and generated tree. A passing offline result covers this documentation candidate. The prior native pilot and first-use observations retain their original identities. Publication and promotion use separate approval.
