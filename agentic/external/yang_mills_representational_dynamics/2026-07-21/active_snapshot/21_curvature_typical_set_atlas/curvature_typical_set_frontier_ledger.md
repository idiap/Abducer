# Stage 21 Frontier Ledger

## Proved local concentration theorem

For jointly Gaussian blocks `A_j` of dimension `r` whose marginal covariance
operators are bounded by `lambda`, dependence is irrelevant to the union
estimate

```text
P(max_j ||A_j|| > sqrt(lambda)(sqrt(r)+sqrt(2 log(N/delta)))) <= delta.
```

At `t=3e-6` on the finite `2^4` Coulomb Gaussian, the degree-18 target gives:

| local object | certified radius |
|---|---:|
| one link, dimension 3 | `0.00402583` |
| four-link plaquette input, dimension 12 | `0.00602316` |
| linear curvature, dimension 3 | `0.00928852` |

The prior global-ball diagnostic `0.02463088` is therefore not the correct
local coverage requirement.

## Exact group atlas

The `+I` and `-I` exponential charts of radius `pi/2` cover `SU(2)`.  The
normalized Haar density is `(sin r/r)^2/(2 pi^2)`, with ratio at most
`(pi/2)^2` on each chart.  Relative tree gauge has constant Haar gauge volume.

## Remaining gap

The existing nonlinear fiber/base certificate closes at radius `0.003` but
does not close at the required local radius `0.00602316`.  Stage 22 audits that
smaller, now correctly posed overlap deficit.

Strongest level: `C2` analytic local-union/atlas theorem plus `C1` finite
spectral calibration.

