# cycle-0075

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Beta-zero XOR transfer is valid, but any searchable EF+SAT_U proof-mediated source certificate for C(H_N^SAT)>N^{1+epsilon} must either avoid dense functional naturalization or certify the row-residual robustness gate below; otherwise a concrete falsifier gives a subthreshold H circuit.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), x in {0,1}^N, M_N<=N^{q+o(1)}, L_N=(log N)^d.
- target object: SAT has no polynomial-size nonuniform circuits; equivalently SAT notin P/poly by contradiction against every fixed exponent c.
- controlled interface: beta=0 batched substitution, using a size L^c SAT circuit only on generated polylog queries and paying C(G_N)+M_N L_N^c.
- target-preserving condition: q<1+epsilon, rho<1+epsilon, no advice except the fixed generator family, and the same nonuniform circuit size measure on source and target.
- certificate model: EF+SAT_U is Extended Frege with atoms naming SAT labels on U_N=im(G_N), searchable in 2^{O(L_N)} and sound for real SAT labels.
- row residual: a pair (D_N,R_N) with D_N agreeing with H_N^SAT on all source rows outside R_N and circuit size C(D_N)=S_D.

## Assumptions

- Circuits are nonuniform Boolean circuits of fan-in two; size constants are irrelevant to exponents.
- The generator family has C(G_N)<=N^{rho+o(1)} and outputs L_N-bit SAT instances with d>1 fixed.
- The source claim is an unrestricted lower bound C(H_N^SAT)>N^{1+epsilon-o(1)}, not a restricted-model or promise lower bound.
- Functional certificate soundness means validity over arbitrary label vectors on U_N; SAT-semantic soundness alone is weaker and nonrelativizing.
- Certificate advice cannot encode an exceptional row set R_N of size below N^{epsilon-o(1)}.

## Equations

- beta0_substitution: `C(H_N^{SAT}) \le C(G_N)+M_N\cdot L_N^c+O(M_N\log M_N)=N^{\max\{\rho,q\}+o(1)}`. Valid when: Valid when L_N=(log N)^d, M_N<=N^{q+o(1)}, C(G_N)<=N^{rho+o(1)}, and a size n^c SAT circuit is substituted nonuniformly into every generated query.
- row_residual_patch: `D_N=H_N^{SAT}\text{ off }R_N \Rightarrow C(H_N^{SAT})\le S_D+O(|R_N|N)`. Valid when: Valid when unrestricted circuits may hardwire the exceptional N-bit rows and compare equality to each row before output correction.
- robustness_gate: `\forall(D_N,R_N)\;[D_N=H_N^{SAT}\text{ off }R_N \Rightarrow S_D+O(|R_N|N)\ge N^{1+\epsilon-o(1)}]`. Valid when: Requires a claimed source lower bound C(H_N^SAT)>N^{1+epsilon-o(1)} in the same nonuniform circuit model.

## Attempted Derivation

- Assume SAT has size n^c circuits. Substitute the circuit into each L_N-bit generated query of H_N and charge the generator once, giving the beta-zero transfer bound.
- If q,rho<1+epsilon and C(H_N^SAT)>N^{1+epsilon-o(1)}, the transfer contradicts SAT in SIZE(n^c) for every fixed c; this is route-level SAT notin P/poly only from the source bound.
- Given D_N agreeing with H_N off R_N, patch D_N by equality tests for rows in R_N. If S_D+O(|R_N|N)<N^{1+epsilon}, the source lower bound is false.
- For EF+SAT_U certificates, dense functional soundness yields a natural label property; nonfunctional SAT-semantic soundness must therefore certify the row-residual gate or remain only a heuristic witness.

Blocking gap: No theorem yet extracts row-residual robustness from short EF+SAT_U semantic proofs, and no construction yet proves such extraction impossible.

## Falsifiers

- Subthreshold residual falsifier: find D_N,R_N with D=H off R and S_D+O(|R|N)<N^{1+epsilon-o(1)}.
- Naturalization falsifier: EF+SAT_U certificates are dense, 2^{O(L)} searchable, and functionally sound over all label vectors on U_N.
- Advice leakage falsifier: the certificate or generator encodes an exceptional row set of size N^{theta} with theta<epsilon.
- Beta/q falsifier: any hidden query-length exponent beta>0 or overhead max{rho,q}>=1+epsilon collapses the all-exponent target transfer.

## Learning

Cycle 75 turns the Psys gap into a precise EF+SAT_U audit. Ordinary semantic soundness is insufficient: a valid proof-mediated beta-zero XOR route must either be nonlarge/nonconstructive/direct or certify row-residual robustness against subthreshold patching.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for EF+SAT_U row leakage.`
- Rationale: The abstract bridge is already valid; the live uncertainty is whether SAT-semantic certificates can hide a sparse exceptional row set without becoming functional natural proofs.
- Situation seed: Fix H_N^SAT with q,rho<1+epsilon and plant an EF+SAT_U proof transcript that verifies all rows except a selectable residual set R_N, while D_N computes the verified-row parity.
- Varied variable: theta in |R_N|=N^theta, varied across theta<epsilon, theta=epsilon, and theta>epsilon.
- Held-fixed controls: L_N=(log N)^d with d>1 and beta=0 substitution., Same nonuniform circuit model for source H_N and target SAT., No nonuniform advice except the fixed generator and public EF+SAT_U rules., M_N<=N^{q+o(1)} with q<1+epsilon.
- Expected observation: For theta<epsilon, equality patching should always give a subthreshold H circuit; for theta>=epsilon, the row-residual attack no longer falsifies the source bound by itself.
- Transfer certificate needed: A formal EF+SAT_U extraction/no-extraction theorem: accepted SAT-semantic certificates either yield functional label properties or imply the robustness gate against all D_N,R_N pairs.

## Next Experiment

Instantiate EF+SAT_U proofs as circuits over SAT_U label atoms, define functionalization formally, and try to construct a theta<epsilon residual-leaky transcript or prove extraction to the robustness gate.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Conditional bridge: a beta-zero XOR proof-mediated lower-bound certificate with logarithmic target projection, logarithmic projection-decision width, and DirectClusterSound(C,k) induces a valid large constructive property useful against SIZE_{m_N}(N^k).

## Definitions

- source object: H_N^SAT is the beta-zero XOR truth table on N coordinates, H_N(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N<=N^{q+o(1)}, SAT query length L_N=(log N)^d, and generator overhead N^{rho+o(1)}.
- target object: P_C is the truth-table property accepted by the projected row-cluster CSP Phi_C(T|_{U_C},z) for N-bit tables T, targeting SIZE_{m_N}(N^k) where m_N=ceil(log N).
- controlled interface: a uniform Psys row cluster C whose verifier rows query target coordinates Q_r and proof variables, with U_C=union_{r in C}Q_r and projected existential decision width d_N.
- target-preserving condition: DirectClusterSound(C,k) holds, meaning every SIZE_{m_N}(N^k) circuit truth table makes Phi_C unsatisfiable for all proof-view assignments, while H_N^SAT has an accepting projected proof view.

## Assumptions

- Model: nonuniform Boolean circuits over m_N input bits, size threshold N^k, with no hidden row-selection advice beyond O(log N) uniformly recoverable public parameters.
- Regime: |U_C|<=a log N and d_N<=b log N for constants a,b independent of N and of the target circuit.
- Constructivity: from N and C, the projected predicate Phi_C(T|_{U_C},z) is decidable in N^{O(1)} time by enumerating or dynamic-programming over the width-d_N proof-view representation.
- Completeness: the actual H_N^SAT projection is accepted by some proof-view assignment z*, so the property is nonempty and contains the source object.
- Usefulness: DirectClusterSound is semantic over all small circuit truth tables, not merely ordinary verifier soundness for a fixed global proof.

## Equations

- projection_size: `U_C=\bigcup_{r\in C}Q_r,\qquad |U_C|=w_N\le a\log N`. Valid when: Valid when C is a uniformly selected row cluster and Q_r are exactly the verifier target-table queries.
- largeness: `\Pr_{T\leftarrow\{0,1\}^N}[T\in\mathcal P_C]=|A_C|/2^{w_N}\ge 2^{-w_N}\ge N^{-a}`. Valid when: Valid when completeness makes the projected accepting set A_C nonempty and w_N is logarithmic.
- constructivity_time: `\mathrm{Time}_{construct}(\mathcal P_C)\le N^{O(1)}2^{O(d_N)}=N^{O(1)}`. Valid when: Valid when the projection-decision representation has width d_N=O(log N) and is uniformly given.
- direct_usefulness: `\mathrm{DirectClusterSound}(C,k):\ \forall B\in SIZE_{m_N}(N^k)\ \forall z\ \neg\Phi_C(TT(B)|_{U_C},z)`. Valid when: Valid when usefulness is required against the same nonuniform circuit class named by the target theorem.

## Attempted Derivation

- Instantiate Psys as a row-local projection-CSP verifier for beta-zero XOR certificates; rows query target coordinates Q_r and proof variables P_r.
- For a candidate cluster C, form Phi_C(T|_{U_C},z), the existential CSP describing simultaneous acceptance of all rows in C under a projected proof view z.
- Completeness gives Phi_C(H_N^SAT|_{U_C},z*) for some z*, hence P_C is nonempty.
- If |U_C|=O(log N), P_C has density at least 2^{-|U_C|}=N^{-O(1)} among all N-bit truth tables.
- If the projection-decision width is O(log N), membership in P_C is decidable in N^{O(1)} time, so the property is constructive.
- To make P_C useful against SIZE_{m_N}(N^k), one needs DirectClusterSound(C,k), excluding every small circuit truth table from the projected accepting set.
- Ordinary soundness only excludes globally consistent accepting proofs; the odd-charge Tseitin embedding supplies locally satisfying proof views for every target table on proper clusters.
- Sparse residual compression shows that any certificate whose row selection leaves only a small exceptional set also leaks a nonuniform patching circuit for H_N.

Blocking gap: No named proof system in the current packet proves DirectClusterSound(C,k) from ordinary soundness, local consistency, or bounded projection treewidth alone.

## Falsifiers

- Odd-charge Tseitin with dummy SAT projection: every logarithmic proper cluster is satisfiable for every target truth table, so ordinary soundness is not a valid substitute for DirectClusterSound.
- Sparse-row residual compression: if accepted certificates reveal D_N plus |R_N|=o(N^epsilon) exceptions in the P_N=N row-block regime, the claimed N^{1+epsilon} source lower bound is falsified by patching.
- Natural-proofs pressure: if the cluster property is large, constructive, and useful against SIZE_{m_N}(N^k), then PRF assumptions for that class are the conflict target.
- Advice leakage falsifier: nonuniform row selection or proof-view advice of superlogarithmic size can encode the hard projection and destroy both constructivity and target preservation.
- Exponent-cap falsifier: beta-zero substitution gives no consequence when the asserted H_N lower bound fails to exceed N^{max{rho,q}+eta}.

## Learning

Cycle 75 upgrades the support branch from barrier language to a theorem/no-go fork. Logarithmic projection plus logarithmic decision width is useful only under DirectClusterSound; otherwise odd-charge Tseitin makes the accepted projected property density one and not useful. Sparse residuals add an independent quantitative falsifier for advice leakage. This is valid route-level progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for DirectClusterSound before promoting any beta-zero XOR certificate route.`
- Rationale: The branch already has the abstract naturalization theorem; the missing information is whether a concrete proof-mediated cluster can avoid the Tseitin local-satisfiability obstruction while preserving logarithmic projection width.
- Situation seed: Embed an odd-charge Tseitin parity component into a padded beta-zero XOR certificate verifier, with SAT-query labels wired as dummy projected coordinates and H_N^SAT parameters M_N<=N^{q+o(1)}, L_N=(log N)^d, generator overhead N^{rho+o(1)} held intact.
- Varied variable: The varied variable is the cluster projection width w_N, increased from a log N through the girth/full-parity-cover threshold of the Tseitin component.
- Held-fixed controls: Target class remains SIZE_{m_N}(N^k) with m_N=ceil(log N)., Cluster selection is uniform and advice-free except for O(log N) public parameters., The beta-zero XOR generator parameters q, rho, and d are unchanged., Verifier rows remain projection-CSP rows with bounded local arity and dummy SAT labels.
- Expected observation: For w_N below the parity-cover threshold, every cluster has an accepting proof view for every target table, so DirectClusterSound fails at density one; when w_N reaches a full odd-parity obstruction, usefulness may appear but logarithmic largeness can collapse if the cover threshold is superlogarithmic.
- Transfer certificate needed: A valid transfer needs a theorem that the actual named Psys forbids such Tseitin kernels or forces every logarithmic accepting cluster to carry a direct small-circuit contradiction, without adding nonuniform advice or increasing w_N beyond O(log N).

## Next Experiment

Instantiate one concrete Psys, preferably a PCP-style local proof of CC(H_N)>N^{1+epsilon} or an MCSP/MKtP certificate verifier, compute its U_C and projection-decision width, and test whether DirectClusterSound survives the odd-charge Tseitin embedding without row advice.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Let H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N<=N^{q+o(1)}, query length L_N=(log N)^d, and generator size N^{rho+o(1)}. If a Psys/MCSP/MKtP certificate carrier computes the queried SAT labels through an advice-free adaptive cover of exponent alpha_ad except on a residual R_N of size N^{r+o(1)}, then C(H_N^{SAT})<=N^{max{rho,q+alpha_ad,r+1}+o(1)}. Hence any claimed source lower bound C(H_N^{SAT})>N^a is falsified when max{rho,q+alpha_ad,r+1}<a.

## Definitions

- source object: beta-zero SAT-XOR family H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N<=N^{q+o(1)}, L_N=(log N)^d, and G_N computable by circuits of size N^{rho+o(1)}.
- target object: a claimed unrestricted circuit lower bound C(H_N^{SAT})>N^a and any derived advice-free E/NP lower-bound consequence; this is route-level evidence, not P != NP itself.
- controlled interface: Psys/MCSP/MKtP certificate openings for the SAT-query labels, summarized by an adaptive-cover exponent alpha_ad and a residual exception set R_N.
- target-preserving condition: the opener, row selector, and residual semantics refer to the same H_N^{SAT} lengths, use no advice or auxiliary language, and preserve the unrestricted circuit model used by the target claim.

## Assumptions

- Unrestricted Boolean circuit size C(.) is measured as a function of the outer input length N.
- The SAT-query generator G_N is uniform enough to have size N^{rho+o(1)} circuits on inputs (x,j).
- For every nonresidual pair (x,j), the accepted certificate supplies a functional label opener with adaptive-cover exponent alpha_ad; nonfunctional semantic certificates are outside this lemma until functionalized.
- The residual set R_N is a set of outer inputs x where the derived predictor may disagree with H_N^{SAT}; for a nonuniform upper bound its members may be hardwired at cost O(|R_N|N).
- The falsifier is valid only when the lower-bound claim and the constructed upper bound are for the identical H_N^{SAT} family and the identical circuit model.

## Equations

- adaptive_cover_cap: `\alpha_{ad}=\max\{\tau,\max_\ell(a_\ell+\mu_\ell),\max_\ell\omega_\ell\}`. Valid when: Valid when the certificate carrier is represented by adaptive summaries, openings, and transcript control costs in one unrestricted circuit model.
- beta0_cover_predictor_size: `C(D_N)\le N^{\rho+o(1)}+N^{q+\alpha_{ad}+o(1)}`. Valid when: Valid when each queried SAT label is opened by the same advice-free adaptive cover and M_N is at most N^{q+o(1)}.
- row_residual_patch: `C(H_N^{SAT})\le C(D_N)+O(|R_N|N)\le N^{\max\{\rho,q+\alpha_{ad},r+1\}+o(1)}`. Valid when: Applies after D_N agrees with H_N^{SAT} off R_N and residual inputs may be hardwired in unrestricted circuits.
- source_lower_bound_falsifier: `\max\{\rho,q+\alpha_{ad},r+1\}<a\quad\Rightarrow\quad \neg[C(H_N^{SAT})>N^a]`. Valid when: Requires the claimed lower bound to target the same explicit beta-zero XOR family and the same unrestricted circuit size measure.

## Attempted Derivation

- Fix N and the beta-zero family H_N^{SAT}; assume a certificate-derived predictor D_N computes all queried SAT labels outside residual R_N.
- Implement G_N once with size N^{rho+o(1)} to generate each query G_N(x,j).
- For each j<=M_N, attach the certificate label opener. Since M_N<=N^{q+o(1)} and each opener costs N^{alpha_ad+o(1)}, the total label-opening cost is N^{q+alpha_ad+o(1)}.
- XOR the M_N labels to compute D_N(x); this adds only lower-order gate cost.
- Patch disagreements on R_N by hardwiring equality tests for residual outer inputs, costing O(|R_N|N)=N^{r+1+o(1)} when |R_N|=N^{r+o(1)}.
- Compare the resulting upper exponent max{rho,q+alpha_ad,r+1} with the claimed lower-bound exponent a.

Blocking gap: For a named Psys beyond the DirectClusterSound-style toy carrier, we still need a formal theorem that accepted certificates either yield functional label openings/residuals or avoid every such adaptive cover. Without that dichotomy the no-go is scoped to low-cover carriers.

## Falsifiers

- falsifier: alpha_ad<a-q-o(1) and |R_N|<N^{a-1-o(1)} give an explicit unrestricted circuit below the claimed source lower bound.
- falsifier: a hard-row selector using nonuniform advice proves only a nonuniform row claim unless the advice is charged by multiplexing or removed.
- falsifier: a locally checkable dense projection of accepted certificates to useful small-circuit avoidance becomes a natural-property obstruction, not a valid sparse carrier.
- falsifier: residual agreement with an easy D_N off polynomially many inputs collapses any claimed N^{1+epsilon} beta-zero lower bound when r<epsilon.

## Learning

Cycle 75 converts the adaptive-cover audit into a beta-zero XOR exponent test: low label-cover cost is charged as q+alpha_ad, sparse residuals as r+1, and generator overhead as rho. This gives a finite falsifier for MCSP/MKtP certificate carriers before any promotion of the beta-zero row-residual packet.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the beta-zero XOR packet.`
- Rationale: The route needs a concrete exponent threshold for when MCSP/MKtP certificates produce an upper bound on the exact target family rather than merely sounding weak.
- Situation seed: Take H_N^{SAT}(x)=xor_{j<=N^{0.42}} SAT(G_N(x,j)) with L_N=(log N)^d, generator size N^{0.48+o(1)}, and a proposed Psys certificate proving C(H_N^{SAT})>N^{1.06}. The certificate clusters query labels and has an adaptive opener except on R_N.
- Varied variable: Vary the adaptive-cover exponent alpha_ad of the label opener from 0.40 to 0.70.
- Held-fixed controls: M_N=N^{0.42+o(1)}, rho=0.48, and beta-zero query length L_N=(log N)^d are fixed., No advice is allowed in row selection or certificate opening., Residual size is held at |R_N|<=N^{0.03+o(1)} unless the experiment explicitly crosses the patch threshold., The target remains the same H_N^{SAT} circuit lower bound, not an auxiliary MCSP language.
- Expected observation: For alpha_ad<0.64, the upper exponent max{0.48,0.42+alpha_ad,1.03} is below 1.06, so the carrier is invalid. At alpha_ad>=0.64, the low-cover falsifier no longer fires and the proof obligation becomes high adaptive-cover dimension or direct anti-ball soundness.
- Transfer certificate needed: A formal opener-to-circuit lemma showing that accepted Psys certificates generate functional SAT labels for all nonresidual outer inputs, plus a same-family residual agreement certificate for H_N^{SAT}.

## Next Experiment

Instantiate Psys as the beta-zero XOR certificate model from the main packet; compute tau,a_l,mu_l,omega_l, residual exponent r, and selector advice b_N, then decide whether the carrier is killed by max{rho,q+alpha_ad,r+1}<a.
