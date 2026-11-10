# cycle-0114

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

TransparentRowSupport_N support-pressure theorem: for every large valid N, any sound Psys_sym proof pi of LB_N(1+epsilon) whose FormulaEval lines satisfy the transparent support interface must either pay the charged transcript threshold or leave at least N^{epsilon-o(1)} patchable residual rows; otherwise the parsed transcript constructs a small SIZE circuit and is a valid falsifier for the claimed source lower bound.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, formula length L_N=(log N)^d, d>1, and generator size N^{rho+o(1)}.
- target object: LB_N(1+epsilon) is the statement C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)} in the same nonuniform Boolean circuit model used by the parser-to-circuit construction.
- controlled interface: TransparentRowSupport_N means visible selector code, advice-free RowSet enumeration or charged full scan, influence closure, same-theory occurrence expansion, and no hidden row-support advice for every FormulaEval line.
- target-preserving condition: beta=0 polylogarithmic SAT queries, fixed q,rho,eta,tau with q,rho below 1+epsilon, and every surfaced FormulaEval influence is included in Gamma_trans before the lower-bound certificate is used.
- source statement: pi is a Psys_bEF^- plus transparent FormulaEval certificate for LB_N(1+epsilon), with transcript cost Gamma_trans(pi) and residual row count E_pi.
- target statement: if N^{rho+o(1)}+Gamma_trans(pi)+E_pi N^{1+o(1)} is subthreshold, the asserted LB_N(1+epsilon) is refuted inside the same SIZE model.
- model context: nonuniform Boolean SIZE circuits, bit-explicit EF dependencies, SATeq links, bounded-SR_h rules, and FormulaEval support surfaced as occurrence rows.
- quantifier context: for all sufficiently large valid N, fixed epsilon>0 and fixed exponents q,rho,eta,tau; row enumerators are advice-free apart from N and the proof text pi.

## Assumptions

- Psys_bEF^- line induction is already valid for EF dependencies, SATeq semantic links, and bounded-SR_h with explicit bit fields and row-index encodings.
- Every transparent FormulaEval line ell has a finite RowSet_ell that contains all rows whose SAT value can affect ell under the same-theory proof semantics.
- U_pi charges selector enumeration, prefix/search overhead, or the declared full scan; X_pi charges occurrence expansion at N^{1+o(1)} per surfaced row.
- Nonuniform circuits may hardwire N and the accepted proof text pi, but may not hardwire uncharged private SAT labels or hidden support advice.
- Barrier status: the positive theorem is relativizing over surfaced row labels; the only nonrelativizing issue is the separate RealSATInfluenceRealizer_N escape for hidden real-SAT semantic influence.

## Equations

- GammaTrans: `\Gamma_{\mathrm{trans}}(\pi)=B_{\mathrm{EF}}(\pi)+B_{\mathrm{eq}}(\pi)+B_{\mathrm{SR}}(\pi)+U_{\pi}+X_{\pi}`. Valid when: Valid when the proof system line types are bit-explicit or satisfy TransparentRowSupport_N with all FormulaEval support charges surfaced.
- FormulaEvalExpansion: `X_{\pi}=\sum_{\ell\in FE(\pi)} N^{1+o(1)}\,|RowSet_{\ell}|`. Valid when: Applies after every FormulaEval selector has an advice-free RowSet enumeration or the full-scan alternative is charged.
- ParsedCircuitUpperBound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{\mathrm{trans}}(\pi)+O(E_{\pi}N^{1+o(1)})`. Valid when: Requires the target-preserving beta-zero generator, same-theory expansion, and equality patching of only E_pi residual source rows.
- SoundCertificatePressure: `\Gamma_{\mathrm{trans}}(\pi)+E_{\pi}N^{1+o(1)}\ge N^{1+\epsilon-o(1)}`. Valid when: Valid for sound certificates of LB_N(1+epsilon) once the previous circuit upper bound is accepted in the same SIZE model.
- SupportDensityCorollary: `|K_{idx}(\pi)|\ge N^{\epsilon-o(1)},\quad |K_{idx}(\pi)|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Applies when generator, EF, equality, and bounded-SR charges are subthreshold and FormulaEval row support is the remaining pressure term.

## Attempted Derivation

- Fix a valid length N, beta-zero carrier H_N^SAT, M_N=N^{q+o(1)}, generator G_N of size N^{rho+o(1)}, and a Psys_bEF^- plus FormulaEval proof pi claiming LB_N(1+epsilon).
- Maintain the line-induction invariant I_t: after t lines, every row label that can affect the parsed proof state is either in the charged support K_t or counted as a residual row; the accumulated cost is B_EF+B_eq+B_SR+U+X.
- For EF, SATeq, and bounded-SR_h lines, use the existing bit-explicit parser: parent pointers, row-index encodings, touched occurrence neighborhoods, and eta/tau leaf costs update Gamma_bEF without hidden semantic advice.
- For a transparent FormulaEval line ell, run the visible selector or full scan, charge U_ell, expand each row in RowSet_ell into same-theory occurrence support, charge X_ell=N^{1+o(1)}|RowSet_ell|, and update K_t by influence closure.
- At the final line, hardwire pi and the charged transcript into a nonuniform circuit: compute G_N, evaluate all charged local transcript components, and equality-patch E_pi residual source rows at cost O(E_pi N^{1+o(1)}).
- This gives C(H_N^SAT)<=N^{rho+o(1)}+Gamma_trans(pi)+O(E_pi N^{1+o(1)}); contraposition yields the support-pressure and q-density corollaries for any sound LB_N certificate.
- For hidden semantic FormulaEval, choose an influential uncharged row r*, construct two row-label worlds or an unread-enable-bit pair agreeing on K_vis(pi) and all visible proof checks, but differing on the parity of H_N at one source input. Thus the occurrence parser is falsified unless real SAT semantics is converted into charged support by RealSATInfluenceRealizer_N.

Blocking gap: The positive theorem is complete for TransparentRowSupport_N, but full semantic FormulaEval remains blocked at RealSATInfluenceRealizer_N: no advice-free nonrelativizing procedure is known that surfaces all real-SAT influences with subthreshold cost.

## Falsifiers

- private-row falsifier: an uncharged influential row makes two visible transcripts agree while H_N parity differs
- unread-enable-bit falsifier: a FormulaEval selector can hide whether a row is active unless the enable bit is visible and charged
- threshold falsifier: N^{rho+o(1)}+Gamma_trans(pi)+E_pi N^{1+o(1)}<N^{1+epsilon-o(1)} refutes LB_N(1+epsilon) in the same SIZE model
- q<epsilon density falsifier: required support density exceeds one when FormulaEval is the only remaining pressure term
- semantic-advice falsifier: RealSATInfluenceRealizer_N is invalid if it smuggles nonuniform row labels into RowSet output

## Learning

Cycle 114 upgrades the promoted theorem pair into an auditable live inference packet: transparent FormulaEval is exactly charged support realization, hidden semantic FormulaEval has a two-world falsifier, and the full-system question is the named nonrelativizing RealSATInfluenceRealizer_N rather than generic barrier folklore.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The branch already has the abstract transparent theorem; the remaining risk is a hidden semantic FormulaEval line that appears to certify support without paying U_N+X_N. A concrete two-world test checks exactly whether the theorem pair is target-preserving.
- Situation seed: Take H_N^SAT(x)=xor_{j<=N^q} SAT(G_N(x,j)) with L_N=(log N)^d, d>1, and insert one symbolic FormulaEval line Eval(j,e_j) whose real influence includes row j* only when an enable bit e_{j*} is semantically true but not exposed in RowSet.
- Varied variable: visibility exponent kappa, where |K_vis|=N^{kappa+o(1)} surfaced influential rows while the actual enabled influence set contains N^{epsilon+o(1)} rows.
- Held-fixed controls: beta=0 polylogarithmic SAT query length and generator overhead N^{rho+o(1)} with rho<1+epsilon, same Psys_bEF^- bit-explicit parser, bounded-SR_h eta/tau costs, and same-theory SATeq links, nonuniform SIZE target model and equality-patching cost O(N) per residual source row, no change to the carrier parity definition or to the valid length set
- Expected observation: If kappa<epsilon, the private-row/unread-enable-bit pair leaves the proof transcript unchanged and yields a subthreshold circuit falsifier. If kappa>=epsilon, the Gamma_trans support term reaches the support-pressure threshold, so the certificate is no longer a weak magnification source.
- Transfer certificate needed: A valid RealSATInfluenceRealizer_N or TransparentRowSupport_N certificate proving that every semantically enabled row is surfaced by an advice-free RowSet enumerator and charged through U_N+X_N before the parser-to-circuit implication is used.

## Next Experiment

Instantiate RealSATInfluenceRealizer_N for one concrete full semantic FormulaEval rule, or prove a rule-specific private-row countermodel showing that the full Psys_sym extension must remain quarantined.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

In Psys_sym^TRS, any sound accepted proof pi of LB_N(1+epsilon) for H_N^SAT with generator exponent rho<1+epsilon forces normalized row-equivalent support \widehat S_eff(pi)>=N^{epsilon-o(1)}. If nonrow debt is subthreshold, then visible FormulaEval row support has density at least N^{epsilon-q-o(1)} inside M_N=N^{q+o(1)} rows.

## Definitions

- source object: beta-zero SAT-parity carrier H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), with N=2^n, M_N=N^{q+o(1)}, generator circuit size N^{rho+o(1)}, and source statement LB_N(1+epsilon): C(H_N^SAT)>N^{1+epsilon-o(1)} in nonuniform Boolean SIZE.
- target object: a transparent proof transcript pi in Psys_sym^TRS containing bit-explicit bEF lines and FormulaEval lines, parsed into a same-theory circuit upper-bound falsifier for the same H_N^SAT.
- controlled interface: TransparentRowSupport_N, requiring visible selector code, advice-free RowSet enumeration or full-scan charge, influence closure, row expansion as ordinary proof syntax, and no hidden semantic row advice.
- target-preserving condition: the parser uses only pi and G_N, preserves N, M_N, q, rho, epsilon, the no-advice uniform extractor, and the target class nonuniform SIZE without replacing H_N^SAT by an easier promise object.
- K_idx^+(pi) is the visible index-expanded row set touched by FormulaEval after selector extensionality and influence closure.
- E_N^*(pi) is the number of full-row FormulaEval expansions charged instead of explicit enumeration.
- U_N(pi) is the total bit work of proof-visible RowSet enumeration, including scan or selector traversal costs.
- Gamma_bEF(pi) is the already-derived bit-explicit bEF transcript charge from the row-faithful core.

## Assumptions

- Model: Psys_sym^TRS consists of EF+SATeq+bounded-SR_h plus FormulaEval rules satisfying TransparentRowSupport_N.
- Length regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, h=N^{eta+o(1)}, all o(1) terms are along the same slice sequence.
- Uniformity/advice regime: the parser and RowSetEnumerator are deterministic and advice-free; selector descriptions are proof-visible bits, not semantic side information.
- Same-theory regime: every charged row expansion is representable inside the proof language used by the bEF line induction.
- Target regime: circuit upper bounds and lower-bound claims are both measured in the same nonuniform Boolean SIZE model on the same truth-table length N.
- Exponent regime: rho<1+epsilon is required; otherwise the generator alone can mask the support threshold and the lemma is not a valid falsifier.

## Equations

- carrier_definition: `H_N^{SAT}(x)=\bigoplus_{j<M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)}`. Valid when: Valid when the source carrier is the beta-zero SAT-parity family with fixed row count exponent q.
- transparent_charge: `\Gamma_{trans}(\pi)=\Gamma_{bEF}(\pi)+U_N(\pi)+N\bigl(|K_{idx}^+(\pi)|+E_N^*(\pi)\bigr)`. Valid when: Valid when every FormulaEval influence is either visibly enumerated or charged by a full-row expansion.
- normalized_support: `\widehat S_{eff}(\pi)=\left\lceil\Gamma_{bEF}(\pi)/N\right\rceil+\left\lceil U_N(\pi)/N\right\rceil+|K_{idx}^+(\pi)|+E_N^*(\pi)`. Valid when: Valid when bit costs are normalized into row-equivalent units after the bEF line induction.
- parser_upper_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+O(\Gamma_{trans}(\pi)\,polylog N)\le N^{\rho+o(1)}+N^{1+o(1)}\widehat S_{eff}(\pi)`. Valid when: Applies after the transparent parser synthesizes a same-SIZE circuit from the generator and charged transcript.
- forced_support: `LB_N(1+\epsilon)\wedge \rho<1+\epsilon\Rightarrow \widehat S_{eff}(\pi)\ge N^{\epsilon-o(1)}`. Valid when: Requires the lower-bound claim and parser upper bound to refer to the same carrier and circuit model.
- debt_or_density: `D_{nonrow}<N^{\epsilon-o(1)}\Rightarrow |K_{idx}^+(\pi)|+E_N^*(\pi)\ge N^{\epsilon-o(1)},\quad (|K_{idx}^+|+E_N^*)/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Valid when D_nonrow denotes the normalized bEF plus enumeration debt and M_N has exponent q.

## Attempted Derivation

- Fix N=2^n, M_N=N^{q+o(1)}, H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), and an accepted Psys_sym^TRS proof pi of LB_N(1+epsilon).
- Apply the bit-explicit bEF line induction to all non-FormulaEval lines, obtaining Gamma_bEF(pi) and preserving the same Boolean SIZE target model.
- For each FormulaEval line, use TransparentRowSupport_N: visible enumeration contributes U_N, and full row expansion or influence closure contributes N(|K_idx^+|+E_N^*). This yields Gamma_trans=Gamma_bEF+U_N+N(|K_idx^+|+E_N^*).
- Synthesize the standard transcript circuit: hardwire the generator circuit of size N^{rho+o(1)}, add the charged transcript gadgets, and obtain C(H_N^SAT)<=N^{rho+o(1)}+O(Gamma_trans polylog N).
- Contrapose the source lower-bound claim. If rho<1+epsilon and widehat S_eff<N^{epsilon-o(1)}, then the synthesized circuit has size below N^{1+epsilon-o(1)}, contradicting LB_N(1+epsilon). Therefore any sound accepted TRS proof forces widehat S_eff>=N^{epsilon-o(1)}.
- Separate widehat S_eff into nonrow debt D_nonrow=ceil(Gamma_bEF/N)+ceil(U_N/N) and visible row mass R=|K_idx^+|+E_N^*. If D_nonrow is subthreshold, then R>=N^{epsilon-o(1)} and R/M_N>=N^{epsilon-q-o(1)}.
- live_packet: source_statement=short accepted Psys_sym^TRS proof of LB_N(1+epsilon) for H_N^SAT; target_statement=normalized transcript circuit upper-bound falsifier or forced row-equivalent support; model_context=nonuniform Boolean SIZE, beta-zero SAT-parity carrier, EF+SATeq+bounded-SR_h plus TRS FormulaEval, simulation/extraction not many-one reduction; quantifier_context=N=2^n, M_N=N^{q+o(1)}, rho<1+epsilon, |pi|=N^{tau+o(1)}, h=N^{eta+o(1)}, no parser advice; derivation_status=restricted theorem derived, full semantic FormulaEval blocked at RealSATInfluenceRealizer_N; reviewer_findings=valid for TRS, invalid for hidden semantic support by private-row falsifier, no claim toward P != NP.

Blocking gap: RealSATInfluenceRealizer_N remains unproved for unrestricted semantic FormulaEval-SAT; without it, hidden row dependence is not charged and the TRS theorem cannot be lifted.

## Falsifiers

- private-row FormulaEval: one hidden row b changes SAT(G_N(x,b)) while the visible transcript and charged support remain unchanged
- unread-enable-bit FormulaEval: a dormant selector bit is semantically read by RealSAT but absent from RowSetEnumerator_N
- bEF-heavy undercharge: if Gamma_bEF is omitted from widehat S_eff, a proof with no FormulaEval rows evades the previous support theorem
- q<epsilon global ceiling: C(H_N^SAT)<=N^{1+q+o(1)} falsifies any claimed N^{1+epsilon} source lower bound unless nonrow debt or generator assumptions are retyped
- semantic advice leakage: a selector table supplied outside pi makes enumeration appear small while hiding N^{epsilon} row choices

## Learning

Cycle 114 upgrades the normalized TRS theorem into a debt-or-density packet. A valid transparent FormulaEval proof of LB_N(1+epsilon) must pay N^{epsilon-o(1)} row-equivalent support once rho<1+epsilon; if bEF and enumeration debt are small, visible FormulaEval rows have density N^{epsilon-q-o(1)}. Hidden semantic FormulaEval remains quarantined by the private-row falsifier until RealSATInfluenceRealizer_N is proved. This is route-level proof-system certification, not progress on P != NP itself.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for RealSATInfluenceRealizer_N and as a validation test for the TRS clauses.`
- Rationale: The branch no longer needs another selector example; it needs a concrete way to decide whether semantic FormulaEval dependence is recoverable or hidden. The private-row experiment directly tests target preservation of the parser theorem.
- Situation seed: Construct H_N^SAT with M_N=N^q rows and a FormulaEval atom A_e that evaluates a visible selector S plus one enabled private row b when an unread bit e_b=1. Two generators G and G' agree on every visible selected row but differ on SAT(G(x,b)).
- Varied variable: selector visibility v in {0,1}, where v=1 exposes b in RowSetEnumerator_N and v=0 hides b behind semantic FormulaEval.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, rho<1+epsilon, and the same SAT-parity carrier H_N^SAT, the same displayed proof surface pi, FormulaEval atom syntax, and nonuniform SIZE target model, no parser advice and the same bEF core charge Gamma_bEF, same-theory row expansion for every row that is visible
- Expected observation: For v=1 the row b is charged in K_idx^+ or E_N^*, so Gamma_trans increases by N and the TRS theorem remains valid. For v=0 the two completions have identical charged transcripts but different hidden FormulaEval truth, giving a finite countermodel to surface occurrence completion.
- Transfer certificate needed: A valid RealSATInfluenceRealizer_N must uniformly recover b or prove it irrelevant from proof-visible syntax with no advice; otherwise the intuition is only a countermodel and cannot support the full parser theorem.

## Next Experiment

Write the referee-style proof of Lemma L1 with all ceilings removed into O(N^{o(1)}) slack, then instantiate the private-row countermodel for one concrete semantic FormulaEval rule A_e and verify that the two transcripts are bit-identical while H_N^SAT differs.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

TransparentRowSupport_N is a sufficient and nearly necessary interface for FormulaEval in the parser theorem: every influence-closed transparent FormulaEval line contributes exactly its row-discovery charge plus row-expansion charge to Gamma_trans, while any uncharged influential row gives a private-row/unread-enable-bit falsifier for the occurrence parser.

## Definitions

- source object: a bit-explicit Psys_sym proof pi over H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)}, and FormulaEval lines that may select SAT rows.
- target object: a same-length nonuniform SIZE upper bound for H_N^SAT used to refute a claimed LB_N(1+epsilon) lower-bound proof when the transcript is subthreshold.
- controlled interface: TransparentRowSupport_N consists of visible selector code, advice-free RowSet enumeration or declared full-scan charge, influence closure, same-theory occurrence expansion, and no hidden semantic support advice.
- target-preserving condition: the parser expansion must keep the same SAT generator G_N, same N-length target language, same nonuniform circuit model, and same exponent regime rho,q,epsilon up to o(1).
- K_idx(pi) is the set of SAT-query indices whose values can influence the target parity or a FormulaEval line after quotienting witnessed formula identities.
- U_N is the total visible support discovery cost: sum of certified enumerator costs, RealSATInfluenceRealizer witnesses, or full-scan charges for non-output-sensitive lines.
- X_N is the total same-theory occurrence expansion cost for the SAT rows exposed by TransparentRowSupport_N.
- Gamma_bEF(pi) is the prior bit-explicit bounded-EF parser ledger from the restricted Psys_bEF^- line induction.

## Assumptions

- Circuit model is nonuniform Boolean SIZE on N-bit inputs; the result is not a uniform language lower bound by itself.
- Length regime has N tending to infinity, M_N=N^{q+o(1)}, formula length polylog(N), and fixed epsilon>0.
- Psys_bEF^- rules already satisfy Gap98-SRhNormalForm with eta/tau overhead charged in Gamma_bEF(pi).
- Every transparent FormulaEval line has a syntactic selector object whose RowSet can be enumerated advice-free in cost U_L, or else the line pays the full scan N^{1+q+o(1)} charge.
- Influence closure is required: if changing a SAT row can change the FormulaEval value in the ambient theory, that row is visible, realized, and charged.
- Same-theory expansion is required: rows are expanded into occurrence-level SAT queries rather than imported as semantic oracle answers.
- No hidden selector advice, nonuniform hard-row choice, or unparsed SAT extensionality is allowed in the positive theorem.
- The theorem is a route-level parser obstruction and valid falsifier, not a proof of P != NP.

## Equations

- transparent_ledger: `\Gamma_{trans}(\pi)=\Gamma_{bEF}(\pi)+U_N+X_N+N^{o(1)}`. Valid when: Valid when every FormulaEval line satisfies TransparentRowSupport_N and all bit-explicit base rules have already been parsed into Gamma_bEF.
- row_expansion_floor: `X_N \ge N^{1+o(1)}\,|K_{idx}(\pi)|`. Valid when: Applies when each influential SAT-query index must be expanded across the N target inputs inside the same occurrence-level theory.
- parser_upper_bound: `C(H_N^{SAT}) \le N^{\rho+o(1)}+\Gamma_{trans}(\pi)`. Valid when: Requires the target-preserving simulation that combines the generator circuit with the parsed proof transcript in the same nonuniform SIZE model.
- subthreshold_falsifier: `N^{\rho+o(1)}+\Gamma_{trans}(\pi)<N^{1+\epsilon-o(1)} \Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Valid when LB_N(1+epsilon) asserts a SIZE lower bound for the identical H_N^SAT family and no model switch or advice leakage occurs.
- density_corollary: `|K_{idx}(\pi)|/M_N \ge N^{\epsilon-q-o(1)} \Rightarrow X_N\ge N^{1+\epsilon-o(1)}`. Valid when: Applies after M_N=N^{q+o(1)} is fixed and influential indices are charged by full same-theory row expansion.

## Attempted Derivation

- Fix N, H_N^SAT, M_N=N^{q+o(1)}, and a Psys_sym proof pi claiming LB_N(1+epsilon) in the same nonuniform SIZE model.
- Normalize all Psys_bEF^- lines by Gap98-SRhNormalForm and assign their verified contribution to Gamma_bEF(pi).
- For each FormulaEval line L, inspect the visible selector code. If RowSet_L is certified output-sensitive, add its enumeration cost to U_N; if not, require the declared full-scan charge N^{1+q+o(1)} or mark L nontransparent.
- Check influence closure for L. Every row whose SAT value can change L must either lie in RowSet_L or be supplied by RealSATInfluenceRealizer_N; otherwise invoke the private-row falsifier.
- Expand each charged row into occurrence-level SAT formula bits in the same theory and add the expansion to X_N. This preserves target identity because it does not replace SAT by an oracle truth predicate.
- Induct on proof lines: base and bounded-EF rules are simulated by Gamma_bEF; transparent FormulaEval lines are simulated by their U_L+X_L expansion; witnessed formula identities only quotient already charged occurrences.
- Combine the parsed transcript with the generator circuit of size N^{rho+o(1)} to obtain C(H_N^SAT)<=N^{rho+o(1)}+Gamma_trans(pi).
- If the right side is below N^{1+epsilon-o(1)}, the proof transcript is a valid upper-bound falsifier for LB_N(1+epsilon), not a lower-bound breakthrough.
- For the negative branch, choose the first nontransparent FormulaEval line with uncharged influence r. Construct two completions A0,A1 agreeing on every parser-visible bit and charged row but flipping the unread enable/private row so that L differs. The parser cannot be sound on both.

Blocking gap: Promotion to full Psys_sym is blocked exactly at RealSATInfluenceRealizer_N for unwitnessed SAT extensionality; the restricted transparent theorem and hidden-support countermodel are otherwise theorem-shaped.

## Falsifiers

- private-row falsifier: an uncharged influential SAT row changes FormulaEval while every parsed occurrence bit remains fixed
- unread-enable-bit falsifier: selector membership is controlled by a bit outside the visible support code
- nonuniform selector falsifier: the proof chooses hard or influential rows by advice rather than by an advice-free enumerator
- full-scan threshold falsifier: a membership-only selector without output-sensitive enumeration must pay N^{1+q+o(1)} and cannot remain subthreshold
- semantic-oracle falsifier: unwitnessed SAT extensionality supplies truth information without same-theory occurrence expansion

## Learning

Cycle 114 closes a proof-delivery gap by making TransparentRowSupport_N a two-sided theorem interface: influence-closed transparent FormulaEval lines have a derivable Gamma_trans ledger, and the first uncharged semantic influence gives a finite private-row falsifier. The remaining full-system issue is RealSATInfluenceRealizer_N, not another selector class, MCSP slogan, or P != NP claim.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the hidden-support theorem.`
- Rationale: The top theorem pair needs a concrete finite countermodel showing that hidden FormulaEval support is not merely an accounting omission but invalidates the occurrence parser.
- Situation seed: Fix H_N^SAT with M_N=N^{q+o(1)} and a FormulaEval line L whose visible selector lists all rows except one private row r=(x*,j*) controlled by an unread enable bit e; L outputs the xor of listed SAT values plus e*SAT(G_N(x*,j*)).
- Varied variable: Number h_N of uncharged influential private rows, starting with h_N=1 and then increasing to N^{alpha}.
- Held-fixed controls: Same generator G_N, same target H_N^SAT, same nonuniform SIZE model, same exponent parameters q,rho,epsilon., Same parsed Psys_bEF^- transcript and same charged RowSet enumeration for all nonprivate rows., No advice and no RealSATInfluenceRealizer_N witness for the private row., Formula lengths remain polylog(N), so any change is in support visibility rather than formula size.
- Expected observation: For h_N>=1 there are two same-transcript completions differing only on a private enable/SAT bit but changing L; for h_N=N^{alpha}, a valid transparent repair must charge at least N^{1+alpha-o(1)} row expansion or declare a semantic-oracle escape.
- Transfer certificate needed: Before this intuition affects proof obligations, prove the finite completion lemma: occurrence-local proof checking cannot distinguish A0,A1, while the FormulaEval semantic value differs; alternatively provide an advice-free RealSATInfluenceRealizer_N certificate listing r and paying U_N+X_N.

## Next Experiment

Write the paper-ready finite completion lemma: specify the bit fields read by a FormulaEval line, define A0/A1 completions for one private row r=(x*,j*), prove transcript equality and FormulaEval disagreement, then plug it into the Gamma_trans line induction.
