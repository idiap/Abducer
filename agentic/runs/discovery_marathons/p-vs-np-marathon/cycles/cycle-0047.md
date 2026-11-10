# cycle-0047

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: locality-extraction obstruction

## Candidate Lemma

Relativizing separator-promotion is false. For any 0<sigma<theta<1+epsilon and fixed d>1, there is an oracle label language U and a generated-OR family with q=0, rho=theta+o(1), L=(log N)^d such that H_N^U has O(1)-size circuits, while every zero-error one-sided local separator for the generated positive and negative bags has size greater than N^sigma with high probability over the codebook. Thus separator hardness is not a valid source lower bound unless a nonrelativizing locality-extraction theorem is supplied.

## Definitions

- source object: generated-OR carrier H_N^U on N input bits with M=N^q oracle/SAT-label queries of length L=(log N)^d produced by nonuniform generator G_N of size N^rho.
- target object: SAT on length L inputs, or its relativized label analogue U, with the target consequence obtained only through the separate substitution bridge.
- controlled interface: arbitrary circuit upper bounds for H_N versus one-sided local separators p on individual generated formulas.
- target-preserving condition: q,rho<1+epsilon and no nonuniform advice may leak a solution for the local SAT-label problem except through the named separator or substitution circuit.
- One-sided separator means p(a_y)=1 for every generated positive codeword and p(b_y)=0 for every generated negative codeword.
- The codebook has R=N^theta random pairs (a_y,b_y) in {0,1}^L, with U(a_y)=1 and U(b_y)=0.

## Assumptions

- The generator input has a control bit c and an address y; G_N(c,y) outputs a_y when c=1 and b_y when c=0.
- The codebook is stored nonuniformly in G_N, so |G_N|=O(RL).
- The separator circuit receives only the length-L formula/codeword, not the control bit c or address y.
- The oracle labels on the chosen codewords are independent; this is a relativizing falsifier, not a real-SAT lower bound.

## Equations

- generator-size-threshold: `R=N^{\theta},\quad |G_N|=O(RL)=N^{\theta+o(1)}<N^{1+\epsilon}`. Valid when: Valid when d is fixed, theta is below 1+epsilon, and the codebook table is allowed as nonuniform generator advice.
- planted-control-easy-carrier: `H_N^U(c,y,w)=U(G_N(c,y,w))=c,\quad C(H_N^U)=O(1)`. Valid when: Valid when the oracle labels assign one to every positive codeword and zero to every negative codeword.
- separator-counting-bound: `\Pr[\exists p: |p|\le S,\ p(a_y)=1,\ p(b_y)=0\ \forall y\le R]\le 2^{O(S\log S)-2R}`. Valid when: Valid when the oracle codewords are sampled independently and S log S=o(R).
- separator-hardness-window: `S=N^{\sigma},\quad \sigma<\theta\ \Longrightarrow\ \operatorname{Sep}^{1s}_N(0)>N^{\sigma}`. Valid when: Valid when 2^L is much larger than R and the union bound over size-S circuits succeeds.

## Attempted Derivation

- Assume a circuit C of size T computes H_N(x)=OR_j SAT(G_{N,j}(x)).
- For each positive input x, choose a satisfiable generated query F_{x,j}; try to define a local predicate p(F) that accepts one such F and rejects all formulas from negative bags.
- The naive definition p(F)=1 iff there exists x,j with G_{N,j}(x)=F and C(x)=1 is not one-sided, because C may be using nonlocal control information rather than any property of F.
- Adding the condition that F never appears in a negative bag requires hard semantic range membership and may cost as much as the original H_N circuit.
- The planted-control oracle realizes this failure sharply: C reads the control bit c, while a local separator must solve an independent random classification problem on the codewords.

Blocking gap: There is no valid black-box operation that extracts a formula-local one-sided separator from an arbitrary global circuit for H_N. The missing step must exploit nonrelativizing real-SAT structure or be replaced by a direct arbitrary-circuit lower bound for H_N.

## Falsifiers

- falsifier: planted-control oracle with theta in (sigma,1+epsilon) makes H_N easy while zero-error local separators require size greater than N^sigma.
- falsifier: any relativizing separator-promotion theorem would prove a false implication in the oracle codebook model.
- falsifier: nonuniform generator advice can encode hard local classification while the global carrier depends only on a cheap control bit.
- falsifier: if max{rho,q}>=1+epsilon, even the valid target substitution bridge loses its contradiction threshold.

## Learning

Cycle 47 converts the locality-extraction warning into a formal relativizing obstruction. A planted-control oracle gives hard one-sided local separators but an O(1)-size generated-OR carrier, so separator hardness is not a valid source lower-bound certificate by itself. The target substitution bridge survives unchanged; the route must now prove a nonrelativizing extraction theorem for real SAT or attack C(H_N) directly.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for separator-to-source promotion.`
- Rationale: The branch already has a valid target bridge; the unresolved issue is whether one-sided separator lower bounds can certify an arbitrary-circuit lower bound for H_N. A concrete oracle carrier tests exactly that transfer, rather than restating hardness magnification.
- Situation seed: Oracle-coded pair carrier: choose R=N^theta random length-L codeword pairs (a_y,b_y), set U(a_y)=1 and U(b_y)=0, and let G_N(c,y) output a_y for c=1 and b_y for c=0, so H_N^U(c,y)=c.
- Varied variable: theta, the codebook-size and generator-advice exponent, varied between the desired separator exponent sigma and the target threshold 1+epsilon.
- Held-fixed controls: L=(log N)^d with fixed d>1, so the codeword universe is much larger than N^theta., q=0 and rho=theta+o(1), keeping the substitution-threshold condition rho,q<1+epsilon., Separators see only individual length-L codewords, not the control bit or address., The relativized target bridge is held fixed; only the separator-promotion step is being tested.
- Expected observation: For theta>sigma, counting gives Sep_N^{1s}(0)>N^sigma with high probability, while H_N^U has O(1)-size circuits. Separator hardness therefore does not transfer to source lower bounds by any relativizing argument.
- Transfer certificate needed: A nonrelativizing locality-extraction theorem for real SAT, explaining which SAT witness or proof structure invalidates the planted-control oracle and yielding explicit overhead below N^{1+epsilon}.

## Next Experiment

Try a real-SAT extraction using self-reducibility or witness isolation: from a small circuit for H_N, define a local predicate that accepts formulas whose forced witness path changes the global OR value, compute the overhead, and test it against the planted-control oracle falsifier.

# Barrier-Aware Lower-Bound Route: modular polynomial degree target gate

## Candidate Lemma

For fixed prime p and size exponent k, an F_p probabilistic-degree lower bound deg^{prob}_{p,1/3}(SAT_m) >= m^alpha transfers only to AC0[p] circuits of size m^k and depth beta log m/log log m with beta<alpha-o(1). It is not a valid transfer to unrestricted SIZE(m^k) without a depth-reduction certificate below this threshold.

## Definitions

- source object: the F_p probabilistic polynomial degree deg^{prob}_{p,epsilon}(f_m) of the m-bit Boolean slice, with f_m usually SAT_m.
- target object: nonuniform or DLOGTIME-uniform AC0[p] circuits with unbounded fan-in AND, OR, NOT, MOD_p gates, depth d, and size s=m^k; unrestricted SIZE(m^k) is a different target.
- controlled interface: the Razborov-Smolensky simulation maps every AC0[p]_{d,s} circuit to an epsilon-error F_p probabilistic polynomial of degree D_p(s,d,epsilon).
- target-preserving condition: a P-vs-NP transfer would require converting every SIZE(m^k) circuit for SAT_m into AC0[p] depth d and size poly(m) while keeping D_p(poly(m),d,1/3)<deg^{prob}_{p,1/3}(SAT_m), with no padding or advice leakage.

## Assumptions

- p is fixed before m grows; constants may depend on p and the gate basis.
- The SAT encoding is the same m-bit slice before and after the transfer.
- The probabilistic polynomial has two-sided pointwise error at most epsilon over its internal coins.
- Uniformity is preserved if the target claim is uniform; otherwise the statement is purely nonuniform.

## Equations

- rs-degree-upper-bound: `D_p(s,d,\epsilon) \le (C_p\log(s/\epsilon))^d`. Valid when: Valid when the circuit basis is unbounded-fan-in AC0[p] with fixed prime p, fixed depth parameter d, and error is measured over the probabilistic-polynomial coins.
- restricted-transfer: `\deg^{\mathrm{prob}}_{p,1/3}(SAT_m)>D_p(m^k,d,1/3)\;\Rightarrow\; SAT_m\notin AC0[p]_{d,m^k}`. Valid when: Applies after the SAT slice, input length, circuit size, depth, and nonuniform or uniform convention are all held fixed.
- degree-ceiling: `\deg^{\mathrm{prob}}_{p,\epsilon}(f)\le \deg_p(f)\le m`. Valid when: Valid for Boolean functions on m bits over a fixed finite field, since multilinear exact representation has degree at most m.
- loglog-depth-threshold: `(C_pk\log m)^d<m^{\alpha}\quad\Leftarrow\quad d\le (\alpha-o(1))\frac{\log m}{\log\log m}`. Valid when: Requires size s=m^k, fixed p and k, and depth below the logarithmic-over-loglog threshold before constants overtake the exponent.

## Attempted Derivation

- Assume a source lower bound L_alpha: deg^{prob}_{p,1/3}(SAT_m) >= m^alpha for a fixed alpha in (0,1].
- Use Razborov-Smolensky: AC0[p] circuits of size m^k and depth d have 1/3-error F_p probabilistic polynomials of degree at most (C_pk log m)^d.
- Conclude a valid restricted lower bound when d <= (alpha-o(1)) log m/log log m.
- Try to reach unrestricted SIZE(m^k) by simulating an arbitrary Boolean circuit as an AC0[p] circuit.
- The direct layer-by-layer simulation has depth Theta(m^k), and any depth exceeding about log m/log log m makes the RS degree bound at least m.
- Because every m-bit Boolean function has exact F_p degree at most m, the degree measure cannot exceed the threshold needed for unrestricted polynomial-size circuits.
- MOD_q confirms the obstruction: the same method proves strong fixed-depth AC0[p] lower bounds for a P-easy function.

Blocking gap: Missing DepthReductionCertificate(p,k,alpha): a uniform, target-preserving compiler from SIZE(m^k) SAT circuits to AC0[p] depth below alpha log m/log log m and polynomial size, with no advice, padding, or semantic leakage.

## Falsifiers

- falsifier: MOD_q for q distinct from p is P-computable yet hard for fixed-depth AC0[p], so restricted modular lower bounds do not transfer to P.
- falsifier: the universal F_p degree ceiling deg_p(f)<=m makes any RS-based threshold with D_p>=m vacuous for full SIZE(m^k).
- falsifier: padding an AC0[p]-hard P function preserves P-easiness while weakening only the measured exponent, exposing padding-sensitive transfer claims.
- A valid route must name the target class AC0[p]_{d,s}; saying only that a finite-field method proves a lower bound loses the target-preserving condition.

## Learning

Cycle 47 converts modular-polynomial lower-bound enthusiasm into a valid quantitative gate: deg^{prob}_{p,1/3}(SAT_m)>=m^alpha proves only AC0[p] lower bounds up to depth alpha log m/log log m. The transfer to P collapses at the universal degree ceiling, and MOD_q is the falsifier showing restricted success can occur inside P.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: This branch needs a concrete quantitative threshold, not another statement that AC0[p] lower bounds are restricted. Varying depth shows exactly where the finite-field carrier loses contact with unrestricted circuits.
- Situation seed: Compare m-bit SAT_m with the P-easy function MOD_q under AC0[p] circuits of size m^k, where p and q are distinct primes and the proof carrier is F_p probabilistic degree.
- Varied variable: beta in the depth setting d=beta log m/log log m.
- Held-fixed controls: Prime p, distinct prime q, and size exponent k are fixed constants., Input length is the same m for SAT_m and MOD_q; no padding change is allowed during the transfer., Error is fixed at 1/3 for probabilistic polynomials., No nonuniform advice is introduced beyond the audited circuit itself.
- Expected observation: The RS threshold behaves like m^{beta+o(1)}. A source lower bound m^alpha separates only when beta<alpha, while beta>=1 reaches the universal degree ceiling and cannot support any unrestricted SIZE(poly) conclusion.
- Transfer certificate needed: A formal compiler from arbitrary SIZE(m^k) SAT circuits to AC0[p] circuits of depth beta log m/log log m with beta<alpha and polynomial size, preserving uniformity and the SAT slice. Without this certificate, the intuition remains a restricted-model lower bound.

## Next Experiment

Audit threshold-circuit routes analogously: identify whether sign-rank, margin, or low-degree threshold approximations transfer to TC0 only, and find the exact parameter where unrestricted SIZE(poly) simulation collapses.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For a verifier image I_m of truth tables on m bits and threshold S_m=2^{epsilon m}, MCSP no-side soundness is invalid if any accepted row lies within Hamming distance t of a circuit of size s with s+c t m <= S_m. Equivalently, every valid source must avoid all bad Hamming neighborhoods U_m(s,t) below this correction budget. This sharpens the cycle-46 sparse-correction falsifier into a union-of-balls audit condition.

## Definitions

- source object: an advice-free sequential certificate verifier V_m with E-canonical distinct-image set I_m subset {0,1}^{2^m}.
- target object: an E-uniform hard truth-table family giving MCSP(f_m)>2^{epsilon m} and, through the carrier bridge, E circuit lower-bound exponent delta<epsilon/(kappa(1+D)).
- controlled interface: source length m, threshold S_m, distinct-image entropy D, padding gap kappa, and the map from accepted certificates to truth-table rows.
- target-preserving condition: unranking and bit production remain E-uniform, no advice selects rows, D and kappa stay constant, and no subthreshold random-access circuit is leaked.

## Assumptions

- Fixed fan-in two Boolean circuit basis; equality to one m-bit input costs c m+O(1) gates for an absolute c.
- V_m claims universal MCSP no-side soundness for every accepted distinct row, or uses a previously certified multiplexed hard-row transfer.
- The audit is source-side only; it does not prove P != NP and only validates or rejects proposed carriers.

## Equations

- correction_upper_bound: `\operatorname{MCSP}(f) \le s + c\,t\,m + O(t)`. Valid when: Valid when f differs from a size-s circuit on at most t input strings and corrections are implemented by hardwired equality tests.
- bad_union: `U_m(s,t)=\bigcup_{C:\ |C|\le s} B_H(\mathrm{tt}(C),t)`. Valid when: Valid when the source lower-bound model is unrestricted Boolean circuits over m input variables with Hamming distance on truth tables.
- soundness_disjointness: `I_m\cap U_m(s,t)=\varnothing\quad\text{for every }s+c\,t\,m+O(t)\le S_m`. Valid when: Applies to universal no-side MCSP soundness after constants from the fixed circuit basis have been absorbed.
- carrier_extraction: `\delta < \frac{\epsilon}{\kappa(1+D)}`. Valid when: Requires the target-preserving carrier transfer with E-canonical unranking, constant gap kappa, and distinct-image entropy D.

## Attempted Derivation

- Define S_m=2^{epsilon m} and U_m(S_m/2,S_m/(4cm)) as the bad set of tables correctable from subthreshold circuits.
- Use the union bound to show a random low-D image avoids U_m with probability 1-2^{-2^m+o(2^m)}.
- Try to set D=0 by taking the lexicographically first table outside U_m, then invoke the existing bridge to obtain delta<epsilon/kappa.
- Audit E-uniformity: exact outside-U testing enumerates about 2^{Theta(S_m log S_m)} circuits, far beyond the 2^{O(m)} budget for bit production.
- Audit barrier status: if outside-U becomes poly(N)-constructive and dense, it is a large useful natural-property-style predicate against N^{epsilon} circuits; a sparse non-large image would avoid that barrier but is not supplied by the derivation.

Blocking gap: No valid E-uniform, advice-free, non-natural selector is known for the complement of the bad union while preserving low distinct-image entropy and avoiding random-access leakage.

## Falsifiers

- An accepted row lies in U_m(s,t) with s+c t m<=2^{epsilon m}, giving an explicit small correction circuit.
- The carrier is specified by random advice or by a nonuniform table list rather than an E-uniform unranker.
- The construction uses lexicographic exclusion of all small circuits and therefore needs 2^{2^{Theta(epsilon m)}} time.
- A bit-addressable generator for accepted rows has circuit size below the claimed MCSP threshold.
- The proof exposes a dense poly(N)-constructive outside-U predicate; this is a large useful natural-property-style falsifier for the route.
- The source factors through a rankable profile, low-degree predicate, affine syndrome, or sparse perturbation invariant already known to accept low-complexity fillers.

## Learning

Cycle 47 formalizes the sparse-correction obstruction as bad-ball disjointness and computes the calibration bound: random low-D images robustly avoid every subthreshold correction ball with overwhelming probability. Thus the route is not blocked by combinatorics. It is blocked by producing an E-uniform, non-large, non-natural selector; lex-first and dense outside-U repairs are invalid.

## Gedanken Experiment Design Seed

- Need decision: `design-now-as-falsifier-probe`
- Rationale: The route now needs a quantitative check that the robust-distance audit is not itself impossible; random sparse carriers isolate explicitness as the real obstruction.
- Situation seed: For each m choose M=2^{D m} independent random truth tables and call the image acceptable if every row avoids all Hamming balls around circuits of size 2^{epsilon m}/2.
- Varied variable: The correction-radius exponent beta in r_m=2^{beta m}, with beta swept from epsilon-o(1) up to values below 1.
- Held-fixed controls: epsilon<1 is fixed as the MCSP threshold exponent., D and kappa are fixed constants used in the carrier extraction delta<epsilon/(kappa(1+D))., The circuit basis and equality-test correction cost c m are fixed., No advice, no dense constructive property, and no subthreshold random-access generator are allowed in any transfer certificate.
- Expected observation: For every beta<1 the random image avoids the bad union with probability 1-2^{-2^m+o(2^m)}, so distance robustness is abundant and the missing ingredient is explicit non-natural selection.
- Transfer certificate needed: Before the intuition may enter the proof queue, supply an E-uniform sequential unranker with low D whose image avoids U_m(s,t), plus a soundness proof that is non-large, nonuniform-free, and not reducible to exact MCSP enumeration.

## Next Experiment

Test whether proof-complexity certificates for avoiding U_m(s,t) can be sparse and non-large: vary certificate entropy D while holding epsilon,kappa fixed and audit whether verification secretly enumerates circuits or creates a natural property.
