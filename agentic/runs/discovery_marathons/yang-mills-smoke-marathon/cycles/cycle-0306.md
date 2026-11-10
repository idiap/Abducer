# cycle-0306

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint source-interval gate for the post-H,K reflected-Wilson block

## Candidate Lemma

Finite C_ep endpoint certificate: for the three-hairpin post-H,K null scalar in heat-kernel plaquette-sheet SU(N), signed endpoint source intervals give a valid promotion certificate I_->0 and a finite same-theory falsifier certificate I_+<0. The claim is only for this finite reflected-Wilson OS block.

## Definitions

- source object: endpoint-class data C_ep={alpha,L_alpha,t_alpha,kappa_alpha,b_12,b_13,b_23,T_tail} obtained from regulated heat-kernel Wilson plaquette-sheet source derivatives.
- target object: the scalar Schur-Feshbach gate G_post for the fixed three-hairpin reflected-Wilson OS matrix after the computed H,K reduction.
- controlled interface: Phi_ep maps same-theory endpoint cumulant intervals and signed null incidences to the interval [I_-,I_+] containing G_post.
- same-theory condition: all Z_alpha, Wilson normalizations, reflection maps, and endpoint limits come from the same regulated gauge-invariant Wilson action with no boundary counterterm or changed observable algebra.
- conceptual pressure: endpoint collapse must be sign-certified inside the same Wilson theory rather than hidden in symbolic R.
- declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint boundary OPE must jointly hold, but H,K plus half-overlap data do not decide G_post.
- efficient representation: encode endpoint source classes, seven source values, cumulant intervals, signed incidences, C_N, M_G, and T_tail; preserve Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; use source differentiation, interval arithmetic, source-equivalence, color multiplication, clipping, incidence contraction, and tail addition; identify carriers only by equal regulated source data; export only [I_-,I_+].

## Assumptions

- Model: four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette action and reflected Wilson hairpin observables.
- Regime: fixed finite three-hairpin collar block after the already computed H,K Schur-Feshbach reduction.
- Cutoff: endpoint boxes have lattice spacing a, heat time t_alpha, and source norm bounded in one injectivity chart, uniformly over the finite block.
- Same-theory: endpoint source derivatives are taken in the locked gauge-invariant Wilson algebra and no boundary OPE counterterm is introduced.
- Uniformity: the remainder E_alpha and T_tail bounds are uniform in the collar-collapse limit for this finite regulator family.
- Local: Wick-square Gram terms and straight f f commutator contacts have already been removed by connected-log and null-incidence cancellations.
- Validity: this is a finite certificate for a Wilson block, not a continuum OS/Wightman reconstruction or a Hamiltonian mass-gap theorem.

## Equations

- endpoint-source-cumulant: `\kappa_\alpha(L)=\left.\partial_s^4\log Z_\alpha(sL)\right|_{s=0},\quad Z_\alpha(sL)=\int_{SU(N)}K_{t_\alpha}(U)e^{s\operatorname{tr}(L X(U))}\,dU`. Valid when: Valid when X(U) is the endpoint logarithm in the heat-kernel plaquette-sheet regulator and the source is inserted in the locked Wilson observable algebra.
- root-quartic-leading-term: `\kappa_\alpha(L)=-\frac{t_\alpha^4}{60}R_4(L)+E_\alpha,\quad R_4(L)=N\operatorname{tr}(L^4)+3(\operatorname{tr}(L^2))^2`. Valid when: Applies for small endpoint heat time inside one SU(N) logarithm chart with bounded source norm and same-theory heat-kernel measure.
- signed-null-incidence: `D_\alpha=2b_{12,\alpha}-4b_{13,\alpha}-4b_{23,\alpha}`. Valid when: Valid after the Feshbach null vector has contracted the three reflected hairpin pair incidences in the fixed H,K block.
- clipped-lower-gate: `I_-=M_G-C_N\sum_\alpha \overline\beta_\alpha [D_\alpha]_+-T_{tail},\quad \overline\beta_\alpha=\frac{t_\alpha^4}{60}R_4(L_\alpha)+\varepsilon_\alpha`. Valid when: Requires negative endpoint cumulant orientation, uniform root-quartic error bounds, and all protective D_alpha<=0 contributions discarded only for a lower bound.
- finite-gate-decision: `G_{post}\in[I_-,I_+],\quad I_->0\Rightarrow G_{post}>0,\quad I_+<0\Rightarrow \det_{OS}<0\ \text{on this block}`. Valid when: Valid when the endpoint interval contains all connected cumulant, endpoint-tail, and cutoff-remainder contributions for the same finite Wilson block.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: endpoint-class data C_ep={alpha,L_alpha,t_alpha,kappa_alpha,b_12,b_13,b_23,T_tail} obtained from regulated heat-kernel Wilson plaquette-sheet source derivatives.; target object: the scalar Schur-Feshbach gate G_post for the fixed three-hairpin reflected-Wilson OS matrix after the computed H,K reduction.; Model: four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette action and reflected Wilson hairpin observables..
- Start with the already reduced three-hairpin Schur-Feshbach scalar G_post=M_G+R_end+R_tail, where M_G is the positive Gaussian margin from H,K.
- Represent R_end by connected source derivatives of endpoint heat-kernel partition functions; the connected log removes Wick-square Gram pieces.
- Use the previously established null-incidence identity to cancel straight C_A f f commutator contacts, leaving only endpoint/corner connected cumulants.
- In SU(N) endpoint logarithm coordinates, expand the heat-kernel/Haar density. The first non-Gaussian fourth cumulant is the negative root-quartic term -(t^4/60)(N tr L^4+3(tr L^2)^2).
- Contract each endpoint class with D_alpha=2b12-4b13-4b23. Since the leading cumulant is negative, only [D_alpha]_+ can lower the gate; D_alpha<=0 is protective.
- Compress endpoint boxes only after verifying source-equivalence, then compute I_-=M_G-C_N sum alpha beta_bar_alpha[D_alpha]_+-T_tail.
- The hard gate is the finite post-H,K reflected-Wilson OS transfer gate: I_->0 promotes this finite block, while I_+<0 gives a same-theory finite falsifier.

Blocking gap: The actual endpoint source classes, fractional incidences b_ij, and a cutoff-uniform T_tail are not yet computed for the target hairpin geometry.

## Falsifiers

- A certified endpoint class with D_alpha>0 and beta_alpha D_alpha larger than M_G/C_N after tail gives a finite same-theory OS falsifier.
- A nonuniform T_tail(a) or large-field endpoint escape demotes the C_ep certificate even if the root-quartic term is safe.
- A required boundary counterterm or changed Wilson normalization violates the same-theory condition and invalidates the transfer.
- Finite source differences for log Z_alpha that disagree with the SU(N) root-quartic interval falsify the proposed local expansion regime.
- Clipping endpoint boxes before source-equivalence can create a false falsifier; this is a stress case for the carrier implementation.

## Learning

Conceptual pressure: endpoint collapse must be sign-certified in the same Wilson theory. Declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular endpoint OPE must coexist without adding a boundary theory, but H,K plus half-overlap data do not decide the scalar. Carrier audit: raw R is representation-limited, raw kappa_4 spectra are too strong, and global Schur-preimage positivity is valid but too coarse after H,K. The sharp value signal is the clipped source-equivalent endpoint interval: negative SU(N) root-quartic cumulants demote only through positive D leakage plus uncontrolled tail. This changes only the finite post-H,K reflected-Wilson OS gate and leaves all Clay continuum, nontriviality, OS/Wightman, and mass-gap gates untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe while the branch remains quarantined for endpoint data.`
- Rationale: The branch has exhausted abstract OS-closed-cone and symbolic R moves; the only decision-grade uncertainty is the signed connected cumulant witness in endpoint source classes.
- Situation seed: In the heat-kernel SU(N) plaquette-sheet regulator, take the fixed three reflected Wilson hairpins after H,K and replace their endpoint overlap pattern by a one-parameter family of fractional endpoint boxes with b12=1 and b13+b23=eta.
- Varied variable: The fractional overlap eta=(b13+b23)/b12, equivalently D=2-4eta, while the endpoint source direction L and heat time t are held fixed.
- Held-fixed controls: Same SU(N) heat-kernel plaquette action and locked gauge-invariant Wilson observable algebra., The computed H,K null vector and Gaussian margin M_G for the finite three-hairpin block., No boundary counterterm, no changed Wilson-loop normalization, and the same reflection map., Uniform root-quartic error epsilon and a fixed tail budget T_tail.
- Expected observation: For eta>=1/2 the half-overlap shield gives D<=0 and the negative root-quartic cumulant is protective; for eta<1/2 the lower interval decreases linearly in 2-4eta and may cross zero, producing a finite falsifier threshold.
- Transfer certificate needed: A validator-facing table of endpoint source derivatives, fractional incidences, C_N, epsilon, and T_tail proving that the observed interval is cutoff-uniform and same-theory before it can affect the finite OS proof queue.

## Next Experiment

Proof-search handoff: compute the validator-facing C_ep table for the actual three-hairpin endpoint boxes in the heat-kernel SU(N) plaquette-sheet regulator, using seven-point finite differences of log Z_alpha as a connected cumulant witness, then test I_->0 versus I_+<0 with uniform E_alpha and T_tail.

# Ward-Hessian sector constants for endpoint R++

## Candidate Lemma

For SU(N) Wilson action with gradient flow, the plus endpoint polarization R_{++}^{ren} has a lower interval: positive pair contraction minus Ward-subtracted C4 sector Hessians and recovery errors. This is finite Route A only.

## Definitions

- source object: centered flowed Wilson hairpin pair W_+(J_i),W_+(J_j) on a finite endpoint box, encoded by H,K sheet currents and endpoint cells.
- target object: finite Schur-Feshbach endpoint-box positivity certificate Q_+>0 after H,K reduction; not OS spectral transfer or a Clay mass-gap theorem.
- controlled interface: same-theory centered flowed Wilson cumulant R_{++}^{ren}=kappa_2(W_+(J_i),W_+(J_j)) enters the Feshbach scalar with explicit recovery error.
- same-theory condition: regulator, flow window, counterterms, sheet-current recovery map, and subtraction scheme are identical for pair term, C4 sectors, and Feshbach input.
- carrier: endpoint sheet currents replace raw contours; they preserve gauge, color, reflection, orientation, cutoff locality, and zero-pairing equivalence.
- sector constants: C_s^{near},C_s^{far} bound Ward-subtracted kernels for s in {3g,4g,ct,end} after plus-channel moment cancellation.

## Assumptions

- Model: SU(N) hypercubic Wilson measure at finite volume with flowed gauge-invariant Wilson hairpins and point-split endpoints.
- Regime: endpoint cell diameter eta << sqrt(t) <= d/4; H,K geometry and Schur-Feshbach leakage L_+ are fixed finite data.
- Cutoff: Ward and cusp counterterms cancel one-hairpin perimeter/cusp divergences uniformly in a and point split epsilon.
- Same-theory: recovery map from sheet currents to Wilson loops has error E_rec and preserves gauge/color/reflection/orientation invariants.
- Local: success changes only finite endpoint-box positivity after H,K; continuum existence, OS axioms, and mass gap remain untouched.

## Equations

- flowed cumulant decomposition: `R_{++}^{ren}=g_t^4(N^2-1)\left(2G_{++}+N\sum_{s\in\mathcal S}I_s^{WS}\right)+E_6+E_{rec}`. Valid when: Valid when centered flowed hairpins are expanded to order g_t^4 with Ward/cusp subtractions and fixed endpoint geometry.
- Ward-Hessian sector majorant: `|I_s^{WS}|\le \left(C_s^{near}(t,\rho)+C_s^{far}(t,\rho,d)\right)M_{2,+}^2`. Valid when: Requires the Ward-subtracted four-curvature kernel to be C^2 on every endpoint cell after the near-diagonal heat-kernel split.
- endpoint promotion interval: `R_{++}^{-}=g_t^4(N^2-1)\left(2G_{++}^{-}-N C_4^{+}M_{2,+}^2\right)-E_6^{+}-E_{rec}^{+},\quad R_{++}^{-}>L_+\Rightarrow Q_+>0`. Valid when: Applies only after the finite Schur-Feshbach theorem supplies L_+ for the same H,K endpoint vector and recovery map.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: centered flowed Wilson hairpin pair W_+(J_i),W_+(J_j) on a finite endpoint box, encoded by H,K sheet currents and endpoint cells.; target object: finite Schur-Feshbach endpoint-box positivity certificate Q_+>0 after H,K reduction; not OS spectral transfer or a Clay mass-gap theorem.; Model: SU(N) hypercubic Wilson measure at finite volume with flowed gauge-invariant Wilson hairpins and point-split endpoints..
- Encode the H,K plus endpoint vector as a sheet current j_+; raw Wilson contours are rejected as fragmented because moment cancellation is not primitive there.
- Expand the centered flowed cumulant kappa_2(W_+(J_i),W_+(J_j)); disconnected products, one-hairpin cusp terms, and Ward-longitudinal pieces cancel.
- Partition endpoint boxes; Taylor expand Ward-subtracted C4 kernels. Plus monopole/dipole cancellation leaves Hessian terms controlled by M_{2,+}^2.
- Insert the sector interval in the Schur-Feshbach scalar: R_{++}^{-}>L_+ proves finite endpoint positivity, while the opposite inequality is a falsifier.

Blocking gap: No outward-rounded numerical or analytic constants yet for C_s^{near}, C_s^{far}, E_6, and E_rec in the fixed H,K endpoint geometry.

## Falsifiers

- Ward/cusp subtraction leaves an epsilon- or a-dependent residue in any C4 sector, invalidating same-theory transfer.
- The zero-pairing quotient changes the positive pair baseline G_{++} or violates gauge/color/orientation recovery.
- Outward-rounded sector constants are too wide or too negative, giving R_{++}^{-}<=L_+ for the fixed H,K box.
- No stable flow-window plateau exists as volume and cutoff vary; this falsifier demotes the endpoint R repair.

## Learning

Pressure: finite Feshbach positivity needs a same-theory Wilson mediator. Tension: pair covariance and flow renormalization are valid but C4 can erase them. Endpoint currents beat fragmented contours and coarse OS/non-Gaussian routes. Value: R++ becomes a sector-constant interval.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for certified sector constants.`
- Rationale: The branch needs a concrete complexity-reducing experiment because the abstract R term is already decomposed; only cutoff-stable Ward-Hessian constants can change the proof state.
- Situation seed: Finite SU(3) Wilson lattice with gradient-flow observables for the fixed H,K endpoint hairpin box; compute interval enclosures for sectors I_3g,I_4g,I_ct,I_end.
- Varied variable: Near/far split ratio rho/sqrt(t) in the Ward-Hessian enclosure.
- Held-fixed controls: Same H,K sheet-current geometry, endpoint separation d, plus-channel current, and Schur-Feshbach leakage L_+., Same Wilson action, gradient-flow definition, cusp/Ward counterterms, recovery map, and outward-rounded interval arithmetic.
- Expected observation: A plateau where C_4^{+}M_{2,+}^2 is eta^2-suppressed relative to 2G_{++}^{-}, or a certified interval showing R_{++}^{-} cannot beat L_+.
- Transfer certificate needed: Cutoff- and volume-stable interval proof for all sector constants plus a same-theory recovery-error bound before intuition may enter proof obligations.

## Next Experiment

Proof search: derive and interval-enclose C_s^{near/far} for I_3g,I_4g,I_ct,I_end in the fixed H,K box, with outward rounding and recovery errors; validator-facing same-theory nontriviality witness boundary remains a non-claim.

# Raw K4 Phase-Stress Certificate For Post-H,K Wilson Endpoint Positivity

## Candidate Lemma

Raw-K4 phase-stress lemma. For a fixed heat-kernel cutoff SU(N) endpoint box, if interval arithmetic certifies U_pp<=D_p, U_qq<=D_q, and Re(e^{-i theta}U_pq)>=L with D_q>0 and D_p-L^2/D_q<0, then the Schur-corrected post-H,K endpoint form is not positive semidefinite. This is a finite falsifier for the worked collar/hairpin route only.

## Definitions

- source object: heat-kernel regulated SU(N) Wilson endpoint data consisting of endpoint sheets, transported plaquette curvatures, same-cutoff covariance C_sigma, connected four-curvature cumulant K4_sigma, OPE interval E_sigma, and H,K Schur blocks.
- target object: the finite Schur-corrected endpoint quadratic form U_sigma=R_sigma-S_HK on the span of two endpoint vectors e_p,e_q; it is not a Hamiltonian spectral gap statement.
- controlled interface: the connected cumulant witness map (Wilson plaquette data)->(intervals D_p,D_q,L and stress vector x_theta) preserving gauge invariance, reflection support, color factors, and Schur subtraction.
- same-theory condition: C_sigma, K4_sigma, E_sigma, H, and K are computed with the same regulator, coupling, Wilson normalization, endpoint basis, and quotient by exact Wilson identities.
- endpoint observable: Q_i=(g_R^2/(4N)):\sum_a Phi_{i,sigma}^a Phi_{i,sigma}^a: is the vacuum/perimeter-subtracted quadratic flux carrier.
- bridge property: a negative Rayleigh value x^*U_sigma x<0 demotes endpoint-box positivity but does not address gauge-invariant observable density or excitation-sector cyclicity.

## Assumptions

- Model: four-dimensional SU(N) Yang-Mills at finite heat-kernel cutoff sigma with a finite Wilson endpoint-box basis and fixed H,K hairpin/collar data.
- Regime: endpoint sheets are small relative to the OPE radius and sigma/a is fixed, so the plaquette flux expansion and interval OPE remainder are meaningful.
- Same-theory: the Gaussian covariance, connected kappa4 intervals, OPE errors, and Schur energy B^*E^{-1}B are all extracted from one cutoff measure and one Wilson normalization.
- Validity: interval endpoints are outward-rounded, color conventions use tr(T^aT^b)=delta^{ab}/2, and quotienting uses only exact trace and orientation identities.
- Constraint: D_p and D_q are diagonal upper enclosures of U_sigma, while L is a lower enclosure for the chosen phased off-diagonal real part.

## Equations

- transported flux: `\Phi_{i,\sigma}^{a}=\sum_{\pi\in S_i} w_i(\pi)\,\mathrm{Ad}(U_{r\pi})^{ab}\,F_{\sigma}^{b}(\pi)`. Valid when: Valid when endpoint sheet S_i is fixed at cutoff sigma and parallel transporters are taken from the same Wilson regulator.
- connected boundary polarization: `R_{ij,\sigma}=\operatorname{cum}_2(Q_i,Q_j)=\alpha_N g_R^4\,(C_{ij,\sigma}\circ C_{ij,\sigma})+\frac{g_R^4}{16N^2}K4_{ij,\sigma}+E^{\mathrm{OPE}}_{ij,\sigma},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after vacuum and perimeter normalization, with Wick-normalized quadratic fluxes and same-regulator connected four-curvature cumulants.
- Schur-corrected endpoint matrix: `U_{\sigma}=R_{\sigma}-S_{HK,\sigma},\qquad S_{HK,\sigma}=B_{\sigma}^{*}E_{\sigma}^{-1}B_{\sigma}`. Valid when: Valid when the H,K hairpin block E_sigma is positive on the eliminated sector and the endpoint basis is unchanged.
- two-sparse stress margin: `\tau_{pq}(\theta)=D_p-\frac{L_{pq}(\theta)^2}{D_q}<0`. Valid when: Requires D_p,D_q,L_pq(theta) to be certified interval enclosures for the same two-by-two compression of U_sigma.
- stress vector: `x_{pq,\theta}=e_p-\frac{L_{pq}(\theta)}{D_q}e^{-i\theta}e_q,\qquad x_{pq,\theta}^{*}U_{\sigma}x_{pq,\theta}\le \tau_{pq}(\theta)`. Valid when: Valid when D_q is strictly positive and the phased off-diagonal lower bound is positive in the certified interval sector.

## Attempted Derivation

- Attack conceptual pressure: turn the connected boundary-OPE polarization R into a route-deciding finite witness, not another symbolic R or OS-density restatement.
- Freeze the model: finite heat-kernel cutoff SU(N), fixed endpoint sheets, fixed H,K Schur data, and one Wilson normalization.
- Use non-Abelian Stokes/OPE expansion only to the declared order: vacuum and perimeter terms cancel after normal ordering, leaving Q_i=(g_R^2/(4N)):Phi_i^2: plus OPE remainder.
- Separate R_ij into the positive Gaussian crossed-curvature contraction alpha_N g_R^4(C o C)_ij, the connected non-Gaussian K4 term, and E_OPE.
- Compress after eliminating hairpin variables by Schur-Feshbach: U=R-B^*E^{-1}B.
- For endpoints p,q and phase theta, enclose U_pp,U_qq and Re(e^{-i theta}U_pq) by D_p,D_q,L.
- Choose rho=L/D_q and x=e_p-rho e^{-i theta}e_q. Interval arithmetic gives x^*Ux<=D_p-L^2/D_q.
- If tau<0, the finite endpoint form is not PSD and the worked H,K endpoint route is falsified for this geometry.

Blocking gap: The missing object is the first same-regulator raw K4 interval I^{K4}_{pq} for a named endpoint pair in the actual H,K geometry; without it L_pq(theta) remains a proof-search target rather than a computed certificate.

## Falsifiers

- falsifier: a certified tau_pq(theta)<0 gives a negative Rayleigh vector and demotes the finite H,K endpoint positivity route.
- falsifier: raw K4 intervals cannot be obtained in the same regulator as C_sigma, E_OPE, and S_HK.
- falsifier: Wilson quotient auditing identifies e_p and e_q or changes the phased off-diagonal sign, invalidating the stress vector.
- falsifier: all phase sectors satisfy tau_pq(theta)>=0 with tight intervals, forcing abandonment of the two-sparse negative tactic and return to full Delta_raw search.
- falsifier: the connected four-curvature intervals include disconnected Gaussian pairings, double-counting the PSD color square.
- falsifier: diagonal upper intervals D_p,D_q are too wide to give a valid Rayleigh conclusion.

## Learning

Declarative tension: Wilson/OPE coefficients, connected K4 negativity, OPE errors, and H,K Schur subtraction must jointly control one endpoint quadratic form in one cutoff theory, while gauge-invariant observable density, OS reconstruction, nontrivial continuum YM, and Hamiltonian mass gap must remain non-claims. Carrier critique: scalar R is representation-limited, OS Hilbert observable algebra is too strong and circular for this local gate, A012 shells are convenient but quarantined, and raw plaquette enumeration is fragmented yet valid. Compared with full Delta_raw PSD search, the phase-stress route is sharper as a negative tactic because three same-theory intervals can falsify endpoint positivity. Efficient representation requirements are fixed: encode oriented plaquettes, sheet weights, transporters, color tensors, cumulant intervals, OPE intervals, endpoint indices, and Schur blocks; preserve gauge invariance, reflection support, Gaussian/K4 separation, endpoint compression, same-theory normalization, and exact Wilson quotienting; support cumulant contraction, interval summation, phase-sector certification, Rayleigh stress search, Loewner bounds, and Schur subtraction; transfer only through Delta_raw or x_stress; expose falsifiers by negative margin, missing intervals, non-invariant quotienting, or regulator mismatch. Hard gate: tau_pq(theta)<0 demotes the finite H,K endpoint route; survival forces full Delta_raw proof search. Conceptual value signal: sharp and explanatory at finite scope because R becomes a connected cumulant witness with explicit color, geometry, non-Gaussian K4, OPE, and Schur data in one valid inequality.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the finite endpoint-box route.`
- Rationale: The branch has exhausted abstraction cycles; the next valid information is whether an actual same-regulator connected cumulant witness can make the two-sparse Rayleigh margin negative.
- Situation seed: Fixed heat-kernel SU(N) Wilson endpoint box for the worked H,K collar/hairpin geometry, with endpoint pair p,q, exact Schur block S_HK, computed Gaussian covariance C_sigma, and raw plaquette K4 intervals for the off-diagonal polarization.
- Varied variable: The phase-aligned off-diagonal connected K4 lower interval, equivalently xi=inf Re(e^{-i theta}K4_pq)/(sqrt(D_pD_q)) over a discrete phase sector.
- Held-fixed controls: Same Wilson endpoint basis, sheet weights, heat-kernel cutoff sigma, coupling g_R, and fundamental SU(N) color normalization., Same H,K Schur subtraction B^*E^{-1}B and same OPE remainder budget for every tested phase., Exact Wilson trace/orientation quotient policy and finite endpoint-box locality budget., Clay-level gates held fixed as non-claims: continuum existence, OS positivity, observable density, and spectral mass gap.
- Expected observation: If the actual K4 off-diagonal interval is phase-coherent enough that L_pq(theta)^2>D_pD_q, the stress margin becomes negative; otherwise the two-sparse tactic is demoted and full Delta_raw positivity search becomes the only local route.
- Transfer certificate needed: A rigorous same-regulator plaquette-quadruple interval enclosure for K4_pq, an exact quotient audit, and an outward-rounded calculation of D_p,D_q,L_pq(theta) before the intuition may affect proof obligations.

## Next Experiment

Proof search: choose the first endpoint pair p,q from the H,K endpoint box, enumerate its oriented plaquette quadruples, compute the same-regulator connected K4 interval I^{K4}_{pq}, combine it with Gaussian color square, OPE, and Schur intervals, then test tau_pq(theta)<0 over a small phase grid; if no interval appears, quarantine the two-sparse tactic and hand off to full Delta_raw. Include marker audits: connected cumulant witness, gauge-invariant observable density quarantined, vacuum-orthogonal spectral witness non-claim.

