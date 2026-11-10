# cycle-0127

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Declared bounded Tseitin self-reduction is a valid least-closed-support rule case: in Psys_sym^{dag,declTSR_h}, if every TSR root, pivot, restriction child, Tseitin extension map, and same-theory row expansion is syntactically declared before use, then the K_dag fixed point absorbs all TSR influences with charge X_TSR=N^{1+kappa+theta+o(1)}. Consequently a claimed LB_N(1+epsilon) proof with N^{rho+o(1)}+Gamma_bEF(pi)+U(K_dag)+X(K_dag)+X_TSR+O(E_pi N)<N^{1+epsilon-o(1)} is falsified by a same-model SIZE upper bound for H_N^{SAT}.

## Definitions

- source object: H_N^{SAT}(x)=xor_{j<M_N} SAT(G_N(x,j)) on N-bit source inputs, with M_N=N^{q+o(1)}, formula length L_N=(log N)^d, and generator circuit cost N^{rho+o(1)}.
- target object: the same nonuniform SIZE_N lower-bound assertion LB_N(1+epsilon) for the beta-zero parity carrier H_N^{SAT}; the route-level target is a parser/falsifier theorem, not P != NP.
- controlled interface: Psys_sym^{dag,declTSR_h} transcripts whose FormulaEval and TSR lines expose verifier-visible parent pointers, row indices, restriction-node tags, pivot bits, Tseitin maps, child lists, and same-theory expansion certificates.
- target-preserving condition: all row supports are advice-free, prefix-closed, influence-complete, charged in Gamma, and use polylog-length SAT rows so the beta-zero substitution window and the same SIZE model are preserved.

## Assumptions

- Model context: source circuits are nonuniform Boolean SIZE circuits on length N, and proof parsing is charged as circuit size; no uncharged advice string may select rows or branches.
- Quantifier regime: epsilon>0, q>=0, rho>=0, kappa>=0, theta>=0, and d>1 are fixed constants while N tends to infinity through valid generated lengths.
- Declared TSR regime: each used TSR node contains an explicit row id r=(j,a), a pivot variable, two child row ids, and a bounded-depth restriction path of length at most h=polylog(N) or an explicitly charged bounded h.
- Same-theory condition: child rows encode the exact restricted/Tseitin-transformed SAT formulas in the same row theory used by the parser; semantic SAT truth is not used to prune a branch.
- Uniformity/advice status: K_dag(pi) and all declared TSR child rows are computed from N and pi by a finite closure algorithm; the enumerator cost U and row expansion cost X are included in Gamma.
- Barrier status: the positive lemma is syntactic and relativizing as a parser theorem; the escape to full semantic SAT reasoning is explicitly isolated as RealSATInfluenceRealizer_N^arb and is not assumed.
- Source statement: a short Psys_sym^{dag,declTSR_h} transcript purports to certify LB_N(1+epsilon) for H_N^{SAT}.
- Target statement: a subthreshold charged transcript yields an explicit same-model upper bound for H_N^{SAT}, hence is a falsifier for that source certificate.

## Equations

- carrier: `H_N^{\mathrm{SAT}}(x)=\bigoplus_{j<M_N} \mathrm{SAT}(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad |G_N(x,j)|=(\log N)^d`. Valid when: Valid when the source carrier is the beta-zero parity generator with uniformly indexed polylogarithmic SAT rows and no hidden row advice.
- closure_operator: `K_{t+1}=K_t\cup \mathrm{Par}_\pi(K_t)\cup \mathrm{RowSet}_{FE}(K_t)\cup \mathrm{ChildRows}_{TSR}(K_t),\quad K_{dag}=\mathrm{lfp}(K_t)`. Valid when: Valid when every proof line exposes machine-checkable parent pointers and every TSR or FormulaEval influence has a syntactic row certificate.
- declared_TSR_charge: `R_{TSR}(\pi)=N^{\kappa+\theta+o(1)},\qquad X_{TSR}(\pi)=N\cdot R_{TSR}(\pi)=N^{1+\kappa+\theta+o(1)}`. Valid when: Applies after declared TSR roots and children are uniformly enumerable and each declared row expansion is charged by an N-size equality patch.
- gamma_total: `\Gamma_{dag+TSR}(\pi)=\Gamma_{bEF}(\pi)+U(K_{dag})+X(K_{dag})+X_{TSR}(\pi)`. Valid when: Valid when bit-explicit EF costs, transparent FormulaEval costs, and declared TSR expansion costs are all in the same circuit-size ledger.
- parser_upper_bound: `C_{SIZE}(H_N^{\mathrm{SAT}})\le N^{\rho+o(1)}+\Gamma_{dag+TSR}(\pi)+O(E_\pi N)`. Valid when: Requires the target-preserving parser induction to build the final carrier circuit in the same nonuniform SIZE model from the charged transcript.
- lb_falsifier_window: `N^{\rho+o(1)}+\Gamma_{dag+TSR}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Valid when LB_N is the claimed same-model lower bound for H_N and the constructed upper bound has all advice and row costs charged.

## Attempted Derivation

- Initialize K_0 with the final LB_N line, the final carrier row symbols, and any explicitly named residual-error rows.
- Iterate the monotone closure operator: add bit-EF parents, SATeq links, transparent FormulaEval RowSet entries, and for every declared TSR node add both restriction children, the restriction path bits, and the Tseitin extension clauses.
- Charge each insertion by its visible certificate: U(K) for enumerators, X(K) for occurrence or row expansion, Gamma_bEF for bit-explicit proof dependencies, and X_TSR=N R_TSR for declared TSR child rows.
- Prove minimality by induction on closure time: any safe extensional parser that validates the final line must include every predecessor inserted by the operator, otherwise the first omitted predecessor admits the private-row disagreement test.
- Extend the existing Gamma_bEF line induction. For ordinary bEF lines use the old invariant; for FormulaEval lines call TransparentRowSupport_N; for declared TSR lines compute the parent SAT value from declared child values and charged Tseitin consistency circuits.
- At the final line, splice the generator circuit of size N^{rho+o(1)} with the transcript circuits of total size Gamma_{dag+TSR}+O(E_pi N) to obtain a same-model circuit for H_N^{SAT}.
- Contrapose: if the final size is below N^{1+epsilon-o(1)}, the transcript is not a valid certificate of LB_N(1+epsilon).
- For hidden TSR pruning, choose the earliest proof use whose semantically live child r^* is absent from K_dag; construct two label worlds agreeing on K_dag and flipping only r^*, then place r^* at one parity slot x^* to flip H_N while preserving the visible transcript.

Blocking gap: The positive derivation is complete only for declared TSR syntax. Full real-SAT semantic branch pruning remains blocked at RealSATInfluenceRealizer_N^arb: a uniform, advice-free, nonrelativizing procedure must list all live child rows and charge them before the semantic rule is used.

## Falsifiers

- First-unlisted-child private-row falsifier: hidden TSR pruning lets two transcripts agree on all charged rows while the omitted restriction child flips the carrier parity.
- Unread-enable-bit falsifier: a symbolic FormulaEval line whose enabling bit is never surfaced can select an uncharged row after the parser commits to K_dag.
- Threshold falsifier: if kappa+theta<epsilon and all other Gamma terms are subthreshold, declared TSR support produces an explicit SIZE upper bound below N^{1+epsilon}.
- q<epsilon enumeration falsifier: a support cone smaller than N^{epsilon-o(1)} cannot certify LB_N(1+epsilon) because N|K| is patchable.
- Model-mismatch falsifier: row labels selected by SAT-truth advice are outside the same nonuniform SIZE ledger and cannot be counted as transparent support.
- Positive-beta carryover falsifier: any return to black-box target-circuit substitution with beta>0 is capped by q+beta c+o(1) and cannot exclude all SAT circuit exponents.

## Learning

Cycle 127 adds a concrete rule-level proof packet: declared bounded TSR is absorbed by the least closed support cone with exact charge N^{1+kappa+theta+o(1)}, while hidden branch pruning has a first-unlisted-child falsifier. This improves the paper theorem boundary without claiming P != NP or a general H_N lower bound.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for declared versus hidden TSR support.`
- Rationale: The branch already has the abstract K_dag theorem; the remaining risk is whether bounded TSR branch pruning is genuinely chargeable or can smuggle semantic row influence. A concrete two-world test isolates exactly the missing realizer certificate.
- Situation seed: Take H_N^{SAT} with M_N=N^q slots and choose one slot j^*. Let G_N(x^*,j^*) be a Tseitin-encoded formula whose satisfiability under a bounded self-reduction is determined by one restriction child r^*. Compare a declared transcript listing r^* with a hidden-pruning transcript whose proof line uses the parent value but omits r^*.
- Varied variable: theta, the exponent of declared TSR child expansion per active root, together with a binary visibility flag declared versus hidden for r^*.
- Held-fixed controls: Keep beta=0 by using polylogarithmic SAT row length L_N=(log N)^d and no target-query exponent in the substitution., Keep M_N=N^{q+o(1)}, generator cost N^{rho+o(1)}, and the same nonuniform SIZE_N model for all circuits., Keep the proof syntax, visible K_dag rows, and all FormulaEval parent pointers identical across the two worlds., Keep the target-preserving rule that every charged row must have an advice-free index and same-theory expansion certificate.
- Expected observation: When r^* is declared, Gamma gains N^{1+kappa+theta+o(1)} and the falsifier threshold is kappa+theta<epsilon. When r^* is hidden, two worlds agree on every charged row but disagree on H_N(x^*), proving the parser invalid unless the real-SAT semantics force r^* into a charged influence set.
- Transfer certificate needed: A RealSATInfluenceRealizer_N^arb certificate: from N, pi, and the semantic TSR rule, uniformly enumerate all live restriction children, prove same-theory correctness of their Tseitin rows, and charge their total expansion before using the semantic inference.

## Next Experiment

Write the verifier bit fields for one declared TSR line: root row id, restriction-node path, pivot variable, child row ids, Tseitin map hash, occurrence-neighborhood list, parent pointers, and expansion certificate; then prove the single-line induction inequality adding exactly N times the declared child count to Gamma_{dag+TSR}.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For the concrete transparent fragment Psys_sym^{ann-SR_h}, every FormulaEval-SAT use of a bounded self-reduction rule with visible child-row annotations admits a deterministic FE_Extract_N parser. The parser enumerates all influencing rows, prefix-splices same-theory bEF expansions, and charges row-equivalent support; hence any subthreshold proof of LB_N(1+epsilon) yields a same-model SIZE upper-bound falsifier.

## Definitions

- source object: a Psys_sym^{ann-SR_h} proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with |pi|=N^{tau+o(1)}, M_N=N^{q+o(1)}, and each SR_h FormulaEval line carrying h=N^{eta+o(1)} visible child-row descriptors.
- target object: the nonuniform Boolean SIZE model for H_N^SAT at threshold N^{1+epsilon}, together with the parser-to-circuit upper-bound transcript Gamma_SRh(pi).
- controlled interface: FE_Extract_N reads only proof-visible row-cover fields, local occurrence-neighborhood pointers, SR_h child descriptors, and prefix-scoped extension variables; it uses no SAT-truth advice or hidden selector advice.
- target-preserving condition: every row that can change the semantic value of a FormulaEval-SAT line is listed, locally checkable, and charged before the line is used; row expansions remain in the same bEF/SATeq theory and the generator G_N has size N^{rho+o(1)} with rho<1+epsilon.

## Assumptions

- Length regime: N=2^n and all o(1) terms are uniform over the proof family and parser family.
- Proof model: Psys_sym^{ann-SR_h} extends bit-explicit Psys_bEF only by annotated bounded-SR_h FormulaEval lines with visible child-row lists and local verifiers.
- Uniformity/advice condition: FE_Extract_N is deterministic from (N,pi) and does not receive semantic advice about which SAT rows are relevant.
- Same-theory condition: each extracted row expansion can be inserted prefix-locally with fresh extension variables and without changing later line meanings except through declared pointers.
- Lower-bound claim being audited is LB_N(1+epsilon), i.e. the asserted nonexistence of SIZE(N^{1+epsilon-o(1)}) circuits for the beta-zero carrier; the lemma is not a P != NP claim.

## Equations

- row-count: `|R_{SRh}(\pi)| \le |\pi|\,h\,N^{o(1)} = N^{\tau+\eta+o(1)}`. Valid when: Valid when every SR_h FormulaEval invocation explicitly lists at most h child rows and the parser checks only bounded occurrence neighborhoods.
- bit-expansion-charge: `X_{SRh}(\pi) \le N\,|R_{SRh}(\pi)|\,N^{o(1)} = N^{1+\tau+\eta+o(1)}`. Valid when: Valid when one extracted row expansion costs N^{1+o(1)} bEF bits including generator evaluation and SATeq bookkeeping.
- gamma-charge: `\Gamma_{SRh}(\pi)=\Gamma_{bEF}(\pi)+U_N(\pi)+X_{SRh}(\pi)+O(E_\pi N)`. Valid when: Applies after the reduction preserves prefix scope, same-theory expansion, visible row enumeration, and FormulaEval extension links.
- upper-bound-falsifier: `C(H_N^{SAT}) \le N^{\rho+o(1)}+\Gamma_{SRh}(\pi)`. Valid when: Requires the target-preserving extraction to replace every charged FormulaEval use by an explicit circuit fragment in the same nonuniform SIZE model.
- forced-support: `N^{\rho+o(1)}+\Gamma_{SRh}(\pi) \ge N^{1+\epsilon-o(1)}`. Valid when: Valid for any accepted sound proof of LB_N(1+epsilon), because the contrary inequality constructs a SIZE upper-bound falsifier.
- normalized-row-pressure: `\widehat S_{eff}^{SRh}(\pi):=|R_{SRh}(\pi)|+E_\pi+\lceil U_N(\pi)/N\rceil \ge N^{\epsilon-o(1)}`. Valid when: Valid when Gamma_bEF is lower order, rho<1+epsilon, and row-equivalent charge is the only remaining transcript cost.

## Attempted Derivation

- Normalize each annotated bounded-SR_h FormulaEval line into Gap98 fields: parent row id, child row list of length at most h, touched occurrence-neighborhood pointers, local verifier bits, and fresh prefix extension variables.
- Run a worklist from the final LB_N line backwards through declared dependencies; whenever an SR_h line is reached, insert every listed child row into R_SRh and reject if a later semantic dependency is not among the listed children.
- For each extracted row, splice the bEF expansion before the first use of the FormulaEval line; freshness and parent pointers preserve prefix order and avoid changing later formulas.
- Maintain the induction invariant that every surviving proof line is derivable in the row-expanded same theory and that its cost is charged to Gamma_bEF+U_N+X_SRh+O(E_pi N).
- At the final LB_N line, translate the expanded transcript plus the generator circuit into an explicit nonuniform circuit for H_N^SAT of size at most N^{rho+o(1)}+Gamma_SRh(pi).
- If that size is below N^{1+epsilon-o(1)}, the transcript is a same-model falsifier to the asserted LB_N(1+epsilon); therefore sound accepted proofs must pay the forced row-equivalent support threshold.

Blocking gap: The derivation is complete for Psys_sym^{ann-SR_h}. It does not resolve arbitrary semantic FormulaEval because RealSATInfluenceRealizer_N is still needed to recover hidden influencing rows without annotations.

## Falsifiers

- First omitted child-row falsifier: two carriers agree on every annotated row and proof bit but differ on an unlisted SR_h child row that changes the FormulaEval value.
- Unread-enable-bit falsifier: the proof displays a disabled or hidden selector bit whose semantic setting chooses a private row not present in K_idx^+(pi).
- Projected-dDNNF without RowCoverCertificate_N: a projected support cone can hide the first reachable row unless a visible cover certificate is charged.
- q<epsilon source-ceiling falsifier: C(H_N^SAT)<=N^{1+q+o(1)} already contradicts any claimed LB_N(1+epsilon) before proof-system issues matter.
- Naturalness falsifier: if FE_Extract_N plus the proof predicate becomes a poly(N)-constructive large useful property against the same SIZE class, PRF tension applies unless the property is non-large or proof-mediated without truth-table usefulness.

## Learning

Cycle 127 closes a concrete FE_Extract_N subgoal for annotated bounded-SR_h FormulaEval: the exact row-equivalent charge is N^{tau+eta+o(1)}, the bit-expansion debt is N^{1+tau+eta+o(1)}, and tau+eta<epsilon is a valid same-model upper-bound falsifier for LB_N(1+epsilon) when other debts are lower order. Arbitrary semantic FormulaEval remains quarantined at RealSATInfluenceRealizer_N; this is route-level proof-system certification, not progress on P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The remaining question is quantitative, not slogan-level: annotated SR_h transparency must show exactly when proof length and child-row fanout create enough charged support to avoid the extracted upper-bound falsifier.
- Situation seed: A padded beta-zero SAT-parity family H_N^SAT with M_N=N^q rows and a Psys_sym^{ann-SR_h} proof using T=N^tau FormulaEval self-reduction lines, each carrying an explicit list of h child rows and occurrence-neighborhood pointers.
- Varied variable: eta, where h=N^{eta+o(1)} is the annotated child-row fanout per bounded-SR_h FormulaEval line.
- Held-fixed controls: M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and rho<1+epsilon., Proof-visible row annotations, no SAT-truth advice, and deterministic FE_Extract_N from (N,pi)., Same-theory prefix splicing into bEF/SATeq and N^{1+o(1)} bit cost per row expansion., Other debts Gamma_bEF, U_N/N, and E_pi are kept o(N^epsilon) for the threshold probe.
- Expected observation: When tau+eta<epsilon, the row-equivalent support is too small and the expanded transcript gives a SIZE(N^{1+epsilon-o(1)}) circuit, falsifying LB_N(1+epsilon). When tau+eta reaches epsilon, this particular falsifier disappears but no lower bound follows.
- Transfer certificate needed: A valid Gap98-SRh normal form plus FE_Extract_N completeness certificate proving that every influencing row is listed, locally checkable, prefix-spliceable, and charged before the FormulaEval line is used.

## Next Experiment

Write the standalone theorem statement for FE_Extract_N^{ann-SR_h}: include the Gap98 bit fields, RowSet worklist, prefix-splice induction, Gamma_SRh ledger, and the eta+tau<epsilon falsifier inequality; then test one unannotated SR_h line to exhibit the first omitted child row.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For Psys_sym^time proofs of beta-zero H_N^SAT lower-bound lines, prefix-causal transparent FormulaEval support yields a same-model parser-to-circuit simulation with ledger Gamma_time. Any proof with subthreshold Gamma_time is a falsifier for the claimed LB_N(1+epsilon) line, but only inside the named proof-system interface.

## Definitions

- source object: a bit-explicit Psys_sym^time proof pi over H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), where FormulaEval lines may reference SAT rows and all non-FormulaEval lines are parsed by the Psys_bEF^- Gamma_bEF normal form.
- target object: nonuniform SIZE circuits for the same H_N^SAT family over the same input length N, used only to refute the specific proof-line claim LB_N(1+epsilon) when the constructed circuit is below N^{1+epsilon-o(1)}.
- controlled interface: PrefixCausalTransparentRowSupport_N, consisting of prefix-visible selector code, an advice-free row enumerator or full-scan declaration, an influence-closure certificate, same-theory row expansion, and no hidden semantic support before each FormulaEval use.
- target-preserving condition: the parser may use only bits and row expansions already determined by pi_{<t}; it may not import SAT-truth advice, delayed support discovery, nonuniform row choice, or a semantic oracle outside the Psys_sym^time syntax.
- K_t(pi): the least support set after line t obtained by a verifier-visible fixed point that adds exactly the row indices enumerated and influence-certified before line t is evaluated.
- U_time(pi): total prefix row-discovery cost, including selector code, enumerator proof, deduplication, or full-scan charge for FormulaEval lines.
- X_time(pi): total same-theory expansion cost for rows in the time-stamped support cone, with row expansion size E_row(N)=N^{1+o(1)} in the beta-zero SAT-row model.

## Assumptions

- Model: Psys_bEF^- rules already satisfy the Gap98-SRhNormalForm line induction with bit fields, parent pointers, row-index encodings, eta/tau overhead, and Gamma_bEF accounting.
- Regime: M_N=N^{q+o(1)}, generator overhead is N^{rho+o(1)}, row formulas have polylog or N^{o(1)} local description overhead, and all exponents are interpreted along an infinite valid length sequence.
- Uniformity: K_t, its enumerator, and the influence certificates are computed from N and the proof prefix pi_{<t}; no advice string may select a hard row or a hidden support set.
- Same-theory condition: every charged row expansion is an occurrence-level expansion in the same SAT/formula language used by the proof, not an external semantic assertion.
- Non-claim: this proves a restricted parser/falsifier theorem only; it is not a proof of P != NP and it does not handle full semantic FormulaEval without RealSATInfluenceRealizer_N.

## Equations

- beta_zero_family: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)}`. Valid when: Valid when the source proof system addresses the fixed beta-zero SAT-query family and the query exponent q is measured on the same length scale N.
- prefix_support_update: `K_t=\operatorname{cl}_{\pi_{<t}}(K_{t-1}\cup R_t),\quad R_t\text{ enumerated before line }t`. Valid when: Valid when each FormulaEval line exposes its row set and influence certificate in the proof prefix before the semantic value is used.
- gamma_time_ledger: `\Gamma_{time}(\pi)=\Gamma_{bEF}(\pi)+U_{time}(\pi)+X_{time}(\pi)`. Valid when: Valid when Gap98-SRhNormalForm accounts for non-FormulaEval lines and all FormulaEval support is prefix-causal transparent and charged.
- row_expansion_charge: `X_{time}(\pi)\ge N^{1+o(1)}\,|K_{idx}^{time}(\pi)|`. Valid when: Applies when each charged SAT row contributes an occurrence-level expansion over N input positions with only subpolynomial local overhead.
- subthreshold_falsifier: `N^{\rho+o(1)}+\Gamma_{time}(\pi)+O(E_\pi N^{1+o(1)})<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Requires the target-preserving same-model circuit simulation and a claimed LB_N lower-bound threshold in the identical nonuniform SIZE model.

## Attempted Derivation

- Fix N and a Psys_sym^time proof pi of a beta-zero LB_N(1+epsilon) line. Parse non-FormulaEval rules using the established Gap98-SRhNormalForm and charge them to Gamma_bEF(pi).
- Define a verifier-visible fixed point. At line t, the parser reads only pi_{<t}; if t is not FormulaEval, K_t=K_{t-1}. If t is FormulaEval, the prefix must contain selector code, an advice-free enumerator or full-scan declaration, an influence-closure certificate, and a same-theory row-expansion recipe. The enumerated rows R_t are added before the line value is used.
- Prove the induction invariant: after line t, every value used by the parser is determined by the occurrence bits in K_t plus the bEF transcript. The FormulaEval step is valid because influence closure says no unenumerated row can change A_t while the prefix is fixed.
- Build the same-model nonuniform circuit by hardwiring pi, the generator G_N, the parsed bEF transcript, and the expanded SAT rows for K_time. The size is bounded by N^{rho+o(1)}+Gamma_bEF+U_time+X_time+O(E_pi N^{1+o(1)}).
- If this size is below N^{1+epsilon-o(1)}, the proof itself yields a circuit contradicting the asserted LB_N(1+epsilon) line. This is a valid low-cost-transcript falsifier in the target SIZE model.
- For the negative branch, choose the first FormulaEval line with r in Infl(A_t) minus K_{t-1}. Minimality fixes all earlier lines. Since r is not read or charged, construct two occurrence completions agreeing on all prefix-visible bits but differing on r or its unread enable bit. The semantic FormulaEval value flips, so the parser transcript cannot certify the line.
- Instantiate the semantic boundary on Tseitin/self-reduction FormulaEval: explicit branch enumeration is transparent and charged; SAT-truth branch pruning hides an enable bit unless a zero-latency RealSATInfluenceRealizer_N lists the pruned branch influence before the pruning line.

Blocking gap: The restricted K_time theorem is proof-shaped modulo the archived Gap98-SRhNormalForm. The remaining full-system gap is RealSATInfluenceRealizer_N for truth-pruned semantic FormulaEval: no advice-free zero-latency influence lister is proved for real SAT truth pruning.

## Falsifiers

- First hidden semantic influence: r in Infl(A_t) but r not in K_{t-1}, producing the private-row falsifier.
- Post-hoc support discovery: a row set listed after the FormulaEval line is not valid for prefix-causal transparency.
- SAT-truth branch pruning: an unread enable bit can change the pruned self-reduction branch while all charged prefix bits stay fixed.
- Advice-ranked row selection: any nonuniform choice of hard or influential rows violates the target-preserving uniformity ledger.
- Membership-only AC0 or semantic selector without output-sensitive enumeration pays full scan or becomes a semantic-oracle escape.
- Ledger threshold failure: if rho, Gamma_bEF, U_time, or X_time reaches N^{1+epsilon-o(1)}, the low-cost transcript no longer falsifies LB_N(1+epsilon).

## Learning

Cycle 127 turns the prior prefix-causality slogan into a theorem-shaped proof packet. The valid transfer certificate is a time-stamped support cone K_time computed from pi_{<t}; delayed semantic support is not valid and yields a first-hidden-influence falsifier. The only remaining full-semantic escape is a zero-latency RealSATInfluenceRealizer_N, so the contribution is a scoped FormulaEval parser obstruction, not progress on the main P != NP conjecture.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and as the concrete validation example for L127.2.`
- Rationale: The branch is blocked only at semantic FormulaEval. A concrete Tseitin/self-reduction pruning case tests whether prefix-causal transparency is a real theorem boundary or only a restatement.
- Situation seed: A Psys_sym^time proof line evaluates SAT(G_N(x,j)) by a bounded Tseitin self-reduction tree. Version A explicitly enumerates every branch row before use. Version B prunes branches using a SAT-truth predicate and records only the surviving branch.
- Varied variable: prefix latency ell of influence discovery, with ell=0 meaning every branch influence is enumerated before FormulaEval and ell>0 meaning some pruned branch is revealed only after the semantic pruning line.
- Held-fixed controls: The target family remains H_N^SAT with M_N=N^{q+o(1)} and the same nonuniform SIZE lower-bound claim LB_N(1+epsilon)., The parser remains the Psys_sym^time occurrence parser with Gap98-SRhNormalForm for non-FormulaEval lines., No advice strings, nonuniform row selectors, or SAT-truth oracle bits may be added outside the proof prefix., Every charged row expansion must occur in the same SAT/formula theory and be counted in X_time.
- Expected observation: At ell=0, explicit branch enumeration is transparent and pays the row-expansion ledger. At ell>0, an unread branch-enable bit gives two completions with the same prefix transcript but different FormulaEval value, certifying the private-branch falsifier.
- Transfer certificate needed: A zero-latency RealSATInfluenceRealizer_N: from N and pi_{<t}, it must list all semantically influential branches, prove influence closure, and add its cost to Gamma_time before the pruning line is evaluated.

## Next Experiment

Write the referee-checkable K_time fixed-point pseudocode and instantiate it on two Tseitin/self-reduction FormulaEval lines: explicit branch enumeration with charged support, and truth-pruned branch selection with an unread-enable-bit falsifier.
