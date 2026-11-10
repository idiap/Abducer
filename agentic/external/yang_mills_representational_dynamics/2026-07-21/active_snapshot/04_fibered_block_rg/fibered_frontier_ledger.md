# Fibered block-RG frontier ledger

## Outcome

The completed next step identifies and removes a false requirement from the
earlier basin formulation: a retained relevant mode should be transported by an
RG step, not forced to contract inside that same step.  The correct local target
is contraction of the **conditional fiber** after the retained mode and gauge
redundancy have been quotiented out.

This is a representational advance and a restricted theorem package.  It is not
a construction of four-dimensional Yang--Mills theory and not a Clay solution.

## Implemented todos

- [x] Freeze an interacting two-plaquette heat-kernel block with retained total
  holonomy and centered fiber coordinate.
- [x] Derive its exact compact `U(1)` bridge density.
- [x] Prove the exact Gaussian tangent responses: full coordinate `1/2`,
  centered fiber `0`.
- [x] Numerically calibrate the compact bridge in circular Wasserstein distance.
- [x] Prove the iterated law-of-total-covariance decomposition for an RG tower.
- [x] State and prove an abstract conditional fibered-clustering theorem.
- [x] Prove a rooted connected-bad-cluster bound in the independent-defect model.
- [x] Prove finite-product total-variation tensorization for regulator comparison.
- [x] Compare the heat-kernel and Wilson one-plaquette laws and fixed 16-plaquette
  blocks numerically.
- [x] Add executable tests, machine-readable calibration output, and a theorem
  dependency graph.
- [x] Audit every claim by scope and record the remaining four-dimensional
  obligations.

## Proved statements and exact scope

| ID | Statement | Scope | Status |
|---|---|---|---|
| F1 | `gamma_t^s(q)=p_t(q)p_t(s-q)/p_{2t}(s)` | two compact `U(1)` plaquettes | proved |
| F2 | full response `1/2`, centered-fiber response `0` | Gaussian tangent bridge | proved |
| F3 | multiscale covariance equals terminal transported covariance plus fiber increments | abstract square-integrable RG tower | proved |
| F4 | rooted all-bad connected set bound `p(Delta^2 p)^(n-1)` | independent Bernoulli defects | proved |
| F5 | `TV(mu^m,nu^m) <= m TV(mu,nu)` | finite product measures | proved |
| C1 | fiber contraction + summable defects + terminal clustering imply original clustering | abstract theorem with explicit hypotheses | conditional theorem |

## Calibration

For heat times `t = 0.5, 0.2, 0.1, 0.05`, the compact bridge full-coordinate
coefficient is approximately `0.4983, 0.5000, 0.5000, 0.5000`; the centered-fiber
coefficient is below numerical resolution at the displayed precision.  With
Gaussian good-field radius `rho=3`, the bad probability is about `0.00270`; the
independent degree-eight branching proxy `64 p` is about `0.173 < 1`.

The 16-plaquette heat-kernel/Wilson product-TV upper bound decreases from the
trivial value `1` at `t=0.5` to about `0.0716` at `t=0.05`.  This is only a fixed
block comparison.

## What has been falsified

1. **Full-coordinate one-step contraction is the wrong invariant.** The
   Gaussian bridge transports half the retained boundary shift to the internal
   coordinate, even though its centered fluctuation is completely insensitive
   to that shift.
2. **Independent-tail estimates are not yet a Yang--Mills polymer estimate.**
   Four-dimensional defects are dependent and can carry gauge/topological
   structure.
3. **Fixed-block regulator agreement is not continuum universality.** If a
   physical block contains `m(a) -> infinity` plaquettes, one needs a
   one-plaquette error `o(1/m(a))` or a sharper interacting comparison.

## Open four-dimensional obligations

- [ ] **O1 — Gauge-covariant disintegration.** Define a local block map for a
  compact simple nonabelian group, its retained gauge-invariant data, and a
  measurable conditional fiber, with overlap consistency and reflection
  compatibility.
- [ ] **O2 — Good-field fiber contraction.** Establish a computable quotient
  Wasserstein/Dobrushin coefficient `K_k < 1` uniformly in volume and cutoff on
  good blocks.
- [ ] **O3 — Dependent defect polymers.** Replace Bernoulli independence by a
  conditional large-deviation or domination theorem controlling connected bad
  blocks, exceptional gauge orbits, and topological sectors; prove a summable
  remainder `R_k`.
- [ ] **O4 — Basin entry.** Show that the asymptotically free ultraviolet measure
  enters the fibered basin after finitely or controllably many gauge-covariant RG
  steps, without defining the basin by the desired conclusion.
- [ ] **O5 — Continuum coherence.** Prove regulator-independent convergence of a
  separating gauge-invariant observable core, reflection positivity,
  Euclidean covariance, symmetry, regularity, and nontriviality.
- [ ] **O6 — Spectral transfer.** Perform Osterwalder--Schrader reconstruction
  and turn uniform physical-unit clustering into `spec(H) subset {0} union
  [Delta,infinity)` for some `Delta>0`.

## Immediate research order

1. Work first on O1 in the smallest nonabelian block where retained loop data
   and stabilizers can be described explicitly.
2. Define O2 only on the resulting conditional fiber; test it in `SU(2)` near
   the identity and against noncommuting boundary perturbations.
3. Build an adversarial defect family before attempting O3: large curvature,
   near-cut-locus holonomy, reducible stabilizer, and nontrivial flux.
4. Attempt O3 with stochastic domination or a polymer norm that retains the
   dependence structure.
5. Only after O1--O3 have cutoff-uniform constants should O4 be claimed as the
   frontier theorem.

