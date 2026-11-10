# cycle-0313

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology -> finite endpoint source screen

## Candidate Lemma

Endpoint root-quartic cap screening lemma: for the heat-kernel plaquette-sheet regulator, the post-H,K connected endpoint boundary-OPE polarization has a valid one-sided analytic lower bound using only positive-D leakage, SU(N) root-quartic trace caps, and a cutoff-uniform tail budget. If this lower bound is nonnegative, the finite post-H,K reflected-Wilson OS gate is promoted; if certified source stencils give an upper interval below zero, the block is a same-theory finite falsifier.

## Definitions

- source object: finite three-hairpin reflected Wilson endpoint carrier C_ep(a,t), consisting of endpoint source classes c, heat-kernel box partition functions Z_c(sA_c), signed incidences b_{ij,c}, D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}, color factor C_N, Gaussian margin M_G, and tail interval T_tail.
- target object: the finite post-H,K reflected-Wilson OS transfer gate, namely nonnegativity of the Schur-Feshbach null-channel scalar for this locked Wilson block.
- controlled interface: map C_ep to an interval [I_-,I_+] for M_G plus the connected endpoint boundary-OPE polarization, using regulated source derivatives, signed incidence contraction, color multiplication, clipping, and tail addition.
- same-theory condition: the heat-kernel Wilson normalization, endpoint source insertions, reflection map, and cutoff bookkeeping are identical to the collar Wilson observables; no boundary counterterm, algebra enlargement, or changed loop renormalization is introduced.
- conceptual pressure: endpoint collapse must be sign-certified inside the same Wilson theory rather than hidden in symbolic R.
- declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must jointly hold without a boundary theory; H,K and the half-overlap shield alone do not decide the scalar.
- carrier audit: raw R is representation-limited, raw kappa4 spectra are too strong, and global Schur-preimage positivity is valid but too coarse after H,K; C_ep is the efficient carrier.
- efficient representation: encode endpoint classes, source stencils, cumulant intervals, signed fractional incidences, C_N, M_G, and T_tail; preserve Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; use source differentiation, interval arithmetic, source-equivalence, clipping, incidence contraction, and tail addition; equivalence is equality of regulated source data; transfer only [I_-,I_+].

## Assumptions

- Model: four-dimensional Euclidean SU(N) Yang-Mills on a lattice/plaquette-sheet heat-kernel regulator, restricted to the finite reflected Wilson hairpin block already reduced by H,K.
- Regime: endpoint boxes are small enough for a fixed exponential-coordinate heat-kernel expansion and source norms are inside the regulator chart radius.
- Cutoff: all constants epsilon_c and tau_tail are uniform in lattice spacing and volume for this finite block before any continuum claim is made.
- Same-theory: the source derivatives of log Z_c are computed from the same Wilson action and same gauge-invariant observables used in the collar OS matrix.
- Local: Wick-square Gram terms and straight-segment C_A f f contacts have already cancelled in the null-channel incidence contraction; only endpoint/corner cumulants and tails remain.
- Validity: the SU(N) root-quartic coefficient uses the stated trace convention for Hermitian traceless endpoint sources; a different convention must be converted before promotion.
- Constraint: C_N is nonnegative and D_c is the signed null-channel endpoint incidence, so only [D_c]_+ can multiply a negative fourth cumulant into a dangerous term.

## Equations

- endpoint fourth cumulant expansion: `\kappa_c(A_c)=\left.\partial_s^4\log Z_c(sA_c)\right|_{s=0}=-\frac{t_c^4}{60}R_4(A_c)+E_c,\quad R_4(A)=N\operatorname{tr}(A^4)+3(\operatorname{tr}A^2)^2`. Valid when: Valid when the heat-kernel endpoint box is written in the fixed SU(N) exponential chart with small t_c and the same Wilson source normalization as the collar observables.
- root-quartic cap: `0\le R_4(A_c)\le (N+3)(\operatorname{tr}A_c^2)^2`. Valid when: Valid for Hermitian traceless endpoint sources A_c after singlet projection and the trace convention used in the heat-kernel source derivative.
- analytic screening lower bound: `I_{\rm gate}\ge I_{\rm cap}^-:=M_G-C_N\sum_c [D_c]_+\left(\frac{t_c^4}{60}(N+3)(\operatorname{tr}A_c^2)^2+\epsilon_c\right)-\tau_{\rm tail}`. Valid when: Applies after Wick-square Gram terms and straight f f contacts have been cancelled in the H,K null channel and only endpoint classes are charged.
- stencil interval for promotion or demotion: `I_{\rm exact}=M_G+C_N\sum_cD_c\kappa_c+T_{\rm tail},\quad I_-\le I_{\rm exact}\le I_+`. Valid when: Requires certified seven-point source stencils for each source-equivalence class and a cutoff-uniform interval for the endpoint tail contribution.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: finite three-hairpin reflected Wilson endpoint carrier C_ep(a,t), consisting of endpoint source classes c, heat-kernel box partition functions Z_c(sA_c), signed incidences b_{ij,c}, D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}, color factor C_N, Gaussian margin M_G, and tail interval T_tail.; target object: the finite post-H,K reflected-Wilson OS transfer gate, namely nonnegativity of the Schur-Feshbach null-channel scalar for this locked Wilson block.; Model: four-dimensional Euclidean SU(N) Yang-Mills on a lattice/plaquette-sheet heat-kernel regulator, restricted to the finite reflected Wilson hairpin block already reduced by H,K..
- Freeze claim level: prove or falsify only the finite post-H,K reflected-Wilson endpoint scalar, not the continuum Clay target.
- Use heat-kernel plaquette-sheet endpoint boxes and write the same-theory source partition function Z_c(sA_c) for each source-equivalence class.
- Expand the SU(N) Haar-Jacobian/heat-kernel endpoint contribution in exponential coordinates; the connected fourth source derivative gives the negative root-quartic term plus E_c.
- Use connected log Z_c, so disconnected Wick-square contractions are removed from kappa_c; the remaining Wick-square Gram contribution has already been assigned to the safe H,K margin.
- Use the null-channel incidence identity from the H,K block to cancel straight C_A f f contacts, leaving endpoint/corner cumulants and T_tail.
- Contract endpoint classes by D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}; since the leading kappa_c is nonpositive, only [D_c]_+ can reduce I_gate.
- Apply tr(A^4)<= (tr A^2)^2 for Hermitian endpoint sources to obtain the computable cap R_4(A)<= (N+3)(tr A^2)^2.
- Export I_cap^- as an analytic screen: I_cap^->=0 promotes this finite block; otherwise compute exact seven-point source stencils only on positive-D classes.

Blocking gap: The root-quartic coefficient, the remainder epsilon_c, and T_tail need a cutoff-uniform certificate in the exact heat-kernel chart; actual positive-D source-class data are still missing.

## Falsifiers

- A positive-D endpoint class whose certified seven-point source stencil gives I_+<0 is a finite same-theory falsifier of the post-H,K block.
- A nonuniform endpoint tail T_tail as a->0 invalidates the analytic screen even if all local source classes look safe.
- A boundary counterterm or changed Wilson-loop renormalization needed at the reflection plane violates the same-theory condition.
- A source-equivalence coarsening that groups unequal regulated log Z_c derivatives can hide a dangerous connected cumulant witness.
- A heat-kernel chart conversion that changes the sign or size of the root-quartic coefficient beyond epsilon_c demotes the cap to heuristic evidence.
- Endpoint boxes with eta_c<1/2 and large tr(A_c^2)^2 are the stress case for the half-overlap shield.

## Learning

Cycle 313 replaces data-only quarantine by an analytic screening theorem for endpoint collapse in the same Wilson theory. The sharp value signal is finite and explanatory: negative SU(N) root-quartic endpoint cumulants are not the falsifier; only positive-D leakage, certified by same-theory source data, plus a uniform tail can demote the post-H,K block. Success changes the finite reflected-Wilson OS transfer gate; failure gives a finite falsifier; all Clay continuum, nontriviality, OS/Wightman, and mass-gap gates remain open.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe and analytic-screen calibration.`
- Rationale: The branch is quarantined for missing endpoint data; another abstraction of C_ep would loop. Varying endpoint overlap gives a target-preserving way to see whether positive-D leakage can actually overcome the finite Gaussian margin.
- Situation seed: In the SU(N) heat-kernel plaquette-sheet regulator, take one endpoint source-equivalence class for the three reflected Wilson hairpins with fixed b12>0 and vary how much of that endpoint footprint is shared with the 13 and 23 pairings, while keeping the H,K block and Wilson normalization fixed.
- Varied variable: The overlap ratio eta=(b13+b23)/b12, especially the transition through eta=1/2 where D=2b12(1-2eta) changes sign.
- Held-fixed controls: Gauge group SU(N), heat-kernel endpoint-box regulator, and the same Wilson action/source normalization., The previously computed H,K Schur-Feshbach data and positive Gaussian margin M_G., No boundary counterterm, no gauge fixing change, no observable algebra enlargement., Uniform tail budget tau_tail and fixed source norm tr(A^2).
- Expected observation: For eta>=1/2 the negative root-quartic endpoint cumulant is protective or neutral; for eta<1/2 the analytic lower bound decreases linearly in 1-2eta and may identify a small set of positive-D connected cumulant witness classes needing exact stencils.
- Transfer certificate needed: A cutoff-uniform heat-kernel expansion with the stated root-quartic coefficient, certified fractional incidences for the endpoint class, and a same-theory source-derivative equality certificate before the observation can affect the finite OS proof queue.

## Next Experiment

Proof search plus endpoint data: certify the root-quartic remainder in the heat-kernel chart, compute D_c and tr(A_c^2) for each source-equivalence class, run seven-point log Z_c stencils on the positive-D connected cumulant witness set, and decide whether I_->=0, I_+<0, or quarantine persists.

# Endpoint-sector certificate for the flowed Wilson R_{++} term

## Candidate Lemma

Conditional finite Route A lemma: a same-theory Ward-Hessian enclosure of the connected boundary-OPE polarization gives a valid lower interval for R_{++}^{ren}; if this interval exceeds the finite Schur-Feshbach leakage L_+, the post-H,K endpoint-box plus channel is positive. This changes only the finite endpoint-box positivity gate, not the Clay continuum or mass-gap gates.

## Definitions

- source object: finite-volume SU(N) Wilson Yang-Mills at cutoff a with positive gradient-flow time t, reflected H,K hairpin endpoint boxes, and centered renormalized flowed Wilson hairpins \hat W_+(J;t,a).
- target object: the finite Schur-Feshbach endpoint-box positivity certificate Q_+^{ren}=Q_+^{bare}+R_{++}^{ren}-L_+ for the plus channel after the H,K reduction.
- controlled interface: endpoint sheet-current recovery map \Phi_{t,a} from raw Wilson hairpins to endpoint currents J, with recorded recovery error E_rec and preservation of gauge, color, reflection, orientation, locality, and endpoint moments.
- same-theory condition: all cumulants, counterterms, pair contractions, sector kernels, and recovery errors are computed in the same flowed Wilson measure that defines the finite H,K matrices; no Gaussian surrogate may supply the sign of R_{++}.

## Assumptions

- Model: SU(N) Wilson lattice Yang-Mills in a finite reflection-symmetric box, with Wilson loops evaluated after gradient flow at fixed t>0.
- Regime: endpoint-cell diameter eta sqrt(t) is smaller than the H,K collar separation, and a/sqrt(t) is inside a fixed regulator window.
- Cutoff: the boundary-OPE expansion is used only to order g_t^4 with an explicit nonnegative remainder envelope E_6^+(t,a,eta).
- Same-theory: perimeter, cusp, Ward, and coupling counterterms are those of the same finite Wilson theory used for the cumulant.
- Uniformity: sector constants Lambda_s^+ and recovery errors E_rec^+ are required to be stable under the finite cutoff refinements used in the certificate.
- Local: endpoint currents are supported in the finite endpoint boxes and obey the plus-channel zero monopole and zero dipole moment constraints after subtraction.
- Validity: the claim is a restricted finite positivity certificate, not a construction of continuum Schwinger functions, OS positivity, observable density, or a Hamiltonian mass gap.

## Equations

- flowed endpoint covariance defining R: `R_{++}^{\rm ren}(t,a,\eta)=\kappa_2^{(a,t)}\big(\hat W_+(J_1;t,a),\hat W_+(J_2;t,a)\big)`. Valid when: Valid when the centered hairpin observables are renormalized at fixed positive flow time and both are evaluated in the same finite Wilson measure.
- pair plus connected-polarization decomposition: `R_{++}^{\rm ren}=g_t^4\{2(N^2-1)G_{++}+N(N^2-1)C_{4,++}^{\rm WS}\}+E_{\ge6}+E_{\rm rec}`. Valid when: Applies after disconnected products, one-hairpin perimeter factors, and cusp counterterms are subtracted in the boundary-OPE window with a bounded sixth-order remainder.
- Ward-Hessian domination of C4: `C_{4,++}^{\rm WS}\ge -M_{2,+}^2\big(\Lambda_{3g}^++\Lambda_{4g}^++\Lambda_{ct}^++\Lambda_{end}^+\big)`. Valid when: Requires the plus endpoint currents to have zero monopole and dipole moments after Ward and cusp subtraction on every endpoint cell.
- promotion interval against Feshbach leakage: `R_{++}^{I,-}=g_t^4(N^2-1)\{2G_{++}^{I,-}-N M_{2,+}^2\Lambda_{C4}^{I,+}\}-E_6^{I,+}-E_{rec}^{I,+},\quad R_{++}^{I,-}>L_+`. Valid when: Valid when the sector constants, recovery errors, and pair lower bound are enclosed by outward-rounded interval arithmetic at fixed cutoff and volume.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: finite-volume SU(N) Wilson Yang-Mills at cutoff a with positive gradient-flow time t, reflected H,K hairpin endpoint boxes, and centered renormalized flowed Wilson hairpins \hat W_+(J;t,a).; target object: the finite Schur-Feshbach endpoint-box positivity certificate Q_+^{ren}=Q_+^{bare}+R_{++}^{ren}-L_+ for the plus channel after the H,K reduction.; Model: SU(N) Wilson lattice Yang-Mills in a finite reflection-symmetric box, with Wilson loops evaluated after gradient flow at fixed t>0..
- Attack pressure: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator between leakage L_+ and the connected boundary-OPE polarization R_{++}.
- Use the gradient-flow regulator and boundary point-splitting; define R_{++}^{ren} as the connected cumulant of two centered renormalized thin H,K plus hairpins.
- Apply the boundary-OPE cumulant expansion to order g_t^4. The disconnected product and one-hairpin perimeter/cusp terms cancel by centering and counterterm subtraction.
- Separate the explicit pair contraction with color factor 2(N^2-1), giving G_{++}>=0 for nonzero endpoint geometry.
- Place all connected four-curvature polarization into sector kernels 3g, 4g, counterterm, and endpoint-current sectors with color factor N(N^2-1).
- Replace raw contours by endpoint sheet currents. This is not merely convenient: raw contours are fragmented and representation-limited, while endpoint currents expose Ward, cusp, reflection, orientation, and plus-moment invariants.
- Use the zero monopole/dipole plus-channel constraints to subtract constant and linear Taylor jets of every Ward-subtracted sector kernel.
- Bound the remainder by mixed endpoint Hessian constants times M_{2,+}^2; split constants into analytic far envelopes and near-cell outward-rounded quadrature.
- Obtain the finite lower interval R_{++}^{I,-}=g_t^4(N^2-1)(2G_{++}^{I,-}-N M_{2,+}^2 Lambda_{C4}^{I,+})-E_6^{I,+}-E_rec^{I,+}.
- Compare this interval with the exact finite Schur-Feshbach leakage L_+ from the H,K theorem.

Blocking gap: The missing mediator is the certified same-theory bound for Lambda_{C4}^{I,+}, E_6^{I,+}, and E_rec^{I,+}; the pair term is explicit, but connected C4 can still erase it.

## Falsifiers

- Ward/cusp subtraction fails, leaving a nonzero endpoint monopole or dipole; this falsifier destroys the Hessian suppression.
- The certified Lambda_C4^{I,+} is so large that R_{++}^{I,-}<=L_+ throughout the allowed eta window.
- The plus hairpin geometry has G_{++}^{I,-}=0 or an orientation error that removes the positive pair baseline.
- The recovery map Phi_{t,a} changes the theory, loses reflection/orientation invariants, or has E_rec larger than the endpoint interval margin.
- The interval has no cutoff plateau as a/sqrt(t) decreases, so the finite certificate is regulator-fragile.
- A near-cell sector contains an uncanceled cusp or longitudinal singularity not represented in the sector constants.
- Higher-order boundary-OPE remainder E_6^+ is not bounded in the finite regulator window.

## Learning

Cycle 313 attacks the conceptual pressure that finite Schur-Feshbach positivity needs a same-theory Wilson mediator. Declarative tension: positive flowed pair covariance, same-theory renormalization, and endpoint positivity can all be valid while connected C4 erases the pair term. The current carrier, raw Wilson contours, is too fragmented; endpoint sheet currents are sharper because Ward/cusp subtraction, plus-moment cancellation, mixed Hessian bounds, interval arithmetic, and zero-pairing quotienting become primitive. Compared with global OS spectral transfer or a non-Gaussian Schwinger family route, this abstraction targets the hard gate of finite endpoint-box positivity after H,K. Conceptual value signal: R_{++}/kappa_4 is now a falsifiable color-geometric lower interval with explicit sector constants and recovery errors, not a symbolic endpoint term. Success promotes one finite Route A gate; failure quarantines the R repair while preserving all Clay commitments.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and proof-search guide, not as numerical evidence for the Clay theorem.`
- Rationale: The branch is no longer served by abstract Wilson/OS language. The decisive unknown is whether the connected boundary-OPE polarization can be interval-dominated by the positive pair term in the same finite Wilson theory.
- Situation seed: Finite SU(2) Wilson lattice in a reflection-symmetric box with gradient flow at fixed physical t; insert the explicit H,K plus hairpin endpoint currents in two endpoint boxes and evaluate the centered flowed Wilson covariance defining R_{++}^{ren}.
- Varied variable: Endpoint-cell diameter eta in the window a/sqrt(t) << eta << collar separation/sqrt(t).
- Held-fixed controls: Wilson action, gauge group SU(2), reflection plane, finite volume, and H,K plus-channel sheet-current geometry are fixed., Gradient-flow time t, boundary point-splitting prescription, perimeter/cusp counterterms, and centering normalization are fixed., The same finite Wilson measure is used for pair contraction, C4 sectors, recovery errors, and the finite Schur-Feshbach leakage L_+.
- Expected observation: If moment cancellation is the right abstraction, the certified connected C4 majorant scales like eta^4 times mixed-jet constants while G_{++}^{I,-} remains positive; failure to beat L_+ is a real route falsifier.
- Transfer certificate needed: Before intuition may affect proof obligations, provide outward-rounded intervals for G_{++}^{I,-}, Lambda_s^{I,+}, E_6^{I,+}, and E_rec^{I,+}, plus a same-theory recovery proof from raw hairpins to endpoint currents.

## Next Experiment

Route explicitly to proof search: compute an outward-rounded interval for the SU(2) flowed H,K plus endpoint-cell case, first certifying the moment identities and far-sector derivative constants, then enclosing the near 3g/4g/ct/end kernels. Record the centered Wilson covariance as a connected cumulant witness and potential same-theory nontriviality witness only after the finite same-theory recovery certificate is valid.

# Raw K4 phase-stress certificate for post-H,K endpoint positivity

## Candidate Lemma

Finite theorem: in the heat-kernel regulated H,K endpoint box, a phase-separated off-diagonal raw connected K4 interval gives a two-sparse Rayleigh falsifier for Schur-corrected endpoint positivity whenever the phase-stress margin is negative.

## Definitions

- source object: finite heat-kernel regulated SU(N) lattice Yang-Mills endpoint data consisting of Wilson plaquette-sheet weights, transported curvature insertions, raw connected K4 interval bounds, OPE intervals, and H,K Schur blocks; this is a connected cumulant witness, not an OS Hilbert observable algebra claim.
- target object: the two-dimensional Schur-corrected endpoint compression U_sigma restricted to span{e_p,e_q}, viewed as an independently meaningful finite Hermitian matrix whose positivity is required by the worked Route A endpoint calculation.
- controlled interface: phase-rotated interval Rayleigh map from raw Wilson plaquette cumulants and H,K Schur data to a two-sparse stress vector; it preserves gauge invariance, reflection support, endpoint compression, Gaussian/K4 separation, and exact Wilson quotienting.
- same-theory condition: all cumulant intervals, Gaussian contractions, OPE remainders, Schur energies, coupling constants, cutoff a, heat-kernel width sigma, Wilson basis, vacuum subtraction, and reflected H,K geometry are taken in one cutoff theory.
- carrier critique: scalar R is representation-limited, A012 shell compression is quarantined, and gauge-invariant observable density is too strong and circular for this finite endpoint gate.
- efficient representation: encode oriented plaquettes, sheet weights, heat-kernel transporters, color tensors, endpoint labels, cumulant intervals, OPE intervals, and Schur blocks; primitive operations are cumulant contraction, interval summation, phase certification, Rayleigh minimization, Loewner bounding, and Schur subtraction; equivalence is only by exact Wilson trace identities.
- hard gate: tau_pq(theta)<0 demotes finite H,K endpoint positivity; survival is not promotion and only hands the problem to full Delta_raw PSD proof search.

## Assumptions

- Model: finite-volume lattice SU(N) Yang-Mills with heat-kernel plaquette regulator and reflection plane chosen before endpoint compression.
- Cutoff: a>0, sigma>0, and the endpoint box contains finitely many plaquette sheets with sigma/a inside the OPE validity window.
- Same-theory: K4 intervals, Gaussian covariance, OPE error, and S_HK are computed from the same regulated vacuum and the same Wilson collar/hairpin basis.
- Validity: diagonal upper bounds u_pp^+, u_qq^+ are rigorous interval upper bounds for the Schur-corrected compression entries, with u_qq^+>0 unless the q diagonal is already a direct falsifier.
- Local: the claim changes only finite Route A endpoint-box positivity and makes no OS/Wightman, continuum, nontriviality, observable-density, excitation-sector cyclicity, or Hamiltonian mass-gap claim.

## Equations

- endpoint Wilson quadratic observable: `Q_i=\sum_{(r,s)\in\mathcal P_i} w_i(r,s)\,\mathcal T_i^{AB}(r,s):F^A_{r,\sigma}F^B_{s,\sigma}:`. Valid when: Valid when the endpoint sheet family is finite, transported plaquette curvatures are heat-kernel smeared, and normal ordering uses the same regulated vacuum.
- Schur-corrected raw endpoint compression: `U_{ij,\sigma}=\alpha_N g_R^4 G_{ij,\sigma}+\frac{g_R^4}{16N^2}K^{(4)}_{ij,\sigma}+E^{\mathrm{OPE}}_{ij,\sigma}-S^{HK}_{ij,\sigma},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid when vacuum and perimeter disconnected pieces are cancelled before compression and H,K Schur subtraction is formed in the same endpoint basis.
- phase lower interval: `\ell_{pq}(\theta)=\inf\{\operatorname{Re}(e^{-i\theta}z):z\in\mathcal R_{pq}\},\quad \mathcal R_{pq}\supseteq U_{pq,\sigma}`. Valid when: Applies when the complex off-diagonal entry has a rigorous rectangular or polygonal interval enclosure after all Gaussian, K4, OPE, and Schur contributions are combined.
- two-sparse Rayleigh bound: `x(t,\theta)=e_p-t e^{i\theta}e_q,\quad x^*U_\sigma x\le u_{pp}^+ +t^2u_{qq}^+-2t\ell_{pq}(\theta)`. Valid when: Valid for every admissible Hermitian matrix inside the interval enclosure, provided the phase lower bound is certified for the same off-diagonal entry.
- phase-stress demotion gate: `\tau_{pq}(\theta)=u_{pp}^+-\frac{(\ell_{pq}(\theta)_+)^2}{u_{qq}^+}<0\ \Longrightarrow\ \exists x_{\mathrm{stress}}:x_{\mathrm{stress}}^*U_\sigma x_{\mathrm{stress}}<0`. Valid when: Requires u_qq^+ positive, the same interval enclosure for all entries, and the optimizing choice t=ell_pq(theta)_+/u_qq^+.

## Attempted Derivation

- Define Q_i as a finite weighted sum of heat-kernel transported, vacuum-normal-ordered plaquette curvature pairs in the H,K endpoint box.
- Use connected cumulant subtraction: disconnected vacuum and perimeter terms cancel before R_ij is formed, leaving a PSD Gaussian color square, raw K4, and an OPE interval.
- Compress the same endpoint data by the Schur-Feshbach correction S_HK to obtain the finite Hermitian interval matrix U_sigma.
- For endpoints p,q, enclose U_pq in a complex interval rectangle R_pq and choose a phase theta with positive lower support ell_pq(theta).
- For x=e_p-t e^{i theta}e_q, bound x^*U_sigma x by u_pp^+ + t^2 u_qq^+ - 2t ell_pq(theta), then optimize t=ell_pq(theta)_+/u_qq^+.
- Conclude that tau_pq(theta)<0 is a valid falsifier for finite endpoint PSD; if tau survives, the proof state moves to full Delta_raw search, not promotion.

Blocking gap: No actual same-regulator raw K4 interval values for the selected H,K endpoint pair p,q have been computed in this cycle; the theorem is validator-facing but data-conditional.

## Falsifiers

- falsifier: the complex off-diagonal interval R_pq contains the origin in every useful phase sector, so ell_pq(theta)=0 and no two-sparse stress is certified.
- falsifier: same-regulator diagonal upper bounds or OPE intervals are too wide, making tau_pq(theta) nonnegative for all endpoint pairs.
- falsifier: the raw K4 interval changes under an alleged Wilson quotient symmetry, exposing non-invariant enumeration.
- falsifier: Gaussian, K4, OPE, and Schur inputs use mismatched regulator widths, couplings, or endpoint bases, invalidating same-theory transfer.
- falsifier: a claimed negative stress disappears after adding the H,K Schur subtraction with certified signs and intervals.

## Learning

Conceptual pressure attacked: replace symbolic boundary polarization by a validator-facing connected cumulant witness that can decide a finite Schur-corrected endpoint gate. Declarative tension: Wilson/OPE coefficients, raw connected K4 negativity, OPE errors, and H,K Schur subtraction must jointly control one finite endpoint quadratic form in the same cutoff theory, while OS reconstruction, gauge-invariant observable density, excitation-sector cyclicity, nontrivial continuum YM, and the Hamiltonian mass gap are barred as conclusions. Carrier revision: scalar R is too weak, A012 shells are convenient but quarantined, raw plaquette enumeration is fragmented yet valid, and OS Hilbert observable algebra is too strong and circular for this local gate. Compared with full Delta_raw PSD search, the phase-stress route is a sharper negative tactic because three endpoint interval types can produce a falsifier. Conceptual value signal: sharp and route-changing at finite scope; it unifies Gaussian color positivity, non-Gaussian K4 danger, OPE error, and Schur hairpin energy in one valid inequality without implying Clay.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and validator-facing interval-computation design.`
- Rationale: The branch has already quarantined symbolic R and A012 shells; the only contribution-making move left is to test whether a few raw connected K4 intervals can demote the finite endpoint route before full Delta_raw proof search.
- Situation seed: Finite SU(N) heat-kernel lattice endpoint box for the worked H,K collar/hairpin geometry: choose two reflected endpoint plaquette-sheet nodes p,q and assemble U_pq from Gaussian color square, raw K4 cumulant, OPE interval, and Schur hairpin energy.
- Varied variable: The single varied parameter is rho=ell_pq(theta)/sqrt(u_pp^+ u_qq^+), the phase-sector off-diagonal lower support normalized by the certified diagonal upper scale.
- Held-fixed controls: Same cutoff a, heat-kernel width sigma, renormalized coupling g_R, finite volume, and endpoint Wilson basis., Same H,K Schur blocks, reflection plane, vacuum/perimeter subtraction, color trace normalization, and OPE error budget., Exact Wilson quotienting policy and finite endpoint-box complexity budget.
- Expected observation: If rho>1 for some phase sector then tau_pq(theta)<0 and the H,K endpoint positivity route is demoted by a concrete stress vector; if rho<=1 for all certified sectors, the two-sparse negative tactic is exhausted and full Delta_raw PSD search is required.
- Transfer certificate needed: A same-theory raw plaquette interval certificate for Re(e^{-i theta}U_pq), U_pp, and U_qq, with gauge-invariant enumeration, exact quotient audit, OPE interval proof, and Schur subtraction in the identical endpoint basis.

## Next Experiment

Proof search: choose the first concrete H,K endpoint pair p,q, compute same-regulator raw K4 phase intervals for the connected cumulant witness, assemble tau_pq(theta), and either output x_stress as a finite falsifier or quarantine and move to full Delta_raw PSD search; keep gauge-invariant observable density and OS spectral transfer as explicit non-claims.

