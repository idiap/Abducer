# cycle-0015

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Generated-OR polylog bridge with lookup safety: if H_N^{G,q,L} has i.o. SIZE(N^{1+epsilon}) lower bounds, max{rho,q}<1+epsilon, and the lookup falsifier is avoided, then SAT is not in P/poly.

## Definitions

- source object: H_N^{G,q,L} on x in {0,1}^N, the OR of N^q generated SAT instances of length L(N)=A(log N)^d.
- target object: SAT notin P/poly, equivalently NP not subset P/poly for the standard complete language.
- controlled interface: compose a single SAT circuit for length L(N) with a uniform generator G_N of size N^rho and an N^q-way OR.
- target-preserving condition: max{rho,q}<1+epsilon and no subthreshold lookup/advice circuit computes SAT on the generated length universe.
- source lower-bound model: nonuniform Boolean circuits SIZE(s) over N input bits, with an infinitely-often lower bound s>N^{1+epsilon}.
- valid length regime: L(N)=A(log_2 N)^d with constants A>0 and d>0; the generator has no satisfiability advice.

## Assumptions

- G_N is P-uniform or DLOGTIME-uniform, has size N^rho, and outputs N^q well-formed formulas of length L(N).
- SAT in P/poly means there is one length-L circuit S_L of size L^c, reused for every generated query at that length.
- The OR fan-in N^q and wiring overhead are charged inside SIZE(N^{q+o(1)}).
- The lower-bound proof for H_N is not allowed to hardwire the SAT truth table or leak nonuniform query answers.

## Equations

- carrier: `H_N(x)=\bigvee_{i\le N^q}\mathrm{SAT}(G_{N,i}(x)),\qquad |G_{N,i}(x)|=L(N)=A(\log_2 N)^d`. Valid when: Valid when G_N is a uniform generator whose outputs are well-formed SAT encodings of length L(N).
- sat_substitution_upper: `\mathrm{SAT}\in \mathrm{SIZE}(n^c)\Rightarrow C(H_N)\le N^\rho+N^qL(N)^c+O(N^q)=N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies after the assumed SAT circuit is length-uniform nonuniform advice for exactly L(N)-bit formulas.
- lookup_audit: `C_{\mathrm{lookup}}(H_N)\le N^\rho+N^q2^{L(N)},\quad \lambda(N)=\log_N2^{L(N)}=A(\log_2N)^{d-1}`. Valid when: Requires the lookup audit to be compared with the same N^{1+epsilon} source threshold.

## Attempted Derivation

- Fix G_N of size N^rho producing m=N^q SAT queries of length L=A(log N)^d and define H_N as their OR.
- Assume SAT has circuits of size n^c. Substitute the length-L circuit S_L into every query and add the generator plus OR overhead.
- Since L^c=N^{o(1)}, the composed circuit has size N^{max{rho,q}+o(1)}, contradicting any i.o. H_N lower bound above N^{1+epsilon} when max{rho,q}<1+epsilon.
- Audit the independent lookup circuit for SAT_L. It is subthreshold exactly when q+A(log N)^{d-1}<1+epsilon eventually, producing a source-level falsifier.

Blocking gap: No explicit no-advice generator G_N is known for which H_N has an i.o. N^{1+epsilon} general-circuit lower bound by a non-natural method.

## Falsifiers

- Lookup falsifier: if d<1, or d=1 with q+A<1+epsilon, the table for SAT_L gives C(H_N)<N^{1+epsilon} and the source premise is impossible.
- Threshold falsifier: if rho>=1+epsilon or q>=1+epsilon, SAT-substitution no longer yields a contradiction to the H_N lower bound.
- Advice-leakage falsifier: if G_N or the lower-bound proof embeds satisfiability bits for the generated query set, the target-preserving interface to SAT in P/poly is invalid.
- Natural-proof falsifier: if the H_N lower bound is obtained via a large constructive property useful against SIZE(N^{1+epsilon}), standard PRF assumptions block it for general circuits.

## Learning

Cycle 15 adds the exact lookup boundary. Polylog queries always preserve all SAT polynomial exponents in the substitution term, but source plausibility requires q+A(log N)^{d-1} not fall below 1+epsilon. Thus d<1 is quarantined, d=1 has a sharp constant window, and d>1 is safely valid from lookup.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and threshold selector.`
- Rationale: The transfer algebra is settled; the open choice is whether the carrier survives unconditional lookup while still allowing SAT-circuit substitution.
- Situation seed: For fixed epsilon,q,rho,A, study H_N^d=OR_{i<=N^q} SAT(G_{N,i}(x)) with query length L=A(log_2 N)^d and a uniform size-N^rho generator.
- Varied variable: d, the polylogarithmic query-length exponent.
- Held-fixed controls: max{rho,q}<1+epsilon is held fixed., G_N remains uniform and carries no SAT advice., The same length-L SAT circuit is reused for every query., The source lower bound remains an i.o. general-circuit lower bound for H_N.
- Expected observation: d<1 is invalid by lookup; d=1 has the sharp boundary q+A>=1+epsilon; d>1 is lookup-safe and still gives N^{max{rho,q}+o(1)} under SAT in P/poly.
- Transfer certificate needed: A valid certificate must include an explicit generator, no nonuniform leakage, a non-natural H_N lower-bound proof, and the inequality max{rho,q}<1+epsilon.

## Next Experiment

Instantiate the boundary cases d=1 with A=1+epsilon-q and d=2; search for a generator whose H_N avoids known small-circuit constructions without smuggling SAT advice.

# Cycle 15: Public-coin local separators naturalize after global-seed soundness

## Candidate Lemma

A public-coin local truth-table separator with logarithmic query and witness lengths is still a natural-proof object if its soundness is small enough to union-bound over all target small circuits. Randomness is not a barrier escape unless the route refuses the global-seed certificate or loses constructivity.

## Definitions

- source object: a public-coin local verifier V^{f}(rho,w) for a target truth table K_N, with random seed rho in {0,1}^R, existential transcript w in {0,1}^A, and at most q adaptive queries to f in {0,1}^N.
- target object: a Razborov-Rudich style property P_N over N-bit truth tables useful against SIZE(s) circuits, where s=m^k and N=2^m for the audited Boolean-function model.
- controlled interface: choose one public seed rho* after a union bound over all size-s circuits, then define P_{rho*}(f)=1 iff there exists w with V^{f}(rho*,w)=1.
- target-preserving condition: completeness gives Pr_rho[exists w V^{K_N}(rho,w)=1] >= gamma, soundness gives for every size-s circuit C that Pr_rho[exists w V^{tt(C)}(rho,w)=1] <= epsilon, and gamma exceeds the circuit-count union-bound loss.

## Assumptions

- The target circuit class is nonuniform Boolean circuits of size at most s=m^k on m inputs, with truth-table length N=2^m.
- The verifier is deterministic once rho,w and oracle answers are fixed; adaptive queries depend only on the previous local transcript.
- The random seed rho* may be hardwired into the property description without exceeding the allowed poly(N)-time constructivity budget.
- Completeness is for the intended hard truth table K_N, not merely for some promise object unrelated to the target lower bound.
- Soundness is universal over all size-s circuits and all existential transcripts w.

## Equations

- circuit_count: `M(s,m) \le 2^{O(s\log s)} = 2^{O(m^k\log m)}`. Valid when: Valid when the target class is ordinary fan-in two Boolean circuits encoded gate-by-gate on m input variables.
- global_seed_threshold: `\gamma > M(s,m)\epsilon`. Valid when: Applies after soundness is measured per fixed circuit but before choosing a single public seed for all circuits.
- natural_density: `\mu(P_{\rho^*}) \ge 2^{-q}`. Valid when: Requires an accepting transcript for K_N under rho* and at most q deterministic adaptive oracle queries along that accepting path.
- constructivity_budget: `T_{P}(N) \le 2^A \cdot \operatorname{poly}(N,R,|V|)`. Valid when: Valid when the property algorithm receives the full truth table and enumerates all existential transcripts for the fixed seed.
- log_threshold: `A=O(\log N),\ q=O(\log N) \Rightarrow T_P(N)=\operatorname{poly}(N),\ \mu(P_{\rho^*})\ge N^{-O(1)}`. Valid when: Applies when witness length and query complexity are logarithmic in the truth-table length rather than in the original input length.

## Attempted Derivation

- Let T={rho: exists w V^{K_N}(rho,w)=1}; completeness gives |T|/2^R >= gamma.
- For every size-s circuit C, let B_C={rho: exists w V^{tt(C)}(rho,w)=1}; soundness gives |B_C|/2^R <= epsilon.
- The number of such circuits is M(s,m)<=2^{O(s log s)}. Hence |union_C B_C|/2^R <= M(s,m)epsilon.
- If gamma > M(s,m)epsilon, choose rho* in T \ union_C B_C.
- Define P_{rho*}(f)=1 iff exists w V^f(rho*,w)=1. Then K_N is in P_{rho*}, and no size-s circuit truth table is in P_{rho*}.
- Since K_N has an accepting transcript w*, the accepting adaptive path fixes at most q queried bits. All truth tables agreeing with K_N on those bits are accepted, so density is at least 2^{-q}.
- If A=O(log N), exhaustive enumeration of w gives a poly(N)-time constructive property; if q=O(log N), the density is polynomially large.

Blocking gap: The derivation needs exponentially small soundness epsilon < gamma/2^{O(s log s)} or an equivalent hitting-seed certificate. Standard constant-error AM soundness is insufficient.

## Falsifiers

- falsifier: constant per-circuit soundness lets bad seed sets for exponentially many small circuits cover every public seed, so no useful fixed-seed property follows.
- falsifier: A=omega(log N) can destroy poly(N) constructivity even if a good seed exists.
- falsifier: q=omega(log N) can make the accepting cylinder exponentially small, outside the standard largeness threshold.
- falsifier: if rho* requires superpolynomial advice to find and cannot be hardwired within the accepted property model, the transfer loses explicitness.
- falsifier: if soundness quantifies only against honest provers rather than all transcripts for small circuits, P_{rho*} may accept easy truth tables.

## Learning

Cycle 15 isolates the public-randomness threshold for local separator routes. Random coins are not automatically a natural-proof escape: if soundness is exponentially small enough to beat the 2^{O(s log s)} circuit count, one seed makes an existential local property useful, large, and poly(N)-constructive. Constant soundness is the precise falsifier to this transfer. This is valid route-level barrier progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and threshold calculator.`
- Rationale: The branch has already naturalized deterministic, advised, randomized-local, and short-Merlin certificates. The remaining plausible escape is public randomness; a concrete seed-fixing experiment decides whether randomness changes the barrier status or only adds a union-bound threshold.
- Situation seed: Consider an AM-local separator for the SAT_m truth table of length N=2^m. The verifier uses public seed rho, an existential transcript w, and q adaptive truth-table queries. It claims to reject every SIZE(m^k) truth table with small error.
- Varied variable: The varied parameter is the soundness exponent alpha in epsilon=2^{-alpha m^k log m}.
- Held-fixed controls: Target class remains nonuniform SIZE(m^k) on m inputs., Query bound is q=c log N and witness length is A=c' log N., Completeness gamma is fixed at 2/3 for the SAT_m truth table., The property may hardwire one seed rho* but must remain decidable in poly(N) time.
- Expected observation: There is a threshold near alpha larger than the circuit-count constant. Above it, a global seed exists and the protocol yields a valid natural property of density N^{-O(1)}. Below it, constant or weak soundness gives no useful seed and public randomness is not yet barrier-classified.
- Transfer certificate needed: A formal amplification or hitting-seed lemma proving gamma > M(s,m)epsilon while preserving q=O(log N), A=O(log N), target class SIZE(m^k), and poly(N) constructivity.

## Next Experiment

Audit whether parallel repetition or error reduction for public-coin local truth-table separators can reduce epsilon below 2^{-O(s log s)} without increasing q or A beyond O(log N); if not, quarantine AM-local certificates as constant-error non-naturalized objects rather than barrier escapes.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Restart leakage lemma: a sequential MCSP no-side carrier with a subepsilon uniform restart map has small circuits for its own streamed truth table. Thus a valid threshold-epsilon source must be globally sequential and anti-restartable, not merely lacking direct random access.

## Definitions

- source object: sequential certificates c_m of length O(m) for a verifier V_m that streams a truth table T_m in time 2^{O(m)} and is sound for C(T_m)>2^{epsilon m}.
- target object: an E language L_T obtained by uniform search over kappa-dense source lengths, aiming for L_T notin SIZE(2^{delta n}) for every delta<epsilon/kappa.
- controlled interface: MCSP no-side soundness at threshold N^epsilon with N=2^m, plus E-time extraction that only reads sequential streams and never receives nonuniform selectors.
- target-preserving condition: any restart, checkpoint, address, or selector mechanism must be uniform and counted in the bit-circuit size; subepsilon leakage is an invalid transfer.

## Assumptions

- For infinitely or kappa-densely many m, V_m accepts c_m and emits T_m with |T_m|=2^m.
- A restart map R_m(c,j) returns the exact verifier state at boundary jB, where B=2^{alpha m}.
- R_m has uniform circuits or time 2^{sigma m+o(m)} after hardwiring the O(m)-bit certificate.
- The accepted-source property is sparse/non-large; a dense constructive version triggers the natural-proofs falsifier.

## Equations

- restart_upper_bound: `C(T_m) \le 2^{\max\{\alpha,\sigma\}m+o(m)}`. Valid when: Valid when R_m returns exact verifier states and the per-output update has polynomial overhead.
- soundness_constraint: `\max\{\alpha,\sigma\} \ge \epsilon-o(1)`. Valid when: Requires accepted streams to be sound MCSP no-side witnesses at threshold 2^{epsilon m}.
- carrier_transfer: `\delta < \epsilon/\kappa`. Valid when: Applies after source lengths are kappa-dense and extraction preserves E-uniformity without advice.

## Attempted Derivation

- Fix accepted c_m and block size B=2^{alpha m}; on input x in {0,1}^m compute index i, boundary j=floor(i/B), and offset r.
- Use R_m(c_m,j) to obtain the verifier state at time jB with circuit size 2^{sigma m+o(m)}; hardwiring c_m costs only O(m).
- Unroll the deterministic streaming update for r<B steps and output bit i, giving size 2^{max(alpha,sigma)m+o(m)}.
- If max(alpha,sigma)<epsilon-o(1), this contradicts MCSP no-side soundness C(T_m)>2^{epsilon m}; hence valid sources must defeat all such restarts.

Blocking gap: No construction is known for a sparse sound source whose verifier state is provably impossible to restart below exponent epsilon without already proving a circuit lower bound.

## Falsifiers

- falsifier: a uniform restart/checkpoint algorithm with exponent sigma and spacing alpha satisfying max(alpha,sigma)<epsilon gives subthreshold circuits for T_m.
- falsifier: nonuniform checkpoint advice of total size 2^{theta m} with max(theta,alpha)<epsilon leaks the target circuit and breaks MCSP soundness.
- falsifier: brute-force enumeration of circuits only certifies s=O(m/log m), so epsilon_m=O(log m/m) and the transfer collapses to delta=o(1).
- falsifier: a dense constructive recognizer for acceptable streams is a natural-proofs obstruction; the route must stay sparse/non-large and nonuniform-free.

## Learning

Cycle 15 adds a precise restart-leakage threshold: sequential-only is insufficient. A valid constant-threshold MCSP source must be anti-restartable against every uniform checkpoint mechanism below 2^{epsilon m-o(m)}. This is a source-side obstruction, not progress on P != NP itself.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The branch must distinguish true sequential hardness from hidden restartability; another abstract MCSP-carrier restatement would not test the remaining source obstruction.
- Situation seed: Checkpointed sequential MCSP certificate family: V_m(c_m) streams T_m, and an optional module R_beta tries to return verifier states at boundaries of length B=2^{beta m}.
- Varied variable: checkpoint spacing exponent beta
- Held-fixed controls: MCSP no-side threshold C(T_m)>2^{epsilon m}, certificate length O(m) and deterministic verifier time 2^{O(m)}, kappa-dense source lengths for E extraction, no nonuniform advice, selector, or external truth table oracle
- Expected observation: If beta and restart-cost exponent are both below epsilon, the induced bit circuit violates soundness; a valid source must force beta or restart cost to reach epsilon-o(1).
- Transfer certificate needed: A formal simulation proving R_beta is uniform and exact, and that all checkpoint data are counted in the circuit bound before the intuition affects proof obligations.

## Next Experiment

Test proof-transcript carriers where a restart state would compress a long dependency chain; formalize whether such compression implies a small circuit for T_m or merely a proof-complexity lower bound.
