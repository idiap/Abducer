# cycle-0326

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint connected-cumulant leakage screen for finite Wilson OS gate

## Candidate Lemma

Root-quartic leakage cap: for the heat-kernel endpoint-box regulator, the post-H,K endpoint polarization is bounded below by a same-theory connected cumulant witness interval; only positive-D endpoint leakage can reduce the finite OS scalar.

## Definitions

- source object: heat-kernel regulated SU(N) endpoint-box Wilson source functionals Z_c(s;a,L) for the fixed three-hairpin reflected collar block.
- target object: the finite post-H,K reflected-Wilson OS transfer scalar I_gate for that same finite block.
- controlled interface: source-equivalent connected cumulant witness intervals are aggregated with signed endpoint incidences and passed as a scalar interval to the finite OS gate.
- same-theory condition: the Wilson loop normalization, endpoint source insertion, reflection map, and cutoff limit are identical to the collar observables; no boundary counterterm or auxiliary boundary Hilbert sector is introduced.
- carrier: C_ep=(source classes c, seven values F_c(kh), incidence D_c, color factor C_N, Gaussian margin M_G, tail tau_tail).
- declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular endpoint boundary OPE must coexist, but raw R forgets incidence signs and raw kappa_4 overstates danger.

## Assumptions

- Model: four-dimensional Euclidean SU(N) lattice Yang-Mills with heat-kernel plaquette action and reflected Wilson plaquette-sheet endpoint boxes.
- Regime: endpoint boxes are smaller than the collar scale, and the source strength h lies inside the analytic heat-kernel chart.
- Uniformity: M_{8,c}, epsilon_c, and tau_tail are bounded independently of the cutoff along the finite Route A block.
- Same-theory: source derivatives are taken in the original Wilson Schwinger family, so the connected cumulant witness is not a boundary-renormalized theory.
- Validity: Wick-square Gram terms have already been removed by connected logarithms, and straight f f contacts cancel by the null-channel incidence identity.

## Equations

- seven_point_connected_cumulant_interval: `F_c(s)=\log Z_c(s),\quad \kappa_c\in \frac{-F_c(-3h)+12F_c(-2h)-39F_c(-h)+56F_c(0)-39F_c(h)+12F_c(2h)-F_c(3h)}{6h^4}+[-7h^4M_{8,c}/240,7h^4M_{8,c}/240]`. Valid when: Valid when the endpoint source family is analytic on the seven-point stencil disk and the eighth source derivative is uniformly bounded.
- haar_root_quartic_screen: `\kappa_c=-A_c+e_c,\quad A_c=\frac{t_c^4}{60}R_4(L_c),\quad R_4(L)=N\operatorname{tr}(L^4)+3(\operatorname{tr}(L^2))^2,\quad |e_c|\le \epsilon_c`. Valid when: Valid when heat-kernel endpoint coordinates are used before cutoff removal and non-Haar interaction remainders are absorbed in epsilon_c.
- signed_endpoint_gate: `I_{\mathrm{gate}}\in M_G+C_N\sum_c D_c\kappa_c+[-\tau_{\mathrm{tail}},\tau_{\mathrm{tail}}],\quad D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}`. Valid when: Valid when source-equivalent endpoint boxes are aggregated before clipping and all off-class locality errors are charged to tau_tail.
- conservative_promotion_screen: `I_-:=M_G-C_N\sum_c\big([D_c]_+A_c+|D_c|\epsilon_c\big)-\tau_{\mathrm{tail}}>0\ \Longrightarrow\ I_{\mathrm{gate}}>0`. Valid when: Valid when C_N is positive in the singlet channel and the root-quartic cap bounds every same-theory connected endpoint cumulant interval.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: heat-kernel regulated SU(N) endpoint-box Wilson source functionals Z_c(s;a,L) for the fixed three-hairpin reflected collar block.; target object: the finite post-H,K reflected-Wilson OS transfer scalar I_gate for that same finite block.; Model: four-dimensional Euclidean SU(N) lattice Yang-Mills with heat-kernel plaquette action and reflected Wilson plaquette-sheet endpoint boxes..
- Start from the heat-kernel plaquette-sheet endpoint partition function Z_c(s) with source sL_c inserted in the same Wilson sheet used in the collar block.
- Take F_c=log Z_c; the fourth source derivative is the connected four-flux endpoint cumulant, so Gaussian Wick-square contractions are absent in kappa_c.
- Use the compact-group heat-kernel chart near the endpoint identity to isolate the Haar-Jacobian root-quartic term -t_c^4 R4(L_c)/60 and put all non-Haar interaction and chart errors into epsilon_c.
- Use the already established null-channel cancellation of straight C_A f f contacts, leaving only endpoint classes and the tail budget.
- Aggregate all source-equivalent boxes, form D_c=2b12-4b13-4b23, and multiply intervals after aggregation.
- Bound D_c(-A_c+e_c) below by -[D_c]_+A_c-|D_c|epsilon_c; add M_G and subtract tau_tail to obtain the conservative promotion screen.

Blocking gap: The missing analytic input is a cutoff-uniform epsilon_c and tau_tail for the actual positive-D source classes, or the seven-point source data needed to replace the conservative cap by a tight interval.

## Falsifiers

- A certified positive-D endpoint source class has I_+<0 after exact interval multiplication; this is a finite same-theory falsifier of the post-H,K OS transfer block.
- The eighth-derivative or chart-remainder bound grows with the cutoff, so the endpoint connected cumulant witness is not uniform.
- A boundary counterterm is required to define Z_c(s) at the reflected endpoint, violating the same-theory condition.
- Endpoint source equivalence collapses boxes with different Wilson normalization or reflection images, producing an invalid carrier.
- The tail budget contains long-range topology or large-field contributions not localized near endpoint boxes.

## Learning

Cycle 326 attacks the conceptual pressure of endpoint collapse inside the same Wilson theory. Declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must coexist without a boundary theory, while raw R is representation-limited, raw kappa_4 spectra are too strong, and global Schur-preimage positivity is valid but too coarse after H,K. The new finite contribution is a conservative root-quartic leakage cap for the connected cumulant witness. It is sharp at its scope because negative SU(N) endpoint cumulants are not the obstruction; only positive-D leakage times same-theory cumulants plus a uniform tail can demote the finite gate. Clay continuum construction, nontriviality, full OS/Wightman reconstruction, and positive mass gap remain non-claimed.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe and analytic screen.`
- Rationale: The branch is data-waiting; varying a single endpoint-overlap parameter tests whether the root-quartic leakage cap is genuinely sharp or merely a restatement of quarantine.
- Situation seed: Heat-kernel regulated SU(N) three-hairpin endpoint block with one source class c carrying a fixed connected cumulant witness kappa_c=-A+e and footprint fractions b12, b13, b23.
- Varied variable: The endpoint overlap ratio eta=(b13+b23)/b12, varied across the half-overlap boundary eta=1/2 while keeping b12 and source L fixed.
- Held-fixed controls: Same Wilson plaquette-sheet regulator and source stencil F_c(kh) for k=-3,...,3., Fixed H,K finite block, positive Gaussian margin M_G, color factor C_N, and null-channel vector., No boundary counterterm, no gauge fixing change, and no enlargement of the gauge-invariant Wilson algebra.
- Expected observation: For eta>=1/2 the root-quartic negative cumulant cannot lower the gate through this class; for eta<1/2 the lower bound decreases linearly in b12(1-2eta) and can expose a finite falsifier if it beats M_G and tau_tail.
- Transfer certificate needed: A validator-facing table of regulated source values, fractional endpoint incidences, epsilon_c, and tau_tail proving the observation is cutoff-uniform and same-theory valid.

## Next Experiment

Proof search plus validator-facing endpoint computation: enumerate source-equivalent positive-D endpoint classes, evaluate the seven heat-kernel source values, certify epsilon_c and tau_tail, and test the connected cumulant witness interval I_gate.

# Gauge-Invariant Nontriviality Witness Selection: annular R++ tail certificate

## Candidate Lemma

Conditional annular Ward-Hessian compression: after Ward/cusp subtraction and plus-channel moment cancellation, the far connected C4 contribution to the flowed Wilson endpoint polarization is bounded by a geometric tail with ratio q_s=2^{4-2nu_s}. A positive certified margin promotes only finite endpoint-box positivity after H,K.

## Definitions

- source object: finite H,K endpoint sheet-current data J_+ on endpoint cells, the SU(N) Wilson lattice regulator at spacing a, gradient-flow time t>0, and centered flowed Wilson hairpin observables W_t(J).
- target object: a lower interval Delta_R^- for the finite Schur-Feshbach endpoint-box quadratic form R_{++}^{ren}-L_+ in the plus channel.
- controlled interface: the centered same-theory flowed Wilson cumulant kappa_2(W_t(J_+),W_t(J_+)) expanded into pair and connected four-curvature sector kernels.
- same-theory condition: the flow, counterterms, endpoint recovery map, and cumulant normalization are taken on the same cutoff sequence and continuum Schwinger family; no change of theory or external spectral model is allowed.
- Endpoint moment M_{2,+}: the certified second absolute moment of the plus endpoint current after monopole and dipole cancellation.
- Sector s: one connected C4 kernel sector among 3g, 4g, counterterm, and endpoint-recovery sectors with mixed Hessian decay exponent nu_s.

## Assumptions

- Model: four-dimensional SU(N) lattice Yang-Mills with Wilson action, gauge-invariant gradient-flow observables, and endpoint point-splitting before a->0.
- Regime: endpoint boxes have diameter eta, far annuli start at r0>=max(4 sqrt(8t),4 eta), and sector Hessian exponents satisfy nu_s>2.
- Cutoff: the mixed Hessian constants A_s^+(t,r0,a) and near-cell constants H_s^+(t,a) are bounded uniformly on the selected cutoff window.
- Same-theory: the raw Wilson hairpins and endpoint sheet currents are related by a recovery map with error epsilon_rec^+ inside the same flowed Wilson cumulant family.
- Validity: Ward identities remove monopole terms, cusp counterterms remove one-hairpin divergences, and plus-channel symmetry removes dipole terms before the Hessian Taylor remainder is used.
- Constraint: L_+ is the fixed Schur-Feshbach leakage from the previously certified finite H,K theorem and is not refit after R_{++} is estimated.

## Equations

- flowed endpoint polarization decomposition: `R_{++}^{ren}=g_t^4(N^2-1)\left(2G_{++}-N\sum_s C_{s,++}^{WS}\right)+E_{\ge 6}+E_{rec}`. Valid when: Valid when centered flowed Wilson hairpins are expanded to fourth curvature order after Ward, cusp, and one-hairpin subtraction in the same cutoff theory.
- dyadic annular tail compression: `|C_{s,++}^{far}|\le A_s^+ M_{2,+}^2\, r_0^{4-2\nu_s}\,(1-2^{4-2\nu_s})^{-1}`. Valid when: Valid when the mixed Hessian sector kernel obeys the annular decay bound with exponent nu_s greater than two and endpoint plus moments cancel through first order.
- near-far lower interval: `R_{++}^- = g_t^4(N^2-1)\left(2G_{++}^- - N\sum_s\left(H_s^+M_{2,+}^2+A_s^+M_{2,+}^2\frac{r_0^{4-2\nu_s}}{1-2^{4-2\nu_s}}\right)\right)-E_{\ge6}^+-\epsilon_{rec}^+`. Valid when: Applies after outward-rounded interval bounds for near cells, far annuli, recovery errors, and sixth-order Wilson remainders are all certified on the same regulator window.
- finite endpoint-box promotion margin: `\Delta_R^-:=R_{++}^- - L_+\quad;\quad \Delta_R^->0`. Valid when: Valid as a Route A finite positivity certificate only when L_+ is the unchanged Schur-Feshbach leakage and all interval inputs are cutoff-stable.

## Attempted Derivation

- Attack conceptual pressure: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator, but the connected C4 boundary polarization can erase the positive pair covariance.
- Freeze the hard gate: finite endpoint-box positivity after H,K; success promotes one finite Route A gate, failure quarantines the R repair, and all Clay gates remain untouched.
- Use endpoint sheet currents because raw Wilson contours are fragmented; compare against global OS spectral transfer and non-Gaussian Schwinger-family routes, which are too coarse for this finite obstruction.
- Expand the centered flowed Wilson covariance into a positive two-curvature pair baseline with color 2(N^2-1) and connected C4 sectors with color N(N^2-1).
- Apply disconnected-product subtraction and one-hairpin perimeter/cusp subtraction; then Ward identities and plus-channel symmetry remove monopole and dipole endpoint moments.
- Taylor expand each far sector kernel on dyadic annuli; the first surviving term is controlled by mixed Hessian bounds and M_{2,+}^2.
- Sum shell bounds: shell_n contributes at most A_s^+ M_{2,+}^2 r_0^{4-2nu_s} 2^{(4-2nu_s)n}; for nu_s>2 this compresses to the geometric denominator 1-q_s.
- Combine near-cell interval constants, far-tail compression, sixth-order remainders, recovery errors, and the fixed leakage L_+ into Delta_R^-.
- Promotion requires Delta_R^->0 with cutoff-stable constants; demotion requires a valid negative upper margin or a structural falsifier such as failed Ward cancellation.

Blocking gap: The mixed Hessian constants A_s^+ and near constants H_s^+ for the interacting connected four-curvature sectors are not yet interval-certified from the actual flowed lattice/continuum kernels.

## Falsifiers

- Ward subtraction leaves a monopole or dipole endpoint term, making the Hessian annular tail invalid.
- A connected sector has nu_s<=2 or an unsummable logarithmic tail after counterterms.
- The zero-pairing quotient changes a retained pair or C4 sector pairing.
- The recovery error epsilon_rec^+ grows under cutoff refinement or flow-time plateau tests.
- The lower margin Delta_R^- is nonpositive with narrow certified intervals; this is a valid falsifier for the endpoint R repair.
- A positive margin exists only at one flow time and disappears on the same-theory plateau.

## Learning

Cycle 326 attacks the missing mediator between finite Schur-Feshbach positivity and same-theory Wilson cumulant positivity. The declarative tension is that endpoint positivity, positive flowed pair covariance, and raw-hairpin recovery must jointly be valid, while connected C4 can erase R_{++}. The carrier critique remains: raw contours are fragmented, and global OS or non-Gaussian routes are too coarse; endpoint sheet currents are efficient because Ward moments, mixed Hessians, dyadic tails, interval arithmetic, and zero-pairing guards become primitive. The sharp value signal is a concrete annular compression formula and dominance margin Delta_R^-, a route-deciding finite falsifier rather than a symbolic boundary-OPE term. Success changes only the finite endpoint-box gate; failure quarantines this R repair while Clay existence, OS/Wightman axioms, observable density, large-field/topology control, OS spectral transfer, nontrivial continuum limit, and mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and proof-search guide, not as evidence for the Clay theorem.`
- Rationale: The branch has compressed R_{++} into an annular certificate; the next learning comes from varying one concrete regulator-scale parameter and observing whether pair dominance is stable or artificial.
- Situation seed: SU(N) Wilson lattice Yang-Mills with gradient-flow time t, two fixed H,K plus-channel thin hairpin endpoint sheets in one endpoint box, centered flowed Wilson covariance used as the connected cumulant witness for R_{++}.
- Varied variable: The far-annulus start ratio alpha=r0/sqrt(8t), with r0 also constrained to exceed 4 eta.
- Held-fixed controls: Fixed H,K endpoint geometry, plus-channel orientation, color normalization, and Schur-Feshbach leakage L_+., Fixed same-theory Wilson action, gradient-flow observable definition, cusp/perimeter counterterms, and endpoint recovery map., Fixed Ward/cusp subtraction rules, zero-pairing quotient policy, and finite endpoint-cell refinement depth.
- Expected observation: If the route is viable, Delta_R^-(alpha) has a plateau where the positive pair baseline dominates near-cell and annular C4 majorants; if not, the certified upper margin stays negative or interval width fails to contract.
- Transfer certificate needed: A cutoff-uniform Ward-Hessian sector-constant certificate plus same-theory recovery bounds for the flowed Wilson cumulant before any intuition may enter proof obligations.

## Next Experiment

Route to proof search: compute certified annular constants A_s^+, near constants H_s^+, and recovery error epsilon_rec^+ for the centered flowed Wilson connected cumulant witness; then run the same-theory nontriviality witness boundary audit without claiming continuum OS spectral transfer.

# Signed-orbit raw K4 endpoint stress audit

## Candidate Lemma

Finite signed-orbit K4 stress lemma: in a fixed heat-kernel lattice cutoff, raw four-plaquette connected cumulant orbit intervals give a valid two-sparse falsifier of post-H,K endpoint PSD when L_pq(theta)^2>D_p^+D_q^+. Survival implies only full Delta_raw search.

## Definitions

- source object: finite heat-kernel lattice SU(N) Wilson/OPE data on the fixed H,K endpoint box: oriented plaquette sheets, transporters, raw connected four-curvature cumulant intervals, OPE intervals, and Schur blocks.
- target object: a finite Schur-corrected endpoint quadratic form U_sigma on vacuum-subtracted reflected Wilson endpoint states; target is PSD or a two-sparse negative stress vector, not a continuum mass gap.
- controlled interface: signed-orbit recovery map from raw plaquette K4 cumulant intervals to Re(e^{i theta}U_pq), then Rayleigh stress after Gaussian color square, OPE error, and S_HK subtraction.
- same-theory condition: identical cutoff a, heat-kernel scale sigma, coupling g_R, Wilson basis, reflection plane, transporters, and H,K Schur data are used for K4, OPE, Gaussian, and stress bounds.
- carrier: connected cumulant witness; scalar R is too weak, OS Hilbert observable algebra is too strong, A012 shells are quarantined, raw enumeration is fragmented but valid.

## Assumptions

- Model: finite heat-kernel regulated SU(N) lattice Yang-Mills on a fixed endpoint box with reflected Wilson loops and fixed H,K collar/hairpin truncation.
- Cutoff: a, sigma, volume, coupling, endpoint basis, reflection plane, and H,K Schur matrix are fixed; no continuum or infinite-volume uniformity is asserted.
- Same-theory: raw K4 intervals, Gaussian covariance, OPE bounds, and S_HK are computed from the same lattice measure and Wilson normalization.
- Validity: signed-orbit quotient uses only exact trace, orientation, reflection, and sheet symmetries; no A012 shell compression or OS Hilbert observable algebra is imported.
- Constraint: QHQ is positive and invertible on the retained hairpin sector, so S_HK=B^*E^{-1}B is finite.

## Equations

- raw-K4 orbit recovery: `K^{(4)}_{pq}=\sum_{o\in\mathcal O_{pq}}m_o\,\omega_o\,I_o,\quad I_o\ni \operatorname{cum}_4(\mathcal F_{o1},\mathcal F_{o2},\Theta\mathcal F_{o3},\Theta\mathcal F_{o4})`. Valid when: Valid when the heat-kernel cutoff, reflected Wilson endpoint sheets, vacuum/perimeter normal ordering, and exact transported plaquette representatives are fixed before taking connected cumulants.
- Schur-corrected endpoint entry: `U_{pq}=\alpha_N g_R^4(C\circ C)_{pq}+\frac{g_R^4}{16N^2}K^{(4)}_{pq}+E^{\mathrm{OPE}}_{pq}-S^{HK}_{pq},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after diagonal normalization and Schur subtraction are performed in the same finite endpoint basis and the OPE remainder has interval bounds.
- two-sparse demotion gate: `\tau_{pq}(\theta)=D_p^+D_q^+-L_{pq}(\theta)^2<0\ \Longrightarrow\ \exists x:\ x^*U_\sigma x<0`. Valid when: Requires Hermitian two-by-two endpoint compression with nonnegative diagonal upper bounds and a certified phased lower bound for the off-diagonal real part.

## Attempted Derivation

- Fix the heat-kernel cutoff and endpoint basis; expand each reflected Wilson endpoint as normal-ordered quadratic transported curvature flux plus an OPE interval.
- Use vacuum/perimeter cancellation: disconnected Wilson factors and one-point flux terms cancel, leaving crossed Gaussian square plus connected four-curvature cumulant K4.
- Recover K4 by exact signed orbits of oriented plaquette quadruples; interval-sum each orbit to bound Re(e^{i theta}U_pq).
- Apply the 2x2 Rayleigh test: if the off-diagonal lower bound overwhelms the diagonal upper product, a phase vector has negative Schur-corrected energy.

Blocking gap: No validator-certified same-regulator raw K4 orbit intervals exist yet for the fixed H,K endpoint pair.

## Falsifiers

- falsifier: the signed-orbit quotient changes a transported trace identity or loses Hermitian phase data, so recovered K4 intervals are not valid.
- falsifier: raw K4 intervals are too wide and give L_pq(theta)^2<=D_p^+D_q^+ for every endpoint pair and phase.
- falsifier: the heat-kernel regulator or Wilson normalization used for K4 differs from the Schur/OPE data, breaking the same-theory condition.
- falsifier: OPE or diagonal upper intervals are uncertified, so the two-sparse Rayleigh stress cannot be trusted.

## Learning

Conceptual pressure: R must be a connected cumulant witness, not OS-density rhetoric. Declarative tension: Wilson/OPE, raw K4, OPE error, and S_HK must share one cutoff while Clay gates are non-claims. Signed-orbit carrier is sharp but quarantined without raw intervals.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe, not as another abstraction cycle.`
- Rationale: The conceptual pressure is missing raw K4 evidence. The finite theorem is already shaped; only a concrete connected cumulant witness can decide whether the H,K endpoint route survives.
- Situation seed: Finite SU(3) heat-kernel lattice endpoint box with two H,K hairpin endpoints p,q; enumerate signed orbit representatives of four plaquettes crossing the reflection collar and compute interval cumulants.
- Varied variable: signed-orbit inclusion radius r around the endpoint collar
- Held-fixed controls: cutoff a, heat-kernel scale sigma, coupling g_R, volume, and reflection plane, fixed H,K Wilson endpoint basis, Schur block S_HK, OPE interval convention, and exact Wilson quotient policy
- Expected observation: If short signed orbits already give L^2>D_p^+D_q^+, the finite endpoint PSD is killed; if narrow intervals stay below threshold, full Delta_raw proof search becomes the valid next gate.
- Transfer certificate needed: A same-regulator raw cumulant interval certificate with exact orbit recovery, Hermitian phase bounds, vacuum/perimeter cancellation audit, and Schur/OPE data hash.

## Next Experiment

Proof search: compute the first same-regulator signed-orbit K4 intervals for one H,K endpoint pair; if absent, quarantine this carrier and backtrack to full Delta_raw or a new finite Wilson geometry.

