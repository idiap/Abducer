---
name: framework-paper-dependent-type-writer
description: Draft scientific paper sections or appendices explaining Prism workflows through dependent typing judgments, indexed artifact families, dependent pairs, and explicit substitution. Use after source extraction, dependent-type modeling, and claim/notation review to produce a reviewable LaTeX section packet.
---

# Framework Paper Dependent Type Writer

Explain which later artifacts depend on which earlier values, what makes each step well typed, and what the notation establishes. This is a paper-writing lane, not a dependent type checker or a mechanical renaming of category arrows.

## Inputs and scope

Consume a frozen `PrismWorkflowAppendixSource`, `PrismWorkflowDependentTypeModel`, curated claim ledger, approved `PaperBlueprint`, and manuscript context packet. The blueprint assigns this owner, permitted claims, notation, labels, and placement. Read the model's [contract](../framework-workflow-dependent-type-modeler/references/dependent-type-model-contract.md) and the [writing and handoff guide](references/dependent-type-writing.md).

Require matching source/model identifiers and snapshot digests. `input_digest` is the `RepositoryEvidenceIndex.index_digest` copied through the blueprint, not a hash of a serialized input file. Incomplete evidence, unlicensed claims, or an ill-typed derivation blocks the affected claim; return a diagnostic and retain explicit unknowns instead of inventing premises.

Default to an appendix supplement to the current paper's canonical-flow coverage. A main-text formalization section is supported when assigned by the blueprint. Neither choice authorizes rewriting the manuscript. This optional lane is invoked through skills with manually prepared, reviewed packets; the current CLI/runner does not allocate this owner. Record that integration gap rather than claim automatic support.

## Writing decisions

1. Lead with the scientific question answered by indexing: preserving which context, candidate, or snapshot a result concerns. State the selected calculus and whether the model is a native projection, an expository construction, or a proposed indexed refinement.
2. Introduce ordered contexts, type formation, and term judgments before the first derivation. Explain `Pi` as a family-indexed function and `Sigma` as a value with a dependent component only when these structures are present in the model. Plain records and function arrows need no dependent embellishment.
3. Explain one source-backed chain and one value-sensitive case through variable binding, substitution, and retained context. Display every adapter or wrapper-elimination premise. `Generated[T]` is not `T`; do not synthesize an extraction operation or monadic laws from its name.
4. Distinguish source facts, well-formedness under declared assumptions, proposed refinements, checked proof terms, and open obligations throughout. An assessment record or successful test is evidence about an artifact, not automatically an inhabitant of a proposition proving that artifact correct. A declared constant is an assumption until its implementation or proof is separately established.
5. Keep definitional equality, propositional identity, observational comparison, and same-endpoint typing separate. Transport across an index equality requires the stated equality witness and family. Do not infer proof irrelevance, uniqueness of identity proofs, univalence, equivalence, or a compiler guarantee.
6. Give a compact mapping for every workflow in scope: purpose, native boundary, dependent presentation, substitution/adapter premises, source posture, and unresolved obligations. Preserve discrepancies and incomplete chains. Explain how the representation complements any existing categorical presentation without asserting an unconstructed categorical/type-theoretic correspondence.

Every mathematical display and substantive assertion must map to permitted claim IDs and model records. Use the context packet's notation, escape source labels as inert TeX, and request additional packages through the integration sidecar. Keep detailed source spans out of the narrative unless they aid understanding.

## Granular workflow explanations

When the user asks for Prism-level conceptual detail, apply the [granularity guide](../framework-paper-workflow-appendix-writer/references/granular-conceptual-description.md) to each scoped workflow before presenting indexed refinements. Explain the native occurrence and relation structure first; dependent notation then exposes a specific retained-value obligation. A polished indexed example for one workflow does not fulfill a request covering the full workflow family.

## Worked examples for every workflow

Use `$framework-workflow-example-designer` and `$framework-paper-workflow-example-writer`
to include one accepted, substantive example under every workflow in the appendix scope.
Instantiate contexts and indices with the case's actual claims, inputs and assessments;
show why a dependent input matters to one concrete inference. Keep technical mappings
in sidecars, and lead reader-facing prose with the problem and what the reasoning finds.
Preserve hypothetical-case labeling and native/refinement limits. Merge child fragments
and provenance under this section owner, recompute hashes, and withhold complete coverage
when an original scoped workflow lacks an accepted example.

## Taxonomy and type figures

When requested, incorporate reviewed `$framework-paper-taxonomy-plotter` outputs beside
the appendix's workflow descriptions. Distinguish native nominal type/use diagrams from
proposed indexed-family refinements; a wrapper, bundle or shared label does not establish
subtyping or equality. Explain any displayed index using the approved model. Preserve
figure coverage, readable labels and claim/provenance mapping under this section owner.

## Outputs and review

Emit a TeX fragment, the existing `PaperSectionDraft`, and provenance/integration sidecars as specified in the guide. Set `section_owner` to `framework-paper-dependent-type-writer`. `tex_fragment` holds a filename, never inline TeX; do not extend the closed section schema.

Review index fidelity, context order, substitution, native/refinement separation, proof/evidence distinctions, claim ownership, coverage, notation collisions, packet digests, and TeX escaping. Send reviewable packets to the paper consistency/review lane and `$framework-paper-latex-assembler`. The assembler owns document structure, package imports, placement, and final builds. Isolated compilation checks TeX buildability only. Return remaining scientific and integration obligations explicitly; do not overwrite the manuscript or current PDF as a drafting side effect.

## Mandatory step explanation gate

Read [the shared step explanation contract](../framework-paper-workflow-appendix-writer/references/step-explanation-contract.md) for occurrence-level paper revisions.

Require the same seven-field step explanations as the categorical lane. Index-sensitive notation must accompany concrete reasoning and examples; judgments alone do not meet explanatory completeness.
