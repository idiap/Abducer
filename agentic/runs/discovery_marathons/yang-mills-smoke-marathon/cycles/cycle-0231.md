# cycle-0231

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Finite Schur-Feshbach tangent cone for Wilson quotient blocks

## Candidate Lemma

Let q_epsilon be a Hermitian n by n same-theory Wilson quotient block with q_epsilon=11^*+epsilon H+epsilon^2 K+o(epsilon^2). Set e=n^{-1/2}1, P=I-ee^*, A=PHP, and C=P(K-n^{-1}Hee^*H)P. If q_epsilon is PSD for all sufficiently small epsilon>0, then A>=0 on 1^perp and Pi C Pi>=0 on ker A. Conversely, if A>0 on 1^perp, or A>=0 and Pi C Pi>0 on ker A, then q_epsilon is PSD for all sufficiently small epsilon>0. A negative vector for A or for Pi C Pi is a valid finite OS falsifier.

## Definitions

- source object: a finite diagonal-normalized reflected Wilson quotient matrix q_epsilon=N_epsilon oslash B_epsilon whose collar-collapse OPE is Hermitian in operator norm.
- target object: positivity of the intended same-theory OS matrix after undoing the boundary anomaly, tested on the locked finite Wilson block.
- controlled interface: Schur complement against the rank-one vacuum vector followed by Feshbach reduction on 1^perp maps Wilson OPE coefficients H,K to PSD tangent-cone tests.
- same-theory condition: diagonal one-body Wilson congruences are fixed before forming q_epsilon, so a negative reduced form is a mixed boundary defect rather than a renormalization choice.
- e=n^{-1/2}1 is the normalized vacuum direction and P=I-ee^* removes the OS rank-one direction.
- Pi denotes the orthogonal projection in P C^n onto ker(PHP).

## Assumptions

- n is finite and epsilon>0 approaches zero through collar-separated regulated observables.
- q_epsilon is Hermitian and has an operator-norm expansion through order epsilon^2 with remainder o(epsilon^2).
- The diagonal normalization is locked before the quotient is formed, so pure one-body factors are not counted as mixed defects.
- The vacuum eigenvalue <e,q_epsilon e> stays positive near n, which follows from the expansion.

## Equations

- rank-one collar expansion: `q_\varepsilon={\bf 1}{\bf 1}^*+\varepsilon H+\varepsilon^2 K+R_\varepsilon,\qquad \|R_\varepsilon\|=o(\varepsilon^2)`. Valid when: Valid when the normalized finite Wilson quotient block has a uniform Hermitian expansion in operator norm.
- vacuum Schur complement: `q_\varepsilon\ge0\iff \lambda_\varepsilon>0\ \text{and}\ F_\varepsilon:=Pq_\varepsilon P-Pq_\varepsilon e\,\lambda_\varepsilon^{-1}\,e^*q_\varepsilon P\ge0,\quad \lambda_\varepsilon=e^*q_\varepsilon e`. Valid when: Applies after the vacuum rank-one eigenvalue remains isolated for sufficiently small positive collar parameter.
- corrected second-order form: `F_\varepsilon=\varepsilon A+\varepsilon^2 C+o(\varepsilon^2),\qquad A=PHP,\quad C=P\bigl(K-n^{-1}Hee^*H\bigr)P`. Valid when: Requires the same-theory boundary OPE expansion and Hermitian normalization before taking the Schur complement.
- null-sector gate: `q_\varepsilon\ge0\ \Rightarrow\ A\ge0\ \text{on}\ 1^\perp,\qquad \Pi C\Pi\ge0\ \text{on}\ \ker A`. Valid when: Valid when A has a well-defined nullspace and the remainder is o epsilon squared in finite dimension.

## Attempted Derivation

- Normalize the finite quotient block so q_0=11^* and the same Wilson algebra labels all q_epsilon.
- Decompose C^n=span{e} orthogonal sum 1^perp, with e=n^{-1/2}1.
- Compute lambda_epsilon=e^*q_epsilon e=n+O(epsilon), hence lambda_epsilon>0 for small epsilon.
- Use the exact finite-dimensional Schur complement: q_epsilon>=0 iff the P-block complement F_epsilon is PSD.
- Expand Pq_epsilon P=epsilon PHP+epsilon^2 PKP+o(epsilon^2) and Pq_epsilon e=epsilon PHe+O(epsilon^2).
- The rank-one direction contributes epsilon^2 n^{-1}PHee^*HP, giving C=P(K-n^{-1}Hee^*H)P rather than PKP.
- Apply the elementary finite PSD perturbation lemma to F_epsilon=epsilon A+epsilon^2 C+o(epsilon^2): negative A is immediately visible; if A vanishes on a vector, the first possible obstruction is the projected C form.
- For higher degeneracy, repeat the same Schur-Feshbach reduction on the positive spectral subspace of A and then on null sectors.

Blocking gap: There is no blocking gap for the finite second-order tangent-cone theorem. The remaining gap is analytic: no concrete Yang-Mills reflected Wilson hairpin OPE has yet supplied uniform h, ell, hence H,K.

## Falsifiers

- A realized Wilson block with v^*PHPv<0 for some v perpendicular to 1 is an immediate same-theory falsifier.
- A realized Wilson block with PHP>=0 but v in ker(PHP) and v^*P(K-n^{-1}Hee^*H)Pv<0 is the corrected second-order falsifier.
- A boundary log-OPE whose pure one-body part does not cancel under the locked quotient indicates that the same-theory normalization was changed.
- A finite block requiring only pairwise damping tests but failing the Schur-Feshbach determinant test shows the branch has regressed to an invalid obstruction ladder.

## Learning

Cycle 231 proves the finite second-order Schur-Feshbach gate rigorously. The corrected form is C=P(K-n^{-1}Hee^*H)P, not PKP, because the rank-one vacuum direction contributes through the Schur complement. Pure one-body Wilson factors cancel, so a negative reduced C-form is a genuine mixed-boundary falsifier. The branch is not looping, but the next contribution must compute H,K for an actual reflected Wilson collar/hairpin block.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Pick the smallest nontrivial reflected Wilson hairpin triple with a common boundary footprint, write log q_{ij}=epsilon h_{ij}+epsilon^2 ell_{ij}, remove one-body terms, then compute PHP and Pi P(ell+1/2 h∘h-n^{-1}hee^*h)P Pi.

# Backtrack from witness loop to finite Schur-Feshbach tangent cone

## Candidate Lemma

Finite Schur-Feshbach tangent-cone theorem. Let \(\mathcal H=\mathcal K\oplus\mathcal R\) be finite dimensional, \(A_0=0_{\mathcal K}\oplus D\) with \(D>0\), and \(M(t)=A_0+tB+t^2C+r(t)\), \(r(t)=o(t^2)\), self-adjoint. Put \(G=B_{KK}\), \(L=\ker G\), and \(Q=C_{KK}-B_{KR}D^{-1}B_{RK}\). If \(M(t)\ge0\) for all small \(t>0\), then \(G\ge0\) and \(P_LQP_L\ge0\). Conversely, these two inequalities are exactly the second-order tangent-existence conditions: there is a self-adjoint \(\tilde r(t)=o(t^2)\) with \(A_0+tB+t^2C+\tilde r(t)\ge0\). If \(P_LQP_L\ge \eta P_L\), \(\eta>0\), then the positivity conclusion is stable for every sufficiently small prescribed remainder \(r(t)=o(t^2)\).

## Definitions

- source object: a finite-dimensional self-adjoint pencil \(M(t)=A_0+tB+t^2C+o(t^2)\) with \(A_0\ge0\) and an isolated positive block \(D=A_0|_{\mathcal R}\).
- target object: the first and corrected second-order tangent cone inequalities on \(\ker A_0\), expressed after Schur-Feshbach elimination of \(\mathcal R\).
- controlled interface: positivity of the original pencil is transferred to positivity of the Schur complement without changing the finite operator data.
- same-theory condition: the blocks \(A_0,B,C\), the inverse \(D^{-1}\), and the Schur complement all come from the same finite pencil, with no replacement by an auxiliary Gaussian or OS model.

## Assumptions

- \(\mathcal H\) is finite dimensional and complex Hilbert.
- \(D=D^*>0\) on \(\mathcal R\), so \(M_{RR}(t)\) remains invertible for small positive \(t\).
- \(B=B^*\), \(C=C^*\), and \(\|r(t)\|/t^2\to0\).
- The positivity direction is one-sided, \(t\downarrow0\), matching collar or hairpin perturbations with nonnegative scale.

## Equations

- block base point: `A_0=\begin{pmatrix}0&0\\0&D\end{pmatrix},\qquad D>0`. Valid when: Valid when the null directions are isolated from the positive block by a finite spectral gap.
- Schur equivalence: `M(t)\ge0\iff M_{RR}(t)>0\ \text{ and }\ S(t):=M_{KK}(t)-M_{KR}(t)M_{RR}(t)^{-1}M_{RK}(t)\ge0`. Valid when: Valid when the lower-right block stays strictly positive and invertible for all sufficiently small positive parameters.
- inverse expansion: `M_{RR}(t)^{-1}=D^{-1}+O(t)`. Valid when: Applies after finite-dimensional norm control gives Neumann expansion around the positive block D.
- corrected second-order Schur form: `S(t)=tB_{KK}+t^2\big(C_{KK}-B_{KR}D^{-1}B_{RK}\big)+o(t^2)`. Valid when: Requires the same finite pencil expansion and ignores only terms contributing order three or smaller.
- first tangent inequality: `B_{KK}\ge0`. Valid when: Valid when positivity of S(t) is tested on fixed vectors in the kernel block and divided by t.
- second tangent inequality: `P_{\ker B_{KK}}\big(C_{KK}-B_{KR}D^{-1}B_{RK}\big)P_{\ker B_{KK}}\ge0`. Valid when: Valid when the first-order form vanishes on L and the Schur complement is divided by t squared.

## Attempted Derivation

- The previous nontriviality-witness branch was looping, so I backtracked to contribution move (1): prove the finite Schur-Feshbach tangent-cone theorem.
- Decompose \(\mathcal H=\ker A_0\oplus(\ker A_0)^\perp=\mathcal K\oplus\mathcal R\) and write \(A_0=0\oplus D\), \(D>0\).
- For small \(t>0\), \(M_{RR}(t)=D+O(t)>0\), hence positivity of \(M(t)\) is equivalent to positivity of its Schur complement \(S(t)\).
- Use \((D+tB_{RR}+O(t^2))^{-1}=D^{-1}+O(t)\). Since \(M_{KR}(t)=tB_{KR}+O(t^2)\), the first nontrivial Feshbach correction is \(t^2B_{KR}D^{-1}B_{RK}\).
- Therefore \(S(t)=tG+t^2Q+o(t^2)\), with \(G=B_{KK}\) and \(Q=C_{KK}-B_{KR}D^{-1}B_{RK}\).
- For arbitrary \(x\in\mathcal K\), \(0\le t^{-1}\langle x,S(t)x\rangle\to\langle x,Gx\rangle\), proving \(G\ge0\).
- For \(x\in L=\ker G\), \(0\le t^{-2}\langle x,S(t)x\rangle\to\langle x,Qx\rangle\), proving \(P_LQP_L\ge0\).
- Conversely, if the two inequalities hold, add a positive correction \(t^2\epsilon(t)P_N\), where \(N\) is the remaining zero eigenspace in the reduced cone and \(\epsilon(t)\downarrow0\) slowly enough, to dominate boundary cross terms while preserving \(o(t^2)\) at the original scale.
- If \(P_LQP_L\) is strictly positive, no corrective remainder is needed: the \(L\) block has size \(t^2\), the \(L^\perp\) block has size \(t\), and finite-dimensional block estimates absorb all \(o(t^2)\) errors.

Blocking gap: The theorem is rigorous for necessity, tangent-existence, and strict-gap stability. The remaining gap is the full classification of fixed-remainder positivity in the semidegenerate case \(P_LQP_L\ge0\) with a nontrivial kernel; third-order data decide it.

## Falsifiers

- falsifier: find \(M(t)\ge0\) with \(D>0\) but \(B_{KK}\) has a negative vector; Schur division by t says this cannot occur.
- falsifier: find \(M(t)\ge0\) with \(x\in\ker B_{KK}\) and \(\langle x,Qx\rangle<0\); Schur division by \(t^2\) says this cannot occur.
- falsifier: use the uncorrected condition \(C_{KK}\ge0\) and ignore \(-B_{KR}D^{-1}B_{RK}\); a coupled two-block pencil can pass the uncorrected test and fail the valid Schur test.
- falsifier: claim semidefinite \(P_LQP_L\ge0\) gives positivity for every fixed representative; \(G=\mathrm{diag}(0,1)\), \(Q_{12}=1\) disproves that overstatement.

## Learning

The branch was looping on non-Gaussian witnesses; the useful move is the finite Schur-Feshbach cone theorem. The corrected second-order obstruction is exactly the Feshbach term \(-B_{KR}D^{-1}B_{RK}\). The word valid now has teeth: fixed-remainder positivity is stronger than tangent-existence, and a boundary falsifier exposes the difference.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the smallest symbolic H,K Wilson collar/hairpin block split, identify \(D\), \(B_{KK}\), and \(Q=C_{KK}-B_{KR}D^{-1}B_{RK}\), then test PHP against the valid corrected second-order inequality.

# Pivot from stalled observable density to finite Schur-Feshbach tangent cone

## Candidate Lemma

Let \(X_0\in\mathrm{Herm}(E)\), \(E=P\oplus Q\), satisfy \(X_0\ge0\), \(\ker X_0=P\), and \(C_0=QX_0Q>0\). For Hermitian \(Y,Z\), write \(A_1=PYP\), \(B_1=QYP\), \(A_2=PZP\), and let \(\Pi\) project in \(P\) onto \(\ker A_1\). Then \(Z\in T^2_{\mathsf S_+}(X_0;Y)\), with \(\operatorname{dist}(X_0+tY+t^2Z/2,\mathsf S_+)=o(t^2)\), iff \(A_1\ge0\) and \(\Pi(A_2-2B_1^*C_0^{-1}B_1)\Pi\ge0\). This is the finite corrected PHP theorem.

## Definitions

- source object: a finite Hermitian pencil \(X_0+tY+t^2Z/2\) on the same truncated Gram space \(P\oplus Q\).
- target object: the parabolic second tangent cone of the positive semidefinite cone at \(X_0\) in direction \(Y\).
- controlled interface: Schur-Feshbach elimination of the massive \(Q\)-block, retaining the exact order-two correction \(-2B_1^*C_0^{-1}B_1\).
- same-theory condition: \(X_0,Y,Z,P,Q\) are computed with one inner product, one null quotient, and one finite observable truncation.

## Assumptions

- Finite-dimensional complex Hilbert space; no domain or closure issue is hidden.
- \(C_0=QX_0Q\) has a strictly positive spectral lower bound.
- The second tangent cone is the distance version: \(\operatorname{dist}(X_0+tY+t^2Z/2,\mathsf S_+)=o(t^2)\).
- The projection \(P\) is the exact kernel projection of \(X_0\), not an approximate low-mode cutoff.

## Equations

- block data: `X_0=\begin{pmatrix}0&0\\0&C_0\end{pmatrix},\quad Y=\begin{pmatrix}A_1&B_1^*\\B_1&C_1\end{pmatrix},\quad Z=\begin{pmatrix}A_2&B_2^*\\B_2&C_2\end{pmatrix}.`. Valid when: Valid when the basis is adapted to the exact kernel of X0 and QX0Q is strictly positive.
- Schur expansion: `S(t)=A(t)-B(t)^*C(t)^{-1}B(t)=tA_1+\frac{t^2}{2}\bigl(A_2-2B_1^*C_0^{-1}B_1\bigr)+o(t^2).`. Valid when: Valid when Ct remains invertible for small positive t and the pencil has a second order expansion.
- tangent-cone criterion: `Z\in T^2_{\mathsf S_+}(X_0;Y)\iff A_1\ge0\ \text{and}\ \Pi\bigl(A_2-2B_1^*C_0^{-1}B_1\bigr)\Pi\ge0.`. Valid when: Applies after diagonal normalization of PYP and only on the null directions left by first order PHP.
- H,K,L convention: `X(t)=H+tK+t^2L+o(t^2)\Rightarrow \Pi\bigl(PLP-PKQ(QHQ)^{-1}QKP\bigr)\Pi\ge0.`. Valid when: Valid when H is nonnegative, P is ker H, QHQ is positive, and Z equals 2L.

## Attempted Derivation

- Backtracked from the repeated gauge-invariant density loop because it was not producing a contribution-making invariant.
- Adapted the finite pencil to \(E=P\oplus Q\) with \(P=\ker X_0\), so cross terms of \(X_0\) vanish and \(QX_0Q=C_0>0\).
- For \(M(t)=X_0+tY+t^2Z/2\), the \(Q\)-block \(C(t)\) is positive for small \(t>0\).
- PSD of \(M(t)\) is equivalent, up to bounded congruence and hence up to \(o(t^2)\) distance, to PSD of the Schur complement \(S(t)\).
- Expanding \(C(t)^{-1}=C_0^{-1}+O(t)\) and \(B(t)=tB_1+O(t^2)\) gives \(S(t)=tA_1+t^2(A_2/2-B_1^*C_0^{-1}B_1)+o(t^2)\).
- Diagonalize \(A_1\) on \(P\) as \(0\oplus \Lambda\), \(\Lambda>0\). The positive \(\Lambda\)-block absorbs order \(t^2\) cross terms.
- The reduced null block has leading order \(t^2\Pi(A_2/2-B_1^*C_0^{-1}B_1)\Pi\), so negative spectrum of this block is exactly a non-o\((t^2)\) distance obstruction.
- Thus the finite theorem is proved for the parabolic tangent cone, and the 2x2 hairpin test realizes the correction explicitly.

Blocking gap: No blocking gap remains for the finite-dimensional tangent-cone theorem; the remaining gap is extracting actual Wilson collar/hairpin H,K,L coefficients from a same-theory construction.

## Falsifiers

- falsifier: \(H=\mathrm{diag}(0,1)\), off-diagonal \(K_{12}=1\), and \(L=0\) passes naive \(PHP=0\) but violates the corrected second-order form.
- If \(QHQ\) has zero modes, \((QHQ)^{-1}\) is undefined and the Schur-Feshbach theorem is not valid without a further reduction.
- If \(P\) is an approximate low-energy projection rather than \(\ker H\), the formula can give a false obstruction or false pass.
- If H, K, and L are taken from different Wilson normalizations or different null quotients, the same-theory condition fails.

## Learning

The real finite obstruction is not PHP alone. Off-diagonal hairpin coupling creates the negative correction \(-PKQ(QHQ)^{-1}QKP\), and the 2x2 falsifier shows why naive first-order positivity is mathematically invalid.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Extract the smallest Wilson collar/hairpin Gram pencil, identify \(c,a,b,\ell\), and test both naive PHP and the corrected Schur-Feshbach second-order inequality.
