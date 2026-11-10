# cycle-0234

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Three-hairpin Wilson H,K Schur-Feshbach gate

## Candidate Lemma

For the normalized three-hairpin Wilson quotient with overlaps l12=4,l13=l23=1, PHP is PSD with null z=(1,1,-2). The corrected second-order gate is 8m^2+2R12-4R13-4R23>=0; failure is a concrete same-theory falsifier.

## Definitions

- source object: normalized collar quotient q_delta=hat N_delta oslash hat B_delta for three locked reflected Wilson hairpins with boundary overlaps 4,1,1.
- target object: finite OS positivity of the intended Wilson Schwinger block after collar collapse.
- controlled interface: extract H,K from the boundary OPE and apply the finite Schur-Feshbach tangent-cone test near J=11^*.
- same-theory condition: diagonal and one-body Wilson renormalizations are fixed before testing; only connected mixed boundary OPE data enter R.

## Assumptions

- q_delta is Hermitian, has diagonal 1, and admits a uniform expansion through o(delta^2).
- The leading boundary damping is Gaussian with coefficient m>=0 and overlap lengths l_ij.
- K_ij=(m^2/2)l_ij^2+R_ij off diagonal after same-theory normalization.
- R is the connected second boundary-OPE polarization for the reflected hairpin pair.

## Equations

- normalized hairpin expansion: `q_\delta=J+\delta H+\delta^2K+o(\delta^2),\quad H_{ij}=-m\ell_{ij},\quad K_{ij}=\tfrac12m^2\ell_{ij}^2+R_{ij}\ (i\ne j)`. Valid when: Valid when the reflected Wilson hairpins have a uniform small-collar boundary OPE and diagonal normalization has already removed one-body factors.
- first-order PHP test: `\ell=\begin{pmatrix}0&4&1\\4&0&1\\1&1&0\end{pmatrix},\quad x^*PHPx=2m|x_1-x_2|^2\quad(x_1+x_2+x_3=0),\quad \ker(PHP)=\mathbb C(1,1,-2)`. Valid when: Applies after choosing the first concrete hairpin block with overlaps four, one, one and testing only zero-sum vectors.
- corrected null-channel threshold: `z^*P\bigl(K-\tfrac13Hee^*H\bigr)Pz=8m^2+2R_{12}-4R_{13}-4R_{23},\quad z=(1,1,-2),\ e=3^{-1/2}(1,1,1)`. Valid when: Requires the same-theory boundary OPE expansion through second order and the first-order null direction left by PHP.

## Attempted Derivation

- Normalize the quotient matrix so q_delta has diagonal 1; pure one-body Wilson factors then vanish on 1^perp and cannot affect the test.
- Insert l12=4,l13=l23=1 into H=-m l. On x1+x2+x3=0, the quadratic form collapses to 2m|x1-x2|^2, so PHP is valid and has one null vector z.
- Eliminate the vacuum direction by the finite Schur complement. Since Hz=-2m(1,1,1), the rank-one correction subtracts 4m^2 from the raw second-order z-channel.
- The Gaussian square gives z^*(m^2 l^2/2)z=12m^2. Adding connected R and subtracting 4m^2 leaves the threshold 8m^2+2R12-4R13-4R23.

Blocking gap: R has only been symbolically parameterized; no cutoff-uniform Yang-Mills boundary OPE computation yet gives its sign or size.

## Falsifiers

- falsifier: a cutoff computation gives 2R12-4R13-4R23<-8m^2, making the corrected null-channel form negative while PHP remains valid.
- falsifier: diagonal normalization leaves pair-dependent one-body terms, so R is not connected same-theory boundary data.
- falsifier: the o(delta^2) remainder is not uniform on the null channel, invalidating promotion from the tangent gate to finite delta positivity.
- falsifier: cusp smoothing or orientation changes the overlap matrix, producing a negative first-order PHP direction instead of the stated null channel.

## Learning

The branch is not looping: the first concrete hairpin block passes PHP, and the corrected null-channel gate reduces the problem to one number, 8m^2+2R12-4R13-4R23. Leading Gaussian damping cannot falsify OS; only connected second boundary-OPE polarization can.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute R_ij from the reflected Wilson hairpin boundary OPE, starting with the connected two-gluon boundary contraction and checking whether length-linear second terms cancel after normalization.

# Finite Wilson collar/hairpin Schur-Feshbach test

## Candidate Lemma

In the first finite collar/hairpin Wilson Gram block with two null Wilson directions and one positive range direction, PHP reduces to μ>=0 and the corrected second-order obstruction is p+2q+r-(s+t)^2/δ>=0. Strict positivity of this corrected scalar gives a valid local fixed-path certificate; equality is only a tangent-cone boundary and needs higher-order control.

## Definitions

- source object: a three-observable reflected Wilson Gram block G_epsilon=(<Theta X_i X_j>_epsilon) for collar C, hairpin H, and one range mode R.
- target object: scalar PHP and corrected Schur-Feshbach inequalities certifying finite reflected-positivity to second order.
- controlled interface: reflection positivity of the finite Wilson block is translated into positivity of its Schur complement on the null Wilson sector K=span{C,H}.
- same-theory condition: all coefficients δ,μ,p,q,r,s,t are extracted from one cutoff/source family of Wilson observables before any continuum comparison.
- PHP convention: PHP denotes P_K B P_K, the projection of the first variation B onto the null Wilson sector, not the zeroth Gram H0.

## Assumptions

- G_epsilon=H0+epsilon B+epsilon^2 C+o(epsilon^2) as a symmetric finite matrix.
- H0 has kernel K=span{e_C,e_H} and positive range R=span{e_R} with D=δ>0.
- After diagonal normalization and collar/hairpin exchange reduction, P_K B P_K has Laplacian form μ[[1,-1],[-1,1]].
- B_KR=(s,t)^T and C_KK=[[p,q],[q,r]] in the ordered basis (C,H).
- The o(epsilon^2) remainder is uniform on this finite block.

## Equations

- normalized finite block: `G_\varepsilon=H_0+\varepsilon B+\varepsilon^2 C+o(\varepsilon^2),\quad H_0=\begin{pmatrix}0&0&0\\0&0&0\\0&0&\delta\end{pmatrix},\ \delta>0`. Valid when: Valid when the reflected Wilson observables are centered, finitely many, and differentiable in the same cutoff/source parameter.
- PHP collar-hairpin test: `P_KBP_K=\mu\begin{pmatrix}1&-1\\-1&1\end{pmatrix}\succeq0\quad\Longleftrightarrow\quad \mu\ge0`. Valid when: Applies after diagonal normalization and collar-hairpin exchange symmetry identify the first-order kernel block.
- corrected Schur complement: `S_K(\varepsilon)=\varepsilon B_{KK}+\varepsilon^2\bigl(C_{KK}-B_{KR}\delta^{-1}B_{RK}\bigr)+o(\varepsilon^2)`. Valid when: Requires the range entry δ to stay positive uniformly along the finite reflected Gram expansion.
- hairpin-collar common-mode obstruction: `(1,1)\bigl(C_{KK}-B_{KR}\delta^{-1}B_{RK}\bigr)\binom{1}{1}=p+2q+r-\frac{(s+t)^2}{\delta}\ge0`. Valid when: Valid when the PHP matrix has null vector (1,1) and the Feshbach range is one-dimensional.
- fully degenerate first-order variant: `\mu=0\quad\Rightarrow\quad \begin{pmatrix}p&q\\q&r\end{pmatrix}-\delta^{-1}\binom{s}{t}\begin{pmatrix}s&t\end{pmatrix}\succeq0`. Valid when: Applies when the first-order collar-hairpin block vanishes, so every kernel vector reaches second order.
- strict fixed-path sufficient regime: `\mu>0\ \text{ and }\ p+2q+r-(s+t)^2/\delta>0\quad\Longrightarrow\quad G_\varepsilon\succeq0\ \text{for }0<\varepsilon<\varepsilon_0`. Valid when: Valid when the expansion remainder is o(ε^2) uniformly on the finite three-dimensional block.

## Attempted Derivation

- Decompose the finite reflected Gram matrix by K=span{C,H} and R=span{R}; H0 is zero on K and δ>0 on R.
- Since the range block is D_epsilon=δ+O(epsilon), invert it and reduce positivity to the Schur complement S_K(epsilon).
- The off-diagonal K-R block starts as epsilon B_KR, so the first nontrivial range correction is exactly -epsilon^2 B_KR δ^{-1} B_RK.
- Insert the collar/hairpin Laplacian PHP block μ[[1,-1],[-1,1]]. The antisymmetric mode (1,-1) is controlled at first order iff μ>=0.
- The symmetric common mode (1,1) lies in ker(PHP), so the corrected second-order form gives Q_+=p+2q+r-(s+t)^2/δ.
- If μ=0 the entire K plane is in ker(PHP), hence the full 2x2 corrected matrix must be positive semidefinite.
- Strict μ>0 and Q_+>0 dominate the uniform o(epsilon^2) remainder; boundary equality is only a valid tangent statement, not a fixed-path proof.

Blocking gap: The coefficients δ,μ,p,q,r,s,t have not yet been computed from a named SU(N) collar/hairpin Wilson integral, so this is a concrete symbolic instance rather than a numerical or character-expanded Wilson case.

## Falsifiers

- falsifier: extracted μ<0, showing the projected first variation PHP is not positive.
- falsifier: μ>=0 but Q_+=p+2q+r-(s+t)^2/δ<0, so PHP passes while the corrected second-order form fails.
- falsifier: δ=0 or the chosen range mode is also null, invalidating the one-dimensional Feshbach reduction.
- falsifier: Q_+=0 with nonzero boundary cross terms and no third-order compensation, showing tangent validity but fixed-path failure.
- falsifier: coefficients are assembled from different cutoff limits or Wilson normalizations, violating the same-theory condition.

## Learning

The first H0,K collar/hairpin reduction is not another OS obstruction restatement: it yields a seven-coefficient finite test. PHP alone is too weak; the valid second-order scalar is Q_+=p+2q+r-(s+t)^2/δ. The key boundary falsifier is equality Q_+=0, where tangent membership can survive while a fixed Wilson path still loses positivity at higher order.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Choose a smallest SU(N) plaquette-action collar/hairpin triple, compute G_ij(epsilon) to second order by character or Weingarten integration, extract δ,μ,p,q,r,s,t, then test μ>=0 and Q_+>=0.

# Finite Schur-Feshbach Tangent Cone for Wilson Collar/Hairpin Positivity

## Candidate Lemma

Finite Schur-Feshbach tangent-cone theorem: let H_\varepsilon=H_0+\varepsilon K+\varepsilon^2L+o(\varepsilon^2) be self-adjoint on a finite Hilbert space, H_0\ge0, P=\ker H_0, Q=1-P, and B=QH_0Q\ge\gamma Q. Put A=PKP, E=PKQ, C=PLP, M=C-EB^{-1}E^*. If H_\varepsilon\ge0 for all sufficiently small \varepsilon>0, then A\ge0 and RMR\ge0 for R=\ker A inside P\mathcal H. Conversely, if A\ge0, A is strictly positive on (1-R)P\mathcal H, and RMR is strictly positive on R\mathcal H, then H_\varepsilon\ge0 for all sufficiently small \varepsilon. With non-strict RMR\ge0 this is the valid second-order tangent condition, not a full positivity certificate without higher-order data.

## Definitions

- source object: a finite Wilson collar/hairpin truncation represented by a self-adjoint matrix jet H_0+\varepsilon K+\varepsilon^2L on one fixed finite Hilbert space.
- target object: the local tangent cone to the positive semidefinite cone at H_0, including the second-order Schur-Feshbach correction on the zero-mode sector.
- controlled interface: replace naive PHP testing by the Feshbach complement after eliminating Q=(\ker H_0)^\perp with the same finite matrix entries.
- same-theory condition: H_0,K,L and all projections are extracted from the same truncation and inner product; no changed boundary OPE, measure, or observable algebra is allowed.

## Assumptions

- The Hilbert space is finite-dimensional over R or C, so all inverses and spectral projections are ordinary matrix objects.
- H_0\ge0 and QH_0Q=B\ge\gamma Q for some \gamma>0.
- K,L are self-adjoint and \|H_\varepsilon-H_0-\varepsilon K-\varepsilon^2L\|=o(\varepsilon^2).
- For the strict converse, RMR\ge mR with m>0 and A\ge a(1-R)P with a>0 on the positive first-order subspace.

## Equations

- PQ block jet: `H_\varepsilon=\begin{pmatrix}\varepsilon A+\varepsilon^2C+o(\varepsilon^2)&\varepsilon E+O(\varepsilon^2)\\ \varepsilon E^*+O(\varepsilon^2)&B+O(\varepsilon)\end{pmatrix}_{P\oplus Q}`. Valid when: Valid when the finite truncation has a norm second-order expansion and QH_0Q has a positive spectral gap.
- Feshbach complement expansion: `F_\varepsilon=PH_\varepsilon P-PH_\varepsilon Q(QH_\varepsilon Q)^{-1}QH_\varepsilon P=\varepsilon A+\varepsilon^2(C-EB^{-1}E^*)+o(\varepsilon^2)`. Valid when: Applies after diagonal normalization of the Q block and for sufficiently small positive epsilon.
- second-order tangent cone condition: `PKP\ge0,\qquad R\bigl(PLP-PKQ(QH_0Q)^{-1}QKP\bigr)R\ge0,\quad R=\mathbf 1_{\{0\}}(PKP)`. Valid when: Requires the same-theory finite matrix jet and tests only directions where the first-order form vanishes.
- corrected zero-mode quadratic form: `q_2(u)=\langle u,Lu\rangle-\langle QKPu,(QH_0Q)^{-1}QKPu\rangle\quad (u\in R\mathcal H)`. Valid when: Valid when u lies in the kernel of PKP and the hairpin sector Q has already been Feshbach eliminated.

## Attempted Derivation

- Decompose the finite Hilbert space as P\mathcal H\oplus Q\mathcal H with P=\ker H_0 and B=QH_0Q\ge\gamma Q.
- For small \varepsilon, QH_\varepsilon Q remains positive and invertible; positivity of H_\varepsilon is equivalent to positivity of the Schur complement F_\varepsilon.
- Use the Neumann expansion (QH_\varepsilon Q)^{-1}=B^{-1}+O(\varepsilon). The off-diagonal block \varepsilon E contributes the negative term -\varepsilon^2EB^{-1}E^*.
- Hence F_\varepsilon=\varepsilon A+\varepsilon^2M+o(\varepsilon^2), with M=C-EB^{-1}E^*.
- Necessity: F_\varepsilon\ge0 implies A\ge0 after division by \varepsilon. Testing u\in\ker A and dividing by \varepsilon^2 gives \langle u,Mu\rangle\ge0.
- Strict sufficiency: split P\mathcal H=R\mathcal H\oplus S\mathcal H, where R=\ker A. On S, \varepsilon A dominates. On R, \varepsilon^2RMR dominates. The R-S cross term is O(\varepsilon^2) and its Schur correction is only O(\varepsilon^3).
- Therefore strict A on S and strict RMR on R force F_\varepsilon\ge0, hence H_\varepsilon\ge0, for sufficiently small \varepsilon.

Blocking gap: The theorem proves the finite tangent-cone gate, but a non-strict RMR leaves a third-order kernel that must be checked recursively; the concrete Yang-Mills Wilson coefficients \alpha,\eta,\beta,\lambda have not yet been extracted.

## Falsifiers

- falsifier: H_0=diag(0,1), K=((0,1),(1,0)), L=0 passes PHP but has a negative eigenvalue -\varepsilon^2+O(\varepsilon^4).
- falsifier: any Wilson truncation with \alpha=0 and \lambda<|\eta|^2/\beta fails the corrected second-order test despite nonnegative first-order collar diagonal.
- falsifier: if QH_0Q has no positive lower bound, the inverse in the Schur correction is invalid and the finite theorem cannot be applied.
- falsifier: if H_0,K,L are assembled from different normalizations or boundary rules, the same-theory condition fails and the audit is not valid.

## Learning

The contribution-making object is the finite Schur-Feshbach tangent cone. Off-diagonal hairpin coupling is invisible to PHP but subtracts |hairpin coupling|^2/hairpin energy at order \varepsilon^2. A Wilson positivity audit is valid only after this correction and same-theory normalization.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Construct the smallest Gram-normalized Wilson collar/hairpin basis, compute H_0,K,L entries \alpha,\eta,\beta,\lambda, and test both PHP and the corrected Schur-Feshbach form.
