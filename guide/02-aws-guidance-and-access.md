# AWS guidance and access

**Status:** Planning guidance. This scaffold does not configure credentials, install plugins, inspect an AWS account, or authorize deployment.

Use official **AWS Core** for AWS guidance; use **AWS Data Analytics** when the workload needs its specialized capabilities. Reuse an existing official installation. Keep one installation per official plugin identity in each intended surface. Verify local Codex and Codex cloud separately: an installation or successful call in one does not establish the other’s state.

Begin with [start here](01-start-here.md), record the workload in [the project brief](../project/brief.md), and record surface evidence using [the environment capabilities template](../templates/environment-capabilities.md). For an existing workload, also follow [brownfield adoption](05-brownfield-adoption.md). This guide defines the AWS adapter boundary within the repository’s development workflow.

## Start with public consultation

Honor the task's skill preferences. For documentation-only research or a skill opt-out, use current official documentation directly and skip skill discovery and retrieval in steps 2–4. Those steps apply only when skill use is allowed.

1. State the workload question, accepted decisions, constraints, and desired evidence. For brownfield work, inspect authorized repository artifacts first and distinguish recorded architecture from verified live state.
2. Use AWS Core `search_documentation` with `topics: ["agent_skills"]` and a task-specific `search_phrase`.
3. Copy a returned `skill_name` exactly into `retrieve_skill`. It is an opaque registry identifier; do not derive it from a display title.
4. Retrieve a reference only when needed, using its exact returned path. Load additional skills only when the task requires them.
5. Check material guidance against current official AWS documentation and the official toolkit repository. Record the source, review date, and any difference between hosted guidance and upstream documentation.
6. Label findings as verified, assumed, recommended, or unresolved. Catalogue search is non-exhaustive; a missing search result alone does not prove a skill is unavailable.

Documentation search and skill discovery can work without AWS credentials. A skill’s instructions do not grant authority to call account APIs. Keep any account-dependent examples in a skill as reference until the relevant operation is authorized.

## Verify the execution surface

The local `workflow.py doctor` inspection helps establish package and project
setup. It intentionally leaves AWS plugin availability/loading/testing unresolved:
it does not invoke a plugin manager, inspect credentials or issue an AWS request.
Perform the public capability check below in the actual Codex surface that will
provide guidance. A native batch runner's configured model process and tool access
also need their own observed environment record; a source file or executable name
does not establish that configuration.

Record these separately in the project’s setup evidence under `evidence/<work-id>/`:

| State | Evidence |
| --- | --- |
| Available | The selected surface exposes the official capability |
| Installed | Its plugin manager reports the official identity installed |
| Loaded | The current session exposes the needed tools or skill |
| Tested | A recorded public documentation/skill call succeeds |
| Version | Reported version or revision; otherwise **unresolved** |

If a selected Codex surface lacks the official plugin, consult the [official Codex setup instructions](https://github.com/aws/agent-toolkit-for-aws#codex). The documented marketplace entry is `aws/agent-toolkit-for-aws`; installation is a separate setup task. Update existing official plugins in place through supported releases. Do not replace them with copied standalone AWS skills, private forks, local-folder plugins, or duplicate connections. Report unavailable hosted updates honestly.

## Match access to the activity

| Activity | Boundary |
| --- | --- |
| Public consultation | No account, credential, or resource access |
| Repository implementation | Authorized code, IaC, documentation, and local checks |
| Account assessment | Explicit task authorization naming environment and inspection scope; a narrow read role |
| Cloud preview | Explicit account scope; may create change-set metadata, perform lookups, or publish assets |
| Deployment | Authorized target, release identity, permissions, cost limits, and recovery procedure |
| Production verification | Authorized observations and synthetic transactions, with their data effects specified |

Routine reversible work continues under existing authorization. Do not repeatedly request approval for the same scope. Prepare the concrete release evidence before a required release decision; ask again when scope materially changes or a real control requires it.

Use temporary, narrowly scoped AWS identities. Agent instructions are behavioral guidance; IAM, environment permissions, and the delivery system enforce access. Never place credentials in prompts, specifications, logs, or source control. See [security](../security/README.md) and [delivery](../delivery/README.md), then continue with [the first feature](03-first-feature.md) and [maintenance and release](04-maintain-and-release.md).

## References

- [Agent Toolkit for AWS](https://github.com/aws/agent-toolkit-for-aws)
- [Toolkit getting started](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/quick-start.html)
- [AWS MCP and IAM](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/security_iam_service-with-iam.html)
- [CDK context lookups](https://docs.aws.amazon.com/cdk/v2/guide/context.html)

