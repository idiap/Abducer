# cycle-0263

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Post-H,K Wilson endpoint-box R/kappa4 interval certificate

## Candidate Lemma

For the first concrete three-hairpin Wilson block, after the known H,K Feshbach reduction and the Wick-square/straight-ff cancellations, the remaining connected endpoint polarization is controlled by a clipped interval sum. A positive lower endpoint interval promotes the finite same-theory OS block; a negative upper interval is a finite Wilson falsifier. This changes only the reflection-positivity transfer gate, not continuum existence or the Hamiltonian mass-gap gate.

## Definitions

- source object: a regulated SU(N) Yang-Mills heat-kernel plaquette-sheet endpoint-box family Z_v(s;a,eta) with Wilson source X_v inserted in the locked three-hairpin null channel.
- target object: the finite corrected Schur-Feshbach null scalar for the intended same-theory Wilson OS matrix after H,K are fixed, before any Clay mass-gap conclusion.
- controlled interface: source-derivative intervals for connected endpoint fourth cumulants are contracted with endpoint incidence intervals and exported as one scalar interval I_tot for the OS positivity gate.
- same-theory condition: the heat-kernel action, Wilson normalization, representation, reflection collar collapse, and endpoint source differentiations are all performed in the same regulated gauge-invariant theory and have cutoff-uniform remainders.

## Assumptions

- Model: four-dimensional Euclidean lattice SU(N) Yang-Mills with heat-kernel plaquette action, gauge-invariant Wilson loop algebra, and reflection plane t=0.
- Regime: fixed finite three-hairpin block with already computed H,K; endpoint boxes of side eta surround only hairpin/collar endpoints and exclude straight shared boundary interiors.
- Uniformity: source derivatives of log Z_v through order eight and endpoint-tail cumulants are bounded uniformly in a along the chosen cutoff-removal subnet.
- Cancellation: connected logarithms remove Wick-square disconnected contractions, and the null-channel incidence identity removes straight-segment C_A f f contact terms before endpoint estimates are applied.
- Naturalness: endpoint partition and source coordinates are local and do not introduce boundary counterterms or an enlarged Wilson observable algebra.
- Non-claim boundary: this is a finite Route A sign certificate, not a construction of the full four-dimensional continuum Yang-Mills theory and not a proof of a positive mass gap.

## Equations

- endpoint_source_cumulant: `\kappa_{4,v}^{\mathrm{sing}}(a,\eta)=\left.\partial_s^4\log Z_v(s;a,\eta)\right|_{s=0}=\langle X_v^4\rangle_{c,a,\eta}`. Valid when: Valid when the heat-kernel source couples only to the singlet-projected endpoint plaquette-sheet flux X_v in the locked Wilson block.
- negative_kappa_interval: `-\kappa_{4,v}^{\mathrm{sing}}\in[\beta_v^-,\beta_v^+],\qquad 0\le \beta_v^-\le \beta_v^+`. Valid when: Applies after the compact-group fourth cumulant and finite-difference remainder are enclosed by same-theory source-derivative bounds.
- endpoint_dominance_incidence: `D_v=2G_{12,v}-4G_{13,v}-4G_{23,v},\qquad D_v\in[d_v^-,d_v^+]`. Valid when: Requires the three fixed hairpin footprints, the Feshbach null vector contraction, and endpoint-box geometric incidence intervals.
- clipped_lower_endpoint_bound: `I_{\mathrm{end}}^- = M_G+C_N\sum_v\left(\beta_v^-[-d_v^+]_+-\beta_v^+[d_v^+]_+\right)+T_{\mathrm{tail}}^-`. Valid when: Valid when beta intervals are nonnegative, D_v intervals enclose all endpoint incidences, and all nonlocal overlap is charged to T_tail.
- finite_block_decision: `I_{\mathrm{end}}^->0\Rightarrow q_{\mathrm{3hp}}\ge0,\qquad I_{\mathrm{end}}^+<0\Rightarrow \exists z\perp 1: z^*q_{\mathrm{3hp}}z<0`. Valid when: Valid after the H,K Schur-Feshbach reduction and after endpoint intervals enclose every remaining connected R contribution.

## Attempted Derivation

- Conceptual pressure: make endpoint collapse sign-certifiable without changing the Wilson theory; the declarative tension is collar OS positivity plus same gauge-invariant algebra plus endpoint OPE singularity, with the missing mediator being a cutoff-uniform signed endpoint representation.
- Critique of current carrier: raw R is representation-limited because it hides incidence signs; a full Schur-preimage matrix test is valid but too global after H,K; the clipped endpoint carrier is local and directly computable from same-theory source derivatives.
- Start from the corrected H,K Feshbach null scalar and isolate the remaining connected boundary-OPE endpoint term; one-body and length-linear terms are already removed by the Schur correction.
- Use log Z_v source derivatives, so disconnected Wick-square contractions do not enter kappa_4; use the null incidence identity to cancel straight C_A f f contacts before endpoint boxes are summed.
- Write each endpoint contribution as -C_N beta_v D_v plus its allocated tail, with beta_v>=0 enclosing the negative compact-group fourth cumulant and D_v=2G12-4G13-4G23 enclosing incidence dominance.
- Apply monotone interval arithmetic to the product beta_v D_v; positive D_v is dangerous, negative D_v is protective, giving the clipped lower bound beta_v^-[-d_v^+]_+-beta_v^+[d_v^+]_+.
- Hard gate: if I_end^->0, the finite same-theory OS positivity gate for this block is promoted; if I_end^+<0, the branch has a finite Wilson falsifier. The continuum limit, OS density, Wightman reconstruction, and mass-gap gates remain untouched.

Blocking gap: No certified table of beta_v intervals, D_v incidence intervals, and T_tail bounds has yet been computed for the actual SU(N) endpoint boxes with cutoff-uniform constants.

## Falsifiers

- falsifier: a certified endpoint configuration with d_v^+>0 and beta_v^+ large enough that I_end^+<0 gives a negative corrected null-channel OS form.
- falsifier: source-derivative intervals for log Z_v fail to be uniform in the cutoff a, so the finite endpoint sign does not transfer to the regulated continuum passage.
- falsifier: endpoint overlap cannot be localized and T_tail becomes comparable to or larger than the positive Gaussian margin M_G.
- A valid stress case is 12-endpoint dominance, G12>4(G13+G23) in symmetric boxes, where the negative compact-group kappa_4 becomes dangerous rather than protective.
- A same-theory failure occurs if the endpoint source computation requires a boundary counterterm, altered Wilson normalization, or a different test algebra.

## Learning

Cycle 263 attacks the conceptual pressure of making endpoint collapse sign-certifiable in the same Wilson theory. The declarative tension is explicit: finite collar OS positivity, unchanged gauge-invariant Wilson observables, and singular endpoint boundary OPE must coexist, but raw R is too representation-limited to mediate them. The new local value signal is sharpness: negative kappa_4 is not the obstruction; only clipped positive endpoint dominance plus uncontrolled tail can demote the block. Efficient representation requirements are now fixed: encode endpoint boxes, beta intervals, D_v intervals, color factors, and tails; preserve Wilson normalization, null-channel cancellations, and cutoff uniformity; use source differentiation, interval arithmetic, incidence contraction, and tail addition; identify carriers only by equal regulated source derivatives; export a scalar interval to the finite OS gate. Success changes the proof state by promoting or falsifying this finite post-H,K Wilson block; it leaves continuum construction and mass gap untouched but removes a paper-handoff obstruction.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and endpoint-data guide.`
- Rationale: The branch has already reduced the post-H,K obstruction to endpoint intervals; another abstract OS restatement would loop, while a concrete dominance experiment tests whether the remaining R/kappa_4 term can actually demote the finite block.
- Situation seed: Regulated SU(3) heat-kernel plaquette-sheet endpoint box for the fixed three-hairpin null channel, with one endpoint box shared more strongly by the 12 pair than by the 13 and 23 pairs.
- Varied variable: Endpoint dominance ratio r=G_{12,v}/(G_{13,v}+G_{23,v}) at fixed beta_v and fixed tail budget.
- Held-fixed controls: The same heat-kernel lattice action, Wilson representation, and source derivative definition of kappa_{4,v}^{sing}., The previously fixed H,K collar/hairpin data and corrected Schur-Feshbach null vector., The cancellation rules: connected log removes Wick-square terms and null incidence removes straight f f contacts., The Clay target boundary: no inference to continuum existence or mass gap from this finite endpoint probe.
- Expected observation: For r below the clipped dominance threshold the negative compact-group kappa_4 is protective or harmless; for sufficiently large r and small tail uncertainty the interval I_end can cross zero, producing either a finite promotion certificate or a concrete falsifier.
- Transfer certificate needed: A cutoff-uniform source-derivative bound for beta_v, a verified endpoint incidence table for G_ij,v, and a locality estimate charging all box overlap and corner remainder to T_tail before the intuition may affect proof obligations.

## Next Experiment

Compute a one-box SU(3) heat-kernel source-derivative interval for beta_v using the seven-point fourth-derivative stencil, then pair it with a hand-verified G12/G13/G23 incidence table for the most 12-dominant endpoint; report I_end^- and I_end^+ with tail assumptions separated.

# Endpoint-box R++ interval certificate via Ward-subtracted flowed Wilson kernels

## Candidate Lemma

Finite regulated endpoint-box enclosure: for known H,K hairpin sheets, the plus-channel endpoint contribution R_{++}^{ren}/kappa_4 has a rigorous interval lower bound obtained from the positive pair contraction plus a Ward-subtracted interval enclosure of the connected four-curvature polarization Xi_{++}. This changes only the finite post-H,K endpoint-box positivity gate; it does not construct the continuum YM theory or prove a Hamiltonian mass gap.

## Definitions

- source object: a finite-cutoff SU(N) Euclidean Yang-Mills Wilson measure with gradient-flow time tau>0, endpoint point-splitting epsilon, and centered renormalized hairpin Wilson observables \widehat W_i=Z_i(W(H_i)-\langle W(H_i)\rangle).
- target object: the finite Schur-Feshbach plus-channel endpoint scalar q_+^{box}=R_{++}^{ren}/\kappa_4-L_+ whose sign decides the local endpoint-box repair after H,K are fixed, not the Clay mass-gap property.
- controlled interface: oriented flowed sheet currents J_i^{\mu\nu}, endpoint currents e_i^\mu, and sector kernels for pair, 3g, 4g, counterterm, and endpoint contractions of the connected Wilson cumulant.
- same-theory condition: all expectations, subtractions, flow kernels, renormalizations, and limits are taken in one Yang-Mills Schwinger family with the same coupling and regulator sequence; no auxiliary Gaussian theory supplies R.
- carrier critique: raw Wilson contours are representation-limited and fragmented; sheet-plus-endpoint currents preserve gauge, color, reflection, and orientation data while making Ward cancellation a primitive.
- efficient representation: encode H,K sheets and endpoints; preserve gauge/color/reflection/orientation invariants; use cumulant expansion, Ward subtraction, and interval integration as primitives; quotient only by same-theory zero-pairing current equivalence; keep finite endpoint-box locality and demote on cusp, plateau, or interval-width falsifiers.

## Assumptions

- Model: pure four-dimensional SU(N), N>=2, in a reflection-positive finite regulator such as the Wilson lattice action, with gradient flow at tau>0 before endpoint point-splitting removal.
- Regime: H,K endpoint boxes are fixed finite Wilson hairpin/collar objects already normalized in the same basis that produced the Schur-Feshbach leakage L_+.
- Uniformity: interval bounds are first finite-cutoff certificates; continuum transfer requires regulator-window stability in a, tau, and epsilon and a same-theory OS-positive limiting Schwinger family.
- Perturbative use: the displayed Xi_{++} formula is valid only where the flowed small-box expansion has an explicit remainder bound E_rem; otherwise the lemma certifies the finite sector integral, not the full cumulant.
- Naturalness: endpoint boxes are small compared with the separation scale d but not sent through a singular limit before the Ward-subtracted cumulant is bounded.

## Equations

- R-pair-plus-polarization: `\frac{R_{++}^{ren}}{\kappa_4}=2(N^2-1)G_{++}+g_R^2N(N^2-1)\Xi_{++}+\mathrm{Rem}_2`. Valid when: Valid when centered flowed hairpins use the same H,K normalization, the same renormalized coupling, and an explicit second-order remainder bound.
- positive-pair-baseline: `G_{++}=\int_{\Sigma_1\times\Sigma_2}J_+^{\mu\nu}(x)J_+^{\rho\sigma}(y)P_{\tau,\mu\nu;\rho\sigma}(x-y)^2\,dx\,dy>0`. Valid when: Applies after diagonal plus-channel normalization of nonzero reflected endpoint sheets with positive flowed two-curvature pairing.
- sector-decomposition: `\Xi_{++}=I_{3g}+I_{4g}+I_{ct}+I_{end},\qquad I_s=\int_{D_s}\omega_s(z)\widetilde K_s(z;\tau,\epsilon)\,dz`. Valid when: Requires the Ward-subtracted same-theory boundary OPE kernels for the fixed H,K endpoint-box geometry.
- interval-enclosure: `\underline\Xi_{++}\le \sum_{s,Q}|Q|\,\inf_{z\in Q}(\omega_s\widetilde K_s)(z)\le \Xi_{++}\le \sum_{s,Q}|Q|\,\sup_{z\in Q}(\omega_s\widetilde K_s)(z)=\overline\Xi_{++}`. Valid when: Valid for a finite cell partition whose interval arithmetic encloses all sector kernels and orientation weights.
- endpoint-box-promotion-test: `2(N^2-1)G_{++}+g_R^2N(N^2-1)\underline\Xi_{++}-E_{rem}>L_+`. Valid when: Applies only after L_+ and R_{++} share the same Schur-Feshbach, Wilson, and kappa_4 normalizations.

## Attempted Derivation

- Conceptual pressure attacked: same-theory Wilson positivity, gradient-flow renormalization, and finite Schur-Feshbach positivity must jointly hold, but the missing mediator is a certified sign/size for Xi_{++}.
- Declarative tension: L_+ is exact in the finite Schur-Feshbach theorem, while R_{++} is a Wilson cumulant needing same-theory renormalized extraction; a symbolic R cannot validly repair the endpoint box.
- Current carrier audit: raw Wilson-loop contours are too fragmented for proof search; sheet currents plus endpoint currents are sharper because gauge/color/orientation invariants and Ward cancellation are explicit.
- Compared route: the old non-Gaussian OS witness route only tested nontriviality; the current interval-kernel route attacks the hard local gate of finite endpoint-box positivity after H,K while leaving continuum existence and mass gap untouched.
- Write the centered hairpin covariance R_{++}^{ren}=kappa_2(\widehat W_+^{(1)},\widehat W_+^{(2)}) after disconnected-product and one-hairpin perimeter/cusp subtractions.
- Expand the flowed Wilson cumulant in endpoint-box sheet currents. The Gaussian pair contractions give two pairings and color factor 2(N^2-1) in the adopted diagonal normalization, hence the positive baseline 2(N^2-1)G_{++}.
- Collect the non-Gaussian connected four-curvature terms into sectors I_{3g}, I_{4g}, I_{ct}, and I_{end}; their common color factor is N(N^2-1) after the same trace normalization.
- Use Ward identities to subtract endpoint Taylor jets from sector kernels; this cancels the disconnected product, perimeter/cusp one-loop remnants, and pure-gauge longitudinal pieces before interval integration.
- Partition each sector domain D_s into cells Q and enclose omega_s and the subtracted kernel \widetilde K_s by interval arithmetic, producing [\underline\Xi_{++},\overline\Xi_{++}].
- Compare the rigorous lower endpoint 2(N^2-1)G_{++}+g_R^2N(N^2-1)\underline\Xi_{++}-E_rem with the finite leakage L_+.

Blocking gap: No certified numerical or symbolic enclosure of the actual H,K sector kernels has yet been produced; the perturbative remainder E_rem and regulator-window plateau also need explicit bounds.

## Falsifiers

- falsifier: Ward-subtracted sectors retain a log epsilon cusp or perimeter divergence in the same H,K normalization.
- falsifier: the certified upper bound satisfies \overline R/\kappa_4<=L_+, killing this endpoint-box repair.
- falsifier: G_{++}=0 because the reflected hairpin endpoint geometry has zero plus-channel two-curvature pairing.
- falsifier: interval widths remain larger than |2(N^2-1)G_{++}-L_+| under admissible cell refinement.
- falsifier: regulator-window tests in a, tau, and epsilon show no stable plateau for Xi_{++}.
- falsifier: a color-normalization mismatch moves the pair coefficient away from 2(N^2-1) in the same Schur-Feshbach basis.
- falsifier: the observable is not in the reconstructed OS algebra of the same limiting Schwinger family.

## Learning

The non-looping move is to make R_{++} an interval-enclosed flowed Wilson cumulant. The sharp conceptual value signal is local route-changing: a vague endpoint-box polarization becomes a valid inequality with color factors, Ward cancellation, sector kernels, and falsifiers. Success would change one hard gate, finite endpoint-box positivity after H,K; failure would quarantine this repair while leaving the Clay gates of continuum construction, OS/Wightman axioms, nontriviality, and positive Hamiltonian mass gap untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design concrete falsifier probe now.`
- Rationale: The branch needs a target-preserving endpoint-box computation, not another abstract Wilson/OS restatement; the local hard gate is whether R_{++}/kappa_4 can beat L_+ for the actual H,K instance.
- Situation seed: Take SU(2) Wilson lattice Yang-Mills with gradient flow, two reflected rectangular endpoint hairpins representing the first H,K plus-channel collar, centered by identical flowed renormalization, and compute the finite endpoint-box covariance by sector kernels on a hypercubic cell partition.
- Varied variable: rho=sqrt(8*tau)/epsilon, the flow-radius to endpoint point-splitting ratio.
- Held-fixed controls: Same Wilson action, bare coupling sequence, and reflection-positive regulator family., Same H,K sheet geometry, endpoint orientation, kappa_4 normalization, and Schur-Feshbach leakage L_+., Same disconnected-product, perimeter, and cusp subtraction scheme inside the Wilson cumulant., Same color trace normalization giving pair coefficient 2(N^2-1).
- Expected observation: A stable positive lower interval for R_{++}/kappa_4-L_+ over a nonempty rho window promotes the endpoint-box repair; a negative upper interval or nonshrinking interval width demotes it.
- Transfer certificate needed: Uniform same-theory bounds allowing a,tau,epsilon window comparison, verified Ward/cusp cancellation, explicit perturbative or lattice-flow remainder control, and exact matching to the H,K Schur-Feshbach normalization.

## Next Experiment

Forge the explicit SU(2) first-H,K endpoint sheets as sheet/end currents, derive the four sector kernels with Ward subtraction, run a coarse interval partition for rho in {1,2,4}, and test whether \underline R/\kappa_4-L_+ or \overline R/\kappa_4-L_+ separates sign.

# Post-H,K endpoint-box kappa4 shell certificate

## Candidate Lemma

Finite shell-envelope certificate for the post-H,K endpoint-box term: after H,K are fixed, the Schur-corrected endpoint matrix is positive on the finite Wilson endpoint subspace if the Gaussian Hadamard-square margin dominates the connected four-curvature negative shell envelope, the OPE remainder, and the Schur hairpin subtraction.

## Definitions

- source object: heat-kernel regulated SU(N) Yang-Mills Wilson cumulants of transported plaquette-sheet curvature fluxes in a finite endpoint box B, with cutoff a, flow time sigma, renormalized coupling g_R(sigma), and finite Wilson endpoint index set I.
- target object: the finite Hermitian endpoint-box quadratic form Q_sigma(I) whose nonnegative spectrum certifies local Route A endpoint positivity for the fixed H,K truncation.
- controlled interface: sheet-kernel hypergraph encoding sheets, weights, transporters, color tensors, dyadic shell labels, Gaussian covariance C_sigma, connected four-curvature cumulant K4_sigma, OPE error E_OPE,sigma, and Schur data S_HK=B^*E^{-1}B.
- same-theory condition: C_sigma, K4_sigma, E_OPE,sigma, H, K, and S_HK are extracted from the same regulated YM measure, Wilson normalization, gauge group, endpoint boxes, and heat-kernel scale before any continuum or Hamiltonian transfer is claimed.
- M4_sigma^-(I) is the operator norm of the negative part of the compressed connected four-curvature cumulant P_I K4_sigma P_I.
- m_G is the smallest eigenvalue of alpha_N g_R(sigma)^4 P_I(C_sigma circ C_sigma)P_I on the endpoint subspace; s_HK is the top eigenvalue of the finite Schur subtraction.

## Assumptions

- Model: finite heat-kernel regularized SU(N) Yang-Mills Wilson observable calculation in a fixed endpoint-box truncation, not an OS reconstruction theorem.
- Regime: sigma>0 and a>0 are fixed with endpoint boxes separated from the reflection plane as required by the reflected Wilson construction.
- Uniformity: all matrix entries are computed with the same regulator, coupling convention, transport paths, and vacuum subtraction; no change of theory is allowed between R, H,K, and the Schur inverse.
- Schur validity: the complement block E=QHQ is strictly positive on the finite hairpin complement, so S_HK=B^*E^{-1}B is a valid second-order Feshbach subtraction.
- OPE control: the boundary OPE remainder has a certified operator-norm bound e_OPE on the same finite endpoint subspace.
- Shell control: the connected kappa4 entries admit dyadic shell bounds b_l and a tail T_L after quotienting only by Wilson sheet symmetries and trace identities.
- Naturalness boundary: this is a finite Route A certificate; it changes only the endpoint-box positivity gate and leaves OS/Wightman reconstruction, continuum existence, and the Hamiltonian mass gap untouched.

## Equations

- endpoint R decomposition: `R_{\partial,\sigma}=\alpha_N g_R(\sigma)^4\,P_I(C_\sigma\circ C_\sigma)P_I+\frac{g_R(\sigma)^4}{16N^2}P_IK_{4,\sigma}P_I+E_{\mathrm{OPE},\sigma},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid when Wilson observables are expanded into transported curvature fluxes with heat-kernel smoothing, connected vacuum subtraction, and identical endpoint compression.
- connected four-curvature Wilson cumulant: `(K_{4,\sigma})_{ij}=\int_{\Sigma_i^2\times\Sigma_j^2}\mathcal W_i^{ab}(x_1,x_2)\mathcal W_j^{cd}(y_1,y_2)\langle F^a_\sigma(x_1)F^b_\sigma(x_2)F^c_\sigma(y_1)F^d_\sigma(y_2)\rangle_c\,d\mu`. Valid when: Valid when transported curvature insertions are parallel transported to the Wilson basepoints and only the connected four-point cumulant remains after perimeter and vacuum cancellations.
- dyadic shell negative-spectrum envelope: `M^-_{4,\sigma}(I):=\|(P_IK_{4,\sigma}P_I)_-\|\le \max_{i\in I}\sum_{\ell=0}^{L} n_i(\ell)b_\ell+T_L`. Valid when: Applies after sheet-kernel entries are grouped into dyadic geometric shells with certified entry envelopes b_l and a same-regulator tail bound T_L.
- Schur-corrected promotion margin: `Q_\sigma(I):=R_{\partial,\sigma}-S_{HK,\sigma}\succeq \Delta_\sigma(I)P_I,\quad \Delta_\sigma=m_G-\frac{g_R(\sigma)^4}{16N^2}M^-_{4,\sigma}-e_{\mathrm{OPE}}-s_{HK}`. Valid when: Requires known H,K Schur data, a positive complement block, certified OPE error, and the same finite endpoint basis used for all compressed matrices.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Observable Density In The Excitation Sector; source object: heat-kernel regulated SU(N) Yang-Mills Wilson cumulants of transported plaquette-sheet curvature fluxes in a finite endpoint box B, with cutoff a, flow time sigma, renormalized coupling g_R(sigma), and finite Wilson endpoint index set I.; target object: the finite Hermitian endpoint-box quadratic form Q_sigma(I) whose nonnegative spectrum certifies local Route A endpoint positivity for the fixed H,K truncation.; Model: finite heat-kernel regularized SU(N) Yang-Mills Wilson observable calculation in a fixed endpoint-box truncation, not an OS reconstruction theorem..
- Conceptual pressure attacked: the post-H,K route needs a mediator between actual connected Wilson cumulants and Schur-corrected endpoint positivity, not another OS observable-density restatement.
- Declarative tension: same-theory Wilson/OPE coefficients, finite Schur-Feshbach subtraction, and endpoint positivity must jointly hold; the missing mediator was a representation that preserves color, sheet geometry, connected-cumulant subtraction, and finite locality.
- Critique of carrier: scalar R is too weak and representation-limited; full OS gauge-invariant density is too strong for this local gate; raw plaquette enumeration is fragmented unless quotienting preserves Wilson trace identities.
- Chosen abstraction: the sheet-kernel hypergraph encodes sheets, weights, transporters, color tensors, shell labels, and Schur data while preserving gauge invariance, reflection support, Gaussian/kappa4 separation, and endpoint compression.
- Expand each endpoint Wilson carrier to quadratic transported curvature flux with heat-kernel smoothing; connected subtraction cancels vacuum and perimeter terms.
- Use SU(N) trace contractions to isolate the PSD Gaussian term alpha_N g_R^4(C_sigma circ C_sigma) and the dangerous connected four-curvature term g_R^4 K4_sigma/(16N^2).
- Compress all terms to the same finite endpoint basis P_I and subtract the Schur-Feshbach hairpin term S_HK from the already known H,K data.
- Bound the negative spectral size of P_IK4_sigmaP_I by a dyadic shell row-sum envelope plus a same-regulator tail, giving a rigorous sufficient margin Delta_sigma.
- Hard gate: Delta_sigma>0 promotes the finite endpoint positivity certificate; a certified negative Rayleigh vector is a falsifier and demotes the Wilson collar/hairpin branch.

Blocking gap: The remaining gap is not formal decomposition but data: rigorous interval bounds for the actual connected four-curvature shell envelopes b_l, the tail T_L, and the same-regulator OPE norm are still missing for the first concrete H,K geometry.

## Falsifiers

- falsifier: interval evaluation of the first endpoint-box H,K case yields a vector v with v^*Q_sigma v<0 after the Schur subtraction.
- falsifier: the connected kappa4 shell tail T_L is nonuniform as a/sqrt(sigma) is controlled, so no valid same-theory endpoint certificate survives refinement.
- falsifier: Wilson sheet symmetry quotient changes a K4 matrix entry or color factor, showing the sheet-kernel carrier is representation-limited.
- Stress case: nearly null Gaussian PSD direction where m_G is small and the Schur hairpin energy alone can overwhelm the endpoint R term.
- Failure case: OPE remainder bound e_OPE is larger than m_G-s_HK, making the sign test inconclusive even if kappa4 is small.

## Learning

The contribution-making move is a finite post-H,K certificate: R is a same-theory connected Wilson cumulant, not a scalar placeholder. The efficient carrier is the sheet-kernel hypergraph because it preserves color factors, sheet geometry, locality shells, cumulant cancellation, and Schur data; scalar R was too weak, full OS density was too strong, and raw plaquette enumeration was fragmented. The hard gate is Delta_sigma: success changes only the finite Route A endpoint-box positivity gate, while OS/Wightman reconstruction, nontrivial continuum existence, and a positive Hamiltonian mass gap remain untouched. The conceptual value signal is sharp and route-changing at finite scope: it turns the unknown kappa4 obstruction into a computable sign/size certificate or falsifier without weakening Clay target commitments.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The abstraction is fixed enough; another abstract restatement would not decide the hard gate. The branch now needs a concrete same-theory shell-envelope estimate for the connected kappa4 term.
- Situation seed: Heat-kernel regulated SU(N) plaquette-sheet endpoint-box audit for the first known H,K collar/hairpin geometry, with Wilson carriers expanded into transported curvature sheets and compressed to the finite endpoint basis I.
- Varied variable: dyadic shell cutoff L in the sheet-kernel hypergraph for K4_sigma.
- Held-fixed controls: Gauge group SU(N), heat-kernel flow time sigma, cutoff a, and renormalized coupling convention are held fixed during the shell audit., The finite Wilson endpoint basis I and the already extracted H,K Schur data are held fixed., Vacuum subtraction, transport paths, trace normalization, and endpoint boxes are identical for C_sigma, K4_sigma, E_OPE,sigma, and S_HK.
- Expected observation: The partial shell sum for M4_sigma^-(L) either stabilizes below the Gaussian-minus-Schur margin, giving Delta_sigma>0, or crosses the margin and identifies a negative-eigenvector search region.
- Transfer certificate needed: A rigorous same-regulator tail bound T_L, certified interval arithmetic for color/geometric K4 entries, and a proof that the Wilson symmetry quotient preserves all compressed matrix elements before the intuition may affect proof obligations.

## Next Experiment

For the first available H,K collar/hairpin endpoint geometry, instantiate the sheet-kernel hypergraph, compute C_sigma and the color/geometric K4_sigma entries by dyadic shells, bound T_L and e_OPE, then evaluate Delta_sigma and search for a negative Rayleigh witness if the margin is nonpositive.
