# Adaptive Nonlinear Bridge: Frontier Synthesis

> **Stage 19--22 update.**  The scalar adaptive conditional remains a valid
> sufficient route, but it is no longer the preferred frontier.  A
> state-weighted subkernel retains the entry cost of rare hostile boundary
> states.  Dependency-aware local concentration reduces the required
> four-link radius to `0.00602316`, and a sharp plaquette-log Hessian theorem
> proves nonlinear control through radius `0.01145379`.  See
> `STATE_WEIGHTED_FRONTIER_SYNTHESIS.md` for the current frontier.

## Strongest new conclusions

1. The coherent-staple theorem now has a rigorous finite-time `SU(2)` form.
   Its finite-volume prefactor is decisive: it closes the Stage 14 weight near
   `t=8.9942e-7`, but not at the frozen `t=3e-6` witness.
2. Incoherent collars carry an exact continuous nonabelian charge.  However,
   combining that charge with the good-collar threshold yields maximal frozen
   exponent `0.9339`, far below the needed collar rate.
3. Nonlinear action oscillation inside the certified Stage 08 chart is tiny.
   The unresolved cost is normalization and chart coverage: the available
   408-dimensional inner-ball lower bound loses about `3.7188` per plaquette,
   against target `0.2`.
4. Activity construction is not logically necessary for the bad-set process.
   A history-uniform adaptive conditional bound gives exact Bernoulli
   stochastic domination and the desired connected-cluster estimate.
5. Joint intersection bounds alone cannot supply that conclusion; the
   two-site anticorrelated counterexample proves the missing quantifier is
   genuinely adaptive.

## Revised first unproved implication

Construct a gauge-covariant multi-link/block exploration of the complete
finite-volume `SU(2)` heat-kernel measure and prove, after every positive
exposure history,

```text
P(next block is bad | exposed history) <= 0.002430277501841998,
```

uniformly in volume.  The exposure must retain enough boundary information to
charge center and continuous collar frustration, and it must use a chart atlas
whose coverage and overlap costs fit the nonlinear comparison budget.

## Why this is a sharper programme

The preceding frontier mixed three distinct questions: finite-time heat-kernel
prefactors, collar energetics, and event-to-activity conversion.  The first two
are now quantified, and the third is replaced by a proved stochastic theorem.
What remains is a concrete analytic construction with explicit quantifiers,
not a generic request for a polymer expansion.

## Remaining Clay chain

```text
adaptive multi-link SU(2) conditional bound [OPEN]
  -> Bernoulli domination and one-scale cluster control [PROVED CONDITIONALLY]
  -> gauge-covariant RG propagation with summable errors [OPEN]
  -> finite-physical-scale rigidity-basin entry [OPEN]
  -> cutoff/volume limits preserving OS data [OPEN]
  -> observable-complete reconstruction [OPEN]
  -> positive Hamiltonian mass gap [OPEN].
```

The strongest defensible level remains `C2`: rigorous finite and restricted
theorems with a substantially narrower analytic frontier.  No continuum
Yang--Mills construction or mass-gap proof is claimed.
