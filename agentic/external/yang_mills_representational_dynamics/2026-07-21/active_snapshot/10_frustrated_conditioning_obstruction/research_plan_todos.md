# Stage 10 Research Plan and Completed Todos

## High-value target

Test the most direct route from the Stage 09 independent benchmark to a
dependent-measure estimate: a boundary-uniform one-link conditional
small-curvature bound.  The decision target is exact and finite:

> Can every conditioning of the links surrounding an interior link keep all
> six incident plaquettes in the identity chart with uniformly high
> probability at weak coupling?

## Completed todos

- [x] Freeze the open `2^4` block, heat-kernel convention, center element, and
  gauge-invariant plaquette bad event.
- [x] Select an interior link with six incident plaquettes.
- [x] Build the exact binary center-staple map from the remaining links to the
  six incident plaquette staples.
- [x] Prove executable rank six and construct a boundary assignment with five
  identity staples and one `-I` staple.
- [x] Derive the exact conditional link density
  `p_t(U)^5 p_t(-U) dU` for that admissible conditioning.
- [x] Reduce the density to the `SU(2)` class angle and derive the rate function
  `I_6(theta)=5 theta^2+(pi-theta)^2`.
- [x] Compute the unique minimizer `theta_*=pi/6`, the frustrated plaquette
  angle `5pi/6`, and the exact good-event rate gap
  `6(5pi/6-rho)^2`.
- [x] Prove that for every `rho<5pi/6` the target plaquette is bad with
  conditional probability tending to one as `t` tends to zero.
- [x] Conclude that worst-case boundary-uniform one-link Dobrushin domination
  by rare curvature defects is impossible for this event.
- [x] Implement stable signed-log Poisson-image evaluation and logarithmic
  Gauss--Legendre calibration without ultraviolet underflow.
- [x] Cross-check the numerical mode and scaled logarithmic probability against
  the exact large-deviation rate.
- [x] Add positive, boundary, algebraic, numerical, and false-promotion tests.
- [x] Replace the failed route by a precise strategy ledger: restricted-good
  boundaries, multi-link block integration, contours/activities, and explicit
  center/topology labels.
- [x] Produce the theorem report, calibration JSON, dependency graph, frontier
  ledger, source, tests, and reproducibility instructions.
- [x] Audit the result as `C2`, a rigorous restricted obstruction theorem.

## Decision and consequence

The direct uniform-conditional route fails.  The failure is not caused by a
loose estimate: a realizable center-frustrated boundary condition moves the
weak-coupling conditional minimum from the identity to `theta=pi/6`, leaving
the designated plaquette at angle `5pi/6`.

The next dependent-polymer theorem must therefore avoid a supremum over
arbitrary microscopic boundary fields.  It must charge frustrated boundary
patterns to a larger contour/polymer, condition only on an explicitly good
collar, or integrate a multi-link block before estimating its activity.

