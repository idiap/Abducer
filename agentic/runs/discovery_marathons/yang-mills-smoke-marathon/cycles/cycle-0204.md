# cycle-0204

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

Finite Wilson OS positivity after collar removal is valid if the boundary OPE quotient matrix has trivial phase holonomy and positive real modulus quotient on every realized locked Wilson family. More precisely, let N be the positive collar-limit OS matrix and suppose the same-theory boundary factorization N_{ij}=B_{ij}M_{ij} holds with B_{ij}\ne0. The intended OS matrix M is positive exactly when B^{[-1]}\circ N is positive; this can be tested by first removing quotient phases when their cycle holonomy vanishes, then checking PSD of the remaining real modulus quotient. A nonzero triangle holonomy or a negative real quotient minor is a concrete falsifier of the same-theory bridge.

## Definitions

- source object: finite families of regulated gauge-invariant Wilson collar observables T_\delta F_i whose fixed-collar Schwinger matrices N^\delta_{ij}=S(\Theta T_\delta F_i,T_\delta F_j) have OS-positive limits N.
- target object: the intended continuum OS matrix M_{ij}=S(\Theta F_i,F_j) on the locked gauge-invariant Wilson test algebra, before adding boundary counterterms or changing loop renormalization at the reflection plane.
- controlled interface: a boundary OPE factorization N=B\circ M with nonzero Hermitian boundary factor B, together with the Schur-preimage test M=B^{[-1]}\circ N on each finite realized Wilson support graph.
- same-theory condition: B must be a removable collar artifact for the same locked observables; if removing B requires enlarging the algebra, changing Wilson-loop normalization at t=0, or adding a boundary Hilbert sector, the bridge is not a proof for the original Yang-Mills theory.

## Assumptions

- Fixed-collar RG convergence is strong enough to pass every reflected Wilson OS matrix entry to a limit N_{ij}.
- The boundary collision of reflected Wilson collars admits a multiplicative leading factor B_{ij} with no zero entries on the finite support being tested, after diagonal one-body renormalizations already included in the locked observable definition.
- Additive positive contact terms have zero diagonal after diagonal trace continuity and hence vanish by Cauchy-Schwarz; any surviving additive term is treated as a separate falsifier.
- The realized Wilson cone is not assumed to be all PSD matrices; all positivity tests are only claimed for matrices actually produced by locked Wilson observables.

## Equations

- collar-positive source matrix: `N_{ij}=\lim_{\delta\downarrow0}S(\Theta T_\delta F_i,T_\delta F_j),\qquad N\succeq0`. Valid when: The cutoff-removal topology controls the fixed-collar reflected Wilson probes and the regulated OS cone is closed for these finite forms.
- same-theory Schur preimage: `N=B\circ M,\qquad M=B^{[-1]}\circ N,\qquad (B^{[-1]})_{ij}=1/B_{ij}`. Valid when: The boundary OPE produces only a multiplicative nonzero collar factor B and no additional boundary observable or counterterm.
- quotient phase holonomy: `\Phi_{ijk}=\arg\!\left(\frac{N_{ij}N_{jk}\overline{N_{ik}}}{B_{ij}B_{jk}\overline{B_{ik}}}\right)`. Valid when: The three matrix entries are nonzero; \Phi_{ijk}=0\mod 2\pi for all triangles is the local cycle test for quotient phases to be removable by diagonal unitary congruence on a complete support graph.
- three-hairpin determinant test: `\det M_{\{1,2,3\}}=M_{11}M_{22}M_{33}\left(1+2r_{12}r_{23}r_{13}\cos\Phi_{123}-r_{12}^2-r_{23}^2-r_{13}^2\right)`. Valid when: The 3 by 3 target matrix is normalized by positive diagonal entries and r_{ij}=|M_{ij}|/\sqrt{M_{ii}M_{jj}}=|N_{ij}/B_{ij}|/\sqrt{M_{ii}M_{jj}}.

## Attempted Derivation

- Start from regulated reflection positivity: for every finite collar family, Q_{a,L}(T_\delta F,c)\ge0. RG convergence of fixed-collar reflected probes gives N^\delta\to N entrywise, hence N\succeq0 by closedness of the finite PSD cone.
- The target OS form is not N if collar collapse contributes a boundary factor. Under the multiplicative boundary OPE N=B\circ M, the same-theory target is M=B^{[-1]}\circ N. Therefore the closed-cone lemma proves positivity of N, but the missing bridge is positivity of this Schur preimage M.
- Normalize to positive diagonal and write M_{ij}=r_{ij}e^{i\theta_{ij}}. A diagonal unitary U changes phases by \theta_{ij}\mapsto\theta_{ij}+u_j-u_i, so phases are removable exactly when their cycle sums vanish. On triples this invariant is \Phi_{ijk}=\theta_{ij}+\theta_{jk}-\theta_{ik}.
- After quotient phases are removed, the test reduces to the real symmetric matrix R with R_{ii}=M_{ii} and R_{ij}=|M_{ij}|. PSD of R is still substantive; pairwise bounds only give 2 by 2 minors. The first non-pairwise obstruction is the 3 by 3 determinant formula above.
- Thus the proof route is: prove boundary quotient holonomy vanishes for reflected Wilson triples, then prove the real modulus quotient is PSD on every realized finite Wilson family. Conversely, any negative principal minor of B^{[-1]}\circ N is a falsifier even though the collar-limit matrix N remains positive.

Blocking gap: The derivation is finite-dimensional and valid once B and N are supplied, but Yang-Mills analysis has not yet proved that the reflected Wilson boundary OPE yields trivial quotient holonomy or a PSD real modulus quotient on the realized locked Wilson cone.

## Falsifiers

- A three-hairpin Wilson calculation with nonzero quotient phase holonomy and negative normalized determinant, even though every pairwise damping inequality is valid.
- A boundary OPE factor B with zeros on a realized Wilson support edge, making the Schur preimage ill-defined without changing the observable algebra.
- A surviving additive boundary contact with zero diagonal but nonzero off-diagonal, contradicting positive-contact Cauchy-Schwarz and exposing an invalid boundary decomposition.
- A modulus quotient R_{ij}=|N_{ij}/B_{ij}| that passes all 2 by 2 tests but has a negative 4 by 4 or larger principal minor on realized Wilson observables.

## Learning

Cycle 204 sharpened the post-collar obstruction into a two-layer finite invariant test. The closed-cone argument is valid for collar-limit matrices N, but same-theory OS positivity is exactly the positivity of M=B^{[-1]}\circ N. This is not decided by B alone and not by pairwise damping alone. The first genuinely new falsifier is a triangle determinant controlled by quotient phase holonomy; after phases are coboundaries, the remaining modulus quotient must still be PSD on realized Wilson families. The next Yang-Mills work is therefore a boundary OPE computation for reflected Wilson triples and then higher principal minors.

## Next Experiment

Construct a minimal three-hairpin reflected Wilson collar family with common reflection-plane footprint; compute the leading boundary OPE factor B_{ij}, the collar matrix N_{ij}, and the determinant of B^{[-1]}\circ N to see whether quotient holonomy or the real modulus minor supplies the first concrete falsifier.
