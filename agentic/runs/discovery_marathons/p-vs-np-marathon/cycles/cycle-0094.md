# cycle-0094

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For the beta-zero SAT parity carrier, the support-declaration hypothesis can be removed for bit-explicit EF+SATeq+bounded-SR_h: transitive traversal of extension definitions gives an advice-free transcript. If its charged dependency, bounded-SR leaf solving, and sparse-row residual patching cost is below N^{1+epsilon-o(1)}, then the claimed source lower bound LB_N is false. Thus any valid proof-mediated lower-bound certificate in this fragment must pay superthreshold charge, naturalize functionally, or leave this fragment.

## Definitions

- source object: beta-zero SAT parity carrier H_N^SAT on N source rows, H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, L_N=(log N)^d, and generator circuit size N^{rho+o(1)}.
- target object: target-preserving consequence SAT notin P/poly obtained by substituting hypothetical polynomial-size SAT circuits into all polylogarithmic generated queries.
- controlled interface: bit-explicit EF+SATeq+bounded-SR_h proofs whose extension variables are definitional Boolean DAGs over concrete row-label atoms A_{x,j} and declared bounded self-reduction leaves.
- target-preserving condition: q,rho<1+epsilon, L_N=(log N)^d with d>1, no nonuniform advice beyond the size-N circuit/proof being audited, and every subthreshold parsed transcript must produce an actual circuit for H_N^SAT.
- bridge observable: Dep^*(pi) is the transitive set of concrete SAT-label atoms, EqSAT links, SR leaves, and residual source rows reachable from the proof DAG of pi.

## Assumptions

- Source model is nonuniform Boolean circuits for the length-N truth-table function H_N^SAT; LB_N(1+epsilon) means C(H_N^SAT)>N^{1+epsilon-o(1)}.
- Psys_bEF syntax explicitly lists every extension definition and every concrete SAT atom; the parser traverses the proof DAG and receives no semantic advice string.
- Bounded self-reduction depth h_N has at most N^{eta+o(1)} leaves per generated query, and the promised leaf solver has circuit size N^{tau+o(1)} on the generated leaf range.
- Residual row set R_N has size E_N and is patchable by equality tests of cost O(E_N N); this is a nonuniform source-circuit upper bound, not a target SAT circuit.
- Natural-proofs reasoning is invoked only for functional label certificates; this lemma handles nonfunctional bit-explicit transcripts and their row-residual falsifier.

## Equations

- carrier_definition: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad L_N=(\log N)^d`. Valid when: Valid when the carrier is evaluated on exactly N source rows and every generated SAT instance has length L_N=(log N)^d.
- beta_zero_substitution: `SAT\in SIZE(n^c)\Rightarrow C(H_N^{SAT})\le N^{\rho+o(1)}+M_N L_N^c=N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies after the target SAT circuit is substituted only into polylogarithmic generated queries and the generator overhead is N^{rho+o(1)}.
- parsed_charge: `\Gamma_{bEF}(\pi)=S_{dep}(\pi)+S_{link}(\pi)+N^{q+\eta+\tau+o(1)}+E_NN`. Valid when: Valid when the proof is bit-explicit, extension definitions are concrete DAG clauses, and bounded self-reduction leaves are declared by the parser.
- transcript_upper_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{bEF}(\pi)`. Valid when: Requires the transcript to compute H_N^SAT outside E_N rows and uses equality patches for the residual source rows.
- subthreshold_falsifier: `N^{\rho+o(1)}+\Gamma_{bEF}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Requires rho<1+epsilon and the transcript upper bound to be an actual nonuniform circuit for the source carrier.

## Attempted Derivation

- Fix Psys_bEF: EF extension variables are introduced only by explicit Boolean definitions over earlier variables and concrete SAT atoms A_{x,j}; SATeq and bounded-SR links are listed as concrete proof edges.
- Define Dep^*(pi) by reverse graph traversal from the lower-bound certificate conclusion through extension definitions, EqSAT links, SR leaves, and residual row declarations. This is advice-free and polynomial in the proof DAG size.
- From Dep^*(pi), build a circuit D_pi that evaluates the generator, all reached label predicates, bounded-SR leaf solvers, and the extension DAG. On rows outside R_N it agrees with H_N^SAT by the transcript soundness premise.
- Patch the E_N residual rows with equality tests, obtaining C(H_N^SAT)<=N^{rho+o(1)}+Gamma_bEF(pi). Therefore any subthreshold transcript is a concrete falsifier for LB_N(1+epsilon).
- Apply the independent beta-zero substitution audit: if SAT has L_N^c-size circuits for every fixed c, then H_N^SAT has N^{max{rho,q}+o(1)} circuits, so the target-preserving window remains q,rho<1+epsilon.
- Attempt to extend the parser to Psys_sym with FormulaEval-SAT comprehension. A single symbolic line can range over N M_N generated labels; surface occurrence support is no longer completion-sound under independent occurrence-label spoofing.
- Conclude that NSP_N is proved for bit-explicit EF+SATeq+bounded-SR_h, but full symbolic EF+SAT is blocked at a named semantic principle: succinct FormulaEval-SAT comprehension must be expanded, charged, or handled by a new nonrelativizing invariant.

Blocking gap: NSP_sym: an advice-free parser for succinct formula-indexed SAT atoms must either expand N^{1+q+o(1)} concrete row-index labels or prove a new semantic-support theorem that remains completion-sound without occurrence expansion.

## Falsifiers

- falsifier: a bit-explicit transcript with N^{rho+o(1)}+Gamma_bEF(pi)<N^{1+epsilon-o(1)} yields an actual small circuit for H_N^SAT and invalidates LB_N.
- falsifier: a sparse residual row set E_N<N^{epsilon-o(1)} is patchable by equality circuits of cost O(E_N N).
- falsifier: positive target-query exponent beta would reintroduce the transfer cap q+beta c and cannot support all-exponent P/poly exclusion.
- falsifier: a symbolic FormulaEval-SAT proof with only surface occurrence support refutes size-only parser soundness unless the parser charges the full row-index expansion.
- falsifier: a dense functional certificate triggers the naturalization side gate rather than providing a nonfunctional SAT-semantic escape.

## Learning

Cycle 94 closes a concrete support-transparency subcase: bit-explicit EF extension variables can be parsed without support declarations, giving a valid transcript falsifier theorem. The full formula-semantic extraction fork is now sharper: the obstruction is not arbitrary EF extension variables but succinct FormulaEval-SAT comprehension, which defeats size-only occurrence parsing unless its row-index expansion is charged.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch is blocked by whether formula-semantic proofs can hide row support inside symbolic generator comprehension; a concrete thought experiment tests the threshold between bit-explicit transcript falsifiers and genuine symbolic SAT-semantic escapes.
- Situation seed: Compare two accepted proof sketches for the same H_N^SAT: one bit-explicit EF+SATeq+bounded-SR_h proof listing concrete atoms A_{x,j}, and one Psys_sym proof using a single FormulaEval-SAT comprehension atom SAT(Eval(G_N,X,J)).
- Varied variable: theta=log_N R, where R is the number of concrete source rows that the parser must expand or force from the proof.
- Held-fixed controls: H_N^SAT remains beta-zero with L_N=(log N)^d, d>1, M_N=N^{q+o(1)}, and generator size N^{rho+o(1)}., The source lower-bound threshold remains C(H_N^SAT)>N^{1+epsilon-o(1)} in nonuniform general circuits., The target-preserving substitution window q,rho<1+epsilon is held fixed., No auxiliary nonuniform advice is allowed in the parser beyond the proof object and the fixed length N.
- Expected observation: For theta<epsilon, sparse-row patching gives a subthreshold falsifier. For theta near 1, symbolic comprehension may be completion-sound only after paying expansion above the row-patching window, isolating the SAT-semantic escape rather than proving a lower bound.
- Transfer certificate needed: A formal parser certificate showing that every accepted proof either expands at least N^{epsilon-o(1)} complete rows, induces a functional naturalizing label property, or supplies a new nonrelativizing semantic-support invariant for FormulaEval-SAT.

## Next Experiment

Formalize Psys_sym on finite length N: specify whether FormulaEval-SAT comprehension is a proof line, axiom schema, or extension rule; then prove either an expansion-charge parser with cost N^{1+q+o(1)} or a minimal countermodel showing surface occurrence completion is unsound.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Conditional support-density pressure lemma: in EF+SAT_U^subst, any short proof of C(H_N^SAT)>N^{1+epsilon-o(1)} that admits no-advice semantic residual extraction must have index-expanded semantic support |K_idx(pi)|>=N^{epsilon-o(1)}; moreover |K_idx(pi)|/M_N>=N^{epsilon-q-o(1)}. Thus q=epsilon+o(1) forces near-full semantic row charge, while q<epsilon-o(1) is a source-lower-bound falsifier.

## Definitions

- source object: beta-zero SAT parity carrier H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)) with generated SAT instances of length L_N=(log N)^d and row count M_N=N^{q+o(1)}.
- target object: fork-resolving extraction/no-go theorem for EF+SAT_U^subst proofs of the source lower bound C(H_N^SAT)>N^{1+epsilon-o(1)} against nonuniform Boolean circuits.
- controlled interface: no-advice semantic residual extraction pi -> (D_pi,K_idx(pi)) followed by sparse-row patching, q-density accounting, and naturalness audit.
- target-preserving condition: D_pi is computed uniformly from pi without advice, agrees with H_N^SAT after deleting rows outside K_idx(pi), and all circuit sizes, row counts, and generator overheads use the same N-parameter.
- semantic support K_idx(pi): the set of row indices whose SAT-value functions remain semantically indispensable after expanding indexed SAT substitutions and extension definitions in pi.
- residual circuit D_pi: a circuit produced from pi that computes the parity contribution of all rows outside K_idx(pi), not a witness chosen with nonuniform row advice.

## Assumptions

- Proof model: EF+SAT_U^subst is Extended Frege plus uniform SAT predicate axioms, with extension variables allowed inside SAT atoms; ordinary occurrence counts are not invariant under this substitution rule.
- Length regime: L_N=(log N)^d, M_N=N^{q+o(1)}, generator overhead at most N^{rho+o(1)}, and beta-zero substitution is measured before any claimed target transfer.
- Source regime: the asserted lower bound is C(H_N^SAT)>N^{1+epsilon-gamma_N} for gamma_N=o(1), with epsilon>0 fixed.
- Extraction regime: NoAdviceSemanticResidualExtractor_N returns D_pi of size S_D<=N^{1+epsilon-eta_N} and K_idx(pi), with eta_N>gamma_N on the tested margin.
- Uniformity/advice regime: the extractor may read pi and the uniform description of G_N but may not hardwire the deleted row set except through the explicit output K_idx(pi).
- Naturalness regime: if the extraction instead yields a dense poly(N)-constructive truth-table property useful against the same circuit class, the object is a valid natural-proof candidate and must face the PRF falsifier audit.

## Equations

- carrier_definition: `H_N^{SAT}(x)=\bigoplus_{j<M_N} SAT(G_N(x,j))`. Valid when: Valid when the branch convention fixes the outer length N, beta-zero SAT instance length L_N, and row index set before any proof extraction.
- row_count_regime: `M_N=N^{q+o(1)},\quad L_N=(\log N)^d`. Valid when: Valid when the generator family is fixed uniformly and the row count exponent q is measured in the same N parameter as circuit size.
- positive_beta_zero_transfer: `C(H_N^{SAT})\le N^{\rho+o(1)}+M_N L_N^c=N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies after the reduction preserves uniformity and substitutes an L_N^c-size SAT circuit into every generated query without row advice.
- sparse_row_patching: `C(H_N^{SAT})\le S_D+c\,|K_{idx}(\pi)|\,N^{1+o(1)}`. Valid when: Requires a no-advice residual circuit D agreeing with H_N^SAT outside K_idx and an explicit row implementation of size N^{1+o(1)} per patched row.
- forced_semantic_support: `|K_{idx}(\pi)|\ge c^{-1}\left(N^{\epsilon-\gamma_N-o(1)}-N^{\epsilon-\eta_N-o(1)}\right)`. Valid when: Valid when the asserted source lower bound has exponent 1+epsilon-gamma_N and the extracted residual circuit is smaller by margin eta_N greater than gamma_N.
- support_density_window: `|K_{idx}(\pi)|/M_N\ge N^{\epsilon-q-\\gamma_N-o(1)}`. Valid when: Valid when M_N=N^{q+o(1)} and the residual circuit term is lower order than the claimed lower-bound margin.

## Attempted Derivation

- Fix a short EF+SAT_U^subst proof pi of the lower-bound sentence LB_N: C(H_N^SAT)>N^{1+epsilon-gamma_N}.
- Assume the named extractor NoAdviceSemanticResidualExtractor_N returns (D_pi,K_idx(pi)) where D_pi computes the parity of all rows outside K_idx(pi) and has size S_D<=N^{1+epsilon-eta_N}.
- For every deleted row j in K_idx(pi), patch D_pi by inserting the explicit row circuit for x -> SAT(G_N(x,j)); xoring these residual rows gives a circuit for H_N^SAT.
- The patching circuit has size at most S_D+c|K_idx(pi)|N^{1+o(1)}, so the source lower bound forces |K_idx(pi)| to exceed the normalized gap between N^{1+epsilon-gamma_N} and S_D.
- Substitute M_N=N^{q+o(1)} to obtain |K_idx(pi)|/M_N>=N^{epsilon-q-gamma_N-o(1)} whenever S_D is lower order than the source margin.
- The same row implementation gives C(H_N^SAT)<=N^{1+q+o(1)}, hence q<epsilon-o(1) is an immediate falsifier for the advertised source lower bound.

Blocking gap: The proof is conditional on NoAdviceSemanticResidualExtractor_N, equivalently SATSemanticLocality_N: EF+SAT_U^subst may use SAT-semantic inferences whose effect is not decomposable into a residual circuit plus an explicit row set.

## Falsifiers

- q<epsilon-o(1): row-enumeration gives C(H_N^SAT)<=N^{1+q+o(1)}, refuting the claimed N^{1+epsilon-o(1)} source lower bound.
- Indexed SAT substitution in EF+SAT_U^idx remains a finite falsifier for occurrence-based parsers: one displayed SAT atom can denote M_N row-indexed semantic dependencies.
- Small K_idx with no residual D_pi is the targeted falsifier for NoAdviceSemanticResidualExtractor_N and would certify a genuinely SAT-semantic proof behavior.
- A dense functional property extracted from proofs is a natural-proofs falsifier unless the route proves non-largeness, nonconstructivity, or proof-mediated usefulness not inducing truth-table largeness.
- Nonuniform row advice hidden in D_pi invalidates the transfer because the residual agreement would no longer be a uniform target-preserving extraction.

## Learning

Cycle 94 adds a non-repeated quantitative sharpening: semantic support is not only at least N^{epsilon-o(1)} under residual extraction; its row density is at least N^{epsilon-q-o(1)}. This converts the q>=epsilon ceiling into a trichotomy for the formula-semantic fork: invalid source when q<epsilon, near-full row pressure when q=epsilon+o(1), and weakened density when q>epsilon. The live inference-quality packet is explicit and the only remaining proof gap is NoAdviceSemanticResidualExtractor_N/SATSemanticLocality_N, not generic barrier folklore and not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch needs a concrete quantitative stress test for the q-density window; another abstract restatement of naturalization or semantic locality would not decide whether the beta-zero carrier can support the draft theorem chain.
- Situation seed: Consider EF+SAT_U^subst proofs for beta-zero carriers H_N^SAT with M_N=N^{epsilon+delta} rows, L_N=(log N)^d, generator overhead N^{rho+o(1)}, and a hypothetical no-advice residual extractor producing D_pi plus K_idx(pi).
- Varied variable: delta=q-epsilon, the row-count slack above the mandatory source-lower-bound threshold.
- Held-fixed controls: epsilon>0 and the claimed source lower bound C(H_N^SAT)>N^{1+epsilon-o(1)}, beta-zero query length L_N=(log N)^d and uniform generator description, proof model EF+SAT_U^subst with indexed SAT substitutions allowed, no-advice extraction and same-N circuit-size accounting, row implementation cost N^{1+o(1)} for sparse patching
- Expected observation: When delta<0 the source lower bound is falsified by the row ceiling; when delta=0 the semantic branch must charge an N^{-o(1)} fraction of all rows; when delta>0 the absolute N^{epsilon-o(1)} support remains but full-row pressure weakens by N^{-delta}.
- Transfer certificate needed: A proof of NoAdviceSemanticResidualExtractor_N/SATSemanticLocality_N showing that every nonfunctional short proof yields a residual circuit D_pi and explicit K_idx(pi) without advice; otherwise the thought experiment remains only a falsifier probe.

## Next Experiment

Instantiate NoAdviceSemanticResidualExtractor_N on the minimal EF+SAT_U^subst fragment with SAT self-reduction and extension substitution: either construct D_pi,K_idx explicitly for every proof step, or isolate the first SAT-semantic rule that breaks residual agreement without becoming a dense functional property.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Cook-Reckhow guard for unwitnessed SAT extensionality: an advice-free proof carrier using formula extensionality for H_N^SAT is target-preserving only if every semantic identity step supplies a checkable quotient witness counted in alpha_ext. If the step is accepted as an unwitnessed SAT-semantic oracle rule, the parser pi -> Q_pi is not a valid MCSP/MKtP carrier transfer; it is a semantic-oracle escape, not a proof of the beta-zero lower bound.

## Definitions

- source object: A P_uExt proof pi of the sentence LB_N: C(H_N^SAT)>N^{1+epsilon-o(1)}, where H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), M_N<=N^{q+o(1)}, and G_N has uniform generation overhead N^{rho+o(1)}.
- target object: An advice-free occurrence transcript or quotient witness Q_pi with adaptive-cover exponent alpha_ext that lets the beta-zero row-residual patch construct a circuit for H_N^SAT.
- controlled interface: The parser may use the proof string, explicit witnessed equality data, and uniform verifier code, but not semantic SAT-oracle answers, nonuniform row selectors, or hidden formula-equivalence advice.
- target-preserving condition: The extracted Q_pi must be E-uniform and its cover, forced-row, residual, query-count, and generator exponents must remain below the claimed lower-bound exponent.

## Assumptions

- Proof model: ordinary Cook-Reckhow verification is uniform polynomial time over the proof string; a semantic SAT-extensionality side condition is either witnessed in the proof or explicitly reclassified as an oracle/advice rule.
- Circuit model: C(.) is unrestricted nonuniform Boolean circuit size for the N-bit truth table of H_N^SAT; the upper-bound patch and the claimed lower bound use the same circuit model.
- Length regime: N is the external input length, M_N<=N^{q+o(1)}, generator overhead is N^{rho+o(1)}, forced-row exponent is f, residual-row exponent is r, and quotient cover exponent is alpha_ext.
- Uniformity/advice regime: Q_pi and all quotient witnesses are advice-free and computable from pi and N; hardwiring a fixed accepted proof is allowed only when deriving a negative upper-bound falsifier.
- Barrier scope: this is a sparse proof-carrier audit, not a large constructive natural property and not a route to P != NP by itself.

## Equations

- adaptive_cover_cost: `alpha_ext = max_l { tau_l, a_l + mu_l, omega_l }`. Valid when: Valid when each witnessed extensionality step is represented by explicit block summaries, local openers, and routing costs in the adaptive-cover normal form.
- patched_upper_bound: `C(H_N^SAT) <= N^{max{rho, q + alpha_ext, max{f,r} + 1} + o(1)}`. Valid when: Applies after the parser outputs an advice-free quotient transcript and row-residual set for the beta-zero SAT-parity carrier.
- lower_bound_falsifier_threshold: `max{rho, q + alpha_ext, max{f,r} + 1} < 1 + epsilon => no valid proof-carrier certificate for C(H_N^SAT)>N^{1+epsilon-o(1)}`. Valid when: Valid when the asserted source lower bound and the constructed patch circuit are measured in the identical unrestricted circuit model.
- uExt_dichotomy: `UExt = WExt(alpha_ext) or SemanticOracleEscape`. Valid when: Requires that every semantic identity rule be classified as either proof-string witnessed or outside advice-free Cook-Reckhow verification.

## Attempted Derivation

- Fix H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N<=N^{q+o(1)} and generator overhead N^{rho+o(1)}; measure all consequences in unrestricted nonuniform circuit size C(.).
- Classify each formula-identity step in a candidate proof pi. If the verifier checks the step from proof data, package that data as W_i and charge it to the adaptive-cover exponent alpha_ext.
- Induct over proof steps: ordinary occurrence-local steps preserve the existing transcript; witnessed identity steps contract quotient edges; row-parity binding marks forced rows; all other rows are residual.
- Compose the generator circuit, the quotient opener, and residual row patches to obtain C(H_N^SAT)<=N^{max{rho,q+alpha_ext,max{f,r}+1}+o(1)}.
- Compare this exponent with the claimed source lower bound exponent 1+epsilon. If it is smaller, the proof carrier is a falsifier for the claimed certificate route.
- Try to parse a genuinely unwitnessed UExt step from proof syntax alone. The parser lacks the quotient witness needed to determine which occurrences share SAT semantics.
- Use the SAT_U oracle-completion thought countermodel: keep the proof skeleton fixed and flip a private unforced row. The parser's transcript is unchanged, but the row parity changes, so the extraction is not sound.
- Conclude the dichotomy: witnessed extensionality is paid for by alpha_ext; unwitnessed extensionality is a semantic-oracle model change unless UExtWitnessability is proved for the concrete proof system.

Blocking gap: UExtWitnessability remains unproved for any full strong system with hidden SAT-semantic reasoning: one must show that every semantic identity used by short proofs has an advice-free quotient witness with declared alpha_ext, or explicitly classify the system as outside the controlled MCSP/MKtP carrier interface.

## Falsifiers

- falsifier: a proof checker accepts an unwitnessed SAT-equivalence step only by semantic oracle access, so the carrier is not advice-free Cook-Reckhow data.
- falsifier: the extracted quotient has alpha_ext with max{rho,q+alpha_ext,max{f,r}+1}<1+epsilon, giving a valid upper bound against the claimed source lower bound.
- falsifier: nonforced private rows can be spoofed while preserving all occurrence-local labels, so local soundness alone cannot certify row-parity binding.
- falsifier: a quotient witness depends on a nonuniform row selector or hidden formula-equivalence advice, invalidating the target-preserving transfer.
- falsifier: residual rows exceed the declared exponent r, causing the patch ledger to undercount the actual circuit upper bound.

## Learning

Cycle 94 sharpens the formula-semantic fork into a Cook-Reckhow guard: witnessed extensionality is not an escape and pays alpha_ext in a valid upper-bound falsifier, while unwitnessed SAT extensionality is not a stronger MCSP/MKtP carrier but a semantic-oracle model change unless UExtWitnessability is proved. This is route-level progress only.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the UExtWitnessability fork.`
- Rationale: The top proof-delivery obstruction is not another hardness-magnification restatement; it is whether semantic formula identity supplies an advice-free quotient transcript or hides oracle advice.
- Situation seed: Padded SAT-query family: let G_N(x,j)=Pad_{z_j}(F_i(x)) where many syntactically distinct padded formulas are semantically equivalent. A P_uExt proof uses one atomic unwitnessed extensionality step to identify all pads before proving a row-parity claim for H_N^SAT.
- Varied variable: alpha_ext, the exponent of the explicit quotient witness needed to open the semantic equivalence classes of the padded formulas.
- Held-fixed controls: M_N<=N^{q+o(1)} and generator overhead N^{rho+o(1)} remain fixed., The target circuit model is unrestricted nonuniform C(H_N^SAT)., The parser is advice-free and may read only pi plus explicit witnesses., The claimed lower-bound threshold is C(H_N^SAT)>N^{1+epsilon-o(1)}., Residual-row patch accounting uses the same r and f exponents as the beta-zero row-residual packet.
- Expected observation: When alpha_ext is supplied and charged, the patch bound becomes N^{max{rho,q+alpha_ext,max{f,r}+1}+o(1)}. When the quotient is uncharged, the same proof skeleton can hide private-row parity changes, so the parser extraction is invalid.
- Transfer certificate needed: A UExtWitnessability certificate: every semantic extensionality step in the concrete proof system must output an advice-free quotient witness with measured alpha_ext and row-parity preservation before the intuition may enter proof obligations.

## Next Experiment

Instantiate two concrete systems, EF+WExt and EF+SAT-oracle-UExt, for the same LB_N sentence; write the parser for the witnessed system and the SAT_U private-row countermodel for the oracle system with explicit alpha_ext, f, r, q, and rho.
