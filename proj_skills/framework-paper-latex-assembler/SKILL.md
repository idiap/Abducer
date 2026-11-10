---
name: framework-paper-latex-assembler
description: Deterministically assemble approved framework-paper section fragments, figures, bibliography metadata, and labels into a standalone LaTeX source and build manifest. Use after all mandatory section packets pass claim and consistency review.
---

# Framework Paper LaTeX Assembler

For conceptual-organization requests, follow [the shared conceptual inquiry contract](../framework-core-mechanism-curator/references/conceptual-inquiry-contract.md). Require one reviewed conceptual argument across body, abstract, introduction, conclusion, and figures before integration. Preserve its `not_conceptual` exit, plural alternatives, correction conditions, and supporting status of operator notation through assembly. Retain the existing complete workflow/occurrence appendix and its actual inclusion checks. Rebuild and inspect the requested manuscript with refreshed hashes and provenance; a conceptual reorganization is not a new supported fixed-runner stage.

Consume an approved blueprint and section packets from one evidence-bundle digest.

1. Fail closed on missing, duplicate, stale, or unapproved mandatory sections.
2. Own the document wrapper, packages, ordering, labels, cross-references, and bibliography wiring.
3. Never interpolate raw repository inventory text; section producers must provide controlled fragments.
4. Write `main.tex` and `build-manifest.json` deterministically.
5. Compile in a temporary directory only when an engine exists. Compilation proves build syntax, not scientific validity.
6. Never modify `docs/publications/`; promotion is a separate explicit operation.

Run `scripts/assemble_paper.py`, then `$framework-paper-validator`.

For the optional skill-authored workflow appendix, review its fragment and sidecar
separately: the current script has no appendix mode. In an explicitly requested manuscript
integration, insert after the existing `\appendix` or introduce that switch once, resolve
labels and notation against the paper, and rebuild with updated provenance. A standalone
scratch wrapper is appropriate for testing; do not silently amend a validated bundle.

Taxonomy plot PDFs and inclusion fragments come from `$framework-paper-taxonomy-plotter`.
Preserve vector originals, resolve paths relative to the assembled document, declare
`graphicx` when needed, and check legibility at the actual appendix page size. The main
section owner merges figure claims/captions/provenance and recomputes hashes. Do not
insert a second appendix switch or treat renderer success as a scientific review pass.

## Mandatory step explanation gate

Read [the shared step explanation contract](../framework-paper-workflow-appendix-writer/references/step-explanation-contract.md) for occurrence-level paper revisions.

Render accepted StepExplanationPacket fragments with the reusable checker, incorporate each exactly once in the actual workflow subsection, rebuild the requested root paper, and inspect final pages. Verify inclusion and fresh hashes; a scratch PDF is not delivery. Preserve the seven separate field labels from the shared renderer and inspect their alignment, wrapping and page breaks at final size. Re-render and recheck exact fragment inclusion after formatting changes; never merge Output and Next to save space.

## Recursive goals and workflow relationships

When this explanation is requested, read [the shared recursive-goals contract](../framework-core-mechanism-curator/references/recursive-goals-and-workflow-relations.md). Preserve the reviewed goal/attempt distinction, stopping table, recursive example, relationship overview and complete keyed workflow detail through integration. Rebuild and inspect the actual paper and refresh provenance. This is a manual authoring extension, not a new fixed-runner schema or stage.
