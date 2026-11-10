# cycle-0324

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: finite endpoint source interval gate

## Candidate Lemma

For the post-H,K reflected-Wilson hairpin block in the heat-kernel plaquette-sheet regulator, source-equivalent endpoint boxes may be aggregated before any sign clipping. The finite same-theory OS gate is decided by an exact interval product scalar, not by raw R or a raw negative kappa_4 spectrum.

## Definitions

- source object: a finite family of regulated SU(N) reflected Wilson endpoint boxes v with heat-kernel plaquette-sheet sources F_v(s)=log Z_v(sL_v), fractional incidences b_ij(v), and source-equivalence classes c defined by equality of regulated source derivatives through order eight.
- target object: the finite post-H,K Schur-Feshbach null-channel scalar S_HKR for the locked three-hairpin Wilson block; positivity promotes only this finite OS transfer gate and does not assert continuum existence or a mass gap.
- controlled interface: the carrier C_ep sends endpoint source intervals [kappa_c^-,kappa_c^+], aggregated incidence intervals [D_c^-,D_c^+], color factor C_N, Gaussian margin M_G, and tail budget tau_tail to a certified scalar interval [I_-,I_+].
- same-theory condition: the Wilson loops, heat-kernel regulator, reflection map, source normalization, and endpoint partition functions are identical before and after collar collapse; no boundary counterterm, algebra enlargement, or gauge-fixed replacement is allowed.
- bridge/carrier: C_ep is source-equivalent, incidence-signed, cutoff-budgeted, and exports only [I_-,I_+] to the finite OS gate.
- conceptual pressure: endpoint collapse must be sign-certified inside the same Wilson theory rather than hidden in symbolic R.
- declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must jointly hold, but H,K and the half-overlap shield do not determine the connected cumulant witness.

## Assumptions

- Model: four-dimensional lattice SU(N) Yang-Mills with reflection-positive heat-kernel plaquette action and gauge-invariant Wilson observables only.
- Regime: finite Route A endpoint-box computation after the H,K Schur-Feshbach reduction; the claim is restricted to this finite Wilson block.
- Cutoff: endpoint boxes have fixed physical shape while a,L remain in the regulated collar regime; all source derivative and tail bounds are uniform over the finite block.
- Same-theory: source-equivalence means equality of regulated Wilson source functions, not visual equality of endpoint geometry or a renormalized boundary theory.
- Uniformity: the tail tau_tail bounds all non-endpoint, corner-overlap, and unresolved higher-order contributions with the same cutoff normalization.
- Validity: interval products are computed after aggregating incidences inside each source class; clipping before aggregation is not valid because it destroys null-channel cancellations.

## Equations

- seven_point_endpoint_cumulant_stencil: `\widehat\kappa_c(h)=\frac{-F_c(-3h)+12F_c(-2h)-39F_c(-h)+56F_c(0)-39F_c(h)+12F_c(2h)-F_c(3h)}{6h^4}`. Valid when: Valid when F_c(s)=\log Z_c(sL_c) has eight uniformly bounded source derivatives on the same heat-kernel endpoint box.
- stencil_error_budget: `|\widehat\kappa_c(h)-\partial_s^4F_c(0)|\le \frac{7h^4}{240}M_{8,c}`. Valid when: Applies when the eighth source derivative is bounded by M_{8,c} throughout the symmetric stencil interval.
- source_class_incidence: `D_c=\sum_{v\in c}\bigl(2b_{12}(v)-4b_{13}(v)-4b_{23}(v)\bigr)`. Valid when: Valid when v ranges over one regulated source-equivalence class and b_ij are the fractional endpoint incidences after the fixed null-vector contraction.
- exact_interval_product_lower: `p_c^-:=\min\{D_c^-\kappa_c^-,D_c^-\kappa_c^+,D_c^+\kappa_c^-,D_c^+\kappa_c^+\}`. Valid when: Valid when the endpoint incidence interval and source cumulant interval independently enclose the same source-equivalence class contribution.
- finite_gate_interval: `I_-:=M_G+C_N\sum_c p_c^- -\tau_{\rm tail},\qquad I_+:=M_G+C_N\sum_c p_c^+ +\tau_{\rm tail}`. Valid when: Requires the post-H,K decomposition into Gaussian margin, endpoint connected cumulants, and a uniform tail budget for the locked Wilson block.
- finite_transfer_decision: `I_-\ge0\Rightarrow S_{HKR}\ge0,\qquad I_+<0\Rightarrow \exists x\perp {\bf 1}:\ x^*Q_{\rm target}x<0`. Valid when: Valid when [I_-,I_+] encloses the complete Schur-Feshbach null scalar for the same reflected Wilson observables.

## Attempted Derivation

- Start with the finite Schur-Feshbach null scalar after the previously computed H,K gate; do not rederive the old threshold.
- Use the regulated Wilson boundary OPE decomposition: Wick-square terms are positive Gram contributions, the straight C_A f f contact cancels by null incidence, and the remaining connected boundary polarization is endpoint-local plus tau_tail.
- Partition endpoints by equality of regulated source data F_v(s) through the derivative order used by the stencil; this is the same-theory equivalence policy.
- For each class c, sum signed incidences to D_c before clipping. This preserves cancellations that raw kappa_4 spectra and geometry-only grouping lose.
- Enclose the connected fourth cumulant by either the seven-point source stencil or the root-quartic screen with a uniform remainder.
- Compute the exact interval product p_c=[D_c^-,D_c^+]\,[\kappa_c^-,\kappa_c^+] and sum it with C_N, M_G, and tau_tail to obtain [I_-,I_+].
- If I_->=0, the finite post-H,K reflected-Wilson block is promoted as OS-positive at this gate. If I_+<0, the same Wilson observables give a finite same-theory falsifier. Otherwise the branch remains quarantined with a validator-facing connected cumulant witness request.

Blocking gap: No actual endpoint source table, derivative bounds M_8,c, or cutoff-uniform tau_tail has been supplied for the positive-D source classes.

## Falsifiers

- A source-certified endpoint class has D_c^+>0, kappa_c^+<0, and the resulting I_+<0; this is a finite same-theory falsifier of the post-H,K OS gate.
- The heat-kernel endpoint source stencil requires a boundary counterterm or a changed Wilson normalization at t=0, invalidating the same-theory condition.
- The eighth-derivative or chart remainder bound grows with cutoff so tau_tail is not uniform.
- Endpoint boxes grouped as source-equivalent fail equality of regulated source derivatives, so aggregation before clipping was invalid.
- A positive-D thin 12-only endpoint family violates the half-overlap shield and dominates M_G despite the root-quartic screen.
- The reflection-positive lattice regulator controls collar observables but not the endpoint source derivatives entering the connected cumulant witness.

## Learning

Cycle 324 upgrades screened quarantine into an exact finite interval-product carrier. The conceptual pressure is endpoint collapse inside the same Wilson theory. The declarative tension is collar OS positivity plus fixed gauge-invariant Wilson observables plus singular connected endpoint OPE without a boundary theory. Raw R is too weak, raw kappa_4 spectra are too strong, and global Schur-preimage positivity is valid but too coarse after H,K. The sharp contribution is aggregate-before-clipping plus exact interval multiplication for the connected cumulant witness. Success promotes only the finite post-H,K reflected-Wilson OS gate; failure gives a finite same-theory falsifier; Clay continuum construction, full OS/Wightman reconstruction, nontriviality, and positive mass gap remain non-claimed.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe while the branch remains under screened quarantine.`
- Rationale: The abstract OS closed-cone and Wilson obstruction ladder are already exhausted; the finite gate now depends on whether positive-D endpoint leakage survives actual source differentiation in the same Wilson theory.
- Situation seed: Heat-kernel plaquette-sheet SU(N) three-hairpin endpoint-box family with one endpoint source class continuously moved from a 12-only overlap footprint to a mixed 12/13/23 footprint while the reflected Wilson collar geometry and H,K data are held fixed.
- Varied variable: Fractional leakage alpha=(b_13+b_23)/b_12 in the endpoint incidence table, with alpha crossing the half-overlap value 1/2.
- Held-fixed controls: Same SU(N) heat-kernel plaquette regulator and reflection-positive Wilson action., Same gauge-invariant Wilson loop observables and same source normalization L_c., Same Schur-Feshbach H,K finite block, Gaussian margin M_G, and color factor C_N., No boundary counterterm, no gauge-fixed replacement algebra, and no change of endpoint source equivalence policy.
- Expected observation: For alpha>=1/2 the negative root-quartic cumulant is shielded because D_c<=0; for alpha<1/2 the connected cumulant witness can lower I_- and may become a finite falsifier if the source interval and tau_tail certify I_+<0.
- Transfer certificate needed: A validator-facing table of regulated endpoint source values F_c(kh), uniform M_8,c and tau_tail bounds, and a proof that the source-equivalence classes and fractional incidences are cutoff-uniform in the same Wilson theory.

## Next Experiment

Proof search plus validator-facing endpoint computation: build the C_ep table for positive-D source classes, evaluate the seven source values F_c(kh), certify kappa intervals and tau_tail, then decide I_->=0 promotion, I_+<0 falsifier, or continued quarantine.

# Annular Ward-Hessian R++ Certificate

## Candidate Lemma

For centered flowed H,K plus hairpins, if every connected C4 sector has Ward-Hessian annular decay nu_s>2 and recovery error E_rec, then R++ has a computable lower interval; R++>L+ promotes finite endpoint-box positivity, otherwise quarantine this R repair.

## Definitions

- source object: centered gradient-flowed Wilson hairpin cumulant R_{++}^{ren} for two reflected plus-channel endpoint boxes in one cutoff SU(N) Wilson ensemble.
- target object: finite endpoint-box positivity margin for the plus channel in the Schur-Feshbach H,K reduction, with leakage L_+ fixed before Wilson input.
- controlled interface: recovery map Phi_{t,epsilon} from raw H,K Wilson hairpins to endpoint sheet currents preserving orientation, color trace, reflection labels, and cell moments.
- same-theory condition: all flowed observables, counterterms, sector constants, and recovery errors are computed inside the same cutoff Wilson measure and same limiting family.
- observable: J_+ is the plus endpoint sheet current; its monopole and dipole moments vanish after Ward, cusp, and reflection cancellations.
- sector constants: C_{s,<} are near-cell C4 interval bounds; T_s is the dyadic far-annulus tail for sector s.

## Assumptions

- Model: four-dimensional SU(N) Wilson lattice Yang-Mills with gradient-flow time t>0 and endpoint point-splitting epsilon before the continuum limit.
- Regime: endpoint box side eta is fixed with epsilon << sqrt(8t) << eta, and the H,K geometry is the actual post-reduction collar/hairpin geometry.
- Uniformity: G_{++}, C_{s,<}, A_{s,J0}, and E_rec have cutoff- and volume-uniform outward-rounded intervals in the chosen coupling window.
- Same-theory: Phi_{t,epsilon} changes representation only; it cannot import a different measure, auxiliary Gaussian field, or non-Gaussian Schwinger family.
- Validity: the cumulant expansion, Ward subtraction, and cusp counterterms are valid for the centered flowed Wilson observables used in R_{++}^{ren}.
- Local: this is a finite Route A endpoint certificate; it does not claim OS reconstruction, observable density, nontriviality, or a Hamiltonian mass gap.

## Equations

- flowed_cumulant_carrier: `R_{++}^{ren}(t,\epsilon)=\kappa_2(W^{ren}_{J_1,+}(t,\epsilon),W^{ren}_{J_2,+}(t,\epsilon))`. Valid when: Valid under the source object and Same-theory assumptions when t>0 and epsilon>0 regularize both centered Wilson hairpins.
- lower_interval: `\underline R_{++}=g_t^4(N^2-1)\left(2G_{++}^{-}-N M_{2,+}^2\sum_s(C_{s,<}^{+}+T_s^{+})\right)-E_{rec}^{+}`. Valid when: Applies after Ward, cusp, and plus-moment cancellations with cutoff-uniform sector constants and fixed endpoint cell moments.
- annular_tail: `T_s^{+}=A_{s,J_0}^{+}\,2^{(4-2\nu_s)J_0}/(1-2^{4-2\nu_s}),\qquad \nu_s>2`. Valid when: Requires the far-annulus mixed-Hessian bound in the Regime assumption on every dyadic shell beyond J0.

## Attempted Derivation

- Use gradient flow and endpoint point-splitting; expand kappa_2 of two centered renormalized hairpins through g_t^4. Disconnected product and one-hairpin perimeter/cusp counterterms cancel before sector splitting.
- Represent H,K hairpins by plus endpoint sheet currents. Ward identity and reflection symmetry kill monopole/dipole moments, leaving C4 sectors tested only by mixed Hessians against M_{2,+}^2.
- Split the endpoint complement into near cells and dyadic far annuli. Near sectors enter C_{s,<} by interval quadrature; far shell J contributes at most A_{s,J0}^+ 2^{(4-2nu_s)J}.
- Sum the geometric tail and subtract E_rec^+ and L_+. The sign of Delta_R=underline R_{++}-L_+ is the finite promotion or quarantine certificate.

Blocking gap: Need cutoff-uniform verification of mixed-Hessian exponents nu_s>2 and recovery error E_rec for the actual flowed Wilson regulator, not just a formal sector decomposition.

## Falsifiers

- falsifier: a sector interval gives nu_s<=2 or q_s=2^{4-2nu_s}>=1, so the far C4 tail cannot be summed.
- falsifier: Ward/cusp subtraction leaves a nonzero monopole or dipole endpoint moment, invalidating the M_{2,+}^2 Hessian reduction.
- falsifier: E_rec from raw Wilson hairpins to endpoint currents grows with cutoff, breaking the same-theory transfer.
- falsifier: certified Delta_R=underline R_{++}-L_+<=0 for the actual H,K geometry, quarantining the endpoint repair.

## Learning

Conceptual pressure: finite Feshbach positivity needs a same-theory Wilson mediator. Declarative tension: pair covariance and recovery may be valid while connected C4 erases R. Endpoint currents beat raw contours and global OS/non-Gaussian routes because Ward moments and annular tails are primitive. Value: route-deciding finite falsifier.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The abstract R term is isolated; the proof state needs target-preserving interval behavior under one controlled parameter, not another OS/Wilson restatement.
- Situation seed: SU(N) Wilson lattice on a large four-torus, two actual H,K plus-channel hairpins in fixed endpoint boxes, gradient-flow time t, point-splitting epsilon, and centered kappa_2 evaluated by endpoint sheet currents.
- Varied variable: dyadic cutoff J0 for far annuli, equivalently the inner scale at which the C4 tail is replaced by a geometric Hessian majorant.
- Held-fixed controls: same Wilson action, bare-coupling window, gauge group SU(N), and H,K endpoint geometry, gradient-flow regulator t and point-splitting epsilon with sqrt(8t)<<eta and epsilon<<eta, Ward/cusp counterterms, plus-channel current normalization, and Schur-Feshbach leakage L_+
- Expected observation: If all sector exponents nu_s>2, tail certificates shrink geometrically and Delta_R stabilizes; a negative plateau is a valid falsifier for the endpoint repair.
- Transfer certificate needed: Cutoff-uniform recovery map from raw hairpins to endpoint currents plus outward-rounded interval proof of G, C_{s,<}, A_{s,J0}, and E_rec in the same Wilson ensemble.

## Next Experiment

Proof search: compute outward-rounded G_{++}^-, C_{s,<}^+, A_{s,J0}^+, and E_rec^+ for actual H,K plus hairpins; report Delta_R as connected cumulant witness data, while same-theory nontriviality witness and OS spectral gates remain untouched.

# Signed-orbit raw K4 stress witness for finite Wilson endpoint positivity

## Candidate Lemma

Signed-orbit two-sparse stress falsifier. In a finite heat-kernel regulated SU(N) Wilson endpoint box, exact signed-orbit intervals for the raw connected four-curvature cumulant give a valid finite demotion certificate: if a phase theta and endpoints p,q satisfy L_pq(theta)^2>D_p^+D_q^+, then the Schur-corrected endpoint matrix is not positive semidefinite. This kills only the worked H,K finite Route A endpoint gate, not the Clay mass-gap problem.

## Definitions

- source object: same-cutoff heat-kernel regulated SU(N) Wilson endpoint cumulants built from transported plaquette curvature variables in a fixed finite endpoint box.
- target object: the finite Hermitian Schur-corrected endpoint quadratic form U on the selected Wilson endpoint basis, independently defined before any spectral or continuum transfer.
- controlled interface: signed-orbit raw K4 interval recovery map from plaquette cumulant representatives to phase-resolved two-by-two endpoint principal compressions.
- same-theory condition: Gaussian covariance, raw K4 intervals, OPE remainder, Wilson normalization, and H,K Schur block are computed with the same regulator, cutoff, coupling, volume, endpoint basis, and reflection support.

## Assumptions

- Model: SU(N) Yang-Mills on a finite hypercubic lattice with heat-kernel plaquette action, cutoff a, smoothing scale sigma>=c a, and finite endpoint Wilson sheets.
- Cutoff: all plaquette sums, orbit representatives, OPE errors, and Schur blocks are finite-dimensional interval objects at fixed a and fixed endpoint geometry.
- Same-theory: no continuum limit, OS reconstruction, or observable-density assertion is imported; the stress witness is a connected cumulant witness in one cutoff theory.
- Validity: orbit quotienting uses only exact Wilson trace identities, orientation conjugation, lattice symmetries preserving the endpoint box, and explicitly recorded multiplicities.
- Local: the result changes the finite post-H,K endpoint-box positivity gate; volume/cutoff-uniform basin entry, OS positivity in the continuum, gauge-invariant observable density, excitation-sector cyclicity, and physical-unit spectral transfer remain untouched.

## Equations

- transported endpoint quadratic observable: `Q_i^\sigma=\sum_{(r,s)\in \mathcal S_i} w_i(r,s)\,:\Phi_r^a(\sigma)\Phi_s^a(\sigma):`. Valid when: Valid when Q_i^sigma is built from transported heat-kernel plaquette curvature variables in the same finite endpoint box.
- Schur-corrected raw endpoint matrix: `U_{ij}=\alpha_N g_R^4 G_{ij}+\frac{g_R^4}{16N^2}K^{(4)}_{ij}+E^{\mathrm{OPE}}_{ij}-S^{HK}_{ij},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after vacuum and perimeter normalization in the same cutoff Wilson basis, before any continuum or OS spectral transfer is invoked.
- signed-orbit K4 recovery: `K^{(4)}_{pq}(\theta)=\sum_{O\in\mathcal O_{pq}} c_O(\theta)\,\kappa_O^\sigma,\quad \kappa_O^\sigma\in[\ell_O,u_O]`. Valid when: Requires exact signed-orbit quotienting by Wilson identities and interval enclosures for each representative connected four-curvature cumulant.
- phase interval lower modulus: `\mathcal I_{pq}(\theta)=\operatorname{Hull}\{\operatorname{Re}(e^{-i\theta}U_{pq})\},\quad L_{pq}(\theta)=\operatorname{dist}(0,\mathcal I_{pq}(\theta))`. Valid when: Valid when the phase theta is fixed and all summand intervals are propagated with outward-rounded interval arithmetic.
- two-sparse falsifier gate: `L_{pq}(\theta)^2>D_p^+D_q^+\;\Longrightarrow\; \exists x\in\operatorname{span}\{e_p,e_q\}:\ x^*U x<0`. Valid when: Applies to the two-dimensional principal compression when D_p^+ and D_q^+ are certified upper bounds for the same Hermitian endpoint matrix.

## Attempted Derivation

- Conceptual pressure attacked: R must become an actual connected cumulant witness with computable raw K4 intervals, not scalar R rhetoric, A012 shell aspiration, or OS Hilbert observable algebra language.
- Declarative tension: Wilson/OPE coefficients, non-Gaussian raw K4, OPE error, and S_HK must jointly control one finite endpoint quadratic form in a single cutoff theory, while continuum YM existence, gauge-invariant observable density, excitation-sector cyclicity, and Hamiltonian mass gap remain non-claims.
- Start from the same-theory Schur-corrected endpoint matrix U=alpha_N g_R^4 G+g_R^4 K4/(16N^2)+E_OPE-S_HK.
- Use exact Wilson symmetries to compress raw plaquette quadruple cumulants into signed orbits; propagate representative intervals to a phase interval for Re(e^{-i theta}U_pq).
- Define diagonal upper bounds D_p^+,D_q^+ using Gaussian upper bounds, K4 orbit upper intervals, OPE upper intervals, and lower Schur subtraction from the same cutoff data.
- PSD of a Hermitian two-by-two principal compression implies |U_pq|^2<=U_pp U_qq. Therefore the certified inequality L_pq(theta)^2>D_p^+D_q^+ gives a negative determinant and an explicit Rayleigh stress vector.
- Hard gate: a successful inequality demotes the finite H,K endpoint route; failure merely forces full Delta_raw Loewner proof search.

Blocking gap: No validator-certified raw signed-orbit intervals [ell_O,u_O] for the heat-kernel connected four-curvature cumulant have been supplied for the concrete H,K endpoint geometry.

## Falsifiers

- falsifier: an exact signed-orbit K4 interval set yields L_pq(theta)^2>D_p^+D_q^+ for some endpoint pair, killing the finite H,K endpoint PSD route.
- falsifier: orbit compression identifies plaquette quadruples not related by exact Wilson identities, making the interval recovery invalid.
- falsifier: the K4 intervals, OPE bounds, Gaussian covariance, or Schur block are computed with different regulators or normalizations, violating the same-theory condition.
- falsifier: all phase intervals contain zero and diagonal upper bounds are too large, demoting the two-sparse tactic to full Delta_raw proof search.
- falsifier: a diagonal upper bound D_p^+<0 already gives a one-sparse negative Rayleigh certificate and bypasses the off-diagonal test.

## Learning

The contribution-making move is a finite signed-orbit stress theorem for the connected boundary-OPE polarization. The current carrier audit is decisive: scalar R is representation-limited, A012 shells are convenient but quarantined, full Delta_raw search is complete but expensive, and OS Hilbert observable algebra or gauge-invariant observable density is too strong and circular for this local gate. The efficient representation must encode oriented plaquettes, sheet weights, heat-kernel transporters, color tensors, cumulant intervals, OPE intervals, endpoint indices, and Schur blocks; preserve gauge invariance, reflection support, Hermiticity, Gaussian/K4 separation, same-theory normalization, and exact Wilson quotienting; support cumulant contraction, phase interval summation, Rayleigh stress search, Loewner bounds, and Schur subtraction; use finite endpoint-box complexity; transfer only through tau, Delta_raw, or x_stress; and expose falsifiers by negative margin, missing intervals, non-invariant quotienting, or regulator mismatch. The conceptual value signal is sharp and route-changing at finite scope: a few raw K4 orbit intervals can kill the H,K endpoint route, while survival honestly hands off to full finite proof search and leaves every Clay frontier gate untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the signed-orbit raw K4 interval computation.`
- Rationale: The branch is looping unless the connected boundary-OPE polarization is tested on concrete raw cumulant intervals rather than restated through OS density or scalar R language.
- Situation seed: Fixed SU(N) heat-kernel lattice at cutoff a with smoothing sigma=2a, one worked H,K endpoint collar/hairpin box, exact Wilson endpoint basis, and signed-orbit representatives for plaquette quadruple cumulants contributing to K4_pq.
- Varied variable: Width epsilon_K4 of each certified signed-orbit cumulant interval, with interval centers and exact orbit multiplicities held fixed.
- Held-fixed controls: Same cutoff a, heat-kernel action, renormalized coupling g_R, smoothing sigma, finite endpoint box, and reflection support., Same Wilson normalization, Gaussian covariance G, OPE error budget E_OPE, and H,K Schur block S_HK., Exact Wilson quotient policy; no approximate geometric orbit merging and no continuum or OS spectral import.
- Expected observation: As epsilon_K4 decreases, either one phase interval separates from zero enough to satisfy L_pq(theta)^2>D_p^+D_q^+ and produce a finite falsifier, or all two-sparse gates survive and the proof state must move to full Delta_raw Loewner search.
- Transfer certificate needed: A validator-facing connected cumulant witness: outward-rounded raw signed-orbit intervals for K4 representatives, exact multiplicity/sign audit, same-theory Gaussian/OPE/Schur data, and a recovered stress vector or full-matrix handoff certificate.

## Next Experiment

Proof search: compute the first same-regulator signed-orbit raw K4 interval table for one endpoint pair p,q in the H,K box, recover D_p^+,D_q^+, scan theta in exact phase sectors, and either output x_stress as a connected cumulant witness falsifier or hand off to full Delta_raw Loewner search. Do not pursue OS Hilbert observable algebra or gauge-invariant observable density in this cycle.

