# cycle-0279

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint-source interval certificate for the post-H,K reflected-Wilson gate

## Candidate Lemma

Finite endpoint clipping lemma: for the computed three-hairpin H,K block in the heat-kernel plaquette-sheet regulator, the post-H,K gate is certified by a scalar interval in which only endpoint boxes with positive 12-only null incidence can lower the Schur-Feshbach margin.

## Definitions

- source object: the regulated endpoint source carrier C_ep(a,epsilon), consisting of endpoint boxes v, seven heat-kernel source values log Z_v(ell h), beta intervals for -kappa_{4,v}^{sing}, binary footprint incidences b_{ij}(v), color factor C_N, Gaussian margin interval M_G, and tail interval T_tail.
- target object: the finite post-H,K reflected-Wilson OS transfer gate for the locked three-hairpin block, namely positivity of the Schur-Feshbach null scalar after endpoint collapse.
- controlled interface: source differentiation and interval arithmetic map C_ep to one gate interval [I_-,I_+] without changing Wilson normalization, reflection, the null vector, or the gauge-invariant observable algebra.
- same-theory condition: every endpoint source derivative is computed from the same heat-kernel plaquette-sheet Wilson measure and the same Wilson loop recovery map used before collar collapse; no boundary counterterm, algebra enlargement, or altered loop renormalization is allowed.
- carrier critique: raw R is representation-limited because it forgets incidence signs, while a raw kappa_4 spectrum is too strong because it treats protective endpoint boxes as dangerous.
- efficient representation: encode endpoint boxes, source stencils, beta intervals, incidences, C_N, M_G, and T_tail; preserve Wilson normalization, reflection symmetry, null cancellations, cutoff bookkeeping, and same-theory observables; primitive operations are source differentiation, interval enclosure, color multiplication, incidence clipping, and tail addition; equivalence is equality of regulated source data; locality cost is charged to T_tail; the transfer interface exports only [I_-,I_+].

## Assumptions

- Model: four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette action and plaquette-sheet Wilson approximants for the three reflected hairpins.
- Regime: fixed finite collar/hairpin geometry after H,K have been computed, with endpoint boxes small compared with segment lengths but larger than the lattice spacing.
- Cutoff: beta, M_G, and T_tail intervals are uniform along the cutoff-removal subsequence used for the finite Wilson block.
- Same-theory: the source perturbations are auxiliary derivatives of the locked Wilson observables and are set to zero after differentiation, so they do not define a new boundary theory.
- Validity: Wick-square Gram terms and straight f f contacts have already been removed by the connected log and the null-incidence cancellation; the lemma only bounds the residual endpoint/corner contribution.
- Constraint: beta_v=-kappa_{4,v}^{sing} is nonnegative in the compact-group endpoint box enclosure; if an interval crosses zero, use its full signed interval rather than the clipped simplified formula.

## Equations

- binary endpoint incidence: `D_v=2b_{12}(v)-4b_{13}(v)-4b_{23}(v),\qquad b_{ij}(v)\in\{0,1\}`. Valid when: Valid when endpoint boxes are assigned binary membership in the three pairwise Wilson footprint overlaps after the fixed H,K null vector has been chosen.
- seven point endpoint fourth cumulant: `\kappa_{4,v}^{\rm sing}=h^{-4}\sum_{\ell=-3}^{3}w_\ell\log Z_v(\ell h)+E_{8,v},\quad (w_0,w_{\pm1},w_{\pm2},w_{\pm3})=(28/3,-13/2,2,-1/6),\quad |E_{8,v}|\le 7h^4M_{8,v}/240`. Valid when: Applies when log Z_v(s) is eight times differentiable for the endpoint source direction and the heat-kernel box measure gives a uniform eighth-derivative bound.
- clipped gate lower interval: `I_- = M_G^- - C_N\sum_v \beta_v^+\,[D_v^+]_+ - T_{\rm tail}^+`. Valid when: Valid when beta_v=-kappa_{4,v}^{sing} is enclosed by [beta_v^-,beta_v^+] and all non-endpoint or overlap-leakage contributions are included in T_tail.
- promotion and falsifier tests: `I_->0\Rightarrow \text{finite block promoted},\qquad I_+<0\Rightarrow \text{finite same\mbox{-}theory falsifier}`. Valid when: Requires the preceding interval enclosure, the same-theory source policy, and cutoff-uniform error bounds for every endpoint box and tail term.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: the regulated endpoint source carrier C_ep(a,epsilon), consisting of endpoint boxes v, seven heat-kernel source values log Z_v(ell h), beta intervals for -kappa_{4,v}^{sing}, binary footprint incidences b_{ij}(v), color factor C_N, Gaussian margin interval M_G, and tail interval T_tail.; target object: the finite post-H,K reflected-Wilson OS transfer gate for the locked three-hairpin block, namely positivity of the Schur-Feshbach null scalar after endpoint collapse.; Model: four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette action and plaquette-sheet Wilson approximants for the three reflected hairpins..
- Attack conceptual pressure: endpoint collapse must be sign-certified while preserving collar OS positivity and the fixed gauge-invariant Wilson theory; the missing mediator is a cutoff-uniform endpoint source carrier rather than a symbolic R.
- Start from the finite Schur-Feshbach post-H,K scalar gate for the already computed three-hairpin null channel; do not change H,K or the Wilson algebra.
- Use the connected endpoint log Z_v to remove disconnected Wick-square pieces; use the known null-incidence identity to cancel straight-segment C_A f f contacts.
- Represent the remaining singlet connected four-flux endpoint cumulant by the seven-point fourth-derivative stencil with eighth-derivative error 7h^4M8/240.
- Set beta_v=-kappa_{4,v}^{sing}; compact-group endpoint curvature gives beta_v>=0 in the small-box enclosure, so the sign of each endpoint contribution is controlled by D_v=2b12-4b13-4b23.
- Compute the binary incidence table; only b=(1,0,0) has D_v>0, hence only 12-only endpoint dominance can lower the gate, while all boxes touching 13 or 23 are protective or neutral up to T_tail.
- Aggregate endpoint boxes into I_-=M_G^- - C_N sum beta_v^+[D_v^+]_+ - T_tail^+ and I_+=M_G^+ + C_N sum beta_v^+[-D_v^-]_+ + T_tail^+ for decision.
- Hard gate changed: the finite post-H,K reflected-Wilson OS transfer gate becomes a finite interval check; success promotes this block, failure gives a concrete same-theory falsifier. Clay continuum construction, full OS/Wightman reconstruction, nontriviality, and mass gap remain untouched.

Blocking gap: Actual cutoff-uniform beta_v intervals, eighth-derivative bounds M8_v, endpoint incidence leakage estimates, and T_tail are not yet computed for the concrete plaquette-sheet endpoint partition.

## Falsifiers

- falsifier: a certified 12-only endpoint family with I_+<0 gives a finite same-theory OS obstruction for this hairpin block.
- falsifier: T_tail is not cutoff-uniform or scales like the Gaussian margin, so endpoint locality is too weak for a valid certificate.
- falsifier: the source recovery map leaves a boundary counterterm or source-dependent Wilson normalization at s=0, changing the theory.
- falsifier: endpoint boxes cannot be made binary or interval-controlled; incidence leakage then invalidates the clipped support claim.
- falsifier: the compact-group beta interval crosses sign with large uncertainty, forcing the crude full interval to include negative gate values.

## Learning

Cycle 279 makes the clipped endpoint source carrier decision-grade. The declarative tension is now precise: finite collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE can coexist only if endpoint source derivatives produce a cutoff-uniform interval that does not require a boundary theory. Raw R is too weak and raw kappa_4 is too strong; C_ep is sharper because it records incidence signs. The conceptual value signal is route-changing at finite scope: negative compact-group kappa_4 is not the falsifier; only certified 12-only endpoint dominance plus uncontrolled tail is. This changes the finite post-H,K reflected-Wilson OS gate and leaves all Clay-level continuum and mass-gap gates untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and endpoint-data design guide.`
- Rationale: The branch has reduced the abstract Wilson/OS obstruction to a finite endpoint interval; another abstract restatement would not decide whether 12-only endpoint dominance can actually defeat the positive Schur-Feshbach margin.
- Situation seed: Heat-kernel SU(N) plaquette-sheet three-hairpin block with the fixed H,K null vector; endpoint boxes are partitioned into 12-only, 13-touching, 23-touching, mixed, and tail boxes, and log Z_v(s) is sampled by the seven-point fourth-derivative stencil.
- Varied variable: The 12-only endpoint dominance ratio eta = (sum_{v:b=(1,0,0)} beta_v)/(M_G/C_N), with all protective endpoint boxes and H,K data held fixed.
- Held-fixed controls: Same regulated Wilson loops, reflection map, heat-kernel plaquette action, and source recovery map., Fixed three-hairpin H,K block, null vector, color factor C_N, and collar geometry., Cutoff-uniform derivative error rule 7h^4M8/240 and a declared tail budget T_tail., No boundary counterterm, no observable-algebra enlargement, and no change of Wilson normalization.
- Expected observation: There should be a sharp eta threshold: below it I_->0 promotes the finite block; above it I_+<0 supplies a same-theory finite falsifier; near threshold the decisive data are M8 and T_tail, not the sign of raw kappa_4.
- Transfer certificate needed: A regulator-level interval certificate for every endpoint beta_v, binary or interval incidence D_v, and T_tail, plus verification that the source derivatives recover the original Wilson Schwinger functional at s=0.

## Next Experiment

Compute the endpoint source interval table for the concrete plaquette-sheet partition: list b(v), evaluate or bound the seven log Z_v(ell h) values, enclose beta_v and M8_v, add T_tail, and decide the sign of [I_-,I_+].

# Gauge-invariant endpoint mediator for finite H,K Route A

## Candidate Lemma

Finite endpoint-box certificate: for fixed SU(N) Wilson regulator, gradient flow time t>0, and the H,K plus hairpin endpoint geometry, the post-H,K correction R_{++}^{ren} has a computable lower interval from a positive pair contraction minus a Ward-subtracted connected four-curvature Hessian bound. If this lower interval beats the Schur-Feshbach leakage L_+, finite endpoint-box positivity is promoted; otherwise this R repair is falsified. This is a local finite theorem and not a Clay mass-gap claim.

## Definitions

- source object: the finite-volume hypercubic SU(N) Wilson lattice measure at spacing a, gradient-flowed gauge field B_t, reflected H,K plus-channel hairpin sheet currents, and centered perimeter/cusp-subtracted Wilson observables.
- target object: the scalar post-H,K endpoint-box Schur-Feshbach plus entry Q_+^{end}, equivalently the sign certificate R_{++}^{ren}-L_+ for the finite reflected Wilson cone.
- controlled interface: sheet-current and endpoint-current representation of the flowed Wilson covariance, preserving gauge invariance, color contractions, reflection parity, orientation, and endpoint locality.
- same-theory condition: all pair contractions, connected cumulants, counterterms, flow maps, and comparisons with L_+ are computed in the same cutoff Wilson theory and along the same cutoff-removal candidate family.
- Endpoint box E_z is z+[-ell,ell]^4; d is the separation to the reflected endpoint box; eta=ell/d.
- rho_+ is the signed plus-channel endpoint current obtained after replacing raw Wilson contours by oriented sheet-boundary currents.
- H_4^I is an interval enclosure for the Hessian norm of the Ward- and cusp-subtracted connected four-curvature kernel on E_z^4.
- L_+ is the finite Schur-Feshbach leakage term already isolated from -B_{KR}D^{-1}B_{RK} in the plus channel.

## Assumptions

- Model: finite-volume SU(N) Wilson lattice gauge theory with compact link variables, Wilson action, reflection plane fixed, and gauge-invariant gradient flow B_t at t>0.
- Regime: endpoint boxes are disjoint and separated, d>=4ell+4sqrt(8t), eta<=1/8, with the rest of the H,K collar geometry held fixed.
- Cutoff: a<epsilon<ell at point splitting, epsilon is removed at fixed a,L,t after one-hairpin perimeter/cusp subtraction; cutoff-uniformity is an extra obligation, not assumed for Clay transfer.
- Same-theory: the covariance defining R_{++}^{ren} and the finite matrix giving L_+ use the same Wilson measure, reflection, flow time, normalization, and observable algebra.
- Validity: the cumulant expansion is used only with a certified sixth-and-higher remainder E_6^I, so the displayed inequality is a finite regulated certificate.
- Local: the conclusion changes only the finite endpoint-box positivity gate after H,K; continuum existence, OS positivity in the limit, nontriviality, and Hamiltonian mass gap remain untouched.

## Equations

- regulated endpoint covariance: `R_{++}^{ren}(a,L,t)=\lim_{\epsilon\downarrow0}\kappa_2\big(:W_{h_+}^{t,\epsilon}:_{pc},:\Theta W_{h_+}^{t,\epsilon}:_{pc}\big)_{\Lambda,a}`. Valid when: Valid when the flowed reflected hairpin Wilson observables are centered and perimeter/cusp subtracted in the same finite Wilson theory.
- pair-plus-polarization decomposition: `R_{++}^{ren}=g_t^4 (N^2-1)\{2\mathcal G_{++}+N C_{4,++}^{WS}\}+E_6`. Valid when: Valid in the small-sheet cumulant expansion after disconnected products, one-hairpin counterterms, and Ward descendants have been subtracted.
- plus endpoint moment cancellation: `\int_{E_z}\rho_+(u)\,du=0,\qquad \int_{E_z}(u-z)_i\rho_+(u)\,du=0`. Valid when: Valid when the H,K plus hairpin endpoint currents are represented by oriented sheet boundaries with reflection-symmetric charges.
- Ward-subtracted Hessian enclosure: `|C_{4,++}^{WS}|\le H_4^{I,+}(t,d,\ell)\,M_{2,+}^2,\qquad M_{2,+}=\int_{E_z}|u-z|^2|\rho_+(u)|\,du`. Valid when: Applies after endpoint Taylor expansion on separated boxes and after monopole and dipole moments vanish exactly.
- lower interval for endpoint mediator: `R_{++}^{I,-}=g_t^4 (N^2-1)\big(2\mathcal G_{++}^{I,-}-N H_4^{I,+}M_{2,+}^2\big)-E_6^{I,+}`. Valid when: Valid when interval enclosures for the pair kernel, Hessian kernel, moments, and truncation remainder are certified simultaneously.
- finite promotion inequality: `R_{++}^{I,-}>L_+ + \Delta_{int}\ \Longrightarrow\ Q_+^{end}>0`. Valid when: Requires the same finite Schur-Feshbach normalization for L_+ and the same Wilson-cumulant normalization for R_{++}^{ren}.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: the finite-volume hypercubic SU(N) Wilson lattice measure at spacing a, gradient-flowed gauge field B_t, reflected H,K plus-channel hairpin sheet currents, and centered perimeter/cusp-subtracted Wilson observables.; target object: the scalar post-H,K endpoint-box Schur-Feshbach plus entry Q_+^{end}, equivalently the sign certificate R_{++}^{ren}-L_+ for the finite reflected Wilson cone.; Model: finite-volume SU(N) Wilson lattice gauge theory with compact link variables, Wilson action, reflection plane fixed, and gauge-invariant gradient flow B_t at t>0..
- Conceptual pressure attacked: finite Schur-Feshbach positivity, positive flowed pair covariance, and same-theory Wilson renormalization must jointly hold, but connected four-curvature polarization can erase the pair term.
- Declarative tension: raw Wilson contours give gauge-invariant observables but are fragmented for endpoint cancellation; global non-Gaussian OS witnesses are too coarse; endpoint sheet currents are the efficient carrier because Ward moments, color contractions, and interval Hessians become primitive.
- Fix the regulator: SU(N) Wilson lattice on finite volume, gradient flow t>0, boundary point splitting epsilon, reflected H,K plus hairpin endpoint boxes, and same-theory perimeter/cusp subtraction.
- Rewrite the plus hairpin as oriented sheet current plus endpoint current rho_+, keeping gauge, color, reflection, orientation, and same-theory invariants.
- Expand the centered flowed Wilson covariance through the kappa_4 endpoint term: disconnected products cancel, one-hairpin perimeter/cusp terms cancel, and the cross-pairing yields color factor 2(N^2-1) times the positive geometric pairing G_{++}.
- Separate the connected four-curvature remainder with color factor N(N^2-1) into K_4^{WS}; the Ward-subtracted endpoint kernel is the only possible sign-changing carrier.
- Use plus-channel endpoint moments: monopole and dipole vanish, so Taylor expansion of K_4^{WS} on endpoint cells starts at the Hessian remainder.
- Bound the remainder by H_4^{I,+}M_{2,+}^2 and form the lower interval R_{++}^{I,-}=g_t^4(N^2-1)(2G_{++}^{I,-}-NH_4^{I,+}M_{2,+}^2)-E_6^{I,+}.
- Compare R_{++}^{I,-} with the already isolated Schur-Feshbach leakage L_+; a strict positive margin promotes the finite endpoint-box gate, while failure is a falsifier for this local repair.

Blocking gap: No certified numerical or analytic interval is yet available for H_4^{I,+}, E_6^{I,+}, and G_{++}^{I,-} in the actual H,K endpoint geometry with cutoff-refinement stress tests.

## Falsifiers

- Ward moment falsifier: the oriented endpoint-current representation leaves a nonzero monopole or dipole moment, invalidating the Hessian suppression.
- Cusp falsifier: one-hairpin cusp or perimeter subtraction leaves an endpoint logarithm that is not absorbed in the same Wilson observable normalization.
- Size falsifier: NH_4^{I,+}M_{2,+}^2+E_6^{I,+} exceeds 2G_{++}^{I,-} before comparison with L_+.
- Leakage falsifier: the lower interval R_{++}^{I,-} is positive but does not beat the finite Schur-Feshbach leakage L_+.
- Regulator falsifier: the interval is valid at one cutoff but widens or changes sign under a->0 or L->infty refinement.
- Geometry falsifier: the actual H,K plus endpoint current has zero or near-zero G_{++}^{I,-}, so the positive pair baseline cannot carry the endpoint repair.

## Learning

Cycle 279 refits the carrier from raw Wilson contours to endpoint sheet currents and turns the connected boundary-OPE polarization into a Hessian interval problem. The sharp contribution is the explicit lower interval R_{++}^{I,-}=g_t^4(N^2-1)(2G_{++}^{I,-}-NH_4^{I,+}M_{2,+}^2)-E_6^{I,+} with Ward/cusp and plus-moment cancellations named. This is valuable because it gives a valid finite falsifier and promotion test for endpoint-box positivity without implying the Clay theorem.

## Gedanken Experiment Design Seed

- Need decision: `Design and run as a falsifier probe before any promotion of the endpoint mediator lemma.`
- Rationale: The branch needs a concrete target-preserving stress test because repeated abstract formulations already isolated R_{++}; the next proof-state change depends on whether the Hessian lower interval can plausibly beat L_+ in the actual H,K geometry.
- Situation seed: Finite SU(2) Wilson lattice on a reflected four-torus with the fixed H,K plus hairpin endpoint boxes, gradient flow time t, centered perimeter/cusp-subtracted thin Wilson hairpins, and interval arithmetic for the Ward-subtracted four-curvature kernel on endpoint cells.
- Varied variable: eta=ell/d, the endpoint-cell size divided by reflected endpoint separation, varied through eta in {1/16,1/12,1/8} with flow ratio sqrt(8t)/ell held fixed.
- Held-fixed controls: Same Wilson action, gauge group, reflection plane, H,K sheet-current geometry, and Schur-Feshbach leakage L_+., Same gradient-flow definition, perimeter/cusp counterterm scheme, endpoint-current orientation convention, and interval cell partition rule., Same color normalization so the pair term has factor 2(N^2-1) and the connected polarization has factor N(N^2-1).
- Expected observation: If the moment mechanism is real, the ratio |C_{4,++}^{WS}|/G_{++} scales like O(eta^2) or better while G_{++} remains positive, producing a stable lower interval for small eta. If the ratio stays O(1) or changes sign wildly, the endpoint Hessian repair is demoted.
- Transfer certificate needed: A certified Ward/cusp cancellation log, interval enclosures for G_{++}, H_4, and E_6, and cutoff/volume refinement showing the same-theory flowed Wilson cumulant remains valid before any continuum or OS-spectral obligation is affected.

## Next Experiment

Build the actual H,K endpoint-current cell list, compute M_{2,+} exactly from oriented cells, interval-enclose G_{++}^{I,-} with the flowed two-curvature kernel, then bound H_4^{I,+} for K_4^{WS}; stop immediately if R_{++}^{I,-} cannot beat L_+.

# Same-regulator kappa4 shell interval for the post-H,K endpoint term

## Candidate Lemma

Finite Route A shell certificate: for a heat-kernel regulated finite reflected endpoint box, the Schur-corrected endpoint form is positive if the Gaussian Wilson square margin dominates the compressed negative four-curvature cumulant shell envelope, the OPE interval, and the H,K hairpin Schur energy.

## Definitions

- source object: normalized reflected Wilson endpoint observables in the heat-kernel SU(N) lattice regulator at cutoff a, smoothing sigma, finite box B, and fixed collar/hairpin geometry H,K.
- target object: the finite endpoint quadratic form Q_sigma=R_sigma-S_HK on the vacuum-subtracted Wilson endpoint span, not a continuum Hamiltonian spectral gap.
- controlled interface: the sheet-kernel hypergraph recovery map Rec_sigma sending plaquette sheets, transporters, color tensors, shell labels, and multiplicities to the matrix entries of R_sigma and to interval bounds for K4_sigma.
- same-theory condition: all Wilson loops, transported curvature fluxes, cumulants, OPE remainders, coupling g_R, reflection operation, and Schur data are computed in the same cutoff theory with the same normalization.

## Assumptions

- Model: four-dimensional finite-volume lattice SU(N) Yang-Mills with heat-kernel plaquette action and reflection plane separating paired endpoint boxes.
- Cutoff: a>0 and sigma>=a are fixed before any endpoint compression; no continuum or volume-uniform claim is made.
- Regime: the Wilson boundary OPE is used only inside the finite endpoint collar, with a certified remainder interval E_OPE(sigma).
- Same-theory: S_HK=B_v^*E_v^{-1}B_v is formed from the same reflected Wilson Gram matrix as R_sigma.
- Local: the endpoint basis is finite and quotienting uses only Wilson trace identities and reflection-preserving sheet symmetries.
- Validity: shell amplitudes A_l(sigma) are certified upper bounds for the absolute row sums of the compressed connected four-curvature cumulant in shell l.

## Equations

- connected-polarization-decomposition: `R_\sigma=\alpha_N g_R^4\,(C_\sigma\circ C_\sigma)+\frac{g_R^4}{16N^2}K_{4,\sigma}+E_{\mathrm{OPE},\sigma},\qquad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid when normalized reflected Wilson endpoint observables are expanded through the boundary OPE in the fixed heat-kernel cutoff theory.
- four-curvature-shell-envelope: `A_\ell(\sigma)=\max_i\sum_{j:\,d_{\mathrm{sh}}(i,j)=\ell}\left|\left(K_{4,\sigma}\right)_{ij}\right|,\qquad M^-_{4,\sigma}\le \sum_\ell A_\ell(\sigma)`. Valid when: Applies after endpoint compression and shell quotienting preserve all Wilson trace and reflection symmetries of K4_sigma.
- schur-corrected-margin: `\lambda_{\min}(R_\sigma-S_{HK})\ge m_G(\sigma)-\frac{g_R^4}{16N^2}\sum_\ell A_\ell(\sigma)-e_{\mathrm{OPE}}(\sigma)-s_{HK}(\sigma)=:\Delta_\sigma`. Valid when: Requires the same-regulator Gaussian margin, certified shell envelopes, OPE interval, and H,K Schur energy in one finite endpoint basis.
- promotion-criterion: `\Delta_\sigma>0\ \Longrightarrow\ R_\sigma-S_{HK}\succ 0\ \text{on the endpoint span}`. Valid when: Valid only for the finite compressed Wilson endpoint problem and not for continuum OS spectral transfer.

## Attempted Derivation

- Conceptual pressure attacked: mediate actual connected Wilson cumulants to Schur-corrected endpoint positivity without inflating a finite Wilson calculation into the Clay mass-gap theorem.
- Declarative tension: Wilson/OPE coefficients, connected kappa4 negativity, OPE errors, and H,K Schur energy must be valid in one cutoff theory, while continuum OS reconstruction, observable density, and physical-unit spectral transfer stay quarantined.
- Freeze the Clay claim level: the source is a finite heat-kernel Wilson endpoint calculation; the target is finite positivity of R_sigma-S_HK; the untouched gates are continuum existence, OS/Wightman axioms, nontriviality, and Hamiltonian mass gap.
- Expand the same-regulator normalized Wilson endpoint observables through transported curvature fluxes Phi_p^a; vacuum and perimeter normalization cancel disconnected and one-sided terms before compression.
- Evaluate crossed two-flux contractions using tr(T^aT^b)=delta^{ab}/2 and the reflected covariance C_{pq,sigma}; the resulting Gaussian matrix is alpha_N g_R^4(C_sigma o C_sigma), hence PSD by the Schur product theorem on the finite endpoint span.
- Isolate the non-Gaussian connected four-curvature term K4_sigma with color tensor T_N^{abcd}; compress it in the same endpoint basis and bound its negative spectral size by Gershgorin shell row sums A_l(sigma).
- Subtract the already finite Schur-Feshbach hairpin energy S_HK and the certified OPE interval to obtain Delta_sigma as a lower bound for lambda_min(R_sigma-S_HK).
- Hard gate: Delta_sigma>0 promotes only finite endpoint-box positivity; Delta_sigma<=0 is a valid falsifier locating failure in kappa4, OPE error, or hairpin coupling.

Blocking gap: The first shell amplitudes A_l(sigma) have not yet been certified from the actual heat-kernel Yang-Mills measure; a rigorous bound must control connected four-curvature cumulants with color transporters and large-field tails in the finite box.

## Falsifiers

- falsifier: a certified negative eigenvector of K4_sigma whose magnitude exceeds the Gaussian margin after H,K Schur subtraction.
- falsifier: quotienting the sheet-kernel hypergraph by a non-Wilson symmetry changes a row sum A_l(sigma) or the recovered Delta_sigma.
- falsifier: the OPE interval is not small at sigma/a in the endpoint collar, so R_sigma cannot be separated into Gaussian plus K4 plus controlled error.
- falsifier: S_HK computed from the same Gram matrix has an endpoint row sum larger than the claimed margin.
- Stress case: near-rough fields at small beta produce nondecaying shell amplitudes, making the finite endpoint certificate fail without contradicting the Clay target.

## Learning

Cycle 279 moves from aspirational R/kappa4 language to a finite shell-envelope theorem with an explicit lower bound Delta_sigma. The conceptual value signal is sharp and explanatory: the unknown boundary-OPE polarization is decomposed into a PSD Gaussian color square, one compressed connected four-curvature operator, an OPE interval, and the H,K Schur subtraction. The current carrier audit says scalar R is representation-limited, OS density is too strong and circular for this local gate, and raw plaquette enumeration is fragmented; the sheet-kernel hypergraph is retained because it preserves color, geometry, locality, cumulant cancellation, and recovery maps. This changes only the finite Route A endpoint-box gate and remains valuable because success or failure decides whether the worked Wilson collar/hairpin calculation deserves promotion without implying the Clay theorem.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the first same-regulator shell interval.`
- Rationale: The branch has repeated the Delta_sigma form; it now needs a concrete finite-regulator stress test for whether A_l(sigma) can plausibly be bounded before more abstraction is useful.
- Situation seed: Finite SU(2) heat-kernel lattice Yang-Mills on a reflected 4D torus with one fixed H,K endpoint collar/hairpin geometry; compute the connected four-plaquette curvature cumulant between two reflected boundary sheets after Wilson normalization and perimeter cancellation.
- Varied variable: rho=sigma/a, the heat-kernel smoothing-to-lattice ratio controlling boundary OPE locality and shell decay.
- Held-fixed controls: Same endpoint Wilson basis, H,K Schur blocks, and reflection plane., Same heat-kernel action, coupling beta, volume, and perimeter normalization for all cumulants., Same sheet-kernel hypergraph quotient policy and color-trace convention., No change of theory to a Gaussian surrogate or continuum OS reconstruction.
- Expected observation: If the route is viable, A_l(rho) decays across shells fast enough that m_G(rho)-g_R^4 sum_l A_l(rho)/(16N^2)-e_OPE(rho)-s_HK(rho) becomes positive on a rho interval; if not, the first few shells already force Delta_sigma<=0.
- Transfer certificate needed: A reflection-positive same-regulator cumulant computation or certified interval arithmetic proving that the measured or bounded A_l(rho) enclosures are rigorous for the finite heat-kernel Yang-Mills measure before they enter the proof queue.

## Next Experiment

Compute the first same-regulator shell amplitude A_0(sigma) for the fixed H,K endpoint box: enumerate reflected plaquette-sheet quadruples, attach transporters and SU(N) color tensors, subtract disconnected cumulants after Wilson normalization, and test whether the resulting interval already determines the sign of Delta_sigma.

