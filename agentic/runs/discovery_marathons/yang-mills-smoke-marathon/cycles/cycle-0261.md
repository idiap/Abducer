# cycle-0261

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Post-H,K Endpoint kappa4 Interval Certificate

## Candidate Lemma

Clipped endpoint-dominance certificate: after the already fixed H,K three-hairpin block and Schur-Feshbach null contraction, the remaining connected boundary-OPE polarization is certified by endpoint heat-kernel source intervals. Negative compact-group kappa4 contributes dangerously only through positive endpoint dominance D_v>0; otherwise it is protective or invisible. This is a finite same-theory endpoint certificate, not a Clay mass-gap proof.

## Definitions

- source object: regulated SU(N) Yang-Mills Wilson plaquette-sheet endpoint boxes B_v(a,ell) with heat-kernel action, gauge-invariant parallel-transported flux sources eta_{ij,v}, and connected source derivatives of log Z_{v,a,ell}.
- target object: a certified interval for the post-H,K Schur-Feshbach null-channel endpoint contribution M_G+R_end in the locked reflected Wilson OS block.
- controlled interface: the map from singlet connected four-flux endpoint cumulants, color factors, endpoint incidence intervals, and tail bounds to the scalar Feshbach endpoint interval.
- same-theory condition: the same lattice action, Wilson normalization, reflection plane, gauge-invariant test algebra, and collar-to-endpoint localization are used throughout; no boundary counterterm, algebra enlargement, or post hoc diagonal normalization is inserted.
- K_v^{sing}(eta) is the singlet-projected fourth connected source derivative in one endpoint box.
- D_v=2G_{12,v}-4G_{13,v}-4G_{23,v} is the null-channel endpoint incidence dominance after Wick-square and straight f f cancellations.
- beta_v is the positive magnitude of the leading negative compact-group fourth cumulant, with kappa_{4,v}^{sing} in [-beta_v^+,-beta_v^-].

## Assumptions

- Model: finite-volume hypercubic heat-kernel lattice regularization of pure SU(N) Yang-Mills with Wilson plaquette-sheet observables representing the fixed three-hairpin collar geometry.
- Regime: endpoint boxes have radius ell larger than a and smaller than the collar separation scale; distinct endpoint boxes are separated enough that mixed endpoint cumulants are placed in T_tail.
- Uniformity: beta_v^\pm, D_v^\pm, and T_tail^\pm are bounded uniformly along the cutoff-removal subsequence used for the same Wilson block.
- Cancellation assumption: connected logarithms remove Wick-square Gram pieces, and the null incidence identity cancels the straight C_A f f contact on non-endpoint shared segments.
- Same-theory assumption: source differentiation is performed inside the original heat-kernel measure and then set to zero; it does not define a new boundary theory.
- Larger YM balance: success strengthens the OS positivity/same-theory transfer gate for this finite Wilson block; it leaves nontrivial continuum existence and positive Hamiltonian mass gap untouched.

## Equations

- endpoint-source-cumulant: `\kappa_{4,v}^{\mathrm{sing}}(\eta)=\left.\partial_s^4\log Z_{v,a,\ell}(s\eta)\right|_{s=0},\quad Z_{v,a,\ell}(s\eta)=\left\langle e^{sX_v(\eta)}\right\rangle_{a,\ell}`. Valid when: Valid when the endpoint source X_v is a gauge-invariant parallel-transported plaquette-sheet flux insertion inside one heat-kernel endpoint box.
- post-cancellation-endpoint-decomposition: `R_{\mathrm{end}}=c_{\mathrm{col}}\sum_v \kappa_{4,v}^{\mathrm{sing}}D_v+T_{\mathrm{tail}},\quad c_{\mathrm{col}}={g_a^4\over4}\left({T_F\over N}\right)^2`. Valid when: Applies after Wick-square Gram positivity and straight f f incidence cancellation have already been performed for the fixed hairpin block.
- incidence-dominance: `D_v=2G_{12,v}-4G_{13,v}-4G_{23,v},\quad G_{ij,v}=\langle\eta_{ij,v},\eta_{ij,v}\rangle_{B_v}^{\mathrm{geom}}`. Valid when: Requires the same endpoint-box geometry and null Feshbach weights inherited from the fixed reflected Wilson three-hairpin calculation.
- clipped-product-interval: `\kappa_{4,v}\in[-\beta_v^+,-\beta_v^-],\ D_v\in[d_v^-,d_v^+]\Rightarrow -\beta_vD_v\in[\ell_v,u_v]`. Valid when: Valid when beta_v is nonnegative and interval arithmetic is applied independently to each localized endpoint cumulant contribution.
- clipped-bounds: `\ell_v=-\beta_v^+[d_v^+]_+ + \beta_v^-[-d_v^+]_+,\quad u_v=\beta_v^+[-d_v^-]_+ - \beta_v^-[d_v^-]_+`. Valid when: Valid when the fourth cumulant is certified nonpositive on the endpoint box and D_v is bounded by real incidence intervals.
- promotion-falsifier-test: `I_{\mathrm{tot}}=M_G+[T^-_{\mathrm{tail}},T^+_{\mathrm{tail}}]+c_{\mathrm{col}}\sum_v[\ell_v,u_v]`. Valid when: Gives a valid finite OS-block certificate after H,K are fixed and endpoint intervals control every remaining connected boundary-OPE term.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: regulated SU(N) Yang-Mills Wilson plaquette-sheet endpoint boxes B_v(a,ell) with heat-kernel action, gauge-invariant parallel-transported flux sources eta_{ij,v}, and connected source derivatives of log Z_{v,a,ell}.; target object: a certified interval for the post-H,K Schur-Feshbach null-channel endpoint contribution M_G+R_end in the locked reflected Wilson OS block.; Model: finite-volume hypercubic heat-kernel lattice regularization of pure SU(N) Yang-Mills with Wilson plaquette-sheet observables representing the fixed three-hairpin collar geometry..
- Conceptual pressure attacked: the last R/kappa4 obstruction must become sign-certifiable rather than remain a symbolic endpoint phrase.
- Start from the fixed post-H,K three-hairpin null channel; do not alter H,K, the Wilson block, or the reflection plane.
- Write the connected endpoint contribution as a source derivative of log Z_v in the heat-kernel plaquette-sheet regulator.
- Use connected logarithms to remove Wick-square Gram contractions; these are nonnegative and cannot be the falsifier in the null channel.
- Use the verified null incidence identity to cancel the straight nonabelian C_A f f contact along shared non-endpoint segments.
- Localize the surviving irreducible connected four-flux term to endpoint boxes; place overlapping boxes, corner leakage, and long-range remnants in T_tail.
- Insert the color/geometric factor c_col=(g_a^4/4)(T_F/N)^2 and contract with D_v=2G12-4G13-4G23.
- Because kappa4_v is negative to leading compact-group order, replace each product by a clipped interval: positive D_v is dangerous, negative D_v is protective.
- Add the positive Gaussian Schur-Feshbach margin M_G and tails to obtain I_tot.
- Hard gate: inf I_tot>0 promotes the same-theory OS finite-block transfer; sup I_tot<0 produces a finite Wilson falsifier. Neither outcome resolves continuum existence or the Hamiltonian mass gap.

Blocking gap: The branch still lacks actual same-theory numerical or analytic intervals for beta_v, D_v, and T_tail on the fixed endpoint geometry.

## Falsifiers

- A same-theory endpoint source computation gives sup I_tot<0; this is a finite Wilson OS falsifier for the post-H,K block.
- The heat-kernel endpoint fourth cumulant is not sign-stable or has a positive noncompact tail outside the beta interval.
- Endpoint boxes cannot be separated without changing the Wilson observable, so mixed endpoint cumulants are not controlled by T_tail.
- A boundary counterterm is required to define log Z_v source derivatives, violating the same-theory condition.
- The cutoff-uniform tail bound grows faster than the positive Gaussian margin M_G and demotes the interval certificate.

## Learning

Declarative tension: the same finite Wilson block must inherit OS positivity from collar reflection positivity, keep the identical gauge-invariant theory, and tolerate endpoint collapse; the missing mediator is a signed, cutoff-uniform representation of the connected endpoint boundary OPE. The old carrier, symbolic R or a raw kappa4 spectrum, is representation-limited: it hides incidence signs and makes negative compact-group kappa4 look automatically dangerous. Compared with a global Schur-preimage matrix test, the clipped endpoint interval carrier is more local and directly computable after H,K; compared with a formal OPE assertion, it has primitive operations: source differentiation, interval arithmetic, incidence contraction, color multiplication, and tail addition. Efficient representation requirements are now explicit: encode endpoint boxes, beta intervals, D_v incidence intervals, color factors, and tails; preserve same-theory Wilson normalization and null-channel cancellations; identify equivalent carriers only through equal regulated source derivatives; keep locality cost finite by charging all overlap to T_tail; export only the scalar interval I_tot to the OS transfer gate. Conceptual value signal: sharpness and route change. Negative kappa4 is not the obstruction; positive endpoint dominance plus uncontrolled tails is. Route next step: proof search plus endpoint-data computation, not forge-new abstraction and not quarantine.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and endpoint-interval calibration.`
- Rationale: The branch has already fixed H,K and reduced the obstruction to R/kappa4; another abstract OS restatement would loop. A concrete endpoint dominance experiment tests the only remaining sign mechanism.
- Situation seed: First three-hairpin reflected Wilson block on a finite heat-kernel SU(N) lattice, with endpoint boxes around each boundary hairpin endpoint and source derivatives of the local plaquette-sheet partition functions.
- Varied variable: Endpoint incidence asymmetry alpha_v=G_{12,v}/(G_{13,v}+G_{23,v}) while keeping beta_v and the regulator scale window fixed.
- Held-fixed controls: Gauge group SU(N), heat-kernel plaquette action, and Wilson plaquette-sheet normalization., The already computed H,K hairpin geometry and the Feshbach null vector., Same reflection plane, same gauge-invariant test algebra, and no boundary counterterm., Endpoint-box radius ell/a and the tail bookkeeping convention.
- Expected observation: For alpha_v below the positive-dominance threshold, negative compact-group kappa4 is protective or neutral; for alpha_v sufficiently above it, the clipped lower endpoint interval can cross zero and become a finite-block falsifier if tails do not compensate.
- Transfer certificate needed: A cutoff-uniform proof that the endpoint incidence table and finite-difference beta_v intervals are computed in the same regulated Yang-Mills measure and that T_tail bounds all omitted connected endpoint correlations.

## Next Experiment

Compute the endpoint incidence ledger for the fixed three-hairpin geometry: list each endpoint box v, its G12,G13,G23 intervals, D_v clipping sign, beta_v stencil inputs, and T_tail assignment; then evaluate inf and sup of I_tot.

# Endpoint-box R++ polarization interval certificate

## Candidate Lemma

For the fixed post-H,K plus hairpin endpoint box, the flowed Wilson covariance coefficient R_{++}^{ren} has a same-theory pair-plus-polarization decomposition. A rigorous sectorwise interval for Xi_{++} is a valid route-deciding certificate: its lower endpoint promotes the corrected second-order form if it beats the Schur-Feshbach leakage L_+, and its upper endpoint falsifies this endpoint repair if it cannot.

## Definitions

- source object: same-cutoff gradient-flow SU(N) lattice Yang-Mills expectations of two centered thin plus-hairpin Wilson observables inside the H,K endpoint box.
- target object: the finite fourth-order endpoint-box coefficient R_{++}^{ren} entering the corrected post-H,K Schur-Feshbach second-order form Q_+.
- controlled interface: boundary-OPE projection after heat-flow regulation, boundary point splitting, and perimeter/cusp subtraction, retaining only the plus-channel endpoint polarization.
- same-theory condition: the cutoff sequence, bare-coupling tuning, Wilson observables, H,K projection, and flow-window extrapolation all belong to one Yang-Mills theory and introduce no auxiliary Gaussian replacement.
- carrier observable: \widehat W_+(\Sigma;t_f,\epsilon) is the centered, perimeter-renormalized, cusp-renormalized flowed Wilson hairpin associated with the plus-channel sheet \Sigma.
- hard gate changed: this can decide the finite Route A endpoint-box positivity gate; it does not touch continuum existence, OS reconstruction, or the Hamiltonian mass-gap gate.

## Assumptions

- Model: pure Euclidean SU(N) Yang-Mills is represented first by Wilson lattice measures at spacing a, with Luescher gradient flow time t_f>0.
- Regime: endpoint-box hairpin area scale rho is small compared with the collar scale, while point splitting epsilon and lattice spacing a are removed under fixed positive flow time before the rho-coefficient is read.
- Uniformity: the H,K finite Schur-Feshbach normalization defining L_+ is held fixed while R_{++}^{ren} is extracted.
- Same-theory validity: all expectations, counterterms, and cumulants are computed on the same cutoff trajectory; no change of observable algebra or Gaussian comparison theory is allowed.
- Perturbative-control boundary: the displayed Xi_{++} formula is a one-loop flowed boundary-OPE coefficient with explicit remainder E_{2,++}; promotion requires an independent bound on that remainder.
- Non-claim: success gives a finite endpoint-box certificate only, not the Clay mass-gap theorem.

## Equations

- centered-flowed-hairpin: `\widehat W_+(\Sigma;t_f,\epsilon)=Z_{\rm cusp}^{-1}Z_{\rm per}^{-1}\left(W_+(\Sigma;t_f,\epsilon)-\langle W_+(\Sigma;t_f,\epsilon)\rangle\right)`. Valid when: Valid when the same flowed lattice measure defines the expectation, perimeter subtraction, and cusp subtraction before endpoint projection.
- renormalized-endpoint-coefficient: `R_{++}^{\rm ren}=\lim_{a\to0}\lim_{\epsilon\to0}\rho^{-4}\kappa_2(\widehat W_+(\Sigma_1),\widehat W_+(\Sigma_2))`. Valid when: Valid when the endpoint-box area scale rho is taken after fixed positive flow time and before the H,K projection limit.
- pair-polarization-split: `R_{++}^{\rm ren}=2(N^2-1)G_{++}+g_R^2N(N^2-1)G_{++}\Xi_{++}+E_{2,++}`. Valid when: Applies in the one-loop flowed boundary-OPE expansion with finite geometry factor G_{++} and controlled two-loop remainder E_{2,++}.
- sector-decomposition: `\Xi_{++}=I_{3g}+I_{4g}+I_{\rm ct}+I_{\rm end}`. Valid when: Valid after longitudinal Ward pieces and one-hairpin cusp counterterms are assigned in the same renormalization convention.
- interval-certificate: `\underline\Xi_{++}=\sum_s\underline I_s\le \Xi_{++}\le \sum_s\overline I_s=\overline\Xi_{++}`. Valid when: Valid when each sector integral is enclosed by rigorous interval arithmetic on the flowed compactified endpoint domain.
- promotion-inequality: `2(N^2-1)G_{++}\left(1+\frac{g_R^2N}{2}\underline\Xi_{++}\right)-|E_{2,++}|>L_+`. Valid when: Requires the H,K Schur-Feshbach leakage L_+ and the same endpoint-box normalization used in R_{++}^{ren}.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: same-cutoff gradient-flow SU(N) lattice Yang-Mills expectations of two centered thin plus-hairpin Wilson observables inside the H,K endpoint box.; target object: the finite fourth-order endpoint-box coefficient R_{++}^{ren} entering the corrected post-H,K Schur-Feshbach second-order form Q_+.; Model: pure Euclidean SU(N) Yang-Mills is represented first by Wilson lattice measures at spacing a, with Luescher gradient flow time t_f>0..
- Fix the H,K plus-channel endpoint geometry and encode each hairpin by a signed sheet current J^{mu nu}_Sigma plus endpoint current j_{partial Sigma}.
- Use the centered flowed Wilson observable so disconnected products and one-hairpin perimeter/cusp factors cancel before the covariance coefficient is extracted.
- Expand the two-hairpin covariance to fourth order in the endpoint-box area scale rho. The two cross-pair curvature contractions give the positive baseline 2(N^2-1)G_{++}.
- Collect the connected one-loop four-curvature terms into I_{3g}, I_{4g}, I_ct, and I_end. Their common color factor is N(N^2-1) under the chosen generator normalization.
- Apply the open-sheet Ward identity partial_mu J^{mu nu}=j^nu_{partial Sigma}. The longitudinal endpoint singularity is converted into the same local cusp structure subtracted from the one-hairpin observable.
- Compactify the remaining endpoint variables and express each sector as a dimensionless heat-kernel integral Phi_s(u;lambda,H,K,N).
- Define interval sums over cells, obtaining a mathematically checkable enclosure [underline Xi_{++}, overline Xi_{++}].
- Compare the lower and upper interval endpoints with the Schur-Feshbach leakage L_+ to promote or falsify the endpoint-box repair.

Blocking gap: The exact H,K geometry still needs certified interval evaluation of Phi_s and a same-window bound on E_{2,++}; no numerical sign or size certificate for Xi_{++} is claimed in this cycle.

## Falsifiers

- falsifier: the centered covariance retains an uncancelled cusp or endpoint divergence after the declared same-theory subtraction.
- falsifier: G_{++}=0 for the actual H,K plus geometry, making the positive pair baseline unavailable.
- falsifier: the certified upper bound on R_{++}^{ren} is below L_+ throughout the admissible flow window.
- falsifier: Xi_{++}(lambda) has no continuum-stable plateau as a->0 and epsilon->0 at fixed physical endpoint geometry.
- falsifier: the one-loop remainder bound |E_{2,++}| is larger than the promotion-demotion gap.
- falsifier: interval subdivision exposes a sign-changing endpoint cell whose width cannot be reduced without changing the carrier representation.

## Learning

Conceptual pressure attacked: the finite tangent-cone theorem gives an exact leakage L_+, but the Yang-Mills endpoint mediator R_{++} is still uncertified. The declarative tension is that same-theory Wilson positivity, gradient-flow renormalization, and Schur-Feshbach positivity must jointly hold, while the missing mediator is a sign/size certificate for Xi_{++}. The raw Wilson cumulant carrier was too fragmented; the refit to sheet currents, endpoint currents, sector kernels, and interval cells is more efficient and falsifiable. Compared with the older non-Gaussian OS witness route, this local route changes one hard gate only: finite endpoint-box positivity; continuum existence and the Hamiltonian mass gap remain untouched. Efficient representation requirements are now explicit: encode H,K sheets, preserve gauge/color/orientation invariants, use Ward cancellation and interval integration as primitives, identify equivalent sheets by currents, respect endpoint locality, transfer only through same-theory flowed cumulants, and demote on cusp, plateau, or interval-width falsifiers.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch has already reduced R to Xi_{++}; another abstract restatement would loop. A concrete flow-window endpoint-box experiment tests whether the same-theory cumulant can actually beat the finite Schur-Feshbach leakage.
- Situation seed: Pure SU(N) Wilson lattice Yang-Mills with Luescher gradient flow, two fixed H,K plus-hairpin endpoint sheets in one endpoint box, centered Wilson covariance, point splitting epsilon, and continuum extrapolation of R_{++}^{ren}.
- Varied variable: lambda=sqrt(8t_f)/d, the flow-radius to endpoint-separation ratio inside the admissible window lambda_min<=lambda<=lambda_max.
- Held-fixed controls: The same bare-coupling continuum trajectory and Wilson action are used for all hairpin cumulants., The H,K collar/hairpin geometry, plus-channel projection, and Schur-Feshbach leakage L_+ are held fixed., The disconnected-product, perimeter, and one-hairpin cusp subtractions are fixed before varying lambda., The endpoint-box area normalization rho^{-4} and color normalization tr(T^aT^b)=delta^{ab}/2 are held fixed.
- Expected observation: A valid endpoint repair should show a stable interval for Xi_{++}(lambda) whose lower endpoint makes R_{++}^{ren}>L_+ in some flow window. A persistent upper bound below L_+ is a route-demoting observation.
- Transfer certificate needed: Uniform a->0, epsilon->0, rho->0 error bounds, Ward-cusp cancellation in the same Wilson algebra, and an interval certificate for E_{2,++} before the observation can affect proof obligations.

## Next Experiment

Encode the actual H,K plus hairpin sheets as signed bivector currents, isolate the nearest-endpoint cells, and produce certified interval bounds for I_end and the longitudinal-cancelled part of I_3g at three flow ratios lambda.

# Post-H,K endpoint-box kappa_4 shell certificate for Wilson Route A

## Candidate Lemma

For a fixed finite post-H,K endpoint-box Wilson basis with heat-kernel flow time sigma, the dangerous connected boundary-OPE polarization term is bounded by a dyadic plaquette-sheet shell envelope. If m_G-g_R^4 D_sigma/(16N^2)-e_OPE,sigma-s_HK>0, then the Schur-corrected endpoint-box quadratic form is positive on this finite subspace. This changes only the finite Wilson positivity gate, not the OS/Wightman construction or the Clay mass gap theorem.

## Definitions

- source object: heat-kernel regulated SU(N) Wilson endpoint-box cumulants on the finite collar/hairpin basis, with flowed curvature sheets and connected vacuum expectation functional.
- target object: the finite corrected endpoint-box quadratic form R_sigma-S_HK on the already chosen post-H,K Wilson subspace, not the full YM Hamiltonian.
- controlled interface: compress the connected four-curvature Wilson cumulant to the endpoint-box coefficient matrix and compare its negative spectrum with the Gaussian Hadamard-square margin and Schur-Feshbach subtraction.
- same-theory condition: use the identical Wilson action or continuum candidate, gauge group, regulator sigma, renormalized coupling, observable basis, vacuum subtraction, and H,K Schur data; no change of theory or sector is allowed.
- endpoint sheet: a small oriented plaquette-sheet in an endpoint box, carrying an area weight, a parallel transporter to a reference point, and an SU(N) generator contraction.
- shell envelope: A_{4,sigma}(r) is a supremum bound for the transported connected four-curvature cumulant when the four sheet points have dyadic diameter or separation comparable to r.

## Assumptions

- Model/regime: finite lattice or UV-cutoff Euclidean SU(N) Yang-Mills with reflection-positive Wilson measure before any continuum passage.
- Regulator: all field-strength insertions are gauge-covariantly heat-kernel flowed at the same sigma and then parallel transported inside the same endpoint box convention.
- Uniformity: the endpoint-box family is finite, H,K and S_HK=B^*E^{-1}B have already been computed in the same Wilson basis, and the sigma/a ratio is fixed during the finite audit.
- Naturalness: vacuum and perimeter self-energy counterterms are removed only by normalizing the same Wilson loops, not by changing the action.
- OPE regime: endpoint boxes are separated from collar singularities by a fixed multiple of sqrt(sigma), so the OPE remainder e_OPE,sigma is a finite certified error.
- Non-claim: positivity here is a finite tangent-cone certificate and does not assert continuum existence, OS cyclicity, or a positive Hamiltonian mass gap.

## Equations

- flowed sheet curvature: `\Phi_{u,p}^{a}=\int_{\Sigma_{u,p}}K_{\sigma}(x_{u,p},y)\,U_{x_{u,p}\leftarrow y}^{ab}F_{\mu\nu}^{b}(y)n_{u,p}^{\mu\nu}(y)\,dA(y)`. Valid when: Applies in the heat-kernel regulated Wilson-sheet expansion before either sigma removal or continuum passage is attempted.
- connected four-curvature cumulant: `\Gamma_{4,\sigma}^{abcd}(i,j,k,l)=\langle\Phi_i^a\Phi_j^b\Phi_k^c\Phi_l^d\rangle-\sum_{\pi\in P_2(4)}\langle\Phi_{\pi_1}\Phi_{\pi_2}\rangle\langle\Phi_{\pi_3}\Phi_{\pi_4}\rangle`. Valid when: Valid when fluxes are vacuum-centered and the Gaussian pairings have already been assigned to R_G.
- compressed kappa4 endpoint matrix: `(\kappa_{4,\sigma})_{uv}=\sum_{p,q,r,s}G_u^{pq}G_v^{rs}\,\mathcal C_{abcd}^{pqrs}\,\Gamma_{4,\sigma}^{abcd}(u,p;u,q;v,r;v,s)`. Valid when: Requires the fixed endpoint-box geometry, SU(N) color contractions, and the same transported curvature convention for every sheet.
- dyadic shell domination: `(\kappa_{4,\sigma})_{uv}=\sum_{n\ge0}(\kappa_{4,\sigma}^{[n]})_{uv},\qquad |(\kappa_{4,\sigma}^{[n]})_{uv}|\le D_{uv,n}A_{4,\sigma}(2^n\sqrt{\sigma})`. Valid when: Valid when the four sheet positions are partitioned by dyadic diameter and the shell envelope bounds the connected cumulant there.
- negative spectrum row-shell bound: `M_{4,\sigma}^{-}\le \|\Pi_E\kappa_{4,\sigma}\Pi_E\|_{op}\le D_{\sigma}:=\max_u\sum_v\sum_nD_{uv,n}A_{4,\sigma}(2^n\sqrt{\sigma})`. Valid when: Requires the finite endpoint-box compression Pi_E and summable shell envelopes for the connected four-curvature kernel.
- corrected endpoint-box certificate: `\lambda_{\min}\Pi_E(R_{\sigma}-S_{HK})\Pi_E\ge m_G-\frac{g_R^4}{16N^2}D_{\sigma}-e_{OPE,\sigma}-s_{HK}`. Valid when: Applies after H,K are fixed and the Schur-Feshbach correction is computed in the same finite Wilson basis.

## Attempted Derivation

- Attack the conceptual pressure: finite Wilson positivity must separate calculable Gaussian endpoint polarization from uncomputed connected kappa_4 before any spectral transfer is meaningful.
- Expand normalized endpoint Wilson products using heat-kernel transported curvature sheets; the regulator is sigma and the observable is the same Wilson endpoint-box family.
- Use vacuum/perimeter normalization to cancel disconnected self terms; assign crossed two-curvature contractions to R_G with color factor alpha_N=(N^2-1)/(8N^2).
- Define kappa_{4,sigma} as the remaining connected four-curvature cumulant compressed by endpoint geometry and SU(N) trace contractions.
- Partition quadruples of sheet insertions into dyadic shells and bound each compressed entry by geometry counts D_{uv,n} times the kernel envelope A_{4,sigma}(2^n sqrt(sigma)).
- Use the finite row-sum/operator-norm bound to control the negative spectrum M_{4,sigma}^-; this is a falsifier-ready estimate, not a symbolic lambda model.
- Combine the bound with the already finite Schur-Feshbach correction S_HK and OPE error to get the endpoint certificate m_G-g_R^4D_sigma/(16N^2)-e_OPE,sigma-s_HK>0.

Blocking gap: The actual first H,K endpoint geometry and a rigorous or computed envelope A_{4,sigma}(r) for the connected four-curvature kernel are still missing. Without them D_sigma is a certificate template, not a numerical sign result.

## Falsifiers

- falsifier: for the first actual H,K endpoint basis, D_sigma g_R^4/(16N^2)+e_OPE,sigma+s_HK>=m_G, so the corrected endpoint-box form cannot be certified positive.
- The connected four-curvature shell envelope A_{4,sigma}(r) is non-summable or grows as sigma/a is held in the target regime.
- Heat-kernel smearing or chosen transport paths break the reflection-positive support needed for same-theory transfer.
- Perimeter or vacuum pieces fail to cancel in normalized Wilson cumulants at the required order.
- The Gaussian PSD margin m_G vanishes on the endpoint compression after actual color/geometric degeneracies are imposed.
- Different sheet-hypergraph encodings of gauge-equivalent endpoint boxes yield inequivalent kappa_4 matrices.

## Learning

Conceptual pressure attacked: the post-H,K route needs a mediator between finite Wilson cumulants and Schur-corrected positivity, not another OS density restatement. Declarative tension: same-theory Wilson/OPE data, finite Schur-Feshbach correction, and endpoint positivity must all hold, but the missing mediator was a locality-preserving representation of the connected kappa_4 term. The old scalar R carrier is too weak and representation-limited; the full OS observable-density carrier is too strong for this local gate. Compared with abstract transfer, the sheet-kernel hypergraph preserves color factors, sheet geometry, dyadic locality, connected-cumulant subtraction, and the H,K interface. Efficient representation requirements: encode sheets, weights, transporters, color tensors, shell labels, and Schur data; preserve gauge invariance, reflection support, Gaussian/kappa_4 separation, and endpoint compression; primitive operations are cumulant contraction, shelling, row-sum/operator bounds, and Schur subtraction; equivalence is by Wilson-invariant sheet symmetries and trace identities; locality budget is finite endpoint boxes with controlled sigma/a; transfer interface is only a finite R_sigma-S_HK certificate; falsifiers are margin failure, nonuniform envelopes, or representation non-invariance. Value signal: sharp and route-changing at finite scope because it turns the unknown R/kappa_4 obstruction into a computable shell-envelope sign test while preserving Clay target commitments.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch has already reduced R to Gaussian PSD plus connected kappa_4. Another abstract restatement would loop; the decisive information is whether the actual heat-kernel four-curvature cumulant shell envelope can exceed the finite Schur-corrected margin.
- Situation seed: Finite SU(N) lattice Yang-Mills on a reflection-symmetric box, with the first collar/hairpin endpoint boxes represented as heat-kernel flowed plaquette-sheets and the known H,K Schur subtraction inserted as a fixed matrix.
- Varied variable: flow-radius ratio rho=sqrt(sigma)/ell_endpoint while keeping the endpoint Wilson basis and renormalized coupling convention fixed.
- Held-fixed controls: Same Wilson action or continuum candidate, same gauge group SU(N), and same vacuum expectation functional., Same endpoint-box basis, H,K matrices, Schur-Feshbach subtraction S_HK, and vacuum/perimeter normalization., Same color normalization Tr(T^aT^b)=delta^{ab}/2 and same crossed-curvature Gaussian contribution R_G., Same finite volume reflection plane and boundary separation from the collar singularities.
- Expected observation: If shell-locality is strong, D_sigma decreases or stays below the margin window as rho is varied; if a short-distance connected kappa_4 spike dominates, the endpoint certificate fails before any Clay-level transfer is attempted.
- Transfer certificate needed: A uniform same-theory bound or computation of A_{4,sigma}(r), stable under lattice refinement and compatible with reflection positivity, plus explicit H,K endpoint geometry so D_sigma and the corrected lower bound are not representation artifacts.

## Next Experiment

Build the first sheet-hypergraph table for the concrete H,K collar/hairpin endpoint boxes: list sheets, orientation weights, SU(N) trace factors, dyadic shell counts D_{uv,n}, then evaluate the certified margin using any available same-theory bound for A_{4,sigma}(r).
