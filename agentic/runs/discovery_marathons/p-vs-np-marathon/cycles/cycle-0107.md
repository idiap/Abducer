# cycle-0107

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Transparent selector FormulaEval extraction: in Psys_sym^{sel-scan}, every FormulaEval-SAT line whose row selector is a bit-explicit predicate Sel_a(j) over j< M_N can be expanded to occurrence rows either output-sensitively when RowSetEnumerator_N is supplied, or by a uniform full scan with charge F_FE(pi) N^{1+q+o(1)}. Consequently a parsed proof pi yields the same parser-to-circuit falsifier as Psys_bEF^- with Gamma_bEF enlarged by B_FE^{sel}; if N^{rho+o(1)}+Gamma_bEF^{sel}(pi)<N^{1+epsilon-o(1)}, then the claimed source lower bound LB_N(1+epsilon) is false. This is a route-level valid theorem packet, not a P != NP claim.

## Definitions

- source object: Psys_sym^{sel-scan} proofs pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, |G_N(x,j)|=(log N)^d, and bit-explicit FormulaEval selector descriptors a.
- target object: an occurrence transcript Gamma_bEF^{sel}(pi) plus a nonuniform circuit for H_N^SAT of size N^{rho+o(1)}+Gamma_bEF^{sel}(pi), giving a falsifier for LB_N(1+epsilon) when this size is subthreshold.
- controlled interface: RowSetEnumerator_N(a) either lists RowSet(a)={j<M_N:Sel_a(j)=1} with output-sensitive N^{o(1)} delay, or the proof system explicitly accepts the full-scan fallback over all M_N slots and pays N M_N per FormulaEval line.
- target-preserving condition: the selector predicate, row index encoding, generator G_N, SAT formula encoding, and expansion charge are uniform and advice-free; unexpanded semantic FormulaEval-SAT is not counted as occurrence support.

## Assumptions

- Length regime: N tends to infinity, q,rho,epsilon,eta,tau are fixed constants with M_N=N^{q+o(1)} and polylogarithmic SAT instance length L_N=(log N)^d.
- Proof-size regime: the number F_FE(pi) of FormulaEval lines and all selector descriptors are N^{o(1)} unless explicitly charged inside Gamma_bEF^{sel}(pi).
- Circuit model: target circuits are nonuniform Boolean circuits for H_N^SAT; source lower bound LB_N(1+epsilon) means C(H_N^SAT)>N^{1+epsilon-o(1)} in the same circuit model.
- Uniformity and advice status: the parser may read pi and N but has no semantic advice about SAT labels; any selector enable bit depending on SAT truth is a semantic-oracle mechanism and is excluded from this lemma.
- Barrier status: the extraction is syntactic and relativizing as an upper-bound falsifier; it is not a natural-proofs argument and does not attempt a lower-bound certificate.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j<M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad |G_N(x,j)|=(\log N)^d.`. Valid when: Valid when the beta-zero carrier has polylogarithmic SAT queries, explicit row index encoding, and generator size N^{rho+o(1)}.
- output_sensitive_FE_charge: `B_{FE}^{out}(\pi)=N^{1+o(1)}\sum_{\ell\in FE(\pi)} |RowSet(a_\ell)|.`. Valid when: Valid when RowSetEnumerator_N is uniform, advice-free, and lists exactly the selected rows with subpolynomial per-output overhead.
- full_scan_FE_charge: `B_{FE}^{scan}(\pi)=F_{FE}(\pi)\,N\,M_N\,N^{o(1)}=F_{FE}(\pi)N^{1+q+o(1)}.`. Valid when: Valid when selectors are decidable from proof bits and row indices but no output-sensitive enumeration certificate is available.
- selector_gamma: `\Gamma_{bEF}^{sel}(\pi)=S_{dep}(\pi)+S_{link}(\pi)+N^{q+\eta+\tau+o(1)}+B_{FE}^{sel}(\pi)+E_NN.`. Valid when: Applies after EF dependencies, SATeq links, bounded-SR_h neighborhoods, FormulaEval expansions, and sparse row patches are all charged.
- parser_falsifier: `N^{\rho+o(1)}+\Gamma_{bEF}^{sel}(\pi)<N^{1+\epsilon-o(1)}\;\Longrightarrow\;\neg LB_N(1+\epsilon).`. Valid when: Requires the target-preserving parser-to-circuit simulation in the same nonuniform circuit model as the asserted source lower bound.
- support_trichotomy: `|K_{idx}(\pi)|\ge N^{\epsilon-o(1)},\quad |K_{idx}(\pi)|/M_N\ge N^{\epsilon-q-o(1)}.`. Valid when: Valid for any parsed proof that avoids the subthreshold falsifier and charges each complete contacted row by N^{1-o(1)}.

## Attempted Derivation

- Defined Psys_sym^{sel-scan}: each FormulaEval-SAT line contains a selector descriptor a, a syntactic evaluator Sel_a(j), and either an enumerator certificate or permission to full-scan j<M_N.
- For an output-sensitive enumerator, replaced the FormulaEval line by one occurrence expansion per j in RowSet(a); the charge is N^{1+o(1)} per complete row because the row-neighborhood transcript must be usable in the H_N^SAT circuit simulation.
- For selectors without an enumerator, scanned all M_N=N^{q+o(1)} row indices, evaluated Sel_a(j) syntactically, and expanded every accepted row. This proves B_FE^{scan}=F_FE N^{1+q+o(1)} for F_FE=N^{o(1)}.
- Inserted B_FE^{sel} into the previously promoted line-induction proof for Psys_bEF^-: EF dependency, SATeq link, bounded-SR_h, FormulaEval, and sparse-patch charges are additive in Gamma_bEF^{sel}.
- Derived the live inference-quality source statement: a Psys_sym^{sel-scan} proof of LB_N(1+epsilon) with subthreshold Gamma_bEF^{sel} yields a circuit for H_N^SAT below N^{1+epsilon-o(1)}, contradicting the source statement in the same circuit model.
- Tried to upgrade arbitrary AC0 selectors to output-sensitive RowSetEnumerator_N by recursive prefix search; the missing step is uniform AC0PrefixNonemptiness_N with N^{o(1)} delay, so only the full-scan fallback is currently proved.

Blocking gap: AC0PrefixNonemptiness_N: no advice-free, output-sensitive enumeration theorem is proved for arbitrary AC0 row selectors over q log N row bits; brute force gives a valid but sometimes over-threshold scan charge.

## Falsifiers

- semantic FormulaEval enable bit depending on a private SAT row, which breaks occurrence completion unless charged by FE_Extract_N^{sem}
- q<epsilon with F_FE=N^{o(1)} under full-scan extraction, since B_FE^{scan}=N^{1+q+o(1)} is subthreshold and falsifies LB_N(1+epsilon)
- nonuniform selector advice that names RowSet(a) without being encoded in pi, invalidating the advice-free parser model
- AC0 sparse selector with no certified prefix-nonemptiness procedure, blocking output-sensitive enumeration and forcing the weaker scan charge
- positive beta black-box substitution interface, where q+beta c caps any claimed all-exponent NP not subset P/poly transfer

## Learning

Cycle 107 adds a real validation upgrade: transparent FormulaEval selectors no longer require interval-union structure for a valid theorem, because full syntactic scanning gives a certified B_FE=F_FE N^{1+q+o(1)} charge. This closes the q<epsilon falsifier for a broader selector fragment and isolates the only missing improvement as AC0PrefixNonemptiness_N for output-sensitive enumeration. Full semantic FormulaEval remains quarantined by the private-row falsifier, not by generic barrier folklore.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for semantic FormulaEval and as a calibration case for transparent selector extraction.`
- Rationale: The restricted theorem is already promoted; the remaining danger is an invalid upgrade from syntactic FormulaEval rows to semantic row access. A concrete private-row experiment tests exactly whether row support is explicit or hidden.
- Situation seed: Let M_N=N^q and add one FormulaEval line with selector Sel_e(j)=IU_a(j) OR (e AND [j=j_*]), where IU_a is a transparent interval-union selector and e is either an explicit proof bit or the semantic bit SAT(G_N(x_0,j_*)).
- Varied variable: explicitness of the enable bit e: syntactic proof-bit, enumerator-visible computed bit, or hidden SAT-semantic bit.
- Held-fixed controls: The beta-zero carrier H_N^SAT and generator size N^{rho+o(1)} remain fixed., The target class is the same nonuniform circuit model used by LB_N(1+epsilon)., Formula length remains L_N=(log N)^d and row indices have q log N+o(log N) bits., Expansion charge N per complete selected row is always paid when the row is explicit.
- Expected observation: When e is explicit, RowSetEnumerator_N outputs j_* and the parser pays one extra N-row charge; when e is hidden semantically, two private-row labelings agree on the exposed transcript but disagree on the FormulaEval line, so occurrence extraction is invalid.
- Transfer certificate needed: A formal FE_Extract_N certificate showing that every enable condition affecting FormulaEval truth is computable from proof bits and row index, or else an explicit expansion theorem charging the semantic dependency before it enters Gamma_bEF^{sel}.

## Next Experiment

Formalize AC0PrefixNonemptiness_N as a finite lemma: for AC0 selectors on q log N row bits, test whether descriptor structure yields N^{o(1)} prefix emptiness; if not, state the selector-scan theorem as final and add AC0 output-sensitive enumeration to open problems.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For Psys_sym^{ext,infl}, FormulaEval introduced as an extension rule is parser-safe exactly when every SAT-influential row has proof-visible selector and influence code. Then a deterministic no-advice extractor outputs K_idx^+(pi), charges Gamma_ext(pi), and yields the same upper-bound falsifier as the bit-explicit bEF parser. Semantic FormulaEval remains outside this valid theorem.

## Definitions

- source object: A Psys_sym^{ext,infl} proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), with N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, selector size N^{sigma+o(1)}, and generator size N^{rho+o(1)}.
- target object: A nonuniform SIZE transfer audit producing a Gamma_ext row transcript and the falsifier C(H_N^SAT)<=N^{rho+o(1)}+Gamma_ext(pi) whenever the transcript is subthreshold.
- controlled interface: Each FormulaEval extension line exposes selector circuits, enable bits, extension-DAG parent pointers, and influence certificates for every row whose SAT value can affect that line.
- target-preserving condition: The extractor is deterministic, no-advice, bit-explicit, and preserves N,q,rho,tau,sigma,eta,epsilon while charging every SAT-influential row by enumeration or N-row expansion.

## Assumptions

- Model: EF+SATeq+bounded-SR_h plus FormulaEval extension rules; FormulaEval is not a semantic oracle and not an unparsed proof-line predicate.
- Regime: N=2^n, M_N=N^{q+o(1)}, h=N^{eta+o(1)}, |pi|=N^{tau+o(1)}, q,rho,tau,eta,sigma fixed before the o(1) terms.
- Uniformity/advice: the parser receives only pi,N and public encodings of G_N; it receives no hidden row advice, no private selector advice, and no semantic SAT oracle.
- Extensionality: if two SAT-row tables agree on R_a, the FormulaEval extension value at line a agrees; this is checked by proof-visible SelectorExtensionality_N certificates.
- Influence closure: every row whose SAT bit can change the FormulaEval line is either in R_a or the line is rejected by the extractor.
- Boundary: this is route-level proof-system certification and does not assert P != NP; naturalness pressure applies only if the transcript becomes a large constructive useful truth-table property.

## Equations

- FE-rowset: `R_a=\{j<M_N:\mathrm{Sel}_a(j)=1\wedge \mathrm{Infl}_a(j)=1\}`. Valid when: Valid when the source proof exposes selector and influence circuits in the extension-rule syntax.
- visible-enumeration-cost: `\mathrm{Enum}_N(\pi)\le N^{q+\tau+\sigma+o(1)}`. Valid when: Applies when N^{tau+o(1)} FormulaEval lines use visible selector code evaluable over M_N=N^{q+o(1)} rows.
- charged-support: `K_{idx}^+(\pi)=K_{bEF}(\pi)\cup\bigcup_{a\in FE(\pi)}R_a,\qquad E_N^*=\sum_{a\in FE(\pi)}|R_a|`. Valid when: Valid when K_bEF already comes from the bit-explicit parser and FormulaEval rows are extension-rule visible.
- extension-transcript-cost: `\Gamma_{ext}(\pi)=S_{dep}+S_{link}+N^{q+\tau+\sigma+o(1)}+N E_N^*`. Valid when: Requires selector enumeration, bounded-SR_h line parsing, and row expansion to be charged in the same no-advice transcript.
- upper-bound-falsifier: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{ext}(\pi)`. Valid when: Applies after the reduction preserves generator size and replaces every FormulaEval use by charged row data.
- support-pressure: `LB_N(1+\epsilon)\Rightarrow |K_{idx}^+(\pi)|+E_N^*\ge N^{\epsilon-o(1)}`. Valid when: Valid when the asserted lower bound is C(H)>N^{1+epsilon-o(1)} and non-row overheads stay subthreshold.
- q-density-trichotomy: `\frac{|K_{idx}^+(\pi)|}{M_N}\ge N^{\epsilon-q-o(1)}`. Valid when: Requires M_N=N^{q+o(1)} and the charged union to be the actual SAT-influential support.

## Attempted Derivation

- Fix N=2^n, public G_N, M_N=N^{q+o(1)}, and a Psys_sym^{ext,infl} proof pi of LB_N(1+epsilon).
- Parse the EF extension-DAG and import K_bEF(pi), S_dep, and S_link from the bit-explicit parser packet.
- For each FormulaEval extension line a, read the selector code Sel_a, enable bits, and influence witness Infl_a from proof-visible fields.
- Enumerate all j<M_N, evaluate Sel_a(j) and Infl_a(j), and place j in R_a exactly when both accept.
- Use SelectorExtensionality_N to replace the FormulaEval line by explicit dependence on SAT rows in R_a; reject the line if an influence witness is missing.
- Charge the enumeration by N^{q+tau+sigma+o(1)} and the row expansion by N E_N^*, then form Gamma_ext(pi).
- Compose the parsed transcript with the public generator circuit of size N^{rho+o(1)}; if N^{rho+o(1)}+Gamma_ext(pi)<N^{1+epsilon-o(1)}, obtain the route-level upper-bound falsifier to LB_N(1+epsilon).
- For semantic-oracle FormulaEval, attempt the same parser; the unread-enable-bit construction chooses b outside Q(pi), so the displayed proof surface is unchanged while the required SAT row changes.

Blocking gap: Full Psys_sym remains blocked at RealSATInfluenceRealizer_N: semantic truth of FormulaEval does not imply visible selector extensionality or influence closure.

## Falsifiers

- q<epsilon source-ceiling falsifier: the brute-force row expansion C(H_N^SAT)<=N^{1+q+o(1)} is below the claimed N^{1+epsilon} lower bound.
- Unread-enable-bit falsifier: one hidden enabled row outside Q(pi) changes FormulaEval while preserving the displayed proof surface.
- Hidden-selector-code falsifier: Sel_a is semantically chosen but not proof-visible, so RowSet(a) is not uniformly enumerable.
- Missing-influence-witness falsifier: FormulaEval depends on a row omitted from R_a, invalidating SelectorExtensionality_N.
- Natural-property falsifier: if the extracted transcript induces a poly(N)-constructive large useful property against SIZE, PRF tension applies to the functional property, not to P != NP.

## Learning

Cycle 107 replaces the four-way FormulaEval classification by a sharper extension-rule extractor: visible selector code plus influence closure yields Gamma_ext=S_dep+S_link+N^{q+tau+sigma+o(1)}+N E_N^* and the usual subthreshold falsifier. The exact full-system gap is RealSATInfluenceRealizer_N; semantic FormulaEval is refuted by the unread-enable-bit countermodel rather than by generic barrier folklore.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The branch needs a concrete semantic-escape test for FormulaEval rather than another abstract barrier restatement; the unread row decides whether the parser is genuinely target-preserving.
- Situation seed: A beta-zero H_N^SAT carrier with one FormulaEval extension line whose selector is either proof-visible or hidden as a private enabled row b in a semantic oracle.
- Varied variable: lambda, the number of proof-visible bits revealing the enabled row or selector code, from 0 to log M_N.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and the same LB_N(1+epsilon) sentence., The parser is deterministic and no-advice, with access only to displayed proof syntax and public G_N., The target class remains nonuniform Boolean SIZE and the transfer remains simulation/extraction, not a many-one reduction.
- Expected observation: For lambda=log M_N with extensionality and influence witnesses, RowSet is enumerable and Gamma_ext is valid; for lambda<log M_N, at least two private rows share the same proof surface, giving the unread-enable-bit falsifier.
- Transfer certificate needed: TransparentSelectorCode_N plus SelectorExtensionality_N plus InfluenceClosure_N; without these, the intuition cannot enter proof obligations and the line is classified as semantic oracle.

## Next Experiment

Instantiate the extractor on one concrete FormulaEval extension-rule line with visible AC0 selector code and one hidden-enable semantic variant; record bit fields, RowSet enumeration time, influence witnesses, and the exact Gamma_ext inequality before handing the SR_h line-charge fields to the primary normal-form branch.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For a transparent Psys_sym FormulaEval-SAT line whose selected row set is the projection of a guarded deterministic decomposable NNF C_N(z,y), the valid parser charge is S_N+W_N N^{o(1)}+T_N M_N N^{o(1)}, where W_N counts accepting row-witness pairs and T_N counts distinct projected rows. A T_N-only charge is valid only with an advice-free functional quotient/direct projected-row enumerator or with W_N<=T_N N^{o(1)}.

## Definitions

- source object: a Psys_sym FormulaEval-SAT proof line selecting R_N={z: exists y C_N(z,y)=1}, with C_N a bit-explicit guarded dDNNF over row bits z and auxiliary witness bits y.
- target object: an occurrence transcript for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) and the resulting nonuniform circuit upper-bound falsifier for LB_N(1+epsilon).
- controlled interface: RowSetEnumerator_N enumerates accepting (z,y) witnesses of C_N, projects to z, stable-deduplicates z, and expands FormulaEval only on distinct rows.
- target-preserving condition: C_N, guards, variable partition, and enumerator are advice-free and parseable from the proof line; W_N and T_N M_N are both charged before deriving any target lower-bound contradiction.
- observable: W_N is the witness-support size, T_N is projected row support, S_N is selector description size, and M_N=N^{q+o(1)} is the beta-zero SAT-query count.

## Assumptions

- Model: Psys_sym^proj-gdDNNF treats FormulaEval-SAT as an explicit proof line, axiom schema, or extension rule, not as a semantic oracle.
- Regime: S_N=N^{s+o(1)}, W_N=N^{w+o(1)}, T_N=N^{t+o(1)}, M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)}, and SAT formula length polylog N.
- Uniformity/advice: the dDNNF, decomposition tree, guards, row-bit order, witness-bit domain, and deduplication routine are generated from N and pi without advice-selected rows.
- Cutoff: sorting or stable deduplication of O(log N)-bit row addresses costs N^{o(1)} per emitted witness or row in the transcript/circuit accounting.
- Same-theory condition: the rule evaluates syntactic formulas G_N(z,j); formula identity or SAT extensionality is allowed only when witnessed and paid by the existing quotient-cover ledger.
- Non-claim: the lemma is a FormulaEval expansion/falsifier theorem for a restricted proof mechanism, not a proof of P != NP.

## Equations

- witness_support: `W_N = |{(z,y): C_N(z,y)=1}| = N^{w+o(1)}`. Valid when: Valid when C_N is a guarded deterministic decomposable NNF over explicitly bounded row and witness variables.
- projected_support: `T_N = |{z: exists y C_N(z,y)=1}| = N^{t+o(1)}, t <= w`. Valid when: Applies after projection is only over auxiliary witness variables and row addresses remain explicit.
- projected_formulaeval_charge: `Gamma_proj(N) <= S_N + W_N N^{o(1)} + T_N M_N N^{o(1)}`. Valid when: Requires witness enumeration, projection deduplication, and distinct-row FormulaEval expansion to be charged in the transcript.
- upper_bound_transfer: `C(H_N^SAT) <= N^{rho+o(1)} + Gamma_base(pi) + Gamma_proj(N)`. Valid when: Applies after the parsed transcript and beta-zero generator are combined in the same nonuniform circuit model.
- lb_falsifier_threshold: `max{rho,gamma_base,s,w,t+q} < 1+epsilon => not LB_N(1+epsilon)`. Valid when: Valid when LB_N asserts size at least N^{1+epsilon-o(1)} in the unrestricted nonuniform circuit model.

## Attempted Derivation

- Fix a Psys_sym^proj-gdDNNF FormulaEval line with bit-explicit C_N(z,y), row address length O(log N), witness domain Y_N, selector size S_N, witness support W_N, and projected support T_N.
- Use guarded deterministic decomposability to enumerate each satisfying full assignment (z,y) with near-linear delay in the output size; this is a standard transparent enumeration step over the full variable space, not over the projection.
- Project each emitted pair to z and run stable deduplication on O(log N)-bit row addresses; this costs W_N N^{o(1)} and produces exactly the distinct RowSet R_N when the dDNNF and guards are syntactically parsed.
- For every distinct row z in R_N, expand the FormulaEval-SAT step over the M_N=N^{q+o(1)} generated SAT instances G_N(z,j), contributing T_N M_N N^{o(1)} occurrence work.
- Add selector description size S_N and compose with the existing beta-zero generator overhead N^{rho+o(1)} and prior parser ledger Gamma_base(pi), yielding the nonuniform circuit upper bound.
- Conclude the low-cost falsifier: if every exponent in {rho,gamma_base,s,w,t+q} is below 1+epsilon by omega(1), the claimed LB_N(1+epsilon) for H_N^SAT is false in the target circuit model.
- Attempted strengthening to charge only T_N fails: projection can have T_N=1 and W_N=N^{beta}; without a functional quotient or direct projected enumerator, the parser has no syntactic certificate that all hidden witnesses collapse to the same row set.

Blocking gap: No lower bound is claimed for arbitrary projected dDNNF enumeration: a special advice-free direct projected-row enumerator U_N may beat W_N. The exact valid dichotomy is charge min{U_N,W_N} for row discovery, plus T_N M_N for FormulaEval expansion, with U_N allowed only when explicitly certified.

## Falsifiers

- falsifier: a projected selector with T_N small, W_N=N^{beta} large, and no canonical quotient invalidates a T_N-only FormulaEval charge.
- falsifier: a membership-only projected selector can hide an unread witness fiber and admit a private-row spoof.
- falsifier: advice-supplied canonical witnesses identify nonuniform rows and do not preserve the target E/nonuniform-circuit transfer ledger.
- falsifier: unparsed SAT extensionality or FormulaEval semantics is a semantic-oracle model change, not a transparent proof-system rule.
- falsifier: a genuine direct projected-row enumerator U_N << W_N refutes any claimed necessity of W_N charge and must be recorded as an escape certificate.

## Learning

Cycle 107 refines projection fiber entropy into an auditable FormulaEval ledger. The exact row-discovery cost is min{certified projected enumerator U_N, witness support W_N}; the exact SAT expansion cost is T_N M_N. This is a valid paper-level obstruction/falsifier for projected selectors, not progress on the main P vs NP conjecture.

## Gedanken Experiment Design Seed

- Need decision: `use now as a falsifier probe and threshold calibrator`
- Rationale: The projected-selector loophole is concrete: support T_N can be tiny while hidden witness support W_N is large. Varying the fiber exponent tests whether the parser charge must include witness discovery or whether a quotient certificate suffices.
- Situation seed: A family C_{N,beta}(z,y)=A_N(z) AND B_{z,beta}(y) of guarded dDNNF selectors, with |{z:A_N(z)=1}|=N^t, each selected row having N^beta witnesses, and FormulaEval applied to H_N^SAT with M_N=N^q generated formulas.
- Varied variable: fiber exponent beta, so W_N=N^{t+beta+o(1)} while projected support remains T_N=N^{t+o(1)}.
- Held-fixed controls: The beta-zero generator G_N, query count q, and generator overhead rho remain fixed., C_{N,beta} is bit-explicit, guarded, deterministic, decomposable, and advice-free., FormulaEval-SAT is treated as a transparent syntactic proof line, not as a semantic oracle., The target lower-bound claim is LB_N(1+epsilon) against unrestricted nonuniform circuits.
- Expected observation: As beta increases, the valid transcript exponent shifts from max{s,t+q} to max{s,t+beta,t+q} unless a canonical quotient of exponent u<t+beta is supplied. Thus projected support alone is not a valid cost certificate.
- Transfer certificate needed: A formal Psys_sym encoding of witness enumeration, projection deduplication, and quotient coverage; otherwise the intuition may only be used as a private-row falsifier and not as a promoted parser theorem.

## Next Experiment

Finalize the bit-level Psys_sym encoding for projected guarded dDNNF enumeration: specify row/witness fields, guard table, deterministic-decomposition traversal, stable dedup circuit, and then decide whether the paper theorem states the W_N charge, the canonical-quotient escape, or the private-projection countermodel as the promoted result.
