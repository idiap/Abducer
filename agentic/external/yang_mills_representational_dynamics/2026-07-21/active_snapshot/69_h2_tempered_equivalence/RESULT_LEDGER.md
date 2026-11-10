# H2 Phase 1 result ledger: state-dependent tempered equivalence

## Scope

This stage proves a finite theorem for positive sub-Markov kernels on changing
finite state spaces. It does **not** construct a Yang--Mills kernel, establish
reflection positivity, identify a dense observable core, or prove a mass gap.
The claim level is C2.

The inequalities in this ledger are exact mathematical statements.  The
executable certificate uses binary floating point and tolerance checks.

## Theorem H2-TE

Let (Q_n:S_n\to S_{n+1}) be nonnegative kernels and let (V_n,W_n>0).
Denote their least weighted ceilings by

\[
 q_n^V=\max_{x\in S_n}\frac{(Q_nV_{n+1})(x)}{V_n(x)},
 \qquad
 q_n^W=\max_{x\in S_n}\frac{(Q_nW_{n+1})(x)}{W_n(x)}.
\]

Suppose the sharp two-sided equivalence constants satisfy

\[
 a_nV_n\leq W_n\leq b_nV_n,
 \qquad
 a_n=\min_{x\in S_n}\frac{W_n(x)}{V_n(x)},
 \quad
 b_n=\max_{x\in S_n}\frac{W_n(x)}{V_n(x)}.
\]

Then each step obeys

\[
 q_n^V\frac{a_{n+1}}{b_n}
 \leq q_n^W
 \leq q_n^V\frac{b_{n+1}}{a_n},
\tag{H2-TE.1}
\]

and therefore

\[
 \prod_{n<N}\frac{a_{n+1}}{b_n}
 \leq
 \frac{\prod_{n<N}q_n^W}{\prod_{n<N}q_n^V}
 \leq
 \prod_{n<N}\frac{b_{n+1}}{a_n}.
\tag{H2-TE.2}
\]

### Proof

Positivity gives

\[
 Q_nW_{n+1}\leq b_{n+1}Q_nV_{n+1}
 \leq b_{n+1}q_n^VV_n
 \leq q_n^V\frac{b_{n+1}}{a_n}W_n.
\]

This proves the upper inequality. For every (x\in S_n), positivity and the
opposite sides of the two equivalences give

\[
 \frac{(Q_nW_{n+1})(x)}{W_n(x)}
 \geq \frac{a_{n+1}}{b_n}
 \frac{(Q_nV_{n+1})(x)}{V_n(x)}.
\]

Taking maxima proves the lower inequality. Multiplication proves
(H2-TE.2). No common state space and no stationarity are used.

## Coboundary--width decomposition

Set

\[
 c_n=\sqrt{a_nb_n},
 \qquad
 \eta_n=\frac12\log\frac{b_n}{a_n}.
\]

The two logarithmic product bounds are centered on the scalar endpoint
coboundary

\[
 C_N=\log\frac{c_N}{c_0}
\]

with half-width

\[
 \Omega_N=\eta_0+\eta_N+2\sum_{n=1}^{N-1}\eta_n.
\]

Consequently,

\[
 \left|
 \log\frac{\prod_{n<N}q_n^W}{\prod_{n<N}q_n^V}
 -C_N
 \right|\leq\Omega_N.
\tag{H2-TE.3}
\]

For accumulated physical length (L_N=\sum_{n<N}\ell_n), define

\[
 m_N^V=-\frac1{L_N}\log\prod_{n<N}q_n^V,
 \qquad
 m_N^W=-\frac1{L_N}\log\prod_{n<N}q_n^W.
\]

Then

\[
 \left|m_N^W-\left(m_N^V-\frac{C_N}{L_N}\right)\right|
 \leq\frac{\Omega_N}{L_N}.
\tag{H2-TE.4}
\]

Thus a sufficient uniform tempered-equivalence condition is

\[
 \frac{|C_N|}{L_N}\longrightarrow0,
 \qquad
 \frac{\Omega_N}{L_N}\longrightarrow0.
\tag{H2-TE.5}
\]

The first condition controls scalar normalization. The second controls the
state-dependent/projective width accumulated at all intermediate levels.
Uniform bounded equivalence at every level is not by itself enough when
(L_N\asymp N): a fixed nonzero projective width produces an (O(N)) robust
distortion budget.

## Exact scalar special case

If (W_n=c_nV_n), then (a_n=b_n=c_n), every (eta_n=0), and

\[
 q_n^W=q_n^V\frac{c_{n+1}}{c_n},
 \qquad
 \prod_{n<N}q_n^W
 =\frac{c_N}{c_0}\prod_{n<N}q_n^V.
\]

Hence the scalar ambiguity is exactly a telescoping coboundary, not an
accumulated width.

## Additive defects

For

\[
 x_{n+1}\leq q_nx_n+r_n,
\]

iteration yields the sharp Duhamel bound

\[
 x_N\leq x_0\prod_{j<N}q_j
 +\sum_{k<N}r_k\prod_{j=k+1}^{N-1}q_j.
\tag{H2-AD.1}
\]

If the homogeneous transport and every post-injection tail satisfy

\[
 \prod_{j<N}q_j\leq C e^{-mL_N},
 \qquad
 \prod_{j=k+1}^{N-1}q_j
 \leq C e^{-m(L_N-L_{k+1})},
\]

then a sufficient uniform condition preserving rate (m) is

\[
 \sup_N\sum_{k<N}r_k e^{mL_{k+1}}<\infty.
\tag{H2-AD.2}
\]

Ordinary summability of (r_k) is insufficient because errors injected near
the terminal scale have no time to decay.

Both transport hypotheses are necessary.  Identity transport with all
\(r_k=0\) has zero exponentially weighted error budget but homogeneous
product and terminal iterate equal to one, so it has no positive rate.

## Executable countermodels

1. **Non-tempered chart.** Identity transport with
   (W_n=e^{m(N-n)}V_n) has raw (W)-rate (m) and raw (V)-rate zero,
   while the root weight exactly cancels the apparent contraction and the
   physical identity correlation remains one.
2. **Additive defects.** With (q_n=e^{-1}) and
   (r_n=(n+2)^{-2}), the errors are summable but the terminal effective
   rate tends to zero. The exponentially weighted budget diverges.
3. **Support growth.** A transport factor (e^{-mL}) multiplied by an
   observable reconstruction factor (e^{\gamma L}) has effective rate
   (m-\gamma). It is canceled at (gamma=m) and reversed at
   (gamma>m).
4. **Zero errors without homogeneous decay.** Identity transport has a zero
   additive budget and zero terminal rate, isolating the missing homogeneous
   hypothesis.

## Quantitative finite calibration

The canonical changing-space example has dimensions (2\to3\to2\to1),
passes every two-sided step and product check, and gives

\[
 \Omega_N=1.317139002008847,
 \qquad
 \left|
 \log(Q^W/Q^V)-\log(c_N/c_0)
 \right|=0.4816934435931375.
\]

The 64-level scalar example has exactly zero projective width and its product
ratio agrees with (c_N/c_0) to floating-point precision.

## Frontier

The first H2 physical target remains unchanged but is now more precise:
construct a same-measure reflection-positive calibration and prove that its
observable reconstruction maps have sublinear logarithmic support/norm
growth. Only after that calibration is it meaningful to attempt uniform
tempered equivalence across Yang--Mills regulator charts.
