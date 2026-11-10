---
name: dimensional-symmetry-constraint-checker
description: Check qualitative physics relation claims against dimensions, scaling, symmetry, conservation, positivity, convexity, boundedness, and invariance. Use when a variable relation, monotonicity claim, asymptotic claim, or transfer claim may be physically impossible or underconstrained.
---

# Dimensional Symmetry Constraint Checker

## Conceptual Role

Use this skill as a hard plausibility filter before a qualitative relation is promoted. It asks whether the proposed relation is even compatible with dimensions, scaling, symmetries, conservation laws, positivity, convexity, boundedness, or invariance.

This is evaluative reasoning, not style review. Actively try to break the relation by applying constraints the generative step may have missed.

## Procedure

1. Restate the mathematical object, source variable, target variable, regime, and claimed relation.
2. Check units or scaling dimensions for every term and parameter.
3. Check symmetry and invariance: gauge invariance, translation/rotation, parity, time reversal, boundary invariance, or problem-specific transformations.
4. Check conservation, normalization, positivity, convexity, spectral support, boundedness, and monotonicity constraints.
5. Identify whether the relation uses a variable that cannot change independently because of a constraint.
6. Produce a verdict: pass, needs retyping, needs regime split, challenged, invalidated, or proof obligation.
7. Convert failures into graph challenges, falsifiers, or queue tasks.

## Mathematical Invariants

- Mathematical object: relation claim, variables, units, symmetries, conserved quantities, positivity cone, and valid regime.
- Preserved invariants: dimensional consistency, transformation behavior, conservation, positivity, boundedness, and source/target typing.
- Broken invariants: dimension mismatch, symmetry-violating observable, impossible sign, missing normalization, or hidden constrained variation.
- Edge case or counterexample: a relation may pass dimensions but fail under symmetry or positivity; do not treat one constraint family as sufficient.

## Epistemic Discipline

Assign epistemic status: `constraint_passed`, `needs_retyping`, `regime_split_required`, `challenged`, `invalidated`, `explicit_unknown`, or `proof_obligation`. Cite evidence paths, equations, KB IDs, cycle IDs, source artifacts, validators, or explicit unknowns.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when a deterministic check can ground the critique. For generated graph updates, run the qualitative validators and inspect whether challenged edges keep their epistemic status.

## Output Contract

Return:

1. `Claim Under Test`: relation, variables, regime, and source.
2. `Dimensional Check`: units, scaling dimensions, and mismatches.
3. `Symmetry/Invariance Check`: transformations preserved or violated.
4. `Constraint Check`: conservation, positivity, convexity, boundedness, and normalization.
5. `Verdict`: pass, challenged, invalidated, retype, split regime, or proof obligation.
6. `Failure Modes`: counterexamples, impossible signs, missing invariants, or proxy shifts.
7. `Validation Handoff`: graph challenge, relation packet, falsifier, queue item, or validator.

## Failure/Demotion

Demote claims that fail dimensions, violate symmetry, ignore conservation, or use an impossible sign. Quarantine if the relation can only be made valid by changing the mathematical object or target observable.

## Validation Handoff

Use `python agentic/scripts/validate_qualitative_relation_packets.py`, `python agentic/scripts/build_qualitative_mechanistic_graph.py --target <target>`, and `python agentic/scripts/validate_qualitative_mechanistic_graph.py` after constraint-driven graph changes.
