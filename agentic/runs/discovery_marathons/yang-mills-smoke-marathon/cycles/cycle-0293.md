# cycle-0293

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint source-equivalence compression for the post-H,K Wilson gate

## Candidate Lemma

Endpoint source-equivalence compression gives a valid finite Route A certificate for the post-H,K reflected-Wilson block: aggregate endpoint boxes only when their regulated seven-point source data agree, form the scalar interval for the null-channel endpoint term, promote the finite block if its lower endpoint is nonnegative, and produce a same-theory finite falsifier if its upper endpoint is negative. This changes only the finite post-H,K OS transfer gate; continuum YM construction, nontriviality, OS/Wightman reconstruction for all observables, and the mass gap remain untouched.

## Definitions

- source object: C_ep is the heat-kernel plaquette-sheet endpoint carrier for the fixed three-hairpin reflected Wilson block, consisting of endpoint boxes v, seven source values z_v(rh)=log Z_v(rh L_v), kappa_4 intervals, fractional incidences b_ij,v, color factor C_N, Gaussian margin M_G, and tail interval T_tail.
- target object: I_gate is the scalar Schur-Feshbach endpoint gate for the already reduced finite Wilson OS quotient block in the null channel, with sign deciding only this finite block.
- controlled interface: source-equivalence compression maps C_ep to I_gate by grouping endpoint boxes with equal regulated source data, summing their signed incidences, multiplying by the same-theory kappa_4 interval and color factor, and adding the certified tail interval.
- same-theory condition: every source derivative is taken inside the original heat-kernel Wilson plaquette-sheet regulator with the locked Wilson normalization, reflection action, null-channel cancellations, and no boundary counterterm or enlarged boundary observable algebra.

## Assumptions

- Model: four-dimensional Euclidean lattice SU(N) Yang-Mills with heat-kernel plaquette action and gauge-invariant Wilson plaquette-sheet approximants to the three reflected hairpins.
- Regime: fixed finite H,K hairpin block after the Schur-Feshbach reduction, small collar thickness, and endpoint boxes scaled with the cutoff before the continuum limit is claimed.
- Cutoff: all source derivative, eighth-derivative, and tail bounds are uniform in the cutoff over the endpoint classes being compressed.
- Same-theory: the Wilson observables, reflection map, source insertions, and recovery maps are identical before and after endpoint compression; no boundary theory is introduced.
- Local: non-endpoint overlap, corner leakage, and topology-changing remainder contributions are charged to T_tail rather than hidden in the endpoint kappa_4 term.
- Validity: this is a restricted finite-block theorem and not a construction of continuum Schwinger functions or a Hamiltonian mass gap.

## Equations

- source-class-equivalence: `v\sim w \iff z_v(rh)=z_w(rh)\ \text{for}\ r=-3,-2,-1,0,1,2,3\ \text{and the same }M_8\text{ bound applies}`. Valid when: Valid when Model and Same-theory assumptions identify endpoint boxes by equal regulated heat-kernel source values.
- fourth-cumulant-stencil-interval: `\mathcal K_\alpha=D_h^{(4)}z_\alpha+[-7h^4M_{8,\alpha}/240,\,7h^4M_{8,\alpha}/240]`. Valid when: Valid when the endpoint source function is C^8 in the source parameter uniformly over the cutoff range.
- compressed-null-incidence: `\mathcal D_\alpha=\sum_{v\in\alpha}\beta_v\,(2b_{12,v}-4b_{13,v}-4b_{23,v})`. Valid when: Valid after the H,K Schur-Feshbach null vector and the reflected Wilson endpoint incidence convention are fixed.
- endpoint-gate-interval: `I_{\rm gate}=M_G+C_N\sum_\alpha \mathcal K_\alpha\mathcal D_\alpha+T_{\rm tail},\quad [I_-,I_+]=M_G+C_N\sum_\alpha[\inf(\mathcal K_\alpha\mathcal D_\alpha),\sup(\mathcal K_\alpha\mathcal D_\alpha)]+[T_-,T_+]`. Valid when: Valid when endpoint classes are source-equivalent and all nonlocal leftover terms are included in T_tail.
- finite-promotion-and-falsifier-test: `I_-\ge0\Rightarrow\text{finite block promoted},\qquad I_+<0\Rightarrow\text{finite same-theory OS falsifier}`. Valid when: Valid only for the fixed post-H,K finite Wilson gate under the stated cutoff-uniform endpoint interval assumptions.

## Attempted Derivation

- Start from the already reduced finite Wilson OS quotient gate and keep only the post-H,K endpoint residue after Wick-square Gram positivity and straight f f incidence cancellation.
- Represent every endpoint box by the same-theory heat-kernel source function z_v(s)=log Z_v(sL_v), not by a symbolic R entry or by an abstract kappa_4 spectrum.
- Declare source-equivalent boxes only when the seven stencil values and the uniform M8 remainder bound agree; this prevents illegal coarsening across different Wilson endpoint theories.
- For each source class alpha, aggregate the signed null incidence D_alpha before multiplying by the class kappa_4 interval; this is the new compression step that preserves the cancellation information.
- Add the certified tail interval for corner, topology, and nonlocal leakage terms, then test the scalar interval [I_-,I_+] against zero.

Blocking gap: No actual endpoint source table, M8 bound, or cutoff-uniform T_tail interval is presently attached to the branch. The algebraic carrier is valid, but the numerical or analytic endpoint data needed for promotion or falsifier status are missing.

## Falsifiers

- falsifier: a certified 12-dominant source class with b13+b23<b12/2 and sufficiently negative kappa_4 interval makes I_+<0 for the finite Wilson OS gate.
- falsifier: a cutoff-dependent endpoint tail T_tail whose negative part grows faster than the Gaussian margin invalidates the finite promotion interval.
- falsifier: endpoint source equivalence fails after compression, so the same kappa_4 interval was illegally assigned to inequivalent Wilson endpoint boxes.
- falsifier: endpoint collapse requires a boundary counterterm or modified Wilson normalization, breaking the same-theory condition even if the resulting matrix is positive.
- A valid stress case is all endpoint boxes satisfying the half-overlap shield; then negative compact-group kappa_4 is protective or null and only T_tail can demote the block.

## Learning

The contribution of cycle 293 is a valid source-equivalence compression theorem for the endpoint carrier: endpoint boxes may be aggregated only by equal regulated source data, then signed incidences are summed before kappa_4 multiplication. This is sharper than raw R, raw kappa_4 spectra, or a global Schur-preimage test because it preserves the exact null-channel cancellations. The conceptual pressure is endpoint collapse in the same Wilson theory; the declarative tension is finite collar OS positivity plus fixed gauge-invariant Wilson observables plus singular endpoint OPE without adding a boundary theory. The hard gate is the finite post-H,K reflected-Wilson OS transfer gate. Success promotes only this finite block; failure gives a finite same-theory falsifier; lack of endpoint data quarantines the branch.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The branch has exhausted abstract Wilson/OS carrier restatements; the proof state now turns on whether a concrete endpoint incidence/source table can cross the finite scalar gate.
- Situation seed: Heat-kernel SU(N) plaquette-sheet regulator for the fixed three-reflected-hairpin endpoint boxes after the H,K Schur-Feshbach reduction, with same Wilson loops and no boundary counterterm.
- Varied variable: fractional endpoint dominance eta=(b13+b23)/b12 in the potentially dangerous 12-source class, with eta varied through the half-overlap threshold 1/2.
- Held-fixed controls: same heat-kernel plaquette action and Wilson plaquette-sheet regulator, same Feshbach null vector and weights 2,-4,-4, same color factor C_N, Gaussian margin M_G, and Wilson normalization, same source stencil spacing h and cutoff-uniform M8/tail bookkeeping
- Expected observation: For eta>=1/2 the negative endpoint kappa_4 contribution cannot lower I_gate; for eta<1/2 the interval can cross zero only if the certified negative source cumulant and tail exceed M_G.
- Transfer certificate needed: A cutoff-uniform seven-point source derivative interval and T_tail estimate in the same Wilson theory, plus verification that endpoint compression used only equal regulated source data.

## Next Experiment

Either compute the heat-kernel endpoint source table for the source-equivalence classes in the fixed three-hairpin block, or quarantine the branch and hand off to a data/literature import route for uniform endpoint cumulant and tail estimates.

# Finite endpoint R++ Ward-Hessian certificate for post-H,K Route A

## Candidate Lemma

Conditional finite theorem: in a fixed H,K endpoint box, the connected boundary-OPE polarization term R_{++}^{ren} has a certified lower interval once the Ward-subtracted four-curvature kernel has near/far Hessian constants and the plus endpoint current has zero monopole and dipole moments. This changes only finite endpoint-box positivity after H,K.

## Definitions

- source object: finite-volume SU(N) Wilson lattice measure at spacing a with gradient-flowed centered H,K endpoint hairpin observables :W_t(J_+): and :W_t(\theta J_+):.
- target object: the finite Route A plus-channel endpoint-box Schur-Feshbach scalar Q_+ after H,K, with leakage L_+=B_{+R}D^{-1}B_{R+} fixed.
- controlled interface: the renormalized reflected Wilson covariance R_{++}^{ren}=\kappa_2(:W_t(J_+):,:W_t(\theta J_+):) enters Q_+ only through the endpoint-box matrix element.
- same-theory condition: the Wilson measure, gradient flow, centering, cusp counterterms, and reflection map are the same cutoff theory on both sides of the transfer.
- regulator: Wilson plaquette action on a finite four-torus, Yang-Mills gradient flow at time t, boundary point-splitting epsilon, and fixed endpoint cell diameter eta.
- carrier: endpoint sheet current J_+ with color, orientation, reflection, cell-moment, and zero-pairing data retained.
- polarization term: Xi_{++}^{WS} is the Ward-subtracted connected four-curvature contribution after disconnected-product and one-hairpin perimeter/cusp cancellations.

## Assumptions

- Model: four-dimensional finite-volume SU(N) lattice Yang-Mills with Wilson action, fixed N>=2, and gauge-invariant flowed Wilson hairpins.
- Regime: a^2/t <= delta_a, epsilon^2/t <= delta_e, eta <= c sqrt(t), and the H,K endpoint box is fixed before any continuum limit is discussed.
- Cutoff: all constants G_{++}^{I,-}, H_near^{I,+}, H_far^{I,+}, and E_6^{I,+} are certified with outward rounding at the same cutoff and volume.
- Same-theory: no observable, counterterm, or recovery map is imported from a different regulator or RG basin.
- Validity: Ward and cusp subtractions remove the one-hairpin perimeter/cusp pieces, and the plus endpoint current satisfies M_0(J_+)=M_1(J_+)=0 after certified zero-pairing quotienting.
- Local: the claim is finite and endpoint-box-local; it does not assert OS reconstruction, nontrivial continuum existence, observable density, or a Hamiltonian mass gap.

## Equations

- flowed reflected cumulant defining R++: `\displaystyle R_{++}^{\mathrm{ren}}(a,V,t,\epsilon)=\kappa^{a,V}_2\big(:W_t(J_+):_{\epsilon},:W_t(\theta J_+):_{\epsilon}\big)`. Valid when: Valid when the centered Wilson hairpins use the same cutoff measure, gradient flow time, reflection plane, and cusp-subtracted endpoint current.
- pair baseline plus connected polarization: `\displaystyle R_{++}^{\mathrm{ren}}=g_t^4 (N^2-1)\{2G_{++}+N\Xi_{++}^{\mathrm{WS}}\}+E_6`. Valid when: Applies in the thin endpoint-sheet expansion after disconnected-product removal and perimeter/cusp subtraction, with the sixth-order remainder bounded on the fixed finite endpoint box.
- Ward-Hessian polarization bound: `\displaystyle |\Xi_{++}^{\mathrm{WS}}|\le \big(H_{\mathrm{near}}^+(\rho,t)+H_{\mathrm{far}}^+(\rho,t)\big)M_{2,+}^2`. Valid when: Requires Ward-subtracted sector kernels, zero monopole and dipole moments for the plus endpoint current, and cell diameter eta below the selected near-far radius rho.
- certified lower interval: `\displaystyle R_{++}^{I,-}=g_t^4(N^2-1)\{2G_{++}^{I,-}-N(H_{\mathrm{near}}^{I,+}+H_{\mathrm{far}}^{I,+})M_{2,+}^2\}-E_6^{I,+}`. Valid when: Valid for an outward-rounded interval enclosure of the pair kernel, Ward-Hessian constants, second cell moment, and sixth-order Wilson remainder in the same cutoff theory.
- finite Route A promotion test: `\displaystyle R_{++}^{I,-}>L_+\quad \Longrightarrow\quad Q_+^{I,-}=R_{++}^{I,-}-L_+>0`. Valid when: Applies only to the finite H,K endpoint-box Schur-Feshbach scalar with D positive on the fixed remainder subspace and no continuum spectral conclusion.

## Attempted Derivation

- Attack conceptual pressure: finite Schur-Feshbach positivity after H,K needs a same-theory Wilson mediator; positive pair covariance and gradient flow are valid but C4 can erase the endpoint term.
- Fix the source: finite SU(N) Wilson lattice measure, flowed hairpin sheets J_+ and theta J_+, centering, boundary point-splitting, and cusp/perimeter subtraction.
- Expand the two centered Wilson hairpins through order g_t^4. The disconnected product and one-hairpin perimeter/cusp terms cancel; the cross-pair contraction gives the positive color-geometric term 2(N^2-1)G_{++}.
- Decompose the remaining connected four-curvature polarization into I_{3g}, I_{4g}, I_ct, and I_end with total color factor N(N^2-1).
- Use Ward subtraction and the plus-channel endpoint moment conditions M_0=M_1=0. Endpoint Taylor expansion removes constant and linear kernel parts, leaving a Hessian bound times M_{2,+}^2.
- Split cells at radius rho. Bound far cells by interval Hessian suprema and near cells by flowed heat-kernel derivative majorants plus counterterm and endpoint intervals.
- Insert the resulting lower interval into Q_+=R_{++}-L_+. Success promotes only finite endpoint-box positivity; failure quarantines the R repair and leaves Clay existence and mass-gap gates untouched.

Blocking gap: The proof still lacks certified numerical or analytic intervals for G_{++}^{I,-}, H_near^{I,+}, H_far^{I,+}, E_6^{I,+}, and E_rec^{I,+} for a concrete SU(2) or SU(3) H,K endpoint partition.

## Falsifiers

- falsifier: the Ward-subtracted connected four-curvature interval satisfies N(H_near^{I,+}+H_far^{I,+})M_{2,+}^2 >= 2G_{++}^{I,-} beyond the leakage margin.
- falsifier: cusp or perimeter subtraction leaves a residual growing as epsilon->0 or a^2/t->0.
- falsifier: the recovery map from Wilson contours to endpoint sheet currents changes the same-theory covariance by more than E_rec.
- falsifier: zero-pairing quotienting identifies two endpoint currents with different reflected Wilson covariances.
- falsifier: the lower interval is not stable under one endpoint-cell refinement or one cutoff reduction at fixed t-window.
- falsifier: the positive pair baseline G_{++}^{I,-} vanishes because the chosen H,K endpoint geometry has zero reflected pairing.
- Stress case: choose eta close to sqrt(t) and rho too small; near-cell Hessian domination may become too crude and demote the interval route.

## Learning

Conceptual pressure attacked: the missing same-theory mediator between finite Schur-Feshbach positivity and Wilson cumulant positivity. Declarative tension: positive pair covariance, gradient-flow renormalization, and endpoint positivity must jointly be valid, but the connected four-curvature polarization can erase the pair term unless Ward-Hessian constants and recovery errors are certified. Carrier critique: raw Wilson contours are fragmented; global OS spectral transfer and non-Gaussian witness routes are too coarse for this local obstruction. Endpoint sheet currents are sharper but only if they preserve gauge/color/reflection/orientation/cutoff/same-theory invariants, encode H,K sheets, endpoint moments, sector kernels, and counterterms, use cumulant expansion, Ward/cusp subtraction, heat-kernel Hessian majorants, interval quadrature, outward rounding, and zero-pairing quotienting as primitives, keep locality to finite endpoint cells, and transfer through centered flowed Wilson cumulants. Hard gate: finite endpoint-box positivity after H,K. Success promotes one finite Route A gate; failure quarantines the R repair. Conceptual value signal: R_{++}/kappa_4 is now a route-deciding color-geometric near/far interval with a valid falsifier, not a symbolic threshold. Clay existence, OS/Wightman axioms, nontrivial continuum limit, observable density, large-field/topology control, and Hamiltonian mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and proof-search calibration.`
- Rationale: The branch has reached a concrete finite Route A endpoint obstruction; another abstract OS or non-Gaussian witness restatement would not decide whether R_{++} can beat Schur-Feshbach leakage.
- Situation seed: SU(2) Wilson lattice Yang-Mills on a finite four-torus with fixed H,K plus-channel endpoint hairpin sheets, gradient flow time t, boundary point-splitting epsilon, and a reflected endpoint box partitioned into symmetric cells.
- Varied variable: The single varied parameter is theta=eta/sqrt(8t), the endpoint cell diameter measured in flow units.
- Held-fixed controls: Same Wilson action, finite volume, bare coupling window, reflection plane, gradient-flow definition, and cusp/perimeter counterterms., Same H,K endpoint geometry, plus-channel current weights, zero-pairing equivalence policy, and Schur-Feshbach leakage L_+., Same interval arithmetic rules, near/far split rho/sqrt(t), and outward-rounded heat-kernel majorants.
- Expected observation: As theta decreases, the ratio zeta(theta)=N(H_near^{I,+}+H_far^{I,+})M_{2,+}^2/(2G_{++}^{I,-}) should either fall below the leakage margin, promoting the finite endpoint-box gate, or stay above one, falsifying this R repair.
- Transfer certificate needed: Before intuition affects proof obligations, certify same-theory recovery from Wilson loops to flowed endpoint sheet currents, cutoff-stable Ward/cusp subtraction, and interval lower bounds for G_{++} and upper bounds for Xi_{++}^{WS} on the fixed H,K endpoint partition.

## Next Experiment

Proof search: instantiate SU(2), one symmetric H,K endpoint partition, theta in {1/4,1/8}, rho=sqrt(8t), compute outward-rounded G_{++}^{I,-}, H_near^{I,+}, H_far^{I,+}, E_6^{I,+}, and E_rec^{I,+}; decide R_{++}^{I,-}>L_+ or quarantine the R repair.

# Raw plaquette interval certificate for post-H,K endpoint positivity

## Candidate Lemma

Finite raw-plaquette stress-certificate lemma. In a fixed heat-kernel lattice Yang-Mills cutoff theory, the post-H,K endpoint form is positive on the worked endpoint space if the interval lower bound Delta_raw is positive; it is falsified if one admissible stress vector has a strictly negative interval upper bound.

## Definitions

- source object: finite-volume heat-kernel regulated SU(N) lattice Yang-Mills measure at spacing a, coupling g_R, endpoint collar scale sigma, and the actual Wilson plaquette variables used in the H,K construction.
- target object: the finite Schur-Feshbach corrected endpoint quadratic form on the vacuum-subtracted endpoint Wilson coefficient space E_{H,K}, not a continuum Hamiltonian spectral statement.
- controlled interface: the raw plaquette cumulant matrix R_raw=(cum_2(Q_i,Q_j))_{i,j} with exact Wilson recovery maps Q_i from endpoint sheets to oriented plaquette sums.
- same-theory condition: R_raw, the OPE interval, and S_HK=B^*E^{-1}B are computed with the same cutoff, same gauge group, same coupling, same Wilson basis, and same vacuum/perimeter normalization.
- Bridge carrier: oriented plaquette tuple (p,epsilon,w,U_path,a_color) encoding sheet weights, heat-kernel transporters, color insertion, and reflection support.
- Endpoint observable: Q_i=:Phi_i^2: where Phi_i is the transported boundary curvature flux attached to endpoint sheet i.

## Assumptions

- Model: finite-volume SU(N) lattice Yang-Mills with heat-kernel plaquette action and reflection plane chosen before endpoint truncation.
- Regime: fixed finite endpoint box and fixed H,K hairpin/collar geometry; no infinite-volume or a->0 uniformity is claimed.
- Cutoff: sigma/a is finite and all plaquette sums defining Q_i are explicitly enumerated or enclosed by rigorous intervals.
- Same-theory: normal ordering, vacuum subtraction, perimeter cancellation, R_raw, OPE errors, and Schur data use the identical lattice measure.
- Local: endpoint sheets lie in the reflected Wilson collar where the finite Schur-Feshbach theorem from prior cycles applies.
- Validity: the connected four-curvature cumulant is supplied as an interval matrix K4_raw^- <= K4_raw <= K4_raw^+ in the raw plaquette basis.
- Constraint: quotienting is allowed only by exact Wilson trace identities, orientation reversal identities, and sheet symmetries that preserve interval endpoints.

## Equations

- transported-plaquette-flux: `\Phi_i=\sum_{p\in S_i} w_{i,p}\,\epsilon_{i,p}\,X_p^{a}\,T^a,\qquad Q_i=:\!\operatorname{tr}(\Phi_i^2)\!:`. Valid when: Valid when S_i is the enumerated endpoint sheet and X_p^a is the heat-kernel transported plaquette curvature at fixed cutoff a.
- raw-connected-polarization: `R^{\mathrm{raw}}_{ij}=\operatorname{cum}_2(Q_i,Q_j)`. Valid when: Valid when Q_i and Q_j are vacuum-subtracted Wilson endpoint observables in the same heat-kernel cutoff theory.
- Gaussian-color-square: `R^{G}_{ij}=\alpha_N g_R^4\sum_{p,q\in S_i}\sum_{r,s\in S_j} w_{i,p}w_{i,q}w_{j,r}w_{j,s}\,C_{p r}\,C_{q s},\qquad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after normal ordering cancels disconnected contractions and the remaining crossed two-curvature contractions use the same transported covariance C.
- kappa4-interval-insertion: `R^{\mathrm{raw}}\in R^{G}+\frac{g_R^4}{16N^2}[K4^{-}_{\mathrm{raw}},K4^{+}_{\mathrm{raw}}]+[E^{-}_{\mathrm{OPE}},E^{+}_{\mathrm{OPE}}]`. Valid when: Requires a rigorous interval enclosure for every connected four-curvature plaquette cumulant and the same-regulator endpoint OPE remainder.
- schur-corrected-margin: `\Delta_{\mathrm{raw}}=\lambda_{\min}\!\left(R^{G}+\frac{g_R^4}{16N^2}K4^{-}_{\mathrm{raw}}+E^{-}_{\mathrm{OPE}}-S_{H,K}\right)`. Valid when: Valid when K4_raw^- and E_OPE^- are Loewner lower interval matrices and S_HK is the finite Schur-Feshbach hairpin energy.
- stress-vector-falsifier: `\exists v\ne0:\quad \frac{v^*\left(R^{G}+\frac{g_R^4}{16N^2}K4^{+}_{\mathrm{raw}}+E^{+}_{\mathrm{OPE}}-S_{H,K}\right)v}{v^*v}<0`. Valid when: This falsifier is valid when the upper interval matrix encloses the true endpoint form for the identical cutoff theory.

## Attempted Derivation

- Conceptual pressure attacked: replace symbolic R and quarantined A012 shells by an actual same-regulator plaquette interval controlling the Schur-corrected endpoint form.
- Declarative tension: Wilson/OPE coefficients, connected kappa4 negativity, OPE remainders, and H,K Schur energy must jointly hold in one cutoff theory, while OS/Wightman reconstruction and spectral transfer must remain non-claims.
- Carrier audit: scalar R is representation-limited, OS observable density is too strong and circular for this local gate, shell compression is convenient but quarantined, and raw plaquette enumeration is fragmented yet valid.
- Compared route: raw plaquette interval proof search beats the sheet-shell abstraction for validity because it preserves every transporter and color factor; the cost is finite combinatorial complexity.
- Define transported curvature flux Phi_i from oriented plaquettes in endpoint sheet S_i and normal-ordered Q_i=:tr(Phi_i^2): using the identical heat-kernel measure.
- Expand cum_2(Q_i,Q_j). Vacuum/perimeter and disconnected Wick pieces cancel by the same normal ordering used in the Wilson endpoint basis.
- The crossed two-curvature contractions give R_G with color factor alpha_N=(N^2-1)/(8N^2) and a positive semidefinite covariance square on the finite endpoint space.
- All remaining same-order connected four-curvature terms are placed in K4_raw, an interval matrix over raw plaquette tuples; endpoint OPE truncation is placed in E_OPE.
- Insert the prior finite Schur-Feshbach correction S_HK=B^*E^{-1}B and compute the Loewner lower matrix defining Delta_raw.
- Hard gate: Delta_raw>0 promotes only finite endpoint-box positivity; a negative stress vector for the upper matrix demotes this H,K route.
- Efficient representation requirements: encode oriented plaquettes, sheet weights, heat-kernel transporters, color tensors, cumulant intervals, OPE intervals, and Schur blocks; preserve gauge invariance, reflection support, Gaussian/kappa4 separation, endpoint compression, and same-theory normalization; support cumulant contraction, interval summation, quotient audit, row/operator bounds, and Schur subtraction; quotient only by exact Wilson identities; keep finite endpoint complexity; transfer only through Delta_raw; expose falsifiers by margin failure or non-invariant intervals.
- Reporting skill: timeline-definition-assumption-elicitor should audit every definition, assumption marker, validity regime, and non-claim boundary before promotion.

Blocking gap: No certified numerical or symbolic raw K4_raw interval has yet been computed for the concrete H,K endpoint plaquette list, and the OPE interval for the same cutoff is still an input rather than a derived bound.

## Falsifiers

- A negative stress vector v with a valid upper interval bound for v^*(R_raw-S_HK)v demotes the finite endpoint route.
- The K4_raw negative row/operator bound exceeds the PSD Gaussian margin plus OPE slack, making Delta_raw nonpositive.
- A purported quotient changes transporter ordering, color trace order, orientation sign, or reflection support; the interval certificate is then invalid.
- Disconnected vacuum/perimeter terms fail to cancel because R_raw and S_HK used different normalizations or different cutoff measures.
- Large endpoint complexity prevents exact enumeration and no invariant interval compression is available; the raw proof search is quarantined.
- A Clay-level conclusion is inferred from finite Delta_raw without regulator-independent Schwinger functions and OS spectral transfer; this is an overclaim falsifier.

## Learning

Cycle 293 sharpens the contribution from a conditional finite theorem into a proof-search-ready raw plaquette stress certificate. The conceptual value signal is route-changing at finite scope: R is an actual connected Wilson cumulant with color, geometry, kappa4, OPE, and Schur data in one valid inequality. The hard gate is Delta_raw>0 or a negative stress vector; success promotes only endpoint-box positivity, while failure cleanly falsifies this H,K collar/hairpin route. The larger Yang-Mills Clay commitments are preserved as non-claims.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and proof-search guide for the raw interval computation.`
- Rationale: The branch needs a concrete complexity-controlled test because another abstract R/kappa4 restatement would not decide whether raw plaquette enumeration can beat the quarantined A012 shell abstraction.
- Situation seed: Finite SU(2) heat-kernel lattice endpoint box with the worked H,K collar/hairpin Wilson sheets; enumerate all oriented plaquette tuples contributing to Q_i and Q_j inside distance two of the endpoint boundary.
- Varied variable: The endpoint resolution ratio rho=sigma/a, varied over rho=2,3,4 while holding the Wilson geometry and renormalized coupling label fixed.
- Held-fixed controls: Same heat-kernel lattice measure, gauge group, reflection plane, and vacuum/perimeter normalization for R_raw, K4_raw, OPE intervals, and S_HK., Same H,K endpoint Wilson basis and Schur-Feshbach block decomposition; no shell A012 replacement is allowed., Only exact Wilson trace, orientation, and lattice reflection symmetries may quotient plaquette tuples.
- Expected observation: If the route is viable, the Gaussian color-square margin should scale coherently with rho and dominate the outward-rounded K4_raw/OPE/Schur subtraction; if a small-rho negative stress vector persists under exact refinement, it is a credible finite falsifier.
- Transfer certificate needed: A certified raw interval enclosure for K4_raw and E_OPE at each rho, plus an exact quotient audit showing that the computed Delta_raw is the same-theory endpoint form before any proof-state promotion.

## Next Experiment

Build the rho=2 SU(2) heat-kernel endpoint plaquette list, compute R_G exactly from transported covariance, enclose K4_raw by raw cumulant intervals, insert the known S_HK block, and search for either Delta_raw>0 or a valid negative stress vector.

