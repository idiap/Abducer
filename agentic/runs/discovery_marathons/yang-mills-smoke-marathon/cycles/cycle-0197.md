# cycle-0197

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

Realized Boundary Schur-Preimage Bridge Lemma: after fixed-collar reflection positivity has passed to the continuum, a Wilson-sector collar-collapse boundary factor preserves OS positivity for the intended same theory exactly when every realized finite collar-limit OS matrix lies in the Schur image of the target positive cone. Equivalently, for every locked finite Wilson family, the entrywise quotient by the boundary Gram factor is positive semidefinite.

## Definitions

- source object: a directed net of regulated reflection-positive Schwinger forms S_{a,L} on a locked positive-time gauge-invariant algebra, together with collar embeddings T_delta whose finite matrices N^{a,L,delta}_{ij}=S_{a,L}(Theta T_delta F_i,T_delta F_j) are positive semidefinite.
- target object: continuum Schwinger functions S on the same gauge-invariant observable algebra, with OS matrices M_{ij}=S(Theta F_i,F_j) intended to define the physical OS Hilbert space, vacuum vector, and positive Hamiltonian.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions, split into a valid fixed-collar closed-cone passage and a boundary Schur-preimage test for the delta down to zero collar collapse.
- same-theory condition: the observables, collar maps, and renormalizations are fixed before taking the OS limit; a boundary factor B is valid for the same theory only if B^{[-1]} circ N is positive on realized locked Wilson families, or if B is merely a diagonal congruence already included in the fixed normalization.

## Assumptions

- For each finite locked family F_1,...,F_m, fixed-collar RG convergence is strong enough to pass all reflected quadratic forms, so N^delta >= 0 and N=lim_{delta down to 0} N^delta exists entrywise.
- The boundary OPE for reflected Wilson collars has the finite-matrix form N=A+B circ M, where A is an additive contact matrix and B is a multiplicative boundary Gram factor with nonzero entries on the tested family.
- Diagonal trace continuity is valid: A_{ii}=0 after the individual Wilson operators have been locked to the target normalization.
- The additive contact matrix A is positive semidefinite whenever it arises as a boundary Hilbert-sector covariance.

## Equations

- boundary factorization: `N_{ij}=\lim_{\delta\downarrow0}S(\Theta T_\delta F_i,T_\delta F_j)=A_{ij}+B_{ij}M_{ij}`. Valid when: The collar collapse admits a Wilson boundary OPE with an additive contact part A and a multiplicative hairpin Gram factor B.
- additive contact elimination: `A\succeq0,\quad A_{ii}=0\ \forall i\quad\Longrightarrow\quad A_{ij}=0\ \forall i,j`. Valid when: A is a positive boundary covariance and diagonal trace continuity has already removed individual boundary defects.
- same-theory Schur preimage criterion: `M=B^{[-1]}\circ N\succeq0`. Valid when: All relevant B_{ij}\neq0 and no new boundary algebra or counterterm is allowed in the target theory.
- three point determinant detector: `R_{ij}=\widehat N_{ij}/\widehat B_{ij},\quad \det R=1+2\operatorname{Re}(r_{12}r_{23}\overline{r_{13}})-|r_{12}|^2-|r_{23}|^2-|r_{13}|^2\ge0`. Valid when: The three observables are normalized so R_{ii}=1; failure is a 3-by-3 falsifier even if all two-by-two thresholds pass.

## Attempted Derivation

- Fix a finite locked family F_1,...,F_m in the positive-time gauge-invariant Wilson algebra and push it into a collar by T_delta so that reflection positivity gives N^{a,L,delta}=(S_{a,L}(Theta T_delta F_i,T_delta F_j))_{ij} >= 0.
- Use the cutoff-removal topology to take a fixed-delta continuum limit and then the closed-cone argument to keep N^delta >= 0. If the delta down to zero limit exists entrywise, the collar-limit matrix N is positive semidefinite.
- Model the possible reflection-plane obstruction by a finite boundary OPE N=A+B circ M, where M is the intended target OS matrix, A is additive contact, and B is a multiplicative Wilson hairpin Gram factor.
- If A is positive and diagonal trace continuity gives A_{ii}=0, Cauchy-Schwarz for positive matrices gives A=0. Thus the only remaining obstruction is multiplicative: N=B circ M.
- Since the same-theory target is M rather than the enlarged boundary theory represented by N, OS positivity is exactly B^{[-1]} circ N >= 0 on every realized finite family.
- For m=2 this recovers the cycle-196 threshold rho_N <= |B_{12}|. For m=3, positivity adds the determinant inequality for R=widehat B^{[-1]} circ widehat N, so pairwise threshold tests are not complete.

Blocking gap: The Yang-Mills analytic gap is now precise: there is no estimate proving that every realized locked Wilson collar matrix N has a positive Schur preimage through the boundary Gram factor B, and no computation ruling out a three-observable hairpin determinant falsifier.

## Falsifiers

- A realized three-Wilson family has N>=0 and satisfies all pairwise inequalities |widehat N_{ij}|<=|widehat B_{ij}|, but det(widehat B^{[-1]} circ widehat N)<0; this is a finite falsifier of same-theory OS positivity.
- A boundary OPE produces an additive contact A with A_{ii}=0 but A not positive semidefinite, so the Cauchy-Schwarz elimination is invalid and the additive sector can itself change the target theory.
- Some B_{ij}=0 while the corresponding collar-limit N_{ij} is nonzero, making the intended target quotient singular rather than a valid OS matrix.
- The gauge-invariant Wilson algebra is too poor to realize any determinant test beyond rank-one or mutually commuting boundary footprints, so the bridge cannot be promoted without an explicit richness or density theorem.

## Learning

Cycle 197 upgrades the cycle-196 two-by-two threshold into the exact finite Schur-preimage criterion. The closed-cone step is valid for collar-limit matrices N, but same-theory OS positivity requires M=B^{[-1]} circ N to be positive on every realized locked Wilson family. The new discovery is that pairwise damping tests are incomplete: a three-observable boundary phase or triangle-correlation determinant can be a falsifier even when every two-by-two inequality passes. The next analytic burden is therefore to prove Schur-preimage positivity for all realized Wilson finite matrices, or to compute a concrete three-hairpin determinant obstruction.

## Next Experiment

Construct the smallest explicit reflected Wilson triple with coincident boundary footprints; estimate the normalized boundary Gram entries B_{ij} and collar correlations N_{ij}, then test the determinant of R=widehat B^{[-1]} circ widehat N as the first non-pairwise same-theory falsifier.
