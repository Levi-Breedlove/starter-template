# AWS Starter Template

**From idea to verified implementation.**

A reusable engineering framework for building AWS applications with Codex through guided consultation, structured specifications and evidence-driven development.

## What is AWS Starter Template?

AWS Starter Template helps developers turn an idea or an existing application into an organized, well-defined engineering project.

Codex acts as your engineering consultant, helping you establish requirements, recommend architecture, consider security and costs, and translate decisions into actionable implementation tasks.

Rather than starting with a predetermined architecture, your project takes shape through conversation.

## Why use it?

- **Build with direction:** Establish what you want to build before implementing it.
- **Stay organized:** Maintain consistent project documentation, specifications and repository conventions.
- **Preserve context:** Save decisions and continue development across sessions.
- **Follow AWS best practices:** Research relevant official AWS guidance throughout development.
- **Develop securely:** Consider security, permissions, costs and reliability from the beginning.
- **Verify your work:** Connect requirements and implementation tasks to meaningful tests and evidence.

The framework supports both new projects and existing applications without imposing a particular technology stack.

## Getting started

### Prerequisites

- Git
- Python 3.10 or newer
- A configured Codex client

### Start a new project

1. Select **Use this template → Create a new repository**.
2. Leave **Include all branches** unchecked.
3. Open your new repository in GitHub Codespaces.
4. Open Codex at the repository root.
5. Enter:

   ```text
   start
   ```

Codex will inspect the project and begin your consultation. Describe what you want to build, and work through the recommendations together.

Your requirements, architecture, decisions and tasks will be recorded directly in your repository.

Use `resume` to continue your work or `status` to review progress.

## Project structure

```yaml
.
├── .aws-workflow/                    # Reusable engineering framework
├── costs/                            # Cost estimates and budgets
├── delivery/
│   ├── current-handoff.md            # Progress and next steps
│   └── environment-capabilities.md   # Environment and tooling
├── docs/
│   ├── decisions/                    # Architecture decision records
│   └── diagrams/                     # Technical diagrams
├── evidence/
│   └── 0001-booking-retries/         # Example verification evidence
│       └── same-key-retry.md
├── infrastructure/                   # Infrastructure as code
├── project/
│   ├── adoption-report.md            # Existing project assessment
│   ├── architecture.md               # System architecture
│   ├── brief.md                      # Product vision and scope
│   ├── requirements.md               # System-wide requirements
│   ├── structure.md                  # Repository conventions
│   └── tech.md                       # Technology standards
├── runbooks/                         # Operational procedures
├── security/                         # Security planning and controls
├── specs/
│   └── 0001-booking-retries/         # Example feature specification
│       ├── requirements.md           # Expected behavior
│       ├── design.md                 # Technical solution
│       ├── tasks.md                  # Implementation checklist
│       ├── analysis.json             # Requirements analysis
│       ├── properties.json           # Correctness properties
│       ├── work.json                 # Context and traceability
│       └── execution.json            # Optional execution policy
├── src/                              # Application source code
├── tests/                            # Application tests
├── AGENTS.md                         # Agent instructions
└── README.md                         # Project introduction
```

Project foundations define the application. Specifications organize implementation, while tests and evidence establish whether requirements are satisfied.

The booking specification and evidence are illustrative examples of how the repository grows during development. New projects begin with empty specification and evidence directories.

[Repository conventions](project/structure.md) · [First-feature guide](.aws-workflow/guide/03-first-feature.md)

## Learn more

- [Getting started](.aws-workflow/guide/00-quickstart.md)
- [AWS Agent Toolkit setup](.aws-workflow/guide/02-aws-guidance-and-access.md)
- [Developing your first feature](.aws-workflow/guide/03-first-feature.md)
- [Adopting an existing application](.aws-workflow/guide/05-brownfield-adoption.md)
- [Repository conventions](project/structure.md)
- [Optional AWS Emulator](.aws-workflow/guide/08-aws-emulator.md)

AWS account access and deployment require separate authorization. Local consultation and development can begin without AWS credentials.
