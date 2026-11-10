# H1 frontier ledger

## Proved

- Finite vacuum Doob transform and stationary-state theorem.
- Reversibility for symmetric positive transfer amplitudes.
- Exact inverse-amplitude cancellation for masked bad transitions.
- Collatz--Wielandt optimality of a positive defect weight.
- Exact Perron optimality of the package's four-channel star weight.
- Positive-kernel chain iteration with root moment.
- Strict degree-18 rooted connected-cluster bound.
- Cross-stage consistency with Stages 19, 24, and 25.

## Conceptual correction

`psi` and `V` have dual roles:

```text
psi       normalizes T into the Doob dynamics;
1/psi     prices rare states in the forward exploration;
V_PF(Q)   optimizes the declared bad subkernel.
```

The last two coincide only under additional structure. A Perron vector of an
RG or exploration kernel is not automatically a physical vacuum amplitude.

## Falsified shortcuts

- Using `psi` and `1/psi` interchangeably.
- Inferring uniform inverse-weight bounds from finite-volume positivity.
- Calling an exploration Perron vector a vacuum without temporal
  reflection-positive identification.
- Optimizing a bad kernel before proving that it is the complete normalized
  physical kernel.
- Dropping the root-state moment.
- Accepting equality at the cluster threshold.

## First open physical implication

Construct the complete normalized nonlinear SU(2) retained-state kernel and a
positive vacuum-derived or exploration-Perron cost weight satisfying, uniformly
in volume, cutoff, and positive-mass history,

```text
Q V <= q V,
root_law(V) <= M,
q < 0.0027927080803578997.
```

## Claim ceiling

C2 finite/conditional theorem suite. No physical one-scale basin entry,
repeated RG, continuum construction, OS reconstruction, or mass gap.
