# cycle-0024

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: hitting-cover gate for generated-OR carriers

## Candidate Lemma

For a polylog-query generated-OR carrier, any small nonuniform positive hitting cover or negative product cover gives an explicit subthreshold circuit for H_N^G. Thus a valid N^{1+epsilon} source lower bound must first prove a hitting-cover lower bound, not merely range-label balance.

## Definitions

- source object: H_N^G:{0,1}^N -> {0,1}, H_N^G(x)=OR_{j<=M} SAT(G_{N,j}(x)), where G_N is an explicit multi-output circuit producing M=N^q formulas of length L=(log N)^d.
- target object: SAT_L nonuniform circuits, with target consequence SAT notin SIZE(n^c) for every fixed c if the source lower bound holds on the same infinite length set.
- controlled interface: a target circuit for SAT_L is substituted only at the M generated positions; generator cost is charged once as size N^rho, and no advice about SAT labels on the generated range is hidden.
- target-preserving condition: L=(log N)^d with d>1 and max{rho,q}<1+epsilon, so every fixed SAT exponent contributes only N^{q+o(1)} below the source threshold.
- Positive cover K^+=(K_j^+) has K_j^+ subset SAT cap R_j and hits every positive input: H_N^G(x)=1 implies exists j with G_{N,j}(x) in K_j^+.
- Negative cover K^-=(K_j^-) has K_j^- subset UNSAT cap R_j and covers every query on every negative input: H_N^G(x)=0 implies for all j, G_{N,j}(x) in K_j^-.
- kappa^+ is the minimum of sum_j |K_j^+| over positive covers; kappa^- is the analogous minimum for negative covers; kappa=min{kappa^+,kappa^-}.

## Assumptions

- Circuit model is nonuniform fan-in-two Boolean SIZE with constants; multi-output wires of G_N may be shared by all downstream tests.
- G_N has size O(N^rho), M=N^q, L=(log N)^d, and q,rho,d are fixed constants independent of N.
- The asserted source lower bound is C(H_N^G)>N^{1+epsilon} in the same unrestricted nonuniform model.
- Covers are allowed to be fully nonuniform and length-dependent, so this gate directly audits nonuniform leakage.
- The target bridge is only route-level: it implies SAT lower bounds if the source lower bound is proved; it is not a proof of P != NP.

## Equations

- generated_or_definition: `H_N^G(x)=\bigvee_{j=1}^{M} SAT(G_{N,j}(x)),\quad M=N^q,\quad L=(\log N)^d`. Valid when: Valid when G_N is a shared multi-output generator and each output string encodes a SAT instance of length L.
- target_substitution_upper_bound: `SAT\in SIZE(n^c)\Rightarrow C(H_N^G)\le O(N^\rho+M L^c+M)=N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies after the reduction preserves nonuniform size accounting and the query length is polylogarithmic in N.
- hitting_cover_upper_bound: `C(H_N^G)\le O(N^\rho+M+L\cdot \min\{\kappa^+_N,\kappa^-_N\})`. Valid when: Valid when the selected covers are exact on positive or negative fibers and membership is tested by equality circuits.
- necessary_cover_threshold: `C(H_N^G)>N^{1+\epsilon}\Rightarrow \min\{\kappa^+_N,\kappa^-_N\}>\Omega((N^{1+\epsilon}-N^\rho-M)/L)=N^{1+\epsilon-o(1)}`. Valid when: Requires rho and q to stay below 1+epsilon so generator and OR costs do not already meet the threshold.

## Attempted Derivation

- Defined positive hitting covers and negative product covers on the actual generated SAT ranges R_j.
- Built a circuit by first computing the shared generator G_N, then testing each output against the selected nonuniform label sets with equality ORs of cost O(L|K_j|).
- For a positive cover, correctness follows because negative inputs generate only unsatisfiable formulas, while every positive input is hit by some selected satisfiable formula.
- For a negative cover, the AND of unsatisfiable-membership tests computes the complement of H_N^G exactly, because every positive input has at least one satisfiable query outside every K_j^-.
- Combined the cover circuit with the existing SAT-substitution upper bound to isolate two independent gates: target transfer max{rho,q}<1+epsilon and source cover hardness kappa>N^{1+epsilon-o(1)}.
- Tried to derive kappa lower bounds from cycle-23 label balance, but a planted-template plus decoy construction separates label balance from hitting-cover size.

Blocking gap: No current argument lower-bounds the exact hitting-cover parameter kappa for an explicit target-clean generator; raw semantic range size, variable entropy, and label balance all allow small-cover falsifiers.

## Falsifiers

- hitting-cover collapse: kappa_N <= N^{1+epsilon-o(1)}/L gives a direct subthreshold circuit for H_N^G
- planted satisfiable template: every positive input emits one of few canonical SAT formulas despite large decoy ranges
- negative product cover: all negative inputs use a small per-position family of unsatisfiable formulas
- semantic block-cover compression from earlier cycles can dominate singleton cover counts
- nonuniform leakage through length-dependent equality tables for selected generated labels
- model mismatch if G_N must be replicated M times rather than charged once as a shared multi-output circuit
- target threshold collapse if max{rho,q} >= 1+epsilon, independent of cover size

## Learning

Cycle 24 sharpens the generated-OR route from label balance to exact hitting-cover hardness. The valid target bridge is unchanged, but the source lower bound must now defeat nonuniform covers of positive fibers and negative product fibers of total size N^{1+epsilon-o(1)}. This gives a new concrete falsifier and shows that high semantic range entropy alone cannot justify the carrier.

## Gedanken Experiment Design Seed

- Need decision: `design now`
- Rationale: Cycle-23 range-label balance may be a false comfort: a concrete decoy-rich carrier can satisfy balance while remaining easy through a small nonuniform hitting cover.
- Situation seed: Planted-template generated-OR carrier with M=N^q SAT queries of length L=(log N)^d: positive inputs always emit one of h canonical satisfiable formulas at some position, while all positions also range over many satisfiable and unsatisfiable decoy formulas.
- Varied variable: theta in h=N^theta, the total size exponent of the positive hitting-cover family.
- Held-fixed controls: L=(log N)^d with fixed d>1, so exhaustive SAT lookup is superpolynomial in N^0 but target substitution remains N^{o(1)} per query., M=N^q and generator size N^rho with max{q,rho}<1+epsilon, preserving the target bridge., The source model remains unrestricted nonuniform SIZE on N input bits., Decoy range counts are kept above the cycle-23 label-balance threshold to isolate the new cover parameter.
- Expected observation: As theta crosses 1+epsilon, the equality-cover upper bound crosses the claimed source threshold while the SAT-substitution target transfer is unchanged. If theta<1+epsilon, the carrier is killed by a valid falsifier even with high range-label balance.
- Transfer certificate needed: Before this intuition can affect proof obligations, one needs a formal lower bound kappa_N>N^{1+epsilon-o(1)} against positive hitting covers, negative product covers, and semantic block covers for the actual explicit generator.

## Next Experiment

Formalize the minimum cover parameter as a bipartite set-cover problem between input fibers and generated SAT labels; test whether known disperser/extractor-style generators can force kappa_N>N^{1+epsilon-o(1)} without reintroducing nonuniform leakage.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Log-threshold Walsh-energy separators are natural-proof objects. Let N=2^n, let Gamma_n be a nonempty explicitly enumerable set of Walsh characters, and let lambda_n <= a log N. If a route proves E_Gamma(tt(SAT_n)) >= lambda_n while E_Gamma(tt(C)) < lambda_n for every C in SIZE(n^k), then P_{Gamma,lambda}={f:E_Gamma(f)>=lambda} is N^{O(1)}-constructive, N^{-O(a)}-dense, and useful against SIZE(n^k). Thus this route is inside the natural-proof barrier unless it raises the threshold, loses constructivity, or weakens usefulness.

## Definitions

- source object: explicit Walsh-energy lower-bound certificate (Gamma_n,lambda_n) for the SAT_n truth table, where Gamma_n subset {0,1}^n and lambda_n <= a log N.
- target object: a Razborov-Rudich natural property P_{Gamma,lambda} on N=2^n bit truth tables useful against nonuniform SIZE(n^k).
- controlled interface: compute selected Walsh coefficients from the full truth table and transfer the same threshold inequality to all target circuit truth tables.
- target-preserving condition: Gamma_n is uniformly enumerable in N^{O(1)} time, |Gamma_n|<=N^{O(1)}, lambda_n<=a log N, and usefulness quantifies over every SIZE(n^k) circuit without advice leakage.

## Assumptions

- Truth tables use the +/-1 encoding f:{0,1}^n->{-1,1}.
- SAT_n is a fixed padded complete-language slice, so the target circuit lower bound is SIZE(n^k) on n input bits.
- The proposed separator has a strict usefulness gap: SAT_n is accepted and every target circuit truth table is rejected.
- Natural-proof constructivity is measured in time polynomial in N, not polynomial in n.

## Equations

- walsh_energy: `\(X_\gamma(f)=N^{-1/2}\sum_{x\in\{0,1\}^n} f(x)(-1)^{\gamma\cdot x},\quad E_\Gamma(f)=\sum_{\gamma\in\Gamma}X_\gamma(f)^2.\)`. Valid when: Valid when f is a full +/-1 truth table on n input bits and Gamma is a set of distinct Walsh characters.
- polynomial_density_from_one_mode: `\(\mu(P_{\Gamma,\lambda})\ge \Pr\left[\left|N^{-1/2}\sum_{i=1}^{N}\varepsilon_i\right|\ge \sqrt{\lambda}\right]\ge \exp(-O(\lambda))/\sqrt{\lambda}\ge N^{-O(a)}.\)`. Valid when: Valid when 1<=lambda<=a log N and standard moderate-deviation lower bounds for Rademacher sums apply.
- constructivity_bound: `\(T(P_{\Gamma,\lambda})\le N|\Gamma|\operatorname{polylog}N+T_{enum}(\Gamma)\le N^{O(1)}.\)`. Valid when: Valid when Gamma is uniformly enumerable with polynomially many characters and the threshold has polynomially bounded precision.
- usefulness_transfer: `\(tt(SAT_n)\in P_{\Gamma,\lambda}\ \wedge\ \forall C\in SIZE(n^k),\ tt(C)\notin P_{\Gamma,\lambda}\ \Rightarrow\ P_{\Gamma,\lambda}\text{ is useful against }SIZE(n^k).\)`. Valid when: Valid when the target circuit class is exactly the class quantified in the proposed lower-bound separation.

## Attempted Derivation

- Fix any gamma in Gamma. For uniform random f, the random variable X_gamma(f) is exactly N^{-1/2} times a sum of N independent Rademacher signs.
- Since E_Gamma(f) >= X_gamma(f)^2, the event |X_gamma(f)| >= sqrt(lambda) is contained in P_{Gamma,lambda}.
- For lambda <= a log N, moderate-deviation lower bounds give probability exp(-O(lambda))/sqrt(lambda), hence polynomial density in N.
- Direct summation over all selected characters decides P_{Gamma,lambda} in N^{O(1)} time when Gamma is polynomially enumerable.
- The route's claimed energy separation gives usefulness against the named target class SIZE(n^k).
- Therefore a low-threshold spectral-energy proof object is a natural property and is vulnerable to the PRF falsifier at the matching density exponent.

Blocking gap: No gap remains for the stated conditional bridge; the unresolved mathematical burden is to prove any actual SAT-vs-SIZE(n^k) Walsh-energy separation without falling into this naturalized regime.

## Falsifiers

- A pseudorandom function family in SIZE(n^k) secure against N^{O(1)} full-truth-table distinguishers with advantage N^{-O(a)} is a direct falsifier for any claimed low-threshold Walsh-energy separator.
- A separator with lambda=omega(log N) is a falsifier to the low-threshold naturalization lemma but must then prove nonlarge or nonnatural target preservation separately.
- A nonuniformly chosen Gamma_n encoding SAT_n is a falsifier to constructivity, not a valid escape toward P != NP.
- A proof that rejects only a sampled subclass of SIZE(n^k) circuits falsifies the usefulness transfer and cannot be promoted.

## Learning

Cycle 24 adds a concrete quantitative gate for spectral routes: any explicit Walsh-energy SAT separator using threshold lambda<=O(log N) yields a valid natural property of density N^{-O(1)}. The escape parameter is not spectral language itself, but superlogarithmic energy threshold, nonconstructive character choice, or loss of full usefulness.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and threshold calibration.`
- Rationale: The branch has audited local, affine, halfspace, communication, and low-degree polynomial certificates; spectral-energy certificates are a nearby route object with a computable density threshold not covered by degree alone.
- Situation seed: For padded SAT_n, choose Gamma_n as the first t lexicographic Walsh characters and test the property P_beta={f:E_Gamma(f)>=beta log N} against truth tables of SIZE(n^k) circuits and against random truth tables.
- Varied variable: beta, the coefficient in the energy threshold lambda=beta log N.
- Held-fixed controls: Target class remains nonuniform SIZE(n^k) on n-bit inputs., Gamma_n is uniformly enumerable in N^{O(1)} time and has polynomial size., The property receives the full N-bit truth table, so constructivity is measured in poly(N)., Usefulness must reject every target circuit truth table, with no advice leakage or promise restriction.
- Expected observation: For constant beta, random acceptance remains N^{-Theta(beta)} and the route naturalizes; only beta growing with N can plausibly leave the largeness regime, at the cost of demanding a much stronger SAT spectral-energy gap.
- Transfer certificate needed: A moderate-deviation density proof for the chosen Gamma_n plus a uniform proof that the same threshold separates tt(SAT_n) from every SIZE(n^k) circuit; without both, the intuition cannot enter the proof queue.

## Next Experiment

Audit superlogarithmic Walsh-energy thresholds: determine whether lambda=(log N)^{1+epsilon} can still be polynomial-density through multi-mode chi-square tails for t=polylog N, or whether it genuinely exits the natural-proof largeness window.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Existential hard accepted MCSP certificates transfer without a selector by multiplexing the certificate index into the target truth table. If certificates have length at most c m and hard accepted witnesses occur on kappa-dense source lengths with threshold 2^{epsilon m}, then the resulting E language has circuit lower bound exponent every delta < epsilon/(kappa(1+c)).

## Definitions

- source object: a uniform certificate/emitter family V_m with p in {0,1}^{ell_m}, ell_m <= c m, each accepted p emitting a table T_{m,p}:{0,1}^m -> {0,1}, and for kappa-dense m at least one accepted p satisfying C(T_{m,p}) > 2^{epsilon m}.
- target object: an E-uniform language L whose n-bit slices have Boolean circuit complexity greater than 2^{delta n} for every fixed delta < epsilon/(kappa(1+c)), after standard padding between source lengths.
- controlled interface: replace selector choice by the multiplexer F_m(p,x)=1[V_m accepts p] T_{m,p}(x), using p as extra input bits and x as the original truth-table address.
- target-preserving condition: c,kappa,epsilon are constants, the source schedule is E-decidable, verification/emission is uniform and advice-free, and the lower-bound model is ordinary Boolean circuits with constants.

## Assumptions

- Certificate length ell_m is padded to exactly ceil(c m) if needed, so the multiplexed input length is M_m=m+ell_m <= (1+c)m+O(1).
- For every sufficiently large source length in a kappa-dense set, at least one accepted certificate emits a function with circuit complexity above 2^{epsilon m}.
- The verifier can decide acceptance and sequentially emit T_{m,p} in time 2^{O(m)} without nonuniform advice.
- Padding from hard lengths to intervening target lengths is uniform and does not use an MCSP oracle.

## Equations

- multiplexed_input_length: `M_m=m+\ell_m\le (1+c)m+O(1)`. Valid when: Valid when certificates are padded to a fixed linear length and emitted tables are functions on m input bits.
- multiplexer_definition: `F_m(p,x)=\mathbf{1}[V_m(p)=1]\cdot T_{m,p}(x)`. Valid when: Applies when acceptance is uniformly decidable before or during the sequential emission of the block indexed by p.
- restriction_lower_bound: `C(F_m)\ge \max_{p:V_m(p)=1} C(T_{m,p})-O(M_m)`. Valid when: Requires ordinary Boolean circuits with constants, since fixing p in a circuit for F_m yields a circuit for T_{m,p}.
- exponent_loss: `C(F_m)>2^{(\epsilon/(1+c)-o(1))M_m}`. Valid when: Valid when c and epsilon are fixed constants and additive O(M_m) losses are negligible compared with 2^{epsilon m}.
- dense_padding_transfer: `\delta<\epsilon/(\kappa(1+c))`. Valid when: Applies after source lengths are kappa-dense and padding transfers each multiplexed hard block to intervening target input lengths uniformly.

## Attempted Derivation

- Start with the weaker source promise rejected in cycle 23: for each good m there exists at least one accepted certificate p* whose emitted table T_{m,p*} has C(T_{m,p*})>2^{epsilon m}; other accepted certificates may be easy.
- Pad all certificates to ell_m <= c m and define F_m(p,x)=1[V_m(p)=1]T_{m,p}(x) on M_m=m+ell_m inputs.
- If F_m had a circuit of size S, hardwiring p=p* gives a circuit for T_{m,p*} of size S+O(M_m); hence S>2^{epsilon m}-O(M_m).
- Rewrite 2^{epsilon m} as 2^{(epsilon/(1+c)-o(1))M_m}. This computes the exact exponent paid for eliminating the selector.
- For kappa-dense source lengths, define L on intervening lengths by padding the last available F_m and ignoring extra input bits; restriction gives all-length exponent delta<epsilon/(kappa(1+c)).
- Uniformity is preserved because evaluating L_n requires deciding the source length, checking V_m(p), and sequentially producing the requested bit in 2^{O(n)} time.

Blocking gap: The derivation still assumes a uniform, sparse, cap-compatible source proving existence of a hard accepted certificate at constant epsilon; constructing that source is the unresolved non-natural lower-bound task.

## Falsifiers

- falsifier: certificate index exponent c_m=ell_m/m is unbounded, making epsilon/(1+c_m)=o(1) and destroying a constant target lower-bound exponent.
- falsifier: hard accepted certificates occur only on lengths with unbounded gaps, so dense padding yields no all-length E lower bound.
- falsifier: the verifier or source schedule uses nonuniform advice to locate or validate p*, breaking the target-preserving E construction.
- falsifier: source soundness threshold epsilon exceeds the block-checkpoint cap alpha_V of the proposed emitter, giving small circuits for the emitted tables.
- falsifier: a salted dense certificate family restores largeness and constructivity, re-entering the natural-proofs obstruction.
- falsifier: the claimed hard witness is hard only against a weaker circuit model than the target lower-bound model, so the restriction inequality is not valid for the desired consequence.

## Learning

Cycle 24 repairs the previous selector obstruction. Existential hard accepted witnesses suffice via certificate-index multiplexing, with exact quantitative loss factor 1+c in the exponent. Easy contamination is a falsifier only for same-length extraction; the remaining hard obstruction is constructing a sparse, non-natural, cap-compatible source with constant epsilon and linear certificate length.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: Cycle 23 treated easy contamination as fatal. A concrete contaminated list tests whether selector soundness is truly necessary or only necessary for same-length extraction.
- Situation seed: For every source length m, let V_m accept 2^{c m} certificates. One hidden certificate p* emits a table H_m with C(H_m)>2^{epsilon m}; every other accepted certificate emits the zero function. The target construction forms F_m(p,x), the certificate-index multiplexer.
- Varied variable: certificate-length exponent c=ell_m/m.
- Held-fixed controls: epsilon is a fixed positive MCSP no-side threshold for H_m., source lengths are kappa-dense with fixed kappa., verification and sequential emission are deterministic, uniform, and advice-free in time 2^{O(m)}., the target lower-bound model is ordinary Boolean circuits with constants.
- Expected observation: The multiplexer remains hard because the p=p* restriction is H_m, while the target exponent decreases from epsilon/kappa to epsilon/(kappa(1+c)). Easy contamination is harmless until c grows enough to collapse the exponent.
- Transfer certificate needed: A formal restriction lower-bound proof, an E-uniform padding schedule, and a source-soundness certificate showing existence of p* without natural-proof largeness or nonuniform leakage.

## Next Experiment

Audit candidate source mechanisms for existential hard witnesses under the new multiplexed bridge; compute their c, kappa, epsilon, alpha_V profile, and whether the source proof avoids large constructive hardness recognition.
