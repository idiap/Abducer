# cycle-0092

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For the concrete proof system Psys_h^supp = EF with SATeq axioms, bounded self-reduction axioms to depth h, and support-declared extension variables, any accepted proof pi of LB_N(epsilon): Ckt(H_N^SAT)>N^{1+epsilon-o(1)} whose parsed transcript has subthreshold support, leaf-solver, and residual-row cost is not a valid lower-bound certificate. The transcript constructs a circuit for H_N^SAT below the claimed threshold, giving a route-level falsifier, while the beta-zero transfer to SAT notin P/poly remains conditional on a genuine source lower bound.

## Definitions

- source object: Psys_h^supp proof pi of LB_N(epsilon): Ckt(H_N^SAT)>N^{1+epsilon-o(1)}, where H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), M_N<=N^{q+o(1)}, L_N=(log N)^d.
- target object: the target-preserving consequence SAT notin P/poly obtained from a valid LB_N plus beta-zero transfer; the contrapositive subthreshold circuit is used only as a route falsifier.
- controlled interface: beta-zero SAT-query substitution plus an advice-free parser pi -> T_pi exposing EqSAT links, bounded self-reduction leaves, EF extension supports, and residual row set R_pi.
- target-preserving condition: q,rho and the transcript, leaf-solver, and patch exponents stay below 1+epsilon while L_N is polylogarithmic, so fixed polynomial SAT circuits contribute only N^{o(1)} debt.
- Psys_h^supp syntax: EF extension definitions may mention prior extension variables and SAT labels only when a checkable row-support set is declared and charged by the parser.
- bounded-SR leaf profile: after at most h self-reduction layers the transcript exposes B_N<=N^{q+eta+o(1)} leaf formula families, evaluated by a nonuniform leaf solver of size N^{tau+o(1)} on the generated leaf range.
- residual rows: R_pi is the set of source inputs x on which the transcript-induced approximator D_{T_pi} may disagree with H_N^SAT.

## Assumptions

- Circuit model is nonuniform Boolean SIZE over a fixed finite basis; equality tests for N-bit source rows cost O(N).
- Length regime is L_N=(log N)^d with d>1, M_N<=N^{q+o(1)}, generator size C(G_N)<=N^{rho+o(1)}, and fixed epsilon>0 with max{q,rho}<1+epsilon.
- Advice status is advice-free except that the proof pi, transcript T_pi, and leaf solver are explicitly charged inside S_T or N^{tau+o(1)}; no hidden table of SAT labels is allowed.
- Support adequacy assumption: from an accepted Psys_h^supp proof the parser produces D_{T_pi} agreeing with H_N^SAT off R_pi using only declared supports, EqSAT links, bounded-SR leaves, and the charged leaf solver.
- Same-theory condition: SATeq and SR axioms are interpreted over the real SAT predicate on the generated polylogarithmic formulas, not over arbitrary occurrence labels.
- Non-claim boundary: this lemma does not cover arbitrary EF+SAT extension variables unless the normal-support parser lemma NSP_N is separately proved.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\quad M_N\le N^{q+o(1)},\quad |G_N(x,j)|=L_N=(\log N)^d`. Valid when: Valid when the carrier generator and SAT-label universe are fixed before any proof-system parsing or target-circuit substitution.
- beta_zero_transfer: `SAT\in SIZE(n^c)\Rightarrow C(H_N^{SAT})\le N^{\rho+o(1)}+M_N\,L_N^c=N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies after the SAT circuit is nonuniform but fixed-exponent and the target query length is polylogarithmic beta-zero.
- transcript_approximator: `C(D_{T_\pi})\le S_T+N^{\rho+o(1)}+B_N\,N^{\tau+o(1)}\le S_T+N^{\rho+o(1)}+N^{q+\eta+\tau+o(1)}`. Valid when: Requires support adequacy for Psys_h^supp and a charged bounded-SR leaf solver on the generated leaf range.
- row_patching: `C(H_N^{SAT})\le C(D_{T_\pi})+O(|R_\pi|N)`. Valid when: Requires the approximator be defined on all source inputs and disagree only on the explicitly listed residual rows.
- certificate_falsifier_threshold: `S_T+N^{\rho+o(1)}+N^{q+\eta+\tau+o(1)}+|R_\pi|N<N^{1+\epsilon-o(1)}\Rightarrow LB_N(\epsilon)\text{ is not soundly certified by }\pi`. Valid when: Valid when all proof, parser, leaf, generator, and residual-patching costs are charged in the same nonuniform circuit model.

## Attempted Derivation

- Fixed the carrier H_N^SAT with beta=0, M_N<=N^{q+o(1)}, L_N=(log N)^d, and generator size N^{rho+o(1)}; the source statement is LB_N(epsilon): Ckt(H_N^SAT)>N^{1+epsilon-o(1)}.
- Named the concrete proof model Psys_h^supp: EF+SATeq+bounded-SR with support-declared extension variables, no hidden advice, and charged proof/transcript/leaf-solver costs.
- Parsed any accepted proof pi into T_pi containing declared row supports, EqSAT quotient links, bounded-SR leaf families, a charged leaf solver, and a residual row set R_pi.
- Under support adequacy, built D_T by computing G_N, following T_pi, evaluating charged SR leaves with the leaf solver, and xoring the resulting labels; this gives C(D_T)<=S_T+N^{rho+o(1)}+N^{q+eta+tau+o(1)}.
- Patched the residual set R_pi by equality tests on N-bit source rows, yielding C(H_N^SAT)<=C(D_T)+O(|R_pi|N).
- Concluded that any accepted proof with total charge below N^{1+epsilon-o(1)} is a falsifier for the claimed source lower-bound certificate, not evidence for P != NP.
- Separated the restricted theorem from the full EF+SAT ambition: arbitrary extension variables require NSP_N, an advice-free normal-support parser lemma not supplied by ordinary soundness.

Blocking gap: NSP_N: every short arbitrary EF+SATeq+SR proof of LB_N must admit a support-complete, advice-free transcript with row distance and leaf-solver costs small enough to preserve the N^{1+epsilon} threshold. This is unproved and may fail for extension-compressed SAT-semantic reasoning.

## Falsifiers

- Subthreshold support transcript falsifier: S_T+N^{q+eta+tau}+|R_pi|N<N^{1+epsilon-o(1)} gives an explicit small circuit for H_N^SAT.
- Bounded-SR leaf-solver falsifier: if q+eta+tau<1+epsilon and residual rows are fewer than N^{epsilon-o(1)}, the proof-mediated source lower bound collapses.
- Low constrained row-distance falsifier after EqSAT/SR quotienting: row-parity distance below N^{epsilon-o(1)} is patchable.
- Hidden-advice falsifier: any parser that uses uncharged SAT truth-table information invalidates the claimed advice-free extraction.
- Functional-density falsifier: dense constructive label-functional certificates naturalize rather than escape barriers.
- Positive-beta falsifier remains quarantined: any return to target-query length N^beta with beta>0 caps the transfer by q+beta c.

## Learning

Cycle 92 turns the formula-semantic fork into a sharper proof packet. For support-declared EF+SATeq+bounded-SR, subthreshold parsed support plus bounded leaf solving and sparse residual rows gives a valid small-circuit falsifier for LB_N. The full EF+SAT claim is not proved; the precise remaining obstruction is NSP_N, the advice-free extraction of arbitrary extension-variable reasoning into charged row supports and SR leaves. This is route-level certification, not progress on the main P != NP conjecture itself.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The full-system gap is about whether EF extension variables hide semantic support. A concrete target-preserving thought experiment tests the exact support threshold instead of restating hardness magnification or barrier folklore.
- Situation seed: Consider a beta-zero SAT parity carrier with L_N=(log N)^d, d>1, M_N=N^q, q<1+epsilon, and a Psys_h proof that introduces one extension variable Z_x intended to equal xor_{j<=M_N} SAT(G_N(x,j)) using EqSAT and depth-h self-reduction links.
- Varied variable: lambda, the exponent of declared or extractable source-row support, |R_pi|=N^{lambda+o(1)}, while the bounded-SR leaf-solver exponent q+eta+tau is held fixed.
- Held-fixed controls: Beta-zero query length L_N=(log N)^d and generator size N^{rho+o(1)} with max{q,rho}<1+epsilon., Nonuniform Boolean SIZE model with equality patch cost O(N) per residual row., No hidden advice in the parser; all proof, support, extension, EqSAT, SR, and leaf-solver data are charged., Target consequence remains SAT notin P/poly only if a genuine source lower bound survives the audit.
- Expected observation: When max{q+eta+tau,1+lambda}<1+epsilon, the support-declared proof yields a subthreshold H_N circuit, so the certificate is invalid. If a full EF proof survives below this threshold, it must use a named SAT-semantic extension principle not captured by occurrence or bounded-SR support.
- Transfer certificate needed: An advice-free NSP_N theorem mapping arbitrary EF+SAT extension DAGs to support-complete transcripts with preserved row distance, or a counterexample naming the semantic principle that prevents such a valid transfer.

## Next Experiment

Try to prove NSP_N for the fragment EF+SATeq+SR whose extension definitions are row-affine and support-monotone; if the proof fails, extract the minimal extension rule that creates uncharged SAT-semantic support and state the final theorem scope around Psys_h^supp.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Conditional semantic-support dichotomy for EF+SAT_U^subst. Fix epsilon>0 and beta-zero carrier H_N^SAT. If every short accepted EF+SAT_U^subst proof pi of LB_N either yields a no-advice functional truth-table property or an ExtensionRowRealizer_N output (K_pi,D_pi) satisfying the residual identity, then functional outputs naturalize, while nonfunctional outputs must have |K_pi|>=N^{epsilon-o(1)} under the claimed source lower bound C(H_N^SAT)>N^{1+epsilon-o(1)}.

## Definitions

- source object: a concrete EF+SAT_U^subst proof pi of LB_N(H_N^SAT), where H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), x has n=log N bits, M_N<=N^{q+o(1)}, and G_N has generator overhead N^{rho+o(1)}.
- target object: a fork-resolving extraction theorem producing either a functional natural property of N-bit truth tables or a semantic row-support certificate K_pi with a residual circuit D_pi.
- controlled interface: ExtensionRowRealizer_N is a uniform no-advice algorithm which reads pi and returns K_pi plus D_pi such that H_N^SAT equals D_pi patched by the rows in K_pi.
- target-preserving condition: q,rho<1+epsilon, proof length and verifier time are poly(N), extraction uses no nonuniform row advice, and the target class remains nonuniform Boolean SIZE_n(N^{1+epsilon-o(1)}).
- semantic row support: K_pi is a set of generator indices j whose row functions x -> SAT(G_N(x,j)) are not absorbed by the extracted residual D_pi.
- functional output: a total decidable property P_pi of N-bit truth tables, containing TT(H_N^SAT) and excluding every truth table of circuits in the named target class.

## Assumptions

- Model: EF+SAT_U^subst is extended Frege over Boolean formulas plus SAT_U atoms on extension-coded formula descriptions, with a substitution rule preserving SAT truth under formula-code equality.
- Regime: N=2^n, beta=0 source length, M_N<=N^{q+o(1)}, q<1+epsilon, and all hidden constants are independent of N.
- Uniformity/advice: the extractor and verifier are uniform polynomial-time in the proof encoding and N, and do not receive a row set, truth table, or circuit as advice.
- Lower-bound cutoff: the source statement is the route-level hypothesis C(H_N^SAT)>N^{1+epsilon-o(1)}, not P != NP.
- Naturalness cutoff: a functional property with density at least N^{-O(1)}, poly(N) constructivity, and usefulness against SIZE_n(N^{1+epsilon/2}) is treated as a valid natural-proofs object.

## Equations

- beta_zero_carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\quad M_N\le N^{q+o(1)}`. Valid when: Valid when the source object is the beta-zero SAT-parity carrier with x ranging over n=log N bits.
- black_box_sat_transfer: `SAT_{L_N}\in SIZE(L_N^c)\Rightarrow C(H_N^{SAT})\le N^{\rho+o(1)}+N^{q+o(1)}L_N^c=N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies after the generator overhead is N^{rho+o(1)} and L_N=(log N)^d makes L_N^c=N^{o(1)}.
- semantic_residual_identity: `H_N^{SAT}(x)=D_\pi(x)\oplus\bigoplus_{j\in K_\pi} SAT(G_N(x,j))`. Valid when: Valid when ExtensionRowRealizer_N outputs a residual circuit whose omitted semantic rows are exactly K_pi.
- sparse_patch_upper_bound: `C(H_N^{SAT})\le S(D_\pi)+O(|K_\pi|N)`. Valid when: Requires nonuniform patching of each omitted n-bit row function by a truth-table circuit of size O(N).
- forced_row_threshold: `S(D_\pi)\le N^{1+\epsilon-\eta},\ |K_\pi|\le N^{\epsilon-\eta}\Rightarrow C(H_N^{SAT})\le N^{1+\epsilon-\Omega(\eta)}`. Valid when: Valid when the residual identity and sparse patching inequality both hold with eta bounded below by 1/polylog N.

## Attempted Derivation

- Fixed source sentence LB_N as C(H_N^SAT)>N^{1+epsilon-o(1)} for N=2^n truth-table length and target nonuniform SIZE_n.
- Named proof system EF+SAT_U^subst: extended Frege plus SAT_U atoms over extension-coded formula descriptions and extensional substitution for formula-code equality.
- Tried to normalize every SAT_U atom in pi to a formula-code circuit B_a(x,z) and define Rows(a) as the generator indices j whose row SAT(G_N(x,j)) is semantically queried by B_a.
- If the union K_pi of Rows(a) is small and the remaining proof behavior is fixed, the residual identity gives C(H_N^SAT)<=S(D_pi)+O(|K_pi|N), forcing |K_pi|>=N^{epsilon-o(1)} under the source lower bound.
- If the proof behavior instead depends only on TT(H_N^SAT), the accepted-table set is poly(N)-constructive; with polynomial density it becomes a valid natural property useful against the same target class.
- Tested occurrence extraction and refuted it by EF+SAT_U^idx: one indexed SAT_U atom has O(1) displayed occurrence charge but M_N semantic rows.

Blocking gap: ExtensionRowRealizer_N remains unproved for full EF+SAT_U^subst. SAT_U substitution and formula-code extension variables can hide row dependence behind arbitrary semantic equivalences, so the branch cannot uniformly extract K_pi or D_pi without a row-faithfulness theorem.

## Falsifiers

- falsifier: one indexed SAT_U macro A_N(x,J)=SAT_U(Code(G_N(x,J))) separates O(1) displayed occurrences from M_N semantic rows, invalidating occurrence-based parsers.
- falsifier: a SAT-composition axiom can reason about a formula-code circuit without exposing generator-row constants, blocking private-label row invariance.
- falsifier: any extracted residual D_pi of size N^{1+epsilon-eta} with |K_pi|<=N^{epsilon-eta} contradicts the claimed source lower bound by sparse patching.
- falsifier: a functional accepted-proof property with density N^{-O(1)} is a valid natural property and conflicts with PRF hardness for the exact separated circuit class.
- falsifier: row set K_pi chosen with nonuniform advice after seeing TT(H_N^SAT) destroys target preservation and cannot support the proof-delivery queue.

## Learning

Cycle 92 makes one proof-delivery move: the branch now has a concrete strong proof system, EF+SAT_U^subst, and a finite EF+SAT_U^idx falsifier to occurrence parsing. The live pvsnp_inference_quality packet is: source_statement=short EF+SAT_U^subst proof of LB_N for H_N^SAT; target_statement=functional naturalization or semantic-support forced-row theorem; model_context=nonuniform Boolean circuits, beta-zero SAT parity carrier, EF+SAT_U^subst proof model, extraction/simulation rather than many-one reduction; quantifier_context=N=2^n, M_N<=N^{q+o(1)}, q,rho<1+epsilon, poly(N) proofs, uniform no-advice extractor; derivation_status=conditional dichotomy proved from ExtensionRowRealizer_N plus sparse patching, full theorem blocked at RowFaithfulExtensionRealizer; reviewer finding=occurrence parser invalid, semantic support is the valid invariant, naturalness triggers only on functional dense constructive outputs. This is route-level progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for ExtensionRowRealizer_N and occurrence-parser claims.`
- Rationale: The current branch needs a concrete formula-semantic stress test because abstract barrier labels no longer distinguish occurrence-local proofs from EF+SAT_U^subst proofs with indexed formula-code substitution.
- Situation seed: Take a padded beta-zero SAT-query family with H_N^SAT(x)=xor_{j<=N^q} SAT(G_N(x,j)) and build an EF+SAT_U^idx proof skeleton using the single macro atom A(x,J)=SAT_U(Code(G_N(x,J))) plus parity wiring over J.
- Varied variable: row-index leakage b, the number of index bits hidden inside each SAT_U formula-code atom, ranging from b=0 to b=ceil(log M_N).
- Held-fixed controls: N=2^n truth-table length and target class SIZE_n(N^{1+epsilon-o(1)}) are fixed., q,rho<1+epsilon and the beta-zero transfer regime are fixed., The extractor is uniform and receives no row advice or truth-table advice., Proof length is charged by formula-code circuit DAG size, not by expanding all J assignments.
- Expected observation: At b=0 the occurrence parser and semantic support coincide; at b=log M_N one displayed SAT_U atom can carry M_N semantic rows, so occurrence charge collapses while residual patching still requires semantic K_pi of size N^{epsilon-o(1)} if the source lower bound is true.
- Transfer certificate needed: A row-faithful ExtensionRowRealizer_N showing how indexed SAT_U atoms either expand to semantic K_pi, functionalize into a natural property, or invoke a named nonrelativizing SAT-semantic principle that is outside occurrence-relativizing proofs.

## Next Experiment

Formalize RowFaithfulExtensionRealizer_N for the restricted normal-form fragment where every SAT_U atom has formula-code Code(G_N(x,j)) with explicit j wires; prove the dichotomy there, then test the first rule that breaks it: extensional substitution of an arbitrary formula-code circuit B(x,J).

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For the beta-zero SAT-parity carrier and P_uExt=EF+SAT_U^{occ} plus unwitnessed SAT-extensionality, any short proof pi that is valid for the controlled MCSP/MKtP interface obeys a dichotomy: either every semantic extensionality call has an advice-free quotient witness with adaptive-cover exponent alpha_ext and the standard low-cover circuit upper-bound falsifier follows, or pi uses a semantic-oracle step and is not a target-preserving carrier for language hardness.

## Definitions

- source object: A P_uExt proof pi of LB_{N,epsilon}(H_N^SAT) in EF+SAT_U^{occ} plus unwitnessed semantic SAT-extensionality steps, where H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), M_N<=N^{q+o(1)}, and G_N has generator circuits of size N^{rho+o(1)}.
- target object: Either an unrestricted circuit upper-bound falsifier for H_N^SAT of size N^{max{rho,q+alpha_ext,max{f,r}+1}+o(1)}, or a certification that pi uses a non-Cook-Reckhow semantic-oracle step outside the MCSP/MKtP carrier model.
- controlled interface: A uniform parser maps each accepted proof to occurrence transcripts, forced-row set F_N, quotient/extensionality witnesses with adaptive-cover exponent alpha_ext, and residual row set R_N, without advice or nonuniform hard-row selection.
- target-preserving condition: The parser and quotient witnesses are E-uniform, advice-free, preserve the same H_N^SAT length N and SAT-query family G_N, and never replace lower-bound evidence by a nonuniform semantic oracle.
- P_wExt is the witnessed fragment in which every formula-identity or SAT-extensionality inference carries an explicit quotient transcript checkable by the parser.
- P_uExt is the unwitnessed semantic extension in which the proof may invoke SAT(F)=SAT(F') as an atomic semantic premise without exposing a quotient transcript.
- ForcedRows(pi) are rows whose parity is constant over the local SAT-label completions allowed by the parsed transcript and quotient witnesses.
- alpha_ext is the adaptive-cover exponent paid by all quotient witnesses used to open, identify, or patch SAT-query labels in pi.

## Assumptions

- Length regime: N ranges over the beta-zero carrier lengths, M_N<=N^{q+o(1)}, and each SAT query has polylogarithmic or otherwise fixed audited length consistent with generator overhead N^{rho+o(1)}.
- Proof regime: pi has size polynomial in N or in the paper's accepted proof-size scale, and every syntactic EF or occurrence-local rule is checkable without SAT or formula-equivalence advice.
- Uniformity regime: the parser, quotient witnesses, residual list, and patch circuits are computable uniformly from (N,pi); no hard row, equality quotient, or residual selector is supplied as nonuniform advice.
- Extensionality regime: a semantic SAT-extensionality step is valid for the controlled interface only after an advice-free quotient witness is exposed and charged to alpha_ext.
- Circuit model: the target upper bound is for unrestricted nonuniform Boolean circuits computing the same truth table H_N^SAT on N-bit inputs; this is a route-level falsifier, not a lower bound.
- Residual regime: |F_N|<=N^{f+o(1)} and |R_N|<=N^{r+o(1)} are the forced and residual row counts left after parsing and quotient contraction.
- Naturalness scope: sparse proof-derived transcripts are not automatically large natural properties, but any repair that makes the accepted row property dense and polynomial-time decidable triggers the natural-property falsifier.
- Same-theory condition: quotient witnesses must certify identities among the actual formulas generated by G_N, not among a substituted or advice-selected SAT-query family.

## Equations

- beta_zero_carrier: `H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)), M_N<=N^{q+o(1)}`. Valid when: Valid when the source object is the beta-zero SAT-parity family with the named generator G_N and audited query count exponent q.
- adaptive_ext_cover: `alpha_ext=max_e max{tau_e, max_l(a_{e,l}+mu_{e,l}), max_l omega_{e,l}}`. Valid when: Valid when each extensionality inference e supplies an explicit quotient transcript whose adaptive cover levels and opener costs are parsed uniformly.
- low_cover_decoder_size: `S(D_N)<=N^{max{rho,q+alpha_ext}+o(1)}`. Valid when: Applies after generator overhead rho and M_N SAT-query labels are simulated through advice-free quotient witnesses of cover exponent alpha_ext.
- patch_upper_bound: `C(H_N^{SAT})<=N^{max{rho,q+alpha_ext,max{f,r}+1}+o(1)}`. Valid when: Requires the parsed decoder D_N to agree with H_N^{SAT} outside forced and residual rows, which are patched by unrestricted row circuits.
- lower_bound_compatibility_gate: `max{rho,q+alpha_ext,max{f,r}+1} >= 1+epsilon-o(1)`. Valid when: Valid when pi is claimed to support C(H_N^{SAT})>N^{1+epsilon-o(1)} and low-cover parsing would otherwise give a contradiction.

## Attempted Derivation

- Source statement: a short P_uExt proof pi is proposed as an MCSP/MKtP-style certificate for the lower-bound sentence C(H_N^SAT)>N^{1+epsilon-o(1)}.
- Target statement: classify pi as witnessed-low-cover, occurrence-relativizing with patch upper bound, or semantic-oracle and therefore not a valid target-preserving carrier.
- Model context: source carrier is a proof/certificate object; target class is unrestricted circuits for H_N^SAT; reduction type is transcript-to-decoder simulation plus residual patching.
- Quantifier context: all parameters q,rho,alpha_ext,f,r,epsilon are fixed constants or o(1)-stable exponents over the beta-zero length regime; all parsers and witnesses are uniform and advice-free.
- Run induction over syntactic EF and occurrence-local rules; these update Q_pi and preserve LocSat invariance without semantic SAT reasoning.
- For each witnessed formula-identity or SAT-extensionality step, contract the quotient witness, charge its adaptive cover to alpha_ext, and keep the same generated SAT-query family.
- Define F_N as rows whose parity is constant over LocSat(Q_pi,E_pi); rows outside F_N union R_N admit a private-label spoof, so local soundness alone cannot certify them.
- Build D_N by composing the generator G_N with the low-cover quotient openers for all M_N queries, giving size N^{max{rho,q+alpha_ext}+o(1)}.
- Patch F_N and R_N by hardwiring at most N^{max{f,r}+o(1)} exceptional rows, giving C(H_N^SAT)<=N^{max{rho,q+alpha_ext,max{f,r}+1}+o(1)}.
- If a P_uExt step lacks a quotient witness, the induction stops exactly at UExtWitnessability: either add a witness and pay alpha_ext, or classify the proof as a semantic-oracle object outside the controlled carrier interface.
- Reviewer findings for the live inference-quality packet: reduction consistency passes for witnessed steps, quantifier-uniformity passes only with advice-free quotient witnesses, barrier-specificity flags dense constructive repairs as natural, and proof-derivation status is blocked only at UExtWitnessability.

Blocking gap: UExtWitnessability: an unwitnessed semantic SAT-extensionality premise has no advice-free quotient transcript, so the parser cannot certify row-parity binding or build the low-cover decoder without changing the proof model.

## Falsifiers

- falsifier: alpha_ext<1+epsilon-q and max{rho,max{f,r}+1}<1+epsilon give an unrestricted circuit upper bound contradicting the claimed source lower bound.
- falsifier: a semantic SAT-extensionality step without an advice-free quotient witness is a model change, not a valid MCSP/MKtP carrier transfer.
- falsifier: local soundness or occurrence consistency without row-parity binding admits private-row spoof completions.
- falsifier: a residual set of size N^{r+o(1)} with r+1<1+epsilon patches away the purported lower-bound source.
- falsifier: a dense polynomial-time property of accepted rows would naturalize the certificate route unless the image remains sparse or nonconstructive.
- falsifier: nonuniform selection of a hard row or quotient graph violates the target-preserving uniformity ledger.

## Learning

Cycle 92 turns the remaining formula-semantic fork into a sharper dichotomy: witnessed extensionality is paid for by alpha_ext and yields a valid low-cover upper-bound falsifier, while unwitnessed SAT-extensionality is not a stronger carrier but a semantic-oracle escape unless an advice-free quotient witness is supplied. This is route-level progress and does not assert P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the UExtWitnessability branch.`
- Rationale: The branch already has the abstract low-cover theorem; the unresolved issue is whether an unwitnessed semantic extensionality step can be a valid proof carrier without secretly supplying the quotient witness that yields the circuit upper bound.
- Situation seed: For each N, take a beta-zero SAT-parity family with M_N=N^{q+o(1)} generated by G_N of size N^{rho+o(1)}. A P_uExt proof cancels many row parities through atomic claims SAT(F_{x,t})=SAT(F'_{x,t}) supplied by a semantic extensionality oracle, while the occurrence transcript sees only the individual SAT-query labels.
- Varied variable: alpha_ext, the adaptive-cover exponent of an advice-free quotient witness for the semantic equality graph, with the special value 'absent' representing a pure oracle extensionality step.
- Held-fixed controls: The target function remains the same H_N^SAT and the same generator G_N is used throughout., The query exponent q and generator overhead rho are fixed below the claimed lower-bound threshold., No hard row, quotient graph, or semantic equality table may be supplied as advice., The circuit model for the falsifier remains unrestricted nonuniform circuits on N input bits., Residual density r and forced-row exponent f are separately recorded and charged in the patch term.
- Expected observation: When alpha_ext is below the compatibility threshold, quotient exposure yields the low-cover upper bound. When alpha_ext is absent, the occurrence parser admits private-row spoof completions, showing that the proof used a semantic oracle rather than a target-preserving carrier.
- Transfer certificate needed: An advice-free quotient transcript for every semantic extensionality edge, with measured alpha_ext and row-parity binding; otherwise a formal oracle-model classification that quarantines P_uExt from the MCSP/MKtP carrier route.

## Next Experiment

Fix the exact syntax of P_wExt for one proof formalism, run the rule induction on three rule classes (EF extension, SAT_U^{occ} occurrence rule, witnessed extensionality), and either produce the paper-ready WExtTranscriptInduction proof or isolate the first unparsed rule as a new named blocker.
