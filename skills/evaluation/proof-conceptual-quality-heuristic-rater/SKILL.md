---
name: proof-conceptual-quality-heuristic-rater
description: Rate proof cycles for conceptual depth, explanatory power, unification power, mechanism specificity, compression, generativity, transfer reach, falsifiability, boundary sharpness, and literature displacement. Use when judging discovery quality without treating heuristics as proof.
---

# Proof Conceptual Quality Heuristic Rater

Score conceptual quality with evidence and demotion triggers.

## Critical Conceptual Depth

Judge whether the cycle touches the root tension of the proof rather than a
surface artifact. High depth requires a mechanism, invariant, obstruction, or
bridge that explains why the problem was hard in the first place. Depth is not
length, technical density, or successful formatting.

## Value Signal

For every score, state the value claim it supports: new understanding,
explanatory compression, unification of formerly separate cases, sharper
boundary, literature displacement, or generative next obligations. Penalize
results that are correct but do not change what can be understood, proved,
falsified, or compared to the literature.

## Mathematical Invariants

- Identify the mathematical object, definitions, mechanism, mediator,
  enabling condition, preserved invariants, broken invariants, and boundary
  regime.
- Require edge cases, counterexamples, falsifiers, or failure regimes for
  falsifiability and boundary sharpness.
- Cap transfer reach, explanatory power, unification power, and literature
  displacement if transfer-substance audit fails.

## Epistemic Discipline

- Cite evidence paths, KB ids, proof packets, prior-art anchors, and explicit
  unknowns for every score.
- Label each dimension as evidence-backed, conjectural, proof-obligation,
  blocked, demoted, or quarantined.
- Heuristic scores guide search, lock-in, or demotion; they never substitute
  for proof or transfer certificates.

## Output Contract

Emit one vector with these dimensions:

- `conceptual_depth`
- `explanatory_power`
- `unification_power`
- `mechanism_specificity`
- `compression`
- `generativity`
- `transfer_reach`
- `falsifiability`
- `boundary_sharpness`
- `literature_displacement`

For each dimension return `score`, `evidence`, `missing_evidence`, `scope`, and
`demotion_trigger`, followed by `overall_use` and `validation_handoff`.

## Failure/Demotion

Demote elegant prose without mechanism, invariant, falsifier, or case
unification. Quarantine any high score used as proof authority or any
unification claim that hides object mismatch or transfer failure.
