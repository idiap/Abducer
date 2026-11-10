---
name: framework-paper-workflow-example-writer
description: Write a meaningful realistic example inside every in-scope workflow appendix subsection. Use a reviewed WorkflowExamplePlan and source-backed workflow models to explain concrete inputs, substantive reasoning, and an informative outcome, with optional categorical or dependent-type notation and a single final appendix owner.
---

# Framework Paper Workflow Example Writer

Help a reader understand what each workflow does by following a plausible problem through its distinctive reasoning. An example should teach something about the problem and the workflow. Passing checks, moving records, or collecting receipts is not an informative outcome.

## Inputs and ownership

Consume the reviewed `WorkflowExamplePlan` from `$framework-workflow-example-designer`, its frozen `PrismWorkflowAppendixSource`, any category or dependent-type models it references, the curated claim ledger, approved `PaperBlueprint`, and manuscript context. Read the [plan contract](../framework-workflow-example-designer/references/example-plan-contract.md) and the [example fragment contract](references/example-fragment-contract.md). Require exact matching source/model identities and digests. `input_digest` is the evidence-index digest inherited through the blueprint, distinct from a packet file hash.

The blueprint must identify one final appendix section owner: normally `$framework-paper-workflow-appendix-writer` for the categorical presentation or `$framework-paper-dependent-type-writer` for dependent typing. This skill supplies nested example fragments to that owner. It does **not** create a second `PaperSectionDraft`, compete for section ownership, or allocate a new CLI stage. This is a manual skill-orchestrated lane; manuscript integration requires the existing owner and assembler handoff.

Freeze scope from the complete source workflow inventory and the blueprint's documented scope decision. A request for every workflow means every workflow in that inventory unless the user has explicitly narrowed it. Existing manuscript subsections may be incomplete; do not infer the inventory solely from them. Match `scope_workflow_ids` exactly against the reviewed plan, with one coverage row per workflow. Missing, stale, unreviewed, or empty examples block an all-workflow completion claim; retain a diagnostic row rather than quietly reducing scope.

## Write each case

1. Begin with a concrete question or practical task and the consequence of getting it wrong. Name the case's evidential posture in reader-facing prose: an invented case is an **illustrative scenario**, not a reported run. For mixed cases, distinguish supplied observations from invented intermediate content and outcomes locally.
2. Supply enough input content for the reader to follow the reasoning: competing explanations, a short passage, numerical observations with units, an explicit constraint, or another domain-appropriate artifact. Choose details because a later decision uses them. Avoid anonymous `Candidate A` placeholders when the reader needs the underlying ideas.
3. Show the meaningful intermediate change and why it follows: a hypothesis revised by a contradiction, an ambiguity resolved using context, a proposed discriminating observation, or another transformation actually supported by this workflow. Preserve multi-input dependencies, partial order, branches, fallibility, and unresolved source gaps. Do not invent native steps to make the case satisfying.
4. End with a concrete product, conclusion, changed question, or useful limitation. Explain what the reader learned and why this is a representative instance of the workflow's defining mechanism. A failed or inconclusive case can be excellent if its consequence is intelligible. A routine case need not fabricate a failure branch.
5. Use the plan's contrast to reveal what matters: changing one relevant input should alter an inference, permissible next step, or conclusion. This may be one sentence within the case; it need not become another experiment. Avoid repeating an identical toy chain under different workflow names. Shared scenarios are useful only when each subsection demonstrates its own substantive operation.
6. Add only formal notation that explains the concrete case. For dependent typing, bind the actual problem/context and show why an assessment of one hypothesis cannot be reused for a different hypothesis without the declared conversion. Retain `Generated` wrappers and extraction premises. For categorical style, instantiate supported endpoints and retained inputs before displaying a composition. Map every symbol to the relevant content; omit decoration when no formal model licenses it.

Keep prose compact but sufficient to understand the problem, input, transformation, and outcome without opening the provenance file. Put administrative identifiers, source spans, and integration details in sidecars. Do not mistake domain precision for bureaucracy: quantities, constraints, and meaningful premises belong in the narrative when the reasoning needs them.

## Review and handoff

Emit per-workflow TeX fragments and `WorkflowExampleFragments` plus provenance/integration sidecars described in the contract. Escape untrusted source text as inert TeX; request any new packages through the owner. Keep synthetic values out of empirical claims, quantitative evaluation summaries, and claims about actual execution or workflow efficacy.

Review every workflow for realism, defining-mechanism fidelity, concrete inputs, visible reasoning, informative outcome, evidence posture, and meaningful formal annotations. An elegant generic vignette does not pass representativeness. Repair weaknesses and re-review changed fragments; record blocked cases explicitly. Send the complete bundle to the sole appendix owner, who merges each fragment inside its workflow subsection, validates the existing closed `PaperSectionDraft` schema, and hands the assembled section to consistency review and `$framework-paper-latex-assembler`. An isolated TeX build establishes buildability only.

## Mandatory step explanation gate

Read [the shared step explanation contract](../framework-paper-workflow-appendix-writer/references/step-explanation-contract.md) for occurrence-level paper revisions.

Write a before/after example for every binding in the planned continuous case. Reuse the actual prior output and preserve parallel input sharing; compare failure with a meaningful changed-input alternative.
