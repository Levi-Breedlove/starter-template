# Consult

## Trigger

Use this procedure to clarify a new project, a substantial change, or an uncertain architectural decision. Start in public-guidance mode unless the user separately authorizes account-specific discovery.

For a **greenfield** project, establish the first accepted product and AWS constraints before selecting services or generating implementation tasks. For a **brownfield** project, complete [Brownfield intake](brownfield.md) first and use its adoption report as the baseline.

## Inputs

- The user's goal, intended users, success measures, and known constraints.
- `project/brief.md`, accepted decisions, relevant specifications, and `delivery/current-handoff.md`.
- Existing repository structure and evidence, when available.
- Available budget, delivery window, and account/region/environment constraints; record unknowns rather than inventing values.

## Stages

1. **Ground the discussion.** In greenfield work, define users, product outcomes, data, expected load, availability, delivery, and operational constraints; record unknown values. In brownfield work, inspect the existing project and adoption report, separating implemented behavior, accepted plans, and unsupported assumptions. Identify functionality that should be reused.
2. **Clarify decisions that matter.** Ask about scope, data, reliability, security, cost, and operations only where an answer changes the recommendation. Batch related questions; do useful research before asking.
3. **Consult official AWS guidance.** When skill use is allowed, use the existing hosted Core/Data Analytics route: discover relevant skills through Core `search_documentation` using `agent_skills`, retrieve the exact returned IDs, and read needed references. For documentation-only research or a skill opt-out, use current official documentation directly. Check material claims against current official documentation. Record sources and gaps without querying AWS accounts.
4. **Compare feasible options.** Recommend an approach with its costs, operational burden, limitations, and alternatives. Select an architecture for the actual project instead of inheriting a previous project's stack. Preserve accepted architecture unless a specific change is proposed and justified. Include a cost model with explicit assumptions rather than a fabricated bill.
5. **Choose the work route.** Use Requirements-First for behavior-led work; Design-First for an established architecture; Quick Spec for familiar scoped work; Plan-led work for a lighter exploration-to-implementation handoff; [Bugfix](bugfix.md) for a defect.
6. **Capture the decision.** Update the brief and relevant decision/cost/security records. Present concrete scope and acceptance outcomes. Record accepted decisions separately from recommendations still awaiting a decision.

## Outputs

- An updated brief or scoped change proposal, with sources, assumptions, unresolved decisions, and boundaries.
- A selected route and work identifier; links to existing artifacts rather than copied versions.
- A clear next action for the feature or bugfix procedure.

## Completion evidence

The recommendation addresses the user's objective and identifies how success will be checked. Material uncertainties and decisions are visible. Cost assumptions are traceable. Claims of existing implementation refer to inspected evidence. No deployment or account verification is implied by the consultation.

## Continue, pause, and resume

Proceed into specification work when already authorized. Pause only for a decision that materially changes scope, cost, architecture, or permitted access; explain its consequence. Resume from the saved brief, decision record, and handoff rather than restarting consultation. Do not add a new approval step for each document.

## Reference

[Kiro project grounding](https://kiro.dev/docs/getting-started/first-project/) and [workflow selection](https://kiro.dev/docs/specs/feature-specs/) inform this procedure. The AWS consultation contract here is a repository recommendation, not a promise of native product behavior.
