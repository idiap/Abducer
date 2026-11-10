# cycle-0203

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

For a finite locked Wilson collar family, same-theory OS positivity across the reflection plane is equivalent to positivity of the Hadamard quotient matrix after removing only a diagonal phase coboundary. The phase obstruction is the triangle holonomy; the remaining modulus obstruction is an ordinary real Gram-quotient determinant problem on the realized Wilson cone, not on all positive matrices.

## Definitions

- source object: fixed-collar reflected Wilson OS matrices N^{\delta}_{ij}=S(\Theta W_i^\delta,W_j^\delta) with N=\lim_{\delta\downarrow0}N^\delta\ge0 by the valid closed-cone passage.
- target object: intended continuum Wilson OS matrix M_{ij}=S(\Theta W_i,W_j) in the locked gauge-invariant test algebra, before adding boundary counterterms or renormalized reflection-plane observables.
- controlled interface: multiplicative boundary anomaly B_{ij}\ne0 satisfying N_{ij}=B_{ij}M_{ij}+o(1) for every finite reflected Wilson pairing; hence M=B^{[-1]}\circ N if additive contacts vanish.
- same-theory condition: B may be absorbed only by a diagonal nonzero congruence already fixed in the observable normalization; any non-coboundary phase or non-PSD realized quotient is a falsifier for this bridge, even if a modified boundary theory remains positive.
- normalized quotient q_{ij}=N_{ij}/B_{ij} with q_{ii}=1 after diagonal normalization.
- triangle quotient holonomy H_{ijk}=\arg(q_{ij}q_{jk}\overline{q_{ik}}), invariant under diagonal unitary changes of Wilson representatives.

## Assumptions

- The collar limit topology controls every finite reflected Wilson matrix entry N_{ij}.
- Diagonal trace continuity holds, so positive additive boundary contacts vanish by zero diagonal plus Cauchy-Schwarz.
- B_{ij} is nonzero on the tested finite support graph and is the full multiplicative boundary anomaly for mixed reflected Wilson products.
- The locked Wilson observables are the same before and after collar removal; no boundary-local observable is silently added.

## Equations

- multiplicative trace quotient: `N_{ij}=B_{ij}M_{ij},\qquad M=B^{[-1]}\circ N`. Valid when: Valid only after additive contacts are ruled out and B is computed in the same Wilson normalization used to define the target continuum Schwinger functions.
- phase coboundary criterion: `\exists u_i\in U(1):\ \arg q_{ij}=\arg u_i-\arg u_j\quad\Longleftrightarrow\quad H_{ijk}=0\ \text{for every triangle }(i,j,k)`. Valid when: Valid on each connected finite support graph with nonzero q_{ij}; for sparse graphs the condition is imposed on every cycle, not only literal geometric triangles.
- post-phase modulus determinant: `\det M_{I}\ge0\quad\text{for all finite }I,\qquad M_{ij}=|N_{ij}|/|B_{ij}|\ \text{after phase removal}`. Valid when: Valid as the remaining OS test exactly when quotient phases have been gauged away by diagonal unitary congruence.

## Attempted Derivation

- Start with fixed collar observables W_i^\delta supported in t>\delta. Regulated reflection positivity and RG convergence give N^\delta\to N with N\ge0; this step is valid by the closed cone in the topology of finite reflected OS forms.
- Use the boundary trace ansatz N_{ij}=B_{ij}M_{ij}+A_{ij}. Diagonal trace continuity gives A_{ii}=0; if A is a positive contact matrix, Cauchy-Schwarz implies A=0, so the remaining bridge is M=B^{[-1]}\circ N.
- Normalize diagonals and set q_{ij}=N_{ij}/B_{ij}. Diagonal unitary congruence can change edge phases but cannot change cycle holonomy H_C=\arg\prod_{(ij)\in C}q_{ij}; therefore nonzero holonomy is an immediate phase falsifier for same-theory OS positivity.
- If all quotient holonomies vanish, choose phases u_i so u_i^*M_{ij}u_j is real nonnegative. The remaining question is whether the modulus quotient matrix |N_{ij}|/|B_{ij}| is PSD on every realized finite Wilson family.
- Local boundary OPE then predicts |B_{ij}| through a connected footprint kernel. If its log cross-ratios vanish, the modulus factor is just diagonal congruence and the bridge promotes; if not, one must test actual finite determinants of B^{[-1]}\circ N.

Blocking gap: The missing Yang-Mills estimate is a controlled computation or bound of the reflected Wilson boundary OPE for triples and quadruples: enough to prove zero quotient holonomy plus PSD modulus quotient, or to exhibit a determinant falsifier. Current RG compactness does not yet control the boundary anomaly B with phase and modulus resolution.

## Falsifiers

- A three-hairpin Wilson family with nonzero quotient cycle holonomy H_{123}; this is a phase falsifier even if every two-by-two minor is valid.
- A phase-trivial triple with det(|N_{ij}|/|B_{ij}|)<0 after diagonal normalization.
- A nonzero connected boundary OPE kernel C_\partial for coincident reflection-plane footprints that creates K_{ij;k\ell}\ne0 and is detected by realized collar correlations.
- A proof of reflection positivity only for an enlarged algebra containing boundary Wilson counterterms, not for the locked same-theory gauge-invariant algebra.

## Learning

Cycle 203 learned that the post-collar obstruction has a clean two-stage finite-matrix form: first remove quotient phases exactly when cycle holonomy vanishes; then test the real modulus quotient for PSD on realized Wilson families. This avoids the earlier overclaim that B alone decides failure. A nonzero boundary Gram anomaly is a falsifier only when its phase holonomy or modulus minors are detected by the locked Wilson OS matrices; otherwise it may be invisible to the realized cone.

## Next Experiment

Compute the reflected boundary OPE for the simplest three Wilson hairpins with one shared reflection-plane footprint: extract B_{ij}, form q_{ij}=N_{ij}/B_{ij}, test H_{123}, then test det(|N_{ij}|/|B_{ij}|).
