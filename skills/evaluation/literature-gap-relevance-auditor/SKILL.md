---
name: literature-gap-relevance-auditor
description: Audit whether a proof avenue has a precise literature-positioned research gap, novelty boundary, field or physics impact, unification power, route-decision power, and enough major-publication reward to justify broad investment. Use before opening a new branch-exploration avenue, before promoting a marathon route after shallow cycles, after prior-art criticism, or whenever Abducer must decide between invest_in_avenue, artifact_sprint_only, reframe_gap_before_investment, do_not_invest_prior_art_collision, and quarantine_low_relevance.
---

# Literature Gap Relevance Auditor

## Purpose

Use this skill as a preinvestment gate. Its job is to stop the workflow from
spending broad proof-search cycles on routes that are merely interesting,
definition-built, local, rediscovered, or weakly relevant to the target field.

The output is not a literature review essay. It is an avenue warrant: a compact,
evidence-cited decision packet that says whether the route deserves broad
investment, a bounded artifact sprint, a gap reframe, a prior-art stop, or
quarantine.

## Mathematical Invariants

Audit the mathematical object or physical object that actually carries the proposed claim, not the rhetoric around it. Preserve the source object, target object, carrier, model or theory, quantifier regime, transfer interface, and claimed novelty delta when comparing the route to closest known results.

The key invariant is non-definitional gap preservation: the target property, physics payoff, or complexity payoff must not be built into a renamed bridge definition. Edge cases and counterexamples include prior-art absorption, proxy shifts, finite-to-global gaps, weak physical carriers, low unification power, and routes whose next step cannot change a decision.

## Epistemic Discipline

Every warrant must state epistemic status, evidence citation, source artifacts, source search provenance, explicit unknowns, and validation handoff. If the literature account is local-only, stale, incomplete, or missing primary sources, mark that limitation rather than treating the gap as established.

Demote, reframe, or quarantine when disconfirming evidence, prior-art collision, low field impact, weak physical relevance, or target-equivalent assumptions make broad investment unjustified.

## Required Reading

Before judging an avenue, read the smallest available target-scoped evidence:

1. Target problem and literature evolution report.
2. Current marathon or result-atlas report for the target.
3. Prior-art, disqualifier, physical-relevance, contribution, or strategy
   reports when present.
4. The branch or proposed avenue text itself.

If only local static sources are available, say so in
`source_search_provenance`. Do not pretend a live external literature search was
performed.

## Audit Questions

Answer these at object level:

1. What is the smallest honest claim?
2. What mathematical or physical object carries the claim?
3. Which target commitments does it touch?
4. What are the closest known results, and what exactly do they not provide?
5. What is the gap statement after accounting for those sources?
6. Why is this not already known, and what would count as a prior-art collision?
7. What field understanding would change if the claim succeeds or fails?
8. What does it unify: constraints, carriers, estimates, representations,
   proof pressures, or route families?
9. What route decision would the next bounded test actually make?
10. What disqualifier would stop, demote, or quarantine the route?

## Decision Standard

Return exactly one investment decision:

- `invest_in_avenue`: only when the warrant has a precise gap, high target
  relevance, field impact, unification power, and route-decision power. Broad
  exploration is allowed.
- `artifact_sprint_only`: the route may be valuable, but only the named finite
  theorem, calculation, falsifier, proof packet, or literature delta should be
  pursued. Broad exploration is blocked.
- `reframe_gap_before_investment`: the idea may matter, but the literature gap,
  novelty boundary, or efficient representation is not yet sharp enough.
- `do_not_invest_prior_art_collision`: closest known results absorb the claimed
  novelty or make the avenue redundant.
- `quarantine_low_relevance`: the route is weakly target-facing, proxy-like,
  purely heuristic, or unlikely to support a major publication.

## Yang-Mills Discipline

For Yang-Mills, do not count local mathematical activity as impact unless it
names a physical carrier and Clay-facing gate:

- physical carrier: gauge-invariant Wilson observable, Schwinger family, OS
  Hilbert observable or excitation sector, Hamiltonian or spectral-measure
  object, or connected-cumulant nontriviality witness;
- target gate: same-theory continuum construction, OS/Wightman reconstruction,
  gauge-invariant observable density, nontriviality, or positive spectral mass
  gap.

Finite endpoint calculations, Schur complements, symbolic identities, or
restricted-model lemmas are support-only unless the warrant states the transfer
condition and field-facing understanding shift.

## P Vs NP Discipline

For P vs NP, require source statement, target statement, model, reduction or
proof-system interface, length/exponent regime, uniformity and advice status,
and barrier status. A route is not novel because it is another possible attack.
Novelty must be a precise bridge theorem, obstruction lemma, parameter
calculation, finite countermodel, or disqualifier test.

## Output Contract

Emit or repair a packet with:

- `target_id`
- `avenue_id`
- `smallest_honest_claim`
- `mathematical_or_physical_object`
- `target_commitments_touched`
- `closest_known_results`
- `source_search_provenance`
- `gap_statement`
- `why_not_already_known`
- `relevance_threshold`
- `physics_or_field_impact`
- `unification_power`
- `route_decision_power`
- `novelty_boundary`
- `disqualifier_matrix`
- `explicit_unknowns`
- `allowed_next_modes`
- `investment_decision`
- `validation_handoff`

Use `agentic/spec/avenue_literature_gap_warrant.schema.json` as the structural
contract and `agentic/scripts/validate_avenue_literature_gap_warrant.py` as the
deterministic gate.

## Anti-Incrementality Rule

Do not recommend broad investment unless the route could plausibly become a
major publication or major route-decision result. If the next useful step is an
appendix-grade calculation, finite table, local proof cleanup, analogy audit, or
literature positioning exercise, choose `artifact_sprint_only` or
`reframe_gap_before_investment`, not `invest_in_avenue`.

## Failure/Demotion

Fail the gate when the avenue cannot name a precise literature gap, mathematical or physical object, closest-known comparator, target-facing consequence, unification gain, route decision, and falsifier. Demote or quarantine when the proposal is incremental, definitional, proxy-like, already absorbed by known results, or not plausibly a major publication pathway.
