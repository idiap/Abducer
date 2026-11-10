# cycle-0033

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For the generated-OR carrier, the valid source audit is not a single local SAT-label predicate but every subthreshold feature-aggregator surrogate plus its residual. If C(H_N)>N^{1+epsilon-o(1)} in SIZE, then for every local feature family A and bag aggregator B with subthreshold evaluation cost, the residual H_N xor S_{A,B} must itself have circuit complexity N^{1+epsilon-o(1)}. Conversely, any subthreshold feature-aggregator with subthreshold residual is a concrete falsifier for the proposed source lower bound.

## Definitions

- source object: H_N(x)=OR_{j<=M_N} SAT(G_{N,j}(x)) on N-bit inputs, where M_N=N^q and each generated formula has length L=(log N)^d.
- target object: nonuniform Boolean circuits for SAT on L-bit formulas; excluding size L^c for every fixed c is the target-preserving SAT notin P/poly consequence at these lengths.
- controlled interface: a target SAT circuit may be substituted only as a charged local feature inside the generated bag, followed by a charged aggregator; generator cost, feature-evaluation cost, and residual correction cost are all counted in the same SIZE model.
- target-preserving condition: d>1, rho<1+epsilon, q<1+epsilon, no advice hidden in G_N, and every additional local feature or aggregator remains below the N^{1+epsilon} source threshold.

## Assumptions

- C is nonuniform fan-in-two Boolean circuit size, closed under composition and xor with additive overhead.
- The tuple generator G_N=(G_{N,1},...,G_{N,M_N}) has circuit size N^{rho+o(1)} and outputs M_N formulas of length L.
- A=(A_1,...,A_t) is a family of local predicates on L-bit formulas with total size S_A=sum_i C(A_i)=N^{alpha+o(1)}.
- B is a nonuniform bag aggregator on the M_N by t feature matrix with size N^{beta+o(1)}.
- S_{A,B}(x)=B((A_i(G_{N,j}(x)))_{j<=M_N,i<=t}) and R_{A,B}=H_N xor S_{A,B}.
- The claimed source lower bound is C(H_N)>N^{1+epsilon-o(1)} in the same circuit model.

## Equations

- carrier_parameters: `M_N=N^q, L=(log N)^d, C(G_N)=N^{rho+o(1)}`. Valid when: Valid when the generated-bag carrier fixes polynomially many polylogarithmic SAT queries.
- feature_surrogate: `S_{A,B}(x)=B((A_i(G_{N,j}(x)))_{j<=M_N,i<=t})`. Valid when: Valid when all local features are evaluated on generated formulas before aggregation.
- surrogate_upper_bound: `C(S_{A,B}) <= N^{rho+o(1)} + N^{q+alpha+o(1)} + N^{beta+o(1)}`. Valid when: Valid when G_N, all local features, and B are circuits in the same SIZE model.
- residual_reconstruction: `C(H_N) <= O(C(S_{A,B}) + C(R_{A,B}) + N), where R_{A,B}=H_N xor S_{A,B}`. Valid when: Valid when the residual circuit is allowed to correct the surrogate on all inputs.
- threshold_contradiction: `max{rho,q+alpha,beta,gamma}<1+epsilon and C(R_{A,B})<=N^{gamma+o(1)} imply C(H_N)<N^{1+epsilon-o(1)}`. Valid when: Applies when every charged component stays below the claimed source lower-bound exponent.
- feature_residual_exponent: `Phi_N^{feat}=inf_{A,B} max{rho,q+alpha(A),beta(B),log_N C(H_N xor S_{A,B})}`. Valid when: Valid when the infimum ranges over nonuniform feature families and bag aggregators.

## Attempted Derivation

- Start with any feature family A on L-bit formulas and any aggregator B over the M_N by t feature matrix.
- Compose G_N with all A_i on all M_N positions; by circuit composition this costs N^{rho+o(1)}+N^{q+alpha+o(1)}.
- Feed the resulting feature matrix to B, obtaining S_{A,B} with total size at most N^{rho+o(1)}+N^{q+alpha+o(1)}+N^{beta+o(1)}.
- If a residual circuit R_{A,B}=H_N xor S_{A,B} has size N^{gamma+o(1)}, combine S_{A,B}, R_{A,B}, and one xor gate to compute H_N.
- Thus any feature-aggregator-residual certificate with all exponents below 1+epsilon contradicts the claimed N^{1+epsilon-o(1)} source lower bound.
- For target transfer, choose t=1, A_1 equal to the hypothesized SAT_L circuit of size L^c=N^{o(1)}, and B=OR_{M_N}; the residual is zero and the cost is N^{max{rho,q}+o(1)}.

Blocking gap: The missing proof obligation is a lower bound on C(H_N xor S_{A,B}) for all subthreshold feature families and aggregators. Promise SAT hardness on the generated range does not imply this residual lower bound, because B may exploit many weak local features jointly.

## Falsifiers

- feature-compression falsifier: t=N^tau local predicates with q+alpha<1+epsilon and a small aggregator predict H_N up to subthreshold residual complexity.
- advice-coded aggregator falsifier: B stores labels for large generated-range blocks with beta<1+epsilon, collapsing the source lower bound without solving SAT globally.
- low-dimensional generator falsifier: G_N maps bags into a feature space where OR-SAT is decided by a small lookup or threshold over features.
- structured residual falsifier: H_N xor S_{A,B} is easy even when its error support is dense, so sparse-error audits miss the collapse.
- barrier audit: a dense constructive proof that all feature-aggregator residuals are hard would look natural unless it exploits non-natural SAT semantics or another explicit non-natural certificate.

## Learning

Cycle 33 strengthens the generated-OR source obligation from single residual correction to feature-aggregator residual hardness. This is a contribution-making repair: it preserves the exact target bridge but exposes a broader nonuniform-leakage falsifier class that prior selector and separator audits did not cover.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the repaired source audit.`
- Rationale: The abstract residual gate is too broad unless we test whether parallel weak local formula features can jointly compress generated SAT bags below the magnification threshold.
- Situation seed: Take H_N as OR of M_N=N^q formulas of length L=(log N)^d generated by an explicit expander-walk clause generator G_N of size N^rho; audit feature maps A_1,...,A_t on formulas and an aggregator B on the resulting bag-feature matrix.
- Varied variable: tau where t=N^tau and the total feature size exponent alpha includes all t local predicates.
- Held-fixed controls: d>1 so truth-table lookup costs N^{omega(1)} and does not give the old short-query collapse., q<1+epsilon and rho<1+epsilon so the target SAT-substitution bridge remains valid., All circuits are nonuniform SIZE circuits with no uncharged advice in G_N or in feature indexing., The target transfer uses the one-feature SAT predicate and OR aggregator as a zero-residual control case.
- Expected observation: There should be a sharp leakage threshold near q+alpha=1+epsilon: if residual complexity falls below N^{1+epsilon-o(1)} for tau below this boundary, the generated-OR carrier fails; if it stays high for all tau below the boundary, the feature-leakage audit survives this probe.
- Transfer certificate needed: Either prove Phi_N^{feat}>=1+epsilon-o(1) for all feature families with q+alpha,beta<1+epsilon, or exhibit an explicit subthreshold A,B,R certificate; only such a theorem or counterexample may affect the P/poly transfer queue.

## Next Experiment

Formalize the restricted case where B is a depth-2 threshold or DNF over t=N^tau local features, compute the exact q+alpha+beta leakage threshold, and search for an explicit low-residual construction on expander-walk generated SAT bags.

# Barrier-Aware Lower-Bound Route: rectangle-cover target gate

## Candidate Lemma

Balanced one-rectangle-cover lower bounds transfer to DNF and low-nondeterministic-communication targets, but not to full polynomial-size circuits. The obstruction is formal: EQ_r is in SIZE(O(r)) and has maximum one-cover complexity under the same split, so no threshold tau<=r is useful against SIZE(m^k), while tau>r is impossible for the source.

## Definitions

- source object: M_{SAT_m}^pi, the 2^r by 2^r communication matrix of the length-m SAT truth table with m=2r under a fixed balanced partition pi.
- target object: SIZE(m^k) Boolean circuits on the same m input bits, with DNF_T and low-N^1 protocol classes recorded as restricted salvage targets.
- controlled interface: a circuit-to-rectangle-cover simulation asserting that each target function h has C^1(M_h^pi)<=a(m) under the same partition and uniformity conventions.
- target-preserving condition: the source threshold tau(m) must satisfy C^1(M_{SAT_m}^pi)>tau(m)>=a(m), and the rejecting property must exclude every target circuit truth table, not just low-cover matrices.
- C^1(M) denotes ceil(log_2 cov_1(M)), where cov_1 is the minimum number of 1-monochromatic rectangles covering all 1-entries.
- The route is a lower-bound carrier for a named class only after an all-functions-in-target upper bound on C^1 is proved.

## Assumptions

- m=2r and the partition pi is fixed before comparing SAT_m with target functions.
- Communication rectangles are over the same input split used by the source lower bound.
- The target class is nonuniform SIZE(m^k) unless explicitly restricted.
- No advice may choose a different partition or a different matrix measure for each target circuit.

## Equations

- matrix_size: `\(N=2^m=2^{2r}\)`. Valid when: Valid when the length-m truth table is viewed through one fixed balanced two-party partition.
- one_cover_complexity: `\(C^1(M)=\lceil \log_2 \operatorname{cov}_1(M)\rceil\)`. Valid when: Applies when one-rectangles are the covering objects and logarithmic nondeterministic communication cost is being measured.
- equality_falsifier: `\(\operatorname{cov}_1(M_{EQ_r})=2^r,\quad C^1(M_{EQ_r})=r,\quad EQ_r\in SIZE(O(r))\)`. Valid when: Requires a fixed split in which EQ_r compares Alice's r bits with Bob's r bits.
- dnf_transfer: `\(\operatorname{DNFsize}(h)\le T\Rightarrow C^1(M_h^\pi)\le \lceil\log_2 T\rceil\)`. Valid when: Applies when the target circuit is a DNF and each term factors across the fixed partition.
- trivial_ceiling: `\(C^1(M_f^\pi)\le r\)`. Valid when: Valid when no promise restricts the matrix and singleton-row rectangles are allowed.

## Attempted Derivation

- Fix m=2r and form M_f^pi from length-m truth tables under one balanced partition.
- Assume a source proof gives C^1(M_{SAT_m}^pi)>tau(m).
- For DNF_T, each term is a 1-rectangle, so tau>log T yields a valid DNF lower bound.
- Try to extend the same interface to SIZE(m^k) by recursively translating circuit gates into covers.
- The recursive simulation gives no useful bound below r, and every matrix already has C^1<=r by singleton-row rectangles.
- EQ_r is computable by O(r)-size circuits and has cov_1=2^r, so any all-SIZE upper bound C^1<r is false.
- Thus the desired full circuit transfer would need tau>r, but the source measure can never exceed r.

Blocking gap: The missing bridge is an all-polynomial-circuit theorem C^1(M_h^pi)<=r-epsilon r under a fixed split; EQ_r proves this theorem false.

## Falsifiers

- EQ_r is a linear-size circuit family with C^1(M_EQ)=r, a direct falsifier to full-SIZE usefulness of one-cover thresholds.
- The universal ceiling C^1(M_f)<=r is a quantitative threshold-collapse falsifier for any proposed tau>r source claim.
- A DNF-only cover simulation claimed for arbitrary circuits is invalid unless AND gates are compressed without increasing cover cost.
- A fixed explicit fooling-set checker has density 2^{-Omega(T^2)}, so it is not automatically a natural-property falsifier of PRFs at polynomial density.
- Changing the partition after seeing the target circuit leaks nonuniform information and breaks the controlled interface.

## Learning

Cycle 33 turns rectangle-cover and fooling-set enthusiasm into a valid target gate. The method transfers quantitatively to DNF_T or classes with N^1_pi<=a(m), but it fails for full SIZE(poly) because EQ_r is small and has maximum one-cover and fooling-set complexity. This is route-level barrier progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and a restricted-transfer calibration.`
- Rationale: The branch needs a concrete target-preserving test because communication lower bounds can look strong while measuring functions that small circuits also realize. Equality supplies a small-circuit high-cover control object under the exact same matrix interface.
- Situation seed: For m=2r, compare the balanced communication matrices of SAT_m and EQ_r. The proposed route proves C^1(M_SAT^pi)>tau and tries to infer SAT_m notin SIZE(m^k).
- Varied variable: The threshold tau in units of r, equivalently gamma=tau/r from 0 to 1.
- Held-fixed controls: The partition pi is fixed and balanced before source and target are compared., The target remains nonuniform SIZE(m^k) unless explicitly replaced by DNF_T or a low-N^1 class., The measure is one-rectangle cover complexity C^1 with no advice-dependent repartitioning., The source object is the total length-m SAT truth table, not a promise or padded submatrix.
- Expected observation: For tau>log T the DNF_T consequence is valid. For full SIZE(m^k), every tau<r is defeated by EQ_r, while tau>r is impossible because C^1(M)<=r for all matrices.
- Transfer certificate needed: A formal all-target bound C^1_pi(C_m)<tau for the named class C_m. For SIZE(poly) this certificate is refuted by equality, so only restricted classes with proven low nondeterministic communication remain eligible.

## Next Experiment

Audit partition-robust variants: vary whether the source lower bound holds for one split, all balanced splits, or a target-chosen split, and test against equality, indexing, and small DNF controls before claiming any circuit-class transfer.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For any E-canonical bounded-image MCSP source, the ranked decoder F_m(r,x) is the exact leakage interface: row hardness at threshold 2^{epsilon m} is impossible if F_m has circuits 2^{beta m} with beta<epsilon, while an aggregate lower bound above 2^{(D+epsilon)m} forces a hard row.

## Definitions

- source object: a canonical bounded-image MCSP certificate source V_m whose accepted distinct outputs are truth tables T_{m,r}:{0,1}^m->{0,1} indexed by ranks r in {0,1}^{d_m}, d_m<=D m.
- target object: an E-uniform language L obtained by padding and multiplexing a hard accepted row, with desired circuit lower bound SIZE(2^{delta n}) against Boolean circuits.
- controlled interface: E-canonical distinct-image unranking plus a ranked decoder F_m(r,x)=T_{m,r}(x), MCSP threshold s_m=2^{epsilon m}, density/padding loss kappa, image entropy D.
- target-preserving condition: D,kappa,epsilon are constants, epsilon<=alpha_V, unranking is E-uniform with no advice, and any selected hard row is transferred only through the established multiplexing bridge delta<epsilon/(kappa(1+D)).

## Assumptions

- Circuit size C(.) is nonuniform Boolean circuit size for length-m truth tables; MCSP no-side means C(T)>s_m.
- The rank length d_m<=D m indexes canonical distinct accepted images; invalid ranks are mapped to a fixed easy row.
- The source may be sequentially E-explicit, but ranked random access is not assumed.
- All logarithmic and polynomial factors are absorbed into o(m) exponent slack.

## Equations

- decoder-row-sandwich: `\max_r C(T_{m,r}) \le C(F_m)+O(d_m) \le 2^{d_m}(\max_r C(T_{m,r})+\mathrm{poly}(m+d_m))`. Valid when: Valid when ranks enumerate distinct accepted images uniformly and circuits may hardwire a fixed rank to obtain a row slice.
- subthreshold-ranked-decoder-falsifier: `C(F_m)\le 2^{\beta m}\ \wedge\ \beta<\epsilon-o(1)\ \Longrightarrow\ \forall r\, C(T_{m,r})<2^{\epsilon m}`. Valid when: Applies when a nonuniform ranked decoder circuit exists for all valid ranks at length m.
- aggregate-decoder-sufficient-condition: `C(F_m)>2^{(D+\epsilon)m+o(m)}\ \Longrightarrow\ \exists r\, C(T_{m,r})>2^{\epsilon m}`. Valid when: Requires d_m at most Dm and the aggregate decoder lower bound to exceed the full rank multiplexer upper bound.
- preserved-transfer: `\exists r\, C(T_{m,r})>2^{\epsilon m}\ \Longrightarrow\ \exists L\in E\ \forall \delta<\frac{\epsilon}{\kappa(1+D)}:\ C_L(n)>2^{\delta n}\ \text{infinitely often or on the certified padded lengths}`. Valid when: Applies after the reduction preserves E-uniform canonical unranking, constant density loss, and the MCSP threshold parameters.

## Attempted Derivation

- Start with a canonical bounded-image verifier V_m, rank length d_m<=D m, and claimed existence of an accepted table T with MCSP threshold 2^{epsilon m}.
- Define the ranked decoder F_m(r,x) as the x-th bit of the r-th distinct accepted image under E-canonical unranking.
- Hardwire r in any circuit for F_m to obtain a circuit for row T_{m,r}; conversely multiplex circuits for all rows to compute F_m.
- Derive the subthreshold ranked-decoder falsifier beta<epsilon and the sufficient aggregate lower bound C(F_m)>2^{(D+epsilon)m+o(m)}.
- Feed any certified hard row into the existing carrier bridge to recover delta<epsilon/(kappa(1+D)).

Blocking gap: The only generic certification found is an aggregate lower bound for F_m, which is already a direct E-function circuit lower bound at exponent (D+epsilon)/(1+D) and is stronger than the transferred target exponent.

## Falsifiers

- falsifier: a ranked decoder F_m of circuit size 2^{beta m} with beta<epsilon-o(1) makes every row MCSP-easy at the claimed threshold.
- falsifier: a bounded-image proof based only on |I_m|<=2^{D m} is invalid because I_m may be wholly contained in the easy functions.
- falsifier: proving only C(F_m)>2^{gamma n_F} with gamma below (D+epsilon)/(1+D) does not force any hard row.
- falsifier: nonuniform rank advice or a nonuniform length selector breaks the valid E-uniform transfer certificate.
- falsifier: D growing with m or kappa growing with m collapses delta to o(1).
- falsifier: epsilon>alpha_V contradicts the verifier cap before the carrier bridge can be applied.

## Learning

Cycle 33 identifies the ranked decoder as the exact leakage interface for low-image MCSP carriers. The valid transfer remains delta<epsilon/(kappa(1+D)), but bounded-image entropy cannot count its way to hardness. A valid source theorem must give structural row-hardness without advice, or else use an external non-natural aggregate decoder lower bound; subthreshold ranked random access is a concrete falsifier.

## Gedanken Experiment Design Seed

- Need decision: `use now as a falsifier probe`
- Rationale: The branch is blocked at source construction; the ranked-decoder lemma gives a concrete threshold beta that can invalidate proposed sequential sources before another abstract restatement.
- Situation seed: A canonical MCSP image source has ranks r of length Dm and outputs N=2^m truth tables. The x-th bit is recovered by replaying a padded SAT-query transcript or proof transcript of length 2^{beta m}; the source claims a no-side threshold 2^{epsilon m}.
- Varied variable: ranked random-access seek exponent beta
- Held-fixed controls: D is a fixed constant and distinct-image unranking is E-canonical., kappa is a fixed padding-density loss and the target transfer remains delta<epsilon/(kappa(1+D))., No nonuniform advice, no length selector, and epsilon<=alpha_V are allowed., The source remains sparse and non-large, so natural-proofs largeness is not introduced.
- Expected observation: If beta<epsilon, unrolling the ranked decoder gives circuits below the claimed MCSP threshold and the source fails. If beta>=epsilon, this leakage falsifier disappears but row soundness is still unproved.
- Transfer certificate needed: A valid certificate must prove either a structural hard row in the bounded image or a non-natural aggregate decoder lower bound above 2^{(D+epsilon)m+o(m)}, while preserving E-uniformity and avoiding advice.

## Next Experiment

Audit a concrete proof-transcript image source: compute D, beta, alpha_V, and kappa; reject it if its row bits have a padded-query ranked decoder below 2^{epsilon m}, and otherwise ask for a structural non-counting hard-row certificate.
