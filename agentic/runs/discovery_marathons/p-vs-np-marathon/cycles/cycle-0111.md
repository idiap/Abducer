# cycle-0111

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For Psys_sym proofs whose FormulaEval lines satisfy TransparentRowSupport_N, every accepted LB_N(1+epsilon) certificate parses to a charged transcript with Gamma_trans(pi)=Gamma_bEF^-(pi)+U_N(pi)+X_N(pi). If N^{rho+o(1)}+Gamma_trans(pi)+E_N N^{1+o(1)}<N^{1+epsilon-o(1)}, the certificate is falsified in the same nonuniform SIZE model. This is a restricted parser/falsifier theorem, not P != NP.

## Definitions

- source object: H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), where M_N=N^{q+o(1)}, |G_N(x,j)|=(log N)^d with d>1, C(G_N)=N^{rho+o(1)}, and LB_N(1+epsilon) abbreviates C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)}.
- target object: a parser-to-circuit falsifier for a Psys_sym lower-bound certificate pi; the target is invalidating subthreshold proof-mediated evidence for LB_N, not proving NP not subset P/poly.
- controlled interface: TransparentRowSupport_N means every FormulaEval line has visible selector code, advice-free row enumeration or a charged full scan, influence closure, same-theory occurrence expansion, and no hidden support advice.
- target-preserving condition: the simulation stays in the same nonuniform SIZE model, uses valid lengths, has beta=0 polylog SAT queries, keeps q,rho<1+epsilon, and never upgrades hidden semantic support to occurrence support unless it is surfaced and charged or RealSATInfluenceRealizer_N is supplied.

## Assumptions

- Psys_bEF^- lines are bit-explicit with declared parent pointers, extension supports, SATeq links, and bounded-SR_h leaves already charged in Gamma_bEF^-.
- Each FormulaEval line a satisfies TransparentRowSupport_N: RowSet(a) is produced by a finite visible selector/enumerator or the line pays the full scan charge.
- Influence closure is extensional over occurrence labels: changing any row outside RowSet(a) cannot change the parsed FormulaEval value in the proof transcript.
- The proof-to-circuit extraction is advice-free except for ordinary nonuniform circuit descriptions counted in Gamma_trans(pi).
- Residual row errors E_N are explicitly equality-patched; if E_N=0 the theorem is an exact parser upper bound.
- epsilon>0 is fixed, q,rho,eta,tau are constants or o(1)-tracked exponents, and all o(1) losses are uniform over valid N.

## Equations

- transparent_charge: `\Gamma_{\mathrm{trans}}(\pi)=\Gamma_{\mathrm{bEF}^{-}}(\pi)+U_N(\pi)+X_N(\pi)`. Valid when: Valid when every FormulaEval influence is enumerated or full-scanned and occurrence expansion is performed inside the same parsed proof theory.
- formulaeval_line_charge: `B_{FE}(a)\le \min\{U_a+X_a,\ F_a N^{1+q+o(1)}\}`. Valid when: Applies when the selector code for line a is visible and the fallback full scan ranges over all N source rows and M_N=N^{q+o(1)} slots.
- parser_upper_bound: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{\mathrm{trans}}(\pi)+E_N N^{1+o(1)}`. Valid when: Valid when the line-induction parser outputs circuits for every unpatched source row and residual rows are equality patched in the same nonuniform SIZE model.
- support_density_trichotomy: `|K_{idx}(\pi)|\ge N^{\epsilon-o(1)},\quad |K_{idx}(\pi)|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Requires LB_N(1+epsilon), beta-zero transfer, and the convention that each surfaced complete parity-slot support costs N^{1+o(1)} in Gamma_trans.

## Attempted Derivation

- Source statement: For beta-zero parity carrier H_N^SAT with M_N=N^{q+o(1)}, polylog SAT instances, generator size N^{rho+o(1)}, and source lower-bound claim LB_N(1+epsilon), audit proof certificates in Psys_sym.
- Target statement: Prove a restricted parser/falsifier theorem for transparent FormulaEval and a countermodel theorem for hidden FormulaEval; do not infer P != NP or NP not subset P/poly.
- Model context: nonuniform SIZE circuits for H_N, bit-explicit Psys_bEF^- proof lines, FormulaEval extension rules, bounded-SR_h leaves, SATeq links, and same-theory occurrence expansions.
- Quantifier context: fixed epsilon>0; q,rho<1+epsilon; beta=0 because query length is polylogarithmic; all o(1) losses uniform on valid lengths; no uncharged advice or semantic row leakage.
- Line induction base: axioms, bit-explicit EF extensions, SATeq links, and bounded-SR_h rules already have support fields and contribute exactly their Gamma_bEF^- charges from the prior SR_h normal form packet.
- FormulaEval induction step: TransparentRowSupport_N supplies either an advice-free RowSet enumerator with cost U_a or a full scan over N*M_N rows, then same-theory occurrence expansion costs X_a; influence closure ensures no omitted row can affect the transcript.
- Circuit extraction: combine the generator circuit, all parsed local transcript circuits, and equality patches for E_N residual source rows to obtain size at most N^{rho+o(1)}+Gamma_trans(pi)+E_N N^{1+o(1)}.
- Falsifier consequence: if this upper bound is below N^{1+epsilon-o(1)}, the certificate cannot be valid evidence for LB_N(1+epsilon) in the same SIZE model.
- Hidden-support proof: if visibility, selector extensionality, or influence closure fails, choose a private row or unread enable bit; two completions agree on all charged transcript fields but differ on the FormulaEval value or carrier parity, so occurrence completion is invalid.
- Barrier status: the positive transparent theorem is syntactic and relativizing; the hidden-support escape requires a nonrelativizing real-SAT influence realizer. Natural-proofs and algebrization are not the operative obstruction in this theorem pair.
- Reviewer handoff: pvsnp-inference-quality-controller checks source/target statements; reduction-consistency checks beta-zero substitution; quantifier-uniformity checks q,rho,epsilon and advice; barrier-specificity checks private-row scope; proof-derivation-builder checks the line induction.

Blocking gap: No gap remains for the conditional TransparentRowSupport_N theorem pair. The full Psys_sym extension is blocked exactly at RealSATInfluenceRealizer_N for hidden semantic FormulaEval lines.

## Falsifiers

- q<epsilon support-density falsifier: |K_idx|/M_N would exceed 1, so a subthreshold transparent proof cannot certify LB_N(1+epsilon).
- Private-row falsifier: a hidden FormulaEval influence absent from RowSet(a) yields two charged-identical transcripts with different induced parity.
- Unread-enable-bit falsifier: selector code may look empty while an uncharged semantic enable bit activates a row.
- Threshold-collapse falsifier: N^{rho+o(1)}+Gamma_trans+E_NN^{1+o(1)} below N^{1+epsilon-o(1)} gives a same-model upper bound against the claimed LB_N.
- Nonuniform-leakage falsifier: U_N or X_N supplied as semantic advice rather than finite visible code invalidates the parser theorem.
- Model-mismatch falsifier: an occurrence-local proof step is advertised as real-SAT semantic without same-theory expansion or RealSATInfluenceRealizer_N.

## Learning

Cycle 111 converts the transparent FormulaEval consolidation into a proof-delivery packet: Gamma_trans is derived by line induction, hidden support has a precise private-row falsifier, and the only full semantic escape is the named nonrelativizing RealSATInfluenceRealizer_N. This is a valid scoped parser/falsifier contribution, not progress on the main P vs NP conjecture itself.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The theorem pair is already abstractly stated; the remaining risk is whether hidden semantic FormulaEval can evade RowSet charging while still affecting the beta-zero parity carrier.
- Situation seed: A Psys_sym FormulaEval line for H_N^SAT has visible selector code selecting no rows, but a hidden enable bit e(x,j) semantically activates one generated SAT instance G_N(x*,j*) in the proof of LB_N(1+epsilon).
- Varied variable: leakage_count lambda_N, the number of semantically enabled but unenumerated row-slot pairs in FormulaEval lines.
- Held-fixed controls: M_N=N^{q+o(1)} with q<1+epsilon and polylog formula length, so beta=0 remains fixed., Generator size N^{rho+o(1)} and the bit-explicit Gamma_bEF^- charges are held fixed., The proof transcript, visible selector code, and charged RowSet fields are identical in the two completions., The target model remains nonuniform SIZE with equality patching charged at N^{1+o(1)} per residual source row.
- Expected observation: At lambda_N=0 the TransparentRowSupport_N line induction is valid. At lambda_N>=1 a private-row flip changes the FormulaEval value or carrier parity while all charged fields agree, proving that hidden support cannot be used without a realizer charge.
- Transfer certificate needed: RealSATInfluenceRealizer_N must turn every hidden real-SAT influence into an advice-free enumerated support with same-theory occurrence expansion and explicit U_N+X_N cost before the intuition may affect proof obligations.

## Next Experiment

Write the final paper theorem text for TransparentRowSupport_N with clauses T1-T6, prove the line induction lemma in referee style, then test one genuinely semantic FormulaEval rule against RealSATInfluenceRealizer_N or instantiate the private-row countermodel.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

TransparentRowSupport_N gives a valid restricted theorem: for any accepted Psys_sym^TRS_N proof pi of LB_N(1+epsilon) for the beta-zero SAT-parity carrier, the same-theory parser extracts a charged transcript Gamma_trans(pi). If the proof is sound in the nonuniform SIZE target, then the extracted simulation forces N^{rho+o(1)}+Gamma_trans(pi)>=N^{1+epsilon-o(1)} and effective support at least N^{epsilon-o(1)}. Hence a subthreshold Gamma_trans is a concrete falsifier of the claimed lower-bound proof, not evidence for P != NP.

## Definitions

- source object: an accepted Psys_sym^TRS_N proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}.
- target object: the extracted charged transcript Gamma_trans(pi) and the induced nonuniform SIZE upper-bound falsifier for H_N^SAT.
- controlled interface: TransparentRowSupport_N, consisting of visible selector code, advice-free RowSet enumeration or full-scan charge, selector extensionality, influence closure, same-theory occurrence expansion, and no hidden row advice.
- target-preserving condition: every FormulaEval or SAT-semantic line is invariant under changes to unlisted rows, and all listed or expanded rows are charged in K_idx^+(pi) before the parser-to-circuit simulation is invoked.
- K_idx^+(pi) is the union of all row indices exposed by bEF occurrence parsing, selector enumeration, full-scan FormulaEval, and influence-closure expansion.
- U_N(pi) is the total proof-visible enumeration cost for row selectors, measured as Boolean circuit or transcript bits in the same N-scale model.
- E_N^*(pi) counts charged FormulaEval row-expansion units after influence closure; X_N(pi) converts them into row-level occurrence cost.
- S_eff(pi)=|K_idx^+(pi)|+E_N^*(pi)+ceil(U_N(pi)/N) normalizes enumeration-heavy and row-heavy transparent proofs into one support threshold.

## Assumptions

- Model: nonuniform Boolean SIZE circuits over the beta-zero carrier; the proof extraction is a simulation/extraction, not a many-one reduction from SAT.
- Length regime: N=2^n, M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, proof length |pi|=N^{tau+o(1)}, selector code size N^{sigma+o(1)}, and row formulas have the fixed polylog-SAT format used by the carrier.
- Uniformity/advice regime: the parser is deterministic and advice-free; selector code, row enumerators, expansion links, and influence witnesses are visible in pi or charged by full scan.
- Same-theory regime: FormulaEval expansion uses exactly the SAT atoms and extension variables allowed by Psys_sym^TRS_N; it may not appeal to real-SAT semantic facts outside the proof language.
- Soundness regime: LB_N(1+epsilon) means C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)} in the same nonuniform target class used by the extracted upper-bound falsifier.
- Barrier regime: if the transcript becomes a poly(N)-constructive dense useful property, natural-proofs pressure applies; the theorem itself is a scoped proof-system boundary and does not claim P != NP.

## Equations

- Gamma decomposition: `\Gamma_{\mathrm{trans}}(\pi)=\Gamma_{\mathrm{bEF}}(\pi)+U_N(\pi)+X_N(\pi)`. Valid when: Valid when every bEF rule is bit-explicit and every FormulaEval line satisfies TransparentRowSupport_N with its enumerator or scan charge recorded.
- FormulaEval expansion charge: `X_N(\pi)=N\cdot E_N^*(\pi)+L_{\mathrm{FE}}(\pi),\quad L_{\mathrm{FE}}(\pi)\le N^{q+\tau+\sigma+o(1)}`. Valid when: Valid when selector evaluation is proof-visible, extensionality is checkable, and full-scan or enumerated influence closure charges each affected row.
- Extracted upper-bound falsifier: `C_{\mathrm{SIZE}}(H_N^{\mathrm{SAT}})\le N^{\rho+o(1)}+\Gamma_{\mathrm{trans}}(\pi)`. Valid when: Valid when the charged transcript supplies all SAT row values needed by the generator simulation without hidden advice or semantic leakage.
- Necessary soundness pressure: `N^{\rho+o(1)}+\Gamma_{\mathrm{trans}}(\pi)\ge N^{1+\epsilon-o(1)}`. Valid when: Valid when pi is sound for LB_N(1+epsilon) in the same nonuniform SIZE model as the extracted simulator.
- Effective support threshold: `S_{\mathrm{eff}}(\pi):=|K_{\mathrm{idx}}^+(\pi)|+E_N^*(\pi)+\lceil U_N(\pi)/N\rceil\ge N^{\epsilon-o(1)}`. Valid when: Valid when rho<1+epsilon and lower-order bEF bookkeeping is absorbed into Gamma_trans without changing the row-normalized threshold.
- q-density trichotomy: `\delta_{\mathrm{eff}}(\pi):=S_{\mathrm{eff}}(\pi)/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Valid when M_N=N^{q+o(1)} and the effective support threshold has been derived from the same transcript charge.

## Attempted Derivation

- Define for each proof line l an invariant I_l=(K_l,U_l,X_l,V_l): K_l is visible row support, U_l is enumerator cost, X_l is row-expansion cost, and V_l is the same-theory occurrence view determined by these data.
- Base bEF, SATeq, and bounded-SR_h lines inherit the cycle-110 bit-explicit parser; their occurrence neighborhoods and row labels are appended to K_l with Gamma_bEF charge.
- For a transparent FormulaEval axiom/proof line/extension rule, read its visible selector code e_l. If RowSet(e_l) is output-sensitive enumerable, add the enumeration cost to U_l and rows to K_l. If not, use full scan over M_N rows and charge L_FE<=N^{q+tau+sigma+o(1)}.
- Apply selector extensionality: two syntactically different selector descriptions must have the same listed RowSet before they can share a FormulaEval value. This blocks hidden aliasing of row support.
- Apply influence closure: any row whose SAT value can change the FormulaEval outcome is either listed in K_l or charged in E_N^*. Same-theory occurrence expansion contributes N per expansion unit, giving X_N=N E_N^*+L_FE.
- Induct over proof lines. Boolean rules combine supports by union and add local verifier charge. Extension variables inherit the support of their defining formula, so no semantic row is introduced for free.
- At the final LB_N line, the extracted transcript plus the generator circuit yields a nonuniform circuit of size at most N^{rho+o(1)}+Gamma_trans(pi). If this is below N^{1+epsilon-o(1)}, it is a falsifier to the soundness of pi as a proof of LB_N(1+epsilon).
- Normalize Gamma_trans by row cost N to obtain S_eff>=N^{epsilon-o(1)} when rho<1+epsilon. Dividing by M_N=N^{q+o(1)} gives the q-trichotomy: q<epsilon invalidates the source claim, q=epsilon forces near-full effective contact, and q>epsilon leaves only weak density pressure.
- For the negative side, remove one TRS clause. Choose a private row r* or unread enable bit. Build A,A' agreeing on every parser-visible bit but differing at r*. Then View_pi(A)=View_pi(A') while FormulaEval or H parity flips, so surface occurrence completion is not sound.

Blocking gap: The restricted theorem is proved only for Psys_sym^TRS_N. The full Psys_sym lift is blocked exactly at RealSATInfluenceRealizer_N: actual SAT semantics may constrain row toggles, and the branch lacks a proof-visible extractor for all semantically influential real-SAT rows.

## Falsifiers

- Subthreshold charge falsifier: if N^{rho+o(1)}+Gamma_trans(pi)<N^{1+epsilon-o(1)}, the extracted circuit contradicts pi's LB_N conclusion in the same SIZE model.
- q<epsilon enumeration falsifier: S_eff<=M_N=N^{q+o(1)} cannot meet S_eff>=N^{epsilon-o(1)} without extra expansion or advice leakage.
- Private-row falsifier: a FormulaEval line consults r* not visible to the parser, yielding identical View_pi but different semantic value.
- Unread-enable-bit falsifier: a hidden enable bit selects whether a row matters; if the bit is not charged, selector extensionality and influence closure fail.
- Semantic-oracle falsifier: replacing actual SAT rows by an oracle table makes hidden support possible, so any relativizing parser theorem for full FormulaEval is invalid.
- Nonuniform-leakage falsifier: if RowSet is supplied as secret advice, the extracted transcript is not target-preserving and cannot support the claimed proof-system bridge.

## Learning

Cycle 111 adds the effective-support normalization S_eff=|K_idx^+|+E_N^*+ceil(U_N/N). This separates row-heavy transparent proofs from enumeration-heavy transparent proofs while preserving the same subthreshold falsifier and q-trichotomy. The full-system gap is no longer a generic semantic concern; it is exactly RealSATInfluenceRealizer_N.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The abstract TRS definition is now stable; the remaining risk is a hidden semantic row that defeats occurrence completion while preserving the visible proof transcript. A concrete private-row experiment tests exactly the RealSATInfluenceRealizer_N boundary.
- Situation seed: Take H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)} and a Psys_sym FormulaEval extension line whose displayed selector lists an interval I but whose semantic oracle also consults a private row r* through an unread enable bit b.
- Varied variable: leakage exponent lambda, where the parser is allowed to see and charge N^{lambda+o(1)} rows including, or not including, r*.
- Held-fixed controls: Nonuniform SIZE target and LB_N(1+epsilon) threshold remain fixed., Generator size N^{rho+o(1)}, proof length N^{tau+o(1)}, and selector code size N^{sigma+o(1)} remain fixed., The parser is deterministic, advice-free, and same-theory., The FormulaEval line is the only source of possible hidden support; bEF and bounded-SR_h lines stay bit-explicit.
- Expected observation: For lambda<epsilon and r* hidden, the transcript remains subthreshold and the private-row flip is a falsifier. Once r* is exposed and charged, S_eff rises by the normalized row cost and the positive Gamma_trans theorem applies.
- Transfer certificate needed: A valid transfer requires either TransparentRowSupport_N with r* in the enumerated or expanded support, or a RealSATInfluenceRealizer_N proof that actual SAT semantics cannot hide r* outside the charged row set.

## Next Experiment

Run a referee-style proof audit of cycle111.TRS.effective_support_line_induction: verify each proof-rule case, check that U_N/N normalization cannot mask advice leakage, and attempt either a proof or finite refutation of RealSATInfluenceRealizer_N for one concrete real-SAT FormulaEval rule.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For bit-explicit Psys_bEF^- extended by Psys_sym FormulaEval lines satisfying TransparentRowSupport_N, every proof pi has a same-theory occurrence transcript of cost Gamma_trans(pi)=Gamma_bEF(pi)+U_N(pi)+X_N(pi). Therefore a purported LB_N(1+epsilon) certificate with N^{rho+o(1)}+Gamma_trans(pi)<N^{1+epsilon-o(1)} is invalid in the same nonuniform SIZE model; the transcript is a finite falsifier, not a P != NP proof.

## Definitions

- source object: A finite Psys_sym proof pi over H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, bit-explicit bEF lines, and FormulaEval lines whose selectors are part of the proof text.
- target object: A nonuniform SIZE_N upper-bound simulation for H_N^SAT and a falsifier to the specific lower-bound assertion LB_N(1+epsilon) in that same circuit model.
- controlled interface: TransparentRowSupport_N consists of visible selector code, advice-free RowSetEnumerator_N or declared full scan, influence closure for SAT-dependent rows, same-theory occurrence expansion, and no hidden support advice.
- target-preserving condition: The generator G_N, enumerators, influence witnesses, and occurrence expansions are uniform in N, preserve the target length N, and use no nonuniform hard-row selection beyond ordinary circuit hardwiring allowed in the target SIZE model.
- Gamma_bEF(pi) is the archived cost of the bit-explicit Psys_bEF^- line induction transcript.
- U_N(pi)=sum_l U_l is the total row-discovery cost over transparent FormulaEval lines.
- X_N(pi)=sum_l X_l is the total same-theory SAT occurrence-expansion cost for the listed rows.

## Assumptions

- Circuit model: nonuniform Boolean circuits of size N^a for H_N^SAT on N-bit inputs; no uniform-language lower bound is inferred.
- Length regime: N tends to infinity, M_N=N^{q+o(1)}, every G_N(x,j) has polylogarithmic SAT formula length, and generator size is N^{rho+o(1)}.
- Proof model: bEF rules satisfy the archived Gap98-SRhNormalForm and contribute exactly Gamma_bEF(pi) to the occurrence transcript.
- FormulaEval transparency: each FormulaEval line l exposes either an advice-free enumerator for K_l or pays full scan over all M_N rows; the selector code and all parameters are syntactically visible.
- Influence closure: if a SAT row can change the line value, then its row index appears in K_l and its occurrence neighborhood is expanded in the same proof theory.
- No-hidden-advice condition: the proof text contains no semantic selector, oracle row set, or nonuniform hard-row advice not charged in U_N(pi)+X_N(pi).

## Equations

- E1_length_generator: `M_N=N^{q+o(1)},\qquad |G_N|\le N^{\rho+o(1)}`. Valid when: Valid when the SAT-parity carrier is the fixed H_N^SAT family and the generator overhead is measured in the same N-input circuit model.
- E2_gamma_trans: `\Gamma_{trans}(\pi)=\Gamma_{bEF}(\pi)+U_N(\pi)+X_N(\pi)`. Valid when: Valid when every FormulaEval line satisfies TransparentRowSupport_N and bEF lines satisfy the archived Gap98 normal-form parser.
- E3_row_expansion_charge: `X_N(\pi)\le \sum_l |K_l|\,N^{o(1)}`. Valid when: Applies when each listed row expands to a polylogarithmic SAT occurrence neighborhood and row identifiers are charged explicitly.
- E4_upper_bound_falsifier: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{trans}(\pi)`. Valid when: Requires the parser-to-circuit simulation to preserve the same nonuniform SIZE target and to hardwire only the charged transcript.
- E5_threshold_conflict: `\max\{\rho,\gamma_{trans}\}<1+\epsilon\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Valid when Gamma_trans(pi)=N^{gamma_trans+o(1)} and LB_N(1+epsilon) is asserted for the identical H_N^SAT circuit family.

## Attempted Derivation

- Fix N and H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)); all costs are measured against nonuniform SIZE circuits on N-bit inputs.
- Define Q_pi as Q_bEF(pi) plus, for each FormulaEval line l, the selector code, enumerator certificate or scan declaration, the emitted row list K_l, influence witnesses, and occurrence-level expansions of SAT(G_N(x,j)) for j in K_l.
- Base and structural bEF rules preserve the invariant by the archived Gap98-SRhNormalForm, contributing Gamma_bEF(pi).
- For a transparent FormulaEval line, RowSetEnumerator_N supplies exactly the rows K_l charged by U_l; influence closure says no unlisted row can change the line; same-theory expansion charges X_l and makes all listed SAT facts visible to the occurrence parser.
- Inductively, two completions agreeing on Q_pi agree on every proof line value. Thus FormulaEval adds only U_N+X_N to the existing Gamma_bEF ledger, proving Gamma_trans(pi)=Gamma_bEF(pi)+U_N+X_N for the transparent fragment.
- Invoke the archived parser-to-circuit simulation with Q_pi replacing Q_bEF(pi). The hardwired charged transcript plus the generator G_N gives C(H_N^SAT)<=N^{rho+o(1)}+Gamma_trans(pi) in the identical target SIZE model.
- Therefore any asserted LB_N(1+epsilon) supported by such a pi is falsified whenever max{rho,gamma_trans}<1+epsilon. This is a route-specific proof-system obstruction, not a lower bound.
- For the negative branch, if K_vis misses an influential row or enable bit, choose two occurrence completions that agree on all charged fields and flip the unread SAT value; the line value changes while Q_pi is fixed, so the parser theorem is invalid unless RealSATInfluenceRealizer_N charges the influence.

Blocking gap: The positive theorem is proved only for TransparentRowSupport_N. Full semantic FormulaEval remains blocked at RealSATInfluenceRealizer_N: produce advice-free influence witnesses, pay full expansion, or accept the private-row countermodel.

## Falsifiers

- falsifier: a FormulaEval selector whose semantic support is not included in the charged row list K_l.
- falsifier: an unread enable bit that toggles a private row while every occurrence read by Q_pi is fixed.
- falsifier: a row enumerator using nonuniform advice or a hard-row selector outside the proof text.
- falsifier: q<epsilon with required forced-row density exceeding one, making the proposed LB_N(1+epsilon) certificate invalid under the transparent ledger.
- falsifier: projected or membership-only selectors without certified deduplication cost U_N or witness-support charge W_N.

## Learning

Cycle 111 converts the theorem-pair slogan into a line-induction packet: transparent FormulaEval contributes exactly U_N+X_N to Gamma_bEF, while any uncharged semantic influence yields a private-row falsifier. The result is a paper-level parser obstruction and live inference-quality claim, not progress on the main P vs NP conjecture.

## Gedanken Experiment Design Seed

- Need decision: `use now as a falsifier probe for hidden semantic FormulaEval`
- Rationale: The top proof item needs a concrete test distinguishing charged transparent support from semantic support. A private-row experiment directly validates the countermodel theorem and avoids adding another selector class.
- Situation seed: Fix H_N^SAT with M_N=N^{q+o(1)}. A Psys_sym FormulaEval line claims to evaluate xor over a selector S(e,j) where an enable bit e_{j*} for one row j* is read semantically by the rule but not output by RowSetEnumerator_N and not expanded in Q_pi.
- Varied variable: The single varied parameter is beta, the exponent of omitted influential rows, with |Infl(l)\K_vis(l)|=N^{beta+o(1)}; the minimal probe sets beta=0 for one private row.
- Held-fixed controls: M_N=N^{q+o(1)} and generator size N^{rho+o(1)} remain fixed., The proof syntax, bEF transcript Q_bEF(pi), and all charged FormulaEval row expansions remain fixed., The target claim remains LB_N(1+epsilon) for the same H_N^SAT in the same nonuniform SIZE model., No advice, padding change, or oracle is added to select j*.
- Expected observation: For beta>=0, if even one omitted row is eval-critical, two occurrence completions agree on all charged transcript bits but flip FormulaEval_l. Thus hidden semantic support invalidates the parser; if no such completion exists, the rule has supplied an implicit influence realizer that must be charged.
- Transfer certificate needed: A valid RealSATInfluenceRealizer_N certificate: an advice-free procedure, expressed in the same proof theory, that lists every eval-critical row or proves full-scan/influence closure with cost added to U_N+X_N before the intuition may enter proof obligations.

## Next Experiment

Write the paper-ready TransparentRowSupport_N definition and prove the FormulaEval induction sublemma line-by-line for one representative line l, then instantiate the hidden-support countermodel with a single omitted row j* and record the two completions A,B.
