---
name: contribution-value-assessor
description: Qualify the value of a scientific contribution candidate by conceptual novelty, explanatory power, implications, generality, robustness, and validation burden. Use when a subgoal has been detected as contribution-shaped and needs a rigorous value assessment rather than a generic breakthrough score.
---

# Contribution Value Assessor

## Conceptual Role

Use this skill after a candidate contribution has been detected. Its job is to judge the quality of the contribution, not merely whether it is exciting.

Assess four primary dimensions:

1. `conceptual_novelty`: does the subgoal introduce a new abstraction, obstruction, bridge, decomposition, or viewpoint?
2. `explanatory_power`: does it make a mechanism clearer, reduce confusion, or explain why routes succeed or fail?
3. `implications`: what downstream proof, experiment, method, or research decisions become possible?
4. `certification_readiness`: what evidence exists, what is missing, and what could falsify the claim?

Separate two scores:

- `exploration_payoff_score`: whether this branch is worth testing next.
- `publishable_subgoal_score`: whether this branch is close to a paper-level stepping-stone contribution.

High exploration payoff is not enough for publishable readiness.

## Paper Relevance Markers

When judging whether a candidate is close to a good enough paper, add a separate marker layer:

- `conceptual_depth`: Does it reach a deep proof obligation or conceptual pressure point?
- `conceptual_novelty`: What is new relative to the closest known result family?
- `unblocking_power`: Which branch, proof route, or paper decision does it unlock?
- `applicability`: Where else can the object, theorem, test, or abstraction be reused?
- `understanding_gain`: What does it explain that was previously confused, opaque, or only heuristic?

For P vs NP, make the assessment concrete: source language/carrier, target class, circuit model, transfer inequality, all-exponent quantifier behavior, nonuniform/advice leakage, and barrier status must be named when relevant. A marker is `strong` only when it changes a route-level mathematical decision, not merely when it uses impressive vocabulary.

## Assessment Procedure

1. Restate the candidate in its smallest honest form.
2. Score each dimension qualitatively: `low`, `medium`, `high`, or `exceptional`.
3. Explain each score with evidence, not adjectives.
4. Name the audience: theorem prover, mathematical physicist, epistemologist, workflow scientist, or domain expert.
5. Compare against the null contribution: what would the field or project still not know without this subgoal?
6. Identify implications at three horizons: immediate next analysis, broader route portfolio, and possible paper contribution.
7. State the validation burden and overclaim boundary.
8. Run disqualifier-first review before promotion:
   - already known,
   - proxy problem,
   - target-equivalent assumption,
   - evidence gap,
   - validation unbounded,
   - overclaim risk,
   - narrow bookkeeping.
9. Classify stepping-stone maturity as `contribution_shaped`, `near_stepping_stone`, or `publishable_handoff_ready`.

## Mathematical Invariants

- Mathematical object: contribution claim, novelty-bearing concept, explanatory mechanism, implication chain, evidence basis, and validation burden.
- Preserved invariants: claim scope, assumptions, status labels, relation to the main target, and prior-art uncertainty.
- Broken invariants: novelty asserted without comparison class, explanatory power asserted without mechanism, implications asserted without a downstream decision, or certification claimed without validation.
- Edge case or counterexample: a strong assessment must survive known-prior-art, same-theory transfer failure, boundary regimes, and cases where the result only works for a proxy object.

## Epistemic Discipline

Use epistemic status labels: `provisional_value`, `evidence_backed_value`, `high_prior_art_risk`, `high_validation_burden`, `overclaim_risk`, `certification_ready`, or `quarantine`.

Keep novelty, explanatory power, implications, and proof status separate. A result can be conceptually novel but not yet certified; it can be explanatory but already known; it can be technically valid but low implication.

## Output Contract

Return:

1. `Candidate Summary`: smallest honest claim and contribution type.
2. `Value Matrix`: conceptual novelty, explanatory power, implications, generality, robustness, and certification readiness.
3. `Evidence For Each Dimension`: artifacts, equations, source cycles, validators, source references, or explicit unknowns.
4. `Implication Map`: immediate, route-level, and paper-level consequences.
5. `Validation Burden`: what remains to certify or demote the contribution.
6. `Overclaim Boundary`: exactly what the contribution does not prove.
7. `Hard Gates`: claim statement, evidence, novelty boundary, validation/disqualifier, and overclaim boundary.
8. `Prior-Art Boundary`: closest known results, reused machinery, novelty-if-true, rediscovery risk, and citation tasks.
9. `Paper Relevance Markers`: conceptual depth, conceptual novelty, unblocking power, applicability, understanding gain, with evidence and missing work.
10. `Final Disposition`: publishable handoff, near stepping stone, contribution-shaped, develop, watch, quarantine, or reject.

## Failure/Demotion

Demote if the assessment uses generic praise, collapses novelty into usefulness, hides prior-art risk, lacks evidence citations, labels exploration value as publishable readiness, or fails to state what would disconfirm or demote the contribution.

## Validation Handoff

Use `python agentic/scripts/build_scientific_contribution_monitor.py` and `python agentic/scripts/validate_scientific_contribution_monitor.py`; for prior-art uncertainty, hand off to `prior-art-importer` or `evidence-acquisition-planner`.
