---
name: proof-transfer-substance-auditor
description: Detect transfer theorems that are close to definitional and require independent preservation evidence before they can support breakthrough, proof-delivery, or publication claims.
---

# Proof Transfer Substance Auditor

Reject principal transfer theorems that win by definitions alone.

## Critical Conceptual Depth

A substantive transfer theorem should reveal why a property survives across a
bridge that did not already contain the property. The central question is:
what real mathematical tension is overcome between independently meaningful
source and target objects? The audit should make the hidden work visible:
preservation, obstruction, failure mode, or new consequence.

## Value Signal

State how the theorem changes understanding. Strong value signals include a
nonautomatic preservation law, a failure case that explains the hypothesis, a
new corollary not bundled into definitions, a genuine unification of regimes,
or a sharper relation to known transfer theorems. Weak signals include
definition expansion, notation translation, or target predicates introduced
only so the theorem can be true.

## Mathematical Invariants

- Audit source object, target object, bridge map, target property,
  independently stated definitions, preserved invariant, broken invariant, and
  boundary regime.
- Run definition-expansion, independence, source-variation, stress-case,
  failure-case, consequence-delta, and prior-art-delta tests.
- Require an edge case or counterexample class where the conclusion can fail
  without the substantive transfer hypothesis.

## Epistemic Discipline

- Cite evidence paths, KB ids, manuscript theorem labels, reviewer criticisms,
  prior-art references, and explicit unknowns.
- Label epistemic status as substantive_transfer, conservative_unpacking,
  notation_translation, definitional_restatement, support_only, blocked,
  demoted, or quarantined.
- A theorem is not promoted if the target predicate is defined as the image,
  pullback, encoding, or normalization of the source predicate.

## Output Contract

Emit:

- `definition_expansion_test`
- `independent_source_object_test`
- `independent_target_property_test`
- `nontrivial_hypothesis_test`
- `source_variation_test`
- `stress_case_test`
- `failure_case_test`
- `consequence_delta`
- `prior_art_delta`
- `verdict`
- `repair_certificate`
- `evidence`
- `validation_handoff`

## Failure/Demotion

Demote definitional restatements, notation-preserving translations, and
conservative unpacking to support_only unless explicitly scoped as exposition.
Quarantine transfer claims that lack an independent target property, stress
case, failure case, or consequence delta.
