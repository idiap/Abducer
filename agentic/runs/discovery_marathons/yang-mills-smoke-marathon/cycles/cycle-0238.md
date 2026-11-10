# cycle-0238

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Heat-kernel computation of the connected Wilson boundary polarization R

## Candidate Lemma

For the first three-hairpin Wilson collar block, heat-kernel plaquette-sheet regularization expresses the null-polarized second boundary coefficient as a positive Wick-square Gram term plus an irreducible connected four-flux cumulant plus an f f commutator contact. In the actual H-derived footprint geometry, the translation-invariant local f f bulk overlap cancels in the null polarization; only endpoint/corner tails and the irreducible four-flux cumulant can be a same-theory falsifier.

## Definitions

- source object: cutoff SU(N) Yang-Mills with reflection-positive heat-kernel plaquette sheets, normalized fundamental Wilson hairpins W_i(δ,ε), and boundary curvature F_{0α,ε} parallel-transported to a common base point.
- target object: the null-channel second boundary-OPE coefficient R_v controlling the corrected Schur-Feshbach OS gate for the continuum Wilson hairpin block.
- controlled interface: R_ij is extracted as the δ^2 coefficient of the normalized Wilson OS quotient after diagonal self-renormalization, rank-one vacuum Schur removal, and subtraction of one-body collar factors.
- same-theory condition: no pair-dependent boundary counterterm or altered Wilson algebra is introduced while ε and the lattice spacing are removed.
- notation: α_F=T_F/d_F, C_F d_F=T_F(N^2-1), C_A=N, v=(1,1,-2), and M_{4,c}(ε) denotes the operator norm of the smeared truncated four-curvature distribution on the boundary footprint test space.

## Assumptions

- The regulator is a gauge-invariant heat-kernel plaquette-sheet regulator with a<<ε<<δ before the collar limit.
- The selected hairpin footprints have H-derived pairwise overlap multiplicities L12=4 and L13=L23=1, with the same local orientation sign on the straight shared pieces.
- The boundary OPE has a uniform remainder allowing the δ expansion of each finite OS matrix entry before ε→0.
- Diagonal Wilson self factors and length-linear one-body terms have already been locked and removed from the quotient matrix.
- The commutator contact is local along coincident straight boundary footprints up to endpoint/corner heat-kernel tails.

## Equations

- heat-kernel boundary flux variable: `\Phi_i^a(\varepsilon)=\int_{\Gamma_i} j_i^\alpha(x)\,{\mathcal U}_{x\to *}^{ab}F_{0\alpha,\varepsilon}^b(0,x)\,d\sigma(x)`. Valid when: Valid when the heat-kernel radius is larger than the lattice spacing and smaller than every macroscopic footprint scale.
- irreducible four-flux part of R: `R_{ij}^{4c,\varepsilon}=\frac{g^4\alpha_F^2}{4}\int_{\Gamma_i^2\times\Gamma_j^2} j_i(x_1)j_i(x_2)j_j(y_1)j_j(y_2)\,\kappa_4^\varepsilon(F^a_{x_1},F^a_{x_2},F^b_{y_1},F^b_{y_2})`. Valid when: Applies after diagonal normalization and after the two-pair Wick contractions have been separated from the truncated four-flux cumulant.
- Wick-square positivity: `\mathcal R_v^{\mathrm{Wick},\varepsilon}=\frac{g^4\alpha_F^2}{2}\left\|\sum_i v_i\,G_\varepsilon^{1/2}(j_i\otimes j_i)\right\|^2\ge 0,\qquad v=(1,1,-2)`. Valid when: Valid when the reflected two-flux covariance G_epsilon is positive on the heat-kernel boundary test space.
- local nonabelian commutator contact: `R_{ij}^{ff,\mathrm{bulk},\varepsilon}=-\frac{g^4C_FC_A}{12}\,\chi_{ij}\,\ell(\Gamma_i\cap\Gamma_j)+O_{\partial\Gamma}(\varepsilon)`. Valid when: Requires the coincident-footprint limit where the heat kernel sees a locally straight shared boundary segment.
- actual-footprint null cancellation of f f bulk contact: `\mathcal R_v^{ff,\mathrm{bulk},\varepsilon}=2R_{12}^{ff}-4R_{13}^{ff}-4R_{23}^{ff}=-\frac{g^4C_FC_A\chi}{12}(2\cdot4-4\cdot1-4\cdot1)+O_{\partial\Gamma}(\varepsilon)=O_{\partial\Gamma}(\varepsilon)`. Valid when: Valid when the three selected hairpin footprints have the H-derived overlap multiplicities four, one, and one with common orientation sign.
- first calculable cumulant bound: `|\mathcal R_v^{4c,\varepsilon}|\le \frac{g^4\alpha_F^2}{4}\,\|\mathcal J_v\|_{\varepsilon,4}\,M_{4,c}(\varepsilon),\qquad \mathcal J_v=2J_{12}-4J_{13}-4J_{23}`. Valid when: Applies once the regulated truncated four-curvature distribution is bounded on the tensor boundary footprint norm used by the plaquette-sheet tests.

## Attempted Derivation

- Choose the heat-kernel plaquette-sheet regulator and write each collar hairpin as a normalized Wilson exponential whose boundary-sensitive part is the smeared curvature flux Φ_i(ε).
- Expand the logarithm of the normalized reflected Wilson quotient to second boundary order. The color trace of the quadratic Wilson term contributes α_F Φ_i^aΦ_i^a, so the two-pair contraction is a Wick-square Gram matrix.
- Polarize by the previously isolated null vector v=(1,1,-2). The Wick-square contribution becomes a squared norm and is therefore not the negative second-order falsifier.
- Evaluate the path-ordering commutator contact using N^{-1}Tr([T^a,T^b][T^a,T^b])=-C_A C_F. For a locally straight coincident footprint, the contact is proportional to the oriented overlap length.
- Insert the actual first-block overlap multiplicities L12=4 and L13=L23=1. The null-polarized local bulk commutator coefficient is proportional to 2L12-4L13-4L23 and cancels, leaving only endpoint/corner heat-kernel tails.
- The remaining dangerous term is the irreducible connected four-flux cumulant κ4 integrated against the polarized footprint tensor J_v, plus any finite endpoint contact not absorbed by allowed diagonal Wilson normalization.

Blocking gap: There is still no rigorous continuum-uniform sign or size estimate for the heat-kernel smeared connected four-curvature cumulant κ4 on coincident reflection-plane Wilson footprints.

## Falsifiers

- A direct heat-kernel plaquette computation finds an f f contact with a bilocal footprint kernel, not a local overlap density; then the bulk cancellation is false.
- The irreducible connected four-flux cumulant has a negative null-polarized finite part larger than the positive Schur reserve; this is the main remaining falsifier.
- Endpoint or cusp heat-kernel tails leave a pair-dependent finite boundary counterterm after diagonal normalization, violating the same-theory condition.
- The orientation signs χ12, χ13, χ23 are not common for the actual reflected hairpin sheets, so the computed local commutator cancellation must be rejected.
- The bound M_{4,c}(ε) diverges after standard Wilson renormalization in a way not removable by locked one-body factors.

## Learning

The branch made a concrete R computation rather than restating the obstruction ladder. Heat-kernel Wilson contractions show that the Wick-square part is a positive Gram term, and the local nonabelian f f commutator bulk contact cancels in the actual three-hairpin null geometry. The only remaining dangerous R contribution is the irreducible connected four-flux boundary cumulant plus endpoint/corner tails. Thus the branch is not looping; it has narrowed the possible falsifier to a specific regulated κ4 estimate.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute κ4 for the polarized footprint tensor J_v using the heat-kernel plaquette action: enumerate the four plaquette-sheet contractions touching the reflection plane, separate color tensors δδ and f f, subtract Wick pairs, and estimate the finite endpoint contribution for the three actual hairpin footprints.

# Gauge-Invariant Nontriviality Witness Selection: flowed hairpin R-kernel extraction

## Candidate Lemma

For two disjoint boundary-collar Wilson hairpins, gradient flow, boundary point-splitting, centering, and perimeter/cusp renormalization reduce the normalized cumulant R_{ij} to a positive Wick-square curvature contraction plus one connected four-curvature polarization term. This is the actual Yang-Mills input needed by the corrected Schur-Feshbach plus-channel test.

## Definitions

- source object: OS-positive continuum SU(N) Yang-Mills Schwinger functional with flowed gauge-invariant Wilson hairpin observables.
- target object: the finite H,K Schur-Feshbach second-order coefficient for the first collar/hairpin positivity test.
- controlled interface: gradient-flow and point-split Wilson hairpin cumulants are formed at cutoff, renormalized, centered, and only then matched to the finite H,K matrix entry.
- same-theory condition: all limits use the same bare sequence, coupling normalization, reflection, and Wilson-loop counterterms as the OS reconstruction.
- B_\tau is the Yang-Mills gradient-flow connection and W_\tau(\gamma) is the fundamental normalized Wilson loop of B_\tau.
- H_i^{ren}=Z_{per}^{-1}Z_{cusp}^{-1}(W_\tau(\gamma_{i,\varepsilon,\eta})-\langle W_\tau(\gamma_{i,\varepsilon,\eta})\rangle) is the centered renormalized thin hairpin.
- \sigma_i^{\mu\nu} is the oriented boundary-collar bivector of hairpin i, and d_{ij} is its boundary separation from j.
- \mathcal R_{++}^{ren} is the plus-channel polarization obtained by contracting \mathcal R_{ij}^{ren} with the normalized plus vector in the finite H,K reduction.

## Assumptions

- The hairpins are disjoint, have fixed cusp angle, and satisfy \sqrt\tau,\eta\ll\varepsilon\ll d_{ij}.
- Fundamental generators obey tr(T^aT^b)=\delta^{ab}/2, and curvature insertions between distinct points are adjoint-parallel-transported before color contraction.
- The small-loop boundary OPE is valid after the same perimeter and cusp counterterms used for the Wilson observables.
- The flowed curvature two-point function has the standard short-distance tensor leading term, with interaction corrections assigned to the connected remainder.
- A nonperturbative OPE remainder bound for the flowed connected four-curvature cumulant is not assumed proven; it is the named blocker.

## Equations

- normalized connected hairpin kernel: `\mathcal R_{ij}^{\rm ren}=\lim_{\varepsilon\downarrow0}\varepsilon^{-8}\,\kappa_2\!\left(H_{i,\tau,\varepsilon,\eta}^{\rm ren},H_{j,\tau,\varepsilon,\eta}^{\rm ren}\right),\qquad \sqrt\tau,\eta=o(\varepsilon),\ d_{ij}\ {\rm fixed}.`. Valid when: Valid when the reflected Wilson hairpins are disjoint before the small-loop limit and the same perimeter, cusp, and centering subtractions are used for both factors.
- boundary small-loop OPE: `\varepsilon^{-4}H_i^{\rm ren}=-\frac{g^2}{4N}\,\sigma_i^{\mu\nu}\sigma_i^{\rho\sigma}\,:[F^a_{\mu\nu}F^a_{\rho\sigma}]_R:(x_i)+O(\varepsilon^2 d_{ij}^{-2}).`. Valid when: Applies after diagonal normalization of the cusp-smooth hairpin, with fixed collar geometry and separation much larger than the hairpin thickness.
- Wick-plus-connected decomposition: `\mathcal R_{ij}^{\rm ren}=c_h^2\sigma_i^{\mu\nu}\sigma_i^{\rho\sigma}\sigma_j^{\alpha\beta}\sigma_j^{\gamma\delta}\left[2G^{ab}_{\mu\nu,\alpha\beta}(x_i,x_j)G^{ab}_{\rho\sigma,\gamma\delta}(x_i,x_j)+C^{ab,\rm ren}_{\mu\nu\rho\sigma;\alpha\beta\gamma\delta}(x_i,x_j)\right],\quad c_h=\frac{g^2}{4N}.`. Valid when: Requires the same-theory boundary OPE and the cancellation of the disconnected Wilson product together with all one-hairpin self-contractions.
- explicit positive pair term: `\mathcal G_{ij}=c_h^2\frac{2(N^2-1)}{\pi^4d_{ij}^8}\,\Theta_{ij}^2,\qquad \Theta_{ij}=\sigma_i^{\mu\nu}\sigma_j^{\alpha\beta}\Pi_{\mu\nu,\alpha\beta}(\widehat{x_i-x_j}).`. Valid when: Valid when the leading flowed curvature propagator is evaluated at boundary separation d_{ij} and interaction corrections are not folded into the pair term.
- dimensionless four-curvature falsifier ratio: `\chi_{ij}:=\frac{\mathcal C_{ij}^{\rm ren}}{\mathcal G_{ij}},\qquad |\chi_{ij}|\le C_N g^2(1/d_{ij})+C_{np}(\Lambda d_{ij})^4+o(1)\ \Rightarrow\ \mathcal R_{ij}^{\rm ren}=\mathcal G_{ij}(1+\chi_{ij}).`. Valid when: Valid when asymptotic freedom and a flowed composite-OPE remainder estimate control the connected four-curvature polarization at short collar distance.
- corrected plus-channel insertion: `Q_{+}^{\rm ren}=Q_{+,0}^{\rm SF}+\mathcal R_{++}^{\rm ren},\qquad Q_{+,0}^{\rm SF}=p+2q+r-\frac{(s+t)^2}{\delta}.`. Valid when: Applies when the finite Schur-Feshbach reduction has already normalized the plus vector and the Wilson cumulant supplies exactly the missing H,K matrix entry.

## Attempted Derivation

- Start with two centered renormalized flowed hairpins H_i^{ren}, H_j^{ren}; centering cancels the disconnected Wilson product, while Z_per and Z_cusp cancel one-hairpin perimeter and cusp self-contractions.
- Use the nonabelian small-loop expansion. Since tr F=0, the first gauge-invariant term is quadratic in curvature: H_i^{ren} contributes -(g^2/4N)\varepsilon^4\sigma_i\sigma_i:[FF]_R(x_i).
- Divide the two-hairpin cumulant by \varepsilon^8 and pass to the boundary OPE coefficient; the finite limit is a cumulant of two renormalized curvature-square composites.
- Apply the cumulant identity \kappa_2(:FF:,:FF:)=2GG+\kappa_4(F,F,F,F). This names the connected boundary-OPE polarization term R rather than hiding it in symbolic coefficients.
- Contract color using tr(T^aT^b)=\delta^{ab}/2. The Wick-square part has color factor 2(N^2-1) and geometric factor \Theta_{ij}^2/(\pi^4d_{ij}^8), hence is nonnegative and strictly positive when \Theta_{ij}\ne0.
- The remaining term is \mathcal C_{ij}^{ren}, the connected four-curvature polarization. At short collar distance asymptotic freedom predicts \mathcal C_{ij}^{ren}/\mathcal G_{ij}=O(g^2(1/d_{ij}))+O((\Lambda d_{ij})^4).
- Insert \mathcal R_{++}^{ren}=\mathcal G_{++}(1+\chi_{++}) into the corrected Schur-Feshbach scalar. Promotion requires \mathcal G_{++}(1+\chi_{++})>-Q_{+,0}^{SF} with positive margin.

Blocking gap: The missing valid proof is a uniform nonperturbative bound, or an explicit one-loop-plus-remainder extraction, for the flowed connected four-curvature polarization C_4^{ren} in the boundary hairpin geometry.

## Falsifiers

- Regulator-path falsifier: after standard Wilson counterterms, \mathcal R_{ij}^{ren} depends on the ratio \tau/\varepsilon^2 or on the boundary point-splitting direction.
- Geometry falsifier: the actual plus-channel hairpin bivectors give \Theta_{++}=0, eliminating the positive Wick-square term.
- Sign falsifier: the extracted connected polarization satisfies \chi_{++}\le -1+M_+/\mathcal G_{++}, so R cannot overcome Schur-Feshbach leakage.
- Same-theory falsifier: the flowed curvature-square composite needed for C_4^{ren} is not obtained as a limit of the Wilson observable algebra used in OS reconstruction.
- Cancellation falsifier: disconnected-product subtraction and one-hairpin perimeter/cusp subtraction fail to remove all \varepsilon^{-8} divergent self-terms.

## Learning

The branch is not looping on Wilson/OS obstruction language. The useful invariant is the dimensionless ratio \chi=C_4^{ren}/\mathcal G: the pair contraction is explicitly positive with color factor 2(N^2-1), and every remaining demotion comes from a concrete connected four-curvature cumulant or from zero hairpin geometry.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute a_N for the plus hairpin by evaluating the flowed two-[F^2] connected one-loop diagrams \mathcal I_{3g\times3g}, \mathcal I_{4g}, and \mathcal I_{Z_{F^2}}, subtract the Wick pair term, and test whether the resulting \chi_{++} stays above the Schur-Feshbach promotion margin.

# Heat-kernel Wilson R extraction for the first collar/hairpin Schur audit

## Candidate Lemma

For the first reflected Wilson collar/hairpin block at one boundary vertex, after same-theory Wilson normalization the first-order PHP/P_vK_vP_v test gives no obstruction, and the valid second-order test is the Schur-corrected form with P_vL_vP_v supplied by a concrete heat-kernel regulated connected Wilson cumulant R_{ij,σ}. The Gaussian crossed contraction contributes a positive color-geometric matrix g_R^4(N^2-1)(G_σ∘G_σ)/(8N^2); the only undecided Yang-Mills input is the connected four-curvature remainder κ_σ and its size relative to the hairpin Schur subtraction.

## Definitions

- source object: gradient-flow/heat-kernel regulated SU(N) Wilson collar cumulants for small reflected plaquette sheets Σ_i sharing a boundary vertex v.
- target object: the Schur-Feshbach corrected finite collar/hairpin quadratic form on P_v=ker H_v in M_v(t)=H_v+tK_v+t^2L_v+o(t^2).
- controlled interface: identify the t^2 block P_vL_vP_v with the boundary-OPE polarization matrix R_{ij,σ} extracted from connected Wilson two-collar cumulants.
- same-theory condition: the heat-kernel time σ, renormalized coupling g_R, vacuum measure, parallel transports, reflection, and Wilson normalization are identical in R_{ij,σ}, H_v, and K_v.
- X_{i,σ} is the transported flowed curvature flux through collar sheet Σ_i, based at v.
- E_v=Q_vH_vQ_v is the positive hairpin block and B_v=Q_vK_vP_v is the off-diagonal collar-hairpin coupling.

## Assumptions

- The regulated YM measure is gauge invariant, reflection positive, and color invariant at fixed σ>0.
- The nonabelian Stokes expansion of each small collar Wilson loop is uniform through fourth total flux order.
- Perimeter, cusp, and vacuum one-point factors are removed by the same Wilson renormalization before forming connected cumulants.
- The first-order collar block satisfies P_vK_vP_v=0 on the tested null collar sector after this cancellation.
- The hairpin block obeys E_v>=e_h I with e_h>0, so the finite Schur complement is well-defined.
- The connected four-curvature term κ_{ij,σ} exists as a finite flowed cumulant and has a regulator-stable continuum limit along the chosen scaling window.

## Equations

- transported flowed curvature flux: `X_{i,\sigma}^{a}=\int_{\Sigma_i} n_i^{\mu\nu}(x)\,[\operatorname{Ad}_{U_\sigma(\gamma_{x\to v})}F_{\mu\nu,\sigma}(x)]^{a}\,dS_x`. Valid when: Valid when the gradient-flow radius is positive and the collar sheets are smooth at that scale.
- first-order collar test: `P_vK_vP_v=0\quad\text{on the reflected Wilson collar null sector}`. Valid when: Applies after Wilson one-point subtraction cancels the linearized collar self-energy contribution.
- quadratic Wilson collar OPE: `\widehat W_i=-\frac{g_R^2}{4N}:X_{i,\sigma}^{a}X_{i,\sigma}^{a}:_\sigma+O(|\Sigma_i|^3)`. Valid when: Applies after perimeter and cusp normalization for collars smaller than the heat-kernel variation scale.
- R as a connected Wilson cumulant: `R_{ij,\sigma}=\frac{g_R^4}{16N^2}\operatorname{Cum}_\sigma\big(:X_{i,\sigma}^{a}X_{i,\sigma}^{a}:,:X_{j,\sigma}^{b}X_{j,\sigma}^{b}:\big)`. Valid when: Requires the same-theory boundary OPE and connected cumulant normalization for both Wilson collars.
- color-diagonal geometric two-point kernel: `C_{ij,\sigma}^{ab}:=\langle X_{i,\sigma}^{a}X_{j,\sigma}^{b}\rangle_c=\delta^{ab}G_{ij,\sigma}`. Valid when: Valid when the regulated vacuum preserves global color symmetry and the transports use the same basepoint convention.
- R decomposition into crossed contraction plus four-curvature cumulant: `R_{ij,\sigma}=\frac{g_R^4(N^2-1)}{8N^2}G_{ij,\sigma}^{2}+\frac{g_R^4}{16N^2}\kappa_{ij,\sigma}+O(|\Sigma|^5)`. Valid when: Valid when fourth-order cumulants are separated into Wick-crossed two-point contractions and a truncated four-curvature part.
- one-hairpin corrected second-order form: `\mathfrak C_{v,\sigma}(c)=\sum_{i,j}\bar c_iR_{ij,\sigma}c_j-\frac{|\sum_i b_i c_i|^2}{e_h}\quad(c\in P_v)`. Valid when: Applies when the first concrete hairpin complement is one-dimensional with energy e_h and coupling vector b.
- matrix promotion inequality: `\lambda_{\min,P_v}\!\left(\frac{g_R^4(N^2-1)}{8N^2}(G_\sigma\circ G_\sigma)+\frac{g_R^4}{16N^2}\kappa_\sigma\right)>\|E_v^{-1/2}B_vP_v\|^2`. Valid when: Valid when the finite expansion error is o(t^2) uniformly on the collar null sector.

## Attempted Derivation

- Fix gradient-flow time σ and define each collar observable by a small reflected Wilson loop with all transports based at the common vertex v.
- Use the nonabelian Stokes expansion. The trace kills the linear curvature term, and vacuum/perimeter normalization cancels the one-point quadratic self-term, leaving the normal-ordered quadratic flux as the first term relevant to a two-collar fourth-order cumulant.
- Form Cum(\widehat W_i,\widehat W_j). At order |Σ_i|^2|Σ_j|^2 it is exactly g_R^4/(16N^2) times Cum(:X_i^2:,:X_j^2:).
- Decompose this quadratic-flux cumulant into two crossed two-point contractions plus the genuinely connected four-curvature cumulant κ_{ij,σ}.
- Color invariance gives C_{ij}^{ab}=δ^{ab}G_{ij}; hence 2∑_{a,b}C^{ab}C^{ab}=2(N^2-1)G_{ij}^2, producing the positive coefficient g_R^4(N^2-1)/(8N^2).
- Since G_σ is a flux Gram matrix, G_σ∘G_σ is positive semidefinite by the Schur product theorem; negativity can only come from κ_σ or from the finite Schur hairpin subtraction.
- Insert R_σ as P_vL_vP_v in M_v(t)=H_v+tK_v+t^2L_v+o(t^2). With P_vK_vP_v=0 and E_v=Q_vH_vQ_v>0, the finite Schur-Feshbach tangent-cone theorem gives the corrected form P_vR_σP_v-B_v^*E_v^{-1}B_v.

Blocking gap: The actual sign and lower bound of κ_{ij,σ}, the connected flowed four-curvature cumulant for the two plaquette sheets, has not been computed nonperturbatively.

## Falsifiers

- falsifier: κ_σ has a negative eigenvalue on P_v whose magnitude exceeds the positive crossed-contraction matrix and the Schur margin.
- falsifier: the heat-kernel contact terms at a shared boundary vertex add uncanceled negative color structures not represented by δ^{ab}G_{ij}.
- falsifier: the hairpin block E_v develops a small eigenvalue in the continuum scaling window, making B_v^*E_v^{-1}B_v dominate R_σ.
- falsifier: same-theory Wilson normalization fails to cancel cusp or perimeter factors uniformly, so the fourth-order R extraction is not a valid finite L-block.
- falsifier: G_σ∘G_σ is degenerate on the tested collar vector while B_vc≠0, forcing the corrected form negative unless κ_σ supplies compensation.

## Learning

The branch is not looping on the OS density ladder. The concrete YM input is the heat-kernel connected Wilson cumulant R_{ij,σ}. Its Gaussian crossed-curvature part is positive with an explicit SU(N) color factor, and same-theory vacuum/perimeter cancellation explains why disconnected pieces do not enter. The valid obstruction test is now a numerical/sign comparison: positive R_σ, including κ_σ, must dominate the Schur hairpin energy B_v^*E_v^{-1}B_v.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the flowed plaquette-sheet cumulant κ_{12,σ}=Cum_4(X_1^aX_1^a,X_2^bX_2^b) for two adjacent collar sheets using the same heat-kernel regulator, subtract the crossed Wick contractions explicitly, then evaluate the one-hairpin form c*R_σc-|b·c|^2/e_h on the first collar null vector.
