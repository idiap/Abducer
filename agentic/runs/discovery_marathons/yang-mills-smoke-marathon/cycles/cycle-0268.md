# cycle-0268

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Post-H,K endpoint-box cumulant interval certificate

## Candidate Lemma

For the fixed three-hairpin post-H,K block, the remaining connected endpoint boundary-OPE term is controlled by same-theory heat-kernel endpoint source derivatives. The negative Haar-Jacobian fourth cumulant is dangerous only after the null-channel endpoint incidence D_v is positive; a clipped interval gives a valid finite promotion or falsifier test.

## Definitions

- source object: heat-kernel plaquette-sheet SU(N) endpoint boxes v carrying regulated Wilson boundary flux sources B_{i,v} for the already fixed three-hairpin collar block.
- target object: the scalar post-H,K null-channel endpoint interval I_gate whose sign decides this finite reflected-Wilson OS transfer gate, not the full Yang-Mills mass gap.
- controlled interface: fourth source derivatives of the same regulated Wilson endpoint partition functions, contracted with the Feshbach null incidence weights and exported as one interval.
- same-theory condition: the endpoint source Z_v(s) is obtained from the same Wilson loops, heat-kernel action, color trace normalization, and cutoff sequence as the collar OS matrix; no boundary counterterm or algebra enlargement is introduced.
- conceptual pressure: make endpoint collapse sign-certifiable while preserving the same Wilson theory.
- declarative tension: finite collar OS positivity, unchanged gauge-invariant Wilson observables, and singular connected endpoint OPE terms must jointly hold; raw R cannot remember incidence signs.
- carrier critique: symbolic R is representation-limited, while a raw kappa_4 spectrum is too strong because it ignores the null incidence contraction.
- efficient representation: encode endpoint boxes, B_{i,v}, source stencils, beta intervals, D_v intervals, color factors, and tails; preserve Wilson normalization, null cancellations, cutoff uniformity, and same-theory observables; primitive operations are source differentiation, interval arithmetic, polarization, clipping, and tail addition; equivalence means equal regulated source derivatives; locality cost is charged to T_tail; transfer exports only I_gate.

## Assumptions

- Model/regime: four-dimensional Euclidean SU(N) Yang-Mills is kept at finite heat-kernel plaquette cutoff a and finite collar thickness before any continuum claim.
- Uniformity: endpoint boxes have heat-kernel times t_v with source-derivative remainders bounded uniformly over the selected finite Wilson block as a tends to zero along the chosen cutoff sequence.
- Same-theory condition: the Wilson loops, plaquette sheets, reflection map, and color trace normalization are identical to those used to build H and K.
- Cancellation assumption: connected logs remove Wick-square Gram pieces, and the straight nonabelian f f contact cancels under the already verified null incidence identity for this block.
- Locality assumption: nonendpoint overlap and corner leakage are either absent by separation or included in a signed tail interval T_tail with cutoff-uniform enclosure.
- Naturalness boundary: the lemma is a finite regulated endpoint certificate; it does not assert continuum existence, all-observable OS positivity, Wightman reconstruction, nontriviality, or a Hamiltonian mass gap.

## Equations

- endpoint-source-cumulant: `Z_v(\mathbf s)=\int_{G^{E_v}}\exp\{-S_{HK,v}(U)+\sum_i s_i X_{i,v}(U)\}\,d\mu_{HK}(U),\qquad \kappa_{ij,v}^{(4)c}=\partial_{s_i}^2\partial_{s_j}^2\log Z_v(\mathbf s)\big|_{\mathbf s=0}`. Valid when: Valid when the heat-kernel endpoint box isolates one endpoint after collar thickness is smaller than all nonendpoint separations and the Wilson sources are the locked gauge-invariant plaquette-sheet sources.
- quartic-color-polarization: `\mathcal C_4(Y)=\operatorname{tr}_{ad}(\operatorname{ad}_Y)^4=2N\operatorname{tr}_F(Y^4)+6(\operatorname{tr}_F(Y^2))^2,\qquad G_{ij,v}=\frac14\partial_s^2\partial_t^2\mathcal C_4(sB_{i,v}+tB_{j,v})\big|_{0}`. Valid when: Applies in SU(N) exponential coordinates near the endpoint identity with Hermitian generators normalized by tr_F(T^aT^b)=delta^{ab}/2 and with heat-kernel time small enough that the Haar-Jacobian expansion controls the fourth cumulant.
- haar-jacobian-fourth-cumulant: `\kappa_{ij,v}^{(4)c}=-\frac{t_v^4}{120}G_{ij,v}+E_{ij,v},\qquad |E_{ij,v}|\le \epsilon_v\|B_{i,v}\|^2\|B_{j,v}\|^2`. Valid when: Requires the endpoint box action to be heat-kernel dominated and the eighth source-derivative remainder to be bounded uniformly in the cutoff for the selected finite hairpin block.
- null-channel-endpoint-contraction: `R_{\partial}^{\zeta}=\gamma\sum_v\{2\kappa_{12,v}^{(4)c}-4\kappa_{13,v}^{(4)c}-4\kappa_{23,v}^{(4)c}\}+T_{\rm tail},\qquad \gamma=\frac{g_a^4}{4}(T_F/N)^2`. Valid when: Valid after the H,K block and null vector zeta are fixed, diagonal one-body Wilson factors are removed, Wick-square Gram terms are separated, and straight f f contacts cancel by null incidence.
- clipped-promotion-lower-bound: `\underline I_{\rm gate}=M_G-\gamma\sum_v\frac{t_v^4}{120}[\overline D_v]_+-\sum_v\gamma\overline\epsilon_v-\tau_{\rm tail},\qquad D_v=2G_{12,v}-4G_{13,v}-4G_{23,v}`. Valid when: Applies when D_v and remainder intervals enclose the same regulated endpoint derivatives and M_G denotes the positive Schur-Feshbach Gaussian margin of this finite block.
- finite-block-decision-rule: `\underline I_{\rm gate}\ge0\Rightarrow {\rm promote\ finite\ block},\qquad \overline I_{\rm gate}<0\Rightarrow {\rm finite\ same\mbox{-}theory\ falsifier}`. Valid when: Valid only for the finite post-H,K Wilson block under the locked regulator and does not assert continuum existence, full OS reconstruction, nontriviality, or a Hamiltonian mass gap.

## Attempted Derivation

- Attack conceptual pressure: endpoint collapse must be sign-certified without replacing the Wilson observable algebra or redoing the OS closed-cone ladder.
- Localize the post-H,K remainder to heat-kernel endpoint boxes after Wick-square Gram positivity and straight f f null-incidence cancellation.
- Represent each endpoint contribution by source derivatives of log Z_v; connected logarithms remove Gaussian Wick-square terms automatically.
- Use the exponential-coordinate Haar density log j(Y)=-tr_ad(ad_Y)^2/24-tr_ad(ad_Y)^4/2880+...; the fourth derivative of the quartic term gives -t_v^4 C_4(Y)/120 plus a controlled source remainder.
- Polarize C_4 between the Wilson endpoint source directions B_{i,v}; this exposes the color/geometric factors G_{ij,v} rather than hiding them in a symbolic R_{ij}.
- Contract with the null-channel pair weights 2,-4,-4 to form D_v. Because the leading compact-group kappa_4 is negative, only [D_v]_+ is demoting; D_v<0 is protective.
- Add the certified endpoint remainder and the locality tail T_tail. The hard gate becomes the sign of one scalar interval I_gate for this finite Wilson block.
- Balance test: success promotes only the finite post-H,K reflected-Wilson OS transfer gate; failure gives a finite same-theory falsifier; continuum construction, full OS/Wightman reconstruction, nontriviality, and mass gap remain untouched.

Blocking gap: The actual endpoint incidence table B_{i,v}, cutoff-uniform eighth-derivative bounds, and signed tail interval T_tail have not yet been computed for the regulated hairpin geometry.

## Falsifiers

- A same-theory endpoint stencil produces an interval with overline I_gate<0; this is a finite reflected-Wilson OS falsifier for the post-H,K block.
- The endpoint incidence table violates the straight f f null-cancellation identity, invalidating the claimed reduction to connected kappa_4 endpoints.
- The source chart or Haar-Jacobian expansion requires a boundary counterterm not present in the locked Wilson theory.
- The eighth-derivative or locality-tail bound is not cutoff-uniform, so the interval carrier is not valid for the intended cutoff passage.
- Endpoint boxes overlap in a way not chargeable to T_tail, making the local endpoint decomposition representation-limited rather than same-theory.
- The global collar OS matrix passes while the computed endpoint source carrier changes the observable algebra; that would demote the branch as proving positivity for the wrong theory.

## Learning

Cycle 268 refits the last R/kappa_4 obstruction into a finite endpoint source interval. The sharp value signal is explanatory and route-changing at local scope: negative compact-group kappa_4 is not itself the falsifier; only positive null-channel endpoint dominance plus uncontrolled tail can demote the block. Compared with a global Schur-preimage matrix test, this carrier is local and computable after H,K; compared with formal OPE language, it exposes primitive operations and validity checks. The hard gate changed is the finite post-H,K reflected-Wilson OS transfer gate. The Clay gates of continuum existence, full OS/Wightman reconstruction, nontriviality, and positive Hamiltonian mass gap are untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and endpoint-data design guide.`
- Rationale: The branch has already fixed H,K and reduced the obstruction to post-H,K R/kappa_4 endpoint signs; another abstract OS restatement would loop, while an endpoint dominance dial tests exactly the remaining carrier.
- Situation seed: A heat-kernel SU(N) plaquette-sheet three-hairpin block with the same null vector and Wilson source normalization, but with endpoint footprints arranged so the 12 overlap boxes can be made increasingly dominant over the 13 and 23 boxes.
- Varied variable: alpha, the ratio of total positive endpoint dominance sum_v [D_v]_+ on 12-type boxes to the protective and tail-controlled endpoint mass.
- Held-fixed controls: The same heat-kernel regulator, plaquette-sheet Wilson contractions, color trace convention, and cutoff sequence used for H and K., The same finite three-hairpin geometry away from endpoint footprint redistribution, including the Feshbach null vector and Schur-Feshbach Gaussian margin M_G., No boundary counterterm, gauge fixing change, or Wilson algebra enlargement is allowed.
- Expected observation: As alpha increases, the certified interval for I_gate should cross from promoted to undecided and then to a finite falsifier if endpoint dominance can overcome M_G plus the tail allowance.
- Transfer certificate needed: A regulated endpoint incidence table B_{i,v}, seven-point source intervals for kappa_4, and a cutoff-uniform T_tail bound proving that the thought-experiment endpoint redistribution is realizable by the locked Wilson plaquette sheets.

## Next Experiment

Build the endpoint incidence table B_{i,v} for the heat-kernel plaquette-sheet three-hairpin geometry, compute G_{ij,v} via quartic SU(N) polarization, enclose kappa_4 with the seven-point stencil and M8 bound, then report the interval sign of I_gate.

# Endpoint-box R++ interval enclosure by Ward-subtracted flowed sheet currents

## Candidate Lemma

Finite endpoint-box transfer lemma: for fixed extracted H,K hairpin sheets, a certified lower interval for the same-theory flowed Wilson covariance R_{++}^{ren} promotes the post-H,K endpoint-box gate exactly when it beats the Schur-Feshbach leakage L_+; otherwise this R-repair is demoted without claiming any Clay mass gap result.

## Definitions

- source object: the same-theory SU(N) Euclidean Yang-Mills Schwinger family regulated by lattice spacing a, gradient flow time t>0, endpoint point-splitting epsilon, and renormalized thin Wilson hairpin sheets Sigma_H,Sigma_K.
- target object: the finite post-H,K endpoint-box Schur-Feshbach scalar q_+^{box}=R_{++}^{ren}-L_+ controlling one finite positivity gate, not the continuum Hamiltonian gap.
- controlled interface: the map from oriented flowed sheet currents J_H,J_K to the centered Wilson cumulant kappa_2(W_H^{ren,c},W_K^{ren,c}) after perimeter, cusp, and disconnected-product subtraction.
- same-theory condition: the regulator, Wilson action or continuum limit, gradient-flow counterterms, H,K observables, and reflection-positive Schwinger family are identical on both sides of the transfer.

## Assumptions

- Model/regime: four-dimensional pure SU(N) Yang-Mills in a fixed finite endpoint box B_e, with a<<epsilon<=rho and t comparable to rho^2 but positive.
- Uniformity: constants in the flowed Ward bounds and OPE remainder are independent of a along the chosen continuum subsequence.
- Cutoff/naturalness: the H,K sheets and endpoint currents are fixed finite objects; no advice, auxiliary scalar, external mass, or changed gauge theory is introduced.
- Renormalization: one-hairpin perimeter/cusp counterterms are subtracted before taking the connected cross-cumulant.
- Same-theory transfer: R_{++}^{ren} is evaluated in the same Schwinger family that would enter OS reconstruction; the lemma changes only the finite endpoint-box positivity gate.

## Equations

- flowed_endpoint_covariance_decomposition: `R_{++}^{ren}(t,\epsilon,\rho)=g_t^4\left[2(N^2-1)G_{++}(t,\epsilon,\rho)+g_t^2N(N^2-1)\Xi_{++}^{ren}(t,\epsilon,\rho)+E_6(t,\epsilon,\rho)\right]`. Valid when: Valid when the two centered renormalized hairpin Wilson observables are expanded in the endpoint box at positive flow time with fixed H,K sheets and diagonal current normalization.
- connected_polarization_sectors: `\Xi_{++}^{ren}=I_{3g}+I_{4g}+I_{ct}+I_{end}`. Valid when: Valid when the flowed four-curvature cumulant is Ward-subtracted and decomposed into three-gluon, four-gluon, counterterm, and endpoint-local sectors in the same regulator.
- promotion_inequality: `g_t^4\left[2(N^2-1)\underline G_{++}+g_t^2N(N^2-1)\underline\Xi_{++}-\overline{|E_6|}\right]>L_+ + \eta`. Valid when: Applies after interval quadrature supplies rigorous lower and upper enclosures for the pair baseline, connected polarization, and sixth-order OPE remainder.
- demotion_inequality: `g_t^4\left[2(N^2-1)\overline G_{++}+g_t^2N(N^2-1)\overline\Xi_{++}+\overline{|E_6|}\right]\le L_+`. Valid when: Valid when the same interval enclosure is sharp enough that even the optimistic endpoint-box covariance cannot overcome the Schur-Feshbach leakage.

## Attempted Derivation

- Conceptual pressure attacked: finite Schur-Feshbach positivity needs a same-theory endpoint mediator, while positive pair covariance and gradient-flow renormalization alone do not control the connected four-curvature polarization.
- Declarative tension: OS-compatible same-theory Wilson observables, flowed renormalization, and the finite tangent-cone leakage formula must all be valid, but the missing mediator is a sign/size certificate for Xi_{++}^{ren}.
- Carrier critique: raw Wilson contours are fragmented and representation-limited; sheet currents with endpoint currents are sharper because Ward subtraction, color contraction, and interval integration become primitive operations.
- Abstraction comparison: a global non-Gaussian OS witness is too weakly targeted for this local obstruction, while a finite Ward-subtracted interval-kernel route directly tests the hard gate of endpoint-box positivity after H,K.
- Replace the two H,K Wilson hairpins by renormalized flowed sheet-current observables in B_e and center them before cumulant formation.
- Expand the connected covariance through the two-curvature pair term and the connected four-curvature term; disconnected products and one-hairpin perimeter/cusp pieces cancel by construction.
- Compute the pair color contraction in the normalized plus channel, giving 2(N^2-1)G_{++} with G_{++}>=0 for transverse positive flowed covariance.
- Decompose the connected four-curvature polarization into I_{3g}, I_{4g}, I_{ct}, and I_{end}; apply Ward subtraction before heat-kernel majorization.
- Partition B_e into cells and assign Taylor/interval enclosures to each sector kernel, yielding [underline Xi_{++},overline Xi_{++}] plus an OPE remainder bound overline{|E_6|}.
- Compare the certified lower bound for R_{++}^{ren} with the already finite Schur-Feshbach leakage L_+; success promotes only the finite endpoint-box gate, failure quarantines the R-repair.

Blocking gap: No certified numerical or symbolic interval for Xi_{++}^{ren} has yet been produced; the uniform Ward-subtracted C_W and sixth-order remainder constants are proof obligations.

## Falsifiers

- Certified upper bound R_{++}^{ren}<=L_+ in the admissible flow window is a route-level falsifier for the endpoint-box repair.
- Ward subtraction leaves a cusp or endpoint divergence depending on epsilon, so the proposed same-theory covariance is not finite.
- The interval enclosure for Xi_{++}^{ren} is too wide to decide the sign or size after reasonable cell refinement.
- The positive pair baseline G_{++} vanishes for the actual extracted H,K endpoint geometry.
- The apparent positivity appears only at finite cutoff a and disappears along every same-theory continuum subsequence.
- Changing the spanning sheet while keeping the Wilson boundary changes R_{++}^{ren}, showing the carrier was not gauge-invariantly valid.

## Learning

The cycle is non-looping: it sharpens R_{++} into a concrete same-theory flowed Wilson cumulant with pair color 2(N^2-1), connected color N(N^2-1), named sector kernels, Ward cancellation, and promotion/demotion inequalities. Hard gate changed: finite endpoint-box positivity after H,K; success promotes this local gate, failure quarantines the R repair. Untouched gates: continuum construction, OS/Wightman axioms, nontriviality, and positive Hamiltonian mass gap. Conceptual value signal: a symbolic endpoint term becomes a valid falsifiable interval problem with an explicit regulator, carrier, invariants, equivalence policy, and falsifier set.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and quadrature design constraint.`
- Rationale: The branch has already reduced the local obstruction to R_{++}^{ren}; another abstract restatement would loop, while varying the regulator window tests whether a valid endpoint-box certificate can exist.
- Situation seed: Flowed lattice SU(N) Wilson action with fixed extracted H,K plus-channel endpoint sheets inside one box B_e; compute the centered renormalized covariance of the two thin hairpin Wilson observables using sheet-current cell intervals.
- Varied variable: The single varied parameter is tau=t/rho^2, the gradient-flow time divided by endpoint-box size squared.
- Held-fixed controls: Same bare gauge action and same continuum subsequence for every tau., Same H,K sheet currents, endpoint orientation, plus-channel normalization, and Schur-Feshbach leakage L_+., Same perimeter/cusp subtraction scheme and endpoint point-splitting ratio epsilon/rho., Same cell partition refinement policy and Ward-subtracted sector decomposition.
- Expected observation: A promotion-quality window would show a stable lower interval for R_{++}^{ren}-L_+ that remains positive over a tau plateau; demotion would show sign drift, loss of Ward cancellation, or an upper interval below L_+.
- Transfer certificate needed: A uniform flow-time/cutoff theorem showing that the flowed cumulant intervals converge to the same OS Schwinger family and that the finite endpoint-box inequality is independent of regulator artifacts.

## Next Experiment

Compute G_{++} and a first coarse [underline Xi_{++},overline Xi_{++}] for the actual H,K sheet cells using flowed heat-kernel Ward-subtracted sector bounds; vary only tau=t/rho^2 and test R_{++}^{ren}-L_+ for a valid plateau.

# Post-HK endpoint-box kappa4 interval certificate

## Candidate Lemma

For a finite reflected Wilson collar/hairpin endpoint basis with known H,K Schur data, the heat-kernel regulated endpoint polarization has a same-theory interval certificate Delta_sigma. If Delta_sigma>0, the finite Route A endpoint-box positivity gate is valid after Schur subtraction; if Delta_sigma<=0 or is regulator-nonuniform, this is a falsifier for this Wilson geometry. No OS/Wightman, continuum, or Hamiltonian mass-gap gate is changed.

## Definitions

- source object: heat-kernel regulated connected SU(N) Wilson endpoint-box cumulants for the fixed collar/hairpin sheet set after H,K extraction.
- target object: the finite endpoint-box quadratic form P(R_sigma-S_HK)P on the reflected Wilson endpoint coefficient space, with a certified lower interval.
- controlled interface: sheet-kernel hypergraph carrying endpoint sheets, transported curvature fluxes, color tensors, shell labels, OPE errors, and Schur data.
- same-theory condition: the Wilson basis, heat-kernel regulator, coupling, vacuum subtraction, counterterms, and Schur H,K data are all taken from one cutoff Yang-Mills measure before any continuum inference.
- Endpoint sheet u is an oriented plaquette-sheet or smoothed collar patch with a fixed basepoint and reflection support.
- kappa4_sigma is the compressed connected four-curvature cumulant left after vacuum/perimeter and Gaussian crossed-contraction cancellation.

## Assumptions

- Model: finite cutoff pure SU(N) Yang-Mills on a reflected four-torus or box with reflection-positive Wilson measure.
- Regime: cutoff a, heat-kernel width sigma, and endpoint diameter L satisfy a << sigma << L, with a finite endpoint sheet set fixed before estimates.
- Uniformity: the same regulator sigma is used for C_sigma, kappa4_sigma, E_OPE,sigma, and the H,K Schur subtraction; no mixed-regulator transfer is allowed.
- OPE assumption: the boundary Wilson expansion through fourth transported-curvature order has a certified matrix remainder norm e_OPE,sigma on this finite sheet set.
- Schur assumption: E=QHQ is positive on the hairpin complement, so S_HK=B^*E^{-1}B is a valid finite Schur-Feshbach subtraction.
- Naturalness boundary: the lemma is a finite Wilson calculation and does not assert continuum existence, OS reconstruction, or a positive Hamiltonian mass gap.

## Equations

- transported heat-kernel curvature: `F^a_{\mu\nu,\sigma}(x;b)=\int K_\sigma(x,y)\,\mathrm{Ad}_{U(b\leftarrow y)}^{aa'}F^{a'}_{\mu\nu}(y)\,dy`. Valid when: Valid when heat-kernel smearing lies between cutoff and endpoint-box diameter and transport paths are fixed by Wilson sheet geometry.
- endpoint flux covariance: `\Phi_u^a=\int_{\Sigma_u} dS^{\mu\nu}(x)F^a_{\mu\nu,\sigma}(x;b_u),\quad C_{uv,\sigma}=\frac{1}{N^2-1}\sum_a\langle \Phi_u^a\Phi_v^a\rangle_c`. Valid when: Valid when u and v belong to the finite reflected endpoint basis and vacuum subtraction removes one-point perimeter terms.
- same-regulator R decomposition: `R_{uv,\sigma}=\alpha_N g_R^4(C_\sigma\circ C_\sigma)_{uv}+\frac{g_R^4}{16N^2}\kappa^{(4)}_{uv,\sigma}+E^{\mathrm{OPE}}_{uv,\sigma},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid when the Wilson boundary OPE is truncated at fourth curvature order using the same heat-kernel regulator and sheet basis.
- connected four-curvature polarization: `\kappa^{(4)}_{uv,\sigma}=\int_{\Sigma_u^2\times\Sigma_v^2}\delta_{ab}\delta_{cd}\,\langle F^a_\sigma(x_1)F^b_\sigma(x_2)F^c_\sigma(y_1)F^d_\sigma(y_2)\rangle_c\,dS_{x_1}dS_{x_2}dS_{y_1}dS_{y_2}`. Valid when: Valid after all four curvatures are transported to the prescribed basepoints and only the connected cumulant is retained.
- shell row-sum negative-size bound: `\kappa^{(4)}_\sigma=\sum_{\ell=0}^{L_\sigma}\kappa^{(4)}_\sigma[\ell],\quad M^-_{4,\sigma}\le B_{4,\sigma}:=\max_u\sum_v\sum_\ell |\kappa^{(4)}_{uv,\sigma}[\ell]|`. Valid when: Valid when the shells partition the four-sheet integration domain and the endpoint compression is finite dimensional.
- post-HK endpoint margin: `\Delta_\sigma=\lambda_{\min}(\alpha_N g_R^4(C_\sigma\circ C_\sigma))-\frac{g_R^4}{16N^2}B_{4,\sigma}-e_{\mathrm{OPE},\sigma}-\|B^*E^{-1}B\|_{\mathrm{op}}`. Valid when: Valid when E equals QHQ on the same H,K hairpin complement and all matrices use identical endpoint coordinates.
- finite certificate implication: `\Delta_\sigma>0\quad\Longrightarrow\quad P(R_\sigma-S_{HK})P\ge \Delta_\sigma P`. Valid when: Valid for the finite reflected endpoint coefficient space after diagonal normalization and Schur-Feshbach subtraction are completed.

## Attempted Derivation

- Attack conceptual pressure: concrete Wilson/OPE data, kappa4 negativity, and Schur subtraction must meet in one finite same-theory object rather than in scalar R notation.
- Start with transported heat-kernel curvature fluxes Phi_u on the fixed endpoint sheets from the H,K collar/hairpin audit.
- Expand the normalized endpoint Wilson observables to fourth transported-curvature order and normal-order them against the same cutoff vacuum.
- Use vacuum and perimeter cancellation: one-box expectations and disconnected products are removed before forming R_sigma.
- Separate crossed two-curvature contractions from the connected four-curvature cumulant; the crossed part gives alpha_N g_R^4(C_sigma o C_sigma) and is PSD.
- Compress the connected four-curvature term into kappa4_sigma on endpoint labels, retaining the color tensor delta_ab delta_cd and geometric four-sheet integration.
- Partition the four-sheet integration domain into heat-kernel distance shells and bound the negative spectral part by a Gershgorin row-sum envelope B_4,sigma.
- Apply Weyl monotonicity and the finite Schur-Feshbach theorem to obtain Delta_sigma as a lower bound for P(R_sigma-S_HK)P.
- Hard gate: Delta_sigma decides the finite endpoint-box positivity state; success promotes a worked Wilson calculation, failure gives a valid falsifier for this Route A geometry.

Blocking gap: The first shell value of kappa4_sigma[0] and the OPE remainder e_OPE,sigma are not yet evaluated for the actual H,K endpoint sheet list; the formula is a proof-search certificate, not a completed positivity proof.

## Falsifiers

- A same-regulator computation gives g_R^4 B_4,sigma/(16N^2)+e_OPE,sigma+||S_HK||op >= lambda_min(alpha_N g_R^4(C_sigma o C_sigma)).
- The connected four-curvature first shell has a negative eigenvector aligned with the endpoint Gaussian minimum, making Delta_sigma nonpositive.
- Changing only the admissible sheet quotient changes the Delta_sigma interval, showing the carrier is not invariant.
- The heat-kernel window a << sigma << L has no stable interval because B_4,sigma or e_OPE,sigma diverges relative to the Gaussian margin.
- Vacuum/perimeter cancellation fails in the same Wilson normalization used for H,K, so the computed R is not the endpoint-box cumulant.
- E=QHQ has a near-zero hairpin mode, making the Schur subtraction dominate the endpoint polarization.

## Learning

Cycle 268 attacks the conceptual pressure that the post-H,K route needs a valid mediator from actual connected Wilson cumulants to Schur-corrected endpoint positivity. Declarative tension: Wilson/OPE coefficients, connected kappa4 negativity, and S_HK must be evaluated in one cutoff theory, but scalar R is too weak, full OS density is too strong and circular for this local gate, and raw plaquette enumeration is fragmented. The sheet-kernel hypergraph remains the best abstraction because it encodes sheets, weights, transporters, color tensors, shell labels, multiplicities, OPE errors, and Schur data; preserves gauge invariance, reflection support, Gaussian/kappa4 separation, endpoint compression, and same-theory normalization; supports cumulant contraction, quotienting, shell row/operator bounds, interval arithmetic, and Schur subtraction; quotients only by Wilson trace symmetries; and exposes falsifiers by margin failure or non-invariance. The hard gate is Delta_sigma. Its sign changes only the finite Route A endpoint-box proof state; OS/Wightman reconstruction, nontrivial continuum limit, and positive Hamiltonian mass gap remain untouched. The value signal is sharp and route-changing at finite scope because the unknown boundary-OPE polarization is now a computable interval certificate rather than a symbolic parameter.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: This branch is past abstract obstruction restatement; the decisive unknown is the sign and size of the connected boundary-OPE polarization after H,K Schur subtraction.
- Situation seed: Fix the first reflected SU(N) collar/hairpin endpoint-box sheet set from the H,K audit on a finite cutoff four-torus. Use heat-kernel smeared transported curvature and evaluate the plaquette-sheet cumulants defining kappa4_sigma shell by shell.
- Varied variable: rho=sigma/a, varied over a small regulator window such as rho in {2,3,4,6} while the endpoint geometry is fixed.
- Held-fixed controls: Same Wilson endpoint basis and reflection plane as the H,K calculation., Same cutoff action, coupling, trace normalization, and vacuum subtraction., Same Schur data E=QHQ and B=QKP, with no recomputation under a different regulator., Same shell quotient policy generated only by Wilson-invariant sheet symmetries.
- Expected observation: Either the first shell kappa4 negative envelope is dominated and Delta_sigma stays positive over a regulator window, or the first shell creates a stable nonpositive Delta_sigma falsifier.
- Transfer certificate needed: A same-regulator interval certificate for C_sigma, kappa4_sigma[ell], e_OPE,sigma, and S_HK, with quotient invariance and an explicit Delta_sigma sign.

## Next Experiment

Using the actual H,K endpoint sheets, compute the heat-kernel first-shell connected four-curvature cumulant kappa4_sigma[0], the Gaussian matrix C_sigma o C_sigma, and S_HK, then report the interval sign of Delta_sigma.
