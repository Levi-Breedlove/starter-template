# Brownfield intake

## Trigger

Use this procedure when adopting the workflow in an existing application, infrastructure repository, or service. Establish an evidence-based baseline and a bounded first change. Preserve the existing source layout, accepted architecture, IaC ownership, and delivery process.

## Inputs

- The repository and requested outcome, with any supplied architecture or operational evidence.
- Existing instructions, requirements, decisions, task authority, pipeline configuration, and runbooks.
- Available revisions, test/release results, and current handoff.
- Authorized inspection/change scope and known compatibility or data obligations.

## Stages

1. **Inventory without disturbing work.** Inspect the branch/revision, uncommitted changes, instructions, layout, applications, dependencies, tests, IaC, CI/CD, and operating documents. Record inaccessible areas. Preserve contributors' work; do not overwrite instructions or move files to match this skeleton.
2. **Separate evidence from intent.** Distinguish observed implementation, declared architecture, accepted decisions, the requested change, and unknown live state. Existing behavior is not automatically correct. Source code does not prove which version is deployed; an IaC declaration does not establish live ownership.
3. **Derive preservation obligations.** Inspect public contracts, consumers, data ownership/lifecycle, migration boundaries, authorization/networking expectations, and operations. Recommend the smallest change that satisfies the request. Research technical questions from official AWS guidance where needed, using the [public consultation boundary](../guide/02-aws-guidance-and-access.md).
4. **Interview only the remaining gaps.** Lead with the established facts and proposed approach. Ask one to three questions when conflicting intent, undocumented product policy, ownership, or material risk remains. Explain the consequence and suggest a resolution where supported. Do not ask which language, IaC tool, or pipeline to use when the repository already answers. Save each consequential answer and its evidence in the brief or work contract; link it from the adoption report.
5. **Identify infrastructure ownership and limits.** Inspect declared stacks/modules, state/backend references, pipeline responsibilities, environments, and ownership boundaries. Record what requires later authorized verification. Do not import resources, bootstrap an environment, move state, change ownership, or query an account during public/repository intake.
6. **Establish the verification baseline.** Inspect existing results and their revision/environment. Run permitted local checks when they resolve an actual uncertainty. Record pre-existing failures and characterization needs. Avoid treating mocks or repository declarations as proof of AWS behavior.
7. **Map and review incremental adoption.** In the project's adoption report, name the existing authoritative artifacts, useful workflow additions, unresolved decisions, and the first bounded work item. Review the proposed overlay against existing instructions and pipeline expectations. Record the actual outcome and authorization; routine documentation changes may already be covered. Avoid duplicate task authorities, blanket refactors, and copying all history into agent context.
8. **Select the next route.** Use Design-First for a change constrained by established design; Requirements-First for new behavior; Quick Spec for understood bounded scope; Plan-led for a small investigation; or [Bugfix](bugfix.md) for a defect. Carry the evidence and answers into [Consult](consult.md) or the chosen work procedure rather than restarting discovery.

## Outputs

- An adoption report with baseline identity, evidence, preservation obligations, ownership, uncertainty, adoption decisions, and the first work item.
- A project brief linking existing canonical artifacts and saved answers.
- A current handoff identifying the next action and any consequential question.

## Completion evidence

The report distinguishes observation, intent, recommendation, and unknown live state. Document/task authority is explicit. The first change has a bounded scope and verification path. Existing architecture, interfaces, data, state ownership, and delivery controls are preserved or have a separately recorded change decision.

## Continue, pause, and resume

Continue repository inspection, public research, and authorized documentation work. Pause dependent work only for inaccessible evidence, a consequential unresolved decision, account access, or spending outside existing authority. Explain the exact gap. On resume, compare the current revision with the saved baseline and use [Reconcile](reconcile.md) for material differences; reuse valid answers.
