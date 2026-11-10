# SU(2) quotient-fiber frontier ledger

Statuses: **P** proved here, **C** implication proved from explicit hypotheses,
**N** numerical/executable calibration, **I** imported standard theorem,
**O** open.

| ID | Claim | Status | Scope or blocker |
|---|---|---:|---|
| Q0 | The `2^4` cubical cochain complex has 81 vertices, 216 links, and 216 plaquettes, with `d1 d0=0` | P | Exact finite complex |
| Q1 | `rank(d0)=80`, `rank(d1)=136`, and flat tangent fields are exactly infinitesimal gauge fields | P | Contractibility of the block |
| Q2 | The physical scalar tangent quotient has dimension 136; after tensoring with `su(2)` it has dimension 408 | P | One finite block |
| Q3 | The 24 displayed boundary coarse-face fluxes have exact scalar rank 17 | P | Exact rational elimination and coarse-cube topology |
| Q4 | The scalar conditional fiber has dimension 119 and the `su(2)` fiber has dimension 357 | P | Q2 and Q3 |
| Q5 | On `ker(d0^T)`, `||d1 A||^2 >= 2 ||A||^2` | P | Product Hodge-spectrum theorem for the frozen block |
| Q6 | The same coercivity lower bound holds on the retained-data fiber | P | Fiber is a subspace of the physical quotient |
| Q7 | The computed scalar fiber minimum is approximately `3.438447187` | N | Floating-point spectral calibration; theorem uses the certified bound 2 |
| G1 | For the tangent Gaussian measure, conditioning changes the mean but not the centered fiber covariance | P | Exact finite Gaussian theorem |
| G2 | Full-coordinate base response has computed operator norm about `0.393174`; centered response is exactly zero | P/N | Exact zero after centering; full norm numerical |
| L1 | Local nonlinear `SU(2)` heat-kernel action differs from the quadratic tangent action by `O(rho/t)+O(1)` in Hessian on a fixed small-field chart | P | Existential finite-block constants from the heat-kernel parametrix and BCH analyticity |
| L2 | If the scaled Hessian remainder is `eta<2`, the nonlinear fiber is `(2-eta)/t` strongly convex | P | Direct Hessian perturbation theorem |
| L3 | A centered cross-gradient bound `chi/t` gives `W_2` response at most `chi/(2-eta)` | P | Common convex fiber chart; LSI and transport inequality |
| L4 | There exists a sufficiently small local tube for which the centered good-fiber coefficient is below one | P | Local existential theorem; no explicit cutoff-uniform radius supplied |
| F1 | An exact gauge-covariant nonlinear block disintegration with global orbit-atlas compatibility exists | O | Local slice and constant-rank construction do not cover exceptional orbits |
| F2 | Explicit constants remain stable for generated effective actions over all ultraviolet RG steps | O | Requires a Balaban-type action norm and recursion |
| F3 | Bad blocks and topology admit a dependent, cutoff-uniform summable polymer bound | O | Large-field/topological frontier |
| F4 | The retained base enters a massive basin at finite physical scale | O | Nonperturbative crossover; central mass-generation frontier |
| F5 | Continuum Schwinger functions exist, are nontrivial pure Yang--Mills, satisfy OS axioms, and have a dense observable core | O | Continuum construction and theory identity |

## Strongest defensible claim

The package reaches **C2**: a rigorous local/restricted block theorem. It is the
first stage in the programme that uses an explicit four-dimensional cubical
gauge complex with `su(2)` color multiplicity. It does not reach a regulated
full-measure four-dimensional theorem because F1--F3 are open, and it does not
generate infrared mass because F4 is open.

## What the result establishes

The finite block has a genuine quotient-fiber coercivity margin once gauge
directions and retained curvature data are separated. In the Gaussian tangent
theory, all dependence on the retained data is transported by the conditional
mean; the centered fiber law is exactly independent of the base. Analyticity
then makes this property locally stable for the nonlinear heat-kernel action.

## What it does not establish

1. The local Coulomb/constant-rank chart is not a global gauge quotient.
2. The good-field law is not the full block conditional law; its complement
   must become the defect channel.
3. Existential small-field constants are not yet useful for iteration through
   `k(a) -> infinity` RG steps.
4. Fiber contraction controls forgotten fluctuations. It does not make the
   retained base massive.
5. No continuum limit, universality theorem, or Hamiltonian gap follows.

## First next theorem

Derive explicit constants in the local nonlinear estimates for the exact
`SU(2)` heat kernel and prove that they are stable under one generated
effective-action RG step. The required certificate is

```text
t || Hess_F(S_t - Q_t) || <= eta < 2,
t || grad_F V_y - grad_F V_y' || <= chi d_Y(y,y'),
chi/(2-eta) < 1,
```

with a gauge-invariant bad-block remainder and all constants expressed in a
norm that can be iterated.
