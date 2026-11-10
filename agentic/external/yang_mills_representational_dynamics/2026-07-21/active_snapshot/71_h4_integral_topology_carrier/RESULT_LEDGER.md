# H4 P1 result ledger

| ID | Statement | Status | Level | Evidence |
|---|---|---:|---:|---|
| H4-P1.1 | The one-cell periodic cubical (T^4) has integral cell ranks and Betti numbers ((1,4,6,4,1)), zero coboundaries, trivial Smith diagonals, and (H^2\cong\mathbb Z^6). | proved | C2 | exact finite-cell certificate and tests |
| H4-P1.2 | The mod-two carrier is additive and has (2^6=64) labels. | proved | C2 | exact coordinate reduction |
| H4-P1.3 | Pfaffian polarization is governed by the symmetric matrix (J) with (J^2=I), \(\det J=-1\), and signature ((3,3)). | proved | C2 | exact determinant, matrix multiplication, and exhaustive polarization probes |
| H4-P1.4 | The Pfaffian changes by the orientation sign under all coordinate permutations; its mod-two reduction is orientation-blind. | proved | C2 | all 24 permutations tested |
| H4-P1.5 | Six basis-context pairings reconstruct the full flux. | proved | C2 | explicit inverse (J^{-1}=J) |
| H4-P1.6 | Every statistic sufficient to predict (q(n+c)) for all contexts is injective. | proved | C2 | nondegeneracy proof below |
| H4-P1.7 | Center plus scalar Pfaffian charge is not closed under two-block composition. | proved | C2 | 531,441 exact compositions and explicit witness |
| H4-P1.8 | Scalar charge-sector weights determine gluing. | refuted | C2 | equal input weights (1/2) produce composite weights (1) and (1/4) in one common context |
| H4-P1.9 | A bounded cubical block with relative cohomology and interface transgression is complete. | open | — | not represented by the periodic one-cell quotient |
| H4-P1.10 | The carrier classifies nonabelian (SU(2)) lattice topology. | open | — | embedded integral-flux algebra only |
| H4-P1.11 | A normalized physical topology-sector kernel or uniform sector bound follows. | open | — | no Yang–Mills conditional measure constructed |

## Contextual-minimality proof

Let (s:\mathbb Z^6\to S) satisfy

\[
s(n)=s(m)\Longrightarrow q(n+c)=q(m+c)
\quad\text{for every }c\in\mathbb Z^6.
\]

Taking (c=0) gives (q(n)=q(m)).  Subtracting the two polarized formulas
then gives

\[
B(n-m,c)=0\quad\text{for every }c.
\]

In the fixed basis this says ((n-m)^T J=0).  Since \(\det J=-1\), (J) is
unimodular over \(\mathbb Z\), and hence (n=m).  Thus (s) is injective.
Equivalently, the complete pairing covector

\[
\bigl(B(n,e_1),\ldots,B(n,e_6)\bigr)
\]

is already equivalent to retaining (n), because (J^{-1}=J).

## Composition certificate

The redundant carrier

\[
\tau(n)=\bigl(n,n\bmod2,q(n),\beta(n)\bigr)
\]

composes through

\[
\begin{aligned}
n''&=n+n',\\
z''&=z+z'\pmod2,\\
\beta''&=\beta+\beta',\\
q''&=q+q'+\beta(n)\cdot n'.
\end{aligned}
\]

Bilinearity gives the cocycle identity and therefore associativity.  In this
fixed torus basis, (n) is the coordinate-minimal carrier; (z,q,\beta) are
redundant audit fields.  For a bounded region, however, boundary/relative
data may be additional rather than redundant, which is the next open gate.

