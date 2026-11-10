# Stage 17 Frontier Ledger

## Proved comparison

For `d mu_D proportional exp(-R) d nu_D` and
`osc_D R <= kappa`, every event satisfies

```text
mu_D(A) <= exp(kappa) nu_D(A)
        <= exp(kappa-log nu(D)) nu(A).
```

If `R(0)=dR(0)=0` and `||d^2R||<=H` on a convex radius-`r` ball, then
`kappa<=H r^2`.

## Stage 08 calibration

| Quantity | Value |
|---|---:|
| physical Gaussian dimension | `408` |
| inner radius | `0.003` |
| Hessian remainder | `0.705133286` |
| oscillation loss | `6.34620e-6` |
| certified inner-ball log mass | `-803.252660` |
| total loss per 216 plaquettes | `3.71876234` |
| Stage 14 target | `0.2` |

An abstract global-ball radius about `0.02463` would meet the declared loss,
and radius `0.03657` would give reference log mass `-0.1`.  These are
diagnostics only: Stage 08 does not certify its nonlinear chart at those
radii.

## First open implication

Prove a gauge-covariant chart atlas or a larger block chart whose total
reference coverage and overlap/Jacobian costs meet the nonlinear comparison
budget.
