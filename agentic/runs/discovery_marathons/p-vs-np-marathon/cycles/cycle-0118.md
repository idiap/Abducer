# cycle-0118

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Compositional TransparentRowSupport closure theorem for extensional FormulaEval: for beta-zero XOR SAT carriers, every Psys_sym^ext proof whose FormulaEval influence cones are either surfaced and charged or included in a charged RealSATInfluenceRealizer closure parses to a Gamma_comp transcript; if the transcript is subthreshold, it is a valid nonuniform circuit falsifier for the claimed LB_N(1+epsilon).

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, polylog formula length L_N=(log N)^d, d>1, and generator circuit size N^{rho+o(1)}.
- target object: the route-level lower-bound assertion LB_N(1+epsilon): C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)} in the same nonuniform SIZE model; the target is not P != NP.
- controlled interface: Psys_sym^ext consists of bit-explicit bEF lines, explicit bounded-SR_h rules, SATeq links, and extensional FormulaEval lines with visible selector code, row enumerators or full-scan charge, influence closure, and same-theory occurrence expansion.
- target-preserving condition: beta=0, q,rho<1+epsilon, all proof support is advice-free or charged, SR_h overhead eta+tau is explicit, and every FormulaEval semantic influence is either surfaced in K_idx or certified by RealSATInfluenceRealizer_N.

## Assumptions

- Length regime: N ranges over the valid carrier lengths, M_N=N^{q+o(1)}, L_N=N^{o(1)}, and all o(1) terms are uniform over the proof family.
- Circuit model: nonuniform Boolean circuits with fan-in two and equality patches charged by O(N) per exceptional source row.
- Proof model: every bEF extension variable has bit-explicit dependency support; bounded-SR_h rules expose parent pointers, leaf SAT calls, eta/tau branching overhead, and touched occurrence neighborhoods.
- FormulaEval model: an extensional FormulaEval line has a finite syntactic influence cone I_l over generated SAT rows, independent of SAT truth labels except through declared row labels.
- Same-theory condition: occurrence expansions and row enumerators are checkable inside the same Psys_sym^ext syntax, so parsed support cannot be imported as external advice.
- Realizer condition: R_FE(pi) charges every row whose influence is not visible syntactically but is forced by real SAT semantics; without this charge the result is only an extensional-label theorem.
- Non-claim: the lemma gives a parser/falsifier boundary for a magnification route and does not prove NP not subset P/poly or P != NP.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j=1}^{M_N} SAT(G_N(x,j))`. Valid when: Valid when the generated instance family G_N is fixed, advice-free, and has M_N=N^{q+o(1)} indexed rows of polylogarithmic target length.
- composite_transcript_charge: `\Gamma_{comp}(\pi)=\Gamma_{bEF}(\pi)+B_{SR_h}(\pi)+U_{FE}(\pi)+X_{FE}(\pi)+R_{FE}(\pi)`. Valid when: Applies after bit-explicit EF support, bounded SR_h fields, transparent FormulaEval enumeration, expansion charges, and semantic realizer rows are all separately charged.
- sr_charge: `B_{SR_h}(\pi)\le N^{q+\eta+\tau+o(1)}`. Valid when: Valid when the bounded self-reduction rule has at most N^{\eta+o(1)} leaves per active row and leaf verifier overhead N^{\tau+o(1)}.
- parser_upper_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{comp}(\pi)+E_N N`. Valid when: Requires the parser to produce a same-model circuit for all but E_N exceptional source rows, with equality patches charged nonuniformly per row.
- falsifier_window: `N^{\rho+o(1)}+\Gamma_{comp}(\pi)+E_NN<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Valid when LB_N is stated in the identical nonuniform SIZE model and the parsed circuit computes the carrier on every valid input length.
- support_density_corollary: `|K_{idx}(\pi)|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Follows only when all other transcript terms are subthreshold and FormulaEval support is the remaining necessary charged source of hardness.

## Attempted Derivation

- Define the influence cone I_l for each FormulaEval line l as the set of generated row labels whose flip can change the line value with all visible syntax fixed.
- For transparent lines, enumerate I_l by the visible selector code or charge a full scan over M_N rows; add U_l+X_l to Gamma_comp.
- For bEF, SATeq, and bounded-SR_h lines, reuse the bit-explicit dependency parser and SR_h field parser; add Gamma_bEF and B_SR_h to Gamma_comp.
- For hidden FormulaEval lines, either a same-theory RealSATInfluenceRealizer_N lists the forced influence rows and contributes R_FE, or mark the line unsafe.
- If no unsafe line remains, perform line induction: every proof line is simulated by a circuit using the generator, charged row labels, charged SR leaves, and charged FormulaEval expansions.
- The final line gives a circuit for H_N except on E_N explicitly residual rows; equality patches yield C(H_N)<=N^{rho+o(1)}+Gamma_comp(pi)+E_NN.
- If an unsafe line remains, choose the last unsafe line whose hidden row reaches the final output without later charged realization. Flip that row in an extensional two-world model while fixing all charged rows; the transcript is identical but the induced parity differs.
- Conclude that surfaced influence plus realizer closure is sufficient for the parser, and failure of both is a private-row falsifier for extensional FormulaEval.

Blocking gap: The last-unsafe-line argument is valid in the extensional label model. For real SAT semantics, a hidden row may be forced by nonrelativizing formula identities, self-reduction constraints, or EqSAT links without being syntactically visible. That exact gap is RealSATInfluenceRealizer_N.

## Falsifiers

- Subthreshold Gamma_comp falsifier: N^{rho+o(1)}+Gamma_comp(pi)+E_NN<N^{1+epsilon-o(1)} contradicts any claimed LB_N(1+epsilon) in the same SIZE model.
- Private-row falsifier: an unsurfaced nonsemantic FormulaEval influence outside K_idx union R_FE yields two label worlds with identical transcript and different carrier parity.
- Unread-enable-bit falsifier: a selector whose enabling bit is never surfaced can switch a row into the influence cone without changing the charged transcript.
- Threshold-collapse falsifier: if q+eta+tau, U_FE, X_FE, or R_FE reaches 1+epsilon, the parser theorem may remain valid but no barely-superlinear lower-bound contradiction follows.
- Model-mismatch falsifier: a proof that treats semantic SAT implications as occurrence support without a same-theory realizer leaks nonuniform advice into the source lower-bound certificate.

## Learning

Cycle 118 adds a compositional repair to the FormulaEval boundary: local surfaced influence is not enough unless hidden influences are closed under later proof use. The valid restricted theorem is Psys_sym^ext plus charged RealSATInfluenceRealizer_N rows implies Gamma_comp line induction and the LB_N falsifier window. The necessity direction is now a last-unsafe-line private-row theorem. Full semantic FormulaEval remains open exactly at a nonrelativizing realizer lemma, not at generic relativization, natural-proofs, or P vs NP folklore.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the compositional necessity direction.`
- Rationale: The current route no longer needs another abstract TransparentRowSupport restatement; it needs a concrete test showing whether local unsurfaced influence survives whole-proof composition or is repaired by a semantic realizer charge.
- Situation seed: A beta-zero XOR carrier with M_N=N^q generated SAT rows and one guarded FormulaEval line Eval(sel_e(x),phi) where an unread enable bit e controls whether a private row r* is included; later proof lines use only the FormulaEval value and visible rows unless RealSATInfluenceRealizer_N lists r*.
- Varied variable: The realizer-closure exponent kappa defined by |R(pi)|=N^{kappa+o(1)} hidden forced rows.
- Held-fixed controls: M_N=N^{q+o(1)} with q<1+epsilon and L_N=(log N)^d, d>1, so beta=0 is fixed., Generator size is N^{rho+o(1)} with rho<1+epsilon., bEF and bounded-SR_h parser charges are already below N^{1+epsilon-o(1)}., Circuit target model remains nonuniform SIZE with equality patch cost O(N) per residual row.
- Expected observation: For kappa<epsilon and no listed r*, the private-row worlds agree on the charged transcript while flipping H_N on a chosen input, so the proof is not surface-complete. If every such r* is listed, R_FE contributes N^{1+kappa+o(1)} and the q/epsilon density pressure reappears.
- Transfer certificate needed: A formal last-unsafe-line lemma for extensional FormulaEval plus a nonrelativizing RealSATInfluenceRealizer_N theorem for any use of real SAT semantics before the thought experiment may affect unrestricted Psys_sym proof obligations.

## Next Experiment

Run a finite proof audit on Psys_sym^ext: instantiate one guarded FormulaEval line, compute I_l, K_idx, R_FE, and Gamma_comp, then verify the last-unsafe-line two-world construction or identify the first real SAT-semantic rule that forces a nonrelativizing realizer charge.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Restricted theorem: every Psys_sym^TRS proof pi of LB_N(1+epsilon) admits an advice-free same-theory row-expanded bEF transcript of size Gamma_trans(pi). Hence a subthreshold Gamma_trans is a same-model falsifier to the claimed lower bound, while sound transparent proofs must pay row-equivalent support N^{epsilon-o(1)} when rho<1+epsilon.

## Definitions

- source object: beta-zero SAT-parity carrier H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with N=2^n, M_N=N^{q+o(1)}, and generator G_N of circuit size N^{rho+o(1)}.
- target object: same-length nonuniform lower-bound assertion LB_N(1+epsilon): C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)} as formalized inside Psys_sym^TRS.
- controlled interface: TransparentRowSupport_N certificate per FormulaEval line, consisting of visible selector code, advice-free RowSet enumeration or full-scan charge, influence closure, row expansion template, same-theory occurrence replacement, and no-hidden-advice check.
- target-preserving condition: every FormulaEval expansion uses the same SAT predicate, same row generator, same nonuniform SIZE target, and no semantic oracle or nonuniform row advice beyond the proof-visible certificate.
- Gamma_bEF(pi) is the already audited bit-explicit charge for non-FormulaEval EF+SATeq+bounded-SR_h lines.
- U_N(pi) is the total proof-visible enumeration debt for row selectors; X_N(pi) is the explicit row-expansion debt, including N E_N^* for E_N^* certified row instantiations.

## Assumptions

- Model: nonuniform Boolean SIZE on inputs of length N, with proof extraction used only as a simulation/falsifier, not as a many-one reduction proving P != NP.
- Regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, row generator size N^{rho+o(1)}, and rho<1+epsilon for forced-charge consequences.
- Uniformity: the TRS checker and row enumerators are deterministic and advice-free in poly(|pi|,N,M_N) time; selector code is proof-visible.
- Same-theory condition: replacing a FormulaEval line by its expanded rows preserves the formal SAT formula being evaluated and does not add real-SAT semantic axioms.
- Parser dependency: the Gap98-bEF parser theorem is available for the non-FormulaEval fragment with its eta/tau overhead already charged in Gamma_bEF.
- Soundness cutoff: if Psys_sym^TRS proves LB_N(1+epsilon), then any produced SIZE circuit below N^{1+epsilon-o(1)} is a valid contradiction to that proof, not a proof of the global conjecture.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j))`. Valid when: Valid when N=2^n, the row generator G_N is uniform and explicit, and M_N is the audited beta-zero row count.
- transparent_charge: `\Gamma_{trans}(\pi)=\Gamma_{bEF}(\pi)+U_N(\pi)+X_N(\pi)+O(|\pi|\operatorname{polylog}N)`. Valid when: Applies after non-FormulaEval lines are parsed by Gap98-bEF and every FormulaEval line passes TransparentRowSupport_N.
- row_expansion_debt: `X_N(\pi)=N\,E_N^*(\pi)+F_N(\pi)\,N^{1+q+o(1)}`. Valid when: Valid when E_N^* counts TRS-certified row instantiations and F_N counts full-scan FormulaEval mechanisms rather than hidden semantic access.
- parser_upper_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{trans}(\pi)`. Valid when: Requires the same nonuniform SIZE model and a no-advice parser-to-circuit simulator from the expanded transcript.
- forced_charge: `\Gamma_{trans}(\pi)\ge N^{1+\epsilon-o(1)}-N^{\rho+o(1)}`. Valid when: Applies when the proof is sound for LB_N and rho is bounded below 1+epsilon by a fixed margin.
- row_equivalent_support: `\widehat S_{eff}(\pi)=\left\lceil\Gamma_{bEF}(\pi)/N\right\rceil+\left\lceil U_N(\pi)/N\right\rceil+E_N^*(\pi)+F_N(\pi)N^{q+o(1)}`. Valid when: Valid in the transparent support model where all charged terms are convertible into row-equivalent support units.
- visible_density_corollary: `|K_{idx}(\pi)|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Requires small bEF and enumeration debt plus M_N=N^{q+o(1)} in the beta-zero row regime.

## Attempted Derivation

- Fix N=2^n, M_N=N^{q+o(1)}, generator G_N, target LB_N(1+epsilon), and an accepted Psys_sym^TRS proof pi.
- Run the Gap98-bEF parser on every non-FormulaEval line; charge its bit fields, parent pointers, row-index encodings, bounded-SR_h neighborhoods, and eta/tau overhead to Gamma_bEF(pi).
- For each FormulaEval line, run the finite TRS checker. If it supplies an explicit RowSet enumerator, enumerate rows and charge U_i; if it declares full scan, charge N^{1+q+o(1)}; if it supplies E_i row instantiations, charge N E_i.
- Use influence closure to replace the FormulaEval line by the same-theory collection of row-expanded SAT occurrence clauses, with no new semantic SAT axiom and no hidden selector advice.
- Concatenate the expanded blocks in proof order. Parent references remain valid because each FormulaEval value is replaced before its descendants and extension variables receive fresh local names.
- Sum the line charges to obtain Gamma_trans(pi)=Gamma_bEF(pi)+U_N(pi)+X_N(pi)+O(|pi|polylog N).
- Invoke the same-model parser-to-circuit simulator: generator circuitry plus expanded transcript yields C(H_N^SAT)<=N^{rho+o(1)}+Gamma_trans(pi).
- If this upper bound is below N^{1+epsilon-o(1)}, it is a valid falsifier to the soundness of a purported proof of LB_N(1+epsilon); otherwise Gamma_trans must be at least the forced threshold.
- Normalize by N to obtain row-equivalent support. If Gamma_bEF and U_N are subdominant and no full scans occur, the visible FE support density is at least N^{epsilon-q-o(1)}.

Blocking gap: The derivation does not prove RealSATInfluenceRealizer_N for unrestricted semantic FormulaEval; it cannot extract hidden real-SAT influence rows without a visible certificate, full-scan charge, or advice-free semantic-locality theorem.

## Falsifiers

- private-row/unread-enable-bit falsifier: one hidden influential row changes FormulaEval semantics while the displayed transcript and surface Gamma charge remain identical
- q<epsilon source-ceiling falsifier: the trivial rowwise construction gives C(H_N^SAT)<=N^{1+q+o(1)}, contradicting any claimed N^{1+epsilon} source lower bound when q<epsilon-o(1)
- semantic-oracle FormulaEval falsifier: a verifier may accept using real-SAT meaning while no advice-free RowSetEnumerator_N exists for the parser
- natural-property falsifier: if the expanded certificate becomes poly(N)-constructive, N^{-O(1)}-dense, and useful against the same SIZE class, PRF tension applies and the route must name a valid escape

## Learning

Cycle 118 adds the missing same-theory expansion step: TRS visibility is not merely a finite checker condition; it lets each transparent FormulaEval line be replaced by charged row-expanded bEF material, yielding Gamma_trans and the subthreshold SIZE falsifier. The unrestricted semantic lift remains blocked exactly at RealSATInfluenceRealizer_N, and the private-row construction is the finite no-go object.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The theorem pair hinges on whether one uncharged semantic row can alter the proof while preserving the same target carrier and SIZE model. A concrete hidden-row experiment tests the exact TRS clauses rather than restating natural-proofs or relativization folklore.
- Situation seed: Take H_N^SAT(x)=xor_{j<=M_N}SAT(G_N(x,j)) and add one FormulaEval extension A_e whose visible selector is empty but whose semantic evaluator secretly includes row r when an unread enable bit e=1.
- Varied variable: lambda, the number of uncharged hidden influential rows, varied over 0, 1, and N^alpha while keeping the displayed proof syntax fixed.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and target lower-bound threshold N^{1+epsilon-o(1)}, same nonuniform SIZE target model and same SAT predicate used by the transparent expansion theorem, same displayed proof length, bEF transcript, selector text, and claimed FormulaEval line type, no nonuniform row advice available to the parser
- Expected observation: For lambda=0 the TRS expansion is valid and Gamma_trans charges all influence. For lambda=1 the surface parser misses row r unless it charges all possible rows, proving that hidden semantic support is not target-preserving without RealSATInfluenceRealizer_N.
- Transfer certificate needed: A proof of RealSATInfluenceRealizer_N showing that every semantic FormulaEval influence has an advice-free visible TRS certificate, or a theorem that the rule must pay full-scan charge N^{1+q+o(1)} before it enters Gamma_trans.

## Next Experiment

Attempt RealSATInfluenceRealizer_N for one concrete semantic rule: AC0 output-sensitive FormulaEval with proof-visible circuit and no advice. Either derive a TRS certificate with U_N output-sensitive enumeration, or instantiate the hidden-row bisimulation as a formal counterexample.

# MCSP / Meta-Complexity Carrier Transfer supporting TransparentRowSupport_N theorem pair

## Candidate Lemma

TransparentRowSupport_N lines admit a valid same-model parser-to-circuit simulation: for any bit-explicit Psys_bEF^- transcript pi proving LB_N(1+epsilon) for H_N^SAT, if every FormulaEval line has visible advice-free support enumeration or full-scan charge, influence closure, and same-theory occurrence expansion, then Gamma_trans(pi)=Gamma_bEF(pi)+U_N(pi)+X_N(pi). Hence N^{rho+o(1)}+Gamma_trans(pi)N^{o(1)}<N^{1+epsilon-o(1)} is a falsifier for the claimed nonuniform SIZE lower bound, not a proof of P != NP.

## Definitions

- source object: a bit-explicit Psys_bEF^- proof transcript pi over H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), augmented with FormulaEval lines and the previously established bounded-SR_h parser ledger Gamma_bEF(pi).
- target object: the finite lower-bound assertion LB_N(1+epsilon) meaning C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)} in the same nonuniform Boolean circuit model used by the parser simulation.
- controlled interface: each FormulaEval line exposes selector code S_l, an advice-free RowEnum_l or declared full scan, a realized influence set K_l, duplicate-safe incremental row-union accounting, and occurrence expansion of the selected SAT instances inside the same proof theory.
- target-preserving condition: the expansion uses the same G_N(x,j), same length N, same M_N=N^{q+o(1)}, same nonuniform SIZE target, no hidden advice, and no semantic SAT influence outside the charged row support.

## Assumptions

- Model: Psys_bEF^- has bit fields, parent pointers, bounded-SR_h normal form, and a valid line-induction parser for non-FormulaEval rules.
- FormulaEval regime: every transparent line either enumerates exactly its influential rows with cost U_l or pays full scan cost N^{1+q+o(1)}; duplicate rows are charged only at first appearance.
- Generator regime: G_N has nonuniform circuit size N^{rho+o(1)}, M_N=N^{q+o(1)}, and each generated SAT instance has polylogarithmic formula length so row expansion has the stated N^{o(1)} overhead.
- Quantifiers: epsilon>0 is fixed, q and rho are fixed exponents, o(1) terms are uniform over the considered proof family, and all claims are finite-length theorem-packet claims.
- Uniformity/advice: the parser, row enumerators, and influence witnesses are advice-free and encoded in pi; nonuniformity enters only through the final SIZE upper-bound circuit.
- Non-claim: this lemma refutes subthreshold transcript certificates for LB_N(1+epsilon); it does not construct hard SAT parity functions and does not prove P != NP.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)}`. Valid when: Valid when the source carrier is the beta-zero SAT parity family with polylogarithmic generated formulas and fixed exponent q.
- transparent-ledger: `\Gamma_{trans}(\pi)=\Gamma_{bEF}(\pi)+U_N(\pi)+X_N(\pi)`. Valid when: Valid when every FormulaEval influence is either enumerated advice-free or paid by a full scan and then occurrence-expanded.
- upper-bound-simulation: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{trans}(\pi)N^{o(1)}`. Valid when: Applies after the parser transcript and generator circuit are combined in the same nonuniform SIZE target model.
- lb-falsifier-threshold: `N^{\rho+o(1)}+\Gamma_{trans}(\pi)N^{o(1)}<N^{1+\epsilon-o(1)}\Rightarrow \pi \text{ cannot validly prove } LB_N(1+\epsilon)`. Valid when: Requires the target lower-bound statement to use the same nonuniform circuit model and the transparent parser simulation to be sound.
- support-density-charge: `X_N(\pi)\ge N^{1+o(1)}\,|K_{idx}(\pi)|`. Valid when: Valid when each newly influential row must be expanded to its occurrence-level SAT contribution rather than treated as semantic advice.

## Attempted Derivation

- Define Infl_l as the set of rows whose SAT/enable values can change FormulaEval line l while all prior charged fields are fixed.
- For transparent l, require RowEnum_l or full scan to output a superset of Infl_l, and require same-theory occurrence expansion for each newly discovered row.
- Maintain an incremental union K_idx^{<=l}; charge U_l for discovery and charge X_l only for rows in K_idx^{<=l}\K_idx^{<l}. This closes the duplicate-counting gap left by selector-by-selector packets.
- Run the established Psys_bEF^- line induction unchanged on non-FormulaEval rules, contributing Gamma_bEF(pi).
- At a FormulaEval line, substitute the charged row occurrences for the semantic value; influence closure guarantees the substituted line is invariant under every uncharged occurrence completion.
- The resulting occurrence transcript has size Gamma_bEF(pi)+U_N(pi)+X_N(pi) up to N^{o(1)} encoding overhead, proving the Gamma_trans ledger.
- Combine the transcript circuit with the generator circuit for G_N to compute H_N^SAT in size N^{rho+o(1)}+Gamma_trans(pi)N^{o(1)}.
- If this upper bound is below N^{1+epsilon-o(1)}, the proof pi cannot be a valid proof of LB_N(1+epsilon) in the same nonuniform SIZE model.
- For a nontransparent line, choose the first uncharged influential row and build two occurrence completions agreeing on all charged/read fields but flipping the private row; this proves the hidden-support falsifier.

Blocking gap: Full semantic FormulaEval-SAT remains blocked exactly at RealSATInfluenceRealizer_N: can unparsed SAT extensionality be converted to advice-free influence witnesses with a declared R_N charge?

## Falsifiers

- A FormulaEval line has a first uncharged influential row; the private-row/unread-enable-bit countermodel invalidates the parser.
- RowEnum_l is membership-only, semantic, or advice-selected; then U_N is not a valid advice-free discovery cost.
- The selector enumerates projected witnesses but not distinct projected rows; projection fiber entropy must be charged or the support claim is false.
- Gamma_trans is counted without incremental de-duplication; repeated selector examples can artificially inflate or hide the true threshold.
- Generator overhead rho or realized semantic overhead R_N already exceeds 1+epsilon; then the subthreshold contradiction disappears although the ledger theorem may remain valid.
- A claimed hard-row carrier chooses rows by nonuniform advice; this supports only nonuniform hard rows and not a target-preserving language lower bound.

## Learning

Cycle 118 improves the theorem pair by making the row ledger incremental and influence-complete: transparent FormulaEval is valid exactly because uncharged occurrence completions cannot change any line, while the first hidden semantic influence is a finite private-row falsifier. The branch contribution is a paper-level parser obstruction with exact same-model SIZE thresholds, not progress on P vs NP itself.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the hidden-support theorem and as a sanity check for the Gamma_trans ledger.`
- Rationale: The top proof item turns on whether semantic FormulaEval influence is visible and charged. A concrete private-row experiment tests the exact target-preserving boundary better than another abstract selector restatement.
- Situation seed: Fix H_N^SAT(x)=xor_{j<=N^q} SAT(G_N(x,j)). A proof line FormulaEval_L uses a selector whose visible code lists all rows except one row r*, while an unread enable bit e_{r*} gates SAT(G_N(r*)). The parser reads the visible selector, prior proof lines, and all charged occurrences but never reads e_{r*} or the private formula bit determining SAT(G_N(r*)).
- Varied variable: lambda=1 if r* is realized or full-scan charged, and lambda=0 if r* remains hidden semantic support; no other parameter is varied.
- Held-fixed controls: The same generator G_N, same M_N=N^{q+o(1)}, and same nonuniform SIZE target LB_N(1+epsilon) are held fixed., The surface proof transcript, bounded-SR_h fields, previously charged row occurrences, and parser read set are held fixed., No advice, no oracle row selector, and no change of SAT instance semantics are allowed between the two completions.
- Expected observation: At lambda=0, two completions agree on the parser transcript but differ in FormulaEval_L, giving a finite falsifier. At lambda=1, the row is charged in U_N+X_N or R_N and the Gamma_trans simulation remains valid.
- Transfer certificate needed: An advice-free RealSATInfluenceRealizer_N or explicit RowEnum/full-scan certificate proving Infl_l is contained in the charged row set before the FormulaEval value is used.

## Next Experiment

Write the paper-ready proof of HSC-118 first: formalize the first-hidden-influence minimality argument, construct y0,y1 occurrence completions, verify prior line preservation, and then cite it as the negative half of the TransparentRowSupport_N theorem pair.
