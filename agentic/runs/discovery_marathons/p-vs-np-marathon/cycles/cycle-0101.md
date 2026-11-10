# cycle-0101

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For Psys_bEF^- with bit-explicit EF, SATeq links, and one bounded-SR_h rule with syntactic RowSet, every accepted proof pi of LB_N(1+epsilon) parses to an occurrence transcript Q_pi with SR charge B_SR(pi). If N^{rho+o(1)}+Gamma_bEF(pi)<N^{1+epsilon-o(1)}, LB_N is falsified. Restricted route theorem only.

## Definitions

- source object: Psys_bEF^- proof pi for LB_N(1+epsilon) about H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), M_N=N^{q+o(1)}, L=(log N)^d, bit-explicit formula encodings, no symbolic FormulaEval oracle.
- target object: charged occurrence transcript Q_pi and circuit upper bound for H_N; target class is nonuniform SIZE(N^{1+epsilon-o(1)}) as a falsifier of the source lower-bound sentence, not a claimed NP lower bound.
- controlled interface: line parser reads EF dependency bits, SATeq link bits, and SR_h rule fields (tag,row j,node u,branch b,occurrence offset p,parent pointers) and emits touched occurrence-neighborhoods plus row indices.
- target-preserving condition: beta=0 polylog SAT queries, generator size N^{rho+o(1)}, q,rho<1+epsilon, advice-free bit parsing, and every semantic SAT use either SATeq/bounded-SR_h or charged separately; otherwise FE_Extract_N is required.

## Assumptions

- Model: nonuniform Boolean circuits; proof verifier is uniform in proof length; extension variables declare bit-level support DAG; RowSet is not semantic advice.
- Regime: N tends to infinity, epsilon>0 is fixed, M_N=N^{q+o(1)}, and SR leaf-enumeration exponents eta,tau are uniform over accepted proofs.
- SR_h rule: from node u it asserts SAT(F_u)=OR_b SAT(F_{u,b}) through at most h bounded steps; verifier exposes local rewrite neighborhoods, not global truth.
- Same-theory condition: SATeq links and SR rewrites use the same binary formula encoding as G_N; symbolic FormulaEval lines are excluded from this lemma.
- Barrier status: the parser is occurrence-local and relativizing; any full Psys_sym extension must be nonrelativizing via FE_Extract_N or be quarantined.

## Equations

- SR-charge: `B_{SR}(\pi)=\sum_{r\in K_{SR}(\pi)} O(N^{\eta+\tau+o(1)}) \le N^{q+\eta+\tau+o(1)}.`. Valid when: Valid when RowSet(pi) is syntactically declared and each bounded-SR_h row has at most N^{eta+tau+o(1)} exposed leaf and neighborhood checks.
- Gamma-bEF: `\Gamma_{bEF}(\pi)=S_{dep}(\pi)+S_{link}(\pi)+B_{SR}(\pi)+E_N N.`. Valid when: Applies after EF dependencies, SATeq links, bounded-SR fields, and sparse row residuals are separately parsed with no semantic advice leakage.
- Transcript-upper-bound: `C(H_N^{SAT}) \le N^{\rho+o(1)}+\Gamma_{bEF}(\pi);\quad N^{\rho+o(1)}+\Gamma_{bEF}(\pi)<N^{1+\epsilon-o(1)} \Rightarrow \neg LB_N(1+\epsilon).`. Valid when: Requires the beta-zero generator substitution and a valid transcript that computes or patches every row touched by pi in the same circuit model.

## Attempted Derivation

- Encode each SR line as (tag=SR,row j,node u,depth t,branch b,parent pointer,occurrence offsets). Row j has (q+o(1))log N bits; node/depth fields contribute the eta,tau overhead; local neighborhoods are polylog N.
- Verifier checks parent-child formula transformations by rereading only listed neighborhoods and SATeq-normalized bit strings. No semantic SAT truth is queried; the rule contributes its declared row to K_SR and listed leaves to B_SR.
- Induct on proof lines: EF lines add S_dep, SATeq lines add S_link, SR_h lines add the bounded-SR term, and pointers compose parsed transcripts. Thus Q_i has exactly the partial Gamma_bEF cost up to uniform o(1) encoding slack.
- Given Q_pi and G_N, build a circuit generating referenced formulas, implementing transcript leaf decisions, patching E_N residual rows, and XORing outputs. A subthreshold cost is a valid falsifier for LB_N(1+epsilon).

Blocking gap: The induction excludes symbolic FormulaEval-SAT; FE_Extract_N is still needed to enumerate RowSet(a) or force the N^{1+q+o(1)} expansion charge.

## Falsifiers

- A semantic FormulaEval line with a private row whose truth depends on an unread enable bit: the surface parser sees no row, but the proof output changes; this falsifier blocks Psys_sym without FE_Extract_N.
- If q+eta+tau>=1+epsilon, the bounded-SR charge alone reaches the lower-bound threshold, so the transcript no longer contradicts LB_N.
- If RowSet is supplied as nonuniform advice of size o(N^epsilon), touched rows may be hidden and the advice-free normal form is invalid.
- If SATeq uses a different formula encoding than G_N, local neighborhoods do not certify target-preserving row identity.

## Learning

Cycle 101 upgrades bounded-SR_h from a named cost to a bit-normal restricted parser theorem: SR contributes B_SR(pi)<=N^{q+eta+tau+o(1)} to Gamma_bEF. The remaining live obstruction is exactly FE_Extract_N for symbolic FormulaEval rows.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the bounded-SR_h charge threshold.`
- Rationale: The branch needs to verify whether SR_h normal form gives an actual subthreshold transcript or merely renames semantic proof power. Varying one exponent tests the exact contribution to Gamma_bEF.
- Situation seed: Beta-zero XOR carrier H_N with M_N=N^{q+o(1)} generated polylog SAT formulas, and a Psys_bEF^- proof in which every generated row may invoke one explicit bounded-SR_h rule with declared neighborhoods.
- Varied variable: tau, the exponent for SR_h node/depth and leaf-index overhead per touched row.
- Held-fixed controls: L=(log N)^d, so target-query beta remains zero., Generator size is N^{rho+o(1)} with q,rho<1+epsilon., Proof system is bit-explicit EF+SATeq+bounded-SR_h, excluding FormulaEval oracle lines., RowSet is syntactically declared and advice-free.
- Expected observation: For q+eta+tau<1+epsilon and small residual E_N, Gamma_bEF is subthreshold and refutes the claimed LB_N certificate; crossing q+eta+tau=1+epsilon removes the falsifier.
- Transfer certificate needed: A checked SRhBitNormalForm parser: uniform RowSet enumeration, local occurrence-neighborhood verification, same-encoding SATeq normalization, and line induction proving the bounded-SR term in Gamma_bEF.

## Next Experiment

Write the finite verifier table for one SR_h rule: tag layout, row j encoding, node/depth fields, parent pointers, occurrence-neighborhood list, and the exact charge contributing to B_SR(pi).

# Barrier-Aware Lower-Bound Route: interval-union FormulaEval expansion boundary

## Candidate Lemma

For Psys_sym^iu, a bit-explicit EF+SATeq+bounded-SR_h proof system whose FormulaEval-SAT atoms carry disjoint interval-union row selectors, every accepted proof pi of LB_N(1+epsilon) for H_N^SAT has an expansion-aware transcript with cost Gamma_iu(pi)=S_dep+S_link+N^{q+eta+tau+o(1)}+N E_N. Hence a sound proof must satisfy |K_idx(pi)|+E_N>=N^{epsilon-o(1)} whenever rho<1+epsilon; otherwise the transcript gives a circuit upper-bound falsifier for the asserted lower bound.

## Definitions

- source object: a Psys_sym^iu proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), where M_N=N^{q+o(1)} and each FormulaEval-SAT selector is a proof-displayed disjoint union of intervals in [M_N].
- target object: an expansion-aware occurrence transcript Q_pi plus a nonuniform circuit for H_N^SAT of size at most N^{rho+o(1)}+Gamma_iu(pi), used only as a route-level falsifier to the proof-system lower-bound claim.
- controlled interface: RowSetEnumerator_N reads only proof bits, interval endpoints, extension-DAG pointers, SATeq links, and bounded-SR_h occurrence neighborhoods, then emits concrete row indices and instantiated SAT(G_N(x,j)) atoms with no semantic advice.
- target-preserving condition: each emitted row j is row-faithful for the same beta-zero carrier H_N^SAT, preserves the generator G_N and length regime, and charges N per semantically selected row before any lower-bound-to-circuit contradiction is invoked.
- K_idx(pi) is the set of concrete SAT rows already exposed by ordinary row-faithful bEF, SATeq, and bounded-SR_h syntax.
- E_N is the total number of additional rows emitted by FormulaEval^iu selectors, counted with multiplicity suppressed after canonical row indexing.
- S_dep and S_link are the extension-DAG dependency and equality-link transcript sizes; they exclude the N E_N FormulaEval expansion charge.

## Assumptions

- Model: nonuniform Boolean circuits over the beta-zero truth-table carrier H_N^SAT; this is not a many-one reduction from SAT and not a proof of P != NP.
- Proof system: Psys_sym^iu extends bit-explicit Psys_bEF only by FormulaEval^iu lines whose selectors are syntactically listed interval unions with endpoints of O(log M_N) bits.
- Uniformity: RowSetEnumerator_N is deterministic and advice-free; all interval endpoints and formula-template bits are contained in pi or generated from the fixed uniform G_N.
- Regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, bounded-SR_h neighborhood parameter h=N^{eta+o(1)}, and generator overhead N^{rho+o(1)} with rho<1+epsilon.
- Soundness premise: an accepted Psys_sym^iu proof of LB_N(1+epsilon) asserts C(H_N^SAT)>N^{1+epsilon-o(1)} in the same nonuniform circuit model in which the transcript upper bound is built.
- Cutoff: interval enumeration is charged by semantic row mass; if the selector description uses hidden predicates, oracle bits, or advice-generated endpoints, the lemma is invalid and the opaque-countermodel lemma applies.
- Barrier status: the construction may become a natural property only if the transcript induces a poly(N)-constructive large useful set of truth tables; this lemma itself is a proof-system parser and upper-bound falsifier.

## Equations

- row_count: `M_N=N^{q+o(1)}`. Valid when: Valid when the source carrier is the beta-zero SAT parity family with the row generator fixed uniformly for the whole proof packet.
- interval_expansion_mass: `E_N=\left|\bigcup_{a\in FE(\pi)} RowSet(a)\setminus K_{idx}(\pi)\right| \leq M_N`. Valid when: Applies when every FormulaEval selector is proof-displayed as an interval union and RowSetEnumerator_N canonicalizes duplicate row indices.
- gamma_interval_union: `\Gamma_{iu}(\pi)=S_{dep}+S_{link}+N^{q+\eta+\tau+o(1)}+N E_N`. Valid when: Requires the bit-explicit Psys_bEF parser costs plus the transparent FormulaEval expansion charge for all selected rows.
- transcript_upper_bound: `C(H_N^{SAT})\leq N^{\rho+o(1)}+\Gamma_{iu}(\pi)`. Valid when: Applies after the transcript is row-faithful and the generator circuit of size N^{rho+o(1)} is shared across instantiated rows.
- forced_support: `|K_{idx}(\pi)|+E_N\geq N^{\epsilon-o(1)}`. Valid when: Valid when pi soundly proves C(H_N^{SAT})>N^{1+epsilon-o(1)} and rho is strictly below 1+epsilon.
- density_trichotomy: `\frac{|K_{idx}(\pi)|+E_N}{M_N}\geq N^{\epsilon-q-o(1)}`. Valid when: Requires the forced-support inequality and the row-count normalization M_N=N^{q+o(1)} in the same length regime.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Barrier-Aware Lower-Bound Route; source object: a Psys_sym^iu proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), where M_N=N^{q+o(1)} and each FormulaEval-SAT selector is a proof-displayed disjoint union of intervals in [M_N].; target object: an expansion-aware occurrence transcript Q_pi plus a nonuniform circuit for H_N^SAT of size at most N^{rho+o(1)}+Gamma_iu(pi), used only as a route-level falsifier to the proof-system lower-bound claim.; Model: nonuniform Boolean circuits over the beta-zero truth-table carrier H_N^SAT; this is not a many-one reduction from SAT and not a proof of P != NP..
- Define Psys_sym^iu by adding FormulaEval^iu lines to Psys_bEF; each such line stores a formula template T_a(x,j), a list of disjoint intervals [l_b,r_b] subset [M_N], and a local proof-checker certificate that endpoints are ordered and in range.
- Construct RowSetEnumerator_N(pi,a): scan interval endpoints, output each j in each interval once, and instantiate the row atom SAT(G_N(x,j)) with the same bit encoding used by the bEF parser.
- Run the existing transitive extension-DAG traversal on ordinary bEF, SATeq, and bounded-SR_h lines; append the FormulaEval-instantiated rows as new leaves with link records to their originating FE line.
- Charge ordinary syntax by S_dep+S_link+N^{q+eta+tau+o(1)} and charge each newly emitted FormulaEval row by N for the row SAT-evaluation circuit or transcript simulation, giving N E_N.
- If |K_idx|+E_N<N^{epsilon-o(1)} and rho<1+epsilon, combine the shared generator circuit of size N^{rho+o(1)} with the parsed row transcript to obtain C(H_N^SAT)<N^{1+epsilon-o(1)}, contradicting the sound lower-bound sentence.
- Normalize by M_N=N^{q+o(1)} to get the support-density trichotomy: q<epsilon falsifier by subthreshold support, q=epsilon+o(1) near-full contact, q>epsilon only absolute support pressure.

Blocking gap: This is a proof for interval-union transparent selectors only. Unrestricted Psys_sym remains blocked at RowSetEnumerator_N/SATSemanticLocality_N for arbitrary symbolic predicates or semantic FormulaEval oracles.

## Falsifiers

- falsifier: If q<epsilon and |K_idx|+E_N<N^{epsilon-o(1)}, the parsed transcript plus generator gives a valid circuit upper bound below the claimed LB_N(1+epsilon).
- falsifier: A single opaque FormulaEval atom with an unread enable bit for private row j* has identical surface syntax but different semantic support, refuting occurrence completion.
- falsifier: Selector endpoints generated by hidden advice rather than proof bits break the no-advice RowSetEnumerator_N and invalidate the transparent expansion theorem.
- falsifier: Shared formula-DAG equality can merge displayed occurrences, so occurrence count alone is invalid unless replaced by semantic row support K_idx^+.
- falsifier: Treating FormulaEval as an extension rule without charging N per selected row collapses to the N^{1+q+o(1)} upper-bound regime and loses the claimed threshold.

## Learning

Cycle 101 closes a concrete fragment: interval-union FormulaEval is target-preserving exactly because rows are enumerable and charged by N E_N. Opaque FormulaEval is not an uncharged proof line; the unread-enable-bit row is a finite falsifier to surface occurrence completion. This is valid route-level proof-system certification, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The remaining gap is not abstract barrier folklore but whether FormulaEval selectors expose row support or hide it semantically; a concrete private-row experiment separates the two proof-system mechanisms.
- Situation seed: Take H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with one FormulaEval line FE(a). In the transparent world, RowSet(a) is the interval [1,L]. In the opaque world, RowSet(a) is [1,L] plus a hidden enable-controlled row j*>L not mentioned in pi.
- Varied variable: selector transparency: interval-union row mass L versus one hidden unread-enable-bit row j*.
- Held-fixed controls: same generator G_N, row count M_N=N^{q+o(1)}, and lower-bound sentence LB_N(1+epsilon), same displayed proof bits, extension-DAG links, SATeq syntax, and bounded-SR_h verifier resources, same nonuniform circuit target and no-advice parser requirement
- Expected observation: The interval world expands with charge N L and is parser-valid; the opaque world has the same surface transcript but different H_N^SAT value after toggling row j*, proving that semantic FormulaEval cannot be promoted without a row enumerator or semantic-locality certificate.
- Transfer certificate needed: A valid promotion needs RowSetEnumerator_N for the selector class or a nonrelativizing SATSemanticLocality_N theorem proving that all semantically relevant rows are charged in K_idx^+ without leaking advice.

## Next Experiment

Extend RowSetEnumerator_N from interval-union selectors to AC0 row selectors by scanning all M_N rows with explicit membership circuits; record whether the forced charge becomes N^{1+q+o(1)} automatically or whether a smaller enumerable normal form exists without semantic advice.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For Psys_sym^IU, where FormulaEval-SAT lines use advice-free interval-union row selectors and the SAT-query generator G_N is uniform, every valid FormulaEval use has a dichotomy: transparent lines parse into a RowSet transcript costing T_N N^{q+o(1)}, while any nontransparent claim about an unparsed row-query pair admits a two-completion private-row falsifier unless UExtWitnessability supplies an advice-free quotient witness charged separately.

## Definitions

- source object: a Psys_sym^IU FormulaEval-SAT proof line for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with x in [N], M_N=N^{q+o(1)}, polylogarithmic formula encodings, and interval-union row selector data written in the proof.
- target object: a bit-explicit occurrence transcript Gamma_FE(ell) that the parser can add to Gamma_bEF(pi) and then use to build a nonuniform circuit for H_N^SAT under the beta-zero upper-bound falsifier.
- controlled interface: RowSetEnumerator_N reads the line ell, enumerates selected rows and row-query formula occurrence neighborhoods, and records SATeq or FormulaEval dependencies without semantic advice.
- target-preserving condition: the enumeration must be E-uniform, advice-free, same-generator, same-length, and must preserve the unrestricted circuit lower-bound target LB_N(1+epsilon) rather than selecting a nonuniform hard row.
- RowSet(ell) is the set of row indices covered by the interval-union selector after canonical disjoint sorting; T_N=|RowSet(ell)|.
- Transparent FormulaEval means the proof object exposes enough bit fields to reconstruct every G_N(x,j) encoding used by the SAT assertion; semantic FormulaEval means the proof asserts SAT(G_N(x,j)) without those bit fields.
- UExtWitnessability means an advice-free quotient or extension witness proving formula identity or SAT extensionality inside the same Cook-Reckhow proof model.

## Assumptions

- Length regime: N ranges over powers of two, row inputs have log N bits, M_N=N^{q+o(1)} for fixed q>=0, and each generated formula has length L_N=(log N)^{O(1)}.
- Proof model: interval endpoints and selector tags are part of the proof string; the parser may canonicalize them but may not use nonuniform row advice or semantic SAT answers.
- Uniformity regime: G_N(x,j) is computable in N^{rho+o(1)} size or time and the transcript generator runs within a fixed E exponent.
- Target model: LB_N(1+epsilon) quantifies unrestricted Boolean circuits for the full truth table of H_N^SAT, not a restricted proof-system circuit class.
- Semantic-escape cutoff: an unparsed FormulaEval rule is not valid for the controlled interface unless UExtWitnessability is explicitly supplied and its adaptive-cover cost is charged.
- Non-claim boundary: the lemma is a restricted FormulaEval classification and upper-bound falsifier, not a proof of P != NP.

## Equations

- per_row_eval_cost: `E_N=M_N L_N=N^{q+o(1)}`. Valid when: Valid when M_N=N^{q+o(1)} and each generated SAT formula has polylogarithmic bit length.
- interval_union_transcript_charge: `\Gamma_{FE}(\ell)=T_N E_N+O(R_N\log N)+N^{o(1)}=T_N N^{q+o(1)}+N^{a+o(1)}`. Valid when: Applies when interval endpoints are explicitly encoded and the parser unfolds every selected row-query formula.
- full_row_formulaeval_expansion: `T_N=N\ \Longrightarrow\ \Gamma_{FE}^{full}=N E_N=N^{1+q+o(1)}`. Valid when: Requires the FormulaEval line to bind all N rows transparently without semantic oracle compression.
- low_cost_upper_bound_falsifier: `N^{\rho+o(1)}+\Gamma_{bEF}(\pi)+\Gamma_{FE}(\pi)<N^{1+\epsilon-o(1)}\ \Longrightarrow\ LB_N(1+\epsilon)\text{ is false}`. Valid when: Valid when the parsed transcript computes H_N uniformly and the lower-bound sentence quantifies unrestricted circuits.
- private_row_two_completion: `Tr_{\pi}(C_0)=Tr_{\pi}(C_1)\ \wedge\ H_N^{SAT,C_0}(x^*)\ne H_N^{SAT,C_1}(x^*)`. Valid when: Applies when some row-query formula contains an eval-critical bit outside all parsed occurrence neighborhoods.

## Attempted Derivation

- Fix H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)} and L_N=(log N)^{O(1)}. Let ell be a FormulaEval-SAT line with interval-union selector I_1,...,I_R and no semantic SAT oracle tag.
- Parse the bit fields of ell: rule tag, interval count R, endpoints, generator identifier, formula-length convention, and SATeq links. Canonicalize intervals by sorting and merging overlaps; this costs O(R log N) bits and is proof-local.
- Enumerate each row x in the canonical RowSet and each query j<=M_N. For each pair compute or copy the bit encoding of G_N(x,j), list the touched occurrence neighborhoods, and attach the SAT assertion dependency. This yields T_N M_N L_N plus endpoint overhead.
- If RowSet covers all rows, substitute T_N=N to obtain the expansion N^{1+q+o(1)}. Adding this to the already parsed Gamma_bEF(pi) gives the upper-bound falsifier whenever the total is below N^{1+epsilon-o(1)}.
- For a nontransparent FormulaEval line, choose an unparsed row-query pair (x*,j*) with an eval-critical enable bit. Construct completions C_0 and C_1 that agree on every parsed bit and proof dependency but make G_N(x*,j*) unsatisfiable in one completion and satisfiable in the other. Then the transcript is identical while H_N^SAT(x*) flips, so row-parity binding is invalid.
- For AC0 selectors, a full row scan is valid and gives N^{1+o(1)}+T_N N^{q+o(1)}. The attempted support-sensitive extension is blocked because compressed AC0 descriptions do not automatically supply uniform rank/unrank enumeration of satisfying rows.

Blocking gap: The interval-union transparent fragment is proved, and AC0 scan expansion is valid, but support-sensitive RowSetEnumerator_N for arbitrary compressed AC0 selectors and UExtWitnessability for semantic FormulaEval remain named open obligations.

## Falsifiers

- private-row falsifier: if RowSet(ell) omits x* and no quotient witness binds that row, two completions preserve the proof transcript but flip H_N^SAT(x*).
- unread-enable-bit falsifier: an unparsed formula bit can toggle a generated SAT instance between unsatisfiable and tautological while every surface occurrence read by the proof remains fixed.
- support-sensitive AC0 falsifier: a compressed AC0 selector does not justify a T_N N^{q} charge unless a valid uniform rank/unrank enumerator is provided.
- nonuniform-endpoint falsifier: interval endpoints supplied as advice rather than proof bits destroy the target-preserving Cook-Reckhow parser.
- threshold falsifier: q>=epsilon eliminates the subthreshold upper-bound contradiction from full FormulaEval expansion, though semantic-oracle classification is still required.
- UExt leakage falsifier: a FormulaEval line that hides formula identity in semantic advice is outside Psys_sym^IU and cannot be promoted as a controlled carrier transfer.

## Learning

Cycle 101 closes a concrete proof-delivery subcase: interval-union transparent FormulaEval is not free but pays T_N N^{q+o(1)}, full-row FormulaEval pays N^{1+q+o(1)}, and nontransparent omitted rows have a private-row falsifier. Arbitrary AC0 selectors are safe only with scan charge until a support-sensitive enumerator is proved. This is a paper-level obstruction theorem fragment, not progress on P != NP itself.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the FormulaEval-SAT boundary.`
- Rationale: The branch must decide whether symbolic FormulaEval is a charged transcript or an oracle escape; another abstract barrier restatement would not resolve the parser theorem packet.
- Situation seed: Take a padded SAT-query family G_N(x,j) whose encoding contains an enable bit e_{x,j}: e=0 encodes a fixed unsatisfiable formula and e=1 encodes a fixed tautological satisfiable formula, with all other bits generated uniformly. A Psys_sym^IU line claims FormulaEval over an interval-union RowSet.
- Varied variable: Coverage exponent f where T_N=|RowSet|=N^{f+o(1)}, moving from sparse selected rows to f=1 full-row FormulaEval.
- Held-fixed controls: M_N=N^{q+o(1)} and formula length L_N=(log N)^{O(1)}., Interval endpoints are explicit proof bits, not advice., The lower-bound target remains LB_N(1+epsilon) for unrestricted circuits computing full H_N^SAT., No UExtWitnessability or semantic SAT oracle is allowed unless separately declared and charged.
- Expected observation: For f<1 there is an omitted row, and flipping one unread enable bit gives a private-row falsifier. For f=1 the private row disappears but the transparent transcript pays N^{1+q+o(1)} expansion.
- Transfer certificate needed: A formal RowSetEnumerator_N plus row-parity binding lemma showing that every semantically forced row is either enumerated and charged or covered by a valid advice-free quotient witness.

## Next Experiment

Write the paper-ready theorem for Psys_sym^IU: include the bit-field grammar, RowSetEnumerator_N pseudocode, Gamma_FE derivation, private-row enable-bit countermodel, and then decide whether AC0 selectors are accepted with scan charge or quarantined until support-sensitive enumeration is proved.
