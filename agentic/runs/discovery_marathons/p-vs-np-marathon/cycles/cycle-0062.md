# cycle-0062

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Rank-density naturalness fork for the XOR generated-SAT carrier: high F_2 incidence rank makes the property C(H_{N,G,y})>S large over label vectors y. Therefore any poly(2^L)-constructive certificate proving the actual SAT label vector has this property, while rejecting every L^c-size target function through the valid substitution bridge, is a Razborov-Rudich natural property. The route must be non-large, nonconstructive, proof-mediated, or a direct arbitrary-circuit lower bound not mediated by a large semantic property.

## Definitions

- source object: H_{N,G,y}:{0,1}^N->{0,1}, H_{N,G,y}(x)=xor_{j<=N^q} y_{G_N(x,j)}, where y is a label vector on L-bit formula encodings and the actual source instance uses y=SAT_L.
- target object: SAT_L on L=(log N)^d bit encodings, with target consequence SAT notin SIZE(n^c) for every fixed c only after a valid source lower bound against arbitrary circuits is obtained.
- controlled interface: nonadaptive XOR of M=N^q generated SAT queries plus a generator/decoder circuit of size N^rho; target circuits are substituted only at queried formulas.
- target-preserving condition: L=(log N)^d with d>1, q,rho<1+epsilon, no SAT-label advice in G or the certificate, and the source lower bound is against arbitrary nonuniform circuits for the actual SAT label vector.
- incidence matrix: A_N has row a_N(x) in F_2^{U_N}, recording queried formula positions with parity multiplicity; r_N=rank_{F_2}(A_N).
- certificate property: R_N(y)=1 means C(H_{N,G,y})>S or a sound strengthening that implies this lower bound for the carrier.
- naturalness regime: R_N is constructive if decidable in poly(2^L) time from the L-bit truth table, large if its density is at least 2^{-poly(L)}, and useful against SIZE(L^c) if it rejects every truth table computed by L^c-size circuits.

## Assumptions

- Circuit model is nonuniform fan-in-two Boolean circuits; all advice hardwired into G, the carrier, or the certificate is charged to the displayed size bound.
- Regime has fixed epsilon>0, fixed d>1, L=(log N)^d, M=N^q, and fixed target exponent c before letting N grow.
- The generator G_N is label-free: its circuit and transcript depend on formula syntax and the source input, not on SAT labels or on H_N itself.
- The standard circuit counting bound #SIZE(S) <= 2^{K S log S} is used with a universal constant K.
- Natural-proofs obstruction is conditional on polynomial-size pseudorandom functions for the target scale L; without this assumption the lemma is only a barrier-typing certificate.
- Usefulness is transferred through the polylog-query substitution bridge, so q,rho<1+epsilon is required for the lower-bound threshold S=N^{1+epsilon-o(1)}.

## Equations

- xor_carrier_linearization: `H_{N,G,y}(x)=\langle a_N(x),y\rangle_{\mathbb F_2}=\bigoplus_{j=1}^{N^q} y_{G_N(x,j)}`. Valid when: Valid when G_N outputs only L-bit formula encodings and a_N records queried positions with parity multiplicity over F_2.
- polylog_target_substitution: `\mathrm{SAT}_L\in \mathrm{SIZE}(L^c)\Rightarrow C(H_{N,G,\mathrm{SAT}})\le O(N^\rho+N^q L^c\operatorname{polylog}N)=N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies when L=(log N)^d, c is fixed, target circuits are nonuniform, and the generator has size N^rho without SAT-label advice.
- direct_circuit_density_bound: `\Pr_y[C(H_{N,G,y})\le S]\le 2^{K S\log S-r_N}`. Valid when: Valid when y is uniform over L-bit truth tables, r_N is the F_2 rank of the incidence rows, and size-S circuits are counted by 2^{K S log S}.
- largeness_threshold: `r_N\ge K S\log S+L^k\Rightarrow \Pr_y[C(H_{N,G,y})>S]\ge 1-2^{-L^k}`. Valid when: Requires the incidence-rank gap to dominate the circuit-counting entropy and chooses k within the remaining explicit rank margin.
- naturalness_fork: `\mathrm{Constructive}(R_N)\wedge \mathrm{Large}(R_N)\wedge \mathrm{Useful}_{L^c}(R_N)\Rightarrow R_N\text{ is a natural property against }\mathrm{SIZE}(L^c)`. Valid when: Applies when R_N depends only on the L-bit truth table, is decidable in poly(2^L) time, and rejects all L^c-size truth tables.

## Attempted Derivation

- Fix U_N as the L-bit formula universe touched by G_N and write H_{N,G,y}=A_N y over F_2 on the truth-table rows indexed by x in {0,1}^N.
- For any Boolean function h on {0,1}^N, the set of labels y satisfying A_N y=h is empty or an affine subspace of codimension r_N, hence has uniform measure 2^{-r_N}.
- Union-bound over all size-S source circuits h. Using #SIZE(S)<=2^{K S log S} gives Pr_y[C(H_{N,G,y})<=S]<=2^{K S log S-r_N}.
- If r_N exceeds K S log S by L^k, the lower-bound property C(H)>S is overwhelmingly large over L-bit truth tables.
- If SAT_L had L^c-size circuits, the valid polylog substitution gives C(H_{N,G,SAT})<=N^{max{q,rho}+o(1)}, so R_N(y)=C(H_{N,G,y})>N^{1+epsilon-o(1)} rejects every L^c-size truth table when q,rho<1+epsilon.
- Thus a poly(2^L)-constructive verifier accepting the actual SAT truth table and certifying R_N would be a natural property against SIZE(L^c), conditional on the usual PRF barrier assumptions.

Blocking gap: The derivation does not produce the actual source lower bound. It only says that high-rank, efficiently checkable, large certificates are barrier-exposed, while absence of label-free sketches is still not equivalent to arbitrary-circuit hardness without a nonrelativizing extraction theorem.

## Falsifiers

- falsifier: r_N<=O(N^{1+epsilon} log N) gives too little rank for the density-counting route and revives low-rank affine sketch upper bounds.
- falsifier: any transcript or codebook depending on SAT labels, including T_N=H_N, violates label-freeness and collapses the audit into nonuniform leakage.
- falsifier: a poly(2^L)-constructive large certificate for the actual SAT label vector becomes a natural-property route under PRF assumptions, so it is not a valid barrier escape.
- falsifier: if a repaired carrier has target-query length N^beta with beta>0, the q+beta c transfer cap blocks all-exponent SAT lower bounds.
- falsifier: hidden advice in G_N, the codebook, or the verifier above the N^{1+epsilon} budget invalidates the source lower-bound accounting.

## Learning

Cycle 62 adds a new fork: high incidence rank can make the XOR carrier lower-bound property large, so an efficient semantic certificate would be natural, while low rank is an upper-bound falsifier. The polylog beta=0 bridge remains valid, but the surviving source proof must be non-natural, non-large, proof-mediated, or direct.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch needs to distinguish a genuinely non-natural source certificate from a high-rank counting illusion; another abstract restatement would not decide whether the XOR carrier is proof-relevant or barrier-exposed.
- Situation seed: Random-affine XOR generated-SAT carrier: let L=(log N)^d with d>1, M=N^q, and let an explicit k-wise independent generator map each N-bit seed and position j to an L-bit formula index; define H_N as the parity of SAT labels on the generated bag.
- Varied variable: incidence-rank gap kappa=(r_N-K S log S)/L^k for S=N^{1+epsilon-delta}
- Held-fixed controls: q,rho<1+epsilon-delta so the polylog target substitution remains target-preserving for every fixed SAT exponent c., The generator and all transcripts are label-free and have charged size at most N^rho., The source model is nonuniform Boolean circuits on N input bits with lower-bound threshold S., The actual target label vector is SAT_L; random y is used only to test largeness and naturalness.
- Expected observation: Below kappa<=0, low-rank/codebook sketches should give explicit upper-bound falsifiers. Above kappa>>1, NoSmallCarrier becomes large with density 1-2^{-L^k}; any efficient certificate for actual SAT then looks natural unless it is deliberately non-large or proof-mediated.
- Transfer certificate needed: Before the intuition affects proof obligations, one must prove the explicit generator rank, verify q,rho and beta=0, exhibit the certificate verifier, and classify it as non-large, nonconstructive, non-natural, or else quarantine it under the natural-proofs obstruction.

## Next Experiment

Instantiate the random-affine generator with L=(log N)^2 and q in ((1+epsilon)/2,1+epsilon); compute r_N for the induced sparse incidence matrix and test whether the rank gap forces naturalness or low-rank falsification.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

A lower-bound proof that only tests agreement with SAT on a finite set H_m cannot be useful against SIZE_m(s) unless |H_m|=Omega(s/m). Below this threshold a lookup DNF of size O(|H_m|m) matches all SAT labels on H_m, giving a concrete falsifier to the claimed point-test certificate.

## Definitions

- source object: H_m is a uniformly listable subset of {0,1}^m with h(m) distinct SAT instances and labels SAT_m(x).
- target object: SIZE_m(s) is the nonuniform Boolean circuit class on m input bits over a fixed De Morgan basis with at most s gates or wires, up to constant-factor convention.
- controlled interface: the certificate induces the cylinder property P_H={f in {0,1}^{2^m}: f(x)=SAT_m(x) for every x in H_m}.
- target-preserving condition: P_H is useful only if every truth table computed by a circuit in SIZE_m(s) lies outside P_H, with no hidden advice or changed input length.
- observable: the manipulated parameter is h=|H_m|, measured against N=2^m and the target size s=m^k.

## Assumptions

- Circuit size counts exact-match terms of width m with O(m) cost per memorized positive point.
- H_m is explicit enough that membership in P_H is decidable in poly(N) time after listing H_m and computing SAT labels by exhaustive search.
- The route is restricted to pointwise disagreement on H_m; no algebraic, semantic, or proof-system condition outside P_H is used.
- Usefulness is against the same nonuniform target class SIZE_m(s), not a smaller restricted class.

## Equations

- cylinder_density: `\mu(P_H)=2^{-h}`. Valid when: Valid when H_m has h distinct coordinates and P_H fixes exactly those SAT-labeled truth-table bits.
- lookup_size: `\operatorname{size}(C_{H})\le A\,h\,m+A`. Valid when: Valid when the circuit basis permits literals, conjunctions, and disjunctions for exact-point DNF memorization.
- usefulness_necessary_threshold: `P_H\text{ useful against }SIZE_m(s)\Rightarrow A h m+A>s`. Valid when: Requires the controlled interface to reject circuits solely by disagreement with SAT on H_m.
- natural_largeness_threshold: `h\le a\log_2 N=a m\Rightarrow \mu(P_H)\ge N^{-a}`. Valid when: Applies in the standard natural-proof regime where largeness means inverse-polynomial density in truth-table length N.

## Attempted Derivation

- Fix m, N=2^m, target size s=m^k, and a uniformly listable test set H_m of h distinct SAT instances.
- Define P_H as the cylinder of all m-bit truth tables agreeing with SAT_m on H_m; this is the exact proof object exposed by a point-test lower-bound route.
- The density calculation gives mu(P_H)=2^{-h}; for h=O(m) this is N^{-O(1)}, so largeness is present.
- Construct C_H by OR-ing exact m-literal terms for the positive SAT-labeled points in H_m; C_H has size at most A h m+A and agrees with SAT on all of H_m.
- If A h m+A<=s, then C_H is a target circuit whose truth table belongs to P_H, so P_H is not useful against SIZE_m(s).
- Therefore any valid point-test certificate for SAT_m notin SIZE_m(s) needs h>Omega(s/m); for s=m^k this is h>Omega(m^{k-1}).
- If h=O(m) and usefulness nevertheless holds, the property is large, constructive, and useful; under target PRFs it becomes a natural-proof contradiction.
- If h is superlinear, the route may escape largeness, but the remaining obligation is a direct explicit hitting theorem against all SIZE_m(s) circuits, not evidence for P != NP by itself.

Blocking gap: For h>Omega(s/m), no derivation proves that a uniformly described H_m actually hits every SIZE_m(s) circuit; H_m={0,1}^m is a trivial non-large endpoint that merely restates the lower bound.

## Falsifiers

- Lookup DNF matching all SAT labels on H_m whenever A|H_m|m+A<=s is the decisive usefulness falsifier.
- A SIZE_m(s) PRF family secure against poly(N)-time truth-table distinguishers falsifies any large constructive useful P_H with h=O(m).
- The full truth-table test H_m={0,1}^m avoids natural largeness but is circular and supplies no nontrivial lower-bound method.
- Padding that measures s in a larger length while H_m sees only a small core worsens the memorization leakage and destroys target preservation.

## Learning

The point-test lower-bound route has an exact two-threshold anatomy: h=O(m) yields a valid natural-property object under usefulness, while h<=s/O(m) is not useful because the target class memorizes the tested labels. For SIZE_m(m^k), a certificate needs h=Omega(m^{k-1}); this is route-level progress and a concrete falsifier for short counterexample-set slogans, not progress on P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch needs a concrete quantitative transfer because point-test lower-bound certificates look barrier-free only until h is compared with both natural density and target-circuit memorization size.
- Situation seed: For fixed k, consider padded or unpadded SAT_m and a uniformly generated family H_{m,beta} of h=m^beta queried instances; the proposed proof certifies SAT_m notin SIZE_m(m^k) only by disagreement on H_{m,beta}.
- Varied variable: beta, the exponent in the number of point tests h=m^beta.
- Held-fixed controls: Target class remains nonuniform SIZE_m(m^k) over the same m-bit SAT slice., The verifier property is exactly the cylinder P_H and uses no semantic side condition., H_{m,beta} is listable in poly(N) and SAT labels are computed without advice., Circuit size convention and input length are held fixed across beta.
- Expected observation: For beta<k-1 the lookup DNF has size O(m^{beta+1})<=m^k and falsifies usefulness; for beta<=1 any valid useful cylinder is a natural property; only beta>max(1,k-1) can be both non-large and beyond the memorization falsifier.
- Transfer certificate needed: A proof that every SIZE_m(m^k) circuit disagrees with SAT_m on H_{m,beta}, plus an audit that this hitting proof is advice-free and does not secretly change the target class or length parameter.

## Next Experiment

Run a finite prior-art boundary check against teaching dimension, sample compression, hitting-set lower bounds, and Razborov-Rudich natural proofs; then test whether any known SAT lower-bound certificate uses a non-cylinder feature that escapes the lookup-DNF falsifier.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

A constant-rate, advice-free generated anti-ball source with image entropy D and kappa-dense lengths yields an E language with SIZE lower bound exponent any delta<theta/(kappa(1+D)); unbounded proof-generation exponent is a quantitative falsifier, not a harmless proof-length issue.

## Definitions

- source object: ABGen(theta,D,kappa,gamma) is an advice-free deterministic streamer which on source length m in S outputs a canonical list I_m of at most 2^{Dm+o(m)} m-bit truth tables and a generated nonblackbox proof that at least one listed row avoids SIZE(2^{theta m-o(m)}).
- target object: L_AB is the E-uniform rank-multiplexed and kappa-padded language whose core truth table is M_m(i,x)=T_{m,i}(x) for T_{m,i} in I_m.
- controlled interface: generated row/proof stream -> canonical rank multiplexer -> padded E language; the proof certifies source soundness but is not advice to L_AB.
- target-preserving condition: gamma is a fixed constant, S is kappa-dense, ranks are E-canonical, and anti-ball soundness is against unrestricted nonuniform circuits with no row-selection advice.
- anti-ball observable: distance zero is already enough for exact MCSP hardness; positive radius rho is charged only if the source proves smaller-center exclusion or spends an edit list.

## Assumptions

- Circuit model is unrestricted fan-in two Boolean SIZE(s); uniformity is only for generating L_AB, not for target lower bounds.
- S is kappa-dense: every large target length lies within a padding factor kappa+o(1) of some core length m(1+D).
- The generated proof may be exponentially long, but its stream and the rows are produced in time 2^{gamma m+o(m)} with fixed gamma.
- The canonical list has no indexed decoder or restart mechanism producing row bits by circuits below 2^{theta m-o(m)}.
- The projection of valid generated pairs remains sparse, so the construction is not a large poly(N)-decidable useful natural property.

## Equations

- image_and_generation_budget: `|I_m| \le 2^{D m+o(m)},\quad T_G(m) \le 2^{\gamma m+o(m)},\quad \gamma=O(1)`. Valid when: Valid when ABGen uses an advice-free deterministic streaming generator on source lengths m and D,gamma are fixed constants independent of m.
- multiplexer_row_hardness: `C(M_m) \ge 2^{\theta m-o(m)}\quad\text{where }M_m(i,x)=T_{m,i}(x)`. Valid when: Applies when the anti-ball proof is sound for unrestricted nonuniform circuits and rank multiplexing lists every generated row without advice.
- padded_extraction_exponent: `\forall \delta<\frac{\theta}{\kappa(1+D)},\quad C(L_{AB,n})>2^{\delta n}\text{ for all large }n`. Valid when: Requires kappa-dense padding, bounded image entropy D, and constant generation exponent so that the target language remains in E.

## Attempted Derivation

- Define M_m by rank-multiplexing the generated list I_m; no selector for the hard row is used in the language definition.
- If M_m had circuits below 2^{theta m-o(m)}, fixing the rank of the certified hard row would give a circuit of that size plus O(Dm), contradicting anti-ball soundness.
- Pad M_m across kappa gaps; a circuit for the padded length n restricts to a circuit for the core, giving exponent theta/(kappa(1+D)).
- Compute L_AB by regenerating the canonical stream up to the queried bit; fixed gamma gives 2^{O(n)} time, while gamma(m)=omega(1) exits E.

Blocking gap: No explicit ABGen(theta,D,kappa,gamma) source with unrestricted anti-ball soundness and sparse non-natural projection is known.

## Falsifiers

- falsifier: a rank-addressed decoder or checkpoint restart computing T_{m,i}(x) with circuits 2^{a m+o(m)} for a<theta invalidates MCSP no-side soundness.
- falsifier: gamma(m)=omega(1) makes regeneration time 2^{omega(n)} after padding, so the extracted language is not certified to be in E.
- falsifier: a poly(N)-decidable projection of measure at least 1/poly(N) that excludes small circuits becomes a valid useful natural property rather than a sparse carrier.
- falsifier: a proof excluding only uniform, algebraic, or restricted circuits does not certify unrestricted MCSP row hardness needed by the multiplexer argument.

## Learning

Cycle 62 closes a ledger gap: generated proof length is harmless, but generated proof time must have a fixed exponential rate. The bridge exponent is unchanged by constant gamma; unbounded gamma is a valid quantitative falsifier because it moves the target out of E.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for generated anti-ball source proposals.`
- Rationale: The branch already has the transfer formula; the live uncertainty is whether proof generation overhead or row/proof locators silently destroy the target-preserving E lower-bound certificate.
- Situation seed: For each m, imagine ABGen streams 2^{Dm} candidate truth tables and a generated nonblackbox anti-ball proof that some row has MCSP threshold above 2^{theta m}; L_AB rank-multiplexes the rows and pads across kappa gaps.
- Varied variable: generation exponent gamma in T_G(m)=2^{gamma m+o(m)}
- Held-fixed controls: theta, D, and kappa are fixed positive constants with theta>0., No advice, no nonuniform hard-row choice, and canonical rank order are allowed., Soundness is against unrestricted nonuniform SIZE circuits, not a restricted model., Projection of valid pairs is kept sparse to avoid natural-property largeness pressure.
- Expected observation: For every fixed gamma the lower-bound exponent delta remains theta/(kappa(1+D)); when gamma grows with m, E-uniformity collapses even though the nonuniform row lower bound would still be meaningful.
- Transfer certificate needed: A clocked advice-free streamer, E-canonical unranking, unrestricted anti-ball soundness, sparsity of the projection, and a padding lemma preserving the theta,D,kappa parameters.

## Next Experiment

Instantiate ABGen with one named nonblackbox proof system Psys; audit whether its proof generator is fixed-exponent, advice-free, sparse in projection, and sound for unrestricted SIZE(2^{theta m}) anti-balls.
