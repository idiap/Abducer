# cycle-0274

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Post-H,K endpoint source-interval gate for reflected Wilson hairpins

## Candidate Lemma

Finite endpoint interval lemma: after H,K are fixed, sign-certified heat-kernel endpoint source intervals give a valid lower bound for the post-H,K null OS gate; positivity promotes this finite block, while a negative certified interval is a same-theory falsifier.

## Definitions

- source object: cutoff SU(N) heat-kernel plaquette-sheet endpoint boxes v with gauge-invariant Wilson source partition functions Z_{a,v}(sL_v).
- target object: the finite post-H,K null-channel OS scalar gate for the locked three-hairpin Wilson block.
- controlled interface: endpoint source-derivative intervals for singlet connected four-flux cumulants are contracted with null incidence D_v.
- same-theory condition: no boundary counterterm, no loop renormalization change, and identical reflected Wilson algebra across collar collapse.
- carrier: clipped endpoint interval data (K_v,beta_v,D_v,C_N,tau_tail) exporting only I_gate to the finite OS test.
- recovery map: identity on locked Wilson loop labels; endpoint source data are forgotten only after the scalar gate interval is formed.

## Assumptions

- Model: finite-volume four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette action and reflected Wilson plaquette sheets at fixed cutoff a.
- Regime: H,K and the corrected Schur-Feshbach null vector are already fixed; this lemma handles only the post-H,K endpoint R/kappa_4 term.
- Uniformity: eighth source derivatives and endpoint tails have cutoff-uniform bounds including large-field and topological sectors charged to tau_tail.
- Same-theory naturalness: source differentiation uses the original Wilson observables and regulator, not a boundary-renormalized or enlarged algebra.
- Sign condition: each endpoint cumulant interval is certified inside [-beta_v,0]; otherwise clipping by [D_v]_+ is not valid.

## Equations

- endpoint R decomposition: `R_{\rm end}=C_N\sum_v D_v\kappa_{4,v}^{\rm sing}+T_{\rm tail},\quad D_v=2G_{12,v}-4G_{13,v}-4G_{23,v}`. Valid when: Applies in the heat-kernel plaquette-sheet regulator after Wick-square subtraction and straight f f null-incidence cancellation.
- source stencil certificate: `\kappa_{4,v}^{\rm sing}\in[\Delta_h^4\log Z_v(0)-\varepsilon_v,\Delta_h^4\log Z_v(0)+\varepsilon_v],\quad \varepsilon_v=7h^4M_{8,v}/240`. Valid when: Valid when seven same-theory source evaluations obey a uniform eighth-derivative bound on each endpoint box.
- clipped promotion bound: `I_{\rm gate}^{\rm low}=M_G-C_N\sum_v\beta_v[D_v]_+-\tau_{\rm tail}>0`. Valid when: Requires sign-certified endpoint cumulants K_v subset [-beta_v,0] and a cutoff-uniform tail bound tau.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: cutoff SU(N) heat-kernel plaquette-sheet endpoint boxes v with gauge-invariant Wilson source partition functions Z_{a,v}(sL_v).; target object: the finite post-H,K null-channel OS scalar gate for the locked three-hairpin Wilson block.; Model: finite-volume four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette action and reflected Wilson plaquette sheets at fixed cutoff a..
- Localize R to endpoint boxes using the heat-kernel plaquette-sheet regulator; connected fourth source derivatives remove Wick-square pieces, and the straight f f contact cancels by null incidence.
- For each endpoint v, compute seven same-theory source values of log Z_v and enclose kappa_{4,v}^{sing} with the h^4 M8 stencil error.
- Use the certified sign K_v subset [-beta_v,0]: only positive D_v lowers the gate, so D_v<=0 is protective and enters no demotion bound.
- Add the cutoff-uniform tail tau_tail and compare I_gate^low with zero; positive promotes this finite block, negative certified upper interval gives a finite falsifier.

Blocking gap: The actual endpoint incidence table G_{ij,v}, same-theory source values, and cutoff-uniform M8/tail bounds are not yet computed for the locked hairpin geometry.

## Falsifiers

- falsifier: an endpoint source interval crosses positive values, invalidating kappa_4<=0 clipping and making D_v<0 potentially dangerous.
- A cutoff-dependent tau_tail or a required endpoint boundary counterterm breaks the same-theory transfer.
- Actual G_{ij,v} data show certified positive 12-endpoint dominance large enough that I_gate^high<0.
- Large-field or topological sectors destroy the uniform M8 derivative bound used by the stencil certificate.

## Learning

Conceptual pressure: endpoint collapse must be sign-certified without changing Wilson theory. Declarative tension: collar OS positivity, fixed gauge-invariant Wilson algebra, and singular endpoint OPE must coexist. The clipped source interval is sharper than raw R or raw kappa4 because it preserves incidence signs and exports one finite gate.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch is past abstract OS/Wilson obstructions; the hard gate is now a finite post-H,K endpoint interval whose sign can promote or falsify the block.
- Situation seed: Locked three-hairpin reflected Wilson block in SU(N) heat-kernel plaquette-sheet regulation, with four-flux sources supported in endpoint boxes around each reflected hairpin endpoint.
- Varied variable: Endpoint dominance ratio r=(C_N sum_v beta_v[D_v]_+ + tau_tail)/M_G.
- Held-fixed controls: Same heat-kernel regulator and same gauge-invariant Wilson loop algebra., Fixed H,K block, Feshbach null vector, reflection map, and Wilson normalization., Uniform large-field/topology tail budget tau_tail and no boundary counterterm.
- Expected observation: If r<1 with certified intervals, the finite endpoint term cannot demote OS positivity; if r>1 with I_gate^high<0, the endpoint OPE gives a finite same-theory falsifier.
- Transfer certificate needed: Exact endpoint incidence table, seven-point source intervals for each Z_v, cutoff-uniform M8 and tail bounds, and verification that the recovery map is identity on Wilson observables.

## Next Experiment

Compute the actual endpoint incidence table G_{ij,v} for the locked three-hairpin geometry, then run seven-point heat-kernel source stencils to certify K_v subset [-beta_v,0] and I_gate interval.

# Post-H,K endpoint-box R/kappa4 Hessian certificate

## Candidate Lemma

At fixed positive gradient-flow time, after perimeter, cusp, disconnected-product, and Ward affine-mode subtraction, the plus-channel endpoint-box Wilson polarization admits a computable lower bound R_{++}^{ren}/kappa_4 >= (N^2-1)G_{++}(2-N epsilon_H). If kappa_4(N^2-1)G_{++}(2-N epsilon_H)>L_+, the finite Schur-Feshbach endpoint-box gate is promoted; if the inequality fails by certified interval, this R-repair is demoted without implying any Clay-level conclusion.

## Definitions

- source object: a finite-volume cutoff SU(N) Wilson Yang-Mills measure with Wilson gradient flow time t>0, endpoint point-splitting eta, lattice spacing a, and centered renormalized thin hairpin currents J_i supported in a boundary box E of diameter rho.
- target object: the finite post-H,K Schur-Feshbach plus-channel endpoint-box coefficient R_{++}^{ren}/kappa_4 and its comparison with the already extracted leakage L_+.
- controlled interface: the map from flowed Wilson hairpin currents to the Ward-subtracted connected two-hairpin cumulant, decomposed into a positive pair baseline plus a connected four-curvature polarization interval.
- same-theory condition: the same cutoff action, same flow, same renormalization constants, same reflected Wilson observable algebra, and same H,K endpoint currents are used for G_{++}, Xi_{++}, R_{++}^{ren}, and L_+.
- carrier: sheet currents plus endpoint currents, not raw Wilson contours; quotient only by certified zero-pairing current equivalence.
- hard gate affected: finite endpoint-box positivity after H,K; continuum existence, OS/Wightman reconstruction, nontriviality, and Hamiltonian mass gap remain untouched.

## Assumptions

- Model/regime: finite lattice or heat-kernel regularized SU(N) Yang-Mills on a four-torus, with t>0 fixed before a->0 and V->infty are discussed.
- Uniformity: all interval constants are local in the endpoint box and independent of the finite H,K matrix size; no volume-uniform full-measure basin is claimed.
- Ward regime: the flowed curvature cumulant satisfies the lattice/flow Ward identities needed to remove constant and affine endpoint modes after the stated subtractions.
- Moment regime: the plus-channel endpoint current has zero monopole and dipole moments in each paired endpoint cell after orientation signs are included.
- Naturalness/cutoff condition: eta<rho<=c sqrt(t), with no topology tunneling or large-field summability claim beyond fixed regulated support.
- Same-theory transfer: L_+ is imported only from the finite Schur-Feshbach calculation for the same H,K objects, not from a different effective model.

## Equations

- R-pair-plus-C4: `\frac{R_{++}^{ren}}{\kappa_4}=(N^2-1)\mathcal G_{++}\left(2+N\Xi_{++}\right)`. Valid when: Valid when the flowed two-hairpin cumulant is expanded through the same renormalized endpoint currents and the disconnected product plus one-hairpin perimeter and cusp pieces have been subtracted.
- positive-pair-baseline: `\mathcal G_{++}=\int_{E\times E} J_+^{a,\mu\nu}(x)J_+^{b,\rho\sigma}(y)\,\Pi^{ab}_{t;\mu\nu,\rho\sigma}(x-y)^2\,dx\,dy>0`. Valid when: Valid when the plus-channel endpoint geometry has nonzero flowed two-curvature pairing and reflection orientation does not cancel the endpoint current identically.
- Hessian-polarization-bound: `|\Xi_{++}|\le \epsilon_H:=\frac{1}{\mathcal G_{++}}\sum_{s\in\{3g,4g,ct,end\}} C_s\,\mathsf M_2(J_+)^2\,\sup_{E^4}\|\nabla_{end}^2 K^{Ward}_{s,t}\|`. Valid when: Applies after Ward affine-mode subtraction and plus-channel monopole and dipole cancellation on each endpoint cell of diameter rho.
- promotion-inequality: `\kappa_4(N^2-1)\mathcal G_{++}(2-N\epsilon_H)>L_+`. Valid when: Valid when L_+ is the same finite Schur-Feshbach leakage computed for the identical H,K endpoint basis and normalization.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: a finite-volume cutoff SU(N) Wilson Yang-Mills measure with Wilson gradient flow time t>0, endpoint point-splitting eta, lattice spacing a, and centered renormalized thin hairpin currents J_i supported in a boundary box E of diameter rho.; target object: the finite post-H,K Schur-Feshbach plus-channel endpoint-box coefficient R_{++}^{ren}/kappa_4 and its comparison with the already extracted leakage L_+.; Model/regime: finite lattice or heat-kernel regularized SU(N) Yang-Mills on a four-torus, with t>0 fixed before a->0 and V->infty are discussed..
- Conceptual pressure attacked: finite Schur-Feshbach positivity requires a same-theory endpoint mediator, but pair positivity and gradient-flow renormalization leave the connected four-curvature polarization C4 uncontrolled.
- Declarative tension: the positive pair covariance, Ward/cusp-renormalized Wilson observable, and finite Feshbach leakage comparison must all hold simultaneously; the missing mediator is a certified sign/size bound for Xi_{++}.
- Carrier critique: raw Wilson contours are fragmented and representation-limited for cancellations; sheet currents plus endpoint currents are sharper because Ward subtraction, moment cancellation, and interval Hessian bounds become primitive operations.
- Route comparison: a global non-Gaussian OS witness is too weakly targeted for this local obstruction, while a finite interval-kernel proof search directly decides endpoint-box positivity after H,K.
- Write the centered flowed hairpin cumulant as pair contractions plus the connected four-curvature remainder; color algebra gives pair color 2(N^2-1) and connected color N(N^2-1).
- Use disconnected-product subtraction and one-hairpin perimeter/cusp subtraction to isolate the endpoint-local C4 polarization.
- Use Ward identities to remove constant and affine endpoint kernel modes; plus-channel orientation imposes zero monopole and dipole moments of J_+ in each endpoint cell.
- Taylor expand each Ward-subtracted sector kernel on endpoint cells. The affine terms integrate to zero, so the first surviving term is controlled by endpoint second moments and a C2 Hessian seminorm.
- Normalize by the positive pair baseline G_{++} to obtain |Xi_{++}|<=epsilon_H and hence the lower bound (N^2-1)G_{++}(2-N epsilon_H).
- Compare the lower bound with the already finite Schur-Feshbach leakage L_+; this is the hard gate, and success promotes only finite endpoint-box positivity while failure quarantines the R repair.

Blocking gap: The actual H,K endpoint currents and the Ward-subtracted sector Hessian seminorms have not yet been interval-enclosed for the chosen regulator; this is the remaining proof-search computation.

## Falsifiers

- falsifier: the actual H,K plus-channel endpoint current has nonzero affine moment after orientation signs, invalidating Hessian suppression.
- falsifier: G_{++}=0 because the endpoint geometry cancels the positive flowed pair baseline.
- falsifier: a Ward-subtracted sector retains a cusp or endpoint singularity not bounded by the stated C2 seminorm.
- falsifier: certified epsilon_H>=2/N, so the connected polarization can erase the positive pair term.
- falsifier: the lower interval for R_{++}^{ren}/kappa_4 does not exceed L_+, demoting the endpoint-box repair.
- falsifier: the regulator plateau changes sign or size as a, V, or t are varied, showing no same-theory stable finite input.
- Stress case: shrink eta/sqrt(t) to zero while holding rho/sqrt(t) fixed; the C4/pair ratio should scale like eta^2 or the moment-cancellation mechanism is false.

## Learning

Cycle 274 makes the endpoint R/kappa4 task sharper: the connected boundary-OPE polarization is no longer just Xi_{++}; it is bounded by an endpoint-moment Hessian certificate after Ward, cusp, and plus-channel monopole/dipole cancellation. The conceptual value signal is local but route-changing: it converts the dangerous C4 term into a valid finite interval inequality against L_+. Efficient representation requirements are explicit: encode H,K sheets and endpoint currents; preserve gauge, color, reflection, orientation, and same-theory invariants; use cumulant expansion, Ward subtraction, endpoint Taylor expansion, heat-kernel majorants, and interval arithmetic as primitives; quotient only by certified zero-pairing current equivalence; keep locality to endpoint boxes and finite cells; transfer through flowed Wilson cumulants; demote on Ward, cusp, plateau, geometry, cutoff-uniformity, or interval-width falsifier. Hard gate: finite endpoint-box positivity after H,K; success promotes that finite gate, failure quarantines the R repair, and both leave Clay existence, OS/Wightman axioms, nontriviality, and positive Hamiltonian mass gap untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the endpoint-moment Hessian certificate.`
- Rationale: The branch already has the symbolic R representation; only a concrete same-theory Wilson input can decide whether the endpoint-box gate is promoted or quarantined.
- Situation seed: Finite SU(2) Wilson lattice Yang-Mills on a four-torus with Wilson gradient flow, the extracted H,K hairpin endpoint currents embedded in one boundary box, and centered flowed Wilson hairpin observables with perimeter, cusp, and disconnected-product subtraction.
- Varied variable: theta=eta/sqrt(t), the endpoint point-splitting measured in flow-radius units.
- Held-fixed controls: The same Wilson action, flow definition, H,K endpoint-current basis, and reflection orientation are held fixed., The physical endpoint-box diameter rho/sqrt(t), finite Schur-Feshbach leakage L_+, and plus-channel normalization are held fixed., The Ward-subtraction prescription and one-hairpin renormalization constants are held fixed., No continuum OS or spectral-transfer claim is allowed from the finite experiment.
- Expected observation: If the Hessian mechanism is valid, the interval for |Xi_{++}|/G_{++} decreases quadratically in theta until a regulator plateau; if it plateaus at O(1) or changes sign erratically, the R repair is demoted.
- Transfer certificate needed: Before intuition may affect proof obligations, provide a same-theory interval certificate for G_{++}>0, zero monopole/dipole endpoint moments, Ward-subtracted C2 sector bounds, and the inequality kappa_4(N^2-1)G_{++}(2-Nepsilon_H)>L_+.

## Next Experiment

Extract the actual H,K endpoint current table, compute monopole/dipole moments and G_{++} under gradient-flow heat-kernel pairing, then interval-bound one sector Hessian K^{Ward}_{3g,t} on endpoint cells before attempting all-sector Xi_{++}.

# Post-H,K heat-kernel Wilson endpoint-box kappa4 interval certificate

## Candidate Lemma

Finite same-regulator endpoint-box certificate: for a fixed heat-kernel regulated SU(N) Wilson endpoint sheet family and already computed finite H,K hairpin data, the Schur-corrected endpoint form is nonnegative if the PSD Gaussian color square dominates the compressed negative connected four-curvature cumulant, the OPE error, and the Schur hairpin energy. This changes only the finite Route A endpoint-box gate; OS reconstruction, continuum existence, and Hamiltonian mass gap remain untouched.

## Definitions

- source object: heat-kernel regularized finite-volume SU(N) Euclidean Yang-Mills Wilson cumulants for a fixed reflected endpoint sheet family, with lattice spacing a or continuum cutoff Lambda, smearing scale sigma, and reflection-positive measure before any continuum limit.
- target object: the finite real symmetric endpoint quadratic form on vacuum-subtracted Wilson collar coefficients after eliminating hairpin variables by the Schur-Feshbach complement, not the full reconstructed Hilbert space.
- controlled interface: a sheet-kernel hypergraph Rec_sigma carrying sheets, weights, heat-kernel transporters, color tensors, shell labels, OPE error intervals, and H,K Schur data into the endpoint-box matrix R_sigma-S_HK.
- same-theory condition: C_sigma, K4_sigma, E_OPE,sigma, H, and K are computed with the same regulator, coupling normalization, Wilson basis, reflection convention, and finite-volume boundary condition.
- bridge/carrier: the manipulated observable is the connected boundary-OPE polarization R_sigma, decomposed as a gauge-invariant Wilson cumulant rather than an abstract scalar R.
- recovery maps: Wilson sheet data -> transported smeared curvature flux Phi_i; cumulant compression -> C_sigma and K4_sigma; Schur recovery -> S_HK=B^*E_H^{-1}B; interval recovery -> Delta_sigma.
- representation morphisms: quotient maps may identify only exact Wilson trace symmetries, orientation-paired reflected sheets, and color-index relabelings that preserve all compressed cumulants.
- invariants preserved: gauge invariance, reflection support, vacuum/perimeter cancellation, Gaussian/kappa4 separation, endpoint compression, color factor alpha_N, and same-theory normalization.

## Assumptions

- Model: fixed finite cutoff SU(N) Yang-Mills with heat-kernel smearing e^{sigma Delta_A} and reflection-positive Wilson regulator; no continuum or infinite-volume assertion is made.
- Regime: endpoint sheets are finite, separated at the cutoff scale, and small enough for the fourth-order Wilson boundary OPE with certified remainder e_OPE,sigma.
- Uniformity: all constants are finite-box constants; promotion to Clay-level gates would additionally require volume/cutoff uniform full-measure basin entry, large-field and topology summability, and regulator-independent Schwinger functions.
- Same-theory naturalness: H,K, the Wilson OPE coefficients, and kappa_4 are not imported from different gauges, regulators, volumes, or couplings.
- Hairpin condition: the eliminated hairpin block E_H=QHQ is positive on the finite complement with a known lower spectral bound, so S_HK is a well-defined finite matrix.
- Endpoint compression: the finite endpoint basis is fixed before estimating K4_sigma; no adaptive quotient may discard a negative witness vector.
- Error budget: ||E_OPE,sigma|| and shell tail T_{L,sigma} are included in the final interval and cannot be hidden inside positivity language.
- Non-claim: Delta_sigma>0 proves only finite endpoint-box positivity for the worked H,K geometry, not OS positivity, observable density, or a physical-unit mass gap.

## Equations

- transported smeared flux: `\Phi_i^a(\sigma)=\sum_{p\in\mathcal S_i} w_{ip}\int_{S_p} \operatorname{Ad}_{U_{x\to b_i}}(e^{\sigma\Delta_A}F_{\mu\nu}(x))^a\,dS_p^{\mu\nu}(x)`. Valid when: Valid when the endpoint sheet family, heat-kernel transporter, basepoints, and finite cutoff regulator are fixed before compression.
- two-flux covariance kernel: `C_{ij,\sigma}=\frac{1}{N^2-1}\sum_a\langle \Phi_i^a(\sigma)\Phi_j^a(\sigma)\rangle_c`. Valid when: Valid when the same finite regulated Yang-Mills measure defines both flux insertions and the connected expectation.
- connected endpoint polarization decomposition: `R_{ij,\sigma}=\alpha_N g_R^4\,(C_{ij,\sigma})^2+\frac{g_R^4}{16N^2}K^{(4)}_{ij,\sigma}+E^{\mathrm{OPE}}_{ij,\sigma},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after vacuum and perimeter disconnected Wilson pieces cancel in the same-regulator fourth-order boundary OPE.
- kappa4 shell row envelope: `M^-_{4,\sigma}(L)\le \max_i\sum_j\left|\sum_{\ell=0}^{L}K^{(4)}_{ij,\sigma}[\ell]\right|+T_{L,\sigma}`. Valid when: Requires a sheet-kernel shell decomposition with a certified tail bound for all omitted connected four-flux cumulants.
- Schur-corrected endpoint margin: `\Delta_\sigma=\lambda_{\min}\big(\alpha_N g_R^4(C_\sigma\circ C_\sigma)\big)-\frac{g_R^4}{16N^2}M^-_{4,\sigma}(L)-\|E^{\mathrm{OPE}}_\sigma\|-\|S_{HK}\|`. Valid when: Valid when H,K are known in the same finite Wilson basis and the matrix norms are taken on the fixed endpoint coefficient space.
- finite promotion implication: `\Delta_\sigma>0\;\Longrightarrow\; R_\sigma-S_{HK}\succeq 0\quad\text{on the endpoint box}`. Valid when: Valid only for the finite endpoint-box quadratic form after all listed same-theory inputs and error budgets are certified.

## Attempted Derivation

- Freeze Clay target and claim level: the cycle proves or falsifies only a finite endpoint-box Wilson positivity certificate; it does not assert OS/Wightman reconstruction, continuum Schwinger functions, observable density, or Hamiltonian spectral transfer.
- Declare the declarative tension: same-theory Wilson/OPE coefficients, connected kappa_4 negativity, and finite Schur-Feshbach subtraction must jointly control one endpoint quadratic form, but scalar R loses color/locality data, full OS density is circular for this gate, and raw plaquette enumeration is too fragmented for interval proof search.
- Choose the heat-kernel Wilson regulator at scale sigma and define transported fluxes Phi_i for each endpoint sheet; this preserves gauge-invariant Wilson observables and gives recovery maps from sheets to C_sigma and K4_sigma.
- Expand the pair of vacuum-subtracted endpoint Wilson observables to fourth order in the transported curvature flux. Vacuum and perimeter disconnected terms cancel because the same normalized Wilson observables and regulator are used on both sides of the covariance.
- Separate the surviving boundary-OPE polarization into alpha_N g_R^4(C_sigma circ C_sigma), g_R^4 K4_sigma/(16N^2), and E_OPE,sigma. The first term is PSD by the Schur product theorem; the second is the connected four-curvature cumulant that can carry a negative sign.
- Compress K4_sigma by locality shells in the sheet-kernel hypergraph and bound its negative spectral contribution by a row-sum envelope M^-_{4,sigma}(L) plus a tail T_{L,sigma}. This is a finite Gershgorin/min-max estimate, not a continuum RG estimate.
- Insert the already computed H,K hairpin data through S_HK=B^*E_H^{-1}B and subtract it from R_sigma. The hard gate is Delta_sigma; success changes the finite Route A endpoint-box proof state to certified, while failure identifies whether kappa4, OPE error, or hairpin coupling kills the geometry.
- Compare abstraction routes: OS observable density is too strong and would define the target through the bridge; scalar R is too weak and representation-limited; raw plaquette enumeration is exact but fragmented. The sheet-kernel hypergraph is retained because it encodes sheets, weights, transporters, color tensors, shell labels, multiplicities, OPE errors, and Schur data with audited equivalence.

Blocking gap: The first actual H,K endpoint geometry still needs numerical or symbolic insertion of C_sigma, shell-resolved K4_sigma[ell], E_OPE,sigma, and S_HK in one regulator. Without those values Delta_sigma is a valid finite theorem schema, not a completed endpoint certificate.

## Falsifiers

- Concrete falsifier: find v in the endpoint coefficient space with v^T(R_sigma-S_HK)v<0 using the same heat-kernel regulator and unquotiented Wilson sheet data.
- Interval falsifier: Delta_sigma<=0 after certified K4 shell row sums, OPE error, and Schur hairpin energy are inserted.
- Representation falsifier: a quotient class changes C_sigma, K4_sigma, or S_HK, or a negative raw witness does not lift from the reduced hypergraph.
- Regulator falsifier: the sign of Delta_sigma is not stable under the allowed finite sigma/a window while all other endpoint controls are fixed.
- Large-field/topology frontier falsifier: any attempted continuum promotion fails because cumulant tails are nonuniform across RG steps or topological sectors.
- Same-theory falsifier: H,K imported from one cutoff theory and K4_sigma from another invalidate the endpoint certificate even if each isolated computation is positive.

## Learning

Cycle 274 attacks the conceptual pressure that the post-H,K endpoint route needs an actual mediator from connected Wilson cumulants to Schur-corrected positivity. The declarative tension is now operational: Wilson/OPE coefficients, kappa_4 negativity, OPE remainders, and hairpin Schur energy must be valid in one cutoff theory, while Clay-level OS reconstruction and spectral transfer stay quarantined. Scalar R is too weak and representation-limited; OS density is too strong and circular; raw enumeration is exact but fragmented. The sheet-kernel hypergraph is retained because it preserves the color, geometry, locality, cancellation, and H,K data needed for a finite interval certificate. The hard gate is Delta_sigma: success certifies only the worked endpoint box, and failure is a precise falsifier. The conceptual value signal is route-changing at finite scope because it turns the unknown boundary-OPE polarization into a computable sign/size test with explicit recovery maps and error budgets.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and coefficient-extraction guide.`
- Rationale: The branch has repeated the Delta_sigma abstraction enough; the next valid learning must test whether the actual heat-kernel connected Wilson cumulant can dominate the Schur hairpin subtraction in the first H,K endpoint box.
- Situation seed: Finite SU(N) heat-kernel Wilson endpoint box with two reflected collar sheets and the first hairpin block H,K already fixed; evaluate the connected cumulant of two quadratic transported curvature fluxes after vacuum/perimeter cancellation.
- Varied variable: The smearing-to-cutoff ratio sigma/a within a fixed finite window, e.g. 1.5 <= sigma/a <= 3, while shell cutoff L is increased until the certified tail is below the target margin.
- Held-fixed controls: Gauge group SU(N), trace normalization, finite volume, boundary condition, and heat-kernel regulator family., The same endpoint Wilson sheet basis, reflection convention, H,K Schur data, and renormalized coupling g_R., The fourth-order Wilson OPE order, vacuum/perimeter subtraction rule, and quotient-invariance audit., No continuum, OS-density, or Hamiltonian mass-gap inference is allowed from the finite observation.
- Expected observation: If the route is viable, the PSD Gaussian color square has a positive lower endpoint eigenvalue that remains larger than the kappa4 negative shell envelope, OPE error, and S_HK across the finite sigma/a window. If not, a stable negative witness vector identifies the obstruction.
- Transfer certificate needed: A same-regulator interval certificate for C_sigma, K4_sigma shells, E_OPE,sigma, and S_HK, plus a quotient audit proving the reduced hypergraph preserves the raw Wilson quadratic form before Delta_sigma may enter proof obligations.

## Next Experiment

Compute the first same-regulator endpoint interval: enumerate the endpoint sheet hypergraph for the selected H,K geometry, form C_sigma, evaluate K4_sigma shells 0 and 1 or rigorous row envelopes, attach E_OPE,sigma and S_HK, then report the certified sign of Delta_sigma or a lifted negative witness.

