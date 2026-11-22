# Official source ledger

**Research review date:** 2026-11-21 (America/Los_Angeles). Sources are public primary documentation or official demonstration material. Dates below are publication dates where verified, not assumed modification dates. Product details change; verify the relevant client and current source before implementation.

The ledger records source coverage, not test results. [Research synthesis](../research/README.md) separates documents, published visual transcripts, descriptions, proposed design, and actual local observations.

## Kiro documentation

| Source | Used to verify |
| --- | --- |
| [How Kiro works](https://kiro.dev/docs/how-kiro-works/) | Shared harness, context/tool/permission loop, surface boundaries. |
| [Your first project](https://kiro.dev/docs/getting-started/first-project/) | Project grounding, steering, spec/task workflow, demo/transcript links. |
| [Specs](https://kiro.dev/docs/specs/) | Specification artifacts, dependency execution, capability matrix. |
| [Feature Specs](https://kiro.dev/docs/specs/feature-specs/) | Feature structure and acceptance criteria. |
| [Requirements-First](https://kiro.dev/docs/specs/feature-specs/requirements-first/) | Behavior-led specification sequence. |
| [Design-First](https://kiro.dev/docs/specs/feature-specs/tech-design-first/) | Technical-design-led sequence. |
| [Quick Spec](https://kiro.dev/docs/specs/quick-spec/) | Upfront questions and reduced intermediate review stops. |
| [Bugfix Specs](https://kiro.dev/docs/specs/bugfix-specs/) | Incorrect, expected, and preserved behavior. |
| [Plan mode](https://kiro.dev/docs/specs/plan/) | Conversational planning and documented tool limits. |
| [Analyze Requirements](https://kiro.dev/docs/specs/analyze-requirements/) | Ambiguity/interaction analysis and supported spec types. |
| [Correctness](https://kiro.dev/docs/specs/correctness/) | Properties, requirement/task links, optionality and surface limits. |
| [Spec best practices](https://kiro.dev/docs/specs/best-practices/) | Updating requirements/design and synchronizing tasks. |
| [Steering](https://kiro.dev/docs/steering/) | Product/technology/structure guidance, scoped inclusion, AGENTS support. |
| [Hooks](https://kiro.dev/docs/hooks/) | Event-triggered automation overview. |
| [Hook types](https://kiro.dev/docs/hooks/types/) | Event-level semantics and surface/version support. |
| [Hook actions](https://kiro.dev/docs/hooks/actions/) | Command/prompt action behavior. |
| [Workflows](https://kiro.dev/docs/workflows/) | Runtime-managed isolated steps, handoffs, control flow. |
| [Workflow authoring](https://kiro.dev/docs/workflows/authoring/) | Recipe structure, nodes, conditions, waits, agent roles. |
| [Workflow examples](https://kiro.dev/docs/workflows/patterns/) | Review/correction patterns and PR feedback workflow. |
| [Workflow management](https://kiro.dev/docs/workflows/manage/) | Persisted progress, pause/stop/retry distinctions and limitations. |
| [Subagents](https://kiro.dev/docs/custom-agents/subagents/) | Delegated contexts and permission boundaries. |
| [Skills](https://kiro.dev/docs/skills/) | Reusable on-demand instructions; documentation only, no user skill invoked. |
| [Powers](https://kiro.dev/docs/powers/) | Bundled capability guidance and tools. |
| [MCP](https://kiro.dev/docs/mcp/) | External tool integration. |
| [Checkpoints](https://kiro.dev/docs/checkpoints/) | File recovery versus conversation forks and uncovered effects. |
| [Compaction](https://kiro.dev/docs/compaction/) | Long-session context management. |
| [Memory](https://kiro.dev/docs/memory/) | Persistent context mechanism distinct from work acceptance evidence. |
| [Working with the Web agent](https://kiro.dev/docs/web/using-the-agent/) | Cloud work and PR-oriented interaction. |
| [Web tasks](https://kiro.dev/docs/web/using-the-agent/creating-tasks/) | Task queue/lifecycle distinct from specification completion. |
| [Cloud configuration](https://kiro.dev/docs/web/cloud-configuration/) | Opt-in configuration transfer and local/cloud boundaries. |
| [Web environment configuration](https://kiro.dev/docs/web/sandbox/environment-configuration/) | Configured sandbox identity and AWS access. |
| [Crew Task Runner](https://kiro.dev/docs/crew/features/task-runner/) | Separate long-running execution mechanism and documented review/retry defaults. |

## Codex documentation

| Source | Used to verify |
| --- | --- |
| [Best practices](https://learn.chatgpt.com/guides/best-practices) | Repository guidance, planning and review practices. |
| [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | Project and scoped instructions. |
| [Build skills](https://learn.chatgpt.com/docs/build-skills) | Optional repository packaging boundary; no active skill package delivered. |
| [Hooks](https://learn.chatgpt.com/docs/hooks) | Supported events/handlers, trusted project configuration, duplicates and limitations. |
| [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Native delegation and surface availability. |
| [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode) | Exec events and structured output interface. |
| [Codex SDK](https://learn.chatgpt.com/docs/codex-sdk) | Supported programmatic thread execution/continuation. |
| [App Server](https://learn.chatgpt.com/docs/app-server) | Optional custom control interface and thread/turn events. |
| [Git worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees) | Workspace isolation for concurrent changes. |
| [GitHub integration](https://learn.chatgpt.com/docs/third-party/github) | Review integration distinct from a complete delivery controller. |
| [Scheduled tasks](https://learn.chatgpt.com/docs/automations) | Surface-specific background triggers; no schedule created. |

Read-only local CLI discovery identified `codex-cli 0.172.0-alpha.2` in the research environment. Help text is advertised capability, not a tested integration or an observation of the owner's desktop installation.

## AWS documentation

| Source | Used to verify |
| --- | --- |
| [Agent Toolkit for AWS repository](https://github.com/aws/agent-toolkit-for-aws) | Official supported repository, plugin identity, integration instructions. |
| [Toolkit guide](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/) | AWS knowledge and operations layer. |
| [Toolkit quick start](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/quick-start.html) | Codex setup and credential-free public guidance boundary. |
| [Toolkit skills](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/skills.html) | On-demand public discovery/retrieval procedure. |
| [MCP tool reference](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/understanding-mcp-server-tools.html) | Public tools versus account/data/operational tools. |
| [Toolkit capabilities](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/capabilities.html) | Supported investigation features and limitations. |
| [Toolkit IAM](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/security_iam_service-with-iam.html) | Downstream authorization, temporary credentials, current IAM guidance. |
| [CDK diff](https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-diff.html) | Preview modes and possible change-set/asset side effects. |
| [CDK context](https://docs.aws.amazon.com/cdk/v2/guide/context.html) | Context lookup and reproducibility considerations. |
| [CloudFormation change sets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html) | Preview versus execution success. |
| [CloudFormation drift](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html) | Resource/property coverage limits. |
| [CloudFormation resource import](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/import-resources-manually.html) | Import checks versus live-property equivalence. |
| [Lambda testing](https://docs.aws.amazon.com/lambda/latest/dg/testing-guide.html) | Local/mocked tests versus real cloud evidence. |
| [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html) | Delayed cost notifications rather than hard caps. |
| [IAM Identity Center credentials](https://docs.aws.amazon.com/sdkref/latest/guide/feature-sso-credentials.html) | Temporary identity option for later authorized use. |
| [Toolkit launch](https://aws.amazon.com/about-aws/whats-new/2026/05/agent-toolkit/) | Publication chronology: 2026-05-06. |

## Official video material

The seven items and exact access levels are in the [research inventory](../research/README.md). Two short official visual transcripts were read. Five additional official video descriptions/metadata listings were inspected. Full playback and full spoken transcripts for those five were not available in the retrieved material. Detailed workflow claims rely on written documentation rather than assumed footage.

## Freshness and conflicting evidence

Prefer the feature's specific event/schema/version reference over a broad marketing overview. A stale indexed Kiro Hooks overview differed from the clean current page during research; re-opening the clean page resolved the apparent Web availability disagreement. The event-level surface table remains the appropriate reference.

Older demo IAM or installation steps may predate current AWS guidance. Preserve official plugin identity, verify supported updates in the actual environment, and state unresolved release availability. Do not replace an unavailable hosted update with a private/local duplicate.

