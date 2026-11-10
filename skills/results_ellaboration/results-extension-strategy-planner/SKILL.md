---
name: results-extension-strategy-planner
description: Plan a paper-specific result-elaboration strategy from extracted extension needs. Use when a draft needs detailed self-contained TODOs, skill assignments, validation criteria, and non-discovery workflow hooks for expanding result slots into publishable material.
---

# Results Extension Strategy Planner

## Conceptual Role

This skill plans how to discharge paper expansion needs without turning the paper into an open-ended discovery marathon. It orders work by claim payoff, dependency order, and replacement value in the manuscript.

## Workflow

1. Read typed needs from `results-extension-need-extractor`.
2. Build a dependency graph between needs: context first, transfer certificates before application claims, coefficient extraction before finite sign tests, prior-art boundary before novelty language.
3. Create self-contained TODOs. Each TODO must name:
   source marker, target section, mathematical object, required input, action, expected artifact, slot-specific validation criterion, limitation addressed, paper insertion target, stop condition, and skill handoff.
4. Assign result-elaboration skills and compatible existing reporting/evaluation skills when useful.
5. Add workflow hooks only inside the result-elaboration workflow: pre-context, post-need-extraction, pre-strategy, post-narrative, final-validation.


## Epistemic Discipline

Treat each manuscript result as a mathematical object with an explicit epistemic status: proved, certified finite, conditional, conjectural, blocked, or demoted. Cite evidence through source artifacts, paper labels, validation reports, deterministic script outputs, or explicit unknowns. Preserve the finite/geometric/endpoint/continuum claim boundary, and end with a validation handoff or unresolved obligations.

## Output Contract

Return: strategy ID, ordered TODOs, dependency graph, skill map, local workflow hooks, validation matrix, demotion criteria, narrative integration plan, and next executable command.

## Guardrails

- Do not hook this workflow to discovery marathon jobs, branch queues, or target-run schedulers.
- Do not schedule infinite exploration; every TODO must have a discharge criterion or quarantine condition.
- Do not accept class-level boilerplate such as "remove the marker" or "add assumptions and remainders" as a validation criterion. The TODO must say what mathematical object becomes checkable and where it enters the paper.
- Do not claim the paper is publishable until proof, computation, transfer, and prior-art TODOs that support the stated contribution are discharged.

## Validation Handoff

Run the result-elaboration report builder and validator when available, then inspect the produced TODO report.
## Failure/Demotion

Demote or quarantine the result when the evidence is missing, the mathematical object is not defined, the validation handoff fails, or the manuscript wording would overclaim beyond the cited source artifacts.
