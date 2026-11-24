# Infrastructure

**Status:** Empty implementation boundary. This scaffold selects no architecture, IaC framework, account, region, or deployment resources. Existing project choices remain authoritative during adoption.

Keep infrastructure code here after consultation records the project’s accepted design. Choose the IaC framework that fits the existing project and team; this template does not impose CDK, CloudFormation, SAM, Terraform, or a particular compute service.

## Greenfield and brownfield entry

For greenfield work, make the decisions below before generating infrastructure. For brownfield work, first inventory the repository’s existing IaC, state/backend configuration, stack ownership, environment mapping, deployed artifact references, and pipeline. Link existing locations instead of moving or duplicating them merely to fit this folder. See [brownfield adoption](../guide/05-brownfield-adoption.md).

Distinguish repository intent, recorded deployment evidence, and live state. Drift remains **unknown** until an authorized assessment establishes it. Do not recreate or import existing resources, migrate state/backends, rename resource identities, or take over stack ownership unless explicitly included in the approved migration scope. Prepare migration effects and recovery evidence before the applicable decision; existing authorization continues within its scope.

Report the coverage of any live drift check: unsupported resources and properties remain outside its conclusion. CloudFormation import does not itself verify that live properties match the template. See [the AWS delivery reference](../docs/reference/aws-delivery.md) for source-backed adoption and verification boundaries.

## Decisions required before implementation

- Workload and data flows, service boundaries, availability/recovery objectives, and network trust boundaries.
- Environment separation, region selection, identity, state ownership, and configuration/secrets sources.
- IaC framework, dependency/version policy, stateful-resource lifecycle, and reuse boundaries.
- Deployment mechanism, preview/review method, drift handling, and recovery path.
- Cost assumptions, experiment limits, and cleanup ownership.

Record these choices in `specs/<work-id>/design.md` and the project’s decision records (see the [decision template](../templates/decision.md)), using the constraints in [the project brief](../project/brief.md). For an existing project, preserve accepted choices and propose changes only with a concrete benefit and tradeoff. This reusable scaffold imports no application architecture.

## Verification layers

| Layer | What it can establish |
| --- | --- |
| Static checks | Syntax, selected policy rules, and expected template properties |
| Local tests/emulation | Application logic and the supported simulated integrations |
| Authorized cloud preview | Proposed infrastructure changes in the named target |
| Authorized cloud tests | Actual service integration, IAM, networking, and runtime behavior |

Do not call an IaC command offline merely because it is a preview: synthesis can execute project code and perform AWS context lookups; CDK diff can create a change set and use deployment permissions. Classify the selected tool’s behavior before running it.

Local emulation cannot establish cloud parity for IAM, quotas, networking, or all service behavior. SAM local runs a local Lambda environment, but its SDK calls can still reach real AWS unless dependencies/endpoints are controlled. Document the boundaries of local test evidence. For compatible AWS operations in new or existing projects, see [AWS Emulator setup and verification](../guide/08-aws-emulator.md).

## References

- [CDK context](https://docs.aws.amazon.com/cdk/v2/guide/context.html)
- [CDK diff](https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-diff.html)
- [AWS testing and emulation limits](https://docs.aws.amazon.com/lambda/latest/dg/testing-guide.html)

