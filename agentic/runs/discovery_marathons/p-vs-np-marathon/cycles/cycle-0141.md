# cycle-0141

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For beta-zero parity carrier proofs in Psys_bEF^- plus counterfactual declared TSR, quotienting duplicate CTSR children is sound for the parser-to-circuit falsifier exactly when every quotient merge is backed by an acyclic, dependency-closed, same-theory certificate forest already contained in the charged support cone K_Q(pi). Under this interface, a subthreshold Gamma_Q(pi) yields a same-model SIZE upper bound refuting the claimed LB_N(1+epsilon) certificate; it is not a lower bound for H_N and not P != NP.

## Definitions

- source object: H_N^{SAT}(x)=xor_{j<M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, polylog SAT length L_N=(log N)^d, and Psys_bEF^-+CTSR_Q^{cert} proof pi of a source lower-bound line LB_N(1+epsilon).
- target object: a same nonuniform Boolean SIZE circuit for H_N^{SAT} of size below N^{1+epsilon-o(1)}, used as a falsifier for the proof certificate, not as a target-class separation.
- controlled interface: a parser maps pi to the least charged cone K_Q(pi) containing bit-explicit parents, counterfactual TSR children, SR leaves, FormulaEval surfaced rows, and all EqSAT quotient certificate dependencies.
- target-preserving condition: beta=0, generator overhead N^{rho+o(1)}, advice-free enumeration of K_Q(pi), no hidden SAT-truth row selection, and every quotient merge certified in the same theory before it is used.
- K_Q(pi): the least fixed point over proof-line dependency edges plus CTSR counterfactual child edges plus same-theory quotient-certificate forest edges.
- R_Q(pi): number of distinct row-slots charged by K_Q(pi) after certified quotient identifications; C_Q(pi): bit and gate cost for checking the surfaced quotient certificate forests.
- Gamma_Q(pi): Gamma_bEF(pi) plus bounded-SR, row-expansion, and quotient-certificate charges in the nonuniform SIZE ledger.

## Assumptions

- Circuit/proof model: nonuniform Boolean SIZE for H_N circuits; pi is a finite syntactic proof in Psys_bEF^- extended only by declared counterfactual TSR and certified EqSAT quotient rules.
- Length regime: N tends to infinity over valid carrier lengths; M_N=N^{q+o(1)}; L_N=(log N)^d with d>1; q,rho,eta,tau,kappa,theta,chi,epsilon are fixed constants.
- Uniformity/advice status: G_N and the parser for K_Q(pi) are uniform or explicitly encoded; K_Q may use pi as input but may not use SAT-truth advice or hidden row selectors.
- Same-theory condition: a quotient merge a~b is valid only if its certificate forest proves EqSAT(a,b) using earlier surfaced rows, EqSAT axioms, bit-explicit EF lines, or already charged CTSR dependencies.
- Counterfactual completeness: for each adaptive TSR node, all restriction children reachable in the syntactic frontier are declared before actual branch pruning is allowed.
- Error model: E_N residual bad source rows may be patched by equality tests at cost O(E_N N); the falsifier applies only when E_N<N^{epsilon-o(1)}.
- Barrier status: the positive theorem is syntactic and relativizing within the surfaced transcript; the hidden semantic escape is isolated as RealSATInfluenceRealizer_N^{arb}, so no generic natural-proofs or P vs NP claim is invoked.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j<M_N} SAT(G_N(x,j))`. Valid when: Valid when N ranges over admissible carrier lengths and G_N is the fixed advice-free generator.
- closed_support: `K_Q(\pi)=\operatorname{lfp}(S\mapsto S\cup Parents(S)\cup CTSRChild(S)\cup EqCertDeps(S))`. Valid when: Valid when every FormulaEval, CTSR, and quotient dependency is syntactically addressable before the line using it.
- ledger: `\Gamma_Q(\pi)=\Gamma_{bEF}(\pi)+O(N^{q+\eta+\tau+o(1)}+N\,R_Q(\pi)+C_Q(\pi))`. Valid when: Valid when SR leaves, row expansions, and certificate-forest checks are charged in the same SIZE model.
- transcript_upper_bound: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_Q(\pi)+O(E_NN)`. Valid when: Valid after the line induction has replaced every proof line by its charged transcript simulator.
- threshold_window: `R_Q\le N^{\kappa+\theta+o(1)},\ C_Q\le N^{\chi+o(1)},\ E_N\le N^{\delta+o(1)}\Rightarrow C(H_N)\le N^{\max\{\rho,q+\eta+\tau,1+\kappa+\theta,\chi,1+\delta\}+o(1)}`. Valid when: Valid when R_Q, C_Q, and E_N have the stated polynomial-exponent bounds uniformly in N.
- LB_falsifier_window: `\max\{\rho,q+\eta+\tau,1+\kappa+\theta,\chi,1+\delta\}<1+\epsilon\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Valid when LB_N is a claimed same-model SIZE lower bound for the carrier H_N.

## Attempted Derivation

- Define proof-line records with fields line_id, rule_tag, parent_ids, row_slot, formula_id, restriction_word, quotient_id, certificate_root, and local verifier bits.
- Initialize K_Q with the final LB_N line and close backward under bit-explicit EF parents, SATeq links, bounded-SR leaves, and FormulaEval surfaced rows.
- For each CTSR node in K_Q, add every syntactically reachable counterfactual restriction child, not merely the actual branch; this preserves extensional safety under private-row changes.
- For each quotient merge in K_Q, require a same-theory certificate forest whose leaves are earlier members of K_Q and whose conclusion is EqSAT(child_a,child_b); reject cyclic certificates by topological order on line_id and certificate_root.
- Charge N R_Q(pi) for row expansion, N^{q+eta+tau+o(1)} for bounded-SR leaves, C_Q(pi) for certificate checking, and inherit Gamma_bEF(pi) for bit-explicit EF support.
- Run line induction: each proof line in K_Q has a local circuit simulator using only charged parents; quotient lines reuse a representative only after the certificate verifier establishes same-theory equality inside the transcript.
- Assemble the carrier circuit from the generator circuit, charged row simulators, quotient representatives, and equality patches for E_N residual rows, giving C(H_N)<=N^{rho+o(1)}+Gamma_Q+O(E_NN).
- Derive the exponent window: if rho<1+epsilon, q+eta+tau<1+epsilon, kappa+theta<epsilon, chi<1+epsilon, and delta<epsilon, then the claimed LB_N(1+epsilon) certificate is invalid in the same SIZE model.

Blocking gap: The derivation is complete only for syntactic same-theory quotient certificates. It blocks for full semantic FormulaEval or adaptive pruning where the set of influencing rows is determined by real SAT truth rather than proof-visible dependencies; this is exactly RealSATInfluenceRealizer_N^{arb}.

## Falsifiers

- first uncertified quotient merge: two transcripts agree on K_Q but differ on the hidden child row
- cyclic same-theory certificate forest: quotient equality depends on its own compressed representative
- actual-branch-only TSR declaration: private-row flip at an unvisited counterfactual child changes extensional safety
- hidden SAT-semantic branch pruning without RealSATInfluenceRealizer_N^{arb}: influence rows are not uniformly listable before use
- threshold collapse: max{rho,q+eta+tau,1+kappa+theta,chi,1+delta} reaches or exceeds 1+epsilon
- nonuniform leakage: quotient representative chosen using SAT-truth advice rather than surfaced proof syntax

## Learning

The new contribution is that quotient compression in counterfactual TSR is not a free Gamma reduction. It is valid only as a dependency-closed, acyclic same-theory certificate transformation; otherwise the first uncertified merge gives a private-row falsifier. This closes a proof-audit loophole in the restricted transparent-support theorem while preserving the separation between route-level certificate collapse and the main P vs NP conjecture.

## Gedanken Experiment Design Seed

- Need decision: `use now as a falsifier probe for certified quotient compression`
- Rationale: The branch already has a promoted CTSR parser; the remaining risk is that quotient compression silently hides row influence and falsely lowers Gamma. A concrete experiment tests whether the new certificate-forest clause is necessary and threshold-preserving.
- Situation seed: Construct H_N^{SAT} with M_N=N^q polylog queries and one CTSR node having N^kappa frontier formulas, each with N^theta counterfactual restriction children. Pair half the children by apparent EqSAT quotient merges, then choose whether each merge carries a surfaced same-theory certificate forest.
- Varied variable: chi, the exponent for total visible quotient-certificate cost C_Q=N^{chi+o(1)}, with hidden-merge count held at N^{zeta+o(1)} in the falsifier variant.
- Held-fixed controls: beta=0 polylog SAT-query length, so the positive-beta black-box cap is not the active obstruction, same nonuniform SIZE model for source carrier circuits and falsifier circuits, generator overhead N^{rho+o(1)} and bounded-SR exponent q+eta+tau fixed below 1+epsilon, counterfactual completeness of the TSR frontier except for deliberately hidden quotient dependencies
- Expected observation: When chi<1+epsilon and all merges are certified, Gamma_Q remains subthreshold and the parser-to-circuit falsifier is valid. When even one influential merge is hidden, two-world private-row spoofing preserves the transcript but changes a row label or parity, proving that the compression was unsound rather than a real threshold improvement.
- Transfer certificate needed: An acyclic same-theory certificate forest for every quotient merge, dependency-closed inside K_Q(pi), with verifier cost C_Q charged before the merge is used; otherwise the intuition may not enter proof obligations.

## Next Experiment

Instantiate one two-merge CTSR proof toy model: one certified EqSAT quotient with charged forest and one uncertified merge. Write the local verifier fields, compute R_Q and C_Q, and demonstrate transcript agreement plus parity disagreement for the uncertified merge.

# Barrier-Aware Lower-Bound Route: SAT-selector FormulaEval boundary

## Candidate Lemma

For the concrete semantic FormulaEval rule SATsel(A) with row set R_A={j<=M_N : SAT(P_A(j))=1}, RealSATInfluenceRealizer_N is valid exactly under proof-visible row-cover enumeration or full-scan charge. Without such charge, a first omitted selected row gives a private-row falsifier to occurrence completion.

## Definitions

- source object: Psys_sym^SATsel is bEF plus terminal-edge-complete transparent FormulaEval and one semantic SAT-defined row-selector rule SATsel(A) whose predicate P_A(j) is proof-visible but whose satisfying row set is not supplied as a cover.
- target object: LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) against same-model nonuniform Boolean SIZE(N^{1+epsilon}), with N=2^n and M_N=N^{q+o(1)}.
- controlled interface: RealSATInfluenceRealizer_N must, before using the semantic rule, compute an advice-free influence-closed row set R_A, give same-theory row expansions, and add its enumeration and expansion charges to Gamma.
- target-preserving condition: the parser is deterministic and no-advice, expansion is prefix-scoped with fresh variables in the same proof theory, and every terminal-relevant semantic edge is either listed, covered, or paid for by full scan.

## Assumptions

- Length regime: N=2^n, M_N=N^{q+o(1)}, proof length |pi|=N^{tau+o(1)}, generator size N^{rho+o(1)}, rho<1+epsilon.
- Rule regime: P_A(j) may be an arbitrary SAT instance generated from A and j; the proof line exposes P_A but not the set R_A unless a row-cover certificate is attached.
- Uniformity regime: the extractor may run polynomially in the expanded transcript it charges, but it may not use SAT-truth advice, a hidden selector table, or a nonuniform list of chosen rows.
- Same-theory regime: row-expanded FormulaEval material must be spliceable into the bEF/TEC prefix without changing the final LB_N formula.
- Barrier regime: if SATsel plus the parser induces a polynomial-density constructive useful truth-table property, the natural-proofs falsifier applies; otherwise this lemma is only a proof-system support theorem/no-go.

## Equations

- SAT-selector charged ledger: `\Gamma_{sat}(\pi)=\Gamma_{tec}(\pi)+\sum_{A\in K_{tec}(\pi)}(T_{enum}(A)+N\cdot |R_A|)`. Valid when: Valid when every SATsel line in the terminal-edge-complete cone has an advice-free enumerator or certified row cover and each listed row is expanded in the same proof theory.
- full-scan fallback cost: `T_{enum}(A)+N\cdot |R_A|\le N^{1+q+o(1)} \quad \text{when } R_A \subseteq [M_N] \text{ is obtained by scanning all rows}`. Valid when: Applies when the semantic SAT selector has no output-sensitive cover and the extractor deliberately pays for evaluating or expanding all M_N candidate rows.
- same-model upper-bound falsifier: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{sat}(\pi)+O(N E_\pi)`. Valid when: Requires the target-preserving same-theory splice, visible terminal dependencies, and charged FormulaEval expansions before the claimed lower-bound proof is converted to a circuit.
- subthreshold contradiction test: `N^{\rho+o(1)}+\Gamma_{sat}(\pi)+O(N E_\pi)<N^{1+\epsilon-o(1)} \Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Valid in the same nonuniform SIZE model as the source lower-bound statement and only after all parser, generator, and FormulaEval debts are included.
- full-scan q-threshold: `N^{1+q+o(1)}<N^{1+\epsilon-o(1)} \iff q<\epsilon-o(1)`. Valid when: Applies to the full-scan SAT-selector repair where the dominant expansion debt is scanning all M_N rows and no larger bEF debt is present.

## Attempted Derivation

- Fix Psys_sym^SATsel and compute the terminal-edge-complete cone K_tec(pi) from the final LB_N line as in cycle 140.
- For each SATsel line A in K_tec(pi), demand either a proof-visible cover enumerating R_A or mark A for full scan over all M_N rows.
- If a cover or full scan is present, splice the row-expanded bEF material before the first use of A, allocate fresh extension variables, and add T_enum(A)+N|R_A| to Gamma_sat.
- Run the previous TEC line induction unchanged on non-SATsel lines; at SATsel lines, the induction uses the inserted row expansions instead of a semantic oracle call.
- Derive the same-model circuit upper bound C(H_N^SAT)<=N^{rho+o(1)}+Gamma_sat(pi)+O(N E_pi). If this is below N^{1+epsilon-o(1)}, the claimed LB_N proof is refuted in the target model.
- For the negative branch, suppose A has a terminal-relevant r in R_A omitted from the charged support. Construct two carriers agreeing on all charged rows and proof-visible bits but toggling the SAT value at r; the parser transcript is identical while the semantic rule or parity carrier changes.
- Conclude that unannotated SAT-defined selector FormulaEval is not folded into TransparentRowSupport_N unless it supplies row covers or pays full scan; this is a rule-specific RealSATInfluenceRealizer_N disposition.

Blocking gap: The no-go is unconditional only for the formal SATsel rule that treats R_A semantically and does not require a cover. A stronger rule with certified output-sensitive SAT enumeration could satisfy the positive side, but that certificate must be specified and charged.

## Falsifiers

- first-omitted-row falsifier: a terminal-relevant selected row outside the charged cone makes two visible transcripts identical but changes SATsel influence
- full-scan threshold falsifier: if q<epsilon and SATsel is repaired only by scanning all M_N rows, the induced upper bound is below the claimed LB_N(1+epsilon)
- hidden-selector falsifier: a semantic predicate P_A(j) whose selected singleton is not cover-certified defeats occurrence counting and invalidates surface FormulaEval parsing
- naturalness falsifier: if the charged parser induces a large poly(N)-constructive useful property for SIZE(N^{1+epsilon}), PRF pressure blocks promotion absent a nonlarge or nonconstructive escape

## Learning

Cycle 141 makes a concrete semantic-FormulaEval disposition: SAT-defined row selectors do not get RealSATInfluenceRealizer_N for free. They are target-preserving only with a proof-visible row cover or by paying full scan N^{1+q+o(1)}; otherwise a first omitted selected row is a finite falsifier to occurrence completion. This is valid proof-system boundary progress, not progress on P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the concrete SATsel semantic rule.`
- Rationale: The remaining gap is not another abstract barrier label; it is whether a semantic FormulaEval line can hide a terminal-relevant row while preserving the beta-zero parity target. A singleton SAT-defined selector tests exactly that interface.
- Situation seed: A padded beta-zero SAT-parity family H_N^SAT with M_N=N^q rows, plus one FormulaEval SATsel line whose predicate P_A(j) is a SAT instance with exactly one satisfying row r; the proof exposes P_A but not r or a row cover.
- Varied variable: enumeration exponent lambda where the parser charges N^lambda candidate rows before using the SATsel line, with 0<=lambda<=q.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)} with rho<1+epsilon, same nonuniform SIZE target and same bEF/TEC prefix-splice proof model, deterministic no-advice extractor; no SAT-truth oracle for row selection, terminal relevance of the selected row to H_N^SAT or to the SATsel premise
- Expected observation: For lambda<q, choose r outside the charged set and the private-row pair is a valid countermodel. At lambda=q, full scan repairs visibility but costs N^{1+q+o(1)}, yielding a subthreshold contradiction only when q<epsilon-o(1).
- Transfer certificate needed: A proof-visible row-cover certificate or an advice-free output-sensitive SAT-selector enumerator with its N|R_A| expansion charge; without it, the intuition cannot enter the proof queue.

## Next Experiment

Formalize the SATsel rule syntax in paper notation: line fields A, P_A(j), cover certificate C_A, terminal-edge pointer, and splice location; then prove the two clauses Gamma_sat positive expansion and first-omitted-row countermodel as standalone propositions.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Prefix-visible cell-refinement witnesses give the exact restricted equality-compression rule for FormulaEval: in Psys_sym^{QEeq,cell}, a row can be reused from a first owner iff a RowSetEqualityWitness_N covers it before first external use; otherwise it is sum-charged, and an uncharged uncovered influence yields a private-row falsifier.

## Definitions

- source object: a bit-explicit Psys_sym^{QEeq,cell} transcript pi for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), M_N=N^{q+o(1)}, whose FormulaEval lines use canonical cell-decomposable row producers P_t with visible cell descriptors, parent pointers, dominator exits, and optional RowSetEqualityWitness_N fields.
- target object: a same-theory nonuniform SIZE upper-bound falsifier for the claimed LB_N(1+epsilon) lower-bound line, obtained by expanding only first-owned SAT rows plus charged proof-system overhead.
- controlled interface: RowSetEqualityWitness_N consists of prefix-visible cell-refinement equations certifying that every covered row of a new producer is identical to a previously first-owned row cell; uncovered rows are explicitly added to the owner table and charged by row expansion.
- target-preserving condition: no SAT-truth advice, no semantic deduplication, no post-hoc witness, no hidden auxiliary enable bit, and every equality witness plus dominator exit is parsed before the FormulaEval value can affect an external line.
- canonical cell producer: a producer whose support is a disjoint union of cells with checkable row-index maps, refinement children, and canonical row names independent of SAT truth values.
- first-owner table: the prefix-computed partial map Own_t(j) assigning each charged row j to the earliest FormulaEval line and cell that exposed it.
- complete cell cover: a witness list W_t such that every row used by line t is either in a certified equal owned cell or is marked as a new first-owned row.

## Assumptions

- Circuit model is unrestricted nonuniform SIZE over the same Boolean row functions SAT(G_N(x,j)); the conclusion is an upper-bound contradiction inside that model, not a P != NP proof.
- Length regime has N tending to infinity, M_N=N^{q+o(1)}, formula descriptions of size N^{1+o(1)} per expanded row, and all proof-bit parsing overheads recorded in Gamma_bEF or U_cell.
- Uniformity regime is advice-free for the parser: from N and the proof prefix pi_{<t}, the verifier enumerates cell descriptors, equality fields, first-owner updates, and row expansions in the stated charge.
- Timing regime is prefix-causal: equality compression is valid only if the witness is visible before the first unquarantined use of the FormulaEval value.
- Same-theory regime requires row expansion to use the same occurrence-level SAT formula G_N(x,j) that defines H_N^SAT; no external oracle or semantic SAT evaluator is imported.
- Restricted-model boundary: arbitrary AC0 membership selectors, truth-pruned semantic FormulaEval, and projected selectors without fiber witnesses are not covered unless they instantiate the canonical cell grammar.

## Equations

- Gamma_cell_ledger: `\Gamma_{cell}(\pi)=\Gamma_{bEF}(\pi)+U_{cell}(\pi)+X_{own}(\pi)+W_{eq}(\pi)`. Valid when: Valid when pi is in the restricted prefix-causal canonical-cell system and every FormulaEval line exposes its producer, equality-witness fields, and first-owner updates before use.
- first_owner_expansion: `X_{own}(\pi)=N^{1+o(1)}\cdot |K_{own}(\pi)|`. Valid when: Valid when each first-owned row j is expanded as the same SAT occurrence formula G_N(x,j) of size N^{1+o(1)} and equality-covered rows are not re-expanded.
- same_model_upper_bound: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{cell}(\pi)+O(E_\pi N^{1+o(1)})`. Valid when: Applies after the bit-explicit parser has converted all charged proof lines and first-owned FormulaEval rows into a same-model nonuniform circuit for the parity target.
- subthreshold_falsifier_condition: `\max\{\rho,\gamma_{bEF},u_{cell},w_{eq},1+k_{own},1+e_\pi\}<1+\epsilon`. Valid when: Valid when the named exponents satisfy Gamma_bEF=N^{gamma_bEF+o(1)}, U_cell=N^{u_cell+o(1)}, W_eq=N^{w_eq+o(1)}, |K_own|=N^{k_own+o(1)}, and E_pi=N^{e_pi+o(1)}.

## Attempted Derivation

- Source statement: Psys_sym^{QEeq,cell} proofs with canonical FormulaEval row producers, prefix dominator timing, and RowSetEqualityWitness_N fields admit a computable first-owner support cone K_own(pi).
- Target statement: if the resulting Gamma_cell ledger is below N^{1+epsilon-o(1)}, the claimed finite lower-bound line LB_N(1+epsilon) is false in the same unrestricted SIZE model for H_N^SAT.
- Model context: source carrier is a proof transcript plus visible row-support witnesses; target class is nonuniform SIZE circuits for the beta-zero parity target; reduction type is parser-to-circuit simulation, not many-one hardness transfer.
- Quantifier context: for all sufficiently large N, fixed epsilon>0, M_N=N^{q+o(1)}, advice-free parsing from N and pi, and no nonuniform hard-row selection.
- Base induction: non-FormulaEval bEF and bounded-SR_h lines use the already proved Gamma_bEF parser ledger.
- FormulaEval step: enumerate the canonical cells of P_t; verify each equality witness against the prefix owner table; inherit covered rows from first owners; add uncovered cells to K_own and charge N^{1+o(1)} per new row.
- Sharing step: if two cells overlap, the verifier accepts compression only through a prefix-visible refinement equation assigning each row to a unique first owner; otherwise the overlap is sum-charged.
- Timing step: quarantined delayed support is legal only if a dominator exit pays the witness and owner charge before any external dependency of the FormulaEval line.
- Countermodel step: at the earliest uncharged uncovered semantic influence, freeze all read fields and charged rows, flip the private row or unread enable bit, and obtain two completions with the same transcript but different FormulaEval value.
- Reviewer findings: reduction consistency passes for canonical cell producers; quantifier-uniformity passes only for advice-free prefix witnesses; barrier-specificity classifies full semantic SAT pruning as outside the controlled interface rather than as a valid nonrelativizing lower-bound proof; derivation remains restricted-model paper progress.

Blocking gap: Full semantic FormulaEval is still blocked at RealSATInfluenceRealizer_N, and arbitrary membership-only AC0 selectors are blocked at output-sensitive RowSetEnumerator_N. The restricted cell grammar is not a proof of those cases.

## Falsifiers

- Semantic row-set deduplication with no prefix-visible RowSetEqualityWitness_N is a private-row falsifier, not a valid compression.
- A projected-dDNNF selector whose auxiliary fiber equality is hidden behind SAT truth must pay witness support or becomes an unread-enable-bit falsifier.
- Post-hoc equality certificates discovered after the first external use violate prefix causality and cannot justify earlier compression.
- Membership-only AC0 support tests without output-sensitive enumeration pay full scan charge or leave the transparent interface.
- Any nonuniform choice of a hard or influential row is invalid for the parser-to-circuit target because the upper bound can hardwire that choice.

## Learning

Cycle 141 converts equality compression from a coverage slogan into a restricted line-induction rule with a first-owner table and prefix-visible cell-refinement witnesses. The valid contribution is a paper-level parser/falsifier theorem: syntactic cell equality can reduce K_idx, while semantic deduplication without such witnesses is a private-row falsifier. Full semantic FormulaEval remains quarantined at RealSATInfluenceRealizer_N, so this is not P vs NP progress.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The remaining ambiguity is not abstract barrier folklore but whether equality compression survives hidden projection fibers in a concrete FormulaEval line while preserving the same target lower-bound statement.
- Situation seed: Take two projected-dDNNF FormulaEval producers A and B for rows j<=M_N in H_N^SAT. A exposes disjoint projected cells with first owners. B selects the same projected rows except for one auxiliary enable fiber e_{j*} whose equality to A is either witnessed by cell refinement or hidden behind SAT-truth pruning.
- Varied variable: The varied parameter is h_N, the number of B-rows whose equality to A is hidden in auxiliary fibers rather than covered by prefix-visible cell-refinement witnesses.
- Held-fixed controls: H_N^SAT, M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)}, and the finite LB_N(1+epsilon) target are fixed., The proof model remains Psys_sym^{QEeq,cell} with same-theory occurrence expansion and no advice., The row expansion cost per first-owned row remains N^{1+o(1)}., Dominator timing is fixed: witnesses must appear before the first unquarantined use.
- Expected observation: For h_N=0 the Gamma_cell ledger reuses first owners and is valid; for any uncharged h_N>0 the first hidden enabled row yields two completions agreeing on all charged data but flipping the FormulaEval value. If the proof instead charges those rows, the upper-bound exponent increases by 1+log_N h_N.
- Transfer certificate needed: A prefix-visible RowSetEqualityWitness_N certificate giving canonical cell-refinement equations for every projected row, plus an owner-map audit showing that no SAT-truth or auxiliary-fiber advice enters before the charged dominator exit.

## Next Experiment

Instantiate L141.1 on one projected-dDNNF FormulaEval line: list cell descriptors, auxiliary fiber fields, first-owner rows, RowSetEqualityWitness_N refinements, Gamma_cell charges, then remove one enable witness and verify the private-row falsifier.
