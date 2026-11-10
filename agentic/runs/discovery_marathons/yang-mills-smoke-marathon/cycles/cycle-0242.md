# cycle-0242

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint-box kappa_4 bound for the three-hairpin Wilson collar block

## Candidate Lemma

In the heat-kernel plaquette-sheet regulator, after the Wick-square Gram term and the straight-segment f f commutator contact cancel in the three-hairpin null channel, the only remaining post-H,K danger is the negative spectral part of the singlet-projected connected four-flux endpoint cumulant. A valid endpoint bound below the positive Gaussian margin promotes the block; a signed endpoint eigenvector exceeding that margin is a same-theory falsifier.

## Definitions

- source object: heat-kernel plaquette-sheet Wilson collar observables W_i^{epsilon,sigma} for the actual three reflected hairpins, with endpoint boxes B_p(sigma) on the reflection plane.
- target object: the signed endpoint-box kappa_4 contribution E_kappa4(v) to the corrected second Schur-Feshbach scalar for v=(1,1,-2).
- controlled interface: regulated Wilson cumulant expansion -> finite Schur-Feshbach endpoint quadratic form after Wick-square positivity and straight-segment f f cancellation.
- same-theory condition: the same renormalized Wilson loops are used before and after collar collapse; no boundary counterterm, endpoint normalization, or algebra enlargement is allowed.
- Omega_{i,p}(x,y) is the oriented two-flux plaquette-sheet incidence density of hairpin i inside endpoint box p, including the right-angle corner smoothing.
- Z_p^{ab}(x,y)=delta^{ab} sum_i v_i Omega_{i,p}(x,y) is the null-channel singlet two-flux load.
- I_v=sum_p ||Z_p||_2^2 is the explicit geometric incidence norm; it is read directly from the endpoint incidence table, not fitted from a symbolic model.
- lambda_-(K_p) means max(0,-lambda_min(K_p)) for the singlet endpoint cumulant operator.

## Assumptions

- The heat-kernel plaquette-sheet regulator is reflection positive and preserves the locked gauge-invariant Wilson test algebra at finite epsilon and sigma.
- The endpoint boxes are disjoint after smoothing, and cross-box cumulants are bounded by a tail C_tail sigma^alpha or by the available mass/clustering estimate.
- The previously computed H,K block fixes a positive Gaussian margin M_G=8m^2 in the null channel; this cycle only estimates the remaining endpoint kappa_4 term.
- The Wick-square part of the four-flux expansion is a nonnegative Gram contribution and is not used as a falsifier.
- The local straight-boundary f f commutator contact has zero oriented incidence against v=(1,1,-2); endpoint corner remnants are retained in K_p.
- The singlet color projection is the fundamental Wilson trace projection (1/N)Tr(T^a T^b)=(T_F/N)delta^{ab}, with C_A=N for SU(N).

## Equations

- endpoint connected four-flux term: `R_{ij}^{\mathrm{end},\kappa_4}(\epsilon,\sigma)=\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2\sum_{p\in E}\delta^{ab}\delta^{cd}\int_{B_p^4}\Omega_{i,p}(x,y)\Omega_{j,p}(z,w)\langle F^a(x)F^b(y)F^c(z)F^d(w)\rangle_{c,\epsilon}\,dxdydzdw+\mathrm{Tail}_{ij}(\sigma)`. Valid when: Valid when the heat-kernel plaquette-sheet regulator separates endpoint boxes from straight boundary segments before the cutoff is removed.
- null-channel endpoint reduction: `E_{\kappa_4}(v)=\sum_{i,j}v_i v_j R_{ij}^{\mathrm{end},\kappa_4}=\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2\sum_{p\in E}\langle Z_p,\mathcal K_{p,\epsilon}^{\mathrm{sing}}Z_p\rangle+\mathrm{Tail}_v(\sigma)`. Valid when: Applies after diagonal normalization and the null vector have eliminated one-body and length-linear Wilson terms.
- singlet color decomposition: `\delta^{ab}\delta^{cd}\mathcal K_p^{abcd}=(N^2-1)^2\kappa_{0,p}+C_A(N^2-1)\kappa_{f,p}+\frac{(N^2-4)(N^2-1)}{N}\kappa_{d,p}`. Valid when: Requires an SU(N) invariant endpoint cumulant decomposed into scalar, f-channel, and d-channel color tensors.
- negative-spectrum endpoint bound: `E_{\kappa_4}(v)\ge -\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2\sum_{p\in E}\lambda_-(\mathcal K_{p,\epsilon}^{\mathrm{sing}})\|Z_p\|_2^2-|\mathrm{Tail}_v(\sigma)|`. Valid when: Valid when each endpoint cumulant defines a bounded quadratic form on the smeared two-flux singlet space.
- first promotion test: `\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2\Lambda_-\mathcal I_v+C_{\mathrm{tail}}\sigma^{\alpha}<M_G,\qquad M_G=8m^2`. Valid when: Applies after the H,K computation has fixed the positive Gaussian margin for this finite hairpin block.
- signed falsifier test: `\sum_{p\in E}\langle Z_p,\mathcal K_p^{\mathrm{sing}}Z_p\rangle<-\frac{4N^2}{g^4T_F^2}M_G-O(\sigma^{\alpha})\quad\Longrightarrow\quad \det q_{\mathrm{Schur}}<0`. Valid when: Valid when the signed endpoint cumulant survives cutoff removal in the same Wilson-loop normalization.

## Attempted Derivation

- Start from the heat-kernel plaquette-sheet representation of each reflected Wilson hairpin and expand the logarithm of the regulated Wilson quotient through four boundary flux insertions.
- Separate the four-flux term into Wick-square contractions, local commutator contacts, and the irreducible connected cumulant kappa_4.
- Use the previously verified null-channel cancellations: one-body Wilson factors vanish on 1^perp, length-linear second terms vanish for v=(1,1,-2), the Wick-square part is a positive Gram term, and the straight f f contact has zero oriented incidence.
- Localize the remaining connected term by a partition of unity into endpoint boxes B_p(sigma); separated-box cumulants are assigned to Tail_v(sigma).
- Apply the fundamental Wilson trace projection twice, giving the color factor (g^4/4)(T_F/N)^2 delta^{ab}delta^{cd}.
- Package the oriented geometric sheet data into Z_p and view the endpoint cumulant as a self-adjoint singlet quadratic form K_p on two-flux smearing functions.
- Bound the endpoint contribution from below by the negative spectral part lambda_-(K_p) times the incidence norm ||Z_p||_2^2, plus the controlled cross-endpoint tail.
- Compare that explicit bound with the positive Gaussian margin M_G from the already computed H,K Schur-Feshbach gate.

Blocking gap: The missing analytic input is a cutoff-uniform signed estimate, or at least a sharp negative-spectrum bound, for the singlet-projected connected four-flux endpoint cumulant K_p in four-dimensional Yang-Mills heat-kernel regulation.

## Falsifiers

- A negative eigenvalue of the singlet endpoint cumulant aligned with Z_p and large enough to exceed M_G is a direct same-theory falsifier.
- The endpoint tail Tail_v(sigma) fails to vanish or cannot be bounded uniformly as epsilon -> 0 and sigma -> 0.
- The straight-segment f f cancellation is spoiled by path-ordering at the corner, leaving a nonlocal commutator term not included in K_p.
- Wilson loop renormalization at endpoint boxes requires a new boundary counterterm; then the same-theory condition fails even if positivity is restored.
- The heat-kernel plaquette-sheet regulator changes the locked Wilson algebra in the cutoff limit, invalidating the incidence norm comparison.

## Learning

Cycle 242 turns the post-H,K R problem into a precise endpoint spectral estimate. The actual Yang-Mills input is the singlet-projected connected Wilson four-flux cumulant in heat-kernel plaquette-sheet regulation. The cancellations being used are Wick-square Gram positivity and straight f f incidence cancellation; after them, only endpoint kappa_4 negative spectrum and tails can be a falsifier. The branch learned a valid promotion test: bound (g^4/4)(T_F/N)^2 Lambda_- I_v plus endpoint tails below M_G.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Build the endpoint incidence table for the three hairpins, compute I_v exactly, then evaluate or bound the singlet color contractions kappa_0,kappa_f,kappa_d for one heat-kernel endpoint box to estimate Lambda_-.

# Endpoint-box R polarization for post-H,K Wilson hairpins

## Candidate Lemma

For two nondegenerate plus-channel endpoint boxes, the post-H,K term R_{++}^{ren}/kappa_4 is the flowed connected cumulant of two centered thin Wilson hairpins. Its one-loop form is a positive pair baseline plus a finite connected four-curvature polarization. Positivity is reduced to a computable lower bound on the dimensionless integral Xi_{++}.

## Definitions

- source object: continuum SU(N) Yang-Mills Schwinger family probed by gradient-flow regulated, point-split, centered thin Wilson hairpin observables X_{B,+}^{ren}.
- target object: the endpoint-box coefficient R_{++}^{ren}/kappa_4 entering the post-H,K Schur-Feshbach second-order form in the plus channel.
- controlled interface: identify R_{++}^{ren}=kappa_2(X_{B1,+}^{ren},X_{B2,+}^{ren}) after disconnected-product cancellation and one-hairpin perimeter/cusp subtraction.
- same-theory condition: the flow time tau and point-splitting epsilon regularize observables only, not the Yang-Mills measure; epsilon is removed inside the same continuum Schwinger family and any tau limit uses the same renormalized theory.
- B1 and B2 are endpoint boxes of side ell and separation d; rho=ell/d and eta=tau/d^2.
- h_+ is the plus-channel endpoint-box smearing tensor induced by the two Wilson hairpin sheets; A,B,C,D denote antisymmetric curvature-index pairs.
- Theta_{++} is the nonzero leading bivector overlap of the two endpoint-box smearings.

## Assumptions

- Gauge group SU(N), four Euclidean dimensions, and gauge-invariant Wilson observables; Feynman or background gauge is used only to compute the gauge-invariant coefficient.
- Regulator window epsilon << sqrt(tau) << ell <= d/8, with endpoint boxes away from the reflection plane except for the prescribed boundary collar limit.
- The small-hairpin boundary OPE through quadratic curvature order is valid after the standard Wilson perimeter and cusp renormalizations.
- The one-loop expansion at the flow scale is used only to isolate the finite C4 polarization; the nonperturbative handoff requires an interval or lattice-flow bound on the same Xi_{++}.
- The plus-channel geometry is nondegenerate: Theta_{++} != 0, so the pair baseline is not killed by symmetry.

## Equations

- flowed centered hairpin density: `\displaystyle X_{B,+}^{ren}=\lim_{\epsilon\downarrow0}Z_{hp}^{-1}(\tau,\epsilon)\left[\ell^{-4}\int_B h_+^{\mu\nu\rho\sigma}(x):F_{\mu\nu}^a(\tau,x)F_{\rho\sigma}^a(\tau,x):_{\epsilon}\,dx\right]`. Valid when: Valid when the hairpin is thinner than the endpoint box and the flow time keeps coincident curvature products finite before the continuum limit.
- endpoint R cumulant: `\displaystyle R_{++}^{ren}(B_1,B_2;\tau)=\kappa_2\left(X_{B_1,+}^{ren},X_{B_2,+}^{ren}\right)`. Valid when: Valid when both endpoint observables are centered and renormalized inside the same Schwinger family before taking the cumulant.
- flowed free curvature covariance: `\displaystyle \langle F_{\mu\nu}^a(\tau,x)F_{\rho\sigma}^b(\tau,y)\rangle_0=\delta^{ab}{\mathcal K}_{\mu\nu,\rho\sigma}^{\tau}(x-y),\quad {\mathcal K}_{\mu\nu,\rho\sigma}^{\tau}(z)=T_{\mu\nu,\rho\sigma}(\partial)\int\frac{d^4p}{(2\pi)^4}\frac{e^{ip\cdot z-2\tau p^2}}{p^2}`. Valid when: Applies in the leading flowed perturbative expansion with positive flow time, separated endpoints, and gauge-invariant contractions.
- positive pair baseline: `\displaystyle P_{++}=2(N^2-1){\mathcal G}_{++},\quad {\mathcal G}_{++}=\iint_{B_1\times B_2}h_1^{AB}(x)h_2^{CD}(y){\mathcal K}_{AC}^{\tau}(x-y){\mathcal K}_{BD}^{\tau}(x-y)\,dxdy=\frac{\Theta_{++}^2}{\pi^4d^8}\left(1+O(\rho^2+\eta)\right)`. Valid when: Valid when the endpoint boxes have separation d much larger than their side length and the plus-channel bivector overlap is nonzero.
- one-loop R decomposition: `\displaystyle R_{++}^{ren}=P_{++}+g_\tau^2N(N^2-1)J_{++}^{conn}+O(g_\tau^4)=P_{++}\left[1+\frac{g_\tau^2N}{2}\Xi_{++}+O(g_\tau^4)\right],\quad \Xi_{++}=J_{++}^{conn}/{\mathcal G}_{++}`. Valid when: Requires the same-theory boundary OPE after disconnected products and one-hairpin perimeter-cusp terms have been subtracted.
- absolute polarization majorant: `\displaystyle |\Xi_{++}|\le \Xi_{abs}(\rho,\eta):=\frac{1}{{\mathcal G}_{++}}\int_{B_1^2\times B_2^2}|h_1^{IJ}h_2^{KL}{\mathcal C}_{IJKL}^{(1),red,\tau}|\le C_{box}(1+|\log\eta|)(1+c\rho^2)`. Valid when: Valid when the flowed one-loop four-curvature tensor is integrated against the actual endpoint-box smearing functions.
- post-H,K endpoint lower bound: `\displaystyle Q_+^{box}=C_{++,loc}+R_{++}^{ren}-B_{+R}D^{-1}B_{R+}\ge C_{++,loc}-B_{+R}D^{-1}B_{R+}+P_{++}\left[1-\frac{g_\tau^2N}{2}\Xi_{abs}+O(g_\tau^4)\right]`. Valid when: Applies after H,K have been fixed and the endpoint box is the only unresolved kappa_4 contribution.

## Attempted Derivation

- Use the small-hairpin boundary OPE: after Wilson perimeter/cusp renormalization, the centered hairpin starts with a quadratic flowed-curvature density smeared over the endpoint box.
- Take kappa_2 of the two centered densities. Normal ordering removes same-hairpin self-contractions, and the cumulant removes the product of one-hairpin expectations.
- At Gaussian order, only the two cross-pairings between B1 and B2 survive. Their color trace is delta^{ab}delta^{ab} times two Wick pairings, giving 2(N^2-1), and their geometry is the positive Gram integral G_{++}.
- At order g_tau^2, collect the connected four-curvature cumulant C4^{(1),red,tau}. Tadpoles and one-loop cusp/perimeter pieces are already absorbed in Z_hp; ghost and longitudinal pieces remain only inside the gauge-invariant reduced tensor.
- The color contraction of the reduced connected four-curvature tensor contributes C_A dim(G)=N(N^2-1), so the relative correction is (g_tau^2 N/2)Xi_{++}.
- Gradient-flow factors e^{-tau p^2}, point splitting, and positive endpoint separation make Xi_{++} finite. The first practical bound is the absolute majorant Xi_abs against the actual endpoint smearing.
- Insert the lower bound for R_{++}^{ren} into the post-H,K corrected second-order coefficient Q_+^{box}. Promotion requires the pair baseline, after the worst allowed polarization loss, to exceed the Feshbach leakage gap.

Blocking gap: The missing hard step is a certified evaluation or sharp interval bound for Xi_abs(rho,eta), including ghost, path-ordering, and contact contributions for the actual plus-channel endpoint smearing.

## Falsifiers

- falsifier: the plus-channel endpoint geometry has Theta_{++}=0, making the positive pair baseline vanish before the polarization test starts.
- falsifier: an explicit Xi_{++} evaluation gives 1+(g_tau^2 N/2)Xi_{++} below the leakage margin needed in Q_+^{box}.
- falsifier: the regulator window epsilon << sqrt(tau) << ell << d is empty for the H,K endpoint geometry extracted from the Wilson collar.
- falsifier: a path-ordering or ghost contact term omitted from C4^{(1),red,tau} cancels the claimed pair contribution after the same-theory subtraction.
- falsifier: R_{++}^{ren} survives only for the flowed auxiliary observable and has no valid tau-removal or renormalized Wilson-OPE interpretation in the original Schwinger family.

## Learning

The branch is not looping. The actual post-H,K R term is a same-theory connected Wilson cumulant with an explicitly positive pair part 2(N^2-1)G_{++}; all serious uncertainty is compressed into the finite dimensionless polarization Xi_{++} with color factor N(N^2-1). The valid promotion condition is a lower bound on R_{++}^{ren} strong enough to beat the Schur-Feshbach leakage term.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Write the explicit momentum-space integrand for C4^{(1),red,tau}, including four-gluon, two-three-gluon, ghost, and nonlinear-F insertions; evaluate Xi_{++}(rho,eta) by interval quadrature for rho<=1/8 and eta in the flow window.

# Endpoint-box kappa4 audit for the Wilson Schur-Feshbach handoff

## Candidate Lemma

For a finite Wilson collar/hairpin truncation with H,K already extracted, the post-H,K endpoint-box contribution is controlled by a heat-kernel smeared four-curvature operator. The corrected second-order form is valid and nonnegative if the negative part of this operator is dominated by the Gaussian Hadamard-square term minus the Schur hairpin energy.

## Definitions

- source object: heat-kernel regulated SU(N) Euclidean Yang-Mills Wilson collars, endpoint boxes B_p, and OS-positive Wilson cumulants at smoothing scale sigma.
- target object: the finite kernel-sector matrix P(R_box,sigma+R_rest,sigma)P-B^*E^{-1}B acting on ker(PHP) after H,K are fixed.
- controlled interface: R_ij is identified with the same-theory connected cumulant of vacuum-subtracted quadratic transported curvature fluxes, with disconnected vacuum and perimeter factors cancelled before Schur testing.
- same-theory condition: H,K,R,kappa_4 use the same regulator sigma, basepoint parallel transport, Wilson normalization, counterterm convention, and finite collar geometry.
- Endpoint flux X_i,sigma^a is the heat-kernel smeared curvature two-form through the endpoint box of collar i, transported to a common basepoint.
- C_ij,sigma is the color-diagonal two-flux covariance, and kappa_4,ij,sigma is the fully connected four-flux cumulant remaining after the crossed two-point contractions are removed.
- S_HK=B^*E^{-1}B is the Schur-Feshbach hairpin correction, where E=QHQ is positive on the eliminated finite sector.

## Assumptions

- The finite Schur-Feshbach tangent-cone theorem is available for the extracted H,K block, with E=QHQ bounded below on Q.
- The endpoint Wilson loops are small enough, after heat-kernel smoothing, for the boundary OPE through order g_R^4 to separate quadratic flux terms from a controlled O(g_R^6) remainder.
- Global color invariance gives C_ij,sigma^{ab}=delta^{ab} C_ij,sigma in the vacuum sector.
- The heat-kernel smeared connected four-curvature distribution defines a bounded quadratic form on two-flux endpoint test functions, or else the lemma is demoted to a falsifier test.
- Vacuum subtraction and perimeter/area counterterms are performed before taking connected cumulants, so disconnected one-loop factors do not enter R.

## Equations

- transported endpoint flux: `X_{i,\sigma}^{a}=\int_{B_i} f_{i,\sigma}^{\mu\nu}(x)\,\mathrm{Ad}(U_{x\to b_i})^{ab}F_{\mu\nu}^{b}(x)\,d^4x`. Valid when: Valid when the endpoint collar is heat-kernel smoothed before the continuum limit and the transported curvature is evaluated in the reconstructed Euclidean measure.
- quadratic Wilson endpoint term: `Q_{i,\sigma}=-\frac{g_R^2}{2N}:\!\operatorname{tr}(X_{i,\sigma}^2)\!:\,=-\frac{g_R^2}{4N}:\!X_{i,\sigma}^{a}X_{i,\sigma}^{a}\!:`. Valid when: Applies after diagonal Wilson normalization removes the vacuum and perimeter factors and the endpoint OPE is truncated at quadratic flux order.
- connected R definition: `R_{ij,\sigma}^{\mathrm{box}}=\langle Q_{i,\sigma}Q_{j,\sigma}\rangle_c+\mathcal E_{ij,\sigma}^{(6)}`. Valid when: Requires the same-theory boundary OPE for both Wilson collars and connected cumulants taken after all one-loop normalizations are fixed.
- Gaussian plus kappa4 decomposition: `R_{ij,\sigma}^{\mathrm{box}}=\frac{g_R^4}{8N^2}\sum_{a,b}C_{ij,\sigma}^{ab}C_{ij,\sigma}^{ab}+\frac{g_R^4}{16N^2}\sum_{a,b}\kappa_{iijj,\sigma}^{aabb}+\mathcal E_{ij,\sigma}^{(6)}`. Valid when: Valid when the four-flux moment is decomposed into crossed two-point contractions plus the fully connected four-curvature cumulant.
- color-reduced endpoint formula: `R_{ij,\sigma}^{\mathrm{box}}=\frac{g_R^4(N^2-1)}{8N^2}C_{ij,\sigma}^2+\frac{g_R^4}{16N^2}\kappa_{4,ij,\sigma}+\mathcal E_{ij,\sigma}^{(6)}`. Valid when: Applies when vacuum color symmetry makes the two-flux covariance proportional to delta^{ab} for the chosen transported endpoint boxes.
- negative kappa4 operator bound: `v^*R_{\kappa,\sigma}^{\mathrm{box}}v\ge -\frac{g_R^4}{16N^2}M_{4,\sigma}^-\,\|\Psi_v\|_{L^2(B\times B)}^2,\quad \Psi_v=\sum_i v_i f_{i,\sigma}\otimes f_{i,\sigma}`. Valid when: Valid when the negative spectral part of the smeared connected four-curvature kernel is bounded by M_{4,sigma}^- on endpoint two-flux test functions.
- promotion inequality: `v^*\left(R_{G,\sigma}^{\mathrm{box}}-S_{HK}-\mathcal E_{\sigma}^{\mathrm{OPE}}\right)v\ge \frac{g_R^4}{16N^2}M_{4,\sigma}^-\|\Psi_v\|_2^2\quad\forall v\in\ker(PHP)`. Valid when: Valid as a sufficient finite-dimensional positivity test after H,K extraction and after the endpoint OPE remainder has an operator-norm bound.

## Attempted Derivation

- Fix the heat-kernel regulator K_sigma and use the same transported endpoint boxes used in H,K; no symbolic R_ij model is introduced.
- Expand each normalized endpoint Wilson collar by the boundary OPE: the first nontrivial same-theory term is Q_i=-(g_R^2/2N):tr X_i^2:.
- Compute the connected product <Q_i Q_j>_c. Vacuum and perimeter pieces cancel because the Wilson variables are normalized before cumulants are formed.
- Split the four-flux moment into crossed two-point contractions and the fully connected four-curvature cumulant. With tr(T^aT^b)=delta^{ab}/2, the crossed part is g_R^4(N^2-1)C_ij^2/(8N^2).
- Represent the kappa_4 contribution as an integral operator on two-flux endpoint test functions Psi_v=sum_i v_i f_i tensor f_i. This gives a concrete negative-part norm M_4,sigma^- to compute or bound.
- Insert the finite Schur-Feshbach correction from the known H,K block: the tested matrix is R_box+R_rest-S_HK, not PHP or R alone.

Blocking gap: The missing proof input is a rigorous same-regulator bound on M_4,sigma^- for the connected heat-kernel smeared four-curvature kernel in four-dimensional Yang-Mills.

## Falsifiers

- A lattice or constructive same-theory measurement finds a vector v with v^*R_kappa v below the promotion inequality margin.
- Endpoint contact counterterms in the boundary OPE contribute at order g_R^4 with regulator dependence not shared by H,K.
- The heat-kernel four-curvature kernel is not a bounded quadratic form on endpoint two-flux tests as sigma tends to zero.
- The Schur hairpin energy S_HK exceeds the positive Gaussian Hadamard-square term on a kernel vector even when kappa_4 is set to zero.
- Geometric orientation of the first actual endpoint boxes makes C_ij,sigma vanish or nearly vanish on the relevant polarization vector.
- The O(g_R^6) Wilson OPE remainder is not small compared with R_G-S_HK in the finite truncation.

## Learning

The branch is not looping on OS density or symbolic thresholds. The concrete endpoint-box R term decomposes into a positive color-computed Gaussian square and a single dangerous kappa_4 operator. The valid next invariant is the negative spectral size M_4,sigma^- relative to R_G-S_HK-E_OPE; this is a falsifier-ready quantity rather than a formal placeholder.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

For the first concrete collar/hairpin truncation, build f_i,sigma for its endpoint boxes, compute C_ij,sigma and S_HK, then estimate M_4,sigma^- by either a plaquette-sheet cumulant measurement or a rigorous heat-kernel OPE bound.
