# cycle-0145

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For the beta-zero parity carrier, a Psys_sym^{QCTSR} proof pi satisfying finite ranked-quotient transparency has a computable least closed support K_Q(pi). The Gamma_QCTSR line induction is valid, and any subthreshold Gamma_QCTSR(pi) gives a same-model SIZE falsifier for LB_N(1+epsilon). If a quotient merge lacks a surfaced ranked same-theory certificate with dependencies inside the prefix closure, the first bad merge gives a private-row or unread-enable-bit countermodel.

## Definitions

- source object: H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, polylog SAT length L_N=(log N)^d, and Psys_sym^{QCTSR} proofs pi of a claimed LB_N(1+epsilon) for this carrier.
- target object: a nonuniform SIZE_N circuit upper bound for H_N^{SAT} contradicting the claimed source lower bound; this is a parser/falsifier theorem, not P != NP.
- controlled interface: TransparentRowSupport_N^{QCTSR}, consisting of visible FormulaEval rows, counterfactual TSR child rows, EqSAT quotient rows, ranked same-theory certificate forests, parent pointers, row-index encodings, and advice-free enumeration charges.
- target-preserving condition: beta=0, q,rho<1+epsilon, all rows and quotient certificates are determined by N and pi before use, same-theory equivalences are checked syntactically, and no SAT-truth advice or hidden row selector enters the circuit simulation.
- K_Q(pi) is the least fixed point containing final-line rows and closed under FormulaEval dependencies, counterfactual TSR children, quotient representatives, and every row used by a same-theory certificate forest.
- A ranked quotient certificate is a bit-explicit forest whose nodes carry row identifiers, formula hashes, rule tags, parent pointers, and ranks decreasing along certificate-dependency edges.

## Assumptions

- Circuit model: nonuniform Boolean SIZE on N-bit inputs for H_N, with the same model used for the source lower-bound claim and for the falsifying upper bound.
- Proof model: Psys_sym^{QCTSR} extends bit-explicit Psys_bEF^- by transparent FormulaEval, counterfactual declared TSR, and proof-carrying EqSAT quotient compression only.
- Length regime: N ranges over valid carrier lengths, M_N=N^{q+o(1)}, L_N=(log N)^d for fixed d>1 or any polylog regime giving beta=0, and generator size is N^{rho+o(1)}.
- Uniformity/advice condition: K_Q(pi), row enumerators, and certificate forests are computable from N and pi; hidden nonuniform support advice invalidates the positive theorem and triggers the falsifier side.
- Same-theory condition: a quotient merge may delete a row only if the certificate proves equivalence in the declared EqSAT/CTSR theory without querying real SAT truth values.
- Threshold condition: the source lower bound is LB_N(1+epsilon) in the same SIZE model; the parser theorem only refutes that claim when the constructed simulator is below N^{1+epsilon-o(1)}.
- Barrier status: the positive theorem is a syntactic same-model simulation, not a natural property; the negative side is an oracle-style private-row falsifier for uncharged support, not a generic relativization slogan.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j=1}^{M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad L_N=(\log N)^d`. Valid when: Valid when N is a valid carrier length and beta-zero polylogarithmic target-query length is part of the branch interface.
- least_closed_support: `K_Q(\pi)=\mu K\,[Rows(final)\cup Dep(K)\cup CTSR_{cf}(K)\cup QuotRep(K)\cup CertRows_Q(K)]`. Valid when: Valid when every dependency operator is syntactically computable from the proof text and certificate forests are ranked acyclic objects.
- charged_gamma: `\Gamma_{QCTSR}(\pi)=\Gamma_{bEF}(\pi)+U(K_Q)+X(K_Q)+B_{CTSR}(K_Q)+B_Q(K_Q)`. Valid when: Applies after all transparent rows, counterfactual TSR children, and quotient certificates have been surfaced and charged in the same ledger.
- simulator_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{QCTSR}(\pi)+O(E_\pi N)`. Valid when: Requires the parser line induction, same-model circuit simulation, and residual error rows E_pi patchable by equality tests on N-bit inputs.
- falsifier_window: `N^{\rho+o(1)}+\Gamma_{QCTSR}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Valid when LB_N is asserted against nonuniform SIZE circuits and the constructed simulator uses no stronger advice than the proof permits.
- support_density_corollary: `|K_{idx}(\pi)|\ge N^{\epsilon-o(1)},\quad |K_{idx}(\pi)|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Applies when each surfaced row index costs an N-sized occurrence expansion and all other Gamma terms remain subthreshold.

## Attempted Derivation

- Parse pi line by line and create bit fields: line_id, rule_tag, row_id, formula_hash, restriction_string, quotient_class_id, certificate_id, parent_pointer_list, rank, and local charge.
- Initialize K with every row mentioned by the final LB_N line; then iterate the closure operators Dep, CTSR_cf, QuotRep, and CertRows_Q until a fixed point is reached.
- For a transparent FormulaEval line, either enumerate the surfaced row set and charge U(K) plus occurrence expansion X(K), or full-scan all M_N rows and charge the corresponding N^{1+q+o(1)} term.
- For a counterfactual TSR line, add every syntactically reachable child row, not just the actual branch; charge B_CTSR=N^{1+kappa+theta+o(1)} in the exponent regime where the child list is complete.
- For a quotient merge, accept row deletion only if a same-theory certificate forest is present, all certificate dependencies are already in K or are added by closure, and ranks strictly decrease along every dependency edge.
- The local verifier checks certificate acyclicity by rank comparison, checks formula hashes and parent pointers, and refuses any edge whose target row was not already surfaced or newly charged.
- Line induction: assuming all parent lines have circuit simulations using only K_Q rows, each allowed rule produces the next line with additional size bounded by its ledger charge; quotient representatives are interchangeable only through accepted same-theory certificates.
- At the final line, compose the generator circuit of size N^{rho+o(1)}, the parsed transcript circuit of size Gamma_QCTSR, and equality patches for E_pi residual rows, obtaining C(H_N)<=N^{rho+o(1)}+Gamma_QCTSR+O(E_pi N).
- If this size is below N^{1+epsilon-o(1)}, the claimed LB_N(1+epsilon) is falsified in the same nonuniform SIZE model.
- For necessity, choose the first unaccepted quotient merge e. Toggle a private row behind e while keeping all charged prefix rows fixed. The transcript remains accepted but the represented parity or branch value changes, proving that the unranked merge was not transparent.

Blocking gap: The derivation is complete for surface QCTSR syntax with a specified EqSAT/CTSR same-theory checker. It does not handle arbitrary semantic FormulaEval or hidden adaptive pruning unless RealSATInfluenceRealizer_N^{arb} uniformly lists and charges the same influenced rows before use.

## Falsifiers

- First unranked quotient merge falsifier: a row deletion not backed by a ranked same-theory certificate admits a private-row two-world collision.
- Cyclic certificate falsifier: a quotient proof with no decreasing rank can hide semantic advice in a dependency loop and is rejected by the finite verifier.
- Advice-chosen representative falsifier: selecting quotient representatives using SAT labels or hidden row sets violates the target-preserving condition and invalidates Gamma shrinkage.
- Actual-branch-only TSR falsifier: charging only the followed restriction child leaves a first-hidden-child private row for the counterfactual branch.
- Threshold-collapse falsifier: if kappa+theta>=epsilon, chi>=epsilon, or E_pi>=N^{epsilon-o(1)}, the constructed simulator is not subthreshold.
- Positive-beta falsifier for broader magnification claims: SAT in SIZE(n^c) still gives carrier size N^{q+beta c+o(1)}, so beta>0 cannot exclude all c through this interface.

## Learning

Cycle 145 upgrades ranked QCTSR from a line-induction slogan to a finite verifier/minimality packet. Quotient compression is valid only when proof-carrying same-theory certificates are ranked, dependency-closed, and charged before use. The exact obstruction is the first rejected quotient merge, which yields a private-row falsifier. This strengthens the paper parser/countermodel boundary without proving H_N lower bounds or P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for quotient compression and hidden semantic pruning.`
- Rationale: The promoted theorem already has a positive line induction; the remaining risk is that quotient compression silently deletes rows without a checkable influence certificate. A concrete two-world construction tests exactly that target-preserving boundary.
- Situation seed: Take H_N^{SAT}(x)=xor_{j<=N^{q}} SAT(G_N(x,j)) with beta=0 and insert a counterfactual TSR tree where two child formulas are merged by an EqSAT quotient step. In world A the merge carries a ranked same-theory certificate forest. In world B the merge is unranked and the deleted child contains one private parity-influential row.
- Varied variable: certificate rank slack r_Q, equivalently the presence or absence of a strictly decreasing rank label on the quotient certificate dependency path.
- Held-fixed controls: q,rho,epsilon and L_N=(log N)^d are fixed in the beta-zero target-preserving regime., The proof syntax, generator G_N, and all charged rows before the tested merge are identical in both worlds., The circuit model remains nonuniform SIZE_N with no SAT-truth advice and no hidden row selector., Counterfactual TSR child declarations are required for every reachable branch outside the tested quotient merge.
- Expected observation: With ranked proof-carrying quotient certificates, the two worlds cannot differ on the merged rows without violating a checked same-theory edge. Without the rank certificate, the transcript accepts both worlds while the carrier parity changes, demonstrating a local falsifier for uncharged Gamma reduction.
- Transfer certificate needed: A finite verifier that checks row hashes, parent pointers, same-theory rule tags, dependency closure, and rank decrease before the quotient merge is used; for real SAT-semantic pruning, a nonrelativizing RealSATInfluenceRealizer_N^{arb} must list and charge the same rows.

## Next Experiment

Instantiate the finite verifier on one toy QCTSR proof with two EqSAT-equivalent counterfactual TSR children: compute K_Q, ranks, B_Q, and Gamma_QCTSR; then delete one certificate edge and explicitly write the two-world private-row falsifier.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Restricted cache-normal-form theorem: for Psys_sym^{cTEC} FormulaEval proofs with terminal-edge-complete transparent support and extensional cache misses, every accepted proof pi of LB_N(1+epsilon) for H_N^SAT either pays row-equivalent support at least N^{epsilon-o(1)} or yields a same-model SIZE upper-bound falsifier. Cache hits are free only when they cite a prior charged miss through bEF-checkable extensional equality.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with N=2^n, M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and an accepted Psys_sym^{cTEC} proof pi of LB_N(1+epsilon).
- target object: a same-model nonuniform SIZE circuit for H_N^SAT contradicting the claimed LB_N(1+epsilon), or a forced row-equivalent support lower bound for the proof transcript.
- controlled interface: terminal-edge-complete TransparentRowSupport with extensional cache misses, bEF-checkable cache-hit links, visible row covers or full scans, and prefix-scoped same-theory row expansion.
- target-preserving condition: every terminal-relevant FormulaEval dependency is either row-expanded, reached by a visible row cover or full scan, or linked to an earlier charged extensional cache miss, with no hidden advice or semantic SAT-truth row selection.

## Assumptions

- Circuit target model is nonuniform Boolean SIZE on the same H_N^SAT input length; the argument is simulation/extraction, not a many-one reduction.
- Length regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, bounded-SR_h fan h=N^{eta+o(1)}, and generator overhead rho<1+epsilon.
- Uniformity regime: the cTEC checker computes the least terminal reverse cone K_cTEC(pi) deterministically from N and pi with no semantic oracle and no private advice.
- Cache regime: every cache hit in K_cTEC(pi) points backward to a prior cache miss and carries a bEF-verifiable equality proof for formula-DAG pointer, selector code, row-cover certificate, and all enable bits used by the miss.
- Same-theory regime: replacing a transparent FormulaEval line by its row-expanded bEF material uses fresh extension variables scoped before the dependent line and preserves subsequent proof references.

## Equations

- cache-ledger: `\Gamma_{\mathrm{cTEC}}(\pi)=\Gamma_{\mathrm{bEF}}(\pi)+\sum_{a\in Miss(K_{\mathrm{cTEC}})}(N\,|R_a|+Enum(a))+Link_{hit}(K_{\mathrm{cTEC}})+SR_h(K_{\mathrm{cTEC}})`. Valid when: Valid when the cTEC proof has prefix-scoped same-theory row expansions, extensional miss certificates, and no hidden cache advice.
- same-model-upper-bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{\mathrm{cTEC}}(\pi)+O(1)`. Valid when: Applies after terminal-relevant cache hits cite earlier charged misses with bEF-checkable extensional equality proofs.
- subthreshold-falsifier: `N^{\rho+o(1)}+\Gamma_{\mathrm{cTEC}}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Requires the source lower-bound claim and constructed circuit to use the same nonuniform SIZE model.
- forced-support: `\widehat S_{\mathrm{cTEC}}(\pi):=\sum_{a\in Miss}|R_a|+\left\lceil(\Gamma_{\mathrm{bEF}}+\sum_a Enum(a)+Link_{hit}+SR_h)/N\right\rceil\ge N^{\epsilon-o(1)}`. Valid when: Valid when a sound LB_N proof is accepted and rho is below 1+epsilon.
- visible-row-density: `|K_{row}(\pi)|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Applies when bEF debt, enumeration debt, hit-link debt, and SR_h debt are lower order than N^{1+epsilon}.

## Attempted Derivation

- Define K_cTEC(pi) by a backward worklist from the final LB_N line. Add ordinary proof parents, bEF extension dependencies, terminal FormulaEval edges, cache-hit predecessor edges, and the row-cover/full-scan edges of each reachable cache miss. Reject forward cache references.
- For each reachable cache miss a, enumerate its certified row set R_a. Splice before a the bEF row expansions for all r in R_a, plus the visible selector-extensionality checks. Charge N|R_a|+Enum(a).
- For each reachable cache hit, replace the semantic reuse by a bEF proof that the hit key, formula-DAG pointer, selector code, enable-bit vector, and row-cover digest equal those of an earlier charged miss. Charge only Link_hit, not another N|R_a| expansion.
- Run the existing bEF/TEC line induction on the prefix-spliced proof. The induction invariant is that every terminal-relevant FormulaEval value has either a local row expansion or a causal extensional predecessor whose expansion already appears earlier.
- Extract a nonuniform circuit for H_N^SAT by hardwiring the charged transcript, generator G_N, and prefix-spliced FormulaEval material. This gives C(H_N^SAT)<=N^{rho+o(1)}+Gamma_cTEC(pi)+O(1).
- If the right side is below N^{1+epsilon-o(1)}, the accepted LB_N(1+epsilon) is false in the same target model; hence a sound accepted proof must pay N^{epsilon-o(1)} row-equivalent support.
- For the negative side, choose the first terminal-relevant cache hit whose key omits an influencing field. Flip the omitted enable bit or private row r* while preserving all visible key and transcript bits. The checker accepts the same transcript, but the FormulaEval value or carrier parity changes, giving the finite falsifier.

Blocking gap: The restricted cTEC theorem is derivable, but arbitrary semantic selector equivalence remains blocked at RealSATInfluenceRealizer_N: no advice-free procedure is known to list output-sensitive SAT-selected rows without a visible cover or full scan.

## Falsifiers

- Hash-only cache key omitting one enable bit: same visible hit, different selected private row, invalid occurrence completion.
- Forward cache hit citing a future miss: prefix-splice order fails, so same-theory expansion is not valid.
- Semantic selector equivalence certified only by real SAT truth: row set is not uniformly enumerable and becomes a RealSATInfluenceRealizer_N falsifier.
- q<epsilon with lower-order Gamma debt: the trivial generator-plus-transcript upper bound falsifies any claimed LB_N(1+epsilon).
- Dense constructive truth-table property induced by the transcript would face the natural-proofs PRF falsifier unless it is non-large, nonconstructive, or proof-system-specific.

## Learning

Cycle 145 improves the FormulaEval boundary by normalizing memoization: cache compression is valid only through a causal extensional miss lineage inside the terminal reverse cone. Duplicate hits need not be row-expanded, but every new influencing row must appear in a prior charged miss. Hash-only or prefix-only cache keys have a finite private-row collision falsifier. This is proof-system boundary progress and not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The cache interface is the current theorem-boundary; a concrete collision experiment tests whether memoization preserves target rows or leaks semantic advice before more abstract RealSATInfluenceRealizer_N restatement.
- Situation seed: A beta-zero H_N^SAT proof contains one terminal-relevant FormulaEval cache hit with key k=(formula-DAG, selector-code-prefix) while the full selector state also has an enable bit e_{r*} controlling row r*. A prior cache miss is charged only for e_{r*}=0, but the hit is reused when e_{r*}=1.
- Varied variable: cache-key leakage exponent kappa, measured as the number of terminal-relevant selector bits omitted from the extensional key; compare kappa=0 with kappa>=1.
- Held-fixed controls: Keep H_N^SAT, M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)}, and target class nonuniform SIZE fixed., Keep the proof model Psys_sym^{cTEC} with terminal reverse cone, prefix splicing, and bEF-checkable line verification fixed., Keep the reduction type as same-model simulation/extraction, not a many-one SAT reduction., Keep no hidden advice and no SAT-truth oracle access in the parser.
- Expected observation: For kappa=0, every hit has a charged extensional ancestor and Gamma_cTEC is valid. For kappa>=1, two selector states collide on k while differing on r*, producing the private-row falsifier and invalidating uncharged memoization.
- Transfer certificate needed: A bEF-checkable injectivity or row-cover certificate for the cache key on all terminal-relevant influence fields, or a full-scan charge N^{1+q+o(1)} before the cached semantic value is used.

## Next Experiment

Instantiate K_cTEC on a three-line toy proof with one miss and two hits, compute Gamma_cTEC exactly, then instantiate the omitted-enable-bit collision and verify that the checker transcript is identical while the terminal FormulaEval value differs.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For Psys_sym^QEeq with canonical cell-decomposable FormulaEval producers, prefix-visible exit-local first-owner refinement witnesses are sufficient to derive the Gamma_QEeq parser ledger; any semantic row sharing not witnessed at the dominating exit must be sum-charged or gives a private-row falsifier.

## Definitions

- source object: a bit-explicit Psys_sym^QEeq proof pi of LB_N(1+epsilon) over H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)} and FormulaEval blocks sealed by quarantine exits.
- target object: a same-theory nonuniform SIZE upper bound circuit for H_N^SAT, charged by generator overhead, bEF parsing cost, visible row enumeration, row expansion, and equality-witness overhead.
- controlled interface: FormulaEval cell producers expose producer code, row-index cells, parent pointers, exit timestamps, first-owner identifiers, and syntactic refinement witnesses before any external dependency uses the rows.
- target-preserving condition: all charged expansions remain in the same SAT occurrence theory, are advice-free and prefix-visible, and no semantic equality, SAT-truth pruning, or hidden hard-row selector is used without a RealSATInfluenceRealizer_N certificate.

## Assumptions

- Model: Psys_sym^QEeq extends the already parsed Psys_bEF^- rules only by quarantined FormulaEval blocks whose exits dominate all external dependencies.
- Regime: N tends to infinity, M_N=N^{q+o(1)}, generator overhead is N^{rho+o(1)}, and the claimed lower bound threshold is SIZE N^{1+epsilon-o(1)} for fixed epsilon>0.
- Uniformity: the parser, row enumerators, cell-refinement verifiers, and first-owner table are computable from proof bits and N, with no nonuniform row-selection advice.
- Cell grammar: every row producer is canonical and decomposes its row set into disjoint cells whose membership and refinement implications are syntactically checkable coordinate by coordinate.
- Timing: a compression witness for a cell C at exit e is valid only if its owner cell O is prefix-visible before e, C is syntactically refined by O, and e dominates the first external use of C.
- Non-claim: the lemma is a restricted proof-system parser/falsifier theorem and is not a proof of P != NP or an unrestricted lower bound.

## Equations

- owner_closure: `K_{e}=K_{<e}\cup\{\operatorname{own}_{e}(C): C\in \mathrm{Cells}_{e},\ \mathrm{Refine}_{e}(C,\operatorname{own}_{e}(C))\}\cup\{C: C\in \mathrm{Cells}_{e}\ \text{uncovered}\}`. Valid when: Valid when each cell is emitted by the canonical producer grammar and each owner pointer is checked before the dominating quarantine exit.
- gamma_update: `\Gamma_{\mathrm{QEeq}}(\pi)=\Gamma_{\mathrm{bEF}}(\pi)+\sum_{e}\big(U^{\mathrm{new}}_{e}+X^{\mathrm{new}}_{e}+W^{\mathrm{ref}}_{e}\big)+N^{o(1)}`. Valid when: Applies after the reduction preserves prefix timing, first-owner uniqueness, syntactic refinement coverage, and same-theory row expansion for every FormulaEval exit.
- upper_bound_falsifier: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{\mathrm{QEeq}}(\pi)+O(E_{\pi}N^{1+o(1)})`. Valid when: Requires the parser-to-circuit simulation in the same nonuniform SIZE model and requires all FormulaEval influence to be visible, charged, or quarantined.
- subthreshold_contradiction: `N^{\rho+o(1)}+\Gamma_{\mathrm{QEeq}}(\pi)+O(E_{\pi}N^{1+o(1)})<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Valid when LB_N asserts a same-model lower bound for H_N^SAT and the constructed circuit family is nonuniform but advice-free from hidden semantic support.
- support_density_corollary: `X_N\ge N^{1+o(1)}|K_{idx}(\pi)|,\qquad |K_{idx}(\pi)|/M_N\ge N^{\epsilon-q-o(1)}\ \text{is necessary to avoid the low-cost falsifier}`. Valid when: Applies when each realized row expansion has polynomial-length SAT occurrence encoding and M_N=N^{q+o(1)} rows are the only parity summands.

## Attempted Derivation

- Base: inherited Gap98-SRhNormalForm gives Gamma_bEF for non-FormulaEval lines in Psys_bEF^- with bit fields, local verifier, parent pointers, and eta/tau costs already charged.
- Induction invariant: after each proof prefix, K_e contains exactly the first-owner compressed row cells whose influence is prefix-visible; every external dependency reads only rows in K_e or rows in a syntactically sealed quarantine.
- FormulaEval entry: while a block is quarantined, delayed row discovery is allowed only internally; no external line may depend on its semantic value before the exit certificate is parsed.
- Exit rule: parse each cell record (producer id, cell id, row-index constraints, owner id, refinement witness, timestamp, dominator id). If the owner witness is valid, charge W_ref and reuse the first owner; otherwise add the cell to the uncovered set and charge U_new plus X_new.
- Compression soundness: canonical cell refinement implies every row of the child cell is already among the owner rows, so replacing child rows by owner rows preserves the same expanded SAT occurrence transcript.
- Circuit simulation: hardwire the proof transcript, generator G_N, and expanded charged rows; compute H_N^SAT by following the parsed proof dependencies, with size bounded by N^{rho+o(1)}+Gamma_QEeq+O(E_pi N^{1+o(1)}).
- Negative fork: choose the first exit where an influential row is neither covered nor charged. Minimality fixes all earlier dependencies; an unread occurrence or enable bit in the hidden cell gives two completions with identical parsed transcript and opposite parity, invalidating the low-cost parser.

Blocking gap: The derivation is complete for canonical cell-decomposable Psys_sym^QEeq. It does not handle full semantic FormulaEval unless RealSATInfluenceRealizer_N supplies zero-latency advice-free influence rows and their Gamma charge.

## Falsifiers

- A FormulaEval rule uses SAT-truth pruning to decide which row cells exist, so the row set is not prefix-visible from proof syntax.
- A row-set equality is asserted semantically rather than by canonical cell-refinement witnesses, enabling a private-row falsifier.
- A projected selector hides witness fibers and pays only projected support instead of min{certified projected enumeration, witness support}.
- A hard-row carrier chooses the owner or representative by nonuniform advice, breaking the target-preserving uniformity ledger.
- A purported low-cost transcript has q<epsilon and full enumeration charge N^{1+q+o(1)}, yielding an immediate subthreshold upper-bound falsifier rather than a lower-bound proof.
- A RealSATInfluenceRealizer_N is claimed but omits the first external use timing, making it delayed support rather than valid prefix support.

## Learning

Cycle 145 makes the equality-compression rule referee-checkable: first-owner reuse is valid only through prefix-visible canonical refinement at the dominating exit, and the Gamma_QEeq ledger follows by line induction. This closes a proof-audit gap for restricted FormulaEval while preserving the full semantic boundary at RealSATInfluenceRealizer_N. The result is a paper-level parser obstruction and finite falsifier, not progress on P != NP itself.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the exit-local first-owner normal form.`
- Rationale: The remaining risk is not an abstract barrier but a concrete hidden semantic deduplication step; a small projected-dDNNF FormulaEval case can test whether the bit grammar detects the first unowned influence.
- Situation seed: Take H_N^SAT with M_N=N^{q+o(1)} rows and two quarantined projected-dDNNF FormulaEval blocks B0,B1 that semantically select the same SAT rows, but B1 exposes only a projected cell while hiding one witness-enable bit until after its exit.
- Varied variable: The fraction p_N of B1 selected rows whose equality to B0 is semantic-only, with p_N ranging from 0 to N^{-q+o(1)} so that even one hidden row can be isolated.
- Held-fixed controls: The SAT generator G_N, parity target H_N^SAT, and same nonuniform SIZE target model are fixed., The proof syntax remains Psys_sym^QEeq with canonical cell producers and dominator exits., No advice, nonuniform hard-row selector, or post-exit equality certificate is allowed., The generator overhead N^{rho+o(1)}, row count M_N=N^{q+o(1)}, and threshold N^{1+epsilon-o(1)} are fixed.
- Expected observation: For p_N=0 the exit certificate charges W_ref and reuses first-owner rows. For any p_N>0 without a prefix-visible refinement witness, the first hidden projected cell admits an unread-enable-bit completion changing a row SAT value while preserving all parsed bits, so semantic deduplication is invalid.
- Transfer certificate needed: A formal verifier lemma showing that canonical refinement witnesses imply row-set inclusion before the dominating exit, plus a same-theory two-completion lemma for the first unowned influential row.

## Next Experiment

Instantiate the verifier on one projected-dDNNF FormulaEval exit: list the producer-code fields, canonical cell ids, owner ids, refinement clauses, dominator timestamp, and the first hidden witness-enable bit; then compute U_new, X_new, W_ref and exhibit the two completions if a cell lacks a prefix-visible owner.
