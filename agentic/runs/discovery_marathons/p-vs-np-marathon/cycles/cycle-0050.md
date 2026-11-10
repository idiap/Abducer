# cycle-0050

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: Relativizing Extraction Falsified

## Candidate Lemma

For the high-q generated-OR route, no relativizing locality-extraction theorem can convert every small circuit for H_N into a sub-N^{1+epsilon} one-sided separator cover. A structured-slab singleton oracle has C(H_N)=O(N) but requires separator cover size N^{a-o(1)} for any slab exponent a>1+epsilon.

## Definitions

- source object: H_N^A(x)=OR_{j<=N^q} A(G_N(x,j)) on N-bit inputs, with L=(log N)^d, d>1, and a structured slab X_N of N^a inputs.
- target object: a one-sided separator cover over the generated formula range, of total circuit size T<N^{1+epsilon-o(1)}, covering all but E<N^epsilon positive bags.
- controlled interface: a locality-extraction map which, from G_N and a size-S circuit for H_N, outputs such separators while treating SAT labels as a black-box oracle.
- target-preserving condition: keep q,rho<1+epsilon and require the extraction loss below N^{1+epsilon}; otherwise the generated-OR substitution bridge is valid only as a conditional route lemma, not as a source lower-bound certificate.

## Assumptions

- Fix constants epsilon>0, q>0, d>1, and choose a>1+epsilon with a+q=o((log N)^{d-1}) automatically for fixed a,q.
- Let X_N={x in {0,1}^N: all but the first ceil(a log N) bits are 0}, so |X_N|=R=N^{a+o(1)} and membership in X_N has O(N)-size circuits.
- The generator is injective on X_N x [M], M=N^q, into strings of length L; outside X_N all generated labels are negative.
- For each x in X_N, the oracle has exactly one positive generated label G_N(x,f(x)), where f:X_N->[M] is an arbitrary selector.
- Separators are one-sided with respect to the oracle labels: accepting a generated string that is not the selected positive label is invalid.

## Equations

- slab_capacity: `R=|X_N|=N^{a+o(1)},\quad M=N^q,\quad RM=N^{a+q+o(1)}\le 2^L`. Valid when: Valid when d>1 and a,q are fixed constants, so the polylogarithmic formula universe contains the polynomial slab range.
- easy_carrier: `H_N^A(x)=\bigvee_{j\le M}A(G_N(x,j))=\mathbf{1}_{x\in X_N},\quad C(H_N^A)=O(N)`. Valid when: Valid when the oracle plants one positive label in each slab bag and no positive labels outside the slab.
- selector_cover_counting: `T\log T \ge \Omega((R-E)\log M)-O(Rh(E/R))`. Valid when: Valid when a one-sided cover of size T must encode a partial selector agreeing with f on at least R-E slab inputs.
- threshold_contradiction: `E<N^\epsilon,\ a>1+\epsilon\ \Longrightarrow\ T\ge N^{a-o(1)}>N^{1+\epsilon}`. Valid when: Applies when the extraction promises subthreshold separator cost and the slab exponent is chosen above the lower-bound threshold.

## Attempted Derivation

- Replace SAT labels on the generated range by an oracle A while preserving the generated-OR interface H_N^A(x)=OR_j A(G_N(x,j)).
- Choose a structured slab X_N of R=N^{a+o(1)} inputs with O(N)-size membership circuit.
- Use d>1 to inject X_N x [N^q] into the polylogarithmic label universe.
- Plant exactly one positive label per slab bag according to an arbitrary selector f:X_N->[N^q], and plant no positives outside the slab.
- Then H_N^A is exactly the slab membership predicate, so C(H_N^A)=O(N) despite arbitrary hidden choices of f.
- A one-sided separator cover for all but E slab positives determines f on at least R-E inputs; otherwise it either misses the bag or accepts an oracle-negative label.
- Counting covers of total size T gives T log T >= Omega((R-E)log N^q)-O(Rh(E/R)).
- For E<N^epsilon and a>1+epsilon, every valid cover has size N^{a-o(1)}, contradicting any promised sub-N^{1+epsilon} relativizing extraction.

Blocking gap: The argument is an oracle obstruction, not a real-SAT lower bound. Real CNF satisfiability may have nonrelativizing syntactic structure unavailable to singleton oracle labels.

## Falsifiers

- structured-slab singleton oracle falsifier for subthreshold relativizing locality extraction
- threshold collapse if the slab exponent a is not above 1+epsilon
- model mismatch if the extraction treats formula labels as pair-oracle cells rather than real CNF strings
- nonuniform leakage through an explicit selector table when the covered positive slab has size at most N^{1+epsilon-o(1)}
- generator collisions or low semantic range that allow a compact one-sided cover
- neutralization that proves restricted-SAT hardness instead of a barely-superlinear H_N lower bound

## Learning

Cycle 50 gives a precise obstruction: small H_N circuits can coexist with superthreshold one-sided separator complexity in a structured singleton oracle. Thus the extraction bridge must be explicitly nonrelativizing and real-SAT-specific; separator hardness alone is not a valid source lower-bound certificate.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for locality extraction.`
- Rationale: The branch currently depends on converting small arbitrary H_N circuits into local SAT separators. A concrete oracle slab tests whether that conversion is valid or merely a relativizing restatement.
- Situation seed: Polylog injective slab oracle: X_N consists of N^a easy-to-recognize inputs; M=N^q generated queries per input; G_N injects X_N x [M] into length L=(log N)^d strings; the oracle marks exactly one generated string per slab bag positive and none outside, making H_N the O(N)-size slab indicator.
- Varied variable: slab exponent a
- Held-fixed controls: d>1 so the polynomial slab range fits inside the polylogarithmic formula universe, q in the high-q generated-OR window with q<1+epsilon, rho=1 generator/read cost, hence rho<1+epsilon, one-sided separator soundness on the generated range, error budget E<N^epsilon for patchable missed positives
- Expected observation: For a<=1+epsilon the selector can be leaked at or below the source threshold; for a>1+epsilon, H_N remains easy but every one-sided cover for a random selector has size N^{a-o(1)}, so subthreshold relativizing extraction is impossible.
- Transfer certificate needed: A nonrelativizing real-SAT locality-extraction theorem with loss kappa<epsilon-sigma, or a direct lower bound for C(H_N); oracle-valid extraction is formally blocked.

## Next Experiment

Audit real-SAT self-reduction or proof-certificate structure as a possible nonrelativizing extractor, and compute whether its verifier/certificate overhead stays below N^{1+epsilon} rather than collapsing to restricted-SAT hardness.

# Random-Restriction Survival Barrier Gate

## Candidate Lemma

Random-restriction survival is a valid quantitative bridge for width-w DNF/CNF targets at the switching-lemma threshold, but it is not target-preserving for unrestricted SIZE(poly).

## Definitions

- source object: the truth table TT(f_m) of a total Boolean function f_m:{0,1}^m->{0,1}, especially a fixed encoding of SAT_m.
- target object: width-w DNF/CNF formulas on the same m input variables, or one explicitly named bottom layer of AC0 with bottom fan-in w.
- controlled interface: product random restrictions R_p and the survival statistic Sigma_{p,t}(f)=Pr_{rho in R_p}[DT(f|rho)>=t].
- target-preserving condition: the restriction distribution, input length, width bound, and thresholds p,t are identical for the source lower bound and target switching-lemma upper bound; padding or easy branches may not dominate the statistic.
- DT(g) denotes deterministic decision-tree depth of the restricted subfunction g.

## Assumptions

- 0<p<=1/(10w) and t>=1.
- The target computes f_m exactly on the same m-bit input space.
- For AC0 extrapolation, every switching iteration must state fan-in blowup, depth reduction, and residual class; otherwise only the depth-2 conclusion is valid.

## Equations

- survival_profile: `\Sigma_{p,t}(f)=\Pr_{\rho\sim R_p}[DT(f|\rho)\ge t]`. Valid when: Valid when the source function is total and restrictions are sampled independently across the m input coordinates.
- switching_upper_bound: `\Sigma_{p,t}(F)\le (5pw)^t \quad \text{for every width-}w\text{ DNF or CNF }F`. Valid when: Valid when p w is below the switching-lemma constant and F is a width-w DNF or CNF.
- contrapositive_width_lower_bound: `\Sigma_{p,t}(f_m)>(5pw)^t \implies f_m\notin \mathrm{DNF}_w\cup \mathrm{CNF}_w`. Valid when: Applies after the source lower bound and target upper bound use the same p,t,w parameters.
- parity_survival_falsifier: `\Sigma_{p,t}(\mathrm{PARITY}_m)=\Pr[\mathrm{Bin}(m,p)\ge t]`. Valid when: Valid when parity is restricted by R_p because remaining unset variables exactly determine decision-tree depth.

## Attempted Derivation

- Typed the source as TT(f_m), not an arbitrary NP-complete presentation.
- Applied Hastad's switching lemma to width-w DNF/CNF targets under the same R_p distribution.
- Contraposed the switching upper bound to obtain a valid restricted-class lower-bound criterion.
- Tried to replace width-w DNF/CNF by unrestricted SIZE(m^k); no width or switching upper bound survives.
- Computed PARITY_m survival, showing a linear-size P function has maximal survival for many p,t.
- Added the branched SAT/parity carrier to show that NP-completeness itself does not protect the statistic.
- Audited constructivity: exact survival is decidable in poly(N) from the truth table, so a dense useful SIZE property would naturalize.

Blocking gap: There is no target-preserving compiler from P or SIZE(m^k) circuits to bounded-width formulas, nor an iterated AC0 switching certificate with preserved p,t thresholds; the statistic can also be supplied by P-easy ballast.

## Falsifiers

- PARITY_m has size O(m) and Sigma_{p,t}(PARITY_m)=Pr[Bin(m,p)>=t], falsifying unrestricted SIZE transfer.
- The branched carrier L_{m,r}(b,x,y)=SAT_m(x) on b=0 and PARITY_r(y) on b=1 is NP-complete but can have high survival from the easy parity branch.
- When p w exceeds the switching-lemma constant, the bound (5pw)^t is useless or above one, causing quantitative threshold collapse.
- A survival predicate that is dense, useful against SIZE(poly), and computed from the full truth table is a natural-proof object, not a valid barrier escape.

## Learning

Cycle 50 isolates a valid random-restriction bridge: Sigma_{p,t}(f)>(5pw)^t separates f from width-w DNF/CNF at the named switching threshold. The same statistic is poly(N)-constructive and fails for unrestricted SIZE because parity and parity-branched SAT are concrete falsifier objects. This is route-level barrier progress, not progress on P != NP.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The route tests whether random-restriction survival can transfer from an NP-complete source to circuit lower bounds; easy high-survival P functions threaten target preservation.
- Situation seed: Use the padded branched language L_{m,r}(b,x,y)=SAT_m(x) if b=0 and PARITY_r(y) if b=1, with SAT reducing to the b=0 branch.
- Varied variable: The parity ballast exponent beta in r=m^beta.
- Held-fixed controls: Fixed canonical SAT core length m and reduction phi -> (0,phi,0^r)., Fixed product restriction distribution R_p on all coordinates., Fixed survival threshold t=Theta(p r) for the full input., Fixed valid target bridge as width-w DNF/CNF with p w below the switching threshold.
- Expected observation: As beta grows, Sigma_{p,t}(L_{m,r}) becomes large because restrictions often expose a hard parity subfunction, even if the SAT branch contributes no survival lower bound.
- Transfer certificate needed: A proof must condition the statistic on the SAT branch or define a reduction-invariant statistic excluding P-easy ballast, and it must also provide a valid compiler from the named circuit target to bounded-width or iterated switching thresholds.

## Next Experiment

Compute iterated switching parameters for depth-d AC0 of size m^k with bottom fan-in w=m^a, and test whether the required SAT-slice survival lower bound remains below the parity-ballast and naturalness obstruction thresholds.

# MCSP / Meta-Complexity Carrier Transfer, cycle 50: rank-successor leakage

## Candidate Lemma

A low-D MCSP carrier generated from an easy seed by a rank-successor path with subthreshold sparse edits cannot be a valid no-side carrier. For unrestricted circuits, all prior edits to a fixed row can be hardwired, giving size exponent at most max(a,D+u). Thus a valid threshold 2^{epsilon m} source must have a hard seed or rank jumps of exponent at least epsilon-D-o(1).

## Definitions

- source object: a bounded distinct-image MCSP carrier {T_{m,r}:0<=r<R_m} of truth tables of m-bit Boolean functions, with R_m<=2^{D m+O(1)}.
- target object: unrestricted circuit lower bounds C(T_{m,r})>2^{epsilon m} feeding the existing E-extraction bridge with exponent loss D and padding kappa.
- controlled interface: an E-uniform sequential enumeration equipped with adjacent update sets Delta_{m,r}={x:T_{m,r+1}(x) != T_{m,r}(x)} or an equivalent edit transcript.
- target-preserving condition: every emitted row used as an MCSP no-instance must remain hard for unrestricted nonuniform circuits; advice, local decoding, or hardwired sparse edit histories below threshold are invalid.
- seed exponent a is defined by C(T_{m,0})<=2^{a m+o(m)}.
- update exponent u is defined by |Delta_{m,r}|<=2^{u m+o(m)} for all adjacent ranks in the exposed order.

## Assumptions

- Rows have length N=2^m and are interpreted as truth tables of m-input Boolean functions.
- The rank order starts at a row with unrestricted circuit size at most 2^{a m+o(m)}; typical iterative repair starts from zero, parity, or another easy table.
- For every r<R_m-1, the adjacent difference set has size at most 2^{u m+o(m)}; the circuit upper bound may hardwire all update locations for the fixed target row.
- There is constant slack eta>0 with max(a,D+u)<=epsilon-eta if the source is claimed to beat threshold 2^{epsilon m}.
- The argument is nonuniform and therefore applies to the MCSP target model; it does not assume the update transcript is efficiently rankable.

## Equations

- image-entropy-bound: `R_m \le 2^{D m+O(1)}`. Valid when: Valid when the carrier image is counted after canonical duplicate quotienting at each source length.
- successor-update-bound: `|\Delta_{m,r}|=|\{x:T_{m,r+1}(x)\ne T_{m,r}(x)\}| \le 2^{u m+o(m)}`. Valid when: Valid when the proposed selector exposes a rank order with uniformly sparse adjacent edits.
- hardwired-path-upper-bound: `C(T_{m,r}) \le C(T_{m,0})+O(r\,2^{u m+o(m)}m) \le 2^{\max\{a,D+u\}m+o(m)}`. Valid when: Applies when circuits are unrestricted and update locations for one fixed row may be nonuniformly hardwired.
- soundness-necessary-condition: `\max\{a,D+u\} \ge \epsilon-o(1)`. Valid when: Requires all emitted rows to be valid MCSP no-instances at threshold 2^{epsilon m} with polynomial factors absorbed.
- unchanged-extraction-if-source-survives: `\delta < \epsilon/(\kappa(1+D))`. Valid when: Applies after the source survives leakage tests and the kappa-dense distinct-image unranking is E-uniform.

## Attempted Derivation

- Fix m and a row T_{m,r} in a bounded-image carrier with R_m<=2^{D m+O(1)}.
- Write T_{m,r} as T_{m,0} plus the cumulative adjacent edits Delta_{m,0},...,Delta_{m,r-1}.
- For the fixed row, build a nonuniform circuit: compute the easy seed circuit, then test input x against every edited address in the cumulative transcript and override or xor according to the final parity/value.
- The number of hardwired address tests is at most r 2^{u m+o(m)} <= 2^{(D+u)m+o(m)}, and each equality test costs O(m).
- Therefore every row on such a path has unrestricted circuit size at most 2^{max(a,D+u)m+o(m)}.
- If max(a,D+u)<epsilon, the claimed MCSP no-side threshold 2^{epsilon m} is contradicted; this is a valid route-specific falsifier.

Blocking gap: The derivation only rules out smooth-update or iterative-repair selectors. A fully decoder-hard sequential selector with large adjacent jumps and no easy seed is not refuted.

## Falsifiers

- rank-successor sparse-update path from an easy seed with D+u<epsilon
- iterative bad-ball repair using fewer than 2^{epsilon m-o(m)} total hardwirable edits
- indexed interval decoder with alpha_int<epsilon from cycle 49
- subthreshold local or block-restart access to row bits
- accepted row within O(2^{epsilon m}/m) sparse correction distance of a small circuit
- nonuniform length selector or advice selecting hard rows
- lex-first dense outside-U repair that creates a large constructive property
- aggregate row-forcing below q_force=(D+epsilon)/(1+D)

## Learning

Cycle 50 adds a new quantitative leakage obstruction: low-D plus smooth rank traversal is itself a circuit upper bound. Random robust carriers can be combinatorially far from all small circuits, but an explicit iterative repair path with fewer than 2^{epsilon m} cumulative hardwirable edits destroys MCSP soundness. The surviving source must be non-natural, no-advice, low-D, cap-compatible, interval-hard, and now rank-jump-hard. This is valid route-level progress only, not progress on the main P != NP conjecture.

## Gedanken Experiment Design Seed

- Need decision: `design-now-as-falsifier-probe`
- Rationale: The route is blocked not by random existence but by explicit selector leakage. A concrete sparse-repair experiment tests whether a plausible derandomization of the robust carrier immediately yields small nonuniform circuits.
- Situation seed: At length m, start with the zero truth table and try to enumerate R_m=2^{D m} candidate MCSP rows by repairing one row at a time away from all circuits of size below 2^{epsilon m}; each repair step flips a bounded set of truth-table positions while preserving the low-D image budget.
- Varied variable: update exponent u, where each adjacent repair flips at most 2^{u m} positions.
- Held-fixed controls: MCSP no-side threshold remains 2^{epsilon m} for unrestricted circuits., Distinct-image entropy D and padding density kappa are fixed., The selector is E-uniform and uses no advice., Rows are eventually fed only through the existing extraction bridge delta<epsilon/(kappa(1+D)).
- Expected observation: When D+u<epsilon, every repaired row has a hardwired edit-list circuit below the MCSP threshold, so the construction is invalid. Only a jump regime u>=epsilon-D or a hard nonuniform seed can survive this falsifier.
- Transfer certificate needed: Before this intuition may affect proof obligations, provide a formal transcript-to-circuit upper bound for the proposed repair model or prove that the source has no exposed sparse rank-successor transcript.

## Next Experiment

Audit candidate sequential selectors based on pseudorandom walks or iterative hitting-set repairs: compute their adjacent Hamming update exponent u and test the sharp inequality D+u>=epsilon.
