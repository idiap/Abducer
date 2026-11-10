---
name: proof-hard-gate-selector
description: Select the single decisive hard gate a proof cycle must attack and define how success, failure, or demotion changes the proof state. Use after a proof-depth pressure packet exists.
---

# Proof Hard Gate Selector

Force each queued cycle to name the bottleneck it can actually move.

## Critical Conceptual Depth

A hard gate is not merely the next missing step. It is the place where the
proof's core concept is under strain: carrier transparency, normalization,
uniformity, geometric realization, barrier specificity, or semantic transfer.
Select the gate whose resolution would reorganize the route, not the gate that
would produce the most convenient next artifact.

## Value Signal

For the selected gate, state the value of a positive and negative outcome. A
positive outcome should unlock a sharper theorem, new bridge, publication
subgoal, or genuine transfer certificate. A negative outcome should collapse a
branch, identify a falsifier, or create reusable learning that prevents future
loops.

## Guardrails

- Do not select a gate just because it is easiest to work on.
- Do not allow broad goals such as "improve the proof" or "explore route" to
  stand as gates.
- Reject cycles whose output cannot affect a target commitment, proof
  obligation, or learning-ledger rule.
- Route close-to-definitional transfer claims to an anti-definitionality gate
  before proof writing.

## Epistemic Discipline

- Cite source artifacts, KB ids, cycle ids, and explicit unknowns for the
  selected and rejected gates.
- Label the selected gate as proof-obligation, blocked, conjectural, promoted,
  demoted, or quarantined.
- Preserve the difference between workflow validity and mathematical progress.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the gate:
inspect relevant reports, run deterministic validators when available, and
interpret executed commands as evidence rather than as automatic progress.

## Output Contract

Return:

- `selected_gate`
- `rejected_gates`
- `mathematical_invariant_at_stake`
- `gate_movement_test`
- `inference_to_learn`
- `promotion_test`
- `pivot_test`
- `next_experiment`
- `evidence`
- `validation_handoff`

## Failure/Demotion

Demote gate selections with no hard-gate movement test, no declared invariant,
or no future routing effect. Quarantine any selection that silently changes
the model, representation, regulator, complexity class, or semantic regime.
