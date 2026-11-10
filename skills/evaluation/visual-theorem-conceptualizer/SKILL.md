---
name: visual-theorem-conceptualizer
description: Explain theorems, proof routes, obstructions, and scientific concepts with property-preserving visual metaphors. Use when a deep reflection cycle needs a theorem-level analogy that names the main objects, key properties, physical carrier, proof pressure, distortions, and hypothesis-generating consequences.
---

# Visual Theorem Conceptualizer

Use this skill to turn a theorem, concept, obstruction, or proof route into a disciplined visual metaphor. The metaphor is useful only if it preserves named properties and creates a route consequence.

## Mathematical Invariants

Start from the mathematical object, not from imagery: formal focus, source object, target object, carrier, maps, invariants, symmetries, sign/positivity structure, locality/globality, limit order, physical carrier, and proof obligation. The metaphor is allowed only after those invariants are visible.

Required edge cases and counterexamples include proxy shifts, finite-to-global gaps, hidden regularity, noncommuting limits, singular endpoint behavior, loss of gauge/equivalence structure, and metaphors whose visual smoothness overstates proof force.

## Epistemic Discipline

Every conceptualization must assign epistemic status, evidence citation, source artifacts, explicit unknowns, and validation handoff. Label the output as `explanation_only`, `hypothesis_seed`, `requires_preservation_audit`, or `quarantine`; do not treat a visual metaphor as proof evidence.

Disconfirming distortions or missing preservation data must route the metaphor to `visual-analogy-preservation-auditor` before it can influence branch selection, publication claims, or proof-search priorities.

## Workflow

1. Identify the formal object before proposing imagery:
   - statement or concept
   - source object and target object
   - maps, carriers, witnesses, and observables
   - invariants, symmetries, sign or positivity structure
   - locality/globality and limiting behavior
   - proof obligation or obstruction
   - physical meaning and non-claim boundary when the target is physical

2. Choose a metaphor family only after the property inventory is visible:
   - `landscape`: energy barriers, basins, minima, saddles
   - `flow`: renormalization, transport, monotonicity, leakage, bottlenecks
   - `bridge`: transfer, functoriality, preservation, missing load-bearing beams
   - `lens`: projection, loss of information, coarse graining, distortion
   - `fiber`: base/fiber separation, gauge freedom, holonomy, local trivialization
   - `scaffold`: staged proof obligations, dependency support, missing columns
   - `tension_field`: incompatible commitments, force balance, stress concentration
   - `resonance`: spectral response, mode separation, gap, decay

3. Emit a property-preservation table. Include each relevant property with:
   - formal property
   - visual counterpart
   - preservation verdict: `preserved`, `partially_preserved`, `distorted`, or `absent`
   - why the mapping is faithful or dangerous

4. Emit a distortion ledger:
   - what the image hides
   - what it makes too easy
   - which proxy shift it might encourage
   - which limit, sign, or physical-carrier issue it could obscure

5. Test whether the analogy inspires new work:
   - new hypothesis
   - route mutation
   - missing artifact
   - falsifier
   - counterfactual variant
   - representation requirement

6. Assign a cautious status:
   - `explanation_only`
   - `hypothesis_seed`
   - `requires_preservation_audit`
   - `quarantine`

## Output Contract

Return a `visual_conceptualization` object with:

- `target_id`
- `source_context`
- `formal_focus`
- `main_concepts`
- `key_properties`
- `visual_metaphor`
- `property_preservation_table`
- `distortion_ledger`
- `hypothesis_inspiration`
- `non_claim_boundary`
- `recommended_audit`

## Guardrails

- Do not treat analogy as proof evidence.
- Do not introduce a metaphor that changes the theory, observable family, regulator, carrier, or complexity model without naming the proxy shift.
- For Yang-Mills, name the physical carrier: Wilson loop, Schwinger family, OS Hilbert object, spectral object, gauge-invariant observable, cumulant witness, or explicit absence.
- A metaphor that cannot produce a falsifier, missing artifact, route mutation, or representation requirement remains explanation-only.

## Failure/Demotion

Demote visualizations that only decorate a theorem, omit key properties, lack validation handoff, or fail to preserve the mathematical object. Quarantine metaphors that hide counterexamples, collapse source and target, erase physical relevance, or generate unsupported route claims.
