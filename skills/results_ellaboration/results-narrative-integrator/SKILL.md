---
name: results-narrative-integrator
description: Integrate result expansions into the explanatory narrative of a mathematical or physics paper. Use when new theorem, computation, transfer, or prior-art material must be placed into the manuscript without disrupting claim boundaries or turning the paper into a list of TODOs.
---

# Results Narrative Integrator

## Conceptual Role

This skill decides how result-elaboration work should read inside the paper. It translates completed or pending expansion needs into a coherent explanatory arc: why the result matters, what it proves locally, why the transfer boundary is honest, and where the reader should see the next mathematical pressure.

## Workflow

1. Read the draft context and the ordered extension TODOs.
2. Build the narrative spine: motivation, finite theorem, Wilson-block transfer, coefficient extraction, first application, endpoint extension, claim boundary.
3. For each expansion need, specify where it belongs: theorem section, application section, appendix, discussion, prior-art paragraph, figure/table, or author-only checklist.
4. Write explanation requirements for the final prose: definitions before equations, assumptions before claims, local result before global relevance, non-claims before speculative implications.
5. State how a completed TODO should change the abstract, introduction, section transitions, and conclusion.


## Epistemic Discipline

Treat each manuscript result as a mathematical object with an explicit epistemic status: proved, certified finite, conditional, conjectural, blocked, or demoted. Cite evidence through source artifacts, paper labels, validation reports, deterministic script outputs, or explicit unknowns. Preserve the finite/geometric/endpoint/continuum claim boundary, and end with a validation handoff or unresolved obligations.

## Output Contract

Return: narrative spine, insertion map, explanation requirements, abstract/introduction/conclusion update plan, appendix policy, claim-boundary warnings, and validation handoff.

## Guardrails

- Do not hide missing mathematics behind fluent explanation.
- Do not elevate conditional endpoint algebra into a completed Wilson calculation.
- Do not make the paper claim Yang-Mills construction, OS reconstruction, or mass gap unless those obligations are actually discharged.

## Validation Handoff

Hand off to `results-expansion-validator` or a TeX compile/audit pass once manuscript edits are made.
## Failure/Demotion

Demote or quarantine the result when the evidence is missing, the mathematical object is not defined, the validation handoff fails, or the manuscript wording would overclaim beyond the cited source artifacts.
