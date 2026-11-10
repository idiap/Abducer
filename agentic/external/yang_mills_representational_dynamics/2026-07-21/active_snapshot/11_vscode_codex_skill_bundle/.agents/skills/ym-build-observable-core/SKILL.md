---
name: ym-build-observable-core
description: Define, test, and audit gauge-invariant observable classes for rigorous Yang--Mills construction and mass-gap arguments. Use when choosing Wilson loops, local composite fields, flowed observables, observable nets, or any class claimed to determine states, continuum limits, clustering, or the complete physical spectrum.
---

# Build the Yang--Mills Observable Core

## Workflow

1. Specify the regulated configuration, gauge group action, spacetime localization, and state.
2. Partition candidates into bounded local observables, extended observables, renormalized composites, and auxiliary gauge-dependent quantities.
3. Define support, separation, involution, products, symmetry action, and continuum renormalization for the physical class.
4. Test whether the class separates regulated states and is convergence determining.
5. State the exact cyclicity or spectral-completeness condition required after OS reconstruction.
6. Add observables capable of detecting topological, diffuse, and superselection sectors, or record why they are excluded.
7. Construct a hidden-sector countermodel for every proposed incomplete class.
8. Emit the smallest justified observable core and its unresolved density theorem.

## Control points

- Do not identify gauge potentials with observables.
- Do not infer a full spectral gap from decay of one glueball operator or a finite set of loops.
- Separate point-local composite renormalization from extended-loop renormalization.
- Track observable norms and prefactors uniformly in cutoff and volume.
- Require a dense generated subspace before upgrading correlation decay to spectral exclusion.

## Output contract

Return: typed observable classes; localization rules; state-separation result; convergence criterion; spectral-completeness obligation; renormalization map; counterexamples; and epistemic status. Stop the spectral argument when low-energy sectors may remain invisible.
