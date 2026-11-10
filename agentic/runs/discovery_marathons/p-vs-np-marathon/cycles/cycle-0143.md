# cycle-0143

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For Psys_bEF^- plus transparent FormulaEval, counterfactual declared TSR, and ranked same-theory quotient merges, the least quotient-closed support K_Q(pi) gives a valid Gamma_QCTSR line induction; any first unranked or uncertified merge has a private-row falsifier.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, L=(log N)^d, generator size N^{rho+o(1)}, and claimed LB_N(1+epsilon) in nonuniform SIZE.
- target object: scoped parser/falsifier theorem for QCTSR proof certificates; subthreshold Gamma yields a same-model circuit for H_N^SAT, not P != NP.
- controlled interface: proof transcript pi -> least ranked quotient-closed support K_Q(pi) -> charged ledger Gamma_QCTSR(pi) -> circuit upper bound for H_N^SAT.
- target-preserving condition: beta=0 polylog SAT calls, advice-free visible row enumeration, complete counterfactual CTSR frontier, and ranked acyclic same-theory quotient certificates charged before deletion.

## Assumptions

- Psys model is bit-explicit bEF^- plus transparent FormulaEval, counterfactual declared TSR, and quotient merges carrying verifier-visible same-theory certificates.
- Rank r(e) on quotient edges strictly decreases along certificate dependencies; cycles and adaptive advice-chosen merges are disallowed.
- Uniformity is syntactic auditability from N and pi; nonuniformity is allowed only in the final circuit model, not in row selection.
- Exponent regime: q,rho<1+epsilon; CTSR charge exponent is 1+kappa+theta; promotion only when every ledger term is below N^{1+epsilon-o(1)}.

## Equations

- QClosure: `K_Q(\pi)=\operatorname{lfp}(R\mapsto R\cup Dep_{bEF}(R)\cup FE(R)\cup CTSR(R)\cup Cert_Q(R))`. Valid when: Valid when proof syntax exposes every FormulaEval, CTSR, and quotient dependency before the consuming line.
- QLedger: `\Gamma_{QCTSR}(\pi)=\Gamma_{bEF}(\pi)+U(K_Q)+X(K_Q)+B_{CTSR}(\pi)+B_Q(\pi)`. Valid when: Applies after ranked same-theory certificates are charged and duplicate row deletions are certified.
- ParserUpperBound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{QCTSR}(\pi)+O(E_\pi N)`. Valid when: Requires beta-zero target calls and same nonuniform SIZE model for the reconstructed circuit.

## Attempted Derivation

- Initialize K_Q at the final LB_N rows; repeatedly add bEF parents, transparent FormulaEval rows, all reachable counterfactual TSR frontier children, and all dependencies of quotient certificates.
- For a quotient merge a~b, require a same-theory certificate DAG whose edges have strictly smaller rank; add its occurrence rows before allowing deletion of either duplicate row from the ledger.
- Induct on proof lines ordered by proof index and quotient rank. Each consumed row is either explicit in K_Q or replaced by a certified same-theory row; hence the simulator pays exactly Gamma_QCTSR.
- Contraposition: at the first merge lacking a ranked certificate, build two transcripts agreeing on K_Q but differing on the private deleted row or unread enable bit; the proof transcript agrees while H_N parity can differ.

Blocking gap: This does not solve RealSATInfluenceRealizer_N^arb for full semantic FormulaEval; it only handles proof-carrying same-theory quotient compression.

## Falsifiers

- First uncertified quotient merge: a deleted duplicate row has no surfaced same-theory certificate in K_Q, so private-row spoofing invalidates the parser.
- Cyclic certificate SCC: ranked descent fails, so the line induction has no well-founded order and the quotient deletion is not valid.
- Adaptive advice-chosen merge: the row pair is selected by semantic advice rather than N and pi, causing nonuniform leakage outside Gamma_QCTSR.
- Threshold collapse falsifier: if 1+kappa+theta>=1+epsilon or Gamma_QCTSR>=N^{1+epsilon-o(1)}, the parser gives no contradiction to LB_N.

## Learning

Cycle 143 turns quotient compression into a proof-carrying ledger rule: Gamma may shrink only through ranked acyclic same-theory certificates already in K_Q. Unranked quotienting is not a harmless optimization; it is exactly a private-row falsifier.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for QCTSR minimality.`
- Rationale: The branch needs a concrete audit of quotient compression, because an abstract EqSAT quotient can hide precisely the row that the private-row countermodel flips.
- Situation seed: A six-row beta-zero XOR carrier transcript where CTSR generates two counterfactual child rows, a quotient merge deletes one as EqSAT-equivalent, and the final parity line consumes the quotient class.
- Varied variable: Rank slack Delta: the number of strictly lower-ranked certificate dependencies available before the quotient deletion.
- Held-fixed controls: M_N=N^{q+o(1)} and L=(log N)^d with beta=0., Generator overhead N^{rho+o(1)} and final model nonuniform SIZE., Complete counterfactual CTSR frontier is declared before quotienting., No semantic advice is allowed in row-pair selection.
- Expected observation: Delta>=1 with all dependencies surfaced preserves Gamma_QCTSR; Delta=0 or a rank cycle creates a first-bad-merge transcript where two worlds agree on visible rows but differ on carrier parity.
- Transfer certificate needed: A finite acyclic same-theory certificate checker whose dependency rows are included in K_Q before deletion and whose cost is charged in B_Q.

## Next Experiment

Instantiate the six-row QCTSR transcript, list row IDs, quotient certificate dependencies, rank labels, and show the first uncertified merge produces two agreeing visible transcripts with opposite H_N parity.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For Psys_sym^{SATsel,TEC,cache}, memoized SAT-defined FormulaEval is target-preserving exactly when every terminal-relevant cache hit points to a previously charged extensional miss whose visible key determines the influencing RowSet, or the miss pays a full scan. Under this interface the TEC prefix-splice proof yields a valid Gamma_cache ledger and the same-model upper-bound falsifier for LB_N(1+epsilon).

## Definitions

- source object: a Psys_sym^{SATsel,TEC,cache} proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with N=2^n and M_N=N^{q+o(1)}.
- target object: the nonuniform SIZE model for the same N-bit truth table, where the claimed lower bound is C(H_N^SAT)>N^{1+epsilon-o(1)}.
- controlled interface: terminal-edge-complete TransparentRowSupport with cache-key extensionality, visible row covers or full scans, prefix-scoped same-theory expansion, and no hidden advice.
- target-preserving condition: every terminal-relevant FormulaEval cache value exposes a dependency edge to a charged miss whose visible key determines all influencing rows, or else pays the full N M_N row-scan charge before semantic use.
- RowSet(a) is the set of SAT-parity rows j whose SAT(G_N(x,j)) value can change FormulaEval atom a on some proof-relevant assignment.
- Key(a) is extensional if N, selector code, generator identifier, row-domain parameters, cover certificate or scan flag, and all dependency parents determine RowSet(a).
- F_scan(pi) counts terminal-relevant cache misses using full scans; K_cov(pi) is the union of visibly covered terminal-relevant rows; U_key(pi) is the bit cost of key checking, cache links, and cover verification.

## Assumptions

- Length regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, bounded-SR height h=N^{eta+o(1)}, and generator overhead size(G_N)=N^{rho+o(1)} with rho<1+epsilon.
- Proof model: bit-explicit bEF plus terminal-edge-complete SATsel FormulaEval; cache hits are proof lines with parent pointers to cache misses, not semantic oracles.
- Uniformity/advice condition: the parser, worklist, RowSet covers, and cache-key checker are deterministic from (N,pi) and use no hidden row advice or SAT-truth advice.
- Same-theory condition: each charged FormulaEval miss can be prefix-spliced into bEF-compatible row-expanded material with fresh extension variables and no change to later proof semantics.
- Barrier status: the object is proof-system-specific and nonrelativizing only through explicit proof syntax; if it induces a large constructive useful truth-table property, the natural-proofs falsifier must be run separately.

## Equations

- cache_support_fixed_point: `K_{cache}(\pi)=\operatorname{lfp}(T\mapsto T\cup Pred_{tec}(T)\cup RowCov(T)\cup FullScan(T))`. Valid when: Valid when terminal-edge completeness gives every proof-relevant dependency edge and cache hits point to visible charged misses.
- cache_gamma_ledger: `\Gamma_{cache}(\pi)=\Gamma_{bEF}(\pi)+U_{key}(\pi)+N\,|K_{cov}(\pi)|+F_{scan}(\pi)\,N M_N+N^{o(1)}`. Valid when: Applies after cache-key extensionality, row-cover verification, full-scan accounting, and same-theory prefix expansion are all certified.
- same_model_falsifier_threshold: `N^{\rho+o(1)}+\Gamma_{cache}(\pi)<N^{1+\epsilon-o(1)}\;\Rightarrow\; \pi\text{ falsifies }LB_N(1+\epsilon)`. Valid when: Valid in the nonuniform SIZE target model when the extracted circuit computes the same H_N^SAT truth table.
- forced_row_equivalent_support: `\widehat S_{cache}:=|K_{cov}|+F_{scan}M_N+\left\lceil(\Gamma_{bEF}+U_{key})/N\right\rceil\ge N^{\epsilon-o(1)}`. Valid when: Requires sound acceptance of LB_N, rho below one plus epsilon, and the cache-aware parser theorem above.

## Attempted Derivation

- Type every FormulaEval cache event as miss-cover, miss-scan, or hit-to-miss; reject semantic hits without a visible parent edge.
- Run the terminal reverse-cone worklist from the final LB_N line; add bEF predecessors, TEC semantic edges, cache parent edges, cover rows for miss-cover entries, and all M_N rows for miss-scan entries.
- For each miss-cover row j, splice a same-theory bEF expansion of SAT(G_N(x,j)); for a miss-scan splice all rows; for a cache hit reuse the already spliced miss under a fresh-variable hygiene convention.
- Charge key verification and cache-link checking to U_key, row-expanded covers to N|K_cov|, and scans to F_scan N M_N, giving Gamma_cache.
- Compose the generator circuit of size N^{rho+o(1)} with the expanded transcript. If the total is below N^{1+epsilon-o(1)}, the accepted LB_N line is contradicted in the same nonuniform SIZE model.
- For any omitted cache parameter, choose the first terminal-relevant key collision and toggle a private selected row; visible transcript checks agree but FormulaEval semantics changes, yielding the finite falsifier.

Blocking gap: The restricted theorem is derived for cache-key-extensional SATsel FormulaEval. Arbitrary semantic output-sensitive SATsel enumeration remains blocked at RealSATInfluenceRealizer_N because the proof syntax may assert the selected set without a cover, scan, or extensional key.

## Falsifiers

- Cache-key collision: two selector contexts share the visible key while a terminal-relevant private row lies in their symmetric difference.
- Unread-enable-bit row: a hidden enable variable gates one selected row and is never listed in K_cache.
- Subthreshold ledger falsifier: N^{rho+o(1)}+Gamma_cache(pi)<N^{1+epsilon-o(1)} contradicts the source LB_N claim in the same SIZE model.
- q<epsilon source-ceiling falsifier: M_N=N^{q+o(1)} gives insufficient row mass for an N^{1+epsilon} lower-bound claim unless extra debt is charged.
- Semantic output-sensitive SATsel without cover or scan is quarantined because it may use SAT-truth advice to choose rows.

## Learning

Memoization is not a free escape from TransparentRowSupport. A cache hit is target-preserving only through an extensional charged miss; otherwise the first bad key gives a finite private-row falsifier. The new quantitative threshold is D_cache plus visible cover density, not another selector-family slogan.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The remaining SATsel issue is not abstract barrier folklore; it is whether memoized semantic row selection leaks uncharged support while preserving the beta-zero target carrier.
- Situation seed: A Psys_sym^{SATsel,TEC,cache} proof has one terminal FormulaEval line whose selector is SAT(Q_a(j)) over M_N rows and whose answer is memoized under a visible cache key before proving LB_N(1+epsilon) for H_N^SAT.
- Varied variable: cache-key coarseness lambda, the number of row-determining selector parameters omitted from the visible key.
- Held-fixed controls: N=2^n and M_N=N^{q+o(1)} for the same SAT-parity carrier H_N^SAT., Generator G_N and overhead N^{rho+o(1)} with rho<1+epsilon., Terminal-edge-complete reverse-cone parser and same-theory prefix splicing., No hidden advice, no SAT-truth row advice, and the same nonuniform SIZE target model.
- Expected observation: At lambda=0 the extensional key determines RowSet and the Gamma_cache charge is valid; at any lambda>0 a collision can isolate a private selected row unless the rule pays the full scan N M_N charge.
- Transfer certificate needed: A finite CacheKeyExtensionality_N checker proving Key(a) determines RowSet(a), or else a first-collision certificate that instantiates the private-row falsifier before the intuition affects proof obligations.

## Next Experiment

Instantiate CacheKeyExtensionality_N on the projected-dDNNF SATsel cache example: list key fields, compute U_key and F_scan, then try to construct the first bad key by deleting one row-domain parameter.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Restricted theorem packet: in Psys_sym^{QEeq,cell}, first-owner compression across quarantined FormulaEval blocks is valid exactly for rows covered by prefix-visible canonical cell-refinement witnesses at the dominating exit; all uncovered influence is sum-charged, and any uncharged semantic deduplication gives a same-theory private-row falsifier.

## Definitions

- source object: a bit-explicit Psys_sym^{QEeq,cell} transcript pi for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with canonical cell-decomposable FormulaEval producers, quarantine blocks, exit dominators, and row-set equality witness fields.
- target object: a same-model nonuniform SIZE circuit upper bound for H_N^SAT, used only to refute a claimed low-cost proof of LB_N(1+epsilon) when the parsed transcript is subthreshold.
- controlled interface: the parser extracts Gamma_QEeq(pi), owner table Own_t, first-owned row set K_idx^own(pi), enumerator costs U_t, row-expansion costs X_t, equality-witness costs W_t, and hidden-influence falsifier data from proof bits alone.
- target-preserving condition: every FormulaEval row influencing an external line is prefix-visible at its dominating exit, either first-owned or covered by a prefix row-index equality witness, expanded in the same SAT-occurrence theory, and selected without advice or SAT-truth pruning.
- canonical cell producer: each selector emits a finite disjoint cell list with a row-index decoder, local membership test, and parent pointers to earlier proof lines; projected cells must expose the projection fiber or pay the enumerated support cost.
- first-owner rule: a row is charged to the first prefix producer whose certified cell contains it; later producers may reuse it only through a prefix-visible refinement witness proving identical row indices, not through semantic equality of SAT values.
- quarantine exit: a syntactic dominator line after which a delayed FormulaEval value first affects an external dependency; all row support and equality compression for that block must be charged before that exit.

## Assumptions

- Length regime: N tends to infinity, M_N=N^{q+o(1)}, formula generator overhead is N^{rho+o(1)}, and all parser overheads are measured in the same N-scale ledger.
- Proof model: Psys_sym^{QEeq,cell} extends the already parsed Psys_bEF^- rules by FormulaEval cells, syntactic quarantine, and prefix-visible row-equality witnesses; no full semantic SAT-extensionality rule is included.
- Circuit model: the target upper bound is nonuniform SIZE over the same Boolean encoding of H_N^SAT used by the alleged LB_N proof; no uniform lower-bound conclusion is claimed.
- Uniformity/advice regime: the parser, row enumeration, equality checking, and owner updates are advice-free and computable from N and pi; hidden row selectors or nonuniform hard-row choices invalidate the transfer.
- Same-theory condition: row expansion builds the SAT-occurrence formulas used by the proof, so the upper-bound circuit and the proof statement refer to the same H_N^SAT object.
- Timing condition: equality witnesses may compress only if present before the first external dependency of the dominated quarantine block; after-the-fact semantic deduplication is not valid.
- Barrier status: the lemma is a restricted parser/falsifier theorem, nonrelativizing only through explicit SAT occurrence expansion, and it does not assert a natural-property lower bound or P != NP.

## Equations

- QEeq ledger: `\Gamma_{QEeq}(\pi)=\Gamma_{bEF}(\pi)+\sum_t U_t^{new}+\sum_t X_t^{own}+\sum_t W_t^{eq}`. Valid when: Valid when Psys_sym^{QEeq,cell} exposes owner, equality-witness, and exit-dominator fields before each FormulaEval dependency is used.
- owned support expansion: `X_N(\pi)\ge N^{1+o(1)}\,|K_{idx}^{own}(\pi)|`. Valid when: Applies after every first-owned influential row is expanded in the same SAT-occurrence theory with polylog formula length.
- parser upper bound: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{QEeq}(\pi)+O(E_\pi N)`. Valid when: Requires the parsed proof transcript, generator circuit, and row expansions to be advice-free and in the same nonuniform SIZE model.
- subthreshold falsifier: `N^{\rho+o(1)}+\Gamma_{QEeq}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \pi \text{ is not a sound proof of } LB_N(1+\epsilon)`. Valid when: Valid when LB_N(1+epsilon) asserts a same-object SIZE lower bound exceeding the constructed parser circuit threshold.
- q support corollary: `|K_{idx}^{own}|/M_N\ge N^{\epsilon-q-o(1)}\Rightarrow X_N\ge N^{1+\epsilon-o(1)}`. Valid when: Applies after M_N=N^{q+o(1)} and owned support is counted after prefix-visible equality compression only.

## Attempted Derivation

- Parse each proof line into type, parent pointers, quarantine-block id, exit-dominator id, FormulaEval producer id, canonical cell descriptors, owner pointers, equality-witness pointers, and charge records.
- Maintain a prefix state S_t=(K_t,Own_t,Gamma_t). Ordinary bEF and bounded-SR_h lines update Gamma_t by the archived Gamma_bEF induction and do not change K_t.
- For a FormulaEval cell C inside quarantine, enumerate its visible row cells or record full-scan charge U_t. Each row not already owned is inserted into K_t with owner t and row-expansion charge X_t.
- For a later cell C' claiming reuse, verify a prefix row-index refinement witness covering C' by already owned cells. If verified before the dominating exit, add W_t^{eq} and no new row charge; if not verified, sum-charge C' as new support.
- At a quarantine exit, require that every external dependency from the block is dominated by the exit line and that the exit ledger includes all first-owner, uncovered, and equality-witness costs. This gives the invariant Gamma_t=Gamma_bEF+sum U+sum X+sum W for the reachable prefix-closed cone.
- If a minimal external FormulaEval use has an influential row r outside the owner/equality/sum-charged cone, form two occurrence completions agreeing on all visible transcript bits and charged rows but differing on r or on its unread enable bit. The proof prefix cannot distinguish them, yet the FormulaEval value can change, giving the private-row falsifier.
- Combine the parsed transcript circuit, the generator for G_N, and same-theory row expansions to obtain C_SIZE(H_N^SAT)<=N^{rho+o(1)}+Gamma_QEeq(pi)+O(E_pi N). If this is below the asserted LB_N threshold, the transcript is refuted in the same model.

Blocking gap: No blocking gap remains for restricted canonical cell producers with prefix-visible refinement witnesses and exit dominators. The unresolved full-system gap is RealSATInfluenceRealizer_N for semantic FormulaEval and semantic RowSetEqualityWitness_N without syntactic cell witnesses.

## Falsifiers

- Private-row/unread-enable-bit falsifier: a hidden influential row outside prefix-owned support yields two visible-equivalent completions with different FormulaEval value.
- Semantic-dedup falsifier: reusing row support by SAT extensionality without a prefix row-index witness is invalid unless the proof sum-charges the row set.
- Owner-reassignment falsifier: changing the first owner after an external dependency can hide the actual support used by the parser and breaks the valid ledger.
- Truth-pruned projection falsifier: a projected-dDNNF selector that omits witness fibers using SAT truth advice is not transparent and must pay full support or be quarantined.
- Subthreshold transcript falsifier: if N^{rho+o(1)}+Gamma_QEeq+O(E_pi N)<N^{1+epsilon-o(1)}, the claimed LB_N(1+epsilon) proof is refuted in the same SIZE model.

## Learning

Cycle 143 adds an exit-local ownership ledger: syntactic equality compression is valid not merely when cell equality is witnessed eventually, but when first-owner coverage is prefix-visible at the dominating quarantine exit before any external dependency. This closes a timing loophole in the restricted FormulaEval parser and leaves full semantic deduplication quarantined at RealSATInfluenceRealizer_N.

## Gedanken Experiment Design Seed

- Need decision: `Design concrete falsifier probe now.`
- Rationale: The branch has a restricted theorem but the dangerous loophole is semantic equality compression at quarantine exits; a concrete row-support experiment tests whether the new exit-local owner ledger is really target-preserving.
- Situation seed: A projected-dDNNF FormulaEval block computes a subset of rows for H_N^SAT, exits through one dominator, and claims that a later block has the same row set by semantic SAT equality while leaving one enable bit for a row r unread.
- Varied variable: Coverage fraction zeta of the later block's cells by prefix-visible row-index refinement witnesses, with zeta=1 syntactic coverage and zeta<1 leaving at least one hidden cell.
- Held-fixed controls: H_N^SAT, M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)}, and the same nonuniform SIZE target are fixed., The proof syntax remains Psys_sym^{QEeq,cell} with canonical cell producers, first-owner table, and one dominating quarantine exit., No SAT-truth advice, nonuniform row selector, or after-the-fact equality witness is allowed., The alleged LB_N(1+epsilon) statement and all row expansions refer to the same SAT-occurrence theory.
- Expected observation: For zeta=1 the ledger charges only first-owned rows plus W^{eq}; for any zeta<1 the uncovered hidden row is either sum-charged or supports a private-row falsifier by flipping the unread enable bit while preserving all visible proof fields.
- Transfer certificate needed: A verified CellOwnerExitLedger_N proof showing prefix witness coverage, first-owner monotonicity, exit dominance, and same-theory row expansion before the observation can affect the proof queue.

## Next Experiment

Instantiate the exit-local owner ledger on one projected-dDNNF FormulaEval block with a shared projected row set: write the actual owner fields, refinement-witness fields, uncovered-cell sum charge, and the unread-enable-bit falsifier when one projected fiber lacks a prefix witness.
