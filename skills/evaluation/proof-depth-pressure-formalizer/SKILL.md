---
name: proof-depth-pressure-formalizer
description: Convert stalled proof routes, repeated branch patterns, referee criticisms, or weak result ensembles into typed proof-depth pressure packets. Use when a cycle may be locally valid but not attacking the decisive mathematical tension.
---

# Proof Depth Pressure Formalizer

Turn unease about a proof route into a decision-valued pressure packet before
another cycle is queued.

## Critical Conceptual Depth

Pressure is deep when it names the conceptual tension that makes the route
interesting: an object cannot yet exist, an invariant is missing, a transfer
law is not yet justified, a bridge would change the meaning of the target, or
a known barrier is being approached without the right interface. Do not merely
label the route as hard. Explain why the current proof architecture cannot
advance until this pressure is resolved.

## Value Signal

State what would become newly understandable if the pressure were resolved:
which theorem body would sharpen, which assumption would disappear, which
bridge would become legitimate, which family of failures would unify, or which
literature boundary would move. If the pressure has no such value signal,
demote it to local workflow maintenance.

## Mathematical Invariants

- Treat the mathematical object as the active theorem body plus its missing
  carrier, normalization, reduction, invariant, or transfer law.
- Name preserved invariants and broken invariants separately: model,
  regulator, representation, quantifier discipline, positivity, uniformity,
  semantics, or boundary regime.
- Include at least one edge case, counterexample class, or failure regime that
  would make the pressure concrete.

## Epistemic Discipline

- Cite evidence paths, KB ids, report cycle ids, reviewer comments, explicit
  unknowns, or validator output for every pressure claim.
- Label pressure as proof-obligation, blocked, conjectural, promoted,
  demoted, or quarantined; never call a route deep merely because it is hard.
- Emit `definitional_collapse` pressure when a principal theorem may follow by
  definition expansion, notation change, or target predicates built into a
  bridge.

## Output Contract

Return:

- `pressure_kind`: object_mismatch, hidden_normalization,
  missing_construction, weak_invariant, transfer_failure, circularity,
  definitional_collapse, barrier_mismatch, boundary_regime_instability, or
  literature_displacement.
- `target_commitment`: the theorem, subgoal, or paper claim under pressure.
- `missing_object`: the carrier, map, invariant, certificate, or falsifier not
  yet available.
- `decision_value`: how resolving the pressure changes route selection.
- `inference_question`: the exact yes/no or typed inference the next cycle must
  decide.
- `evidence`: artifact paths and explicit unknowns.
- `validation_handoff`: next validator, auditor, or queue item.

## Failure/Demotion

Demote pressure packets that only say "do deeper work", lack evidence, lack a
decision-valued inference question, or collapse several unrelated tensions into
one vague label. Quarantine packets that hide a target change or overclaim
mathematical progress.
