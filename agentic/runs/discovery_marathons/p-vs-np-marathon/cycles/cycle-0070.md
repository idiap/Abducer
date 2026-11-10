# cycle-0070

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For the beta=0 XOR carrier, any label-mediated certificate property Q_N that is complete for SAT labels, sound for the N^{1+epsilon} source lower bound, 2^{O(L)}-constructive, and classically large in label space extends by restriction to a Razborov-Rudich natural property useful against SIZE(L^c) for every fixed c. The exact classical largeness cutoff is delta_N >= 2^{-O(L)}, not merely ambient source-image density.

## Definitions

- source object: H_y on N-bit source inputs is the XOR carrier H_y(x)=xor_{j<=N^q} y_{G_{N,j}(x)}, where y is a label table on the generated formula range U_N subseteq {0,1}^L and G_N has circuit size N^rho.
- target object: SAT_L is the Boolean function on length-L formula encodings, and the target consequence is SAT_L notin SIZE(L^c) for every fixed c along the valid length sequence, hence a route-level NP notsubset P/poly consequence if all lengths are covered.
- controlled interface: beta=0 black-box substitution uses L=(log N)^d with fixed d>=1, substitutes a size L^c circuit for the label oracle y, and pays N^q slot cost plus N^rho generator cost.
- target-preserving condition: max{q,rho}<1+epsilon, U_N is label-free uniformly enumerable within 2^{O(L)}, Q_N soundness is in the same nonuniform Boolean circuit model, and the certificate uses no advice depending on SAT labels beyond the displayed truth table.

## Assumptions

- Circuit model is nonuniform fan-in two Boolean circuits; size floors and poly(L) decoding factors are absorbed into N^{o(1)}.
- Parameters epsilon>0, q, rho, d are fixed before c; c is any fixed target polynomial exponent.
- Q_N subseteq {0,1}^{U_N} has relative density delta_N=|Q_N|/2^{|U_N|}, accepts SAT restricted to U_N, and satisfies Q_N(y)=1 => C_N(H_y)>N^{1+epsilon}.
- Membership in Q_N from the indexed label table y is decidable in time 2^{O(L)} after enumerating U_N; the enumeration is independent of SAT truth values.
- The restriction extension is R_L(f)=1 iff Q_N(f restricted to U_N)=1 for arbitrary Boolean functions f:{0,1}^L -> {0,1}.

## Equations

- substitution_upper_bound: `C_N(H_{f|U_N}) \le N^\rho + N^q\,C_L(f)\operatorname{poly}(L)+N^{o(1)} = N^{\max\{\rho,q\}+o(1)} \quad \text{if } C_L(f)\le L^c.`. Valid when: Valid when L=(log N)^d with fixed d>=1, c is fixed, and the carrier accesses target labels only through the generated slots.
- cylinder_density_preservation: `\Pr_{f:{0,1}^L\to\{0,1\}}[R_L(f)=1]=\frac{|Q_N|}{2^{|U_N|}}=\delta_N.`. Valid when: Valid when R_L depends only on the restriction of the full truth table to the enumerated range U_N.
- constructivity_transfer: `T_R(L) \le T_Q(N)+O(|U_N|\operatorname{poly}(L)) \le 2^{O(L)}.`. Valid when: Valid when |U_N|<=N^q=2^{O(L)} and Q_N is decidable from the restricted label table within 2^{O(L)} time.
- classical_largeness_cutoff: `\delta_N\ge 2^{-O(L)} \Rightarrow R_L \text{ is RR-large};\quad \delta_N=2^{-L^\theta},\ \theta>1 \Rightarrow R_L \text{ is not classically large}.`. Valid when: Applies when naturalness is measured at target input length L with the standard Razborov-Rudich density threshold 2^{-O(L)}.

## Attempted Derivation

- Fix N and L=(log N)^d, d>=1; enumerate U_N label-free and define R_L(f)=Q_N(f|U_N).
- For uniformly random truth table f on {0,1}^L, the restriction f|U_N is uniform over {0,1}^{U_N}; hence density is exactly preserved as delta_N.
- Given a truth table for f, enumerate U_N, read the indexed bits, and run Q_N; the total time is 2^{O(L)} under |U_N|<=N^q.
- If R_L(f)=1 and f had size L^c, substitute that circuit into the XOR carrier to get C_N(H_{f|U_N})<=N^{max{q,rho}+o(1)}<N^{1+epsilon}, contradicting Q_N soundness.
- Since Q_N accepts SAT|U_N, R_L accepts SAT_L; thus any classically large constructive Q_N would naturalize the proof-mediated source lower bound.

Blocking gap: This does not prove that such Q_N exists, and it does not turn sparse or nonconstructive certificates into barriers. It only gives a valid no-go for dense, constructive, same-model label certificates.

## Falsifiers

- falsifier: delta_N>=2^{-O(L)} with T_Q<=2^{O(L)} means the certificate route is a classical natural property, not a valid naturalness escape.
- falsifier: max{q,rho}>=1+epsilon collapses the source threshold before any target lower bound is obtained.
- falsifier: U_N enumeration or Q_N membership uses nonuniform advice encoding SAT labels, breaking the label-free restriction extension.
- falsifier: source soundness proves only local separator hardness or rank hardness, not arbitrary circuit lower bounds for H_y.
- falsifier: d<1 with |U_N|=2^{omega(L)} can destroy 2^{O(L)} constructivity of the cylinder property even when beta remains subpolynomial.

## Learning

Cycle 70 corrects the naturalness gate for the beta=0 XOR route. A dense label certificate cylinder-extends to a valid classical natural property exactly at density 2^{-O(L)} with 2^{O(L)} constructivity; source-image ambient sparsity is irrelevant after restriction. The real escapes are nonlarge density below the classical cutoff, nonconstructivity, advice leakage, or a direct nonrelativizing H_N lower bound.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a finite falsifier probe for proof-mediated XOR certificates.`
- Rationale: The branch already has the beta=0 transfer; the live ambiguity is whether a certificate escapes natural proofs by source-image sparsity or only by genuine nonlargeness, nonconstructivity, advice leakage, or nonrelativizing directness.
- Situation seed: Take a beta=0 XOR carrier with L=(log N)^d, d>=1, q,rho<1+epsilon, and a hypothetical label certificate Q_N of density delta_N=2^{-L^theta} that soundly certifies C_N(H_y)>N^{1+epsilon}.
- Varied variable: theta, the label-density exponent in delta_N=2^{-L^theta}.
- Held-fixed controls: The generated range U_N is uniformly enumerable without SAT-label advice., The source soundness statement is for arbitrary nonuniform circuits computing H_y., The target substitution interface remains beta=0 with max{q,rho}<1+epsilon., The verifier runs in 2^{O(L)} time from the restricted label table.
- Expected observation: For theta<=1 the restriction extension is a classical natural property useful against polynomial-size L-bit circuits; for theta>1 the classical barrier no longer applies, though a stronger delta-natural barrier may still apply if matching PRFs are assumed.
- Transfer certificate needed: A formal restriction-extension certificate: uniform enumeration of U_N, exact density preservation, 2^{O(L)} constructivity, and the substitution contradiction from small f to small H_{f|U_N}.

## Next Experiment

Instantiate the density-tier audit on a toy proof-certificate family: certificates describing affine anti-alignment witnesses over U_N. Compute delta_N, verifier time, and whether soundness reaches arbitrary C_N(H_y)>N^{1+epsilon} or only sketch hardness.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

View-shadow cluster naturalization gate: a proof-mediated local lower-bound verifier yields a valid natural property whenever a uniform logarithmic seed cluster has SAT completeness, logarithmic table/proof footprint, and direct cluster-shadow soundness against the named target circuits.

## Definitions

- source object: an advice-free public-coin local verifier V for the assertion CC(f)>s on truth tables f in {0,1}^N, N=2^m, with seed length ell, q truth-table queries, and t proof-bit queries per seed.
- target object: truth tables of SIZE_m(s) Boolean circuits, mainly s=m^k for fixed k>1, with circuit count M_s at most 2^{O(s log s)}.
- controlled interface: a uniform seed-cluster family C_m of size d and the property P_C(f)=1 iff some assignment to the proof cells touched by C makes every seed in C accept on f.
- target-preserving condition: qd=O(log N), the distinct touched proof cells B_C=O(log N), C_m is computable in poly(N), SAT has an accepting proof on C_m, and no SIZE_m(s) truth table has a consistent accepting local proof assignment on C_m.

## Assumptions

- The verifier is total after fixing a seed, truth-table answers, and local proof answers; adaptivity is unfolded into a finite transcript tree counted in q and t.
- Constructivity is uniform poly(N), not a nonuniform cluster-advice property; otherwise the natural-proof conclusion is weakened to an advice-leakage warning.
- Completeness is only required on the chosen cluster C_m, not on all public coins, so this is a route-level bridge and not a proof of P != NP.
- Direct cluster-shadow soundness means every target truth table g in SIZE_m(s) is rejected for every assignment to the union of proof cells queried by seeds in C_m.

## Equations

- footprints: `Q_C\le dq,\qquad B_C\le dt`. Valid when: Valid when the verifier's adaptive transcripts are unfolded and C is fixed before seeing the candidate truth table.
- density: `\mu(P_C)\ge 2^{-Q_C}\ge N^{-O(1)}`. Valid when: Valid when SAT completeness fixes one accepting proof-view and qd is at most a constant times log N.
- constructivity: `T_{rec}(N)\le 2^{B_C}\operatorname{poly}(N,d,q,t)`. Valid when: Applies when the recognizer enumerates all local proof-cell assignments and B_C is O(log N).
- usefulness: `P_C\cap TT(SIZE_m(s))=\varnothing`. Valid when: Requires direct cluster-shadow soundness for every target circuit truth table in the named size class.

## Attempted Derivation

- Start with a proof-mediated verifier V for CC(TT(SAT_m))>m^k and a candidate accepting seed cluster C of size d.
- Define P_C(f) by existentially assigning only the proof cells touched by C, not the full long proof.
- If SAT has one proof accepting all seeds in C, then all tables matching SAT on the Q_C queried locations are accepted, giving density at least 2^{-Q_C}.
- If B_C=O(log N), P_C is decidable in poly(N) by enumerating the local proof-cell assignments.
- Usefulness is equivalent to direct cluster-shadow soundness: no m^k-size circuit truth table has any consistent accepting local proof assignment on C.
- Trying to replace direct cluster-shadow soundness by ordinary global-proof soundness fails because the accepting local proof assignment may be chosen after seeing C.
- A random-cluster repair needs a shadow cap alpha and yields the threshold log(1/alpha)>=Omega(qm^{k-1} log m) under qd=O(log N).

Blocking gap: No candidate proof system currently supplies the required exponentially small existential-view shadow or a uniform cluster with direct cluster-shadow soundness; ordinary soundness is too weak.

## Falsifiers

- 3-XOR-style locally satisfiable seed constraints give alpha=1 while every fixed global proof has low acceptance, so ordinary soundness is an invalid usefulness certificate.
- A constant shadow cap alpha<1 is still insufficient for SIZE_m(m^k) when qd=O(log N), since the circuit-count union bound needs log(1/alpha)=Omega(qm^{k-1} log m).
- If the seed cluster C_m is selected with nonuniform advice not computable in poly(N), the property may lose valid natural-proof constructivity rather than prove a target lower bound.
- If qd exceeds O(log N), the accepting cylinder has subpolynomial or negligible density and the natural-property falsifier no longer applies.
- If B_C exceeds O(log N) without an efficient structured search over proof views, the recognizer is not poly(N)-constructive.

## Learning

Cycle 70 isolates the existential local-view shadow as the missing parameter for long-proof escape attempts. For SIZE_m(m^k) and natural density qd=O(log N), a union-bound cluster proof needs log(1/alpha)=Omega(qm^{k-1} log m), far stronger than ordinary soundness. The 3-XOR local-satisfiability falsifier shows alpha can be 1 while global proofs are sound. This is valid route-level progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for proof-mediated naturalization routes.`
- Rationale: The branch has narrowed the escape to long proofs with local access; the remaining mathematical question is whether local proof views have small existential shadow or merely ordinary soundness.
- Situation seed: A public-coin verifier whose seed samples r random 3-XOR equations over a large proof alphabet and performs q fixed truth-table checks against a padded easy table g; each seed's local XOR system is satisfiable, but every fixed global proof satisfies only about 2^{-r} of seeds.
- Varied variable: The existential shadow density alpha, controlled by adding consistency checks or increasing r, while keeping qd=O(log N).
- Held-fixed controls: Target class SIZE_m(m^k) and length relation N=2^m., Uniform cluster constructivity requirement for C_m., Logarithmic table footprint qd=O(log N) so largeness remains polynomial., SAT-cluster completeness for the corresponding proof-mediated lower-bound assertion.
- Expected observation: Ordinary soundness delta can be small while alpha remains 1; only when alpha drops below exp(-Omega(qm^{k-1} log m)) can a random logarithmic cluster plausibly reject all m^k-size circuits by the counted transfer.
- Transfer certificate needed: A proof that the actual verifier has direct cluster-shadow soundness, or a uniform cluster plus a bound on cluster-local satisfiability strong enough to beat 2^{O(m^k log m)} target circuits without violating qd=O(log N).

## Next Experiment

Instantiate the shadow audit for one named PCP/IOP-style lower-bound verifier: compute q,t,ell,B_C and prove either alpha=1 via local satisfiability or alpha<=exp(-Omega(qm^{k-1} log m)) via a genuine consistency theorem.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Semantic block-cover gate: if a claimed MCSP-hard carrier row T_m has a block decomposition whose blocks have short summaries and a common small opener, then T_m has a small unrestricted circuit. Hence any source claiming CC(T_m)>2^{theta m} is invalid when the cover exponent is below theta.

## Definitions

- source object: a generated anti-ball MCSP carrier row T_m in {0,1}^{2^m}, intended to be a truth table of an m-bit Boolean function with unrestricted circuit complexity above 2^{theta m}.
- target object: an E language L obtained from canonical row/image multiplexing and kappa-gap padding, intended to inherit SIZE(2^{delta n}) lower bounds from the hard row.
- controlled interface: a semantic block cover with block exponent lambda, summary exponent mu, and opener exponent omega: q=2^{(1-lambda)m} blocks, summaries a_j of length at most 2^{mu m+o(m)}, and one common circuit O_m of size 2^{omega m+o(m)} opening any bit from the selected summary.
- target-preserving condition: the carrier-to-E extraction is valid only for an advice-free canonically located row whose semantic-cover exponent is at least theta-o(1), with image entropy D and kappa-gap padding preserved; a subtheta cover is a nonuniform circuit upper bound and kills the source.

## Assumptions

- Circuit model is unrestricted nonuniform Boolean circuits over m input bits; hardwired block summaries count as circuit constants and gates.
- Blocks are consecutive or uniformly computable from the input index, and the opener receives only the offset and the selected summary, not advice depending on the queried bit.
- The source threshold theta, image entropy D, and padding gap kappa are fixed constants; all o(m) losses are absorbed into exponent slack.
- The argument is a route-level falsifier for MCSP carrier soundness, not a proof of P != NP or a natural-property lower bound.

## Equations

- block_count: `N=2^m,\quad B=2^{\lambda m},\quad q=N/B=2^{(1-\lambda)m}.`. Valid when: Valid when T_m is viewed as a truth table on m variables and the chosen block partition has exponential block length 2^{lambda m}.
- semantic_cover_upper_bound: `CC(T_m)\le O(q\cdot 2^{\mu m+o(m)}+2^{\omega m+o(m)}+\mathrm{poly}(m))\le 2^{\max\{1-\lambda+\mu,\omega\}m+o(m)}.`. Valid when: Valid when all block summaries can be hardwired and one common opener circuit can be shared after multiplexing the selected summary bits.
- falsifier_threshold: `\alpha_{sem}(\lambda,\mu,\omega):=\max\{1-\lambda+\mu,\omega\}<\theta\ \Longrightarrow\ T_m\notin \mathrm{MCSP\text{-}No}(2^{\theta m}).`. Valid when: Valid when the source claim is an unrestricted MCSP no-side claim at threshold 2^{theta m} for the same row T_m.
- surviving_extraction_rate: `\delta<\theta/(\kappa(1+D)).`. Valid when: Applies after the row survives the semantic-cover audit and the canonical multiplexing preserves image entropy D, padding gap kappa, and E-uniform location.

## Attempted Derivation

- Fix a claimed hard row T_m and choose block length B=2^{lambda m}; write the input x as block index j and offset r.
- For each summary coordinate t, build a multiplexer M_t(j) with the t-th bits of all summaries a_j hardwired. The total selector size is O(q|a_j|)=2^{(1-lambda+mu)m+o(m)}.
- Feed the selected summary vector and offset r into one common opener O_m. Circuit sharing avoids copying O_m once per block, so the opener contributes only 2^{omega m+o(m)} gates.
- The resulting circuit computes every bit of T_m and has exponent alpha_sem=max{1-lambda+mu,omega}. If alpha_sem<theta, this contradicts the source's MCSP no-side claim.
- Checkpoint, skip-ahead, block-digest, Merkle-opening, and rankable block-summary implementations instantiate the same cover once their summaries and openers are expressible as nonuniform circuits.
- Trying to promote the route now requires proving that a generated anti-ball row has no semantic cover below theta, not merely that the generator is sequential or noniteratable.

Blocking gap: No non-circular method is known in this branch to certify covdim_m(T)>=theta for an explicit generated anti-ball row against unrestricted semantic covers. Such a certificate appears as strong as the desired MCSP row lower bound unless it is proof-mediated, sparse, and non-natural.

## Falsifiers

- falsifier: a block commitment or proof stream with summaries of exponent mu and common opener exponent omega satisfying max{1-lambda+mu,omega}<theta.
- falsifier: polynomial-space near-linear sequential generation with checkpoint summaries giving the earlier theta>1/2 cap as a special case.
- falsifier: algebraic skip-ahead or iteratable transitions that yield block summaries with subtheta openers even if the full stream looks globally sequential.
- falsifier: dense locator or projection repair that makes a polynomial-time decidable large useful property while preserving small-circuit exclusion.
- falsifier: unbounded distinct-image entropy D, which leaves the source perhaps hard nonuniformly but destroys the stated E-transfer exponent.

## Learning

Cycle 70 compresses several leakage channels into a single semantic block-cover exponent. Any generated MCSP carrier whose row admits short per-block summaries and a shared opener has an unrestricted circuit of exponent alpha_sem=max{1-lambda+mu,omega}. Thus a valid source must prove high semantic covering dimension; sequential, noniteratable, or advice-free generation alone is insufficient.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The branch needs a concrete falsifier probe for generated anti-ball sources: sequentiality and noniterability are too weak unless they exclude semantic block covers in the unrestricted circuit model.
- Situation seed: Take a generated anti-ball MCSP row/proof stream whose proof is organized into block commitments. The row length is N=2^m, the claimed hardness threshold is 2^{theta m}, and each block has a generated certificate opening all bits in that block.
- Varied variable: Vary the block length exponent lambda while measuring the induced summary exponent mu(lambda) and opener exponent omega(lambda).
- Held-fixed controls: Keep the target extraction model fixed: E-uniform canonical row/image multiplexing with image entropy D and padding gap kappa., Keep the source hardness claim fixed: unrestricted MCSP no-side threshold 2^{theta m}, not uniform or restricted-circuit hardness., Keep the source sparse and advice-free so that natural-property largeness and nonuniform row-choice leakage are not introduced.
- Expected observation: Ordinary commitment or checkpoint implementations should show alpha_sem(lambda)=max{1-lambda+mu(lambda),omega(lambda)} dropping below theta for large enough lambda, giving a finite invalidation. A viable source must force either mu(lambda)>=theta+lambda-1 or omega(lambda)>=theta for every lambda.
- Transfer certificate needed: Before the intuition can affect proof obligations, prove a semantic-cover lower bound covdim_m(T)>=theta-o(1) for the selected row and verify that canonical extraction still has delta<theta/(kappa(1+D)) in E.

## Next Experiment

For three candidate generated anti-ball implementations--checkpointed sequential stream, Merkle-style block proof, and noniteratable hash-chain stream--compute mu(lambda), omega(lambda), and min_lambda alpha_sem; quarantine any implementation with min alpha_sem<theta and record the exact valid parameter range.
