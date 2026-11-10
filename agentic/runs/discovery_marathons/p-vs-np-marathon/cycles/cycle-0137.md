# cycle-0137

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For beta-zero parity carrier proofs in Psys_sym^CTSR, the counterfactual closed support cone K_CTSR(pi) is not only sufficient for the Gamma_CTSR parser but minimal for extensional safety: every reachable FormulaEval or TSR influence row must either appear in K_CTSR(pi) and be charged, or a private-row/unread-child falsifier makes the occurrence parser invalid. Hence a subthreshold Gamma_CTSR transcript yields only a same-model upper-bound falsifier for LB_N(1+epsilon), not a P != NP proof.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, formula length L=(log N)^d, beta=0, and generator cost N^{rho+o(1)}.
- target object: same-model nonuniform SIZE upper-bound falsifier for the claimed source lower bound LB_N(1+epsilon): C(H_N^SAT)>N^{1+epsilon-o(1)}.
- controlled interface: Psys_bEF^- plus transparent FormulaEval lines and counterfactual declared bounded-TSR rules whose verifier exposes bit fields, parent pointers, row indices, child selectors, and same-theory expansion certificates.
- target-preserving condition: all row influences used by the proof are uniformly listable from pi and N without SAT-truth advice, expanded in the same row theory, and charged before the target substitution bridge is invoked.
- K_CTSR(pi) is the least fixed point from the final LB_N line under visible proof-DAG parents, FormulaEval support enumerators, EF extension support, SATeq links, bounded-SR_h leaves, and every counterfactual TSR child row for each declared restriction family.
- Gamma_CTSR(pi) is Gamma_bEF(pi) plus enumerator cost U(K_CTSR), row-expansion cost X(K_CTSR), declared TSR child-expansion cost, and sparse residual correction O(E_pi N).

## Assumptions

- Circuit model is nonuniform Boolean SIZE over the same representation of H_N and the parsed rows; no advice string may encode unlisted row support.
- Length regime is N -> infinity, M_N=N^{q+o(1)}, L=(log N)^d with d>1 or another beta=0 subpolynomial query regime, and rho,q<1+epsilon.
- Proof syntax is finite and bit-explicit: every CTSR rule record contains rule_id, parent_line, base_row, restriction_bits, child_count <=N^{theta+o(1)}, selector_seed length N^{kappa+o(1)}, and a row-expansion verifier of size N^{o(1)} per emitted row block.
- Same-theory condition: replacing a FormulaEval/TSR line by its charged occurrence expansion preserves the proof line's Boolean meaning in the row theory; semantic SAT pruning is excluded unless RealSATInfluenceRealizer_N^arb supplies the charged row set.
- Barrier status: the theorem is relativizing as a parser/countermodel boundary and deliberately avoids claiming a natural-proof escape; any full semantic SAT influence must be nonrelativizing and advice-free to enter the valid proof queue.

## Equations

- least_fixed_point: `K_{CTSR}(\pi)=\mu K\,[Final(\pi)\cup Parents(K)\cup FE(K)\cup EF(K)\cup SATeq(K)\cup SR_h(K)\cup CChild_{TSR}(K)]`. Valid when: Valid when pi is a finite Psys_sym^CTSR proof whose rule records expose dependency edges and counterfactual child descriptors advice-free.
- ledger: `\Gamma_{CTSR}(\pi)=\Gamma_{bEF}(\pi)+U(K_{CTSR})+X(K_{CTSR})+N^{1+\kappa+\theta+o(1)}+O(E_\pi N)`. Valid when: Applies after every emitted row is expanded in the same row theory and the declared TSR family has N^{\kappa+o(1)} bases and N^{\theta+o(1)} counterfactual children per base.
- parser_upper_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{CTSR}(\pi)`. Valid when: Requires the beta-zero target-preserving substitution regime and a line-induction parser that turns each charged proof line into a circuit fragment for H_N.
- subthreshold_falsifier: `N^{\rho+o(1)}+\Gamma_{CTSR}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Valid when LB_N(1+epsilon) is the same nonuniform SIZE lower-bound assertion for H_N and sparse residual errors are already included in Gamma_CTSR.

## Attempted Derivation

- Define K_0 as the final LB_N line; iteratively add visible proof-DAG parents, bit-explicit EF supports, SATeq-linked rows, bounded-SR_h leaves, FormulaEval enumerator outputs, and every counterfactual child row declared by a CTSR rule touching the current set.
- Termination is immediate because pi has finitely many line records and each CTSR record declares at most N^{kappa+theta+o(1)} child rows with finite bit encodings; the least fixed point is the union of all iterations.
- Line induction: for bEF lines use the cycle-98/102 Gamma_bEF parser; for transparent FormulaEval lines replace the symbolic line by its K_CTSR row expansion charged in U+X; for CTSR lines use the complete counterfactual child table to compute the same restricted self-reduction value without semantic pruning advice.
- The constructed circuit first computes G_N with cost N^{rho+o(1)}, then evaluates the charged transcript fragments and combines them according to the proof's final parity/LB_N line; sparse residual rows, if any, are equality-patched at O(E_pi N).
- If a reachable row r is omitted, choose the first proof line l whose extensional value depends on r. Build two row-oracle worlds agreeing on K_CTSR(pi) minus r and all bit-visible records, but differing on r so that l and ultimately the asserted occurrence completion differ. The verifier cannot distinguish the worlds, proving the private-row falsifier.
- The quantitative contradiction is only against the source LB_N(1+epsilon) claim: if N^{rho+o(1)}+Gamma_CTSR(pi)<N^{1+epsilon-o(1)}, the parsed circuit is a valid same-model upper bound for H_N.

Blocking gap: The derivation does not handle full semantic branch pruning where real SAT itself proves the omitted child determined by charged rows. That is exactly RealSATInfluenceRealizer_N^arb: an advice-free, nonrelativizing realizer must list and charge all influencing rows before the semantic rule is used.

## Falsifiers

- first-hidden-child adaptive pruning: actual-branch declarations undercharge a counterfactual child row that can change the semantic TSR value
- private-row/unread-enable-bit falsifier: two transcripts agree on all surfaced support but differ on an uncharged row influencing H_N
- threshold collapse falsifier: rho or kappa+theta reaches epsilon, making the parser upper bound no longer subthreshold
- nonuniform leakage falsifier: a selector or row list is encoded as advice rather than uniformly recovered from pi and N
- positive-beta black-box substitution falsifier remains active for any carrier extension with query length N^beta and beta>0

## Learning

Cycle 137 improves the promoted CTSR packet by proving minimality pressure, not just sufficiency: complete counterfactual child support is the least valid transparent object for adaptive TSR. Removing one reachable child gives a concrete first-hidden-child falsifier; adding all children gives the exact Gamma_CTSR threshold kappa+theta<epsilon. The learning is a scoped parser/countermodel contribution, not a lower bound for H_N and not P != NP progress.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch already has a promoted CTSR parser theorem; the remaining proof risk is whether counterfactual declaration is truly necessary or only a conservative overcharge. A concrete private-row experiment tests that exact boundary without broadening the carrier.
- Situation seed: Construct a Psys_sym proof of H_N^SAT using a bounded TSR line whose actual branch follows an enable bit e(x,j). The record declares the taken child row only, while the untaken child is a generated SAT restriction of length (log N)^d. Compare two row-oracle worlds that agree on all declared rows but flip SAT on the first untaken child.
- Varied variable: hidden_child_density delta, the exponent with N^{delta+o(1)} unlisted counterfactual children among N^{kappa+theta+o(1)} possible child rows.
- Held-fixed controls: M_N=N^{q+o(1)}, beta=0, q<1+epsilon, and generator overhead N^{rho+o(1)} with rho<1+epsilon, same Psys_bEF^- bit-explicit base parser and same nonuniform SIZE source model, formula length L=(log N)^d and no SAT-truth advice in row enumeration, CTSR depth h and per-child verifier overhead N^{o(1)}
- Expected observation: For any delta>0 with at least one reachable hidden child, actual-branch transcripts can be identical while the induced self-reduction value changes. When complete counterfactual support is charged, the attack disappears but the ledger gains N^{1+kappa+theta+o(1)}, yielding the exact kappa+theta<epsilon threshold.
- Transfer certificate needed: A formal first-hidden-child lemma plus, for any semantic escape, an advice-free RealSATInfluenceRealizer_N^arb proving that real SAT semantics determines the hidden child from charged rows and adding its row-realization cost to Gamma_CTSR.

## Next Experiment

Write the standalone L137 first-hidden-child theorem: specify the CTSR bit fields, define the two row-oracle worlds, prove transcript equality on K_CTSR minus r, prove final parity disagreement, and compute the Gamma_CTSR threshold for kappa+theta<epsilon with q-trichotomy support density.

# Barrier-Aware Lower-Bound Route, cycle 137: terminal-relevant rrBTRS charge packet

## Candidate Lemma

For a transparent Psys_sym^{rrBTRS} proof pi of LB_N(1+epsilon) for H_N^SAT, the least reverse-reachable support cone K_rr(pi) from the final lower-bound line is the unique charged object needed for the parser-to-circuit falsifier. Dead FormulaEval padding outside K_rr is erased. If the Gamma_rr ledger is below N^{1+epsilon-o(1)} while the generator overhead is below N^{1+epsilon-o(1)}, the alleged lower bound is refuted in the same nonuniform SIZE model; otherwise the proof pays N^{epsilon-o(1)} row-equivalent terminal support.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with N=2^n, M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and an accepted Psys_sym^{rrBTRS} proof pi of LB_N(1+epsilon).
- target object: a same-model nonuniform Boolean SIZE upper-bound falsifier for LB_N(1+epsilon), or a forced row-equivalent terminal-support lower bound for pi.
- controlled interface: deterministic no-advice reverse worklist over proof-line dependencies, visible selector code, row-cover certificates, influence closure, and same-theory row expansion for every FormulaEval line in the reachable cone.
- target-preserving condition: every terminal-relevant FormulaEval influence row is proof-visible and charged before use, prefix splicing uses fresh extension variables, and no semantic SAT truth advice or hidden row selector is imported.
- K_rr(pi): the least fixed point initialized by the final LB_N line and closed under syntactic parents, extension parents, selector witnesses, row-cover children, and bounded-SR_h touched occurrence neighborhoods.
- Gamma_rr(pi): Gamma_bEF restricted to K_rr plus row enumeration debt U_rr, row expansion debt X_rr, and charged FormulaEval bit debt N E_rr^*.
- widehat S_rr(pi): row-equivalent charge ceil(Gamma_bEF(K_rr)/N)+ceil(U_rr/N)+E_rr^*+|K_FE,rr|.

## Assumptions

- Model: nonuniform Boolean SIZE on N-bit truth tables, with the source carrier H_N^SAT and the target lower bound LB_N(1+epsilon) interpreted in the same model.
- Regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, bounded-SR_h radius h=N^{eta+o(1)}, optional visible existential witness list size N^{alpha+o(1)}, and rho<1+epsilon.
- Uniformity/advice: the K_rr worklist, row enumeration, row-cover verification, and prefix splicing are deterministic from (N,pi) and use no nonuniform advice beyond pi itself.
- Same-theory condition: each FormulaEval line in K_rr is replaceable by row-expanded bEF material inside the same proof theory, with fresh extension variables scoped before the line they support.
- Naturalness cutoff: if the extracted transcript is total, poly(N)-constructive, large, and useful against SIZE(N^{1+epsilon}), then the natural-proofs falsifier audit applies; this lemma itself is only a proof-system parser theorem.

## Equations

- RR fixed point: `K_{0}=\{\ell_{final}\},\quad K_{t+1}=K_t\cup Dep_{rrBTRS}(\pi,K_t),\quad K_{rr}=\bigcup_t K_t.`. Valid when: Valid when Dep_rrBTRS is computed from proof-visible parent pointers, selector witnesses, row covers, and occurrence-neighborhood fields without semantic advice.
- Terminal charge ledger: `\Gamma_{rr}(\pi)=\Gamma_{bEF}(K_{rr})+U_{rr}(K_{rr})+X_{rr}(K_{rr})+N E_{rr}^{*}(K_{rr}).`. Valid when: Valid when every FormulaEval line in the reverse-reachable cone has a same-theory row expansion and all enumeration or witness debts are charged.
- Parser-to-circuit falsifier: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{rr}(\pi).`. Valid when: Applies after the prefix-splice expansion preserves the original carrier, proof theory, uniform row labels, and nonuniform SIZE target model.
- Forced row-equivalent support: `\text{if }\rho<1+\epsilon\text{ and }LB_N(1+\epsilon)\text{ is sound, then }\widehat S_{rr}(\pi)\ge N^{\epsilon-o(1)}.`. Valid when: Valid when Gamma_rr is measured in bit-size units and widehat S_rr is the normalized row-equivalent charge Gamma_rr divided by N up to lower-order terms.
- Visible-row density corollary: `|K_{FE,rr}|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Requires bEF, enumeration, existential-witness, and expansion debts outside visible FormulaEval rows to be o(N^{1+epsilon}) in the same length regime.

## Attempted Derivation

- Type the source statement as an accepted Psys_sym^{rrBTRS} proof pi of LB_N(1+epsilon) for H_N^SAT in the beta-zero SAT-parity carrier, not as a claim about P != NP.
- Build a directed dependency graph whose vertices are proof lines, selector certificates, row-cover witnesses, extension definitions, and bounded-SR_h occurrence neighborhoods. Edges point from a line to every object needed to verify it.
- Run the reverse worklist from the final LB_N line. Add syntactic parents, formula parents, visible feasible-witness rows, row-cover children, and all touched SR_h neighborhoods. Termination is immediate because all vertices are finite proof-visible fields of pi.
- Prove leastness by induction on any prefix-closed transparent support S containing the final line: every Dep_rrBTRS addition is forced by one verifier clause, hence K_t subset S for all t and K_rr subset S.
- Define Gamma_rr on K_rr only. Dead lines outside K_rr are absent from the ledger, so padding a proof with irrelevant FormulaEval lines does not change the valid transfer bound.
- For each line in topological order of K_rr, maintain the invariant that its expanded bEF prefix derives the same formula as the original symbolic line. bEF lines use the old parser; transparent FormulaEval lines are replaced by their certified row expansion; bounded-SR_h lines charge N^{tau+eta+o(1)} when their visible witness exponent is zero and N^{tau+alpha+eta+o(1)} in the existential-index case.
- Use prefix-splice freshness to avoid extension-variable capture. The expanded transcript has size at most Gamma_rr(pi)+lower-order verifier overhead.
- Compile the row-expanded transcript plus generator G_N into a nonuniform circuit for H_N^SAT of size at most N^{rho+o(1)}+Gamma_rr(pi). This is a simulation/extraction, not a many-one reduction.
- If N^{rho+o(1)}+Gamma_rr(pi)<N^{1+epsilon-o(1)}, the source lower-bound assertion is falsified in the same target model. Therefore any sound accepted proof must have normalized row-equivalent charge at least N^{epsilon-o(1)}.
- If a terminal-relevant semantic row is omitted from K_rr, flip the private row or unread enable bit while preserving all visible fields. The two transcripts remain identical but the FormulaEval semantic value can differ, giving the named falsifier to occurrence-only parsing.

Blocking gap: The derivation is complete only for rrBTRS-transparent FormulaEval. Arbitrary semantic FormulaEval is still blocked at RealSATInfluenceRealizer_N: syntax and N must uniformly determine an influence-closed row set, charged overhead, and same-theory expansions before the semantic rule is used.

## Falsifiers

- Dead-line padding falsifier: charging the whole proof rather than K_rr can exceed N^{1+epsilon} without any terminal relevance, so full-proof Gamma is not a valid invariant.
- Unread-enable-bit falsifier: a hidden row controls a FormulaEval line while every visible row-cover field is unchanged, refuting occurrence-only parsing.
- q<epsilon source-ceiling falsifier: if M_N=N^{q+o(1)} with q<epsilon, the carrier has a same-model upper bound below N^{1+epsilon-o(1)} before any proof-system analysis.
- Selector-extensionality falsifier: two selector codes with identical displayed occurrences but different hidden extensional row sets defeat RowSetEnumerator_N unless the extension is proof-visible and charged.
- Natural-property falsifier: if the extracted accepting transcript becomes poly(N)-constructive, large, and useful against the exact SIZE target, PRF tension applies; the route must remain proof-mediated or non-large to avoid this audit.

## Learning

Cycle 137 adds a non-cosmetic refinement: the valid charge invariant is the least terminal-relevant reverse cone K_rr, not the full proof and not the full selector zoo. This makes the parser theorem invariant under dead-line padding, gives a sharper Gamma_rr upper-bound falsifier, and isolates the exact unproved bridge as dependency-edge completeness for semantic FormulaEval. The result is route-level proof-system certification, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the terminal-relevance invariant.`
- Rationale: The branch has already proved many selector-specific charges; the remaining risk is that the new K_rr invariant is merely cosmetic. A concrete padded proof with many dead FormulaEval lines tests whether the charge theorem is actually target-preserving and padding-immune.
- Situation seed: Construct a Psys_sym^{rrBTRS} proof over H_N^SAT with M_N=N^{q+o(1)} rows: one reverse-reachable chain uses N^{alpha+eta+o(1)} visible existential-index SR_h rows, while N^{omega+o(1)} additional FormulaEval lines scan unrelated SAT rows but have no path to the final LB_N line.
- Varied variable: omega, the exponent of dead FormulaEval padding outside the final-line reverse cone.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and rho<1+epsilon., The terminal chain has visible row covers, same-theory row expansions, and no hidden advice., The final LB_N line and all reverse-reachable dependencies are held fixed while only dead lines are added., The target model remains nonuniform Boolean SIZE and the proof-to-circuit step remains simulation/extraction.
- Expected observation: Gamma_full grows like N^{1+omega+o(1)} and can falsely block the subthreshold falsifier, while Gamma_rr is invariant under omega and remains the correct valid terminal-relevant ledger. If a dead line can influence the final line without entering K_rr, the worklist definition is incomplete.
- Transfer certificate needed: A formal dependency-edge completeness certificate: every semantic or syntactic influence on the final LB_N line must create a proof-visible edge included by Dep_rrBTRS, with same-theory row expansion and charged overhead before the line is used.

## Next Experiment

Instantiate L137.1 on a projected-dDNNF FormulaEval line with one omitted reachable row: run the K_rr worklist, compute Gamma_rr, then flip the omitted row to verify the unread-enable-bit falsifier and the exact dependency edge that a RowCoverCertificate must add.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For a bit-explicit Psys_sym^{QEeq} transcript, prefix-visible quarantine exits plus syntactic equality-coverage witnesses give a valid Gamma_QEeq line induction. The resulting same-model circuit upper bound is a route-level falsifier for any subthreshold LB_N(1+epsilon) claim; it is not a P != NP proof.

## Definitions

- source object: a Psys_sym^{QEeq} proof transcript pi for H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)), with bEF^- core lines, quarantined FormulaEval blocks, exit dominators, row enumerators, and RowSetEqualityWitness_N certificates.
- target object: a nonuniform SIZE upper bound for the same H_N^{SAT} family in the same row-expansion theory used by the proof transcript.
- controlled interface: prefix-visible FormulaEval support through quarantine exits, first-owner row certificates, syntactic equality coverage, sum charging for uncovered rows, and same-theory occurrence expansion.
- target-preserving condition: every row that can influence an unquarantined line is enumerated, equality-covered by a prefix-visible syntactic witness, or sum-charged before first external dependency; no SAT-truth advice, semantic row equality, or nonuniform hard-row selection is used.
- K_idx^cov(pi) is the set of charged row representatives after first-owner compression, with uncovered rows retained at the exit that first exposes them.
- U_cov(pi) is the prefix-visible cost of discovering row support and verifying equality-coverage witnesses; X_cov(pi) is the same-theory SAT-row expansion cost for K_idx^cov(pi).

## Assumptions

- Circuit model: nonuniform Boolean SIZE over input length N for H_N^{SAT}; LB_N(1+epsilon) means C(H_N^{SAT})>N^{1+epsilon-o(1)} in this same model.
- Length regime: M_N=N^{q+o(1)}, formula descriptions G_N(x,j) have polylogarithmic row overhead, and generator/parsing overhead is N^{rho+o(1)} plus the explicit Gamma ledger.
- Proof-system regime: Psys_bEF^- line induction and Gap98-SRhNormalForm are available for non-FormulaEval lines with eta/tau costs already charged in Gamma_bEF(pi).
- Uniformity/advice regime: row enumerators, ownership certificates, equality witnesses, and exit dominators are computable from N and proof bits; no advice string selects rows or identifies hard truth-table positions.
- Timing regime: a quarantined FormulaEval block may delay support only until a sealed exit that dominates all external dependencies and is processed before first unquarantined use.
- Barrier status: the theorem is a nonrelativizing proof-system parser obstruction only when same-theory SAT expansion is explicit; full semantic FormulaEval remains quarantined at RealSATInfluenceRealizer_N.

## Equations

- row_count: `M_N=N^{q+o(1)}`. Valid when: Valid when N is the outer input length and the SAT-query generator exposes M_N rows with uniform polylogarithmic row descriptions.
- charged_support: `K^{cov}_{idx}(\pi)=\{r: r\text{ is first-owned before use or uncovered and sum-charged at its owner exit}\}/\equiv_{syn}`. Valid when: Valid when syntactic equality witnesses are prefix-visible and semantic equality is not used to identify row sets.
- row_expansion_charge: `X_{cov}(\pi)=N^{1+o(1)}\cdot |K^{cov}_{idx}(\pi)|`. Valid when: Applies after each charged row is expanded in the same SAT occurrence theory with polylogarithmic formula overhead.
- gamma_ledger: `\Gamma_{QEeq}(\pi)=\Gamma_{bEF}(\pi)+U_{cov}(\pi)+X_{cov}(\pi)+N^{o(1)}L_\pi`. Valid when: Valid when every FormulaEval dependency crossing a quarantine exit is dominated, visible, and charged exactly once by first ownership.
- parser_upper_bound: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{QEeq}(\pi)+O(E_\pi N)`. Valid when: Requires the parser-to-circuit simulation to preserve the nonuniform SIZE model and the same row-expansion semantics.
- lb_falsifier: `N^{\rho+o(1)}+\Gamma_{QEeq}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \pi\text{ falsifies }LB_N(1+\epsilon)`. Valid when: Valid when LB_N is asserted for the same H_N^{SAT} family and the same nonuniform circuit model.

## Attempted Derivation

- Build the proof-prefix dependency DAG. Mark quarantined FormulaEval blocks B and require a sealed exit e_B that dominates every edge from B to an unquarantined line.
- At each prefix t maintain K_t^cov, a first-owner map own_t, and a list of uncovered rows. Ordinary bEF^- and bounded-SR_h lines update only Gamma_bEF using the archived line induction.
- For a FormulaEval line inside a quarantine block, allow support to remain sealed only if no external dependency leaves the block before its exit; otherwise the first hidden row triggers the private-row falsifier.
- At exit e_B, run the visible RowSetEnumerator_N or pay full scan. For each row r, either assign first ownership, reuse a previous representative by a prefix-visible RowSetEqualityWitness_N, or keep r as an uncovered sum-charged row.
- Prove the induction invariant: every unquarantined line value after prefix t is computable by a same-theory circuit using the generator, bEF parser, and SAT expansions only for K_t^cov, with cost bounded by the running Gamma_QEeq ledger.
- In the FormulaEval exit case, syntactic equality witnesses justify reuse because they expose occurrence-level identity; semantic equality without a witness is not used and is handled by the countermodel lemma.
- At the final LB_N line, compose the generator circuit with the transcript simulator to obtain C_SIZE(H_N^{SAT})<=N^{rho+o(1)}+Gamma_QEeq(pi)+O(E_pi N). If this is below N^{1+epsilon-o(1)}, the transcript is a same-model falsifier for the asserted lower bound.

Blocking gap: The abstract proof is theorem-shaped, but paper-final validation still needs one named Psys_sym^{QEeq} bit grammar for RowSetEqualityWitness_N: row-index fields, parent pointers, occurrence-map hashes or lists, and verifier time/eta/tau costs.

## Falsifiers

- Uncovered semantic row equality used for deduplication before a prefix-visible RowSetEqualityWitness_N exists.
- A quarantined FormulaEval block whose exit does not dominate all external dependencies.
- SAT-truth branch pruning that lists only true influencing rows without a zero-latency advice-free realizer.
- Nonuniform row selector or hard-row choice embedded as proof advice rather than derived from N and proof bits.
- q<epsilon with all M_N=N^{q+o(1)} rows transparently enumerable and all other costs subthreshold, yielding a direct upper-bound falsifier.
- Same-theory expansion failure: the row-expansion circuit uses an oracle or semantic SAT rule not present in the proof model.

## Learning

Cycle 137 upgrades equality compression from a coverage invariant to a line-induction proof packet: syntactic witnesses can reduce K_idx, but semantic equality cannot. The new exact obstruction is the RowSetEqualityWitness_N bit grammar; without it, sharing is either sum-charged or becomes a private-row falsifier. This is paper-level parser progress only, not P vs NP progress.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the QEeq coverage ledger.`
- Rationale: The branch needs to test whether equality sharing is genuinely syntactic support compression or hidden semantic advice; this is the live proof-delivery boundary, not a generic MCSP slogan.
- Situation seed: A projected-dDNNF FormulaEval block for H_N^{SAT} has two quarantined subblocks B1 and B2 whose projected row sets are semantically equal, but only a fraction of B2 rows have prefix-visible occurrence-level equality witnesses to B1 representatives.
- Varied variable: coverage exponent lambda where the number of syntactically covered B2 rows is N^{lambda+o(1)} while the total projected support has size T_N=N^{t+o(1)}.
- Held-fixed controls: M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)}, and target lower-bound threshold N^{1+epsilon-o(1)} are fixed., The proof model remains Psys_sym^{QEeq} with sealed exits dominating external dependencies., Row expansion is same-theory SAT occurrence expansion; no SAT-truth advice or nonuniform selector is permitted., All enumerators and equality witnesses must be computable from N and prefix proof bits.
- Expected observation: As lambda increases, X_cov drops only for rows with actual syntactic witnesses; uncovered rows remain sum-charged. If semantic equality compresses any uncharged uncovered row, a private-row completion flips the FormulaEval value while preserving all read bits.
- Transfer certificate needed: A RowSetEqualityWitness_N verifier with explicit row-index maps, occurrence-neighborhood equality checks, prefix timing, and eta/tau overhead bounds before the compression intuition may enter Gamma_QEeq.

## Next Experiment

Instantiate RowSetEqualityWitness_N for one concrete Psys_sym^{QEeq}: specify row-index encoding, first-owner pointer, occurrence-neighborhood equality list, exit-dominator certificate, verifier bit cost, eta/tau overhead, and then recompute Gamma_QEeq on the projected-dDNNF sharing example.
