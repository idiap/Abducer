# cycle-0271

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint source-interval certificate for the post-H,K Wilson block

## Candidate Lemma

For the locked finite three-hairpin Wilson block with H,K already fixed, the connected endpoint part of the post-H,K Schur-Feshbach scalar is certified by same-regulator endpoint source intervals. If the lower endpoint of I_gate is nonnegative, this finite block passes the same-theory OS gate; if the upper endpoint is negative, this is a finite same-theory falsifier. No continuum Yang-Mills existence or mass gap conclusion follows.

## Definitions

- source object: heat-kernel regulated SU(N) plaquette-sheet endpoint boxes for the locked reflected three-hairpin Wilson block, with H,K already fixed and the Feshbach null vector contracted.
- target object: a scalar interval for the finite post-H,K Schur-Feshbach OS gate M_G+R_end, deciding only this Wilson block.
- controlled interface: same-regulator source derivatives of endpoint log partition functions are contracted with null-channel endpoint incidences D_v and a cutoff-uniform tail bound.
- same-theory condition: no boundary counterterm, no Wilson-loop renormalization change, identical heat-kernel action, identical gauge-invariant loop algebra, and cutoff-uniform endpoint/tail estimates.
- endpoint carrier: L_v(s)=log Z_v(s) is the singlet-projected endpoint-box log partition function with source s coupled to the null-channel Wilson flux X_v.
- incidence carrier: G_{ij,v} is the signed geometric/color overlap of endpoint box v between reflected Wilson hairpin pair i,j after parallel transport to the singlet channel.
- color factor: C_N=(g^4/4)(T_F/N)^2 is the common endpoint fourth-cumulant prefactor for the fundamental Wilson traces.

## Assumptions

- Model: finite cutoff SU(N) lattice Yang-Mills with heat-kernel plaquette action and reflection-symmetric plaquette-sheet Wilson regulators near the boundary plane.
- Regime: H,K and the Feshbach null vector are already computed for this finite block; only the residual connected endpoint polarization R_end is under test.
- Uniformity: the endpoint source functions L_v are C^8 on |s|<=3h with cutoff-uniform derivative bounds M_{8,v}.
- Same-theory condition: all source evaluations use the identical Wilson loops, action, regulator, and normalization as the collar OS matrix.
- Cancellation condition: connected logarithms remove Wick-square Gram pieces, and the straight C_A f f contact cancels by the null incidence identity in the same regulator.
- Tail condition: all non-endpoint boxes, corner leakage, and regulator-mismatch errors are bounded by a cutoff-uniform scalar tau.
- Naturalness: endpoint intervals are identified only by equality of regulated source derivatives, not by formal OPE symbolism.

## Equations

- connected endpoint cumulant: `\kappa_{4,v}(\xi_v)=\left.\partial_s^4 L_v(s;\xi_v)\right|_{s=0},\qquad L_v(s;\xi_v)=\log \mathbb E_{a,t}\exp(sX_v(\xi_v))`. Valid when: Valid when the heat-kernel plaquette-sheet regulator and singlet source projection are fixed before taking endpoint-box derivatives.
- Rij endpoint contraction: `R^{\mathrm{conn}}_{ij,\mathrm{end}}=C_N\sum_v \kappa_{4,v}G_{ij,v}+T_{ij},\qquad C_N={g^4\over4}\left({T_F\over N}\right)^2`. Valid when: Valid when the connected Wilson boundary OPE is localized to endpoint boxes after Wick-square and straight-contact cancellations.
- null incidence reduction: `R_{\mathrm{end}}=C_N\sum_v\kappa_{4,v}D_v+T_{\mathrm{tail}},\qquad D_v=2G_{12,v}-4G_{13,v}-4G_{23,v}`. Valid when: Valid when H and K are already fixed and the Feshbach null vector has been contracted before endpoint clipping.
- seven-point fourth-source stencil: `\widehat\kappa_{4,v}(h)={-L_v(3h)+12L_v(2h)-39L_v(h)+56L_v(0)-39L_v(-h)+12L_v(-2h)-L_v(-3h)\over 6h^4},\quad |\kappa_{4,v}-\widehat\kappa_{4,v}(h)|\le {7h^4M_{8,v}\over240}`. Valid when: Valid when L_v is C^8 on the chosen source interval and the eighth derivative bound is cutoff uniform.
- clipped endpoint gate interval: `I_{\mathrm{gate}}=M_G+C_N\left[\sum_v(-\beta_v^+[D_v]_+ +\beta_v^-[-D_v]_+),\sum_v(-\beta_v^-[D_v]_+ +\beta_v^+[-D_v]_+)\right]+[-\tau,\tau]`. Valid when: Valid when every endpoint fourth cumulant is certified inside [-beta_v^+,-beta_v^-] and the residual tail is bounded by tau.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: heat-kernel regulated SU(N) plaquette-sheet endpoint boxes for the locked reflected three-hairpin Wilson block, with H,K already fixed and the Feshbach null vector contracted.; target object: a scalar interval for the finite post-H,K Schur-Feshbach OS gate M_G+R_end, deciding only this Wilson block.; Model: finite cutoff SU(N) lattice Yang-Mills with heat-kernel plaquette action and reflection-symmetric plaquette-sheet Wilson regulators near the boundary plane..
- Conceptual pressure attacked: endpoint collapse must become sign-certifiable in the unchanged Wilson theory, rather than hidden inside symbolic R or an overstrong raw kappa_4 spectrum.
- Declarative tension: finite collar OS positivity, unchanged gauge-invariant Wilson observables, and singular connected endpoint boundary OPE must jointly hold; the missing mediator is a cutoff-uniform signed endpoint source carrier.
- Start from the finite Schur-Feshbach tangent-cone output: H,K are fixed and the remaining local gate is the scalar M_G+R_end for the Feshbach null channel.
- Write the actual Yang-Mills input as the connected Wilson four-flux endpoint cumulant kappa_{4,v}=partial_s^4 log Z_v(s)|0 in the heat-kernel plaquette-sheet regulator.
- Use connected logarithms to remove Wick-square Gram pieces and the null incidence identity to cancel the straight C_A f f contact, leaving endpoint boxes plus T_tail.
- Contract the endpoint cumulants with the actual color/geometric incidence D_v=2G12_v-4G13_v-4G23_v and common factor C_N=(g^4/4)(T_F/N)^2.
- Certify each kappa_{4,v} by seven same-theory source evaluations with a C^8 error interval, then clip the negative endpoint cumulant by [D_v]_+ and [-D_v]_+.
- Obtain I_gate. Its lower endpoint >=0 promotes this finite Wilson block; its upper endpoint <0 gives a finite same-theory falsifier.

Blocking gap: The actual endpoint incidence table G_{ij,v}, same-theory source intervals for L_v, and cutoff-uniform T_tail are not yet computed for the physical three-hairpin geometry.

## Falsifiers

- A certified interval with sup I_gate<0 is a finite same-theory falsifier for the post-H,K reflected-Wilson OS transfer gate.
- The heat-kernel endpoint source L_v requires a boundary counterterm or Wilson-loop renormalization not present in the collar theory.
- The straight C_A f f contact fails to cancel after the actual endpoint orientation and parallel-transport conventions are inserted.
- The source derivative bound M8 or tail tau is not cutoff uniform, so the endpoint interval is not valid for the intended same-theory passage.
- The actual incidence table has certified positive 12-only endpoint dominance large enough that clipped negative kappa_4 overwhelms M_G.
- Endpoint carriers judged equivalent by formal OPE but not by equal regulated source derivatives give different I_gate values.

## Learning

Cycle 271 refits the last R/kappa_4 obstruction into a valid finite endpoint source-interval problem. The conceptual pressure is endpoint collapse in the same Wilson theory. The declarative tension is that collar OS positivity, unchanged gauge-invariant Wilson observables, and connected endpoint OPE singularities must jointly hold, while symbolic R is representation-limited and a raw kappa_4 spectrum is too strong because it ignores null incidence. Compared with the global Schur-preimage matrix route, the clipped source carrier is local after H,K and exports one scalar I_gate; compared with formal OPE language, it exposes primitive operations: source differentiation, interval arithmetic, color multiplication, incidence contraction, clipping, and tail addition. Efficient representation requirements are now explicit: encode endpoint boxes, L_v source stencils, beta intervals, G and D incidences, C_N, and tau; preserve Wilson normalization, null cancellations, reflection symmetry, cutoff uniformity, and same-theory observables; identify equivalent carriers only by equal regulated source data; keep locality finite by charging leftovers to T_tail; transfer only I_gate to the finite OS gate; demote on negative interval, nonuniform tail, or boundary counterterm. Hard gate changed: the finite post-H,K reflected-Wilson OS transfer gate can be promoted or falsified by actual endpoint data. Clay-level continuum construction, full OS/Wightman reconstruction, nontriviality, and positive Hamiltonian mass gap remain untouched. Conceptual value signal: sharpness and route change, because negative compact-group kappa_4 is not the falsifier; certified positive 12-endpoint dominance plus uncontrolled tail is.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and promotion rehearsal for the finite post-H,K endpoint interval.`
- Rationale: The branch no longer needs another abstract OS/Wilson restatement; it needs to know whether actual endpoint incidence can make negative compact-group kappa_4 dangerous in the same theory.
- Situation seed: Take the regulated SU(N) heat-kernel lattice three-hairpin Wilson block with fixed H,K, fixed null vector, and endpoint boxes v at the reflection-plane hairpin tips. Compute L_v(kh) for k=-3,...,3 and contract with the same endpoint incidences G_{ij,v}.
- Varied variable: Endpoint dominance ratio eta_v=G_{12,v}/(G_{13,v}+G_{23,v}) produced by sliding only the first hairpin endpoint within a fixed reflection-symmetric boundary box.
- Held-fixed controls: The heat-kernel plaquette action, lattice spacing sequence, and reflection-symmetric plaquette-sheet regulator are unchanged., The Wilson loop algebra, trace normalization, H,K data, Feshbach null vector, and color factor C_N are held fixed., Source step h is chosen inside a cutoff-uniform C^8 interval, and all off-endpoint effects remain charged to the same tau budget.
- Expected observation: For eta_v<=2 the negative endpoint kappa_4 contributes protectively or harmlessly; only eta_v>2 plus sufficiently large beta_v and tail can drive I_gate below zero.
- Transfer certificate needed: A same-theory certificate consisting of audited endpoint source intervals, exact incidence table, straight-contact cancellation check, and cutoff-uniform T_tail before the thought-experiment intuition may affect proof obligations.

## Next Experiment

Compute the endpoint incidence table for the actual three-hairpin plaquette sheets, then run the seven-point same-theory source stencil for each endpoint box and assemble I_gate with an audited tau bound.

# Post-H,K endpoint-box R certificate by Ward-suppressed flowed cumulants

## Candidate Lemma

For fixed H,K endpoint sheets, the flowed point-split R++ has a valid lower interval if the Ward-subtracted connected four-curvature sectors obey |Xi_W|<=c_W eta^2 G++; promotion occurs exactly when this interval beats L_+.

## Definitions

- source object: flowed 4D pure SU(N) Yang-Mills Schwinger family with fixed H,K hairpin sheet currents in one endpoint box.
- target object: finite endpoint-box Schur-Feshbach scalar R_{++}^{ren} compared with the already computed leakage L_+.
- controlled interface: centered cusp-renormalized Wilson hairpin covariance represented by sheet currents, endpoint currents, and Ward-subtracted sector kernels.
- same-theory condition: gradient flow, point-splitting, cusp subtraction, and cutoff removal use the same OS-positive lattice/continuum Schwinger family.
- carrier critique: raw Wilson contours are representation-limited; sheet plus endpoint currents preserve gauge, color, reflection, and orientation data.
- eta:=rho/sqrt(8 tau), with rho the endpoint-box scale and tau the Yang-Mills gradient-flow time.

## Assumptions

- Model: pure Euclidean SU(N) Yang-Mills at cutoff a with gradient flow tau>0 and gauge-invariant Wilson hairpins.
- Regime: a << epsilon << rho << sqrt(8 tau), with H,K geometry fixed in physical units and no change of bare action.
- Uniformity: cusp/perimeter counterterms are fixed by the one-hairpin scheme and are not retuned for the two-hairpin covariance.
- Ward assumption: the I_{3g}, I_{4g}, I_{ct}, and I_{end} kernels are subtracted before interval bounding, so contact and longitudinal pieces cancel cellwise.
- Remainder assumption: higher flowed sectors have an interval bound Delta_{>=2} in the same renormalized coupling window.

## Equations

- flowed endpoint cumulant: `R_{++}^{\tau,\rho}:=\kappa_2\!\left(:W_{H,+}^{\tau,\rho}:,:W_{K,+}^{\tau,\rho}:\right)_{cusp}`. Valid when: Valid when H,K are fixed finite hairpin sheets, tau regulates fields, and cusp-renormalized centered Wilson observables remain in the same cutoff family.
- pair-plus-polarization: `R_{++}^{\tau,\rho}=2(N^2-1){\mathcal G}_{++}^{\tau,\rho}+N(N^2-1)g_R^2(\mu)\Xi_{++}^{W}(\tau,\rho)+\Delta_{\ge2}`. Valid when: Applies in the flowed boundary-OPE window after disconnected products and one-hairpin perimeter/cusp counterterms have been subtracted in one scheme.
- Ward-suppressed promotion interval: `R_{++}^{\tau,\rho}\ge 2(N^2-1){\mathcal G}_{++}^{\tau,\rho}\left(1-\frac{N}{2}c_W g_R^2\eta^2\right)-|\Delta_{\ge2}|,\quad R_{++}^{\tau,\rho}>L_+`. Valid when: Requires cellwise Ward-subtracted heat-kernel bounds for I_{3g}, I_{4g}, I_{ct}, I_{end} and a valid interval remainder for higher sectors.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: flowed 4D pure SU(N) Yang-Mills Schwinger family with fixed H,K hairpin sheet currents in one endpoint box.; target object: finite endpoint-box Schur-Feshbach scalar R_{++}^{ren} compared with the already computed leakage L_+.; Model: pure Euclidean SU(N) Yang-Mills at cutoff a with gradient flow tau>0 and gauge-invariant Wilson hairpins..
- Replace raw H,K Wilson contours by flowed sheet currents plus endpoint currents; expand centered hairpins to the two-cross-pair and connected four-curvature sectors.
- Disconnected products and one-hairpin perimeter/cusp subtractions cancel, leaving a positive pair baseline with color factor 2(N^2-1).
- Apply Ward subtraction to I_{3g}, I_{4g}, I_{ct}, I_{end}; derivative heat-kernel majorants give the candidate eta^2 suppression of Xi_W relative to G++.
- Compare the certified lower interval with L_+; success promotes finite endpoint-box positivity, failure quarantines only this R repair.

Blocking gap: The missing mediator is a rigorous cellwise proof of the Ward-subtracted heat-kernel majorant with stable constants across epsilon,rho,tau windows.

## Falsifiers

- falsifier: the Ward-subtracted sector intervals show an O(eta) or O(1) connected polarization instead of eta^2 suppression.
- The flow plateau fails: R++ changes under tau variation after fixed cusp/perimeter renormalization.
- The interval lower bound is valid but remains <=L_+, so finite endpoint-box positivity is not repaired.
- Sheet-current equivalence erases G++ or flips orientation, destroying the positive pair baseline.

## Learning

Conceptual pressure: finite Feshbach positivity needs a same-theory endpoint mediator; pair positivity and flow renormalization do not control C4. Carrier revision: raw contours are fragmented; sheet/endpoint currents are efficient. Hard gate: endpoint-box positivity after H,K; success promotes, failure quarantines. Clay gates remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and interval-kernel calibration.`
- Rationale: The branch needs a concrete R++ sign/size test; another abstract Wilson/OS restatement would not decide the finite endpoint-box gate.
- Situation seed: Flowed lattice SU(N) Yang-Mills endpoint box with the extracted H,K hairpin sheets, centered cusp-renormalized Wilsons, and sector kernels I_{3g},I_{4g},I_{ct},I_{end}.
- Varied variable: eta=rho/sqrt(8 tau), varied by changing the endpoint-box size rho at fixed physical H,K geometry and fixed flow scheme.
- Held-fixed controls: Same bare-action trajectory and same OS-positive Schwinger family., Fixed H,K sheet orientations, color normalization, and endpoint locality., Fixed Schur-Feshbach leakage L_+ and centered Wilson normalization., Fixed Ward/cusp subtraction prescription.
- Expected observation: R++/G++ should approach 2(N^2-1) with a downward correction bounded by O(g_R^2 eta^2); a plateau lower interval above L_+ promotes the local gate.
- Transfer certificate needed: Uniform continuum-in-cutoff flow window, proved Ward/cusp cancellation, and certified interval quadrature for the same-theory flowed cumulant before intuition enters proof obligations.

## Next Experiment

Write the sheet-current kernels for I_{3g}, I_{4g}, I_{ct}, I_{end}; compute interval bounds for c_W and Delta_{>=2} over eta in [0.05,0.25].

# Cycle 271: same-regulator kappa4 shell interval for post-H,K endpoint box

## Candidate Lemma

For a finite endpoint Wilson basis E and already known H,K Schur data, a heat-kernel same-regulator shell envelope for the connected four-curvature cumulant gives a valid lower interval for the Schur-corrected endpoint form. A positive interval promotes only the finite Route A endpoint-box gate; a negative interval is a falsifier for this collar/hairpin geometry.

## Definitions

- source object: heat-kernel regulated SU(N) cutoff Yang-Mills Wilson expectations at spacing a or UV scale Lambda, with reflected endpoint Wilson sheets S_i and smearing sigma >= c a^2.
- target object: the finite endpoint quadratic form on coefficient vectors x in span(E) after Schur-Feshbach elimination of the already computed collar/hairpin H,K blocks.
- controlled interface: the connected boundary-OPE polarization R_sigma is compressed to span(E), decomposed into a Gaussian flux square, connected kappa_4 shell operator, OPE remainder, and Schur subtraction S_HK=B^*E_HK^{-1}B.
- same-theory condition: all Wilson loops, heat-kernel smearing, coupling normalization, reflection map, cumulants, H,K matrices, and OPE errors are computed in the identical cutoff theory before any continuum or Hamiltonian claim.
- carrier: sheet-kernel hypergraph with vertices given by smeared sheets, colored transported flux legs, shell labels, multiplicities, trace tensors, and Schur block labels.
- hard gate: Delta_sigma>0 for the compressed Schur-corrected endpoint matrix; success changes finite Route A positivity only, while OS/Wightman reconstruction, continuum existence, and Hamiltonian mass gap remain untouched.

## Assumptions

- Model/regime: finite-volume reflection-positive SU(N) Wilson cutoff theory or a constructive finite regulator with heat-kernel smearing sigma >= c a^2 and endpoint sheets at positive distance from the reflection plane except for prescribed boundary collars.
- Uniformity: the endpoint basis E is finite, H,K are computed in the same basis and regulator, and the hairpin block E_HK=QHQ is positive invertible with a recorded lower bound eta_HK>0.
- Naturalness: small-sheet boundary OPE is used only up to the endpoint-box order displayed; its remainder is bounded by e_OPE(sigma,a,E) in operator norm.
- Kappa_4 input: for each shell ell, the connected four-flux cumulant entries obey an invariant bound |(kappa_{4,sigma})_{ij}| <= b_ell(sigma) whenever the sheet pair (i,j) lies in shell ell.
- Same-theory non-claim: the lemma does not assert existence of a continuum YM measure, OS/Wightman reconstruction, or a positive Hamiltonian mass gap; it certifies or falsifies one finite Wilson endpoint calculation.

## Equations

- transported smeared curvature flux: `\Phi_i^a(\sigma)=\int_{S_i} h_\sigma(z,z_i)\,U_{z_i z}^{ab}\,F_{\mu\nu}^b(z)\,dS_i^{\mu\nu}(z)`. Valid when: Valid when each Wilson sheet S_i is inside the endpoint box, the heat-kernel smearing scale satisfies sigma >= c a^2, and parallel transport uses fixed same-theory tree or geodesic paths.
- quadratic Wilson OPE carrier: `\mathcal Q_i(\sigma)=-\frac{g_R^2}{4N}\sum_a \Phi_i^a(\sigma)\Phi_i^a(\sigma)`. Valid when: Applies after normalized fundamental Wilson traces are expanded to quadratic curvature order with tr(T^aT^b)=delta^{ab}/2 and linear color-trace terms cancel.
- connected endpoint polarization: `R_{ij,\sigma}=\langle \mathcal Q_i(\sigma);\theta\mathcal Q_j(\sigma)\rangle_c`. Valid when: Valid when vacuum and perimeter counterterm contributions are subtracted in the same cutoff theory and theta is the reflection used for OS positivity.
- Gaussian plus connected four-curvature split: `R_\sigma=\alpha_N g_R^4(C_\sigma\circ C_\sigma)+\frac{g_R^4}{16N^2}\kappa_{4,\sigma}+E_{\mathrm{OPE},\sigma},\qquad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after vacuum and perimeter cancellation for small heat-kernel Wilson sheets, with color-isotropic two-flux covariance and all non-Gaussian four-flux terms assigned to kappa_4.
- connected kappa4 entry: `(\kappa_{4,\sigma})_{ij}=\sum_{a,b,c,d}\gamma_i^{ab}\gamma_j^{cd}\,\langle \Phi_i^a\Phi_i^b;\theta\Phi_j^c\theta\Phi_j^d\rangle_{c,\sigma}`. Valid when: Requires the same regulator, sheet orientations, trace tensors gamma_i, and connected cumulant subtraction used in the Wilson OPE definition of R_sigma.
- shell row-sum negative-spectrum bound: `M_{4,\sigma}^-:=\|(P_E\kappa_{4,\sigma}P_E)_-\|\le \max_i\sum_{\ell} n_{i\ell}\,b_\ell(\sigma)`. Valid when: Requires a Wilson-invariant shell partition of endpoint-sheet pairs and entrywise connected kappa_4 bounds stable under trace and sheet symmetries.
- post-HK endpoint interval: `\Delta_\sigma\ge \lambda_{\min}(\alpha_N g_R^4P_E(C_\sigma\circ C_\sigma)P_E)-\frac{g_R^4}{16N^2}M_{4,\sigma}^- -\|P_EE_{\mathrm{OPE},\sigma}P_E\|-\|B^*E_{HK}^{-1}B\|`. Valid when: Valid when the finite Schur block E_HK is positive invertible, H,K have been computed in the same Wilson basis, and all operators are compressed to P_E.

## Attempted Derivation

- Conceptual pressure attacked: same-theory Wilson/OPE coefficients, connected kappa_4 negativity, and finite Schur-Feshbach subtraction must jointly control one endpoint quadratic form without invoking OS observable density or claiming a Clay-level mass gap.
- Choose a finite reflected endpoint sheet basis E and the heat-kernel regulator sigma >= c a^2 used already in the H,K collar/hairpin calculation.
- Expand each normalized Wilson sheet through the quadratic curvature carrier Q_i; trace normalization gives the coefficient -g_R^2/(4N), while vacuum and perimeter terms cancel under connected cumulant subtraction.
- Write R_ij as the connected covariance of Q_i with theta Q_j; Wick-paired two-flux contractions yield alpha_N g_R^4(C circ C)_ij with alpha_N=(N^2-1)/(8N^2).
- Define the non-Gaussian remainder as the connected four-curvature cumulant kappa_{4,sigma} with explicit color trace tensors gamma_i and gamma_j; this is the actual YM input, not a symbolic R parameter.
- Compress R to P_E, subtract the known Schur hairpin energy S_HK=B^*E_HK^{-1}B, and use the Schur product theorem to keep the Gaussian block nonnegative.
- Partition sheet pairs into locality shells and bound the negative spectral part of P_E kappa_4 P_E by the Wilson-invariant row sum max_i sum_ell n_iell b_ell(sigma).
- The hard gate is Delta_sigma>0. Success proves finite endpoint-box positivity after H,K; failure gives a valid falsifier for this Wilson collar/hairpin route only.

Blocking gap: The missing proof ingredient is a same-regulator quantitative shell envelope b_ell(sigma) for the connected four-flux cumulant in the first concrete H,K endpoint geometry. Without it, Delta_sigma is a formula with a computable slot, not a completed certificate.

## Falsifiers

- falsifier: the first nearest-shell bound b_0(sigma) alone makes g_R^4 M_4^-/(16N^2) exceed the Gaussian margin minus OPE and Schur terms.
- The heat-kernel shell quotient changes the value of kappa_4 under a Wilson trace identity, showing the carrier is not representation invariant.
- The connected cumulant subtraction leaves uncanceled perimeter or vacuum pieces, so R_sigma is not a same-theory boundary-OPE polarization.
- The H,K Schur block is singular or has eta_HK too small, making S_HK dominate every available Gaussian endpoint margin.
- The OPE remainder is nonuniform as sigma/a^2 or endpoint box size is varied, invalidating a stable finite interval.
- A direct plaquette-sheet computation gives a negative Delta interval for the first collar/hairpin geometry, demoting Route A for that geometry without touching the Clay target.

## Learning

Declarative tension: Wilson/OPE data, connected kappa_4 negativity, and Schur-Feshbach subtraction must be simultaneously valid in one cutoff theory, but the result must not be inflated into OS/Wightman reconstruction or a mass-gap theorem. The scalar R carrier is too weak and representation-limited; full OS observable density is too strong and circular for this local gate; raw plaquette enumeration is fragmented. The sheet-kernel hypergraph remains the efficient representation because it encodes sheets, weights, heat-kernel transporters, color tensors, shell labels, multiplicities, OPE errors, and Schur data; preserves gauge invariance, reflection support, Gaussian/kappa_4 separation, endpoint compression, and same-theory normalization; supports cumulant contraction, quotienting, shell row/operator bounds, interval arithmetic, and Schur subtraction; quotients only by Wilson-invariant trace and sheet symmetries; keeps a finite endpoint-box locality budget; transfers only to Delta_sigma; and has falsifiers by margin failure, nonuniform envelopes, or non-invariant quotienting. Conceptual value signal: the branch is sharp and route-changing at finite scope because it converts the unknown boundary-OPE polarization into a concrete sign/size interval for the first H,K endpoint box while leaving all Clay-level gates untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and proof-search guide, not as another abstraction scaffold.`
- Rationale: The branch has already identified R as a connected Wilson cumulant; the current missing object is the first same-regulator kappa_4 shell interval that can change the finite endpoint proof state.
- Situation seed: Finite SU(N) Wilson cutoff on a reflected box with the already computed H,K collar/hairpin basis, heat-kernel smeared endpoint sheets S_i, and R_ij measured or symbolically contracted as the connected covariance of quadratic curvature carriers Q_i and theta Q_j.
- Varied variable: The smearing-to-cutoff ratio rho=sigma/a^2, with rho varied over a fixed finite grid above the reflection-positive heat-kernel threshold.
- Held-fixed controls: Same Wilson action, bare/renormalized coupling convention, gauge group SU(N), and finite endpoint sheet set E., Same reflection plane, Wilson trace normalization, heat-kernel transporter convention, and H,K Schur matrices., Same OPE truncation order, same connected-cumulant subtraction, and same shell quotient policy.
- Expected observation: If the route is viable, the Gaussian margin m_G(rho) remains positive while the shell row-sum envelope for negative kappa_4 plus OPE and Schur costs falls below it for at least one rho. If not, Delta_rho stays nonpositive and supplies a finite falsifier.
- Transfer certificate needed: A rigorous same-regulator interval for b_ell(rho), e_OPE(rho), and s_HK, plus proof that the shell quotient and color tensors reproduce the original Wilson cumulant before Delta_rho is allowed to affect proof obligations.

## Next Experiment

For the first available H,K collar/hairpin geometry, enumerate endpoint sheets, compute C_sigma and alpha_N g_R^4(C_sigma circ C_sigma), then contract the nearest-shell connected four-flux plaquette sheets defining kappa_{4,sigma}; record b_0(sigma), e_OPE, S_HK, and the resulting interval I_Delta.
