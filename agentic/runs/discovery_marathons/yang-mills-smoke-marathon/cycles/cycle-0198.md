# cycle-0198

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: finite Schur-preimage obstruction

## Candidate Lemma

Assume fixed-collar RG convergence is valid for every finite reflected gauge-invariant Wilson family and that additive reflection-plane contacts vanish after diagonal trace continuity. Then same-theory OS positivity of the target continuum functions is equivalent to positivity of the Schur preimage B(F)^{[-1]} circ N(F) for every realized finite collar OS matrix N(F). Pairwise damping inequalities are necessary but not sufficient; the first genuinely new falsifier can occur in a three-observable determinant through a boundary phase or triangle-correlation defect.

## Definitions

- source object: finite collar OS matrices N(F) obtained from regulated reflection-positive Schwinger forms S_{a,L}(Theta T_delta F_i,T_delta F_j) on the locked positive-time gauge-invariant Wilson/composite algebra.
- target object: intended continuum same-theory OS matrices M(F)=S(Theta F_i,F_j) on the same labeled observables, before adding boundary counterterms or changing Wilson-loop renormalization at the reflection plane.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions by passing fixed-collar positive matrices to N(F), then proving the boundary trace correction sends N(F) to a positive M(F).
- same-theory condition: the observable labels F_i, gauge-invariant test algebra, and Wilson renormalization convention are identical before and after collar collapse; any boundary factor B must be a removable congruence or a Schur-preimage-positive defect, not a hidden change of theory.

## Assumptions

- For each fixed collar width delta>0, T_delta F_i has support strictly in t>0 and S_{a,L} is reflection positive on the regulated lattice/continuum cutoff theory.
- The cutoff-removal topology controls every mixed reflected matrix entry S_{a,L}(Theta T_delta F_i,T_delta F_j), not only individual Wilson expectations.
- The collar collapse has a boundary OPE of the form N_{ij}=B_{ij}M_{ij}+A_{ij}, with B_{ij} nonzero on the finite family under test.
- Diagonal trace continuity is valid; if A is a positive additive contact matrix, A_{ii}=0 forces A=0 by Cauchy-Schwarz.
- The matrix family N(F) is the realized cone supplied by the locked Yang-Mills Wilson algebra, not the full cone of all abstract positive matrices.

## Equations

- fixed-collar closed cone: `N^{\delta}_{ij}(F)=\lim_{a,L} S_{a,L}(\Theta T_\delta F_i,T_\delta F_j),\qquad N^\delta(F)\succeq 0`. Valid when: The RG compactness topology is strong enough for all finite reflected collar probes.
- boundary factorization: `N_{ij}(F)=B_{ij}(F)M_{ij}(F)+A_{ij}(F)`. Valid when: The reflected Wilson collar collapse admits a multiplicative boundary factor plus an additive contact term.
- same-theory Schur preimage: `A=0,\ B_{ij}\ne0\ \Longrightarrow\ M(F)=B(F)^{[-1]}\circ N(F),\qquad M(F)\succeq 0`. Valid when: OS positivity is being claimed for the intended target observables, not for a boundary-renormalized algebra.
- three-point determinant test: `D_3(M)=1+2\operatorname{Re}(m_{12}m_{23}\overline{m_{13}})-|m_{12}|^2-|m_{23}|^2-|m_{13}|^2\ge 0`. Valid when: M is normalized to M_{ii}=1; this condition is required in addition to all 2-by-2 principal minors.

## Attempted Derivation

- Start with regulated reflection positivity: for every cutoff and fixed collar width delta, the finite OS matrix S_{a,L}(Theta T_delta F_i,T_delta F_j) is positive.
- Use the RG-to-OS closed-cone passage to obtain a positive fixed-collar continuum matrix N^delta(F), then pass delta down to the reflection plane where the collar limit exists.
- Model the collar collapse by a boundary OPE N=B circ M + A. Diagonal trace continuity gives A_{ii}=0. If A is a positive contact matrix, Cauchy-Schwarz gives A_{ij}=0, so the additive contact vanishes.
- The intended same-theory target matrix is therefore M=B^{[-1]} circ N. Thus the exact bridge condition is not positivity of N alone, but positivity of this Schur preimage for every realized locked Wilson family.
- For two observables the condition reduces to the valid threshold |N_{12}|/sqrt(N_{11}N_{22}) <= |B_{12}|/sqrt(B_{11}B_{22}).
- For three observables, pairwise thresholds do not decide positivity. The normalized determinant D_3 detects boundary triangle phase and correlation defects; a negative D_3 is a concrete same-theory falsifier even when every two-by-two minor is nonnegative.

Blocking gap: The remaining gap is analytic, not linear algebraic: derive the boundary OPE factor B for reflected Wilson hairpins and prove Schur-preimage positivity for all realized finite Wilson matrices, or exhibit an actual realized triple with negative D_3 after division by B.

## Falsifiers

- A three-hairpin Wilson family for which N(F) is positive but det(B^{[-1]} circ N(F))<0 is a decisive same-theory falsifier.
- A boundary OPE with nonzero additive contact after diagonal trace continuity would falsify the reduction to the multiplicative Schur-preimage problem.
- A cutoff-removal topology that controls single Wilson loop limits but not mixed reflected entries S(Theta F_i,F_j) falsifies the claimed valid RG-to-OS interface.
- A boundary factor B with zeros where the realized collar matrix N has nonzero entries is a falsifier for entrywise same-theory reconstruction.
- A proof that only all two-by-two thresholds hold, with no finite determinant control, is not valid for full OS positivity because triple phase obstructions can remain.

## Learning

Cycle 198 shows that the branch must not promote from pairwise damping tests to OS positivity. The valid condition is finite Schur-preimage positivity on the realized Wilson cone, and the first phase-sensitive falsifier is a three-hairpin determinant. This sharpens the obstruction from a vague nonrank-one boundary Gram factor to an explicit matrix experiment: compute B and N for triples, then test det(B^{[-1]} circ N).

## Next Experiment

Work out the smallest reflected Wilson hairpin triple near the reflection plane: compute or bound the normalized boundary anomaly beta_{ij}, estimate the realized collar correlations N_{ij}, and evaluate the three-point determinant D_3(B^{[-1]} circ N) as the next concrete falsifier test.
