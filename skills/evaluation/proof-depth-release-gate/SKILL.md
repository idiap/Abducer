---
name: proof-depth-release-gate
description: Decide whether a proof cycle should be promoted, retained as support, demoted, quarantined, sent to proof delivery, locked into a publication subgoal, pivoted, or stopped. Use after pressure, gate, nontriviality, conceptual-quality, and transfer audits exist.
---

# Proof Depth Release Gate

Release only cycles that changed a hard gate or produced useful negative
learning.

## Critical Conceptual Depth

Release decisions must ask whether the cycle changed the conceptual topology
of the route. Promotion requires movement in a hard gate, a new mechanism, a
load-bearing object, a nontrivial transfer, a real obstruction, or a learning
event that prevents future shallow loops.

## Value Signal

State why the released result deserves its status. A promoted cycle should
explain how understanding changed; a support-only cycle should say what it
supports without inflating the claim; a demoted cycle should say what the
system learned by rejecting it.

## Mathematical Invariants

- Identify the mathematical object whose status is being released: theorem
  candidate, proof packet, obstruction, carrier, bridge, or falsifier.
- Inspect theorem body, target commitment, hard gate, preserved invariants,
  broken invariants, same-domain status, and transfer-substance verdict.
- Require edge cases, counterexamples, or failure regimes for theorem-shaped
  promotions and transfer claims.
- Keep support-only calculations visible without inflating breakthrough or
  paper-readiness claims.

## Epistemic Discipline

- Cite evidence paths, KB ids, validators, cycle ids, and explicit unknowns.
- Label status as promote, support_only, lock_in_candidate, demote,
  quarantine, proof_delivery, pivot, or stop.
- Forbid breakthrough language if no hard gate changed or if a principal
  transfer theorem failed anti-definitionality tests.

## Output Contract

Return:

- `pressure_packet`
- `selected_hard_gate`
- `nontriviality_audit`
- `conceptual_quality_vector`
- `transfer_substance_audit`
- `same_domain_transfer_audit`
- `release_decision`
- `reasons`
- `next_consumer_skill`
- `evidence`
- `validation_handoff`

## Failure/Demotion

Demote workflow activity, exposition, validation-only artifacts, or
definition-built principal transfer theorems. Quarantine overclaims that lack
evidence, hard-gate movement, or a named repair certificate.
