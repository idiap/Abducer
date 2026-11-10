# cycle-0131

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For Psys_bEF^- plus TransparentRowSupport_N and complete declared bounded-TSR_{kappa,theta} rules, the least reachable support cone K_DTSR(pi) gives a valid same-model parser-to-circuit falsifier: any sound proof pi of LB_N(1+epsilon) must have N^{rho+o(1)}+Gamma_DTSR(pi)+O(E_pi N) >= N^{1+epsilon-o(1)}.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, polylog formula length L_N=(log N)^d, and generator circuit size N^{rho+o(1)}.
- target object: the route-level target is a same-model SIZE upper-bound falsifier for LB_N(1+epsilon), not a proof of P != NP or a lower bound for SAT.
- controlled interface: a Psys_bEF^-+TransparentRowSupport_N+DeclaredTSR_{kappa,theta} proof pi is parsed into the least prefix-closed row/child support cone K_DTSR(pi) and charged transcript Gamma_DTSR(pi).
- target-preserving condition: beta=0 polylog SAT queries, advice-free visible row enumeration, complete child declarations before semantic use, same nonuniform SIZE model, and subthreshold charges below N^{1+epsilon-o(1)}.
- row identifier: (line id, N-bit source key a, slot j in [M_N], child-path p, polarity bit, formula-hash pointer).
- declared TSR field: each rule instance lists parent row, restriction variable or Tseitin gate, branch literal, affected occurrence-neighborhood list, child formula hash, and child row pointer.
- least support cone: K_DTSR(pi) is the least fixed point containing rows used by the final LB_N line and closed under EF parents, FormulaEval influences, SATeq links, bounded-SR_h leaves, and declared TSR children.

## Assumptions

- Circuit model is nonuniform SIZE over Boolean circuits; the generator G_N and all parsers are counted in the same model.
- Length regime has M_N=N^{q+o(1)}, L_N=(log N)^d with fixed d>1, and all o(1) terms are uniform over the accepted length sequence.
- The bounded-SR_h part is bit-explicit and has visible eta,tau overhead already included in Gamma_bEF(pi).
- Each declared TSR rule has at most N^{theta+o(1)} child restrictions across each of N^{kappa+o(1)} active syntactic rule families, with no SAT-truth advice selecting children.
- TransparentRowSupport_N supplies either an advice-free row enumerator or a full-scan charge, plus same-theory occurrence expansion for every surfaced FormulaEval influence.
- E_pi is the number of residual bad source rows after parsing; equality patching one source row costs O(N) gates.
- LB_N(1+epsilon) means C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)} in the same source model; the theorem is contraposed as an upper-bound falsifier.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N}\mathrm{SAT}(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad L_N=(\log N)^d.`. Valid when: Valid when the source carrier is the beta-zero generated parity family with uniformly generated polylogarithmic SAT instances.
- bounded_SR_charge: `B_{SR_h}(\pi)\le N^{q+\eta+\tau+o(1)}.`. Valid when: Valid when the bounded self-reduction rule exposes every touched occurrence neighborhood and the eta,tau overheads are syntactic parser costs.
- declared_TSR_charge: `B_{DTSR}(\pi)=\sum_{r\in DTSR(\pi)} N\cdot |A_r|\cdot N^{o(1)}\le N^{1+\kappa+\theta+o(1)}.`. Valid when: Applies when every TSR child in every active rule family is declared before use and row expansion is charged in the source length N.
- gamma_DTSR: `\Gamma_{DTSR}(\pi)=\Gamma_{bEF}(\pi)+U(K_{DTSR})+X(K_{DTSR})+B_{DTSR}(\pi).`. Valid when: Valid when K_DTSR is the least prefix-closed support fixed point and all FormulaEval, SR_h, and TSR influences are surfaced.
- upper_bound_falsifier: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{DTSR}(\pi)+O(E_\pi N).`. Valid when: Requires the line-induction parser to evaluate every proof line on surfaced rows and to patch only the E_pi residual source rows.
- subthreshold_contradiction: `N^{\rho+o(1)}+\Gamma_{DTSR}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon).`. Valid when: Valid when LB_N is interpreted in the same nonuniform SIZE model and no semantic rule uses hidden advice or uncharged SAT influence.

## Attempted Derivation

- Encode every proof-line dependency by visible fields: line pointer, rule tag, source key a, slot j, child path p, parent pointers, polarity, formula hash, and touched occurrence-neighborhood list.
- Compute K_DTSR(pi) by a worklist from the final LB_N line: add EF parents, SATeq quotient links, TransparentRowSupport_N influences, bounded-SR_h leaves, and every declared TSR child; terminate because pi is finite and all selectors are syntactic or full-scan charged.
- For a bEF or SATeq line, reuse the existing Gamma_bEF induction: evaluating the parent row values and link certificates suffices to evaluate the child line on all rows in the cone.
- For a bounded-SR_h line, charge B_SR_h<=N^{q+eta+tau+o(1)} because the verifier lists the bounded depth path, row-index encoding, and occurrence-neighborhoods touched by each restriction.
- For a declared TSR line, the child list A_r is part of the syntax; expanding each child over N source keys costs N|A_r|N^{o(1)}, so all TSR instances cost at most N^{1+kappa+theta+o(1)}.
- For a transparent FormulaEval line, use its advice-free enumerator or full scan to add U(K_DTSR), then charge X(K_DTSR) for same-theory occurrence expansion of the listed rows.
- Induct over the proof DAG to build a circuit of size N^{rho+o(1)}+Gamma_DTSR(pi) that agrees with H_N except possibly on E_pi residual source rows; add O(E_pi N) equality patches.
- Contrapose: if the resulting size is below N^{1+epsilon-o(1)}, the claimed LB_N(1+epsilon) is false in the same source model, so any sound certificate must exceed the threshold.
- Necessity check: if a later line depends on an unlisted TSR child, construct two worlds agreeing on K_DTSR but differing on that child; the visible parser outputs the same value while the enabled carrier parity differs.

Blocking gap: The restricted declared-TSR theorem has no current internal gap. The full semantic pruning case remains blocked exactly at RealSATInfluenceRealizer_N^arb: an advice-free nonrelativizing procedure must list all real-SAT influencing rows and charge them before use.

## Falsifiers

- first-unlisted-child private-row falsifier for hidden TSR branch pruning
- unread-enable-bit falsifier for non-closed FormulaEval influence
- q<epsilon support-density falsifier when reachable rows are too sparse
- positive-beta substitution cap N^{q+beta c+o(1)} for black-box target-circuit interfaces
- nonuniform leakage through SAT-truth advice in row selection
- threshold collapse when rho, Gamma_DTSR, or E_pi N reaches N^{1+epsilon-o(1)}

## Learning

Cycle 131 turns declared bounded TSR into an auditable fixed-point rule case: complete child declarations are sufficient for the Gamma_DTSR parser and necessary up to the first-unlisted-child falsifier. The valid contribution is a route-level theorem/countermodel boundary for beta-zero parity magnification certificates, not progress on the main P vs NP conjecture.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The branch already has a promoted transparent-support theorem; the remaining mathematical uncertainty is whether declared TSR charges are necessary and sufficient, which is best tested by varying the child-declaration exponent while preserving the beta-zero target bridge.
- Situation seed: Take H_N^SAT(x)=xor_{j<=N^q} SAT(G_N(x,j)) with L_N=(log N)^d and a Psys_bEF^- proof using N^{kappa} declared TSR parent families; each parent either declares all N^{theta} restriction children or hides one pruning branch behind an unread enable bit.
- Varied variable: theta, the exponent of declared TSR children per active rule family, with kappa fixed.
- Held-fixed controls: beta=0 polylog SAT query length and generator size N^{rho+o(1)}, same nonuniform SIZE source and target model, complete TransparentRowSupport_N for non-TSR FormulaEval lines, no SAT-truth advice in row selection, residual error budget E_pi<N^{epsilon-o(1)}
- Expected observation: When kappa+theta<epsilon and all children are declared, B_DTSR=N^{1+kappa+theta+o(1)} stays below the LB threshold and the parser yields a valid upper-bound falsifier. When a single reachable child is hidden, two visible-identical worlds with different carrier parity refute the surface parser regardless of the nominal exponent.
- Transfer certificate needed: An advice-free child-row enumerator or a nonrelativizing RealSATInfluenceRealizer_N^arb that outputs an influence-closed row set, occurrence-neighborhood certificates, and the charged B_DTSR term before the semantic TSR rule is used.

## Next Experiment

Run the reviewer audit on L131.1: instantiate one toy projected-dDNNF FormulaEval line plus one declared TSR parent with two restriction children, compute K_DTSR by the worklist, verify Gamma_DTSR numerically as N^{1+kappa+theta+o(1)}, then flip the first unlisted child in the hidden-pruning variant to validate the private-row falsifier.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For Psys_sym^TRS, every accepted proof pi of LB_N(1+epsilon) for H_N^SAT either pays row-equivalent support S_hat_TRS(pi)>=N^{epsilon-o(1)} or yields a same-model SIZE upper-bound falsifier to the asserted lower bound. This is a restricted proof-system theorem, not a P != NP claim.

## Definitions

- source object: H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), with N=2^n, M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and a Psys_sym^TRS proof pi asserting LB_N(1+epsilon).
- target object: the same nonuniform Boolean SIZE_N threshold C(H_N^SAT)>N^{1+epsilon}; the parser target is a circuit upper-bound falsifier or forced row-equivalent support.
- controlled interface: TransparentRowSupport_N requires visible FormulaEval selector code, RowEnum_N or full-scan charge, influence-closed row sets, same-theory row expansion templates, prefix-scoped fresh extension variables, and no hidden advice.
- target-preserving condition: every FormulaEval line must be conservatively prefix-spliced into row-expanded bEF material before the semantic rule is used, with all influencing rows charged in the ledger and no oracle access to real SAT truth.
- K_TRS(pi) is the least reachable row set obtained from the final LB_N line by following proof-visible bEF touches, FormulaEval parent pointers, selector certificates, and influence-closure annotations.
- U_N(pi) is the bit cost of proof-visible row enumeration or full scans; X_N(pi)=N|K_TRS(pi)|+O(N E_pi) is the row-expansion bit debt; Gamma_bEF(pi) is the previously audited bit-explicit bEF transcript charge.

## Assumptions

- Model: nonuniform Boolean SIZE on the N-input truth table slice; reductions are parser/simulation reductions, not many-one reductions from SAT.
- Regime: epsilon>0 is fixed, N tends to infinity, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, and size(G_N)=N^{rho+o(1)} with rho<1+epsilon.
- Uniformity: the TRS verifier and K_TRS worklist are deterministic and advice-free from N and pi; selector extensionality is checked from proof-visible code or charged by full scan.
- Same-theory condition: prefix splicing introduces fresh extension variables scoped before the consuming FormulaEval line and does not invoke a stronger proof system.
- Soundness cutoff: LB_N(1+epsilon) means a claimed lower bound against the same SIZE_N model in which the parser constructs the upper-bound falsifier.
- Naturalness status: the theorem is proof-system-specific; it becomes a natural-proofs object only if the extracted acceptance condition is large, poly(N)-constructive, and useful for the named SIZE class.

## Equations

- least-support-fixed-point: `K_TRS(pi)=mu K . (Touch_bEF(pi) union Influence_FE(pi,K))`. Valid when: Valid when all FormulaEval dependencies expose parent pointers, selector certificates, and influence-closure annotations to the deterministic worklist.
- transparent-charge-ledger: `Gamma_TRS(pi)=Gamma_bEF(pi)+U_N(pi)+X_N(pi)+O(N E_pi)`. Valid when: Valid when each transparent FormulaEval line is prefix-spliced into row-expanded bEF material with fresh variables and charged rows.
- parser-upper-bound: `C(H_N^SAT) <= N^{rho+o(1)} + Gamma_TRS(pi) + N^{o(1)}`. Valid when: Applies after the generator circuit, parsed transcript, and row expansions all live in the same nonuniform SIZE model.
- forced-row-equivalent-support: `S_hat_TRS(pi)=(Gamma_bEF(pi)+U_N(pi))/N + |K_TRS(pi)| + E_pi >= N^{epsilon-o(1)}`. Valid when: Requires pi to be sound for LB_N(1+epsilon) and rho<1+epsilon so a smaller ledger would be a falsifier.
- visible-row-density: `|K_TRS(pi)|/M_N >= N^{epsilon-q-o(1)}`. Valid when: Valid when Gamma_bEF(pi)/N, U_N(pi)/N, and E_pi are lower order than N^{epsilon} in the forced-support inequality.

## Attempted Derivation

- Define the TRS line record: kind, parent line ids, selector or scan code, RowEnum_N output convention, extensionality certificate, influence-row list, row-expansion template, and freshness interval for extension variables.
- Compute K_TRS(pi) by a monotone worklist from the final LB_N line. Add bEF-touched rows directly; for FormulaEval lines add exactly the rows produced by visible selectors or by full scan; reject if a semantic dependency lacks a certificate.
- For each accepted FormulaEval line, splice a prefix block using fresh extension names. The block materializes the listed rows, proves the local FormulaEval assertion in bEF syntax, and links the result back to the original line.
- Run line induction. Ordinary bEF, SATeq, and bounded-SR_h lines contribute Gamma_bEF. Transparent FormulaEval contributes U_N for enumeration and X_N for row materialization. Freshness gives conservative same-theory replacement.
- Build the same-model circuit upper bound from G_N plus the parsed charged transcript. If N^{rho+o(1)}+Gamma_TRS(pi)<N^{1+epsilon-o(1)}, the asserted LB_N(1+epsilon) is falsified inside the same SIZE_N target model.
- Contrapose for sound accepted proofs: since rho<1+epsilon, any valid proof must satisfy S_hat_TRS(pi)>=N^{epsilon-o(1)} after normalizing bit debt by N.
- Prove the negative side by first omitted row. If a semantic FormulaEval atom has an unlisted influential row r*, set an unread enable bit so the visible transcript is unchanged while H_N^SAT parity changes; occurrence completion has no target-preserving certificate.
- Live pvsnp_inference_quality packet: source_statement=accepted Psys_sym^TRS proof pi of LB_N(1+epsilon) for H_N^SAT; target_statement=same-model SIZE upper-bound falsifier or forced row-equivalent support; model_context=nonuniform Boolean SIZE, beta-zero SAT-parity carrier, bEF plus transparent FormulaEval, parser/simulation not many-one reduction; quantifier_context=N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, size(G_N)=N^{rho+o(1)}, rho<1+epsilon, deterministic advice-free worklist; derivation_status=restricted TRS theorem and hidden-support countermodel derived, full semantic FormulaEval blocked at RealSATInfluenceRealizer_N; reviewer_findings=valid only under visibility, extensionality, influence closure, same-theory splicing, and no hidden advice.

Blocking gap: Unrestricted semantic FormulaEval remains blocked exactly at RealSATInfluenceRealizer_N: proof syntax and N must uniformly determine all semantically influencing rows, same-theory expansions, and charged overhead before the semantic rule is used.

## Falsifiers

- q<epsilon source-ceiling falsifier: C(H_N^SAT)<=N^{1+q+o(1)} contradicts LB_N(1+epsilon) in the same target model.
- Private-row/unread-enable-bit falsifier: an omitted influential row changes H_N^SAT while the visible proof transcript remains fixed.
- Hidden selector advice falsifier: a selector whose extensional set is not proof-visible can choose a row outside K_TRS without paying U_N or X_N.
- Projected-dDNNF missing-cover falsifier: the first reachable row not covered by a RowCoverCertificate_N defeats output-sensitive parsing.
- Semantic RealSAT atom falsifier: if influence depends on actual SAT truth rather than syntax-visible row support, occurrence counting is not valid.
- Natural-property falsifier probe: if the TRS transcript defines a large poly(N)-constructive useful truth-table property for SIZE_N, it faces PRF tension rather than becoming a barrier escape.

## Learning

Cycle 131 upgrades the cycle-130 theorem pair into an auditable proof packet: TRS has a finite checker, least reachable support, prefix-splice line induction, a derived Gamma_TRS ledger, q-density corollary, and a first-omitted-row countermodel. The contribution is valid route-level proof-system certification, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for hidden semantic FormulaEval and as a validation test for TRS visibility clauses.`
- Rationale: The branch already has abstract TRS clauses; a concrete private-row experiment tests whether the theorem pair really distinguishes target-preserving expansion from semantic leakage.
- Situation seed: Take H_N^SAT with M_N=N^{q+o(1)} rows and one FormulaEval line whose visible selector is an interval union, then add an optional semantic row r* controlled by an unread enable bit e inside the FormulaEval oracle.
- Varied variable: lambda in {0,1}, where lambda=1 means r* is listed in RowCoverCertificate_N and lambda=0 means r* is hidden inside semantic FormulaEval.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, epsilon, rho, tau, and the generator G_N are fixed., The visible proof transcript, interval selector code, and all bEF parent pointers are fixed., The target assertion remains LB_N(1+epsilon) against the same nonuniform SIZE_N class., The parser is deterministic and receives no advice beyond N and pi.
- Expected observation: At lambda=1 the charge ledger adds one row-equivalent unit and prefix splicing remains valid. At lambda=0 two visible transcripts are identical while the parity carrier differs on the r* row, producing the hidden-support falsifier.
- Transfer certificate needed: A uniform RealSATInfluenceRealizer_N that outputs r* and all other influential rows with same-theory expansion and charged overhead before the FormulaEval rule affects LB_N.

## Next Experiment

Instantiate the TRS checker on one projected-dDNNF FormulaEval line with an explicit RowCoverCertificate_N, compute K_TRS, U_N, X_N, and then delete the first reachable cover row to verify the private-row falsifier and the Gamma_TRS failure point.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For bit-explicit Psys_sym^QE, delayed FormulaEval support is harmless exactly when every quarantine exit dominates every external dependency and the exit prefix enumerates and charges the whole influence cone. Then Gamma_QE yields the same-model parser-to-circuit falsifier for LB_N(1+epsilon).

## Definitions

- source object: a bit-explicit Psys_sym^QE transcript pi for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), M_N=N^{q+o(1)}, with Psys_bEF^- rules plus FormulaEval quarantine blocks carrying parent pointers, row selectors, and exit certificates.
- target object: a nonuniform SIZE upper bound for the same H_N^SAT family in the same Boolean circuit model used by the asserted LB_N(1+epsilon), not a proof of P != NP.
- controlled interface: a prefix parser maps pi_{<t} to K_use(t), sealed quarantine exits B->e(B), row enumerators R_exit(B), same-theory row expansions Exp(R), and the ledger Gamma_QE(pi).
- target-preserving condition: before any outside line depends on a quarantined FormulaEval value, every influencing SAT row is prefix-visible, advice-free enumerable or full-scan charged, same-theory expanded, and free of SAT-truth pruning or hidden selector advice.
- exit domination: for every dependency edge from a line inside block B to a line outside B, the exit line e(B) lies on all dependency paths and occurs before the first outside use.
- K_use(t): the least fixed point over visible parent pointers, exposed row selectors, and previously charged exits reachable from the final LB_N line within the prefix pi_{<t}.
- S_seal(pi): the bit cost of checking block boundaries, exit certificates, dependency dominance, and absence of unsealed external uses.

## Assumptions

- Model: Psys_bEF^- plus syntactic FormulaEval quarantine blocks over surface SAT occurrences; semantic SAT extensionality is excluded unless RealSATInfluenceRealizer_N is supplied.
- Length regime: N tends to infinity, M_N=N^{q+o(1)}, formula length and row encodings are N^{o(1)}, and all hidden constants are uniform in N.
- Uniformity/advice: the parser, row enumerators, dominance checker, and expansion generator are advice-free polynomial-time in the proof description and charge all superlinear work in Gamma_QE.
- Same-theory condition: each charged row expansion uses the identical SAT encoding G_N and the same occurrence theory as the asserted proof line.
- Circuit target: the final upper bound is in the nonuniform SIZE model for H_N^SAT, so hardwiring a fixed parsed transcript is allowed but nonuniform hard-row selection is not a valid source construction.
- Barrier status: the lemma is nonrelativizing only if RealSATInfluenceRealizer_N is invoked; the syntactic QE theorem itself is a proof-complexity parser/falsifier and does not bypass natural-proofs or algebrization barriers.

## Equations

- QE ledger: `\Gamma_{QE}(\pi)=\Gamma_{bEF}(\pi)+U_{pre}(\pi)+X_{exit}(\pi)+S_{seal}(\pi)`. Valid when: Valid when Psys_sym^QE satisfies the target-preserving interface clauses and every quarantine exit certificate is prefix-visible before external dependency.
- row expansion charge: `X_{exit}(\pi)\ge N^{1+o(1)}\,|K_{idx}^{exit}(\pi)|`. Valid when: Applies when each charged row index expands to its same-theory SAT row over the N-size input universe with only subpolynomial encoding overhead.
- parser upper bound: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{QE}(\pi)+O(E_\pi N)`. Valid when: Requires the generator overhead, parsed proof transcript, row expansions, and extension-line simulations all target the same nonuniform Boolean circuit model.
- subthreshold falsifier: `N^{\rho+o(1)}+\Gamma_{QE}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \pi\text{ is not a valid same-model proof of }LB_N(1+\epsilon)`. Valid when: Valid when LB_N asserts a SIZE lower bound for exactly H_N^SAT and the parser simulation preserves the proof system's SAT encoding.

## Attempted Derivation

- Define the dependency DAG whose nodes are proof lines, FormulaEval internal rows, quarantine exits, and row-expansion certificates; edges are verifier-visible parent, selector, expansion, or external-use references.
- For each prefix pi_{<t}, compute K_use(t) by monotone fixed point from the final LB_N line through visible parents and already exited blocks; internal quarantined nodes are opaque until their exit line is reached.
- For a block B, require exit dominance: every path from an internal FormulaEval value to an outside line passes through e(B), and e(B) occurs before the first outside dependency. This is checkable from parent pointers and block boundary fields.
- At e(B), enumerate R_exit(B) or charge a full scan, expand all rows in the same SAT occurrence theory, and add U_pre(B)+X_exit(B)+S_seal(B) to Gamma_QE.
- Run line induction after replacing B by its charged exit macro: Psys_bEF^- lines use the archived Gamma_bEF invariant; transparent FormulaEval exits add exactly their enumerator, expansion, and sealing costs; no other line may read quarantined values.
- Construct the upper-bound circuit by hardwiring the parsed transcript skeleton, generator G_N of cost N^{rho+o(1)}, all charged row expansions, and extension-line simulations O(E_pi N). This gives the stated SIZE bound for H_N^SAT.
- For the negative half, choose the earliest external use violating exit dominance or influence closure. Since the row is not visible in the prefix view, toggle an unread enable/formula bit to obtain two surface completions with the same proof view but different FormulaEval value.

Blocking gap: The derivation is complete only for syntactic Psys_sym^QE surface FormulaEval. Full semantic SAT pruning is blocked at RealSATInfluenceRealizer_N: one must either list all real influencing rows with zero prefix latency and charge R_N, or prove a rule-specific no-realizer countermodel for the chosen semantic rule.

## Falsifiers

- First external dependency from a quarantined FormulaEval value occurs before its sealed exit certificate is parsed.
- The exit enumerator uses SAT-truth advice, a hidden selector bit, or nonuniform row ranking not charged in Gamma_QE.
- A row is declared irrelevant by semantic pruning but an unread enable bit can flip its contribution while preserving every visible proof bit.
- The same-theory row expansion is replaced by a different SAT encoding, invalidating the target-preserving transfer.
- Non-row costs N^{rho+o(1)}, Gamma_bEF, S_seal, or O(E_pi N) already exceed N^{1+epsilon-o(1)}, so no subthreshold falsifier follows.
- A purported MCSP/MKtP carrier supplies only an advice-selected hard row rather than a searchable prefix-visible certificate.

## Learning

Cycle 131 adds an implementable dominance criterion to the timing normal form: delayed FormulaEval support is valid exactly when a sealed exit dominates every external dependency and pays the full influence cone before use. This gives a referee-checkable Gamma_QE line induction for syntactic Psys_sym^QE and turns truth-pruned semantic FormulaEval into a concrete zero-latency realizer obligation or private-row falsifier.

## Gedanken Experiment Design Seed

- Need decision: `use now as a falsifier probe for RealSATInfluenceRealizer_N and QE exit dominance`
- Rationale: The branch has a theorem-shaped timing normal form; the remaining risk is a concrete semantic FormulaEval rule that prunes branches by SAT truth before any prefix-visible support certificate exists.
- Situation seed: A Tseitin/self-reduction FormulaEval block for SAT(F) splits on variable z, explicitly lists both branch formulas F|z=0 and F|z=1 inside quarantine, but a semantic-pruning variant exports only the branch currently known satisfiable before exit.
- Varied variable: exit latency ell: the number of outside dependency steps after the FormulaEval value is used and before the omitted branch row is enumerated or charged.
- Held-fixed controls: H_N^SAT, M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)}, and the same SAT encoding G_N are fixed., The base parser is Psys_bEF^- with bit-visible parent pointers and the QE block boundary grammar., No nonuniform selector advice, SAT-truth advice, or post-hoc row discovery may be used outside the charged Gamma_QE ledger., The target remains a same-model SIZE upper bound falsifier for LB_N(1+epsilon), not a P vs NP claim.
- Expected observation: For ell=0 with both branch rows listed at exit, the block is transparent and pays the QE ledger. For ell>0 or truth-pruned omission, an unread branch-enable bit creates two prefix-identical completions with different exported FormulaEval value.
- Transfer certificate needed: A zero-latency RealSATInfluenceRealizer_N for the Tseitin/self-reduction rule: from pi_{<t} and N alone it must enumerate every potentially influencing branch row, prove same-theory relevance or irrelevance, and add R_N to Gamma before first external use.

## Next Experiment

Instantiate the Tseitin/self-reduction FormulaEval thought experiment: write bit fields for the two branch rows, compute U_pre and X_exit when both branches are listed at exit, then construct the truth-pruned private-branch falsifier for exit latency ell>0.
