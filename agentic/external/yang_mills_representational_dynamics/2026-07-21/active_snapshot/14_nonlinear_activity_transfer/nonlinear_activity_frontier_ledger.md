# Stage 14 Frontier Ledger

## Proved abstract connected-event transfer

For every connected plaquette set `X`, assume

```text
mu(B_X and coherent collar) <= exp(-(J-kappa)|X|),
mu(B_X and collar failure)  <= exp(-K|X|).
```

Then

```text
mu(B_X) <= q_eff^|X|,
q_eff = exp(kappa-J)+exp(-K).
```

With plaquette adjacency degree 18, the rooted weighted sum is bounded by

```text
exp(alpha) q_eff / (1-exp(alpha)18^2 q_eff).
```

This theorem is exact and does not assume independence.  Its left side is a
rooted connected bad-event envelope, not an already constructed Mayer/Ursell
activity.

## Frozen budget

| Quantity | Value |
|---|---:|
| dependent Gaussian `J` | 6.69010107 |
| declared `kappa` | 0.2 |
| declared `K` | 7.0 |
| good-channel weight | 0.00151839554 |
| collar-failure weight | 0.000911881966 |
| `q_eff` | 0.00243027750 |
| critical weight | 0.00279270808 |
| branching ratio | 0.870222534 |
| rooted sum upper | 0.0206959813 |

If collar failure were absent, the comparison loss could be as large as
`0.809357554`.  At `kappa=0.2`, the exact convergence threshold requires
`K>6.66534843`; the declared target `K=7` is strict.

## First unproved implication

For the complete finite-volume heat-kernel `SU(2)` link measure, uniformly in
volume and admissible exterior gauge-invariant data, prove both

```text
mu(B_X and G_X) <= exp(0.2 |X|) mu_Gauss(B_X^lin),
mu(B_X and not G_X) <= exp(-7 |X|)
```

for the same `t`, `rho`, `eta`, block geometry, and connected support.  The
second inequality must charge center, boundary-holonomy, orbit-atlas, and
topological labels to `X` rather than optimize them away.

After these inequalities, either construct the corresponding nonlinear
polymer activities with the same envelope or prove a stochastic domination
route from the event sum.  This conversion is also open.

## Claim audit

| Claim | Status |
|---|---|
| two-tier probability/activity lemma | proved |
| numerical budget algebra | proved |
| Mayer/Ursell activity identification or stochastic domination | open |
| finite declared scale-registry summation | proved conditionally on entries |
| nonlinear good-collar comparison for full `SU(2)` | open |
| nonlinear charged collar rate for full `SU(2)` | open |
| scale-uniform RG iteration | open |
| continuum construction and mass gap | open |

Strongest level: `C2`.  The next target is no longer a generic request for
"dependence control"; it is the pair of quantified inequalities above.
