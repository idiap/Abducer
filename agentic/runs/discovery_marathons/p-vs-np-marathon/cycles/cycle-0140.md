# cycle-0140

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: QCTSR Certified-Quotient Parser Boundary

## Candidate Lemma

For the beta-zero parity carrier H_N^SAT, any Psys_sym^{QCTSR} proof pi satisfying bit-explicit bEF parsing, TransparentRowSupport_N, reachable counterfactual TSR frontier closure, and surfaced same-theory EqSAT quotient certificates has a same-model circuit upper bound charged by Gamma_QCTSR(pi). Hence a subthreshold Gamma_QCTSR(pi) is a valid falsifier for LB_N(1+epsilon); quotienting without surfaced certificates is not a valid compression step.

## Definitions

- source object: LB_N(1+epsilon) is the assertion that H_N^SAT has nonuniform Boolean circuit size greater than N^{1+epsilon-o(1)} on valid source lengths.
- target object: the target is a scoped parser-to-circuit falsifier theorem for Psys_sym^{QCTSR}, not a proof of P != NP or of H_N lower bounds.
- controlled interface: the proof transcript pi exposes bit-explicit bEF dependencies, visible FormulaEval row support, all reachable counterfactual TSR children, and a same-theory EqSAT certificate forest for every quotient merge.
- target-preserving condition: beta=0, SAT query length L_N=(log N)^d, M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)}, advice-free row enumeration, and all charges remain in the same nonuniform SIZE model.
- Row universe R_N consists of pairs (j,a) naming a generated formula position and a local assignment/restriction row used by FormulaEval, SR_h, TSR, or EqSAT quotient reasoning.
- K_Q(pi) is the least fixed point of visible dependencies, reachable counterfactual TSR children, and dependencies of quotient certificates, after replacing certified duplicate rows by charged representatives.
- RepIdx(K_Q) is the set of charged representative occurrence rows after safe quotienting; suppressed rows are legal only if linked to a representative by a surfaced same-theory EqSAT proof forest.

## Assumptions

- Circuit model is nonuniform Boolean SIZE; the only nonuniform information allowed is the written proof transcript and fixed generator description, not hidden row-selection advice.
- The generator G_N has circuit size N^{rho+o(1)} and produces M_N=N^{q+o(1)} SAT instances of polylogarithmic length, so beta=0 in the target-circuit substitution term.
- Every FormulaEval or CTSR line gives either an advice-free enumerator for its influenced rows or pays the full row-scan expansion charge in the ledger.
- Every adaptive TSR node declares all reachable counterfactual children before branch pruning; actual-branch-only declarations are excluded from the positive theorem.
- Each quotient edge r -> s carries a same-theory EqSAT certificate proving SAT(G_r)=SAT(G_s), and all certificate dependencies are inserted into K_Q before the quotient is used.
- All o(1) losses are uniform over the valid length sequence and do not depend on hidden semantic advice.

## Equations

- carrier: `H_N(x)=\bigoplus_{j<M_N} SAT(G_N(x,j)),\qquad M_N=N^{q+o(1)},\quad |G_N(x,j)|=(\log N)^d`. Valid when: Valid when H_N is the beta-zero generated parity carrier with polylogarithmic SAT instances and explicit generator G_N.
- safe_quotient_closure: `K_Q(\pi)=\mu K\,[Final(\pi)\cup Par(K)\cup CTSR_{cf}(Rep(K))\cup EqCertDep(K)]`. Valid when: Applies when proof syntax exposes parent pointers, counterfactual TSR children, representatives, and dependencies of every quotient certificate.
- ledger: `\Gamma_{QCTSR}(\pi)=\Gamma_{bEF}(\pi)+U(K_Q)+N\cdot |RepIdx(K_Q)|+C_{Eq}(K_Q)+O(E_\pi N)`. Valid when: Requires the transparent parser ledger to charge enumeration, row expansion, EqSAT proof forests, and sparse residual patching.
- parser_upper_bound: `C(H_N)\le N^{\rho+o(1)}+\Gamma_{QCTSR}(\pi)`. Valid when: Applies after the line induction replaces every proof use by charged rows in the same nonuniform SIZE model.
- subthreshold_falsifier: `\rho<1+\epsilon,\ \Gamma_{QCTSR}(\pi)<N^{1+\epsilon-o(1)}\ \Longrightarrow\ \neg LB_N(1+\epsilon)`. Valid when: Valid when LB_N is a same-model circuit lower-bound claim for H_N on the same valid length sequence.

## Attempted Derivation

- Define the visible row universe R_N and initialize K with the final LB_N line, final carrier rows, and explicit bEF dependencies.
- Run the least fixed point: add parent rows of every reachable FormulaEval line, add every counterfactual TSR child of each reachable representative, and add all dependencies of each EqSAT quotient certificate before allowing its merge.
- Use union-find only after certificate insertion: a suppressed row r may be replaced by representative s in the parser iff the certificate forest contains a path proving same-theory SAT equivalence between r and s.
- Line induction cases: bEF lines charge Gamma_bEF; transparent FormulaEval lines charge U(K_Q)+N|RepIdx|; CTSR lines charge all reachable counterfactual children; quotient lines charge C_Eq and then reuse the representative row.
- Construct the H_N circuit by wiring G_N, the charged row evaluators/transcripts, representative occurrence expansions, EqSAT certificate checkers if needed, and O(E_pi N) equality patches for sparse residual rows.
- Derive C(H_N)<=N^{rho+o(1)}+Gamma_QCTSR(pi). If this is below N^{1+epsilon-o(1)}, the asserted LB_N(1+epsilon) is falsified in the same nonuniform model.
- For necessity, choose the first reachable quotient merge or child-pruning step absent from K_Q. Two private-row worlds agree on all charged data and the proof transcript but flip the hidden row's parity contribution, contradicting extensional parser soundness.

Blocking gap: The derivation does not handle arbitrary real-SAT semantic pruning. It requires either surfaced same-theory EqSAT certificates or a future RealSATInfluenceRealizer_N^{arb} that uniformly lists and charges all semantic influences before use.

## Falsifiers

- Uncertified quotient merge: a suppressed row influences the final parity but has no surfaced same-theory certificate to a representative.
- First-hidden-child adaptive pruning: a reachable counterfactual TSR child is omitted because only the actual branch was declared.
- Unread-enable-bit FormulaEval: selector output hides a row whose later symbolic use reaches the final line.
- Positive beta target queries: black-box substitution gives q+beta*c+o(1) and cannot exclude all SAT circuit exponents.
- Nonuniform leakage: representative choices or row sets are supplied as semantic advice instead of proof-visible enumeration.
- Certificate-charge collapse: C_Eq(K_Q) itself is N^{1+epsilon-o(1)} or larger, so the parser theorem remains valid but gives no subthreshold falsifier.

## Learning

Cycle 140 turns safe EqSAT quotienting from a slogan into a ledger transformation: duplicate counterfactual CTSR rows may be removed only through a surfaced same-theory certificate forest whose dependencies are in K_Q. The exact new falsifier is the first uncertified quotient merge. This strengthens the scoped parser/countermodel contribution and remains separate from proving any lower bound or P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the safe-quotient CTSR boundary.`
- Rationale: The remaining issue is not another abstract support slogan; quotient compression can make or break the Gamma ledger, so a concrete row-merge stress test checks whether the parser is target-preserving.
- Situation seed: A beta-zero H_N^SAT parity carrier whose Psys_sym proof uses counterfactual TSR on Tseitin-encoded SAT instances and then quotient-merges many restriction children claimed EqSAT-equivalent.
- Varied variable: The quotient collision exponent mu, where |RepIdx(K_Q)|=N^{mu+o(1)}, while the unquotiented reachable frontier has exponent kappa+theta.
- Held-fixed controls: SAT query length is L_N=(log N)^d, so beta=0 and target substitution contributes only N^{rho+o(1)}., M_N=N^{q+o(1)} parity slots and the same nonuniform SIZE model are held fixed., Every TSR node has bounded depth h and all counterfactual children are syntactically reachable before pruning., No hidden row advice is allowed; EqSAT quotient edges must be written as same-theory certificates.
- Expected observation: Certified quotienting lowers row expansion from N^{1+kappa+theta+o(1)} to N^{1+mu+o(1)} plus C_Eq; any uncertified saving produces a two-world private-row falsifier at the first hidden merge.
- Transfer certificate needed: A uniform same-theory EqSAT certificate forest plus the K_Q fixed-point audit, showing every suppressed child is influence-closed and charged before the proof uses the quotient.

## Next Experiment

Instantiate K_Q on a toy projected-dDNNF FormulaEval proof with two CTSR levels and three EqSAT quotient classes; compute |RepIdx|, C_Eq, Gamma_QCTSR, then delete one quotient certificate to exhibit the first-hidden-merge falsifier.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Terminal-edge-complete TransparentRowSupport admits a line-order-preserving same-theory expansion. For any accepted Psys_sym^TEC proof pi of LB_N(1+epsilon) for H_N^SAT, the finite K_tec checker and fresh namespaces construct a Psys_bEF^- expansion with charge Gamma_tec(pi). If the resulting same-slice circuit size is below N^{1+epsilon-o(1)}, the proof line is falsified in its own target model.

## Definitions

- source object: a Psys_sym^TEC proof pi whose final line asserts LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), with N=2^n, M_N=N^{q+o(1)}, and |pi|=N^{tau+o(1)}.
- target object: a same-slice nonuniform Boolean SIZE circuit for H_N^SAT of size below N^{1+epsilon-o(1)}, used as a falsifier to the asserted lower-bound line.
- controlled interface: terminal-edge-complete TransparentRowSupport_N with visible selector code, row-set certificates, dependency-edge certificates, same-theory row expansion, fresh extension namespaces, and no hidden advice.
- target-preserving condition: every terminal-relevant FormulaEval influence edge and every row used by its expansion is computable from (N,pi) before the semantic rule is invoked, so the expansion is a simulation rather than a many-one reduction.
- K_tec(pi) is the least reverse-reachable cone from the final LB_N line closed under visible proof predecessors and visible FormulaEval row-support edges.
- U_tec is the bit cost of enumerating certified row sets and witness lists; X_tec is the same-theory row-expansion cost; alpha is the exponent of visible existential row witnesses.

## Assumptions

- Circuit target is nonuniform Boolean SIZE on the N-bit truth-table slice; LB_N(1+epsilon) means no circuit of size N^{1+epsilon-o(1)} computes H_N^SAT on that slice.
- The proof system is bEF plus FormulaEval rules satisfying TEC certificates; each semantic dependency used by a terminal-relevant line has a visible earlier-line or row-support edge.
- The parser is deterministic, uniform in N and pi, and uses no SAT-truth advice, no hidden selector advice, and no oracle answers beyond the displayed row expansions.
- Fresh extension variables are namespaced by (line,row,local-index), preventing capture when row-expansion blocks are prefix-spliced before their first terminal-relevant use.
- The generator G_N has nonuniform size N^{rho+o(1)} with rho<1+epsilon; bounded-SR_h neighborhoods have h=N^{eta+o(1)}; visible existential witnesses, if present, have exponent alpha.

## Equations

- TEC fixed point: `K_0={\ell_*},\quad K_{t+1}=K_t\cup Pred_{vis}(K_t)\cup RowSupp_{vis}(K_t),\quad K_{tec}=\bigcup_t K_t.`. Valid when: Valid when pi supplies checkable predecessor and row-support certificates for every terminal-relevant FormulaEval line.
- TEC charge ledger: `\Gamma_{tec}(\pi)=\Gamma_{bEF}(K_{tec})+U_{tec}(K_{tec})+X_{tec}(K_{tec})+N^{\tau+\alpha+\eta+o(1)}.`. Valid when: Applies after visible existential witnesses are enumerated with exponent alpha and bounded-SR_h neighborhoods have arity h=N^{eta+o(1)}.
- same-model parser falsifier: `N^{\rho+o(1)}+\Gamma_{tec}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon).`. Valid when: Requires the final LB_N line to mean absence of same-slice SIZE circuits below N^{1+epsilon-o(1)} for H_N^SAT.
- support-density corollary: `\Gamma_{bEF}+U_{tec}/N+X_{tec}/N=o(N^{\epsilon})\Rightarrow |K_{idx}(\pi)|/M_N\ge N^{\epsilon-q-o(1)}.`. Valid when: Valid when row-equivalent debt is dominated by visible FormulaEval rows and M_N=N^{q+o(1)} in the beta-zero regime.

## Attempted Derivation

- Compute K_tec(pi) by reverse worklist from the final LB_N line using only visible predecessor edges and FormulaEval row-support certificates.
- Discard lines outside K_tec as terminal-irrelevant; this preserves the final derivation because every retained line has all visible dependencies retained by fixed-point closure.
- For each retained FormulaEval line a, enumerate RowSupp_vis(a); insert, before the first retained use of a, a row-expanded bEF block deriving the same local assertion from the listed rows.
- Namespace each inserted extension variable by (a,row,local-index), so prefix splicing cannot identify variables across unrelated FormulaEval blocks.
- Induct over the topological order of retained lines: bEF lines translate directly; FormulaEval lines are replaced by their certified row-expanded blocks; dependency-edge completeness supplies the induction hypotheses.
- Sum the charges over retained lines to obtain Gamma_tec(pi)=Gamma_bEF+U_tec+X_tec+N^{tau+alpha+eta+o(1)}; dead-line padding outside K_tec contributes zero.
- Compose the generator circuit G_N of size N^{rho+o(1)} with the expanded transcript. If N^{rho+o(1)}+Gamma_tec(pi)<N^{1+epsilon-o(1)}, the result is a same-model circuit falsifying LB_N(1+epsilon).

Blocking gap: The derivation is complete only for terminal-edge-complete transparent FormulaEval. For arbitrary semantic FormulaEval, the unproved bridge is RealSATInfluenceRealizer_N: syntax and N must uniformly determine all terminal-relevant influence rows and same-theory expansions before the semantic rule fires.

## Falsifiers

- first-omitted-terminal-edge falsifier: a hidden row changes the SAT-parity carrier while every visible charged transcript remains fixed
- unread-enable-bit falsifier: selector code hides whether a row is active, so RowSupp_vis is incomplete and Gamma_tec undercounts
- namespace-collision falsifier: row-expanded extension variables are reused across spliced blocks and create unsound identifications
- q<epsilon ceiling falsifier: the carrier already has same-model support below the claimed N^{1+epsilon} lower-bound threshold
- semantic RealSAT oracle falsifier: FormulaEval returns a SAT fact whose influencing rows are not uniformly reconstructible from (N,pi)

## Learning

Cycle 140 closes a proof-delivery hole: K_tec is not merely computable but supports a prefix-scoped same-theory expansion with explicit Gamma_tec charge and fresh-variable hygiene. The valid contribution is a scoped parser/falsifier theorem for terminal-edge-complete transparent FormulaEval. Live pvsnp_inference_quality packet: source_statement=accepted Psys_sym^TEC proof of LB_N(1+epsilon) for H_N^SAT; target_statement=Gamma_tec upper-bound falsifier or forced row-equivalent support; model_context=nonuniform Boolean SIZE, beta-zero SAT-parity carrier, bEF plus TEC FormulaEval, simulation/extraction not many-one reduction; quantifier_context=N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, h=N^{eta+o(1)}, alpha-visible witnesses, rho<1+epsilon, deterministic no-advice parser; derivation_status=restricted theorem derived, arbitrary semantic FormulaEval blocked at RealSATInfluenceRealizer_N; reviewer_findings=valid only under visible influence, same-theory expansion, and no hidden advice, and not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the TEC boundary.`
- Rationale: The branch already has an abstract transparent-support theorem; the remaining question is whether one omitted terminal edge really breaks target preservation or can be repaired by prefix splicing.
- Situation seed: A padded SAT-parity family H_N^SAT with one guarded-dDNNF FormulaEval line feeding the final LB_N line; the guard contains a hidden enable bit for exactly one row r*.
- Varied variable: z, the number of terminal-relevant influence edges omitted from the visible TEC certificate, varied from z=0 to z=1.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and the same nonuniform SIZE target class are fixed., The final assertion remains LB_N(1+epsilon) for the same H_N^SAT slice., All bEF and bounded-SR_h syntax, proof length exponent tau, and neighborhood exponent eta are held fixed., No advice is allowed in the parser; only (N,pi) and visible certificates may be used.
- Expected observation: At z=0, K_tec includes r* and the prefix-splice expansion pays the row charge. At z=1, two private-row completions agree on all visible syntax but flip the parity contribution of r*, giving a concrete falsifier to surface occurrence parsing.
- Transfer certificate needed: A finite TEC certificate proving dependency-edge completeness, row-set extensionality, and same-theory row expansion; without it the intuition cannot enter proof obligations.

## Next Experiment

Instantiate L140.1 on one guarded-dDNNF row-cover FormulaEval line and one unread-enable-bit hidden row; compute K_tec, U_tec, X_tec, Gamma_tec, and the exact exponent inequality tau+alpha+eta<epsilon or its failure.

# MCSP / Meta-Complexity Carrier Transfer supporting FormulaEval parser boundary

## Candidate Lemma

For the restricted proof system Psys_sym^{QEeq-cell}, equality compression of FormulaEval row sets is valid exactly for rows covered by prefix-visible canonical cell-refinement witnesses; uncovered influential rows are sum-charged, and any uncharged uncovered influence yields a private-row falsifier. Under this interface the Gamma ledger extends the bit-explicit Psys_bEF^- line induction and gives the same-model SIZE upper-bound obstruction for any claimed LB_N(1+epsilon) below the charged threshold.

## Definitions

- source object: a bit-explicit Psys_sym^{QEeq-cell} transcript pi for H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, quarantined FormulaEval blocks, canonical cell-decomposable row producers, and prefix timestamps for every rule use.
- target object: a same-theory nonuniform SIZE circuit upper bound for H_N^{SAT} obtained by expanding only the charged occurrence rows, used as a falsifier for a stronger transcript-derived LB_N(1+epsilon) claim, not as a P vs NP lower bound.
- controlled interface: RowSetEqualityWitness_N is a prefix-visible record containing producer identifiers, cell identifiers, row-index equations, refinement-cover lists, first-owner identifiers, dominator-exit timestamps, and occurrence-expansion pointers for every compressed row class.
- target-preserving condition: every influencing FormulaEval row is either enumerated and charged before first external use or is covered by a syntactic equality witness before that use; no SAT-truth pruning, semantic row equality, hidden advice, or post-use witness may affect the target SIZE model.

## Assumptions

- Circuit target is ordinary nonuniform SIZE on the truth table family H_N^{SAT}; the parser may hardwire the proof transcript but may not use advice selecting uncharged rows.
- Length regime has N tending through the proof family lengths, M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)}, and SAT instance length polylogarithmic or otherwise charged in the row-expansion term.
- Psys_bEF^- rules already satisfy the Gap98-SRhNormalForm ledger Gamma_bEF(pi), with row pointers, touched occurrence neighborhoods, and eta/tau overheads bounded in the archived parser theorem.
- Each FormulaEval producer in the restricted class has a canonical cell decomposition whose cells have prefix-computable row-index descriptions and disjoint or witness-refinable coverage.
- Dominator timing is strict: a quarantine exit may release delayed FormulaEval consequences only after all owned or equality-covered rows in its influence cone are visible and charged.
- Equality compression is syntactic, not semantic: two row producers are identified only through a RowSetEqualityWitness_N proof of cell refinement and row-index equality available in pi_{<t}.
- The lower-bound claim being falsified is same-model LB_N(1+epsilon): C(H_N^{SAT})>N^{1+epsilon-o(1)} in the same nonuniform SIZE model used by the parser simulation.

## Equations

- Gamma_QEeq_ledger: `\Gamma_{QEeq}(\pi)=\Gamma_{bEF}(\pi)+U_{cell}(\pi)+X_{fo}(\pi)+X_{sum}(\pi)+N^{o(1)}E_{FE}(\pi)`. Valid when: Valid when pi is a Psys_sym^{QEeq-cell} transcript whose FormulaEval support, equality witnesses, and quarantine exits are prefix-visible before first external use.
- first_owner_expansion_charge: `X_{fo}(\pi)=N^{1+o(1)}\cdot |K^{fo}_{idx}(\pi)|`. Valid when: Applies when each first-owned row index expands to a same-theory SAT occurrence row of size N^{1+o(1)} or the stated row-size charge.
- uncovered_sum_charge: `X_{sum}(\pi)=N^{1+o(1)}\cdot \operatorname{mult}(K^{uncov}_{idx}(\pi))`. Valid when: Valid when uncovered or equality-unwitnessed influences are not compressed and are instead charged with multiplicity at their first use.
- same_model_upper_bound: `C_{SIZE}(H_N^{SAT}) \le N^{\rho+o(1)}+\Gamma_{QEeq}(\pi)+O(E_{base}(\pi)N^{1+o(1)})`. Valid when: Requires the parser simulation to preserve the same nonuniform SIZE target and to expand only prefix-certified occurrence rows.
- support_density_corollary: `|K^{fo}_{idx}(\pi)|+\operatorname{mult}(K^{uncov}_{idx}(\pi)) \ge N^{\epsilon-o(1)}`. Valid when: Valid when a transcript is claimed to certify LB_N(1+epsilon) and the preceding same-model upper-bound falsifier is avoided.
- fractional_q_threshold: `\frac{|K^{fo}_{idx}|+\operatorname{mult}(K^{uncov}_{idx})}{M_N} \ge N^{\epsilon-q-o(1)}`. Valid when: Applies in the beta-zero parity setting M_N=N^{q+o(1)} after row expansion is charged at N^{1+o(1)} per row.

## Attempted Derivation

- Define each FormulaEval producer P as a prefix-visible canonical cell list Cell(P) whose cell c carries a row-domain predicate D_c(j), a row-index expression idx_c(z), and an occurrence expansion pointer to G_N(x,idx_c(z)).
- Define a RowSetEqualityWitness record W=(P,Q,c,d,theta,owner,t_dom,t_use,Ref) where theta proves idx_c(z)=idx_d(z') over the refined domain Ref, owner is the first charged producer, t_dom is the quarantine-exit dominator, and t_dom<t_use.
- Verifier bit fields are: producer_id bits, cell_id bits, local decomposition path bits, refinement-child count, child row-domain constraints, row-index equation proof, first-owner pointer, dominator-exit pointer, and expansion-row pointer. Each field is read before the FormulaEval line uses the compressed row.
- Induct over proof lines. Base Psys_bEF^- lines use the archived Gamma_bEF parser. A transparent FormulaEval line adds U_cell for cell enumeration plus X_fo for newly first-owned rows. A QE exit is legal only if it dominates all external uses and releases all owned/equality-covered rows with charges already in Gamma_QEeq.
- For an equality witness, replace a duplicate row charge by a pointer to the first owner only when the cell-refinement cover is total over the influencing row domain. Partial coverage leaves uncovered rows in K_idx^{uncov} and charges them with multiplicity.
- For the first illegal semantic compression, choose a row j in the uncovered influential symmetric difference. Since no prefix record reads or charges j, make two occurrence completions agreeing on all read bits but differing on SAT(G_N(x,j)) or on an unread enable bit. The downstream FormulaEval value changes, contradicting validity of the compressed parser.
- The resulting circuit hardwires pi, computes the generator part in N^{rho+o(1)}, and expands exactly the charged rows, giving the same-model upper bound stated in the lemma.

Blocking gap: CanonicalCellDecomposition_N is proved only for interval-union, ROBDD, guarded dDNNF, and projected-dDNNF with explicit witness support. Arbitrary AC0 membership selectors or full semantic SAT-equivalence producers still lack a support-sensitive canonical cell verifier.

## Falsifiers

- falsifier: semantic row deduplication without a prefix RowSetEqualityWitness_N lets a private row change FormulaEval while every charged proof bit is fixed.
- falsifier: post-hoc equality witness after first external dependency violates dominator timing and cannot justify compression.
- falsifier: membership-only AC0 selector with no output-sensitive enumerator pays full scan or becomes a hidden-support countermodel.
- falsifier: SAT-truth branch pruning chooses rows by real satisfiability rather than proof-visible syntax and is outside the controlled interface.
- falsifier: nonuniform advice selecting equal row classes preserves a circuit upper bound for a fixed transcript but is invalid as an advice-free parser theorem.

## Learning

Cycle 140 upgrades equality compression from a coverage invariant to a verifier-field theorem for canonical cell producers. The valid local rule is first-owner compression only under prefix-visible cell-refinement equality and dominator timing; otherwise the proof must sum-charge or faces a finite private-row falsifier. This improves the paper parser module and remains route-level support, not P vs NP progress.

## Gedanken Experiment Design Seed

- Need decision: `use now as a falsifier probe for equality-compression timing`
- Rationale: The branch no longer needs another abstract TransparentRowSupport_N restatement; it needs a concrete test of whether prefix cell witnesses are enough to distinguish valid compression from semantic dedup leakage.
- Situation seed: A projected-dDNNF FormulaEval block has two producers P and Q over the same M_N=N^{q+o(1)} row universe. P exposes canonical cells immediately; Q hides auxiliary witnesses until a quarantine exit. The proof tries to count P and Q as one support set before the exit.
- Varied variable: lambda, the fraction of Q's influential rows covered by prefix-visible cell-refinement witnesses before the first external FormulaEval dependency.
- Held-fixed controls: H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)) and the same nonuniform SIZE target LB_N(1+epsilon)., Generator overhead N^{rho+o(1)}, Psys_bEF^- base parser costs, and row expansion charge N^{1+o(1)} per charged row., No SAT-truth pruning and no nonuniform advice for choosing equality classes., Quarantine exits must dominate all external uses and be prefix-visible before release.
- Expected observation: For lambda=1 the compressed first-owner ledger is valid and charges U_cell+X_fo. For lambda<1, every uncovered influential row is either sum-charged, increasing X_sum, or gives a private-row/unread-enable-bit countermodel. The q-threshold then depends on the charged post-compression support, not on semantic equality size.
- Transfer certificate needed: A formal CanonicalCellDecomposition_N plus RowSetEqualityWitness_N verifier showing total refinement coverage, row-index equality, first-owner identity, and dominator timing before the FormulaEval line may affect the Gamma_QEeq proof obligations.

## Next Experiment

Work a two-producer projected-dDNNF example end to end: list cells, write one RowSetEqualityWitness_N record, compute U_cell, X_fo, X_sum, and then delete one refinement child to exhibit the first private-row falsifier.
