# cycle-0074

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: beta-zero XOR row-residual audit

## Candidate Lemma

Beta-zero XOR transfer plus sparse-row residual falsifier: an i.o. lower bound C(H_N^SAT)>N^{1+epsilon} target-preservingly implies SAT notin P/poly when max{rho,q}<1+epsilon; independently, any subthreshold approximator wrong on a sparse set of source rows refutes that source lower bound.

## Definitions

- source object: H_N^SAT:{0,1}^N->{0,1} is the XOR over M_N generated SAT instances G_N(x,j) of length L_N.
- target object: nonuniform SAT circuits at input length n; the target consequence is SAT notin P/poly, hence NP not subset P/poly.
- controlled interface: beta-zero compact substitution with L_N=(log N)^d=N^{o(1)}, M_N<=N^{q+o(1)}, and batched generator size N^{rho+o(1)}.
- target-preserving condition: q<1+epsilon, rho<1+epsilon, no nonuniform advice is hidden in G_N, and source and target use the same Boolean circuit model.
- row residual: R_N subset {0,1}^N is a hardwired set of exceptional source rows where an approximator D_N may disagree with H_N^SAT.
- circuit measure: C(F) denotes nonuniform fan-in two Boolean circuit size for the length-N truth table family.

## Assumptions

- The batched generator outputs or streams all M_N queries with total circuit size N^{rho+o(1)}, not M_N independent copies of cost N^rho.
- For every fixed c, SAT in P/poly supplies length-L_N circuits of size L_N^c for all sufficiently large valid N.
- The source lower bound C(H_N^SAT)>N^{1+epsilon} is claimed on infinitely many valid N in the same nonuniform model.
- Equality to one hardwired N-bit row costs O(N) gates, so E exceptional rows cost O(EN) gates to patch.

## Equations

- carrier_definition: `H_N^{SAT}(x)=\bigoplus_{j=1}^{M_N} SAT(G_N(x,j)),\quad M_N\le N^{q+o(1)},\quad L_N=(\log N)^d.`. Valid when: Valid when each G_N(x,j) is a well-formed length-L_N SAT instance and XOR is implemented by ordinary Boolean circuits.
- beta_zero_substitution: `SAT\in SIZE(n^c)\ \Longrightarrow\ C(H_N^{SAT})\le N^{\rho+o(1)}+M_N L_N^c+O(M_N)=N^{\max\{\rho,q\}+o(1)}.`. Valid when: Applies after assuming a length-n SAT circuit of size n^c and substituting it uniformly into every generated query slot.
- target_preserving_implication: `C(H_N^{SAT})>N^{1+\epsilon}\ \text{i.o.}\ \wedge\ \max\{\rho,q\}<1+\epsilon\ \Longrightarrow\ SAT\notin P/poly.`. Valid when: Applies when the source lower bound occurs on infinitely many valid source lengths and the substitution upper bound would hold on every such length.
- row_patching_bound: `D_N=H_N^{SAT}\ \text{on}\ \{0,1\}^N\setminus R_N\ \Longrightarrow\ C(H_N^{SAT})\le C(D_N)+O(|R_N|N).`. Valid when: Valid when R_N is explicitly hardwired and equality to an N-bit source row costs O(N) gates in the same circuit model.
- residual_falsifier_threshold: `C(D_N)+O(|R_N|N)<N^{1+\epsilon}\ \Longrightarrow\ (D_N,R_N)\ \text{falsifies}\ C(H_N^{SAT})>N^{1+\epsilon}.`. Valid when: Requires C(D_N) and |R_N|N to be measured at the same source length and against the same exponent threshold.

## Attempted Derivation

- Fix a batched generator G_N with M_N<=N^{q+o(1)}, L_N=(log N)^d, and circuit size N^{rho+o(1)}; define H_N^SAT by XOR aggregation.
- Assume SAT has circuits of size n^c. Substitute the length-L_N SAT circuit into every generated query and obtain C(H_N^SAT)<=N^{max{rho,q}+o(1)} because L_N^c=N^{o(1)}.
- If max{rho,q}<1+epsilon, any i.o. lower bound C(H_N^SAT)>N^{1+epsilon} contradicts SAT in P/poly; this is a valid route-level bridge, not a proof of the source lower bound.
- Let D_N agree with H_N^SAT outside R_N. Hardwire equality tests for all rows in R_N where D_N is wrong, XOR the correction, and get C(H_N^SAT)<=C(D_N)+O(|R_N|N).
- Instantiate Psys as EF+SAT_U. If its accepted certificates are functional over arbitrary label tables and dense at 2^{-O(L_N)}, the certificate property naturalizes. If soundness is only for the real SAT label table, the route escapes that barrier but must prove row-residual robustness.
- Tried to derive a sparse D_N,R_N from an arbitrary nonfunctional EF+SAT_U proof by collecting rows whose SAT-semantic axioms are used essentially.

Blocking gap: No proof-analysis theorem currently forces a semantic EF+SAT_U certificate either to functionalize over all label tables or to localize its nonfunctionality to fewer than N^{epsilon-o(1)} source rows. EF may use global SAT structure shared by many rows through the same formula labels.

## Falsifiers

- falsifier: a circuit D_N of size N^{1+epsilon-gamma} agreeing with H_N^SAT except on at most N^{epsilon-gamma} source rows.
- falsifier: any positive-beta black-box interface claiming all-exponent SAT lower bounds from a fixed N^{1+epsilon} source lower bound.
- falsifier: hidden advice in G_N or in the certificate search procedure that makes the source lower bound target-equivalent.
- falsifier: a dense functional EF+SAT_U certificate family, which is valid as a natural property but invalid as a claimed natural-proofs escape.
- falsifier: a batched-generator accounting failure where producing all queries costs M_N N^{rho} rather than N^{rho}+N^{q+o(1)}.

## Learning

Cycle 74 upgrades the focus packet: the beta-zero XOR bridge and row-residual patching bound are theorem-shaped and valid under explicit batched-generator assumptions. The live obstruction is now narrower: prove an EF+SAT_U semantic extraction/no-extraction theorem, or quarantine proof-mediated certificates that cannot certify residual robustness.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch has an exact bridge but lacks a proof-analysis extraction theorem. A concrete row-deletion experiment tests whether semantic proof objects can leak through sparse exceptional rows before more abstract naturalness discussion is useful.
- Situation seed: Set q=1+epsilon/2, rho=1, d=2, M_N=N^q, L_N=(log N)^2, and let an advice-free generator G_N map rows x to a high-entropy list of length-L_N SAT formulas. Imagine an EF+SAT_U certificate that proves a lower bound for H_N^SAT after deleting E_N suspicious source rows and supplies a small circuit D_N for the undeleted residual.
- Varied variable: theta in E_N=N^theta, the exponent of deleted or semantically exceptional source rows.
- Held-fixed controls: beta=0 with L_N=N^{o(1)} and q,rho<1+epsilon., The target consequence remains SAT notin P/poly via substitution, not a restatement of P vs NP., Circuit model is nonuniform fan-in two Boolean circuits for both D_N and H_N^SAT., G_N is advice-free and batched with total size N^{rho+o(1)}.
- Expected observation: For theta<epsilon, any D_N of size below N^{1+epsilon-o(1)} becomes an exact subthreshold circuit after equality patching, so the certificate route is falsified. For theta>=epsilon, row deletion alone no longer collapses the threshold, so the certificate must prove a genuine residual lower bound rather than rely on sparse leakage.
- Transfer certificate needed: A formal extraction or no-extraction theorem for EF+SAT_U showing whether semantic nonfunctionality yields a pair (D_N,R_N) with |R_N|=N^{theta+o(1)}, or else proving that the proof system is nonrelativizing in a way not captured by row residuals.

## Next Experiment

Formalize EF+SAT_U syntax with label table U_N, prove the functional dense naturalization lemma cleanly, then attempt a finite extraction theorem: every nonfunctional accepted proof either identifies a row set R_N and approximator D_N or uses a nonrelativizing SAT principle outside the row-residual audit.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Log-projection DirectClusterSound naturalizes a proof-mediated beta-zero XOR lower-bound certificate.

## Definitions

- source object: A beta-zero XOR carrier H_N^SAT with truth table T_N in {0,1}^N, together with a row-local certificate model Psys whose verifier row r reads target bits Q_r subseteq [N], proof bits P_r, and accepts predicate A_r(y_{Q_r},pi_{P_r}).
- target object: The target class is SIZE_m(s) on m=log N input bits, usually s=m^k or the exponent window required by the beta-zero XOR transfer, represented by truth tables TT(D) in {0,1}^N.
- controlled interface: A cluster C of verifier rows has target projection U_C=union_{r in C} Q_r and projection-decision width w_C; Acc_C(y)=1 iff some proof assignment satisfies all A_r on y_{U_C}; DirectClusterSound(C,s) means Acc_C(TT(D))=0 for every D in SIZE_m(s).
- target-preserving condition: The same explicit cluster C must be accepted by T_N, reject exactly the named SIZE_m(s) target without advice-dependent row selection, and be decidable from y with |U_C|+w_C=O(log N).
- carrier observable: P_C={y in {0,1}^N: Acc_C(y)=1}; this is a route-level natural-property audit, not a P != NP claim.

## Assumptions

- Cluster C_N is computable from 1^N in poly(N) time and its row set is not chosen using the candidate circuit D.
- Completeness holds: Acc_{C_N}(T_N)=1 via a proof assignment compatible on all queried proof bits in C_N.
- DirectClusterSound(C_N,s) holds in the same nonuniform target model SIZE_m(s), not merely as ordinary global soundness of Psys.
- The existential proof-bit CSP induced by C_N has an explicit decomposition deciding Acc_C(y) in poly(N)2^{O(w_C)} time.

## Equations

- projection_size: `h_C:=|U_C|,\quad U_C=\bigcup_{r\in C}Q_r`. Valid when: Valid when verifier rows and their target-query sets are explicitly named for the chosen cluster.
- largeness: `\Pr_{Y\leftarrow\{0,1\}^N}[P_C(Y)=1]\ge 2^{-h_C}\ge N^{-a}\quad\text{if }h_C\le a\log_2 N`. Valid when: Applies when completeness supplies one fixed accepting proof-view assignment and rows inspect no target bits outside U_C.
- constructivity: `\mathrm{Time}(P_C)\le N^{O(1)}2^{O(w_C)}`. Valid when: Requires an explicit projection-decision decomposition and bounded-arity row predicates over target and proof variables.
- usefulness: `P_C\cap\{TT(D):D\in SIZE_m(s)\}=\varnothing`. Valid when: Requires DirectClusterSound(C,s) in the same circuit-size model used for the target lower bound.
- prf_pressure: `\mathrm{Adv}_{P_C}(G)\ge \Pr[P_C(Y)=1]\ge 2^{-h_C}`. Valid when: Valid when every keyed function G_k lies in SIZE_m(s) and P_C is poly(N)-constructive on full truth tables.

## Attempted Derivation

- Fix Psys as a row-local existential certificate model for LB(y,s), where rows query target bits and proof bits.
- For a cluster C, define Acc_C(y) by existential satisfaction of the row predicates and define P_C={y:Acc_C(y)=1}.
- Completeness for T_N gives one accepting proof-view assignment; every y agreeing with T_N on U_C is accepted, so density is at least 2^{-|U_C|}.
- If the proof-view CSP has projection-decision width w_C=O(log N), dynamic programming decides P_C in poly(N) time.
- If DirectClusterSound(C,s) holds, P_C rejects every SIZE_m(s) truth table, hence is useful against the exact target class.
- Thus any log-projection direct cluster becomes a valid large constructive useful property and faces PRF/natural-proofs pressure.
- Attempting to replace DirectClusterSound by ordinary soundness fails: odd-charge Tseitin has global unsatisfiability but every proper cluster is satisfiable, so Acc_C(y)=1 for all y.
- For beta-zero XOR, any certificate that leaves only a sparse residual R_N can be patched, giving C(H_N^SAT)<=S_D+O(|R_N|N) and falsifying a subthreshold source lower bound.

Blocking gap: No named beta-zero XOR certificate system is known to provide DirectClusterSound(C,s) with |U_C|+w_C=O(log N) while also avoiding naturalization or sparse residual leakage.

## Falsifiers

- Odd-charge Tseitin is a finite falsifier for ordinary soundness or local consistency as a substitute for DirectClusterSound.
- A sparse-row residual R_N with S_D+O(|R_N|N)<N^{theta} is a falsifier for the claimed beta-zero XOR source lower bound at threshold N^{theta}.
- A log-projection cluster with DirectClusterSound is a valid natural property; cryptographic PRF tension falsifies any claim that proof mediation alone escapes natural proofs.
- Advice-dependent row selection is a falsifier for target preservation because the selected cluster can encode the small circuit being rejected.
- A high-width proof-view CSP is a falsifier for the constructivity part of the naturalization bridge, not for DirectClusterSound itself.

## Learning

Cycle 74 upgrades the DirectClusterSound gap into a theorem-shaped audit: if a proof-mediated beta-zero XOR certificate has logarithmic target projection and logarithmic projection-decision width, then it is a valid large constructive useful property. Odd-charge Tseitin proves ordinary soundness cannot supply the missing direct condition, and sparse residuals give a quantitative patching falsifier for subthreshold source lower bounds.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for DirectClusterSound and row-residual leakage.`
- Rationale: The branch has already isolated the abstract missing premise; the next useful move is to test whether a concrete local proof carrier collapses to Tseitin-style satisfiable clusters or to patchable sparse residuals.
- Situation seed: Embed an odd-charge Tseitin system on a connected graph G into a row-local Psys for beta-zero XOR certificates, with dummy or fixed H_N^SAT target queries and proof variables as edge labels.
- Varied variable: The target projection size h=|U_C|, varied from 0 to a log N while keeping the proof-view cluster C proper.
- Held-fixed controls: Target class remains SIZE_m(m^k) with m=log N., The beta-zero XOR parameters M_N<=N^{q+o(1)}, L_N=(log N)^d, and overhead N^{rho+o(1)} remain unchanged., Row predicates remain bounded-arity F_2 parity constraints plus dummy SAT-projection gates., Cluster selection is explicit and advice-free.
- Expected observation: For every proper Tseitin cluster, Acc_C(y)=1 for all target tables y, so local consistency gives density but zero usefulness; adding h=O(log N) target pins creates largeness N^{-O(1)} but still no circuit-sensitive rejection unless DirectClusterSound is separately proved.
- Transfer certificate needed: A formal theorem that the named Psys enforces DirectClusterSound against every SIZE_m(m^k) circuit at logarithmic projection width, or a no-go proof that any such enforcement naturalizes or requires nonlogarithmic/nonconstructive structure.

## Next Experiment

Instantiate Psys as a local PCP-style certificate for LB(y,m^k); compute h_C,w_C for its smallest accepting row cluster on T_N, then embed the odd-charge Tseitin proof-view gadget and test whether any direct circuit-sensitive row predicate survives without creating a natural property.

# Cycle 74: DirectClusterSound adaptive-cover falsifier for MCSP/MKtP carriers

## Candidate Lemma

Adaptive-cover no-side falsifier: any generated MCSP/MKtP certificate carrier whose accepted row has adaptive cover exponent alpha_ad<theta cannot be a valid no-side source for threshold 2^{theta m}; the cover itself gives an unrestricted circuit for the row.

## Definitions

- source object: generated MCSP/MKtP no-side certificate family V_m(pi)->T_{m,pi} for truth tables on m input bits, claiming C(T_{m,pi})>2^{theta m}.
- target object: advice-free E-uniform hard-row carrier yielding an E language with circuit lower bound 2^{delta n} after kappa-gap and distinct-image loss D.
- controlled interface: adaptive proof-opening cover with top transcript exponent tau, level counts a_l, summary exponents mu_l, and opener exponents omega_l.
- target-preserving condition: the selected hard row and its certificate are generated or searchable without advice within 2^{O(m)} time and preserve theta, kappa, and D under multiplexing.
- DirectClusterSound(C,k) is modeled as a local cluster certificate whose row bits are opened through summaries, consistency transcripts, and semantic label openers.
- C(T) denotes unrestricted nonuniform Boolean circuit size of the truth-table row T, the same size notion used by MCSP no-side soundness.

## Assumptions

- Circuit model is unrestricted fan-in two Boolean circuits with nonuniform hardwiring allowed for a fixed accepted row.
- The adaptive cover opens every queried truth-table bit of T_{m,pi}, not merely sampled verifier locations.
- The verifier may be non-natural or proof-mediated, but its accepted row must be an actual MCSP no-side witness at threshold 2^{theta m}.
- The cover parameters are uniform enough to be named, but the upper-bound circuit may hardwire the summaries; hence advice-freeness does not save a subthreshold cover.
- The comparison alpha_ad<theta is interpreted with an o(1) slack margin, e.g. alpha_ad<=theta-eta for some eta>0.

## Equations

- adaptive_cover_exponent: `\alpha_{ad}=\max\{\tau,\max_\ell(a_\ell+\mu_\ell),\max_\ell \omega_\ell\}`. Valid when: Valid when the certificate opening protocol is decomposed into transcript, summary-volume, and opener-circuit exponent ledgers.
- row_upper_bound_from_cover: `C(T_{m,\pi})\le 2^{\alpha_{ad}m+o(m)}`. Valid when: Valid when the adaptive cover opens all row bits and unrestricted circuits may hardwire row-specific summaries.
- no_side_contradiction: `\alpha_{ad}<\theta\ \Longrightarrow\ T_{m,\pi}\notin \mathrm{MCSPNo}_{m,2^{\theta m}}`. Valid when: Valid when MCSP no-side soundness requires every accepted row to exceed the same unrestricted circuit threshold.

## Attempted Derivation

- Instantiate DirectClusterSound(C,k) as a certificate pi that induces a SAT-label row T_{m,pi} and proves local cluster consistency for the beta-zero XOR query matrix.
- Abstract its openings into an adaptive cover: top transcript budget 2^{tau m}, level-l summary family size 2^{a_l m}, summary length 2^{mu_l m}, and opener circuit size 2^{omega_l m}.
- For a fixed accepted pi, build a nonuniform circuit for T_{m,pi} by hardwiring all transcript tables and summaries and wiring the opener circuits; size is at most 2^{alpha_ad m+o(m)}.
- Compare this upper bound with the claimed MCSP/MKtP no-side threshold 2^{theta m}; alpha_ad<theta contradicts accepted-row hardness.
- Feed the same audit into the beta-zero XOR packet: functional label certificates with low adaptive cover either yield subthreshold row circuits or a sparse residual approximant, so they cannot support a valid source lower bound.

Blocking gap: We have not proved that every named DirectClusterSound or Psys certificate necessarily has low alpha_ad; the result is a theorem-shaped falsifier for implementations that expose rankable summaries, not a universal impossibility theorem.

## Falsifiers

- falsifier: an accepted MCSP/MKtP certificate whose Merkle, checkpoint, or cluster openings give alpha_ad<theta immediately yields a small unrestricted circuit for the row.
- falsifier: a hard-row selector that chooses pi or a row index using nonuniform advice fails to define an E-uniform target language.
- falsifier: DirectClusterSound acceptance based only on local consistency and ordinary soundness may functionalize SAT labels into a sparse residual D_N plus R_N, collapsing the claimed N^{1+epsilon} lower bound.
- falsifier: beta-zero XOR parameters with a<=max{rho,q} cannot transfer a source lower bound to SAT circuit lower bounds by substitution.
- falsifier: low-complexity sparse or parity rows accepted by the certificate model show that the certificate is not circuit-sensitive enough for MCSP no-side soundness.

## Learning

Cycle 74 instantiates the adaptive-cover obstruction on a concrete DirectClusterSound-style carrier. The contribution-making move is a finite falsifier: low-cover MCSP/MKtP certificates do not merely look weak; they give explicit unrestricted row circuits below the claimed threshold. The positive source theorem is still open and essentially requires high adaptive cover dimension plus advice-free hard-row generation.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The branch needs a concrete carrier audit, not another abstract barrier citation; DirectClusterSound with block summaries is the smallest target-preserving model that exposes alpha_ad and residual leakage.
- Situation seed: Take H_N^SAT(x)=xor_{j<=N^{q+o(1)}}SAT(G_N(x,j)) with L_N=(log N)^d and attach DirectClusterSound certificates that group the SAT-query labels into blocks of 2^{lambda m} positions, with Merkle-style consistency summaries and polynomial-time local openers.
- Varied variable: lambda, the block-length exponent controlling the number of summaries and hence alpha_cluster=max{tau,1-lambda+mu,omega}.
- Held-fixed controls: beta=0 polylogarithmic SAT query length L_N=(log N)^d, generator overhead N^{rho+o(1)} and query count N^{q+o(1)}, unrestricted circuit size as the MCSP row-hardness measure, no advice in row selection or certificate search, claimed no-side threshold 2^{theta m} and beta-zero lower-bound target N^{1+epsilon}
- Expected observation: With polynomial summaries and openers, alpha_cluster=1-lambda+o(1). If lambda>1-theta, every accepted row is subthreshold-easy, so the certificate is invalid; if lambda<=1-theta, the carrier avoids this falsifier but pays large summary volume and still must prove genuine row hardness without advice.
- Transfer certificate needed: A formal mapping from DirectClusterSound rows to the H_N^SAT label matrix, an E-search procedure for accepted certificates, and a proof that no sparse residual D_N,R_N or advice-selected row is being smuggled into the transfer.

## Next Experiment

Formalize DirectClusterSound(C,k) with block exponent lambda, compute tau, mu, omega for its actual openings, and decide whether it falls into alpha_ad<theta, sparse residual collapse, advice leakage, or genuine high-cover escape.
