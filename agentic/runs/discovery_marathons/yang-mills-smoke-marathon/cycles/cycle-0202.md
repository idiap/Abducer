# cycle-0202

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

Let N(F) be the collar-limit OS matrix for a finite locked Wilson family F and let B(F) be the multiplicative boundary Gram anomaly produced by reflected collar collapse, with nonzero entries. The intended same-theory OS matrix is M(F)=B(F)^{[-1]}\circ N(F). A sufficient finite-matrix bridge is: after normalizing diagonals, the quotient phase of Q_{ij}=N_{ij}/B_{ij} is a coboundary and the quotient modulus matrix |Q| is positive semidefinite on every realized family. Then M(F) is positive, so collar reflection positivity transfers to the intended OS form. Conversely, a nontrivial triangle quotient phase or a modulus quotient with a negative principal minor is a concrete falsifier of the bridge.

## Definitions

- source object: regulated reflection-positive cutoff Schwinger forms on the locked gauge-invariant Wilson collar algebra, together with their continuum collar-limit finite OS matrices N_{ij}=\lim_{\delta\downarrow0}\lim_{a,L}S_{a,L}(\Theta F_{i,\delta},F_{j,delta}).
- target object: the intended continuum OS-positive Schwinger functions on the same gauge-invariant observable algebra after collars are removed, represented on finite families by M_{ij}=S(\Theta F_i,F_j).
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions, mediated by finite reflected Wilson OS matrices and the Hadamard correction M=B^{[-1]}\circ N when boundary collar collapse has a multiplicative anomaly B.
- same-theory condition: the collar-removal map may only introduce diagonal congruences or removable phase coboundaries already fixed by the observable renormalization; any non-coboundary quotient phase, negative quotient modulus minor, additive boundary contact, or algebra enlargement changes the theory rather than proving OS positivity for the intended Yang-Mills Schwinger functions.
- A normalized quotient is q_{ij}=M_{ij}/\sqrt{M_{ii}M_{jj}}=(N_{ij}/B_{ij})/\sqrt{(N_{ii}/B_{ii})(N_{jj}/B_{jj})}, whenever the diagonal entries are positive.
- The triangle quotient holonomy is H_{ijk}=\arg(q_{ij}q_{jk}\overline{q_{ik}}); it vanishes modulo 2\pi for all triples exactly when the finite quotient phase can be removed by a diagonal unitary congruence on that connected component.

## Assumptions

- For each cutoff and collar width, the regulated Wilson OS matrix is positive: N_{a,L,delta}\ge0.
- The RG/cutoff-removal topology is valid for every fixed-collar reflected Wilson probe, so N_\delta\to N entrywise for each finite family.
- The boundary anomaly B has nonzero diagonal entries and represents only the multiplicative part of collar collapse after positive additive contacts have been ruled out by diagonal trace continuity.
- The finite Wilson family is realized inside the locked gauge-invariant algebra; no new boundary observables are added to manufacture positivity.
- The quotient phase is cycle-trivial on the realized finite family, and the remaining modulus quotient matrix is positive semidefinite.

## Equations

- collar OS positivity: `N_{a,L,\delta}(F)_{ij}=S_{a,L}(\Theta F_{i,\delta},F_{j,\delta})\ge 0\quad\Longrightarrow\quad N(F)\ge0`. Valid when: Reflection positivity holds at the regulated level and fixed-collar reflected Wilson probes converge entrywise in the RG topology.
- same-theory Schur preimage: `M(F)=B(F)^{[-1]}\circ N(F),\qquad M_{ij}=\frac{N_{ij}}{B_{ij}}`. Valid when: The only collar-collapse discrepancy between the collar limit and the intended observable is a nonzero multiplicative boundary Gram factor B on the same finite Wilson family.
- three-point determinant obstruction: `\det \widehat M=1+2\operatorname{Re}(q_{12}q_{23}\overline{q_{13}})-|q_{12}|^2-|q_{23}|^2-|q_{13}|^2`. Valid when: \widehat M is the 3 by 3 diagonal-normalized intended OS matrix with unit diagonal and q_{ij}=\widehat M_{ij}; positivity requires this determinant and all principal minors to be nonnegative.
- phase coboundary criterion: `\arg q_{ij}=\alpha_i-\alpha_j\ \forall i,j\quad\Longleftrightarrow\quad \arg(q_{ij}q_{jk}\overline{q_{ik}})=0\ \forall i,j,k`. Valid when: All q_{ij} are nonzero on a connected finite family; zero entries are treated componentwise by restricting to the nonzero support graph.

## Attempted Derivation

- Start with fixed collar observables F_{i,\delta}. Regulated reflection positivity gives N_{a,L,\delta}\ge0 for every finite coefficient vector c.
- Use the assumed RG topology on reflected probes to pass a,L to the collar continuum limit, producing N_\delta\ge0; then take \delta\downarrow0 in entries controlled by the Wilson boundary OPE to obtain a positive collar-limit matrix N.
- Represent the discrepancy between the positive collar-limit matrix and the intended same-theory target matrix by a boundary factor B: N=B\circ M, hence M=B^{[-1]}\circ N. This is the point where the proof is no longer a formal closed-cone argument.
- Normalize M to unit diagonal. Pairwise positivity gives |q_{ij}|\le1, but cycle 201 showed this is incomplete because the 3 by 3 determinant also depends on the phase of q_{12}q_{23}\overline{q_{13}}.
- If the quotient phase is a coboundary, conjugating by a diagonal unitary removes it without changing positivity. The remaining matrix has entries |q_{ij}|, so positivity reduces to a real modulus quotient condition on every realized finite Wilson family.
- For triples, the necessary and sufficient normalized determinant condition becomes 1+2|q_{12}q_{23}q_{13}|-|q_{12}|^2-|q_{23}|^2-|q_{13}|^2\ge0 after phase removal; without phase removal the cosine term can make the determinant negative even when all 2 by 2 minors are nonnegative.

Blocking gap: The derivation has not proved that Yang-Mills reflected Wilson hairpin boundary OPEs have cycle-trivial quotient phase or positive modulus quotient on the realized Wilson cone. That is a genuine analytic boundary estimate, not a consequence of reflection positivity alone.

## Falsifiers

- A three-hairpin Wilson family with pairwise |q_{ij}|\le1 but H_{123}\ne0 large enough that det(B^{[-1]}\circ N)<0 is a phase falsifier of same-theory OS positivity.
- A finite Wilson family with cycle-trivial quotient phase but a negative principal minor of the modulus quotient matrix |B^{[-1]}\circ N| falsifies the modulus half of the bridge.
- A nonzero additive boundary contact with zero diagonal would contradict the positive-contact vanishing argument; if such a contact appears, the assumed boundary OPE positivity is invalid.
- A collar limit that requires adding boundary Wilson observables, changing loop renormalization at t=0, or quotienting by a new boundary Hilbert sector fails the same-theory condition even if the modified matrix remains positive.
- If the RG convergence topology controls ordinary Wilson loops but not mixed reflected products \Theta F_i\,F_j, then the closed-cone passage is not valid for the OS quadratic forms actually needed.

## Learning

Cycle 202 learned that the next bridge is not just finite Schur-preimage positivity in one block. It decomposes into a phase problem and a modulus problem. The phase problem is cohomological on each finite Wilson support graph: zero triangle holonomy makes the quotient phases removable by diagonal unitary congruence, while a nonzero triangle holonomy is the first phase falsifier. After that removal, the remaining obstruction is a real positive-semidefinite modulus quotient. This gives a sharper and more operational Yang-Mills target: compute the reflected Wilson boundary OPE for triples, extract quotient holonomy and modulus minors, and test whether the intended same-theory OS matrix is positive.

## Next Experiment

Compute a symbolic 3 by 3 reflected Wilson hairpin model: parameterize B_{ij}=r^B_{ij}e^{i\phi^B_{ij}} and N_{ij}=r^N_{ij}e^{i\phi^N_{ij}}, form q_{ij}=N_{ij}/B_{ij}, and search for a realized-looking regime where every 2 by 2 minor is nonnegative but the triangle determinant is negative. Then map each parameter to a boundary OPE coefficient that Yang-Mills estimates would need to bound or eliminate.
