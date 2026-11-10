# Long Multi-Target Run: Boundary-Sensitive Dependent Activities

Date: 2026-07-20

## Strategic question

Stage 10 proved that a supremum over arbitrary microscopic link
conditionings makes a rare-curvature estimate false.  The action cost of the
frustrating boundary was discarded.  This run develops four successive
replacements, moving from a local conditional theorem to a quantitative
nonlinear transfer gate.

## Shared conventions and stop rules

- Gauge group: `SU(2)` unless a theorem is explicitly formulated for a compact
  group with bi-invariant distance.
- Regulator: one-plaquette heat-kernel weight with generator `(1/2) Delta`.
- Frozen ultraviolet witness: `t=3e-6`, `rho=0.0082`, `alpha=0.1`.
- Connectivity: shared-link adjacency for ordinary bad-set clusters and
  common-three-cell adjacency for center Bianchi contours.
- Geometry: the open side-two four-dimensional cubical block.
- A finite, center-sector, Gaussian, asymptotic, or conditional result is never
  promoted to the complete nonlinear `SU(2)` link measure.
- Every stage must expose its first unproved implication and fail closed on
  invalid parameters.

## Target 11: coherent-staple good collar

Decision theorem: determine whether a gauge-covariant coherence restriction
on the six staples restores rare conditional curvature at the small-time rate
level.

- [x] Replace coordinate bounds on individual staples by the bi-gauge-invariant
  condition that all staples lie in one geodesic ball.
- [x] Derive the conditional energy after translating the common staple center.
- [x] Prove a uniform rate gap `rho^2-m eta^2` for every target plaquette.
- [x] Identify the exact admissibility threshold `eta<rho/sqrt(m)`.
- [x] Show that the Stage 10 `{I,-I}` conditioning has coherence radius
  `pi/2` and is excluded by the good collar.
- [x] Calibrate the frozen ultraviolet witness and the sharp commuting stress
  family.
- [x] Add invalid-input, boundary, monotonicity, and false-promotion tests.
- [x] Produce code, calibration, theorem graph, ledger, LaTeX, and PDF.

Gate: this theorem controls conditionals only when a coherent collar is
supplied.  It does not estimate the probability of collar failure.

## Target 12: exact center-contour charging

Decision theorem: quantify the energetic object erased by the Stage 10
conditioning in the center-valued sector.

- [x] Construct the exact `GF(2)` plaquette-to-three-cell coboundary matrix.
- [x] verify `d_2 d_1=0` and finite-block cochain exactness.
- [x] Reconstruct the Stage 10 center assignment in the full plaquette field.
- [x] Prove by an exhaustive syndrome certificate that its one-frustrated/
  five-aligned incident pattern requires at least five negative plaquettes.
- [x] Exhibit the matching five-plaquette configuration.
- [x] Prove that every nonempty exact center cocycle has at least three
  plaquettes.
- [x] Compute the plaquette adjacency degree and a volume-uniform rooted
  contour bound.
- [x] Derive the explicit center-contour counting threshold.
- [x] Add exact algebra, minimality, counting, and false-promotion tests.
- [x] Produce code, calibration, theorem graph, ledger, LaTeX, and PDF.

Gate: center contours are a nontrivial dependent subsector, not the continuous
nonabelian measure.

## Target 13: dependent Gaussian polymers

Decision theorem: replace Stage 09 independence by the exact shared-link
dependence of the linearized gauge model.

- [x] Put the gauge quotient in curvature coordinates
  `F in im(d_1) tensor R^3`.
- [x] Prove that the curvature covariance is `t P`, with `P` an orthogonal
  projection and hence `P<=I`.
- [x] Derive a joint radial bad-set bound for every plaquette set using a
  quadratic exponential moment.
- [x] Convert the joint estimate into a rooted connected-set sum without an
  independence hypothesis.
- [x] Evaluate the criterion at the frozen Stage 09 witness.
- [x] Solve for the largest heat time allowed by the declared counting bound.
- [x] Check projection, rate, monotonicity, threshold, and false-promotion
  cases.
- [x] Produce code, calibration, theorem graph, ledger, LaTeX, and PDF.

Gate: the theorem is exact for the linearized Gaussian gauge model.  The
nonlinear Haar/action comparison remains open.

## Target 14: nonlinear two-tier transfer

Decision theorem: state the exact pair of estimates that would transfer the
dependent Gaussian result to a nonlinear connected-event envelope and compute
their budget.

- [x] Split every connected bad event into coherent-collar and collar-failure
  channels.
- [x] Parameterize the good-channel Radon--Nikodym loss by `kappa` per
  plaquette and the charged collar rate by `K`.
- [x] Prove the effective event-envelope bound
  `q_eff=exp(kappa-J)+exp(-K)`.
- [x] Prove the rooted connected-event criterion
  `exp(alpha) Delta^2 q_eff<1`.
- [x] Compute the maximum nonlinear comparison loss if collar failure is
  absent.
- [x] Compute the minimum collar rate for a declared comparison loss.
- [x] Formulate a summable multiscale composition criterion.
- [x] Add boundary, monotonicity, failure, and false-promotion tests.
- [x] Produce code, calibration, theorem graph, ledger, LaTeX, and PDF.

Gate: the abstract event-transfer theorem is proved; the required `SU(2)`
Radon--Nikodym and charged-collar estimates, followed by a Mayer/Ursell
activity construction or valid stochastic domination, are quantified but
remain open.

## End-of-run integration

- [x] Run every new test suite.
- [x] Run the complete historical regression suite.
- [x] Compile and visually inspect all four PDFs.
- [x] Update package README, manifest, reproducibility guide, and frontier map.
- [x] Regenerate package checksums and archives and verify ZIP integrity.
- [x] Save the new outputs and aggregate archive to Library.
