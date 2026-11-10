---
name: ym-prove-rg-to-rigidity
description: Prove or audit a quantitative implication from membership in a noncircular Yang--Mills infrared RG basin to uniform physical correlation rigidity. Use when local mixing, polymer contraction, or effective-theory coercivity must be iterated and pulled back to the original gauge-invariant observables.
---

# Prove RG to Rigidity

## Goal

Derive exponential decay in physical distance or Euclidean time from explicit finite-scale basin data. Keep this theorem logically separate from the claim that four-dimensional Yang--Mills enters the basin.

## Workflow

1. Freeze the basin predicate and its one-step contraction factor, stability radius, and norm.
2. Iterate the contraction with exact scale bookkeeping and prove summability of nonlinear remainders.
3. Transport observables through the RG dual maps, including support growth and renormalization factors.
4. Bound correlations of separated observables after enough blocking steps to make their effective supports local.
5. Pull the bound back to the original representation and express the rate as `m_phys = c/ell_*`, where `ell_*` is a physical entry or mixing scale and `c>0` follows from the contraction theorem.
6. Prove prefactor and rate uniformity in volume and cutoff.
7. Distinguish spatial clustering, temporal clustering, transfer-spectrum contraction, and mixing of an auxiliary Markov process.
8. Verify that approximation errors remain smaller than the exponential term on the time scales used later for spectral extraction.

## Required Conclusion

State the observable class, topology, and exact estimate. If temporal reflection-positive correlations are not controlled, do not claim a Hamiltonian gap. If the proof concerns a Langevin generator, report only stochastic mixing unless an independent comparison theorem is supplied.

## Output Contract

Return the iteration lemma, observable pullback theorem, physical rate formula, volume/cutoff uniformity proof, error ledger, and the precise rigidity predicate obtained. Mark the result conditional on basin membership unless basin entry has been proved separately.
