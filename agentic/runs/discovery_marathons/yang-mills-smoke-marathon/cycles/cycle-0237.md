# cycle-0237

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: Wilson R-polarization computation

## Candidate Lemma

For locked reflected Wilson hairpin collars, the heat-kernel plaquette-sheet boundary OPE decomposes the second boundary polarization as a nonnegative Wick-square Gram term plus two dangerous Yang-Mills terms: the irreducible connected four-flux cumulant and the nonabelian commutator contact. Thus the first actual computation of R is reduced to a regulated color/geometric cumulant with a sharp sign test in the null channel.

## Definitions

- source object: SU(N) Wilson hairpin collars C_i^delta represented by gauge-invariant plaquette sheets, heat-kernel smeared at radius r with a<<r<<delta before collar collapse.
- target object: the continuum connected boundary-OPE polarization matrix R_ij entering the normalized Wilson OS quotient after diagonal Wilson factors are removed.
- controlled interface: take a->0 at fixed r,delta, expand reflected plaquette-sheet cumulants through second boundary order, subtract diagonal congruences, then pass r down to 0 with uniform remainders.
- same-theory condition: only standard Wilson loop renormalizations and diagonal congruences are divided out; no boundary counterterm, altered Wilson algebra, or pair-dependent normalization is introduced.
- Boundary flux is B_{i,r}^a(s)=n_i^{mu nu}(s)F_{mu nu}^{a,r}(0,s), with F^r=K_r*F and tr(T^aT^b)=T_F delta^{ab}, T_F=1/2.
- rho_i(s,t) is the signed plaquette-pair density determined by the two boundary legs of hairpin i; kappa_i is the oriented local commutator/contact density from nonabelian area ordering.

## Assumptions

- The heat-kernel regulator is gauge-covariant, reflection symmetric, and is implemented either by smeared continuum curvature or by plaquette parallel transport followed by a->0.
- Boundary OPE remainders are uniform for a<<r<<delta and for the finite three-hairpin geometry under test.
- The diagonal Wilson self-energy, cusp, and length-linear terms have already been removed as same-theory diagonal congruences, so P kills them in the Schur-Feshbach quotient.
- The reflected two-flux boundary covariance G_{partial,r}^{ab}(s,t)=<B_r^a(s)B_r^b(t)> is positive as a reflection-positive covariance kernel.

## Equations

- heat-kernel boundary flux: `B_{i,r}^a(s)=\int K_r((0,s)-y)\,n_i^{\mu\nu}(s)F_{\mu\nu}^a(y)\,dy`. Valid when: Valid when the hairpin footprint is smooth at scale r and the lattice spacing is much smaller than r.
- quadratic color-singlet boundary insertion: `\mathcal E_i^{(r)}=\frac{g^2T_F}{N}\int \rho_i(s,t):B_{i,r}^a(s)B_{i,r}^a(t):\,ds\,dt,\qquad T_F=\frac12`. Valid when: Applies after diagonal normalization removes one-body Wilson factors and the plaquette sheet is expanded to second boundary order.
- R decomposition: `R_{ij}^{(r)}=R_{ij}^{\mathrm{Wick},(r)}+R_{ij}^{4c,(r)}+R_{ij}^{\mathrm{comm},(r)}+o_r(1)`. Valid when: Requires the same-theory boundary OPE with heat-kernel smearing and uniform remainders for reflected Wilson collars.
- Wick-square contraction: `R_{ij}^{\mathrm{Wick},(r)}=2\left(\frac{g^2T_F}{N}\right)^2\int \rho_i(s,t)\rho_j(u,v)G_{\partial,r}^{ab}(s,u)G_{\partial,r}^{ab}(t,v)\,ds\,dt\,du\,dv`. Valid when: Valid when the four-flux contraction is restricted to the Gaussian Wick pairing of two boundary two-point functions.
- Wick Gram positivity: `\sum_{i,j}v_iv_jR_{ij}^{\mathrm{Wick},(r)}=2\left(\frac{g^2T_F}{N}\right)^2\|\sum_i v_i\,\rho_i^{1/2}G_{\partial,r}\rho_i^{1/2}\|_{\mathrm{HS},c}^2\ge0`. Valid when: Valid when the plaquette kernels are positive footprint measures and the boundary two-flux covariance is positive.
- irreducible four-flux cumulant: `R_{ij}^{4c,(r)}=\left(\frac{g^2T_F}{N}\right)^2\int \rho_i(s,t)\rho_j(u,v)\langle B_r^a(s)B_r^a(t)B_r^b(u)B_r^b(v)\rangle_c\,ds\,dt\,du\,dv`. Valid when: Applies to the connected non-Gaussian Yang-Mills cumulant after all Wick pairings have been subtracted.
- commutator contact model: `R_{ij}^{\mathrm{comm},(r)}=-\frac{g^4T_FC_A}{2N}\int \kappa_i(s)\kappa_j(t)G_{\partial,r}(s,t)^2\,ds\,dt+\operatorname{f.p.}_{r\downarrow0}`. Valid when: Applies when nonabelian Stokes or Magnus ordering reduces coincident plaquettes to the f^{abe}f^{abe}=C_A(N^2-1) contact.
- dangerous null-channel sign test: `\mathcal R_v^{\mathrm{dang},(r)}=v^*(R^{4c,(r)}+R^{\mathrm{comm},(r)})v,\quad v=(1,1,-2),\quad \liminf_{r\downarrow0}\mathcal R_v^{\mathrm{dang},(r)}>-8m^2\Rightarrow \text{no second-order falsifier}`. Valid when: Valid after the Schur-Feshbach reduction and after the nonnegative Wick-square polarization has been separated.

## Attempted Derivation

- Chose a reflection-symmetric heat-kernel regulator K_r and represented each Wilson hairpin collar by a gauge-invariant plaquette sheet with a<<r<<delta.
- Expanded the normalized reflected Wilson product by nonabelian Stokes/Magnus through second boundary order, keeping explicit color factors T_F=1/2 and C_A=N.
- Used the same-theory cancellation: diagonal Wilson self-energies, cusp factors, and length-linear terms are congruences killed by the zero-sum Schur-Feshbach projection.
- Separated the four-flux contribution into Wick pairings and an irreducible connected cumulant. The Wick pairings form a covariance of quadratic color-singlet flux insertions and are therefore nonnegative in the null channel.
- Identified the only remaining negative sources as the connected four-flux cumulant C_4 and the f f commutator contact supported on coincident boundary footprints.
- Derived the first calculable sign test: compute or bound v^*(R^{4c}+R^{comm})v for the actual plaquette footprints; the positive Wick-square term may be ignored in a lower-bound promotion test.

Blocking gap: No rigorous sign or sharp size estimate is yet available for the heat-kernel finite part of the connected four-flux cumulant plus commutator contact in four-dimensional Yang-Mills.

## Falsifiers

- A numerical or strong-coupling plaquette cumulant giving liminf v^*(R^{4c}+R^{comm})v<-8m^2 would be a genuine second-order Wilson falsifier.
- A regulator-dependent finite part in R_comm after standard Wilson renormalization would violate the same-theory condition.
- A nonintegrable heat-kernel growth of C_4^{(r)} in the collar limit would invalidate the claimed boundary OPE expansion.
- A hidden pair-dependent boundary counterterm that restores positivity would prove positivity only for a modified theory, not for the locked Wilson algebra.

## Learning

The branch made a real contribution beyond the previous threshold: R is not a black-box symbolic entry. With heat-kernel plaquette sheets, its Wick-square part is a positive Gram term and cannot be the second-order falsifier. The dangerous Yang-Mills content is exactly the irreducible connected four-flux boundary cumulant plus the nonabelian f f commutator contact, with explicit T_F, C_A, and footprint geometry. The next proof pressure is a sign/size estimate for these two terms in the actual hairpin footprints.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Evaluate C_4^{(r)} and I_comm^{(r)} for the three actual hairpin footprints on a hypercubic plaquette regulator: list the coincident plaquette pairs, compute the color contractions f^{abe}f^{abe}=C_A(N^2-1), and bound the connected four-plaquette cumulant by a reflection-positive cluster estimate.

# Gauge-Invariant Nontriviality Witness Selection: flowed hairpin R-kernel extraction

## Candidate Lemma

For two boundary-separated thin Wilson hairpins, the finite H,K polarization entry R_ij is the area-normalized connected cumulant of centered flowed hairpins. Its first calculable Yang-Mills contribution is a nonnegative two-curvature contraction with color factor 2(N^2-1) and a boundary geometry factor; the only possible sign loss is the genuine connected four-curvature remainder.

## Definitions

- source object: continuum SU(N) Yang-Mills Schwinger functional represented by gradient-flowed gauge-invariant Wilson observables at flow time t>0.
- target object: the finite H,K collar/hairpin second-order matrix entry R_ij used in the Schur-Feshbach plus-channel test.
- controlled interface: flowed, boundary point-split, perimeter/cusp-renormalized thin hairpin Wilson loops whose connected cumulant is divided by A_i(ρ)^2 A_j(ρ)^2.
- same-theory condition: the regulator, Wilson loops, counterterms, and cumulant limits are all taken inside the same Yang-Mills measure used for OS reconstruction; no auxiliary Gaussian replacement is allowed.
- Hairpin H_i has anchor x_i on the reflection boundary, boundary tangent τ_i, normal n, collar area A_i(ρ), and separation d_ij=|x_i-x_j|>0.
- The boundary-OPE polarization term is the renormalized connected coefficient left after subtracting the disconnected product and one-hairpin perimeter/cusp factors.

## Assumptions

- G=SU(N), Tr(T^aT^b)=δ^{ab}/2, and flowed Wilson loop Schwinger functions have a continuum limit.
- The collars are separated: sqrt(8t), ε, ρ are all small compared with d_ij before the boundary OPE coefficient is read.
- The nonabelian Stokes/Magnus expansion for the small flowed loop has a uniform remainder after perimeter and cusp renormalization.
- Point splitting plus the adjoint connector defines the local composite F_{nτ}^aF_{nτ}^a without changing the theory.
- The finite Schur-Feshbach leakage Λ_F=⟨B_RK u,D^{-1}B_RK u⟩ is already fixed from the H,K reduction.

## Equations

- centered flowed hairpin: `\widehat W_i=W_i^{\rm flow,ren}-\langle W_i^{\rm flow,ren}\rangle,\quad W_i^{\rm flow,ren}=Z_{{\rm per},i}^{-1}Z_{{\rm cusp},i}^{-1}N^{-1}{\rm Tr}\,P e^{i\oint_{\gamma_i(\varepsilon,\rho)} A_t}`. Valid when: Valid when flowed Wilson loops are evaluated at positive flow time before removing point splitting and collar width.
- R coefficient as connected Wilson cumulant: `R_{ij}^{\rm ren}=\lim_{\rho\downarrow0}\lim_{t,\varepsilon\downarrow0}{\kappa_2(\widehat W_i(t,\varepsilon,\rho),\widehat W_j(t,\varepsilon,\rho))\over c_H(t)^2 A_i(\rho)^2 A_j(\rho)^2}`. Valid when: Valid when boundary separations stay fixed while flow radius and point splitting are taken below the collar width.
- thin-hairpin OPE: `\widehat W_i(t,\varepsilon,\rho)=-c_H(t)A_i(\rho)^2\mathcal E_i^{t,\varepsilon}(x_i)+O(A_i(\rho)^2\rho)+O(A_i(\rho)^3)`. Valid when: Applies for thin collars whose diameter is below the separation scale but above the flow smoothing length.
- gauge-invariant point-split curvature square: `\mathcal E_i^{t,\varepsilon}(x)=:\!F_{n\tau_i}^a(t,x+\varepsilon\tau_i/2)U_{\varepsilon}^{ab}(x)F_{n\tau_i}^b(t,x-\varepsilon\tau_i/2)\!:`. Valid when: Valid when the adjoint connector lies inside the same hairpin collar and removes gauge-frame dependence.
- connected curvature-composite decomposition: `\langle\mathcal E_i(x)\mathcal E_j(y)\rangle_c=2\sum_{a,b}\kappa_2(F_i^a(x),F_j^b(y))^2+\sum_{a,b}\kappa_4(F_i^a,F_i^a,F_j^b,F_j^b)_{x,y}^{\rm ren}`. Valid when: Requires the point-split curvature composites to be centered before the coincident-point limit is taken.
- first calculable boundary contraction: `R_{ij}^{\rm pair}(t)=2(N^2-1)\left({\tau_i\!\cdot\!\tau_j-2(\tau_i\!\cdot\!\hat r_{ij})(\tau_j\!\cdot\!\hat r_{ij})\over \pi^2 d_{ij}^4}\right)^2+O(t/d_{ij}^{10})+O(g^2(d_{ij}^{-1})d_{ij}^{-8})`. Valid when: Applies after diagonal normalization in the separated boundary regime d_ij much larger than sqrt(8t) and rho.
- promotion inequality for the plus channel: `R_{++}^{\rm ren}\ge \sum_{i,j}u_i u_j R_{ij}^{\rm pair}-\|C_4^{\rm ren}\|_{++},\quad u=(1,1),\quad R_{++}^{\rm ren}>\Lambda_F-Q_+^{\rm loc}`. Valid when: Valid when the plus-channel vector is the finite H,K collar vector and the four-curvature remainder has a proven operator-norm bound.

## Attempted Derivation

- Use Yang-Mills gradient flow as the ultraviolet regulator and boundary point splitting ε inside each hairpin; define centered renormalized Wilson hairpins after perimeter and cusp subtraction.
- Apply the small-loop nonabelian Stokes expansion. The trace kills the linear curvature term, so the leading centered term is -c_H A_i^2 times the point-split curvature square E_i=F_{nτ_i}^aF_{nτ_i}^a.
- Take κ_2 of two centered hairpins. The disconnected product cancels by centering, and one-hairpin perimeter/cusp divergences cancel through Z_per and Z_cusp, leaving the boundary-OPE polarization coefficient R_ij.
- Decompose κ_2(E_i,E_j) by cumulants. The two-curvature part contributes 2(N^2-1) times the square of the boundary curvature propagator; the residual term is the genuine connected four-curvature cumulant C_4^{ren}.
- For boundary separation r_ij and electric component F_{nτ}, the flowed free contraction has geometry Θ_ij=τ_i·τ_j-2(τ_i·rhat_ij)(τ_j·rhat_ij), hence R_ij^{pair}=2(N^2-1)Θ_ij^2/(π^4 d_ij^8) up to flow and interaction corrections.
- Insert u=(1,1) to get the plus-channel estimate R_{++}^{ren}≥u^T R^{pair}u-||C_4^{ren}||_{++}, then compare it with the Schur-Feshbach leakage threshold Λ_F-Q_+^{loc}.

Blocking gap: The missing hard estimate is a uniform, regulator-independent bound on the connected four-curvature remainder C_4^{ren} in the simultaneous flow, point-splitting, and thin-collar limits.

## Falsifiers

- falsifier: after the stated cancellations, κ_2(Ŵ_i,Ŵ_j)=o(A_i^2A_j^2), so the extracted R_ij is zero.
- falsifier: the value of R_{++}^{ren} changes when the order of t↓0, ε↓0, and ρ↓0 is varied within the allowed separated regime.
- falsifier: a valid upper bound gives R_{++}^{ren}<Λ_F-Q_+^{loc}, so the polarization cannot overcome Schur-Feshbach leakage.
- The connected four-curvature cumulant is negative with norm larger than the explicit pair term in the plus channel.
- The perimeter/cusp subtraction leaves a boundary contact term rather than a finite separated R-kernel coefficient.
- The hairpin observable fails to belong to the same reconstructed gauge-invariant OS algebra.

## Learning

The branch moved from symbolic thresholds to an actual Yang-Mills R-kernel. The regulator is gradient flow plus boundary point splitting; the cumulant is κ_2 of two centered renormalized thin hairpins; the cancellation is disconnected product plus one-hairpin perimeter/cusp subtraction. The explicit pair term is positive with color factor 2(N^2-1) and geometry Θ^2/(π^4d^8). The valid obstruction is now isolated: bound the connected four-curvature polarization C_4^{ren}.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the simplest actual case: two parallel boundary hairpins separated by d with τ⊥rhat, where R_pair=2(N^2-1)/(π^4d^8). Evaluate or bound C_4^{ren} using the flowed plaquette-sheet cumulant after disconnected and cusp cancellations.

# Heat-kernel Wilson collar R_ij extraction for Schur-corrected audit

## Candidate Lemma

For same-theory SU(N) Wilson collars regulated by gradient-flow heat-kernel smearing, the boundary-OPE polarization coefficient R_ij is the covariance of two vacuum-subtracted quadratic transported curvature fluxes. It decomposes into a positive Wick cross-contraction with explicit color factor plus the genuine connected four-curvature cumulant. The finite positivity test is valid only after subtracting the Schur-Feshbach hairpin term.

## Definitions

- source object: OS-positive SU(N) Yang-Mills Wilson loop Schwinger functions with heat-kernel/gradient-flow regulator rho and common renormalized coupling g_R(rho).
- target object: the finite collar/hairpin Gram tangent coefficient B=P R P-PKQ(QHQ)^{-1}QKP on the degenerate Wilson subspace.
- controlled interface: gauge-invariant Wilson collars are expanded into transported smeared curvature fluxes before OS reconstruction, then inserted into the finite Schur-Feshbach cone.
- same-theory condition: all collars, hairpins, counterterms, and smearing scale rho are taken in one regulated Yang-Mills measure, so normalization changes are common factors not new dynamics.
- A collar sheet Sigma_i has oriented area bivector d sigma_i^{mu nu} and a fixed adjoint connector tree to basepoint b_i.
- Phi_i^a(rho) is the adjoint-transported flowed curvature flux through Sigma_i.
- R_ij^rho is the coefficient of Cov(X_i,X_j) for X_i=1-N^{-1} Re Tr U_rho(C_i) after vacuum and perimeter subtraction.

## Assumptions

- The flowed curvature F_{mu nu,rho} is gauge covariant and has finite correlation functions at rho>0.
- The collar areas satisfy A_i rho^{-2} << 1, so the leading non-Abelian Stokes term dominates the Wilson OPE.
- The finite hairpin complement obeys QHQ >= h0 Q with h0>0.
- The same connector prescription is used in all entries before taking gauge-invariant traces.
- The four-curvature connected cumulant has a regulator-uniform bound strong enough to dominate the Wilson OPE remainder.

## Equations

- transported flowed curvature flux: `\Phi_i^a(\rho)=\int_{\Sigma_i} d\sigma_i^{\mu\nu}(x)\,\operatorname{Ad}_{U_\rho(b_i,x)}^{ab}F_{\mu\nu,\rho}^b(x)`. Valid when: Valid when the collar sheet is thinner than curvature radius and a fixed gauge-covariant connector tree is used.
- small-collar Wilson OPE: `X_i^\rho:=1-\frac1N\operatorname{ReTr}U_\rho(C_i)=\alpha_N g_R(\rho)^2\Phi_i^a\Phi_i^a+O((A_i\rho^{-2})^3),\qquad \alpha_N=\frac1{4N}`. Valid when: Valid when flowed loops are small enough for the non-Abelian Stokes expansion and the same renormalized coupling normalizes every collar.
- R coefficient as connected Wilson cumulant: `R_{ij}^\rho=(\alpha_N g_R^2)^2\,\Big\langle\big(\Phi_i^a\Phi_i^a-\langle\Phi_i^a\Phi_i^a\rangle\big)\big(\Phi_j^b\Phi_j^b-\langle\Phi_j^b\Phi_j^b\rangle\big)\Big\rangle`. Valid when: Requires the same-theory boundary OPE counterterms and vacuum subtraction, so perimeter and isolated self-contractions cancel before comparing collars.
- Wick plus connected four-curvature split: `R_{ij}^\rho=2\alpha_N^2g_R^4\sum_{a,b}(C_{ij}^{ab,\rho})^2+\alpha_N^2g_R^4\sum_{a,b}\langle\Phi_i^a\Phi_i^a\Phi_j^b\Phi_j^b\rangle_c+O((A\rho^{-2})^5)`. Valid when: Applies when the quadratic flux truncation controls the Wilson remainder uniformly over the finite collar family.
- color-diagonal Gaussian factor: `C_{ij}^{ab,\rho}=\delta^{ab}c_{ij}^\rho\quad\Longrightarrow\quad R_{ij,G}^\rho=\frac{g_R^4(N^2-1)}{8N^2}(c_{ij}^\rho)^2\ge 0`. Valid when: Applies after diagonal color normalization of the transported two-point function in an unbroken SU(N) invariant vacuum.
- Schur-corrected finite positivity condition: `B^\rho=P R^\rho P-PK^\rho Q(QH^\rho Q)^{-1}QK^\rho P,\qquad v^TB^\rho v\ge0\ \text{for all }v\in P\mathbb C^m`. Valid when: Valid when QHQ is strictly positive on the finite hairpin complement and R is evaluated in the same regulator.

## Attempted Derivation

- Use the gradient-flow heat-kernel regulator: F_rho is the curvature at flow time rho^2 and U_rho(b,x) transports it to the collar basepoint. This makes Phi_i adjoint-covariant and Phi_i^a Phi_i^a gauge invariant.
- Expand the flowed Wilson collar by the non-Abelian Stokes formula. The trace kills the linear term, tr(T^a)=0, and the first nontrivial term is alpha_N g_R^2 Phi_i^2 with alpha_N=1/(4N).
- Normalize X_i by subtracting its vacuum expectation and using the same perimeter/flow counterterm for every loop. This is the cancellation: self-contractions C_ii C_jj and perimeter divergences cancel before R_ij is read off.
- Apply the moment-cumulant identity to <Phi_i^2 Phi_j^2>-<Phi_i^2><Phi_j^2>. The two crossed Wick contractions give 2 sum_{a,b}(C_ij^{ab})^2; the residual term is the connected four-curvature cumulant sum_{a,b}<Phi_i^a Phi_i^a Phi_j^b Phi_j^b>_c.
- For a kernel vector v, define G_v=2 sum_{i,j}v_i v_j sum_{a,b}(C_ij^{ab})^2, Kappa_v=sum_{i,j}v_i v_j sum_{a,b}<Phi_i^a Phi_i^a Phi_j^b Phi_j^b>_c, and S_v=||(QH Q)^{-1/2}QK Pv||^2.
- The promotion inequality is alpha_N^2 g_R^4(G_v+Kappa_v) >= S_v for every v in the PHP-kernel. The demotion inequality is the reverse for one v, which is a concrete finite falsifier.

Blocking gap: The sign and size of the non-Gaussian four-curvature cumulant Kappa_v are not controlled by reflection positivity alone; a heat-kernel cluster estimate or plaquette-sheet computation is needed.

## Falsifiers

- A same-theory heat-kernel or lattice plaquette measurement finds v^T B^rho v<0 for a vector v in the degenerate collar subspace.
- The connected four-curvature cumulant satisfies Kappa_v<-G_v+S_v/(alpha_N^2 g_R^4) for the first collar/hairpin geometry.
- Changing the connector tree changes R_ij at leading order after trace normalization, showing the proposed extraction is not a gauge-invariant coefficient.
- The boundary-OPE remainder scales like the retained R_ij term as rho is removed, invalidating the finite sign test.
- QHQ develops small eigenvalues comparable to the collar perturbation, so the Schur-Feshbach expansion is not valid in the tested regime.

## Learning

R_ij is no longer a symbolic parameter. With the heat-kernel regulator it is a definite connected Wilson cumulant: crossed two-curvature contractions give a positive color factor g_R^4(N^2-1)/(8N^2) times the squared geometric kernel, while the only dangerous term is the connected four-curvature cumulant. The valid finite test is the size comparison alpha_N^2 g_R^4(G_v+Kappa_v) versus the Schur hairpin energy S_v.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Instantiate the first collar/hairpin geometry on a hypercubic lattice: replace Phi_i by the oriented sum of flowed plaquette defects over Sigma_i, compute the crossed plaquette contraction C_ij and the connected four-plaquette cumulant, then compare Kappa_v to S_v/(alpha_N^2 g_R^4)-G_v for the finite kernel vectors.
