# Stage 12 Frontier Ledger

## Exact finite theorem

The center-valued link field is a one-cochain `x`, with negative plaquettes
`y=d1 x` over `GF(2)`.  On the side-two four-cube:

```text
rank(d1)=136, rank(d2)=80, rank(d1)+rank(d2)=216,
d2 d1=0.
```

Hence every center Bianchi cocycle is exact.  Integer-bitmask syndrome search
exhausts all completions with zero through three additional plaquettes and
proves that the Stage 10 incident pattern has full curvature weight at least
five.  A one-link assignment attains five.

## Contour theorem

The maximum common-three-cell (Bianchi) adjacency degree is 20 and every
nonempty exact center contour has size at least three.  The shared-link graph,
used later for ordinary bad-set clustering, has degree 18.  If a negative plaquette has relative weight
`q`, then

```text
sum_{X contains p} exp(alpha |X|) |z(X)|
 <= exp(3 alpha) q^3 20^4 / (1-exp(alpha)20^2 q).
```

At `alpha=0.1`, the sufficient threshold is
`q<0.00226209354509`.  For the declared calibration `q=1e-4`, the rooted
upper bound is approximately `2.25965e-7`.

## Boundary of the result

The exact minimum five is a center-sector statement.  Continuous `SU(2)`
fields may spread curvature rather than remain at `+I` or `-I`.  Extending the
charged activity to that continuum is not proved here.

Strongest level: `C2`.
