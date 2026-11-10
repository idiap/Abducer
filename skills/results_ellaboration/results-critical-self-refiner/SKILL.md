---
name: results-critical-self-refiner
description: Critically self-refine a result-elaboration plan by testing whether TODOs are paper-specific, mathematically typed, regime-separated, claim-bounded, and capable of feeding back into the manuscript narrative. Use before accepting generated result-extension TODOs.
---

# Results Critical Self Refiner

## Conceptual Role

This skill is the reflective quality gate for result elaboration. It checks whether a plan actually advances the paper or merely restates the open modules in polished prose.

## Workflow

1. For each TODO, ask what concrete mathematical object changes if the TODO succeeds.
2. Separate deterministic validation from generative mathematical work:
   - deterministic validation includes exact symbolic algebra, matrix identities, label/reference checks, TeX compilation, and reproducibility scripts;
   - generative work includes construction of geometric collars, endpoint estimates, transfer theorems, continuum limits, and spectral arguments.
3. Check the paper-integration path: theorem, proposition, table, figure, appendix, numerical protocol, claim-boundary paragraph, or open-module revision.
4. Apply premature-promotion tests:
   - Does this finite statement secretly claim a continuum result?
   - Does this source-collision statement secretly claim a geometric-collar result?
   - Does this endpoint lower bound secretly claim a negative obstruction?
   - Does this reflection-positivity block secretly claim a mass gap?
   - Does this scoped method-class theorem secretly claim the full proof system?
   - Does this route-level obstruction secretly claim the main open problem?
5. Revise TODOs until each has a success artifact, failure/demotion artifact, validation handoff, and manuscript insertion point.

## Recurring Certification Stack

When a TODO is trying to turn a discovery result into a publishable subgoal, require these handoffs:

1. `results-theorem-scope-certifier` for the smallest honest claim and non-claims.
2. `results-finite-object-formalizer` for any new parameter, certificate, quotient, residual set, or obstruction object.
3. `results-proof-packet-deriver` for theorem/proof closure or exact proof debt.
4. `results-prior-art-disqualifier-auditor` for novelty, target-equivalence, advice/model leakage, and barrier status.
5. `results-paper-readiness-gatekeeper` before any paper-ready decision.


## Epistemic Discipline

Treat each manuscript result as a mathematical object with an explicit epistemic status: proved, certified finite, conditional, conjectural, blocked, or demoted. Cite evidence through source artifacts, paper labels, validation reports, deterministic script outputs, or explicit unknowns. Preserve the finite/geometric/endpoint/continuum claim boundary, and end with a validation handoff or unresolved obligations.

## Output Contract

Return: refined TODOs, rejected/generic TODOs, claim-boundary warnings, deterministic/generative split audit, paper-integration audit, and next executable validation command.

## Guardrails

- Do not accept TODOs whose acceptance criterion is "expand this section" or "prove the needed theorem" without naming the object, estimate, or certificate.
- Do not reward breadth over claimability. A narrow theorem with a clear manuscript insertion point is preferred to broad speculative exploration.
- Keep all hooks local to the result-elaboration workflow.

## Validation Handoff

Hand off to `results-expansion-validator` and, when applicable, TeX compilation or exact symbolic scripts.
## Failure/Demotion

Demote or quarantine the result when the evidence is missing, the mathematical object is not defined, the validation handoff fails, or the manuscript wording would overclaim beyond the cited source artifacts.
