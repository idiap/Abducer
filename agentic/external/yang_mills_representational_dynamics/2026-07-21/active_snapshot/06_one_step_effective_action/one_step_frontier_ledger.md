# One-step effective-action frontier ledger

Statuses: **P** proved here, **N** executable numerical witness, **I** imported
standard theorem, **C** conditional application, **O** open.

| ID | Claim | Status | Scope or blocker |
|---|---|---:|---|
| R0 | The five-component scaled derivative norm is a well-defined local effective-action norm | P | Fixed finite retained/fiber chart |
| R1 | `eps_fiber < lambda_fiber` leaves fiber margin `mu=lambda_fiber-eps_fiber` | P | Hessian perturbation |
| R2 | The conditional minimizer satisfies `||Dz_*|| <= eps_cross/mu` | P | Interior minimizer on the full finite fiber |
| R3 | On a radius-`r` centered tube, `chi <= r(tau_cross+tau_fiber eps_cross/mu)` | P | Declared third-derivative bounds |
| R4 | Centered conditional transport is at most `K_fiber=chi/mu` | P/I | Strong convexity plus LSI/T2 |
| R5 | Exact marginalization gives `eta_good=eps_base+eps_cross^2/mu` | P/I | Differentiation plus Brascamp--Lieb covariance |
| R6 | A bad/good ratio with scaled derivative budgets contributes at most `zeta_hessian+zeta_gradient^2` | P | Exact derivative of `log(1+delta)` |
| R7 | Positive marginal state and conditional observable transport are exact | P | Finite-dimensional Fubini/disintegration |
| R8 | Orthogonal residual gauge/frame covariance survives marginalization | P/N | Invariant domain and action |
| R9 | The Gaussian implementation equals the exact Schur complement and respects the theorem bound | N | Deterministic finite matrix witness |
| I1 | Exact `SU(2)` heat-kernel and generated interactions satisfy the declared norm with cutoff-uniform inputs | O | Local initialization constants not supplied |
| I2 | The defect ratio obeys the declared gauge-invariant `C^2` activity bound | O | Large fields, dependencies, topology |
| I3 | The one-step package preserves a uniform polymer locality norm | O | No spatial interaction decomposition in the finite theorem |
| I4 | Reflection positivity is preserved or quantitatively recovered | O | Marginal positivity is weaker than OS reflection positivity |
| I5 | The recursion closes for `k(a)->infinity` steps | O | Requires uniform initialization and summable error flow |
| I6 | The retained base becomes massive at finite physical scale | O | Central nonperturbative crossover |

## Strongest defensible result

The stage remains at **C2**, but it advances the restricted theorem from a
one-block input certificate to an exact one-step output recursion.  It proves
what follows if the local derivative and defect norms are established; it does
not establish those norms for the full regulated theory.

## First missing implication

The earliest unresolved link is initialization:

```text
exact nonlinear SU(2) heat-kernel block plus generated interaction
             |
             |  explicit cutoff-aware derivative and defect bounds (open)
             v
five-component Stage 06 norm
             |
             |  one-step theorem (proved here)
             v
generated retained action and centered-fiber certificate
```

This prevents the recursion from being described as a Yang--Mills RG theorem
without qualification.
