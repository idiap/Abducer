---
name: framework-paper-core-mechanism-writer
description: Put core reasoning mechanisms at the center of a scientific paper through concise conceptual explanations, substantive worked examples, and an argument showing how mechanisms compose. Use a reviewed core-mechanism model, claim ledger, and blueprint to draft the main-text method section or child fragments for its sole owner.
---

# Framework Paper Core Mechanism Writer

For step-level requests, apply [the step explanation contract](../framework-paper-workflow-appendix-writer/references/step-explanation-contract.md).
For a request centered on occurrence explanation, write one continuous case through
the actual occurrences, including a targeted defeater and the retained-context join.
For conceptual-inquiry requests, the main case follows changes in the conceptual
situation; the complete occurrence reconstructions belong in the supporting
appendix. Preserve their scope without letting them dictate the main argument.

Make the reader understand what changes in the reasoning, why that change matters, and how the core operations work together. The main text must carry this explanation; exhaustive workflow listings, type details, and taxonomy figures can support it in the appendix.

## Inputs and section authority

Consume the reviewed `CoreReasoningMechanismModel` from `$framework-core-mechanism-curator`, its frozen source/model bindings, curated claim ledger, approved `PaperBlueprint`, and manuscript context packet. Read the [model contract](../framework-core-mechanism-curator/references/core-mechanism-model-contract.md) and [writing and handoff guide](references/core-mechanism-writing.md). Reuse reviewed example plans when available; do not depend on repository exploration or invent missing native behavior. Reject mismatched source snapshots, stale review hashes, unresolved core selection, or claims not licensed for the final owner. Curator candidate claims require ledger review before use; they are not automatically permitted claims.

This is a manual skill-orchestrated lane. The current CLI does not allocate this owner automatically. The blueprint must assign either this skill as sole owner of a main-text method/core section, or `$framework-paper-method-writer` as sole owner receiving this skill's child fragments. Never emit competing section drafts or duplicate content ownership. Shared claim summaries in the introduction, abstract, or conclusion are permitted when separately authorized by the blueprint, with one authoritative main explanation. Do not modify the current manuscript as a drafting side effect. If main-text placement or claim assignment needs revision, emit an integration proposal for the blueprint owner and mark assembly blocked until reviewed.

## Explain conceptual inquiry

Follow [the shared conceptual inquiry contract](../framework-core-mechanism-curator/references/conceptual-inquiry-contract.md) and require the reviewed 2.0.0 model. Begin with the incumbent conceptual situation and a concrete tension. Make diagnosis explicit, including a grounded `not_conceptual` handoff where ordinary work suffices. Explain materially different primitives, relations, representations, or explanatory commitments and show what each preserves and risks.

Carry one substantive case through the source profile's ontology, dialectic, genealogy, modality, unification, and philosophy-of-physics lenses where applicable. Preserve broader source-profile variation and reasoned non-applicability. Each applied lens must change or defensibly retain actual conceptual content, not repeat its name. Show strongest opposition, preserved successes and differences, plural comparison, understanding delta, new consequences, and revision/correction conditions. These are revisitable questions rather than a universal sequence.

Write connected explanatory units with actual inputs, a visible conceptual change, meaningful contrast and limit. Do not assign one generic paragraph to each operator. Source-bound primitive/composition/motif distinctions may annotate particular moves but are not required card kinds. Native A/D/I and other families can map many-to-many to the inquiry and cannot silently define its stages or exhaust cognition. Retain the full step-level main-text walkthrough and appendix explanations as supporting operational detail.

Introduce formal notation after the conceptual need it addresses. Distinguish native declaration, prescribed procedure, constructed illustration, proposed refinement, and observed execution. Keep target identity, quantifiers, regimes, unknown order, and unresolved producers visible. A selected conceptual anchor requires meaningful main-text example content; a table or appendix-only explanation does not suffice. No fixed word budget may compress away a diagnostic alternative, preserved difference, or correction condition. When structured descriptions are requested, use the [shared step contract](../framework-paper-workflow-appendix-writer/references/step-explanation-contract.md): concise purpose, separately named inputs and outputs, and distinct method, check and continuation. Preserve scientific depth in the worked transformation rather than repeating setup in every field.

## Review and handoff

Emit the outline/integration proposal, controlled TeX, provenance, and the owner-mode packet described in the guide. Require review of core prominence, conceptual specificity, diagnostic exit, substantive alternatives, source-profile reflection, preserved differences, plural comparison, correction conditions, succinctness, meaningful examples, composition, evidence posture, claim authority, and main-text placement. Return missing evidence and incomplete examples explicitly; do not silently shrink the selected core set.

In sole-owner mode validate the existing closed `PaperSectionDraft`; `tex_fragment` is a filename, `input_digest` is the blueprint evidence-index digest, and `section_digest` uses the existing canonical producer convention. In child mode emit no second `PaperSectionDraft`; the method owner merges claims and provenance and computes final digests. Route final content to consistency review and `$framework-paper-latex-assembler`, which owns document structure and compilation. A successful isolated build establishes TeX buildability, not scientific validity or framework efficacy.

## Recursive goals and workflow relationships

When this explanation is requested, read [the shared recursive-goals contract](../framework-core-mechanism-curator/references/recursive-goals-and-workflow-relations.md). Explain why tensions create nested obligations, how child evidence changes parent understanding, and why a stopped attempt can leave its goal open. Carry the continuous scientific case through return, failure, stopping and reopening. This is a manual authoring extension, not a new fixed-runner schema or stage.
