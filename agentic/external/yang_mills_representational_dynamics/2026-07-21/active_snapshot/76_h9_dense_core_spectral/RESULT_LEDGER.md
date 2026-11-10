# H9 dense-core spectral result ledger

## Scope and claim level

This stage proves the finite self-adjoint core of H9 at C2 and calibrates it
executablely. It does not construct an Osterwalder--Schrader continuum theory,
prove density of Yang--Mills observables in its physical Hilbert space, or
identify a reconstructed Hamiltonian with continuum pure Yang--Mills.

## Finite theorem

Let (H=H^astgeq0) act on a finite-dimensional Hilbert space, let
(Omega) be a normalized zero-energy vacuum, and put
(mathcal H_0=Omega^perp). For a centered probe space
(Dsubseteqmathcal H_0), define its time-translation invariant spectral
closure by

\[
 K(D)=\bigoplus_{\lambda\in\operatorname{spec}(H|_{\mathcal H_0})}
 \operatorname{ran}(P_\lambda|_D).
\]

Then:

1. (K(D)) is the smallest (H)-reducing subspace containing (D).
2. The core-visible gap is
   \[
   m_{\rm vis}=\min\{\lambda:P_\lambda D\neq0\}
   =\min\operatorname{spec}(H|_{K(D)}).
   \]
3. (K(D)=\mathcal H_0) exactly when
   \[
   \sum_\lambda \operatorname{rank}(P_\lambda|_D)
   =\dim\mathcal H_0.
   \]
   Thus every multiplicity direction must be visible; merely seeing every
   distinct eigenvalue is insufficient.
4. If for a dense core (C\subseteq\mathcal H_0),
   \[
   |\langle x,e^{-tH}y\rangle|
   \leq e^{-mt}\|x\|\,\|y\|,
   \qquad x,y\in C, t\geq0,
   \]
   continuity extends this bound to all of (mathcal H_0), so
   (|e^{-tH}|_{\mathcal H_0}|leq e^{-mt}). The spectral theorem then
   gives (operatorname{spec}(H|_{\mathcal H_0})\subseteq[m,\infty)).
5. Without density, exactly the same argument certifies only (K(D)), with
   gap (m_{\rm vis}). No conclusion follows for (K(D)^perp).

For item 1, time translation multiplies each spectral projection by the
nonzero scalar (e^{-t\lambda}); finite spectral interpolation recovers the
individual (P_\lambda D). Item 3 follows because the eigenspaces are
orthogonal. For item 4, approximate arbitrary unit (x,y) by core vectors
and pass to the limit in the bounded bilinear form. In finite dimension every
dense linear subspace is already the full space; the approximation proof is
stated because it is the form needed for an eventual OS Hilbert space.

## Decisive counterexamples

For

\[
 H=\operatorname{diag}(0,0.4,1.2),\qquad \Omega=e_0,
\]

the one-probe core (D=\operatorname{span}\{e_2\}) has visible gap (1.2)
while the true gap is (0.4). Its invariant rank is one inside the
two-dimensional (mathcal H_0). The norm-compatible (e^{-1.2t}) bilinear
bound is correct on (K(D)) and false as a statement about the unobserved
full space.

A second fixture uses
(H=\operatorname{diag}(0,0.4,0.4,1.2)). A probe can see the value (0.4)
but span only one direction of its two-dimensional eigenspace. Hence
(m_{\rm vis}=m_{\rm true}) does not imply density or state separation.

Finally,

\[
 T_a=\operatorname{diag}(1,e^{-a^2})
\]

has positive exponent (a^2) per transfer step for every (a>0), but a
step represents physical time (a), so its physical rate is (a	o0). This
rules out promoting cutoff-wise step decay to a uniform continuum gap.

## Executable certificate

The module computes the true gap, the visible gap, per-eigenspace visible
ranks, the invariant generated rank, density, positive-transfer rates, and
the operator norm representing the supremum of all Hilbert-norm-compatible
bilinear forms. The all-time rate decision is tied to the computed visible
spectral edge, so a sample containing only (t=0) cannot certify a positive
rate. Twenty tests cover positive, boundary, incomplete,
multiplicity, gapless, non-self-adjoint, negative, malformed-vacuum, signed
transfer, expansive transfer, and overaggressive-rate cases.

The computation uses floating-point diagonalization. The theorem above is the
mathematical result; the executable fixtures are calibration and adversarial
checks, not formal proof-assistant certificates.

## Frontier audit

| Implication | Status |
|---|---|
| finite spectral closure and rank criterion | proved |
| dense-core bilinear decay to operator norm | proved |
| operator-norm decay to finite spectral gap | proved |
| density of a gauge-invariant temporal core in the OS physical norm | open |
| uniform positive decay in physical time | open |
| OS continuum construction and regulator convergence | open |
| identity with four-dimensional pure Yang--Mills | open |
| continuum Yang--Mills mass gap | not claimed |

The first unproved physical implication is not another finite spectral lemma.
It is the joint construction of the OS physical space and proof that a named
gauge-invariant temporal core is dense there, together with a uniform
physical-time bound for that same core.
