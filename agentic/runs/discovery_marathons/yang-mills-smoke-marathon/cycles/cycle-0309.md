# cycle-0309

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-positivity endpoint source carrier for post-H,K Wilson block

## Candidate Lemma

Finite endpoint source interval gate: for the fixed three-hairpin reflected-Wilson block in heat-kernel plaquette-sheet regulation, after Wick-square Gram positivity and straight f f incidence cancellation, the post-H,K null-channel scalar is certified by same-theory endpoint source cumulants. If its interval lower endpoint is positive, this finite OS transfer block is promoted; if its upper endpoint is negative, it is a finite same-theory falsifier. No continuum YM existence or mass-gap claim follows.

## Definitions

- source object: a finite cutoff SU(N) Yang-Mills heat-kernel plaquette-sheet model with the locked reflected Wilson hairpin observables, endpoint boxes B_v, and source-deformed endpoint partition functions Z_v(sL).
- target object: the finite post-H,K reflected-Wilson OS transfer gate, namely positivity of the Schur-Feshbach null-channel scalar for this one regulated Wilson block.
- controlled interface: the endpoint carrier C_ep sending connected four-flux source cumulants, signed fractional incidences D_v, color factor C_N, Gaussian margin M_G, and tail T_tail to one scalar interval [I_-,I_+].
- same-theory condition: all Z_v, Wilson normalizations, plaquette sheets, source insertions, and tails are computed in the same cutoff gauge-invariant theory, with no boundary counterterm or replacement boundary algebra.
- Endpoint source direction L_v is the Lie-algebra source obtained by contracting the endpoint plaquette-sheet incidence of the Feshbach null channel in B_v.
- D_v=2b_{12,v}-4b_{13,v}-4b_{23,v} records the signed endpoint dominance for the actual post-H,K null contraction, not a symbolic R parameter.

## Assumptions

- Model: SU(N), N>=2, four-dimensional finite lattice Yang-Mills with heat-kernel plaquette action and gauge-invariant Wilson sheet observables only.
- Regime: the hairpin collars, endpoint boxes, and H,K finite block are fixed before taking any continuum or infinite-volume limit.
- Cutoff: all cumulants, source derivatives, and tails are evaluated at fixed cutoff a and endpoint scale r with stated uniform remainder budgets.
- Same-theory: the regulator, Wilson-loop renormalization, reflection map, and gauge-invariant observable algebra are identical on the source and target sides.
- Local: non-endpoint overlap and separated footprint contributions are either included in the positive Gram part or charged to T_tail with a cutoff-uniform bound.
- Validity: the statement is a finite witness theorem and does not assert OS positivity for all observables, Wightman reconstruction, nontriviality, or a Hamiltonian mass gap.

## Equations

- connected endpoint cumulant: `\kappa_v(L)=\left.\partial_s^4\log Z_v(sL)\right|_{s=0}=\langle X_v(L)^4\rangle_{c,a,v}`. Valid when: Valid when Z_v is the same cutoff endpoint-box source partition function and L is inside the heat-kernel coordinate chart.
- endpoint Wilson R contribution: `R^{\mathrm{end}}_{ij}=C_N\sum_v b_{ij,v}\,\kappa_v(L_{ij,v})+T_{ij}^{\mathrm{tail}},\qquad C_N=\frac{g_a^4}{4}\left(\frac{T_F}{N}\right)^2`. Valid when: Applies after Wilson plaquette-sheet expansion, singlet color projection, and isolation of endpoint-box connected four-flux cumulants.
- root-quartic local expansion: `\kappa_v(L)=-\frac{t_v^4}{60}\,R_4(L)+E_v,\qquad R_4(L)=N\operatorname{tr}(L^4)+3(\operatorname{tr}(L^2))^2\ge0`. Valid when: Requires small heat-kernel endpoint coordinates, Hermitian Lie-algebra source convention, and a uniform bound on the remainder E_v.
- null-channel incidence contraction: `D_v=2b_{12,v}-4b_{13,v}-4b_{23,v}=2\bigl(b_{12,v}-2(b_{13,v}+b_{23,v})\bigr)`. Valid when: Valid after contracting the endpoint R_{ij} terms with the already fixed Feshbach null vector of the three-hairpin block.
- scalar interval certificate: `I_{\mathrm{gate}}=M_G+C_N\sum_v D_v\,[-A_v-\epsilon_v,-A_v+\epsilon_v]+[-\tau,\tau],\quad A_v=\frac{t_v^4}{60}R_4(L_v)`. Valid when: Applies when each endpoint source class has a certified remainder |E_v|<=epsilon_v and the total endpoint tail is bounded by tau.
- promotion and falsifier test: `I_->0\Rightarrow \text{finite block promoted},\qquad I_+<0\Rightarrow \text{finite same\mbox{-}theory OS falsifier}`. Valid when: Requires the scalar interval to include every endpoint class and all tails without changing the Wilson observable algebra.

## Attempted Derivation

- Start from the fixed-collar reflected Wilson OS matrix and use the already established Schur-Feshbach reduction to a post-H,K null-channel scalar M_G+R_null+tail, without repeating the earlier threshold calculation.
- Expand each regulated Wilson plaquette-sheet product by connected cumulants in the heat-kernel cutoff theory; keep only gauge-invariant singlet contractions of endpoint flux sources.
- Use the connected logarithm to separate Wick-square contractions as positive Gram contributions; these cannot create a negative null-channel scalar.
- Use the straight-segment incidence identity for the actual hairpin null vector to cancel the local C_A f f commutator contact away from endpoints.
- Localize the remaining connected boundary-OPE polarization to endpoint boxes B_v and represent it by kappa_v(L)=partial_s^4 log Z_v(sL)|0.
- Insert the small heat-kernel Haar-Jacobian expansion kappa_v=-(t_v^4/60)R_4(L_v)+E_v with R_4>=0 and certified remainder |E_v|<=epsilon_v.
- Contract endpoint contributions with D_v=2b12_v-4b13_v-4b23_v, then form the interval M_G+C_N sum_v D_v[-A_v-epsilon_v,-A_v+epsilon_v]+[-tau,tau].
- Read promotion from I_->0 and demotion from I_+<0; otherwise keep the branch quarantined for endpoint source data.

Blocking gap: The actual source-equivalence classes, fractional incidences b_{ij,v}, seven-point source intervals for kappa_v, and cutoff-uniform tail tau have not been computed for the fixed hairpin endpoint partition.

## Falsifiers

- A certified endpoint interval with I_+<0 is a finite same-theory falsifier of the post-H,K Wilson block.
- A nonuniform endpoint tail tau(a,r) that does not stay bounded below the Schur-Feshbach margin invalidates the transfer certificate.
- A boundary counterterm needed to define Z_v(sL) changes the theory and falsifies the same-theory condition.
- A source-equivalence class with D_v>0 and a large negative kappa_v interval defeats the half-overlap shield.
- A mismatch between plaquette-sheet source derivatives and the Wilson observables used in H,K makes the endpoint carrier representation-limited rather than valid.

## Learning

Cycle 309 converts quarantine into a finite validator-facing endpoint theorem. The declarative tension is collar OS positivity plus fixed Wilson observables plus singular endpoint OPE without a boundary theory. Raw R is too weak, raw kappa_4 spectra are too strong, and the global Schur-preimage route is valid but too coarse after H,K. The efficient representation is C_ep: source classes, seven source values, cumulant intervals, signed incidences, C_N, M_G, and T_tail; it preserves same-theory Wilson normalization, reflection symmetry, null cancellations, and cutoff bookkeeping; it uses source differentiation, interval arithmetic, source-equivalence, color multiplication, clipping, incidence contraction, and tail addition. The sharp value signal is that negative root-quartic endpoint cumulants are not the obstruction; positive D leakage plus uncontrolled tail is.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe while the branch remains quarantined from promotion.`
- Rationale: The branch is blocked by endpoint data, not by another OS topology restatement. A target-preserving finite heat-kernel source experiment directly tests the connected cumulant witness that can promote or demote the post-H,K gate.
- Situation seed: Fixed SU(2) or SU(3) heat-kernel lattice endpoint-box model for the three reflected Wilson hairpins; compute the seven source values log Z_v(ell h L_v), ell=-3,...,3, for source-equivalent endpoint classes in the same plaquette-sheet regulator.
- Varied variable: The fractional 12-dominance alpha_v=(b_{13,v}+b_{23,v})/b_{12,v}, varied across endpoint partitions near the half-overlap threshold alpha_v=1/2.
- Held-fixed controls: The same regulated Wilson hairpin observables and Feshbach null vector used to compute H,K., The heat-kernel plaquette action, reflection map, color normalization T_F, and singlet endpoint source convention., The Gaussian Schur margin M_G and the rule that all unlocalized overlap is charged to T_tail., No boundary counterterm, no gauge fixing change, and no replacement observable algebra.
- Expected observation: For alpha_v>=1/2 the root-quartic negative cumulant contributes protectively or cancels; for alpha_v<1/2 a sufficiently negative fourth source difference can drive I_+ below zero and produce a finite same-theory falsifier.
- Transfer certificate needed: Certified source-derivative intervals for kappa_v, source-equivalence proof, fractional incidence table, color factor audit, and a cutoff-uniform T_tail bound before the intuition may affect proof obligations.

## Next Experiment

Route to proof search plus endpoint-data computation: build the heat-kernel SU(N) endpoint source table for the fixed hairpin block, aggregate by regulated source equivalence, compute D_v, form the connected cumulant witness interval C_ep, and either promote the finite gate, produce a falsifier, or keep quarantine.

# Cycle 309: Ward-Hessian sector constants for R++

## Candidate Lemma

For the fixed H,K plus endpoint geometry, Ward/cusp and plus-moment cancellation reduce the connected boundary-OPE polarization to near/far Hessian constants, giving a finite lower interval for R_{++}^{ren}.

## Definitions

- source object: centered flowed SU(N) Wilson hairpin endpoint currents J_+ on a finite hypercubic lattice, with boundary point-splitting and gradient-flow time t.
- target object: the finite post-H,K plus-channel Schur-Feshbach endpoint quadratic form Q_+ on ker B_KK.
- controlled interface: the renormalized connected Wilson cumulant R_{++}^{ren}=kappa_2(W_{J_+},W_{J_+})_c inserted into the C_KK endpoint block.
- same-theory condition: H,K, R_{++}, recovery maps, and limits use one Wilson action, one flow scheme, and one cutoff sequence.
- carrier: endpoint sheet currents with certified zero-pairing quotient; invariants are gauge, color, reflection, orientation, cutoff locality.
- moments: M0_near is near-cell current mass; M2_+ is the plus-channel second endpoint moment after Ward monopole/dipole cancellation.
- sector constants: H_near and H_far bound Ward-subtracted four-curvature kernels on near and far endpoint-cell pairs.

## Assumptions

- Model: finite SU(N) Wilson lattice gauge theory with gradient-flow observables before any continuum claim.
- Regime: endpoint boxes are disjoint except prescribed reflected collars; eta < sqrt(t)/4 and refinement is finite.
- Cutoff: interval constants are uniform for a <= a0 at fixed physical t and endpoint geometry.
- Same-theory: no Gaussian replacement; pair term and C4 kernels are cumulants of the same centered flowed Wilson family.
- Validity: Ward/cusp counterterms cancel one-hairpin divergences and leave zero monopole/dipole plus moments.
- Local: only finite endpoint-box positivity after H,K is claimed; OS/Wightman existence and mass gap remain untouched.

## Equations

- R-sector-decomposition: `\(R_{++}^{\rm ren}=g_t^4\{2(N^2-1)G_{++}^{\rm pair}+N(N^2-1)C_{4,++}^{\rm WS}\}+E_{\rm rec}\)`. Valid when: Valid when centered flowed Wilson hairpins are expanded to fourth order after disconnected, perimeter, and cusp subtractions in the same Wilson regulator.
- Ward-Hessian-majorant: `\(|C_{4,++}^{\rm WS}|\le H_{\rm near}^{+}M_{0,\rm near}^2+H_{\rm far}^{+}\eta^2M_{2,+}^2\)`. Valid when: Applies after Ward subtraction and plus-channel monopole/dipole cancellation on endpoint cells of diameter eta below the flow radius.
- promotion-interval: `\(g_t^4[2(N^2-1)G_{++}^{-}-N(N^2-1)(H_{\rm near}^{+}M_{0,\rm near}^2+H_{\rm far}^{+}\eta^2M_{2,+}^2)]-E_{\rm rec}^{+}>L_+\)`. Valid when: Requires cutoff-uniform interval lower and upper bounds for pair, sector, and recovery terms before inserting the finite Schur-Feshbach leakage.

## Attempted Derivation

- Conceptual pressure: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator; positive pair covariance and flow renormalization are valid but C4 can erase them.
- Rewrite thin hairpins as endpoint sheet currents; raw contours are fragmented, while endpoint currents preserve gauge/color/reflection/orientation and expose Ward moments.
- Compare routes: global OS spectral transfer or non-Gaussian Schwinger family witness is too coarse; finite interval proof search attacks the post-H,K scalar gate directly.
- Taylor expand each Ward-subtracted sector kernel on endpoint cells; zero monopole/dipole moments remove constant/linear terms, leaving Hessian constants times eta^2 M2 plus near-cell mass.

Blocking gap: Need certified H_near^+, H_far^+, G_{++}^- and E_rec^+ with outward rounding and cutoff-uniform recovery; no numerical interval is yet produced.

## Falsifiers

- falsifier: Ward/cusp subtraction leaves a nonzero dipole moment, so the Hessian eta^2 suppression is invalid.
- falsifier: the lower interval for R_{++}^{ren} is <= L_+, so endpoint-box positivity is not repaired.
- falsifier: recovery from endpoint currents to Wilson hairpins changes the same-theory cumulant.
- falsifier: H_near or H_far grows with cutoff or topology sector, breaking uniform validity.

## Learning

Cycle 309 makes R++ a finite sector-Hessian certificate: Ward/cusp and plus-moment cancellations convert C4 to near/far constants competing with the pair baseline. Hard gate: post-H,K endpoint-box positivity; success promotes one Route A gate, failure quarantines R repair; Clay gates untouched.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch has looped on interval scaffolds; a concrete flowed-lattice endpoint-box stress case tests whether the Hessian mechanism has size, not just form.
- Situation seed: SU(N) hypercubic Wilson lattice with two reflected plus-channel H,K endpoint boxes; measure centered flowed hairpins and Ward-subtracted C4 sector kernels.
- Varied variable: endpoint cell diameter eta/sqrt(t), with geometry and flow time fixed.
- Held-fixed controls: same Wilson action and cutoff sequence, fixed H,K collars and plus-channel endpoint current, fixed gradient-flow time t and point-splitting prescription, same Schur-Feshbach leakage L_+
- Expected observation: Pair baseline G++ stays positive while C4 interval shrinks like eta^2 until near-cell mass dominates; crossing the inequality promotes the finite gate.
- Transfer certificate needed: Cutoff-uniform same-theory recovery from endpoint currents to centered flowed Wilson cumulants, plus outward-rounded sector constants valid on all endpoint cells.

## Next Experiment

Route to proof search: compute outward-rounded near/far sector constants for the SU(N) flowed endpoint-box case; record same-theory nontriviality witness as a non-claim and demote on any falsifier.

# Gauge-Invariant Observable Density In The Excitation Sector -> quarantined finite raw-K4 endpoint stress gate

## Candidate Lemma

Phase-projected raw K4 stress criterion. In the first heat-kernel Wilson H,K endpoint box, three same-regulator interval enclosures can disprove Schur-corrected endpoint positivity: if \(\tau_{pq}(\theta)<0\), then \(U_\sigma\) has a negative two-sparse Rayleigh witness and the finite collar/hairpin Route A endpoint is demoted.

## Definitions

- source object: finite heat-kernel regulated SU(N) Wilson lattice measure on one reflected endpoint box, with oriented plaquette sheets, parallel transporters, and vacuum-subtracted endpoint observables \(\mathcal Q_i\).
- target object: the Schur-corrected endpoint quadratic form \(U_\sigma=R_\sigma-B^*E^{-1}B\) on the finite endpoint index set, not an OS Hamiltonian or mass-gap object.
- controlled interface: interval arithmetic for the connected cumulant witness \(R_{ij}=\mathrm{cum}_2(\mathcal Q_i,\mathcal Q_j)\), decomposed into Gaussian color square, raw connected K4, OPE error, and H,K Schur subtraction.
- same-theory condition: the Wilson measure, heat-kernel regulator, endpoint geometry, renormalized coupling, OPE normalization, and Schur blocks are all taken from the same cutoff theory.

## Assumptions

- Model: SU(N) lattice Yang-Mills with heat-kernel plaquette regulator at cutoff a and smearing scale sigma on a fixed finite endpoint box.
- Cutoff: no continuum, volume-uniform, or physical-unit spectral transfer is claimed in this lemma.
- Same-theory: the raw K4 intervals, Gaussian covariance, OPE interval, and H,K Schur data use the identical reflected Wilson basis and normalization.
- Local: endpoints p,q are two endpoint sheet-pair nodes after exact Wilson quotienting, with finite plaquette support and reflection-compatible transporters.
- Validity: diagonal upper intervals \(U_{pp}^+,U_{qq}^+\) and phased off-diagonal lower interval \(L_{pq}(\theta)>0\) are rigorous enclosures for every admissible field configuration in the cutoff measure.

## Equations

- endpoint observable: `\mathcal Q_i=\sum_{\alpha\in S_i}w_{i\alpha}:\operatorname{tr}(T^aU_{\alpha,1}T^bU_{\alpha,2}^{-1})F^a_{\alpha,1}F^b_{\alpha,2}:_{\sigma,a}`. Valid when: Valid when the heat-kernel regulator, endpoint sheets, transporters, and Wilson normalization are fixed in one cutoff theory.
- connected boundary polarization: `R_{ij}=\operatorname{cum}_2(\mathcal Q_i,\mathcal Q_j)=G_{ij}+K^{(4)}_{ij}+E^{\mathrm{OPE}}_{ij}`. Valid when: Valid when vacuum and perimeter terms are cumulant-subtracted before the endpoint compression is formed.
- Gaussian crossed contraction: `G_{ij}=\alpha_N g_R^4\sum_{\alpha\in S_i,\beta\in S_j}w_{i\alpha}w_{j\beta}\,C_{\alpha\beta,13}^{\sigma}C_{\alpha\beta,24}^{\sigma},\qquad \alpha_N=(N^2-1)/(8N^2)`. Valid when: Applies after the two crossed heat-kernel curvature contractions are isolated from the connected Wilson cumulant.
- Schur-corrected endpoint matrix: `U_{ij}=R_{ij}-(B^*E^{-1}B)_{ij}`. Valid when: Valid when the H,K complement block E is positive on its finite range and the same endpoint basis is used.
- two-sparse phase stress: `L_{pq}(\theta)=\inf \Re(e^{-i\theta}U_{pq}),\qquad \tau_{pq}(\theta)=U_{pp}^+-\frac{L_{pq}(\theta)^2}{U_{qq}^+}`. Valid when: Requires rigorous same-regulator upper diagonal intervals and a positive phased lower off-diagonal interval.
- finite falsifier condition: `\tau_{pq}(\theta)<0\;\Longrightarrow\;\exists x\in\operatorname{span}\{e_p,e_q\}:x^*U_\sigma x<0`. Valid when: Valid when \(U_{qq}^+>0\) and the interval inclusions hold simultaneously for the cutoff Wilson measure.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Gauge-Invariant Observable Density In The Excitation Sector; source object: finite heat-kernel regulated SU(N) Wilson lattice measure on one reflected endpoint box, with oriented plaquette sheets, parallel transporters, and vacuum-subtracted endpoint observables \(\mathcal Q_i\).; target object: the Schur-corrected endpoint quadratic form \(U_\sigma=R_\sigma-B^*E^{-1}B\) on the finite endpoint index set, not an OS Hamiltonian or mass-gap object.; Model: SU(N) lattice Yang-Mills with heat-kernel plaquette regulator at cutoff a and smearing scale sigma on a fixed finite endpoint box..
- Freeze the Clay target boundary: this cycle attacks the conceptual pressure of mediating connected boundary-OPE polarization to finite Schur-corrected endpoint positivity, while OS reconstruction, nontrivial continuum YM, gauge-invariant observable density, and mass gap remain non-claims.
- Use the heat-kernel SU(N) cutoff and the first H,K endpoint geometry; represent each endpoint observable as a weighted transported plaquette-sheet quadratic \(\mathcal Q_i\).
- Apply connected-cumulant subtraction. Vacuum and perimeter pieces cancel; crossed two-curvature pairings form the PSD Gaussian color square \(G\); the only non-Gaussian danger is the raw transported four-curvature cumulant \(K^{(4)}\), plus the controlled OPE interval.
- Compress through the finite Schur-Feshbach interface: \(U=G+K^{(4)}+E^{OPE}-B^*E^{-1}B\). This changes only the finite endpoint positivity gate.
- For endpoints p,q and phase theta, take interval upper bounds for \(U_{pp},U_{qq}\) and a lower bound for \(\Re(e^{-i\theta}U_{pq})\). With \(x=e_p-(L_{pq}(\theta)/U_{qq}^+)e^{i\theta}e_q\), interval arithmetic gives \(x^*Ux\le \tau_{pq}(\theta)\).
- If \(\tau_{pq}(\theta)<0\), endpoint PSD fails and this H,K collar/hairpin route is finitely falsified. If all tested phases survive, the proof state moves to full \(\Delta_{raw}\) PSD proof search, not to OS density.

Blocking gap: The same-regulator numerical or symbolic interval enclosures for the three raw K4 quantities \(K^{(4)}_{pp},K^{(4)}_{qq},\Re(e^{-i\theta}K^{(4)}_{pq})\) have not been computed; without them the stress theorem is conditional only.

## Falsifiers

- falsifier: a certified \(\tau_{pq}(\theta)<0\) gives a two-sparse negative Rayleigh vector and demotes the finite H,K endpoint route.
- Regulator mismatch between K4 intervals, Gaussian covariance, OPE error, and Schur blocks invalidates the certificate.
- Exact Wilson quotienting that changes a transported color tensor or orientation sign makes the interval non-invariant.
- If all phase stresses are nonnegative but \(\Delta_{raw}\) later has a negative eigenvector, the two-sparse tactic was incomplete, not wrong.
- If raw K4 intervals are absent after this cycle, the abstraction is quarantined until raw plaquette interval proof search supplies them.

## Learning

Conceptual pressure attacked: replace symbolic boundary polarization by a validator-facing connected cumulant witness that can decide a finite Schur-corrected endpoint gate. Declarative tension: Wilson/OPE coefficients, raw K4 negativity, OPE errors, and H,K Schur subtraction must be valid in one cutoff theory, while continuum OS reconstruction, gauge-invariant observable density, excitation-sector cyclicity, and the mass gap are barred. Carrier audit: scalar R is too weak, OS Hilbert observable algebra is too strong and circular for this local gate, shell A012 is convenient but quarantined, and raw plaquette enumeration is fragmented yet valid. Compared with full \(\Delta_{raw}\) search, the phase-stress route is a sharper negative tactic because three same-theory intervals can falsify endpoint PSD. Efficient representation requirements: encode oriented plaquettes, sheet weights, transporters, color tensors, cumulant intervals, OPE intervals, endpoint indices, and Schur blocks; preserve gauge invariance, reflection support, Gaussian/K4 separation, endpoint compression, same-theory normalization, and exact Wilson quotienting; support cumulant contraction, interval summation, phase certification, Rayleigh stress search, Loewner bounds, and Schur subtraction; transfer only through \(\tau\), \(\Delta_{raw}\), or \(x_{stress}\); expose falsifiers by negative margin, missing intervals, non-invariant quotienting, or regulator mismatch. Hard gate: \(\tau_{pq}(\theta)<0\) demotes the finite H,K endpoint route; survival forces full \(\Delta_{raw}\) proof search. Value signal: sharp and route-changing at finite scope, because it unifies Gaussian color positivity, non-Gaussian K4 danger, OPE error, and Schur hairpin energy in one valid inequality without implying Clay.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the finite H,K endpoint gate.`
- Rationale: The branch has looped through scalar R and shell A012 abstractions; a concrete phase-stress experiment tests the actual connected cumulant witness before any further abstraction is allowed.
- Situation seed: Heat-kernel regulated SU(N) Wilson lattice on the first reflected H,K collar/hairpin endpoint box, with two endpoint sheet-pair nodes p,q and raw plaquette-quartet K4 interval arithmetic.
- Varied variable: phase theta in the two-sparse vector \(e_p-e^{i\theta}t e_q\).
- Held-fixed controls: same Wilson heat-kernel regulator, cutoff a, smearing sigma, group SU(N), and renormalized coupling, same endpoint geometry, sheet weights, transported color tensors, OPE normalization, and H,K Schur blocks, finite endpoint-box locality budget; no continuum or volume extrapolation, exact Wilson quotient identities only, with reflection support preserved
- Expected observation: A valid phase sector either yields \(L_{pq}(\theta)^2>U_{pp}^+U_{qq}^+\), producing a finite falsifier, or fails to do so and forces full \(\Delta_{raw}\) PSD proof search.
- Transfer certificate needed: A validator-facing raw K4 interval certificate for the connected cumulant witness, plus exact quotient audit and same-theory error-budget ledger, before any conclusion may alter the proof queue.

## Next Experiment

Proof search: compute the first same-regulator raw K4 phase intervals for the connected cumulant witness on endpoint pair p,q; if absent, keep the branch quarantined and import or derive heat-kernel plaquette-quartet cumulant bounds before any further promotion.

