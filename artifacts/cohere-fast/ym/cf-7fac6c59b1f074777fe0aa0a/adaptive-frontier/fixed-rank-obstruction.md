# Fixed-rank recovery obstruction

Status: conditional candidate theorem
Consequence: the alpha=1, p=1 pilot cannot be an observable-density proof

## Proposition

Let \(\mathcal H\) be the candidate continuum OS Hilbert space and let
\(W_n\) be regulated carrier spaces with \(\dim W_n\le M\). Suppose a fixed
choice of at most \(M\) carrier generators is transported by same-theory
recovery maps into \(\mathcal H\), and every recovered generator converges in
the Hilbert norm. Then the limiting carrier

\[
W=\operatorname{span}\{\psi_1,\ldots,\psi_M\}
\]

has dimension at most \(M\), is closed, and cannot be dense in any physical
sector of dimension greater than \(M\).

## Proof

The recovered limits provide at most \(M\) vectors, so their span has dimension
at most \(M\). Every finite-dimensional subspace of a Hilbert space is closed.
If the physical sector has dimension greater than \(M\), this closed subspace is
proper and therefore not dense.

The conclusion is unchanged if one formulates recovery by strongly convergent
orthogonal projections of rank at most \(M\): a strong limit cannot acquire
rank greater than the common finite bound. If no coherent limit exists, the
same-theory recovery or limit-commutation gate fails instead.

## Application to alpha=1, p=1

The pilot carrier has exactly three declared channels: charge-even fundamental,
adjoint, and charge-even sextet. Hence coherent recovery gives a continuum
carrier of dimension at most three. Conditional on the vacuum-orthogonal YM
sector having dimension greater than three, this carrier cannot be dense.

This is a structural obstruction, not a Yang--Mills existence or mass-gap
theorem. It fixes the role of the pilot: it may test reflection positivity,
UV collapse, recovery, and visible transfer behavior, but never global density.

## Required quantifier order for the viable route

A density claim needs an unbounded inclusion degree. Schematically,

\[
\forall\psi\in\mathcal H_{\perp\Omega}\;\forall\varepsilon>0\;
\exists p\;\exists n_0\;\forall n\ge n_0\;\exists v_{p,n}\in V_{\alpha,p,n}:
\|J_{n,\alpha,p}v_{p,n}-\psi\|<\varepsilon.
\]

The spectral estimate must then be uniform over this growing family, while
Gram conditioning, recovery error, physical-time calibration, cutoff, and
volume errors remain controlled. A convenient finite carrier with fixed p
cannot replace this diagonal-limit obligation.

## Next bounded derivation target

Specify a predeclared growth law \(p=p(n)\to\infty\) and an error decomposition

\[
\delta_{\rm total}=\delta_{\rm approximation}(p)
+\delta_{\rm recovery}(p,n)+\delta_{\rm Gram}(p,n)
+\delta_{\rm time}(n)+\delta_{\rm volume}(n),
\]

then determine which rates are sufficient for density and for a uniform
fixed-physical-time transfer upper bound. No such rates are currently supplied.
