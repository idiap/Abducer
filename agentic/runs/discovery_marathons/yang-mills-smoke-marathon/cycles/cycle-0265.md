# cycle-0265

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Post-H,K endpoint-box interval certificate for reflected Wilson hairpins

## Candidate Lemma

For the fixed three-hairpin block with H,K already extracted, the remaining connected boundary-OPE polarization R is certified by a finite endpoint-box interval. In the heat-kernel plaquette-sheet regulator, Wick-square terms are positive Gram terms and straight f f contacts cancel in the null channel; the only demotion mechanism is negative connected endpoint kappa_4 multiplied by positive clipped dominance D_v plus uncontrolled tail.

## Definitions

- source object: heat-kernel plaquette-sheet regulator for a fixed SU(N) three-hairpin reflected Wilson block with known H,K, endpoint boxes B_v, and same-theory source partition functions Z_v(s).
- target object: scalar Feshbach null-channel endpoint interval I_tot deciding this finite block's post-H,K OS transfer, not the continuum Yang-Mills mass gap.
- controlled interface: connected boundary-OPE endpoint carrier (beta_v,D_v,T_tail) exported by source derivatives of log Z_v and contracted with the prior null vector.
- same-theory condition: all Z_v(s), Wilson normalizations, endpoint boxes, and tails are computed in the same cutoff Yang-Mills measure as the collar observables, with no boundary counterterm or algebra change.
- carrier critique: symbolic R is representation-limited and raw kappa_4 spectrum is too strong because both hide incidence signs.
- efficient representation: encode endpoint boxes, beta intervals, D_v incidence intervals, color constants, and tails; preserve null-channel cancellations; use source differentiation, interval arithmetic, incidence contraction, and tail addition; identify carriers only through equal regulated source derivatives.

## Assumptions

- Model is four-dimensional Euclidean SU(N) lattice Yang-Mills with heat-kernel plaquette action and gauge-invariant Wilson observables only.
- Regime is a fixed finite reflected Wilson hairpin block after H,K have been computed and before continuum removal is claimed.
- Endpoint boxes are disjoint except for charged overlaps explicitly assigned to T_tail, with cutoff-uniform eighth derivative bounds for source stencils.
- The prior Feshbach null vector and Gaussian margin M_G are held fixed; one-body Wilson renormalizations are already cancelled on 1^perp.
- The same-theory condition forbids adding a reflection-plane counterterm, changing Wilson normalization after the collar limit, or replacing the gauge-invariant algebra.
- Uniformity is only finite-block uniformity in the cutoff and endpoint-box scale; it is not a full OS/Wightman reconstruction theorem.

## Equations

- endpoint_source_cumulant: `Z_v(s;\xi)=\int \exp\{-S_{HK,v}(U)+sX_v(\xi;U)\}\,d\mu_{HK,v}(U),\qquad \kappa_{4,v}(\xi)=\left.\partial_s^4\log Z_v(s;\xi)\right|_{s=0}.`. Valid when: Valid when the endpoint source X_v is the same Wilson flux insertion obtained by differentiating the heat-kernel plaquette-sheet observable in the cutoff theory.
- root_quartic_beta: `-\kappa_{4,v}(\xi)=\beta_v(\xi)=\frac{t_v^4}{60}\sum_{\alpha\in\Phi_+}\bigl(\alpha(\Pi_v\xi)\bigr)^4+O(t_v^5\|\xi\|^4).`. Valid when: Applies in exponential coordinates inside an isolated small heat-kernel endpoint box before cut-locus effects or inter-box tails contribute.
- incidence_dominance: `D_v=2G_{12,v}-4G_{13,v}-4G_{23,v},\qquad G_{ij,v}=\operatorname{Pol}_{ij}\sum_{\alpha\in\Phi_+}\bigl(\alpha(\Pi_v\xi)\bigr)^4.`. Valid when: Valid after Wick-square Gram terms and straight nonabelian f f contacts have been removed by the established null-incidence cancellation.
- interval_export: `I_{\rm tot}=M_G+\sum_v\left(-c_N[\beta_v^-,\beta_v^+][D_v^-,D_v^+]+[-\tau_v,\tau_v]\right).`. Valid when: Requires certified source-derivative intervals for beta_v, certified endpoint incidence intervals for D_v, and cutoff-uniform tail bounds tau_v in the same regulator.
- finite_gate_decision: `\inf I_{\rm tot}>0\Rightarrow q_{\delta}\ge0\ \text{on this block},\qquad \sup I_{\rm tot}<0\Rightarrow \text{finite same-theory OS falsifier}.`. Valid when: Valid for the fixed post-H,K Feshbach null channel with all lower-order kernels and cancellations already locked in the same Wilson theory.

## Attempted Derivation

- Attack conceptual pressure: make endpoint collapse sign-certifiable without changing the Wilson theory or hiding signs inside a symbolic R.
- Start with the fixed three-hairpin Feshbach null channel after H,K; the hard gate is the finite post-H,K reflected-Wilson OS transfer gate.
- Decompose the post-H,K boundary polarization into Wick-square contractions, straight nonabelian f f contact, connected endpoint kappa_4, and tail.
- Use existing cancellations: Wick-square terms are positive Gram contributions and cannot be the falsifier; the straight f f contact cancels by the null-incidence identity for the known hairpin geometry.
- Represent the remaining endpoint term by same-theory source derivatives of log Z_v in heat-kernel plaquette-sheet endpoint boxes.
- In exponential coordinates for SU(N), the Haar factor contributes log J(A)=-sum_{alpha>0} alpha(A)^2/12 - sum_{alpha>0} alpha(A)^4/1440 + higher terms, giving the negative connected fourth cumulant -t_v^4 sum alpha(Pi_v xi)^4/60 to leading order.
- Polarize that fourth cumulant by the Feshbach null pair weights to obtain D_v=2G12_v-4G13_v-4G23_v; hence only D_v>0 can turn negative kappa_4 into a negative OS contribution.
- Export the finite scalar interval I_tot=M_G+sum_v I_v+T_tail; promotion is inf I_tot>0 and a valid finite falsifier is sup I_tot<0.

Blocking gap: The endpoint incidence table D_v and cutoff-uniform tail/eighth-derivative bounds are not yet computed for the actual Wilson footprints; the root-quartic expansion also needs a uniform small-box proof through the chosen cutoff scaling.

## Falsifiers

- A certified heat-kernel endpoint table has c_N sum_v beta_v[D_v]_+ plus tail exceeding the Gaussian Feshbach margin, producing a finite same-theory OS falsifier.
- The source derivative Z_v(s) cannot be identified with the original regulated Wilson plaquette-sheet observable, so the carrier is not same-theory valid.
- Endpoint tails contain a nonlocal connected cumulant not bounded by the assigned tau_v locality budget.
- The exponential-coordinate root-quartic expansion is nonuniform in the cutoff scaling used for endpoint boxes.
- A reflection-plane boundary counterterm is needed to define the endpoint source, changing the target Wilson theory.
- The eighth-derivative stencil bound is too large to decide the sign interval, forcing demotion to undecided rather than promotion.

## Learning

Conceptual pressure: make the singular endpoint collapse sign-certifiable in the same Wilson theory. Declarative tension: finite collar OS positivity, unchanged gauge-invariant Wilson observables, and connected endpoint boundary OPE singularities must jointly hold; the missing mediator is a signed cutoff-uniform endpoint source carrier. Raw R is representation-limited, while a raw kappa_4 spectrum is too strong because it ignores null-channel incidence. Compared with a global Schur-preimage matrix test, the clipped endpoint interval is local, computable after H,K, and exports one scalar to the finite OS gate. The hard gate changed is the finite post-H,K reflected-Wilson OS transfer gate: success promotes this block; failure gives a finite same-theory falsifier. The Clay gates of continuum construction, OS/Wightman reconstruction for all observables, nontriviality, and positive mass gap remain untouched. The conceptual value signal is sharpness: negative compact-group kappa_4 is not the obstruction; positive endpoint dominance plus uncontrolled tail is.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch has reduced the proof pressure to a finite endpoint sign interval; another abstract OS restatement would loop, while a controlled endpoint dominance experiment directly tests the post-H,K R/kappa_4 gate.
- Situation seed: SU(2) heat-kernel plaquette-sheet endpoint box for the known three-hairpin reflected Wilson block, with one reflection-plane endpoint shared by the 12 footprint and two comparable 13,23 endpoint footprints.
- Varied variable: endpoint overlap ratio r=G_{12,v}/(G_{13,v}+G_{23,v}) inside a single isolated endpoint box.
- Held-fixed controls: Same Wilson hairpin observables, same null vector, and the previously computed H,K data are held fixed., Heat-kernel regulator, singlet color projection, and no-boundary-counterterm same-theory condition are held fixed., Wick-square Gram positivity and straight f f null-incidence cancellation are held fixed., Tail budget tau_v is set to zero for the isolated box and restored only after the local test.
- Expected observation: The local endpoint contribution changes sign exactly when D_v=2G12_v-4G13_v-4G23_v crosses zero; negative compact-group kappa_4 becomes dangerous only in the r-dominant regime.
- Transfer certificate needed: A proof that the varied endpoint source is realized by the same regulated Wilson plaquette sheet, plus a cutoff-uniform source-derivative bound allowing the local interval to enter I_tot.

## Next Experiment

Build the actual endpoint table: enumerate endpoint boxes for the three hairpins, compute G12_v,G13_v,G23_v from singlet root-quartic polarization, evaluate seven heat-kernel source values for beta_v or prove the root-quartic bound, add tau_v, and report the interval sign of I_tot.

# Endpoint-box R interval certificate after H,K

## Candidate Lemma

If flowed boundary-OPE sector intervals for the plus endpoint box are valid, then R++ has an explicit lower bound. Positivity of the finite post-H,K Schur-Feshbach block follows only if this bound beats leakage L+. Failure demotes this repair, not Yang-Mills.

## Definitions

- source object: flowed centered Wilson hairpins Wtilde_+^{t,eps} in SU(N) Yang-Mills, encoded by H,K sheet currents and endpoint currents.
- target object: finite post-H,K endpoint-box Schur-Feshbach inequality for the plus channel, not the continuum mass gap.
- controlled interface: boundary-OPE cumulant map sending same-theory flowed Wilson covariance to R_{++}^{ren}/kappa_4 in the finite matrix block.
- same-theory condition: one bare action, one continuum limiting Schwinger family, common gradient-flow renormalization and reflection-positive cutoff removal.
- carrier: Ward-subtracted sheet-current kernels K_s for sectors 3g, 4g, counterterm, and endpoint-local remainder.

## Assumptions

- Model: four-dimensional SU(N) Yang-Mills with Wilson or continuum cutoff and gradient flow t>0 before removing the cutoff.
- Regime: endpoint-box hairpins are small compared with the separation scale, and eps point-splitting resolves cusps.
- Uniformity: sector kernel intervals are cutoff-stable and use the same H,K geometry and color normalization as L+.
- Naturalness: no tuning of endpoint geometry after seeing the sign of Xi++; only the flow ratio is varied in the test.
- Non-claim: success changes the finite endpoint-box positivity gate only; OS/Wightman construction and Hamiltonian mass gap remain untouched.

## Equations

- flowed endpoint cumulant split: `R_{++}^{ren}(t,\epsilon)=\kappa_2(\widetilde W_+^{t,\epsilon},\widetilde W_+^{t,\epsilon})=2(N^2-1)G_{++}^{t,\epsilon}+N(N^2-1)g_t^2\Xi_{++}^{t,\epsilon}+O(g_t^4)`. Valid when: Valid when the flowed boundary-OPE expansion is uniform on the endpoint box after centering and cusp subtraction.
- sector interval enclosure: `\Xi_{++}^{t,\epsilon}\in I_{3g}+I_{4g}+I_{ct}+I_{end},\quad I_s=\sum_{C\in P}\Box\!\int_C J_+^{\otimes4}K_s^{t,\epsilon}`. Valid when: Valid when Ward-subtracted sector kernels are integrable on each interval cell and use the same H,K sheet currents.
- endpoint-box promotion inequality: `Q_+^{box}\ge Q_+^{0}-L_+ +\kappa_4^{-1}(2(N^2-1)\underline G_{++}+N(N^2-1)g_t^2\sum_s\underline I_s-E_4)>0`. Valid when: Valid when finite H,K data, leakage L_+, and kappa_4 normalization come from the same Schur-Feshbach block.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: flowed centered Wilson hairpins Wtilde_+^{t,eps} in SU(N) Yang-Mills, encoded by H,K sheet currents and endpoint currents.; target object: finite post-H,K endpoint-box Schur-Feshbach inequality for the plus channel, not the continuum mass gap.; Model: four-dimensional SU(N) Yang-Mills with Wilson or continuum cutoff and gradient flow t>0 before removing the cutoff..
- Conceptual pressure attacked: exact finite leakage L+ is known, but same-theory Wilson positivity cannot advance without a certified sign/size for R++.
- Replace fragmented raw Wilson contours by sheet and endpoint currents; this makes Ward subtraction, cusp cancellation, and interval integration primitive operations.
- Expand the centered flowed cumulant: the cross-pair term gives positive color 2(N^2-1), while Xi++ decomposes into 3g, 4g, counterterm, and endpoint sectors.
- Apply cellwise heat-kernel derivative bounds to each sector; combine lower endpoints and compare R++/kappa_4 against L+ in the Schur-Feshbach inequality.

Blocking gap: No certified numerical or analytic enclosure of I_3g,I_4g,I_ct,I_end is yet produced, and uniform t,eps plateau control is still missing.

## Falsifiers

- falsifier: the certified lower interval gives R++/kappa_4 <= L_+-Q_+^0 in every same-theory regulator window.
- falsifier: cusp or perimeter subtraction leaves an uncanceled endpoint divergence in a sector kernel.
- falsifier: Xi++ changes sign or grows without a plateau as t/d^2 and eps/sqrt(t) are refined.
- falsifier: interval widths dominate the positive pair baseline, so no valid endpoint-box decision is possible.

## Learning

The sharp value signal is local and route-changing: R++ becomes a valid interval inequality with color factors and Ward cancellation, not a symbolic lambda. The hard gate changed is finite endpoint-box positivity after H,K; Clay existence, OS/Wightman axioms, and mass gap stay untouched.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch would loop if it only restated R++. The hard information is whether the connected four-curvature polarization can defeat finite leakage in a same-theory regulator window.
- Situation seed: SU(N) Wilson lattice with gradient-flowed thin plus-hairpin endpoint boxes matching the extracted H,K currents; measure the centered covariance and sector-subtracted cumulant.
- Varied variable: rho=t/d^2, the flow-time to endpoint-separation ratio.
- Held-fixed controls: same Wilson action and reflection-positive cutoff sequence, fixed H,K sheet and endpoint geometry, fixed color group SU(N) and representation, fixed cusp/perimeter subtraction prescription, fixed Schur-Feshbach leakage L+ and kappa_4 normalization
- Expected observation: A stable interval plateau for Delta(rho)=R++^{ren}/kappa_4-L++Q_+^0. Positive plateau promotes; negative or absent plateau demotes the endpoint-box repair.
- Transfer certificate needed: Uniform flowed-continuum interval bounds plus a same-theory identification of the measured Wilson covariance with the finite R++ entry used in the H,K Schur-Feshbach block.

## Next Experiment

Build the sector cell list for the plus endpoint box, enclose heat-kernel derivative factors and color contractions, then compute the first certified lower interval for Delta(rho).

# Post-H,K endpoint-box R/kappa4 interval certificate

## Candidate Lemma

For a fixed finite reflected-Wilson endpoint basis with already known H,K collar/hairpin blocks, a valid heat-kernel shell envelope for the connected four-curvature cumulant gives a finite Schur-corrected endpoint positivity certificate: if Delta_sigma>0 then R_sigma-S_HK is positive on the endpoint box; if Delta_sigma<=0 the chosen Wilson collar/hairpin route has a concrete falsifier at this truncation.

## Definitions

- source object: heat-kernel regulated SU(N) Yang-Mills Wilson endpoint-box data consisting of finite endpoint observables W_i^sigma, curvature-flux sheets Sigma_i, connected Wilson cumulants, and the already computed H,K collar/hairpin blocks.
- target object: the finite endpoint quadratic form T_sigma=R_sigma-S_HK on P_endpoint after Schur-Feshbach hairpin elimination; its target property is finite positivity, not a Hamiltonian mass gap.
- controlled interface: the sheet-kernel hypergraph encoding sheets, weights, heat-kernel transporters, color tensors, dyadic locality shells, connected-cumulant labels, OPE remainders, and S_HK=B^*E^{-1}B.
- same-theory condition: C_sigma, kappa4_sigma, OPE error, H,K, and S_HK are computed with the same regulator, coupling normalization, Wilson basis, reflection support, and vacuum state.
- Phi_i^sigma is the transported smeared curvature flux through endpoint sheet Sigma_i.
- C_{ij,sigma} is the two-flux covariance after vacuum/perimeter cancellation.
- Kappa_{ij,sigma}^{(4)} is the endpoint-compressed connected four-curvature cumulant, including color transport and sheet weights.
- M_{4,sigma}^- is any certified upper bound on the negative spectral size of Kappa_sigma^{(4)}.
- m_{G,sigma} is the least eigenvalue of the Gaussian Schur-product block alpha_N g_sigma^4(C_sigma o C_sigma) on the finite endpoint space.
- s_{HK,sigma} is the operator norm or sharper quadratic-form bound for the known Schur hairpin subtraction S_HK.

## Assumptions

- Model/regime: finite SU(N) reflected Wilson endpoint basis at cutoff a with heat-kernel smearing sigma>=c a, or its finite continuum-regularized analogue.
- Uniformity: the shell bounds b_{ell,sigma} and OPE error e_{OPE,sigma} are uniform over the endpoint index set and do not use endpoint-dependent advice.
- Schur regime: QH_QQ is strictly positive on the eliminated hairpin space, so S_HK=B^*(QH_QQ)^{-1}B is well-defined in the same finite theory.
- OPE regime: the boundary OPE for the selected endpoint sheets is valid at the chosen sigma and endpoint-box separation scale, with a certified operator-norm remainder.
- Color normalization: generators satisfy tr(T^aT^b)=delta^{ab}/2 and Wilson traces are normalized by 1/N.
- Same-theory condition: no cumulant, H,K block, or Schur subtraction is imported from a different regulator, coupling, lattice action, gauge fixing, or vacuum.
- Naturalness/cutoff: the finite endpoint box is chosen before taking any continuum limit; this lemma claims only a finite certificate or falsifier.

## Equations

- transported_smeared_flux: `\Phi_i^a(\sigma)=\int_{\Sigma_i} w_i(x)\,K_\sigma(x,z)\,\operatorname{Ad}_{U_{x\to x_0}}F_{\mu\nu}^a(z)\,n_i^{\mu\nu}(x)\,dz\,dS_x`. Valid when: Valid when the heat-kernel regulator smooths curvature fields above the lattice cutoff and the transporter paths stay inside the endpoint collar.
- connected_R_decomposition: `R_{ij,\sigma}=\alpha_N g_\sigma^4\,(C_\sigma\circ C_\sigma)_{ij}+\frac{g_\sigma^4}{16N^2}\,\Kappa^{(4)}_{ij,\sigma}+E^{\mathrm{OPE}}_{ij,\sigma},\qquad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after vacuum and perimeter subtractions, with normalized Wilson traces and identical heat-kernel smearing on both endpoint observables.
- two_flux_covariance: `C_{ij,\sigma}=\sum_a\langle \Phi_i^a(\sigma)\Phi_j^a(\sigma)\rangle_c`. Valid when: Valid for reflected endpoint sheets whose transported fluxes are gauge-invariant after trace closure and are evaluated in the same vacuum state.
- connected_four_curvature_kernel: `\Kappa^{(4)}_{ij,\sigma}=\sum_{a,b,c,d}\int_{\Sigma_i^2\times\Sigma_j^2}W_{ij}^{abcd}(x_1,x_2;y_1,y_2)\,\langle F^a_\sigma(x_1)F^b_\sigma(x_2)F^c_\sigma(y_1)F^d_\sigma(y_2)\rangle_c`. Valid when: Requires the same-theory boundary OPE expansion with all disconnected two-flux contractions removed before forming the endpoint compression.
- shell_row_sum_bound: `M_{4,\sigma}^-\le \|\Kappa^{(4)}_\sigma\|_{op}\le \max_i\sum_j |\Kappa^{(4)}_{ij,\sigma}|\le \sum_{\ell=0}^{L} n_\ell b_{\ell,\sigma}+\tau_{L,\sigma}`. Valid when: Valid when dyadic shell envelopes b_{ell,sigma} dominate every sheet-pair contribution and tau_{L,sigma} bounds the remaining tail uniformly.
- schur_corrected_margin: `\Delta_\sigma=m_{G,\sigma}-\frac{g_\sigma^4}{16N^2}M_{4,\sigma}^- - e_{\mathrm{OPE},\sigma}-s_{HK,\sigma}`. Valid when: Applies after the finite H,K Schur-Feshbach subtraction is computed in the same endpoint basis and the OPE error is operator-norm bounded.
- endpoint_certificate: `\Delta_\sigma>0\quad\Longrightarrow\quad x^*(R_\sigma-S_{HK})x\ge \Delta_\sigma\|x\|^2\quad\text{for all }x\in P_{endpoint}`. Valid when: Valid in the finite endpoint space when the Gaussian block is positive by the Schur product theorem and all negative terms are bounded above.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Observable Density In The Excitation Sector; source object: heat-kernel regulated SU(N) Yang-Mills Wilson endpoint-box data consisting of finite endpoint observables W_i^sigma, curvature-flux sheets Sigma_i, connected Wilson cumulants, and the already computed H,K collar/hairpin blocks.; target object: the finite endpoint quadratic form T_sigma=R_sigma-S_HK on P_endpoint after Schur-Feshbach hairpin elimination; its target property is finite positivity, not a Hamiltonian mass gap.; Model/regime: finite SU(N) reflected Wilson endpoint basis at cutoff a with heat-kernel smearing sigma>=c a, or its finite continuum-regularized analogue..
- Conceptual pressure attacked: finite Wilson cumulants, Schur-Feshbach subtraction, and endpoint positivity must be evaluated in one theory, but scalar R is too weak to remember color/locality/cumulant cancellation and OS-density is too strong for this local gate.
- Start from the same-theory connected endpoint Wilson expansion after vacuum and perimeter cancellation; isolate crossed two-curvature contractions and the connected four-curvature cumulant.
- Use the SU(N) trace normalization to obtain the Gaussian block alpha_N g_sigma^4(C_sigma o C_sigma), with alpha_N=(N^2-1)/(8N^2).
- Apply the Schur product theorem to C_sigma o C_sigma, giving a PSD Gaussian contribution and finite eigenvalue lower bound m_{G,sigma}.
- Represent Kappa^{(4)} by the sheet-kernel hypergraph; group its contractions into dyadic shells and bound its negative spectral contribution by the absolute row sum sum_l n_l b_{l,sigma}+tau_{L,sigma}.
- Subtract the already known Schur hairpin energy S_HK=B^*(QH_QQ)^{-1}B and the OPE operator-norm error.
- Conclude that every unit endpoint vector has quadratic form at least Delta_sigma; hence Delta_sigma>0 proves finite endpoint positivity, while Delta_sigma<=0 is a route-deciding stress case.

Blocking gap: The missing proof object is the first rigorous same-regulator shell envelope b_{ell,sigma} for the connected four-curvature cumulant, including color transport and OPE tail control.

## Falsifiers

- falsifier: a certified negative kappa4 shell gives M_{4,sigma}^- large enough that Delta_sigma<=0 after Schur subtraction.
- The Gaussian block C_sigma o C_sigma is singular on the endpoint quotient and the kappa4/OPE/Schur terms remove all positive margin.
- The heat-kernel OPE remainder is not uniformly bounded for the chosen sigma/a window, so the interval certificate is not valid.
- The computed H,K blocks use a different Wilson basis, cutoff, or coupling normalization from the cumulant data, violating the same-theory condition.
- The sheet-kernel quotient merges contractions with different color transport or orientation signs, producing a representation-limited false bound.
- Endpoint-box locality fails: the tail tau_{L,sigma} does not decrease under shell refinement.

## Learning

Cycle 265 attacks the conceptual pressure that the post-H,K route needs a mediator from actual connected Wilson cumulants to Schur-corrected endpoint positivity. Declarative tension: Wilson/OPE data, finite Schur-Feshbach subtraction, and endpoint positivity must all hold in one theory, but scalar R was too weak and representation-limited, raw plaquette enumeration was fragmented, and OS-density was too strong and circular for this local gate. The proposed efficient carrier is the sheet-kernel hypergraph: it encodes sheets, weights, heat-kernel transporters, color tensors, shell labels, multiplicities, OPE errors, and Schur data; preserves gauge invariance, reflection support, Gaussian/kappa4 separation, endpoint compression, and same-theory normalization; supports cumulant contraction, quotienting, shelling, row-sum/operator bounds, interval arithmetic, and Schur subtraction; quotients only by Wilson-invariant sheet symmetries and trace identities; keeps a finite endpoint-box locality budget; and transfers only to the finite certificate Delta_sigma. The hard gate is Delta_sigma. Success changes the finite Route A endpoint-box positivity state and can justify paper-level handoff of a worked Wilson calculation; failure is a valid falsifier for this collar/hairpin geometry. The larger Clay gates--OS/Wightman axioms, nontrivial continuum limit, and positive Hamiltonian mass gap in the same theory--remain untouched. The conceptual value signal is sharp because it turns the unknown boundary-OPE polarization into a computable sign/size interval without pretending to prove the full Clay theorem.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch already has the Schur-Feshbach theorem and the symbolic R decomposition; the hard gate is now numerical or interval sign control of the actual connected boundary-OPE polarization term, not another abstract obstruction restatement.
- Situation seed: Fix SU(N) heat-kernel regulated Wilson theory on a four-dimensional hypercubic torus at cutoff a. Use the first known collar/hairpin H,K endpoint basis, two reflected endpoint boxes, normalized Wilson traces, and the sheet-kernel hypergraph for Kappa^{(4)}.
- Varied variable: eta=sigma/a, the heat-kernel smearing width in cutoff units, varied over a finite window eta in [2,6].
- Held-fixed controls: Same endpoint Wilson basis and same H,K Schur subtraction S_HK for every eta., Same lattice action, bare/renormalized coupling convention, SU(N) trace normalization, and vacuum state., Same reflected endpoint geometry, transporter convention, dyadic shell partition, and OPE truncation order., No change of theory, gauge fixing, or observable algebra while varying eta.
- Expected observation: If the route is viable, m_G remains positive or mildly decreasing while the certified kappa4 row-sum plus OPE tail decreases enough to produce a nonempty eta-window with Delta_sigma>0. If every eta gives Delta_sigma<=0, the endpoint-box Wilson route is demoted for this H,K geometry.
- Transfer certificate needed: A same-theory interval certificate listing C_sigma, shell envelopes b_{ell,sigma}, tail tau_{L,sigma}, e_{OPE,sigma}, and S_HK with regulator-normalized color factors, plus a proof that the quotient hypergraph preserves all Wilson cumulant contractions.

## Next Experiment

Instantiate the first endpoint geometry: list the sheet representatives, compute the SU(N) color tensors for the crossed Gaussian block and the first connected kappa4 shell, audit S_HK normalization, then evaluate the interval margin Delta_sigma for eta=sigma/a in {2,3,4,5,6}.
