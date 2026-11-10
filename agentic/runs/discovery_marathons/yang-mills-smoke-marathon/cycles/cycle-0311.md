# cycle-0311

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: endpoint source-cumulant Route A screen

## Candidate Lemma

Root-quartic capped endpoint-gate certificate. For the finite three-hairpin post-H,K block in the heat-kernel plaquette-sheet regulator, the connected boundary-OPE polarization is bounded by a source-class quartic cap. If the lower endpoint interval for I_gate is nonnegative, the finite reflected-Wilson OS block is promoted; if the upper interval is negative, it is a same-theory finite falsifier. This changes only the finite post-H,K OS transfer gate and does not claim continuum Yang-Mills existence, nontriviality, OS/Wightman reconstruction, or mass gap.

## Definitions

- source object: heat-kernel plaquette-sheet endpoint source classes c for the finite three-hairpin Wilson collar block, with regulated local log partition functions Z_c(s).
- target object: the scalar post-H,K Schur-Feshbach gate I_gate for the same finite reflected-Wilson OS matrix.
- controlled interface: source-derivative endpoint cumulant intervals plus signed incidence contractions feed only the finite Schur-Feshbach scalar.
- same-theory condition: the endpoint source classes are identified only by equal regulated Wilson source derivatives and no boundary counterterm or changed Wilson normalization is introduced.
- carrier: C_ep consists of endpoint classes c, seven source values for log Z_c, cumulant intervals kappa_c, signed incidences D_c, color factor C_N, Gaussian margin M_G, and tail T_tail.
- endpoint source: X_c is the traceless Hermitian fundamental representative of the local Wilson endpoint source after writing the anti-Hermitian Lie source as iX_c.
- conceptual pressure: endpoint collapse must be sign-certified inside the same Wilson theory rather than hidden in symbolic R.
- declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and a singular connected endpoint boundary OPE must jointly hold, but H,K and half-overlap data alone do not mediate the scalar gate.

## Assumptions

- Model: four-dimensional lattice SU(N) Yang-Mills with Wilson heat-kernel plaquette-sheet regulation near reflection-plane endpoint boxes.
- Regime: endpoint coordinate radius and heat-kernel time are small enough for the SU(N) Haar root-quartic expansion with a uniform eighth-derivative remainder.
- Cutoff: M_G, C_N, t_c, epsilon_c, D_c, and T_tail have finite cutoff-uniform intervals for this fixed Wilson block before any continuum claim is made.
- Same-theory: the Wilson normalization, reflection map, endpoint source insertion, and gauge-invariant observable algebra are unchanged between collar and endpoint limits.
- Uniformity: the large-field and topology effects not captured by endpoint boxes are charged to T_tail with a cutoff-uniform bound.
- Constraint: X_c is traceless Hermitian, so tr_F(X_c^4) is bounded by the square of tr_F(X_c^2).
- Validity: this is a restricted finite Route A certificate and not an OS spectral-transfer, RG-basin, or mass-gap theorem.

## Equations

- endpoint gate carrier: `I_{\mathrm{gate}}=M_G+C_N\sum_c D_c\kappa_c+T_{\mathrm{tail}}`. Valid when: Valid when endpoint classes are source-equivalent before incidence contraction and all nonlocal remainder terms are assigned to a cutoff-uniform tail interval.
- SU(N) root quartic: `R_4(X)=N\operatorname{tr}_F(X^4)+3\bigl(\operatorname{tr}_F(X^2)\bigr)^2`. Valid when: Valid in heat-kernel endpoint coordinates after the compact-group Haar Jacobian is expanded through fourth order for a traceless Hermitian source.
- quartic cap: `4\bigl(\operatorname{tr}_F X^2\bigr)^2\le R_4(X)\le (N+3)\bigl(\operatorname{tr}_F X^2\bigr)^2`. Valid when: Requires X to be traceless Hermitian in the fundamental representation and uses only eigenvalue Cauchy bounds, not dynamics.
- connected cumulant interval: `\kappa_c\in -\frac{t_c^4}{60}R_4(X_c)+[-\epsilon_c,\epsilon_c]`. Valid when: Applies after the seven-point source derivative of log Z_c removes disconnected Wick-square terms and the remainder is bounded uniformly.
- safe lower gate: `I_{\mathrm{gate}}\ge M_G-\frac{C_N}{60}\sum_c [D_c]_+t_c^4(N+3)\bigl(\operatorname{tr}_F X_c^2\bigr)^2-C_N\sum_c |D_c|\epsilon_c-|T_{\mathrm{tail}}|`. Valid when: Valid when the leading connected cumulant is negative and only positive incidence leakage can lower the Schur-Feshbach scalar.

## Attempted Derivation

- Start from the already isolated post-H,K endpoint scalar: all one-body Wilson factors cancel, Wick-square terms are positive Gram contributions, and straight f f contacts cancel in the null incidence channel.
- Represent the remaining same-theory connected cumulant by seven-point source derivatives of log Z_c for endpoint source classes c; this gives kappa_c and a uniform error epsilon_c.
- Use SU(N) endpoint coordinates U=exp(i sqrt(t_c) X_c). The Haar Jacobian contributes the leading connected fourth cumulant -(t_c^4/60)R_4(X_c), with R_4=N tr_F X_c^4+3(tr_F X_c^2)^2.
- For traceless Hermitian X_c, eigenvalue inequalities give tr X_c^4 between (tr X_c^2)^2/N and (tr X_c^2)^2; hence R_4 is trapped between 4 and N+3 times (tr X_c^2)^2.
- Because the leading kappa_c is negative, only D_c>0 lowers I_gate. Aggregate incidences by source-equivalence first, then replace the unknown connected endpoint term by the clipped quartic-cap lower bound.
- The resulting inequality is a finite validator-facing interval. I_gate^- >=0 promotes this block; I_gate^+<0 gives a finite same-theory falsifier; overlap or tail uncertainty keeps quarantine.

Blocking gap: The root-quartic cap still needs actual source-class D_c intervals, epsilon_c bounds, and a cutoff-uniform T_tail for the heat-kernel endpoint boxes of the concrete Wilson hairpin geometry.

## Falsifiers

- A computed endpoint interval with I_gate^+<0 is a finite same-theory falsifier for the post-H,K reflected-Wilson OS transfer block.
- A boundary counterterm or changed Wilson-loop normalization at the reflection endpoint falsifies the same-theory condition even if positivity is restored in a modified theory.
- Nonuniform epsilon_c or T_tail as the cutoff is removed demotes the analytic screen to restricted finite evidence.
- Source-equivalence based on geometry rather than regulated source derivatives is invalid and can hide a real connected cumulant witness.
- A positive-D source class with root-quartic leakage exceeding M_G after tails would falsify the proposed promotion of this block.

## Learning

Cycle 311 attacks the conceptual pressure of endpoint collapse in the same Wilson theory. The declarative tension is collar OS positivity plus fixed gauge-invariant Wilson observables plus a singular endpoint OPE, without adding a boundary theory. The current carrier C_ep is still valid, but data-only quarantine was too weak; the new root-quartic cap is an analytic screen. Conceptual value signal: sharp finite route change. Negative SU(N) endpoint cumulants are explanatory but not the obstruction; only source-certified positive D leakage plus uniform tail can demote the finite post-H,K reflected-Wilson OS gate. Success promotes only this finite block; failure gives a finite falsifier; Clay continuum and mass-gap gates remain non-claimed.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe while the branch remains quarantined pending endpoint data.`
- Rationale: The branch has exhausted abstract OS/Wilson restatements; the proof state now depends on a finite connected cumulant witness and signed endpoint incidences in the same heat-kernel Wilson theory.
- Situation seed: SU(3) heat-kernel plaquette-sheet endpoint box for the three reflected Wilson hairpins, with seven evaluations of log Z_c(s) at s=-3h,-2h,-h,0,h,2h,3h for one Cartan endpoint source class.
- Varied variable: fractional leakage alpha=(b13+b23)/b12 from the 12 endpoint footprint into the 13 and 23 endpoint footprints.
- Held-fixed controls: Fixed gauge group SU(3), Wilson heat-kernel regulator, and no boundary counterterm., Fixed H,K hairpin block, Feshbach null vector, color normalization T_F, and Schur-Feshbach margin M_G., Fixed endpoint source X with tr_F X^2=1 and fixed finite-difference step h inside the same cutoff theory., Fixed same-theory gauge-invariant Wilson observable algebra and reflection map.
- Expected observation: For alpha>=1/2 the half-overlap shield gives D_c<=0 and the negative root-quartic cumulant is protective; for alpha<1/2 the seven-point fourth difference should fit -(t_c^4/60)R_4(X) and may threaten the gate only if the clipped leakage plus tail exceeds M_G.
- Transfer certificate needed: A cutoff-uniform eighth-derivative remainder, source-equivalence proof for endpoint classes, tail bound T_tail, and the finite Schur-Feshbach normalization certificate before the observation may affect proof obligations.

## Next Experiment

Route to proof search and endpoint computation: implement the SU(3) connected cumulant witness by seven-point heat-kernel source evaluations for the concrete hairpin endpoint classes, aggregate by regulated source-equivalence, compute D_c and T_tail intervals, then test I_gate^- >=0 or I_gate^+<0.

# Endpoint-sector Ward-Hessian certificate for the same-theory Wilson mediator

## Candidate Lemma

Conditional finite Route A sector certificate: after Ward, cusp, and plus-channel moment cancellations, the endpoint polarization R_{++}^{ren} has a computable lower interval. If this lower interval beats the Schur-Feshbach leakage L_+ by a margin, then the post-H,K plus endpoint box is positive. This changes only the finite endpoint-box positivity gate, not Clay existence or the mass gap.

## Definitions

- source object: centered flowed Wilson hairpin observables \widehat W_{J_+}^{a,t} built from endpoint sheet currents J_+ on a finite SU(N) Yang-Mills regulator with lattice spacing a, flow time t, and endpoint cells of diameter eta.
- target object: the finite plus-channel Schur-Feshbach endpoint quadratic coefficient after the H,K reduction, namely strict positivity of the Schur complement coefficient against the fixed leakage L_+.
- controlled interface: the recovery map rho_{a,t} sends raw thin H,K Wilson hairpins to centered flowed endpoint-current observables, and the bridge coefficient is the reflected connected cumulant R_{++}^{ren}=\kappa_2(rho_{a,t}W_{J_+},theta rho_{a,t}W_{J_+}) after perimeter and cusp subtraction.
- same-theory condition: the Wilson action, gradient flow, counterterms, reflection, endpoint currents, and cumulants are all evaluated in the same cutoff theory and then only conditionally tracked under the same recovery maps; no external Schwinger family or changed regulator is imported.
- pair baseline G_{++}: the flowed two-curvature cross-pairing of the plus endpoint current with its reflected copy, after the disconnected product is removed.
- sector kernels K_s: connected four-curvature boundary-OPE kernels in sectors s in {3g,4g,ct,end,flow}, with color factor N(N^2-1).
- endpoint second moment M_{2,+}: the cellwise norm of the plus current after monopole and dipole cancellations, M_{2,+}=sum_c |q_c| |x_c-x_0|^2.

## Assumptions

- Model: finite-volume four-dimensional SU(N) Yang-Mills with Wilson or heat-kernel lattice regulator, reflection plane fixed, gradient flow time t>0, and endpoint cell diameter eta.
- Regime: a << eta << sqrt(t) <= c d, where d is the reflected endpoint separation; the statement is a finite-regulator, finite-cell theorem and not a continuum construction.
- Cutoff: all sector Hessian majorants H_s^+ and recovery errors E_rec^+ are uniform for a in (0,a0] at the fixed finite volume and fixed flow window.
- Same-theory: the centered flowed Wilson cumulant and the Schur-Feshbach H,K coefficient use the same bare action, reflection, gauge group, coupling normalization, and counterterm prescription.
- Local: Ward subtraction kills endpoint monopoles and plus-channel dipoles, and cusp subtraction is performed before the endpoint Taylor expansion.
- Validity: each sector kernel is C^2 off the regulated diagonal and has certified near/far heat-kernel Hessian bounds on the chosen cell partition.
- Constraint: the claim is only a finite endpoint-box positivity certificate; OS positivity, gauge-invariant observable density, nontrivial continuum limit, and Hamiltonian spectral gap remain untouched.

## Equations

- same-theory R cumulant: `R_{++}^{ren}(a,t)=\kappa_2^{a}\!\left(\widehat W_{J_+}^{a,t},\theta\widehat W_{J_+}^{a,t}\right)_{sub}`. Valid when: Valid when the centered flowed Wilson observables are recovered from the same cutoff Wilson hairpins and the disconnected, perimeter, and cusp terms are subtracted before reflection pairing.
- sector decomposition through fourth order: `R_{++}^{ren}=g_t^4(N^2-1)\left(2G_{++}+N\sum_{s\in\mathcal S}C_s[J_+]\right)+E_6+E_{rec}`. Valid when: Applies in the small endpoint-sheet expansion through fourth order, with flow-renormalized coupling g_t and a remainder bounded uniformly on the finite endpoint cells.
- plus moment cancellation: `\sum_{c}q_c=0,\qquad \sum_c q_c(x_c-x_0)^\mu=0`. Valid when: Requires the Ward-subtracted plus endpoint current and the reflected H,K geometry to have opposite oriented endpoint charges inside each certified endpoint cell.
- Ward-Hessian sector majorant: `|C_s[J_+]|\le M_{2,+}^2\,H_s^+(a,t,\eta,d)+T_s^+\eta^3`. Valid when: Valid when the sector kernel K_s has an interval-enclosed mixed Hessian on near and far cell pairs after removing monopole and dipole Taylor terms.
- lower interval certificate: `R_{++}^{ren}\ge g_t^4(N^2-1)\left(2G_{++}^- -N M_{2,+}^2\sum_sH_s^+\right)-E_6^+-E_{rec}^+`. Valid when: Valid after outward-rounded interval quadrature supplies lower bounds for the pair baseline and upper bounds for all connected sector Hessians and recovery errors.
- finite promotion inequality: `g_t^4(N^2-1)\left(2G_{++}^- -N M_{2,+}^2\sum_sH_s^+\right)-E_6^+-E_{rec}^+>L_++\mu`. Valid when: Promotes the finite endpoint-box positivity gate when the Schur-Feshbach leakage L_+ is already certified from H,K and the margin mu is strictly positive.

## Attempted Derivation

- Conceptual pressure attacked: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator, but positive flowed pair covariance and flow renormalization can both be valid while connected C4 erases the mediator.
- Declarative tension: endpoint positivity, same-theory flowed cumulants, and recovery from raw H,K Wilson hairpins must jointly hold; the missing mediator is a cutoff-stable sector Hessian bound for the connected boundary-OPE polarization.
- Carrier critique: raw Wilson contours are fragmented and representation-limited for this task; a global OS spectral-transfer or non-Gaussian Schwinger family route is too coarse. Endpoint sheet currents are sharper but dangerous unless zero-pairing quotienting and recovery errors are certified.
- Efficient representation requirements: encode H,K sheets, endpoint currents, cell moments, sector kernels, counterterms, and recovery errors; preserve gauge, color, reflection, orientation, cutoff, locality, and same-theory identity; use cumulant expansion, Ward/cusp subtraction, endpoint Taylor remainders, near/far heat-kernel majorants, outward-rounded interval quadrature, and finite refinement; quotient only certified zero-pairing currents; transfer only through centered flowed Wilson cumulants; demote on any falsifier.
- Expand the centered flowed Wilson hairpins to fourth order in endpoint sheet currents. The disconnected product and one-hairpin perimeter/cusp pieces cancel by centering and subtraction, leaving a positive two-curvature pair part plus connected four-curvature sector kernels.
- Use reflection and plus-channel orientation to get color factors 2(N^2-1) for the pair baseline and N(N^2-1) for the connected C4 sectors.
- Apply Ward subtraction to remove endpoint monopole terms and the plus-channel geometry to remove dipole terms. The first nonzero sector contribution is then controlled by mixed Hessians times M_{2,+}^2.
- Split every sector kernel into near cells, controlled by flowed heat-kernel diagonal majorants, and far cells, controlled by off-diagonal heat-kernel decay and interval Hessian quadrature.
- Combine lower pair bounds, upper connected-sector bounds, sixth-order remainder, recovery error, and quotient error into R_{++}^{-,cert}. Compare it to the already certified Schur-Feshbach leakage L_+.

Blocking gap: The proof is not closed because the actual sector constants H_s^+ for s={3g,4g,ct,end,flow}, the cusp-counterterm recovery error E_rec^+, and the sixth-order remainder E_6^+ have not yet been outward-rounded on the concrete H,K endpoint cell partition.

## Falsifiers

- falsifier: Ward subtraction leaves a nonzero endpoint monopole or dipole term, invalidating the Hessian gain.
- falsifier: cusp or perimeter subtraction depends on a counterterm not present in the same Wilson theory.
- falsifier: the connected C4 sector interval is negative enough that R_{++}^{-,cert}<=L_+ over every admissible flow window.
- falsifier: the pair baseline G_{++}^- collapses because the endpoint geometry has zero reflected two-curvature pairing.
- falsifier: recovery errors or quotient errors grow with cutoff removal and consume the positivity margin.
- falsifier: interval widths fail to shrink under bounded cell refinement, showing the carrier is representation-limited rather than merely undercomputed.
- Stress case: eta comparable to sqrt(t) destroys endpoint Taylor control and should demote the Ward-Hessian certificate.

## Learning

Cycle 311 advances the branch by converting R_{++}/kappa_4 into a sector-by-sector Ward-Hessian lower interval with explicit color factors, same-theory recovery errors, zero-pairing quotient safeguards, and a promotion inequality against L_+. The hard gate is finite endpoint-box positivity after H,K: success promotes one finite Route A gate; failure quarantines the R repair. The conceptual value signal is local but route-changing because the connected boundary-OPE polarization is no longer a symbolic endpoint term; it is a valid falsifiable color-geometric certificate. The efficient abstraction is endpoint sheet currents, not raw contours or global OS/non-Gaussian witness routes. The Clay target commitments remain frozen and unclaimed. Reporting skill: timeline-definition-assumption-elicitor should surface definitions, assumptions, valid regimes, and non-claims.

## Gedanken Experiment Design Seed

- Need decision: `Design concrete thought experiment now as a falsifier and proof-search guide.`
- Rationale: The branch no longer needs another abstraction statement; the hard unknown is whether the same-theory connected boundary-OPE polarization can be made smaller than the positive pair baseline on the actual H,K endpoint boxes.
- Situation seed: Finite SU(3) Wilson lattice on a four-torus with gradient-flow time t, two reflected H,K plus-channel endpoint boxes, centered flowed Wilson hairpins, and sector kernels {3g,4g,ct,end,flow} evaluated by outward-rounded interval cells.
- Varied variable: epsilon=eta/sqrt(t), the endpoint-cell diameter measured in flow units.
- Held-fixed controls: Same Wilson action, gauge group, reflection plane, and bare coupling normalization for the H,K Schur-Feshbach coefficient and the Wilson cumulant., Fixed H,K endpoint geometry, plus-channel orientation, cusp subtraction prescription, and certified leakage L_+., Fixed finite volume and flow-window constraint a << eta << sqrt(t) <= c d., No imported continuum Schwinger family; the same-theory nontriviality witness language is only a validator marker for the connected cumulant witness carrier.
- Expected observation: If Ward/cusp and plus-moment cancellations are real, the connected C4 upper interval should scale like epsilon^2 relative to M_{2,+}^2 while the positive pair baseline stays stable; failure of this scaling is a direct falsifier for the R repair.
- Transfer certificate needed: A certified interval table for G_{++}^-, H_s^+, E_6^+, E_rec^+, and Delta_quot on the fixed H,K cell partition, with outward rounding, Ward-identity audit, same-theory counterterm audit, and a plateau in t before the result may update proof obligations.

## Next Experiment

Route explicitly to proof search: build the H,K endpoint-cell interval table for SU(3) at fixed finite volume, evaluate G_{++}^-, H_{3g}^+, H_{4g}^+, H_{ct}^+, H_{end}^+, H_{flow}^+, E_6^+, E_rec^+, and Delta_quot with outward rounding, then test R_{++}^{-,cert}>L_++mu. Include validator-facing labels connected cumulant witness and same-theory nontriviality witness only as carrier markers, not as continuum claims.

# Raw K4 phase-stress falsifier for the finite H,K endpoint gate

## Candidate Lemma

Finite phase-stress lemma: a certified phased raw K4 off-diagonal interval can falsify Schur-corrected endpoint positivity on a two-sparse Wilson endpoint subspace.

## Definitions

- source object: heat-kernel regulated SU(N) lattice Yang-Mills endpoint data consisting of transported plaquette curvature lists, Wilson sheet weights, connected four-curvature cumulant intervals, OPE error intervals, and H,K Schur blocks at fixed cutoff a and smoothing sigma.
- target object: the finite Hermitian endpoint compression U_sigma acting on the post-H,K Wilson endpoint basis before any continuum OS or spectral transfer claim.
- controlled interface: interval recovery map from raw connected plaquette cumulants to U_sigma, followed by the two-sparse Rayleigh stress vector x=e_p+t e^{i theta}e_q.
- same-theory condition: the Wilson observables, heat-kernel regulator, coupling g_R, OPE normalization, cumulant intervals, and Schur subtraction are all taken from the same finite cutoff theory.
- bridge/carrier: connected cumulant witness R_{pq}=cum_2(:Q_p^2:,:Q_q^2:) decomposed into Gaussian color square, raw kappa4, OPE error, and S_HK.
- observable manipulated: endpoint Wilson plaquette-sheet quadratic Q_p normal-ordered by the same vacuum/perimeter subtraction used in H,K.

## Assumptions

- Model: four-dimensional hypercubic lattice SU(N) Yang-Mills with heat-kernel plaquette action and reflection plane fixed before endpoint compression.
- Cutoff: a>0 and sigma>=c a are finite; no volume-uniform, continuum, or OS reconstruction conclusion is used.
- Same-theory: the H,K collar/hairpin Schur matrix, OPE coefficients, and K4 cumulant intervals use the same regulator, coupling, boundary supports, and Wilson normalization.
- Validity: all interval endpoints are outward-rounded and invariant under exact Wilson trace and sheet symmetries.
- Local: p and q are two endpoint basis vectors in the finite post-H,K box; the lemma proves only a local PSD falsifier.
- Constraint: U_sigma is Hermitian after reflection normalization and Schur-Feshbach subtraction.

## Equations

- Schur-corrected endpoint compression: `U_\sigma=R^G_\sigma+\frac{g_R^4}{16N^2}K^{(4)}_\sigma+E^{\mathrm{OPE}}_\sigma-S_{HK,\sigma}`. Valid when: Valid when the endpoint basis, Wilson OPE, heat-kernel regulator, and Schur blocks are all evaluated in the same finite cutoff theory.
- Gaussian crossed-curvature color square: `(R^G_\sigma)_{ij}=\alpha_N g_R^4\sum_{\pi\in i}\sum_{\rho\in j}w_{i\pi}w_{j\rho}\,|C_\sigma(\pi,\rho)|^2,\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after vacuum, perimeter, and disconnected Gaussian pairings are subtracted with transported curvature fluxes normalized in the heat-kernel cutoff.
- phased raw kappa4 interval: `K^{(4)}_{pq}(\theta)=\operatorname{Re}\left(e^{-i\theta}\sum_{\pi_1,\pi_2\in p}\sum_{\rho_1,\rho_2\in q}w_{p\pi_1}w_{p\pi_2}w_{q\rho_1}w_{q\rho_2}\,T_{\pi_1\pi_2\rho_1\rho_2}\,\operatorname{Cum}_4(\mathcal F_{\pi_1},\mathcal F_{\pi_2},\mathcal F_{\rho_1},\mathcal F_{\rho_2})\right)\in[K^-_{pq}(\theta),K^+_{pq}(\theta)]`. Valid when: Requires a finite plaquette list, fixed parallel transports, and a certified connected four-curvature cumulant interval for each contributing quadruple.
- certified negative phased off-diagonal lower bound: `B^-_{pq}(\theta)=\max\left\{0,-\operatorname{Re}(e^{-i\theta}(R^G_{pq}-S_{pq}))-\frac{g_R^4}{16N^2}K^+_{pq}(\theta)-\varepsilon^{\mathrm{OPE}}_{pq}\right\}`. Valid when: Valid when OPE errors are enclosed by symmetric intervals and the displayed K upper endpoint bounds the phased cumulant contribution.
- diagonal upper endpoints: `A_r^+= (R^G_\sigma)_{rr}+\frac{g_R^4}{16N^2}K^+_{rr}+\varepsilon^{\mathrm{OPE}}_{rr}-S^-_{rr},\quad r\in\{p,q\}`. Valid when: Applies when diagonal K4 and Schur intervals are outward rounded in the identical endpoint normalization as U_sigma.
- two-sparse stress certificate: `\tau_{pq}(\theta)=A_p^+-\frac{(B^-_{pq}(\theta))^2}{A_q^+}<0\;\Longrightarrow\;\exists t>0:\langle e_p+t e^{i\theta}e_q,U_\sigma(e_p+t e^{i\theta}e_q)\rangle<0`. Valid when: Valid for Hermitian endpoint compression matrices using Rayleigh quotient minimization over the two-sparse trial vector with A_q^+ strictly positive.

## Attempted Derivation

- Conceptual pressure attacked: replace symbolic boundary polarization R by a validator-facing connected cumulant witness that can decide a finite Schur-corrected endpoint gate.
- Freeze the finite model: heat-kernel SU(N) lattice regulator, fixed a and sigma/a, fixed H,K collar/hairpin endpoint basis, and identical Wilson normalization for cumulants and Schur blocks.
- Use the endpoint Wilson OPE to write Q_i as a normal-ordered curvature-square sheet observable; vacuum, perimeter, and disconnected pairing cancellations remove the non-connected pieces.
- Decompose cum_2(Q_i,Q_j) into a positive Gaussian crossed-curvature square with color factor alpha_N=(N^2-1)/(8N^2), a raw connected K4 plaquette-quadruple interval, and an OPE remainder interval.
- Form the same-theory endpoint matrix U_sigma by subtracting the finite Schur energy S_HK from the raw polarization matrix.
- For endpoint pair p,q and phase theta, upper-bound the diagonals by A_p^+,A_q^+ and lower-bound the negative phased off-diagonal by B^-_{pq}(theta).
- Evaluate the Rayleigh quotient on x=e_p+t e^{i theta}e_q; minimizing the interval upper bound A_p^+ + A_q^+ t^2 - 2B^- t gives tau_pq(theta)=A_p^+-(B^-)^2/A_q^+.
- Hard gate: tau_pq(theta)<0 produces a valid finite falsifier for post-H,K endpoint positivity; survival changes only the search state by forcing full Delta_raw PSD certification.

Blocking gap: The missing object is a certified same-regulator interval for K^+_{pq}(theta) and K^+_{rr} from actual raw connected four-curvature plaquette cumulants for the selected H,K endpoint pair.

## Falsifiers

- falsifier: A certified tau_pq(theta)<0 gives a negative Rayleigh vector and demotes the worked H,K endpoint positivity route immediately.
- falsifier: If raw K4 intervals cannot be produced in the same heat-kernel cutoff and Wilson normalization, the connected cumulant witness is invalid.
- falsifier: If quotienting by sheet symmetries changes any phased K4 interval, the compressed representation is non-invariant and must be abandoned.
- If OPE error intervals exceed the Gaussian-Schur margin, the phase-stress test becomes inconclusive and the branch must pivot to either tighter OPE control or quarantine.
- If all two-sparse stresses survive, this does not promote positivity; it only hands off to full Delta_raw Loewner proof search.

## Learning

Declarative tension: Wilson/OPE coefficients, raw connected K4 negativity, OPE errors, and H,K Schur subtraction must jointly control one endpoint quadratic form in one cutoff theory, while OS reconstruction, gauge-invariant observable density, excitation-sector cyclicity, nontrivial continuum YM, and the mass gap are barred. Carrier critique: scalar R is too weak, OS Hilbert observable algebra is too strong and circular for this local gate, A012 shells are convenient but quarantined, and raw plaquette enumeration is valid but fragmented. Compared with full Delta_raw PSD search, the phase-stress route is the sharper negative tactic because three endpoint interval types can falsify the route. Efficient representation must encode oriented plaquettes, sheet weights, transporters, color tensors, cumulant intervals, OPE intervals, endpoint indices, and Schur blocks; preserve gauge invariance, reflection support, Gaussian/K4 separation, endpoint compression, same-theory normalization, and exact Wilson quotienting; support cumulant contraction, interval summation, phase certification, Rayleigh stress search, Loewner bounds, and Schur subtraction; transfer only through tau, Delta_raw, or x_stress; demote on negative margin, missing intervals, non-invariant quotienting, or regulator mismatch. Conceptual value signal: sharp and route-changing at finite scope because R is now a connected cumulant witness with explicit color, geometry, non-Gaussian K4, OPE, and Schur data in one valid inequality.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe before any further abstraction.`
- Rationale: The branch has repeated the R/kappa4 mediator enough; only a same-theory phase-stress connected cumulant witness can change the finite proof state.
- Situation seed: Finite heat-kernel SU(N) endpoint box from the first H,K collar/hairpin calculation; choose two compressed Wilson sheet endpoints p,q and enumerate their transported plaquette quadruples contributing to the raw K4 interval.
- Varied variable: The phase theta in the two-sparse vector e_p+t e^{i theta}e_q, sampled first on a symmetry-reduced rational grid and then optimized over certified phase sectors.
- Held-fixed controls: Gauge group SU(N), heat-kernel regulator, cutoff a, smoothing ratio sigma/a, and renormalized coupling g_R., The H,K endpoint basis, Schur matrix S_HK, Wilson OPE truncation, vacuum/perimeter subtraction, and OPE error budget., Exact Wilson trace quotient policy and reflection support of the endpoint observables.
- Expected observation: A phase sector with K^+_{pq}(theta) sufficiently negative makes B^- large and tau_pq(theta)<0, giving a valid finite falsifier; otherwise the observation is that two-sparse stress cannot demote and full Delta_raw search is required.
- Transfer certificate needed: Outward-rounded same-regulator intervals for the phased raw K4 sums, diagonal K4 bounds, OPE errors, and Schur entries, plus an audit that quotienting preserves gauge invariance and endpoint normalization.

## Next Experiment

Proof search: select the first H,K endpoint pair p,q, enumerate the heat-kernel transported plaquette quadruples, compute phased raw K4 intervals for theta sectors, assemble the connected cumulant witness, and test tau_pq(theta)<0. This is not a gauge-invariant observable density or OS Hilbert observable algebra claim; it is a finite vacuum-orthogonal spectral witness boundary only after future OS work, which is not used here.

