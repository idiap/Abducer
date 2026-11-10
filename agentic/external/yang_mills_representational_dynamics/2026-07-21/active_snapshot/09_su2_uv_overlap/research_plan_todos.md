# Stage 09 Research Plan and Completed Todos

## High-value target

Decide whether the Stage 08 local nonlinear-control inequalities and a
probabilistically useful ultraviolet small-field scale can coexist.  The
target is deliberately split into two claims:

1. an exact finite-block local-action certificate; and
2. a standalone `SU(2)` heat-kernel tail plus an independent-block polymer
   benchmark.

The second item is a calibration target, not the missing dependent
four-dimensional Yang--Mills polymer theorem.

## Completed implementation todos

- [x] Freeze the heat-kernel convention, chart radius, block size, block
  adjacency degree, and weighted polymer exponent.
- [x] Derive a cancellation-free image-formula upper bound for
  `P_t(theta >= rho)` with an explicit normalization lower bound and summed
  nonzero-image error.
- [x] Derive local Hessian and third-derivative bounds for the exponential-link
  Haar Jacobian `-2 log(sin |A|/|A|)`.
- [x] Add the Haar contribution to the Stage 08 five-component action norm.
- [x] Recompute fiber coercivity, centered transport, and generated-base
  coercivity from the augmented norm.
- [x] Turn the one-plaquette tail into a 216-plaquette block union bound.
- [x] Implement the rooted weighted connected-polymer sum for independent
  bad blocks of maximum adjacency degree eight.
- [x] Exhibit a strict overlap witness and use strict continuity to certify a
  nonempty parameter neighborhood.
- [x] Implement a deterministic grid search that records the best robust
  witness in a declared finite domain without promoting the search to a proof
  of global optimality.
- [x] Cross-check the image upper bound against the independent character
  expansion at the witness.
- [x] Add positive, boundary, monotonicity, and deliberately failing tests.
- [x] Record the gauge-orbit, shared-link, Bianchi, center-flux, topology,
  volume-uniformity, and repeated-RG obligations excluded by the benchmark.
- [x] Produce the LaTeX theorem report, dependency graph, calibration JSON,
  frontier ledger, and reproducibility instructions.
- [x] Audit the claim at level `C2`: a rigorous restricted certificate, not
  full-measure basin entry, continuum Yang--Mills, or a mass gap.

## Decision rule

For a proposed witness `(t,r,r_F)`, the stage passes only if all of the
following strict inequalities hold:

```text
nonlinear physical singular-value lower bound > 0
augmented Hessian remainder eta_total < 1
centered fiber transport K_F < 1
generated reference-base margin > 0
exp(alpha) * Delta^2 * p_block < 1
exp(alpha) * p_block / (1-exp(alpha)*Delta^2*p_block) < 1
```

Here `p_block <= 216 p_plaquette` is only the standalone-tail union-bound
benchmark.  No claim is made that it bounds a marginal of the complete
four-dimensional link measure.

## Implemented witness

```text
t       = 3e-6
r       = 0.0041
rho     = 2r = 0.0082
r_F     = 1e-5
Delta   = 8
alpha   = 0.1
```

The machine-readable calibration contains all derived margins and flags.

