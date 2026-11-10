# cycle-0257

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint kappa4 incidence certificate for the post-H,K Wilson block

## Candidate Lemma

For the first concrete reflected three-hairpin block after H,K are fixed, the remaining connected boundary-OPE polarization is a signed endpoint-box incidence sum. The compact-group fourth cumulant is negative per endpoint direction, but the null-channel weights make equal endpoint boxes valid and safe; a falsifier needs certified 12-endpoint dominance plus tail control.

## Definitions

- source object: heat-kernel plaquette-sheet endpoint-box partition functions Z_v(eta) with locked SU(N) Wilson hairpin incidence vectors xi_{i,v}.
- target object: the post-H,K Schur-Feshbach null scalar for the same continuum Wilson OS block.
- controlled interface: endpoint source derivatives of log Z_v are identified with the connected boundary-OPE polarization R before cutoff removal.
- same-theory condition: the regulator, Wilson loop renormalization, endpoint collars, and observable algebra are identical in N, B, H, K, and the target OS matrix.
- endpoint box v: a heat-kernel plaquette subcomplex around a hairpin endpoint after straight-segment Wick-square and f f contacts are removed.
- singlet projection: P_sing contracts the four flux insertions through the color singlet channel, with color prefactor C_N=(g^4/4)(T_F/N)^2.

## Assumptions

- Pure four-dimensional SU(N) Yang-Mills is kept in a gauge-invariant heat-kernel plaquette-sheet regulator; no mass gap is assumed.
- The first H,K calculation and the corrected finite Schur-Feshbach gate are already fixed; this lemma addresses only the post-H,K R/kappa4 endpoint term.
- Endpoint boxes are chosen before cutoff removal and then transported through the same locked Wilson observable algebra.
- The connected log cumulant removes Wick-square pieces; the null incidence identity cancels the straight C_A f f contact.
- Small endpoint boxes admit exponential-coordinate heat-kernel expansion with a negative compact-group quartic cumulant in the singlet channel and a certified remainder.

## Equations

- endpoint fourth cumulant: `\kappa_{4,v}(a,b,c,d)=\left.\partial_{s_1}\partial_{s_2}\partial_{s_3}\partial_{s_4}\log Z_v\!\left(\sum_{r=1}^4 s_r a_r\right)\right|_{s=0},\quad a_1=a,\ldots,a_4=d`. Valid when: Valid when endpoint boxes are smaller than the collar scale and the heat-kernel regulator is used consistently.
- post-HK endpoint polarization: `R_{\mathrm{end}}=C_N\sum_v\{2\kappa_v^{12}-4\kappa_v^{13}-4\kappa_v^{23}\}+E_{\mathrm{tail}},\quad \kappa_v^{ij}:=\kappa_{4,v}(\xi_{i,v},\xi_{i,v},\xi_{j,v},\xi_{j,v})`. Valid when: Valid after the H,K block has been fixed and only connected endpoint cumulants remain.
- compact-group quartic sign: `\kappa_v^{ij}=-\beta_v\,\|P_{\mathrm{sing}}(\xi_{i,v}\odot\xi_{j,v})\|^2+\epsilon_v^{ij},\quad \beta_v>0,\quad |\epsilon_v^{ij}|\le \varepsilon_v\|\xi_{i,v}\|^2\|\xi_{j,v}\|^2`. Valid when: Applies in the small heat-kernel endpoint box where exponential coordinates stay inside the injectivity radius.
- incidence dominance functional: `B_{ij}:=\sum_v\beta_v\|P_{\mathrm{sing}}(\xi_{i,v}\odot\xi_{j,v})\|^2,\quad D:=2B_{12}-4B_{13}-4B_{23},\quad S_{\mathrm{null}}\ge M_G-C_N\max(D,0)-C_NE_\epsilon-|E_{\mathrm{tail}}|`. Valid when: Requires endpoint cumulant errors and nonendpoint tails to be bounded in the same cutoff scheme.
- equal-box safety check: `B_{12}=B_{13}=B_{23}=B\quad\Longrightarrow\quad D=-6B,\qquad R_{\mathrm{end,lead}}=6C_NB\ge0`. Valid when: Valid when the three pair endpoint strengths are measured in identical boxes.

## Attempted Derivation

- Start with the heat-kernel plaquette-sheet Wilson collar block and keep the H,K data fixed from the previous finite Schur-Feshbach calculation.
- Write each endpoint contribution as a source derivative of log Z_v; this evaluates the connected Wilson four-flux cumulant in the same regulator.
- Use connectedness of log Z_v to remove Wick-square contractions; these are positive Gram terms and cannot create the post-H,K falsifier.
- Use the null incidence identity for the three-hairpin block to cancel the straight shared-segment C_A f f contact, leaving endpoint and corner boxes only.
- Expand the small endpoint heat-kernel integral in exponential coordinates. The Haar/compact-group quartic curvature gives a negative singlet fourth cumulant, encoded by beta_v>0.
- Contract the three pair channels with the Feshbach null weights w_12=2, w_13=-4, w_23=-4. This yields D=2B_12-4B_13-4B_23 and proves that equal endpoint boxes are safe because D is then negative.
- Convert the remaining decision to the interval inequality S_null >= M_G-C_N max(D,0)-C_N E_epsilon-|E_tail|. Promotion needs this lower bound positive; demotion needs a certified negative interval.

Blocking gap: The actual endpoint incidence table xi_{i,v} for the locked Wilson hairpins and the uniform eighth-derivative/tail bounds have not yet been evaluated from regulator data.

## Falsifiers

- falsifier: certified heat-kernel source intervals give C_N D larger than the positive Schur-Feshbach margin after all endpoint errors and tails are subtracted.
- falsifier: the same endpoint box has a positive singlet fourth cumulant in the relevant mixed Wilson direction, contradicting the compact-group negative-kappa4 assumption.
- falsifier: the straight C_A f f contact fails the null-incidence cancellation when the actual plaquette-sheet geometry is inserted.
- falsifier: the endpoint source evaluations require a boundary counterterm or a changed Wilson renormalization, violating the same-theory condition.
- falsifier: tail bounds are of the same size as the margin with uncontrolled sign, so the endpoint-only certificate is not valid.

## Learning

Cycle 257 computes the sign-relevant endpoint incidence form instead of repeating the previous threshold. The connected R term is a same-theory heat-kernel fourth cumulant with weights 2,-4,-4. Negative compact-group kappa4 is safe for equal endpoint boxes; only certified 12-endpoint dominance or a negative tail can demote the block. This gives a valid promotion/falsifier interval for the post-H,K handoff.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Build the endpoint incidence table xi_{i,v} for the actual three hairpin plaquette sheets, evaluate the seven-point log Z_v fourth-derivative stencil for p=12,13,23, and return the certified interval for D and E_tail.

# Endpoint-box R++ flowed Wilson polarization interval

## Candidate Lemma

The post-H,K plus endpoint-box coefficient is a same-theory flowed Wilson covariance whose pair part is explicit and whose connected four-curvature polarization is reduced to one finite interval Xi_{++}. A certified interval gives a valid promotion or falsifier against the Schur-Feshbach leakage L_+.

## Definitions

- source object: the OS-positive Euclidean SU(N) Yang-Mills Schwinger family with gradient-flowed curvature G_{mu nu}^a(t,x) and thin same-boundary Wilson hairpins H_1,H_2.
- target object: the finite H,K Schur-Feshbach endpoint-box coefficient R_{++}^{ren}(t,d) entering the corrected plus-channel second-order form after the leakage L_+.
- controlled interface: replace each centered renormalized hairpin by its boundary-OPE leading curvature-square sheet functional and keep the remainder bounded in the flowed norm.
- same-theory condition: t>0, boundary point-splitting ell>0, cusp/perimeter subtraction, and cutoff removal are performed inside the same Schwinger family before varying t or ell.
- X_i(t) is the centered, cusp-subtracted, gradient-flowed Wilson hairpin observable attached to sheet Sigma_i.
- X_+=(X_1+X_2)/sqrt(2) is the plus endpoint-box mode used by the finite H,K reduction.
- L_+=B_{+R}D^{-1}B_{R+} is the already isolated Schur-Feshbach leakage in the plus channel.
- G_{++}(t,d) is the dimensionless positive cross-pair geometry of the two flowed hairpin sheets.

## Assumptions

- Pure SU(N) Yang-Mills Schwinger functions satisfy the Clay-target OS axioms in the same continuum limit; this lemma only supplies one endpoint coefficient.
- Gradient flow at t>0 makes curvature composites finite, and the t-window is chosen before attempting t down to zero.
- Hairpin thickness is smaller than sqrt(t), while endpoint point-splitting ell removes local collar coincidences.
- The one-hairpin perimeter and cusp counterterms are fixed from the same Wilson-loop renormalization used in the reconstructed observable algebra.
- The H,K finite reduction and L_+ are already computed in the same normalization as R_{++}^{ren}.
- The plus geometry is nondegenerate: G_{++}(t,d)>0.

## Equations

- flowed Wilson covariance defining R++: `R_{++}^{\mathrm{ren}}(t,d)=\kappa_2(X_+(t),X_+(t))_{\mathrm{ren}},\quad X_i(t)=Z_H^{-1}(t,\ell)\bigl(W_t(H_i)-\langle W_t(H_i)\rangle\bigr)`. Valid when: Valid when the reflected Wilson hairpins are flowed, centered, cusp-subtracted, and separated before removing the ultraviolet cutoff.
- boundary-OPE leading sheet observable: `X_i(t)=c_H(t)\int_{\Sigma_i^2}T_i^{AB}(x,y):G_A^a(t,x)G_B^a(t,y):\,dx\,dy+\mathrm{Rem}_i(t,\ell)`. Valid when: Applies when hairpin thickness is below sqrt(t) and sheet endpoints are point-split away from the collar boundary.
- plus pair geometry: `\mathcal G_{++}(t,d)=\int_{\Sigma_+^2\times\Sigma_+^2}T_+^{AB}(x,y)T_+^{CD}(u,v)C_{AC}^t(x-u)C_{BD}^t(y-v)\,dx\,dy\,du\,dv`. Valid when: Valid when the plus sheet tensor has nonzero cross geometry and flowed two-point curvature kernels have a continuum limit.
- explicit positive pair baseline: `P_{++}(t,d)=2(N^2-1)c_H(t)^2\mathcal G_{++}(t,d)>0`. Valid when: Valid when disconnected products and one-hairpin perimeter/cusp terms have been subtracted in the same renormalization scheme.
- R++ one-loop polarization form: `R_{++}^{\mathrm{ren}}=P_{++}\left[1+\lambda_t\Xi_{++}(t/d^2,\ell/d)+\mathcal R_2\right],\quad \lambda_t=\frac{g_t^2N}{16\pi^2}`. Valid when: Valid in a perturbative flowed window or as an asymptotic definition for the lattice-flow interval estimator.
- sector decomposition of connected four-curvature polarization: `\Xi_{++}=\mathcal G_{++}^{-1}\left(I_{3g}^{++}+I_{4g}^{++}+I_{\mathrm{ct}}^{++}+I_{\mathrm{end}}^{++}\right)`. Valid when: Requires the same-theory boundary OPE, gradient-flow regulator, and endpoint counterterms used in the pair baseline.
- certified lower interval: `\Xi^-\le\Xi_{++}\le\Xi^+,\quad |\mathcal R_2|\le\rho\quad\Rightarrow\quad R_{++}^{\mathrm{ren}}\ge P_{++}(1+\lambda_t\Xi^- -\rho)`. Valid when: Valid when certified quadrature or lattice-flow estimates enclose Xi and the OPE remainder in one regulator window.
- promotion and falsifier test: `P_{++}(1+\lambda_t\Xi^- -\rho)>L_+\Rightarrow Q_+^{\mathrm{corr}}>0,\quad P_{++}(1+\lambda_t\Xi^+ +\rho)\le L_+\Rightarrow \mathrm{falsifier}`. Valid when: Valid when L_+ is the already computed same finite-dimensional Feshbach leakage for the H,K plus channel.

## Attempted Derivation

- Fix the regulator: gradient flow at time t, endpoint point-splitting ell, and flowed coupling g_t at mu=1/sqrt(8t).
- Define R_{++}^{ren} as the renormalized connected cumulant kappa_2(X_+,X_+) of two centered thin Wilson hairpins in the same Schwinger family.
- Use the boundary OPE/non-Abelian Stokes expansion to replace each hairpin by a normal-ordered flowed curvature-square sheet functional plus Rem_i(t,ell).
- The disconnected product <X_+>^2 and all one-hairpin perimeter/cusp pieces cancel by construction; only cross-sheet pair contractions and connected four-curvature cumulants remain.
- The cross pair contraction has two Wick pairings and color delta^{ab}delta^{ab}=N^2-1, giving P_{++}=2(N^2-1)c_H^2 G_{++}.
- The connected one-loop four-curvature term splits into two-cubic-vertex, one-quartic-vertex, counterterm, and endpoint-subtraction sectors; f^{abe}f^{cde} contracted with color-singlet hairpins gives N(N^2-1).
- Normalize the connected contribution by G_{++} to define Xi_{++}; positive flow time and endpoint subtraction make the sector integrals finite.
- Derive the interval criterion R_{++}^{ren}>=P_{++}(1+lambda_t Xi^- -rho), so the endpoint-box repair is promoted only if this lower bound exceeds L_+.

Blocking gap: No certified numerical or analytic interval for I_{3g}^{++}+I_{4g}^{++}+I_ct^{++}+I_end^{++} has yet been produced for the actual H,K endpoint geometry, and the O(g_t^4) remainder rho is not bounded.

## Falsifiers

- A certified Xi interval with P_{++}(1+lambda_t Xi^+ +rho)<=L_+ falsifies this endpoint-box repair for the chosen geometry.
- Failure of perimeter/cusp subtraction to commute with the continuum limit invalidates the same-theory Wilson cumulant.
- If G_{++}(t,d)=0 or is parametrically below the Feshbach leakage scale, the plus endpoint box cannot be repaired by R_{++}.
- If the boundary-OPE remainder rho is comparable to or larger than 1+lambda_t Xi, the reduction is not controlled.
- If no regulator window exists with ell<<sqrt(t)<<d and stable cutoff removal, the flowed estimate is not valid for the continuum target.
- A lattice-flow measurement of the same cumulant with a negative interval large enough to cross L_+ is an empirical-mathematical falsifier for this branch.

## Learning

Cycle 257 made the endpoint-box task sharper: R_{++} is a valid flowed Wilson cumulant with explicit pair color 2(N^2-1), connected polarization color N(N^2-1), named sectors I_{3g}, I_{4g}, I_ct, I_end, and a concrete falsifier inequality against L_+. The next non-looping contribution must enclose Xi_{++} numerically or analytically.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the first certified Xi_{++} enclosure: write the Feynman-gauge heat-kernel tensors for I_{4g} and I_{3g}, scale all endpoint variables by d, partition the compact endpoint box, bound Gaussian tails by |partial^m K_t| estimates, and return an interval for Xi_{++} plus rho.

# Post-HK Endpoint-Box Kappa4 Bound For Wilson Collar/Hairpin Audit

## Candidate Lemma

For a fixed finite endpoint-box Wilson subspace with H,K already extracted, the post-H,K endpoint quadratic form is positive if the Gaussian Hadamard-square floor dominates the compressed negative connected four-curvature cumulant, the OPE remainder, and the Schur hairpin energy.

## Definitions

- source object: heat-kernel/gradient-flow regulated four-dimensional SU(N) Yang-Mills Wilson Schwinger functions for the fixed collar/hairpin endpoint-box basis.
- target object: the finite endpoint-box quadratic form P_E(R_\sigma-S_{HK})P_E on the OS-reconstructed Wilson truncation after H,K are known.
- controlled interface: R_\sigma is extracted from the same connected boundary-OPE Wilson cumulant and S_{HK}=B^*E^{-1}B from the same finite Schur-Feshbach data.
- same-theory condition: C_\sigma, \kappa_{4,\sigma}, E_{OPE,\sigma}, H, K, and S_{HK} use one coupling, one regulator, one Wilson basis, one vacuum normalization, and one OS measure.
- transported curvature flux: \Phi_i^a(\sigma) is the heat-kernel smeared curvature integrated over endpoint sheet \Sigma_i and parallel transported to basepoint b_i.
- plaquette-sheet absolute integral: I_{ij}^{(4)}(\sigma) is the absolute integral of the transported connected four-curvature kernel over \Sigma_i^2\times\Sigma_j^2 including bivector and color-trace weights.

## Assumptions

- SU(N) generators are in the fundamental representation with tr(T^aT^b)=delta^{ab}/2.
- The regulator is positive flow time sigma, so transported curvature products define finite Wilson cumulants before removing the regulator.
- The reflected endpoint boxes are exactly those used in the finite H,K Wilson collar/hairpin extraction.
- QHQ is strictly positive on the eliminated hairpin block, making S_HK=B^*E^{-1}B well-defined.
- The boundary OPE through fourth curvature order has an endpoint-box operator-norm remainder e_sigma.
- The connected four-curvature kernel is integrable on the heat-kernel smeared plaquette sheets.

## Equations

- transported flux covariance: `\Phi_i^a(\sigma)=\int_{\Sigma_i} n_i^{\mu\nu}(x)\,\mathcal F_{\mu\nu,\sigma}^a(x;b_i)\,dA_x,\quad C_{ij}^{\sigma}=\frac{1}{N^2-1}\sum_a\langle \Phi_i^a(\sigma)\Phi_j^a(\sigma)\rangle_c`. Valid when: Valid when sigma>0 fixes a gauge-covariant heat-kernel regulator and the endpoint sheets are the same Wilson sheets used to build H and K.
- connected four-flux cumulant: `(\kappa_{4,\sigma})_{ij}=\sum_{a,b}\langle :\Phi_i^a\Phi_i^a:\,:\Phi_j^b\Phi_j^b:\rangle_c^{\mathrm{nonG}}`. Valid when: Valid when the reflected Wilson observables are expanded to fourth curvature order after identical vacuum and perimeter normalization in one OS measure.
- endpoint R decomposition: `R_{\sigma}=\alpha_N g_R^4(C_{\sigma}\circ C_{\sigma})+\frac{g_R^4}{16N^2}\kappa_{4,\sigma}+E_{\mathrm{OPE},\sigma},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Valid when disconnected two-point pairings are separated from the connected four-curvature cumulant in the reflected Wilson boundary OPE.
- negative kappa4 row-sum bound: `M_{4,\sigma}^-:=\lambda_{\max}((-P_E\kappa_{4,\sigma}P_E)_+)\le \max_i\sum_j |(P_E\kappa_{4,\sigma}P_E)_{ij}|\le A_{4,\sigma}\max_i\sum_j I_{ij}^{(4)}(\sigma)`. Valid when: Valid when the finite endpoint-box subspace is fixed and the heat-kernel four-point kernel is integrable over all plaquette sheets.
- Gaussian floor and error norms: `m_{G,\sigma}:=\alpha_N g_R^4\lambda_{\min}(P_E(C_{\sigma}\circ C_{\sigma})P_E),\quad s_{HK}:=\|P_ES_{HK}P_E\|,\quad e_{\sigma}:=\|P_EE_{\mathrm{OPE},\sigma}P_E\|`. Valid when: Valid when H and K have already been extracted in the identical finite Wilson truncation, so the Schur term is known.
- corrected endpoint lower bound: `\lambda_{\min}P_E(R_{\sigma}-S_{HK})P_E\ge m_{G,\sigma}-\frac{g_R^4}{16N^2}M_{4,\sigma}^- -e_{\sigma}-s_{HK}`. Valid when: Valid when the OPE remainder is operator-norm controlled on the endpoint-box subspace at the chosen regulator scale.
- promotion inequality: `m_{G,\sigma}>\frac{g_R^4}{16N^2}M_{4,\sigma}^-+e_{\sigma}+s_{HK}`. Valid when: Valid when the desired output is finite-dimensional positivity of the post-H,K Wilson endpoint box rather than a full Clay mass gap.

## Attempted Derivation

- Fix the heat-kernel/gradient-flow regulator sigma and the endpoint sheets from the already extracted finite H,K collar/hairpin basis; no new observable algebra is introduced.
- Expand each vacuum/perimeter-renormalized endpoint Wilson loop through the quadratic transported curvature flux term, W_i-<W_i>=-(g_R^2/(4N)):Phi_i^a Phi_i^a:+O_sigma(Phi^3).
- Evaluate the reflected connected two-Wilson cumulant at order g_R^4. The cancellation used is identical vacuum/perimeter centering, which removes disconnected self-pairings and leaves crossed two-point contractions plus the connected four-curvature cumulant.
- Use tr(T^aT^b)=delta^{ab}/2 and color-diagonal flux covariance to obtain the Gaussian coefficient alpha_N=(N^2-1)/(8N^2). This gives alpha_N g_R^4(C_sigma o C_sigma), a PSD Hadamard-square contribution.
- Compress the non-Gaussian residue to the finite endpoint-box subspace and define M4_sigma^- as the positive spectral size of -P_E kappa4_sigma P_E. Bound it by the block/Gershgorin row sum of the actual plaquette-sheet four-curvature kernel.
- Subtract the finite Schur-Feshbach hairpin term S_HK=B^*E^{-1}B and obtain the lower bound m_G,sigma-g_R^4 M4_sigma^-/(16N^2)-e_sigma-s_HK.

Blocking gap: The numerical H,K endpoint geometry and a same-regulator bound or computation of the connected four-curvature plaquette-sheet kernel are still missing.

## Falsifiers

- falsifier: a heat-kernel plaquette-sheet computation gives g_R^4 M4_sigma^-/(16N^2)+e_sigma+s_HK >= m_G,sigma for the first endpoint-box basis.
- falsifier: P_E(C_sigma o C_sigma)P_E has a near-kernel aligned with the Schur hairpin subtraction, making m_G,sigma too small.
- falsifier: the connected four-curvature kernel is not integrable uniformly as sigma is lowered in the same Wilson basis.
- falsifier: H,K were extracted with a different regulator, coupling, perimeter subtraction, or endpoint normalization than R_sigma.
- falsifier: the boundary OPE remainder has an operator norm comparable to the Gaussian floor on the finite endpoint-box subspace.

## Learning

The contribution-making invariant is now a computable negative spectral size M4_sigma^- of the actual heat-kernel connected four-curvature Wilson cumulant. The Gaussian R term is PSD with fixed color factor, so the branch is valid only if kappa4, OPE error, and Schur hairpin energy are quantitatively dominated.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Using the first H,K endpoint geometry, assemble C_sigma and the plaquette-sheet absolute integrals I_ij^(4)(sigma) under the heat-kernel regulator; compute m_G,sigma, the row-sum bound for M4_sigma^-, and the Schur-subtracted endpoint lower bound.
