---
name: proof-learning-ledger-maintainer
description: Maintain append-only, target-scoped proof learning ledgers from validated inference events. Use when conceptual learning must affect later queueing, demotion, lock-in, or report decisions.
---

# Proof Learning Ledger Maintainer

Keep proof learning as reusable state, not just prose inside reports.

## Critical Conceptual Depth

The ledger should preserve conceptual structure, not just chronology. Each
stored rule should say which object, invariant, mechanism, transfer, or
barrier was learned and why that learning changes future proof search.

## Value Signal

Mark whether each ledger entry has discovery value, publication-subgoal value,
demotion value, or routing value. Entries with no effect on future branch
selection, proof obligations, or claim boundaries should stay out of the
promoted ledger.

## Mathematical Invariants

- Preserve each event's mathematical object, premises, scope condition,
  invariant, broken invariant, boundary regime, and repair certificate.
- Store edge cases, counterexamples, failure regimes, and transfer-substance
  failures as first-class ledger material.
- Keep Yang-Mills, P vs NP, and other targets in separate target-scoped paths.

## Epistemic Discipline

- Cite evidence paths, KB ids, cycle ids, validators, and explicit unknowns.
- Label events as learned_rule, unresolved_question, demoted_generalization,
  required_certificate, branch_routing_rule, blocked, refuted, or quarantined.
- Deduplicate repeated claims while preserving distinct premise/scope pairs.

## Output Contract

Return:

- `target_id`
- `ledger_path`
- `events_added`
- `events_deduplicated`
- `transfer_substance_rules`
- `branch_routing_rules`
- `required_certificates`
- `demoted_generalizations`
- `evidence`
- `validation_handoff`

## Failure/Demotion

Demote ledger updates that merge targets, overwrite prior events, store
chronology instead of inference rules, or cannot affect future queueing.
Quarantine events with no evidence path or scope condition.
