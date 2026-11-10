# H10 finite gauge-quotient observable-recovery ledger

## Scope and claim ceiling

This stage proves an exact C2 theorem on one finite **Z2 gauge toy model**.  It
is not a nonlinear SU(2) block map and it supplies no cutoff, volume, density,
Osterwalder--Schrader, or mass-gap theorem.

The graph has two vertices joined by three parallel edges.  A fine
configuration is

\[
 x=(e_0,e_1,e_2)\in X=\{-1,+1\}^3,
\]

and a local gauge element \(g=(g_L,g_R)\in \mathbb Z_2^2\) acts by

\[
 (g\cdot x)_i=g_L e_i g_R.
\]

The global diagonal subgroup is the action kernel, so every effective orbit
has two elements.

## Exact quotient and reconstruction theorem

Define two independent Wilson products

\[
 W_{01}(x)=e_0e_1,\qquad W_{12}(x)=e_1e_2
\]

and the block map and reconstruction

\[
 B(x)=(W_{01}(x),W_{12}(x)),\qquad
 R(y_1,y_2)=(1,y_1,y_1y_2).
\]

Then, exactly on the finite spaces,

\[
 B(g\cdot x)=B(x),\qquad B\circ R=\operatorname{id}_Y,
\]

and \(R Bx\) is gauge equivalent to \(x\).  Moreover,

\[
 R B(g\cdot x)=R Bx,
\]

so the canonical recovery projection erases gauge copies.  Direct enumeration
finds eight fine configurations, four quotient points, and four fibres, each
equal to one effective two-point gauge orbit.

## Declared separating observable algebra

The declared rational invariant algebra has character basis

\[
 \mathcal B=\{1,W_{01},W_{12},W_{02}\},\qquad
 W_{02}=W_{01}W_{12}=e_0e_2.
\]

For coefficients \(c=(c_0,c_1,c_2,c_3)\in\mathbb Q^4\), let

\[
 O_c=c_0+c_1W_{01}+c_2W_{12}+c_3W_{02},
 \qquad \lVert O_c\rVert_{\mathcal A}=\sum_i|c_i|.
\]

The exact character table has rank four.  Consequently this basis spans every
rational function on the four-point quotient and separates every pair of
physical orbit labels.  Character multiplication is closed by XOR of the two
exponents, and the declared coefficient norm is submultiplicative.

For any declared observable, define

\[
 e_{\infty,O}(B,R)=\max_{x\in X}|O(RBx)-O(x)|,
\]

with the analogous uniform-fine-space \(L^1\) error.  Every basis error, and
hence every algebra error by linearity, is exactly zero.  In particular the
product loop \(W_{02}\), deliberately excluded from the initial probe family
\(\{1,W_{01}\}\), is recovered exactly by the complete map.

## One-step and two-step composition theorem

For a deterministic quotient endomap \(f:Y\to Y\), define the
observable-indexed defect

\[
 e_O(f)=\max_{y\in Y}|O(f(y))-O(y)|.
\]

For any \(f,g:Y\to Y\), the exact two-step estimate is

\[
 e_O(g\circ f)\le e_O(f)+e_O(g).
\]

Indeed, for each \(y\), insert and subtract \(O(f(y))\); the second increment
is bounded by \(e_O(f)\), while the first is bounded by \(e_O(g)\) evaluated
at the point \(f(y)\in Y\).  Maximization proves the claim with amplification
constant one.

For \(O=(W_{01}+W_{12})/2\), take \(f\) to flip the first loop coordinate and
\(g\) to flip the second.  The one-step errors are \(1\) and \(1\), while the
two-step error is \(2\), so the bound is sharp.  Exhaustive enumeration checks
all 256 quotient endomaps, all ordered map pairs, and all four basis
observables: 262,144 exact inequalities, with minimum slack zero.

## Logical counterexamples

### Gauge-copy erasure without physical recovery

The constant block \(B_{\rm collapse}(x)=(1,1)\) is exactly gauge invariant,
but it maps four physical orbit labels to one.  Its \(W_{01}\) and \(W_{12}\)
supremum recovery errors are both \(2\).  Thus vertical erasure does not imply
horizontal physical recovery.

### Invariant recovery without gauge-copy erasure

Retain \((W_{01},W_{12},e_0)\), including the gauge-copy sign.  The
reconstruction

\[
 R_{\rm label}(y_1,y_2,s)=(s,sy_1,sy_1y_2)
\]

obeys \(R_{\rm label}B_{\rm label}=\operatorname{id}_X\), so it recovers every
invariant observable (indeed the whole fine configuration).  But the label
\(e_0\) flips under an effective gauge transformation.  Recovery therefore
does not imply erasure.

### Incomplete probes do not certify recovery

The quotient map \(h(y_1,y_2)=(y_1,-y_2)\) exactly preserves the initial probes
\(1,W_{01}\), yet its errors on \(W_{12}\) and \(W_{02}\) are both \(2\).
Agreement on a nonseparating probe list does not imply observable-algebra
recovery.

## Strongest proved relation

The strongest relation is an exact quotient together with exact recovery of
the complete rational invariant observable algebra on this declared finite
Z2 graph.  The uniformity domain consists only of its eight configurations
and four local gauge elements.

## Physical frontier

Still unproved are a nonlinear SU(2) quotient/block rule, a chart-uniform or
intrinsic reconstruction, volume- and cutoff-uniform observable errors,
closure and density of a continuum temporal observable core, OS
reconstruction, and a positive Yang--Mills mass gap.  No item in this ledger
licenses any of those implications.

