# AWS guidance and access

**Status:** Planning guidance. This scaffold does not configure credentials, install plugins, inspect an AWS account, or authorize deployment.

Use **AWS Core** for general guidance and skill discovery. Use the other relevant official Agent Toolkit for AWS plugins when the chosen Codex surface provides them. Reuse existing installations, with one installation per official plugin identity on each surface. Record observations for local Codex and Codex cloud separately.

Begin with [start here](01-start-here.md), record the workload in [the project brief](../../project/brief.md), and record surface evidence using [the environment capabilities template](../templates/environment-capabilities.md). For an existing workload, also follow [brownfield adoption](05-brownfield-adoption.md). This guide defines the AWS adapter boundary within the repository’s development workflow.

## Start with public consultation

Honor the task's skill preferences. For documentation-only research or a skill opt-out, use current official documentation directly and skip skill discovery and retrieval in steps 2–4. Those steps apply only when skill use is allowed.

1. State the workload question, accepted decisions, constraints, and desired evidence. For brownfield work, inspect authorized repository artifacts first and distinguish recorded architecture from verified live state.
2. Use AWS Core `search_documentation` with `topics: ["agent_skills"]` and a task-specific `search_phrase`.
3. Copy a returned `skill_name` exactly into `retrieve_skill`. It is an opaque registry identifier; do not derive it from a display title.
4. Retrieve a reference only when needed, using its exact returned path. Load additional skills only when the task requires them.
5. Check material guidance against current official AWS documentation and the official toolkit repository. Record the source, review date, and any difference between hosted guidance and upstream documentation.
6. Label findings as verified, assumed, recommended, or unresolved. Catalogue search is non-exhaustive; a missing search result alone does not prove a skill is unavailable.

Use relevant guidance during consultation, architecture and cost planning, implementation and local tests, security and networking review, delivery planning, and operations. Follow public documentation links directly when an official connector is unavailable. Record actionable guidance in the relevant project foundation or work specification with its source. A later applicability change calls for a new check of the affected guidance.

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

## Use the official catalog in Codex and Codespaces

In the Codespaces terminal, run `codex plugin marketplace list` and inspect
`/plugins` in Codex. Hosted and IDE surfaces can expose the official integrations
through their own plugin manager. Reuse an installed official identity on that
surface. When the AWS marketplace is missing and setup is authorized, run
`codex plugin marketplace add aws/agent-toolkit-for-aws`. Choose the needed
official entry in `/plugins` and follow the client's existing permission controls.
On a supported CLI, `codex plugin marketplace upgrade agent-toolkit-for-aws`
refreshes that marketplace's published snapshot. Use the client's supported
update action for the installed plugin and verify its reported version and
needed capability after the update.
[Official Codex setup](https://github.com/aws/agent-toolkit-for-aws#codex)

Discover relevant plugins from the current official Codex marketplace manifest.
It includes general AWS guidance, analytics, agent development, security,
startup advice and organizational context. Record the exact identity and
operation selected. Only load the skills and references needed for the work.
[Current official plugin catalog](https://github.com/aws/agent-toolkit-for-aws/blob/main/.agents/plugins/marketplace.json)

Classify **each operation** before using it. Documentation search, public
documentation reads and skill retrieval can support credential-free work even
when the same plugin also exposes account APIs. A sign-in requirement during
installation or tool use is a separate capability observation. If sign-in is
required, defer that action until authorized cloud integration or delivery.
Continue with available public tools and official documentation. Account
inventory, access to private organizational knowledge, signed URLs, remote
scripts and deployment each need authority for the actual data or environment
involved. Keep private knowledge and account tools idle during public setup.
[AWS MCP knowledge and API tools](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/understanding-mcp-server-tools.html)

When local integration depends on AWS APIs, discover the emulator guidance the
same way and check the operations used by the workload. [Optional local testing](08-aws-emulator.md)

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

