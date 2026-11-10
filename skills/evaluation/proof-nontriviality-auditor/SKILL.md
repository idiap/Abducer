---
name: proof-nontriviality-auditor
description: Classify proof objects as load-bearing, support-only, exposition-only, validation-only, blocked, demoted, or quarantined. Use when a theorem-shaped object may be locally valid but strategically shallow.
---

# Proof Nontriviality Auditor

Separate mathematical load from polish, exposition, and artifact hygiene.

## Critical Conceptual Depth

Nontriviality means the result does conceptual work. Look for a changed theorem
body, a removed assumption, a constructed object, a preserved invariant that
was not automatic, a failure mechanism that explains why a route stalls, or a
bridge that lets two regimes communicate without collapsing their differences.

## Value Signal

State how the proof object changes what a reader can understand or prove. Good
signals include a sharper result, a novel obstruction, a unifying mechanism, a
new falsifier, a decisive demotion, or a literature-facing distinction. Weak
signals include cleaner notation, longer derivation, more examples of the same
calculation, or a transfer theorem whose conclusion follows by definition.

## Mathematical Invariants

- Identify the mathematical object under audit: theorem-shaped claim, proof
  object, constructed carrier, transfer bridge, obstruction, or falsifier.
- Audit the theorem body, assumptions, constructed objects, preserved
  invariants, broken invariants, transfer closure, and literature boundary.
- Check edge cases, counterexample classes, and boundary regimes before calling
  a result load-bearing.
- Treat a definitional restatement, notation-preserving translation, or
  conservative unpacking as support-only unless the claim is explicitly
  exposition.

## Epistemic Discipline

- Cite evidence paths, KB ids, proof packets, validator output, and explicit
  unknowns.
- Label epistemic status as load_bearing, support_only, exposition_only,
  validation_only, blocked, demoted, or quarantined.
- Require a `learned_inference_delta`; a valid lemma can still be shallow.

## Output Contract

Return:

- `proof_object`
- `theorem_body_delta`
- `assumption_delta`
- `constructed_object_delta`
- `invariant_delta`
- `falsifier_or_counterexample_delta`
- `transfer_closure_delta`
- `literature_boundary_delta`
- `learned_inference_delta`
- `classification`
- `evidence`
- `validation_handoff`

## Failure/Demotion

Demote polish, restatement, local algebra, validation-only output, or
definition-built transfer claims. Quarantine overclaims that use explanatory or
unification language without naming the mechanism, invariant, cases unified,
or demotion trigger.
