# cycle-0079

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: beta-zero XOR row-forcing audit

## Candidate Lemma

For the beta-zero XOR carrier, any occurrence-oracle or functionally label-local certificate that soundly implies C(H_N^SAT)>N^{1+epsilon-o(1)} must force at least N^{epsilon-o(1)} full source rows. If the certificate constrains a set Q of generated SAT instances and fewer than N^{epsilon-o(1)} rows have all M_N parity coordinates in Q, then an occurrence-label spoof agrees with the certificate transcript but yields a sparse-row carrier of size below the claimed source threshold.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) on x in {0,1}^{n_N}, with source truth-table length N=2^{n_N}, M_N<=N^{q+o(1)}, formula length L_N=(log N)^d, and generator circuit size N^{rho+o(1)}.
- target object: the target consequence is SAT notin P/poly obtained only through the beta=0 substitution bridge, not through a direct proof of P != NP.
- controlled interface: a named certificate verifier Psys=EF+SAT_U^{occ} sees generated formula occurrences and SAT labels through a bounded occurrence/label interface Q_pi and may output a claimed lower bound C(H_N^SAT)>N^{1+epsilon-o(1)}.
- target-preserving condition: max{rho,q}<1+epsilon, L_N=N^{o(1)}, no certificate advice may be reused as a circuit for SAT, and the proof must remain valid after separating route-level H_N lower bounds from the main NP notsubset P/poly target.
- ForcedRows(Q)={x: G_N(x,j) in Q for every j<=M_N}; these are the rows whose XOR parity cannot be freely reset by changing at least one unmentioned occurrence label.
- An occurrence-label spoof for Q is a label assignment A_Q agreeing with SAT on every formula occurrence in Q and choosing unmentioned generated labels so that H_N^{A_Q}(x)=0 for every x notin ForcedRows(Q).

## Assumptions

- Nonuniform Boolean circuit size is the source model; equality testing an n_N-bit row costs O(n_N) gates, recorded as O(N^{o(1)}) per patched row in the truth-table-length parameter N.
- The generator G_N is uniform enough that circuits can compute all generated formulas for a row with size N^{rho+o(1)} and can substitute target SAT circuits of size L_N^c for each generated query.
- The certificate method is occurrence-relativizing: its acceptance transcript is determined by the explicit proof string, the generated occurrences in Q_pi, and their labels, and is invariant under arbitrary changes to unmentioned generated labels.
- Soundness is functional or occurrence-semantic in the scoped sense: if the same transcript accepts against a label assignment A, then it asserts the same source lower bound for H_N^A.
- The no-go does not apply to a proof that derives new constraints on unmentioned SAT instances from real CNF syntax in a nonrelativizing way; that is the intended escape condition.

## Equations

- beta0_substitution_upper_bound: `C(H_N^{SAT}) \le N^{\rho+o(1)} + M_N\,L_N^c = N^{\max\{\rho,q\}+o(1)}`. Valid when: Valid when SAT on length L_N formulas has circuits of size L_N^c and the beta-zero generator makes only M_N<=N^{q+o(1)} polylog-length queries.
- sparse_row_patch_upper_bound: `C(F) \le S_D + O(E_N n_N) + N^{o(1)} \le S_D + N^{1+o(1)}E_N/N`. Valid when: Applies when a circuit D of size S_D agrees with the row function F except on E_N explicitly hardwired rows of n_N=log N bits.
- forced_row_spoof_size: `C(H_N^{A_Q}) \le N^{\rho+o(1)} + O(|ForcedRows(Q)|\,n_N)`. Valid when: Requires the occurrence-label spoof to zero every row outside ForcedRows(Q) and allows the remaining forced rows to be patched by equality gates.
- row_forcing_threshold: `|ForcedRows(Q_\pi)| \ge N^{\epsilon-o(1)}`. Valid when: Necessary when an occurrence-relativizing certificate transcript soundly asserts C(H_N)>N^{1+epsilon-o(1)} against all label assignments consistent with its queried occurrences.

## Attempted Derivation

- Fix an accepted occurrence-relativizing certificate pi and let Q_pi be the generated SAT occurrences whose labels affect its transcript.
- Define A_Q to agree with real SAT on Q_pi. For each source row x not in ForcedRows(Q_pi), choose one unmentioned coordinate j_x and set its label so that xor_j A_Q(G_N(x,j))=0.
- Then H_N^{A_Q} is supported only on ForcedRows(Q_pi). A circuit computes it by checking whether x is one of these rows and hardwiring the residual parity values; the size is N^{rho+o(1)}+O(|ForcedRows(Q_pi)| log N).
- If |ForcedRows(Q_pi)|<N^{epsilon-o(1)} and rho<1+epsilon, this circuit has size below N^{1+epsilon-o(1)}.
- Occurrence-relativizing transcript invariance makes pi accept equally under SAT and under A_Q, so functional soundness would assert the same lower bound for the easy spoofed carrier. Contradiction.

Blocking gap: The derivation is a proof only for EF+SAT_U^{occ} or functional label-local certificates. Full EF+SAT_U may use real formula syntax to constrain unmentioned generated instances, so an extraction theorem for Q_pi or a nonrelativizing semantic certificate is still missing.

## Falsifiers

- falsifier: a subthreshold residual circuit D_N with fewer than N^{epsilon-o(1)} bad rows gives C(H_N^SAT)<N^{1+epsilon-o(1)} by equality patching.
- falsifier: an accepted occurrence-relativizing certificate pi with |ForcedRows(Q_pi)|<N^{epsilon-o(1)} is unsound for the claimed source lower bound.
- falsifier: positive beta target-query length reintroduces the transfer cap q+beta c and destroys all-exponent SAT lower-bound transfer.
- falsifier: if the certificate proof string or verifier advice encodes more than N^{1+epsilon-o(1)} row information, the source lower bound is being assumed rather than certified.
- falsifier: ordinary EF+SAT_U soundness without row-residual robustness does not imply a valid source lower bound.

## Learning

Cycle 79 replaces vague SAT-semantic escape language by the full-row-forcing parameter ForcedRows(Q). A proof-mediated beta-zero XOR certificate that treats generated SAT instances as occurrence labels must force at least N^{epsilon-o(1)} complete parity rows; otherwise a private occurrence-label spoof gives a subthreshold sparse-row circuit. The valid contribution is a scoped no-go and an exact extraction obligation for full EF+SAT_U, not progress on the main conjecture itself.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The route has narrowed to whether SAT-semantic proof objects escape the functional row-local no-go. A concrete occurrence-label experiment tests exactly how many full parity rows a certificate must force before it can be valid evidence.
- Situation seed: Take a beta-zero XOR carrier with M_N=N^q, L_N=(log N)^d, rho<1+epsilon, and an EF+SAT_U^{occ} certificate whose proof mentions a set Q of generated formula occurrences. Construct an occurrence oracle A_Q agreeing with SAT on Q and zeroing every row with at least one free coordinate.
- Varied variable: gamma=log_N |ForcedRows(Q)|, the exponent of full-row forcing by the certificate.
- Held-fixed controls: q,rho<1+epsilon so the beta-zero target bridge remains target-preserving., L_N=(log N)^d so SAT substitution costs N^{o(1)} for every fixed target circuit exponent., The verifier transcript is occurrence-relativizing and cannot inspect labels outside Q., No nonuniform certificate advice is allowed to serve as a circuit for H_N or SAT.
- Expected observation: For gamma<epsilon, the spoofed carrier has circuit size N^{max{rho,gamma}+o(1)} below the source threshold while the certificate transcript remains unchanged; for gamma>=epsilon, this specific falsifier no longer applies.
- Transfer certificate needed: A formal transcript-invariance lemma extracting Q from the proof, plus a proof that full EF+SAT_U either satisfies this occurrence condition or explicitly uses nonrelativizing CNF semantics outside the method class.

## Next Experiment

Instantiate Psys=EF+SAT_U^{occ}: define the proof parser that extracts Q_pi, prove acceptance transcript invariance under A_Q, and compute whether known EF encodings force full rows or merely individual generated formula occurrences.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Affine-local syndrome repair gate: a logarithmic beta-zero XOR proof cluster whose only proof-side support for DirectClusterSound is bounded local F2/Tseitin consistency cannot be useful. For a connected odd-charge Tseitin core, every proper viewed set of vertex equations is satisfiable, so the existential local shadow accepts every target truth table. DirectClusterSound in this method class therefore requires seeing all syndrome rows, adding a nonlocal checksum, or using a genuinely target-functional constraint.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N<=N^{q+o(1)}, query length L_N=(log N)^d, generator overhead N^{rho+o(1)}, and truth table length N.
- target object: SIZE_m(m^k) circuits for the m=log N input truth table of H_N^SAT, with uniformity/advice fixed before the certificate is searched.
- controlled interface: a Psys cluster C with target projection U(C), proof-view equations B_{S_C}z=b_{S_C} from a connected Tseitin core, and existential shadow Sh_C={y in {0,1}^N: exists pi A_C(y|U(C),pi)=1}.
- target-preserving condition: if H_N^SAT in Sh_C and DirectClusterSound(C,k) excludes every SIZE_m(m^k) truth table from Sh_C, then Sh_C is a valid lower-bound certificate; the cluster search, projection map, and verifier must be poly(N)-uniform and advice-free.
- DirectClusterSound(C,k) means that for every circuit D of the target class, no assignment to the viewed proof labels makes C accept on TT(D)|U(C).
- Affine-local syndrome carrier means that all proof-only constraints viewed by C are F2-linear vertex equations of a Tseitin instance; no global parity row or semantic SAT oracle is available inside the cluster.

## Assumptions

- G_t=(V,E) is connected and bounded-degree, B is its F2 incidence matrix, and b in F2^V has odd total charge.
- The cluster views only S_C subseteq V of the Tseitin vertex equations, plus h=|U(C)| target truth-table coordinates.
- The embedding permits the target literals in C to be dummy or locally satisfiable independently of the syndrome variables, so the falsifier tests proof-side soundness alone.
- The claimed route uses ordinary proof soundness or local consistency as the support for DCS; no separate direct soundness theorem is assumed.
- The target model is fixed before the construction; hidden advice selecting residual rows or syndrome repairs is not allowed.

## Equations

- tseitin_rank_cut: `\operatorname{rank}_{\mathbb F_2}(B_S)=|S|\quad(S\subsetneq V),\qquad \operatorname{rank}(B_V)=|V|-1,\qquad B_V z=b\text{ is inconsistent iff }\sum_{v\in V}b_v=1.`. Valid when: Valid when G_t is connected, B is the vertex-edge incidence matrix over F2, and S is a proper subset of vertices.
- proper_view_shadow_density: `S_C\subsetneq V\ \text{and dummy target projection}\quad\Longrightarrow\quad \mu(\mathrm{Sh}_C)=1.`. Valid when: Applies when acceptance checks only a proper Tseitin row set and target queried bits impose no unsatisfied semantic constraint.
- dcs_repair_condition: `\mathrm{DCS}(C,k)\ \Longrightarrow\ S_C=V\ \text{or C observes a nonlocal syndrome checksum or target-functional constraint}.`. Valid when: Requires the claimed DCS proof to be derived solely from affine-local syndrome consistency in the fixed target model.

## Attempted Derivation

- Define DCS(C,k) as direct rejection of every target circuit table by the same cluster, not ordinary global proof soundness.
- Represent the proof-side local consistency gadget by a connected odd-charge Tseitin system Bz=b over F2.
- Use incidence-matrix rank: every proper subset of vertex equations is independent and hence satisfiable for any local charge pattern.
- Embed the Tseitin core into a beta-zero XOR certificate with dummy or independently satisfiable target projection, preserving the source H_N^SAT parameters.
- For any small target circuit D, if C sees a proper row subset, choose proof labels satisfying the viewed equations; then C accepts TT(D)|U(C).
- Therefore local F2 consistency cannot imply DCS unless C observes all syndrome rows or has a nonlocal/target-functional constraint.
- If such a DCS constraint exists while projection and decision width remain logarithmic, cycle79.L2 converts the cluster into a valid large constructive useful property, triggering natural-proofs pressure.
- Independently, if certificate nonfunctionality exposes a sparse residual approximant, cycle79.L3 patches it and falsifies the claimed N^{1+epsilon} source lower bound.

Blocking gap: The no-go is proved only for affine-local syndrome carriers and dummy-target embeddings. A named Psys could still use nonaffine SAT semantics, a global checksum, or nonconstructive cluster selection; each must be typed and audited separately.

## Falsifiers

- Tseitin-core falsifier: a connected odd-charge core of size t greater than the proof-view budget makes every proper local syndrome view satisfiable, so ordinary local consistency gives no DCS.
- Density-without-usefulness falsifier: under dummy target projection the existential shadow has density one but contains every small-circuit truth table.
- Sparse residual falsifier: any exposed D_N with |R_N|=o(N^epsilon) and S_D<N^{1+epsilon-o(1)} yields C(H_N^SAT)<N^{1+epsilon}.
- Natural-proofs falsifier: if DCS plus logarithmic projection succeeds, the induced property is large, constructive, and useful against SIZE_m(m^k), conflicting with PRF-style assumptions for that class.
- Advice-leakage falsifier: row choices or proof clusters selected by hidden polynomial advice must be charged, otherwise the target-preserving condition is invalid.

## Learning

Cycle 79 adds a repair threshold to the support branch: affine-local Tseitin consistency cannot become DirectClusterSound unless the cluster sees the whole syndrome core or introduces a nonlocal/target-functional escape. Seeing the whole core breaks logarithmic-view density when t is chosen larger than the view budget; adding DCS at logarithmic width naturalizes. This is valid route-level progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch needs a concrete target-preserving stress test that distinguishes true DirectClusterSound from ordinary local consistency and measures the exact projection-width repair cost.
- Situation seed: Embed an odd-charge Tseitin core G_t into the proof-view side of a beta-zero XOR certificate for H_N^SAT, while the target SAT queries in U(C) are padded dummy queries preserving the H_N^SAT generator parameters.
- Varied variable: Tseitin core size t relative to the cluster proof-view budget b_N=O(log N).
- Held-fixed controls: M_N<=N^{q+o(1)}, L_N=(log N)^d, and generator overhead N^{rho+o(1)} remain fixed., The target class is SIZE_m(m^k) with no hidden advice and the same truth-table length N., The cluster target projection satisfies |U(C)|=O(log N)., The verifier uses only affine-local F2/Tseitin consistency unless an explicit escape feature is declared.
- Expected observation: For t>b_N every cluster sees a proper syndrome subset, hence its existential shadow accepts every target circuit table; for t<=b_N a direct refutation can exist but the logarithmic projection then naturalizes the property.
- Transfer certificate needed: A formal embedding from the named Psys views to affine Tseitin rows, plus a proof that dummy SAT projection preserves the beta-zero XOR source parameters and the target SIZE_m(m^k) model.

## Next Experiment

Instantiate Polynomial Calculus or low-degree F2 proof certificates as Psys: map each verifier view to affine syndrome rows, choose t=omega(log N), and test whether any accepted beta-zero XOR certificate supplies DCS without a global checksum or target-functional constraint.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

DCS-LC row-parity semantic cover falsifier: for beta-zero SAT-XOR H_N, any DCS-LC certificate whose openings have adaptive cover exponent alpha_ad and whose row-parity semantics fail only on |R_N|<=N^{r+o(1)} rows gives C(H_N)<=N^{max(rho,q+alpha_ad,r+1)+o(1)}. Hence it falsifies any route claim C(H_N)>N^a with a above this maximum.

## Definitions

- source object: H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N<=N^{q+o(1)}, beta=0, and G_N generated with circuit overhead N^{rho+o(1)}.
- target object: unrestricted nonuniform circuits for the same Boolean family H_N^{SAT}; the conclusion is an upper-bound obstruction to a proposed source lower bound, not P != NP.
- controlled interface: a named DirectClusterSound label-cover certificate family DCS-LC_N whose row openings compute bits b_Pi(x,j) through an adaptive cover with exponent alpha_ad=max(tau,max_l(a_l+mu_l),max_l omega_l).
- target-preserving condition: the certificate is row-parity SAT-semantic, meaning xor_j b_Pi(x,j)=H_N^{SAT}(x) for every source row x outside a residual row set R_N, and no padding, oracle, or advice changes the target family.
- residual exponent: |R_N|<=N^{r+o(1)} and residuals are charged as whole source rows, not merely bad query pairs.
- negative-use convention: a fixed low-cover certificate may be hardwired into the circuit upper bound, so selector advice is irrelevant for this falsifier direction.

## Assumptions

- Model: H_N has source input length N in the row-residual ledger, so correcting one exceptional row by equality costs O(N) gates up to polylog factors.
- Uniformity: G_N is the fixed beta-zero SAT-query generator; all generated formulas stay in the intended polylog-length SAT instance model.
- Cover regime: every opening used in one row can be flattened to an unrestricted circuit of size N^{alpha_ad+o(1)} after accounting for all adaptive levels.
- Semantic regime: DCS-LC ordinary local consistency is not assumed sufficient; the needed property is explicit row-parity binding to SAT values outside R_N.
- Non-claim: this is a valid route-level obstruction theorem only; it gives no lower bound and no proof of P != NP.

## Equations

- source_xor: `H_N^{\mathrm{SAT}}(x)=\bigoplus_{j\le M_N} \mathrm{SAT}(G_N(x,j)),\quad M_N\le N^{q+o(1)}`. Valid when: Valid when x ranges over the beta-zero source inputs and G_N is the fixed uniform SAT-query generator.
- adaptive_cover_cap: `\alpha_{ad}=\max\{\tau,\max_l(a_l+\mu_l),\max_l \omega_l\}`. Valid when: Valid when the DCS-LC proof-opening stream is flattened into adaptive summary, decoder, and overhead levels.
- row_parity_binding: `D_\Pi(x):=\bigoplus_{j\le M_N} b_\Pi(x,j)=H_N^{\mathrm{SAT}}(x)\quad \text{for }x\notin R_N`. Valid when: Valid when the named certificate proves SAT-semantic row parity, not merely local label consistency.
- low_cover_surrogate_size: `C(D_\Pi)\le N^{\max\{\rho,q+\alpha_{ad}\}+o(1)}`. Valid when: Applies after adaptive covers are flattened to unrestricted circuits and q counts the full SAT-query fanout.
- residual_correction_bound: `C(H_N^{\mathrm{SAT}})\le C(D_\Pi)+O(|R_N|N)\le N^{\max\{\rho,q+\alpha_{ad},r+1\}+o(1)}`. Valid when: Requires the residual set to consist of source rows, so equality corrections cost O(N) each.

## Attempted Derivation

- Fix a DCS-LC_N certificate Pi_N and define b_Pi(x,j) as the bit returned by its covered opening for query j on row x.
- Use the beta-zero generator to produce all G_N(x,j) within N^{rho+o(1)} overhead and use the adaptive cover to open all M_N<=N^{q+o(1)} labels with total size N^{q+alpha_ad+o(1)}.
- XOR the opened bits to obtain a surrogate D_Pi(x). This step needs only row-parity binding, not entrywise equality b_Pi(x,j)=SAT(G_N(x,j)).
- Assume D_Pi(x)=H_N^{SAT}(x) for x outside R_N. Add a residual correction gate E_R(x)=xor_{u in R_N} [x=u]*(H_N(u) xor D_Pi(u)).
- Charge the correction by O(|R_N|N)=N^{r+1+o(1)} and combine exponents to get C(H_N)<=N^{max(rho,q+alpha_ad,r+1)+o(1)}.
- Conclude that any certificate route claiming a larger exponent is internally falsified.

Blocking gap: The remaining open validation is proving row-parity SAT-semantic binding for the named DCS-LC proof system. Local consistency, ordinary soundness, or cluster agreement alone does not imply this binding; an odd-charge Tseitin-style parity ambiguity remains a concrete falsifier.

## Falsifiers

- DCS-LC accepts locally consistent labels whose row parity is not SAT-semantic for H_N^{SAT}.
- Odd-charge Tseitin or cycle-parity gadgets produce projection-indistinguishable labels with opposite global parity.
- Adaptive cover exponent satisfies q+alpha_ad below the claimed lower-bound exponent, yielding a valid upper-bound contradiction.
- Residual errors are sparse rows with r+1 below the claimed exponent, so residual correction collapses the threshold.
- Residual accounting counts bad query pairs but not induced bad source rows; then the stated correction bound is invalid until repaired.
- A proposed MCSP/MKtP carrier uses a subthreshold opener, checkpoint, or block summary, giving row circuits before any lower-bound extraction.
- Entrywise SAT binding is demanded unnecessarily; if only row-parity binding is available it is sufficient, but if neither is available the route is quarantined.

## Learning

Cycle 79 sharpens the named DCS-LC packet: entrywise SAT binding is stronger than needed, row-parity binding is sufficient, and local soundness alone is invalid. The valid contribution is a finite falsifier theorem with cap max(rho,q+alpha_ad,r+1); the live proof obligation is now a precise parity-binding lemma or counterexample for the chosen Psys.

## Gedanken Experiment Design Seed

- Need decision: `design-now-as-falsifier-probe`
- Rationale: The branch needs a concrete target-preserving test of the semantic-binding gate; another abstract hardness-magnification restatement would not decide whether DCS-LC labels actually imply a circuit upper bound.
- Situation seed: Take a padded beta-zero SAT-query matrix A_N(x,j)=SAT(G_N(x,j)) with M_N=N^q, attach DCS-LC cluster labels that pass all local projection checks, and compare them with an odd-charge Tseitin-modified label family that preserves projections but flips one row parity.
- Varied variable: adaptive cover exponent alpha_ad, varied across the threshold a-q while keeping the residual exponent fixed.
- Held-fixed controls: The source family H_N^{SAT}, generator G_N, query exponent q, and overhead rho are unchanged., The target circuit model is unrestricted nonuniform circuits at the same N scale., Residuals are charged as whole source rows with |R_N|<=N^{r+o(1)}., No hard-row selector, oracle change, or advice-dependent language change is allowed.
- Expected observation: Below alpha_ad<a-q and r+1<a, any row-parity-bound certificate yields a small circuit and is a falsifier; a locally sound but parity-ambiguous certificate teaches that semantic binding, not advice leakage, is the decisive missing axiom.
- Transfer certificate needed: A formal DCS-LC row-parity binding lemma or an explicit parity-ambiguity counterexample, plus an adaptive-cover flattening proof with the alpha_ad ledger and a row-residual correction certificate.

## Next Experiment

Instantiate the odd-charge Tseitin parity-ambiguity test inside the named DCS-LC local projection system: list the tested projections, construct two projection-identical labelings with opposite row parity or prove that a checked global parity axiom prevents them.
