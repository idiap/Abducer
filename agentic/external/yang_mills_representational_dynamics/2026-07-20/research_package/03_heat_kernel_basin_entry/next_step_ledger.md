# Next-step proof ledger

| ID | Claim | Status | Consequence |
|---|---|---|---|
| HK0 | Heat-kernel plaquette measure is a legitimate finite regulator with exact lattice gauge invariance | Imported/restricted | Primary regulator selected |
| HK1 | Heat kernels on compact groups form an approximate identity | Imported | Input to the obstruction theorem |
| HK2 | For fixed `h != e`, `TV(mu_t, L_h mu_t) -> 1` | Proved here | Worst-case translated-kernel influence degenerates |
| HK3 | The one-plaquette heat-kernel conditional family has worst-case TV coefficient tending to one | Proved here | No cutoff-uniform `q < 1` for the naive basin |
| HK4 | The numerical U(1) calibration reproduces fixed-shift degeneration and the `sqrt(t)` local limit | Restricted/executable | Seven tests pass |
| HK5 | The SU(2) character calibration reproduces antipodal degeneration | Restricted/executable | General compact-group theorem calibrated on a simple group |
| HK6 | Exact U(1) convolution blocking reduces fixed-shift sensitivity only when accumulated heat time becomes macroscopic | Restricted/executable | Blocking alone is not yet a uniform entry theorem |
| HK7 | Curvature-matched U(1) heat-kernel and Wilson one-plaquette laws approach one another at small heat time | Restricted/executable | Regulator comparison calibration, not universality |
| HK8 | A degree-eight optimistic local-plus-tail proxy is approximately `1.16 > 1` | Restricted/executable | The naive toy budget does not enter the replacement basin |
| TB1 | A two-tier good-field/defect coupling recursion with weighted norm below one implies exponential covariance decay | Proved here, conditional on local recursion | Replacement basin-to-rigidity theorem |
| TB2 | The two-tier basin is open under weighted perturbations smaller than its contraction margin | Proved here | Stability certificate |
| BE-G | Four-dimensional heat-kernel Yang--Mills satisfies the good-field coupling bound after finite physical RG scale | Open | Requires quotient coercivity and block transport |
| BE-D | Bad blocks and topological defects satisfy a uniformly subcritical disagreement-polymer bound | Open | Requires full-measure large-field/topology control |
| BE-R | RG reconstruction errors and positivity certificates are summable to the entry scale | Open | Required for physical rigidity transfer |

## Revised first open implication

Find a finite physical block scale `ell_*`, a gauge-invariant good set, and
nonnegative matrices `K_*` and `R_*` such that

```text
sup_B sum_C exp(kappa d(B,C)) [K_*(B,C) + R_*(B,C)] <= q < 1,
```

uniformly in volume and cutoff. `K_*` must be obtained from couplings of
good-field quotient conditionals. `R_*` must dominate bad-field and topological
disagreement propagation, with a summable polymer certificate. Neither matrix
may be defined using the desired long-distance clustering or mass gap.

## Claim level

The obstruction theorem and abstract two-tier transfer theorem are C2 results.
Their application to four-dimensional pure Yang--Mills remains C3-conditional.
Fourteen executable tests cover the U(1) and SU(2) calibrations. No continuum
construction or Clay-level gap is claimed.
