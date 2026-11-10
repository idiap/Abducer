# cycle-0200

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: three-hairpin Schur-preimage obstruction

## Candidate Lemma

For three locked Wilson hairpin observables, fixed-collar reflection positivity gives a positive collar-limit OS matrix N. If collar collapse differs from the intended plane value only by a nonzero Hermitian multiplicative boundary factor B, then same-theory OS positivity for this triple is exactly positivity of M=B^{[-1]}\circ N. Pairwise damping |N_{ij}|<=|B_{ij}| is only necessary. The first complete phase-sensitive test is the normalized 3 by 3 determinant; a realized violation is a falsifier of the controlled interface even when every two-observable test is valid.

## Definitions

- source object: a regulated lattice/RG family of reflection-positive gauge-invariant Schwinger forms evaluated on three collar-separated Wilson hairpin observables F_i^delta, with cutoff first removed at fixed collar and then delta down to 0 to produce a positive collar OS matrix N.
- target object: the intended continuum OS matrix M_{ij}=S(\Theta F_i,F_j) for the same uncollared Wilson observables in the physical gauge-invariant Schwinger theory.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions, localized to the collar-collapse trace map N=B\circ M and the Schur-preimage test M=B^{[-1]}\circ N.
- same-theory condition: the boundary factor B must be forced by the locked Wilson observable embedding and existing renormalizations; it may not add a new boundary Hilbert sector, pair-dependent counterterm, or coefficient-dependent change of test algebra.
- B^{[-1]} denotes entrywise reciprocal on the tested finite matrix entries, not an operator inverse.

## Assumptions

- At fixed positive collar, RG convergence is valid for every reflected quadratic form S(\Theta F_i^delta,F_j^delta), so the closed-cone argument gives N>=0.
- Diagonal trace continuity is already secured; any positive additive boundary contact with zero diagonal vanishes by finite-dimensional Cauchy-Schwarz.
- B is Hermitian with B_{ii}>0 and B_{ij} nonzero for the tested pairs; diagonal factors are absorbed by congruence so N_{ii}=B_{ii}=M_{ii}=1.
- The three observables remain in the same locked gauge-invariant Wilson algebra before and after cutoff removal.

## Equations

- multiplicative trace factor: `N_{ij}=\lim_{\delta\downarrow0}S(\Theta F_i^\delta,F_j^\delta)=B_{ij}M_{ij},\qquad M=B^{[-1]}\circ N`. Valid when: Valid when collar collapse creates no additive contact and all remaining boundary renormalization is a nonzero pairwise multiplicative factor on this finite Wilson family.
- pairwise necessary threshold: `q_{ij}:=N_{ij}/B_{ij},\qquad \det\begin{pmatrix}1&q_{ij}\\ \overline{q_{ij}}&1\end{pmatrix}\ge0\Longleftrightarrow |q_{ij}|\le1`. Valid when: Valid after diagonal normalization for each two-observable principal minor of the intended target matrix M.
- triple determinant obstruction: `\det M=1-|q_{12}|^2-|q_{13}|^2-|q_{23}|^2+2\operatorname{Re}(q_{12}q_{23}\overline{q_{13}})\ge0`. Valid when: Valid for a normalized Hermitian 3 by 3 OS target matrix; this is the first phase-sensitive condition beyond pairwise damping.
- phase window: `\cos(\Phi_N-\Phi_B)\ge \frac{a_{12}^2+a_{13}^2+a_{23}^2-1}{2a_{12}a_{13}a_{23}},\quad a_{ij}=|N_{ij}/B_{ij}|`. Valid when: Valid when all a_{ij}>0, with Phi_N=arg(N_{12}N_{23}\overline{N_{13}}) and Phi_B=arg(B_{12}B_{23}\overline{B_{13}}); if some a_{ij}=0 the condition reduces to the pairwise minors.

## Attempted Derivation

- Start with regulated reflection positivity at fixed collar: every cutoff matrix N_{a,L}^{delta}=(S_{a,L}(\Theta F_i^delta,F_j^delta)) is positive.
- Use RG convergence in the reflected-probe topology to pass a fixed-collar subsequence to a positive continuum collar matrix, then close the cone to obtain N^delta>=0 and finally N>=0 for the collar limit.
- Use the prior trace analysis: diagonal trace continuity plus positivity eliminates positive additive contacts, so any remaining Wilson boundary discrepancy must be multiplicative on the finite matrix entries.
- Write N=B\circ M. The intended same-theory target is therefore M=B^{[-1]}\circ N, not N itself.
- For two observables, positivity of M gives only |N_{ij}/B_{ij}|<=1. This is valid but incomplete.
- For three observables, normalize the diagonal and compute det M. The determinant contains the phase-sensitive term Re(q_{12}q_{23}\overline{q_{13}}), giving the phase-window inequality.
- Algebraic model check: with B_{ii}=N_{ii}=1, B_{ij}=1/2, N_{12}=N_{23}=0.3, and N_{13}=-0.3, both B and N are positive and all pairwise thresholds pass, but det(B^{[-1]}\circ N)=-0.512.

Blocking gap: No Yang-Mills estimate currently computes or bounds the connected reflected Wilson boundary OPE well enough to determine Phi_B, Phi_N, and the magnitudes a_{ij} for realized three-hairpin families.

## Falsifiers

- A realized three-hairpin Wilson family with normalized B_{ij}=1/2, N_{12}=N_{23}=0.3, and N_{13}=-0.3: B and N are positive, pairwise thresholds are valid, yet det(B^{[-1]}\circ N)=-0.512, making it a finite-matrix falsifier of same-theory OS positivity.
- A boundary OPE producing a cross-ratio phase Phi_B that pushes cos(Phi_N-Phi_B) below the phase-window bound while keeping |N_{ij}|<=|B_{ij}| for every pair.
- Any cutoff-removal topology that controls N pairwise but not the triple reflected product phase; it can certify all two-by-two minors while missing an invalid 3 by 3 OS determinant.
- A nonzero connected coincident-footprint Wilson boundary sector whose Gram factor is not absorbed by the locked observable renormalization and whose Schur preimage has a negative eigenvalue on a realized finite family.

## Learning

Cycle 200 learned that the valid same-theory obstruction is phase-sensitive finite Schur-preimage positivity. Pairwise damping rho_N<=|B_{ij}| is necessary but can miss a negative 3 by 3 determinant. The concrete new invariant is the phase difference Phi_N-Phi_B in q_{12}q_{23}\overline{q_{13}}. Thus the next falsifier is not merely a nonrank-one boundary Gram factor; it is a realized Wilson triple whose boundary cross-ratio phase makes B^{[-1]}\circ N indefinite.

## Next Experiment

Compute the small-loop or perturbative boundary OPE for three reflected Wilson hairpins with a shared reflection-plane footprint; extract B_{ij}, N_{ij}, Phi_B, and Phi_N, then test the normalized determinant det(B^{[-1]}\circ N) before returning to the general finite-matrix proof.
