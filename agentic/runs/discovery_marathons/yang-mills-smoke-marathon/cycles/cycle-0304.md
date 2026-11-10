# cycle-0304

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: endpoint source interval gate

## Candidate Lemma

For the finite three-hairpin post-H,K block in the SU(N) heat-kernel plaquette-sheet regulator, the endpoint part of the connected boundary-OPE polarization has a valid signed interval controlled by the negative Haar root-quartic cumulant, the null-channel incidence D_v, and a cutoff-uniform tail. Promotion is I_- >= 0; demotion is I_+ < 0, a finite same-theory falsifier.

## Definitions

- source object: finite heat-kernel plaquette-sheet endpoint boxes E_v with source maps L_v and regulated endpoint logarithmic partition functions Z_v(s)=Z_v(sL_v).
- target object: the finite post-H,K reflected-Wilson OS null scalar for the fixed three-hairpin Wilson block after Schur-Feshbach reduction.
- controlled interface: the endpoint source carrier C_ep=(Z_v(-3h),...,Z_v(3h),D_v,C_N,M_G,T_tail) mapping regulated connected cumulants to one scalar interval.
- same-theory condition: the sources L_v come from the original gauge-invariant Wilson plaquette sheets, with no boundary counterterm, no added boundary Hilbert sector, and identical Wilson normalization before and after endpoint collapse.
- Endpoint incidence is D_v=2b_{12,v}-4b_{13,v}-4b_{23,v}, where b_{ij,v} is the fractional footprint of the reflected i,j hairpin pairing inside endpoint box v.
- The color factor C_N is the singlet Wilson contraction prefactor remaining after the Wick-square Gram term and straight f f contact are removed.
- The tail T_tail charges all endpoint overlap not represented by the finite endpoint boxes, including corner mismatch and regulator-chart remainder.

## Assumptions

- Model: four-dimensional Euclidean SU(N) lattice Yang-Mills with heat-kernel plaquette action, finite volume, cutoff a>0, and fixed reflected Wilson hairpin observables.
- Regime: endpoint heat-kernel coordinates satisfy t_v ||L_v|| below a fixed chart radius so the SU(N) Haar-Jacobian expansion has a uniform remainder.
- Uniformity: the bounds on E_v and T_tail are independent of cutoff along the finite block and depend only on finitely many endpoint geometry classes.
- Same-theory: endpoint source derivatives are taken inside the locked gauge-invariant Wilson algebra and are not replaced by boundary fields or gauge-fixed representatives.
- Local: the lemma concerns one finite post-H,K Wilson block; it does not assert continuum existence, OS reconstruction for all observables, nontriviality, or a mass gap.
- Validity: timeline-definition-assumption-elicitor should flag any use of uncomputed source intervals, nonuniform tails, or hidden boundary renormalization.

## Equations

- endpoint connected fourth cumulant: `\kappa_v(L_v)=\left.\partial_s^4\log Z_v(sL_v)\right|_{s=0}=-\frac{t_v^4}{60}R_4(L_v)+E_v,\quad R_4(L)=N\operatorname{tr}(L^4)+3(\operatorname{tr}L^2)^2`. Valid when: Valid when the endpoint heat-kernel coordinate chart is small, the source is traceless anti-Hermitian in the SU(N) Lie algebra, and the Haar-Jacobian remainder E_v is uniformly bounded.
- null-channel endpoint incidence: `D_v=2b_{12,v}-4b_{13,v}-4b_{23,v},\qquad b_{13,v}+b_{23,v}\ge b_{12,v}/2\Longrightarrow D_v\le0`. Valid when: Valid when the three-hairpin Schur-Feshbach null vector and the fixed post-H,K pair weights are used without changing Wilson normalizations or endpoint footprints.
- signed endpoint interval: `I_{gate}=M_G+C_N\sum_v D_v\kappa_v+T_{tail}\in\left[M_G+C_N\sum_v(D_v^+\kappa_v^- -D_v^-\kappa_v^+)+\tau^-,\;M_G+C_N\sum_v(D_v^+\kappa_v^+ -D_v^-\kappa_v^-)+\tau^+\right]`. Valid when: Applies after same-theory endpoint source intervals \kappa_v\in[\kappa_v^-,\kappa_v^+] and tail interval T_tail in [tau^-,tau^+] are certified uniformly at fixed cutoff family.
- root-quartic worst-case lowering: `\kappa_v\ge -\frac{t_v^4}{60}R_4^+(L_v)-\epsilon_v,\qquad \Delta I_{danger}\ge -C_N\sum_v [D_v]_+\left(\frac{t_v^4}{60}R_4^+(L_v)+\epsilon_v\right)-\tau_+`. Valid when: Requires positive color prefactor C_N, bounded endpoint remainder |E_v|<=epsilon_v, and the same signed incidence carrier used in the finite OS null scalar.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: finite heat-kernel plaquette-sheet endpoint boxes E_v with source maps L_v and regulated endpoint logarithmic partition functions Z_v(s)=Z_v(sL_v).; target object: the finite post-H,K reflected-Wilson OS null scalar for the fixed three-hairpin Wilson block after Schur-Feshbach reduction.; Model: four-dimensional Euclidean SU(N) lattice Yang-Mills with heat-kernel plaquette action, finite volume, cutoff a>0, and fixed reflected Wilson hairpin observables..
- Fix the SU(N) heat-kernel plaquette-sheet regulator, the three reflected Wilson hairpins, and the already computed H,K Schur-Feshbach null vector; do not change the observable algebra.
- Write each endpoint contribution as a regulated source derivative of log Z_v(sL_v). The connected logarithm removes disconnected Wick-square terms from the dangerous scalar, while earlier null incidence cancels the straight C_A f f contact.
- Expand the SU(N) endpoint Haar Jacobian in heat-kernel coordinates. The fourth source derivative gives the leading connected non-Gaussian term -t_v^4 R_4(L_v)/60 plus a uniform remainder E_v.
- Contract the endpoint cumulants with the actual null-channel signed incidence D_v=2b12-4b13-4b23. Negative kappa_v lowers the gate only when D_v>0; half-overlap boxes with D_v<=0 are protective or neutral.
- Replace individual endpoint boxes by source-equivalence classes only when their seven regulated source values and error budgets agree, then sum incidences before interval multiplication.
- Add the positive Gaussian margin M_G and tail interval T_tail to obtain [I_-,I_+]. This is the finite gate exported to proof search.

Blocking gap: The actual endpoint source-equivalence classes, fractional incidences b_ij,v, uniform remainder E_v, and tail interval T_tail have not been computed for the concrete regulated hairpin geometry.

## Falsifiers

- A same-theory connected cumulant witness with certified I_+<0 is a finite reflected-Wilson OS falsifier for this post-H,K block.
- Endpoint source derivatives that require a boundary counterterm or a boundary Hilbert sector violate the same-theory condition.
- A nonuniform endpoint remainder E_v or tail T_tail as a->0 invalidates the finite-to-regulated transfer certificate.
- A source-equivalence compression based only on geometric similarity, not equal regulated source data, can hide positive D leakage and is invalid.
- A stress case with b12>0 and b13=b23=0 tests maximal 12-only dominance; if its root-quartic lowering exceeds M_G after tails, the branch demotes.

## Learning

Conceptual pressure attacked: endpoint collapse must be sign-certified in the same Wilson theory rather than hidden in symbolic R. Declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular endpoint boundary OPE must jointly hold without adding a boundary theory; H,K plus half-overlap data alone do not decide the post-H,K scalar. Carrier audit: raw R is too weak, raw kappa_4 spectra are too strong, and the global Schur-preimage test is valid but too coarse after H,K. Efficient representation C_ep encodes endpoint source classes, seven source values, cumulant intervals, signed incidences, C_N, M_G, and T_tail; preserves Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; uses source differentiation, interval arithmetic, source-equivalence, color multiplication, clipping, incidence contraction, and tail addition; identifies carriers only by equal regulated source data; exports [I_-,I_+] to the finite OS gate. Conceptual value signal: sharp local route change; the negative SU(N) root-quartic cumulant is explanatory but not itself the falsifier, only positive-D endpoint dominance plus uncontrolled tail can demote the finite block.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe while the branch remains quarantined for endpoint data.`
- Rationale: The abstract OS closed-cone and symbolic R routes are exhausted; the finite gate now turns on one same-theory connected cumulant witness multiplied by fractional endpoint dominance.
- Situation seed: SU(N) heat-kernel plaquette-sheet three-hairpin endpoint box with one source-equivalence class, fixed H,K null vector, and fractional overlaps b12=1, b13=b23=alpha/2.
- Varied variable: alpha=(b13+b23)/b12, the endpoint half-overlap ratio controlling D=2b12(1-2alpha).
- Held-fixed controls: Same Wilson hairpin observables and Wilson normalization used in the collar calculation., Heat-kernel plaquette-sheet regulator and SU(N) color normalization C_N., No boundary counterterm, no gauge fixing, and no added boundary Hilbert sector., Previously computed H,K Schur-Feshbach data and positive Gaussian margin M_G., Cutoff-uniform source-remainder and tail-budget assumptions.
- Expected observation: For alpha>=1/2 the root-quartic negative cumulant is shielded; for alpha<1/2 the interval decreases linearly in 1-2alpha and can cross zero only if the certified root-quartic plus tail beats M_G.
- Transfer certificate needed: Equal regulated endpoint source data for compression, cutoff-uniform E_v and T_tail, and a same-theory boundary-OPE certificate before the intuition may affect finite OS proof obligations.

## Next Experiment

Route to proof search plus endpoint data: compute the connected cumulant witness for each heat-kernel endpoint source-equivalence class, form D_v=2b12-4b13-4b23, certify E_v and T_tail, and export [I_-,I_+] to the finite post-H,K OS gate; remain quarantined if the endpoint source intervals are unavailable.

# Gauge-Invariant Nontriviality Witness Selection -> endpoint Wilson cumulant interval gate

## Candidate Lemma

Conditional finite theorem: for the fixed H,K plus-channel endpoint boxes, Ward/cusp subtraction and plus-channel moment cancellation reduce the connected boundary-OPE polarization R_{++}^{ren} to a positive pair baseline minus a computable near/far Ward-Hessian C4 majorant and recovery errors. If the resulting lower interval beats the Schur-Feshbach leakage L_+, finite endpoint-box positivity after H,K is valid; otherwise this R repair is falsified.

## Definitions

- source object: centered flowed Wilson endpoint cumulant R_{++}^{ren}(t,epsilon,a;E)=kappa_2(W_+^{ren},W_+^{ren}) for fixed H,K hairpin endpoint boxes in four-dimensional SU(N) Yang-Mills.
- target object: finite Route A endpoint-box positivity certificate Q_+^{ren}=P_+-L_+ + R_{++}^{ren} >= 0 for the Schur-Feshbach plus channel; this is not the Clay mass-gap property.
- controlled interface: endpoint sheet-current recovery map Rec_E from renormalized Wilson hairpins to signed endpoint currents, preserving gauge, color, reflection, orientation, cutoff locality, and cumulant errors Delta_rec.
- same-theory condition: one SU(N) Yang-Mills regulator/RG trajectory supplies the Wilson loops, flowed curvatures, counterterms, pair covariance, C4 kernels, and recovery errors; no Gaussian reference theory replaces the source theory.
- carrier: endpoint sheet currents with cell moments, Ward-subtracted sector kernels K_s^{WS}, counterterms, near/far heat-kernel majorants, and outward-rounded interval arithmetic.
- hard gate changed: finite endpoint-box positivity after H,K; success promotes this local Route A gate, failure quarantines only the R_{++} repair.
- untouched gates: continuum existence, OS/Wightman reconstruction, gauge-invariant observable density, large-field/topology control, nontrivial continuum limit, and positive Hamiltonian mass gap.

## Assumptions

- Model: four-dimensional Euclidean SU(N) Yang-Mills on a finite reflected box or lattice regulator, with fixed finite H,K Wilson collar/hairpin geometry.
- Regime: gradient-flow time t>0, point-splitting epsilon>0, endpoint cell diameter eta <= c sqrt(t), and a finite near/far split rho between eta and the endpoint-box scale.
- Cutoff: t >= c0 a^2 and all constants are stated with explicit a,t,epsilon,eta dependence before any continuum use.
- Same-theory: W_+^{ren}, flowed curvature insertions, cusp/perimeter counterterms, and Rec_E are evaluated on the same bare action and same RG trajectory.
- Uniformity: Ward identities and cusp subtractions are required uniformly over endpoint cells and sector partitions used in the interval enclosure.
- Local: the claim concerns one fixed finite H,K plus-channel endpoint-box test and does not assert OS positivity or a spectral gap.
- Validity: sixth-order and higher cumulant remainder E_6^+ and recovery error Delta_rec^+ must be bounded with outward rounding.

## Equations

- flowed endpoint cumulant decomposition: `R_{++}^{ren}=g_t^4 (N^2-1)\left(2G_{++}+N C_{4,++}^{WS}\right)+E_6`. Valid when: Valid when the flowed Wilson hairpins are centered, cusp-renormalized, and expanded at fixed t using the same endpoint-cell recovery map.
- plus-channel endpoint moment cancellation: `\int_E d\mu_+(x)=0,\qquad \int_E (x-c)_\alpha\,d\mu_+(x)=0`. Valid when: Requires the reflected H,K plus current, the certified orientation convention, and the Ward-subtracted endpoint-cell representation.
- Ward-Hessian near/far constant: `H_4^{I,+}(t,\rho)=\sum_{s\in\{3g,4g,ct,end\}}\left(H_{s,near}^{I,+}(t,\rho)+H_{s,far}^{I,+}(t,\rho)\right)`. Valid when: Applies after each one-loop sector kernel is Ward-subtracted and enclosed on the same finite endpoint-cell partition.
- connected polarization majorant: `|C_{4,++}^{WS}|\le H_4^{I,+}(t,\rho)\,M_{2,+}^2+\Delta_{rec}^{I,+}`. Valid when: Valid when monopole and dipole moments vanish and the sector Hessian intervals cover all near and far cell pairs.
- endpoint lower interval: `R_{++}^{I,-}=g_t^4 (N^2-1)\left(2G_{++}^{I,-}-N H_4^{I,+}M_{2,+}^2\right)-E_6^{I,+}-g_t^4N(N^2-1)\Delta_{rec}^{I,+}`. Valid when: Requires positive pair covariance, same-theory recovery, bounded sixth-order remainder, and outward-rounded interval constants for the fixed H,K instance.
- finite promotion inequality: `R_{++}^{I,-}\ge L_+ + \tau\quad (\tau>0)\ \Longrightarrow\ Q_+^{ren}\ge \tau`. Valid when: Valid when L_+ is the Schur-Feshbach leakage from the same finite H,K matrix normalization and no endpoint basis change is made.
- analytic far-tail template: `H_{s,far}^{I,+}(t,\rho)\le C_s^{I}\,t^{-6}\exp(-\rho^2/(32t))\Phi_s(\rho/\sqrt t)`. Valid when: Applies to flowed curvature sector kernels represented by heat-kernel derivatives after Ward cancellation removes unflowed massless tails.

## Attempted Derivation

- Conceptual pressure attacked: finite Schur-Feshbach positivity needs a same-theory Wilson mediator, while the connected four-curvature polarization can erase a valid positive pair covariance.
- Start with R_{++}^{ren}=kappa_2(W_+^{ren},W_+^{ren}) under gradient flow and boundary point-splitting; expand the centered Wilson exponentials through order g_t^4.
- Use disconnected-product subtraction and one-hairpin perimeter/cusp renormalization; the remaining order-g_t^4 terms split into the positive two-curvature cross-pairing 2(N^2-1)G_{++} and sector kernels 3g,4g,ct,end with color N(N^2-1).
- Replace raw Wilson contours by endpoint sheet currents; the carrier critique is that raw contours are fragmented, whereas endpoint currents make Ward subtraction, moment cancellation, and interval Hessians primitive.
- Compare abstractions: global OS spectral transfer or a non-Gaussian Schwinger family route is too coarse for this finite obstruction; endpoint interval proof search directly attacks the finite H,K gate.
- Apply the plus-channel cancellation int dmu_+=0 and int(x-c)dmu_+=0, so constant and dipole pieces of each Ward-subtracted sector kernel drop out.
- Split each sector kernel into near cells |z|<=rho and far cells |z|>rho. Near cells require outward-rounded Hessian suprema; far cells use flowed heat-kernel derivative majorants with Gaussian tail after Ward cancellation.
- Obtain the lower interval R_{++}^{I,-}=g_t^4(N^2-1)(2G_{++}^{I,-}-N H_4^{I,+}M_{2,+}^2)-E_6^{I,+}-g_t^4N(N^2-1)Delta_rec^{I,+}.
- Transfer to finite positivity only if R_{++}^{I,-}>=L_+ + tau for the same Schur-Feshbach normalization.

Blocking gap: The proof still lacks certified numerical or analytic values for the sector Hessian constants H_{s,near}^{I,+}, the far-tail constants C_s^I, and the sixth-order/recovery error bounds in one regulator window.

## Falsifiers

- falsifier: the plus-channel endpoint current has a residual monopole or dipole after the actual H,K orientation data are inserted.
- falsifier: Ward or cusp subtraction leaves an uncancelled near-diagonal term whose interval grows faster than M_{2,+}^{-2}.
- falsifier: the far-tail majorant is not valid for flowed curvature sector kernels because a massless unflowed tail survives the Ward subtraction.
- falsifier: the same-theory recovery error Delta_rec is comparable to or larger than the positive pair baseline.
- falsifier: R_{++}^{I,-}<L_+ for every admissible rho and flow-time plateau, quarantining the endpoint R repair.
- falsifier: the endpoint quotient discards a current with nonzero covariance against the retained H,K test family.
- Stress case: eta approaches sqrt(t), making the endpoint Taylor remainder too wide for promotion.
- Stress case: N is large enough that the N H_4^{I,+}M_{2,+}^2 penalty overwhelms the 2G_{++}^{I,-} baseline.

## Learning

Cycle 304 attacks the missing same-theory mediator between finite Schur-Feshbach endpoint positivity and Wilson cumulant positivity. The declarative tension is precise: positive flowed pair covariance, same-theory renormalization, and finite endpoint positivity can each be valid while connected C4 erases the pair term unless Ward-Hessian constants and recovery errors are certified. The current carrier, raw Wilson contours, is representation-limited and fragmented; global OS spectral transfer and a non-Gaussian Schwinger family witness are too coarse for this local obstruction. The efficient representation encodes H,K sheets, endpoint currents, cell moments, sector kernels, counterterms, and recovery errors; preserves gauge, color, reflection, orientation, cutoff, locality, and same-theory identity; uses cumulant expansion, Ward/cusp subtraction, endpoint Taylor remainders, heat-kernel majorants, outward-rounded interval quadrature, and certified zero-pairing quotienting; keeps finite endpoint-cell locality; transfers only through centered flowed Wilson cumulants; and demotes on any falsifier. Hard gate: finite endpoint-box positivity after H,K. Conceptual value signal: R_{++}/kappa_4 is now a route-deciding color-geometric near/far interval certificate rather than a symbolic endpoint term; success promotes one finite Route A gate, failure quarantines this R repair, and all Clay gates remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and interval-scaling guide, not as evidence for the Clay theorem.`
- Rationale: The branch has repeated the need for H_4 constants; a concrete regulator-preserving variation of the near/far split tests whether the endpoint-moment mechanism can plausibly beat L_+ before more abstraction is added.
- Situation seed: Fixed SU(2) Wilson plaquette regulator on a reflected four-torus, fixed H,K collar/hairpin endpoint boxes, gradient-flowed curvature Wilson cumulants, cusp-renormalized thin hairpins, and endpoint sheet-current recovery with outward-rounded interval cells.
- Varied variable: The dimensionless split u=rho/sqrt(t) over a bounded set, with t/eta^2 and the H,K geometry held fixed.
- Held-fixed controls: Same bare Wilson action and same RG trajectory for all Wilson cumulants and counterterms., Same H,K endpoint geometry, reflection convention, plus-channel current, and Schur-Feshbach leakage L_+., Same gradient-flow renormalization scheme, boundary point-splitting convention, and endpoint-cell partition depth., Same pair covariance normalization G_{++}^{I,-} and same recovery-map error protocol.
- Expected observation: If the mechanism is real, H_{near}(u)+H_{far}(u) has a stable interval minimum and yields R_{++}^{I,-}>L_+ on a nonempty flow-time plateau; if not, the lower interval stays negative or unstable under u.
- Transfer certificate needed: A certified same-theory Ward-Hessian interval with zero-pairing recovery audit and cutoff-stable error bounds before the intuition may affect proof obligations or the same-theory nontriviality witness queue.

## Next Experiment

Proof search: instantiate the SU(2) fixed-H,K endpoint cells, compute the plus-current moment table, derive Ward-subtracted 3g/4g/ct/end kernels, and run outward-rounded near/far interval enclosures for u=rho/sqrt(t). Include a validator-facing connected cumulant witness and same-theory nontriviality witness audit only as non-claims; the immediate target is the finite R_{++}^{I,-} >= L_+ promotion or falsifier.

# Raw K4 two-sparse stress witness for the post-H,K Wilson endpoint box

## Candidate Lemma

In a fixed heat-kernel SU(N) cutoff theory, a two-sparse endpoint stress vector with tau_pq(theta)<0 is a valid finite falsifier for Schur-corrected post-H,K endpoint positivity.

## Definitions

- source object: raw heat-kernel regulated Wilson plaquette-sheet data P_sigma, including oriented plaquettes, sheet weights, transporters, color tensors, Gaussian covariance C_sigma, connected K4 intervals, OPE intervals, and the fixed H,K Schur block.
- target object: the finite Hermitian endpoint quadratic form U_sigma on the post-H,K endpoint subspace; it is independently the second-order Wilson Gram correction after Schur-Feshbach elimination, not an OS spectral-gap claim.
- controlled interface: Rec_sigma sums same-regulator plaquette cumulant intervals into R_raw, compresses to endpoint indices p,q, subtracts B^*E^{-1}B, and exposes U_pp^+, U_qq^+, and a phased off-diagonal lower bound L_pq(theta).
- same-theory condition: Wilson action, gauge group, coupling, heat-kernel smearing sigma, finite volume, endpoint Wilson basis, OPE normalization, and H,K Schur data are identical for C_sigma, K4, E_OPE, and S_HK.
- carrier: validator-facing connected cumulant witness, not gauge-invariant observable density, excitation-sector cyclicity, OS Hilbert observable algebra, or a vacuum-orthogonal spectral witness.
- stress pair: p,q are two endpoint Wilson sheet nodes surviving H,K elimination; theta is a certified phase chosen before interval evaluation.

## Assumptions

- Model: four-dimensional Euclidean lattice SU(N) Yang-Mills with heat-kernel regulator and finite endpoint Wilson collar/hairpin geometry.
- Cutoff: a>0, sigma>=c a, finite volume, and finite endpoint box are fixed; no continuum or infinite-volume limit is asserted.
- Same-theory: all intervals, OPE coefficients, Gaussian covariance, and Schur blocks are computed in the same cutoff measure and Wilson normalization.
- Regime: the boundary-OPE expansion is used only inside the endpoint box with an outward-rounded error matrix E_OPE.
- Local: E=QHQ is strictly positive on the eliminated H,K hairpin subspace, so B^*E^{-1}B is a valid finite Schur subtraction.
- Validity: interval arithmetic is outward-rounded and quotients only by exact Wilson trace identities and orientation symmetries.
- Constraint: U_qq^+>0 and L_pq(theta)>0 for the displayed tau test; if U_qq^+<=0, the diagonal itself is already a stress falsifier.

## Equations

- raw endpoint polarization decomposition: `R^{\rm raw}_{ij,\sigma}=\operatorname{cum}_2(:Q_{i,\sigma}^2:,:Q_{j,\sigma}^2:)=\alpha_N g_R^4(C_\sigma\circ C_\sigma)_{ij}+\frac{g_R^4}{16N^2}K_{4,ij,\sigma}+E^{\rm OPE}_{ij,\sigma},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid when Q_i is the heat-kernel transported curvature flux for the same endpoint Wilson sheet and vacuum/perimeter disconnected terms have been subtracted.
- Schur-corrected endpoint matrix: `U_{ij,\sigma}=R^{\rm raw}_{ij,\sigma}-(B^*E^{-1}B)_{ij}`. Valid when: Applies after the finite H,K hairpin block has positive eliminated block E and the endpoint basis is the same Wilson basis used in R_raw.
- phase lower bound: `L_{pq}(\theta)=\underline{\operatorname{Re}\{e^{i\theta}U_{pq,\sigma}\}}`. Valid when: Valid when the interval for U_pq is Hermitian-consistent and theta is fixed before taking the outward-rounded real lower endpoint.
- optimized two-sparse stress margin: `\tau_{pq}(\theta)=U^+_{pp,\sigma}-\frac{L_{pq}(\theta)^2}{U^+_{qq,\sigma}}`. Valid when: Requires positive diagonal upper bound U_qq^+ and a positive phased off-diagonal lower bound from the same regulator interval matrix.
- stress vector upper bound: `x_{pq}(\theta)^*U_\sigma x_{pq}(\theta)\le \tau_{pq}(\theta),\quad x_{pq}(\theta)=e_p-e^{i\theta}\frac{L_{pq}(\theta)}{U^+_{qq,\sigma}}e_q`. Valid when: Valid for the two-dimensional principal compression on p,q after replacing U_pp, U_qq, and the phased off-diagonal by certified interval bounds.
- raw K4 demotion threshold: `\underline K^{\theta}_{4,pq,\sigma}>\frac{16N^2}{g_R^4}\left(\sqrt{U^+_{pp,\sigma}U^+_{qq,\sigma}}-\operatorname{Re}(e^{i\theta}(G_{pq,\sigma}-S_{pq}))+e^{\rm OPE}_{pq,\sigma}\right)\Rightarrow \tau_{pq}(\theta)<0`. Valid when: Applies when G is the Gaussian color-square contribution, S is the exact Schur subtraction, and K4 is the same-regulator phased connected four-curvature cumulant interval.

## Attempted Derivation

- Attack conceptual pressure: turn the connected boundary-OPE polarization into a route-deciding finite witness rather than another symbolic R or OS-density restatement.
- Declarative tension: Wilson/OPE coefficients, connected K4 intervals, OPE errors, and H,K Schur subtraction must jointly control one endpoint quadratic form in a single cutoff theory, while continuum existence, OS/Wightman reconstruction, gauge-invariant observable density, and the Clay mass gap remain non-claims.
- Carrier audit: scalar R is too weak and representation-limited; OS Hilbert observable algebra and excitation-sector cyclicity are too strong and circular for this local gate; shell A012 compression was convenient but quarantined; raw plaquette enumeration is fragmented yet valid.
- Compare routes: full Delta_raw matrix proof is complete but expensive; the two-sparse stress route is sharper as a negative tactic because three same-regulator intervals can already demote the H,K endpoint route.
- Fix heat-kernel SU(N) cutoff data, endpoint sheets, and the finite H,K Schur block E>0.
- Use Wilson boundary-OPE cancellation: vacuum and perimeter disconnected pieces are removed by normal ordering, leaving the Gaussian color Hadamard square plus connected four-curvature cumulant K4 and an OPE interval.
- Assemble U_sigma=R_raw-B^*E^{-1}B on endpoint nodes; preserve gauge invariance by transported curvature contractions and exact Wilson quotienting only.
- For a candidate pair p,q and phase theta, compute U_pp^+, U_qq^+, and L_pq(theta)=lower Re(e^{i theta}U_pq).
- Choose x=e_p-e^{i theta}(L_pq/U_qq^+)e_q; interval arithmetic gives x^*U x<=U_pp^+-L_pq^2/U_qq^+.
- Hard gate: tau_pq(theta)<0 is a valid finite falsifier for endpoint PSD; if all such tests survive, the proof state moves to full Delta_raw Loewner/Gershgorin proof search, not to Clay-level spectral transfer.

Blocking gap: The same-regulator raw K4 intervals for the chosen endpoint pair p,q and the corresponding diagonal K4 intervals have not yet been computed; without them tau_pq(theta) cannot be numerically signed.

## Falsifiers

- A certified tau_pq(theta)<0 is a falsifier for the worked H,K endpoint positivity route.
- Regulator mismatch between K4 intervals, OPE bounds, Gaussian covariance, and Schur block makes the stress test invalid.
- Intervals so wide that L_pq(theta)<=0 for every phase leave the negative tactic inconclusive and demote to raw interval refinement.
- A non-invariant quotient that changes K4_pq under Wilson trace identities invalidates the connected cumulant witness.
- If full Delta_Gersh remains negative after interval refinement, the finite collar/hairpin endpoint route is killed even without a two-sparse stress.

## Learning

Cycle 304 converts the promoted tau test into an explicit raw-K4 interval recipe: the first calculable demotion bound is an off-diagonal phased K4 lower interval exceeding the Gaussian-Schur-OPE threshold relative to the two diagonal upper intervals. This is sharp at finite scope because it decides only the post-H,K endpoint-box positivity gate and leaves every Clay-level Yang-Mills gate untouched.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch has exhausted abstraction-level R/K4 restatements; it now needs a concrete same-regulator stress computation to decide whether the finite H,K endpoint route survives.
- Situation seed: Finite SU(3) heat-kernel lattice YM endpoint box with the fixed H,K collar/hairpin basis, two endpoint Wilson sheet nodes p and q sharing a boundary plaquette strip, and raw connected four-curvature cumulant intervals computed by plaquette quadruple enumeration.
- Varied variable: smearing ratio beta=sigma/a over a small certified set, with theta chosen from the finite phase set after each beta interval is assembled.
- Held-fixed controls: Gauge group SU(3), lattice action, finite volume, coupling g_R, endpoint Wilson basis, and H,K Schur block., Exact Wilson trace quotient policy, outward-rounded interval arithmetic, same OPE normalization, and no continuum or OS spectral-transfer conclusion.
- Expected observation: For some beta the off-diagonal connected K4 phased lower bound either exceeds the threshold and gives tau_pq(theta)<0, or it remains below threshold and forces full Delta_raw proof search.
- Transfer certificate needed: A validator-facing certificate listing U_pp^+, U_qq^+, L_pq(theta), the raw K4 plaquette intervals used, the OPE error, the Schur block, and a same-theory audit before the intuition may affect proof obligations.

## Next Experiment

Proof search: compute the connected cumulant witness intervals K4_pp, K4_qq, and K4_pq(theta) for the first endpoint pair in the heat-kernel SU(3) H,K box, then evaluate tau_pq(theta); do not revisit gauge-invariant observable density or OS Hilbert observable algebra unless this finite route is quarantined.

