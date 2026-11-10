# Adaptive Nonlinear Bridge: Multi-Target Run

Date: 2026-07-20

## Strategic target

Stages 11--14 reduced the first Yang--Mills frontier to a one-scale question:
can the nonlinear `SU(2)` link measure be converted into a volume-uniform bad-
block process with weight below the degree-18 counting threshold?  This run
separates four logically different issues that were previously compressed into
that question.

## Shared conventions and stop rules

- Heat generator: `(1/2) Delta` on `SU(2)`.
- Frozen witness: `t=3e-6`, `rho=0.0082`, `m=6`, `alpha=0.1`, `Delta=18`.
- The coherent-staple radius is denoted `eta`; the denominator-ball radius in
  the finite-time proof is `delta`.
- A one-link conditional, deterministic geometric charge, chart-restricted
  comparison, or abstract domination theorem is not promoted to a full
  nonlinear block estimate.
- Event intersection bounds are not called Mayer/Ursell activities.
- Every numerical optimization is labeled calibration unless its extremality
  is proved independently.
- Every stage records the first unproved implication and fails closed on
  invalid radii, probabilities, dimensions, or graph degrees.

## Stage 15: finite-time coherent conditionals

- [x] Replace the Stage 11 small-time limsup by an explicit finite-time bound.
- [x] Use radial monotonicity of the `SU(2)` heat kernel and exact Haar ball
  volume.
- [x] Control local heat-kernel ratios with the Poisson-image remainder.
- [x] Preserve all finite-volume prefactors instead of reporting only a rate.
- [x] Optimize the auxiliary denominator radius as a declared calibration.
- [x] Solve for the heat time at which the bound crosses the Stage 14 weight.
- [x] Add monotonicity, threshold, invalid-input, and false-promotion tests.
- [x] Produce code, calibration, graph, ledger, LaTeX, and PDF.

Gate: the theorem is exact for a single link under a supplied coherent collar;
it does not prove that collars occur with adequate conditional probability.

## Stage 16: continuous collar charging

- [x] Prove that relative staple distances equal relative incident-plaquette
  distances after any selected-link value is inserted.
- [x] Charge collar failure to an incident curvature above `eta/2`.
- [x] Prove the stronger total incident energy charge `eta^2/2`.
- [x] Combine the charge with the Stage 11 admissibility threshold.
- [x] Test compatibility with the Stage 14 collar rate `K`.
- [x] Derive the maximum time allowed by energy charging.
- [x] Derive the stricter maximum time allowed by the radial Gaussian rate.
- [x] Add exact quaternion, boundary, no-go, and false-promotion tests.
- [x] Produce code, calibration, graph, ledger, LaTeX, and PDF.

Gate: local deterministic charging is exact but quantitatively insufficient at
the frozen witness; multi-link or coarser collar integration is required.

## Stage 17: chart density comparison

- [x] Prove normalized measure comparison from oscillation of a remainder.
- [x] Derive remainder oscillation from a Hessian bound on a convex ball.
- [x] include the reference mass of the retained chart explicitly.
- [x] Implement stable log-probabilities for high-dimensional Gaussian balls.
- [x] Import the Stage 08 finite-block Hessian certificate at the frozen time.
- [x] Separate the small local action oscillation from chart-coverage entropy.
- [x] Compute a diagnostic radius needed for a declared reference mass.
- [x] Add exact examples, high-dimensional stress tests, and scope guards.
- [x] Produce code, calibration, graph, ledger, LaTeX, and PDF.

Gate: the action-density comparison is proved on a retained chart.  Available
chart coverage is too weak to certify the Stage 14 nonlinear loss.

## Stage 18: adaptive stochastic domination

- [x] State the exact history-uniform conditional probability hypothesis.
- [x] Prove domination by a shared-uniform sequential coupling.
- [x] Transfer domination to joint bad-set and connected-cluster bounds.
- [x] Combine the theorem with the Stage 14 numerical weight.
- [x] Construct a two-site counterexample showing that intersection moments
  alone do not imply stochastic domination.
- [x] Identify adaptive multi-link exposure as the corrected frontier target.
- [x] Add coupling, counterexample, threshold, and false-promotion tests.
- [x] Produce code, calibration, graph, ledger, LaTeX, and PDF.

Gate: stochastic-domination conversion is no longer open as an abstract step;
the full `SU(2)` adaptive conditional block estimate remains open.

## Integration

- [x] Run all new and historical tests.
- [x] Compile, render, and inspect all four PDFs.
- [x] Update the cross-stage registry, README, manifest, reproducibility guide,
  and frontier synthesis.
- [x] Regenerate checksums and verify the aggregate archive.
- [x] Save the new artifacts and aggregate package to Library.
