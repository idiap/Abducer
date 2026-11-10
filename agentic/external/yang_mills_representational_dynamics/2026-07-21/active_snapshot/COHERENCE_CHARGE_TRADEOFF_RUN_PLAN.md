# Coherence--Charge Trade-off Long Run

## Main target

The Stage 26 frontier is the boundary-state- and volume-uniform estimate

\[
 \sup_{\Lambda,s,c}
 \frac{B_{V,c}(s)}{Z_{G,\mathrm{ref}}(s)V(s)}
 \le e^{-F_*},
 \qquad F_*>6.71292101139.
\]

This run attacks the numerator rather than adding a further abstract transfer
layer.  It resolves four coupled questions: the exact Haar entropy paid by a
local comparison ball; the best coherent-staple conditional estimate within
the certified nonlinear window; the overlap-correct free-energy charge of an
incoherent multi-link witness family; and whether the coherent and incoherent
feasible regions meet at one common coherence scale.

The claim ceiling is `C2`.  A finite or conditional theorem is not promoted to
physical basin entry unless it is proved for the complete nonlinear `SU(2)`
conditional measure uniformly in finite volume, retained state, channel, and
adaptive history.

## Stage 27 -- exact `SU(2)` Haar entropy

- [x] Derive the normalized geodesic-ball formula on `SU(2)=S^3`.
- [x] Prove explicit cubic small-ball upper and lower bounds.
- [x] Convert those bounds into certified entropy brackets.
- [x] Implement exact ball, shell, and entropy calculations with stable
  small-radius evaluation.
- [x] Calibrate every radius used by Stages 21, 22, 25, and 26.
- [x] Record the denominator entropy paid by the coherent conditional bound.
- [x] Add theorem source/PDF, tests, JSON calibration, dependencies, ledger,
  and stage README.

## Stage 28 -- coherent conditional budget optimizer

- [x] Rewrite the Stage 15 finite-time bound as an exact one-variable
  denominator optimization problem.
- [x] Prove the stationarity equation
  `v'(delta)/v(delta)=m(eta+delta)/t` and uniqueness in the admissible local
  interval.
- [x] Replace an uncertified golden search by a sign-bracketed bisection
  certificate.
- [x] Solve for the least curvature threshold meeting the Stage 26 residual
  ceiling for both ideal and declared coherence radii.
- [x] Re-optimize the `K+R` radius rather than freezing the former equal split.
- [x] Prove a nonempty conditional coherent-channel budget inside the sharp
  nonlinear window.
- [x] Keep the collar-occurrence probability and full nonlinear kernel marked
  open.
- [x] Add theorem source/PDF, adversarial tests, JSON, dependencies, ledger,
  and README.

## Stage 29 -- overlap-correct incoherent-collar free energy

- [x] Prove that `k` collar-failure witnesses with plaquette overlap at most
  `nu` force global Gibbs exponent at least
  `k eta^2/(4 nu t)`.
- [x] Include connected-witness entropy through the exact branching ratio
  `theta=exp(alpha) D^2 exp(-eta^2/(4 nu t))`.
- [x] Derive the convergence threshold and rooted-contour free-energy bound.
- [x] Add an identical-witness counterexample that invalidates naive additive
  charging without overlap control.
- [x] Jointly compare the maximum coherence radius accepted by Stage 28 with
  the minimum coherence radius required by contour entropy.
- [x] Quantify the branching reduction or charge amplification needed to close
  the gap.
- [x] Add theorem source/PDF, tests, JSON, dependencies, ledger, and README.

## Stage 30 -- channel-resolved partition frontier

- [x] Separate center, coherent continuous, incoherent continuous, cut/orbit,
  and topology numerator channels.
- [x] Mark each channel as exact restricted, conditional, quantitatively open,
  or structurally unrepresented.
- [x] Compose only proved/conditional inputs with the Stage 25 `K+R` theorem.
- [x] State the first remaining physical numerator inequality without hiding
  normalizers, entropy, retained states, or volume quantifiers.
- [x] Rank the next interventions by the measured deficit.
- [x] Add theorem source/PDF, executable ledger, tests, JSON, dependencies,
  and README.

## Integration and validation

- [x] Add a cross-stage synthesis, dependency graph, and parameter registry.
- [x] Update root README, manifest, reproducibility guide, and package counts.
- [x] Update the exported workflow guidance to start future runs from the
  measured coherence--charge deficit.
- [x] Run every stage test and audit all calibration JSON.
- [x] Compile and visually inspect the four new theorem PDFs.
- [x] Refresh checksums and both distributable archives.

## Hard stop

This run may prove a coherent-channel estimate and a conditional multi-witness
criterion.  It must stop short of one-scale physical basin entry if the same
coherence parameter does not control both the coherent conditional numerator
and the incoherent-collar contour sum for the complete nonlinear measure.  It
must stop still earlier than continuum construction or a mass gap.
