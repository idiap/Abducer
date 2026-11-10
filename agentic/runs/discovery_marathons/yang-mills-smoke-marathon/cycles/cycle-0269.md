# cycle-0269

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint-Incidence Clipping for the Post-H,K Wilson Gate

## Candidate Lemma

In the known three-hairpin post-H,K null channel, after heat-kernel plaquette-sheet endpoint localization and the valid Wick-square and straight f f cancellations, the connected endpoint four-flux contribution is controlled by the incidence scalar D_v=2G12(v)-4G13(v)-4G23(v). If each singlet endpoint fourth-cumulant interval is nonpositive, only boxes with D_v>0 can lower the finite Schur-Feshbach gate; mixed or 13/23 endpoint boxes are protective or neutral.

## Definitions

- source object: a regulated SU(N) heat-kernel plaquette-sheet endpoint box v with local source s coupled to the singlet null-channel Wilson flux X_v in the reflected three-hairpin collar block.
- target object: the scalar finite post-H,K Schur-Feshbach gate interval I_gate for this fixed reflected-Wilson OS block; it is not a continuum Yang-Mills construction or a mass-gap claim.
- controlled interface: the endpoint source carrier (G12(v),G13(v),G23(v), beta_v, tau_tail) maps regulated connected endpoint cumulants to the scalar gate interval without changing Wilson observables.
- same-theory condition: the same locked gauge-invariant Wilson loops, heat-kernel regulator, source normalization, color trace convention, and no boundary counterterm are used before collar collapse and in the endpoint-box limit.
- bridge/carrier: clipped endpoint incidence, retaining [D_v]_+ as the only dangerous multiplier when beta_v is certified nonpositive.

## Assumptions

- Model: finite three-hairpin reflected Wilson block in four-dimensional Euclidean SU(N) Yang-Mills with heat-kernel plaquette-sheet regulator at cutoff a.
- Regime: endpoint boxes are disjoint at scale epsilon(a), surround only collar endpoints/corners, and leave all straight shared-boundary pieces assigned to the previously canceled sector.
- Uniformity: source derivatives of log Z_v(s) up to order eight are bounded uniformly in the cutoff window used for the endpoint stencil.
- Same-theory condition: no boundary field, counterterm, changed Wilson-loop renormalization, or gauge-fixed observable replaces the locked gauge-invariant Wilson algebra.
- Cancellation assumption: connected log removes Wick-square disconnected contractions, and the straight C_A f f contact has zero null incidence in this hairpin block.
- Sign assumption for the clipping form: the certified interval for beta_v lies in [-b_v,0] after including the compact-group Haar-Jacobian contribution and the local regulator correction.

## Equations

- endpoint fourth cumulant: `\kappa_{4,v}^{\rm sing}=\left.\frac{d^4}{ds^4}\log Z_v(s)\right|_{s=0},\qquad \beta_v=\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2\kappa_{4,v}^{\rm sing}`. Valid when: Valid when the endpoint box partition function uses the same heat-kernel plaquette-sheet regulator and the source couples to the singlet null-channel flux.
- null incidence scalar: `D_v=2G_{12}(v)-4G_{13}(v)-4G_{23}(v),\qquad G_{ij}(v)\in\{0,1\}`. Valid when: Applies after the H,K null vector has contracted the three reflected-hairpin pair polarizations and all length-linear terms are removed.
- endpoint incidence table: `\begin{array}{c|cccccccc}(G_{12},G_{13},G_{23})&(0,0,0)&(1,0,0)&(0,1,0)&(0,0,1)&(1,1,0)&(1,0,1)&(0,1,1)&(1,1,1)\\ D_v&0&2&-4&-4&-2&-2&-8&-6\end{array}`. Valid when: Valid for disjoint endpoint boxes whose local source support is charged at most once by each pairwise Wilson contraction.
- endpoint gate interval: `\mathcal I_{\rm gate}=M_G+\sum_v D_v\,\beta_v+[-\tau_{\rm tail},\tau_{\rm tail}]`. Valid when: Requires endpoint localization of the connected boundary OPE and a uniform tail estimate for all non-box Wilson contractions.
- clipped promotion bound: `\beta_v\in[-b_v,0]\quad\Longrightarrow\quad \inf \mathcal I_{\rm gate}\ge M_G-\sum_v b_v[D_v]_+-\tau_{\rm tail}`. Valid when: Valid when certified endpoint fourth-cumulant intervals are nonpositive and the tail interval has been symmetrized conservatively.

## Attempted Derivation

- Attack conceptual pressure: endpoint collapse must become sign-certifiable while preserving the same Wilson theory and the finite collar OS positivity already obtained.
- Declarative tension: finite collar OS positivity, unchanged gauge-invariant Wilson observables, and singular connected endpoint OPE terms must jointly hold; raw R forgets incidence signs, while a raw kappa_4 spectrum is too strong because it treats protective endpoint boxes as dangerous.
- Use the heat-kernel plaquette-sheet endpoint source carrier. The connected log eliminates Wick-square disconnected pieces; the null incidence identity eliminates the straight C_A f f contact; remaining non-box effects are charged to tau_tail.
- Contract the post-H,K null channel before estimating spectra. Each endpoint box contributes by D_v=2G12-4G13-4G23, so the local sign problem reduces to the eight-entry incidence table.
- Insert beta_v in [-b_v,0]. Since beta_v is nonpositive, only D_v>0 lowers the gate; all D_v<=0 boxes can be ignored in a conservative lower bound or used as positive slack.
- The hard gate is the finite post-H,K reflected-Wilson OS transfer gate. Success, inf I_gate>0, promotes this finite block; failure, sup/inf interval crossing negative with valid same-theory data, gives a finite falsifier. The Clay gates of continuum construction, full OS/Wightman reconstruction, nontriviality, and mass gap remain untouched.
- Efficient representation requirements: encode endpoint boxes, G_ij incidence bits, seven-point source stencil values, beta intervals, color factors, and tail intervals; preserve Wilson normalization, null cancellations, cutoff uniformity, and same-theory observables; primitive operations are source differentiation, interval arithmetic, incidence contraction, clipping, and tail addition; equivalence means equality of regulated source data and incidence map; locality budget charges all residual overlap to tau_tail; transfer interface exports only I_gate.

Blocking gap: The actual hairpin endpoint geometry has not yet supplied the list of boxes with G_ij values, and the source intervals beta_v plus tau_tail are not numerically or analytically certified for the real cutoff family.

## Falsifiers

- A certified 12-only endpoint family with M_G-2\sum_{12-only}b_v-\tau_tail<0 gives a finite same-theory OS falsifier for the post-H,K block.
- A boundary counterterm or Wilson-loop renormalization inserted only at the reflection endpoint breaks the same-theory condition even if the clipped interval is positive.
- Endpoint boxes overlap so that G_ij is not a local 0/1 incidence variable and the residual cannot be bounded by tau_tail.
- The heat-kernel source log has an eighth-derivative bound growing too fast for the seven-point beta_v interval to be cutoff-uniform.
- A noncompact or gauge-fixed source calculation changes the singlet Wilson flux cumulant and is not valid for the locked gauge-invariant observable algebra.
- The previously used straight f f null-incidence cancellation fails for the actual endpoint-corner geometry, returning a bulk contact term not covered by the endpoint table.

## Learning

Cycle 269 attacks the conceptual pressure of endpoint-collapse sign certification in the same Wilson theory. The declarative tension is finite collar OS positivity plus unchanged gauge-invariant Wilson observables plus singular connected endpoint OPE. Raw R is representation-limited; a raw kappa_4 spectrum is too strong because it ignores null-channel incidence. Compared with a global Schur-preimage matrix test, the clipped endpoint carrier is local after H,K and directly computable from source derivatives. The conceptual value signal is sharpness: negative compact-group kappa_4 is not itself the falsifier; only certified positive 12-only endpoint dominance plus uncontrolled tail can demote the block. The hard gate changed is the finite post-H,K reflected-Wilson OS transfer gate, while all Clay-level continuum and mass-gap gates remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and promotion threshold for the finite post-H,K endpoint gate.`
- Rationale: The branch already has H,K and a corrected finite Schur-Feshbach form; another abstract OS restatement would loop. The remaining proof state is controlled by concrete endpoint incidence and source intervals.
- Situation seed: Use the fixed three-hairpin reflected Wilson block in the SU(N) heat-kernel plaquette-sheet regulator. Populate endpoint boxes by incidence type (12-only, 13-only, 23-only, mixed) and evaluate beta_v from seven source values of log Z_v.
- Varied variable: alpha=(sum_v b_v[D_v]_+ + tau_tail)/M_G, equivalently the certified 12-only endpoint dominance ratio.
- Held-fixed controls: Same locked gauge-invariant Wilson loops and same reflected collar/hairpin geometry after H,K., Same heat-kernel plaquette-sheet regulator, color normalization T_F/N, and singlet source coupling., Previously valid cancellations: connected Wick-square removal and straight C_A f f null-incidence cancellation., No boundary counterterm, no gauge-fixed replacement algebra, and no change of Wilson-loop renormalization at the reflection plane.
- Expected observation: For alpha<1 the endpoint interval promotes the finite block; for alpha>1 with a valid negative interval the block is demoted by a finite same-theory falsifier. Mixed endpoint dominance should increase slack rather than danger.
- Transfer certificate needed: A cutoff-uniform endpoint OPE with seven-point source derivative intervals, an exact incidence table for the actual hairpin geometry, and a tail bound charging every nonlocal or overlapping endpoint contraction.

## Next Experiment

Build the actual endpoint-box list for the three-hairpin geometry, assign each v its (G12,G13,G23), compute D_v and [D_v]_+, then pair it with seven-point heat-kernel source intervals for beta_v and a tail bound to certify the sign of I_gate.

# Cycle 269: Ward-subtracted endpoint-box R/kappa4 interval carrier

## Candidate Lemma

Endpoint Ward-subtracted interval enclosure: for the known H,K plus-channel hairpin sheets, the post-H,K endpoint mediator R_{++}^{ren} is a same-theory flowed Wilson covariance whose pair part is positive and whose connected polarization is a finite sector integral Xi_{++}; a certified lower interval for Xi_{++} gives a valid finite Schur-Feshbach endpoint-box test without implying YM existence or a mass gap.

## Definitions

- source object: finite-volume SU(N) Euclidean Yang-Mills with Wilson cutoff a, renormalized coupling g_R(mu), gradient-flow time tau>0, endpoint point-splitting rho, and the already extracted H,K hairpin sheet currents.
- target object: the finite endpoint-box Schur-Feshbach scalar Q_+^{box}=Q_+^{HK}+R_{++}^{ren}-L_+ controlling positivity of the known H,K compression with leakage L_+ fixed independently.
- controlled interface: the centered flowed Wilson hairpin covariance R_{++}^{ren}(a,tau,rho)=kappa_2(W_+^{ren},W_+^{ren}) inserted as the endpoint-box entry of the same finite matrix problem.
- same-theory condition: the cutoff sequence, Wilson action, gauge group, representation, flow map, renormalization prescription, H,K currents, and reflection structure are held fixed while a,rho,tau are sent through one admissible window.
- sheet current: J^+_{mu nu}(x)=sum_e sigma_e int_{Sigma_e^+} dS_{mu nu}(z) h_tau(x-z), with endpoint boxes retained as separate boundary currents.
- pair baseline: G_{++}=int J^+ Pi_tau J^+ J^+ Pi_tau J^+ is the positive cross-pairing geometry after reflection symmetrization.
- polarization ratio: Xi_{++}=C_{4,++}^{ren}/G_{++}, where C_{4,++}^{ren} is the connected four-curvature cumulant after Ward and cusp subtractions.

## Assumptions

- Model: SU(N) pure Yang-Mills on a torus or box with reflection-compatible Wilson cutoff and Osterwalder-Schrader positive finite-cutoff measure.
- Regime: a << rho << sqrt(8 tau) << d_box, where d_box is the endpoint-box separation scale and the H,K sheets are fixed smooth lattice approximants.
- Uniformity: heat-kernel majorants, Ward-subtracted sector kernels, and perturbative remainders are bounded independently of a in the admissible window.
- Renormalization: one-hairpin perimeter and cusp factors are divided out before forming the connected covariance, and the disconnected product is subtracted before the continuum-window estimate.
- Same-theory transfer: no replacement by a Gaussian model, strong-coupling surrogate, or changed observable algebra is permitted; every cumulant is evaluated in the same Wilson family used for H,K.
- Local non-claim: the lemma changes only finite endpoint-box positivity after H,K; continuum construction, OS/Wightman reconstruction, nontriviality, and Hamiltonian mass gap remain untouched.

## Equations

- flowed sheet current: `J^+_{\mu\nu}(x)=\sum_{e}\sigma_e\int_{\Sigma_e^+}dS_{\mu\nu}(z)\,h_\tau(x-z)`. Valid when: Valid when the H,K hairpin surfaces are fixed before the cutoff limit and the flowed curvature expansion is made at positive flow time.
- renormalized covariance carrier: `R_{++}^{ren}=\kappa_2\big(W_+^{ren},W_+^{ren}\big)`. Valid when: Valid when disconnected products, one-hairpin perimeter factors, and cusp counterterms have been removed in the same regulated Yang-Mills measure.
- pair-plus-polarization decomposition: `R_{++}^{ren}=\eta^4\{2(N^2-1)G_{++}+g_R^2N(N^2-1)\Xi_{++}\}+E_{g^4}`. Valid when: Applies for small endpoint sheets in the perturbative flowed window with fixed geometry and a uniform bound on the higher-order remainder.
- Ward-subtracted sector definition: `\Xi_{++}=I_{3g}^{T}+I_{4g}^{T}+I_{gh}^{T}+I_{ct}^{T}+I_{end}^{T}`. Valid when: Requires the BRST Ward combination of cubic, quartic, ghost, counterterm, and endpoint-current terms before interval integration is attempted.
- finite endpoint-box promotion inequality: `Q_+^{box}\ge Q_+^{HK}-L_+ +\eta^4G_{++}\big(2(N^2-1)+g_R^2N(N^2-1)\underline\Xi_{++}\big)-\overline E_{g^4}`. Valid when: Requires certified lower intervals for all Ward-subtracted sectors and a same-theory upper interval for the perturbative remainder.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: finite-volume SU(N) Euclidean Yang-Mills with Wilson cutoff a, renormalized coupling g_R(mu), gradient-flow time tau>0, endpoint point-splitting rho, and the already extracted H,K hairpin sheet currents.; target object: the finite endpoint-box Schur-Feshbach scalar Q_+^{box}=Q_+^{HK}+R_{++}^{ren}-L_+ controlling positivity of the known H,K compression with leakage L_+ fixed independently.; Model: SU(N) pure Yang-Mills on a torus or box with reflection-compatible Wilson cutoff and Osterwalder-Schrader positive finite-cutoff measure..
- Conceptual pressure attacked: finite Schur-Feshbach positivity needs a same-theory endpoint mediator, while positive pair covariance and gradient-flow renormalization alone do not control the connected four-curvature polarization.
- Declarative tension: OS positivity, flowed Wilson renormalization, and the finite tangent-cone theorem must jointly hold, but the missing mediator is a sign/size certificate for Xi_{++}.
- Replace raw Wilson contours, which are representation-limited and fragmented, by flowed sheet currents J plus endpoint currents B; this makes Ward cancellation and interval integration primitive operations.
- Expand the two centered renormalized hairpins through the four-curvature term. The disconnected product and one-hairpin perimeter/cusp factors cancel before taking the connected covariance.
- The Wick cross-pairing gives the positive baseline 2(N^2-1)G_{++}. This is the only sign-definite part available before evaluating the connected Yang-Mills polarization.
- Combine cubic-gluon, quartic-gluon, ghost, counterterm, and endpoint-current kernels using the BRST Ward identity. The resulting K_T is transverse away from endpoint cells and defines Xi_{++}.
- Partition endpoint boxes into reflection-identified cells. On each cell use flowed heat-kernel majorants and color/orientation signs to enclose I_{3g}^T, I_{4g}^T, I_{gh}^T, I_{ct}^T, and I_{end}^T.
- Insert the lower interval underline Xi_{++} and the uniform remainder bound into Q_+^{box}. Success promotes finite endpoint-box positivity after H,K; failure quarantines this R repair.

Blocking gap: The sector integrals have not yet been numerically or analytically enclosed with certified interval widths, and the O(g_R^4) flowed remainder still needs a same-theory bound in the window a << rho << sqrt(8 tau) << d_box.

## Falsifiers

- Cusp or endpoint divergences survive after the stated perimeter, cusp, Ward, and disconnected-product cancellations.
- The certified lower interval makes R_{++}^{ren}<L_+-Q_+^{HK}, demoting the endpoint-box repair.
- The positive geometry factor G_{++} vanishes because the extracted H,K endpoint sheets cancel by orientation or reflection symmetry.
- The Xi_{++} interval changes sign or size without a plateau as tau/d_box^2 varies inside the admissible flow window.
- The computation uses a Gaussian, strong-coupling, or changed-observable surrogate rather than the same Wilson family, violating the same-theory condition.
- Interval tails or roundoff dominate the pair baseline, leaving no valid decision after the refinement budget.

## Learning

The branch is not looping: the endpoint term is now a concrete same-theory cumulant with a computable Ward-subtracted polarization. Hard gate: finite endpoint-box positivity after H,K; success promotes this local gate, failure quarantines the R repair, and both leave continuum existence, OS/Wightman axioms, nontriviality, and positive Hamiltonian mass gap untouched. Conceptual value signal: sharp local route-change, because R_{++} is no longer symbolic but an interval-enclosable Yang-Mills input with regulator, color factors, cancellations, and a falsifier inequality. Carrier critique: raw Wilson contours are too fragmented; sheet currents plus endpoint currents preserve gauge/color/reflection/orientation invariants, support cumulant expansion, Ward subtraction, heat-kernel majorants, interval arithmetic, same-theory zero-pairing equivalence, endpoint locality, and transfer only through flowed Wilson cumulants. Compared route: a global non-Gaussian OS witness is too weakly targeted for this obstruction; finite interval-kernel proof search is the efficient abstraction.

## Gedanken Experiment Design Seed

- Need decision: `Design and use now as a falsifier probe for the endpoint-box R/kappa4 route.`
- Rationale: The branch has already identified the exact finite leakage L_+; another abstract restatement would loop. The concrete question is whether the same-theory flowed Wilson polarization Xi_{++} can be bounded strongly enough to alter the finite endpoint-box gate.
- Situation seed: A reflected SU(N) lattice Yang-Mills endpoint box containing the extracted plus-channel H,K hairpin sheets, represented by flowed sheet currents and endpoint currents, with R_{++}^{ren}=kappa_2(W_+^{ren},W_+^{ren}) measured or interval-enclosed on matched cells.
- Varied variable: u=sqrt(8 tau)/d_box, the dimensionless flow-radius to endpoint-box separation ratio.
- Held-fixed controls: Same Wilson action, gauge group SU(N), representation, reflection plane, H,K sheet geometry, and coupling trajectory., Same point-splitting hierarchy rho/sqrt(8 tau), same perimeter/cusp subtraction, and same disconnected-product subtraction., Same Schur-Feshbach leakage scalar L_+ and same finite plus-channel endpoint matrix entry being tested.
- Expected observation: A stable u-window should show G_{++}>0 and a narrow interval for Xi_{++}; promotion requires the certified lower bound to keep Q_+^{box} nonnegative, while a persistently negative or unstable interval is a route falsifier.
- Transfer certificate needed: Uniform convergence of the Ward-subtracted flowed cumulant and its interval enclosure as a,rho are refined, plus proof that the measured R_{++}^{ren} is the same finite endpoint entry used in the H,K Schur-Feshbach matrix.

## Next Experiment

Run proof search on the Ward-subtracted endpoint kernel: derive explicit formulas for I_{3g}^T, I_{4g}^T, I_{gh}^T, I_{ct}^T, and I_{end}^T in sheet-current coordinates, then produce the first certified interval for Xi_{++} over u=sqrt(8 tau)/d_box with all heat-kernel tails included.

# Post-H,K endpoint-box kappa4 interval certificate

## Candidate Lemma

Same-regulator endpoint-box interval lemma: for a finite reflected Wilson collar/hairpin endpoint family, the Schur-corrected endpoint polarization has the lower certificate Delta_sigma. If Delta_sigma>0, the finite Route A endpoint block passes the valid post-H,K positivity gate. If Delta_sigma<0 for a realized shell envelope, it is a falsifier for this Wilson collar/hairpin geometry. This changes only the finite endpoint-box gate, not OS reconstruction, continuum existence, or the Clay mass gap theorem.

## Definitions

- source object: A finite heat-kernel regulated SU(N) Yang-Mills cutoff measure on a reflected four-torus, with normalized fundamental Wilson loops supported by endpoint sheets S_i and smearing scale sigma.
- target object: The finite Hermitian endpoint-box matrix R_sigma-S_HK,sigma acting on the already selected collar/hairpin endpoint subspace after vacuum and perimeter normalization.
- controlled interface: The sheet-kernel hypergraph records sheets, weights, heat-kernel transporters, color contractions, locality shells, OPE errors, and Schur data, then transfers only the interval lower bound Delta_sigma.
- same-theory condition: The Wilson loops, heat-kernel smearing, coupling normalization, H,K Schur data, OPE subtraction, and kappa4 cumulant are all evaluated in the same cutoff Yang-Mills approximant before any continuum inference.
- bridge/carrier: The manipulated observable is the connected cumulant of two quadratic transported curvature fluxes Q_i,sigma and Q_j,sigma, compressed to the endpoint-box basis.

## Assumptions

- Model: finite-volume cutoff SU(N) Yang-Mills with reflection-positive heat-kernel smearing sigma>=c a and fundamental trace normalization tr(T^aT^b)=delta^{ab}/2.
- Regime: endpoint sheets have diameter O(sigma) and lie in the reflection-positive time half-space, with finite sheet number and finite shell radius L.
- Uniformity: the OPE remainder matrix obeys ||E_OPE,sigma||_op<=e_OPE,sigma in the same finite endpoint basis.
- Same-theory H,K: the Schur hairpin subtraction S_HK,sigma=B_sigma^*E_sigma^{-1}B_sigma is computed from the same Wilson variables and the same cutoff measure.
- Naturalness: shell envelopes Gamma_{ell,sigma} bound the actual connected four-curvature cumulant after quotienting only by Wilson trace identities and geometric symmetries preserving transporters.
- Non-claim: a positive Delta_sigma is only a finite Wilson calculation; it does not imply the Wightman axioms, a nontrivial continuum limit, or a Hamiltonian mass gap.

## Equations

- transported smeared flux: `\Phi_{i,\sigma}^a=\int_{S_i}\int h_\sigma(x-y)\,\chi_i(x)\,{\rm Ad}_{U_{x\to x_i}}^{ab}F_{\mu\nu}^b(y)\,dS_i^{\mu\nu}(x)\,dy`. Valid when: Valid when the heat-kernel smearing scale dominates the cutoff and the sheet transporter is fixed inside one endpoint box.
- quadratic Wilson flux variable: `Q_{i,\sigma}=-\frac{g_R^2}{4N}\sum_a \Phi_{i,\sigma}^a\Phi_{i,\sigma}^a`. Valid when: Applies after diagonal Wilson normalization and expansion through the quadratic curvature-flux term in the selected finite basis.
- two-flux covariance kernel: `C_{ij,\sigma}=\frac{1}{N^2-1}\sum_a \langle \Phi_{i,\sigma}^a\Phi_{j,\sigma}^a\rangle_{2,c}`. Valid when: Valid when color symmetry is unbroken and the two-point curvature covariance is evaluated in the same cutoff measure.
- connected four-flux cumulant: `\kappa_{4,ij,\sigma}=\sum_{a,b}\langle \Phi_{i,\sigma}^a\Phi_{i,\sigma}^a\Phi_{j,\sigma}^b\Phi_{j,\sigma}^b\rangle_c^{\rm conn}`. Valid when: Requires connected cumulant subtraction after all vacuum, perimeter, and disconnected two-two Wilson contractions have been removed.
- endpoint polarization decomposition: `R_{ij,\sigma}=\alpha_N g_R^4(C_\sigma\circ C_\sigma)_{ij}+\frac{g_R^4}{16N^2}\kappa_{4,ij,\sigma}+E^{\rm OPE}_{ij,\sigma},\qquad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid for the heat-kernel Wilson OPE through fourth flux order with the same regulator and fundamental SU(N) color normalization.
- shell negative-size bound: `M_{4,\sigma}^-\le \|\kappa_{4,\sigma}\|_{op}\le \max_i\sum_{\ell\le L} n_{i\ell}\Gamma_{\ell,\sigma}+\varepsilon_{{\rm tail},L}`. Valid when: Applies when the sheet-kernel hypergraph shell partition is invariant and each shell envelope bounds the actual compressed cumulant entries.
- Schur-corrected interval gate: `\Delta_\sigma=\alpha_N g_R^4\lambda_{\min}(C_\sigma\circ C_\sigma)-\frac{g_R^4}{16N^2}M_{4,\sigma}^- - e_{{\rm OPE},\sigma}-s_{HK,\sigma}`. Valid when: Valid after the H,K Schur subtraction, OPE error, and kappa4 shell bound are computed in the same finite cutoff theory.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Observable Density In The Excitation Sector; source object: A finite heat-kernel regulated SU(N) Yang-Mills cutoff measure on a reflected four-torus, with normalized fundamental Wilson loops supported by endpoint sheets S_i and smearing scale sigma.; target object: The finite Hermitian endpoint-box matrix R_sigma-S_HK,sigma acting on the already selected collar/hairpin endpoint subspace after vacuum and perimeter normalization.; Model: finite-volume cutoff SU(N) Yang-Mills with reflection-positive heat-kernel smearing sigma>=c a and fundamental trace normalization tr(T^aT^b)=delta^{ab}/2..
- Conceptual pressure attacked: the route needs a mediator from actual connected Wilson cumulants to Schur-corrected endpoint positivity, not another OS density restatement.
- Declarative tension: Wilson/OPE coefficients, connected kappa4 negativity, and S_HK must jointly hold in one cutoff theory; scalar R hides color/locality data, full OS density is circular for this local gate, and raw plaquette enumeration does not preserve cancellations compactly.
- Fix normalized Wilson observables \widehat W_i=W_i/\langle W_i\rangle-1 on the endpoint sheets, all in the same heat-kernel regulated cutoff theory.
- Use the nonabelian Stokes/OPE expansion through fourth flux order. Diagonal vacuum and perimeter terms cancel by normalization; this is the cancellation being used.
- The connected cumulant \langle Q_i Q_j\rangle_c splits into crossed two-flux contractions and the connected four-flux cumulant. The fundamental SU(N) color trace gives alpha_N=(N^2-1)/(8N^2).
- The two-flux covariance C_sigma is positive semidefinite; hence C_sigma o C_sigma is positive semidefinite by the Schur product theorem.
- Compress the dangerous connected cumulant kappa4_sigma by transporter-preserving locality shells. Gershgorin/operator norm gives M4^- <= max_i sum_ell n_iell Gamma_ell + tail.
- Subtract S_HK,sigma=B^*E^{-1}B from the same H,K Wilson collar/hairpin calculation to obtain the hard finite gate Delta_sigma.

Blocking gap: The first numerical endpoint certificate still needs the actual H,K geometry table, same-regulator shell envelopes Gamma_ell,sigma, and an OPE tail bound for the selected cutoff family.

## Falsifiers

- falsifier: A realized same-regulator shell envelope has M4^- >= 16N^2(alpha_N lambda_min(C o C)-e_OPE-s_HK)/g_R^4, forcing Delta_sigma<=0.
- falsifier: The heat-kernel regulator used for kappa4 is not the one used in H,K, so the same-theory condition fails.
- falsifier: Diagonal Wilson normalization leaves an uncancelled perimeter or vacuum term in R_sigma, invalidating the decomposition.
- falsifier: A shell quotient identifies two sheet kernels with different parallel transporter orderings or color tensors.
- Stress case: kappa4 has a coherent negative rank-one mode aligned with the smallest eigenvector of C_sigma o C_sigma, saturating the row-sum bound.

## Learning

The conceptual value signal is sharp and finite: R is no longer a symbolic endpoint parameter but a same-regulator connected Wilson cumulant with a PSD Gaussian color square plus one dangerous compressed kappa4 operator. The efficient carrier is the sheet-kernel hypergraph because it preserves color, locality, transporters, cumulant cancellations, OPE errors, and Schur data, while scalar R is too weak, OS density is too strong, and raw plaquette enumeration is fragmented. This is novel only at finite Route A scope: it unifies Wilson OPE, kappa4 negativity, and Schur-Feshbach correction into one falsifier-ready interval without implying the full Yang-Mills mass gap theorem.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and certificate rehearsal.`
- Rationale: The branch has repeated the abstraction enough; the next valid learning comes from testing whether kappa4 can overwhelm the PSD Gaussian square after the fixed Schur subtraction.
- Situation seed: Heat-kernel regulated SU(N) Yang-Mills on a reflected four-torus with the first collar/hairpin endpoint-box Wilson sheets, normalized by the same vacuum/perimeter factors and compressed to the post-H,K endpoint basis.
- Varied variable: rho=sigma/a, the heat-kernel smearing length in cutoff units, varied over a small finite grid while the endpoint geometry is fixed.
- Held-fixed controls: Gauge group SU(N), fundamental trace normalization, and renormalized coupling convention g_R., The endpoint Wilson sheet family, reflection plane, H,K Schur data, and endpoint compression basis., The OPE truncation order, diagonal normalization rule, and transporter-preserving shell equivalence policy.
- Expected observation: If increasing rho suppresses the negative shell envelope faster than it suppresses lambda_min(C o C), Delta_sigma becomes positive on an interval; if not, the endpoint-box route is likely demoted for this geometry.
- Transfer certificate needed: A same-regulator table of C_sigma, Gamma_ell,sigma, e_OPE,sigma, and S_HK,sigma with interval arithmetic proving the sign of Delta_sigma before any intuition enters proof obligations.

## Next Experiment

Extract the first collar/hairpin endpoint sheets, compute the heat-kernel covariance C_sigma and shell multiplicities n_iell, then bound Gamma_ell,sigma and evaluate Delta_sigma over rho=sigma/a with certified same-regulator intervals.
