# cycle-0320

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint-source interval gate for post-H,K reflected Wilson collapse

## Candidate Lemma

For the finite three-hairpin reflected Wilson block after the H,K Feshbach reduction, the remaining connected boundary-OPE polarization is validly represented by a source-equivalent endpoint interval; only positive null-channel endpoint leakage multiplied by negative connected cumulant data, plus a cutoff-uniform tail, can demote the block.

## Definitions

- source object: heat-kernel plaquette-sheet endpoint source data C_ep(a,L,eps) for the three reflected Wilson hairpins after H,K reduction, consisting of endpoint classes c, seven source values F_c(rh)=log Z_c(rh), cumulant intervals kappa_c, fractional incidences b_{ij,c}, color factor C_N, Gaussian margin M_G, and tail T_tail.
- target object: the finite post-H,K reflected-Wilson OS transfer scalar I_gate whose nonnegativity promotes this single Wilson block and whose certified negative interval is a same-theory finite falsifier.
- controlled interface: source-equivalent endpoint classes are contracted by signed null-channel incidence D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}, clipped only for one-sided danger, and exported as the scalar interval [I_-,I_+] without changing observables.
- same-theory condition: the source stencils are computed in the same heat-kernel Wilson lattice theory and the same gauge-invariant Wilson normalization as the collar Schwinger functions; no boundary counterterm, algebra enlargement, or endpoint renormalization is inserted.
- conceptual pressure: endpoint collapse must be sign-certified inside the same Wilson theory rather than hidden in symbolic R.
- declarative tension: collar reflection positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must jointly hold, but H,K and the half-overlap shield do not determine the scalar without a source cumulant mediator.
- carrier audit: raw R is representation-limited, raw kappa_4 spectra are too strong because they forget D_c signs, and global Schur-preimage positivity is valid but too coarse after H,K.
- efficient representation: encode endpoint classes, source stencils, cumulant intervals, signed incidences, C_N, M_G, and T_tail; preserve Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; allow source differentiation, interval arithmetic, source-equivalence, clipping, color multiplication, incidence contraction, and tail addition; identify carriers only by equal regulated source data; export only [I_-,I_+] to the finite OS gate.

## Assumptions

- Model: SU(N) heat-kernel lattice Yang-Mills with fundamental Wilson traces and reflection-positive plaquette measure before endpoint collapse.
- Regime: a fixed finite three-hairpin Route A block after the already-computed H,K Schur-Feshbach reduction; no continuum or mass-gap conclusion is claimed.
- Cutoff: the source-stencil error bounds, endpoint partition, and T_tail are uniform in lattice spacing for the chosen physical endpoint boxes.
- Same-theory: the recovery map from endpoint sources back to Wilson observables is the identity on the locked gauge-invariant Wilson algebra, modulo only source-equivalence by equal regulated data.
- Validity: Wick-square contractions have been separated as positive Gram terms, and straight f f commutator contacts cancel by the null incidence identity.
- Local: all non-endpoint, large-field, and topology leakage not represented by endpoint classes is charged to T_tail with an explicit interval budget.

## Equations

- seven_point_connected_cumulant_stencil: `\Delta^{(4)}_{h,7}F_c(0)=\frac{-F_c(-3h)+12F_c(-2h)-39F_c(-h)+56F_c(0)-39F_c(h)+12F_c(2h)-F_c(3h)}{6h^4}`. Valid when: Valid when F_c(s)=log Z_c(s) is the same-theory endpoint source free energy with eight bounded source derivatives on the stencil interval.
- cumulant_interval: `\kappa_c\in \Delta^{(4)}_{h,7}F_c(0)+[-7h^4M_{8,c}/240,\,7h^4M_{8,c}/240]`. Valid when: Applies after the heat-kernel endpoint source is fixed and M_{8,c} bounds the eighth derivative uniformly over the seven-point stencil.
- endpoint_gate_interval: `[I_-,I_+]=M_G+C_N\sum_c [D_c][\kappa_c]+[T_{\rm tail}],\quad D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}`. Valid when: Requires the H,K Feshbach reduction, source-equivalence aggregation after signed incidence summation, and a cutoff-uniform endpoint tail interval.
- one_sided_promotion_screen: `M_G>C_N\sum_c \overline{[D_c]_+}\,\overline{[-\kappa_c]_+}+\overline{[-T_{\rm tail}]_+}\Longrightarrow I_->0`. Valid when: Valid when interval endpoints dominate every same-theory endpoint source class and positive-D leakage is the only negative cumulant channel.
- fundamental_color_prefactor: `C_N=\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2`. Valid when: Applies after singlet projection of four endpoint flux insertions in the fundamental Wilson normalization used for the same reflected block.

## Attempted Derivation

- Start from the collar-limit finite OS matrix and apply the existing H,K Schur-Feshbach reduction; the remaining null-channel scalar is M_G plus a connected endpoint polarization and a tail.
- Represent the endpoint polarization by source derivatives of log Z_c, so disconnected Wick-square terms are removed by the logarithm and do not contribute to kappa_c.
- Use the previously isolated cancellation: straight nonabelian f f contact terms vanish in the null incidence channel, leaving endpoint classes and T_tail.
- Aggregate endpoint boxes only by equality of regulated source stencils; then sum signed incidences before multiplying by cumulant intervals, preventing the raw-kappa_4 overestimate.
- Derive the interval [I_-,I_+]=M_G+C_N sum_c [D_c][kappa_c]+[T_tail] and the one-sided safety screen using only positive-D leakage against negative cumulants.
- Insert the heat-kernel Haar-Jacobian expansion to obtain the root-quartic cap [-kappa_c]_+ <= t_c^4 R_4(L_c)/60+|E_c| as an analytic pre-screen for the validator stencil.

Blocking gap: The actual endpoint source classes, fractional incidences, seven source values, M_8 bounds, and cutoff-uniform T_tail have not been computed for the locked three-hairpin geometry.

## Falsifiers

- A same-theory endpoint class with D_c>0 and a certified negative cumulant interval large enough that I_+<0 is a finite reflected-Wilson falsifier.
- The seven source values of log Z_c require a boundary counterterm or changed Wilson normalization; then the carrier is not same-theory even if the interval is positive.
- The tail T_tail has nonuniform cutoff growth from large-field or topology sectors, invalidating the finite endpoint export to the OS gate.
- Source-equivalence aggregation before signed incidence summation changes D_c and can create a spurious promotion; this is a representation falsifier.
- A stress case with b_{12,c} dominant and b_{13,c}+b_{23,c}<b_{12,c}/2 tests whether the half-overlap shield is genuinely absent rather than assumed.

## Learning

Cycle 320 attacks the conceptual pressure of endpoint collapse in the same Wilson theory. The declarative tension is collar OS positivity plus fixed gauge-invariant Wilson observables plus singular connected endpoint OPE without a boundary theory. The new finite contribution is a validator-facing clipped source interval with a root-quartic analytic screen: raw R is too weak, raw kappa_4 spectra are too strong, and the global Schur-preimage route is valid but too coarse after H,K. The hard gate is the finite post-H,K reflected-Wilson OS transfer scalar. Success promotes only this block; failure gives a finite same-theory falsifier; missing source or tail data keeps quarantine. The conceptual value signal is sharpness and route change at finite scope: negative SU(N) endpoint cumulants are not themselves the obstruction; positive-D leakage times connected cumulants plus uniform tail is. Clay continuum construction, nontriviality, full OS/Wightman reconstruction, and positive mass gap remain non-claimed.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe and validator-facing endpoint-stencil design.`
- Rationale: The branch has exhausted abstract OS-closure and H,K threshold work; the only remaining finite obstruction is the connected endpoint cumulant witness multiplied by signed incidence, so another abstract restatement would not change the proof state.
- Situation seed: In SU(N) heat-kernel lattice Yang-Mills, take the locked three reflected Wilson hairpins after H,K reduction and partition each collapsing endpoint into source-equivalent boxes with the same seven-point log Z_c stencil.
- Varied variable: The fractional endpoint dominance alpha_c=b_{12,c}/(b_{12,c}+b_{13,c}+b_{23,c}) for one source class, varied through the half-overlap threshold while keeping the source direction L_c fixed.
- Held-fixed controls: Gauge group SU(N), fundamental Wilson trace normalization, heat-kernel plaquette-sheet regulator, and reflection-positive lattice measure., The same three Wilson hairpins, the H,K null vector, the Gaussian margin M_G, and the straight f f null-incidence cancellation., No boundary counterterm, no algebra enlargement, no changed recovery map, and all non-endpoint leakage charged to a cutoff-uniform T_tail.
- Expected observation: For alpha_c at or below the half-overlap shield the negative root-quartic cumulant is protective or cancels; above it, the connected cumulant witness can lower I_gate, and a certified negative interval becomes a finite same-theory falsifier.
- Transfer certificate needed: A source-equivalence table, seven same-theory log Z_c values or analytic kappa_c intervals, a uniform M_8/remainder bound, signed incidence intervals, and a cutoff-uniform large-field/topology tail before the thought experiment may affect proof obligations.

## Next Experiment

Proof search plus endpoint data: build the validator-facing connected cumulant witness table for the locked heat-kernel three-hairpin endpoints, evaluate seven log Z_c stencil values or root-quartic intervals, compute signed D_c after source-equivalence, add a uniform T_tail, and decide I_gate; if data remain unavailable, keep the branch quarantined rather than adding another abstraction.

# Gauge-Invariant Nontriviality Witness Selection -> finite endpoint R certificate

## Candidate Lemma

For the H,K plus-channel endpoint boxes, the far-annular part of the connected boundary-OPE polarization is bounded by a finite dyadic sum plus an explicit geometric tail. Hence R_{++}^{ren}-L_+ has a valid finite sign test once the near annuli and recovery errors are interval-certified.

## Definitions

- source object: finite-cutoff SU(N) Wilson lattice Yang-Mills on a reflected four-torus, with gradient-flowed, centered, perimeter/cusp-renormalized plus-hairpin sheet currents J_+ supported in the H,K endpoint cells.
- target object: the finite Schur-Feshbach endpoint-box positivity margin Delta_R for the H,K plus channel; this is not the continuum OS Hamiltonian mass gap.
- controlled interface: the carrier map J_+ -> R_{++}^{ren} sends endpoint sheet currents to the connected flowed Wilson cumulant by a positive pair contraction plus Ward-subtracted connected C4 sector kernels.
- same-theory condition: the Wilson action, coupling, flow time, counterterms, endpoint cells, and recovery map are shared by the pair term, C4 sectors, and Schur-Feshbach leakage L_+; no external spectral measure witness is substituted.
- preserved observables: centered flowed Wilson hairpins W_t^{ren}(J_+) and their gauge-invariant connected cumulant witness values.
- representation morphism: raw reflected Wilson contour -> oriented sheet current -> endpoint moment vector -> sector-kernel interval scalar.
- invariants: gauge invariance, color trace normalization, reflection sign, sheet orientation, endpoint locality, cutoff label, and same-theory identity.

## Assumptions

- Model: SU(N) Wilson lattice gauge theory at finite volume and cutoff a, with Wilson action and gradient flow time t satisfying t >= c_t a^2.
- Regime: endpoint cell radius eta, annular split rho_0, and flow time obey a << eta <= rho_0/4 and rho_0^2/t is explicitly recorded.
- Cutoff: the claimed theorem is finite-regulator unless all heat-kernel constants, recovery errors, and interval widths are shown uniform as a -> 0.
- Same-theory: W_t^{ren}, the pair covariance, C4 kernels, cusp counterterms, and L_+ are computed from the same regulated measure and normalization.
- Constraint: the plus endpoint current has vanishing monopole and dipole moments after Ward/cusp subtraction; otherwise the Hessian reduction is invalid.
- Local: the proof uses only endpoint boxes after the finite H,K reduction and does not claim OS positivity, observable density, or a Hamiltonian spectral gap.

## Equations

- lower_R_interval: `R_{++}^{ren} \ge g_t^4 (N^2-1)\bigl(2G_{++}^{-}-N C_{4,++}^{maj}\bigr)-E_{6}^{+}-E_{rec}^{+}`. Valid when: Valid when the centered flowed hairpins use the same Wilson action, flow time, endpoint cells, and cusp subtraction.
- ward_hessian_majorant: `C_{4,++}^{maj}\le {M_{2,+}^2\over 4}\sum_{s\in\{3g,4g,ct,end\}}\bigl(C_s^{near}(\rho_0,t)+C_s^{far}(\rho_0,t)\bigr)`. Valid when: Applies after Ward and cusp subtraction and after plus-channel monopole and dipole moments vanish.
- dyadic_far_tail: `C_s^{far}\le A_s t^{-6}\left[\sum_{j=0}^{J-1}16^j e^{-4^j\rho_0^2/(32t)}+{16^J e^{-4^J\rho_0^2/(32t)}\over 1-q_J}\right],\quad q_J=16e^{-3\cdot4^J\rho_0^2/(32t)}<1`. Valid when: Requires a flowed sector-kernel mixed-Hessian heat bound on every annulus outside the endpoint core.
- promotion_margin: `\Delta_R:=g_t^4 (N^2-1)\bigl(2G_{++}^{-}-N C_{4,++}^{maj}\bigr)-E_6^{+}-E_{rec}^{+}-L_+`. Valid when: Valid in the finite H,K plus basis where L_+ is the Schur-Feshbach leakage scalar.
- endpoint_gate: `\Delta_R>0\ \Longrightarrow\ Q_{+}^{ren}=Q_{+}^{bare}+R_{++}^{ren}>0`. Valid when: Requires the same finite Schur-Feshbach decomposition and no change of endpoint observable algebra.

## Attempted Derivation

- Conceptual pressure attacked: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator, while positive flowed pair covariance can be erased by connected C4 polarization.
- Hard gate: finite endpoint-box positivity after H,K. Success promotes one finite Route A gate; failure quarantines the R repair without touching Clay existence or mass gap gates.
- Fix SU(N) Wilson lattice Yang-Mills, gradient flow time t, endpoint cell radius eta, annular split rho_0, and reflected H,K plus hairpin current J_+.
- Use centered flowed Wilson observables and subtract disconnected products plus one-hairpin perimeter/cusp counterterms; this isolates R_{++}^{ren}=kappa_2(W_+^{ren},W_+^{ren}).
- The g_t^4 pair contraction contributes the positive scalar 2(N^2-1)G_{++}; this is a same-theory gauge-invariant connected cumulant witness only at finite scope.
- The connected four-curvature part is decomposed into sector kernels s in {3g,4g,ct,end} with color factor N(N^2-1), then Ward-subtracted.
- Plus-channel endpoint-current symmetry gives zero monopole and dipole moments, so each C4 sector integral is controlled by a mixed Hessian times M_{2,+}^2/4.
- On annulus A_j={2^j rho_0 <= |z| <= 2^{j+1} rho_0}, the flowed heat-kernel Hessian envelope gives a_j <= A_s t^{-6}16^j exp(-4^j rho_0^2/(32t)).
- The ratio a_{j+1}/a_j <= q_j=16 exp(-3*4^j rho_0^2/(32t)); if q_J<1, the infinite far tail is bounded by the first omitted term divided by 1-q_J.
- Insert near-core interval upper bounds, far-tail constants, E_6^{+}, E_rec^{+}, and L_+ into Delta_R. A positive lower interval proves the finite endpoint-box repair; a nonpositive interval is a valid falsifier.

Blocking gap: The missing proof objects are certified sector constants A_s, near-core outward-rounded intervals, and recovery errors for the chosen regulator window. Without them Delta_R is a formula, not yet a proved sign certificate.

## Falsifiers

- falsifier: plus-channel endpoint currents fail the zero monopole or dipole moment test after recovery from raw Wilson contours.
- falsifier: Ward or cusp subtraction leaves an uncancelled logarithmic near-core term not absorbed by the stated counterterms.
- falsifier: the dyadic tail ratio q_J is not below one in the chosen rho_0^2/t window.
- falsifier: connected C4 sector intervals dominate the positive pair baseline so that the certified Delta_R lower bound is <= 0.
- falsifier: zero-pairing quotienting changes gauge, color, reflection, orientation, or endpoint locality data beyond E_rec^{+}.
- falsifier: the regulator plateau is absent, so the finite computation cannot be treated as same-theory support for the continuum candidate.
- stress case: shrink rho_0 toward the flow radius; the near interval should widen and demote if the cusp cancellation is not real.
- stress case: enlarge rho_0; the far tail should decay geometrically while the near quadrature burden grows, exposing the optimal split.

## Learning

Cycle 320 adds a concrete computation layer: the far connected C4 polarization is not just a sector constant but a dyadic annular tail with explicit ratio q_J and finite remainder. Declarative tension: Schur-Feshbach endpoint positivity, positive same-theory flowed Wilson pair covariance, and recovery from raw contours must jointly be valid, but connected C4 can erase the mediator. Raw Wilson contours remain fragmented; endpoint sheet currents are efficient only with recovery errors, Ward/cusp cancellation, moment cancellation, interval arithmetic, and zero-pairing guards. Conceptual value signal: R_{++}/kappa_4 becomes a route-deciding annular sign/size certificate, not a symbolic boundary-OPE term. The only changed hard gate is finite endpoint-box positivity after H,K; all Clay target commitments remain frozen and unclaimed.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and proof-search guide.`
- Rationale: The branch is no longer helped by restating Wilson/OS obstructions. The decisive unknown is the sign and size of the same-theory connected boundary-OPE polarization R_{++} after H,K, and the annular constants are the first finite calculable obstruction.
- Situation seed: Finite SU(2) Wilson lattice Yang-Mills on a reflected four-torus with two recovered plus-hairpin endpoint sheet currents in the H,K collar boxes, gradient flow t, cell radius eta, fixed Schur-Feshbach leakage L_+, and centered flowed Wilson cumulant R_{++}^{ren}.
- Varied variable: u=rho_0^2/t, the annular split in flow units.
- Held-fixed controls: Wilson lattice action, group SU(2), volume, cutoff a, and bare coupling used for every cumulant., The H,K plus-channel geometry, reflection orientation, endpoint current recovery map, and zero-pairing quotient policy., The same perimeter/cusp counterterms and gradient-flow normalization for pair and C4 sectors., The finite Schur-Feshbach leakage scalar L_+ and the target claim level: finite endpoint-box positivity only.
- Expected observation: A valid route should show a stable window of u where the far tail decreases geometrically, the near interval remains plateau-stable, and the lower margin Delta_R is either certified positive or decisively nonpositive. A sign change under harmless u variation is a demotion signal.
- Transfer certificate needed: Before the intuition affects proof obligations, provide outward-rounded near-sector intervals, certified A_s heat-kernel Hessian constants, q_J<1 tail proof, same-theory recovery error E_rec^{+}, and a statement that this is support for a connected cumulant witness, not an OS spectral measure witness or mass-gap proof.

## Next Experiment

Route to proof search: implement the SU(2) H,K plus-channel annular split, compute certified A_s and near-core intervals for the centered flowed Wilson connected cumulant witness, record same-theory nontriviality witness status as support-only, and demote if Delta_R is not strictly positive.

# Gauge-Invariant Observable Density In The Excitation Sector -> raw K4 endpoint witness

## Candidate Lemma

Finite signed-orbit raw K4 stress lemma: in one heat-kernel cutoff theory, a Schur-corrected two-endpoint principal block is falsified if a phase-aligned lower interval for the connected four-plaquette cumulant beats the diagonal Gaussian-Schur-OPE upper product.

## Definitions

- source object: finite heat-kernel regulated SU(N) lattice Yang-Mills endpoint box with oriented plaquettes, transported plaquette Lie algebra coordinates X_p, Wilson sheet weights, and vacuum normal ordering at smearing sigma.
- target object: finite Hermitian Schur-corrected endpoint matrix U_sigma=R_sigma-S_HK on the post-H,K endpoint span, before any OS Hilbert spectral transfer.
- controlled interface: raw plaquette connected cumulant witness recovery map from transported plaquette quadruple intervals and OPE intervals to phase-resolved principal-block interval bounds for U_sigma.
- same-theory condition: the Gaussian covariance, connected K4 intervals, OPE remainder, Wilson endpoint basis, H,K Schur block, coupling convention, cutoff a, finite volume Lambda, and smearing sigma are all taken from the same regulated Yang-Mills measure.
- bridge carrier: quotient of oriented plaquette quadruples by exact Wilson trace identities, reflection labels, endpoint sheet labels, color tensors, and transporter paths.
- declarative tension: finite Wilson/OPE coefficients, connected K4 negativity, OPE error, and S_HK must jointly control one endpoint quadratic form, while gauge-invariant observable density, OS reconstruction, continuum existence, and the Hamiltonian mass gap remain non-claims.
- carrier critique: scalar R is too weak, OS Hilbert observable algebra is too strong and circular for this local gate, A012 shells are convenient but quarantined, and raw plaquette enumeration is fragmented but valid.

## Assumptions

- Model: SU(N) heat-kernel lattice Yang-Mills on a finite reflection-symmetric box Lambda with fixed cutoff a and smearing sigma.
- Cutoff: all plaquette cumulants and Schur blocks are evaluated before taking a continuum or infinite-volume limit.
- Same-theory: the endpoint Wilson observables, H,K hairpin block, covariance C_sigma, K4 cumulants, and OPE errors use the identical regulator and coupling normalization.
- Local: only the finite post-H,K endpoint box and its transported plaquette sheets are considered.
- Validity: quotienting is allowed only by exact Wilson trace, orientation, color, and reflection identities verified in the cutoff theory.
- Constraint: the conclusion is a finite falsifier for endpoint positivity, not a proof or disproof of the Clay mass gap.

## Equations

- transported plaquette flux: `\Phi_i^a=\sum_{p\in S_i} w_i(p)\,\mathrm{Ad}(U_{\gamma_{p\to v_i}})^{ab}X_p^b`. Valid when: Valid when the endpoint sheet S_i, transporter paths, weights, and heat-kernel plaquette coordinates are fixed in the same cutoff box.
- normal ordered endpoint observable: `Q_i=:\Phi_i^a\Phi_i^a:_\sigma`. Valid when: Valid when vacuum normal ordering is performed with the same heat-kernel regulated expectation used for all cumulants.
- connected boundary polarization decomposition: `R_{ij,\sigma}=\operatorname{cum}_2(Q_i,Q_j)=\alpha_N g_R^4\sum_{p,q}W_{ij}(p,q)C_\sigma(p,q)^2+\frac{g_R^4}{16N^2}K^{(4)}_{ij,\sigma}+E^{\mathrm{OPE}}_{ij,\sigma},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid after disconnected vacuum and perimeter terms cancel under same-regulator normal ordering and the Wilson OPE is truncated with a recorded error interval.
- signed orbit K4 interval enclosure: `\mathcal K^{(4)}_{ij,\sigma}:=\sum_{O\in\mathcal O_{ij}}m_O\chi_O I_O(\sigma)\ni K^{(4)}_{ij,\sigma}`. Valid when: Valid when every plaquette quadruple contributing to K4 is assigned to an exact Wilson-invariant orbit with certified representative interval I_O.
- two sparse stress falsifier: `L_{pq}(\theta)=\underline{\Re(e^{i\theta}U_{pq,\sigma})},\quad D_r^+=\overline{U_{rr,\sigma}},\quad L_{pq}(\theta)^2>D_p^+D_q^+\Rightarrow U_\sigma\not\succeq0`. Valid when: Valid for a Hermitian interval enclosure of the same Schur-corrected endpoint matrix with positive diagonal upper bounds D_p^+ and D_q^+.

## Attempted Derivation

- Conceptual pressure attacked: replace repeated phase-stress abstraction by a validator-facing raw K4 signed-orbit interval computation for the connected boundary-OPE polarization R.
- Start from the same-regulator endpoint observable Q_i=:Phi_i^2:_sigma so vacuum one-point and perimeter pieces cancel inside cum_2(Q_i,Q_j).
- Separate the Gaussian crossed contraction, giving the PSD color square alpha_N g_R^4(C_sigma o C_sigma), from the connected four-plaquette cumulant K4 and the OPE interval.
- Enumerate oriented plaquette quadruples contributing to K4; retain transporter paths, endpoint labels, orientation signs, and color tensors before quotienting.
- Quotient only by exact Wilson identities and reflection symmetries, producing signed orbits O with multiplicities m_O and representative intervals I_O.
- Recover phase lower bounds L_pq(theta) and diagonal upper bounds D_p^+ from the Gaussian square, signed K4 intervals, OPE error, and S_HK subtraction in the same cutoff theory.
- Apply the 2x2 Rayleigh determinant test: L_pq(theta)^2>D_p^+D_q^+ gives a concrete stress vector and falsifies endpoint PSD for this H,K geometry.

Blocking gap: The raw representative intervals I_O(sigma) for the first nearest reflected plaquette quadruple orbits have not yet been computed from heat-kernel character bounds or direct finite integration.

## Falsifiers

- A same-regulator K4 interval table yields L_pq(theta)^2>D_p^+D_q^+ for some endpoint pair, producing a finite falsifier for post-H,K endpoint positivity.
- The orbit quotient fails Hermiticity or changes transporter homotopy, invalidating the signed-orbit recovery map.
- The OPE interval or Schur hairpin uncertainty dominates every phase lower bound, forcing quarantine of the two-sparse negative tactic.
- The raw K4 intervals are regulator-mismatched with the Gaussian covariance or S_HK data, making the certificate invalid.
- All two-sparse stress tests survive but Delta_raw has an independent negative eigenvector, showing the phase-stress route was incomplete but not wrong.

## Learning

Cycle 320 attacks the conceptual pressure that R must become an actual connected cumulant witness, not scalar rhetoric or OS-density language. Declarative tension: Wilson/OPE data, raw K4, OPE error, and S_HK must be valid in one cutoff theory, but Clay-level OS reconstruction, gauge-invariant observable density, excitation-sector cyclicity, continuum existence, and mass gap are barred. Current carrier revision: scalar R is too weak; OS Hilbert observable algebra is too strong and circular for this local gate; A012 shells are convenient but quarantined; raw plaquette enumeration is fragmented yet valid. Compared with full Delta_raw search, signed-orbit K4 intervals give the first calculable negative tactic because a few representative cumulant intervals can falsify endpoint PSD. Efficient representation requirements are now concrete: encode oriented plaquettes, sheet weights, heat-kernel transporters, color tensors, cumulant intervals, OPE intervals, endpoint indices, and Schur blocks; preserve gauge invariance, reflection support, Gaussian/K4 separation, endpoint compression, same-theory normalization, Hermiticity, and exact Wilson quotienting; support cumulant contraction, phase interval summation, Rayleigh stress search, Loewner bounds, and Schur subtraction; use a finite endpoint-box complexity budget; transfer only through tau, Delta_raw, or x_stress; expose a falsifier by negative margin, missing intervals, non-invariant quotienting, or regulator mismatch. Conceptual value signal: sharp and route-changing at finite scope because the hard gate L_pq(theta)^2>D_p^+D_q^+ decides whether the worked H,K endpoint route is killed or must proceed to full Delta_raw search, while every Clay frontier gate remains untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the finite H,K endpoint route.`
- Rationale: The branch is looping unless the connected cumulant witness is converted into raw same-regulator K4 intervals; varying an actual regulator parameter tests whether sign-coherent plaquette orbits can dominate the Schur-corrected diagonal budget.
- Situation seed: Finite SU(N) heat-kernel lattice Yang-Mills endpoint box with the worked H,K collar/hairpin Wilson sheets, transported plaquette fluxes, exact Wilson quotient table, and a two-endpoint phase-stress pair (p,q).
- Varied variable: rho=sigma/a^2, the heat-kernel smearing time in cutoff units.
- Held-fixed controls: Gauge group SU(N), finite H,K endpoint geometry, and endpoint Wilson basis., Same cutoff a, finite volume Lambda, coupling convention g_R, and vacuum normal ordering., Exact Wilson trace/reflection quotient rules and the H,K Schur block S_HK., OPE truncation order and interval arithmetic policy.
- Expected observation: For small-to-moderate rho the nearest reflected plaquette quadruple orbits either show phase-coherent K4 intervals large enough to violate L_pq^2<=D_p^+D_q^+, or they remain too wide/small and force full Delta_raw proof search.
- Transfer certificate needed: A rigorous same-regulator interval table for representative K4 orbits, an OPE error interval, and a Hermitian quotient audit before the observation may affect finite proof obligations.

## Next Experiment

Proof search: compute the first same-regulator signed-orbit intervals I_O for nearest reflected plaquette quadruples in the H,K endpoint box, then evaluate the connected cumulant witness inequality L_pq(theta)^2>D_p^+D_q^+ with the Hermitian quotient audit attached.

