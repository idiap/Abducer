# cycle-0275

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint-incidence source intervals for the post-H,K Wilson gate

## Candidate Lemma

For the first three-hairpin block after H,K are fixed, the heat-kernel endpoint contribution to the corrected Schur-Feshbach null scalar is dangerous only through clipped positive endpoint dominance D_v^+. In binary endpoint incidence, the only negative-kappa_4 demotion channel is a certified 12-only endpoint box; all boxes touching 13 or 23 enter the protective side or cancel. This is a finite same-theory Wilson gate, not a Clay mass-gap claim.

## Definitions

- source object: regulated SU(N) heat-kernel plaquette-sheet endpoint boxes v for the locked reflected Wilson hairpins, with same-theory source functions Z_v(s) and pair incidences b_{v,ij}.
- target object: the finite post-H,K Feshbach null-channel scalar I_gate whose nonnegative certified interval promotes this Wilson block through the same-theory OS transfer gate.
- controlled interface: the endpoint source-interval carrier (beta_v,b_{v,ij},C_N,T_tail) maps connected boundary-OPE data to an interval for the scalar polarization entering the finite Schur-Feshbach gate.
- same-theory condition: Wilson loop observables, color traces, heat-kernel regulator, reflection map, diagonal normalization, and recovery maps are fixed across collar collapse; no boundary counterterm, gauge-fixed replacement, or enlarged observable algebra is allowed.
- bridge/carrier: beta_v=-kappa_{4,v}^{sing}>=0 records the magnitude of the singlet connected endpoint fourth cumulant obtained from log Z_v; b_{v,ij} records the regulated endpoint overlap of pair (i,j).
- hard gate changed: the finite post-H,K reflected-Wilson OS transfer gate is promoted if I_gate has a nonnegative interval and demoted by a negative interval falsifier.
- Clay boundary: continuum existence, regulator-independent Schwinger functions, full OS/Wightman reconstruction, nontriviality, and positive Hamiltonian mass gap remain untouched.

## Assumptions

- Model/regime: four-dimensional lattice SU(N) Yang-Mills with heat-kernel plaquette action at cutoff a and finite volume L; the statement is finite-regulator and finite-volume unless uniform bounds are separately proved.
- Regulator obligation: endpoint boxes have side ell with a<<ell below the collar scale, and all overlap not assigned to boxes is charged to T_tail with a cutoff-uniform bound.
- Same-theory observable assumption: the Wilson hairpin observables are gauge-invariant traces in the locked algebra, and the endpoint source differentiation is a recovery map for the same observables, not an auxiliary boundary theory.
- Cancellation assumption: disconnected Wick-square contractions are handled as positive Gram terms, and the straight-segment C_A f f contact cancels under the already fixed Feshbach null incidence.
- Sign assumption: beta_v is an interval-certified nonnegative magnitude of the local compact-group connected fourth cumulant; if the interval includes positive kappa_4, this lemma becomes only a signed interval test.
- Uniformity/advice boundary: no imported RG package result is used as a full frontier discharge; large-field and topological summability remain external obligations.

## Equations

- endpoint_R_decomposition: `R_{end}=C_N\sum_v \kappa^{sing}_{4,v}\,D_v+T_{tail},\quad C_N=\frac{g_a^4}{4}\left(\frac{T_F}{N}\right)^2,\quad D_v=2b_{v,12}-4b_{v,13}-4b_{v,23}.`. Valid when: Valid when heat-kernel endpoint boxes localize the connected four-flux cumulant after Wick-square and straight-contact cancellations.
- binary_incidence_table: `D_v(S)=2{\bf 1}_{12\in S}-4{\bf 1}_{13\in S}-4{\bf 1}_{23\in S}\in\{0,2,-4,-4,-2,-2,-8,-6\}.`. Valid when: Applies when endpoint overlap incidence is binary for the three pair footprints within each regulated endpoint box.
- clipped_lower_bound: `I_{gate}\ge M_G-C_N\sum_v \beta_v[D_v]_+-T_{tail}^{+},\quad \beta_v=-\kappa^{sing}_{4,v}\ge0.`. Valid when: Valid when the endpoint fourth cumulants are nonpositive and all unlocalized contributions are bounded above by T_tail^+.
- interval_promotion_test: `I_-:=M_G^- - C_N^+\sum_v \beta_v^+[D_v^+]_+-T_{tail}^+\ge0\ \Longrightarrow\ \text{finite block promoted}.`. Valid when: Requires certified intervals for the Gaussian margin, color factor, endpoint cumulants, incidences, and tail in the same regulator.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: regulated SU(N) heat-kernel plaquette-sheet endpoint boxes v for the locked reflected Wilson hairpins, with same-theory source functions Z_v(s) and pair incidences b_{v,ij}.; target object: the finite post-H,K Feshbach null-channel scalar I_gate whose nonnegative certified interval promotes this Wilson block through the same-theory OS transfer gate.; Model/regime: four-dimensional lattice SU(N) Yang-Mills with heat-kernel plaquette action at cutoff a and finite volume L; the statement is finite-regulator and finite-volume unless uniform bounds are separately proved..
- Conceptual pressure attacked: endpoint collapse must be sign-certified in the same Wilson theory after H,K, without reverting to a raw symbolic R or a raw kappa_4 spectrum.
- Declarative tension: collar reflection positivity gives a finite positive matrix, the locked gauge-invariant Wilson algebra must stay unchanged, and the boundary OPE is singular at endpoints; the missing mediator is a signed, cutoff-aware endpoint source carrier.
- Freeze the Clay target: this cycle claims only a finite regulated Wilson endpoint gate; it does not construct continuum Yang-Mills, OS/Wightman fields, nontriviality, or a Hamiltonian mass gap.
- Use the heat-kernel plaquette-sheet regulator and decompose the connected boundary-OPE polarization into endpoint boxes plus T_tail.
- Use connected log Z_v to isolate the singlet connected four-flux cumulant; disconnected Wick-square terms are positive Gram contributions and are not the dangerous negative endpoint term.
- Use the already fixed null-channel incidence to cancel the straight C_A f f contact on shared straight boundary segments.
- Insert the Feshbach null pair weights (2,-4,-4) into the endpoint overlap variables b_{v,ij}, producing D_v=2b_{12}-4b_{13}-4b_{23}.
- For binary endpoint incidence, compute the table D_v(S) for S subset {12,13,23}; only S={12} gives positive D_v and hence only this class can turn negative kappa_4 into a demoting contribution.
- Replace kappa_{4,v}^{sing} by -beta_v with beta_v>=0 and bound unresolved nonlocal/corner effects by T_tail^+ to get the interval lower bound I_-.
- Compare endpoint carrier against alternatives: a global Schur-preimage test is exact but too coarse after H,K; formal OPE language is too weak; raw kappa_4 spectrum is too strong because it ignores incidence signs. The clipped source carrier is the efficient local representation.

Blocking gap: Actual endpoint-box incidence intervals b_{v,ij}, beta_v source intervals, and T_tail^+ have not yet been computed for the geometric Wilson hairpins; without them I_gate is a formula, not a numerical certificate.

## Falsifiers

- A same-theory source computation gives I_+<0; this is a finite post-H,K Wilson falsifier of the proposed OS transfer for the block.
- The endpoint tail T_tail is not cutoff-uniform or absorbs an unbounded topological/large-field contribution.
- The heat-kernel source derivative requires a boundary counterterm or an enlarged observable algebra, violating the same-theory condition.
- The straight C_A f f cancellation fails for the actual hairpin endpoint geometry or orientation.
- Endpoint incidence is not binary and interval leakage permits b_{12}>2(b_{13}+b_{23}) in boxes not classified as 12-only.
- The connected fourth cumulant has an uncertified sign or a positive component that invalidates the clipped negative-kappa_4 bound.
- The recovery map from endpoint sources to Wilson observables is not injective on the finite data used by the gate.

## Learning

Cycle 275 makes the endpoint carrier sharper than the previous raw clipped-interval slogan. The sign-relevant computation is the incidence table D_v(S): with binary endpoint boxes, negative compact-group kappa_4 can demote the finite Wilson block only in 12-only boxes; any endpoint touching 13 or 23 is protective or cancels after the valid null-channel contractions. The hard gate is the finite post-H,K reflected-Wilson OS transfer gate: success gives a finite same-theory promotion certificate for this block, while failure gives a concrete falsifier. The conceptual value signal is sharpness and route change: the obstruction is not kappa_4 negativity, but kappa_4 negativity multiplied by certified positive endpoint dominance plus a controlled tail. Efficient representation requirements are now fixed: encode endpoint boxes, source stencils, beta intervals, b/D incidence intervals, color factor C_N, Gaussian margin M_G, and T_tail; preserve Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; use source differentiation, interval arithmetic, clipping, incidence contraction, and tail addition; identify equivalent carriers only by equal regulated source data; export only [I_-,I_+] to the finite OS gate. Larger Clay gates remain untouched and explicitly non-claimed.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the post-H,K endpoint gate.`
- Rationale: The branch is past the finite Schur-Feshbach theorem and the first H,K hairpin case; the only contribution-making move left here is to compute or falsify the endpoint R/kappa_4 term in the actual regulated Wilson input.
- Situation seed: Three reflected Wilson hairpins in the SU(N) heat-kernel plaquette-sheet regulator, with endpoint boxes labeled by which pair footprints {12,13,23} they intersect and source functions Z_v(s) for the singlet endpoint flux.
- Varied variable: Endpoint leakage parameter theta in b_{v,13}=b_{v,23}=theta for a nominal 12-only endpoint box, with b_{v,12}=1 fixed.
- Held-fixed controls: The H,K finite block and Feshbach null vector are held fixed., The heat-kernel plaquette-sheet regulator, color normalization, and Wilson trace observables are held fixed., No boundary counterterm, gauge fixing, or observable-algebra enlargement is allowed., The Wick-square Gram positivity and straight f f null-incidence cancellation are assumed exactly as in the finite derivation.
- Expected observation: D_v=2-8theta crosses from dangerous to safe at theta=1/4; if actual endpoint smearing forces theta>=1/4, negative compact-group kappa_4 cannot demote through that box, while theta<1/4 requires a quantitative beta_v and tail comparison.
- Transfer certificate needed: A cutoff-uniform endpoint OPE/recovery certificate proving the incidence intervals and source-derivative beta_v values are valid for the same regulated Wilson observables before the scalar interval is allowed to affect the OS proof queue.

## Next Experiment

Construct the actual endpoint incidence table for the three reflected hairpin footprints: list each endpoint box v, compute intervals for b_{v,12}, b_{v,13}, b_{v,23}, evaluate D_v^+, then attach beta_v source-stencil intervals and T_tail^+ to decide the sign of I_gate.

# Post-HK endpoint-box R/kappa4 Hessian certificate

## Candidate Lemma

Endpoint-moment Hessian certificate: for the first explicit H,K plus-channel endpoint hairpin, the connected boundary-OPE polarization R_{++}^{ren} is bounded below by the positive flowed pair baseline minus a Ward-subtracted four-curvature Hessian remainder. If this interval lower bound exceeds the finite Schur-Feshbach leakage L_+, the post-H,K endpoint-box gate is promoted; if not, the R repair is falsified locally.

## Definitions

- source object: finite-volume hypercubic Wilson SU(N) Yang-Mills measure with lattice spacing a, bare coupling g0(a), gradient-flow time t, and centered renormalized thin Wilson hairpin observables W_t(J_i) represented by oriented sheet currents J_i plus endpoint currents e_i.
- target object: the finite-dimensional Schur-Feshbach endpoint-box positivity certificate R_{++}^{ren}/kappa_4 > L_+ for the already extracted H,K plus channel; it is a finite Wilson-calculus gate, not the Clay mass-gap theorem.
- controlled interface: the carrier map sends each H,K Wilson collar or hairpin to a gauge-invariant flowed sheet-current cumulant, preserving color trace, reflection parity, orientation signs, endpoint boxes, and the same Feshbach coordinates used to define L_+.
- same-theory condition: all cumulants, subtractions, flow times, H,K observables, and endpoint limits come from the same cutoff sequence and same continuum Schwinger-family candidate; no auxiliary Gaussian, strong-coupling, or changed-regulator theory may supply R_{++}.
- B_eta(x_p) is the endpoint box of side eta around endpoint p; d is the separation of the paired endpoint boxes and a^2 << t << eta^2 << d^2 is the intended finite-regulator window.
- J_+ is the plus-channel sheet current obtained from the H,K hairpin pair after reflection symmetrization; its endpoint moments M_0 and M_1 vanish after Ward, cusp, and plus-channel cancellation.
- P_{++}(t,eta,d) is the exact two-curvature Wick-pair part of the flowed Wilson covariance, with color factor 2(N^2-1).
- C_{4,++}^{WS}(t,eta,d) is the connected four-curvature polarization after disconnected-product, one-hairpin perimeter, cusp, and Ward-subtraction removals.
- H_*(t,d) is a certified sup-norm or interval enclosure for the endpoint Hessian of the Ward-subtracted connected four-curvature kernel on B_eta x B_eta.

## Assumptions

- Model: compact SU(N) Wilson lattice Yang-Mills in four Euclidean dimensions at finite volume before any continuum claim; the regulator is gradient flow plus boundary point-splitting in endpoint boxes.
- Regime: a^2 << t, eta^2 >= c_t t, and eta/d <= rho0 < 1/10 so flowed kernels are smooth on endpoint boxes and endpoint Taylor remainders are controlled.
- Uniformity: all constants in the endpoint-box estimate are bounded on a declared flow plateau t in [t_min,t_max] and do not use volume- or cutoff-uniform full-measure basin entry beyond this finite calculation.
- Same-theory naturalness: the Wilson action, gauge group, flow, centering, cusp subtraction, and H,K sheet currents are fixed before evaluating R_{++}; no advice-dependent observable is inserted to force positivity.
- Cancellation assumption: Ward identities remove longitudinal endpoint terms, renormalized cusp/perimeter counterterms cancel the one-hairpin divergences, and plus-channel orientation gives M_0(J_+)=M_1(J_+)=0.
- Hessian assumption: the remaining C_{4,++}^{WS} kernel has a finite interval Hessian bound H_* on B_eta x B_eta after flow and subtraction; this is the first missing certificate to compute.
- Finite-gate boundary: L_+ is the Schur-Feshbach leakage already obtained from the finite H,K reduction; proving R_{++}^{ren}/kappa_4 > L_+ changes only endpoint-box positivity after H,K.
- Clay boundary: continuum existence, OS/Wightman reconstruction, observable density, regulator independence, large-field/topological summability, and positive Hamiltonian mass gap remain untouched.

## Equations

- flowed endpoint cumulant decomposition: `R_{++}^{\mathrm{ren}}=\kappa_2\big(W_t(J_+),W_t(J_+)\big)_{\mathrm{ren}}=P_{++}+C_{4,++}^{\mathrm{WS}}+O(g_t^8)`. Valid when: Valid when the same Wilson regulator, gradient flow time, renormalized hairpin centering, and Ward-subtracted endpoint boxes define both terms before any continuum transfer is attempted.
- positive pair baseline: `P_{++}=2(N^2-1)g_t^4\!\int J_+^{a\mu\nu}(x)K_{t,d}^{\mu\nu,\rho\sigma}(x,y)J_+^{a\rho\sigma}(y)\,dx\,dy\ge A_N g_t^4\Theta_+^2 d^{-8}(1-\varepsilon_{\mathrm{pair}})`. Valid when: Applies after diagonal color normalization and reflected plus-channel orientation, with endpoint boxes separated by d and heat-flow smearing scale much smaller than d.
- endpoint moment cancellation: `M_0(J_+)=\int_{B_\eta}J_+(u)\,du=0,\qquad M_1(J_+)=\int_{B_\eta}u\,J_+(u)\,du=0`. Valid when: Requires the same-theory Ward subtraction, cusp renormalization, and plus-channel reflection signs for the concrete H,K hairpin endpoints under evaluation.
- Hessian remainder bound: `|C_{4,++}^{\mathrm{WS}}|\le c_N g_t^6\eta^2 H_*(t,d)\|M_2(J_+)\|^2+E_{\mathrm{Taylor}}(\eta/d)+E_{\mathrm{flow}}(a^2/t)`. Valid when: Valid when the Ward-subtracted four-curvature connected kernel is twice differentiable on endpoint boxes and its Hessian has a certified interval enclosure H_* there.
- finite endpoint-box promotion inequality: `\underline R_{++}/\kappa_4-L_+ := \kappa_4^{-1}\big(P_{++}^{\mathrm{low}}-|C_{4,++}^{\mathrm{WS}}|^{\mathrm{up}}\big)-L_+>0`. Valid when: This is valid as a finite Schur-Feshbach gate only after H,K, L_+, kappa_4, and the R_{++} interval are computed in the same Wilson theory.

## Attempted Derivation

- Conceptual pressure attacked: finite Feshbach positivity, same-theory Wilson positivity, and gradient-flow renormalization must jointly hold, but the missing mediator is a certified sign/size for the connected endpoint polarization C_{4,++}^{WS}.
- Critique of carrier: raw Wilson contours are fragmented and representation-limited for interval proof search; global non-Gaussian OS witnesses are too weakly targeted; sheet currents with endpoint moments are the efficient local abstraction.
- Encode the known H,K plus channel as a reflected sheet current J_+ supported near two endpoint boxes plus a fixed interior sheet segment; preserve gauge trace, color normalization, reflection parity, and orientation signs.
- Expand the centered flowed Wilson covariance to order g_t^6: the disconnected product and one-hairpin perimeter/cusp parts are removed, leaving P_{++} plus C_{4,++}^{WS}.
- Use the flowed two-curvature covariance to isolate P_{++}; diagonal color contraction gives 2(N^2-1), and the endpoint geometry gives a positive d^{-8} baseline with explicit shape factor Theta_+^2.
- Apply Ward subtraction and plus-channel reflection to the endpoint expansion of C_{4,++}^{WS}; the monopole and dipole moments vanish, so the first surviving endpoint contribution is Hessian-controlled and O(eta^2).
- Form the interval lower bound underline R_{++}=P_{++}^{low}-|C_{4,++}^{WS}|^{up}; compare underline R_{++}/kappa_4 with the finite Schur-Feshbach leakage L_+.
- Hard gate: finite endpoint-box positivity after H,K. Success promotes this finite gate and justifies paper handoff for the endpoint repair; failure quarantines R_{++} without affecting continuum existence or mass-gap gates.

Blocking gap: The missing proof certificate is a rigorous interval bound H_*(t,d) for the Ward-subtracted connected four-curvature Hessian on endpoint boxes, including nonabelian ordering, counterterm, and endpoint-cell remainder terms.

## Falsifiers

- Ward-subtracted endpoint kernel has a residual monopole or dipole term, destroying the eta^2 suppression.
- The connected four-curvature Hessian interval H_* is so wide that underline R_{++}/kappa_4 <= L_+.
- The positive pair baseline vanishes for the actual H,K geometry because the plus-channel shape factor Theta_+ is zero.
- Cusp or perimeter counterterms fail to cancel uniformly in the selected flow window.
- The interval changes sign under harmless endpoint-box refinement, indicating representation or quadrature instability.
- The same-theory condition fails because R_{++} is computed with a different regulator, flow normalization, or observable algebra than H,K and L_+.
- Large-field or topological sectors introduce uncancelled finite-volume artifacts; this is a frontier falsifier for transfer, not for the finite algebraic calculation.
- No regulator plateau exists as a is decreased with fixed physical t, so the endpoint-box estimate remains finite-cutoff evidence only.

## Learning

Cycle 275 makes the next contribution-making move: the connected boundary-OPE polarization is estimated by an endpoint-moment Hessian certificate with explicit pair color, Ward/cusp cancellation, moment cancellation, and a finite promotion inequality. Declarative tension is now exact: positive pair covariance and flow renormalization are valid but insufficient until C_{4,++}^{WS} is interval-bounded in the same Wilson theory. Conceptual value signal: local route-changing, because R_{++}/kappa_4 becomes a falsifiable finite interval problem rather than a symbolic endpoint term. The hard gate changed is finite endpoint-box positivity after H,K; all Clay gates remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and interval-design guide, not as evidence for the Clay theorem.`
- Rationale: The branch has already abstracted R_{++}; another restatement would loop. A concrete endpoint-box experiment tests whether the proposed eta^2 Hessian suppression can plausibly beat the known finite leakage L_+ in the actual H,K plus-channel carrier.
- Situation seed: Finite-volume 4D SU(2) and SU(3) Wilson lattice Yang-Mills with gradient-flowed reflected H,K plus-channel hairpins, endpoint boxes B_eta, and the Ward-subtracted cumulant kappa_2(W_t(J_+),W_t(J_+)) evaluated by flowed plaquette-sheet contractions.
- Varied variable: The single varied parameter is rho=eta/d, with a^2/t, t/d^2, the H,K geometry, gauge group, and plus-channel orientation held fixed.
- Held-fixed controls: Same Wilson plaquette action, bare coupling trajectory, gauge group, and finite volume for H,K, L_+, kappa_4, and R_{++}., Same gradient-flow definition, centering, perimeter/cusp subtraction, endpoint boxes, and reflected sheet-current encoding., Same plus-channel H,K shape factor Theta_+, color normalization, and Schur-Feshbach leakage L_+., No continuum or mass-gap inference is allowed from the finite experiment; it only probes endpoint-box positivity.
- Expected observation: If the abstraction is correct, P_{++} remains stable while |C_{4,++}^{WS}|/P_{++} scales like O(rho^2) after Ward and cusp cancellation. A lower interval beating L_+ promotes the finite endpoint gate; persistent O(rho^0) or O(rho) behavior is a falsifier for the moment-cancellation mechanism.
- Transfer certificate needed: A certified interval Hessian bound for the Ward-subtracted four-curvature kernel, a stable flow plateau under lattice refinement, and a same-theory recovery map from sheet-current cumulants back to the original Wilson H,K observables are required before the observation may affect proof obligations.

## Next Experiment

Build the endpoint-cell interval table for C_{4,++}^{WS}: list cells in B_eta x B_eta, compute heat-kernel Hessian majorants for I_3g, I_4g, I_ct, and I_end, verify M_0=M_1=0 for the actual H,K plus current, and test whether the certified lower interval beats L_+.

# Post-H,K endpoint-box kappa4 shell certificate for reflected Wilson Route A

## Candidate Lemma

For a fixed finite endpoint box with known H,K Schur data, heat-kernel regulated SU(N) Wilson boundary-OPE data certify the Schur-corrected endpoint form by the finite margin Delta_sigma. If Delta_sigma >= 0, the worked endpoint box passes Route A positivity at this cutoff; if an interval vector gives negative value, it is a valid falsifier for this H,K geometry only.

## Definitions

- source object: finite-volume heat-kernel regulated SU(N) Yang-Mills cutoff theory with spacing a, smoothing sigma, fixed endpoint box B, reflected Wilson sheet family S_i, transported curvature fluxes, and connected curvature cumulants C_sigma and kappa4_sigma.
- target object: the finite Schur-corrected endpoint quadratic form Q_sigma on Wilson collar endpoint coefficients after eliminating the known H,K hairpin block.
- controlled interface: the recovery map Rec_sigma sends endpoint Wilson coefficients to transported curvature sheet fluxes, decomposes the connected boundary-OPE polarization R_sigma into a Gaussian color square, a compressed connected four-curvature operator kappa4_sigma, and an OPE remainder, then subtracts S_HK=B_HK^*E_HK^{-1}B_HK.
- same-theory condition: all Wilson observables, cumulants, OPE coefficients, H,K blocks, Schur inverse, vacuum/perimeter normalization, coupling g_sigma, reflection split, and error intervals are computed in the same cutoff theory and regulator.
- bridge/carrier: sheet-kernel hypergraph with vertices equal to transported surface patches, hyperedges equal to four-curvature connected cumulant contractions, labels for color tensors, shell distance, multiplicity, reflection side, and Schur endpoint index.
- preserved observables: normalized gauge-invariant Wilson loops and vacuum-subtracted reflected Wilson collar/hairpin observables; no gauge-fixed field observable is transferred.
- error budget: e_OPE bounds the boundary-OPE truncation in operator norm, M4_sigma^- bounds the negative spectral part of compressed kappa4, and s_HK bounds the Schur hairpin energy on the same endpoint coefficient space.

## Assumptions

- Model/regime: finite cutoff pure SU(N) Yang-Mills with heat-kernel smearing sigma >= c a, finite volume, fixed boundary conditions, and reflection-compatible Wilson loops.
- H,K input: the collar/hairpin blocks are already extracted in the same Wilson basis, E_HK=QHQ is strictly positive on the eliminated hairpin sector, and S_HK=B_HK^*E_HK^{-1}B_HK is finite.
- Uniformity boundary: constants are finite-box and cutoff-dependent; no volume-uniform basin entry, no cutoff-uniform large-field/topology summability, and no continuum OS spectral transfer are claimed.
- Same-theory naturalness: parallel transporters in the fluxes use the same connection as the Wilson loops, and diagonal normalization cancels vacuum and perimeter factors only inside connected Wilson cumulants.
- Computability assumption: shell intervals I_{ij,l,sigma}^{(4)} enclose the raw plaquette-sheet connected four-curvature cumulants with Wilson trace color factors and heat-kernel geometric kernels included.
- Claim-level assumption: success changes only the finite Route A endpoint-box positivity gate; OS/Wightman axioms, nontrivial continuum limit, observable density, and Hamiltonian mass gap remain untouched.

## Equations

- transported sheet flux: `X_i^A(\sigma)=\int_{S_i} w_i(x)\,\operatorname{Ad}_{U_{\gamma_{i,x}}}^{AB}F_{\mu_i\nu_i,\sigma}^B(x)\,d\Sigma_i(x)`. Valid when: Valid when the heat-kernel smearing scale sigma dominates the cutoff a and the Wilson sheet S_i remains inside the finite endpoint box.
- two-flux covariance: `\langle X_i^A(\sigma)X_j^B(\sigma)\rangle_{c}=\delta^{AB}C_{ij,\sigma}`. Valid when: Valid after gauge-covariant transport to one endpoint frame and connected expectation in the same finite cutoff measure.
- connected endpoint polarization decomposition: `R_{ij,\sigma}=\alpha_N g_\sigma^4\,(C_\sigma\circ C_\sigma)_{ij}+\frac{g_\sigma^4}{16N^2}\kappa^{(4)}_{ij,\sigma}+E^{\mathrm{OPE}}_{ij,\sigma},\qquad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid for the fourth-order boundary-OPE of normalized Wilson loops after disconnected vacuum and perimeter terms are cancelled by connected cumulant subtraction.
- connected four-curvature Wilson cumulant: `\kappa^{(4)}_{ij,\sigma}=\sum_{A,B,C,D}\int_{S_i^2\times S_j^2}\!\tau^{ABCD}_{ij}\,G_{ij}(x,y,u,v)\,\langle F_\sigma^A(x)F_\sigma^B(y)F_\sigma^C(u)F_\sigma^D(v)\rangle_c\,d\Sigma^4`. Valid when: Applies when the color tensor tau and geometric kernel G are inherited from the same Wilson trace expansion and transported sheet geometry.
- shell row-sum negative-part bound: `M_{4,\sigma}^{-}\le \max_i\sum_j\sum_{\ell=0}^{L}\left|I^{(4)}_{ij\ell,\sigma}\right|+\varepsilon^{(4)}_{\mathrm{tail},\sigma}`. Valid when: Valid when the shell partition covers all plaquette-sheet contractions and the interval enclosures contain the raw connected four-curvature cumulant entries.
- Schur-corrected endpoint form: `Q_\sigma=R_\sigma-S_{HK,\sigma},\qquad S_{HK,\sigma}=B_{HK,\sigma}^*E_{HK,\sigma}^{-1}B_{HK,\sigma}`. Valid when: Requires the same H,K Wilson basis, positive eliminated block E_HK, and endpoint compression used in the recovered R_sigma matrix.
- finite positivity margin: `\Delta_\sigma=m_{G,\sigma}-\frac{g_\sigma^4}{16N^2}M_{4,\sigma}^{-}-e_{\mathrm{OPE},\sigma}-s_{HK,\sigma},\qquad m_{G,\sigma}=\lambda_{\min}\bigl(\alpha_N g_\sigma^4(C_\sigma\circ C_\sigma)\bigr)`. Valid when: Valid on the finite endpoint coefficient space after operator-norm bounds for OPE error and Schur hairpin energy are certified.
- certificate implication: `\Delta_\sigma\ge 0\Longrightarrow Q_\sigma\succeq 0,\qquad \exists v:\ v^*Q_\sigma v<0\Longrightarrow \text{endpoint-box Route A fails for this H,K geometry}`. Valid when: Valid only for the finite cutoff endpoint box with all intervals evaluated in the same heat-kernel regulated Yang-Mills theory.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Observable Density In The Excitation Sector; source object: finite-volume heat-kernel regulated SU(N) Yang-Mills cutoff theory with spacing a, smoothing sigma, fixed endpoint box B, reflected Wilson sheet family S_i, transported curvature fluxes, and connected curvature cumulants C_sigma and kappa4_sigma.; target object: the finite Schur-corrected endpoint quadratic form Q_sigma on Wilson collar endpoint coefficients after eliminating the known H,K hairpin block.; Model/regime: finite cutoff pure SU(N) Yang-Mills with heat-kernel smearing sigma >= c a, finite volume, fixed boundary conditions, and reflection-compatible Wilson loops..
- Conceptual pressure attacked: the missing mediator between concrete connected Wilson cumulants and Schur-corrected endpoint positivity, while Clay-level OS reconstruction and spectral transfer remain quarantined.
- Freeze claim level: work at finite cutoff, finite endpoint box, heat-kernel regulator, same gauge-invariant Wilson algebra; no continuum YM existence or mass gap is inferred.
- Define Rec_sigma from endpoint Wilson coefficients to transported sheet fluxes X_i^A. This keeps source data and target endpoint form independently meaningful.
- Expand the connected product of normalized Wilson loops through fourth boundary-OPE order. Diagonal vacuum/perimeter normalization and connected cumulant subtraction remove disconnected factors.
- Compute the crossed two-curvature Gaussian contribution. With tr(T^aT^b)=delta^{ab}/2 and normalized traces, the color square gives alpha_N=(N^2-1)/(8N^2), hence a PSD Hadamard square on the endpoint coefficient space.
- Isolate the actual Yang-Mills input as kappa4_{ij,sigma}: the connected four-curvature plaquette-sheet contraction with Wilson color tensor tau^{ABCD}_{ij} and heat-kernel geometric kernel G_{ij}.
- Compress kappa4 to the endpoint basis and partition raw plaquette-sheet contractions into locality shells. Gershgorin/operator-norm enclosure gives M4_sigma^- from signed interval row sums plus a shell tail.
- Subtract the known finite Schur-Feshbach hairpin energy S_HK=B^*E^{-1}B on the same endpoint coefficient space and form Delta_sigma.
- Hard gate: Delta_sigma >= 0 promotes only a finite endpoint-box positivity certificate; a certified v with v^*Q_sigma v<0 demotes this Wilson collar/hairpin branch.

Blocking gap: The branch still lacks the raw first H,K endpoint geometry with certified plaquette-sheet shell intervals for kappa4 and a numerical same-regulator bound for e_OPE and s_HK.

## Falsifiers

- falsifier: a quotient hyperedge combines raw contractions with different Wilson trace tensors or transported orientations, invalidating the sheet-kernel interval.
- falsifier: the certified negative kappa4 row sum satisfies g_sigma^4 M4_sigma^-/(16N^2) > m_G - e_OPE - s_HK, forcing Delta_sigma < 0.
- falsifier: the Schur block E_HK has a small eigenvalue or wrong endpoint compression, making S_HK nonuniform or undefined.
- falsifier: the OPE remainder is of the same size as the Gaussian color square at the chosen sigma/a, so fourth-order truncation cannot decide the endpoint box.
- falsifier: the heat-kernel shell tail is not summable at finite volume/cutoff, showing that the proposed locality budget is representation-limited.
- falsifier: using imported continuum or lattice package estimates changes regulator, coupling, or Wilson normalization, breaking the same-theory condition.

## Learning

Cycle 275 attacks the conceptual pressure that the post-H,K route lacks a valid mediator from connected Wilson cumulants to endpoint positivity. Declarative tension: Wilson/OPE coefficients, connected kappa4 negativity, OPE errors, and Schur-Feshbach hairpin energy must be evaluated in one cutoff theory, but the result must not be inflated into OS/Wightman reconstruction or a mass-gap theorem. Scalar R is too weak and representation-limited; full OS observable density is too strong and circular for this local gate; raw plaquette enumeration is exact but fragmented. The sheet-kernel hypergraph is retained because it encodes the color, geometry, locality, transport, cancellation, and H,K data needed for finite interval arithmetic. The hard gate is Delta_sigma: success promotes only finite endpoint-box positivity, while failure gives a precise falsifier. The conceptual value signal is route-changing at finite scope because the unknown boundary-OPE polarization becomes a computable sign/size interval with explicit recovery maps and error budgets.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the first post-H,K endpoint interval.`
- Rationale: The branch has repeated the abstract Delta_sigma carrier enough; the route now needs a concrete same-regulator shell audit to decide whether kappa4 or Schur hairpin energy kills the Wilson endpoint box.
- Situation seed: Finite SU(N) heat-kernel regulated endpoint box containing the first extracted reflected Wilson collar H and hairpin K; enumerate plaquette-sheet four-curvature contractions contributing to the connected boundary-OPE polarization R_{ij,sigma}.
- Varied variable: rho=sigma/a, the heat-kernel smoothing ratio, varied over a small certified range while keeping the cutoff lattice and endpoint geometry fixed.
- Held-fixed controls: same finite endpoint Wilson sheet family S_i and same H,K Schur matrices, same normalized gauge-invariant Wilson loop algebra and connected cumulant subtraction, same SU(N), coupling convention g_sigma, trace normalization, reflection split, and boundary OPE order, same shell cutoff L with an explicit interval tail bound
- Expected observation: As rho increases modestly, the PSD Gaussian color square should smooth but remain nonnegative, while the kappa4 shell envelope and OPE remainder should either shrink enough to make Delta_sigma positive or expose a stable negative endpoint vector.
- Transfer certificate needed: Before intuition affects proof obligations, provide raw-to-hypergraph quotient audit, interval enclosures for each kappa4 shell, same-regulator e_OPE and S_HK bounds, and a verified Delta_sigma interval or negative-vector certificate.

## Next Experiment

Build the first same-regulator endpoint-box table: list S_i sheets from H,K, compute tau^{ABCD}_{ij} and G_{ij} for shells ell=0,1, bound the connected plaquette-sheet kappa4 intervals, then evaluate Delta_sigma(rho) with the Schur subtraction included.

