# cycle-0319

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: endpoint source screen for finite Wilson gate

## Candidate Lemma

For the heat-kernel plaquette-sheet regulator, the remaining post-H,K null-channel endpoint polarization admits a valid clipped interval screen: only source-certified classes with positive signed endpoint dominance can lower the finite reflected-Wilson OS gate.

## Definitions

- source object: C_ep(a,t,h), the regulated heat-kernel plaquette-sheet endpoint carrier consisting of endpoint source classes c, seven source values for log Z_c(sL_c), cumulant intervals [kappa_c^-,kappa_c^+], signed incidences b_{ij,c}, color factor C_N, Gaussian margin M_G, and tail budget tau.
- target object: I_gate, the scalar Schur-Feshbach post-H,K reflected-Wilson OS transfer gate for the fixed finite three-hairpin block; I_gate>=0 promotes only this finite block and is not a continuum or mass-gap claim.
- controlled interface: the map C_ep -> [I_-,I_+] formed by source differentiation, source-equivalence aggregation, signed incidence contraction D_c, color multiplication, clipping, and tail addition.
- same-theory condition: all Z_c are endpoint restrictions of the original regulated Wilson plaquette partition function with the locked gauge-invariant Wilson observables, with no boundary counterterm, no changed normalization, and no enlarged boundary algebra.
- endpoint dominance: D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}; the half-overlap shield is D_c<=0 whenever b_{13,c}+b_{23,c}>=b_{12,c}/2.
- connected cumulant witness: kappa_c is the singlet-projected connected fourth flux cumulant obtained from log Z_c, after Wick-square Gram terms and straight f f incidence contacts have been removed.

## Assumptions

- Model: four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette action on a reflection-symmetric collar/hairpin finite block.
- Regime: fixed finite H,K hairpin block after the first-order and second-order Schur-Feshbach reductions have been performed.
- Cutoff: a>0 and endpoint heat-kernel time t_c>0 are finite, with constants stated uniformly on the endpoint boxes under comparison.
- Same-theory: Wilson loop normalization, gauge-invariant observable algebra, and reflection map are identical before and after collar collapse.
- Uniformity: the endpoint tail tau bounds all nonlocal endpoint/corner leftovers uniformly in the same regulator family.
- Validity: Wick-square contractions are treated as positive Gram contributions and the straight C_A f f contact is canceled by the previously established null-incidence identity.
- Local: endpoint boxes are aggregated only after equality of regulated source data, not merely after geometric resemblance.

## Equations

- endpoint connected cumulant: `\kappa_c(L_c)=\left.\partial_s^4\log Z_c(sL_c)\right|_{s=0}`. Valid when: Valid when Z_c is the same heat-kernel endpoint partition function and L_c is the locked singlet source induced by the finite hairpin block.
- signed endpoint incidence: `D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}`. Valid when: Valid after the Schur-Feshbach null vector has contracted the three reflected Wilson pair polarizations in the fixed finite block.
- general interval gate: `[I_-,I_+]=M_G+C_N\sum_c[\min(D_c\kappa_c^-,D_c\kappa_c^+),\max(D_c\kappa_c^-,D_c\kappa_c^+)]+[-\tau,\tau]`. Valid when: Applies when endpoint source classes have been aggregated by equal regulated source data and the remaining tail is bounded by tau.
- clipped nonpositive-cumulant screen: `\kappa_c\in[-B_c,0]\ \Longrightarrow\ I_-\ge M_G-C_N\sum_c B_c[D_c]_+-\tau`. Valid when: Requires certified nonpositive connected endpoint cumulants and preserves the signed incidence before clipping positive endpoint dominance.
- SU(N) root-quartic cap: `\kappa_c(L_c)=-\frac{t_c^4}{60}\,R_{4,N}(L_c)+E_c,\quad R_{4,N}(L)=N\operatorname{tr}(L^4)+3(\operatorname{tr}L^2)^2`. Valid when: Valid in small endpoint normal coordinates for the heat-kernel box, provided the remainder E_c is uniformly bounded for the same source family.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: C_ep(a,t,h), the regulated heat-kernel plaquette-sheet endpoint carrier consisting of endpoint source classes c, seven source values for log Z_c(sL_c), cumulant intervals [kappa_c^-,kappa_c^+], signed incidences b_{ij,c}, color factor C_N, Gaussian margin M_G, and tail budget tau.; target object: I_gate, the scalar Schur-Feshbach post-H,K reflected-Wilson OS transfer gate for the fixed finite three-hairpin block; I_gate>=0 promotes only this finite block and is not a continuum or mass-gap claim.; Model: four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette action on a reflection-symmetric collar/hairpin finite block..
- Start from the already reduced finite Schur-Feshbach null scalar after H,K; write the remaining endpoint contribution as M_G plus connected boundary-OPE polarization plus a tail.
- Use the heat-kernel plaquette-sheet regulator and expand reflected Wilson endpoint sheets by singlet flux sources L_c; connected log Z_c removes disconnected Wick-square terms.
- Use the prior null-incidence cancellation of straight C_A f f contacts, leaving only endpoint connected fourth cumulants and endpoint/corner tails.
- Group endpoint boxes by equality of regulated seven-point source data; sum signed incidences D_v inside each source class before clipping.
- Apply interval arithmetic: each class contributes D_c[kappa_c^-,kappa_c^+] and the tail contributes [-tau,tau].
- When a nonpositive cumulant certificate is available, replace the general interval by the clipped lower screen M_G-C_N sum B_c[D_c]_+-tau.
- Use the SU(N) Haar root-quartic expansion only as a one-sided analytic cap, not as a substitute for same-theory source data.

Blocking gap: The actual endpoint source classes, fractional incidences, uniform eighth-derivative bounds, and tail tau have not been computed for the fixed hairpin geometry.

## Falsifiers

- A direct same-theory stencil gives I_+<0 for the fixed finite block; this is a finite reflected-Wilson OS falsifier.
- The endpoint tail tau is not cutoff-uniform, so the claimed interval is not valid for cutoff removal.
- A boundary counterterm or boundary Hilbert sector is required to define Z_c at the collapsed endpoint, violating the same-theory condition.
- Two geometrically identical endpoints have different regulated source data, invalidating geometry-only compression.
- A positive-D source class has a negative connected cumulant large enough to overcome M_G after color multiplication and tail addition.
- The eighth-derivative bound for the seven-point stencil scales worse than the endpoint margin.

## Learning

Cycle 319 turns quarantine into a sharper finite proof-search object: the valid carrier is the clipped endpoint source interval, not raw R and not a raw negative kappa_4 alarm. The conceptual pressure is endpoint collapse inside the same Wilson theory. The declarative tension is collar OS positivity plus fixed gauge-invariant Wilson observables plus singular endpoint OPE without adding a boundary theory. The hard gate is the finite post-H,K reflected-Wilson OS transfer scalar: success promotes this one finite block; failure gives a finite same-theory falsifier; missing source data keeps quarantine. The conceptual value signal is sharpness and route change at finite scope, because only positive-D leakage times same-theory connected cumulants plus uniform tail can demote the gate. Clay continuum construction, nontriviality, full OS/Wightman reconstruction, and positive mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch has exhausted abstract OS-cone and symbolic R arguments; the remaining hard gate is a finite endpoint connected cumulant witness with signed incidences.
- Situation seed: Fix the heat-kernel SU(N) plaquette-sheet regulator and the same post-H,K three-hairpin endpoint boxes; imagine a source-equivalent class whose fractional overlaps are b12=1, b13=eta/2, b23=eta/2, with identical seven-point endpoint source data.
- Varied variable: eta=b13+b23, the fractional non-12 overlap protecting the endpoint class from positive D leakage.
- Held-fixed controls: Locked gauge-invariant Wilson observables and reflection map are unchanged., Heat-kernel plaquette action, SU(N), color factor C_N, source norm L_c, and Gaussian margin M_G are fixed., No boundary counterterm or auxiliary boundary algebra is allowed., The tail budget tau is assumed cutoff-uniform for the thought experiment.
- Expected observation: For eta>=1/2 the class is shielded because D_c<=0; for eta<1/2 a negative connected cumulant lowers I_gate by C_N B_c(2-4eta), giving a concrete promotion or falsifier interval.
- Transfer certificate needed: Before affecting proof obligations, the imagined class must be realized by actual endpoint source data, a uniform seven-point stencil error bound, and a same-theory tail estimate in the heat-kernel regulator.

## Next Experiment

Route explicitly to proof search plus endpoint source computation: build the validator-facing connected cumulant witness table for the fixed heat-kernel three-hairpin endpoints, compute D_c after source-equivalence aggregation, certify M8 and tau, then decide I_->0 promotion, I_+<0 falsifier, or continued quarantine.

# Gauge-Invariant Nontriviality Witness Selection -> finite endpoint R certificate

## Candidate Lemma

Annular Ward-Hessian dominance lemma: for the H,K plus endpoint current, the renormalized endpoint covariance R_{++}^{ren} has a valid lower interval given by positive flowed pair covariance minus annular connected-C4 Hessian majorants, same-theory recovery error, and the Schur-Feshbach leakage L_+.

## Definitions

- source object: centered flowed Wilson hairpin observables h_i^{t,eps} for fixed finite H,K endpoint boxes, represented by gauge-invariant sheet currents J_i and endpoint currents partial J_i in the same Wilson measure.
- target object: the finite Route A plus-channel endpoint positivity margin Delta_R that certifies the post-H,K Schur-Feshbach endpoint box, not a continuum mass gap.
- controlled interface: the centered cumulant R_{++}^{ren}=kappa_2(h_+^{t,eps},h_+^{t,eps}) after Ward/cusp subtraction and recovery from raw contours to endpoint sheet currents.
- same-theory condition: the regulator, coupling, counterterms, flow time, observable algebra, and recovery maps are shared with the Wilson Schwinger family used for any later same-theory nontriviality witness.
- h_+=h_1+h_2 is the plus endpoint hairpin channel; J_+=J_1+J_2 is its sheet-current representative.
- G_{++}^{-} is an outward-rounded lower interval for the Gaussian pair contraction of two flowed curvature insertions on J_+.
- C_{4,++}^{WS} is the Ward-subtracted connected four-curvature polarization integrated against four copies of J_+.
- rho is the annular split radius around each endpoint cell; eta is the endpoint cell diameter; M_{2,+} is the certified second endpoint moment after monopole and dipole cancellation.

## Assumptions

- Model: four-dimensional SU(N) Wilson lattice Yang-Mills with gradient-flow time t>0, boundary point splitting eps, and fixed finite H,K endpoint geometry before any continuum claim.
- Cutoff: constants are stated at finite lattice spacing a and must be shown stable as a/eta -> 0 for promotion beyond a regulator computation.
- Regime: endpoint boxes are disjoint, eta < rho < c sqrt(8t), and the collar separation d is fixed in physical units.
- Same-theory: Ward/cusp counterterms, flowed observables, and endpoint-current recovery are all computed inside the same regulated Wilson theory.
- Validity: plus-channel reflection symmetry gives zero endpoint monopole and dipole moments; otherwise the Hessian reduction is invalid.
- Local: the lemma changes only finite endpoint-box positivity after H,K and leaves Clay existence, OS/Wightman reconstruction, observable density, topology control, and spectral gap untouched.

## Equations

- R-decomposition: `R_{++}^{ren}=2g_t^4(N^2-1)G_{++}-g_t^4N(N^2-1)C_{4,++}^{WS}+E_6+E_{rec}`. Valid when: Valid when the flowed Wilson cumulant is expanded in the fixed endpoint boxes after disconnected-product removal, one-hairpin perimeter/cusp subtraction, and same-theory recovery from contours to sheet currents.
- plus-moment cancellation: `\int_{B_e}J_+(x)\,dx=0,\qquad \int_{B_e}(x-x_e)_\mu J_+(x)\,dx=0`. Valid when: Valid when the H,K plus-channel endpoint currents are paired by reflection and orientation symmetry inside each endpoint cell before applying the Taylor Hessian remainder.
- annular Hessian bound: `|C_{4,++}^{WS}|\le M_{2,+}^2\left(A_{near}(\rho)+A_{far}(\rho)\right)`. Valid when: Applies when the Ward-subtracted connected four-curvature kernels have certified mixed-Hessian majorants on the near core and every dyadic far annulus.
- sector constants: `A_{near}(\rho)=\sum_s |\Gamma_s|\sup_{\Omega_{<\rho}}\|\nabla_x\nabla_yK_s^{ren}\|,\quad A_{far}(\rho)=\sum_{s,q\ge0}|\Gamma_s|2^{-2q}\sup_{\Omega_{2^q\rho,2^{q+1}\rho}}\|\nabla_x\nabla_yK_s^{ren}\|`. Valid when: Requires a finite sector decomposition into three-gluon, four-gluon, counterterm, and endpoint sectors with heat-kernel or interval-quadrature Hessian enclosures.
- dominance margin: `\Delta_R(\rho)=g_t^4(N^2-1)\{2G_{++}^{-}-NM_{2,+}^2[A_{near}(\rho)+A_{far}(\rho)]\}-E_6^{+}-E_{rec}^{+}-L_+`. Valid when: Valid when all intervals use outward rounding, the Schur-Feshbach leakage L_+ is the same finite H,K matrix leakage, and errors are upper bounds in the same regulator.
- promotion implication: `\exists\rho\in(\eta,c\sqrt{8t}):\Delta_R(\rho)>0\ \Longrightarrow\ Q_+^{endpoint}>0`. Valid when: Applies only to the finite post-H,K endpoint-box matrix after the annular R interval and the Schur-Feshbach leakage are both certified.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: centered flowed Wilson hairpin observables h_i^{t,eps} for fixed finite H,K endpoint boxes, represented by gauge-invariant sheet currents J_i and endpoint currents partial J_i in the same Wilson measure.; target object: the finite Route A plus-channel endpoint positivity margin Delta_R that certifies the post-H,K Schur-Feshbach endpoint box, not a continuum mass gap.; Model: four-dimensional SU(N) Wilson lattice Yang-Mills with gradient-flow time t>0, boundary point splitting eps, and fixed finite H,K endpoint geometry before any continuum claim..
- Freeze the Clay target and local claim level: prove only a finite endpoint-box positivity certificate after H,K, not existence or a Hamiltonian gap.
- Use gradient-flow plus boundary point splitting as regulator; expand the centered thin hairpin covariance through the flowed curvature cumulant.
- Cancel the disconnected product and one-hairpin perimeter/cusp terms, leaving a positive two-curvature pair contraction and the connected four-curvature polarization.
- Replace raw contours by endpoint sheet currents; impose the zero-pairing quotient guard so the carrier does not change the Wilson observable.
- Use plus-channel reflection/orientation symmetry to cancel endpoint monopole and dipole moments in each cell.
- Taylor expand the Ward-subtracted C4 kernel around endpoint centers; the first nonzero remainder is controlled by mixed Hessian norms times M_{2,+}^2.
- Split the mixed-Hessian domain into a near core of radius rho and dyadic far annuli; define A_{near}(rho) and A_{far}(rho) from sector kernels K_s^{ren}.
- Combine the lower pair interval, upper connected-C4 interval, recovery error, sixth-order remainder, and Schur-Feshbach leakage into Delta_R(rho).

Blocking gap: The missing mediator is a certified cutoff-stable interval for the sector Hessian constants A_{near}, A_{far}, plus E_rec; one-loop formulas or formal Ward identities do not yet provide a regulator-uniform bound.

## Falsifiers

- Ward or cusp subtraction leaves a logarithmic endpoint divergence, invalidating the Hessian remainder.
- The plus-channel endpoint current has a nonzero monopole or dipole moment after recovery; then the eta^2 suppression is false.
- A certified interval gives Delta_R(rho)<=0 for every admissible rho; this is the decisive falsifier for the R endpoint repair.
- The zero-pairing quotient changes the Wilson observable or violates same-theory recovery.
- The far-annulus tail is not summable uniformly in cutoff or volume.
- Interval widths exceed the pair baseline, so the sign/size certificate is not valid.
- The finite R_{++} survives only at fixed cutoff and cannot be used as a same-theory nontriviality witness.

## Learning

Conceptual pressure attacked: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator, while positive flowed pair covariance and same-theory recovery can both be valid and still be erased by connected C4. Hard gate: finite endpoint-box positivity after H,K; success promotes one Route A finite gate, failure quarantines the R repair without touching Clay existence, OS/Wightman axioms, nontriviality, observable density, topology control, OS spectral transfer, or mass gap. Declarative tension: endpoint positivity, Wilson cumulant positivity, and same-theory recovery must jointly hold, but the missing mediator is a cutoff-stable Ward-Hessian annular dominance interval. Carrier critique: raw Wilson contours are fragmented and representation-limited; global OS spectral transfer or a non-Gaussian Schwinger family route is too coarse here. Efficient representation: encode H,K sheets, endpoint currents, cell moments, sector kernels, counterterms, and recovery errors; preserve gauge, color, reflection, orientation, cutoff, locality, and same-theory invariants; use cumulant expansion, Ward/cusp subtraction, Taylor Hessian remainders, heat-kernel majorants, interval quadrature, outward rounding, and zero-pairing quotienting; keep finite endpoint-cell locality; transfer only through centered flowed Wilson cumulants; demote on any falsifier. Conceptual value signal: R_{++}/kappa_4 is now an annular sign/size certificate, not a symbolic boundary-OPE term.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and proof-search guide.`
- Rationale: The branch is blocked by sector constants, not by another abstract obstruction restatement. A concrete annular endpoint computation can decide whether the positive pair term plausibly beats connected C4 and L_+.
- Situation seed: SU(2) and SU(3) Wilson lattice on a large finite torus, with gradient-flowed plaquette-sheet representatives of the fixed H,K plus hairpin endpoint boxes; compute the centered flowed Wilson covariance and its Ward-subtracted C4 sector intervals.
- Varied variable: The annular split ratio r=rho/sqrt(8t), with eta/sqrt(8t), H,K geometry, and physical collar separation held fixed.
- Held-fixed controls: Fixed H,K endpoint geometry and plus-channel reflection/orientation symmetry., Same Wilson action, coupling branch, flow time normalization, and boundary counterterm prescription., Endpoint-cell diameter eta and physical separation d in lattice units scaled toward fixed physical values., Outward-rounded interval arithmetic and the same zero-pairing quotient policy for all representatives.
- Expected observation: If the mechanism is real, Delta_R(r) develops a positive stable plateau for a nonempty r-interval; if connected C4 dominates or recovery is unstable, all certified margins remain nonpositive and the endpoint repair is quarantined.
- Transfer certificate needed: A cutoff- and volume-stable recovery map for flowed Wilson hairpins, Ward/cusp subtraction identities in the same theory, annular Hessian tail summability, and a finite Schur-Feshbach handoff to L_+ before intuition affects proof obligations.

## Next Experiment

Proof search: build the annular interval table for I_{3g}, I_{4g}, I_ct, and I_end in the fixed H,K plus endpoint cell, then report Delta_R(rho) with same-theory nontriviality witness boundary explicitly marked as a non-claim unless cutoff-stable connected cumulants are later validated.

# Raw K4 connected-cumulant stress certificate for the finite H,K endpoint box

## Candidate Lemma

Raw transported-plaquette interval contraction lemma: in one heat-kernel regulated cutoff Yang-Mills theory, the connected boundary-OPE polarization R_{ij} of the post-H,K endpoint box is enclosed by a computable interval matrix obtained from Gaussian crossed plaquette contractions, raw connected K4 plaquette cumulant intervals, OPE remainders, and the fixed Schur hairpin subtraction.

## Definitions

- source object: finite-volume SU(N) lattice Yang-Mills measure with Wilson action, heat-kernel smearing scale sigma, cutoff a, endpoint Wilson sheet family S_i, and raw plaquette logarithms X_p^a transported to a common endpoint frame.
- target object: the finite Hermitian endpoint quadratic form U_sigma=R_sigma-S_HK whose positivity or stress-vector negativity decides only the post-H,K Route A endpoint-box gate.
- controlled interface: the recovery map from oriented plaquette cumulant intervals I_{prst}^{abcd}(sigma,a,L) to entries of R_sigma, followed by the already fixed Schur-Feshbach subtraction S_HK=B^*E^{-1}B in the same endpoint basis.
- same-theory condition: Wilson/OPE coefficients, heat-kernel transporters, raw K4 cumulant intervals, OPE error intervals, and H,K Schur blocks are computed with the same cutoff, volume, coupling, boundary reflection convention, and endpoint Wilson observables.
- connected cumulant witness: R_{ij}=cum_2(Q_i,Q_j) with Q_i a vacuum-subtracted endpoint Wilson sheet quadratic flux operator; disconnected vacuum and perimeter pieces are cancelled before compression.
- carrier critique: scalar R is representation-limited, A012 shell compression is convenient but quarantined, OS Hilbert observable algebra is too strong and circular for this local gate, while raw plaquette enumeration is fragmented but valid.

## Assumptions

- Model: finite-volume lattice SU(N) Yang-Mills with Wilson plaquette action and heat-kernel smearing; no continuum or OS reconstruction claim is made.
- Cutoff: a>0, sigma>=c a, and the endpoint box, H,K collar, and hairpin supports are finite and reflection-compatible.
- Same-theory: the same regulated measure supplies Wilson expectations, OPE coefficients, raw K4 intervals, Gaussian covariance C_sigma, and Schur blocks B,E.
- Validity: the boundary OPE is used only inside the finite endpoint collar with an explicit interval remainder E_OPE(sigma,a,L).
- Local: all plaquette transports stay within the chosen endpoint box and quotienting is only by exact Wilson trace identities and orientation symmetries.
- Constraint: the target property is not gauge-invariant observable density, excitation-sector cyclicity, OS positivity in the continuum, or a Hamiltonian mass gap.

## Equations

- endpoint quadratic flux observable: `Q_i^{\sigma}=\sum_{(p,r)\in S_i} w_i(p,r)\,T_i^{ab}(p,r)\, :X_p^a X_r^b:_\sigma`. Valid when: Valid when heat-kernel transported plaquette logarithms are defined in the finite endpoint collar and normal ordering uses the same regulated vacuum expectation.
- connected polarization decomposition: `R_{ij}^{\sigma}=\operatorname{cum}_2(Q_i^{\sigma},Q_j^{\sigma})=\alpha_N g_R^4\,(C_{ij}^{\sigma}\circ C_{ij}^{\sigma})+\frac{g_R^4}{16N^2}K_{ij}^{(4),\sigma}+E_{ij}^{\mathrm{OPE},\sigma}`. Valid when: Applies after vacuum and perimeter disconnected terms cancel in the same cutoff Wilson measure and the endpoint OPE remainder is interval bounded.
- raw K4 recovery map: `K_{ij}^{(4),\sigma}\in \sum_{p,r\in S_i}\sum_{s,t\in S_j} w_i(p,r)w_j(s,t)\,T_i^{ab}(p,r)T_j^{cd}(s,t)\,I_{prst}^{abcd}(\sigma,a,L)`. Valid when: Valid when every transported four-plaquette connected cumulant interval is certified before Wilson-identity quotienting and interval arithmetic is outward rounded.
- Schur-corrected endpoint matrix: `U_\sigma \in \alpha_N g_R^4(C^\sigma\circ C^\sigma)+\frac{g_R^4}{16N^2}\mathcal I_{K4}^\sigma+\mathcal I_{\mathrm{OPE}}^\sigma-S_{HK}^\sigma`. Valid when: Requires the H,K Schur block S_HK to be computed in the same endpoint basis and with the same reflected Wilson normalization.

## Attempted Derivation

- Conceptual pressure attacked: replace repeated phase-stress rhetoric by a raw same-regulator K4 interval computation that can actually decide or quarantine the finite endpoint route.
- Declarative tension: Wilson/OPE coefficients, raw connected K4 intervals, OPE errors, and S_HK must jointly control one finite endpoint quadratic form, while OS Hilbert observable algebra, gauge-invariant observable density, continuum existence, and Hamiltonian mass gap are barred as conclusions.
- Start with heat-kernel regulated finite lattice SU(N). Define Q_i^sigma as the transported, normal-ordered quadratic plaquette-flux approximation to the endpoint Wilson sheet observable.
- Use connected cumulants: vacuum expectation, perimeter self-energy, and disconnected Gaussian products cancel before endpoint compression, leaving crossed Gaussian contractions plus connected K4 plus OPE remainder.
- The crossed Gaussian contraction gives a positive semidefinite Hadamard square with color factor alpha_N=(N^2-1)/(8N^2).
- Recover K4_ij by summing raw transported four-plaquette connected cumulant intervals against sheet weights and color tensors; this is the first validator-facing connected cumulant witness.
- Subtract the finite Schur-Feshbach hairpin energy S_HK in the same endpoint basis to form U_sigma.
- For a pair p,q and phase theta, bound the Rayleigh quotient of e_p-eta e^{-i theta}e_q above by U_pp^+ + eta^2 U_qq^+ - 2 eta L_pq(theta). Optimizing gives tau_pq(theta).
- Hard gate: tau_pq(theta)<0 is a finite falsifier; if every tested tau survives, only full Delta_raw proof search can promote finite endpoint positivity.

Blocking gap: The branch still lacks actual certified same-regulator raw K4 intervals I_{prst}^{abcd} for the chosen H,K endpoint geometry and a quotient audit proving the phase lower bound L_pq(theta) is invariant.

## Falsifiers

- A negative tau_pq(theta) is a valid falsifier for finite H,K endpoint-box positivity in this Wilson collar/hairpin route.
- Regulator mismatch between K4 intervals and S_HK invalidates the same-theory recovery map.
- A Wilson-identity quotient changing any interval endpoint is a falsifier for the raw plaquette carrier.
- If OPE intervals or raw K4 intervals are wider than the Gaussian-Schur margin, the branch must be quarantined rather than promoted.
- If stress survival is mistaken for full PSD, the proof state is invalid; full Delta_raw remains mandatory.

## Learning

Cycle 319 attacks the missing mediator between raw connected Wilson cumulants and Schur-corrected finite endpoint positivity. The current carrier audit is decisive: scalar R is too weak, OS Hilbert observable algebra and gauge-invariant observable density are too strong and circular for this local gate, A012 shells are quarantined, and raw plaquette intervals are fragmented but valid. The efficient representation must encode oriented plaquettes, sheet weights, heat-kernel transporters, color tensors, raw cumulant intervals, OPE intervals, endpoint indices, and Schur blocks; preserve gauge invariance, reflection support, Gaussian/K4 separation, endpoint compression, same-theory normalization, Hermiticity, and exact Wilson quotienting; support cumulant contraction, phase interval summation, Rayleigh stress search, Loewner lower bounds, and Schur subtraction; use finite endpoint-box complexity; transfer only through tau, Delta_raw, or x_stress; and expose falsifiers by negative margin, missing intervals, non-invariant quotienting, or regulator mismatch. Conceptual value signal: sharp and route-changing at finite scope because R is a connected cumulant witness with explicit color, geometry, non-Gaussian K4, OPE, and Schur data in one valid inequality, while all Clay-level gates remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe.`
- Rationale: The branch is looping unless raw K4 intervals are tested; another abstraction of R would not change the proof state. A finite phase-stress probe can demote the H,K endpoint route from three endpoint interval types while preserving Clay non-claims.
- Situation seed: Finite SU(3) Wilson lattice on a reflected endpoint box containing the worked H,K collar/hairpin supports; heat-kernel smearing sigma=2a is applied to all endpoint plaquette logarithms, and Q_p,Q_q are two endpoint Wilson sheet flux observables sharing one boundary corner.
- Varied variable: The phase theta in Re(e^{i theta}U_pq) and, in a secondary scan, the smearing ratio sigma/a within {1.5,2,3}.
- Held-fixed controls: Same Wilson action, coupling g_R, finite volume, cutoff a, and reflected boundary convention for all Gaussian, K4, OPE, and Schur terms., Same endpoint Wilson sheet basis, same H,K Schur blocks B,E, and exact Wilson quotient policy., No continuum extrapolation, no OS spectral transfer, and no gauge-invariant observable density conclusion.
- Expected observation: Either a phase sector has L_pq(theta)^2>U_pp^+U_qq^+, giving tau_pq(theta)<0 and a finite falsifier, or all phase sectors survive and force full Delta_raw Loewner proof search.
- Transfer certificate needed: A validator-facing raw plaquette interval file certifying I_{prst}^{abcd}(sigma,a,L), OPE intervals, Gaussian covariance, Schur blocks, Hermitian closure, and Wilson-identity quotient invariance before the stress intuition may affect proof obligations.

## Next Experiment

Proof search: compute the first raw K4 interval triple for one endpoint pair p,q in the H,K box, assemble U_pp^+, U_qq^+, and L_pq(theta) at theta in {0,pi/2,pi,3pi/2}, then either output a certified x_stress falsifier or route to full Delta_raw Loewner lower-bound computation.

