# Conditional Partition-Ratio Frontier: Synthesis

## Strongest new result

The former normalized-comparison obstruction has split into a closed local
representation issue and an open boundary-uniform free-energy issue.

Stage 23 proves that a dependency-safe local-cylinder good event has normalized
comparison loss

```text
kappa - log(1-delta)/m.
```

At the frozen centered reference this equals
`3.01676132805e-5` per support unit, far below the target `0.2`.  The earlier
loss `3.71876` came from an unnecessarily small global `408`-dimensional ball.

Stage 24 proves the exact multichannel star-weight condition

```text
sum_i a_i b_i/(q-c_i) <= q,    c_i < q.
```

For four forced-return channels at the Stage 19 target, the combined entry
budget is `q^2=5.90624873596e-6`; the state weight stores a factor
`1/q=411.47564393`.  This clarifies that weighting transports rare-entry cost
but cannot replace it.

Stage 25 proves the positive-kernel composition law

```text
K <= exp(ell) K0,  K0 V <= kV,  RV <= rV
    => (K+R)V <= (exp(ell)k+r)V.
```

There is a strict feasible local window.  Radius `0.00614955590043` allocates
half the target to each channel and uses only `53.69%` of the maximum nonlinear
radius.  The resulting combined ceiling is `0.00243027750184`, below the
critical `0.00279270808036`.

Stage 26 reduces the missing nonlinear estimate to an exact partition ratio.
For good partition `Z_G`, bad partition `Z_B`, and weighted bad numerator
`B_V`, the bad row equals

```text
B_V(s)/((Z_G(s)+Z_B(s))V(s)).
```

The residual channel closes if a boundary-uniform free-energy charge satisfies

```text
F_* > 6.71292101139.
```

## What was falsified

- A deterministic action charge is insufficient: exponentially many bad
  microstates can cancel it.
- A pointwise good formula is insufficient: the conditional normalizer can
  collapse for a retained state.
- A state weight is insufficient if defect persistence is at least the target
  ceiling.
- The present simply connected local block cannot silently stand in for a
  genuine topology sector.

## Corrected first unproved implication

Uniformly over finite volumes, positive-mass exposure histories, retained
boundary states, and center/continuous/orbit/topology defect channels, prove

```text
B_V(s)/(Z_G_ref(s)V(s)) <= exp(-F_*),
F_* > 6.71292101139,
```

while also transporting the Stage 23 local comparison constants to those
retained states.  This is a free-energy inequality: action, Haar/chart
entropy, transition multiplicity, and boundary normalization must be handled
together.

## Remaining programme

```text
uniform weighted conditional partition ratio [OPEN]
  -> physical one-scale SU(2) K+R basin inequality [OPEN]
  -> stability under gauge-covariant RG iteration [OPEN]
  -> finite-physical-scale basin entry [OPEN]
  -> continuum OS coherence and theory identity [OPEN]
  -> Hamiltonian mass gap [OPEN].
```

## Frontier audit

The new theorems are `C2` abstract or finite results; their large finite
matrix/radius evaluations are `C1` calibrations.  They do not prove the
uniform nonlinear numerator inequality, basin entry, repeated RG, continuum
Yang--Mills, or the Clay mass gap.
