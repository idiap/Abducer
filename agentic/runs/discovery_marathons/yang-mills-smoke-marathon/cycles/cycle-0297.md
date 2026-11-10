# cycle-0297

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint-source interval quarantine for post-H,K Wilson boundary OPE

## Candidate Lemma

Endpoint-source interval gate. For the fixed heat-kernel regulated three-hairpin block after the H,K Schur-Feshbach reductions, the post-H,K endpoint contribution is a same-theory scalar interval. If all endpoint source classes and tails are cutoff-uniform, I_->=0 promotes this finite OS block, I_+<0 is a finite same-theory falsifier, and missing positive-D connected cumulant witness data forces quarantine.

## Definitions

- source object: heat-kernel plaquette-sheet endpoint source classes [v] with seven regulated log Z_v(s) values, fractional incidences b_ij(v), color factor C_N, Gaussian margin M_G, and tail interval T_tail.
- target object: the finite post-H,K reflected-Wilson OS gate scalar I_gate for the locked three-hairpin block, not the continuum mass-gap theorem.
- controlled interface: C_ep maps same-theory regulated endpoint source derivatives and signed incidences to a scalar interval [I_-,I_+] consumed by the finite Schur-Feshbach OS gate.
- same-theory condition: the Wilson loop normalization, endpoint source insertion, reflection map, and cutoff removal use the original gauge-invariant Wilson algebra with no boundary counterterm or algebra enlargement.
- representation morphism: pi_ep sends each endpoint box to its source-equivalence class, incidence vector (b12,b13,b23), cumulant interval, and locality charge.
- invariants preserved: Wilson normalization, reflection symmetry, null-channel cancellations, color singlet projection, and source-equivalence by equal regulated data.
- error budget: finite-difference error, endpoint-box truncation, and T_tail are the only admitted errors; no imported continuum OS spectral transfer is used.

## Assumptions

- Model: four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette-sheet regulator and normalized gauge-invariant Wilson observables.
- Regime: fixed finite H,K hairpin block after Wick-square Gram positivity and straight f f contact cancellation have already been verified.
- Uniformity: endpoint source derivative bounds and T_tail are uniform in the lattice spacing over the chosen endpoint classes.
- Same-theory: endpoint aggregation is allowed only by equal regulated source data, not by geometric resemblance or a boundary effective theory.
- Validity: the claim is a finite interval/quarantine theorem and does not construct continuum Schwinger functions, OS Hilbert space, or a positive mass gap.

## Equations

- signed endpoint incidence: `D_v=2b_{12}(v)-4b_{13}(v)-4b_{23}(v)`. Valid when: Valid when b_ij(v) are fractional heat-kernel endpoint overlaps for the fixed reflected Wilson hairpin block.
- source-equivalence compression: `u\sim v\iff (\ell_u(-3h),\ldots,\ell_u(3h))=(\ell_v(-3h),\ldots,\ell_v(3h)),\qquad D_{[v]}=\sum_{u\in[v]}D_u`. Valid when: Applies when equivalent endpoint boxes have identical regulated source data before any incidence contraction is performed.
- class contribution interval: `J_{[v]}=[\min(\kappa^-_{[v]}D_{[v]},\kappa^+_{[v]}D_{[v]}),\max(\kappa^-_{[v]}D_{[v]},\kappa^+_{[v]}D_{[v]})]`. Valid when: Requires cutoff-uniform connected fourth-cumulant intervals for the same source-equivalence class and fixed signed incidence.
- finite OS gate interval: `[I_-,I_+]=M_G+C_N\sum_{[v]}J_{[v]}+T_{\rm tail}`. Valid when: Valid after the H,K Schur-Feshbach reduction and the stated Wilson endpoint cancellations have isolated the endpoint contribution.
- forced quarantine condition: `D_{[v]}>0\ \text{and}\ [\kappa^-_{[v]},\kappa^+_{[v]}]\ \text{missing}\ \Longrightarrow\ \text{quarantine}`. Valid when: Valid when missing positive-incidence endpoint classes are the only undecided contributors to the finite gate interval.

## Attempted Derivation

- Attacked conceptual pressure: endpoint collapse must be sign-certified in the same Wilson theory rather than hidden in symbolic R.
- Declarative tension: finite collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint boundary OPE must coexist without adding a boundary theory.
- Fixed the heat-kernel plaquette-sheet regulator and kept the already established cancellations: Wick-square terms are positive Gram terms and straight f f contacts cancel in the null incidence channel.
- Replaced raw R by C_ep, because raw R is too weak to remember incidence signs and raw kappa_4 spectra are too strong since negative kappa_4 is harmless when D<=0.
- Compared abstraction routes: global Schur-preimage positivity is valid but too coarse after H,K; endpoint source intervals are local, computable, and export exactly one scalar to the finite OS gate.
- Compressed endpoint boxes only by equal regulated source data, then summed signed incidences before multiplying by connected cumulant intervals.
- Derived the class interval J_[v] and the finite gate interval [I_-,I_+]=M_G+C_N sum J_[v]+T_tail.
- Tried to promote using the half-overlap shield, but the shield eliminates only classes with D<=0 and certified nonpositive cumulants; it does not decide positive-D classes.

Blocking gap: No cutoff-uniform same-theory source derivative intervals are available for positive-D endpoint classes, and T_tail is not yet bounded sharply enough to decide [I_-,I_+].

## Falsifiers

- falsifier: a source-equivalence class with D_[v]>0, certified kappa_[v]^+<0, and tail small enough to make I_+<0 gives a finite same-theory OS determinant failure.
- A boundary counterterm needed to define the endpoint source derivative changes the Wilson algebra and invalidates the same-theory condition.
- Cutoff-nonuniform M8_v or T_tail prevents transfer of the endpoint interval to the post-H,K finite gate.
- Source-equivalence merging by geometry rather than equal regulated source values can reverse signed incidences and create a spurious valid interval.
- A positive connected cumulant in a D<0 class defeats the simplified half-overlap shield and forces full interval arithmetic.
- Large-field or topological endpoint sectors escaping T_tail control would demote the carrier before any OS conclusion.

## Learning

Cycle 297 converts quarantine into a precise theorem-level obstruction. The conceptual pressure is endpoint collapse in the same Wilson theory. The declarative tension is finite collar OS positivity plus fixed gauge-invariant Wilson observables plus singular connected endpoint OPE, with no boundary theory allowed. The current carriers are inadequate: raw R is representation-limited, raw kappa_4 spectra are too strong, and the global Schur-preimage test is valid but too coarse after H,K. The efficient representation is C_ep: endpoint source classes, seven source values, cumulant intervals, signed incidences, C_N, M_G, and T_tail; it preserves Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; it uses source differentiation, interval arithmetic, source-equivalence, color multiplication, clipping, incidence contraction, and tail addition; it exports only [I_-,I_+] to the finite OS gate. Hard gate changed: the finite post-H,K reflected-Wilson OS transfer gate can now be promoted, falsified, or quarantined by actual endpoint source data. Clay continuum construction, full OS/Wightman reconstruction, nontriviality, and positive mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe while the branch remains quarantined from promotion.`
- Rationale: The branch has exhausted abstract OS/Wilson restatements; the decisive unknown is a concrete connected cumulant witness for positive-D endpoint classes in the same heat-kernel Wilson theory.
- Situation seed: SU(N) heat-kernel lattice endpoint-box experiment for the fixed three reflected Wilson hairpins: compute seven same-theory source values log Z_v(kh) for a pure 12 endpoint class and for mixed 13/23 classes, then contract with D_v=2b12-4b13-4b23.
- Varied variable: fractional shield ratio alpha=(b13+b23)/b12 for a source-equivalence endpoint class, including alpha<1/2 12-dominant stress cases.
- Held-fixed controls: fixed H,K Schur-Feshbach hairpin block and null vector, heat-kernel plaquette-sheet regulator and normalized Wilson loop algebra, same SU(N) color factor C_N and singlet source insertion, no boundary counterterm, no gauge-fixed observable replacement, and no continuum mass-gap claim, uniform M8_v and T_tail bookkeeping across cutoff refinements
- Expected observation: For alpha>=1/2 and kappa_v<=0 the endpoint contribution is protective; for alpha<1/2 the sign of the certified fourth connected source cumulant decides whether the finite gate remains valid or yields a finite falsifier.
- Transfer certificate needed: A cutoff-uniform source-equivalence table, M8 remainder bound, and T_tail estimate proving that C_ep is the same-theory interface from regulated endpoint data to the finite OS gate.

## Next Experiment

Quarantine except for one validator-facing computation: in the heat-kernel plaquette-sheet regulator, compute the connected cumulant witness kappa_v=d_s^4 log Z_v(0) by the seven-point stencil for positive-D endpoint source classes, certify M8_v and T_tail, then feed [I_-,I_+] to the finite post-H,K OS gate.

# Gauge-Invariant Nontriviality Witness Selection -> finite endpoint R certificate

## Candidate Lemma

Ward-Hessian endpoint-cell certificate: for fixed H,K plus-channel endpoint currents, the connected boundary-OPE polarization term R_{++} has a computable lower interval once the Ward-subtracted four-curvature kernel has a cutoff-uniform Hessian bound and the recovery-map error is enclosed.

## Definitions

- source object: finite-volume four-dimensional SU(N) Wilson lattice Yang-Mills measure with cutoff a, gradient-flow time t, flowed curvature F_t, and fixed H,K plus endpoint sheet currents J_+^U,J_+^V supported in endpoint boxes U,V.
- target object: the scalar post-H,K Schur-Feshbach endpoint mediator R_{++}^{ren}(a,t;U,V) and its lower interval compared with the already finite leakage L_+.
- controlled interface: the centered flowed Wilson hairpin map J -> \widehat W_t(J), followed by the same cutoff connected cumulant kappa_2 and Ward/cusp-subtracted endpoint Taylor expansion.
- same-theory condition: W_t, counterterms, endpoint currents, recovery maps, and L_+ are all evaluated in the same cutoff Wilson theory before any continuum or OS spectral transfer claim.

## Assumptions

- Model: finite Route A endpoint block inside four-dimensional SU(N) Wilson lattice Yang-Mills with gradient-flow regulator; no continuum existence or mass-gap theorem is claimed.
- Regime: endpoint boxes have diameter eta, separation d>=8eta, and a<<sqrt(8t)<=eta/2 so flowed kernels are smooth on each endpoint cell.
- Same-theory: the centered hairpin observables, perimeter/cusp counterterms, H,K finite block, and Schur-Feshbach leakage L_+ use the same lattice measure and the same renormalized flow-time coupling g_t.
- Uniformity: near/far constants must be stable under a->0 at fixed physical eta,d,t; large-field summability and topological sector control remain hard frontier gates.
- Constraint: the plus endpoint current has certified zero monopole and dipole moments after discretization, so Ward and cusp cancellation remove constant and linear endpoint Taylor terms.

## Equations

- centered flowed hairpin carrier: `\widehat W_t(J)=Z_{\rm hp}^{-1}(a,t)\bigl(W_t(J)-\langle W_t(J)\rangle_{a,L}\bigr)`. Valid when: Valid when the flowed Wilson hairpin and its one-hairpin perimeter/cusp normalization are defined in the same finite cutoff measure.
- endpoint R cumulant: `R_{++}^{\rm ren}(a,t;U,V)=\kappa_2\bigl(\widehat W_t(J_+^U),\widehat W_t(J_+^V)\bigr)`. Valid when: Valid when both centered hairpins are separated by reflection-compatible endpoint boxes and use the same gradient-flow regulator.
- positive pair baseline: `G_{++}=\int_{U\times V}J_{+,\mu\nu}^{U,b}(x)\,\mathcal P_{t,\mu\nu;\rho\sigma}(x-y)\,J_{+,\rho\sigma}^{V,b}(y)\,dx\,dy\ge G_{++}^{-}`. Valid when: Valid after color-diagonal flowed two-curvature contraction and endpoint-cell interval enclosure of the fixed H,K geometry.
- color decomposition through order g_t^4: `R_{++}^{\rm ren}=g_t^4(N^2-1)\{2G_{++}+N C_{4,++}^{\rm WS}\}+E_6+E_{\rm rec}`. Valid when: Valid in the perturbative flowed cumulant expansion after disconnected products and one-hairpin perimeter/cusp divergences are subtracted.
- Ward-Hessian polarization bound: `|C_{4,++}^{\rm WS}|\le H_4^{+}(t,a,U,V;\rho)\,M_{2,+}(U)M_{2,+}(V)+C_{\rm ct}^{+}\epsilon_{\rm cusp}`. Valid when: Valid when Ward-subtracted sector kernels have certified endpoint Hessian bounds and plus-current monopole and dipole moments vanish.
- certified lower interval: `R_{++}^{I,-}=g_t^4(N^2-1)\bigl(2G_{++}^{I,-}-N H_4^{I,+}M_{2,+}(U)M_{2,+}(V)-N C_{\rm ct}^{I,+}\epsilon_{\rm cusp}\bigr)-E_6^{I,+}-E_{\rm rec}^{I,+}`. Valid when: Valid for outward-rounded interval data enclosing pair contractions, Ward-Hessian constants, truncation error, and recovery-map error in the same theory.
- finite Route A promotion inequality: `R_{++}^{I,-}>L_+`. Valid when: Valid only for the fixed finite H,K Schur-Feshbach block whose leakage scalar L_+ was computed in the same normalization.

## Attempted Derivation

- Conceptual pressure attacked: finite Schur-Feshbach positivity needs a same-theory Wilson mediator; positive pair covariance and gradient-flow renormalization are valid local inputs but can be erased by the connected four-curvature polarization.
- Fix the source object as centered flowed Wilson hairpins for H,K endpoint currents and the target object as the finite scalar R_{++}^{ren} compared with L_+; this avoids defining the target property as the bridge image.
- Expand the same-theory cumulant kappa_2(W_hat_t(J_+^U),W_hat_t(J_+^V)). Disconnected products cancel by centering; one-hairpin perimeter and cusp terms cancel by Z_hp and the chosen counterterms.
- The order g_t^4 pair contractions give 2(N^2-1)G_{++}; the remaining connected four-curvature polarization has color N(N^2-1) and kernel K_4^{WS}.
- Represent the plus hairpin by endpoint sheet currents. Certified zero monopole and dipole moments make the constant and linear endpoint Taylor terms vanish, leaving a second-moment Hessian remainder.
- Split K_4^{WS} into I_3g,I_4g,I_ct,I_end and split endpoint domains into near/far cells. Direct interval quadrature bounds near cells; flowed heat-kernel majorants bound far cells.
- Combine the bounds to get R_{++}^{I,-}=g_t^4(N^2-1)(2G_{++}^{I,-}-NH_4^{I,+}M_2(U)M_2(V)-N C_ct^{I,+}epsilon_cusp)-E_6^{I,+}-E_rec^{I,+}.
- The hard gate is finite endpoint-box positivity after H,K: success proves R_{++}^{I,-}>L_+ and promotes this finite Route A repair; failure quarantines the R repair without touching Clay continuum or spectral gates.

Blocking gap: No certified outward-rounded interval currently encloses all near-cell Hessians, far heat-kernel tails, E_6, and recovery-map errors for the concrete H,K endpoint geometry.

## Falsifiers

- falsifier: the recovered plus endpoint current has a nonzero monopole or dipole moment, so Hessian suppression is invalid.
- falsifier: H_4^{I,+}M_{2,+}(U)M_{2,+}(V) is large enough that R_{++}^{I,-}<=L_+ for every allowed flow window.
- falsifier: the positive pair baseline G_{++}^{I,-} vanishes because the H,K endpoint geometry has zero reflected pairing.
- falsifier: cusp or endpoint counterterm intervals depend on the regulator in a way that changes the same-theory observable.
- falsifier: the interval lower bound has no cutoff-stable plateau as a decreases with fixed physical eta,d,t.
- falsifier: quotienting raw Wilson contours to endpoint currents changes a centered flowed Wilson cumulant beyond E_rec.

## Learning

Cycle 297 attacks the missing same-theory mediator between finite Feshbach positivity and Wilson cumulant positivity. Declarative tension: Schur-Feshbach endpoint positivity, positive flowed pair covariance, and same-theory recovery must jointly be valid, but C4 can erase the pair term. Raw Wilson contours are representation-limited; global OS spectral transfer or a non-Gaussian Schwinger family witness is too coarse. Endpoint sheet currents are sharper because Ward subtraction, plus-moment cancellation, near/far heat-kernel Hessians, interval arithmetic, and zero-pairing quotienting become primitive. Conceptual value signal: R_{++}/kappa_4 is now a route-deciding color-geometric interval with a falsifier, not a symbolic threshold.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and proof-search guide, not as evidence for the Clay theorem.`
- Rationale: The branch is looping unless the endpoint R/kappa_4 term gets a concrete sign/size certificate. A target-preserving regulator experiment can reveal whether Ward-Hessian suppression plausibly beats Schur-Feshbach leakage before more abstraction is added.
- Situation seed: Fixed SU(3) Wilson lattice Yang-Mills in a finite box with gradient flow, the concrete H,K plus-channel endpoint hairpin sheets, centered flowed Wilson hairpins, and Ward/cusp-subtracted connected cumulant kappa_2 defining R_{++}^{ren}.
- Varied variable: The flow-to-cell ratio sigma=sqrt(8t)/eta, varied over a window with a<<sqrt(8t)<=eta/2.
- Held-fixed controls: Gauge group SU(3), H,K endpoint geometry, orientation conventions, and plus-channel moment constraints., Physical endpoint diameter eta, separation d/eta, finite Schur-Feshbach leakage L_+, and the same Wilson cutoff measure for all observables., Ward/cusp subtraction scheme, zero-pairing quotient policy, near/far split rule, and outward-rounded interval arithmetic.
- Expected observation: A valid window should show a cutoff-stable lower interval R_{++}^{I,-}(sigma) with positive pair baseline dominant over the Ward-Hessian C4 bound; absence of such a plateau demotes the endpoint repair.
- Transfer certificate needed: Before intuition affects proof obligations, provide cutoff-uniform interval constants for G_{++}, H_4, E_6, and E_rec plus a same-theory recovery-map certificate for the connected cumulant witness.

## Next Experiment

Route explicitly to proof search: build the endpoint-cell interval table for G_{++}^{I,-}, H_{4,s}^{near/far,I,+}, E_6^{I,+}, and E_rec^{I,+} for the concrete H,K plus hairpin geometry; keep the validator-facing marker connected cumulant witness / same-theory nontriviality witness as support-only, and demote on any stated falsifier.

# Raw K4 two-sparse stress test for post-H,K endpoint positivity

## Candidate Lemma

Two-sparse raw-K4 stress lemma: in finite heat-kernel cutoff YM, an interval-enclosed vector x=e_p+eta e_q with sup x^*U_sigma x<0 is a valid falsifier of post-H,K endpoint positivity; absence of such x proves neither PSD nor Clay mass gap.

## Definitions

- source object: heat-kernel regulated finite-volume SU(N) Wilson plaquette-sheet cumulant data {C_sigma,K4_sigma,E_OPE,S_HK} for the worked H,K endpoint box.
- target object: finite endpoint quadratic form U_sigma on Wilson collar/hairpin endpoint coefficients, before any continuum or OS spectral claim.
- controlled interface: Rec_raw maps oriented plaquettes, weights, transporters, color tensors, and Schur blocks to interval entries of U_sigma.
- same-theory condition: one lattice action, cutoff a, heat-kernel width sigma, coupling g_R, Wilson basis, normal ordering, and H,K Schur data are used throughout.
- carrier audit: scalar R is too weak, OS density is too strong/circular, A012 shells are convenient but quarantined; raw plaquette intervals are fragmented yet valid.
- representation requirements: encode plaquettes, weights, transporters, color tensors, cumulant/OPE intervals, Schur blocks; preserve gauge invariance and reflection; operate by contraction, interval sum, quotient audit, Rayleigh stress, Schur subtraction.

## Assumptions

- Model: finite-volume lattice SU(N) Yang-Mills with heat-kernel plaquette regulator and reflection-compatible endpoint box; no continuum limit is claimed.
- Cutoff: sigma/a and box size are fixed; plaquette cumulant intervals enclose every retained Wilson/OPE orientation and transporter choice.
- Same-theory: R_raw, K4, E_OPE, and S_HK use the same action, coupling, regulator, Wilson basis, and normal-ordering cancellation.
- Local: only finite Route A endpoint-box positivity changes; gauge-invariant observable density, OS Hilbert observable algebra, and spectral transfer remain non-claims.

## Equations

- raw-connected-polarization: `R^{\rm raw}_{ij,\sigma}=\operatorname{cum}_2(Q_i,Q_j),\quad Q_i=\sum_{p\in\Sigma_i}w_{ip}\,\operatorname{tr}(U_pF_pU_p^{-1})^2`. Valid when: Valid when Q_i are vacuum/perimeter-normalized Wilson sheet observables in the same heat-kernel cutoff and disconnected cumulants have been cancelled before boundary OPE compression.
- Gaussian-K4-OPE-split: `R^{\rm raw}_{ij,\sigma}=\alpha_N g_R^4\,(C_\sigma\circ C_\sigma)_{ij}+\frac{g_R^4}{16N^2}K^{(4)}_{ij,\sigma}+E^{\rm OPE}_{ij,\sigma},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Requires finite SU(N) color trace normalization, transported curvature insertions on oriented plaquettes, and a cutoff Wilson/OPE expansion with enclosed K4 and OPE intervals.
- two-sparse-stress-gate: `U_\sigma=R^{\rm raw}_\sigma-S_{HK},\quad I_{pq}(\eta)=[U_{pp}]+|\eta|^2[U_{qq}]+2\operatorname{Re}(\eta[U_{pq}]);\ \sup I_{pq}(\eta)<0\Rightarrow U_\sigma\not\succeq0`. Valid when: Applies when U_sigma entries are interval-enclosed in the same endpoint basis and x=e_p+eta e_q is an allowed finite Wilson coefficient vector.

## Attempted Derivation

- Conceptual pressure: replace symbolic boundary R by a validator-facing connected cumulant witness that can kill or promote the finite H,K endpoint route.
- Use vacuum/perimeter normal ordering in the heat-kernel Wilson sheet observables so disconnected pieces cancel before forming cum_2(Q_i,Q_j).
- Split cum_2 into the PSD Gaussian color Hadamard square, the connected four-curvature K4 interval, and the OPE interval; then subtract S_HK in the same endpoint basis.
- Test x=e_p+eta e_q. If interval arithmetic gives sup x^*U_sigma x<0, finite endpoint positivity is contradicted by a concrete Rayleigh stress vector.

Blocking gap: The same-regulator K4 interval entries for the selected endpoint pair p,q and the matching Schur entries are not yet computed.

## Falsifiers

- A same-regulator p,q,eta gives sup I_pq(eta)<0; this is the intended falsifier and demotes the H,K endpoint route.
- The K4 intervals require large-field or topological tails not uniformly enclosed at fixed sigma/a, invalidating the finite certificate.
- Exact Wilson quotient audit changes a sign, multiplicity, or transporter, so the stress vector was an artifact of representation compression.
- No two-sparse stress appears and Delta_raw has no positive lower bound; then the branch must quarantine rather than loop on abstractions.

## Learning

Declarative tension: Wilson/OPE coefficients, connected K4 negativity, OPE error, and S_HK must jointly hold in one cutoff theory, while Clay-level continuum and spectral claims are barred. The two-sparse stress gate is sharp because a few raw K4 intervals can demote the route without full matrix PSD.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and proof-search guide.`
- Rationale: The branch no longer needs another OS-density restatement; it needs a concrete same-regulator K4 interval stress test for the finite endpoint gate.
- Situation seed: Heat-kernel SU(N) lattice endpoint box for the worked H,K collar/hairpin geometry; choose two boundary plaquette-sheet nodes p,q sharing one transported edge and compute the connected cumulant witness intervals.
- Varied variable: The complex phase and magnitude eta in the two-sparse vector x=e_p+eta e_q.
- Held-fixed controls: Same Wilson action, cutoff a, heat-kernel width sigma, coupling g_R, finite volume, and endpoint H,K geometry., Same normal-ordering cancellation, oriented plaquette list, transporter convention, color trace normalization, OPE interval budget, and Schur block S_HK.
- Expected observation: If K4_pq is sufficiently negative relative to the Gaussian square and Schur diagonal cost, sup I_pq(eta)<0 for a phase aligning with -U_pq; otherwise two-sparse stress is absent.
- Transfer certificate needed: A validator-facing Rec_raw table proving same-theory interval enclosures for U_pp,U_pq,U_qq, exact Wilson quotient invariance, and recovery of x as an allowed endpoint coefficient vector.

## Next Experiment

Proof search: compute the first adjacent plaquette-pair K4 interval table for p,q, scan eta phases, and hand a connected cumulant witness to validation; no further symbolic R or gauge-invariant observable density looping.

