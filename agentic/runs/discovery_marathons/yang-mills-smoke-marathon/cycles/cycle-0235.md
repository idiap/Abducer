# cycle-0235

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: concrete three-hairpin H,K gate

## Candidate Lemma

For the first three reflected Wilson hairpin collar block with overlap lengths L12=4 and L13=L23=1, the diagonal-normalized quotient q_epsilon=J+epsilon H+epsilon^2 K+o(epsilon^2) passes the first-order PHP test and has exactly one null channel v=(1,1,-2). The valid corrected second-order gate is 8m^2+2R12-4R13-4R23>=0. Affine one-body and length-linear second boundary terms cancel; a quadratic connected footprint term R_ij=lambda L_ij^2 is a falsifier exactly when lambda<-m^2/3.

## Definitions

- source object: a locked regulated Wilson collar triple W_1(epsilon),W_2(epsilon),W_3(epsilon) whose reflected pair quotients q_ij(epsilon) are diagonal-normalized before cutoff removal.
- target object: a finite same-theory OS tangent-cone certificate or falsifier for the intended continuum Wilson Schwinger functions.
- controlled interface: the quotient matrix q_epsilon=N_epsilon oslash B_epsilon, expanded as J+epsilon H+epsilon^2 K+o(epsilon^2), after eliminating diagonal Wilson renormalizations.
- same-theory condition: H,K,R are extracted from the same Wilson loop observables and regulator family, with no boundary counterterm or post-hoc algebra enlargement.

## Assumptions

- m>0 is the leading reflected boundary damping coefficient.
- The hairpin footprint matrix is L=[[0,4,1],[4,0,1],[1,1,0]].
- The quotient has a uniform second-order OPE on this finite block.
- R is the connected second boundary-OPE coefficient after subtracting the square of the leading damping.
- The o(epsilon^2) remainder is uniform on unit vectors in the PHP-null tube.

## Equations

- three-hairpin expansion: `L=\begin{pmatrix}0&4&1\\4&0&1\\1&1&0\end{pmatrix},\quad H=-mL,\quad K=\tfrac12 m^2 L^{\circ 2}+R,\quad R_{ii}=0.`. Valid when: Valid when the three reflected Wilson hairpins have the stated collar footprint overlaps and the diagonal quotient normalization fixes q_ii(epsilon)=1.
- first-order PHP test: `P=I-\tfrac13{\bf 1}{\bf 1}^*,\quad x=(a,b,-a-b)\Rightarrow x^*PHPx=2m|a-b|^2,\quad \ker(PHP)=\mathbb C(1,1,-2).`. Valid when: Applies after diagonal normalization and projection away from the rank-one vacuum direction in the three-observable OS block.
- corrected null-channel gate: `e=3^{-1/2}{\bf 1},\quad C=P\bigl(K-\tfrac13 Hee^*H\bigr)P,\quad v=(1,1,-2),\quad v^*Cv=8m^2+2R_{12}-4R_{13}-4R_{23}.`. Valid when: Valid when the Schur complement of the vacuum eigenvalue is expanded to second order with uniform finite-block remainders.
- connected R extraction: `R_{ij}=\lim_{\epsilon\downarrow0}\epsilon^{-2}\bigl(\log q_{ij}(\epsilon)+m\epsilon L_{ij}\bigr),\quad \mathcal T(R)=2R_{12}-4R_{13}-4R_{23}.`. Valid when: Requires the same-theory boundary OPE to exist for reflected Wilson quotients before any positivity-preserving modification is introduced.
- affine cancellation and quadratic threshold: `\mathcal T(u_i+u_j+\alpha L_{ij})=0,\quad \mathcal T(\lambda L_{ij}^2)=24\lambda,\quad 8m^2+24\lambda\ge0\iff \lambda\ge-m^2/3.`. Valid when: Valid for this 4,1,1 hairpin geometry when R is decomposed into one-body, length-linear, and quadratic connected footprint components.

## Attempted Derivation

- Start from the diagonal-normalized three-hairpin quotient q_epsilon=J+epsilon H+epsilon^2 K+o(epsilon^2).
- Use the extracted footprint lengths L12=4, L13=L23=1 to set H=-mL and K=(1/2)m^2 L^{circ 2}+R.
- Project away from the vacuum direction with P=I-11^*/3. For x=(a,b,-a-b), compute x^*PHPx=2m|a-b|^2, so PHP is positive with null vector v=(1,1,-2).
- Take the Schur complement of the large eigenvalue of J=3ee^*. This gives the corrected second-order operator P(K-(1/3)Hee^*H)P, not PKP.
- Evaluate on v. The Gaussian square gives v^*(1/2 m^2L^{circ2})v=12m^2, while the vacuum Schur correction gives (1/3)|v^*He|^2=4m^2, leaving 8m^2 plus v^*Rv.
- Since Rii=0, v^*Rv=2R12-4R13-4R23. One-body terms u_i+u_j and length-linear terms alpha Lij cancel in this combination.
- For the symbolic connected model R_ij=lambda L_ij^2, the remaining scalar is 8m^2+24lambda, so the concrete threshold is lambda>=-m^2/3.

Blocking gap: The missing Yang-Mills input is the regulator-independent value or lower bound of the connected coefficient 2R12-4R13-4R23 for actual nonabelian Wilson hairpins.

## Falsifiers

- falsifier: a computed connected boundary coefficient with 2R12-4R13-4R23<-8m^2 makes the corrected finite OS quotient indefinite for small collars.
- If R_ij depends on the cutoff scheme after diagonal normalization, the same-theory condition is not valid.
- If the reflected Wilson OPE contains a nonuniform cusp remainder of order epsilon^2 in the null tube, the finite tangent test is inconclusive.
- If the actual footprint matrix differs from [[0,4,1],[4,0,1],[1,1,0]] because the hairpin collar geometry was misidentified, the concrete threshold must be recomputed.
- If diagonal normalization secretly inserts a boundary counterterm, positivity may be proved for a modified theory rather than Yang-Mills Wilson observables.

## Learning

Cycle 235 converts the first concrete hairpin block into a one-number boundary OPE problem. The PHP gate is positive with null vector (1,1,-2), and the corrected Schur-Feshbach second-order scalar is 8m^2+2R12-4R13-4R23. All one-body and length-linear second terms cancel, so the first possible falsifier is genuinely connected and nonlinear in the boundary footprint. In the symbolic model R_ij=lambda L_ij^2, the exact threshold is lambda=-m^2/3.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute R for the 4,1,1 reflected hairpin triple from the connected second cumulant of near-boundary plaquette-sheet insertions; first test whether the coefficient is affine in L, quadratic lambda L^2, or has a genuinely nonlocal connected polarization.

# First H,K collar/hairpin Schur-Feshbach coefficient test

## Candidate Lemma

In the first one-remainder collar/hairpin reduction, PHP on the K-block is not the valid second-order positivity test. If the plus hairpin vector u_+=η_L+η_R is first-order flat, the necessary Schur-Feshbach scalar is Q_+=p+2q+r-(s+t)^2/δ; Q_+<0 is a finite falsifier of same-theory positivity, while Q_+>0 gives a stable second-order tangent cone certificate.

## Definitions

- source object: a finite reflected Wilson Gram matrix M(ε) restricted to collar vectors η_L,η_R and one hairpin remainder ρ, expanded in the same cutoff and normalization.
- target object: the channelwise Schur-Feshbach tangent-cone inequality detecting whether the same Wilson family can remain positive through second order.
- controlled interface: identify K=span{η_L,η_R}, R=span{ρ}, keep the reflected observable basis fixed, and pass only through the finite Gram block before any OS reconstruction language.
- same-theory condition: all coefficients α,p,q,r,s,t,δ are extracted from the same Wilson action, boundary OPE convention, reflection normalization, and cutoff-removal path.

## Assumptions

- M(ε)=M_0+εB+ε^2C+O(ε^3) is a real symmetric reflected Gram block.
- M_0|_K=0, M_0|_R=δ>0, and M_0 has no K-R block.
- Reflection/collar symmetry puts B_KK=α[[1,-1],[-1,1]] with α≥0, so u_+=η_L+η_R lies in ker B_KK.
- C_KK=[[p,q],[q,r]] and B_RK=(s,t) in the ordered basis (η_L,η_R,ρ).
- The O(ε^3) remainder is uniform on this three-dimensional block.

## Equations

- three-by-three collar/hairpin expansion: `M(\varepsilon)=\begin{pmatrix}0&0&0\\0&0&0\\0&0&\delta\end{pmatrix}+\varepsilon\begin{pmatrix}\alpha&-\alpha&s\\-\alpha&\alpha&t\\s&t&u\end{pmatrix}+\varepsilon^2\begin{pmatrix}p&q&*\\q&r&*\\ *&*&*\end{pmatrix}+O(\varepsilon^3)`. Valid when: Valid when the reflected Wilson observables are restricted to the two collar generators and the first hairpin remainder with δ uniformly positive.
- PHP first-order test: `P_KBP_K=\alpha\begin{pmatrix}1&-1\\-1&1\end{pmatrix}\succeq0,\qquad P_KBP_Ku_+=0`. Valid when: Applies after diagonal normalization and reflection symmetry have reduced the K-block to the even and odd hairpin channels.
- corrected plus-channel scalar: `Q_+=u_+^TC_{KK}u_+-u_+^TB_{KR}D^{-1}B_{RK}u_+=p+2q+r-\frac{(s+t)^2}{\delta}`. Valid when: Requires the same-theory boundary OPE coefficients s,t and the positive remainder mass δ from the identical finite Gram block.
- optimized second-order quadratic form: `\inf_{z\in\mathbb R}\{\delta z^2+2z(s+t)+p+2q+r\}=Q_+`. Valid when: Valid when testing vectors have the Feshbach form u_++εzρ plus arbitrary K-corrections that do not alter second order.

## Attempted Derivation

- Choose the ordered basis (η_L,η_R,ρ) and impose the reflected collar symmetry B_KK=α[[1,-1],[-1,1]].
- The odd vector η_L-η_R has first-order weight 4α, so for α>0 only u_+=η_L+η_R remains tangent-flat.
- Test vectors x(ε)=u_++ε(y_K+zρ). Since B_KKu_+=0, the y_K term drops out of the ε^2 coefficient.
- The ε^2 coefficient is p+2q+r+2z(s+t)+δz^2.
- Minimizing over the remainder coordinate gives z_*=-(s+t)/δ and the corrected scalar Q_+=p+2q+r-(s+t)^2/δ.
- Therefore PHP alone misses negative leakage through ρ; the Schur-Feshbach correction is exactly the square of the combined hairpin coupling divided by δ.

Blocking gap: The symbolic coefficients p,q,r,s,t,δ have not yet been extracted from a concrete Wilson plaquette/collar ensemble with a fixed normalization; equality Q_+=0 also needs a third-order remainder bound.

## Falsifiers

- falsifier: α<0, since the PHP first-order block is already indefinite.
- falsifier: α≥0 and Q_+<0, since the optimized vector u_++εz_*ρ makes the reflected Gram block negative at order ε^2.
- falsifier: δ tends to 0 under cutoff removal, because the one-remainder Schur complement is then not a valid finite reduction.
- falsifier: the extracted s,t,p,q,r come from different Wilson normalizations, which violates the same-theory condition.
- Boundary falsifier: Q_+=0 may allow tangent membership but cannot certify a fixed positive Wilson path without third-order control.

## Learning

The branch is not looping on Wilson/OS obstruction language. The first H,K collar/hairpin case has a concrete seven-coefficient test: PHP checks α≥0, but valid second-order positivity in the flat plus channel is governed by Q_+=p+2q+r-(s+t)^2/δ. The Feshbach leakage term is the exact correction and supplies an immediate falsifier when negative.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Build the explicit three-observable reflected Wilson Gram block (η_L,η_R,ρ), expand its entries to second order in the chosen strong/weak collar parameter, and compute α,p,q,r,s,t,δ to test PHP and Q_+.

# Finite Schur-Feshbach tangent cone replacing PHP Wilson audit

## Candidate Lemma

Let H,K,L be finite Hermitian n by n matrices with H>=0, P=ker H, Q=1-P, and QHQ>=gamma Q on ran Q. Put A=PKP, E=PLP-PKQ(QHQ)^{-1}QKP, and let R be the projection in P onto ker A. Then (K,L) lies in the second-order tangent cone to the finite PSD cone at H iff A>=0 and RER>=0. For a fixed path H+tK+t^2L+o(t^2), these conditions are necessary; they are sufficient when RER is strictly positive on R, or for tangent-cone membership after an allowed o(t^2) repair.

## Definitions

- source object: a finite same-theory Wilson/OS Gram path G(t)=H+tK+t^2L+o(t^2) extracted from one truncated observable family.
- target object: the parabolic second-order tangent cone to the finite positive semidefinite cone at the unperturbed Gram matrix H.
- controlled interface: Schur-Feshbach elimination of the positive Q-block, converting full Gram positivity into positivity of the effective P-block.
- same-theory condition: H,K,L,P,Q are computed in one normalization of the same finite observable system; no independent counterterm may be inserted to cancel the hairpin term.
- P is the orthogonal projection onto ker H and Q=1-P.
- The inverse (QHQ)^{-1} is the bounded inverse on ran Q only.
- The tangent cone uses corrections r(t)=o(t^2) in finite operator norm.

## Assumptions

- Finite-dimensional Hermitian matrices; no domain or closability issue is hidden.
- H is positive semidefinite and the nonzero spectral block QHQ has gap gamma>0.
- Perturbations are one-sided with t down to 0, matching a small Wilson deformation parameter.
- The PSD cone is tested by ordinary quadratic forms on all finite vectors.

## Equations

- finite Gram path: `G(t)=H+tK+t^2L+o(t^2),\qquad H\ge 0,\quad QHQ\ge \gamma Q.`. Valid when: Valid when the Wilson truncation is finite dimensional and the positive block of H has a spectral gap.
- Schur equivalence: `G(t)\ge 0\iff QG(t)Q>0\ \text{and}\ S(t):=PG(t)P-PG(t)Q\,(QG(t)Q)^{-1}QG(t)P\ge 0.`. Valid when: Valid when t is small enough that the Q-block remains strictly positive after perturbation.
- corrected second-order effective form: `S(t)=tA+t^2E+o(t^2),\quad A=PKP,\quad E=PLP-PKQ(QHQ)^{-1}QKP.`. Valid when: Applies after Schur-Feshbach elimination with all inverses restricted to the Q range.
- parabolic tangent criterion: `(K,L)\in T^2_{\mathcal S^n_+}(H)\iff A\ge 0\ \text{on }P\ \text{and}\ RER\ge 0\ \text{on }R=\ker_P A.`. Valid when: Requires the parabolic tangent definition allowing only corrections smaller than t squared.
- strict fixed-path certificate: `A\ge 0,\quad RER\ge \mu R\ (\mu>0)\quad\Longrightarrow\quad H+tK+t^2L+o(t^2)\ge 0\ \text{for all small }t>0.`. Valid when: Valid when the corrected kernel form has a strictly positive lower bound.

## Attempted Derivation

- Decompose the finite Hilbert space as P\oplus Q with P=ker H and Q=1-P; then PHP=0 and PHQ=0 because H>=0.
- Since QHQ>=gamma Q, the perturbed block QG(t)Q remains positive and invertible for sufficiently small t by the Neumann expansion.
- Apply the finite Schur complement: full PSD of G(t) is equivalent to positivity of QG(t)Q and of the effective block S(t).
- Expand (QG(t)Q)^{-1}=(QHQ)^{-1}+O(t). The cross term PG(t)Q begins as tPKQ, producing the order t^2 subtraction PKQ(QHQ)^{-1}QKP.
- Thus S(t)=tA+t^2E+o(t^2). If A has a negative vector, S(t) is negative at order t; hence A>=0 is necessary.
- Let R project to ker A. Testing vectors x in ran R gives x*S(t)x=t^2 x*Ex+o(t^2), so RER>=0 is necessary for any PSD path.
- For sufficiency in the tangent-cone sense, split P=(ker A)^perp\oplus ker A. The positive part of A controls the first block at order t; RER controls the null block at order t^2; a large positive c t^3 I repair absorbs cross terms without violating o(t^2).
- For an actual fixed path, the same block estimate gives sufficiency when RER has a strict positive margin on ker A; without strictness, higher-order data are needed.

Blocking gap: The finite theorem is now essentially proved, but the branch has not yet extracted a real same-theory Wilson collar/hairpin Gram matrix H,K,L from the Yang-Mills observable construction.

## Falsifiers

- falsifier: H=diag(0,1), K=((0,1),(1,0)), L=0 has PHP=0 but lambda_min=-t^2+O(t^3), so PHP-only positivity is false.
- falsifier: if QHQ has a zero mode, the Schur inverse is invalid and the theorem must be applied after enlarging P.
- falsifier: if H,K,L come from different normalizations or different theories, the hairpin subtraction may be an artifact rather than a valid same-theory correction.
- falsifier: RER>=0 with a non-strict kernel does not certify an arbitrary fixed o(t^2) path; negative higher-order terms can still break positivity.

## Learning

The finite obstruction has been sharpened into a real theorem: positivity near a degenerate Gram matrix is governed by the Schur-Feshbach tangent cone. PHP is only the first test. The hairpin coupling subtracts PKQ(QHQ)^{-1}QKP at order t^2, and the 2x2 falsifier shows why ignoring it is invalid.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Extract the smallest Wilson observable pair producing one collar state and one hairpin state, normalize H so QHQ=h>0, compute a,b,ell, and test ell-|b|^2/h rather than PHP alone.
