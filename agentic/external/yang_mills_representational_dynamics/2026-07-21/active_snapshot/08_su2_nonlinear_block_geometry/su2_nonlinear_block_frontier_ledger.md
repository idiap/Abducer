# Nonlinear block-geometry frontier ledger

Statuses: **P** proved analytically, **N** executable numerical calibration,
**C** conditional interface, **O** open.

| ID | Claim | Status | Scope or blocker |
|---|---|---:|---|
| A0 | Unit-quaternion multiplication and the exponential/logarithm conventions realize the local `SU(2)` chart | P | Principal logarithm before the cut locus |
| A1 | On `||q-1||<=delta<1`, the first three logarithm derivatives are bounded by `(1-delta)^-1`, `(1-delta)^-2`, and `2(1-delta)^-3` | P | Banach-algebra power series |
| A2 | For four link-log inputs of joint norm `r`, the product derivatives are bounded by `2`, `4`, and `8` | P | Duhamel formula and unit quaternion norm |
| A3 | The composed plaquette-log map has explicit `M_1,M_2,M_3` and derivative deviation `delta_1<=M_2 r` | P | Requires `2r<1` |
| I0 | The block has 81 vertices, 216 links, 216 plaquettes, maximum vertex degree 8, and maximum link incidence 6 | P/N | Exact enumeration; integer matrices |
| I1 | `||d0||=||d1||=sqrt(12)` and `d1` has singular-value floor `sqrt(2)` on `ker d0^T` | P/N | Product-complex spectrum; numerical cross-check |
| C0 | The full plaquette-log derivative differs from `d1` by at most `sqrt(6)M_2r` | P | Incidence aggregation |
| C1 | If that deviation is below `sqrt(2)`, the plaquette-log map is bi-Lipschitz on the convex Coulomb chart | P | Local finite chart |
| G0 | Mean-zero logarithmic gauge parameters solve the Coulomb condition by a contraction with explicit coefficient | P | Local gauge chart; residual constant conjugation remains |
| G1 | The calibrated gauge ball maps input norm `0.0002` into action-chart radius `0.003` | P/N | One contractible finite block |
| H0 | The exact heat-kernel plaquette action has a global scaled Hessian remainder about `0.74748` and third budget about `295.10` on the calibrated chart | P/N | Stage 07 radial bounds plus A3 and I0--I1 |
| H1 | Hodge-whitened retained coordinates give all five Stage 06 local norm inputs | P | Pure plaquette action on the good chart |
| H2 | The default local input gives centered transport below one and positive generated-base reference margin | P/N/C | Stage 06 algebra; defect set to zero only on the good-chart calculation |
| D0 | The link-Haar and gauge-slice/Faddeev--Popov density terms satisfy the same explicit norm | O | Not included in H0--H2 |
| D1 | The small chart carries most of the regulated measure | O/failed calibration | At `t=0.01`, `P(theta>=0.006)>0.9999` for one plaquette |
| D2 | Dependent bad blocks have summable gauge-invariant polymer activity | O | Shared links, Bianchi constraints, topology, volume and cutoff |
| R0 | Generated quasilocal interactions preserve the certificate over `k(a)->infinity` steps | O | No repeated action/locality recursion |
| R1 | Reflection positivity and observable reconstruction survive the complete RG trajectory | O | Not addressed by local marginal positivity |
| M0 | The retained theory enters a massive finite-physical-scale basin | O | Nonperturbative crossover |
| M1 | A nontrivial pure Yang--Mills OS continuum theory and Hamiltonian mass gap follow | O | Clay frontier |

## Strongest defensible result

The stage remains **C2**.  It is a rigorous restricted-model theorem that
supplies the previously missing finite-block quaternion/BCH, incidence, local
slice, and projection constants.  It also produces the first explicit local
parameter set accepted by the Stage 06 recursion.

The local chart is quantitatively much too small to be promoted to a
full-measure statement.  This failed overlap is itself the decisive output of
the calibration: local differentiability and local RG contraction do not yet
meet the probability scale of typical curvature fluctuations.

## First unproved implication

```text
explicit nonlinear good-chart block certificate (proved here)
                 |
                 | sharper chart plus Haar/FP density and
                 | dependent bad-block polymer estimate (open)
                 v
full one-step regulated Yang--Mills RG certificate
                 |
                 | uniform iteration and nonperturbative basin entry (open)
                 v
continuum reconstruction and Hamiltonian gap
```

## Strategic consequence

The next target should not merely shrink constants inside the same Banach-log
majorant.  It should seek an `SU(2)`-specific covariant derivative estimate
that uses compact-group cancellations, and it must be optimized jointly with
the large-field activity.  The success criterion is an actual overlap window
where both the local Hessian margin and the dependent exceptional-set norm are
small.
