# cycle-0264

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Post-HK endpoint-box interval certificate for reflected Wilson hairpins

## Candidate Lemma

Endpoint clipped-dominance lemma: for the fixed three-hairpin post-H,K block, the connected boundary-OPE endpoint contribution is safely exported to the finite OS gate by a scalar interval. Negative compact-group kappa_4 is dangerous only on endpoint boxes with positive dominance D_v; protective boxes and Wick-square terms cannot be used as falsifiers.

## Definitions

- source object: a heat-kernel plaquette-sheet regulated SU(N) endpoint box v with singlet-projected connected four-flux source derivative K_v^{sing} and endpoint incidence Gram entries G_{ij,v}.
- target object: the scalar Schur-Feshbach null-channel coefficient C_partial for the intended same-theory finite Wilson OS quotient matrix after H,K are fixed.
- controlled interface: source derivatives and incidence contractions are mapped to an interval [C_lower,C_upper] using color factor c_N, clipped D_v dominance, and a tail interval T_tail.
- same-theory condition: the Wilson normalization, gauge-invariant test algebra, heat-kernel regulator, endpoint-box partition functions, and collar-limit observable labels are identical on the source and target sides, with no added boundary counterterm.
- carrier: endpoint data tuple E_v=([beta_v^-,beta_v^+],[d_v^-,d_v^+],c_N,[tau_v^-,tau_v^+]) plus the finite null incidence weights (2,-4,-4).
- declarative tension: collar reflection positivity, unchanged Wilson theory, and singular endpoint collapse must jointly hold, but raw R is representation-limited because it hides incidence signs and endpoint locality.
- efficient representation: encode endpoint boxes, beta intervals, D_v intervals, color factors, and tails; preserve Wilson normalization and null-channel cancellations; primitives are source differentiation, interval multiplication, incidence contraction, color multiplication, clipping, and tail addition; equivalent carriers require equal regulated source derivatives; locality cost is finite by charging unresolved overlap to T_tail; transfer interface is the scalar interval C_partial.

## Assumptions

- Model/regime: four-dimensional Euclidean SU(N) lattice Yang-Mills with heat-kernel plaquette action, fixed finite hairpin geometry, collar width positive before the endpoint limit, and endpoint boxes smaller than the collar separation scale.
- Uniformity: the fourth source derivatives defining K_v^{sing} and the tail estimates are bounded uniformly in the cutoff along the regulated continuum subsequence used by the Wilson block.
- Same-theory assumption: every endpoint source derivative is taken inside the original Wilson observable algebra; no boundary field, defect algebra, or external counterterm is introduced during endpoint collapse.
- Cancellation assumption: connected log derivatives remove Wick-square disconnected contractions, and the straight-segment nonabelian f f contact cancels under the established null incidence identity; only endpoint/corner tails remain outside the box terms.
- Sign assumption for this certificate: the compact-group endpoint fourth cumulant is represented as K_v^{sing}=-beta_v with beta_v in a nonnegative certified interval; boxes whose sign is not certified are absorbed into T_tail.
- Local-to-global boundary: success changes only the finite reflected-Wilson OS transfer gate; continuum Yang-Mills construction, OS/Wightman axioms for all observables, and the positive Hamiltonian mass gap remain untouched.

## Equations

- endpoint connected four-flux source derivative: `K_v^{\mathrm{sing}}(Y)=\left.\partial_s^4\log Z_v(sY)\right|_{s=0}=\langle X_v(Y)^4\rangle^{\mathrm{sing}}_{c}`. Valid when: Valid when the heat-kernel endpoint box has a uniform source neighborhood and lower cumulants are subtracted inside log Z_v.
- color factor for singlet endpoint box: `c_N=\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2`. Valid when: Applies after singlet projection of the four Wilson flux insertions and the fixed plaquette-sheet normalization is used.
- null-channel endpoint dominance: `D_v=2G_{12,v}-4G_{13,v}-4G_{23,v}`. Valid when: Valid after the three-hairpin Feshbach null vector contracts the endpoint incidence Gram entries in the fixed block.
- endpoint scalar after cancellations: `\mathcal C_{\partial}=M_G+T_{\mathrm{tail}}-\sum_v c_N\,\beta_vD_v`. Valid when: Requires negative compact-group endpoint cumulants, Wick-square connected-log cancellation, and straight f f null-incidence cancellation before tails are added.
- certified lower endpoint interval: `\underline{\mathcal C}_{\partial}=M_G+\tau_- -\sum_v c_N\,\beta_v^+\,[d_v^+]_+`. Valid when: Valid when beta_v lies in a nonnegative interval and D_v is enclosed by [d_v^-,d_v^+] for each endpoint box.
- finite OS gate from endpoint interval: `\underline{\mathcal C}_{\partial}>0\Rightarrow \text{endpoint block promoted},\qquad \overline{\mathcal C}_{\partial}<0\Rightarrow \text{finite falsifier}`. Valid when: Applies only to the fixed post-H,K null channel after all previous Schur-Feshbach gates and same-theory identifications are valid.

## Attempted Derivation

- Start from the already fixed finite Schur-Feshbach post-H,K null channel and denote its positive Gaussian margin by M_G, avoiding any restatement of the earlier threshold.
- Use the heat-kernel plaquette-sheet regulator and insert a source sY localized in endpoint box v. The connected fourth derivative of log Z_v gives the singlet four-flux cumulant K_v^{sing}.
- The connected logarithm removes Wick-square disconnected contractions; the prior null incidence identity removes the straight nonabelian f f contact. Remaining nonlocal or corner mismatch is assigned to T_tail.
- Write K_v^{sing}=-beta_v on boxes with certified negative compact-group fourth cumulant. The local endpoint contribution to the null scalar is then -c_N beta_v D_v.
- Contract the fixed null weights to obtain D_v=2G12-4G13-4G23. Since beta_v is nonnegative, the contribution is dangerous exactly on the clipped positive part [D_v]_+.
- Interval arithmetic gives the valid lower certificate C_lower=M_G+tau_- - sum_v c_N beta_v^+ [d_v^+]_+. A positive lower endpoint promotes the finite block; a negative upper endpoint supplies a finite same-theory falsifier.

Blocking gap: The branch still lacks a cutoff-uniform endpoint incidence table G_{ij,v}, certified beta_v intervals from actual source derivatives, and a scale-sharp T_tail bound for corner overlap.

## Falsifiers

- A regulated endpoint box with certified D_v>0 and large beta_v makes C_upper<0, giving a finite same-theory OS falsifier.
- The heat-kernel source derivative K_v^{sing} fails to have a cutoff-uniform interval, so the endpoint carrier is not valid for the continuum passage.
- Straight f f contact cancellation breaks at a corner because the endpoint box intersects unequal Wilson sheet orientations.
- A negative tail from unresolved overlap is not bounded by T_tail and overwhelms the positive Schur-Feshbach margin.
- Two endpoint carriers judged geometrically equivalent have different regulated source derivatives, violating the same-theory condition.

## Learning

Cycle 264 attacks the conceptual pressure of making endpoint collapse sign-certifiable in the same Wilson theory. Declarative tension: finite collar OS positivity, unchanged gauge-invariant Wilson observables, and singular endpoint boundary OPE must jointly hold, but raw R is representation-limited and a raw kappa_4 spectrum is too strong because it ignores incidence signs. Compared with a global Schur-preimage matrix test, the clipped endpoint interval carrier is more local and directly computable after H,K; compared with a formal OPE assertion, it exposes primitive operations and falsifiers. The conceptual value signal is sharpness: negative compact-group kappa_4 is not the obstruction; positive endpoint dominance D_v>0 plus uncontrolled tail is. Success changes the finite post-H,K reflected-Wilson OS transfer gate by promoting the block; failure gives a finite same-theory falsifier. The larger Clay gates of continuum existence, full OS/Wightman reconstruction, nontriviality, and positive mass gap remain untouched, which is valuable because it removes or identifies a paper-handoff obstruction without overclaiming the mass gap theorem.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and endpoint-data design guide.`
- Rationale: The branch has reduced the remaining R term to endpoint dominance intervals; another abstract OS restatement would loop, while varying one incidence parameter tests exactly where the finite gate promotes or fails.
- Situation seed: Heat-kernel SU(N) plaquette-sheet endpoint boxes for the fixed three-hairpin Wilson block, with one tunable local geometry that increases the 12 footprint overlap while holding the 13 and 23 overlaps fixed.
- Varied variable: alpha=G_{12,v}/(G_{13,v}+G_{23,v}), the endpoint 12-dominance ratio.
- Held-fixed controls: Same heat-kernel regulator and Wilson sheet normalization for all source derivatives., Fixed H,K block, fixed Feshbach null vector, and fixed color factor c_N., Certified negative compact-group beta_v interval and the same tail-budget convention., No boundary counterterm and no enlargement of the gauge-invariant Wilson algebra.
- Expected observation: For alpha<=2 the endpoint box is protective or neutral; for alpha>2 the negative kappa_4 term becomes dangerous and must be compared quantitatively with M_G and T_tail.
- Transfer certificate needed: A cutoff-uniform equality between the imagined incidence deformation and actual regulated Wilson source derivatives, plus a tail bound proving that all unmodeled corner overlap is inside T_tail before the observation affects proof obligations.

## Next Experiment

Compute the endpoint incidence table for the actual three-hairpin heat-kernel plaquette sheets: enumerate endpoint boxes, evaluate or bound G12,G13,G23, clip D_v, then pair with seven-point source-derivative intervals for beta_v and a cutoff-uniform T_tail bound to produce the scalar interval [C_lower,C_upper].

# Endpoint-box R interval enclosure for flowed Wilson hairpins

## Candidate Lemma

Conditional Ward-interval endpoint lemma: for fixed H,K plus-channel hairpin sheets, the post-H,K endpoint scalar R_{++}^{ren}/kappa_4 has a valid lower certificate consisting of an explicit positive pair baseline, sectorwise Ward-subtracted connected four-curvature intervals, and a same-theory Schur-Feshbach leakage comparison.

## Definitions

- source object: reflected plus-channel endpoint hairpin sheet currents J_1^+,J_2^+ with flowed curvature insertions F_t and centered renormalized Wilson hairpin variables \widehat W_i(t,epsilon,a).
- target object: the finite endpoint-box scalar R_{++}^{ren}/\kappa_4 entering the H,K Schur-Feshbach matrix and compared with leakage L_+; it is not a continuum mass-gap observable.
- controlled interface: the cumulant expansion of \kappa_2(\widehat W_1,\widehat W_2) into a positive two-curvature pair baseline plus a Ward-subtracted connected four-curvature polarization Xi_{++}.
- same-theory condition: the same bare Yang-Mills measure, gradient-flow equation, Wilson observable family, reflection structure, subtractions, and finite H,K matrix are used throughout.
- regulator: Wilson lattice cutoff a or equivalent UV cutoff, positive Yang-Mills gradient flow time t, endpoint point-splitting epsilon, and fixed endpoint separation d.
- cancellation: disconnected product removal plus one-hairpin perimeter/cusp subtraction, followed by Ward conversion of longitudinal terms to endpoint total divergences.
- hard gate changed: finite endpoint-box positivity after H,K; untouched gates are continuum construction, OS/Wightman axioms, nontriviality, and Hamiltonian mass gap.

## Assumptions

- Model/regime: pure four-dimensional Euclidean SU(N) Yang-Mills, N>=2, with a reflection-positive lattice regulator or a positive-flow continuum cutoff.
- Cutoff hierarchy: a << epsilon << sqrt(8t) <= c d, with endpoint boxes disjoint and fixed H,K combinatorics.
- Uniformity: interval bounds and the remainder C_rem are uniform on the chosen compact regulator window; otherwise the statement is only a finite-cutoff diagnostic.
- Same-theory naturalness: cusp and perimeter counterterms are extracted from the same Wilson hairpin family, with no external mass term, Higgs field, or changed boundary action.
- Schur-Feshbach input: L_+ is already computed from the same finite reflected-Wilson H,K inner-product matrix.
- Non-claim: even a positive certificate proves only this local endpoint repair and not the Clay existence-and-mass-gap theorem.

## Equations

- flowed-curvature-kernel: `\mathcal D^{ab}_{\mu\nu,\rho\sigma}(t;z)=\delta^{ab}\int\frac{d^4p}{(2\pi)^4}\,e^{ip\cdot z-2tp^2}\frac{(p_\mu\delta_{\nu\alpha}-p_\nu\delta_{\mu\alpha})(p_\rho\delta_{\sigma\alpha}-p_\sigma\delta_{\rho\alpha})}{p^2}`. Valid when: Valid when positive gradient flow time separates the endpoint boxes and the curvature insertions are evaluated before removing the common regulator.
- positive-pair-baseline: `P_{++}=2(N^2-1)\mathcal G_{++},\qquad \mathcal G_{++}=\int (J_1^+\mathcal D_tJ_2^+)(J_1^+\mathcal D_tJ_2^+)\ge0`. Valid when: Applies after diagonal normalization of the plus hairpin channel, with nonzero sheet-current pairing and same-theory one-hairpin subtractions already performed.
- renormalized-R-decomposition: `\frac{R_{++}^{ren}(t,\epsilon,a)}{\kappa_4}=P_{++}+g_t^2N(N^2-1)\Xi_{++}(t,\epsilon,a)+E_4(t,\epsilon,a)`. Valid when: Requires the Ward-subtracted flowed cumulant expansion with fixed H,K endpoint geometry and a uniform remainder in the chosen regulator window.
- sector-polarization: `\Xi_{++}=I_{3g}+I_{4g}+I_{ct}+I_{end},\qquad I_s=\int_{B_{end}^4}K_s^{Ward}(J_1^+,J_2^+;x_1,\ldots,x_4)`. Valid when: Valid when the reflected Wilson endpoint boxes are separated at positive flow time and all longitudinal sectors have been Ward reduced.
- interval-lower-certificate: `\frac{R_{++}^{ren}}{\kappa_4}\ge P_{++}+g_t^2N(N^2-1)\sum_s\ell_s-C_{rem}g_t^4`. Valid when: Valid for a finite cell partition whose interval kernels enclose every Ward-reduced sector on the same flowed regulator.
- endpoint-promotion-test: `P_{++}+g_t^2N(N^2-1)\sum_s\ell_s-C_{rem}g_t^4>L_+`. Valid when: Applies only after the Schur-Feshbach leakage L_+ has been computed from the same finite H,K inner-product matrix.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: reflected plus-channel endpoint hairpin sheet currents J_1^+,J_2^+ with flowed curvature insertions F_t and centered renormalized Wilson hairpin variables \widehat W_i(t,epsilon,a).; target object: the finite endpoint-box scalar R_{++}^{ren}/\kappa_4 entering the H,K Schur-Feshbach matrix and compared with leakage L_+; it is not a continuum mass-gap observable.; Model/regime: pure four-dimensional Euclidean SU(N) Yang-Mills, N>=2, with a reflection-positive lattice regulator or a positive-flow continuum cutoff..
- Replace the raw plus-channel Wilson hairpins by centered renormalized flowed variables \widehat W_i and endpoint sheet currents J_i^+; centering removes one-point and disconnected-product terms.
- Expand \kappa_2(\widehat W_1,\widehat W_2) at positive flow time. The two cross-pairings of flowed curvatures give the explicit positive baseline P_{++}=2(N^2-1)G_{++} after the prior diagonal normalization.
- Collect the non-Gaussian connected four-curvature contribution into sectors I_{3g}, I_{4g}, I_{ct}, and I_{end}. The color factor left after trace normalization is N(N^2-1).
- Use Ward identities to move longitudinal propagator derivatives to endpoint total divergences. Opposite hairpin sides and the one-hairpin cusp/perimeter subtraction cancel the endpoint-local divergent pieces.
- Partition B_{end}^4 into finite cells. For each sector kernel K_s^{Ward}, compute interval enclosures [ell_s,u_s] and add a uniform |E_4|<=C_rem g_t^4 remainder.
- Compare the certified lower bound for R_{++}^{ren}/kappa_4 with the same-theory Schur-Feshbach leakage L_+.

Blocking gap: The actual interval quadrature has not yet enclosed Xi_{++}; the uniform g_t^4 remainder and cusp-cancellation bookkeeping must be certified in the same regulator window.

## Falsifiers

- Endpoint-kernel falsifier: Ward reduction leaves an uncanceled cusp or perimeter divergence after same-theory one-hairpin subtraction.
- Geometry falsifier: the extracted H,K plus-channel endpoint current has zero transverse pairing, so P_{++}=0 and the repair loses its positive baseline.
- Size falsifier: the certified lower interval satisfies P_{++}+g_t^2N(N^2-1)sum ell_s-C_rem g_t^4<=L_+.
- Regulator falsifier: no plateau exists as a, epsilon, and t are varied inside a<<epsilon<<sqrt(8t)<<d.
- Same-theory falsifier: the subtraction or flow used to define R_{++}^{ren} cannot be identified with the reflected Wilson inner product that produced H,K.
- Remainder falsifier: the valid bound on E_4 is wider than the entire pair baseline and makes the endpoint inequality undecidable.

## Learning

Conceptual pressure attacked: the finite tangent-cone theorem supplies an exact leakage L_+, but same-theory Wilson positivity, gradient-flow renormalization, and endpoint Schur-Feshbach positivity cannot jointly advance until the connected boundary-OPE polarization R_{++} has a certified sign/size. Declarative tension: the pair term is positive and color-explicit, yet the connected four-curvature polarization Xi_{++} may be negative or regulator-fragile. Carrier critique: raw Wilson contours are fragmented and representation-limited; sheet currents with endpoint currents are sharper because Ward cancellation and interval integration become primitive operations. Abstraction comparison: a non-Gaussian OS witness route is too global for this local obstruction, while a finite interval-kernel route directly changes the hard gate of post-H,K endpoint-box positivity. Efficient representation requirements: encode H,K sheets and endpoints; preserve gauge, color, reflection, and orientation invariants; use cumulant expansion, Ward subtraction, and interval arithmetic as primitives; quotient only by same-theory zero-pairing current equivalence; keep locality to endpoint boxes and finite cells; transfer through flowed Wilson cumulants; demote on cusp, plateau, geometry, same-theory, or interval-width falsifier. Conceptual value signal: this is route-changing at local scope because R_{++} becomes a valid falsifiable inequality rather than a symbolic placeholder, while the Clay target commitments remain intact and unclaimed.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch has already reduced the route to the missing R_{++} sign/size mediator; another abstract Wilson/OS restatement would loop, while a target-preserving flowed endpoint-box computation can promote or quarantine the repair.
- Situation seed: Flowed SU(3) Wilson lattice Yang-Mills on a large four-torus, with the previously fixed H,K plus-channel endpoint hairpin sheets embedded in two separated endpoint boxes and evaluated through the centered covariance of two renormalized thin hairpins.
- Varied variable: eta=sqrt(8t)/d, the flow-radius to endpoint-separation ratio.
- Held-fixed controls: Same Wilson action, same gauge group SU(3), same reflection plane, and same H,K plus-channel sheet-current geometry., Same centering, disconnected-product subtraction, one-hairpin cusp/perimeter subtraction, and Schur-Feshbach leakage L_+., Same endpoint box size in units of d and the same finite cell partition refinement rule., No change of theory, no external mass deformation, and no replacement by a Gaussian toy model.
- Expected observation: A valid route should show a stable positive lower bound B(eta)=P_{++}+g_t^2N(N^2-1)sum ell_s-C_rem g_t^4 over a nonempty eta window, or else a clean negative/undecidable interval that falsifies the endpoint-box repair.
- Transfer certificate needed: Uniform interval enclosure for all Ward-reduced sector kernels, proof of same-theory cusp cancellation, a regulator-window plateau as a->0 and epsilon->0 at positive flow time, and equality of the flowed cumulant scalar with the H,K Schur-Feshbach endpoint matrix entry.

## Next Experiment

Run the first certified Xi_{++} enclosure: fix SU(3), the prior H,K plus sheet currents, and eta in a small grid; evaluate interval bounds for I_{4g} and I_{ct} after Ward subtraction, then test whether their combined lower bound can still leave room for R_{++}^{ren}/kappa_4>L_+.

# Post-H,K endpoint-box kappa4 shell certificate

## Candidate Lemma

For a finite reflected Wilson endpoint family with known H,K blocks, the heat-kernel post-H,K endpoint form has a valid lower bound Delta_sigma obtained from the Gaussian Schur-square, a row-sum envelope for the connected four-curvature cumulant kappa4, the OPE remainder, and the Schur hairpin subtraction. Delta_sigma>0 certifies only finite endpoint-box positivity; Delta_sigma<=0 with a witness vector is a falsifier for this Route A collar/hairpin branch.

## Definitions

- source object: heat-kernel regulated SU(N) reflected Wilson endpoint cumulants for a fixed finite sheet family E, including transported curvature two- and four-point connected functions at cutoff a and smearing sigma.
- target object: the finite endpoint compression of the Schur-corrected quadratic form Q_sigma=P_E(R_sigma-S_HK,sigma)P_E on the null-quotiented endpoint coefficient space.
- controlled interface: a sheet-kernel hypergraph whose vertices are endpoint sheets, edges are transported curvature cumulant contractions, shell labels record endpoint distance, and weights carry Wilson/OPE coefficients.
- same-theory condition: R_sigma, H, K, g_R, the heat-kernel regulator, Wilson normalization, and the null quotient are all computed from one OS-positive regulated Yang-Mills measure, with no imported sectoral data.

## Assumptions

- Model/regime: finite cutoff SU(N) Yang-Mills Wilson measure or a rigorously specified heat-kernel regularized continuum approximant with OS reflection positivity at scale sigma>a.
- Uniformity: the fourth-order boundary OPE for the selected Wilson sheets has operator-norm remainder at most e_OPE,sigma on the finite endpoint space.
- Cutoff/naturalness: sigma/a and endpoint-box diameter/sigma are fixed finite parameters during the certificate; no continuum or infinite-volume conclusion is claimed.
- Same-theory H,K: the collar block H, hairpin coupling K, and QHQ inverse entering S_HK are computed in the identical Wilson basis and regulator, with QHQ>=c_sigma I on the eliminated sector.
- Null quotient: endpoint vectors annihilated by the regulated Gram form are removed before taking lambda_min or row-sum bounds.

## Equations

- transported flux covariance: `C_{ij,\sigma}=\int_{\Sigma_i\times\Sigma_j}w_i(z)w_j(z')\,n_i^{\mu\nu}(z)n_j^{\rho\tau}(z')\,\mathcal U_i^{ab}(z)\mathcal U_j^{ab'}(z')\,\langle F^b_{\mu\nu}(z)F^{b'}_{\rho\tau}(z')\rangle_{c,\sigma}\,dz\,dz'`. Valid when: Valid when heat-kernel smearing scale sigma exceeds the cutoff and each transported curvature insertion lies inside the finite reflected endpoint box.
- post-HK R decomposition: `R_\sigma=\alpha_N g_R^4(C_\sigma\circ C_\sigma)+\frac{g_R^4}{16N^2}\kappa_{4,\sigma}+E^{\mathrm{OPE}}_\sigma,\qquad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after vacuum, perimeter, and same-loop disconnected factors are removed by normalized Wilson observables in the same regulated theory.
- dyadic shell row envelope: `\kappa_{4,\sigma}=\sum_{r=0}^{r_{\max}}\kappa^{(r)}_{4,\sigma},\qquad M_{4,\sigma}^-\le \|P_E\kappa_{4,\sigma}P_E\|\le \sum_r\rho_r,\quad \rho_r=\max_i\sum_j |(\kappa^{(r)}_{4,\sigma})_{ij}|`. Valid when: Requires a finite endpoint index set and dyadic shell partition with absolutely bounded transported four-curvature cumulant integrals.
- endpoint-box margin: `\Delta_\sigma=m_{G,\sigma}-\frac{g_R^4}{16N^2}\sum_r\rho_r-e_{\mathrm{OPE},\sigma}-s_{HK,\sigma},\quad m_{G,\sigma}=\lambda_{\min}P_E\alpha_N g_R^4(C_\sigma\circ C_\sigma)P_E`. Valid when: Valid after H,K are computed in the identical regulator and QHQ is uniformly positive on the eliminated hairpin sector.
- finite certificate implication: `\Delta_\sigma>0\ \Longrightarrow\ P_E(R_\sigma-S_{HK,\sigma})P_E\ge \Delta_\sigma I_E`. Valid when: Applies only on the finite null-quotiented endpoint space with the above same-theory cumulant and Schur data.

## Attempted Derivation

- Conceptual pressure attacked: the post-H,K route needs a mediator from finite same-theory Wilson cumulants to Schur-corrected positivity, not another OS density restatement.
- Declarative tension: Wilson/OPE coefficients, Schur-Feshbach subtraction, and endpoint positivity must be simultaneously valid in one regulated Yang-Mills theory; the missing mediator is a locality-preserving representation of the connected boundary-OPE polarization kappa4.
- Critique of carriers: scalar R is too weak and representation-limited; full OS observable density is too strong and circular for this finite gate; raw plaquette enumeration is fragmented. The sheet-kernel hypergraph is retained because it preserves color tensors, sheet geometry, cumulant cancellation, shell locality, and H,K data.
- Start with normalized endpoint Wilson observables and expand their reflected two-point function to fourth curvature order using heat-kernel smeared transported fluxes.
- Use SU(N) trace normalization to isolate the Gaussian crossed contraction with coefficient alpha_N=(N^2-1)/(8N^2); Schur-product positivity makes C_sigma o C_sigma positive semidefinite on the finite endpoint space.
- Use connected-cumulant subtraction to cancel vacuum, perimeter, and same-sheet disconnected terms; the remaining non-Gaussian term is the transported connected four-curvature cumulant kappa4_sigma.
- Decompose kappa4_sigma into dyadic endpoint shells. For shell r, define rho_r=max_i sum_j |kappa4^{(r)}_{ij}|; Gershgorin or Schur testing gives M4^- <= sum_r rho_r on the null-quotiented finite space.
- Subtract the known Schur term S_HK=PKQ(QHQ)^{-1}QKP and the OPE error to obtain Delta_sigma. This is the hard gate: Delta_sigma>0 promotes a finite endpoint certificate; a negative witness vector is a falsifier for this Route A branch.

Blocking gap: The first-shell interval rho_0 has not yet been evaluated from an explicit plaquette-sheet contraction, and the OPE tail plus s_HK must be numerical or symbolic intervals from the same H,K regulator before Delta_sigma is a proof object.

## Falsifiers

- Direct interval evaluation of kappa4^{(0)} gives g_R^4 rho_0/(16N^2)>m_G-s_HK-e_OPE before tail shells are added.
- The Gaussian matrix C_sigma o C_sigma has a null direction that survives the endpoint null quotient and is not repaired by higher valid Wilson data.
- H,K or S_HK are computed with a different regulator, coupling, basis, or normalization than R_sigma, breaking the same-theory condition.
- The heat-kernel OPE remainder is nonuniform in sigma/a or endpoint-box size, so e_OPE cannot be bounded on the certificate space.
- A Wilson trace identity or reflection symmetry changes the hypergraph compression and yields different Delta_sigma intervals.
- A negative endpoint vector x is found with x^*P_E(R_sigma-S_HK)P_E x<0; this is a finite route falsifier, not a Clay disproof.

## Learning

Cycle 264 turns the post-H,K obstruction into the hard gate Delta_sigma. The conceptual value signal is sharp and finite: the connected boundary-OPE polarization R is decomposed into a PSD Gaussian color square, a compressed kappa4 shell envelope, an OPE error, and the Schur hairpin subtraction. Success changes only the finite Route A endpoint-box positivity gate; failure gives a valid falsifier for the Wilson collar/hairpin route. The larger Clay gates--OS/Wightman axioms, nontrivial continuum limit, and positive Hamiltonian mass gap in the same theory--remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the first shell certificate.`
- Rationale: The branch has already named R and kappa4; another abstract restatement would loop. The next valid learning is whether the first endpoint shell can quantitatively overwhelm the Gaussian Schur-square after the known H,K subtraction.
- Situation seed: Take a finite SU(N) heat-kernel regulated endpoint box with the already fixed collar/hairpin Wilson sheets and known H,K. Evaluate the plaquette-sheet contraction defining kappa4^{(0)} inside the endpoint ball of radius sigma, keeping transported color tensors and normalized Wilson cumulants.
- Varied variable: theta=sigma/a, the heat-kernel smearing-to-cutoff ratio.
- Held-fixed controls: Same Wilson endpoint sheet family E and same collar/hairpin H,K blocks., Same OS reflection plane, SU(N) trace normalization, coupling g_R, and heat-kernel normal ordering., Same endpoint null quotient and Schur subtraction S_HK., Same fourth-order Wilson/OPE truncation order and finite endpoint-box diameter/sigma.
- Expected observation: If rho_0(theta)+tail(theta) stays below m_G(theta)-s_HK(theta)-e_OPE(theta) on an interval, the endpoint-box positivity gate is promoted. If rho_0 alone exceeds that margin, the branch is demoted by a concrete finite falsifier.
- Transfer certificate needed: A same-regulator interval bound for kappa4^{(0)}, a certified tail envelope for r>0, an OPE operator-norm remainder, and exact H,K Schur data before the thought experiment can affect proof obligations.

## Next Experiment

Compute the r=0 endpoint plaquette-sheet integral for kappa4^{(0)} in the heat-kernel regulator, extract rho_0(theta), and compare g_R^4 rho_0/(16N^2) against m_G-s_HK-e_OPE before adding tail shells.
