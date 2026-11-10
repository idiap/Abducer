# cycle-0069

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For the beta=0 XOR carrier, any label-mediated source certificate that is dense and constructive at the target length L extends to an ambient natural property for L-bit functions by restriction to U_N. Thus the tiny density of the induced H_N truth-table image is not the decisive escape; the valid escape is sub-2^{-poly(L)} label density, nonconstructivity, advice leakage, or failure of same-model soundness.

## Definitions

- source object: H_{N,z}(x)=\langle A_N(x),z\rangle_2, where A_N maps N-bit source inputs to incidence vectors over U_N and z is a label vector for formulas in U_N.
- target object: SAT_L is the Boolean function on L-bit formula encodings, with L=(\log N)^d and d>1 in the surviving polylog-query window.
- controlled interface: U_N is a uniformly enumerable set of M_N=N^{q+o(1)} distinct L-bit formulas and A_N has circuit overhead N^{\rho+o(1)}.
- target-preserving condition: q<1+\epsilon, \rho<1+\epsilon, beta=0, no advice in U_N or in the verifier, and certificate soundness is stated in the same circuit model as the target lower bound.
- label certificate: P_N\subseteq\{0,1\}^{M_N} accepts label vectors claimed to force C(H_{N,z})>N^{1+\epsilon}.
- ambient extension: Q_N(f)=1 iff P_N((f(u))_{u\in U_N})=1 for a full L-bit truth table f.

## Assumptions

- Nonuniform Boolean circuits are the source and target model; size counts wires/gates up to N^{o(1)} factors.
- U_N has no repeated coordinates, or repetitions are quotient-compressed before the density calculation.
- P_N is decidable in time 2^{O(L)} from the M_N queried labels, so Q_N is constructive in the natural-proofs sense for L-bit functions.
- Soundness means P_N(z)=1 implies C(H_{N,z})>N^{1+\epsilon}, not merely a syntactic or proof-system claim.
- The substitution upper bound holds uniformly for every L-bit function f with circuits of size L^c.

## Equations

- label_space_size: `M_N=|U_N|=N^{q+o(1)}=2^{qL^{1/d}+o(L^{1/d})}`. Valid when: Valid when L=(log N)^d with fixed d>1 and the generator emits N^{q+o(1)} distinct target formulas.
- beta_zero_substitution: `C(H_{N,f|U_N})\le N^{\max\{\rho,q\}+o(1)}\cdot L^{O(c)}=N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies when target queries have polylogarithmic length and f has L^c-size circuits for fixed c.
- restriction_density_preservation: `\Pr_{f\leftarrow\{0,1\}^{2^L}}[Q_N(f)=1]=|P_N|/2^{M_N}=\delta_N`. Valid when: Valid when the coordinates in U_N are distinct so a random full truth table induces a uniform label vector.
- natural_largeness_threshold: `\delta_N\ge 2^{-L^a}\quad\Longrightarrow\quad Q_N\text{ is }2^{-\mathrm{poly}(L)}\text{-large}`. Valid when: Requires a fixed constant a and the standard target-length naturalness convention for L-bit Boolean functions.

## Attempted Derivation

- Fix L=(log N)^d, d>1, and a uniform distinct query set U_N of size M_N=N^{q+o(1)}.
- Given a label property P_N, define Q_N on full L-bit truth tables by reading only coordinates in U_N.
- A uniformly random full truth table induces a uniformly random label vector on U_N; hence ambient target density equals label density delta_N exactly.
- If f has L^c-size circuits, beta=0 substitution gives H_{N,f|U_N} size N^{max{rho,q}+o(1)}; with max{rho,q}<1+epsilon, soundness forces Q_N(f)=0.
- If P_N is decidable in 2^{O(L)} and delta_N>=2^{-poly(L)}, then Q_N is a constructive large property useful against L^c-size circuits.

Blocking gap: No construction is given of a P_N that accepts SAT|U_N while remaining sound; the derivation only classifies when such a proof-mediated route would naturalize.

## Falsifiers

- falsifier: beta>0 with transfer exponent q+beta c reaches the source threshold before all SAT exponents are excluded.
- falsifier: low constructive rank or label-free codebook for the XOR incidence map gives a direct upper bound for H_N.
- falsifier: P_N has density at least 2^{-poly(L)} and verifier time 2^{O(L)}, yielding a valid target-restriction natural property rather than a barrier escape.
- falsifier: U_N or the certificate verifier uses nonuniform advice not reproducible by the target-side natural property.
- falsifier: soundness is proved only for realized SAT labels and not for all small target functions f, breaking useful-property naturalization.

## Learning

Cycle 69 turns the image-density ambiguity into a precise threshold theorem. A label-mediated beta=0 XOR certificate naturalizes through restriction to U_N exactly when its label density is at least 2^{-poly(L)} and its verifier is 2^{O(L)}-constructive. The earlier ambient-tiny source image is not by itself a valid escape; the real escapes are nonlarge density, nonconstructivity, advice leakage, or explicitly nonrelativizing direct lower bounds.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for proof-mediated beta=0 XOR certificates.`
- Rationale: The branch already has the beta=0 transfer; the unresolved issue is whether a certificate escapes natural proofs because the source-function image is ambient-tiny. A concrete density sweep decides the route status.
- Situation seed: Let L=(log N)^2, choose a uniform set U_N of M=N^q generated SAT formulas, and define H_{N,z}(x)=<A_N(x),z> over F_2 with A_N computable in size N^rho and q,rho<1+epsilon.
- Varied variable: The relative label density delta_N of the accepted certificate set P_N, varied from constant density through 2^{-L^a} down to 2^{-N^gamma}.
- Held-fixed controls: beta=0 polylog target-query length, q,rho<1+epsilon for the magnification bridge, uniform distinct enumeration of U_N without advice, same nonuniform circuit model for source soundness and target substitution
- Expected observation: For delta_N>=2^{-poly(L)} and verifier time 2^{O(L)}, restriction extension produces a large constructive useful property on L-bit functions; for delta_N=2^{-N^gamma}, the naturalness obstruction disappears but the source lower-bound proof burden remains unchanged.
- Transfer certificate needed: A formal restriction-extension lemma proving exact density preservation, constructivity within 2^{O(L)}, and contrapositive soundness from all L^c-size target circuits to subthreshold H_N circuits.

## Next Experiment

Instantiate U_N with L=(log N)^2 and q in ((1+epsilon)/2,1+epsilon); compute whether candidate proof systems give certificate density above 2^{-poly(L)} or force a nonlarge escape, then run the prior-art boundary check.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

A proof-mediated local lower-bound route naturalizes if it has a logarithmic table/proof seed cluster with direct cluster-soundness; ordinary public-coin soundness certifies such usefulness only at the threshold |C|>delta 2^ell, which is incompatible with polynomial-density naturalization when ell=Omega(log N) and delta is constant or mildly small.

## Definitions

- source object: a public-coin verifier V_m(T,pi;rho) for the statement CC(T)>s, where T in {0,1}^N is a truth table with N=2^m, pi has length L, rho in {0,1}^ell, and each seed queries at most q table bits and t proof bits.
- target object: the nonuniform class SIZE_m(s), usually s=m^k, represented by its m-bit truth tables; target usefulness means the constructed property rejects every truth table computed by a circuit of size at most s.
- controlled interface: a seed cluster C and an explicit predicate Cons_C over the union B_C of proof positions queried by C; P_C(T)=1 iff there exists y in {0,1}^{B_C} such that Cons_C(y) holds and every seed in C accepts using T restricted to A_C and y restricted to its proof queries.
- target-preserving condition: direct cluster-soundness holds, namely for every T in TT(SIZE_m(s)) and every y on B_C, Cons_C(y) fails or at least one seed in C rejects; C, A_C, B_C, and Cons_C are computable in poly(N) without target-dependent advice.
- A_C is the union of all table coordinates queried by seeds in C and Q_C=|A_C|; B_C is the union of all proof coordinates queried by seeds in C and H_C=|B_C|.
- The verifier is deterministic after fixing rho, and all query locations and acceptance predicates are uniformly computable from m,rho and previous local answers in time poly(N).

## Assumptions

- Completeness is cluster-local: TT(SAT_m) has a proof pi* such that Cons_C(pi*|B_C) holds and all seeds in C accept.
- Constructivity is measured on full truth-table input T in time poly(N), not in time poly(m).
- The cluster C is fixed from m and the verifier, not chosen using a low-complexity circuit, a PRF key, or nonuniform knowledge of TT(SAT_m).
- Usefulness is the direct cluster-soundness condition above; ordinary average-case verifier soundness is not silently substituted for it.
- The natural-proof pressure applies only against a target class containing a PRF family secure against poly(N)-time truth-table distinguishers with inverse-polynomial advantage.

## Equations

- cluster_density: `\mu(P_C) \ge 2^{-Q_C}`. Valid when: Valid when the SAT witness pi* makes every seed in C accept and every truth table matching TT(SAT_m) on A_C may reuse the same local proof assignment.
- cluster_constructivity: `T_{dec}(P_C) \le 2^{H_C}\,|C|\,\mathrm{poly}(N,L)`. Valid when: Valid when B_C is explicitly enumerated, Cons_C is polynomial-time computable, and the decider brute-forces only the proof bits in B_C.
- ordinary_soundness_threshold: `\text{ordinary soundness implies cluster rejection only if } |C|/2^{\ell} > \delta`. Valid when: Valid when soundness says every bad T and global proof pi is accepted on at most a delta fraction of all public seeds.
- density_soundness_incompatibility: `Q_C\le A\log N,\ q_{min}\ge1 \Rightarrow |C|\le A\log N \Rightarrow \delta < A\log N/2^{\ell}`. Valid when: Applies when each seed reads at least one fresh-or-counted table coordinate and natural largeness requires Q_C bounded by O(log N).
- prf_distinguisher_advantage: `\mathrm{Adv}_{D_{P_C}} \ge \mu(P_C) \ge N^{-A}\quad\text{if }Q_C\le A\log_2 N`. Valid when: Valid when P_C is useful against the exact circuit class containing the PRF truth tables and is decidable in polynomial time in N.

## Attempted Derivation

- Fix V_m, a cluster C, and define P_C using only the table coordinates A_C and proof coordinates B_C seen by C.
- Completeness for TT(SAT_m) gives one local proof assignment y*=pi*|B_C; every table agreeing with TT(SAT_m) on A_C is accepted, giving density at least 2^{-Q_C}.
- The decider for P_C enumerates all 2^{H_C} local proof assignments and checks all seeds in C, so H_C=O(log N) and polynomially describable C give poly(N) constructivity.
- Direct cluster-soundness gives P_C cap TT(SIZE_m(s)) empty, hence usefulness against the named target class.
- If only ordinary soundness with error delta is available, an accepting cluster contradicts it only when the cluster occupies more than a delta fraction of all seeds, i.e. |C|>delta 2^ell.
- For ell=Theta(log N) and delta=1/3, this forces |C|=Omega(N^b), which makes Q_C at least polynomial unless table queries collapse heavily; polynomial-density naturalization is then lost.

Blocking gap: The missing finite object is a direct cluster-soundness or extractor theorem for a logarithmic-union cluster; average public-coin soundness is quantitatively too weak.

## Falsifiers

- Constant-soundness PCP-style verifier with ell=Theta(log N): any cluster with Q_C=O(log N) has too few seeds to contradict ordinary soundness; this is a falsifier to average-soundness-to-usefulness transfer.
- 3-XOR local-view carrier: small queried subinstances are often satisfiable by local assignments even when the global proof object is inconsistent, falsifying naive long-proof escape claims.
- Nonuniform row-selection leakage: if C is selected using TT(SAT_m), a PRF key, or a forbidden circuit, constructivity and target preservation fail.
- High-overlap but large-union cluster with H_C=omega(log N): usefulness may survive, but poly(N) constructivity of the natural property is no longer valid.
- A PRF family inside SIZE_m(s) secure against poly(N)-time truth-table distinguishers is the conditional conflict target for any large constructive useful P_C.

## Learning

Cycle 69 sharpens the proof-mediated escape: long proofs do not matter by themselves. A logarithmic-union accepting cluster with direct cluster-soundness creates a valid large constructive useful property; ordinary soundness can justify usefulness only at |C|>delta 2^ell, which destroys density for ell=Theta(log N). The new contribution is the exact cluster-soundness versus density incompatibility and a 3-XOR-style falsifier template.

## Gedanken Experiment Design Seed

- Need decision: `Design and use now as a falsifier probe.`
- Rationale: The route currently hinges on whether long proof length blocks naturalization; the decisive issue is a concrete cluster-soundness threshold, not another abstract barrier restatement.
- Situation seed: A PCP-like verifier for the claimed certificate CC(T)>m^k whose long proof layer is modeled by a 3-XOR constraint graph; instantiate clusters C of public seeds and test whether P_C accepts an easy table T0.
- Varied variable: The overlap deficit Delta=t|C|-H_C, equivalently how many proof-query collisions the seed cluster forces while keeping Q_C=O(log N).
- Held-fixed controls: N=2^m, target class SIZE_m(m^k), and truth-table constructivity measured in poly(N)., Each seed makes q=O(log N) table queries and t=O(1) or O(log N) proof queries with uniform query computation., The cluster C is fixed from m and V_m and carries no nonuniform advice about SAT, PRF keys, or excluded circuits., Usefulness must reject every TT(SIZE_m(m^k)) table, not merely most random tables or most proofs.
- Expected observation: For low overlap, local 3-XOR assignments satisfy all queried views on an easy T0, giving a falsifier to usefulness. For high overlap with Q_C,H_C=O(log N), any successful soundness proof immediately yields a large constructive useful property and therefore natural-proof pressure.
- Transfer certificate needed: A formal cluster-soundness extractor: from any Cons_C-satisfying accepting local assignment for a target-class table, derive either a global proof accepted on more than delta 2^ell seeds or a direct contradiction to T in SIZE_m(m^k).

## Next Experiment

Instantiate the 3-XOR queried-view model with ell=b log N, q=O(log N), t=3, choose clusters with increasing overlap deficit Delta, and compute whether any Cons_C with H_C=O(log N) excludes all affine or constant-size target tables without becoming a natural property.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Block-summary openers give a nonuniform upper bound on every row of a generated MCSP carrier. Hence a claimed no-side threshold 2^{theta m} is invalid whenever some block scale lambda has max{1-lambda+sigma(lambda),omega(lambda)}<theta.

## Definitions

- source object: a deterministic advice-free generated anti-ball MCSP carrier G_m whose rows T_{m,a}:{0,1}^m->{0,1} are intended to satisfy CC(T_{m,a})>2^{theta m}.
- target object: an E-uniform language obtained by low-image-entropy row multiplexing, with intended circuit lower bound exponent delta<theta/(kappa(1+D)).
- controlled interface: a block-summary opener covering the N=2^m input positions by 2^{(1-lambda)m+o(m)} rankable blocks, storing for each block a summary of 2^{sigma(lambda)m+o(m)} bits, and evaluating any bit in that block by circuits of size 2^{omega(lambda)m+o(m)}.
- target-preserving condition: the carrier remains valid only if no such opener has exponent below theta, the row family is advice-free E-uniform, kappa-gap lengths are preserved, and low distinct-image entropy D is E-canonically unrankable.

## Assumptions

- Circuit size is unrestricted nonuniform Boolean circuit size for truth tables of m input bits.
- The block cover is rankable from x in poly(m) gates, and the summary lookup table may be hardwired because MCSP hardness is nonuniform.
- The opener circuit works for every x in its block and for the actual emitted row, not merely for most positions.
- The exponent functions sigma(lambda) and omega(lambda) are constants or have limits along the source length subsequence; o(1) slack is absorbed below theta.
- This is a route-level source falsifier; it does not assert P != NP or refute MCSP hardness in general.

## Equations

- block_count: `B_m(\lambda)=2^{(1-\lambda)m+o(m)}`. Valid when: Valid when the block cover partitions or rankably covers N=2^m positions with block size 2^{lambda m+o(m)}.
- summary_lookup_size: `S_{lookup}(m,\lambda)=2^{(1-\lambda+\sigma(\lambda))m+o(m)}`. Valid when: Valid when every block summary has length 2^{sigma(lambda)m+o(m)} and all summaries are hardwired nonuniformly.
- opener_upper_bound: `CC(T_{m,a}) \le 2^{(\max\{1-\lambda+\sigma(\lambda),\omega(\lambda)\}+o(1))m}`. Valid when: Applies after block rank computation, summary lookup, and within-block opener circuits are valid for the same emitted row.
- block_cap: `\alpha_{blk}=\inf_{0\le\lambda\le1}\max\{1-\lambda+\sigma(\lambda),\omega(\lambda)\}`. Valid when: Requires a family of block-summary openers at the tested scales and constant exponent profiles along the carrier lengths.
- source_validity_gate: `\theta \le \alpha_{blk}`. Valid when: Necessary when the source claims MCSP no-side hardness above 2^{theta m} for every accepted or selected row.

## Attempted Derivation

- Fix a claimed hard row T:{0,1}^m->{0,1} emitted by the generated carrier and a rankable cover of its N=2^m positions by B=2^{(1-lambda)m+o(m)} blocks.
- For each block j, assume a summary a_j of length 2^{sigma m+o(m)} and an opener O_j or uniform opener O that computes T(x) from a_j and the offset of x using 2^{omega m+o(m)} gates.
- Build a nonuniform circuit for T: on input x compute its block index j and offset, use a hardwired multiplexer over all summaries a_j, then run the opener.
- The hardwired summaries cost 2^{(1-lambda+sigma)m+o(m)} gates; the opener costs 2^{omega m+o(m)} gates; polynomial rank logic is negligible.
- Thus CC(T)<=2^{(max{1-lambda+sigma,omega}+o(1))m}. If this exponent is below theta, the alleged MCSP no-side row is contradicted.
- Apply the contrapositive to generated anti-ball carriers: every valid source theorem must prove absence of all block-summary openers below theta, in addition to absence of indexed openings, checkpoints, and algebraic skips.
- Conditional on a surviving row and E-canonical low-D unranking, the existing multiplexing argument gives L in E and transfers any target circuit of exponent delta<theta/(kappa(1+D)) into a forbidden row circuit.

Blocking gap: The derivation gives an upper-bound falsifier, not a source construction. The open gap is a nonnatural, advice-free generated anti-ball source with no subthreshold block-summary opener and a proof of unrestricted row hardness.

## Falsifiers

- falsifier: a rankable block cover with summary exponent sigma and opener exponent omega satisfying max{1-lambda+sigma,omega}<theta
- falsifier: a Merkleized, tableau, or commitment-style proof stream whose authentication paths are generated by subthreshold circuits for arbitrary row bits
- falsifier: nonuniform length or row advice selecting the only hard row instead of E-canonical distinct-image unranking
- falsifier: D-entropy quotient exists abstractly but has no E-uniform canonical unranking
- falsifier: anti-ball certificate excludes only uniform circuits or restricted circuits rather than unrestricted nonuniform circuits
- falsifier: theta is above the checkpoint, skip-ahead, or block-summary cap even though the extraction formula is otherwise valid

## Learning

Cycle 69 adds a covering-opener cap: any generated MCSP carrier with rankable block summaries has row circuits of exponent max{1-lambda+sigma,omega}. This is a valid finite falsifier for many non-skippable proof streams and refines the source obligation to block-summary-hard, noniteratable, advice-free anti-ball generation. The carrier-to-E transfer is unchanged but only conditional on surviving this audit.

## Gedanken Experiment Design Seed

- Need decision: `design now as a falsifier probe`
- Rationale: The branch needs a concrete audit for generated anti-ball sources after skip-hardness: many plausible proof streams are not algebraically skippable but still expose block summaries that nonuniform circuits can hardwire.
- Situation seed: Take a generated MCSP anti-ball carrier whose proof stream is divided into rankable blocks of 2^{lambda m} row positions, with one per-block transcript summary used to open all bits in that block; test whether such a carrier can still claim CC(T)>2^{theta m}.
- Varied variable: lambda, the block length exponent in the block-summary cover.
- Held-fixed controls: Unrestricted nonuniform circuit complexity is the MCSP target model., The row family is advice-free and E-uniformly generated at fixed exponential rate., The low-image-entropy multiplexing parameter D and padding gap kappa are fixed., The intended threshold theta and target transfer delta<theta/(kappa(1+D)) are held fixed., No dense constructive property repair is allowed.
- Expected observation: If some lambda makes max{1-lambda+sigma(lambda),omega(lambda)} below theta, the carrier is invalid even without algebraic skip-ahead; if every lambda stays above theta, the source survives this leakage audit and the remaining obstruction is genuine anti-ball soundness.
- Transfer certificate needed: A formal no-block-summary-opener theorem below theta, plus E-canonical row unranking and a proof that the anti-ball certificate excludes unrestricted circuits rather than a restricted or uniform subclass.

## Next Experiment

Instantiate the block-summary cap on three candidate implementations: Merkleized row/proof streams, divide-and-conquer tableau certificates, and nonalgebraic sequential generators with cached interval transcripts; compute alpha_blk and compare with the intended theta.
