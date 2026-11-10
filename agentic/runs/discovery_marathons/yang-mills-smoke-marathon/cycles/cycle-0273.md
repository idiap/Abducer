# cycle-0273

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Post-H,K endpoint source-interval gate

## Candidate Lemma

In the heat-kernel plaquette-sheet regulator, the post-H,K endpoint contribution is validly lower-bounded by a clipped source-derivative interval; negative kappa4 is dangerous only where the null endpoint dominance D_v is certified positive.

## Definitions

- source object: heat-kernel regulated SU(N) plaquette-sheet endpoint boxes B_v with singlet Wilson source evaluations Z_v(sL_v).
- target object: finite post-H,K reflected-Wilson OS gate scalar I_gate for the locked three-hairpin block, not a continuum mass gap claim.
- controlled interface: endpoint source intervals (beta_v,D_v,T_tail) mapped to a lower/upper interval for I_gate after fixed cancellations.
- same-theory condition: the source L_v is obtained from the same regulated Wilson collars and recovery maps used to define H,K, with no boundary counterterm or algebra enlargement.
- conceptual pressure: endpoint collapse must be sign-certified while collar OS positivity and the unchanged gauge-invariant Wilson algebra remain jointly valid.
- declarative tension: finite collar positivity, same Wilson observables, and singular connected endpoint OPE coexist only if raw R is replaced by an incidence-aware source carrier.
- carrier critique: symbolic R is representation-limited and a raw kappa4 spectrum is too strong; the endpoint interval carrier keeps signs, color factors, locality budget, and a falsifier.
- efficient representation: encode B_v,L_v,beta,D,C_N,T_tail; preserve Wilson normalization, reflection, null cancellations, cutoff uniformity; operate by source differences, clipping, color multiplication, tail addition.

## Assumptions

- Model/regime: finite-volume 4D Euclidean SU(N) heat-kernel lattice, plaquette-sheet Wilson loops, collar width delta>0, and endpoint boxes smaller than the collar scale.
- Uniformity: beta_v,D_v,M8_v,T_tail intervals are independent of a and volume along the cutoff-removal subnet used for this finite block.
- Same-theory naturalness: no boundary counterterm, gauge-fixing change, or Wilson renormalization change is inserted when collars collapse to the reflection plane.
- Cancellation regime: Wick-square Gram terms are nonnegative, and straight f^{abc}f^{abd} contacts obey the previously checked null-incidence identity.
- Clay boundary: success changes only the finite reflected-Wilson OS transfer gate; continuum existence, OS/Wightman reconstruction, nontriviality, and mass gap remain untouched.

## Equations

- endpoint source cumulant: `\kappa_{4,v}^{\rm sing}(L_v)=\left.\partial_s^4\log Z_v(sL_v)\right|_{s=0},\quad L_v=\sum_{ij\in\{12,13,23\}}w_{ij}\ell_{ij,v}^{a}T^{a}`. Valid when: Applies when heat-kernel plaquette-sheet endpoint boxes are sourced by the same Wilson collar recovery maps and the singlet projection has fixed color normalization.
- clipped lower gate: `I_{\rm gate}\ge M_G-C_N\sum_v\overline\beta_v[\overline D_v]_+-T_{\rm tail},\quad D_v=2G_{12,v}-4G_{13,v}-4G_{23,v},\quad C_N={g^4\over4}(T_F/N)^2`. Valid when: Valid when Wick-square Gram pieces are retained only as nonnegative terms, the straight f f contact cancels, and the endpoint intervals are cutoff-uniform.
- seven-point source certificate: `\kappa_{4,v}^{\rm sing}\in(6h^4)^{-1}\sum_{r=-3}^{3}a_r\log Z_v(rhL_v)+[-7h^4M_{8,v}/240,7h^4M_{8,v}/240],\quad a=(-1,12,-39,56,-39,12,-1)`. Valid when: Requires log Z_v analytic on the source segment, a uniform eighth-derivative bound M8_v, and identical heat-kernel endpoint boxes for all stencil points.

## Attempted Derivation

- Freeze the finite Wilson block and replace raw R_ij by endpoint source derivatives of log Z_v in the same heat-kernel plaquette-sheet regulator.
- Use connected/cumulant expansion: Wick-square Gram terms are safe, and the straight nonabelian f f contact cancels under the null incidence identity.
- Contract the remaining endpoint kappa4 with the null-channel geometry, giving D_v and the color factor C_N; discard protective D_v<0 terms for a rigorous lower interval.
- Certify beta_v by the seven-point fourth-source stencil and add T_tail, producing a valid scalar interval for the finite OS gate.

Blocking gap: The actual endpoint incidence table G_{ij,v}, source stencil values log Z_v(rhL_v), uniform M8_v bounds, and T_tail are not yet computed.

## Falsifiers

- falsifier: certified source intervals yield sup(I_gate)<0 for the locked endpoint boxes, giving a finite same-theory OS counterexample.
- A boundary counterterm or changed Wilson normalization is needed to make Z_v analytic or positive, breaking the same-theory condition.
- The endpoint tail is not summable uniformly in cutoff or volume, so the finite interval cannot pass to the regulated Wilson collar limit.
- The straight f f cancellation fails for the actual oriented endpoint incidence table, invalidating the clipped lower-bound formula.

## Learning

The sharp carrier is not kappa4 alone but clipped negative kappa4 times certified positive endpoint dominance plus tail. This is route-changing locally: the hard gate is now a finite endpoint interval, not an abstract OS obstruction.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch has exhausted symbolic thresholds; the next valid information is whether actual endpoint incidence can make negative kappa4 overcome the positive finite Schur-Feshbach margin.
- Situation seed: Heat-kernel SU(N) lattice endpoint box for the locked three reflected Wilson hairpins, with seven source evaluations of log Z_v for each endpoint footprint.
- Varied variable: endpoint dominance ratio eta_v=G12_v/(G13_v+G23_v) within the same collar geometry.
- Held-fixed controls: Same heat-kernel regulator, color normalization T_F, and singlet Wilson source recovery map., Same H,K finite block, null vector, reflection plane, and no boundary counterterm., Cutoff-uniform M8_v and a fixed locality budget T_tail.
- Expected observation: There is a sharp crossing: equal endpoint footprints keep I_gate positive, while sufficiently 12-dominant boxes can make the clipped lower interval inconclusive or negative.
- Transfer certificate needed: A cutoff-uniform equality between the endpoint source derivatives and the Wilson boundary-OPE R term, plus validated incidence tables and tail summability before the intuition affects proof obligations.

## Next Experiment

Build the endpoint incidence table for the three hairpin footprints, compute D_v intervals, then run the seven-point heat-kernel source stencil to certify beta_v and I_gate.

# Post-H,K endpoint-box R++ Hessian certificate

## Candidate Lemma

For the first finite H,K plus-channel endpoint box, the connected boundary-OPE polarization term in R_{++} admits a valid lower interval once the Ward-subtracted flowed four-curvature kernels have a uniform endpoint Hessian bound. This is a finite post-H,K obstruction test, not a Clay mass-gap theorem.

## Definitions

- source object: finite-volume cutoff SU(N) Yang-Mills with Wilson action on a four-torus, Luscher gradient flow B_t at t>0, boundary point-splitting rho, and two centered renormalized thin Wilson hairpin variables built from the extracted H,K plus-channel sheet current J_+^eta.
- target object: the finite Schur-Feshbach endpoint-box scalar Q_+ on ker B_KK, with leakage L_+=B_{+R}D^{-1}B_{R+} already determined by the finite H,K reduction.
- controlled interface: the same-theory flowed Wilson covariance R_{++}^{ren}=kappa_2(What_t(J_+^eta),What_t(J_+^eta))_{ren}, decomposed into a positive pair contraction and a Ward-subtracted connected four-curvature polarization Xi_{++}.
- same-theory condition: the H,K extraction, Wilson hairpin observable, flow-time renormalization, boundary counterterms, volume limit, and cutoff-removal maps use the same gauge group, regulator, action, boundary conditions, observable algebra, and recovery maps.

## Assumptions

- Model: pure four-dimensional SU(N) lattice Yang-Mills with Wilson plaquette action; no matter fields and no change of theory across H,K and R_{++}.
- Regime: a<<rho<=eta<<min(d,sqrt(8t)) with endpoint boxes disjoint, t fixed in physical units, and L large enough that heat-kernel tails are below eps_vol.
- Uniformity: all sector kernels have interval enclosures stable as a/rho -> 0 and L/sqrt(8t) -> infinity; this is a finite-cumulant assumption, not full continuum construction.
- Cancellation: disconnected products are removed, one-hairpin perimeter and cusp counterterms are subtracted, and plus-channel reflection makes endpoint monopole and dipole moments vanish.
- Finite data: D is positive on the R-block and L_+ is the already extracted Schur-Feshbach leakage from the finite H,K problem.
- Error budget: eps_cell, eps_vol, eps_a, eps_flow, and eps_ge6 are explicit upper bounds before any promotion; a missing bound is a falsifier for this route.
- Clay boundary: success changes only finite endpoint-box positivity after H,K; OS/Wightman reconstruction, nontrivial continuum limit, large-field and topology control, and Hamiltonian mass gap remain untouched.

## Equations

- flowed endpoint covariance: `R_{++}^{ren}(a,L,t,\eta,\rho)=\kappa_2\big(\widehat W_t(J_+^\eta),\widehat W_t(J_+^\eta)\big)_{ren}`. Valid when: Valid when the flowed Wilson variables are centered, perimeter and cusp counterterms use the same cutoff family, and endpoint boxes are disjoint.
- pair-plus-polarization split: `\frac{R_{++}^{ren}}{\kappa_4}=2(N^2-1)\,\mathcal G_{++}+N(N^2-1)\,\Xi_{++}+\mathcal E_{\ge6}`. Valid when: Applies in the fourth-order flowed Wilson cumulant expansion after endpoint point-splitting and before any continuum extrapolation.
- sector decomposition: `\Xi_{++}=I_{3g}+I_{4g}+I_{ct}+I_{end}`. Valid when: Requires the same-theory boundary OPE sector split with Ward-subtracted kernels and fixed H,K geometry.
- endpoint moment cancellation: `\int_{B_\eta}J_+^\eta=0,\qquad \int_{B_\eta}(x-x_0)_\mu J_+^\eta(x)=0,\qquad \|M_2(J_+^\eta)\|\le c_Q\eta^2\|J_+^\eta\|_1`. Valid when: Valid when plus-channel reflection symmetrization cancels endpoint monopole and dipole moments in each box.
- Hessian lower bound: `\underline\Xi_{++}\ge -c_Q\theta^2 H_4(t,d,\rho)-\varepsilon_{cell}-\varepsilon_a-\varepsilon_{vol},\qquad \theta=\eta/\min\{d,\sqrt{8t}\}`. Valid when: Requires flowed connected kernels to be C2 on endpoint boxes and interval-enclosed uniformly in the cutoff.
- finite endpoint promotion inequality: `2(N^2-1)\mathcal G_{++}+N(N^2-1)\underline\Xi_{++}-\overline{\mathcal E}_{\ge6}>L_+/\kappa_4\ \Longrightarrow\ Q_+>0`. Valid when: Applies after the finite H,K Schur-Feshbach blocks are extracted and D is strictly positive.

## Attempted Derivation

- Conceptual pressure attacked: finite Schur-Feshbach positivity requires a same-theory endpoint mediator, while pair positivity and gradient-flow renormalization do not control the connected four-curvature polarization C4.
- Declarative tension: H,K leakage L_+ is exact in the finite tangent-cone theorem, R_{++} must be a Wilson observable in the same theory, and the connected C4 term can negate the positive pair baseline unless a valid sign/size certificate is supplied.
- Freeze target and claim level: the branch claims only a finite post-H,K endpoint-box interval criterion; Clay continuum existence, OS/Wightman axioms, nontriviality, and positive Hamiltonian mass gap are untouched.
- Use regulator: Wilson lattice action, Luscher flow time t, boundary point-splitting rho, endpoint box eta, and centered renormalized hairpin Wilson variables.
- Expand the same-theory covariance to fourth Wilson-cumulant order: the cross-pair contraction gives the positive color factor 2(N^2-1)G_{++}; connected polarization has color N(N^2-1) and sectors I_{3g}, I_{4g}, I_ct, I_end.
- Use cancellations: disconnected-product removal, one-hairpin perimeter/cusp subtraction, Ward identities for flowed kernels, and plus-channel endpoint monopole/dipole cancellation.
- Taylor expand the Ward-subtracted C4 kernels in endpoint coordinates. Zeroth and first moments vanish, so the remaining endpoint contribution is controlled by the second moment and a Hessian supremum H_4, giving an O(theta^2) lower bound for Xi_{++}.
- Insert the lower bound into Q_+=C_{++}^{fin}-L_++R_{++}^{ren}. Promotion requires the declared lower interval to exceed L_+ after eps_cell, eps_a, eps_vol, eps_flow, and eps_ge6 are subtracted.
- Carrier critique: raw Wilson contours are representation-limited and fragmented; sheet currents plus endpoint currents are the efficient abstraction because Ward subtraction, moment cancellation, and interval cells become primitive operations.
- Route comparison: a global non-Gaussian OS witness is too weakly targeted for this finite obstruction; finite interval-kernel proof search directly attacks the post-H,K R/kappa_4 endpoint term.

Blocking gap: The actual sector kernels I_{3g}, I_{4g}, I_ct, and I_end still need certified interval evaluation or analytic Hessian majorants in the chosen regulator window.

## Falsifiers

- A decisive falsifier is a Ward-subtracted sector interval with lower endpoint so negative that R_{++}^{ren} cannot beat L_+.
- Failure of one-hairpin cusp or perimeter cancellation makes the Hessian estimate invalid rather than merely weak.
- If plus-channel endpoint monopole or dipole moments do not cancel in the actual H,K geometry, the O(theta^2) suppression is false.
- If G_{++}=0 by geometry or orientation, the positive pair baseline cannot support the repair.
- If interval widths grow under a/rho -> 0 or L -> infinity, the same-theory cutoff-uniform condition fails.
- If two sheet-current representatives related by the proposed equivalence give different R_{++} beyond eps_rep, the representation morphism is invalid.
- If the flow-time plateau disappears as t varies in physical units, the endpoint estimate is regulator-fragile.
- If higher Wilson cumulants exceed eps_ge6 in the endpoint window, the fourth-order certificate is not promotion-ready.

## Learning

Cycle 273 makes a local contribution-making move: R_{++}/kappa_4 is estimated through an endpoint-moment Hessian certificate rather than restated as an obstruction. The hard gate is finite endpoint-box positivity after H,K; success promotes that finite gate by proving a lower interval beating L_+, while failure quarantines the R repair without touching Clay existence or mass-gap gates. The conceptual value signal is sharp and explanatory: Ward, cusp, and plus-channel moment cancellations explain why the dangerous connected four-curvature polarization should be O(theta^2) relative to the positive pair baseline. The efficient representation requirements are now explicit: encode H,K sheets and endpoint currents; preserve gauge, color, reflection, orientation, and same-theory invariants; use cumulant expansion, Ward subtraction, endpoint Taylor expansion, heat-kernel majorants, and interval arithmetic as primitives; quotient only by certified zero-pairing current equivalence; keep locality to endpoint boxes and finite cells; transfer through flowed Wilson cumulants; demote on Ward, cusp, plateau, geometry, cutoff-uniformity, or interval-width falsifier. Reporting skill: timeline-definition-assumption-elicitor should surface missing definitions, assumptions, validity regimes, and non-claims.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and interval-kernel calibration, not as evidence for the Clay theorem.`
- Rationale: The branch already has the finite Schur-Feshbach theorem and symbolic H,K leakage; the missing mediator is the sign and size of the same-theory connected boundary-OPE polarization R_{++}. Another abstract OS restatement would loop.
- Situation seed: SU(N) Wilson lattice Yang-Mills on a large four-torus with Luscher flow, two extracted plus-channel H,K thin hairpins in disjoint endpoint boxes, and the Ward-subtracted flowed four-curvature cumulant evaluated by sheet-current interval cells.
- Varied variable: theta=eta/min(d,sqrt(8t)), the dimensionless endpoint-box size controlling monopole/dipole cancellation and Hessian suppression.
- Held-fixed controls: Gauge group SU(N), Wilson plaquette action, boundary conditions, H,K hairpin geometry, and plus-channel reflection convention., Same flow time t in physical units, same point-splitting rho, same perimeter/cusp counterterms, and same centered Wilson recovery map., Fixed Schur-Feshbach leakage L_+ and fixed positive-pair geometry G_{++}., No change to continuum, OS, or spectral-transfer hypotheses during the thought experiment.
- Expected observation: As theta decreases, the interval for Xi_{++} should contract like O(theta^2) after Ward and cusp cancellation, while the pair baseline remains positive; failure of this scaling demotes the endpoint-moment mechanism.
- Transfer certificate needed: A certified same-theory interval proof that the sector Hessian majorants and error budgets are stable under a/rho -> 0 and L/sqrt(8t) -> infinity before the lower bound may enter Q_+.

## Next Experiment

Instantiate the actual plus-channel H,K sheet currents, choose theta grid values, compute interval bounds for I_{3g}, I_{4g}, I_ct, and I_end under Luscher flow with point-splitting rho, and compare the resulting lower R_{++}^{ren} interval against L_+.

# Post-H,K endpoint-box kappa4 shell certificate for reflected Wilson Route A

## Candidate Lemma

Fixed cutoff endpoint-box certificate: for a heat-kernel regulated finite SU(N) Wilson collar/hairpin geometry with H,K already fixed, the Schur-corrected endpoint form is positive on the endpoint box if \Delta_\sigma>0; a rigorous interval giving a negative trial vector is a falsifier for this finite geometry only.

## Definitions

- source object: finite-volume hypercubic lattice SU(N) Yang-Mills with heat-kernel plaquette action, smoothing scale sigma, cutoff a, coupling g_R, and vacuum-normalized traced Wilson sheet observables in the first post-H,K endpoint box.
- target object: the finite-dimensional endpoint quadratic form Q_{end,sigma}=P_B(R_sigma-S_{HK,sigma})P_B acting on the already chosen endpoint Wilson basis B; it is not an OS Hilbert-space spectral statement.
- controlled interface: the sheet-kernel hypergraph whose vertices are smeared curvature sheets and whose edge labels encode transported color tensors, shell classes, multiplicities, OPE errors, and Schur data, with recovery map Rec_sigma sending the hypergraph to the Wilson cumulant matrix R_sigma.
- same-theory condition: all entries C_sigma, kappa_{4,sigma}, E_{OPE,sigma}, H, K, and S_{HK,sigma} are computed with the same heat-kernel regulator, volume, coupling normalization, Wilson basis, reflection plane, and vacuum/perimeter normalization.

## Assumptions

- Model: finite lattice SU(N) heat-kernel gauge theory at fixed a,L,sigma,g_R; reflection support and gauge-invariant traced Wilson observables are preserved, but no continuum or infinite-volume limit is claimed.
- Regime: the endpoint sheets have diameter and separation inside the chosen boundary-OPE collar, with sigma/a fixed so smeared plaquette-sheet contractions are finite and computable.
- Same-theory uniformity: the Schur data H,K and the Wilson cumulants use identical regulator, boundary collar, coupling convention, and normalization; imported continuum estimates are support-only unless rederived at this cutoff.
- Finite Schur assumption: QHQ=E_sigma is strictly positive on the hairpin complement used in the already fixed H,K decomposition, so S_{HK,sigma}=B_sigma^*E_sigma^{-1}B_sigma is well-defined.
- Error budget: the only allowed losses are the negative shell envelope for kappa_4, the endpoint OPE norm e_{OPE,sigma}, and the known Schur hairpin energy s_{HK,sigma}.
- Balance: success changes only the finite Route A endpoint-box positivity gate; OS/Wightman reconstruction, regulator-independent Schwinger functions, large-field/topology summability, and the Hamiltonian mass gap remain untouched.

## Equations

- endpoint R decomposition: `R_\sigma=\alpha_N g_R^4\,(C_\sigma\circ C_\sigma)+\frac{g_R^4}{16N^2}\,\kappa_{4,\sigma}+E_{\mathrm{OPE},\sigma},\qquad \alpha_N=\frac{N^2-1}{8N^2}.`. Valid when: Valid when Wilson loops are vacuum-normalized in the same heat-kernel cutoff and expanded to the boundary-OPE order where crossed two-curvature contractions and the connected four-curvature cumulant are retained.
- connected four-curvature sheet contraction: `(\kappa_{4,\sigma})_{ij}=\sum_{p,q\in\Sigma_i}\sum_{r,s\in\Sigma_j} w_pw_qw_rw_s\,\mathcal T^{abcd}_{pqrs}\,\langle F^a_\sigma(p)F^b_\sigma(q)F^c_\sigma(r)F^d_\sigma(s)\rangle_c.`. Valid when: Valid when each plaquette sheet is parallel-transported to the endpoint basepoint before tracing, so the color tensor and connected cumulant are gauge-invariant finite-cutoff quantities.
- negative shell envelope: `M^-_{4,\sigma}(B):=\sup_{\|x\|=1}\big[-x^*P_B\kappa_{4,\sigma}P_Bx\big]_+\le \rho^-_{\mathrm{shell}}:=\max_i\sum_\ell n_{i\ell}A^-_\ell.`. Valid when: Valid when the sheet-kernel hypergraph quotient preserves Wilson trace symmetries and A^-_ell bounds the negative real part of every transported kappa_4 contraction in shell ell.
- Schur-corrected endpoint margin: `\Delta_\sigma=m_{G,\sigma}-\frac{g_R^4}{16N^2}\rho^-_{\mathrm{shell}}-e_{\mathrm{OPE},\sigma}-s_{HK,\sigma},\quad m_{G,\sigma}:=\lambda_{\min}(\alpha_N g_R^4P_B(C_\sigma\circ C_\sigma)P_B).`. Valid when: Valid when P_B is the fixed endpoint projection, the Schur energy and OPE norm are measured in the same endpoint basis, and all interval bounds are outward-rounded.
- hairpin Schur subtraction: `S_{HK,\sigma}=B_\sigma^*E_\sigma^{-1}B_\sigma,\qquad E_\sigma=QH_\sigma Q,\quad B_\sigma=QK_\sigma P_B.`. Valid when: Valid when the finite Schur-Feshbach tangent-cone hypotheses hold and E_sigma has a strictly positive interval lower bound on the hairpin complement.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Observable Density In The Excitation Sector; source object: finite-volume hypercubic lattice SU(N) Yang-Mills with heat-kernel plaquette action, smoothing scale sigma, cutoff a, coupling g_R, and vacuum-normalized traced Wilson sheet observables in the first post-H,K endpoint box.; target object: the finite-dimensional endpoint quadratic form Q_{end,sigma}=P_B(R_sigma-S_{HK,sigma})P_B acting on the already chosen endpoint Wilson basis B; it is not an OS Hilbert-space spectral statement.; Model: finite lattice SU(N) heat-kernel gauge theory at fixed a,L,sigma,g_R; reflection support and gauge-invariant traced Wilson observables are preserved, but no continuum or infinite-volume limit is claimed..
- Conceptual pressure attacked: the post-H,K route needs a non-circular mediator between concrete connected Wilson cumulants and Schur-corrected endpoint positivity, not another OS-density restatement.
- Freeze claim level: this cycle proves at most a finite cutoff endpoint-box interval theorem; it does not assert OS reconstruction, a continuum Yang-Mills measure, or a Hamiltonian mass gap.
- Use the preserved gauge-invariant observables \widehat W_Sigma=W_Sigma/\langle W_Sigma\rangle-1; the recovery map Rec_sigma contracts the sheet-kernel hypergraph back to R_sigma in the same Wilson observable algebra.
- Expand each endpoint Wilson sheet through transported smeared curvature fluxes in the heat-kernel regulator. The cumulant normalization cancels disconnected vacuum and perimeter factors.
- Compute the color factor of crossed two-curvature contractions with tr(T^aT^b)=delta^{ab}/2, giving the PSD term alpha_N g_R^4(C_sigma o C_sigma), alpha_N=(N^2-1)/(8N^2).
- Isolate the only dangerous same-order non-Gaussian input as the connected transported four-curvature cumulant kappa_{4,sigma}; compress it to the finite endpoint basis P_B.
- Bound the negative spectrum of P_B kappa_4 P_B by a shell row-sum envelope rho^-_shell using shell multiplicities n_{i ell} and per-shell negative interval constants A^-_ell.
- Subtract the corrected second-order Schur hairpin energy S_HK=B^*E^{-1}B, not merely PHP, and add the OPE and quotient error budgets.
- Hard gate: Delta_sigma>0 promotes this finite endpoint-box positivity certificate; a certified vector x with x^*Q_end x<0 is a falsifier and demotes this H,K Wilson geometry.

Blocking gap: The first numerical or symbolic same-regulator values A^-_ell for the connected four-curvature shells, and the exact H,K endpoint geometry, are still not computed here.

## Falsifiers

- Direct same-regulator interval arithmetic finds Delta_sigma<=0 for the first H,K endpoint box.
- A trial endpoint vector aligns with negative kappa_4 shells and gives x^*P_B(R_sigma-S_HK)P_Bx<0; this is a finite Route A falsifier.
- The heat-kernel OPE remainder is comparable to or larger than the Gaussian color-square floor m_G,sigma.
- The Schur hairpin energy s_HK,sigma exceeds the positive Gaussian endpoint margin after kappa_4 is included.
- The sheet-kernel quotient is non-invariant: recovered Wilson cumulants differ from raw plaquette-sheet enumeration beyond the declared error.
- The Gaussian Hadamard square has a null direction in the endpoint box, so any negative kappa_4 component in that direction demotes the branch.
- H,K are unavailable or regulator-mismatched, making the same-theory Schur subtraction invalid.

## Learning

Declarative tension: same-theory Wilson/OPE coefficients, connected kappa_4 negativity, and finite Schur-Feshbach subtraction must jointly control one endpoint quadratic form, while Clay-level OS reconstruction and spectral transfer must remain quarantined. The scalar R carrier is too weak and representation-limited; full OS observable density is too strong and circular for this local gate; raw plaquette enumeration is exact but fragmented. The efficient representation is the sheet-kernel hypergraph: it encodes sheets, weights, transporters, color tensors, shell labels, multiplicities, OPE errors, and Schur data; preserves gauge invariance, reflection support, Gaussian/kappa_4 separation, endpoint compression, and same-theory normalization; supports cumulant contraction, shell row/operator bounds, interval arithmetic, quotient auditing, and Schur subtraction; quotients only by Wilson-invariant trace and sheet symmetries; keeps a finite endpoint-box locality budget; transfers only through Rec_sigma to Delta_sigma; and has falsifiers by margin failure, nonuniform envelopes, or non-invariant quotienting. Conceptual value signal: the cycle changes the proof state from an aspirational R parameter to a valid finite interval inequality with named computable inputs; success is route-changing for the worked Wilson H,K endpoint box, and failure is explanatory because it isolates whether kappa_4, OPE error, or hairpin coupling kills the route. The larger YM gates--volume/cutoff uniformity, large-field and topological summability, regulator-independent Schwinger functions, OS positivity, observable density, and physical-unit spectral transfer--remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the first same-regulator endpoint interval.`
- Rationale: The branch has already identified R as a connected Wilson cumulant; the decisive missing information is whether the kappa_4 shell envelope can overwhelm the PSD Gaussian color square after Schur subtraction.
- Situation seed: Finite SU(2) heat-kernel lattice gauge theory on a reflected box with the first collar/hairpin endpoint Wilson sheets fixed, normalized traced Wilson loops, and H,K Schur data held in the same cutoff model.
- Varied variable: The smoothing ratio eta=sigma/a, varied over a small finite grid while the endpoint sheet geometry and coupling convention are fixed.
- Held-fixed controls: Same heat-kernel plaquette action, volume, coupling g_R, reflection plane, and vacuum/perimeter normalization., Same endpoint Wilson basis B and the same H,K collar/hairpin Schur decomposition., Same sheet-kernel hypergraph quotient rules and outward-rounded interval arithmetic., No continuum, OS, or spectral-transfer conclusion is allowed from the observation.
- Expected observation: If increasing eta lowers rho^-_shell and e_OPE faster than it lowers m_G, Delta_sigma should enter a positive interval; if rho^-_shell scales with or above m_G, the endpoint-box route is falsified for this geometry.
- Transfer certificate needed: A raw plaquette-sheet or heat-kernel character-expansion computation of A^-_ell, e_OPE, m_G, and s_HK in the same regulator, plus a proof that Rec_sigma reproduces the Wilson cumulant matrix within the declared interval budget.

## Next Experiment

Compute the first shell table for the fixed H,K endpoint box: enumerate transported plaquette-sheet quadruples, group by Wilson-invariant shell, evaluate or bound A^-_ell in the heat-kernel character expansion, then assemble Delta_sigma with outward-rounded interval arithmetic.

