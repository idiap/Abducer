# cycle-0350

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Finite post-H,K Wilson endpoint screen for same-theory OS transfer

## Candidate Lemma

One-sided endpoint leakage screen: after the H,K Schur-Feshbach reductions and the known Wick-square and straight ff cancellations, the finite three-hairpin OS gate is protected whenever the positive Gaussian margin exceeds only the positive-D leakage of the same-theory connected endpoint fourth cumulants plus a uniform tail.

## Definitions

- source object: heat-kernel plaquette-sheet SU(N) endpoint source classes c, each carrying regulated log-partition data F_c(s)=log Z_c(s) for the Wilson endpoint source L_c.
- target object: the finite post-H,K reflected-Wilson OS transfer scalar I_gate for the fixed three-hairpin block, not a continuum OS/Wightman theorem.
- controlled interface: the carrier C_ep=(F_c,D_c,C_N,M_G,T_tail)_c with source-equivalence aggregation before clipping and interval multiplication after aggregation.
- same-theory condition: the endpoint sources are obtained by differentiating the same regulated Wilson observables used in the collar OS matrix, with no boundary counterterm, no algebra enlargement, and cutoff-uniform normalization.
- D_c is the aggregated null-channel endpoint incidence 2b12(c)-4b13(c)-4b23(c) after source-equivalent endpoints have been merged.
- kappa_c is the connected cumulant witness d_s^4 log Z_c(0) for the singlet-projected endpoint Wilson flux source.
- C_N=(g^4/4)(T_F/N)^2 times the fixed singlet/color-incidence normalization inherited from the plaquette-sheet regulator.

## Assumptions

- Model: four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette-sheet Wilson insertions and reflection-positive collar regularization.
- Regime: fixed finite three-hairpin Route A block after H,K have been computed and the collar width is sent to the endpoint scale inside the regulator.
- Cutoff: all endpoint source derivatives and T_tail bounds are uniform in the lattice spacing along the same regulator/RG basin used for the Wilson observables.
- Same-theory: aggregation is allowed only for endpoint boxes with identical regulated source data F_c, not for geometrically similar boxes with different Wilson contractions.
- Validity: Wick-square terms are treated as positive Gram contributions and straight nonabelian ff contacts cancel by the established null-incidence identity.
- Local: all unassigned corner, overlap, and nonlocal OPE remnants are charged to T_tail with a signed interval bound.

## Equations

- aggregated endpoint incidence: `D_c=\sum_{v\in c}\bigl(2b_{12}(v)-4b_{13}(v)-4b_{23}(v)\bigr)`. Valid when: Valid when source-equivalent endpoint boxes have first been aggregated using identical regulated endpoint source data.
- one-sided lower screen: `I_{\rm gate}\ge M_G-C_N\sum_c [D_c]_+\,\eta_c-\tau_{\rm tail},\qquad \eta_c\ge[-\kappa_c]_+`. Valid when: Applies after Wick-square positivity and straight ff cancellation leave only endpoint connected cumulants and certified tails.
- root-quartic cumulant cap: `\eta_c\le {t_c^4\over 60}\,R_4(L_c)+\epsilon_c,\qquad R_4(L)=N\operatorname{tr}(L^4)+3(\operatorname{tr}L^2)^2`. Valid when: Valid in heat-kernel endpoint coordinates where the SU(N) Haar-Jacobian expansion is uniform in the source box.
- promotion inequality: `M_G>C_N\sum_c [D_c]_+\left({t_c^4\over 60}R_4(L_c)+\epsilon_c\right)+\tau_{\rm tail}\ \Longrightarrow\ I_{\rm gate}>0`. Valid when: Requires the same-theory endpoint source classes, positive Gaussian margin, and cutoff-uniform tail bound stated above.

## Attempted Derivation

- Start from the finite Schur-Feshbach scalar I_gate after the previously computed H,K block and null-vector reduction.
- Use the established cancellations: connected logarithm removes disconnected Wick-square Gram pieces from the dangerous channel, and the straight C_A ff contact cancels by the null-incidence identity.
- Partition endpoint boxes by equality of regulated source data F_v(s); aggregate D_v within each source class before clipping, because clipping before aggregation would destroy cancellations.
- Write the remaining connected endpoint polarization as C_N sum_c D_c kappa_c plus a signed tail interval.
- For promotion, replace each possible negative kappa_c by the SU(N) root-quartic cap and keep only [D_c]_+, giving a one-sided lower bound on I_gate.
- For validation or demotion, replace the cap by seven-point same-theory source intervals and perform exact interval multiplication.

Blocking gap: The actual endpoint source classes, fractional incidences D_c, uniform eighth-derivative bounds, and T_tail for the fixed hairpin geometry have not been computed.

## Falsifiers

- A positive-D endpoint class has a certified negative connected cumulant witness whose interval overwhelms M_G after color multiplication and tail addition.
- The endpoint source finite differences require a boundary counterterm or source renormalization not present in the original Wilson algebra.
- The tail T_tail is not cutoff-uniform, so the finite endpoint screen is not valid in the regulator passage.
- Source-equivalence aggregation identifies boxes with unequal regulated F_c(s), producing an artificial cancellation.
- A stress case with b13+b23 just below b12/2 and large root-quartic R4(L_c) makes the one-sided cap inconclusive and forces direct source computation.

## Learning

Conceptual pressure: sign-certify endpoint collapse inside the same Wilson theory after H,K. Declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must coexist without a boundary theory, while raw R is too weak, raw kappa_4 spectra are too strong, and global Schur-preimage positivity is valid but too coarse after H,K. The hard gate is the finite post-H,K reflected-Wilson OS scalar: success promotes only this fixed block, failure gives a finite same-theory falsifier, and missing source/tail data keeps quarantine. Conceptual value signal: the obstruction is one-sided and local; negative SU(N) endpoint cumulants are explanatory but lower the gate only through positive-D leakage times a connected cumulant witness plus uniform tail. Clay continuum construction, gauge-invariant observable density, OS/Wightman reconstruction, nontriviality, OS spectral transfer, and positive mass gap remain non-claimed.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and validator-facing endpoint-source computation design.`
- Rationale: The branch is quarantined unless the connected boundary-OPE polarization R is bounded or computed; another abstract OS/Wilson restatement would not change the proof state.
- Situation seed: Fixed SU(N) heat-kernel plaquette-sheet regulator for the three reflected Wilson hairpins after H,K, with endpoint source classes c evaluated by seven same-theory source values of log Z_c(s).
- Varied variable: Fractional endpoint leakage alpha_c=(b13(c)+b23(c))/b12(c), varied through the half-overlap threshold alpha_c=1/2 while holding the Wilson hairpin block fixed.
- Held-fixed controls: Same regulated gauge-invariant Wilson observables and Wilson normalization; no boundary counterterm or algebra enlargement., The H,K Schur-Feshbach data, null vector, color factor C_N, and reflection-positive heat-kernel regulator., Uniform tail budget T_tail and source analyticity radius for the seven-point connected cumulant witness.
- Expected observation: For alpha_c>=1/2 the endpoint class is shielded in the one-sided lower bound; for alpha_c<1/2 the measured kappa_c interval must be compared against M_G to promote or falsify the finite gate.
- Transfer certificate needed: A cutoff-uniform table of source-equivalent classes with D_c, seven log Z_c values or root-quartic caps, M8 remainders, and T_tail, proving the calculation remains in the same Wilson theory.

## Next Experiment

Proof search plus targeted endpoint source computation: build the C_ep table for the actual heat-kernel three-hairpin endpoints, compute D_c and seven log Z_c samples for every connected cumulant witness class, then certify whether I_gate is positive, negative, or still quarantined.

# First-annulus Ward-Hessian certificate for the flowed Wilson endpoint mediator

## Candidate Lemma

Conditional finite theorem: in the Wilson lattice SU(N) theory with gradient flow, the first endpoint annulus contributes a certified lower interval to R_{++}^{ren}; if the dominance margin Delta_R^- is positive, the post-H,K endpoint-box Schur-Feshbach obstruction is removed for this finite model instance. This is not a Clay mass-gap claim.

## Definitions

- source object: centered flowed Wilson hairpins W_+^H(t,a), W_+^K(t,a) represented by endpoint sheet currents J_+^H,J_+^K on a fixed H,K collar geometry in finite-volume lattice SU(N).
- target object: the scalar finite Route A endpoint mediator R_{++}^{ren}(t,a) and its dominance margin against the known Schur-Feshbach leakage L_+.
- controlled interface: the connected cumulant witness kappa_2(W_+^H,W_+^K) after disconnected-product, one-hairpin perimeter, cusp, and Ward subtractions, transferred through the same gradient-flow recovery map.
- same-theory condition: the source cumulant, recovery errors, counterterms, coupling g_t, flow time t, cutoff a, and H,K geometry are taken from one regulator/RG trajectory, with no imported spectral or area-law theory change.
- first annulus A_0: endpoint pairs with rho <= |x-y| <= 2 rho inside the fixed endpoint box, decomposed into outward-rounded quadrature cells.
- carrier: endpoint sheet currents modulo certified zero-pairing equivalence; raw Wilson contours are treated as recovery data, not as the primary proof representation.

## Assumptions

- Model: four-dimensional finite-volume lattice SU(N) Yang-Mills with Wilson action, gradient flow time t>0, cutoff a>0, and fixed boundary endpoint boxes separated from other insertions.
- Regime: a << sqrt(8t) <= rho and endpoint-box diameter eta*rho is small enough for the Taylor-Hessian remainder to be dominated by the second moment M_{2,+}.
- Uniformity: all constants H_{s,0}^+, G_{++}^{0,-}, and E_{rec}^+ are interval-enclosed with outward rounding uniformly over the chosen finite volume and cutoff window.
- Same-theory: the centered flowed Wilson cumulant, pair covariance, connected C4 sectors, and recovery map use the same bare action, same gauge group, same flow, and same normalization.
- Local: only the first annulus A_0 and its compressed tail interface are claimed; continuum OS reconstruction, observable density, and Hamiltonian spectral transfer remain untouched.

## Equations

- Rpp_cumulant_definition: `R_{++}^{ren}(t,a)=\kappa_2\!\left(W_{+,ren}^H(t,a),W_{+,ren}^K(t,a)\right)`. Valid when: Valid when the flowed Wilson hairpins are centered and renormalized by the same perimeter, cusp, and endpoint counterterms.
- pair_C4_decomposition: `R_{++}^{ren}\ge g_t^4\Big(2(N^2-1)G_{++}^{0,-}-N(N^2-1)C_{4,++}^{0,+}\Big)-E_{rec}^{0,+}`. Valid when: Applies after disconnected products and one-hairpin divergences are subtracted on the first endpoint annulus.
- Ward_Hessian_C4_bound: `C_{4,++}^{0,+}\le M_{2,+}^2\sum_{s\in\mathcal S}H_{s,0}^+ + T_{3,0}^+`. Valid when: Requires Ward cancellation, cusp subtraction, and plus-channel monopole and dipole moment cancellation on every annular cell.
- dominance_margin: `\Delta_R^-:=g_t^4\Big(2(N^2-1)G_{++}^{0,-}-N(N^2-1)M_{2,+}^2\sum_sH_{s,0}^+-N(N^2-1)T_{3,0}^+\Big)-E_{rec}^{0,+}-L_+`. Valid when: Valid when L_+ is the finite Schur-Feshbach leakage for the same H,K reduction and normalization.
- promotion_criterion: `\Delta_R^->0\ \Longrightarrow\ Q_{+,postHK}>0\quad\text{for this finite endpoint-box instance}`. Valid when: Applies only in the finite Route A model where all interval endpoints and recovery errors are certified.

## Attempted Derivation

- Attack conceptual pressure: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator; positive pair covariance and raw-hairpin recovery can each be valid while connected C4 erases R_{++}.
- Replace fragmented raw contours by endpoint sheet currents, but keep a recovery-error term E_{rec}^+ so the carrier change is not circular.
- Expand the two centered flowed Wilson hairpins to order g_t^4 on the first annulus A_0. The disconnected product and one-hairpin perimeter/cusp pieces cancel by construction.
- Evaluate the Gaussian pair contraction: reflection/orientation in the plus channel gives the positive baseline 2(N^2-1)G_{++}^{0,-}.
- Collect connected four-curvature contributions into Ward-subtracted sectors s with color factor N(N^2-1). No favorable sign is assumed.
- Use Ward identities and plus-channel monopole/dipole cancellation to remove zeroth and first endpoint moments, leaving a mixed-Hessian bound proportional to M_{2,+}^2.
- Enclose each sector on A_0 by outward-rounded quadrature plus Taylor remainder, producing H_{s,0}^+ and T_{3,0}^+.
- Subtract the Schur-Feshbach leakage L_+ and recovery error E_{rec}^{0,+}; the resulting Delta_R^- is the finite promotion or quarantine margin.

Blocking gap: The actual validator-facing interval numbers for G_{++}^{0,-}, H_{s,0}^+, T_{3,0}^+, and E_{rec}^{0,+} have not yet been computed with outward rounding on the H,K geometry.

## Falsifiers

- First-annulus falsifier: certified Delta_R^- <= 0, so connected C4 plus recovery error defeats the pair baseline and L_+.
- Ward falsifier: the Ward-subtracted sector kernel has an uncancelled boundary or cusp residue on A_0.
- Same-theory falsifier: the endpoint-current recovery map changes normalization, flow time, action, or observable algebra relative to the raw Wilson cumulant.
- Plateau falsifier: H_{s,0}^+ or the annular tail ratio fails to stabilize over the cutoff/flow window.
- Geometry falsifier: plus-channel monopole or dipole moments do not vanish for the actual H,K endpoint currents.
- Interval-width falsifier: outward-rounded quadrature intervals are wider than the dominance margin and cannot decide the sign.

## Learning

Cycle 350 attacks the conceptual pressure that finite Schur-Feshbach endpoint positivity lacks a same-theory Wilson mediator. The declarative tension is exact: endpoint positivity, positive flowed pair covariance, and raw-hairpin recovery may each be valid while connected C4 erases R_{++}. Raw Wilson contours are fragmented and representation-limited; global OS spectral transfer, area-law intuition, and broad same-theory nontriviality witness routes are too coarse for this finite obstruction. Endpoint sheet currents are the efficient representation because they encode H,K sheets, endpoint moments, sector kernels, counterterms, recovery errors, and L_+; preserve gauge/color/reflection/orientation/cutoff/locality/same-theory invariants; use cumulant expansion, Ward/cusp subtraction, Taylor Hessians, heat-kernel majorants, dyadic interval quadrature, outward rounding, and certified zero-pairing equivalence; keep finite endpoint locality plus summable annuli; and expose falsifiers. Conceptual value signal: R_{++}/kappa_4 is now a first-annulus Ward-Hessian dominance certificate, not a symbolic boundary-OPE term. Success promotes one finite Route A hard gate; failure quarantines the R repair while all Clay target commitments remain unclaimed. Reporting skill: timeline-definition-assumption-elicitor.

## Gedanken Experiment Design Seed

- Need decision: `Design concrete thought experiment now as a falsifier probe and proof-search guide.`
- Rationale: The branch no longer needs another obstruction restatement; the proof state hinges on whether the actual same-theory connected cumulant witness has a positive first-annulus dominance margin after Ward-Hessian subtraction.
- Situation seed: Finite-volume SU(N) Wilson lattice Yang-Mills with gradient-flowed centered H,K plus-channel hairpins, endpoint boxes fixed, and the first plateau annulus A_0 represented by dyadic endpoint-current cells.
- Varied variable: The dimensionless annulus parameter u=rho/sqrt(8t), varied while keeping the H,K geometry and endpoint-box aspect eta fixed.
- Held-fixed controls: Same Wilson action, gauge group SU(N), bare trajectory, gradient-flow map, and renormalization scheme for all cumulants., The H,K collar/hairpin endpoint sheet currents, plus-channel reflection/orientation convention, and Schur-Feshbach leakage L_+., Ward/cusp subtraction rules, zero-pairing equivalence policy, and outward-rounded interval arithmetic.
- Expected observation: A real proof route should show a plateau where G_{++}^{0,-} stays positive, H_{s,0}^+M_{2,+}^2 and E_{rec}^+ remain smaller than the pair baseline minus L_+, and Delta_R^- has stable positive sign; loss of this plateau is a valid demotion signal.
- Transfer certificate needed: A cutoff-window certificate proving that the flowed endpoint-current cumulant equals the raw centered Wilson cumulant up to E_{rec}^+, with Ward/cusp cancellations and quadrature bounds uniform in the finite regulator window.

## Next Experiment

Route to proof search: instantiate the first-annulus connected cumulant witness for the concrete H,K endpoint cells, compute outward-rounded intervals for G_{++}^{0,-}, H_{s,0}^+, T_{3,0}^+, E_{rec}^{0,+}, and Delta_R^-, then promote finite endpoint-box positivity or quarantine the R_{++} repair.

# Support-function raw K4 stress certificate for the finite H,K endpoint box

## Candidate Lemma

Finite support-function falsifier: for the heat-kernel regulated SU(N) endpoint matrix U_sigma=R_sigma-S_HK, a diagonal upper bound D_i^+<0 or a support-certified off-diagonal lower bound L_pq(nu)^2>D_p^+D_q^+ proves that the post-H,K endpoint block is not positive semidefinite. This changes only the finite Route A endpoint-box gate; it is not an OS reconstruction, gauge-invariant observable density, excitation-sector cyclicity, or mass-gap claim.

## Definitions

- source object: a finite heat-kernel lattice SU(N) cutoff theory with endpoint Wilson sheet-pair observables Q_i=:Phi_i^2:_sigma in one reflected endpoint box.
- target object: the finite Hermitian Schur-corrected endpoint matrix U_sigma on the chosen H,K Wilson endpoint basis, tested only for positive semidefiniteness.
- controlled interface: Rec_sigma maps raw signed four-curvature Wilson cumulant orbit intervals, Gaussian flux contractions, OPE intervals, and the H,K Schur block into interval entries of U_sigma.
- same-theory condition: the regulator a, smearing sigma, renormalized coupling g_R, Wilson basis, quotient identities, OPE subtraction, and H,K Schur data are identical in every term of Rec_sigma.
- connected cumulant witness: R_{ij,sigma}=cum_2(Q_i,Q_j) after vacuum and perimeter cancellation, not a symbolic scalar R.
- support direction: nu in C with |nu|=1 is used to certify a lower bound on |U_{pq}| without phase-net discretization.

## Assumptions

- Model: finite hypercubic heat-kernel lattice regularization of pure SU(N) Yang-Mills with a fixed endpoint box and finite Wilson sheet basis.
- Cutoff: a>0 and sigma>=a are fixed, so all Wilson cumulants and Schur blocks are finite-dimensional objects.
- Same-theory: the Gaussian contraction, connected K4 cumulant intervals, OPE error, and S_HK are computed in the same cutoff measure and normalization.
- Validity: exact Wilson trace identities and orientation symmetries are used for quotienting; no empirical phase averaging or cross-regulator import is allowed.
- Local: the lemma concerns only the endpoint subspace after the H,K collar/hairpin elimination and does not assert continuum Schwinger coherence.

## Equations

- connected endpoint polarization: `R_{ij,\sigma}=\operatorname{cum}_2(Q_i,Q_j)=G_{ij,\sigma}+K_{ij,\sigma}+E^{\mathrm{OPE}}_{ij,\sigma}`. Valid when: Valid when Q_i are heat-kernel regulated endpoint Wilson observables in the fixed cutoff theory and disconnected vacuum/perimeter terms have been subtracted.
- Gaussian color square: `G_{ij,\sigma}=\alpha_N g_R^4\,(C_{ij,\sigma}\odot \overline{C_{ij,\sigma}}),\qquad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after transported two-curvature Gaussian contractions are evaluated with the same Wilson sheets and SU(N) trace normalization.
- Schur-corrected endpoint matrix: `U_{\sigma}=R_{\sigma}-S_{HK},\qquad S_{HK}=B_{HK}^*E_{HK}^{-1}B_{HK}`. Valid when: Requires the finite H,K hairpin block E_HK to be positive and invertible on the eliminated complement.
- diagonal upper bound: `D_i^+=G_{ii,\sigma}+\frac{g_R^4}{16N^2}\sum_o \max\{b_{ii,o}\ell_o,b_{ii,o}u_o\}+e_{ii}-s_{ii}^-`. Valid when: Valid when each raw signed K4 orbit interval is [ell_o,u_o] and S_HK has a certified lower diagonal bound s_ii^-.
- support lower bound: `L_{pq}(\nu)=\left[\operatorname{Re}(\overline{\nu}z^0_{pq})+\frac{g_R^4}{16N^2}\sum_o \min\{a_o(\nu)\ell_o,a_o(\nu)u_o\}-e_{pq}\right]_+`. Valid when: Valid when z^0_pq=G_pq-S_HK,pq, a_o(nu)=Re(conj(nu)b_pq,o), and OPE uncertainty has radius e_pq.
- two-sparse PSD falsifier: `D_i^+<0\quad\text{or}\quad \exists\nu\in\mathbb C,\ |\nu|=1:\ L_{pq}(\nu)^2>D_p^+D_q^+\ \Longrightarrow\ U_\sigma\not\succeq0`. Valid when: Applies because every positive semidefinite Hermitian matrix has nonnegative diagonal entries and satisfies the two-by-two principal minor inequality.

## Attempted Derivation

- Conceptual pressure attacked: raw non-Gaussian Wilson K4 data must mediate to a finite Schur-corrected endpoint PSD decision without circular OS Hilbert observable algebra, gauge-invariant observable density, or excitation-sector cyclicity claims.
- Declarative tension: Wilson/OPE coefficients, signed K4 orbit intervals, OPE errors, and S_HK must be valid in one cutoff theory, while continuum existence, OS positivity, observable density, and Clay mass gap conclusions are barred.
- Start from R_ij=cum_2(Q_i,Q_j). Vacuum and perimeter disconnected terms cancel by normal ordering and cumulant subtraction, leaving Gaussian crossed curvature contractions plus connected four-curvature K4 plus OPE error.
- Insert the finite Schur-Feshbach correction U=R-S_HK; this is the same H,K collar/hairpin block already fixed by the Route A endpoint calculation.
- For diagonal entries, propagate raw K4 intervals and OPE radii to an upper bound D_i^+. If D_i^+<0 then U_ii<0 for all completions, contradicting PSD.
- For off-diagonal entries, treat the signed orbit uncertainty set as a convex subset of C. For any unit support direction nu, the infimum of Re(conj(nu)U_pq) gives a certified lower bound L_pq(nu) on |U_pq|.
- Use the necessary PSD inequality |U_pq|^2<=U_pp U_qq. Upper bounds on U_pp,U_qq and a lower bound on |U_pq| yield the falsifier L_pq(nu)^2>D_p^+D_q^+.
- This replaces phase-net scanning by an exact support-function certificate over recovered raw signed orbits; A012 shell envelopes are quarantined because they do not preserve phases.

Blocking gap: The branch still lacks actual same-regulator raw K4 orbit intervals [ell_o,u_o] for the first endpoint pair p,q; without them the support function cannot produce a numeric sign or size certificate.

## Falsifiers

- Raw K4 orbit intervals are missing, regulator-mismatched, or not derived from the same heat-kernel cutoff theory.
- Exact Wilson quotienting fails Hermiticity, so the recovered K4 interval matrix is not a valid Hermitian connected cumulant witness.
- The OPE interval radius e_pq is large enough that every support lower bound L_pq(nu) vanishes.
- A diagonal upper certificate D_i^+ is negative, immediately falsifying endpoint PSD for the worked H,K geometry.
- A support direction satisfies L_pq(nu)^2>D_p^+D_q^+, giving a valid two-sparse falsifier for the finite endpoint route.
- All two-sparse tests survive but full Delta_raw proof search gives a negative Rayleigh vector x_stress.
- The finite certificate depends on A012 shell compression rather than raw signed orbits, demoting the claimed support-function bound.

## Learning

Cycle 350 refines the branch from support-function rhetoric into a finite conditional theorem with a concrete recovery map. The hard gate is D_i^+<0 or L_pq(nu)^2>D_p^+D_q^+: success supplies a valid falsifier for only the worked post-H,K endpoint PSD gate, while failure gives no positivity and forces full Delta_raw proof search or quarantine. The conceptual value signal is sharp and unifying at finite scope: Gaussian color positivity, signed connected K4 danger, OPE error, and Schur hairpin energy are combined in one same-theory connected cumulant witness. Carrier audit: scalar R is too weak, A012 shells lose phases, phase nets are convenient but discretization-sensitive, OS Hilbert observable algebra and gauge-invariant observable density are too strong and circular for this local gate, and full Delta_raw is complete but expensive. Efficient representation requirements are now explicit: encode oriented plaquettes, sheet weights, heat-kernel transporters, color tensors, cumulant intervals, OPE intervals, endpoint phases, support directions, and Schur blocks; preserve gauge invariance, reflection support, Hermiticity, Gaussian/K4 separation, exact Wilson quotienting, locality, and same-theory normalization; primitive operations are cumulant contraction, signed orbit summation, support-function certification, Rayleigh stress search, Loewner bounds, and Schur subtraction; equivalence is exact Wilson identity quotienting only; locality budget is the finite endpoint box; transfer is only through tau, Delta_raw, or x_stress. Larger Yang-Mills gates--volume/cutoff-uniform basin entry, large-field and topology control, regulator-independent Schwinger functions, OS positivity, observable density, excitation-sector cyclicity, physical-unit spectral transfer, and the Clay mass gap--remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and validator-facing computation design.`
- Rationale: The branch is looping unless the connected boundary-OPE polarization R is tested through actual same-regulator K4 intervals; a concrete finite stress experiment can kill the H,K endpoint route without invoking OS-density abstractions.
- Situation seed: Fix a heat-kernel regulated SU(3) lattice endpoint box with the worked H,K collar/hairpin Schur block, two endpoint sheet-pair nodes p,q, Gaussian covariance C_sigma, and signed raw K4 orbit coefficients b_pq,o.
- Varied variable: rho, the amplitude of the dominant signed connected four-curvature orbit interval in the off-diagonal direction selected by the support functional.
- Held-fixed controls: Same cutoff a and smearing sigma for Gaussian, K4, OPE, and S_HK data., Same Wilson endpoint basis, transported curvature normalization, and SU(3) trace convention., Fixed H,K Schur block and fixed OPE error budget e_ij., Exact Wilson quotient identities and Hermiticity constraints.
- Expected observation: There is a computable threshold rho_* at which L_pq(nu)^2 crosses D_p^+D_q^+; crossing gives a finite falsifier, while non-crossing only routes to full Delta_raw proof search.
- Transfer certificate needed: A proof that the varied interval is a valid same-regulator connected cumulant witness for the raw K4 orbit, with exact quotient invariance and no shell-compression phase loss.

## Next Experiment

Proof search: compute the first same-regulator signed raw K4 orbit interval for a selected endpoint pair p,q in the heat-kernel SU(3) H,K box, then evaluate D_p^+, D_q^+, and the support-function lower bound L_pq(nu); if no interval is available, quarantine this branch rather than restating OS Hilbert observable algebra or gauge-invariant observable density.

