# cycle-0256

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint kappa4 incidence sign test for the post-H,K Wilson block

## Candidate Lemma

Under heat-kernel plaquette-sheet regulation, the isolated endpoint-box contribution to the post-H,K R scalar is controlled by the negative root-quartic fourth cumulant of the compact group measure. With null pair weights (2,-4,-4), equal disjoint endpoint boxes are sign-safe; a falsifier needs certified 12-endpoint dominance plus tails large enough to overcome the positive Gaussian margin M_G.

## Definitions

- source object: heat-kernel regulated plaquette-sheet endpoint boxes for the locked three-hairpin Wilson collar block, with the same lattice gauge action and Wilson algebra used before OS reconstruction.
- target object: the post-H,K Feshbach null scalar M_G+R_end+T_tail controlling the endpoint part of the same-theory OS quotient.
- controlled interface: singlet connected four-flux source derivatives of log Z_v are inserted into the finite Schur-Feshbach endpoint scalar after Wick-square and straight f f cancellations.
- same-theory condition: endpoint sources are generated only by infinitesimal deformations of the original Wilson plaquette sheets, with no boundary counterterm, no algebra enlargement, and no post hoc normalization.
- Phi_v^A is the parallel-transported boundary flux through endpoint plaquettes in box v.
- xi_{mu,v} is the color-geometric incidence source for the pair mu in {12,13,23} at endpoint box v.
- M_G is the already computed positive Gaussian Schur-Feshbach margin after the H,K gate.

## Assumptions

- Gauge group is SU(N) or a fixed compact simple group with fundamental Wilson traces normalized by tr(T^A T^B)=T_F delta^{AB}.
- Endpoint boxes are disjoint at the regulator scale; triple-overlap and corner-sharing boxes are placed into T_tail.
- The heat-kernel time tau_v is small enough for one exponential chart and a uniform Minakshisundaram remainder.
- Connected logs remove Wick-square contractions, and the straight C_A f f contact cancels by the null incidence identity already established.
- The first H,K block and its Feshbach null vector are fixed before evaluating R_end.

## Equations

- endpoint connected Wilson source: `Z_v(s;\xi)=\left\langle \exp\{s\,\xi_A\Phi_v^A\}\right\rangle_{a,v}^{HK},\qquad \kappa_{4,v}^{\rm sing}(\xi)=\left.\partial_s^4\log Z_v(s;\xi)\right|_{s=0}`. Valid when: Valid when the endpoint plaquette box is isolated before the continuum and collar limits are taken.
- heat-kernel root-quartic cumulant: `\kappa_{4,v}^{\rm sing}(\xi)=-\frac{\tau_v^4}{120}\sum_{\alpha>0}(\alpha(\xi))^4+O(\tau_v^5\|\xi\|^4+\tau_v^6\|\xi\|^6+\mathcal E_v)`. Valid when: Applies in one injectivity-radius chart for small heat-kernel time with uniformly bounded endpoint sources.
- null-channel endpoint scalar: `R_{\rm end}^{(4)}=C_{\rm col}\sum_{\mu}w_\mu\sum_{v\in E_\mu}\kappa_{4,v}^{\rm sing}(\xi_{\mu,v})+T_{\rm mix}=-C_{\rm col}\Delta_{\rm end}+T_{\rm mix},\quad C_{\rm col}=\frac{g_a^4}{4}\left(\frac{T_F}{N}\right)^2`. Valid when: Requires the same-theory Wilson sheet incidence and the Feshbach null vector after H,K are fixed.
- incidence dominance parameter: `w_{12}=2,\quad w_{13}=w_{23}=-4,\quad \Delta_{\rm end}=\frac{1}{120}\sum_{\mu}w_\mu\sum_{v\in E_\mu}\tau_v^4\sum_{\alpha>0}(\alpha(\xi_{\mu,v}))^4`. Valid when: Valid when endpoint boxes are assigned to one pair type and mixed boxes are quarantined into tails.
- certified seven-point source derivative: `D_{h,7}^{(4)}f(0)=\frac{-f(-3h)+12f(-2h)-39f(-h)+56f(0)-39f(h)+12f(2h)-f(3h)}{6h^4},\quad |D_{h,7}^{(4)}f(0)-f^{(4)}(0)|\le \frac{7h^4}{240}M_8`. Valid when: Valid when log Z_v has eight bounded source derivatives on the whole stencil interval.
- promotion-or-falsifier interval: `\mathcal I_{\rm end}=\left[M_G-C_{\rm col}\Delta_{\rm end}^{+}+T_-,\;M_G-C_{\rm col}\Delta_{\rm end}^{-}+T_+\right],\quad \mathcal I_{\rm end}\subset(0,\infty)\Rightarrow {\rm promote},\quad \mathcal I_{\rm end}\subset(-\infty,0)\Rightarrow {\rm falsifier}`. Valid when: Valid when all endpoint remainders and corner tails are enclosed by rigorous same-theory intervals.

## Attempted Derivation

- Locked the regulator to heat-kernel plaquette sheets at spacing a and collar width epsilon, so endpoint sources are same-theory deformations of Wilson sheets.
- Wrote each isolated endpoint box as U_v=exp X_v and used the heat-kernel small-time density K_tau(exp X)dU = Gaussian_tau(X) J(X)(1+E_v)dX with J the square-root Haar Jacobian.
- Expanded log J(X) in roots: the quadratic term only renormalizes the Gaussian covariance, while the first connected fourth term is negative and equals -sum_{alpha>0}(alpha(X))^4/2880 in log density.
- Differentiating log Z_v four times gives kappa_{4,v}^{sing}(xi)=-(tau_v^4/120) sum_{alpha>0}(alpha(xi))^4 plus controlled heat-kernel and chart remainders.
- Inserted this cumulant into the already reduced null-channel endpoint scalar. Wick-square terms are absent because log Z_v is connected, and the straight C_A f f contact is absent by null incidence cancellation.
- The remaining leading sign is governed by Delta_end=2A12-4A13-4A23. Equal disjoint endpoint weights give Delta_end<0 and therefore increase the margin; only A12>2(A13+A23) can make the leading endpoint term dangerous.

Blocking gap: The actual endpoint incidence vectors xi_{mu,v} and the mixed/corner tail interval T_tail have not yet been evaluated for the concrete plaquette-sheet geometry.

## Falsifiers

- A certified seven-point source-derivative computation gives Delta_end positive enough that M_G-C_col Delta_end+T_+<0.
- The endpoint boxes cannot be assigned to same-theory Wilson sheet deformations without adding a boundary counterterm or changing Wilson normalization.
- Mixed triple-endpoint boxes produce a negative tail larger than the positive Gaussian margin after all straight f f cancellations.
- The heat-kernel chart remainder is not uniform as a->0, invalidating the claimed endpoint cumulant interval.
- A direct regulated Wilson cumulant disagrees in sign with the negative root-quartic prediction outside the stated small-time regime.

## Learning

Cycle 256 computes the first sign-relevant local Yang-Mills input for the post-H,K R term. The compact-group endpoint kappa4 is negative, but the Feshbach null weights make equal disjoint endpoint boxes safe. The branch is not looping: the remaining decision is a concrete endpoint incidence and tail interval, not another OS obstruction restatement.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Construct the actual endpoint incidence table for the three locked plaquette-sheet hairpins, compute Delta_end by seven-point same-theory source derivatives of log Z_v, and enclose T_tail from mixed/corner boxes.

# Post-H,K flowed Wilson endpoint-box R interval

## Candidate Lemma

Endpoint-box handoff lemma. For separated flowed Wilson hairpins, the post-H,K scalar R_{++}^{ren} is reduced to a certified pair baseline plus one connected four-curvature polarization interval. Promotion is valid only if the certified lower endpoint beats the Schur-Feshbach leakage L_+.

## Definitions

- source object: OS-positive SU(N) Euclidean Yang-Mills Schwinger family with gradient-flowed, centered, perimeter/cusp-renormalized Wilson hairpin observables.
- target object: the post-H,K endpoint-box coefficient R_{++}^{ren} entering the corrected Schur-Feshbach second-order scalar.
- controlled interface: same-theory connected Wilson covariance kappa_2 of two thin hairpins, normalized by the small-sheet limit before Hamiltonian reconstruction.
- same-theory condition: the gauge group, action, continuum limit, flow regulator, and Wilson observable algebra are unchanged throughout the extraction.
- regulator: Yang-Mills gradient flow time t>0, boundary point splitting rho, and smooth sheet diameter a in endpoint boxes.
- cumulant: R is extracted from kappa_2 of two centered renormalized hairpins; disconnected products are subtracted.
- cancellation: one-hairpin perimeter and cusp factors cancel by Z_h, while the disconnected Wilson product cancels by centering.

## Assumptions

- N>=2 and the same continuum Schwinger family supplies the flowed Wilson observables.
- Endpoint boxes B_i,B_j are disjoint, with separation d much larger than sheet diameter a and flow length sqrt(t).
- The H,K finite reduction has already supplied the leakage scalar L_+ and endpoint coupling kappa_4.
- The flowed small-box OPE has a controlled second remainder E_{++}^{(2)}, or a lattice-flow interval replaces the perturbative bound.
- Gauge-invariant counterterm matching removes flow-regulated local cusp/perimeter divergences without changing the theory.

## Equations

- flowed centered hairpin: `\widehat H_i(t,\rho,a)=Z_{h,i}^{-1}(t,\rho,a)\left(W_i[B_t;\rho,a]-\langle W_i[B_t;\rho,a]\rangle\right)`. Valid when: Valid when positive flow time and point splitting make the Wilson hairpin a finite gauge-invariant observable.
- endpoint-box R coefficient: `R_{ij}^{\mathrm{ren}}(t,\rho)=\lim_{a\downarrow0}a^{-8}\,\kappa_2(\widehat H_i(t,\rho,a),\widehat H_j(t,\rho,a))`. Valid when: Valid when the thin-sheet normalization has a continuum limit after cusp and perimeter renormalization.
- cross-curvature kernel: `\mathcal G_{ij}(t)=\int_{\Sigma_i}\int_{\Sigma_j}\Omega_i^{\mu\nu}(x)\Omega_j^{\rho\sigma}(y)\mathcal D_{\mu\nu,\rho\sigma}(x-y;t)\,dx\,dy`. Valid when: Valid in the separated endpoint-box regime where flowed curvature two-point functions are smooth kernels.
- positive pair baseline: `P_{++}=2(N^2-1)\mathcal G_{++}(t)^2=\frac{2(N^2-1)\Theta_+^2}{\pi^4d^8}\left(1+O(a/d+t/d^2)\right)`. Valid when: Valid when both endpoint boxes are separated by distance d much larger than sheet diameter and flow length.
- one-loop polarization split: `R_{++}^{\mathrm{ren}}=g_R^4\left[2(N^2-1)\mathcal G_{++}^2+g_R^2N(N^2-1)\mathcal G_{++}^2\Xi_{++}+E_{++}^{(2)}\right]`. Valid when: Valid as a small-box flowed OPE expansion after disconnected products and one-hairpin counterterms cancel.
- Xi kernel projection: `\Xi_{++}=\mathcal G_{++}^{-2}\sum_{\Gamma\in\{4A,3A3A,ct\}}c_\Gamma\int_{B_+^4}T_+\,K_\Gamma^{(t,\rho,\mu)}`. Valid when: Applies after diagonal normalization of the plus channel and after gauge-invariant counterterm matching.
- certified lower endpoint: `R_{++}^{\mathrm{ren}}\ge g_R^4(N^2-1)\mathcal G_{++}^2\left[2+g_R^2N\Xi_- -\varepsilon_2\right]`. Valid when: Valid when certified quadrature gives Xi_{++} at least Xi_- and the OPE remainder is bounded by epsilon_2.
- promotion inequality: `\kappa_4g_R^4(N^2-1)\mathcal G_{++}^2\left[2+g_R^2N\Xi_- -\varepsilon_2\right]>L_+`. Valid when: Requires the same-theory boundary OPE coefficient kappa_4 and Schur-Feshbach leakage L_+ already fixed.

## Attempted Derivation

- Fixed the regulator to gradient flow time t>0 plus boundary point splitting rho; the observable is a centered thin Wilson hairpin in each endpoint box.
- Expanded the renormalized hairpin by the flowed nonabelian Stokes/Duhamel formula. The leading centered term is the curvature-flux square, scaled by a^4; hence the covariance scales as a^8.
- Used centering to cancel the disconnected Wilson product and Z_h to cancel one-hairpin perimeter/cusp factors. The remaining same-theory cumulant is kappa_2 of two endpoint hairpins.
- Contracted two flowed curvatures across the boxes. The two Wick pairings give factor 2, and the adjoint color trace gives N^2-1, producing P_{++}=2(N^2-1)G_{++}^2.
- For separated boxes, the curvature two-point kernel gives G_{++}=Theta_+/(pi^2 d^4)(1+O(a/d+t/d^2)); zero Theta_+ is an immediate geometric falsifier.
- Decomposed the connected four-curvature cumulant into quartic-gluon contact, two cubic-gluon exchange, and counterterm diagrams. Projection onto the plus channel factors out N(N^2-1)G_{++}^2 and defines Xi_{++}.
- Derived the interval handoff: if Xi_{++}>=Xi_- and |E_{++}^{(2)}|<=epsilon_2(N^2-1)G_{++}^2, then the lower bound for R_{++}^{ren} is the scalar in the promotion inequality.
- Converted the Clay-adjacent claim into a falsifiable endpoint-box test: compare kappa_4 times the certified lower bound with L_+ from the finite Schur-Feshbach reduction.

Blocking gap: No certified numerical interval for Xi_{++} has been produced yet; the exact tensor kernels and counterterm convention must be frozen before the quadrature certificate is valid.

## Falsifiers

- Falsifier: the cusp/perimeter subtraction fails to produce a finite R_{++}^{ren} as a->0 at fixed t and rho.
- Falsifier: Theta_+=0 for the chosen endpoint geometry, killing the positive pair baseline before Xi is relevant.
- Falsifier: the certified interval has 2+g_R^2N Xi_- - epsilon_2<=0, so the connected polarization overwhelms the pair baseline.
- Falsifier: even the certified upper bound on kappa_4 R_{++}^{ren} is below L_+, so the endpoint box cannot repair the Schur-Feshbach leakage.
- Falsifier: the extracted Xi_{++} depends on the covariant-gauge parameter after adding the counterterm piece.
- Falsifier: no regulator window exists with a/d<<1, sqrt(t)/d<<1, and controlled interval width.

## Learning

The cycle made a contribution-making move: R_{++} is no longer a symbolic placeholder. It is a flowed Wilson cumulant with an explicit positive pair baseline, a named connected four-curvature polarization Xi_{++}, a cancellation mechanism, and a valid lower-bound inequality against L_+. The remaining work is certified quadrature or a lattice-flow interval; failure of the inequality is a real falsifier for this endpoint-box repair.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Freeze the symmetric plus endpoint geometry, set alpha=t/d^2=1/64 and eta=a/d<=1/8, derive the explicit T_+K_Gamma tensors, then produce certified intervals for Xi_{++} for SU(2) and SU(3) and compare them with the stored L_+.

# Post-H,K endpoint-box R/kappa4 extraction

## Candidate Lemma

Post-H,K endpoint positivity reduces to a computable heat-kernel Wilson cumulant bound: on the finite Schur tangent kernel, Pi0(R_sigma-S_HK,sigma)Pi0 is positive if the Gaussian crossed-curvature square dominates the negative connected four-curvature cumulant, the OPE remainder, and the hairpin Schur energy.

## Definitions

- source object: heat-kernel regulated SU(N) Wilson endpoint-box observables W_i^sigma in the same finite collar/hairpin basis, with vacuum/perimeter normalized connected products.
- target object: the compressed post-H,K endpoint matrix Pi0(R_sigma-S_HK,sigma)Pi0 on the finite Schur-Feshbach tangent kernel.
- controlled interface: extract R_sigma only from same Wilson loops used to define H and K, then subtract B^*E^{-1}B without changing observables.
- same-theory condition: cutoff a, heat-kernel radius sigma, renormalized coupling g_R(sigma), parallel transport convention, and boundary OPE counterterms are identical in H, K, R, and kappa_4.
- Pi0 is the orthogonal projection onto ker H0 in the endpoint finite basis after first-order PHP constraints.
- S_HK,sigma=B_sigma^*E_sigma^{-1}B_sigma with E_sigma=QH_sigma Q positive on the hairpin complement.

## Assumptions

- Gauge group SU(N), Tr(T^aT^b)=delta^{ab}/2, and endpoint boxes are smooth at scale sigma.
- The finite H,K collar/hairpin matrices are already known in the same regulator and normalization.
- QH_sigma Q has a spectral lower bound e0>0 on the eliminated hairpin subspace.
- Boundary OPE errors are compressed by ||Pi0 E_OPE,sigma Pi0||<=e_OPE,sigma.
- Color averaging makes the two-curvature covariance diagonal in adjoint color after gauge-invariant parallel transport.
- The heat-kernel regulator is removed only after finite positivity margins are uniform in the same theory.

## Equations

- transported-flux covariance: `(C_\sigma)_{ij}:=\frac{1}{N^2-1}\int_{B_i\times B_j} n_i^{\mu\nu}(x)n_j^{\rho\lambda}(y)\langle \mathcal F^a_{\mu\nu}(x)\mathcal F^a_{\rho\lambda}(y)\rangle_\sigma\,dx\,dy`. Valid when: Valid when the heat-kernel transported curvatures are evaluated in separated endpoint boxes with identical smearing and parallel transport.
- connected four-curvature polarization: `(\kappa_{4,\sigma})_{ij}:=\int_{B_i^2\times B_j^2}\delta^{ab}\delta^{cd}\langle \Phi_i^a\Phi_i^b\Phi_j^c\Phi_j^d\rangle_{c,\sigma}\,d\mu_{iijj}`. Valid when: Valid when Phi denotes the same endpoint curvature flux appearing in the Wilson expansion and cumulants are connected.
- endpoint-box R decomposition: `R_\sigma=\alpha_N g_R(\sigma)^4(C_\sigma\circ C_\sigma)+\frac{g_R(\sigma)^4}{16N^2}\kappa_{4,\sigma}+E_{\mathrm{OPE},\sigma},\quad \alpha_N=\frac{N^2-1}{8N^2}`. Valid when: Applies after vacuum and perimeter cancellation leaves only crossed quadratic curvature contractions and the connected four-curvature cumulant.
- Schur-corrected lower margin: `\lambda_{\min}\{\Pi_0(R_\sigma-S_{HK,\sigma})\Pi_0\}\ge m_G-\frac{g_R(\sigma)^4}{16N^2}M^-_{4,\sigma}-e_{\mathrm{OPE},\sigma}-s_{HK,\sigma}`. Valid when: Requires the finite H,K matrices to be known and QH_sigmaQ invertible on the eliminated hairpin space.
- first calculable kappa4 row bound: `M^-_{4,\sigma}\le \|\Pi_0\kappa_{4,\sigma}\Pi_0\|_{\mathrm{op}}\le \max_i\sum_j |(\Pi_0\kappa_{4,\sigma}\Pi_0)_{ij}|`. Valid when: Valid for the finite compressed endpoint matrix before the continuum limit and gives a direct plaquette-sheet falsifier.

## Attempted Derivation

- Expand each endpoint Wilson loop by the non-abelian Stokes/plaquette-sheet expansion in heat-kernel smeared transported curvature flux Phi_i^a.
- The linear term drops because Tr T^a=0; the quadratic endpoint term is -(g_R^2/(4N))delta^{ab}Phi_i^aPhi_i^b.
- In the connected product of two vacuum/perimeter normalized Wilson loops, disconnected vacuum factors and perimeter self-contractions cancel by cumulant normalization.
- The two crossed Gaussian pairings give 2(N^2-1) times the squared scalar flux covariance, hence alpha_N=(N^2-1)/(8N^2).
- The non-Gaussian residue is exactly the color-contracted connected four-curvature cumulant kappa_{4,sigma} with coefficient g_R^4/(16N^2).
- Compress R_sigma to the finite PHP tangent kernel and subtract the Schur-Feshbach hairpin term S_HK=B^*E^{-1}B.
- Apply the min-max principle and the finite row-sum operator bound to obtain the margin Delta_sigma.

Blocking gap: The continuum-sign input is still missing: one needs a rigorous bound or extraction of the negative spectrum of the connected four-curvature cumulant in the same heat-kernel regulator.

## Falsifiers

- falsifier: a stable negative eigenvalue of Pi0(R_sigma-S_HK,sigma)Pi0 after heat-kernel and plaquette extrapolation.
- The row sum max_i sum_j |(Pi0 kappa4 Pi0)_ij| exceeds 16N^2(m_G-e_OPE-s_HK)/g_R^4 with an aligned negative eigenvector.
- The connected plaquette-sheet cumulant changes sign or size under a/sigma refinement beyond the stated discretization error.
- The vacuum/perimeter cancellation fails because H,K and R were not normalized in the same theory.
- QH_sigmaQ develops a small eigenvalue, invalidating the finite Schur-Feshbach subtraction.

## Learning

The branch is not looping on Wilson/OS obstruction restatement. The concrete new invariant is the compressed negative size of the heat-kernel connected four-curvature cumulant, bounded first by a plaquette-sheet row sum. The Gaussian R piece is color-computed and PSD; the Clay-relevant same-theory commitment is preserved by using the identical Wilson basis, regulator, coupling, and Schur subtraction.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Implement the finite endpoint plaquette-sheet table: compute C_sigma, kappa4_sigma row sums, s_HK, and Delta_sigma for the first actual H,K collar/hairpin geometry using the same heat-kernel regulator.
