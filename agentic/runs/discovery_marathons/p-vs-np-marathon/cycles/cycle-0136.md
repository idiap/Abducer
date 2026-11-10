# cycle-0136

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For beta-zero parity carrier proofs in Psys_sym^{CTSR}, complete counterfactual child declarations give a computable least closed support cone K_CTSR(pi). The bit-explicit parser line induction yields a same-model upper-bound falsifier whenever N^{rho+o(1)}+Gamma_CTSR(pi)+O(E_pi N)<N^{1+epsilon-o(1)}. This is a restricted parser/falsifier theorem, not a P != NP claim.

## Definitions

- source object: Psys_sym^{CTSR} proof pi for H_N^{SAT}(x)=xor_{j<M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, |G_N(x,j)|=(log N)^d, d>1, and bit-explicit Psys_bEF^- base lines.
- target object: A same nonuniform SIZE-model circuit for H_N^{SAT} below the claimed LB_N(1+epsilon) threshold, hence a route-level falsifier for that source lower-bound certificate.
- controlled interface: The least prefix-closed counterfactual support cone K_CTSR(pi), computed from verifier-visible parent pointers, FormulaEval row certificates, bEF dependencies, and declared bounded Tseitin self-reduction child tables.
- target-preserving condition: beta=0 polylog target queries, advice-free support enumeration, same-theory occurrence expansion, no SAT-truth row advice, and all counterfactual CTSR children charged before semantic use.
- CTSR line bit fields: line_id, rule_tag=CTSR, parent_row a, formula_id f, restriction word r, depth counter h, branch-coordinate list B, child_index b, child_row c(a,b), Tseitin-map id, occurrence-neighborhood pointers, enable-bit source, and local OR-of-children witness.
- K_CTSR closure rule: start from final LB_N row, add syntactic proof dependencies, add every row in each visible FormulaEval support certificate, and for every reached CTSR parent add every declared counterfactual child, not merely the branch used by the proof transcript.

## Assumptions

- Length regime: N ranges over valid carrier lengths; M_N=N^{q+o(1)} and generator size is N^{rho+o(1)}.
- Circuit model: nonuniform Boolean SIZE, with equality patching of E_pi bad x-rows costing O(E_pi N) gates in the same model.
- Proof model: Psys_bEF^- lines are bit-explicit; Psys_sym^{CTSR} adds only FormulaEval lines satisfying TransparentRowSupport_N and CTSR lines with complete counterfactual child tables.
- CTSR overhead: the total declared child-row count is N^{kappa+theta+o(1)}, so same-theory occurrence expansion charges N^{1+kappa+theta+o(1)}.
- Threshold regime: the falsifier is subthreshold when max{rho, gamma_CTSR, 1+e_error}<1+epsilon in exponent notation; in particular kappa+theta<epsilon keeps the CTSR charge harmless.
- Uniformity/advice status: the parser may use proof syntax and N, but not SAT truth-table advice, hidden row selectors, or semantic branch-pruning advice.
- Barrier status: the theorem is nonrelativizing only if a real SAT influence realizer is added; this restricted CTSR version is syntactic and outside any claim about full EF+SAT semantic reasoning.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j<M_N}\mathrm{SAT}(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad |G_N(x,j)|=(\log N)^d`. Valid when: Valid when N ranges over the carrier lengths and G_N is the fixed advice-free generator.
- least_closed_support: `K_{t+1}=K_t\cup \mathrm{Dep}_{bEF}(K_t)\cup \mathrm{FE}(K_t)\cup \mathrm{CTSR}_{cf}(K_t),\quad K_{CTSR}=\bigcup_t K_t`. Valid when: Valid when proof syntax exposes parent pointers, FormulaEval support, and counterfactual CTSR child tables.
- ledger: `\Gamma_{CTSR}(\pi)=\Gamma_{bEF}(\pi)+U(K_{CTSR})+X(K_{CTSR})+B_{CTSR}(\pi)`. Valid when: Valid when each line is parsed in the same nonuniform SIZE model and all reachable influences are charged.
- ctsr_charge: `B_{CTSR}(\pi)\le N^{1+\kappa+\theta+o(1)}`. Valid when: Valid when each active row has N^{\kappa+\theta+o(1)} declared children and row expansion costs Theta(N).
- transcript_upper_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{CTSR}(\pi)+O(E_\pi N)`. Valid when: Valid when the generated proof transcript has E_pi residual bad rows and equality patching is allowed in SIZE.
- source_lb_falsifier: `N^{\rho+o(1)}+\Gamma_{CTSR}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Valid when the inequality is evaluated in the same source circuit model as LB_N.

## Attempted Derivation

- Define a CTSR proof line as a finite record with explicit parent_row, formula_id, restriction_word, depth_counter, branch-coordinate list, child-row identifiers, Tseitin-map id, enable-bit source, and occurrence-neighborhood pointers.
- Compute K_CTSR(pi) by a monotone fixed point from the final LB_N line: add bEF dependencies, transparent FormulaEval support, same-theory row expansions, and every counterfactual CTSR child of each reached parent.
- For each row in K_CTSR, expand the referenced SAT formula occurrences and attach the local verifier showing SAT(parent)=OR_b SAT(child_b) or the declared bounded self-reduction relation used by the rule.
- Induct on proof lines: bEF and SATeq lines use Gamma_bEF, transparent FormulaEval lines use U(K)+X(K), and CTSR lines use only already charged counterfactual child rows.
- Build the transcript circuit A_pi from the generator plus the parsed proof transcript; its size is bounded by N^{rho+o(1)}+Gamma_CTSR(pi).
- If A_pi has residual error on E_pi source rows, patch by equality gates of total size O(E_pi N), obtaining the displayed upper bound for H_N^{SAT}.
- Contrapose: any claimed LB_N(1+epsilon) proof in this restricted model with subthreshold Gamma_CTSR is refuted in the same SIZE model.

Blocking gap: The derivation does not handle arbitrary semantic branch pruning. The named open bridge is RealSATInfluenceRealizer_N^{arb}: from real SAT semantics and proof syntax alone, uniformly list every influencing child row with charged overhead before the semantic rule is used.

## Falsifiers

- first-hidden-child adaptive pruning: actual-branch-only declaration lets two transcripts agree while the carrier parity differs
- unread-enable-bit FormulaEval: the selected row is semantically live but absent from K_CTSR
- SAT-truth advice in child selection: destroys advice-free support enumeration and invalidates the parser
- positive-beta substitution leakage: if target query length is N^beta with beta>0, the upper bound q+beta c caps all-exponent transfer
- threshold collapse: kappa+theta>=epsilon makes CTSR expansion alone too expensive for the subthreshold falsifier
- nonuniform row selector leakage: a short selector hardwires the charged support without surfacing verifier-visible dependencies

## Learning

Cycle 136 turns counterfactual declared TSR from a boundary slogan into a bitfield-level closed-support theorem: K_CTSR(pi) is a finite fixed point, Gamma_CTSR is derived by line induction, and first-hidden-child adaptive pruning is the exact falsifier for extensional safety. The valid contribution remains a scoped parser/falsifier theorem for beta-zero parity magnification certificates; it does not prove H_N lower bounds or P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The route has a nearly completed restricted theorem; the remaining ambiguity is not abstract hardness magnification but whether counterfactual child completeness is really necessary for target-preserving parsing.
- Situation seed: A beta-zero parity carrier H_N^{SAT} with M_N=N^q generated polylog SAT slots and a Psys_sym proof using one bounded Tseitin self-reduction line whose actual branch is declared but one counterfactual child row is hidden behind an unread enable bit.
- Varied variable: alpha, the exponent such that the number of source rows whose proof value depends on hidden counterfactual children is E_hidden=N^alpha.
- Held-fixed controls: Keep beta=0 and |G_N(x,j)|=(log N)^d with d>1, so SAT circuit substitution remains N^{o(1)}., Keep q,rho,kappa,theta below the advertised subthreshold window except for the varied hidden-row error exponent alpha., Keep the proof syntax bit-explicit and the nonuniform SIZE model identical on source and target sides., Keep the hidden child semantically live: flipping its SAT label changes either a reached FormulaEval value or the final parity bit.
- Expected observation: For alpha<epsilon, the hidden-child mechanism yields a small visible transcript plus O(N^{1+alpha}) equality patching, so the claimed LB_N(1+epsilon) certificate is falsified. At alpha>=epsilon the sparse-patch falsifier no longer proves collapse, but the proof still lacks a valid transparent parser unless the children are charged.
- Transfer certificate needed: An advice-free RealSATInfluenceRealizer_N^{arb} or a syntactic complete counterfactual declaration certificate that lists the hidden child in K_CTSR with same-theory row expansion cost before the semantic pruning line is used.

## Next Experiment

Select one concrete full semantic pruning rule beyond CTSR declarations, preferably adaptive Tseitin branch pruning with real SAT contradiction tests, and attempt either a charged RealSATInfluenceRealizer_N^{arb} or a minimal first-unchargeable-row countermodel.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For a Psys_sym^BTRS proof pi of LB_N(1+epsilon) for the beta-zero SAT-parity carrier, if every FormulaEval use has proof-visible selector code, row-cover certificates, influence closure, and same-theory row expansion, then the parser charge is computed on the least reverse-reachable support cone K_rr(pi), not on all displayed lines. A sound proof with rho<1+epsilon must either pay Gamma_rr(pi)>=N^{1+epsilon-o(1)} in the same nonuniform SIZE model or face a same-model upper-bound falsifier to LB_N(1+epsilon).

## Definitions

- source object: an accepted Psys_sym^BTRS proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), with N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, and generator size N^{rho+o(1)}.
- target object: a nonuniform Boolean SIZE upper bound for H_N^SAT below N^{1+epsilon-o(1)}, or equivalently a forced row-equivalent support lower bound for any sound transparent proof.
- controlled interface: reverse-reachable Budgeted Transparent Row Support, consisting of visible proof dependencies, FormulaEval row covers, influence-closed selectors, explicit enumerator charges, and prefix-scoped same-theory bEF expansion.
- target-preserving condition: the parser is deterministic and advice-free, every charged row expands inside the same proof theory and same H_N^SAT carrier, and hidden semantic SAT influence is excluded unless RealSATInfluenceRealizer_N supplies the missing row list.
- K_rr(pi) is the least fixed point reached from the final LB_N line by following ordinary proof parents, extension dependencies, selector dependencies, and certified FormulaEval row covers.
- Gamma_rr(pi) is the bit-expansion ledger restricted to K_rr(pi): bEF transcript cost plus visible enumeration debt plus row-expansion debt plus explicit FormulaEval expansion debt.
- Dead-line padding means adding proof lines unreachable from the final LB_N assertion; such lines must not change the valid transfer charge.

## Assumptions

- Model: nonuniform Boolean circuits for the target SIZE lower bound, with proof-system extraction used as a simulation, not a many-one reduction from SAT.
- Length regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, bounded-SR height h=N^{eta+o(1)}, visible existential witness set size N^{alpha+o(1)} when present.
- Uniformity and advice: the K_rr worklist, row-cover verification, and row expansion are deterministic from (N,pi) with no hidden row advice or SAT-truth advice.
- Same-theory condition: each FormulaEval row in K_rr has a prefix-scoped expansion using fresh extension variables, preserving line order and not adding semantic oracle axioms.
- Soundness cutoff: LB_N(1+epsilon) asserts C(H_N^SAT)>N^{1+epsilon-o(1)} in the same nonuniform SIZE model used by the constructed upper-bound falsifier.
- Barrier status: the object is proof-system-specific and nonrelativizing only through explicit syntax; if it induces a large poly(N)-constructive useful truth-table property, the natural-proofs audit becomes active.

## Equations

- HCarrier: `\(H_N^{SAT}(x)=\bigoplus_{j<M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)}\)`. Valid when: Valid when the source carrier is the beta-zero SAT-parity family with proof-visible generator circuits and fixed row parameter j.
- ReverseClosure: `\(K_{rr}(\pi)=\operatorname{lfp}_{S\supseteq\{L_{final}\}}(S\cup Dep(S)\cup RowCov(S)\cup Infl(S))\)`. Valid when: Valid when every dependency, row-cover, and influence edge is syntactically exposed by the BTRS verifier before FormulaEval is trusted.
- GammaLedger: `\(\Gamma_{rr}(\pi)=\Gamma_{bEF}(K_{rr})+U_{rr}+X_{rr}+N E_{rr}\)`. Valid when: Valid when transparent rows in the reverse-reachable cone are prefix-spliced into same-theory bEF material with enumerator debt charged explicitly.
- ParserUpperBound: `\(C(H_N^{SAT})\le N^{\rho+o(1)}+	ilde O(\Gamma_{rr}(\pi))\)`. Valid when: Applies after the parser expansion preserves the carrier, row indices, nonuniform circuit model, and all threshold parameters without hidden advice.
- SubthresholdFalsifier: `\(\rho<1+\epsilon\ \wedge\ \Gamma_{rr}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)\)`. Valid when: Valid when LB_N is interpreted as a same-model SIZE lower bound for H_N^{SAT} and the constructed circuit is accepted as nonuniform.
- DensityCorollary: `\(|K_{row,rr}(\pi)|/M_N\ge N^{\epsilon-q-o(1)}\)`. Valid when: Requires row-expansion debt to dominate nonrow debts and applies only to reachable transparent rows among M_N=N^{q+o(1)} carrier rows.

## Attempted Derivation

- Define the verifier-visible directed hypergraph D_pi with nodes equal to proof lines, selector-code nodes, row-cover entries, extension variables, and row-expansion obligations.
- Initialize the worklist with the final LB_N line; repeatedly add ordinary proof parents, extension definers, selector definers, certified FormulaEval row-cover entries, and influence witnesses. Termination is bounded by the finite proof encoding.
- Minimality follows by monotonicity: any prefix-closed transparent support containing the final line must contain every edge target added by the worklist, hence contains K_rr(pi).
- For each ordinary bEF node in K_rr, use the existing bit-explicit parser charge. For each FormulaEval node, replace the semantic use by its listed row expansions, paying U_rr for enumeration and X_rr+N E_rr for row material.
- Prefix-scope fresh extension variables in topological order of K_rr; unreachable lines are never spliced. This yields a same-theory proof transcript whose induced circuit has size at most N^{rho+o(1)}+tilde O(Gamma_rr(pi)).
- If rho<1+epsilon and Gamma_rr(pi)<N^{1+epsilon-o(1)}, the induced circuit contradicts the asserted LB_N(1+epsilon), giving a valid same-model falsifier. Therefore any sound transparent proof must pay the threshold charge.
- For q-density, subtract nonrow debts. If visible row debt is the leading term, |K_row,rr|>=N^{epsilon-o(1)}, and division by M_N=N^{q+o(1)} gives row density N^{epsilon-q-o(1)}.

Blocking gap: The restricted BTRS theorem is derivable from visible row covers and same-theory prefix splicing. The full semantic FormulaEval transfer remains blocked exactly at RealSATInfluenceRealizer_N: arbitrary semantic rules may have an unlisted first influencing row.

## Falsifiers

- Dead-line padding falsifier for whole-proof Gamma ledgers: add N^lambda unreachable transparent lines; old charge changes, K_rr charge does not.
- First omitted reachable row falsifier: a FormulaEval rule reads an unread enable bit selecting r*, while all visible row covers omit r*.
- Hidden selector advice falsifier: the selector code is extensionally small but its chosen accepting row set is supplied only by semantic advice, breaking no-advice enumeration.
- Nonuniform leakage falsifier: the row list is hardwired into the verifier for this N but is not computable from pi and N, invalidating target-preserving extraction.
- Naturalness falsifier probe: if K_rr induces a poly(N)-constructive large property useful against SIZE(N^{1+epsilon}), then PRF tension applies and the proof-system escape must be retyped.

## Learning

Cycle 136 strengthens the BTRS packet by identifying the least reverse-reachable support cone as the correct invariant. This is a valid route-level theorem shape: transparent FormulaEval pays Gamma_rr and is immune to dead-line padding, while hidden semantic influence is isolated by a first-omitted-row falsifier. The result supports a scoped parser/countermodel paper module and does not advance P != NP itself.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the reverse-reachable charge theorem.`
- Rationale: The branch must verify that the new charge is not an artifact of proof length and that hidden semantic influence is the only remaining obstruction; varying padding gives a concrete target-preserving stress test.
- Situation seed: Take a valid transparent BTRS proof skeleton pi for LB_N(1+epsilon) over H_N^SAT and append Delta_lambda, a block of N^lambda syntactically valid FormulaEval row scans whose conclusions are never used by the final LB_N line.
- Varied variable: lambda, the exponent of unreachable but verifier-valid padding lines.
- Held-fixed controls: The final LB_N line, generator G_N, M_N=N^{q+o(1)}, and rho<1+epsilon are held fixed., All row-cover certificates on the reverse-reachable cone are held fixed and advice-free., The target model remains nonuniform Boolean SIZE and the transfer remains extraction/prefix splicing, not a many-one reduction., No hidden semantic FormulaEval oracle is added to Delta_lambda.
- Expected observation: Whole-proof Gamma grows like N^lambda, but K_rr(pi+Delta_lambda)=K_rr(pi) and Gamma_rr is unchanged. If any Delta_lambda line can influence the final assertion without a visible edge, the first such edge becomes the private-row countermodel.
- Transfer certificate needed: A finite verifier certificate that dependency edges are complete, extension variables are prefix-scoped and fresh, and FormulaEval influence cannot cross from Delta_lambda into the final cone without entering RowCov or Infl.

## Next Experiment

Write the referee-checkable K_rr worklist verifier and test it on two finite examples: a padded transparent proof where Gamma_rr is invariant, and an unread-enable-bit FormulaEval rule where the first omitted row breaks visible-support completion.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For Psys_sym^QEeq proofs of LB_N(1+epsilon) over H_N^SAT, prefix-visible first-owner row certificates plus prefix-visible syntactic equality-cover witnesses yield a valid Gamma_QEeq line-induction parser. Covered duplicate rows are charged once; uncovered influential rows are sum-charged; any uncharged uncovered influence gives a private-row falsifier.

## Definitions

- source object: a bit-explicit Psys_sym^QEeq transcript pi for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, quarantined FormulaEval blocks, exit dominators, first-owner row certificates, and optional RowSetEqualityWitness_N certificates.
- target object: a same-theory nonuniform SIZE circuit for H_N^SAT, or a finite same-theory countermodel to the claimed low-cost LB_N(1+epsilon) proof transcript.
- controlled interface: prefix-visible row-support ownership, syntactic equality witnesses, occurrence-level row expansion, and Gamma-ledger simulation from proof lines to circuit gates.
- target-preserving condition: every influential FormulaEval row used outside quarantine is exposed before first external dependency, charged in Gamma_QEeq, expanded in the same SAT-row theory, and selected without advice or SAT-truth semantic pruning.
- K_idx^own(pi) is the set of influential row indices after first-owner compression and only after prefix-visible equality coverage is accepted.
- S_uncovered(pi) is the full row-expansion charge for influential rows not covered by a prefix-visible equality witness before their first use.

## Assumptions

- Circuit target is nonuniform SIZE over the same Boolean input variables used by H_N^SAT; the result is an upper-bound falsifier for a proof route, not a P != NP lower bound.
- Length regime has N tending to infinity, M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)}, row formulas of polylog or N^{o(1)} description size, and all o(1) terms uniform in pi.
- The restricted bEF/SR_h parser normal form is available for non-FormulaEval lines, with Gamma_bEF(pi) already charging eta/tau occurrence neighborhoods.
- Each quarantined block has a prefix-visible sealed exit dominating all external uses; delayed support is valid only inside the block and is charged at exit.
- RowSetEqualityWitness_N is syntactic: it proves row-set equality by visible code, parent pointers, or union-find derivations, not by semantic SAT equivalence or hidden hard-row advice.
- If equality coverage is missing, the theorem remains valid only with sum charging; if the missing row is also uncharged, the private-row falsifier applies.

## Equations

- QEeq ledger: `\Gamma_{QEeq}(\pi)=\Gamma_{bEF}(\pi)+U_{own}(\pi)+X_{own}(\pi)+W_{eq}(\pi)+S_{uncovered}(\pi)`. Valid when: Valid when the source proof is Psys_sym^QEeq and every FormulaEval dependency is either first-owned, syntactically equality-covered, or explicitly sum-charged before first external use.
- row expansion lower charge: `X_{own}(\pi)+S_{uncovered}(\pi)\ge N^{1+o(1)}\,|K_{idx}^{own}(\pi)|`. Valid when: Applies after first-owner compression is fixed and each charged row requires same-theory occurrence expansion of one SAT row family.
- same-model upper-bound falsifier: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{QEeq}(\pi)+O(E_\pi N^{1+o(1)})`. Valid when: Requires the target-preserving parser simulation, bit-explicit generator overhead, and same-theory expansion costs to be uniformly recoverable from the proof transcript.
- LB contradiction threshold: `N^{\rho+o(1)}+\Gamma_{QEeq}(\pi)+O(E_\pi N^{1+o(1)})<N^{1+\epsilon-o(1)}\Rightarrow \text{LB}_N(1+\epsilon)\text{ is not certified by }\pi`. Valid when: Valid when LB_N claims a SIZE lower bound above N^{1+epsilon-o(1)} in exactly the same nonuniform circuit model simulated by the parser.

## Attempted Derivation

- Initialize the parser state with Gamma_bEF for ordinary Psys_bEF^- lines and an empty first-owner map Own_t, equality union-find UF_t, and quarantined block stack.
- For a transparent FormulaEval line, enumerate its visible row set or pay full scan; for each row r, if r has no owner set Own_t(r)=line and charge one row expansion to X_own.
- For a quarantined FormulaEval block, permit delayed internal dependencies only until a sealed exit; at exit, require the dominator certificate to list the full influence cone and then apply the same ownership rule before any external line reads the block result.
- For a claimed duplicate row, accept compression only if RowSetEqualityWitness_N has a prefix-visible syntactic path in UF_t from the duplicate to its owner; charge W_eq for the witness and no second row expansion.
- For an influential row lacking ownership and equality coverage, either add it to S_uncovered by sum charging before use or mark it as the minimal bad row for the private-row countermodel.
- Maintain the induction invariant: any two occurrence completions agreeing on the charged support, accepted equality witnesses, generator bits, and bEF neighborhoods give identical values for every parsed line up to t.
- At the final LB_N line, compile the generator plus charged FormulaEval expansions plus ordinary bEF transcript into a nonuniform circuit of size N^{rho+o(1)}+Gamma_QEeq(pi)+O(E_pi N^{1+o(1)}).
- If this size is below N^{1+epsilon-o(1)}, the transcript cannot validly certify LB_N(1+epsilon) in the same target model; if a hidden influence was skipped, use the minimal-bad-line countermodel instead.

Blocking gap: Full semantic FormulaEval with SAT-extensional equality still lacks RealSATInfluenceRealizer_N: the proof syntax may assert row equality or influence by semantic SAT truth without a prefix-visible row list, equality path, or occurrence expansion charge.

## Falsifiers

- Private-row falsifier: one influential SAT row is absent from K_idx^own, Cover_eq, and SumCharged before first use, allowing two visible-identical completions with different FormulaEval values.
- Unread-enable-bit falsifier: a selector gate or projected witness hides an enable bit; flipping it changes row support without changing any prefix-visible proof bit.
- Semantic-dedup falsifier: two row sets are merged because they are true-SAT equivalent, but no syntactic RowSetEqualityWitness_N is present before first external dependency.
- q<epsilon full-scan falsifier: when M_N=N^{q+o(1)} with q<epsilon, charging all FormulaEval rows still yields N^{1+q+o(1)} below the claimed N^{1+epsilon} lower-bound threshold.
- Advice-leakage falsifier: choosing the hard row, owner representative, or equality class by nonuniform advice gives a row-level carrier but not a uniform same-model language lower bound.

## Learning

Cycle 136 upgrades equality sharing from a yes/no clause to a coverage normal form: first-owner compression is valid exactly on rows covered by prefix-visible syntactic equality witnesses; uncovered influence is either sum-charged or becomes a finite private-row falsifier. This strengthens the paper-level FormulaEval parser obstruction and does not claim P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch no longer needs another selector example; it needs to test whether equality compression can stay low-cost without prefix-visible witnesses while preserving the same target circuit model.
- Situation seed: A padded SAT-query parity family H_N^SAT with M_N=N^{q+o(1)} rows, two quarantined projected-dDNNF FormulaEval blocks, and a claimed shared row set produced by semantic projection equality rather than explicit row-set witnesses.
- Varied variable: coverage deficit exponent z, where the number of influential duplicate rows not covered by RowSetEqualityWitness_N is N^{z+o(1)}.
- Held-fixed controls: Generator overhead is fixed at N^{rho+o(1)} and row formulas have N^{o(1)} description size., The proof system remains Psys_sym^QEeq with sealed exits and prefix-visible dominator certificates., The target is the same nonuniform SIZE model used by LB_N(1+epsilon), with no advice-selected hard row., All visible first-owner rows are expanded in the same SAT-row theory before first external use.
- Expected observation: If uncovered rows are uncharged, the first one yields a private-row falsifier. If they are sum-charged, the ledger gains N^{1+z+o(1)}; for z<epsilon this still gives a subthreshold upper-bound refutation of LB_N, while for z>=epsilon the proof is no longer a low-cost transcript. No semantic dedup path remains free.
- Transfer certificate needed: A zero-latency syntactic RowSetEqualityWitness_N or RealSATInfluenceRealizer_N that lists every influential row or equality class before first use and pays W_eq plus row expansion in Gamma_QEeq.

## Next Experiment

Instantiate Psys_sym^QEeq on one projected-dDNNF FormulaEval block pair: write the equality-witness bit fields, run the union-find first-owner ledger, compute Gamma_QEeq, and exhibit the unread-enable-bit countermodel when a projected duplicate row lacks a prefix-visible witness.
