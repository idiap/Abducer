# H3 Gate-B result ledger

## Claim ceiling

This stage proves a C2 exact finite, linearized result on the open side-two
four-cube. It proves no growing-polymer boundary law, physical boundary
measure, nonlinear `SU(2)` change of variables, continuum construction, or
mass gap.

## Exact systems

Let

\[
R_P=\bigoplus_{\ell\in P} C_6O_\ell S_\ell d_1,
\qquad
B_P=E_{U(P)^c}d_1,
\]

and let \(h_P(y)=\inf_{R_Px=y}\|B_Px\|^2\), with the metric induced on the
duplicated, centered star data. All ranks, KKT substitutions, null vectors,
and characteristic identities below are exact over \(\mathbb Q\).
For each row-coordinate system \(u=R_6x\), the executable certificate produces
matrices \(X,\Lambda\) and substitutes them into the complete equations

\[
R_6X=I,
\qquad
B_P^{\mathsf T}B_PX=R_6^{\mathsf T}\Lambda.
\]

Convexity then proves that \(X^{\mathsf T}B_P^{\mathsf T}B_PX\) is the exact
minimum-cost form, including equations omitted from the rank-locating minor.

| System | \(\operatorname{rank}R_P\) | \(\operatorname{rank}h_P\) | \(\dim\ker h_P\) | Exact characteristic data |
|---|---:|---:|---:|---|
| Adjacent pair | 10 | 10 | 0 | \((\lambda-16/19)^3(\lambda-5/4)^2(\lambda-3/2)^3(\lambda-24/11)^2\) |
| Central four | 18 | 14 | 4 | \(\lambda^4(\lambda-24/11)^2q(\lambda)^3\) |
| All eight | 24 | 17 | 7 | \(\lambda^7(\lambda-3/4)^6(\lambda-12/11)^8(\lambda-10/7)^3\) |

The central-four algebraic factor is

\[
q(\lambda)=\lambda^4-\frac{603718}{99909}\lambda^3
+\frac{15120541}{1198908}\lambda^2
-\frac{1045934}{99909}\lambda+\frac{5696}{1959}.
\]

An exact Sturm calculation isolates one simple positive root of \(q\) in
each of

\[
(0.5912,0.5913),\quad(0.9871,0.9872),\quad
(2.2091,2.2092),\quad(2.2551,2.2552).
\]

Thus the earlier floating central-four spectral groups are upgraded to
rigorously defined algebraic eigenvalues; they are not guessed rational
numbers.

## Orientation falsification

For one rooted star, the correct operator is
\((6I-J)OSd_1\). The hostile center-before-orient operator
\(O(6I-J)Sd_1\) differs in 60 entries by a rank-two matrix. Exact KKT
certification gives spill nullity zero for the correct convention and one for
the hostile convention. The old zero mode is therefore exactly spurious.

## Interpretation

Collectivity is now a theorem on this finite complex: four and seven exact
zero-spill directions occur in the central-four and all-eight systems, while
the adjacent pair remains coercive. What remains unproved is the H3 scaling
claim: these three systems do not constitute a growing family, do not identify
a boundary trace factorization, and do not show that zero modes cover the
repair-relevant bad displacement cone.
