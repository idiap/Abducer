# cycle-0084

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Conditional row-forcing theorem. Fix epsilon>0 and the beta-zero XOR carrier H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N<=N^{q+o(1)}, L_N=(log N)^d, and generator size N^{rho+o(1)}. In Psys=EF+SAT_U^{occ,rn}, if an accepted row-normal occurrence-local functional certificate proves the source lower bound C(H_N^{SAT})>T_N=N^{1+epsilon-o(1)}, then its parsed object Q_pi must syntactically force at least N^{epsilon-o(1)} complete XOR rows. Otherwise a private occurrence-label spoof preserves the transcript and yields a valid subthreshold patch circuit, refuting functional soundness.

## Definitions

- source object: an EF+SAT_U^{occ,rn} accepted transcript pi for the occurrence-label carrier H_N^a(x)=xor_{j<=M_N} a_{x,j}, with real labels a^{SAT}_{x,j}=SAT(G_N(x,j)).
- target object: a scoped no-go/extraction theorem for proof-mediated beta-zero XOR magnification, not a proof of P != NP.
- controlled interface: the parser pi -> Q_pi records row-local label atoms, row views V_x(Q_pi), and ForcedRows(Q_pi) without using the desired lower bound.
- target-preserving condition: q,rho<1+epsilon, L_N=(log N)^d, beta=0, no nonuniform advice beyond pi, and substitution of SAT circuits contributes only N^{o(1)} per queried formula.
- complete row: a source input x together with all M_N occurrence labels a_{x,1},...,a_{x,M_N}.
- forced row: a row x for which all Q_pi-compatible completions of the occurrence labels have the same parity xor_j a_{x,j}.
- private spoof A_Q: a rowwise completion of unforced rows that preserves every atom read by Q_pi while setting their row parity to a chosen easy predicate, usually 0.

## Assumptions

- Circuit model is nonuniform Boolean SIZE over N-bit source inputs; equality to one exceptional row costs O(N) gates.
- Psys is row-normal and occurrence-local: after parsing, every acceptance predicate factors through Q_pi and does not inspect real formula semantics except through occurrence labels.
- Functional label soundness holds: if pi accepts an occurrence-label assignment a, then the induced function H_N^a has circuit size greater than T_N.
- Transcript invariance is syntactic: any label assignment with the same Q_pi-view as the real SAT labels is accepted by the same transcript.
- The theorem is conditional for EF+SAT_U^{occ,rn}; it does not cover full EF+SAT_U unless a semantic-to-occurrence extraction map is proved.

## Equations

- beta0_xor_carrier: `H_N^a(x)=\bigoplus_{j=1}^{M_N} a_{x,j},\quad a^{SAT}_{x,j}=SAT(G_N(x,j))`. Valid when: Valid when G_N is the fixed beta-zero generator and a is any occurrence-label assignment.
- beta0_target_transfer: `SAT\in SIZE(n^c)\Rightarrow C(H_N^{SAT})\le N^{\rho+o(1)}+M_N L_N^c=N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies after SAT circuits are substituted only into polylogarithmic queries and generator overhead is counted.
- sparse_row_patch: `D=H_N \text{ off } R_N\Rightarrow C(H_N)\le C(D)+O(|R_N|N)`. Valid when: Requires D and H to differ on explicitly listed N-bit source rows only.
- forced_row_threshold: `|ForcedRows(Q_\pi)|\ge T_N/O(N)=N^{\epsilon-o(1)}\quad\text{for }T_N=N^{1+\epsilon-o(1)}`. Valid when: Valid under functional label soundness and transcript invariance for row-normal occurrence certificates.

## Attempted Derivation

- Fix N, epsilon, q,rho<1+epsilon, and an accepted EF+SAT_U^{occ,rn} transcript pi claiming C(H_N^{SAT})>T_N=N^{1+epsilon-o(1)}.
- Parse pi syntactically into Q_pi; for each source row x, compute the row view V_x(Q_pi) and put x in F=ForcedRows(Q_pi) iff V_x has no two compatible completions of opposite parity.
- Assume |F|=E<N^{epsilon-o(1)}. For every x notin F, choose a Q_pi-compatible completion with row parity 0; for x in F, leave the real SAT occurrence labels unchanged.
- By row-separability, the rowwise completions combine into one global occurrence-label assignment a' with the same Q_pi-view as the real SAT labels.
- By transcript invariance, pi accepts a'. By functional label soundness, C(H_N^{a'})>T_N.
- But H_N^{a'} is supported only on F, so an OR of equality tests for rows in F, with the correct hardwired output bit for each forced row, computes H_N^{a'} using O(EN) gates.
- Since E<N^{epsilon-o(1)}, O(EN)=N^{1+epsilon-o(1)} below the claimed threshold after choosing the margin in T_N, contradiction.
- Therefore every valid row-normal occurrence-local functional certificate must force at least N^{epsilon-o(1)} complete rows.

Blocking gap: The derivation is complete only for row-normal occurrence-local functional certificates. Full EF+SAT_U remains blocked at semantic-to-occurrence extraction because SAT_U axioms can couple labels through real formula syntax and witnesses, so private occurrence-label spoofs may not preserve acceptance.

## Falsifiers

- falsifier: if |ForcedRows(Q_pi)|=N^eta with eta<epsilon and row-normal invariance holds, the spoofed carrier has an O(N^{1+eta}) patch circuit contradicting the source lower-bound certificate.
- falsifier: a parser atom that hides real SAT_U semantics rather than occurrence labels invalidates the occurrence-local theorem for full EF+SAT_U and triggers the extraction-boundary quarantine.
- falsifier: any reintroduced positive query exponent beta gives the older transfer cap q+beta*c+o(1), so beta-zero preservation must be rechecked for every proposed carrier variant.
- falsifier: nonuniform advice selecting the exceptional rows without being charged can fake ForcedRows robustness; advice must be included in Q_pi or in the circuit-size accounting.

## Learning

Cycle 84 turns the ForcedRows packet into a proof-shaped conditional theorem: row-normal occurrence-local functional certificates must force N^{epsilon-o(1)} complete XOR rows, because otherwise private label spoofing plus sparse equality patching is a valid falsifier. The remaining gap is exactly semantic-to-occurrence extraction for full EF+SAT_U, not ordinary soundness or generic natural-proofs folklore.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The top proof item turns on whether private-row spoofing creates an actual subthreshold circuit; varying the number of forced rows gives the exact threshold rather than another abstract barrier restatement.
- Situation seed: Fix a row-normal EF+SAT_U^{occ} transcript pi for H_N^{SAT}. Mark E=N^eta complete source rows as syntactically forced. On every unforced row, keep the Q_pi-view unchanged but flip a private occurrence label so the XOR parity becomes 0.
- Varied variable: eta=log_N E, the forced-row exponent.
- Held-fixed controls: M_N<=N^{q+o(1)} with q<1+epsilon., Generator size N^{rho+o(1)} with rho<1+epsilon., Target query length L_N=(log N)^d, so beta=0., Functional label soundness for EF+SAT_U^{occ,rn}., Equality-patch cost O(N) per exceptional N-bit source row.
- Expected observation: For eta<epsilon the spoofed function is supported on N^eta rows and has size N^{1+eta+o(1)}, so any accepted functional certificate is unsound. The threshold transition occurs at eta=epsilon.
- Transfer certificate needed: A formal parser-invariance certificate pi->Q_pi proving that every unforced row has a parity-changing completion preserving all accepted transcript atoms; for full EF+SAT_U this must be replaced by a nonrelativizing semantic-to-occurrence extraction theorem.

## Next Experiment

Audit one standard full EF+SAT_U encoding rule: attempt to extract its occurrence-label dependency into Q_pi preserving A_Q-invariance; if a witness or clause-soundness axiom breaks invariance, record the minimal rule-level countermodel and restrict the theorem statement to EF+SAT_U^{occ,rn}.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Occurrence-local row-forcing theorem packet: Fix epsilon>0. In Psys=EF+SAT_U^{occ}, let pi be accepted as a certificate that C(H_N^{SAT})>N^{1+epsilon-o(1)} for H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)). If the verifier is row-view sound under private occurrence-label perturbations and the parser residual outside complete forced rows is point-sparse, then either |ForcedRows(Q_pi)|>=N^{epsilon-o(1)} or there is an admissible spoof assignment A_pi for which the same transcript accepts a false lower-bound claim for a function of circuit size <N^{1+epsilon-o(1)}.

## Definitions

- source object: Psys=EF+SAT_U^{occ} transcript pi accepted for a beta-zero XOR lower-bound certificate for H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N<=N^{q+o(1)} and generator overhead N^{rho+o(1)}.
- target object: a route-specific no-go theorem saying that any sound occurrence-local certificate for C(H_N^{SAT})>N^{1+epsilon-o(1)} must force at least N^{epsilon-o(1)} complete generator rows, unless sparse patching gives a smaller circuit.
- controlled interface: parser pi -> Q_pi exposes touched private occurrence labels, complete rows, ForcedRows(Q_pi), an isolated point residual P_pi, and a perturbation A_Q acting only on unforced private labels while keeping the verifier transcript fixed.
- target-preserving condition: the lower-bound implication is measured in the same nonuniform circuit model C/SIZE over the N-bit truth table of H_N^{SAT}, with no row advice and with patch circuits counted against the N^{1+epsilon} threshold.
- CompleteRow(j) means the parser has a syntactic row token or protected-label set determining all N labels SAT(G_N(x,j)) for that generator row, not merely a few mentioned occurrences.
- ForcedRows(Q_pi) is the set of j with CompleteRow(j) in Q_pi; this is syntactic and independent of the desired lower bound.
- The spoof function H_N^A is obtained by replacing SAT labels with private Boolean labels a_{x,j} while preserving every label value read by pi and every occurrence-local rule premise.

## Assumptions

- Model: EF+SAT_U^{occ} treats each generated SAT query occurrence as a private atom unless the transcript explicitly protects it; no shared formula-syntax equality is available in this restricted model.
- Uniformity/cutoff: G_N is computable with overhead N^{rho+o(1)}, M_N<=N^{q+o(1)}, and all asymptotics range over valid generator lengths.
- Soundness regime: an accepted transcript for a lower-bound certificate is required to be sound under every admissible occurrence-label interpretation that satisfies the same local transcript checks.
- Residual regime: labels not covered by ForcedRows(Q_pi) and not in P_pi can be changed to an easy default D_pi without changing pi; |P_pi|log N<=N^{1+o(1)} in the row-view certificate model.
- Threshold regime: rho<1+epsilon and C(D_pi)<=N^{1+o(1)}, so the only superlinear patch term below the claimed lower bound is |ForcedRows(Q_pi)|N.
- Non-claim: this theorem audits a proof route; it does not prove C(H_N^{SAT})>N^{1+epsilon} or P != NP.

## Equations

- spoof_xor: `H_N^A(x)=xor_{j<=M_N} a_{x,j}`. Valid when: Valid when A assigns one Boolean private label to each generated occurrence and the occurrence-local transcript does not identify equal SAT formulas.
- sparse_patch_upper_bound: `C(H_N^A) <= N^{rho+o(1)} + c |ForcedRows(Q_pi)| N + c' |P_pi| log N + C(D_pi)`. Valid when: Valid when unforced nonresidual labels are set to the easy default D_pi, forced rows are hardwired as N-bit tables, and isolated point residuals are patched individually.
- row_charge_threshold: `|ForcedRows(Q_pi)| >= (N^{1+epsilon-o(1)}-N^{rho+o(1)}-C(D_pi)-c'|P_pi|log N)/(cN) = N^{epsilon-o(1)}`. Valid when: Requires the claimed lower-bound threshold, rho<1+epsilon, point residual cost N^{1+o(1)}, and soundness against all admissible private-label spoof functions.

## Attempted Derivation

- Fix epsilon>0 and a valid length N. Work in Psys=EF+SAT_U^{occ}, where every SAT_U atom generated from G_N(x,j) is a private occurrence label unless Q_pi marks a complete row protected.
- Run the parser on an accepted transcript pi to obtain Q_pi, ForcedRows(Q_pi)=F_pi, isolated point residual P_pi, and the set of occurrence labels whose values are actually inspected by the accepting computation.
- Assume |F_pi|<N^{epsilon-o(1)} and |P_pi|log N<=N^{1+o(1)}. Define A_pi to agree with the transcript on inspected labels, agree with true labels on rows in F_pi, and set every other private label to the easy default D_pi.
- Occurrence locality gives transcript invariance: pi sees the same labels and rule premises under A_pi, so the verifier accepts the same lower-bound certificate for H_N^{A_pi}.
- Build a circuit for H_N^{A_pi}: compute D_pi and the generator bookkeeping, hardwire each forced row as an N-bit table, and patch isolated residual points. This gives C(H_N^{A_pi})<=N^{rho+o(1)}+c|F_pi|N+c'|P_pi|log N+C(D_pi).
- Under rho<1+epsilon and the residual assumptions, the upper bound is <N^{1+epsilon-o(1)}, contradicting row-view soundness. Therefore any sound occurrence-local certificate must have |F_pi|>=N^{epsilon-o(1)}.
- Attempted lift to full EF+SAT_U stops at EqFib(pi): private A_pi may assign different values to occurrences of the same SAT formula, so full syntax needs Realize(Q_pi,E_pi) or a large equality-fiber row charge.

Blocking gap: The occurrence-local proof is blocked only by a rule-by-rule audit of EF extension and SAT_U^{occ} premises; the full EF+SAT_U transfer is blocked at the row-syntax realizer Realize(Q_pi,E_pi), with shared-DAG equality as the concrete countermodel.

## Falsifiers

- Sparse-row spoof falsifier: if |ForcedRows(Q_pi)|<N^{epsilon-o(1)} and residual point cost is N^{1+o(1)}, the accepted occurrence-local transcript can certify a spoof function with a below-threshold patch circuit.
- Shared-DAG equality falsifier: two occurrences of the same SAT formula in different generator rows invalidate private-label perturbations in full EF+SAT_U unless the spoof is constant on their equality fiber.
- Odd-charge Tseitin falsifier: bounded local consistency can accept every local view while the global parity charge is inconsistent, so ordinary soundness is not DirectClusterSound.
- Natural-property falsifier: if logarithmic projection plus DirectClusterSound is added, the route yields a valid large constructive useful property and collides with the PRF/natural-proofs pressure for the same target class.
- Projection-residual falsifier: if P_pi has size N^{1+epsilon-o(1)}, the sparse patch contradiction disappears and the certificate has leaked the lower-bound-sized object into the transcript.

## Learning

Cycle 84 upgrades the support branch from a remembered obstruction to a proof-delivery packet: in EF+SAT_U^{occ}, private-label invariance plus sparse patching forces N^{epsilon-o(1)} complete rows or gives a concrete spoof falsifier. The full EF+SAT_U lift is valid only with a row-syntax realizer or an equality-fiber row-charge theorem; shared-DAG equality is the named finite obstruction. This is route-level progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The remaining live gap is not another abstract barrier label; it is whether full EF+SAT_U equality fibers permit the sparse spoof needed for the occurrence-local row-forcing theorem.
- Situation seed: Construct a beta-zero XOR family where G_N(x,j) deliberately reuses identical SAT formula DAGs across blocks of rows, while an EF+SAT_U transcript mentions only logarithmic projected views and a candidate set of complete forced rows.
- Varied variable: gamma, the exponent in the equality-fiber row charge |E_bad(pi)|=N^{gamma+o(1)} created by shared formula-DAG reuse.
- Held-fixed controls: M_N<=N^{q+o(1)} and generator overhead N^{rho+o(1)} are fixed., The claimed source threshold remains C(H_N^{SAT})>N^{1+epsilon-o(1)} in the same nonuniform circuit model., The verifier is not allowed row advice or a semantic oracle beyond EF+SAT_U formula syntax., The occurrence-local parser definitions of Q_pi, ForcedRows(Q_pi), and P_pi are held fixed.
- Expected observation: If gamma<epsilon and a row-syntax realizer exists outside E_bad(pi), sparse patching still falsifies the full-system certificate. If every realizer forces gamma>=epsilon, the full lift is blocked for a precise combinatorial reason: equality fibers themselves carry the required row charge.
- Transfer certificate needed: A formal Realize(Q_pi,E_pi) lemma producing a transcript-preserving, equality-fiber-constant spoof assignment, or a proof that every such realizer charges at least N^{epsilon-o(1)} rows.

## Next Experiment

Run the full EF+SAT_U equality-fiber thought experiment: build a minimal shared-DAG two-row countermodel, then generalize to a parameter gamma and test whether Realize(Q_pi,E_pi) exists below the N^{epsilon-o(1)} row-charge threshold.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Equality-quotient ForcedRows falsifier for full EF+SAT_U: given a full EF+SAT_U beta-zero XOR transcript pi, parse syntactic formula identity and extension-variable congruence into an equality graph Gamma_pi. If the quotient labels have adaptive cover exponent alpha_eq, the quotient-forced rows have size N^{f+o(1)}, and residual disagreement has size N^{r+o(1)}, then any row-parity-bound carrier yields C(H_N^SAT)<=N^{max{rho,q+alpha_eq,max(f,r)+1}+o(1)}. Hence a claimed N^{1+epsilon-o(1)} lower-bound certificate is invalid whenever this cap is below 1+epsilon.

## Definitions

- source object: a full EF+SAT_U proof transcript pi for the beta-zero XOR carrier H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with real formula syntax, SAT_U oracle atoms, and extension-variable definitions.
- target object: a scoped route-specific no-go theorem for proof-mediated beta-zero XOR certificates, not a proof of P != NP.
- controlled interface: the parser pi -> (Q_pi,Gamma_pi,LocSat_Gamma(Q_pi),ForcedRows_Gamma(pi),Cover_Gamma(pi)) that exposes only syntactic equality, local proof constraints, quotient labels, and adaptive-cover summaries.
- target-preserving condition: the quotient perturbations must respect all formula-identity and extension-congruence edges, and the derived circuit must compute the same H_N^SAT truth table in the original nonuniform circuit model.
- Gamma_pi has vertices for touched SAT_U query occurrences, generated subformula occurrences, and extension-variable occurrences; edges identify syntactically identical formulas and declared extension congruences.
- ForcedRows_Gamma(pi) is the set of x for which the XOR of the M_N quotient labels addressed by row x is constant over all locally satisfying quotient assignments.
- alpha_eq is the adaptive-cover exponent of quotient-label opening: tau for global transcript access, a_l+mu_l for level-l summaries, and omega_l for level-l openers.

## Assumptions

- Model: nonuniform Boolean circuits measure C(.) on truth tables of length N, with H_N^SAT E-uniformly generated by G_N in overhead N^{rho+o(1)}.
- Query regime: M_N<=N^{q+o(1)} and query length L_N=(log N)^d; q, rho, alpha_eq, f, r are fixed exponents up to o(1).
- Proof-system regime: EF+SAT_U rules are syntactic after quotienting by Gamma_pi; no semantic formula-equivalence rule is used unless its certificate is inserted as an edge in Gamma_pi.
- Binding regime: the transcript is row-parity binding outside a residual set R_N of size N^{r+o(1)} after quotienting; otherwise a private quotient-label spoof is a valid falsifier of the carrier.
- Cover regime: Cover_Gamma(pi) supplies advice-free, same-length circuits for all quotient labels touched by G_N, with exponent alpha_eq and no nonuniform hard-row selector.
- Non-claim: the lemma is a transfer obstruction for this carrier route only; it does not prove the main P != NP conjecture.

## Equations

- beta_zero_xor_carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\quad M_N\le N^{q+o(1)},\quad |G_N(x,j)|=(\log N)^d.`. Valid when: Valid when the beta-zero carrier family and the generator overhead are fixed uniformly before inspecting any proof transcript.
- quotient_forced_rows: `ForcedRows_\Gamma(\pi)=\{x:\bigoplus_{j\le M_N} b_{[x,j]} \text{ is constant on } LocSat_\Gamma(Q_\pi)\}.`. Valid when: Valid when Gamma_pi quotients all syntactic formula identities and extension congruences appearing in the transcript.
- quotient_adaptive_cover_cap: `\alpha_{eq}(\pi)=\max\{\tau_\Gamma,\max_\ell(a_\ell+\mu_\ell),\max_\ell \omega_\ell\}.`. Valid when: Valid when quotient labels are opened through a declared adaptive cover with named summary and opener exponents.
- patch_upper_bound: `C(H_N^{SAT})\le N^{\max\{\rho,q+\alpha_{eq},\max(f,r)+1\}+o(1)}.`. Valid when: Applies after row-parity binding, quotient-cover decoding, and sparse residual patching are all preserved in the same circuit model.
- certificate_falsifier_threshold: `\max\{\rho,q+\alpha_{eq},\max(f,r)+1\}<1+\epsilon \;\Rightarrow\; \pi \text{ cannot certify } C(H_N^{SAT})\ge N^{1+\epsilon-o(1)}.`. Valid when: Requires the target lower-bound threshold and the derived upper bound to concern the identical truth-table family H_N^SAT.

## Attempted Derivation

- Start with the equality-free occurrence-local theorem from cycle 83, where private labels are independent per generated SAT_U occurrence.
- For full EF+SAT_U, replace independent labels by connected components of Gamma_pi, adding edges for identical formula encodings and extension-variable congruence.
- Define LocSat_Gamma(Q_pi) as local proof constraints over quotient labels; this definition is syntactic and valid for equality-explicit transcripts.
- Define ForcedRows_Gamma(pi) by constancy of row XOR over LocSat_Gamma; nonconstancy yields a quotient-private spoof pair preserving every quotient-local verifier check.
- Assume an advice-free adaptive cover opens every quotient label touched by G_N with exponent alpha_eq. Composing G_N, the cover opener, and XOR over M_N queries gives a default circuit of size N^{max(rho,q+alpha_eq)+o(1)}.
- Patch rows in ForcedRows_Gamma(pi) and residual rows R_N by equality tests on x, costing O((|ForcedRows_Gamma|+|R_N|)N^{1+o(1)})=N^{max(f,r)+1+o(1)}.
- Combine the default circuit and patch circuit to obtain C(H_N^SAT)<=N^{max{rho,q+alpha_eq,max(f,r)+1}+o(1)}.
- Therefore a purported certificate for C(H_N^SAT)>=N^{1+epsilon-o(1)} is refuted whenever the cap is below 1+epsilon.

Blocking gap: The derivation is fully valid for equality-explicit EF+SAT_U, but not for unrestricted full EF+SAT_U unless every semantic use of formula identity and extension-variable reuse is extractable into Gamma_pi with a low adaptive cover or is charged as UnparsedIdentity(pi).

## Falsifiers

- A low-cover equality quotient with alpha_eq satisfying q+alpha_eq<1+epsilon and small forced/residual row exponents is a direct falsifier of the claimed beta-zero certificate.
- A transcript using unrecorded semantic formula identity is a falsifier for any attempt to promote the equality-free occurrence-local theorem to full EF without an extraction lemma.
- A nonuniform hard-row selector inside the MCSP/MKtP carrier invalidates the target-preserving transfer to a uniform language lower bound.
- A sparse residual set R_N with |R_N|=N^{r+o(1)} and r<epsilon lets equality-test patching defeat an N^{1+epsilon-o(1)} source lower-bound claim.
- A quotient opener below the adaptive-cover threshold gives small unrestricted row circuits, so local proof soundness alone is not a valid certificate of row hardness.

## Learning

Cycle 84 localizes the remaining full-EF obstruction: formula identity is harmless when it is parsed into a low-cover equality quotient, because the same patch upper bound follows. The only valid escape is high quotient cover, many forced rows, large residual/generator overhead, or an unparsed semantic identity rule. This converts the prior vague full-EF gap into a finite equality-graph extraction task.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch has a concrete full-EF boundary gap: does real formula identity merely create a quotient cover, or can it force row parity without becoming a small circuit? A target-preserving thought experiment isolates this parameter.
- Situation seed: Take a padded SAT-query family G_N where a fraction of generated queries collide syntactically across rows through shared padded cores. Build two transcripts: one equality-free EF+SAT_U^{occ} transcript and one equality-explicit EF+SAT_U transcript whose only added power is edges identifying equal padded cores.
- Varied variable: The equality-graph component exponent chi, measured by the largest number N^{chi+o(1)} of row-query incidences opened from one quotient component, equivalently its contribution to alpha_eq.
- Held-fixed controls: Keep H_N^SAT, M_N<=N^{q+o(1)}, L_N=(log N)^d, and generator overhead N^{rho+o(1)} fixed., Keep the claimed target threshold C(H_N^SAT)>=N^{1+epsilon-o(1)} fixed., Forbid nonuniform hard-row advice and require every quotient opener to be E-uniform., Keep residual size |R_N|<=N^{r+o(1)} and patch model unchanged.
- Expected observation: For chi below the cap 1+epsilon-q, quotienting only lowers entropy and strengthens the circuit upper bound; for percolating chi near the threshold, the occurrence-local spoof stops transferring and the escape is exactly high quotient adaptive cover, not generic EF strength.
- Transfer certificate needed: A formal equality-graph extraction certificate: every full-EF use of formula identity must either become an edge in Gamma_pi with declared cover exponent alpha_eq, or be isolated as an UnparsedIdentity rule that blocks the full-EF promotion.

## Next Experiment

Instantiate Gamma_pi on a toy padded-SAT EF+SAT_U transcript with two rows sharing one formula core; compute ForcedRows_Gamma and alpha_eq, then verify whether the private spoof survives quotienting or the shared component exactly accounts for the lost invariance.
