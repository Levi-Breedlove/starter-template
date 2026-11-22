# AWS integration research: Kiro behavior and a Codex adapter

**Reviewed:** 2026-11-21 (America/Los_Angeles).  
**Scope:** Official public AWS/Kiro documentation, the official AWS toolkit repository, and four primary demo listings.  
**Result:** Design evidence for a repository scaffold. No AWS account access, installation, deployment, benchmark, or production validation was performed for this research.

## Finding

The AWS Agent Toolkit is the AWS-facing knowledge and operations layer. It does not supply the coding agent or its entire development lifecycle. Kiro supplies agent orchestration and development surfaces; the toolkit supplies current AWS guidance and IAM-governed access. A Codex repository can define an equivalent engineering process around the official toolkit, but native Kiro controls and operational results must be mapped and tested separately. [AWS toolkit overview](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/) · [Kiro Workflows](https://kiro.dev/docs/workflows/)

The design should therefore keep three boundaries explicit: the development process, the AWS adapter, and the workload’s delivery system. A successful demo of one small deployment is useful discovery evidence; it does not establish production readiness for another architecture.

## 1. Demo evidence and its limits

The evidence inspected here is publisher-provided description and metadata. No full published transcript or video footage was retrieved. The two YouTube watch-page opens were throttled; indexed official descriptions remained available. These are **discovery-only video references**, not claims that every displayed step or result was independently checked.

| Primary demo | Publication and inspected evidence | What the publisher describes | Use and limitation |
| --- | --- | --- | --- |
| [Introducing Agent Toolkit for AWS — AWS Developers](https://www.youtube.com/watch?v=d1GHVtEFy2A) | 2026-05-06; official channel description and chapter labels | Python Lambda behind API Gateway HTTP API; chapters identify deployment, adapting a skill, an invocation permission step, auditability, and beginning with read-only access | Identifies integration and permission checks worth verifying. Timing and successful endpoint claims are publisher claims, not our benchmark. Current documentation governs implementation. |
| [Ship Without the Guesswork — Kiro + Agent Toolkit](https://kiro.dev/videos/jv3dsOpDeH4/) | 2026-09-30; official Kiro page, 7:28 duration, description | Building a new portfolio site using Kiro and the toolkit | Relevant greenfield entry example. The description’s first-pass success language is not a guarantee or a basis for choosing a production architecture. |
| [Working With Kiro workflows](https://kiro.dev/videos/b4U9PlBI5qM/) | 2026-10-15; official Kiro page, 7:20 duration, description | Generate or choose a workflow, refine steps/agents/branches/conditions, run it, and save a reusable recipe | Supports discovery of the orchestration experience. Runtime semantics are checked against the written Workflows documentation. |
| [AWS Tech Tales: Catching Up with Kiro — AWS Events](https://www.youtube.com/watch?v=w-fn-vELIEs) | 2026-05-04; official channel description | Teaching Kiro an existing codebase, adding features, and using hooks, MCP, and subagents | Relevant brownfield discovery example. It predates the toolkit launch and later Workflows release; it cannot establish those newer features or an AWS deployment result. |

The dates matter. The [AWS toolkit launch announcement](https://aws.amazon.com/about-aws/whats-new/2026/05/agent-toolkit/) is dated 2026-05-06. Kiro’s [Workflows introduction](https://kiro.dev/blog/introducing-workflows/) is dated 2026-09-30. Earlier demos may show a valid older workflow without documenting the current runtime or permission model.

## 2. Current documented capabilities

| Capability | Verified from the written documentation | Repository design implication |
| --- | --- | --- |
| Official Codex integration | AWS documents adding its official marketplace and selecting `aws-core`; plugins package guidance and MCP configuration | Record the actual surface’s availability, installation, loading, version, and public-call evidence separately. Reuse official identities. [Setup](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/quick-start.html) |
| Public AWS knowledge | Documentation search and discovery can operate without AWS credentials; proxy startup behavior varies by configuration | Consultation must not implicitly sign in or inspect an account. Test the intended public path before claiming it works in another surface. [Setup](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/quick-start.html) |
| On-demand procedures | AWS documents discovering relevant skills with `search_documentation`, then loading them with `retrieve_skill`, including references only when needed | Specify the discovery protocol, not a copied private skill collection. The task’s authority remains separate from retrieved instructions. [Skills](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/skills.html) |
| Knowledge versus API tools | AWS distinguishes public information tools from scripts, S3 transfers, and long-running operational tasks | Classify every tool action by data access and side effect. A name containing “check” does not make the operation account-free. [Tool reference](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/understanding-mcp-server-tools.html) |
| IAM enforcement | Downstream AWS services authorize calls under the caller’s identity; temporary credentials and MCP context keys are supported | Use narrow identities and real enforcement. Instructions alone cannot reduce broad credentials. [IAM](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/security_iam_service-with-iam.html) |
| Read-only serverless investigation | AWS documents diagnosis, recent logs/configuration/changes, and trace summaries for supported Lambda-connected resources | Enable only for an explicitly scoped assessment. Missing permissions or telemetry must become evidence gaps, not invented results. [Capabilities](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/capabilities.html) |
| Kiro Web AWS role | A configured IAM role provides short-lived credentials to the sandbox, its tools, and MCP servers | Treat credential delivery as an adapter capability to verify, not something a repository file automatically grants Codex. [Web environment](https://kiro.dev/docs/web/sandbox/environment-configuration/) |
| Kiro Workflows | Isolated steps exchange artifacts through explicit handoffs; the runtime supports branches, bounded loops, waits, and recovery at node boundaries | A Markdown workflow documents the process. Native execution, recovery, and UI parity remain implementation work. [Workflows](https://kiro.dev/docs/workflows/) |

The official repository and hosted distribution can change independently. This research checks public documentation; it does not establish an installed local or cloud plugin revision. Follow supported releases and report unresolved version state. Do not infer a complete hosted catalogue from a search result. [Official toolkit repository](https://github.com/aws/agent-toolkit-for-aws)

### Source nuances that affect implementation

The toolkit overview has broad wording about authenticating to follow procedures, while the targeted setup guide explicitly supports credential-free documentation and discovery for the Codex plugin. Use the targeted setup contract and a scoped public verification, rather than interpreting general prose as a requirement to access an account. [Overview](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/) · [Setup](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/quick-start.html)

The IAM guide also says preview-era `aws-mcp:InvokeMcp`, `aws-mcp:CallReadOnlyTool`, and `aws-mcp:CallReadWriteTool` actions no longer have effect. Older demo or configuration examples must be compared with current IAM guidance before reuse. [IAM guide](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/security_iam_service-with-iam.html)

## 3. Proposed access levels for this repository

These are design categories, not AWS product modes or configured permissions.

| Level | Permitted purpose after appropriate task authorization | Required evidence / boundary |
| --- | --- | --- |
| Public consultation | Public sources, requirements, repository planning | No account metadata, credentials, resource calls, or provisioning |
| Repository work | Authorized source/IaC edits and relevant local checks | Explicit command classification; isolate tests that could reach AWS |
| Account assessment | Inspect named environments/resources | Scoped temporary identity, defined data scope, sanitized observations; reads may still expose sensitive data or incur query charges |
| Cloud preview | Evaluate a concrete change in a named target | Required lookup/change-set/asset permissions, preview identity, source/configuration revision, time, and target |
| Deployment | Execute the authorized release | Exact source, configuration, target and scope; applicable artifact/preview identities with justified N/A; cost/recovery conditions and actual execution result |
| Operational response | Observe, mitigate, restore, or remove scoped resources | Separate inspection and mutation scope; verify recovery or cleanup rather than inferring it from a command exit |

Existing authorization persists for routine work within scope. The process should prepare useful evidence without repeatedly asking for the same permission. A material target, permissions, spend, or destructive-effect change must be evaluated against the actual authorization and platform controls. This scaffold does not configure these levels.

## 4. Greenfield entry and brownfield adoption

### Greenfield

Start with the problem, users, data, constraints, recovery needs, and budget assumptions. Select services, IaC, environment boundaries, and delivery mechanism after comparing appropriate options. The repository can then create specifications, implementation tasks, checks, and runbooks around those accepted choices. There is no universal requirement to use EKS, Lambda, a particular database, or a particular pipeline.

### Brownfield

Begin with an authorized repository inventory: application entry points, dependencies, IaC, state/backend configuration, stack ownership, pipeline definitions, artifact registry references, environment mapping, and existing tests/runbooks. Record three separate views:

1. **Declared:** what repository configuration says should exist.
2. **Recorded:** what prior deployment or operational evidence says happened.
3. **Observed:** what a currently authorized account assessment actually establishes.

Do not convert “no live access” into “no drift.” CloudFormation drift detection covers supported resources and explicitly set properties; unsupported resources and other exclusions require an honest coverage statement. A completed drift check is not proof that every behavior or property matches. [Drift documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html)

CloudFormation import validates existence, schema, required properties, and ownership constraints, but does not establish that the template matches live resource properties. Therefore importing existing resources, changing state ownership, or renaming resource identities must be scoped as migration work with configuration comparison and recovery evidence. Adding this scaffold should not silently perform that migration. [Resource import](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/import-resources-manually.html)

Use existing locations and interfaces where they remain appropriate. A brownfield adoption should first prove that the process can describe and verify a small existing behavior without replacing the application’s architecture or delivery system. See [brownfield adoption](../../guide/05-brownfield-adoption.md).

## 5. From deployment demonstration to release evidence

The following requirements are this repository’s proposed engineering controls. The demos above do not claim or prove that these controls were satisfied.

### Preview scope

CDK synthesis may execute project code and perform account context lookups. Current CDK diff can create a CloudFormation change set and use deployment permissions; a template comparison has different capabilities and accuracy. Record which path ran. Do not equate the word “preview” with zero account access or zero side effects. [CDK context](https://docs.aws.amazon.com/cdk/v2/guide/context.html) · [CDK diff](https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-diff.html)

CloudFormation change sets describe proposed resource changes, but do not guarantee execution success. Review replacements/deletions and migration effects before release, then observe the actual result. [Change sets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html)

### Test scope

Local tests and emulators are useful for fast feedback. They cannot establish complete parity for cloud IAM, service integrations, quotas, and runtime settings. SAM local can still make SDK calls to real AWS dependencies. Keep local logic evidence distinct from authorized cloud integration evidence. [AWS testing guide](https://docs.aws.amazon.com/lambda/latest/dg/testing-guide.html)

### Cost and recovery scope

Track standing cost, usage sensitivity, experiments, and cleanup. Brownfield estimates also need retained/shared costs and temporary migration overlap. AWS Budgets can notify after charges have accrued, so a budget notification is not an immediate spending cap. [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)

Kiro file checkpoints track built-in file edits and exclude changes made through shell or MCP tools. They cannot restore an AWS environment or reverse database/external effects. Recovery requires the workload’s own tested procedure and compatible artifact/configuration/data state. [Kiro checkpoints](https://kiro.dev/docs/checkpoints/)

Bind the release to the full source commit, immutable built artifact, configuration source, target, and reviewed preview identity. Capture deployment and user-visible verification results. See [delivery](../../delivery/README.md), [deployment](../../runbooks/deploy.md), and [rollback](../../runbooks/rollback.md).

## 6. Proposed acceptance metrics

These are **proposed targets**, not implemented controls, measured results, or a claim of outperforming Kiro. They make the desired improvement over an ad hoc prompt-and-deploy process measurable. A future evaluation must compare equivalent workloads and disclose the baseline, agent/tool versions, allowed access, and costs.

| ID | Metric and proposed acceptance target | Evidence / evaluation method |
| --- | --- | --- |
| AWS-E01 | Every release has complete source, configuration and target identity, plus applicable artifact/preview identities or justified N/A | Validate required and applicable release fields; deliberately change one input and confirm stale evidence is rejected by the eventual validator; N/A cannot waive actual project gates |
| AWS-E02 | Every mandatory acceptance criterion links to relevant evidence or is explicitly incomplete | Trace specification → task → check → result; an unrun test never appears as passed |
| AWS-A01 | Zero operational AWS calls during public-consultation evaluation | Inspect the recorded tool-call sequence; first evaluate with mocks and no account credentials |
| AWS-A02 | Every proposed cloud operation has target, access/side-effect classification, and applicable authorization | Evaluate read, preview, deploy, rollback, and teardown cases; include an ambiguous-account case that must remain unresolved |
| AWS-B01 | Zero unapproved resource replacements, imports, ownership transfers, or duplicate deployment triggers during brownfield adoption | Review the adoption diff and planned resource/pipeline effects against the migration scope |
| AWS-B02 | Every drift report states observed coverage, excluded/unsupported items, and observation time | Evaluate partial, failed, and unsupported-resource fixtures; none may be reported as comprehensive “no drift” |
| AWS-C01 | Every proposed billable resource/category has a regional dated price source, usage assumption, or explicit unknown | Review the estimate, including idle, network, observability, backup, CI, retained resources, and migration overlap |
| AWS-C02 | Every authorized experiment has agreed duration, resource constraints, cleanup owner, and post-cleanup evidence | Verify the experiment record and eventual inventory check; budget alerts alone do not satisfy this target |
| AWS-C03 | Forecast-versus-observed cost error is reported over an agreed stable window | Record absolute/relative variance and explanation; set a tolerance after baseline data exists rather than inventing a universal percentage |
| AWS-R01 | Each release with material stateful impact has a compatible recovery decision and a documented validation status | Check artifact/schema compatibility and restore prerequisites; measure recovery time/data loss against project-defined objectives in an authorized drill |
| AWS-R02 | Interrupted work resumes without blindly repeating external effects | Use simulated partial deployment/timeout scenarios; reconcile operation state and artifact identity before retry |
| AWS-R03 | Deployment completion includes actual service evidence and ownership of remaining work | Capture terminal execution result, critical journey, telemetry/observation window, migration outcome, and unresolved limitations |

Start with repository fixtures and simulated adapters. Any live AWS evaluation requires separately authorized scope and cost limits. Multi-agent review depth should be proportional to the task; measure useful evidence and defect detection as well as model usage and elapsed time. Faster output with weaker verification is not a successful result for this design.

## 7. Remaining uncertainties and implementation decisions

- Video narration, screen details, exact commands, and full outcomes were not verified from a transcript or watched recording. Revisit the linked primary videos if those details are needed.
- Local Codex/cloud plugin versions, available capabilities, credentials, and enforcement settings are not established by this research.
- Kiro features vary across client versions and surfaces. No file in this repository automatically creates Kiro’s runtime or UI in Codex.
- No application architecture, IaC framework, account topology, pipeline, budget amount, recovery objective, or production target is selected by the scaffold.
- Serverless diagnostic helpers depend on supported resources, permissions, and available telemetry. Their documented existence does not prove they are available in the selected connection or sufficient for every workload.
- The proposed metrics need implementable validators, fixtures, failure cases, and later authorized operational trials. Their completion belongs in [the foundation task list](../../specs/0001-workflow-foundation/tasks.md).

## 8. Decisions carried into the scaffold

Use public guidance first; keep the official toolkit identity; discover only relevant guidance; classify AWS access explicitly; preserve existing state and delivery ownership for brownfield work; make release identity and verification evidence concrete; distinguish workspace recovery from workload recovery; and report capability/version/test gaps honestly.

The repository should bootstrap disciplined work immediately through documented procedures, while labeling unimplemented orchestration and adapters as planned. That is the reviewable bridge from Kiro’s documented lifecycle to a Codex-driven AWS workflow.

