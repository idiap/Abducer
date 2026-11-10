# H8 state-refinement TODOs

## A. Freeze the finite theorem contract

- [ ] Fix one SU(2) heat-kernel regulator, finite-volume family, block geometry, exposure order, boundary convention, and channel set.
- [ ] Define all positive-mass microscopic histories without deleting hostile cases.
- [ ] Define the exact normalized channel subkernels, including denominators, Haar factors, Jacobians, and chart complements.
- [ ] State which emitted outputs, beyond the next state, must be conditionally sufficient.

Exit: the history space, seed state, kernels, and equality notion are immutable inputs.

## B. Build the physical boundary tables

- [ ] Populate the boundary-history table with continuous collar/chart ownership, center flux, orbit/cut transitions, and a full integer topological carrier.
- [ ] Add gauge-orbit representatives, reflection partners, and positive-mass certificates.
- [ ] Populate the channel transition table with exact numerators and conditional denominators.
- [ ] Prove every symmetry reduction is equivariant before quotienting rows.
- [ ] Store exact values or certified intervals and provenance; use floating point only for diagnostics.

Exit: every conditional row used by refinement is reproducible and normalized.

## C. Implement certified monotone refinement

- [ ] Reproduce the four-state H8 history `(0,0,1,1) -> (0,0,1,2) -> (0,1,2,3)` and defects `1 -> 0`.
- [ ] Refine by source cell, channelwise mass to every current destination cell, and all declared emitted outputs.
- [ ] Prove monotonicity, finite termination, coarsest stable refinement, and stable-partition lumpability.
- [ ] Add witnesses for each split: two histories, the distinguishing channel/cell, and the exact discrepancy.
- [ ] Add Stage 18 moment-only, Stage 19 weighted two-state, and Stage 24 unequal-persistence regression cases.

Exit: no rounded equality is used in a theorem claim, and every split has a certificate.

## D. Audit compression and closure

- [ ] Record cell count, cell-size distribution, maximum defect, and physical split feature by round.
- [ ] Test whether stable cells have gauge-covariant, reflection-compatible physical labels.
- [ ] Bound state count and support growth uniformly in the declared finite-volume family, or record failure.
- [ ] Apply the same block once more and test whether new label types appear.
- [ ] Stop on full-history recovery, uncontrolled continuous precision, nonuniform cell growth, or absence of a contractive closure recursion.

Exit: either a controlled retained state is certified or state explosion is explicitly reported as a negative result.

## E. Prove the next theorem

- [ ] Prove the physical one-block boundary-table sufficiency theorem at a precisely restricted C2 level.
- [ ] Keep lumpability separate from construction of a positive weight and the inequality `QV <= qV`.
- [ ] Hand the stable channel kernel to the Stage 19/24 weighted-ceiling problem only after sufficiency is certified.
- [ ] Audit claim language: retain C1 for the Stage 52 probe; make no C3 assertion of uniform physical sufficiency, basin entry, repeated RG, continuum theory, or mass gap.

Exit: exact hypotheses, conclusion, failure modes, and downstream dependencies appear in one theorem statement.
