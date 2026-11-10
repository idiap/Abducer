# Target 57 frontier

## Cocycle theorem

For changing state spaces and weights,

```text
Q_n V_{n+1} <= q_n V_n
```

composes to a chain bound with factor `product q_n`, including the initial
root moment. This is the correct representational transport law.

## Physical-length correction

A constant contraction `q<1` per geometrically growing RG level gives
`q^n=R^{-gamma}` in the terminal scale `R=b^n`; it does not by itself give
`exp(-mR)`. A positive physical mass requires the stronger cocycle

```text
product q_n <= exp(-m sum ell_n)
```

for physical increments `ell_n`.

## First open physical implication

Construct the physical block/RG kernels and prove length-scaled contraction
with uniform errors while preserving positivity, locality, retained-state
sufficiency, and observables.

Claim ceiling: C2 finite cocycle and C3 conditional length criterion.
