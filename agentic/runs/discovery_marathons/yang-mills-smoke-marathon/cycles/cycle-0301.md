# cycle-0301

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint source interval carrier for the post-H,K Wilson hairpin gate

## Candidate Lemma

For an SU(N) heat-kernel plaquette-sheet endpoint box, the same-theory connected fourth source cumulant has leading negative Haar-Jacobian term, but the finite post-H,K OS gate sees it only through the signed null-incidence scalar D_v. Thus endpoint collapse is demoted or promoted by a scalar interval, not by raw negativity of kappa_4.

## Definitions

- source object: regulated SU(N) heat-kernel plaquette-sheet endpoint boxes v with endpoint partition functions Z_v(s;L_v), locked Wilson source directions L_v, fractional overlaps b_{ij}(v), and cutoff a.
- target object: the finite post-H,K reflected-Wilson Schur-Feshbach scalar I_gate for the three-hairpin OS block, not a continuum Yang-Mills mass-gap statement.
- controlled interface: endpoint source carrier C_ep=(Z_v,L_v,b_{ij},C_N,M_G,T_tail) maps connected cumulant intervals to I_gate by signed incidence contraction, color multiplication, clipping, and tail addition.
- same-theory condition: all Z_v are obtained from the same heat-kernel Wilson plaquette-sheet regulator and Wilson normalization as the collar observables, with no boundary counterterm, no changed observable algebra, and cutoff-uniform tails.
- Endpoint source cumulant: kappa_v(L_v)=d_s^4 log Z_v(s;L_v)|_{s=0}, a connected cumulant witness for the boundary OPE endpoint.
- Null incidence: D_v=2b_{12}(v)-4b_{13}(v)-4b_{23}(v), with b_{ij} measured in the same endpoint box and source class.
- Root quartic: R4(L)=sum_{alpha>0} alpha(L)^4=N tr_F(L^4)+3(tr_F(L^2))^2 for traceless diagonalized L under tr_F(T^aT^b)=delta^{ab}/2 conventions up to the stated generator normalization.

## Assumptions

- Model: four-dimensional SU(N) lattice Yang-Mills with Wilson heat-kernel plaquette action and reflection plane endpoint boxes for the worked three-hairpin finite block.
- Regime: endpoint coordinates satisfy ||L_v|| t_v^{1/2} below the injectivity-radius scale and box diameters are smaller than the collar separation scale before collapse.
- Cutoff: all cumulant and tail bounds are uniform for the regulator sequence used in the collar-to-endpoint limiting procedure.
- Same-theory: the source insertion differentiates the same locked gauge-invariant Wilson observables used to define H,K,N,B; no boundary field or renormalized plane algebra is added.
- Validity: Wick-square Gram terms and straight C_A f f contacts have already been removed by the prior H,K null-channel cancellations; this lemma estimates the remaining endpoint connected cumulant only.
- Local: source-equivalent endpoint boxes may be aggregated only after equality of the seven regulated source values, then incidences are summed before multiplying by kappa intervals.
- Constraint: this is a finite Wilson block gate; it does not assert continuum existence, OS density for all observables, nontriviality, or a Hamiltonian mass gap.

## Equations

- endpoint_source_cumulant: `\kappa_v(L_v)=\left.\frac{d^4}{ds^4}\log Z_v(s;L_v)\right|_{s=0}`. Valid when: Valid when Z_v is the same regulated heat-kernel endpoint partition function differentiated along the locked Wilson source direction.
- haar_root_quartic_leading_term: `\kappa_v(L_v)=-\frac{t_v^4}{60}\,R_4(L_v)+E_v,\qquad R_4(L)=\sum_{\alpha>0}\alpha(L)^4`. Valid when: Applies in exponential endpoint coordinates before caustics, with Haar-Jacobian expansion and cutoff-uniform control of higher root terms.
- suN_root_quartic_trace_form: `R_4(L)=N\operatorname{tr}_F(L^4)+3\big(\operatorname{tr}_F(L^2)\big)^2\quad (L\in\mathfrak{su}(N),\ \operatorname{tr}_F L=0)`. Valid when: Valid for SU(N) after diagonalizing L and using the stated fundamental trace normalization for roots.
- signed_endpoint_gate_interval: `I_{\rm gate}\in M_G+C_N\sum_v D_v\,[\kappa_v^-,\kappa_v^+]+[-T_{\rm tail},T_{\rm tail}]`. Valid when: Requires the prior Schur-Feshbach H,K reduction, same-theory endpoint source intervals, and uniform localization of all non-endpoint remainders.
- half_overlap_shield: `D_v\le 0\quad\Longleftarrow\quad b_{13}(v)+b_{23}(v)\ge \frac{1}{2}b_{12}(v)`. Valid when: Valid when the fractional endpoint incidences are measured in one source-equivalence class before clipping or tail allocation.

## Attempted Derivation

- Freeze Clay target and claim level: this cycle attacks endpoint-collapse sign certification inside the same Wilson theory; success affects only the finite post-H,K reflected-Wilson OS transfer gate, while continuum construction, full OS/Wightman reconstruction, nontriviality, and mass gap remain untouched.
- Use exponential coordinates U=exp X in one endpoint box. The SU(N) Haar density contributes log j(X)=2 sum_{alpha>0} log(sin(alpha(X)/2)/(alpha(X)/2)).
- Expand log j(X)=-sum_{alpha>0} alpha(X)^2/12 - sum_{alpha>0} alpha(X)^4/1440 + O(||X||^6).
- Insert a heat-kernel Gaussian source sL_v. Shifting the Gaussian mean by t_v s L_v gives the fourth source derivative of the quartic Haar term as -24 t_v^4/1440 sum_{alpha>0} alpha(L_v)^4=-(t_v^4/60)R4(L_v).
- Convert the root quartic to trace form for SU(N): sum_{i<j}(lambda_i-lambda_j)^4=N sum_i lambda_i^4+3(sum_i lambda_i^2)^2.
- Feed kappa_v into the already reduced null-channel endpoint scalar: R_end=C_N sum_v D_v kappa_v plus T_tail, with D_v=2b12-4b13-4b23.
- Observe the explanatory sign: kappa_v is negative at leading order, but boxes satisfying b13+b23>=b12/2 have D_v<=0 and are protective, so only certified positive-D endpoint dominance is dangerous.
- Conceptual carrier audit: raw R is representation-limited because it hides D_v; raw kappa_4 spectrum is too strong because it ignores incidence; the global Schur-preimage route is valid but too coarse after H,K; C_ep is the efficient local carrier.

Blocking gap: The proof still lacks cutoff-uniform bounds for E_v and T_tail and lacks actual seven-point source intervals for every positive-D source class.

## Falsifiers

- A positive-D endpoint source class whose certified interval gives M_G+C_N sum D_v kappa_v+T_tail strictly negative is a finite same-theory falsifier for the post-H,K OS gate.
- The sixth-order Haar/action remainder E_v is not cutoff-uniform in the endpoint collapse, invalidating the claimed interval carrier.
- A boundary counterterm is needed to define Z_v or kappa_v at the reflection plane, violating the same-theory condition.
- Two geometrically similar endpoint boxes have different regulated source stencils, so source-equivalence compression would be false.
- A tail contribution from corner topology or large fields is not summable across endpoint boxes and overwhelms the Gaussian margin.
- The heat-kernel endpoint coordinates exit the injectivity regime before the collar limit, making the root-quartic expansion invalid.

## Learning

Cycle 301 upgrades quarantine into a sharper proof-search handoff. The conceptual pressure is endpoint collapse in the same Wilson theory. The declarative tension is finite collar OS positivity plus fixed gauge-invariant Wilson observables plus singular connected endpoint boundary OPE, with no boundary theory allowed. The carrier audit is decisive: raw R is too weak, raw kappa_4 spectra are too strong, and the global Schur-preimage test is valid but too coarse after H,K. The efficient representation is C_ep: endpoint source classes, seven source values, kappa intervals, signed fractional incidences, C_N, M_G, and T_tail; it preserves Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; it uses source differentiation, interval arithmetic, source-equivalence, color multiplication, clipping, incidence contraction, and tail addition; equivalence is equality of regulated source data; locality cost is charged to T_tail; transfer exports only [I_-,I_+]. The new computation is the SU(N) Haar root-quartic term kappa_v=-(t_v^4/60)R4(L_v)+E_v with R4=N tr L^4+3(tr L^2)^2. This is sharp and explanatory because negative endpoint kappa_4 is not the falsifier; only positive-D endpoint dominance plus uncontrolled tail can demote the finite gate.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe while the branch remains quarantined for data.`
- Rationale: The branch has a finite carrier but no endpoint source values. A concrete target-preserving thought experiment can test whether positive-D endpoint dominance can realistically overcome the Gaussian margin without changing the Wilson theory.
- Situation seed: Three reflected Wilson hairpins in the SU(N) heat-kernel plaquette-sheet regulator, with endpoint boxes grouped by equal seven-point source stencils and evaluated as connected cumulant witness data for the finite post-H,K OS gate.
- Varied variable: fractional overlap ratio eta=(b13+b23)/b12 inside a fixed positive-D candidate endpoint class.
- Held-fixed controls: Fixed SU(N), heat-kernel Wilson plaquette action, reflection plane, and locked gauge-invariant Wilson source normalization., Fixed Schur-Feshbach null vector and previously computed H,K cancellations, including Wick-square Gram positivity and straight C_A f f null-incidence cancellation., Fixed color factor C_N, Gaussian margin M_G, endpoint box scale t_v, and no boundary counterterm same-theory condition.
- Expected observation: For eta>=1/2 the leading negative root-quartic cumulant is protective; for eta<1/2 the interval decreases linearly with D_v and can become a falsifier only if the certified negative cumulant plus tail exceeds M_G.
- Transfer certificate needed: A cutoff-uniform seven-point source interval for kappa_v, a valid E_v and T_tail bound, and source-equivalence proof that the thought-experiment endpoint class is realized by the locked Wilson observables.

## Next Experiment

Proof search plus endpoint data computation: for each realized positive-D source-equivalence class, evaluate the seven-point heat-kernel source stencil for log Z_v, certify kappa_v=-(t_v^4/60)R4(L_v)+E_v, add C_N D_v and T_tail intervals, and return the scalar sign [I_-,I_+] for the finite post-H,K OS gate.

# Gauge-Invariant Nontriviality Witness Selection: endpoint R/kappa4 Ward-Hessian certificate

## Candidate Lemma

Finite endpoint-cell Ward-Hessian enclosure: for the actual H,K plus-channel endpoint sheet current, the connected boundary-OPE polarization in the flowed Wilson covariance has a certified lower interval equal to the positive pair baseline minus a Ward-Hessian C4 majorant and recovery errors.

## Definitions

- source object: finite-cutoff SU(N) Wilson lattice measure on a four-torus with gradient-flowed gauge field B_t and centered renormalized hairpin Wilson observables W_t^{ren}(J).
- target object: a finite endpoint-box lower interval for R_{++}^{ren} strong enough to compare with the Schur-Feshbach leakage L_+; this is not a continuum mass-gap statement.
- controlled interface: endpoint sheet-current representation J_+ -> centered flowed Wilson cumulant kappa_2(W_t^{ren}(J_+^1),W_t^{ren}(J_+^2)) with Ward/cusp subtraction and certified recovery errors.
- same-theory condition: all pair, connected C4, counterterm, and recovery terms are computed in the same cutoff action, flow time, boundary observable normalization, and limiting Schwinger family.
- Regulator: Wilson plaquette action at lattice spacing a plus Yang-Mills gradient flow time t and boundary point-splitting eta.
- Carrier: H,K hairpins are replaced by oriented flowed plaquette sheets with endpoint currents j_C on endpoint cells C.
- Cancellation: subtract disconnected products and one-hairpin perimeter/cusp counterterms before extracting the connected cumulant.
- Moment data: M_{2,+}^I is the interval upper bound for the second centered endpoint moment after plus-channel monopole and dipole cancellation.
- Kernel data: H_{4,++}^{I,+}=H_{near}^{I,+}+H_{far}^{I,+}+H_{ct}^{I,+}+H_{end}^{I,+} is the interval Hessian majorant for the Ward-subtracted connected four-curvature sector.

## Assumptions

- Model: SU(N), N>=2, Wilson plaquette lattice gauge theory on a reflection-symmetric finite four-torus; the lemma is finite-cutoff and finite-volume.
- Regime: a^2 << t, endpoint cell diameter eta <= sqrt(t)/4, and distinct endpoint boxes separated by d >= 8 sqrt(t).
- Cutoff: flowed composite fields and Wilson hairpins use the same a,t,eta and the same cusp/perimeter subtraction constants.
- Uniformity: interval constants are required to be stable under one dyadic endpoint-cell refinement and one halving of a at fixed physical t,eta,d.
- Same-theory: no imported continuum Schwinger function or auxiliary Gaussian theory may replace the Wilson measure used in the cumulant.
- Validity: the expansion is used only through the finite endpoint-box cumulant order needed for the Route A positivity test, with E_6 bounding the remainder.
- Constraint: plus-channel endpoint currents have certified zero total charge and zero first moment after reflection/orientation pairing.

## Equations

- endpoint connected cumulant: `R_{++}^{ren}(t,\eta,a)=\kappa_2\!\left(W_t^{ren}(J_{+,1}),W_t^{ren}(J_{+,2})\right)_{end,cusp\,sub}`. Valid when: Valid when the two centered flowed hairpin observables use the same Wilson measure, flow time, point splitting, and cusp-subtracted normalization.
- positive pair baseline: `P_{++}^{I,-}=g_t^4\,2(N^2-1)\,G_{++}^{I,-},\quad G_{++}=\int_{\Sigma_1\times\Sigma_2} q_1^{\mu\nu}(x)\,D^{t}_{\mu\nu,\rho\sigma}(x-y)\,q_2^{\rho\sigma}(y)\,dx\,dy`. Valid when: Valid when the flowed two-curvature contraction is evaluated in the endpoint sheet-current representation after disconnected and one-hairpin terms are removed.
- Ward-Hessian C4 majorant: `|C_{4,++}^{WS,I}|\le g_t^6\,N(N^2-1)\,H_{4,++}^{I,+}\,(M_{2,+}^{I})^2`. Valid when: Valid when Ward subtraction and plus-channel monopole and dipole cancellation hold on every certified endpoint cell before Taylor expansion.
- near-far Hessian split: `H_{4,++}^{I,+}=H_{near}^{I,+}+H_{far}^{I,+}+H_{ct}^{I,+}+H_{end}^{I,+},\quad H_{far}^{I,+}\le C_F\sum_{C,D}\frac{e^{-r_{CD}^2/(16t)}|C||D|}{(r_{CD}^2+t)^6}`. Valid when: Applies when cells with r_CD at least two eta are treated by heat-kernel far bounds and the remaining cells by near-cell L1-Linfty bounds.
- route-deciding lower interval: `R_{++}^{ren,I,-}=g_t^4(N^2-1)\left(2G_{++}^{I,-}-g_t^2 N H_{4,++}^{I,+}(M_{2,+}^{I})^2\right)-E_{rec}^{I,+}-E_6^{I,+}`. Valid when: Valid when pair, C4, counterterm, endpoint, recovery, and sixth-order remainder intervals are all produced from the same cutoff Wilson ensemble.
- promotion inequality: `R_{++}^{ren,I,-}>L_+ + \Delta_{safe}`. Valid when: Requires the finite Schur-Feshbach leakage L_+ and the Wilson endpoint cumulant interval to be normalized in the same H,K basis.

## Attempted Derivation

- Freeze claim level: prove only a finite endpoint-box interval certificate for Route A; do not claim Clay existence, OS/Wightman reconstruction, nontrivial continuum limit, observable density, or Hamiltonian mass gap.
- Represent the actual H,K plus-channel hairpins by oriented endpoint sheet currents J_+ and apply Rec_{a,t,eta} to centered flowed Wilson observables.
- Expand the centered cusp-subtracted Wilson covariance through the endpoint cumulant: the disconnected product and one-hairpin perimeter/cusp pieces cancel by construction.
- Evaluate the order g_t^4 pair contraction; color trace gives 2(N^2-1), and the endpoint geometry is stored in G_{++}^{I,-}.
- Isolate the connected four-curvature polarization C_{4,++}^{WS}; color routing gives N(N^2-1), with sectors 3g, 4g, counterterm, and endpoint-contact.
- Use Ward subtraction plus plus-channel reflection/orientation cancellation to certify zero monopole and dipole moments on endpoint cells.
- Taylor expand the Ward-subtracted sector kernels about cell centers; the first surviving term is bounded by H_{4,++}^{I,+}(M_{2,+}^{I})^2.
- Split H4 into near cells controlled by flowed heat-kernel L1-Linfty bounds and far cells controlled by exponential heat-kernel tails; add counterterm, endpoint-contact, recovery, and E6 intervals.
- Combine the positive pair baseline and negative C4 majorant to form R_{++}^{ren,I,-}; compare with the fixed Schur-Feshbach leakage L_+.

Blocking gap: The near-cell constants H_near^{I,+} and the recovery error E_rec are not yet numerically enclosed for the actual H,K endpoint mesh with outward rounding.

## Falsifiers

- falsifier: the actual H,K plus-channel endpoint current has a nonzero certified monopole or dipole moment after Ward/cusp subtraction.
- falsifier: the near-cell Hessian interval scales too strongly as eta -> 0 and destroys the eta^2 endpoint-moment suppression.
- falsifier: the connected C4 interval is negative enough that R_{++}^{ren,I,-} <= L_+ for every stable flow window.
- falsifier: zero-pairing quotienting changes the pair baseline G_{++}^{I,-} or the Schur-Feshbach normalization.
- falsifier: recovery errors or sixth-order remainders dominate the positive pair term under cutoff refinement.
- A valid demotion occurs if the interval has no plateau under a halving of a and one dyadic endpoint-cell refinement.

## Learning

Conceptual pressure attacked: the missing same-theory mediator between finite Schur-Feshbach endpoint positivity and Wilson cumulant positivity. Declarative tension: positive flowed pair covariance, same-theory renormalization, and finite endpoint positivity can all be individually valid while connected C4 erases the pair term unless Ward-Hessian constants and recovery errors are certified. Carrier critique: raw Wilson contours are fragmented and representation-limited; global OS spectral transfer and a non-Gaussian Schwinger family route are too coarse for this local obstruction. Better abstraction: endpoint sheet currents with cell moments, sector kernels, counterterms, recovery errors, Ward/cusp subtraction, heat-kernel Hessian bounds, interval quadrature, outward rounding, and certified zero-pairing quotienting. Efficient representation must encode H,K sheets, endpoint currents, moments, kernels, counterterms, and errors; preserve gauge, color, reflection, orientation, cutoff, locality, and same-theory identity; keep finite endpoint-cell locality and bounded refinement; transfer only through centered flowed Wilson cumulants; demote on any falsifier. Hard gate: finite endpoint-box positivity after H,K. Conceptual value signal: R_{++}/kappa_4 is now a valid route-deciding color-geometric interval certificate, not a symbolic endpoint term; success promotes one finite Route A gate, failure quarantines this R repair, while Clay existence, OS/Wightman axioms, nontrivial continuum limit, observable density, large-field/topology control, and positive Hamiltonian mass gap remain unclaimed.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and proof-search guide, not as evidence for the Clay theorem.`
- Rationale: The branch is blocked by a concrete sign/size certificate for the connected boundary-OPE polarization R_{++}; another abstract OS or Wilson obstruction restatement would not change the proof state.
- Situation seed: Finite SU(N) Wilson lattice on a reflection-symmetric four-torus with the actual post-H,K plus-channel endpoint boxes, flowed at time t, represented by endpoint sheet currents and tested as a connected cumulant witness in the same theory.
- Varied variable: theta=eta/sqrt(t), the endpoint-cell diameter relative to flow radius.
- Held-fixed controls: Gauge group SU(N), the H,K plus-channel geometry, and the Schur-Feshbach leakage L_+ are fixed., The Wilson action, gradient-flow definition, cusp/perimeter subtraction, and centered observable normalization are fixed., Endpoint-box separation d/sqrt(t) and finite-volume aspect ratio are held fixed., Only same-theory flowed Wilson cumulants are used; no Gaussian replacement or continuum spectral-transfer hypothesis is imported.
- Expected observation: If Ward-Hessian suppression is real, H4(theta) M2(theta)^2 decreases like O(theta^2) relative to the positive G_{++} pair baseline over a nonempty theta window; if not, the lower interval crosses below L_+ and the endpoint repair is falsified.
- Transfer certificate needed: Certified recovery map Rec_{a,t,eta}, Ward/cusp cancellation audit, outward-rounded near/far interval constants, cutoff-refinement plateau, and normalization match to the finite H,K Schur-Feshbach basis.

## Next Experiment

Route to proof search: build the validator-facing endpoint-cell packet for the actual H,K plus-channel geometry, compute G_{++}^{I,-}, M_{2,+}^{I}, H_near^{I,+}, H_far^{I,+}, E_rec^{I,+}, and E6^{I,+}, then test the connected cumulant witness inequality R_{++}^{ren,I,-} > L_+ + Delta_safe under one cutoff and one endpoint-refinement check.

# Raw K4 two-sparse stress certificate for post-H,K Wilson endpoint positivity

## Candidate Lemma

Two-sparse raw K4 stress lemma: in a fixed heat-kernel cutoff theory, a certified negative interval upper bound for one phase-aligned two-sparse Rayleigh quotient of the Schur-corrected endpoint form U_sigma is a valid falsifier for finite post-H,K endpoint-box positivity.

## Definitions

- source object: same-cutoff heat-kernel SU(N) lattice Yang-Mills endpoint data consisting of reflected Wilson sheet weights, transported plaquette-pair covariance C_sigma, raw connected four-curvature cumulant intervals K4_sigma, OPE interval E_OPE, and H,K Schur blocks.
- target object: the finite Schur-corrected endpoint quadratic form U_sigma on the post-H,K Wilson endpoint span; positivity of this finite form is the only local Route A claim.
- controlled interface: the recovery map Rec_raw sending raw plaquette cumulant intervals and Wilson weights to interval enclosures for every 2x2 principal compression of U_sigma.
- same-theory condition: all C_sigma, K4_sigma, E_OPE, and S_HK are computed with the identical cutoff, heat-kernel regulator, coupling normalization, reflected Wilson basis, and endpoint compression.
- observable manipulated: the connected cumulant witness R_ij=cum_2(Q_i,Q_j) for vacuum-subtracted Wilson endpoint flux squares Q_i.
- larger YM gate changed: only the finite Route A endpoint-box positivity gate; OS reconstruction, nontrivial continuum limit, gauge-invariant observable density, and physical-unit mass gap remain untouched.

## Assumptions

- Model: four-dimensional finite-volume hypercubic SU(N) Yang-Mills with heat-kernel plaquette action and reflection plane chosen before endpoint compression.
- Cutoff: lattice spacing a, smoothing scale sigma, endpoint box, and Wilson sheet set are fixed throughout the certificate.
- Same-theory: the Gaussian covariance, raw K4 intervals, OPE bounds, and Schur blocks are all extracted from the same regulated measure and normalization.
- Local: only finitely many oriented plaquettes and sheet-pair weights occur; no volume-uniform or continuum assertion is made.
- Validity: the H,K complement block E_sigma is strictly positive on the finite eliminated hairpin subspace, so the Schur subtraction is defined.
- Constraint: quotienting is allowed only by exact Wilson trace identities and exact reflected sheet symmetries.

## Equations

- schur-corrected-endpoint-form: `\(U_{\sigma}=R^{G}_{\sigma}+\frac{g_R^4}{16N^2}K^{(4)}_{\sigma}+E^{\mathrm{OPE}}_{\sigma}-S_{HK,\sigma},\quad S_{HK,\sigma}=B_{\sigma}^{*}E_{\sigma}^{-1}B_{\sigma}\)`. Valid when: Valid when the finite H,K decomposition is fixed and the same cutoff data feed both Wilson cumulants and Schur blocks.
- gaussian-crossed-curvature-contraction: `\((R^{G}_{\sigma})_{ij}=\alpha_N g_R^4\sum_{p\in S_i}\sum_{q\in S_j}w_{i,p}w_{j,q}C_{\sigma}(p,q)^2,\quad \alpha_N=(N^2-1)/(8N^2)\)`. Valid when: Applies after vacuum and perimeter normal-ordering cancel disconnected Wilson pieces in the heat-kernel small-loop expansion.
- two-sparse-rayleigh-quotient: `\(\rho_{pq}(\eta,\theta)=U_{pp}+\eta^2U_{qq}-2\eta\operatorname{Re}(e^{i\theta}U_{pq})\)`. Valid when: Valid for the vector e_p minus eta e^{i theta} e_q in the finite endpoint basis.
- interval-stress-falsifier: `\(\overline U_{pp}+\eta^2\overline U_{qq}-2\eta\,\underline{\operatorname{Re}(e^{i\theta}U_{pq})}<0\ \Longrightarrow\ U_{\sigma}\not\succeq0\)`. Valid when: Requires rigorous interval enclosures for the selected principal compression of the same Schur-corrected endpoint matrix.

## Attempted Derivation

- Conceptual pressure attacked: convert the connected boundary-OPE polarization into a route-deciding finite witness, not another symbolic R or OS Hilbert observable algebra restatement.
- Declarative tension: Wilson/OPE coefficients, connected K4 negativity, OPE errors, and H,K Schur subtraction must jointly control one endpoint quadratic form in one cutoff theory, while Clay-level continuum existence, OS/Wightman reconstruction, gauge-invariant observable density, and Hamiltonian mass gap are barred conclusions.
- Carrier audit: scalar R is representation-limited; OS observable-density or excitation-sector cyclicity is too strong and circular for this local gate; shell A012 compression is convenient but quarantined; raw plaquette enumeration is fragmented yet valid.
- Use the heat-kernel Wilson expansion for vacuum-subtracted endpoint flux squares Q_i. Normal ordering cancels disconnected vacuum and perimeter factors, leaving crossed Gaussian curvature contractions plus one connected four-curvature cumulant K4 and an OPE remainder.
- Insert the SU(N) color contraction tr(T^aT^b)tr(T^aT^b) to recover alpha_N=(N^2-1)/(8N^2) for the Gaussian Hadamard-square term.
- Apply finite Schur-Feshbach elimination of the H,K hairpin complement, subtracting S_HK=B^*E^{-1}B in the same endpoint basis.
- Compress U_sigma to endpoints p,q and test x=e_p-eta e^{i theta}e_q. If the rigorous interval upper bound for x^*U_sigma x is negative, then U_sigma is not PSD.
- Hard gate: Delta_raw>0 would promote finite endpoint-box positivity, while a negative two-sparse stress vector demotes this H,K collar/hairpin route. Either outcome changes only the finite Route A proof state.

Blocking gap: The missing mediator is now concrete: same-regulator raw K4 interval enclosures for a selected plaquette-pair compression and fixed phase sector have not been computed. Without them the stress inequality is conditional.

## Falsifiers

- A certified pair p,q, phase theta, and eta with overline rho_pq(eta,theta)<0 is a falsifier for finite endpoint-box positivity of this H,K geometry.
- If K4 intervals cannot be produced in the same heat-kernel regulator and Wilson basis, the raw connected cumulant witness is invalid.
- If exact Wilson quotienting changes any interval endpoint, the proposed compression is non-invariant and must be demoted.
- If OPE error or Schur hairpin uncertainty exceeds the Gaussian color-square margin on every tested pair, the two-sparse route provides no promotion.
- If the recovered U_sigma depends on an OS observable-density assumption, the local finite certificate is circular and must be quarantined.

## Learning

Cycle 301 sharpens the negative tactic: the connected boundary-OPE polarization R is a validator-facing connected cumulant witness whose route-deciding content can be tested on a 2x2 Schur-corrected endpoint compression. The conceptual value signal is sharp and explanatory because a few raw K4 intervals, plus Gaussian color square, OPE error, and H,K energy, can either falsify the worked finite endpoint route or force full Delta_raw proof search. Efficient representation requirements are fixed: encode oriented plaquettes, sheet weights, heat-kernel transporters, color tensors, cumulant intervals, OPE intervals, endpoint indices, and Schur blocks; preserve gauge invariance, reflection support, Gaussian/K4 separation, endpoint compression, same-theory normalization, and exact Wilson quotienting; support cumulant contraction, interval summation, phase-sector certification, Rayleigh stress search, Loewner lower bounds, and Schur subtraction; keep a finite endpoint-box complexity budget; transfer only through Delta_raw or x_stress; demote on negative Rayleigh margin, missing intervals, non-invariant quotienting, or regulator mismatch.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the raw K4 computation queue.`
- Rationale: The branch has exhausted abstraction around R; a concrete two-sparse stress experiment identifies the first raw K4 interval whose sign or size can demote the finite H,K endpoint route.
- Situation seed: Fix one heat-kernel SU(N) endpoint box with the worked H,K collar/hairpin Wilson sheets. Choose the adjacent reflected endpoint pair p,q with largest Gaussian covariance overlap and recover the same-regulator connected cumulant witness U_pq.
- Varied variable: The phase-aligned raw non-Gaussian lower interval k_{pq}^{theta,-}=underline{Re(e^{i theta}K4^{(4)}_{pq})}.
- Held-fixed controls: The lattice cutoff a, smoothing scale sigma, heat-kernel action, coupling normalization, and finite endpoint box., The reflected Wilson sheet weights, H,K Schur blocks, OPE interval rule, and exact Wilson quotient policy., The non-claim boundary: no continuum limit, OS spectral transfer, or Clay mass-gap conclusion is inferred.
- Expected observation: As k_{pq}^{theta,-} varies, the inequality ell_pq(theta)^2>d_p d_q should exhibit a sharp threshold where the two-sparse Rayleigh interval becomes negative; crossing it gives a valid route-demoting stress certificate.
- Transfer certificate needed: A rigorous same-regulator interval recovery Rec_raw for C_sigma, K4_sigma, E_OPE, and S_HK on the chosen 2x2 compression, checked by timeline-definition-assumption-elicitor for definitions, assumptions, validity regimes, and non-claims.

## Next Experiment

Proof search: compute the first same-regulator raw K4 2x2 interval for the largest-overlap endpoint pair p,q, fix theta by the Gaussian-plus-Schur phase, evaluate ell_pq(theta)^2>d_p d_q, and return either x_stress as a connected cumulant witness falsifier or quarantine the two-sparse route.

