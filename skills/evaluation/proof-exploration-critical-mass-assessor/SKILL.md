---
name: proof-exploration-critical-mass-assessor
description: Decide whether exploratory proof cycles have enough target-scoped learning to lock into a bounded publication subgoal, continue exploring, demote, or block. Use when a route risks endless exploration or premature commitment.
---

# Proof Exploration Critical Mass Assessor

Decide when exploration has earned a temporary lock-in.

## Critical Conceptual Depth

Critical mass exists only when exploration has converged on a meaningful
conceptual object: a hard gate, bridge, invariant, falsifier, obstruction, or
smallest honest theorem. Do not lock in because there are many cycles; lock in
because the accumulated learning now identifies a finite subgoal with real
mathematical pressure.

## Value Signal

State why the locked subgoal would be worth a paper or serious handoff. The
subgoal should be sharp, novel relative to its boundary, explanatory or
unifying, and honest about non-claims. If it would only package a fragmented
ensemble of minor lemmas, continue exploration or demote.

## Mathematical Invariants

- Identify the mathematical object around which exploration has converged:
  hard gate, bridge, invariant, falsifier, obstruction, or smallest honest
  theorem.
- Inspect repeated pressure, named hard gates, candidate objects, invariants,
  falsifiers, required certificates, and boundary regimes.
- Require edge cases, counterexamples, or failure regimes that rule out shallow
  variants.
- Refuse lock-in when the principal theorem is a transfer theorem that fails
  transfer-substance audit.

## Epistemic Discipline

- Cite learning-ledger paths, evidence artifacts, KB ids, cycle ids,
  validators, and explicit unknowns.
- Label outcome as exploration_continue, lock_in_ready, premature_lockin,
  forced_demote, blocked, or quarantined.
- Treat a smallest honest publication subgoal as valid without implying the
  main problem is solved.

## Output Contract

Return:

- `target_id`
- `mode_decision`
- `smallest_publication_subgoal`
- `repeated_pressure`
- `candidate_object_or_falsifier`
- `negative_learning_summary`
- `conceptual_quality_basis`
- `transfer_substance_status`
- `cycle_budget`
- `stop_condition`
- `non_claims`
- `evidence`
- `validation_handoff`

## Failure/Demotion

Demote lock-in candidates with no publishable subgoal, low explanatory or
unification value, failed transfer-substance audit, or no stop condition.
Quarantine premature lock-in that hides uncertainty or main-problem overclaim.
