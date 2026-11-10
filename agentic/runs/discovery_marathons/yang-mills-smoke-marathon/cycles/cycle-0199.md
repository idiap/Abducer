# cycle-0199

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

For a finite triple of locked gauge-invariant Wilson collar observables, fixed-collar reflection positivity transfers to the intended zero-collar Schwinger functions only if the boundary-defect Schur preimage is positive. After diagonal one-body factors are absorbed, this gives an explicit three-by-three determinant test; pairwise damping inequalities are necessary but not sufficient because a boundary phase/cross-ratio can make the intended OS matrix indefinite.

## Definitions

- source object: normalized collar-limit OS matrices N=(N_{ij}) obtained from reflected Wilson observables W_i^delta with supports in t>delta, after taking delta down to 0 along a cutoff-removal/RG limit for which each fixed-collar quadratic form is valid.
- target object: the intended continuum OS matrix M=(M_{ij}) for the same locked Wilson observables evaluated at the reflection-plane trace, with no added boundary sector, boundary counterterm, or algebra change.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions, mediated by finite reflected Wilson matrices and their boundary-defect Schur preimages.
- same-theory condition: every boundary factor must be removable only by locked observable renormalizations already present in the target theory, so the target matrix is M=B^{[-1]}\circ N and must be positive on the realized Wilson cone, not merely on a boundary-renormalized enlarged theory.

## Assumptions

- The cutoff-removal topology controls every finite reflected Wilson collar matrix entry N^delta_{ij}=S(Theta W_i^delta,W_j^delta).
- For the chosen triple, diagonal trace continuity has removed additive positive contact terms; any remaining boundary effect is multiplicative, Hermitian, and has nonzero entries B_{ij}.
- The Wilson observables are normalized so N_{ii}=B_{ii}=1 after absorbing valid one-body factors into the locked observable normalization.
- The same finite family is used before and after the collar trace; no gauge fixing, quotient, boundary extension, or change of test algebra is allowed.

## Equations

- collar positivity: `N^\delta_{ij}=S(\Theta W_i^\delta,W_j^\delta),\qquad \sum_{i,j}\overline c_i c_j N^\delta_{ij}\ge 0`. Valid when: The regulated lattice/RG construction is reflection-positive for the gauge-invariant collar observables at fixed positive distance from the reflection plane.
- closed collar limit: `N^\delta\to N\quad\Longrightarrow\quad N\ge 0`. Valid when: The cutoff-removal topology gives entrywise convergence for the finite reflected collar matrix.
- same-theory Schur preimage: `M_{ij}=B_{ij}^{-1}N_{ij},\qquad M=B^{[-1]}\circ N`. Valid when: The zero-collar trace creates only a multiplicative boundary factor B and all diagonal one-body renormalizations have been locked into the same observable normalization.
- normalized three-observable determinant: `\det M=1+2\operatorname{Re}\!\left({N_{12}N_{23}\overline{N_{13}}\over B_{12}B_{23}\overline{B_{13}}}\right)-\left|{N_{12}\over B_{12}}\right|^2-\left|{N_{23}\over B_{23}}\right|^2-\left|{N_{13}\over B_{13}}\right|^2\ge 0`. Valid when: M is a normalized 3 by 3 Hermitian OS correlation matrix for the intended same-theory observables.

## Attempted Derivation

- Start with fixed-collar Wilson observables W_i^delta supported in positive Euclidean time. Regulated reflection positivity gives N^delta>=0 for every finite family.
- Use the cutoff-removal topology only for those reflected finite matrix entries. Entrywise convergence N^delta -> N places N in the closed positive cone, so the collar-limit matrix is positive.
- Let the collar trace delta down to 0. Diagonal trace continuity rules out positive additive contacts: if the additive contact matrix A is positive and A_{ii}=0 for all i, then Cauchy-Schwarz gives A_{ij}=0.
- Model the remaining boundary effect as a multiplicative Hermitian factor B_{ij}; after absorbing one-body factors, the same-theory target matrix is M_{ij}=N_{ij}/B_{ij}.
- For two observables, M>=0 is just |N_{12}|<=|B_{12}| after normalization. This recovers the previous damping threshold but shows it is only a minor condition.
- For three observables, positivity requires the determinant formula involving the phase-sensitive product N_{12}N_{23}overline{N_{13}}/(B_{12}B_{23}overline{B_{13}}). Thus a boundary cross-ratio phase can be a falsifier even if every two-by-two test is valid.

Blocking gap: The derivation assumes a well-defined multiplicative boundary factor B for reflected Wilson collar collapse and lacks a Yang-Mills estimate or OPE computation showing what B and N are for actual hairpin triples.

## Falsifiers

- A concrete three-hairpin Wilson family with pairwise ratios |N_{ij}/B_{ij}|<=1 but det(B^{[-1]} circ N)<0; this is the cleanest phase-sensitive falsifier of the same-theory bridge.
- A nonzero additive boundary contact matrix with zero diagonal but nonzero off-diagonal entries; this would falsify the assumed positive-contact compatibility because a positive matrix with zero diagonal cannot have such entries.
- A boundary factor B with some B_{ij}=0 while the corresponding collar correlation N_{ij} is nonzero, making the intended Schur preimage undefined or divergent.
- An RG compactness topology that controls fixed-collar Wilson entries but not the joint triple limit needed for the determinant test.
- A proof of positivity only for the boundary-renormalized matrix N, with no valid argument that M=B^{[-1]} circ N is positive for the locked target observables.

## Learning

Cycle 199 identifies the first genuinely phase-sensitive falsifier. The pairwise threshold rho_N<=|B_ij| is valid but incomplete: OS positivity for the same theory requires every finite Schur preimage B^{[-1]} circ N to be positive. For triples this becomes an explicit determinant with a boundary cross-ratio phase. The branch therefore learned that the next useful calculation is not another closed-cone restatement, but a three-hairpin Wilson boundary OPE computation or bound.

## Next Experiment

Construct an explicit symbolic three-hairpin test family: normalize B and N, parameterize the boundary cross-ratio phase phi_B=arg(B12 B23 overline{B13}), and determine whether locality or reflection symmetry forces phi_N-phi_B into the determinant-positive region. If not, use the resulting determinant inequality as the next concrete Yang-Mills falsifier target.
