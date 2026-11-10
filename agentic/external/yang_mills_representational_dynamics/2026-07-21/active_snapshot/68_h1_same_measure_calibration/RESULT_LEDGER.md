# H1 same-measure result ledger

## Scope

This stage closes the finite representational loop left open by earlier H1
calibrations: the Gibbs edge weight, temporal transfer, Perron vacuum, Doob
dynamics, and bad subkernel are now derived from one matrix (T).  It does not
model the nonlinear (SU(2)) retained-boundary-state measure.

## Proved finite results

Let (T) be a strictly positive symmetric positive-definite two-state matrix,
with eigenvalues (lambda _0>lambda _1>0), positive Perron vector (psi),
and declared edge mask (0\leq M_{ij}\leq1).  Define

\[
 P_{ij}=\frac{T_{ij}\psi_j}{\lambda_0\psi_i},\qquad
 Q_{ij}=M_{ij}P_{ij},\qquad
 V_i=\frac{\max_k\psi_k}{\psi_i}.
\]

The algebra proves, and the floating-point implementation tests with explicit
tolerances:

1. `T` is a positive Gram kernel, the finite certificate used here for
   bond-reflection positivity. The executable certificate records a factor
   `T = L L^T`; hence the reflected edge quadratic form is a sum of squares.
2. (P) is stochastic and reversible with
   (pi_i=\psi_i^2/\sum_k\psi_k^2).
3. (Q\leq P) entrywise and is a subkernel selected from the same finite
   measure.
4. The inverse-vacuum cancellation is exact:

   \[
   \frac{(QV)_i}{V_i}=\frac{1}{\lambda_0}
   \sum_j M_{ij}T_{ij}.
   \]

5. The stationary root moment is exactly
   (∑_i\pi_iV_i), and the finite temporal gap is
   (m_T=-\log(\lambda_1/\lambda_0)>0).

For the nontrivial-vacuum calibration at (θ=0.05):

| Quantity | Value |
|---|---:|
| weighted bad ceiling | `0.054862500859364255` |
| scalar bad ceiling | `1.0` |
| stationary root moment | `1.0474931563783176` |
| maximum inverse-vacuum weight | `19.95012499921876` |
| finite temporal gap | `5.99647077621632` |

The scalar bad ceiling can therefore be one even though the weighted ceiling
is small, now with both quantities derived from the same temporal/Gibbs
measure.

## Refuted implication

For

\[
 T_\delta=\begin{pmatrix}1&\delta\\\delta&1\end{pmatrix},
 \qquad
 M=\begin{pmatrix}0&1\\1&0\end{pmatrix},
 \qquad 0<\delta<1,
\]

the vacuum is unique, (V=(1,1)), and

\[
 q(\delta)=\frac{\delta}{1+\delta}\longrightarrow0,
 \qquad
 m_T(\delta)=-\log\frac{1-\delta}{1+\delta}\longrightarrow0.
\]

Hence an upper bound on a same-measure masked bad channel, even with finite
reflection positivity and exact inverse-vacuum weighting, does not force a
uniform lower bound on the full temporal gap.

## Claim boundary

Classification: **C2 finite algebraic theorem with a tolerance-certified
floating-point realization, plus a finite-family countermodel**.  “Exact” in
the formulas above refers to the mathematics, not bit-exact executable
arithmetic.

Not established:

- a nonlinear (SU(2)) retained-state kernel;
- boundary-, volume-, and cutoff-uniform root moments;
- an inequality making the bad mask observable on every nonvacuum temporal
  mode;
- continuum existence or any OS axiom package;
- a Yang--Mills Hamiltonian mass gap.

The first open mathematical implication is therefore not another
normalization identity.  It is an observability or coercivity theorem linking
the selected defect channel to the entire orthogonal temporal spectrum.
