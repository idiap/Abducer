# cycle-0125

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For Psys_sym^dag extended by a declared bounded Tseitin self-reduction rule TSR_decl, the least prefix-closed support cone can be enlarged by all declared restriction children, and the Gamma_dag line induction remains valid with an extra charge N^{1+kappa+theta+o(1)}. Hence any proof of LB_N(1+epsilon) with rho<1+epsilon, prior Gamma_dag<N^{1+epsilon-o(1)}, E_pi<N^{epsilon-o(1)}, and kappa+theta<epsilon is a same-model upper-bound falsifier for that LB_N claim.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, formula length L_N=(log N)^d, and source assertion LB_N(1+epsilon): C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)}.
- target object: a restricted parser-to-circuit falsifier theorem for Psys_sym^dag+TSR_decl proofs of LB_N, not a proof of P != NP or NP not subset P/poly.
- controlled interface: TransparentRowSupport_N plus a declared TSR rule whose syntax lists each parent row, branch word, restricted child formula, row index, occurrence-neighborhood certificate, and enumerator code before the semantic equality is used.
- target-preserving condition: beta=0 polylog SAT-query length, same nonuniform SIZE model, advice-free row enumeration, same-theory occurrence expansion, generator overhead N^{rho+o(1)}, and no hidden branch-pruning or semantic row advice.

## Assumptions

- N ranges over valid carrier lengths; q,rho,kappa,theta,epsilon are fixed constants and all o(1) terms are uniform along valid lengths.
- The Psys_bEF^- parser and bounded-SR_h normal form from the prior packet are already valid and contribute Gamma_bEF(pi).
- The proof DAG is acyclic; reachable FormulaEval dependencies are computed from the final LB_N line, not from the full selector zoo.
- There are T_N=N^{kappa+o(1)} reachable TSR_decl invocations, and each declared restriction DAG has at most R_N=N^{theta+o(1)} child rows after duplicate row identifiers are merged.
- Every declared child row has a bit-explicit row identifier and an occurrence expansion whose circuit cost is O(N L_N^{O(1)}).
- Residual bad source rows E_pi are patched only by equality circuits, costing O(E_pi N), with no SAT-truth advice.

## Equations

- declared_tsr_closure: `K_{TSR}(\pi)=\operatorname{lfp}(K_{dag}(\pi)\cup Child_{TSR}^{decl}(K)),\qquad |K_{TSR}\setminus K_{dag}|\le T_N R_N=N^{\kappa+\theta+o(1)}.`. Valid when: Valid when the TSR rule syntax declares every restriction child and the fixed-point operator follows only reachable proof dependencies.
- gamma_tsr_charge: `\Gamma_{TSR}(\pi)=\Gamma_{dag}(\pi)+U(K_{TSR})+X(K_{TSR}\setminus K_{dag}),\qquad X(\Delta K)\le N\,|\Delta K|L_N^{O(1)}\le N^{1+\kappa+\theta+o(1)}.`. Valid when: Valid when row enumeration is advice-free and every declared child is expanded in the same occurrence-level proof theory.
- parser_to_circuit_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{TSR}(\pi)+O(E_\pi N).`. Valid when: Applies after the line induction supplies a complete charged transcript for all proof values used by the final carrier circuit.
- subthreshold_falsifier_window: `\rho<1+\epsilon,\quad \Gamma_{dag}(\pi)<N^{1+\epsilon-o(1)},\quad E_\pi<N^{\epsilon-o(1)},\quad \kappa+\theta<\epsilon\ \Longrightarrow\ C(H_N^{SAT})<N^{1+\epsilon-o(1)}.`. Valid when: Valid when all four exponent inequalities hold with a common positive margin along the same valid length subsequence.

## Attempted Derivation

- Initialize K to the final LB_N line, its bit-explicit Psys_bEF^- dependencies, and the least reachable FormulaEval support from the existing K_dag fixed-point algorithm.
- For each transparent FormulaEval line, add the enumerated row set or charge the full scan; add all later symbolic uses by prefix closure.
- For each reachable TSR_decl line, read its parent row id, branch-word field, child restricted-formula bit fields, child row ids, and occurrence-neighborhood certificates; add every child row to K before the TSR equality is evaluated.
- Iterate until no newly added row can be used by a later proof line. Termination follows from the finite proof DAG and finite declared child DAGs, not from semantic SAT truth.
- Run line induction: bEF lines use Gamma_bEF; transparent FormulaEval lines use U(K_dag)+X(K_dag); TSR_decl lines use the declared children and the Boolean Tseitin self-reduction equality over charged SAT labels.
- Build the falsifying circuit for H_N by composing the generator, the charged transcript evaluator, and equality patches for E_pi residual source rows. This gives C(H_N)<=N^{rho+o(1)}+Gamma_TSR+O(E_pi N).
- Apply the exponent audit: if kappa+theta<epsilon and the previous Gamma_dag and residual terms are subthreshold, the alleged LB_N(1+epsilon) proof produces a smaller same-model circuit, so the proof certificate is invalid for that LB_N claim.

Blocking gap: RealSATInfluenceRealizer_N^arb for hidden semantic branch-pruning: the derivation does not extract unlisted rows whose relevance is certified only by actual SAT semantics.

## Falsifiers

- Declared TSR threshold collapse: kappa+theta>=epsilon makes the extra row expansion too large to refute LB_N(1+epsilon).
- First-hidden-branch falsifier: a pruned restriction child influences a later line but is absent from K_TSR, so two private-row worlds share the transcript and differ on the conclusion.
- Unread-enable-bit falsifier: a selector bit can activate a row after the parser fixed point without being included in the visible support cone.
- Nonuniform leakage falsifier: the row enumerator uses advice depending on SAT labels or on the final hardwired carrier truth table.
- Positive-beta substitution falsifier: any return to target queries of length N^beta obeys q+beta c and cannot exclude all SAT circuit exponents.

## Learning

Cycle 125 converts the TSR semantic boundary into a theorem-shaped split. Declared bounded TSR is validly absorbed by the least-support parser with charge N^{1+kappa+theta+o(1)}, giving a falsifier exactly when kappa+theta<epsilon. Hidden semantic branch-pruning is not a free extension of FormulaEval: it has a first-hidden-row private-row no-go unless a nonrelativizing RealSATInfluenceRealizer_N^arb supplies charged influence rows. This is a scoped parser/falsifier contribution, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the declared-versus-hidden TSR boundary.`
- Rationale: The branch already has the abstract K_dag theorem; the remaining decision is whether bounded TSR is a charged transparent extension or an unchargeable semantic escape. Varying one expansion exponent tests the exact threshold without broadening carriers.
- Situation seed: Take H_N^SAT(x)=xor_{j<=N^q} SAT(G_N(x,j)) with L_N=(log N)^d, and add a TSR_decl rule that for each reachable root row lists a bounded restriction DAG of size N^theta; compare with a hidden-pruning rule that lists only branches certified useful by SAT semantics.
- Varied variable: theta, the declared restriction-DAG expansion exponent per reachable TSR root.
- Held-fixed controls: beta=0 polylog target-query length and the same nonuniform SIZE circuit model., Generator overhead N^{rho+o(1)} and prior Gamma_dag subthreshold assumptions., Advice-free row identifiers, occurrence-neighborhood certificates, and same-theory expansion for all declared rows., Root count exponent kappa and residual patch count E_pi are fixed while theta varies.
- Expected observation: For theta<epsilon-kappa the declared TSR proof is automatically a source-LB falsifier; at theta=epsilon-kappa the proof sits at the critical support-density boundary; for theta>epsilon-kappa the parser theorem remains valid but no longer yields a subthreshold contradiction. Hidden pruning fails at every theta unless a real-SAT-specific realizer lists or proves away the hidden influences.
- Transfer certificate needed: A uniform RealSATInfluenceRealizer_N^TSR certificate: from proof syntax and N, before using the TSR semantic line, enumerate an influence-closed row set R_A, give occurrence expansions for all rows, charge N|R_A|L_N^{O(1)}, and prove same-theory correctness without SAT-truth advice.

## Next Experiment

Write the referee-auditable TSR_decl proof block: child-row bit fields, fixed-point pseudocode, Gamma_TSR induction case, and a two-world hidden-pruning countermodel with a named first hidden child row r_star.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For bounded semantic Tseitin/SR FormulaEval, a same-model parser transfer is valid exactly in the annotated row-cover interface: if every influencing row is enumerated and prefix-spliced, Gamma_tSR charges the proof; if a row can influence the semantic line without visible cover, the private-row/unread-enable-bit construction is a finite falsifier to surface occurrence completion.

## Definitions

- source object: Psys_sym^uSR/tSR FormulaEval lines for beta-zero carrier H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), N=2^n, M_N=N^{q+o(1)}.
- target object: same nonuniform SIZE upper-bound falsifier for a claimed LB_N(1+epsilon) lower-bound proof, or forced row-equivalent support in transparent proofs.
- controlled interface: RealSATInfluenceRealizer_N enumerates all rows influencing a semantic FormulaEval line, verifies local bounded-SR_h neighborhoods, and emits same-theory row-expanded bEF material before the line is used.
- target-preserving condition: the enumerator is deterministic, advice-free, prefix-scoped, independent of SAT truth values, charges R_N in Gamma, and uses fresh extension variables so the circuit/proof model is unchanged.
- observable: FErow(A) is the set of SAT-row indices whose row bit can change the truth of the FormulaEval assertion A after fixing all visible non-row syntax.
- countermodel carrier: a hidden enable bit or unannotated selector chooses a first omitted row j* while leaving the visible transcript and all charged rows unchanged.

## Assumptions

- Nonuniform Boolean SIZE is the target class; the proof-system result is a parser/falsifier theorem, not a many-one reduction and not a P != NP proof.
- Length regime is N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, size(G_N)=N^{rho+o(1)}, with rho<1+epsilon.
- Annotated tSR lines expose row-cover records containing row index, local occurrence neighborhood, parent pointer, SR_h depth, and a checkable reason that the row is in FErow(A).
- Same-theory prefix splicing uses fresh extension variables and inserts the row-expanded bEF derivation before the semantic FormulaEval line is invoked.
- No hidden advice: the row set must be computable from N, the proof prefix, and displayed FormulaEval syntax, not from SAT truth values or a nonuniform semantic oracle.

## Equations

- influence_set: `\mathrm{FErow}(A)=\{j<M_N:\exists z,z'\; z_{-j}=z'_{-j}\wedge A(z)\ne A(z')\}.`. Valid when: Valid when a FormulaEval line A is interpreted as a Boolean functional of the M_N SAT-row bits under a fixed visible proof prefix and fixed non-row syntax.
- annotated_charge: `\Gamma_{tSR}(\pi)=\Gamma_{bEF}(\pi)+U_N+X_N+N\cdot R_N+O(|\pi|\operatorname{polylog}N).`. Valid when: Applies when annotated row covers enumerate every FErow member before use and each listed row is expanded into bEF clauses with prefix-fresh variables.
- parser_falsifier_bound: `N^{\rho+o(1)}+\Gamma_{tSR}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow C(H_N^{SAT})<N^{1+\epsilon-o(1)}.`. Valid when: Requires the target-preserving complexity-class transfer where the generator circuit and parsed transcript are both nonuniform SIZE circuits over the same input length.
- forced_support: `\widehat S_{eff}(\pi)=\Gamma_{tSR}(\pi)/N\ge N^{\epsilon-o(1)}.`. Valid when: Valid after soundness of the claimed LB_N(1+epsilon) proof is combined with the parser falsifier inequality and rho is below 1+epsilon.

## Attempted Derivation

- Define FErow(A) extensionally as row-bit influence under a fixed proof prefix; this converts semantic FormulaEval support from a surface occurrence count into a functional dependency set.
- For annotated tSR, require each FormulaEval line to display a cover C_A with row indices, occurrence-neighborhood lists, parent pointers, and bounded-SR_h local checks; the worklist accepts only rows whose certificates verify from syntax.
- Prefix-splice the row-expanded bEF derivation for each j in C_A immediately before A, using fresh extension variables; by line induction, the parsed transcript charge is Gamma_bEF+U_N+X_N+N R_N+lower-order verifier overhead.
- Compose the parsed transcript with the generator circuit for G_N; if N^{rho+o(1)}+Gamma_tSR(pi)<N^{1+epsilon-o(1)}, the same nonuniform SIZE model computes H_N^SAT below the claimed LB_N threshold, giving a valid falsifier to the proof claim.
- For unannotated tSR, choose the first row j* whose hidden enable bit changes A but which is not in the visible support K; construct z,z' agreeing on K and all displayed fields, differing only at j*, so the parser transcript is bisimilar while the semantic FormulaEval value and xor carrier differ.
- Thus annotated tSR is promoted as a restricted RealSATInfluenceRealizer_N theorem, while arbitrary semantic FormulaEval remains blocked at uniform FErow enumeration rather than at generic barrier folklore.

Blocking gap: For arbitrary semantic FormulaEval, formula equivalence, compression, or opaque SAT semantics may hide FErow(A); no advice-free algorithm is known that enumerates all influencing rows from displayed syntax while preserving the N*R_N charge.

## Falsifiers

- First-omitted-row falsifier: an unannotated tSR FormulaEval line has j* in FErow(A) but j* absent from K_dag(pi), so two bisimilar transcripts disagree on the carrier parity.
- Unread-enable-bit falsifier: a hidden selector bit gates a private row while surface syntax and charged rows remain unchanged, invalidating occurrence-only parsing.
- q<epsilon source-ceiling falsifier: C(H_N^SAT)<=N^{1+q+o(1)} contradicts any claimed LB_N(1+epsilon) when q<epsilon-o(1), independent of proof-system syntax.
- Projected-dDNNF missing-cover falsifier: projection hides a reachable row unless a RowCoverCertificate_N lists it and pays the corresponding Gamma_rc charge.
- Natural-property falsifier probe: if the transparent checker becomes large, constructive, and useful against SIZE(m^k), PRF pressure applies; hidden semantic support escapes constructivity but then loses valid transfer.

## Learning

Cycle 125 converts the tSR semantic boundary into a sharper rule-level theorem/countermodel pair: annotated bounded-SR_h FormulaEval is a valid target-preserving interface because all influencing rows are listed and charged, while an unannotated hidden row is a finite falsifier to any occurrence-only parser. This is route-level proof-system certification, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for RealSATInfluenceRealizer_N.`
- Rationale: The branch already has the abstract TRS theorem; the decisive issue is whether a concrete semantic tSR rule can hide an influencing row without paying Gamma, so a finite row-table experiment tests the transfer interface directly.
- Situation seed: A padded beta-zero SAT-parity instance with M_N=N^{q+o(1)} rows and one semantic bounded-SR_h FormulaEval line whose selector is either annotated by a visible row cover or controlled by an unread private enable bit for row j*.
- Varied variable: Row-cover visibility v in {0,1}: v=1 exposes j* with its occurrence-neighborhood certificate, while v=0 hides j* behind semantic FormulaEval evaluation.
- Held-fixed controls: The carrier H_N^SAT(x)=xor_j SAT(G_N(x,j)) and generator size N^{rho+o(1)} are fixed., The target class is the same nonuniform SIZE model on the same length N., The parser is deterministic, advice-free, and prefix-scoped with fresh extension variables., The proof length exponent tau and row count exponent q are held fixed while only support visibility changes.
- Expected observation: At v=1 the worklist charges N for row j* and the Gamma_tSR induction remains valid; at v=0 two row tables agree on the visible transcript but flip H_N^SAT, proving a hidden-row falsifier.
- Transfer certificate needed: A formal proof that the visible annotation enumerates all of FErow(A), that each row expansion is same-theory bEF material, and that no SAT-truth or nonuniform advice enters before the semantic rule is used.

## Next Experiment

Instantiate the worklist on a three-row bounded-SR_h toy FormulaEval line: compute FErow(A), run the annotated cover checker, calculate Gamma_tSR, then delete the certificate for the first influencing row and verify the bisimulation/parity-flip falsifier.

# MCSP / Meta-Complexity Carrier Transfer supporting FormulaEval parser boundary

## Candidate Lemma

For explicit lengths N, let pi be a bit-explicit Psys_sym^time transcript for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), M_N=N^{q+o(1)}. If every FormulaEval line is timestamped-transparent before first semantic use, then the least prefix-closed support cone K_time(pi) is computable from proof bits, Gamma_time(pi)=Gamma_bEF(pi)+U_time+X_time+T_time is derived by line induction, and any transcript claiming LB_N(1+epsilon) with N^{rho+o(1)}+Gamma_time(pi)+O(E_pi N)<N^{1+epsilon-o(1)} is a same-model upper-bound falsifier, not a proof of P != NP.

## Definitions

- source object: a bit-explicit Psys_sym^time proof transcript pi whose lines are bEF/SR_h rules plus FormulaEval lines over SAT(G_N(x,j)).
- target object: a nonuniform Boolean SIZE upper bound for the target truth-table family H_N^SAT, compared against the claimed LB_N(1+epsilon) threshold.
- controlled interface: timestamped transparent FormulaEval support, consisting of visible selector code, row enumerator or full-scan declaration, parent pointers, influence witnesses, same-theory occurrence expansion, and no hidden row advice.
- target-preserving condition: every row that can influence a FormulaEval line is enumerated and charged in the proof prefix before that line is used; the parser remains advice-free and in the same SAT row theory.
- bridge observable: K_time(pi,ell) is the least proof-prefix reachable support cone at line ell, not the after-the-fact global support set.
- charge observable: U_time counts row-discovery/enumerator work, X_time counts same-theory row expansion, and T_time counts timestamp and parent-pointer verification overhead.

## Assumptions

- Circuit model: nonuniform Boolean SIZE over the N-bit external input x; the conclusion is an upper-bound falsifier inside this model only.
- Length regime: M_N=N^{q+o(1)}, G_N has uniform generator overhead N^{rho+o(1)}, and all o(1) terms are along the explicit length subsequence.
- Proof model: ordinary bEF and bounded-SR_h lines already satisfy the Gap98-SRhNormalForm ledger and contribute exactly Gamma_bEF(pi).
- Uniformity/advice condition: the parser reads only N and the proof prefix; selectors, quotient witnesses, row lists, and influence witnesses are not supplied as nonuniform advice.
- Same-theory condition: each expanded row is a SAT(G_N(x,j)) occurrence in the original row theory, not an external semantic SAT oracle value.
- Semantic boundary: full semantic FormulaEval is admitted only through a RealSATInfluenceRealizer_N that lists all influencing rows before use; otherwise it is quarantined as a semantic-oracle escape.
- Barrier status: this is a restricted parser/falsifier theorem, not a natural-property lower bound and not a relativizing proof of P vs NP.

## Equations

- Ktime_fixed_point: `K_{time}(\ell)=\mu S\supseteq K_{time}(<\ell)\cup VisSupp(\ell)\;[Parent(S)\cup Infl_{\ell}(S)\subseteq S]`. Valid when: Valid when the FormulaEval line exposes selector code, parent pointers, and influence witnesses inside the proof prefix before line ell is checked.
- Gamma_time_ledger: `\Gamma_{time}(\pi)=\Gamma_{bEF}(\pi)+\sum_{\ell\in FE(\pi)}(U^{new}_{\ell}+X^{new}_{\ell}+T^{stamp}_{\ell})`. Valid when: Applies after incremental support discovery is deduplicated by K_time and every charged row expansion remains in the same SAT occurrence theory.
- parser_upper_bound: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{time}(\pi)+O(E_{\pi}N)`. Valid when: Requires the generator overhead, bit-explicit line parser, and all FormulaEval support charges to be uniform and advice-free at length N.
- low_cost_transcript_falsifier: `N^{\rho+o(1)}+\Gamma_{time}(\pi)+O(E_{\pi}N)<N^{1+\epsilon-o(1)}\Rightarrow \pi\text{ is not a valid proof of }LB_N(1+\epsilon)`. Valid when: Valid when LB_N(1+epsilon) asserts a same-model nonuniform SIZE lower bound for H_N^SAT at the stated threshold.
- support_density_charge: `X_{time}\ge N^{1+o(1)}\,|K_{idx}(\pi)|`. Valid when: Applies when each reachable row index in K_idx is expanded into its N-bit row occurrence representation before semantic use.

## Attempted Derivation

- Initialize parser state with ordinary bEF/SR_h line data and empty FormulaEval support; existing Gap98-SRhNormalForm supplies Gamma_bEF for these lines.
- At each line ell compute K_time(pi,ell) by monotone closure over visible row certificates, parent pointers, quotient witnesses, and declared influence lists contained in the proof prefix.
- For an ordinary proof rule, preserve the invariant that any two completions agreeing on K_time and prior parsed bits give the same line value; add only the Gamma_bEF charge.
- For a transparent FormulaEval line, enumerate new row indices or pay a full-scan charge, expand each row in the same SAT occurrence theory, and add U_new+X_new+T_stamp to Gamma_time.
- Use influence closure to show semantic stability: no uncharged row flip can change the FormulaEval line because every influential row is already in K_time(pi,ell^-).
- Compose the generator circuits for G_N with the charged row expansions and the bit-explicit proof parser to obtain C_SIZE(H_N^SAT)<=N^{rho+o(1)}+Gamma_time(pi)+O(E_pi N).
- Compare the obtained upper bound with the claimed LB_N(1+epsilon). If the bound is subthreshold, the transcript is a finite same-model falsifier of that lower-bound claim.
- For the Tseitin/self-reduction rule, explicit quotient plus explicit branch enumeration satisfies the transparent clause; SAT-truth-dependent branch pruning produces a first hidden branch and triggers the private-row countermodel.

Blocking gap: Full semantic FormulaEval with truth-dependent influence selection still lacks RealSATInfluenceRealizer_N. The named gap is prefix-visible advice-free enumeration of all rows whose SAT value can affect the semantic inference before that inference is used.

## Falsifiers

- Prefix-latency falsifier: a row certificate appearing after its first semantic use lets an unread enable bit flip the FormulaEval value while preserving the parsed prefix.
- Hidden projection-fiber falsifier: projected-dDNNF support with unlisted witnesses can hide an influential projected row unless the projected enumerator or witness support is charged.
- SAT-truth pruning falsifier: a bounded self-reduction that omits branches based on semantic SAT truth is not a valid transparent realizer without prefix branch certificates.
- Nonuniform selector falsifier: choosing the hard or influential row by advice gives only nonuniform row hardness and does not transfer to an advice-free language lower-bound packet.
- Subthreshold transcript falsifier: if rho, Gamma_time, and E_pi N all stay below N^{1+epsilon-o(1)}, the claimed LB_N(1+epsilon) proof yields its own same-model upper bound.

## Learning

Cycle 125 sharpens the theorem pair: the valid transfer certificate is zero prefix latency for influential FormulaEval support, not merely eventual support discovery. For the concrete Tseitin/self-reduction semantic rule, explicit branch enumeration is transparent and charged, while SAT-truth branch pruning is a named semantic-oracle escape with a private-branch falsifier. This advances the paper parser obstruction only, not P vs NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the timestamped support theorem.`
- Rationale: The current proof-delivery risk is not another abstract FormulaEval restatement; it is whether prefix visibility, rather than global support visibility, is the exact transfer certificate for the parser-to-circuit simulation.
- Situation seed: DelayedEnable projected-dDNNF FormulaEval over H_N^SAT: a proof line uses a projected row selector whose enable bit for row r is certified either before the line, after the line, or never; all other selector syntax is visible.
- Varied variable: Prefix latency lambda, the number of proof lines between first semantic use of row r and the first visible certificate or expansion for r.
- Held-fixed controls: M_N=N^{q+o(1)} and generator overhead N^{rho+o(1)} are fixed., The target lower-bound claim remains LB_N(1+epsilon) in the same nonuniform SIZE model., The parser is advice-free and may read only the proof prefix before each line., The row theory is the same SAT(G_N(x,j)) occurrence theory; no external SAT oracle values are inserted.
- Expected observation: At lambda=0 the row is charged and the Gamma_time induction is valid. For any lambda>0 with r influential, two same-prefix completions differ only on the unread enable or row value and flip the FormulaEval line, giving a finite hidden-support falsifier.
- Transfer certificate needed: A formal prefix-visible RealSATInfluenceRealizer_N proving that every influential row is enumerated and charged before use; absent this certificate, the thought experiment may only justify the countermodel, not a positive transfer.

## Next Experiment

Write the paper-ready L125 K_time theorem: give closure pseudocode, prove the line-induction invariant, instantiate the DelayedEnable projected-dDNNF counterexample, and compute the Tseitin/self-reduction charge R_N for explicit versus truth-pruned branches.
