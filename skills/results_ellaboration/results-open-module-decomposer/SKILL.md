---
name: results-open-module-decomposer
description: Decompose paper open-module environments or forward-work blocks into precise result-extension obligations. Use when a manuscript already contains a finite result and names open modules such as geometric family, normalization, coefficient extraction, endpoint bounds, continuum reconstruction, or spectral gap.
---

# Results Open Module Decomposer

## Conceptual Role

This skill turns a paper's explicit open modules into publishable next-result tasks. It is for manuscripts that are beyond placeholder slots: the current paper may already prove a finite theorem, while the open modules define the exact boundary between claimable results and future work.

## Workflow

1. Deterministically extract every `openmodule` block, its section, label/name, source text, and nearby equations or claims.
2. Classify each module by mathematical role: geometric construction, same-theory normalization, coefficient extraction, nondegeneracy, endpoint derivation, endpoint/tail bounds, continuum reconstruction, spectral estimate, or manuscript hygiene.
3. Split each module into:
   - deterministic regime: algebra, labels, TeX, finite symbolic checks, exact matrix identities, boundedness checks;
   - generative regime: proof strategy, construction design, estimate architecture, literature positioning, and paper narrative integration.
4. Produce self-contained TODOs with dependencies, expected artifacts, validation handoffs, stop/quarantine conditions, and paper insertion targets.
5. Mark which TODOs can be implemented inside the current paper and which must remain as bounded open modules.


## Epistemic Discipline

Treat each manuscript result as a mathematical object with an explicit epistemic status: proved, certified finite, conditional, conjectural, blocked, or demoted. Cite evidence through source artifacts, paper labels, validation reports, deterministic script outputs, or explicit unknowns. Preserve the finite/geometric/endpoint/continuum claim boundary, and end with a validation handoff or unresolved obligations.

## Output Contract

Return: extracted modules, module taxonomy, deterministic checks, generative proof-plan tasks, dependency graph, ordered TODOs, paper insertion targets, critical self-refinement prompts, and validation handoff.

## Guardrails

- Do not promote an open module into a theorem unless the paper already contains the necessary proof ingredients.
- Do not treat finite source-collision algebra as a proof of geometric collar collapse.
- Do not treat finite reflection positivity as OS reconstruction or a spectral gap.
- Keep the result-elaboration workflow independent from discovery marathons and target schedulers.

## Validation Handoff

Hand off to `results-critical-self-refiner` and `results-expansion-validator`. The validator must check that every open module is either converted into a concrete manuscript patch plan or explicitly kept open with a reason.
## Failure/Demotion

Demote or quarantine the result when the evidence is missing, the mathematical object is not defined, the validation handoff fails, or the manuscript wording would overclaim beyond the cited source artifacts.
