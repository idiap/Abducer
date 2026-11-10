# cycle-0335

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint source-interval quarantine for finite post-H,K Wilson OS gate

## Candidate Lemma

For the fixed post-H,K three-hairpin Wilson block, the valid same-theory endpoint carrier is an affine interval product over source-equivalent endpoint classes; it may promote, falsify, or quarantine only this finite OS scalar.

## Definitions

- source object: heat-kernel plaquette-sheet SU(N) endpoint boxes with regulated Wilson source partition functions Z_c(s) for each source-equivalence class c.
- target object: the finite post-H,K reflected-Wilson OS transfer scalar I_gate for the locked three-hairpin block, not the continuum Yang-Mills theory.
- controlled interface: C_ep={source classes, seven source values, kappa intervals, signed incidences D_c, color factor C_N, Gaussian margin M_G, tail T_tail} exported as one scalar interval.
- same-theory condition: all Z_c(s) are evaluated in the same regulated gauge-invariant Wilson theory, with no boundary counterterm, no changed Wilson normalization, and no enlarged endpoint algebra.
- endpoint source class: two endpoint boxes are equivalent only when their seven regulated source values and incidence data agree within certified cutoff intervals.
- connected cumulant witness: kappa_c is the fourth source derivative of log Z_c, so Wick-square disconnected pieces are removed before incidence contraction.

## Assumptions

- Model: four-dimensional lattice SU(N) Yang-Mills with heat-kernel plaquette action and reflected Wilson hairpin collars already reduced through the finite H,K Schur-Feshbach gate.
- Regime: fixed finite Wilson block and fixed endpoint boxes at positive cutoff a; no continuum limit or mass-gap assertion is used.
- Cutoff: stencil errors and T_tail are bounded uniformly over the endpoint boxes selected for this block.
- Same-theory: the source insertion differentiates the original Wilson observable family and does not introduce a boundary Hilbert sector or boundary OPE counterterm.
- Validity: aggregation is performed over source-equivalent endpoint classes before any sign clipping or root-quartic screening.
- Constraint: the local claim changes only the finite post-H,K reflected-Wilson OS gate; continuum existence, observable density, OS spectral transfer, and positive mass gap remain untouched.

## Equations

- seven point connected cumulant witness: `\kappa_c=D_h^{(4)}\log Z_c(0)+\varepsilon_c,\quad D_h^{(4)}f(0)=h^{-4}\sum_{r=-3}^{3}w_r f(rh),\quad |\varepsilon_c|\le 7h^4 M_{8,c}/240`. Valid when: Valid when the endpoint source path is analytic in a heat-kernel coordinate chart and the eighth source derivative is uniformly bounded on the seven-point stencil.
- signed endpoint incidence: `D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}`. Valid when: Valid when the previous H,K Feshbach null vector and Wilson endpoint incidences are fixed for this three-hairpin block.
- affine interval transfer scalar: `I_{gate}\in M_G+C_N\sum_c [D_c^-,D_c^+]\boxtimes[\kappa_c^-,\kappa_c^+]+[-T_{tail},T_{tail}]`. Valid when: Valid when endpoint classes have been aggregated by regulated source equivalence before interval multiplication and the remaining geometry is charged to a uniform tail.
- root quartic screen: `\kappa_c=-\frac{t_c^4}{60}\{N\operatorname{tr}(L_c^4)+3(\operatorname{tr}L_c^2)^2\}+E_c`. Valid when: Applies after diagonal heat-kernel endpoint normalization for sufficiently small endpoint source strength with the Haar-Jacobian remainder E_c bounded in the same cutoff theory.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: heat-kernel plaquette-sheet SU(N) endpoint boxes with regulated Wilson source partition functions Z_c(s) for each source-equivalence class c.; target object: the finite post-H,K reflected-Wilson OS transfer scalar I_gate for the locked three-hairpin block, not the continuum Yang-Mills theory.; Model: four-dimensional lattice SU(N) Yang-Mills with heat-kernel plaquette action and reflected Wilson hairpin collars already reduced through the finite H,K Schur-Feshbach gate..
- Conceptual pressure: endpoint collapse must be sign-certified inside the same Wilson theory after the finite H,K reduction, without adding a boundary theory.
- Declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must jointly hold, but raw R hides incidences and raw kappa_4 spectra ignore the null-channel signs.
- Replace raw R by C_ep, whose primitive operations are source differentiation, interval arithmetic, source-equivalence aggregation, color multiplication, incidence contraction, and tail addition.
- Use log Z_c before differentiating so the connected cumulant witness removes Wick-square disconnected terms; the earlier straight f f term is already killed by null incidence.
- Aggregate endpoint boxes by regulated source data, compute D_c affinely, then multiply D_c by the certified kappa_c interval; do not clip before aggregation.
- Apply the root-quartic heat-kernel expansion only as a conservative screen for possible negative kappa_c in positive-D classes.
- Export the single interval I_gate to the finite OS gate: I_gate>0 promotes this block, I_gate<0 is a finite falsifier, and unresolved source or tail data keeps quarantine.

Blocking gap: No certified same-theory endpoint source intervals and no cutoff-uniform T_tail bound are currently available for the positive-D source classes.

## Falsifiers

- A certified I_gate interval strictly below zero gives a finite same-theory falsifier for the post-H,K reflected-Wilson OS transfer block.
- A required boundary counterterm or changed Wilson normalization violates the same-theory condition even if a modified positive theory exists.
- A nonuniform endpoint tail as a->0 invalidates the transfer from heat-kernel source data to the finite OS scalar.
- Two endpoint boxes declared equivalent by geometry but not by regulated source values break the aggregation theorem.
- Premature clipping of D_v before source-equivalence aggregation can manufacture a false valid promotion certificate.
- A positive-D source class with a large negative connected cumulant witness beyond the root-quartic screen demotes the branch.

## Learning

Cycle 335 should remain quarantined, but the proof state is sharper. The conceptual pressure is endpoint collapse in the same Wilson theory. The hard gate is the finite post-H,K reflected-Wilson OS transfer scalar: success promotes only this fixed block, failure gives a finite same-theory falsifier, and missing source or tail data keeps quarantine. The declarative tension is collar OS positivity plus fixed gauge-invariant Wilson observables plus singular connected endpoint OPE without a boundary theory. Raw R is representation-limited, raw kappa_4 spectra are too strong, and the global Schur-preimage route is valid but too coarse after H,K. The efficient representation is C_ep: source classes, seven source values, cumulant intervals, signed incidences, C_N, M_G, and T_tail; it preserves Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; equivalence is equality of regulated source data; transfer exports only I_gate. Conceptual value signal: sharpness at finite scope. Negative SU(N) endpoint cumulants are explanatory but not the obstruction; positive-D leakage times a connected cumulant witness plus uniform tail is.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe while the proof branch remains quarantined for endpoint source data.`
- Rationale: The branch is looping on promotion language; a target-preserving finite endpoint computation is needed to decide the post-H,K scalar rather than restating the Wilson/OS obstruction ladder.
- Situation seed: In the heat-kernel plaquette-sheet SU(N) regulator, take the fixed three-hairpin endpoint block after H,K and evaluate seven same-theory source values of log Z_c(s) for each source-equivalent endpoint class with fractional incidences b12,b13,b23.
- Varied variable: Vary the fractional endpoint dominance ratio alpha_c=b12,c/(b13,c+b23,c+eta) while keeping the source generator norm and endpoint scale fixed.
- Held-fixed controls: The gauge group SU(N), heat-kernel plaquette regulator, reflected Wilson hairpin geometry, and Feshbach null vector are fixed., The locked gauge-invariant Wilson observable algebra and Wilson normalization are fixed; no boundary counterterm is allowed., The Gaussian margin M_G, color factor C_N, source stencil h, and tail accounting rule T_tail are held fixed., Only source-equivalent endpoint classes may be aggregated, and all disconnected Wick-square pieces are removed by log Z.
- Expected observation: Classes with alpha below the half-overlap shield should be protective or neutral, while a source-certified positive-D class can make I_gate negative only if its connected cumulant witness is sufficiently negative after the uniform tail is added.
- Transfer certificate needed: A cutoff-uniform certificate for the seven-point source derivative intervals, the source-equivalence partition, the signed incidence intervals, and T_tail; without it the observation remains a finite-regulator probe and cannot affect OS proof obligations.

## Next Experiment

Route to proof search plus targeted endpoint source computation: build the C_ep table for positive-D source classes, evaluate the seven-point log Z_c stencil in the same heat-kernel Wilson theory, certify T_tail, and decide whether I_gate is positive, negative, or still quarantined.

# Annular Ward-Hessian R++ endpoint certificate

## Candidate Lemma

Conditional finite theorem: if annular Ward-Hessian intervals give Delta_R^->0, then the same-theory R_{++}^{ren} beats Schur-Feshbach leakage L_+ and proves only finite endpoint-box positivity after H,K.

## Definitions

- source object: finite SU(N) lattice Yang-Mills Wilson action with gradient-flow time t, centered thin H,K endpoint hairpins, and reflected endpoint sheet currents J_+.
- target object: a finite post-H,K Schur-Feshbach endpoint-box margin Delta_R^- proving only local positivity of the plus channel.
- controlled interface: recovery map raw hairpin -> centered flowed sheet current with error E_rec, preserving gauge, color, reflection, orientation, locality.
- same-theory condition: same bare Wilson action, boundary geometry, reflection plane, flow-time window, and cutoff family; no imported continuum theory.
- observable carrier: centered flowed Wilson cumulant kappa_2(W_+,W_+) after disconnected product and one-hairpin cusp/perimeter subtraction.
- representation: endpoint sheet currents encode H,K sheets, cell moments, sector kernels, counterterms, L_+, and recovery errors; zero-pairing quotient only by certificate.

## Assumptions

- Model: finite hypercubic lattice SU(N), Wilson action, gradient flow t>0, finite volume before any continuum discussion.
- Regime: endpoint box size eta, flow radius sqrt(8t) comparable but bounded, a << sqrt(8t) <= c eta; H,K geometry fixed.
- Uniformity: sector Hessian constants and recovery error are bounded uniformly for a/eta in the audited window; no RG basin claim.
- Same-theory: all cumulants use centered flowed Wilson observables recovered from the same raw hairpins; OS spectral transfer is untouched.
- Local: large-field and topology controls are assumed only insofar as they validate finite flowed cumulant intervals; not a Clay-level discharge.

## Equations

- R-decomposition: `R_{++}^{\mathrm{ren}}=g_t^4\{2(N^2-1)G_{++}-N(N^2-1)\sum_s C_s\}-E_{rec}`. Valid when: Valid when the centered flowed hairpin cumulant is expanded after disconnected product and one-hairpin cusp/perimeter subtractions.
- annular-C4-bound: `C_s\le A_s^{near}+B_s^{far}\,q_s^{J_0}/(1-q_s),\quad q_s=2^{4-2\nu_s}<1`. Valid when: Applies when Ward and plus-moment cancellation reduce sector s to a mixed-Hessian kernel with decay exponent nu_s greater than two.
- promotion-margin: `\Delta_R^-:=g_t^4[2(N^2-1)G_{++}^- -N(N^2-1)\sum_s C_s^+]-E_{rec}^+-L_+`. Valid when: Requires the same H,K Schur-Feshbach leakage L_+ and all interval bounds to use identical endpoint cells and normalization.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: finite SU(N) lattice Yang-Mills Wilson action with gradient-flow time t, centered thin H,K endpoint hairpins, and reflected endpoint sheet currents J_+.; target object: a finite post-H,K Schur-Feshbach endpoint-box margin Delta_R^- proving only local positivity of the plus channel.; Model: finite hypercubic lattice SU(N), Wilson action, gradient flow t>0, finite volume before any continuum discussion..
- Replace raw thin hairpins by centered flowed endpoint sheet currents via the recovery map; subtract disconnected product and one-hairpin cusp/perimeter counterterms.
- Evaluate the pair contraction: two cross-pairings give the positive baseline 2(N^2-1)G_{++}, with gauge and reflection invariants preserved.
- Use Ward identity plus plus-channel monopole/dipole cancellation to make connected C4 controlled by mixed Hessians of flowed four-curvature sector kernels.
- Split endpoint separations into near cells and dyadic annuli; interval-bound near cells, sum far tails with q_s=2^{4-2nu_s}, then compare Delta_R^- to zero.

Blocking gap: Certified outward-rounded intervals for A_s^{near}, B_s^{far}, G_{++}^-, E_rec^+, and the zero-pairing quotient are not yet computed.

## Falsifiers

- falsifier: Ward or cusp subtraction mismatch leaves an O(eta^0) monopole/dipole C4 term larger than the pair baseline.
- falsifier: annular decay exponent nu_s<=2, so q_s>=1 and the far connected polarization is not summable.
- falsifier: the recovery map from raw hairpins to flowed sheet currents is not same-theory or has E_rec^+ >= positive margin.
- falsifier: a cutoff or flow-radius plateau test makes Delta_R^- change sign or fail to dominate L_+.

## Learning

Pressure: finite Feshbach positivity needs a same-theory Wilson mediator. Tension: pair covariance, recovery, and endpoint positivity can each be valid while C4 erases R. Value: R_{++} is now a route-deciding annular interval, not a symbolic boundary-OPE term.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch needs a concrete plateau test because abstract positivity is already exhausted; only a cutoff-stable R_{++} interval can promote or quarantine the finite endpoint gate.
- Situation seed: SU(N) Wilson lattice with fixed H,K endpoint hairpin sheets, gradient-flow regulator, centered Wilson cumulant kappa_2(W_+,W_+), and annular sector quadrature for C4.
- Varied variable: rho=sqrt(8t)/eta, the flow-radius to endpoint-box ratio.
- Held-fixed controls: same bare Wilson action, N, finite H,K geometry, reflection plane, and endpoint cell partition, same cusp/perimeter counterterms, recovery map, zero-pairing quotient policy, and Schur-Feshbach leakage L_+
- Expected observation: A stable interval plateau for Delta_R^- across rho; positive plateau promotes finite endpoint-box positivity, negative or unstable plateau quarantines the R repair.
- Transfer certificate needed: Cutoff-stable same-theory recovery plus outward-rounded annular interval bounds uniform in a/eta before any intuition affects proof obligations.

## Next Experiment

Proof search: compute outward-rounded annular plateau constants for R_{++}^{ren}; record relation to a connected cumulant witness and same-theory nontriviality witness only as support, not a Clay claim.

# Raw signed-orbit K4 interval witness for finite post-H,K endpoint positivity

## Candidate Lemma

Finite signed-orbit K4 stress certificate. In the heat-kernel regulated SU(N) endpoint box, after the H,K Schur compression, same-regulator raw connected four-curvature orbit intervals give a valid finite falsifier if D_p^+<0 or if L_{pq}(theta)^2>D_p^+D_q^+. The conclusion is only that the worked finite H,K endpoint quadratic form is not positive semidefinite; it is not a Clay mass-gap theorem.

## Definitions

- source object: finite heat-kernel regulated SU(N) Wilson endpoint data consisting of oriented plaquette sheets, transported curvature insertions, raw connected four-curvature cumulant intervals, OPE intervals, and H,K Schur blocks in one cutoff theory.
- target object: the finite Hermitian Schur-corrected endpoint matrix U_sigma on the span of endpoint Wilson observables after H,K removal; independently it is the local Route A positivity gate, not a continuum Hamiltonian.
- controlled interface: the signed-orbit recovery map Rec_orb converts raw plaquette cumulant intervals, Gaussian color-square entries, OPE error intervals, and Schur data into interval enclosures for entries of U_sigma.
- same-theory condition: the cutoff a, heat-kernel parameter sigma, coupling g_R, Wilson normalization, endpoint basis, quotient identities, OPE truncation, and H,K Schur blocks are all fixed before the interval recovery is applied.
- endpoint observable Q_i: the vacuum-subtracted quadratic Wilson boundary flux carried by sheet S_i with heat-kernel parallel transport to the reflection boundary.
- signed K4 orbit: an exact Wilson-quotient class of oriented plaquette quadruples with multiplicity m_o and phase phi_o retained rather than replaced by an unsigned shell envelope.
- stress entry D_i^+: the certified upper endpoint of the interval enclosing the diagonal U_{ii}.
- stress entry L_{ij}(theta): a certified lower bound on |Re(e^{-i theta} U_{ij})| obtained from signed orbit intervals and same-regulator OPE/Schur data.

## Assumptions

- Model: finite four-dimensional hypercubic lattice SU(N) Yang-Mills with heat-kernel plaquette regulator and compact link integration.
- Cutoff: a>0, sigma/a<infty, finite endpoint box, and finite Wilson sheet family are fixed; no continuum or infinite-volume limit is taken.
- Same-theory: Gaussian contractions, K4 cumulants, OPE remainders, and S_HK are computed from the same regulated measure and the same endpoint Wilson basis.
- Validity: the raw interval arithmetic is outward-rounded and respects Hermiticity, reflection support, gauge invariance, and exact Wilson trace identities.
- Local: the theorem changes only the finite Route A endpoint-box gate; OS/Wightman reconstruction, gauge-invariant observable density, nontrivial continuum YM, and physical-unit spectral transfer remain untouched.

## Equations

- color-square-coefficient: `\alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid when the two crossed transported-curvature contractions are normalized in the fundamental Wilson trace for SU(N).
- connected-boundary-polarization: `R_{ij,\sigma}=\alpha_N g_R^4(C_\sigma\circ C_\sigma)_{ij}+\frac{g_R^4}{16N^2}K^{(4)}_{ij,\sigma}+E^{\mathrm{OPE}}_{ij,\sigma}`. Valid when: Valid when the heat-kernel Wilson OPE is truncated after quadratic flux terms and disconnected vacuum/perimeter pieces are removed by connected cumulants.
- signed-orbit-recovery: `K^{(4)}_{ij,\sigma}\in \sum_{o\in\mathcal O_{ij}} m_o e^{i\phi_o} I_o(\sigma,a,g_R)`. Valid when: Applies when exact Wilson quotienting groups oriented plaquette quadruples without discarding their phases or same-regulator interval provenance.
- post-HK-endpoint-form: `U_\sigma=R_\sigma-S_{HK,\sigma},\qquad S_{HK,\sigma}=B_\sigma^*E_\sigma^{-1}B_\sigma`. Valid when: Requires the H,K hairpin block E_sigma to be positive on the eliminated finite subspace and computed in the identical Wilson basis.
- two-sparse-stress-falsifier: `D_p^+<0\ \mathrm{or}\ L_{pq}(\theta)^2>D_p^+D_q^+\quad\Longrightarrow\quad \exists x\in\mathrm{span}\{e_p,e_q\}:x^*U_\sigma x<0`. Valid when: Valid when D_p^+, D_q^+ are certified diagonal upper bounds and L_pq(theta) is a certified phased off-diagonal lower bound for the same Hermitian interval matrix.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Observable Density In The Excitation Sector; source object: finite heat-kernel regulated SU(N) Wilson endpoint data consisting of oriented plaquette sheets, transported curvature insertions, raw connected four-curvature cumulant intervals, OPE intervals, and H,K Schur blocks in one cutoff theory.; target object: the finite Hermitian Schur-corrected endpoint matrix U_sigma on the span of endpoint Wilson observables after H,K removal; independently it is the local Route A positivity gate, not a continuum Hamiltonian.; Model: finite four-dimensional hypercubic lattice SU(N) Yang-Mills with heat-kernel plaquette regulator and compact link integration..
- Attack conceptual pressure: R must be a connected cumulant witness in one cutoff theory, not scalar endpoint rhetoric, A012 shell aspiration, OS Hilbert observable algebra, or a gauge-invariant observable density restatement.
- Freeze declarative tension: Wilson/OPE data, raw non-Gaussian K4 intervals, OPE error, and S_HK must jointly control one finite endpoint quadratic form, while continuum OS reconstruction, excitation-sector cyclicity, nontriviality, and mass gap remain non-claims.
- Start from Q_i as a vacuum-subtracted transported quadratic boundary flux; connected cumulants cancel disconnected vacuum and perimeter factors before Schur subtraction.
- Decompose R_{ij,sigma} into the PSD Gaussian Hadamard color square, the connected K4 term, and the OPE interval error in the same heat-kernel regulator.
- Replace sign-losing A012 shells by exact signed Wilson orbit classes, preserving multiplicity, phase, orientation, color trace, and endpoint indices.
- Assemble interval entries for U_sigma=R_sigma-S_HK,sigma, then compute D_i^+ and the phased lower bound L_{ij}(theta).
- Apply the Rayleigh 1-sparse test D_i^+<0 or the 2-sparse determinant test L_{ij}(theta)^2>D_i^+D_j^+ to obtain an explicit x_stress.

Blocking gap: The branch still lacks actual same-regulator raw K4 orbit intervals I_o(sigma,a,g_R) for the first H,K endpoint pair, so D_i^+, L_{ij}(theta), and x_stress cannot yet be numerically or interval-certified.

## Falsifiers

- A valid falsifier for the finite H,K endpoint route is D_i^+<0 from raw same-regulator intervals.
- A valid two-sparse falsifier is L_{ij}(theta)^2>D_i^+D_j^+ with a recovered Rayleigh vector x_stress.
- Regulator mismatch between K4 intervals, OPE errors, and S_HK invalidates the stress certificate.
- Unsigned A012 shells pretending to provide a phased lower bound demote the abstraction as non-invariant.
- If OPE interval overflow makes every D_i^+ and L_{ij} vacuous, the branch must quarantine rather than promote.
- If all stress tests survive but no full Loewner lower bound is computed, survival is not a positivity proof.

## Learning

The conceptual pressure is no longer observable-density cyclicity; it is the missing mediator from raw connected Wilson cumulants to a Schur-corrected finite endpoint quadratic form. The carrier audit is decisive: scalar R is too weak, A012 shells are sign-losing, OS Hilbert observable algebra is too strong and circular for this local gate, full Delta_raw is complete but expensive, and signed raw orbits are efficient because they preserve phases, Hermiticity, gauge invariance, exact Wilson quotienting, and same-theory normalization. The hard gate D_i^+<0 or L_ij(theta)^2>D_i^+D_j^+ is sharp because it either supplies a finite falsifier or forces full Delta_raw proof search, while every Clay frontier gate remains untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the finite endpoint route.`
- Rationale: The branch has exhausted symbolic R and shell abstractions; only a concrete same-regulator connected cumulant witness can decide whether the post-H,K Wilson endpoint matrix is killed or deserves full Delta_raw proof search.
- Situation seed: Finite SU(2) heat-kernel lattice Yang-Mills on one reflected endpoint box with two fixed boundary Wilson sheets p and q, exact H,K Schur block frozen, and raw plaquette quadruples grouped into signed Wilson orbits.
- Varied variable: The heat-kernel smoothing ratio b=sigma/a is varied while the endpoint geometry and coupling normalization are held fixed.
- Held-fixed controls: Same finite endpoint Wilson basis Q_p,Q_q and the same H,K Schur block B^*E^{-1}B., Same lattice cutoff a, finite box, gauge group SU(2), Wilson trace normalization, and exact quotient policy., Same OPE truncation order, connected-cumulant subtraction, and outward-rounded interval arithmetic.
- Expected observation: As b varies, either a phased orbit contribution enlarges L_pq(theta) enough to satisfy L_pq(theta)^2>D_p^+D_q^+, producing a finite falsifier, or all two-sparse stresses survive and the route must move to full Delta_raw Loewner proof search.
- Transfer certificate needed: A validator-facing raw K4 signed-orbit interval table, Hermiticity and Wilson-quotient audit, OPE error interval, and same-basis Schur subtraction certificate before the intuition may affect proof obligations.

## Next Experiment

Proof search: compute the first validator-facing raw K4 signed-orbit interval table for the connected cumulant witness cum_2(Q_p,Q_q) in the heat-kernel SU(2) endpoint box, then evaluate D_p^+<0 or L_pq(theta)^2>D_p^+D_q^+; do not return to gauge-invariant observable density or excitation-sector cyclicity unless this finite Route A branch is quarantined.

