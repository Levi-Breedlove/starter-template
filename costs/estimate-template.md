# Cost estimate template

**Status:** Unpopulated. Values below are placeholders, not an approved budget or a price quote.

| Field | Value |
| --- | --- |
| Project / specification | `<project and spec reference>` |
| Adoption mode | `<greenfield or brownfield>` |
| Architecture decision | `<design or decision reference>` |
| Estimator / reviewer | `<owner>` / `<reviewer>` |
| Estimate date / currency | `<date>` / `<currency>` |
| AWS region(s) | `<approved or proposed regions>` |
| Environment(s) | `<development / test / production as applicable>` |
| Pricing source / calculator export | `<public URL or evidence reference>` |
| Approved operating budget | `<unset until explicitly agreed>` |
| Approved experiment scope | `<duration, resource limits, amount, and owner; unset>` |

## Usage assumptions

Describe request volume, concurrency, data size and growth, retention, availability target, traffic paths, build frequency, and environment uptime. Distinguish measured inputs from estimates. Explain the low, expected, and high scenarios.

| Service or cost category | Pricing unit and source date | Low usage / cost | Expected usage / cost | High usage / cost |
| --- | --- | --- | --- | --- |
| `<selected resource>` | `<unit, source, date>` | `<assumptions and amount>` | `<assumptions and amount>` | `<assumptions and amount>` |
| `<shared or supporting cost>` | `<unit, source, date>` | `<assumptions and amount>` | `<assumptions and amount>` | `<assumptions and amount>` |
| **Total** | `<period and currency>` | `<not calculated>` | `<not calculated>` | `<not calculated>` |

Include applicable network transfer, logs, backups, secrets, image/artifact storage, CI usage, and idle resources. List taxes, support, discounts, credits, or other exclusions explicitly.

## Existing workload and incremental change

Complete this section for brownfield work. For greenfield work, mark it not applicable.

| Item | Value |
| --- | --- |
| Existing baseline and evidence | `<documented estimate or authorized observed spend; otherwise unknown>` |
| Resources added or changed | `<identities/references, usage assumptions, and estimated delta>` |
| Retained/shared resources | `<ownership, allocation method, and continuing cost>` |
| Migration overlap | `<old/new environments, duration, transfer, and temporary cost>` |
| Proposed removals | `<scope, dependencies, and savings only after verified cleanup>` |
| Resulting total / confidence | `<baseline plus delta, or total unknown with supported delta>` |

## Decisions and controls

- Largest cost drivers: `<items and why>`.
- Cost/availability/performance tradeoffs: `<decision references>`.
- Resource constraints: `<allowed sizes, counts, concurrency, retention>`.
- Experiment expiry and cleanup owner: `<scope, time, owner>`.
- Notification thresholds and recipients: `<proposed; not created>`.
- Response to an exceeded limit: `<authorized action and escalation>`.
- Remaining uncertainty: `<unknowns and how to resolve them>`.

## After authorized deployment

Record the observation window, billing evidence reference, estimate-versus-actual difference, explanation, and follow-up decision. Billing data can lag; label the observation’s completeness. Keep credentials and unnecessary sensitive billing details out of committed evidence.

See [cost guidance](README.md) for source and access rules.

