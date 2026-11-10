# cycle-0121

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: L121 least-closed support audit

## Candidate Lemma

For a Psys_sym^dag proof pi with bit-explicit bEF lines and transparent FormulaEval lines, the least prefix-closed reachable support cone K_dag(pi), computed from the final LB_N line by verifier-visible dependency closure, is sufficient for the Gamma_dag line induction. If N^{rho+o(1)}+Gamma_dag(pi)+O(E_pi N)<N^{1+epsilon-o(1)}, then the claimed LB_N(1+epsilon) has a same-model circuit falsifier. This is a restricted parser/falsifier theorem, not a proof of P != NP.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, SAT instance length L_N=(log N)^d, beta=0, and generator circuit size N^{rho+o(1)}.
- target object: the same nonuniform SIZE statement LB_N(1+epsilon) asserting C(H_N^SAT)>N^{1+epsilon-o(1)} inside Psys_sym^dag; the target is not NP not subset P/poly.
- controlled interface: a parser from proof pi to a circuit/transcript using bit-explicit Gamma_bEF charges plus visible FormulaEval row enumeration U_N(K) and same-theory row-expansion charge X_N(K).
- target-preserving condition: all reachable FormulaEval influences are surfaced by advice-free syntax, prefix-closed before later symbolic use, expanded in the same proof theory, and charged before applying the beta-zero parity magnification bridge.
- K_dag(pi): the least fixed point containing the final lower-bound line, its proof parents, every FormulaEval row named by reachable support certificates, and every later support dependency of those rows.
- U_N(K): verifier-visible cost to enumerate or full-scan the row identifiers in K, including selector code and parent-pointer traversal.
- X_N(K): occurrence/row expansion cost for rows in K, normally \tilde O(N|K_idx|) when each selected slot row is expanded across N source inputs.

## Assumptions

- Length regime: N tends to infinity, epsilon>0 is fixed, q and rho are fixed real exponents, and all o(1) terms are uniform over pi_N.
- Proof model: Psys_sym^dag lines have explicit parent pointers; bEF extension variables are bit-explicit; FormulaEval lines expose selector code, support certificates, and occurrence-neighborhood fields.
- Transparency regime: a later proof line may use a FormulaEval value only through an influence path already included in K_dag(pi).
- Advice status: row sets are computed from N and proof syntax only; no nonuniform SAT-truth advice or hidden row selector is allowed.
- Same-theory condition: each charged row expansion is represented as a Psys_sym^dag object, not as an external semantic oracle.
- Error regime: E_pi exceptional source rows are allowed only if they are equality-patchable at cost O(E_pi N) in the same SIZE model.
- Barrier status: the theorem is relativizing for extensional row labels; full semantic SAT FormulaEval is excluded unless RealSATInfluenceRealizer_N supplies a nonrelativizing charged row set.

## Equations

- fixed_point_closure: `K_{0}=\{\ell_{final}\},\quad K_{t+1}=K_t\cup Par(K_t)\cup Supp_{FE}(K_t)\cup Infl(K_t),\quad K_{dag}=\bigcup_t K_t.`. Valid when: Valid when Psys_sym^dag exposes parent pointers and FormulaEval support certificates syntactically.
- gamma_dag_ledger: `\Gamma_{dag}(\pi)=\Gamma_{bEF}(\pi)+U_N(K_{dag}(\pi))+X_N(K_{dag}(\pi)).`. Valid when: Applies after the closure algorithm has surfaced every reachable FormulaEval influence.
- parser_upper_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{dag}(\pi)+O(E_\pi N).`. Valid when: Requires beta zero, same-model row expansion, and equality patching for exceptional rows.
- lb_falsifier_window: `N^{\rho+o(1)}+\Gamma_{dag}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon).`. Valid when: Valid when LB_N is the lower-bound claim for the same carrier and circuit model.
- support_density_corollary: `|K_{idx}(\pi)|\ge N^{\epsilon-o(1)},\quad |K_{idx}(\pi)|/M_N\ge N^{\epsilon-q-o(1)}.`. Valid when: Applies when each charged FormulaEval slot has expansion cost \tilde O(N).

## Attempted Derivation

- Normalize pi into a finite DAG of lines with IDs, parent lists, and rule tags; reject lines whose parents are implicit semantic advice.
- Initialize the active line set A with the final LB_N line and initialize K_idx, K_occ, U, X to empty ledgers.
- Process a worklist: when a line is popped, add all proof parents to A; for a bEF line add its bit-explicit dependency charge to Gamma_bEF.
- For each reachable FormulaEval line, run its visible support enumerator or certified full scan; add each row identifier, occurrence-neighborhood, and parent support certificate to K_dag.
- Close under later symbolic use: if a reachable line reads a FormulaEval value, add the row certificate and all support parents before the line is counted valid.
- Terminate because each step adds a proof line, support certificate, or row occurrence from the finite transcript; the fixed point is least by monotonicity of the closure operator.
- Prove the line-induction invariant: every reachable line has a same-theory circuit/transcript of size at most the accumulated prefix of Gamma_bEF+U+X, with exceptional rows recorded in E_pi.
- At the final LB_N line, compose the generator for G_N with the parsed transcript and equality patches, obtaining C(H_N^SAT)<=N^{rho+o(1)}+Gamma_dag+O(E_pi N).
- Derive the falsifier inequality: a proof of LB_N(1+epsilon) with subthreshold Gamma_dag contradicts the same-model circuit upper bound, so any valid proof must pay the support-density threshold.
- For minimality, remove a reachable influencing row and choose two row-label worlds agreeing on K_dag but differing there; the first line whose value changes gives the private-row/unread-enable-bit countermodel.

Blocking gap: The restricted proof is complete only for transparent extensional FormulaEval. Full semantic SAT FormulaEval remains blocked at RealSATInfluenceRealizer_N: proof syntax must nonrelativizingly determine and charge every real SAT influence before use.

## Falsifiers

- first-hidden-reachable-row falsifier: a later proof line depends on a row absent from K_dag
- unread-enable-bit falsifier: selector output is disabled in syntax but semantically gates an uncharged row
- q<epsilon enumeration falsifier: subthreshold reachable support density yields an immediate small circuit for the claimed LB_N
- semantic-advice falsifier: RowSet(a) is chosen using SAT truth or nonuniform advice rather than proof syntax
- same-theory failure falsifier: row expansion is asserted externally and cannot be represented inside Psys_sym^dag
- positive-beta transfer falsifier remains quarantined: q+beta c caps all-exponent target transfer unless beta=0 or subpolynomial

## Learning

Cycle 121 turns K_dag(pi) into a finite auditable fixed-point object. The valid contribution is sharper than the previous transparency slogan: least prefix-closed reachable support is sufficient for the Gamma_dag parser and necessary for extensional safety via a first-hidden-row falsifier. The remaining full-system gap is exactly RealSATInfluenceRealizer_N for real SAT-semantic FormulaEval, not generic relativization, natural proofs, or P vs NP folklore.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for L121.2 and as a validation example for L121.3.`
- Rationale: The least-closed support theorem needs a concrete boundary test showing that prefix closure is not cosmetic: one uncharged reachable row must break the parser while a visible projected-dDNNF cone must be validly charged.
- Situation seed: Take H_N^SAT with M_N=N^q slots and a Psys_sym^dag proof containing one projected-dDNNF FormulaEval line whose output is later used in the final LB_N line; add an optional unread enable bit e_j controlling one projected row r_j.
- Varied variable: theta where the number of hidden enabled reachable rows is N^theta, with all other exponents fixed.
- Held-fixed controls: beta=0 and L_N=(log N)^d SAT instances, generator cost N^{rho+o(1)} and same nonuniform SIZE model, bit-explicit bEF charges Gamma_bEF are unchanged, FormulaEval syntax size and projected-dDNNF graph size S_D are fixed, no SAT-truth advice is allowed in row enumeration
- Expected observation: When theta<epsilon, hidden enabled rows are patchable or give a private-row countermodel, so LB_N(1+epsilon) is not validly certified. When all enabled rows are surfaced, Gamma_dag pays roughly N^{1+theta} expansion and the support-density pressure appears explicitly.
- Transfer certificate needed: A verifier-visible K_dag fixed-point enumeration plus same-theory expansion for every enabled projected row; for real SAT-semantic enabling, a nonrelativizing RealSATInfluenceRealizer_N certificate must list the same influence-closed row set before the intuition may enter proof obligations.

## Next Experiment

Write the formal L121.1 proof skeleton as theorem text: fixed-point pseudocode for K_dag, induction invariant per rule type, charge table for bEF/SR_h/FormulaEval/projected-dDNNF, and the unread-enable-bit counterexample with theta<epsilon.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

In Psys_sym^dag, where every FormulaEval line exposes parent pointers, selector code, support certificates, and same-theory row-expansion templates, the least prefix-closed reachable support cone K_dag(pi) is computable from pi and N. Replacing exactly this cone by row-expanded bEF material yields a charge Gamma_dag and the same-model SIZE falsifier for any claimed LB_N(1+epsilon) below threshold.

## Definitions

- source object: a beta-zero SAT-parity carrier H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)) with N=2^n, M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)}, and a Psys_sym^dag proof pi of LB_N(1+epsilon).
- target object: a same-model nonuniform SIZE upper-bound falsifier C(H_N^SAT)<N^{1+epsilon-o(1)} contradicting that particular proof-system lower-bound claim, not a proof of P != NP.
- controlled interface: LeastClosedTransparentSupport_N, the finite fixed-point parser over final-line reachability, bEF parent pointers, FormulaEval selector certificates, influence rows, prefix extension definitions, and row-expansion templates.
- target-preserving condition: every semantic row used by a FormulaEval inference is proof-visible, advice-free enumerable or full-scan charged, influence-closed, and expandable inside the same bEF theory with fresh prefix-scoped extension variables.

## Assumptions

- Model: nonuniform Boolean SIZE on the same N-bit truth-table carrier, with Psys_bEF local rules plus transparent FormulaEval_DAG rules only.
- Regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, generator cost N^{rho+o(1)}, and fixed epsilon>0 with rho<1+epsilon.
- Uniformity/advice: the closure operator reads only pi and N; selector enumeration uses no SAT-truth advice and no hidden row oracle.
- Same-theory condition: each charged FormulaEval atom has a bEF row-expansion proof using only earlier prefix definitions and fresh local extension variables.
- Barrier status: the theorem is proof-system-specific and nonrelativizing only through bit syntax and proof soundness; if it induces a large constructive useful truth-table property, the natural-proof falsifier audit applies separately.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j<M_N} SAT(G_N(x,j)),\qquad M_N=N^{q+o(1)}`. Valid when: Valid when N=2^n and M_N=N^{q+o(1)} are the fixed carrier lengths in the beta-zero parity construction.
- least_cone: `K_{dag}(\pi)=\operatorname{lfp}(\Phi_{\pi,N})`. Valid when: Valid when the proof syntax exposes parent pointers, selector code, and support certificates before any FormulaEval semantic step is invoked.
- charge: `\Gamma_{dag}(\pi)=\Gamma_{bEF}(\pi\upharpoonright K_{dag})+U_{dag}(\pi)+X_{dag}(\pi)+O(E_{\pi}N)`. Valid when: Applies after every reachable FormulaEval line has either enumerated rows or paid the full row-expansion charge in the same proof theory.
- subthreshold_falsifier: `N^{\rho+o(1)}+\Gamma_{dag}(\pi)<N^{1+\epsilon-o(1)}\;\Longrightarrow\; C(H_N^{SAT})<N^{1+\epsilon-o(1)}`. Valid when: Requires the target-preserving same-model circuit extraction from the row-expanded bEF transcript and the generator overhead bound rho<1+epsilon.
- forced_support: `\widehat S_{dag}(\pi):=|K_{dag}|+\lceil U_{dag}/N\rceil+E_{\pi}\ge N^{\epsilon-o(1)}`. Valid when: Valid when the proof is sound for LB_N(1+epsilon) and the subthreshold falsifier inequality is unavailable because the charge is too large.

## Attempted Derivation

- Define the finite universe V(pi,N) of proof lines, FormulaEval atoms, selector-code nodes, formula-DAG nodes, extension-definition nodes, and row indices j<M_N that are explicitly reachable from displayed certificates.
- Define Phi_{pi,N}; from the final LB_N line it adds parent lines, bEF occurrence neighborhoods, FormulaEval RowSet certificates, formula-DAG parents, influence rows, and earlier extension definitions needed by any active node.
- Iterate Phi from the final line until saturation. Because the universe is finite and all transitions are proof-bit computable, K_dag(pi) is advice-free and auditable.
- Prove minimality: any prefix-closed transparent splice support S must be closed under the same transitions; hence by induction on iterations K_dag(pi) subset S.
- For each reachable FormulaEval atom, invoke its row-expansion template on every row in K_dag and introduce fresh extension variables immediately before the atom's first use; charge enumeration to U_dag and row clauses to X_dag.
- Perform line induction over the original proof order. Non-cone lines are irrelevant to the final line; cone bEF lines are parsed by Gamma_bEF, and cone FormulaEval lines have already been replaced by row-expanded bEF material.
- Apply the existing parser-to-circuit extraction to the spliced transcript: if N^{rho+o(1)}+Gamma_dag(pi)<N^{1+epsilon-o(1)}, the same carrier has a smaller SIZE circuit, giving the route-level falsifier to LB_N(1+epsilon).
- Test projected-dDNNF: the argument is valid with a proof-visible disjoint projection-cover certificate, but ordinary semantic projection does not expose first influencing row and fails the TRS checker.
- Test unread-enable-bit: two visible-identical transcripts with different hidden enable state agree under Phi but differ on row influence, proving that opaque semantic FormulaEval is not covered.

Blocking gap: Full semantic FormulaEval remains blocked exactly at RealSATInfluenceRealizer_N: for arbitrary semantic SAT-evaluation rules, pi and N need not uniformly determine an influence-closed row set before the rule is used.

## Falsifiers

- Unread-enable-bit FormulaEval: one hidden row j* changes the semantic atom while all visible selector fields remain identical, falsifying surface occurrence completion.
- Projected-dDNNF without disjoint projection-cover certificate: existential projection can hide the first influencing row, so RowSet is semantic advice rather than transparent support.
- q<epsilon source-ceiling falsifier: C(H_N^SAT)<=N^{1+q+o(1)} already contradicts any claimed N^{1+epsilon} lower bound when q<epsilon-o(1).
- Nonprefix extension reuse: a row expansion depending on a future or redefined extension variable breaks same-theory splicing and invalidates Gamma_dag accounting.
- Natural-property pressure falsifier: if the extracted checker becomes poly(N)-constructive, dense, and useful against the same SIZE class, it conflicts with PRF-based natural-proofs assumptions rather than supporting P != NP.

## Learning

Cycle 121 improves the TRS packet by replacing all-selector support with a least reachable fixed point K_dag(pi). The new valid contribution is a minimality theorem plus a charge-preserving prefix-splice proof: transparent FormulaEval pays Gamma_dag, while projected-dDNNF without row-cover certificates and unread-enable-bit semantic support are finite falsifier objects. Live inference-quality packet: source_statement=short Psys_sym^dag proof pi of LB_N(1+epsilon) for H_N^SAT; target_statement=same-model SIZE upper-bound falsifier or forced row-equivalent support; model_context=nonuniform Boolean SIZE, beta-zero SAT-parity carrier, bEF plus transparent FormulaEval_DAG, simulation/extraction rather than many-one reduction; quantifier_context=N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, generator overhead N^{rho+o(1)}, rho<1+epsilon, deterministic no-advice closure; derivation_status=restricted L120.1 proof packet derived, full semantic FormulaEval blocked at RealSATInfluenceRealizer_N; reviewer_findings=valid only for proof-visible influence and same-theory expansion, naturalness pressure applies only if the checker becomes large constructive useful, and there is no claim toward P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch needs a concrete boundary test for L120.1: projected-dDNNF FormulaEval looks transparent syntactically, but existential projection can hide row influence unless a row-cover certificate is charged.
- Situation seed: A Psys_sym^dag proof contains one FormulaEval line A_D using a projected-dDNNF selector D for rows of H_N^SAT, and a paired version A_D^e where an unread enable bit secretly toggles one row j*.
- Varied variable: projection-cover explicitness lambda: lambda=0 means only semantic projection is asserted, lambda=1 means a disjoint proof-visible row-cover certificate is provided and charged.
- Held-fixed controls: Carrier H_N^SAT with N=2^n and M_N=N^{q+o(1)}., Target class nonuniform SIZE and claimed threshold N^{1+epsilon}., Generator overhead N^{rho+o(1)} with rho<1+epsilon., No SAT-truth advice and same-theory bEF row expansion requirement., Proof length and selector code are held polynomial in N.
- Expected observation: At lambda=1, Phi_{pi,N} reaches all projected rows and Gamma_dag pays U_D+X_D; at lambda=0, the unread-enable row j* is invisible, giving a bisimulation falsifier to any uncharged parser theorem.
- Transfer certificate needed: A formal ProjectedDNNFSupportCertificate_N proving output-sensitive row enumeration, disjoint projection, influence closure, and prefix-scoped bEF row expansion before the FormulaEval line may enter the proof queue as valid.

## Next Experiment

Write the finite verifier pseudocode for Phi_{pi,N}; run it on a toy projected-dDNNF with a disjoint row-cover certificate and on the unread-enable-bit pair, recording K_dag, U_dag, X_dag, and the first row where semantic support escapes.

# MCSP / Meta-Complexity Carrier Transfer supporting TransparentRowSupport_N proof delivery

## Candidate Lemma

For a bit-explicit Psys_sym^dag proof pi whose FormulaEval lines expose selector code, parent pointers, support certificates, and same-theory row expansions, the least prefix-closed reachable cone K_dag(pi) is computable without advice; the parser ledger is Gamma_dag(pi)=Gamma_bEF(pi)+U_N(K_dag)+X_N(K_dag); if N^{rho+o(1)}+Gamma_dag(pi)+O(E_pi N)<N^{1+epsilon-o(1)}, then pi is a same-model upper-bound falsifier to any claimed LB_N(1+epsilon) for H_N^SAT.

## Definitions

- source object: a Psys_sym^dag transcript pi over H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, bit-explicit ordinary bEF lines, and FormulaEval DAG lines carrying visible selector and dependency certificates.
- target object: a nonuniform SIZE circuit for the same Boolean function H_N^SAT in the same SAT-occurrence theory and length regime, used only to refute the transcript's lower-bound claim when the circuit is below N^{1+epsilon-o(1)}.
- controlled interface: the closure algorithm K_dag takes the final LB_N line, follows verifier-visible parent pointers, enumerates every visible FormulaEval row, expands same-theory SAT occurrences, and charges all enumerator and row-expansion costs in Gamma_dag.
- target-preserving condition: closure, enumeration, and row expansion are deterministic and advice-free from (N,pi), preserve the same target function and nonuniform SIZE model, and do not use hidden SAT-truth advice or nonuniform hard-row selection.
- observable: K_idx(pi) is the set of distinct SAT-row indices reached by K_dag, U_N is the total certified row-discovery cost, X_N is the total same-theory row-expansion cost, and E_pi is the number of proof lines needing ordinary parser overhead.

## Assumptions

- Model: Psys_bEF^- ordinary rules satisfy the Gap98-SRhNormalForm parser with explicit bit fields, local verifiers, parent pointers, and eta/tau overhead already charged in Gamma_bEF.
- FormulaEval model: every semantic use is replaced by a transparent row-support certificate or is excluded from this lemma; full real semantic SAT remains quarantined at RealSATInfluenceRealizer_N.
- Quantifier regime: N ranges over the beta-zero parity-magnification lengths, q,rho,epsilon are fixed constants with epsilon>0, and all o(1) terms are uniform over the considered proof family.
- Uniformity/advice: K_dag, row enumeration, and expansion are computed from (N,pi) only; nonuniform advice is allowed only in the final SIZE upper bound, not in row discovery.
- Same-theory condition: each expanded row is the SAT-occurrence object actually used by H_N^SAT, not an extensional surrogate unless a visible quotient witness is charged.
- Non-claim boundary: the lemma is a scoped parser/falsifier theorem for transcripts, not a proof of P != NP or of unconditional circuit lower bounds.

## Equations

- beta_zero_carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)}`. Valid when: Valid when the source generator G_N is bit-explicit, advice-free, and fixed for the beta-zero length regime.
- least_closure_fixed_point: `K^{0}=Sink(pi),\quad K^{s+1}=K^{s}\cup Parents(K^{s})\cup VisibleRows(K^{s})\cup OccExpand(K^{s}),\quad K_{dag}(pi)=\bigcup_s K^{s}`. Valid when: Valid when every rule exposes computable parent pointers and every FormulaEval support certificate has an advice-free enumerator.
- gamma_dag_ledger: `\Gamma_{dag}(pi)=\Gamma_{bEF}(pi)+U_N(K_{dag})+X_N(K_{dag})`. Valid when: Applies after Gap98 ordinary-line costs are charged and transparent FormulaEval contributes only enumerated support and expansion costs.
- row_expansion_pressure: `X_N(K_{dag})\ge N^{1+o(1)}\,|K_{idx}(pi)|`. Valid when: Requires each reached SAT row to be expanded in the same occurrence model with polylog formula length overhead.
- same_model_upper_bound: `SIZE(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{dag}(pi)+O(E_pi N)`. Valid when: Valid when the parser circuit reuses the fixed generator, the charged transcript cone, and ordinary line verifiers without hidden semantic advice.
- falsifier_threshold: `N^{\rho+o(1)}+\Gamma_{dag}(pi)+O(E_piN)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)\text{ for this transcript model}`. Valid when: Applies only in the same nonuniform SIZE target model as the claimed lower-bound line of pi.
- support_density_corollary: `|K_{idx}(pi)|\ge N^{\epsilon-o(1)},\quad |K_{idx}(pi)|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Follows when rho, Gamma_bEF, U_N, and E_piN are all subthreshold and the LB_N line avoids the upper-bound falsifier.

## Attempted Derivation

- Initialize K^0 with the final LB_N sink fields and the H_N^SAT rows syntactically referenced by the final parity/lower-bound line.
- For an ordinary bEF predecessor, add its parent line identifiers, row-index encodings, verifier bit fields, and touched occurrence neighborhoods; Gap98-SRhNormalForm supplies the eta/tau contribution already counted in Gamma_bEF.
- For a transparent FormulaEval predecessor A, run its verifier-visible enumerator, insert every output row into K_idx, attach the same-theory SAT occurrence expansion for that row, and add all declared parent FormulaEval dependencies.
- Iterate the monotone closure until no new line, row, or occurrence field is added; finiteness of pi and finite row enumerators gives termination, and monotonicity gives leastness by induction over all prefix-closed support cones.
- Build the upper-bound circuit by hardwiring the nonuniform transcript skeleton, computing G_N at cost N^{rho+o(1)}, simulating every charged proof-line verifier in Gamma_dag, and wiring the O(E_pi N) ordinary row-level overhead.
- If the charged circuit is below N^{1+epsilon-o(1)}, the transcript cannot validly establish LB_N(1+epsilon) in the same SIZE model; this is the parser-to-circuit falsifier.
- For the negative half, choose the first FormulaEval line whose true influence is absent from K_dag; prefix minimality keeps all earlier lines fixed, and the unread private row or enable bit flips A while preserving all read bits.

Blocking gap: The derivation is complete for transparent Psys_sym^dag lines but still blocked for full semantic SAT FormulaEval by RealSATInfluenceRealizer_N: one must either uniformly list all real semantic influence rows with a charged R_N cost or accept the semantic-oracle quarantine.

## Falsifiers

- falsifier: a FormulaEval rule uses SAT extensionality or formula identity without an advice-free quotient/influence witness charged in Gamma_dag.
- falsifier: a row selector is membership-only or semantic and cannot enumerate K_idx except by a full scan that exceeds the claimed low-cost ledger.
- falsifier: K_dag depends on nonuniform advice, SAT-truth advice, or a hard-row selector not computable from (N,pi).
- falsifier: projected dDNNF FormulaEval hides large witness fiber entropy while charging only projected support size.
- falsifier: q<epsilon with subthreshold Gamma_bEF,U_N,E_piN and |K_idx|<=M_N=N^{q+o(1)}; the support-density inequality becomes impossible.
- falsifier: an unread enable bit or private row changes a FormulaEval value while all parser-read occurrence bits remain fixed.

## Learning

Cycle 121 makes the least closed support cone K_dag the proof-auditable invariant. Transparent FormulaEval is valid exactly because fixed-point closure enumerates and charges every influence before use; hidden semantic influence is a finite private-row falsifier. The q-trichotomy is now derived from X_N>=N^{1+o(1)}|K_idx|, while full semantic FormulaEval remains quarantined at RealSATInfluenceRealizer_N. This is a paper-level parser obstruction, not main P vs NP progress.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for L121.1 and L121.3.`
- Rationale: The top proof packet needs one concrete boundary case showing that K_dag is not just a restatement of transparency: projected support can be small while witness fibers or unread enable bits hide real influence.
- Situation seed: A projected guarded-dDNNF FormulaEval line selects rows j through auxiliary witnesses y; an additional enable bit e_y controls whether SAT(G_N(x,j)) participates in the row parity, and e_y is either exposed by the support certificate or hidden behind projection.
- Varied variable: projection fiber entropy ell=log_N W_N, where W_N is the number of accepting witnesses before duplicate row suppression.
- Held-fixed controls: H_N^SAT(x)=xor_{j<=N^{q+o(1)}} SAT(G_N(x,j)) and the same nonuniform SIZE target model are fixed., The proof system remains Psys_sym^dag with Gap98 bit-explicit ordinary rules and no advice in row discovery., The projected row count T_N, generator overhead N^{rho+o(1)}, and claimed LB_N(1+epsilon) threshold are fixed., SAT occurrence expansions are same-theory objects; no extensional SAT-truth oracle is allowed.
- Expected observation: When ell is charged by a certified projected enumerator or witness scan, Gamma_dag rises by U_N and the theorem remains valid; when ell is hidden, toggling an unread enable bit gives the first-bad-line countermodel.
- Transfer certificate needed: A formal duplicate-suppressing projected-row enumerator or an explicit witness-support scan with cost U_N, plus an influence-closure certificate proving every enable bit that can change FormulaEval is in K_dag before the line fires.

## Next Experiment

Write the audit-level K_dag pseudocode and run it on two instances: a projected-dDNNF FormulaEval line with fiber entropy ell charged by duplicate-suppressed enumeration, and the same line with one hidden enable bit to exhibit the first-bad-line falsifier.
