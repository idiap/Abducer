# cycle-0284

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: fractional endpoint source gate

## Candidate Lemma

Fractional half-overlap endpoint shield: in the heat-kernel plaquette-sheet regulator, the post-H,K null-channel endpoint contribution is certified nonnegative whenever the Gaussian Schur-Feshbach margin exceeds the clipped 12-dominant endpoint interval; endpoint boxes with b13+b23 >= b12/2 cannot be the negative kappa4 falsifier.

## Definitions

- source object: regulated SU(N) heat-kernel plaquette-sheet endpoint boxes v carrying same-theory Wilson source functions Z_v(s) for the three reflected hairpin pairings 12,13,23.
- target object: the finite post-H,K Schur-Feshbach null scalar for the locked three-hairpin Wilson OS block, not the continuum YM mass gap theorem.
- controlled interface: the carrier C_ep=(Z_v, beta_v, b_{12,v},b_{13,v},b_{23,v},C_N,M_G,T_tail) maps endpoint source intervals to one scalar interval [I_-,I_+] for the finite OS gate.
- same-theory condition: sources differentiate the original regulated Wilson observables and no boundary counterterm, algebra enlargement, or endpoint state is introduced during collar collapse.
- Endpoint cumulant beta_v=-d_s^4 log Z_v(0) is represented by a certified interval [beta_v^-,beta_v^+] with beta_v^- >=0 after subtracting Wick-square pieces.
- Fractional incidence b_{ij,v} is the normalized overlap of endpoint box v with the connected boundary-OPE source for reflected hairpin pair ij; D_v=2b_{12,v}-4b_{13,v}-4b_{23,v}.
- The hard gate changed is the finite post-H,K reflected-Wilson OS transfer gate; success promotes this finite block, failure gives a finite same-theory falsifier, and Clay continuum existence plus mass gap remain untouched.

## Assumptions

- Model: four-dimensional Euclidean SU(N) lattice Yang-Mills with heat-kernel plaquette action and gauge-invariant Wilson hairpin observables before cutoff removal.
- Regime: fixed finite three-hairpin collar block after the H,K Schur-Feshbach reduction, with endpoint boxes smaller than the collar scale but larger than the plaquette cutoff.
- Cutoff: beta_v, b_ij,v, and T_tail have regulator-uniform intervals along the chosen refinement subsequence.
- Same-theory: the source derivative d_s^4 log Z_v is computed inside the same Wilson observable algebra and the same reflection-positive lattice measure.
- Validity: Wick-square Gram contributions are removed by connected logarithms, and straight f f contacts cancel by the previously verified null-incidence identity.
- Local: all non-endpoint and unresolved corner interactions are charged to T_tail with a signed interval, not silently discarded.
- Constraint: no claim is made about volume-uniform basin entry, regulator-independent continuum Schwinger functions, OS density, spectral transfer, nontriviality, or positive Hamiltonian mass gap.

## Equations

- fractional_endpoint_dominance: `D_v=2b_{12,v}-4b_{13,v}-4b_{23,v}=2\bigl(b_{12,v}-2(b_{13,v}+b_{23,v})\bigr)`. Valid when: Valid when fractional incidences are measured from the same heat-kernel endpoint box decomposition used for the three reflected Wilson pairings.
- half_overlap_shield: `b_{13,v}+b_{23,v}\ge {1\over 2}b_{12,v}\quad\Longrightarrow\quad [D_v]_+=0`. Valid when: Valid when the endpoint box has nonnegative normalized incidences and the null-channel weights are exactly 2,-4,-4 after H,K reduction.
- adversarial_lower_gate: `I_-=M_G^- - C_N^+\sum_v \beta_v^+[D_v^+]_+ - T_{tail}^+`. Valid when: Valid when beta_v bounds the negative connected fourth endpoint cumulant and protective negative-D_v contributions are intentionally ignored.
- promotion_demote_interval: `I_-\ge0\Rightarrow \text{finite block promoted},\qquad I_+<0\Rightarrow \text{finite same\mbox{-}theory falsifier}`. Valid when: Valid when the scalar interval encloses the complete endpoint, corner, and tail contribution to the Schur-Feshbach null gate.

## Attempted Derivation

- Start from the post-H,K null scalar after prior cancellations: Gaussian margin M_G plus connected endpoint/corner remainder.
- Represent each endpoint contribution by the singlet source derivative beta_v=-d_s^4 log Z_v(0) with beta_v>=0 for the leading compact-group curvature term.
- Contract the endpoint source with null-channel pair weights inherited from the finite Schur-Feshbach block, giving D_v=2b12-4b13-4b23.
- Observe the exact shield b13+b23>=b12/2, so only boxes with strict fractional 12 dominance can contribute negatively.
- Use interval arithmetic and ignore protective negative-D_v terms to obtain the valid conservative lower bound I_-=M_G^- - C_N^+ sum beta_v^+[D_v^+]_+ - T_tail^+.
- Route the finite OS decision through I_- >=0 for promotion or I_+ <0 for a same-theory falsifier, while explicitly leaving continuum and spectral gates untouched.

Blocking gap: Actual regulated endpoint source data beta_v and cutoff-uniform signed T_tail are still missing for the fractional endpoint decomposition.

## Falsifiers

- A same-theory endpoint source computation yields I_+<0 for the three-hairpin null scalar; this is a finite Wilson OS falsifier.
- The required Z_v(s) exists only after adding a boundary counterterm or endpoint state, violating same-theory validity.
- The fractional incidence table has a 12-only endpoint box with D_v near 2 and beta_v large enough to defeat M_G.
- The eighth-derivative or tail bounds grow with cutoff so the endpoint interval is not regulator-uniform.
- A residual straight f f contact survives the null-incidence contraction, invalidating the endpoint-only decomposition.
- The locked gauge-invariant Wilson observable algebra is not preserved by the endpoint source recovery map.

## Learning

Cycle 284 makes the endpoint carrier decision-grade by deriving the half-overlap shield D_v<=0 from the actual null-channel weights. The conceptual pressure is endpoint collapse in the same Wilson theory; the declarative tension is collar OS positivity plus fixed gauge-invariant Wilson observables plus singular endpoint OPE without a boundary theory. Raw R is too weak and raw kappa4 is too strong; C_ep is sharper because it records source data and incidence signs. Success or failure changes the finite post-H,K reflected-Wilson OS gate only. Clay continuum construction, nontriviality, full OS/Wightman reconstruction, and mass gap remain non-claimed.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and interval-design guide.`
- Rationale: The branch has reduced the abstract Wilson/OS obstruction to a finite endpoint source interval; varying one overlap parameter reveals whether the carrier can actually demote the finite gate before more abstraction is useful.
- Situation seed: Heat-kernel SU(N) plaquette-sheet three-hairpin endpoint block with one endpoint box v whose 12 sheet footprint overlaps the 13 and 23 endpoint footprints by a controllable fraction alpha, while source derivatives are taken in the same Wilson measure.
- Varied variable: alpha=(b13_v+b23_v)/b12_v, the fractional non-12 overlap protecting the endpoint box.
- Held-fixed controls: Gauge group SU(N), heat-kernel plaquette action, and gauge-invariant Wilson source normalization are held fixed., The H,K finite Schur-Feshbach block, null vector, color factor C_N, and Gaussian margin M_G are held fixed., No boundary counterterm, gauge fixing, algebra enlargement, or continuum spectral claim is allowed., The endpoint source stencil and tail accounting scheme are kept identical across alpha.
- Expected observation: For alpha>=1/2 the clipped dangerous term vanishes; for alpha<1/2 the lower gate decreases linearly like -C_N beta_v 2b12(1-2alpha) until tail and beta intervals decide promotion or falsifier status.
- Transfer certificate needed: A regulator-uniform construction proving that the varied fractional footprint is realized by same-theory Wilson endpoint sources and that all unmodeled interactions are included in T_tail.

## Next Experiment

Compute the actual fractional incidence table for the three hairpin endpoint boxes, then evaluate the seven-point heat-kernel source stencil for any box with b13+b23 < b12/2 and assemble [I_-,I_+] with a regulator-uniform T_tail bound.

# Gauge-invariant endpoint-cell R polarization certificate

## Candidate Lemma

Conditional finite Route A theorem: for reflected H,K plus-channel endpoint sheet currents, a Ward-Hessian interval lower bound on the same-theory flowed Wilson cumulant gives a valid certificate for the post-H,K Schur-Feshbach endpoint-box scalar. It changes only the hard gate of finite endpoint-box positivity after H,K; Clay continuum existence, OS/Wightman reconstruction, nontriviality, large-field/topology control, and Hamiltonian mass gap remain untouched.

## Definitions

- source object: finite-volume cutoff SU(N) Yang-Mills with Wilson plaquette action, lattice spacing a, volume V, gradient-flowed connection B_t, and centered renormalized thin Wilson hairpins \widehat W_{+,t}^{I} supported in endpoint cell I.
- target object: the finite Schur-Feshbach endpoint positivity scalar for the H,K plus channel, with leakage L_+ computed from the already fixed finite reflected-Wilson Gram block.
- controlled interface: the carrier is the representation morphism \Phi from reflected Wilson hairpin contours to oriented sheet currents plus endpoint currents; the recovery map \Psi reconstructs the centered flowed Wilson observable before taking \kappa_2.
- same-theory condition: the pair term, connected four-curvature polarization, counterterms, leakage matrix entries, and recovery map are evaluated in the same cutoff, volume, flow-time, reflection, and Wilson-action family.
- Regulator: gradient flow at t>0 with endpoint point-splitting scale rho and cell diameter eta, followed by one-hairpin perimeter/cusp subtraction.
- Preserved observables: traced Wilson loops, flowed curvature insertions integrated over H,K sheets, reflection parity, color trace invariants, orientation signs, endpoint moments, and gauge-invariant cumulants.
- Error budget: G_{++}^{I,-} for the positive pair baseline, H_4^{I,+} for the Ward-subtracted four-curvature Hessian, E_6^{I,+} for sixth and higher cumulants, and E_ct^{I,+} for counterterm mismatch.

## Assumptions

- Model: finite lattice SU(N) Yang-Mills on a four-torus with Wilson plaquette measure and reflected Wilson observables; no continuum limit is assumed inside the lemma.
- Regime: endpoint cell I has diameter eta, endpoint separation d satisfies a<<sqrt(t)<=rho<eta<<d, and the H,K sheets meet I only through the certified endpoint currents.
- Cutoff: all constants are allowed to depend on a,V,t before a separate plateau audit; cutoff-uniformity is an extra frontier obligation, not part of the finite claim.
- Same-theory: the same gradient-flowed measure defines G_{++}^{I}, Xi_{++}^{I}, E_6^{I}, E_ct^{I}, and the Schur-Feshbach blocks B,D,C.
- Validity: the cumulant expansion is truncated only with an explicit E_6^{I,+} remainder and the fourth-order connected kernel is bounded after Ward and cusp subtraction.
- Local: only endpoint-box contributions are certified; bulk Wilson positivity and global OS spectral transfer are not claimed.

## Equations

- flowed endpoint cumulant defining R: `R_{++}^{I,\mathrm{ren}}=\kappa_2\left(\widehat W_{+,t}^{I},\theta \widehat W_{+,t}^{I}\right)_{\mathrm{ren}}`. Valid when: Valid when the recovered centered hairpins are gauge-invariant flowed Wilson observables in the same finite reflected lattice theory.
- color-geometric fourth-order split: `R_{++}^{I,\mathrm{ren}}=g_t^4(N^2-1)\left(2G_{++}^{I}+N\Xi_{++}^{I}\right)+E_6^{I}+E_{\mathrm{ct}}^{I}`. Valid when: Applies after diagonal color normalization, one-hairpin counterterm subtraction, and an explicit sixth-order cumulant remainder bound at fixed cutoff.
- Ward-Hessian polarization bound: `\Xi_{++}^{I}\ge -H_4^{I,+}M_{2,+}(I)^2`. Valid when: Requires Ward-subtracted connected four-curvature kernels whose endpoint monopole and dipole moments vanish in the plus channel.
- certified endpoint lower interval: `R_{++}^{I,-}=g_t^4(N^2-1)\left(2G_{++}^{I,-}-NH_4^{I,+}M_{2,+}(I)^2\right)-E_6^{I,+}-E_{\mathrm{ct}}^{I,+}\le R_{++}^{I,\mathrm{ren}}`. Valid when: Valid when G, H_4, moment, counterterm, and remainder intervals are computed from the same sheet-current representation.
- finite promotion inequality: `R_{++}^{I,-}>L_+:=B_{+R}D^{-1}B_{R+}-C_{++}^{(0)}`. Valid when: Applies when the finite Schur-Feshbach block D is positive and L_+ is the fixed post-H,K leakage threshold.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Nontriviality Witness Selection; source object: finite-volume cutoff SU(N) Yang-Mills with Wilson plaquette action, lattice spacing a, volume V, gradient-flowed connection B_t, and centered renormalized thin Wilson hairpins \widehat W_{+,t}^{I} supported in endpoint cell I.; target object: the finite Schur-Feshbach endpoint positivity scalar for the H,K plus channel, with leakage L_+ computed from the already fixed finite reflected-Wilson Gram block.; Model: finite lattice SU(N) Yang-Mills on a four-torus with Wilson plaquette measure and reflected Wilson observables; no continuum limit is assumed inside the lemma..
- Attack conceptual pressure: finite Schur-Feshbach positivity, positive flowed pair covariance, and same-theory Wilson renormalization must jointly hold, but the connected four-curvature polarization is the missing mediator that can erase the pair term.
- Replace the fragmented raw-contour carrier by endpoint sheet currents; compare route choices: a global non-Gaussian OS witness is too coarse, while interval kernel proof search targets the exact endpoint-box obstruction.
- Use the recovery map Psi to write the centered flowed hairpin as a sheet-current curvature integral plus controlled higher cumulants, preserving gauge invariance, color trace, reflection parity, orientation, and same-theory labels.
- Expand the flowed Wilson covariance to fourth order: the cross-pair contraction gives the positive term 2g_t^4(N^2-1)G_{++}^{I}; the connected four-curvature boundary-OPE term gives g_t^4N(N^2-1)Xi_{++}^{I}.
- Subtract the disconnected product and one-hairpin perimeter/cusp counterterms; invoke Ward subtraction so constant endpoint fields decouple from the centered plus current.
- Use reflected plus-channel orientation to certify zero endpoint monopole and dipole moments; Taylor expand the Ward-subtracted C4 kernel around the cell center.
- Bound the Taylor remainder by H_4^{I,+}M_{2,+}(I)^2 and attach E_6^{I,+}, E_ct^{I,+}; combine with the fixed leakage L_+=B_{+R}D^{-1}B_{R+}-C_{++}^{(0)}.
- Conclude the conditional finite certificate: if R_{++}^{I,-}>L_+ then the endpoint-box scalar is positive; if not, the R repair is demoted.

Blocking gap: The missing hard estimate is a certified same-theory interval for H_4^{I,+}, E_6^{I,+}, and E_ct^{I,+} with enough margin; no cutoff-uniform large-field/topology summability or continuum Schwinger-function construction is proved.

## Falsifiers

- falsifier: the plus-channel endpoint current has a nonzero dipole after actual H,K orientation signs are inserted.
- falsifier: Ward or cusp subtraction leaves an uncancelled O(1) boundary-OPE term in Xi_{++}^{I}.
- falsifier: interval quadrature gives NH_4^{I,+}M_{2,+}^2+E_6^{I,+}+E_ct^{I,+}\ge 2G_{++}^{I,-} with no positive margin.
- falsifier: the lower interval is positive at one cutoff but fails the same-theory regulator plateau test.
- falsifier: the recovered endpoint current is not equivalent to the original gauge-invariant Wilson hairpin under certified zero-pairing current equivalence.
- falsifier: finite endpoint positivity succeeds but cannot be attached to any OS-positive continuum Schwinger family; then it remains local evidence only.

## Learning

Cycle 284 makes the local contribution sharper: R_{++}/kappa_4 is not a symbolic threshold but a same-theory flowed Wilson cumulant with a Ward-Hessian endpoint-cell lower interval. The conceptual pressure is the missing mediator between finite Feshbach positivity and Wilson cumulant positivity. Success changes one hard gate, finite endpoint-box positivity after H,K; failure quarantines the R repair. The value signal is explanatory and route-changing at finite scope because moment cancellation converts C4 from an uncontrolled boundary-OPE term into an eta^2 interval problem, while every Clay gate remains untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and proof-search guide, not as evidence for the Clay theorem.`
- Rationale: The branch is blocked by a quantitative mediator, not by vocabulary: the actual question is whether Ward-Hessian suppression of C4 beats the positive pair baseline and the fixed Schur-Feshbach leakage.
- Situation seed: Finite SU(2) or SU(3) Wilson lattice gauge theory on a reflected four-torus with two thin gradient-flowed H,K hairpin endpoint boxes, represented by endpoint sheet currents and evaluated by interval arithmetic on the Ward-subtracted C4 kernel.
- Varied variable: Endpoint cell diameter eta relative to fixed endpoint separation d and flow radius sqrt(t).
- Held-fixed controls: Same Wilson action family, gauge group, reflection map, H,K sheet geometry, and centered renormalized Wilson hairpin recovery map., Fixed flow window c0 a^2 <= t <= c1 d^2, fixed one-hairpin perimeter/cusp counterterm convention, and fixed Schur-Feshbach leakage L_+., Fixed color normalization tr(T^AT^B)=delta^{AB}/2 and fixed plus-channel orientation signs.
- Expected observation: If the carrier is correct, the negative connected polarization interval scales like eta^2 while the positive pair baseline stays bounded below, producing a positive margin R_{++}^{I,-}-L_+ on a nonempty regulator window.
- Transfer certificate needed: A same-theory Ward-Hessian interval certificate with recovery-map equivalence, counterterm matching, sixth-order remainder control, and regulator plateau stability before any intuition may affect proof obligations.

## Next Experiment

Proof search: instantiate the actual H,K endpoint cells, compute the plus-current monopole and dipole moments, then interval-bound G_{++}^{I,-} and H_4^{I,+} on a near/far heat-kernel cell partition before evaluating R_{++}^{I,-}-L_+.

# Post-H,K connected Wilson polarization: first A012 shell certificate

## Candidate Lemma

Finite heat-kernel endpoint theorem: in the fixed reflected H,K endpoint box, if the connected four-curvature Wilson cumulant is enclosed by shell row bounds A_0,A_1,A_2 plus a tail T_{>=3}, then the Schur-corrected endpoint form has lower margin Delta_sigma^(012). Delta_sigma^(012)>0 certifies only finite Route A endpoint positivity; a certified negative Rayleigh quotient is a falsifier for this collar/hairpin geometry.

## Definitions

- source object: finite cutoff SU(N) heat-kernel lattice Yang-Mills measure mu_{a,B,beta}^{HK} on the reflected endpoint box, with vacuum-subtracted traced Wilson sheet-pair observables O_u.
- target object: Schur-corrected endpoint quadratic form G^{end}_sigma-S_{HK} on the finite H,K endpoint coefficient space, with numerical lower margin Delta_sigma^(012).
- controlled interface: sheet-kernel hypergraph H_sigma whose nodes are endpoint sheet-pairs u and whose edges encode transported plaquette-pair contractions, color tensors, shell labels ell, OPE intervals, and recovery map Rec_sigma(H_sigma)=R_sigma-S_{HK}.
- same-theory condition: C_sigma, kappa_{4,sigma}, E_{OPE,sigma}, and S_{HK} are computed from the same mu_{a,B,beta}^{HK}, same Wilson basis, same coupling normalization, same reflection, and same heat-kernel smoothing sigma.
- preserved observable: vacuum-subtracted traced Wilson sheet-pair O_u=:Tr U(S_u):-<Tr U(S_u)> in the H,K endpoint basis.
- representation morphism: Phi_sheet sends plaquette-sheet data to the endpoint matrix and preserves gauge invariance, reflection support, Gaussian/kappa_4 separation, and endpoint compression.
- shell distance: d_sh(u,v) is the minimum dyadic endpoint-box shell separating any plaquette pair in the supports of u and v.
- error budget: e_OPE bounds the boundary-OPE truncation, T_{>=3} bounds discarded shells, and interval radii bound compact-group quadrature.

## Assumptions

- Model: finite hypercubic endpoint box B subset a Z^4 with compact gauge group SU(N), heat-kernel plaquette action, reflected boundary split, and finite H,K collar/hairpin Wilson basis already fixed.
- Cutoff: sigma>=2a and all transported curvature insertions are heat-kernel smeared before the Wilson OPE expansion is truncated at fourth curvature order.
- Same-theory: no coefficient is imported from another regulator, volume, gauge fixing, coupling convention, or observable basis.
- Local: the certificate concerns only the finite endpoint box after H,K compression; it does not assert OS reconstruction, continuum existence, or a Hamiltonian mass gap.
- Validity: the OPE remainder is bounded as a quadratic-form interval |<x,E_{OPE}x>|<=e_OPE||x||^2 on the endpoint coefficient space.
- Constraint: shell quotienting is allowed only by Wilson trace identities, sheet symmetries, and reflection symmetries that leave Rec_sigma invariant.
- Uniformity: constants are finite-volume and finite-cutoff constants; no volume- or cutoff-uniform RG basin entry is claimed.

## Equations

- transported smeared plaquette curvature: `\mathfrak F_{p,u}^a(\sigma)=\operatorname{Ad}_{\tau_{p\to u}}F_p^a(\sigma)`. Valid when: Valid when each plaquette curvature is heat-kernel smeared and parallel transported along the fixed sheet path.
- two-curvature covariance kernel: `C_{uv}(\sigma)=\frac{1}{N^2-1}\sum_{p\in S_u,r\in S_v}w_{u,p}w_{v,r}\,\langle \mathfrak F_{p,u}^a(\sigma)\mathfrak F_{r,v}^a(\sigma)\rangle_c`. Valid when: Applies after vacuum subtraction and same-regulator transport of both sheet-supported curvature insertions.
- Gaussian Wilson polarization: `R^G_\sigma=\alpha_N g_R^4\,(C_\sigma\circ C_\sigma),\qquad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid for the crossed two-curvature Wick contraction in the traced Wilson normalization used here.
- connected four-curvature polarization: `K^{(4)}_{uv}(\sigma)=\sum_{p,q\in S_u\atop r,s\in S_v}W_{u,pq}W_{v,rs}\,\tau_N^{abcd}\,\langle \mathfrak F_p^a\mathfrak F_q^b\mathfrak F_r^c\mathfrak F_s^d\rangle_c`. Valid when: Requires the same heat-kernel measure, transported color frame, and connected cumulant subtraction for all four insertions.
- A012 shell row amplitudes: `A_\ell(\sigma)=\max_u\sum_{v:\,d_{sh}(u,v)=\ell}\frac{|K^{(4)}_{uv}(\sigma)|}{16N^2},\qquad \ell=0,1,2`. Valid when: Applies to the finite endpoint sheet-kernel hypergraph after quotienting only invariant sheet symmetries.
- negative kappa4 spectral envelope: `M_{4,\sigma}^-\le A_0(\sigma)+A_1(\sigma)+A_2(\sigma)+T_{\ge3}(\sigma)`. Valid when: Valid when Gershgorin row-sum compression is used on the endpoint coefficient matrix.
- Schur-corrected endpoint margin: `\Delta_\sigma^{(012)}=\lambda_{\min}(\alpha_N g_R^4(C_\sigma\circ C_\sigma))-g_R^4\sum_{\ell=0}^2A_\ell-g_R^4T_{\ge3}-e_{OPE}-s_{HK}`. Valid when: Applies after diagonal normalization of the endpoint basis and same-basis Schur subtraction.
- finite positivity certificate: `\langle x,(G^{end}_\sigma-S_{HK})x\rangle\ge \Delta_\sigma^{(012)}\|x\|^2`. Valid when: Valid when all previous interval bounds enclose the recovered endpoint matrix in the same cutoff theory.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Observable Density In The Excitation Sector; source object: finite cutoff SU(N) heat-kernel lattice Yang-Mills measure mu_{a,B,beta}^{HK} on the reflected endpoint box, with vacuum-subtracted traced Wilson sheet-pair observables O_u.; target object: Schur-corrected endpoint quadratic form G^{end}_sigma-S_{HK} on the finite H,K endpoint coefficient space, with numerical lower margin Delta_sigma^(012).; Model: finite hypercubic endpoint box B subset a Z^4 with compact gauge group SU(N), heat-kernel plaquette action, reflected boundary split, and finite H,K collar/hairpin Wilson basis already fixed..
- Freeze Clay target and claim level: the cycle attacks the missing mediator from connected boundary-OPE polarization to Schur-corrected endpoint positivity, not YM existence or mass gap.
- Choose regulator: finite SU(N) heat-kernel lattice action on the reflected endpoint box, with sigma-smeared transported plaquette curvatures and vacuum-subtracted traced Wilson sheets.
- Expand each endpoint Wilson sheet through fourth transported-curvature order; connected cumulants remove vacuum and perimeter pieces before any Schur subtraction.
- Compute the crossed two-curvature contribution: the SU(N) trace normalization gives alpha_N=(N^2-1)/(8N^2), and the geometric part is C_sigma circ C_sigma, hence PSD.
- Represent the remaining connected four-curvature cumulant as K^{(4)} on sheet-pair nodes with color tensor tau_N^{abcd}, Wilson weights W_{u,pq}, and shell distance d_sh.
- Apply a Gershgorin row-sum compression on shells ell=0,1,2 and a quarantined tail T_{>=3} to bound the negative spectrum M_{4,sigma}^-.
- Subtract the same-basis Schur hairpin energy s_HK=||E_HK^{-1/2}B_HK||^2 and OPE error e_OPE to obtain Delta_sigma^(012).
- Hard gate: Delta_sigma^(012)>0 promotes a finite endpoint-box positivity theorem; a certified negative interval Rayleigh quotient demotes this Wilson collar/hairpin route.

Blocking gap: The derivation still lacks outward-rounded same-regulator interval values for A_0,A_1,A_2 and T_{>=3}; without them Delta_sigma^(012) is a formula and not yet a numerical certificate.

## Falsifiers

- falsifier: exact interval quadrature gives Delta_sigma^(012)<=0 for every admissible sigma/a window in the fixed H,K geometry.
- falsifier: a normalized endpoint vector y has a certified negative interval Rayleigh quotient after all same-theory errors are included.
- falsifier: the A012 shell quotient changes Rec_sigma, showing the sheet-kernel carrier is non-invariant.
- falsifier: T_{>=3} is larger than the Gaussian PSD margin, so local shell truncation is not valid even at finite cutoff.
- falsifier: connected perimeter or vacuum terms survive, invalidating the cancellation used to isolate kappa_4.

## Learning

Conceptual pressure attacked: mediate actual connected Wilson cumulants to Schur-corrected endpoint positivity without inflating a finite Wilson calculation into the Clay theorem. Declarative tension: Wilson/OPE coefficients, connected kappa_4 negativity, OPE errors, and H,K Schur energy must be valid in one cutoff theory, while continuum OS reconstruction and spectral transfer remain quarantined. Carrier audit: scalar R is too weak and representation-limited; full gauge-invariant OS density is too strong and circular for this local gate; raw plaquette enumeration is exact but fragmented. Compared with those routes, the sheet-kernel hypergraph is efficient because it encodes sheets, weights, transporters, color tensors, shell labels, multiplicities, OPE intervals, and Schur data; preserves gauge invariance, reflection support, Gaussian/kappa_4 separation, endpoint compression, and same-theory normalization; supports cumulant contraction, quotient auditing, shell row/operator bounds, interval arithmetic, and Schur subtraction; quotients only by Wilson trace and sheet symmetries; keeps a finite endpoint-box locality budget; transfers only through Rec_sigma and Delta_sigma; and has falsifiers by margin failure, nonuniform envelopes, or non-invariant quotienting. Conceptual value signal: sharp and route-changing at finite scope because R is now a computable connected Wilson cumulant interval with explicit color and geometric factors, not a symbolic threshold. The hard gate is Delta_sigma^(012): success promotes only finite endpoint-box positivity, while failure kills this H,K collar/hairpin route without touching the larger Clay gates.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the finite H,K endpoint route.`
- Rationale: The branch has repeated the Delta_sigma abstraction enough; the proof state now depends on whether actual same-regulator A_0,A_1,A_2 intervals are small enough after Schur subtraction.
- Situation seed: Finite SU(3) heat-kernel lattice endpoint box with the fixed reflected H,K collar/hairpin Wilson sheets; evaluate compact-group interval enclosures for connected four-plaquette cumulants in shells 0,1,2.
- Varied variable: rho=sigma/a, the heat-kernel smoothing ratio, varied over rho in {2,3,4} at fixed beta and fixed endpoint geometry.
- Held-fixed controls: same H,K Wilson sheet-pair basis and diagonal normalization, same heat-kernel plaquette action, coupling convention, and finite endpoint box, same reflection structure and vacuum-subtracted traced Wilson observables, same Schur hairpin matrix S_HK and same OPE truncation order
- Expected observation: If smoothing suppresses connected kappa_4 faster than it suppresses the Gaussian color square, Delta_sigma^(012) should become positive in a rho window; if A_0 remains too negative, the route is demoted for this geometry.
- Transfer certificate needed: A rigorous outward-rounded interval quadrature certificate showing gauge-invariant quotient preservation, connected-cumulant subtraction, A012 row bounds, OPE error, tail bound, and same-basis Schur subtraction before the observation may affect proof obligations.

## Next Experiment

Build the A012 interval table for the fixed SU(3) heat-kernel H,K endpoint box: enumerate shell-labeled plaquette quadruples, apply connected cumulant subtraction and color reduction, compute outward-rounded compact-group intervals, recover Delta_sigma^(012), and run the interval Rayleigh falsifier.

