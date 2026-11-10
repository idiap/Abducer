# cycle-0080

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Scoped theorem for Psys=EF+SAT_U^{occ}: let pi be an accepted occurrence-local, functionally sound certificate asserting C(H_N^SAT)>s_N with s_N=N^{1+epsilon-o(1)}. Let Q_pi be the parsed occurrence object, S_Q its evaluator cost, and R=ForcedRows(Q_pi). If S_Q+O(|R|N)<s_N, then pi is invalid under a private occurrence-label spoof. Hence every valid occurrence-local functional certificate at this threshold must satisfy |ForcedRows(Q_pi)|>=Omega((s_N-S_Q)/N)=N^{epsilon-o(1)} when S_Q=o(s_N).

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) on N-bit source rows x, with M_N<=N^{q+o(1)} and generated formulas of length L_N=(log N)^d.
- target object: a scoped no-go/extraction theorem for Psys=EF+SAT_U^{occ} certificates that claim C(H_N^SAT)>N^{1+epsilon-o(1)} as input to beta=0 magnification.
- controlled interface: occurrence labels a_{x,j} replace SAT(G_N(x,j)); a transcript pi is parsed to Q_pi=(T_pi,row-tags,local equations) and can inspect only these labels through occurrence-local rules.
- target-preserving condition: the theorem preserves the beta=0 transfer only for q,rho<1+epsilon and treats private occurrence-label spoofing as a falsifier of the certificate route, not as a circuit for real SAT.
- ForcedRows(Q_pi) is the set of rows x whose parity xor_j a_{x,j} is fixed by Q_pi under all occurrence-label completions; in the atomic occurrence model this requires all row labels to be touched or an explicit locally derived row-parity tag.
- S_Q is the size of the nonuniform circuit that evaluates the parsed finite object Q_pi and the spoofed default predicate; equality patching on E source rows costs O(EN) gates.

## Assumptions

- Generator G_N is available to the carrier circuit with size N^{rho+o(1)}, and the SAT-query length is beta=0, namely L_N=(log N)^d.
- Psys=EF+SAT_U^{occ} is occurrence-local: rule validity is invariant under arbitrary replacements of occurrence labels outside Q_pi, with no appeal to real formula semantics except through listed occurrence labels.
- Functional soundness: an accepted certificate for C(H_A)>s_N must be valid for every occurrence-label completion A consistent with Q_pi, not only for the real SAT label vector.
- The proof-size/parser overhead satisfies S_Q<s_N-O(|R|N); otherwise the certificate is too large to support the barely-superlinear source claim.
- Circuit model is nonuniform Boolean circuits over N-bit source inputs; a row patch for a listed x uses an equality test of size O(N).

## Equations

- occurrence carrier: `H_A(x)=\bigoplus_{j\le M_N} a_{x,j}`. Valid when: Valid when A is an arbitrary occurrence-label assignment over U_N and the row parity carrier is defined syntactically.
- sparse-row spoof upper bound: `C(H_{A^0})\le S_Q+O(|ForcedRows(Q_\pi)|\,N)`. Valid when: Valid when Q_pi is occurrence-local, S_Q bounds its evaluator, and only forced rows remain nonzero after spoofing.
- forced-row threshold: `|ForcedRows(Q_\pi)|\ge \Omega((s_N-S_Q)/N)`. Valid when: Valid when pi is functionally sound for all completions consistent with Q_pi and the claimed lower bound threshold is s_N.
- beta-zero target substitution: `C(H_N^{SAT})\le N^{\rho+o(1)}+M_N L_N^c=N^{\max\{\rho,q\}+o(1)}`. Valid when: Valid when SAT has circuits of size n^c, L_N=(log N)^d, and the generator circuit has size N^{rho+o(1)}.

## Attempted Derivation

- Define U_N={(x,j):x in {0,1}^N, j<=M_N} and replace each SAT(G_N(x,j)) by an independent occurrence label a_{x,j}.
- Parse an accepted occurrence-local transcript pi into Q_pi by collecting every queried occurrence, every locally derived equation, and every explicit row-parity tag; define ForcedRows(Q_pi) as rows whose parity is fixed under all completions of Q_pi.
- Prove parser invariance by induction on the EF+SAT_U^{occ} derivation: each rule depends only on premises already in Q_pi, so preserving Q_pi preserves acceptance.
- For every unforced row choose a private completion making xor_j a_{x,j}=0 while preserving Q_pi; forced rows keep their Q_pi-determined parity.
- The spoofed carrier H_{A^0} is supported on R=ForcedRows(Q_pi), so a nonuniform circuit hardwires R and uses O(N)-size equality tests to patch those rows, with total size S_Q+O(|R|N).
- If pi is functionally sound for the claimed lower bound s_N, then H_{A^0} must have circuit complexity greater than s_N; the patch circuit contradicts this whenever S_Q+O(|R|N)<s_N.
- Conclude that any valid occurrence-local functional certificate at the N^{1+epsilon-o(1)} threshold must force N^{epsilon-o(1)} complete rows, unless it is nonfunctional, nonconstructive, too large, or uses real SAT semantics outside EF+SAT_U^{occ}.

Blocking gap: The derivation is valid for EF+SAT_U^{occ}. It is blocked for full EF+SAT_U by the missing extraction lemma from real SAT semantic derivations to syntactic row forcing; full EF may use formula structure in a nonrelativizing way that private occurrence-label spoofing does not preserve.

## Falsifiers

- Subthreshold forced rows: |ForcedRows(Q_pi)|<N^{epsilon-o(1)} with S_Q=o(N^{1+epsilon}) yields a sparse-row patch circuit and is a direct falsifier for the claimed occurrence-local certificate.
- Parser leakage: if Q_pi contains a truth table, a SAT solver, or H_N advice, then S_Q must be charged; if charged size is subthreshold it falsifies the source lower bound, otherwise the certificate is not barely-superlinear.
- Nonfunctional soundness: a certificate valid only for the real SAT label vector escapes the occurrence-label theorem but loses the functional naturalization/no-go claim until a nonrelativizing extraction is proved.
- Global parity equations: low-cost constraints fixing many row parities without touching complete rows falsify the atomic ForcedRows definition and require a parity-rank ForcedRows repair.
- Positive-beta transfer remains an independent falsifier: if any replacement carrier reintroduces query length n^beta with beta>0, the window q+beta c blocks all-exponent target separation.

## Learning

Cycle 80 discharges the scoped EF+SAT_U^{occ} proof packet: occurrence-local functional certificates for the beta-zero XOR carrier must force at least N^{epsilon-o(1)} complete parity rows, or a private occurrence-label spoof plus sparse-row equality patch gives a valid subthreshold falsifier. The live gap is no longer ordinary soundness; it is the full EF+SAT_U extraction of real SAT-semantic reasoning into syntactic ForcedRows, or a deliberate restriction of the paper theorem to EF+SAT_U^{occ}.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch has a theorem-shaped occurrence-local no-go; a concrete private-row spoof experiment tests the exact N^epsilon row-forcing threshold instead of restating barrier folklore.
- Situation seed: Take a beta-zero XOR carrier with M_N=N^q generated polylog SAT instances per row and an accepted EF+SAT_U^{occ} transcript pi whose parsed object Q_pi fully determines exactly E source rows while leaving one private occurrence free in every other row.
- Varied variable: E=|ForcedRows(Q_pi)|, varied from N^{epsilon}/log N to N^{epsilon}log N while keeping S_Q=N^{1+epsilon}/log^2 N.
- Held-fixed controls: L_N=(log N)^d and beta=0, so SAT circuits of size L_N^c contribute only N^{o(1)} per query., q,rho<1+epsilon, preserving the beta-zero target substitution window., Verifier is occurrence-local and functionally sound over all label completions consistent with Q_pi., Patch circuits are charged in ordinary nonuniform SIZE on N-bit source inputs.
- Expected observation: Below E=N^{epsilon-o(1)}, the spoofed carrier is supported on too few rows and has size below N^{1+epsilon-o(1)}; at or above the threshold the sparse-row falsifier no longer refutes the certificate by equality patching alone.
- Transfer certificate needed: A formal parser-invariance certificate for EF+SAT_U^{occ}; for full EF+SAT_U, an additional nonrelativizing extraction theorem showing that real formula semantics force complete rows or are charged as advice.

## Next Experiment

Attempt the full EF+SAT_U boundary lemma: inspect a standard encoding of SAT_U extension axioms and decide whether each semantic rule is occurrence-local, charges enough advice into S_Q, or yields a nonrelativizing complete-row extraction.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Strict occurrence-local EF+SAT_U^{occ} row-forcing theorem: fix T_N=N^{1+epsilon}. If an accepted transcript pi is row-view sound for the beta-zero XOR carrier and the parser closure is complete for occurrence constraints, then either |ForcedRows(pi)| >= (T_N-S_D)/(cN) for every decoy circuit D of size S_D, or the same accepted view is a falsifier because it has a completion whose induced row function has circuit size below T_N. With S_D<=N^{1+eta}, eta<epsilon, sound certificates force N^{epsilon-o(1)} rows. This is valid only for the strict occurrence-local model, not full EF+SAT_U.

## Definitions

- source object: EF+SAT_U^{occ} transcript pi accepted by a verifier V_N for H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)) with private occurrence labels (x,j).
- target object: scoped no-go/extraction theorem for claimed certificates of C(H_N^{SAT})>N^{1+epsilon} in the occurrence-local model.
- controlled interface: parser pi -> Q_pi, occurrence closure cl_occ(Q_pi), ForcedRows(pi), spoof completion A_Q, and sparse patch circuit P_{D,R}.
- target-preserving condition: the verifier and proof rules read only occurrence labels in Q_pi and declared local row-XOR gates, while the patch circuit preserves the same H_N length, generator G_N, and circuit-size threshold T_N.
- Complete/forced row: x is forced when the row parity vector for (x,1),...,(x,M_N) is syntactically determined inside cl_occ(Q_pi); in the pure label-read subcase this requires all M_N labels or an explicit row-XOR gate.
- Row-view soundness: no accepted transcript may remain accepted for an occurrence assignment A whose induced row function H_N^A has circuit size at most T_N.

## Assumptions

- N=2^n, M_N<=N^{q+o(1)}, formula length L_N=(log N)^d, and G_N is uniform with overhead N^{rho+o(1)}.
- The target model is nonuniform Boolean circuits on n=log N inputs with size threshold T_N=N^{1+epsilon}.
- Psys is the strict occurrence-local abstraction: real SAT formula equality, semantic satisfiability, and global EF extension variables are unavailable unless explicitly represented in Q_pi.
- Closure completeness holds: if x is not in ForcedRows(pi), there is an occurrence completion preserving cl_occ(Q_pi) that flips the row XOR at x.
- A decoy D_N on n inputs has circuit size S_D and can be imposed on every unforced row by setting one free occurrence bit in that row.
- Sparse patching uses hardwired exceptional rows and costs at most c|R|N gates in the audited circuit model.

## Equations

- occurrence_row_function: `H_N^{A}(x)=\bigoplus_{j\le M_N} A(x,j)`. Valid when: Valid when A is an occurrence assignment over the strict occurrence-local carrier and M_N is the audited XOR fan-in.
- forced_rows_linear_closure_proxy: `R_\pi=\mathrm{ForcedRows}(\pi)=\{x\in[N]: h_x\in \mathrm{cl}_{occ}(Q_\pi)\}`. Valid when: Valid when h_x denotes the explicit row-XOR symbol and closure completeness is part of the occurrence-local parser model.
- spoof_completion: `H_N^{A_Q}(x)=H_N^{SAT}(x)\mathbf{1}_{x\in R_\pi}+D_N(x)\mathbf{1}_{x\notin R_\pi}`. Valid when: Valid when every unforced row has a free occurrence bit that can be assigned after preserving the transcript view.
- sparse_patch_upper_bound: `C(H_N^{A_Q})\le S_D+c|R_\pi|N`. Valid when: Applies when exceptional rows are hardwired and equality tests fit within the audited nonuniform circuit model.
- row_forcing_threshold: `|R_\pi|\ge \frac{T_N-S_D}{cN}=N^{\epsilon-o(1)}\quad\text{if }T_N=N^{1+\epsilon},\ S_D\le N^{1+\eta},\eta<\epsilon`. Valid when: Requires row-view soundness, the spoof completion lemma, and a decoy circuit strictly below the claimed threshold.

## Attempted Derivation

- Fix strict EF+SAT_U^{occ}; replay pi and collect Q_pi, all cited occurrence bits, equality/copy links, and explicit row-XOR gates.
- Compute cl_occ(Q_pi). Define ForcedRows(pi) as rows whose row-XOR symbol h_x is fixed in this closure; this is syntactic and independent of C(H_N^{SAT}).
- Assume |R_pi| is small. Pick a decoy D_N of size S_D, e.g. constant zero or the best audited residual circuit.
- Build A_Q: on forced rows set occurrence bits to the actual SAT values; on every unforced row preserve all bits seen by pi and set one remaining free occurrence bit so that the row XOR equals D_N(x).
- Because V_N and every rule are occurrence-local, pi has exactly the same view under A_Q as under the actual SAT occurrence assignment; acceptance is invariant.
- The induced function H_N^{A_Q} equals H_N^{SAT} only on R_pi and equals D_N off R_pi, so the sparse patch circuit has size at most S_D+c|R_pi|N.
- Row-view soundness of the certificate says an accepted proof cannot exist for any completion whose induced function has circuit size <=T_N. Therefore c|R_pi|N+S_D>T_N.
- For T_N=N^{1+epsilon} and S_D<=N^{1+eta}, eta<epsilon, this yields |R_pi|>=N^{epsilon-o(1)}.

Blocking gap: The proof is valid for strict occurrence-local EF+SAT_U^{occ} with row-view soundness. It is blocked for full EF+SAT_U because real formula syntax and SAT_U semantics may create dependencies not preserved by private occurrence-label perturbations.

## Falsifiers

- Sparse-row spoof falsifier: if |ForcedRows(pi)|<N^{epsilon-o(1)} and D_N has size below N^{1+epsilon}, A_Q preserves the accepted occurrence view while inducing a small circuit.
- Odd-charge Tseitin falsifier: bounded affine local consistency can accept every small projection while the global system is unsatisfiable, so ordinary soundness is not DirectClusterSound.
- Full-syntax falsifier: a global EF equality between generated formulas can make two private occurrence perturbations invalid even when Q_pi records only one label.
- Naturalization falsifier: if DCS plus logarithmic projection is supplied, the accepting shadow is large, constructive, and useful, creating PRF/natural-proofs tension rather than a barrier escape.

## Learning

Cycle 80 upgrades the support branch from repeated barrier audit to a restricted proof packet: in strict occurrence-local EF+SAT_U^{occ}, row-view-sound beta-zero XOR certificates must force N^{epsilon-o(1)} rows or fall to a sparse-row spoof falsifier. The new exact gap is full EF+SAT_U extraction, not another natural-proofs slogan.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the forced-row theorem.`
- Rationale: The branch needs a concrete target-preserving test of whether occurrence-local certificates can avoid sparse-row spoofing without becoming natural properties.
- Situation seed: Use H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)) with a strict EF+SAT_U^{occ} transcript pi whose view touches only a closure Q_pi; replace unforced occurrence labels by a private assignment A_Q that makes off-row XORs equal a small decoy D_N.
- Varied variable: theta where |ForcedRows(pi)|=N^theta, with epsilon and decoy exponent eta held fixed.
- Held-fixed controls: M_N<=N^{q+o(1)} and L_N=(log N)^d are unchanged., The target lower-bound claim remains C(H_N^{SAT})>N^{1+epsilon}., The verifier is strict occurrence-local and sees the same Q_pi under SAT and A_Q., The decoy circuit size is S_D<=N^{1+eta} with eta<epsilon.
- Expected observation: For theta<epsilon-o(1), the patch size S_D+O(N^{1+theta}) is below T_N, so any accepted row-view-sound transcript is refuted. For theta>=epsilon-o(1), the sparse spoof no longer contradicts the claimed threshold.
- Transfer certificate needed: A formal invariance certificate that V_N(pi) depends only on cl_occ(Q_pi), plus a sparse patch implementation in the same circuit model; full EF+SAT_U additionally needs a syntax-to-occurrence extraction theorem.

## Next Experiment

Formalize the full EF+SAT_U extraction boundary: add formula-identity and extension-variable rules one at a time, then test whether A_Q transcript invariance fails by a minimal rule-level countermodel or yields an enlarged ForcedRows_full parser.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Occurrence-local forced-row cap: let Psys=EF+SAT_U^{occ} and let an accepted beta-zero XOR transcript pi parse to an advice-free low-cover row decoder D_pi and a syntactic forced-row set F_pi. If D_pi(x)=H_N^SAT(x) for all rows x notin F_pi, C(D_pi)<=N^{max{rho,q+alpha_ad}+o(1)}, and |F_pi|<=N^{f+o(1)}, then C(H_N^SAT)<=N^{max{rho,q+alpha_ad,1+f}+o(1)}. Thus any valid certificate claiming C(H_N^SAT)>N^{1+epsilon-o(1)} with rho,q+alpha_ad<1+epsilon must have f>=epsilon-o(1), or it is refuted by a sparse-row patch falsifier.

## Definitions

- source object: an EF+SAT_U^{occ} transcript pi for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with occurrence labels y_{x,j} and an adaptive label-cover profile alpha_ad.
- target object: a scoped route no-go theorem saying low-cover proof-mediated beta-zero XOR certificates cannot validly certify C(H_N^SAT)>N^{1+epsilon-o(1)} unless they force at least N^{epsilon-o(1)} complete rows.
- controlled interface: the parser pi -> (Q_pi,D_pi,F_pi) outputs the touched occurrence object Q_pi, the low-cover row-parity decoder D_pi(x)=xor_j a_pi(x,j), and ForcedRows F_pi requiring explicit semantic patching.
- target-preserving condition: the parser, decoder, and patch construction are uniform or advice-free except for hardwiring the fixed falsifying transcript in the negative direction, and all circuit upper bounds stay in the same unrestricted Boolean circuit model as the claimed lower bound.
- ForcedRows F_pi are syntactically identified rows whose semantic parity is not supplied by the low-cover decoder under the parser's row-parity binding rules.
- A sparse-row patch for F_pi is an unrestricted circuit that computes D_pi off F_pi and hardwires corrected row behavior on F_pi.

## Assumptions

- Model is the restricted occurrence-local proof system EF+SAT_U^{occ}; full EF+SAT_U is not covered unless complete-row forcing is extractable from real formula syntax.
- The generator G_N is uniform, has overhead N^{rho+o(1)}, and emits SAT instances of length polylog(N) in a beta-zero XOR family with M_N<=N^{q+o(1)} queries per row.
- The adaptive cover for pi has exponent alpha_ad=max{tau,max_l(a_l+mu_l),max_l omega_l} and supplies all labels needed by D_pi without advice-selected hard rows.
- Row-parity binding is assumed outside F_pi: for every x notin F_pi, the transcript syntactically certifies D_pi(x)=H_N^SAT(x) without circular reference to the target lower bound.
- Patch circuits are unrestricted Boolean circuits in the same size measure used by the claimed beta-zero lower bound.
- This is a route-level falsifier theorem; it is not a proof of P != NP.

## Equations

- beta-zero-query-ledger: `M_N \le N^{q+o(1)},\quad T_G(N) \le N^{\rho+o(1)}`. Valid when: Valid when the beta-zero generator family and query schedule are fixed uniformly for the length N instance.
- low-cover-decoder-bound: `C(D_\pi) \le N^{\max\{\rho,q+\alpha_{ad}\}+o(1)}`. Valid when: Applies when every row label used by the parity decoder is opened through the declared adaptive cover without extra advice.
- sparse-forced-row-patch: `C(H_N^{SAT}) \le C(D_\pi)+O(|F_\pi|N)`. Valid when: Requires row-parity binding on all rows outside F_pi and uses unrestricted row patches in the same circuit model.
- combined-cap: `|F_\pi|\le N^{f+o(1)}\Rightarrow C(H_N^{SAT})\le N^{\max\{\rho,q+\alpha_{ad},1+f\}+o(1)}`. Valid when: Valid after the low-cover decoder bound and the sparse forced-row patch bound are both established.
- forced-row-threshold: `C(H_N^{SAT})>N^{1+\epsilon-o(1)}\Rightarrow f\ge \epsilon-o(1)`. Valid when: Holds when rho and q plus alpha_ad are both below 1 plus epsilon by a fixed margin.

## Attempted Derivation

- Fix N and parse pi into Q_pi=(V_pi,E_pi,Cover_pi,Sem_pi); define D_pi by opening the labels used in the XOR row and define F_pi by syntactic row-parity binding clauses.
- Use the adaptive-cover normal form to build an unrestricted circuit for D_pi: compute G_N, enumerate M_N=N^{q+o(1)} row queries, open labels through the cover, and XOR them, giving exponent max{rho,q+alpha_ad}.
- Assume row-parity binding for all x notin F_pi. Then D_pi and H_N^SAT differ only on F_pi.
- Patch the forced rows by a row-lookup correction circuit of size O(|F_pi|N), obtaining C(H_N^SAT)<=N^{max{rho,q+alpha_ad,1+f}+o(1)} when |F_pi|<=N^{f+o(1)}.
- Compare with a claimed lower-bound certificate C(H_N^SAT)>N^{1+epsilon-o(1)}. If rho<1+epsilon, q+alpha_ad<1+epsilon, and f<epsilon, the transcript contradicts its own target claim.
- For rows not in F_pi and not parity-bound, apply the odd private-row perturbation. Acceptance is invariant in the occurrence-local model but D_pi(x) flips, so the transcript is a semantic spoof rather than a valid certificate.

Blocking gap: The parser and patch chain are theorem-shaped for EF+SAT_U^{occ}, but promotion needs a rule-by-rule proof that every accepted transcript either exposes row-parity binding clauses or is invariant under the private odd-row perturbation. Full EF+SAT_U also needs a separate extraction lemma from real SAT formula syntax to complete rows.

## Falsifiers

- falsifier: an accepted transcript with alpha_ad low, |F_pi|<N^{epsilon-o(1)}, and row-parity binding outside F_pi gives an explicit patch circuit below the claimed lower-bound threshold.
- falsifier: an odd private-row perturbation preserves EF+SAT_U^{occ} local checks while flipping D_pi(x), showing that local consistency is not semantic row binding.
- falsifier: a parser that defines ForcedRows by target hardness rather than proof syntax is circular and invalid for the proof-delivery queue.
- falsifier: nonuniform row selection or advice-chosen hard rows may certify isolated hard truth tables but does not transfer to a uniform language lower bound.
- falsifier: full EF+SAT_U formula-sharing rules that identify occurrences globally break the occurrence-local perturbation unless a complete-row extraction lemma is supplied.

## Learning

Cycle 80 converts the live parity-binding obligation into a sharp forced-row threshold: low-cover occurrence-local certificates with fewer than N^{epsilon-o(1)} semantically forced rows either yield a same-model patch upper bound or admit a private-row spoof. The contribution is a restricted-model falsifier packet and parser obligation, not progress on the main P != NP conjecture itself.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the EF+SAT_U^{occ} row-forcing theorem.`
- Rationale: The branch needs a concrete test of whether parity binding is syntactic or merely hoped for; another abstract hardness-magnification restatement would not close the proof-delivery queue gap.
- Situation seed: Take a beta-zero XOR family with M_N=N^{q+o(1)} SAT occurrences per row and a toy EF+SAT_U^{occ} transcript whose DCS-LC labels are opened by an adaptive cover of exponent alpha_ad. Mark F_pi rows as complete semantic openings and leave all other rows occurrence-private.
- Varied variable: The forced-row exponent f where |F_pi|=N^{f+o(1)}.
- Held-fixed controls: Generator overhead rho and query exponent q are fixed., Adaptive cover exponent alpha_ad is fixed below 1+epsilon-q., The proof rules are occurrence-local except for explicitly marked row-parity binding clauses., No advice-selected hard row or nonuniform selector is allowed in the positive direction.
- Expected observation: For f<epsilon, either the low-cover decoder plus F_pi patch yields a circuit below N^{1+epsilon-o(1)}, or an odd private-row flip preserves the transcript while changing an unforced row parity. Both outcomes refute the certificate route in the restricted model.
- Transfer certificate needed: A formal parser-invariance certificate: every Psys rule must be classified as local-invariant, cover-openable, or semantic row-binding, and the patch circuit must be in the same unrestricted circuit model as the target claim.

## Next Experiment

Instantiate the parser on a minimal EF+SAT_U^{occ} transcript with one XOR row and one DCS-LC cover opening; flip one private occurrence label, record exactly which rule first fails, and classify that rule as local-invariant or semantic row-binding.
