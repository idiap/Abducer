# SU(2) heat-kernel initialization frontier ledger

Statuses: **P** proved analytically, **N** floating computation with an analytic
series-tail bound, **C** conditional interface, **O** open.

| ID | Claim | Status | Scope or blocker |
|---|---|---:|---|
| H0 | The character convention uses generator `(1/2)Delta`, exponent `exp(-n(n+2)t/2)`, and principal action `theta^2/(2t)` | P | Fixed `SU(2)=S^3` normalization |
| H1 | The character and Poisson-image expressions represent the same central heat kernel | P/N | Poisson summation; numerical ratio cross-check |
| H2 | Pairing images gives explicit uniform derivative bounds `Q_0,...,Q_3` with a geometric omitted-image tail | P | `rho<pi/2` and declared `t_max` condition |
| H3 | On `theta<=rho`, the scaled action Hessian remainder is bounded by `t_max(A_2+B_2)` | P | Curvature logarithm chart |
| H4 | The scaled Euclidean third derivative is bounded by `4 t_max(A_3+B_3)` | P | Conservative radial-tensor bound |
| H5 | The default `(t_max,rho)=(0.2,1)` gives Hessian budget about `0.0824566` and third budget about `0.149094` | N | Double precision; analytic image tails |
| H6 | `theta(U_p)>=rho` is a conjugation-invariant one-plaquette exceptional event | P | Gauge invariant but not a block polymer |
| H7 | Its probability is enclosed by an integrated character sum plus an analytic omitted-character tail | P/N | Floating partial sum with explicit roundoff allowance |
| C1 | Declared curvature-chart derivatives propagate the local budgets by explicit chain-rule formulas | P/C | Actual block chart constants not supplied |
| B1 | The transported plaquette-log maps on the full `2^4` quotient chart satisfy useful explicit constants | O | Noncommutative BCH, slice, projection, overlap norms |
| B2 | One-plaquette tails generate a summable dependent bad-block polymer activity | O | Dependence, volume, topology, boundary sectors |
| B3 | All five Stage 06 norm components are initialized for the generated action | O | Needs B1--B2 and interaction locality |
| B4 | The recursion closes for a cutoff-diverging number of scales | O | Uniform constants and summable accumulation |
| B5 | The retained base becomes massive and survives the OS continuum limit | O | Central Clay frontier |

## Strongest defensible claim

Stage 07 is a **C2 restricted one-plaquette theorem**.  It removes the
existential constant from the radial heat-kernel action itself and supplies an
exact interface for chart composition.  It is not yet a nonlinear theorem on
the 216-plaquette block because the BCH/slice/incidence constants are open.

## First missing implication

```text
exact radial SU(2) heat-kernel initializer (proved here)
             |
             | explicit 2^4 plaquette-log/slice/projection norms (open)
             v
five-component retained/fiber action norm
             |
             | Stage 06 one-step theorem (proved)
             v
generated effective-action certificate
```

The one-plaquette probability is a genuine gauge-invariant large-field datum,
but it cannot be tensorized as though neighboring plaquettes were independent.
