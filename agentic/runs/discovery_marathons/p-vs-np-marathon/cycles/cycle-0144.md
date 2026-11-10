# cycle-0144

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: ranked QCTSR ledger validation

## Candidate Lemma

For beta-zero parity carrier certificates in Psys_bEF^- plus transparent FormulaEval, counterfactual declared TSR, and quotient compression, Gamma may be reduced by deleting duplicate counterfactual rows only through a dependency-closed ranked acyclic same-theory certificate forest already charged in K_Q. Under this interface, the line induction yields a same-model parser-to-circuit falsifier for any subthreshold LB_N(1+epsilon) proof transcript.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, polylog SAT instance length L_N=(log N)^d, generator size N^{rho+o(1)}, and a Psys_QCTSR proof pi of LB_N(1+epsilon) over this carrier.
- target object: a nonuniform SIZE_N circuit computing H_N^SAT below N^{1+epsilon-o(1)}, hence a route-level falsifier for the claimed source lower-bound certificate, not a proof of P != NP.
- controlled interface: K_Q(pi) is the least reachable support fixed point closed under bEF dependencies, transparent FormulaEval supports, all counterfactual TSR children, and ranked same-theory quotient certificates whose dependencies have lower rank and are already visible.
- target-preserving condition: beta=0, q,rho<1+epsilon, every row influence is advice-free enumerable or full-scan charged, every quotient merge has a surfaced same-theory certificate preserving SAT labels, and all charges enter Gamma_QCTSR before the LB_N inference is used.

## Assumptions

- Circuit model is the same nonuniform SIZE model for the source carrier and the constructed falsifier circuit; no change of lower-bound model is hidden in the parser theorem.
- Length regime is N -> infinity, M_N=N^{q+o(1)}, L_N=(log N)^d with fixed d>1, and all o(1) terms are uniform over fixed q,rho,kappa,theta,epsilon.
- Proof system is restricted: bit-explicit EF support, transparent FormulaEval lines, declared counterfactual bounded TSR, and quotient rules with explicit ranked same-theory certificates; full semantic FormulaEval is not included.
- Advice status is negative: the row set K_Q(pi), ranks, parent pointers, quotient certificates, and TSR children are determined by N and pi, not by SAT labels or hidden nonuniform row advice.
- Same-theory certificates may use EqSAT, renaming, and surfaced Tseitin equivalences only when their dependency rows are already in K_Q(pi) with smaller rank; cyclic or adaptive quotient dependencies are invalid.
- Sparse residual patching is allowed only for E_pi bad source rows and costs O(E_pi N) gates, so the falsifier is valid only when this term is included in the final size inequality.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j=1}^{M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)}`. Valid when: Valid when the source carrier is the beta-zero parity construction with uniformly generated polylog-length SAT rows and no target query length exponent hidden in G_N.
- ledger: `\Gamma_{QCTSR}(\pi)=\Gamma_{bEF}(\pi)+U(K_Q)+X(K_Q)+B_{CTSR}(K_Q)+B_Q(K_Q)`. Valid when: Applies after K_Q is computed as the least dependency-closed support cone containing all proof-reachable FormulaEval, counterfactual TSR, and ranked quotient-certificate rows.
- ctsr_charge: `B_{CTSR}(K_Q)\le N^{1+\kappa+\theta+o(1)}`. Valid when: Valid when the reachable TSR frontier has exponent kappa, every frontier node exposes N^{theta+o(1)} counterfactual children, and child encodings are charged before semantic pruning.
- quotient_charge: `B_Q(K_Q)=\sum_{e\in F_Q}\left(|cert(e)|+N\cdot |Rows(cert(e))\setminus K_{<rank(e)}|\right)`. Valid when: Requires each quotient edge e to carry a ranked same-theory certificate whose previously unseen dependency rows are added and charged before the deleted row is merged.
- parser_falsifier: `N^{\rho+o(1)}+\Gamma_{QCTSR}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Applies in the same nonuniform SIZE model after the generator, parsed transcript, quotient certificates, TSR children, and sparse residual corrections are all counted in the circuit size.

## Attempted Derivation

- Fix pi and compute K_Q by least fixed point: seed final LB_N line; add bEF parent dependencies; add transparent FormulaEval support rows and row-expansion witnesses; add all reachable counterfactual TSR children; add quotient-certificate dependency rows in increasing rank until closure.
- Define a quotient edge r_del -> r_keep to be admissible only if a certificate cert(e) proves same-theory SAT(r_del)=SAT(r_keep) using rows in K_{<rank(e)}. The rank order makes the certificate forest acyclic and independently checkable.
- Run line induction. bEF lines use the existing Gamma_bEF parser. FormulaEval lines add U(K_Q)+X(K_Q). CTSR lines add all counterfactual children, so actual-branch pruning cannot hide influence. Quotient lines replace a deleted row by a kept row only after the equality of SAT labels is certified from already charged dependencies.
- Construct C_pi: compute G_N in size N^{rho+o(1)}, evaluate the parsed transcript and same-theory certificates using Gamma_QCTSR gates, and patch E_pi exceptional source rows by equality tests of cost O(E_pi N).
- If the displayed size is below N^{1+epsilon-o(1)}, then the claimed source lower bound LB_N(1+epsilon) is falsified in the same nonuniform model. This is a valid route-level implication and not a lower bound for H_N.
- For necessity, choose the first quotient edge without a ranked certificate. Because all earlier dependencies are fixed, flip the private deleted row label while preserving the visible prefix. If its residual parity incidence is odd, the proof transcript is unchanged but H_N changes, contradicting extensional safety of the compressed ledger.

Blocking gap: The positive proof is complete only for restricted Psys_QCTSR. Full semantic FormulaEval or hidden adaptive pruning still requires RealSATInfluenceRealizer_N^{arb}, an advice-free nonrelativizing theorem that lists and charges all real SAT influence rows before use.

## Falsifiers

- First unranked quotient merge: a deleted row is identified with a kept row without a surfaced rank-decreasing same-theory certificate.
- Cyclic quotient dependency: certificates for two row deletions depend on each other and therefore cannot be audited by a finite lower-rank induction.
- Advice-chosen quotient forest: the merge list depends on SAT labels or hidden semantic advice rather than on N and pi.
- Actual-branch-only TSR declaration: an unlisted counterfactual child can be made the private row, so occurrence completion is invalid.
- q<epsilon with full row scan: FormulaEval expansion costs N^{1+q+o(1)} below the claimed N^{1+epsilon} lower bound, giving a direct same-model falsifier.
- Positive beta black-box substitution: SAT in SIZE(n^c) would give source circuits of size N^{q+beta c+o(1)}, so all-exponent target exclusion is invalid unless beta=0 or genuinely subpolynomial.

## Learning

Cycle 144 closes a proof-audit loophole: quotient compression in counterfactual TSR is valid exactly as proof-carrying ranked same-theory compression, not as semantic row deletion. The contribution is a scoped parser/falsifier theorem: ranked QCTSR preserves the Gamma line induction, while the first unranked quotient merge is a concrete private-row falsifier. This improves the paper theorem boundary without giving any H_N lower bound or P != NP result.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the ranked quotient rule and as a finite audit for QCTSR promotion.`
- Rationale: The branch no longer needs another abstract barrier statement; the proof packet hinges on whether quotient deletion is a charged same-theory transformation or an uncharged semantic compression that changes the parity carrier.
- Situation seed: Take H_N^SAT with M_N=N^q rows and a counterfactual TSR node whose two children produce syntactically different but Tseitin-equivalent SAT formulas. Allow the proof to merge one child row into the other either with a surfaced ranked EqSAT/Tseitin certificate or by an unlisted semantic quotient instruction.
- Varied variable: The single varied parameter is zeta, the exponent of omitted quotient-certificate support: omitted dependency rows have count N^{zeta+o(1)}, ranging from zeta=0 fully surfaced to zeta>0 hidden support.
- Held-fixed controls: beta=0 parity carrier and polylog SAT row length are fixed., M_N=N^{q+o(1)}, generator cost N^{rho+o(1)}, and the same nonuniform SIZE model are fixed., Counterfactual TSR frontier and all FormulaEval visible supports are held fixed., No SAT-truth advice or hidden row selector is allowed outside the varied quotient-certificate omission.
- Expected observation: For zeta=0 the ranked certificate charge preserves the Gamma_QCTSR line induction. For any zeta with omitted rows and an odd residual incidence, a private-row flip leaves the transcript unchanged but changes H_N, showing that the compressed proof is not extensionally valid.
- Transfer certificate needed: A formal same-theory soundness certificate plus rank-decreasing dependency closure is needed before quotient compression may reduce Gamma; otherwise the private-row falsifier blocks the proof-to-circuit transfer.

## Next Experiment

Write the referee-checkable K_Q closure pseudocode with rank ordering, then test it on a two-child Tseitin-equivalent TSR merge and on the same example with the certificate omitted to exhibit the first-unranked-merge falsifier.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For Psys_sym^{TEC,cache}, terminal-edge-complete transparent FormulaEval with extensional cache hits is conservatively replaceable by row-expanded bEF material with charge Gamma_cache; non-extensional cache hits have a first-bad-key private-row falsifier.

## Definitions

- source object: an accepted proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) in Psys_sym^{TEC,cache}, with N=2^n and M_N=N^{q+o(1)}.
- target object: a same-model nonuniform SIZE circuit for H_N^SAT of size N^{rho+o(1)}+Gamma_cache(pi), used only as a falsifier to the asserted source lower bound.
- controlled interface: each terminal-relevant FormulaEval cache miss exposes selector code, row-cover certificate, row-expansion recipe, parent pointers, and each cache hit points to an earlier miss with bEF-checkable equality of all extensional key fields.
- target-preserving condition: the cache key must determine the same RowSet and same FormulaEval dependencies without advice, and the miss expansion must be prefix-spliced in the same proof theory with fresh-variable hygiene.

## Assumptions

- Model is nonuniform Boolean SIZE; the proof system is bEF plus terminal-edge-complete transparent FormulaEval and explicit cache-link rules.
- Length regime is N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, generator overhead size(G_N)=N^{rho+o(1)}, and rho<1+epsilon.
- Uniformity condition: from N and pi a deterministic parser computes the terminal reverse cone, cache-hit links, miss row covers, and expansion scripts with no semantic SAT advice.
- Same-theory condition: every charged FormulaEval miss can be expanded into bEF/SATeq lines before its first use, and every cache hit is replaced by a pointer/equality derivation to that miss.
- Cache extensionality condition: two cache keys equal in the proof iff their visible selector code, environment, row cover, and influence edges define the same RowSet and same row-local formula family.
- Non-claim boundary: the lemma certifies a restricted parser/falsifier theorem and is not evidence for P != NP.

## Equations

- cache_cone_fixed_point: `K_{cache}(\pi)=\operatorname{lfp}(\{\ell_{final}\}\cup Dep_{bEF}\cup Dep_{TEC}\cup HitToMiss\cup MissRows)`. Valid when: Valid when every terminal-relevant dependency edge and cache hit pointer is syntactically visible and independently checkable from the proof transcript.
- cache_gamma_ledger: `\Gamma_{cache}(\pi)=\Gamma_{bEF}(K_{cache})+U_{TEC}(K_{cache})+X_{miss}(K_{cache})+D_{cache}(K_{cache})`. Valid when: Valid when miss expansions are charged once, hits only pay equality-link debt, and dead proof lines outside the terminal cone are ignored.
- miss_expansion_charge: `X_{miss}(K_{cache})\le N^{1+o(1)}\sum_{\mu\in Miss(K_{cache})}|RowSet(\mu)|`. Valid when: Applies after each visible cache miss supplies an advice-free row enumerator and each enumerated row has a same-theory bEF expansion of size N^{1+o(1)}.
- subthreshold_falsifier: `N^{\rho+o(1)}+\Gamma_{cache}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Requires the extracted transcript circuit to compute the same H_N^SAT in the same nonuniform SIZE model as the asserted lower bound.
- visible_density_corollary: `\sum_{\mu\in Miss(K_{cache})}|RowSet(\mu)|\ge N^{\epsilon-o(1)}\quad\Rightarrow\quad density\ge N^{\epsilon-q-o(1)}`. Valid when: Valid when all non-row debts are lower order, M_N=N^{q+o(1)}, and the source lower bound survives the subthreshold circuit falsifier.

## Attempted Derivation

- Define K_cache(pi) by a worklist initialized at the final LB_N line; add ordinary bEF parents, TEC dependency edges, cache-hit-to-miss edges, and all miss row-expansion edges.
- For a cache miss mu, use its visible selector code and row-cover certificate to enumerate RowSet(mu), then splice the row-expanded bEF/SATeq derivation before the first terminal use of mu.
- For a cache hit h, require h to point to an earlier miss mu and require a bEF-checkable equality proof for every extensional key field; replace h by a pointer/equality derivation and charge only D_cache(h).
- Order all splices by first use and allocate fresh extension variables per splice; this preserves same-theory derivability and prevents cache-variable capture.
- Run the previous terminal-cone line induction: ordinary bEF lines charge Gamma_bEF, visible enumeration charges U_TEC, miss expansions charge X_miss, and cache links charge D_cache.
- Obtain a circuit for H_N^SAT of size N^{rho+o(1)}+Gamma_cache(pi); if this is below N^{1+epsilon-o(1)}, it is a same-model falsifier to LB_N(1+epsilon).
- If the worklist encounters a terminal cache hit without an extensional earlier miss, choose the first such hit and construct two completions agreeing on all visible cache fields while flipping one omitted influencing row.

Blocking gap: The restricted proof is blocked only for semantic output-sensitive cache rules whose key does not visibly determine RowSet; the named open bridge is CacheExtensionality_N, a cache-specific instance of RealSATInfluenceRealizer_N.

## Falsifiers

- first-bad-key falsifier: a terminal cache hit reuses a value while omitting one influencing private row r*, so two completions have identical visible proof transcripts but different FormulaEval values.
- unread-enable-bit falsifier: the selector has a hidden enable bit for r*; the cache key records the selector name but not the enable valuation, invalidating occurrence completion.
- non-injective-digest falsifier: a shortened hash-like cache key is used without an in-theory collision-free proof, so equal keys do not certify equal RowSet semantics.
- dead-padding falsifier avoided: K_cache charges only the terminal reverse cone, so irrelevant cached misses cannot inflate the theorem or hide the real support.
- q<epsilon enumeration falsifier: if the carrier has M_N=N^{q+o(1)} with q<epsilon and all debts are subthreshold, the extracted upper bound contradicts the claimed LB_N(1+epsilon).

## Learning

Cycle 144 turns cache hygiene into a theorem-shaped interface: memoization is target-preserving only through extensional charged misses and bEF-checkable hit links. The valid invariant is Gamma_cache on the terminal cone. A non-extensional cache key has a finite private-row falsifier. This is proof-system boundary progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The route needs a concrete cache-specific test because memoization can look like a transparent syntactic optimization while secretly importing semantic row advice.
- Situation seed: A SATsel FormulaEval proof has one cache miss for a selector family and many cache hits; one selected row r* is controlled by an unread enable bit that is omitted from the cache key but can flip the final parity carrier H_N^SAT.
- Varied variable: cache key explicitness lambda, ranging from a surface selector name only to a full extensional row-cover certificate with equality proofs.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)}, and the same beta-zero SAT-parity carrier H_N^SAT., Terminal-edge-complete proof syntax, same-theory prefix splicing, and no hidden nonuniform advice for the parser., The asserted target lower bound remains LB_N(1+epsilon) against the same nonuniform SIZE model.
- Expected observation: Below full extensional explicitness, one obtains two visible-identical cache transcripts with different hidden row influence; at full extensional explicitness, each hit collapses to a charged miss plus D_cache equality debt.
- Transfer certificate needed: A formal CacheExtensionality_N certificate: proof-visible key equality must imply equality of RowSet, influence edges, and row-local formulas, and every miss must have a charged same-theory expansion.

## Next Experiment

Write the standalone paper theorem: CacheExtensionality_N for Psys_sym^{TEC,cache}, with line-by-line K_cache worklist pseudocode, Gamma_cache induction, and a one-row unread-enable-bit counterexample; then check whether any remaining SATsel output-sensitive cache rule supplies the required extensional row-cover certificate.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Restricted theorem packet: for Psys_sym^QEeq transcripts with canonical cell-decomposable FormulaEval blocks, equality compression is valid exactly at a dominating quarantine exit where first-owner coverage is prefix-visible; uncovered rows are charged once, and uncharged uncovered influence gives a private-row falsifier.

## Definitions

- source object: A bit-explicit Psys_sym^QEeq transcript pi over H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, a Psys_bEF^- core, and quarantined FormulaEval blocks B whose exit e(B) dominates every external dependency.
- target object: A same-theory nonuniform SIZE upper bound for H_N^SAT or a refutation of an asserted LB_N(1+epsilon) proof line; this is not a uniform P != NP separation.
- controlled interface: At each exit e(B), the parser sees canonical cell producers, row-index equations, first-owner pointers, and refinement witnesses before any external use; it charges new uncovered rows and enumerator overhead.
- target-preserving condition: Row expansions use the same SAT instances G_N and the same nonuniform SIZE model as LB_N; no semantic SAT advice, hidden deduplication, nonuniform row selection, or post-exit witness discovery is allowed.

## Assumptions

- Model: Psys_sym^QEeq extends the previously parsed Psys_bEF^- line rules by syntactic quarantine blocks and prefix-visible FormulaEval exits only.
- Length regime: N tends to infinity, M_N=N^{q+o(1)}, formula length per row is N^{1+o(1)}, and rho,q,epsilon are fixed constants unless explicitly varied.
- Uniformity/advice regime: the parser, enumerators, first-owner table, and row-equality witnesses are computed from N and proof-prefix bits with no hidden advice.
- Cell regime: each FormulaEval producer at exit e has a canonical disjoint cell decomposition and bit-checkable refinement witnesses to earlier owner cells.
- Timing regime: an equality witness is usable only if it is visible at e(B) before the first external dependency on B.
- Same-model regime: the derived upper bound and the challenged LB_N(1+epsilon) statement are both in the same unrestricted nonuniform SIZE model.

## Equations

- new_rows_at_exit: `K_{new}(e)=K(e)\setminus\bigcup_{o<e}\mathrm{Cov}_{e}(o)`. Valid when: Valid when K(e) is the exit-visible row set and Cov_e(o) contains only prefix-visible refinement witnesses to earlier first-owner cells.
- exit_local_gamma_ledger: `\Gamma_{QEeq}(\pi)=\Gamma_{bEF}(\pi)+\sum_{e\in Exit(\pi)}\left(U_e+N^{1+o(1)}|K_{new}(e)|\right)+\eta(\pi)+\tau(\pi)`. Valid when: Valid when every FormulaEval external dependency is dominated by a charged exit and every compressed row has a prefix-visible equality witness.
- same_model_upper_bound_falsifier: `N^{\rho+o(1)}+\Gamma_{QEeq}(\pi)+O(E_{\pi}N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Applies after the parser simulation constructs a same-model nonuniform circuit for H_N^SAT below the asserted lower-bound threshold.
- support_budget_cutoff: `N^{1+o(1)}|K_{idx}(\pi)|<N^{1+\epsilon-o(1)}\iff |K_{idx}(\pi)|<N^{\epsilon-o(1)}`. Valid when: Requires that row expansion costs N^{1+o(1)} per distinct first-owned row and no hidden semantic rows are used uncharged.

## Attempted Derivation

- Define Exit(pi) as quarantine exits that dominate every later dependency on internal FormulaEval lines; reject any block with an external edge bypassing its exit.
- At each exit e, parse the canonical cell producer for K(e), enumerate cells or pay scan charge, and verify row-index equations against earlier owner cells visible in the prefix pi_{<=e}.
- Maintain Own_e(r), the first visible owner of each row r; if r is covered by a prefix-visible refinement witness to Own_{<e}(r), reuse the prior row circuit, otherwise put r into K_new(e).
- Induct on proof lines: Psys_bEF^- lines use the archived Gamma_bEF parser, quarantined internal lines have no external effect, and exit lines expose exactly the charged row values needed by later dependencies.
- Sum the enumerator costs U_e and first-owned row expansions N^{1+o(1)}|K_new(e)| to obtain Gamma_QEeq(pi).
- Compose the row circuits with the generator for G_N and the bEF transcript simulator; if the displayed inequality is below N^{1+epsilon-o(1)}, obtain a same-model SIZE circuit contradicting LB_N(1+epsilon).
- For the negative direction, choose the first external dependency whose influential row is neither charged nor prefix-covered; flip an unread enable bit or private row occurrence while preserving all visible transcript bits, making the FormulaEval value disagree.

Blocking gap: The derivation is complete only for canonical cell-decomposable producers with prefix-visible equality witnesses. Full semantic FormulaEval and semantic row deduplication remain blocked at RealSATInfluenceRealizer_N and noncanonical RowSetEqualityWitness_N.

## Falsifiers

- falsifier: a row-equality compression witness appears only after the dominating exit or after the first external dependency.
- falsifier: a membership-only selector claims output-sensitive charge without an enumerator and without paying full scan cost.
- falsifier: semantic deduplication merges row sets by SAT truth rather than by prefix-visible row-index equations.
- falsifier: an unread enable bit changes a FormulaEval row while every parser-visible occurrence bit is fixed.
- falsifier: a nonuniform selector or hard-row choice supplies the carrier row, so the target language lower bound is not advice-free.

## Learning

Cycle 144 closes a timing loophole in equality compression: the valid unit is not a row set eventually shown equal, but a row covered by a prefix-visible first-owner refinement witness at the dominating exit. This yields a restricted line-induction theorem for Gamma_QEeq and a finite private-row falsifier for hidden semantic deduplication. It is paper-level parser progress only, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch needs a concrete test of the new exit-local timing condition; abstract TransparentRowSupport_N restatements no longer improve the proof queue.
- Situation seed: Twin projected-dDNNF FormulaEval blocks B1 and B2 in the beta-zero family H_N^SAT, both semantically selecting the same N^t rows, with B2 exiting after B1 and claiming equality compression against B1.
- Varied variable: coverage deficit exponent lambda, where B2 has N^{lambda+o(1)} rows not covered by prefix-visible cell-refinement witnesses at its exit.
- Held-fixed controls: H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)} and row expansion cost N^{1+o(1)}., Same Psys_sym^QEeq syntax, same bEF core Gamma_bEF, same generator overhead N^{rho+o(1)}, and no semantic SAT advice., The B2 exit dominates all later dependencies, so only witness coverage, not timing topology, is varied.
- Expected observation: If lambda<epsilon and all uncovered rows are charged, B2 remains within the possible low-cost upper-bound falsifier budget; if any of the N^{lambda} rows is used uncharged, a private-row completion flips B2 while preserving visible proof bits. The threshold lambda=epsilon marks loss of subthreshold support.
- Transfer certificate needed: A prefix-visible RowSetEqualityWitness_N bit grammar plus an exit-dominator certificate; without both, the thought experiment is only a falsifier probe and cannot reduce Gamma_QEeq.

## Next Experiment

Instantiate the theorem on one projected-dDNNF pair with an explicit cell-refinement witness table: list verifier bit fields for producer id, cell id, owner pointer, row-index equation, exit id, and dependency edge; compute U_e and |K_new(e)|, then construct the unread-enable-bit falsifier for the same example after deleting one witness.
