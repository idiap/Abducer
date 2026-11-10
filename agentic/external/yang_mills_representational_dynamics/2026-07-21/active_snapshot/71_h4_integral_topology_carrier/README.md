# Stage 71 — H4 integral topology carrier

## Outcome

This stage implements the H4 P1 finite-cell baseline with exact integer and
`Fraction` arithmetic.  On the standard one-cell periodic cubical quotient of
the oriented four-torus,

\[
H^2(T^4;\mathbb Z)\cong\mathbb Z^6,
\qquad
n=(n_{01},n_{02},n_{03},n_{12},n_{13},n_{23}).
\]

The Pfaffian charge

\[
q(n)=n_{01}n_{23}-n_{02}n_{13}+n_{03}n_{12}
\]

does not close under gluing unless its polarized cross term is retained:

\[
q(n+c)=q(n)+q(c)+B(n,c),
\qquad B(n,c)=\beta(n)\cdot c,
\]

where

\[
\beta(n)=(n_{23},-n_{13},n_{12},n_{03},-n_{02},n_{01}).
\]

The matrix of this map satisfies (J^2=I) and \(\det J=-1\).  Therefore
the full pairing covector reconstructs the full six-component flux.  More
strongly, every statistic that predicts (q(n+c)) for all additive contexts
(c\) must be injective in (n).  This is the exact contextual-minimality
theorem.

## Exhaustive two-block result

The declared bounded catalog is

\[
\mathcal C_1=\{-1,0,1\}^6,
\qquad |\mathcal C_1|=729.
\]

All (729^2=531{,}441) ordered pairs were composed.  Grouping first blocks
only by the scalar sector

\[
\sigma(n)=(n\bmod2,q(n))
\]

gives 112 sectors.  Of these, 111 contain multiple states.  They contain
2,908 distinct same-sector pairs, and every such pair is distinguished by
the six basis contexts.  Hence there is no context-independent operation

\[
F\bigl(\sigma(n),\sigma(c)\bigr)=\sigma(n+c)
\]

on these scalar sectors.

The regression witness is

\[
\begin{aligned}
n&=(-1,-1,-1,-1,-1,-1),\\
n'&=(-1,-1,-1,-1,1,1),\\
c&=(1,0,0,0,0,0).
\end{aligned}
\]

Both first blocks have the same center label and (q=1), but

\[
q(n+c)=0,
\qquad
q(n'+c)=2.
\]

For the exact scalar weight (w(n)=2^{-|q(n)|}), both inputs have weight
(1/2) and the context has weight (1), whereas the composites have weights
(1) and (1/4).  Thus scalar sector weights cannot determine gluing.

## Finite-cell and orientation certificates

The one-cell periodic torus has one cell for every coordinate subset, so its
cell ranks are

\[
(1,4,6,4,1).
\]

All integral cellular coboundaries vanish after the opposite-face
identifications.  Their full Smith forms therefore have rank zero and no
nonzero invariant factors; the integral cohomology is torsion-free with the
same Betti numbers.  This completes the Smith calculation for this minimal
periodic finite-cell model.

All 24 coordinate permutations are checked.  The Pfaffian changes by the
orientation sign over \(\mathbb Z\), while mod-two reduction erases that sign.
The center carrier remains additive in \(\mathbb F_2^6\).

## Claim boundary

The result is `C2`: exact finite algebra on an embedded integral-flux model.
It does **not** provide the Smith/cohomology calculation for a bounded cubical
block with relative boundary data, a boundary transgression carrier, a
complete nonabelian topology classifier, a normalized sector measure, a
uniform topology-channel bound, repeated RG, continuum Yang–Mills, or a mass
gap.  Every one of those guardrails is `false` in the canonical JSON.

## Files

- `h4_integral_topology.py` — executable exact model and certificate builder.
- `test_h4_integral_topology.py` — 13 hostile and exhaustive tests.
- `h4_integral_topology_results.json` — canonical computed results.
- `theorem_dependencies_h4_p1.json` — proved/open dependency graph.
- `RESULT_LEDGER.md` — claim-by-claim scope audit.
- `NEXT_STEP_TODOS.md` — bounded-relative and nonabelian handoff.

## Reproduction

From this directory:

```bash
python3 -m unittest -v test_h4_integral_topology.py
python3 h4_integral_topology.py --bound 1 --write h4_integral_topology_results.json
python3 -m json.tool h4_integral_topology_results.json >/dev/null
python3 -m json.tool theorem_dependencies_h4_p1.json >/dev/null
```

