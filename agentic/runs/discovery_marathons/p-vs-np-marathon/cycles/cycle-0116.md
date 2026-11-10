# cycle-0116

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: Transparent FormulaEval Minimality Audit

## Candidate Lemma

For the beta-zero parity carrier H_N^SAT and Psys_sym with bit-explicit EF/SATeq/bounded-SR plus FormulaEval, TransparentRowSupport_N is a sufficient and clause-minimal interface for the parser-to-circuit falsifier. Transparent FormulaEval lines contribute U_FE+X_FE to Gamma_trans; failure of visibility, extensional enumeration, influence closure, or no-hidden-advice yields a private-row or unread-enable-bit two-world falsifier. Failure of same-theory expansion is not refuted by that oracle argument and is quarantined exactly as RealSATInfluenceRealizer_N.

## Definitions

- source object: H_N^SAT(x)=XOR_{j<M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, |G_N|=N^{rho+o(1)}, and each generated formula length L_N=(log N)^d for fixed d>1.
- target object: LB_N(1+epsilon), the nonuniform SIZE lower-bound assertion C(H_N^SAT)>N^{1+epsilon-o(1)}, used only as a route-level source lower bound and not as P != NP.
- controlled interface: TransparentRowSupport_N for each FormulaEval line provides visible selector code, advice-free row enumeration or full scan, influence closure, same-theory occurrence expansion, and no hidden semantic advice.
- target-preserving condition: The parser simulation stays in the same nonuniform SIZE model, preserves beta=0 polylog target-query length, charges every surfaced row by N^{1+o(1)}, and never treats real SAT semantics as occurrence support unless realized by RealSATInfluenceRealizer_N.
- Gamma_bEF(pi) is the prior bit-explicit EF/SATeq/bounded-SR transcript charge, including B_SR(pi) and sparse residual row charge when present.
- U_FE(pi) is the total advice-free enumeration cost for visible FormulaEval row supports; X_FE(pi)=N^{1+o(1)} times the number of surfaced row indices expanded in the same proof theory.

## Assumptions

- Circuit model is nonuniform Boolean SIZE over inputs of source length N; advice is allowed only as ordinary circuit nonuniformity and must be charged if it selects proof rows.
- Psys_sym lines outside FormulaEval already satisfy the Psys_bEF^- parser theorem from cycles 100-104, including bit fields, parent pointers, SATeq links, and bounded-SR_h overhead eta,tau.
- A transparent FormulaEval selector has a syntactic code whose RowSet is extensionally enumerable from the proof line and public parameters, or else the proof pays the full scan charge over M_N rows.
- Influence closure means every carrier row whose SAT label can change the FormulaEval truth value is included in RowSet before occurrence expansion.
- Same-theory expansion means the expanded row occurrences are formulas inside the same lower-bound proof language, not an external semantic oracle for real SAT.
- The two-world countermodel is valid only for hidden support not forced by real SAT semantics; real SAT-specific forcing is the named nonrelativizing escape RealSATInfluenceRealizer_N.

## Equations

- carrier: `H_N^SAT(x)=XOR_{j<M_N} SAT(G_N(x,j)), M_N=N^{q+o(1)}, |G_N|=N^{rho+o(1)}`. Valid when: Valid when the source carrier is the beta-zero batched SAT parity problem with polylogarithmic generated instances and explicit generator overhead.
- transparent_charge: `Gamma_trans(pi)=Gamma_bEF(pi)+U_FE(pi)+X_FE(pi), X_FE(pi)=N^{1+o(1)} sum_l |RowSet_l|`. Valid when: Applies after every FormulaEval line has visible advice-free row support and same-theory occurrence expansion charged by row index.
- parser_upper_bound: `C_SIZE(H_N^SAT)<=N^{rho+o(1)}+Gamma_trans(pi)+E_N N^{1+o(1)}`. Valid when: Valid when the parsed proof transcript computes the carrier except for E_N residual source rows patchable by equality gates.
- lb_falsifier_window: `N^{rho+o(1)}+Gamma_trans(pi)+E_N N^{1+o(1)}<N^{1+epsilon-o(1)} => not LB_N(1+epsilon)`. Valid when: Requires the target-preserving SIZE simulation, beta-zero substitution, and exact lower-bound threshold to be in the same length regime.

## Attempted Derivation

- Fix N, M_N=N^{q+o(1)}, beta=0, generator G_N of size N^{rho+o(1)}, and a Psys_sym proof pi whose non-FormulaEval lines are parsed by the Psys_bEF^- theorem.
- For each transparent FormulaEval line l, compute RowSet_l from visible selector code. If enumeration is output-sensitive charge U_l; otherwise full scan costs M_N N^{1+o(1)} and is recorded in X_FE.
- Expand every j in RowSet_l into the same proof theory by inserting the occurrence neighborhood for SAT(G_N(x,j)) over all source rows x; charge N^{1+o(1)} per row index and add this to Gamma_trans.
- Run line induction: bit-explicit EF dependencies, SATeq links, bounded-SR_h leaves, and transparent FormulaEval expansions each yield circuits for the line predicates with total size bounded by Gamma_trans plus generator overhead.
- If the proof certifies LB_N(1+epsilon) but N^{rho+o(1)}+Gamma_trans+E_N N^{1+o(1)} is below N^{1+epsilon-o(1)}, the derived circuit is a valid falsifier for the asserted source lower bound.
- For minimality, suppose a FormulaEval line has a hidden influential row r not in the charged RowSet. Build two label worlds agreeing on all charged rows and proof-visible bits but differing on the SAT label of r; carrier parity differs after choosing x with r's coefficient one, so occurrence completion was not sound.
- If the selector has an unread enable bit, choose two settings with identical parsed transcript and different inclusion of r. This gives the same two-world falsifier and shows extensional enumeration is necessary.
- If influence closure fails, downstream FormulaEval can depend on r through an unlisted derived predicate. Flipping r preserves the transcript but changes the carrier-relevant line, so the parser misses a row charge.
- If hidden advice selects r, the proof transcript is unchanged while the selected support changes. The advice must either be charged as U_FE or the private-row falsifier applies.
- If same-theory expansion fails because real SAT semantics determine r, the two-world spoof may violate SAT. This is not a valid countermodel; it is exactly the RealSATInfluenceRealizer_N blocked lemma.

Blocking gap: Full semantic FormulaEval remains blocked at RealSATInfluenceRealizer_N: private-row spoofing is a relativizing falsifier for hidden support, but it cannot refute genuinely real-SAT semantic influence without a same-theory realization or a concrete semantic no-go.

## Falsifiers

- Private-row falsifier: an uncharged influential row r has two label worlds agreeing on the parsed transcript but differing on H_N^SAT.
- Unread-enable-bit falsifier: selector inclusion of r is controlled by a bit not read by the parser, so RowSet is not extensionally valid.
- Hidden-advice falsifier: nonuniform row-selection advice can encode the needed support while evading U_FE and X_FE charges.
- Subthreshold Gamma falsifier: N^{rho}+Gamma_trans+E_N N<N^{1+epsilon} gives an explicit small SIZE circuit against LB_N(1+epsilon).
- Same-theory failure is not a valid oracle falsifier; it quarantines the route at RealSATInfluenceRealizer_N rather than at generic barrier folklore.

## Learning

Cycle 116 closes the minimality audit for the transparent FormulaEval theorem pair. The valid paper claim is now a restricted parser/falsifier boundary: every surfaced influence is charged in Gamma_trans, and every unsurfaced nonsemantic influence admits a private-row falsifier. The only remaining full-system route is the named nonrelativizing RealSATInfluenceRealizer_N; this is not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the minimality theorem pair.`
- Rationale: The top proof item needs a concrete test that distinguishes transparent support from hidden semantic FormulaEval; another abstract restatement would not validate the minimality clauses.
- Situation seed: A projected-dDNNF FormulaEval line over H_N^SAT has visible RowSet S but an unread enable bit e that conditionally adds one private row r outside S; all non-FormulaEval proof lines are bit-explicit Psys_bEF^- lines.
- Varied variable: h_N, the number of hidden influential rows not enumerated or charged, varied from 0 to 1 while keeping q,rho,epsilon fixed.
- Held-fixed controls: M_N=N^{q+o(1)}, L_N=(log N)^d with d>1, beta=0, and generator size N^{rho+o(1)}., The visible transcript, charged RowSet S, Gamma_bEF, U_FE, and same nonuniform SIZE target model are held fixed., No real SAT semantic constraints are used in the spoof unless RealSATInfluenceRealizer_N supplies a charged certificate.
- Expected observation: At h_N=0 the line induction is valid and charges Gamma_trans. At h_N=1 two label worlds agree on all charged data but disagree on the private row, so the parser cannot soundly surface occurrence completion.
- Transfer certificate needed: A same-theory RealSATInfluenceRealizer_N certificate showing that the private row is forced by real SAT semantics and charging its support; without it, the two-world falsifier blocks promotion to full Psys_sym.

## Next Experiment

Instantiate RealSATInfluenceRealizer_N or refute it for one concrete strong rule: FormulaEval with Tseitin-extension equality plus bounded self-reduction; list exact bit fields, RowSet extraction, same-theory expansion certificates, and the first semantic inference that cannot be charged.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Restricted theorem packet: for Psys_sym^TRS, every accepted transparent FormulaEval proof pi of LB_N(1+epsilon) for H_N^SAT admits a deterministic no-advice parser producing a row-equivalent charge \widehat S_eff(pi). If rho<1+epsilon and \widehat S_eff(pi)<N^{epsilon-o(1)}, then the parsed transcript plus the generator gives a nonuniform circuit of size <N^{1+epsilon-o(1)} for H_N^SAT, a falsifier to the proved lower-bound sentence. Hence sound transparent proofs must pay \widehat S_eff(pi)>=N^{epsilon-o(1)}.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with N=2^n, M_N=N^{q+o(1)}, and generator circuit size N^{rho+o(1)} producing polylog-length SAT instances.
- target object: the nonuniform SIZE lower-bound sentence LB_N(1+epsilon) asserting C(H_N^SAT)>N^{1+epsilon-o(1)} in the same Boolean circuit model used by the parser-to-circuit falsifier.
- controlled interface: TransparentRowSupport_N for Psys_sym FormulaEval lines, consisting of visible selector code, proof-visible RowSet enumerator or full-scan charge, selector extensionality, influence closure, row-expansion witnesses, same-theory occurrence expansion, and no hidden row advice.
- target-preserving condition: every row whose SAT value can influence an accepted FormulaEval line is either listed in K_idx^+(pi), paid by E_N^*(pi), or paid by U_N(pi)/N, and the parser uses no semantic advice outside the proof-visible theory.

## Assumptions

- Model: nonuniform Boolean circuits for H_N^SAT and bit-explicit EF+SATeq+bounded-SR_h plus transparent FormulaEval proof lines for LB_N.
- Length regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, selector descriptions have size N^{sigma+o(1)}, and all o(1) losses are uniform along the chosen N subsequence.
- Uniformity/advice regime: the parser and RowSet enumerators are deterministic, advice-free, and run in poly(|pi|,M_N,N) time; nonuniformity is allowed only in the final circuit upper-bound falsifier, as in the target model.
- Same-theory regime: FormulaEval expansion, SATeq use, extension links, and bounded-SR_h rows are verified inside the same proof formalism; no external real-SAT oracle is charged as a proof line.
- Barrier scope: this is a proof-system transfer obstruction, not a natural-property proof of P != NP; naturalness pressure triggers only if the transcript is converted into a large constructive useful truth-table property.

## Equations

- canonical_charge: `\Gamma_{trans}(\pi)=\Gamma_{bEF}(\pi)+U_N(\pi)+X_N(\pi), \quad X_N=N E_N^*(\pi)+L_N(\pi)`. Valid when: Valid when TransparentRowSupport_N supplies visible row enumeration, influence closure, and same-theory expansion for every FormulaEval line of pi.
- row_equivalent_support: `\widehat S_{eff}(\pi)=\left\lceil \Gamma_{bEF}(\pi)/N \right\rceil+\left\lceil U_N(\pi)/N \right\rceil+E_N^*(\pi)+\left\lceil L_N(\pi)/N \right\rceil`. Valid when: Applies after all bEF, enumeration, FormulaEval expansion, and link-overhead charges have been normalized to row-sized circuit patches.
- upper_bound_falsifier: `C(H_N^{SAT}) \le N^{\rho+o(1)}+N\widehat S_{eff}(\pi)\,polylog(N)`. Valid when: Requires the generator circuit, charged row patches, and parsed transcript to live in the same nonuniform Boolean circuit target model.
- forced_support: `\rho<1+\epsilon \;\wedge\; \pi\text{ sound for }LB_N(1+\epsilon) \Rightarrow \widehat S_{eff}(\pi)\ge N^{\epsilon-o(1)}`. Valid when: Valid when the previous upper-bound falsifier inequality is target-preserving and LB_N uses the identical SIZE threshold.
- visible_density_corollary: `|K_{idx}^{+}(\pi)|/M_N \ge N^{\epsilon-q-o(1)} \quad \text{if } \Gamma_{bEF}/N+U_N/N+E_N^*+L_N/N=o(N^{\epsilon}) \text{ except visible rows}`. Valid when: Applies in the transparent regime when non-row debts are subthreshold and M_N=N^{q+o(1)} rows are the only remaining support source.

## Attempted Derivation

- Live packet source_statement: accepted Psys_sym^TRS proof pi of LB_N(1+epsilon) for H_N^SAT with N=2^n, M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and transparent FormulaEval support fields.
- Live packet target_statement: deterministic parser produces Gamma_trans and \widehat S_eff; if \widehat S_eff is subthreshold, the transcript yields a SIZE upper-bound falsifier for the claimed lower bound; hidden semantic FormulaEval is quarantined unless realized.
- Model context: source carrier is beta-zero SAT parity; target class is nonuniform Boolean SIZE; proof model is bit-explicit EF+SATeq+bounded-SR_h plus TRS FormulaEval; transfer type is simulation/extraction, not a many-one reduction.
- Quantifier context: rho<1+epsilon, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, h=N^{eta+o(1)}, selector code size N^{sigma+o(1)}, uniform advice-free parsing, nonuniformity only in the final circuit upper-bound object.
- Line induction base: bEF, SATeq, bounded-SR_h, and extension-link lines contribute exactly Gamma_bEF plus L_N by previously established bit-field parent-pointer accounting.
- FormulaEval step: TRS requires each FormulaEval line to expose either an enumerator for RowSet(a), a full scan, or an influence-complete expansion; charge the enumeration work to U_N and the row evaluations to N E_N^*.
- Invariant: after each line t, every row capable of changing the derived proof state is contained in K_idx^+(pi_{<=t}) or is represented by paid debt U_N/N, E_N^*, or L_N/N.
- Circuit reconstruction: hardwire the generator circuit of size N^{rho+o(1)}, simulate all charged transcript decisions, and patch only the row-equivalent support; this gives C(H_N^SAT)<=N^{rho+o(1)}+N\widehat S_eff polylog(N).
- Falsifier conclusion: if an accepted proof of LB_N(1+epsilon) has \widehat S_eff<N^{epsilon-o(1)} while rho<1+epsilon, then the reconstructed circuit violates the lower-bound sentence in the same target model, so such a proof is unsound.
- Hidden-support branch: when the invariant fails, choose an unread enable/private row j*, flip only that row, keep the visible transcript fixed, and obtain the same parser charge with different semantic FormulaEval behavior.

Blocking gap: The restricted TRS line induction is now theorem-shaped, but the unrestricted Psys_sym lift is blocked exactly at RealSATInfluenceRealizer_N for arbitrary semantic FormulaEval-SAT atoms with shared extension syntax.

## Falsifiers

- Private-row/unread-enable-bit FormulaEval: a hidden row changes semantic acceptance while all visible TRS fields and Gamma_trans remain fixed.
- q<epsilon source-ceiling falsifier: the carrier has an N^{1+q+o(1)} style upper-bound route, so a claimed N^{1+epsilon} source lower bound is invalid when q<epsilon-o(1).
- Opaque selector advice falsifier: RowSet(a) is encoded semantically but not enumerably, so U_N is zero while support can range over M_N rows.
- Shared-DAG substitution falsifier: one displayed FormulaEval atom can semantically cover many generator rows unless RealSATInfluenceRealizer_N expands the influence.
- Naturalness falsifier boundary: if the transcript is turned into a poly(N)-constructive dense useful truth-table property, PRF tension applies; if it remains proof-system-specific and nonlarge, that particular barrier is not triggered.

## Learning

Cycle 116 consolidates the TRS theorem pair into a canonical charge invariant: transparent FormulaEval proofs must pay row-equivalent support \widehat S_eff, and subthreshold charge gives a same-model SIZE upper-bound falsifier for LB_N(1+epsilon). The hidden-support countermodel is now a bisimulation theorem, while the unrestricted semantic lift remains blocked only at RealSATInfluenceRealizer_N. This is route-level proof-system certification, not progress on P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for RealSATInfluenceRealizer_N.`
- Rationale: The branch already has abstract TRS charges; the remaining uncertainty is whether a concrete semantic FormulaEval line can hide a row influence while preserving the same LB_N target and exponent regime.
- Situation seed: A padded SAT-query parity family H_N^SAT(x)=xor_{j<=N^q} SAT(G_N(x,j)) with one Psys_sym FormulaEval line evaluating a selector S_a. In the transparent version S_a is an interval-union enumerator; in the semantic version S_a contains an unread enable bit e_{j*} for a private row j*.
- Varied variable: Visibility fraction alpha of influential rows certified by TRS, from alpha=1 with full enumeration to alpha=1-N^{-q} with exactly one hidden private row.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, rho<1+epsilon, and the same generator G_N in both variants., The target lower-bound sentence LB_N(1+epsilon) and nonuniform SIZE model are unchanged., The displayed proof syntax, bEF parent pointers, bounded-SR_h fields, and all charged rows except j* are held fixed., The parser remains deterministic and advice-free; only FormulaEval support visibility is varied.
- Expected observation: At alpha=1 the Gamma_trans reconstruction is valid and forces \widehat S_eff>=N^{epsilon-o(1)} for sound proofs. With a single uncharged j*, two visible-identical transcripts can disagree semantically, giving the private-row falsifier and proving that surface occurrence charge is not target-preserving.
- Transfer certificate needed: A same-theory RealSATInfluenceRealizer_N certificate that turns every semantically influential row into visible RowSet support or charged U_N/X_N debt before any intuition from the experiment may affect proof obligations.

## Next Experiment

Run a proof-quality audit of TRS116_CanonicalChargeTheorem: instantiate one FormulaEval extension-rule line, write its visible bit fields, prove the invariant update for K_idx^+, U_N, E_N^*, L_N, and verify that the reconstructed circuit size remains N^{rho+o(1)}+N\widehat S_eff polylog(N).

# MCSP / Meta-Complexity Carrier Transfer supporting TransparentRowSupport_N proof packet

## Candidate Lemma

Restricted theorem: for every large N, any Psys_sym proof pi of LB_N(1+epsilon) whose FormulaEval lines satisfy TransparentRowSupport_N has a charged transcript with Gamma_trans(pi)=Gamma_bEF(pi)+U_N(pi)+X_N(pi). If the resulting same-model circuit upper bound is below N^{1+epsilon-o(1)}, pi is a valid low-cost-transcript falsifier for that lower-bound proof in this interface.

## Definitions

- source object: a Psys_sym^TRS proof pi of LB_N(1+epsilon) over H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with a bit-explicit bEF core transcript and FormulaEval lines.
- target object: the nonuniform SIZE model for H_N^SAT at parameter N, with target lower-bound statement LB_N(1+epsilon): C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)}.
- controlled interface: TransparentRowSupport_N consists of visible selector code, advice-free row enumeration or full-scan charge, influence closure, same-theory occurrence expansion, and no hidden semantic support advice.
- target-preserving condition: the parser, row enumerator, FormulaEval expansion, and generator G_N are uniform in N and produce circuits in the same nonuniform SIZE model used by LB_N(1+epsilon).
- K_idx(pi) is the deduplicated set of FormulaEval row indices whose SAT values can influence the accepted transcript after influence closure.
- U_N(pi) is the charged cost of discovering the union of visible row supports, including selector code, enumerator overhead, or full scan.
- X_N(pi) is the charged cost of expanding the selected SAT rows into same-theory occurrence neighborhoods used by the bEF parser.

## Assumptions

- Model: the bEF core rules already satisfy Gap98-SRhNormalForm, so each non-FormulaEval inference has explicit bit fields, parent pointers, and local verifier cost charged in Gamma_bEF(pi).
- Regime: M_N=N^{q+o(1)}, the generator G_N has circuit overhead N^{rho+o(1)}, epsilon,q,rho are fixed constants on the selected length sequence, and all o(1) terms are uniform over pi.
- Uniformity/advice: selector code and row enumerators are either printed in pi or generated from N without advice; nonuniformly chosen hard rows are not allowed as source evidence.
- Influence closure: every row whose SAT value can change acceptance, the forced parity, or the lower-bound certificate is included in K_idx(pi) or supplied by a charged RealSATInfluenceRealizer_N witness.
- Same-theory condition: occurrence expansion uses the same SAT encoding and proof language as the bEF parser; no semantic FormulaEval value is imported as an oracle fact.

## Equations

- GammaLedger: `\Gamma_{\mathrm{trans}}(\pi)=\Gamma_{\mathrm{bEF}}(\pi)+U_N(\pi)+X_N(\pi).`. Valid when: Valid when every FormulaEval line satisfies TransparentRowSupport_N and duplicate row charges are merged by the incremental union ledger.
- TranscriptCircuitBound: `C_{\mathrm{SIZE}}(H_N^{\mathrm{SAT}})\le N^{\rho+o(1)}+\Gamma_{\mathrm{trans}}(\pi).`. Valid when: Applies when the proof certificate is beta-zero target-preserving and the charged transcript computes every SAT row that can affect H_N^SAT.
- ExponentLedger: `N^{\rho+o(1)}+\Gamma_{\mathrm{trans}}(\pi)=N^{\max\{\rho,g,u,x\}+o(1)}\quad\text{if }\Gamma_{\mathrm{bEF}}=N^{g+o(1)},\ U_N=N^{u+o(1)},\ X_N=N^{x+o(1)}.`. Valid when: Requires fixed exponents g,u,x,rho and polynomially bounded sums over the chosen length sequence.
- SubthresholdNoProof: `\max\{\rho,g,u,x\}<1+\epsilon\ \Rightarrow\ \pi\text{ is not a sound proof of }LB_N(1+\epsilon).`. Valid when: Valid when LB_N(1+epsilon) asserts a same-model SIZE lower bound above N^{1+epsilon-o(1)} for H_N^SAT.
- RowExpansionCharge: `X_N(\pi)\ge E_N\,|K_{\mathrm{idx}}(\pi)|,\qquad E_N=N^{1+o(1)}.`. Valid when: Valid when same-theory occurrence expansion materializes every visible influential SAT row with bit-level formula encoding cost E_N.

## Attempted Derivation

- Source_statement: Psys_sym^TRS proof pi uses a bit-explicit Psys_bEF^- core plus FormulaEval lines over H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)).
- Target_statement: prove a scoped parser obstruction, namely that subthreshold Gamma_trans(pi) implies a same-model SIZE upper bound contradicting LB_N(1+epsilon) for that proof; this is not a proof of P != NP.
- Model_context: source carrier is a transparent proof transcript, target class is nonuniform SIZE for H_N^SAT, and the reduction type is parser-to-circuit simulation with no nonuniform row-selection advice beyond charged transcript bits.
- Quantifier_context: for all sufficiently large N on the chosen length sequence, M_N=N^{q+o(1)}, generator overhead is N^{rho+o(1)}, epsilon is constant, and all enumerators/realizers are N-uniform or printed and charged.
- Induction base: Gap98-SRhNormalForm supplies explicit verifier fields for bEF rules, so non-FormulaEval lines increase the circuit transcript cost by exactly their Gamma_bEF contribution.
- Transparent FormulaEval step: the visible selector enumerates new rows or pays full scan; the incremental union ledger charges only first discoveries to U_N; same-theory occurrence expansion charges X_N; influence closure prevents uncharged semantic dependence.
- Circuit simulation: hardwire the charged transcript and selector code, compute G_N with N^{rho+o(1)} overhead, evaluate exactly the charged SAT occurrence neighborhoods, and compose the beta-zero parity certificate inside the same SIZE model.
- Subthreshold contradiction: if max{rho,g,u,x}<1+epsilon, the constructed circuit is smaller than the lower-bound threshold asserted by LB_N(1+epsilon), so a sound proof pi in this interface cannot exist.
- Negative branch: if influence closure first fails at row j*, build two formula completions agreeing on all visible bits but differing on SAT(G_N(x,j*)); the same transcript then supports different parities, giving a private-row falsifier for the parser claim.
- Reviewer_findings: reduction consistency is valid only for same-model SIZE; quantifier uniformity passes for printed or N-uniform selectors; barrier specificity says the result is nonrelativizing only if RealSATInfluenceRealizer_N handles real semantic SAT, otherwise it is a semantic-oracle quarantine.

Blocking gap: RIR-116: RealSATInfluenceRealizer_N is not proved for unrestricted real semantic FormulaEval-SAT; the positive theorem is complete for TransparentRowSupport_N but full semantic SAT remains outside the controlled interface.

## Falsifiers

- falsifier: one hidden influential FormulaEval row j* with no charged occurrence expansion yields two completions agreeing on the visible transcript but differing on H_N^SAT parity.
- falsifier: a selector that uses per-length advice to name K_idx(pi) violates the source uniformity condition and cannot target-preserve the SIZE lower-bound statement.
- falsifier: a membership-only AC0 or semantic selector with no output-sensitive enumerator pays full scan N^{1+q+o(1)} or becomes a private-row case.
- falsifier: if q<epsilon and the proof requires density |K_idx|/M_N>=N^{epsilon-q-o(1)}, the density demand exceeds the available row universe, so the claimed low-contact proof cannot be valid.
- falsifier: importing SAT-extensionality without a same-theory quotient or influence witness is a semantic-oracle model change, not a proof in the transparent parser interface.

## Learning

Cycle 116 turns the prior TransparentRowSupport_N slogan into an auditable theorem-pair packet: transparent FormulaEval contributes exactly U_N+X_N to Gamma_bEF, while the first uncharged semantic influence gives a finite private-row falsifier. The only remaining full-system gap is RealSATInfluenceRealizer_N, so the contribution is a scoped parser obstruction, not progress on the main P vs NP conjecture.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The remaining proof boundary is semantic visibility of FormulaEval influence, not another abstract MCSP carrier slogan; a finite unread-bit experiment tests the exact private-row countermodel and the RealSATInfluenceRealizer_N escape.
- Situation seed: Use the padded SAT-query family G_N(x,j) with M_N=N^{q+o(1)}. For one row j* add an enable bit e_{j*} controlling a satisfiable disjunct, and arrange that the FormulaEval selector transcript reads all visible rows K_idx but not e_{j*}.
- Varied variable: h, the number of semantically influential FormulaEval rows omitted from the visible charged support, varied from h=0 to h=1 and then to h=N^{a+o(1)}.
- Held-fixed controls: The target function remains H_N^SAT and the target class remains the same nonuniform SIZE model used by LB_N(1+epsilon)., The generator overhead N^{rho+o(1)}, row count M_N=N^{q+o(1)}, and bEF core parser Gamma_bEF(pi) are held fixed., No advice is allowed for choosing j* or K_idx; all visible support must be printed or N-uniform and charged., The proof language and SAT formula encoding are the same on both completions.
- Expected observation: At h=0 the Gamma_trans line induction is stable. At h>=1 two occurrence completions have the same transcript but opposite SAT value at j*, producing the hidden-support falsifier. If h=N^{a+o(1)} is made transparent, X_N increases by N^{1+a-o(1)} and may cross the lower-bound threshold.
- Transfer certificate needed: A RealSATInfluenceRealizer_N theorem proving that every semantically influential row has an advice-free same-theory witness and is charged in U_N+X_N before the parser-to-circuit simulation is treated as valid.

## Next Experiment

Write the paper-ready theorem text for TRS116.PositiveParserLedger and TRS116.HiddenSupportCountermodel, then attempt RealSATInfluenceRealizer_N on one concrete semantic FormulaEval rule; if no complete advice-free witness relation appears, quarantine that rule as semantic-oracle FormulaEval.
