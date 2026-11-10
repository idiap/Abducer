# cycle-0018

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: positioned entropy cover gate

## Candidate Lemma

For a generated-OR carrier, small positioned effective range gives an explicit nonuniform circuit upper bound. Hence an N^{1+epsilon} source lower bound is valid only if the positioned entropy term reaches the same threshold after charging generator and OR costs.

## Definitions

- source object: H_N on N input bits, H_N(x)=OR over M_N=N^{q+o(1)} SAT queries y_i(x)=Gamma_{N,i}(x) of length L_N=(log N)^d and variable count v_i.
- target object: SAT notin P/poly, obtained only by substituting hypothetical SAT circuits into all generated queries and contradicting a source lower bound for H_N.
- controlled interface: a batched generator Gamma_N of circuit size N^{rho+o(1)} exposes all query positions, with no uncharged advice and with per-position ranges R_i={Gamma_{N,i}(x):x in {0,1}^N}.
- target-preserving condition: max{rho,q}<1+epsilon, L_N=(log N)^d with d>1, and every fixed SAT exponent c contributes only L_N^c=N^{o(1)} to the carrier circuit.

## Assumptions

- Circuit size means nonuniform Boolean circuit size over a fixed finite fan-in basis; polylogarithmic factors are absorbed into N^{o(1)}.
- For each position i, formulas in R_i use at most v_i Boolean variables; a circuit may either table SAT on R_i or brute-force all 2^{v_i} assignments.
- The source lower bound C(H_N)>N^{1+epsilon} is interpreted on the same valid length set as the generator family, either eventually or i.o. with matching quantifiers.

## Equations

- carrier_definition: `H_N(x)=\bigvee_{i=1}^{M_N} SAT(\Gamma_{N,i}(x)),\quad M_N=N^{q+o(1)},\quad L_N=(\log N)^d`. Valid when: Valid when the batched generator exposes all query positions and the SAT predicate is evaluated only on formulas of length L_N.
- positioned_effective_entropy: `B_N=\sum_{i=1}^{M_N}\min\{|R_i|,2^{v_i}\},\quad \theta_N=\log_N B_N`. Valid when: Valid when each position has its own range dictionary and variable bound, so ranges from different positions are not merged for free.
- cover_upper_bound: `C(H_N)\le N^{\rho+o(1)}+N^{q+o(1)}+B_N\cdot L_N^{O(1)}`. Valid when: Applies when nonuniform circuits may hardwire per-position dictionaries or instead brute-force all variables of each produced formula.
- entropy_gate_contrapositive: `C(H_N)>N^{1+\epsilon}\ \wedge\ \max\{\rho,q\}<1+\epsilon\ \Rightarrow\ \theta_N\ge 1+\epsilon-o(1)`. Valid when: Requires the source lower bound, generator-size accounting, and positioned cover upper bound to hold on the same valid lengths.

## Attempted Derivation

- Fix N and position i; let R_i be the set of formulas reachable as x varies.
- For this position, build a nonuniform evaluator either by hardwiring SAT(y) for every y in R_i and comparing Gamma_{N,i}(x) to the dictionary, or by brute-force checking all 2^{v_i} assignments of the produced formula.
- The cheaper evaluator costs min{|R_i|,2^{v_i}} L_N^{O(1)} gates, after Gamma_N has produced the query bits.
- Run the batched generator once, evaluate all M_N positioned queries, and OR the M_N answers.
- This gives C(H_N)<=N^{rho+o(1)}+N^{q+o(1)}+B_N L_N^{O(1)}; taking the contrapositive yields the entropy threshold gate.

Blocking gap: The derivation proves only an upper-bound/falsifier lemma. It does not prove C(H_N)>N^{1+epsilon} for any explicit high-entropy carrier.

## Falsifiers

- positioned entropy falsifier: B_N<=N^{1+epsilon-delta} on infinitely many valid lengths gives subthreshold circuits for H_N.
- generator-cost falsifier: charged batched generation size S_charged(Gamma_N)>=N^{1+epsilon-o(1)} destroys the barely-superlinear magnification window.
- target-transfer falsifier: max{rho,q}>=1+epsilon means SAT circuit substitution no longer contradicts the source lower bound.
- variable-count falsifier: if v_i<=alpha log N uniformly and q+alpha<1+epsilon, then B_N<=N^{q+alpha+o(1)} and the source lower bound is impossible.
- natural-proof falsifier: a dense P/poly-constructive property proving the H_N lower bound is blocked under standard PRF assumptions, unless the certificate is non-natural or sufficiently sparse.

## Learning

Cycle 18 proves the exact positioned entropy cover upper bound. The route now has two independent gates: target transfer needs max{rho,q}<1+epsilon, while source plausibility needs B_N>=N^{1+epsilon-o(1)} after charging the generator. Low variable count or low positioned range is a concrete falsifier, not a folklore barrier.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch has isolated positioned entropy as the decisive gate; varying one entropy parameter now tests whether the valid target transfer can coexist with source plausibility.
- Situation seed: For N=2^t, choose d>1 and define Gamma_N as a size N^rho batched generator producing M=N^q length t^d 3-CNF formulas. Each position ranges over clauses on the first v=alpha t variables via an explicit affine disperser of x, and H_N is the OR of their SAT values.
- Varied variable: alpha=v/log N, the variable-entropy exponent per positioned query.
- Held-fixed controls: q<1+epsilon and rho<1+epsilon are fixed below threshold., d>1 is fixed so exhaustive truth-table lookup over whole query strings costs N^{omega(1)}., The circuit model is nonuniform general Boolean circuits., The generator is target-clean: no SAT-answer advice or uncharged selector table is allowed.
- Expected observation: When q+alpha<1+epsilon, the per-position brute-force cover gives C(H_N)<N^{1+epsilon} and falsifies the source. When q+alpha>1+epsilon, this falsifier disappears while the SAT-substitution bound remains N^{max{rho,q}+o(1)}.
- Transfer certificate needed: Before intuition affects proof obligations, prove a formal lower bound on B_N for the explicit generator, charge all generator/selector costs, and supply a non-natural lower-bound method for H_N against general circuits.

## Next Experiment

Instantiate the affine-disperser generated-OR family and compute B_N exactly as a function of alpha, q, and clause density; then audit whether any known lower-bound technique for this restricted H_N avoids the natural-proofs density condition.

# Barrier-Aware Lower-Bound Route: Correlation Halfspace Gate

## Candidate Lemma

For fixed k, a SAT correlation-halfspace certificate at threshold theta_m transfers to a Razborov-Rudich natural property useful against SIZE(m^k) exactly while the halfspace has polynomial density. Quantitatively, theta_m=c sqrt(N log N) gives density N^{-c^2/2-o(1)}, while theta_m/sqrt(N log N)->infinity loses largeness. Thus a low-correlation global predicate is a valid natural-proof object; a high-correlation predicate is outside this falsifier only by requiring stronger average-case SAT hardness.

## Definitions

- source object: For m input bits let N=2^m and T_m in {+/-1}^N be the SAT_m truth table; the certificate is P_theta={F:<F,T_m> >= theta_m} plus soundness for SIZE(m^k).
- target object: A Razborov-Rudich natural property over N-bit truth tables, constructible in poly(N), large with density delta_m, useful against m-input circuits of size m^k, and giving a PRF distinguisher of advantage delta_m.
- controlled interface: Use only the same halfspace P_theta; compute T_m by exhaustive SAT in poly(N); transfer completeness, soundness, density, and constructivity without claiming P != NP.
- target-preserving condition: The threshold satisfies 0 <= theta_m < N and soundness quantifies over every nonuniform circuit of size m^k on m inputs, so an exact small SAT circuit would contradict soundness.

## Assumptions

- Boolean functions are represented by +/-1 truth tables of length N=2^m.
- SAT_m is explicit enough that its full truth table is computable in poly(N) time.
- The route proves the uniform family of inequalities <T_C,T_m> < theta_m for every circuit C of size at most m^k.
- The threshold theta_m is the same in the density calculation and in the small-circuit soundness claim.

## Equations

- correlation_threshold_property: `P_{\theta}(F)=1 \iff \langle F,T_m\rangle\ge \theta_m,\quad N=2^m.`. Valid when: Valid when Boolean functions are encoded as +/-1 truth tables and theta_m is below N.
- density_as_rademacher_tail: `\delta_m=\Pr_{F\leftarrow\{\pm1\}^N}[F\in P_{\theta}]=\Pr\left[\sum_{i=1}^{N}R_i\ge \theta_m\right].`. Valid when: Valid when T_m is fixed and F is uniformly random over all N-bit truth tables.
- moderate_deviation_threshold: `\theta_m=c\sqrt{N\log N}\ \Longrightarrow\ \delta_m=N^{-c^2/2-o(1)}.`. Valid when: Applies in the moderate-deviation regime c=O(1) with theta_m=o(N).
- superpolynomial_largeness_loss: `\theta_m/\sqrt{N\log N}\to\infty\ \Longrightarrow\ \delta_m=N^{-\omega(1)}.`. Valid when: Valid when theta_m=o(N) and standard Rademacher tail asymptotics remain applicable.
- usefulness_transfer: `\forall C\in SIZE(m^k),\ \langle T_C,T_m\rangle<\theta_m\quad\Rightarrow\quad P_{\theta}(T_C)=0.`. Valid when: Requires soundness for all nonuniform size m^k circuits at the identical threshold theta_m.
- prf_distinguisher_advantage: `\operatorname{Adv}_{D}(PRF_{m^k})\ge \delta_m,\quad D(F)=1[P_{\theta}(F)].`. Valid when: Applies after PRF truth tables have circuit size at most m^k and the property is poly(N)-constructive.

## Attempted Derivation

- Fix m and N=2^m; encode every m-input Boolean function F as a +/-1 truth table and let T_m be SAT_m.
- Define P_theta by the signed correlation inequality <F,T_m> >= theta_m. Completeness is immediate because <T_m,T_m>=N.
- For random F, the products F_i T_m(i) are independent Rademacher variables, so the density of P_theta is a one-sided Rademacher tail.
- Apply moderate-deviation estimates: theta_m=c sqrt(N log N) yields polynomial density N^{-c^2/2-o(1)}, while theta_m much larger than sqrt(N log N) yields superpolynomially small density.
- Membership in P_theta is decidable in poly(N) by computing the SAT_m truth table by brute force and taking an inner product.
- If the route proves <T_C,T_m><theta_m for every size m^k circuit C, then P_theta rejects all such circuit truth tables and is useful against SIZE(m^k).
- When density is polynomial, the resulting property distinguishes random truth tables from truth tables of size m^k PRFs with advantage delta_m, giving the precise natural-proof obstruction.
- When density is superpolynomially small, the natural-proof transfer is invalid; the escape is real only if the route can prove the stronger average-case correlation lower bound without advice leakage.

Blocking gap: No known method proves the required SAT correlation soundness for theta_m<N against SIZE(m^k). Low theta_m is blocked by the natural-proofs falsifier under standard PRF assumptions; high theta_m avoids largeness but demands a much stronger average-case lower bound.

## Falsifiers

- theta_m=N^{1/2+epsilon} gives a q=1 poly(N)-computable global predicate with density exp(-Omega(N^{2epsilon})); this falsifier shows query count alone is not a naturalization certificate.
- If soundness is only for uniform algorithms, average circuits, or a promise distribution, usefulness against nonuniform SIZE(m^k) is invalid.
- If the route uses a threshold theta_m=O(sqrt(N log N)) and a poly(N)-constructive predicate, standard SIZE(m^k) PRFs with N^{-O(1)} security falsify the route as a natural proof.
- If T_m or the predicate description is supplied by superpolynomial advice rather than computed in poly(N), constructivity and target preservation fail.
- If density is proved for a nearby Hamming ball or a random transcript rather than for the actual SAT accepting set, the transfer certificate is invalid.

## Learning

Cycle 18 isolates a concrete nonlinear global-predicate threshold. A SAT correlation halfspace at theta=c sqrt(N log N) is large with density N^{-c^2/2-o(1)}, constructible in poly(N), and useful if the same threshold rejects all SIZE(m^k) circuits; hence it is a valid natural-proof object and PRF falsifier. Raising theta above sqrt(N log N) destroys largeness, so nonlinearity can escape this barrier only by demanding strong average-case correlation lower bounds. This is route-level progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now_use_as_falsifier_probe`
- Rationale: The branch needs a concrete nonlinear-query threshold, not another statement that natural proofs exist. Correlation halfspaces give an exact density calculation and expose when a global predicate is validly naturalized.
- Situation seed: For each m, take the full SAT_m truth table T_m of length N=2^m. A proposed lower-bound certificate accepts an arbitrary truth table F iff <F,T_m> >= theta_m and claims every m^k-size circuit has smaller correlation with SAT_m.
- Varied variable: The threshold exponent beta in theta_m=N^beta, with the boundary refinement theta_m=c sqrt(N log N).
- Held-fixed controls: Target class is nonuniform SIZE(m^k) on m input bits for fixed k., The property is evaluated from the full truth table and must run in poly(N) time., Completeness is exact for SAT_m and soundness is universal over all circuits in the target class., No nonuniform advice beyond a uniform poly(N)-computable description is allowed.
- Expected observation: For beta<1/2 density is constant, for theta_m=c sqrt(N log N) density is N^{-c^2/2-o(1)}, and for beta>1/2 density is superpolynomially small. Thus low-threshold correlation proofs are natural-proof objects, while high-threshold proofs escape only by proving strong average-case hardness.
- Transfer certificate needed: A formal proof that the same theta_m used in the tail bound also upper-bounds correlation for every SIZE(m^k) circuit, plus a uniform poly(N) construction of T_m and a PRF-security threshold if invoking the barrier.

## Next Experiment

Audit low-degree polynomial threshold predicates P(F)=1[Q(F,T_m)>=theta]: compute anticoncentration/fiber-density thresholds and decide when they reduce to natural properties or genuinely evade largeness.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

A sequential MCSP carrier has a model-sensitive checkpoint cap. If V has checkpoint size S_m<=2^{sigma m+o(m)} and within-block decoder exponent tau_V(lambda), then every accepted emitted truth table has circuit size at most 2^{alpha_V m+o(m)}, where alpha_V=inf_lambda max(1-lambda+sigma,tau_V(lambda)). Thus a claimed no-side threshold 2^{epsilon m} is valid only when epsilon<=alpha_V; epsilon>alpha_V is a falsifier for source soundness.

## Definitions

- source object: a deterministic uniform streaming certificate verifier V(1^m,c) with |c|=O(m), canonical acceptance, and output y_m in {0,1}^{2^m} claimed to be on the no-side of MCSP_{m,2^{epsilon m}}.
- target object: an E-language L whose length-m truth table is the selected accepted y_m on kappa-dense source lengths, intended to yield L notin SIZE(2^{delta n}).
- controlled interface: exhaustive E-time enumeration of O(m)-bit certificates, hardwired checkpoints from the selected transcript, and a named within-block decoder circuit family for V.
- target-preserving condition: the transfer preserves threshold epsilon, density kappa, uniform canonical selection, and excludes advice, hidden randomness, and nonuniform witness-location leakage.

## Assumptions

- Output length is T_m=2^m and the output index is the m-bit input to the extracted Boolean function.
- A checkpoint of the selected transcript, including work state, heads, and certificate position, has bit length S_m<=2^{sigma m+o(m)}.
- For block length 2^{lambda m}, the selected source model admits nonuniform circuits of size 2^{tau_V(lambda)m+o(m)} that compute the requested within-block output bit from a checkpoint and offset.
- The cap is an upper bound on emitted-table circuit complexity; it is not itself a construction of a high-MCSP carrier.

## Equations

- checkpoint_size: `S_m \le 2^{\sigma m+o(m)}`. Valid when: Valid when the whole selected verifier configuration is explicitly bounded in bits.
- block_storage_cost: `B(\lambda)S_m=(2^m/2^{\lambda m})S_m \le 2^{(1-\lambda+\sigma)m+o(m)}`. Valid when: Valid when checkpoints are hardwired at every block boundary of one accepted transcript.
- within_block_decoder: `D_V(\lambda,m) \le 2^{\tau_V(\lambda)m+o(m)}`. Valid when: Valid when the source model supplies the named block-decoding simulation bound.
- checkpoint_cap: `CKT(y_m) \le 2^{\max\{1-\lambda+\sigma,\tau_V(\lambda)\}m+o(m)}`. Valid when: Applies after storage and within-block decoding are combined in one circuit.
- optimized_cap: `\alpha_V=\inf_{0\le\lambda\le 1}\max\{1-\lambda+\sigma,\tau_V(\lambda)\}`. Valid when: Valid when lambda ranges over exponential block lengths inside the truth table.
- soundness_necessary_condition: `\epsilon \le \alpha_V`. Valid when: Requires the MCSP no-side claim to survive the checkpoint upper-bound falsifier.

## Attempted Derivation

- Fix a deterministic canonical accepted transcript producing y_m and partition its 2^m output positions into blocks of length 2^{lambda m}.
- Hardwire the checkpoint configuration at the start of each block; this costs 2^{(1-lambda+sigma)m+o(m)} gates as constants in a nonuniform circuit for y_m.
- On input index i, compute its block and offset, select the hardwired checkpoint, and invoke the source-model block decoder of size 2^{tau_V(lambda)m+o(m)}.
- Optimize over lambda to obtain CKT(y_m)<=2^{alpha_V m+o(m)}.
- Compare the claimed MCSP no-side threshold epsilon with alpha_V; if epsilon exceeds alpha_V, the accepted transcript contradicts its own soundness.
- If the source survives this audit and is kappa-dense with O(m)-bit canonical certificates, apply the existing exhaustive-selection transfer to get E lower bound exponent delta<epsilon/kappa.

Blocking gap: No actual sparse non-natural certificate source with proved soundness and a proved tau_V profile is known. The derivation supplies a valid cap and falsifier, not a carrier construction.

## Falsifiers

- falsifier: epsilon>alpha_V for the declared verifier model, because checkpoint circuits put every accepted table on the MCSP yes-side.
- falsifier: tau_V(lambda) is omitted or borrowed from a stronger local model than the source actually permits.
- falsifier: the carrier is located by nonuniform advice or hidden randomness, yielding at most a nonuniform consequence.
- falsifier: certificate length omega(m) or verifier overhead above 2^{O(m)} breaks the E-time exhaustive selector.
- falsifier: kappa-density is lost, so the lower-bound exponent collapses to o(1) after padding.
- falsifier: a dense constructive accepted set turns the source into a natural-property object rather than a sparse non-natural carrier.

## Learning

Cycle 18 repairs the checkpoint obstruction: the cap is not a universal (1+sigma)/2 statement but alpha_V=inf_lambda max(1-lambda+sigma,tau_V(lambda)). The route gains a valid quantitative falsifier for proposed MCSP sources and a cap-aware E-transfer ceiling delta<epsilon/kappa<=alpha_V/kappa. The remaining hard task is constructing a sparse, canonical, non-natural source with proved soundness and declared tau_V profile.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The branch now hinges on a quantitative source-model distinction: the same checkpoint idea gives different caps depending on the block-decoder exponent tau_V, so an abstract MCSP-carrier restatement would hide the valid threshold.
- Situation seed: Consider a padded family of canonical MCSP carrier verifiers V_sigma that, on O(m)-bit certificates, emits a 2^m-bit truth table in time 2^{O(m)} on kappa-dense lengths; compare a local streaming implementation with a word-RAM implementation having the same checkpoint size 2^{sigma m}.
- Varied variable: the block-simulation exponent tau_V(lambda), with sigma fixed first and then swept from 0 to 1.
- Held-fixed controls: MCSP no-side threshold 2^{epsilon m} is held fixed., Carrier density kappa is held fixed and constant., Certificates remain O(m) bits and canonical., No advice, hidden randomness, random-access selector, or dense natural property is allowed., The target extraction remains the same E-language padding transfer.
- Expected observation: The local model predicts alpha_V=(1+sigma)/2, while full-state simulation predicts a weaker cap such as 1/2+sigma. A claimed source at epsilon above the appropriate alpha_V should be invalid; below it, the checkpoint obstruction disappears but soundness is still unconstructed.
- Transfer certificate needed: A formal block-decoder theorem giving tau_V(lambda) for the named verifier model, plus a uniform canonical-selection proof and a kappa-density certificate before any observation may enter the proof queue.

## Next Experiment

Instantiate tau_V(lambda) for three explicit source models: polyspace streaming, exponential-space local-tape streaming, and word-RAM transcript verification; compute the largest valid epsilon and resulting delta ceiling for each.
