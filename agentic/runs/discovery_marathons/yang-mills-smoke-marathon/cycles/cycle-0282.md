# cycle-0282

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Fractional endpoint source intervals for the post-H,K Wilson gate

## Candidate Lemma

Fractional endpoint source intervals give a valid finite same-theory certificate for the post-H,K three-hairpin OS gate: I_- >= 0 promotes this finite block, while I_+^adv < 0 gives a concrete same-theory falsifier.

## Definitions

- source object: finite-cutoff SU(N) Yang-Mills heat-kernel plaquette-sheet endpoint boxes v with same-theory Wilson sheet sources Z_{v,a}(s) attached to the reflected three-hairpin block.
- target object: the scalar Schur-Feshbach post-H,K OS endpoint gate for the fixed reflected Wilson block, not a continuum YM theory and not a mass-gap statement.
- controlled interface: the carrier C_ep maps seven endpoint source values, fractional incidences b_ij(v), color factor C_N, Gaussian margin M_G, and T_tail to an interval [I_-,I_+^adv].
- same-theory condition: auxiliary sources are differentiated at zero and then removed; no boundary counterterm, no change of Wilson normalization, and no enlargement of the gauge-invariant observable algebra are allowed.
- fractional incidence: b_ij(v) is the fraction of endpoint box v covered by the ij reflected Wilson pair footprint in the heat-kernel plaquette-sheet regulator.
- danger carrier: D_v=2 b_12(v)-4 b_13(v)-4 b_23(v); negative endpoint kappa4 is dangerous only through [D_v]_+.

## Assumptions

- Model: four-dimensional finite-volume SU(N) lattice Yang-Mills with heat-kernel plaquette action, reflection plane fixed, and gauge-invariant Wilson plaquette sheets only.
- Regime: fixed three-hairpin collar block after the H,K Schur-Feshbach computation; endpoint boxes have side ell with a << ell << collar separation before collapse.
- Cutoff: Z_{v,a}(s) is computed with the original heat-kernel measure and the same Wilson sheet geometry; the source is an auxiliary probe of the connected boundary OPE.
- Uniformity: eighth source derivatives and endpoint-tail estimates are bounded independently of a along the chosen endpoint scaling window.
- Same-theory: the recovery map exports only the zero-source Wilson Schwinger data interval; source insertions do not define new observables.
- Local: Wick-square Gram terms are removed by using log Z, and the straight f f commutator contact is canceled by the already verified null-incidence identity.
- Validity: fractional incidences b_ij(v) are measured from regulated plaquette sheets and must be stable under reflection and endpoint-box refinement.

## Equations

- fractional endpoint dominance: `b_{ij}(v)=\frac{|P_{ij}\cap v|}{|v|},\qquad D_v=2b_{12}(v)-4b_{13}(v)-4b_{23}(v)`. Valid when: Valid when the endpoint boxes are measured in the heat-kernel plaquette-sheet regulator and the same three Wilson pair footprints define all b_ij.
- seven point endpoint cumulant stencil: `\widehat\kappa_{4,v}(\ell)=h^{-4}\sum_{r=-3}^{3}c_r\log Z_{v,a}(rh\ell),\quad c_0=28/3,\ c_{\pm1}=-13/2,\ c_{\pm2}=2,\ c_{\pm3}=-1/6`. Valid when: Applies when log Z_{v,a}(s\ell) is eight times differentiable in the same-theory source direction on the certified interval |s|<=3h.
- stencil remainder: `\left|\widehat\kappa_{4,v}-\partial_s^4\log Z_{v,a}(s\ell)|_{s=0}\right|\le \frac{7h^4}{240}M_{8,v}`. Valid when: Requires a cutoff-uniform bound M_{8,v} for the eighth source derivative of the endpoint-box log partition function.
- negative cumulant clipping: `\beta_v^+=\max(0,-\underline\kappa_{4,v}),\qquad \beta_v^-=\max(0,-\overline\kappa_{4,v})`. Valid when: Valid when the certified interval [underline kappa4, overline kappa4] encloses the same singlet connected four-flux endpoint cumulant.
- finite endpoint gate interval: `I_-=M_G-C_N\sum_v\beta_v^+[D_v]_+-T_{\rm tail},\quad I_+^{\rm adv}=M_G-C_N\sum_v\beta_v^-[D_v]_+ + C_N\sum_v\beta_v^+[-D_v]_+ +T_{\rm tail}`. Valid when: Applies after Wick-square Gram positivity and straight f f null-incidence cancellation have removed all non-endpoint contributions except the certified tail.

## Attempted Derivation

- Conceptual pressure attacked: endpoint collapse must be sign-certified while preserving the same finite Wilson theory inherited from collar reflection positivity.
- Declarative tension: finite collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must jointly hold, but raw R is representation-limited and raw kappa4 is too strong because it ignores null-channel incidence.
- Freeze the finite three-hairpin post-H,K block; the hard gate is the finite reflected-Wilson OS Schur-Feshbach endpoint scalar, not any Clay-level continuum or mass-gap gate.
- Replace symbolic R by heat-kernel endpoint source partition functions Z_{v,a}(s); fourth derivatives of log Z give the singlet connected four-flux cumulant and remove Wick-square Gram pieces.
- Use the previously isolated null-incidence identity to cancel straight f f commutator contacts; charge all remaining nonlocal corner and large-field contributions to T_tail.
- Contract the connected endpoint cumulant with fractional incidences D_v=2b12-4b13-4b23; negative compact-group kappa4 contributes adversely only through [D_v]_+.
- Apply the seven-point fourth-derivative stencil with the explicit M8 remainder to get beta_v intervals, then form I_- and I_+^adv.
- Conceptual value signal: this is sharp and route-changing at finite scope because it distinguishes harmful 12-dominance from harmless negative kappa4 and exports one valid scalar interval to the OS gate.

Blocking gap: Actual certified values of b_ij(v), beta_v intervals from Z_{v,a}, and cutoff-uniform T_tail are not yet computed for the locked hairpin endpoint boxes.

## Falsifiers

- A certified endpoint data set with I_+^adv<0 is a finite same-theory falsifier of the post-H,K Wilson OS transfer gate.
- The seven source values of log Z_v fail to have a cutoff-uniform M8 remainder, so the endpoint interval is not valid.
- Fractional incidences are unstable under plaquette-sheet refinement or reflection, meaning C_ep is not a same-theory carrier.
- A boundary counterterm is needed to define Z_{v,a}(s) or its derivatives at endpoint collapse.
- The tail T_tail absorbs a nonlocal large-field contribution that does not vanish or remain bounded in the cutoff window.
- Two carriers with identical visual endpoint geometry but different regulated source derivatives give different intervals, falsifying geometry-only abstraction.
- The Wilson observable algebra changes when endpoint source probes are introduced, breaking the same-theory condition.

## Learning

Cycle 282 advances from a clipped-carrier slogan to a valid fractional endpoint interval theorem. The current carrier raw R is too weak because it forgets incidence signs, and raw kappa4 is too strong because negative compact-group kappa4 is harmless unless multiplied by positive D_v. Compared with the global Schur-preimage route, C_ep is local after H,K and decision-grade for this finite gate. Efficient representation now encodes endpoint boxes, seven source values, beta intervals, fractional b_ij incidences, C_N, M_G, and T_tail; preserves Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; uses source differentiation, interval arithmetic, clipping, color multiplication, incidence contraction, and tail addition; identifies carriers only by equal regulated source data; and transfers only [I_-,I_+^adv] to the finite OS gate. Success promotes the finite post-H,K reflected-Wilson OS transfer gate; failure gives a concrete falsifier. Clay continuum construction and mass gap remain non-claimed.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and data-design template for the finite post-H,K endpoint calculation.`
- Rationale: The branch needs a concrete heat-kernel endpoint computation because abstract OS closed-cone arguments and raw kappa4 signs cannot decide the fractional incidence gate.
- Situation seed: Finite-volume SU(N) heat-kernel lattice Yang-Mills with the locked three-hairpin reflected Wilson block; endpoint boxes are plaquette-sheet neighborhoods where b12, b13, and b23 overlaps are measured fractionally, and Z_v(s) is evaluated at seven source points.
- Varied variable: fractional 12-dominance alpha_v=D_v=2b12(v)-4b13(v)-4b23(v) while beta_v, M_G, C_N, and T_tail are held in certified intervals.
- Held-fixed controls: Same heat-kernel plaquette regulator and finite cutoff action., Same zero-source gauge-invariant Wilson hairpin observables and Wilson normalization., Same H,K Schur-Feshbach null channel and straight f f cancellation identity., No boundary counterterm and no enlargement of the test algebra., Same endpoint-box scaling ell(a) and source stencil step h.
- Expected observation: If alpha_v<=0 on all dominant boxes, negative endpoint kappa4 is protective or neutral; if alpha_v>0 on sufficiently large 12-dominant boxes, I_- can cross zero and I_+^adv can become a finite falsifier interval.
- Transfer certificate needed: Certified regulated source-derivative intervals, stable fractional incidence measurements, a cutoff-uniform M8 remainder, a valid T_tail bound, and an explicit same-theory audit showing sources are removed after differentiation.

## Next Experiment

For the locked three-hairpin heat-kernel plaquette-sheet regulator, tabulate fractional b12,b13,b23 for each endpoint box, compute the seven log Z_v(rh ell) intervals, certify M8 and T_tail, then evaluate I_- and I_+^adv.

# Endpoint Ward-Hessian interval for the H,K Wilson mediator

## Candidate Lemma

Conditional finite Route A lemma: a cutoff-uniform Ward-Hessian enclosure of the flowed endpoint cumulant gives a valid lower interval for R_{++}; if it beats the Schur-Feshbach leakage L_+, the post-H,K endpoint box is positive.

## Definitions

- source object: finite-volume SU(N) lattice Wilson measure with gradient-flowed hairpin sheet currents J_+^I in an endpoint box I.
- target object: finite Schur-Feshbach plus-channel endpoint positivity Q_+^I>0, not continuum YM existence or a mass gap.
- controlled interface: R_{++}^I is the centered flowed Wilson covariance after disconnected, perimeter, and cusp subtractions.
- same-theory condition: the Wilson action, cutoff sequence, flow time, counterterms, and reflected observables are identical on both sides of the transfer.

## Assumptions

- Model: SU(N), N>=2, finite box, lattice spacing a, Wilson action, reflection plane fixed, gradient flow t>=c a^2.
- Regime: endpoint cell diameter eta<sqrt(t)/10 and separation from nonlocal sheet features at least 3sqrt(t).
- Cutoff: heat-kernel derivative majorants for C_4 and C_6 are uniform in a along the chosen RG window.
- Same-theory: no auxiliary Gaussian measure replaces the Wilson ensemble; pair terms are only a cumulant-expansion component.
- Local: H,K sheets, endpoint currents, cell moments, and counterterms are fixed finite objects.

## Equations

- flowed-endpoint-cumulant: `R_{++}^I(t,a)=\kappa_2^{t,a}(:W[J_+^I]:,:W[\theta J_+^I]:)`. Valid when: Valid when the reflected flowed Wilson hairpins use identical lattice action, flow time, endpoint cell, and subtraction scheme.
- ward-hessian-lower-interval: `R_{++}^I\ge g_t^4(N^2-1)(2G_{++}^{I,-}-NH_4^{I,+}M_{2,+}^2)-E_6^{I,+}`. Valid when: Applies after Ward, cusp, monopole, and dipole cancellations leave only endpoint Hessian remainders in the local cell.
- finite-promotion-test: `A_+^I+R_{++}^{I,-}-L_+^I>0\ \Rightarrow\ Q_+^I>0`. Valid when: Requires the same finite H,K Schur-Feshbach block, certified leakage L_+, and cutoff-uniform lower interval for R_{++}^I.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: finite-volume SU(N) lattice Wilson measure with gradient-flowed hairpin sheet currents J_+^I in an endpoint box I.; target object: finite Schur-Feshbach plus-channel endpoint positivity Q_+^I>0, not continuum YM existence or a mass gap.; Model: SU(N), N>=2, finite box, lattice spacing a, Wilson action, reflection plane fixed, gradient flow t>=c a^2..
- Expand the two centered flowed Wilson hairpins in sheet currents through order g_t^4; disconnected product and one-hairpin perimeter/cusp counterterms cancel local singular pieces.
- The cross-pair contractions give the positive baseline 2g_t^4(N^2-1)G_{++}^I; reflection and orientation fix the color sign.
- For the connected four-curvature term, Ward identities plus plus-channel moment cancellation remove monopole and dipole pieces; Taylor remainder is bounded by NH_4^+M_2^2.
- Insert R_{++}^{I,-} into the finite Schur-Feshbach plus block Q_+=A_+ + R_{++}-L_+; positivity is a finite Route A certificate only.

Blocking gap: Need a cutoff-uniform interval proof for H_4^{I,+}, E_6^{I,+}, and counterterm matching in the lattice-flow regulator.

## Falsifiers

- falsifier: lattice Ward subtraction leaves an uncancelled O(eta^0) or O(eta^1) endpoint term.
- falsifier: certified H_4 or E_6 intervals grow with cutoff and destroy the valid flow-window bound.
- falsifier: R_{++}^{I,-}<=L_+^I-A_+^I for the concrete H,K endpoint geometry.
- falsifier: endpoint current equivalence changes the Wilson covariance, showing the carrier is representation-limited.

## Learning

Declarative tension: finite Schur-Feshbach positivity, positive flowed pair covariance, and same-theory Wilson renormalization must jointly hold, but C4 can erase the mediator. Endpoint sheet currents beat raw contours and global OS witnesses because Ward moments, heat-kernel Hessians, and interval arithmetic become primitive. Value signal: R_{++} becomes a valid finite falsifier and promotion inequality.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and proof-search guide.`
- Rationale: The branch needs a concrete test of whether C4 is eta^2-suppressed, not another OS/Wilson obstruction restatement.
- Situation seed: SU(N) lattice Wilson action with gradient flow, fixed reflected H,K hairpin endpoint boxes, centered renormalized Wilson hairpins, and Ward-subtracted sheet currents.
- Varied variable: rho=eta/sqrt(t), the endpoint-cell diameter relative to flow radius.
- Held-fixed controls: same Wilson action, cutoff sequence, reflection plane, and flowed observable family, fixed H,K sheet geometry, plus-channel endpoint current, N, and Schur-Feshbach leakage L_+, same perimeter/cusp counterterms and Ward-subtraction prescription
- Expected observation: As rho decreases, the connected C4 interval should scale like rho^2 while the positive pair baseline stays on a flow plateau; violation is a route-demoting falsifier.
- Transfer certificate needed: A cutoff-uniform Ward-Hessian interval and flow-plateau certificate proving the observed scaling transfers to the finite Schur-Feshbach endpoint inequality in the same theory.

## Next Experiment

Build the concrete H,K endpoint cell partition, compute certified intervals for G_{++}^-, H_4^+, M_{2,+}, E_6^+, and test the promotion inequality against L_+.

# Gauge-Invariant Observable Density In The Excitation Sector / finite post-H,K Wilson endpoint audit

## Candidate Lemma

Finite same-regulator shell-envelope theorem: the post-H,K reflected-Wilson endpoint form is bounded below by Delta_sigma. Delta_sigma>0 certifies only finite endpoint-box positivity; Delta_sigma<=0 is a valid falsifier for this collar/hairpin Route A geometry.

## Definitions

- source object: heat-kernel regulated finite-volume SU(N) Wilson measure at lattice spacing a, smearing sigma, coupling g_R(a,sigma), reflected endpoint Wilson sheets S_u, and transported curvature fluxes X_u^a.
- target object: the finite endpoint quadratic form on H,K-reduced reflected Wilson states after Schur-Feshbach subtraction, not the continuum Hamiltonian spectrum.
- controlled interface: sheet-kernel hypergraph Phi_sigma with sheet-pair nodes, Gaussian covariance C_sigma, connected four-curvature block K4_sigma, OPE intervals, endpoint weights, and a recovery map to the Wilson Gram matrix.
- same-theory condition: all cumulants, OPE errors, H,K matrices, Schur energy, reflection plane, coupling normalization, and Wilson basis are computed in the same cutoff theory.
- bridge observable: R_{uv,sigma} is the connected boundary-OPE polarization cumulant of two vacuum-subtracted transported curvature-square Wilson insertions.
- shell amplitudes: A_ell(sigma) are weighted row-sum envelopes of K4_sigma over graph-distance ell in Phi_sigma.
- hard gate: Delta_sigma is the finite endpoint positivity margin after Gaussian positivity, kappa4 negativity, OPE error, and Schur hairpin subtraction.

## Assumptions

- Model: finite lattice SU(N) Yang-Mills with heat-kernel plaquette regulator and reflection plane fixed before endpoint compression.
- Cutoff: sigma/a lies in a compact admissible interval and the endpoint box contains finitely many Wilson sheets of bounded diameter.
- Same-theory: no cumulant, Schur matrix, or OPE coefficient is imported from a different regulator, coupling, volume, or Wilson basis.
- Local: the H,K collar/hairpin geometry and endpoint sheet-kernel graph are fixed finite objects during this certificate.
- Validity: the boundary Wilson OPE has a same-regulator operator-norm remainder bounded by e_OPE(sigma) on the endpoint span.
- Constraint: QHQ on the eliminated H,K hairpin sector is invertible with Schur energy s_HK=||B^*E^{-1}B|| on the endpoint subspace.
- Non-claim: success changes only the finite Route A endpoint-box gate and does not prove OS reconstruction, continuum existence, observable density, or a Hamiltonian mass gap.

## Equations

- transported flux: `\mathsf X_u^a=\int_{S_u} h_{x_0x}^{(\sigma)}F_{\mu\nu}^a(x)h_{xx_0}^{(\sigma)}\,d\Sigma^{\mu\nu}(x)`. Valid when: Valid when each endpoint sheet is smaller than the smearing scale and heat-kernel parallel transport is used in the cutoff theory.
- connected boundary polarization: `R_{uv,\sigma}=\operatorname{Cum}_{\mu_{a,\sigma}}\big(:\operatorname{tr}\mathsf X_u^2:,:\operatorname{tr}\mathsf X_v^2:\big)`. Valid when: Valid when Wick ordering denotes subtraction of the same cutoff expectation and both observables lie in the reflected Wilson algebra.
- Gaussian plus kappa4 split: `R_{uv,\sigma}=\alpha_N g_R^4(C_{uv,\sigma})^2+\frac{g_R^4}{16N^2}K^{(4)}_{uv,\sigma}+E^{\mathrm{OPE}}_{uv,\sigma},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid when the Wilson boundary OPE is truncated at four transported curvature insertions and disconnected vacuum/perimeter terms are subtracted.
- shell amplitudes: `A_\ell(\sigma)=\sup_u\sum_{v:\,d_\Gamma(u,v)=\ell}|w_u w_v K^{(4)}_{uv,\sigma}|`. Valid when: Valid when sheet-kernel hypergraph distance and endpoint weights are fixed by the H,K Wilson geometry.
- endpoint lower bound: `\lambda_{\min}(P_E R_\sigma P_E-S_{HK})\ge g_R^4\alpha_N m_G(\sigma)-\frac{g_R^4}{16N^2}(A_0+A_1+A_2+T_{\ge3})-e_{\mathrm{OPE}}(\sigma)-s_{HK}`. Valid when: Valid when the endpoint compression, shell row-sum bounds, and Schur-Feshbach matrices are all computed in the same cutoff theory.
- hard gate margin: `\Delta_\sigma:=g_R^4\alpha_N m_G-\frac{g_R^4}{16N^2}(A_0+A_1+A_2+T_{\ge3})-e_{\mathrm{OPE}}-s_{HK}>0`. Valid when: Valid when the finite endpoint form is the only target and no continuum OS spectral transfer is being claimed.

## Attempted Derivation

- Conceptual pressure attacked: mediate actual connected Wilson cumulants to Schur-corrected endpoint positivity without inflating a finite calculation into the Clay mass-gap theorem.
- Declarative tension: Wilson/OPE coefficients, connected kappa4 negativity, OPE errors, and H,K Schur energy must all be valid in one cutoff theory, while continuum OS reconstruction and spectral transfer remain quarantined.
- Critique of current carrier: scalar R is too weak and representation-limited; full gauge-invariant OS density is too strong and circular for this local gate; raw plaquette enumeration is exact but fragmented.
- Choose the sheet-kernel hypergraph because it encodes sheets, plaquette weights, heat-kernel transporters, color tensors, shell labels, multiplicities, OPE intervals, and Schur data while preserving gauge invariance and reflection support.
- Expand each endpoint Wilson insertion by the same-regulator boundary OPE through four transported curvature insertions; subtract vacuum and perimeter pieces before forming R_{uv,sigma}.
- Use SU(N) trace normalization to isolate the crossed Gaussian contraction alpha_N g_R^4(C_sigma o C_sigma), which is positive semidefinite by the Schur product theorem.
- Put every non-Gaussian connected four-curvature contribution into K4_sigma and compress it to the endpoint span with the same weights as the H,K Schur form.
- Partition K4 entries by graph shell d_Gamma(u,v)=ell and apply Gershgorin row-sum bounds to get negative spectral size at most A_0+A_1+A_2+T_ge3.
- Subtract e_OPE and s_HK from the Gaussian minimum m_G to obtain Delta_sigma, the hard gate for finite endpoint positivity.
- Hard gate effect: Delta_sigma>0 promotes a finite Route A endpoint-box theorem; Delta_sigma<=0 or non-summable shell tails demotes this collar/hairpin geometry as a valid falsifier.

Blocking gap: The missing proof object is a same-regulator nonperturbative interval for B_0(sigma), B_1(sigma), B_2(sigma), and T_ge3 controlling the connected four-curvature cumulant in the heat-kernel lattice measure.

## Falsifiers

- Delta_sigma<=0 after rigorous A_0,A_1,A_2,T_ge3 intervals is a finite falsifier for the H,K endpoint positivity route.
- A same-regulator kappa4 shell envelope that grows with shell multiplicity faster than the Gaussian square margin demotes the sheet-kernel certificate.
- A quotient audit showing non-invariant trace reduction invalidates the compressed hypergraph and forces raw plaquette enumeration.
- An OPE remainder e_OPE comparable to m_G at admissible sigma invalidates the boundary-OPE polarization transfer.
- A Schur hairpin energy s_HK exceeding the positive Gaussian color-square margin shows the H,K correction kills the endpoint certificate.
- Any attempt to infer OS/Wightman reconstruction or a Hamiltonian mass gap from Delta_sigma alone is an overclaim falsifier for branch promotion.

## Learning

Cycle 282 makes the contribution-making move requested by the R/kappa4 audit: R is a same-regulator connected Wilson cumulant, not a symbolic endpoint parameter. The conceptual pressure is the missing mediator from actual boundary-OPE polarization to Schur-corrected positivity. The efficient representation is still the sheet-kernel hypergraph, but now its value is operational: it names the first computable shell intervals A_0,A_1,A_2 and the hard gate Delta_sigma. The result is sharp and route-changing only at finite Route A scope; success proves endpoint-box positivity for the worked H,K geometry, while failure is a valid falsifier. Clay-level existence, nontrivial continuum limit, and Hamiltonian mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the first same-regulator A_0,A_1,A_2 interval.`
- Rationale: The branch has already fixed the abstract R/kappa4 carrier; the next valid learning is whether the concrete heat-kernel Wilson cumulant can beat Schur hairpin energy in a finite endpoint box.
- Situation seed: Fixed finite SU(N) heat-kernel lattice endpoint box with the worked H,K collar/hairpin Wilson sheets, reflected boundary OPE, and sheet-kernel hypergraph Phi_sigma.
- Varied variable: rho=sigma/a, the smearing-to-lattice ratio, varied over a compact admissible interval while the endpoint geometry is unchanged.
- Held-fixed controls: Same Wilson endpoint basis, reflection plane, and H,K Schur-Feshbach blocks., Same finite volume, lattice spacing a, heat-kernel action, coupling normalization g_R, and trace normalization., Same quotient policy: only Wilson trace and sheet symmetries with audited recovery., Same non-claim boundary: no continuum limit, OS spectral transfer, or Clay mass-gap conclusion.
- Expected observation: If A_0,A_1,A_2 and T_ge3 decrease or remain bounded as rho increases while m_G stays positive, Delta_sigma may become positive; if kappa4 shells or OPE errors dominate, the route is demoted.
- Transfer certificate needed: A rigorous same-regulator interval for B_0,B_1,B_2,T_ge3, plus quotient recovery and OPE error bounds, before the observation may enter the finite endpoint positivity proof queue.

## Next Experiment

For the fixed H,K endpoint box, enumerate raw sheet-pair shells ell=0,1,2; compute M_ell and G_ell from the heat-kernel transport kernels; insert provisional rigorous B_ell intervals; audit quotient recovery; then evaluate Delta_sigma(rho) over admissible sigma/a.

