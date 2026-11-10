# cycle-0289

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Endpoint-source coarsening for post-HK reflected Wilson gate

## Candidate Lemma

Finite endpoint dominance interval theorem: after the H,K Schur-Feshbach reduction for the fixed reflected three-hairpin block, the dangerous connected boundary-OPE polarization is enclosed by a same-theory endpoint-source interval; only clipped positive 12-dominance can lower the null-channel scalar.

## Definitions

- source object: heat-kernel plaquette-sheet regulated SU(N) Wilson endpoint boxes v for the fixed reflected three-hairpin collar block, with local source partition functions Z_v(s).
- target object: the finite post-H,K null-channel Schur-Feshbach scalar for the same three Wilson hairpins in the regulated OS matrix.
- controlled interface: C_ep=(V,Z_v,b_ij,C_N,M_G,T_tail) records endpoint source derivatives, fractional incidences, color factor, Gaussian margin, and residual tail.
- same-theory condition: all Z_v(s) are generated inside the original heat-kernel lattice Yang-Mills measure by Wilson plaquette-sheet sources, with no boundary counterterm, no changed observable algebra, and cutoff-uniform identifications.
- bridge observable: kappa_v=f_v^{(4)}(0) is the singlet connected four-flux endpoint cumulant, with f_v(s)=log Z_v(sL_v).
- hard gate: the finite post-H,K reflected-Wilson OS transfer gate, not the continuum OS/Wightman or mass-gap gate.

## Assumptions

- Model: four-dimensional Euclidean SU(N) lattice Yang-Mills with heat-kernel plaquette action and a fixed reflection plane.
- Regime: fixed finite three-hairpin collar geometry after the previously computed H,K reduction, with endpoint boxes smaller than the collar scale and larger than the lattice spacing.
- Cutoff: beta_v and T_tail intervals are uniform in the cutoff along the regulator-removal subsequence being tested.
- Same-theory: source insertion L_v changes only the Wilson plaquette-sheet observable inside the original measure and does not add a boundary action.
- Validity: Wick-square disconnected contractions are removed by the connected log derivative, and straight C_A f f contacts cancel by the null-incidence identity.
- Local: all non-endpoint connected remnants and corner leakage are charged to the declared T_tail interval.

## Equations

- endpoint cumulant source: `f_v(s)=\log Z_v(sL_v),\qquad \kappa_v=f_v^{(4)}(0)`. Valid when: Valid when the heat-kernel endpoint box source is analytic for the finite regulator and the fourth derivative is taken before cutoff removal.
- null incidence dominance: `D_v=2b_{12}(v)-4b_{13}(v)-4b_{23}(v),\qquad b_{13}(v)+b_{23}(v)\ge b_{12}(v)/2\Rightarrow D_v\le0`. Valid when: Valid for fractional endpoint incidences measured in the same reflected three-hairpin null channel after H,K normalization.
- post-HK scalar carrier: `I_{\mathrm{gate}}=M_G+C_N\sum_{v\in V}\kappa_vD_v+T_{\mathrm{tail}}`. Valid when: Applies after Wick-square positivity, straight f f cancellation, and allocation of all non-endpoint connected remnants to T_tail.
- clipped interval enclosure: `I_- = M_G+\tau_- - C_N\sum_v \beta_v^+ [d_v^+]_+,\quad I_+=M_G+\tau_+ +C_N\sum_v\beta_v^+[-d_v^-]_+-C_N\sum_v\beta_v^+[d_v^-]_+`. Valid when: Valid when kappa_v lies in [-beta_v^+,-beta_v^-], D_v lies in [d_v^-,d_v^+], C_N is positive, and T_tail lies in [tau_-,tau_+].

## Attempted Derivation

- Freeze the Clay claim level: this cycle targets only a finite regulated post-H,K Wilson block and makes no continuum, nontriviality, OS-density, or mass-gap claim.
- Start from the heat-kernel plaquette-sheet regulator and write each endpoint contribution as f_v^{(4)}(0) for the singlet source L_v; connected logs remove Wick-square disconnected pieces.
- Use the previously valid cancellations: the Wick-square part is a positive Gram term and the straight nonabelian C_A f f contact cancels under the three-hairpin null incidence.
- Contract the remaining connected endpoint cumulant with the null-channel weights, giving D_v=2b12-4b13-4b23 and the scalar carrier I_gate=M_G+C_N sum kappa_v D_v+T_tail.
- Insert signed intervals kappa_v in [-beta_v^+,-beta_v^-] and incidence intervals D_v in [d_v^-,d_v^+] to get a conservative lower interval controlled only by [d_v^+]_+.
- Repair the carrier fragmentation: if endpoint cells have identical regulated source data, sum D over the source-equivalence class before clipping because [sum D]_+ is never larger than sum [D_v]_+.

Blocking gap: The proof still needs actual same-theory source intervals beta_v, a cutoff-uniform M8_v bound, and a local T_tail bound for cross-box connected cumulants; without these, the interval theorem is valid but unpopulated.

## Falsifiers

- A same-theory endpoint source certificate yields I_+<0 after all valid coarsenings, giving a finite reflected-Wilson OS falsifier for this block.
- The eighth-derivative bound M8_v grows with the cutoff, so the source interval is not valid for the regulator/RG passage.
- A required endpoint boundary counterterm or changed Wilson normalization violates the same-theory condition.
- Cross-box connected four-flux cumulants exceed T_tail, making the coarsened carrier falsely local.
- All half-overlap shields fail in a 12-dominant endpoint class and the certified negative kappa mass exceeds M_G plus tail.

## Learning

Conceptual pressure attacked: endpoint collapse must be sign-certified in the same Wilson theory after H,K. Declarative tension: finite collar OS positivity, fixed gauge-invariant Wilson observables, and a singular connected endpoint boundary OPE must jointly hold without a boundary theory; raw R is representation-limited because it hides incidence signs, while a raw kappa_4 spectrum is too strong because negative kappa_4 is harmless when D<=0. Compared with the global Schur-preimage route, C_ep is local after H,K and decision-grade for this finite gate; compared with formal OPE language, it has primitive operations: source differentiation, interval arithmetic, source-equivalence coarsening, color multiplication, incidence contraction, clipping, and tail addition. Efficient representation requirements: encode endpoint boxes/classes, seven source values, beta intervals, fractional b_ij incidences, C_N, M_G, and T_tail; preserve Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; identify equivalent carriers only by equal regulated source data; keep locality cost finite through T_tail; transfer only [I_-,I_+] to the finite OS gate; demote on negative interval, nonuniform tail, or boundary counterterm. Hard gate changed: the finite post-H,K reflected-Wilson OS transfer gate can now be promoted or falsified by source-equivalent endpoint data. Conceptual value signal: sharpness and route change at finite scope, because the obstruction is certified 12-dominance after valid coarsening plus uncontrolled tail, not negative endpoint kappa_4 itself. Clay continuum construction, full OS/Wightman reconstruction, nontriviality, and mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch has reduced the post-H,K R term to endpoint incidence and source intervals; a concrete thought experiment tests whether the new coarsening carrier prevents false demotion or exposes a real finite falsifier.
- Situation seed: Heat-kernel SU(N) lattice Yang-Mills on a fixed reflected three-hairpin plaquette-sheet block with endpoint cells near one reflection-plane corner; adjacent cells have source-equivalent compact-group kappa_4 data but different fractional overlaps b12,b13,b23.
- Varied variable: source-equivalence coarsening radius r, equivalently the fraction alpha=(b13+b23)/b12 surviving after aggregation.
- Held-fixed controls: Same Wilson hairpin geometry and the previously computed H,K null vector are held fixed., The heat-kernel plaquette action, reflection plane, Wilson normalization, color factor C_N, and Gaussian margin M_G are held fixed., No boundary counterterm, gauge fixing change, or observable-algebra enlargement is allowed., All cross-cell nonlocal remnants are charged to the same declared T_tail budget.
- Expected observation: For alpha>=1/2 the aggregate D_E is nonpositive and negative kappa_4 is protective; for alpha<1/2 the dangerous interval decreases linearly with 2b12-4b13-4b23 and can become a valid finite falsifier if it exceeds M_G plus tail.
- Transfer certificate needed: A source-equivalence certificate from seven regulated log Z values, a cutoff-uniform M8 bound, and a T_tail estimate showing that coarsening is only bookkeeping inside the same heat-kernel Yang-Mills theory.

## Next Experiment

Populate one source-equivalence class table for the heat-kernel three-hairpin endpoint: compute seven log Z_v source values, certify beta_v and M8_v, aggregate D_E before clipping, and report the interval sign of I_gate with a cutoff-uniform T_tail bound.

# Ward-Hessian endpoint certificate for the flowed Wilson R_{++} term

## Candidate Lemma

Conditional finite Route A theorem: for the concrete H,K endpoint plus channel, a Ward-subtracted flowed Wilson cumulant gives a certified lower interval for R_{++}^{ren}; if this interval beats the Schur-Feshbach leakage L_+, endpoint-box positivity is promoted, while failure quarantines only this finite repair.

## Definitions

- source object: finite-cutoff SU(N) Wilson lattice Yang-Mills measure with gradient-flowed gauge field B_t and two reflected endpoint hairpin sheet currents q_+^1,q_+^2.
- target object: finite Route A H,K endpoint-box Schur-Feshbach positivity inequality R_{++}^{ren}>L_+ for the plus channel.
- controlled interface: centered renormalized flowed Wilson hairpin covariance decomposed into positive pair contraction plus Ward-subtracted connected four-curvature polarization.
- same-theory condition: all observables, counterterms, flow time, coupling, reflection, and limiting intervals come from the same Wilson regulator family before any OS or spectral transfer.
- carrier: endpoint sheet currents with cell moments, not raw Wilson contours; zero-pairing current equivalence is allowed only after a certified heat-kernel pairing check.
- hard gate changed: finite endpoint-box positivity after H,K; continuum existence, OS/Wightman reconstruction, observable density, nontriviality, and Hamiltonian mass gap remain untouched.

## Assumptions

- Model: SU(N), N>=2, Wilson plaquette action on a finite reflected lattice box, with Lüscher gradient flow time t>0 and lattice spacing a.
- Regime: endpoint cell diameter eta and split radius rho satisfy a << eta <= rho/8 <= sqrt(8t)/32, and the endpoint boxes stay inside the H,K collar geometry.
- Cutoff: heat-kernel derivative bounds, cusp/perimeter counterterms, and fourth-order Wilson expansion remainders are enclosed uniformly for a<a0(t,eta,rho) and finite volume L>=L0.
- Same-theory: the H,K Feshbach matrix, the flowed Wilson hairpins, and all renormalization factors are evaluated in the same regulated Yang-Mills measure.
- Validity: Ward/cusp subtraction kills the one-hairpin perimeter and endpoint contact terms before the connected four-curvature kernel is interval-bounded.
- Local: the claim is a finite endpoint-box certificate, not a continuum construction, not OS spectral transfer, and not the Clay mass gap theorem.

## Equations

- centered-renormalized-hairpin: `\widehat W_t(q)=Z_{\rm cusp}^{-1}Z_{\rm per}^{-1}\left({\rm Tr}\,P\exp\left(i\oint_{\partial q} B_t\right)-\left\langle {\rm Tr}\,P\exp\left(i\oint_{\partial q} B_t\right)\right\rangle\right)`. Valid when: Applies when the flowed Wilson hairpin is defined at fixed positive flow time and the same cusp and perimeter counterterms are used for both endpoint cells.
- endpoint-cumulant-carrier: `R_{++}^{I,{\rm ren}}(t,a)=\kappa_2\left(\widehat W_t(q_+^1),\widehat W_t(q_+^2)\right)`. Valid when: Valid when q_+^1 and q_+^2 are the reflected plus-channel endpoint sheet currents in the same finite H,K collar instance.
- pair-plus-connected-decomposition: `R_{++}^{I,{\rm ren}}=g_t^4\left(2(N^2-1)G_{++}^{I}+N(N^2-1)C_{4,++}^{I,{\rm WS}}\right)+E_6^{I}`. Valid when: Requires the fourth-order flowed Wilson expansion after disconnected-product removal, one-hairpin subtraction, and Ward-subtracted connected four-curvature sector grouping.
- plus-moment-cancellation: `m_0(q_+)=\int q_+(u)\,du=0,\qquad m_1(q_+)=\int (u-c)q_+(u)\,du=0,\qquad M_{2,+}\le C_H\eta^2\|q_+\|_1`. Valid when: Valid when the H,K plus-channel endpoint current is represented by oriented sheets and Ward plus cusp cancellations have been checked cellwise.
- Ward-Hessian-polarization-bound: `\left|C_{4,++}^{I,{\rm WS}}\right|\le M_{2,+}(q_+^1)M_{2,+}(q_+^2)\left(H_{\rm near}^{I,+}(t,\rho)+H_{\rm far}^{I,+}(t,\rho)+H_{\rm ct}^{I,+}(t)\right)+T_{\rm tail}^{I,+}`. Valid when: Applies after mixed second-derivative interval envelopes for every Ward-subtracted four-curvature sector are certified on the near and far endpoint cells.
- promotion-inequality: `R_{++}^{I,-}:=g_t^4(N^2-1)\left(2G_{++}^{I,-}-N M_{2,+}^2 H_{4}^{I,+}\right)-E_6^{I,+}-T_{\rm tail}^{I,+},\qquad R_{++}^{I,-}>L_++\sigma`. Valid when: Valid when G_{++}^{I,-}, H_4^{I,+}, E_6^{I,+}, T_tail^{I,+}, and L_+ are outward-rounded intervals for the same H,K Feshbach instance.

## Attempted Derivation

- Conceptual pressure attacked: finite Schur-Feshbach positivity needs a same-theory Wilson mediator; positive pair covariance and gradient flow are valid inputs but the connected four-curvature polarization can erase them.
- Represent q_+ as an oriented endpoint sheet current in the concrete H,K plus channel and center the flowed Wilson hairpins after disconnected, perimeter, and cusp subtraction.
- Expand the centered flowed Wilson hairpin covariance to fourth curvature order. The cross-pairing contraction is positive and gives the explicit color factor 2(N^2-1)G_{++}.
- Group the remaining connected one-loop four-curvature terms into Ward-subtracted sectors K_{3g}, K_{4g}, K_ct, and K_end with color factor N(N^2-1).
- Use Ward identities plus plus-channel endpoint orientation to get m0(q_+)=m1(q_+)=0, so the first nonzero contribution of K_4^{WS} is controlled by mixed Hessians and second moments.
- Split endpoint cells into near and far regions. Near constants are finite interval quadratures; far constants use flowed heat-kernel derivative majorants with exponential flow tails.
- Combine the bound on C_{4,++}^{WS} with the positive pair interval and the existing Schur-Feshbach leakage L_+ to obtain the promotion inequality R_{++}^{I,-}>L_++sigma.

Blocking gap: The actual near-cell interval quadrature and the far heat-kernel constants A_s(N),B_s(N) have not yet been certified for the concrete H,K geometry and a stable t,eta,rho window.

## Falsifiers

- falsifier: Ward/cusp subtraction leaves a nonzero monopole or dipole moment, destroying the eta^2 Hessian suppression.
- falsifier: the connected four-curvature interval satisfies N M_{2,+}^2 H_4^{I,+} >= 2G_{++}^{I,-}-L_+/(g_t^4(N^2-1)) across every stable flow window.
- falsifier: the sixth-order Wilson remainder E_6^{I,+} is comparable to or larger than the positive pair baseline.
- falsifier: the lower interval depends on the gauge-fixing used to compute K_s after sector summation.
- falsifier: changing a, volume, or flow time within the finite regulator window destroys the sign plateau, indicating no same-theory certificate.
- falsifier: zero-pairing quotienting merges endpoint currents whose Hessian bounds lead to different promotion decisions.

## Learning

Conceptual pressure attacked: the missing mediator between finite Schur-Feshbach positivity and same-theory Wilson cumulant positivity. Declarative tension: pair covariance, gradient-flow renormalization, and finite endpoint positivity must jointly hold, but C4 can erase the pair term unless a cutoff-stable Ward-Hessian interval is valid. Carrier critique: raw Wilson contours are fragmented and representation-limited; global OS or non-Gaussian witness routes are too coarse for this local obstruction. Efficient representation: encode H,K sheets, endpoint currents, cell moments, sector kernels, and counterterms; preserve gauge, color, reflection, orientation, cutoff, and same-theory invariants; use cumulant expansion, Ward/cusp subtraction, endpoint Taylor expansion, heat-kernel majorants, interval arithmetic, and zero-pairing quotienting as primitives; keep locality to endpoint cells; transfer only through flowed Wilson cumulants; demote on any falsifier. Hard gate: finite endpoint-box positivity after H,K. Conceptual value signal: R_{++}/kappa_4 is now a route-deciding finite color-geometric interval certificate, not a symbolic endpoint term, while Clay commitments remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and proof-search guide.`
- Rationale: The branch has already reduced R_{++} to a flowed Wilson cumulant; another abstract OS restatement would not decide whether C4 erases the positive pair term.
- Situation seed: Finite SU(3) Wilson lattice on a reflected box with gradient flow t, the concrete H,K plus-channel endpoint hairpin sheets, Ward/cusp subtraction, and outward-rounded interval evaluation of G_{++}, H_4, E_6, and L_+.
- Varied variable: theta=eta/sqrt(8t), the endpoint-cell diameter measured in flow units.
- Held-fixed controls: same Wilson plaquette action, coupling window, reflection plane, and gradient-flow definition, same H,K collar/hairpin geometry and same Schur-Feshbach leakage L_+, same endpoint-current orientation, color normalization, Ward/cusp subtraction, and zero-pairing quotient policy, finite endpoint-box claim only; no continuum or spectral transfer inference
- Expected observation: As theta decreases inside a computable window, the pair interval should remain positive while the Ward-Hessian C4 bound falls like a second-moment term; a stable positive R_{++}^{I,-}-L_+ would promote the finite endpoint gate, and persistent negativity would demote the repair.
- Transfer certificate needed: Before intuition affects proof obligations, require same-theory interval certificates for Ward/cusp cancellation, near/far Hessian constants, sixth-order remainders, cutoff/volume/flow sign plateaus, and equality of the Wilson cumulant carrier with the H,K Feshbach instance.

## Next Experiment

Implement the proof-search worksheet for the concrete H,K endpoint boxes: compute the positive pair interval G_{++}^{I,-}, certify m0=m1=0, enclose K_{3g}, K_{4g}, K_ct, K_end Hessians with near/far split, then test R_{++}^{I,-}>L_+ across theta=eta/sqrt(8t) windows.

# Raw plaquette interval gate for the post-H,K boundary polarization

## Candidate Lemma

Raw plaquette interval enclosures for the connected four-curvature Wilson cumulant give a valid finite Schur-corrected endpoint-box certificate: if Delta_raw(sigma)>0, the worked H,K endpoint quadratic form is positive; if Delta_raw(sigma)<=0 after sharp intervals, this collar/hairpin Route A instance is demoted.

## Definitions

- source object: finite-volume SU(N) heat-kernel lattice gauge theory on Lambda(a,L), with fixed endpoint Wilson sheet family Sigma_i, transported plaquette logarithms X_p in a heat-kernel small-field chart, and a separately bounded large-field remainder.
- target object: the finite Schur-corrected endpoint quadratic form Q_sigma=R_sigma-S_HK on the H,K Wilson endpoint span E_HK,sigma; positivity here is only a Route A local gate, not OS reconstruction or a mass gap.
- controlled interface: raw plaquette interval aggregation maps every connected plaquette-quartet cumulant kappa_pqrs and OPE/log remainder into a verified lower bound Delta_raw(sigma) for Q_sigma.
- same-theory condition: C_sigma, K4_sigma, OPE errors, large-field errors, and S_HK are computed with the same cutoff measure, heat-kernel regulator, coupling normalization, Wilson basis, reflection support, and endpoint compression.
- bridge/carrier: the carrier is the raw plaquette-quartet interval matrix I K4_sigma, not the earlier symbolic A012 shell abstraction.
- observable manipulated: Phi_i,sigma is the transported smeared curvature flux attached to endpoint sheet Sigma_i, and R_ij,sigma is cum_2(:Phi_i^2:,:Phi_j^2:).

## Assumptions

- Model: finite hypercubic four-dimensional lattice gauge theory with compact group SU(N), heat-kernel plaquette action, finite volume, and fixed boundary endpoint box.
- Cutoff: a>0 and sigma/a are fixed; no continuum, infinite-volume, or RG-uniform claim is made in this lemma.
- Same-theory: the H,K Schur matrix S_HK is evaluated in the identical Wilson observable basis and cutoff Gibbs measure as the cumulants defining R_sigma.
- Regime: the plaquette-log Wilson/OPE expansion is used only on the heat-kernel small-field chart; the complement contributes an explicit positive error budget e_LF.
- Validity: every plaquette-quartet orbit interval must enclose the actual connected cumulant with outward-rounded interval arithmetic and no non-invariant quotienting.
- Local: all sheet supports and reflected partners lie inside the finite endpoint box used for the H,K calculation.

## Equations

- endpoint-polarization-cumulant: `\mathcal R_{ij,\sigma}=\operatorname{cum}_2\!\left(:\Phi_{i,\sigma}^a\Phi_{i,\sigma}^a:,:\Phi_{j,\sigma}^b\Phi_{j,\sigma}^b:\right)`. Valid when: Valid when Phi_i,sigma are transported plaquette-flux sums in one finite heat-kernel lattice measure and normal ordering uses that same measure.
- raw-kappa4-contraction: `K^{(4)}_{ij,\sigma}=\sum_{p,q\in\Sigma_i}\sum_{r,s\in\Sigma_j} W_i^{ab}(p,q)W_j^{cd}(r,s)\,\kappa^{abcd}_{pqrs}`. Valid when: Valid when the Wilson sheet expansion is truncated after four transported curvatures and all plaquette quadruples lie in the endpoint box.
- Gaussian-plus-connected-decomposition: `\mathcal R_\sigma=\alpha_N g_R^4(C_\sigma\circ C_\sigma)+\frac{g_R^4}{16N^2}K^{(4)}_\sigma+E_{\mathrm{OPE}}+E_{\mathrm{LF}}`. Valid when: Valid when disconnected cumulants are cancelled by same-measure normal ordering and the log-chart large-field contribution is enclosed separately.
- raw-interval-endpoint-margin: `\Delta_{\mathrm{raw}}(\sigma)=\lambda_{\min}^{\mathrm{Gersh}}\!\left(\alpha_N g_R^4(C_\sigma\circ C_\sigma)+\frac{g_R^4}{16N^2}\mathbb I K^{(4)}_\sigma-S_{HK}\right)-e_{\mathrm{OPE}}-e_{\mathrm{LF}}`. Valid when: Applies after interval inclusion for every plaquette-quartet orbit and after the H,K Schur matrix is computed in the identical basis.
- finite-certificate-implication: `\Delta_{\mathrm{raw}}(\sigma)>0\Longrightarrow R_\sigma-S_{HK}\succeq0\quad\text{on }E_{HK,\sigma}`. Valid when: Valid when the interval Gershgorin lower bound is rigorous and the endpoint compression space is exactly the H,K Wilson space.

## Attempted Derivation

- Conceptual pressure attacked: the branch had quarantined symbolic A012; the missing mediator is now a raw same-regulator route from actual Wilson plaquette cumulants to Schur-corrected endpoint positivity.
- Freeze the Clay target boundary: this cycle targets only finite endpoint-box positivity for one H,K Wilson geometry; OS/Wightman axioms, continuum existence, observable density, and physical-unit mass gap remain untouched.
- Choose regulator: finite SU(N) heat-kernel lattice action, plaquette-log small-field chart at smoothing scale sigma, and explicit large-field complement e_LF.
- Define transported endpoint fluxes Phi_i,sigma from plaquette logarithms and express R_ij,sigma as cum_2(:Phi_i^2:,:Phi_j^2:) in the same Gibbs measure.
- Use the finite cumulant identity to decompose R_sigma into the PSD Gaussian color square alpha_N g_R^4(C_sigma o C_sigma), the connected four-curvature contraction K4_sigma, and OPE/log remainders.
- Replace shell amplitudes by raw plaquette-quartet intervals: enumerate orbits only if transporter, color, orientation, and multiplicity inclusion are valid; otherwise use the unquotiented list.
- Insert the interval matrix into the Schur-Feshbach endpoint form and compute Delta_raw(sigma) by a verified Gershgorin or stronger interval eigenvalue lower bound.
- Hard gate: Delta_raw(sigma)>0 promotes a finite Route A endpoint positivity certificate; Delta_raw(sigma)<=0 with sharp intervals is a route falsifier for this H,K geometry.

Blocking gap: The actual same-regulator intervals for the connected plaquette-quartet cumulants kappa_nu, the large-field tail e_LF, and the explicit H,K Schur matrix have not yet been enumerated or numerically certified.

## Falsifiers

- falsifier: verified raw plaquette intervals give Delta_raw(sigma)<=0 after tight OPE and large-field errors, killing this H,K endpoint-box positivity route.
- A non-invariant plaquette-orbit quotient misses a transporter or orientation sign, so the compressed K4 interval is not valid.
- The heat-kernel large-field complement e_LF is comparable to or larger than the Gaussian square margin, making the small-field Wilson/OPE certificate useless.
- The Schur hairpin energy S_HK computed in the same basis exceeds the positive Gaussian color square plus every admissible kappa4 lower bound.
- The Wilson perimeter/vacuum cancellation is regulator-mismatched, so disconnected terms re-enter R_sigma.
- Interval widths remain nonuniform as sigma/a varies, indicating that the local finite certificate cannot be promoted even as restricted evidence.

## Learning

The branch has moved from symbolic R and quarantined A012 shells to a falsifier-ready raw plaquette interval theorem: the only admissible promotion is Delta_raw(sigma)>0 in the same cutoff theory, while failure cleanly demotes the finite H,K endpoint route without touching the Clay-level gates.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The branch has already quarantined symbolic shell amplitudes; a concrete raw plaquette experiment is needed to see whether kappa4 or large-field errors can realistically dominate the positive Gaussian color square before any proof-search promotion.
- Situation seed: Finite SU(2) heat-kernel lattice gauge theory on a 4D endpoint box containing the worked H,K collar/hairpin Wilson sheets; enumerate all plaquette quadruples contributing to K4_sigma in the first reflected boundary layers and enclose their connected cumulants by character-expansion or certified Monte Carlo interval surrogates.
- Varied variable: rho=sigma/a, the heat-kernel smoothing radius in lattice units.
- Held-fixed controls: Same finite endpoint box, same H,K Wilson sheet geometry, and same reflected endpoint compression E_HK,sigma., Same heat-kernel regulator, coupling normalization g_R, plaquette-log chart, and same Gibbs expectation for normal ordering., Same Schur-Feshbach subtraction S_HK and same OPE/large-field error accounting., No continuum, infinite-volume, or OS spectral-transfer inference is allowed from the observation alone.
- Expected observation: A positive window for Delta_raw(rho) would identify a plausible finite endpoint certificate; a consistently nonpositive or error-dominated window is a sharp falsifier for this collar/hairpin Route A geometry.
- Transfer certificate needed: Before intuition affects proof obligations, every plaquette-quartet interval, orbit multiplicity, color factor, large-field tail, OPE error, and S_HK entry must be same-regulator and outward-rounded, with an independently checked interval eigenvalue lower bound.

## Next Experiment

Build the first unquotiented endpoint-box plaquette-quartet table for SU(2) heat-kernel regulator at fixed rho, compute color/geometry weights W_iW_j, attach provisional rigorous intervals for kappa_nu, then evaluate Delta_raw with S_HK and explicit e_OPE,e_LF.

