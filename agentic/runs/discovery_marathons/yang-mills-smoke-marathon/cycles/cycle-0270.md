# cycle-0270

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Post-H,K endpoint-source interval for reflected Wilson hairpins

## Candidate Lemma

For the fixed three-hairpin post-H,K block, the endpoint part of the connected boundary-OPE polarization has a valid scalar interval certificate. Negative compact-group kappa4 can demote the finite OS transfer only through beta-weighted endpoint boxes with positive D_v=2G12_v-4G13_v-4G23_v, plus an uncontrolled tail. Success promotes only this finite reflected-Wilson gate; failure gives a finite same-theory falsifier and does not imply the Clay mass gap.

## Definitions

- source object: heat-kernel plaquette-sheet regulated SU(N) Wilson endpoint boxes v with same-theory source functions Z_v(s)=<exp(s X_v)> for the flux variable X_v induced by the locked three-hairpin collar block.
- target object: the finite post-H,K Schur-Feshbach null-channel scalar I_gate for this three-hairpin OS transfer block, not the continuum Yang-Mills theory and not the Hamiltonian mass gap.
- controlled interface: the endpoint carrier (beta_v,D_v,T_tail) mapping same-theory fourth source cumulants and endpoint incidence to an interval [I_low,I_high] for the R/kappa4 contribution entering I_gate.
- same-theory condition: endpoint boxes, source derivatives, Wilson normalization, color trace, and collar limit are those of the same regulated Wilson loops used to compute H and K, with no boundary counterterm or changed observable algebra.
- Gij_v is the normalized signed endpoint overlap intensity of hairpin pair ij inside endpoint box v after straight-segment contributions have been removed.
- D_v=2G12_v-4G13_v-4G23_v is the Feshbach null-channel incidence coefficient; [D_v]_+ is the only local multiplier of a negative endpoint kappa4 that can lower I_gate.
- M_G denotes the already computed positive Gaussian Schur-Feshbach margin for the finite block; C_NF=(g^4/4)(T_F/N)^2 times the endpoint color-normalization convention.

## Assumptions

- Model/regime: four-dimensional SU(N), N>=2, heat-kernel plaquette-sheet regulator at lattice spacing a with fixed finite hairpin geometry and endpoint boxes smaller than the collar scale but larger than the plaquette scale.
- Uniformity: the endpoint source derivatives of log Z_v have cutoff-uniform intervals and the nonlocal remainder is bounded by a same-theory tail T_tail.
- Same-theory condition: the endpoint carrier is extracted from the locked gauge-invariant Wilson algebra; no gauge fixing, boundary state, or endpoint renormalization is introduced after H,K are fixed.
- Cancellation assumption: disconnected Wick-square terms are separated as positive Gram terms, one-body Wilson factors vanish on the Feshbach null channel, and straight C_A f f contact incidence cancels in the chosen hairpin geometry.
- Naturalness: mixed endpoint boxes not resolved by the finite list are charged to T_tail rather than silently identified with a favorable local class.
- Hard gate changed: the finite post-H,K reflected-Wilson OS transfer gate is promoted if I_low>=0 and demoted by a finite falsifier if I_high<0; continuum existence, OS/Wightman reconstruction, nontriviality, and positive mass gap remain untouched.

## Equations

- endpoint source cumulant: `Z_v(s)=\left\langle e^{sX_v}\right\rangle_{a,t,v},\qquad \kappa_{4,v}=\left.\partial_s^4\log Z_v(s)\right|_{s=0}`. Valid when: Valid when the heat-kernel endpoint box is isolated and the source X_v is the same regulated Wilson flux used in the collar block.
- local quartic sign carrier: `\kappa_{4,v}^{\mathrm{sing}}(Y)=-\beta_v\,\mathrm{Tr}_{\mathrm{ad}}((\mathrm{ad}_Y)^4)+E_v,\qquad \beta_v\ge 0`. Valid when: Applies in the small endpoint heat-kernel regime after Gaussian Wick-square pieces are separated and BCH/Haar-Jacobian remainders are bounded.
- null incidence coefficient: `D_v=2G_{12,v}-4G_{13,v}-4G_{23,v}`. Valid when: Valid for the fixed three-hairpin Feshbach null vector after one-body factors and straight-segment f f contacts have cancelled.
- binary endpoint incidence table: `\begin{array}{c|c}(G_{12},G_{13},G_{23})&D_v\\(1,0,0)&2\\(0,1,0)&-4\\(0,0,1)&-4\\(1,1,0)&-2\\(1,0,1)&-2\\(0,1,1)&-8\\(1,1,1)&-6\end{array}`. Valid when: Valid for normalized equal endpoint boxes whose only unresolved overlaps are pairwise or triple coincident footprints charged locally.
- clipped endpoint lower and upper gates: `I_{\mathrm{low}}=M_G-C_{NF}\sum_v\overline\beta_v[D_v]_+-T_{\mathrm{tail}},\qquad I_{\mathrm{high}}=M_G+C_{NF}\sum_v\overline\beta_v[-D_v]_+ +T_{\mathrm{tail}}`. Valid when: Valid when beta_v intervals dominate the same-theory fourth cumulants and all nonlocal or unresolved endpoint interactions are included in T_tail.
- promotion and falsifier test: `I_{\mathrm{low}}\ge0\Rightarrow \text{finite block promoted},\qquad I_{\mathrm{high}}<0\Rightarrow \text{finite same-theory falsifier}`. Valid when: Requires the finite Schur-Feshbach tangent theorem, the fixed H,K data, and the endpoint interval enclosure above.

## Attempted Derivation

- Attack conceptual pressure: endpoint collapse must be sign-certified without leaving the same Wilson theory; raw R is representation-limited and a raw kappa4 spectrum is too strong because it ignores incidence signs.
- Start from the finite Schur-Feshbach post-H,K scalar and isolate the endpoint-local connected boundary-OPE part of the R term.
- Use connected source derivatives of log Z_v to remove disconnected Wick-square contributions; keep the already separated Wick-square Gram term as nonnegative.
- Use the null-channel incidence identity to cancel one-body Wilson factors and straight-segment C_A f f contact terms.
- Expand the heat-kernel endpoint-box measure in exponential coordinates; the Haar-Jacobian quartic gives a negative local fourth cumulant with coefficient beta_v>=0 up to certified remainder E_v.
- Contract the cumulant with the fixed pair weights 2,-4,-4; this gives D_v=2G12_v-4G13_v-4G23_v.
- Compute the normalized binary incidence table: only 12-only boxes have D_v>0; 13, 23, mixed, and triple boxes are protective or neutral for the negative compact-group kappa4.
- Clip the dangerous part to [D_v]_+ and bound all unresolved mixed endpoint interactions by T_tail, producing I_low and I_high.
- Apply the finite Schur-Feshbach gate: I_low>=0 promotes the finite block; I_high<0 is a finite same-theory falsifier.

Blocking gap: The actual regulated hairpin geometry still needs certified Gij_v endpoint intervals, beta_v source-stencil intervals, and a cutoff-uniform T_tail; the present cycle gives the incidence computation and interval theorem, not the numerical endpoint data.

## Falsifiers

- A certified set of endpoint boxes with beta-weighted 12-only dominance and tail large enough to force I_high<0 is a finite same-theory falsifier of this block.
- The heat-kernel source derivatives may fail to have cutoff-uniform M8_v bounds, invalidating the seven-point kappa4 certificate.
- Endpoint localization may be false: nonlocal corner tails could scale like the Gaussian margin rather than fit inside T_tail.
- A boundary counterterm or altered Wilson-loop renormalization may be needed to define Z_v, breaking the same-theory condition.
- Mixed endpoint boxes with orientation data outside the binary table could produce positive D_v not captured by the current carrier.
- The straight C_A f f cancellation may fail for the actual plaquette-sheet embedding rather than the idealized endpoint incidence geometry.

## Learning

Cycle 270 attacks the conceptual pressure of endpoint-collapse sign certification in the same Wilson theory. Declarative tension: finite collar OS positivity, unchanged gauge-invariant Wilson observables, and singular connected endpoint boundary OPE must jointly hold, but raw R cannot encode incidence signs and a raw kappa4 spectrum overstates danger. Compared with a global Schur-preimage matrix test, the clipped endpoint carrier is local after H,K; compared with formal OPE language, it exposes source differentiation, interval arithmetic, color factors, clipping, equivalence by regulated source data, and a finite locality budget T_tail. The hard gate changed is the finite post-H,K reflected-Wilson OS transfer gate: success promotes this block, failure gives a finite falsifier. The conceptual value signal is sharpness and route change: negative compact-group kappa4 is dangerous only through certified positive 12-only endpoint dominance plus tail. Clay-level continuum construction, OS/Wightman reconstruction, nontriviality, and positive mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a target-preserving falsifier probe.`
- Rationale: The branch has already passed H,K and isolated R/kappa4; another abstract OS restatement would loop. The concrete question is whether positive 12-only endpoint dominance can overpower the finite Schur-Feshbach margin in the same Wilson regulator.
- Situation seed: Heat-kernel plaquette-sheet SU(2) or SU(3) three-hairpin block with fixed H,K data, endpoint boxes classified as 12-only, 13-only, 23-only, mixed, triple, or tail.
- Varied variable: alpha, the beta-weighted fraction of endpoint source strength carried by 12-only boxes relative to all protective endpoint classes.
- Held-fixed controls: Same regulated Wilson loops, color trace normalization, and heat-kernel plaquette-sheet measure used for H,K., Fixed Feshbach null vector and pair weights 2,-4,-4., No boundary counterterm, no gauge fixing change, and no algebra enlargement., Uniform source step h and identical seven-point stencil policy for every endpoint box.
- Expected observation: There is a critical alpha at which I_low crosses zero; below it the finite endpoint contribution is certified safe, while above it actual source data can become a finite falsifier if T_tail is not small.
- Transfer certificate needed: A cutoff-uniform table of Gij_v intervals, beta_v intervals from log Z_v source stencils, an M8_v error bound, and a same-theory T_tail estimate before the thought experiment can affect proof obligations.

## Next Experiment

Compute the actual endpoint incidence table for the regulated three-hairpin plaquette sheets, then run the seven-point same-theory log Z_v stencil for SU(2) and SU(3) endpoint boxes to certify beta_v, M8_v, and T_tail intervals.

# Post-H,K endpoint-box R/kappa_4 interval bound via Ward-reduced flowed Wilson cumulants

## Candidate Lemma

Conditional Ward-reduced endpoint-box majorant: in the finite H,K plus-channel endpoint geometry, the connected four-curvature polarization in the same-theory flowed Wilson covariance is bounded by an eta^2 multiple of the positive pair baseline. This attacks the missing mediator between Schur-Feshbach leakage and Wilson positivity; it changes only the finite endpoint-box positivity gate, not the Clay existence or mass-gap gates.

## Definitions

- source object: centered renormalized gradient-flowed SU(N) Wilson hairpins \(\widehat W_{H_+}^{t,\epsilon}\), \(\widehat W_{K_+}^{t,\epsilon}\) built from finite H,K sheet currents and endpoint boxes.
- target object: a finite lower interval for \(R_{++}^{ren}/\kappa_4\) to compare with the Schur-Feshbach leakage scalar \(L_+=B_{+R}D^{-1}B_{R+}\).
- controlled interface: the covariance \(R_{++}^{ren}=\kappa_2(\widehat W_{H_+}^{t,\epsilon},\widehat W_{K_+}^{t,\epsilon})\), expanded by the flowed nonabelian Stokes formula and enclosed after Ward subtraction.
- same-theory condition: the Wilson action cutoff sequence, flow time, point splitting, cusp counterterms, and limiting Schwinger family are the same objects used for the surrounding OS/Wilson reconstruction attempt.
- carrier critique: raw Wilson contours are representation-limited and fragmented; sheet currents plus endpoint currents preserve orientation, color, reflection, and Ward data.
- efficient representation: encode H,K sheets and endpoints; preserve gauge/color/reflection/orientation invariants; use cumulant expansion, Ward subtraction, heat-kernel majorants, and interval arithmetic as primitives; quotient only by same-theory zero-pairing current equivalence; keep endpoint-box locality and finite-cell complexity; demote on Ward, cusp, plateau, geometry, or interval-width falsifier.

## Assumptions

- Model: four-dimensional Euclidean SU(N), N>=2, with Wilson lattice or smooth gauge-invariant UV regulator, followed by Yang-Mills gradient flow at time t and endpoint point splitting epsilon.
- Regime: finite endpoint boxes of size ell and separation d satisfy a << epsilon << sqrt(8t) <= c ell < ell << d, with plus-channel reflected orientation and positive pair geometry G_{++}>0.
- Uniformity: the one-loop flowed four-curvature kernel admits regulator-uniform sector kernels K_{3g}, K_{4g}, K_ct, K_end after local perimeter/cusp subtraction.
- Same-theory naturalness: no observable-specific counterterm is introduced outside the Wilson hairpin algebra used to define the Schwinger functions.
- Ward condition: disconnected products and one-hairpin perimeter/cusp terms are subtracted before the endpoint-box cumulant is compared with Schur-Feshbach leakage.
- Non-claim boundary: the lemma is a finite endpoint-box estimate, not a construction of the continuum Yang-Mills measure and not a Hamiltonian mass-gap theorem.

## Equations

- flowed endpoint covariance: `R_{++}^{ren}(t,\epsilon)=\kappa_2\!\left(\widehat W_{H_+}^{t,\epsilon},\widehat W_{K_+}^{t,\epsilon}\right)`. Valid when: Valid when the reflected Wilson hairpins are centered, cusp-subtracted, gradient-flowed, and evaluated in the same regulated Yang-Mills ensemble.
- pair-plus-connected decomposition: `\frac{R_{++}^{ren}}{\kappa_4}=2(N^2-1)G_{++}+\frac{g_t^2}{16\pi^2}N(N^2-1)\Xi_{++}+E_{\ge6}`. Valid when: Applies in the endpoint-box boundary-OPE regime where the flowed Wilson expansion is truncated with a controlled sixth-order remainder.
- sector polarization: `\Xi_{++}=I_{3g}[J_H,J_K;t,\epsilon]+I_{4g}[J_H,J_K;t,\epsilon]+I_{ct}[J_H,J_K;t,\epsilon]+I_{end}[J_H,J_K;t,\epsilon]`. Valid when: Requires the same-theory Ward-subtracted one-loop kernels and the finite H,K sheet-current representation with fixed endpoint boxes.
- Ward-reduced majorant: `|\Xi_{++}|\le C_W\eta^2G_{++},\qquad \eta=\ell/d+\sqrt{8t}/d+\epsilon/\ell`. Valid when: Valid if the sector kernels obey transverse heat-kernel derivative bounds after disconnected and one-hairpin cusp cancellations.
- endpoint promotion interval: `\frac{R_{++}^{ren}}{\kappa_4}\ge2(N^2-1)G_{++}\left(1-\frac{Ng_t^2C_W}{32\pi^2}\eta^2\right)-|E_{\ge6}|`. Valid when: Applies after diagonal normalization when G_{++} is positive and the Ward-reduced majorant plus remainder bound are certified.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: centered renormalized gradient-flowed SU(N) Wilson hairpins \(\widehat W_{H_+}^{t,\epsilon}\), \(\widehat W_{K_+}^{t,\epsilon}\) built from finite H,K sheet currents and endpoint boxes.; target object: a finite lower interval for \(R_{++}^{ren}/\kappa_4\) to compare with the Schur-Feshbach leakage scalar \(L_+=B_{+R}D^{-1}B_{R+}\).; Model: four-dimensional Euclidean SU(N), N>=2, with Wilson lattice or smooth gauge-invariant UV regulator, followed by Yang-Mills gradient flow at time t and endpoint point splitting epsilon..
- Conceptual pressure attacked: finite Schur-Feshbach positivity needs a same-theory endpoint mediator, but positive pair Wilson covariance and gradient-flow renormalization do not by themselves control the connected four-curvature polarization.
- Hard gate: finite endpoint-box positivity after H,K. Success supplies a lower bound for the corrected plus scalar; failure quarantines the R_{++} repair and leaves continuum construction, OS/Wightman axioms, nontriviality, and Hamiltonian mass gap untouched.
- Replace fragmented raw Wilson contours by sheet currents J_H,J_K plus endpoint currents. This is sharper than the older global non-Gaussian OS witness route because it targets the local Feshbach leakage L_+.
- Expand the centered flowed Wilson hairpins by the nonabelian Stokes formula through four curvature insertions; disconnected products and one-hairpin perimeter/cusp terms are subtracted before forming the covariance.
- The two cross-pairings of flowed curvatures give the positive baseline with color factor 2(N^2-1). Reflection-plus orientation makes the geometric quadratic form G_{++} nonnegative, and the branch must falsify zero geometry separately.
- The connected one-loop four-curvature sectors carry color factor N(N^2-1): three-gluon exchange I_3g, four-gluon vertex I_4g, counterterm I_ct, and endpoint-current sector I_end.
- Ward subtraction replaces endpoint currents by transverse representatives. The cancellation being used is disconnected-product removal plus one-hairpin cusp/perimeter subtraction; it should kill longitudinal endpoint residues and leave at least two transverse endpoint moments.
- Applying flowed heat-kernel derivative majorants to the transverse sector kernels gives the conditional estimate |Xi_{++}| <= C_W eta^2 G_{++}. This is the first calculable sign/size test: small eta preserves the positive pair baseline unless the one-loop interval violates the majorant.
- Insert the lower interval into Q_+^{corr}=Q_+^{bare}+R_{++}^{ren}/kappa_4-L_+. Promotion requires the interval lower endpoint to exceed L_+-Q_+^{bare}; demotion occurs if the interval upper endpoint does not.

Blocking gap: The proof still needs certified constants C_W by sector, a regulator-uniform bound on E_{>=6}, and a verified flow-window plateau for the normalized Xi_{++}/G_{++} ratio.

## Falsifiers

- falsifier: G_{++}=0 for the actual extracted H,K endpoint sheets, so the positive pair baseline cannot carry the plus channel.
- falsifier: a certified interval gives Xi_{++} so negative that the lower bound for R_{++}^{ren}/kappa_4 is at or below L_+-Q_+^{bare}.
- falsifier: one-hairpin cusp subtraction depends on the remote separation d, breaking same-theory locality.
- falsifier: longitudinal endpoint-current residues survive Ward subtraction with logarithmic epsilon dependence.
- falsifier: the normalized ratio Xi_{++}/G_{++} has no stable gradient-flow plateau as a -> 0 and epsilon -> 0.
- falsifier: interval cells are too wide to decide the promotion inequality within the four-cycle publication consolidation limit.

## Learning

The non-looping contribution is a conditional analytic enclosure: after Ward and cusp cancellation, the dangerous connected four-curvature polarization should be eta^2-suppressed relative to the positive pair baseline. This makes the hard gate explicit: endpoint-box positivity after H,K is promoted by a lower interval beating L_+, or the R repair is falsified. The local result is valuable without implying the Clay theorem because it tests one finite Schur-Feshbach obstruction while continuum existence, OS/Wightman axioms, nontriviality, and positive Hamiltonian mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design concrete falsifier probe now.`
- Rationale: The branch has already reduced R_{++} to a flowed Wilson cumulant; another abstract restatement would loop. The decisive unknown is the sign/size of the connected boundary-OPE polarization relative to the pair baseline and Schur-Feshbach leakage.
- Situation seed: Take SU(N) Wilson lattice Yang-Mills on a four-torus, apply gradient flow, and insert the extracted plus-channel H,K endpoint hairpin sheets in two reflected endpoint boxes separated by distance d; evaluate the same centered covariance R_{++}^{ren}.
- Varied variable: eta=ell/d, the endpoint-box size to separation ratio, with sqrt(8t)/d and epsilon/ell tied to fixed small constants.
- Held-fixed controls: Same Wilson action cutoff sequence and same gradient-flow scheme as the surrounding Schwinger family., Fixed finite H,K sheet-current combinatorics, plus-channel reflection orientation, and Schur-Feshbach leakage L_+., Identical cusp/perimeter subtraction rule for one-hairpin and two-hairpin cumulants., Fixed color group SU(N) and fixed normalization of kappa_4, G_{++}, and Q_+^{bare}.
- Expected observation: If Ward cancellation is valid, the normalized connected ratio |Xi_{++}|/G_{++} should scale like O(eta^2) or remain inside the certified majorant; a negative plateau large enough to violate the leakage inequality demotes the R repair.
- Transfer certificate needed: A regulator-uniform interval enclosure of the flowed one-loop sector kernels, a same-theory cusp-locality proof, and a continuum-flow plateau certificate before the thought experiment can alter finite proof obligations.

## Next Experiment

Build the sector-kernel interval table for the actual plus-channel H,K sheet currents: first certify cusp locality and Ward transversality, then enclose I_3g, I_4g, I_ct, I_end for eta in a decreasing grid and test whether the lower endpoint of R_{++}^{ren}/kappa_4 beats L_+-Q_+^{bare}.

# Post-H,K endpoint-box kappa4 interval certificate for finite Route A

## Candidate Lemma

For a finite post-H,K Wilson endpoint basis, the heat-kernel regulated Schur-corrected endpoint form is certified nonnegative if the PSD Gaussian color square dominates the compressed connected four-curvature cumulant, the OPE remainder, and the Schur hairpin energy. This changes only the finite Route A endpoint-box gate; it does not prove OS/Wightman reconstruction, a continuum limit, or the Clay mass gap.

## Definitions

- source object: finite cutoff SU(N) Yang-Mills Wilson measure with heat-kernel curvature smearing at scale sigma, fixed endpoint/collar sheets Sigma_i, transported flux variables Phi_i, and connected boundary-OPE cumulants.
- target object: the finite Schur-corrected endpoint-box quadratic form on the known post-H,K Wilson coefficient space, with vacuum line removed and no continuum spectral claim attached.
- controlled interface: sheet-kernel hypergraph whose vertices are smeared curvature insertions, colored edges are transported two- and four-point cumulants, and weights are Wilson/OPE coefficients compressed to the endpoint box.
- same-theory condition: the Wilson action/coupling, cutoff a, heat-kernel regulator sigma, reflection plane, endpoint basis, H,K Schur data, and counterterm normalization are identical in C_sigma, kappa4_sigma, E_OPE, and S_HK.
- alpha_N=(N^2-1)/(8N^2) uses fundamental SU(N) generators normalized by tr(T^aT^b)=delta^{ab}/2.
- C_sigma is the transported two-flux covariance matrix on endpoint sheets; kappa4_sigma is the compressed connected four-curvature cumulant matrix.
- S_HK=B^*E^{-1}B is the finite Schur-Feshbach hairpin subtraction produced by the known H,K block decomposition.

## Assumptions

- Model: finite lattice or ultraviolet-cutoff continuum SU(N) Yang-Mills with reflection-positive Wilson/heat-kernel regularization and sigma >= c a.
- Regime: endpoint box and Wilson basis are finite; H,K have already been extracted in the same basis and QHQ=E is strictly positive on the eliminated hairpin space.
- Uniformity: all interval bounds are outward-rounded at fixed a,sigma,g_R,N; no continuum limit or infinite-volume uniformity is claimed.
- Same-theory naturalness: the OPE subtraction, vacuum/perimeter normalization, curvature smearing, and Schur subtraction use the same cutoff theory, not matched data from another model.
- Boundary OPE assumption: the omitted endpoint-box terms form a Hermitian error E_OPE with operator norm at most e_OPE in the chosen finite coefficient norm.
- Compression assumption: the sheet-kernel hypergraph quotient preserves Wilson trace identities, sheet orientation, color transport, reflection support, and multiplicities.

## Equations

- transported smeared flux: `\Phi_i^a=\int_{\Sigma_i}dS_i^{\mu\nu}(x)\int K_\sigma(x-u)\,\mathrm{Ad}_{U_{x\to u}}^{ab}F_{\mu\nu}^b(u)\,du`. Valid when: Valid when each endpoint sheet is plaquette-resolved or smooth and the heat-kernel radius sigma stays above the ultraviolet cutoff scale.
- two-flux covariance: `C_{ij,\sigma}=\sum_a\langle \Phi_i^a\Phi_j^a\rangle_c`. Valid when: Valid when connected cumulants are evaluated in the same cutoff vacuum state for the transported curvature fluxes.
- post-HK endpoint polarization decomposition: `R_{ij,\sigma}=\alpha_N g_R^4\,(C_\sigma\circ C_\sigma)_{ij}+\frac{g_R^4}{16N^2}\kappa^{(4)}_{ij,\sigma}+E^{\mathrm{OPE}}_{ij,\sigma}`. Valid when: Applies after vacuum and perimeter subtraction in the fixed endpoint Wilson basis, using the same regulator and generator normalization.
- connected four-curvature cumulant: `\kappa^{(4)}_{ij,\sigma}=\int_{\Sigma_i^2\times\Sigma_j^2}\mathcal W_{ij}^{abcd}(x_1,x_2,y_1,y_2)\langle F^a_\sigma(x_1)F^b_\sigma(x_2)F^c_\sigma(y_1)F^d_\sigma(y_2)\rangle_c`. Valid when: Requires the same-theory boundary OPE with heat-kernel smearing, transported color tensors, and connected cumulant subtraction before endpoint compression.
- finite row-sum lower bound: `\lambda_{\min}(R_\sigma-S_{HK})\ge m_G-\frac{g_R^4}{16N^2}\rho_4-e_{\mathrm{OPE}}-s_{HK},\quad \rho_4=\max_i\sum_j|\kappa^{(4)}_{ij,\sigma}|`. Valid when: Valid for the finite Hermitian endpoint matrix after H,K are known, with rho_4 bounding the compressed kappa4 operator norm.
- hard endpoint gate: `\Delta_\sigma:=m_G-\frac{g_R^4}{16N^2}\rho_4-e_{\mathrm{OPE}}-s_{HK}>0`. Valid when: Promotes the finite endpoint-box positivity claim only when every term is computed in the same cutoff Yang-Mills theory.

## Attempted Derivation

- Conceptual pressure attacked: the post-H,K route needs a valid mediator from actual connected Wilson cumulants to Schur-corrected endpoint positivity, rather than another OS-density or scalar-R restatement.
- Fix the finite endpoint/collar Wilson coefficient space after H,K are known, and write the Schur correction as S_HK=B^*E^{-1}B with E=QHQ>0.
- Expand the vacuum/perimeter-normalized endpoint Wilson cumulant using heat-kernel transported curvature fluxes. Same-loop disconnected terms cancel because cumulants are taken after the same vacuum normalization.
- The crossed Gaussian curvature contractions yield alpha_N g_R^4(C_sigma o C_sigma). Since C_sigma is a covariance matrix, the Schur product theorem makes this term PSD on the finite endpoint space.
- The non-Gaussian remainder at the same order is exactly the compressed connected four-curvature cumulant kappa4_sigma, with transported color tensor W_ij^{abcd}. Higher endpoint terms are placed in E_OPE with norm e_OPE.
- Apply Weyl plus the finite row-sum norm bound ||kappa4_sigma|| <= max_i sum_j |kappa4_ij,sigma|. Subtract the Schur hairpin energy by ||S_HK|| <= s_HK.
- The hard gate is Delta_sigma>0. Success promotes only finite endpoint-box positivity for this H,K geometry; failure supplies a valid falsifier for this Wilson collar/hairpin route.

Blocking gap: The proof still needs a same-regulator interval table for kappa4 shell entries and numerical or symbolic H,K data giving s_HK. Reflection positivity alone does not bound the negative spectrum of the connected four-curvature cumulant sharply enough.

## Falsifiers

- kappa4 negative row sum exceeds the Gaussian margin after Schur subtraction, giving Delta_sigma <= 0.
- The heat-kernel shell tail U^{>L} is nonuniform in sigma/a, so no valid finite interval certificate survives regulator variation.
- The H,K Schur block is not strictly positive on Q, making S_HK undefined or unstable.
- A quotient orbit mixes inequivalent Wilson trace/color tensors, invalidating the compressed row-sum bound.
- Vacuum/perimeter normalization used for R differs from the one used for H,K, breaking the same-theory cancellation.
- The OPE remainder interval is larger than the entire Gaussian color-square margin.
- Stress case: an endpoint coefficient vector nearly lies in the kernel of C_sigma o C_sigma, so any small negative kappa4 shell demotes the branch.

## Learning

Declarative tension: same-theory Wilson/OPE coefficients, connected kappa4 negativity, and finite Schur-Feshbach subtraction must jointly control one endpoint quadratic form, but no Clay-level spectral conclusion is allowed. The current scalar R carrier is representation-limited; full OS observable density is too strong and circular for this local gate; raw plaquette enumeration is fragmented. Compared with those routes, the sheet-kernel hypergraph encodes sheets, weights, heat-kernel transporters, color tensors, shell labels, multiplicities, OPE errors, and Schur data; preserves gauge invariance, reflection support, Gaussian/kappa4 separation, endpoint compression, and same-theory normalization; supports cumulant contraction, quotienting, shell row/operator bounds, interval arithmetic, and Schur subtraction; quotients only by Wilson-invariant trace and sheet symmetries; keeps a finite endpoint-box locality budget; transfers only to Delta_sigma; and exposes falsifiers by margin failure, nonuniform envelopes, or non-invariant quotienting. The conceptual value signal is sharp and route-changing at finite scope: R becomes a computable connected Wilson cumulant interval, not a symbolic parameter, while OS/Wightman reconstruction, continuum existence, and the Hamiltonian mass gap remain untouched. Route next: proof search for the first same-regulator kappa4 shell interval, not abstraction-only looping.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the first same-regulator endpoint interval.`
- Rationale: The branch has already abstracted R; the next valid learning comes from testing whether a concrete finite endpoint box can keep Delta_sigma positive after kappa4 and Schur subtraction.
- Situation seed: Finite SU(N) hypercubic Wilson lattice endpoint box with three fixed collar sheets and the already-extracted H,K hairpin block, using heat-kernel curvature smearing and a sheet-kernel hypergraph quotient.
- Varied variable: q=sigma/a, the heat-kernel smearing radius in lattice units, varied over a small admissible integer window while the endpoint geometry is fixed.
- Held-fixed controls: Gauge group SU(N), Wilson action, bare/renormalized coupling convention, cutoff a, and reflection plane., The endpoint Wilson basis, collar/hairpin H,K blocks, Schur subtraction S_HK, vacuum/perimeter normalization, and boundary OPE truncation order., The quotient equivalence policy: only Wilson trace identities, exact sheet symmetries, and color-transport-preserving shell labels are allowed.
- Expected observation: If the route is viable, the PSD Gaussian margin m_G(q) stays above the kappa4 row envelope plus e_OPE(q)+s_HK(q) for at least one regulator window; if not, a localized negative kappa4 shell or Schur energy gives a falsifier.
- Transfer certificate needed: A same-regulator interval certificate listing m_G, rho_4, e_OPE, and s_HK with outward rounding, quotient invariance proof, and a statement that Delta_sigma>0 is only a finite endpoint-box positivity result.

## Next Experiment

Build the first q=sigma/a endpoint-box shell table: compute C_sigma, alpha_N(C o C), quotient multiplicities, kappa4 nearest-shell interval, E_OPE bound, and s_HK; then report the outward-rounded Delta_sigma sign.
