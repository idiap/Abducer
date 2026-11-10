---
name: ym-reconstruct-os-gap
description: Apply and audit Osterwalder--Schrader reconstruction for gauge-invariant continuum Yang--Mills data and derive the exact Hamiltonian spectral conclusion from positive Euclidean correlations. Use when a continuum Euclidean construction must become a physical Hilbert space with vacuum, positive energy, and a mass gap.
---

# Reconstruct OS Gap

## Objective

Recover the physical Hilbert space, vacuum, Euclidean time semigroup, Hamiltonian, and spectrum, then translate uniform temporal rigidity into a gap above the vacuum.

## Workflow

1. Verify the precise OS axioms and regularity assumptions for the declared gauge-invariant Schwinger functions.
2. Form the positive-time pre-Hilbert space, quotient its null vectors, and complete it.
3. Construct translations and the contraction semigroup; identify its positive self-adjoint generator `H`.
4. Establish the vacuum vector and prove uniqueness when required.
5. Prove that the chosen observable core is dense in the reconstructed physical space.
6. Apply the positive spectral-measure lemma to exclude spectrum in `(0,m)` from uniform temporal correlation decay.
7. Establish the presence of a finite-energy nonvacuum state or nonempty spectrum above the gap if the target formulation requires it.
8. State separately any results about confinement, particle poles, isolated one-particle states, or scattering. None follows merely from a spectral gap.

## Audit Points

- Positivity is reflection positivity, not positivity of the Euclidean action alone.
- Spatial clustering does not replace temporal semigroup control without an additional theorem.
- A gap seen by an incomplete observable sector is only sectorial.
- Vacuum degeneracy changes the spectral statement.
- The mass gap does not by itself identify particles or prove confinement.

## Output Contract

Return the reconstructed objects, axiom-to-construction dependency map, density proof status, spectral-measure argument, precise spectrum inclusion, and any nonemptiness or uniqueness assumptions. Stop at a conditional OS-gap theorem if an axiom, density statement, or continuum estimate is missing.
