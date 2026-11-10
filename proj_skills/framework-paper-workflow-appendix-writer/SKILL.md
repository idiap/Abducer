---
name: framework-paper-workflow-appendix-writer
description: Write a scientific LaTeX appendix describing Prism workflows through source-backed typed objects, operation arrows, composition, and control annotations. Use after native workflow extraction, category modeling, claim curation, and notation approval; emit a reviewable section packet with provenance and integration instructions.
---

# Framework Paper Workflow Appendix Writer

Describe what the workflows mean, how typed operations compose, and which obligations remain open. Use category-theory notation only to the extent supported by the model; a workflow graph does not establish semantic laws.

When the requested representation is dependent-type-theory style, route to
`$framework-workflow-dependent-type-modeler` and `$framework-paper-dependent-type-writer`
using the same source packet. This skill remains the categorical presentation owner;
do not force typing judgments into an arrow-only narrative or require a category
model as an intermediate for the dependent lane.

## Required inputs

Consume one frozen bundle containing `PrismWorkflowAppendixSource`, `PrismWorkflowCategoryModel`, a curated claim ledger, and an approved `PaperBlueprint` assigning an appendix section to this skill. Read the category model's [contract](../framework-workflow-category-modeler/references/category-model-contract.md), and the [appendix handoff guide](references/appendix-handoff.md). Accept an indexed manuscript context packet for existing notation, labels, packages, appendix placement, and narrative overlap. The writer consumes packets, not raw repository inventory.

Require matching snapshot digests and referenced model/source packet IDs. Missing claim ownership, stale evidence, unresolved typing on a claimed composite, or absent notation approval blocks the affected prose. Record diagnostics rather than fill gaps from memory. Unknown behavior can be described as unknown under an authorized descriptive claim.

This is an optional skill-orchestrated scratch lane. The existing blueprint generator and runner do not allocate this appendix section. A manually authored, schema-valid scratch blueprint and claim ledger are valid inputs after claim curation and review have assigned this owner and its allowed claims; generating their JSON does not itself confer approval. Their `input_digest` must equal `RepositoryEvidenceIndex.index_digest`, distinct from hashes of serialized packet files. Record the review basis in the integration sidecar.

## Writing decisions

1. Open with the appendix scope and evidence posture. Explain why the selected workflows are grouped together and connect them to the paper's reasoning motifs. Distinguish native Prism declarations from source-policy routing and implementation or execution evidence.
2. Introduce objects as the model's typed boundary bundles, generating arrows as operation occurrences, and identities and path concatenation as syntactic structure. Use `g\circ f` only for a checked codomain/domain match. Retain named multi-input bindings, `Generated` wrappers, explicit adapters, and preserved context.
3. State separately which categorical structure is constructed and which semantic interpretation or equation is merely conditional or unresolved. Do not call two paths commutative from shared endpoints; do not infer products, coproducts, monads, natural transformations, or equivalence from diagrams, parallelism, branches, or `Generated` spelling.
4. Give a compact workflow coverage table and representative typed derivations. For each requested workflow record its purpose, input/output boundary, composition or unresolved segment, routing conditions/profile, evidence posture, and source mapping. Preserve original/native disagreements and partial ordering. Do not silently omit difficult workflows to make a complete-coverage claim.
5. Render checked paths using the manuscript's existing math packages; an `aligned` display with labeled arrows is an acceptable diagram. Visually distinguish control annotations from operation arrows, and explain any dashed or other notation in the caption. If TikZ or another package materially helps, request it in the handoff rather than insert a preamble into the fragment.
6. Translate every mathematical claim and diagram label back to the model and allowed claim IDs. Keep provenance details in the companion mapping, with concise source descriptions in the prose. Escape source labels as inert TeX text; never copy executable TeX from raw source descriptions.

Follow the blueprint's terminology and notation. The current manuscript already has an appendix covering canonical flow motifs; the context packet must specify whether this section supplements or replaces that coverage. Do not repeat the main argument or use operational inventory as scientific explanation.

## Granular Prism-level explanation

For occurrence-level conceptual descriptions, read [the granularity guide](references/granular-conceptual-description.md). Account for every declared occurrence and relation use in each scoped workflow, explaining its distinctive input, conceptual move, output and limit alongside a typed dependency display. Preserve explicit holes and inter-workflow adapter gaps. Motif labels or a signature inventory alone do not meet this request.

## Worked examples for every workflow

Incorporate accepted child fragments from `$framework-paper-workflow-example-writer`,
planned by `$framework-workflow-example-designer`, beside each workflow's formal
description. Show concrete values through the relevant arrows, a defining reasoning
step and a substantive outcome. Preserve illustrative-versus-observed labeling and
reconcile the original workflow scope against accepted examples before claiming full
coverage. Merge child prose and mappings into this owner's section, resolve labels,
and recompute hashes; child fragments are not duplicate sections.

## Taxonomy and type figures

When requested, incorporate `$framework-paper-taxonomy-plotter` figures from a reviewed
`ReasoningTaxonomyModel`. Introduce the reasoning membership overview and typed I/O
details with scientific captions explaining what each relation means. Preserve native
wrappers and retained multi-input context; taxonomy edges do not prove composability.
Merge figure claims, labels and provenance into this section's packet and fresh hashes.

## Outputs and integration

Emit a controlled TeX fragment and `PaperSectionDraft` using the existing [section schema](../../agentic/spec/framework_paper_section_draft.schema.json), plus the separate provenance and integration sidecars in the handoff guide. The section owner is `framework-paper-workflow-appendix-writer`. Do not add custom fields to the closed section schema.

Review source fidelity, type compatibility, mathematical claim posture, coverage, notation collisions, claim ownership, and TeX escaping. Pass the packet to the paper consistency/review lane and `$framework-paper-latex-assembler`. The assembler owns `\appendix`, packages, document ordering, labels, and final builds. A temporary compilation demonstrates TeX buildability only; preserve all scientific and runtime non-claims.

If the installed runner cannot route an appendix owner, return an explicit integration gap and reviewable fragments. Never label an unwired stage as automatically supported. Do not overwrite a manuscript/PDF or promote a publication as a side effect of drafting an appendix.

## Mandatory step explanation gate

Read [the shared step explanation contract](../framework-paper-workflow-appendix-writer/references/step-explanation-contract.md) for occurrence-level paper revisions.

Require a seven-field explanation and continuous example transition for every binding. Use the shared contract's compact Purpose/Input/Method/Check/Output/Next/Example presentation beside the typed display. Give Input and Output concise named scientific content; keep returned status separate from routing. A workflow-level paragraph cannot substitute for step explanations.

## Recursive goals and workflow relationships

When this explanation is requested, read [the shared recursive-goals contract](../framework-core-mechanism-curator/references/recursive-goals-and-workflow-relations.md). Reconcile every scoped workflow with the integrated relationship map and its evidence posture. Preserve unknown links and all occurrence explanations; grouping does not replace workflow-specific scientific content. This is a manual authoring extension, not a new fixed-runner schema or stage.
