---
name: ym-mechanize-proof-core
description: Formalize or execute the finite-dimensional core of Yang--Mills representation composition, error propagation, transfer-semigroup decay, and spectral-gap extraction. Use when theorem dependencies need machine-checked bookkeeping or adversarial finite models, while keeping the unmechanized analytic frontier explicit.
---

# Mechanize Proof Core

## Scope

Mechanize the algebraic and finite spectral lemmas that can be checked independently of the unresolved four-dimensional continuum estimates. Never present a verified finite core as a mechanization of the Clay problem itself.

## Targets

- Typed representation packages and admissible morphism composition.
- Additive or multiplicative approximation-error propagation.
- Finite positive self-adjoint Hamiltonians and vacuum projectors.
- The implication from a spectral lower bound to semigroup correlation decay.
- Finite counterexamples for incomplete observable sectors and nonuniform gap sequences.
- A theorem-dependency graph with machine-readable claim statuses.

## Workflow

1. Freeze conventions and exact finite statements before coding.
2. Prefer a proof assistant when available; otherwise build an executable exact-arithmetic checker and state its weaker epistemic status.
3. Include positive, boundary, and deliberately failing test cases.
4. Verify all artifacts from a clean command and record tool versions.
5. Cross-reference each artifact to the paper theorem it checks.
6. List every analytic hypothesis that remains outside the mechanization: full-measure RG control, continuum compactness, OS axioms, basin entry, or universality.

## Required Tests

Check a gapped diagonal Hamiltonian, a gapless sequence, a hidden gapless direct summand, an invalid signed measure or non-self-adjoint input, and composed morphisms whose error exceeds the allowed budget.

## Output Contract

Return source, tests, reproducible commands, verification output, theorem mapping, and a mechanization boundary statement. Fail closed on invalid positivity, normalization, density, or error-budget inputs.
