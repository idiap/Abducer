# cycle-0126

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For the beta-zero parity carrier, a Psys_sym^{dag+declTSR(h)} proof whose Tseitin self-reduction children are syntactically declared before use has a computable least prefix-closed support cone K_dag^TSR(pi). The Gamma line induction extends with an explicit TSR row-expansion charge. If the resulting transcript is subthreshold, the claimed LB_N(1+epsilon) is falsified in the same nonuniform SIZE model. Hidden semantic branch-pruning is not covered and has a first-hidden-row falsifier unless RealSATInfluenceRealizer_N^arb is supplied.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, polylogarithmic generated formula length L_N=(log N)^d, and generator circuit size N^{rho+o(1)}.
- target object: a same-model nonuniform SIZE upper-bound falsifier for LB_N(1+epsilon) for H_N^SAT, explicitly not a P != NP or NP not subset P/poly separation.
- controlled interface: the least prefix-closed reachable parser K_dag^TSR(pi) containing final-line rows, visible FormulaEval parents, bit-explicit EF supports, bounded-SR leaves, and declared TSR child rows, each with an auditable enumerator or full-scan charge.
- target-preserving condition: every row influencing the proof is visible before semantic use, uniformly enumerable without SAT-truth advice, expanded in the same proof theory, and charged in Gamma below the source lower-bound threshold; otherwise the full semantic claim is quarantined.
- Psys_sym^{dag+declTSR(h)} is Psys_bEF^- plus transparent FormulaEval DAG lines and a bounded Tseitin self-reduction rule whose restriction children are named by row indices and parent pointers.
- R_TSR(pi) denotes the number of declared TSR child row-slots reachable from the final LB_N line; if R_TSR=N^{kappa+theta+o(1)} then the occurrence expansion costs N^{1+kappa+theta+o(1)} up to polylog factors.
- E_pi is the number of residual bad source rows patched by equality gates; the sparse-row patch cost is O(E_pi N).

## Assumptions

- Circuit model is nonuniform SIZE over Boolean circuits; proof transcript, generator code, and visible support enumerators are allowed as fixed nonuniform data only through their charged sizes.
- Length regime is N -> infinity with L_N=(log N)^d for fixed d>1, M_N=N^{q+o(1)}, beta=0 target queries, and q,rho<1+epsilon for the magnification transfer window.
- The proof system is syntactic and bit-explicit except for declared transparent FormulaEval and declared TSR rules; extension variables carry verifier-visible support fields.
- Every FormulaEval or TSR row in K_dag^TSR(pi) has same-theory occurrence expansion, so row truth is not imported as a semantic oracle.
- The TSR rule is bounded: each invocation has a finite declared restriction tree, and all enabled children affecting the rule conclusion appear in the row list before the conclusion is used.
- The lower-bound claim LB_N(1+epsilon) means C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)} on the valid length subsequence in the same nonuniform circuit model.
- No hidden nonuniform row selector, unread enable bit, or SAT-truth advice may choose rows outside K_dag^TSR(pi).

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad |G_N(x,j)|=(\log N)^d.`. Valid when: Valid when the source carrier is the beta-zero generated parity carrier with uniformly generated polylogarithmic SAT instances.
- fixed_point: `K_{t+1}=K_t\cup Parents_{FE}(K_t)\cup Supp_{bEF}(K_t)\cup Leaves_{SR_h}(K_t)\cup Children_{TSR}^{decl}(K_t),\quad K_dag^{TSR}=\bigcup_t K_t.`. Valid when: Valid when all proof lines expose parent pointers and declared TSR child row indices before semantic use.
- tsr_charge: `X_{TSR}(\pi)\le N\,R_{TSR}(\pi)L_N^{O(1)}=N^{1+\kappa+\theta+o(1)}\quad\text{if }R_{TSR}(\pi)=N^{\kappa+\theta+o(1)}.`. Valid when: Valid when each declared child row expands to N source-row occurrences and polylogarithmic formula-local overhead is absorbed.
- gamma_packet: `\Gamma_{dag}^{TSR}(\pi)=\Gamma_{bEF}(\pi)+U(K_dag^{TSR})+X(K_dag^{TSR})+X_{TSR}(\pi).`. Valid when: Valid when FormulaEval, bounded self-reduction, bit-explicit EF, and declared TSR supports are all charged in the same ledger.
- upper_bound: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{dag}^{TSR}(\pi)+O(E_\pi N).`. Valid when: Applies after the parser line induction converts the charged transcript into a same-model circuit for the carrier.
- falsifier_window: `\max\{\rho,\gamma_{dag}^{TSR},1+e\}<1+\epsilon\Rightarrow LB_N(1+\epsilon)\text{ is false},\quad \Gamma_{dag}^{TSR}=N^{\gamma_{dag}^{TSR}+o(1)},\ E_\pi=N^{e+o(1)}.`. Valid when: Valid when the asserted source lower bound is in nonuniform SIZE and all transcript charges are subthreshold.
- declared_tsr_threshold: `\kappa+\theta<\epsilon\Rightarrow X_{TSR}(\pi)=N^{1+\kappa+\theta+o(1)}<N^{1+\epsilon-o(1)}.`. Valid when: Valid when R_TSR counts only declared reachable child rows and no hidden semantic branch pruning is used.

## Attempted Derivation

- Define proof-line nodes for bit-explicit EF, transparent FormulaEval, bounded SR_h, and declared TSR. Each node stores row-index fields, parent pointers, local verifier bits, and a list of declared child rows when a TSR rule is used.
- Initialize K_0 with the row occurrences syntactically read by the final LB_N line. Iteratively add visible FormulaEval parents, bEF extension supports, SR_h leaves, and declared TSR child rows. The proof DAG is finite, so the monotone closure reaches a least fixed point K_dag^TSR(pi).
- For each line i, prove an invariant: the parsed circuit C_i depends only on generator bits, previous parsed circuits, and the expanded rows in K_i. bEF lines use the existing bit-explicit parser; FormulaEval lines use enumerator/full-scan charges; declared TSR lines compute the Tseitin restriction combination over their listed children.
- Charge every declared TSR child row by N L_N^{O(1)} gates for occurrence expansion and local verification. With R_TSR=N^{kappa+theta+o(1)}, this adds X_TSR=N^{1+kappa+theta+o(1)}.
- At the final line, splice the generator circuit of size N^{rho+o(1)} with the parsed transcript circuit. Sparse residual mistakes on E_pi source rows are corrected by equality gates costing O(E_pi N).
- Therefore a proof transcript with N^{rho+o(1)}+Gamma_dag^TSR(pi)+O(E_pi N)<N^{1+epsilon-o(1)} yields a same-model circuit contradicting LB_N(1+epsilon). This is a valid falsifier theorem for the restricted proof system.
- For necessity, suppose a semantic TSR child r^* influences a conclusion but is absent from K_dag^TSR(pi). Keep all visible rows fixed, flip the private row r^* or an unread enable bit, and choose the generated parity carrier so the final value changes. The parser cannot distinguish the worlds, so uncharged occurrence completion fails.

Blocking gap: The derivation does not cover arbitrary semantic branch-pruning where real SAT semantics decide which children matter without a syntactic declaration. The named missing lemma is RealSATInfluenceRealizer_N^arb: from proof syntax and N alone, uniformly list all semantically influencing TSR/FormulaEval rows before use and charge them in Gamma.

## Falsifiers

- Subthreshold declared TSR charge: if kappa+theta<epsilon and all other Gamma terms are subthreshold, the proof transcript gives a same-model SIZE upper-bound falsifier for LB_N(1+epsilon).
- First hidden reachable row: an undeclared TSR child or unread enable bit can change a rule conclusion while all charged rows remain fixed, refuting free occurrence completion.
- Nonuniform selector leakage: if the row list is chosen by advice or SAT-truth labels rather than proof-visible code, K_dag^TSR is not a valid controlled interface.
- q<epsilon support-density collapse: requiring |K|/M_N>=N^{epsilon-q-o(1)} exceeds unit density, so a transparent certificate in that regime must fail or pay another superthreshold charge.
- Semantic pruning escape: arbitrary real-SAT simplification may be nonrelativizing and outside the private-row spoof, but then it must be isolated as RealSATInfluenceRealizer_N^arb rather than folded into the parser for free.

## Learning

Cycle 126 converts declared bounded TSR from a semantic warning into a charged fixed-point rule case. The valid contribution is a restricted theorem: declared TSR rows are absorbed by K_dag with threshold kappa+theta<epsilon, while hidden branch-pruning is a precise private-row falsifier. Full semantic FormulaEval is still not proved; it is isolated at RealSATInfluenceRealizer_N^arb.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the declared-versus-hidden TSR boundary.`
- Rationale: The branch already has the abstract K_dag parser. The remaining proof obligation is whether bounded Tseitin self-reduction contributes charged rows or silently imports semantic advice; a concrete threshold experiment tests exactly that interface.
- Situation seed: Take H_N^SAT with M_N=N^q and L_N=(log N)^2. A projected-dDNNF FormulaEval line invokes a bounded TSR tree on N^kappa parent rows. In world A every restriction child is declared and charged; in world B one child is guarded by an unread enable bit and omitted from K_dag.
- Varied variable: theta, the exponent for declared TSR child expansion per parent, so R_TSR=N^{kappa+theta+o(1)} while q,rho,epsilon are fixed.
- Held-fixed controls: beta=0 polylog target-query length and the same nonuniform SIZE circuit model., Generator size N^{rho+o(1)} with rho<1+epsilon., Visible FormulaEval parent pointers and bit-explicit EF support fields., No SAT-truth advice and no hidden row selector in the declared world., Residual bad-row correction charged as O(E_pi N).
- Expected observation: For theta<epsilon-kappa the declared world yields a subthreshold Gamma falsifier for LB_N(1+epsilon). In the hidden world, the first omitted enabled child produces two indistinguishable visible transcripts with different final parity, demonstrating parser invalidity rather than a stronger lower bound.
- Transfer certificate needed: A valid transfer back into the proof queue requires either a syntactic declaration list with X_TSR=N^{1+kappa+theta+o(1)} charge or a nonrelativizing RealSATInfluenceRealizer_N^arb proving that real SAT semantics uniformly exposes the same influence-closed row set before use.

## Next Experiment

Formalize the Psys_sym^{dag+declTSR(h)} grammar in one page: exact row-index fields, TSR parent/child encodings, local verifier predicate, K_dag^TSR fixed-point pseudocode, and the declared TSR line-induction case; then instantiate with kappa=epsilon/3, theta=epsilon/3, q in ((1+epsilon)/2,1+epsilon), rho<1+epsilon to verify all charges remain subthreshold except the intended q-density pressure.

# Barrier-Aware Lower-Bound Route cycle 126: Gap98 bounded-SR_h normal form

## Candidate Lemma

Annotated bounded-SR_h lines in Psys_bEF^- have a deterministic bit-explicit normal form. Replacing each such line by a prefix-scoped bEF block with fresh extension variables preserves the proof theory and contributes exactly the bounded-SR term in Gamma_bEF. Consequently a low-charge accepted proof of LB_N(1+epsilon) for H_N^SAT gives a same-model SIZE falsifier, while any sound proof below that falsifier threshold must pay N^{epsilon-o(1)} row-equivalent support.

## Definitions

- source object: a Psys_bEF^- proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, and bounded-SR row-touch budget h=N^{eta+o(1)}.
- target object: a same-model nonuniform SIZE upper-bound falsifier circuit for H_N^SAT of size N^{rho+o(1)}+Gamma_bEF^SR(pi)+O(E_pi N), or else forced row-equivalent support N^{epsilon-o(1)}.
- controlled interface: annotated bounded-SR_h lines expose type tag, parent line ids, row index, self-reduction node address, touched occurrence-neighborhood list, child-row ids, and a local bEF verifier for reachability and linkage.
- target-preserving condition: every SAT row or child row that can influence the rule is listed in the occurrence-neighborhood list and can be prefix-spliced into the same bEF theory with fresh extension variables.
- Occ_h(L) is the verifier-visible list of row/occurrence/parent-link tuples touched by bounded-SR line L; h bounds the number of listed tuples, not the semantic depth of an unexpanded tree.
- Gamma_bEF^SR(pi) is the ordinary bit-explicit bEF charge plus the sum of local verifier and row-expansion charges for all annotated bounded-SR_h lines.

## Assumptions

- Bit-explicit proof model: row indices, node addresses, parent pointers, and occurrence addresses have N^{o(1)} bits and are checked by a uniform polynomial-time parser in N.
- Annotated-rule restriction: the SR rule is row-faithful and does not call a semantic FormulaEval oracle or hidden selector to choose a child row.
- Same-theory expansion: every replacement block uses fresh extension variables and is inserted before the first line depending on the SR conclusion, so no later line changes meaning.
- Quantifier regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, h=N^{eta+o(1)}, generator size N^{rho+o(1)}, and rho<1+epsilon.
- No-advice condition: the parser obtains all row choices from proof bits and G_N, not from SAT truth advice, semantic row advice, or a nonuniform row table.

## Equations

- carrier: `H_N^{\mathrm{SAT}}(x)=\bigoplus_{j\le M_N}\mathrm{SAT}(G_N(x,j)),\qquad M_N=N^{q+o(1)}`. Valid when: Valid when the carrier is the beta-zero SAT-parity family with row generator G_N fixed uniformly and no advice hidden in row selection.
- local_sr_touch_bound: `\forall L\in SR(\pi):\ |\mathrm{Occ}_h(L)|\le h\cdot \ell_{loc}(N)=N^{\eta+o(1)}`. Valid when: Applies when bounded-SR_h is defined as an explicit row-touch budget and each occurrence address has N^{o(1)} local encoding.
- sr_gamma_definition: `\Gamma_{bEF}^{SR}(\pi)=\Gamma_{base}(\pi)+\sum_{L\in SR(\pi)} c_{SR}|\mathrm{Occ}_h(L)|\ell_{loc}(N)+O(|\pi|\log |\pi|)`. Valid when: Requires the annotated verifier fields to list every influencing occurrence and the prefix-splice expansion to stay inside the same bEF theory.
- eta_tau_bound: `|SR(\pi)|\le |\pi|=N^{\tau+o(1)}\ \Longrightarrow\ \Gamma_{bEF}^{SR}(\pi)\le \Gamma_{base}(\pi)+N^{\tau+\eta+o(1)}`. Valid when: Valid when every proof line has at most one bounded-SR invocation or a visible constant number of invocations charged separately.
- subthreshold_falsifier: `N^{\rho+o(1)}+\Gamma_{bEF}^{SR}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\ \Longrightarrow\ \neg LB_N(1+\epsilon)`. Valid when: Applies after the parser-to-circuit simulation preserves the nonuniform SIZE model, row lengths, generator overhead, and the claimed lower-bound threshold.

## Attempted Derivation

- Fix an accepted Psys_bEF^- proof pi and parse each bounded-SR_h line L into bit fields: type tag, line number, parent ids, principal row j, self-reduction node address a, list Occ_h(L)=((r_t,occ_t,parent_t,sign_t))_{t<s_L}, and local child-link hashes.
- Run the local verifier: for each tuple, check that r_t is a legal row index, occ_t addresses an occurrence in G_N(x,r_t), parent_t points to either L's principal node or an earlier listed node, and sign_t matches the SR recurrence used by the rule.
- Construct a prefix block B_L with fresh extension variables for every listed SAT atom and every local Boolean connective in the bounded SR recurrence; derive the same conclusion as L by ordinary bEF reasoning over the listed rows.
- Maintain the induction invariant K_pre(i)=all row ids appearing in earlier normalized lines plus all Occ_h blocks already expanded. The normalized i-th line mentions only rows in K_pre(i) union Occ_h(i).
- Charge B_L by c_SR |Occ_h(L)| N^{o(1)} plus parent-pointer overhead; summing over at most |pi| lines gives the eta+tau exponent bound.
- Compose the normalized proof with the existing generator circuit of size N^{rho+o(1)} and row-expansion debt O(E_pi N). If the total is below N^{1+epsilon-o(1)}, it is a same-model SIZE circuit contradicting LB_N(1+epsilon), hence a valid route-level falsifier.
- Test the necessity of annotation by omitting one child row from Occ_h(L). The parser transcript remains unchanged under a private-row SAT-value flip, while the semantic SR conclusion can change; therefore occurrence-only completion is invalid for unannotated SR.

Blocking gap: The derivation proves only the annotated row-faithful bounded-SR_h schema. Arbitrary semantic self-reduction or real-SAT FormulaEval remains blocked at OccNeighborhoodRealizer_N/RealSATInfluenceRealizer_N.

## Falsifiers

- Unannotated SR line with a private child row omitted from Occ_h(L): visible transcript equality but H_N^SAT parity flips.
- Quantitative threshold collapse: if tau+eta>=epsilon-o(1), the SR expansion charge alone can exceed the support-forcing margin, so the subthreshold LB_N falsifier is unavailable.
- Semantic FormulaEval-SAT choosing child rows by real SAT truth rather than proof-visible syntax: no advice-free occurrence parser is valid without RealSATInfluenceRealizer_N.
- Nonuniform row advice table embedded in selector code: row support is not target-preserving because the parser cannot distinguish proof information from hidden SAT advice.

## Learning

Cycle 126 adds a rule-level proof packet: annotated bounded-SR_h has an explicit Gap98 normal form with charge N^{tau+eta+o(1)}, while the first omitted child row is a finite falsifier to unannotated occurrence parsing. This is valid proof-system certification, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch needs a concrete test that separates annotated bounded-SR_h transparency from semantic row leakage; another abstract barrier restatement would not discharge Gap98-SRhNormalForm or its countermodel boundary.
- Situation seed: A padded SAT-parity family H_N^SAT with one bounded-SR_h proof line deriving a SAT self-reduction identity; in the annotated version all child rows are listed in Occ_h(L), while in the unannotated version one private child row r* is selected by an unread enable bit.
- Varied variable: eta in the row-touch budget h=N^{eta+o(1)} for the bounded-SR_h line.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and claimed threshold LB_N(1+epsilon)., Same nonuniform SIZE target model and same bEF proof theory before and after prefix splicing., No-advice deterministic parser; visible rows must be recoverable from proof bits and G_N only., The private-row perturbation changes only SAT(G_N(x,r*)) and preserves every listed occurrence neighborhood.
- Expected observation: For eta+tau<epsilon-rho-o(1), annotated SR expansion remains subthreshold and yields the parser-to-circuit falsifier. In the unannotated case, the first omitted row produces transcript bisimulation and invalidates occurrence completion regardless of the small eta value.
- Transfer certificate needed: A formal OccNeighborhoodRealizer_N certificate: every influencing SR child row is uniformly listed, locally verified, charged in Gamma_bEF^SR, and prefix-spliceable in the same theory before the intuition may affect proof obligations.

## Next Experiment

Convert L126.1 into a paper-ready verifier table: enumerate exact bit fields for one bounded-SR_h rule, prove the prefix-splice bEF derivation line by line, and recompute the q/epsilon trichotomy after adding the N^{tau+eta+o(1)} SR charge.

# MCSP / Meta-Complexity Carrier Transfer: prefix-causal FormulaEval support audit

## Candidate Lemma

For Psys_sym^time proofs whose FormulaEval lines expose all influential rows in the prefix before the line is checked, the least time-closed cone K_time(pi) yields a same-model parser-to-circuit upper bound. Hence any proof of LB_N(1+epsilon) with subthreshold Gamma_time is falsified inside the intended nonuniform SIZE model; this is a route obstruction, not P != NP progress.

## Definitions

- source object: a bit-explicit Psys_sym^time transcript pi for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)}, and FormulaEval lines carrying timestamped selector/enumerator certificates.
- target object: a same-theory nonuniform SIZE circuit computing the asserted hard target H_N^SAT on length N, used only as a falsifier for a claimed LB_N(1+epsilon) proof.
- controlled interface: prefix-causal transparent FormulaEval, meaning the proof prefix before line a uniformly determines every influential row set R_a, its enumerator cost U_a, and its occurrence expansion cost X_a, with no SAT-truth advice.
- target-preserving condition: the parser, row expansions, and extracted circuit remain in the same nonuniform SIZE model and length regime as LB_N, and all support discovery is advice-free and prefix-visible before the semantic value is used.
- K_time(a) is the least fixed point over lines <=a adding non-FormulaEval syntactic dependencies and every row enumerated by a prefix-visible FormulaEval certificate before its line.
- Delta K_a=K_time(a)\K_time(a-1) is the newly charged influential row set at line a.

## Assumptions

- Model: Psys_bEF^- non-FormulaEval rules have the Gap98-SRhNormalForm parser with eta/tau costs already charged in Gamma_bEF(pi).
- Regime: N tends to infinity, M_N=N^{q+o(1)}, formula length and row occurrence neighborhoods are N^{o(1)} unless explicitly charged.
- Uniformity/advice: selector code, enumerator code, and row-expansion certificates are computable from N and the proof prefix; no nonuniform hard-row choice or SAT-truth pruning is allowed.
- Same-theory condition: each expanded row is the actual occurrence-level formula G_N(x,j) used by H_N^SAT, not a semantic surrogate with hidden extensional equality.
- Cutoff: the contradiction applies only when the extracted upper bound is below N^{1+epsilon-o(1)} in the target SIZE model.

## Equations

- H-target: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\qquad M_N=N^{q+o(1)}`. Valid when: Valid when the beta-zero parity target and row generator family G_N are fixed before the proof transcript is parsed.
- time-ledger: `\Gamma_{time}(\pi)=\Gamma_{bEF}(\pi)+\sum_{a\in FE(\pi)} U_a+\sum_{a\in FE(\pi)} X_a+O(E_\pi N^{1+o(1)})`. Valid when: Applies when every FormulaEval line has prefix-visible support certificates and non-FormulaEval lines satisfy the established bit-explicit Gamma_bEF parser normal form.
- row-expansion-charge: `X_a\ge N^{1+o(1)}\,|\Delta K_a|`. Valid when: Requires occurrence-level same-theory expansion of every newly influential SAT row before the FormulaEval line can affect the final lower-bound assertion.
- upper-bound-falsifier: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{time}(\pi)`. Valid when: Valid after the prefix-causal parser reconstructs the final parity circuit using the generator circuit and all charged row expansions without hidden advice.
- subthreshold-contradiction: `N^{\rho+o(1)}+\Gamma_{time}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow \pi\text{ is not a valid same-model proof of }LB_N(1+\epsilon)`. Valid when: Applies in the nonuniform SIZE target model when LB_N asserts no circuits of size N^{1+epsilon-o(1)} for the same H_N^{SAT} family.

## Attempted Derivation

- Define K_time(0)=empty. Process proof lines in order. For non-FormulaEval rules, add only the already parsed local bit fields charged by Gamma_bEF.
- At a FormulaEval line a, require the prefix to contain selector code S_a, an advice-free enumerator Enum_a, and row-expansion witnesses for every row whose value can influence FE_a. Run Enum_a before accepting line a; add its output to K_time(a).
- Maintain invariant I(a): every value in the parsed prefix that can affect the final LB_N line is a Boolean function of the generator bits, the charged syntactic proof fields, and the row truth values indexed by K_time(a), with circuit cost at most N^{rho+o(1)} plus accumulated ledger.
- For transparent FE_a, replace each newly added row by its same-theory occurrence expansion G_N(x,j), paying X_a>=N^{1+o(1)}|Delta K_a|; compose with the selector/evaluator circuit paying U_a.
- For the final lower-bound line, I(final) yields a nonuniform SIZE circuit for H_N^SAT of size N^{rho+o(1)}+Gamma_time(pi). If this is below N^{1+epsilon-o(1)}, the transcript cannot be a valid proof of LB_N(1+epsilon) in the same model.
- For the negative half, choose the first line a with r in Infl(a)\K_time(a-1). Since r is not prefix-visible, construct two surface completions agreeing on all prefix reads and flipping the private row or enable bit. The FormulaEval value differs, so the parser induction cannot be sound.

Blocking gap: Full semantic SAT truth pruning is not refuted as a mathematical inference rule; it is quarantined because the controlled parser lacks a prefix-causal RealSATInfluenceRealizer_N proving and charging all semantic influences before use.

## Falsifiers

- Post-hoc K_dag support: a row listed after the FormulaEval line is not valid because zero prefix latency is required.
- SAT-truth branch pruning without an advice-free influence certificate is a concrete hidden-support falsifier.
- Membership-only AC0 or projected selectors without output-sensitive enumeration pay full scan or become semantic-oracle cases.
- Advice-selected hard rows, ranked truth-table choices, or nonuniform pruning tables do not transfer to a uniform target language lower bound.
- An unread enable bit controlling a private branch gives two prefix-identical completions with different FormulaEval values.

## Learning

The new audit point is prefix causality: transparent FormulaEval is valid only when the proof prefix already determines and charges every influential row. This converts semantic pruning from a vague escape into a zero-latency realizer obligation or a private-branch falsifier, preserving a scoped parser obstruction rather than claiming P vs NP progress.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The live theorem boundary is no longer abstract MCSP transfer; it is whether a concrete semantic FormulaEval rule can be made prefix-causal without SAT-truth advice. A thought experiment isolates the latency parameter that decides transparency versus private-branch falsifier.
- Situation seed: Bounded Tseitin/self-reduction FormulaEval for H_N^SAT where a line branches on b variables of G_N(x,j), either enumerating all 2^b child rows or pruning children using semantic SAT truth.
- Varied variable: prefix support latency lambda, where lambda=0 means every influential branch is listed before the FormulaEval line and lambda>0 means some influential branch is revealed only later or never.
- Held-fixed controls: The target family H_N^SAT and generator overhead N^{rho+o(1)} are fixed., The target lower-bound claim remains same-model nonuniform SIZE LB_N(1+epsilon)., No advice, SAT-truth table, or nonuniform row selector is permitted in the transparent interface., The row-expansion cost per newly influential branch is charged as N^{1+o(1)}.
- Expected observation: At lambda=0 the rule enters the Gamma_time ledger with cost at least 2^b N^{1+o(1)}. At any positive or hidden latency, the first omitted branch supports a private-branch falsifier unless an explicit RealSATInfluenceRealizer_N proves noninfluence before use.
- Transfer certificate needed: A prefix-causal, advice-free RealSATInfluenceRealizer_N that lists every semantic influential or pruned-sensitive branch, supplies same-theory row witnesses, and adds its overhead R_N to Gamma_time before the FormulaEval line is accepted.

## Next Experiment

Instantiate K_time on a toy bounded self-reduction line with b=2: list the four branch row encodings, compute U_a and X_a, then delete one semantically pruned branch and write the two prefix-identical private-branch completions explicitly.
