# cycle-0142

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For Psys_sym^QCTSR, quotient deletion of counterfactual TSR rows is valid only with an acyclic same-theory certificate forest F_Q whose leaves lie in the least closed support cone; then Gamma_QCTSR line induction gives a same-model LB_N falsifier, while the first uncertified merge has a private-row countermodel.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), M_N=N^{q+o(1)}, polylog row length L_N, and claimed nonuniform SIZE lower bound LB_N(1+epsilon).
- target object: a same-model upper-bound falsifier for LB_N via a parsed proof transcript; this is a scoped certificate-collapse theorem, not P != NP evidence.
- controlled interface: bit-explicit Psys_bEF^- plus transparent FormulaEval, counterfactual declared TSR, and EqSAT quotient merges charged by a visible Gamma_QCTSR ledger.
- target-preserving condition: beta=0 or polylog SAT rows, q,rho<1+epsilon, advice-free support enumeration, complete counterfactual child exposure, acyclic same-theory quotient certificates.
- K_Q(pi) is the least fixed point generated from the final LB_N line by parent pointers, FormulaEval supports, CTSR children, and leaves of quotient certificates.
- F_Q is a surfaced EF/SATeq same-theory forest certifying each deleted duplicate row against its kept representative without SAT-truth advice.

## Assumptions

- Circuit model is nonuniform Boolean SIZE; G_N has size N^{rho+o(1)} and all parser circuits stay in the same model.
- Every proof line exposes opcode, parents, row index, formula pointer, CTSR child list, quotient representative, and certificate-root fields.
- Each quotient certificate has a rank decreasing along dependencies; cycles or semantic representative choices invalidate the lemma.
- Sparse transcript failures affect E_pi source inputs and are patchable only by O(E_pi N) equality gates.

## Equations

- ledger: `\Gamma_{QCTSR}(\pi)=\Gamma_{bEF}(\pi)+U(K_Q)+X(K_Q)+C(F_Q)+N^{1+\kappa+\theta+o(1)}+O(E_\pi N)`. Valid when: Valid when K_Q is the least closed support cone and F_Q is an acyclic same-theory certificate forest with all leaves surfaced before quotient deletion.
- parser_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{QCTSR}(\pi)`. Valid when: Applies after the generator, row verifiers, quotient certificates, CTSR children, and sparse-row patches are implemented in the same nonuniform SIZE model.
- subthreshold_falsifier: `N^{\rho+o(1)}+\Gamma_{QCTSR}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Requires the claimed LB_N to be a lower bound for the same H_N carrier and the parser-bound circuit to preserve all length and advice conventions.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Hardness-Magnification Bridge Realization; source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), M_N=N^{q+o(1)}, polylog row length L_N, and claimed nonuniform SIZE lower bound LB_N(1+epsilon).; target object: a same-model upper-bound falsifier for LB_N via a parsed proof transcript; this is a scoped certificate-collapse theorem, not P != NP evidence.; Circuit model is nonuniform Boolean SIZE; G_N has size N^{rho+o(1)} and all parser circuits stay in the same model..
- Initialize K_Q from the final LB_N assertion; close under bit-explicit parents, FormulaEval row supports, all counterfactual TSR children, quotient certificate leaves, and certificate parents until a finite fixed point is reached.
- Orient each quotient certificate by a visible rank. The induction hypothesis covers lower-rank dependencies before the merge deletes a duplicate row, so the kept representative is same-theory, not SAT-advice chosen.
- For each line, add its local verifier and row-expansion cost to Gamma_QCTSR. The bEF, transparent FormulaEval, CTSR, and certified quotient cases compose, giving the parser_bound circuit with O(E_pi N) equality patching.
- If the first bad merge is uncertified or cyclic, vary a private duplicated row while preserving all surfaced syntax; the transcript remains accepted but the carrier parity changes, contradicting extensional safety.

Blocking gap: The argument does not realize hidden semantic FormulaEval or adaptive SAT branch pruning; RealSATInfluenceRealizer_N^arb remains the named nonrelativizing open lemma.

## Falsifiers

- falsifier: a first quotient merge whose representative is chosen by SAT truth or nonuniform advice rather than by a surfaced same-theory certificate.
- falsifier: a directed cycle in F_Q, since the line induction can no longer justify deleting a row before its equivalence proof is parsed.
- falsifier: an omitted counterfactual TSR child; two transcripts agree on actual branches while a hidden child flips the quotient row.
- falsifier: any claimed positive-beta extension with transfer cap C(H_N)<=N^{q+beta c+o(1)} that cannot exclude all SAT exponents.

## Learning

Cycle 142 makes quotient compression proof-carrying: row deletion is valid only after a ranked same-theory certificate is charged in Gamma_QCTSR. Acyclicity is the new finite audit condition; cyclic, adaptive, or advice-chosen merges are concrete countermodels, not generic barrier folklore.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The branch needs a concrete audit of whether quotient compression preserves the beta-zero transparent interface or silently imports semantic advice.
- Situation seed: A QCTSR proof of an LB_N line for H_N^SAT with two syntactically different but EqSAT-equivalent counterfactual child rows; compare a surfaced EF certificate forest with one hidden adaptive quotient merge.
- Varied variable: mu, the number of quotient merges lacking surfaced acyclic same-theory certificates, varied from 0 to N^{theta}.
- Held-fixed controls: H_N^SAT parity carrier, M_N=N^{q+o(1)}, and polylog row length L_N., beta=0 target interface with q,rho,kappa+theta<epsilon., Nonuniform SIZE model and advice-free bit-explicit parser fields., Complete counterfactual TSR child declarations except for the tested quotient defect.
- Expected observation: At mu=0, Gamma decreases only by certified duplicate deletion minus C(F_Q). At mu>0, the first hidden merge creates two valid-looking worlds with different parity, exposing the private-row falsifier.
- Transfer certificate needed: A finite verifier for ranked acyclic F_Q, plus the Gamma_QCTSR line induction and same-model circuit construction before the intuition can affect proof obligations.

## Next Experiment

Write the finite verifier for K_Q and ranked F_Q on a toy projected-dDNNF plus CTSR example with one duplicate child pair; compute Gamma savings, then remove one certificate edge to exhibit the private-row falsifier.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For terminal-edge-complete Psys_sym FormulaEval with a SAT-defined row selector B_a(j)=SAT(C_a(j)), RealSATInfluenceRealizer_N is valid only in two checkable modes: a proof-visible cover R_a with an inclusion certificate B_a(j)=>j in R_a, or a full-scan charge over all M_N rows. If a terminal-relevant selected row is neither covered nor scanned, a first-omitted-row falsifier refutes occurrence completion.

## Definitions

- source object: accepted Psys_sym^{SATsel,TEC} proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), where M_N=N^{q+o(1)}.
- target object: same nonuniform Boolean SIZE lower-bound assertion C(H_N^SAT)>N^{1+epsilon} and its parser-to-circuit upper-bound falsifier.
- controlled interface: terminal-edge-complete transparent FormulaEval support K_tec(pi), with visible selector code, visible cover or scan mode, same-theory row expansion, and no hidden advice.
- target-preserving condition: every terminal-relevant semantic dependency edge is exposed before use, and every exposed row is charged in Gamma_{SATsel}^{tec} in the same circuit/proof model.

## Assumptions

- Length regime N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, generator size N^{rho+o(1)}, and rho<1+epsilon.
- Proof-system regime is bEF plus FormulaEval-SATsel lines whose selectors are either cover-certified or scan-charged by a finite checker; no SAT truth-table advice is available to the parser.
- Uniformity regime is deterministic advice-free extraction from (N,pi) with prefix-scoped fresh extension variables and same-theory row-expanded replacement of FormulaEval lines.
- Semantic inclusion certificates for covers are part of the proof-visible interface; absent such certificates, the rule is not claimed to be transparent.
- Naturalness status is conditional: if the extracted transcript becomes a large constructive useful truth-table property, natural-proof pressure applies separately and does not prove P != NP.

## Equations

- sat_selector_modes: `R_a^{scan}=[M_N],\qquad R_a^{cover}\supseteq \{j<M_N: SAT(C_a(j))=1\}.`. Valid when: Valid when a terminal-relevant SATsel FormulaEval line is either certified by a visible cover or deliberately charged by a full scan over all M_N row indices.
- tec_satselect_charge: `\Gamma_{SATsel}^{tec}(\pi)=\Gamma_{bEF}(\pi)+U_N+N\sum_{a\in K_{tec}^{cover}} |R_a|+N M_N\,F_{scan}+X_{link}.`. Valid when: Applies after the K_tec fixed point has exposed every syntactic parent and every charged row set before same-theory expansion is spliced.
- same_model_falsifier: `N^{\rho+o(1)}+\Gamma_{SATsel}^{tec}(\pi)<N^{1+\epsilon-o(1)}\ \Longrightarrow\ \pi\text{ cannot validly prove }LB_N(1+\epsilon).`. Valid when: Requires the parser expansion to be advice-free, prefix-scoped, and in the same nonuniform SIZE model as the asserted lower bound.
- row_equivalent_pressure: `\widehat S_{SATsel}=\Gamma_{bEF}/N+U_N/N+\sum_{a}|R_a|+M_NF_{scan}+X_{link}/N\ge N^{\epsilon-o(1)}.`. Valid when: Valid for sound transparent proofs after lower-order generator overhead is below the N^{1+epsilon} lower-bound threshold.

## Attempted Derivation

- Define K_0 as the final LB_N(1+epsilon) line. Iterate backward: add syntactic parents, extension definitions, bEF antecedents, and every dependency edge declared by a terminal-relevant FormulaEval line.
- For a SATsel FormulaEval line a in the cone, inspect its mode bit. In cover mode, require visible selector code C_a, enumerated row set R_a, and a checkable certificate that SAT(C_a(j)) implies j in R_a for all j<M_N. Charge U_a+N|R_a|.
- In scan mode, set R_a=[M_N] without proving selector extensionality. Charge N M_N for that line, or one cached N M_N charge only when the cache key and reuse proof are prefix-visible.
- Splice row-expanded bEF material immediately before the first use of the FormulaEval value, using fresh extension variables and preserving line order. This extends the existing Gamma_bEF induction to Gamma_{SATsel}^{tec}.
- If total size N^{rho+o(1)}+Gamma_{SATsel}^{tec}(pi) is below N^{1+epsilon-o(1)}, the splice gives a same-model circuit/transcript upper bound for H_N^SAT, contradicting the asserted LB_N(1+epsilon).
- If a terminal-relevant accepting row is neither in a cover nor scan-charged, choose the first such edge and vary the private row while fixing all charged rows. The parser transcript is unchanged, so occurrence completion is refuted by the falsifier.

Blocking gap: A full RealSATInfluenceRealizer_N for arbitrary SAT-defined selectors would require an advice-free output-sensitive enumerator or universal inclusion certificate for {j: SAT(C_a(j))}; this is not supplied by semantic FormulaEval syntax and may encode SAT-truth advice.

## Falsifiers

- First omitted selected row: SAT(C_a(j*))=1, j* terminal-relevant, j* absent from every visible cover, and no full scan charge; this falsifier invalidates surface occurrence parsing.
- Unread enable bit: a hidden bit toggles whether row j* is selected while all proof-visible bits and charged rows remain fixed, separating semantic influence from the Gamma ledger.
- Subthreshold scan falsifier: q+phi<epsilon with lower-order debts yields N^{rho}+Gamma<N^{1+epsilon}, so an accepted LB_N(1+epsilon) proof would imply its own same-model upper bound.
- Advice leakage falsifier: a cover list produced from SAT truth advice rather than from proof-visible certificates is not valid for the no-advice parser and cannot be promoted.
- Cache misuse falsifier: treating repeated scans as one charge without a visible cache key and prefix-scoped reuse proof undercounts Gamma_{SATsel}^{tec}.

## Learning

Cycle 142 converts SAT-defined FormulaEval from a vague semantic escape into a cover-or-scan boundary theorem. Live inference-quality packet: source_statement=accepted Psys_sym^{SATsel,TEC} proof pi of LB_N(1+epsilon) for H_N^SAT; target_statement=Gamma_{SATsel}^{tec} same-model upper-bound falsifier or forced row-equivalent support; model_context=nonuniform Boolean SIZE, beta-zero SAT-parity carrier, bEF plus terminal-edge-complete SATsel FormulaEval, simulation/prefix splicing rather than many-one reduction; quantifier_context=N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, F_scan=N^{phi+o(1)}, generator overhead N^{rho+o(1)}, rho<1+epsilon, deterministic no-advice parser; derivation_status=restricted cover-or-scan theorem derived, arbitrary semantic output-sensitive SATsel enumeration blocked at RealSATInfluenceRealizer_N; reviewer findings=valid only with visible influence, same-theory expansion, cache hygiene, and no hidden advice, with first omitted selected row as falsifier and no claim toward P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for SAT-defined FormulaEval row selectors.`
- Rationale: The route is blocked at a concrete semantic interface, so varying an explicit SATsel cover size tests whether the bridge is a theorem, a charged expansion, or a no-realizer countermodel.
- Situation seed: For each N, let B_{a,N}(j)=SAT(C_N(a,j)) select rows of H_N^SAT, plant one private selected row j* whose SAT value changes the parity, and give the proof either a visible cover R_a or only the semantic selector atom.
- Varied variable: alpha, where |R_a|=N^{alpha+o(1)} is the exponent of proof-visible cover rows; scan mode corresponds to alpha=q plus the scan multiplicity exponent phi.
- Held-fixed controls: H_N^SAT beta-zero parity carrier with M_N=N^{q+o(1)}., Same nonuniform SIZE target and LB_N(1+epsilon) threshold., Generator overhead N^{rho+o(1)} with rho<1+epsilon., Advice-free deterministic parser and prefix-scoped same-theory expansion., Terminal-edge-complete dependency convention for visible FormulaEval lines.
- Expected observation: If alpha<epsilon and other debts are lower order, the visible cover gives a parser upper-bound falsifier; if alpha>=epsilon, the charge blocks the contradiction; if j* is omitted, two transcripts agree while the selected parity differs.
- Transfer certificate needed: A finite certificate that every terminal-relevant SAT-selected row is in R_a, or an explicit full-scan/cached-scan charge with visible reuse; without this certificate, intuition cannot affect proof obligations.

## Next Experiment

Instantiate the cover-or-scan checker on a minimal SATsel line with one planted selected row j*: write the cover certificate fields, cache-key fields, scan multiplicity phi, and the two-transcript private-row falsifier; then decide whether arbitrary output-sensitive SATsel enumeration should be quarantined as RealSATInfluenceRealizer_N-open.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Restricted Cell-Ownership FormulaEval Parser. For bit-explicit Psys_sym^QEeq transcripts whose FormulaEval producers expose canonical disjoint cell decompositions, first-owner row records, prefix-visible cell-refinement equality witnesses, and QE exit dominators, the least cell-owned support cone K_cell(pi) is computable from proof bits and yields Gamma_cell(pi)=Gamma_bEF(pi)+U_cell(pi)+X_cell(pi)+S_uncovered(pi). If N^{rho+o(1)}+Gamma_cell(pi)+O(E_pi N)<N^{1+epsilon-o(1)}, an alleged LB_N(1+epsilon) line is falsified by a same-model SIZE circuit for H_N^SAT. Equality compression outside the witness coverage is not valid and is either sum-charged or refuted by a private-row falsifier.

## Definitions

- source object: a Psys_sym^QEeq proof transcript pi over H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, bit-explicit bEF lines, and FormulaEval lines carrying producer code, cell ids, row-index ranges, parent pointers, equality-witness ids, and QE exit-dominator stamps.
- target object: a same nonuniform SIZE model upper-bound simulation of H_N^SAT at size N^{rho+o(1)}+Gamma_cell(pi)+O(E_pi N), used only as a route-specific falsifier for subthreshold LB_N(1+epsilon) claims.
- controlled interface: CellOwner_N(pi), a prefix parser maintaining a first-owner table for row indices, a canonical cell-refinement table for equality compression, and a charged support cone K_cell(pi) containing every row whose SAT value can influence an unquarantined FormulaEval use.
- target-preserving condition: row expansion uses the same G_N formulas, same SAT predicate, same proof theory occurrence encoding, no SAT-truth advice, no nonuniform row selector, and every equality or deduplication claim is witnessed before first external dependency.
- cell record: a tuple (producer id, local cell id, row-index equation, optional witness projection, exit time, owner bit) whose denotation is a set of j in [M_N] and whose enumeration cost is charged as U_t.
- RowSetEqualityWitness_N: a prefix-visible proof object giving a common refinement of two canonical cells together with row-index equations proving equal projected row sets; it may reduce first-owner charge only for covered rows.
- inference-quality packet: source_statement is the restricted Psys_sym^QEeq transcript; target_statement is the same-model SIZE falsifier; model_context is bEF plus transparent FormulaEval; quantifier_context is all large N, fixed epsilon,q,rho,eta,tau with advice-free parsing; derivation_status is proved for canonical-cell grammar and blocked for full semantic dedup.

## Assumptions

- Model regime: N tends to infinity, M_N=N^{q+o(1)}, formula length and row expansion overheads are polylog or included in E_pi N, and all o(1) terms are uniform over the fixed proof-system fragment.
- Uniformity/advice regime: the parser, enumerators, equality witnesses, and dominator checks are computed from pi and N; no advice string may choose hard rows or declare semantic equality.
- Prefix timing regime: a row may influence an unquarantined line only after its owner cell is charged or after a QE exit dominator has paid the full delayed support cone.
- Equality regime: compression is valid only through syntactic canonical cell refinement; semantic equality of SAT-defined row sets without a witness is outside the controlled interface.
- Same-theory regime: every charged row expands to the original SAT(G_N(x,j)) occurrence family, so the resulting circuit upper bound targets H_N^SAT rather than a surrogate language.
- Barrier status: the result is a syntactic parser/falsifier theorem; it does not use a large natural property and full semantic SAT influence remains quarantined at RealSATInfluenceRealizer_N.
- Non-claim: this is not a proof of P != NP and not a lower bound; it is a scoped obstruction to low-cost proof-certificate or MCSP-style carriers.

## Equations

- cell_cone_update: `K_t=K_{t-1} \cup OwnerNew_t \cup SumCharged_t, \quad EqCovered_t \subseteq K_{t-1} \text{ only via prefix-visible refinement witnesses}`. Valid when: Valid when the source transcript is prefix ordered and every reused row has a visible cell-refinement witness before first use.
- gamma_cell_ledger: `\Gamma_{cell}(\pi)=\Gamma_{bEF}(\pi)+\sum_t U_t+\sum_t X_t+\sum_t S^{uncovered}_t`. Valid when: Applies after every FormulaEval line is classified as owned, witness-covered, or uncovered and sum-charged inside the same proof model.
- same_model_upper_bound: `SIZE(H_N^{SAT}) \le N^{\rho+o(1)}+\Gamma_{cell}(\pi)+O(E_\pi N)`. Valid when: Valid when the charged cone expands the same SAT rows generated by G_N and the parser uses no hidden advice or semantic shortcut.
- low_cost_falsifier_threshold: `N^{\rho+o(1)}+\Gamma_{cell}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)} \Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Requires the target-preserving same-model SIZE simulation and an LB_N statement asserting exclusion of all circuits below N^{1+epsilon-o(1)}.
- support_density_corollary: `X_{cell}(\pi) \ge N^{1+o(1)}\,|K_{idx}(\pi)|`. Valid when: Valid when each owned or sum-charged row contributes a same-theory FormulaEval expansion with no semantic deduplication discount.

## Attempted Derivation

- Initialize K_0 as empty and import the already validated Gamma_bEF line induction for non-FormulaEval bEF rules.
- For each FormulaEval producer line, parse canonical disjoint cells from proof bits; enumerate row-index equations or charge full scan when enumeration is absent.
- Maintain Owner[j]=first cell id for the first charged occurrence of row j; later occurrences may avoid X cost only when RowSetEqualityWitness_N gives a prefix-visible common refinement covering j.
- For quarantined blocks, require an exit dominator that appears before any external dependency; charge delayed support at the exit and then commute the block to a transparent line in the induction.
- Induction invariant: every unquarantined line value is determined by proof bits plus the SAT values of rows in K_t, and every row in K_t has either a first owner expansion or a sum-charge certificate.
- If the invariant first fails at line t, choose an influential row j* outside K_{t-1} and outside witnessed equality coverage; flip unread occurrence bits for G_N(x,j*) while preserving all visible fields to obtain the private-row falsifier.
- Given the invariant through the final LB_N line, hardwire the generator part of size N^{rho+o(1)}, the charged FormulaEval expansions, and the bEF transcript simulation to obtain the same-model SIZE upper bound.
- Compare the upper bound with the asserted LB_N(1+epsilon) threshold; if it is below N^{1+epsilon-o(1)}, the transcript is refuted within the same target model.

Blocking gap: Closed only for canonical cell-decomposable producers with prefix-visible equality witnesses and QE dominator timing. Full semantic SAT-truth pruning, semantic row-set equality, and arbitrary AC0 output-sensitive enumeration remain blocked at RealSATInfluenceRealizer_N or a missing enumerator theorem.

## Falsifiers

- A reused row has no prefix-visible RowSetEqualityWitness_N before first external dependency, giving a private-row falsifier.
- A claimed equality compression uses SAT-truth advice or semantic deduplication rather than canonical cell refinement, so it is not valid in the controlled interface.
- A selector is membership-only AC0 with no output-sensitive enumerator; it must pay full scan or leave hidden influence.
- A QE block exits after an external dependency already used its hidden support; delayed support cannot be commuted and the timing normal form fails.
- A hard-row or MCSP-style carrier selects a nonuniform row after seeing SAT truth; the target language hardness transfer leaks advice.
- A transcript satisfies Gamma_cell<N^{1+epsilon-o(1)} while asserting LB_N(1+epsilon); the same-model circuit upper bound is the explicit falsifier.

## Learning

Cycle 142 turns the last equality-compression ambiguity into a line-induction theorem for canonical cell producers: first-owner compression is valid exactly on prefix-witnessed refinement coverage, while semantic deduplication without such coverage is a finite private-row falsifier. The result strengthens the paper parser obstruction and preserves the non-claim that no P vs NP lower bound has been proved.

## Gedanken Experiment Design Seed

- Need decision: `design-now as a falsifier probe for equality compression in the restricted FormulaEval parser`
- Rationale: The branch no longer needs another abstract barrier restatement; it needs to test whether prefix-visible cell witnesses are exactly the transfer certificate separating valid compression from hidden semantic support.
- Situation seed: Two projected-dDNNF FormulaEval producers A and B over rows j<=M_N of H_N^SAT have the same visible projected cells except for one auxiliary-witness fiber containing a private row j*. The proof tries to deduplicate B against A before a QE exit.
- Varied variable: coverage fraction lambda of B's rows certified by prefix-visible RowSetEqualityWitness_N, with lambda=1 full coverage and lambda<1 leaving at least one uncovered private row.
- Held-fixed controls: The generator G_N, target function H_N^SAT, and M_N=N^{q+o(1)} are fixed., The proof model is Psys_sym^QEeq with bit-explicit bEF base rules and same-theory SAT row expansion., No SAT-truth advice, nonuniform row selector, or after-the-fact equality witness is allowed., The final target claim remains LB_N(1+epsilon) in the same nonuniform SIZE model.
- Expected observation: At lambda=1, first-owner compression preserves Gamma_cell and the line induction is valid. At any lambda<1 with nonzero influence of j*, two occurrence completions agree on all charged fields but flip FormulaEval, so compression must be replaced by sum charge or rejected by the private-row falsifier.
- Transfer certificate needed: A zero-latency RowSetEqualityWitness_N certificate giving canonical cell-refinement coverage for every reused row before QE exit; for semantic pruning, a RealSATInfluenceRealizer_N listing all influencing rows and charging R_N before use.

## Next Experiment

Instantiate the c142 ledger on one projected-dDNNF producer pair with a single uncovered witness fiber: compute U_t, X_t, the first-owner table, and the two occurrence completions, then verify that lambda=1 is charged and lambda<1 triggers the private-row falsifier.
