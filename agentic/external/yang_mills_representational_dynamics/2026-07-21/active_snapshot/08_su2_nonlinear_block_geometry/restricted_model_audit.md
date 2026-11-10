# Restricted-model, parameter, and limit audit

## Parameter registry

| Symbol | Meaning | Calibrated value | Quantifier and role |
|---|---|---:|---|
| `t_max` | upper heat time | `0.01` | all `0 < t <= t_max`; ultraviolet local estimate |
| `r` | joint four-link plaquette radius | `0.003` | every plaquette extraction in the good chart |
| `rho=2r` | curvature radius | `0.006` | before the principal-log cut locus |
| `r_F` | centered fiber-coordinate radius | `0.001` | Stage 06 transport tube |
| `a` | ungauged global link-field radius | `0.0002` | input to the local slice theorem |
| `s` | mean-zero gauge-parameter radius | `0.0006` | contraction ball |
| `kappa` | global nonlinear derivative deviation | `0.0593212` | must be below `sqrt(2)` |
| `eta` | global scaled Hessian remainder | `0.747472` | must be below fiber reference curvature `2` |
| `tau` | global scaled third-derivative budget | `295.100` | controls centered response on radius `r_F` |

All constants concern one fixed side-two four-dimensional block.  There is no
volume parameter, lattice spacing limit, or iterated scale index in the
theorem.

## Calibration matrix

| Controlled model or hostile case | Expected behavior | Result | Consequence |
|---|---|---:|---|
| Commuting/abelian-aligned link logs | BCH remainder vanishes | Pass | Quaternion implementation reduces exactly to the oriented linear sum |
| Small noncommuting quaternion samples | Remainder stays below the analytic Taylor majorant | Pass | Product-log derivative calculus accepts genuinely nonabelian inputs |
| Unquotiented link Hessian | Gauge zero modes remain | Pass | Curvature injectivity is asserted only on `ker(d0^T)` |
| Coulomb quotient on the `2^4` block | Physical singular-value floor is `sqrt(2)` | Pass | Nonlinear inverse theorem has a positive finite margin |
| Local mean-zero gauge orbit | Fixed-point map contracts | Pass | A unique local Coulomb representative exists modulo constant conjugation |
| Principal-log cut locus | Coordinate chart must fail | Pass | Antipodal quaternion and excessive-radius inputs are rejected |
| Excessive nonlinear chart | Fiber margin is exhausted | Pass | Certificate fails closed instead of returning a misleading constant |
| One-plaquette heat law at `t=0.01` | Typical curvature lies outside `rho=0.006` | Pass/falsifies promotion | Good-chart control is not a full-measure theorem |
| Finite-volume gapped matrix | May satisfy a local coercivity certificate | Accepted only locally | Finite-dimensional coercivity is not labeled a physical mass gap |
| Gapless cutoff sequence | No uniform continuum gap follows from finite local margins | Rejected as inference | Cutoff-uniform basin entry remains open |
| Hidden gapless direct summand | Incomplete observable/local sectors cannot establish a total gap | Rejected as inference | Observable completeness is still required |
| Topological or center-flux sector | Absent from a single principal-log chart | Outside scope | Requires an orbit atlas and sector-dependent defect channel |

## Representation-preservation audit

| Structure | Status | Reason |
|---|---:|---|
| Local gauge covariance of plaquette class angles | Preserved | Holonomy transforms by conjugation |
| Nonconstant gauge redundancy | Locally controlled | Mean-zero Coulomb contraction |
| Residual constant gauge action | Preserved | Acts by simultaneous conjugation |
| State normalization | Not instantiated | The result bounds the action, not the full restricted density |
| Link Haar density | Open | Its logarithmic Jacobian is not included in the five budgets |
| Gauge-slice/Faddeev--Popov density | Open | Orbit-volume derivatives are not included |
| Locality | Finite-block local | No quasilocal polymer norm for generated interactions |
| Reflection positivity | Unchanged/unproved | No reflection-positive block-map theorem is invoked |
| Observable reconstruction | Open | No multiscale observable transport is constructed |
| Topology and center flux | Open | Principal-log contractible chart only |

## Limit and quantifier ledger

The proved statement has quantifiers

```text
for the fixed 2^4 block,
for every 0 < t <= 0.01,
for every Coulomb link-log field with every local plaquette extraction <= 0.003,
the displayed derivative and inverse estimates hold.
```

It does not quantify uniformly over:

- growing lattice volume;
- lattice spacing `a -> 0`;
- a number of RG steps `k(a) -> infinity`;
- all compact simple gauge groups;
- nontrivial bundle, center-flux, or boundary-holonomy sectors;
- the full regulated probability measure;
- a dense continuum observable algebra.

## Frontier verdict

The theorem is a C2 restricted finite-block result.  Its first failed
implication is now quantitative rather than merely existential: the analytic
chart is accepted by the local action recursion but has no probability
overlap at the calibrated endpoint.  The next proof mechanism must enlarge
the chart using `SU(2)`-specific cancellations and simultaneously control the
dependent chart complement.  Repeating the present Banach-log estimate at
more digits does not address that incompatibility.
