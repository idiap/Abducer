# cycle-0058

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-magnification bridge via XOR carriers and sparse quotient-polynomial falsifiers

## Candidate Lemma

For the high-q XOR-SAT carrier, any charged sparse polynomial over SAT-blind quotient features gives a concrete upper-bound falsifier for the desired barely-superlinear source lower bound. The prior low-degree audit is valid only after replacing degree by monomial-support cost, because high-degree sparse combiners can still be subthreshold.

## Definitions

- source object: H_N:{0,1}^N -> {0,1}, H_N(x)=xor_{j<=M_N} SAT(F_{N,j}(x)), with M_N=N^q and formula length L_N=(log N)^d.
- target object: nonuniform Boolean circuits for SAT_n; the target consequence is SAT notin SIZE(n^c) for every fixed c, hence NP not subset P/poly under the usual encoding.
- controlled interface: substitute an assumed SAT circuit of size L_N^c into every generated query and charge the generator, query fanout, and final XOR explicitly.
- target-preserving condition: L_N=(log N)^d, d>1, max{rho,q}<1+epsilon, no target advice is hidden in the generator beyond the fixed nonuniform carrier family.
- SAT-preserving quotient: a partition U_N of generated formulas into blocks with a well-defined SAT label a_u, while I_{N,u}(x) records the parity of positions whose generated formula falls in block u.
- charged quotient feature: T_N:{0,1}^N -> {0,1}^{r_N} has total circuit cost S_T and is charged separately from the final polynomial; allowing an uncharged H_N feature would make the audit tautological.

## Assumptions

- Source lower-bound model is general nonuniform Boolean circuit size C(H_N), with the desired threshold C(H_N)>N^{1+epsilon-o(1)}.
- Generator cost is C(G_N)<=N^{rho+o(1)} and all generated formulas have length L_N=(log N)^d.
- The sparse sketch has P_N(z)=xor_{A in M_N^*} prod_{i in A} z_i over F_2 with support size A_N=|M_N^*|.
- The sketch may be wrong on at most E_N inputs, and those exceptions are patched by equality circuits at cost O(E_N N).

## Equations

- quotient-inner-product-normal-form: `H_N(x)=\bigoplus_{u\in U_N} a_u I_{N,u}(x)=\langle a_N,I_N(x)\rangle_{\mathbb F_2}.`. Valid when: Valid when U_N is a SAT-preserving quotient of the generated formulas and I_N records parity incidence per quotient class.
- target-substitution-upper-bound: `SAT\in SIZE(n^c)\ \Rightarrow\ C(H_N)\le N^{\rho+o(1)}+N^q L_N^{c+O(1)}=N^{\max\{\rho,q\}+o(1)}.`. Valid when: Applies when SAT on length L_N formulas has nonuniform size L_N^c and the generator is target-clean.
- sparse-sketch-upper-bound: `H_N=P_N(T_N)\text{ off }B_N,\ |B_N|=E_N\ \Rightarrow\ C(H_N)\le S_T+O(A_N r_N+E_N N).`. Valid when: Requires that all feature circuits are charged once, monomial gates share them, and exceptions are patched by equality tests.
- exponent-falsifier-threshold: `S_T\le N^\sigma,\ A_N\le N^\alpha,\ r_N\le N^\gamma,\ E_N\le N^\eta\ \Rightarrow\ C(H_N)\le N^{\max\{\sigma,\alpha+\gamma,1+\eta\}+o(1)}.`. Valid when: Valid when the parameter exponents are asymptotic and r_N is at most N^{gamma+o(1)}.

## Attempted Derivation

- Start from the quotient normal form H_N=<a_N,I_N(x)> over F_2 for the XOR carrier.
- Observe that cycle 57's low-degree feature bound gives C(H_N)<=S_T+binom(r,<=t)+E_N N when the final combiner has degree t.
- Test the converse direction: high degree does not imply high circuit cost, because a degree-r monomial needs only O(r) gates after feature computation.
- Replace the degree parameter by monomial support A_N and derive C(H_N)<=S_T+O(A_N r_N+E_N N).
- Check target preservation separately: SAT in SIZE(n^c) still gives C(H_N)<=N^{max{rho,q}+o(1)} for polylogarithmic queries.

Blocking gap: No valid derivation converts an arbitrary small H_N circuit into a charged sparse quotient-polynomial sketch. Without this extraction, sketch lower bounds are falsifier tests, not source lower bounds.

## Falsifiers

- Sparse quotient-polynomial sketch with S_T+A_N r_N+E_N N<N^{1+epsilon-o(1)}.
- High-degree but one-monomial combiner, showing that degree-only hardness evidence is not valid.
- Uncharged feature map that directly computes H_N, collapsing the audit into a tautology rather than a route-specific falsifier.
- Target threshold collapse when max{rho,q}>=1+epsilon or when L_N is not polylogarithmic.
- Nonuniform leakage of the SAT label vector into the generator or feature circuits without being charged.
- Relativizing planted-control oracle where H_N is easy while quotient-sketch or separator measures remain hard.

## Learning

Cycle 58 repairs the XOR-carrier audit: low degree was the wrong nonlinear measure. The valid upper-bound falsifier is sparse quotient-polynomial support with threshold S_T+A_N r_N+E_N N<N^{1+epsilon}. This preserves the polylog-query target bridge but narrows the source obligation and exposes a new extraction gap: sparse-sketch hardness is not yet general-circuit hardness.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the XOR carrier source lower bound.`
- Rationale: The route already has a valid target-substitution bridge; the live uncertainty is whether quotient incidence can hide a subthreshold sparse nonlinear combiner that defeats the barely-superlinear source claim.
- Situation seed: Take a high-q XOR carrier with M_N=N^q generated SAT formulas of length L_N=(log N)^d, d>1, quotient the generated range by SAT-preserving symmetries, and compute H_N as the parity of the SAT labels hit by the incidence vector.
- Varied variable: The monomial-support exponent alpha in a final F_2 polynomial P_N(T_N), with A_N=N^alpha and feature dimension r_N=N^gamma.
- Held-fixed controls: q in ((1+epsilon)/2,1+epsilon) so dense tuple leakage remains threshold-blocked., rho<1+epsilon and max{rho,q}<1+epsilon so SAT substitution remains target-preserving., L_N=(log N)^d with d>1 so exhaustive truth-table lookup is not a subthreshold falsifier., All feature costs S_T and exception patches E_N N are charged explicitly.
- Expected observation: If alpha+gamma, sigma, and 1+eta all stay below 1+epsilon, the carrier is easy despite high quotient rank; if no such sketch appears, this only raises source plausibility and does not prove the lower bound.
- Transfer certificate needed: A formal nonrelativizing extraction theorem from arbitrary small circuits for H_N to charged SAT-blind sparse quotient-polynomial sketches, or else the observation remains only an upper-bound falsifier.

## Next Experiment

Formalize the weakest nontrivial extraction candidate: restrict arbitrary H_N circuits to circuits whose wires are invariant under SAT-preserving quotient symmetries, and test whether such invariant circuits collapse to sparse quotient-polynomial sketches with subthreshold loss.

# Barrier-Aware Lower-Bound Route: time-space tradeoff exponent gate

## Candidate Lemma

A SAT time-space product lower bound transfers to a deterministic time lower bound only after exponent division by the space exponent. If every decider for SAT_m satisfies T(m)S(m)^a >= m^b in a named uniform model, then SAT_m is not in DTIME(m^k) only when b>(a+1)k up to polylog slack. If the lower bound is stated only for S<=m^s, it covers only alleged algorithms whose actual space lies below that cap. Thus fixed-exponent time-space tradeoffs are valid restricted-algorithm lower bounds but are not P != NP progress without an unbounded exponent family or an all-polynomial-space transfer certificate.

## Definitions

- source object: a uniform time-space tradeoff lower bound for SAT_m in a named machine model M, stated as T(m)S(m)^a >= m^b or under S(m)<=m^s.
- target object: deterministic polynomial-time decision of SAT on m-bit encodings, audited exponent-by-exponent as DTIME(m^k).
- controlled interface: the only transfer uses the universal inequality S_A(m)<=O(T_A(m) polylog m) for standard uniform machines; no circuit, advice, or proof-system inference is smuggled in.
- target-preserving condition: the lower bound must be on the same SAT encoding length m and must cover the space used by the alleged m^k-time algorithm; padding changes the exponent and must be explicitly accounted for.

## Assumptions

- The machine model is fixed before comparing source and target, e.g. multitape Turing machine or log-cost RAM with standard space accounting.
- The tradeoff lower bound quantifies over deterministic deciders for the same SAT encoding, not over a promise slice with hidden decompression.
- The alleged P algorithm is uniform; nonuniform circuit consequences require a separate simulation and are not inferred here.
- Polylogarithmic overhead in the space<=time simulation is negligible only after an explicit exponent margin b>(a+1)k.

## Equations

- source_tradeoff: `T_A(m)\,S_A(m)^a \ge m^b`. Valid when: Valid when the source lower-bound model quantifies over all deterministic deciders in the named machine model on the same SAT_m slice.
- space_time_interface: `S_A(m) \le C\,T_A(m)\log^d m`. Valid when: Applies for standard Turing or RAM models where all written cells are reached during the counted computation.
- time_exponent_transfer: `T_A(m) \ge m^{b/(a+1)}/\log^{O(1)}m`. Valid when: Requires the tradeoff lower bound to cover the actual space of A and uses only S_A<=T_A polylog m.
- dt_k_exclusion_threshold: `b>(a+1)k \quad\Longrightarrow\quad SAT\notin DTIME(m^k)`. Valid when: Valid when k is fixed before the transfer and constants in the polylog overhead are dominated by the exponent margin.
- restricted_space_domain: `A\in DTIME(m^k)\text{ is covered by }S\le m^s\text{ only when }S_A(m)\le m^s`. Valid when: Applies when the source theorem is conditional on an a priori space cap rather than all polynomial spaces.
- padding_erosion: `M=n^c,\quad n^b=M^{b/c}`. Valid when: Applies after the reduction pads an n-bit SAT instance to length M=n^c while preserving NP-hardness for fixed c.

## Attempted Derivation

- Assume a uniform theorem: every deterministic decider A for SAT_m in model M has T_A(m)S_A(m)^a >= m^b.
- Assume toward a fixed-exponent transfer that SAT has an algorithm A with T_A(m)<=m^k.
- Use the controlled interface S_A(m)<=T_A(m)polylog(m), giving T_A(m)^{a+1}polylog(m)^a >= m^b.
- Conclude T_A(m)>=m^{b/(a+1)}/polylog(m), so the assumed m^k algorithm is contradicted only if b/(a+1)>k.
- For a theorem restricted to S<=m^s, first verify S_A(m)<=m^s; time m^k alone supplies no such verification when k>s.
- Under padding M=n^c, rewrite any core exponent b in the full target length as b/c, so padding can erase the margin against any fixed k.

Blocking gap: No fixed b,a tradeoff rules out all polynomial-time exponents. Space-capped tradeoffs do not quantify over all P algorithms. Padding can preserve NP-hardness while collapsing the measured exponent.

## Falsifiers

- A claimed TS^a>=m^b to P != NP bridge fails under the falsifier k>b/(a+1): an m^k-time SAT algorithm could satisfy the tradeoff rather than contradict it.
- A space-capped theorem with S<=m^s is not target-preserving for P: a hypothetical m^{s+1}-time polynomial-space decider lies outside the theorem's quantified domain.
- Padded SAT_c with M=n^c is a target-preserving falsifier for exponent claims measured on the core length n; NP-hardness remains for fixed c but the lower-bound exponent becomes b/c in M.
- A purely relativizing diagonalization-style proof object remains barrier-suspect unless it names a nonrelativizing ingredient; the present gate is valid only as exponent accounting, not as a barrier escape.

## Learning

Cycle 58 isolates a valid quantitative bridge for SAT time-space routes: T*S^a >= m^b excludes DTIME(m^k) only past the threshold b>(a+1)k, and space-capped or padded variants lose target preservation. This is route-level progress and a falsifier for fixed-exponent tradeoff slogans, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for time-space-to-P transfers.`
- Rationale: The route's risk is quantitative threshold collapse, not lack of terminology. Padding gives a concrete way to test whether the claimed bridge respects the target input length.
- Situation seed: Let L_c={pad_c(phi): phi in SAT_n and |pad_c(phi)|=M=n^c}. The map phi -> pad_c(phi) is polynomial-time for fixed c, so NP-hardness is preserved while the time-space lower-bound exponent is measured in the padded length M.
- Varied variable: padding exponent c in M=n^c.
- Held-fixed controls: The SAT core language and verifier are unchanged., The machine model and time-space measure T*S^a are unchanged., The many-one reduction remains uniform and polynomial time for every fixed c., No advice and no promise decoding are added.
- Expected observation: A core tradeoff exponent b becomes b/c in the full target length. For large c the bridge cannot exclude DTIME(M^k), showing that any valid route must either forbid padding or prove the tradeoff directly on dense full-length SAT encodings.
- Transfer certificate needed: A formal certificate that the lower bound is stated on the actual target length with b>(a+1)k for the desired k, or a padding-robust normalization theorem that preserves the exponent margin under reductions.

## Next Experiment

Audit branching-program length-width lower bounds for SAT using the same exponent discipline: source object L*log W or time-space simulation, target class DTIME(m^k), and padding erosion under full input length.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Generated anti-ball proofs give a valid MCSP-carrier bridge: let theta>0. If on kappa-dense source lengths m a deterministic no-advice generator emits at most 2^{D m+O(1)} rows T_{m,i} in {0,1}^{2^m} and proofs pi_{m,i}, at least one emitted pair is accepted, and a globally sound verifier satisfies V_m(T,pi)=1 => C(T)>2^{theta m} against unrestricted Boolean circuits, then the multiplexed language is in E and has circuit complexity 2^{delta n} for every delta<theta/(kappa(1+D)). Proof length 2^{lambda m} with constant lambda affects only the E running-time constant, not the lower-bound exponent.

## Definitions

- source object: a length-indexed deterministic generator G which sequentially emits a sparse list of truth tables and nonblackbox anti-ball proofs for MCSP no-side claims.
- target object: the multiplexed E language L_G whose length n_m block has truth table F_m(i,x)=T_{m,i}(x).
- controlled interface: image entropy D, hard threshold theta, length-gap kappa, generator overhead lambda, and verifier soundness against unrestricted circuits.
- target-preserving condition: generation is uniform and advice-free, source lengths are kappa-dense, and the consequence is an E circuit lower bound rather than P != NP itself.
- row length N=2^m; image count M_m<=2^{D m+O(1)}; multiplexed input length n_m=m+ceil(log M_m).
- Global soundness means every accepted pair is hard, not merely that the generated transcript is intended to describe a hard row.

## Assumptions

- Constants theta>0, D>=0, kappa>=1, and lambda<infty are independent of m.
- The generator can be simulated deterministically in 2^{O(m)} time per requested multiplexed bit by sequential scanning; no nonuniform row index or proof advice is used.
- For kappa-dense m, some emitted pair (T_{m,i},pi_{m,i}) is accepted by V_m.
- Verifier soundness is for unrestricted circuits of size below 2^{theta m}; restricted or uniform lower bounds are not enough.

## Equations

- multiplex_fixing_bound: `C(F_m) \le 2^{q n_m} \Rightarrow C(T_{m,i}) \le 2^{q(m+\log M_m)+o(m)}`. Valid when: Applies when the generated list is indexed inside the multiplexed table and the row index may be fixed nonuniformly.
- extracted_exponent: `q < \frac{\theta}{1+D} \quad \Rightarrow \quad C(F_m)>2^{q n_m}`. Valid when: Applies after at least one generated accepted row is globally soundly certified hard at threshold 2^{theta m}.
- all_length_padding_loss: `\delta < \frac{\theta}{\kappa(1+D)}`. Valid when: Requires kappa-dense source lengths and padding that preserves deterministic E uniformity without advice.
- radius_accounting: `\theta=\epsilon \text{ for exact exclusion of size }2^{\epsilon m};\quad \theta=\epsilon-\rho \text{ if only smaller centers }2^{(\epsilon-\rho)m}\text{ are excluded}`. Valid when: Valid when the verifier proves exact MCSP hardness, or when the radius loss is explicitly charged to a smaller excluded center class.
- proof_length_noncharge: `t_{L_G}(n_m) \le 2^{O((1+D+\lambda)m)}=2^{O(n_m)}`. Valid when: Applies when the row/proof stream is deterministic and every overhead exponent is an absolute constant.

## Attempted Derivation

- Model the source as a deterministic generator G(1^m) emitting M_m<=2^{D m+O(1)} row/proof pairs, rather than as an existential proof search problem.
- Define the target language by multiplexing only the emitted rows; proofs are used for soundness but are not part of the target truth table.
- If F_m has circuits of size 2^{q n_m}, fixing the emitted hard row index gives a circuit for that row of size 2^{q(1+D)m+o(m)}.
- Global verifier soundness for an accepted generated pair contradicts this when q<theta/(1+D), and kappa-dense padding gives delta<theta/(kappa(1+D)).
- Audit the proof relation: a poly(N) locator on a large accepted projection triggers the natural-proofs barrier, while a subthreshold indexed row decoder directly falsifies MCSP soundness.

Blocking gap: No generated, sparse, advice-free, globally sound, non-natural anti-ball proof family is known. The bridge is valid only after constructing such a binding certificate without a large locatable projection and without subthreshold row access.

## Falsifiers

- falsifier: the row/proof pair is existentially present but not E-uniformly generated, causing double-exponential proof-location search.
- falsifier: the verifier is sound only for promised generated transcripts and not for arbitrary accepted pairs, unless a direct theorem proves the generated row hard.
- falsifier: a poly(N)-time locator plus large accepted projection converts the relation into a natural useful property.
- falsifier: an indexed or interval decoder of size below 2^{theta m} makes the emitted row MCSP-easy.
- falsifier: nonuniform advice chooses the hard row, the proof, or the source length.
- falsifier: radius accounting reduces theta to o(1), causing the extracted exponent delta to collapse.

## Learning

Cycle 58 separates proof length from proof locatability. A generated proof may be exponentially long without reducing the carrier-to-E lower-bound exponent, provided the row/proof stream is deterministic and advice-free. The real new obstruction is projection/locator naturalness: making proofs findable for a large set of rows turns the source into a natural useful property, while indexed access still falsifies MCSP soundness. Thus the valid transfer is delta<theta/(kappa(1+D)); constructing the generated non-natural anti-ball source remains open.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: Cycle 57 left open whether long generated proofs should be charged to extraction. A concrete proof-length experiment tests this without restating hardness magnification or P vs NP.
- Situation seed: For each m, let G_m sequentially emit M=2^{D m} candidate truth tables and nonblackbox anti-ball proofs of length 2^{lambda m}; V_m certifies that an accepted row is outside every unrestricted circuit ball of size 2^{theta m}. The target is the multiplexed E language F_m(i,x).
- Varied variable: proof-length exponent lambda in |pi|=2^{lambda m}.
- Held-fixed controls: hardness threshold theta and image entropy D are fixed constants, source lengths remain kappa-dense and generation is deterministic with no advice, the emitted rows have no indexed decoder below 2^{theta m}, verifier soundness is against unrestricted circuits, not a restricted model
- Expected observation: As lambda increases through subtable, table-length, and supertable constant regimes, E membership changes only by a time constant and the lower-bound exponent remains delta<theta/(kappa(1+D)). Any need for a row-to-proof locator instead of length-indexed generation exposes a natural-proof falsifier.
- Transfer certificate needed: A formal certificate that V is globally sound, the generated list is sparse or non-large, no constructive large projection locator is used, and the emitted rows lack subthreshold random access before the intuition may enter the proof queue.

## Next Experiment

Try a tiny-D nonblackbox binding invariant based on universal-circuit diagonal anti-ball certificates; audit first for row-to-proof locator largeness, then for indexed-decoder leakage, before attempting any extraction claim.
