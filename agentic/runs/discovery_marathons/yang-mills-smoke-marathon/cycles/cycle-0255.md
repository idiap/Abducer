# cycle-0255

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Post-HK endpoint kappa4 incidence test

## Candidate Lemma

For the first locked three-hairpin block in heat-kernel plaquette-sheet regulation, the post-H,K null-channel boundary-OPE polarization reduces to a signed sum of six endpoint-box fourth connected Wilson flux cumulants. With disjoint pair endpoints the incidence weights are (2,2,-4,-4,-4,-4), so the leading negative compact-group kappa4 is safe unless the 12-endpoint strength dominates the 13 and 23 endpoint strengths beyond the positive Feshbach margin and tail allowance.

## Definitions

- source object: heat-kernel plaquette-sheet regulated SU(N) Yang-Mills Wilson collar block with the already computed H,K and Feshbach null vector z=(1,1,-2).
- target object: same-theory OS Schwinger block after collar collapse, with the post-H,K scalar endpoint contribution bounded before continuum removal.
- controlled interface: connected boundary-OPE polarization R extracted from singlet four-flux endpoint cumulants, after Wick-square positivity and straight f f contact cancellation.
- same-theory condition: the endpoint-box source derivatives are computed with the same heat-kernel Wilson action, locked Wilson algebra, and no added reflection-plane counterterm or renormalized boundary observable.
- endpoint source: B_{ij,v} is the oriented plaquette-sheet flux source at endpoint box v for the reflected Wilson pair i,j, including path-ordering signs, plaquette normals, and the singlet color projection.
- endpoint strength: gamma_v=-kappa_v is nonnegative for the leading compact-group root-quartic term; deviations are assigned to the certified tail interval.

## Assumptions

- The three pairwise boundary footprints in the concrete H matrix are represented by disjoint endpoint intervals E12,E13,E23 with two endpoint boxes each and no triple endpoint box.
- The regulator is the heat-kernel plaquette-sheet regulator at spacing a with endpoint box heat time t_v and collar scale larger than each endpoint box.
- The connected log source derivative isolates the irreducible four-flux cumulant; disconnected Wick-square contractions are treated as positive Gram contributions outside the dangerous scalar.
- The straight-segment nonabelian f f contact cancels in the z=(1,1,-2) null incidence channel, leaving only endpoint/corner cumulants plus a tail.
- Uniform eighth-source derivative and corner-tail bounds are available on the same locked Wilson source family.

## Equations

- endpoint connected source cumulant: `Z_v(s)=\left\langle \exp\{sX_v(B_v)\}\right\rangle_{HK,v},\quad \kappa_v(B_v)=\partial_s^4\log Z_v(s)|_{s=0}`. Valid when: Applies when the heat-kernel endpoint box is smaller than the collar scale and the source is supported on the locked plaquette sheet.
- pair endpoint contraction defining R_ij: `R^{end}_{ij}=C_{YM}\sum_{v\in E_{ij}}\kappa_v(B_{ij,v})+T^{corner}_{ij},\quad C_{YM}=\frac{g_a^4}{4}\left(\frac{T_F}{N}\right)^2`. Valid when: Valid when only endpoint boxes survive after straight-segment cancellations in the reflected plaquette-sheet contraction.
- null endpoint incidence table: `\omega_v=2\chi_{12}(v)-4\chi_{13}(v)-4\chi_{23}(v),\quad (\omega_{12^-},\omega_{12^+},\omega_{13^-},\omega_{13^+},\omega_{23^-},\omega_{23^+})=(2,2,-4,-4,-4,-4)`. Valid when: Valid when the three pair footprint endpoint intervals are disjoint and no triple endpoint box is present.
- scalar post-HK endpoint polarization: `R_{end}(z)=C_{YM}\sum_v\omega_v\kappa_v(B_v)+T_{tail}`. Valid when: Valid when the null vector contraction has already removed the rank-one vacuum direction and the positive H sector.
- small heat-kernel root-quartic sign: `\kappa_v(B_v)=-\frac{t_v^4}{120}\sum_{\alpha\in\Phi_+}(\alpha\cdot B_v)^4+O(t_v^5\|B_v\|^4+t_v^4\|B_v\|^6+a^\eta\|B_v\|^4)`. Valid when: Applies in the small heat-kernel box regime after diagonalizing the endpoint source inside one coordinate chart.
- seven point fourth derivative certificate: `D_h^{(4)}F_v=\frac{-F_v(-3h)+12F_v(-2h)-39F_v(-h)+56F_v(0)-39F_v(h)+12F_v(2h)-F_v(3h)}{6h^4},\quad |D_h^{(4)}F_v-F_v^{(4)}(0)|\le \frac{7h^4}{240}M_8`. Valid when: Valid when an eighth source derivative bound holds uniformly on the sampled interval.
- endpoint interval sign test: `I_{end}=M_G+C_{YM}(-2\Gamma_{12}+4\Gamma_{13}+4\Gamma_{23})+[T_-,T_+],\quad \Gamma_{ij}=\sum_{v\in E_{ij}}\gamma_v,\quad \gamma_v=-\kappa_v`. Valid when: Valid when the previous H,K Feshbach reduction has isolated this scalar endpoint remainder.

## Attempted Derivation

- Start from the already reduced finite Schur-Feshbach problem: only the scalar null channel z=(1,1,-2) remains after PHP is nonnegative and the corrected second-order form isolates a positive margin M_G plus the connected boundary-OPE polarization.
- Use heat-kernel plaquette sheets and write each endpoint contribution through F_v(s)=log Z_v(s), where the fourth derivative is the singlet connected four-flux cumulant for the same Wilson source.
- Separate R into three pieces: Wick-square contractions, straight nonabelian f f contacts, and irreducible endpoint/corner kappa4. The first is a positive Gram contribution; the second cancels on straight shared segments by the null incidence identity.
- For each surviving endpoint box v, the null scalar supplies the pair weight omega_v=2 chi12(v)-4 chi13(v)-4 chi23(v). In the disjoint-endpoint geometry this gives two +2 weights for E12 and four -4 weights for E13,E23.
- Insert the small-box heat-kernel expansion. The compact-group Jacobian gives a negative root-quartic fourth cumulant, so equal endpoint boxes make the weighted endpoint term positive rather than dangerous.
- The only demotion route is certified 12-endpoint dominance: the negative fourth cumulants at E12 must exceed the weighted E13,E23 strengths plus M_G and the tail interval.
- A seven-point finite difference of log Z_v gives a same-theory numerical or symbolic certificate for each kappa_v with an explicit eighth-derivative error bound.

Blocking gap: The actual locked Wilson endpoint source table B_{ij,v} and uniform tail bounds T_-,T_+ have not been computed from a concrete plaquette-sheet geometry; the incidence table is valid only under the disjoint-endpoint geometry assumption.

## Falsifiers

- A geometry falsifier: the first three-hairpin plaquette sheet contains triple endpoint boxes or nested endpoint boxes, changing the incidence vector away from (2,2,-4,-4,-4,-4).
- A sign falsifier: certified endpoint data give sup I_end<0, so the same-theory post-H,K OS quotient has a negative null-channel scalar.
- A regulator falsifier: the heat-kernel endpoint source derivative is not the same observable as the Wilson collar limit because a boundary counterterm or endpoint renormalization is inserted.
- A cancellation falsifier: the straight C_A f f contact leaves a nonzero null-incidence remainder on the lattice plaquette sheet.
- A tail falsifier: corner or overlap tails are negative and larger than the positive Feshbach margin plus safe endpoint contribution.

## Learning

Cycle 255 advances the R/kappa4 handoff: the dangerous endpoint term is not a free symbolic parameter. In the heat-kernel plaquette-sheet regulator it is a color-weighted sum of connected fourth Wilson flux cumulants with explicit null incidence. The leading compact-group kappa4 is negative, but the actual null weights make equal disjoint endpoint boxes promote positivity. A genuine falsifier now requires certified 12-endpoint dominance or a negative tail, both testable by same-theory source derivatives.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Build the explicit B_{ij,v} table for the six endpoint boxes of the first hairpin plaquette sheet, evaluate or bound the seven source values F_v(kh) for k=-3,...,3, and produce the certified interval I_end.

# Gauge-invariant hairpin R-kernel endpoint-box extraction

## Candidate Lemma

For fixed H,K data and nondegenerate plus-channel hairpin geometry, the post-H,K endpoint-box term is a same-theory flowed Wilson covariance with positive pair baseline and one finite connected four-curvature polarization Xi_{++}. A valid lower bound is obtained from the absolute flowed kernel before any symbolic threshold is invoked.

## Definitions

- source object: continuum SU(N) Yang-Mills Schwinger family with gauge-invariant flowed Wilson hairpin observables at flow time t>0.
- target object: the post-H,K endpoint-box scalar R_{++}/kappa_4 entering the finite Schur-Feshbach handoff inequality.
- controlled interface: R_{++}^{ren} is extracted as a same-theory connected Wilson covariance, not as a Gaussian surrogate kernel.
- same-theory condition: take a->0 at fixed t,rho, renormalize each hairpin, then remove rho and t only inside the OS Schwinger family used for reconstruction.
- Regulator: Yang-Mills gradient flow for curvature insertions plus boundary point-splitting rho inside each thin endpoint box.
- Hairpin field: X_i^a(t,rho)=int_{Sigma_i(rho)} Theta_i^{mu nu}(u) G_{mu nu}^a(t,z_i+u) du, parallel-transported to one endpoint before color contraction.
- Centered observable: O_i(t,rho)=:X_i^a(t,rho)X_i^a(t,rho):_{perimeter,cusp}, with disconnected expectation and one-hairpin perimeter/cusp counterterms removed.
- Plus channel: O_+=(O_1+O_2)/sqrt(2) after H,K have selected the endpoint-box collar mode.

## Assumptions

- The continuum Schwinger functions satisfy OS positivity, Euclidean invariance, gauge invariance, and local regularity for flowed gauge-invariant composites.
- Endpoint boxes are disjoint, with distance d much larger than rho and sqrt(t), and the plus hairpin bivector is not null under the free flowed curvature covariance.
- The H,K finite reduction and the Schur-Feshbach leakage scalar L_+ are already fixed in the same observable basis.
- The cumulant normalization kappa_4 is the same one used in the paper handoff; no rescaling is introduced after R_{++}^{ren} is computed.

## Equations

- flowed connected Wilson covariance: `R_{ij}^{ren}(t,\rho)=\kappa_2\big(O_i(t,\rho),O_j(t,\rho)\big)`. Valid when: Valid when the continuum limit is first taken at fixed positive flow time and point-splitting.
- pair-plus-connected decomposition: `R_{ij}^{ren}=P_{ij}+C_{4,ij}^{ren}+O(|\Sigma|^6),\qquad P_{ij}=2(N^2-1){\mathcal D}_{ij}^2`. Valid when: Valid when the two endpoint boxes are disjoint and the renormalized thin-hairpin expansion is truncated before cubic sheet area terms.
- flowed curvature pairing: `{\mathcal D}_{ij}=\int_{\Sigma_i\times\Sigma_j}\Theta_i^{\mu\nu}(u)\Theta_j^{\alpha\beta}(v)K^t_{\mu\nu,\alpha\beta}(z_i-z_j+u-v)\,du\,dv`. Valid when: Valid when |r_{ij}| is larger than both the flow radius and collar thickness.
- endpoint asymptotic pair term: `P_{ij}=2(N^2-1)\frac{(\Theta_i\Pi(r_{ij})\Theta_j)^2}{\pi^4|r_{ij}|^8}\big(1+O(\sqrt t/|r_{ij}|+\rho/|r_{ij}|)\big)`. Valid when: Applies after diagonal normalization of nonzero hairpin bivectors in the endpoint-box regime.
- connected polarization parameter: `C_{4,ij}^{ren}=g_R^2(\mu_t)N(N^2-1){\mathcal D}_{ij}^2\Xi_{ij}(t,\rho,\mu_t)+O(g_R^4{\mathcal D}_{ij}^2),\quad \mu_t=(8t)^{-1/2}`. Valid when: Valid when perturbation theory is used only to parameterize the flowed connected four-curvature kernel in a fixed regulator window.
- absolute-kernel lower bound: `R_{++}^{ren}\ge P_{++}\left(1-\frac{g_R^2(\mu_t)N}{2}I_{++}^{abs}(t,\rho)\right)+O(g_R^4P_{++})`. Valid when: Valid when the absolute kernel integral is finite after cumulant and cusp cancellations.
- handoff promotion inequality: `\frac{R_{++}^{ren}}{\kappa_4}-\frac{L_+}{\kappa_4}>0\quad\Leftarrow\quad P_{++}\left(1-\frac{g_R^2N}{2}I_{++}^{abs}\right)>L_+`. Valid when: Valid after the H,K Schur-Feshbach data and the same-theory kappa_4 normalization have been fixed.

## Attempted Derivation

- Started from the centered flowed hairpin observable O_i=:X_i^aX_i^a: rather than from an abstract R_{ij}.
- Expanded the connected covariance kappa_2(O_i,O_j). Wick pairing gives two cross contractions and color delta^{ab}delta^{ab}=N^2-1, hence P_{ij}=2(N^2-1)D_{ij}^2.
- Separated the remaining term as the connected four-curvature cumulant integrated over two point-split endpoint boxes.
- Projected the YM order-g_R^2 kernel onto the color singlet bilinears; the nonabelian color contraction gives N(N^2-1).
- Used the cumulant subtraction to remove the product of one-hairpin expectations and used the one-hairpin perimeter/cusp counterterm to remove local same-box singular pieces.
- Observed that longitudinal and ghost pieces become boundary divergences under the closed collar-sheet projection; this is the cancellation that should leave only a finite cross-box Xi_{++}.
- Converted sign uncertainty into the interval bound |Xi_{++}|<=I_{++}^{abs}, giving the concrete promotion test P_{++}(1-g_R^2NI_{++}^{abs}/2)>L_+.

Blocking gap: No certified numerical interval for I_{++}^{abs} or Xi_{++} has been computed for the actual H,K endpoint-box geometry, and the O(g_R^4) plus O(|Sigma|^6) remainders are not yet bounded nonperturbatively.

## Falsifiers

- falsifier: the plus-channel geometry has D_{++}=0, making the positive pair baseline vanish.
- falsifier: cusp/perimeter subtraction leaves a rho-dependent logarithm in Xi_{++}.
- falsifier: certified quadrature gives 1-(g_R^2N/2)I_{++}^{abs}<=0 in every admissible flow window.
- falsifier: the Schur-Feshbach leakage L_+ is at least as large as the proven lower bound on R_{++}^{ren}.
- falsifier: lattice-flowed Wilson covariance disagrees in sign with the continuum flowed cumulant after matching kappa_4.
- falsifier: the required observable is not present in the reconstructed OS algebra after regulator removal.

## Learning

The branch is not looping on the Wilson/OS obstruction ladder. The concrete contribution is an R_{++}/kappa_4 handoff formula: a positive pair baseline with color 2(N^2-1), a connected four-curvature polarization with color N(N^2-1), and a valid falsifiable inequality against the Schur-Feshbach leakage L_+.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Instantiate the H,K plus-channel endpoint bivector, write D_{++} as an explicit heat-kernel integral, and run interval quadrature for Xi_{4v}, Xi_{33}, Xi_{gh}, and Xi_{ct} separately to test the promotion inequality.

# Post-H,K endpoint-box R/kappa4 Wilson audit

## Candidate Lemma

After H,K are fixed in the same Wilson truncation, the endpoint-box polarization is a concrete heat-kernel connected cumulant: a positive Gaussian Hadamard square plus one compressed connected four-curvature cumulant, followed by the Schur hairpin subtraction.

## Definitions

- source object: heat-kernel regulated SU(N) Yang-Mills Wilson measure on a lattice approximant or constructive continuum approximant with endpoint plaquette sheets S_i.
- target object: the finite matrix P_K(R_sigma-S_HK,sigma)P_K controlling the post-H,K second-order tangent cone on the lower-order kernel K.
- controlled interface: connected endpoint Wilson-box cumulants are converted into transported curvature-flux covariance C_sigma and connected four-flux cumulant kappa4_sigma before Schur subtraction.
- same-theory condition: sigma, lattice spacing or counterterms, coupling normalization, Wilson perimeter renormalization, vacuum subtraction, reflection plane, H,K,R, and Schur block E are all held in the same regulated theory.
- Endpoint flux Phi_i is based at the collar endpoint by adjoint parallel transport, so color contractions are gauge invariant after summing indices.
- S_HK,sigma denotes B_sigma^* E_sigma^{-1} B_sigma, with E_sigma the positive complement hairpin block from the finite Schur-Feshbach theorem.

## Assumptions

- Generators satisfy tr(T^a T^b)=delta^{ab}/2 and Wilson loops are normalized by N^{-1}tr.
- The endpoint sheets are small relative to the collar scale and are heat-flowed at radius sigma before OPE expansion.
- H,K and the kernel projection P_K have already been extracted in the same finite truncation.
- The Schur complement block E_sigma is strictly positive on the finite complement; otherwise the finite tangent-cone theorem is not applicable.
- Disconnected vacuum and perimeter factors are removed by connected cumulants and the same Wilson renormalization used for H,K.

## Equations

- transported plaquette flux: `\Phi_i^a(\sigma,a)=\sum_{p\in S_i}a^2\omega_{ip}\,\operatorname{Ad}_{U(\gamma_{ip})}^{ab}\mathcal F_p^b(\sigma),\qquad \mathcal F_p^b(\sigma)=a^{-2}2\operatorname{Im}\operatorname{tr}(T^bU_p(\sigma))`. Valid when: Valid when heat-flowed plaquette curvature is transported to a common endpoint basepoint before taking gauge-invariant contractions.
- curvature covariance and four-cumulant: `C_{ij,\sigma}=\frac{1}{N^2-1}\sum_a\langle \Phi_i^a\Phi_j^a\rangle_c,\qquad \kappa^{(4)}_{ij,\sigma}=\sum_{a,b}\operatorname{Cum}_c(\Phi_i^a,\Phi_i^a,\Phi_j^b,\Phi_j^b)`. Valid when: Valid when the endpoint sheets are small compared with the heat-kernel radius and the boundary OPE remainder is retained.
- endpoint polarization decomposition: `R_{ij,\sigma}=\alpha_N g_R^4(C_{ij,\sigma})^2+\frac{g_R^4}{16N^2}\kappa^{(4)}_{ij,\sigma}+E^{\mathrm{OPE}}_{ij,\sigma},\qquad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid after same-theory vacuum and perimeter cancellations remove disconnected Wilson factors from the endpoint-box cumulant.
- post-HK corrected endpoint test: `\lambda_{\min}P_K(R_\sigma-S_{HK,\sigma})P_K\ge m_G-\frac{g_R^4}{16N^2}M^-_{4,\sigma}-e_{\mathrm{OPE},\sigma}-s_{HK,\sigma}`. Valid when: Requires the same H,K regulator and a positive Schur complement block on the finite hairpin complement.
- finite plaquette kappa bound: `M^-_{4,\sigma}\le \|P_K\kappa^{(4)}_\sigma P_K\|\le \max_i\sum_j |\kappa^{(4)}_{ij,\sigma}|,\qquad |\kappa^{(4)}_{ij,\sigma}|\le 64N^2L_i^2L_j^2`. Valid when: Applies only to the bounded plaquette proxy before removing the lattice cutoff or sharpening constants.

## Attempted Derivation

- Fix the heat-kernel regulator sigma and endpoint plaquette sheets S_i in the same finite Wilson collar/hairpin truncation used to extract H,K.
- Replace each endpoint Wilson box by its small-sheet expansion W_i-<W_i>=-(g_R^2/(4N)):Phi_i^a Phi_i^a:+O_OPE, using tr(T^aT^b)=delta^{ab}/2.
- Take the connected two-box cumulant. Vacuum and perimeter factors cancel because the cumulant and Wilson renormalization are the same as in the H,K extraction.
- Split Cov(:Phi_i^2:,:Phi_j^2:) into crossed two-curvature contractions plus the connected four-curvature cumulant. Color diagonality gives 2(N^2-1)C_ij^2 and hence alpha_N=(N^2-1)/(8N^2).
- Use the Schur product theorem to keep alpha_N g_R^4(C o C) positive semidefinite on the finite endpoint subspace.
- Compress to the lower-order kernel K and subtract the finite Schur hairpin energy S_HK=B^*E^{-1}B supplied by the tangent-cone theorem.
- Bound the negative kappa4 contribution at finite cutoff by the plaquette flux bound ||Phi_i||<=sqrt(2N)L_i and a row-sum spectral estimate.

Blocking gap: The first actual H,K kernel basis, the numerical or analytic sign of P_K kappa4 P_K, and a same-regulator OPE error bound are still missing for the first collar/hairpin geometry.

## Falsifiers

- falsifier: compute the first same-regulator endpoint matrices and find lambda_min P_K(R_sigma-S_HK,sigma)P_K<0 with an error bar smaller than the negative margin.
- falsifier: P_K(C_sigma o C_sigma)P_K has a null vector on which the Schur hairpin energy is strictly positive and kappa4 plus OPE cannot compensate.
- falsifier: H,K and R require incompatible Wilson normalization, perimeter subtraction, or heat-kernel regulator choices; then the comparison is not same-theory valid.
- falsifier: the connected four-curvature cumulant has a negative compressed eigenvalue larger than the Gaussian Hadamard square by the endpoint-box scale.
- falsifier: the OPE endpoint remainder is of the same size as R_sigma in the tested geometry, so the finite endpoint-box audit has no controlled sign.

## Learning

The branch is not looping on OS density or symbolic thresholds. The new contribution is a concrete post-H,K endpoint-box formula: R_sigma=alpha_N g_R^4(C_sigma o C_sigma)+g_R^4 kappa4_sigma/(16N^2)+E_OPE, followed by S_HK subtraction. The first valid promotion quantity is m_G-g_R^4 M4^-/(16N^2)-e_OPE-s_HK; its failure is a sharp falsifier for the Wilson collar/hairpin branch.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Instantiate the smallest endpoint-box collar/hairpin geometry: list S_i weights, compute the heat-kernel plaquette covariance C_ij, extract or bound P_K kappa4 P_K by a row-sum or strong-coupling cumulant estimate, insert the known H,K Schur block, and report the signed margin.
