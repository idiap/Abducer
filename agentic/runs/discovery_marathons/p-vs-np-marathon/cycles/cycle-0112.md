# cycle-0112

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For beta-zero parity carrier H_N^SAT and a Psys_sym proof pi whose FormulaEval uses satisfy TransparentRowSupport_N, every proof line has a materialized occurrence transcript, and a claimed LB_N(1+epsilon) is falsified whenever N^{rho+o(1)}+Gamma_bEF(pi)+U_N(pi)+X_N(pi)+E_N N<N^{1+epsilon-o(1)}. This is a valid restricted parser/falsifier theorem, not a proof of P != NP.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, |G_N(x,j)|=(log N)^{d+O(1)}, generator size N^{rho+o(1)}, and LB_N(1+epsilon) meaning C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)}.
- target object: a same-model nonuniform SIZE circuit upper bound for H_N^SAT extracted from a Psys_sym transcript, used only to refute subthreshold lower-bound certificates for the source carrier.
- controlled interface: TransparentRowSupport_N, consisting of visible selector code, advice-free RowSet enumeration or charged full scan, influence closure, same-theory occurrence expansion, bounded SR_h parsing, and no hidden support advice.
- target-preserving condition: beta=0 polylog SAT-query length, q,rho<1+epsilon, all proof encodings are bit-explicit or charged, and FormulaEval influence is surfaced in the same proof theory before being used by the parser.
- Gamma_bEF(pi) is the sum of bit-explicit EF dependency charges, SATeq semantic-link charges, bounded-SR_h charges B_SR(pi), and sparse-row residual correction charges inherited from the Psys_bEF^- parser.
- U_N(pi) is the total cost of advice-free row enumeration for transparent FormulaEval lines; if no output-sensitive enumerator is certified, U_N includes the full syntactic scan charge.
- X_N(pi) is the row occurrence-expansion charge for all enumerated FormulaEval supports after influence closure; for global support it is N|RowSet| up to polylog factors.
- E_N is the number of residual source rows patched by equality gadgets; sparse residual patching is valid only below the N^epsilon threshold.

## Assumptions

- Circuit model is nonuniform Boolean SIZE with polynomially bounded advice only as ordinary circuit description; no semantic advice may choose hidden rows.
- Length regime is N->infinity, M_N=N^{q+o(1)}, query length L_N=(log N)^{d+O(1)}, and all o(1) losses are uniform over fixed epsilon,q,rho,d.
- Proof model is restricted Psys_sym^trans: Psys_bEF^- plus FormulaEval lines satisfying the finite TransparentRowSupport_N checklist.
- Same-theory condition: each expanded FormulaEval occurrence is expressed as a line, axiom instance, or extension rule of the same syntactic proof system, not as an external SAT oracle.
- Uniformity condition: RowSet enumerators and visible selectors have O(polylog N) or charged descriptions and can be verified by the parser without consulting SAT labels.
- Advice status: hidden row indices, private enable bits, and semantic selector tables are forbidden unless their full description is included in U_N or X_N.
- Barrier status: the positive theorem is relativizing over surfaced occurrence labels; it deliberately excludes nonrelativizing real-SAT influence unless RealSATInfluenceRealizer_N is proved.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j=1}^{M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad |G_N(x,j)|=(\log N)^{d+O(1)}.`. Valid when: Valid when the source carrier is the beta-zero batched SAT parity object with polylogarithmic generated formulas.
- transparent_charge: `\Gamma_{trans}(\pi)=\Gamma_{bEF}(\pi)+U_N(\pi)+X_N(\pi).`. Valid when: Valid when every FormulaEval line satisfies TransparentRowSupport_N and all influence rows are enumerated or full-scan charged.
- parser_upper_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{trans}(\pi)+O(E_NN\operatorname{polylog}N).`. Valid when: Applies after the parser line induction materializes a same-theory transcript and residual row errors are equality-patched.
- falsifier_threshold: `N^{\rho+o(1)}+\Gamma_{trans}(\pi)+E_NN<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon).`. Valid when: Requires the source lower-bound claim and the extracted circuit to be measured in the same nonuniform SIZE model.
- support_density_corollary: `|K_{idx}(\pi)|\ge N^{\epsilon-o(1)},\qquad |K_{idx}(\pi)|/M_N\ge N^{\epsilon-q-o(1)}.`. Valid when: Valid when each unforced row can be patched at cost O(N polylog N) and q is fixed in M_N=N^{q+o(1)}.

## Attempted Derivation

- Define Psys_sym^trans as Psys_bEF^- plus FormulaEval rules carrying visible selector code, RowSet enumerator or full-scan declaration, influence-closure proof, and same-theory occurrence expansion template.
- Induct on proof lines. Bit-explicit EF lines extend the transcript by their declared support and are charged inside Gamma_bEF(pi).
- For bounded SR_h lines, use the existing SR_h bit-normal form: parent pointers, row-index fields, touched occurrence-neighborhood list, and eta/tau overhead contribute B_SR(pi) inside Gamma_bEF(pi).
- For a transparent FormulaEval line a, run the certified RowSet enumerator. If output-sensitive enumeration is not certified, charge the full syntactic scan. Add this to U_N(pi).
- Expand each row in the influence closure of a into same-theory occurrence clauses and charge the total row expansion to X_N(pi). This prevents semantic FormulaEval from acting as a free SAT oracle.
- The final transcript gives a circuit for H_N^SAT by wiring the generator G_N of size N^{rho+o(1)}, the parsed local decisions from Gamma_trans(pi), and equality patches for E_N residual rows.
- If the resulting size is below N^{1+epsilon-o(1)}, it contradicts the source lower-bound statement LB_N(1+epsilon); hence such a proof pi is a valid falsifier for the claimed lower bound, not evidence for P != NP.
- For hidden FormulaEval, construct two label structures that agree on every charged visible row but differ on an uncharged influencing row or unread enable bit. The same transcript then supports different carrier values, so occurrence completion is invalid.

Blocking gap: No blocking gap remains for Psys_sym^trans as defined. The extension to full semantic Psys_sym is blocked exactly at RealSATInfluenceRealizer_N, which must convert real-SAT semantic influence into charged same-theory row support.

## Falsifiers

- private-row falsifier: an uncharged generated row changes the carrier while the visible transcript is unchanged
- unread-enable-bit falsifier: a semantic FormulaEval gate has an unparsed enable bit that toggles influence without appearing in RowSet
- threshold falsifier: N^{rho+o(1)}+Gamma_trans(pi)+E_NN<N^{1+epsilon-o(1)} gives a same-model circuit refuting LB_N(1+epsilon)
- nonuniform leakage falsifier: RowSet enumeration depends on hidden advice not counted in U_N or X_N
- same-theory failure falsifier: FormulaEval expansion uses an external SAT oracle rather than proof-system lines
- positive-beta background falsifier: any black-box target substitution with exponent beta>0 still obeys q+beta c and cannot exclude all SAT exponents

## Learning

Cycle 112 turns the transparent FormulaEval packet into a finite theorem pair: transparency is exactly a charged support-realization condition, and hidden semantic support is not merely difficult but has a two-world private-row falsifier. The contribution remains a route-level parser/falsifier boundary for beta-zero magnification; the main P vs NP conjecture is untouched.

## Gedanken Experiment Design Seed

- Need decision: `use now as a falsifier probe`
- Rationale: The theorem pair hinges on whether semantic FormulaEval influence is surfaced and charged; a concrete private-row experiment tests the exact support-visibility clause rather than restating barrier folklore.
- Situation seed: Take H_N^SAT(x)=xor_{j<=N^q} SAT(G_N(x,j)) with polylog formula length and insert one FormulaEval-SAT line whose conclusion depends on row r through an enable bit e_r that is not read by the declared RowSet enumerator.
- Varied variable: h, the number of hidden enabled influence rows left outside the charged RowSet closure, with the critical range h<N^{epsilon-o(1)} versus h>=N^{epsilon-o(1)}.
- Held-fixed controls: beta=0 polylog SAT-query regime and fixed q,rho<1+epsilon, same nonuniform SIZE model for source lower bound and extracted circuit upper bound, Psys_bEF^- bit-explicit parser and bounded SR_h normal form charges, no hidden advice except the deliberately varied unread enable rows
- Expected observation: For h<N^{epsilon-o(1)}, equality patching plus the visible transcript yields a subthreshold circuit; for h=1 with odd parity incidence, two transcripts agree visibly while H_N flips, proving the hidden FormulaEval parser invalid. If h is fully surfaced, the cost moves into U_N+X_N and the transparent theorem applies.
- Transfer certificate needed: A RealSATInfluenceRealizer_N certificate showing that every real semantic influence row and enable condition is advice-free enumerable, influence-closed, same-theory expandable, and charged before it can affect the proof.

## Next Experiment

Write the corollary table as examples only: interval-union, full scan, ROBDD, guarded-dDNNF, projected-dDNNF, and influence-complete extension rules must each be checked against the five TransparentRowSupport_N clauses or demoted.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

In the restricted proof system Psys_sym^TRS, any sound accepted proof pi of LB_N(1+epsilon) for H_N^SAT with generator exponent rho<1+epsilon must have effective transparent support S_eff(pi)>=N^{epsilon-o(1)}. If S_eff(pi)<N^{epsilon-delta}, the same visible transcript accepts a spoof carrier of circuit size <N^{1+epsilon}, giving a finite falsifier to the claimed transfer.

## Definitions

- source object: H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)) with N=2^n, M_N=N^{q+o(1)}, polylog SAT instances, and generator circuit size N^{rho+o(1)}.
- target object: the proof-system claim LB_N(1+epsilon), meaning nonuniform SIZE lower bound C(H_N^SAT)>N^{1+epsilon-o(1)} on the N-bit truth-table slice.
- controlled interface: TransparentRowSupport_N for FormulaEval lines, consisting of visible selector code, advice-free RowSet enumeration or full-scan charge, influence closure, same-theory occurrence expansion, and no hidden row advice.
- target-preserving condition: every row whose SAT value can affect any accepted FormulaEval line is either listed in K_idx^+(pi), paid through E_N^*, or paid through U_N/N, so transcript invariance under uncharged-row spoofs is valid.
- TRS bit fields are tag, parent-line pointers, selector-code pointer, row-index port, influence-port list, expansion-certificate pointer, and row-mass charge token.
- S_eff(pi)=|K_idx^+(pi)|+E_N^*(pi)+ceil(U_N(pi)/N) is the row-equivalent support after converting enumeration work into the number of N-bit rows it could have hardwired.

## Assumptions

- Model: nonuniform Boolean SIZE on N input bits; proof model is EF+SATeq+bounded-SR_h plus TRS FormulaEval rules, not unrestricted semantic RealSAT.
- Regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, h=N^{eta+o(1)}, all hidden constants independent of N, and rho<1+epsilon.
- Uniformity: the parser and RowSet enumerator are deterministic, advice-free, and read only proof-visible bit fields.
- Same-theory condition: FormulaEval expansion is performed inside the same syntactic SAT theory used by the bEF line induction; no external semantic oracle is queried.
- Soundness cutoff: pi is allowed to prove LB_N only if every same-transcript carrier satisfying the interpreted proof premises also has circuit complexity above N^{1+epsilon-o(1)}.
- Naturalness boundary: the lemma is a proof-system transfer obstruction; it is not a proof of P != NP and it triggers natural-proof pressure only if the transcript is converted into a large constructive useful truth-table property.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j<M_N} SAT(G_N(x,j)),\qquad M_N=N^{q+o(1)}`. Valid when: Valid when the beta-zero SAT-parity carrier and its row index set are fixed before parsing the proof.
- transparent_charge: `\Gamma_{trans}(\pi)=\Gamma_{bEF}(\pi)+U_N(\pi)+X_N(\pi)`. Valid when: Applies after every FormulaEval line satisfies TransparentRowSupport_N and bEF lines already have the bit-explicit Gamma_bEF induction.
- effective_support: `S_{eff}(\pi)=|K_{idx}^{+}(\pi)|+E_N^{*}(\pi)+\lceil U_N(\pi)/N\rceil`. Valid when: Valid when enumeration cost U_N is deterministic and can be normalized to N-bit row-hardwiring units.
- spoof_upper_bound: `C(H_N^{spoof})\le N^{\rho+o(1)}+O(N\,S_{eff}(\pi))`. Valid when: Requires transcript invariance under uncharged rows, visible influence closure, and hardwiring only the charged row truth tables.
- forced_support: `S_{eff}(\pi)\ge N^{\epsilon-o(1)}\quad\text{whenever }\rho<1+\epsilon\text{ and }\pi\text{ is sound}`. Valid when: Follows in the sound transparent proof regime where the spoof upper bound would otherwise violate LB_N(1+epsilon).
- density_pressure: `S_{eff}(\pi)/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Applies when M_N=N^{q+o(1)} and effective support, including enumeration debt, is compared with all SAT rows.

## Attempted Derivation

- Fix N=2^n, M_N=N^{q+o(1)}, generator G_N of circuit size N^{rho+o(1)}, and a Psys_sym^TRS proof pi of LB_N(1+epsilon).
- Run the bit-explicit bEF parser on non-FormulaEval lines, producing Gamma_bEF(pi) with parent pointers, row-index encodings, and bounded-SR_h occurrence neighborhoods.
- For each TRS FormulaEval line, read its selector-code field and influence-port list. If RowSet is enumerated, add the listed rows to K_idx^+ and charge the enumeration work to U_N. If full row expansion is used, charge E_N^* rows and X_N=N E_N^* occurrence bits.
- Use influence closure to prove line-by-line transcript invariance: changing uncharged rows cannot change any parsed premise, extension definition, SATeq step, bounded-SR_h rule, or FormulaEval output read by pi.
- Construct H_N^spoof by preserving all charged rows and replacing every uncharged row by an easy row, e.g. constant zero or a row produced by the small generator baseline. The visible transcript remains identical, so the checker accepts the same LB_N proof for H_N^spoof.
- Build a circuit for H_N^spoof by combining the generator-side fixed circuitry of size N^{rho+o(1)} with hardwired truth tables for O(S_eff(pi)) charged rows, giving C(H_N^spoof)<=N^{rho+o(1)}+O(N S_eff(pi)).
- If S_eff(pi)<N^{epsilon-delta} and rho<1+epsilon-delta, this circuit is smaller than N^{1+epsilon-o(1)}, contradicting soundness of an accepted proof of LB_N(1+epsilon). Therefore sound transparent proofs must satisfy S_eff(pi)>=N^{epsilon-o(1)}.

Blocking gap: The derivation is blocked for unrestricted Psys_sym only at RealSATInfluenceRealizer_N: semantic FormulaEval must expose every influential row with no advice and same-theory expansion. Without that realizer, the hidden private-row falsifier is valid.

## Falsifiers

- Private-row/unread-enable-bit falsifier: a semantic FormulaEval atom depends on row r* while the visible selector code omits r*, so occurrence parsing is invalid.
- Subthreshold support falsifier: S_eff(pi)<N^{epsilon-o(1)} gives a same-transcript spoof carrier with circuit size below N^{1+epsilon-o(1)}.
- Advice leakage falsifier: a selector uses nonuniform hidden advice to choose RowSet(a), defeating the deterministic no-advice enumeration needed for a valid charge.
- Extensionality falsifier: two equivalent selector descriptions have different charged supports, so the parser cannot assign a stable K_idx^+ invariant.
- Natural-proof falsifier: if the transcript is converted into a poly(N)-constructive dense property useful against SIZE(N^{1+epsilon}), then PRF tension applies unless the property is non-large, nonconstructive, or proof-system-specific.

## Learning

Cycle 112 converts the previous S_eff definition into a theorem-shaped forced-charge statement: in transparent FormulaEval systems, sound LB_N(1+epsilon) proofs must pay N^{epsilon-o(1)} row-equivalent support, where enumeration debt contributes U_N/N. This is valid route-level proof-system certification. The unrestricted semantic case remains blocked exactly at RealSATInfluenceRealizer_N, with the private-row/unread-enable-bit falsifier as the no-go object; there is no new claim toward P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for hidden support and as a threshold probe for the U_N/N effective-support normalization.`
- Rationale: The branch needs to decide whether enumeration-heavy transparent FormulaEval proofs really pay row-equivalent support, or whether semantic row choice leaks through without charge. This is more informative than restating a barrier because it tests the exact transfer certificate used by Gamma_trans.
- Situation seed: Take H_N^SAT(x)=xor_{j<M_N}SAT(G_N(x,j)) and a one-line FormulaEval selector a that visibly enumerates an interval R but whose semantic implementation also reads a private row r* through an unread enable bit. Compare a transparent version where r* is listed with a hidden version where it is not.
- Varied variable: Enumeration overhead exponent u defined by U_N=N^{1+u+o(1)}, while q, epsilon, rho, and the proof transcript size are held fixed.
- Held-fixed controls: N=2^n and M_N=N^{q+o(1)} for the same beta-zero SAT-parity carrier., Generator size exponent rho<1+epsilon and polylog SAT instance length., No nonuniform selector advice and the same visible proof transcript in both enable-bit settings., Same target claim LB_N(1+epsilon) in nonuniform Boolean SIZE.
- Expected observation: In the transparent version, listing or scanning r* increases S_eff by one row-equivalent unit or by U_N/N; the forced-charge inequality remains valid. In the hidden version, two transcripts agree while H changes, giving the private-row falsifier and showing that RealSATInfluenceRealizer_N is necessary.
- Transfer certificate needed: A formal RealSATInfluenceRealizer_N or TRS influence-closure proof that every row with nonzero FormulaEval influence is enumerated, expansion-charged, or full-scan charged before the spoofing intuition may enter proof obligations.

## Next Experiment

Run the proof audit for TRS112.EffectiveSupportForcedCharge: verify each rule case in the line induction, then test one semantic FormulaEval atom against RealSATInfluenceRealizer_N using the unread-enable-bit private row.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

TransparentRowSupport_N theorem packet: for H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)), any Psys_sym proof pi whose bEF core is bit-explicit and whose FormulaEval lines satisfy TransparentRowSupport_N has a same-model parser-to-circuit simulation. Thus a transcript with N^{rho+o(1)}+Gamma_trans(pi)<N^{1+epsilon-o(1)} is a valid falsifier for pi as a proof of LB_N(1+epsilon) in the nonuniform SIZE model.

## Definitions

- source object: Psys_sym FormulaEval transcript pi over the finite truth table H_N^{SAT}, with bEF core lines, FormulaEval lines, visible selector code, and charged row-support expansion.
- target object: a nonuniform SIZE upper bound for H_N^{SAT} at length N, used only to refute a too-cheap proof of LB_N(1+epsilon), not to prove P != NP.
- controlled interface: TransparentRowSupport_N, consisting of visible selector code, advice-free RowSet enumeration or full scan, influence closure, same-theory occurrence expansion, and no hidden support advice.
- target-preserving condition: all support discovery, row expansion, formula occurrence translation, and patch construction are uniform within the intended proof/circuit model and charged in Gamma_trans(pi).
- M_N=N^{q+o(1)} is the number of SAT queries per row; G_N has generator size N^{rho+o(1)} and outputs formulas in the fixed SAT encoding.
- K_l is the visible row set influencing FormulaEval line l; U_l is its row-discovery cost; X_l is its occurrence/SAT expansion cost; R_pi is residual sparse patch cost.

## Assumptions

- Length regime: N ranges over the padded SAT-parity lengths, M_N=N^{q+o(1)}, and all o(1) terms are uniform over the selected proof family.
- Circuit model: LB_N(1+epsilon) means C_SIZE(H_N^{SAT})>N^{1+epsilon-o(1)} for unrestricted nonuniform Boolean circuits on log N input bits.
- Proof model: the bEF fragment Psys_bEF^- has the previously certified bit-field parser and Gamma_bEF line induction; FormulaEval is the only added symbolic mechanism.
- Uniformity/advice: RowSetEnumerator_N, influence witnesses, and occurrence expansion are advice-free; hardwiring pi is allowed only for the negative upper-bound falsifier because pi is a fixed alleged proof.
- Same-theory condition: the parser expands SAT/formula facts into the same syntactic theory rather than importing an external semantic SAT oracle.
- Barrier status: the theorem is nonrelativizing only if RealSATInfluenceRealizer_N supplies real influence witnesses; otherwise hidden FormulaEval is classified as semantic-oracle escape, not as generic proof-system strength.

## Equations

- Gamma-trans-ledger: `Gamma_{trans}(pi)=Gamma_{bEF}(pi)+\sum_{l in FE(pi)}(U_l+X_l)+R_pi`. Valid when: Valid when pi is parsed by the bit-explicit bEF induction and every FormulaEval line satisfies TransparentRowSupport_N with charged enumeration and expansion.
- row-expansion-cost: `X_l=|K_l| M_N N^{o(1)}`. Valid when: Applies when K_l is the visible enumerated row set and each selected row expands to M_N SAT queries of polylogarithmic formula length.
- parser-upper-bound: `C_SIZE(H_N^{SAT}) <= N^{rho+o(1)}+Gamma_{trans}(pi)`. Valid when: Requires the target-preserving same-theory simulation where the generator circuit and charged transcript patches compute H_N^{SAT} in the nonuniform SIZE model.
- subthreshold-falsifier: `N^{rho+o(1)}+Gamma_{trans}(pi)<N^{1+epsilon-o(1)} => not Valid_{Psys_sym}(pi,LB_N(1+epsilon))`. Valid when: Valid when LB_N(1+epsilon) is interpreted in the same SIZE model and lower-order terms leave a polynomial exponent gap.
- support-density-corollary: `|K_idx(pi)|/N >= N^{epsilon-q-o(1)}`. Valid when: Applies after support costs below the threshold are discharged and K_idx(pi) is the union of all visible rows influencing the proof.

## Attempted Derivation

- Define the source statement for the live inference-quality packet: pi is a Psys_sym proof of LB_N(1+epsilon) for H_N^{SAT}, with bEF core plus FormulaEval lines satisfying or failing TransparentRowSupport_N.
- Define the target statement: either derive C_SIZE(H_N^{SAT})<=N^{rho+o(1)}+Gamma_trans(pi), yielding a subthreshold falsifier for pi, or construct two completions witnessing hidden semantic support.
- Base induction: the archived Psys_bEF^- parser supplies Gamma_bEF(pi) from bit fields, parent pointers, row-index encodings, and local rule verifiers.
- Transparent FormulaEval step: given visible selector code, RowSetEnumerator_N emits K_l at cost U_l or pays full scan; occurrence expansion of every selected row contributes X_l=|K_l|M_NN^{o(1)}.
- Influence-closure step: the parser records that changing any row outside K_l cannot affect the FormulaEval value used by line l; this is the exact clause that projected selectors and semantic DNNF must certify.
- Ledger step: summing bEF, FormulaEval row discovery, FormulaEval expansion, and residual sparse patches gives Gamma_trans(pi)=Gamma_bEF(pi)+sum_l(U_l+X_l)+R_pi.
- Simulation step: hardwire the fixed alleged proof pi and the charged transcript into a nonuniform circuit; combine with the generator of size N^{rho+o(1)} to compute H_N^{SAT} on all rows covered by the proof obligation.
- Falsifier step: if N^{rho+o(1)}+Gamma_trans(pi)<N^{1+epsilon-o(1)}, the same SIZE model contains a circuit below the asserted lower bound, so pi is not a valid proof of LB_N(1+epsilon).
- Countermodel step: if a semantic FormulaEval line has an uncharged row j*, build completions A and B that agree on every parser-read occurrence but toggle an unread enable bit or SAT-critical formula occurrence for j*, changing FE_l and hence the proof-relevant parity.
- Reviewer findings: reduction consistency is valid for same truth table and same SIZE model; quantifier uniformity is valid only under advice-free enumerators/realizers; barrier specificity isolates semantic SAT-oracle access, not natural-proofs folklore; proof-derivation status is scoped theorem plus open RealSATInfluenceRealizer_N.

Blocking gap: Full semantic proof systems remain blocked exactly at RealSATInfluenceRealizer_N: prove an advice-free influence-complete witness procedure with charged cost, or classify the rule as a semantic-oracle escape by the private-row falsifier.

## Falsifiers

- unread-enable-bit falsifier: a hidden selector bit toggles inclusion of one row while all charged parser fields remain unchanged
- private-row falsifier: one SAT-critical row outside K_idx(pi) flips H_N^{SAT} under two occurrence completions agreeing on the transcript
- subthreshold ledger falsifier: N^{rho+o(1)}+Gamma_trans(pi)<N^{1+epsilon-o(1)} contradicts the claimed LB_N(1+epsilon) in the same SIZE model
- q<epsilon density falsifier: visible support cannot reach |K_idx|/N>=N^{epsilon-q-o(1)} because the required fraction exceeds one
- semantic-oracle falsifier: FormulaEval uses SAT truth or formula identity without an advice-free influence witness and therefore leaves the controlled interface

## Learning

Cycle 112 upgrades the theorem pair by making influence closure the exact audit point. Transparent FormulaEval is valid precisely when every influential row is visible or realized and charged; otherwise a private-row/unread-enable-bit falsifier invalidates the parser. The q-trichotomy follows from a single support-density inequality. This is paper-level route progress only, not a P != NP proof.

## Gedanken Experiment Design Seed

- Need decision: `design-now-as-falsifier-probe`
- Rationale: The branch already has the abstract theorem pair; the remaining risk is an unnoticed semantic FormulaEval influence that evades the row-support ledger. A concrete private-row experiment tests the exact target-preserving boundary.
- Situation seed: Padded SAT-query family H_N^{SAT}(x)=xor_{j<=N^q} SAT(G_N(x,j)) with a Psys_sym FormulaEval line whose selector is visible except for one unread enable bit e_{x*,j*} controlling a private SAT instance on row x*.
- Varied variable: visibility exponent u, where U_N=N^{u+o(1)} is the cost needed to enumerate or realize all influential rows; u ranges from output-sensitive visible support to hidden semantic support.
- Held-fixed controls: M_N=N^{q+o(1)} and generator size N^{rho+o(1)} remain fixed, LB_N(1+epsilon) is interpreted in the same nonuniform SIZE model throughout, the bEF core parser and row-index encoding are held bit-explicit, no advice or nonuniform row selector is allowed except hardwiring the fixed alleged proof for the negative upper-bound simulation
- Expected observation: For u+q below 1+epsilon, the transparent ledger yields a subthreshold circuit falsifier; when the private enable bit is not in the charged support, two occurrence completions agree on the proof transcript but differ on FormulaEval, showing the parser is invalid.
- Transfer certificate needed: A valid RealSATInfluenceRealizer_N certificate: an advice-free, same-theory procedure emitting an influence-complete charged support set, with total U_N+X_N included in Gamma_trans(pi), before the semantic intuition may affect proof obligations.

## Next Experiment

Write the paper-ready theorem pair: formal TransparentRowSupport_N clauses, line-induction proof of Gamma_trans, private-row countermodel proof, q-density corollary table, and a live inference-quality packet with RealSATInfluenceRealizer_N as the named unresolved lemma.
