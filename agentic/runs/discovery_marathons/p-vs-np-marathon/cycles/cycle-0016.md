# cycle-0016

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Entropy-gated generated-OR bridge: if an explicit target-clean carrier H_N=OR of N^q SAT queries of length L=(log N)^d has generator size N^rho, q,rho<1+epsilon, and H_N requires SIZE(N^{1+epsilon}) on infinitely many N, then SAT notin P/poly. The source is valid only past the variable-enumeration falsifier.

## Definitions

- source object: H_N:{0,1}^N->{0,1}, H_N(x)=OR_{i<=N^q} SAT(Phi_i(x)), with compact uniform generator G_N for the formulas.
- target object: SAT on inputs of length n against nonuniform polynomial-size Boolean circuits, yielding SAT notin P/poly as the target consequence.
- controlled interface: replace each SAT query of length L=(log N)^d by a size L^c circuit, while paying N^rho for G_N and N^q query fanout.
- target-preserving condition: G_N uses no SAT-truth-table advice, queries are genuine SAT instances, q and rho are fixed below 1+epsilon, and the lower bound is against unrestricted nonuniform circuits for H_N.
- variable entropy: v(N) is the maximum number of Boolean variables occurring in any generated formula Phi_i(x); brute force costs 2^{v(N)}, not 2^L.

## Assumptions

- The source lower bound is SIZE(H_N)>N^{1+epsilon} for infinitely many valid input lengths N.
- For every fixed c, SAT in SIZE(n^c) supplies circuits for all generated length-L instances.
- Uniformity of G_N is strong enough to build the H_N circuit without hidden nonuniform advice.
- The entropy gate requires liminf_N (q+v(N)/log_2 N) >= 1+epsilon or else the source lower bound is unconditionally falsified.

## Equations

- carrier_definition: `H_N(x)=\bigvee_{i=1}^{M} SAT(\Phi_i(x)),\quad M=N^q,\quad |\Phi_i(x)|\le L=(\log N)^d`. Valid when: Valid when the compact generator computes each queried SAT instance uniformly without embedding SAT advice.
- sat_substitution_upper_bound: `SAT\in SIZE(n^c)\Rightarrow SIZE(H_N)\le N^{\rho}+N^q L^c\,polylog(N)=N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies after the reduction preserves nonuniform target circuits and q,rho are constants independent of c.
- variable_enumeration_falsifier: `SIZE(H_N)\le N^{\rho}+N^q2^{v(N)}poly(L)=N^{\max\{\rho,q+v(N)/\log_2N\}+o(1)}`. Valid when: Valid when generated formulas have at most v(N) variables and deterministic exhaustive assignment evaluation is allowed.

## Attempted Derivation

- Fix H_N with M=N^q generated SAT queries, length L=(log N)^d, generator cost N^rho, and max{q,rho}<1+epsilon.
- Assume SAT has circuits of size n^c. Substitute the length-L SAT circuit into every query; since L^c=N^{o(1)}, H_N has size N^{max{q,rho}+o(1)}.
- For large valid N this contradicts SIZE(H_N)>N^{1+epsilon}; hence the bridge would imply SAT notin P/poly, not merely a weak restatement of P vs NP.
- Audit the source: independent of SAT circuits, each query can be solved by enumerating v(N) variables, so the lower bound is impossible below the threshold q+v(N)/log_2 N >= 1+epsilon.

Blocking gap: No explicit target-clean generator is known whose OR carrier has a non-natural unrestricted N^{1+epsilon} circuit lower bound while also passing the variable-entropy gate.

## Falsifiers

- Entropy falsifier: if generated formulas use only v(N)<(1+epsilon-q-eta)log_2 N variables, exhaustive assignment gives subthreshold circuits for H_N.
- Advice-leakage falsifier: if G_N encodes SAT truth bits or hard functions as nonuniform advice, the transfer no longer certifies SAT notin P/poly.
- Sparsity falsifier: if the query family lands in an easy SAT fragment or repeats N^{o(1)} essential formulas, H_N may have circuits below N^{1+epsilon}.
- Naturality falsifier: a large constructive property proving the H_N lower bound would collide with standard PRG-based natural-proofs barriers unless the proof is non-natural or outside their scope.

## Learning

Cycle 16 sharpens the generated-OR route: the valid transfer to SAT notin P/poly needs only q,rho<1+epsilon, but source plausibility additionally requires variable entropy q+v/log N at least 1+epsilon. The old 2^L lookup audit was too weak; the real falsifier is low variable count.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The previous lookup boundary used encoding length L; the decisive concrete parameter is variable entropy v(N), because SAT enumeration depends on variables, not bits of encoding.
- Situation seed: Take H_N as OR of N^q uniformly generated 3CNF formulas of encoding length (log N)^d, generator size N^rho, and exactly v(N) variables per query.
- Varied variable: Set v(N)=A log_2 N and vary A, then compare with v(N)=(log N)^d for d>1.
- Held-fixed controls: q,rho<1+epsilon are fixed throughout the experiment., The generator is uniform, compact, and contains no SAT-truth-table advice., The target substitution uses arbitrary P/poly circuits for SAT of length L., The source lower bound is against unrestricted nonuniform circuits for H_N.
- Expected observation: For A<=1+epsilon-q the source lower bound is killed by brute force; for superlogarithmic v(N) the enumeration falsifier disappears while SAT-circuit substitution remains N^{max{q,rho}+o(1)}.
- Transfer certificate needed: A formal no-leakage and high-essential-variable certificate for G_N, plus an explicit non-natural lower-bound method for H_N before the intuition enters the proof queue.

## Next Experiment

Instantiate G_N with high-essential-variable polylog 3CNF queries and test whether any structural simplification gives SIZE(H_N)<=N^{1+epsilon-o(1)} despite v(N) superlogarithmic.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

A deterministic adaptive q-query truth-table separator for SAT_N versus SIZE(n^k) yields a Razborov-Rudich natural property when q=O(log N). Adaptivity only selects an accepting leaf; it does not by itself escape the natural-proof falsifier.

## Definitions

- source object: a uniform deterministic adaptive oracle verifier V^y(1^N) querying at most q(N) bits of a length-N truth table y, accepting the SAT_N truth table tau_N, and rejecting every SIZE(n^k) truth table.
- target object: a poly(N)-constructive property P_N of Boolean functions on n bits, with density at least 1/poly(N), useful against SIZE(n^k).
- controlled interface: record the accepting adaptive transcript L of V on tau_N and define P_N as all truth tables that follow L and reach the same accepting leaf.
- target-preserving condition: tau_N query answers and the transcript L are computable in poly(N), V has no superpolynomial hidden advice, and soundness is universal over all small circuits.

## Assumptions

- N=2^n and circuit size is measured on n-bit Boolean functions.
- SAT_N is explicit enough that each queried bit of tau_N is decidable in N^{O(1)} time.
- V's next-query rule is computable in poly(N), including adaptive branching.
- For every circuit C of size n^k, V^{tt(C)}(1^N) rejects.

## Equations

- leaf_density: `\mu(P_N)=2^{-|L|}\ge 2^{-q(N)}`. Valid when: Valid when the accepting transcript fixes only distinct queried truth-table bits and all unqueried coordinates remain unrestricted.
- natural_threshold: `q(N)\le c\log N \Rightarrow \mu(P_N)\ge N^{-c}`. Valid when: Applies when the query bound is logarithmic in truth-table length and density is measured over all N-bit truth tables.
- prf_distinguisher_advantage: `\operatorname{Adv}(D)\ge \mu(P_N)\ge 2^{-q(N)}`. Valid when: Requires every keyed PRF truth table to lie in SIZE(n^k) and P_N to reject all such circuit truth tables.

## Attempted Derivation

- Run V on tau_N and compute the unique accepting transcript L=(i_1,b_1,...,i_t,b_t), t<=q(N), using brute-force SAT answers in poly(N) time.
- Define P_N(y)=1 iff V^y follows transcript L and accepts; membership simulates V and checks the t fixed oracle answers.
- The set P_N is an accepting cylinder of co-dimension t, hence has density 2^{-t} and is large when q=O(log N).
- Universal soundness gives P_N(tt(C))=0 for every SIZE(n^k) circuit C, so P_N is useful; PRF existence in that class makes this a natural-proof obstruction.

Blocking gap: The lemma audits only deterministic adaptive certificates with computable SAT transcripts. Randomized, interactive, or superlog-query variants need separate seed and density accounting.

## Falsifiers

- falsifier: q=N^{0.01} gives density 2^{-N^{0.01}}, below polynomial largeness, so this naturalization gate no longer applies.
- falsifier: a nonexplicit target truth table whose queried bits are not decidable in poly(N) destroys constructivity of P_N.
- falsifier: hidden N^{0.1}-bit advice selecting L avoids uniform constructivity unless an anti-leakage certificate is supplied.
- falsifier: soundness only against a sampled circuit family is insufficient; usefulness needs rejection of every SIZE(n^k) truth table.

## Learning

Cycle 16 proves a route-specific bridge: deterministic adaptive log-query SAT separators naturalize via their accepting leaf. The valid escape threshold is not adaptivity but superlogarithmic query complexity, nonconstructive transcript selection, or weakened soundness.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: Adaptivity is a common claimed escape after log-query naturalization. A concrete padded-SAT adaptive decision tree tests whether the escape changes density or merely hides an accepting leaf.
- Situation seed: For each N=2^n, imagine a uniform adaptive oracle verifier V for the SAT_N truth table that makes q alpha log N queries and rejects every n^k-size circuit truth table.
- Varied variable: alpha in q=alpha log N, crossing from polynomial density to subpolynomial density when q grows beyond O(log N).
- Held-fixed controls: target language is SAT_N and queried SAT bits are computable in N^{O(1)} time, soundness is universal over all SIZE(n^k) truth tables, no advice beyond the uniform verifier description, target consequence is only a natural-proof audit, not P != NP
- Expected observation: For constant alpha, the accepting adaptive path has density N^{-alpha}; adaptivity changes which coordinates are fixed but not the largeness calculation.
- Transfer certificate needed: A formal transcript-recovery proof in poly(N) time and a soundness statement quantified over all small circuits before the intuition is valid for the proof queue.

## Next Experiment

Audit private-coin interactive local separators: quantify when prover messages plus verifier coins collapse to a large existential cylinder and when seed elimination exceeds poly(N) constructivity.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

A purported sequential MCSP no-side source at threshold 2^{epsilon m} is invalid if its accepted stream admits a subthreshold indexable restart interface. The interface itself yields a circuit for the emitted truth-table function, so it is a source-side falsifier, not progress toward the main P != NP target.

## Definitions

- source object: a uniform sequential MCSP no-side certificate source S that on length m emits a truth table T_m of length 2^m and claims every accepted T_m has circuit complexity greater than 2^{epsilon m}.
- target object: an E-uniform language obtained from kappa-dense accepted truth tables, with the already established transfer giving circuit lower-bound exponent delta<epsilon/kappa when the source is sound.
- controlled interface: a restart map J_m(x) plus replay procedure that reconstructs the generator state within L_m positions of truth-table index x using circuit cost R_m and per-step replay cost u_m.
- target-preserving condition: J_m is uniform or E-computable, uses no hidden nonuniform advice beyond the certified object, and satisfies R_m+L_m u_m<2^{epsilon m-o(m)} only when used as a falsifier of source soundness.

## Assumptions

- For each accepted certificate c_m, the stream generator is deterministic and outputs T_m in lexicographic index order.
- J_m on input x returns a correct reachable state preceding x by at most L_m stream steps.
- The circuit cost R_m includes hardwiring the O(m)-bit certificate and implementing the restart computation.
- MCSP no-side soundness quantifies against all Boolean circuits of size at most 2^{epsilon m}, including nonuniform circuits built from the certificate.

## Equations

- restart_circuit_upper_bound: `size(f_m) <= O(R_m + L_m u_m + poly(m))`. Valid when: Valid when J_m maps each input index to a correct reachable state and replay is deterministic without hidden advice.
- subthreshold_restart_contradiction: `R_m + L_m u_m <= 2^{epsilon m - omega(log m)} => size(f_m) < 2^{epsilon m}`. Valid when: Applies when the simulation overhead is absorbed by slack below the claimed MCSP no-side threshold.

## Attempted Derivation

- Assume an accepted sequential certificate emits T_m with claimed complexity greater than 2^{epsilon m}.
- Place checkpoints every L_m=2^{alpha m} positions in the stream and hardwire every checkpoint state into a circuit for the table function f_m.
- On input x, select the checkpoint for x, replay at most L_m steps, and output the indexed bit.
- Obtain size(f_m)<=2^{max(alpha,1-alpha)m+o(m)} when state and step costs are subexponential.
- Compare this upper bound with the claimed threshold 2^{epsilon m}.

Blocking gap: The argument refutes the source only when max(alpha,1-alpha)<epsilon. For epsilon<=1/2 no evenly spaced checkpoint array is subthreshold, so banning all restartability is quantitatively false.

## Falsifiers

- Subthreshold indexable restart map J_m with R_m+L_m u_m <= 2^{epsilon m-o(m)}.
- Locally decodable certificate or commitment with P_m+Q_m <= 2^{epsilon m-o(m)}.
- Checkpoint array with exponent max(alpha,1-alpha)<epsilon and subexponential state and step costs.
- Dense polynomial-time decidable table property that is large enough to trigger the natural-proofs obstruction under standard pseudorandom-function assumptions.
- Any extraction that uses advice depending on T_m beyond the O(m)-bit certified object, making the consequence only nonuniform.

## Learning

Cycle 16 narrows the source-side obstruction. Sequential restartability is not itself a falsifier; only subthreshold indexed restart, short local decoding, or a checkpoint storage/replay tradeoff below 2^{epsilon m} invalidates the MCSP no-side claim. This keeps the route non-large and outside the immediate natural-proofs barrier, while preserving the valid carrier-to-E transfer as route-level progress only.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for restart-based source repairs.`
- Rationale: The branch has a valid MCSP-to-E transfer, but the source obstruction is now quantitative restart leakage. A concrete checkpoint experiment separates fatal compressed access from harmless coarse sequential structure.
- Situation seed: Consider a family C_{m,alpha} of sequential MCSP certificates whose generator emits a length-2^m truth table and stores reachable checkpoints every 2^{alpha m} bits; compare an explicit checkpoint array with a compressed jump-to-block restart map.
- Varied variable: checkpoint spacing exponent alpha in L_m=2^{alpha m}.
- Held-fixed controls: MCSP no-side threshold s_m=2^{epsilon m} with constant epsilon., O(m)-bit primary certificate and deterministic E-time verifier., kappa-dense source lengths for the established E lower-bound transfer., No hidden advice and no local decoder for T_m except the tested restart interface.
- Expected observation: Explicit checkpoint arrays leak circuits of size 2^{max(alpha,1-alpha)m+o(m)}, while compressed jump maps leak size R_m+2^{alpha m}u_m. The route should reject only interfaces below 2^{epsilon m-o(m)}.
- Transfer certificate needed: A formal proof that any accepted source either has restart cost at least 2^{epsilon m-o(m)} for every indexable jump interface, or else is quarantined as an invalid MCSP no-side carrier before invoking the density transfer.

## Next Experiment

Formalize a one-way streaming transcript source based on pebbling or communication bottlenecks; vary memory exponent and prove whether any jump-to-index restart map below 2^{epsilon m-o(m)} would imply a small circuit for the transcript bits.
