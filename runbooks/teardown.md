# Teardown runbook template

**Status:** Planned. No resource deletion is authorized by this template.

## Scope and preservation

| Field | Value |
| --- | --- |
| Target environment and owner | `<explicit target and owner>` |
| Inventory / infrastructure state | `<authoritative scope reference>` |
| Teardown authorization | `<decision covering the listed destructive actions>` |
| Data to retain/export | `<datasets, backups, retention rules, owners>` |
| Shared dependencies to preserve | `<identified dependencies>` |
| Expected remaining resources/cost | `<intentional retained items and estimate>` |

## Procedure

1. Review the actual inventory and IaC state within authorized access. Identify resources outside stack/state management, shared dependencies, retention policies, and deletion protection.
2. Prepare the exact deletion plan. Explain irrecoverable data loss, required exports/backups, and intentionally retained resources before the applicable decision.
3. Confirm required preservation completed and verify the target identity. Use `<reviewed teardown action>` only within the approved scope.
4. Observe failures and retained resources. Do not force deletion or disable protections beyond the authorization merely to make teardown appear successful.
5. Verify the resulting inventory, retained data, and remaining billable resources. Record evidence and owners for residual items.
6. Review later billing observations when authorized, acknowledging billing delay. A successful destroy command alone does not establish zero continuing cost.

Teardown of an experiment should be planned when that experiment is proposed. Any future scheduled cleanup needs explicit configuration, scope, and ownership; this scaffold creates none.

## References

- [CloudFormation deletion policies](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-attribute-deletionpolicy.html)
- [Cost evidence](../costs/README.md)

