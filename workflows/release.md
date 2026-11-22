# Release

## Trigger

Use this procedure to prepare a verified candidate for deployment or to execute an already authorized release. Preparation and AWS execution are distinct stages; a request to draft a plan does not authorize account access.

Apply the selected project's delivery controls to the actual release. Record an explicit reason and supporting evidence for any artifact, preview, or review marked **not applicable**. This cannot waive a required project gate, review, or acceptance check. Exact source, configuration, target, and authorization remain required, along with meaningful verification of an executed release.

## Inputs

- Candidate source revision and, when the release includes a built artifact, its immutable version or image digest.
- Accepted requirements, applicable verification and review evidence, and remaining limitations.
- Target environment, account/region scope, accepted execution path, and deployment roles.
- Environment-specific infrastructure/configuration changes, cost assumptions, and recovery/runbook links.
- The actual release authorization and project limits, including spending and permitted operations.

## Stages

1. **Assemble readiness.** Confirm that the candidate matches the reviewed source and that required checks apply to it. Identify migrations, replacements/deletions, availability risks, IAM/network changes, and operational dependencies. Use official AWS guidance through the existing plugins as needed.
2. **Prepare a reviewable release package.** Record the target, intended changes, cost implications, validation, rollout, recovery method, and abort criteria in `delivery/releases/<release-id>.md`. Prepare the runbook and evidence links before seeking any missing final authorization.
3. **Review the applicable target-specific plan.** When infrastructure changes or project controls require a preview, use the project's existing infrastructure and delivery tooling to produce and review it under authorized access. Otherwise record why a preview does not apply. Treat authenticated previews appropriately: a change-set or backend-backed plan may write state or perform service work. A local template check is not the same as a reviewed live-environment change plan.
4. **Confirm authority.** Reuse an existing authorization that covers this release. If scope, cost, or consequential operations fall outside it, present the concrete release package and ask only for that missing decision. Do not infer authority from an installed plugin, skill, document, or successful sign-in.
5. **Deploy through the accepted path.** For greenfield work, use the delivery design selected for this project. For brownfield work, preserve its established pipeline and infrastructure ownership unless an accepted decision changes them; this includes CodePipeline/CodeBuild where that is the existing path. Deploy the reviewed source revision and any applicable immutable artifact, with separately reviewed environment configuration and infrastructure changes. When promoting a built artifact, use the same reviewed artifact. Record the execution/run and applicable artifact identities; do not claim that staging and production necessarily use identical templates.
6. **Verify service behavior.** Observe deployment completion, then run the agreed application, security, health, and operational checks in the target environment. Compare the result with abort/recovery criteria. Execute recovery only within its authorized scope and verify its outcome.
7. **Close or hand off.** Record what is ready, deployed, verified, failed, or still unobserved. Update runbooks, tasks, and the current handoff. Open scoped follow-up work for unresolved issues rather than treating them as a successful release.

## Outputs

- A release record with reviewed revision, applicable artifact and preview identities, target configuration, authorization, run links, verification, and recovery outcome when applicable; justified not-applicable entries remain visible.
- Updated operating guidance and lightweight evidence links.
- A precise status report distinguishing readiness from deployment and service verification.

## Completion evidence

For preparation: the package is concrete and all readiness claims have supporting evidence or visible limitations. For execution: the actual authorized deployment is observed and required target checks pass. An exit code, task checkbox, or generated URL alone does not establish healthy operation.

## Continue, pause, and resume

Continue all authorized preparation and execution within stated limits. Pause before an unapproved account operation, new paid execution, or materially changed release scope. If blocked, preserve the exact candidate, package, observed state, and smallest next action. On resume, reassess environment drift and evidence freshness before deployment.

## Related reference

[Kiro environment configuration](https://kiro.dev/docs/web/sandbox/environment-configuration/) describes a Kiro-specific IAM-role integration. It does not establish Codex authentication, permissions, or deployment parity. AWS implementation details belong in current official guidance, not copied into this contract.
