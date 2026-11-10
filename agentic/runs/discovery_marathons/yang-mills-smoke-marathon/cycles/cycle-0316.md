# cycle-0316

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: finite endpoint kappa_4 screen

## Candidate Lemma

In the heat-kernel plaquette-sheet regulator for the locked three-hairpin Wilson block, the post-H,K endpoint contribution admits a valid clipped lower screen: if I_scr^->0 then this finite Schur-Feshbach gate is promoted; if a certified interval has I_+<0 then the block gives a finite same-theory falsifier. This is not a Clay mass-gap theorem.

## Definitions

- source object: source-equivalent endpoint classes c, each carrying seven regulated values of log Z_c(s) for the null-channel endpoint source L_c and signed fractional incidences b_{ij,c}.
- target object: the finite post-H,K reflected-Wilson OS transfer scalar for the same locked three-hairpin block, not the continuum Yang-Mills theory or its spectral gap.
- controlled interface: the carrier C_ep maps endpoint source cumulant intervals and signed incidences to one scalar interval [I_-,I_+] entering the Schur-Feshbach reduced gate.
- same-theory condition: the Wilson loops, heat-kernel regulator, source derivatives, endpoint classes, and tail bound are computed in the same gauge-invariant theory without boundary counterterms or observable-algebra changes.
- endpoint dominance: D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}; only D_c>0 can turn a negative endpoint cumulant into a dangerous contribution.
- recovery map: Rec(C_ep)=M_G+C_N sum_c D_c kappa_c+T_tail, where C_N=(g^4/4)(T_F/N)^2 and M_G is the already-certified positive Schur-Feshbach margin.

## Assumptions

- Model: four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette-sheet Wilson regularization and fundamental trace normalization T_F=1/2.
- Regime: endpoint boxes are small enough for exponential-coordinate Haar-Jacobian expansion and separated enough that non-endpoint contacts are assigned to T_tail.
- Cutoff: all cumulant intervals, endpoint source stencils, and tail estimates are uniform in lattice spacing over the finite block being certified.
- Same-theory: source insertion differentiates the original Wilson observable family and does not introduce a boundary state, gauge fixing artifact, or modified Wilson renormalization.
- Local: Wick-square Gram terms and straight f f commutator contacts have already been removed by the valid H,K null-channel cancellations.
- Validity: the lemma is a finite Route A screen only; it leaves continuum Schwinger coherence, OS reconstruction for all observables, nontriviality, and mass gap untouched.

## Equations

- endpoint root-quartic cumulant: `\kappa_c=\partial_s^4\log Z_c(s)\vert_{s=0}=-\frac{t_c^4}{60}R_4(Y_c)+E_c,\quad R_4(Y)=N\operatorname{tr}(Y^4)+3(\operatorname{tr}(Y^2))^2\ge0`. Valid when: Valid when the heat-kernel endpoint coordinate chart is small, the source direction is traceless Hermitian after multiplying by i, and the Haar-Jacobian normalization is fixed before cutoff removal.
- signed endpoint dominance: `D_c=2b_{12,c}-4b_{13,c}-4b_{23,c},\quad [D_c]_+=\max(D_c,0)`. Valid when: Valid when b_{ij,c} are the same regulated fractional endpoint incidences used in the H,K null-channel contraction and source-equivalence aggregation.
- same-theory endpoint recovery: `I_{\rm gate}=M_G+C_N\sum_cD_c\kappa_c+T_{\rm tail}`. Valid when: Valid when the endpoint carrier contains all connected boundary-OPE fourth cumulants and every omitted large-field, corner, or topology term is charged to T_tail uniformly.
- clipped promotion screen: `I_{\rm scr}^-:=M_G-C_N\sum_c [D_c]_+\left(\frac{t_c^4}{60}R_4(Y_c)+\eta_c\right)-|T_{\rm tail}|\,>0`. Valid when: Applies after source classes are fixed, root-quartic remainders satisfy |E_c|<=eta_c, and protective D_c<=0 contributions are deliberately discarded rather than used.

## Attempted Derivation

- Freeze the Clay claim level: only a finite reflected-Wilson Schur-Feshbach endpoint scalar is under discussion; continuum OS/Wightman reconstruction and mass gap remain untouched.
- Use the heat-kernel endpoint source Z_c(s) and compute the connected fourth cumulant by the seven-point stencil; the connected log removes Wick-square Gram terms already known to be safe.
- Insert the SU(N) endpoint Haar-Jacobian expansion, giving the leading negative root-quartic term -(t_c^4/60)R_4(Y_c) plus a uniform remainder E_c.
- Contract with the actual null-channel signed incidence D_c=2b12-4b13-4b23; this identifies positive-D leakage as the only dangerous use of the negative cumulant.
- Apply source-equivalence compression before clipping, so protective and dangerous incidences with identical source data cancel in the valid same-theory carrier.
- Discard all D_c<=0 protective terms and bound E_c plus endpoint/corner leftovers by eta_c and T_tail, producing the conservative screen I_scr^-.
- Conclude finite promotion only if I_scr^->0; conclude finite falsifier only if the full certified interval has I_+<0; otherwise keep quarantine.

Blocking gap: The actual endpoint source stencils, fractional b_ij incidences, uniform eta_c bounds, and T_tail interval are not yet supplied for the validator-facing three-hairpin geometry.

## Falsifiers

- A validator source class with D_c>0 and a negative fourth connected cumulant large enough to make I_+<0 is a finite same-theory falsifier.
- A nonuniform T_tail from large-field or topological sectors invalidates the screen even if endpoint root-quartic terms look safe.
- A boundary counterterm or endpoint Wilson renormalization not present in the original observable algebra breaks the same-theory condition.
- Two endpoint boxes that are geometrically similar but have different regulated source stencils falsify source-equivalence compression.
- If the heat-kernel endpoint chart leaves the small-box regime, the root-quartic cap is not valid and the branch must demote to raw stencil intervals.

## Learning

Conceptual pressure attacked: endpoint collapse must be sign-certified inside the same Wilson theory. Declarative tension: finite collar OS positivity, fixed gauge-invariant Wilson observables, and a singular connected endpoint OPE must coexist without a boundary theory, while H,K and the half-overlap shield do not decide the scalar. Carrier audit: raw R is too weak, raw kappa_4 spectra are too strong, and global Schur-preimage positivity is valid but too coarse after H,K. The efficient representation C_ep encodes endpoint source classes, seven source values, cumulant intervals, signed incidences, C_N, M_G, and T_tail; preserves Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; uses source differentiation, interval arithmetic, source-equivalence, color multiplication, clipping, incidence contraction, and tail addition; identifies equivalence only by regulated source data; exports [I_-,I_+] to the finite gate. Conceptual value signal: sharp finite route change. Negative SU(N) root-quartic endpoint cumulants are explanatory but not the obstruction; positive-D leakage plus uncontrolled tail is.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe while keeping the branch quarantined until source data are supplied.`
- Rationale: The branch has exhausted abstract OS closed-cone and symbolic R analysis; the remaining proof state is a finite same-theory endpoint connected cumulant witness with signed incidences.
- Situation seed: SU(3) hypercubic heat-kernel plaquette-sheet endpoint box for three reflected Wilson hairpins sharing one reflection-plane endpoint; compute seven source values of log Z_c(s) for the null-channel source and recover kappa_c.
- Varied variable: Fractional endpoint overlap alpha=(b13+b23)/b12, with D_c=2b12-4b13-4b23 varied through the half-overlap shield alpha=1/2.
- Held-fixed controls: Same locked gauge-invariant Wilson hairpin observables and reflection map throughout the experiment., Heat-kernel regulator, fundamental trace normalization, and source-equivalence policy fixed before clipping., Previously certified Wick-square Gram positivity and straight f f null-incidence cancellation held fixed., No boundary counterterm, gauge fixing change, or observable-algebra enlargement allowed.
- Expected observation: For alpha>=1/2 the negative root-quartic cumulant is protective or neutral; for alpha<1/2 the finite gate is controlled by the quantitative competition M_G versus C_N[D_c]_+|kappa_c| plus T_tail.
- Transfer certificate needed: A cutoff-uniform endpoint stencil interval, source-equivalence proof, and tail bound showing that Rec(C_ep) is the same-theory Wilson scalar entering the Schur-Feshbach gate.

## Next Experiment

Run proof search plus validator-facing endpoint stencil computation for the connected cumulant witness: enumerate source-equivalent endpoint classes, compute seven heat-kernel log Z_c source values, recover kappa_c intervals, aggregate D_c before clipping, add C_N, M_G, and T_tail, then decide promote, falsifier, or continued quarantine.

# Gauge-Invariant Nontriviality Witness Selection -> finite endpoint R certificate

## Candidate Lemma

For the finite H,K plus-channel endpoint box, the renormalized flowed Wilson covariance R_{++}^{ren} has a certified lower interval equal to a positive two-curvature pair term minus Ward-Hessian sector majorants for the connected four-curvature polarization and recovery errors. If this interval exceeds the Schur-Feshbach leakage L_+, the local endpoint-box positivity gate is promoted; if not, the R repair is quarantined.

## Definitions

- source object: centered gradient-flow Wilson hairpin observables on a finite SU(N) hypercubic regulator, encoded as endpoint sheet currents J_+ with one-hairpin perimeter and cusp counterterms subtracted.
- target object: the scalar post-H,K endpoint mediator R_{++}^{ren} entering the plus-channel Schur-Feshbach endpoint-box inequality against the finite leakage L_+.
- controlled interface: the same-theory centered flowed cumulant map J_i,J_j -> kappa_2(W_t[J_i],W_t[J_j])_c^{ren}, expressed after zero-pairing quotienting by endpoint-cell moments and sector kernels.
- same-theory condition: the regulator, flow time, counterterms, recovery map from raw hairpins, and Wilson cumulants are all taken inside one cutoff family before any continuum or OS spectral-transfer claim.
- J_+ denotes the plus-channel endpoint sheet current after reflection pairing; its Ward-subtracted endpoint moments satisfy M_0(J_+)=M_1(J_+)=0 in the certified geometry.
- G_{++} is the flowed two-curvature cross-pairing of the two plus-channel endpoint currents; H_{4,s} is the outward-rounded mixed-Hessian majorant of the Ward-subtracted connected four-curvature sector s in {3g,4g,ct,end}.
- E_rec and E_{>=8} are, respectively, recovery error from raw Wilson hairpins to flowed sheet currents and the bounded higher-order or finite-cutoff cumulant tail.
- Conceptual pressure: finite Schur-Feshbach positivity needs a same-theory Wilson mediator, while positive pair covariance and flow renormalization remain compatible with a negative connected C4 term.

## Assumptions

- Model: finite-volume lattice SU(N) Yang-Mills with Wilson action, gradient-flow observables at positive flow time t, and physical endpoint boxes separated from the reflection plane by the H,K collar geometry.
- Regime: a << sqrt(8t), endpoint cell diameter rho <= eta sqrt(8t), and eta is small enough that the endpoint Taylor remainder is Hessian-dominated but not so small that G_{++} degenerates.
- Cutoff: all constants are finite-a interval enclosures with an explicit recovery error; cutoff-uniform promotion is not claimed until the intervals are stable under a -> 0 at fixed physical geometry.
- Same-theory: the R_{++}^{ren} cumulant, the counterterms, and the finite Schur-Feshbach matrix entries are extracted from the same regulated Wilson measure and the same normalization of the hairpin observables.
- Validity: Ward identities, reflection pairing, cusp subtraction, and plus-channel monopole/dipole cancellation must be verified before the Hessian bound is applied.
- Local: success changes only finite endpoint-box positivity after H,K; Clay existence, OS/Wightman axioms, nontrivial continuum limit, gauge-invariant observable density, and Hamiltonian mass gap remain untouched.

## Equations

- flowed Wilson covariance defining Rpp: `R_{++}^{ren}(t,a)=\kappa_2\!\left(\widetilde W_t[J_+],\widetilde W_t[J_+]\right)_{c}^{ren}`. Valid when: Valid when the centered flowed hairpin observables use the same cutoff Wilson measure, counterterm scheme, and endpoint sheet-current recovery map.
- loop-sector decomposition: `R_{++}^{ren}=g_t^4\,2(N^2-1)G_{++}+g_t^6\,N(N^2-1)C_{4,++}^{WS}+E_{\ge 8}+E_{rec}`. Valid when: Applies in the finite flowed weak-coupling cumulant expansion after disconnected products, one-hairpin perimeter terms, and cusp counterterms have been subtracted.
- Ward-Hessian C4 bound: `|C_{4,++}^{WS}|\le \sum_{s\in\{3g,4g,ct,end\}} H_{4,s}^{+}\,M_{2,+}^2`. Valid when: Requires Ward-subtracted sector kernels with plus-channel endpoint monopole and dipole moments vanishing on each certified endpoint cell partition.
- certified lower interval: `R_{++}^{I,-}=g_t^4\,2(N^2-1)G_{++}^{I,-}-g_t^6\,N(N^2-1)\sum_s H_{4,s}^{I,+}M_{2,+}^{I,+2}-E_{\ge8}^{I,+}-E_{rec}^{I,+}`. Valid when: Valid for outward-rounded interval enclosures of the pair kernel, sector Hessian constants, endpoint moments, recovery error, and higher cumulant tail.
- endpoint-box promotion inequality: `R_{++}^{I,-}>L_+ + \epsilon_F\quad\Longrightarrow\quad Q_{+}^{endpoint}>0`. Valid when: Applies after the finite Schur-Feshbach leakage L_+ is computed in the same H,K basis and the endpoint correction enters the same plus channel.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: centered gradient-flow Wilson hairpin observables on a finite SU(N) hypercubic regulator, encoded as endpoint sheet currents J_+ with one-hairpin perimeter and cusp counterterms subtracted.; target object: the scalar post-H,K endpoint mediator R_{++}^{ren} entering the plus-channel Schur-Feshbach endpoint-box inequality against the finite leakage L_+.; Model: finite-volume lattice SU(N) Yang-Mills with Wilson action, gradient-flow observables at positive flow time t, and physical endpoint boxes separated from the reflection plane by the H,K collar geometry..
- Freeze the Clay target: the branch claims only a finite endpoint-box Wilson calculation or falsifier, not YM existence or mass gap.
- Replace fragmented raw Wilson contours by endpoint sheet currents J_+ and record recovery error E_rec in the same regulated Wilson theory.
- Center each flowed hairpin observable and subtract disconnected product, one-hairpin perimeter term, and cusp counterterm; this makes R_{++}^{ren} a genuine connected Wilson cumulant.
- Expand the flowed covariance through the pair and connected four-curvature sectors: the pair sector is 2(N^2-1)G_{++} and is positive when the endpoint geometry has nonzero cross-pairing.
- Use reflection and plus-channel orientation to impose M_0(J_+)=M_1(J_+)=0 after Ward subtraction; this cancels monopole and dipole contributions of C4.
- Taylor expand each Ward-subtracted C4 sector kernel over endpoint cells; the remaining term is controlled by mixed Hessian constants H_{4,s}^{+} times M_{2,+}^2.
- Combine outward-rounded lower and upper intervals to form R_{++}^{I,-}; compare it with the finite Schur-Feshbach leakage L_+ plus a safety margin epsilon_F.

Blocking gap: The missing proof object is a certified table of sector Hessian constants H_{4,s}^{I,+}, recovery errors E_rec^{I,+}, and tail bounds E_{>=8}^{I,+} stable under the chosen cutoff and flow window.

## Falsifiers

- falsifier: Ward subtraction leaves a nonzero endpoint monopole or dipole moment, invalidating the Hessian-only C4 estimate.
- falsifier: the cusp counterterm used for the raw Wilson hairpin differs from the flowed cumulant subtraction, so the same-theory condition fails.
- falsifier: the positive pair interval G_{++}^{I,-} collapses to zero in the actual H,K endpoint geometry.
- falsifier: a connected sector constant H_{4,s}^{I,+} is so large that R_{++}^{I,-}<=L_+, demoting the endpoint-box repair.
- falsifier: recovery or higher-cumulant tail intervals dominate the pair baseline over the whole valid flow window.
- falsifier: interval widths do not shrink under endpoint-cell refinement, indicating a representation-limited carrier rather than a computable certificate.

## Learning

Cycle 316 converts the endpoint R/kappa_4 problem into a sharper finite certificate: R_{++}^{ren}=positive pair covariance minus Ward-Hessian sector majorants and same-theory recovery errors. The declarative tension is explicit: Schur-Feshbach endpoint positivity, positive flowed Wilson pair covariance, and same-theory recovery can all be individually valid while connected C4 still destroys the mediator. Raw Wilson contours are fragmented and representation-limited; endpoint sheet currents are better because Ward/cusp cancellation, plus-moment cancellation, mixed Hessian bounds, interval arithmetic, and zero-pairing quotienting become primitive. Compared with global OS spectral transfer or a non-Gaussian Schwinger-family route, this local abstraction targets the exact hard gate of finite endpoint-box positivity after H,K. Conceptual value signal: a symbolic boundary-OPE polarization is now a falsifiable color-geometric lower interval with explicit promotion and demotion tests, while all Clay target commitments remain unclaimed.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and proof-search guide.`
- Rationale: The branch has already reduced R_{++} to a sector interval; another abstract restatement would not decide whether the connected C4 term can erase the positive pair mediator.
- Situation seed: Finite SU(N) hypercubic Wilson regulator with the fixed H,K plus-channel endpoint hairpin geometry, gradient-flow time t, and endpoint boxes partitioned into symmetric cells carrying sheet currents J_+.
- Varied variable: eta=rho/sqrt(8t), the endpoint-cell diameter in flow units.
- Held-fixed controls: Same Wilson action, gauge group SU(N), and H,K reflected endpoint geometry., Same gradient-flow time t in physical units while varying cell diameter only., Same centered cumulant, perimeter/cusp subtraction, and recovery map Rec_t., Same finite Schur-Feshbach leakage L_+ and plus-channel normalization.
- Expected observation: If Ward and plus-moment cancellation are effective, the C4 majorant scales like eta^2 M_{2,+}^2 while G_{++} stays positive on an eta plateau; otherwise the lower interval remains negative or unstable and the R repair is falsified.
- Transfer certificate needed: A validator-facing interval table proving Ward moments, cusp cancellation, zero-pairing equivalence, G_{++}^{I,-}, H_{4,s}^{I,+}, E_rec^{I,+}, and E_{>=8}^{I,+} for the same regulated Wilson cumulant before any effect is transferred to the finite Schur-Feshbach proof queue.

## Next Experiment

Route to proof search: build the endpoint-cell interval table for the fixed H,K plus-channel geometry, varying eta, and report whether the connected cumulant witness R_{++}^{ren} has a valid positive margin over L_+ or a falsifier that quarantines the endpoint R repair.

# Raw plaquette K4 interval recovery for finite H,K endpoint gate

## Candidate Lemma

Raw plaquette interval recovery lemma: certified same-regulator K4 intervals, Gaussian covariance, OPE error, and H,K Schur data determine a rigorous interval matrix for the connected boundary polarization R_sigma and its endpoint form U_sigma.

## Definitions

- source object: heat-kernel regulated finite-volume SU(N) Wilson lattice YM at spacing a, smoothing sigma, fixed coupling, and finite H,K endpoint box.
- target object: Schur-corrected finite endpoint quadratic form U_sigma on Wilson endpoint coefficients, with PSD or stress-vector status.
- controlled interface: raw connected plaquette cumulant intervals recover R_sigma and feed U_sigma=R_sigma-S_HK-E_OPE.
- same-theory condition: identical action, coupling, volume, cutoff a, smoothing sigma, endpoint basis, Wilson normalization, and Schur blocks are used.
- observable/carrier: Q_i^sigma=sum_p b_ip T_p F_p^sigma T_p^{-1}; R_ij=cum_2(:Q_i^2:,:Q_j^2:), a connected cumulant witness.
- carrier audit: scalar R is too weak; A012 shells are convenient but quarantined; OS Hilbert observable algebra is too strong here; raw plaquette intervals are fragmented but valid.
- efficient representation: encode oriented plaquettes, sheet weights, transporters, color tensors, cumulant/OPE intervals, and Schur blocks; preserve gauge invariance, reflection, Gaussian-K4 split, exact Wilson quotienting; transfer via Delta_raw or stress falsifier.

## Assumptions

- Model: finite SU(N) Wilson lattice Yang-Mills with heat-kernel smoothing; no continuum or infinite-volume conclusion is claimed.
- Cutoff: sigma>=c a and fixed endpoint-box diameter; the boundary OPE remainder has a certified interval in the same regulator.
- Same-theory: H,K Schur data, Gaussian covariance C, and K4 intervals are computed before any RG or regulator change.
- Validity: vacuum/perimeter normal ordering cancels disconnected Wilson factors, leaving crossed Gaussian contractions plus connected K4 only.

## Equations

- R_raw_decomposition: `R_{ij}^{\sigma}=\alpha_N g_R^4\sum_{p,r}b_{ip}b_{jr}C_{pr}^{\sigma}C_{pr}^{\sigma}+\frac{g_R^4}{16N^2}\sum_{p,q,r,s}b_{ipq}b_{jrs}K_{pqrs}^{(4),\sigma}+E_{ij}^{OPE}`. Valid when: Valid when the heat-kernel boundary OPE is applied after vacuum/perimeter normalization, with the same cutoff, endpoint sheets, and transported curvature basis.
- raw_K4_interval_pushforward: `\mathcal I_{ij}^{K4}=\frac{g_R^4}{16N^2}\sum_{p,q,r,s}b_{ipq}b_{jrs}[\underline K_{pqrs}^{(4),\sigma},\overline K_{pqrs}^{(4),\sigma}]`. Valid when: Valid when each raw plaquette four-curvature cumulant interval is certified in the identical regulator and exact Wilson quotient.
- endpoint_gate: `\Delta_{raw}=\lambda_{min}\big(G^{\sigma}+\underline{\mathcal I}^{K4}-|E^{OPE}|-S_{HK}\big)`. Valid when: Valid when the Schur block, OPE errors, and raw cumulant intervals are expressed in one endpoint basis.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Observable Density In The Excitation Sector; source object: heat-kernel regulated finite-volume SU(N) Wilson lattice YM at spacing a, smoothing sigma, fixed coupling, and finite H,K endpoint box.; target object: Schur-corrected finite endpoint quadratic form U_sigma on Wilson endpoint coefficients, with PSD or stress-vector status.; Model: finite SU(N) Wilson lattice Yang-Mills with heat-kernel smoothing; no continuum or infinite-volume conclusion is claimed..
- Conceptual pressure attacked: mediate real connected Wilson cumulants to Schur-corrected endpoint positivity without inflating a finite Wilson calculation into Clay.
- Expand each endpoint Wilson sheet by the heat-kernel boundary OPE into transported curvature fluxes Q_i^sigma; vacuum/perimeter subtraction removes disconnected pieces.
- Compute cum_2(:Q_i^2:,:Q_j^2:): crossed two-curvature contractions give the PSD color square with alpha_N=(N^2-1)/(8N^2); the remaining non-Gaussian input is K4.
- Push raw K4 plaquette intervals through sheet weights and color tensors, then subtract same-basis OPE intervals and S_HK to form Delta_raw or a stress Rayleigh bound.

Blocking gap: The missing mediator is not conceptual now; it is the actual same-regulator interval table for K_{pqrs}^{(4),sigma} with exact Wilson quotient audit.

## Falsifiers

- falsifier: a stress vector x with x^*U_sigma^+x<0 in the same endpoint basis kills the finite H,K endpoint route.
- Regulator mismatch between raw K4 intervals and H,K Schur data invalidates the transfer, even if each separate estimate is valid.
- Exact Wilson quotienting changes an interval sign or multiplicity; then the raw plaquette carrier is non-invariant and must be demoted.
- OPE error plus S_HK exceeds the Gaussian color-square margin before K4 is added; the branch loses its endpoint positivity budget.

## Learning

Declarative tension: Wilson/OPE, raw K4, OPE error, and S_HK must share one cutoff while Clay gates stay non-claims. Value signal: R is now a validator-facing connected cumulant witness with a raw plaquette interval recovery map, not scalar R or OS-density rhetoric.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the finite H,K endpoint route.`
- Rationale: The branch is looping unless raw same-regulator K4 intervals are produced; varying one computable interval width tests whether proof search can decide Delta_raw.
- Situation seed: Finite SU(N) Wilson lattice endpoint box with fixed collar H,K, heat-kernel smoothing, and raw plaquette K4 interval oracle for the connected cumulant witness.
- Varied variable: rho, the certified half-width of raw K4 intervals after exact Wilson quotienting.
- Held-fixed controls: Same Wilson action, coupling, cutoff a, smoothing sigma, and endpoint Wilson basis., Same H,K Schur blocks, vacuum/perimeter normalization, Gaussian covariance C, and OPE error budget.
- Expected observation: There is a threshold rho_*: below it Delta_raw stays positive or a stress Rayleigh bound becomes negative; above it the finite route is undecidable.
- Transfer certificate needed: A rigorous same-regulator K4 interval table, exact quotient audit, and OPE error certificate before the thought experiment may affect proof obligations.

## Next Experiment

Proof search: compute the first same-regulator raw K4 interval table for the smallest H,K endpoint plaquette set, push it to U_sigma, and decide Delta_raw or exhibit x_stress.

