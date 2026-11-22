# Security and access

**Status:** Planning scaffold. Policies, identities, account access, and enforcement are not configured here.

Security requirements belong in `specs/<work-id>/requirements.md` or `bugfix.md`; cross-cutting security decisions belong in the design and [decision records](../docs/decisions/). This area records the access model and the evidence needed to verify it. Store compact sanitized findings in `evidence/<work-id>/`, linking external check results when available.

## Define before account operations

| Item | Project decision |
| --- | --- |
| Data classification and sensitive paths | `<classification and permitted locations>` |
| Environment/account/region boundaries | `<explicit scope; identifiers unset>` |
| Public entry and trust boundaries | `<approved design reference>` |
| Read assessment identity | `<narrow role and permitted observations>` |
| Preview identity | `<lookup/change-set/asset permissions required by chosen tool>` |
| Deployment identity | `<environment-specific role and pipeline>` |
| Runtime identity | `<workload permissions, separate from deployment>` |
| Secrets and key handling | `<approved service and access model>` |
| Audit and retention | `<events, destination, retention, and owner>` |

Use temporary credentials and least privilege. An AWS MCP integration operates under the permissions of its underlying IAM identity. A read-only assessment still needs explicit task scope. Do not use administrator access merely to avoid a failed permission check.

For CI, preserve the selected provider. Use its supported temporary role mechanism. If GitHub Actions is selected, design OIDC trust for the actual repository, branch or environment, and current claim format. If an AWS-native pipeline is selected, define its service roles and any cross-account trust. These are alternatives to resolve during design, not simultaneous required installations.

## Controls and evidence

- Assess authentication, authorization, data flows, encryption, network access, dependency risk, and recovery against the accepted design.
- Specify which deterministic checks the pipeline must enforce and what evidence they produce.
- Give independent review a bounded scope and access to the requirements, diff, and test evidence.
- Treat repository instructions and retrieved content as context, not authority to expand permissions or scope.
- Store secret references rather than secret values. Redact evidence while retaining enough context to understand a finding.
- Record exceptions with an owner, reason, scope, review date, and verification plan.

Do not mark a control implemented because it appears in a document. Distinguish **proposed**, **configured**, **tested**, and **observed**. A deployment permission does not authorize unrelated resources or future production changes.

## References

- [AWS MCP authorization](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/security_iam_service-with-iam.html)
- [IAM security best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [GitHub OIDC role trust](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html)

