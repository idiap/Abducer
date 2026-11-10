# cycle-0002

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Fix epsilon>0. Let H_k=Pad_k(SAT). If for every target exponent c there is a padding parameter k with c/k<1+epsilon such that C_{H_k}(N)>N^{1+epsilon} on all sufficiently large padded lengths N=n^k, then SAT notin SIZE(n^c) for every c, hence NP is not contained in P/poly. For one fixed k the same bridge excludes only c<k(1+epsilon).

## Definitions

- source object: H_k=Pad_k(SAT), the total padded SAT language at lengths N=n^k, measured by nonuniform Boolean circuit size C_{H_k}(N).
- target object: SAT circuit lower bounds C_{SAT}(n) notin O(n^c) for every fixed c, implying NP not subset P/poly.
- controlled interface: the uniform padding map R_k(x)=x10^{n^k-n-1} and circuit pullback/pushforward with an explicit O(N)-size padding-validity checker.
- target-preserving condition: for each target exponent c one must have a source lower bound for some k satisfying c/k<1+epsilon on all sufficiently large padded lengths, with no advice depending on x beyond length.

## Assumptions

- Circuit model is nonuniform fan-in two Boolean circuits over total length-N functions.
- The lower bound is eventual over padded lengths N=n^k; an i.o. version gives only the corresponding i.o. contradiction.
- The exponent epsilon is independent of N and must remain positive after the padding overhead.
- The source claim is not a compressed-input SAT lower bound in disguise.

## Equations

- length_relation: `N=n^k,\quad R_k(x)=x1 0^{n^k-n-1}`. Valid when: Valid when k is fixed and padded lengths N=n^k are the only target lengths considered.
- upper_transfer: `C_{H_k}(N)\le aN+b\,C_{SAT}(N^{1/k})`. Valid when: Applies when the total padded language includes the O(N) off-image validity checker and constants are model-fixed.
- exponent_transfer: `C_{SAT}(n)=O(n^c)\Rightarrow C_{H_k}(N)=O(N^{\max\{1,c/k\}})`. Valid when: Requires the padding reduction to preserve nonuniform length parameters and circuit-size accounting without extra advice leakage.
- strict_margin: `\Delta=1+\epsilon-\max\{1,c/k\}>0\Rightarrow C_{H_k}(N)=O(N^{1+\epsilon-\Delta})<N^{1+\epsilon}\text{ eventually}`. Valid when: Valid when the exponent margin is strict, so asymptotic constants are absorbed for large padded lengths.
- uniform_k_consequence: `(\exists\epsilon>0)(\forall c)(\exists k>c/(1+\epsilon))\ C_{H_k}(N)>N^{1+\epsilon}\Rightarrow NP\nsubseteq P/poly`. Valid when: Valid only when the source lower bound is available for unbounded padding parameters, not one fixed k.

## Attempted Derivation

- Assume for contradiction that SAT has circuits of size O(n^c) for some fixed c.
- Choose k from the source hypothesis with c/k<1+epsilon.
- Construct a circuit for H_k on length N=n^k by checking the padding pattern in O(N) gates and running the SAT circuit on the first n=N^{1/k} bits.
- Obtain C_{H_k}(N)=O(N^{max{1,c/k}}).
- Since max{1,c/k}<1+epsilon, the upper bound is eventually below N^{1+epsilon}.
- Contradict the asserted source lower bound for H_k at that k.
- Because c was arbitrary only under the forall c exists k source quantifier, derive SAT notin P/poly conditionally.

Blocking gap: No known source theorem proves C_{H_k}(N)>N^{1+epsilon} for unbounded k with a common epsilon against general nonuniform circuits.

## Falsifiers

- falsifier: fixed k only yields a finite exponent ceiling c<k(1+epsilon), so arbitrary polynomial advice sizes survive.
- falsifier: threshold C_{H_k}(N)>N+N^{0.9} is absorbed by the O(N) padding checker and transfers no SAT exponent lower bound.
- falsifier: a lower bound for a compressed n-bit version of SAT merely restates the target and is not a valid source model.
- falsifier: if lower bounds hold for only finitely many k, every c above (1+epsilon) max k remains unaddressed.
- falsifier: a large constructive property proving the source lower bound against general circuits would meet the natural-proofs obstruction under standard PRF assumptions.

## Learning

Cycle 2 turns the previous threshold collapse into an exact quantifier repair. The valid route lemma is: fixed k gives only a finite SAT exponent lower bound, while a common-epsilon lower bound for unbounded padded carriers H_k would imply NP not subset P/poly. The decisive falsifier is not folklore but the inequality c/k>=1+epsilon, plus the O(N) checker floor.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Test MCSP or proof-complexity carriers for producing the unbounded-k source family: formalize whether a weak lower bound for MCSP[2^{N^{1/k}}] transfers to C_{H_k}(N)>N^{1+epsilon} without becoming natural or losing the strict exponent margin.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

A sound lower-bound template for the canonical NP-complete language K cannot both relativize uniformly and preserve the P-vs-NP target threshold. If it did, a proof of K notin P would transfer to K^O notin P^O for every oracle O, contradicting a BGS oracle A with P^A=NP^A.

## Definitions

- source object: a uniformly relativizing proof template T for deterministic oracle Turing-machine lower bounds on the canonical bounded oracle-NP complete language K^O, claiming K^emptyset notin DTIME(n^c) for all fixed c.
- target object: P != NP via K^emptyset notin P, with the oracle target family K^O notin P^O used only for the barrier audit.
- controlled interface: proposed lower-bound method -> relativization audit, formalized by an oracle-lift map L(T,O) preserving each inference, reduction, and machine simulation.
- target-preserving condition: if T proves the unrelativized polynomial-time lower bound, then L(T,O) proves the same fixed-exponent lower bound against DTIME^O(n^c) for every oracle O.

## Assumptions

- K^O is complete for NP^O under polynomial-time many-one reductions with oracle access to O.
- T is a sound finite or recursively enumerable proof template whose semantic inferences remain sound after replacing all machines by oracle machines.
- The oracle lift preserves the quantitative threshold union_c DTIME(n^c), allowing only fixed polynomial reindexing of exponents.
- There exists a Baker-Gill-Solovay oracle A such that P^A=NP^A.
- The conclusion is a route-level quarantine, not a proof of P != NP.

## Equations

- target_threshold: `K^{\emptyset}\notin \mathsf{P}=\bigcup_{c\ge 1}\mathsf{DTIME}(n^c)`. Valid when: Valid when K is the fixed NP-complete language and the intended target is a uniform polynomial-time lower bound.
- relativizing_transfer: `\mathsf{RelTP}(T)\wedge T\vdash K^{\emptyset}\notin\bigcup_c\mathsf{DTIME}(n^c)\Rightarrow \forall O\;K^O\notin\bigcup_c\mathsf{DTIME}^O(n^c)`. Valid when: Applies when every proof inference has a uniform oracle lift and preserves all fixed polynomial exponents.
- bgs_falsifier: `\exists A\;[\mathsf{P}^A=\mathsf{NP}^A]\Rightarrow K^A\in \mathsf{P}^A=\bigcup_c\mathsf{DTIME}^A(n^c)`. Valid when: Valid when K^A is chosen complete for NP^A under oracle polynomial-time reductions.
- quarantine_conclusion: `\mathsf{RelTP}(T)\Rightarrow \neg\bigl(T\text{ is a sound proof of }K^{\emptyset}\notin\mathsf{P}\bigr)`. Valid when: Requires the target-preserving complexity-class transfer and the BGS collapsing oracle in the same oracle convention.

## Attempted Derivation

- Type the source model as deterministic oracle Turing machines plus the canonical bounded NP^O-complete language K^O.
- Assume a sound proof template T has a uniform oracle lift L(T,O) preserving every inference and polynomial-time reduction.
- Under target preservation, a T-proof of K^emptyset notin union_c DTIME(n^c) becomes, for every oracle O, a proof of K^O notin union_c DTIME^O(n^c).
- Instantiate O by a Baker-Gill-Solovay collapsing oracle A with P^A=NP^A.
- Because K^A is NP^A-complete and P^A=NP^A, K^A lies in P^A, hence in DTIME^A(n^d) for some fixed d.
- This contradicts the transferred lower bound, so no sound route satisfying RelTP(T) can establish the target.

Blocking gap: The argument only blocks fully relativizing, target-preserving templates. It does not evaluate a route whose decisive step is nonrelativizing, non-natural, or non-algebrizing in a formally specified way.

## Falsifiers

- falsifier: exhibit a necessary proof step whose statement is not valid relative to arbitrary oracles.
- falsifier: show the route uses algebraic extension queries in a way that is nonrelativizing and then pass a separate algebrization audit.
- falsifier: demonstrate that the claimed lower bound is for a nonuniform or promise target that no longer transfers to K notin P.
- falsifier: quantify a threshold loss where K notin DTIME(n^c) transfers only to a subpolynomial or advice-bearing statement, not to P != NP.

## Learning

Cycle 2 converts the relativization barrier from folklore into a route-specific bridge lemma: RelTP(T) plus a K notin P proof would force K^O notin P^O for all O, but the BGS oracle A is a concrete falsifier. This is meaningful route-level progress: it certifies a class of proof objects as invalid while leaving P != NP untouched.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Instantiate an arithmetization-based proof object, such as a low-degree extension or PCP-style consistency test, and run the algebrization audit: specify oracle access, extension degree, reduction overhead, and whether a BGS/AW-style oracle remains a falsifier.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

If a uniform length-balanced many-one gap reduction from SAT to LowMCSP maps every no-instance to a truth table of circuit complexity at least N^epsilon, then canonical contradictions yield an explicit high-MCSP carrier and an i.o. E circuit lower bound of size 2^{epsilon' n} for every epsilon'<epsilon. This is route-level progress, not P != NP.

## Definitions

- source object: a deterministic polynomial-time reduction R that maps a 3CNF phi of length m to (x_phi,s_phi), where x_phi has length N_phi, and phi unsat implies CC(x_phi)>s_phi>=N_phi^epsilon.
- target object: an E-uniform language L whose length-n truth table equals a padded x_{psi_m} on infinitely many n, with CC(L_n)>2^{epsilon' n}.
- controlled interface: feed only canonical unsatisfiable formulas psi_m into R; use no MCSP oracle, no advice string, and no search over truth tables.
- target-preserving condition: the output lengths are unbounded and length-balanced, m<=N_phi^k, and padding from N_phi to a power of two loses only o(N_phi^{epsilon'}).

## Assumptions

- R is uniform and runs in m^{O(1)} time.
- There is a fixed epsilon>0 with no-side gap s_phi>=N_phi^epsilon.
- For infinitely many canonical contradictions psi_m, N_{psi_m} tends to infinity and m<=N_{psi_m}^k.
- Circuit size is measured for Boolean circuits computing the truth table function; padding overhead is O(log N).

## Equations

- threshold-transfer: `s_m \ge N_m^{\epsilon} \ge (2^{n_m})^{\epsilon'} = 2^{\epsilon' n_m}`. Valid when: Valid when n_m=ceil(log N_m), epsilon'<epsilon, and padding changes length by less than a factor two.
- uniform-output-time: `T_A(n_m) \le m^{O(1)} \le N_m^{O(k)} = 2^{O(n_m)}`. Valid when: Valid when the reduction is length-balanced on the canonical contradiction family and no nonuniform advice is used.
- lower-bound-instance: `CC(L_{n_m}) > 2^{\epsilon' n_m} - O(n_m)`. Valid when: Applies after the padded truth table still restricts to the original high-MCSP string with only comparator overhead.

## Attempted Derivation

- Start with the stronger-than-folklore source model: a length-balanced gap Karp reduction R from SAT to LowMCSP with no-instances mapped to CC>N^epsilon.
- Choose a canonical unsatisfiable 3CNF family psi_m, e.g. z AND not z padded to length m, so the SAT answer is known without solving SAT.
- Compute R(psi_m)=(x_m,s_m). By correctness, x_m is high-complexity on the no side; no MCSP decision procedure is invoked.
- Use length balance m<=N_m^k to output x_m in poly(N_m) time, hence in E after interpreting x_m as a truth table.
- Pad to the next power of two and lose only O(log N_m) gates when restricting a small circuit for the padded function back to x_m.
- Conclude an i.o. E lower bound CC(L_n)>2^{epsilon' n} on the image lengths for every epsilon'<epsilon.

Blocking gap: No known SAT-to-MCSP reduction supplies a no-side gap s>=N^epsilon with uniform length balance. Ordinary MCSP-hardness conjectures, Turing reductions, or reductions with tiny thresholds do not provide this carrier.

## Falsifiers

- falsifier: the reduction outputs N_m much smaller than m^{c}, so computing the carrier costs super-polynomial time in its truth-table length.
- falsifier: the no-side MCSP threshold is logarithmic, polylogarithmic, or otherwise below N^epsilon, causing quantitative threshold collapse.
- falsifier: the construction needs advice to choose the hard MCSP instance, so the target becomes nonuniform and the IW transfer is not valid.
- falsifier: the reduction is a Turing reduction whose accepting path depends on unknown SAT answers, so a fixed contradiction does not expose a single high truth table.
- falsifier: the output is an MCSP yes-instance on contradictions under the chosen convention; then it certifies low complexity rather than high complexity.

## Learning

The repair isolates a concrete bridge: co-side gap reductions to MCSP are not just hardness evidence; with length balance and threshold N^epsilon they automatically manufacture explicit E lower bounds. Thus the route's main obstruction is quantitative source strength, not extraction. This also explains why weak MCSP reductions and nonuniform selectors are invalid for the target.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Audit known MCSP-hardness constructions for the exact tuple (many-one, no-side high, s>=N^epsilon, N between m^a and m^b, no advice); reject or record the first valid tuple.
