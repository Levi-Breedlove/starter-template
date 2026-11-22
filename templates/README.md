# Artifact templates

These are original project record formats for consultation, specification and delivery. Use only the records needed for the current work. The [workflow contract](../docs/reference/workflow-contract.md) explains route selection; the [tooling reference](../docs/reference/workflow-tooling.md) defines the parseable task and metadata format.

| Template | Purpose |
| --- | --- |
| [Project brief](project-brief.md) | Outcomes, known facts, answers, constraints, recommendations and unresolved decisions. |
| [Requirements](requirements.md) | Observable behavior, failure paths and acceptance criteria. |
| [Design](design.md) | Architecture, interfaces, data, tradeoffs and verification approach. |
| [Tasks](tasks.md) | Stable IDs, dependencies, contract/check links and the sole completion checklist. |
| [Bugfix](bugfix.md) | Faulty, expected and preserved behavior. |
| [Work metadata](work.json) | Versioned index of context, phase, reviews and evidence. Prefer CLI initialization. |
| [Decision](decision.md) | A consequential choice, its reason, alternatives and authority. |
| [Review](review.md) | Candidate-specific findings, scope and disposition. |
| [Release](release.md) | Candidate, target, applicable readiness evidence and observed outcome. |
| [Handoff](handoff.md) | Current work, evidence, uncertainty and next eligible action. |
| [Environment capabilities](environment-capabilities.md) | Available, installed, loaded and tested capabilities. |
| [Brownfield assessment](brownfield-assessment.md) | Existing authority, baseline, ownership and preservation obligations. |

Templates are starting points, not completed decisions. Replace placeholders with known facts, explicit assumptions or unanswered questions. Do not invent a full architecture to fill a section. Save answers in the existing canonical brief/contract and point metadata back to them.

A normal feature follows its selected artifact order; quick work produces the connected documents together after clarification. A bugfix retains preservation obligations. A plan or small edit may use a smaller record. Reviews document actual decisions, and evidence documents actual observations; neither creates new authority.
