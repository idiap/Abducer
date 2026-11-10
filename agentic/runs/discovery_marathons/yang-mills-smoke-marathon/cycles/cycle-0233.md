# cycle-0233

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Three-hairpin Wilson H,K gate and corrected second-order threshold

## Candidate Lemma

For the first three-hairpin Wilson collar block with overlap data \(\ell_{12}=4,\ell_{13}=\ell_{23}=1\), the first-order Schur-Feshbach gate passes with one null direction, and the corrected second-order obstruction is exactly \(T=8m^2+2R_{12}-4R_{13}-4R_{23}\). If \(T<0\), the same-theory OS quotient is indefinite for all sufficiently small collars; if \(T>0\), this finite block is positive through second order.

## Definitions

- source object: the normalized finite Wilson collar quotient \(q_\delta=\widehat N_\delta\oslash\widehat B_\delta\) for three reflected hairpin observables with common boundary footprint and overlap matrix \(\ell_{12}=4,\ell_{13}=\ell_{23}=1,\ell_{ii}=0\).
- target object: positivity of the intended continuum OS matrix on the three-dimensional locked Wilson span after the collar parameter \(\delta\downarrow0\).
- controlled interface: Schur-Feshbach reduction of \(q_\delta\) near the rank-one vacuum matrix \(J=\mathbf1\mathbf1^*\), retaining the first nonzero reduced coefficient.
- same-theory condition: \(H,K,R\) are extracted from the same renormalized Wilson observables before and after collar collapse, with diagonal normalization only and no boundary counterterm, algebra enlargement, or pair-dependent replacement.

## Assumptions

- \(q_\delta=J+\delta H+\delta^2K+O(\delta^3)\) as Hermitian matrices, uniformly on this finite Wilson block.
- The leading mixed boundary damping is \(H_{ij}=-m\ell_{ij}\) for \(i\ne j\), \(H_{ii}=0\), with \(m>0\).
- The second coefficient is parameterized as \(K_{ij}=\frac12m^2\ell_{ij}^2+R_{ij}\) for \(i\ne j\), \(K_{ii}=0\), where \(R\) is the connected second boundary-OPE polarization after diagonal normalization.
- The collar remainder is small enough that the sign of the first nonzero Feshbach coefficient controls the corresponding small eigenvalue.

## Equations

- normalized quotient expansion: `q_\delta=\mathbf1\mathbf1^*+\delta H+\delta^2K+O(\delta^3),\qquad (q_\delta)_{ii}=1`. Valid when: Valid when the reflected Wilson collar quotients admit a uniform finite-block boundary OPE expansion after diagonal normalization.
- first hairpin damping matrix: `H=-m\begin{pmatrix}0&4&1\\4&0&1\\1&1&0\end{pmatrix},\qquad m>0`. Valid when: Valid when the three chosen hairpins have boundary overlap lengths four, one, and one in the locked normalization.
- first-order tangent gate: `P=I-\frac13\mathbf1\mathbf1^*,\quad v=(1,-1,0),\quad \eta=(1,1,-2),\quad v^*Hv=8m,\quad PH\eta=0`. Valid when: Applies after projecting away the rank-one vacuum direction and testing the two-dimensional zero-sum tangent space.
- second coefficient split: `K_{ij}=\frac12m^2\ell_{ij}^2+R_{ij}\quad(i\ne j),\qquad K_{ii}=0`. Valid when: Valid when the exponential square of the leading damping is separated from the connected second boundary polarization.
- corrected second-order form: `C=P\left(K-\frac19H\mathbf1\mathbf1^*H\right)P,\qquad \eta^*C\eta=8m^2+2R_{12}-4R_{13}-4R_{23}`. Valid when: Requires the Schur complement of the vacuum eigenline before judging the null direction of the first-order kernel.
- determinant falsifier: `\det q_\delta=2m\left(8m^2+2R_{12}-4R_{13}-4R_{23}\right)\delta^3+O(\delta^4)`. Valid when: Valid when the positive first-order tangent eigenvalue is separated and the third-order remainder is uniform for this block.

## Attempted Derivation

- Normalize the same-theory Wilson quotient so that all diagonal entries are one and the vacuum limit is \(J=\mathbf1\mathbf1^*\).
- Insert the three-hairpin overlap data into \(H_{ij}=-m\ell_{ij}\), giving the explicit matrix \(-m[[0,4,1],[4,0,1],[1,1,0]]\).
- Project to \(\mathbf1^\perp\). The vector \(v=(1,-1,0)\) has positive first-order value \(8m\), while \(\eta=(1,1,-2)\) satisfies \(PH\eta=0\).
- Eliminate the vacuum eigenline by the Schur complement. Since \(H\eta=-2m\mathbf1\), the rank-one correction subtracts \(\eta^*(1/9)H\mathbf1\mathbf1^*H\eta=4m^2\).
- Use \(K_{ij}=\frac12m^2\ell_{ij}^2+R_{ij}\) to compute \(\eta^*K\eta=12m^2+2R_{12}-4R_{13}-4R_{23}\).
- Subtract the vacuum correction and obtain \(T=8m^2+2R_{12}-4R_{13}-4R_{23}\).
- Multiplying the large vacuum eigenvalue \(3\), the positive tangent eigenvalue \(4m\delta\), and the null eigenvalue \((T/6)\delta^2\) gives \(\det q_\delta=2mT\delta^3+O(\delta^4)\).

Blocking gap: The actual Yang-Mills value of the connected second boundary-OPE polarization \(R\) has not been computed, and the required uniform \(O(\delta^3)\) collar remainder is still an analytic estimate.

## Falsifiers

- falsifier: a boundary OPE computation giving \(2R_{12}-4R_{13}-4R_{23}<-8m^2\), which makes the finite OS determinant negative for small collars.
- falsifier: failure of the expansion \(q_\delta=J+\delta H+\delta^2K+O(\delta^3)\) uniformly on reflected Wilson hairpin blocks.
- falsifier: a pair-dependent boundary renormalization needed to define \(R\), because that violates the same-theory condition even if a modified quotient stays positive.
- falsifier: a different leading hairpin overlap matrix for the regulated Wilson representatives, since then the computed PHP gate is not testing the intended block.
- falsifier: a nonuniform third-order remainder large enough to swamp the sign of \(T\) as \(delta\downarrow0\).

## Learning

Cycle 233 extracts the first concrete finite Wilson hairpin gate rather than restating the OS obstruction ladder. The leading Gaussian boundary damping is safe: after the Schur correction the null-channel threshold contains a positive \(8m^2\). Length-linear second terms cancel. The only immediate same-theory danger is a sufficiently negative connected second boundary-OPE polarization in the combination \(2R_{12}-4R_{13}-4R_{23}\).

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Write \(R_{ij}\) as the connected second cumulant of the reflected Wilson hairpin boundary OPE in one fixed regulator, then evaluate the combination \(2R_{12}-4R_{13}-4R_{23}\) for the overlap pattern \((4,1,1)\); first test local length-linear, quadratic-overlap, and residual connected kernels separately.

# Finite Schur-Feshbach tangent cone proof and boundary falsifier

## Candidate Lemma

For a fixed finite Hermitian space and coefficient convention A_0+tB+t^2C, the second-order contingent cone of the positive semidefinite cone at A_0 along B is characterized by B_{KK}\succeq0 and P_L(C_{KK}-B_{KR}D^{-1}B_{RK})P_L\succeq0, where K=ker A_0, R=K^\perp, D=A_0|_R>0, and L=ker B_{KK}.

## Definitions

- source object: a finite-dimensional Hermitian jet A_0+tB+t^2C+o(t^2) with A_0\succeq0, K=\ker A_0, R=K^\perp, and D=A_0|_R\ge\delta I_R.
- target object: the one-sided second-order contingent cone T_+^{(2)}(A_0;B) of the positive semidefinite cone at A_0 along B.
- controlled interface: replace positivity of the full jet by positivity of the Schur complement over the uniformly positive R-block.
- same-theory condition: K,R,D,B,C are computed in the same finite Hermitian space and the same Loewner cone; no cutoff, observable, or inner product is changed.
- L:=ker B_{KK} inside K, after imposing the first-order condition B_{KK}\succeq0.
- Q:=C_{KK}-B_{KR}D^{-1}B_{RK}, the corrected second-order Feshbach form.

## Assumptions

- The space is finite-dimensional over C or R, and all matrices are Hermitian/self-adjoint.
- The parameter is one-sided, t down to 0 through positive values.
- R-block positivity is uniform: D\ge\delta I_R for some delta>0.
- All remainders are in operator norm, so o(t^2) is meaningful on the fixed space.
- The t^2C convention is used; no hidden factor 1/2 is present.

## Equations

- second-order cone definition: `\mathcal T_+^{(2)}(A_0;B)=\{C:\exists t_n\downarrow0,\ E_n=o(t_n^2),\ A_0+t_nB+t_n^2C+E_n\succeq0\}`. Valid when: Valid when second-order tangent vectors use the t^2 C coefficient convention rather than half-acceleration notation.
- block jet near the face: `A(t)=\begin{pmatrix}tB_{KK}+t^2C_{KK}+o(t^2)&tB_{KR}+t^2C_{KR}+o(t^2)\\tB_{RK}+t^2C_{RK}+o(t^2)&D+tB_{RR}+t^2C_{RR}+o(t^2)\end{pmatrix}`. Valid when: Valid when the jet is measured in operator norm on a fixed finite-dimensional Hermitian space.
- R-block inverse expansion: `A_{RR}(t)^{-1}=D^{-1}-tD^{-1}B_{RR}D^{-1}+O(t^2)`. Valid when: Valid when D has a positive spectral gap and t is sufficiently small for Neumann expansion.
- Schur-Feshbach expansion: `S(t)=A_{KK}(t)-A_{KR}(t)A_{RR}(t)^{-1}A_{RK}(t)=tB_{KK}+t^2Q+o(t^2)`. Valid when: Valid when the R-block stays uniformly positive, so Schur complement positivity is equivalent to full positivity.
- parabolic cone characterization: `C\in\mathcal T_+^{(2)}(A_0;B)\iff B_{KK}\succeq0\ \text{and}\ P_LQP_L\succeq0,\quad L=\ker B_{KK}`. Valid when: Valid when tangent membership means existence of a positive semidefinite lifting with o(t^2) error.
- boundary falsifier for fixed paths: `S(t)=\begin{pmatrix}t&t^2\\t^2&0\end{pmatrix}=t\begin{pmatrix}1&0\\0&0\end{pmatrix}+t^2\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad P_LQP_L=0,\quad \det S(t)=-t^4`. Valid when: Valid when K is two-dimensional and the falsifier tests fixed uncorrected paths rather than existential lifts.

## Attempted Derivation

- Diagonalize the face: write A_0=0_K\oplus D_R with D\ge\delta I_R; this is only a coordinate choice inside the same cone.
- For any PSD lift, the R-block is positive for small t, hence A(t)\succeq0 iff its Schur complement S(t)\succeq0.
- Expand A_{RR}(t)^{-1}; the only order-t^2 cross contribution to S(t) is -B_{KR}D^{-1}B_{RK}, giving Q=C_{KK}-B_{KR}D^{-1}B_{RK}.
- Necessity: divide <u,S(t)u> by t for u in K to get B_{KK}\succeq0; then divide by t^2 for u in L=ker B_{KK} to get P_LQP_L\succeq0.
- Sufficiency: decompose K=M\oplus L with B_{KK}|_M\ge\beta I_M. If P_LQP_L is only semidefinite, add an allowed t^3G correction on L, chosen positive on the kernel of P_LQP_L and large enough to dominate the finite Schur complement term from Q_{LM}.
- With that t^3 correction, S(t) is PSD for small t; restoring the R-block gives A_0+tB+t^2C+o(t^2)\succeq0, proving existential cone membership.
- The 2x2 boundary matrix shows why the same conditions do not imply positivity of the uncorrected fixed path.

Blocking gap: No internal gap remains for the finite existential theorem; the external gap is extracting the first actual H,K Wilson collar/hairpin finite block with a uniformly positive R-block.

## Falsifiers

- Finite falsifier: find D>0 and blocks satisfying B_{KK}\succeq0 and P_LQP_L\succeq0 but for which every o(t^2) lifting fails to be PSD.
- Uniform-gap falsifier: in a Wilson H,K extraction, the putative D^{-1} is unbounded or cutoff-dependent, so the Schur-Feshbach reduction is not valid.
- Same-theory falsifier: K, R, or the inner product changes with the perturbation parameter, so the cone theorem is being applied across different theories.
- Boundary falsifier: the fixed path tB+t^2Q is negative although the existential tangent condition holds; this refutes only the stronger fixed-remainder claim.

## Learning

The branch is no longer looping on non-Gaussian witness language. The valid contribution is a rigorous finite Schur-Feshbach tangent-cone theorem, and the boundary falsifier clarifies exactly why existential tangency is weaker than fixed-path positivity.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Build the smallest symbolic H,K collar/hairpin matrix, identify K,R,D, compute B_{KK}, B_{KR}, C_{KK}, and test PHP against the corrected Feshbach form P_LQP_L.

# Finite Schur-Feshbach tangent cone for Wilson collar/hairpin blocks

## Candidate Lemma

Let M(t)=H_0+tK+t^2L+E(t) be a finite Hermitian path with E(t)=o(t^2), H_0>=0, P=ker H_0, Q=1-P, and QH_0Q>=mu Q. Define A=PKP, C=PLP-PKQ(QH_0Q)^{-1}QKP, and R=ker_P A. If M(t)>=0 for all sufficiently small t>0, then A>=0 and RCR>=0. Conversely, if A>=0 and RCR>=eta R for some eta>0, then M(t)>=0 for all sufficiently small t>0. Thus off-diagonal hairpin coupling enters the valid second-order tangent cone through the negative Schur-Feshbach term.

## Definitions

- source object: finite Hermitian Wilson collar/hairpin truncation M(t)=H_0+tK+t^2L+o(t^2) with H_0 positive semidefinite.
- target object: finite positive-semidefinite cone condition for M(t) on the selected truncated excitation space.
- controlled interface: Schur-Feshbach elimination across P=ker H_0 and Q=1-P without changing entries or theories.
- same-theory condition: H_0,K,L come from one fixed cutoff, normalization, and observable extraction, not from mixed gauges or truncations.
- R is the orthogonal projection inside P onto ker(PKP).
- The strict converse is intentionally a robust sufficiency statement; the non-strict second-order boundary needs the next jet.

## Assumptions

- The Hilbert space is finite dimensional and all matrices are Hermitian.
- The expansion is one-sided for t>0 with operator-norm remainder o(t^2).
- QH_0Q has a positive lower spectral bound, so the Q block is invertible for small t.
- No claim is made here about OS density or the full Yang-Mills Hilbert space.

## Equations

- block expansion: `M(t)=\begin{pmatrix}tA+t^2A_2+o(t^2)&tB+o(t)\\ tB^*+o(t)&D_0+tD_1+o(t)\end{pmatrix}_{P\oplus Q}`. Valid when: Valid when H_0 is finite Hermitian positive semidefinite and QH_0Q has a strictly positive spectral floor.
- coefficient identification: `A=PKP,\quad A_2=PLP,\quad B=PKQ,\quad D_0=QH_0Q`. Valid when: Applies after fixing P=ker H_0 and reading the right Taylor coefficients in one finite basis.
- exact Schur-Feshbach test: `M(t)\ge0\iff QMQ>0\ \text{and}\ S(t):=PMP-PMQ(QMQ)^{-1}QMP\ge0`. Valid when: Valid when t is small enough that the Q block remains positive and invertible.
- corrected second-order form: `S(t)=t\,PKP+t^2\bigl(PLP-PKQ(QH_0Q)^{-1}QKP\bigr)+o(t^2)`. Valid when: Applies after a C^2 one-sided expansion where the off-diagonal block starts at order t.
- two-level tangent cone: `M(t)\ge0\Rightarrow PKP\ge0,\ RCR\ge0;\quad PKP\ge0,\ RCR\ge\eta R\Rightarrow M(t)\ge0\ (0<t<t_0)`. Valid when: Requires one-sided small positive t and strict positivity on the second-order kernel.

## Attempted Derivation

- Set D(t)=QM(t)Q. Since D(0)=QH_0Q>=mu Q and E(t)=o(t^2), D(t)>=mu Q/2 for small t.
- Use the finite congruence factorization of a block Hermitian matrix: positivity of M(t) is equivalent to positivity of D(t) and of S(t)=PMP-PMQD(t)^{-1}QMP.
- Expand D(t)^{-1}=D_0^{-1}+O(t). Since PMQ=tPKQ+O(t^2), the product PMQ D(t)^{-1} QMP contributes t^2 PKQ D_0^{-1} QKP+o(t^2).
- Thus S(t)=tA+t^2C+o(t^2) with A=PKP and C=PLP-PKQD_0^{-1}QKP.
- If A has a negative vector, S(t) and hence M(t) are negative for small t. If r in ker A has <r,Cr><0, then <r,S(t)r>=t^2<r,Cr>+o(t^2)<0.
- For sufficiency, split P=U⊕R with A positive on U and zero on R. The U block of S(t) is order t positive, the R block is order t^2 positive by RCR>=eta R, and the U-R cross correction after eliminating U is only order t^3. Hence S(t)>=0 for small t.

Blocking gap: The theorem does not yet compute an actual Wilson H_0,K,L collar/hairpin instance. If RCR has zero modes, the second-order jet is valid but inconclusive and a third-order Schur step is required.

## Falsifiers

- 2x2 falsifier: H_0=diag(0,1), K_{12}=k≠0, L=0 gives PKP=0 but det(H_0+tK)=-t^2|k|^2<0.
- Second-order boundary falsifier: M_+(t)=diag(t^3,1) and M_-(t)=diag(-t^3,1) share H_0,K,L through order two, so non-strict RCR=0 is not decisive.
- Same-theory falsifier: using QH_0Q from one truncation and PKQ from another can manufacture a false positive Schur correction.
- Extraction falsifier: if the Wilson collar basis is not orthonormalized, the inverse must be the Gram-corrected inverse, not the displayed Euclidean matrix inverse.

## Learning

The finite obstruction is now sharply identified: first-order positivity on the kernel is necessary but not stable under hairpin coupling. The valid second-order object is the Schur-Feshbach corrected form, and the 2x2 falsifier explains exactly why PHP/PKP alone cannot certify a Wilson truncation.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Build the smallest same-theory Wilson collar/hairpin truncation, orthonormalize its Gram matrix, compute P=ker H_0, then evaluate PKP and C=PLP-PKQ(QH_0Q)^{-1}QKP on R=ker(PKP).
