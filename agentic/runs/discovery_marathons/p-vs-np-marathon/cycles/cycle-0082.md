# cycle-0082

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Row-normal EF+SAT_U^{occ} parser-forcing lemma: any accepted functional certificate for C(H_N)>N^{1+epsilon-o(1)} must syntactically force N^{epsilon-o(1)} complete source rows, or a private-label spoof yields a subthreshold circuit falsifier.

## Definitions

- source object: a row-normal EF+SAT_U^{occ} transcript pi for H_N(x)=xor_{j<=M_N} SAT(G_N(x,j)) with occurrence labels y_{x,j}.
- target object: a scoped no-go theorem for proof-mediated beta-zero XOR certificates, not a proof of P != NP.
- controlled interface: beta-zero compact generator, M_N<=N^{q+o(1)}, L_N=(log N)^d, overhead N^{rho+o(1)}, and occurrence-local proof access.
- target-preserving condition: q,rho<1+epsilon and the parser/spoof construction uses no SAT-circuit advice, so the valid target transfer remains unchanged.
- Q_pi is the finite dependency graph of occurrence labels, extension definitions, and explicit row-parity forcing declarations parsed from pi.
- ForcedRows(pi) is the syntactically inspectable set of x whose full row parity xor_j y_{x,j} is declared or derived in row-normal form.

## Assumptions

- Model is row-normal EF+SAT_U^{occ}: any parity-sensitive complete-row dependency must be exposed by an inspectable row-parity node.
- Functional soundness ranges over all occurrence-label assignments satisfying Q_pi, not only over the real SAT labeling.
- Private labels may be changed independently on unforced rows while preserving every parsed line of pi.
- The claimed source lower bound is C(H_N)>N^{1+epsilon-o(1)} in unrestricted nonuniform circuits on N-bit source inputs.

## Equations

- beta0_transfer: `C(H_N^{SAT}) <= N^{rho+o(1)} + M_N L_N^c = N^{max{rho,q}+o(1)}`. Valid when: Valid when SAT has size L_N^c circuits and the beta-zero generator uses M_N=N^{q+o(1)} queries.
- sparse_row_patch: `C(H_N) <= S_D + O(E_N N)`. Valid when: Valid when D_N is an explicit circuit and errors are at most E_N source inputs.
- forced_row_threshold: `|ForcedRows(pi)| >= N^{epsilon-o(1)}`. Valid when: Valid when the row-normal parser and private-label invariance assumptions are established.

## Attempted Derivation

- Parse pi into Q_pi by listing occurrence labels, extension equations, rule justifications, and explicit complete-row parity nodes; this is independent of the desired lower bound.
- For x not in ForcedRows(pi), flip or set y_{x,j} privately so xor_j y_{x,j}=0 while preserving all row-normal dependencies appearing in Q_pi.
- Define spoofed carrier H^A to be zero off ForcedRows(pi); equality gates patch the forced rows, giving size O(|ForcedRows(pi)|N)+N^{o(1)}.
- Functional soundness would accept pi for H^A, so if |ForcedRows(pi)|<N^{epsilon-o(1)} it certifies hardness for an easy function, contradiction.

Blocking gap: The derivation is valid for row-normal occurrence-local transcripts; full EF+SAT_U may use real SAT syntax to create nonrelativizing dependencies not represented by Q_pi.

## Falsifiers

- falsifier: a transcript with fewer than N^{epsilon-o(1)} forced rows and row-normal invariance gives a valid subthreshold spoof circuit.
- falsifier: hidden extension gates computing row parity without syntactic exposure break the parser lemma and force a restriction of the theorem.
- falsifier: SAT-semantic rules using formula syntax rather than occurrence labels evade private-label flips and require nonrelativizing extraction.
- falsifier: q or rho reaching 1+epsilon collapses the target-preserving beta-zero transfer window.

## Learning

Cycle 82 upgrades the proof-delivery packet by isolating a row-normal parser theorem: occurrence-local functional certificates are valid only if they force N^{epsilon-o(1)} complete rows. The remaining gap is exactly full EF+SAT_U semantic-to-occurrence extraction.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the row-forcing threshold.`
- Rationale: The route needs a concrete test of whether sparse forced rows are enough to refute occurrence-local certificates, rather than another abstract barrier statement.
- Situation seed: Take a beta-zero XOR carrier with M_N=N^q generated polylog SAT instances per source row and a row-normal EF+SAT_U^{occ} transcript pi that declares E_N complete row parities.
- Varied variable: kappa where E_N=N^kappa, varied across kappa<epsilon, kappa=epsilon, and kappa>epsilon.
- Held-fixed controls: q,rho<1+epsilon so target transfer is valid., Occurrence labels are private off declared complete rows., Functional soundness is over all satisfying occurrence-label assignments., Patch cost is O(E_N N) for N-bit source rows.
- Expected observation: For kappa<epsilon, the spoofed carrier has circuits N^{1+kappa+o(1)}, contradicting any valid N^{1+epsilon-o(1)} functional certificate; the threshold is sharp at kappa=epsilon.
- Transfer certificate needed: A formal parser-invariance certificate showing unforced rows can be privately relabeled while every line of the row-normal transcript remains accepted.

## Next Experiment

Construct the smallest EF extension-rule countermodel that hides row parity without a row-normal node, or prove a normalization that exposes such parity with subthreshold overhead.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For the beta-zero XOR carrier, the EF+SAT_U^{occ} ForcedRows theorem lifts to full EF+SAT_U only under a row-syntax-realizability extractor. The extractor must turn a full transcript pi into complete forced rows R_pi such that private perturbations outside R_pi are realizable by valid shared formula syntax. Without this extractor, shared-DAG equality is a finite falsifier to the occurrence-local invariance step.

## Definitions

- source object: a full EF+SAT_U proof transcript pi for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), where full means SAT_U arguments are real formulas or extension-DAG nodes, not private occurrence labels.
- target object: a scoped row-forcing no-go theorem saying any sound beta-zero XOR certificate either forces |R_pi|>=N^{epsilon-o(1)} complete rows or admits a sparse-row spoof/patch circuit below the claimed source lower bound.
- controlled interface: a syntactic parser E_full(pi) producing Q_pi, the shared dependency hypergraph Dep_pi, complete forced rows R_pi, and the allowed perturbation family A_Q without using the target lower bound as an oracle.
- target-preserving condition: every charged row j must correspond to the length-N row function R_j(x)=SAT(G_N(x,j)), the patch cost must be O(N) per charged row, and every perturbation outside R_pi must satisfy all full EF extension and substitution equations.
- EF+SAT_U^{occ}: the restricted model in which each SAT_U occurrence carries a private label and occurrence-local rules cannot compare labels except through the accepted view.
- full EF+SAT_U: extended Frege plus a universal SAT predicate over actual formula encodings, with equality, substitution, and shared extension definitions enforcing consistency between repeated subformulas.
- complete row: the whole truth table x -> SAT(G_N(x,j)) for a fixed j, not a single touched SAT_U argument or formula bit.

## Assumptions

- The beta-zero XOR carrier has M_N<=N^{q+o(1)}, formula length L_N=(log N)^d, and generator overhead N^{rho+o(1)}.
- The source lower-bound claim under audit is C(H_N^SAT)>N^{1+epsilon-o(1)} for a named nonuniform circuit model with row lookup patch cost O(N).
- The occurrence-local ForcedRows theorem is valid only in EF+SAT_U^{occ}, where private-label perturbations preserve accepted transcripts outside charged rows.
- The full extractor must be uniform or advice-free at the proof-parser level; nonuniform row advice is counted as leakage and cannot certify target-preserving transfer.
- Soundness used for the lift must be row-view soundness or DirectClusterSound, not ordinary local consistency alone.

## Equations

- beta_zero_xor_carrier: `H_N^{SAT}(x)=\bigoplus_{j=1}^{M_N} SAT(G_N(x,j)),\quad M_N\le N^{q+o(1)},\quad |G_N(x,j)|=(\log N)^d.`. Valid when: Valid when the source object is the fixed beta-zero XOR carrier and N denotes the truth-table length of the outer function.
- row_definition: `R_j(x)=SAT(G_N(x,j)),\qquad H_N^{SAT}=\bigoplus_{j\le M_N} R_j.`. Valid when: Valid when rows are complete length-N functions indexed by j and not individual proof occurrences or formula-bit queries.
- syntax_realizability_gate: `\mathrm{Lift}_{full}(\pi)\Rightarrow \forall A_Q\ \exists \sigma_A\,[\sigma_A\models \mathrm{DAG}_{G_N}\ \wedge\ \mathrm{view}_{\pi}(\sigma_A)=A_Q|_{\mathrm{view}_{\pi}}].`. Valid when: Valid when A_Q ranges over private perturbations claimed by the occurrence invariance proof and sigma_A must satisfy all full EF extension equations.
- sparse_row_patch: `C(H_N^{SAT})\le S_D+c\,|R|N+N^{o(1)}.`. Valid when: Applies after a circuit D of size S_D agrees with H_N^{SAT} after deleting residual complete rows R, and each residual row truth table is hardwired by O(N) gates.
- forced_row_threshold: `|R_\pi|\ge \frac{N^{1+\epsilon-o(1)}-S_D}{cN}=N^{\epsilon-o(1)}\quad \text{if } S_D=N^{1+o(1)}.`. Valid when: Requires the claimed source lower bound, the sparse patch inequality, and a parser whose charged objects are complete patchable rows.

## Attempted Derivation

- Start from the cycle-81 EF+SAT_U^{occ} theorem: row-view-sound accepted transcripts either force N^{epsilon-o(1)} private complete rows or admit a sparse-row spoof circuit.
- Attempt to interpret each full EF+SAT_U SAT_U call as a private occurrence label and reuse the private perturbation A_Q outside ForcedRows(pi).
- Define Q_pi as the visible proof-view atoms, row indices, formula-bit labels, and SAT_U argument occurrences extracted from pi.
- Try to preserve the accepted transcript under A_Q by changing unforced row labels while leaving Q_pi fixed.
- The preservation step needs a full-syntax realization sigma_A satisfying all extension equations for G_N and all equality/substitution rules used by pi.
- A finite shared-DAG fragment e1=e2=y blocks this step: A_Q may flip e1 but not e2, which is allowed in the occurrence model but impossible in full EF+SAT_U.
- Therefore TouchedRows(pi) and private ForcedRows_occ(pi) are not target-preserving complete rows in full syntax unless a row-syntax extractor charges every visible cross-row dependency.
- If such an extractor E_full exists and satisfies RowSep(pi,R_pi), the occurrence theorem plus sparse patching gives |R_pi|>=N^{epsilon-o(1)}.
- No proof of RowSep for standard full EF+SAT_U and the actual generator syntax is currently available; the valid theorem remains restricted to EF+SAT_U^{occ}.

Blocking gap: RowSyntaxRealizability(E_full): prove that every private perturbation outside charged complete rows is realizable by a valid full EF+SAT_U shared formula-DAG assignment, or exhibit the exact shared dependency that must be charged.

## Falsifiers

- falsifier: a shared extension variable y feeding two SAT_U occurrences makes independent private-label perturbation syntactically invalid in full EF+SAT_U.
- falsifier: a transcript touching one formula bit in each of many rows can have many TouchedRows but zero complete ForcedRows, so the sparse patch threshold cannot be charged.
- falsifier: ordinary proof soundness or local consistency accepts odd-charge Tseitin-style local views without DirectClusterSound, giving density without usefulness.
- falsifier: if D agrees with H_N^SAT off a subthreshold complete-row set R, then C(H_N^SAT)<=S_D+O(|R|N), contradicting any claimed N^{1+epsilon-o(1)} source lower bound.
- falsifier: nonuniform row advice inside E_full can select hard rows directly and is not a valid target-preserving proof-parser interface.

## Learning

Cycle 82 converts the full EF+SAT_U gap into a precise extractor obstruction. The EF+SAT_U^{occ} row-forcing theorem is valid only because occurrence labels are private. Full EF+SAT_U shares formula syntax, so private-label invariance needs row-syntax-realizability; shared-DAG equality is a finite falsifier to any automatic lift. This is route-level proof-boundary progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for full EF+SAT_U extraction.`
- Rationale: The branch no longer needs another abstract barrier restatement; the live gap is whether shared generator syntax invalidates private occurrence perturbations while preserving the beta-zero XOR target.
- Situation seed: Use the same H_N^SAT carrier but encode G_N in full EF+SAT_U by a shared extension-DAG. Insert a block of B rows whose SAT_U argument encodings share a visible sub-DAG Z_x, then compare the EF+SAT_U^{occ} parser with a full-syntax parser.
- Varied variable: lambda, the maximum number of distinct row indices whose visible SAT_U arguments share one extension-DAG node.
- Held-fixed controls: M_N<=N^{q+o(1)}, L_N=(log N)^d, and generator overhead N^{rho+o(1)} are unchanged., The target lower-bound audit remains C(H_N^SAT)>N^{1+epsilon-o(1)} with O(N) patch cost per complete row., No nonuniform row advice is allowed in the parser or perturbation selection., DirectClusterSound or row-view soundness is held fixed; ordinary soundness alone is not upgraded.
- Expected observation: At lambda=1, row-local syntax should permit the occurrence proof to lift. For lambda>1, independent private perturbations fail unless the parser charges every row incident to the shared node; if the charge is subthreshold, sparse patching becomes a valid falsifier.
- Transfer certificate needed: A row-syntax separation theorem mapping every visible shared-DAG dependency to complete charged rows R_pi, proving perturbation realizability outside R_pi and preserving the O(N) per-row patch threshold.

## Next Experiment

Instantiate E_full on a toy full EF+SAT_U transcript with two rows sharing one extension sub-DAG; compute Dep_pi, the minimum row boundary B_pi, and whether every private perturbation outside B_pi has a valid full-syntax realization.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For equality-free EF+SAT_U^{occ}, an accepted transcript pi is invariant under every private occurrence-label assignment in LocSat(Q_pi). Hence valid row-parity binding forces certified rows into F(Q_pi); small F plus low adaptive cover yields a patch upper bound, while nonforced rows give a spoof falsifier.

## Definitions

- source object: accepted equality-free EF+SAT_U^{occ} transcript pi for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N<=N^{q+o(1)} and generator overhead N^{rho+o(1)}.
- target object: scoped route-specific no-go theorem: low-cover proof-mediated beta-zero XOR certificates cannot certify C(H_N^SAT)>N^{1+epsilon-o(1)} when the patch exponent is below 1+epsilon.
- controlled interface: parser pi -> Q_pi, LocSat(Q_pi), ForcedRows F(Q_pi), residual set R_pi, and adaptive-cover exponent alpha_ad for opening certificate-controlled row parities.
- target-preserving condition: same N and same unrestricted circuit target are used; G_N is uniform, occurrence labels are not advice-selected hard rows, and row patches are charged in the same nonuniform circuit model.
- Q_pi records exactly the SAT_U occurrence atoms, local rule premises, claimed row parities, and explicit occurrence equalities present in pi.
- LocSat(Q_pi) is the set of private Boolean labelings of parsed occurrences satisfying all local constraints and containing the true SAT labeling as a valid member.
- F(Q_pi) consists of complete rows whose XOR parity is constant over LocSat(Q_pi), not rows merely mentioned by the transcript.

## Assumptions

- Psys is equality-free EF+SAT_U^{occ}: rule checking can inspect occurrence names and parsed local clauses, but cannot compare unparsed real SAT formulas extensionally.
- Row-parity binding is semantic over LocSat(Q_pi): an accepted certificate claiming row bit b for x is valid only if every A in LocSat(Q_pi) gives parity b for x.
- The low-cover decoder computes certified parities outside F(Q_pi) union R_pi with size N^{q+alpha_ad+o(1)} and uses no advice depending on a hard row selector.
- Let |F(Q_pi)|<=N^{f+o(1)} and |R_pi|<=N^{r+o(1)}; patching a row costs O(N^{1+o(1)}) gates in the target unrestricted circuit model.

## Equations

- forced_rows: `F(Q_pi)={x in [N] : |{ xor_{j<=M_N} A_{x,j} : A in LocSat(Q_pi)}|=1}`. Valid when: Valid when Q_pi is the parsed occurrence constraint graph and LocSat ranges over private occurrence-label assignments satisfying exactly those parsed local constraints.
- patch_upper_bound: `C(H_N^SAT) <= N^{rho+o(1)}+N^{q+alpha_ad+o(1)}+N^{max(f,r)+1+o(1)}`. Valid when: Applies after the low-cover decoder computes all nonforced nonresidual rows and forced or residual rows are patched in the same unrestricted circuit model.
- collapse_test: `max{rho,q+alpha_ad,max(f,r)+1}<1+epsilon => C(H_N^SAT)<N^{1+epsilon-o(1)}`. Valid when: Requires the intended source claim be an unrestricted circuit lower bound at exponent 1+epsilon for this same beta-zero XOR family.

## Attempted Derivation

- Parse pi line by line into Q_pi: every oracle atom becomes an occurrence variable; every local premise becomes a constraint; explicit copied labels are edges, while unmentioned formula equality is deliberately absent.
- Induct on EF+SAT_U^{occ} rules. Because each rule verifier reads only parsed occurrence labels and local clauses, any A in LocSat(Q_pi) makes the same transcript locally valid; this proves private-label invariance for the restricted Psys.
- If x is not in F(Q_pi), choose A,A' in LocSat(Q_pi) with opposite row XOR. Invariance keeps pi accepted under both, so a certificate claiming a fixed row parity for x is not row-parity binding; this is the spoof falsifier.
- For rows outside F(Q_pi) union R_pi, use the low adaptive-cover decoder; patch F(Q_pi) union R_pi by lookup rows and add generator overhead. This gives the displayed upper bound and threshold collapse test.

Blocking gap: Full EF+SAT_U may encode real formula identity, sharing, or substitution congruence that creates cross-occurrence constraints absent from Q_pi; the occurrence-local parser must either record them or the theorem cannot cover full EF+SAT_U.

## Falsifiers

- If LocSat(Q_pi) is empty, ForcedRows is vacuous; the parser must prove the true SAT labeling is a valid member before using constancy.
- An allowed congruence rule comparing G_N(x,j) and G_N(x',j') outside occurrence names breaks private-label invariance and falsifies the equality-free theorem scope.
- If alpha_ad or max(f,r)+1 reaches 1+epsilon, the patch bound is not subthreshold and gives no contradiction to the claimed lower bound.
- If the claimed consequence is only uniform hardness, the nonuniform row patch is not a valid refutation; the target model must be unrestricted circuits.

## Learning

Cycle 82 moves the ForcedRows packet from semantic intuition to a restricted proof fork: equality-free occurrence-local certificates have private-label invariance, so valid row-parity binding forces syntactic row constancy. The exact escape is nonlocal formula identity in full EF+SAT_U.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The live gap is not another barrier slogan but whether private occurrence labels really create a spoof or a patch circuit in the named Psys.
- Situation seed: Fix a padded SAT-query family G_N and an equality-free EF+SAT_U^{occ} transcript pi whose local constraints touch all certificate labels but leave most complete XOR rows privately assignable.
- Varied variable: forced-row exponent f where |F(Q_pi)|=N^{f+o(1)}.
- Held-fixed controls: M_N<=N^{q+o(1)} and generator overhead N^{rho+o(1)} are fixed., Adaptive-cover exponent alpha_ad and residual exponent r are fixed., The true SAT labeling is required to lie in LocSat(Q_pi)., No rule may compare real SAT formulas except through parsed occurrence labels.
- Expected observation: As f crosses 1+epsilon-1, the patch term changes from a valid lower-bound falsifier to a harmless upper bound; below the threshold, nonforced rows admit private-label spoofing.
- Transfer certificate needed: A formal parser theorem proving Q_pi completeness for the restricted rule list, plus an extraction boundary showing which full EF+SAT_U rules add nonlocal constraints.

## Next Experiment

Write the minimal EF+SAT_U^{occ} rule list and run the induction case check for extension, cut, oracle-axiom, copy, and claimed-row-output rules; record the first rule that needs real formula identity.
