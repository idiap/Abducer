# cycle-0095

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: bit-explicit parser and FormulaEval boundary

## Candidate Lemma

For beta-zero SAT parity carriers, every accepted bit-explicit EF+SATeq+bounded-SR_h proof pi whose extension variables are defined by explicit bit DAGs parses into a charged occurrence transcript of cost Gamma_bEF(pi). Therefore C(H_N^SAT) <= N^{rho+o(1)}+Gamma_bEF(pi); if this is below N^{1+epsilon-o(1)}, the source lower-bound sentence LB_N(1+epsilon) is false, so such a pi is a valid falsifier of the claimed lower bound rather than evidence for P != NP.

## Definitions

- source object: H_N^SAT(x)=XOR_{j<=M_N} SAT(G_N(x,j)), where x has length N, M_N=N^{q+o(1)}, G_N has batched circuit size N^{rho+o(1)}, and each generated formula has length L_N=(log N)^d.
- target object: the source statement LB_N(1+epsilon) means nonuniform Boolean circuit size C(H_N^SAT)>N^{1+epsilon-o(1)}; target-class consequences are only beta-zero transfer consequences and are not asserted here.
- controlled interface: Psys_bEF is EF with fan-in-two bit-explicit extension definitions, SATeq links between explicitly encoded formulas, bounded self-reduction rules SR_h with frontier exponent tau and leaf-solver overhead exponent eta, and a deterministic advice-free verifier reading pi.
- target-preserving condition: beta=0, q,rho<1+epsilon, all parser charges are uniform in N, no FormulaEval-SAT semantic oracle is primitive, and the only nonuniformity allowed in the upper bound is the circuit family constructed from pi.

## Assumptions

- Bit encodings are self-delimiting and uniform: a formula bit, variable index, row index, and extension-variable definition are recoverable in polylog(N) time from pi and N.
- Every EF extension variable e_a is defined by an explicit acyclic Boolean definition over input bits, row-index bits, constants, and earlier extension variables; there is no implicit comprehension over all rows.
- SATeq axioms identify SAT labels only through listed formula encodings and listed equivalence links; the parser charges the transitive closure of such links as S_link.
- The bounded-SR_h rule unfolds at most N^{tau+o(1)} frontier leaves per row and invokes only leaf procedures with total overhead N^{eta+o(1)} per frontier unit in the stated model.
- Exceptional residual rows are explicitly bounded by E_N, and equality patching a row predicate on N-bit inputs costs O(N) gates per exceptional row.
- All o(1) terms are uniform for fixed q,rho,d,eta,tau,epsilon and for proof length bounded by N^{O(1)} in the verifier model.

## Equations

- carrier: `M_N = N^{q+o(1)}, L_N = (log N)^d, H_N^SAT(x) = XOR_{j<=M_N} SAT(G_N(x,j))`. Valid when: Valid when the beta-zero carrier has polylogarithmic formula length and the batched generator parameters are fixed independently of target SAT circuit exponent c.
- parser_charge: `Gamma_bEF(pi) = S_dep(pi) + S_link(pi) + N^{q+eta+tau+o(1)} + E_N N`. Valid when: Valid when extension dependencies, SATeq links, bounded self-reduction frontiers, and exceptional residual rows are all parsed from bit-explicit proof lines.
- transcript_upper_bound: `C(H_N^SAT) <= N^{rho+o(1)} + Gamma_bEF(pi)`. Valid when: Applies after the parsed transcript computes the nonexceptional row parities and equality patching covers exactly the declared residual row set.
- source_falsifier: `N^{rho+o(1)} + Gamma_bEF(pi) < N^{1+epsilon-o(1)} => not LB_N(1+epsilon)`. Valid when: Requires the source lower-bound model to be nonuniform circuit size for H_N^SAT and the constructed transcript circuit to be valid for all N-bit inputs.

## Attempted Derivation

- Define Psys_bEF lines as bit strings with typed tags: EF extension definition, SATeq link, bounded-SR_h invocation, Boolean inference, and final lower-bound certificate line.
- Traverse the EF extension DAG in topological order. For each extension variable, record whether its definition depends on x bits, row-index bits, previous charged variables, or constants; add the transitive charged definitions to S_dep(pi).
- For each SATeq link, normalize the two explicitly encoded formulas, charge the row/formula selectors and link witnesses to S_link(pi), and merge only the listed quotient classes.
- For each bounded-SR_h line, unfold the allowed self-reduction tree to its declared frontier, charge N^{tau+o(1)} frontier leaves and N^{eta+o(1)} leaf-solver overhead per row block, giving the term N^{q+eta+tau+o(1)}.
- Build a nonuniform circuit for the transcript: compute the batched generator with size N^{rho+o(1)}, evaluate charged extension/link/SR components, XOR the nonexceptional row labels, and patch E_N exceptional rows by equality tests costing O(E_N N).
- Conclude C(H_N^SAT)<=N^{rho+o(1)}+Gamma_bEF(pi). Comparing with LB_N(1+epsilon) gives the falsifier theorem whenever the right side is subthreshold.
- Test Psys_sym by adding one symbolic FormulaEval-SAT rule. The previous traversal cannot assign row support to the rule unless it is expanded into fixed-row instances; otherwise a private unexpanded-row labeling preserves all surface occurrences while violating the semantic rule.

Blocking gap: The remaining named gap is FE_expand_N: prove that any sound use of symbolic FormulaEval-SAT either expands to Omega(N^{1+q-o(1)}) row charge or is explicitly outside the parser model as a semantic oracle. Psys_bEF itself is not blocked under the stated bit-explicit assumptions.

## Falsifiers

- falsifier: a parsed Psys_bEF transcript with N^{rho+o(1)}+Gamma_bEF(pi)<N^{1+epsilon-o(1)} gives an explicit small circuit for H_N^SAT and invalidates LB_N(1+epsilon).
- falsifier: q<epsilon makes full row enumeration cost N^{1+q+o(1)}, below the claimed source threshold.
- falsifier: primitive symbolic FormulaEval-SAT with sub-N^{1+q} charge defeats surface occurrence completion by private unexpanded-row label changes.
- falsifier: nonuniform leakage through undeclared EF extension support invalidates any parser that is not bit-explicit or support-declared.

## Learning

Cycle 95 upgrades cycle 94 from a parser slogan to a restricted theorem packet: Psys_bEF proofs with bit-explicit EF support have a valid charged transcript and a concrete LB_N falsifier inequality. The surviving strong-system gap is exactly symbolic FormulaEval-SAT: row expansion costs N^{1+q-o(1)}, while free symbolic comprehension has a private-row countermodel to surface occurrence completion.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for Psys_sym FormulaEval-SAT.`
- Rationale: The abstract obstruction is already isolated; the remaining decision is whether symbolic FormulaEval-SAT can be charged without expanding N^{q+o(1)} row functions. A concrete row-index experiment tests exactly that transfer certificate.
- Situation seed: A Psys_sym proof has one line asserting FormulaEval-SAT for Phi_N(x,j)=G_N(x,j) for all j<=M_N, while the beta-zero parity carrier H_N^SAT keeps M_N=N^{q+o(1)}, L_N=(log N)^d, and generator size N^{rho+o(1)}.
- Varied variable: alpha, the exponent for the number N^{alpha+o(1)} of row indices explicitly instantiated from the symbolic FormulaEval-SAT line.
- Held-fixed controls: beta=0 and L_N=(log N)^d, so target SAT circuit substitution has no positive beta debt., The proof verifier is advice-free and sees the same pi for all inputs of length N., Row patching costs O(N) gates per exceptional row in the nonuniform circuit model., No additional MCSP, MKtP, or global natural-property carrier is introduced.
- Expected observation: If alpha<q, an unexpanded private row j* remains and surface occurrence completion is not valid; if alpha=q, the parser pays N^{1+q-o(1)} expansion charge, which usually exceeds the barely-superlinear source threshold when q>=epsilon.
- Transfer certificate needed: A formal FE_expand_N theorem: every sound symbolic FormulaEval-SAT use either has an explicit fixed-row expansion covering all semantic row classes or supplies a nonrelativizing certificate that implies the same row functions with a charged support lower bound.

## Next Experiment

Instantiate FE_expand_N on the smallest symbolic FormulaEval-SAT rule: one generator circuit G_N(x,j), one asserted vector y_j=SAT(G_N(x,j)), and alpha row instantiations. Prove the private-row countermodel for alpha<q and the N^{1+q-o(1)} expansion charge for alpha=q.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Restricted theorem packet: for bit-explicit Psys_bEF, every sound accepted proof pi of LB_N(1+epsilon) for the beta-zero SAT-parity carrier has a uniform advice-free parser producing row support K_idx(pi), exceptional rows E_N(pi), and a transcript of size at most N^{rho+o(1)}+Gamma_bEF(pi). If this is below N^{1+epsilon-o(1)}, the transcript is a concrete circuit upper-bound falsifier for the source lower-bound sentence, not a proof of P != NP.

## Definitions

- source object: H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)) on N=2^n truth-table inputs, with M_N=N^{q+o(1)}, generator circuit size N^{rho+o(1)}, and formula encodings of beta-zero length N^{o(1)}.
- target object: the nonuniform lower-bound sentence LB_N(1+epsilon) asserting C_bool(H_N^SAT)>N^{1+epsilon-o(1)} against unrestricted Boolean circuits on the same n-bit input slice.
- controlled interface: Psys_bEF is EF with canonical bit encodings, acyclic extension variables, SATeq axioms requiring displayed bitwise equality witnesses, and bounded-SR_h substitution/rewrite rules whose dependency cones are explicitly listed.
- target-preserving condition: the parser is uniform, advice-free, preserves N,q,rho,epsilon and the same H_N^SAT slice, and charges every SAT use through displayed formula bits or a named exceptional row.

## Assumptions

- Model: nonuniform Boolean circuits are the target; Psys_bEF is only a proof-system parser and gives no direct P-vs-NP conclusion.
- Length regime: N=2^n, M_N=N^{q+o(1)}, formula length N^{o(1)}, q,rho,epsilon are fixed constants up to o(1) losses.
- Uniformity/advice regime: the parser algorithm receives N, G_N, and pi, runs in poly(|pi|,N), and receives no row advice other than data written in pi.
- Proof-system regime: every SAT atom in Psys_bEF is either an original displayed generated formula, an SATeq image with bitwise equality proof, or a bounded-SR_h image with listed extension-DAG dependencies.
- Soundness regime: if the parsed transcript computes H_N^SAT with circuit size below the claimed lower-bound threshold, then LB_N(1+epsilon) is false on this slice.
- Naturalness boundary: the lemma is not asserting a large truth-table property unless the parser output can be recognized on arbitrary truth tables with polynomial density.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j<M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)}`. Valid when: Valid when H_N^{SAT} is the named beta-zero carrier with canonical row encodings and no advice.
- gamma_definition: `\Gamma_{bEF}(\pi)=S_{dep}(\pi)+S_{link}(\pi)+N^{q+\eta+\tau+o(1)}+E_N(\pi)N`. Valid when: Valid when Psys_bEF rules expose dependency cones, SATeq links, bounded rewrite overheads, and exceptional rows explicitly.
- transcript_upper_bound: `C_{bool}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{bEF}(\pi)`. Valid when: Applies after the advice-free parser compiles the same generated carrier and every charged transcript component.
- falsifier_inequality: `N^{\rho+o(1)}+\Gamma_{bEF}(\pi)<N^{1+\epsilon-o(1)}\;\Longrightarrow\;\neg LB_N(1+\epsilon)`. Valid when: Valid when the transcript is extension-sound and computes the same H_N^{SAT} slice targeted by LB_N.

## Attempted Derivation

- Define Psys_bEF lines as bit strings naming EF extension gates, formula encodings, row indices j, and SAT atoms; the verifier is polynomial time in |pi| and N and has no advice.
- For every proof line a, define Dep(a) as the transitive extension-DAG cone of formula bits on which a may depend. Acyclicity gives a topological induction and contributes S_dep(pi).
- For every SATeq step SAT(u)<->SAT(v), require an explicit bitwise equality derivation u=v; charge the equality proof and link endpoints to S_link(pi).
- For every bounded-SR_h step, expand only the listed h-neighborhood of substitutions; its global overhead is recorded as N^{q+eta+tau+o(1)} in the beta-zero row regime.
- Collect K_idx(pi) from all displayed generated-row tags reached by the dependency induction; collect E_N(pi) for parser failures, ambiguous encodings, or rules intentionally declared exceptional.
- Compile the parsed data with the generator of size N^{rho+o(1)}. Nonuniformly patch each exceptional row by an N-bit table. This yields the transcript upper bound N^{rho+o(1)}+Gamma_bEF(pi).
- Contrapose LB_N(1+epsilon): if the compiled transcript is smaller than N^{1+epsilon-o(1)}, it is a same-slice circuit upper bound and therefore a falsifier for the source lower-bound sentence.
- Derive |K_idx|>=N^{epsilon-o(1)} whenever the source LB is valid and all other Gamma terms are subthreshold; divide by M_N=N^{q+o(1)} to get the support-density trichotomy.
- Audit Psys_sym separately: FormulaEval-SAT as displayed syntax joins Psys_bEF; FormulaEval-SAT as semantic oracle gives the Occ_surf=1 versus |K_idx|=M_N countermodel and must pay N^{1+q+o(1)} expansion.

Blocking gap: Full Psys_sym remains blocked at FormulaEvalSATCharge_N: prove that semantic FormulaEval-SAT pays N^{1+q+o(1)} expansion, or accept the minimal opaque-extension countermodel as a no-go for surface occurrence completion.

## Falsifiers

- q<epsilon row-enumeration falsifier: C_bool(H_N^SAT)<=N^{1+q+o(1)} contradicts any claimed valid LB_N(1+epsilon).
- Opaque FormulaEval-SAT falsifier: one extension-coded SAT atom has surface occurrence one but semantic support M_N, invalidating occurrence completion.
- Advice-leakage falsifier: if K_idx(pi) is selected by external advice rather than parsed from pi, the transcript bound is not a valid uniform extraction.
- SATeq-without-bits falsifier: any equality axiom that omits bitwise formula equality destroys the bEF dependency induction.
- Natural-property falsifier: a dense poly(N)-constructive useful truth-table predicate induced by the parser conflicts with standard PRF pressure for the same circuit scale.

## Learning

Cycle 95 upgrades the support branch into a restricted theorem/countermodel packet: Psys_bEF has a bit-explicit parser with a derived Gamma_bEF transcript bound and q-density trichotomy, while Psys_sym with opaque FormulaEval-SAT is a precise semantic escape or countermodel. The progress is route-level validation and falsifier construction, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch needs a concrete quantitative test of whether the bEF parser preserves the lower-bound target or collapses into row enumeration; abstract barrier labels no longer distinguish q<epsilon, q=epsilon, and q>epsilon.
- Situation seed: Take a padded beta-zero SAT-parity family H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)) with canonical formula encodings and a Psys_bEF proof pi whose SATeq links form a shallow extension-DAG; compare it with a Psys_sym variant using one opaque FormulaEval-SAT atom.
- Varied variable: row exponent q in M_N=N^{q+o(1)}.
- Held-fixed controls: N=2^n and the same H_N^SAT target slice are held fixed., Generator size remains N^{rho+o(1)} with rho<1+epsilon., Formula length remains beta-zero, N^{o(1)}., Parser uniformity is advice-free and verifier resources are polynomial in |pi| and N., Target class is unrestricted nonuniform Boolean circuits at threshold N^{1+epsilon-o(1)}.
- Expected observation: For q<epsilon the row-enumeration circuit is already a falsifier; for q=epsilon+o(1) any valid proof must touch M_N/N^{o(1)} semantic rows; for q>epsilon the density lower bound weakens to N^{epsilon-q-o(1)} but absolute support remains N^{epsilon-o(1)}. The opaque FormulaEval-SAT variant should violate surface support at all q.
- Transfer certificate needed: A formal proof that the parser output computes the same H_N^SAT slice without advice, plus either a FormulaEval-SAT expansion-charge theorem or the opaque-extension countermodel quarantining semantic Psys_sym.

## Next Experiment

Instantiate a two-line Psys_sym opaque FormulaEval-SAT rule over z=Enc(G_N(x,j)) and prove formally that either expanding z over all (x,j) costs N^{1+q+o(1)} or the Occ_surf=1, |K_idx|=M_N countermodel refutes surface occurrence completion.

# MCSP / Meta-Complexity Carrier Transfer supporting bit-explicit parser boundary

## Candidate Lemma

Conditional parser theorem: for Psys_bEF=bit-explicit EF+SATeq_wit+bounded-SR_h, every accepted proof pi of LB_N(1+epsilon) for the beta-zero SAT-parity carrier yields an E-uniform occurrence transcript Q_pi and an unrestricted circuit upper bound C(H_N^SAT)<=N^{rho+o(1)}+Gamma_bEF(pi). Hence if this upper bound is below N^{1+epsilon-o(1)}, LB_N(1+epsilon) is false; this is a route-specific falsifier, not a proof of P != NP.

## Definitions

- source object: a Psys_bEF proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and bit-level encodings of the generated SAT formulas.
- target object: an occurrence transcript Q_pi, a parsed row-support set K_idx(pi), and an unrestricted Boolean circuit upper bound for the same H_N^SAT family.
- controlled interface: EF extension-DAG dependencies, witnessed SATeq quotient links, and bounded-SR_h substitution/reference rules are parsed into dependency cost S_dep, link cost S_link, surface-support cost, and exceptional-row patches.
- target-preserving condition: the parser is E-uniform and advice-free, every formula identity is witnessed or charged, bounded-SR_h has declared exponent tau, and no FormulaEval-SAT semantic oracle is used.
- Psys_bEF line types: input bit axioms, EF definitions y:=op(a,b), witnessed SATeq(F,F') links with checkable formula-code certificates, and bounded-SR_h rules referencing at most h=N^{tau+o(1)} surface occurrences per relevant row block.
- Gamma_bEF(pi): total transcript cost S_dep(pi)+S_link(pi)+N^{q+eta+tau+o(1)}+E_N N, where eta records line-local encoding overhead and E_N counts explicitly patched exceptional rows.

## Assumptions

- Length regime N tends to infinity; epsilon>0 is fixed; q,rho,eta,tau are constants or named o(1)-stable exponents.
- The generator G_N is E-uniform, has circuit size N^{rho+o(1)}, and outputs the row formula code for row j without advice.
- The target circuit model is unrestricted nonuniform Boolean circuits; the simulation is allowed to hardwire pi but not an unparsed hard-row selector.
- SATeq witnesses are bit-level objects checkable inside the proof verifier and their quotient-cover cost is included in S_link(pi).
- bounded-SR_h has no hidden semantic evaluation: every replacement path is reachable by transitive traversal of explicit extension-DAG pointers.
- FormulaEval-SAT, if present without witnesses, is excluded from Psys_bEF and moved to the Psys_sym semantic-boundary lemma.

## Equations

- carrier_definition: `H_N^{SAT}(x)=xor_{j<M_N} SAT(G_N(x,j)),  M_N=N^{q+o(1)}`. Valid when: Valid when G_N is an advice-free E-uniform generator and the row count exponent q is fixed for the length interval.
- transcript_cost: `Gamma_bEF(pi)=S_dep(pi)+S_link(pi)+N^{q+eta+tau+o(1)}+E_N N`. Valid when: Valid when EF dependencies, witnessed equality links, bounded surface references, and exceptional rows are the only parser resources used.
- parsed_upper_bound: `C(H_N^{SAT}) <= N^{rho+o(1)} + Gamma_bEF(pi)`. Valid when: Applies after the parsed transcript is composable with the E-uniform generator and no semantic FormulaEval oracle contributes uncharged information.
- lower_bound_falsifier_threshold: `N^{rho+o(1)}+Gamma_bEF(pi) < N^{1+epsilon-o(1)}  =>  not LB_N(1+epsilon)`. Valid when: Valid when LB_N(1+epsilon) means unrestricted circuit complexity above N^{1+epsilon-o(1)} for the identical H_N^{SAT} family.

## Attempted Derivation

- Define Psys_bEF lines as bit strings with tagged rule type, parent pointers, formula-code ranges, EF extension variables, and verifier checks; this fixes the source proof model and advice status.
- Set induction invariant I(t): after parsing the first t lines, every occurrence-relevant row-parity consequence has a transcript whose cost is bounded by accumulated S_dep+S_link+surface+exception terms.
- EF case: traverse the explicit acyclic extension-DAG from each row-relevant occurrence; add each newly reached gate/wire once to S_dep(pi), preserving uniformity because all pointers are verifier-visible.
- SATeq_wit case: verify the equality/equisatisfiability witness, union the quotient classes, and charge the witnessed link cover to S_link(pi); no unparsed formula identity is used.
- bounded-SR_h case: for M_N=N^{q+o(1)} rows, line-local overhead N^{eta+o(1)}, and h=N^{tau+o(1)} bounded references, the surface traversal contributes N^{q+eta+tau+o(1)}.
- Exception case: if E_N rows are not covered by the parser invariant, hardwire their row functions at cost E_N N, giving the final Gamma_bEF(pi).
- Compose Q_pi with the generator circuit G_N and an XOR tree to obtain C(H_N^SAT)<=N^{rho+o(1)}+Gamma_bEF(pi).
- Compare the upper bound with LB_N(1+epsilon); a strict subthreshold inequality is a valid falsifier of the claimed lower-bound instance, not a proof of the main conjecture.
- Run the live inference-quality handoff: source statement is Psys_bEF proof of LB_N; target statement is unrestricted circuit upper bound; reduction type is proof-transcript-to-circuit simulation; quantifiers are fixed epsilon and all large N; advice status is no advice except hardwired pi in the negative simulation.

Blocking gap: The conditional induction is blocked from paper promotion until the exact bit grammar for SATeq_wit certificates and bounded-SR_h references is written and checked; Psys_sym with uncharged FormulaEval-SAT remains a separate semantic-oracle countermodel unless UExtWitnessability is proved.

## Falsifiers

- falsifier: an unwitnessed FormulaEval-SAT line returns SAT(F_c) while the parser never expands the relevant formula-code bit, producing two occurrence-identical completions with different row parity.
- falsifier: a bounded-SR_h rule hides a global substitution whose affected rows are not reachable through explicit parent pointers and not counted in N^{q+eta+tau}.
- falsifier: K_idx(pi) is chosen by nonuniform hard-row advice rather than derived by the transcript parser, invalidating target-preserving extraction.
- falsifier: q<epsilon with per-row cost N^{1+o(1)} gives C(H_N^SAT)<=N^{1+q+o(1)}, so the proposed source lower bound is already below threshold.
- falsifier: SATeq witnesses certify only local occurrence equality while the proof uses full formula extensionality; then S_link undercounts the semantic quotient.

## Learning

Cycle 95 converts the prior witnessed/unwitnessed extensionality fork into a conditional parser induction with a concrete Gamma_bEF ledger. The route-level contribution is a valid finite falsifier theorem for low-cost Psys_bEF transcripts and a sharper FormulaEval-SAT expansion-or-oracle boundary; the unresolved work is bit-level verifier formalization and the minimal countermodel/expansion proof, not the main P != NP conjecture.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The branch is blocked at the concrete FormulaEval-SAT boundary; a target-preserving thought experiment can distinguish explicit expansion from semantic oracle power without broadening into MCSP folklore.
- Situation seed: Padded beta-zero SAT-query family with M_N=N^{q} rows where each G_N(x,j) contains a formula-code bit b_j toggling between a satisfiable gadget and an unsatisfiable gadget, and Psys_sym has one FormulaEval-SAT(c_j) line per row.
- Varied variable: coverage exponent beta for how many of the N^{1+q+o(1)} row-evaluation footprint bits are explicitly expanded or witnessed by the parser.
- Held-fixed controls: H_N^SAT, M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)}, and the claimed LB_N(1+epsilon) target are unchanged., No advice-selected hard row is allowed; the parser may use only proof-visible bits and witnessed quotient links., The target circuit model remains unrestricted Boolean circuits, and all upper-bound simulations hardwire only the fixed proof pi.
- Expected observation: If beta<1+q-o(1), an unexpanded toggling bit yields two completions agreeing on Q_pi but disagreeing on at least one FormulaEval-SAT value; if beta>=1+q-o(1), the semantic use is paid by the expansion charge and cannot beat the Gamma threshold.
- Transfer certificate needed: A formal indistinguishability/countermodel lemma for beta<1+q and an expansion-charge theorem for beta>=1+q before the intuition may change proof obligations.

## Next Experiment

Write the minimal bit-level Psys_bEF verifier grammar and prove the induction invariant for one bounded-SR_h line; in parallel instantiate the toggling-bit FormulaEval-SAT countermodel and compute whether its expansion charge is exactly N^{1+q+o(1)} or admits a smaller witnessed quotient.
