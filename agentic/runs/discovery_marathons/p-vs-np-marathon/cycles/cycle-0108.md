# cycle-0108

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

TransparentRowSupport_N theorem pair, positive direction: for the beta-zero SAT parity carrier H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), every Psys_sym proof pi using bit-explicit bEF, bounded SR_h, and FormulaEval lines satisfying TransparentRowSupport_N has a parsed transcript of cost Gamma_trans(pi)=Gamma_bEF(pi)+U_N(pi)+X_N(pi). Hence any accepted proof of LB_N(1+epsilon) with subthreshold N^{rho+o(1)}+Gamma_trans(pi)+E_N N polylog(N) is falsified by an explicit SIZE circuit for H_N^SAT.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) on N-bit source inputs, with M_N=N^{q+o(1)}, polylogarithmic SAT length ell_N=(log N)^d, generator size N^{rho+o(1)}, and source lower-bound statement LB_N(1+epsilon): C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)}.
- target object: a parser-to-circuit falsifier for short Psys_sym lower-bound proofs, not a proof of P != NP; the target conclusion is that transparent proof mechanisms cannot certify LB_N below the charged Gamma_trans threshold.
- controlled interface: TransparentRowSupport_N consists of visible selector code, advice-free RowSet enumeration or certified full scan, influence closure for all SAT-label rows affecting the FormulaEval line, same-theory occurrence expansion, and no hidden semantic advice.
- target-preserving condition: the parser, generator, FormulaEval expansion, sparse-row correction, and lower-bound claim all live in the same nonuniform SIZE model, with beta=0 target-query length and q,rho,eta,tau tracked before applying the falsifier.
- K_idx(a) is the visible set of row-slot indices whose SAT labels can influence FormulaEval line a after influence closure.
- U_N(pi) is the total advice-free selector/enumerator cost for all transparent FormulaEval lines in pi.
- X_N(pi) is the total row-expansion cost N*|K_idx(a)|*polylog(N), with full-scan fallback |K_idx(a)|=M_N.
- E_N is the number of source rows not handled by the parsed transcript and corrected by equality patches.

## Assumptions

- For all sufficiently large N, epsilon>0 is fixed and q,rho are fixed exponent parameters with q,rho<1+epsilon for the intended magnification window.
- The source and target circuit model is nonuniform Boolean SIZE; no step upgrades to uniform P or to NP not subset P/poly without the separate beta-zero transfer theorem.
- Psys_sym^trans extends the already parsed Psys_bEF^- system; bEF dependency, SATeq links, and bounded SR_h contribute Gamma_bEF(pi) with eta,tau already charged.
- Each FormulaEval line either provides an advice-free RowSet enumerator verified inside the parser or accepts the full-scan charge over all M_N slots.
- Influence closure is semantic over the restricted row-label abstraction: changing SAT labels outside K_idx(a) cannot change the FormulaEval line value or any later parsed use.
- Same-theory expansion means the FormulaEval row witnesses are expanded into occurrence-level objects accepted by the same parser, not by an external semantic oracle.
- The proof may be nonuniform as an object, but the parser extracting Gamma_trans(pi) receives only pi,N and visible selector code, not hidden row advice.

## Equations

- beta_zero_carrier_parameters: `\ell_N=(\log N)^d,\quad M_N=N^{q+o(1)},\quad |G_N|=N^{\rho+o(1)}`. Valid when: Valid when the carrier generator outputs polylogarithmic SAT instances and q,rho are fixed exponent parameters.
- transparent_gamma: `\Gamma_{trans}(\pi)=\Gamma_{bEF}(\pi)+U_N(\pi)+X_N(\pi)`. Valid when: Applies after every FormulaEval line satisfies TransparentRowSupport_N or is charged by full syntactic scanning.
- formulaeval_expansion_charge: `X_N(\pi)=\sum_{a\in FE(\pi)} N\,|K_{idx}(a)|\,\ell_N^{O(1)}\le F_{FE}(\pi)N^{1+q+o(1)}`. Valid when: Valid when K_idx(a) is advice-free enumerable and the fallback scan ranges over all M_N slots.
- parsed_upper_bound: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{trans}(\pi)+E_NN\ell_N^{O(1)}`. Valid when: Requires the same nonuniform SIZE model, a parsed proof transcript, and only E_N unparsed source rows.
- subthreshold_falsifier: `N^{\rho+o(1)}+\Gamma_{trans}(\pi)+E_NN\ell_N^{O(1)}<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Applies when LB_N asserts an N^{1+epsilon-o(1)} lower bound for this exact carrier.
- support_density_corollary: `|K_{idx}^{tot}|\ge N^{\epsilon-o(1)},\quad |K_{idx}^{tot}|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Valid when FormulaEval support is the only unabsorbed term preventing the parser-circuit falsifier inequality.

## Attempted Derivation

- Fixed the beta-zero carrier H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, ell_N=(log N)^d, and generator size N^{rho+o(1)}.
- Defined TransparentRowSupport_N as five clauses: visible selector code, advice-free enumeration or full scan, influence closure, same-theory occurrence expansion, and no hidden support advice.
- Inherited the cycle-102 Psys_bEF^- line induction: EF dependencies, SATeq links, and bounded SR_h contribute Gamma_bEF(pi), including eta,tau and touched occurrence neighborhoods.
- For a transparent FormulaEval line a, enumerate K_idx(a) or scan all M_N slots; expand every selected row into occurrence-level verifier fields; charge U_a plus N|K_idx(a)|ell_N^{O(1)}.
- Summed FormulaEval charges to obtain Gamma_trans(pi)=Gamma_bEF(pi)+U_N(pi)+X_N(pi), with X_N<=F_FE N^{1+q+o(1)} under full scan.
- Extended the line induction: every later proof line depends only on generated formulas, charged row labels, and parsed transcript gates; influence closure forbids uncharged semantic dependence.
- Constructed the falsifying circuit D_pi for H_N^SAT by combining G_N, transcript gates of size Gamma_trans(pi), and equality patches for E_N residual source rows, giving C(H_N)<=N^{rho+o(1)}+Gamma_trans(pi)+E_NN polylog(N).
- Contraposed LB_N(1+epsilon): if the displayed upper bound is below N^{1+epsilon-o(1)}, the purported proof certificate is invalid for the claimed source lower bound.
- Proved the hidden-support no-go at row-label level: if r* affects FormulaEval but is not in K_idx and not influence-forced, two label assignments agree on the whole visible transcript while differing on r*; an unread enable bit can make proof acceptance fixed while carrier parity flips.
- Separated the open semantic escape: real SAT may invalidate arbitrary label flips, so full semantic FormulaEval needs RealSATInfluenceRealizer_N rather than another occurrence-parser assertion.

Blocking gap: The positive theorem is valid for TransparentRowSupport_N and full-scan fallback. The full Psys_sym semantic theorem remains blocked exactly at RealSATInfluenceRealizer_N; AC0PrefixNonemptiness_N is only an optimization gap for output-sensitive enumeration.

## Falsifiers

- Subthreshold Gamma_trans falsifier: N^{rho+o(1)}+Gamma_trans(pi)+E_NN polylog(N)<N^{1+epsilon-o(1)} contradicts LB_N(1+epsilon) for this carrier.
- Support-density falsifier: if total FormulaEval support |K_idx^{tot}|<N^{epsilon-o(1)}, row expansion cannot support a valid LB_N certificate at exponent 1+epsilon.
- q<epsilon falsifier: |K_idx|/M_N>=N^{epsilon-q-o(1)} exceeds density one, so subthreshold transparent FormulaEval certificates cannot exist.
- Hidden-support falsifier: a private row r* or unread enable bit makes two visible transcripts agree while the carrier parity differs.
- Nonuniform leakage falsifier: if row names or selector witnesses are supplied as semantic advice instead of parsed code, TransparentRowSupport_N is violated.
- Positive-beta transfer falsifier remains active for any broadened carrier: q+beta c caps all-exponent transfer unless beta=0 or the use is genuinely nonblackbox.

## Learning

Cycle 108 replaces selector-case accumulation by a single TransparentRowSupport_N theorem pair. Transparent FormulaEval is valid only after U_N+X_N charging or full scan; hidden semantic FormulaEval is refuted by a private-row falsifier unless RealSATInfluenceRealizer_N supplies a nonrelativizing charged-support certificate. This is a paper-level parser/falsifier boundary, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The branch has enough abstract parser structure; the decisive question is whether hidden FormulaEval influence can evade charged row support while preserving the beta-zero carrier target.
- Situation seed: Take H_N^SAT with M_N=N^q slots and add one FormulaEval line whose visible selector is a guarded dDNNF over charged rows K, plus an unread enable bit e* that selects a private slot r* when e*=1. The proof syntax never prints r*.
- Varied variable: hidden_influence_count h, the number of semantically influential rows not included in K_idx, with h=0 for transparent support and h=1 for the smallest countermodel.
- Held-fixed controls: M_N=N^{q+o(1)}, ell_N=(log N)^d, generator size N^{rho+o(1)}, and beta=0 target-query regime., The same Psys_bEF^- plus bounded SR_h transcript and the same nonuniform SIZE lower-bound statement LB_N(1+epsilon)., Parser input restricted to pi,N, visible selector code, charged rows, and no hidden advice., Sparse-row correction still costs E_NN polylog(N), so patching thresholds are unchanged.
- Expected observation: At h=0 the line induction and Gamma_trans charge are valid; at h=1 two label structures agree on all visible support but differ at r*, so the occurrence parser cannot soundly surface FormulaEval completion. Full scan restores validity at cost N^{1+q+o(1)}.
- Transfer certificate needed: A formal RealSATInfluenceRealizer_N or TransparentRowSupport_N verification proving that every semantically influential SAT row is visible, influence-closed, same-theory expandable, and charged before the parser-to-circuit falsifier is invoked.

## Next Experiment

Write the referee-style TransparentRowSupport_N definition and audit six examples as corollaries: interval-union, full scan, ROBDD, guarded-dDNNF, projected-dDNNF, and influence-complete extension rules. Do not add new selector families unless they prove a clause, refute a clause, or improve AC0PrefixNonemptiness_N.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

TransparentRowSupport_N theorem pair, positive half: for a bit-explicit Psys_sym^TRS proof pi of LB_N(1+epsilon) for the beta-zero SAT-parity carrier, every FormulaEval mechanism with visible selector code, advice-free row enumeration or full-scan charge, selector extensionality, influence closure, same-theory occurrence expansion, and no hidden row advice is parsed into a charged transcript Gamma_trans. If the resulting transcript plus generator circuit is below N^{1+epsilon-o(1)}, the accepted lower-bound proof is falsified in the same nonuniform SIZE model.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), M_N=N^{q+o(1)}, with generator circuit size N^{rho+o(1)} and a Psys_sym^TRS proof pi of LB_N(1+epsilon).
- target object: the claimed nonuniform Boolean lower bound C(H_N^SAT)>N^{1+epsilon-o(1)} against SIZE circuits on the same N-scale truth-table carrier.
- controlled interface: TransparentRowSupport_N consists of visible selector code, proof-visible extensionality for RowSet(a), influence closure for FormulaEval-SAT rows, advice-free enumeration or full scan, same-theory occurrence expansion, and no semantic hidden support.
- target-preserving condition: the parser, enumerator, and expansion circuit are deterministic and advice-free, preserve the N,M_N,q,rho,epsilon length regime, and build an upper-bound circuit for the same H_N^SAT rather than for an auxiliary promise object.
- K_idx(pi) is the bEF-visible row support; E_N^*(pi) is the number of additional FormulaEval-influential rows forced by influence closure; K_idx^+(pi)=K_idx(pi) union FE-influential rows.
- U_N(pi) is the proof-visible enumeration or full-scan charge for all FormulaEval selectors; X_N(pi)=N E_N^*(pi) is the same-theory row-expansion charge.

## Assumptions

- Model: nonuniform Boolean circuits, beta-zero SAT-parity carrier, and a bit-explicit EF+SATeq+bounded-SR_h base parser extended only by TransparentRowSupport_N FormulaEval lines.
- Regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, selector code size at most N^{sigma+o(1)}, generator size N^{rho+o(1)}, and fixed epsilon>0.
- Uniformity/advice: the parser, RowSet enumerators, selector extensionality checks, and occurrence expansions use no private advice depending on the SAT truth table.
- Same-theory condition: every row inserted into the transcript is justified inside the same formal proof language, not by an external real-SAT oracle.
- Barrier condition: if Gamma_trans induces a dense efficiently recognizable property useful against SIZE, the natural-proofs audit is triggered; the theorem itself is a parser-to-upper-bound falsifier, not a P != NP proof.

## Equations

- Gamma_trans_decomposition: `\Gamma_{\mathrm{trans}}(\pi)=\Gamma_{\mathrm{bEF}}(\pi)+U_N(\pi)+X_N(\pi)`. Valid when: Valid when every FormulaEval line satisfies TransparentRowSupport_N and the base bEF parser already supplies Gamma_bEF for non-FormulaEval lines.
- full_scan_or_visible_enum_charge: `U_N(\pi)\le \sum_{a\in FE(\pi)} \mathrm{EnumCost}(a) \le N^{q+\tau+\sigma+o(1)}`. Valid when: Valid when selector code is proof-visible, extensionality is checkable, and the parser may either enumerate RowSet(a) or scan all M_N rows per FormulaEval line.
- row_expansion_charge: `X_N(\pi)=N\,E_N^*(\pi)`. Valid when: Valid when each FormulaEval-influential row is expanded into an N-scale occurrence transcript in the same proof theory without semantic shortcuts.
- upper_bound_falsifier: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{\mathrm{trans}}(\pi)`. Valid when: Applies after the parser output and generator circuit compose into a nonuniform circuit for the identical H_N^SAT carrier.
- subthreshold_invalidity: `N^{\rho+o(1)}+\Gamma_{\mathrm{trans}}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow \pi\text{ is not a valid proof of }LB_N(1+\epsilon)`. Valid when: Valid when LB_N(1+epsilon) asserts a lower bound against the same nonuniform SIZE model used by the constructed upper-bound circuit.
- support_density_pressure: `|K_{idx}^+(\pi)|\ge N^{\epsilon-o(1)},\qquad |K_{idx}^+(\pi)|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Requires rho<1+epsilon and all non-row overheads in Gamma_trans to be below the claimed lower-bound threshold.

## Attempted Derivation

- Define TransparentRowSupport_N linewise: visible selector code, advice-free RowSet enumerator or full scan, proof-visible extensionality, influence closure, same-theory occurrence expansion, and no hidden row advice.
- Run the existing bEF line induction on all non-FormulaEval lines, preserving Gamma_bEF(pi) and the prior eta/tau overhead accounting.
- For each transparent FormulaEval line a, enumerate RowSet(a) or scan all M_N rows, charge EnumCost(a), and verify inside the proof theory that RowSet(a) contains every row whose SAT value can affect the line.
- For every newly forced FE-influential row, insert the same-theory occurrence expansion; this contributes X_N=N E_N^*.
- Concatenate these local charges over at most N^{tau+o(1)} proof lines to obtain Gamma_trans=Gamma_bEF+U_N+X_N.
- Compose the generator circuit of size N^{rho+o(1)} with the transcript circuit produced by the parser; this yields C(H_N^SAT)<=N^{rho+o(1)}+Gamma_trans in the same nonuniform SIZE model.
- Conclude the subthreshold falsifier: an accepted proof of LB_N(1+epsilon) cannot have N^{rho+o(1)}+Gamma_trans<N^{1+epsilon-o(1)}.
- Derive the support-density corollary by isolating the row-count part of Gamma_trans: unless |K_idx^+|>=N^{epsilon-o(1)}, the transcript gives the forbidden upper bound.
- For failure of any TransparentRowSupport_N clause, instantiate the unread-enable-bit/private-row semantic FormulaEval line; two row assignments agree on all visible transcript data but disagree on the hidden FormulaEval influence, refuting surface occurrence parsing.

Blocking gap: RealSATInfluenceRealizer_N remains open for unrestricted Psys_sym with real FormulaEval-SAT semantics: one must prove that actual SAT-semantic influences are always representable by visible, extensional, chargeable row support or else accept the semantic-oracle quarantine.

## Falsifiers

- q<epsilon with subthreshold Gamma_trans gives the explicit upper-bound falsifier C(H_N^SAT)<N^{1+epsilon-o(1)} for the claimed LB_N(1+epsilon).
- A hidden selector bit choosing row r* outside visible RowSet(a) is a finite falsifier to surface occurrence completion.
- Projected dDNNF with hidden witnesses falsifies output-sensitive enumeration unless projection extensionality is proof-visible.
- Semantic FormulaEval-SAT used as an oracle is outside the valid parser theorem and is quarantined unless RealSATInfluenceRealizer_N is proved.
- A nonuniform advice string encoding RowSet(a) falsifies target preservation because it leaks support without being charged in Gamma_trans.
- If Gamma_trans induces a polynomial-density constructive property useful against SIZE, the natural-proofs falsifier search must audit PRF tension before any route promotion.

## Learning

Cycle 108 consolidates the FormulaEval selector zoo into a theorem/countermodel pair. Transparent row support is a valid target-preserving interface and yields Gamma_trans=Gamma_bEF+U_N+X_N plus the subthreshold upper-bound falsifier. Hidden semantic support is refuted by the private-row/unread-enable-bit countermodel. The remaining full-system gap is precisely RealSATInfluenceRealizer_N, not generic barrier folklore and not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The branch needs a concrete semantic-support test because the remaining gap is not another selector family but whether hidden FormulaEval influence can evade charged row support while preserving the same H_N^SAT lower-bound target.
- Situation seed: Consider Psys_sym with one FormulaEval line L_v over H_N^SAT: for visible flag v=1 it enumerates an interval-union RowSet; for v=0 an unread enable bit redirects the line to a private row r* while the displayed selector remains empty.
- Varied variable: the visibility flag v controlling whether the influential row r* is included in the proof-visible RowSet or hidden behind semantic FormulaEval.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, fixed q,rho,epsilon and the same generator G_N, the target lower-bound statement LB_N(1+epsilon) against nonuniform SIZE, the bEF base parser, proof length exponent tau, selector-size exponent sigma, and no-advice parser requirement, the carrier H_N^SAT and the same-theory occurrence-expansion cost N per charged row
- Expected observation: When v=1 the theorem charges either the enumerator or full scan and preserves Gamma_trans; when v=0 two assignments agree on visible transcript data but differ on L_v through r*, so the parser misses a necessary row and the hidden-support countermodel fires.
- Transfer certificate needed: A RealSATInfluenceRealizer_N certificate proving that actual real-SAT FormulaEval cannot implement the v=0 hidden influence without exposing a chargeable row, or a formal quarantine that semantic FormulaEval is outside the target-preserving parser theorem.

## Next Experiment

Attempt RealSATInfluenceRealizer_N for one concrete real-SAT axiom schema: specify the formula fields, prove every satisfying-assignment influence induces a proof-visible RowSet entry, or instantiate the unread-enable-bit countermodel inside that schema.

# MCSP / Meta-Complexity Carrier Transfer supporting TransparentRowSupport_N proof packet

## Candidate Lemma

TransparentRowSupport_N Gamma-extension theorem. For H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), M_N=N^{q+o(1)}, if every Psys_sym FormulaEval line in a proof pi has visible advice-free row support, certified enumeration or full-scan charge, influence closure, same-theory occurrence expansion, and no hidden semantic support, then the existing Psys_bEF^- parser induction extends to a transcript Q_pi with Gamma_trans(pi)=N^{tau+o(1)}(Gamma_bEF(pi)+U_N+E_N|K_idx(pi)|). Hence a claimed LB_N(1+epsilon) proof with max{rho,gamma_trans}<1+epsilon is invalid in the same nonuniform SIZE model; the parsed transcript gives a circuit upper-bound falsifier, not a P != NP proof.

## Definitions

- source object: a bit-explicit Psys_sym proof transcript pi of a lower-bound assertion LB_N(1+epsilon) about H_N^SAT, including FormulaEval lines whose selected SAT rows are meant to justify parity or row-forcing facts.
- target object: a same-language nonuniform SIZE upper bound for H_N^SAT at length N, used only to refute the particular low-cost proof transcript if its exponent is below 1+epsilon.
- controlled interface: TransparentRowSupport_N consists of visible selector code, an advice-free RowSetEnumerator_N or declared full scan, influence closure Inf_e subset K_e, same-theory occurrence expansion for each row, and no hidden support advice.
- target-preserving condition: the parser, expansion, and circuit simulation keep the carrier H_N^SAT, the length parameter N, the generator G_N, and the nonuniform circuit model fixed; semantic FormulaEval is not imported as an oracle.
- source statement: every FormulaEval semantic dependency in pi is exposed by charged row indices K_idx(pi) and expandable to occurrence-level SAT data within Psys_sym.
- target statement: if the total charged transcript exponent gamma_trans plus generator exponent rho is subthreshold, then pi cannot validly certify C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)}.
- observable: Gamma_trans(pi) is the cost ledger joining the old Gamma_bEF parser charge, row discovery U_N, row expansion E_N|K_idx|, and parser compilation overhead tau.

## Assumptions

- Circuit/proof model: target lower bound is against unrestricted nonuniform Boolean circuits of size N^{1+epsilon-o(1)}, and proofs are Cook-Reckhow bit strings whose accepted lines can be parsed syntactically.
- Length regime: N tends to infinity, M_N=N^{q+o(1)}, generator size or uniform circuit for G_N is N^{rho+o(1)}, and individual SAT instances have polylogarithmic description length compatible with occurrence expansion E_N=N^{eta+o(1)} or declared E_N=N^{1+eta+o(1)} after row-block normalization.
- Uniformity and advice: selectors, enumerators, quotient witnesses, and expansion routines are advice-free and computable inside the intended proof-parser model; nonuniform hard-row selection is forbidden.
- Transparency: for each FormulaEval line e, the charged set K_e contains every SAT row whose value can change the truth of that line under completions consistent with previously parsed data.
- Same-theory condition: FormulaEval expansion produces explicit occurrence transcripts usable by the same Psys_sym parser; it does not appeal to external SAT semantics unless RealSATInfluenceRealizer_N is separately proved.
- Base dependency: the restricted Gap98-SRhNormalForm and Gamma_bEF line induction for Psys_bEF^- are available as the non-FormulaEval part of the parser.
- Naturalness status: the theorem is a sparse transcript falsifier, not a large constructive property over many truth tables, so it is outside the immediate natural-proofs trigger but still subject to advice leakage checks.

## Equations

- carrier: `H_N^{SAT}(x)=xor_{1<=j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}`. Valid when: Valid when the source carrier is the beta-zero SAT-parity family and the generator length and row indexing conventions are fixed.
- transparent-gamma-ledger: `Gamma_trans(pi)=N^{tau+o(1)}(Gamma_bEF(pi)+U_N+E_N |K_idx(pi)|)`. Valid when: Valid when every FormulaEval line satisfies TransparentRowSupport_N and occurrence expansion remains inside the same proof theory.
- exponent-ledger: `gamma_trans=tau+max{g,u,k+eta}, where Gamma_bEF=N^{g+o(1)}, U_N=N^{u+o(1)}, |K_idx|=N^{k+o(1)}, E_N=N^{eta+o(1)}`. Valid when: Applies after all transcript, enumeration, support, expansion, and parser-overhead costs have polynomial exponent forms.
- upper-bound-transfer: `C_SIZE(H_N^{SAT}) <= N^{max{rho,gamma_trans}+o(1)}`. Valid when: Requires the target-preserving parser-to-circuit simulation, the same nonuniform SIZE model, and no hidden semantic FormulaEval advice.
- low-cost-falsifier: `max{rho,gamma_trans}<1+epsilon => pi is a falsifier-invalid proof of LB_N(1+epsilon)`. Valid when: Valid when LB_N(1+epsilon) asserts a same-length unrestricted circuit lower bound for H_N^{SAT} above N^{1+epsilon-o(1)}.

## Attempted Derivation

- Define the row universe R_N for H_N^SAT and attach to every FormulaEval line e a visible selector code Sel_e, an influence set Inf_e, a charged support K_e, an enumerator cost U_e, and a row-expansion cost E_N.
- Impose TransparentRowSupport_N: Sel_e is syntactically present, RowSetEnumerator_N outputs K_e or a full scan is charged, Inf_e subset K_e is certified, each row in K_e expands to occurrence-level SAT data in Psys_sym, and no advice string chooses hidden rows.
- Run the existing Gap98/Psys_bEF^- line induction on non-FormulaEval lines; for a FormulaEval line, first enumerate K_e, then attach same-theory occurrence transcripts for all rows in K_e, then record parent pointers so later lines depend only on charged data.
- Sum line costs. The non-FormulaEval part contributes Gamma_bEF(pi), row discovery contributes U_N=sum_e U_e or full-scan charges, and occurrence materialization contributes E_N|K_idx(pi)|, all multiplied by the parser compile overhead N^{tau+o(1)}.
- Apply the parser-to-circuit patch lemma in the same nonuniform SIZE model: hardwire the charged transcript and combine it with the generator G_N of size N^{rho+o(1)} to compute the challenged H_N^SAT behavior, giving C_SIZE(H_N^SAT)<=N^{max{rho,gamma_trans}+o(1)}.
- Conclude that a proof pi with max{rho,gamma_trans}<1+epsilon cannot be a valid proof of LB_N(1+epsilon); this is a local falsifier for the proof transcript.
- For the negative half, suppose r in Inf_e is not visible or charged. Use a private row or unread enable bit to build two completions agreeing on all parsed fields but flipping SAT(F_r), so the same surface transcript has different FormulaEval truth.
- Classify the only escape: prove RealSATInfluenceRealizer_N or a charged quotient witness for r; otherwise the rule is a semantic-oracle mechanism outside TransparentRowSupport_N.

Blocking gap: The transparent theorem is proof-shaped modulo the already archived Gap98 base parser, but arbitrary semantic FormulaEval and arbitrary AC0 membership-only selectors remain blocked at RealSATInfluenceRealizer_N or output-sensitive RowSetEnumerator_N.

## Falsifiers

- falsifier: a FormulaEval line has an unread enable bit whose setting changes satisfiability while the parser-visible occurrence neighborhood is unchanged.
- falsifier: RowSetEnumerator_N is only a membership oracle or AC0 predicate with no output-sensitive enumeration certificate, forcing scan charge or semantic-oracle classification.
- falsifier: selector projection hides high witness-fiber entropy and pays neither U_N nor W_N, so projected support is not valid at T_N cost.
- falsifier: a quotient or extensionality witness is chosen by nonuniform advice rather than produced in the proof transcript.
- falsifier: Gamma_trans is computed in a stronger semantic model than the target lower-bound proof system, breaking same-theory validity.
- falsifier: rho or gamma_trans already exceeds 1+epsilon, so the route gives no low-cost contradiction and must be recorded as high-cost rather than promoted.

## Learning

Cycle 108 stops selector accumulation by replacing the selector zoo with a single TransparentRowSupport_N theorem pair. The positive side gives a valid Gamma_trans ledger and low-cost transcript falsifier; the negative side gives a private-row/unread-enable-bit countermodel. The remaining escape is exactly RealSATInfluenceRealizer_N, not generic proof-system strength or a new MCSP carrier.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for hidden FormulaEval support.`
- Rationale: The top queue requires a concrete theorem/countermodel pair, and the remaining ambiguity is whether semantic FormulaEval influences can be made visible without paying expansion. A private-row experiment directly tests the target-preserving parser condition.
- Situation seed: Take H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) and a Psys_sym FormulaEval rule whose selector visibly lists K_e but whose semantic value also depends on one unlisted row r controlled by an unread enable bit in G_N(x,r).
- Varied variable: visibility gap v, the number or exponent of influential SAT rows not included in the charged support K_e; start with v=1 private row and then scale to v=N^{beta}.
- Held-fixed controls: Keep M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)}, and the claimed target LB_N(1+epsilon) fixed., Keep the target circuit model unrestricted nonuniform SIZE at the same length N., Keep the parser restricted to same-theory occurrence expansion with no semantic oracle and no advice-selected row., Keep the visible transcript, selector code, and all charged rows identical in the two completions.
- Expected observation: For v>=1, two completions can agree on all charged data but disagree on the FormulaEval truth, so transparency fails. If a realizer charges all v rows, Gamma_trans increases by at least v E_N N^{tau-o(1)}, yielding the density threshold rather than a free semantic shortcut.
- Transfer certificate needed: A valid RealSATInfluenceRealizer_N must output, inside Psys_sym and without advice, an influence-closed support K_e plus occurrence expansions proving every semantic FormulaEval dependency is charged; otherwise the thought experiment remains a countermodel, not proof evidence.

## Next Experiment

Write the paper-ready proof of TransparentRowSupport_N: formal clauses, line-induction invariant, Gamma_trans summation, private-row countermodel, corollary table for prior selector classes, and a named open problem RealSATInfluenceRealizer_N for semantic FormulaEval.
