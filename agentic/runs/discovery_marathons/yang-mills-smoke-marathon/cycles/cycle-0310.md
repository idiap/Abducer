# cycle-0310

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint source interval gate for post-H,K reflected Wilson block

## Candidate Lemma

Finite Route A endpoint theorem: for the fixed reflected three-hairpin Wilson block, in the heat-kernel plaquette-sheet regulator, the post-H,K null-channel scalar is certified by endpoint source classes C_ep. After Wick-square Gram positivity and straight f f null-incidence cancellation, I_gate>0 promotes only this finite OS block; I_gate<0 is a same-theory finite falsifier; no continuum existence or mass-gap claim follows.

## Definitions

- source object: C_ep(a,L,h) is the finite list of heat-kernel endpoint source classes c, their seven source values F_c(rh), fractional incidences b_ij,c, color factor C_N, Gaussian margin M_G, and tail budget T_tail for the locked Wilson hairpin block.
- target object: the target is the second Feshbach null scalar of the intended same-theory OS matrix for the finite reflected Wilson block, not a continuum Schwinger family and not a Hamiltonian mass gap.
- controlled interface: Phi_ep maps regulated endpoint source derivatives and incidences to the scalar interval [I_-,I_+] while preserving Wilson normalization, reflection symmetry, null-channel cancellations, and cutoff bookkeeping.
- same-theory condition: all source values are computed from the same heat-kernel Wilson measure and the same gauge-invariant Wilson observables; no boundary counterterm, altered cusp renormalization, gauge fixing, or enlarged boundary algebra is allowed.
- endpoint class: c is a source-equivalence class; classes may be merged only when their regulated functions F_c(s)=log Z_c(s) agree on the stencil to the certified error.
- incidence: D_c=2b_12,c-4b_13,c-4b_23,c is the null-channel endpoint dominance coefficient after the already-computed H,K block.

## Assumptions

- Model: four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette-sheet regulator in a fixed finite volume before cutoff removal.
- Regime: the theorem concerns one finite reflected Wilson collar/hairpin block after the H,K Schur-Feshbach gates have already been passed.
- Cutoff: endpoint-box radius, heat-kernel time t_c, and stencil step h are chosen with explicit cutoff-uniform derivative and tail bounds.
- Same-theory: Wilson loop normalization and source insertions are inherited from the original gauge-invariant lattice theory, with no boundary field or counterterm added at the reflection plane.
- Validity: Wick-square contractions are treated as positive Gram terms, and the straight nonabelian f f contact is assumed to satisfy the verified null-incidence cancellation for this geometry.
- Local: all unclassified endpoint/corner interactions are charged to T_tail, which must be cutoff-uniform for the certificate to be valid.

## Equations

- seven_point_source_cumulant: `F_c(s)=\log Z_c(s),\quad \kappa_c=F_c^{(4)}(0),\quad \widehat\kappa_c(h)=h^{-4}\sum_{r=-3}^{3}w_rF_c(rh),\quad w=( -1/6,2,-13/2,28/3,-13/2,2,-1/6)`. Valid when: Valid when the endpoint source function is eight-times differentiable on the stencil interval and the heat-kernel source class is fixed.
- endpoint_dominance_incidence: `D_c=2b_{12,c}-4b_{13,c}-4b_{23,c},\qquad D_c\le 0\ \text{if}\ b_{13,c}+b_{23,c}\ge b_{12,c}/2`. Valid when: Valid when the fixed three-hairpin null vector and the source-equivalence endpoint incidences are those of the regulated Wilson collar geometry.
- post_HK_endpoint_scalar: `I_{\rm gate}=M_G+C_N\sum_c D_c\kappa_c+T_{\rm tail}`. Valid when: Valid after the H,K Schur-Feshbach reduction, Wick-square Gram positivity, one-body cancellation, and straight f f null-incidence cancellation have been applied.
- root_quartic_endpoint_cumulant: `\kappa_c=-\frac{t_c^4}{60}\,R_4(L_c)+E_c,\qquad R_4(L)=N\operatorname{tr}(L^4)+3(\operatorname{tr}(L^2))^2`. Valid when: Valid in small heat-kernel endpoint coordinates with SU(N) Haar-Jacobian expansion and a certified sixth-and-higher remainder bound.
- safe_lower_interval: `I_-^{\rm safe}=M_G-C_N\sum_c[D_c]_+(A_c+\epsilon_c)-C_N\sum_c[-D_c]_+\max(0,\epsilon_c-A_c)-T_{\rm tail},\quad A_c=t_c^4R_4(L_c)/60`. Valid when: Valid when each endpoint cumulant interval satisfies kappa_c in [-A_c-epsilon_c,-A_c+epsilon_c] and tails are bounded symmetrically by T_tail.

## Attempted Derivation

- Attack conceptual pressure: endpoint collapse must be sign-certified inside the same Wilson theory, not hidden in symbolic R or repaired by a boundary theory.
- Freeze the finite Route A object: the already-reduced reflected three-hairpin block after the H,K Schur-Feshbach gates; Clay continuum existence, nontriviality, OS reconstruction for all observables, and mass gap are not claimed.
- Use heat-kernel plaquette-sheet endpoint coordinates and define F_c(s)=log Z_c(s) for the singlet endpoint source L_c; the fourth source derivative is the connected cumulant witness for the boundary OPE polarization.
- Apply the two valid cancellations already isolated: the connected log removes Wick-square disconnected pieces as Gram-positive data, and the null incidence identity cancels the straight C_A f f contact in the hairpin geometry.
- Aggregate endpoint boxes by equality of regulated source data, then contract signed incidences to D_c=2b_12,c-4b_13,c-4b_23,c; this avoids premature clipping artifacts.
- Expand the SU(N) Haar-Jacobian in small endpoint heat-kernel coordinates to obtain the leading non-Gaussian connected cumulant kappa_c=-(t_c^4/60)(N tr L_c^4+3(tr L_c^2)^2)+E_c.
- Combine the positive Schur-Feshbach margin M_G, color factor C_N, signed endpoint cumulants, and the endpoint/corner tail T_tail to obtain the finite interval [I_-,I_+].

Blocking gap: The actual endpoint source-class table, certified eighth-derivative stencil errors, and a cutoff-uniform T_tail are not yet computed for the regulated Wilson hairpin geometry.

## Falsifiers

- A certified heat-kernel endpoint class with D_c>0 and negative kappa_c large enough that I_+<0 is a finite same-theory falsifier of this OS transfer gate.
- A nonuniform endpoint/corner tail T_tail along the cutoff sequence prevents promotion beyond regulator-level evidence.
- A boundary counterterm, altered Wilson normalization, or added boundary algebra needed to compute Z_c violates the same-theory condition.
- Source-equivalence classes that merge unequal regulated source derivatives make the interval invalid.
- Failure of the straight f f null-incidence cancellation in the actual collar/hairpin geometry reopens the post-H,K R term.

## Learning

Cycle 310 turns the quarantined endpoint carrier into a sharper finite theorem: the actual connected boundary-OPE polarization is the source-derivative interval M_G+C_N sum D_c kappa_c+T_tail. The negative SU(N) root-quartic cumulant is explanatory but not itself the obstruction; only source-certified positive D leakage plus uncontrolled tails can demote the finite block. This is novel only at finite Route A scope and leaves the Clay continuum, nontriviality, OS/Wightman, and mass-gap gates untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe while the branch remains quarantined for endpoint data.`
- Rationale: The branch no longer needs another abstract OS-closed-cone restatement; the hard gate is a finite post-H,K reflected-Wilson endpoint scalar whose sign is decided by source intervals and incidences.
- Situation seed: Take one SU(N) heat-kernel plaquette-sheet endpoint box for the fixed three-hairpin reflected Wilson block, with one source class c carrying the same-theory connected cumulant witness kappa_c from F_c(s)=log Z_c(s).
- Varied variable: Vary eta=(b_13,c+b_23,c)/b_12,c from 0 to 1 while keeping b_12,c and the source L_c fixed.
- Held-fixed controls: The heat-kernel regulator, Wilson observable normalization, reflection plane, and finite H,K block are fixed., No boundary counterterm, gauge fixing, or enlarged boundary observable algebra is introduced., The root-quartic source cumulant interval and color factor C_N are held fixed., The Gaussian Schur-Feshbach margin M_G and tail budget T_tail are held fixed.
- Expected observation: The endpoint contribution changes sign-pressure at eta=1/2: eta>=1/2 is shielded when kappa_c<=0, while eta<1/2 creates positive D leakage that can become a valid finite falsifier if it exceeds M_G after tails.
- Transfer certificate needed: A cutoff-uniform source-derivative interval for kappa_c, a certified incidence table for b_ij,c in the actual Wilson contraction, and a tail bound proving that the thought-experiment endpoint class is realized in the same theory.

## Next Experiment

Route to proof search plus endpoint data computation: build the heat-kernel endpoint source-class table for the fixed three-hairpin block, evaluate the connected cumulant witness by the seven-point stencil, certify the root-quartic remainder and T_tail, then return exactly one validator-facing interval [I_-,I_+] for the finite OS gate.

# Gauge-Invariant Nontriviality Witness Selection: endpoint R++ sector certificate

## Candidate Lemma

Conditional finite Route A theorem: for the H,K plus-channel endpoint box, Ward/cusp subtraction and plus-moment cancellation give a certified lower interval for the same-theory connected Wilson cumulant R_{++}; if this interval exceeds the known Schur-Feshbach leakage L_+, endpoint-box positivity is promoted, while failure quarantines only this R repair.

## Definitions

- source object: finite endpoint-cell data for two centered gradient-flowed Wilson hairpin sheet currents J_+^{(1)},J_+^{(2)} in the H,K collar, including cell moments, sector kernels, counterterms, cutoff a, volume V, flow time t, and recovery errors.
- target object: a finite plus-channel endpoint-box lower interval R_{++}^{I,-} to be inserted into the Schur-Feshbach endpoint matrix for Route A.
- controlled interface: same-theory centered flowed Wilson cumulant map (J_1,J_2) -> kappa_2(W_t(J_1),W_t(J_2))_c with Ward/cusp subtraction and certified zero-pairing current quotienting.
- same-theory condition: the Wilson action, gradient-flow map, reflection plane, counterterms, normalization, cutoff sequence, and continuum Schwinger family are identical for the pair baseline and the connected C4 polarization.
- carrier observable: the connected cumulant witness is the centered flowed Wilson hairpin covariance, not a global OS spectral measure witness.
- hard gate changed: finite endpoint-box positivity after H,K; continuum existence, OS/Wightman reconstruction, observable density, large-field/topology control, and Hamiltonian mass gap remain untouched.

## Assumptions

- Model: four-dimensional Euclidean SU(N) Yang-Mills with Wilson lattice regulator or an equivalent gauge-invariant flowed regulator in finite volume before cutoff removal.
- Regime: endpoint boxes have diameter eta, mutual distance d, and flow time t with a^2 << t and eta <= c sqrt(t) << d in the certified cell decomposition.
- Cutoff: all sector constants, Ward residuals, cusp counterterms, and recovery errors are bounded uniformly along the chosen cutoff subsequence.
- Same-theory: pair contraction, connected C4 kernels, counterterms, and recovery maps are computed from the same regulated measure and the same flowed Wilson observables.
- Validity: Ward and cusp subtractions make each renormalized sector kernel C^2 on cell products except for near-diagonal pieces controlled by explicit heat-kernel majorants.
- Local: the claim is finite-cell and endpoint-local; it does not assert a continuum Yang-Mills construction or a positive Hamiltonian mass gap.
- Constraint: plus-channel endpoint currents have certified zero monopole and dipole moments after quotienting only by zero-pairing currents.

## Equations

- centered flowed cumulant defining R++: `R_{++}^{\mathrm{ren}}(I)=\kappa_2\!\left(\widehat W_t(J_+^{(1)}),\widehat W_t(J_+^{(2)})\right)_{\mathrm{ren}},\quad \widehat W_t(J)=W_t(J)-\langle W_t(J)\rangle`. Valid when: Valid when the reflected endpoint hairpin currents are flowed, centered, renormalized, and supported in the fixed H,K endpoint cells.
- pair-plus-connected sector decomposition: `R_{++}^{\mathrm{ren}}=g_t^4(N^2-1)\left(2G_{++}+N\sum_{s\in\mathcal S}\Xi_s\right)+E_6+E_{\mathrm{rec}}`. Valid when: Applies after disconnected-product removal, one-hairpin perimeter and cusp subtraction, and projection to the plus-channel endpoint current basis.
- plus moment cancellation: `M_{0,+}=\int_I J_+(x)\,dx=0,\qquad M_{1,+}^{\alpha}=\int_I (x-x_I)^{\alpha}J_+(x)\,dx=0`. Valid when: Requires the H,K plus-channel orientation convention and the certified zero-pairing quotient for endpoint sheet currents.
- sector Hessian remainder bound: `|\Xi_s^I|\le H_s^{I,+}M_{2,+}^2,\qquad M_{2,+}=\int_I |x-x_I|^2|J_+(x)|\,dx`. Valid when: Valid when the Ward-subtracted sector kernel has an outward-rounded Hessian majorant H_s^{I,+} on the chosen cell product.
- route-A promotion interval: `R_{++}^{I,-}=g_t^4(N^2-1)\left(2G_{++}^{I,-}-NM_{2,+}^2\sum_{s\in\mathcal S}H_s^{I,+}\right)-E_6^{I,+}-E_{\mathrm{rec}}^{I,+},\quad R_{++}^{I,-}>L_+`. Valid when: Applies after all lower and upper interval bounds are outward-rounded and L_+ is the previously computed finite Schur-Feshbach leakage.

## Attempted Derivation

- Freeze the claim level: finite Route A endpoint-box positivity after H,K only; no Clay existence, OS reconstruction, or mass-gap claim is made.
- Replace fragmented raw Wilson contours by endpoint sheet currents carrying gauge, color, reflection, orientation, cutoff, locality, and same-theory invariants.
- Define R_{++}^{ren} as the centered gradient-flowed Wilson hairpin covariance in the same Wilson measure; this keeps the connected cumulant witness validator-facing.
- Expand the cumulant through the endpoint R/kappa_4 order: disconnected products and one-hairpin perimeter/cusp terms cancel, leaving a positive pair contraction with color 2(N^2-1) and connected C4 sectors with color N(N^2-1).
- Use plus-channel monopole and dipole cancellation to remove constant and linear Taylor terms of each Ward-subtracted sector kernel on an endpoint cell.
- Bound the remaining sector terms by Hessian constants times M_{2,+}^2, add E_6 and E_rec, and obtain the lower interval R_{++}^{I,-}.
- Compare R_{++}^{I,-} with the already finite Schur-Feshbach leakage L_+; strict dominance promotes the endpoint-box gate, while failure quarantines the R repair.

Blocking gap: The proof is blocked at certified numerical or analytic enclosures for H_s^{I,+}, E_rec, and E_6 in a cutoff-stable flow-time window; connected C4 contact sectors may still be too wide or sign-indefinite.

## Falsifiers

- falsifier: the outward-rounded interval gives R_{++}^{I,-} <= L_+ for every admissible eta/sqrt(t) and cutoff window.
- falsifier: Ward or cusp residuals survive the subtraction and create an uncanceled contact term in C4.
- falsifier: the recovery map from raw Wilson hairpins to endpoint currents has E_rec of the same order as the positive pair baseline.
- falsifier: the positive pair contraction G_{++}^{I,-} vanishes because the H,K geometry has zero effective endpoint orientation overlap.
- falsifier: near-sector heat-kernel constants grow as a -> 0 at fixed physical t, breaking cutoff uniformity.
- falsifier: zero-pairing quotienting identifies currents whose centered Wilson cumulants differ by a nonzero same-theory observable.
- stress case: take eta close to sqrt(t) and d barely above the far-cell threshold; interval-width blowup then tests whether the Hessian certificate is real or representation-limited.

## Learning

Conceptual pressure attacked: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator, while positive flowed pair covariance and renormalization can both be valid yet connected C4 can erase them. Declarative tension: endpoint positivity, same-theory flowed cumulants, and recovery from raw Wilson hairpins must jointly hold, but the missing mediator is a cutoff-stable Ward-Hessian sector certificate. Carrier critique: raw Wilson contours are fragmented; global OS spectral transfer and a non-Gaussian Schwinger-family route are too coarse for this local obstruction. Better abstraction: endpoint sheet currents with cell moments, sector kernels, counterterms, recovery errors, Ward/cusp subtraction, heat-kernel Hessians, outward-rounded interval arithmetic, and certified zero-pairing quotienting. Efficient representation requirements: encode H,K sheets, endpoint currents, moments, sector kernels, counterterms, and errors; preserve gauge/color/reflection/orientation/cutoff/locality/same-theory invariants; use cumulant expansion, Taylor remainders, near/far heat-kernel majorants, and finite refinement; transfer only through centered flowed Wilson cumulants; demote on any falsifier. Hard gate: finite endpoint-box positivity after H,K. Value signal: R_{++}/kappa_4 is a valid route-deciding color-geometric lower interval, not a symbolic endpoint term; success promotes one finite Route A gate, failure quarantines the R repair, and all Clay gates remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch has reduced R_{++} to sector constants; another abstract restatement would loop. A concrete target-preserving thought experiment can expose whether Ward-Hessian suppression plausibly beats L_+ before full interval proof search.
- Situation seed: Finite-volume SU(2) Wilson lattice Yang-Mills with gradient flow at fixed physical t, using the already fixed H,K collar/hairpin endpoint geometry and centered plus-channel endpoint sheet currents; measure R_{++}^{ren} by the same flowed Wilson cumulant and decompose it into pair, C4-near, C4-far, counterterm, and recovery intervals.
- Varied variable: rho=eta/sqrt(t), the endpoint-cell diameter in flow units.
- Held-fixed controls: Wilson action, gauge group SU(2), reflection plane, H,K endpoint geometry, plus-channel orientation, and centered flowed Wilson normalization are held fixed., The cutoff hierarchy a^2 << t, volume large compared with d, and same-theory counterterm scheme are held fixed while rho varies., The finite Schur-Feshbach leakage L_+ and the zero-pairing quotient test space are held fixed.
- Expected observation: If the endpoint-moment mechanism is valid, C4-sector intervals scale like O(rho^2) relative to the positive pair baseline until near-contact cells dominate; a stable window with R_{++}^{I,-}>L_+ would promote the finite endpoint-box gate, while monotone dominance failure demotes the repair.
- Transfer certificate needed: Before intuition enters proof obligations, require cutoff-uniform Ward residual bounds, interval-enclosed near/far sector constants, same-theory recovery errors, and a regulator plateau showing that the flowed cumulant is the same observable family, not a lattice artifact.

## Next Experiment

Route explicitly to proof search: compute outward-rounded sector constants for the SU(2) flowed H,K endpoint-cell model at fixed rho values, then certify or falsify R_{++}^{I,-}>L_+. Keep the connected cumulant witness and same-theory nontriviality witness markers visible, but report only the finite endpoint-box Route A consequence.

# Gauge-Invariant Observable Density In The Excitation Sector

## Candidate Lemma

In a finite heat-kernel SU(N) Wilson endpoint box, raw K4 intervals for endpoints p,q give a valid falsifier: if the certified phase-stress envelope tau_pq(theta)<0, the Schur-corrected endpoint form is not PSD. Only the finite H,K Route A gate is demoted.

## Definitions

- source object: finite cutoff heat-kernel Wilson measure with transported plaquette curvatures, sheet weights, and connected four-plaquette cumulant intervals.
- target object: the two-dimensional Schur-corrected endpoint quadratic form U_sigma on span{e_p,e_q} from the worked H,K collar/hairpin basis.
- controlled interface: a connected cumulant witness mapping raw plaquette K4 intervals, Gaussian color square, OPE interval, and S_HK into U_sigma entries.
- same-theory condition: the K4 intervals, Wilson OPE coefficients, regulator sigma, coupling g_R, endpoint basis, and H,K Schur block are from one cutoff ensemble.
- declarative tension: Wilson/OPE data, raw K4 negativity, OPE errors, and H,K subtraction must jointly hold, while gauge-invariant observable density and OS spectral transfer are non-claims.
- carrier audit: scalar R is too weak; OS Hilbert observable algebra is too strong and circular; A012 shells are quarantined; raw plaquette intervals are fragmented but valid.
- route comparison: full Delta_raw PSD search can promote positivity but needs many entries; two-sparse phase stress is a sharper negative tactic using three certified intervals.
- representation requirements: encode oriented plaquettes, sheet weights, transporters, color tensors, endpoint indices, cumulant/OPE intervals, and Schur blocks; quotient only by exact Wilson identities.

## Assumptions

- Model: finite lattice SU(N) Yang-Mills with heat-kernel regulator sigma and reflection-compatible endpoint boxes.
- Cutoff: all plaquette cumulants are bounded at fixed a, finite volume, fixed sigma/a, before any continuum or RG claim.
- Same-theory: the H,K Schur block and raw K4 intervals use identical Wilson normalization, coupling, gauge group, and boundary supports.
- Validity: U is Hermitian after reflection pairing; diagonal upper bounds and phase lower bounds are certified by interval arithmetic.

## Equations

- raw_K4_sheet_contraction: `K^{(4)}_{ij,\sigma}=\sum_{\alpha\beta\gamma\delta}w_i^\alpha w_i^\beta w_j^\gamma w_j^\delta T^{abcd}_{\alpha\beta\gamma\delta}\,\kappa^c_{4,\sigma}(F^a_\alpha,F^b_\beta,F^c_\gamma,F^d_\delta)`. Valid when: Valid when the heat-kernel lattice regulator, transported plaquette curvature variables, and endpoint sheet weights are fixed before interval bounding.
- endpoint_form_decomposition: `U_{ij}=\alpha_N g_R^4 P_{ij}+\frac{g_R^4}{16N^2}K^{(4)}_{ij,\sigma}+E^{OPE}_{ij}-S^{HK}_{ij},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after same-basis Wilson OPE normalization, connected-cumulant subtraction, and Schur-Feshbach elimination of the H,K hairpin block.
- phase_stress_falsifier: `\ell_{pq}(\theta)=\Re(e^{-i\theta}U_{pq})_{low},\quad \tau_{pq}(\theta)=\bar U_{pp}-\ell_{pq}(\theta)^2/\bar U_{qq}<0\Rightarrow \exists x:x^*Ux<0`. Valid when: Requires Hermitian endpoint compression, positive diagonal upper bound, and phase lower bound certified in the same cutoff ensemble.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Observable Density In The Excitation Sector; source object: finite cutoff heat-kernel Wilson measure with transported plaquette curvatures, sheet weights, and connected four-plaquette cumulant intervals.; target object: the two-dimensional Schur-corrected endpoint quadratic form U_sigma on span{e_p,e_q} from the worked H,K collar/hairpin basis.; Model: finite lattice SU(N) Yang-Mills with heat-kernel regulator sigma and reflection-compatible endpoint boxes..
- Expand each endpoint observable Q_i as a normal-ordered quadratic flux over transported plaquette sheets; disconnected vacuum and perimeter terms cancel in cum_2(Q_i,Q_j).
- Separate cum_2(Q_i,Q_j) into the PSD Gaussian color square P_ij and one raw connected four-curvature contraction K4_ij with explicit sheet weights and color tensor T.
- Add the same-regulator OPE interval and subtract the precomputed H,K Schur energy to obtain interval entries for U_pp,U_qq and phase lower bounds for Re(e^{-i theta}U_pq).
- Test the Rayleigh vector x=(1,-ell/theta_den e^{-i theta}); tau_pq(theta)<0 gives x^*Ux<0, a finite falsifier for endpoint PSD.

Blocking gap: The proof search still lacks certified same-regulator numerical intervals for K4_pp, K4_qq, and the phased K4_pq contraction in the chosen endpoint box.

## Falsifiers

- A negative tau_pq(theta) is a valid falsifier for the finite H,K endpoint PSD route, not for Yang-Mills itself.
- Regulator mismatch between K4 intervals and S_HK invalidates the connected cumulant witness.
- Non-invariant Wilson quotienting can fake a phase lower bound and must demote the certificate.
- If diagonal upper intervals are too wide, the stress test becomes inconclusive and must hand off to full Delta_raw proof search.

## Learning

Conceptual pressure: replace symbolic R by a connected cumulant witness. Hard gate: tau_pq(theta)<0 demotes only finite H,K endpoint positivity; survival forces Delta_raw search. Value signal: sharp finite unification of Gaussian color positivity, raw K4 danger, OPE error, and Schur hairpin energy while Clay gates stay quarantined.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the finite Route A endpoint calculation.`
- Rationale: The branch is looping unless the connected boundary-OPE polarization is tested on raw same-regulator plaquette intervals rather than scalar R or OS-density language.
- Situation seed: Finite SU(N) heat-kernel lattice box with two reflected endpoint plaquette sheets p,q from the H,K collar/hairpin geometry; measure the connected cumulant witness K4_pp,K4_qq,K4_pq.
- Varied variable: phase angle theta used to align the off-diagonal raw K4 interval in the two-sparse Rayleigh stress vector.
- Held-fixed controls: same cutoff a, regulator sigma, coupling g_R, gauge group SU(N), and finite volume, same Wilson endpoint basis, reflection normalization, OPE subtraction, and H,K Schur block
- Expected observation: Either one theta yields tau_pq(theta)<0 and demotes endpoint PSD, or all certified phases survive and the route must attempt full Delta_raw positivity.
- Transfer certificate needed: A validator-facing interval certificate for three raw K4 contractions with exact Wilson quotient audit and same-theory normalization.

## Next Experiment

Proof search: compute the three same-regulator raw K4 intervals for endpoints p,q, scan certified theta values, and either output tau<0 stress vector or quarantine this H,K endpoint route.

