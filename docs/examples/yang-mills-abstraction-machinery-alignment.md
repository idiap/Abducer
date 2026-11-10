<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Yang-Mills Abstraction Machinery Alignment

This document is an illustrative target-led example. The universal machinery taxonomy lives in `docs/research-methods/abstraction-machinery-selection-policy.md`; Yang-Mills supplies one demanding instantiation through the active target ledger.

## Exact Target Object

The target is a nontrivial four-dimensional quantum Yang-Mills theory on R^4 for a compact simple gauge group, satisfying OS/Wightman adequacy and a strictly positive Hamiltonian mass gap in the reconstructed physical theory.

## Universal Roles As Yang-Mills Machinery

| Universal role | Yang-Mills example | Useful role | Premature use | Validation obligation |
| --- | --- | --- | --- | --- |
| `construction` | Balaban/RG and multiscale control | Build regulated gauge-field objects and control cutoff removal toward continuum Schwinger functions. | Treat ultraviolet stability or finite-volume control as a mass-gap proof. | RG-to-Schwinger bridge with limiting topology, reflection positivity preservation, and nontriviality witness. |
| `representation` | Gauge-invariant Schwinger functions | Give Euclidean Yang-Mills data a form on which OS reconstruction and correlator decay can act. | Use generic QFT notation without identifying observables or the limiting object. | Schwinger-function packet with gauge-invariant observable family and OS axiom targets. |
| `invariant_preservation` | Gauge invariance, OS positivity, nontriviality, same-theory identity | Keep the target unchanged across regulators, limits, reconstruction, and spectral statements. | Combine construction, nontriviality, and gap witnesses from different approximations. | Same-theory table for object, observable algebra, reconstruction output, and gap witness. |
| `transfer` | Osterwalder-Schrader reconstruction | Transfer Euclidean data into Hilbert-space, vacuum, and Hamiltonian semantics. | Write H, Omega, or P_perp before reconstructing them. | OS reconstruction packet naming input Schwinger functions, null quotient, H_YM, Omega, H, and observable domains. |
| `witness` | Euclidean correlator decay and spectral measures | Detect support away from zero for physical excitations. | Use strong-coupling lattice decay or numerical spectroscopy as theorem authority. | Decay-to-gap lemma with cutoff-uniform constants and spectrally determining observables. |
| `obstruction` | Cutoff leakage, Gaussian collapse, weak observable sector | Explain why a route fails and what must be repaired. | Rename a blockage with more field vocabulary. | Failure packet naming the broken interface and repair target. |
| `validation` | Cutoff-uniformity, same-theory checks, observable density | Certify that progress belongs to the Clay target. | Count a beautiful local result as global progress without the bridge certificates. | Gate evidence that no essential commitment was weakened. |

## Abstraction Chain

1. Clay target object.
2. Regulated compact-simple gauge fields with cutoff and volume parameters.
3. Continuum gauge-invariant Schwinger functions.
4. Preserved invariants: gauge symmetry, OS positivity, covariance, nontrivial connected sector, same-theory identity.
5. OS reconstruction to H_YM, Omega, H, and the observable algebra.
6. Spectral witness: cutoff-uniform Euclidean decay or spectral-measure support away from zero.
7. Hamiltonian endpoint: Spec(H on P_perp H_YM) subset [Delta, infinity) with Delta > 0.

Each arrow is a bridge obligation. If an arrow cannot be stated with assumptions, output, failure mode, and validation handoff, the machinery is not yet allowed to steer the proof queue.

## Invalid Proof Substitutes

| Substitute | Why it is not enough | Correct workflow status |
| --- | --- | --- |
| Hamiltonian language before reconstruction | It names the endpoint but does not construct H_YM, Omega, H, or P_perp. | Backtrack to OS reconstruction premises. |
| Lattice transfer-matrix gap as final proof | It may live at fixed cutoff or finite volume. | Evidence task until cutoff-uniform transfer is certified. |
| Numerical glueball spectrum | It is physically relevant empirical evidence but not theorem authority. | Empirical-evidence request with proof boundary. |
| Lower-dimensional analogy | It can suggest mechanisms while changing the target. | Quarantine or evidence task until same-target transfer is supplied. |
| RG stability alone | It controls scale construction but does not by itself exclude low-energy excitations. | Construction machinery requiring a spectral witness bridge. |
