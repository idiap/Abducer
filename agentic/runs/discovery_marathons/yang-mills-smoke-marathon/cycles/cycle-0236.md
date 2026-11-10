# cycle-0236

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: heat-kernel extraction of the Wilson boundary polarization R

## Candidate Lemma

For the fixed three reflected Wilson hairpin block, heat-kernel flowed collar quotients decompose the second boundary-OPE coefficient into a nonnegative Wick-square polarization plus an irreducible connected four-flux and path-ordering commutator remainder. After the known one-body and length-linear cancellations, only this remainder can be a genuine same-theory falsifier.

## Definitions

- source object: heat-kernel-flowed cutoff Yang-Mills Wilson collar quotients \(\widehat q_{ij}(r,\varepsilon,a,L)\) for the fixed three reflected hairpin footprints, with standard bulk Wilson-loop renormalization already applied.
- target object: the continuum connected second boundary-OPE polarization matrix \(R_{ij}\) entering the corrected finite Schur-Feshbach form for the locked three-hairpin block.
- controlled interface: extract \(R\) as the \(r^2\) finite connected cumulant after diagonal normalization, then pass cutoff and volume limits only through finite reflected Wilson OS matrix entries.
- same-theory condition: the heat-flow regulator may smooth fields but may not add a reflection-plane boundary counterterm or change the locked gauge-invariant Wilson algebra.
- \(\Pi=\{t=0\}\) is the reflection plane, \(r\) is collar width, \(\varepsilon\) is heat-kernel flow time, and \(\gamma_i\subset\Pi\) are the boundary footprints of the hairpins.
- \(E_\alpha(\varepsilon,s)=F_{0\alpha}(\varepsilon,0,s)\) denotes the flowed normal-electric boundary field, parallel transported to a common base point before color contraction.

## Assumptions

- Take limits in the order \(a\downarrow0,L\uparrow\infty\) at fixed \((r,\varepsilon)\), then extract the small-collar coefficient with \(\sqrt\varepsilon=o(r)\), and finally test whether the finite part has an \(\varepsilon\downarrow0\) limit.
- The heat-kernel flowed Wilson loops are reflection-compatible and remain in the same gauge-invariant observable algebra after removing the regulator.
- The boundary OPE for every finite reflected Wilson matrix has a uniform \(O(r^{2+\alpha})\) remainder after diagonal normalization.
- The flowed two-flux boundary cumulant is color diagonal by gauge invariance and positive as a reflected boundary covariance.
- The irreducible four-flux cumulant and commutator contact terms have finite distributional boundary restrictions after ordinary bulk Wilson renormalization.

## Equations

- flowed boundary flux variable: `\Phi_i^{\varepsilon}=\int_{\gamma_i}\dot\gamma_i^\alpha(s)\,\operatorname{Ad}_{U_i(s)}F_{0\alpha}(\varepsilon,0,s)\,ds,\qquad W_i(r,\varepsilon)=d_R^{-1}\operatorname{tr}_R\mathcal P\exp\{ig r\Phi_i^{\varepsilon}+O(r^2)\}.`. Valid when: Valid when heat-kernel flow resolves the boundary field and the collar is small compared with footprint curvature radii but larger than the smoothing scale.
- normalized quotient OPE: `\log \widehat q_{ij}(r,\varepsilon)=rH_{ij}^{\varepsilon}+r^2\big(A_i^{\varepsilon}+A_j^{\varepsilon}+\ell_{ij}^{\varepsilon}+R_{ij}^{\varepsilon}\big)+O(r^{2+\alpha}).`. Valid when: Applies after diagonal normalization of Wilson collars and before taking the zero-flow limit, with uniform finite-matrix remainders.
- connected R decomposition: `R_{ij}^{\varepsilon}=R_{ij}^{\mathrm{Wick},\varepsilon}+R_{ij}^{4c,\varepsilon}+R_{ij}^{\mathrm{comm},\varepsilon},\qquad R_{ij}^{\mathrm{Wick},\varepsilon}=c_R g^4\int_{\gamma_i\times\gamma_j}|G_{\partial}^{\varepsilon}(s,t)|^2\,ds\,dt\ge0.`. Valid when: Valid when the boundary two-flux cumulant \(G_{\partial}^{\varepsilon}\) is reflection-positive and the four-flux cumulant is split into Wick and connected parts.
- irreducible four-flux term: `R_{ij}^{4c,\varepsilon}=c'_R g^4\int_{\gamma_i^2\times\gamma_j^2}\langle E(s_1)E(s_2)E(t_1)E(t_2)\rangle_{c,\varepsilon}\,d s_1d s_2d t_1d t_2\; +\;\text{color parallel-transport contractions}.`. Valid when: Requires the same-theory boundary OPE to give a locally integrable flowed connected four-point distribution on coincident reflected footprints.
- null-channel cancellation of nonconnected second terms: `x^T(A_i+A_j+\ell)x=0,\qquad x^TR^{\varepsilon}x=x^T\big(R^{\mathrm{Wick},\varepsilon}+R^{4c,\varepsilon}+R^{\mathrm{comm},\varepsilon}\big)x,\qquad x=(1,1,-2).`. Valid when: Applies for the previously isolated three-hairpin null channel where one-body Wilson factors and length-linear semigroup terms cancel exactly.
- R promotion or demotion gate: `\mathcal C_x^{\varepsilon}=\eta_{\mathrm{Schur}}+x^TR^{\mathrm{Wick},\varepsilon}x+x^T\big(R^{4c,\varepsilon}+R^{\mathrm{comm},\varepsilon}\big)x.`. Valid when: Valid when the first-order projected kernel has the fixed one-dimensional null space and the corrected Schur-Feshbach margin \(\eta_{\mathrm{Schur}}>0\) has already been computed.

## Attempted Derivation

- Choose heat-kernel flow as the regulator: replace each gauge field in the collar Wilson loop by the flowed field at time \(\varepsilon\), keeping the Wilson observable gauge invariant by parallel transport along the flowed loop.
- Use a collar version of nonabelian Stokes expansion: a hairpin of width \(r\) inserts the boundary normal-electric flux \(\Phi_i^{\varepsilon}\) plus higher-area corrections.
- Expand the logarithm of the diagonally normalized quotient \(\widehat q_{ij}\) by connected cumulants. Diagonal self-energy terms become \(A_i+A_j\); semigroup/length terms become \(\ell_{ij}\); the remaining nonlinear pair-dependent finite part is \(R_{ij}\).
- Evaluate the Gaussian/Wick part of the four-flux cumulant. Reflection positivity of the two-flux kernel makes \(R_{ij}^{\mathrm{Wick}}\) an integral of \(|G_{\partial}|^2\), hence nonnegative in every real polarization.
- Insert the previously found null vector only to identify cancellations, not to rederive the old threshold: \(x^T(A_i+A_j+\ell)x=0\), so the decisive new number is the connected boundary polarization \(x^T(R^{4c}+R^{\mathrm{comm}})x\) added to the positive Wick and Schur margins.
- The branch therefore computes a sign decomposition of R: perturbative Gaussian boundary damping promotes the block; a negative non-Gaussian connected four-flux or commutator contact of larger size is the first real falsifier.

Blocking gap: No Yang-Mills estimate yet proves a regulator-independent lower bound for \(x^T(R^{4c,\varepsilon}+R^{\mathrm{comm},\varepsilon})x\) as coincident boundary footprints are unsmoothed.

## Falsifiers

- A valid falsifier is a negative heat-flow finite part of the irreducible boundary four-flux cumulant whose magnitude exceeds the positive Wick-square and Schur margins.
- A commutator/path-ordering contact term localized at the reflection-plane cusp with negative coefficient would falsify the same-theory R gate.
- If two admissible gauge-invariant regulators give different finite \(R\) after standard bulk Wilson renormalization, the branch has found a boundary counterterm dependence rather than OS positivity for the same theory.
- Failure of local integrability for the connected four-flux boundary restriction is a falsifier of the proposed collar trace theorem, even if fixed-collar positivity remains valid.

## Learning

The first new R computation is a decomposition, not another threshold: heat-kernel regularization identifies a nonnegative Wick-square contribution to the connected boundary-OPE polarization. The dangerous term is narrower than before: only the irreducible connected four-flux cumulant and the nonabelian commutator contact can defeat the corrected second-order form. One-body Wilson renormalizations and length-linear terms cancel in the null channel, so a surviving negative result would be a genuine mixed-boundary falsifier.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute \(R^{4c,\varepsilon}\) explicitly for two nested interval footprints using the heat-kernel flowed boundary four-flux cumulant: subtract the Wick square, retain parallel-transport color contractions, estimate the commutator contact, and test the sign of the null-channel polarization before sending \(\varepsilon\downarrow0\).

# Gauge-Invariant Nontriviality Witness Selection: H,K hairpin boundary polarization extraction

## Candidate Lemma

For the first H,K collar/hairpin reduction, the connected boundary-OPE polarization term is a heat-flow, point-split covariance of transported normal-electric curvature insertions; after perimeter/cusp and disconnected cumulant cancellation it enters the valid plus-channel Schur-Feshbach test as the additive term competing with leakage.

## Definitions

- source object: the same continuum OS-positive Yang-Mills Schwinger family, evaluated on heat-flowed Wilson collars at flow time ε and boundary point-splitting ρ.
- target object: the finite H,K hairpin positivity matrix with coefficients p,q,r,s,t,δ and corrected plus-channel scalar Q_+.
- controlled interface: extract R_{ij} from the connected second cumulant of two renormalized thin hairpin Wilson collars before applying the Schur-Feshbach cone theorem.
- same-theory condition: ε,ρ and collar thickness λ are regulators for observables in the same Schwinger family, with no auxiliary Gaussian or changed measure introduced.
- Let Σ be the reflection plane and n the Euclidean normal.
- Let I_i be the boundary footprint of hairpin i, ψ_i its signed boundary density, and A_ε the Yang-Mills gradient-flow regularized connection.
- Let \mathcal E_ε^a(u)=\operatorname{Ad}_{U_{u_0u}^{ε}}^{ab}F_{nτ}^{b,ε}(u) be the gauge-transported normal-electric insertion along Σ.
- Let \widehat W_i^λ denote the Wilson hairpin after subtracting the same one-hairpin perimeter/cusp counterterm m_i.

## Assumptions

- Mandelstam area differentiation is valid for heat-flowed Wilson loops at fixed ε>0.
- The collar limit λ↓0 is taken before the OS cutoff removal, with ρ>0 preventing boundary contact collisions.
- The one-hairpin counterterm is fixed from the same Wilson family and is not refit in the two-hairpin cumulant.
- The H,K remainder block has δ>0, so the finite Schur-Feshbach correction is defined.

## Equations

- transported boundary electric kernel: `\mathcal G_{ε,ρ}(u,v)=\big\langle \mathcal E_ε^a(u+ρn)\,\mathcal U_{uv}^{ab,ε}\,\mathcal E_ε^b(v+ρn)\big\rangle_c`. Valid when: Valid when the two boundary insertions are heat-flow smeared and point-split before the collar width is sent to zero.
- polarization matrix: `R_{ij}^{ε,ρ}=\int_{I_i}\!du\int_{I_j}\!dv\;ψ_i(u)ψ_j(v)\,\mathcal G_{ε,ρ}(u,v)`. Valid when: Applies when the Wilson footprints are fixed smooth intervals and the gauge connectors stay inside the regulated boundary collar.
- connected Wilson cumulant extraction: `\kappa_2(\widehat W_i^λ,\widehat W_j^λ)=λ^2R_{ij}^{ε,ρ}+o_{ε,ρ}(λ^2)`. Valid when: Requires the same-theory perimeter, cusp, and disconnected product subtractions to be made before taking the thin-collar limit.
- plus-channel decomposition: `p+2q+r=L_+^{ε,ρ}+R_{++}^{ε,ρ},\qquad R_{++}^{ε,ρ}=R_{11}^{ε,ρ}+2R_{12}^{ε,ρ}+R_{22}^{ε,ρ}`. Valid when: Valid when the H,K symmetry reduction identifies the plus vector with the sum of the two boundary hairpin densities.
- corrected second-order scalar: `Q_+^{ε,ρ}=L_+^{ε,ρ}+R_{++}^{ε,ρ}-\frac{(s^{ε,ρ}+t^{ε,ρ})^2}{δ^{ε,ρ}}`. Valid when: Applies after diagonal normalization of the positive remainder block and after projecting to the flat plus channel.
- promotion inequality: `R_{++}^{\mathrm{ren}}>\frac{(s+t)^2}{δ}-L_+ +η\quad\Longrightarrow\quad Q_+^{\mathrm{ren}}\ge η`. Valid when: Valid when the joint renormalized limits of R, L, s, t, and δ exist along the same cutoff-removal net.

## Attempted Derivation

- Use gradient flow A↦A_ε and boundary point-splitting ρ to make Wilson collars differentiable observables at fixed regulator.
- Apply the Mandelstam area derivative to a thin hairpin: the first collar displacement produces a transported insertion of F_{nτ} on the boundary footprint.
- Normalize each hairpin by the same one-loop object m_i, removing perimeter and cusp self-contractions before forming any two-hairpin quantity.
- Take the connected cumulant κ_2(\widehat W_i^λ,\widehat W_j^λ); the product of one-point Wilson expectations cancels the disconnected contraction, leaving only the connected transported electric kernel.
- Let λ↓0 at fixed ε,ρ to identify the λ^2 coefficient with R_{ij}^{ε,ρ}.
- Project the H,K matrix to the plus vector, giving R_{++}=R_{11}+2R_{12}+R_{22}, and insert it into the already-promoted Schur-Feshbach scalar Q_+.
- The branch promotes only if the renormalized R_{++} exceeds the Feshbach leakage deficit by a positive margin.

Blocking gap: The derivation extracts R symbolically but does not yet compute or bound the renormalized sign and size of the connected boundary electric kernel as ε,ρ go to zero in the interacting same-theory limit.

## Falsifiers

- Regulator falsifier: R_{++}^{ε,ρ} changes by a finite amount under admissible ε↓0,ρ↓0 paths after the fixed one-hairpin subtraction.
- Cumulant falsifier: the disconnected Wilson product does not cancel the leading boundary contraction, so the extracted R is not connected.
- Same-theory falsifier: a new two-hairpin counterterm is needed to make R finite.
- Sign falsifier: the computed R_{++}^{ren} is below (s+t)^2/δ-L_+, forcing Q_+<0 in the corrected second-order form.
- Interface falsifier: the transported F_{nτ} insertion cannot be obtained as an OS observable limit of the original Wilson algebra.

## Learning

The useful next object is not another obstruction ladder but the connected boundary-OPE polarization kernel. The regulator is Yang-Mills gradient flow plus boundary point-splitting; the cumulant is κ_2 of two renormalized thin Wilson hairpins; the cancellation is disconnected product plus one-hairpin perimeter/cusp subtraction. The decisive valid test is whether R_{++}^{ren} is large enough to overcome Schur-Feshbach leakage in Q_+.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the heat-flowed connected kernel \mathcal G_{ε,ρ} for two parallel boundary footprints: first separate its contact, perimeter, and connected pieces by the Wilson area-derivative formula, then test the plus-channel inequality numerically or symbolically before taking ε,ρ↓0.

# Heat-kernel Wilson hairpin R-cumulant extraction for the Schur-corrected finite audit

## Candidate Lemma

For heat-kernel regularized reflected Wilson hairpins of collar height \rho, the boundary-OPE polarization coefficient R entering the finite Schur-Feshbach second-order form is the connected cumulant of two quadratic transported curvature fluxes. It splits into a nonnegative two-contraction square plus a genuinely non-Gaussian four-curvature cumulant; promotion requires this latter term and the Schur subtraction to be dominated.

## Definitions

- source object: OS-positive Euclidean SU(N) Yang-Mills Schwinger functional with heat-kernel flowed connection A^{(a)}, rounded Wilson hairpins H_i(\rho), and collar Wilson loops K_\alpha(\rho) in one reflected half-space.
- target object: the finite Gram perturbation coefficient L_{PP}^{ij}=R_{ij}^{(a,\rho)} used in the Schur-Feshbach corrected tangent-cone test on P=\ker H_0.
- controlled interface: regulated Wilson cumulants -> boundary-OPE coefficients -> finite Gram blocks H_0,K_1,L_2 with no spectral-density claim inserted.
- same-theory condition: the same gauge group, coupling, reflection plane, flow time a, cusp rounding, vacuum subtraction, and diagonal normalization are used on both sides; no auxiliary Gaussian measure replaces Yang-Mills.

## Assumptions

- Reflection positivity survives the heat-kernel Wilson regulator at fixed a>0 and rounded cusp radius comparable to a.
- Each hairpin bounds a thin surface S_i=I_i\times[0,\rho] with \rho smaller than boundary separation and curvature scales.
- The transported curvature flux B_i^\alpha=\int_{S_i} U_{x_i,x}F^{(a),\alpha}_{01}(x)U_{x,x_i}\,d^2x has finite connected cumulants up to order four.
- The boundary OPE has a remainder o(\rho^4) after vacuum subtraction and diagonal loop renormalization.
- QH_0Q is strictly positive on the finite complement Q of the null hairpin sector.

## Equations

- heat-kernel Wilson hairpin: `W_i^{(a)}(\rho)=N^{-1}\operatorname{Tr}\,\mathcal P\exp\!\left(\oint_{\partial S_i} A^{(a)}\right),\qquad A^{(a)}=e^{a^2\Delta_{\mathrm{cov}}/2}A`. Valid when: Valid when heat-kernel flowed connections define finite reflected Wilson observables with rounded cusps and fixed positive flow time.
- first surviving gauge-invariant boundary channel: `X_i:=W_i^{(a)}-\langle W_i^{(a)}\rangle=-\frac{g_a^2}{2N}:B_i^\alpha B_i^\alpha:+O(\rho^3\|F^{(a)}\|^3)`. Valid when: Valid when the hairpin surface is smaller than separation scales and the non-Abelian Stokes expansion is used before removing the regulator.
- connected R polarization decomposition: `R_{ij}^{(a,\rho)}=\frac{g_a^4}{4N^2}\kappa_2(:B_i^\alpha B_i^\alpha:,:B_j^\beta B_j^\beta:)=\frac{g_a^4}{4N^2}\left(2C_{ij}^{\alpha\beta}C_{ij}^{\alpha\beta}+\kappa_4(B_i^\alpha,B_i^\alpha,B_j^\beta,B_j^\beta)\right)+o(\rho^4)`. Valid when: Valid when vacuum subtraction is applied and all fields are evaluated in one regulated Yang-Mills measure.
- thin-collar curvature contraction: `C_{ij}^{\alpha\beta}=\langle B_i^\alpha B_j^\beta\rangle_c=\delta^{\alpha\beta}\epsilon_i\epsilon_j\rho^2\int_{I_i\times I_j}\mathcal K_{01,01}^{(a)}(s-t)\,ds\,dt+O(\rho^3)`. Valid when: Valid when the heat-kernel radius is below boundary separation and the collar height is below all curvature radii.
- diagonal normalization cancels loop counterterms: `\widehat R_{ij}^{(a,\rho)}=\frac{R_{ij}^{(a,\rho)}}{\sqrt{R_{ii}^{(a,\rho)}R_{jj}^{(a,\rho)}}},\qquad Z_{\mathrm{per}}(S_i)Z_{\mathrm{cusp}}(S_i)\text{ cancels from }\widehat R_{ij}`. Valid when: Valid when diagonal variances are nonzero and the same multiplicative loop counterterms occur in numerator and denominator.
- Schur-corrected Wilson audit form: `\mathfrak q(v)=\langle v,L_{PP}v\rangle-\langle QK_1Pv,(QH_0Q)^{-1}QK_1Pv\rangle,\qquad L_{PP}^{ij}=R_{ij}^{(a,\rho)}+\text{local }m_i^2\delta_{ij}`. Valid when: Valid when a finite Gram expansion is C2 in the collar parameter and QH0Q has a positive inverse on Q.

## Attempted Derivation

- Fixed the regulator: heat-kernel flow time a>0 with cusp rounding radius comparable to a, so Wilson loops and curvature cumulants are finite before any limit.
- Expanded each thin hairpin by non-Abelian Stokes. The trace kills the linear transported flux; the first vacuum-subtracted gauge-invariant channel is :B_i^\alpha B_i^\alpha:.
- Evaluated the Wilson contraction being tested: the connected cumulant \kappa_2(:B_i^2:,:B_j^2:), not a disconnected product of Wilson expectations.
- Used the cumulant identity \kappa_2(X^2,Y^2)=2\kappa_2(X,Y)^2+\kappa_4(X,X,Y,Y), with color sums and transported fluxes, to decompose R into a positive Gaussian square and a sign-indefinite Yang-Mills connected four-point term.
- Used the thin-collar expansion B_i^\alpha=\epsilon_i\rho\int_{I_i}F_{01}^{(a),\alpha}(0,s)ds+O(\rho^2), giving C_{ij}^{\alpha\beta}=\delta^{\alpha\beta}\epsilon_i\epsilon_j\rho^2\int\mathcal K_{01,01}^{(a)}+O(\rho^3).
- Identified the cancellation being used: vacuum subtraction removes the identity channel, while diagonal normalization cancels equal perimeter and cusp factors from the same Wilson measure.
- Inserted L_{PP}=R+local diagonal terms into the finite Schur-Feshbach form and obtained an explicit promotion/demotion inequality involving R^{ng} and the Schur subtraction \Sigma.

Blocking gap: The sign and size of the regulated connected four-curvature cumulant \kappa_4(B_i,B_i,B_j,B_j) are not controlled by OS positivity; reflection positivity gives covariance positivity but not domination of non-Gaussian cumulants by the two-contraction square.

## Falsifiers

- falsifier: a negative regulated four-curvature cumulant with magnitude larger than the two-contraction square plus local diagonal mass terms makes the corrected Schur form negative.
- falsifier: perimeter or cusp renormalization fails to cancel under diagonal normalization because the reflected hairpin and collar use inequivalent regulators.
- falsifier: QH0Q has a small eigenvalue at the same \rho order as R, so the Schur subtraction dominates every positive R contribution.
- falsifier: the boundary OPE develops contact delta terms at the reflection plane that survive vacuum subtraction and change the finite matrix coefficient.
- falsifier: diagonal variance Rii vanishes in the OS null quotient, so normalized hairpin carriers are not valid vectors.

## Learning

The branch is no longer looping on OS density. The concrete R term is the connected cumulant of two quadratic transported curvature fluxes. Its Gaussian part is positive and computable from the heat-kernel boundary curvature contraction; the only decisive unknown is the non-Gaussian four-curvature cumulant and whether it is large enough, after the Schur subtraction, to keep the corrected second-order Wilson form nonnegative.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Evaluate the heat-kernel integral \int_{I_i\times I_j}\mathcal K_{01,01}^{(a)} and estimate the regulated connected F4 cumulant for the minimal two-hairpin/one-collar matrix; compare the resulting R lower bound directly against the Schur subtraction \Sigma.
