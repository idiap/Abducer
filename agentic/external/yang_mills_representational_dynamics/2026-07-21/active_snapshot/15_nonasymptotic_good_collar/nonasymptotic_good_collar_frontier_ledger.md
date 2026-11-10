# Stage 15 Frontier Ledger

## Proved

For `m` staples in a common `eta`-ball and any auxiliary `delta` satisfying
`rho^2>m(eta+delta)^2`, the target conditional event obeys

```text
P_bad <= v(delta)^(-1) (rho/sin rho) c_t^(m+1)
         exp(-(rho^2-m(eta+delta)^2)/(2t)).
```

Here `v(delta)=(delta-sin(2delta)/2)/pi`, and `c_t` is the explicit local
Poisson-image ratio.  The result is finite-time and uniform over coherent,
possibly noncommuting staple families.

## Calibration

| Quantity | Value |
|---|---:|
| frozen `t` | `3e-6` |
| selected frozen `delta` | `8.22875586e-4` |
| frozen raw log upper bound | `14.97453169` |
| Stage 14 critical weight | `0.00279270808` |
| crossing time | `8.99420304e-7` |
| crossing `delta` | `3.36486781e-4` |

The frozen finite-time bound is therefore trivial despite the favorable
small-time rate.  This is a prefactor obstruction, not a contradiction.

## Open

No collar-occurrence probability, adaptive block exposure, repeated RG,
continuum limit, or mass gap is proved.  The first open implication is a
history-uniform nonlinear coherent/charged collar alternative.
