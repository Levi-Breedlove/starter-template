# Repository structure

Use this foundation to record where work belongs, who owns each component and
which conventions the project has accepted. Preserve established brownfield
paths, tooling and ownership. Consult `.aws-workflow/manifest.json` for mapped
records when their locations differ from the template defaults.

## Components and ownership

| Default location | What belongs here |
| --- | --- |
| `project/` | Shared brief, system requirements, technology, structure and architecture decisions that guide work across features. |
| `src/` and `tests/` | Application components and their verification. Follow the layout expected by the language, framework and test runner. |
| `infrastructure/` and `security/` | Infrastructure as code and environment ownership, plus security boundaries, controls and review responsibilities. |
| `costs/` and `runbooks/` | Cost assumptions, estimates and controls, plus operational, incident and recovery procedures. |
| `docs/decisions/` and `docs/diagrams/` | Architecture decision records and diagrams. Reference these from the relevant foundation or specification. |
| `specs/<work-id>/` | Scoped requirements or defect contract, design, tasks and workflow records. |
| `evidence/` and `delivery/` | Verification receipts, and the current handoff, release and recovery records that refer to them. |
| `.aws-workflow/` | Installed workflow, reusable guidance and manifest. |

## Layout and naming conventions

For new project-owned directories and ordinary Markdown files, prefer lowercase
kebab-case, such as `booking-api/` and `retry-policy.md`. Keep conventional root
filenames `README.md`, `AGENTS.md`, `CHANGELOG.md`, `CONTRIBUTING.md` and
`SECURITY.md`. Name source files, tests and symbols according to the language
and tools selected for the application.

The structured CLI requires a work ID of 1 to 80 characters. Start with a
lowercase ASCII letter or digit, then use lowercase ASCII letters, digits or
hyphens. A numbered descriptive ID such as `0001-booking-retries` is a useful
default. The ID in `work.json` must match its directory under `specs/`.
Artifact paths in that record are relative to the work directory. Usual names
are `requirements.md` (or `bugfix.md`), `design.md` and `tasks.md`. Recorded
analysis and correctness properties use `analysis.json` and `properties.json`.

Keep identifiers stable within each specification. For example, trace
`REQ-001` to design `DES-001`, correctness property `PROP-001`, task `T-001`
and check `CHK-001`. These identifiers use their uppercase prefix and at least
three digits. Across specifications, cite the work ID or artifact path together
with the identifier, such as `specs/0001-booking-retries/tasks.md` and `T-001`.
For a check receipt under `evidence/<work-id>/`, identify the candidate, check,
method, environment, observation time, inputs and actual result.

## Project decisions and exceptions

Record the actual owner, path and any local exception as decisions are agreed.
Link to the existing decision or tool configuration when it owns the rule.
For a new versioned public interface, consider Semantic Versioning (SemVer).
Its `MAJOR.MINOR.PATCH` components signal incompatible changes, backward-compatible features
and backward-compatible fixes, respectively. Record the project's accepted
release policy and tag convention here or reference its existing release guide.
