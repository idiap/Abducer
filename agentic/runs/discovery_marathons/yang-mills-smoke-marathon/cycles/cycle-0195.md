# cycle-0195

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

Let a locked Wilson collar core have fixed-collar OS limits N^{\delta}\ge 0 and suppose collar collapse produces a positive normalized boundary Gram factor B with N_{ij}=B_{ij}M_{ij} for the intended same-theory boundary OS matrix M. For any realized two-observable block with unit diagonal normalization, the same-theory passage is valid exactly when |M_{12}|\le 1, equivalently |N_{12}|\le |B_{12}|. Thus a nonrank-one boundary Gram factor is a falsifier only if the locked Wilson core realizes an OS correlation exceeding the boundary Gram damping threshold.

## Definitions

- source object: regulated reflection-positive gauge-invariant Wilson collar Schwinger forms S_{a,L}(\Theta F_i^{\delta},F_j^{\delta}) with a,L removed first at fixed collar distance \delta>0
- target object: OS-positive continuum Schwinger functions on the locked gauge-invariant Wilson algebra after the collar observables are traced to the reflection plane without adding boundary counterterms
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions, mediated by finite reflected quadratic forms and a boundary trace map T_\delta F -> F
- same-theory condition: the boundary trace map identifies the same Wilson observable before and after collar collapse; any multiplicative anomaly must be an already-locked diagonal congruence or must pass every realized determinant test in the target algebra

## Assumptions

- For every finite collar family F_i^{\delta}, cutoff removal gives an OS-positive matrix N^{\delta}_{ij}=S(\Theta F_i^{\delta},F_j^{\delta}) and N^{\delta}->N entrywise.
- The intended boundary matrix M_{ij}=S(\Theta F_i,F_j) exists as a distributional trace of the same Wilson observables.
- The only remaining collar-collapse defect in the Wilson sector is multiplicative on each finite block: N_{ij}=B_{ij}M_{ij}, with B_{ii}>0 and B positive semidefinite as a boundary Gram matrix.
- The two-observable block is normalized so M_{11}=M_{22}=1 and B_{11}=B_{22}=1; the same argument applies after diagonal rescaling when diagonals are positive.

## Equations

- multiplicative boundary factorization: `N_{ij}=B_{ij}M_{ij}`. Valid when: The collar limit has no additive boundary contact term and all residual reflected Wilson hairpin effects enter as a finite-block multiplicative boundary Gram factor.
- two-by-two target determinant: `M\ge 0\quad\Longleftrightarrow\quad \det M=1-|M_{12}|^2\ge 0`. Valid when: The two-observable target OS block is Hermitian and normalized by positive diagonal entries.
- realized damping detector: `M_{12}=N_{12}/B_{12},\qquad M\ge0\quad\Longleftrightarrow\quad |N_{12}|\le |B_{12}|`. Valid when: B_{12}\ne0 and the multiplicative factorization holds for the realized two-observable block.
- cross-ratio obstruction: `K_{12;12}=\log B_{11}+\log B_{22}-\log B_{12}-\log B_{21}=-2\log |B_{12}|`. Valid when: The normalized boundary Gram entries are nonzero and phases have been removed by diagonal unitary rescaling.

## Attempted Derivation

- Start with fixed-collar reflection positivity: for any coefficients c, c^*N^{\delta}c\ge0. Entrywise cutoff removal at fixed \delta preserves this by the closed cone argument, so N^{\delta}->N with N\ge0.
- Assume the collar trace does not alter the algebra except through a boundary Gram factor B, so N=B\circ M. This is the precise place where the same-theory condition is tested rather than assumed.
- Normalize a two-observable realized block by positive diagonal congruence, giving B_{11}=B_{22}=M_{11}=M_{22}=1. Positivity of B gives |B_{12}|\le1 and positivity of N gives |N_{12}|\le1.
- The intended target block is M_{12}=N_{12}/B_{12}. Its determinant is 1-|N_{12}/B_{12}|^2. Therefore the target OS block is positive exactly when the realized collar correlation is no larger than the boundary Gram correlation: |N_{12}|\le|B_{12}|.
- If |B_{12}|<1 but the Wilson core cannot realize |N_{12}|>|B_{12}|, then the nonrank-one boundary sector is not yet a falsifier. If such a pair is realized, the determinant is negative and the same-theory OS bridge fails.

Blocking gap: The missing analytic input is a richness or separation theorem for the locked Wilson core: can reflected Wilson hairpin observables realize collar OS correlations above a prescribed nonrank-one boundary damping level |B_{12}|, or are all realized correlations automatically bounded by the boundary Gram factor?

## Falsifiers

- A concrete two-loop hairpin family with normalized |B_{12}|<1 and realized fixed-collar |N_{12}|>|B_{12}| is a determinant falsifier of the same-theory OS passage.
- An additive boundary contact term with zero diagonal but nonzero off-diagonal would falsify the positive-contact reduction used before the multiplicative detector.
- If the cutoff-removal topology controls fixed-collar probes but not the \delta->0 trace of mixed reflected Wilson products, then the closed-cone argument is valid only on the collar algebra and not on the intended continuum algebra.
- If quotienting or renormalizing Wilson loops at the reflection plane changes B by an unrecorded boundary counterterm, the positivity proof may describe a modified theory rather than the same Yang-Mills target.

## Learning

Cycle 195 turns the previous richness caveat into a precise two-by-two inequality. A nonrank-one boundary Gram factor is not automatically a same-theory falsifier; it becomes one exactly when the realized collar OS correlation exceeds the damping supplied by the boundary Gram entry. This is useful because it gives a valid finite determinant experiment: compute or bound |B_{12}| from the boundary hairpin OPE and compare it with an actually realized |N_{12}| from locked Wilson collar observables. The bridge has moved from universal Schur-multiplier overclaiming to a concrete realized-correlation threshold.

## Next Experiment

Model two reflected Wilson hairpins sharing one reflection-plane footprint. Derive the leading boundary OPE contribution to B_{12}, then test whether a locked pair of collar loop observables can realize |N_{12}| above that value after diagonal normalization.
