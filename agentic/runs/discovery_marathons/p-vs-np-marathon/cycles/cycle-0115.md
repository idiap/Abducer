# cycle-0115

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For the beta-zero parity carrier, a Psys_sym FormulaEval mechanism is parser-valid exactly when every row with possible carrier-parity influence is surfaced by a visible support enumerator or paid for by a full-scan/row-expansion charge. If an influential row is hidden, the private-row or unread-enable-bit construction is a valid falsifier for occurrence-completion parsing unless RealSATInfluenceRealizer_N supplies a nonrelativizing charged support certificate.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, SAT-instance length L_N=(log N)^d, generator size N^{rho+o(1)}, and source claim LB_N(1+epsilon): C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)}.
- target object: a Psys_sym lower-bound certificate using bit-explicit EF, SATeq links, bounded SR_h, and FormulaEval lines, parsed into a nonuniform SIZE circuit upper bound or rejected by a hidden-support countermodel.
- controlled interface: TransparentRowSupport_N consists of visible selector code, advice-free row enumeration or full scan, influence closure, same-theory occurrence expansion, and no hidden semantic support advice.
- target-preserving condition: the parser and the simulated circuit stay in the same nonuniform SIZE model, preserve beta=0 polylog SAT-query use, charge every surfaced row by N^{1+o(1)} when expanded, and do not infer real-SAT influence without a named nonrelativizing certificate.
- source_statement: A claimed proof of LB_N(1+epsilon) for H_N^SAT is acceptable only if no subthreshold parsed transcript computes the carrier in SIZE below N^{1+epsilon-o(1)}.
- target_statement: TransparentRowSupport_N yields Gamma_trans(pi) and hence an explicit circuit upper-bound falsifier; hidden FormulaEval support yields a two-world countermodel rather than a proof of LB_N.

## Assumptions

- model_context: Source circuits, parser circuits, equality patches, and generated SAT-substitution circuits are all nonuniform Boolean SIZE circuits with the same length parameter N.
- quantifier_context: Fix epsilon>0 and q,rho<1+epsilon; all inequalities are for sufficiently large N with o(1) terms uniform over the finite proof rule schema.
- uniformity_advice_status: Row enumerators may be nonuniform only through the proof string pi and visible selector code; no separate semantic advice may name hidden rows.
- same_theory_condition: SATeq and bounded SR_h links may constrain row labels only through charged bit-explicit occurrence neighborhoods or through a declared RealSATInfluenceRealizer_N output.
- barrier_status: The positive transparent theorem is relativizing at the occurrence-label level; the only valid full semantic escape is explicitly nonrelativizing and outside the private-row oracle countermodel.
- derivation_status: Transparent fragments are proved by line induction; full semantic FormulaEval remains blocked exactly at RealSATInfluenceRealizer_N, not at generic natural-proofs or algebrization folklore.
- reviewer_findings: reduction consistency checks the circuit upper bound, quantifier uniformity checks q,rho,epsilon and o(1), barrier specificity checks private-row relativization, and proof-derivation review checks the line induction.

## Equations

- GammaTrans: `Gamma_trans(pi)=Gamma_bEF(pi)+U_N(pi)+X_N(pi)+O(E_N N)`. Valid when: Valid when every FormulaEval influence is surfaced by TransparentRowSupport_N or charged by full scan and residual row errors are explicitly counted.
- ParsedCircuitUpperBound: `C_SIZE(H_N^SAT)<=N^{rho+o(1)}+Gamma_trans(pi)`. Valid when: Applies after the generator, all parsed proof lines, and all transparent FormulaEval row expansions are compiled into the same nonuniform SIZE model.
- LB_Falsifier_Window: `N^{rho+o(1)}+Gamma_trans(pi)+O(E_N N)<N^{1+epsilon-o(1)} => not LB_N(1+epsilon)`. Valid when: Requires the source lower-bound claim to be in the same SIZE model and the parser transcript to compute H_N^SAT on all but E_N patchable rows.

## Attempted Derivation

- Define the row universe R_N={(x,j):j<=M_N} and treat a FormulaEval line L as transparent only when its possible dependence set Infl_pi(L) is listed by visible selector code or charged by full scan.
- For transparent L, add enumerator cost U_N(L) and row-expansion cost X_N(L) to Gamma_trans; the existing bit-explicit line induction then compiles L into a circuit fragment without changing the SIZE model.
- For a hidden row r with Delta_r(L)=1 and r not in the charged support, build two occurrence-label worlds that agree on pi, visible selectors, EF support, SATeq links, and bounded SR_h neighborhoods but differ on SAT(r).
- If the proof transcript is identical in the two worlds while the carrier parity changes, the parser-to-circuit inference is invalid; this is the private-row/unread-enable-bit falsifier for hidden FormulaEval support.
- Contrapositively, any valid parser theorem for full semantic FormulaEval must prove that no such r exists, which is exactly the RealSATInfluenceRealizer_N obligation with charged output size.

Blocking gap: The transparent theorem and hidden-support countermodel are proof-shaped for occurrence-visible fragments, but the full semantic case is blocked by RealSATInfluenceRealizer_N: one must show that real SAT semantics forces every influential row into a charged support set.

## Falsifiers

- private-row falsifier: an uncharged influential FormulaEval row can be flipped while the visible proof transcript is fixed
- unread-enable-bit falsifier: a selector contains a dormant semantic enable bit whose active row is not surfaced by TransparentRowSupport_N
- q<epsilon support-density falsifier: absolute support below N^{epsilon-o(1)} gives a subthreshold parsed circuit after patching
- full-scan collapse: unenumerated transparent FormulaEval pays F_FE N^{1+q+o(1)}, which destroys the barely-superlinear window when q is too large
- nonuniform leakage falsifier: hidden selector advice names rows outside the proof bit string and invalidates the parser theorem
- positive-beta substitution cap: any black-box target-query exponent beta>0 leaves the transfer window q+beta c+o(1) and cannot exclude all SAT polynomial exponents

## Learning

Cycle 115 adds a minimality proof obligation to the promoted transparent-support theorem pair. Transparent FormulaEval is not just sufficient for a valid Gamma_trans parser; hidden influence is exactly what the private-row/unread-enable-bit falsifier exploits. Thus the full-system boundary is a named nonrelativizing RealSATInfluenceRealizer_N lemma, while the paper-level contribution remains a scoped parser/falsifier result rather than evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The theorem pair is already promoted; the remaining mathematical risk is whether hidden semantic FormulaEval can masquerade as transparent support. A concrete two-world private-row experiment tests exactly that parser obligation without restating hardness magnification.
- Situation seed: Take H_N^SAT(x)=xor_{j<=N^{q+o(1)}} SAT(G_N(x,j)) and add one FormulaEval line with a visible selector S plus an unread enable bit e. When e=0 the line appears to touch only S; when e=1 it also depends on a private row r whose SAT value changes the carrier parity.
- Varied variable: hidden_influence_count k_hid, with k_hid=0 for transparent support and k_hid=1 as the smallest private-row countermodel
- Held-fixed controls: M_N=N^{q+o(1)}, L_N=(log N)^d, generator size N^{rho+o(1)}, and q,rho<1+epsilon, the base Psys_bEF^- parser, SATeq links, bounded SR_h neighborhoods, and nonuniform SIZE target model, visible selector code and proof string pi are identical in the two worlds, no additional semantic advice is allowed except what RealSATInfluenceRealizer_N explicitly outputs and charges
- Expected observation: At k_hid=0 the line induction charges U_N+X_N and the Gamma_trans upper bound is valid. At k_hid=1 the two transcripts remain identical while H_N^SAT flips, proving that uncharged hidden FormulaEval support is a falsifier for occurrence completion.
- Transfer certificate needed: A valid transfer from this intuition to the proof queue requires either a formal private-row independence lemma for the chosen proof fragment or a nonrelativizing RealSATInfluenceRealizer_N theorem proving that the private row is impossible and charging the surfaced support.

## Next Experiment

Formalize the private-row independence lemma for one full symbolic FormulaEval rule with an unread enable bit: write the two transcripts, the charged constraint set, the flipped row r, and the proof that all visible lines agree while H_N^SAT parity differs; if independence fails, record the exact same-theory constraint as a RealSATInfluenceRealizer_N candidate.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

If a Psys_sym FormulaEval line lets an unread enable bit choose an influential SAT row not visible in K_idx^+, U_N, or X_N, then the surface Gamma_trans parser is not target-preserving; two equal visible transcripts compute different carriers.

## Definitions

- source object: Psys_sym proof pi for LB_N(1+epsilon) over H_e(x)=xor_j e_j SAT(G_N(x,j)) with one private enable bit e_{r_*}.
- target object: TransparentRowSupport_N parser producing K_idx^+(pi), U_N, X_N, Gamma_trans(pi), and a circuit upper-bound falsifier in nonuniform SIZE.
- controlled interface: visible selector code, row enumerator, influence closure, same-theory expansion, and no hidden advice are the only charged FormulaEval inputs.
- target-preserving condition: same beta-zero SAT-parity carrier, same N=2^n, M_N=N^{q+o(1)}, same SIZE threshold N^{1+epsilon}, and deterministic advice-free extraction.

## Assumptions

- Model is nonuniform Boolean SIZE with bit-explicit bEF plus FormulaEval-SAT; proof parsing is simulation/extraction, not a many-one reduction.
- Regime has generator size N^{rho+o(1)}, proof size poly(N), and rho<1+epsilon; q is arbitrary but fixed in M_N=N^{q+o(1)}.
- The hidden row is semantically influential: some x has SAT(G_N(x,r_*))=1 and r_* is absent from all visible charged row sets.
- The parser reads only proof-visible fields; it cannot query real SAT semantics or receive row-support advice.

## Equations

- surface_charge: `\Gamma_{surf}(\pi)=\Gamma_{bEF}(\pi)+U_N+X_N`. Valid when: Valid when the parser is restricted to visible proof fields and excludes hidden semantic FormulaEval support.
- hidden_toggle: `H_{e^1}(x)\oplus H_{e^0}(x)=\mathrm{SAT}(G_N(x,r_*))`. Valid when: Valid when the two semantic interpretations differ only at one unread enabled row r_*.
- visible_surrogate_bound: `C(T_{vis})\le N^{\rho+o(1)}+\Gamma_{surf}(\pi)`. Valid when: Valid when same-theory expansion builds circuits only from charged visible rows and generator gates.

## Attempted Derivation

- Fix pi and all visible selector/enumerator fields; choose r_* outside K_idx^+ and not charged in U_N or X_N.
- Define e^0,e^1 identical on visible fields, with e^0_{r_*}=0 and e^1_{r_*}=1; the surface parser outputs the same Gamma_surf and T_vis.
- For x with SAT(G_N(x,r_*))=1, H_{e^0}(x) and H_{e^1}(x) differ, while T_vis is unchanged; the parsed surrogate cannot certify the real carrier.
- Thus hidden semantic FormulaEval is a finite falsifier to occurrence completion unless a no-advice influence realizer exposes and charges r_*.

Blocking gap: The full positive theorem still needs RealSATInfluenceRealizer_N for arbitrary semantic FormulaEval-SAT atoms.

## Falsifiers

- Private-row falsifier: an unread enable bit selects r_* while all visible transcript fields and Gamma_surf stay fixed.
- Non-influence falsifier to the countermodel: if SAT(G_N(x,r_*))=0 for every x, the hidden row does not alter H_e.
- TRS repair falsifier: proof-visible extensionality enumerates r_* and charges it in K_idx^+ or U_N, making the surface parser valid again.
- Target-drift falsifier: if the claimed LB concerns T_vis instead of H_N^SAT, the argument is no longer target-preserving.

## Learning

Cycle 115 adds a finite hidden-enable FormulaEval countermodel: surface Gamma charge is valid only for TRS-visible influence. This is route-level proof-system certification and a live inference-quality packet source/target/model/quantifier update, not progress on P != NP.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The top theorem needs a concrete hidden-support no-go, not another selector class. The unread-enable experiment tests exactly whether Gamma_trans survives semantic FormulaEval without TRS.
- Situation seed: Beta-zero SAT-parity family H_e(x)=xor_{j<=M_N} e_j SAT(G_N(x,j)) with one FormulaEval atom whose enable bit e_{r_*} is private to real-SAT semantics.
- Varied variable: alpha in h=N^alpha hidden enabled rows, starting with alpha=0 for a single private row.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and LB threshold N^{1+epsilon}., Visible proof transcript, selector code, bEF lines, U_N, X_N, and no-advice parser are held fixed., Target class remains nonuniform SIZE and the reduction type remains same-theory extraction.
- Expected observation: Gamma_surf is insensitive to alpha, while the semantic carrier changes on any satisfiable hidden row; valid transfer therefore requires charging h rows or realizing them visibly.
- Transfer certificate needed: RealSATInfluenceRealizer_N: an advice-free procedure that maps every influential semantic FormulaEval row to visible K_idx^+, U_N, or X_N with preserved exponents.

## Next Experiment

Instantiate the countermodel with h=N^alpha hidden rows and compute the exact replacement charge: Gamma_trans plus N h or a visible realizer term; then fold it into the TRS theorem pair.

# MCSP / Meta-Complexity Carrier Transfer supporting TransparentRowSupport_N theorem pair

## Candidate Lemma

For Psys_sym FormulaEval lines satisfying TransparentRowSupport_N, the bit-explicit parser extends with exact incremental cost Gamma_trans=Gamma_bEF+U_N+X_N. If a claimed LB_N(1+epsilon) proof has N^{rho+o(1)}+Gamma_trans<N^{1+epsilon-o(1)}, the same SIZE model gets a circuit for H_N^SAT below the claimed bound. If the first FormulaEval line has uncharged semantic influence, the surface occurrence parser has a private-row or unread-enable-bit falsifier unless RealSATInfluenceRealizer_N supplies an advice-free witness.

## Definitions

- source object: Psys_sym transcripts pi over H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, polylogarithmic SAT formulas, and a Gap98-valid Psys_bEF^- base parser.
- target object: a nonuniform SIZE upper bound for the same H_N^SAT family and a scoped refutation of a proof-system claim LB_N(1+epsilon), not a proof of P != NP.
- controlled interface: TransparentRowSupport_N consists of visible selector code, advice-free row enumeration or full-scan charge, influence closure, same-theory occurrence expansion, no hidden support advice, row-discovery cost U_N, and row-expansion cost X_N.
- target-preserving condition: the simulation uses the same length N, the same H_N^SAT generator, the same nonuniform circuit model, the same proof theory after occurrence expansion, and charges every semantic influence unless RealSATInfluenceRealizer_N is valid.
- K_idx(pi) is the union of influential SAT row indices used by FormulaEval after transparent realization.
- U_N(pi) counts incremental row-discovery and selector-verification work; X_N(pi) counts incremental same-theory row expansion work.

## Assumptions

- Regime: N tends to infinity; q, rho, epsilon are fixed constants up to o(1) slack; M_N=N^{q+o(1)}; each G_N(x,j) has length polylog(N).
- Base model: Gap98-SRhNormalForm and the Gamma_bEF line induction are valid for the non-FormulaEval Psys_bEF^- fragment.
- Uniformity/advice: all selector codes, row enumerators, and row expansions are generated advice-free in time charged to U_N+X_N; no nonuniform hard-row choice is imported.
- Same-theory condition: FormulaEval expansion creates proof lines or extension definitions in the same formal system rather than appealing to an external SAT oracle.
- Influence-closure condition: every row whose SAT value can affect the FormulaEval line value, selected support, or subsequent proof state is either enumerated and charged or realized by RealSATInfluenceRealizer_N.
- Circuit target: the upper bound is in unrestricted nonuniform SIZE over the truth table inputs of H_N^SAT; generator overhead N^{rho+o(1)} is explicitly included.

## Equations

- GammaLedger: `\Gamma_{trans}(\pi)=\Gamma_{bEF}(\pi)+U_N(\pi)+X_N(\pi)`. Valid when: Valid when all FormulaEval lines satisfy TransparentRowSupport_N and U_N,X_N are defined incrementally over newly exposed rows.
- CircuitSimulation: `C_{SIZE}(H_N^{SAT}) \le N^{\rho+o(1)}+\Gamma_{trans}(\pi)`. Valid when: Applies after the generator circuit and parsed transcript are composed in the same nonuniform SIZE model.
- UpperBoundFalsifier: `N^{\rho+o(1)}+\Gamma_{trans}(\pi)<N^{1+\epsilon-o(1)} \Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Requires that LB_N is a same-model lower-bound assertion for H_N^{SAT} and the parser construction is valid.
- RowExpansionFloor: `X_N(\pi)\ge N^{1+o(1)}\,|K_{idx}(\pi)|`. Valid when: Valid when realizing one influential row requires expanding its SAT value across the N-sized x-domain.
- SupportDensityPressure: `\frac{|K_{idx}(\pi)|}{M_N}\ge N^{\epsilon-q-o(1)}`. Valid when: Applies when a claimed lower-bound proof must avoid the upper-bound falsifier and all non-row-expansion charges are subthreshold.

## Attempted Derivation

- Fix N and a Psys_sym transcript pi proving LB_N(1+epsilon) about H_N^SAT; partition proof lines into base Psys_bEF^- lines and FormulaEval lines.
- Apply the already finalized Gap98-SRhNormalForm to base lines, obtaining Gamma_bEF(pi) with bit fields, parent pointers, and bounded-SR_h occurrence neighborhoods.
- For each FormulaEval line satisfying TransparentRowSupport_N, verify its selector code, enumerate or scan its influential row set, deduplicate against prior rows, and charge the incremental discovery to U_N.
- For every newly charged influential row, insert the same-theory occurrence expansion of SAT(G_N(x,j)) over the N-sized x-domain and charge this to X_N; influence closure ensures the line has no remaining semantic dependency.
- Induct over proof lines: base rules preserve Gamma_bEF, transparent FormulaEval rules add exactly their incremental U and X charges, and references to prior row expansions are free except for charged pointer overhead.
- Compose the parsed transcript with the explicit H_N^SAT generator of size N^{rho+o(1)} to obtain C_SIZE(H_N^SAT) <= N^{rho+o(1)}+Gamma_trans(pi).
- If this upper bound is below N^{1+epsilon-o(1)}, the claimed same-model LB_N(1+epsilon) is falsified; this is a proof-system obstruction, not a proof of P != NP.
- For the negative half, take the first FormulaEval line whose influential row is not visible or charged. In the occurrence-completion or explicit enable-bit model, flip an unread eval-critical bit for that private row while preserving all previously read fields, contradicting deterministic parser soundness.

Blocking gap: The full semantic SAT case is still blocked exactly at RealSATInfluenceRealizer_N: an advice-free witness must show that every real SAT influence is either visible and charged or has an enable-bit/private-row countermodel inside the same formula family.

## Falsifiers

- falsifier: a FormulaEval line has an influential SAT row absent from visible support, and the omitted row has an unread eval-critical occurrence.
- falsifier: the selector is membership-only or semantic AC0 with no output-sensitive enumerator; the valid charge becomes full scan N^{1+q+o(1)} or the parser is invalid.
- falsifier: U_N hides nonuniform advice choosing hard rows or ranking truth-table rows; then the target language lower bound is not uniform or target-preserving.
- falsifier: X_N uses an external SAT oracle rather than same-theory occurrence expansion; the bridge becomes a semantic-oracle model change.
- falsifier: q<epsilon with subthreshold non-row charges, because |K_idx|>=N^{epsilon-o(1)} cannot fit inside M_N=N^{q+o(1)}.
- falsifier: RealSATInfluenceRealizer_N is asserted without witnesses, cutoff, uniform construction, and advice ledger.

## Learning

Cycle 115 upgrades the theorem pair from a slogan to a proof-auditable packet: transparent FormulaEval is charged by an incremental union ledger, while the first uncharged semantic influence is enough for a private-row falsifier. The q-trichotomy is a consequence of X_N>=N^{1+o(1)}|K_idx| and the upper-bound threshold, not a separate hardness-magnification claim. The remaining gap is exactly RealSATInfluenceRealizer_N for real semantic SAT, so the contribution is a scoped parser obstruction rather than progress on the main P != NP conjecture.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the hidden-support half of TransparentRowSupport_N.`
- Rationale: The branch no longer needs another selector example; it needs to test whether uncharged semantic influence is genuinely fatal or can be target-preservingly realized and charged.
- Situation seed: A padded SAT-parity family H_N^SAT(x)=xor_{j<=N^q} SAT(G_N(x,j)) where one FormulaEval rule uses a hidden selector bit Enable(j*) that is not in the enumerated support and can flip SAT(G_N(x,j*)) while all visible occurrence neighborhoods are fixed.
- Varied variable: sigma, the exponent of hidden influential rows, with |K_hidden|=N^{sigma+o(1)} and q,rho,epsilon held fixed.
- Held-fixed controls: Same H_N^SAT generator and same nonuniform SIZE target model., Same Gap98-valid Psys_bEF^- base parser and same Gamma_bEF ledger., Formula lengths remain polylogarithmic and row expansion cost remains N^{1+o(1)} per realized influential row., No advice is allowed to name j* unless its bits are charged in U_N and X_N.
- Expected observation: If sigma>0 and hidden rows are not charged, the first hidden row gives two occurrence completions with identical parser transcript and different FormulaEval value. If they are charged, X_N increases by at least N^{1+sigma-o(1)}, yielding the support-density threshold.
- Transfer certificate needed: A valid RealSATInfluenceRealizer_N certificate must either expose every hidden influential row with advice-free row identifiers and same-theory SAT expansion, or prove the enable-bit/private-row spoof cannot occur for the real formula grammar.

## Next Experiment

Write the paper-ready proof of L115.FirstBadInfluenceCountermodel for an explicit unread-enable-bit SAT gadget, then run the same proof attempt on real FormulaEval-SAT; if the gadget proof works but the real proof blocks, record RealSATInfluenceRealizer_N as the precise open lemma and promote the restricted theorem pair.
