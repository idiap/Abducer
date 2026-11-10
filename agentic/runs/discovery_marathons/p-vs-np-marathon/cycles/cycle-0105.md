# cycle-0105

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Restricted parser/falsifier theorem: for beta-zero parity carrier H_N^SAT and any accepted Psys_bEF^- proof pi whose FormulaEval-SAT mechanisms are transparent interval-union selectors, a uniform parser outputs an explicit transcript Q_pi with cost Gamma_bEF^IU(pi). If N^{rho+o(1)}+Gamma_bEF^IU(pi)<N^{1+epsilon-o(1)}, then LB_N(1+epsilon) is false. This is a valid restricted proof-system result, not a P != NP proof.

## Definitions

- source object: H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), where x in {0,1}^N, M_N=N^{q+o(1)}, |G_N(x,j)|=(log N)^d with d>1, generator size is N^{rho+o(1)}, and LB_N(1+epsilon) asserts C(H_N^SAT)>N^{1+epsilon-o(1)} on valid lengths.
- target object: Psys_bEF^- proofs of LB_N using bit-explicit EF extension variables, SATeq links, bounded-SR_h rules, sparse-row residual patches, and interval-union FormulaEval-SAT rules, interpreted over nonuniform Boolean circuits of fan-in two.
- controlled interface: the parser traverses the extension-definition DAG, records occurrence dependencies, SATeq quotient links, bounded-SR_h leaf neighborhoods, interval-union RowSet indices, and residual error rows; it outputs K_idx(pi), Q_pi, and Gamma_bEF^IU(pi).
- target-preserving condition: SAT query length is polylogarithmic so beta=0, q,rho<1+epsilon, the parser is advice-free from the proof bits and N, and every FormulaEval-SAT selector is explicitly enumerable rather than a semantic oracle.

## Assumptions

- Model: nonuniform circuit size C(f) is measured over standard Boolean circuits; Psys_bEF^- proof lines have explicit bit encodings and no hidden semantic advice.
- Length regime: N ranges over the valid carrier lengths; q,rho,eta,tau,epsilon are fixed constants and all o(1) terms are uniform along this subsequence.
- Bounded-SR_h regime: each generated row has at most N^{eta+o(1)} SR leaves and each leaf occurrence-neighborhood transcript costs N^{tau+o(1)} bits/gates after local verifier normalization.
- FormulaEval regime: every interval-union selector lists O(N^{o(1)}) endpoints and RowSetEnumerator_N outputs exactly RowSet(a) in time and circuit size N^{o(1)} per row produced.
- Barrier status: the theorem is syntactic and relativizing for the restricted parser; full semantic FormulaEval-SAT is outside scope unless a nonrelativizing FE_Extract_N theorem supplies the missing row exposure.

## Equations

- carrier: `H_N^{\mathrm{SAT}}(x)=\bigoplus_{j<M_N}\mathrm{SAT}(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad |G_N(x,j)|=(\log N)^d`. Valid when: Valid when the source carrier is the beta-zero generated parity problem with polylogarithmic SAT instances and explicit generator bits.
- transcript_cost: `\Gamma_{bEF}^{IU}(\pi)=S_{dep}(\pi)+S_{link}(\pi)+B_{SR}(\pi)+N\,|RowSet_{FE}(\pi)|+E_NN`. Valid when: Applies after every EF, SATeq, bounded-SR_h, interval-union FormulaEval, and residual-error component has been parsed explicitly.
- bounded_SR_charge: `B_{SR}(\pi)\le N^{q+\eta+\tau+o(1)}`. Valid when: Requires the bounded self-reduction verifier to expose row indices, node paths, and touched occurrence neighborhoods with eta and tau overheads.
- parsed_upper_bound: `C(H_N^{\mathrm{SAT}})\le N^{\rho+o(1)}+\Gamma_{bEF}^{IU}(\pi)+N^{o(1)}`. Valid when: Applies after the parsed transcript and the generator circuit are composed without nonuniform leakage or semantic FormulaEval advice.
- LB_falsifier: `N^{\rho+o(1)}+\Gamma_{bEF}^{IU}(\pi)<N^{1+\epsilon-o(1)}\ \Longrightarrow\ \neg LB_N(1+\epsilon)`. Valid when: Valid when LB_N means the stated nonuniform circuit lower bound for the same carrier, lengths, and gate model.

## Attempted Derivation

- source_statement: LB_N(1+epsilon) is C(H_N^SAT)>N^{1+epsilon-o(1)} for the beta-zero parity carrier over valid N, with nonuniform circuits and no advice beyond circuit descriptions.
- target_statement: accepted Psys_bEF^-+IU proofs with subthreshold Gamma_bEF^IU(pi) imply an explicit circuit for H_N^SAT below the claimed lower bound, so they are falsified as certificates of LB_N.
- For each EF extension line e:=a op b, store D(e)=D(a) union D(b) plus the defining gate bit fields (line id, opcode, parent pointers, output bit); transitive DAG traversal charges S_dep(pi) once per reached occurrence dependency.
- For each SATeq link, store the two formula pointers, the equality-witness or syntactic rewrite code, and the affected row indices; quotienting charges S_link(pi) but does not create free hidden rows.
- For each bounded-SR_h rule, use verifier fields (rule tag, parent line, row index j in [M_N], node path u of length <=h, branch variable id, child formula pointers, leaf solver id, touched occurrence-neighborhood list, local accept bit). The local verifier recomputes the child clauses and checks that every touched bit is in the listed neighborhood.
- The SR_h line induction shows that replacing every SR rule by its leaf-neighborhood transcript preserves the line's Boolean value on all rows already in K_idx; the total charge is B_SR(pi)<=N^{q+eta+tau+o(1)} because there are N^{q+o(1)} rows, N^{eta+o(1)} leaves per row, and N^{tau+o(1)} neighborhood cost per leaf.
- For each interval-union FormulaEval line, RowSetEnumerator_N expands endpoints into explicit row indices; the parser charges N per enumerated row, giving N|RowSet_FE(pi)| and preventing free symbolic occurrence completion.
- Residual disagreement on E_N rows is corrected by equality gates comparing x to each bad source row, costing E_NN; this is valid only for E_N<N^{epsilon-o(1)} in the falsifier regime.
- Composing the generator circuit of size N^{rho+o(1)} with the parsed transcript yields C(H_N^SAT)<=N^{rho+o(1)}+Gamma_bEF^IU(pi)+N^{o(1)}; if this is below N^{1+epsilon-o(1)}, the source lower-bound sentence is false in the same circuit model.
- Inference-quality status: source carrier, target proof model, reduction type (parser-to-circuit simulation), length regime, exponent regime, advice status, and barrier scope are explicit; pvsnp-symbolic-complexity-auditor should only recheck endpoint enumeration and eta/tau accounting.

Blocking gap: No remaining gap for Psys_bEF^- with transparent interval-union FormulaEval. Full Psys_sym remains blocked at FE_Extract_N^sem: a semantic FormulaEval rule may compute SAT facts over hidden selected formulas without outputting RowSet indices or occurrence neighborhoods.

## Falsifiers

- Subthreshold transcript falsifier: N^{rho+o(1)}+Gamma_bEF^IU(pi)<N^{1+epsilon-o(1)} gives an explicit circuit contradicting LB_N(1+epsilon).
- Private-row falsifier: semantic FormulaEval with an unenumerated selected row admits two oracle labelings agreeing on the transcript but flipping the parity output.
- q<epsilon enumeration falsifier: global row-expanded FormulaEval costs N^{1+q+o(1)}, below the lower-bound threshold when other terms are subthreshold.
- Nonuniform leakage falsifier: if eta or tau is supplied by advice rather than verifier-readable bit fields, Gamma_bEF undercounts the transcript and the theorem is invalid.
- Positive-beta transfer falsifier: any black-box target circuit substitution with query length n^beta yields exponent q+beta c+o(1), so all-exponent NP versus P/poly consequences are capped unless beta=0 or subpolynomial.

## Learning

Cycle 105 converts the promoted restricted packet into an auditable inference-quality theorem: Psys_bEF^- plus transparent interval-union FormulaEval has a valid parser-to-circuit falsifier with Gamma_bEF^IU, while full semantic FormulaEval is not merely hard or barrier-limited but blocked by the exact FE_Extract_N^sem private-row countermodel. The contribution is a paper-level parser/falsifier boundary, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for FormulaEval support density and selector transparency.`
- Rationale: The restricted theorem is valid, but the paper packet needs a concrete stress test distinguishing explicit interval-union expansion from semantic hidden-row FormulaEval before promoting claims about Psys_sym.
- Situation seed: Take H_N^SAT with M_N=N^q generated polylog SAT rows and add one FormulaEval-SAT rule whose RowSet is an interval union of size N^{q-delta}; compare it with a hidden selector of the same cardinality that withholds one row r from the parser.
- Varied variable: delta, the support-sparsification exponent in |RowSet|=N^{q-delta+o(1)}.
- Held-fixed controls: beta=0 polylogarithmic SAT query length and d>1 lookup-safety regime., Generator size N^{rho+o(1)} with rho<1+epsilon., Bit-explicit EF, SATeq, and bounded-SR_h rules with advice-free eta/tau accounting., Same nonuniform circuit gate model and same valid length subsequence for source and target statements.
- Expected observation: For transparent interval unions the expansion charge is N^{1+q-delta+o(1)} and crosses the falsifier threshold at q-delta<epsilon. For hidden selectors, even above that size, one private row can invalidate occurrence completion unless FE_Extract_N exposes r.
- Transfer certificate needed: A RowSetEnumerator_N proof for the selector class, plus a nonrelativizing FE_Extract_N certificate if the rule uses real SAT semantics rather than explicit row expansion.

## Next Experiment

Run the delta-varied interval-union selector audit: instantiate |RowSet|=N^{q-delta}, verify RowSetEnumerator_N gate cost, compute Gamma_bEF^IU at delta=q-epsilon +/- o(1), and test whether any proposed semantic selector supplies a valid FE_Extract_N certificate rather than triggering the private-row falsifier.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For the restricted fragment Psys_sym^infl, every FormulaEval-SAT atom whose proof-visible code enumerates all FE-influential rows is target-preserving: an accepted proof pi of LB_N(1+epsilon) yields an advice-free parsed transcript with charge Gamma_infl(pi). Hence N^{rho+o(1)}+Gamma_infl(pi)<N^{1+epsilon-o(1)} is a falsifier to the claimed lower-bound proof, and any sound proof must pay the induced support threshold.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with N=2^n, M_N=N^{q+o(1)}, uniform generator G_N of circuit size N^{rho+o(1)}, and polylogarithmic SAT instances.
- target object: LB_N(1+epsilon), the nonuniform SIZE statement Ckt(H_N^SAT)>N^{1+epsilon-o(1)}, not the global P != NP conjecture.
- controlled interface: a deterministic no-advice parser maps Psys_sym^infl proof lines to row indices, extension-DAG dependencies, SATeq links, bounded-SR_h neighborhoods, and FormulaEval influence rows.
- target-preserving condition: every FormulaEval-SAT line exposes selector code, evaluator code, and an influence-complete RowSet enumerator; every listed row is charged in E_N^* or expanded at N E_N^* cost.

## Assumptions

- Model: nonuniform Boolean circuits for H_N^SAT and bit-explicit EF+SATeq+bounded-SR_h plus FormulaEval-SAT proof lines for Psys_sym^infl.
- Regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, bounded-SR_h parameter h=N^{eta+o(1)}, selector-code size N^{sigma+o(1)}, and fixed epsilon>0.
- Uniformity/advice: the parser and RowSet enumerator are uniform polynomial-time in the displayed proof and use no semantic advice about SAT truth values.
- Soundness: the proof system proves the same lower-bound sentence LB_N(1+epsilon) that the transcript simulator refutes; no hidden semantic oracle line is permitted in this lemma.
- Naturalness boundary: if the transcript becomes a large constructive useful truth-table property, the natural-proofs pressure is valid; otherwise this lemma is only a proof-system transfer audit.

## Equations

- beta_zero_carrier: `H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j))`. Valid when: Valid when G_N is uniform, row encodings have polylogarithmic length, and H_N is the beta-zero SAT-parity source carrier.
- FE_influence_set: `I_FE(pi)={(a,j): a is a FormulaEval-SAT line of pi and row j can change its truth value under legal assignments}`. Valid when: Valid when FormulaEval atoms expose the selector and evaluator codes used by the verifier, so influence is a syntactic relation.
- charged_support: `K_idx^+(pi)=K_idx(pi) cup pr_2(I_FE(pi)); E_N^*=|I_FE(pi)|`. Valid when: Valid when every FE-influential row is either explicitly enumerated or charged by the expansion-aware parser.
- influence_gamma: `Gamma_infl(pi)=S_dep(pi)+S_link(pi)+N^{q+eta+tau+o(1)}+N^{q+tau+sigma+o(1)}+N E_N^*`. Valid when: Applies after the bounded-SR_h verifier, selector enumerator, and FormulaEval row expansions are all proof-visible and uniformly chargeable.
- upper_bound_falsifier: `Ckt(H_N^SAT) <= N^{rho+o(1)}+Gamma_infl(pi)`. Valid when: Requires the parsed transcript to cover every row dependency used by the proof and the generator circuit to be hardwired without advice leakage.
- soundness_pressure: `N^{rho+o(1)}+Gamma_infl(pi) >= N^{1+epsilon-o(1)}`. Valid when: Valid when pi is sound for LB_N(1+epsilon) and the transcript simulator is a target-preserving nonuniform circuit construction.
- support_density: `|K_idx(pi)|+E_N^* >= N^{epsilon-o(1)} and (|K_idx(pi)|+E_N^*)/M_N >= N^{epsilon-q-o(1)}`. Valid when: Applies when dependency, link, enumeration, and generator overhead terms are below the N^{1+epsilon} lower-bound threshold.

## Attempted Derivation

- Typed Psys_sym^infl lines with fields line_type, parent_ids, ext_var, gate_op, sat_atom_id, formula_ptr, row_index, selector_code_id, evaluator_code_id, and optional FE_charge_id.
- Inherited the previous bEF parser for EF extension definitions, SATeq links, and bounded-SR_h occurrence neighborhoods, contributing S_dep(pi), S_link(pi), and N^{q+eta+tau+o(1)}.
- For a FormulaEval line a, defined FE influence syntactically: j is influential if changing the SAT bit of row j while holding other legal inputs fixed can change the verifier predicate for a.
- Required SelectorCode(a) and EvaluatorCode(a) to be proof-visible; the enumerator scans all j<=M_N and all visible selector states, adding every influential pair (a,j) to I_FE(pi).
- Charged selector enumeration by N^{q+tau+sigma+o(1)} and row expansion by N E_N^*, where E_N^*=|I_FE(pi)|; this prevents the prior hidden-selector undercharge.
- Performed line induction: every accepted line has its needed row dependencies inside K_idx(pi) cup pr_2(I_FE(pi)); extension parents add only S_dep, equality links add only S_link, and bounded-SR_h adds its local neighborhood term.
- Built the nonuniform simulator for H_N^SAT by hardwiring the generator G_N and the parsed transcript; this gives Ckt(H_N^SAT)<=N^{rho+o(1)}+Gamma_infl(pi).
- Compared with LB_N(1+epsilon). If the right side is below N^{1+epsilon-o(1)}, the accepted proof is unsound; if soundness is retained, the support-density pressure |K_idx|+E_N^*>=N^{epsilon-o(1)} follows after lower-order terms are subtracted.

Blocking gap: The derivation is complete only for Psys_sym^infl. For unrestricted real FormulaEval-SAT, RealSATInfluenceRealizer_N is unproved; hidden semantic row choice remains a valid falsifier.

## Falsifiers

- Unread-enable-bit FormulaEval: RowSet_surf(a)=empty while a depends on SAT(G_N(x,j*)).
- Hidden-selector code with identical displayed proof bits but different semantic row j*; no advice-free parser can be valid for both.
- Shared-DAG real-SAT composition where formula equality hides which generator row supplies the SAT bit.
- q<epsilon source-ceiling falsifier: C(H_N^SAT)<=N^{1+q+o(1)} contradicts any claimed N^{1+epsilon-o(1)} lower bound before proof-system issues matter.
- Natural-property falsifier: if the transcript induces a poly(N)-constructive polynomial-density property useful against the same SIZE class, PRF tension applies unless non-largeness or nonconstructivity is certified.

## Learning

Cycle 105 converts the FormulaEval boundary into a theorem/countermodel split. Live pvsnp_inference_quality packet: source_statement=accepted Psys_sym^infl proof pi of LB_N(1+epsilon) for H_N^SAT with M_N=N^{q+o(1)}; target_statement=Gamma_infl transcript, upper-bound falsifier, and support-density pressure; model_context=nonuniform Boolean SIZE, beta-zero SAT-parity carrier, EF+SATeq+bounded-SR_h plus influence-complete FormulaEval, simulation/extraction rather than many-one reduction; quantifier_context=N=2^n, |pi|=N^{tau+o(1)}, h=N^{eta+o(1)}, selector size N^{sigma+o(1)}, generator size N^{rho+o(1)}, no advice; derivation_status=restricted theorem derived, full Psys_sym blocked at RealSATInfluenceRealizer_N; reviewer findings=valid for influence-complete transparent FE, invalid for opaque semantic FE by unread-enable-bit falsifier, and not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for RealSATInfluenceRealizer_N.`
- Rationale: The branch has already proved transparent selector fragments; the remaining question is whether real FormulaEval semantics can hide influence rows while preserving the same lower-bound target.
- Situation seed: A Psys_sym proof of LB_N(1+epsilon) contains one FormulaEval-SAT atom A_b that evaluates OR_{j<=M_N}(e_j(b) AND SAT(G_N(x,j))) where the displayed selector code is fixed but the enable predicate e_j(b) is semantic and not written in the proof.
- Varied variable: alpha, where the number of hidden enabled influential rows is h_N=N^{alpha+o(1)}.
- Held-fixed controls: H_N^SAT, M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and the target statement LB_N(1+epsilon)., Proof length |pi|=N^{tau+o(1)}, bounded-SR_h parameter h=N^{eta+o(1)}, and no-advice deterministic parser requirement., The verifier accepts the same FormulaEval truth condition; only visibility of enabled rows is varied.
- Expected observation: For alpha=0 a single unread row already refutes surface occurrence completion; for alpha>=epsilon the influence charge E_N^* restores the required support pressure but only if those rows are enumerable. Thus hidden influence is a countermodel, while visible influence is merely expensive.
- Transfer certificate needed: A RealSATInfluenceRealizer_N theorem proving Infl_sem(a) subseteq EnumRows_N(a) uniformly within N^{q+tau+sigma+o(1)}, or a formal semantic-oracle classification showing the rule is outside the parser theorem.

## Next Experiment

Formalize the smallest real-SAT hidden-influence atom in the selected Psys_sym syntax: one FormulaEval line, one shared formula pointer, one semantic enable bit, and two assignments with identical displayed proof bits but different influential row j*. If this atom is legal, quarantine unrestricted Psys_sym; if illegal, extract the rule forbidding it as RealSATInfluenceRealizer_N's first axiom.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Certified guarded-dDNNF RowSetEnumerator_N theorem: in Psys_sym^gDNNF, a FormulaEval-SAT line whose row selector A_N has size S_N and selected-row count T_N is transparent only after paying S_N N^{o(1)}+T_N M_N N^{o(1)}; thus it cannot be a free semantic shortcut in the beta-zero transcript.

## Definitions

- source object: a bit-encoded guarded deterministic decomposable NNF row selector A_N on n=ceil(log N) row bits, with size S_N, syntactic guard cubes at OR gates, and explicit variable-set certificates at AND gates.
- target object: the FormulaEval-SAT contribution to a beta-zero transcript for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), where M_N=N^{q+o(1)} and G_N is uniform polylog-length.
- controlled interface: RowSetEnumerator_N(A_N) must output every selected row x exactly once, then the parser expands the M_N surface SAT occurrences attached to that row.
- target-preserving condition: the selector, enumerator, and formula generator are E-uniform and advice-free, and the rule manipulates surface occurrence encodings rather than an unparsed SAT semantic oracle.
- guarded OR gate: each child is conjoined with an explicit literal cube, and different child guard cubes are syntactically inconsistent.
- decomposable AND gate: child variable sets are explicitly listed and pairwise disjoint, so child assignments combine by Cartesian product without conflict.

## Assumptions

- Model: Psys_sym^gDNNF treats A_N as a proof line or extension object with checkable bit fields, not as an oracle for membership in RowSet(A_N).
- Regime: N tends to infinity, M_N=N^{q+o(1)}, S_N<=N^{O(1)}, T_N=|RowSet(A_N)|, and each generated SAT formula has length N^{o(1)}.
- Uniformity/advice: the selector DAG, guard certificates, variable-set lists, enumeration order, and G_N are generated without advice.
- Same-theory condition: FormulaEval expands the actual surface formulas G_N(x,j); semantically equivalent replacements require witnessed quotient evidence and are charged separately.
- Cutoff: the lemma is a restricted transparent-selector theorem; it does not cover arbitrary AC0, membership-only circuits, or semantic d-DNNF determinism without a certificate.

## Equations

- parameter_regime: `M_N=N^{q+o(1)},\quad S_N=N^{s+o(1)},\quad T_N=|RowSet(A_N)|=N^{t+o(1)}`. Valid when: Valid when N tends to infinity with fixed exponent parameters and the selector family is E-uniform.
- enumeration_time: `Time(RowSetEnumerator_N(A_N))\le (S_N+T_N)(\log N)^{O(1)}`. Valid when: Applies when A_N is a syntactically certified guarded decomposable deterministic selector with explicit gate-variable sets.
- formulaeval_charge: `\Gamma_{FE}^{gDNNF}(A_N)\le S_N N^{o(1)}+T_N M_N N^{o(1)}`. Valid when: Requires emitted rows to be expanded into surface FormulaEval calls for all M_N generated SAT formulas, with no semantic oracle substitution.
- exponent_charge: `\Gamma_{FE}^{gDNNF}(A_N)\le N^{\max\{s,t+q\}+o(1)}`. Valid when: Valid when q, s, and t are fixed exponent parameters and all formula lengths are N^{o(1)}.
- transcript_falsifier_threshold: `\gamma_{tot}=\max\{\rho,\gamma_{bEF},s,t+q\};\quad \gamma_{tot}<1+\epsilon\Rightarrow LB_N(1+\epsilon)\text{ is false for this transcript}`. Valid when: Applies after the Psys_bEF parser has already supplied a valid Gamma_bEF ledger and the generator overhead is advice-free.

## Attempted Derivation

- Fix n=ceil(log N). Encode each guarded-dDNNF gate with type, child pointers, Var(g), and for OR gates a guard cube per child; for AND gates require pairwise disjoint child variable sets.
- Define Enum(g,p). Literal and cube gates extend p. AND gates recursively combine child outputs by Cartesian product over disjoint variable sets. OR gates iterate guarded children; inconsistent guards ensure no duplicate complete row can arise across children.
- Induct on the selector DAG: Enum(g,p) emits exactly the satisfying completions of g extending p, each once. The output work is charged to visited gates plus emitted rows, giving (S_N+T_N)(log N)^{O(1)} after memoized gate traversal and lexicographic free-variable expansion.
- For each emitted row x, expand the M_N surface formulas G_N(x,j) and their SAT labels. Because G_N has polylog length and is uniform, per-row expansion costs M_N N^{o(1)}.
- Add selector verification cost S_N N^{o(1)} and the already parsed Gamma_bEF(pi). If N^{rho+o(1)}+Gamma_bEF(pi)+Gamma_FE^{gDNNF}(A_N)<N^{1+epsilon-o(1)}, the transcript itself constructs a smaller circuit for H_N^SAT, so the asserted LB_N(1+epsilon) is falsified in this restricted model.

Blocking gap: The derivation does not verify semantic determinism for arbitrary d-DNNF; it proves the theorem only for syntactically guarded deterministic decomposable selectors whose disjointness and variable-set data are bit-checkable.

## Falsifiers

- An OR gate whose children overlap semantically but lack syntactic inconsistent guards can duplicate or hide rows, invalidating the output-sensitive charge.
- A nondecomposable AND gate can require solving consistency among child assignments; the enumerator proof no longer has the Cartesian-product induction.
- A membership-only selector of size N^s for a scattered row set may have no output-sensitive enumerator; treating it as transparent is a semantic-oracle error.
- A selector with nonuniform row advice can name hard rows without giving an E-uniform language; this triggers the advice-leakage falsifier.
- If FormulaEval touches fewer than the certified emitted rows, an unread eval-critical bit gives the private-row countermodel.
- If max{rho,gamma_bEF,s,t+q} is not below 1+epsilon, the upper-bound contradiction does not fire; the route has only a charge theorem, not a lower-bound consequence.

## Learning

Cycle 105 adds a new paper-level transparent selector class: guarded deterministic decomposable NNF. The contribution is the exact FormulaEval charge S_N+T_N M_N up to N^{o(1)}, plus a sharper falsifier for semantic or membership-only selectors. This advances the parser/FormulaEval obstruction theorem only, not the main P vs NP conjecture.

## Gedanken Experiment Design Seed

- Need decision: `use-now-as-falsifier-probe`
- Rationale: The live issue is whether FormulaEval is a transparent row expansion or a hidden semantic selector. A concrete selector comparison tests the exact scan-vs-enumeration threshold instead of restating the FormulaEval boundary.
- Situation seed: Beta-zero SAT parity H_N^SAT with M_N=N^{q+o(1)}. Compare two selectors for the same scattered T_N=N^{t+o(1)} row set: one is a certified guarded-dDNNF of size S_N=N^{s+o(1)}, the other is only a succinct membership circuit with no enumerator certificate.
- Varied variable: the guarded decomposition size exponent s
- Held-fixed controls: q, t, rho, epsilon, and the polylog-uniform generator G_N are fixed., No selector advice and no unwitnessed SAT extensionality are allowed., FormulaEval must expand surface occurrences G_N(x,j) for emitted rows., The prior Psys_bEF Gamma_bEF parser ledger is treated as already valid.
- Expected observation: The guarded-dDNNF selector pays exponent max{s,t+q}, while the membership-only selector pays scan exponent 1+q or becomes a semantic-oracle/private-row case. The observation identifies the exact threshold where the transcript falsifier can be valid.
- Transfer certificate needed: A bit-checkable duplicate-free RowSetEnumerator_N certificate: guard inconsistency at OR gates, decomposable variable-set lists at AND gates, E-uniform enumeration order, and equality between emitted rows and surface FormulaEval occurrences.

## Next Experiment

Write the bit fields for a Psys_sym^gDNNF FormulaEval line: gate table, child pointers, guard cubes, Var(g) lists, root free-variable expansion, emitted-row checksum, and the Gamma_FE derivation; then test whether the same format subsumes the prior ROBDD enumerator without increasing the exponent.
