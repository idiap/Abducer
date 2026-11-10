# cycle-0322

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Screened endpoint source interval for the post-H,K Wilson gate

## Candidate Lemma

For the fixed three-hairpin Route A block, the post-H,K endpoint contribution is certified by a source-equivalent clipped interval. Negative endpoint kappa_4 can demote the finite OS gate only through positive signed endpoint leakage and a uniform tail.

## Definitions

- source object: heat-kernel plaquette-sheet SU(N) endpoint source classes c with regulated Wilson endpoint partition functions Z_{a,c}(s) and fractional incidences b_{ij,c}.
- target object: the finite post-H,K reflected-Wilson Schur-Feshbach scalar I_gate for the null channel of one Route A Wilson block, not the continuum Yang-Mills mass gap.
- controlled interface: C_ep sends same-source endpoint classes to kappa intervals, signed D_c incidences, color factor C_N, Gaussian margin M_G, and tail tau_tail, then exports only [I_-,I_+] to the finite OS gate.
- same-theory condition: Z_{a,c}(s), Wilson normalization, source classes, incidences, and tails are computed in the same heat-kernel regulated gauge-invariant Wilson theory with no boundary counterterm or observable replacement.
- Endpoint source class c means all endpoint boxes with identical regulated source derivative data after orientation, color trace, and reflection conventions are fixed.
- The conceptual pressure is endpoint collapse inside the same Wilson theory; the declarative tension is collar OS positivity plus fixed Wilson observables plus singular connected endpoint OPE without a boundary theory.

## Assumptions

- Model: four-dimensional Euclidean SU(N) lattice Yang-Mills with heat-kernel plaquette-sheet Wilson regulator and reflected hairpin collars.
- Regime: fixed finite three-hairpin block after the H,K Schur-Feshbach reduction, with small endpoint boxes and fixed physical Wilson geometry.
- Uniformity: source derivative bounds, incidence limits, and tau_tail are uniform in cutoff and volume for the selected finite block.
- Same-theory: the Wilson observables, reflection map, color normalization, and endpoint source partition functions are not changed during collar collapse.
- Validity: connected logarithms remove Wick-square disconnected pieces, and the straight f f commutator contact cancels by the null-incidence identity.
- Local: all non-endpoint and corner-overlap leftovers are charged to tau_tail rather than hidden in a changed boundary theory.

## Equations

- endpoint signed leakage: `D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}`. Valid when: Valid when endpoint boxes have been quotient-coarsened by identical regulated source data and fractional Wilson incidences.
- connected endpoint cumulant witness: `\kappa_c=\left.\partial_s^4\log Z_{a,c}(s)\right|_{s=0},\qquad \kappa_c\in[\kappa_c^-,\kappa_c^+]`. Valid when: Applies to the same heat-kernel endpoint source used by the Wilson collar observables.
- root-quartic analytic screen: `\kappa_c=-\frac{t_c^4}{60}R_4(L_c)+E_c,\qquad R_4(L)=N\operatorname{tr}(L^4)+3(\operatorname{tr}L^2)^2\ge0`. Valid when: Requires endpoint normal coordinates, small source strength, and a uniform bound on the remainder E_c.
- post-HK endpoint scalar: `I_{gate}=M_G+C_N\sum_c D_c\kappa_c+T_{tail},\qquad C_N=\frac{g_a^4}{4}\left(\frac{T_F}{N}\right)^2`. Valid when: Valid after the H,K reduction, Wick-square Gram positivity, and straight-contact null cancellation are imposed.
- certified lower interval: `I_- = M_G+C_N\sum_c\big([D_c]_+\kappa_c^- -[-D_c]_+\kappa_c^+\big)-\tau_{tail}`. Valid when: Valid when each cumulant interval and the absolute tail bound are cutoff-uniform for the endpoint classes.
- clipped root-quartic sufficient screen: `\kappa_c^+\le0\ \Longrightarrow\ I_-\ge M_G-C_N\sum_c[D_c]_+\left(\frac{t_c^4}{60}R_4^+(L_c)+\varepsilon_c\right)-\tau_{tail}`. Valid when: Applies after the analytic screen certifies nonpositive endpoint cumulants on the protected classes.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: heat-kernel plaquette-sheet SU(N) endpoint source classes c with regulated Wilson endpoint partition functions Z_{a,c}(s) and fractional incidences b_{ij,c}.; target object: the finite post-H,K reflected-Wilson Schur-Feshbach scalar I_gate for the null channel of one Route A Wilson block, not the continuum Yang-Mills mass gap.; Model: four-dimensional Euclidean SU(N) lattice Yang-Mills with heat-kernel plaquette-sheet Wilson regulator and reflected hairpin collars..
- Start with the heat-kernel plaquette-sheet Wilson regulator and the fixed post-H,K three-hairpin null channel; keep the gauge-invariant Wilson algebra locked.
- Write each endpoint contribution as a connected source derivative of log Z_{a,c}; the fourth connected derivative kills disconnected Wick-square contractions.
- Use the established cancellations: one-body Wilson normalizations vanish on the null channel, and the straight nonabelian f f contact cancels by the incidence identity.
- Coarsen endpoint boxes only by equality of regulated source data; sum signed D_v before clipping to avoid artificial positive-D leakage.
- Insert the SU(N) endpoint normal-coordinate expansion, where the leading connected non-Gaussian term is the negative root-quartic Haar contribution plus a uniform remainder.
- Derive the interval I_- and I_+ for I_gate; I_->=0 promotes this finite block, while I_+<0 is a same-theory finite falsifier.

Blocking gap: The actual endpoint source intervals, fractional incidence table, and cutoff-uniform tau_tail bound have not been computed for the concrete hairpin geometry.

## Falsifiers

- A source-certified class with D_c>0 and a sufficiently negative connected cumulant interval forcing I_+<0 is a finite same-theory falsifier.
- A protected D_c<0 class with kappa_c^+>0 large enough to lower I_- falsifies the nonpositive root-quartic screen.
- A cutoff-dependent tau_tail or endpoint M_8 bound makes the proposed finite interval not valid for the regulator-removal direction.
- A boundary counterterm, cusp renormalization not already in the locked Wilson normalization, or changed source algebra violates the same-theory condition.
- Incorrect source-equivalence coarsening, detected by unequal seven-point log Z data, invalidates the aggregation before clipping.

## Learning

Cycle 322 attacks the conceptual pressure of endpoint collapse inside the same Wilson theory. The theorem-level tension is that collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must coexist without adding a boundary theory, while H,K and the half-overlap shield do not decide the scalar. The current carrier raw R is too weak, raw kappa_4 spectra are too strong, and global Schur-preimage positivity is valid but too coarse after H,K. The sharper carrier C_ep is source-equivalent, incidence-signed, and cutoff-budgeted: it encodes source classes, seven source values, cumulant intervals, D_c, C_N, M_G, and tau_tail; preserves Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; uses source differentiation, interval arithmetic, aggregation before clipping, color multiplication, and tail addition; identifies equivalence only by regulated source data; exports only [I_-,I_+]. The hard gate is the finite post-H,K reflected-Wilson OS transfer scalar. Success promotes only this finite block; failure gives a finite falsifier; missing source data keeps quarantine. The conceptual value signal is sharpness at finite scope: negative SU(N) root-quartic cumulants are explanatory but not the obstruction; positive-D leakage times same-theory connected cumulants plus uniform tail is. Clay continuum construction, full OS/Wightman reconstruction, nontriviality, and positive mass gap remain non-claimed.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe and proof-search guide.`
- Rationale: The branch has already isolated the endpoint R/kappa_4 term; another abstract OS restatement would not decide the finite post-H,K gate. A target-preserving endpoint source experiment can test the connected cumulant witness without changing the Wilson theory.
- Situation seed: SU(N) heat-kernel plaquette-sheet regulator for the fixed three reflected Wilson hairpins; endpoint boxes are grouped by equal seven-point source data and fractional incidences b12,b13,b23.
- Varied variable: positive-D leakage ratio alpha_c=b12,c/(b13,c+b23,c+eta), equivalently the signed dominance D_c=2b12,c-4b13,c-4b23,c.
- Held-fixed controls: Same gauge-invariant Wilson observable algebra and reflection map., The H,K Schur-Feshbach reduction, null vector, and Gaussian margin M_G., Heat-kernel regulator, color normalization C_N, and no boundary counterterm., Uniform source step h, endpoint scale t_c, and tail accounting rule tau_tail.
- Expected observation: Classes with half-overlap shield D_c<=0 should be harmless when kappa_c<=0; only source-certified D_c>0 classes can compete with M_G. Crossing C_N sum [D_c]_+ A_c + tau_tail > M_G predicts demotion pressure.
- Transfer certificate needed: A cutoff-uniform seven-point connected cumulant witness, valid source-equivalence proof, fractional incidence convergence, no boundary renormalization, and a tau_tail bound before the observation may enter the finite OS proof queue.

## Next Experiment

Proof search plus validator-facing endpoint computation: build the source-equivalence table, evaluate the seven-point connected cumulant witness for each heat-kernel endpoint class, compute D_c after aggregation before clipping, certify M_8 and tau_tail, and return the interval [I_-,I_+] for the finite post-H,K OS gate.

# Gauge-Invariant Nontriviality Witness Selection via finite endpoint R certificate

## Candidate Lemma

Conditional annular Ward-Hessian dominance lemma: for fixed H,K endpoint boxes, the flowed plus-channel Wilson cumulant R_{++}^{ren} has a computable lower interval once each Ward-subtracted connected C4 sector has a dyadic mixed-Hessian decay exponent nu_s>2. A positive resulting margin promotes only finite endpoint-box positivity after H,K, not the Clay mass gap.

## Definitions

- source object: centered flowed SU(N) Wilson hairpin cumulants on a hypercubic lattice with Wilson action, spacing a, flow time t, endpoint boxes E_1,E_2, and renormalized one-hairpin perimeter/cusp subtraction.
- target object: the finite Schur-Feshbach endpoint-box positivity margin Delta_R for the already reduced H,K collar/hairpin cone problem.
- controlled interface: endpoint sheet currents mu_+ with zero monopole and dipole moments, Ward/cusp-subtracted C4 sector kernels K_s, positive pair kernel G_{++}, recovery error E_rec, and leakage constant L_+.
- same-theory condition: pair term, connected C4 sectors, counterterms, and recovery maps are computed from the same cutoff Yang-Mills measure and the same gradient-flow normalization before any continuum or OS spectral-transfer claim.
- R_{++}^{ren}: connected cumulant of two centered renormalized plus-channel endpoint hairpins.
- q_s: dyadic tail ratio 2^{4-2nu_s} for sector s after four-dimensional annular counting and Hessian decay.
- M_{2,+}: certified second endpoint moment of the plus current after monopole/dipole cancellation.

## Assumptions

- Model: four-dimensional Euclidean SU(N) lattice Yang-Mills with Wilson plaquette action and gauge-covariant gradient flow at t>0.
- Regime: endpoint-box diameter eta is smaller than separation rho and rho is at least a fixed multiple of sqrt(8t).
- Cutoff: all interval constants are uniform for 0<a<=a0 at fixed physical endpoint geometry and fixed flow window.
- Same-theory: no continuum Schwinger family, OS Hilbert space, or spectral measure witness is imported into this finite certificate.
- Local: only the finite H,K endpoint boxes and their endpoint sheet currents enter the inequality.
- Validity: Ward subtraction removes gauge-longitudinal and cusp-local pieces before the endpoint Taylor expansion is applied.
- Constraint: each far sector s has a certified mixed-Hessian bound with exponent nu_s>2, so q_s<1.

## Equations

- flowed connected Wilson endpoint cumulant: `R_{++}^{ren}(a,t)=\kappa_2\big(W_{+,1}^{ren}(a,t),W_{+,2}^{ren}(a,t)\big)`. Valid when: Valid when the reflected Wilson hairpins are centered, flowed, cusp-subtracted, and evaluated in the same cutoff Yang-Mills measure.
- pair and connected C4 decomposition: `R_{++}^{ren}=g_t^4 (N^2-1)\,2G_{++}+g_t^6 N(N^2-1)\,C_{4,++}^{WS}+E_{\ge 6}`. Valid when: Applies after the cumulant expansion is truncated at four-curvature order with a certified flowed remainder bound.
- annular Hessian tail: `T_s^{far}(J)\le A_s M_{2,+}^2\,{q_s^J\over 1-q_s},\qquad q_s=2^{4-2\nu_s}<1`. Valid when: Requires Ward/cusp subtraction, plus-current monopole and dipole cancellation, and sector Hessian decay on every dyadic annulus.
- certified endpoint margin: `\Delta_R^-:=g_t^4(N^2-1)\left(2G_{++}^- -N\sum_s\left(H_{s,near}^+ + A_sM_{2,+}^2{q_s^{J_s}\over1-q_s}\right)\right)-E_{rec}^+-E_{\ge6}^+-L_+`. Valid when: Valid when all interval endpoints are outward-rounded and the Schur-Feshbach leakage L_+ is from the same finite H,K reduction.
- promotion condition: `\Delta_R^->0\ \Longrightarrow\ Q_+^{endpoint}>0`. Valid when: Applies only to the finite endpoint-box Schur-Feshbach problem after H,K, not to continuum existence or mass gap.

## Attempted Derivation

- Attack conceptual pressure: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator, while positive pair covariance and same-theory recovery can both be valid and still be erased by connected C4.
- Write R_{++}^{ren} as the centered flowed Wilson cumulant after disconnected-product removal and one-hairpin perimeter/cusp subtraction.
- Expand the two thin endpoint hairpins into sheet-current curvature insertions; the pair contraction gives the positive baseline 2g_t^4(N^2-1)G_{++}.
- Use Ward subtraction and plus-channel monopole/dipole cancellation to kill constant and first Taylor terms of each far C4 sector kernel.
- On dyadic annulus j, bound the mixed Hessian by A_s 2^{-2nu_s j}; four-dimensional annular counting gives the ratio q_s=2^{4-2nu_s}.
- Sum the far annuli by A_s M_{2,+}^2 q_s^J/(1-q_s), add near-cell interval constants, recovery error, higher-cumulant remainder, and subtract the fixed Schur-Feshbach leakage L_+.
- Declare the hard gate: Delta_R^->0 promotes finite endpoint-box positivity after H,K; Delta_R^-<=0 or invalid constants quarantines this R repair without touching Clay existence or mass gap.

Blocking gap: The sector constants A_s, exponents nu_s, near-cell intervals H_{s,near}^+, and recovery error E_rec have not yet been certified by outward-rounded quadrature or analytic heat-kernel majorants for the actual H,K geometry.

## Falsifiers

- falsifier: any Ward or cusp remainder survives at order eta^0 or eta^1 and invalidates the plus-moment Hessian reduction.
- falsifier: a sector has nu_s<=2, hence q_s>=1 and the annular tail cannot be summed by the proposed certificate.
- falsifier: certified E_rec^+ exceeds the positive pair interval, showing endpoint sheet currents are representation-limited for this geometry.
- falsifier: outward-rounded near-cell quadrature gives Delta_R^-<=0 for every admissible flow window and annular split.
- falsifier: the flowed Wilson cumulant is positive at finite cutoff but loses a valid cutoff-uniform plateau as a->0.
- falsifier: zero-pairing quotienting changes color, reflection, orientation, or same-theory identity of the H,K endpoint observable.

## Learning

The declarative tension is exact: Schur-Feshbach endpoint positivity, positive flowed pair covariance, and same-theory recovery must jointly be valid, yet connected C4 can erase the mediator. Raw Wilson contours are fragmented; global OS spectral transfer and non-Gaussian witness routes are too coarse for this finite obstruction. Endpoint sheet currents are efficient only if they encode H,K sheets, endpoint moments, sector kernels, counterterms, and recovery errors; preserve gauge, color, reflection, orientation, cutoff, locality, and same-theory invariants; use Ward/cusp subtraction, Taylor Hessians, annular summation, interval arithmetic, and zero-pairing quotienting; transfer through centered flowed Wilson cumulants; and demote on any falsifier. The conceptual value signal is local and route-changing: R_{++}/kappa_4 becomes a valid annular sign/size certificate against L_+, while Clay existence, OS/Wightman axioms, nontriviality, observable density, large-field/topology control, OS spectral transfer, and mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and proof-search guide.`
- Rationale: The branch is blocked by sign/size certification of the connected boundary-OPE polarization, not by another abstract OS/Wilson restatement.
- Situation seed: Hypercubic SU(N) Wilson lattice with gradient-flow regulator, fixed physical H,K collar/hairpin endpoint boxes, centered plus-channel endpoint sheet currents, and dyadic annular decomposition of the Ward-subtracted C4 kernel.
- Varied variable: The flow-to-cell ratio lambda=sqrt(8t)/eta, with the annular starting scale J(lambda) chosen by the first shell outside the endpoint near box.
- Held-fixed controls: Same Wilson action, gauge group SU(N), and gradient-flow definition for pair, C4, counterterms, and recovery maps., Fixed H,K endpoint geometry, plus-current moment normalization M_{2,+}, and Schur-Feshbach leakage L_+., Outward-rounded interval arithmetic and the same zero-pairing quotient policy for all lambda., No continuum OS or mass-gap conclusion is inferred from a finite positive margin.
- Expected observation: A genuine endpoint mediator should show a stable positive Delta_R^-(lambda) plateau where the pair baseline dominates near constants, annular tails, recovery error, and higher cumulants; absence of such a plateau is a demotion signal.
- Transfer certificate needed: A cutoff-uniform same-theory interval proof for G_{++}^-, A_s, nu_s, H_{s,near}^+, E_rec^+, and E_{>=6}^+ before the intuition may enter proof obligations or a same-theory nontriviality witness discussion.

## Next Experiment

proof search: compute certified A_s, nu_s, H_{s,near}^+, and E_rec for the actual H,K endpoint cells in the flowed lattice regulator; report whether Delta_R^->0, Delta_R^-<=0, or the branch must quarantine. Include the validator-facing same-theory nontriviality witness boundary only after a cutoff-uniform connected cumulant witness is certified.

# Signed-Orbit Raw K4 Stress Witness for Post-H,K Endpoint Positivity

## Candidate Lemma

Finite signed-orbit stress lemma: in one heat-kernel regulated endpoint box, exact signed-orbit intervals for the raw connected K4 cumulant give a valid two-sparse falsifier for Schur-corrected endpoint positivity whenever the phase-separated off-diagonal lower amplitude dominates the two diagonal upper bounds.

## Definitions

- source object: finite SU(N) heat-kernel lattice Yang-Mills endpoint box with oriented plaquette sheets, endpoint labels p,q, Wilson weights, transported curvature insertions, and raw connected four-curvature cumulant intervals.
- target object: the two-dimensional Hermitian compression of the post-H,K Schur-corrected endpoint quadratic form on span{e_p,e_q}.
- controlled interface: signed-orbit raw plaquette recovery map sending exact Wilson-trace orbits of plaquette quadruples to interval enclosures for the connected cumulant witness U_{pq}.
- same-theory condition: all intervals use the same cutoff a, heat-kernel scale sigma, bare/renormalized coupling convention, reflection plane, endpoint Wilson basis, OPE subtraction, and H,K Schur block.
- connected cumulant witness: the finite object R_{pq}=cum_2(Q_p,Q_q) after vacuum and perimeter cancellations, decomposed into Gaussian color square, raw K4, OPE error, and Schur subtraction.
- carrier critique: scalar R is too weak, A012 shells are quarantined, OS Hilbert observable algebra and gauge-invariant observable density are too strong for this local finite gate, while raw plaquette enumeration is fragmented but valid.
- efficient representation: encode oriented plaquettes, sheet weights, heat-kernel transporters, color tensors, cumulant intervals, OPE intervals, endpoint indices, and Schur blocks; preserve gauge invariance, reflection support, Hermiticity, Gaussian/K4 separation, endpoint compression, same-theory normalization, and exact Wilson quotienting.

## Assumptions

- Model: finite-volume lattice SU(N) Yang-Mills with heat-kernel plaquette regulator and reflection plane fixed before taking any continuum limit.
- Cutoff: a>0 and sigma>0 are fixed; no volume-uniform, cutoff-uniform, or regulator-independent statement is claimed.
- Same-theory: Gaussian covariance, raw K4 cumulant intervals, OPE intervals, and S_HK are computed from the identical Wilson endpoint family and regulator.
- Validity: the orbit quotient group preserves oriented plaquette order, Wilson trace identities, transporter basepoints, color contraction tensors, and endpoint labels.
- Local: only the finite endpoint box after the worked H,K collar/hairpin construction is tested; OS reconstruction, excitation-sector cyclicity, and the Clay mass gap remain untouched.
- Constraint: interval arithmetic is outward-rounded and every quotient representative has a recovery certificate back to raw plaquette quadruples.

## Equations

- signed-orbit K4 interval: `I^{K_4}_{pq,\sigma}(\theta)=\frac{g_R^4}{16N^2}\sum_{O\in\mathcal O_{pq}} m_O W_O\chi_O(\theta) I^{\sigma}_O`. Valid when: Valid when the orbit quotient preserves Wilson trace identities, orientation signs, heat-kernel transporters, and the same cutoff cumulant intervals.
- phase-projected Schur-corrected interval: `I^{U}_{pq,\sigma}(\theta)=\operatorname{Re}(e^{-i\theta}G_{pq,\sigma})+I^{K_4}_{pq,\sigma}(\theta)+I^{E}_{pq,\sigma}(\theta)-\operatorname{Re}(e^{-i\theta}I^{S}_{pq,\sigma})`. Valid when: Applies after vacuum and perimeter cancellation and after Schur data are normalized in the identical endpoint Wilson basis.
- certified off-diagonal amplitude: `L_{pq,\sigma}(\theta)=\max\{0,-\sup I^{U}_{pq,\sigma}(\theta),\inf I^{U}_{pq,\sigma}(\theta)\}`. Valid when: Requires the projected interval to enclose every raw plaquette representative in the chosen phase sector.
- diagonal upper bounds: `D^{+}_{r,\sigma}=\sup I^{U}_{rr,\sigma},\qquad r\in\{p,q\}`. Valid when: Valid when diagonal endpoint intervals include Gaussian, K4, OPE, and Schur uncertainties with outward rounding.
- two-sparse Rayleigh falsifier: `L_{pq,\sigma}(\theta)^2>D^{+}_{p,\sigma}D^{+}_{q,\sigma}\;\Longrightarrow\;\exists x\in\operatorname{span}\{e_p,e_q\}:\ x^*U_\sigma x<0`. Valid when: Valid for the two-dimensional Hermitian endpoint compression when both diagonal upper bounds are nonnegative and the phase interval is sign-separated.

## Attempted Derivation

- Conceptual pressure attacked: the branch must turn boundary-OPE polarization R into an actual connected cumulant witness instead of repeating scalar R, A012 shell, or OS-density language.
- Declarative tension: Wilson/OPE coefficients, raw connected K4 intervals, OPE error, and S_HK must be valid in one cutoff theory, while continuum OS reconstruction, gauge-invariant observable density, excitation-sector cyclicity, nontriviality, and mass gap are non-claims.
- Expand endpoint Wilson observables into transported plaquette curvature fluxes Phi_i and subtract vacuum/perimeter terms; this leaves Gaussian crossed contractions, connected K4, and OPE error.
- Compress raw K4 by exact signed orbits under Wilson trace identities; each orbit contributes multiplicity m_O, geometric weight W_O, color tensor sign, phase projection chi_O(theta), and interval I_O^sigma.
- Assemble the phase-projected off-diagonal interval I^U_pq(theta) and diagonal upper intervals D_p^+,D_q^+ using the same Schur block S_HK.
- If I^U_pq(theta) is sign-separated with amplitude L and L^2>D_p^+D_q^+, choose the two-sparse vector aligned to theta; its Rayleigh quotient is at most 2 sqrt(D_p^+D_q^+)(sqrt(D_p^+D_q^+)-L)<0.
- Hard gate: a certified negative Rayleigh vector demotes the finite H,K endpoint route; survival of all signed-orbit stress tests changes the proof state only by forcing full Delta_raw PSD proof search.

Blocking gap: The actual same-regulator orbit intervals I_O^sigma for at least one endpoint pair p,q have not been computed or imported, so the stress inequality is a validator-facing theorem and recovery map rather than a completed H,K numerical/sign certificate.

## Falsifiers

- A quotient-audit falsifier: two plaquette quadruples placed in one signed orbit have different transported color tensors or different raw K4 intervals.
- A regulator falsifier: K4 intervals, OPE errors, and S_HK are computed with different smearing or coupling conventions, so same-theory normalization fails.
- A stress falsifier for the route: some certified p,q,theta has L_{pq}(theta)^2>D_p^+D_q^+, giving x_stress^*U_sigma x_stress<0 and killing endpoint PSD for this H,K geometry.
- A promotion falsifier: every two-sparse stress test survives but Delta_raw cannot be bounded below because missing off-block intervals destroy Loewner control.
- An overclaim falsifier: any attempt to infer gauge-invariant observable density, OS spectral transfer, or Clay mass gap from this finite endpoint certificate invalidates the branch claim.

## Learning

Cycle 322 refits the carrier rather than restating the obstruction ladder. Declarative tension: finite Wilson/OPE data, non-Gaussian raw K4, OPE error, and Schur hairpin energy must jointly control one endpoint quadratic form in one cutoff theory, but OS Hilbert observable algebra, gauge-invariant observable density, continuum existence, and mass gap are too strong and circular here. Carrier comparison: scalar R is representation-limited; A012 shells are convenient but quarantined; full Delta_raw search is complete but expensive; signed-orbit raw K4 intervals are the sharp negative tactic because a few recovered orbits can give a valid falsifier. Efficient representation must encode oriented plaquettes, sheet weights, transporters, color tensors, cumulant intervals, OPE intervals, endpoint indices, and Schur blocks; preserve gauge invariance, reflection support, Hermiticity, Gaussian/K4 separation, same-theory normalization, and exact Wilson quotienting; support cumulant contraction, phase interval summation, Rayleigh stress search, Loewner bounds, and Schur subtraction; transfer only through tau, Delta_raw, or x_stress. Conceptual value signal: sharp and route-changing at finite scope because it turns R into a connected cumulant witness with a concrete signed-orbit recovery map; success kills or promotes only the finite Route A endpoint-box gate, while every Clay frontier gate remains untouched.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch is looping unless the connected cumulant witness is tested on an actual same-regulator signed-orbit family; another abstract restatement of R or OS density would not change the proof state.
- Situation seed: Finite SU(3) heat-kernel lattice endpoint box for the worked H,K collar/hairpin geometry: choose the nearest nontrivial endpoint pair p,q whose sheets share one boundary-corner plaquette orbit and enumerate all oriented plaquette quadruple signed orbits contributing to K^{raw}_{pq,sigma}.
- Varied variable: The phase projection theta in Re(e^{-i theta}U_{pq}) while keeping the cutoff ratio sigma/a^2 fixed.
- Held-fixed controls: Gauge group SU(3), lattice spacing a, heat-kernel regulator sigma, and coupling convention g_R., The same endpoint Wilson basis, reflection plane, H,K Schur block, OPE subtraction rule, and exact Wilson quotient identities., Finite endpoint-box size and plaquette orientation convention; no continuum or volume limit is varied.
- Expected observation: Either one phase sector gives a sign-separated K4-dominated off-diagonal interval with L^2>D_p^+D_q^+, producing a finite falsifier, or all phases fail and the route must proceed to full Delta_raw interval PSD search.
- Transfer certificate needed: A validator-facing recovery certificate listing each signed orbit representative, multiplicity, color/geometric weight, raw cumulant interval, OPE interval, Schur interval, and exact reconstruction of I^U_{pq}(theta) in the same cutoff theory.

## Next Experiment

Proof search: compute the first same-regulator signed-orbit raw K4 interval table for one SU(3) H,K endpoint pair p,q, then evaluate I^U_pq(theta), D_p^+, D_q^+, and L_pq(theta) with outward-rounded interval arithmetic.

