# cycle-0139

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Safe quotient CTSR normal form: for a Psys_sym^{CTSR,eq} certificate pi over the beta-zero parity carrier, the least valid transparent support object is the reachable counterfactual frontier quotiented only by surfaced same-theory EqSAT certificates. The line induction gives a same-model circuit upper bound C(H_N^{SAT}) <= N^{rho+o(1)}+Gamma_CTSR^=(pi)+O(E_pi N). Hence any subthreshold certificate is a falsifier for LB_N(1+epsilon), while any omitted child or uncertified quotient has a private-row countermodel.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, polylog query length L_N=(log N)^d, and generator size N^{rho+o(1)}.
- target object: the same-model nonuniform SIZE lower-bound assertion LB_N(1+epsilon) for H_N^SAT and its parser-to-circuit refutation when a certificate transcript is subthreshold.
- controlled interface: Psys_sym^{CTSR,eq} proof lines are parsed into a charged row-support transcript K_CTSR^=(pi), Gamma_CTSR^=(pi), and an induced H_N circuit.
- target-preserving condition: beta=0 target SAT queries, no hidden row advice, same-theory EqSAT quotient certificates, and line-by-line occurrence expansion preserve the SIZE model and threshold.
- row key: a verifier-visible tuple (slot j, formula handle h, restriction path sigma, child bit b, parent line p, rule tag r) naming one SAT row used by a FormulaEval or counterfactual TSR rule.
- safe quotient: two row keys are identified only when pi contains a bit-explicit EqSAT certificate whose row expansion is already charged before the merged key is used.
- reachable counterfactual frontier: the least fixed point starting at the final LB_N line and closing under parent pointers, FormulaEval support, EqSAT dependencies, and all children of every reachable adaptive TSR query, not merely the actual branch.

## Assumptions

- model_context: nonuniform Boolean circuits SIZE; proof system Psys_bEF plus extensional FormulaEval, EqSAT, and counterfactual declared bounded TSR; the reduction is a parser simulation, not a black-box Turing reduction.
- quantifier_context: fix epsilon>0 and constants q,rho,kappa,theta; N ranges over valid carrier lengths; all o(1) terms are uniform over the proof family pi_N.
- uniformity/advice: G_N, bit-field decoders, row enumerators, and EqSAT checkers have explicit polylog-uniform descriptions; nonuniformity is only ordinary circuit advice and the explicit proof string pi_N.
- same-theory quotient condition: quotient certificates must be derivable in the same row theory used by the parser, so no SAT-truth table advice or hidden semantic row selection may enter.
- barrier_status: the positive theorem is relativizing over surfaced row labels; EqSAT links are nonrelativizing only when explicitly certified; the lemma is not a natural-proofs escape and does not prove H_N lower bounds.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)}`. Valid when: Valid when N ranges over the carrier lengths, M_N=N^{q+o(1)}, and G_N is the fixed advice-free generator used by the beta-zero parity route.
- safe_frontier_fixed_point: `K_{0}=Rows(final),\quad K_{t+1}=K_t\cup Parents(K_t)\cup FE(K_t)\cup CTSR_{all}(K_t)\cup EqSAT(K_t)\;/\equiv_{cert}`. Valid when: Valid when every rule line exposes parent pointers and every quotient edge has a bit-explicit EqSAT certificate charged before use.
- ctsr_gamma: `\Gamma_{CTSR}^{=}(\pi)=\Gamma_{bEF}(\pi)+U_{enum}(K^{=})+N\,|K^{=}_{CTSR}(\pi)|+B_{SR_h}(\pi)+B_{EqSAT}(\pi)`. Valid when: Valid when K^{=}_{CTSR}(pi) is the stabilized safe quotient frontier and row expansion costs N^{1+o(1)} per distinct charged row key.
- parser_upper_bound: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{CTSR}^{=}(\pi)+O(E_\pi N)`. Valid when: Applies after the line induction parses every proof line into a same-theory circuit transcript and E_pi exceptional source rows are patched by equality gates.
- subthreshold_falsifier: `\rho<1+\epsilon,\quad |K^{=}_{CTSR}|<N^{\epsilon-o(1)},\quad E_\pi<N^{\epsilon-o(1)}\Rightarrow C(H_N^{SAT})<N^{1+\epsilon-o(1)}`. Valid when: Requires beta-zero target queries, charged EqSAT quotienting, and no hidden FormulaEval or TSR influence outside the stabilized support frontier.

## Attempted Derivation

- Bit fields fixed for each relevant line: rule tag, line id, parent ids, slot j, formula handle h, restriction path sigma, branch bit b, enable bit e, frontier flag, EqSAT certificate pointer, and row-expansion handle.
- Define K_CTSR^=(pi) by a least fixed point from the final LB_N line. Closure adds syntactic parents, FormulaEval row sets, EqSAT dependency rows, and both counterfactual children of every reachable TSR node. Quotienting is delayed until a charged EqSAT certificate edge is encountered.
- Verifier audit: enumerate stabilized keys by BFS over the exposed proof DAG; charge U_enum for enumeration, B_EqSAT for certificate verification, and N^{1+o(1)} for expanding each distinct quotient row into the occurrence-level parser.
- Line induction: bEF and SATeq lines use the existing Gamma_bEF invariant; FormulaEval lines read only keys already in K^=; CTSR lines are sound because all reachable children, including unchosen branches, are present; EqSAT lines justify only the certified quotient edges.
- Circuit extraction: replace every parsed row occurrence by the generated SAT subcircuit when available or by the transcript subcircuit charged in Gamma_CTSR^=; patch E_pi exceptional source rows with equality gates, giving C(H_N)<=N^{rho+o(1)}+Gamma_CTSR^=+O(E_pi N).
- Contrapositive: if this upper bound is below N^{1+epsilon-o(1)}, the alleged LB_N(1+epsilon) certificate is invalid in the same nonuniform SIZE model; this is a route-level falsifier, not a proof that H_N is easy unconditionally.
- Necessity test: remove one reachable child or merge two uncertified keys. Choose the first unsafe use, keep all visible fields fixed, and flip the private row label behind the omitted child or quotient collision. The transcript agrees but the induced premise or final parity differs.

Blocking gap: RealSATInfluenceRealizer_N^{arb} remains open for fully semantic adaptive pruning that never exposes counterfactual children or EqSAT certificate edges yet may be sound for real SAT instances.

## Falsifiers

- First-hidden-child adaptive pruning falsifier: an unlisted counterfactual CTSR child changes the induced row label while the visible transcript is unchanged.
- Uncertified quotient-collision falsifier: two syntactically merged child keys can be independently flipped unless a same-theory EqSAT certificate is charged.
- Unread-enable-bit falsifier: a FormulaEval row selected by a hidden enable bit influences a later line without entering K_CTSR^=(pi).
- q<epsilon full-scan enumeration falsifier: if the whole visible slot universe has size N^{q+o(1)} with q<epsilon, expanding all rows is already subthreshold.
- Positive-beta transfer-cap falsifier retained from the atlas: any return to black-box target queries of length n^beta faces the upper-bound window q+beta c+o(1).
- Nonuniform row-selector advice falsifier: a short proof that names a support set only through semantic advice is outside TransparentRowSupport_N and cannot be promoted.

## Learning

Cycle 139 improves the CTSR frontier packet by adding a safe EqSAT quotient rule: duplicate counterfactual child rows reduce Gamma only when a same-theory certificate is surfaced and charged. Otherwise quotienting is exactly where the private-row falsifier attacks. This is a valid scoped parser/countermodel contribution and still not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the safe-quotient CTSR theorem, not as a broad new carrier search.`
- Rationale: The branch has a promoted transparent-support packet; the remaining risk is not another abstract barrier but whether duplicate counterfactual child rows may be safely quotient-charged without hidden semantic advice.
- Situation seed: Consider H_N^{SAT} with M_N=N^q polylog SAT instances where a counterfactual TSR proof tree has N^kappa reachable roots and N^theta child branches per root; half the branches syntactically collide after Tseitin rewriting, but only a chosen fraction have explicit EqSAT certificates.
- Varied variable: The collision-certification fraction alpha: alpha=0 means syntactic or semantic collision with no certificate, alpha=1 means every duplicate child has a charged same-theory EqSAT link.
- Held-fixed controls: beta=0 polylog target-query length and fixed generator overhead N^{rho+o(1)}, same nonuniform SIZE source and target circuit model, counterfactual rather than actual-branch TSR closure, no SAT-truth-table advice and no hidden row-selector advice, fixed epsilon,q,kappa,theta threshold regime
- Expected observation: For alpha=1 the charged support size drops to the certified quotient frontier and Gamma_CTSR^= remains valid; for alpha<1 the first uncertified collision gives a two-world private-row falsifier, so the charge cannot be reduced by semantic intuition alone.
- Transfer certificate needed: A formal same-theory EqSAT certificate parser with row expansion and verifier-visible dependency edges; without it, the quotient intuition cannot enter the proof obligations or the live inference-quality packet.

## Next Experiment

Instantiate Gamma_CTSR^= on a projected-dDNNF FormulaEval proof with two Tseitin-equivalent child formulas: compute K before and after certified EqSAT quotienting, then remove one certificate and exhibit the first uncertified quotient-collision private-row falsifier.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

TerminalEdgeCompleteSupport_N theorem: for Psys_sym^tec proofs whose terminal-relevant FormulaEval dependencies are proof-visible and edge-complete, the least terminal reverse cone K_tec(pi) yields a same-model Gamma_tec parser upper bound; hence any sound proof of LB_N(1+epsilon) for H_N^SAT must pay N^{1+epsilon-o(1)} circuit-size-equivalent charge when rho<1+epsilon.

## Definitions

- source object: an accepted Psys_sym^tec proof pi of LB_N(1+epsilon) asserting C_SIZE(H_N^SAT)>N^{1+epsilon}, where H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), N=2^n, M_N=N^{q+o(1)}, and size(G_N)=N^{rho+o(1)}.
- target object: a nonuniform Boolean SIZE upper-bound circuit for H_N^SAT, or equivalently a contradiction to the same-model LB_N(1+epsilon) proof if the parsed charge is subthreshold.
- controlled interface: terminal-edge-complete transparent FormulaEval, with visible selector code, visible dependency-edge certificates, row enumeration or row-cover certificates, same-theory bEF prefix splicing, and no hidden advice.
- target-preserving condition: every terminal-relevant semantic influence edge used by FormulaEval is listed before use, charged in Gamma_tec, and expandable into the same proof theory without SAT-truth-table advice.

## Assumptions

- Model: nonuniform Boolean circuits over the N-bit x input, with proof objects in bEF plus transparent FormulaEval; the reduction is extraction/prefix-splicing, not many-one SAT reduction.
- Regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, visible selector or witness enumeration exponent alpha when present, bounded-SR_h width h=N^{eta+o(1)}, and generator overhead rho<1+epsilon.
- Uniformity/advice: K_tec(pi) is computed deterministically from N and pi; no row selector, edge list, or influence witness may depend on hidden SAT truth advice.
- Same-theory condition: each charged FormulaEval edge has a bEF row expansion using fresh extension variables scoped before the line that consumes it.
- Soundness condition: LB_N(1+epsilon) and the derived upper bound are both interpreted in the same nonuniform SIZE model for H_N^SAT.

## Equations

- terminal_reverse_closure: `K_0=\{\ell_{\mathrm{fin}}\},\quad K_{s+1}=K_s\cup \mathrm{Parents}(K_s)\cup \mathrm{FERows}_{\mathrm{edge}}(K_s),\quad K_{\mathrm{tec}}(\pi)=\bigcup_{s\le |\pi|}K_s`. Valid when: Valid when proof-line parents and FormulaEval influence edges are syntactically visible and finite.
- charge_ledger: `\Gamma_{\mathrm{tec}}(\pi)=\Gamma_{\mathrm{bEF}}(K_{\mathrm{tec}})+U_{\mathrm{enum}}(K_{\mathrm{tec}})+X_{\mathrm{row}}(K_{\mathrm{tec}})`. Valid when: Valid when enumeration, row expansion, and bEF charges are measured in common circuit-size units.
- parser_upper_bound: `C_{\mathrm{SIZE}}(H_N^{\mathrm{SAT}})\le N^{\rho+o(1)}+\Gamma_{\mathrm{tec}}(\pi)`. Valid when: Applies after every terminal-relevant FormulaEval edge is same-theory expanded and charged.
- subthreshold_falsifier: `\rho<1+\epsilon\ \wedge\ \Gamma_{\mathrm{tec}}(\pi)<N^{1+\epsilon-o(1)}\ \Longrightarrow\ \pi\ \text{is not a sound proof of }LB_N(1+\epsilon)`. Valid when: Valid when the source proof statement and target circuit upper bound use the same SIZE model.
- forced_charge: `\pi\ \text{sound}\ \wedge\ \rho<1+\epsilon\ \Longrightarrow\ \Gamma_{\mathrm{tec}}(\pi)\ge N^{1+\epsilon-o(1)}`. Valid when: Requires the parser upper bound and the claimed lower bound to be mutually comparable.
- row_density_corollary: `|K_{\mathrm{rows}}|\ge N^{\epsilon-o(1)},\qquad |K_{\mathrm{rows}}|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Valid when non-row debts are lower order and each charged row costs O(N).

## Attempted Derivation

- Define Psys_sym^tec as bEF plus FormulaEval lines whose terminal-relevant dependencies are carried by visible edge certificates; the source_statement is an accepted pi proving LB_N(1+epsilon) for H_N^SAT.
- Run C_tec from the final LB line: add ordinary parent pointers, then for each reachable FormulaEval line add exactly the certified influencing rows and their row-expansion obligations; this computes the least terminal reverse cone K_tec(pi).
- Prove minimality by monotonicity: any prefix-closed transparent support containing the final line and satisfying the checked edge clauses must contain every stage K_s of the worklist, hence contains K_tec.
- Perform line induction in topological order on K_tec: bEF lines use the existing bit-explicit parser; FormulaEval lines are replaced by the charged row-expanded bEF material; fresh extension variables are scoped before the consuming line.
- Derive the target_statement: the expanded transcript plus G_N yields a nonuniform SIZE circuit for H_N^SAT of size at most N^{rho+o(1)}+Gamma_tec(pi).
- If this size is below N^{1+epsilon-o(1)}, the claimed LB_N(1+epsilon) is falsified in the same model; if pi is sound and rho<1+epsilon, Gamma_tec(pi) must be at least N^{1+epsilon-o(1)}.
- For the no-go branch, choose the first terminal-relevant semantic edge omitted by C_tec, toggle its private row while holding the visible transcript fixed, and obtain the unread-enable-bit falsifier to occurrence-only parsing.
- Live pvsnp_inference_quality packet: source_statement=accepted Psys_sym^tec proof pi of LB_N(1+epsilon) for H_N^SAT; target_statement=Gamma_tec same-model upper-bound falsifier or forced row-equivalent support; model_context=nonuniform Boolean SIZE, beta-zero SAT-parity carrier, bEF plus terminal-edge-complete transparent FormulaEval, extraction and prefix splicing rather than many-one reduction; quantifier_context=N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, h=N^{eta+o(1)}, visible enumeration exponent alpha when used, size(G_N)=N^{rho+o(1)}, rho<1+epsilon, deterministic no-advice checker; derivation_status=restricted theorem packet derived, arbitrary semantic FormulaEval blocked at RealSATInfluenceRealizer_N and AC0 output-sensitive row-cover validation; reviewer_findings=valid only with visible terminal influence, same-theory expansion, no hidden advice, and no claim toward P != NP.

Blocking gap: The proof does not cover arbitrary semantic FormulaEval rules whose influence relation is not proof-visible or locally coverable; the named gap is RealSATInfluenceRealizer_N, with AC0 output-sensitive row-cover certification as a concrete subgap.

## Falsifiers

- First omitted terminal edge: a hidden feasible row changes a reachable FormulaEval truth value while all charged rows and syntax remain fixed.
- Unread-enable-bit FormulaEval: the selector surface is unchanged, but a private enable bit chooses an unlisted row influencing the final line.
- Dead-line padding falsifier for full-proof support: adding N^B irrelevant FormulaEval lines changes full support but leaves K_tec and the valid Gamma charge unchanged.
- q<epsilon source-ceiling falsifier: if M_N=N^{q+o(1)} with q<epsilon and other debts are subthreshold, the generated carrier itself has a same-model upper bound below LB_N(1+epsilon).
- Semantic SAT-advice selector: a row-cover certificate that needs SAT truth-table advice is not a valid transparent interface and is quarantined at RealSATInfluenceRealizer_N.

## Learning

Cycle 139 upgrades the edge-complete support idea into an auditable theorem packet: the least terminal reverse cone K_tec is computed by a finite checker, is invariant under dead padding, derives Gamma_tec by line induction, and has a first-omitted-edge falsifier. This is valid route-level proof-system certification, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and validation check for L139.1-L139.3.`
- Rationale: The branch has a theorem-shaped transparent-support claim; a concrete thought experiment tests whether terminal-edge completeness is the right invariant rather than another restatement of semantic FormulaEval barriers.
- Situation seed: Construct a Psys_sym proof of a beta-zero SAT-parity LB_N statement with a long block D of padded FormulaEval lines, one terminal chain using an unread-enable-bit row r*, and otherwise visible bounded-SR_h row covers.
- Varied variable: dead-padding exponent delta, where |D|=N^{delta}, while the hidden terminal row r* is either disconnected or connected to the final LB line.
- Held-fixed controls: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)} and fixed q., Generator overhead rho<1+epsilon and the same nonuniform SIZE target model., Deterministic no-advice C_tec checker and same-theory bEF prefix splicing for all visible rows., One omitted row r* with a private unread-enable bit when testing the negative branch.
- Expected observation: When r* is disconnected, K_tec and Gamma_tec remain invariant as delta grows, refuting full-proof support. When r* lies on a terminal dependency path, two visible-identical transcripts differ semantically, giving the finite omitted-edge falsifier.
- Transfer certificate needed: A formal edge-completeness certificate proving that every terminal-relevant FormulaEval influence is either listed and charged or is impossible by a locally checkable row-cover argument.

## Next Experiment

Instantiate C_tec on one projected-dDNNF FormulaEval rule with a visible row-cover certificate; compute U_enum, X_row, and Gamma_tec, then remove the first cover edge to demonstrate the private-row falsifier.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For Psys_sym^QEeq restricted to canonical cell-decomposable FormulaEval producers, prefix-visible RowSetEqualityWitness_N certificates are sound and complete for equality compression of row support. Uncovered overlap is sum-charged, and uncharged uncovered influence yields a private-row falsifier.

## Definitions

- source object: a Psys_sym^QEeq proof pi for beta-zero H_N^SAT, with FormulaEval lines whose row selectors output sorted disjoint canonical cells C=(mask,value,projection,row-formula-template) and timestamps.
- target object: same-theory nonuniform SIZE simulation of H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) and the LB_N(1+epsilon) transcript falsifier.
- controlled interface: prefix-visible RowSetEqualityWitness_N bit grammar giving first-owner id, duplicate producer id, cell ids, row-index equation, canonical cell hash, and dominator-exit timestamp before first use.
- target-preserving condition: every charged or shared row expands to the same SAT occurrence formula used by the proof, all enumeration is advice-free from N and the proof prefix, and hidden semantic equality is disallowed.
- Canonical cell-decomposable means each producer has a verifier-visible finite list of pairwise disjoint cells whose union is the selected row set and whose row-index maps are syntactically comparable.
- Covered row means a duplicate row lies in a cell pair certified by identical canonical signatures or by an explicit refinement whose children have identical canonical signatures.

## Assumptions

- Circuit target is nonuniform SIZE over the same row formulas G_N used in the proof; the result is not a P != NP lower bound.
- Length regime: N tends to infinity, M_N=N^{q+o(1)}, formula length is N^{o(1)}, generator cost is N^{rho+o(1)}, and all proof-prefix verifiers run in N^{o(1)} per listed cell bit.
- Uniformity/advice regime: row-set producers, equality witnesses, and dominator timestamps are determined by N and pi_{<t}; no hard row, SAT-truth advice, or semantic selector is allowed.
- Timing regime: equality sharing is valid only if the witness is present before the first external dependency using the shared support, or inside a sealed QE block whose exit dominates all uses.
- Naturalness/barrier status: the object is a sparse proof-transcript parser, not a large useful property; the obstruction is semantic deduplication without syntax, not generic natural-proofs folklore.

## Equations

- Gamma_QEeq_ledger: `\Gamma_{QEeq}(\pi)=\Gamma_{bEF}(\pi)+U_{own}+X_{own}+W_{eq}+X_{uncov}`. Valid when: Valid when FormulaEval support is discovered by canonical cells, equality compression has prefix-visible witnesses, and uncovered rows are sum-charged.
- first_owner_support: `K^{eq}_{idx}=K^{own}_{idx}\cup K^{covered}_{dup},\quad K^{uncharged}_{dup}=\emptyset`. Valid when: Applies when every duplicate row is either assigned a first owner or covered by a checked RowSetEqualityWitness_N certificate.
- same_model_upper_bound: `SIZE(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{QEeq}(\pi)+O(E_{\pi}N)`. Valid when: Requires the target-preserving same-theory expansion, the bEF parser induction, and advice-free enumeration of all charged support rows.
- low_cost_transcript_falsifier: `N^{\rho+o(1)}+\Gamma_{QEeq}(\pi)+O(E_{\pi}N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Applies after the transcript simulation stays in the intended nonuniform SIZE model and the claimed lower-bound threshold is N^{1+epsilon-o(1)}.
- support_density_corollary: `\text{not falsified}\Rightarrow |K^{eq}_{idx}|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Valid when row expansion costs N^{1+o(1)} per owned row and all lower-order parser, equality, and generator terms are subthreshold.

## Attempted Derivation

- Fix the final LB_N line and compute the least time-stamped support cone K_time^eq by backward reachability through parent pointers, FormulaEval dependencies, QE exits, and equality-witness references.
- For each FormulaEval producer a, require a prefix-visible canonical decomposition D_a=(C_{a,1},...,C_{a,s}) of disjoint row cells; its verifier checks sortedness, cell disjointness, row-index map syntax, and row-formula-template identity.
- Assign first-owner status to the earliest reachable producer-cell occurrence. A later producer-cell may share cost only by citing RowSetEqualityWitness_N(a,c,b,d) whose bit fields include owner id, duplicate id, cell ids, refinement children if needed, canonical signatures, and a dominator timestamp before first external use.
- Define Gamma_QEeq as Gamma_bEF plus owner enumeration cost, owner row-expansion cost, equality-witness checking cost, and uncovered duplicate expansion. This prevents semantic equality from reducing K_idx unless the equality is syntactically witnessed.
- Induct on proof lines: bEF rules use the archived Gap98 ledger; transparent FormulaEval adds its visible row support; QE blocks may delay internal support only until a dominating exit; equality-sharing rules either consume a checked witness or trigger sum charge.
- Build the same-theory nonuniform circuit for H_N^SAT by hardwiring the generator, charged row expansions, and parsed transcript. If its size is below N^{1+epsilon-o(1)}, the transcript is a valid falsifier to LB_N(1+epsilon) in the intended model.
- For the negative side, choose the first line with hidden uncharged semantic influence. Complete all read occurrence bits identically in two transcripts, flip the unread enable/private-row bit, and obtain the same proof prefix but a different FormulaEval value.

Blocking gap: Completeness is proved only for canonical cell-decomposable producers. General semantic AC0 membership selectors, SAT-truth-pruned dDNNF projections, and unwitnessed formula extensionality remain blocked at RealSATInfluenceRealizer_N or must pay full scan/sum charge.

## Falsifiers

- falsifier: an equality witness whose timestamp occurs after the first external dependency invalidates compression and forces sum charge or private-row separation.
- falsifier: a projected-dDNNF selector with an unread enable bit controlling a projected row creates two completions with identical visible transcript but different FormulaEval value.
- falsifier: semantic equality of SAT formulas without a quotient witness is not valid sharing; it is either charged as duplicate support or quarantined as RealSATInfluenceRealizer_N failure.
- falsifier: a membership-only AC0 row selector lacking output-sensitive enumeration pays full scan charge N^{1+q+o(1)} and cannot support a subthreshold transcript claim.
- falsifier: any row-hardness or equality-compression certificate using advice-selected hard rows violates the target-preserving uniformity condition for the same-model SIZE consequence.

## Learning

Cycle 139 improves validation rather than rediscovering the route: equality compression is valid exactly when canonical cell equality is witnessed before use. The new proof-auditable invariant is first-owner support plus prefix-visible cell-refinement coverage; semantic deduplication without that witness is a finite private-row falsifier. This is paper-level parser progress only, not progress on the main P vs NP conjecture.

## Gedanken Experiment Design Seed

- Need decision: `use-now-as-falsifier-probe`
- Rationale: The branch needs to test the exact timing and equality-witness clauses of QEeq compression, not add another selector class or MCSP slogan.
- Situation seed: Take two projected-dDNNF FormulaEval producers A and B for H_N^SAT. They have the same projected row set on paper, but B contains a hidden auxiliary witness fiber with an unread enable bit that controls one row j*.
- Varied variable: coverage fraction lambda of rows whose equality to the first owner is certified by prefix-visible RowSetEqualityWitness_N records before first use.
- Held-fixed controls: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)} and fixed generator overhead N^{rho+o(1)}., Same Psys_sym^QEeq proof syntax, bEF parser costs, and nonuniform SIZE target model., No SAT-truth advice, no hard-row advice, and no post-hoc equality witnesses after first external dependency.
- Expected observation: For lambda=1 the compression charge is valid and Gamma_QEeq counts each row once plus witness overhead. For lambda<1, flipping the unread enable bit on an uncovered influential row gives a private-row falsifier unless that row is sum-charged.
- Transfer certificate needed: A prefix-visible canonical cell refinement plus dominator-timing certificate proving that every shared row is syntactically covered before use; otherwise the thought experiment remains only a countermodel probe.

## Next Experiment

Write the referee-level RowSetEqualityWitness_N bit-field table for one projected-dDNNF producer pair, compute U_own, X_own, W_eq, and X_uncov, then instantiate the unread-enable-bit countermodel when one duplicate cell lacks prefix-visible coverage.
