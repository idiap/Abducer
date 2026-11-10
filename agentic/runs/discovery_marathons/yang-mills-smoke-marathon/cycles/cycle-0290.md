# cycle-0290

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Cycle 290: source-equivalent endpoint interval gate for post-H,K Wilson collapse

## Candidate Lemma

Source-equivalent clipped endpoint coarsening gives a valid finite lower bound for the post-H,K null-channel endpoint contribution. Under nonpositive certified endpoint fourth cumulants, only the adversarial positive part of D=2b12-4b13-4b23 can demote the finite reflected-Wilson OS block.

## Definitions

- source object: a finite heat-kernel plaquette-sheet endpoint data set V_a={v} with same-theory source partition functions Z_v(s), seven-point values log Z_v(rh), cumulant intervals [kappa_v^-,kappa_v^+], fractional incidences b_ij(v), and tail interval T_tail.
- target object: the scalar Schur-Feshbach endpoint gate for the null vector of the already fixed finite three-hairpin reflected-Wilson OS matrix; this is not a continuum existence or mass-gap statement.
- controlled interface: a source-equivalence coarsening pi:V_a->A preserving regulated source derivatives while replacing incidences by outward intervals and exporting only the scalar interval [I_-,I_+] to the finite OS gate.
- same-theory condition: the heat-kernel lattice action, Wilson-loop normalization, reflection map, endpoint sources, and recovery maps are fixed before and after collar collapse; no boundary counterterm, new boundary Hilbert sector, or algebra enlargement is allowed.
- carrier manipulated: C_ep=(Z_alpha(rh),[b_ij^- alpha,b_ij^+ alpha],C_N,M_G,T_tail) with primitive operations source differentiation, interval multiplication, clipping, color multiplication, incidence contraction, and tail addition.

## Assumptions

- Model: four-dimensional SU(N) lattice Yang-Mills with reflection-positive heat-kernel plaquette action and gauge-invariant Wilson loops only.
- Regime: finite cutoff a, finite volume, fixed collar geometry, and endpoint boxes covering exactly the unresolved connected boundary-OPE support after the H,K computation.
- Uniformity: the derivative errors, source-equivalence classes, and tail interval are bounded uniformly over the endpoint boxes used in this finite block.
- Cutoff: the endpoint source stencil is evaluated at fixed h with |h| inside the heat-kernel analyticity radius and with a certified eighth-derivative bound M8.
- Same-theory: every source derivative is obtained by differentiating the original regulated Wilson expectation, not by adding a boundary observable or changing Wilson renormalization at t=0.
- Constraint: the class cumulant certificate satisfies kappa_alpha^+<=0; if this fails, full interval multiplication replaces the clipped shortcut.
- Local: all straight-segment f f contacts have already cancelled by the null-incidence identity, and all nonendpoint connected remainders are charged to T_tail.

## Equations

- seven_point_connected_source_stencil: `\widehat\kappa_\alpha(h)=h^{-4}\sum_{r=-3}^{3}w_r\log Z_\alpha(rh),\quad w=(-1/6,2,-13/2,28/3,-13/2,2,-1/6),\quad |\widehat\kappa_\alpha-\kappa_\alpha|\le 7h^4M_{8,\alpha}/240`. Valid when: Valid when the endpoint source partition function is analytic on the chosen heat-kernel source disk and the eighth derivative is uniformly bounded.
- adversarial_incidence_upper: `D_v=2b_{12}(v)-4b_{13}(v)-4b_{23}(v),\quad D_\alpha^+=2b_{12,\alpha}^+-4b_{13,\alpha}^- -4b_{23,\alpha}^-`. Valid when: Valid when source-equivalent endpoint boxes share the same cumulant data but only incidence intervals are retained after coarsening.
- half_overlap_shield: `b_{13,\alpha}^-+b_{23,\alpha}^-\ge b_{12,\alpha}^+/2\quad\Longrightarrow\quad D_\alpha^+\le0`. Valid when: Applies when the fractional incidence intervals enclose every endpoint footprint assigned to the same source-equivalence class.
- clipped_lower_gate: `I_- = M_G^-+C_N\sum_{\alpha\in A} n_\alpha\,\kappa_\alpha^-\,[D_\alpha^+]_+ + T_{\rm tail}^-`. Valid when: Valid when C_N is positive, kappa_alpha^+ is nonpositive, and protective D_alpha<=0 contributions are discarded conservatively.
- finite_gate_decision: `I_->0\Rightarrow \langle\xi,Q_{\rm postHK}\xi\rangle>0,\qquad I_+<0\Rightarrow \text{finite same\mbox{-}theory falsifier}`. Valid when: Requires the H,K Schur-Feshbach reduction, endpoint source recovery, and tail interval to be valid for the identical Wilson block.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: a finite heat-kernel plaquette-sheet endpoint data set V_a={v} with same-theory source partition functions Z_v(s), seven-point values log Z_v(rh), cumulant intervals [kappa_v^-,kappa_v^+], fractional incidences b_ij(v), and tail interval T_tail.; target object: the scalar Schur-Feshbach endpoint gate for the null vector of the already fixed finite three-hairpin reflected-Wilson OS matrix; this is not a continuum existence or mass-gap statement.; Model: four-dimensional SU(N) lattice Yang-Mills with reflection-positive heat-kernel plaquette action and gauge-invariant Wilson loops only..
- Freeze the Clay claim level: this cycle concerns only a finite regulated reflected-Wilson block after H,K; it does not construct the four-dimensional continuum Yang-Mills theory or prove a mass gap.
- Use the previous H,K computation to isolate the endpoint part of the connected boundary-OPE polarization after Wick-square positivity and straight f f null-incidence cancellation.
- Represent each endpoint box by the same-theory source partition function Z_v(s)=<exp(sX_v)>_HK and recover kappa_v=partial_s^4 log Z_v(0) by the seven-point stencil with eighth-derivative error.
- Coarsen endpoint boxes only when their regulated source data agree; keep incidence data as outward intervals rather than averages.
- Contract the null-channel incidence to D_v=2b12-4b13-4b23 and compute the adversarial class upper D_alpha^+=2b12^+-4b13^- -4b23^-.
- Use kappa_alpha<=0 to discard protective D<=0 contributions and retain only kappa_alpha^- [D_alpha^+]_+ in the lower gate interval.
- Derive the half-overlap shield b13^-+b23^- >= b12^+/2 => D_alpha^+<=0, proving that only certified 12-dominant endpoint classes can be dangerous.
- Transfer the scalar interval [I_-,I_+] to the finite Schur-Feshbach gate: I_->0 promotes this finite block; I_+<0 is a concrete same-theory falsifier.

Blocking gap: The actual endpoint classes still need certified source intervals, fractional incidence intervals for the concrete hairpin geometry, and a cutoff-uniform T_tail. The source recovery also needs a written proof that no endpoint boundary counterterm is introduced.

## Falsifiers

- falsifier: a source-equivalent class with D_alpha^+>0 and C_N n_alpha kappa_alpha^- D_alpha^+ + M_G^+ + T_tail^+ < 0 gives a finite same-theory OS determinant failure.
- falsifier: a nonuniform endpoint tail that grows as a->0 invalidates the finite interval transfer even if every local source stencil is well behaved.
- falsifier: equality of seven source values without equality of the regulated source derivative class hides an endpoint counterexample to coarsening.
- falsifier: a required boundary counterterm at the reflection plane proves the carrier is not same-theory.
- falsifier: if kappa_alpha^+>0 and negative D intervals are present, the clipped nonpositive-kappa shortcut is invalid and must be replaced by full interval multiplication.
- Stress case: averaging D over a mixed 12-only/protective source class can promote falsely; adversarial D_alpha^+ is mandatory for a valid gate.

## Learning

Conceptual pressure attacked: endpoint collapse must be sign-certified in the same Wilson theory after the H,K finite block. Declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must jointly hold without adding a boundary theory; raw R is representation-limited because it hides incidence signs, while raw kappa4 is too strong because negative kappa4 is harmless when the half-overlap shield gives D<=0. Compared with the global Schur-preimage route, C_ep is local after H,K and decision-grade for this finite gate; compared with formal OPE language, it supplies primitive operations and falsifiers. Efficient representation: encode endpoint boxes/classes, seven source values, kappa intervals, fractional b_ij incidences, C_N, M_G, and T_tail; preserve Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; identify equivalents only by regulated source derivatives; keep locality finite through T_tail; export only [I_-,I_+] to the finite OS gate. Hard gate changed: finite post-H,K reflected-Wilson OS transfer. Success promotes this block; failure gives a finite same-theory falsifier. Conceptual value signal: sharpness and route change at finite scope, because certified 12-dominance plus uncontrolled tail is the obstruction, not negative endpoint kappa4 itself.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and interval-sharpness test.`
- Rationale: The branch has already reduced the post-H,K obstruction to endpoint source data; another abstract OS restatement would not change the proof state, while this thought experiment tests whether source-equivalence coarsening can hide a dangerous 12-dominant endpoint.
- Situation seed: A heat-kernel plaquette-sheet three-hairpin endpoint family in which two endpoint boxes have identical seven source values log Z(rh) but different fractional overlaps with hairpin pairs 12,13,23.
- Varied variable: The overlap ratio eta=(b13+b23)/b12 inside one source-equivalence class, varied across the half-overlap threshold eta=1/2 while holding kappa<0 fixed.
- Held-fixed controls: Same SU(N) heat-kernel Wilson action and same reflected three-hairpin geometry outside the endpoint box., Same Feshbach null vector and same H,K Schur-Feshbach reduction., Same source stencil step h, color factor C_N, Wilson normalization, and no boundary counterterm., Same tail budget T_tail and same endpoint-box size in cutoff units.
- Expected observation: For eta>=1/2 the class is shielded since D^+<=0; for eta<1/2 the lower gate decreases linearly like C_N kappa^- b12(2-4eta), exposing exactly when a negative endpoint cumulant can overcome M_G.
- Transfer certificate needed: A formal certificate that source-equivalent boxes really have equal regulated source derivatives, that incidence intervals enclose all endpoint footprints, and that T_tail is cutoff-uniform before the interval may enter the finite OS proof queue.

## Next Experiment

Build the concrete endpoint incidence/source table for the three-hairpin heat-kernel plaquette-sheet regulator: split by regulated source equivalence, compute D_alpha^+, certify kappa_alpha intervals with the seven-point stencil, add C_N and T_tail, and decide the scalar gate [I_-,I_+].

# Endpoint-cell Ward-Hessian constants for the post-H,K R_{++} term

## Candidate Lemma

Conditional finite Route A lemma: for lattice SU(N) Yang-Mills with Wilson action, gradient-flow regulator, and the fixed H,K reflected hairpin endpoint cells, Ward/cusp subtraction and plus-channel monopole/dipole cancellation give a computable near/far lower interval for the connected boundary-OPE polarization R_{++}. If this lower interval exceeds the Schur-Feshbach leakage L_+ plus scheme error, the finite endpoint-box positivity gate passes; otherwise this R repair is demoted. This is not a Clay mass-gap theorem.

## Definitions

- source object: a finite-volume hypercubic lattice SU(N) Yang-Mills measure with Wilson action, lattice spacing a, gradient-flow time t>0, and reflected H,K Wilson hairpin endpoint cells I.
- target object: a finite-dimensional endpoint-box positivity certificate for the post-H,K Schur-Feshbach quadratic form in the plus channel, independent of any continuum spectral claim.
- controlled interface: the same-theory centered flowed Wilson hairpin covariance R_{++}^{a,t}(I), expanded into a positive two-curvature pair contraction and a Ward-subtracted connected four-curvature polarization.
- same-theory condition: the Wilson measure, flow time window, counterterm normalization, H,K matrix entries, leakage L_+, and endpoint currents are all taken along the same cutoff and coupling sequence before any continuum interpretation.
- Regulator: Wilson lattice cutoff plus Yang-Mills gradient flow and endpoint point-splitting at scale eta sqrt(t).
- Carrier: endpoint sheet currents with cell moments M_{0,+}=M_{1,+}=0 and finite M_{2,+}, not raw Wilson contours.
- Cancellation: disconnected product subtraction, one-hairpin perimeter/cusp subtraction, Ward subtraction of longitudinal pieces, and plus-channel reflection moment cancellation.
- Hard gate changed: finite endpoint-box positivity after H,K; untouched gates are continuum construction, OS/Wightman axioms, nontriviality, observable density, large-field/topology summability, and Hamiltonian mass gap.

## Assumptions

- Model: four-dimensional finite-volume hypercubic lattice SU(N) Yang-Mills with Wilson action and gauge-invariant reflected Wilson hairpins.
- Regime: endpoint boxes have diameter eta sqrt(t), cell separation d(I) >= rho sqrt(t), and a^2 << t << d(I)^2 in a fixed finite H,K collar.
- Cutoff: sector Hessian constants c_s^{near}, c_s^{far} are bounded uniformly for sufficiently small a/sqrt(t) and for volumes larger than the endpoint collar.
- Same-theory: the flowed cumulant, counterterms, Feshbach matrices, and leakage L_+ are computed in the same regulated theory and not imported from a different RG basin.
- Local: only finite endpoint cells and finitely many H,K currents are used; the lemma does not construct continuum Schwinger functions.
- Constraint: if the plus-channel endpoint current has a nonzero monopole or dipole after reflection pairing, the Hessian eta^2 estimate is invalid and this lemma demotes.
- Validity: E_6^{a,t} is a certified higher-cumulant remainder in the same flow window, not an assumed small physical correction.

## Equations

- flowed endpoint cumulant: `R_{++}^{a,t}(I)=\kappa_2\left(W_{+}^{a,t}(I)-\langle W_{+}^{a,t}(I)\rangle,\,W_{+}^{a,t}(I)-\langle W_{+}^{a,t}(I)\rangle\right)_{\rm ren}`. Valid when: Valid when the finite cutoff Wilson measure, gradient-flow time t, endpoint cell I, and renormalized one-hairpin subtraction are fixed in the same lattice theory.
- pair plus connected decomposition: `R_{++}^{a,t}=g_t^4(N^2-1)\left(2G_{++}^{a,t}+N C_{4,++}^{\rm WS,a,t}\right)+E_6^{a,t}`. Valid when: Applies after disconnected products, one-hairpin perimeter terms, and cusp counterterms are subtracted before the endpoint Taylor expansion.
- Ward-Hessian polarization bound: `\left|C_{4,++}^{\rm WS,a,t}(I)\right|\le M_{2,+}(I)^2\left(H_{\rm near}^{a,t}(\rho,\eta)+H_{\rm far}^{a,t}(\rho,\eta)\right)`. Valid when: Requires the Ward-subtracted sector kernels have vanishing monopole and dipole endpoint moments on each plus-channel cell.
- near far heat-kernel constants: `H_{\rm near}^{a,t}\le \sum_s c_s^{\rm near}\eta^2\int_{|u|\le\rho}(1+|u|)^6e^{-|u|^2/16}\,du,\quad H_{\rm far}^{a,t}\le \sum_s c_s^{\rm far}e^{-\rho^2/32}`. Valid when: Valid in the heat-kernel scaling window a^2 much smaller than t much smaller than d(I)^2 with sector derivative majorants certified uniformly in the cutoff.
- promotion interval: `R_{++}^{I,-}=g_t^4(N^2-1)\left(2G_{++}^{I,-}-N M_{2,+}(I)^2(H_{\rm near}^{+}+H_{\rm far}^{+})\right)-E_6^{+},\quad R_{++}^{I,-}>L_++\Delta_{\rm sch}`. Valid when: Applies only to the finite H,K endpoint box after the Feshbach leakage L_+ and scheme error Delta_sch are separately enclosed.

## Attempted Derivation

- Attack pressure: finite Schur-Feshbach positivity needs a same-theory Wilson mediator; pair covariance and flow renormalization are valid local inputs but C4 can erase the mediator.
- Use Wilson lattice plus gradient flow and express each H,K hairpin as a flowed sheet-current expansion localized to endpoint cells.
- Center the Wilson variables and subtract disconnected products, one-hairpin perimeter terms, and cusp counterterms; the remaining second cumulant is R_{++}^{a,t}.
- At order g_t^4 the cross-pairing of two flowed curvatures gives the explicit positive term 2g_t^4(N^2-1)G_{++}.
- The connected four-curvature sectors I_{3g}, I_{4g}, I_{ct}, and I_{end} carry color N(N^2-1) and are collected into C_{4,++}^{WS}.
- Ward subtraction removes longitudinal pieces; reflection plus-channel endpoint symmetry cancels monopole and dipole endpoint moments, so the first surviving Taylor term is Hessian-controlled.
- Split the Hessian kernel into |z|<=rho sqrt(t) and |z|>rho sqrt(t); use local heat-kernel derivative majorants for the near part and Gaussian tail for the far part.
- Combine the positive pair baseline, the negative worst-case Hessian bound, and E_6 to form R_{++}^{I,-}; compare with L_+ + Delta_sch.

Blocking gap: The missing proof data are cutoff-uniform numerical or analytic constants c_s^{near}, c_s^{far} for I_{3g}, I_{4g}, I_{ct}, I_{end}, plus a certified E_6 remainder and a cusp-counterterm plateau in the same flow window.

## Falsifiers

- falsifier: Ward subtraction leaves a nonzero monopole or dipole endpoint moment, destroying the eta^2 Hessian suppression.
- falsifier: cusp/perimeter subtraction depends on the endpoint pairing scheme, so R_{++}^{a,t} is not a same-theory renormalized observable.
- falsifier: the certified H_near + H_far bound exceeds 2G_{++}/(N M_{2,+}^2) in every admissible window.
- falsifier: E_6 is not small or not uniformly controlled in the finite flow window.
- falsifier: no plateau in t/a^2 appears before topology or large-field tails dominate the interval.
- Stress case: highly anisotropic endpoint boxes make M_{2,+} large while leaving G_{++} fixed, forcing demotion.
- Failure case: quotienting raw contours by visual isotopy changes a sector pairing and invalidates the endpoint-current carrier.

## Learning

Conceptual pressure attacked: the missing mediator between finite Schur-Feshbach positivity and same-theory Wilson cumulant positivity. Declarative tension: positive pair covariance, gradient-flow renormalization, and endpoint positivity must jointly hold, but the connected four-curvature polarization can erase the pair term unless a cutoff-stable Ward-Hessian interval is valid. Carrier critique: raw Wilson contours are fragmented and representation-limited; global OS or non-Gaussian witness routes are too coarse for this local obstruction. Better abstraction: endpoint sheet currents with zero-pairing quotienting, cell moments, sector kernels, Ward/cusp subtraction, heat-kernel Hessian majorants, interval arithmetic, endpoint locality, and transfer only through flowed Wilson cumulants. Hard gate: finite endpoint-box positivity after H,K; success promotes one finite Route A gate, failure quarantines the R repair. Conceptual value signal: R_{++}/kappa_4 is now a route-deciding color-geometric near/far interval with a valid falsifier, not a symbolic threshold. Clay existence, OS/Wightman axioms, nontrivial continuum limit, observable density, large-field/topology control, and Hamiltonian mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and proof-search calibration, not as evidence for the Clay theorem.`
- Rationale: The branch has a concrete finite inequality but lacks certified near/far constants; varying one endpoint-cell parameter can reveal whether the Ward-Hessian mechanism has a stable sign plateau or is representation-fragile.
- Situation seed: Finite SU(2) and SU(3) Wilson lattice Yang-Mills in a large box with the fixed H,K reflected hairpin endpoint currents, gradient flow at t/a^2 in a certified window, and interval evaluation of R_{++}^{a,t}(I) sector by sector.
- Varied variable: The endpoint-cell diameter eta in units of sqrt(t), with rho chosen by minimizing the certified bound H_near(eta,rho)+H_far(rho).
- Held-fixed controls: Same H,K sheet-current geometry, plus-channel reflection pairing, and Schur-Feshbach leakage L_+., Same Wilson action, coupling sequence, gradient-flow definition, cusp/perimeter subtraction, and endpoint point-splitting rule., Same color normalization tr(T^aT^b)=delta^{ab}/2 and same sector list I_{3g}, I_{4g}, I_{ct}, I_{end}., Finite endpoint collar and finite-volume margin large enough that boundary images do not enter the heat-kernel tail.
- Expected observation: If Ward-Hessian suppression is real, R_{++}^{I,-} should improve like the positive pair baseline minus an O(eta^2) connected penalty and exhibit a nonempty eta plateau beating L_+. If the plateau is absent, the endpoint repair is likely false or too weak.
- Transfer certificate needed: Before intuition affects proof obligations, supply interval-certified sector Hessian constants, verified Ward/cusp cancellations, same-theory counterterm normalization, finite-volume tail bounds, and a cutoff-stable comparison R_{++}^{I,-}>L_+ + Delta_sch.

## Next Experiment

Proof-search task: for the fixed H,K endpoint currents, derive analytic heat-kernel derivative bounds for I_{3g}, I_{4g}, I_{ct}, I_{end}; evaluate rho-optimized intervals for eta in a dyadic grid; audit Ward/cusp cancellations; then report either a certified R_{++}^{I,-}>L_+ + Delta_sch or a demoting falsifier.

# Raw plaquette interval audit for post-H,K Wilson endpoint polarization

## Candidate Lemma

If the same-regulator raw plaquette intervals for the connected boundary-OPE polarization satisfy Delta_raw>0, then the finite post-H,K endpoint Wilson quadratic form is positive on the chosen P-sector. This changes only the finite Route A endpoint-box gate; OS/Wightman reconstruction, continuum nontriviality, observable density, and Hamiltonian mass gap remain untouched.

## Definitions

- source object: finite heat-kernel regulated SU(N) lattice Yang-Mills measure on a fixed reflected box, with transported smeared plaquette variables in the two endpoint Wilson boxes after the H,K collar/hairpin choice.
- target object: finite endpoint-box Schur-corrected Wilson quadratic form on the post-H,K P-sector; it is an algebraic positivity target, not a continuum Hilbert-space spectral gap.
- controlled interface: Rec_raw maps raw transported plaquette covariance and four-cumulant interval data to the matrix R_raw and then to the margin Delta_raw after subtracting the H,K Schur energy and OPE error.
- same-theory condition: the measure, lattice spacing, volume, coupling, heat-kernel scale, Wilson basis, normal ordering, reflection plane, H,K blocks, and Schur subtraction are identical in every term.

## Assumptions

- Model: SU(N) heat-kernel lattice Yang-Mills on a finite reflection-positive hypercubic box, with fixed a,L,beta_R and compact gauge group integration.
- Cutoff: the endpoint boxes contain finitely many oriented plaquettes, the smearing scale sigma satisfies sigma>=c a, and no continuum or infinite-volume limit is taken.
- Same-theory: the raw plaquette cumulants, Wilson OPE coefficients, OPE remainder, and H,K Schur blocks are evaluated in the same cutoff theory and the same Wilson normalization.
- Local: the Q-block energy E_HK is strictly positive on the finite eliminated hairpin subspace, so B_HK^* E_HK^{-1} B_HK is a valid finite Schur subtraction.
- Validity: the plaquette OPE through order g_R^4 has an explicit interval remainder e_OPE for this endpoint geometry and regulator.
- Constraint: no shell A012 quotient is used; every plaquette quadruple interval is kept raw except for exact Wilson trace identities and orientation reversal identities.

## Equations

- transported endpoint flux coordinate: `\Phi_i^a=\sum_{p\in S_i} w_{i,p}\,\tau_{p\to b_i}\big(\log U_p^{(\sigma)}\big)^a`. Valid when: Valid when the endpoint sheet S_i, basepoint b_i, weights, orientations, and heat-kernel plaquette logarithms are fixed in the finite cutoff model.
- raw connected polarization: `R_{ij}^{\mathrm{raw}}=\operatorname{cum}_2\left(:\Phi_i^a\Phi_i^a:,:\Phi_j^b\Phi_j^b:\right)`. Valid when: Applies after same-theory vacuum and perimeter normal ordering removes disconnected Wilson factors in the reflected endpoint boxes.
- Gaussian plus connected four-curvature decomposition: `R_{ij}^{\mathrm{raw}}=\alpha_N g_R^4\,(C_{\sigma}\odot C_{\sigma})_{ij}+\frac{g_R^4}{16N^2}K^{(4)}_{ij}+E^{\mathrm{OPE}}_{ij},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Requires the heat-kernel Wilson OPE, transported color contraction with generators normalized by tr(T^aT^b)=delta^{ab}/2, and finite endpoint compression.
- raw four-cumulant row envelope: `\lambda_{\min}(K^{(4)})\ge -\Gamma_{\mathrm{raw}},\quad \Gamma_{\mathrm{raw}}=\max_i\sum_j |K^{(4)}_{ij}|`. Valid when: Valid when outward-rounded intervals enclose every color-contracted plaquette four-cumulant entering K^{(4)} before any non-exact quotienting.
- same-basis Schur hairpin energy: `s_{HK}=\left\|B_{HK}^*E_{HK}^{-1}B_{HK}\right\|_{P\to P}`. Valid when: Applies after the H,K finite Gram block is decomposed into P and Q sectors with E_HK positive on Q.
- finite endpoint promotion margin: `\Delta_{\mathrm{raw}}=m_G-\frac{g_R^4}{16N^2}\Gamma_{\mathrm{raw}}-e_{\mathrm{OPE}}-s_{HK},\quad m_G=\lambda_{\min}\big(\alpha_N g_R^4(C_{\sigma}\odot C_{\sigma})\big)`. Valid when: Valid for the fixed endpoint Wilson basis when Gaussian, kappa_4, OPE, and Schur terms share one regulator and normalization.

## Attempted Derivation

- Freeze claim level: prove only a finite endpoint-box Schur positivity certificate, not Yang-Mills existence, OS reconstruction, observable density, or a mass gap.
- Represent each endpoint Wilson sheet by transported heat-kernel plaquette logarithms Phi_i^a with fixed weights, orientations, and basepoints.
- Use same-theory normal ordering so vacuum and perimeter disconnected Wilson factors cancel before forming cum_2(:Phi_i^2:,:Phi_j^2:).
- Expand the finite Wilson OPE through order g_R^4. The crossed two-curvature contractions give alpha_N g_R^4(C_sigma odot C_sigma), a positive semidefinite Hadamard-square matrix with alpha_N=(N^2-1)/(8N^2).
- Place every connected four-curvature plaquette cumulant into raw outward-rounded intervals I_{pqrs}^{abcd}; after color and weight contraction these give K^{(4)}.
- Use Gershgorin or interval operator norm to certify lambda_min(K^{(4)})>=-Gamma_raw without assuming symbolic shell amplitudes.
- Subtract the same-basis Schur hairpin energy s_HK=||B_HK^*E_HK^{-1}B_HK|| and the OPE interval e_OPE from the Gaussian lower edge m_G.
- Conclude finite endpoint positivity if Delta_raw>0; otherwise record a route falsifier rather than weakening the Clay target.

Blocking gap: No same-regulator raw interval table I_{pqrs}^{abcd} and no audited e_OPE are presently available for the first H,K endpoint geometry, so the sign of Delta_raw is not yet decided.

## Falsifiers

- falsifier: the raw row envelope Gamma_raw makes Delta_raw<=0 even with the positive Gaussian color square.
- falsifier: an interval for K^{(4)} changes under allowed basepoint, orientation, or reflection recoding, showing the carrier is not Wilson-invariant.
- falsifier: e_OPE is comparable to or larger than m_G-s_HK in the fixed endpoint geometry.
- falsifier: E_HK has a small eigenvalue that makes the Schur subtraction dominate the endpoint matrix.
- falsifier: heat-kernel smearing or normal ordering used for the cumulant is not the same as the one used for H,K and the Wilson OPE.

## Learning

Conceptual pressure attacked: replace symbolic boundary polarization by an actual same-regulator raw plaquette interval certificate. Declarative tension: Wilson/OPE coefficients, connected kappa_4 negativity, OPE error, and H,K Schur energy must jointly hold in one cutoff theory, but Clay-level continuum and spectral claims must remain non-claims. Carrier critique: scalar R is representation-limited, OS observable density is too strong and circular here, shell A012 is convenient but now quarantined, and raw plaquette enumeration is fragmented yet valid. Efficient representation requirements: encode oriented plaquettes, sheet weights, heat-kernel transporters, color indices, cumulant intervals, OPE intervals, and Schur data; preserve gauge invariance, reflection support, locality, Gaussian/kappa_4 separation, endpoint compression, and same-theory normalization; support cumulant contraction, interval summation, row/operator bounds, and Schur subtraction; quotient only by exact Wilson identities; keep finite endpoint complexity; transfer only through Delta_raw; demote on margin failure or non-invariant intervals. Conceptual value signal: the move is sharp and route-changing at finite scope because a positive or negative Delta_raw decides the worked H,K endpoint route without pretending to solve the Clay problem.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the first raw plaquette interval proof search.`
- Rationale: The branch has already quarantined symbolic A012 shells; another abstraction restatement would not decide whether the finite H,K endpoint route survives. A concrete same-regulator raw interval experiment can expose whether kappa_4 or Schur energy kills the route.
- Situation seed: Finite SU(3) heat-kernel lattice on a reflected 8^4 box with the fixed H,K collar/hairpin endpoint geometry, transported plaquette logarithms in the two endpoint boxes, and outward-rounded cumulant intervals computed directly from the lattice measure or a rigorous cluster/strong-coupling enclosure.
- Varied variable: The single varied parameter is the smearing ratio rho=sigma/a over a small grid rho in {1,2,3,4}.
- Held-fixed controls: Gauge group SU(3), endpoint Wilson basis, H,K collar/hairpin geometry, and reflection plane are fixed., The bare lattice action, finite volume, coupling beta_R, normal-ordering convention, plaquette transport paths, and Schur block decomposition are held fixed., No shell quotient or OS spectral-transfer hypothesis is introduced during the experiment.
- Expected observation: If the route is viable, m_G(rho) should remain separated from s_HK+g_R^4 Gamma_raw(rho)/(16N^2)+e_OPE(rho) for at least one rho. If every rho gives nonpositive margin, the finite endpoint route is demoted.
- Transfer certificate needed: A rigorous outward-rounded interval table for all raw color-contracted plaquette four-cumulants, an OPE remainder in the same heat-kernel regulator, and an audited Schur energy in the identical Wilson basis.

## Next Experiment

Build the first raw interval ledger for the smallest H,K endpoint box: list oriented plaquette quadruples, compute color-contracted I_{pqrs}^{abcd}, assemble K^{(4)}, bound Gamma_raw, compute m_G, e_OPE, s_HK, and report the interval sign of Delta_raw.

