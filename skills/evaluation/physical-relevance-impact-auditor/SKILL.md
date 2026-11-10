---
name: physical-relevance-impact-auditor
description: Audit whether a mathematical-physics subgoal has physical relevance and general field impact rather than only incremental mathematical progress. Use for Yang-Mills discovery cycles, Route A finite results, representational-dynamics branches, paper-readiness checks, result-atlas promotion, or any mathematical-physics contribution candidate that must name its physical carrier, same-theory handoff, continuum or spectral gate, field-facing consequence, and unification-power payoff before promotion.
---

# Physical Relevance Impact Auditor

## Conceptual Role

Use this skill when a branch is technically busy but may be drifting away from
physics. The goal is not to punish rigorous local mathematics. The goal is to
classify whether the local result is physically load-bearing, support-only, or
an incremental/proxy artifact until a physical handoff is supplied.

This is also an investment gate. Ordinary proof-search cycles should continue
only when the branch has high physics conceptual reward, visible unification
power, and plausible major-publication potential. If the branch would only
produce an incremental finite lemma, local estimate, symbolic identity,
endpoint calculation, or support-only theorem, the correct output is demote,
reframe, pivot, stop, quarantine, or route to a named artifact/falsifier sprint
whose success would unlock a major physics claim.

## Mathematical Invariants

Audit the mathematical object and physical object together: source theorem, gauge-invariant carrier, observable family, regulator/cutoff/volume/coupling regime, same-theory transfer interface, continuum limit, OS/Hamiltonian target, and spectral or nontriviality claim. The invariant is physical load-bearing preservation: a local lemma only matters when it preserves the carrier and touches a Clay-facing gate without changing theory.

Required edge cases and counterexamples include proxy observables, fixed-regulator artifacts, hidden matter or dimension changes, finite-to-continuum jumps, weak observable density, noncommuting limits, and claims where physical relevance is only motivational language.

## Epistemic Discipline

Every audit must assign epistemic status, evidence citation, source artifacts, explicit unknowns, and validation handoff. A branch can be `physically_relevant_candidate`, `math_support_only_pending_physical_handoff`, `incremental_math_drift_risk`, or `quarantine_proxy_or_artifact`; the decision must cite the physical carrier and missing evidence.

Disconfirming evidence, low unification power, low field impact, or absent same-theory handoff blocks another ordinary proof-search cycle even when the local mathematics is correct.

## Audit Procedure

1. Name the smallest honest mathematical claim.
2. Name the physical carrier:
   - gauge-invariant Wilson observable,
   - Schwinger-function family,
   - OS Hilbert-space object,
   - vacuum-orthogonal excitation sector,
   - Hamiltonian/spectral-measure object,
   - nontriviality witness such as a connected cumulant.
3. Name the larger target gate touched:
   - same-theory continuum construction,
   - OS/Wightman reconstruction,
   - gauge-invariant observable density,
   - nontriviality of the field,
   - positive spectral mass gap.
4. Explain the general impact: what a mathematical physicist or constructive
   QFT reader would understand differently if the claim were certified.
5. Explain the unification power: which formerly separate constraints,
   carriers, estimates, representations, or routes are compressed by one
   mechanism, and what new hypothesis or proof obligation this compression
   exposes.
6. State the major publication gate:
   - `invest_high_physics_reward` only when the pathway can plausibly change
     understanding around a named physical carrier and Clay-facing gate while
     unifying more than one target pressure;
   - `reframe_before_investment` when the idea may be promising but lacks a
     sharp physics claim, unification claim, or route-changing artifact;
   - `do_not_invest_support_only` when the result is useful background or
     appendix material but not a major YM pathway;
   - `quarantine_low_physics_reward` when the branch is proxy-like, local, or
     physically ungrounded.
7. Separate support-only mathematics from physics impact. A finite lemma,
   algebraic identity, Schur complement, or endpoint calculation is support-only
   unless it says how it changes a physical carrier, target gate, or unifies
   previously separate physical/proof pressures.
8. State the next physical-relevance test that would promote, demote, pivot, or
   quarantine the branch.

## Scoring Dimensions

Return a 0-5 assessment for:

- `physical_carrier_integrity`
- `same_theory_physical_transfer`
- `continuum_and_scale_relevance`
- `spectral_gap_interface`
- `nontriviality_and_observable_content`
- `field_understanding_impact`
- `unification_power`
- `route_decision_power`

Each score must include evidence and missing evidence. Strong evidence must use
the target's physics language, not generic paper-value vocabulary.

## Dispositions

- `physically_relevant_candidate`: a physical carrier, target gate, and
  falsifier-backed next test are all visible.
- `math_support_only_pending_physical_handoff`: the mathematics may be useful,
  but the physical carrier, continuum/spectral handoff, or same-theory
  transfer is not yet certified.
- `incremental_math_drift_risk`: the branch adds local calculations or lemmas
  without a physical target commitment.
- `quarantine_proxy_or_artifact`: the branch depends on a proxy observable,
  fixed-cutoff artifact, toy theory, or silent change of physical theory.

## Output Contract

Return:

- `smallest_honest_claim`
- `physical_carrier`
- `target_commitments_touched`
- `general_impact_vector`
- `relevance_decision`
- `major_publication_gate`
- `general_impact_claim`
- `incremental_math_drift_risk`
- `next_physical_relevance_test`
- `overclaim_boundary`
- `evidence`
- `validation_handoff`

## Failure/Demotion

Demote when the branch cannot name a physical carrier, same-theory handoff,
continuum or spectral interface, nontriviality witness, field-facing
understanding gain, unification gain, or falsifier-backed route decision.

Do not allow "mathematically interesting" to substitute for physical relevance.
Do not allow a list of adjacent lemmas to count as unification unless one
mechanism, representation, carrier, or estimate genuinely compresses multiple
target pressures.
Do not allow a fixed-regulator calculation to imply continuum physics unless
the transfer conditions are explicit.
Do not recommend another ordinary proof-search cycle unless
`major_publication_gate.investment_decision` is `invest_high_physics_reward`.
