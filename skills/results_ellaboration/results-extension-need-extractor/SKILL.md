---
name: results-extension-need-extractor
description: Extract concrete extension needs from result-expansion slots, placeholders, author checklists, and marked gaps in a paper draft. Use when a draft must become a list of proof, computation, literature, transfer, and narrative obligations before writing or editing.
---

# Results Extension Need Extractor

## Conceptual Role

This skill turns paper markers into typed expansion needs. A need is not a vague TODO: it names the source marker, the missing result, the required inputs, the acceptable evidence, and the condition under which the marker can be replaced by final paper text.

## Workflow

1. Start from a context packet produced by `results-context-interpreter`.
2. For each slot or marker, extract the missing theorem, lemma, computation, table, estimate, prior-art comparison, or narrative explanation.
3. Type each need by work class:
   proof, coefficient extraction, finite calculation, same-theory transfer, uniform estimate, literature positioning, explanatory narrative, or submission cleanup.
4. State inputs and dependencies: regulator, observable family, finite matrix, coefficient tensors, source bounds, references, or draft sections.
5. State the replacement criterion: what final text, table, proof, bound, or appendix material discharges the marker.


## Epistemic Discipline

Treat each manuscript result as a mathematical object with an explicit epistemic status: proved, certified finite, conditional, conjectural, blocked, or demoted. Cite evidence through source artifacts, paper labels, validation reports, deterministic script outputs, or explicit unknowns. Preserve the finite/geometric/endpoint/continuum claim boundary, and end with a validation handoff or unresolved obligations.

## Output Contract

Return: source draft path, needs list, source labels, work class, priority, dependencies, discharge criterion, paper insertion target, blockers, and validation handoff.

## Guardrails

- Do not invent new research routes unless the draft marker requires them.
- Do not let operational provenance or discovery chronology become a paper need.
- Do not count a narrative explanation as discharging a proof or computation slot.

## Validation Handoff

Hand off to `results-extension-strategy-planner` with enough information to create self-contained TODOs.
## Failure/Demotion

Demote or quarantine the result when the evidence is missing, the mathematical object is not defined, the validation handoff fails, or the manuscript wording would overclaim beyond the cited source artifacts.
