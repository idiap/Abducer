---
name: results-context-interpreter
description: Interpret a mathematical or physics paper draft as a result-bearing argument context. Use when a draft contains theorem statements, claim boundaries, result-expansion slots, placeholders, appendices, or author-facing markers that must be understood before planning paper-specific elaboration work.
---

# Results Context Interpreter

## Conceptual Role

This skill reads a paper draft as an argument object, not as a discovery log. It identifies the main theorem, the bounded contribution claim, the mathematical objects, the explicit non-claims, and the section-level role of each result slot.

## Workflow

1. Read the draft TeX or Markdown and identify title, abstract, main theorem, proof sections, application sections, appendices, and author-facing checklists.
2. State the paper's smallest honest contribution and the strongest claim it explicitly forbids.
3. Extract the main mathematical objects, validity regimes, and transfer boundaries.
4. Classify every expansion marker by argument role: theorem completion, coefficient computation, transfer certificate, prior-art boundary, worked example, narrative explanation, or submission cleanup.
5. Preserve exact labels and section names so downstream skills can patch or plan against the draft without ambiguity.


## Epistemic Discipline

Treat each manuscript result as a mathematical object with an explicit epistemic status: proved, certified finite, conditional, conjectural, blocked, or demoted. Cite evidence through source artifacts, paper labels, validation reports, deterministic script outputs, or explicit unknowns. Preserve the finite/geometric/endpoint/continuum claim boundary, and end with a validation handoff or unresolved obligations.

## Output Contract

Return: paper context ID, source draft path, title, abstract claim, bounded contribution, non-claims, main mathematical objects, section map, expansion markers, argument roles, epistemic status, and validation handoff.

## Guardrails

- Do not route this into discovery-marathon workflows.
- Do not turn placeholders into proved claims.
- Do not weaken the draft's explicit claim boundary.
- Keep finite theorem claims, Wilson-block application claims, and continuum Yang-Mills claims separate.

## Validation Handoff

Hand off to `results-extension-need-extractor` with source labels, slot labels, and argument roles intact.
## Failure/Demotion

Demote or quarantine the result when the evidence is missing, the mathematical object is not defined, the validation handoff fails, or the manuscript wording would overclaim beyond the cited source artifacts.
