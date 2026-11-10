# cycle-0239

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Cycle 239: endpoint-localized κ4 test for the Wilson hairpin R term

## Candidate Lemma

For the first regulated three-hairpin Wilson block with heat-kernel plaquette sheets, the dangerous second-order boundary-OPE polarization is not a free symbolic R. After diagonal normalization, the null-channel contribution is an explicit connected four-flux cumulant pairing plus endpoint tails; the Wick-square term is nonnegative and the bulk nonabelian ff contact cancels in the actual null geometry. Thus the branch is promoted by a uniform lower bound on this κ4-plus-endpoint term and demoted by a negative bound exceeding the Schur margin.

## Definitions

- source object: heat-kernel-regulated SU(N) lattice Yang-Mills Schwinger forms for mirror-smoothed reflected Wilson hairpin collar sheets at spacing a and smearing radius r.
- target object: the diagonal-normalized continuum OS quotient block for the same three reflected Wilson hairpins and its corrected second-order Schur-Feshbach gate.
- controlled interface: the boundary-OPE coefficient R_ij extracted from the logarithm of the reflected Wilson cumulant after Gaussian Wick-square, one-body, and bulk commutator pieces are separated.
- same-theory condition: the same locked Wilson loop observables are obtained as a,r and collar width go to zero, without adding boundary counterterms or changing Wilson-loop normalization.
- Use generators T^a with tr(T^aT^b)=T_F delta^{ab}; C_F=T_F(N^2-1)/N and f^{ace}f^{bce}=C_A delta^{ab}.
- Let beta_i be the smeared pair-source obtained by inserting two boundary plaquette fluxes on the i-th hairpin sheet, with parallel transport to a common base point.
- Let v=(1,1,-2) denote the null vector of the first-order reduced hairpin form, and let R_v=sum_{i<j}2 v_i v_j R_ij be the connected null-channel polarization.

## Assumptions

- Heat-kernel lattice Yang-Mills is reflection positive before removal of the regulator, and the Wilson loops are represented by mirror-smoothed plaquette sheets.
- The regulated cumulant expansion of the diagonal-normalized reflected Wilson quotient is valid through four boundary flux insertions with an o(delta^2) remainder uniform on the fixed hairpin block.
- The prior Schur-Feshbach computation is used only as a gate: PHP is nonnegative with null vector v, so the next possible falsifier is the connected R_v coefficient.
- Bulk straight-segment footprints of the three hairpins have the previously fixed incidence pattern; this is the cancellation used for the local ff commutator contact.
- The smeared irreducible four-flux cumulant has a finite operator norm K_4(a,r) on the endpoint pair-source space, and endpoint/corner tails are collected in T_v^end(a,r).

## Equations

- regulated connected R: `R_{ij}^{\kappa_4}(a,r)=\frac{g_a^4}{8N^2}\operatorname{tr}(T^aT^b)\operatorname{tr}(T^cT^d)\int \beta_i^{\mu\nu,\rho\sigma}(x,y)\,\beta_j^{\alpha\beta,\gamma\delta}(z,w)\,\kappa^{abcd}_{4,a,r;\mu\nu\rho\sigma\alpha\beta\gamma\delta}(x,y,z,w)`. Valid when: Valid when heat-kernel plaquette sheets are mirror-smoothed at scale r and diagonal Wilson factors have already been divided out.
- color reduction: `\operatorname{tr}(T^aT^b)=T_F\delta^{ab},\qquad f^{ace}f^{bce}=C_A\delta^{ab},\qquad C_F=T_F\frac{N^2-1}{N}`. Valid when: Applies when the Wilson loops are in the fundamental representation of SU(N) with a fixed generator normalization.
- boundary polarization decomposition: `R_{ij}=R_{ij}^{\square}+R_{ij}^{\kappa_4}+R_{ij}^{ff,bulk}+R_{ij}^{end}+o_{a,r}(1),\qquad R_{ij}^{\square}=\frac{g_a^4C_F^2}{2}\langle \beta_i,\mathcal G_r^{\otimes2}\beta_j\rangle`. Valid when: Valid when the cumulant expansion is truncated after four boundary flux insertions with a uniform collar-OPE remainder.
- null cancellation and endpoint bound: `\sum_{i<j}2v_iv_jR_{ij}^{ff,bulk}=0,\quad \sum_{i<j}2v_iv_jR_{ij}^{\square}\ge0,\quad |R_v^{\kappa_4+end}|\le \frac{g_a^4T_F^2}{8N^2}\mathfrak K_4(a,r)\mathfrak B_v(r)^2+|T_v^{end}(a,r)|`. Valid when: Requires the same three hairpin footprints, their null vector v=(1,1,-2), and heat-kernel smearing before endpoint boxes are shrunk.
- promotion sign test: `R_v\ge -8m^2+\eta\quad\Leftarrow\quad \frac{g_a^4T_F^2}{8N^2}\mathfrak K_4(a,r)\mathfrak B_v(r)^2+|T_v^{end}(a,r)|\le 8m^2-\eta`. Valid when: Valid when the previously computed positive Schur margin is retained and no extra boundary counterterm changes the Wilson algebra.

## Attempted Derivation

- Represent each reflected hairpin Wilson loop by a mirror-smoothed plaquette sheet and expand the diagonal-normalized quotient in boundary flux insertions.
- Pair two flux insertions on each Wilson trace. The disconnected pairings give the Wick-square term with color factor C_F^2; this is a Gram contribution and cannot create the negative second-order falsifier.
- Separate BCH commutator contacts. The local bulk term carries f^{ace}f^{bce}=C_A delta^{ab}; on each straight shared boundary segment the signed null incidence from v=(1,1,-2) cancels, leaving only endpoint/corner neighborhoods of size r.
- The remaining irreducible Yang-Mills input is the connected four-flux cumulant kappa_4 contracted with beta_i and beta_j. This defines R_ij rather than treating it as a symbolic parameter.
- Polarize with the null vector v. The dangerous contribution is bounded by the smeared kappa_4 operator norm times the endpoint pair-source norm, plus the endpoint commutator tail T_v^end.
- Therefore the first calculable promotion test is K_4(a,r) B_v(r)^2 g_a^4 T_F^2/(8N^2)+|T_v^end| below the Schur margin; the first demotion test is a stable negative lower estimate beyond that margin.

Blocking gap: No rigorous nonperturbative bound is yet available for the smeared irreducible boundary four-flux cumulant K_4(a,r), and the endpoint/corner tail has not been computed uniformly as a,r go to zero.

## Falsifiers

- A direct heat-kernel plaquette cumulant computation finds a negative irreducible endpoint kappa_4 contribution whose magnitude exceeds the positive Schur margin.
- Parallel transport around endpoint boxes produces a residual holonomy contact, so the claimed ff bulk cancellation is spoiled by a nonlocal corner term.
- The endpoint tail T_v^end diverges logarithmically as r goes to zero and cannot be absorbed by diagonal Wilson normalization without changing the theory.
- The topology controlling cutoff removal is not strong enough to pass the regulated four-flux boundary cumulant to a valid continuum distribution.
- A positive Wick-square Gram term is accidentally subtracted by an inconsistent normalization; this would be an artificial falsifier rather than a Yang-Mills obstruction.

## Learning

The branch made a concrete R-step: in heat-kernel regulation the null-channel polarization is endpoint-localized after two cancellations. The Wick-square contraction is a positive Gram term, and the straight-segment nonabelian ff contact cancels in the actual hairpin null geometry. The only substantive remaining falsifier is the regulated irreducible kappa_4 boundary cumulant plus endpoint tails, with a valid norm bound giving the first promotion/demotion test.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute the leading endpoint-box contribution to kappa_4 using the heat-kernel character expansion: enumerate minimal connected plaquette polymers touching the four flux insertions, evaluate the SU(N) group integrals with T_F and C_A factors, and insert the signed hairpin endpoint incidence to decide the sign of T_v^end+R_v^{kappa_4}.

# Gauge-invariant Wilson hairpin R-kernel extraction

## Candidate Lemma

For two separated renormalized thin Wilson hairpins in the same SU(N) Yang-Mills Schwinger family, the normalized boundary-OPE polarization R_{ij}^{ren} splits into a positive two-curvature cross-pairing with color factor 2(N^2-1) and a single connected four-curvature remainder C_4^{ren}. The branch is not looping: the concrete unknown is now the sign and size of C_4^{ren}.

## Definitions

- source object: a continuum SU(N) Euclidean Yang-Mills Schwinger family with gradient-flowed curvature F_tau and renormalized thin Wilson hairpins C_i(ell,epsilon) based at boundary points x_i.
- target object: the finite H,K collar coefficient R_{ij}^{ren} that enters the Schur-Feshbach corrected second-order form for the plus hairpin channel.
- controlled interface: the boundary OPE sends centered hairpin variables to area-bivector contractions of :F_tau F_tau: plus an error controlled by ell_i/d_ij and tau/d_ij^2.
- same-theory condition: the same flowed Schwinger functions, Wilson renormalization, centering, and cutoff-removal path define both R_{ij}^{ren} and the OS reconstructed theory.
- Regulator: gradient flow time tau>0, boundary point-splitting epsilon>0, then ell/d -> 0 before tau,epsilon are removed or matched.
- Color convention: tr(T^aT^b)=delta^{ab}/2 and U_tau(C)=P exp(i g_R integral_C B_tau).

## Assumptions

- The bases of the two hairpins are separated by d_ij>0 and lie in the same reflection collar.
- The flowed Wilson cumulants have a continuum limit after perimeter/cusp normalization and centering.
- The small-area non-Abelian Stokes expansion is uniform for ell_i,ell_j much smaller than d_ij and the collar radius.
- The disconnected product and one-hairpin self-contractions are subtracted before the boundary-OPE coefficient is read.
- The area bivectors hatOmega_i and hatOmega_j have nonzero projection onto the boundary-normal curvature channel.

## Equations

- centered-renormalized-hairpin: `H_i^{\tau,ren}=Z_i^{-1}\left(1-{1\over N}{\rm Tr}\,U_\tau(C_i)\right)-\left\langle Z_i^{-1}\left(1-{1\over N}{\rm Tr}\,U_\tau(C_i)\right)\right\rangle`. Valid when: Valid when the hairpin is built from flowed links at positive flow time and its perimeter and cusp normalization is fixed before centering.
- thin-hairpin-boundary-OPE: `H_i^{\tau,ren}={g_R^2\over 4N}\Omega_i^{\mu\nu}\Omega_i^{\rho\sigma}:F^a_{\mu\nu}F^a_{\rho\sigma}:(x_i^\epsilon,\tau)+E_i,\qquad \|E_i\|_2=O(\ell_i^5 d_i^{-5})+O(g_R^3\ell_i^6\|F_\tau^3\|_2)`. Valid when: Applies after diagonal normalization for thin hairpins whose size is much smaller than all separations and whose flowed basepoint remains inside the collar.
- normalized-polarization-coefficient: `R_{ij}^{ren}:=\lim_{\ell_i,\ell_j\downarrow0}(\ell_i^2\ell_j^2)^{-2}\,\kappa_2(H_i^{\tau,ren},H_j^{\tau,ren})`. Valid when: Requires separated boundary bases with d_ij positive so cross contractions stay finite after the local hairpin counterterms cancel.
- pair-plus-connected-decomposition: `R_{ij}^{ren}={g_R^4\over16N^2}\hat\Omega_i^{\mu\nu}\hat\Omega_i^{\rho\sigma}\hat\Omega_j^{\alpha\beta}\hat\Omega_j^{\gamma\delta}\left[(N^2-1)(G^\tau_{\mu\nu,\alpha\beta}G^\tau_{\rho\sigma,\gamma\delta}+G^\tau_{\mu\nu,\gamma\delta}G^\tau_{\rho\sigma,\alpha\beta})+C^{\tau,ren}_{4;\mu\nu\rho\sigma\alpha\beta\gamma\delta}\right]+O(\ell/d)`. Valid when: Valid when the continuum flowed curvature four-point function exists and the small-area expansion is uniform over the point-split boundary collar.
- explicit-positive-pair-term: `P_{ij}:={g_R^4(N^2-1)\over8N^2}\mathcal G_{ij}^{\tau},\qquad \mathcal G_{ij}^{\tau}:=(\hat\Omega_i^{\mu\nu}G^\tau_{\mu\nu,\alpha\beta}(z_{ij})\hat\Omega_j^{\alpha\beta})^2`. Valid when: Valid when the two area bivectors have nonzero mutual curvature projection; otherwise the leading positive pair term is geometrically killed.
- boundary-normal-leading-geometry: `\mathcal G_{ij}^{\tau}={\Theta_{ij}^2\over \pi^4 d_{ij}^8}+O(\tau d_{ij}^{-10})+O(\epsilon d_{ij}^{-9})`. Valid when: Valid when d_ij squared dominates the flow radius and the point-splitting scale in the boundary-normal hairpin geometry.
- connected-remainder-ratio: `\chi_{ij}:={\hat\Omega_i\hat\Omega_i\hat\Omega_j\hat\Omega_j\,C_4^{\tau,ren}\over 2(N^2-1)\mathcal G_{ij}^{\tau}},\qquad R_{ij}^{ren}=P_{ij}(1+\chi_{ij})+O(\ell/d)`. Valid when: Applies only in channels where the pair geometry is positive, so the dimensionless connected-polarization ratio is well defined.
- first-perturbative-sign-test: `|\chi_{ij}|\le c_N g_R^2(1/d_{ij})\left(1+|\log(d_{ij}^2/\tau)|\right)+O(\ell/d_{ij})`. Valid when: Valid as a perturbative ultraviolet sign test for asymptotically small separated hairpins, not as a nonperturbative infrared estimate.

## Attempted Derivation

- Use gradient-flowed holonomies and boundary point-splitting to make each hairpin observable finite before taking the small-area limit.
- Expand 1-N^{-1}Tr U_tau(C_i) through second order in the area bivector. The linear curvature term vanishes by tr T^a=0, leaving g_R^2 Omega_i Omega_i F^aF^a/(4N).
- Center the observable and divide by the one-hairpin renormalization. This cancels the disconnected expectation, the perimeter/cusp factor, and self-contractions internal to a single hairpin.
- Take kappa_2 of two hairpins. The four-curvature expectation decomposes into two cross Wick pairings plus the connected four-curvature cumulant C_4^{ren}.
- With tr(T^aT^b)=delta^{ab}/2, summing the two cross pairings gives the color factor 2(N^2-1) before Wilson normalization, hence P_ij=g_R^4(N^2-1)G_ij/(8N^2).
- For boundary-normal coplanar hairpins, the flowed free curvature kernel gives G_ij^2=Theta_ij^2/(pi^4 d_ij^8) up to tau/d^2 and epsilon/d corrections.
- Define chi=C_4^{ren}/(2(N^2-1)G). Promotion requires chi_{++} greater than the negative leakage margin in the Schur-Feshbach form; demotion occurs if chi_{++} is at or below -1 modulo errors.

Blocking gap: flowed connected four-curvature sign gap: no rigorous nonperturbative bound yet controls C_4^{ren} after the same perimeter/cusp subtraction.

## Falsifiers

- falsifier: C_4^{ren} is negative enough that chi_{++}<=-1 in the first H,K plus channel after all normalization errors are included.
- falsifier: the perimeter/cusp subtraction leaves a finite scheme-dependent R_{ij}, violating the same-theory condition.
- falsifier: the small-area OPE error is not uniform near the boundary collar, so R cannot be inserted into the finite Schur-Feshbach matrix.
- falsifier: the hairpin geometry has Theta_{++}=0, killing the positive pair term and making this channel non-diagnostic.
- falsifier: the connected cumulant exists only at positive flow time and has no controlled tau-to-continuum matching.

## Learning

The actual R-kernel is not a symbolic lambda. It is P_{ij}(1+chi_{ij}), where P_{ij} is an explicitly positive flowed two-curvature cross-pairing with color factor 2(N^2-1), and every serious demotion is concentrated in the connected four-curvature polarization C_4^{ren}. The cancellation being used is disconnected-product removal plus one-hairpin perimeter/cusp subtraction.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Compute C_4^{tau,ren} for two boundary-normal flowed plaquette sheets using the heat-kernel propagator and the YM three- and four-gluon vertices; output the coefficient c_N and the sign of chi_{++} at scale mu=1/d.

# Gauge-Invariant Observable Density In The Excitation Sector -> concrete Wilson R audit

## Candidate Lemma

For a finite SU(N) family of heat-kernel regulated fundamental Wilson collar/hairpin sheets, the order-g_R^4 connected boundary-OPE polarization matrix decomposes as a positive Schur-square flux-covariance block plus a connected four-curvature cumulant. The valid finite positivity audit is the Schur-Feshbach corrected inequality comparing this positive block against kappa and hairpin subtraction.

## Definitions

- source object: same-regulator vacuum-normalized Wilson observables \widetilde W_i^\sigma=W_i^\sigma/\langle W_i^\sigma\rangle-1 built from small collar/hairpin sheets \Sigma_i.
- target object: the finite tangent form P(R_\sigma-B_\sigma^*E_\sigma^{-1}B_\sigma)P on the null block of the unperturbed Wilson Gram matrix.
- controlled interface: R_{ij,\sigma} is extracted from the connected Wilson cumulant \langle\widetilde W_i^\sigma\widetilde W_j^\sigma\rangle_c and inserted into the Schur-Feshbach tangent cone.
- same-theory condition: the heat-kernel regulator, coupling, vacuum normalization, connected cumulants, and Schur complement are all computed in the same Yang-Mills measure; no Gaussian replacement is allowed except as a decomposition with residual kappa.
- Generators satisfy \operatorname{tr}(T^aT^b)=\delta^{ab}/2 in the fundamental representation.
- Transported curvature flux is \Phi_i^a=\int_{\Sigma_i}\rho_i(x)n_i^{\mu\nu}(x)\mathcal F_{\mu\nu,\sigma}^a(x;x_0)\,d^2x.

## Assumptions

- The heat-kernel flow time \sigma^2>0 makes all curvature insertions finite and gauge covariant after parallel transport to x_0.
- The chosen sheets are small enough for a regulated boundary OPE with a controlled remainder \mathcal E_\sigma.
- The finite Schur-Feshbach block has complement E_\sigma>0 on Q=1-P.
- Global color invariance of the regulated vacuum is unbroken, so two-flux covariances are color diagonal in the base frame.

## Equations

- transported flux covariance: `C_{ij,\sigma}^{ab}=\langle \Phi_i^a\Phi_j^b\rangle_c,\qquad C_{ij,\sigma}^{ab}=\delta^{ab}K_{ij,\sigma}`. Valid when: Valid when the heat-kernel flow time is positive and global color invariance fixes the transported two-point function.
- vacuum-normalized Wilson expansion: `\widetilde W_i^\sigma=-\frac{g_R^2}{4N}\big(\Phi_i^a\Phi_i^a-\langle\Phi_i^a\Phi_i^a\rangle\big)+\mathcal O_\sigma(g_R^3\Phi_i^3)`. Valid when: Applies after same-theory vacuum and perimeter normalization for small regulated sheets admitting the boundary OPE expansion.
- connected polarization decomposition: `R_{ij,\sigma}=\frac{g_R^4}{16N^2}\left(2\sum_{a,b}C_{ij,\sigma}^{ab}C_{ji,\sigma}^{ba}+\mathfrak K_{ij,\sigma}\right)+\mathcal E_{ij,\sigma}`. Valid when: Requires the connected expectation from the same regulated Yang-Mills measure and keeps the order g_R^4 Wilson cumulant coefficient.
- color-geometric Gaussian block: `R^G_{ij,\sigma}=\frac{g_R^4(N^2-1)}{8N^2}K_{ij,\sigma}^2,\qquad R^G_\sigma=\frac{g_R^4(N^2-1)}{8N^2}(K_\sigma\circ K_\sigma)\succeq0`. Valid when: Valid when the scalar flux covariance matrix K_sigma is positive semidefinite, so the Schur product theorem applies.
- promotion inequality for the corrected tangent form: `\lambda_{\min}\big(P R^G_\sigma P\big)>\frac{g_R^4}{16N^2}\|P\mathfrak K_\sigma P\|+\|PB_\sigma^*E_\sigma^{-1}B_\sigma P\|+\|P\mathcal E_\sigma P\|`. Valid when: Applies on the finite null block selected by the unperturbed Gram matrix with E_sigma strictly positive on the hairpin complement.

## Attempted Derivation

- Use the heat-kernel regulator and parallel transport every curvature insertion to a common base point, producing adjoint fluxes \Phi_i^a with finite same-theory cumulants.
- Expand the fundamental Wilson trace. The linear term vanishes by \operatorname{tr}T^a=0; the first nontrivial vacuum-subtracted term is the quadratic flux observable with coefficient -g_R^2/(4N).
- In \langle\widetilde W_i\widetilde W_j\rangle_c, same-sheet self-contractions cancel against the vacuum/perimeter normalization and connected subtraction; only crossed sheet contractions and the connected four-flux cumulant remain.
- Apply the cumulant identity \operatorname{Cov}(X_aX_a,Y_bY_b)=2\operatorname{Cov}(X_a,Y_b)^2+\operatorname{cum}(X_a,X_a,Y_b,Y_b).
- Color invariance gives C_{ij}^{ab}=\delta^{ab}K_{ij}; hence the crossed two-curvature term has coefficient g_R^4(N^2-1)/(8N^2) times K_{ij}^2.
- Since K_\sigma is a finite covariance matrix, K_\sigma\circ K_\sigma is positive semidefinite by the Schur product theorem. Thus Gaussian R cannot be the negative obstruction.
- Insert R_\sigma into the already promoted finite Schur-Feshbach tangent form and obtain the explicit promotion inequality against \mathfrak K, OPE remainder, and hairpin energy.

Blocking gap: The branch still lacks a same-theory numerical or rigorous bound on \mathfrak K_{ij,\sigma} and \mathcal E_{ij,\sigma} for the first concrete H,K collar/hairpin geometry, and B_\sigma^*E_\sigma^{-1}B_\sigma has not yet been evaluated there.

## Falsifiers

- falsifier: the selected collar/hairpin orientations make P(K_\sigma\circ K_\sigma)P singular, leaving no positive Gaussian margin.
- falsifier: the connected four-curvature cumulant \mathfrak K_\sigma is negative with norm larger than the Schur-square covariance margin.
- falsifier: the finite hairpin coupling PB_\sigma^*E_\sigma^{-1}B_\sigma P dominates even when R^G_\sigma is positive.
- falsifier: the heat-kernel boundary-OPE remainder is the same size as the proposed second-order tangent coefficient.
- falsifier: computing R, B, and E with inconsistent regulators or normalizations destroys the same-theory cancellation and makes the sign test invalid.

## Learning

The new contribution is that the calculable Gaussian part of R is not merely positive entrywise; it is a Hadamard square of the flux covariance and therefore positive semidefinite on every finite subspace. The real obstruction is sharply localized to the connected four-curvature cumulant, the OPE remainder, and the Schur hairpin energy. This gives a valid sign/size test rather than another OS-density loop.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Fix the first concrete rectangular collar/hairpin sheets, evaluate K_{ij,\sigma} from the heat-kernel curvature two-point contraction or its plaquette-sheet discretization, compute B_\sigma^*E_\sigma^{-1}B_\sigma, and estimate \mathfrak K_{ij,\sigma} from the connected four-plaquette cumulant; then test the promotion inequality directly.
