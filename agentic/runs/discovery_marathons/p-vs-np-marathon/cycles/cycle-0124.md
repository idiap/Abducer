# cycle-0124

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For Psys_sym^dag augmented by a declared bounded Tseitin self-reduction FormulaEval rule, the least reachable support cone can be extended from K_dag(pi) to K_TSR(pi) by adding all syntactically declared restriction children. This gives an advice-free RealSATInfluenceRealizer_N for this rule and a valid same-model parser-to-circuit falsifier whenever the resulting Gamma_TSR charge is below N^{1+epsilon-o(1)}. This is a scoped parser/falsifier theorem, not a proof of P != NP.

## Definitions

- source object: H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, beta-zero polylog formula rows, generator cost N^{rho+o(1)}, and claimed same-model lower bound LB_N(1+epsilon).
- target object: a restricted proof-system theorem for Psys_sym^{dag+TSR_decl} showing that a parsed lower-bound proof with subthreshold charged support yields a SIZE upper-bound falsifier for H_N^SAT.
- controlled interface: declared Tseitin-SR FormulaEval lines expose root row, Tseitin map, pivot schedule, child-row constructor, parent pointers, and proof-DAG uses before the semantic line is consumed.
- target-preserving condition: all row expansions are same-theory SAT rows, no SAT-truth advice chooses support, the circuit model is nonuniform SIZE on the same length N, and beta=0 is preserved.
- K_TSR(pi) is the least fixed point containing final-line dependencies and closed under proof-DAG parents, transparent FormulaEval support, and declared TSR child rows.
- A declared TSR line has the form SAT(T_a)=OR_{b in {0,1}^{h(a)}} SAT(T_{a,b}), where T_{a,b} is the bit-explicit restriction/Tseitin row named by the rule syntax.

## Assumptions

- Length regime: N tends to infinity, M_N=N^{q+o(1)}, row formula length L_N=(log N)^{d+O(1)}, and epsilon>0 is fixed before the proof family is chosen.
- Uniformity/advice regime: the realizer receives only N and the proof syntax pi_N; it may use deterministic polynomial-time parsing but no nonuniform list of hidden rows.
- Semantic validity regime: each declared Tseitin equivalence and each restriction step has an EF-checkable same-theory derivation of size L_N^{O(1)} per row instance.
- Circuit model regime: the falsifier circuit and the claimed LB_N lower bound are both measured in the same nonuniform SIZE model, with equality patches charged as O(E_pi N).
- Depth regime: 2^{h_N}=N^{theta+o(1)} for the charged TSR height used on the relevant support cone; theta may be zero for constant or polylogarithmic height.
- Boundary regime: arbitrary semantic FormulaEval rules are not covered unless their influences are listed by this declared child-row constructor or by a separate RealSATInfluenceRealizer_N certificate.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j<M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad |G_N(x,j)|=L_N=(\log N)^{d+O(1)}`. Valid when: Valid when the beta-zero parity carrier and generator length regime are fixed before parsing proofs.
- tsr_closure: `K_{TSR}(\pi)=\mu K\,[Reach(final)\cup Cl_{dag}(K)\cup \{child(a,b):a\in K,\ b\in\{0,1\}^{h(a)}\}]`. Valid when: Applies when every TSR line exposes its parent row and all restriction-child row constructors syntactically.
- gamma_charge: `\Gamma_{TSR}(\pi)=\Gamma_{bEF}(\pi)+U(K_{TSR})+X(K_{TSR})+R_{TSR},\quad X(K_{TSR})\le N\,|K_{TSR}|\,L_N^{O(1)}`. Valid when: Requires the charged support cone to be uniformly enumerable and expanded in the same SAT row theory.
- height_threshold: `|K_{base}|=N^{\kappa+o(1)},\ 2^{h_N}=N^{\theta+o(1)}\ \Longrightarrow\ \Gamma_{TSR}\le \Gamma_{bEF}+N^{1+\kappa+\theta+o(1)}`. Valid when: Valid when TSR closure is the only new source of FormulaEval rows beyond the base reachable cone.
- same_model_falsifier: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{TSR}(\pi)+O(E_\pi N)`. Valid when: Applies after the parser line induction converts every charged proof dependency into a same-model circuit component.
- subthreshold_contradiction: `N^{\rho+o(1)}+\Gamma_{TSR}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\ \Longrightarrow\ \neg LB_N(1+\epsilon)`. Valid when: Requires the source lower-bound statement to be exactly the same nonuniform SIZE lower bound for H_N.

## Attempted Derivation

- Fix Psys_sym^{dag+TSR_decl}. Each proof line exposes a type tag: bEF, transparent FormulaEval, or TSR_decl. A TSR_decl line contains row id a, formula/Tseitin code T_a, pivot list p_1,...,p_h, and a uniform constructor for each restricted child T_{a,b}.
- Define K_TSR(pi) by fixed-point iteration. Initialize with rows reachable from the final LB_N line. Add proof-DAG parents. For a transparent FormulaEval line, add its surfaced support as in L120. For a TSR_decl line, add all children child(a,b) for b in {0,1}^{h(a)} and the EF-checkable Tseitin equivalence rows.
- Termination and auditability are finite because the proof DAG and every declared child list are finite; the parser does not ask whether a child is satisfiable. Enumeration cost is U(K_TSR)<=|pi|L_N^{O(1)}+|K_base|2^{h_N}L_N^{O(1)} before row expansion.
- Extend the L120 line-induction invariant. bEF and transparent lines use the previous proof. For a TSR_decl line, the same-theory EF derivation justifies SAT(T_a)=OR_b SAT(T_{a,b}); all child row truth values are already in K_TSR, so the semantic line has no hidden influence.
- The resulting transcript circuit has size at most N^{rho+o(1)}+Gamma_bEF+U(K_TSR)+X(K_TSR)+R_TSR+O(E_pi N). If this is below N^{1+epsilon-o(1)}, it is a valid same-model falsifier for LB_N(1+epsilon).
- For a branch-pruning variant where the rule names only one child chosen by SAT truth, repeat the private-row construction: two completions agree on all surfaced rows and proof syntax but disagree on the hidden child and on one carrier parity bit. Thus no advice-free parser can charge only visible support.

Blocking gap: The proof does not cover arbitrary full semantic FormulaEval. The named remaining gap is RealSATInfluenceRealizer_N^arb: every semantic inference must uniformly reveal all rows whose labels can affect later proof use before the inference is consumed.

## Falsifiers

- Hidden branch bit: a self-reduction line chooses b*(a) from SAT truth without exposing both children; the private-row falsifier keeps the transcript fixed while changing H_N on one source input.
- Height threshold collapse: if |K_base|=N^{kappa+o(1)} and 2^{h_N}=N^{theta+o(1)} with kappa+theta>=epsilon, the row expansion N|K_TSR| is not subthreshold.
- Same-theory failure: a restricted child formula cannot be represented as a Psys row with EF-checkable Tseitin equivalence, so the line induction is invalid.
- Advice leakage: the child-row constructor or reachable support list contains nonuniform SAT-truth advice rather than visible proof syntax.
- Positive beta regression: if the carrier interface reintroduces target query length n^beta with beta>0, the old q+beta c substitution falsifier caps all-exponent transfer.
- Naturalness status falsifier: any dense label-functional certificate over K_TSR must still pass the earlier functional naturalization audit; declared TSR only handles semantic influence, not natural proofs.

## Learning

Cycle 124 makes the semantic boundary sharper: bounded Tseitin self-reduction is foldable into the least-support theorem only when every restriction child is declared and charged. The exact threshold is kappa+theta<epsilon for the new row expansion. Hidden branch-pruning is a concrete private-row falsifier, so full semantic FormulaEval remains blocked at RealSATInfluenceRealizer_N^arb rather than at generic barrier folklore.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a threshold and countermodel probe.`
- Rationale: The branch already has K_dag; the next valid improvement is to test whether a concrete SAT-semantic rule can be folded into the charged support theorem rather than restating the semantic gap.
- Situation seed: A beta-zero parity carrier H_N^SAT with M_N=N^q generated polylog SAT rows; a proof pi has a projected-dDNNF transparent core plus one declared Tseitin self-reduction FormulaEval line per reachable support row.
- Varied variable: Self-reduction height exponent theta where 2^{h_N}=N^{theta+o(1)}.
- Held-fixed controls: q, rho, epsilon, and beta=0 are fixed throughout the experiment., The same nonuniform SIZE model is used for LB_N and for the falsifier circuit., All child rows are same-theory SAT rows with EF-checkable Tseitin/restriction derivations., No hidden SAT-truth advice may select rows; support must be proof-syntax enumerable.
- Expected observation: As theta increases, the charged cone size grows from N^{kappa} to N^{kappa+theta}; the parser theorem remains threshold-valid exactly while kappa+theta<epsilon, and the hidden-branch variant fails even at theta=0 without a realizer.
- Transfer certificate needed: A formal RealSATInfluenceRealizer_N^{TSR_decl} certificate: deterministic enumeration of all child rows, same-theory row expansions, EF derivations of each Tseitin/restriction identity, and inclusion of R_TSR in Gamma before invoking the semantic line.

## Next Experiment

Write the FE_TSR_decl rule schema as bit fields: row id, Tseitin code, pivot list, child constructor, parent pointers, and EF derivation handles; then check the fixed-point K_TSR enumerator on a one-line bounded-SR example and a hidden satisfying-branch counterexample.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For the concrete semantic FormulaEval rule consisting of Tseitin-extension equality plus bounded self-reduction, RealSATInfluenceRealizer_N is valid if every extension and self-reduction line carries proof-visible parent pointers and row-cover certificates. The rule then folds into the transparent support theorem with an added charged ledger R_N^{tSR}.

## Definitions

- source object: Psys_sym^tSR proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with FormulaEval-Tseitin and bounded-SR lines annotated by parent pointers and row-cover certificates.
- target object: same-model nonuniform SIZE upper-bound falsifier for LB_N(1+epsilon), or equivalently forced row-equivalent support in any sound short pi.
- controlled interface: advice-free RealSATInfluenceRealizer_N that maps each semantic FormulaEval line a to an explicit influence row set R(a), a same-theory row-expanded bEF splice, and a ledger charge R_N(a).
- target-preserving condition: N, pi, and visible annotations determine all row sets before semantic SAT truth is consulted; expansion uses no nonuniform advice and remains inside the beta-zero H_N^SAT carrier.
- observable: K_tSR(pi) is the least prefix-closed reachable set of row indices reached from the final LB_N line by following parent pointers, self-reduction children, and row-cover certificates.
- ledger: U_N charges row enumeration, X_N charges row-expanded FormulaEval material, R_N^{tSR} charges annotated semantic Tseitin/SR realization, and Gamma_bEF is the pre-existing bit-explicit bEF transcript charge.

## Assumptions

- Length regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, generator overhead size(G_N)=N^{rho+o(1)}, and rho<1+epsilon.
- Proof model: Psys_sym^tSR extends the bit-explicit bEF/SATeq/bounded-SR_h system only by annotated FormulaEval-Tseitin equality and bounded self-reduction rules.
- Uniformity: the worklist computing K_tSR(pi) is deterministic polynomial time in the displayed proof and uses no SAT-truth advice, selector advice, or hidden row oracle.
- Same-theory condition: each realized FormulaEval line is prefix-spliced with fresh extension variables before its first use, preserving the original proof order and proof theory.
- Row-cover validity: each certificate locally verifies C_t={j} for a literal row atom A_j and C_t=union C_u over visible parents for extension or SR-composition nodes.
- Naturalness boundary: the lemma is a parser/falsifier theorem; it becomes a natural-proof object only if the induced truth-table property is also large, constructive, and useful against the named SIZE class.

## Equations

- K_tSR fixed point: `K_tSR(pi)=lfp({final LB line}; parent, SR-child, and row-cover edges)`. Valid when: Valid when the source proof is in annotated Psys_sym^tSR and every FormulaEval dependency has a visible row-cover certificate.
- semantic realization charge: `R_N^{tSR}(pi) <= N*|K_tSR(pi)| + N^{o(1)}*Edges_tSR(pi)`. Valid when: Valid when row atoms expand to N-bit bEF material and all parent-edge checks have polylogarithmic encodings.
- total charged transcript: `Gamma_tSR(pi)=Gamma_bEF(pi)+U_N+X_N+R_N^{tSR}(pi)`. Valid when: Applies after prefix-splicing replaces each annotated semantic FormulaEval line by same-theory row-expanded material before use.
- subthreshold upper-bound falsifier: `N^{rho+o(1)}+Gamma_tSR(pi)+O(E_pi*N)<N^{1+epsilon-o(1)} => C(H_N^SAT)<N^{1+epsilon-o(1)}`. Valid when: Requires the generator circuit, expanded proof transcript, and extension overhead all live in the same nonuniform SIZE model.
- forced row-equivalent support: `S_eff^{tSR}(pi):=(Gamma_tSR(pi)+O(E_pi*N))/N >= N^{epsilon-o(1)}`. Valid when: Valid for sound proofs of LB_N(1+epsilon) once rho<1+epsilon and the subthreshold falsifier implication is contraposed.
- visible-row density corollary: `|K_tSR(pi)|/M_N >= N^{epsilon-q-o(1)}`. Valid when: Applies when U_N, X_N, Gamma_bEF, and nonrow extension debt are o(N^{1+epsilon}) compared with N*|K_tSR(pi)|.

## Attempted Derivation

- Choose the concrete semantic rule: FormulaEval may introduce Tseitin extension gates and bounded self-reduction nodes, but every node must display parent pointers and a row-cover certificate.
- Run a worklist from the final LB_N line. For each FormulaEval root, add its displayed parents, check local cover equations, and insert every certified row into K_tSR(pi).
- For a row atom A_j=SAT(G_N(x,j)), splice the already available row-expanded bEF material for G_N(x,j) with charge O(N).
- For a Tseitin gate e_t=op(e_u,e_v), splice a fresh extension definition after the prefixes realizing e_u and e_v; the cover equality C_t=C_u union C_v proves no hidden row entered.
- For a bounded-SR node, charge the displayed child-neighborhood list and splice its row-expanded children before the rule application; bounded h only affects the enumerator and edge ledger.
- Induct over proof lines: bEF/SATeq lines use Gamma_bEF; annotated FormulaEval lines use the prefix splice and add R_N^{tSR}; ordinary proof order is preserved by fresh variables.
- Combine the expanded transcript with the generator circuit of size N^{rho+o(1)}. If the total charge is below N^{1+epsilon-o(1)}, it builds a same-model SIZE circuit for H_N^SAT, contradicting LB_N(1+epsilon).
- For the unannotated variant, take the first semantically influential row omitted from the extracted cover; toggle that private row while preserving the surface transcript and all charged rows to obtain the finite falsifier.

Blocking gap: The derivation does not settle arbitrary semantic FormulaEval. The remaining named gap is RealSATInfluenceRealizer_N for unannotated semantic equivalence rules whose influential rows are not determined by proof-visible covers.

## Falsifiers

- q<epsilon with small Gamma_tSR gives a same-model upper-bound falsifier for any claimed LB_N(1+epsilon).
- A first omitted reachable row in a cover certificate is a private-row falsifier for the claimed FormulaEval expansion.
- An unread enable bit selecting row r while leaving r absent from the proof-visible transcript refutes advice-free realization.
- Nonuniform row-selector advice can make the parser appear complete while losing the target-preserving no-advice condition.
- A row-cover verifier that checks syntactic equality but not extensional union permits hidden projected-dDNNF influence.

## Learning

Cycle 124 makes a rule-level move: RealSATInfluenceRealizer_N is valid for annotated Tseitin/SR FormulaEval with visible row covers, and invalid for the unannotated hidden-row variant by a finite falsifier. Live inference-quality packet: source_statement=short Psys_sym^tSR proof pi of LB_N(1+epsilon) for H_N^SAT; target_statement=Gamma_tSR same-model SIZE upper-bound falsifier or forced row-equivalent support; model_context=nonuniform Boolean SIZE, beta-zero SAT-parity carrier, bEF plus annotated semantic FormulaEval, simulation/extraction rather than many-one reduction; quantifier_context=N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, size(G_N)=N^{rho+o(1)}, rho<1+epsilon, deterministic no-advice row-cover worklist; derivation_status=restricted rule derived, arbitrary semantic FormulaEval still blocked at unannotated RealSATInfluenceRealizer_N; reviewer_findings=target-preserving only with visible covers and same-theory prefix splicing, naturalness pressure is conditional, and there is no claim toward P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and threshold calibration for the annotated Tseitin/SR rule.`
- Rationale: The branch has repeatedly isolated RealSATInfluenceRealizer_N abstractly; this concrete rule tests whether semantic FormulaEval can be charged before broadening to arbitrary SAT semantics.
- Situation seed: Let G_N(x,j) be the beta-zero padded SAT-query generator and let a FormulaEval proof introduce a Tseitin DAG whose leaves are row atoms A_j=SAT(G_N(x,j)); the proof claims LB_N(1+epsilon) for H_N^SAT.
- Varied variable: The row-cover exponent chi where |K_tSR(pi)|=N^{chi+o(1)}.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, and H_N^SAT is the xor over the same row family., Generator overhead remains N^{rho+o(1)} with rho<1+epsilon., The proof checker is deterministic, prefix-ordered, and advice-free., The target class is the same nonuniform Boolean SIZE threshold N^{1+epsilon}., Every accepted annotated run must expose parent pointers and cover certificates before SAT truth is queried.
- Expected observation: If chi<epsilon and all nonrow debt is subcritical, the expanded transcript yields the upper-bound falsifier; if a reachable row is omitted, toggling that row gives the private-row countermodel; only chi>=epsilon can support a sound transparent proof without extra debt.
- Transfer certificate needed: A verified local row-cover theorem plus prefix-splice same-theory expansion showing that K_tSR(pi) contains every semantically influential row and that R_N^{tSR} is fully charged in Gamma_tSR.

## Next Experiment

Write the finite verifier for annotated Tseitin/SR row covers: specify node encodings, parent fields, cover union checks, prefix-splice order, and one minimal hidden-enable counterexample where the first omitted row changes FormulaEval truth.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Time-stamped least-closed support theorem for transparent FormulaEval: in Psys_sym^dag, if every FormulaEval use has prefix-visible support certificates and advice-free row enumeration before the line is used, then the parser computes a minimal prefix-respecting cone K_time(pi), derives Gamma_dag(pi), and obtains the same-model SIZE upper-bound falsifier. Post-hoc support certificates do not count as transparent support.

## Definitions

- source object: a bit-explicit Psys_sym^dag proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, bounded-SR_h rules, and FormulaEval lines carrying visible selector code, parent pointers, projection witnesses, and row-support certificates.
- target object: a same-theory nonuniform Boolean SIZE circuit for H_N^SAT of size N^{rho+o(1)}+Gamma_dag(pi)+O(E_pi N), used only as a falsifier for low-cost claimed LB_N(1+epsilon) transcripts.
- controlled interface: K_time(pi), the least prefix-respecting reachable support cone obtained by a worklist that may add rule predecessors, enumerated rows, projection-witness rows, and influence edges only from proof bits available at or before the line where they are used.
- target-preserving condition: the parser uses no SAT-truth advice, all row expansions are in the same occurrence-level SAT language as the proof, every nonuniform choice is either an explicit transcript bit or a charged certificate, and semantic FormulaEval without an influence realizer is quarantined.
- DeltaK_l is the set of row indices newly charged at FormulaEval line l after earlier charged rows are removed.
- U_l is the certified row-discovery or full-scan cost visible before line l; X_l=N^{1+o(1)}|DeltaK_l| is the same-theory row-expansion charge.

## Assumptions

- Length regime: N tends to infinity, M_N=N^{q+o(1)}, formula/query length is N^{o(1)}, generator G_N has circuit overhead N^{rho+o(1)}, and epsilon>0 is fixed.
- Proof model: Psys_sym^dag is Cook-Reckhow bit explicit, contains the finalized bounded-SR_h parser rules, and permits FormulaEval only through prefix-visible support certificates or full scan.
- Uniformity/advice regime: the K_time worklist, row enumerators, projection de-duplicators, and expansion templates are computed from N and pi with no SAT-truth advice and no hidden row selector.
- Circuit model: the target upper bound is nonuniform Boolean SIZE on the same input length and same SAT occurrence encoding; the simulation is a parser-to-circuit construction, not a proof of P != NP.
- Barrier status: the positive theorem is non-large and syntactic; the blocked full semantic FormulaEval case is a nonrelativizing influence-realizer issue, not generic natural-proofs folklore.

## Equations

- Ktime-fixedpoint: `K_time(pi)=least prefix-respecting fixed point of Worklist(seed=final LB line; add Pred_l, Rows_l, Infl_l only from proof prefix <= l)`. Valid when: Valid when each proof line has explicit parent pointers and every FormulaEval support certificate is available before the semantic use it justifies.
- incremental-support-ledger: `DeltaK_l=(Rows_l cap K_time(pi)) minus union_{i<l} Rows_i; U_dag=sum_l U_l; X_dag=sum_l N^{1+o(1)} |DeltaK_l|`. Valid when: Valid when row enumerators output distinct row identifiers or provide a certified de-duplication mechanism charged in U_l.
- gamma-ledger: `Gamma_dag(pi)=Gamma_bEF(pi)+U_dag(pi)+X_dag(pi)`. Valid when: Valid when the bounded-SR_h normal form supplies Gamma_bEF and every FormulaEval line satisfies the prefix-transparent support interface.
- same-model-upper-bound: `SIZE(H_N^SAT) <= N^{rho+o(1)}+Gamma_dag(pi)+O(E_pi N)`. Valid when: Applies after generator overhead, parsed transcript gates, extension overhead, and row expansions are all in the same nonuniform SIZE model.
- low-cost-transcript-falsifier: `N^{rho+o(1)}+Gamma_dag(pi)+O(E_pi N) < N^{1+epsilon-o(1)} => pi is not a valid same-model proof of LB_N(1+epsilon)`. Valid when: Valid when LB_N(1+epsilon) asserts a nonuniform SIZE lower bound for exactly the H_N^SAT family simulated by the parser.

## Attempted Derivation

- Fix N and a Psys_sym^dag transcript pi purporting to prove LB_N(1+epsilon) for H_N^SAT in the same nonuniform SIZE model.
- Parse every line into rule tag, parent pointers, formula-node fields, row-selector code, projection-witness fields, and declared support-certificate pointers; reject lines whose certificates point only forward unless the rule explicitly permits delayed definition and charges it before semantic use.
- Seed a backward worklist at the final LB_N line, but when processing a line l allow only predecessors and support objects contained in pi_{<=l}; this defines the prefix-respecting K_time cone.
- For bounded-SR_h and bit-explicit bEF rules, import the finalized Gamma_bEF line-induction charge and add only syntactic predecessors.
- For a transparent FormulaEval line l, run the prefix-visible enumerator or full scan, de-duplicate projected rows if certified, add DeltaK_l, and charge U_l+N^{1+o(1)}|DeltaK_l|.
- Maintain the invariant that any two occurrence completions agreeing on proof bits and all rows in the current prefix cone give identical values to every processed line; FormulaEval preservation follows exactly from influence closure.
- Assemble a nonuniform circuit for H_N^SAT from G_N, parsed transcript gates, row expansions, and extension overhead, giving SIZE(H_N^SAT)<=N^{rho+o(1)}+Gamma_dag(pi)+O(E_pi N).
- If this size is below N^{1+epsilon-o(1)}, the transcript is a same-model upper-bound falsifier for its own claimed lower bound; if a first semantic influence is not in the prefix cone, the private-row countermodel replaces the positive induction.

Blocking gap: No remaining gap for prefix-visible Psys_sym^dag as a restricted parser theorem, assuming Gap98-SRhNormalForm and same-theory row expansion are accepted. Full semantic FormulaEval remains blocked at the named RealSATInfluenceRealizer_N obligation; membership-only AC0 selectors remain scan-charged unless an output-sensitive enumerator is proved.

## Falsifiers

- Post-hoc support certificate: a row-support witness appears after the FormulaEval line that semantically used it and has no charged predecessor edge before use.
- Unread enable bit: two occurrence completions agree on all visible rows but flipping an uncharged enable bit changes the selected FormulaEval row set.
- Hidden projection fiber: projected-dDNNF membership is small, but auxiliary witnesses reveal additional influencing rows not de-duplicated and charged in K_time.
- Membership-only AC0 selector: the selector answers row membership but lacks an output-sensitive row enumerator, forcing full scan or private-row failure.
- SAT-truth advice leakage: the row selector or RealSAT influence set is chosen using nonuniform SAT values rather than transcript-visible code.
- Model mismatch: the parser expands rows in a different formula language or circuit model than the LB_N(1+epsilon) statement.
- Semantic UExtWitnessability failure: formula identity is asserted extensionally without an advice-free quotient or influence witness.

## Learning

Cycle 124 closes a proof-audit loophole: transparent support must be prefix-visible at the line where semantic FormulaEval is used. A global after-the-fact K_dag explanation is insufficient. The strengthened K_time theorem preserves the valid parser-to-circuit falsifier and converts post-hoc semantic support into a concrete private-row countermodel, while leaving only RealSATInfluenceRealizer_N as the full-semantic escape.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The remaining proof risk is not another abstract barrier but whether chronological support visibility is necessary for the transparent FormulaEval theorem. A concrete timestamp experiment tests exactly the post-hoc support loophole.
- Situation seed: Take H_N^SAT with M_N=N^q rows and a Psys_sym^dag transcript containing one projected-dDNNF FormulaEval line l. The selector visibly enumerates T=N^a rows, while one eval-critical row j* is controlled by an auxiliary enable certificate that can be placed before l, after l, or omitted.
- Varied variable: The timestamp position lambda of the first certificate for j* relative to FormulaEval line l: lambda<0 before use, lambda>0 post-hoc after use, lambda=infinity omitted.
- Held-fixed controls: Fixed target statement LB_N(1+epsilon) for the same H_N^SAT family and same nonuniform SIZE model., Fixed generator overhead N^{rho+o(1)}, M_N=N^{q+o(1)}, and row-expansion cost N^{1+o(1)} per charged row., Fixed no-advice parser: the worklist sees only N and proof bits, never SAT-truth advice., Fixed projected-dDNNF syntax and de-duplication rules except for the timestamp of j*'s certificate.
- Expected observation: When lambda<0, j* enters K_time before l and the ledger pays U_l+N^{1+o(1)}. When lambda>0 or infinity, two prefix completions agree on all charged data before l but differ on Eval_l, producing a finite private-row falsifier. This separates valid transparent support from invalid post-hoc repair.
- Transfer certificate needed: A formal prefix-respecting K_time induction plus a same-theory private-row construction. For any semantic rule escaping this test, the needed certificate is a RealSATInfluenceRealizer_N that lists and charges all influencing rows before semantic use.

## Next Experiment

Write the referee-checkable K_time pseudocode and instantiate it on one Tseitin-extension equality plus bounded self-reduction FormulaEval rule: either produce a prefix-visible RealSATInfluenceRealizer_N with charge R_N, or exhibit the first uncharged semantic inference and the corresponding private-row countermodel.
