---
name: ym-define-relational-rigidity
description: Define and audit regulator-independent infrared rigidity witnesses for constructive Yang--Mills work. Use when translating cutoff correlation decay, transfer-operator estimates, or RG contraction into a candidate physical mass-gap statement, especially when cutoff, volume, observable, normalization, and uniformity quantifiers must be made explicit.
---

# Define Relational Rigidity

## Objective

Formulate a noncircular property that can be verified at regulated scales and transferred across representations without already assuming a continuum mass gap. Treat rigidity as a family of quantitative relations among physical observables, states, scales, and representation maps.

## Required Inputs

- A regulator family indexed by cutoff `a`, volume `L`, and bare or running parameters.
- A specified gauge-invariant observable class and its physical normalization.
- The relevant physical distance or Euclidean time variable.
- The representation maps that compare scales or regulators.
- A declared target: clustering, transfer-spectrum exclusion, or Hamiltonian spectral exclusion.

## Workflow

1. Write every quantifier in the order actually needed: observable, cutoff, volume, separation, and limiting sequence.
2. Express decay rates in physical units. Never infer a continuum gap from a positive number measured only in lattice units.
3. Separate temporal correlation estimates, spatial clustering, transfer-operator estimates, and auxiliary stochastic mixing estimates.
4. State which observables separate the reconstructed physical Hilbert space. If they do not, label the witness sectorial.
5. Require constants and prefactors to be uniform in volume and sufficiently small cutoff after renormalized normalization.
6. Record stability under the approved representation morphisms, including accumulated approximation errors.
7. Test the definition against the false-positive bank before using it in a theorem.

## Canonical Witness

A useful template is uniform physical relational rigidity: there exist physical constants `m>0`, `a_0>0`, and controlled seminorms `N_a` such that for all `a<a_0`, all sufficiently large volumes, and all centered observables in a state-separating class,

`|<A tau_t(B)>_c| <= C N_a(A) N_a(B) exp(-m t) + epsilon_a(A,B,t)`,

where `t` is physical Euclidean time, the prefactor is uniform in volume, and the error vanishes in the declared continuum topology. Specify whether the estimate is pointwise, distributional, or smeared.

## False-Positive Tests

- **Finite-volume discreteness:** a finite box has a discrete spectrum even when the infinite-volume theory is gapless.
- **Lattice-unit collapse:** a cutoff gap `delta_a` with `delta_a/a -> 0` does not produce a positive physical gap.
- **Incomplete observables:** exponential decay in one sector can hide a gapless orthogonal sector.
- **Stochastic confusion:** a Poincare or log-Sobolev gap for a sampling dynamics is not automatically the quantum Hamiltonian gap.
- **Circular clustering:** a basin or rigidity definition that assumes the desired physical exponential clustering proves nothing new.
- **Uncontrolled prefactors:** exponentially growing constants can destroy the claimed decay after limits.

## Output Contract

Return:

- the exact rigidity predicate with all parameters and quantifiers;
- the observable-completeness requirement;
- physical-unit normalization;
- allowed morphisms and error budgets;
- the false-positive tests passed or failed;
- the strongest justified claim level.

Do not call the witness a Yang--Mills mass gap until continuum existence, Osterwalder--Schrader reconstruction, and physical-state completeness have also been established.
