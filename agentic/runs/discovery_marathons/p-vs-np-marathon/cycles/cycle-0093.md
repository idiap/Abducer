# cycle-0093

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Conditional theorem: for Psys_h^un=EF+SATeq+bounded-SR_h proofs of LB_N(s), if an advice-free normal-support parser NSP_N maps each nonfunctional accepted proof pi to a charged transcript with support exponent sigma, SR leaf count exponent q+eta, leaf-solver exponent tau, and residual row error E_N=N^{delta+o(1)}, then max{rho,sigma,q+eta+tau,1+delta}<1+epsilon is a valid falsifier for the claimed source lower bound C(H_N^SAT)>N^{1+epsilon-o(1)}. Hence any proof-mediated escape must functional-naturalize, force a superthreshold charged transcript, or use SAT semantics outside NSP_N.

## Definitions

- source object: a concrete Psys_h^un proof pi of the propositional lower-bound sentence LB_N(s_N) asserting Ckt(H_N^SAT)>s_N for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)).
- target object: the target-preserving consequence SAT notin P/poly obtained from the beta-zero substitution bridge when C(H_N^SAT)>N^{1+epsilon-o(1)} and q,rho<1+epsilon.
- controlled interface: an advice-free parser NSP_N(pi,G_N) producing declared row supports, bounded self-reduction leaves, leaf solvers, and a residual row set R_pi from a nonfunctional proof certificate.
- target-preserving condition: L_N=(log N)^d with d>1, M_N<=N^{q+o(1)}, generator size N^{rho+o(1)}, beta=0, q,rho<1+epsilon, and no parser advice depending on SAT labels or H_N truth table.
- Psys_h^un: extended Frege over source variables x, extension variables e_i<->phi_i, formula equality axioms SAT(u)=SAT(v) for syntactic EqSAT_N pairs, and self-reduction OR axioms expanded to depth at most h.
- functional proof branch: acceptance of pi induces a truth-table property over the SAT-label vector on U_N, constructive in 2^{O(L_N)} and dense enough to trigger the route-specific naturalization audit.
- NSP_N transcript cost: S_supp + K_N T_leaf + O(E_N N), where S_supp=N^{sigma+o(1)}, K_N=N^{q+eta+o(1)}, T_leaf=N^{tau+o(1)}, and E_N=|R_pi|.

## Assumptions

- Source circuits are nonuniform Boolean circuits over N-bit x; the lower bound is scalar Ckt(H_N^SAT)>N^{1+epsilon-o(1)}, not a lower bound for SAT itself.
- Target circuits for SAT at length L_N are nonuniform of size L_N^c for an arbitrary fixed c; beta=0 because L_N is polylogarithmic in N.
- The parser is uniform/advice-free relative to pi and the generator description, and it may not hardwire the SAT label vector, the H_N truth table, or the residual row set unless charged.
- Bounded-SR leaves are formulas of length L_N^{O(1)} whose labels are either solved by explicit leaf circuits or charged as residual rows.
- The nonfunctional branch excludes dense functional label properties; otherwise the certificate is routed to the naturalization obstruction rather than to the row-residual audit.
- The theorem is conditional on NSP_N for unrestricted extension variables; without NSP_N it remains a restricted support-declared theorem and a named open proof obligation.

## Equations

- beta_zero_substitution: `C(H_N^{SAT}) \le N^{\rho+o(1)}+N^{q+o(1)}L_N^c=N^{\max\{\rho,q\}+o(1)}`. Valid when: Valid when SAT has nonuniform circuits of size n^c, the generator has size N^{rho+o(1)}, M_N<=N^{q+o(1)}, and all queries have length L_N=(log N)^d.
- row_residual_patching: `C(H_N^{SAT}) \le S_D+O(|R_N|\,N)`. Valid when: Valid when a circuit D_N agrees with H_N^{SAT} outside an explicit residual row set R_N and equality tests on N-bit source rows are allowed nonuniformly.
- parsed_transcript_upper_bound: `C(H_N^{SAT}) \le N^{\rho+o(1)}+S_{supp}+K_NT_{leaf}+O(E_NN)`. Valid when: Valid when NSP_N outputs charged support of size S_supp, K_N bounded-SR leaves each solved with circuits of size T_leaf, and only E_N rows remain unparsed.
- subthreshold_falsifier_window: `\max\{\rho,\sigma,q+\eta+\tau,1+\delta\}<1+\epsilon \Rightarrow C(H_N^{SAT})<N^{1+\epsilon-o(1)}`. Valid when: Valid when S_supp=N^{sigma+o(1)}, K_N=N^{q+eta+o(1)}, T_leaf=N^{tau+o(1)}, E_N=N^{delta+o(1)}, and polylogarithmic overheads are absorbed into o(1).

## Attempted Derivation

- Fixed proof system Psys_h^un: EF plus extension axioms, EqSAT_N formula-equality axioms, and bounded self-reduction OR axioms to depth h for generated SAT instances of length L_N=(log N)^d.
- Encoded the source sentence LB_N(s_N) as the propositional assertion that every size-s_N circuit differs from H_N^SAT on some source row; s_N=N^{1+epsilon-o(1)}.
- Separated accepted proofs into a functional branch and a nonfunctional branch. The functional branch induces a constructive label property and is routed to the beta-zero naturalization audit.
- For the nonfunctional branch, assumed NSP_N produces a support transcript Q_pi, K_N bounded-SR leaves, leaf solvers of size T_leaf, and residual row set R_pi, all advice-free from pi and G_N.
- Built a circuit D_N that evaluates G_N, follows the parsed support transcript, invokes leaf solvers on charged SR leaves, and agrees with H_N^SAT outside R_pi.
- Applied equality patching to R_pi, yielding C(H_N^SAT)<=N^{rho+o(1)}+S_supp+K_NT_leaf+O(|R_pi|N).
- Concluded that any transcript below the exponent window max{rho,sigma,q+eta+tau,1+delta}<1+epsilon contradicts the source lower-bound claim, so a valid proof-mediated certificate must force a superthreshold transcript or escape NSP_N.
- Tried to prove NSP_N for arbitrary EF extension variables by inducting on extension definitions. The induction fails when an extension variable aggregates row-dependent SAT-semantic information through phi_i without a declared support summary.

Blocking gap: NSP_N: an advice-free normal-support parser for unrestricted EF+SATeq+SR_h extension variables. The missing lemma must extract charged row supports and bounded-SR leaves from arbitrary extension definitions without SAT-label advice and without solving a target-equivalent semantic support problem.

## Falsifiers

- Subthreshold support-declared transcript with max{rho,sigma,q+eta+tau,1+delta}<1+epsilon is a direct falsifier for the claimed N^{1+epsilon} source lower bound.
- A dense 2^{O(L_N)}-constructive functional label property is a naturalization falsifier for proof-mediated beta-zero certificates unless nonlargeness or nonconstructivity is proved.
- An extension variable whose affected rows are not advice-free support-transparent is a falsifier for occurrence-only parser claims about unrestricted EF+SATeq+SR_h.
- Positive target-query exponent beta>0 remains a separate transfer falsifier: q+beta c caps all-exponent SAT lower-bound consequences.
- Low constrained row-parity distance after EqSAT/SR quotienting is a falsifier because sparse residual rows can be equality patched below threshold.

## Learning

Cycle 93 upgrades the formula-semantic extraction fork by naming NSP_N as a support-transparency lemma for unrestricted EF extension variables and proving the conditional transcript falsifier around it. The valid restricted contribution is support-declared EF+SATeq+bounded-SR_h: any subthreshold parsed transcript collapses LB_N by a small circuit plus sparse-row patching. The full EF+SAT claim remains blocked exactly at advice-free extraction of extension-variable support, not at generic soundness or barrier folklore.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The full proof-system fork is blocked at NSP_N, so a concrete target-preserving thought experiment tests whether hidden EF extension support is a real obstruction or merely a bookkeeping defect.
- Situation seed: Take the beta-zero parity carrier H_N^SAT with L_N=(log N)^d and q,rho<1+epsilon. Add to Psys_h^un one EF extension variable e_R(x) computing a row mask for a sparse set R_N of source rows, and allow the proof to branch on e_R before invoking bounded SR facts on generated formulas.
- Varied variable: delta where |R_N|=N^{delta+o(1)}, with delta varied across the patching threshold epsilon.
- Held-fixed controls: M_N=N^{q+o(1)} and generator size N^{rho+o(1)} stay below N^{1+epsilon}., SAT query length remains beta-zero: L_N=(log N)^d with d>1., The parser is not allowed SAT-label advice or the H_N truth table., The target statement remains the same beta-zero implication to SAT notin P/poly if the source lower bound were valid.
- Expected observation: For delta<epsilon, any proof dependence on e_R that is not charged by NSP_N can be simulated by a subthreshold residual patch, so a claimed source certificate is invalid. For delta>=epsilon, the row mask is too expensive to patch and may represent genuine row forcing.
- Transfer certificate needed: An advice-free support-transparency theorem mapping every EF extension definition to charged row support plus bounded-SR leaves, or a countermodel proving that such extraction would require target-equivalent SAT semantic information.

## Next Experiment

Attempt an explicit NSP_N countermodel for unrestricted EF extension variables: construct a small row-mask extension family e_R, prove that occurrence-only parsing misses its support, and decide whether support transparency can be repaired by charging C(Supp(e_R)) without making the parser target-equivalent.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

In EF+SAT_U^subst, a parser that charges only displayed SAT_U occurrences is not row-faithful for the beta-zero XOR carrier once the proof may introduce a row-selector extension E_N(x,z)=G_N(x,z). One displayed atom SAT_U(E_N(x,z)) has semantic row range [M_N], so any valid extractor must charge the whole index-expanded range or name a separate SAT-semantic escape.

## Definitions

- source object: a poly(N)-size EF+SAT_U^subst proof pi of LB_N: C(H_N^SAT)>N^{1+epsilon-o(1)}, where H_N^SAT(x)=XOR_{j<=M_N} SAT(G_N(x,j)).
- target object: a row transcript Q_pi or semantic support K_pi used to naturalize accepted certificates or force residual row charge.
- controlled interface: uniform no-advice extraction from proof syntax to row support, with SAT_U atoms interpreted by actual formula semantics rather than displayed occurrence labels.
- target-preserving condition: replacing uncharged rows by a spoof table D_N preserves every proof-visible SAT-semantic fact used by pi and gives C(H_N^SAT)<=C(D_N)+O(|K_pi|N).
- displayed occurrence support OccRows(pi) counts only literal row constants appearing inside SAT_U atoms.
- index-expanded semantic support K_idx(pi) is the union of all j such that some SAT_U atom in pi contains an extension term semantically equal to G_N(.,j) under an allowed row-index assignment.

## Assumptions

- Proof model: EF with extension variables and SAT_U atoms closed under substitution of extension terms; SAT_U(A) asserts satisfiability of the formula encoded by A.
- Length regime: N=2^n, M_N<=N^{q+o(1)}, L_N=(log N)^d, generator size N^{rho+o(1)}, and q,rho<1+epsilon.
- Extractor model: the parser is uniform poly(N)-time and carries no advice depending on the SAT truth table.
- Row-selector availability: an extension term E_N(x,z) of size N^{rho+o(1)} outputs G_N(x,z) for every z in [M_N].
- Occurrence parser limitation: a displayed SAT_U occurrence without a literal row constant is charged as O(1) row tokens rather than expanded to its full row range.

## Equations

- beta_zero_xor_carrier: `H_N^{SAT}(x)=XOR_{j=1}^{M_N} SAT(G_N(x,j))`. Valid when: Valid when the beta-zero carrier uses polylogarithmic SAT instances generated uniformly from the input and row index.
- indexed_atom_range_gap: `Rows(SAT_U(E_N(x,z)))=[M_N] but OccRows(SAT_U(E_N(x,z)))=O(1)`. Valid when: Valid when the proof system permits an unfixed row-index extension term inside a SAT_U atom.
- sparse_residual_patching: `C(H_N^{SAT}) <= C(D_N)+O(|K|N)`. Valid when: Applies after D_N agrees with H_N^{SAT} off row set K and each residual row is hardwired as an N-bit function.
- forced_support_inequality: `C(D_N)+O(|K_idx(pi)|N) >= N^{1+epsilon-o(1)}`. Valid when: Requires the claimed source lower bound and a row-faithful spoof D_N preserving every proof-visible SAT semantic fact.

## Attempted Derivation

- Fixed the source statement as LB_N: C(H_N^SAT)>N^{1+epsilon-o(1)} in nonuniform Boolean circuits, with proof pi in EF+SAT_U^subst and beta-zero parameters N=2^n, L_N=(log N)^d, M_N<=N^{q+o(1)}, generator size N^{rho+o(1)}.
- Closed a quantitative validation obligation: row hardwiring gives C(H_N^SAT)<=M_N N^{1+o(1)}, so any proposed source lower bound at exponent 1+epsilon must satisfy q>=epsilon-o(1). This is a concrete falsifier for q<epsilon generator proposals.
- Tested the occurrence parser against the indexed substitution atom SAT_U(E_N(x,z)). The displayed occurrence count is O(1), but its semantic row range is [M_N]. Thus occurrence parsing is invalid for full EF+SAT_U^subst unless it expands indexed atoms.
- Repaired the invariant by defining K_idx(pi), the union of semantic row ranges of SAT_U atoms after allowed extension substitutions. This preserves the sparse-row patching form C(H)<=C(D)+O(|K_idx|N) if proof acceptance is local to K_idx.
- Derived the conditional dichotomy from SATSemanticLocality_N: small K_idx plus a low-complexity spoof D_N contradicts LB_N; large K_idx gives the forced-row branch; functional extraction gives the natural-property branch.
- Ran the barrier audit: functional dense constructive extraction is natural and valid only as a route obstruction, not as evidence for P != NP.

Blocking gap: SATSemanticLocality_N remains unproved for arbitrary EF+SAT_U^subst. A proof may use equisatisfiable SAT transformations, self-reductions, or row-mixing extension formulas whose semantic dependence on rows is not captured by K_idx unless the range-expansion algorithm is strengthened.

## Falsifiers

- q<epsilon row-enumeration falsifier: C(H_N^SAT)<=N^{1+q+o(1)} contradicts any claimed N^{1+epsilon-o(1)} source lower bound in the same nonuniform model.
- Indexed-substitution falsifier: one atom SAT_U(E_N(x,z)) syntactically has one occurrence but semantically ranges over all M_N rows.
- Row-mixer falsifier candidate: an equisatisfiable formula B_N(x,u) can encode a disjunction or selector over many rows, defeating naive K_idx unless range semantics are expanded.
- Odd-charge Tseitin falsifier remains active against replacing DirectClusterSound by ordinary local consistency.
- Functional-extraction falsifier: a dense poly(N)-constructive useful property for SIZE_N(N^{1+epsilon}) collides with the natural-proofs/PRF pressure unless nonlargeness or nonconstructivity is certified.

## Learning

Cycle 93 adds two non-repeated route-level facts. First, the source carrier itself has the nonuniform ceiling C(H_N^SAT)<=N^{1+q+o(1)}, so q>=epsilon-o(1) is mandatory for any claimed N^{1+epsilon} source lower bound. Second, full EF+SAT_U^subst cannot use occurrence support because indexed substitution is a finite falsifier; the valid invariant is index-expanded semantic support K_idx. The remaining proof gap is SATSemanticLocality_N, not generic barrier folklore and not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch has looped on abstract parser language; the concrete indexed-substitution case tests whether semantic support, not occurrence support, is the valid target-preserving invariant.
- Situation seed: Consider an EF+SAT_U^subst proof family containing a row-selector extension E_N(x,z)=G_N(x,z) and SAT atoms SAT_U(E_N(x,z)) where a cube constraint fixes h bits of the row index z. The source sentence is LB_N for H_N^SAT, and the spoof D_N changes only rows outside the expanded cube ranges.
- Varied variable: h, the number of fixed row-index bits exposed per SAT_U atom.
- Held-fixed controls: N=2^n, L_N=(log N)^d, M_N=N^{q+o(1)}, and generator size N^{rho+o(1)}., The target lower-bound threshold is C(H_N^SAT)>N^{1+epsilon-o(1)} against the same nonuniform SIZE_N model., The extractor is uniform, no-advice, and uses the same EF+SAT_U^subst syntax and SAT semantics., The spoof must preserve every proof-visible SAT-semantic fact on the expanded row ranges.
- Expected observation: With T_N such atoms, the expanded support is at most min(M_N,T_N M_N/2^h) in the regular cube case. If this support is below N^{epsilon-o(1)} and a spoof exists, sparse patching refutes the source lower bound; if h=0, occurrence parsing undercounts by a factor M_N.
- Transfer certificate needed: A formal SATSemanticLocality_N and exact range-counting certificate for extension terms. Without this certificate the experiment is only a falsifier probe and cannot enter the proof queue.

## Next Experiment

Instantiate the row-mixer falsifier in a minimal EF+SAT_U^subst fragment: define B_N(x,u) whose satisfying witnesses select j and encode G_N(x,j), compute its K_idx under the current range definition, and decide whether SATSemanticLocality_N expands it to all rows or fails.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Let P_uExt be a Cook-Reckhow proof system for beta-zero SAT-parity lower-bound certificates with ordinary syntactic rules, SAT_U facts, and an unwitnessed SAT-extensionality rule UExt. For every short proof pi_N about H_N^SAT, exactly one route-relevant disposition is valid: either all UExt uses are replaced by advice-free quotient witnesses of adaptive cover exponent alpha_U, giving the upper-bound falsifier C(H_N^SAT)<=N^{max{rho,q+alpha_U,max{f,r}+1}+o(1)}, or pi_N is a semantic-oracle carrier outside the controlled MCSP/MKtP interface and cannot be promoted as advice-free row-hardness evidence.

## Definitions

- source object: a concrete P_uExt proof pi_N or certificate transcript for a lower-bound statement about H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)).
- target object: either an occurrence transcript/quotient witness usable to build circuits for H_N^SAT, or an advice-free row-hardness certificate in the intended nonuniform circuit model.
- controlled interface: MCSP/MKtP or proof-certificate information may affect the target only through forced rows, quotient witnesses, residual rows, and the uniform generator overhead rho.
- target-preserving condition: every semantic formula-identity step must be made advice-free by a quotient witness with measured adaptive cover exponent alpha_U; otherwise the step is quarantined as a semantic-oracle rule, not as P vs NP progress.
- UExtWitnessability(pi_N,alpha_U) means that each unwitnessed extensionality invocation in pi_N is accompanied by a uniform quotient/opening transcript whose adaptive cover exponent is at most alpha_U.
- f is the exponent for semantically forced rows; r is the exponent for sparse residual rows requiring direct truth-table patching.

## Assumptions

- Length regime: N is the truth-table input length for H_N^SAT, M_N<=N^{q+o(1)}, and every SAT query has polylogarithmic length L_N=(log N)^d.
- Circuit model: C(H_N^SAT) is unrestricted nonuniform Boolean circuit size as a function of N; proof text and low-cover witnesses may be hardwired when deriving an upper-bound falsifier.
- Proof model: P_uExt contains syntactic Cook-Reckhow inference, explicit SAT_U facts, witnessed extension-variable definitions, and a UExt rule whose side condition is semantic equality of SAT formulas but whose proof line need not include a quotient witness.
- Uniformity/advice status: the extractor from pi_N to quotient witnesses must be advice-free and computable from the proof object and N; nonuniform choice of hard rows is not a valid target-preserving transfer.
- Barrier status: the witnessed branch is a finite low-cover falsifier, while the unwitnessed branch is nonrelativizing and semantic; it is not covered by occurrence-relativizing parser arguments until a witnessability lemma is proved.
- Non-claim: the dichotomy neither proves P != NP nor proves that P_uExt lacks short semantic proofs; it only classifies which proof objects remain inside the route interface.

## Equations

- beta_zero_carrier: `H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), M_N<=N^{q+o(1)}, |G_N(x,j)|<=(log N)^d`. Valid when: Valid when the source lower-bound model is the beta-zero SAT-parity carrier with uniform generator G_N and fixed query exponent q.
- adaptive_quotient_cover: `alpha_U=max{tau,max_l(a_l+mu_l),max_l omega_l}`. Valid when: Valid when quotient witnesses are represented by adaptive transcript layers with verifier time tau, summary exponents a_l+mu_l, and opener exponents omega_l.
- witnessed_extensionality_upper_bound: `C(H_N^SAT)<=N^{max{rho,q+alpha_U,max{f,r}+1}+o(1)}`. Valid when: Valid when every UExt step is replaced by an advice-free quotient witness and residual or forced rows are patched by direct row truth tables.
- lower_bound_falsifier_threshold: `max{rho,q+alpha_U,max{f,r}+1}<1+epsilon => not(C(H_N^SAT)>N^{1+epsilon-o(1)})`. Valid when: Valid when the target claim is an unrestricted nonuniform lower bound for the same H_N^SAT family and the circuit construction preserves all parameters.

## Attempted Derivation

- Fix the beta-zero carrier H_N^SAT with query exponent q and generator circuit exponent rho.
- Define P_uExt as P_wExt plus a UExt rule whose side condition is semantic SAT-extensionality but whose line contains no quotient witness.
- Run transcript induction over pi_N. Syntactic and witnessed rules preserve the occurrence transcript and update alpha_U by the adaptive-cover maximum.
- At a UExt(F,F') line, the induction needs a map identifying occurrences or semantic subformulas of F and F'. Without such a map, row parity is not invariant under private completions of unqueried occurrences.
- If an advice-free extractor supplies the missing quotient witnesses, charge their adaptive cover alpha_U and invoke the sparse-row residual circuit construction, yielding C(H_N^SAT)<=N^{max{rho,q+alpha_U,max{f,r}+1}+o(1)}.
- If no extractor supplies witnesses, the proof relies on a semantic equality oracle. The object may be sound in P_uExt but is not a valid MCSP/MKtP carrier transfer to an advice-free row-hard language.
- Thus the live packet source_statement is the P_uExt proof pi_N; the target_statement is either the low-cover upper-bound falsifier or a quarantine of semantic-oracle UExt; model_context is unrestricted circuits plus Cook-Reckhow proof syntax; reduction type is parser-to-query followed by row-residual simulation.

Blocking gap: Named gap UExtWitnessability: prove or refute that every short semantic-extensionality proof about H_N^SAT has advice-free quotient witnesses with alpha_U below the claimed lower-bound margin.

## Falsifiers

- Low alpha_U witnessed extensionality is a falsifier for any claimed beta-zero lower bound above max{rho,q+alpha_U,max{f,r}+1}.
- A UExt proof whose semantic equality lines lack advice-free quotient witnesses is a falsifier for controlled-interface promotion, not evidence for MCSP row hardness.
- Private-row spoofing in the occurrence-completion model falsifies parsers that treat unwitnessed formula identity as local occurrence information.
- A nonuniform selector for hard rows or quotient representatives falsifies the target-preserving uniformity requirement.
- Sparse residual sets of size N^{r+o(1)} falsify claimed lower bounds whenever r+1 is below the asserted exponent.

## Learning

Cycle 93 converts the remaining formula-semantic fork into a sharper theorem packet: witnessed extensionality is not a loophole but a charged adaptive-cover upper-bound falsifier, while unwitnessed SAT-extensionality is a named semantic-oracle rule unless UExtWitnessability is proved. The valid progress is a route-specific no-go/escape classification, not a proof of P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design now as a concrete falsifier probe`
- Rationale: The top proof-delivery gap is no longer whether witnessed identity is chargeable; it is whether unwitnessed SAT-extensionality can be parsed without smuggling semantic advice.
- Situation seed: Construct a padded SAT-parity family where G_N emits pairs (F_j,Pad_t(F_j)) that are extensionally equivalent but occurrence-disjoint, and let a P_uExt proof cancel the paired contributions using UExt rather than explicit padding witnesses.
- Varied variable: adaptive quotient-cover exponent alpha_U, with alpha_U=infinity representing a purely unwitnessed semantic extensionality rule
- Held-fixed controls: M_N=N^{q+o(1)} and L_N=(log N)^d for the beta-zero carrier., Generator overhead rho and the same target function H_N^SAT are held fixed., No advice is allowed in extracting quotient witnesses or row selectors., The target circuit model remains unrestricted nonuniform size C(H_N^SAT).
- Expected observation: Finite alpha_U below the threshold yields the explicit upper-bound falsifier; alpha_U=infinity makes the occurrence parser fail by two completions agreeing on queried occurrences but disagreeing on the semantic equality side condition.
- Transfer certificate needed: An advice-free quotient-witness extractor from pi_N, with measured adaptive cover profile and a proof that substituting witnesses preserves SAT semantics, forced-row counts, and sparse residual accounting.

## Next Experiment

Instantiate P_uExt^pad on the paired formulas (F_j,Pad_t(F_j)); write the rule table, prove the private-completion no-parser lemma, and compute the smallest alpha_U for explicit padding witnesses.
