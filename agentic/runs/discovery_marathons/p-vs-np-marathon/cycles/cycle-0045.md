# cycle-0045

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: Greedy Cap Dual Gate

## Candidate Lemma

For the high-q generated-OR carrier, a valid N^{1+epsilon-o(1)} source lower bound must defeat the greedy residual cap denominator of all valid one-sided bag separators. If every residual positive set has a separator hitting a 1/D fraction and D<N^{epsilon-sigma-o(1)}, then the carrier has subthreshold circuits; this is a concrete falsifier of the source lower bound.

## Definitions

- source object: H_N(x)=OR_{j<=M} SAT(F_{N,j}(x)), where x in {0,1}^N, M=N^q, each F_{N,j}(x) has length L=(log N)^d, and all queries are produced by a generator G_N of size N^{rho+o(1)}.
- target object: nonuniform SAT_L circuits, with target consequence SAT notin P/poly only after a valid H_N lower bound N^{1+epsilon-o(1)} survives the carrier audit for q,rho<1+epsilon.
- controlled interface: substitute a size L^c SAT circuit into each generated query for target transfer, and audit the reverse source direction by valid one-sided bag separators of cost at most N^sigma.
- target-preserving condition: the bridge is valid only when separator covers, equality-error patches, generator advice, and lookup tables all stay above the N^{1+epsilon} source threshold; any subthreshold cover is a falsifier of the carrier lower bound, not a proof of SAT hardness.
- valid one-sided bag separator: a circuit A in S_sigma with A^{-1}(1) subseteq H_N^{-1}(1) on the generated range; it may be position-indexed or certificate-based but must make no false positive on negative bags.
- cap denominator D_{sigma,E}: the least D such that every residual R subseteq H_N^{-1}(1) with |R|>E has some A in S_sigma satisfying |A^{-1}(1) cap R|>=|R|/D.

## Assumptions

- epsilon>0 is fixed and there is slack eta>0 with max{q,rho}<=1+epsilon-eta.
- The high-q repair is active: (1+epsilon)/2<q<1+epsilon-eta and d>1, so lookup over all SAT queries is superthreshold.
- The separator cost exponent satisfies 0<=sigma<epsilon-eta; otherwise the denominator threshold becomes vacuous.
- Missed positive inputs are corrected by equality gates of total size O(EN), so E<=N^{epsilon-eta} is patchable and larger E is not a useful falsifier.
- The family S_sigma is finite or effectively discretized at circuit-size N^sigma, and all members are semantically one-sided on the actual generated range.

## Equations

- target_substitution_upper_bound: `C(H_N)\le N^{\rho+o(1)}+N^q L^c=N^{\max\{\rho,q\}+o(1)}`. Valid when: Valid when L=(log N)^d with d>1, SAT_L has nonuniform circuits of size L^c, and the generator for all N^q queries has size N^{rho+o(1)}.
- separator_cover_upper_bound: `C(H_N)\le C(G_N)+O(KN^{\sigma}+EN)`. Valid when: Valid when the separators are semantically one-sided on the generated range, cover all but E positive bags, and equality patches for missed inputs cost O(N) each.
- greedy_cover_size: `K\le \left\lceil D_{\sigma,E}\log\frac{|H_N^{-1}(1)|}{\max\{1,E\}}\right\rceil\le N^{1+o(1)}D_{\sigma,E}`. Valid when: Valid when every residual positive set larger than E has a separator cap at least its reciprocal denominator, so greedy removal is legitimate.
- cap_denominator_falsifier_threshold: `D_{\sigma,E}<N^{\epsilon-\sigma-o(1)}\ \wedge\ E<N^{\epsilon-o(1)}\ \Longrightarrow\ C(H_N)<N^{1+\epsilon-o(1)}`. Valid when: Valid contrapositively after the log |P_N| <= N factor, generator cost, and equality-error corrections are all charged below the source threshold.

## Attempted Derivation

- Let P_N=H_N^{-1}(1) and fix the valid separator family S_sigma of size-cost at most N^sigma.
- Assume every residual R subseteq P_N with |R|>E has a separator A hitting at least |R|/D of R.
- Greedy selection removes a 1/D fraction of the current residual, so after at most D log(|P_N|/E) <= N^{1+o(1)}D choices it leaves at most E positives uncovered.
- OR the chosen one-sided separators. Soundness gives no false positives on H_N^{-1}(0); patch the remaining E positives by equality circuits of size O(EN).
- The resulting upper bound is C(H_N)<=N^{rho+o(1)}+N^{1+sigma+o(1)}D+O(EN).
- If D<N^{epsilon-sigma-o(1)} and E<N^{epsilon-o(1)}, this is below N^{1+epsilon-o(1)}, contradicting the proposed source lower bound.
- Therefore a valid source lower-bound proof must either prove D>=N^{epsilon-sigma-o(1)} for all sigma<epsilon or provide hard residual distributions with cap at most N^{-(epsilon-sigma)+o(1)}.

Blocking gap: The derivation only rules out separator-cover upper bounds. It does not prove that every subthreshold exact circuit for H_N has a valid one-sided separator normal form.

## Falsifiers

- cap-denominator falsifier: some sigma<epsilon and E<N^{epsilon-o(1)} have D_{sigma,E}<N^{epsilon-sigma-o(1)}, yielding a subthreshold circuit for H_N.
- normal-form falsifier: an exact small circuit computes H_N using two-sided global information that cannot be represented by valid one-sided separator covers.
- one-sidedness falsifier: a proposed local predicate accepts even one generated negative bag, invalidating the separator-cover upper bound and the residual distribution certificate.
- nonuniform leakage falsifier: the generator or separator list hides advice selecting easy positive fibers, reducing the cover cost below N^{1+epsilon}.
- barrier falsifier: a proof of the residual cap lower bound via a large constructive property of SAT truth tables would run into the natural-proofs obstruction under pseudorandom functions; the current semantic promise object is only outside that barrier's direct scope.
- lookup-threshold falsifier: if d<=1 or variable entropy drops, exhaustive SAT lookup or partial certificate covers can re-enter below the source threshold.

## Learning

Cycle 45 adds the missing logarithmic greedy-cover charge and converts the cap profile into an exact threshold: D_{sigma,E}<N^{epsilon-sigma-o(1)} is a concrete upper-bound falsifier for the generated-OR source lower bound. A valid route must now prove hard residual positive distributions against all one-sided separators and also close the normal-form gap from arbitrary circuits to separator covers.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch now has a quantitative denominator threshold; another abstract restatement would not test whether the high-q generated-OR carrier can plausibly beat valid one-sided separator covers.
- Situation seed: Take a target-preserving generated-OR family where an N-bit seed produces M=N^q random-looking 3CNF instances of length L=(log N)^d with d>1, balanced around the SAT threshold, and define H_N as the OR of their SAT labels.
- Varied variable: separator size exponent sigma in the interval 0<=sigma<epsilon.
- Held-fixed controls: q is fixed in ((1+epsilon)/2,1+epsilon-eta) so dense tuple leakage is threshold-blocked., rho is fixed below 1+epsilon-eta so generator cost cannot mask the separator audit., d>1 is fixed so exhaustive lookup over SAT truth tables is superthreshold., All separators must be valid one-sided on the generated range; false positives on negative bags are disallowed., The target substitution bridge SAT in SIZE(n^c) -> C(H_N)<=N^{max{rho,q}+o(1)} is held fixed.
- Expected observation: As sigma increases, the critical denominator should follow D_crit(sigma)=N^{epsilon-sigma}. If empirical or combinatorial caps give D below this curve for any sigma, the source carrier is falsified; if random-looking residuals stay below cap N^{-(epsilon-sigma)+o(1)} for all sigma, the route earns a concrete lower-bound subproblem.
- Transfer certificate needed: A formal pseudorandom/residual-distribution theorem against every nonuniform valid one-sided separator of cost N^sigma, plus a normal-form theorem showing arbitrary subthreshold circuits for H_N reduce to the audited separator-cover model.

## Next Experiment

Work in a restricted circuit model such as De Morgan formulas or AC0[p] and test whether exact circuits for H_N admit an approximate one-sided separator normal form; compute the resulting D_{sigma,E} threshold for the same high-q polylog generated-OR carrier.

# Barrier-Aware Lower-Bound Route: Formula Fanout Leakage Gate

## Candidate Lemma

An unrolling-only De Morgan formula lower-bound route cannot transfer to SAT_m notin SIZE(m^k) for any fixed k>1. The required formula lower bound is above 2^{Omega(m^k)}, while every m-input Boolean function has a formula of size O(m2^m). This certifies a target-model failure, not P != NP progress.

## Definitions

- source object: TT_m(SAT) viewed as an m-input Boolean function with fan-in-2 De Morgan formula size F_2.
- target object: nonuniform fan-in-2 Boolean circuits SIZE(m^k) for SAT_m, with k fixed before the lower-bound claim.
- controlled interface: a compiler from each target circuit for SAT_m to a De Morgan formula computing the same slice, with size bound B_{form<-circ}(m,k).
- target-preserving condition: the formula lower bound must exceed B_{form<-circ}(m,k) on the same input length m and without changing the SAT slice, padding parameter, or advice budget.

## Assumptions

- Basis is fan-in-2 AND/OR/NOT; NOT gates may be pushed to leaves with constant-factor loss.
- The only target bridge allowed in this lemma is fanout removal by recursive duplication of subcircuits.
- No separate theorem bounds formula size of all m^k-size circuits below the universal truth-table DNF bound.

## Equations

- unroll_simulation: `C_2(f)\le s \;\Longrightarrow\; F_2(f)\le 2^{O(s)}`. Valid when: Valid when the target circuit has fan-in two and the only allowed simulation removes fanout by recursively duplicating subcircuits.
- universal_formula_upper_bound: `\max_{f:\{0,1\}^m\to\{0,1\}} F_2(f) \le O(m2^m)`. Valid when: Valid when the source object is an arbitrary total m-bit Boolean function and a DNF over accepting inputs is permitted.
- unrolling_transfer_sufficiency: `F_2(SAT_m)>2^{c m^k} \;\Longrightarrow\; SAT_m\notin SIZE(m^k)`. Valid when: Applies when c is a constant large enough for the fanout-duplication simulation of every size m^k target circuit.
- collapse_for_polynomial_circuits: `O(m2^m) < 2^{c m^k}\quad (k>1,\;m\to\infty)`. Valid when: Requires fixed k greater than one and sufficiently large m so polynomial exponents dominate the linear truth-table exponent.

## Attempted Derivation

- Let a proposed route prove F_2(SAT_m)>L(m).
- To infer SAT_m notin SIZE(m^k), take the contrapositive: a size m^k circuit for SAT_m must imply a formula for SAT_m of size at most B(m,k).
- The generic fanout-removal compiler gives B(m,k)=2^{O(m^k)}; thus the route needs L(m)>2^{O(m^k)}.
- But the DNF upper bound gives F_2(SAT_m)<=O(m2^m) for every m-input SAT slice.
- For every fixed k>1 and large m, O(m2^m) is below 2^{c m^k}; hence the unrolling-only transfer asks for an impossible source lower bound.
- A depth-restricted target avoids this collapse because B(m,D)=2^{D+1}, which is polynomial for D=O(log m) and quasipolynomial for D=O(log^2 m).

Blocking gap: The missing object is a nontrivial anti-fanout theorem: an upper bound on the formula size of every m^k-size circuit function below the formula lower bound claimed for SAT_m. Without it, formula lower bounds measure lack of fanout, not lack of polynomial circuits.

## Falsifiers

- Parity_m is a falsifier to the inference that superlinear De Morgan formula lower bounds imply comparable circuit lower bounds: F_2(PARITY_m)=Theta(m^2) but C_2(PARITY_m)=O(m).
- The universal DNF upper bound F_2(f)<=O(m2^m) is a falsifier for any unrolling-only requirement such as F_2(SAT_m)>2^{m^2}.
- Padded SAT g_{r,alpha}(x,z)=SAT_r(x), with m=r^alpha, is a falsifier for measuring formula lower bounds in the padded length while the hard core depends on only r variables.
- A claimed formula-size route is not valid for P-vs-NP transfer unless it names B_FC(m,k) and proves the SAT lower bound exceeds it.

## Learning

Cycle 45 isolates formula fanout leakage as a concrete target gate. A De Morgan formula lower bound is a valid lower bound for formulas and bounded-depth circuit classes, but the unrolling-only bridge to SIZE(m^k) requires an impossible 2^{Omega(m^k)} source lower bound for k>1. The contribution is a route-level quarantine and repair condition, not progress on P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for formula-size-to-circuit transfers.`
- Rationale: The abstract slogan that formula lower bounds are circuit lower bounds with no fanout hides a quantitative collapse. Padding makes the collapse visible on a target-preserving SAT-derived family.
- Situation seed: Consider g_{r,alpha}(x,z)=SAT_r(x) on m=r^alpha inputs, where z is ignored padding and the target claim is g_{r,alpha} notin SIZE(m^k).
- Varied variable: The padding exponent alpha>1, with k fixed in the target circuit size m^k.
- Held-fixed controls: Source measure is fan-in-2 De Morgan formula size F_2 on the full m-bit truth table., Target class is unrestricted nonuniform fan-in-2 SIZE(m^k), not formulas or NC1., The reduction preserves the SAT core exactly and adds only ignored padding variables., The only admitted compiler is target-circuit to source-formula simulation without extra advice.
- Expected observation: As alpha increases, the best possible source lower bound remains at most O(r2^r), while the unrolling transfer threshold is 2^{Omega(m^k)}=2^{Omega(r^{alpha k})}. For alpha k>1 the transfer certificate collapses completely.
- Transfer certificate needed: A valid proof influence would require either a depth/fanout-preserving target restriction or a theorem bounding formula size of all SIZE(m^k) functions below O(r2^r); absent that certificate, the thought experiment quarantines the route.

## Next Experiment

Audit general branching-program lower bounds with the same compiler-threshold discipline: name the source BP model, determine whether polynomial-time circuits compile to that BP class below the claimed lower bound, and look for P-easy high-BP-complexity falsifiers.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

A nonempty MCSP source predicate that depends only on one-counts in a subthreshold rankable partition cannot be a sound no-side carrier at threshold 2^{epsilon m}. Its accepted profile has a canonical lexicographic filler with circuits below the claimed threshold.

## Definitions

- source object: a nonempty MCSP certificate predicate A_m on N=2^m truth-table bits whose acceptance depends only on counts inside a rankable partition Pi_m={C_1,...,C_B}.
- target object: no-side MCSP carrier soundness against unrestricted Boolean circuits of size s_m=2^{epsilon m}, subsequently usable by the existing E lower-bound extraction.
- controlled interface: accepted or emitted truth tables must all have circuit complexity greater than s_m before any carrier-to-E transfer is valid.
- target-preserving condition: the partition, rank predicates, and canonical profile filling are E-uniform and use no advice, and the source threshold satisfies beta+eta<epsilon.
- rankable partition: each cell C_i has membership and rank-comparison circuits of size R_m<=2^{eta m}m^{O(1)}.
- profile predicate: A_m(T)=Q_m((|T^{-1}(1) cap C_i|)_{i<=B}) for some uniform decision procedure Q_m.

## Assumptions

- B_m<=2^{beta m} and R_m<=2^{eta m}m^{O(1)}.
- A_m is nonempty for infinitely many source lengths m.
- Acceptance is invariant under permutations preserving every cell count.
- Unrestricted circuit size is the MCSP measure; no uniform-only lower bound is being substituted.

## Equations

- profile_form: `A_m(T)=Q_m\left((a_i)_{i=1}^{B_m}\right),\quad a_i=|\{x\in C_i:T(x)=1\}|`. Valid when: Valid when acceptance is exactly a function of the cell one-count vector and not of circuit-sensitive labels inside cells.
- canonical_filler: `G_T(x)=1\iff \exists i\,[x\in C_i\wedge \operatorname{rank}_{C_i}(x)<a_i]`. Valid when: Applies when every cell has uniform rank comparison and the profile counts are hardwired into the nonuniform circuit.
- canonical_circuit_bound: `\operatorname{size}(G_T)\le O(B_m R_m m^{O(1)})\le 2^{(\beta+\eta+o(1))m}`. Valid when: Requires a rankable partition with at most 2^{beta m} cells and per-cell rank circuits of size 2^{eta m+o(m)}.
- threshold_failure: `\beta+\eta<\epsilon\quad\Rightarrow\quad \operatorname{MCSP}(G_T)<2^{\epsilon m}\ \text{for large }m`. Valid when: Requires exponential separation between the rankable profile description cost and the claimed MCSP no-side threshold.
- conditional_extraction_window: `\delta<\epsilon/(\kappa(1+D))`. Valid when: Applies only after source soundness survives the profile falsifier and the low-image carrier is kappa-dense and E-canonical.

## Attempted Derivation

- Assume a nonempty accepted table T for a profile-invariant source A_m.
- Record the vector a_i of one-counts of T inside each cell C_i of Pi_m.
- Construct G_T by placing the a_i ones at the lexicographically first positions of each cell.
- G_T has the same profile as T, hence A_m(G_T)=1.
- Implement G_T by an OR over cells of membership(C_i) and rank_C_i(x)<a_i; hardwire all a_i.
- The circuit size is O(B_m R_m m^{O(1)}), hence below 2^{epsilon m} when beta+eta<epsilon.
- Therefore A_m cannot be a universal no-side MCSP carrier at threshold 2^{epsilon m}.

Blocking gap: The argument does not touch predicates using unrankable global structure or genuinely circuit-sensitive information that does not factor through a subthreshold profile.

## Falsifiers

- falsifier: the source predicate depends only on Hamming weight, bias, balance, or positive/negative load.
- falsifier: the source factors through a rankable partition profile with beta+eta<epsilon.
- falsifier: the verifier's partition has subthreshold rank/select circuits, making canonical fillers small.
- falsifier: the claimed invariant is only uniform-hard; MCSP soundness needs unrestricted nonuniform circuit hardness.
- falsifier: bounded-D image entropy is bought by a profile quotient whose canonical representatives have small circuits.
- falsifier: nonuniform advice chooses source lengths or hard rows, invalidating the E-uniform target transfer.

## Learning

Cycle 45 turns the vague warning that balance is insufficient into a quantitative no-go: any nonempty MCSP source factoring through a subthreshold rankable profile accepts a canonical low-complexity filler. The next viable source must be non-natural, advice-free, low-D, cap-compatible, and genuinely circuit-sensitive rather than a load or bucket-count invariant.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for proposed balance-based and bucket-profile MCSP sources.`
- Rationale: The branch already has a valid carrier-to-E bridge; the bottleneck is source soundness. A concrete profile experiment tests whether balanced-heavy repairs secretly canonicalize to small circuits.
- Situation seed: Partition {0,1}^m into B=2^{beta m} buckets by the first beta m input bits. Let the MCSP certificate predicate accept exactly those truth tables whose per-bucket one-counts lie in a promised balanced interval, while keeping the carrier threshold s=2^{epsilon m}.
- Varied variable: beta, the bucket-count exponent in the rankable profile partition.
- Held-fixed controls: MCSP threshold s=2^{epsilon m} for fixed epsilon>0., Unrestricted nonuniform circuit size is the hardness measure., No advice and E-uniform description of the verifier and partition., Existing extraction target delta<epsilon/(kappa(1+D)) is not changed., Accepted image entropy D is treated as bounded independently of beta.
- Expected observation: For beta<epsilon, the lexicographic per-bucket filler satisfies the same bucket balances and has size about 2^{beta m}poly(m), so the source is invalid. Only beta>=epsilon escapes this falsifier, but then the profile itself reaches the hardness threshold and gives no cheap low-entropy carrier.
- Transfer certificate needed: A formal rank/select circuit bound for the buckets and a proof that acceptance depends solely on the bucket profile; without that certificate the intuition cannot alter the proof queue.

## Next Experiment

Test algebraic global invariants such as low-degree extension consistency or error-correcting-code syndrome plus nonlinear checks against the profile-filler lemma: identify whether their acceptance reduces to rankable profiles or whether they contain a genuine circuit-sensitive obstruction.
