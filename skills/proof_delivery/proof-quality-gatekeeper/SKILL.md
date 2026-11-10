---
name: proof-quality-gatekeeper
description: Gate proof packets before they are promoted into a report, paper, result-elaboration artifact, or accepted queue completion. Use when a proof-delivery artifact must be checked for definition completeness, quantifier discipline, model preservation, lemma validity, counterexample coverage, inference-quality review, novelty boundary, and paper-ready non-claims.
---

# Proof Quality Gatekeeper

## Role

Use this skill as the final proof promotion gate. A passing report validator is not enough; the proof packet must be mathematically coherent and honestly scoped.

## Mathematical Invariants

Check that the promoted mathematical object is exactly the one proved: theorem statement, definitions, assumptions, quantifiers, model, validity regime, parameters, and proof dependencies must match the proof packet. The invariant is no theorem inflation: examples, definitions, heuristics, analogies, or artifact formatting cannot be promoted as substantive proof.

Gate every edge case and counterexample obligation. A proof cannot pass if boundary regimes, hidden model switches, prior-art collisions, target-equivalent assumptions, or countermodels remain unresolved.

## Epistemic Discipline

Return a precise epistemic status for each claim: `approve_proof`, `approve_conditional_theorem`, `request_repair`, `request_countermodel`, `request_prior_art`, or `quarantine_overclaim`. Require evidence citation to source artifacts, KB IDs, literature-gap warrants, reviewer packets, and validator outputs.

The validation handoff must say which report, paper section, theorem label, or queue item may be updated and which claims remain blocked. Disconfirming evidence or missing novelty/physical relevance requires demotion, not a softer wording of the same overclaim.

## Gate Criteria

Approve only if the proof packet has:

- a theorem statement with source object, target object, and validity regime;
- definitions for all nonstandard objects and parameters;
- explicit assumptions and non-claims;
- a lemma chain with statuses and dependencies;
- proof steps that preserve implication direction and quantifiers;
- edge-case or countermodel checks;
- inference-quality reviewer findings where domain-specific reviewers exist;
- a paper/report insertion target;
- a precise epistemic status.

## Decisions

Use:

- `approve_proof`
- `approve_conditional_theorem`
- `request_repair`
- `request_countermodel`
- `request_prior_art`
- `quarantine_overclaim`

## Output Contract

Return:

1. `Gate Decision`
2. `Accepted Claims`
3. `Rejected Or Overstated Claims`
4. `Required Repairs`
5. `Reviewer Handoffs`
6. `Paper/Report Handoff`
7. `Residual Risk`

## Failure/Demotion

Reject proof packets that are mostly narrative, rely on target-equivalent assumptions, omit countermodel checks, hide advice/model switches, or claim novelty before closest-comparator review.
