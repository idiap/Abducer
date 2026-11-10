<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Qualitative Mechanistic Graph

- Target: `yang-mills-existence-and-mass-gap-target`
- Nodes: `16`
- Edges: `9`
- Status counts: `{'proof_obligation': 1, 'conjectural': 2, 'established': 1, 'validated_probe': 1, 'symbolic_formula': 1, 'analytic_obligation': 1, 'side_condition_ledger': 1, 'falsifier_shape': 1}`

## Relation Edges

### rel-boundary-factor-to-phase
- `var.boundary_factor_B` --enables--> `var.quotient_phase_phi`
- Direction: boundary OPE factors can introduce phase structure in normalized quotients
- Regime: `reg.collar_collapse`
- Epistemic status: `validated_probe`
- Failure modes: A nonzero quotient holonomy makes pairwise positivity insufficient.; A negative determinant falsifies the proposed positivity bridge.

### rel-equational-interface-to-side-conditions
- `var.equational_interface_packet` --constrains--> `var.side_condition_ledger`
- Direction: Every exact identity is valid only under the side-condition ledger; failing a side condition backtracks the branch before analytic promotion.
- Regime: `reg.collar_collapse, reg.continuum_transfer`
- Epistemic status: `side_condition_ledger`
- Failure modes: The determinant formula no longer licenses positivity conclusions.; Additional scale factors enter all minors and quotient comparisons.; The interface must backtrack to support-restricted or regularized quotient definitions.; A coordinate phase may be mistaken for a real obstruction.; The packet is quarantined as proxy algebra.

### rel-finite-interface-falsifier-shapes
- `var.equational_interface_packet` --falsifies--> `var.reflection_gram_N`
- Direction: Formula-derived falsifier shapes can demote pairwise-positivity, phase-removal, or modulus-only transfer branches.
- Regime: `reg.collar_collapse`
- Epistemic status: `falsifier_shape`
- Failure modes: pairwise minors pass while the 3x3 determinant is negative; no diagonal D removes all quotient phases on the support graph; real pairwise bounds do not produce PSD modulus quotient; the quotient identity fails to represent the continuum carrier without extra contact terms

### rel-phase-falsifies-gram-transfer
- `var.quotient_phase_phi` --falsifies--> `var.reflection_gram_N`
- Direction: nonzero holonomy or negative normalized determinant blocks naive positivity transfer
- Regime: `reg.collar_collapse`
- Epistemic status: `conjectural`
- Failure modes: The determinant failure is a toy artifact with no same-theory transfer certificate.; The determinant test is not realized by Yang-Mills observables.; The imagined situation is too remote from the target observable algebra.; The phase obstruction is an artifact of a proxy model.

### rel-symbolic-formula-to-analytic-obligations
- `var.finite_quotient_matrix_Q` --induces--> `var.analytic_estimate_obligations`
- Direction: Exact finite algebra induces proof-relevant analytic estimates before any bounded numeric search is allowed.
- Regime: `reg.continuum_transfer, reg.collar_collapse`
- Epistemic status: `analytic_obligation`
- Failure modes: B_ij is regulator-family dependent or cannot be realized in the same observable algebra.; Contacts shift the finite determinant sign or invalidate pairwise-to-family transfer.; A non-removable holonomy makes det(Q) negative in an admissible finite family.; Pairwise bounds hold while the three-by-three determinant is negative.

### rel-symbolic-quotient-determinant
- `var.quotient_phase_phi` --constrains--> `var.finite_quotient_matrix_Q`
- Direction: The quotient holonomy Phi enters det(Q) through cos(Phi), so phase control can decide finite-family positivity.
- Regime: `reg.collar_collapse`
- Epistemic status: `symbolic_formula`
- Failure modes: pairwise minors hold but det(Q) < 0; Phi is not 0 modulo pi after diagonal rephasing

### rel.cutoff-to-gram-positivity
- `var.cutoff_a` --constrains--> `var.reflection_gram_N`
- Direction: smaller cutoff should preserve positivity only if the positivity cone is closed
- Regime: `reg.fixed_cutoff, reg.continuum_transfer`
- Epistemic status: `proof_obligation`
- Failure modes: Reflection positivity leaks under cutoff removal.; The limiting topology is too weak for positivity closure.

### rel.euclidean-decay-to-gap
- `var.euclidean_time_t` --decreases--> `var.correlation_C`
- Direction: larger Euclidean time suppresses spectral components above the lower support
- Regime: `reg.long_time_spectral`
- Epistemic status: `conjectural`
- Failure modes: Decay is only fixed-regulator.; The observable sector is not dense or misses low-energy states.

### rel.spectral-gap-controls-correlator
- `var.spectral_gap_m` --decreases--> `var.correlation_C`
- Direction: larger mass scale gives faster long-time decay
- Regime: `reg.long_time_spectral`
- Epistemic status: `established`
- Failure modes: The spectral measure has arbitrarily small non-vacuum support.; The correlator does not see the full excitation sector.
