---
name: results-expansion-validator
description: Validate a result-elaboration plan or expanded paper draft for slot coverage, claim-boundary preservation, local workflow-hook use, proof/computation discharge criteria, and narrative coherence. Use before treating a result-expansion plan as ready for manuscript editing or submission work.
---

# Results Expansion Validator

## Conceptual Role

This skill is the quality gate for result elaboration. It checks whether the plan actually addresses the paper markers and whether each proposed expansion has the right epistemic status.

## Workflow

1. Verify every result-expansion slot or marker has a corresponding need and TODO.
2. Verify every TODO has a discharge criterion, validation handoff, stop/quarantine condition, and paper insertion target.
3. Verify every TODO states the specific limitation it addresses in the draft and rejects generic marker-removal criteria.
4. Check that workflow hooks are local to result elaboration and do not call discovery-marathon workflows.
5. Check claim boundaries: finite theorem, Wilson-block application, and continuum Yang-Mills remain separated.
6. Check narrative coherence: the plan should improve the paper argument, not only add artifacts.


## Epistemic Discipline

Treat each manuscript result as a mathematical object with an explicit epistemic status: proved, certified finite, conditional, conjectural, blocked, or demoted. Cite evidence through source artifacts, paper labels, validation reports, deterministic script outputs, or explicit unknowns. Preserve the finite/geometric/endpoint/continuum claim boundary, and end with a validation handoff or unresolved obligations.

## Output Contract

Return: validation verdict, covered markers, uncovered markers, overclaim risks, missing dependencies, hook violations, narrative gaps, and required repairs.

## Failure/Demotion

Demote the plan if it leaves a slot unaddressed, treats a placeholder as a result, lacks slot-specific validation criteria, hides the limitation being fixed, wires into discovery workflows, or cannot explain how the expansion changes the paper.
