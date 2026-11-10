# cycle-0182

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

Finite OS-matrix boundary-defect transfer lemma: fixed-collar reflection positivity transfers to the intended non-collared continuum OS matrix if the collar trace defect is zero or a nonzero rank-one congruence already belonging to the locked observable normalization. More sharply, if the normalized Wilson boundary defect is a non-rank-one positive correlation matrix, then closed-cone positivity of the collar limit is not by itself a valid proof of positivity for the target Schwinger functions; a two-dimensional falsifier matrix can make the collar matrix positive while the intended matrix is indefinite.

## Definitions

- source object: cutoff Yang-Mills gauge-invariant Schwinger functionals S_{a,L} on a locked positive-time algebra A_+ with collar embeddings T_\delta and regulated reflection-positive matrices Q_{a,L}(T_\delta F,c).
- target object: continuum OS-positive Schwinger functional S on the intended non-collared gauge-invariant algebra A_+ producing the physical OS Hilbert pre-inner product.
- controlled interface: for each finite family F_1,\ldots,F_n, the RG limit controls fixed-collar reflected matrix entries and the collar trace has an entrywise defect representation N_{ij}=B_{ij}M_{ij}.
- same-theory condition: the defect B must be identically one or a nonzero rank-one congruence B_{ij}=\overline{b_i}b_j coming from observable normalizations already included in the locked theory, with no pair-dependent boundary counterterm.

## Assumptions

- For every cutoff pair (a,L) and every finite family in the positive-time gauge-invariant algebra, the regulated OS matrix is positive semidefinite.
- For each fixed collar distance \delta>0, the cutoff-removal topology gives convergence of every reflected matrix entry S_{a,L}(\Theta T_\delta F_i,T_\delta F_j).
- The limit \delta\downarrow0 of fixed-collar continuum matrices exists as N_{ij}=\lim_{\delta\downarrow0}S(\Theta T_\delta F_i,T_\delta F_j).
- The intended target matrix is M_{ij}=S(\Theta F_i,F_j), and the trace comparison is multiplicative on the chosen finite family: N_{ij}=B_{ij}M_{ij}.
- The rank-one factors b_i, when present, are nonzero and do not change the observable algebra; they are only individual normalizations, not mixed boundary data.

## Equations

- fixed-collar OS matrix: `N^{(\delta)}_{ij}=S(\Theta T_\delta F_i,T_\delta F_j),\qquad \sum_{i,j}\overline{c_i}c_jN^{(\delta)}_{ij}\ge 0`. Valid when: The collar keeps all reflected supports away from the reflection plane and the RG limit is valid for those reflected probes.
- boundary-defect comparison: `N_{ij}=\lim_{\delta\downarrow0}N^{(\delta)}_{ij}=B_{ij}M_{ij},\qquad M_{ij}=S(\Theta F_i,F_j)`. Valid when: The collar trace exists entrywise and no additive contact term remains after the locked renormalizations.
- rank-one congruence transfer: `B_{ij}=\overline{b_i}b_j\neq0\quad\Longrightarrow\quad N=D^*MD,\;D=\operatorname{diag}(b_i),\;N\ge0\Rightarrow M\ge0`. Valid when: The defect is purely individual and the same-theory condition permits the diagonal normalization.
- two-by-two nonfactorizing falsifier: `B=\begin{pmatrix}1&\beta\\ \overline\beta&1\end{pmatrix},\ |\beta|<1,\quad M=\begin{pmatrix}1&r e^{-i\arg\beta}\\ r e^{i\arg\beta}&1\end{pmatrix},\quad 1<r<|\beta|^{-1}`. Valid when: Then M has eigenvalue 1-r<0 while B\circ M is positive; this is valid as a logical obstruction to any proof using only positivity of the collar matrix.

## Attempted Derivation

- Start with regulated reflection positivity: for every cutoff (a,L), every collar distance \delta>0, and every finite family F_i in the positive-time gauge-invariant algebra, the matrix S_{a,L}(\Theta T_\delta F_i,T_\delta F_j) is positive semidefinite.
- Use the cutoff-removal topology only at fixed \delta. If all reflected fixed-collar entries converge, the closed positive cone of finite Hermitian matrices gives N^{(\delta)}\ge0 in the continuum.
- Let \delta\downarrow0. Entrywise convergence of N^{(\delta)} to N again preserves positivity, so the collar-limit matrix N is positive. Up to this point the proof is formal and valid.
- The target OS matrix is not N but M_{ij}=S(\Theta F_i,F_j). The missing bridge is therefore the trace comparison between N and M, not reflection positivity itself.
- Assume a multiplicative boundary-defect expansion N_{ij}=B_{ij}M_{ij}. If B_{ij}=\overline{b_i}b_j with all b_i\neq0, then N=D^*MD. Since D is invertible, positivity of N implies positivity of M by congruence: y^*My=(D^{-1}y)^*N(D^{-1}y)\ge0.
- Test necessity of this condition for a closed-cone-only proof. Normalize a two-observable Wilson defect to B_{11}=B_{22}=1 and B_{12}=\beta. If |\beta|<1, choose 1<r<|\beta|^{-1} and set M_{12}=r e^{-i\arg\beta}. Then M is indefinite, but B\circ M is positive. Thus collar positivity can hold while target positivity fails.
- This exhibits the exact role of the same-theory condition: individual congruences are harmless, but pair-dependent damping or mixed boundary contact terms can manufacture a positive collar-limit matrix without proving OS positivity for the intended Yang-Mills Schwinger functions.

Blocking gap: The unresolved Yang-Mills estimate is a finite OS-matrix no-new-boundary-renormalization theorem for reflected Wilson products: after ordinary loop renormalization, prove that every mixed collar defect B is rank one, preferably B=1, or show that any residual defect is an already locked individual normalization.

## Falsifiers

- A two-loop Wilson pair with normalized mixed defect |B_{12}|/(B_{11}B_{22})^{1/2}<1 after locked individual renormalizations; this is a direct falsifier because the explicit 2-by-2 matrix construction shows positivity need not transfer.
- A nonzero multiplicative minor B_{ij}B_{k\ell}-B_{i\ell}B_{kj}; this detects a pair-dependent boundary anomaly incompatible with rank-one same-theory congruence.
- An additive reflection-plane contact term C_{ij} in N_{ij}=B_{ij}M_{ij}+C_{ij} that cannot be represented by an existing local observable in the locked algebra.
- A cusp or hairpin anomalous factor in mixed reflected Wilson products that depends on the relative geometry of W_i and W_j rather than on the individual loops.
- The cutoff-removal topology controls separated Wilson loops but not the limit in which reflected supports approach the plane, so fixed-collar positivity remains valid but the trace bridge is unavailable.
- The continuum construction changes the Wilson-loop algebra by adding boundary-renormalized observables; positivity may survive there, but that would be the wrong same-theory target.

## Learning

Cycle 182 turns the previous nonfactorizing-anomaly warning into a precise finite-dimensional bridge theorem. The closed-cone argument gives positivity of the collar-limit matrix N, but the intended OS matrix M is protected only when the boundary trace defect is an invertible rank-one congruence. A normalized mixed Wilson damping |\beta|<1 is not a cosmetic anomaly: it gives an explicit 2-by-2 falsifier where N is positive and M is indefinite. Thus the remaining Yang-Mills problem is sharply localized: prove a finite OS-matrix no-new-boundary-renormalization theorem for reflected Wilson products, while the local mirror-flat sector remains plausibly valid by distributional continuity.

## Next Experiment

Compute the one-loop small-collar asymptotic for two reflected rectangular or hairpin Wilson loops crossing the reflection collar: remove ordinary perimeter and corner factors, form \beta_{CD}=B_{CD}/(B_{CC}B_{DD})^{1/2}, and check whether \beta_{CD}=1 or a nontrivial damping remains. This gives the fastest concrete falsifier or evidence for the rank-one defect theorem.
