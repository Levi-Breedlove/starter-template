# AWS consultation and delivery reference

**Public guidance reviewed:** 2026-11-22. This reference defines how the workflow uses official AWS capabilities. It does not establish account access or a deployed workload.

## Use the official toolkit in the selected client

The official Agent Toolkit for AWS supplies AWS guidance and tools; the coding agent and repository supply the development process. AWS documents a Codex integration and distinguishes public documentation from operations that use credentials. Reuse the installed official AWS Core and AWS Data Analytics identities rather than adding local replacements. [Official setup](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/quick-start.html) · [Official source](https://github.com/aws/agent-toolkit-for-aws)

When relevant and allowed, discover guidance through AWS Core `search_documentation` with `agent_skills`, then retrieve the returned exact skill ID through `retrieve_skill`. Read additional references only as needed. A documentation-only request can use current official documentation directly. The repository does not bundle private or copied AWS skills. [AWS skills reference](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/skills.html)

Record four separate observations: available in the client, installed identity/version, loaded for the current task, and tested through a permitted call. A setup page is evidence of a documented capability; it is not proof that a particular hosted connection is loaded or updated. Public setup checks must not inspect credentials, accounts, account metadata, resources or spending.

## Derive the design from the requirements

Consult on user behavior, data, constraints and service levels before recommending services. A small asynchronous workload may suggest serverless components; a latency, runtime, portability or ownership constraint may lead elsewhere. Keep alternatives proportionate. Explain why the recommendation meets the requirements, its main cost and operational tradeoffs, and which assumption would change it.

A useful design covers the user journey, trust boundaries, data flow, failure paths, deployment ownership, observability, recovery and cost drivers. The template chooses no application language, IaC framework, account layout, region or budget by default. Preserve an existing project's accepted stack unless a concrete requirement justifies a reviewed change.

## Separate public guidance from account operations

| Action | Preparation |
| --- | --- |
| Read public AWS documentation | No account or credentials needed. |
| Inspect an existing account or runtime | Task-authorized accounts, regions, resources, access limits and evidence scope. |
| Prepare infrastructure or application changes | Actual project stack and ownership, bounded desired change, relevant local checks. |
| Produce a preview | Establish whether the selected command reads an account, creates a change set or publishes assets. |
| Deploy | Concrete candidate/artifact, target environment, authorized action and limits, applicable review, recovery and verification plan. |
| Operate or clean up | Named ownership and scope, preserve retained data/resources, observe the outcome. |

Instructions and tools do not grant authority. Downstream AWS service permissions still govern resource access. Prefer the project's existing short-lived identities and delivery controls. [Toolkit IAM](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/security_iam_service-with-iam.html) · [Tool categories](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/understanding-mcp-server-tools.html)

## Brownfield evidence

Repository declarations, deployed observations and unknowns are different evidence classes. Establish IaC ownership, state storage, deployment triggers, interface contracts and operational dependencies before changing them. Importing existing resources is a deliberate migration task; AWS notes that import does not verify every template property against actual configuration. Drift detection also has resource/property coverage limits. Record coverage and observation time rather than claiming a universal clean baseline. [Resource import](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/import-resources-manually.html) · [Drift detection](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html)

For CDK, inspect the actual version and diff method. AWS documents different `auto`, `change-set` and `template` behaviors; a command described as a preview may involve AWS interactions or asset publishing. Select the method from the real task and authority. [CDK diff](https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-diff.html)

## Release evidence

Before a consequential deployment decision, prepare the actual reviewable change. A release record should identify the candidate, artifact where applicable, configuration, target, migration and recovery approach, acceptance checks, expected costs and remaining unknowns. Reuse prior authorization within its scope.

After an authorized deployment, observe terminal execution state, critical user behavior and appropriate telemetry. Include migration outcomes, observation window and remaining limitations. A local test, a successful API request, or a recorded command alone does not establish production readiness. If an operation times out, reconcile its real state before retrying. Rollback must account for data/schema compatibility and retention; restoring a Git commit is not an AWS recovery procedure.

Use the existing [release workflow](../../workflows/release.md), [deployment runbook](../../runbooks/deploy.md), [rollback runbook](../../runbooks/rollback.md) and [cost template](../../costs/estimate-template.md). Instantiate only the artifacts applicable to the project's actual delivery system.
