# cycle-0277

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint-source interval gate for the post-H,K reflected-Wilson block

## Candidate Lemma

Finite endpoint-source interval gate: for the fixed three-hairpin reflected-Wilson block in the heat-kernel plaquette-sheet regulator, the post-H,K endpoint contribution is certified by one interval [I_-,I_+]. If I_->0 the finite same-theory OS transfer block is promoted; if I_+<0 it is a concrete falsifier. This changes only the finite post-H,K reflected-Wilson OS gate and does not claim continuum existence or a mass gap.

## Definitions

- source object: regulated endpoint source carrier C_ep=(Z_v,D_v,[beta_v^-,beta_v^+],C_N,T_tail) extracted from heat-kernel plaquette-sheet Wilson collars at the endpoint boxes v of the fixed three-hairpin block.
- target object: the finite post-H,K Schur-Feshbach scalar I_gate=M_G+R_end for the same-theory reflected-Wilson OS transfer block, not the full Yang-Mills continuum theory.
- controlled interface: seven-point source derivative intervals and endpoint incidence contractions map C_ep to a valid interval enclosure [I_-,I_+] for I_gate.
- same-theory condition: the Wilson loops, heat-kernel plaquette sheets, reflection map, normalization, and gauge-invariant observable algebra are identical before and after collar collapse; no boundary counterterm or algebra enlargement is allowed.
- carrier being manipulated: clipped endpoint dominance, where D_v=2b_12(v)-4b_13(v)-4b_23(v) keeps the null-channel incidence signs that raw R forgets.

## Assumptions

- Model: four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette action and reflection-positive Wilson collar observables.
- Regime: fixed finite three-hairpin block after the H,K Schur-Feshbach reduction; endpoint boxes are smaller than the collar scale but remain regulator-resolved.
- Cutoff: all estimates are at finite cutoff a and finite collar delta, with constants recorded before any continuum passage is attempted.
- Uniformity: the eighth-source-derivative bound M_{8,v} and the tail T_tail are uniform over the endpoint subdivision used in this finite block.
- Same-theory: source insertions differentiate the same regulated Wilson plaquette-sheet partition function that defines the OS matrix entries.
- Validity: Wick-square Gram terms and straight f f contacts have already been removed by the connected-log and null-incidence cancellations.

## Equations

- endpoint dominance: `D_v=2b_{12}(v)-4b_{13}(v)-4b_{23}(v)`. Valid when: Applies after the H,K Feshbach reduction fixes the null-channel weights and endpoint boxes.
- seven point fourth source derivative: `\mathcal D_h^4 f_v(0)=\frac{-f_v(-3h)+12f_v(-2h)-39f_v(-h)+56f_v(0)-39f_v(h)+12f_v(2h)-f_v(3h)}{6h^4}`. Valid when: Valid when f_v(s)=\log Z_v(s) is C^8 on the certified source interval.
- source error enclosure: `\left|\kappa_{4,v}-\mathcal D_h^4\log Z_v(0)\right|\le 7h^4M_{8,v}/240`. Valid when: Requires the same endpoint-box heat-kernel source family and a uniform eighth derivative bound.
- gate interval: `\ell_v=-C_N\beta_v^+[D_v]_+ + C_N\beta_v^-[-D_v]_+,\quad u_v=-C_N\beta_v^-[D_v]_+ + C_N\beta_v^+[-D_v]_+,\quad I_-=M_G+\sum_v\ell_v-T_{\rm tail},\ I_+=M_G+\sum_v u_v+T_{\rm tail}`. Valid when: Valid when beta_v=-kappa_{4,v} is enclosed in [beta_v^-,beta_v^+] and C_N is positive.

## Attempted Derivation

- Attack conceptual pressure: endpoint collapse must be sign-certified without changing the Wilson theory, while collar OS positivity and singular endpoint OPE are both present.
- Declarative tension: finite collar OS positivity, fixed gauge-invariant Wilson observables, and connected endpoint singularities must jointly hold; raw R is representation-limited because it forgets null-channel incidence signs.
- Replace raw R by C_ep. The source object remains a regulated Wilson endpoint partition function, and the target remains a finite Schur-Feshbach scalar, so the bridge is not defined circularly.
- Use connected log Z_v to remove Wick-square disconnected pieces; use the established null-incidence identity to remove straight f f contact pieces.
- Write the remaining endpoint term as -C_N beta_v D_v plus a charged tail, with beta_v=-kappa_{4,v} certified by the seven-point fourth-source stencil.
- Compute the sign table: D_v=2 for 12-only binary boxes, D_v=-4 for 13-only or 23-only boxes, and mixed boxes are nonpositive. Thus negative compact-group kappa_4 is not the falsifier by itself.
- Assemble interval arithmetic: positive D_v contributes to the lower endpoint bound, negative D_v is protective, and T_tail absorbs unresolved locality and corner overlap.
- Hard gate: the finite post-H,K reflected-Wilson OS transfer gate is promoted if I_->0 and demoted by a concrete falsifier if I_+<0; continuum construction, OS reconstruction for all observables, nontriviality, and mass gap are untouched.

Blocking gap: Actual beta_v source intervals and a cutoff-uniform T_tail for the real endpoint boxes have not been computed; the present cycle gives the valid finite certificate formula and the incidence sign classification.

## Falsifiers

- A 12-only endpoint family with certified beta_v and tail gives I_+<0, producing a finite same-theory OS falsifier.
- The eighth-derivative source bound M_{8,v} grows with cutoff so the stencil interval is not valid uniformly.
- Endpoint collapse requires a boundary counterterm or edge-mode algebra, violating the same-theory condition.
- Fractional leakage into 13 or 23 is misestimated; the actual D_v remains positive while the carrier declares it protective.
- A topological endpoint sector changes log Z_v source derivatives but is not charged to T_tail.
- The regulated reflected Wilson observables fail reflection positivity before the endpoint limit, invalidating the source object.

## Learning

Cycle 277 attacks the conceptual pressure of endpoint collapse in the same Wilson theory. The declarative tension is that finite collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must coexist, while raw R forgets incidence signs and raw kappa_4 overstates danger. Compared with the global Schur-preimage route, C_ep is local after H,K and exports one valid scalar interval; compared with formal OPE language, it has primitive operations: source differentiation, interval arithmetic, color multiplication, incidence contraction, clipping, and tail addition. Efficient representation requirements are now explicit: encode endpoint boxes, seven-point source stencils, beta intervals, b/D incidence, C_N, M_G, and T_tail; preserve Wilson normalization, reflection symmetry, null cancellations, cutoff bookkeeping, and same-theory observables; identify equivalents only by equal regulated source derivatives; keep locality finite by charging leftovers to T_tail; transfer only [I_-,I_+] to the finite OS gate. Conceptual value signal: sharpness and route change. Negative compact-group kappa_4 is not the falsifier; certified 12-only endpoint dominance plus uncontrolled tail is.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the finite post-H,K endpoint gate.`
- Rationale: The branch has reduced the obstruction to incidence-signed endpoint intervals; another abstract OS restatement would not decide whether 12-only dominance can defeat the positive finite margin.
- Situation seed: Heat-kernel SU(N) three-hairpin endpoint-box family with one endpoint box initially 12-only and then leaked into the 13 and 23 footprint channels while the same Wilson loops and source stencil are kept fixed.
- Varied variable: Fractional leakage alpha=b13+b23 from the 12-only endpoint box into the protective channels, with b12 fixed at one.
- Held-fixed controls: Same heat-kernel plaquette-sheet regulator and finite cutoff., Same three Wilson hairpin observables and H,K Feshbach null vector., Same color factor C_N and source step h., No boundary counterterm, gauge fixing observable, or algebra enlargement., Same tail accounting rule T_tail for unresolved endpoint overlap.
- Expected observation: The local dominance changes sign at alpha=1/2 because D=2-4alpha. Below the threshold negative kappa_4 can demote; above it the endpoint becomes protective and cannot be the finite falsifier without a negative tail.
- Transfer certificate needed: A certified source interval for beta_v and a cutoff-uniform T_tail proving that the leakage deformation represents the same regulated Wilson observable family before its intuition enters proof obligations.

## Next Experiment

Compute the actual endpoint-box table b_ij(v), seven-point log Z_v source intervals, M_8 remainder, and T_tail for the heat-kernel SU(N) three-hairpin block; then report the certified [I_-,I_+] sign.

# Endpoint Hessian certificate for the flowed Wilson R++ polarization

## Candidate Lemma

Conditional finite endpoint-Hessian certificate: for the plus-channel H,K endpoint box, the Ward- and cusp-subtracted connected four-curvature contribution to R_{++}^{ren} is bounded by the second endpoint moments of the sheet currents and a C^2_x C^2_y kernel norm. If the resulting lower interval beats the Schur-Feshbach leakage L_+, the finite endpoint-box positivity gate is promoted; no continuum mass-gap claim follows.

## Definitions

- source object: the cutoff SU(N) Yang-Mills Wilson measure with gradient-flow time t>0, two reflected thin hairpin sheets in one endpoint box B_eta, and centered renormalized Wilson observables W_i^{ren}(t,eta).
- target object: the finite reflected-Wilson Schur-Feshbach plus-channel scalar Q_+ after H,K reduction, with leakage L_+=(s+t_0)^2/delta fixed from the finite matrix block.
- controlled interface: the same-theory flowed Wilson cumulant R_{++}^{ren}=kappa_2(W_+^{ren},theta W_+^{ren}) transferred only as an endpoint-box matrix entry in Q_+.
- same-theory condition: the Wilson action, reflection, gradient-flow normalization, endpoint subtractions, and H,K/R block extraction use the same cutoff family before any limiting statement.
- carrier: signed endpoint sheet currents J_+^a(u) with color contraction delta^{ab}, reflection orientation, and certified monopole/dipole cancellations.
- kernel: K_{4,t}^{WS}(u,v) is the Ward-subtracted connected four-curvature boundary-OPE kernel after disconnected product and one-hairpin perimeter/cusp subtractions.

## Assumptions

- Model: four-dimensional Euclidean lattice SU(N) Yang-Mills with Wilson plaquette action, finite volume, reflection plane fixed, and gradient flow at positive time t.
- Regime: endpoint support radius eta is smaller than the collar separation and satisfies eta/sqrt(t)<=rho_0, so flowed kernels are smooth on B_eta x theta B_eta.
- Cutoff: all displayed bounds are at fixed lattice spacing a with a<eta; cutoff-uniform use requires constants independent of a along the chosen flow window.
- Same-theory: the H,K finite matrix entries, the pair baseline, and C_{4,++}^{WS} are computed from the same flowed Wilson family and not imported from another regulator.
- Validity: Ward subtraction removes gauge-longitudinal endpoint pieces and cusp subtraction removes one-hairpin local divergences before the Hessian norm is taken.
- Local: only the endpoint box contribution to the post-H,K R/kappa_4 term is certified; continuum construction, OS reconstruction, nontriviality, and Hamiltonian spectral gap are untouched.

## Equations

- R-decomposition: `R_{++}^{ren}=2(N^2-1)\,G_{++}(t,\eta)+N(N^2-1)\,C_{4,++}^{WS}(t,\eta)+E_{\ge6}(t,\eta)`. Valid when: Valid when the flowed Wilson cumulant expansion is truncated in one endpoint box after disconnected, perimeter, and cusp subtractions.
- Ward-subtracted-polarization: `C_{4,++}^{WS}=\int_{B_\eta}\!du\int_{B_\eta}\!dv\;J_+(u)\,K_{4,t}^{WS}(u,v)\,J_+(v)`. Valid when: Applies when sheet-current representation preserves endpoint orientation and the Ward-subtracted kernel is locally integrable on the endpoint box.
- plus-moment-cancellation: `\int_{B_\eta}J_+(u)\,du=0,\qquad \int_{B_\eta}(u-u_0)_\alpha J_+(u)\,du=0`. Valid when: Valid when the H,K plus-channel endpoint current is the reflected signed hairpin combination with matched endpoint weights.
- Hessian-bound: `|C_{4,++}^{WS}|\le {1\over4}\,M_2(J_+)^2\,H_{4,t}^{WS},\quad H_{4,t}^{WS}:=\sup_{u,v\in B_\eta}\|D_u^2D_v^2K_{4,t}^{WS}(u,v)\|`. Valid when: Requires the Ward-subtracted connected kernel to be twice differentiable in each endpoint variable on the flowed box.
- endpoint-lower-interval: `R_{++}^{ren}\ge 2(N^2-1)G_{++}-{N(N^2-1)\over4}M_2(J_+)^2H_{4,t}^{WS}-|E_{\ge6}|`. Valid when: Valid after color factors are normalized consistently and the higher cumulant remainder has an independent absolute interval bound.
- finite-promotion-test: `2(N^2-1)G_{++}-{N(N^2-1)\over4}M_2(J_+)^2H_{4,t}^{WS}-|E_{\ge6}|>L_+`. Valid when: Promotes only the finite endpoint-box positivity gate when all quantities are same-theory interval enclosures for the H,K block.

## Attempted Derivation

- Attack conceptual pressure: finite Feshbach positivity needs a same-theory endpoint mediator, while pair covariance and flow renormalization are valid but C4 can erase them.
- Replace fragmented raw Wilson contours by endpoint sheet currents J_+; this carrier preserves gauge, color, reflection, orientation, and same-theory invariants while making Ward moments primitive.
- Use disconnected-product removal and one-hairpin perimeter/cusp subtraction to define K_{4,t}^{WS}.
- Use plus-channel monopole and dipole cancellation to annihilate the constant and linear endpoint Taylor terms of K_{4,t}^{WS}.
- Apply the two-variable Taylor remainder to bound C_{4,++}^{WS} by M_2(J_+)^2 H_{4,t}^{WS}/4.
- Insert the color factors: the pair baseline has 2(N^2-1), while the connected four-curvature polarization has N(N^2-1).
- Compare the certified lower bound for R_{++}^{ren} with the finite Schur-Feshbach leakage L_+.

Blocking gap: The missing proof object is a validated interval enclosure of H_{4,t}^{WS} and E_{>=6} for the concrete H,K endpoint geometry, with Ward/cusp subtraction checked at the same cutoff.

## Falsifiers

- Ward-subtracted K_{4,t}^{WS} retains a contact cusp singularity in B_eta, invalidating the Hessian norm.
- The plus-channel current has a residual monopole or dipole moment after discretization, so the Taylor cancellation is false.
- The interval upper bound for H_{4,t}^{WS} is so wide that R_{++}^{ren,lower}<=L_+.
- The higher cumulant remainder E_{>=6} is comparable to the pair baseline in the flow window.
- A regulator-window falsifier: varying a at fixed physical t and eta changes the certified interval instead of forming a plateau.
- A same-theory falsifier: the recovery map from sheet currents to Wilson hairpins changes normalization relative to the H,K block.

## Learning

Declarative tension sharpened: finite Schur-Feshbach positivity, positive flowed pair covariance, and same-theory Wilson renormalization must jointly hold, but the connected four-curvature polarization can erase the pair term. The conceptual value signal is local and route-changing: R_{++}/kappa_4 is now a valid endpoint-moment Hessian certificate rather than a symbolic threshold. Compared with a global non-Gaussian OS witness route, this finite interval route attacks the exact hard gate of endpoint-box positivity after H,K. The efficient representation must encode H,K sheets and endpoint currents, preserve gauge/color/reflection/orientation/same-theory invariants, use cumulant expansion, Ward subtraction, endpoint Taylor expansion, heat-kernel majorants, and interval arithmetic as primitives, quotient only by certified zero-pairing current equivalence, keep locality to finite endpoint cells, transfer through flowed Wilson cumulants, and demote on Ward, cusp, plateau, geometry, cutoff-uniformity, or interval-width falsifier.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and proof-search guide.`
- Rationale: The branch no longer needs another abstract OS/Wilson restatement; the decisive uncertainty is the sign and size of the connected boundary-OPE polarization in one finite endpoint box.
- Situation seed: Finite-volume SU(N) Wilson lattice with gradient-flow time t, two reflected plus-channel thin hairpin endpoint boxes from the concrete H,K collar instance, using sheet-current recovery to centered Wilson observables.
- Varied variable: rho=eta/sqrt(t), the endpoint radius measured in flow units.
- Held-fixed controls: Same Wilson plaquette action, gauge group normalization, reflection plane, and gradient-flow convention., Same H,K finite matrix coefficients and leakage L_+ used in the Schur-Feshbach scalar., Same disconnected-product, perimeter, cusp, and Ward subtractions., Same endpoint orientation and plus-channel current normalization.
- Expected observation: If the endpoint-moment mechanism is real, the ratio |C_{4,++}^{WS}|/G_{++} decreases with rho according to the Hessian certificate while G_{++} has a stable positive plateau; failure gives a direct demotion falsifier.
- Transfer certificate needed: A cutoff-uniform interval proof of moment cancellation, Ward/cusp smoothness, H_{4,t}^{WS} bounds, and E_{>=6} control before the observation may be inserted into Q_+.

## Next Experiment

Proof search: instantiate the concrete H,K endpoint current on a finite cell partition, compute M_2(J_+) exactly, derive sector kernels I_3g,I_4g,I_ct,I_end for K_{4,t}^{WS}, and produce a certified interval for H_{4,t}^{WS} at rho=eta/sqrt(t) in a same-theory Wilson flow window.

# Same-regulator kappa4 shell interval for post-H,K Wilson endpoint positivity

## Candidate Lemma

Finite Route A certificate: in a fixed heat-kernel regulated SU(N) lattice Yang-Mills endpoint box, the Schur-corrected post-H,K endpoint matrix is positive if the Gaussian Wilson contraction margin dominates the connected kappa4 shell row envelope, the OPE remainder, and the H,K Schur energy. This changes only the finite endpoint positivity gate, not the Clay theorem.

## Definitions

- source object: finite-volume four-dimensional lattice SU(N) Yang-Mills with heat-kernel smeared curvature insertions, normalized fundamental Wilson loops, vacuum-subtracted connected endpoint Wilson cumulants, and fixed cutoff data (a,L,sigma,g).
- target object: the finite endpoint-box quadratic form Q_{end,sigma}=R_sigma-S_{HK,sigma} on the worked H,K Wilson collar/hairpin truncation, not the continuum Hamiltonian and not an OS spectral measure.
- controlled interface: the sheet-kernel hypergraph Rec_sigma encoding plaquette sheets, weights, heat-kernel transporters, color tensors, shell labels, multiplicities, OPE error intervals, and the H,K Schur block.
- same-theory condition: every matrix entry uses the same lattice action, gauge group, coupling, smearing kernel, Wilson basis, vacuum subtraction, endpoint boxes, and Schur-Feshbach block; no imported spectral gap or changed regulator is allowed.
- bridge observable: X_i=-(g^2/(4N)):\Phi_i^a\Phi_i^a: is the quadratic transported-curvature part of the normalized Wilson endpoint observable.
- kappa4 carrier: kappa_{4,ij,sigma} is the connected four-curvature cumulant compressed to endpoint sheets after the disconnected vacuum and perimeter terms are removed.
- hard gate: Delta_sigma>0 promotes a finite endpoint-box positivity certificate; a certified nonpositive endpoint eigenvalue is a falsifier for this H,K geometry.

## Assumptions

- Model: finite hypercubic torus, gauge group SU(N), normalized generators tr(T^aT^b)=delta^{ab}/2, and reflection-compatible heat-kernel smearing at scale sigma>=c a.
- Cutoff: a, L, sigma, the H,K endpoint boxes, and the Wilson basis are fixed before any estimate is made; no continuum or infinite-volume uniformity is claimed.
- Regime: the fourth-order boundary Wilson OPE is valid on the chosen endpoint sheets with operator-norm remainder bounded by e_{OPE}(sigma).
- Same-theory: C_sigma, kappa4_sigma, E_{OPE,sigma}, and S_{HK,sigma}=B_sigma^*E_sigma^{-1}B_sigma are computed from the same cutoff measure and the same H,K decomposition.
- Local: the sheet-kernel hypergraph has finite shell radius ell_max inside a volume buffer, so row-sum and interval arithmetic are finite operations.
- Validity: E_sigma=QHQ in the Schur complement is strictly positive on the hairpin complement; otherwise S_{HK,sigma} is not a valid subtraction.

## Equations

- transported endpoint flux: `\Phi_i^a(\sigma)=\int_{\Sigma_i}\omega_i(x)K_\sigma(x)\operatorname{Ad}_{U_{x\to b_i}}^{ab}F_{\mu\nu}^b(x)\,dS_{\mu\nu}(x)`. Valid when: Valid when the endpoint sheet Sigma_i, heat-kernel smearing, transporter path, and basepoint b_i are fixed in one cutoff gauge theory.
- connected boundary polarization cumulant: `R_{ij,\sigma}=\operatorname{Cum}_2\big(X_i(\sigma),X_j(\sigma)\big),\qquad X_i=-(g^2/(4N)):\Phi_i^a\Phi_i^a:`. Valid when: Valid when Wilson observables are vacuum-subtracted and normal ordered so disconnected perimeter and one-point pieces cancel before compression.
- Gaussian plus kappa4 decomposition: `R_{ij,\sigma}=\alpha_N g^4(C_\sigma\circ C_\sigma)_{ij}+\frac{g^4}{16N^2}\kappa_{4,ij,\sigma}+E^{OPE}_{ij,\sigma},\qquad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after fourth-order Wilson OPE expansion in the same heat-kernel regulator and after endpoint compression to the identical Wilson basis.
- kappa4 shell row envelope: `M^{row}_{4,\sigma}=\max_i\sum_{\ell=0}^{\ell_{max}}\sum_{j:\,d_{sh}(i,j)=\ell}|\kappa_{4,ij,\sigma}|,\qquad \|\kappa_{4,\sigma}^{-}\|\le M^{row}_{4,\sigma}`. Valid when: Valid when kappa4_sigma is represented as a finite Hermitian endpoint matrix with shell labels preserving sheet adjacency and multiplicity.
- Schur-corrected endpoint margin: `\lambda_{min}(R_\sigma-S_{HK,\sigma})\ge \Delta_\sigma:=m_G(\sigma)-\frac{g^4}{16N^2}M^{row}_{4,\sigma}-e_{OPE}(\sigma)-s_{HK}(\sigma)`. Valid when: Requires the Gaussian matrix, kappa4 matrix, OPE remainder, and Schur matrix all be compressed to the same endpoint subspace.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Observable Density In The Excitation Sector; source object: finite-volume four-dimensional lattice SU(N) Yang-Mills with heat-kernel smeared curvature insertions, normalized fundamental Wilson loops, vacuum-subtracted connected endpoint Wilson cumulants, and fixed cutoff data (a,L,sigma,g).; target object: the finite endpoint-box quadratic form Q_{end,sigma}=R_sigma-S_{HK,sigma} on the worked H,K Wilson collar/hairpin truncation, not the continuum Hamiltonian and not an OS spectral measure.; Model: finite hypercubic torus, gauge group SU(N), normalized generators tr(T^aT^b)=delta^{ab}/2, and reflection-compatible heat-kernel smearing at scale sigma>=c a..
- Fix a finite heat-kernel lattice regulator, the H,K endpoint Wilson basis, and the Schur block E_sigma=QHQ before estimating R_sigma.
- Expand each normalized endpoint Wilson observable to the quadratic transported-flux term X_i=-(g^2/(4N)):Phi_i^a Phi_i^a: plus a fourth-order OPE remainder.
- Use vacuum subtraction and connected cumulants; this cancels one-point, perimeter, and disconnected products before endpoint compression.
- Evaluate the crossed two-curvature contractions: trace normalization gives alpha_N=(N^2-1)/(8N^2) and the geometric factor is C_sigma circ C_sigma.
- Define kappa4_{ij,sigma} as the remaining connected four-curvature cumulant with the same transporters and sheet weights; do not replace it by a symbolic scalar.
- Compress R_sigma, E_OPE, and the Schur subtraction S_HK=B^*E^{-1}B to the identical finite endpoint subspace.
- Apply Weyl and Gershgorin: lambda_min(R-S_HK) is bounded below by the Gaussian minimum minus the kappa4 negative row envelope, OPE norm, and Schur norm.
- The hard gate is Delta_sigma>0; success promotes a finite endpoint-box theorem, while a certified nonpositive endpoint eigenvalue is a concrete falsifier.

Blocking gap: The missing proof object is the first rigorous same-regulator interval for the connected four-curvature cumulant shell envelope M4_row in the actual H,K endpoint geometry, together with certified e_OPE and exact S_HK.

## Falsifiers

- falsifier: a certified endpoint vector v with v^*(R_sigma-S_HK_sigma)v<=0 in the same cutoff theory demotes the H,K Wilson collar/hairpin route.
- A kappa4 contact-shell interval whose negative row envelope exceeds m_G-e_OPE-s_HK blocks promotion even if the Gaussian color square is PSD.
- A non-invariant sheet quotient that changes a raw connected Wilson contraction invalidates Rec_sigma as a carrier.
- If C_sigma has a null direction matching the endpoint subspace, then the Gaussian margin m_G is zero and kappa4 cannot be dominated by this certificate.
- If the fourth-order Wilson OPE remainder is not bounded in the same heat-kernel regulator, the Delta_sigma inequality is not valid.
- If E_sigma=QHQ is not positive on the hairpin complement, the Schur-Feshbach subtraction S_HK is undefined and the route backtracks.

## Learning

Conceptual pressure attacked: mediate actual connected Wilson cumulants to Schur-corrected endpoint positivity without inflating a finite Wilson calculation into the Clay mass-gap theorem. Declarative tension: Wilson/OPE coefficients, connected kappa4 negativity, OPE errors, and H,K Schur energy must all be valid in one cutoff theory, while continuum OS reconstruction and spectral transfer stay quarantined. The scalar R carrier is too weak and representation-limited; full gauge-invariant OS observable density is too strong and circular for this local gate; raw plaquette enumeration is exact but fragmented. The sheet-kernel hypergraph is the efficient representation because it encodes sheets, weights, transporters, color tensors, shell labels, multiplicities, OPE intervals, and Schur data; preserves gauge invariance, reflection support, Gaussian/kappa4 separation, endpoint compression, and same-theory normalization; supports cumulant contraction, quotient auditing, shell row/operator bounds, interval arithmetic, and Schur subtraction; quotients only by Wilson-invariant trace and sheet symmetries; keeps a finite endpoint-box locality budget; transfers only through Delta_sigma; and has falsifiers by margin failure, nonuniform envelopes, or non-invariant quotienting. Hard gate: Delta_sigma>0 proves only finite endpoint-box positivity, while failure isolates whether kappa4, OPE error, or hairpin coupling kills this route. Conceptual value signal: the move is sharp and explanatory because R becomes a computable connected Wilson cumulant interval with explicit color and geometric factors, not a symbolic threshold.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the first same-regulator kappa4 shell interval.`
- Rationale: The branch has repeated the Delta_sigma architecture; the next learning must come from an actual connected Wilson cumulant shell estimate, not another abstract OS-density or scalar-R restatement.
- Situation seed: Finite four-dimensional heat-kernel SU(N) lattice torus with the worked H,K endpoint box: two collar sheets and one hairpin sheet, vacuum-subtracted normalized Wilson loops, and plaquette-sheet contractions enumerated through contact and nearest-neighbor shells.
- Varied variable: rho=sigma/a, the heat-kernel smearing radius in lattice units.
- Held-fixed controls: Same Wilson or heat-kernel lattice action, gauge group SU(N), coupling g, trace normalization, and finite volume buffer., Same H,K endpoint geometry, endpoint Wilson basis, Schur block E_sigma, and vacuum/perimeter subtraction., Same sheet quotient policy, transporter convention, OPE truncation order, and interval arithmetic rules.
- Expected observation: As rho varies, the PSD Gaussian square should smooth and stabilize, while the connected kappa4 contact-shell envelope either stays below the margin or overwhelms it; the latter is an immediate route demotion signal.
- Transfer certificate needed: A rigorous finite interval table for C_sigma, kappa4 shell sums, e_OPE, and S_HK, plus a quotient-invariance audit showing that the compressed hypergraph recovers the raw same-regulator Wilson cumulants.

## Next Experiment

Build the first same-regulator interval table for the H,K endpoint box: enumerate contact and nearest-neighbor sheet pairs, compute the Gaussian color-square C_sigma circ C_sigma, bound connected kappa4 shell sums, insert e_OPE and S_HK, and report the certified sign of Delta_sigma.

