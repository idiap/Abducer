# cycle-0184

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: finite OS-matrix boundary defects

## Candidate Lemma

Finite Wilson OS-matrix defect criterion. Let \(F_1,\ldots,F_n\) be locked gauge-invariant positive-time Wilson/composite observables and let \(T_\delta F_i\) be collar-separated approximants. Suppose the collar OS matrices \(N^{(\delta)}_{ij}=S(\Theta T_\delta F_i,T_\delta F_j)\) have a positive limit \(N\), and suppose the boundary trace relation has the finite-matrix form \(N=\Gamma\circ M+B\), where \(M_{ij}=S(\Theta F_i,F_j)\) is the intended continuum OS matrix, \(\Gamma\) is a multiplicative boundary anomaly, and \(B\) is an additive contact matrix. If \(\Gamma_{ij}=\overline{d_i}d_j\) with all \(d_i\ne0\), and if \(B\ge0\) with \(B_{ii}=0\) for every locked observable, then \(M\ge0\). Thus OS positivity is valid for the intended target theory under rank-one multiplicative renormalization plus diagonal-killed positive additive contact.

## Definitions

- source object: a directed family of regulated reflection-positive Schwinger functionals \(S_{a,L}\) on a fixed gauge-invariant observable algebra, with collar approximants \(T_\delta F\) supported in \(t>\delta\).
- target object: the continuum Schwinger functional \(S\) restricted to the same positive-time gauge-invariant algebra, encoded by finite OS matrices \(M_{ij}=S(\Theta F_i,F_j)\) whose positivity reconstructs the OS Hilbert space.
- controlled interface: the two-step passage \(S_{a,L}\to S\) for fixed collars, followed by \(\delta\downarrow0\) in finite reflected quadratic forms, with possible boundary trace factors recorded as \(N=\Gamma\circ M+B\).
- same-theory condition: the observables \(F_i\) and their collar approximants \(T_\delta F_i\) use the same locked Wilson-loop/composite renormalization; allowed multiplicative factors must be pre-existing diagonal congruences, and no additive boundary field may be added to redefine the target algebra.

## Assumptions

- Regulated reflection positivity holds: for every cutoff pair \((a,L)\), every finite positive-time family \(G_i\), and coefficients \(c_i\), \(\sum_{i,j}\overline c_i c_j S_{a,L}(\Theta G_i,G_j)\ge0\).
- The RG cutoff-removal topology is strong enough to pass every fixed-collar reflected matrix entry to the continuum, so \(N^{(\delta)}\ge0\) and \(N^{(\delta)}\to N\) imply \(N\ge0\).
- For the chosen finite locked Wilson/composite family, the collar trace limit exists and decomposes as \(N=\Gamma\circ M+B\).
- The multiplicative anomaly is a diagonal congruence, \(amma_{ij}=\overline{d_i}d_j\), already included in the fixed normalization of the same observables.
- The additive boundary contact sector is reflection-positive as a finite matrix \(B\ge0\), and individual trace continuity gives \(B_{ii}=0\) for every test observable in the family.

## Equations

- finite OS matrices: `M_{ij}=S(\Theta F_i,F_j),\qquad N_{ij}=\lim_{\delta\downarrow0}S(\Theta T_\delta F_i,T_\delta F_j)`. Valid when: The continuum Schwinger functional is defined on the locked observable algebra and the collar limit exists for the finite reflected family.
- defect decomposition: `N=\Gamma\circ M+B`. Valid when: The boundary value analysis separates multiplicative Wilson renormalization from additive reflection-plane contact terms for the selected finite OS matrix.
- rank-one congruence reduction: `\Gamma_{ij}=\overline{d_i}d_j\quad\Longrightarrow\quad \Gamma\circ M=D^*MD,\qquad D=\operatorname{diag}(d_1,\ldots,d_n)`. Valid when: The multiplicative anomaly factors through individual observable normalizations rather than through pair-dependent cusp or hairpin data.
- positive contact killed by diagonal: `B\ge0,\\ B_{ii}=0\ \forall i\quad\Longrightarrow\quad |B_{ij}|^2\le B_{ii}B_{jj}=0\quad\Longrightarrow\quad B=0`. Valid when: The additive boundary contact is itself a positive Gram contribution and individual collar trace continuity has already removed all diagonal contact terms.
- positivity transfer: `N\ge0,
\quad B=0,
\quad N=D^*MD
\quad\Longrightarrow\quad
M=(D^*)^{-1}ND^{-1}\ge0`. Valid when: All diagonal factors \(d_i\) are nonzero, so the congruence is invertible on the locked finite test space.

## Attempted Derivation

- Start with fixed collar observables \(T_\delta F_i\). Regulated reflection positivity and RG convergence in the OS topology give \(N^{(\delta)}\ge0\) and hence a positive collar-limit matrix \(N\ge0\). This part is valid by the closed-cone argument already isolated in earlier cycles.
- Write the most general finite Wilson trace relation being tested as \(N=\Gamma\circ M+B\), separating pairwise multiplicative boundary factors from additive reflection-plane contacts. The target OS positivity problem is to infer \(M\ge0\) from \(N\ge0\) without changing the theory.
- If \(\Gamma\) is rank-one, \(\Gamma_{ij}=\overline{d_i}d_j\), then \(\Gamma\circ M=D^*MD\). This is an invertible congruence and preserves/refects positivity once \(D\) is fixed by the locked observable normalization.
- For the additive term, assume it is a positive boundary Gram matrix and that diagonal trace continuity has already removed individual defects. Then \(B\ge0\) and \(B_{ii}=0\) imply \(B_{ij}=0\) for every \(i,j\) by Cauchy-Schwarz. Hence \(B=0\), not merely harmless.
- With \(B=0\), positivity transfers by \(M=(D^*)^{-1}ND^{-1}\ge0\). This completes the finite-matrix bridge under the stated assumptions.
- To test necessity, examine a normalized two-observable multiplicative anomaly \(\Gamma=\begin{pmatrix}1&\beta\\\overline\beta&1\end{pmatrix}\). If \(0<|\beta|<1\), then \(\Gamma\ge0\), but \(\Gamma^{[-1]}\) is not positive; entrywise recovery of \(M\) can destroy OS positivity. Thus nonfactorizing mixed damping is a real falsifier.

Blocking gap: The remaining Yang-Mills gap is not the finite-dimensional proof; it is proving that the actual Wilson collar-collapse admits the decomposition \(N=\Gamma\circ M+B\) with rank-one \(\Gamma\), positive additive boundary OPE \(B\), and diagonal no-defect for the locked Wilson renormalization. In particular, no current RG estimate yet proves that hairpin/cusp terms at the reflection plane are positive Gram contacts rather than indefinite pair-dependent counterterms.

## Falsifiers

- falsifier: a two-loop reflected Wilson family with normalized multiplicative anomaly \(\Gamma_{11}=\Gamma_{22}=1\), \(0<|\Gamma_{12}|<1\), because the reciprocal Schur multiplier then fails the two-by-two positivity test.
- falsifier: an additive mixed contact matrix with \(B_{11}=B_{22}=0\) but \(B_{12}\ne0\); such a term cannot be positive semidefinite and would show that boundary contacts are not a valid positive Gram sector.
- falsifier: diagonal collar trace failure for a single locked Wilson observable, since then additive boundary fields have already changed the target theory before any mixed OS test is considered.
- falsifier: a required boundary counterterm or cusp-renormalization ratio depending on the pair \((F_i,F_j)\) rather than on individual observables, since this violates the same-theory condition and cannot be absorbed by diagonal congruence.
- falsifier: RG compactness estimates that converge on ordinary Euclidean correlators but not on reflected collar probes \(S(\Theta T_\delta F_i,T_\delta F_j)\), because then the closed-cone transfer is not valid for the needed OS matrices.

## Learning

Cycle 184 separates additive and multiplicative boundary anomalies more sharply. A positive additive contact is not an independent mixed obstruction once diagonal trace continuity is known: by Cauchy-Schwarz, zero diagonal forces the whole contact matrix to vanish. Therefore a surviving mixed additive defect would itself be a falsifier of positive boundary OPE compatibility. The genuinely dangerous Wilson anomalies are now narrowed to nonrank-one multiplicative damping or indefinite pair-dependent contacts. This turns the previous no-new-boundary-renormalization slogan into a concrete finite OS-matrix theorem with a valid linear-algebra proof and a precise Yang-Mills analytic gap.

## Next Experiment

Analyze a two-observable reflected Wilson hairpin model near \(t=0\): compute whether the collar-collapse OPE contact matrix is positive with zero diagonal after locked single-loop renormalization, and separately test whether the multiplicative cusp factor satisfies the two-by-two reciprocal Schur condition \(|\beta|=1\) rather than mixed damping \(|\beta|<1\).
