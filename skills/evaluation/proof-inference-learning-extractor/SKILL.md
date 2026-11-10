---
name: proof-inference-learning-extractor
description: Convert proof-cycle outputs into declarative inference-level learning events for target-scoped ledgers. Use when a cycle must teach reusable premises, constraints, demotions, or routing rules rather than only narrative lessons.
---

# Proof Inference Learning Extractor

Make conceptual learning cumulative and queryable.

## Critical Conceptual Depth

Extract the inference that changes the proof search state. The best learning
events identify why an attempted move succeeded or failed at the level of
mechanism, invariant, object, transfer, barrier, or boundary condition. Avoid
learning entries that merely summarize activity.

## Value Signal

For each event, state its future value: what it routes away from, what it makes
newly plausible, what it forbids, what certificate it demands, or what
publication subgoal it enables. Negative learning is valuable when it prevents
the system from repeating a shallow theorem-shaped loop.

## Mathematical Invariants

- Record the mathematical object, premises, attempted inference, preserved
  invariants, broken invariants, scope condition, and boundary regime.
- Include failed transfers, missing objects, false analogies, blocked
  normalizations, counterexamples, and demoted local calculations.
- Record definitional transfer collapse as a reusable inference rule with a
  repair condition.

## Epistemic Discipline

- Cite evidence paths, KB ids, cycle ids, proof packets, validator output, and
  explicit unknowns.
- Label learning as learned_rule, unresolved_question, demoted_generalization,
  required_certificate, branch_routing_rule, blocked, refuted, or quarantined.
- Do not record action items as learning evidence; an action is not an
  inference.

## Output Contract

Return one or more learning events with:

- `source_cycle_id`
- `premises_used`
- `attempted_inference`
- `observed_result`
- `learned_constraint`
- `scope_condition`
- `invalidated_generalization`
- `future_routing_effect`
- `epistemic_status`
- `evidence`
- `validation_handoff`

## Failure/Demotion

Demote summaries that only say the branch made progress, sharpened
understanding, or needs more work. Quarantine learning events that erase scope
conditions and therefore overgeneralize a local lesson.
