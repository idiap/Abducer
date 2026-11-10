# cycle-0099

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Let Psys_sym extend Psys_bEF by one symbolic FormulaEval-SAT mechanism ranging over rows R_N and slots [M_N] of the beta-zero SAT-parity carrier. Any advice-free occurrence parser that is valid for quotient-label spoof models either expands FormulaEval-SAT into Omega(|R_N| M_N L_N^{O(1)}) row-slot evaluation atoms, or it is falsified by a private-row countermodel preserving all surface SATeq and bounded-SR_h constraints while changing one H_N row. Hence unexpanded FormulaEval-SAT is a semantic-oracle escape, not a free Psys_bEF parser rule.

## Definitions

- source object: beta-zero SAT-parity carrier H_N^SAT(i)=xor_{j<=M_N} SAT(G_N(i,j)) on N source rows, M_N=N^{q+o(1)} slots, and formula length L_N=(log N)^{O(1)}.
- target object: parser-to-transcript theorem or countermodel for Psys_sym FormulaEval-SAT, yielding only a route-level lower-bound-certificate audit and not P != NP.
- controlled interface: symbolic FormulaEval-SAT proof mechanism -> row-slot occurrence transcript -> circuit upper bound or private-row falsifier.
- target-preserving condition: row and slot indices introduced by FormulaEval-SAT are either advice-free and charged in the transcript, or the mechanism is classified as a semantic oracle outside occurrence parsing.
- row-slot atom: a tuple (i,j,G_N(i,j),y_{i,j}) with y_{i,j} intended to equal SAT(G_N(i,j)).
- surface occurrence completion: closure under syntactically present EF dependencies, SATeq links, and bounded-SR_h leaves, excluding unexpanded universal FormulaEval comprehension.
- private-row countermodel: two quotient-label assignments that agree on the parser transcript closure but differ on one unmentioned row-slot label, changing the XOR value of H_N on that row.

## Assumptions

- Length regime: N tends to infinity, M_N=N^{q+o(1)}, L_N=(log N)^{d+o(1)}, and beta=0 so target SAT instance length is polylogarithmic in N.
- Circuit regime: generator cost is N^{rho+o(1)} and every transcript atom of polylogarithmic SAT length costs N^{o(1)} gates after substitution.
- Proof model: Psys_bEF has bit-explicit EF extension variables, explicit SATeq axioms, and bounded self-reduction depth h with costs already included in Gamma_bEF(pi).
- Psys_sym adds FormulaEval-SAT as exactly one of: expanded axiom schema, symbolic proof line, extension rule, or semantic oracle; the lemma classifies the non-expanded cases.
- Uniformity/advice status: the parser may use the public proof pi and public generator G_N but may not receive a hidden nonuniform list of row supports or SAT labels.
- Countermodel scope: the spoof model is a parser-soundness falsifier for occurrence completion, not a model of true SAT semantics; escaping it requires a nonrelativizing FE_Extract_N theorem.
- Same-theory condition: SATeq and bounded-SR_h constraints used by the proof must be preserved by the quotient-label assignments unless the corresponding atoms are charged.

## Equations

- slot_count: `M_N=N^{q+o(1)}`. Valid when: Valid when the beta-zero carrier family fixes q and all hidden factors are subpolynomial in N.
- carrier_row: `H_N^{SAT}(i)=\oplus_{j\le M_N} SAT(G_N(i,j))`. Valid when: Applies when row i is a public source row and every generated instance has polylogarithmic length.
- formulaeval_expansion_charge: `Ch_{FE}(R_N)\ge |R_N|\,M_N\,L_N^{O(1)}=|R_N|N^{q+o(1)}`. Valid when: Requires the FormulaEval-SAT mechanism to range over all slots for each charged row without hidden advice.
- full_row_expansion: `|R_N|=N^{1-o(1)}\Rightarrow Ch_{FE}(R_N)=N^{1+q+o(1)}`. Valid when: Valid when FormulaEval-SAT is a global row comprehension rather than a finite listed subclaim.
- parsed_upper_bound_with_FE: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{bEF}(\pi)+Ch_{FE}(R_N)+E_NN`. Valid when: Applies after the parser preserves EF dependencies, SATeq links, bounded-SR leaves, and sparse-row patching costs.
- source_LB_falsifier: `N^{\rho+o(1)}+\Gamma_{bEF}(\pi)+Ch_{FE}(R_N)+E_NN<N^{1+\epsilon-o(1)}\Rightarrow LB_N(1+\epsilon)\text{ is false}`. Valid when: Requires the parsed transcript to compute the same carrier H_N on all but E_N explicitly patched rows.

## Attempted Derivation

- Fix the quotient-label abstraction y_{i,j}=SAT(G_N(i,j)) after closing all explicitly charged SATeq and bounded-SR_h constraints from a Psys_sym proof pi.
- Run the Psys_bEF parser on the bit-explicit part of pi, obtaining S_dep, S_link, bounded-SR leaf cost, and sparse-row residual E_N.
- Classify each FormulaEval-SAT occurrence. If it is an expanded axiom schema over rows R_N and slots [M_N], add Ch_FE(R_N)>=|R_N|M_NL_N^{O(1)} to the transcript.
- If a FormulaEval-SAT line is symbolic and the parser charges o(|R_N|M_N) row-slot atoms, choose a row-slot (i*,j*) outside the transitive SATeq/SR_h closure of the transcript.
- Build two label assignments Y and Y' that agree on every charged atom and every explicit link, but differ at (i*,j*) and, if needed, one parity-completing uncharged atom in the same row.
- The surface transcript and proof-local occurrence constraints evaluate identically under Y and Y', while H_N^Y(i*) differs from H_N^{Y'}(i*). Thus occurrence completion cannot soundly certify the row parity or the lower-bound statement.
- Conclude the dichotomy: expanded FormulaEval pays N^{1+q+o(1)} for global row comprehension, while unexpanded FormulaEval must be declared a semantic oracle requiring a separate nonrelativizing FE_Extract_N theorem.

Blocking gap: The derivation does not rule out a real-SAT-specific, nonrelativizing FE_Extract_N theorem showing that true formula evaluation semantics force the missing labels without row-slot expansion. It only proves the surface-occurrence parser no-go and the expansion charge for explicit schemas.

## Falsifiers

- Private-row FormulaEval countermodel: an unexpanded symbolic FormulaEval line with sub-NM charged occurrences cannot be a valid occurrence parser because one unmentioned row-slot label can flip a carrier row.
- Subthreshold transcript falsifier: if N^{rho+o(1)}+Gamma_bEF(pi)+Ch_FE+E_NN<N^{1+epsilon-o(1)}, the claimed LB_N(1+epsilon) lower bound is false in the same circuit model.
- q<epsilon support falsifier: the required absolute FormulaEval support N^{epsilon-o(1)} exceeds the available M_N=N^{q+o(1)} slots, so row enumeration and patching collapse the source lower bound.
- Nonuniform leakage falsifier: any hidden advice list of row supports or SAT labels invalidates the target-preserving parser because it is not charged in Gamma_bEF or Ch_FE.
- Semantic-oracle escape falsifier for promotion: if FormulaEval-SAT is left unclassified, the proof packet is invalid for paper promotion even if the Psys_bEF subtheorem is correct.

## Learning

Cycle 99 converts the remaining Psys_sym ambiguity into a sharper theorem/countermodel fork. FormulaEval-SAT cannot be treated as a free occurrence-completion rule: an expanded schema pays N^{1+q+o(1)} row-slot charge, while an unexpanded symbolic line has a private-row falsifier unless a nonrelativizing FE_Extract_N theorem is supplied. The valid contribution is a scoped parser-boundary packet, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch is blocked at FE_Extract_N, so a concrete private-row thought experiment tests whether symbolic FormulaEval-SAT can be parsed without paying the N^{1+q} expansion charge.
- Situation seed: Take a Psys_sym proof with one symbolic FormulaEval-SAT line asserting evaluation of every generated formula G_N(i,j) for all N rows and M_N=N^{q+o(1)} slots, but whose surface transcript lists only o(NM_N) row-slot atoms.
- Varied variable: q, the slot exponent in M_N=N^{q+o(1)}, varied across q<epsilon, q=epsilon+o(1), and q>epsilon.
- Held-fixed controls: Formula length L_N=(log N)^{d+o(1)} with beta=0 target-query length., Generator cost N^{rho+o(1)} and advice-free public generation of G_N., Psys_bEF dependency, SATeq, and bounded-SR_h charges remain counted in Gamma_bEF(pi)., No hidden nonuniform row-support or label advice is allowed in the parser.
- Expected observation: For q<epsilon, absolute support already exceeds the slot universe and gives a row-enumeration falsifier; for q>=epsilon, a global FormulaEval comprehension must pay Ch_FE=N^{1+q+o(1)} or the private-row countermodel changes H_N while preserving the surface transcript.
- Transfer certificate needed: A valid influence on the proof queue requires either a formal expansion-charge theorem for the chosen FormulaEval rule or a nonrelativizing FE_Extract_N certificate explaining why the private label countermodel is impossible for true SAT semantics.

## Next Experiment

Write the formal FE_Extract_N blocked-lemma proof: define the quotient-label model after SATeq/SR_h closure, prove the unmentioned row-slot existence bound, construct the two assignments Y,Y', and verify that the carrier row parity changes while the parsed transcript remains identical.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Expansion-aware support trichotomy: for beta-zero SAT parity carriers, any accepted no-advice parsed proof of LB_N(1+epsilon) whose non-row charges are subthreshold must have expansion-aware semantic support |K_idx(pi)|+E_N >= N^{epsilon-o(1)}. Hence q<epsilon gives a row-enumeration falsifier for the source lower bound, q=epsilon+o(1) forces exponent-full semantic contact, and q>epsilon permits sparse density but still forces absolute support N^{epsilon-o(1)}.

## Definitions

- source object: H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), where x has N bits, M_N=N^{q+o(1)}, G_N is the beta-zero formula generator, and its generator circuit has size N^{rho+o(1)}.
- target object: LB_N(1+epsilon), the nonuniform Boolean SIZE statement C(H_N^SAT)>N^{1+epsilon-o(1)} on the same N-bit truth-table input length.
- controlled interface: a deterministic no-advice parser/enumerator for Psys_bEF or a charged Psys_sym fragment outputs K_idx(pi), dependency charge S_dep, link charge S_link, enumerator charge T_enum(pi), and FormulaEval expansion mass E_N.
- target-preserving condition: the transcript plus generator must construct an actual nonuniform circuit for H_N^SAT over the same N-bit input space, with no hidden row advice and no change of target class.
- K_idx(pi) is the set of generator rows whose SAT values are semantically inspected by the parsed proof transcript.
- E_N is the number of additional semantic rows covered by FormulaEval-SAT atoms that are not row-instantiated but are explicitly expanded or charged.

## Assumptions

- Length regime: N=2^n, M_N=N^{q+o(1)}, proof size |pi|=N^{tau+o(1)}, bounded semantic row arity h=N^{eta+o(1)}, and all o(1) terms are uniform over the chosen subsequence.
- Circuit model: target lower bounds and upper-bound falsifiers are for nonuniform Boolean circuits of size measured as a function of the N-bit input length.
- Proof model: Psys_bEF uses bit-level encodings, EF extension variables, SATeq axioms, and bounded-SR_h rules whose row references are syntactically recoverable by transitive extension-DAG traversal.
- Semantic model: Psys_sym is allowed only if each FormulaEval-SAT occurrence is classified as row-instantiated, explicitly expanded, or backed by RowSetEnumerator_N; otherwise the lemma is not valid for that occurrence.
- Subthreshold regime: N^{rho+o(1)}+S_dep+S_link+T_enum(pi)=o(N^{1+epsilon}) unless the displayed overhead itself already refutes the claimed route parameters.
- Soundness boundary: the lemma gives a route-level falsifier for the claimed source lower bound, not a proof of P != NP or a consequence for arbitrary proof systems.

## Equations

- row_count: `M_N=N^{q+o(1)}`. Valid when: Valid when the beta-zero generator family and row-index length convention are fixed before parsing the proof.
- expansion_aware_transcript_bound: `C(H_N^{SAT}) \le N^{\rho+o(1)}+S_{dep}+S_{link}+T_{enum}(\pi)+N\bigl(|K_{idx}(\pi)|+E_N\bigr)`. Valid when: Applies after the no-advice parser and residual-completion argument preserve the N-bit target circuit model.
- bEF_instantiation: `\Gamma_{bEF}(\pi)=S_{dep}+S_{link}+N^{q+\eta+\tau+o(1)}+E_NN`. Valid when: Valid when Psys_bEF row references are recovered by bit-DAG traversal with proof length N^{tau+o(1)} and row arity N^{eta+o(1)}.
- support_pressure: `|K_{idx}(\pi)|+E_N \ge N^{\epsilon-o(1)}`. Valid when: Requires LB_N(1+epsilon) to be valid and all generator, dependency, link, and enumeration overheads to stay subthreshold.
- density_pressure: `\frac{|K_{idx}(\pi)|+E_N}{M_N} \ge N^{\epsilon-q-o(1)}`. Valid when: Follows only after substituting M_N=N^{q+o(1)} into the expansion-aware support-pressure inequality.

## Attempted Derivation

- Define K_idx^+(pi)=K_idx(pi) union F(pi), where F(pi) is the charged set of rows induced by non-row-instantiated FormulaEval-SAT atoms; set |F(pi)|=E_N after de-duplication.
- Run the bit-explicit parser for Psys_bEF, or assume RowSetEnumerator_N for the named Psys_sym fragment, to obtain S_dep, S_link, T_enum(pi), and K_idx^+(pi) without advice.
- Use the residual-completion construction: the generator circuit supplies the base N^{rho+o(1)} part, dependency/link gadgets supply S_dep+S_link, enumeration supplies T_enum(pi), and each charged semantic row costs at most N in the resulting nonuniform circuit.
- If the constructed circuit size is below N^{1+epsilon-o(1)}, then LB_N(1+epsilon) for H_N^SAT is false; this is the transcript upper-bound falsifier theorem, not a main-conjecture claim.
- Assuming LB_N(1+epsilon) is valid and non-row overheads are subthreshold, rearrange the circuit upper bound to force |K_idx(pi)|+E_N >= N^{epsilon-o(1)}.
- Substitute M_N=N^{q+o(1)} to get density at least N^{epsilon-q-o(1)}, yielding q<epsilon source falsification by complete row enumeration, q=epsilon+o(1) exponent-full contact, and q>epsilon weakened density with absolute support pressure.
- Barrier audit: if the parser also yields a poly(N)-constructive dense property useful against the same SIZE target, natural-proof PRF tension is triggered; otherwise the result remains a route-specific proof-system falsifier.

Blocking gap: Unrestricted Psys_sym remains blocked at RowSetEnumerator_N: a semantic FormulaEval-SAT atom may define its row set without a uniform, advice-free, output-sensitive enumerator.

## Falsifiers

- q<epsilon is a source-level falsifier because C(H_N^SAT)<=N^{1+q+o(1)} already beats the claimed N^{1+epsilon-o(1)} lower bound.
- A single free-index FormulaEval-SAT atom is a finite falsifier to surface occurrence parsing: O_surf=1 while semantic support is M_N.
- Hidden row advice in RowSetEnumerator_N invalidates the no-advice transcript and destroys target preservation.
- If T_enum(pi) or N E_N is already >=N^{1+epsilon-o(1)}, the parser theorem gives no subthreshold contradiction and only records expansion cost.
- If the induced property is large, poly(N)-constructive, and useful against the exact target SIZE class, the natural-proofs PRF conflict becomes the relevant no-go family.
- If SATeq or bounded-SR_h rules use shared formula-DAG equality not recoverable at bit level, the Psys_bEF parser assumptions fail.

## Learning

Cycle 99 upgrades the support work by replacing vague FormulaEval mass with K_idx^+(pi)=K_idx(pi) plus charged E_N and deriving the exact support threshold |K_idx|+E_N>=N^{epsilon-o(1)}. This proves the q-trichotomy for row-faithful bEF and isolates RowSetEnumerator_N as the only unrestricted Psys_sym gap. The result is valid route-level proof-system certification and falsifier construction, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and threshold calibration for RowSetEnumerator_N.`
- Rationale: The branch needs a concrete complexity-theoretic case distinguishing harmless FormulaEval syntax from semantic row leakage; another abstract barrier restatement would not close the proof-delivery queue.
- Situation seed: Take a padded beta-zero SAT-query parity family H_N^SAT with M_N=N^q rows, and add one Psys_sym FormulaEval-SAT line whose selector R_e covers exactly N^e generator rows but is displayed as one proof atom.
- Varied variable: The semantic row-mass exponent e where E_N=N^e.
- Held-fixed controls: Keep N-bit target length, nonuniform SIZE measurement, and LB_N(1+epsilon) unchanged., Keep generator size N^{rho+o(1)} with rho<1+epsilon., Keep proof length N^{tau+o(1)} and bounded row arity N^{eta+o(1)} subthreshold., Forbid nonuniform row advice in the parser/enumerator.
- Expected observation: For e<epsilon and subthreshold overhead, the transcript gives a circuit upper-bound falsifier to LB_N(1+epsilon); for e>=epsilon the FormulaEval atom pays enough expansion mass to avoid contradiction; if R_e is not uniformly enumerable, the route is blocked at advice-free semantic extraction.
- Transfer certificate needed: A formal RowSetEnumerator_N certificate: from the bit-level FormulaEval line and N, uniformly list all semantically relevant generator rows or prove that the atom is an oracle-like semantic escape outside the parser theorem.

## Next Experiment

Attempt RowSetEnumerator_N for a concrete Psys_sym^sel fragment where FormulaEval selectors are interval unions or AC0 predicates over the row index; compute E_N, T_enum, and the exact e<epsilon falsifier threshold, or output the smallest selector countermodel showing unavoidable semantic advice.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Conditional parser theorem: every valid Psys_bEF^- proof pi of the beta-zero lower-bound sentence for H_N^SAT admits an advice-free occurrence transcript Q_pi with cost Gamma_bEF(pi); hence C(H_N^SAT)<=N^{rho+o(1)}+Gamma_bEF(pi). If this upper bound is below N^{1+epsilon-o(1)}, the asserted LB_N(1+epsilon) is false in the same nonuniform circuit model.

## Definitions

- source object: a bit-explicit Psys_bEF^- proof pi over EF extension variables, SATeq witnessed equality axioms, and bounded-SR_h syntactic rewrite rules, for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)).
- target object: an occurrence transcript Q_pi plus a nonuniform Boolean circuit upper bound for the N-bit truth table H_N^SAT.
- controlled interface: line annotations A_l=(D_l,L_l,K_l,X_l) recording extension dependencies, equality links, semantically contacted SAT-query indices, and exceptional rows.
- target-preserving condition: every SAT fact used by pi is either a generator occurrence or a witnessed SATeq consequence, and each SR_h rewrite expands to explicit bit links without FormulaEval-SAT semantic shortcuts.
- Psys_bEF^- excludes unwitnessed SAT extensionality and excludes any rule deriving SAT(F) from formula semantics without a bit-level witness.
- S_dep counts extension-DAG dependency bits, S_link counts witnessed formula-equality links, E_N N counts exceptional row patches, and h_N=N^{tau+o(1)} is the SR_h local expansion bound.

## Assumptions

- Length regime: N is the truth-table length, M_N=N^{q+o(1)}, proof length T(pi)=N^{eta+o(1)}, and all exponents q,rho,eta,tau,epsilon are fixed constants or have named o(1) slack.
- Circuit model: the target lower bound LB_N(1+epsilon) is against unrestricted nonuniform Boolean circuits of size N^{1+epsilon-o(1)}.
- Uniformity/advice status: G_N and the parser are E-uniform and advice-free; the fixed proof pi may be hardwired only when deriving a nonuniform upper-bound falsifier.
- Rule model: SATeq lines carry explicit bitwise equality or quotient witnesses; bounded-SR_h lines list their touched occurrence sites or provide an E-uniform iterator with h_N local expansion.
- Naturalness/barrier status: the theorem is a negative low-transcript falsifier, not a large constructive useful property and not a proof of P != NP.

## Equations

- parameter_ledger: `M_N=N^{q+o(1)},\quad T(\pi)=N^{\eta+o(1)},\quad h_N=N^{\tau+o(1)}`. Valid when: Valid when N is the truth-table length and the proof family has fixed exponent bounds for queries, lines, and SR_h locality.
- gamma_definition: `\Gamma_{bEF}(\pi)=S_{dep}(\pi)+S_{link}(\pi)+N^{q+\eta+\tau+o(1)}+E_NN`. Valid when: Valid when extension dependencies, witnessed equality links, bounded rewrites, and exceptional rows are charged in the Psys_bEF^- annotation ledger.
- transcript_bound: `|Q_\pi|\le \Gamma_{bEF}(\pi)\cdot N^{o(1)}`. Valid when: Applies after the parser expands every bounded-SR_h step and contracts only witnessed equality quotients with explicit bit links.
- circuit_upper_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{bEF}(\pi)\cdot N^{o(1)}`. Valid when: Requires the generator G_N to be E-uniform of size N^{rho+o(1)} and the parsed transcript to determine row parity outside declared exceptions.
- lower_bound_falsifier: `N^{\rho+o(1)}+\Gamma_{bEF}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Valid when LB_N is stated for the same unrestricted nonuniform circuit model used by the transcript simulation upper bound.

## Attempted Derivation

- Define Psys_bEF^- lines as bit strings encoding EF definitions, witnessed SATeq axioms, bounded-SR_h rewrites, Boolean inference, and the final LB_N sentence; FormulaEval-SAT is not a rule of this restricted system.
- Annotate every line l by A_l=(D_l,L_l,K_l,X_l): D_l is the set of extension-definition bits needed to reconstruct the line, L_l is the witnessed equality-link set, K_l is the SAT-query support touched by the line, and X_l is the declared exceptional row set.
- Base EF definitions add only their input dependency bits to S_dep; Boolean inference unions annotations and adds no semantic SAT information.
- A witnessed SATeq axiom contributes its explicit bit-equality path to S_link and permits quotient contraction only for formula occurrences connected by that path.
- A bounded-SR_h step is normalized by expanding its E-uniform site iterator; with T(pi)=N^{eta+o(1)}, M_N=N^{q+o(1)}, and h_N=N^{tau+o(1)}, the total rewrite charge is N^{q+eta+tau+o(1)}.
- Exceptional-row rules add E_N N literal patches and are charged separately, so no hidden sparse residual is absorbed into o(1).
- The final annotation yields Q_pi of size at most Gamma_bEF(pi) up to N^{o(1)} coding overhead; composing Q_pi with the generator circuit gives C(H_N^SAT)<=N^{rho+o(1)}+Gamma_bEF(pi)N^{o(1)}.
- Therefore any accepted low-cost Psys_bEF^- proof satisfying N^{rho+o(1)}+Gamma_bEF(pi)<N^{1+epsilon-o(1)} contradicts the asserted nonuniform lower bound LB_N(1+epsilon), giving a valid route-level falsifier.
- For Psys_sym, apply the unread-enable-bit pair F_0,F_1 to show that a surface occurrence transcript cannot justify FormulaEval-SAT unless the proof pays expansion or treats the rule as semantic oracle.

Blocking gap: The restricted SR_h normal form is discharged only for Psys_bEF^-. The remaining full-system gap is UExtWitnessability or an N^{1+q+o(1)} expansion theorem for FormulaEval-SAT in Psys_sym.

## Falsifiers

- FormulaEval-SAT line reads only surface occurrences while an unread clause-enable bit can flip SAT value; this is a finite falsifier for occurrence completion.
- Any SR_h rule with unbounded or non-E-uniform site expansion invalidates the N^{q+eta+tau+o(1)} charge.
- If N^{rho+o(1)}+Gamma_bEF(pi) is not below N^{1+epsilon-o(1)}, the parser theorem gives no lower-bound falsifier.
- If SATeq quotient witnesses use advice or nonuniform row selection, the target-preserving parser interface is invalid.
- If q<epsilon, direct row enumeration already refutes LB_N(1+epsilon), so a claimed hard beta-zero source is miscalibrated.

## Learning

Cycle 99 improves the archived parser packet by closing the restricted Gap98-SRhNormalForm case: Psys_bEF^- has a valid Gamma_bEF line-induction parser and low-cost transcript falsifier. The only remaining full-system escape is now sharply localized to FormulaEval-SAT: an unread eval-critical bit gives a finite countermodel unless the rule pays N^{1+q+o(1)} expansion or supplies UExtWitnessability.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for Psys_sym FormulaEval-SAT.`
- Rationale: The branch no longer needs another abstract barrier label; it needs to decide whether surface occurrence completion is a valid parser rule or a semantic escape. A one-bit SAT-flip family tests exactly that interface.
- Situation seed: Padded CNF query family F_b with an enabled unit clause y and a second padded clause enabled by bit b; b=0 leaves a satisfiable formula, b=1 activates a contradictory unit clause and makes the query unsatisfiable. Embed F_b as one G_N(x,j) query in H_N^SAT.
- Varied variable: The parser coverage variable u, namely whether the clause-enable bit b is included in the FormulaEval-SAT transcript or left unread.
- Held-fixed controls: Same N-scale truth-table target H_N^SAT and same query index (x,j)., Same generator overhead N^{rho+o(1)} and M_N=N^{q+o(1)} beta-zero query count., No advice, no nonuniform selector, and the same bit-level CNF encoding., All other formula bits and all witnessed SATeq links are held fixed.
- Expected observation: If u=0, F_0 and F_1 have identical parsed surface data but opposite SAT values, so row-parity binding fails. If u=1 for every affected query, the repair accumulates the N M_N=N^{1+q+o(1)} expansion charge.
- Transfer certificate needed: A bit-level normal-form theorem showing that every FormulaEval-SAT use either has dependency paths to all evaluation-critical formula bits, has an advice-free SATeq quotient witness, or is explicitly classified as a semantic oracle outside Psys_bEF^-.

## Next Experiment

Formalize Psys_sym FormulaEval-SAT as one of four mechanisms: axiom schema with all formula bits, proof line with witnessed quotient, extension rule with bounded-SR_h expansion, or semantic oracle. Prove the N^{1+q+o(1)} expansion charge for the first three or finalize the unread-enable-bit countermodel for the oracle case.
