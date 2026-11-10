# cycle-0003

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Let g be unbounded, nondecreasing, and poly(N)-time checkable on lengths. If the growth-padded SAT carrier H_g has C(H_g,N_m)>N_m^{1+epsilon} for infinitely many valid lengths N_m, then SAT is not in P/poly, hence NP is not subset P/poly.

## Definitions

- source object: H_g={x#0^t : x in SAT, |x|=m, |x#0^t|=N_m=(m+1)^{g(m+1)}} with nonuniform circuits measured only on valid lengths N_m.
- target object: SAT in P/poly as the complete-language proxy for NP subset P/poly; the target consequence is NP not subset P/poly, not a direct proof of P != NP.
- controlled interface: contrapositive circuit transfer SAT_m circuit -> H_g length-N_m circuit using one SAT circuit plus an O(N_m) parser and padding checker.
- target-preserving condition: the lower bound is valid on infinitely many valid lengths, g(m)->infty, length validity is decidable in poly(N_m), and no advice beyond the SAT_m circuit is introduced.

## Assumptions

- Fan-in-2 Boolean circuit size is the source lower-bound model; constants are absorbed by eventually large valid lengths.
- The source lower bound is length-promise/i.o.; an all-length lower bound is impossible because invalid lengths reject by O(N) circuits.
- g is fixed as part of the language, not supplied as advice; this blocks the prior unbounded-k nonuniform leakage.
- SAT in P/poly means there is one polynomial exponent c with circuits for every input length m.

## Equations

- valid_lengths: `N_m=(m+1)^{g(m+1)},\quad H_g\cap\{0,1\}^{N_m}=\{x\#0^{N_m-m-1}:x\in SAT_m\}`. Valid when: Valid when the delimiter format fixes m and g is computable within polynomial time in N_m.
- upper_transfer: `C_{H_g}(N_m)\le a\,(N_m+C_{SAT}(m))\le a\,(N_m+(m+1)^c)=a\,(N_m+N_m^{c/g(m+1)})`. Valid when: Applies after assuming SAT has m^c-size circuits and the parser uses only linear-size circuitry.
- threshold_absorption: `g(m+1)>c/(1+\epsilon/2)\ \Longrightarrow\ C_{H_g}(N_m)\le N_m^{1+\epsilon}\text{ for all large }m`. Valid when: Requires sufficiently large valid lengths so constants and the O(N_m) checker floor are absorbed.

## Attempted Derivation

- Assume toward contradiction that SAT has P/poly circuits of size m^c for some fixed c.
- Build the H_g circuit at valid length N_m by checking the delimiter/padding pattern in O(N_m) gates and feeding the prefix x to the SAT_m circuit.
- Since g(m)->infty, eventually c/g(m+1)<1+epsilon/2, so the transferred circuit has size at most N_m^{1+epsilon}.
- This contradicts an infinitely-often valid-length lower bound C(H_g,N_m)>N_m^{1+epsilon}; therefore no fixed c exists for SAT.

Blocking gap: The required source lower bound is a barely-superlinear lower bound for a sparse explicit NP carrier on valid lengths; proving it already encodes superpolynomial SAT lower bounds in the unpadded parameter.

## Falsifiers

- falsifier: If g is bounded by k, the consequence collapses to ruling out only SAT circuits below exponent about k(1+epsilon).
- falsifier: If the source claim is all-length rather than valid-length/i.o., invalid lengths have trivial rejecting circuits and kill the lower bound.
- falsifier: If a bundled carrier includes small k slices, those slices dominate the threshold and reintroduce the finite-exponent obstruction.
- falsifier: If length validity or prefix recovery needs super-polynomial time in N, H_g may leave NP and the target-preserving transfer is invalid.

## Learning

Cycle 3 finds a valid single-carrier repair: growth padding N_m=(m+1)^{g(m+1)} converts an i.o. N^{1+epsilon} lower bound for H_g into exclusion of every SAT exponent c. This is route-level progress, not P vs NP; the hard obligation is now the sparse valid-length lower bound.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Instantiate g(r)=ceil(log log(r+4)); prove the verifier and length test are poly(N), then analyze whether valid-slice lower bounds for H_g admit a proof-complexity or MCSP carrier formulation.

# Barrier-Aware Lower-Bound Route: algebrization transfer audit

## Candidate Lemma

Let T be a proof template for a uniform NP language K notin P. If T satisfies AlgTP(T,K), meaning the same derivation proves K^O notin P^{\widetilde O} for every oracle O and every admissible low-degree extension \widetilde O encoding O, then T is not a valid route to P != NP. A Baker-Gill-Solovay collapse oracle A has P^A=NP^A, and recoverability of A from \widetilde A gives K^A in P^{\widetilde A}, contradicting the algebrized conclusion.

## Definitions

- source object: an arithmetizing lower-bound proof template T whose oracle dependence is mediated by low-degree extension access \widetilde O and whose source claim is K in NP \ P.
- target object: the uniform separation NP not subset P, witnessed by a named NP language K and polynomial-time target reductions preserving oracle relativization.
- controlled interface: nondeterministic verifiers may query O, deterministic algorithms in the algebrized simulation may query \widetilde O, and original O-bits are polynomial-time recoverable from \widetilde O.
- target-preserving condition: T is accepted as algebrizing only if its empty-oracle proof transfers to K^O notin P^{\widetilde O} for all oracles O and admissible extensions \widetilde O.
- admissible extension: \widetilde O is a standard low-degree extension representation with polynomial query-length and time overhead.

## Assumptions

- K^O is obtained by the standard relativization of the verifier for K, so K^O is in NP^O.
- For every admissible \widetilde O, there is a polynomial-time oracle procedure recovering each Boolean oracle bit O(x) from \widetilde O.
- There exists a Baker-Gill-Solovay oracle A such that P^A=NP^A.
- The proposed proof template claims full algebrizing validity, not merely use of algebra inside the empty-oracle proof.

## Equations

- AlgTP: `\operatorname{AlgTP}(T,K)\Rightarrow \forall O\,\forall \widetilde O\supseteq O:\ K^O\in NP^O\ \land\ K^O\notin P^{\widetilde O}`. Valid when: Valid when the proof template claims algebrization and the target-preserving condition quantifies over all oracles.
- BGS-collapse: `\exists A:\ P^A=NP^A`. Valid when: Valid in the classical relativized regime used to test oracle-invariant separation proofs.
- recovery-overhead: `A\leq_T^{n^{O(1)}}\widetilde A`. Valid when: Applies when the algebraic extension exposes original oracle bits with polynomial overhead.
- extension-containment: `P^A=NP^A\ \land\ A\leq_T^{n^{O(1)}}\widetilde A\Rightarrow NP^A\subseteq P^{\widetilde A}`. Valid when: Requires the collapse oracle and polynomial recovery of A from the extension oracle.
- contradiction: `K^A\in NP^A\subseteq P^{\widetilde A}\quad\bot\quad K^A\notin P^{\widetilde A}`. Valid when: Requires the algebrizing transfer claim and the collapse oracle instantiated together.

## Attempted Derivation

- Typed the proof object as AlgTP(T,K), not as vague arithmetization.
- Instantiated the claimed algebrized transfer at an arbitrary oracle O and admissible extension \widetilde O.
- Chose a Baker-Gill-Solovay oracle A with P^A=NP^A.
- Used K^A in NP^A and the collapse P^A=NP^A to obtain K^A in P^A.
- Used polynomial recoverability A<=_T^p \widetilde A to simulate the P^A decider inside P^{\widetilde A}.
- Derived K^A in P^{\widetilde A}, contradicting the AlgTP conclusion K^A notin P^{\widetilde A}.
- Concluded that fully algebrizing templates are invalid for this target, while partial algebraic methods require a separate escape certificate.

Blocking gap: The argument only kills templates satisfying full AlgTP. It does not classify proofs using algebra solely inside unrelativized SAT syntax, machine-code diagonalization, or proof-system soundness arguments.

## Falsifiers

- falsifier: the BGS collapse oracle A with P^A=NP^A invalidates any fully algebrizing separation transfer.
- falsifier: if \widetilde A does not permit polynomial-time recovery of A, the target model is not the standard algebrization model and the lemma is not valid.
- falsifier: a method depending essentially on empty-oracle Cook-Levin tableau syntax lies outside AlgTP and must be audited under L3-nonalgebrizing-escape-obligation.
- falsifier: any route that says arithmetization escapes barriers but cannot name S has an undefined escape feature.

## Learning

Cycle 3 converts algebrization into a precise route obstruction: AlgTP(T,K) plus standard extension recoverability contradicts the BGS collapse oracle. Algebraic lower-bound methods remain viable only if they identify a nonalgebrizing feature such as unrelativized syntax, nonblack-box machine encoding, or proof-system soundness, and then prove target preservation without advice leakage. This is valid route-level progress, not evidence for P != NP itself.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Audit one concrete nonalgebrizing candidate: an unrelativized Cook-Levin/proof-complexity route. Source object: lower bounds for a named proof system encoding SAT tableaux. Target object: SAT notin P. Test whether the proof-system lower bound transfers to uniform algorithms without natural-proof largeness, relativizing oracle transfer, algebrizing transfer, or nonuniform leakage.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Length-dense E-uniform co-side reductions to GapMCSP at threshold N^epsilon yield an all-length E circuit lower bound 2^{Omega(n)} and hence the standard IW derandomization consequence. Without length density the same interface yields only an i.o.-E lower bound, so the derandomization transfer is not valid.

## Definitions

- source object: an E-uniform no-witnessed family (A,z_m) with A in DTIME(2^{O(m)}), z_m notin A, and z_m computable in time 2^{O(m)}.
- target object: GapMCSP_{epsilon,delta} on truth tables y of length N=2^n, where NO means CC(y)>N^epsilon and YES means CC(y)<=N^delta for fixed 0<delta<epsilon.
- controlled interface: a uniform many-one map R that on inputs of length m outputs a target truth table of length N_m=2^{n_m} in time poly(N_m), with n_m=Theta(m) on the extracted subsequence and no advice.
- target-preserving condition: for every selected m, z_m notin A implies R(z_m) is a NO instance of GapMCSP_{epsilon,delta}, and the hit lengths n_m are rho-dense: for every large n some hit k=n_m lies in [rho n,n].

## Assumptions

- Boolean circuit size is the target lower-bound measure; uniform bit access to R(z_m) is obtained by recomputing the relevant output bit in 2^{O(n_m)} time.
- The density selector n -> m(n) is computable in poly(n), or is otherwise uniformly recoverable inside the E machine.
- The IW consequence is invoked only from all-sufficiently-large length hardness 2^{eta n}, not from infinitely-often hardness.
- No nonuniform selector, promise-violating reduction, or average-case interpretation is used.

## Equations

- threshold_translation: `s(N)=N^{\epsilon}=2^{\epsilon n}\quad\text{for }N=2^n`. Valid when: Valid when the target MCSP instance is literally a truth table of length 2^n and epsilon is a fixed positive constant.
- carrier_no_side_lower_bound: `R(z_m)=\operatorname{tt}(f_{n_m})\ \wedge\ R(z_m)\in \mathrm{NO}\Rightarrow CC(f_{n_m})>2^{\epsilon n_m}`. Valid when: Applies after the co-side reduction preserves the MCSP NO promise and the output length is 2^{n_m}.
- padding_density_transfer: `k\in[\rho n,n]\ \wedge\ CC(f_k)>2^{\epsilon k}\Rightarrow CC(B_n)>2^{\epsilon\rho n}`. Valid when: Requires the dense hit length k to be chosen uniformly and B_n to restrict to f_k by fixing n-k variables.
- iw_target_consequence: `(\exists B\in E)(\forall^{\infty} n)\ CC(B_n)>2^{\eta n}\Rightarrow \mathrm{BPP}=\mathrm{P}`. Valid when: Valid when the standard worst-case Impagliazzo-Wigderson hardness hypothesis holds for all sufficiently large input lengths over Boolean circuits.

## Attempted Derivation

- Start with selected no-instances z_m for the source language A and compute y_m=R(z_m).
- By target preservation, y_m is a truth table of an n_m-bit Boolean function f_{n_m} with circuit complexity greater than 2^{epsilon n_m}.
- Uniformity of z_m and R gives bit access to f_{n_m} in time 2^{O(n_m)}, so the extracted sparse family is E-explicit.
- For an arbitrary large n, use rho-density to find a hit length k=n_m in [rho n,n]. Define B_n(u,v)=f_k(u), where |u|=k and |v|=n-k.
- If B_n had a circuit of size at most 2^{epsilon rho n}, fixing v would give a circuit for f_k of size at most 2^{epsilon k}, contradiction up to constant slack.
- Thus B in E has all-length hardness 2^{Omega(n)}, which is the valid input form for the IW derandomization theorem.

Blocking gap: The previous bridge did not require rho-dense target lengths. A length-balanced reduction n_m=Theta(m) is insufficient if the selected no-witnesses z_m exist only on a sparse set of m.

## Falsifiers

- falsifier: the carrier outputs high-MCSP truth tables only on infinitely many but multiplicatively sparse target lengths, giving no all-length IW hardness.
- falsifier: R is many-one hard only as a promise reduction and does not map the selected co-side inputs inside the valid NO promise.
- falsifier: the selected no-witnesses z_m require advice or search, causing nonuniform leakage into the extracted E language.
- falsifier: the MCSP threshold degrades to N^{o(1)}, collapsing the padding transfer below 2^{Omega(n)}.
- falsifier: the consequence claimed is only nonuniform i.o. lower bound, while the target statement needs uniform all-length hardness.

## Learning

Cycle 3 identifies the missing quantitative invariant: length-balanced co-side GapMCSP reductions give valid sparse E lower bounds, but IW derandomization needs rho-dense all-length hardness. The route is therefore not blocked at extraction once density is assumed; it is blocked at constructing uniform dense no-side carriers without nonuniform leakage.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Search for a source object with intrinsic dense no-instances: bounded-arithmetic proof search, truth-table generator range avoidance, or proof-complexity tautology families whose GapMCSP reduction preserves N^epsilon on every large length.
