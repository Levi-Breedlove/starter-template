# AWS project starter

Open Codex at the root of this repository and type **`start`**. Your AWS consultant will inspect the project, ask what you want to build, and save the decisions you make together. On your next visit, `start` or `resume` picks up from the handoff.

## First use in GitHub Codespaces

1. In the template repository, choose **Use this template → Create a new repository**. Leave **Include all branches** clear to copy the application skeleton. Select private visibility for private work.
2. In your new repository, choose **Code → Codespaces** and open your development environment. Open your configured Codex client at the repository root. A supported setup has Git, Python 3.10 or newer and a Codex client with its existing permissions.
3. Type `start`. Describe the outcome and who needs it. Codex can research public AWS guidance, record the project foundations and propose the first feature. The project is already initialized.

The local workflow uses Python's standard library. Codespaces, Linux, macOS and WSL are supported development targets with these prerequisites. The optional native worker has separate client-state and executable requirements. Check the actual terminal before allocating a worker. [Codespaces setup](.aws-workflow/guide/07-codespaces.md) · [AWS toolkit setup](.aws-workflow/guide/02-aws-guidance-and-access.md) · [Optional AWS Emulator](.aws-workflow/guide/08-aws-emulator.md)

## Where work lives

| Location | Contents |
| --- | --- |
| `project/` | Product brief, system requirements, technology, repository structure, architecture and adoption assessment |
| `specs/` | Feature and defect contracts, design, correctness properties and dependency-ordered tasks |
| `docs/decisions/`, `docs/diagrams/` | Architecture decisions and diagrams when useful |
| `src/`, `tests/`, `infrastructure/` | Application code, verification and infrastructure as the project requires |
| `security/`, `costs/`, `runbooks/` | Threat and access decisions, cost controls and operating procedures |
| `delivery/`, `evidence/` | Handoff, capability observations, release preparation and actual check results |
| `.aws-workflow/` | Packaged instructions, guides, workflow engine and logical path mappings |

Use normal language or one of the seven conversational shortcuts. **start** begins or resumes consultation. **resume** continues eligible work. **status** reads progress. **feature** and **bugfix** start scoped changes. **review** examines actual work and evidence. **release** prepares verification, delivery and recovery. Cloud access, deployment and additional native calls require separate authority. [Project instructions](AGENTS.md) · [Current handoff](delivery/current-handoff.md)

## Existing application

Keep the template checkout separate from the application. Preview the installation from this checkout and inspect the mapped documents and existing task and infrastructure owners. Supply the same arguments with `--apply` to install the reviewed changes. Use `--help` for explicit mappings and upgrade options.

```sh
python3 .aws-workflow/scripts/bootstrap.py --source .aws-workflow --target ../existing-app --mode brownfield
```

The setup check can run before the first specification exists. The second command checks local documentation links and required files.

```sh
python3 .aws-workflow/scripts/workflow.py --root . doctor
python3 .aws-workflow/scripts/check_repository.py --root .
```

The local checks cover this checkout. Verify the application under its actual test and delivery controls. Public AWS documentation and compatible emulation can support development without a cloud account. Account-specific IAM, network behavior, quotas and deployment need separately authorized verification. [Updates and compatibility](CHANGELOG.md) · [Contributing](CONTRIBUTING.md) · [Security reporting](SECURITY.md)
