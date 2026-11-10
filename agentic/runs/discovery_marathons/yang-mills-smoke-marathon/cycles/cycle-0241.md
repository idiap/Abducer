# cycle-0241

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint kappa4 box bound for the Wilson hairpin R term

## Candidate Lemma

For the concrete three-hairpin block after H,K extraction, the remaining dangerous connected polarization is endpoint-local in the heat-kernel plaquette-sheet regulator: after Wick-square positivity and straight-segment ff-contact cancellation, it is a signed endpoint-box integral of the renormalized connected four-flux cumulant plus a controlled tail.

## Definitions

- source object: heat-kernel plaquette-sheet regulated SU(N) Yang-Mills Wilson hairpins W_i^{a,\sigma,\delta} in the locked gauge-invariant lattice/continuum test algebra.
- target object: the Schur-Feshbach second-order null-channel OS quotient scalar \mathcal S_\eta after H,K are known and one-body Wilson factors are removed.
- controlled interface: expansion of reflected Wilson collar products into boundary flux cumulants, followed by projection onto the null endpoint incidence tensor Q_\eta.
- same-theory condition: the same heat-kernel Wilson-loop regulator, diagonal normalization, and gauge-invariant observable algebra are used before and after collar collapse, with no boundary counterterm added.
- \eta is the previously found null channel; E is the set of geometric endpoints/corners left after straight-footprint cancellation.
- Q_p^{ab} is the oriented endpoint incidence tensor for two color flux insertions at endpoint p, including the concrete hairpin signs and fundamental trace normalization T_F.

## Assumptions

- Regulator ordering is a\ll \sigma\ll \ell\ll d_{sep}, where \ell is the endpoint-box radius and d_{sep} separates distinct nonadjacent corners.
- The connected four-flux cumulant of heat-kernel smeared, parallel transported curvature insertions has a regulator-uniform integrable clustering bound.
- The earlier Wick-square term is a nonnegative Gram contribution and is not used as a falsifier.
- The straight boundary ff commutator contact cancels in the concrete null geometry, leaving only endpoint/corner support.
- The finite Schur-Feshbach H,K theorem is already valid with a uniform second-order remainder.

## Equations

- heat-kernel flux cumulant: `\mathcal F_{\sigma}^{a}(x)=\int K_{\sigma}(x,y)\,U_{x\leftarrow y}F_{\mu\nu}^{a}(y)U_{y\leftarrow x}\,dy,\quad \kappa_{4,c}^{abcd}=\langle \mathcal F_{\sigma}^{a}(x_1)\mathcal F_{\sigma}^{b}(x_2)\mathcal F_{\sigma}^{c}(x_3)\mathcal F_{\sigma}^{d}(x_4)\rangle_c`. Valid when: Valid when the heat-kernel radius sigma is larger than the lattice spacing and all fluxes are parallel transported to a common boundary frame.
- irreducible four-flux contribution to R: `R_{ij}^{\kappa_4}=\frac{g_{\sigma}^{4}}{4N^{2}}\int_{\Sigma_i^2\times\Sigma_j^2}{\rm tr}(T^aT^b){\rm tr}(T^cT^d)\,\kappa_{4,c}^{abcd}(x,y,z,w)\,d\mu_{\sigma}^{4}`. Valid when: Valid when the Wilson logarithm is expanded to fourth boundary-flux order after diagonal one-loop and two-loop normalizations have been removed.
- null-channel cancellations before endpoint extraction: `\sum_i\eta_i\chi_{\Gamma_i^{\circ}}(s)n_i(s)=0,\quad \mathcal R_{\eta}^{ff,{\rm bulk}}=0,\quad \mathcal R_{\eta}^{\rm Wick}\ge 0`. Valid when: Applies after diagonal normalization in the concrete hairpin geometry, with matched straight boundary orientations and the previously verified bulk ff-contact cancellation.
- endpoint-box reduction: `\mathcal R_{\eta}^{\rm rem}=\frac{g_{\sigma}^{4}T_F^{2}}{4N^{2}}\sum_{p,q\in E}Q_{p}^{ab}Q_{q}^{cd}\int_{B_p(\ell)^2\times B_q(\ell)^2}\Pi_{\rm sing}^{abcd}\kappa_{4,c}^{abcd}\,d\mu_{\sigma}^{4}+{\rm Err}_{\sigma,\ell}`. Valid when: Requires the same-theory boundary OPE with heat-kernel support much smaller than the endpoint-box size and with separated boxes farther apart than sigma.
- tail estimate from clustering: `|{\rm Err}_{\sigma,\ell}|\le C_{\rm geo}g_{\sigma}^{4}C_4\big((\sigma/\ell)^r+e^{-d_{\rm sep}/(c\sigma)}\big)`. Valid when: Valid when the connected four-flux cumulant satisfies the stated integrable clustering bound uniformly in the continuum regulator.
- endpoint sign gate: `\mathcal S_{\eta}=M_G+\mathcal R_{\eta}^{\rm rem}+o(1),\quad M_G=8m^2,\quad \mathcal S_{\eta}<0\Rightarrow {\rm same\mbox{-}theory\ OS\ falsifier}`. Valid when: Applies after the finite Schur-Feshbach H,K extraction and only in the null channel left by the first-order PHP test.

## Attempted Derivation

- Expanded the heat-kernel regulated reflected Wilson collar product to fourth order in boundary flux insertions, keeping only connected cumulants after diagonal Wilson normalizations.
- Separated the fourth-order term into Wick-square, local nonabelian ff contact, and irreducible connected four-flux cumulant pieces; the Wick-square piece is positive and the straight-segment ff contact cancels in the null geometry.
- Inserted a partition of unity on the reflection-plane footprint: straight interior strips plus endpoint boxes B_p(\ell). The null incidence identity kills the interior connected source, leaving only endpoint boxes and clustering tails.
- Projected the remaining color structure through fundamental traces, giving the factor g_\sigma^4T_F^2/(4N^2) times a singlet-projected connected four-flux endpoint matrix.
- Converted the endpoint matrix into a computable lower bound by its negative Hermitian eigenvalue and compared the bound with the positive Gaussian Schur-Feshbach margin M_G.

Blocking gap: The missing estimate is a signed, regulator-uniform lower bound for the singlet-projected connected four-flux cumulant in endpoint boxes; available clustering bounds control size but not the sharp negative part.

## Falsifiers

- Endpoint falsifier: a heat-kernel lattice or OPE computation gives \mathcal R_{\eta}^{\rm rem}<-8m^2-\epsilon with a uniform continuum/collar error bound.
- A logarithmic or power endpoint anomaly remains after Wilson-loop renormalization, showing that the same-theory boundary trace is not valid.
- The straight-segment ff cancellation fails when the actual oriented plaquette-sheet geometry is used rather than the idealized footprint incidence model.
- The connected four-flux cumulant lacks uniform integrability in endpoint boxes, so the endpoint matrix \mathfrak K^{\sigma,\ell} has no cutoff-independent lower bound.
- Parallel transport in the heat-kernel regulator creates a boundary counterterm not present in the locked Wilson algebra.

## Learning

Cycle 241 computes the next R layer as an endpoint-box problem, not another symbolic threshold. In the heat-kernel plaquette-sheet regulator, the dangerous post-H,K term is the singlet-projected connected four-flux cumulant localized at endpoints after two cancellations. The first valid promotion/demotion parameter is the negative eigenvalue of this endpoint cumulant matrix multiplied by the explicit color/geometric incidence norm.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Evaluate \mathfrak K^{\sigma,\ell} for the actual endpoint boxes: start with small heat-kernel lattice plaquette sheets, compute the singlet connected four-plaquette cumulant with parallel transport, subtract Wick-square and ff-contact pieces, then estimate \lambda_{\min}({\rm Herm}\,\mathfrak K) against the Schur-Feshbach margin.

# Flowed hairpin endpoint-box R-kernel decomposition

## Candidate Lemma

For two separated thin Wilson hairpins regulated by Yang-Mills gradient flow and boundary point-splitting, the post-H,K endpoint-box coefficient has the same-theory expansion R_{ij}^{ren}=P_{ij}[1+(g_R^2N/16π^2)Xi_{ij}+O(g_R^4)]+O((ell/d)^2P_{ij}), where P_{ij} is the explicit positive cross-pairing and Xi_{ij} is a finite connected four-curvature polarization integral. Promotion requires a valid lower bound on R_{++}^{ren} exceeding the Schur-Feshbach leakage gap; demotion occurs if the connected polarization drives this lower bound below it.

## Definitions

- source object: centered renormalized SU(N) Wilson hairpin observables built from the flowed gauge field B_mu(t,x), with boundary point-splitting rho and perimeter/cusp counterterms fixed in the original continuum Schwinger family.
- target object: the finite H,K Schur-Feshbach endpoint-box matrix R^{ren}_{ij}, especially the plus-channel entry R^{ren}_{++}=v_+^T R^{ren}v_+, needed after the H,K coefficients are known.
- controlled interface: identify R^{ren}_{ij} with the continuum cumulant kappa_2(H_i^{ren},H_j^{ren}) and decompose it into the Wick cross-pairing P_{ij} plus the connected four-curvature polarization C^{ren}_{4,ij}.
- same-theory condition: gradient flow time t>0 and splitting rho>0 are regulators for the same Yang-Mills measure; the subtraction is disconnected-product removal plus one-hairpin perimeter/cusp subtraction, not replacement by an auxiliary Gaussian theory.
- B_{mu nu}^a(t,x) is the curvature of the flowed connection, and Delta^{(t)}_{mu nu,alpha beta}(x) is its tree flowed two-point kernel.
- Omega_i^{mu nu}(x) is the oriented point-split surface tensor of the i-th thin hairpin collar, supported away from coincident boundary endpoints.

## Assumptions

- Gauge group SU(N), fundamental trace normalization tr(T^aT^b)=delta^{ab}/2.
- Hairpin diameters ell are small compared with mutual separation d, while sqrt(t) and rho regulate endpoint and UV singularities before any thin-loop limit.
- The boundary-OPE remainder for each hairpin is O((ell/d)^2) after centering and perimeter/cusp subtraction.
- The plus-channel vector v_+ is the finite H,K channel already isolated by the Schur-Feshbach reduction.

## Equations

- renormalized hairpin curvature-square expansion: `H_i^{ren}=-\frac{g_R^2}{4N}\int_{S_i^\rho\times S_i^\rho}\Omega_i^{\mu\nu}(x)\Omega_i^{\alpha\beta}(y):B_{\mu\nu}^a(t,x)U_{xy}^{ab}(t)B_{\alpha\beta}^b(t,y):\,dx\,dy+O(\ell^6)`. Valid when: Valid when the flowed Wilson hairpin is thin, point-split, centered, and expanded in the boundary OPE before removing the flow regulator.
- cross-pairing geometry: `M_{ij}(t,\rho)=\int_{S_i^\rho\times S_j^\rho}\Omega_i^{\mu\nu}(x)\Omega_j^{\alpha\beta}(u)\Delta^{(t)}_{\mu\nu,\alpha\beta}(x-u)\,dx\,du`. Valid when: Valid when the two hairpin supports are disjoint and the flowed curvature covariance is evaluated in the same continuum gauge-invariant Schwinger family.
- positive pair term: `P_{ij}=\frac{g_R^4}{16N^2}\,2(N^2-1)\,M_{ij}(t,\rho)^2\ge 0`. Valid when: Applies after diagonal normalization of the centered hairpins and after subtracting same-hairpin perimeter and cusp self-pairings.
- connected polarization term: `C^{ren}_{4,ij}=\frac{g_R^6}{16N^2}\,\frac{N(N^2-1)}{16\pi^2}\int\Omega_i\Omega_i\Omega_j\Omega_j\,\Pi^{(1),conn}_{t,\perp}(x,y,u,v)\,dx\,dy\,du\,dv+O(g_R^8)`. Valid when: Requires the same-theory boundary OPE with flowed fields, separated hairpins, and Ward cancellation of longitudinal and contact kernels.
- dimensionless endpoint-box ratio: `R^{ren}_{ij}=P_{ij}+C^{ren}_{4,ij}=P_{ij}\left(1+\frac{g_R^2N}{16\pi^2}\Xi_{ij}+O(g_R^4)+O((\ell/d)^2)\right)`. Valid when: Valid when M_{ij} is nonzero and the one-loop flowed four-curvature integral is finite after the stated subtractions.
- promotion inequality: `R^{ren}_{++}>L_+\quad\text{with}\quad R^{ren}_{++}=v_+^TR^{ren}v_+`. Valid when: Valid when the H,K Schur-Feshbach leakage gap L_+ has already been computed in the same finite collar/hairpin reduction.

## Attempted Derivation

- Start from kappa_2(H_i^{ren},H_j^{ren}) for two centered flowed Wilson hairpins; centering removes <H_i><H_j> and the one-hairpin counterterms remove perimeter/cusp self-contractions.
- Use the small-loop boundary OPE: each thin hairpin contributes the gauge-invariant bilocal curvature-square operator with coefficient -g_R^2/(4N).
- Contract one flowed curvature from hairpin i with one from hairpin j in both possible ways. This gives the explicit positive term P_{ij} with color factor 2(N^2-1).
- The remaining non-Wick connected part is the cumulant kappa_4(B,B,B,B). At first perturbative order it has color factor N(N^2-1) and a finite flowed transverse kernel Pi^{(1),conn}_{t,perp}.
- Gauge-longitudinal and coincident endpoint kernels cancel against closed surface tensors and the perimeter/cusp subtraction; this is the essential valid same-theory cancellation.
- Normalize C^{ren}_{4,ij} by P_{ij} to isolate Xi_{ij}; the sign question is now a finite color-geometric endpoint-box integral, not a symbolic lambda model.

Blocking gap: The sign and sharp size of Xi_{++} for the actual H,K hairpin geometry have not yet been evaluated; only the finite integral and the operator-norm falsifier are isolated.

## Falsifiers

- Geometry falsifier: M_{++}(t,rho)=0 or is too small, making the positive pair baseline vanish while the connected polarization remains uncontrolled.
- Sign falsifier: a valid evaluation gives 1+(g_R^2N/16π^2)Xi_{++}+O(g_R^4)<L_+/P_{++}.
- Scheme falsifier: the endpoint-box term changes under allowed same-theory perimeter/cusp subtraction choices, so R^{ren}_{++} is not a controlled interface invariant.
- Regulator falsifier: the t>0 flowed bound is finite but no uniform window exists as rho and the thin-hairpin scale are matched.
- Perturbative falsifier: the one-loop C4 estimate is dominated by the O(g_R^4) remainder in the relevant coupling window.

## Learning

The branch is no longer looping on Wilson/OS obstruction language. The endpoint-box R term is a concrete flowed cumulant: a positive pair baseline with color factor 2(N^2-1) plus a finite connected four-curvature polarization with color factor N(N^2-1). The decisive valid work is now computing or bounding Xi_{++}; every serious falsifier is a sign, size, geometry, or regulator-window failure of that finite integral.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Choose the actual plus-channel H,K hairpin surfaces, write their Omega_+ tensors explicitly, then evaluate M_{++} and the flowed transverse one-loop box integral Xi_{++} by symmetry reduction before attempting numerical quadrature.

# Heat-kernel endpoint-box R/kappa4 extraction after Schur-Feshbach correction

## Candidate Lemma

For a finite family of same-theory Wilson endpoint boxes, the post-H,K second-order endpoint matrix R is the heat-kernel connected cumulant of two quadratic transported curvature fluxes. Its Wick part is a positive Hilbert-Schmidt square with color factor g_R^4/(8N^2), while all possible sign loss is isolated in the connected four-curvature cumulant kappa_4 and the boundary-OPE remainder.

## Definitions

- source object: heat-kernel point-split Euclidean SU(N) Yang-Mills Wilson collars with transported curvature fluxes in disjoint endpoint boxes.
- target object: the finite endpoint-box matrix R_sigma entering P(R_sigma)-B_sigma^*E_sigma^{-1}B_sigma on the Schur-Feshbach first-order kernel.
- controlled interface: normalized vacuum-subtracted Wilson cumulants are expanded only through same-regulator curvature flux cumulants, then inserted into the finite Schur-Feshbach tangent cone.
- same-theory condition: the regulator, coupling g_R, Wilson-line transports, vacuum subtraction, and perimeter normalization are identical in the Wilson cumulant and in the H,K hairpin blocks; no auxiliary Gaussian theory replaces Yang-Mills.
- F_{mu nu,sigma} is covariantly heat-kernel smeared and parallel transported to a common base point o before color contraction.
- kappa_{ij,sigma} is the connected four-flux cumulant Cum_4(Phi_i^a,Phi_i^a,Phi_j^b,Phi_j^b), with repeated color indices summed.

## Assumptions

- Endpoint boxes S_i are disjoint at regulator scale sqrt(sigma), so contact counterterms are not hidden in crossed contractions.
- The fundamental generators obey Tr(T^aT^b)=delta^{ab}/2 and Wilson loops are normalized by N^{-1}Tr.
- The boundary OPE of the regulated Wilson loop is valid through fourth flux order with a controlled remainder E^{OPE}_sigma.
- The finite H,K hairpin blocks have already been computed in the same normalization, with E_sigma=QHQ positive on the complement of the first-order kernel.

## Equations

- transported regulated flux: `\Phi_{i,\sigma}^{a}=\int_{S_i}n_i^{\mu\nu}(x)\,[\operatorname{Ad}U_{x\to o}]^{ab}F_{\mu\nu,\sigma}^{b}(x)\,dA(x)`. Valid when: Valid when the endpoint boxes are disjoint and the covariant heat-kernel point splitting is kept positive before the boundary OPE limit.
- normalized Wilson quadratic term: `\frac{1}{N}\operatorname{Tr}U(S_i)=1-\frac{g_R^2}{4N}\Phi_{i,\sigma}^{a}\Phi_{i,\sigma}^{a}+O(g_R^3\|\Phi_{i,\sigma}\|^3)`. Valid when: Applies after diagonal normalization of fundamental Wilson loops and before taking the heat-kernel regulator to zero.
- R as connected Wilson cumulant: `R_{ij,\sigma}=\operatorname{Cum}_2(W_i,W_j)_{g_R^4,\mathrm{conn}}=\frac{g_R^4}{16N^2}\operatorname{Cum}_2(\Phi_i^a\Phi_i^a,\Phi_j^b\Phi_j^b)+O(g_R^6)`. Valid when: Requires vacuum-subtracted Wilson observables so self-energy and one-loop perimeter factors cancel inside the connected cumulant.
- Gaussian plus kappa4 decomposition: `R_{ij,\sigma}=\frac{g_R^4}{8N^2}\sum_{a,b}C_{ij,\sigma}^{ab}C_{ij,\sigma}^{ab}+\frac{g_R^4}{16N^2}\kappa_{ij,\sigma}+E^{\mathrm{OPE}}_{ij,\sigma},\quad C_{ij,\sigma}^{ab}=\langle\Phi_{i,\sigma}^{a}\Phi_{j,\sigma}^{b}\rangle`. Valid when: Valid when the reflected Wilson observables are expanded to fourth flux order and all higher boundary-OPE terms are controlled uniformly.
- corrected endpoint-box positivity test: `\mathfrak q_{\sigma}(v)=v^*P(R_{G,\sigma}+R_{\kappa,\sigma}+E^{\mathrm{OPE}}_{\sigma})Pv-v^*B_{\sigma}^*E_{\sigma}^{-1}B_{\sigma}v\ge 0`. Valid when: Requires the same-theory boundary OPE, known H,K hairpin blocks, and a finite Schur-Feshbach reduction on the first-order kernel.

## Attempted Derivation

- Fixed a covariant heat-kernel regulator and represented each endpoint Wilson box by its transported curvature flux Phi_{i,sigma}.
- Expanded N^{-1}Tr U(S_i). The trace-zero linear flux term vanishes, and the first gauge-invariant contribution is -g_R^2 Phi_i^a Phi_i^a/(4N).
- Formed Cum_2(W_i,W_j). Vacuum subtraction and identical perimeter normalization cancel the local self-contractions <Phi_i^2><Phi_j^2>, leaving only crossed contractions and Cum_4.
- Applied Wick decomposition to the fourth flux moment. The two crossed pairings give 2 C_{ij}^{ab}C_{ij}^{ab}, hence the coefficient g_R^4/(8N^2). In a color-diagonal channel this is g_R^4(N^2-1)C_{ij}^2/(8N^2).
- Identified the remaining same-theory term as R_{kappa,ij}=g_R^4 kappa_{ij,sigma}/(16N^2), not as an adjustable symbolic lambda.
- Inserted R_sigma into the finite Schur-Feshbach endpoint form P R_sigma P-B^*E^{-1}B, producing a direct promotion/falsification inequality.

Blocking gap: Kappa4 endpoint-box lower-bound gap: no rigorous same-regulator lower bound is yet available for v^*(R_{kappa,sigma}+E^{OPE}_sigma)v uniformly on the Schur kernel and through the sigma-to-zero limit.

## Falsifiers

- falsifier: a heat-kernel plaquette cumulant calculation finding v^*kappa_sigma v<-2\sum_{ijab}\bar v_i v_j C_{ij}^{ab}C_{ij}^{ab} by more than the Schur margin makes the endpoint form negative.
- If endpoint boxes overlap at regulator scale, contact terms can invalidate the claimed perimeter cancellation and the R decomposition must be quarantined.
- If R_G has a null vector on P while S_sigma is positive on that vector, the corrected second-order form fails independently of kappa_4.
- If the kappa_4 estimate is obtained from a different regulator or normalization than H,K, the same-theory condition is violated and the comparison is not valid.

## Learning

The branch is not looping on OS density. The contribution-making object is now the concrete heat-kernel Wilson cumulant R: vacuum/perimeter cancellation leaves crossed curvature contractions plus kappa_4. The crossed part is a positive Hilbert-Schmidt square with explicit color factor, so every possible obstruction is localized to kappa_4, the OPE remainder, or the Schur hairpin energy.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute kappa_{ij,sigma} for the first disjoint plaquette endpoint-box pair using covariant heat-kernel point splitting: evaluate the connected four-plaquette curvature cumulant, subtract the two crossed Gaussian contractions explicitly, and compare the resulting Rayleigh quotient against S_sigma=B^*E^{-1}B.
