# cycle-0299

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology -> finite Wilson endpoint-cumulant quarantine probe

## Candidate Lemma

In the heat-kernel plaquette-sheet regulator, the same-theory endpoint connected cumulant witness has a leading negative Haar-Jacobian root-quartic term. After the valid Wick-square and straight f f incidence cancellations, the finite post-H,K OS gate is decided by a signed endpoint interval, not by raw kappa_4 negativity.

## Definitions

- source object: a regulated SU(N) heat-kernel plaquette-sheet endpoint box v at cutoff a, with logarithmic coordinate X_v near the identity and Wilson source L_v induced by the collapsed reflected hairpin endpoints.
- target object: the scalar finite reflected-Wilson OS gate interval I_gate for the post-H,K Schur-Feshbach null channel, whose sign promotes or falsifies only this finite block.
- controlled interface: replace the unresolved connected boundary-OPE polarization R by source derivatives of log Z_v, contract them with signed endpoint incidences D_v, and add a uniform tail budget T_tail.
- same-theory condition: the source derivatives are taken inside the original regulated Wilson plaquette-sheet measure, with no boundary counterterm, new edge Hilbert sector, gauge-fixed observable, or changed Wilson normalization.
- carrier C_ep: endpoint source classes, seven source values or analytic root-quartic brackets, kappa intervals, signed fractional incidences b_ij, color factor C_W, Gaussian margin M_G, and T_tail.
- conceptual pressure: endpoint collapse must be sign-certified in the same Wilson theory rather than hidden in a symbolic R term.
- declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must jointly hold, but H,K plus the half-overlap shield do not determine the connected endpoint cumulant.

## Assumptions

- Model: four-dimensional lattice SU(N) Yang-Mills with heat-kernel plaquette action and gauge-invariant Wilson plaquette-sheet approximants for the reflected hairpins.
- Regime: endpoint boxes are small enough for logarithmic coordinates and the Weyl-denominator expansion, while separated collar segments are already accounted for in H,K and in T_tail.
- Cutoff: all constants in the endpoint bracket and tail bound are required uniformly along the finite cutoff-removal window used for this Route A block.
- Same-theory: source insertions are derivatives of the locked Wilson observables in the same regulated measure; boundary-local counterterms or altered loop renormalizations demote the lemma.
- Validity: the Gaussian Wick-square contribution is represented as a positive Gram term and the straight C_A f f contact is removed by the established null-incidence identity before this lemma is applied.
- Local: only endpoint/corner boxes enter this bracket; bulk, separated, and nonendpoint overlaps are charged to previous H,K data or to T_tail.
- Constraint: success changes the finite post-H,K reflected-Wilson OS transfer gate only; it does not prove continuum existence, full OS reconstruction, nontriviality, or the mass gap.

## Equations

- Haar Jacobian expansion: `\log J(X)=-\frac{1}{12}\sum_{\alpha>0}\alpha(X)^2-\frac{1}{1440}\sum_{\alpha>0}\alpha(X)^4+O(\|X\|^6)`. Valid when: Valid when the endpoint heat-kernel coordinate X remains inside a fixed Weyl alcove chart and the root normalization is fixed uniformly.
- leading endpoint fourth cumulant: `\kappa_v^{\mathrm{Haar}}(L_v)=\left.\partial_s^4\log Z_v(sL_v)\right|_{s=0}=-\frac{t_v^4}{60}\,\mathcal R_4(L_v)+E_v`. Valid when: Applies after Gaussian Wick contractions are removed and the endpoint source is the same Wilson source L_v in the heat-kernel box.
- root quartic factor: `\mathcal R_4(L)=\sum_{\alpha>0}\alpha(L)^4,\qquad 0\le \mathcal R_4(L)\le C_A\|L\|^4`. Valid when: Requires the standard long-root normalization and an Ad-invariant norm on the Lie algebra for SU(N) endpoint sources.
- signed endpoint incidence: `D_v=2b_{12}(v)-4b_{13}(v)-4b_{23}(v)`. Valid when: Valid for the fixed three-hairpin null vector after H and K have been contracted and endpoint overlaps are fractionally assigned to v.
- finite OS gate interval: `I_{\rm gate}=M_G+C_W\sum_v D_v\kappa_v+T_{\rm tail},\qquad \kappa_v\in[-A_v-E_v,-A_v+E_v],\ A_v=\frac{t_v^4}{60}\mathcal R_4(L_v)`. Valid when: Valid after all one-body Wilson factors, Wick-square Gram terms, and straight f f contacts have been cancelled in the Schur-Feshbach null channel.

## Attempted Derivation

- Represent the endpoint box partition function as Z_v(sL)=int exp(-||X||^2/(2t_v)+s<L,X>) J(X) exp(-V_int(X)) dX in heat-kernel logarithmic coordinates.
- Expand the Weyl-denominator Jacobian. The quadratic term only renormalizes the Gaussian damping already represented in H,K; the quartic term gives the first connected non-Gaussian fourth derivative.
- Differentiate log Z_v four times at s=0. The pure Gaussian fourth cumulant is zero in log form, while the quartic Jacobian produces -(t_v^4/60) sum_{alpha>0} alpha(L_v)^4 to leading order.
- Use the prior valid cancellations: Wick-square contractions are positive Gram terms, and the straight nonabelian f f contact cancels under the null incidence identity. Thus only endpoint/corner cumulants and T_tail remain in R.
- Contract the endpoint cumulant with D_v=2b12-4b13-4b23. Since the leading Haar term is nonpositive, only D_v>0 can reduce the finite OS margin; D_v<=0 is protective up to the certified error interval.
- Export I_gate=M_G+C_W sum_v D_v kappa_v+T_tail to the finite Schur-Feshbach gate. Positive lower interval promotes this finite block; negative upper interval is a finite same-theory falsifier.

Blocking gap: The branch still lacks cutoff-uniform values or bounds for the source-class errors E_v and for T_tail in positive-D endpoint classes.

## Falsifiers

- A positive-D endpoint source class has a certified negative fourth connected cumulant large enough that the upper endpoint of I_gate is below zero.
- The two-mesh source derivative is not cutoff-uniform, showing that the endpoint carrier is not valid for the cutoff-removal window.
- A boundary counterterm or new boundary Wilson renormalization is needed to define log Z_v(sL), violating the same-theory condition.
- The half-overlap incidence table is unstable under refinement, so D_v cannot be assigned without changing the observable algebra.
- Endpoint/corner tails are not summable across the finite collar collapse and overwhelm the Gaussian margin M_G.

## Learning

Cycle 299 adds a computable analytic layer to the quarantined endpoint carrier. In heat-kernel endpoint coordinates, the leading same-theory connected fourth cumulant is the negative Haar-Jacobian root-quartic term -(t_v^4/60) R4(L_v), with a clear uniform error obligation. This explains why negative kappa_4 is not itself the falsifier: it becomes dangerous only after multiplication by positive D_v, while half-overlap classes are protective. The hard gate is the finite post-H,K reflected-Wilson OS transfer gate. Success promotes only this finite block; failure gives a finite same-theory falsifier. Clay continuum construction, nontriviality, full OS/Wightman reconstruction, and mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe while the branch remains quarantined for endpoint data.`
- Rationale: The branch has exhausted abstract OS closed-cone and symbolic R analysis; only a target-preserving endpoint connected cumulant witness can decide the finite post-H,K gate.
- Situation seed: Take an SU(2) or SU(N) heat-kernel plaquette-sheet endpoint box for the three reflected Wilson hairpins, with the same Wilson source L_v and fractional incidences b12,b13,b23 assigned by overlap of endpoint plaquette sheets.
- Varied variable: The overlap ratio eta=(b13+b23)/b12, varied from eta=0 to eta=1 while t_v, L_v, M_G, and the Wilson normalization are held fixed.
- Held-fixed controls: The same regulated gauge-invariant Wilson plaquette-sheet observables are used; no boundary counterterm or gauge-fixed source is introduced., The prior H,K Schur-Feshbach data, null vector, Wick-square Gram positivity, and straight f f cancellation are held fixed., The cutoff window and heat-kernel endpoint chart are held fixed so source derivatives define the same-theory connected cumulant witness.
- Expected observation: For eta>=1/2 the leading negative root-quartic cumulant is protective or neutral; for eta<1/2 the finite source stencil must decide whether positive 12-dominance overcomes M_G after T_tail.
- Transfer certificate needed: A cutoff-uniform equality of regulated source data for each endpoint class, a valid bound on E_v and T_tail, and a signed interval I_gate whose lower endpoint is positive for promotion or whose upper endpoint is negative for a falsifier.

## Next Experiment

Route to proof search plus endpoint data: compute the same-theory connected cumulant witness log Z_v(sL_v) for SU(2) heat-kernel endpoint source classes at two mesh sizes, tabulate D_v, R4(L_v), E_v, and T_tail, then export the scalar interval I_gate for promotion or falsifier status.

# Gauge-Invariant Nontriviality Witness Selection -> finite endpoint R certificate

## Candidate Lemma

Ward-Hessian endpoint-cell enclosure: after centering, perimeter/cusp subtraction, and plus-channel moment cancellation, the connected boundary-OPE polarization in R_{++} admits a same-theory near/far lower interval computable from sector Hessian and L1 heat-kernel constants.

## Definitions

- source object: centered renormalized flowed Wilson hairpin cumulant R_{++}^{ren}(a,t,eta) for the SU(N) Wilson lattice action at cutoff a, with gradient-flow time t and fixed H,K endpoint boxes.
- target object: a finite lower interval R_{++}^{I,-} to be compared with the Schur-Feshbach leakage L_+ in the post-H,K endpoint-box positivity gate.
- controlled interface: endpoint sheet-current recovery map Rec_{a,t,eta} sending each thin hairpin to a gauge-invariant cell current with recorded color, orientation, reflection, zero-moment data, and recovery error E_rec.
- same-theory condition: all Wilson loops, flowed curvature fields, counterterms, cumulants, and recovery errors are computed along the same cutoff family and renormalized Schwinger family; no auxiliary Gaussian or changed action is imported.
- Bridge carrier: Ward-subtracted connected four-curvature kernel K_{4}^{WS}=K_{3g}+K_{4g}+K_{ct}+K_{end} after disconnected product removal and one-hairpin perimeter/cusp cancellation.
- Endpoint moments: M_{0,+}=sum_alpha |q_alpha| |C_alpha| and M_{2,+}=sum_alpha |q_alpha| |C_alpha| |x_alpha-x_*|^2 for the plus-channel endpoint current.

## Assumptions

- Model: four-dimensional hypercubic SU(N) Wilson lattice gauge theory with gradient flow at t>=c a^2 and fixed finite H,K hairpin geometry.
- Regime: endpoint side eta, near/far radius rho, and flow time satisfy a<<eta<=rho/4<=sqrt(t) and the endpoint boxes remain disjoint from nonlocal Wilson segments.
- Cutoff: sector Hessian constants H_{rho,t}^{I,+} and near constants A_{rho,t}^{I,+} are enclosed uniformly for a/sqrt(t) in the chosen regulator window.
- Same-theory: Rec_{a,t,eta} is built from flowed Wilson observables in the same Schwinger family and preserves centering, reflection, gauge invariance, and color normalization up to E_rec.
- Validity: the lemma is a finite endpoint-box certificate only; it does not assert OS reconstruction, continuum existence, observable density, or a Hamiltonian mass gap.

## Equations

- R++ decomposition: `R_{++}^{ren}=g_t^4\,2(N^2-1)G_{++}+g_t^6\,N(N^2-1)\Xi_{++}^{WS}+E_{\ge 8}+E_{rec}`. Valid when: Valid when the flowed hairpin expansion is centered, cusp-subtracted, and truncated inside the fixed endpoint boxes with a certified recovery remainder.
- plus moment cancellation: `\sum_\alpha q_\alpha |C_\alpha|=0,\qquad \sum_\alpha q_\alpha |C_\alpha|(x_\alpha-x_*)=0`. Valid when: Requires the plus-channel H,K endpoint-current encoding and reflection-symmetric cell partition used by Rec_{a,t,eta}.
- far Hessian bound: `|\Xi_{++}^{far}|\le {1\over 4}H_{\rho,t}^{I,+}M_{2,+}^{2}`. Valid when: Applies on the far region where all Ward-subtracted sector kernels are twice differentiable and the monopole and dipole moments vanish.
- near L1 bound: `|\Xi_{++}^{near}|\le A_{\rho,t}^{I,+}M_{0,+}^{4}`. Valid when: Valid on the near collision cells after heat-kernel majorants dominate the Ward-subtracted sector kernels with outward-rounded interval constants.
- endpoint promotion interval: `R_{++}^{I,-}=g_t^4\,2(N^2-1)G_{++}^{I,-}-g_t^6\,N(N^2-1)\left(A_{\rho,t}^{I,+}M_{0,+}^{4}+{1\over4}H_{\rho,t}^{I,+}M_{2,+}^{2}\right)-E_{rec}^{I,+}-E_{\ge8}^{I,+}`. Valid when: Valid when pair covariance, sector kernel bounds, truncation errors, and recovery errors are all interval-enclosed in the same cutoff theory.

## Attempted Derivation

- Conceptual pressure attacked: finite Schur-Feshbach positivity needs a same-theory Wilson mediator, while positive pair covariance and gradient-flow renormalization can both be valid and still be erased by the connected four-curvature polarization.
- Declarative tension: endpoint positivity, Wilson cumulant positivity, and same-theory recovery must jointly hold; the missing mediator is a cutoff-stable Ward-Hessian bound for C4 with recovery errors.
- Carrier critique: raw Wilson contours are fragmented and representation-limited; global OS spectral transfer or a non-Gaussian Schwinger family route is too coarse for this finite endpoint obstruction.
- Abstraction comparison: endpoint sheet currents are better because Ward subtraction, plus-moment cancellation, near/far heat-kernel majorants, outward-rounded interval quadrature, and zero-pairing quotienting become primitive operations.
- Write the centered flowed Wilson hairpin cumulant and subtract the disconnected product plus one-hairpin perimeter/cusp terms; the pair contraction gives the positive baseline g_t^4 2(N^2-1)G_{++}.
- Decompose the remaining connected four-curvature polarization into Ward-subtracted sectors K_{3g}, K_{4g}, K_{ct}, and K_{end}, each with color factor N(N^2-1) after normalization.
- Encode the plus endpoint hairpin as a finite cell current q_alpha with zero monopole and dipole moments; this cancels the constant and linear Taylor jets of K_4^{WS} on far cells.
- Split the integration domain by near distance rho. Bound far cells by a Hessian seminorm H_{rho,t}^{I,+} times M_{2,+}^2, and bound near collision cells by an L1 heat-kernel majorant A_{rho,t}^{I,+} times M_{0,+}^4.
- Combine the bounds into R_{++}^{I,-} and compare with the finite Schur-Feshbach leakage L_+. Success changes the hard gate of finite endpoint-box positivity after H,K; failure quarantines only this R repair.
- Efficient representation requirements: encode H,K sheets, endpoint currents, cell moments, sector kernels, counterterms, and recovery errors; preserve gauge, color, reflection, orientation, cutoff, and same-theory invariants; primitives are cumulant expansion, Ward/cusp subtraction, Taylor remainder, heat-kernel majorants, interval quadrature, outward rounding, and zero-pairing quotienting; locality is finite endpoint cells with bounded refinement; transfer is through centered flowed Wilson cumulants; falsifiers are Ward, cusp, plateau, geometry, cutoff-uniformity, or interval-width failure.

Blocking gap: The proof still needs certified numerical or analytic enclosures for H_{rho,t}^{I,+}, A_{rho,t}^{I,+}, E_{rec}^{I,+}, and E_{>=8}^{I,+} for the concrete H,K endpoint cells and a regulator window uniform in a/sqrt(t).

## Falsifiers

- falsifier: the Ward-subtracted sector kernel retains an uncancelled endpoint contact term, invalidating the Hessian Taylor remainder.
- falsifier: the plus-channel endpoint current fails the certified zero monopole or dipole moment identities after recovery from Wilson hairpins.
- falsifier: the near L1 majorant A_{rho,t}^{I,+} is so large that R_{++}^{I,-} never beats L_+ in any admissible rho window.
- falsifier: no plateau appears as a/sqrt(t) decreases, so the same-theory cutoff-uniform recovery condition is not valid.
- falsifier: cusp/perimeter counterterms depend on the tested pair and are not one-hairpin local, breaking the cancellation used in R_{++}.
- falsifier: interval refinement stalls with width larger than the Schur-Feshbach margin, making the endpoint gate undecidable.

## Learning

Cycle 299 makes the non-looping move from a generic near/far plan to a concrete Ward-Hessian interval formula for R_{++}^{ren}: positive pair baseline minus explicit connected C4 majorants and recovery errors. The conceptual value signal is local and route-changing: a symbolic endpoint term becomes a valid falsifiable color-geometric certificate for finite endpoint-box positivity after H,K. Success promotes one finite Route A gate; failure quarantines the R repair. Clay existence, OS/Wightman axioms, nontrivial continuum limit, gauge-invariant observable density, large-field/topology control, and positive Hamiltonian mass gap remain unclaimed.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a validator-facing falsifier probe for the finite endpoint R certificate.`
- Rationale: The branch has exhausted abstract restatements; the decisive question is whether a concrete same-theory flowed Wilson cumulant can supply a valid endpoint mediator before any continuum or OS spectral-transfer claim is attempted.
- Situation seed: SU(3) Wilson lattice regulator with gradient flow, fixed reflected H,K plus-channel endpoint hairpins, centered flowed Wilson loops, and endpoint cells carrying Ward-subtracted sheet currents; record the output also as a connected cumulant witness candidate but do not promote it beyond finite scope.
- Varied variable: u=rho/sqrt(t), the near/far split radius in physical flow units.
- Held-fixed controls: Same bare Wilson action, same RG trajectory, and same gradient-flow renormalization prescription., Fixed H,K hairpin geometry, reflection plane, plus-channel endpoint current, and Schur-Feshbach leakage L_+., Outward-rounded interval arithmetic, one-hairpin cusp/perimeter subtraction, and zero-pairing equivalence policy., Endpoint locality budget eta<=rho/4 and bounded cell-refinement depth.
- Expected observation: A stable window in u should show R_{++}^{I,-}-L_+ either positive with margin or uniformly nonpositive; the former promotes finite endpoint-box positivity, the latter demotes the R repair.
- Transfer certificate needed: Cutoff-uniform Ward-Hessian and near L1 sector bounds, same-theory recovery errors for Wilson-to-current replacement, and a regulator-window plateau before the intuition may affect proof obligations.

## Next Experiment

Proof search: instantiate the SU(3) H,K plus-channel endpoint cells, compute M_{0,+}, M_{2,+}, G_{++}^{I,-}, and interval-enclose K_{3g}, K_{4g}, K_{ct}, K_{end} for several u=rho/sqrt(t); report whether the connected cumulant witness candidate supplies R_{++}^{I,-}>L_+ or triggers quarantine.

# Gauge-Invariant Observable Density In The Excitation Sector; quarantined to finite raw K4 endpoint stress audit

## Candidate Lemma

Finite raw-K4 two-sparse stress lemma. In a fixed heat-kernel cutoff SU(N) Wilson endpoint box after the H,K Schur-Feshbach reduction, an outward-rounded interval enclosure of the Schur-corrected endpoint matrix U_sigma gives a valid demotion certificate if some two-sparse vector x=e_p+eta e_q has sup I_{pq}(eta)<0. Conversely, only a certified Loewner lower bound U_sigma>=delta I promotes finite endpoint-box positivity; neither conclusion is a continuum OS or mass-gap theorem.

## Definitions

- source object: a heat-kernel regulated finite-volume four-dimensional SU(N) Wilson measure with endpoint plaquette sheets, transported curvature insertions, raw connected K4 cumulant intervals, OPE error intervals, and fixed H,K Schur blocks.
- target object: the finite Schur-corrected endpoint quadratic form U_sigma on the endpoint coefficient space E_end; the target property is finite endpoint positivity U_sigma>=0, not Hamiltonian spectral gap.
- controlled interface: the recovery map Rec_sigma from raw plaquette cumulant intervals to endpoint matrix entries, using Wilson sheet weights, heat-kernel transporters, SU(N) color contractions, exact trace quotients, OPE intervals, and Schur subtraction.
- same-theory condition: the same cutoff sigma, lattice spacing a, volume Lambda, bare coupling, gauge group, reflection support, Wilson normalization, endpoint basis, and H,K Schur data are used for every Gaussian, K4, OPE, and Schur term.
- bridge/carrier: a raw plaquette interval hypergraph whose nodes are oriented transported plaquette insertions and whose edges are connected cumulant intervals; scalar R and shell A012 are quarantined carriers.
- observable marker: connected cumulant witness for a finite Wilson endpoint calculation; gauge-invariant observable density and OS Hilbert observable algebra remain non-claims.

## Assumptions

- Model: finite heat-kernel lattice regulator for Euclidean SU(N) Yang-Mills observables in a reflection-compatible box, with Wilson loops expanded only inside the endpoint collar.
- Regime: finite Route A post-H,K endpoint box with sigma/a fixed and endpoint collar width larger than the OPE support radius.
- Cutoff: all interval inputs are computed in the same cutoff theory; no RG, continuum, or physical-unit spectral transfer is used.
- Same-theory: the Schur block B^*E^{-1}B and the Wilson cumulants are evaluated with identical H,K basis vectors and identical vacuum normalization.
- Validity: interval arithmetic is outward-rounded and every Wilson trace or sheet symmetry quotient is audited before entries are merged.
- Constraint: E=QHQ is strictly positive on the eliminated hairpin subspace, so the finite Schur-Feshbach subtraction is well-defined.

## Equations

- endpoint-flux-carrier: `Q_i^{\sigma}=\sum_{p\in\mathcal P_i} w_{ip}\,\mathrm{Tr}\big(T^{a_p}U_{\gamma_{ip}}F^{a_p}_{\mu_p\nu_p,\sigma}(z_p)U_{\gamma_{ip}}^{-1}\big)`. Valid when: Valid when all raw plaquette nodes and transporters belong to the fixed heat-kernel cutoff endpoint box.
- connected-boundary-polarization: `R_{ij,\sigma}=\operatorname{cum}_2\big(: (Q_i^{\sigma})^2 :,: (Q_j^{\sigma})^2 :\big)`. Valid when: Valid when vacuum and perimeter disconnected pieces are removed in the same regulated Wilson measure.
- raw-Wilson-decomposition: `R_{\sigma}=\alpha_N g_R^4(C_{\sigma}\circ C_{\sigma})+\frac{g_R^4}{16N^2}K^{(4)}_{\sigma}+E^{\mathrm{OPE}}_{\sigma},\qquad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after transported curvature OPE normalization and SU(N) trace contraction in the fixed endpoint basis.
- Schur-corrected-endpoint-matrix: `U_{\sigma}=R_{\sigma}-S_{HK,\sigma},\qquad S_{HK,\sigma}=B_{\sigma}^{*}E_{\sigma}^{-1}B_{\sigma}`. Valid when: Requires the eliminated H,K hairpin block E_sigma to be positive in the finite Schur-Feshbach decomposition.
- two-sparse-interval-Rayleigh: `I_{pq}(\eta)=I_{pp}+2\eta\,I_{pq}+\eta^2 I_{qq}\supset \langle e_p+\eta e_q,U_{\sigma}(e_p+\eta e_q)\rangle`. Valid when: Valid when the interval entries I_ab enclose the corresponding Schur-corrected endpoint matrix entries.
- stress-falsifier-condition: `\sup I_{pq}(\eta)<0\;\Longrightarrow\; U_{\sigma}\not\ge 0`. Valid when: Valid when the two-sparse vector is nonzero and the interval enclosure contains the true same-theory matrix.

## Attempted Derivation

- Conceptual pressure attacked: the branch must stop using symbolic R or shell placeholders and must test whether the actual connected boundary-OPE polarization can certify or kill the post-H,K endpoint positivity gate.
- Freeze independent source and target: the source is the finite heat-kernel Wilson cumulant table plus Schur blocks; the target is positivity of U_sigma on the finite endpoint coefficient space, not gauge-invariant observable density or a mass gap.
- Expand endpoint Wilson carriers to transported curvature fluxes Q_i^sigma and normal-order so vacuum/perimeter disconnected pieces cancel before taking cum_2(:Q_i^2:,:Q_j^2:).
- Separate R_sigma into the SU(N) Gaussian Hadamard square, the connected K4 operator, and an OPE interval; the Gaussian part is PSD, so a negative Rayleigh value must come from K4, OPE, or Schur subtraction.
- Apply finite Schur-Feshbach: U_sigma=R_sigma-B^*E^{-1}B, valid only because the eliminated H,K block E is positive in the finite truncation.
- Compress to a two-sparse stress vector x=e_p+eta e_q and form the interval I_pq(eta)=I_pp+2 eta I_pq+eta^2 I_qq; if its upper endpoint is negative, every admissible same-theory matrix has a negative Rayleigh quotient.
- Hard gate: Delta_raw>0 promotes only finite endpoint-box positivity, while sup I_pq(eta)<0 gives a falsifier for this H,K collar/hairpin route; missing raw K4 intervals force quarantine.

Blocking gap: The actual same-regulator connected K4 intervals for a selected plaquette pair pp,pq,qq and the matching OPE interval are still absent; without them neither Delta_raw nor a two-sparse stress falsifier is numerically valid.

## Falsifiers

- A same-regulator two-sparse interval with sup I_pq(eta)<0 is a valid falsifier for post-H,K endpoint positivity in this H,K geometry.
- The connected K4 interval is so wide that neither the upper stress test nor the lower Loewner margin is decisive; the route is quarantined until sharper raw cumulants exist.
- Exact Wilson quotient auditing fails, so merged plaquette nodes do not preserve gauge-invariant cumulants.
- The OPE interval or Schur block is imported from a different regulator, coupling, volume, or endpoint basis.
- The Gaussian color factor alpha_N=(N^2-1)/(8N^2) is not compatible with the chosen trace normalization.
- A positive finite endpoint margin is found but later used as an OS spectral-transfer or Clay mass-gap claim; that overclaim is invalid.

## Learning

Declarative tension: Wilson/OPE coefficients, connected K4 negativity, OPE errors, and H,K Schur subtraction must jointly control one endpoint quadratic form in a single cutoff theory, while Clay-level continuum existence, OS/Wightman reconstruction, gauge-invariant observable density, and Hamiltonian mass gap are barred as conclusions. Carrier revision: scalar R is too weak and representation-limited; OS observable-density language is too strong and circular for this local gate; shell A012 is convenient but quarantined; raw plaquette enumeration is fragmented yet valid. Compared with full matrix Delta search, the two-sparse stress route is the sharper negative tactic because it can demote the H,K endpoint route from three same-regulator K4 intervals. Efficient representation must encode oriented plaquettes, sheet weights, heat-kernel transporters, color tensors, cumulant intervals, OPE intervals, endpoint indices, and Schur blocks; preserve gauge invariance, reflection support, Gaussian/K4 separation, endpoint compression, same-theory normalization, and exact Wilson quotienting; support cumulant contraction, interval summation, phase-sector certification, Rayleigh stress search, Loewner lower bounds, and Schur subtraction; keep a finite endpoint-box complexity budget; transfer only through Delta_raw or x_stress; and expose falsifiers by negative Rayleigh margin, non-invariant quotienting, missing intervals, or regulator mismatch. Conceptual value signal: sharp and route-changing at finite scope because R is now a validator-facing connected cumulant witness with explicit color, geometry, non-Gaussian K4, OPE, and Schur data in one valid inequality.

## Gedanken Experiment Design Seed

- Need decision: `Design concrete falsifier probe now.`
- Rationale: The branch has repeated abstraction for several cycles; the next mathematically informative move is a target-preserving two-sparse stress test using actual same-regulator K4 intervals rather than another OS/Wilson obstruction restatement.
- Situation seed: Heat-kernel regulated SU(N) Wilson endpoint box after the fixed H,K collar/hairpin Schur reduction; choose two oriented plaquette-sheet nodes p and q sharing one boundary collar edge and build the endpoint vector x=e_p+eta e_q.
- Varied variable: The real two-sparse phase/amplitude eta in x=e_p+eta e_q.
- Held-fixed controls: Gauge group SU(N), finite volume Lambda, heat-kernel cutoff sigma, lattice spacing a, and bare coupling., The same endpoint basis, Wilson normalization, reflection support, H,K Schur blocks, and exact trace quotient policy., The Gaussian covariance C_sigma, OPE error convention, and recovery map Rec_sigma.
- Expected observation: If the connected K4 anticorrelation for p,q dominates the PSD Gaussian square, OPE upper error, and the least Schur subtraction contribution, then sup I_pq(eta)<0 for some eta; otherwise the pair is not a demoting stress witness and proof search must move to Loewner lower bounds or another pair.
- Transfer certificate needed: A validator-facing connected cumulant witness: outward-rounded same-regulator intervals for K4_pp, K4_pq, K4_qq, matching C_sigma and E_OPE entries, certified Schur block intervals, and an exact Wilson quotient audit before the intuition changes proof obligations.

## Next Experiment

Proof search: compute the validator-facing connected cumulant witness for one adjacent endpoint plaquette pair p,q in the fixed heat-kernel SU(N) H,K collar/hairpin box; form I_pq(eta), search eta for sup I_pq(eta)<0, and otherwise attempt a certified Delta_raw Loewner lower bound. Route explicitly to raw_K4 interval computation; quarantine if the same-regulator intervals are still missing.

