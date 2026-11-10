# cycle-0201

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: Three-Hairpin Schur-Preimage Phase Test

## Candidate Lemma

For a locked triple of reflected Wilson collar observables, assume fixed-collar OS positivity has passed to a positive collar-limit matrix N and collar collapse has only a multiplicative boundary hairpin defect B, with additive contacts already ruled out. Then same-theory OS positivity for the intended continuum boundary matrix M is equivalent, for this triple, to positivity of the Hadamard quotient M=B^{[-1]}\circ N. After normalization, the first phase-sensitive obstruction is the determinant inequality 1-r_{12}^2-r_{23}^2-r_{13}^2+2r_{12}r_{23}r_{13}\cos(\Phi_N-\Phi_B)\ge0. Thus a realized Wilson triple with pairwise valid thresholds but negative triangle determinant is a concrete falsifier of the bridge.

## Definitions

- source object: a finite locked gauge-invariant Wilson collar family F_i^\delta supported in t>\delta, with regulated reflection-positive Schwinger matrices converging to a positive collar-limit OS matrix N.
- target object: the intended continuum OS matrix M_{ij}=S(\Theta F_i,F_j) on the same Wilson observables after the collar is collapsed to the reflection plane.
- controlled interface: the boundary OPE comparison map N_{ij}=B_{ij}M_{ij} and hence M=B^{[-1]}\circ N, tested on every realized finite Wilson OS matrix rather than on the full cone of all positive matrices.
- same-theory condition: the observables F_i^\delta converge to the locked F_i without changing Wilson-loop renormalization, adding a boundary counterterm, enlarging the algebra, or replacing M by a boundary-renormalized theory.

## Assumptions

- Diagonal trace continuity is already valid: N_{ii}=B_{ii}M_{ii} with finite positive diagonal entries and no hidden diagonal boundary loss.
- Additive contact terms vanish or have been independently proved zero on this triple; otherwise the multiplicative quotient model is not valid.
- The boundary defect matrix B is Hermitian with nonzero tested entries and is computed from the same reflected hairpin geometry that appears in the collar collapse.
- N is a realized collar-limit OS Gram matrix for actual Yang-Mills Wilson observables, not an arbitrary positive matrix inserted for a universal Schur-multiplier argument.

## Equations

- multiplicative boundary quotient: `N_{ij}=\lim_{\delta\downarrow0}S(\Theta F_i^\delta,F_j^\delta)=B_{ij}M_{ij},\qquad M=B^{[-1]}\circ N`. Valid when: The collar collapse has no additive contact term, B_{ij}\neq0 on the tested entries, and the same locked Wilson observable is used before and after the limit.
- normalized three by three OS determinant: `\det \widehat M=1-|q_{12}|^2-|q_{23}|^2-|q_{13}|^2+2\operatorname{Re}(q_{12}q_{23}\overline{q_{13}})\ge0`. Valid when: The diagonal entries of M are positive and \widehat M_{ij}=q_{ij}=M_{ij}/\sqrt{M_{ii}M_{jj}} is the normalized intended OS matrix for three observables.
- triangle phase obstruction: `q_{ij}=n_{ij}/b_{ij},\quad r_{ij}=|n_{ij}|/|b_{ij}|,\quad \Phi=\arg(n_{12}n_{23}\overline{n_{13}})-\arg(b_{12}b_{23}\overline{b_{13}})`. Valid when: The normalized collar entries n_{ij} and boundary entries b_{ij} are nonzero; then \det\widehat M=1-\sum r_{ij}^2+2r_{12}r_{23}r_{13}\cos\Phi.

## Attempted Derivation

- Start with fixed collar observables F_i^\delta. Regulated reflection positivity gives Q_{a,L}\ge0; RG convergence in the reflected-probe topology gives a positive collar-limit Gram matrix N for each finite family.
- Collapse the collar. If diagonal trace continuity is valid and additive boundary contacts vanish, the only remaining defect in a reflected Wilson product is multiplicative: N_{ij}=B_{ij}M_{ij}.
- The same-theory target is not N and not a boundary-renormalized replacement; it is M=B^{[-1]}\circ N on the locked Wilson algebra.
- For two observables, positivity of M gives the known threshold |n_{12}|/|b_{12}|\le1, so pairwise tests only control 2 by 2 minors.
- For three observables, normalize M to diagonal one. The determinant expands exactly as 1-|q_{12}|^2-|q_{23}|^2-|q_{13}|^2+2 Re(q_{12}q_{23}\overline{q_{13}}).
- Writing q_{ij}=n_{ij}/b_{ij} isolates the new invariant: the determinant depends on the phase difference between the collar triangle n_{12}n_{23}\overline{n_{13}} and the boundary defect triangle b_{12}b_{23}\overline{b_{13}}.
- If all quotient cycle phases vanish on a finite family, a diagonal unitary removes the phases and the problem reduces to modulus quotient positivity. If a triangle phase remains, it is the first phase-sensitive falsifier candidate.

Blocking gap: The finite matrix derivation is valid, but it does not compute the actual Yang-Mills boundary hairpin defect B or the realized collar matrix N. The missing analytic input is a boundary OPE or multiscale estimate for three reflected Wilson hairpins that proves N=B\circ M with zero additive contact and then controls the quotient determinant.

## Falsifiers

- A realized three-hairpin Wilson family with |n_{ij}|\le |b_{ij}| for every pair but det(B^{[-1]}\circ N)<0 is the sharp phase falsifier for this cycle.
- A boundary entry B_{ij}=0 with N_{ij}\ne0 makes the Hadamard preimage singular and invalidates the same-theory quotient map.
- A nonzero additive boundary contact that is not forced to vanish by diagonal trace continuity breaks the multiplicative anomaly model before the phase test is even reached.
- A quotient cycle phase that cannot be written as a diagonal unitary coboundary gives a valid obstruction unless the realized modulus matrix still keeps every finite determinant nonnegative.
- If the locked Wilson algebra cannot realize triples rich enough to test the boundary covariance, then nontrivial B is not yet a falsifier; the branch would need a stronger density theorem rather than a determinant example.

## Learning

Cycle 201 sharpened the obstruction from pairwise damping to finite quotient holonomy. The closed-cone step is still valid for collar matrices N, but same-theory OS positivity depends on whether the Hadamard preimage B^{[-1]}\circ N is positive on realized Wilson families. The first genuinely new falsifier is a three-hairpin triangle whose quotient phase makes the normalized determinant negative. Conversely, if quotient phases are cycle-trivial, they are removable by diagonal unitary congruence, so the next proof route separates into phase-coboundary control plus modulus quotient positivity.

## Next Experiment

Compute the leading boundary OPE for three reflected Wilson hairpins with a common reflection-plane footprint. Extract B_{12}, B_{23}, B_{13} and the collar triangle N_{12}N_{23}\overline{N_{13}}, then evaluate the normalized determinant of B^{[-1]}\circ N to see whether the first phase-sensitive falsifier is realized.
