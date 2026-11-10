# cycle-0081

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

The cycle-80 ForcedRows theorem is a valid scoped no-go for EF+SAT_U^{occ}, but it transfers to full EF+SAT_U only under an explicit shadow-extraction normal form. Standard full SAT_U semantic axioms are not invariant under private occurrence-label spoofing, so the unrestricted full-EF promotion is blocked at a named extraction gap rather than by generic barrier folklore.

## Definitions

- source object: a full EF+SAT_U proof transcript pi whose SAT atoms refer to the real generated formulas G_N(x,j) in the beta-zero XOR carrier H_N^{SAT}.
- target object: the occurrence-local ForcedRows row-forcing no-go for private labels y_{x,j} representing SAT(G_N(x,j)).
- controlled interface: a parser/normalizer Ext mapping pi to an occurrence shadow Q_pi, a touched-occurrence set, and a syntactic complete-row set ForcedRows(Q_pi).
- target-preserving condition: Ext must preserve proof soundness, proof size N^{o(1)} losses, and the row-residual threshold |R_N|<N^{epsilon-o(1)} without using the desired H_N lower bound.
- complete row: a source input x for which Q_pi fixes the parity xor_{j<=M_N} y_{x,j} over all occurrence-label completions satisfying the transcript constraints.
- private occurrence-label spoof: an assignment A_Q to the y_{x,j} labels that preserves Q_pi outside unforced rows while disagreeing with real SAT labels on a sparse row set.
- full SAT_U semantic line: an axiom or derived line tying SAT(F) to the actual syntax and witnesses of F, not merely to an uninterpreted occurrence label.

## Assumptions

- Model: nonuniform Boolean circuits for the source lower bound and EF+SAT_U proof transcripts of size N^{1+epsilon-o(1)} or smaller.
- Carrier regime: M_N<=N^{q+o(1)}, L_N=(log N)^d with d>1, generator complexity N^{rho+o(1)}, and max{rho,q}<1+epsilon.
- Occurrence-local regime: EF+SAT_U^{occ} proofs treat each generated SAT occurrence as a private label and impose only the transcript constraints parsed into Q_pi.
- Full-EF boundary regime: full EF+SAT_U may reason about formula syntax, witnesses, and shared subformula structure, so arbitrary private label flips need not preserve SAT_U axioms.
- Advice condition: Ext cannot hardwire the true SAT label vector on U_N or a circuit for H_N; such leakage would be target-equivalent.
- Uniformity condition: G_N, row indexing, and the parser Ext must be explicit enough that patch circuits and shadow proofs have the stated sizes.

## Equations

- beta_zero_xor_carrier: `H_N^{\mathrm{SAT}}(x)=\bigoplus_{j\le M_N}\mathrm{SAT}(G_N(x,j)),\quad M_N\le N^{q+o(1)},\quad L_N=(\log N)^d`. Valid when: Valid when the source object is the beta-zero generated XOR carrier with polylogarithmic target instances and an explicit row index j.
- shadow_extraction_requirement: `\mathrm{Ext}(\pi)=(Q_\pi,\mathrm{ForcedRows}(Q_\pi),R_\pi),\quad |Q_\pi|\le |\pi|N^{o(1)},\quad |R_\pi|<N^{\epsilon-o(1)}`. Valid when: Valid when a proposed full-EF transfer claims to reduce real SAT-semantic reasoning to occurrence-local constraints without exceeding the sparse-row patch threshold.
- semantic_invariance_obligation: `A_Q\models Q_\pi\ \Longrightarrow\ \pi\ \text{remains sound except on}\ \mathrm{ForcedRows}(Q_\pi)\cup R_\pi`. Valid when: Valid when private occurrence-label perturbations are required to simulate full SAT_U lines and all violations are covered by syntactically forced complete rows plus a residual set.
- full_EF_blocking_fact: `\exists F,b:\ b\ne \mathrm{SAT}(F)\ \Rightarrow\ (y_F=b)\ \text{may satisfy an occurrence shadow but violates SAT_U(F)}`. Valid when: Valid when full EF+SAT_U contains semantic axioms tying SAT labels to actual formula syntax rather than to independent occurrence variables.

## Attempted Derivation

- Start with the valid EF+SAT_U^{occ} theorem: if a functional occurrence-local transcript pi has fewer than N^{epsilon-o(1)} complete forced rows, construct a private-label spoof A_Q and a parity circuit D_N differing from H_N^{SAT} only on those rows.
- Try to lift this to full EF+SAT_U by projecting each full SAT atom SAT(G_N(x,j)) to a private occurrence label y_{x,j} and parsing the proof into Q_pi.
- Check transcript invariance: in EF+SAT_U^{occ}, A_Q preserves all parsed constraints outside ForcedRows(Q_pi); in full EF+SAT_U, a line asserting SAT_U(F) or a witness equivalence is tied to the real syntax of F.
- Construct the countermodel to naive invariance: choose an occurrence F=G_N(x,j) and set y_F to 1-SAT(F). The occurrence shadow can still satisfy uninterpreted constraints, but the full SAT_U axiom for F is false.
- Conclude that sparse-row patching remains a valid falsifier for occurrence-local certificates, but it cannot refute full EF+SAT_U certificates unless a shadow-extraction normal form covers every SAT-semantic violation by forced rows plus a subthreshold residual.

Blocking gap: Semantic-to-occurrence shadow extraction: no proof currently shows that full EF+SAT_U reasoning about actual SAT formulas can be converted into a functional occurrence-local Q_pi with subthreshold row residual and N^{o(1)} overhead.

## Falsifiers

- Full EF+SAT_U promotion falsifier: a SAT_U axiom line whose truth depends on real formula syntax is not preserved by private occurrence-label perturbations.
- Source lower-bound falsifier: any D_N agreeing with H_N^{SAT} off fewer than N^{epsilon-o(1)} rows and having C(D_N)<N^{1+epsilon-o(1)} gives a valid equality-patch upper bound.
- Parser falsifier: Ext hardwires the real SAT label vector or H_N^{SAT}, making the certificate target-equivalent rather than proof-extractable.
- Threshold falsifier: if max{rho,q}>=1+epsilon, the beta-zero substitution bridge no longer yields the claimed all-exponent SAT consequence.
- Naturalization falsifier: a dense constructive functional label certificate over U_N becomes a natural-property-style object unless it is nonlarge, nonconstructive, or genuinely SAT-semantic.

## Learning

Cycle 81 separates the scoped occurrence-local theorem from the full EF+SAT_U ambition. The valid contribution is now sharper: private row spoofing is a genuine falsifier for occurrence-local functional certificates, while full EF+SAT_U requires a nonrelativizing semantic-to-occurrence extraction theorem because real SAT_U axioms are not invariant under independent label flips.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for full EF+SAT_U extraction.`
- Rationale: The abstract occurrence theorem is already scoped; the remaining route risk is conflating private occurrence labels with real SAT semantics. A concrete semantic-coupling experiment tests whether full-EF reasoning forces complete rows or merely breaks the spoof model.
- Situation seed: Build a beta-zero XOR family where each row contains generated pairs F_{x,j} and F'_{x,j}=F_{x,j} OR z with shared syntax, so full SAT_U can reason about implications SAT(F)->SAT(F') while EF+SAT_U^{occ} sees only private labels y_{x,j},y'_{x,j}.
- Varied variable: semantic coupling width w, the number of cross-occurrence SAT_U implications per row exposed to the proof transcript.
- Held-fixed controls: M_N<=N^{q+o(1)}, L_N=(log N)^d with d>1, and max{rho,q}<1+epsilon., The occurrence-local parser Q_pi and complete-row definition from the cycle-80 theorem are held fixed., No advice may encode the real SAT labels or the target H_N^{SAT} truth table., Patch cost remains O(|R_N|N) for row residuals.
- Expected observation: For w=0 the private-label spoof survives and the occurrence theorem applies. As w grows, spoof assignments violate semantic implication axioms without necessarily forcing complete parity rows, exhibiting the exact obstruction to full-EF extraction.
- Transfer certificate needed: A formal normal form showing that every violated semantic implication is charged to complete forced rows or to R_N with |R_N|<N^{epsilon-o(1)} before the experiment can affect proof obligations.

## Next Experiment

Formalize the semantic-coupling-width thought experiment as a lemma: for paired formulas F and F OR z, show exactly which SAT_U implication lines break private-label invariance and whether their violations can be charged to complete forced rows below the N^{epsilon} patch threshold.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Restricted parser lemma: for strict occurrence-local EF+SAT_U^{occ} beta-zero XOR transcripts, an accepted transcript pi determines a syntactic packet Q_pi and a forced-row set R_pi without consulting SAT truth or the intended circuit lower bound.

## Definitions

- source object: EF+SAT_U^{occ} transcript pi for a beta-zero XOR certificate asserting CC(H_N^{SAT})>N^{1+epsilon}, where H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)).
- target object: Q_pi=(Occ_pi,Cl_pi,R_pi,Acc_pi), with R_pi the rows whose output bit is syntactically fixed by the parsed transcript closure.
- controlled interface: parser P_N reads transcript tokens, verifier coins, row labels h_x, and occurrence labels c_{x,j}, then closes only under named occurrence-local EF and row-XOR rules.
- target-preserving condition: Q_pi is computed from N, pi, and fixed public coins without SAT semantics, lower-bound truth, nonuniform row advice, or equality of separately generated formulas.
- row universe: x ranges over [N], row x contains cells c_{x,1},...,c_{x,M_N} and optional output label h_x.
- complete-row charge: a row is charged when h_x is fixed directly or all c_{x,j} are in the parser closure, so patching that row may require an explicit equality test.

## Assumptions

- Strict occurrence-local model: two labels c_{x,j} and c_{x',j'} are distinct unless the transcript explicitly invokes an allowed occurrence-equality rule.
- Verifier randomness is fixed before parsing; randomized certificates are handled seed-by-seed and require a separate seed-union bound.
- The proof checker is syntactic polynomial time in |pi| and N^{o(1)} projection width; it does not run SAT on G_N(x,j).
- Row-XOR axioms may relate h_x to c_{x,1},...,c_{x,M_N}, but no rule may infer an unmentioned SAT occurrence from real formula semantics.

## Equations

- beta_zero_xor_carrier: `H_N^{SAT}(x)=\bigoplus_{j=1}^{M_N} SAT(G_N(x,j)),\quad M_N\le N^{q+o(1)},\quad |G_N(x,j)|\le L_N`. Valid when: Valid when the source lower-bound model is the beta-zero XOR carrier with explicit generator G_N and fixed row/query parameters.
- parser_packet: `Q_\pi=(Occ_\pi,Cl_\pi,R_\pi,Acc_\pi)`. Valid when: Valid when the transcript grammar and verifier coins uniquely determine the occurrence labels and local closure operations.
- forced_rows: `R_\pi=\{x: h_x\in Cl_\pi\ \lor\ \{c_{x,j}:1\le j\le M_N\}\subseteq Cl_\pi\}`. Valid when: Valid when row output forcing is charged either by direct output access or by complete row-cell closure.

## Attempted Derivation

- Fix N, M_N, generator G_N, threshold epsilon>0, and a fixed accepting transcript pi of EF+SAT_U^{occ}.
- Run the syntactic parser P_N to form Occ_pi and Cl_pi by scanning labels and closing under explicit occurrence-local EF and row-XOR rules.
- Define R_pi as rows whose output is fixed directly or whose entire XOR row is fixed; this definition is syntactic and independent of CC(H_N^{SAT}).
- Prove by induction on checker steps that any assignment A' agreeing with A on Cl_pi produces the same transcript decisions; no step can observe a private perturbation outside Cl_pi.
- For each x notin R_pi, choose one unclosed cell and set it so the row parity equals a selected low-complexity base function D(x).
- Patch D on R_pi to match the forced rows, obtaining C(H_{A'})<=S_D+O(|R_pi|N polylog N).
- If |R_pi|<=N^{epsilon-eta} and S_D<=N^{1+o(1)}, the accepted transcript is consistent with a circuit below N^{1+epsilon-o(1)}, contradicting row-view soundness.
- Conclude the restricted theorem: sound occurrence-local certificates must force N^{epsilon-o(1)} charged rows, or else sparse-row spoofing is a valid falsifier for the certificate route.

Blocking gap: The derivation is valid only for strict occurrence-local EF+SAT_U^{occ} plus row-view soundness. Full EF+SAT_U extraction from real formula syntax remains unproved, and ordinary semantic soundness cannot replace row-view soundness.

## Falsifiers

- falsifier: odd-charge Tseitin local consistency gives accepting local views with no global satisfying proof, so ordinary soundness is not a valid substitute for DirectClusterSound or row-view soundness.
- falsifier: a full EF+SAT_U rule that canonicalizes G_N(x,j) and reuses semantic SAT atoms across rows destroys private occurrence-label perturbation invariance.
- falsifier: if the transcript directly fixes N^{epsilon} row outputs, the sparse-spoof contradiction disappears because the required row charge is already present.
- falsifier: if ForcedRows(Q_pi) is defined by semantic necessity of the lower bound rather than by parser closure, the theorem becomes target-equivalent and invalid.
- falsifier: if the base spoof D needs nonuniform advice encoding the unforced rows, the patch circuit no longer refutes the claimed advice-free lower-bound certificate.

## Learning

Cycle 81 upgrades the support branch by discharging the parser definition in the strict occurrence-local model and deriving the exact row-charge threshold |R_pi|>=N^{epsilon-o(1)} from private-label invariance plus sparse patching. The valid contribution is a scoped no-go for EF+SAT_U^{occ}; the full EF+SAT_U case is blocked precisely at formula-syntax extraction, not at generic barrier folklore.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch needs a concrete threshold check for the restricted ForcedRows theorem, not another abstract barrier restatement.
- Situation seed: Take a strict EF+SAT_U^{occ} verifier for H_N^{SAT} with N rows, M_N<=N^{q+o(1)} private SAT occurrence cells per row, and an accepted transcript whose parser closure fixes r=N^gamma charged rows; set the base spoof D to the zero circuit on every unforced row.
- Varied variable: gamma=log_N |R_pi|, the forced-row exponent extracted by the parser.
- Held-fixed controls: Occurrence-local grammar with no real-formula canonicalization., Fixed public verifier seed and logarithmic projection-decision width., Row-view soundness as the soundness notion, not ordinary proof soundness., Target threshold CC(H_N^{SAT})>N^{1+epsilon-o(1)} and conservative patch cost O(N polylog N) per charged row.
- Expected observation: For gamma<epsilon, the patched spoof has size N^{1+gamma+o(1)} and stays below the claimed threshold, so acceptance is impossible under row-view soundness; for gamma>=epsilon the sparse-row falsifier no longer yields a contradiction.
- Transfer certificate needed: A formal parser-invariance certificate for EF+SAT_U^{occ}, plus either a full EF+SAT_U extraction theorem or a written boundary saying the result is restricted to occurrence-local transcripts.

## Next Experiment

Run the full EF+SAT_U extraction boundary test: list each standard SAT_U/EF rule, mark whether it is occurrence-local, row-chargeable, or formula-semantic, and attempt to build the smallest formula-reuse countermodel if any rule is not chargeable.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Parser-forcing theorem for Psys=EF+SAT_U^{occ}: from any accepted low-cover transcript pi_N one computes a syntactic object Q_pi and F_pi={x: the row parity xor_{j<=M_N} z_{x,j} is constant on LocSat(Q_pi)} without referencing the desired lower bound. If the row decoder extracted from pi_N is valid and agrees with H_N^{SAT} outside F_pi union R_N, with |F_pi|=N^{f+o(1)}, |R_N|=N^{r+o(1)}, and adaptive cover exponent alpha_ad, then C(H_N^{SAT})<=N^{max{rho,q+alpha_ad,max(f,r)+1}+o(1)}. Hence a valid occurrence-local certificate for C(H_N^{SAT})>N^{1+epsilon-o(1)} needs max(f,r)>=epsilon-o(1), unless rho or q+alpha_ad already reaches the target threshold. This is a route-specific falsifier theorem, not a proof of P != NP.

## Definitions

- source object: an accepted EF+SAT_U^{occ} transcript pi_N for H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)), where occurrence variables z_{x,j,u} are private proof atoms unless equality is explicitly recorded.
- target object: a scoped no-go/upper-bound certificate for the nonuniform circuit complexity of H_N^{SAT} at threshold N^{1+epsilon-o(1)}.
- controlled interface: the parser pi_N -> Q_pi records touched SAT occurrences, local Boolean constraints, explicit equality edges, extension definitions, decoder openings, and the syntactic forced-row set F_pi.
- target-preserving condition: acceptance is occurrence-local, the adaptive-cover decoder and sparse-row patches are realized in the same nonuniform circuit model as C(H_N^{SAT}), and no hidden SAT oracle or advice-selected hard row is imported.

## Assumptions

- Model: EF+SAT_U^{occ} rules inspect only named occurrence atoms, extension variables, and recorded equality edges; real formula identity is unavailable unless present in Q_pi.
- Regime: M_N<=N^{q+o(1)}, G_N has circuit overhead N^{rho+o(1)}, and each SAT query has length L_N=(log N)^d.
- Uniformity ledger: the parser is deterministic and polynomial in |pi_N|, while the negative upper bound may hardwire the fixed transcript pi_N because the target circuit lower bound is nonuniform.
- Low-cover ledger: the row decoder induced by pi_N has adaptive cover exponent alpha_ad=max{tau,max_l(a_l+mu_l),max_l omega_l}.
- Binding hypothesis: for every x outside F_pi union R_N, the decoded row parity equals the true value H_N^{SAT}(x); if this fails, the transcript is a semantic-spoof falsifier instead of a lower-bound certificate.
- Patch regime: a complete bad row can be corrected in O(N^{1+o(1)}) gates in the chosen row-circuit accounting.

## Equations

- beta_zero_xor_carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\quad M_N\le N^{q+o(1)},\quad L_N=(\log N)^d`. Valid when: Valid when G_N is the fixed uniform beta-zero SAT-query generator and M_N,N,L_N are measured in the same padded length convention.
- adaptive_cover_cap: `\alpha_{ad}=\max\{\tau,\max_\ell(a_\ell+\mu_\ell),\max_\ell\omega_\ell\}`. Valid when: Applies when the adaptive cover family lists all certificate openings used by the row decoder and no advice-dependent opening is omitted.
- forcedrow_patch_upper_bound: `C(H_N^{SAT})\le N^{\max\{\rho,q+\alpha_{ad},\max(f,r)+1\}+o(1)}`. Valid when: Requires row-parity binding outside R_N union F_pi, same nonuniform circuit model for patches, and low-cover decoding without extra advice.
- threshold_consequence: `C(H_N^{SAT})>N^{1+\epsilon-o(1)}\ \wedge\ \rho,q+\alpha_{ad}<1+\epsilon\ \Rightarrow\ \max(f,r)\ge \epsilon-o(1)`. Valid when: Valid when the asserted source lower bound is C(H_N^{SAT})>N^{1+epsilon-o(1)} and overhead exponents are below that target threshold.

## Attempted Derivation

- Normalize pi_N so every proof line is either a local Boolean inference, an extension definition, a recorded equality between occurrence atoms, or a decoder-opening statement.
- Parse pi_N into Q_pi=(Occ,Eq,Ext,Con,Open), where Con is the finite set of Boolean relations actually checked by the transcript verifier.
- Define LocSat(Q_pi) as all Boolean assignments satisfying Eq, Ext, and Con. Define F_pi syntactically by constancy of row parity over LocSat(Q_pi). This definition is inspectable and does not mention C(H_N^{SAT}).
- For x not in F_pi, choose a,b in LocSat(Q_pi) with opposite parity on row x. Because every verifier check is a relation in Q_pi, replacing the private row labels by a or b preserves transcript acceptance. Thus any certification of true SAT parity for x is not justified by occurrence-local acceptance alone.
- If a separate row-parity binding lemma proves that the decoder is correct on every x outside F_pi union R_N, build D_N using G_N and the adaptive-cover opener. Its size is N^{max{rho,q+alpha_ad}+o(1)}.
- Patch the exceptional rows T_N=F_pi union R_N by hardwiring their complete row tables. Lemma L3 gives C(H_N^{SAT})<=N^{max{rho,q+alpha_ad,max(f,r)+1}+o(1)}.
- Compare with the asserted source lower bound N^{1+epsilon-o(1)}. If rho,q+alpha_ad<1+epsilon and max(f,r)<epsilon, the certificate route contradicts its own target; if binding is absent, the private-row spoof is the falsifier.

Blocking gap: The proof is complete only for the normalized occurrence-local verifier. The remaining named gap is Full-EFSAT-Extraction: real EF+SAT_U may share formula syntax or SAT axioms in ways not captured by private occurrence labels, and preservation of alpha_ad and F_pi is unproved.

## Falsifiers

- falsifier: ForcedRows(Q_pi) is defined using true SAT values or the desired circuit lower bound, making the parser circular.
- falsifier: an EF+SAT_U^{occ} rule reads global formula identity not recorded as an equality edge in Q_pi, invalidating private-row perturbation.
- falsifier: the adaptive-cover decoder omits an advice-dependent opener, so q+alpha_ad understates the circuit upper bound.
- falsifier: row-parity binding fails outside F_pi union R_N; then the accepted transcript is locally consistent but semantically spoofable.
- falsifier: rho>=1+epsilon or q+alpha_ad>=1+epsilon, so the threshold comparison gives no contradiction.
- falsifier: complete-row patching costs more than N^{1+o(1)} in the intended target model, so the residual exponent r+1 is miscalibrated.

## Learning

Cycle 81 upgrades the forced-row packet from a slogan to a syntactic parser theorem for EF+SAT_U^{occ}: ForcedRows is constancy of row parity over LocSat(Q_pi), so nonforced rows give a private-label spoof, while valid row-parity binding plus low adaptive cover gives the upper bound N^{max{rho,q+alpha_ad,max(f,r)+1}+o(1)}. The contribution is a scoped falsifier and proof-boundary theorem, not progress on the main P != NP conjecture.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch needs a concrete target-preserving test of whether forced-row density is a syntactic proof obligation or merely semantic handwaving in the beta-zero XOR packet.
- Situation seed: Take a padded SAT-query family G_N(x,j) with M_N=N^{q+o(1)} and create an EF+SAT_U^{occ} transcript whose SAT atoms are private occurrence labels z_{x,j,u}; duplicate one row x* into two private labelings with opposite XOR parity but identical local constraint satisfaction.
- Varied variable: forced-row density f where |F_pi|=N^{f+o(1)}.
- Held-fixed controls: G_N overhead rho and query count exponent q are fixed., Adaptive-cover exponent alpha_ad is fixed and advice-free., The verifier is restricted to occurrence-local rules with explicit equality edges., Sparse residual size r and same-model row-patch cost N^{1+o(1)} are fixed.
- Expected observation: For f<epsilon and r<epsilon, either the transcript remains accepted under the private-row parity flip, showing a semantic-spoof falsifier, or a decoder correct off F_pi union R_N gives C(H_N^{SAT}) below N^{1+epsilon-o(1)}.
- Transfer certificate needed: A formal parser proving Q_pi completeness for the verifier, a row-parity binding lemma for nonexceptional rows, and a same-model sparse patch lemma before the intuition may affect proof obligations.

## Next Experiment

Write the normalized EF+SAT_U^{occ} rule table and verify, rule by rule, that every acceptance predicate is captured in Q_pi; then attempt the row-parity binding lemma with F_pi defined as LocSat constancy and record the first counterexample if binding fails.
