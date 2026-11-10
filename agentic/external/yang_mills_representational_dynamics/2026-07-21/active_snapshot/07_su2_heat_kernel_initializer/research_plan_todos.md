# Stage 07 plan and completed todo ledger

## Frozen target

Initialize the local derivative side of the Stage 06 norm for the exact
one-plaquette `SU(2)` heat-kernel action.  Fix the Laplacian normalization,
derive an exact Poisson-image factorization, convert it into explicit Hessian
and third-derivative bounds on a logarithmic curvature ball, and compute a
gauge-invariant bad-curvature probability with a controlled character-series
tail.  Provide a chain-rule interface for a future full-block BCH theorem.

## Implemented todos

- [x] Freeze `SU(2) = S^3`, Haar normalization, class angle, Laplacian
  convention, heat time, chart radius, and cut-locus exclusion.
- [x] State the exact character expansion and its Casimir exponent.
- [x] derive the Poisson-image representation in the matching normalization.
- [x] Pair positive and negative images to remove the apparent singularity at
  zero curvature.
- [x] Derive explicit uniform bounds `Q_0,...,Q_3` for the image correction and
  an analytic tail after finitely many images.
- [x] Convert `Q_j` into explicit second- and third-derivative bounds for
  `-log(1+q)`.
- [x] Bound the geometric correction `log(sin(theta)/theta)` explicitly.
- [x] Prove scaled curvature-coordinate Hessian and Euclidean third-derivative
  budgets for all `0 < t <= t_max`.
- [x] Derive chain-rule formulas propagating these budgets through a declared
  curvature chart `X(A)`.
- [x] Define the exceptional event `theta(U_p) >= rho` in a gauge-invariant
  manner.
- [x] Integrate the character expansion analytically in the radial Haar
  measure and bound its omitted tail geometrically.
- [x] Cross-check the character and Poisson-image representations numerically.
- [x] Add hostile tests for cut-locus radii, excessive time windows, invalid
  chart constants, missing coercive image tails, and false block promotion.
- [x] Produce calibration data, a theorem dependency graph, and a conservative
  frontier ledger.
- [x] Write, compile, render, and visually inspect the self-contained PDF.
- [x] Integrate all Stage 07 outputs into the complete research package.

## Open frontier beyond this completed target

- Prove explicit derivative constants for the actual transported plaquette-log
  map on the full `2^4` block, including the Coulomb slice and retained/fiber
  projections.
- Replace the safe scalar aggregation factor by the sharp block incidence and
  overlap operator norms.
- Convert one-plaquette tail probabilities into dependent, gauge-invariant
  bad-block polymer activities uniform in volume and cutoff.
- Treat center flux, global holonomy, reducible orbits, cut-locus crossings,
  boundary conditions, and topological sectors.
- Initialize all five Stage 06 norm components for the generated interaction,
  then prove that the one-step recursion closes repeatedly.
- Establish the nonperturbative retained-base crossover, continuum OS theory,
  and Hamiltonian mass gap.
