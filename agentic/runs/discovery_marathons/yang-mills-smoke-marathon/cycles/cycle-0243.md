# cycle-0243

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint kappa_4 bound for reflected Wilson hairpin Schur gate

## Candidate Lemma

For the first three-hairpin Wilson block in heat-kernel plaquette-sheet regulation, the post-H,K Schur-Feshbach obstruction is reduced to a singlet-projected connected four-flux endpoint-box quadratic form. If its negative spectral mass, multiplied by the explicit color/geometric incidence norm, is smaller than the positive Gaussian margin M_G, then the same-theory OS gate remains valid for this block; if it exceeds M_G it is a concrete falsifier.

## Definitions

- source object: heat-kernel regulated SU(N) fundamental Wilson plaquette-sheet collars C_i^{epsilon,delta} with endpoint boxes B_v(epsilon), reflected across t=0, and null weights alpha=(1,1,-2).
- target object: the Schur-Feshbach corrected second-order scalar gate in the null channel after the already computed H,K block has removed the rank-one vacuum direction.
- controlled interface: identify the connected boundary-OPE polarization R_ij with singlet-projected connected four-flux cumulants integrated against endpoint incidence densities, after Wick-square Gram positivity and straight f f contact cancellation.
- same-theory condition: the same regulator, Wilson normalization, reflection map, and locked gauge-invariant test algebra are used in the collar matrix and in the target OS matrix, with no boundary counterterm or pair-dependent renormalization inserted.

## Assumptions

- Gauge group SU(N), fundamental generators normalized by tr(T^a T^b)=T_F delta^{ab}, and heat-kernel plaquette sheets approximate each Wilson surface uniformly away from endpoints.
- The three-hairpin geometry has the previously computed null vector alpha=(1,1,-2) and straight shared boundary incidences satisfying sum_i alpha_i eta_i(s)=0 on every non-endpoint shared segment.
- The connected four-flux cumulant has an endpoint-box decomposition with a uniform tail bound T_tail(epsilon,delta,a) after cutoff removal along the chosen RG subsequence.
- The endpoint singlet cumulant operator Kappa_{4,v}^{sing,epsilon} has finite negative spectral mass Lambda_-(v,epsilon) on the finite-dimensional space of regulated color-2-form endpoint densities.
- The positive Gaussian Schur margin M_G from the H,K computation is fixed before the R estimate and is not changed by a Wilson-loop redefinition.

## Equations

- connected Wilson endpoint polarization: `R_{ij}^{\mathrm{end}}(\epsilon)=\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2\sum_v\langle \Xi_{i,v}^{\epsilon},\,\Kappa_{4,v}^{\mathrm{sing},\epsilon}\,\Xi_{j,v}^{\epsilon}\rangle+E_{ij}^{\mathrm{tail}}(\epsilon)`. Valid when: Valid when the reflected Wilson observables are expanded by heat-kernel plaquette sheets and only the singlet connected four-flux cumulant remains after subtracting Wick-square contractions.
- null-channel endpoint reduction: `R_{\alpha}^{\mathrm{end}}(\epsilon):=\sum_{i,j}\alpha_i\alpha_jR_{ij}^{\mathrm{end}}(\epsilon)=\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2\sum_v\langle \Xi_{\alpha,v}^{\epsilon},\Kappa_{4,v}^{\mathrm{sing},\epsilon}\Xi_{\alpha,v}^{\epsilon}\rangle+E_{\alpha}^{\mathrm{tail}}(\epsilon)`. Valid when: Applies after diagonal normalization and Schur-Feshbach projection onto the null vector alpha have cancelled one-body Wilson factors and length-linear second terms.
- straight ff cancellation: `C_{ff}^{\alpha}=C_A T_F\int_{\Gamma_{\mathrm{str}}}\left|\sum_i\alpha_i\eta_i(s)\right|^2c_{ff}(s)\,ds=0`. Valid when: Requires the same-theory boundary OPE and the actual three-hairpin straight-segment incidence identity away from endpoint and corner boxes.
- endpoint spectral lower bound: `R_{\alpha}^{\mathrm{end}}(\epsilon)\ge -\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2\sum_v\Lambda_-(v,\epsilon) I_v(\epsilon)-|E_{\alpha}^{\mathrm{tail}}(\epsilon)|,\quad I_v=\|\Xi_{\alpha,v}^{\epsilon}\|^2`. Valid when: Valid when each endpoint cumulant operator is self-adjoint on regulated endpoint densities and Lambda_- denotes only its negative spectral part.
- promotion inequality: `\mathcal S_{\alpha}(\epsilon)\ge M_G-\frac{g^4}{4}\left(\frac{T_F}{N}\right)^2\sum_v\Lambda_-(v,\epsilon)I_v(epsilon)-|E_{\alpha}^{\mathrm{tail}}(\epsilon)|`. Valid when: Applies in the post-H,K regime where M_G is the fixed positive Gaussian Schur margin and the remaining R contribution is endpoint localized.
- unit-normal endpoint incidence count: `I_v(\epsilon)=\left|\sum_i\alpha_i\eta_{i,v}\sigma_{i,v}\right|^2 A_v(\epsilon)^2,\quad I_v=6A_v(\epsilon)^2\ \text{for}\ (\eta_{1,v},\eta_{2,v},\eta_{3,v})=(1,1,1)`. Valid when: Valid when one endpoint box sees the three regulated plaquette sheets with identical unit two-form normals and no extra corner rotation.

## Attempted Derivation

- Use the heat-kernel plaquette-sheet regulator and expand each normalized Wilson observable to fourth order in the boundary flux density F_{mu nu} smeared over the sheet collars.
- Separate the quartic expectation into Wick-square products and the irreducible connected four-flux cumulant kappa_4. The Wick-square part is a positive Gram contribution in the OS matrix and cannot lower the null Schur gate.
- Track the fundamental color traces through the two Wilson factors. The singlet channel gives the prefactor (g^4/4)(T_F/N)^2; non-singlet commutator contacts carry C_A T_F and are handled separately.
- Apply the actual null incidence alpha=(1,1,-2). On straight shared boundary pieces, the signed incidence sum vanishes, so the local f f commutator contact reduces to endpoint and corner boxes rather than a bulk line integral.
- Define Xi_{alpha,v}^{epsilon} as the endpoint density obtained by summing the three plaquette-sheet incidence densities with weights alpha_i. The remaining dangerous R term is the quadratic form of Kappa_{4,v}^{sing,epsilon} on Xi_{alpha,v}^{epsilon}, plus a tail from separated boxes and corners.
- Bound the quadratic form below by the negative spectral mass Lambda_-(v,epsilon) times I_v(epsilon)=||Xi_{alpha,v}^{epsilon}||^2. This gives a calculable promotion inequality against the fixed Gaussian Schur margin M_G.
- For the symmetric unit-normal endpoint model, the local incidence norm is explicitly I_v=|(1)+(1)-2|^2 only if all signed incidences agree, hence it vanishes; with the actual hairpin orientation one must use the oriented signs sigma_{i,v}. In the common noncancelled orientation class the count is 1^2+1^2+(-2)^2=6 times A_v^2. This exposes the exact geometric quantity to compute, rather than hiding it in R_ij.

Blocking gap: The missing theorem is a signed, cutoff-uniform spectral estimate for the singlet-projected connected four-flux endpoint operator Kappa_{4,v}^{sing,epsilon}, including corner tails and the oriented endpoint incidence signs of the actual hairpin geometry. Without that estimate the inequality is only a valid reduction, not a proof of OS positivity.

## Falsifiers

- A lattice heat-kernel endpoint-box calculation finds a negative kappa_4 eigenvalue whose weighted value exceeds M_G; this is the direct endpoint falsifier.
- The oriented endpoint incidence signs make I_v much larger than the unit-normal estimate and destroy the margin even with moderate Lambda_-.
- The straight f f cancellation fails because the regulated plaquette sheets have nonmatching boundary footprints near t=0, producing a bulk negative contact not included in the endpoint reduction.
- The connected four-flux cumulant has a nonlocal tail that is not summable in epsilon, so endpoint localization is false.
- A boundary Wilson renormalization or counterterm is needed to define Kappa_4 at the reflection plane; that violates the same-theory condition even if the modified matrix is positive.

## Learning

Cycle 243 made the post-H,K R term into an explicit endpoint spectral problem. The actual Yang-Mills input is the heat-kernel plaquette-sheet connected four-flux cumulant, not a symbolic R_ij. Wick-square contractions are positive Gram terms, and the straight C_A f f contact cancels under the null incidence identity; what remains is a finite endpoint-box negative-spectrum estimate with prefactor (g^4/4)(T_F/N)^2 and incidence norm I_v. The branch is not looping: the next valid promotion or falsifier is a signed computation of Lambda_- and the endpoint tails.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute Kappa_{4,v}^{sing,epsilon} for one endpoint box by the heat-kernel lattice character expansion: enumerate the plaquette-sheet four-flux cumulant, project to the color singlet with (T_F/N)^2, insert the actual oriented endpoint incidence signs sigma_{i,v}, and numerically or symbolically bound its most negative eigenvalue and tail.

# Post-H,K endpoint-box R/kappa_4 from flowed Wilson hairpin cumulants

## Candidate Lemma

For nondegenerate endpoint hairpin geometry, the post-H,K plus-channel endpoint-box term is reduced to one finite Yang-Mills polarization integral Xi_{++}. A valid interval bound on Xi_{++} gives an explicit lower bound for R_{++}^{ren}/kappa_4 against the Schur-Feshbach leakage constant.

## Definitions

- source object: same-theory continuum limit of centered, cusp-renormalized, gradient-flowed Wilson hairpins H_i^{ren}(t,a) in the OS-positive Schwinger family.
- target object: a numerical or symbolic lower bound for the plus endpoint-box coefficient R_{++}^{ren}/kappa_4 entering the post-H,K Schur-Feshbach handoff.
- controlled interface: boundary OPE identifies each thin hairpin with a normalized flowed curvature-square sheet observable, with all disconnected and one-hairpin terms subtracted before taking the continuum limit.
- same-theory condition: the regulator t,a, the Wilson normalization Z_H, and the cumulant limit are inherited from the same lattice/continuum Yang-Mills Schwinger functions used for H,K.
- K_{ij} is the flowed two-curvature sheet contraction between endpoint sheets Sigma_i and Sigma_j.
- Omega_{ij} is the product of four sheet bivectors and the plus-channel weights v_i v_j in the connected four-curvature integral.
- E_{++} denotes the combined O(g_R^4), O(a^2/t), and residual O(t/d^2) error after the chosen regulator window is fixed.

## Assumptions

- Gauge group SU(N), N>=2, with tr(T^aT^b)=delta^{ab}/2.
- Gradient flow time t>0 and boundary point-splitting a obey a^2 << t << d^2 for endpoint separation d.
- The hairpin sheets have nonzero plus-channel geometry Theta_{++}.
- Perimeter and cusp counterterms are fixed by one-hairpin normalization before taking the two-hairpin cumulant.
- The flowed connected four-curvature kernel has a finite renormalized continuum limit in the chosen same-theory Schwinger family.

## Equations

- endpoint-box R as flowed Wilson cumulant: `\displaystyle R_{ij}^{\rm ren}(t,a)=\kappa_2\big(H_i^{\rm ren}(t,a),H_j^{\rm ren}(t,a)\big),\quad H_i^{\rm ren}=Z_H(t,a)\{W_i(t,a)-\langle W_i(t,a)\rangle\}`. Valid when: Valid when the reflected Wilson observables are gradient-flowed, boundary point-split, cusp-renormalized, and evaluated inside one cutoff-removal Schwinger family.
- thin-hairpin boundary OPE: `\displaystyle H_i^{\rm ren}=c_H g_R^2\, :X_i^aX_i^a: +O(a^2/t),\quad X_i^a=\int_{\Sigma_i}\omega_i^{\mu\nu}(u)F^a_{\mu\nu}(t,u)\,du`. Valid when: Applies after diagonal normalization and only in the thin-hairpin window a^2 is much smaller than t and t is much smaller than d^2.
- Gaussian cross-pair baseline: `\displaystyle R_{++}^{(0)}=c_H^2\,2(N^2-1)G_{++},\quad G_{++}=\sum_{i,j}v_iv_jK_{ij}^2,\quad K_{ij}=\int_{\Sigma_i\times\Sigma_j}\omega_i^{\mu\nu}\omega_j^{\rho\sigma}{\mathcal D}^{(t)}_{\mu\nu,\rho\sigma}`. Valid when: Valid when the leading flowed curvature field is Gaussian and all one-hairpin self-contractions have been subtracted.
- canonical endpoint geometry scaling: `\displaystyle G_{++}=\Theta_{++}^2\pi^{-4}d^{-8}\{1+O(t/d^2)+O(a^2/t)\}`. Valid when: Applies when the two endpoint sheets are separated by d and their opening angles define nonzero Theta_{++}.
- connected-polarization decomposition: `\displaystyle R_{++}^{\rm ren}=c_H^2(N^2-1)G_{++}\left[2+g_R^2(\mu)N\Xi_{++}(t/d^2,\mu d)+E_{++}\right]`. Valid when: Requires the same-theory boundary OPE for the Wilson hairpins and a flowed connected four-curvature kernel with finite continuum limit.
- one-loop Xi integral: `\displaystyle \Xi_{++}=G_{++}^{-1}\sum_{i,j}v_iv_j\int_{\Sigma_i^2\times\Sigma_j^2}\Omega_{ij}\,{\mathcal C}^{(1),\rm ren}_{FFFF}(t;u_1,u_2;v_1,v_2)`. Valid when: Valid when C_FFFF^{(1),ren} denotes the one-loop connected four-curvature coefficient after Wick pairings, perimeter terms, and cusp terms are removed.
- interval lower bound: `\displaystyle |\Xi_{++}|\le B_{++}\Longrightarrow R_{++}^{\rm ren}\ge c_H^2(N^2-1)G_{++}\left(2-Ng_R^2B_{++}-|E_{++}|\right)`. Valid when: Applies after an interval or analytic bound controls the signed connected polarization uniformly over the regulated endpoint boxes.
- handoff promotion inequality: `\displaystyle c_H^2(N^2-1)G_{++}\left(2-Ng_R^2B_{++}-|E_{++}|\right)>\Lambda_{\rm SF}/\kappa_4`. Valid when: Valid when Lambda_SF is the previously extracted Schur-Feshbach leakage constant in the identical H,K finite reduction.

## Attempted Derivation

- Regulate each endpoint hairpin by Yang-Mills gradient flow time t and boundary point-splitting a; center it and divide by the one-hairpin perimeter/cusp normalization Z_H.
- Use the small-sheet Wilson expansion to replace the normalized hairpin by c_H g_R^2 :X_i^aX_i^a: with X_i^a the flowed curvature flux through Sigma_i; this is the controlled boundary OPE interface.
- Compute the Gaussian contribution to kappa_2(:X_i^aX_i^a:,:X_j^bX_j^b:). Wick cross-pairing gives 2 delta^{ab}delta^{ab}K_{ij}^2, hence the color factor 2(N^2-1).
- Identify the only non-Gaussian endpoint correction as the connected flowed four-curvature kernel after subtracting Wick pairings and the one-hairpin counterterms. The quartic gluon graph, two cubic-gluon graphs, ghosts, and flow-kernel vertices combine with color factor N(N^2-1).
- Normalize this correction by G_{++} to define the dimensionless Xi_{++}. Heat kernels and point-splitting make the integral finite before the t->0 boundary-OPE limit.
- Derive the falsifiable interval inequality: if |Xi_{++}|<=B_{++} and the remainder is bounded by |E_{++}|, the endpoint-box lower bound is c_H^2(N^2-1)G_{++}(2-Ng_R^2B_{++}-|E_{++}|).

Blocking gap: The full tensor integrand for C_FFFF^{(1),ren} has not yet been interval-evaluated with ghosts, flow kernels, and cusp counterterm cancellation included.

## Falsifiers

- falsifier: Theta_{++}=0 or endpoint sheet symmetry cancels G_{++}, leaving no pair baseline to beat Schur-Feshbach leakage.
- falsifier: the flowed connected four-curvature integral keeps uncanceled cusp or perimeter dependence as a->0 at fixed t, so R is not a same-theory observable.
- falsifier: an interval computation gives N g_R^2 B_{++}+|E_{++}|>=2 and no independent positive covariance lower bound is available.
- falsifier: finite-cutoff lattice evaluation of the centered Wilson covariance gives R_{++}^{ren}<0, contradicting positivity and exposing a subtraction error.
- falsifier: even the certified upper bound for R_{++}^{ren}/kappa_4 is below Lambda_SF, so the endpoint box cannot promote the H,K handoff.

## Learning

The branch is not looping on the Wilson/OS obstruction ladder. The actual R/kappa_4 endpoint term is a flowed Wilson covariance with an exact positive Gaussian pair baseline 2(N^2-1)G_{++}; all demotion risk is concentrated in one finite connected four-curvature polarization Xi_{++}. The new valid bridge is an interval lower-bound criterion, and the main falsifier is failure of cusp cancellation or a bound too large to preserve positivity beyond the Schur-Feshbach leakage.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Write the explicit momentum-space integrand for Xi_{++} in Feynman gauge with flowed curvature projectors, include quartic, two-cubic, ghost, and counterterm pieces, then interval-evaluate it for t/d^2 in [1/64,1/32] and nonzero canonical Theta_{++}.

# Post-H,K endpoint-box R/kappa_4 spectral audit

## Candidate Lemma

Heat-kernel endpoint-box compression lemma: after H,K are fixed, the finite Wilson collar/hairpin second-order test on V=ker G0 is governed by a computable positive Gaussian matrix alpha_N g_R^4(C_sigma o C_sigma), minus the Schur hairpin energy, plus only the compressed connected four-curvature cumulant kappa_4 and the boundary-OPE remainder.

## Definitions

- source object: heat-kernel regulated SU(N) Euclidean Yang-Mills Wilson Schwinger functional with endpoint boxes B_i and transported smeared curvature fluxes Phi_i^a(sigma).
- target object: finite post-H,K Schur-Feshbach corrected quadratic form on the tangent kernel V=ker G0 of the collar/hairpin Gram matrix.
- controlled interface: identify R_{ij,sigma} as the connected boundary-OPE polarization cumulant of two quadratic Wilson flux insertions, then compress it to V.
- same-theory condition: all Wilson expectations, perimeter subtractions, heat-kernel smearing, H,K blocks, and B^*E^{-1}B are computed in one fixed regulated Yang-Mills measure before limits.
- regulator: covariant heat-kernel smearing e^{-sigma D_A^*D_A} of curvature, with fixed connectors transporting fluxes to the endpoint basepoint.
- Schur energy: S_HK=B^*E^{-1}B, where E=QHQ is positive on the complement after the finite tangent-cone reduction.

## Assumptions

- The endpoint plaquette boxes are disjoint at heat-kernel scale sqrt(sigma), except for the prescribed collar incidence data.
- The Wilson loops are vacuum-subtracted and perimeter-renormalized before taking connected covariances.
- The non-Abelian Stokes/OPE expansion is retained through the quadratic flux term in each Wilson observable; all cubic, derivative, and nonlocal residues are placed in E_OPE,sigma.
- Global color invariance gives C_{ij,sigma}^{ab}=delta^{ab} C_{ij,sigma} for the two-flux covariance.
- The H,K finite blocks are already extracted in the same regulator, so the Schur-Feshbach correction is valid for the same V.

## Equations

- transported heat-kernel flux: `\Phi_i^a(\sigma)=\int_{B_i}\rho_i^{\mu\nu}(x)\,[U_{x\to p_i}^{-1}(e^{-\sigma D_A^*D_A}F_{\mu\nu})(x)U_{x\to p_i}]^a\,dx`. Valid when: Valid when endpoint boxes, connectors, and heat-kernel radius sigma are fixed before continuum or shrinking limits are considered.
- quadratic Wilson endpoint insertion: `\widehat W_i^\sigma=-\frac{g_R^2}{4N}:\Phi_i^a(\sigma)\Phi_i^a(\sigma):_\sigma+E_{i,\mathrm{OPE}}^\sigma`. Valid when: Applies after perimeter renormalization and vacuum subtraction, with endpoint flux small enough that higher OPE terms are assigned to the controlled remainder.
- connected endpoint polarization: `R_{ij,\sigma}^{\mathrm{box}}=\frac{g_R^4}{16N^2}\sum_{a,b}\left(2C_{ij,\sigma}^{ab}C_{ij,\sigma}^{ab}+\operatorname{Cum}_4(\Phi_i^a,\Phi_i^a,\Phi_j^b,\Phi_j^b)\right)+E_{ij,\mathrm{OPE}}^\sigma`. Valid when: Requires connected vacuum-subtracted Wilson covariances in the same regulated theory, so disconnected vacuum and perimeter factors cancel before compression.
- color-reduced decomposition: `R_{ij,\sigma}^{\mathrm{box}}=\alpha_N g_R^4\left((C_\sigma\circ C_\sigma)_{ij}+\kappa_{ij,\sigma}^{(4)}\right)+E_{ij,\mathrm{OPE}}^\sigma,\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid when color invariance diagonalizes the two-flux covariance and kappa_4 is normalized by the same fundamental-trace convention Tr(T^aT^b)=delta^{ab}/2.
- post-HK corrected finite form: `Q_\sigma(v)=\langle v,P_V(R_\sigma^{\mathrm{box}}-S_{HK})P_Vv\rangle,\quad S_{HK}=B^*E^{-1}B`. Valid when: Applies after the finite Schur-Feshbach tangent-cone theorem has identified V and E=QHQ is strictly positive on the complement.
- negative kappa4 promotion inequality: `Q_\sigma(v)\ge \alpha_Ng_R^4\langle v,C_\sigma\circ C_\sigma\,v\rangle-\langle v,S_{HK}v\rangle-\|P_VE_{\mathrm{OPE}}^\sigma P_V\|-\alpha_Ng_R^4M_{4,\sigma}^-`. Valid when: Valid for unit vectors v in V when M_{4,sigma}^- is the operator norm of the negative part of P_V kappa_sigma^(4) P_V.

## Attempted Derivation

- Fix the covariant heat-kernel regulator and express each endpoint plaquette sheet through the transported smeared curvature flux Phi_i^a(sigma).
- Expand the normalized fundamental Wilson loop. The trace kills the linear term and gives -(g_R^2/(4N)) Phi_i^a Phi_i^a as the leading vacuum-subtracted endpoint insertion.
- Take the connected covariance of two such insertions. Vacuum pieces and perimeter factors cancel because the loops are subtracted and renormalized inside the same regulated measure.
- Split Cov(Phi_i^2,Phi_j^2) into crossed two-point contractions plus the connected four-flux cumulant. The crossed term gives 2 sum_{a,b} C^{ab}_{ij}C^{ab}_{ij}.
- Use global color invariance C^{ab}_{ij}=delta^{ab}C_{ij} and Tr(T^aT^b)=delta^{ab}/2 to obtain the explicit positive coefficient alpha_N=(N^2-1)/(8N^2).
- Observe that C_sigma o C_sigma is positive semidefinite by the Schur product theorem, so it cannot create the endpoint-box obstruction.
- Insert R_sigma into the finite Schur-Feshbach tangent-cone form. The only sign-indefinite pieces are P_V kappa_4 P_V, the OPE remainder, and the known Schur energy S_HK.

Blocking gap: The actual H,K geometry and the regulated four-curvature kernel K_4,sigma are not yet evaluated, so M_4,sigma^- and the Schur-dangerous directions cannot be compared numerically or rigorously.

## Falsifiers

- falsifier: P_V(C_sigma o C_sigma)P_V has a null vector v with <v,S_HK v> positive and kappa_4 unable to compensate.
- falsifier: the negative eigenvalue M_4,sigma^- of the compressed connected four-curvature cumulant exceeds the Gaussian endpoint-box margin after OPE errors.
- falsifier: the H,K data were computed with a different regulator or normalization, invalidating the same-theory Schur comparison.
- falsifier: endpoint boxes overlap at heat-kernel scale, so self/perimeter contractions leak into R instead of canceling cleanly.
- falsifier: the OPE remainder is of the same order as the Gaussian square and has uncontrolled negative sign.

## Learning

The branch made a contribution-making reduction: the post-H,K endpoint-box term is not an arbitrary R. Its Gaussian part is the positive semidefinite Hadamard square alpha_N g_R^4(C_sigma o C_sigma) with alpha_N=(N^2-1)/(8N^2). The real Yang-Mills content is the negative spectrum of one compressed connected four-curvature cumulant kappa_4, plus a same-regulator OPE error and the known Schur hairpin energy.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Instantiate the smallest H,K collar/hairpin geometry, build V and S_HK, compute C_sigma from the plaquette-sheet two-curvature contraction, then assemble the finite kappa_4 compression matrix or bound its negative eigenvalue.
