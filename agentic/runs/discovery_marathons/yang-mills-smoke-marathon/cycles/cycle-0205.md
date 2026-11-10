# cycle-0205

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology, cycle 205

## Candidate Lemma

Finite quotient-holonomy boundary bridge: for any finite locked Wilson family whose collar OS matrices converge, same-theory OS positivity after collar collapse is equivalent to positivity of the normalized Hadamard quotient by the boundary anomaly matrix. The closed-cone step gives the collar limit N >= 0; the nonformal Yang-Mills content is proving that Q = \widehat N \oslash \widehat B is positive semidefinite on every realized finite family, not merely proving that B is close to trivial.

## Definitions

- source object: finite collar-separated reflected Wilson OS matrices N^{\delta}_{ij}=S(\Theta T_{\delta}F_i,T_{\delta}F_j) obtained from regulated reflection-positive Schwinger forms and then sent through the RG continuum limit at fixed collar width.
- target object: intended continuum same-theory OS matrices M_{ij}=S(\Theta F_i,F_j) for the locked gauge-invariant Wilson/core observable algebra at the reflection plane.
- controlled interface: a nonzero multiplicative boundary anomaly matrix B with N=B\circ M after additive contacts have been ruled out, together with normalized matrices \widehat N, \widehat B, \widehat M having unit diagonal.
- same-theory condition: M is not allowed to absorb B into a redefined boundary Wilson observable or enlarged boundary algebra; diagonal normalizations may be fixed by the original renormalized observables, but pair-dependent boundary factors must be removed only if the resulting \widehat M remains OS-positive.

## Assumptions

- For every finite family F_1,...,F_n in the locked Wilson core, collar approximants T_{\delta}F_i lie in the positive-time test algebra and preserve the reflection operation.
- The cutoff-removal topology is valid for each reflected collar matrix entry, so N^{\delta}_{ij} has a continuum collar limit N_{ij}.
- Diagonal trace continuity is already proved, and any positive additive boundary contact has zero diagonal; hence Cauchy-Schwarz forces that additive contact to vanish.
- The multiplicative anomaly entries B_{ij} are finite and nonzero on the tested finite family, with B_{ii}>0, so normalized Hadamard division is well-defined.
- Hermitian conventions are fixed: N_{ji}=\overline{N_{ij}}, B_{ji}=\overline{B_{ij}}, and M_{ji}=\overline{M_{ij}}.

## Equations

- collar positivity limit: `N^{\delta}_{ij}=S(\Theta T_{\delta}F_i,T_{\delta}F_j),\qquad N^{\delta}\ge 0,\qquad N^{\delta}\to N\ \Longrightarrow\ N\ge0`. Valid when: The RG-to-OS topology controls the finite reflected collar probes, so the closed cone of positive semidefinite matrices is reached by an actual entrywise limit.
- boundary anomaly quotient: `N=B\circ M,\qquad \widehat M_{ij}=\frac{\widehat N_{ij}}{\widehat B_{ij}}=:Q_{ij},\qquad \widehat M\ge0\ \Longleftrightarrow\ Q\ge0`. Valid when: Additive contacts vanish, B has no zero entries on the finite family, and diagonal congruences from normalization are same-theory allowed.
- phase holonomy obstruction: `q_{ij}=|q_{ij}|e^{i\theta_{ij}},\qquad H_{ijk}=\theta_{ij}+\theta_{jk}-\theta_{ik}\ \mod 2\pi`. Valid when: The quotient matrix Q is normalized Hermitian and all three tested off-diagonal entries are nonzero; H_{ijk} is invariant under diagonal unitary rephasing of observables.

## Attempted Derivation

- Start with a finite locked Wilson family F_1,...,F_n and push it off the reflection plane by collars T_{\delta}F_i. Reflection positivity of the regulated lattice/continuum collar construction gives N^{\delta}=[S(\Theta T_{\delta}F_i,T_{\delta}F_j)] >= 0.
- Use the RG-to-OS closed-cone bridge only at fixed collar: if every reflected entry converges, then N^{\delta}->N entrywise and N remains positive semidefinite. This part is valid and no longer contains the hard Yang-Mills issue.
- Model the collar-collapse boundary OPE as N=B\circ M+C, where M is the intended plane OS matrix, B is a multiplicative boundary anomaly, and C is an additive contact matrix. Diagonal trace continuity gives C_{ii}=0; if C is a positive contact form, Cauchy-Schwarz gives C_{ij}=0, so the remaining obstruction is multiplicative.
- Normalize diagonals. Positive diagonal congruence does not affect OS positivity, so the target condition is \widehat M>=0. From N=B\circ M we get \widehat M=\widehat N\oslash\widehat B=:Q. Hence same-theory OS positivity is exactly Q>=0 on the realized finite Wilson family.
- For n=3, write Q_{ij}=\rho_{ij}e^{i\phi_{ij}}. The determinant expansion gives 1-\rho_{12}^2-\rho_{23}^2-\rho_{13}^2+2\rho_{12}\rho_{23}\rho_{13}\cos(\phi_{12}+\phi_{23}-\phi_{13}). This exposes the first phase-sensitive falsifier beyond pairwise damping.
- If all cycle phase holonomies vanish on the finite support graph, solve \theta_{ij}=\alpha_i-\alpha_j and apply the diagonal unitary D. The problem reduces to checking positive semidefiniteness of the real modulus quotient matrix R. If some cycle holonomy survives, principal minors involving that cycle must be tested directly.

Blocking gap: The derivation is finite-dimensional and valid once the boundary OPE data B and the collar matrix N exist, but Yang-Mills analysis has not yet proved the required boundary OPE for reflected Wilson hairpins, the vanishing/positivity of additive contacts, or Schur-preimage positivity of Q on a dense locked Wilson core.

## Falsifiers

- A three-hairpin Wilson calculation with N>=0 but det(\widehat N\oslash\widehat B)<0 is a concrete falsifier of same-theory OS positivity after collar collapse.
- A nonzero additive boundary contact C with zero diagonal but not positive as a contact form would falsify the reduction from N=B\circ M+C to the pure multiplicative quotient model.
- A quotient phase triangle with negative determinant shows that pairwise damping bounds are not a valid substitute for finite OS positivity.
- If the RG cutoff-removal topology controls single Wilson loops but not mixed reflected triple products, then the closed-cone-to-quotient derivation is not valid for the needed test algebra.
- If the anomaly B is absorbed by redefining the boundary Wilson algebra, the positivity statement may be true for a modified theory but is a same-theory falsifier for the intended Yang-Mills Schwinger functions.

## Learning

Cycle 205 learned that the post-collar bridge is an exact Schur-preimage problem on realized Wilson OS matrices. The valid closed-cone argument supplies N>=0, but same-theory positivity is precisely Q=\widehat N\oslash\widehat B>=0 after additive contacts are eliminated. This is stronger than pairwise damping and weaker than demanding B be rank one universally. The first useful falsifier is a three-hairpin determinant with quotient phase holonomy; if phases are coboundaries, the remaining task is real modulus PSD for all principal minors. The branch has therefore moved from topology naming to a concrete boundary OPE computation program.

## Next Experiment

Compute the leading boundary OPE for three reflected Wilson hairpin collars with a shared reflection-plane footprint. Extract \widehat B, \widehat N, the quotient holonomy \Phi, and det(\widehat N\oslash\widehat B). A negative determinant is the next falsifier; zero holonomy plus positive modulus minors would support promotion to a finite-family same-theory OS bridge.
