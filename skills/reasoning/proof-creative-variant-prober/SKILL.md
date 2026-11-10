---
name: proof-creative-variant-prober
description: Generate controlled counterfactuals, toy carriers, and definition-variation probes that reveal which assumptions, invariants, or regimes do real proof work. Use when a route has one dominant story and needs diagnostic alternatives.
---

# Proof Creative Variant Prober

Create variants that decide something, not analogies that merely decorate a
route.

## Critical Conceptual Depth

A useful variant isolates the conceptual load-bearing part of the route. It
changes one meaningful feature while holding the theorem's intended pressure
fixed, so the outcome teaches which invariant, hypothesis, or obstruction is
doing real work.

## Value Signal

State what the variant teaches if it succeeds and if it fails. A valuable
variant should reveal a mechanism, falsifier, boundary, unifying principle, or
repair path. A low-value variant only shows that an analogy can be retold in
another notation.

## Mathematical Invariants

- Specify the varied variable, held-fixed controls, preserved invariants,
  broken invariants, transfer boundary, and target theorem relation.
- Include an edge case, counterexample, or failure regime for each variant.
- Add definitional-collapse probes by weakening or varying bridge definitions
  to test whether a transfer theorem has independent content.

## Epistemic Discipline

- Cite evidence paths, KB ids, cycle ids, source artifacts, and explicit
  unknowns.
- Mark each variant as conjectural, proof-obligation, promoted, demoted,
  blocked, refuted, or quarantined.
- Do not change multiple conditions at once unless the output declares the
  confounding risk.

## Output Contract

Return:

- `variant_id`
- `varied_variable`
- `held_fixed_controls`
- `predicted_observation`
- `disconfirming_observation`
- `preserved_invariants`
- `broken_invariants`
- `edge_case_or_counterexample`
- `transfer_boundary`
- `decision_value`
- `evidence`
- `validation_handoff`

## Failure/Demotion

Demote variants that cannot affect route ranking, lack controls, lack a
disconfirming observation, or never transfer back to the target proof.
Quarantine variants that solve a proxy problem while presenting themselves as
target evidence.
