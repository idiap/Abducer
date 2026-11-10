# cycle-0122

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For a transparent Psys_sym^dag FormulaEval proof pi, the least verifier-visible prefix-closed reachable support cone K_dag(pi), computed by backward fixed point from the final LB_N line, is sufficient and minimal for the same-model parser-to-circuit falsifier. If N^{rho+o(1)}+Gamma_dag(pi)+O(E_pi N)<N^{1+epsilon-o(1)}, then the claimed source lower bound LB_N(1+epsilon) for H_N^SAT is false in the named SIZE model.

## Definitions

- source object: H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)) with |x|=N, M_N=N^{q+o(1)}, SAT query length L_N=(log N)^d, generator cost N^{rho+o(1)}, and a Psys_sym^dag proof pi of LB_N(1+epsilon).
- target object: a same-nonuniform-SIZE circuit for H_N^SAT below N^{1+epsilon-o(1)}, used as a falsifier to the source lower-bound claim and not as a P != NP proof.
- controlled interface: verifier-visible FormulaEval cells (a,r), parent pointers Parent(a,r), row-index maps, enumerators Enum_a, same-theory expansions Exp_a, and the prior bit-explicit Gamma_bEF ledger for EF, SATeq, and bounded-SR_h lines.
- target-preserving condition: beta=0 polylogarithmic SAT-query length, advice-free row enumeration or full-scan charge, prefix closure under later symbolic use, same-theory occurrence expansion, and no hidden FormulaEval row influence before use.
- source_statement: LB_N(1+epsilon) asserts C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)} in the same nonuniform circuit model used by the parser.
- target_statement: subthreshold Gamma_dag gives C_SIZE(H_N^SAT)<=N^{rho+o(1)}+Gamma_dag(pi)+O(E_pi N), contradicting the source statement only within this route.
- model_context: beta-zero parity magnification carrier, Psys_bEF^- plus transparent FormulaEval extensions, nonuniform SIZE circuits, syntactic parser simulation, no semantic SAT-truth advice.
- quantifier_context: N ranges over valid lengths, epsilon>0 and q,rho are fixed constants, d>1 is fixed, pi may be nonuniform but its support certificates are verifier-visible and advice-free.

## Assumptions

- Every FormulaEval line has finite bit fields: opcode, selector code, parent cell list, row-index encoding, same-theory expansion code, and declared enumeration or full-scan cost.
- For each reachable cell (a,r), the verifier can compute Parent(a,r) and RowSupp(a,r) in time charged to U_N(K_dag) without consulting SAT labels or hidden advice.
- FormulaEval outputs used by later lines are closed backward: if a reachable line uses a symbolic value whose definition depends on row r, then (a,r) is inserted before the line-induction step for that later line.
- Bit-explicit EF, SATeq, and bounded-SR_h subproofs satisfy the previously promoted Gamma_bEF normal form, including eta and tau charges for SR_h leaves.
- All row expansions are same-theory occurrences over the generated SAT formulas G_N(x,j); no expansion may replace row syntax by semantic truth-table advice.
- The live pvsnp_inference_quality status is restricted-valid: source and target statements are named, the reduction is parser-to-circuit simulation, and the blocked full-system obligation is RealSATInfluenceRealizer_N.

## Equations

- fixed_point_definition: `K_0=\operatorname{Seed}(\operatorname{FinalLB}(\pi)),\quad K_{t+1}=K_t\cup\operatorname{BackParents}(K_t)\cup\operatorname{RowSupp}(K_t),\quad K_{\dagger}=\operatorname{lfp}(K_t)`. Valid when: Valid when every FormulaEval use exposes verifier-readable parent maps and row support certificates.
- finite_convergence_bound: `T_{\dagger}\le |\operatorname{Cells}(\pi)|+|\operatorname{RowsDeclared}(\pi)|`. Valid when: Applies when the dependency graph is finite and rows are explicitly indexed.
- charged_gamma: `\Gamma_{\dagger}(\pi)=\Gamma_{bEF}(\pi)+U_N(K_{\dagger})+X_N(K_{\dagger})`. Valid when: Valid when bEF charges are already parsed and FormulaEval support is transparent.
- parser_to_circuit_falsifier: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{\dagger}(\pi)+O(E_{\pi}N)`. Valid when: Requires the generator, parsed proof transcript, and sparse residual patches to be same-model circuits.
- subthreshold_contradiction_window: `N^{\rho+o(1)}+\Gamma_{\dagger}(\pi)+O(E_{\pi}N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Valid when LB_N is a lower bound against the same nonuniform SIZE model.
- support_density_corollary: `|K_{idx}(\pi)|\ge N^{\epsilon-o(1)},\qquad |K_{idx}(\pi)|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Applies after each charged row costs at most N^{1+o(1)} to patch.

## Attempted Derivation

- Parse pi line by line into ordinary bEF lines and FormulaEval cells (a,r). For each FormulaEval cell record opcode, row index r, parent-cell pointers, selector code, expansion code, and an enumerator or full-scan certificate.
- Build the backward dependency graph D_pi whose edges go from a used cell to its verifier-visible parent cells and to row occurrences that must be expanded in the same theory.
- Initialize K_0 by the final LB_N assertion and the carrier rows whose parity is read by the final falsifier construction. This seed is syntactic; it contains no SAT-truth advice.
- Iterate K_{t+1}=K_t union BackParents(K_t) union RowSupp(K_t). Termination is bounded by the finite set of declared cells and rows, so K_dag is auditor-computable.
- Define U_N(K_dag) as the sum of enumerator or full-scan costs needed to list reachable rows, and X_N(K_dag) as the same-theory occurrence-expansion cost for exactly those rows.
- Run the existing Gamma_bEF line induction for ordinary EF, SATeq, and bounded-SR_h lines. For FormulaEval lines, use closure of K_dag to guarantee that every later symbolic use already has its parent rows and expansions charged.
- Construct circuits for all reachable proof-line predicates with total size Gamma_bEF(pi)+U_N(K_dag)+X_N(K_dag), then compose with the generator circuit of size N^{rho+o(1)}.
- If the induced circuit is wrong on E_pi exceptional source inputs, patch them by equality circuits at cost O(E_pi N), giving the displayed upper bound for H_N^SAT.
- Derive the q-trichotomy: subthreshold Gamma_dag forces |K_idx|>=N^{epsilon-o(1)}; hence q<epsilon is an enumeration falsifier, q=epsilon forces near-full contact, and q>epsilon leaves weak but absolute support pressure.
- For minimality, choose the first downstream use of an uncharged reachable row and construct two row-label worlds that agree on all visible fields but differ on that row, producing the private-row or unread-enable-bit contradiction.

Blocking gap: The restricted theorem is valid for transparent extensional FormulaEval, but it does not settle full semantic FormulaEval. The named gap is RealSATInfluenceRealizer_N: real SAT-semantic reasoning may determine row influence without a verifier-visible row set, and this requires a nonrelativizing charged realizer or a rule-specific no-go.

## Falsifiers

- first-hidden-reachable-row falsifier: a row affects the final LB_N line but is absent from K_dag and all charges, so two visible-identical transcripts disagree on the carrier.
- unread-enable-bit falsifier: a selector enable controls row reachability while not appearing in parent pointers, invalidating local transparency despite an apparently valid row list.
- q<epsilon enumeration falsifier: K_idx must have absolute size N^{epsilon-o(1)} but the universe has only M_N=N^{q+o(1)} rows.
- semantic-advice leakage: Enum_a or RowSupp(a,r) depends on SAT truth or nonuniform row advice rather than proof syntax and N.
- positive-beta transfer falsifier: any black-box target-circuit substitution with query length n^beta gives the cap q+beta c+o(1), so it cannot yield all-exponent target exclusion unless beta=0 or subpolynomial.
- nonprefix local support falsifier: a row is surfaced where defined but hidden after a later symbolic use, breaking the line-induction invariant.

## Learning

Cycle 122 upgrades K_dag from a named minimal support object to a referee-auditable fixed-point proof packet. The valid theorem is restricted but paper-relevant: least prefix-closed reachable FormulaEval support is sufficient for Gamma_dag line induction and necessary for extensional safety by a first-hidden-row falsifier. The full semantic case is still blocked exactly at RealSATInfluenceRealizer_N, not by generic barrier folklore or by the P vs NP conjecture itself.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_validation_and_falsifier_probe`
- Rationale: The branch already has the abstract K_dag theorem; a concrete projected-dDNNF/unread-enable experiment tests whether the fixed-point support is implementable and whether minimality catches exactly the hidden influence.
- Situation seed: A beta-zero XOR carrier with M_N=N^q polylog-length SAT rows, and a Psys_sym^dag proof containing one projected-dDNNF FormulaEval selector whose output rows feed the final LB_N line.
- Varied variable: alpha, where z_N=N^alpha is the number of projected enable-controlled rows not surfaced as parent cells.
- Held-fixed controls: H_N^SAT parity carrier, M_N=N^{q+o(1)}, L_N=(log N)^d with d>1, and generator cost N^{rho+o(1)}., Same nonuniform SIZE model, bit-explicit Gamma_bEF normal form, bounded-SR_h eta/tau charges, and beta=0 target-query regime., No SAT-truth advice in the selector; only visibility of projection parents is varied.
- Expected observation: For alpha<epsilon, hidden enables are patchable and yield a subthreshold private-row falsifier. For alpha>=epsilon, the theorem forces those rows into K_dag and the charge appears as absolute support pressure rather than selector folklore.
- Transfer certificate needed: A verifier-visible projection-parent list and row enumerator proving U_D(K) and X_D(K), or else a two-world unread-enable-bit countermodel certifying that the FormulaEval rule is outside the transparent theorem.

## Next Experiment

Write the paper-ready L122 module: formal theorem statement, fixed-point pseudocode, line-induction proof, projected-dDNNF charge example, unread-enable-bit counterexample, q-trichotomy corollary, and a separate RealSATInfluenceRealizer_N open-boundary paragraph.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For Psys_sym^dag, the reachable FormulaEval support K_dag(pi) is the least fixed point of an explicit verifier worklist. If every reachable FormulaEval line supplies visible row-cover and influence certificates, then pi has a prefix-scoped same-theory bEF expansion with charge Gamma_dag(pi). Therefore a subthreshold Gamma_dag gives a same-model SIZE falsifier to the asserted LB_N(1+epsilon), while sound proofs force row-equivalent support at least N^{epsilon-o(1)}.

## Definitions

- source object: A Psys_sym^dag proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)) with N=2^n and M_N=N^{q+o(1)}.
- target object: A same-model nonuniform SIZE falsifier circuit for H_N^SAT below N^{1+epsilon-o(1)}, or a forced row-equivalent support lower bound when the LB_N line is sound.
- controlled interface: Visible FormulaEval_DAG records exposing parent pointers, selector code, row-cover enumeration, influence certificates, and same-theory row-expansion splice sites.
- target-preserving condition: The deterministic parser uses no SAT-truth advice, every influencing row is in the reachable fixed point K_dag(pi), and each FormulaEval row expands inside the same bEF/SATeq theory with fresh prefix-scoped variables.
- observable: K_dag(pi) contains row tokens (a,j) only when FormulaEval line a is reachable from the final LB line and j is certified as row-influential for a.

## Assumptions

- Model: nonuniform Boolean SIZE for H_N^SAT and a bit-explicit proof system Psys_bEF extended only by transparent FormulaEval_DAG rules.
- Regime: N=2^n, |pi|=N^{tau+o(1)}, generator overhead N^{rho+o(1)}, rho<1+epsilon, and all verifier overheads are N^{o(1)}-stable.
- Uniformity/advice: the parser and row enumerators are deterministic from (N,pi) and receive no hidden selector, SAT-truth, or semantic row advice.
- Same-theory condition: every FormulaEval expansion line can be spliced before its first use with fresh extension variables and without changing earlier proof semantics.
- Cutoff: the final LB_N(1+epsilon) line means CC(H_N^SAT)>N^{1+epsilon-o(1)} in the same nonuniform circuit model.

## Equations

- worklist_fixed_point: `L_0=\{\ell_{final}\},\ K_0=\emptyset;\quad K_{t+1}=K_t\cup\bigcup_{a\in L_t\cap FE} RowEnum_a(N);\quad L_{t+1}=L_t\cup Par(L_t)\cup ExpPar(K_{t+1})`. Valid when: Valid when all active FormulaEval lines expose terminating row enumerators and parent pointers checked by the Psys_sym^dag verifier.
- least_support: `K_{dag}(\pi)=\mu K\;\Phi_\pi(K)\subseteq K\quad\text{and}\quad K_{dag}(\pi)\subseteq K'\ \text{for every prefix-closed valid support }K'`. Valid when: Valid when prefix-closed support means closure under proof parents, FormulaEval influence rows, and expansion parent obligations.
- charge_definition: `\Gamma_{dag}(\pi)=\Gamma_{bEF}(\pi\upharpoonright L_{dag})+U_{dag}(\pi)+X_{dag}(\pi),\quad X_{dag}=\sum_{(a,j)\in K_{dag}}\chi(a,j)`. Valid when: Valid when bEF lines are parsed bit-explicitly and FormulaEval rows are replaced by prefix-scoped same-theory expansion gadgets.
- parser_to_circuit_falsifier: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{dag}(\pi)+O(E_\pi N)`. Valid when: Applies after the parsed generator circuit and Gamma_dag transcript are combined inside the same nonuniform SIZE model.
- forced_row_equivalent_support: `N^{\rho+o(1)}+\Gamma_{dag}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \text{LB}_N(1+\epsilon)\ \text{has a same-model falsifier}`. Valid when: Requires the LB_N assertion to quantify over the same circuit model and the parser to be advice-free.
- q_density_corollary: `\text{if lower-order debts are }o(N^{1+\epsilon}),\quad |K_{dag}|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Valid when each charged FormulaEval row contributes N^{1+o(1)} expansion cost and M_N=N^{q+o(1)}.

## Attempted Derivation

- Define verifier-visible records for each FormulaEval_DAG line: parent ids, selector code, influence flags, RowEnum or full-scan declaration, RCert for projected gates, and expansion-splice identifiers.
- Run the monotone worklist from the final LB_N line. Add proof parents for active lines, add RowEnum_a(N) for active FormulaEval lines, and add expansion parents for each row token. Termination is finite because each line and certified row token is inserted once.
- Prove leastness by Tarski/Kleene iteration on the finite poset of line sets and row-token sets. Any valid prefix-closed support must contain the final line and be closed under exactly the same verifier rules, hence contains K_dag(pi).
- Splice expansions in topological prefix order with fresh extension variables. The earlier proof is unchanged because each splice is before first use and shares only declared parent variables.
- Charge the transformed proof by Gamma_bEF on reachable bEF material plus U_dag enumerator debt plus X_dag row-expansion debt. This derives the same-model circuit upper bound for H_N^SAT.
- Derive the falsifier inequality: if N^{rho+o(1)}+Gamma_dag+O(E_pi N)<N^{1+epsilon-o(1)}, then the asserted LB_N(1+epsilon) is false in the same nonuniform SIZE model.
- Test projected-dDNNF FormulaEval. With RCert, it satisfies the worklist interface; without RCert, a projected private row j* changes selector semantics while the visible transcript is fixed.

Blocking gap: Full semantic FormulaEval is still blocked at RealSATInfluenceRealizer_N. The more local projected-dDNNF subgap is RowCoverCertificate_N: projection nodes must expose extensional row covers or the first hidden projected row becomes a countermodel.

## Falsifiers

- falsifier: q<epsilon with small Gamma_dag gives an explicit same-model circuit upper bound contradicting the claimed LB_N(1+epsilon).
- falsifier: projected-dDNNF without RCert hides a row j* behind existential projection, so K_dag is incomplete and the transfer is not valid.
- falsifier: unread-enable-bit FormulaEval yields identical visible transcripts and different H_N^SAT parity, refuting surface occurrence completion.
- falsifier: a semantic FormulaEval atom that decides real SAT influence without listing rows violates no-advice extraction and must be quarantined until RealSATInfluenceRealizer_N is proved.
- falsifier: exporting K_dag acceptance as a large constructive useful truth-table property would trigger the natural-proofs PRF conflict unless non-largeness or nonconstructivity is certified.

## Learning

Cycle 122 turns L120.1 into an auditable fixed-point theorem: K_dag is computed by a finite worklist and is minimal among prefix-closed transparent supports. The new boundary is RowCoverCertificate_N for projected-dDNNF; missing covers yield a first hidden-row falsifier. This is route-level proof-system certification, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for projected-dDNNF transparency.`
- Rationale: The branch needs a concrete target-preserving test of whether K_dag sees only reachable support or silently assumes semantic row covers. Another abstract restatement would not decide the projected-dDNNF boundary.
- Situation seed: A Psys_sym^dag proof has one FormulaEval line whose selector is a projected-dDNNF over rows j<M_N. One row j* is selected only when an auxiliary projection variable z is enabled, and the final carrier is H_N^SAT with row j* padded to be parity-decisive on x0.
- Varied variable: row-cover visibility lambda, where lambda=0 means every projection gate has RCert and lambda=1 means the first projected gate hides j*.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, and the final line remains LB_N(1+epsilon) for the same H_N^SAT carrier., The proof system is Psys_sym^dag with the same bEF parser, prefix-splice discipline, and no hidden advice to the K_dag parser., Generator overhead stays N^{rho+o(1)} with rho<1+epsilon, so only support visibility is varied., All visible proof syntax, displayed dDNNF gates, and enumerated rows outside j* are held identical in the two worlds.
- Expected observation: For lambda=0, K_dag enumerates j* or charges a full scan and Gamma_dag remains valid. For lambda=1, two worlds have identical visible transcripts but differ on row j*, producing the unread projected-row falsifier.
- Transfer certificate needed: A verifier-checkable RowCoverCertificate_N, or the stronger RealSATInfluenceRealizer_N, must uniformly list every projection-influential row and add its charge before the intuition may affect proof obligations.

## Next Experiment

Instantiate the worklist on a three-gate projected-dDNNF selector: one visible interval row, one decomposable AND, and one projected OR hiding j*. Compute K_dag and Gamma_dag with RCert present, then remove RCert and display the first hidden-row bisimulation.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For a bit-explicit transparent Psys_sym^dag proof pi_N of a beta-zero LB_N(1+epsilon) statement, the least prefix-closed reachable support cone K_dag(pi_N) is computable from proof bits and yields the valid ledger Gamma_dag=Gamma_bEF+U_dag+X_dag. If N^{rho+o(1)}+Gamma_dag+O(E_pi N)<N^{1+epsilon-o(1)}, the proof transcript gives a same-theory SIZE upper-bound falsifier for the claimed lower bound. This is a restricted parser theorem, not P != NP.

## Definitions

- source object: a bit-explicit Psys_sym^dag proof pi_N over H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, visible proof-line parents, and FormulaEval lines carrying selector/support certificates.
- target object: a same-theory nonuniform SIZE upper-bound falsifier for LB_N(1+epsilon), namely a circuit for the same H_N^SAT below N^{1+epsilon-o(1)} in the model used by the lower-bound claim.
- controlled interface: the least prefix-closed reachable support cone K_dag(pi_N), computed by a fixed-point closure over proof parents, selector certificates, row enumerators, and row-expansion obligations, with ledger Gamma_dag(pi_N).
- target-preserving condition: every FormulaEval influence row is enumerated advice-free and charged before use, row expansion uses the same SAT formulas rather than a semantic oracle, and no hidden support advice or nonuniform hard-row choice enters the parser.
- K_idx(pi_N) is the set of SAT-query row indices reached by K_dag; U_dag is first-discovery row-support enumeration cost; X_dag is same-theory expansion cost for reached rows.
- Gamma_bEF is the already restricted bit-explicit proof parser ledger for non-FormulaEval bEF/SR_h lines; E_pi is the ordinary line-count or extension bookkeeping overhead charged outside FormulaEval.

## Assumptions

- Model: Psys_sym^dag has Cook-Reckhow-verifiable bit fields for line type, parent pointers, selector code, support enumerator certificate, and row-expansion certificate.
- Regime: N tends to infinity, M_N=N^{q+o(1)}, generator overhead for G_N is N^{rho+o(1)}, epsilon>0 is fixed, and all o(1) terms are uniform over the proof family.
- Uniformity/advice: the fixed-point closure and every row enumerator are advice-free algorithms determined by N and pi_N; no SAT-truth table, hard-row selector, or nonuniform witness list is supplied.
- Same-theory condition: expanding a row means inserting the syntactic SAT instance G_N(x,j) and its declared formula-evaluation transcript, not querying an external SAT oracle.
- Barrier status: the claim is nonrelativizing only through explicit SAT syntax; full semantic FormulaEval is quarantined unless RealSATInfluenceRealizer_N supplies charged influence witnesses.
- Non-claim: the lemma only shows a low-cost-proof falsifier inside the scoped proof system; it does not prove a superpolynomial lower bound or P != NP.

## Equations

- Kdag-fixed-point: `K_0=\{v_{\rm fin}\},\quad K_{s+1}=K_s\cup {\rm Par}(K_s)\cup {\rm SelCert}(K_s)\cup {\rm RowExp}({\rm Rows}(K_s)),\quad K_{\dagger}=\bigcup_s K_s.`. Valid when: Valid when the proof DAG exposes parent pointers, selector certificates, and row-expansion nodes as finite verifier-visible bit fields.
- influence-closure: `R_{\dagger}=\bigcup_{v\in K_{\dagger}\cap FE}{\rm Rows}(v),\quad {\rm Infl}(v)\subseteq R_{\dagger}\ \text{ for every }\ v\in K_{\dagger}\cap FE.`. Valid when: Valid when every FormulaEval rule is transparent and the enumerator is advice-free before the semantic value is used.
- Gamma-dag-ledger: `\Gamma_{\dagger}(\pi_N)=\Gamma_{bEF}(\pi_N|K_{\dagger})+U_{\dagger}(R_{\dagger})+X_{\dagger}(R_{\dagger}),\quad X_{\dagger}=N^{1+o(1)}|K_{idx}(\pi_N)|.`. Valid when: Applies after K_dag closure is computed and row expansions remain in the same SAT theory without oracle advice.
- same-model-falsifier-threshold: `N^{\rho+o(1)}+\Gamma_{\dagger}(\pi_N)+O(E_{\pi}N)<N^{1+\epsilon-o(1)}\ \Longrightarrow\ \neg LB_N(1+\epsilon).`. Valid when: Requires the target-preserving parser-to-circuit simulation in the same nonuniform SIZE model and subthreshold exponent regime.
- q-contact-ledger: `M_N=N^{q+o(1)},\ |K_{idx}|=N^{a+o(1)}\ \Longrightarrow\ X_{\dagger}=N^{1+a+o(1)};\ a<\epsilon\ \text{ is subthreshold contact}.`. Valid when: Valid when M_N=N^{q+o(1)} and each charged row expansion has length N^{1+o(1)} with polylog formula overhead.

## Attempted Derivation

- Define a proof-line DAG with typed vertices: bEF/SR_h local lines, FormulaEval lines, selector-certificate lines, and row-expansion lines. Parent pointers are verifier-visible bit fields.
- Run the K_dag fixed-point algorithm from the final LB_N line. When a FormulaEval vertex enters the cone, add its selector certificate, enumerate Rows(v), and add one same-theory row-expansion obligation per newly reached row.
- Maintain the induction invariant: two surface occurrence completions agreeing on all vertices in the current cone and on all charged rows give identical values to every line in the cone. Local bEF/SR_h rules use the old Gamma_bEF induction; FormulaEval uses influence closure.
- At the fixed point, the final lower-bound line is determined by charged proof bits and charged SAT rows only. Combining the generator circuit, the parsed transcript, and row expansions gives the same-model upper-bound circuit with cost N^{rho+o(1)}+Gamma_dag+O(E_pi N).
- If this cost is below N^{1+epsilon-o(1)}, the original LB_N(1+epsilon) assertion is falsified inside the target SIZE model. If influence closure fails at the first bad FormulaEval line, apply the private-row/unread-enable-bit countermodel instead.

Blocking gap: The fixed-point and induction are theorem-shaped for transparent Psys_sym^dag, but the paper proof still needs the exact bit-field layout for RowExp and the eta/tau overhead constants imported from the finalized Gamma_bEF normal form. Full semantic FormulaEval remains blocked at RealSATInfluenceRealizer_N.

## Falsifiers

- First hidden FormulaEval influence row outside K_dag changes a line value while all visible transcript bits remain fixed.
- Membership-only selector with no output-sensitive enumerator pays full scan charge or becomes a semantic-oracle case.
- Projected selector with hidden auxiliary witness imports row-support advice and violates the target-preserving condition.
- Unwitnessed SAT extensionality supplies semantic influence without charged RealSATInfluenceRealizer_N and is not valid for the parser theorem.
- Any MCSP/MKtP carrier that selects a hard row by advice or ranking without searchable row support fails the same uniformity ledger.

## Learning

Cycle 122 upgrades K_dag from an invariant name to an auditable fixed-point parser: the reachable cone is computable from proof bits, Gamma_dag follows by line induction, and the first uncharged semantic influence is a finite falsifier. The contribution is a scoped transparent FormulaEval obstruction theorem with an explicit RealSATInfluenceRealizer_N boundary, not progress on the main P vs NP conjecture.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The branch already has the abstract K_dag theorem; a concrete projected-dDNNF FormulaEval line tests whether the fixed-point closure is implementable and whether hidden projection witnesses trigger the exact countermodel.
- Situation seed: A beta-zero H_N^SAT proof contains one projected guarded-dDNNF FormulaEval line selecting rows j for which exists w C(j,w)=1, plus an optional unread enable literal in one projected witness fiber.
- Varied variable: projection fiber entropy ell, measured as the exponent of hidden witnesses per projected row before deduplication.
- Held-fixed controls: H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)} and fixed generator overhead N^{rho+o(1)}., Same Psys_sym^dag verifier with visible parent pointers and no nonuniform row advice., Same-theory SAT row expansion cost N^{1+o(1)} per distinct projected row., Final target remains only the LB_N(1+epsilon) parser falsifier, not a new P vs NP lower bound.
- Expected observation: When ell is certified by a dedup enumerator, K_dag charges U_v+N^{1+o(1)}T_v and the line is transparent. When ell is hidden, the unread enable bit produces two completions with identical visible support and different FormulaEval values.
- Transfer certificate needed: A referee-checkable dedup enumerator or witness enumeration certificate, plus a proof that every influential projected row is in K_dag before the FormulaEval line is used.

## Next Experiment

Write the RowExp verifier bit fields and eta/tau charges for one projected-dDNNF FormulaEval line, then run the K_dag fixed-point algorithm and construct the unread-enable-bit countermodel when the dedup certificate is removed.
