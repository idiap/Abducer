# cycle-0332

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: endpoint-source quarantine gate

## Candidate Lemma

Finite endpoint-source interval theorem: for the heat-kernel plaquette-sheet regulator, the post-H,K null-channel endpoint contribution is decided by an aggregate-before-product interval I_gate. If inf I_gate>=0, this fixed reflected-Wilson block passes the endpoint gate; if sup I_gate<0, it is a finite same-theory falsifier; otherwise the branch is validly quarantined pending endpoint source data.

## Definitions

- source object: C_ep(a,L) is the same-theory heat-kernel SU(N) plaquette-sheet endpoint carrier: endpoint source classes c, seven values log Z_c(rh), cumulant intervals K_c, signed incidence intervals D_c, color factor C_N, Gaussian margin M_G, and tail interval T_tail.
- target object: I_gate is the finite post-H,K reflected-Wilson OS transfer scalar for the fixed three-hairpin Wilson block; it is an endpoint-order positivity certificate, not a continuum Yang-Mills construction.
- controlled interface: C_ep -> I_gate uses source-equivalence aggregation before interval multiplication, then color multiplication and tail addition; it exports only a scalar interval to the finite OS gate.
- same-theory condition: all source derivatives, incidences, Wilson normalizations, and tails come from the identical heat-kernel regulated gauge-invariant Wilson theory with no boundary counterterm or algebra change.
- connected cumulant witness: K_c is the fourth source derivative of log Z_c along the singlet endpoint source L_c after connected Wick-square cancellation.
- endpoint incidence: D_c=sum_{v in c}(2b_{12}(v)-4b_{13}(v)-4b_{23}(v)) is summed over source-equivalent endpoint boxes before clipping or sign testing.

## Assumptions

- Model: four-dimensional lattice SU(N) Yang-Mills with Wilson heat-kernel plaquette-sheet regulator and reflection plane t=0.
- Regime: fixed finite three-hairpin block after the previously computed H,K Schur-Feshbach reduction; no claim is made for arbitrary Wilson families.
- Cutoff: the intervals K_c and T_tail are uniform along the finite cutoff/volume subsequence used for the collar limit.
- Same-theory: endpoint source insertions are derivatives of the same Wilson partition function, not boundary degrees of freedom or a changed observable algebra.
- Validity: Wick-square Gram terms and straight f f contacts have already been removed by connected-log differentiation and the null-incidence cancellation.
- Local: all endpoint boxes not represented by source classes are charged to T_tail with an explicit locality budget.

## Equations

- seven_point_endpoint_cumulant: `\kappa_c(h)=\frac{-F_c(-3h)+12F_c(-2h)-39F_c(-h)+56F_c(0)-39F_c(h)+12F_c(2h)-F_c(3h)}{6h^4}+E_c(h),\quad F_c(s)=\log Z_c(sL_c)`. Valid when: Valid when F_c is eight-times differentiable in the heat-kernel endpoint source and the same regulated Wilson measure defines all seven evaluations.
- stencil_error_bound: `|E_c(h)|\le \frac{7h^4}{240}\sup_{|s|\le 3h}|F_c^{(8)}(s)|`. Valid when: Applies when the seven-point central fourth-derivative stencil is used with a uniform eighth-source-derivative endpoint bound.
- aggregate_incidence: `D_c=\sum_{v\in c}\bigl(2b_{12}(v)-4b_{13}(v)-4b_{23}(v)\bigr)`. Valid when: Valid when c is a source-equivalence class determined before clipping by equality of regulated endpoint source data.
- finite_endpoint_gate_interval: `I_{\mathrm{gate}}=M_G+C_N\sum_c K_c\,D_c+T_{\mathrm{tail}},\quad C_N=\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2`. Valid when: Requires the post-H,K null-channel reduction, connected cumulant witness intervals, aggregated endpoint incidences, and a same-theory uniform tail interval.
- decision_rule: `\inf I_{\mathrm{gate}}\ge0\Rightarrow \text{finite promotion},\quad \sup I_{\mathrm{gate}}<0\Rightarrow \text{finite falsifier},\quad 0\in I_{\mathrm{gate}}\Rightarrow \text{quarantine}`. Valid when: Valid when I_gate includes every endpoint source class and all unresolved endpoint or corner contributions are inside T_tail.

## Attempted Derivation

- Conceptual pressure attacked: endpoint collapse must be sign-certified inside the same Wilson theory after H,K, rather than hidden in symbolic R or promoted by the OS closed-cone topology.
- Declarative tension: collar reflection positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must jointly hold without adding a boundary theory; H,K, half-overlap shielding, and the root-quartic screen do not determine the scalar.
- Start from the post-H,K null-channel scalar and retain only endpoint connected fourth cumulants because Wick-square Gram terms are positive and straight nonabelian f f contacts cancel by null incidence.
- Define source-equivalence classes by equality of regulated source data F_c(s)=log Z_c(sL_c); aggregate signed incidences inside each class before interval multiplication.
- Use the seven-point fourth-source stencil to enclose the connected cumulant witness K_c with an explicit eighth-derivative error.
- Form I_gate=M_G+C_N sum_c K_c D_c+T_tail and apply interval sign logic: lower nonnegative promotes the finite block, upper negative gives a finite falsifier, straddling zero quarantines.
- Stress calculation: common K=-1 with incidences +1 and -1 contributes zero after valid aggregation but would falsely demote if clipped before aggregation.

Blocking gap: No actual same-theory endpoint source intervals K_c and no cutoff-uniform T_tail have been certified for the positive-D source classes.

## Falsifiers

- A validator computes sup I_gate<0 for a positive-D endpoint source class; this is a finite same-theory falsifier of the post-H,K Wilson OS transfer block.
- The seven source values require a boundary counterterm or altered Wilson normalization; then the same-theory condition fails even if an interval is positive.
- The endpoint tail T_tail is not cutoff-uniform, so the finite gate cannot be validly transferred through collar collapse.
- Source-equivalent boxes clipped before aggregation produce a spurious negative interval; this falsifier targets the carrier, not Yang-Mills.
- A positive-D class has a connected cumulant witness more negative than the root-quartic screen permits, exposing a missing non-Gaussian endpoint contribution.

## Learning

Cycle 332 makes the loop repair explicit. The conceptual pressure is endpoint collapse inside the same Wilson theory. The hard gate is the finite post-H,K reflected-Wilson OS transfer scalar: success promotes only this fixed block; failure gives a finite same-theory falsifier; missing source or tail data keeps quarantine. The declarative tension is collar OS positivity plus fixed gauge-invariant Wilson observables plus singular connected endpoint OPE without a boundary theory. Raw R is too weak, raw kappa4 spectra are too strong, and global Schur-preimage positivity is valid but too coarse after H,K. The efficient representation is C_ep: source classes, seven source values, cumulant intervals, signed incidences, C_N, M_G, and T_tail; it preserves Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; primitive operations are source differentiation, interval arithmetic, aggregation before clipping, color multiplication, and tail addition; equivalence is equality of regulated source data; transfer exports only I_gate; falsifiers are negative interval, nonuniform tail, or boundary counterterm. The conceptual value signal is sharpness at finite scope: negative SU(N) endpoint cumulants are explanatory but not the obstruction; positive-D leakage times a connected cumulant witness plus uniform tail is. Clay continuum construction, gauge-invariant observable density, full OS/Wightman reconstruction, nontriviality, OS spectral transfer, and mass gap remain non-claimed.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe while the branch is quarantined for endpoint data.`
- Rationale: The branch is looping on promotion language; a concrete heat-kernel endpoint family tests whether positive-D leakage can actually defeat the finite margin without changing the Wilson theory.
- Situation seed: Fixed SU(N) heat-kernel plaquette-sheet three-hairpin block after H,K, with one endpoint source class c whose 12 footprint dominates and whose 13/23 leakage fraction is tunable in the incidence data.
- Varied variable: The leakage ratio alpha=(b13+b23)/b12 in D_c=2b12-4(b13+b23), with the endpoint source L_c and heat-kernel time t_c held fixed.
- Held-fixed controls: Same heat-kernel Wilson action and same gauge-invariant Wilson loop observables; no boundary counterterm or gauge-fixing replacement., Fixed H,K hairpin geometry, fixed Gaussian margin M_G, fixed color factor C_N, and fixed seven-point connected cumulant witness stencil., Uniform endpoint box scale and a declared T_tail budget for all nonlocal corner remainders.
- Expected observation: For alpha>=1/2 the class is shielded because D_c<=0; for alpha<1/2 a negative connected cumulant witness can lower I_gate, and a certified sign change would be the finite falsifier.
- Transfer certificate needed: A validator must certify equal regulated source derivatives for the class, cutoff-uniform K_c and T_tail intervals, and reflection-positive same-theory regulator data before the observation affects proof obligations.

## Next Experiment

Proof search plus validator-facing endpoint computation: instantiate the heat-kernel SU(N) three-hairpin source classes, vary alpha in the positive-D stress case, compute the seven-point connected cumulant witness intervals, certify T_tail, and decide I_gate.

# Annular plateau certificate for the flowed Wilson endpoint polarization

## Candidate Lemma

Conditional finite Route A theorem: if the Ward/cusp-subtracted connected four-curvature sectors obey a certified annular plateau bound and the same-theory recovery error is below the dominance margin, then the flowed Wilson endpoint polarization R_{++}^{ren} beats the Schur-Feshbach leakage L_+ and promotes finite endpoint-box positivity after H,K. This does not claim continuum YM existence, OS reconstruction, observable density, or a Hamiltonian mass gap.

## Definitions

- source object: finite-cutoff SU(N) Wilson Yang-Mills measure on a four-torus with gradient-flowed connection A_t, two centered renormalized plus-hairpin Wilson observables, and H,K endpoint sheet currents.
- target object: finite H,K Schur-Feshbach plus-channel endpoint-box positivity margin Delta_R^- for the already finite matrix problem.
- controlled interface: recovery map Rec_{a,t} from raw thin hairpin loops to endpoint sheet currents, preserving gauge, color, reflection, orientation, and centered cumulants up to epsilon_rec.
- same-theory condition: all expectations, subtractions, recovery errors, and endpoint currents are computed in the same cutoff Wilson measure and same flow normalization; no continuum or OS spectral transfer is invoked.
- bridge observable: R_{++}^{ren} is the covariance of two centered flowed plus-hairpins after disconnected-product, perimeter, and cusp subtraction.
- sector constants: A_{s,J}^+ bound Ward-Hessian remainders for sectors s in {3g,4g,ct,end} on dyadic annulus J.
- hard gate changed: finite endpoint-box positivity after H,K; all Clay gates remain untouched.

## Assumptions

- Model: compact SU(N), N>=2, finite volume V, lattice cutoff a, Wilson action, and gauge-covariant gradient flow at time t.
- Regime: endpoint box diameter eta, endpoint separation d0, and flow radius obey a << sqrt(8t) << d0 with eta/d0 <= eta0.
- Cutoff: constants are finite-cutoff and may depend on the chosen regulator window; no a->0 uniformity is asserted here.
- Same-theory: raw hairpins, flowed fields, counterterms, and endpoint currents use one bare measure and one renormalization prescription.
- Uniformity: plateau ratios q_s^*<1 are certified by outward-rounded interval bounds on a nonempty annular window.
- Local: all Taylor remainders are localized to the H,K endpoint cells plus summable dyadic annuli.
- Constraint: plus-channel endpoint currents have zero monopole and dipole moments after Ward/cusp subtraction.
- Validity: E_{>=6}^+ and epsilon_rec^+ are explicit upper intervals, not heuristic error bars.

## Equations

- centered flowed cumulant defining R: `\widehat W_+(t)=W_+^{\rm flow}(t)-\langle W_+^{\rm flow}(t)\rangle_{a,V},\qquad R_{++}^{\rm ren}=\kappa_2^{a,V}(\widehat W_+^{\rm ren}(t),\widehat W_+^{\rm ren}(t))`. Valid when: Valid when the two plus hairpins are centered after the same flowed Wilson renormalization in the finite cutoff theory.
- pair plus connected four-curvature decomposition: `R_{++}^{\rm ren}=g_t^4 (N^2-1)\{2G_{++}-N C_{4,++}^{\rm WS}\}+E_{\ge6}`. Valid when: Applies after disconnected-product, one-hairpin perimeter, and cusp subtractions in the small endpoint-sheet expansion.
- plus-moment Ward-Hessian reduction: `\sum_{e\in E_+}q_e=0,\quad \sum_{e\in E_+}q_e x_e=0\ \Longrightarrow\ |C_{4,++}^{\rm WS}|\le M_{2,+}^2\,\mathcal A_4^+`. Valid when: Requires Ward cancellation and plus-channel monopole-dipole cancellation for the endpoint sheet currents.
- annular plateau compression: `\mathcal A_4^+(J_*)=\sum_s\left(\sum_{J=0}^{J_*}A_{s,J}^+ + {A_{s,J_*+1}^+\over 1-q_s^*}\right),\qquad q_s^*<1`. Valid when: Valid when adjacent outward-rounded annular Hessian intervals prove a geometric tail ratio below one.
- finite dominance margin: `\Delta_R^-:=g_t^4(N^2-1)\{2G_{++}^- -N M_{2,+}^2\mathcal A_4^+(J_*)\}-E_{\ge6}^+-\epsilon_{\rm rec}^+-L_+`. Valid when: Valid for the finite H,K plus channel after the same recovery map and leakage L_+ are fixed.
- promotion implication: `\Delta_R^->0\ \Longrightarrow\ Q_+^{\rm ren}\ge Q_+^{\rm bare}+\Delta_R^->0`. Valid when: Applies only to the finite endpoint-box Schur-Feshbach matrix with the certified R correction inserted.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: finite-cutoff SU(N) Wilson Yang-Mills measure on a four-torus with gradient-flowed connection A_t, two centered renormalized plus-hairpin Wilson observables, and H,K endpoint sheet currents.; target object: finite H,K Schur-Feshbach plus-channel endpoint-box positivity margin Delta_R^- for the already finite matrix problem.; Model: compact SU(N), N>=2, finite volume V, lattice cutoff a, Wilson action, and gauge-covariant gradient flow at time t..
- Conceptual pressure attacked: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator, while connected C4 can erase the positive flowed pair covariance.
- Freeze the Clay claim level: all work is finite-cutoff, finite-volume, and endpoint-local; OS/Wightman reconstruction, nontrivial continuum limit, and Hamiltonian spectral gap are not claimed.
- Define R_{++}^{ren} as the same-theory centered flowed Wilson hairpin covariance; use disconnected-product, perimeter, and cusp cancellation before expanding in endpoint sheet currents.
- Compute the explicit pair contribution from two curvature pairings: color factor 2(N^2-1) and positive geometry G_{++} for nondegenerate plus hairpins.
- Represent the connected boundary-OPE polarization by sector kernels s in {3g,4g,ct,end} with color factor N(N^2-1), then apply Ward identities and plus-channel zero monopole/dipole moments.
- Taylor expand each sector kernel around endpoint cell centers; moment cancellation removes constant and linear terms, leaving a mixed-Hessian majorant multiplied by M_{2,+}^2.
- Partition the complement of the near endpoint cells into dyadic annuli; bound finite near annuli by interval quadrature and compress the far tail by a certified plateau ratio q_s^*<1.
- Subtract E_{>=6}^+, epsilon_rec^+, and L_+ to obtain Delta_R^-; positivity promotes finite endpoint-box positivity, while certified nonpositivity quarantines only this R repair.

Blocking gap: The missing proof object is a regulator-stable outward-rounded table of sector constants A_{s,J}^+, plateau ratios q_s^*, recovery error epsilon_rec^+, and pair lower bound G_{++}^- for the concrete H,K endpoint geometry.

## Falsifiers

- falsifier: Ward or cusp subtraction leaves a first-moment term, destroying the Hessian eta^2 suppression.
- falsifier: an annular sector has q_s^*>=1 in every admissible flow window, so the tail is not summable by plateau compression.
- falsifier: the positive pair geometry G_{++}^- vanishes for the concrete H,K hairpin orientation.
- falsifier: epsilon_rec^+ is not computed in the same Wilson measure, making the endpoint-current carrier representation-limited and invalid.
- falsifier: Delta_R^-<=0 with narrow intervals, quarantining the endpoint R repair while leaving the finite Schur-Feshbach theorem valid.
- Stress case: take eta close to the flow radius so Taylor remainders compete with pair positivity; the branch must demote unless the interval still proves dominance.

## Learning

Declarative tension: finite Schur-Feshbach endpoint positivity, positive same-theory flowed Wilson pair covariance, and recovery from raw hairpins must jointly hold, yet connected C4 may erase R_{++}. The raw Wilson-contour carrier is fragmented; global OS spectral transfer, area-law intuition, and a broad same-theory nontriviality witness route are too coarse for this finite obstruction. Endpoint sheet currents are efficient if they encode H,K sheets, endpoint moments, sector kernels, counterterms, recovery errors, and L_+; preserve gauge, color, reflection, orientation, cutoff, locality, and same-theory invariants; use cumulant expansion, Ward/cusp subtraction, Taylor Hessian remainders, heat-kernel majorants, dyadic tail compression, outward-rounded interval algebra, and zero-pairing quotienting; keep finite endpoint-cell locality plus summable annuli; transfer only through centered flowed Wilson cumulants; and demote on any falsifier. Conceptual value signal: R_{++}/kappa_4 is now a plateau-testable annular dominance margin, not a symbolic boundary-OPE term. Hard gate: finite endpoint-box positivity after H,K; success promotes one finite Route A gate, failure quarantines this repair while every Clay commitment remains unclaimed.

## Gedanken Experiment Design Seed

- Need decision: `Design and use now as a falsifier probe before another abstraction cycle.`
- Rationale: The branch is stuck only if R_{++} remains a symbolic boundary-OPE term; a concrete plateau quadrature can promote or quarantine the finite endpoint-box gate without touching Clay claims.
- Situation seed: On a finite four-dimensional SU(3) Wilson lattice, place the concrete H,K plus-hairpin endpoint sheets in a fixed small endpoint box, flow to time t, subtract perimeter/cusp terms, and evaluate the Ward-Hessian sector kernels on dyadic annuli around the endpoint cell.
- Varied variable: Vary the dimensionless flow-to-separation ratio tau=8t/d0^2 across an admissible window while keeping the H,K geometry fixed.
- Held-fixed controls: Same bare Wilson action, volume window, gauge group SU(3), and gradient-flow definition., Same H,K endpoint sheet currents, plus-channel orientation, and zero-moment normalization., Same disconnected-product, perimeter, cusp, and Ward subtraction scheme., Same Schur-Feshbach leakage L_+ and same endpoint-cell partition depth.
- Expected observation: Either adjacent annular ratios stabilize below q_s^*<1 and Delta_R^-(tau)>0 on a plateau, or a narrow negative interval provides a valid falsifier for the endpoint repair.
- Transfer certificate needed: Outward-rounded interval quadrature for G_{++}, A_{s,J}, E_{>=6}, and epsilon_rec, plus a same-theory recovery proof from raw hairpins to endpoint currents; only then may the observation enter proof obligations.

## Next Experiment

Proof search: perform outward-rounded annular quadrature for the concrete H,K plus-hairpin sectors s={3g,4g,ct,end}, compute the plateau ratios q_s^*(tau), the pair lower bound G_{++}^-, recovery error epsilon_rec^+, and Delta_R^-. Include the validator-facing marker connected cumulant witness / same-theory nontriviality witness only as a finite same-theory cumulant check, not as an OS spectral claim; route to quarantine if the certified dominance margin is nonpositive.

# Raw signed-orbit K4 recovery for finite H,K endpoint stress

## Candidate Lemma

Finite signed-orbit admissibility theorem: for one heat-kernel cutoff endpoint box, exact raw plaquette-orbit intervals for the connected four-curvature cumulant give a valid two-sparse falsifier of the post-H,K Schur-corrected endpoint compression whenever a phased off-diagonal lower bound exceeds the diagonal upper-product bound. Survival of the test is not positivity; it only forces full Delta_raw proof search.

## Definitions

- source object: finite heat-kernel regularized SU(N) Wilson endpoint box with oriented plaquette sheets S_i, transported curvature insertions, vacuum/perimeter subtraction, and raw connected four-curvature cumulant intervals.
- target object: Hermitian two-endpoint Schur-corrected compression U^{(2)}_{pq,\sigma} of the finite post-H,K endpoint quadratic form on span{e_p,e_q}.
- controlled interface: exact Wilson signed-orbit quotient mapping raw plaquette quadruples to multiplicities, phases, color tensors, and interval cumulants before Schur subtraction.
- same-theory condition: one cutoff a, one heat-kernel scale sigma, one coupling g_R, one gauge group SU(N), one endpoint H,K basis, and one OPE normalization are used for Gaussian, K4, OPE, and Schur terms.
- bridge observable: Q_i is the transported endpoint sheet flux whose vacuum-subtracted quadratic Wilson coefficient defines the connected cumulant witness R_{ij,\sigma}.
- hard gate: L_{pq}(theta)^2>D_p^+D_q^+ demotes only the finite H,K endpoint route; failure of the gate leaves the endpoint question undecided.

## Assumptions

- Model: finite four-dimensional hypercubic heat-kernel cutoff for SU(N) Wilson observables; no continuum Yang-Mills field is asserted.
- Cutoff: a>0 and sigma>=a are fixed, and all plaquette sheets and transport paths lie inside one finite reflected endpoint box.
- Same-theory: the Gaussian covariance, raw K4 cumulant intervals, OPE error, and S_HK Schur block are computed with the same regulator, basis, and coupling.
- Validity: each signed orbit interval is a rigorous enclosure of the connected four-curvature cumulant after disconnected vacuum/perimeter pieces have been cancelled.
- Local: the H,K collar/hairpin Schur block is finite dimensional and QHQ is strictly positive on the eliminated hairpin sector.
- Constraint: if a diagonal upper interval D_p^+ is negative the route is already falsified; otherwise D_p^+,D_q^+ are used only as conservative PSD-test bounds.

## Equations

- endpoint sheet flux: `Q_i=\sum_{P\in S_i} w_i(P)\,\operatorname{Tr}\big(T^{a_P}U_{\gamma_P}F_PU_{\gamma_P}^{-1}\big)`. Valid when: Valid when the endpoint sheet S_i is finite, transported plaquette curvatures use the heat-kernel regulator, and the chosen paths remain inside the fixed H,K endpoint box.
- connected boundary polarization decomposition: `R_{ij,\sigma}=\alpha_N g_R^4\,(C_{ij,\sigma}\circ C_{ij,\sigma})+\frac{g_R^4}{16N^2}K^{(4)}_{ij,\sigma}+E^{\mathrm{OPE}}_{ij,\sigma},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid after vacuum and perimeter subtractions in the same heat-kernel cutoff, with the Wilson boundary OPE truncated at the stated endpoint-box error.
- signed raw K4 orbit recovery: `K^{(4)}_{pq,\sigma}\in \sum_{o\in\mathcal O_{pq}} m_o e^{i\phi_o}[\ell_o,u_o]`. Valid when: Applies when the orbit set is obtained by exact Wilson trace identities, orientation symmetries, color contractions, and no sign-erasing shell quotient.
- two-sparse stress falsifier: `L_{pq}(\theta)^2>D_p^+D_q^+\;\Longrightarrow\; U^{(2)}_{pq,\sigma}\not\succeq0`. Valid when: Requires Hermitian endpoint compression, rigorous phased lower bound L_{pq}(theta)<=|U_{pq}|, and rigorous diagonal upper bounds for the same Schur-corrected matrix.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Observable Density In The Excitation Sector; source object: finite heat-kernel regularized SU(N) Wilson endpoint box with oriented plaquette sheets S_i, transported curvature insertions, vacuum/perimeter subtraction, and raw connected four-curvature cumulant intervals.; target object: Hermitian two-endpoint Schur-corrected compression U^{(2)}_{pq,\sigma} of the finite post-H,K endpoint quadratic form on span{e_p,e_q}.; Model: finite four-dimensional hypercubic heat-kernel cutoff for SU(N) Wilson observables; no continuum Yang-Mills field is asserted..
- Start with the heat-kernel Wilson boundary OPE for the endpoint observables and expand the vacuum-subtracted two-point coefficient into Gaussian crossed curvature contractions plus the connected four-curvature cumulant K4 plus an OPE interval.
- Use color trace identities in SU(N) to isolate the Gaussian PSD term with coefficient alpha_N=(N^2-1)/(8N^2); disconnected vacuum and perimeter pieces cancel before the connected cumulant witness is formed.
- Represent every raw K4 plaquette quadruple by an exact signed orbit o carrying multiplicity m_o, phase phi_o, color tensor contraction, and a rigorous interval [ell_o,u_o]. This is stronger than A012 shell compression because it preserves the phased real part.
- Add the OPE interval and subtract the same-basis Schur block S_HK to obtain interval enclosures for U_pp,U_qq and a phased lower bound L_pq(theta) for |U_pq|.
- Apply the necessary PSD condition for a Hermitian 2x2 principal compression: |U_pq|^2<=U_pp U_qq. If L_pq(theta)^2>D_p^+D_q^+, a two-sparse Rayleigh vector gives x^*Ux<0, so finite endpoint PSD fails.

Blocking gap: No actual same-regulator raw signed K4 orbit intervals [ell_o,u_o] have been produced for the H,K endpoint geometry; without them L_pq(theta) is only a formal recovery map.

## Falsifiers

- falsifier: a same-regulator raw K4 orbit computation yields L_pq(theta)^2>D_p^+D_q^+ for some endpoint pair, killing the finite H,K endpoint PSD route.
- falsifier: exact Wilson quotient auditing changes an orbit phase or multiplicity, invalidating the signed-orbit recovery map.
- falsifier: OPE error intervals exceed the Gaussian-Schur margin for every pair, making the two-sparse stress gate non-informative.
- falsifier: the K4 intervals come from a different regulator, coupling, volume, or endpoint basis, breaking the same-theory condition.
- If all signed-orbit stress tests survive but the full Delta_raw Loewner lower bound is not positive, the branch is undecided and must remain quarantined.

## Learning

Conceptual pressure attacked: R must be an actual same-theory connected cumulant witness, not scalar endpoint rhetoric or a gauge-invariant observable density restatement. Declarative tension: Wilson/OPE data, raw non-Gaussian K4, OPE error, and S_HK must jointly control one finite endpoint quadratic form in one cutoff theory, while OS reconstruction, nontrivial continuum YM, excitation-sector cyclicity, and mass gap claims are barred. Carrier critique: scalar R is too weak, A012 shells are sign-losing, full Delta_raw is complete but expensive, and signed raw orbits are the sharp negative carrier because they preserve phases. Conceptual value signal: the result is route-changing at finite scope because it gives a valid hard gate that either produces a finite falsifier or forces full Delta_raw proof search without touching Clay-level commitments.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe before any further abstraction.`
- Rationale: The branch is looping unless the connected boundary-OPE polarization is tested by actual same-regulator signed K4 intervals rather than scalar R, A012 shells, or OS Hilbert observable algebra language.
- Situation seed: Heat-kernel regulated SU(N) finite endpoint box for the worked H,K collar/hairpin geometry; choose two reflected Wilson sheet endpoints p,q and enumerate raw plaquette-quadruple orbits contributing to K^{(4)}_{pq,\sigma}.
- Varied variable: Phase-coherence parameter theta for the signed-orbit off-diagonal lower bound, with a secondary scan over sigma/a only after exact quotient invariance is verified.
- Held-fixed controls: Gauge group SU(N), cutoff a, heat-kernel scale sigma for each scan point, and renormalized coupling g_R., The H,K endpoint basis, Schur block S_HK, Wilson transport paths, OPE normalization, and vacuum/perimeter subtraction., Exact Wilson quotient policy and Hermitian interval arithmetic rules.
- Expected observation: If a small signed orbit family is phase coherent, L_pq(theta)^2 will exceed D_p^+D_q^+ and give a concrete finite falsifier; if phases cancel, the negative tactic fails and the proof queue moves to full Delta_raw.
- Transfer certificate needed: A validator-facing connected cumulant witness: exact orbit list, multiplicities, phases, color factors, interval K4 bounds, OPE interval, Schur data, and a proof that all were computed in the same regulated theory.

## Next Experiment

Proof search: build the validator-facing connected cumulant witness for one endpoint pair p,q by enumerating raw signed K4 Wilson orbits, computing same-regulator intervals, and testing L_pq(theta)^2>D_p^+D_q^+; if missing, quarantine this abstraction and run full Delta_raw interval search.

