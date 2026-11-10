# cycle-0232

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology -> first Wilson hairpin H,K block

## Candidate Lemma

For three reflected Wilson collar hairpins with one boundary shape mode and parameters x=(-a,a,0), the diagonally normalized Schur-preimage quotient has an explicit tangent expansion. Its first-order gate PHP is positive semidefinite with one null vector v=(1,1,-2), and the corrected second-order Schur-Feshbach test is the scalar 8m^2+2R_{12}-4R_{13}-4R_{23}. Thus the first concrete falsifier is a connected second boundary-OPE coefficient below this threshold.

## Definitions

- source object: a fixed-collar regulated Yang-Mills OS matrix G_{ij}(\delta,\varepsilon)=\langle W(\Theta C_i^{\delta,\varepsilon})W(C_j^{\delta,\varepsilon})\rangle for three smooth reflected Wilson hairpins with common footprint and boundary shape parameters (-a,a,0).
- target object: the diagonally normalized continuum Schur-preimage quotient q_\varepsilon=\widehat N_\varepsilon\oslash\widehat B_\varepsilon whose positivity is the same-theory OS test after collar collapse.
- controlled interface: take \delta\downarrow0 first with locked Wilson renormalization, extract uniform boundary OPE coefficients, then test q_\varepsilon=11^*+\varepsilon H+\varepsilon^2K+o(\varepsilon^2) by the finite Schur-Feshbach gate.
- same-theory condition: the diagonal Wilson factors and boundary Gram factor B are those already present in the locked continuum Wilson algebra; no extra reflection-plane counterterm or changed loop observable is allowed.

## Assumptions

- The hairpin family has a smooth common reflection-plane footprint and a single real boundary shape mode \psi, so the three germs differ only by x_i\psi with x=(-a,a,0).
- The normalized collar-collapse boundary OPE is uniform enough to give q_{ij}(\varepsilon)=1-\varepsilon\mu(x_i-x_j)^2+\varepsilon^2[\frac12\mu^2(x_i-x_j)^4+R_{ij}]+o(\varepsilon^2).
- The leading boundary exchange coefficient \mu is positive; perturbatively it is the positive boundary-current norm of \psi times the color factor of the locked Wilson representation.
- R_{ij}=R_{ji}, R_{ii}=0, and R records only connected second-order mixed boundary data after diagonal one-body Wilson factors have been removed.
- The finite Schur-Feshbach tangent-cone theorem from cycle 231 is valid with e=3^{-1/2}(1,1,1) and P=I-ee^*.

## Equations

- normalized three-hairpin quotient expansion: `q_{ij}(\varepsilon)=1-\varepsilon\mu(x_i-x_j)^2+\varepsilon^2\left[\frac12\mu^2(x_i-x_j)^4+R_{ij}\right]+o(\varepsilon^2),\quad x=(-a,a,0)`. Valid when: Valid when the reflected Wilson observables admit a uniform collar boundary OPE after fixed diagonal Wilson normalization.
- first-order H matrix: `m=\mu a^2,\qquad H=-m\begin{pmatrix}0&4&1\\4&0&1\\1&1&0\end{pmatrix}`. Valid when: Applies after diagonal normalization leaves only the leading connected boundary current norm for the three collinear hairpin modes.
- second-order K matrix: `K=m^2\begin{pmatrix}0&8&\tfrac12\\8&0&\tfrac12\\\tfrac12&\tfrac12&0\end{pmatrix}+R,\qquad R_{ii}=0`. Valid when: Requires the same-theory boundary OPE through second order with R collecting connected two-boundary-cumulant and cusp remainder terms.
- first Schur-Feshbach gate: `P=I-ee^*,\quad e=3^{-1/2}(1,1,1),\quad PHP\succeq0,\quad \ker(PHP)=\operatorname{span}\{(1,1,-2)\}`. Valid when: Valid when m is positive and P projects onto the zero-sum Wilson coefficient subspace.
- corrected second-order null test: `v=(1,1,-2),\qquad v^*\left(K-\frac13Hee^*H\right)v=8m^2+2R_{12}-4R_{13}-4R_{23}`. Valid when: Applies when the first-order zero-sum vector lies in the nullspace, so the vacuum Schur complement supplies the rank-one correction.

## Attempted Derivation

- Choose three collar hairpins C_i^{\delta,\varepsilon} with common footprint and boundary shape displacements x_i\psi, x=(-a,a,0).
- After taking \delta\downarrow0 in the locked Wilson algebra, diagonal normalization forces q_{ii}=1 and removes all one-body boundary Wilson factors.
- Use the leading boundary-current OPE to parameterize the mixed damping by \mu(x_i-x_j)^2; this gives H_{ij}=-\mu(x_i-x_j)^2 and hence the displayed H matrix with m=\mu a^2.
- Keep the second-order expansion as the sum of the exponential square \frac12\mu^2(x_i-x_j)^4 and an unknown connected same-theory coefficient R_{ij}; this gives the displayed K matrix.
- On 1^\perp use u=(1,-1,0) and v=(1,1,-2). Direct multiplication gives u^*Hu=8m, u^*Hv=0, and v^*Hv=0, so PHP is positive semidefinite with null direction v.
- Apply the corrected Schur-Feshbach form from the vacuum direction: C=P(K-3^{-1}Hee^*H)P. The pure square term gives v^*Kv=12m^2 and the vacuum correction gives 4m^2, leaving 8m^2 plus the R polarization.

Blocking gap: The scalar R_{12},R_{13},R_{23} has not yet been computed from the actual four-dimensional SU(N) Wilson boundary OPE with uniform collar remainders.

## Falsifiers

- A direct Wilson OPE calculation giving 8m^2+2R_{12}-4R_{13}-4R_{23}<0 is a valid finite same-theory falsifier.
- If the leading mixed hairpin coefficient is not a conditionally negative boundary-current square, then PHP can already fail at first order.
- If collar collapse requires an added reflection-plane counterterm, the calculation may remain positive but no longer tests the same theory.
- If the o(\varepsilon^2) remainder is not uniform as \delta\downarrow0, the extracted H,K data need not control the continuum OS matrix.

## Learning

The branch is no longer looping on the Wilson/OS obstruction ladder. The first concrete three-hairpin block has H=-m[[0,4,1],[4,0,1],[1,1,0]], so PHP passes with one null direction. The corrected second-order form is not PKP; it leaves the explicit threshold 8m^2+2R_{12}-4R_{13}-4R_{23}. Pure leading Gaussian boundary damping is safe; only a sufficiently negative connected second boundary-OPE polarization can falsify same-theory OS positivity in this block.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute R for the same three hairpins in the first perturbative Wilson expansion: isolate two-gluon connected exchange and cusp-counterterm contributions, verify diagonal cancellation, then insert R_{12}, R_{13}, R_{23} into the corrected scalar test.

# Finite Schur-Feshbach tangent-cone theorem instead of looping non-Gaussian witnesses

## Candidate Lemma

Let V=K⊕R be finite-dimensional and A0=0_K⊕D with D positive definite on R. For Hermitian B,C, B is a valid first tangent to the PSD cone at A0 iff B_KK is positive semidefinite. If G=B_KK and L=ker G, then C is a valid parabolic second tangent in direction B iff P_L(C_KK-B_KR D^{-1}B_RK)P_L is positive semidefinite. The negative Schur-Feshbach term is mandatory.

## Definitions

- source object: finite-dimensional Hermitian positive-semidefinite cone at A_0=0_K\oplus D_R with D_R\succ0 and fixed block decomposition V=K\oplus R.
- target object: exact parabolic second-order tangent cone T^2_{\mathcal P}(A_0;B) expressed only on the kernel of B_{KK}.
- controlled interface: Schur-Feshbach reduction across the uniformly positive R block, retaining the order-t^2 effective K block.
- same-theory condition: the spaces K,R, projection P_L, matrix D, and Hermitian perturbations B,C are fixed throughout; no cutoff, observable, or inner product is changed.
- Parabolic second tangent means: C is allowed when A_0+tB+t^2(C+E_t) is PSD for some E_t→0 as t↓0.
- Blocks are taken with respect to V=K⊕R, and P_L is the orthogonal projection onto L=ker B_KK.

## Assumptions

- V is finite-dimensional over C and all matrices are Hermitian.
- D is strictly positive on R, so A_RR(t) remains invertible for small positive t.
- Tangency is one-sided as t↓0.
- The second-order coefficient convention is A(t)=A0+tB+t^2C+o(t^2), with no factor 1/2.

## Equations

- base block expansion: `A(t)=A_0+tB+t^2C+o(t^2),\qquad A_0=\begin{pmatrix}0&0\\0&D\end{pmatrix},\ D\succ0`. Valid when: Valid when the Hermitian path is right twice differentiable at t=0 in a fixed finite-dimensional Hilbert space.
- first tangent cone: `B\in T_{\mathcal P}(A_0)\Longleftrightarrow B_{KK}\succeq0`. Valid when: Valid when tangency is taken to the positive semidefinite cone at a matrix whose kernel is K.
- Schur-Feshbach effective block: `S(t)=A_{KK}(t)-A_{KR}(t)A_{RR}(t)^{-1}A_{RK}(t)=tG+t^2F+o(t^2)`. Valid when: Applies after the R block remains uniformly positive, so its inverse has a convergent small-t expansion.
- corrected second-order form: `G=B_{KK},\qquad F=C_{KK}-B_{KR}D^{-1}B_{RK}`. Valid when: Valid when the same K,R decomposition and the same positive operator D are used in every block.
- variational origin of Feshbach term: `\inf_{r\in R}\{\langle Dr,r\rangle+2\operatorname{Re}\langle B_{RK}k,r\rangle+\langle C_{KK}k,k\rangle\}=\langle Fk,k\rangle`. Valid when: Requires k to lie in L=ker B_{KK}, where the first-order K contribution vanishes exactly.
- parabolic tangent criterion: `C\in T^2_{\mathcal P}(A_0;B)\Longleftrightarrow P_LFP_L\succeq0`. Valid when: Valid when T^2 is the parabolic existential second tangent cone allowing o(t^2) positive lifts.

## Attempted Derivation

- Block decompose A(t) relative to V=K⊕R. Since D≻0, A_RR(t) is positive and invertible for all sufficiently small t>0.
- Necessity of B_KK⪰0 follows from testing PSD on vectors k∈K: <A(t)k,k>=t<B_KKk,k>+O(t^2).
- For k∈L=ker B_KK and r∈R, test x(t)=k+tr. Positivity gives 0≤t^2[<Dr,r>+2Re<B_RKk,r>+<C_KKk,k>]+o(t^2).
- Minimizing over r gives r=-D^{-1}B_RKk and the necessary inequality <(C_KK-B_KR D^{-1}B_RK)k,k>≥0.
- For sufficiency, add the harmless lift Q(t)=A0+tB+t^2C+t^{5/2}I. It has the same first and second coefficients.
- The Schur complement of Q(t) equals tG+t^2F+t^{5/2}I_K+O(t^3).
- Decompose K=ran(G)⊕L. On ran(G), tG dominates t^2F and O(t^3). On L, P_LFP_L⪰0 and t^{5/2}I dominates all boundary cross errors of order t^3.
- Thus the Schur complement is PSD for small t, hence Q(t) is PSD. This proves the existential parabolic tangent equivalence.

Blocking gap: No internal finite-dimensional gap remains; the remaining blocking gap is uniform extraction of the H,K Wilson collar/hairpin matrices A0,B,C,D from the same cutoff theory.

## Falsifiers

- falsifier: K=R=C, D=1, B_KK=C_KK=0, B_KR=1 makes the omitted-Feshbach criterion false because det[[0,t],[t,1]]=-t^2.
- falsifier: A(t)=diag(-t^3,1) shows that valid existential second tangency is weaker than positivity for an arbitrary fixed o(t^2) remainder.
- falsifier: if D loses a uniform lower spectral bound, the Schur inverse expansion is invalid and the theorem no longer applies.
- falsifier: if the K,R decomposition or inner product changes with t, the condition is not same-theory and P_LFP_L is not invariant.

## Learning

The branch stopped looping on Wilson/OS obstruction language. The valid contribution is the finite Schur-Feshbach parabolic cone theorem: first order only sees B_KK, while second order on ker B_KK sees exactly C_KK-B_KR D^{-1}B_RK. Boundary behavior explains why fixed-remainder positivity is stronger than existential tangent membership.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Instantiate the theorem on the first concrete Wilson collar/hairpin H,K finite Gram matrix: compute A0,B,C,D, L=ker B_KK, test PHP, and evaluate P_L(C_KK-B_KR D^{-1}B_RK)P_L.

# Finite Schur-Feshbach tangent cone for Wilson collar/hairpin truncations

## Candidate Lemma

Let V be finite-dimensional, P an orthogonal projection, Q=I-P, H=QHQ with QHQ=D>=gamma Q for gamma>0, and A(t)=H+tK+t^2L+r(t), ||r(t)||=o(t^2), self-adjoint. Put B=PKP, R=PLP-PKQD^{-1}QKP, and let N be the projection in PV onto ker B. If A(t)>=0 for all sufficiently small t>0, then B>=0 and NRN>=0. Conversely, if B>=0 and NRN is positive definite, then A(t)>=0 for all sufficiently small t>0. With NRN merely semidefinite, the same condition is the closed second-order tangent-cone condition, not a uniform stability claim for arbitrary o(t^2) remainders.

## Definitions

- source object: a finite-dimensional self-adjoint pencil A(t)=H+tK+t^2L+o(t^2) on V=PV⊕QV, with PH=HP=0 and QHQ strictly positive.
- target object: the second-order tangent cone to the positive-semidefinite cone at H along K, including the hairpin correction seen by the P-sector.
- controlled interface: Schur-Feshbach elimination of the massive Q block converts positivity of A(t) into positivity of an effective P-block S(t).
- same-theory condition: P,Q,H,K,L come from one finite Wilson collar/hairpin truncation; Q is eliminated algebraically without changing couplings, states, or observables.

## Assumptions

- V is finite-dimensional, so all inverses and spectral projections used below are ordinary matrix operations.
- QHQ=D>=gamma Q with gamma>0; this is the finite massive block needed for Feshbach elimination.
- K,L are self-adjoint and the perturbation remainder satisfies ||r(t)||=o(t^2).
- The positivity test is one-sided for t>0, matching a coupling or collar-thickness expansion.

## Equations

- Schur complement positivity equivalence: `A(t)\ge 0\iff D(t):=QA(t)Q>0\ \text{and}\ S(t):=PA(t)P-PA(t)Q\,D(t)^{-1}\,QA(t)P\ge 0`. Valid when: Valid when the Q block remains strictly positive for small positive t by the gap D>=gamma Q and the finite-dimensional Schur complement theorem applies.
- effective P-block expansion: `S(t)=tB+t^2R+o(t^2),\quad B=PKP,\quad R=PLP-PKQD^{-1}QKP`. Valid when: Applies after expanding D(t)^{-1}=D^{-1}+O(t) and retaining all order t^2 terms from the off-diagonal hairpin coupling.
- closed tangent cone condition: `B\ge 0,\qquad N\bigl(PLP-PKQD^{-1}QKP\bigr)N\ge 0,\quad N=1_{\{0\}}(B)\ \text{on }PV`. Valid when: Requires the same-theory finite pencil and describes the closed second-order tangent cone rather than guaranteed positivity under arbitrary higher-order remainders.
- strict stability version: `B\ge 0\ \text{and}\ N R N\ge \eta N\ (\eta>0)\quad\Longrightarrow\quad A(t)\ge 0\ \text{for }0<t<t_0`. Valid when: Valid when the null-sector second-order correction has a positive spectral margin that dominates the o(t^2) remainder for sufficiently small t.

## Attempted Derivation

- Split V=PV⊕QV and write A(t) in 2x2 blocks.
- Since QHQ=D>=gamma Q and QA(t)Q=D+O(t), the Q block is positive and invertible for small t.
- Apply the finite Schur complement theorem: A(t)>=0 iff QA(t)Q>0 and S(t)>=0.
- Use (D+tQKQ+O(t^2))^{-1}=D^{-1}+O(t) to expand S(t).
- The term PA(t)Q D(t)^{-1} QA(t)P contributes t^2 PKQD^{-1}QKP+O(t^3), producing the negative correction in R.
- For S(t)=tB+t^2R+o(t^2), positivity forces B>=0 by testing fixed P-vectors.
- Testing vectors in ker B gives NRN>=0 as the necessary second-order condition.
- Conversely, decompose PV=ran(B)⊕ker(B). On ran(B), tB dominates t^2R and o(t^2); on ker(B), a strict positive lower bound for NRN dominates the remainder; cross terms are absorbed by completing the square.
- The 2x2 model with H=diag(0,1), K off-diagonal, L=0 gives lambda_min=-t^2+O(t^4), proving PHP-only positivity is invalid.

Blocking gap: The semidefinite case NRN>=0 is only a closed tangent-cone statement unless third-order data are controlled on ker B∩ker(NRN). A concrete Wilson collar/hairpin extraction must either show a positive margin or compute the next term.

## Falsifiers

- falsifier: QHQ has a zero mode; then D^{-1} is not available and the Schur-Feshbach correction is not valid.
- falsifier: PKP has a negative vector; then A(t) is already negative at first order.
- falsifier: B>=0 but some n in ker B has <n,Rn><0; then A(t) has a negative eigenvalue at order t^2.
- falsifier: NRN=0 on a nonzero vector and the O(t^3) coefficient is negative; the closed tangent condition holds but actual positivity fails.
- falsifier: the finite H,K,L are assembled from different regularizations or observables; the same-theory condition is broken.

## Learning

The contribution-making move is valid: finite positivity is governed by a Schur-Feshbach tangent cone, not by PHP alone. The off-diagonal hairpin coupling subtracts PKQ(QHQ)^{-1}QKP, and the 2x2 falsifier shows the obstruction at order t^2. The branch should stop looping on OS density and use this theorem to audit concrete Wilson truncations.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Build the smallest Wilson collar/hairpin basis, compute its finite H,K,L entries symbolically, diagonalize B=PKP, and evaluate NRN=N(PLP-PKQ(QHQ)^{-1}QKP)N with the 2x2 falsifier as the sanity check.
