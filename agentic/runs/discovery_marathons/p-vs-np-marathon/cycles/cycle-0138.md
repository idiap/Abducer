# cycle-0138

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For extensional Psys_sym^CTSR proofs over the beta-zero XOR carrier, the least valid transparent support is the reachable counterfactual CTSR closure K_CTSR(pi). If all reachable CTSR children are declared, Gamma_CTSR line induction gives the same-model LB_N falsifier; if one reachable counterfactual child is hidden, a first-hidden-child two-world falsifier defeats occurrence completion.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) together with a Psys_sym^CTSR proof pi of LB_N(1+epsilon); M_N=N^{q+o(1)}, formula length L_N=(log N)^d, generator size N^{rho+o(1)}.
- target object: a same-model nonuniform SIZE circuit for H_N^SAT below N^{1+epsilon-o(1)}, used only as a falsifier for the claimed source lower bound.
- controlled interface: TransparentRowSupport_N^CTSR, whose fixed point K_CTSR(pi) contains final-line dependencies, visible FormulaEval rows, and every counterfactual child of every reachable adaptive TSR node; charges are Gamma_bEF, U_N, X_N, and B_CTSR.
- target-preserving condition: beta=0 polylog SAT queries, q,rho<1+epsilon, kappa+theta<epsilon for the CTSR charge, same-theory row expansion, advice-free support enumeration, and no hidden semantic branch pruning.
- bit fields: opcode, line id, source row i in [N], slot j in [M_N], CTSR node address a, branch bit b, parent-line pointer, child-list pointer, restriction mask, Tseitin-map id, formula hash, and touched occurrence-neighborhood list.
- frontier: a CTSR child (i,j,a,b) is reachable when a later proof line can use the value of its parent node through visible parent pointers from the final LB_N line.

## Assumptions

- Circuit model is nonuniform SIZE over the same basis for the source lower bound and the parser-produced upper bound; the proof transcript may be hardwired but cannot contain SAT-truth advice or hidden row selectors.
- Every transparent FormulaEval or CTSR line has a verifier-visible enumerator or pays full scan; local verification of bit fields is N^{o(1)} per listed row and does not call real SAT as an oracle.
- CTSR depth and branching are bounded so that the total number of syntactic CTSR sites is N^{kappa+o(1)} and the counterfactual child fanout per source row is N^{theta+o(1)}.
- Residual row errors E_pi are patched by equality gates at cost O(E_pi N); the falsifier is subthreshold only when E_pi<N^{epsilon-o(1)}.
- The necessity direction is extensional and relativizing over row labels; full real SAT semantic pruning is not refuted unless RealSATInfluenceRealizer_N^arb fails for the pruned step.

## Equations

- ctsr_fixed_point: `K_{0}=Dep(final),\quad K_{t+1}=K_t\cup Pred(K_t)\cup Child_{CTSR}(K_t),\quad K_{CTSR}=\bigcup_t K_t`. Valid when: Valid when proof syntax exposes all parent pointers, row indices, and CTSR child declarations.
- ctsr_charge: `B_{CTSR}(\pi)\le N^{1+\kappa+\theta+o(1)}`. Valid when: Applies when there are N source rows, N^{\kappa+o(1)} CTSR sites, and N^{\theta+o(1)} declared counterfactual children per site.
- gamma_ctsr: `\Gamma_{CTSR}(\pi)=\Gamma_{bEF}(\pi)+U_N(K_{CTSR})+X_N(K_{CTSR})+B_{CTSR}(\pi)`. Valid when: Valid after transparent support enumeration and same-theory occurrence expansion are both charged in the proof ledger.
- parser_upper_bound: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{CTSR}(\pi)+O(E_\pi N)`. Valid when: Requires the target-preserving parser simulation in the same nonuniform SIZE model with beta-zero SAT queries.
- support_density_corollary: `N\cdot |K_{idx}(\pi)|\ge N^{1+\epsilon-o(1)}\Rightarrow |K_{idx}(\pi)|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Valid when M_N=N^{q+o(1)} slots and K_CTSR has no hidden semantic row advice.

## Attempted Derivation

- Initialize K_0 with the final LB_N line and all verifier-visible parent pointers used to parse its asserted carrier lower bound.
- For each line in reverse topological order, add ordinary bEF dependencies using the existing Gamma_bEF parser; add FormulaEval rows only through visible enumerators or full-scan charge.
- For a CTSR line, read bit fields (i,j,a,b,parent,child_list,restriction_mask,Tseitin_map,formula_hash,occurrence_neighborhoods). The local verifier checks that each listed child is the correct restricted/Tseitin-transformed formula and that every branch b in the rule alphabet appears, not merely the actual semantic branch.
- Charge U_N for enumerating child indices and X_N for same-theory occurrence expansion. With N source rows, N^{kappa+o(1)} CTSR sites, and N^{theta+o(1)} counterfactual children per site, this contributes B_CTSR<=N^{1+kappa+theta+o(1)}.
- Line induction invariant: after processing a prefix, the hardwired transcript plus generator circuit computes every proof-visible row value using only K_CTSR rows and charged expansions. CTSR parent values are reconstructed from all declared counterfactual children, so adaptive pruning does not introduce unseen support.
- If N^{rho+o(1)}+Gamma_CTSR(pi)+O(E_pi N)<N^{1+epsilon-o(1)}, the constructed circuit is a same-model upper-bound falsifier for LB_N(1+epsilon).
- Necessity attempt: take the first reachable CTSR child absent from K_CTSR. Build worlds W0,W1 agreeing on all charged rows and all bit fields, toggle only the hidden child by private-row/unread-enable-bit assignment, and propagate the toggled value to the parent and final parity. The verifier sees identical transcripts, so occurrence completion was unsound.

Blocking gap: The two-world necessity proof is valid for extensional row-label or occurrence-local semantics, but it does not refute a real SAT semantic derivation proving that the hidden child is impossible unless RealSATInfluenceRealizer_N^arb fails for that derivation.

## Falsifiers

- first-hidden-child falsifier: a reachable counterfactual CTSR child is omitted while later proof lines still depend on its parent value
- actual-branch-only falsifier: the proof declares only the semantically followed branch and hides the unused branch behind an unread enable bit
- nonuniform row-selector falsifier: K_CTSR is chosen with advice not recoverable from proof syntax and N
- subthreshold residual falsifier: E_pi<N^{epsilon-o(1)} lets equality patching erase sparse row errors
- positive-beta transfer falsifier: any attempted return to black-box SAT substitution with beta>0 is capped by q+beta c+o(1) before all exponents
- semantic-pruning escape test: a valid RealSATInfluenceRealizer_N^arb listing and charging all rows neutralizes the private-row countermodel for that rule

## Learning

Cycle 138 identifies the exact minimal CTSR object as reachable counterfactual frontier closure. This improves the promoted packet: actual-branch declarations are not valid transparent support, while full reachable child declarations give the Gamma_CTSR parser with threshold kappa+theta<epsilon. The result is a scoped parser/countermodel theorem and live inference-quality packet, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the CTSR minimality proof.`
- Rationale: The branch already has a positive Gamma_CTSR parser; the remaining contribution is deciding whether actual-branch adaptive pruning can avoid counterfactual support without paying a charge.
- Situation seed: A beta-zero XOR carrier with one CTSR FormulaEval node per selected slot; the proof reads only the actual branch, while a private source row contains an unread enable bit controlling the unlisted counterfactual child formula.
- Varied variable: theta, the exponent for declared counterfactual child fanout per CTSR site, with a secondary toggle between actual-branch-only and full counterfactual declaration.
- Held-fixed controls: M_N=N^{q+o(1)} with q<1+epsilon, generator size N^{rho+o(1)} with rho<1+epsilon, polylog SAT formula length, so beta=0, same nonuniform SIZE model for source lower bound and parser upper bound, no SAT-truth advice and no hidden selector advice, residual error budget E_pi<N^{epsilon-o(1)}
- Expected observation: Actual-branch-only support appears to keep Gamma below threshold but admits two transcript-identical worlds with opposite carrier parity; full counterfactual support removes the falsifier and costs N^{1+kappa+theta+o(1)}.
- Transfer certificate needed: A formal first-hidden-child two-world construction for extensional CTSR, plus a separate nonrelativizing RealSATInfluenceRealizer_N^arb certificate before real SAT semantic pruning may be folded into the valid parser.

## Next Experiment

Write the referee-facing CTSRFrontierCompleteness proof: give closure pseudocode for K_CTSR, prove termination and minimality, verify one adaptive TSR line bit-by-bit, and instantiate the first-hidden-child falsifier on a one-node unread-enable-bit example.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For Psys_sym^ecTRS, terminal-relevant FormulaEval support is exactly the least reverse cone generated by proof-visible dependency edges. If every semantic dependency edge is complete and row-expanded in the same theory, then Gamma_ec gives the parser-to-circuit falsifier; if an edge is missing, the first missing edge yields a private-row falsifier.

## Definitions

- source object: accepted Psys_sym^ecTRS proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with N=2^n, M_N=N^{q+o(1)}, and generator size N^{rho+o(1)}.
- target object: same nonuniform Boolean SIZE lower-bound assertion CC(H_N^SAT)>N^{1+epsilon-o(1)} or the same-model upper-bound falsifier C(H_N^SAT)<N^{1+epsilon-o(1)}.
- controlled interface: terminal-relevant reverse dependency cone K_tr(pi) with proof-visible dependency edges, row enumerators, influence certificates, and prefix-scoped same-theory row expansions.
- target-preserving condition: the extractor is deterministic, advice-free, edge-complete, prefix-scoped, and charges every influencing row or enumerator before the FormulaEval inference is used.
- Psys_sym^ecTRS is bEF plus FormulaEval/SR_h rules whose lines carry finite certificates Pred_cert(a), Row_cert(a), and Exp_cert(a).
- Edge completeness means that changing unlisted rows while fixing listed rows and reachable parent line values cannot change any terminal-relevant FormulaEval line.
- K_idx(K_tr) is the set of SAT-row indices appearing in the terminal-relevant cone, not the full selector zoo and not dead proof lines.

## Assumptions

- Model: nonuniform Boolean circuits over the beta-zero SAT-parity carrier; proof manipulation is extraction/prefix splicing, not a many-one reduction from SAT.
- Regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, SR fanout/window parameter h=N^{eta+o(1)}, visible existential witness budget N^{alpha+o(1)} when present, and rho<1+epsilon.
- Uniformity/advice: the parser receives only N and pi; row sets and dependency edges must be computable from displayed proof syntax without SAT-truth advice or hidden nonuniform selectors.
- Same-theory condition: every charged FormulaEval line can be replaced by bEF-compatible row-expanded material using fresh extension variables scoped before the line that uses them.
- Soundness condition: LB_N(1+epsilon) is interpreted in the same SIZE model as the constructed upper-bound circuit; otherwise the falsifier is not target-preserving.
- Prior restricted packet assumed: SparseResidualPatching_N and the bEF line parser are valid for the beta-zero carrier after row support is explicitly charged.

## Equations

- terminal_reverse_cone: `K_0={ell_out}; K_{t+1}=K_t union {b: b in Pred_cert(a) for some a in K_t}; K_tr(pi)=fix(K_t)`. Valid when: Valid when the proof DAG is finite and each terminal-relevant line exposes a finite predecessor certificate before the extractor runs.
- edge_complete_charge: `Gamma_ec(pi)=Gamma_bEF(K_tr)+N*|K_idx(K_tr)|+N*E_tr+U_tr+R_edge`. Valid when: Valid when row expansion, FormulaEval expansion debt, enumeration debt, and dependency-edge verification are all charged inside the reverse cone.
- row_equivalent_support: `S_hat_ec(pi)=ceil(Gamma_ec(pi)/N)=|K_idx(K_tr)|+E_tr+ceil(U_tr/N)+ceil(R_edge/N)+o(S_hat_ec)`. Valid when: Applies when all nonrow bEF bookkeeping is lower order or explicitly included in Gamma_bEF over the terminal cone.
- same_model_upper_bound: `C(H_N^SAT) <= N^{rho+o(1)} + Gamma_ec(pi)`. Valid when: Requires the target-preserving residual-patching lemma, edge-complete row support, and same-theory prefix splicing for every FormulaEval use.
- subthreshold_falsifier: `N^{rho+o(1)}+Gamma_ec(pi)<N^{1+epsilon-o(1)} => not LB_N(1+epsilon)`. Valid when: Applies only when LB_N asserts a lower bound against the identical nonuniform SIZE model used by the constructed circuit.
- density_corollary: `if other debts are o(N^epsilon), then |K_idx(K_tr)|/M_N >= N^{epsilon-q-o(1)}`. Valid when: Valid when the accepted proof is sound, rho<1+epsilon, and visible row charge dominates enumeration and bEF debts.

## Attempted Derivation

- Parse pi as a finite proof DAG and mark ell_out, the final LB_N(1+epsilon) line.
- Run the reverse worklist K_0={ell_out}; when line a is popped, add exactly the lines and row certificates in Pred_cert(a), rejecting if an edge certificate is ill-formed.
- For bEF and SATeq lines, reuse the existing bit-explicit line induction but restrict the charge to lines in K_tr; dead-line padding contributes zero because it is unreachable from ell_out.
- For each FormulaEval line in K_tr, use EdgeCompletenessVerifier_N to show that Row_cert(a) is extensionally influence-closed; then splice the row-expanded bEF derivation before a with fresh extension variables.
- Accumulate Gamma_ec=Gamma_bEF+N|K_idx|+NE_tr+U_tr+R_edge and obtain a same-theory proof transcript whose parsed circuit computes the residual carrier used by LB_N.
- Apply SparseResidualPatching_N for the beta-zero carrier to derive C(H_N^SAT)<=N^{rho+o(1)}+Gamma_ec(pi).
- Conclude that any accepted sound proof with N^{rho+o(1)}+Gamma_ec<N^{1+epsilon-o(1)} falsifies LB_N(1+epsilon); therefore sound proofs must pay S_hat_ec>=N^{epsilon-o(1)} row-equivalent support.
- If EdgeCompletenessVerifier_N fails at the first reachable FormulaEval line a, choose an omitted influential row r*, form two row assignments agreeing on K_idx(K_tr) and differing at r*, and obtain indistinguishable proof transcripts with different semantic line values.

Blocking gap: EdgeCompletenessVerifier_N is proved only for rules whose row influence is syntactically visible or row-covered. Arbitrary semantic real-SAT FormulaEval remains blocked at RealSATInfluenceRealizer_N: no advice-free certificate currently lists all terminal-relevant influencing rows.

## Falsifiers

- First omitted dependency edge: a terminal-relevant FormulaEval line changes when an unlisted private row is flipped while every visible row and proof bit is fixed.
- Unread-enable-bit selector: the selector code exposes a harmless row unless a hidden enable bit activates an uncharged private row, refuting occurrence-only parsing.
- q<epsilon ceiling: the known source upper bound C(H_N^SAT)<=N^{1+q+o(1)} is already a falsifier to any claimed LB_N(1+epsilon) proof when q<epsilon-o(1).
- Semantic advice leakage: a row chosen by real SAT truth but absent from pi violates the no-advice extractor condition and blocks a valid transfer.
- Dead-line padding is no longer a falsifier to the charge theorem because K_tr is terminal-relevant; it remains a test for any theorem charging the full proof.

## Learning

Cycle 138 upgrades the cycle-137 terminal-cone refinement by making dependency-edge completeness a finite checker and a no-go fork. The valid theorem is restricted: edge-complete transparent FormulaEval pays Gamma_ec and yields the same-model parser falsifier below N^{1+epsilon}. If a terminal-relevant semantic edge is omitted, the private-row construction is a finite falsifier. This is route-level proof-system certification, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design concrete thought experiment now as a falsifier probe for dependency-edge completeness.`
- Rationale: The branch has already consolidated selector examples; the remaining issue is whether semantic FormulaEval influence is actually visible. A concrete private-row experiment tests the exact bridge rather than restating barrier folklore.
- Situation seed: Take H_N^SAT with M_N=N^{q+o(1)} rows and a single terminal-relevant bounded-SR_h FormulaEval line whose visible certificate lists an interval row cover L, while an optional hidden enable bit e redirects one child query to a private row r* outside L.
- Varied variable: The hidden-edge exponent delta, where |R_hidden|=N^{delta+o(1)}; delta=-infinity means no hidden rows and delta>=0 means at least one omitted dependency edge.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and rho<1+epsilon., The displayed proof bits, visible row list L, bEF parser, and prefix-splicing rules are held fixed., The target model is the same nonuniform Boolean SIZE model used by LB_N(1+epsilon)., The extractor receives no SAT-truth advice and may use only pi and N.
- Expected observation: At delta=-infinity the Gamma_ec charge is auditable. At any delta>=0 a first omitted row r* gives two indistinguishable transcripts with different semantic FormulaEval values, so the hidden-support route is invalid unless the row is surfaced and charged.
- Transfer certificate needed: A uniform EdgeCompletenessVerifier_N plus same-theory row-expansion certificate proving that every terminal-relevant semantic influence edge is listed before the FormulaEval line is used.

## Next Experiment

Instantiate EdgeCompletenessVerifier_N on one projected-dDNNF FormulaEval rule with explicit row-cover certificates and then remove one reachable cover edge to verify the first-missing-edge falsifier line by line.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Restricted RowSetEqualityWitness_N lemma: for bit-explicit Psys_sym^{QEeq,cell} transcripts, first-owner equality compression is valid exactly when every sharing edge has a prefix-visible syntactic witness whose cell-level row-index equations are locally checkable before the borrowing FormulaEval line exits quarantine. Then the Gamma_QEeq line induction charges owned rows once, charges uncovered rows by sum, and never uses semantic equality to reduce support.

## Definitions

- source object: bit-explicit Psys_sym^{QEeq,cell} transcript pi for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with quarantined FormulaEval blocks, first-owner row sets, and proposed equality-compression edges.
- target object: same-theory nonuniform SIZE upper-bound falsifier for LB_N(1+epsilon) over the H_N^SAT truth table, with circuit model matching the claimed lower-bound model.
- controlled interface: prefix-visible RowSetEqualityWitness_N records that expose selector producer identifiers, row-index encodings, cell decompositions, local membership proofs, and first-owner transfer maps before any external dependency uses the shared rows.
- target-preserving condition: every FormulaEval influence row is either first-owner charged, syntactically equality-covered by a prefix-visible witness, or sum-charged; no semantic SAT-truth advice, hidden row selector, or after-the-fact equality proof may reduce Gamma_QEeq.
- Psys_sym^{QEeq,cell}: the FormulaEval row producers are from a canonical cell-decomposable grammar: interval unions, disjoint subcubes, ROBDD paths under fixed order, guarded dDNNF products with exposed decomposability, and projected variants only with explicit projected-enumerator certificates.
- RowSetEqualityWitness_N bit fields: header (N,t,owner id,borrower id,dominator-exit id), producer-code hashes as proof pointers not cryptographic assumptions, cell-pair table, row-index affine/prefix equations, projection-witness policy, first-owner target pointer, and local verifier transcript.
- prefix-visible: all witness bits and producer pointers occur in pi_{<t_exit} where t_exit dominates every external dependency of the quarantined FormulaEval value.
- same-theory expansion: each charged row is expanded into the same SAT formula family G_N(x,j) used by H_N^SAT, without changing to an oracle or advice-selected language.

## Assumptions

- Length regime: N tends to infinity, M_N=N^{q+o(1)}, row index length is log M_N+O(1), formula length is N^{o(1)}, and generator overhead for G_N is N^{rho+o(1)}.
- Proof model: Psys_bEF^- line parsing and bounded-SR_h normal form are already available, so non-FormulaEval lines contribute Gamma_bEF(pi).
- Selector model: each row producer in the equality witness has an advice-free canonical decomposition whose cells have syntactic row-index constraints checked in polylog(N) or N^{o(1)} time per cell record.
- Uniformity/advice condition: the parser receives only N and pi; it cannot use SAT truth, nonuniform row choices, semantic equivalence oracles, or after-the-fact witnesses.
- Timing condition: a sharing edge may reduce charge only if its witness is prefix-visible at the quarantine exit that dominates the first external use of the borrowed FormulaEval value.
- Naturalness/barrier status: the theorem is a sparse proof-transcript parser and finite falsifier, not a large constructive useful property; it is outside the direct natural-proofs template but does not prove any main lower bound.

## Equations

- Gamma_QEeq_ledger: `\Gamma_{QEeq}(\pi)=\Gamma_{bEF}(\pi)+U_{vis}(\pi)+X_{own}(\pi)+X_{uncovered}(\pi)+W_{eq}(\pi)`. Valid when: Valid when every FormulaEval line belongs to Psys_sym^{QEeq,cell} and all equality-compression edges are either prefix-witnessed or explicitly left uncovered for sum charging.
- first_owner_expansion: `X_{own}(\pi)=E_N\,|K_{own}(\pi)|\,N^{o(1)},\qquad X_{uncovered}(\pi)=E_N\,|K_{uncovered}^{occ}(\pi)|\,N^{o(1)}`. Valid when: Applies after the row-expansion parser uses the same G_N formulas and uncovered borrowed occurrences are charged separately rather than identified semantically.
- equality_witness_cost: `W_{eq}(\pi)\le N^{o(1)}\sum_{e\in E_{share}(\pi)} |w_e|`. Valid when: Requires each witness w_e to be a bit-level syntactic cell-decomposition certificate with local verification and no hidden SAT-truth or hash-collision assumption.
- parser_upper_bound_falsifier: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{QEeq}(\pi)+O(E_\pi N^{1+o(1)})`. Valid when: Valid when the transcript parser, generator G_N, row expansions, equality witnesses, and extension lines are all uniform from N and pi in the same nonuniform SIZE model.
- LB_refutation_threshold: `N^{\rho+o(1)}+\Gamma_{QEeq}(\pi)+O(E_\pi N^{1+o(1)})<N^{1+\epsilon-o(1)}\Rightarrow \pi\text{ is a falsifier for }LB_N(1+\epsilon)`. Valid when: Applies only for the scoped lower-bound claim over H_N^SAT in the identical target circuit class and exponent regime, not for P versus NP itself.

## Attempted Derivation

- Fix N, M_N=N^{q+o(1)}, and a Psys_sym^{QEeq,cell} transcript pi whose non-FormulaEval lines are already parsed by Gamma_bEF.
- For each FormulaEval row producer P at proof time t, parse a producer record containing its grammar tag, input proof pointers, row-index length, canonical cell decomposition, and enumerator or scan policy.
- For each sharing edge e=(owner O, borrower B), require a RowSetEqualityWitness_N record before the quarantine exit of B: header, owner and borrower producer ids, dominator exit, cell-pair table, local row-index equations, projection-fiber policy, and first-owner transfer pointer.
- Define K_own by the first producer occurrence of each syntactically witnessed row cell; define K_uncovered^{occ} as every borrowed influence occurrence not covered by a prefix-visible witness; define W_eq as the local verification cost of witness records.
- Induct over proof lines. Ordinary bEF and bounded-SR_h lines preserve the existing Gamma_bEF invariant. Transparent FormulaEval introduction adds U_vis plus row expansion for newly owned cells. A witnessed sharing edge adds W_eq and no row expansion for covered cells because local row-index equality maps the borrowed enumerator to an earlier owner. An unwitnessed edge is not compressed and its occurrence enters K_uncovered^{occ}.
- At a quarantine exit, check domination: every external dependency of the delayed FormulaEval value is dominated by the exit line and every support row used after exit is owned, witnessed, or uncovered-sum-charged. This gives Gamma_QEeq for the prefix.
- Build the target circuit for H_N^SAT by hardwiring pi, running the generator G_N, expanding exactly the charged row formulas, and wiring extension and parity gates according to the parsed transcript. Equality witnesses are used only to reuse already built row-expansion subcircuits.
- Conclude the same-model SIZE upper bound. If this bound is below N^{1+epsilon-o(1)}, the transcript is a valid low-cost falsifier for the proposed LB_N(1+epsilon) statement.

Blocking gap: The derivation is complete only for canonical cell-decomposable producer grammars with syntactic equality witnesses. It does not yet handle arbitrary AC0 membership-only selectors, semantic SAT-truth-pruned equality, or projected supports without certified projected enumeration.

## Falsifiers

- falsifier: an equality edge represented only by equal cardinalities or equal hashes without syntactic row-index equations; two row sets can differ on a private row while all parsed bits agree.
- falsifier: a projected-dDNNF selector whose auxiliary witness fiber is hidden; either pay the projected enumerator cost or an unread witness-enable bit changes support.
- falsifier: a FormulaEval block whose equality witness appears after the first external dependency; prefix causality fails even if eventual equality is true.
- falsifier: semantic SAT-pruned equality that identifies row sets by truth of subformulas rather than proof-visible row syntax; this is a RealSATInfluenceRealizer_N obligation, not transparent support.
- falsifier: arbitrary AC0 membership-only support with no output-sensitive enumerator; the parser must full-scan or quarantine the selector.

## Learning

Cycle 138 turns RowSetEqualityWitness_N from a coverage slogan into a restricted bit grammar. Equality compression is valid for canonical cell-decomposable producers only through prefix-visible row-index equations and dominator timing; otherwise rows are sum-charged or a private-row falsifier applies. This strengthens the paper-level FormulaEval parser obstruction and makes no P vs NP lower-bound claim.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for RowSetEqualityWitness_N and projected selector leakage.`
- Rationale: The branch needs a concrete target-preserving test because equality compression can silently import semantic advice; an abstract restatement would not reveal whether K_idx is reduced by syntax or by hidden row selection.
- Situation seed: Projected-dDNNF FormulaEval for H_N^SAT where owner A enumerates rows j with visible witness y, borrower B claims the same projected row set after SAT-truth pruning of y, and a quarantined block tries to reuse A's row expansions without paying B's support.
- Varied variable: projection fiber entropy ell, measured as the number of auxiliary witness bits hidden from the prefix-visible row enumerator.
- Held-fixed controls: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) and M_N=N^{q+o(1)} remain fixed., Target class is the same nonuniform SIZE model used by LB_N(1+epsilon)., The proof system is Psys_sym^{QEeq} with bEF/SR_h parser costs already charged., No SAT-truth advice, nonuniform row selector, or after-the-fact equality witness may be used.
- Expected observation: For ell=0 or certified projected enumeration, first-owner compression is valid and pays W_eq plus owned expansion. As ell grows without a witness, either U_vis pays the projected enumerator/witness support or an unread enable bit gives a private-row falsifier.
- Transfer certificate needed: A prefix-visible RowSetEqualityWitness_N with canonical projected enumerator and local row-index equations, or else a zero-latency RealSATInfluenceRealizer_N that lists every SAT-semantic influence row and charges it before first use.

## Next Experiment

Instantiate the bit grammar on one projected-dDNNF example with hidden projection fiber: write the actual witness records, compute W_eq and U_vis, and show whether compression is valid, sum-charged, or refuted by an unread-enable-bit falsifier.
