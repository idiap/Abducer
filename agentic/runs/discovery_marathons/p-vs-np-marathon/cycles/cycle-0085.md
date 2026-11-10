# cycle-0085

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For the beta-zero XOR carrier, short proofs in the concrete system EF+SATeq_N admit a three-way audit: either the accepted certificate is label-functional and hence subject to the dense naturalization test, or its occurrence transcript forces at least N^{epsilon-o(1)} complete source rows, or its nonrelativizing SAT-equivalence uses touch at least N^{epsilon-o(1)} source rows through semantic links. If neither row count reaches the threshold, private-row spoofing plus equality patching is a valid falsifier for an N^{1+epsilon-o(1)} source lower-bound certificate.

## Definitions

- source object: a concrete EF+SATeq_N proof pi of LB_N(H_N^SAT,N^{1+epsilon}) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, L_N=(log N)^d, and generator size N^{rho+o(1)}.
- target object: a route-level proof-system audit theorem classifying short lower-bound certificates as functional-naturalizing, occurrence-full-row-expensive, or SAT-semantic-link-expensive; it is not a proof of P != NP.
- controlled interface: beta-zero substitution from SAT circuits of length L_N into H_N plus a proof parser producing an occurrence query set Q_pi and a semantic-equivalence link set E_pi from EF+SATeq_N derivations.
- target-preserving condition: q,rho<1+epsilon and every nonfunctional nonnaturalizing accepted certificate must have |ForcedRows(Q_pi) union SemRows(E_pi)|>=N^{epsilon-o(1)} to avoid subthreshold row-residual patching.
- EF+SATeq_N is Extended Frege over the source input variables and SAT-atoms SAT(F), plus the rule EqSAT: from an EF proof of Boolean equivalence F iff F' infer SAT(F) iff SAT(F').
- A complete source row is a fixed x for which the transcript determines the parity-relevant SAT labels SAT(G_N(x,j)) for all j<=M_N, either syntactically by occurrence queries or semantically by EqSAT links to determined atoms.
- ForcedRows(Q_pi) counts rows completed by occurrence-local information; SemRows(E_pi) counts rows whose parity labels are constrained by nonrelativizing formula-equivalence links.

## Assumptions

- Circuit size is nonuniform Boolean SIZE, and the source lower bound is C(H_N^SAT)>N^{1+epsilon-o(1)} on the N-bit carrier input length.
- The proof verifier is uniform polynomial time in |pi| and N; pi is not treated as hidden advice beyond its explicit bits.
- Every EF+SATeq_N inference except EqSAT is label-functional over SAT-atoms, meaning it remains sound under arbitrary Boolean interpretations of the SAT-atoms preserving the syntactic proof lines.
- EqSAT is the only currently named SAT-semantic rule; stronger EF+SAT_U rules must be separately factored into label-functional parts and semantic links before this lemma is applicable.
- The equality-patching circuit may hardwire exceptional source rows, so the residual audit is a nonuniform leakage test rather than a uniform algorithmic construction.

## Equations

- beta_zero_xor_carrier: `H_N^{SAT}(x)=\bigoplus_{j=1}^{M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad L_N=(\log N)^d`. Valid when: Valid when G_N is a fixed batched generator outputting length-L_N SAT instances and the carrier input length is N.
- beta_zero_substitution_transfer: `SAT\in SIZE(n^c)\Rightarrow C(H_N^{SAT})\le N^{\rho+o(1)}+N^{q+o(1)}L_N^c=N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies after the generator overhead is N^{rho+o(1)}, query length is polylogarithmic, and SAT circuits are substituted nonadaptively.
- row_residual_patch: `D_N=H_N^{SAT}\text{ off }R_N\Rightarrow C(H_N^{SAT})\le C(D_N)+O(|R_N|N)`. Valid when: Valid when R_N is a hardwired set of exceptional N-bit source rows and equality tests cost O(N) gates each.
- semantic_link_threshold: `|ForcedRows(Q_\pi)\cup SemRows(E_\pi)|<N^{\epsilon-o(1)}\Rightarrow \text{certificate is row-residual-leaky}`. Valid when: Requires the parser to expose all nonfunctional SAT uses as occurrence queries or EqSAT semantic links, with no hidden advice leakage.

## Attempted Derivation

- Fix EF+SATeq_N: ordinary EF reasoning is syntactic and label-functional; EqSAT is the sole nonrelativizing rule, derived from EF proofs of Boolean formula equivalence.
- Scan a proof pi of LB_N(H_N^SAT,N^{1+epsilon}) and mark every SAT atom occurrence used by label-functional rules; these form Q_pi.
- For every EqSAT application SAT(F)<->SAT(F'), add a semantic link between the source rows whose generated formulas include F or F', when such rows are in the carrier range; off-range links are charged to proof size but not to parity-row forcing.
- Run the previous private-row spoof only on rows outside ForcedRows(Q_pi) union SemRows(E_pi). On those rows, assign occurrence labels to agree with a low-cost completion while preserving all recorded EqSAT constraints.
- If W=|ForcedRows union SemRows|<N^{epsilon-o(1)}, patch the W exceptional rows by equality tests to obtain C(H_N^SAT)<=S_D+O(WN), contradicting a claimed N^{1+epsilon-o(1)} source lower bound.
- The EqSAT padding identity shows why the older occurrence-only parser is invalid for full EF+SATeq_N: semantic equality is not invariant under independent occurrence-label flips.

Blocking gap: The derivation is complete only for EF+SATeq_N where all SAT semantics factors through EqSAT links. It does not yet cover full EF+SAT_U with witness, self-reduction, or minimization rules unless those rules are decomposed into label-functional inferences plus row-chargeable semantic links.

## Falsifiers

- falsifier: positive beta or q+beta c transfer debt still caps black-box magnification before all SAT exponents are excluded.
- falsifier: an occurrence-only parser for EF+SATeq_N is invalid because EqSAT padding equivalence is not preserved by private occurrence-label completions.
- falsifier: W=|ForcedRows union SemRows|<N^{epsilon-o(1)} plus a residual circuit D_N gives a valid subthreshold equality-patching upper bound.
- falsifier: hidden nonuniform advice in the proof pi that selects exceptional rows without being charged breaks the target-preserving certificate audit.
- falsifier: a full EF+SAT_U rule using SAT self-reducibility may evade both functional naturalization and EqSAT-link accounting, forcing quarantine until a named semantic-link factorization is proved.

## Learning

Cycle 85 sharpens the formula-semantic extraction fork: full occurrence parsing is false already for EF+SATeq_N because EqSAT padding identities are real SAT-semantic and nonrelativizing. The valid repair is a semantic-link trichotomy: nonfunctional certificates must pay either occurrence full rows or EqSAT-linked rows at the N^{epsilon-o(1)} threshold, otherwise sparse-row residual patching falsifies the source lower-bound certificate.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the full EF+SAT_U parser ambition.`
- Rationale: The branch needs a concrete target-preserving case where the occurrence theorem provably fails but the beta-zero transfer remains intact, so the next proof obligation is semantic-link accounting rather than another barrier restatement.
- Situation seed: Padded-pair beta-zero SAT parity carrier: for selected source rows x, the generator emits both F_{x,j} and Pad(F_{x,j})=F_{x,j} and (y or not y), and EF+SATeq_N has short EqSAT links proving their SAT labels equal.
- Varied variable: sigma where N^sigma is the number of source rows whose parity labels are protected by EqSAT semantic links instead of occurrence-local full-row queries.
- Held-fixed controls: M_N=N^{q+o(1)} with q<1+epsilon, generator size N^{rho+o(1)} with rho<1+epsilon, query length L_N=(log N)^d with d>1 so beta=0 substitution remains valid, nonuniform SIZE model and no hidden advice beyond the explicit proof transcript, source lower-bound threshold C(H_N^SAT)>N^{1+epsilon-o(1)}
- Expected observation: For sigma<epsilon, equality patching of the semantic-link rows remains subthreshold, so the certificate is leaky; at sigma>=epsilon the old sparse-row falsifier no longer applies, and the proof has paid the same row-forcing cost through nonrelativizing semantics.
- Transfer certificate needed: A formal parser theorem for EF+SAT_U showing every nonfunctional SAT-semantic inference either is label-functional after restriction or contributes to SemRows with a row charge that preserves the beta-zero q,rho threshold.

## Next Experiment

Attempt the finite EF+SATeq_N parser proof: formalize proof lines as Boolean circuits over SAT-atoms, prove label-functionality for EF rules, charge every EqSAT endpoint to SemRows, and test whether SAT self-reduction axioms in full EF+SAT_U admit the same charge or force a new semantic-escape lemma.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Equality-closed row residual gate for the named certificate model P_eq=local EF+SAT_U^{dag,=}. In P_eq, the occurrence-local row-forcing theorem lifts after replacing raw row count by formula-DAG equality-closed row count. Hence a valid beta-zero XOR lower-bound certificate with max{rho,q}<1+epsilon must either have equality-closed row charge at least N^{epsilon-o(1)} or fall to a sparse residual falsifier.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with x in {0,1}^{log N}, M_N=N^{q+o(1)}, L_N=(log N)^d, and generator circuit overhead N^{rho+o(1)}.
- target object: a formula-semantic extraction/no-go theorem for short lower-bound certificates proving C(H_N^SAT)>N^{1+epsilon-o(1)} inside P_eq.
- controlled interface: a parser maps a proof pi to SAT-query occurrences Q_pi, row map row:Q_pi->[M_N], and formula-DAG equality relation E_pi; no hidden row advice is allowed.
- target-preserving condition: every spoof or residual modification must respect E_pi, preserve the beta-zero parameters q,rho,L_N, and patch only equality-closed rows so the target circuit lower-bound threshold is unchanged.
- P_eq: Extended-Frege-style Boolean reasoning over the certificate plus SAT_U atoms where identical formula DAGs denote the same SAT atom; no self-reduction, witness-existence, or semantic equivalence axiom for syntactically distinct formulas is included.
- equality-closed row charge: the minimum size of K=cl_{E_pi}(R) needed to contain all rows whose proof-visible SAT atoms are equality-coupled to the altered residual rows.

## Assumptions

- Model regime: nonuniform Boolean circuit size C on N-point truth tables, with row functions patchable by O(N)-size DNF circuits.
- Uniformity regime: G_N is explicit with circuit overhead N^{rho+o(1)} and row index length log M_N; the proof parser is computable in poly(N).
- Certificate regime: P_eq soundness is ordinary soundness plus equality congruence only, so equality closure is a complete account of proof-visible SAT dependencies.
- Threshold regime: max{rho,q}<1+epsilon, otherwise the beta-zero transfer has no exponent margin and the forced-row conclusion is vacuous.
- Naturalness regime: if the same parser yields a poly(N)-constructive N^{-O(1)}-dense truth-table property useful against SIZE(N^{1+epsilon}), the route is handled by the natural-proofs falsifier rather than by row forcing.

## Equations

- equality_closure: `\operatorname{cl}_{E_\pi}(R)=\{j: \exists o,o'\in Q_\pi,\ \operatorname{row}(o)\in R,\ \operatorname{row}(o')=j,\ \operatorname{enc}(o)=\operatorname{enc}(o')\}`. Valid when: Valid when P_eq identifies SAT atoms only through exact formula-DAG equality edges exposed to the parser.
- residual_patch_bound: `C(H_N^{\mathrm{SAT}})\le S(D_N)+O(|K|N)`. Valid when: Applies when D_N computes the equality-closed residual and each omitted row function is patched nonuniformly by an O(N)-size truth-table circuit.
- beta_zero_substitution_cap: `C(H_N^{\mathrm{SAT}})\le N^{\rho+o(1)}+N^{q+o(1)}L_N^c=N^{\max\{\rho,q\}+o(1)}`. Valid when: Requires SAT on L_N-bit query formulas to have L_N^c-size circuits and the generator to have N^{rho+o(1)} circuit overhead.
- forced_equality_closed_rows: `|K|\ge N^{\epsilon-o(1)}`. Valid when: Follows when the claimed source lower bound is N^{1+epsilon-o(1)} and max{rho,q}<1+epsilon leaves a polynomial margin.

## Attempted Derivation

- Fix P_eq=local EF+SAT_U^{dag,=} and a parsed certificate pi for the sentence C(H_N^SAT)>N^{1+epsilon-o(1)}.
- Quotient all proof-visible SAT atoms by exact formula-DAG equality and define K=cl_{E_pi}(R) for any residual row set R used by the spoof.
- Because P_eq has no semantic SAT axiom except equality congruence, any assignment that is constant on equality fibers preserves all non-Boolean proof-visible constraints outside K.
- If |K| is small, build D_N by the same beta-zero spoof used in the occurrence-local theorem on all rows outside K; equality closure ensures the full-DAG transcript remains accepted.
- Patch the omitted rows in K by arbitrary row truth-table circuits of total size O(|K|N), giving C(H_N^SAT)<=S(D_N)+O(|K|N).
- Use S(D_N)<=N^{max{rho,q}+o(1)} and max{rho,q}<1+epsilon to contradict the claimed source lower bound unless |K|>=N^{epsilon-o(1)}.
- If the parser instead yields a dense functional truth-table property, route control sends it to the natural-proofs audit rather than treating it as a row-forcing proof.

Blocking gap: SemanticClosureParser(P_sem): for full EF+SAT_U with SAT self-reduction, witness, or semantic-equivalence axioms, equality closure is not complete; a row-syntax realizer or a large semantic-closure charge theorem is still missing.

## Falsifiers

- Shared-DAG equality: two proof-visible rows with identical formula encoding invalidate independent occurrence relabeling and force equality-closed patching.
- SAT self-reduction falsifier: SAT(F)=SAT(F|z=0) OR SAT(F|z=1) can reject a spoof that respects equality but violates semantic closure.
- Odd-charge Tseitin falsifier: bounded local consistency may accept all small proof views while global parity is inconsistent, so ordinary soundness is not DirectClusterSound.
- Threshold-collapse falsifier: if max{rho,q}>=1+epsilon, the residual patch bound has no exponent margin and cannot force N^{epsilon-o(1)} rows.
- Functional-naturalization falsifier: a poly(N)-constructive N^{-O(1)}-dense property useful against SIZE(N^{1+epsilon}) conflicts with the standard PRF/natural-proofs obstruction.

## Learning

Cycle 85 upgrades the full-DAG obstruction: occurrence row count is the wrong invariant once formula syntax is shared. For the equality-only model P_eq, the valid invariant is equality-closed row charge, and sparse equality-closed charge gives a concrete residual falsifier via C(H)<=S(D)+O(|K|N). For stronger EF+SAT_U, the remaining proof gap is not generic barrier folklore but the named SemanticClosureParser/row-syntax-realizer problem.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The full EF+SAT_U lift is blocked by whether formula-DAG sharing converts sparse occurrence rows into large equality-closed or semantic-closed row sets; a concrete collision-controlled carrier tests this without restating barrier folklore.
- Situation seed: Construct a padded beta-zero SAT-query family where M_N=N^{q+o(1)} rows are partitioned into blocks of identical formula DAGs of size B_N=N^gamma, while the remaining generator overhead stays N^{rho+o(1)} and L_N=(log N)^d.
- Varied variable: collision block exponent gamma in B_N=N^gamma.
- Held-fixed controls: Keep q,rho<1+epsilon so the beta-zero transfer margin is present., Keep the proof parser projection width O(log N) and proof search poly(N)., Keep the target sentence C(H_N^SAT)>N^{1+epsilon-o(1)} unchanged., Allow only syntax-respecting residual modifications in the full-DAG model.
- Expected observation: Raw occurrence row charge r becomes equality-closed charge about rN^gamma until blocks saturate. For gamma=0 the occurrence theorem is recovered; for gamma large, the shared-DAG falsifier blocks sparse spoofing and forces the proof to pay equality-fiber charge instead.
- Transfer certificate needed: A formal theorem that cl_{E_pi}(R) is the complete dependency closure for P_eq, or for stronger P_sem a row-syntax/semantic realizer proving that all SAT self-reduction and equality constraints remain satisfied.

## Next Experiment

Instantiate P_sem=EF+SAT_U^{dag,=,SR} with the single self-reduction axiom SAT(F)=SAT(F|z=0) OR SAT(F|z=1); define semantic closure cl_SR(R), then test whether cl_SR(R) must be N^{epsilon-o(1)} or whether a row-syntax realizer can preserve self-reduction on a sparse residual.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Let pi be a short EF+SAT_U proof/certificate for the beta-zero SAT-parity carrier H_N^SAT. If pi has a uniform equality-quotient occurrence parser with adaptive quotient-cover exponent alpha_eq, forced-row exponent f, and residual exponent r, then pi cannot validly certify C(H_N^SAT)>N^{1+epsilon-o(1)} whenever max{rho,q+alpha_eq,max(f,r)+1}<1+epsilon. In that regime the certificate is a finite falsifier: the parsed proof yields an unrestricted circuit upper bound for H_N^SAT below the claimed source lower bound.

## Definitions

- source object: a concrete EF+SAT_U proof pi of a lower-bound/certificate sentence for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N<=N^{q+o(1)}, formula length L_N=(log N)^d, and generator overhead N^{rho+o(1)}.
- target object: an unrestricted Boolean circuit for the whole beta-zero target function H_N^SAT, or equivalently a same-model upper bound contradicting any asserted N^{1+epsilon-o(1)} row-hardness consequence.
- controlled interface: parse pi into a quotient occurrence transcript Q_pi^= whose SAT occurrences are identified only through an explicit equality/congruence graph and whose label openings have adaptive cover exponent alpha_eq.
- target-preserving condition: the parser, quotient graph, forced-row list, and residual patch are uniform and advice-free; quotient identities preserve actual formula identity for the SAT queries G_N(x,j); and row-parity binding is required only outside the declared residual set.
- ForcedRows(pi) is the set of x for which the row parity xor_j SAT(G_N(x,j)) is constant over all local SAT-label completions satisfying the quotient transcript Q_pi^=.
- The exponent f is defined by |ForcedRows(pi)|<=N^{f+o(1)} and r by |R_N|<=N^{r+o(1)} for the residual rows not covered by the parser or binding argument.

## Assumptions

- Model: unrestricted nonuniform circuits measure C(.), while pi and the parser are generated and checked uniformly in time N^{O(1)} or 2^{O(log N)} as appropriate for the beta-zero carrier.
- Regime: beta-zero means SAT query length is polylogarithmic in N, so each query formula can be produced within the generator overhead N^{rho+o(1)} and the query count contributes N^{q+o(1)}.
- Uniformity/advice cutoff: no nonuniform hard-row selector, proof skeleton, or quotient opener may be supplied as advice; any fixed low-cover certificate may be hardwired only for the negative upper-bound direction.
- Same-theory condition: every equality edge in Q_pi^= must be justified by syntactic identity, extension-variable congruence, or a parsed SAT-semantic rule whose proof object is included in the cover ledger.
- Binding condition: valid row-parity binding means that every nonresidual accepted completion of Q_pi^= has the same H_N^SAT value on every row outside ForcedRows(pi).

## Equations

- adaptive_quotient_cover: `\alpha_{eq}=\max\{\tau,\max_\ell(a_\ell+\mu_\ell),\max_\ell \omega_\ell\}`. Valid when: Valid when the quotient parser supplies an adaptive opening protocol with transcript exponent tau, level-address exponent a_l, summary exponent mu_l, and local opener exponent omega_l for every parsed equality component.
- parsed_certificate_upper_bound: `C(H_N^{SAT})\le N^{\max\{\rho,\,q+\alpha_{eq},\,\max(f,r)+1\}+o(1)}`. Valid when: Applies after the reduction preserves the beta-zero query parameters, the quotient labels open uniformly without advice, and forced plus residual rows are patchable in the same unrestricted circuit model.
- falsifier_threshold: `\max\{\rho,\,q+\alpha_{eq},\,\max(f,r)+1\}<1+\epsilon \Rightarrow \neg\mathrm{Cert}_{pi}(C(H_N^{SAT})>N^{1+\epsilon-o(1)})`. Valid when: Requires the certificate sentence to claim unrestricted circuit hardness above N^{1+epsilon-o(1)} for the same H_N^SAT family parsed by the quotient transcript.

## Attempted Derivation

- Fix H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N<=N^{q+o(1)} and generator cost N^{rho+o(1)}.
- Given pi, parse all SAT occurrences and equality/congruence justifications into Q_pi^=. For definitional EF+SAT_U, use union-find over explicit copy, renaming, extension, and congruence edges.
- Define LocSat(Q_pi^=) as all Boolean labelings of quotient components consistent with the local SAT facts and proof transcript. Define ForcedRows(pi) by constancy of row parity over LocSat(Q_pi^=).
- If a nonresidual row is not forced, two local completions give different row parity while satisfying the same quotient transcript. This private-row spoof contradicts valid row-parity binding for the certificate.
- For forced rows, compute the certified parity by opening the quotient labels for the M_N queries; this costs N^{q+alpha_eq+o(1)} plus generator overhead N^{rho+o(1)}.
- Patch residual rows and any explicitly listed forced exceptions by a hardwired same-model residual circuit of size N^{max(f,r)+1+o(1)}, matching the previous sparse-row accounting ledger.
- Combine the generator, quotient-label decoder, XOR, and patch circuits to get C(H_N^SAT)<=N^{max{rho,q+alpha_eq,max(f,r)+1}+o(1)}.
- Therefore any proof/certificate claiming C(H_N^SAT)>N^{1+epsilon-o(1)} is invalid in the strict cap regime.

Blocking gap: The derivation is complete for definitional equality-local EF+SAT_U, but full EF+SAT_U may contain a semantic formula-identity or SAT-extensionality rule whose equality quotient is not exposed as a low-cover graph.

## Falsifiers

- Low quotient-cover exponent alpha_eq with rho,q,f,r below the threshold is a concrete falsifier for any claimed beta-zero MCSP/MKtP certificate lower bound.
- A nonforced row with two LocSat completions of opposite parity is a private-row spoof falsifier for local soundness without row-parity binding.
- A residual set R_N with |R_N|<=N^{r+o(1)} and r+1<1+epsilon gives sparse-row patch compression, falsifying the claimed source lower bound.
- A quotient opener, hard-row selector, or equality graph supplied by advice invalidates the target-preserving transfer to a uniform language consequence, though it may still support the negative hardwired upper bound.
- An unparsed ExtSat or formula-semantic identity rule is not a falsifier of the theorem; it is the named escape condition that blocks promotion to full EF+SAT_U.

## Learning

Cycle 85 upgrades the cycle-84 equality-graph task into a theorem-shaped packet: definitional formula identity is harmless because it contracts to a low-cover quotient, giving C(H_N^SAT)<=N^{max{rho,q+alpha_eq,max(f,r)+1}+o(1)}. The remaining full-system obstruction is no longer generic strength of EF; it is the specific presence of unparsed SAT-extensionality or semantic formula identity.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the equality-graph extraction task.`
- Rationale: The branch no longer needs another abstraction of hardness magnification; it needs to see whether formula identity in a concrete proof system merely lowers to a quotient cover or genuinely escapes occurrence parsing.
- Situation seed: Take a padded Tseitin-to-SAT query family G_N(x,j) with M_N=N^{q+o(1)} and build two EF+SAT_U certificates for the same H_N^SAT lower-bound sentence: one reuses formulas only by definitional extension variables, the other adds a primitive ExtSat equality between semantically equivalent but syntactically distant query formulas.
- Varied variable: The quotient equality-cover exponent alpha_eq, ranging from an explicit definitional union-find cover below 1+epsilon-q to an unparsed semantic identity edge with no bounded cover certificate.
- Held-fixed controls: The beta-zero carrier H_N^SAT, query exponent q, generator exponent rho, and polylogarithmic SAT instance length are fixed., The claimed target lower bound remains C(H_N^SAT)>N^{1+epsilon-o(1)} in unrestricted circuits., No advice is allowed for row selection, quotient opening, or residual location in the positive transfer statement., Row-parity binding is required outside the same residual set R_N.
- Expected observation: In the definitional proof, the parser should produce alpha_eq<=alpha_inc and the cap N^{max{rho,q+alpha_eq,max(f,r)+1}+o(1)}. In the ExtSat proof, the first failed parser edge should identify the exact semantic principle needed to escape the falsifier.
- Transfer certificate needed: A formal parser theorem pi -> Q_pi^= preserving SAT formula identity and a proof that every opened quotient label is computable within the declared adaptive-cover exponent; without that certificate the thought experiment cannot affect proof obligations.

## Next Experiment

Instantiate EF+SAT_U with one explicit extension-variable congruence rule set, write the union-find parser, and test a single ExtSat-like rule to decide whether it expands to low-cover equality or becomes the named semantic escape.
