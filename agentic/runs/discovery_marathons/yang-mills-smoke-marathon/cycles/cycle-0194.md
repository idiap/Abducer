# cycle-0194

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

Let a locked gauge-invariant Wilson core admit collar observables whose fixed-collar OS matrices are positive and whose collar collapse has only a multiplicative boundary Gram factor. For a tested pair, if the normalized anomaly entry satisfies |Gamma_{12}|<1 and the realized collar OS cone contains a normalized two-observable matrix with |N_{12}|>|Gamma_{12}|, then the intended same-theory OS matrix M=Gamma^{[-1]}\circ N has negative determinant. Hence a nonrank-one boundary Gram factor is a genuine falsifier only when the locked algebra realizes such near-parallel two-by-two tests; without that realization, the previous rank-one conclusion overclaims.

## Definitions

- source object: finite collar-separated Wilson observable families W_i^delta in the regulated/reflection-positive lattice or continuum cutoff theory, with normalized fixed-collar OS matrices N^delta_{ij}=S_{a,L}(Theta W_i^delta,W_j^delta).
- target object: the intended continuum OS matrix M_{ij}=S(Theta W_i,W_j) on the same gauge-invariant Wilson observables after removing the collar, before adding any boundary label or counterterm.
- controlled interface: a collar trace relation N_{ij}=Gamma_{ij} M_{ij}+A_{ij}, with Gamma a normalized multiplicative boundary Gram factor, Gamma_{ii}=1, and A an additive contact matrix forced to vanish when diagonal trace continuity and contact positivity are valid.
- same-theory condition: the collar removal map identifies W_i^delta with W_i inside the original gauge-invariant test algebra, allowing only pre-declared individual renormalizations, i.e. diagonal congruences, and forbidding pair-dependent boundary sectors or new reflection-plane observables.

## Assumptions

- Fixed-collar reflection positivity is available: every finite matrix N^delta is positive and the RG topology is strong enough to pass its entries to a limiting positive matrix N.
- The additive contact part A is positive or at least satisfies the diagonal-zero Cauchy-Schwarz vanishing criterion after diagonal trace continuity has been proved.
- For the tested pair, the multiplicative anomaly Gamma is a positive normalized boundary Gram matrix with Gamma_{12}=beta and |beta|<1.
- Realized near-parallel testing holds for that pair: after normalizing diagonals, the locked Wilson core realizes a valid collar limit N with |N_{12}|>|beta|, preferably with N_{12} arbitrarily close to the phase of beta.

## Equations

- collar-limit anomaly decomposition: `N_{ij}=\lim_{\delta\downarrow0} S(\Theta W_i^\delta,W_j^\delta)=\Gamma_{ij}M_{ij}+A_{ij}`. Valid when: The same regulated Wilson family is used on both sides, the collar limit exists entrywise, and all boundary effects split into a multiplicative Gram factor plus an additive contact term.
- additive-contact disappearance: `A\ge0,\quad A_{ii}=0\ \forall i\quad\Longrightarrow\quad A_{ij}=0\ \forall i,j`. Valid when: A is a positive semidefinite contact matrix; then Cauchy-Schwarz gives |A_{ij}|^2\le A_{ii}A_{jj}=0.
- two-by-two intended determinant: `M^{(2)}=\begin{pmatrix}1&n/\beta\\ \overline n/\overline\beta&1\end{pmatrix},\qquad \det M^{(2)}=1-|n/\beta|^2`. Valid when: The two observables are normalized so N_{11}=N_{22}=M_{11}=M_{22}=1, A=0, beta=Gamma_{12}\ne0, and n=N_{12}.
- realized determinant falsifier: `|\beta|<|n|\le1\quad\Longrightarrow\quad N^{(2)}\ge0\ \text{but}\ \det M^{(2)}<0`. Valid when: The collar matrix N^{(2)} is an actually realized positive OS matrix and the intended target matrix is obtained by removing the boundary factor without changing the theory.

## Attempted Derivation

- Start from fixed-collar positivity: for every delta>0 and every finite coefficient vector c, c^*N^delta c>=0; the closed-cone argument is valid after entrywise convergence of these reflected forms.
- Collapse the collar and write the most general boundary trace defect still compatible with earlier cycles: N=Gamma\circ M+A. Earlier work showed a positive additive A with zero diagonal must vanish, so the durable obstruction is multiplicative Gamma.
- Normalize a two-observable submatrix so N_{11}=N_{22}=M_{11}=M_{22}=1 and set beta=Gamma_{12}. Then N positivity only requires |n|<=1, while intended M positivity requires |n/beta|<=1.
- If |beta|<1 and the locked algebra realizes n with |beta|<|n|<=1, the collar matrix N is positive but M has determinant 1-|n/beta|^2<0. This is an actual falsifier, not merely an abstract Schur-multiplier example.
- Therefore the previous cycles' statement 'nonrank-one boundary covariance falsifies the bridge' is valid only after adding a realized-richness hypothesis. The proof obligation moves from all positive matrices to the physically realized Wilson OS cone.

Blocking gap: We do not yet know whether the locked gauge-invariant Wilson algebra realizes the required near-parallel two-by-two collar matrices for arbitrary distinct boundary hairpin footprints. Without that, a nonrank-one boundary Gram factor might be invisible to the actual OS test cone.

## Falsifiers

- A concrete pair of Wilson hairpin footprints with beta=Gamma_{12}, |beta|<1, and an actually realized normalized collar OS entry n satisfying |beta|<|n|<=1 is a determinant falsifier of the same-theory OS bridge.
- If additive contact terms are not positive or have nonzero diagonal after diagonal trace locking, then the reduction to multiplicative Gamma is invalid.
- If the RG cutoff-removal topology is not strong enough to take the limit of the near-parallel reflected Wilson matrix entries, the determinant test cannot be transported to the continuum.
- If the only realized Wilson OS matrices satisfy |N_{12}|<=|Gamma_{12}| whenever |Gamma_{12}|<1, then nonrank-one boundary covariance is not by itself a falsifier; the branch must study the smaller realized cone.

## Learning

Cycle 194 corrects the previous rank-one story in a useful way. The universal Schur-multiplier argument is too strong for Yang-Mills because the theory supplies only realized Wilson OS matrices. The valid bridge lemma is now a realized two-by-two detector: a nonrank-one boundary Gram factor breaks the same-theory OS passage exactly when the locked Wilson core can make collar observables more correlated than the boundary Gram entry allows. This turns the vague richness hypothesis into a concrete determinant experiment and separates formal positivity preservation from the analytic question of whether Wilson hairpin probes are rich enough to see boundary covariance.

## Next Experiment

Build the simplest Wilson hairpin pair with common bulk loop and distinct boundary footprint labels; compute or bound the normalized collar OS entry n and the boundary Gram beta. The decisive check is whether |n| can be forced above |beta| while the reflected matrix remains a valid collar OS matrix.
