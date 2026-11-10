# cycle-0106

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Restricted parser/falsifier theorem: for beta-zero H_N^SAT and Psys_bEF^- with bit-explicit EF, SATeq links, bounded-SR_h, and transparent interval-union FormulaEval, any accepted transcript whose charged parser cost is subthreshold yields a nonuniform circuit upper bound for H_N^SAT and therefore falsifies LB_N(1+epsilon). Sound proofs in this restricted system must pay the Gamma_bEF^IU threshold; this is not a proof of P != NP.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) together with a Psys_bEF^- proof pi of LB_N(1+epsilon), where M_N=N^{q+o(1)}, G_N has size N^{rho+o(1)}, and generated formulas have length L_N=(log N)^d.
- target object: the nonuniform circuit upper bound C(H_N^SAT)<=N^{rho+o(1)}+O(Gamma_bEF^IU(pi)) that acts as a falsifier for the claimed source lower bound C(H_N^SAT)>N^{1+epsilon-o(1)}.
- controlled interface: a deterministic bit parser maps every proof line to row indices, occurrence neighborhoods, SATeq link classes, bounded-SR_h leaves, interval-union RowSet lists, and residual row patches, with no semantic row advice.
- target-preserving condition: beta=0 is preserved because all target SAT formulas have polylogarithmic length and the SAT-circuit substitution term is N^{o(1)} for every fixed target exponent c; the theorem only certifies a source-lower-bound obstruction, not NP not subset P/poly.
- source_statement: LB_N(1+epsilon) abbreviates C_{SIZE}(H_N^SAT)>N^{1+epsilon-o(1)} on the valid length set, with nonuniform target circuits allowed and the proof system syntactically fixed.
- target_statement: if N^{rho+o(1)}+Gamma_bEF^IU(pi)<N^{1+epsilon-o(1)}, then the lower-bound sentence for this carrier is false in the stated nonuniform circuit model.
- model_context: source carrier is the beta-zero parity SAT batch; proof model is Psys_bEF^-; target class is nonuniform SIZE; reduction type is parser-to-circuit simulation plus equality patching.
- quantifier_context: epsilon,q,rho,eta,tau are fixed constants, N ranges over valid lengths, h is bounded, d>1 is fixed, and all o(1) losses are uniform over the proof family.
- barrier_status: the restricted parser theorem is a syntactic proof-complexity transfer and does not assert a large constructive natural property; full semantic FormulaEval remains nonrelativizing and outside the proved parser scope.

## Assumptions

- Psys_bEF^- lines are encoded with opcodes, parent pointers, bit-addressed EF extension definitions, explicit occurrence addresses, SATeq link identifiers, bounded-SR_h rule fields, and interval-union selector fields.
- The bounded-SR_h rule has at most N^{eta+o(1)} local leaves per touched slot and verifier overhead N^{tau+o(1)} per leaf family after sharing row and slot indices.
- Interval-union FormulaEval selectors expose endpoints in the proof line, and RowSetEnumerator_N outputs the selected row list uniformly with no hidden advice.
- Residual disagreement on E_N source rows is patchable by equality tests at cost O(E_N N), so the lemma is valid only when E_N is an explicit parser output or a proved residual bound.
- The parser is uniform and advice-free relative to pi,N; nonuniformity is allowed only in the final target circuit and in hardwired parsed constants whose bit length is charged in Gamma_bEF^IU.
- Reviewer packet status: reduction consistency passes for the restricted rules, quantifier-uniformity passes for fixed exponents, barrier specificity passes because the semantic FormulaEval escape is quarantined, and derivation status is proved modulo routine encoding constants.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j=1}^{M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad |G_N|=N^{\rho+o(1)},\quad L_N=(\log N)^d`. Valid when: Valid when the beta-zero carrier generator and all valid lengths are fixed before the proof family is parsed.
- bounded_SR_charge: `B_{SR_h}(\pi)\le N^{q+\eta+\tau+o(1)}`. Valid when: Applies when bounded-SR_h touches M_N slots, has leaf exponent eta, and uses verifier overhead exponent tau.
- charged_transcript: `\Gamma_{bEF}^{IU}(\pi)=S_{dep}(\pi)+S_{link}(\pi)+B_{SR_h}(\pi)+N\cdot |RowSet_{IU}(\pi)|+E_NN`. Valid when: Valid when EF dependencies, SATeq links, SR leaves, interval-union rows, and residual patches are separately enumerated and charged.
- parser_to_circuit: `C(H_N^{SAT})\le N^{\rho+o(1)}+O(\Gamma_{bEF}^{IU}(\pi))`. Valid when: Requires the parsed transcript to determine every generated parity row except the explicitly patched E_N residual rows.
- LB_falsifier: `N^{\rho+o(1)}+\Gamma_{bEF}^{IU}(\pi)<N^{1+\epsilon-o(1)}\;\Longrightarrow\; \neg LB_N(1+\epsilon)`. Valid when: Valid when LB_N means a nonuniform SIZE lower bound for exactly the same carrier H_N^{SAT}.
- support_density: `|K_{idx}(\pi)|\ge N^{\epsilon-o(1)},\quad |K_{idx}(\pi)|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Applies to sound restricted certificates after the parser-to-circuit bound is contraposed below the lower-bound threshold.

## Attempted Derivation

- Define proof-line fields: opcode; line number; parent pointers; EF extension gate id; dependency bit interval; SATeq link id; SR_h leaf tuple (slot j, row r, variable block b, branch word z, occurrence offset u); FormulaEval selector id with interval-union endpoints; residual patch list.
- Run transitive EF-DAG traversal: for every extension variable v, accumulate the union of source row and occurrence dependencies of its defining subformula; charge each newly exposed bit interval to S_dep(pi) once by topological order.
- Process SATeq lines by quotienting explicitly named formula encodings; charge every equality link and copied occurrence neighborhood to S_link(pi); do not infer unlisted rows from semantic equality.
- Process bounded-SR_h lines locally: each touched slot contributes at most N^{eta+tau+o(1)} verifier leaves after shared generator decoding, so the total SR charge over M_N slots is B_SR_h(pi)<=N^{q+eta+tau+o(1)}.
- Process interval-union FormulaEval by expanding each declared interval endpoint list into RowSet_IU(pi); each selected row costs N for equality-test patching or row circuit hardwiring, giving the N|RowSet_IU(pi)| term.
- Induct on proof lines that the semantic value used by each accepted restricted rule is determined by the accumulated charged transcript plus at most E_N residual rows; the induction fails deliberately for unexpanded semantic FormulaEval.
- Compose the generator circuit of size N^{rho+o(1)} with the charged transcript circuit and equality patches to obtain C(H_N^SAT)<=N^{rho+o(1)}+O(Gamma_bEF^IU(pi)).
- Contrapose against LB_N(1+epsilon): any accepted restricted certificate of that lower bound must have N^{rho+o(1)}+Gamma_bEF^IU(pi)>=N^{1+epsilon-o(1)}; otherwise the certificate is invalid because the constructed circuit is a falsifier.
- Run inference-quality checks: source and target statements are identical carrier/model statements; quantifiers are fixed-exponent and valid-length; advice is charged or confined to final nonuniform circuits; full semantic FormulaEval is blocked at FE_Extract_N^sem.

Blocking gap: No blocking gap remains for Psys_bEF^- plus transparent interval-union FormulaEval. The named unresolved gap is FE_Extract_N^sem: extracting complete row supports from unexpanded semantic FormulaEval-SAT without advice or nonrelativizing SAT-specific reasoning.

## Falsifiers

- Subthreshold Gamma_bEF^IU(pi) gives an explicit circuit upper-bound falsifier for LB_N(1+epsilon).
- A hidden semantic FormulaEval row supplies the private-row falsifier to surface occurrence completion.
- q<epsilon with fewer than N^{epsilon-o(1)} complete rows falsifies any claimed restricted source certificate by row enumeration and equality patching.
- Nonuniform leakage through uncharged EF extension variables falsifies the parser unless the transitive dependency DAG is bit-explicit.
- Positive beta in any black-box target-circuit substitution revives the transfer cap q+beta c+o(1), so all-exponent NP/Ppoly claims are invalid outside the beta-zero window.
- Treating EqSAT or SR_h as free semantic power is invalid unless the quotient links or SR leaves are charged in Gamma_bEF^IU.

## Learning

Cycle 106 upgrades the promoted restricted result into a live inference-quality theorem packet: Gamma_bEF^IU is derived by line induction with explicit SR_h and interval-union FormulaEval charges, the q/epsilon support trichotomy is a contraposed corollary, and full semantic FormulaEval remains quarantined by the private-row falsifier rather than by generic barrier folklore.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The restricted theorem is valid only if FormulaEval exposes row support. A concrete private-row experiment tests whether a proposed symbolic FormulaEval rule is an expanded parser rule or a semantic escape.
- Situation seed: Take H_N^SAT with M_N=N^{q+o(1)} polylog formulas and a Psys_sym line FormulaEvalSAT(S) whose selector S is either an interval-union endpoint list or an opaque semantic predicate. Plant one unread enable bit e_{r*} controlling the contribution of row r* to the parity carrier while keeping all queried occurrence neighborhoods unchanged.
- Varied variable: RowSet enumeration overhead exponent alpha, where alpha=q for full transparent expansion, alpha<q for compressed selectors, and alpha=infty for an opaque semantic oracle with no uniform enumerator.
- Held-fixed controls: The carrier H_N^SAT, beta=0 polylog formula length, generator size N^{rho+o(1)}, and target nonuniform SIZE model are fixed., The proof verifier, LB_N(1+epsilon) sentence, residual patch cost E_NN, and absence of parser advice naming r* are fixed., The comparison threshold N^{1+epsilon-o(1)} and the requirement that row support be complete parity-row support are fixed.
- Expected observation: For finite alpha with a uniform enumerator, the parser pays N^{1+alpha+o(1)} expansion and the theorem remains valid. For opaque semantic FormulaEval, the private row remains invisible and two label worlds agree on the transcript while disagreeing on H_N, refuting surface occurrence completion.
- Transfer certificate needed: A valid FE_Extract_N^alpha certificate must output RowSet(S) uniformly from the proof line, list occurrence neighborhoods for every selected row, bound N|RowSet(S)|=N^{1+alpha+o(1)}, and prove that no semantic advice or unread enable bit influences H_N outside the charged rows.

## Next Experiment

Run the finite validation audit on one concrete Psys_sym rule: encode FormulaEval as (a) interval-union axiom schema, (b) AC0 selector with enumerator, and (c) opaque semantic oracle; compute alpha and either attach N^{1+alpha+o(1)} charge or exhibit the private-row countermodel.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Restricted FormulaEval classification theorem: for Psys_sym^cls, every FormulaEval-SAT occurrence is mode-tagged as row-instantiated axiom, enumerated proof line, extension rule, or semantic oracle. In the first three transparent modes, FE_Extract_N outputs an influence-closed row set K_idx^cls(pi) and a Gamma_cls transcript. The transcript gives the same target lower-bound falsifier as the bEF parser. In semantic-oracle mode, occurrence completion is invalid unless the oracle pays the row-expansion charge or supplies RealSATInfluenceRealizer_N.

## Definitions

- source object: an accepted Psys_sym^cls proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), with N=2^n, M_N=N^{q+o(1)}, formula length h=N^{eta+o(1)}, proof length |pi|=N^{tau+o(1)}, and generator size N^{rho+o(1)}.
- target object: a parsed nonuniform circuit upper bound for H_N^SAT of size N^{rho+o(1)}+Gamma_cls(pi), plus support pressure |K_idx^cls(pi)|+E_N^cls(pi)>=N^{epsilon-o(1)} when the claimed lower bound is sound.
- controlled interface: FE_Extract_N reads proof-visible FormulaEval mode tags, selector code, extension-DAG dependencies, and influence certificates; it maps transparent FormulaEval mechanisms to row charges and maps semantic-oracle mechanisms to a quarantine flag.
- target-preserving condition: the extraction is valid only when selector extensionality, influence closure, bounded-SR_h locality, and no-advice uniform parsing hold in the same proof model used to assert LB_N(1+epsilon).
- K_idx^cls(pi) is the union of bEF occurrence rows and all rows whose SAT value can change any transparent FormulaEval truth value under fixed displayed proof bits.
- E_N^cls(pi) counts distinct FormulaEval-influential rows whose SAT truth table over all x must be row-expanded rather than inherited from ordinary bEF occurrences.

## Assumptions

- Model: nonuniform Boolean SIZE lower bounds for the beta-zero SAT-parity carrier; the proof system is EF+SATeq+bounded-SR_h plus mode-tagged FormulaEval.
- Regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, h=N^{eta+o(1)}, selector-code size N^{sigma+o(1)}, selector-extensionality overhead N^{chi+o(1)}, and rho<1+epsilon.
- Uniformity/advice: FE_Extract_N is deterministic, no-advice, and runs from the displayed proof string plus the fixed verifier description; hidden selector tables are not allowed in transparent modes.
- Same-theory condition: FormulaEval soundness, selector extensionality, and extension-DAG dependencies must be facts available in the proof formalism being parsed, not external semantic promises.
- Naturalness boundary: the lemma is proof-system-specific; it yields natural-proof pressure only if the extracted transcript is converted into a large poly(N)-constructive property useful against a named circuit class.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j<M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)}`. Valid when: Valid when the source carrier is the beta-zero SAT-parity family with proof-visible generator G_N and the row parameter j ranges over the displayed M_N rows.
- classification: `FE=FE_{inst}\sqcup FE_{enum}\sqcup FE_{ext}\sqcup FE_{oracle}`. Valid when: Valid when every FormulaEval-SAT occurrence carries a verifier-readable mode tag and the verifier rejects ambiguous or untyped FormulaEval uses.
- gamma-cls: `\Gamma_{cls}(\pi)\le S_{dep}+S_{link}+N^{q+\eta+\tau+o(1)}+N\,E_N^{cls}(\pi)+N^{q+\tau+\sigma+\chi+o(1)}`. Valid when: Applies after extension dependencies are traversed, bounded-SR_h row neighborhoods are charged, and transparent selector enumeration plus extensionality checking have the stated size exponents.
- upper-bound-falsifier: `N^{\rho+o(1)}+\Gamma_{cls}(\pi)<N^{1+\epsilon-o(1)}\;\Rightarrow\; LB_N(1+\epsilon)\text{ is refuted for this source object}`. Valid when: Requires the parsed transcript to compute H_N^{SAT} on the same length N and the lower-bound sentence to claim exclusion of all circuits below N^{1+epsilon-o(1)}.
- support-pressure: `|K_{idx}^{cls}(\pi)|+E_N^{cls}(\pi)\ge N^{\epsilon-o(1)},\quad (|K|+E)/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Holds when the lower-bound proof is sound, rho<1+epsilon, and no smaller transcript upper bound is allowed by the claimed LB_N threshold.

## Attempted Derivation

- Define Psys_sym^cls by adding to Psys_bEF a FormulaEval syntax FE(a,u,b,m) with mode m in {inst, enum, ext, oracle}. The verifier rejects untagged FE occurrences.
- For inst mode, the proof line displays row r and formula bits for G_N(x,r); FE_Extract_N adds r to K_idx^cls and charges the ordinary SATeq/bounded-SR_h neighborhood.
- For enum mode, the proof displays selector code a and an extensionality certificate. A deterministic Enumerator_N(a) lists RowSet(a) in time N^{q+sigma+chi+o(1)} per proof slice; all listed influential rows enter K_idx^cls or E_N^cls.
- For ext mode, extension variables depending on FE are followed through the transitive extension DAG. The dependency charge S_dep+S_link accounts for copied formula bits and parent pointers; no semantic SAT row is created by extension without an originating FE row charge.
- For bounded-SR_h rules, use the already scoped normal-form invariant: each rule touches only h=N^{eta+o(1)} occurrence neighborhoods across |pi|=N^{tau+o(1)} lines and M_N=N^{q+o(1)} row indices, contributing N^{q+eta+tau+o(1)} to Gamma_cls.
- Construct the transcript from the generator circuit of size N^{rho+o(1)}, the parsed dependencies, all charged row truth tables, and selector enumeration witnesses. This yields a circuit for H_N^SAT of size at most N^{rho+o(1)}+Gamma_cls(pi).
- If that size is below N^{1+epsilon-o(1)}, the alleged LB_N(1+epsilon) proof has produced a falsifier to its own source statement. Therefore any sound accepted proof must pay |K_idx^cls|+E_N^cls>=N^{epsilon-o(1)} after lower-order parser costs are subtracted.
- For oracle mode, the proof line is not parsed. The unread-enable-bit construction gives two semantic FE interpretations with identical displayed proof bits but different influential rows, so no valid occurrence parser exists without RealSATInfluenceRealizer_N.

Blocking gap: Full Psys_sym without mandatory FE mode tags, selector extensionality, and influence certificates remains blocked at RealSATInfluenceRealizer_N and SelectorExtensionality_N.

## Falsifiers

- Unread-enable-bit semantic FormulaEval is a finite falsifier to surface occurrence completion: one hidden enabled row r* changes FE influence while all displayed proof bits remain fixed.
- If q<epsilon and rho plus parser overhead stay below 1+epsilon, brute row enumeration gives a valid upper-bound falsifier to the claimed source LB_N(1+epsilon).
- A hidden selector table of size N^{q+o(1)} supplied as semantic advice defeats no-advice FE_Extract_N and must be classified as oracle, not as a transparent proof line.
- A FormulaEval extension variable with no parent pointer to an originating transparent FE row falsifies the extension-DAG parser assumption.
- A selector whose extensionality checker has overhead chi with q+tau+sigma+chi>=1+epsilon collapses the claimed quantitative transfer even if the syntax is transparent.

## Learning

Cycle 106 upgrades the FormulaEval boundary from influence-complete syntax to a four-way proof-system classification. Transparent axiom, proof-line, and extension-rule FormulaEval are valid only with selector extensionality and influence closure, yielding Gamma_cls and the q-density trichotomy. Semantic oracle FormulaEval is not an uncharged proof line; the unread-enable-bit row is a minimal falsifier. This is route-level proof-system certification, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The remaining gap is not another abstract barrier issue; it is whether a single semantic FormulaEval atom can hide influential SAT rows while preserving the displayed proof transcript. A concrete unread-enable experiment tests exactly the target-preserving parser interface.
- Situation seed: A padded beta-zero SAT-parity family H_N^SAT with M_N=N^{q+o(1)} rows, where one Psys_sym FormulaEval line uses selector a_e that enumerates all visible rows plus a private row r* only when a hidden enable bit e=1.
- Varied variable: selector opacity lambda, the number of enabled influential rows hidden from the proof-visible selector code, varied from lambda=0 to lambda=1 and then to lambda=N^{alpha}.
- Held-fixed controls: The generator G_N, row universe M_N=N^{q+o(1)}, and SAT-instance length polylog(N) are fixed., The claimed lower-bound sentence LB_N(1+epsilon), proof length exponent tau, formula length exponent eta, and generator exponent rho are fixed., The parser is no-advice and may read only displayed proof bits, verifier code, extension parent pointers, and visible selector certificates., The target is the same nonuniform SIZE upper-bound falsifier for H_N^SAT, not a many-one reduction to a different language.
- Expected observation: At lambda=0, transparent enumeration gives the Gamma_cls transfer. At lambda=1, a parser that omits r* can be forced to compute the wrong parity on some x, so semantic FormulaEval is already outside the valid parser theorem. For lambda=N^{alpha}, either the proof pays N^{1+alpha} row expansion or the claimed support theorem fails.
- Transfer certificate needed: A valid transfer requires SelectorExtensionality_N plus RealSATInfluenceRealizer_N proving that every row whose SAT bit can affect a FormulaEval truth value is enumerated and charged in K_idx^cls or E_N^cls with no hidden advice.

## Next Experiment

Run the proof-quality audit on FE106-FourWay-Extract: instantiate one ext-mode FormulaEval line with explicit parent pointers, verify the N^{q+tau+sigma+chi+o(1)} enumeration overhead, and decide whether SelectorExtensionality_N can be made a syntactic verifier rule rather than an external semantic promise.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Fiber-capped projected guarded-dDNNF selectors are transparent FormulaEval mechanisms: if C_N(r,z) is a bit-explicit guarded deterministic decomposable NNF for accepting row-witness pairs and every selected row has at most L_N witnesses, then RowSetEnumerator_N for R_N={r: exists z C_N(r,z)=1} has expansion charge S_N+W_N N^{o(1)}+T_N M_N N^{o(1)}, with W_N<=T_N L_N. Hence any beta-zero LB_N proof using this projected selector below that charge is refuted by a transcript upper-bound falsifier.

## Definitions

- source object: a Psys_sym FormulaEval selector C_N(r,z) represented as an E-uniform guarded deterministic decomposable NNF over row bits r and auxiliary witness bits z, with size S_N and syntactic guard/decomposability certificates.
- target object: the beta-zero SAT-parity truth table H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) and the row set R_N={r: exists z C_N(r,z)=1} used by a lower-bound proof for C(H_N^SAT)>N^{1+epsilon-o(1)}.
- controlled interface: RowSetEnumerator_N enumerates all accepting pairs (r,z), sorts their row projections, removes duplicates, and expands the M_N generated SAT instances for every distinct selected row.
- target-preserving condition: the selector, guard certificates, sorting/dedup transcript, and generator G_N are advice-free and E-uniform; the proof system treats FormulaEval-SAT as syntactic expansion, not as an unparsed semantic oracle.

## Assumptions

- Model: Psys_sym is Cook-Reckhow checkable after replacing the FormulaEval step by explicit row-witness enumeration, sorting-network lines, duplicate-elimination witnesses, and SAT-instance expansion lines.
- Regime: M_N=N^{q+o(1)}, T_N=|R_N|=N^{t+o(1)}, L_N=N^{ell+o(1)}, S_N=N^{s+o(1)}, and row indices have O(log N) bits.
- Uniformity/advice: C_N, the variable partition tree, guard annotations, fiber cap certificate, and G_N are generated in time 2^{O(log N)} or by the ambient E-uniform proof-transcript constructor; no selector advice chooses hard rows.
- Same-theory condition: the expanded transcript proves the same row-parity facts as the projected FormulaEval rule because duplicate projected rows are charged once after syntactic stable sorting and deduplication.
- Barrier scope: the lemma is non-natural and proof-mediated; it does not construct a large decidable useful property and does not imply P != NP.

## Equations

- fiber_bound: `W_N=|\{(r,z):C_N(r,z)=1\}|\le T_N L_N`. Valid when: Valid when the projected selector has a certified row-fiber cap and C_N enumerates accepting row-witness pairs without semantic omissions.
- projected_formulaeval_charge: `\Gamma_{proj}(N)\le S_N+W_N N^{o(1)}+T_N M_N N^{o(1)}`. Valid when: Applies after deterministic decomposability gives pair enumeration and syntactic sorting-dedup preserves the projected row set.
- exponent_ledger: `\gamma_{proj}\le \max\{s,t+\ell,t+q\}+o(1)`. Valid when: Requires polynomially bounded exponent parameters S_N=N^s, T_N=N^t, L_N=N^ell, and M_N=N^q in the beta-zero length regime.
- upper_bound_falsifier: `N^{\rho+o(1)}+\Gamma_{base}(N)+\Gamma_{proj}(N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Valid when the parsed transcript plus generator circuit computes H_N^SAT in the same nonuniform circuit model as the claimed lower bound.

## Attempted Derivation

- Start with guarded deterministic decomposable NNF C_N(r,z). The guard certificate names the variable partition at each product gate and proves that each accepting assignment to (r,z) is generated exactly once.
- Run the standard dDNNF enumeration recursion to emit all W_N accepting pairs. Determinism prevents duplicate pairs; decomposability permits Cartesian-product enumeration with only S_N+W_N N^{o(1)} transcript overhead.
- Project each pair to r, sort the O(log N)-bit row names by a uniform sorting network of size W_N N^{o(1)}, and mark first occurrences. This yields exactly R_N because r is output iff some accepting witness z was emitted.
- For every marked row r, expand the M_N generated SAT formulas G_N(r,j) and their occurrence-level FormulaEval bits. This costs T_N M_N N^{o(1)} in the transcript ledger.
- Substitute this explicit transcript for the projected FormulaEval-SAT line in the parsed Psys_bEF/Psys_sym proof. If the resulting generator plus transcript circuit is below N^{1+epsilon-o(1)}, the asserted LB_N(1+epsilon) is false in the same circuit model.

Blocking gap: The derivation is complete only for syntactically guarded deterministic decomposable selectors with a verifiable fiber cap or with pair enumeration charged by W_N. It does not handle arbitrary AC0, nondeterministic DNNF without determinism, or semantic projection rules.

## Falsifiers

- falsifier: a projected selector with one visible row and N^{Omega(1)} hidden witnesses collapses the claimed T_N-only charge unless W_N or L_N is paid.
- falsifier: nondeterministic DNNF with overlapping witnesses can enumerate the same row many times and invalidates support-sensitive FormulaEval accounting without sorting/dedup charge.
- falsifier: membership-only projection lets an unread row be privately assigned the opposite SAT parity while all emitted occurrence neighborhoods remain valid.
- A claimed transfer is invalid if the row selector uses nonuniform advice to choose hard rows or if FormulaEval-SAT is treated as a semantic oracle rather than a syntactic proof mechanism.

## Learning

The new quantitative invariant is projection fiber entropy. Guarded dDNNF transparency survives auxiliary witnesses only after paying W_N or ell; a projected row selector is not valid at T_N cost merely because the projected support is small. This closes a concrete FormulaEval loophole while preserving the non-claim that no main P vs NP lower bound has been proved.

## Gedanken Experiment Design Seed

- Need decision: `use now as a falsifier probe and threshold calibration for projected FormulaEval selectors`
- Rationale: Recent progress promoted transparent gDNNF selectors; the next hidden risk is that auxiliary existential variables smuggle semantic projection or nonuniform row choice without paying occurrence expansion.
- Situation seed: A padded beta-zero SAT-parity family H_N^SAT where a projected guarded-dDNNF selector C_N(r,z) selects T_N=N^t rows, each row has L_N=N^ell witnesses, and each selected row requires M_N=N^q SAT-instance expansions.
- Varied variable: fiber exponent ell in L_N=N^{ell+o(1)}
- Held-fixed controls: Generator overhead remains N^{rho+o(1)} and formula length remains polylogarithmic., The selector syntax is E-uniform and guarded deterministic decomposable before projection., The target lower-bound claim is C(H_N^SAT)>N^{1+epsilon-o(1)} in the same nonuniform circuit model., FormulaEval-SAT must be replaced by explicit occurrence transcript lines, not by semantic SAT oracle access.
- Expected observation: As ell increases, the transparent charge moves from max{s,t+q} to max{s,t+ell,t+q}; once max{s,t+ell,t+q,rho} reaches 1+epsilon, the low-cost-transcript falsifier loses force but the selector is still not a free semantic escape.
- Transfer certificate needed: A formal RowSetEnumerator_N certificate consisting of guarded dDNNF pair enumeration, stable sorting/dedup proof, fiber-cap or W_N accounting, and same-theory SAT occurrence expansion before the intuition may affect proof obligations.

## Next Experiment

Instantiate the lemma on one explicit projected selector: a guarded dDNNF over row bits plus a_k auxiliary block choices with certified fiber L_N=N^ell; write the verifier fields for guard partitions, pair enumeration order, sorting/dedup lines, and plug the resulting gamma_proj into the Gamma_bEF transcript theorem.
