# cycle-0283

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: fractional endpoint dominance gate

## Candidate Lemma

Fractional endpoint-dominance compression lemma. For the fixed three-hairpin post-H,K Wilson block, the dangerous connected endpoint R term is bounded below by a clipped 12-dominance loss. Negative endpoint kappa4 is a falsifier only through positive e_v=b12(v)-2b13(v)-2b23(v) plus tail.

## Definitions

- source object: C_ep(a,L,h) is the heat-kernel plaquette-sheet endpoint source carrier for the fixed three-hairpin Wilson block, consisting of endpoint boxes v, seven log Z_v(sh) values, beta intervals for -d_s^4 log Z_v|0, fractional incidences b_ij(v), color factor C_N, Gaussian margin M_G, and tail bound tau.
- target object: a finite post-H,K Schur-Feshbach scalar interval [I_-,I_+] deciding this reflected-Wilson block before any continuum OS spectral-transfer claim.
- controlled interface: source differentiation plus incidence contraction sends C_ep to I_-=M_G-2 C_N sum_v beta_v^+ [b12(v)-2b13(v)-2b23(v)]_+ - tau, with protective terms discarded.
- same-theory condition: every log Z_v source is inserted in the original regulated Wilson expectation with fixed normalization, no boundary counterterm, no changed observable algebra, and cutoff-uniform tail bookkeeping.
- endpoint dominance e_v=b12(v)-2b13(v)-2b23(v); positive e_v means the endpoint box is more 12-dominated than half-overlapped by 13 and 23.
- beta_v is the certified magnitude interval for the negative singlet connected fourth endpoint cumulant, kappa_v in [-beta_v^+,-beta_v^-].
- C_N=(g_a^4/4)(T_F/N)^2 c_4^{sing}(N) is the positive color-source prefactor after singlet projection.

## Assumptions

- Model: finite-volume SU(N) lattice Yang-Mills with heat-kernel plaquette-sheet Wilson regulator and the already fixed reflected three-hairpin H,K block.
- Regime: endpoint boxes are smaller than the collar scale but contain the corner support of the boundary OPE source.
- Cutoff: beta_v^+, b_ij(v), M_G, and tau are certified uniformly along the cutoff sequence used for this finite block.
- Same-theory: source derivatives are computed in the same regulated Wilson measure and not in an auxiliary boundary theory.
- Validity: Wick-square disconnected terms have been separated as positive Gram terms, and straight C_A f f contacts obey the null-incidence cancellation.
- Local: all endpoint interactions not assigned to boxes v are charged to T_tail with |T_tail|<=tau.
- Constraint: fractional incidences satisfy 0<=b_ij(v)<=1 and are measured by the same plaquette-sheet contraction defining the Wilson observables.

## Equations

- seven_point_endpoint_kappa4: `\kappa_v=\partial_s^4\log Z_v(0)=\frac{-L_v(-3h)+12L_v(-2h)-39L_v(-h)+56L_v(0)-39L_v(h)+12L_v(2h)-L_v(3h)}{6h^4}+E_{8,v},\quad |E_{8,v}|\le \frac{7h^4}{240}M_{8,v}`. Valid when: Valid when the heat-kernel endpoint partition function is C^8 in the source on the certified interval.
- fractional_null_incidence: `D_v=2b_{12}(v)-4b_{13}(v)-4b_{23}(v)=2e_v,\quad e_v=b_{12}(v)-2b_{13}(v)-2b_{23}(v)`. Valid when: Applies after the H,K Feshbach reduction, with fractional endpoint incidences defined from the same regulated Wilson sheets.
- endpoint_R_decomposition: `R_{\mathrm{end}}=C_N\sum_v \kappa_v D_v+T_{\mathrm{tail}},\quad |T_{\mathrm{tail}}|\le \tau`. Valid when: Requires the connected-log endpoint decomposition, the null-incidence cancellation of straight f f contacts, and the uniform endpoint tail bound.
- clipped_lower_bound: `M_G+R_{\mathrm{end}}\ge I_-:=M_G-2C_N\sum_v \beta_v^+[e_v]_+-\tau`. Valid when: Valid when each kappa_v lies in a certified negative interval and protective negative-dominance boxes are deliberately discarded.
- finite_gate_promotion: `I_->0\quad\Longrightarrow\quad \text{the finite post-H,K reflected-Wilson scalar gate is positive}`. Valid when: Promotes only the finite post-H,K block when this lower interval is strictly positive.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: C_ep(a,L,h) is the heat-kernel plaquette-sheet endpoint source carrier for the fixed three-hairpin Wilson block, consisting of endpoint boxes v, seven log Z_v(sh) values, beta intervals for -d_s^4 log Z_v|0, fractional incidences b_ij(v), color factor C_N, Gaussian margin M_G, and tail bound tau.; target object: a finite post-H,K Schur-Feshbach scalar interval [I_-,I_+] deciding this reflected-Wilson block before any continuum OS spectral-transfer claim.; Model: finite-volume SU(N) lattice Yang-Mills with heat-kernel plaquette-sheet Wilson regulator and the already fixed reflected three-hairpin H,K block..
- Conceptual pressure attacked: endpoint collapse must be sign-certified in the same Wilson theory, not by adding a boundary algebra or restating closed-cone positivity.
- Declarative tension: finite collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must jointly hold; raw R is too weak because it forgets incidence signs, while raw kappa4 is too strong because it ignores the null-channel contraction.
- Work at finite a,L in the heat-kernel plaquette-sheet regulator and keep the three-hairpin H,K block fixed; this freezes the Clay claim level to a finite Route A calculation.
- Represent each endpoint box by L_v(mh)=log Z_v(mh), m=-3,...,3, and use the seven-point fourth derivative to certify kappa_v with an eighth-derivative error.
- Use the connected log to isolate the irreducible endpoint four-flux cumulant; Wick-square contractions remain positive Gram terms and are not part of the dangerous R loss.
- Use the previously checked null-incidence identity to cancel straight C_A f f contacts, leaving only endpoint boxes and T_tail.
- Contract the remaining endpoint term with the Feshbach null weights, obtaining D_v=2b12-4b13-4b23=2e_v.
- Assuming kappa_v in [-beta_v^+,-beta_v^-], bound the worst negative contribution by discarding protective e_v<=0 boxes and keeping only 2C_N beta_v^+[e_v]_+.
- The hard gate changed is the finite post-H,K reflected-Wilson OS transfer gate: I_->0 promotes this finite block; I_+<0 or nonuniform tails give a concrete same-theory falsifier.
- Conceptual value signal: the result is sharp at finite scope because it identifies half-overlap as the sign threshold and shows why negative compact-group kappa4 alone is not the obstruction.

Blocking gap: Actual fractional incidences b_ij(v), source-derived beta_v intervals, and a cutoff-uniform T_tail bound have not yet been computed for the physical endpoint geometry.

## Falsifiers

- falsifier: a certified 12-dominated endpoint family with 2C_N sum_v beta_v^+[e_v]_+ + tau >= M_G demotes the finite post-H,K block.
- falsifier: the seven-point source stencil is not cutoff-uniform, so beta_v cannot be used in a valid same-theory interval.
- falsifier: endpoint collapse requires a boundary counterterm or altered Wilson normalization, breaking the same-theory condition.
- falsifier: corner orientation spoils the straight f f null-incidence cancellation and adds an uncontrolled negative contact.
- falsifier: T_tail scales with the cutoff or volume faster than the reserved margin, so the local endpoint carrier is not a valid transfer interface.
- Stress case: b12=1, b13=b23=0 at many boxes is maximally dangerous; half-overlap b13+b23>=b12/2 is the protective opposite case.

## Learning

Cycle 283 attacks the conceptual pressure of endpoint collapse in the same Wilson theory. The declarative tension is collar OS positivity plus fixed gauge-invariant Wilson observables plus singular connected endpoint OPE, with no permission to introduce a boundary theory. Raw R is representation-limited and raw kappa4 is too strong; the efficient carrier is C_ep with endpoint boxes, seven source values, beta intervals, fractional b_ij incidences, C_N, M_G, and tau. It preserves Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; its primitive operations are source differentiation, interval arithmetic, color multiplication, clipping, incidence contraction, and tail addition; equivalence is by regulated source data only; locality cost is charged to tau; transfer exports only [I_-,I_+]. Compared with the global Schur-preimage route, this is local after H,K and sharper for this finite gate. The hard gate changed is the finite post-H,K reflected-Wilson OS transfer gate. The conceptual value signal is sharpness: negative compact-group kappa4 is not the falsifier; positive fractional 12-dominance below half-overlap plus uncontrolled tail is. Clay continuum construction, nontriviality, full OS/Wightman reconstruction, and mass gap remain explicitly non-claimed.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the finite post-H,K endpoint gate.`
- Rationale: The branch has reduced R to fractional endpoint dominance; varying the overlap fraction tests whether the carrier is decision-grade rather than another abstract OS restatement.
- Situation seed: Heat-kernel SU(N) plaquette-sheet three-hairpin endpoint box with fixed source stencil and fixed negative kappa4 interval, but with fractional endpoint overlaps interpolating between 12-only and evenly shared 12/13/23 footprints.
- Varied variable: alpha=(b13+b23)/b12, the fractional half-overlap ratio at endpoint boxes with b12>0.
- Held-fixed controls: same regulated Wilson observables and reflection map, same H,K Feshbach block and null vector, same color factor C_N and Gaussian margin M_G, same seven-point source stencil and eighth-derivative error policy, no boundary counterterm and no change of gauge-invariant test algebra
- Expected observation: The endpoint contribution is dangerous for alpha<1/2 and protective for alpha>=1/2 up to tail; the quantitative flip is I_-=M_G-2C_N sum beta_v^+ b12(v)[1-2alpha_v]_+-tau.
- Transfer certificate needed: A cutoff-uniform endpoint incidence table and source-derivative beta intervals proving that the imagined alpha sweep is realized by actual same-theory Wilson plaquette sheets before it may affect the proof queue.

## Next Experiment

Compute the actual fractional b12,b13,b23 endpoint table for the three hairpin plaquette sheets; then evaluate seven heat-kernel source values for each nonzero endpoint box, form beta_v intervals, and report I_-=M_G-2C_N sum beta_v^+[b12-2b13-2b23]_+-tau.

# Gauge-invariant endpoint Wilson cumulant: Ward-Hessian interval certificate

## Candidate Lemma

Conditional finite endpoint Ward-Hessian certificate: for the H,K plus-channel endpoint box, Ward/cusp subtraction and plus-current monopole/dipole cancellation convert the connected boundary-OPE polarization into a Hessian-controlled lower interval for R_{++}. If this lower interval beats the Schur-Feshbach leakage, the finite Route A endpoint-box gate is promoted; no continuum YM or mass-gap claim follows.

## Definitions

- source object: centered flowed SU(N) Wilson hairpin endpoint observables W_{+,I}^{ren}(t,a) in a Wilson lattice regulator with gradient-flow time t and endpoint box I.
- target object: the finite Route A plus-channel Schur-Feshbach endpoint quadratic form Q_{+,I}^{ren}=A_{+,I}+R_{++,I}^{ren}-L_{+,I}.
- controlled interface: an endpoint sheet-current carrier J_{+,I} with recovery map Rec(J_{+,I})=W_{+,I}^{ren} modulo certified zero-pairing currents.
- same-theory condition: the Wilson action, flow, counterterms, H,K sheets, Feshbach blocks, and reflected cumulants are all computed in the same cutoff sequence before any continuum interpretation.
- bridge observable: the reflected connected cumulant R_{++,I}^{ren}=kappa_2(W_{+,I}^{ren},theta W_{+,I}^{ren})_c after disconnected-product, perimeter, and cusp cancellation.
- representation morphism: Phi sends oriented H,K Wilson collars and hairpins to sheet currents with endpoint currents; it preserves gauge invariance, color trace normalization, reflection parity, and orientation signs.
- error budget: G_{++}^{I,-} is the pair-contraction lower interval, H_4^{I,+} is the Ward-subtracted four-curvature Hessian upper interval, M_{2,+}^{I,+} is the endpoint second-moment upper interval, and E_6^{I,+} is the sixth-order/remainder upper interval.

## Assumptions

- Model: four-dimensional Euclidean SU(N) Yang-Mills with Wilson lattice regulator at spacing a, gradient flow time t>0, and gauge-invariant Wilson-loop observables only.
- Regime: endpoint box side ell=eta sqrt(8t) with 0<eta<eta0, point splitting epsilon<<ell, and a<<epsilon so flowed curvature contractions are smooth on endpoint cells.
- Cutoff: all intervals are uniform for a/sqrt(t)<=delta_a inside the tested regulator window; outside that window the certificate is only finite-cutoff evidence.
- Same-theory: the reflected cumulant, counterterms, H,K Feshbach matrix, and leakage L_{+,I} are evaluated in one Wilson ensemble and one normalization convention.
- Local: the claim concerns one finite endpoint box I and the plus channel after H,K reduction; it does not assert OS reconstruction, observable density, continuum nontriviality, or a Hamiltonian spectral gap.
- Validity: Ward/cusp subtraction leaves a conserved endpoint current and the plus combination has zero monopole and dipole moments in I; if either moment remains, the Hessian bound is invalid.

## Equations

- flowed endpoint cumulant: `R_{++,I}^{ren}(t,a)=\kappa_2\big(W_{+,I}^{ren}(t,a),\theta W_{+,I}^{ren}(t,a)\big)_c`. Valid when: Valid when the Wilson hairpins are centered, reflected, flowed, and renormalized in the same cutoff ensemble.
- plus moment cancellation: `\int_I J_{+,I}(x)\,dx=0,\qquad \int_I (x-z_I)_\alpha J_{+,I}(x)\,dx=0,\qquad M_{2,+}^{I}=\int_I |x-z_I|^2 |J_{+,I}(x)|\,dx`. Valid when: Valid when Ward subtraction, cusp subtraction, and H,K plus-channel orientation symmetries are all certified on the endpoint cell.
- color-geometric R decomposition: `R_{++,I}^{ren}=g_t^4 (N^2-1)\big(2G_{++,I}+N\Xi_{++,I}\big)+E_{6,I}`. Valid when: Applies after fourth-order flowed Wilson expansion, color trace normalization, disconnected-product cancellation, and collection of higher terms into E_6.
- Ward-Hessian polarization bound: `|\Xi_{++,I}^{WS}|\le H_4^{I,+}\,(M_{2,+}^{I,+})^2`. Valid when: Valid when the Ward-subtracted connected four-curvature kernel has an interval Hessian bound on the whole endpoint box.
- certified lower interval: `R_{++,I}^{-}=g_t^4 (N^2-1)\big(2G_{++,I}^{-}-N H_4^{I,+}(M_{2,+}^{I,+})^2\big)-E_{6,I}^{+}`. Valid when: Valid when the pair lower interval, Hessian upper interval, moment upper interval, and remainder upper interval share one regulator window.
- finite endpoint promotion inequality: `A_{+,I}+R_{++,I}^{-}-L_{+,I}>0\ \Longrightarrow\ Q_{+,I}^{ren}>0`. Valid when: Valid when the Schur-Feshbach leakage L_+ and endpoint cumulant intervals are computed for the identical H,K finite reduction.

## Attempted Derivation

- Conceptual pressure attacked: finite Schur-Feshbach positivity, positive flowed pair covariance, and same-theory Wilson renormalization must jointly hold, but the connected four-curvature polarization can erase the endpoint mediator.
- Replace raw Wilson contours by endpoint sheet currents J_{+,I}; raw contours are representation-limited because Ward moments, color factors, and endpoint locality are hidden in contour parametrizations.
- Compare routes: a global non-Gaussian OS witness is too coarse for this finite obstruction, while endpoint-current interval calculus targets exactly the R_{++}/kappa_4 gate.
- Expand the centered flowed Wilson hairpin cumulant to fourth order; disconnected products and one-hairpin perimeter/cusp pieces cancel before the reflected covariance is formed.
- The Gaussian pair contraction gives the explicit positive term 2g_t^4(N^2-1)G_{++,I}; this is the part protected by reflection and color trace positivity.
- The connected four-curvature sector has color factor N(N^2-1) after f^{abc}f^{abc} contraction and is collected as g_t^4N(N^2-1)Xi_{++,I}.
- Ward subtraction makes the sector kernel divergence-free at endpoints; the H,K plus combination cancels monopole and dipole moments of J_{+,I}.
- Taylor expand the Ward-subtracted kernel around the endpoint center z_I; constant and linear terms vanish against the moments, leaving a Hessian term bounded by H_4^{I,+}(M_{2,+}^{I,+})^2.
- Insert the resulting lower interval into Q_{+,I}^{ren}=A_{+,I}+R_{++,I}^{ren}-L_{+,I}; positivity of A+R^- - L promotes only the finite endpoint-box gate.
- Efficient representation requirements: encode H,K sheets, endpoint currents, cell moments, sector kernels, and counterterms; preserve gauge, color, reflection, orientation, cutoff, and same-theory invariants; use cumulant expansion, Ward/cusp subtraction, endpoint Taylor expansion, heat-kernel majorants, and interval arithmetic as primitives; quotient only by certified zero-pairing currents; keep locality to finite endpoint cells; transfer through flowed Wilson cumulants; expose Ward, cusp, plateau, geometry, cutoff-uniformity, and interval-width falsifiers.

Blocking gap: The missing mediator is a certified interval evaluation of H_4^{I,+}, G_{++,I}^{-}, and E_{6,I}^{+} in one regulator window with Ward residuals rounded outward. Without that, the lower interval is a valid formula but not yet a numerical or analytic certificate.

## Falsifiers

- falsifier: the Ward-subtracted endpoint current has a nonzero monopole or dipole interval, so the C4 term is not Hessian-suppressed.
- falsifier: the cusp or perimeter subtraction depends on the chosen recovery map, breaking the same-theory condition.
- falsifier: H_4^{I,+}(M_{2,+}^{I,+})^2 is large enough that 2G_{++,I}^{-}-N H_4^{I,+}(M_{2,+}^{I,+})^2<=0.
- falsifier: the lower interval beats leakage at one cutoff but changes sign under a/sqrt(t), epsilon, or cell refinement.
- falsifier: the positive pair baseline vanishes for the actual H,K endpoint geometry, leaving no mediator to rescue the finite Schur-Feshbach gate.
- falsifier: the sixth-order remainder E_6^{I,+} is of the same size as the pair baseline in the tested flow window.

## Learning

The conceptual value signal is local but sharp: R_{++}/kappa_4 is now a same-theory flowed Wilson cumulant with a finite color-geometric lower interval, not a symbolic threshold. The hard gate is finite endpoint-box positivity after H,K; success promotes that single Route A gate, failure quarantines the R repair. The Clay gates of continuum existence, OS/Wightman axioms, nontriviality, observable density, large-field/topology control, and Hamiltonian mass gap remain untouched. The declarative tension is explicit: positive pair covariance and flow renormalization are valid but insufficient unless the connected four-curvature polarization is bounded in the same theory.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and quadrature design for the finite endpoint-box certificate.`
- Rationale: The branch no longer needs another OS/Wilson restatement; the decisive local question is whether moment cancellation really makes the connected boundary-OPE polarization smaller than the positive pair term in the same finite Wilson theory.
- Situation seed: Flowed SU(2) and SU(3) Wilson lattice endpoint box for the concrete H,K plus hairpin/collar geometry, with sheet currents recovered from the same reflected Wilson observables and outward-rounded interval kernels.
- Varied variable: eta=ell/sqrt(8t), the dimensionless endpoint-box size controlling second moments and Hessian suppression.
- Held-fixed controls: Wilson action family, gauge group N, reflection plane, and H,K endpoint geometry are fixed., Gradient-flow scheme, point-splitting hierarchy a<<epsilon<<ell, and counterterm prescription are fixed., Schur-Feshbach leakage L_{+,I}, color normalization, and plus-channel current orientation are fixed., Recovery map Rec from endpoint sheet currents to centered Wilson hairpins is fixed.
- Expected observation: As eta decreases inside a regulator plateau, G_{++,I}^{-} remains positive while the Ward-Hessian penalty scales down relative to it; promotion needs A_{+,I}+R_{++,I}^{-}-L_{+,I}>0 for both SU(2) and SU(3), while a sign change is a branch-demoting observation.
- Transfer certificate needed: A same-theory certificate containing Ward/cusp residual intervals, cellwise H_4 and G intervals, an E_6 majorant, and a plateau bound uniform over the tested a/sqrt(t), epsilon, and partition refinements before the intuition may affect proof obligations.

## Next Experiment

Build the concrete H,K endpoint sheet-current table, choose eta in {1/4,1/6,1/8}, and interval-enclose G_{++,I}^{-}, H_4^{I,+}, Ward residuals, E_6^{I,+}, and A_+ + R^- - L_+ for SU(2) first, then SU(3), using the same flowed Wilson regulator window.

# Gauge-Invariant Observable Density In The Excitation Sector -- finite post-HK A012 shell audit

## Candidate Lemma

Finite Route A certificate: for a fixed reflected Wilson endpoint box after the H,K Schur-Feshbach reduction, the post-H,K endpoint form is bounded below by Delta_sigma. If Delta_sigma>0, the worked endpoint box is positive in this cutoff theory; if Delta_sigma<=0 or the interval is undecidable, this geometry is demoted. This does not prove OS reconstruction, continuum existence, observable density, or the Clay mass gap.

## Definitions

- source object: finite-volume four-dimensional lattice SU(N) Yang-Mills with heat-kernel plaquette regulator, spacing a, smoothing scale sigma, reflected Wilson collar/hairpin endpoint sheets, and connected cumulants of heat-kernel transported curvature fluxes.
- target object: the normalized finite endpoint quadratic form on Wilson sheet coefficients after H,K elimination, viewed as a Hermitian matrix lower-bound problem on the post-Schur endpoint subspace.
- controlled interface: the sheet-kernel hypergraph recovery map u -> X_u^sigma and endpoint compression P_E send Wilson boundary-OPE data to R_sigma while keeping Gaussian, connected kappa4, OPE-error, and Schur-subtraction terms separate.
- same-theory condition: every term uses the same lattice, volume, coupling g_R, heat-kernel smoothing sigma, Wilson basis, reflection plane, diagonal normalization, and H,K Schur block; no imported continuum spectral theorem is used.
- carrier: sheet nodes u encode oriented plaquette sheets with weights, transport paths, color tensors, shell labels, OPE intervals, and their H,K incidence data.
- hard gate: Delta_sigma>0 promotes only finite endpoint-box positivity; Delta_sigma<=0 is a falsifier for this Wilson collar/hairpin route.

## Assumptions

- Model: pure SU(N) lattice Yang-Mills on a finite box or torus with the heat-kernel action and gauge-invariant Wilson loop observables only.
- Regime: sigma>=a and the endpoint box diameter is finite, so all sheet sums and Schur blocks are finite matrices.
- Cutoff: the heat-kernel curvature field F_sigma is defined by plaquette logarithms or equivalent local heat-kernel smearing with a fixed branch inside the regulated OPE chart.
- Same-theory: R_sigma, the OPE error, and S_HK are computed before changing regulator, coupling, basis, volume, or reflection plane.
- Local: only the first three shell classes ell=0,1,2 and a separately bounded tail T_ge3 enter this cycle.
- Validity: the statement is a finite matrix theorem conditional on the listed Wilson/OPE interval inputs; it is not a continuum or Hamiltonian spectral-transfer theorem.

## Equations

- transported-sheet-flux: `X_u^{a,\sigma}=\sum_{p\in S_u} w_{u,p}\,\operatorname{Ad}_{U_{\gamma_{u,p}}} F_{\mu\nu,\sigma}^{a}(p)\,\omega_u^{\mu\nu}(p)`. Valid when: Valid when the heat-kernel plaquette logarithm and chosen transport paths define the same cutoff Wilson sheet observable.
- endpoint-connected-polarization: `R_{uv}^{\sigma}=\left\langle :Q_u^{\sigma}:\,:Q_v^{\sigma}:\right\rangle_c,\qquad Q_u^{\sigma}=\frac{g_R^2}{4N}\,X_u^{a,\sigma}X_u^{a,\sigma}`. Valid when: Applies after diagonal vacuum and perimeter normalization of the reflected Wilson endpoint observables in the fixed cutoff theory.
- color-geometric-decomposition: `R_{\sigma}=\alpha_N g_R^4\,(C_{\sigma}\circ C_{\sigma})+\frac{g_R^4}{16N^2}K_{4,\sigma}+E_{\mathrm{OPE},\sigma},\qquad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Requires the same-theory boundary OPE through fourth order and the connected-cumulant subtraction of all vacuum factors.
- shell-negative-bound: `\lambda_{\min}\bigl(P_EK_{4,\sigma}P_E\bigr)\ge -A_0^{-}(\sigma)-A_1^{-}(\sigma)-A_2^{-}(\sigma)-T_{\ge3}(\sigma)`. Valid when: Valid for the finite sheet-kernel matrix after Hermitian symmetrization and Gershgorin shell row-sum compression.
- post-HK-margin: `\Delta_{\sigma}=m_G(\sigma)-\frac{g_R^4}{16N^2}\bigl(A_0^{-}+A_1^{-}+A_2^{-}+T_{\ge3}\bigr)-e_{\mathrm{OPE}}(\sigma)-s_{HK}(\sigma)`. Valid when: Applies when m_G is the minimum eigenvalue of the compressed Gaussian color square and s_HK is the same-basis Schur energy.
- finite-endpoint-conclusion: `\Delta_{\sigma}>0\Longrightarrow P_E\bigl(R_{\sigma}-S_{HK}\bigr)P_E\succeq \Delta_{\sigma}P_E`. Valid when: Valid only for the worked finite endpoint box with all interval inputs certified in the same regulator.

## Attempted Derivation

- Conceptual pressure attacked: mediate actual connected Wilson cumulants to Schur-corrected endpoint positivity without inflating a finite Wilson calculation into the Clay theorem.
- Declarative tension: Wilson/OPE coefficients, connected kappa4 negativity, OPE errors, and H,K Schur energy must be valid in one cutoff theory, while continuum OS reconstruction and spectral transfer remain quarantined.
- Critical carrier audit: scalar R is too weak and representation-limited; full gauge-invariant OS observable density is too strong and circular for this local gate; raw plaquette enumeration is exact but fragmented.
- Choose the sheet-kernel hypergraph because it encodes sheets, weights, heat-kernel transporters, color tensors, shell labels, multiplicities, OPE intervals, and Schur data in one finite object.
- Expand each endpoint Wilson sheet through the heat-kernel boundary OPE and define the transported curvature flux X_u^sigma.
- Use vacuum subtraction and diagonal perimeter normalization so disconnected vacuum factors cancel before R_sigma is formed.
- Evaluate crossed two-curvature contractions; the color trace gives alpha_N=(N^2-1)/(8N^2), and the geometric part is the Hadamard square C_sigma o C_sigma, hence PSD.
- Put all genuinely non-Gaussian fourth-order input into K_{4,sigma}, the connected four-curvature cumulant compressed to endpoint sheet nodes.
- Partition K_{4,sigma} rows into shells ell=0,1,2 plus tail and apply a Hermitian Gershgorin row-sum lower bound to its negative spectral part.
- Subtract the already finite H,K Schur energy s_HK and the OPE interval e_OPE to obtain the hard gate Delta_sigma.

Blocking gap: The first actual A0,A1,A2 intervals have not been evaluated from the heat-kernel lattice measure for the worked H,K geometry; the derivation is a valid finite reduction but lacks the numerical or rigorous interval certificate.

## Falsifiers

- Delta_sigma<=0 after certified same-regulator A0,A1,A2 intervals is a direct falsifier for the worked collar/hairpin endpoint route.
- A non-invariant quotient of sheet orbits that changes a Wilson trace identity invalidates the hypergraph recovery map.
- A connected kappa4 orbit with negative interval larger than the Gaussian color-square margin demotes the finite Route A certificate.
- An OPE remainder e_OPE of the same size as m_G-s_HK prevents promotion even if the first three shell bounds are favorable.
- A tail T_ge3 without a finite same-cutoff envelope shows that A012 truncation is not a valid proof object.
- Residual disconnected vacuum or perimeter terms after normalization falsify the claimed R_sigma decomposition.

## Learning

Cycle 283 attacks the missing mediator between connected boundary-OPE polarization and Schur-corrected endpoint positivity. The hard gate is Delta_sigma: success proves only a finite post-H,K endpoint-box positivity certificate, while failure gives a valid falsifier for the Wilson collar/hairpin geometry. The conceptual value signal is sharp and route-changing at finite scope because R is no longer a symbolic parameter: it is a heat-kernel connected Wilson cumulant decomposed into a PSD Gaussian color square, shell-bounded kappa4, OPE error, and the same-basis H,K Schur energy. The larger YM gates--continuum existence, OS/Wightman axioms, observable density, regulator-independent Schwinger functions, large-field/topology control, and physical-unit mass gap--remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and calculation guide for A0,A1,A2.`
- Rationale: The branch has already reduced R to a connected Wilson cumulant; another abstraction-only restatement would loop. A concrete finite heat-kernel endpoint experiment can decide whether the kappa4 shell terms plausibly fit under the Gaussian-Schur margin without touching Clay-level gates.
- Situation seed: Finite SU(N) heat-kernel lattice Yang-Mills on a reflected endpoint box containing the fixed H,K collar/hairpin Wilson sheets; compute the compressed kappa4 shell orbit intervals for ell=0,1,2 using the same Wilson OPE and Schur block.
- Varied variable: The smoothing ratio r=sigma/a, with r in a small discrete set such as 1,2,3 while keeping the endpoint geometry fixed.
- Held-fixed controls: Same finite lattice volume, reflection plane, Wilson sheet basis, and H,K Schur-Feshbach block., Same heat-kernel regulator, coupling g_R, diagonal Wilson normalization, and color trace convention., Same shell equivalence policy: only Wilson-invariant sheet symmetries and trace identities are quotiented.
- Expected observation: If the route is viable, m_G(r)-s_HK(r) should remain larger than the certified kappa4 and OPE envelopes for at least one r; if A0 or A1 already overwhelms the margin, the branch gets an early finite falsifier.
- Transfer certificate needed: A checked hypergraph-to-Wilson recovery map, rigorous interval enclosures for canonical kappa4 shell orbit contractions, a same-regulator OPE error bound, and a verified Schur energy computed in the identical endpoint basis.

## Next Experiment

Build the fixed H,K endpoint sheet-kernel hypergraph, enumerate canonical ell=0,1,2 four-curvature orbit contractions, compute their SU(N) color factors, and return certified intervals for A0,A1,A2 at one heat-kernel smoothing ratio r=sigma/a.

