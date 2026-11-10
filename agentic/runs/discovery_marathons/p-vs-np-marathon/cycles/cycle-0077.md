# cycle-0077

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Direct EF+SAT_U residual-closure theorem: for the beta-zero XOR carrier, any sound EF+SAT_U proof of the exact lower-bound sentence LB_N(T_N): C(H_N^SAT)>T_N automatically rules out every circuit D_N that agrees with H_N^SAT outside an explicitly listed row set R_N whenever |D_N|+aN|R_N|<T_N. Thus explicit sparse-row residual leakage is a falsifier for the claimed direct lower bound, not an extra independent audit; the remaining valid obstruction is extraction from SAT-semantic certificates to LB_N(T_N).

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) on N-bit source rows x, with M_N<=N^{q+o(1)} and query length L_N=(log N)^d.
- target object: all-exponent nonuniform SAT lower bounds, namely SAT notin SIZE(n^c) for every fixed c on the matched length set; this is a route-level target, not a proof of P != NP here.
- controlled interface: beta-zero substitution of a hypothetical SAT circuit of size L_N^c into the generated XOR carrier, with generator overhead N^{rho+o(1)} and no positive query exponent.
- target-preserving condition: max{rho,q}<1+epsilon, d>1 or any polylog L_N with L_N^c=N^{o(1)}, same nonuniform circuit model, and all generator/proof advice counted in the source-size budget.
- Psys object: EF+SAT_U is Extended Frege augmented with sound axioms for the actual SAT truth values on U_N={G_N(x,j)}; a direct certificate concludes LB_N(T_N), not merely a local semantic property.

## Assumptions

- Circuit model is nonuniform Boolean circuits with fan-in two; constants and hardwired exceptional row strings are charged.
- The equality test for one N-bit row costs at most aN+O(1) gates in the same circuit basis.
- The EF+SAT_U proof is sound for the actual SAT_U interpretation and its conclusion is the exact circuit lower-bound sentence LB_N(T_N).
- T_N=N^{1+epsilon-o(1)} and the source and target length sets are identical to those used by the beta-zero transfer.
- No uncharged advice selects exceptional rows or supplies hidden SAT labels.

## Equations

- carrier_definition: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\quad |G_N(x,j)|=L_N=(\log N)^d.`. Valid when: Valid when G_N is a fixed advice-free batched generator and rows are N-bit source inputs.
- beta_zero_transfer: `C(H_N^{SAT})\le C(G_N)+O(M_N\,C_{SAT}(L_N)+M_NL_N)\le N^{\max\{\rho,q\}+o(1)}.`. Valid when: Applies when SAT has L^c-size circuits for fixed c and L_N=(log N)^d makes L_N^c=N^{o(1)}.
- explicit_row_patching: `D_N=H_N^{SAT}\text{ off }R_N\quad\Rightarrow\quad C(H_N^{SAT})\le |D_N|+aN|R_N|+O(|R_N|).`. Valid when: Requires D_N to agree with H_N^{SAT} outside the explicitly listed row set R_N and constants to be charged nonuniformly.
- residual_threshold: `|D_N|+aNE_N<T_N\quad\Rightarrow\quad \neg LB_N(T_N)\text{ for }E_N=|R_N|.`. Valid when: Valid when the source lower-bound claim is an exact circuit lower bound for H_N^{SAT} at threshold T_N.
- conditional_target_consequence: `LB_N(N^{1+\epsilon-o(1)})\wedge \max\{\rho,q\}<1+\epsilon\quad\Rightarrow\quad \forall c\; SAT\notin SIZE(n^c)\text{ on matched lengths}.`. Valid when: Applies after the beta-zero transfer preserves advice accounting and the lower bound holds on the same infinite or eventual length set.

## Attempted Derivation

- Formalized LB_N(T_N) as the direct statement C(H_N^SAT)>T_N in the same nonuniform circuit model used by the beta-zero transfer.
- Constructed the standard equality-patch circuit: compute D_N, test x against each exceptional row r in R_N, and xor the needed correction bit on matches.
- Derived that any direct proof of LB_N(T_N) automatically excludes all explicit residual pairs (D_N,R_N) with |D_N|+aN|R_N|<T_N.
- Tried to lift ordinary EF+SAT_U semantic certificates to LB_N(T_N) by treating accepted certificates as evidence for row-residual robustness.
- Found the obstruction: if the certificate is only row-local and occurrence-relativizing, unseen occurrence labels can be assigned to make the carrier trivial outside the touched rows while preserving transcript acceptance.
- Separated the remaining live case as a nonrelativizing SAT-realization extraction problem, not as a consequence of ordinary semantic soundness.

Blocking gap: No theorem yet shows that actual EF+SAT_U certificates for the intended SAT_U carrier either reduce to the row-touch occurrence-local model or yield a nonrelativizing extraction from certificate acceptance to LB_N(T_N).

## Falsifiers

- explicit residual falsifier: a circuit D_N and explicit bad row list R_N with |D_N|+aN|R_N|<N^{1+epsilon-o(1)} invalidates any claimed direct source lower bound.
- positive-beta falsifier: any repaired carrier with target query length N^beta for beta>0 reintroduces the q+beta*c transfer cap.
- occurrence-oracle falsifier: a row-local certificate touching B_N<N^{epsilon-o(1)} rows is compatible with an easy occurrence-label carrier.
- functional-density falsifier: a dense constructive certificate property over label tables becomes a natural-property route unless it is nonlarge, nonconstructive, or nonfunctional.
- advice-leakage falsifier: uncharged generator, proof, or row-selection advice can hide the residual repair below the recorded threshold.
- target-equivalence falsifier: a direct EF proof of LB_N(T_N) may already encode the desired SAT lower bound, so it is not a weak-source magnification achievement.

## Learning

Cycle 77 sharpens the EF+SAT_U packet: direct lower-bound certificates automatically pass the explicit row-residual audit, so the real gap is not patching but semantic extraction. A new occurrence-oracle row-touch no-go gives a concrete falsifier for relativizing local certificate methods and leaves only SAT-semantic nonrelativizing, nonlarge/nonconstructive, or direct routes alive.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The abstract EF+SAT_U soundness claim is too weak; varying row-touch in an occurrence-label relaxation directly tests whether the certificate route is merely local and relativizing.
- Situation seed: Occurrence-oracle EF+SAT_U transcript for the beta-zero XOR carrier H_N^Y(x)=xor_{j<=M_N}Y_{x,j}, with the verifier allowed to mention only a bounded set of source rows and generated occurrences.
- Varied variable: theta where the certificate touches B_N=N^theta source rows.
- Held-fixed controls: L_N=(log N)^d and beta=0, so SAT circuit substitution remains N^{o(1)} per query., M_N<=N^{q+o(1)} and generator overhead N^{rho+o(1)} with max{rho,q}<1+epsilon., Nonuniform equality-patching cost aN per exceptional row is charged., The verifier transcript and any certificate advice are included in the source-size budget.
- Expected observation: For theta<epsilon, an accepting occurrence-label extension can make H_N^Y zero outside touched rows and then patch touched rows in O(N^{1+theta}) gates, below the claimed N^{1+epsilon} lower-bound threshold. For theta>=epsilon the patching falsifier no longer yields a subthreshold contradiction.
- Transfer certificate needed: A formal bridge showing that the actual EF+SAT_U certificates under study are row-touch occurrence-relativizing, or a counter-certificate proving that they exploit nonrelativizing SAT-realization constraints strongly enough to imply LB_N(T_N).

## Next Experiment

Instantiate Touch(Pi) for a concrete EF+SAT_U encoding of circuit lower-bound certificates: count whether proofs of size N^k can mention sub-N^epsilon rows, and test if formula-equality/SAT-realization axioms break the occurrence-oracle extension.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Logarithmic cluster projection plus logarithmic projection-decision width turns a proof-mediated beta-zero XOR certificate into a valid natural property exactly when DirectClusterSound(C,k) holds. Ordinary proof soundness or local consistency cannot replace DirectClusterSound; odd-charge Tseitin supplies the falsifier.

## Definitions

- source object: A beta-zero XOR certificate family Cert_N for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N<=N^{q+o(1)}, L_N=(log N)^d, and a local verifier V_N querying target truth-table bits and proof bits.
- target object: The target class C_k(N)=nonuniform Boolean circuits of size at most N^k computing N-row truth tables, with the route aiming only to certify a lower-bound transfer obstruction, not P != NP.
- controlled interface: A verifier-view cluster C, its target projection U(C), its proof-view CSP, and DirectClusterSound(C,k): no T in TT(C_k(N)) lies in the existential cluster shadow.
- target-preserving condition: The cluster C is uniformly or advice-free selected, |U(C)|=O(log N), the proof-view CSP has decision width O(log N), and substituting a small target circuit uses no residual row advice beyond the audited patching bound.

## Assumptions

- Model: nonuniform circuit lower bounds over N-bit truth tables, with constructivity measured in poly(N) time given the full table T.
- Uniformity: C_N and all local predicates of V_N are computable in poly(N); if C_N is selected from a proof, its description must be searchable without target-circuit advice.
- Naturalness regime: largeness is measured under the uniform distribution on truth tables T in {0,1}^N; usefulness is exact exclusion of TT(C_k(N)).
- Same-theory condition: DirectClusterSound is stated for the same local verifier, same target class, and same N-to-L_N length map as the beta-zero XOR carrier.

## Equations

- cluster_shadow: `\operatorname{Sh}(C)=\{T\in\{0,1\}^N:\exists \tau\ \forall v\in C\ V_v(T|_{U_v},\tau|_{P_v})=1\}`. Valid when: Valid when C is a fixed uniformly generated cluster and each local view reads only the named target and proof coordinates.
- density_from_log_projection: `\mu(\operatorname{Sh}(C))\ge 2^{-|U(C)|}\ge N^{-a}\quad\text{if } |U(C)|\le a\log_2 N`. Valid when: Applies after an accepting H_N^SAT transcript fixes one proof-view assignment and the cluster projection has logarithmic size.
- constructivity_from_width: `\operatorname{Time}(1_{\operatorname{Sh}(C)})\le N^{O(1)}2^{O(d_C)}`. Valid when: Requires uniform cluster descriptions and logarithmic projection-decision width for the existential proof-view CSP.
- usefulness_equals_direct_soundness: `\operatorname{Sh}(C)\cap TT(C_k(N))=\varnothing`. Valid when: Requires DirectClusterSound for the exact target class and forbids nonuniform residual row advice.

## Attempted Derivation

- Define Sh(C) as the existential set of truth tables whose target bits and some cluster proof-view assignment make all views in C accept.
- Because H_N^SAT has an accepting transcript on C, fixing that proof-view assignment shows every table agreeing with H_N^SAT on U(C) is in Sh(C); logarithmic |U(C)| gives polynomial density without computing H_N^SAT bits.
- If the proof-view CSP has logarithmic decision width, membership in Sh(C) is decidable in poly(N) by enumerating or dynamic-programming over the cluster proof variables.
- DirectClusterSound(C,k) is exactly the statement that Sh(C) excludes every truth table computed by a size-N^k circuit; hence Sh(C) is large, constructive, and useful.
- Trying to replace DirectClusterSound by ordinary Psys soundness fails: an odd-charge Tseitin layer is globally inconsistent but every proper logarithmic cluster is locally satisfiable, so the cluster shadow may contain all truth tables.
- The sparse residual patching inequality gives a second falsifier: if cluster or row advice identifies fewer than N^epsilon residual rows below the claimed exponent, a small D_N can be patched into a full circuit for H_N^SAT.

Blocking gap: No named proof system has yet supplied DirectClusterSound(C,k) at logarithmic target projection without either naturalizing or adding nonlocal advice/checks.

## Falsifiers

- Odd-charge Tseitin embedded in the proof-view layer: all logarithmic clusters are locally satisfiable while the global certificate obligation is false.
- Sparse residual leakage: D_N plus hardwired residual rows gives C(H_N^SAT)<=S_D+O(|R_N|N), contradicting a subthreshold lower-bound claim.
- Nonconstructive cluster selection: if C_N is chosen using hidden proof or target-circuit advice, the natural-property conclusion is invalid but the route loses a clean target-preserving interface.
- H_N-bit computability trap: a direct H-cylinder may not be poly(N)-constructive when L_N=(log N)^d; the valid naturalization must use the existential cluster shadow instead.
- PRF natural-proofs pressure: a large poly(N)-constructive property useful against C_k(N) conflicts with pseudorandom functions secure for the same circuit scale.

## Learning

Cycle 77 isolates the exact support-branch fork: logarithmic proof-mediated clusters naturalize through the existential shadow if DirectClusterSound holds, while odd-charge Tseitin shows ordinary soundness gives density without usefulness. The sparse residual inequality remains an independent falsifier for advice leakage. This is valid route-level certification work, not progress on P != NP itself.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for ordinary-soundness-based beta-zero certificates.`
- Rationale: The branch needs a concrete target-preserving test separating DirectClusterSound from local proof soundness; another abstract barrier restatement would not decide the proof queue.
- Situation seed: Embed an odd-charge Tseitin parity instance on a bounded-degree expander as the proof-view consistency layer of a beta-zero XOR local certificate, and connect target truth-table queries through dummy SAT projections so target bits do not affect local parity satisfiability.
- Varied variable: The projected target width w=|U(C)|, varied from c log N to superlogarithmic while keeping the proof-view cluster locally satisfiable.
- Held-fixed controls: beta=0 XOR carrier with M_N<=N^{q+o(1)} and L_N=(log N)^d, target class C_k(N)=SIZE(N^k) with no advice leakage, uniform cluster descriptions and poly(N)-decidable local predicates, same nonuniform circuit basis for generator, SAT substitutions, and patching circuits
- Expected observation: For w=O(log N), the cluster shadow has polynomial density and can be made all of {0,1}^N under the Tseitin dummy projection; ordinary soundness therefore gives no usefulness, while DirectClusterSound would have to insert a nonlocal checksum or semantic small-circuit exclusion.
- Transfer certificate needed: A formal embedding theorem for the named Psys showing either that every logarithmic cluster contains a target-preserving DirectClusterSound check, or that the odd-charge Tseitin construction realizes the no-go without changing C_k(N), rho, q, or residual patching thresholds.

## Next Experiment

Instantiate Psys as a locally checkable resolution or PCR refutation certificate for the beta-zero XOR lower-bound claim; build the odd-charge Tseitin proof-view layer, compute |U(C)| and decision width, and decide whether Sh(C)=all truth tables or DirectClusterSound(C,k) can be enforced without superlogarithmic projection.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For beta-zero XOR H_N^SAT, any accepted MCSP/MKtP certificate with SAT-semantic adaptive-cover exponent alpha_ad and row residual N^r gives C(H_N^SAT)<=N^{max{rho,q+alpha_ad,r+1}+o(1)}. This is a valid falsifier for any stronger theta lower-bound claim.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N<=N^{q+o(1)} and query length L_N=(log N)^d.
- target object: unrestricted nonuniform Boolean circuits for the row-encoded function H_N^SAT, with claimed lower-bound threshold N^theta.
- controlled interface: an MCSP/MKtP-style Psys certificate pi_N inducing SAT-label openings b_pi(x,j) via an adaptive cover and leaving residual row set R_N.
- target-preserving condition: b_pi(x,j)=SAT(G_N(x,j)) off R_N, G_N is uniform with overhead N^rho, and positive extraction never uses nonuniform selectors.

## Assumptions

- Source model is beta=0: SAT query length is polylogarithmic and no hidden N^beta substitution cost is charged.
- Psys is named, e.g. DirectClusterSound-style MCSP labels; for an upper bound, a fixed accepted pi_N may be hardwired per length.
- The adaptive cover has level data (tau,a_l,mu_l,omega_l) and opens each queried label with unrestricted circuits of exponent alpha_ad.
- Residual rows satisfy |R_N|<=N^{r+o(1)} and the covered approximation D_N agrees with H_N^SAT outside R_N.
- The theta claim is in the same unrestricted nonuniform circuit model, so comparing exponents is valid.

## Equations

- adaptive_cover_cap: `\alpha_{ad}=\max\{\tau,\max_l(a_l+\mu_l),\max_l\omega_l\}`. Valid when: Valid when the certificate-opening process is represented by the named adaptive-cover profile with transcript, summary, and opener exponents recorded.
- covered_xor_upper_bound: `C(D_N)\le N^{\rho+o(1)}+M_N N^{\alpha_{ad}+o(1)}=N^{\max\{\rho,q+\alpha_{ad}\}+o(1)}`. Valid when: Applies after a fixed accepted certificate is hardwired and every generated SAT label is supplied by the adaptive cover.
- residual_corrected_bound: `C(H_N^{SAT})\le C(D_N)+O(|R_N|N)=N^{\max\{\rho,q+\alpha_{ad},r+1\}+o(1)}`. Valid when: Requires that D_N and H_N^SAT differ only on the declared row residual set of size N^{r+o(1)}.

## Attempted Derivation

- Fix an accepted certificate pi_N. Since the contradiction target is nonuniform circuit size, pi_N, its rank choices, and its adaptive policy can be hardwired; no advice-free selector is needed for the no-go.
- Flatten the adaptive cover: transcript cost tau, summaries a_l+mu_l, and openers omega_l give label circuits of size N^{alpha_ad+o(1)} for b_pi(x,j).
- Compute G_N and XOR all M_N<=N^{q+o(1)} covered labels, giving D_N with exponent max{rho,q+alpha_ad}.
- If D_N agrees with H_N^SAT outside |R_N|<=N^{r+o(1)} residual rows, add a sparse row correction of cost O(|R_N|N), yielding the stated upper bound.

Blocking gap: The remaining formal gap is semantic binding for a named Psys: local consistency must imply b_pi(x,j)=SAT(G_N(x,j)) outside R_N, not merely an internal certificate label.

## Falsifiers

- falsifier: a DirectClusterSound certificate with alpha_ad<theta-q and r<theta-1 yields a valid circuit upper bound below the claimed theta threshold.
- falsifier: accepted labels are only proof-local and not SAT-semantic, so the controlled interface to H_N^SAT is absent.
- falsifier: residual rows with r+1>=theta collapse the sparse-row correction threshold and erase the intended lower bound.
- falsifier: positive extraction uses advice-selected hard rows; this invalidates E-language transfer even though the no-go hardwiring remains valid.

## Learning

Cycle 77 strengthens the beta-zero XOR audit: selector advice is irrelevant for the negative direction because a fixed low-cover certificate can be hardwired. The decisive validation task is SAT-semantic binding plus residual accounting for one named Psys.

## Gedanken Experiment Design Seed

- Need decision: `design-now as a falsifier probe`
- Rationale: The alpha_ad formula is already abstract; the branch needs one concrete beta-zero carrier to test whether low-cover certificates actually imply the row-residual circuit upper bound.
- Situation seed: For each N, use padded SAT-query generator G_N and a DirectClusterSound-style MCSP label certificate pi_N for H_N^SAT, allowing a declared residual row set R_N.
- Varied variable: adaptive cover exponent alpha_ad, varied by changing the block-summary exponent lambda while q, rho, r, and theta are fixed.
- Held-fixed controls: M_N<=N^{q+o(1)} and L_N=(log N)^d., The target model is unrestricted nonuniform circuits for H_N^SAT., Semantic label soundness holds outside the declared residual rows., Residual correction cost is charged as O(|R_N|N).
- Expected observation: When alpha_ad crosses theta-q, the constructed circuit crosses the claimed lower-bound threshold; below it the carrier is refuted, above it no positive lower bound follows.
- Transfer certificate needed: A formal flattening lemma from pi_N adaptive openings to label circuits plus a semantic certificate that D_N equals H_N^SAT outside R_N.

## Next Experiment

Instantiate DirectClusterSound(C,k): define b_pi(x,j), compute its adaptive-cover profile, prove or refute SAT-semantic binding, and check whether max{rho,q+alpha_ad,r+1}<theta.
