# cycle-0083

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Conditional row-normal occurrence no-go: Fix epsilon>0 and the beta-zero XOR carrier H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N<=N^{q+o(1)}, L_N=(log N)^d, and generator size N^{rho+o(1)}. Let pi be an accepted row-normal functional EF+SAT_U^{occ} certificate whose conclusion is C(H)>N^{1+epsilon-o(1)} for every occurrence-label assignment satisfying its parsed constraints Q_pi. If Q_pi is row-separable and |ForcedRows(Q_pi)|<N^{epsilon-o(1)}, then pi is not sound: there is a private occurrence-label assignment A_Q satisfying Q_pi for which the induced parity carrier has circuits of size N^{1+epsilon-o(1)}. Hence any valid certificate in this method class must force at least N^{epsilon-o(1)} complete parity rows, unless it exits by nonfunctionality, nonconstructivity, nonlargeness, or real SAT-semantic nonrelativization.

## Definitions

- source object: a row-normal EF+SAT_U^{occ} proof transcript pi over occurrence labels y_{x,j} attached to generated formulas G_N(x,j) in the beta-zero XOR carrier H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)).
- target object: a scoped route-specific no-go theorem for proof-mediated barely-superlinear source lower-bound certificates, not a proof of P != NP or NP not subset P/poly.
- controlled interface: the parser pi -> Q_pi exposes touched occurrence labels, row-local constraints, the set ForcedRows(Q_pi), and the functional conclusion C(H_A)>N^{1+epsilon-o(1)} over all label assignments A satisfying Q_pi.
- target-preserving condition: M_N<=N^{q+o(1)}, L_N=(log N)^d, generator size N^{rho+o(1)}, beta=0, max{q,rho}<1+epsilon, and the certificate is advice-free, functional over occurrence labels, and row-separable after parsing.
- Complete row: a source input x is complete-forced if the row parity xor_{j<=M_N} y_{x,j} is constant over all occurrence-label assignments satisfying Q_pi.
- ForcedRows(Q_pi): the set of complete-forced source rows; it is syntactically inspectable from Q_pi and does not refer to the desired lower bound.
- Row-separable Q_pi: after fixing global syntactic parameters, constraints on occurrence labels factor over rows, so every unforced row has two extensions with opposite parity while preserving Q_pi.

## Assumptions

- Circuit model is nonuniform Boolean SIZE with fan-in two gates; equality patching for one N-bit source row costs O(N).
- The proof system is the restricted occurrence-local EF+SAT_U^{occ,row} model: SAT facts are represented only by private occurrence labels and row-normal rules, not by real formula semantics.
- Functional soundness is parametric: if pi accepts Q_pi, the certified lower-bound conclusion applies to every occurrence-label assignment satisfying Q_pi.
- No hidden advice may encode the true SAT label vector or a row selector outside the parsed transcript; otherwise ForcedRows is not a valid observable.
- The beta-zero transfer is kept separate from the certificate no-go: SAT circuits substitute into labels only through polylog-length generated instances.
- This is a route-level obstruction theorem for a certificate family; it does not establish a lower bound for H_N^SAT itself.

## Equations

- beta_zero_transfer: `SAT in SIZE(n^c) => C(H_N^SAT) <= N^{rho+o(1)} + M_N L_N^c = N^{max{rho,q}+o(1)}`. Valid when: Valid when generated formulas have length L_N=(log N)^d, M_N<=N^{q+o(1)}, beta=0, and one SAT circuit of size L_N^c is reused uniformly across all generated instances.
- private_spoof_upper_bound: `C(H_{A_Q}) <= O(C(Q_pi)) + O(|ForcedRows(Q_pi)| N) + N^{o(1)}`. Valid when: Valid when Q_pi is row-separable, unforced row parities can be set to zero independently, and forced rows are patched by N-bit equality tests.
- forced_row_threshold: `C(H_{A_Q}) > N^{1+epsilon-o(1)} and C(Q_pi)=N^{o(1)} imply |ForcedRows(Q_pi)| >= N^{epsilon-o(1)}`. Valid when: Applies after functional certificate soundness transfers the same lower-bound conclusion to every private occurrence-label assignment satisfying the parsed row-normal constraints.

## Attempted Derivation

- Fix N, epsilon, q, rho with max{q,rho}<1+epsilon and define H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)).
- Parse an accepted row-normal transcript pi into Q_pi; define ForcedRows(Q_pi) as rows whose parity is fixed over all assignments satisfying Q_pi.
- Use parser invariance: acceptance of pi depends only on Q_pi, so any private label assignment A satisfying Q_pi preserves the accepted transcript.
- If Q_pi is row-separable, choose A_Q so every unforced row has parity 0 and every forced row has its Q_pi-forced parity.
- Build a circuit for H_{A_Q}: output 0 by default and patch the forced rows with equality tests; size is O(C(Q_pi))+O(|ForcedRows|N)+N^{o(1)}.
- Functional certificate soundness says the same accepted pi certifies C(H_{A_Q})>N^{1+epsilon-o(1)}. If |ForcedRows|<N^{epsilon-o(1)} and C(Q_pi)=N^{o(1)}, this contradicts the patch circuit.
- Therefore any sound row-normal functional occurrence-local certificate must force N^{epsilon-o(1)} complete rows, or leave the method class.

Blocking gap: The proof is conditional on a row-separable row-normal parser. Arbitrary full EF+SAT_U can use real formula semantics, and arbitrary occurrence-local EF may contain short cross-row parity constraints unless the calculus forbids or charges them.

## Falsifiers

- Row-separability falsifier: a short accepted occurrence rule imposes a global cross-row parity equation that zeroes many spoof choices while ForcedRows remains small.
- Functional-soundness falsifier: the certificate conclusion applies only to real SAT labels, so private occurrence-label spoofing no longer gives a contradiction.
- Sparse-row residual falsifier: a circuit D_N agrees with H_N^SAT off E<N^{epsilon-o(1)} source rows, giving C(H_N^SAT)<=C(D_N)+O(EN) below the claimed threshold.
- Nonuniform-advice falsifier: Q_pi or the verifier hides a selected set of hard rows or the SAT label vector, invalidating the advice-free parser.
- Positive-beta falsifier: if the carrier secretly uses target queries of length N^beta with beta>0, the substitution window becomes q+beta c and cannot exclude all SAT exponents.

## Learning

Cycle 83 upgrades the proof-delivery packet from a parser slogan to a conditional theorem: row-separable row-normal functional occurrence certificates must force N^{epsilon-o(1)} complete XOR rows, or private occurrence-label spoofing yields a valid subthreshold circuit for the induced carrier. The remaining open obligation is no longer ordinary soundness but the exact row-normalization/extraction step for broader EF+SAT_U.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the row-normal parser and transcript-invariance lemmas.`
- Rationale: The current proof item needs a concrete check that private row spoofing is not just a restatement of relativization folklore; it must expose exactly which occurrence-local rules preserve or break the contradiction.
- Situation seed: Take H_N^SAT(x)=xor_{j<=N^q} SAT(G_N(x,j)) with L_N=(log N)^d, q,rho<1+epsilon. Give the verifier a transcript pi whose Q_pi touches all labels in N^eta complete rows and only one label in every other row.
- Varied variable: eta=log_N |ForcedRows(Q_pi)|, varied from 0 to epsilon while q,rho,d and verifier size stay fixed.
- Held-fixed controls: beta=0 polylog target-query length and generator overhead N^{rho+o(1)}., Functional occurrence-label soundness: accepted pi must certify the same lower-bound statement for every A satisfying Q_pi., No hidden advice and no real SAT-semantic rule outside EF+SAT_U^{occ,row}., Equality patching cost O(N) per exceptional source row.
- Expected observation: For eta<epsilon the spoof assignment makes the induced parity function zero off N^eta rows and hence has size N^{1+eta+o(1)}, contradicting any valid N^{1+epsilon-o(1)} functional certificate. At eta>=epsilon the sparse-patch contradiction no longer fires.
- Transfer certificate needed: A formal parser-invariance certificate showing that every accepted transcript in the named proof system factors through Q_pi and that unforced row parities have independent extensions.

## Next Experiment

Instantiate the EF+SAT_U^{occ,row} rule ledger: for each extension, weakening, substitution, SAT_U occurrence axiom, and derived parity line, mark whether it is Q_pi-local, row-separable, or a charged cross-row constraint; the first uncharged cross-row rule becomes the countermodel or repair target.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Full EF+SAT_U lift-or-block gate: for beta-zero XOR certificates claiming C(H_N^{SAT})>N^{1+epsilon-o(1)}, the occurrence-local ForcedRows theorem lifts to full EF+SAT_U exactly under a row-syntax realizer preserving all queried formula-equality and SAT_U atoms outside Q_pi. Under that condition any sound accepted transcript has |Q_pi|>=N^{epsilon-o(1)} when the spoof circuit has size N^{1+o(1)}. Without this realizer, shared formula-DAG equality is a finite falsifier to automatic private-label invariance.

## Definitions

- source object: full EF+SAT_U proof transcript pi for H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)), with formula syntax shared across queried occurrences.
- target object: a scoped lift-or-block theorem for proof-mediated beta-zero XOR lower-bound certificates, not a proof of P != NP.
- controlled interface: parser pi -> (Q_pi, E_pi, Occ_pi, row(.), ForcedRows(Q_pi)) plus a row-syntax realizer A_{Q_pi} satisfying transcript preservation.
- target-preserving condition: A_{Q_pi} is produced without using the desired circuit lower bound, preserves uniform G_N lengths and full EF+SAT_U equality atoms, and yields a small spoof/patch circuit in the same nonuniform target model.
- row-syntax realizer: an assignment of formula strings and SAT_U truth values to off-Q_pi occurrences that is constant on every equality fiber of E_pi and agrees with the spoof truth table outside Q_pi.
- complete row: all SAT-query occurrences G_N(x,j), j<=M_N, contributing to the XOR value H_N^{SAT}(x).

## Assumptions

- Model: full EF+SAT_U allows extension variables and a SAT_U predicate over explicit formula syntax; unlike EF+SAT_U^{occ}, repeated formula DAG nodes must remain syntactically equal.
- Uniformity: G_N, the parser, and the patch construction are computable in poly(N); pi may be nonuniform only as the certificate being audited.
- Soundness regime: accepted transcripts assert a semantic lower bound C(H_N^{SAT})>N^{1+epsilon-o(1)} against the named Boolean circuit model.
- Quantitative regime: the spoof baseline size S_D is below N^{1+epsilon-o(1)}; the clean threshold |Q_pi|>=N^{epsilon-o(1)} uses S_D=N^{1+o(1)}.
- Barrier regime: if projection width and decision width are O(log N) and DirectClusterSound holds, the accepted shadow is a valid natural property, so this lemma is a no-go/escape audit rather than main-conjecture progress.

## Equations

- beta_zero_xor_carrier: `H_N^{\mathrm{SAT}}(x)=\bigoplus_{j\le M_N}\mathrm{SAT}(G_N(x,j)),\quad M_N\le N^{q+o(1)},\quad |G_N(x,j)|=L_N=(\log N)^d`. Valid when: Valid when H_N is the beta-zero XOR carrier with uniform G_N, bounded query count M_N, and logarithmic SAT-query length.
- sparse_patch_bound: `C(H_N^{\mathrm{SAT}})\le S_D+O(|Q_\pi|N)`. Valid when: Applies after the full EF+SAT_U transcript is preserved by a row-syntax realizer and D_N agrees with H_N outside Q_pi.
- row_charge_threshold: `|Q_\pi|\ge \Omega((N^{1+\epsilon-o(1)}-S_D)/N);\quad S_D=N^{1+o(1)}\Rightarrow |Q_\pi|\ge N^{\epsilon-o(1)}`. Valid when: Requires the claimed source lower bound, a below-threshold spoof circuit, and the sparse patch inequality in the same circuit model.

## Attempted Derivation

- Start from the proved EF+SAT_U^{occ} packet: parser pi -> Q_pi and private occurrence-label perturbations preserve accepted transcripts outside ForcedRows(Q_pi).
- Attempt the same perturbation in full EF+SAT_U by changing only one off-Q row of H_N^{SAT}.
- Observe the new obstruction: formula-DAG equality fibers E_pi may connect occurrences in different rows, so a one-row perturbation can violate equality or SAT_U consistency even when no queried local proof rule mentions the lower bound.
- Define row-syntax realizer A_Q as the missing transfer certificate: it must assign formula syntax and SAT_U values consistently on every equality fiber while realizing the spoof truth table outside Q.
- With A_Q, transcript preservation plus soundness says the spoofed easy object cannot be accepted; sparse patching gives C(H_N^{SAT})<=S_D+O(|Q|N), forcing |Q|>=Omega((N^{1+epsilon-o(1)}-S_D)/N).
- Without A_Q, shared-DAG equality over two unforced rows is a finite falsifier to lifting occurrence-local private-label invariance into full EF+SAT_U.

Blocking gap: No proof yet that every standard full EF+SAT_U transcript admitting a beta-zero XOR certificate has a row-syntax realizer with small Q, nor that every failure of realizability yields a large syntactic hitting number.

## Falsifiers

- Shared-DAG equality falsifier: two off-Q rows share one SAT_U formula node, so private perturbation of one row breaks full EF+SAT_U syntax although it was allowed in EF+SAT_U^{occ}.
- Odd-charge Tseitin falsifier: bounded local consistency can accept every projected view while no global satisfying assignment exists, so ordinary soundness is not DirectClusterSound.
- Sparse residual falsifier: if a spoof D_N agrees with H_N^{SAT} outside Q and |Q|<N^{epsilon-o(1)}, the patch circuit contradicts a claimed N^{1+epsilon-o(1)} source lower bound.
- Natural-shadow falsifier: if a low-width cluster also has DirectClusterSound, it yields a large constructive useful property and faces PRF/natural-proofs pressure rather than escaping barriers.
- Advice-leakage falsifier: if Q_pi is selected by hidden nonuniform advice not recoverable from pi, the patch and density calculations are not valid target-preserving transfers.

## Learning

Cycle 83 converts the full EF+SAT_U boundary into a precise combinatorial gate: shared formula-DAG equality creates equality fibers, and a full lift needs either a row-syntax realizer for the sparse spoof or a large equality-fiber row charge. This is valid route-level proof-boundary progress; it strengthens the occurrence-local no-go packet but is not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch is blocked at full EF+SAT_U row-syntax extraction; a concrete shared-syntax experiment tests whether the obstruction is a rare encoding artifact or the central transfer barrier.
- Situation seed: Build a padded SAT-query family G_N(x,j) in which many rows reuse a common formula template T_z through shared DAG nodes, then compare an EF+SAT_U^{occ} transcript with a full EF+SAT_U transcript enforcing equality of the shared nodes.
- Varied variable: gamma, the maximum number of distinct beta-zero XOR rows touched by one equality fiber of the full EF+SAT_U formula-DAG syntax.
- Held-fixed controls: H_N^{SAT} remains the beta-zero XOR carrier with M_N<=N^{q+o(1)} and L_N=(log N)^d., The claimed source threshold remains C(H_N^{SAT})>N^{1+epsilon-o(1)} in the same nonuniform Boolean circuit model., Projection and decision width remain O(log N) so any DirectClusterSound branch would be a valid natural-property object., No hidden advice is allowed in selecting Q_pi or constructing the spoof D_N.
- Expected observation: If gamma is large, equality fibers may themselves force many rows and produce a syntactic row-charge lower bound. If gamma is small but cross-row fibers remain uncharged, private occurrence perturbation is invalid and a separate row-syntax realizer is necessary.
- Transfer certificate needed: A formal row-syntax-realizability theorem or an equality-fiber hitting theorem: for every accepted full EF+SAT_U transcript, either produce A_Q with |Q| below the sparse-patch threshold or prove tau_syn(pi)>=N^{epsilon-o(1)}.

## Next Experiment

Compute tau_syn(pi) for the minimal full EF+SAT_U shared-template transcript with two, then N^alpha, cross-row equality fibers; test whether standard formula encodings make A_Q impossible or merely charge the touched rows.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Equality-free occurrence-local ForcedRows theorem: for Psys=EF+SAT_U^{occ,eqfree}, a valid low-cover row-parity certificate for the beta-zero XOR carrier either forces at least N^{epsilon-o(1)} complete rows, or gives an unrestricted circuit upper bound C(H_N^SAT)<=N^{max{rho,q+alpha_ad,max(f,r)+1}+o(1)}; hence it is a finite falsifier for any claimed N^{1+epsilon-o(1)} source lower bound when all three exponents are subthreshold.

## Definitions

- source object: an accepted EF+SAT_U^{occ,eqfree} transcript pi for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), where M_N<=N^{q+o(1)} and G_N has circuit overhead N^{rho+o(1)}.
- target object: a scoped no-go theorem for proof-mediated beta-zero XOR certificates, not a proof of P != NP.
- controlled interface: the parser pi -> Q_pi, the local SAT-label space LocSat(Q_pi), the syntactic set ForcedRows(Q_pi), an adaptive-cover circuit for labels, and a sparse patch for exceptional rows.
- target-preserving condition: the circuit upper bound computes the same truth table H_N^SAT at length N by advice-free uniform construction of G_N and by hardwiring only the fixed transcript pi, never a nonuniform hard-row selector.
- complete row: an input x is complete for pi if all M_N occurrence labels SAT(G_N(x,j)) relevant to the beta-zero row parity have names in the occurrence universe of Q_pi or are default-free variables in LocSat(Q_pi).
- LocSat(Q_pi): the set of assignments to occurrence labels satisfying every formula-internal SAT-consistency constraint and every equality-free local constraint explicitly touched by pi.
- ForcedRows(Q_pi): rows x for which xor_{j<=M_N} y_{x,j} is constant over LocSat(Q_pi), with untouched labels treated as free private occurrence variables.
- residual rows: an externally declared set R_N on which the low-cover certificate is allowed not to match H_N^SAT and which must be patched explicitly.

## Assumptions

- Model: unrestricted Boolean circuit size is the lower-bound target; the proof system restriction is occurrence-local and equality-free, so no rule identifies two generated SAT formulas by global syntax.
- Uniformity: G_N and the parser for pi are uniform in N; hardwiring pi is allowed only for a route-level negative upper bound against that fixed certificate family.
- Cover regime: the label predictor induced by pi has adaptive-cover exponent alpha_ad=max{tau,max_l(a_l+mu_l),max_l omega_l}.
- Query regime: M_N<=N^{q+o(1)} and every queried formula has length polylog(N), so SAT-label evaluation cost is charged through the cover, not through an oracle.
- Soundness regime: valid row-parity binding means every accepted local transcript certifying a row must have the same row parity on all assignments in LocSat(Q_pi).
- Residual regime: |R_N|<=N^{r+o(1)} and |ForcedRows(Q_pi)|<=N^{f+o(1)} when the upper-bound alternative is invoked.
- Threshold regime: the intended contradiction is only to a claimed source lower bound C(H_N^SAT)>N^{1+epsilon-o(1)} with rho<1+epsilon, q+alpha_ad<1+epsilon, r<epsilon, and f<epsilon.

## Equations

- beta0_carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\qquad M_N\le N^{q+o(1)}.`. Valid when: Valid when the beta-zero XOR carrier uses M_N SAT queries generated uniformly from x and j.
- syntactic_forced_rows: `ForcedRows(Q_\pi)=\{x:\bigoplus_{j\le M_N} y_{x,j}\text{ is constant on }LocSat(Q_\pi)\}.`. Valid when: Valid when occurrence labels are private variables except for constraints explicitly parsed into Q_pi.
- low_cover_predictor_size: `C(D_N)\le N^{\max\{\rho,q+\alpha_{ad}\}+o(1)}.`. Valid when: Valid when G_N has overhead rho and the transcript labels have adaptive-cover exponent alpha_ad.
- patch_upper_bound: `C(H_N^{SAT})\le C(D_N)+O((|ForcedRows(Q_\pi)|+|R_N|)N).`. Valid when: Valid when D_N agrees with H_N^SAT outside forced and residual rows.
- subthreshold_contradiction_gate: `\max\{\rho,q+\alpha_{ad},\max(f,r)+1\}<1+\epsilon\Rightarrow C(H_N^{SAT})<N^{1+\epsilon-o(1)}.`. Valid when: Valid when f and r are row-count exponents below epsilon and all cover overheads are subthreshold.

## Attempted Derivation

- Fix N, M_N<=N^{q+o(1)}, generator overhead rho, transcript pi, residual set R_N, and adaptive-cover exponent alpha_ad.
- Run Scan(pi) to form Q_pi and LocSat(Q_pi); this is syntactic and does not query H_N^SAT.
- Define ForcedRows(Q_pi) by constancy of row parity over LocSat(Q_pi), with untouched occurrence labels free.
- For any nonforced row x, choose A,A' in LocSat(Q_pi) with different row parity; equality-free occurrence locality ensures pi accepts both because all checked constraints are in Q_pi.
- Therefore a valid row-parity-binding certificate cannot claim x unless x is in ForcedRows(Q_pi) or x is declared residual.
- Use the adaptive cover to build D_N: on unforced nonresidual rows, compute the certificate's predicted labels for all j<=M_N and XOR them; the size is N^{max{rho,q+alpha_ad}+o(1)}.
- Patch all forced and residual rows by equality-to-x indicators and hardwired correct output bits; this costs O((|ForcedRows|+|R_N|)N).
- Conclude C(H_N^SAT)<=N^{max{rho,q+alpha_ad,max(f,r)+1}+o(1)}.
- If a source claim asserts C(H_N^SAT)>N^{1+epsilon-o(1)} and rho,q+alpha_ad<1+epsilon while f,r<epsilon, the certificate route is refuted; otherwise the theorem only records the needed forced-row mass or overhead escape.

Blocking gap: The derivation is complete only for equality-free occurrence-local transcripts. Full EF+SAT_U can use formula-identity or extension-variable equality to tie private occurrence labels together; promotion needs an equality-graph parser proving that such ties either raise alpha_ad, create forced complete rows, or are outside the scoped theorem.

## Falsifiers

- falsifier: a transcript with alpha_ad<theta but an unparsed equality graph that makes row labels nonprivate invalidates the equality-free invariance claim for full EF+SAT_U.
- falsifier: if the low-cover predictor uses advice to select a hard row or a nonuniform certificate family, the target-preserving condition fails.
- falsifier: if |ForcedRows(Q_pi)|=N^{epsilon-o(1)} or larger, the sparse-patch contradiction no longer beats an N^{1+epsilon-o(1)} lower-bound claim.
- falsifier: if residual rows have exponent r>=epsilon, sparse residual compression cannot refute the claimed beta-zero lower bound.
- falsifier: if q+alpha_ad>=1+epsilon, the adaptive-cover label computation already sits above the intended threshold.
- falsifier: local soundness without row-parity binding permits private-row spoof assignments and is not a valid certificate of H_N^SAT.

## Learning

Cycle 83 partially discharges the top ForcedRows proof packet: the equality-free occurrence-local theorem is theorem-shaped and valid as a route-specific falsifier. The remaining full-EF boundary is no longer vague; it is the equality-graph extraction problem for real formula identity and extension-variable congruence.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The branch needs a concrete target-preserving thought experiment because the live gap is not abstract natural-proofs folklore but whether private occurrence labels remain independent after adding formula-identity structure to EF+SAT_U certificates.
- Situation seed: Take a padded beta-zero SAT-query family where two rows x and x' contain a controlled fraction of syntactically identical generated formulas G_N(x,j)=G_N(x',j'), and feed it to an EF+SAT_U^{occ} certificate parser that either ignores or records identity edges.
- Varied variable: identity-edge density lambda, the exponent of occurrence pairs tied by real formula syntax but not by local row constraints.
- Held-fixed controls: Keep M_N<=N^{q+o(1)}, generator overhead rho, residual exponent r, and lower-bound target N^{1+epsilon-o(1)} fixed., Keep the adaptive-cover budget alpha_ad fixed and advice-free., Keep row-parity binding as the required certificate semantics., Keep the circuit target unrestricted and same-length for H_N^SAT.
- Expected observation: At lambda=0, nonforced rows admit private-label spoofing, so valid certificates must force rows or trigger the patch upper bound. As lambda grows, spoofing fails only along parsed identity components; if those components have low cover, they should be charged into alpha_ad, while high-cover components become the exact full-EF escape.
- Transfer certificate needed: A formal equality-graph transfer lemma: parsing identity edges either preserves private-label invariance on quotient rows, increases the adaptive-cover exponent used in C(D_N), or syntactically forces complete rows; without this certificate, intuition about full EF+SAT_U may not enter proof obligations.

## Next Experiment

Instantiate the equality-graph parser on a minimal full EF+SAT_U transcript with two identical generated SAT formulas in different rows; compute whether quotienting preserves private-label invariance, increases alpha_ad, or forces complete rows.
