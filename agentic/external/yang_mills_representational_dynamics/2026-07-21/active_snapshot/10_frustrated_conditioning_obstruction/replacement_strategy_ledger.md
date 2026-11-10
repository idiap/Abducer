# Replacement Strategy Ledger

The failed route took a supremum over arbitrary microscopic boundary fields.
That operation forgets the probability and energetic cost of producing a
frustrating boundary.  The replacement must retain that information.

## Candidate mechanisms

| Mechanism | Object to prove | Preserved information | Main risk | Priority |
|---|---|---|---|---:|
| good-collar conditioning | uniform tail conditioned on a gauge-invariant good annulus | local regularity and boundary admissibility | collar failures must still be summed | 1 |
| charged contour activity | activity support includes the bad plaquette and every connected frustrating staple | energetic cost of the cause | entropy and nonabelian constraints | 1 |
| multi-link block integration | integrate the full 216-link block modulo gauge before declaring it bad | shared-link dependence and Bianchi constraints | high-dimensional normalization | 2 |
| chessboard/reflection estimate | compare repeated bad patterns using reflection positivity | positivity and spatial repetition cost | event and regulator compatibility | 2 |
| stochastic domination after coarse graining | dominate coarse bad blocks, not microscopic conditionals | averaging under the true measure | proving finite-energy constants | 3 |
| labeled center/topology polymers | separate curvature, center flux, toron, and charge species | global sector identity | interactions between species | 1 |

## Recommended next theorem

Let `G(A)` be a gauge-invariant good-collar event around a block `B`, and let
`F(B)` be failure of the Stage 09 curvature/orbit chart inside `B`.  Prove a
finite-volume estimate

```text
P(F(B) | G(A), exterior gauge-invariant data) <= p_good(t,rho)
```

uniformly over exterior data compatible with `G(A)`, together with a contour
activity for collar failure:

```text
sup_L sup_o sum_{X containing o}
  exp(alpha |X|) |z_collar,L(X)| < delta.
```

The two estimates must share the same `t`, chart radius, collar thickness, and
block scale.  The second estimate must count center/topological labels rather
than hiding them inside an unsigned error.

## Required representation

Use a typed defect label

```text
Defect =
  CurvatureExit(rho)
  | OrbitAtlasFailure(chart_id)
  | CenterFlux(z)
  | BoundaryHolonomy(class)
  | TopologicalCharge(q)
  | GeneratedInteractionFailure(norm_id).
```

Blocking must specify how each label is transported, merged, discharged, or
retained.  A scalar bad-block bit loses exactly the information exposed by the
frustrated-conditioning theorem.

## Stop conditions

- Do not take a supremum over arbitrary microscopic exterior links.
- Do not use the independent Stage 09 tail as a marginal of the link measure.
- Do not delete center or topological labels when summing contours.
- Do not claim basin entry until activities are uniform in volume and summable
  through the required number of RG steps.

