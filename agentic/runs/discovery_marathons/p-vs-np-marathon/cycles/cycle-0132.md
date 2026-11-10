# cycle-0132

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For Psys_sym^{dag+DTSR} proofs whose FormulaEval supports are transparent and whose bounded Tseitin self-reduction children are completely declared, the least reachable support cone K_DTSR(pi) is computable from pi and yields a same-model parser-to-circuit falsifier whenever N^{rho+o(1)}+Gamma_DTSR(pi)+O(E_pi N)<N^{1+epsilon-o(1)}. This is a restricted proof-system obstruction, not a lower bound for H_N or P != NP.

## Definitions

- source object: a Psys_sym^{dag+DTSR} proof pi of LB_N(1+epsilon) for the beta-zero parity carrier H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)} and polylog formula length L_N.
- target object: a nonuniform SIZE circuit for H_N^SAT of size below N^{1+epsilon-o(1)}, contradicting the asserted source lower-bound certificate in the same circuit model.
- controlled interface: the computable least prefix-closed reachable support cone K_DTSR(pi), containing bEF dependencies, transparent FormulaEval rows, SATeq links, bounded SR_h leaves, and fully declared DTSR child rows with bit-level parent pointers.
- target-preserving condition: beta=0 query length, advice-free support enumeration, same-theory row expansion, complete DTSR child declaration, generator overhead N^{rho+o(1)}, and no hidden semantic row selection before the rule is charged.
- K_DTSR(pi) is computed by starting from the final LB_N line, repeatedly adding verifier-visible parents, FormulaEval influence rows, extension-support rows, SR_h leaf rows, and every DTSR child tuple listed in the rule bit fields until a fixed point is reached.
- A DTSR child tuple has fields (line_id,parent_row,restriction_id,child_row,child_formula_id,local_clause_map,polarity,enable_bit); all fields are syntactic and audited before the semantic self-reduction conclusion is used.

## Assumptions

- Circuit model is nonuniform SIZE over Boolean circuits; the upper-bound falsifier and the claimed LB_N use the same model and length N.
- Quantifier regime: fixed epsilon>0, q,rho,kappa,theta are constants or slowly stable exponents, o(1) terms are uniform along valid N, and E_pi=N^{e+o(1)} counts residual patch rows.
- Formula length is L_N=(log N)^d or any N^{o(1)} length so SAT circuit substitution has beta=0; positive beta would trigger the black-box substitution cap.
- Proof syntax is bit-explicit: parent pointers, row indices, occurrence neighborhoods, extension-variable support, and DTSR child lists are recoverable in time polynomial in |pi| without semantic advice.
- DTSR completeness assumption: each enabled semantic restriction child that can affect the final LB_N line appears in the declared child list or is supplied by a nonrelativizing RealSATInfluenceRealizer_N^{arb}.
- Barrier status: the positive parser relativizes as a syntactic simulation; the only escape is nonrelativizing real-SAT influence realization. No natural-proofs claim is made because no dense truth-table property is used.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j<M_N} SAT(G_N(x,j)),\qquad M_N=N^{q+o(1)}`. Valid when: Valid when the source carrier is the beta-zero generated parity family and G_N uniformly emits polylog-length SAT instances indexed by j.
- dtsr_charge: `B_{DTSR}(\pi)=N\cdot P_N\cdot C_N=N^{1+\kappa+\theta+o(1)}`. Valid when: Valid when P_N=N^{kappa+o(1)} reachable DTSR parent rows each declare C_N=N^{theta+o(1)} child rows with bit-visible indices.
- ledger: `\Gamma_{DTSR}(\pi)=\Gamma_{bEF}(\pi)+U(K_{DTSR})+X(K_{DTSR})+B_{SR_h}(\pi)+B_{DTSR}(\pi)`. Valid when: Applies after the fixed-point parser has closed every reachable transparent influence and every declared self-reduction child before semantic use.
- parser_upper_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{DTSR}(\pi)+O(E_\pi N)`. Valid when: Requires the target-preserving same-model simulation, advice-free support lists, and equality patching only on E_pi explicitly named residual rows.
- subthreshold_falsifier: `\max\{\rho,\gamma,1+e\}<1+\epsilon,\ \Gamma_{DTSR}(\pi)=N^{\gamma+o(1)},\ E_\pi=N^{e+o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Valid when the alleged proof certificate asserts a SIZE lower bound for exactly the same H_N and all parser charges are included.

## Attempted Derivation

- Define K_DTSR^0 as the final LB_N line and its explicit H_N row references.
- Iterate a deterministic closure operator: for each bEF line add parent dependencies and extension supports; for each transparent FormulaEval line add enumerated or full-scan RowSet entries; for SATeq add quotient-linked rows; for SR_h add bounded leaf rows; for DTSR add every declared child tuple and its occurrence neighborhood.
- Termination is immediate because the closure ranges over the finite proof DAG and finite declared child lists; the least fixed point is independent of traversal order by monotonicity.
- Verifier bit fields for a DTSR child tuple are line_id, parent_row, restriction_id, child_row, child_formula_id, local_clause_map, polarity, enable_bit, and next_pointer; each field is read by the local checker before charging B_DTSR.
- Line induction invariant: after processing line t, the partial transcript over K_DTSR restricted to lines <=t suffices to build the corresponding circuit fragment with size bounded by the accumulated Gamma ledger plus generator and residual costs.
- The DTSR line case composes the already-built parent-row circuit with the declared child circuits and local Tseitin maps; because every enabled child is in K_DTSR, no semantic branch is consulted for free.
- At the final line, the transcript yields C(H_N)<=N^{rho+o(1)}+Gamma_DTSR(pi)+O(E_pi N); if this is below N^{1+epsilon-o(1)}, the alleged LB_N certificate is refuted in the same model.
- For hidden pruning, choose the first reachable unlisted child r*, hold all charged rows fixed, flip the row label or unread enable bit at r*, and propagate the parity difference; this proves the countermodel unless a real-SAT influence realizer charges r*.

Blocking gap: RealSATInfluenceRealizer_N^{arb}: arbitrary semantic branch-pruning may be valid over real SAT yet not expose an advice-free row list in the proof syntax. The present theorem covers declared DTSR and transparent support only.

## Falsifiers

- positive beta falsifier: if SAT query length is N^beta with beta>0, SAT in SIZE(n^c) gives source size N^{q+beta c+o(1)} and caps all-exponent transfer
- first-unlisted-child falsifier: a reachable DTSR child not listed in K_DTSR permits two charged-identical transcripts with different final parity
- unread-enable-bit falsifier: a hidden branch-selection bit controls influence while remaining absent from the row ledger
- subthreshold ledger falsifier: Gamma_DTSR(pi)+N^{rho+o(1)}+O(E_pi N)<N^{1+epsilon-o(1)} constructs a same-model circuit for H_N
- nonuniform leakage falsifier: row sets chosen by semantic advice rather than verifier-visible syntax invalidate TransparentRowSupport_N

## Learning

Cycle 132 upgrades declared bounded TSR from a rule-case slogan to a fixed-point parser theorem with explicit bit fields, closure algorithm, ledger, and necessity falsifier. The valid contribution is the restricted TransparentRowSupport_N^{DTSR} theorem/countermodel pair; full semantic pruning remains quarantined exactly at RealSATInfluenceRealizer_N^{arb}.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The declared-DTSR theorem is close to paper-ready, but the full semantic pruning escape is exactly where hidden influence may evade the charged support cone; a concrete two-world test checks whether the boundary is real rather than a restatement.
- Situation seed: Construct a beta-zero parity carrier H_N^SAT with M_N=N^q slots and a proof line applying bounded Tseitin self-reduction to P_N=N^kappa parent rows, each having C_N=N^theta possible restriction children; all but one child are declared in K_DTSR, and the missing child controls one parity slot through an unread enable bit.
- Varied variable: child-declaration exponent theta, equivalently the fraction of enabled TSR children surfaced before the semantic rule is used.
- Held-fixed controls: beta=0 polylog SAT instances and the same nonuniform SIZE model for source and target, generator overhead N^{rho+o(1)} and parity aggregation H_N^SAT fixed, bit-explicit bEF, SATeq, SR_h, and transparent FormulaEval rules fixed, no hidden advice in row enumeration and no change to the final LB_N threshold N^{1+epsilon-o(1)}
- Expected observation: Full declaration yields the charge B_DTSR=N^{1+kappa+theta+o(1)} and a valid line-induction rule case; deleting one reachable enabled child leaves all charged fields unchanged but permits a private-row flip changing the final parity, so hidden pruning cannot be folded into Gamma_DTSR for free.
- Transfer certificate needed: A RealSATInfluenceRealizer_N^{arb} certificate: from the proof syntax and N alone, uniformly list every semantically influencing child row, prove same-theory expansion of those rows, and charge the resulting R_N before the pruning inference is used.

## Next Experiment

Write the paper-ready L132 proof block: pseudocode for K_DTSR(pi), a table of DTSR bit fields and verifier checks, the five line-induction cases, and the first-unlisted-child countermodel; then test one projected-dDNNF+DTSR positive example and one unread-enable-bit hidden-pruning counterexample.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For Psys_sym^{Uidx-SR_h}, where a FormulaEval line may use an unannotated existential index variable y to select bounded-SR_h child rows, there is a dichotomy: either the line carries a proof-visible RowCoverCertificate listing every feasible influencing row and pays the corresponding expansion charge, or the first omitted feasible row gives a private-row/unread-enable-bit falsifier to any occurrence-only RealSATInfluenceRealizer_N. This is a scoped proof-system boundary, not a P != NP theorem.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with N=2^n, M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and a claimed short Psys_sym^{Uidx-SR_h} proof pi of LB_N(1+epsilon).
- target object: same-model nonuniform Boolean SIZE upper-bound falsifier for LB_N(1+epsilon), or forced row-equivalent support at least N^{epsilon-o(1)} inside the proof transcript.
- controlled interface: RealSATInfluenceRealizer_N must, before a semantic FormulaEval_Uidx rule is used, output an advice-free influence-closed row set R_A, same-theory row expansions, prefix-scoped extension variables, and a charged ledger term R_N.
- target-preserving condition: the parser must be deterministic, no-advice, same-theory, and row-faithful; any semantic row that can change the FormulaEval value must be visible in K_idx^+(pi) or charged by full enumeration before the lower-bound-to-circuit transfer is invoked.
- FormulaEval_Uidx line: a displayed rule tuple (T,e,P) contains a bounded-SR_h template T, an enable bit e, and a visible or hidden predicate P(y), while the semantic value may touch Row(T,y) for some feasible y with P(y)=1.
- RowCoverCertificate: a proof-visible list or enumerator C_A satisfying R_A={Row(T,y): P(y)=1 and e can be active}, with membership and completeness checkable from N and the line prefix.

## Assumptions

- Model context: nonuniform Boolean SIZE for the target circuit upper bound; bit-explicit bEF plus FormulaEval_Uidx for the source proof object; the transfer is simulation/extraction, not a many-one reduction.
- Length and exponent regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, h=N^{eta+o(1)}, rho<1+epsilon, and all ledger o(1) terms are uniform over the chosen proof family.
- Uniformity and advice status: the realizer and row-cover checker receive only N, pi, and displayed rule bits; hidden SAT-truth advice or private row advice is disallowed.
- Same-theory condition: every charged row expansion is inserted as bEF/FormulaEval material over the same carrier and with fresh prefix-scoped extension variables, so the resulting transcript remains in the audited proof system.
- Barrier status: the omitted-row countermodel is a relativizing row-oracle falsifier for a semantic parser; a real-SAT positive escape must be nonrelativizing and must prove actual influence completeness for G_N-produced SAT formulas.

## Equations

- uidx_charge_repair: `Gamma_Uidx(pi)=Gamma_TRS(pi)+Enum(R_A)+N*|R_A|`. Valid when: Valid when each FormulaEval_Uidx line supplies a complete proof-visible RowCoverCertificate and same-theory row expansions are prefix-spliced.
- private_row_bisimulation: `O_0|K = O_1|K and O_0(r*) != O_1(r*) => H_{O_0}(x) xor H_{O_1}(x)=1`. Valid when: Valid when r* is a feasible omitted parity row outside the parser support K and the row-oracle model treats carrier rows independently.
- parser_falsifier_inequality: `N^{rho+o(1)}+Gamma_Uidx(pi)<N^{1+epsilon-o(1)} => not LB_N(1+epsilon)`. Valid when: Applies after the charged transcript constructs the same H_N^SAT function in the nonuniform SIZE model with no hidden semantic support.
- support_density_corollary: `|K_idx^+(pi)|/M_N >= N^{epsilon-q-o(1)}`. Valid when: Valid when the lower-bound proof is sound, rho<1+epsilon, and enumeration and bEF debts are lower order than the forced support threshold.

## Attempted Derivation

- Instantiate a concrete semantic rule Uidx-SR_h: a line contains a bounded-SR_h template T, an enable bit e, and an existential index predicate P(y); if e=1 and some feasible y is used, FormulaEval may depend on the row r=Row(T,y).
- Run the least-support parser K_dag from the final LB_N line. If all feasible rows Row(T,y) are in K_dag or in a displayed cover R_A, classify the line as transparent and charge Enum(R_A)+N|R_A|.
- If some feasible row r* is not in K_dag and no cover lists it, build two row-oracle carriers O_0,O_1 agreeing on all visible proof bits and every row in K_dag but differing on r*. The surface transcript and occurrence parser output are identical.
- Set the unread enable bit active on the semantic branch selecting r*. Then FormulaEval_Uidx can distinguish O_0 from O_1 although the parser ledger cannot. For a parity carrier input x using r*, H_{O_0}(x) and H_{O_1}(x) differ by one XOR bit.
- Therefore occurrence-only completion is invalid for the unannotated rule. The only target-preserving repairs are a visible row cover, a full scan charge, or a nonrelativizing real-SAT influence theorem.
- Under the visible-cover repair, splice row-expanded bEF material before the semantic line, add N|R_A| and enumeration debt to Gamma_TRS, and reuse the cycle-131 line induction to obtain the subthreshold upper-bound falsifier.

Blocking gap: The no-go is complete for row-oracle semantic parsers, but it is not a theorem that real SAT rows generated by G_N admit the same independence; a positive full-system route remains blocked at a nonrelativizing RealSATInfluenceRealizer_N for actual SAT semantics.

## Falsifiers

- First omitted feasible row r* outside K_dag: two row-oracle carriers agree on all charged rows while the unread-enable FormulaEval branch changes value.
- Hidden predicate P(y) supplied as semantic advice: the parser cannot enumerate R_A from proof bits, so TransparentRowSupport_N is invalid.
- Output-sensitive cover that lists only accepting rows without a completeness proof: a rejected but influencing row gives the same private-row falsifier.
- Subthreshold ledger N^{rho+o(1)}+Gamma_Uidx<N^{1+epsilon-o(1)}: if accepted as a lower-bound proof, it constructs a same-model SIZE upper bound and falsifies LB_N(1+epsilon).

## Learning

Cycle 132 improves the proof-delivery map by replacing the vague full-semantic FormulaEval gap with a rule-level dichotomy for unannotated existential-index bounded-SR_h. Visible row covers give a valid TRS extension with explicit Gamma charge; an omitted feasible row gives a finite falsifier to occurrence-only parsing. The result is a scoped parser/falsifier theorem and not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for RealSATInfluenceRealizer_N on one concrete semantic rule.`
- Rationale: The branch has a valid transparent-support theorem; the remaining contribution-making move is to decide whether a semantic FormulaEval rule supplies chargeable influence or hides a row. An abstract barrier restatement would not improve the proof packet.
- Situation seed: Take H_N^SAT with M_N=N^{q+o(1)} rows and a Psys_sym^{Uidx-SR_h} proof containing one FormulaEval line whose hidden index y selects a singleton row r* through a bounded-SR_h child template; compare an annotated version listing r* with an unannotated version using an unread enable bit.
- Varied variable: hidden-index domain exponent alpha where the feasible set size |{y:P(y)}|=N^{alpha+o(1)}.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)} with rho<1+epsilon., The proof surface, displayed bounded-SR_h template, and all charged bEF/TRS rows are identical in the two row-oracle worlds., The parser is deterministic, no-advice, prefix-scoped, and may charge only proof-visible rows or full scans., The target transfer remains same-model nonuniform SIZE, not a many-one reduction to a different carrier.
- Expected observation: For alpha=0, a visible singleton cover costs O(N) bits and is transparent; without the cover, the private-row falsifier already works. For alpha>0, transparency costs Enum(R_A)+N^{1+alpha+o(1)} or a full scan; hiding the set leaves an omitted row with unchanged surface transcript.
- Transfer certificate needed: A valid certificate is either a RowCoverCertificate with completeness proof and Gamma charge, or a nonrelativizing RealSATInfluenceRealizer_N proving that actual SAT influence rows are derivable from displayed syntax without semantic advice.

## Next Experiment

Write the finite Uidx-SR_h verifier fields: encoding of y, predicate P, Row(T,y), enable bit e, cover list R_A, completeness check, and prefix-splice order; then test whether actual G_N-produced SAT rows admit any nonrelativizing RealSATInfluenceRealizer_N beyond explicit row covers.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For Psys_sym^QE proofs whose delayed FormulaEval work is sealed in syntactic quarantine components, a prefix-visible exit-dominator forest gives a valid union-charge Gamma_QE line induction. The same-model circuit upper bound is C_SIZE(H_N^SAT) <= N^{rho+o(1)}+Gamma_QE(pi)+O(E_pi N), so any claimed LB_N(1+epsilon) below this threshold is falsified inside the restricted proof-system model.

## Definitions

- source object: a bit-explicit Psys_sym^QE proof pi of a beta-zero SAT-parity lower-bound line LB_N(1+epsilon), with bEF core lines, FormulaEval lines, syntactic quarantine components Q_a, and exposed proof bits before each use.
- target object: a same-N nonuniform SIZE circuit for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), or equivalently a restricted-model falsifier to the asserted LB_N(1+epsilon).
- controlled interface: each quarantine component has a unique exit e(a) carrying a prefix-visible enumerator for all influential FormulaEval row indices and a same-theory occurrence expansion certificate before any external dependency reads the component.
- target-preserving condition: no SAT-truth advice, nonuniform hard-row choice, or after-the-fact support discovery is used; the parser, row expansion, and final circuit all remain in the same nonuniform SIZE model and length regime.
- K_exit(pi) is the deduplicated union of influential row indices first charged at the exit nodes of the dominator forest.
- U_exit(pi) is the total cost of prefix-visible row-set enumeration at exits, including certified projection deduplication when witnesses are projected.
- X_exit(pi)=N^{1+o(1)}|K_exit(pi)| is the same-theory row expansion cost for all newly charged rows.

## Assumptions

- Length regime: N tends to infinity, M_N=N^{q+o(1)}, G_N has generator overhead N^{rho+o(1)}, and all formula lengths inside G_N are polylogarithmic in N.
- Proof model: Psys_sym^QE extends the already parsed Psys_bEF^- core by FormulaEval rules that are either transparent at first external use or sealed inside syntactic quarantine.
- Dominance regime: for every quarantine component Q_a, the exit e(a) dominates all edges from Q_a to nonquarantined lines in the proof dependency DAG.
- Uniformity/advice regime: exit enumerators and expansion certificates are determined by N and pi_{<=e(a)}; no nonuniform selector, hidden SAT-truth bit, or semantic advice is allowed.
- Same-theory condition: row expansion is a syntactic occurrence expansion in the same proof/circuit model, not an oracle call to real SAT semantics.
- Threshold convention: LB_N(1+epsilon) asserts the absence of SIZE at most N^{1+epsilon-o(1)} circuits for H_N^SAT at the considered lengths.

## Equations

- beta_zero_carrier: `H_N^SAT(x)=xor_{1<=j<=M_N} SAT(G_N(x,j)),  M_N=N^{q+o(1)}`. Valid when: Valid when G_N is the fixed advice-free generator and M_N=N^{q+o(1)} in the beta-zero SAT-parity construction.
- exit_union: `K_exit(pi)=Union_{e in Exit(pi)} (R_e \ setminus Union_{e'<e} R_{e'})`. Valid when: Valid when quarantine exits are topologically ordered and previously charged row indices are deducted.
- gamma_qe: `Gamma_QE(pi)=Gamma_bEF(pi)+U_exit(pi)+N^{1+o(1)} |K_exit(pi)|+O(E_pi N^{o(1)})`. Valid when: Valid when every exported dependency is dominated by a charged exit and enumerators are prefix-visible.
- same_model_upper_bound: `C_SIZE(H_N^SAT) <= N^{rho+o(1)} + Gamma_QE(pi) + O(E_pi N)`. Valid when: Valid when the bit-explicit bEF parser, same-theory row expansion, and generator circuit all use the same nonuniform SIZE model.
- lb_falsifier_threshold: `max{rho,gamma_QE,e+1} < 1+epsilon  =>  not LB_N(1+epsilon)`. Valid when: Valid when Gamma_QE=N^{gamma_QE+o(1)} and E_pi=N^{e+o(1)} are measured on the same N scale.

## Attempted Derivation

- Construct the proof dependency DAG with bEF core nodes, FormulaEval nodes, quarantine-internal edges, and external edges leaving quarantine.
- For every quarantine component Q_a, require a syntactic exit e(a); compute a dominator forest by contracting components whose exits dominate all outgoing dependencies.
- Order exits topologically and define R_new(e)=R_e minus previously charged rows, so row support shared by several exits is charged once.
- Induction invariant I_t: every nonquarantined line reachable before t has a parser simulation whose cost is bounded by Gamma_bEF on core rules plus the union of R_new(e) for exits already crossed; quarantined lines have no external semantic effect until their exit.
- Core bEF rules preserve I_t by the archived Gap98-SRhNormalForm line induction.
- A transparent FormulaEval exit preserves I_t because pi_{<=e} supplies an advice-free enumerator for R_e and a same-theory occurrence expansion for every newly charged row.
- If an external edge leaves Q_a before e(a), choose the least such line and apply FirstHiddenInfluenceCountermodel by flipping an unread row or enable bit while preserving the visible prefix.
- At the final LB_N line, I_t yields C_SIZE(H_N^SAT) <= N^{rho+o(1)}+Gamma_QE(pi)+O(E_pi N); if this is below N^{1+epsilon-o(1)}, the proof transcript is a same-model falsifier to LB_N(1+epsilon).

Blocking gap: The derivation is complete only for syntactic Psys_sym^QE exits. Full truth-pruned semantic FormulaEval remains blocked at RealSATInfluenceRealizer_N: no zero-latency, advice-free procedure is known that lists all SAT-truth influential rows before first use.

## Falsifiers

- A first external dependency from a quarantine block before its exit is a private-row falsifier.
- An exit enumerator that is correct only using SAT-truth pruning is not valid without a zero-latency RealSATInfluenceRealizer_N.
- A projected selector whose witness fiber is hidden and not deduplicated pays witness-scan cost or triggers an unread-enable-bit falsifier.
- A nonuniform row selector or hardwired hard-row choice invalidates target preservation because it changes the source-to-target uniformity ledger.
- If q<epsilon and all overheads are subthreshold, even full FormulaEval support M_N=N^{q+o(1)} cannot sustain LB_N(1+epsilon); this is a quantitative falsifier, not a main-conjecture result.

## Learning

Cycle 132 adds the missing sharing ledger for quarantined FormulaEval: support delayed behind multiple syntactic blocks is valid exactly when exits form a prefix-visible dominator forest and row sets are charged by first occurrence. The contribution is a scoped parser/falsifier theorem with exact Gamma_QE accounting; the remaining escape is a named zero-latency RealSATInfluenceRealizer_N, not generic proof-system strength or P vs NP progress.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for RealSATInfluenceRealizer_N and the QE exit timing rule.`
- Rationale: The branch needs a concrete semantic FormulaEval stress test because the abstract transparent-support theorem is already theorem-shaped; the live uncertainty is whether truth-pruned SAT self-reduction can be made prefix-visible without hidden advice.
- Situation seed: A Tseitin-extension FormulaEval block computes SAT(F) by a bounded self-reduction tree, but prunes one branch using the real SAT value of an unread subformula; the block is wrapped in a syntactic quarantine with a proposed exit certificate.
- Varied variable: exit latency ell, the number of external proof dependencies that read the pruned value before the exit lists and expands the influential subformula rows.
- Held-fixed controls: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)} and fixed advice-free G_N., Same nonuniform SIZE target model and LB_N(1+epsilon) threshold., Bit-explicit Psys_bEF core parser and same-theory row expansion cost N^{1+o(1)} per row index., No nonuniform row advice and no post-hoc support certificates after first external use.
- Expected observation: For ell=0 with a complete prefix-visible influence list, the block is valid and pays U_exit+N^{1+o(1)}|R_e|. For ell>0, two completions agreeing on the visible prefix but differing on the pruned branch give a private-branch falsifier.
- Transfer certificate needed: A zero-latency RealSATInfluenceRealizer_N for the chosen Tseitin self-reduction: before any external dependency, it must uniformly enumerate every SAT-truth influential row and provide same-theory row expansions with a charged overhead R_N.

## Next Experiment

Instantiate the dominator-forest algorithm on one projected-dDNNF-with-quarantine proof toy model and one truth-pruned Tseitin self-reduction; compute U_exit, K_exit, X_exit, and exhibit the first hidden row when exit latency ell>0.
