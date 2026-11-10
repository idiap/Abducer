# Stage 19 Frontier Ledger

## Proved

If a bad-transition subkernel `Q` and a weight `V>=1` obey `QV<=qV`, then a
specified chain of `n` bad extensions has probability at most `M q^n`, where
`M` is the root-state `V` moment.  On a graph of degree `Delta`,

```text
sum_{X connected, root in X} exp(alpha |X|) P(B_X)
 <= M exp(alpha) q / (1-exp(alpha) Delta^2 q).
```

The proof uses only positive kernels, induction, and the depth-first-walk
connected-set count.  Independence and full stochastic domination are not
required.

## Strict gain over scalar conditioning

For

```text
Q = [[0,q^2],[1,0]],   V = [1,1/q],
```

the scalar row ceiling is one while `QV=qV`.  Rare entry into the high-cost
state pays for the following forced bad transition.

## Frontier

The theorem changes the correct nonlinear target but does not establish it.
The first open implication is to construct a gauge-covariant retained state,
bad subkernel, and physical weight for the complete finite-volume `SU(2)`
measure with weighted ceiling below `0.0027927080803578997`.

Strongest level: `C2` abstract theorem plus finite exact calibration.

