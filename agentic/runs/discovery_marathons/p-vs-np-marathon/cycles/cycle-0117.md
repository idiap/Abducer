# cycle-0117

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: Transparent FormulaEval Boundary

## Candidate Lemma

For extensional Psys_sym FormulaEval rules over the beta-zero SAT-parity carrier, TransparentRowSupport_N is not only sufficient but locally necessary for parser-safe occurrence completion: if every row influence is surfaced and charged, the Gamma_trans line induction is valid; if some nonsemantic influence is hidden, a private-row or unread-enable-bit two-world falsifier preserves the visible transcript while changing the induced carrier row parity.

## Definitions

- source object: beta-zero SAT-parity carrier H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and formula length L_N=(log N)^d so the SAT-query exponent beta is zero.
- target object: the restricted source lower-bound assertion LB_N(1+epsilon), meaning C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)} in the same nonuniform circuit model; this is not the main P != NP conjecture.
- controlled interface: TransparentRowSupport_N for Psys_sym FormulaEval lines, requiring visible selector code, advice-free row enumeration or full-scan charge, influence closure, same-theory occurrence expansion, and no hidden semantic support advice.
- target-preserving condition: the charged transcript satisfies N^{rho+o(1)}+Gamma_trans(pi)+E_N N<N^{1+epsilon-o(1)}, q and rho remain below 1+epsilon, and no step upgrades occurrence-local parsing to full semantic FormulaEval without RealSATInfluenceRealizer_N.

## Assumptions

- Circuit model is nonuniform SIZE with equality patches charged by O(E_N N) gates and with all generator circuits counted in N^{rho+o(1)}.
- Proof model is Psys_bEF^- plus extensional FormulaEval rules whose syntactic selectors are finite strings parsed in the same theory; ordinary semantic SAT facts are not allowed unless separately realized.
- Length regime is N to infinity, M_N=N^{q+o(1)}, L_N=(log N)^d with d>1, and all o(1) losses are uniform over the fixed proof family.
- Transparency means the parser outputs K_idx(pi), row witnesses, and occurrence neighborhoods without advice depending on the hidden SAT label vector.
- Necessity direction is local: it applies to extensional FormulaEval mechanisms where the truth of a line is a function of declared row values; it does not refute genuinely nonrelativizing RealSATInfluenceRealizer_N principles.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad |G_N|=N^{\rho+o(1)}`. Valid when: Valid when the source carrier is the beta-zero generated parity family and the generator produces polylogarithmic SAT instances with uniform decoding.
- transparent_charge: `\Gamma_{trans}(\pi)=\Gamma_{bEF}(\pi)+U_N(\pi)+X_N(\pi)+F_{FE}(\pi)N^{1+q+o(1)}`. Valid when: Applies after every FormulaEval line either supplies an advice-free row enumerator or is charged by full syntactic scan in the same proof theory.
- falsifier_window: `N^{\rho+o(1)}+\Gamma_{trans}(\pi)+E_NN<N^{1+\epsilon-o(1)}\;\Longrightarrow\; \neg LB_N(1+\epsilon)`. Valid when: Requires the parser-to-circuit simulation to preserve the nonuniform SIZE model and the residual error set to have at most E_N source rows.
- support_density_corollary: `|K_{idx}(\pi)|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Valid when LB_N(1+epsilon) is claimed and the only surfaced FormulaEval support is row-index support among M_N=N^{q+o(1)} slots.

## Attempted Derivation

- Fix a Psys_sym proof pi of LB_N(1+epsilon) for H_N^SAT and parse all Psys_bEF^- lines using the existing bit-explicit EF, SATeq, bounded-SR_h, and sparse-row charges.
- For each FormulaEval line, require TransparentRowSupport_N: the parser receives visible selector code, an advice-free enumerator or full scan, row expansion into occurrence neighborhoods, and influence closure under enable bits and projections.
- Add the enumerator cost U_l, expansion cost X_l, or full-scan cost N^{1+q+o(1)} for the line; summing over lines yields Gamma_trans(pi).
- Run the line induction: every accepted proof line has a circuit/transcript implementation whose size is bounded by the accumulated Gamma_trans prefix, and bounded-SR_h contributes exactly its previous B_SR charge.
- Compose the generator circuit of size N^{rho+o(1)} with the parsed transcript; if the residual exceptional rows are E_N, patch them by equality tests at cost O(E_N N).
- Contrapose: when the total size is below N^{1+epsilon-o(1)}, the alleged LB_N(1+epsilon) certificate is falsified inside the same nonuniform SIZE model.
- For the converse minimality check, suppose an extensional FormulaEval line has a hidden influencing row r. Construct two row-label worlds equal on all surfaced rows and proof text but differing at r; the parser output is identical while the FormulaEval value or parity carrier differs.
- Therefore no occurrence parser that omits r can be sound for extensional rules; this proves local necessity of support visibility and identifies real SAT semantics as the only possible escape.

Blocking gap: The derivation is complete for extensional FormulaEval rules but still blocked for full semantic FormulaEval at RealSATInfluenceRealizer_N, which must nonrelativizingly force real SAT influence into charged same-theory support.

## Falsifiers

- Private-row falsifier: an uncharged active row outside K_idx(pi) yields two visible-identical transcripts with different row labels, invalidating occurrence completion.
- Unread-enable-bit falsifier: a hidden guard selects a row only in one world, so selector extensionality fails unless the guard is surfaced and charged.
- Threshold falsifier: if N^{rho+o(1)}+Gamma_trans(pi)+E_NN<N^{1+epsilon-o(1)}, any claimed LB_N(1+epsilon) certificate collapses to a small circuit.
- Positive-beta falsifier: any repair introducing target queries of length N^beta with beta>0 reactivates the q+beta c transfer cap and cannot exclude all SAT polynomial exponents.
- Nonuniform-leakage falsifier: if row enumeration uses advice depending on SAT labels, the parser theorem is invalid even when its apparent U_N charge is small.

## Learning

Cycle 117 upgrades the promoted theorem pair from sufficiency plus informal minimality to a local safety iff for extensional FormulaEval: surfaced influence is exactly what makes the Gamma_trans parser valid, and unsurfaced nonsemantic influence is exactly what the private-row/unread-enable-bit falsifier exploits. The full semantic case is not dismissed by a barrier slogan; it is isolated as the nonrelativizing RealSATInfluenceRealizer_N obligation. This is a paper-level route-boundary result, not a proof of P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for hidden-support minimality, not as evidence for P != NP.`
- Rationale: The theorem pair is already promoted; the remaining risk is an unnoticed FormulaEval mechanism that influences H_N^SAT through a row not surfaced by TransparentRowSupport_N while still pretending to be parser-safe.
- Situation seed: Take H_N^SAT(x)=xor_{j<=N^q} SAT(G_N(x,j)) and add one FormulaEval line with a selector S(a,r)=visible_interval(a,r) OR (e(a) AND r=r*(a)); the enable bit e(a) is not enumerated, and r*(a) is a private generated row.
- Varied variable: The hidden-enable density theta where e(a)=1 on N^theta source inputs, with q,rho,epsilon and the visible interval selector held fixed.
- Held-fixed controls: M_N=N^{q+o(1)} with q<1+epsilon and L_N=(log N)^d, d>1, so beta remains zero., Generator size N^{rho+o(1)} with rho<1+epsilon is charged exactly once., Psys_bEF^- SR_h, SATeq, and bit-explicit extension charges remain unchanged., No nonuniform advice may reveal r*(a) or e(a) unless it is charged in U_N or X_N.
- Expected observation: For theta<epsilon, even wrong handling on the hidden-enable inputs is equality-patchable at cost N^{1+theta}<N^{1+epsilon}; for any theta, two row-label worlds that differ only at enabled private rows defeat occurrence parsing unless the enable support is surfaced.
- Transfer certificate needed: A valid escape needs RealSATInfluenceRealizer_N producing an advice-free charged certificate for e(a), r*(a), and the real SAT influence of each enabled private row; otherwise the thought experiment is a formal hidden-support countermodel.

## Next Experiment

Write the paper-ready theorem statement as three clauses: TransparentRowSupport_N positive Gamma_trans induction; extensional hidden-support private-row/unread-enable-bit countermodel; RealSATInfluenceRealizer_N open semantic escape with overhead R_N and explicit non-claims.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For Psys_sym^TRS, a proof-visible TransparentRowSupport_N certificate is enough to produce a deterministic no-advice occurrence transcript Q_pi and a same-model upper-bound falsifier. This is a restricted proof-system theorem, not a P != NP claim.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with N=2^n, M_N=N^{q+o(1)}, explicit generator G_N of size N^{rho+o(1)}, and polylogarithmic SAT row length.
- target object: the audited target is the proof-system transfer claim LB_N(1+epsilon) asserting C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)} in the same nonuniform Boolean circuit model.
- controlled interface: TransparentRowSupport_N consists of visible selector code, an advice-free RowSet enumerator or full-scan charge, selector extensionality checks, influence-closure witnesses, same-theory row expansion templates, and no hidden semantic support bits.
- target-preserving condition: every semantically influential FormulaEval row is visible and charged, the expansion stays inside the named proof theory, rho<1+epsilon, and all circuit-size charges are measured on the same N-bit carrier.
- Gamma_bEF(pi) is the existing bit-explicit charge from bEF, SATeq, and bounded-SR_h line parsing.
- K_idx^+(pi) is the set of visibly indexed SAT rows touched by transparent FormulaEval lines after influence closure.
- E_N^*(pi) is the number of fully expanded or full-scan FormulaEval rows charged outside K_idx^+(pi).
- U_N(pi) is the total row-enumerator and selector-extensionality verification debt, counted as bit/circuit work.

## Assumptions

- Model: nonuniform Boolean SIZE over the truth table carrier H_N^SAT; reductions are parser/simulation reductions, not many-one reductions from SAT.
- Proof model: Psys_sym^TRS is bEF plus FormulaEval rules carrying the controlled interface fields named above.
- Uniformity: the transcript extractor and RowSet checker are deterministic and advice-free, with all selector code printed in pi.
- Regime: N tends to infinity, q,rho,tau,eta,sigma are fixed exponents up to o(1), |pi|=N^{tau+o(1)}, and rho<1+epsilon.
- Same-theory condition: each FormulaEval expansion is a derivable bEF/SATeq/bounded-SR_h occurrence transcript over the same row syntax, not an external semantic oracle.
- Influence condition: changing rows outside the certified RowSet cannot change the truth value or applicability of the FormulaEval line in the proof.
- Naturalness boundary: if the transcript is converted into a large constructive useful truth-table property, the natural-proofs falsifier applies separately; this lemma only certifies transparent proof charge.

## Equations

- canonical_charge: `\Gamma_{trans}(\pi)=\Gamma_{bEF}(\pi)+U_N(\pi)+X_N(\pi),\quad X_N(\pi)=N\bigl(|K_{idx}^+(\pi)|+E_N^*(\pi)\bigr)+N^{o(1)}.`. Valid when: Valid when every FormulaEval line has a TransparentRowSupport_N certificate and row expansion is performed in the same bit-explicit proof theory.
- row_equivalent_support: `\widehat S_{eff}(\pi)=\left\lceil\frac{\Gamma_{bEF}(\pi)+U_N(\pi)}{N}\right\rceil+|K_{idx}^+(\pi)|+E_N^*(\pi).`. Valid when: Valid when Gamma_bEF and U_N are raw bit charges while FormulaEval row expansion costs N per charged row.
- same_model_upper_bound: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{trans}(\pi).`. Valid when: Applies after the parser transcript and explicit generator are compiled into the same nonuniform SIZE circuit model without advice leakage.
- subthreshold_falsifier: `N^{\rho+o(1)}+\Gamma_{trans}(\pi)<N^{1+\epsilon-o(1)}\ \Rightarrow\ \pi\text{ cannot soundly prove }LB_N(1+\epsilon).`. Valid when: Valid when LB_N(1+epsilon) is interpreted as a same-carrier SIZE lower bound and the proof system is sound for that statement.
- forced_row_equivalent_charge: `LB_N(1+\epsilon)\text{ soundly proved and }\rho<1+\epsilon\ \Rightarrow\ \widehat S_{eff}(\pi)\ge N^{\epsilon-o(1)}.`. Valid when: Requires the previous upper-bound inequality and the normalization of Gamma_trans into N-sized row-equivalent support units.
- visible_density_corollary: `\frac{|K_{idx}^+(\pi)|}{M_N}\ge N^{\epsilon-q-o(1)}`. Valid when: Valid when the bEF debt, enumeration debt, and full-scan expansion debt are each o(N^{epsilon}) in row-equivalent units.

## Attempted Derivation

- Fix N=2^n, M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and an accepted Psys_sym^TRS proof pi of LB_N(1+epsilon).
- Parse bEF, SATeq, and bounded-SR_h lines using the existing bit-explicit parser, adding their contribution to Gamma_bEF(pi).
- For each FormulaEval line, read the printed selector code, RowSet enumerator, influence witnesses, extensionality checks, and row-expansion template; reject if any field is missing.
- Run the enumerator or charge the full scan. The enumerated rows define K_idx^+ and E_N^*, while the enumeration and extensionality work contributes U_N.
- Replace the FormulaEval line by the same-theory occurrence expansion over the enumerated rows; influence closure proves that rows outside the certificate cannot alter downstream proof acceptance.
- Induct over proof lines: the prefix transcript after line t simulates the original proof prefix and has charge at most Gamma_bEF(prefix)+U(prefix)+X(prefix).
- Compile the explicit generator plus the final transcript into a nonuniform circuit for H_N^SAT of size at most N^{rho+o(1)}+Gamma_trans(pi).
- Conclude that a subthreshold transcript is a same-model falsifier to the asserted lower-bound proof, and that any sound transparent proof must pay N^{epsilon-o(1)} row-equivalent support.

Blocking gap: The derivation proves only the restricted Psys_sym^TRS theorem. For arbitrary semantic RealSAT FormulaEval atoms, influence closure and RowSet enumeration are unavailable without RealSATInfluenceRealizer_N.

## Falsifiers

- falsifier: an unread-enable-bit FormulaEval atom chooses row j* privately; visible fields and Gamma_surface are unchanged while the carrier parity can flip.
- falsifier: selector extensionality is certified by a semantic oracle rather than proof-visible code, so U_N omits an advice table of M_N row decisions.
- falsifier: q<epsilon together with rho<1+epsilon and subthreshold Gamma_trans gives an explicit SIZE upper bound contradicting LB_N(1+epsilon).
- falsifier: bEF-heavy proofs with large Gamma_bEF show that visible FormulaEval row density cannot be inferred unless bEF and enumeration debt are separately small.
- falsifier: a RealSAT composition axiom whose influential rows are not syntactic occurrences defeats occurrence-only parsers unless RealSATInfluenceRealizer_N is supplied.

## Learning

Cycle 117 closes an independent-checkability hole: TransparentRowSupport_N is a finite verifier interface whose accepted FormulaEval lines canonically expand with Gamma_trans=Gamma_bEF+U_N+X_N. The valid theorem is restricted to proof-visible influence; opaque semantic FormulaEval is blocked by the private-row bisimulation unless RealSATInfluenceRealizer_N is proved. This is route-level proof-system certification, not P != NP progress.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the RealSATInfluenceRealizer_N gap.`
- Rationale: The abstract TRS theorem is already charged; the remaining uncertainty is whether semantic FormulaEval can hide row influence while preserving the same lower-bound target. A concrete private-row family tests exactly that interface.
- Situation seed: Private-enable FormulaEval family over H_N^SAT: M_N=N^{q+o(1)} SAT rows are public, but a semantic FormulaEval oracle contains an unread enable bit e_j and privately selects one influential row j* not printed in the proof transcript.
- Varied variable: hidden_support_entropy h=log_2 |J_hidden|, the number of bits needed to identify the semantically influential private row.
- Held-fixed controls: The source carrier H_N^SAT, generator size N^{rho+o(1)}, and lower-bound statement LB_N(1+epsilon) are held fixed., The visible proof length |pi|=N^{tau+o(1)} and all bEF/SATeq/bounded-SR_h parser rules are held fixed., No advice is allowed to the extractor except proof-visible selector and FormulaEval fields., The target model remains nonuniform Boolean SIZE on the same N-bit carrier.
- Expected observation: For h larger than the visible selector budget, two semantic worlds can agree on every checked transcript bit but disagree on j* and on H_N^SAT parity. Thus surface occurrence charge is not target-preserving; only a realizer that recovers j* restores validity.
- Transfer certificate needed: A RealSATInfluenceRealizer_N certificate proving that every semantically influential private row is uniformly recoverable, selector-extensional, influence-closed, and charged by U_N plus N per realized row before the intuition may enter proof obligations.

## Next Experiment

Run a referee-style proof audit of cycle117.TRSCheck_N_CanonicalExpansion: instantiate the checker fields on one influence-complete extension-rule FormulaEval line, verify the U_N and X_N charges line by line, and test the private-enable family as the minimal invalid non-TRS line.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For a bit-explicit Psys_bEF^- transcript extended only by TransparentRowSupport_N FormulaEval lines, a line induction derives Gamma_trans(pi)=Gamma_bEF(pi)+U_N(pi)+X_N(pi). Hence a transcript with generator cost plus Gamma_trans below N^{1+epsilon-o(1)} is a same-model upper-bound falsifier for any claimed proof of LB_N(1+epsilon).

## Definitions

- source object: a Psys_sym FormulaEval transcript pi over H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and a normalized bit-explicit Psys_bEF^- core.
- target object: a nonuniform SIZE upper-bound simulation for H_N^SAT in the same Boolean circuit model used by the lower-bound statement LB_N(1+epsilon).
- controlled interface: TransparentRowSupport_N means visible selector code, advice-free row enumeration or full-scan charge U_N, same-theory occurrence expansion charge X_N, influence closure for every row whose SAT value can affect a FormulaEval assertion, and no hidden support advice.
- target-preserving condition: the transfer is valid only when every FormulaEval influence is represented by charged occurrences in the same proof theory, all row discovery is uniform from N and pi, and the induced circuit uses the original G_N and the same nonuniform SIZE convention as LB_N.

## Assumptions

- Circuit/proof model: Psys_bEF^- has the Gap98 bounded-SR_h parser normal form, and FormulaEval lines are syntactic proof or extension lines rather than an unparsed semantic SAT oracle.
- Length regime: N tends to infinity, M_N=N^{q+o(1)}, generated SAT instances have polylogarithmic description length, and each expanded row costs E_N=N^{1+o(1)} gates or occurrences in the parser ledger.
- Uniformity/advice regime: selector programs, row enumerators, quotient witnesses, and occurrence expansions are computed uniformly from N and pi; no advice string selects rows, certificates, or hard truth tables.
- Influence-closure regime: if changing SAT(G_N(x,j)) while preserving already charged occurrences can change any FormulaEval assertion used by pi, then row j is in the visible or realized charged support.
- Barrier scope: the lemma is a parser-to-circuit simulation and finite falsifier, not a natural-property construction, not a derandomization theorem, and not a proof of P != NP.

## Equations

- Gamma ledger: `\Gamma_{trans}(\pi)=\Gamma_{bEF}(\pi)+U_N(\pi)+X_N(\pi)`. Valid when: Valid when TransparentRowSupport_N supplies visible advice-free enumeration and same-theory occurrence expansion for every FormulaEval line.
- Transcript upper bound: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{trans}(\pi)`. Valid when: Applies after the generator circuit and all parsed proof-line expansions are composed in the same nonuniform SIZE model.
- Subthreshold falsifier: `N^{\rho+o(1)}+\Gamma_{trans}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow \pi\text{ is not a valid proof of }LB_N(1+\epsilon)`. Valid when: Requires that LB_N states a lower bound against the same target circuits simulated by the parsed transcript.
- Row expansion charge: `X_N(\pi)\ge E_N\,|K_{idx}(\pi)|,\quad E_N=N^{1+o(1)}`. Valid when: Valid when each influential SAT row is expanded into same-theory occurrences with no sharing beyond the declared parser ledger.

## Attempted Derivation

- Fix N, M_N=N^{q+o(1)}, generator G_N of size N^{rho+o(1)}, and a normalized Psys_bEF^- core transcript pi for a claimed LB_N(1+epsilon).
- For base Psys_bEF^- lines, import the Gap98 bounded-SR_h line-induction ledger Gamma_bEF(pi), with no FormulaEval semantic oracle calls.
- For each TransparentRowSupport_N FormulaEval line L, run its visible enumerator or full scan, charge row-discovery cost into U_N, and obtain K_idx(L).
- For every row in K_idx(L), expand the SAT occurrence or certified quotient witness in the same proof theory and charge the expansion into X_N; influence closure makes this replacement semantics-preserving.
- Induct over proof lines: after replacing each transparent FormulaEval assertion by its charged expansion, the parsed occurrence transcript Q_pi simulates the original derivation and has total cost Gamma_bEF+U_N+X_N.
- Compose the parsed transcript with the row generator circuit for G_N to obtain a nonuniform circuit for H_N^SAT of size at most N^{rho+o(1)}+Gamma_trans(pi).
- If that size is below N^{1+epsilon-o(1)}, the transcript cannot be a valid same-model proof of LB_N(1+epsilon); this is the subthreshold falsifier.
- For the negative side, take the first FormulaEval line with j* in Infl(L) but not in Vis(L) union Real(L); build two completions agreeing on all parser-read bits while toggling the private row or unread enable bit; the parser transcript is identical but L's truth value differs.
- Conclude that transparent lines are charged and hidden-support lines are invalid unless RealSATInfluenceRealizer_N supplies advice-free same-theory influence witnesses.

Blocking gap: The restricted theorem pair is proof-shaped modulo final bit-level bookkeeping of row encodings and occurrence costs. The full semantic FormulaEval case is blocked exactly at RealSATInfluenceRealizer_N: no advice-free same-theory realization of real SAT influence has been proved.

## Falsifiers

- falsifier: an uncharged row j* whose SAT value changes a FormulaEval assertion while all parser-visible bits remain fixed.
- falsifier: selector advice or nonuniform row choice hidden inside a proof line, because it breaks the target-preserving uniformity condition.
- falsifier: membership-only AC0 or semantic DNNF support with no output-sensitive enumerator, unless it pays full scan or supplies RealSATInfluenceRealizer_N.
- falsifier: quotient or formula-identity witness whose cost is omitted from U_N, X_N, or R_N.
- falsifier: a claimed LB_N proof with N^{rho+o(1)}+Gamma_trans(pi)<N^{1+epsilon-o(1)}, since the parsed transcript gives a same-model circuit upper bound.
- falsifier: any MCSP/MKtP carrier that only selects a nonuniform hard row and does not produce an advice-free searchable row certificate within the intended target class.

## Learning

Cycle 117 converts the TransparentRowSupport_N packet into an inference-quality theorem pair: transparent FormulaEval lines are exactly charged by U_N+X_N in the Gamma ledger, while the first uncharged semantic influence is a private-row falsifier. The q-trichotomy is only a corollary of row expansion charge, and full semantic FormulaEval remains blocked at RealSATInfluenceRealizer_N rather than by generic barrier folklore.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the theorem pair.`
- Rationale: The proof packet needs a concrete check that hidden semantic support cannot be smuggled into FormulaEval without either paying X_N/R_N or becoming a semantic-oracle rule.
- Situation seed: A padded beta-zero SAT-parity family H_N^SAT(x)=xor_{j<=N^{q}} SAT(G_N(x,j)) with a Psys_sym transcript containing one FormulaEval selector whose surface code enumerates N^v rows but whose semantic predicate also depends on a private enabled row j*.
- Varied variable: The support visibility exponent v, where the charged visible support size is |K_idx|=N^{v+o(1)} while q, rho, and epsilon are fixed.
- Held-fixed controls: The generator G_N, row encoding, and nonuniform SIZE target model are fixed across completions., The Psys_bEF^- core parser and bounded-SR_h normal form are fixed and bit-explicit., No advice strings, nonuniform selectors, or external hard-row choices are permitted., The claimed lower-bound threshold remains LB_N(1+epsilon) for the same H_N^SAT.
- Expected observation: If v<epsilon and no private row exists, the transcript is subthreshold and gives an upper-bound falsifier. If the private row influences FormulaEval, two completions agreeing on all charged bits flip the assertion, proving hidden support invalid. The only escape is a realizer that raises charged support or realization cost to the threshold.
- Transfer certificate needed: A checked TransparentRowSupport_N line induction for the positive case, or an advice-free RealSATInfluenceRealizer_N witness covering j* before the semantic intuition may affect proof obligations.

## Next Experiment

Finish the bit-level proof appendix for L117: specify row-id fields, selector output encoding, occurrence-expansion format, incremental union ledger for U_N and X_N, and the exact private-row completion for one FormulaEval line in the chosen Psys_sym fragment.
