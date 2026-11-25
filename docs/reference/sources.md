# Official source ledger

AWS toolkit and emulator entries reviewed on 2026-11-24. Earlier reference review on 2026-11-22. These sources support product integration and AWS operation boundaries. Repository workflow choices are the project's own design. Current files contain no third-party workflow comparison or copied prompt collection.

| Topic | Primary source | Use |
| --- | --- | --- |
| Codex project instructions | [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | Project instruction discovery and scope. |
| Codex native events | [Hooks](https://learn.chatgpt.com/docs/hooks) | Supported event/configuration shapes and client trust requirements. |
| Codex delegation | [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Supported delegation; repository roles do not themselves register agents. |
| Noninteractive execution | [Codex exec](https://learn.chatgpt.com/docs/non-interactive-mode) | Potential future bounded worker adapter. |
| SDK | [Codex SDK](https://learn.chatgpt.com/docs/codex-sdk) | Potential programmatic orchestration boundary. |
| Persistent client interface | [App Server](https://learn.chatgpt.com/docs/app-server) | Future option only if a persistent controller is needed. |
| AWS toolkit setup | [Quick start](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/quick-start.html) | Official agent integration and public-versus-credentialed use. |
| AWS toolkit source | [aws/agent-toolkit-for-aws](https://github.com/aws/agent-toolkit-for-aws) | Published official implementation and identity. |
| Guidance discovery | [Skills](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/skills.html) | Search and retrieve relevant official guidance when allowed. |
| AWS tool scope | [MCP tools](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/understanding-mcp-server-tools.html) | Public information versus operational actions. |
| Official Codex plugin identities | [Codex marketplace](https://github.com/aws/agent-toolkit-for-aws/blob/main/.agents/plugins/marketplace.json) | Discover the current official catalog and per-plugin manifest before selecting capabilities. |
| Local AWS integration | [Emulator compatibility](https://docs.aws.amazon.com/emulator/latest/userguide/check-project.html) · [security](https://docs.aws.amazon.com/emulator/latest/userguide/security.html) · [published releases](https://github.com/aws/aws-emulator/releases) | Match API behavior to fidelity evidence and isolate each local test job. |
| AWS permissions | [Toolkit IAM](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/security_iam_service-with-iam.html) | Actual service authorization. |
| CDK preview behavior | [cdk diff](https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-diff.html) | Method-dependent side effects. |
| Existing resources | [CloudFormation import](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/import-resources-manually.html) | Adoption validation limitations. |
| Deployed divergence | [CloudFormation drift](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html) | Coverage and observation limitations. |

Documentation review is not a live client test. Fixture results, actual client observations and eventual AWS outcomes are recorded separately under the relevant work item. No video-derived implementation claim is required by the current build; historical research delivery is retained only as a historical receipt.
