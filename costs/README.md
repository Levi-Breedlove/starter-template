# Costs

Keep cost assumptions visible from consultation through operation. Start with [estimate-template.md](estimate-template.md), then maintain a project-specific estimate when the architecture is selected.

## What this area owns

- Regional price sources and their review dates.
- Standing cost, usage-sensitive cost, and development/test cost.
- Expected, low, and high usage scenarios with explicit assumptions.
- Project limits for experiments, deployment, retention, and cleanup.
- Authorized measured spend compared with the estimate after deployment.

Architecture and service decisions belong in `specs/<work-id>/design.md` and [decision records](../docs/decisions/). Link them here instead of maintaining a second architecture description. Put compact sanitized observations in `evidence/<work-id>/` and link the relevant release under `delivery/releases/`.

## Working rules

Use current public AWS pricing and a stated region for estimates. Include relevant storage, requests, data transfer, logging, backups, build minutes, and idle infrastructure. Mark excluded costs and uncertainty. Do not invent account IDs, credits, discounts, free-tier eligibility, prices, or approved budget amounts.

For greenfield work, estimate the whole proposed environment. For brownfield work, identify the existing baseline, proposed increment, retained/shared resources, and temporary overlap during migration. Do not attribute all shared-resource cost to one change or assume decommissioned resources stop billing before cleanup is verified. If the live baseline is unavailable, label it unknown and estimate only the supported delta.

Separate estimated cost from actual account spend. Reading billing information requires explicit account authorization, even when the purpose is planning. A user-approved experiment limit should specify duration, resource size/count, and cleanup ownership as well as an amount.

AWS Budgets notifications may arrive after charges accrue. They are not a real-time spending cap. Use the project’s resource constraints, permissions, experiment limits, and verified cleanup to control exposure. The template creates no budgets, alarms, schedules, or billable resources.

## References

- [AWS Pricing Calculator](https://calculator.aws/)
- [AWS pricing](https://aws.amazon.com/pricing/)
- [AWS Budgets update and notification behavior](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)

