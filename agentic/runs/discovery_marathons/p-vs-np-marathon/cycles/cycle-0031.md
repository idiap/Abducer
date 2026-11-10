# cycle-0031

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: approximate relaxed bag separators

## Candidate Lemma

For a generated-OR carrier, an approximate relaxed bag separator with s gates and E bad input bags gives C(H_N)<=O(N^rho+N^q s+NE). Thus an N^{1+epsilon-o(1)} source lower bound forces every such separator above the same threshold; any subthreshold one is a falsifier.

## Definitions

- source object: H_N on N-bit inputs, H_N(x)=OR_{j<=N^q} SAT(G_{N,j}(x)), query length L=(log N)^d, shared generator circuit size N^rho.
- target object: SAT on L-bit formulas; target consequence is SAT notin P/poly if a valid H_N lower bound N^{1+epsilon-o(1)} coexists with q,rho<1+epsilon.
- controlled interface: substitute SAT circuits into generated queries for the forward bridge, and audit reverse nonuniform leakage by bag-level predicates A_N on generated formulas.
- target-preserving condition: d>1, q,rho<1+epsilon, valid-length generation, general circuit source model, and all separator, generator, and exception advice counted nonuniformly.

## Assumptions

- C(.) is general Boolean circuit size on N-bit inputs.
- An (s,E)-separator A_N satisfies OR_j A_N(G_{N,j}(x))=H_N(x) outside at most E inputs x.
- Exceptions may be patched by equality tests using O(NE) gates and stored labels.

## Equations

- carrier: `H_N(x)=\bigvee_{j\le N^q} SAT(G_{N,j}(x)),\quad |G_{N,j}(x)|=(\log N)^d`. Valid when: Valid when the carrier uses fixed generated query bags and shared generator parameters.
- separator_collapse: `C(H_N)\le O(N^\rho+N^q s+NE)`. Valid when: Applies when a size-s bag separator fails on at most E input bags and exceptions are patched nonuniformly.
- audit_threshold: `s=N^\sigma,E=N^\eta\Rightarrow \max\{\rho,q+\sigma,1+\eta\}\ge 1+\epsilon-o(1)`. Valid when: Requires the source lower bound and collapse inequality in the same circuit model and valid-length family.

## Attempted Derivation

- Assume H_N has C(H_N)>N^{1+epsilon-o(1)} and q,rho<1+epsilon on the same valid lengths.
- Given A_N, compute all generated formulas with the shared N^rho generator, apply A_N to each of N^q queries, and OR the answers.
- The resulting circuit agrees with H_N except on E bags; add equality tests for those inputs and hardwire the correct bit, costing O(NE).
- If s=N^sigma and E=N^eta with max{rho,q+sigma,1+eta}<1+epsilon, the patched circuit contradicts the source lower bound.

Blocking gap: We still lack a lower bound against all distribution-local approximate bag separators; global promise-SAT hardness does not rule out local predicates tuned to the generated bags.

## Falsifiers

- Approximate separator falsifier: a local A_N with s<N^{1+epsilon-q-o(1)} and E<N^{epsilon-o(1)} collapses H_N below threshold.
- Exception-patching falsifier: even rare bag errors are harmless to circuits when NE<N^{1+epsilon-o(1)}.
- Distribution leakage falsifier: A_N only needs to be valid on generated bags, not on all SAT instances.
- Natural-proof barrier probe: a dense constructive proof excluding all small A_N would look natural unless it is explicitly range-specific or nonconstructive.

## Learning

Cycle 31 converts relaxed bag separators into an approximate threshold lemma: E bad bags cost NE gates, so errors below N^epsilon are nonuniformly patchable. The valid source obligation is now an approximate distribution-local separator lower bound, not merely promise SAT hardness.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe.`
- Rationale: Exact relaxed separators were too idealized; approximate bag agreement plus equality patching has a sharp exponent threshold that can kill the source lower bound.
- Situation seed: Generated-OR carrier with t=N^q formulas of length L=(log N)^d; choose a local predicate A_N on generated formulas and allow E=N^eta wrong input bags.
- Varied variable: exception exponent eta in E=N^eta
- Held-fixed controls: q,rho<1+epsilon for the target bridge, d>1 so SAT circuit substitution costs N^{q+o(1)}, general Boolean circuit source model with nonuniform exception advice counted
- Expected observation: For eta<epsilon, small A_N gives a subthreshold exact circuit for H_N; only eta>=epsilon or s>=N^{1+epsilon-q-o(1)} survives the audit.
- Transfer certificate needed: A formal lower bound against all distribution-local (s,E)-bag separators, preferably non-natural or range-specific, before the intuition can enter the proof queue.

## Next Experiment

Try a collision-balanced generator and estimate whether majority/hash-based local predicates yield s=N^{o(1)} with E<N^epsilon; if yes, quarantine this carrier family.

# Barrier-Aware Lower-Bound Route: sign-rank target-preservation audit

## Candidate Lemma

Fixed-partition high real sign-rank separators either naturalize, or fail as P-vs-NP routes against full SIZE(n^k): inner product is polynomial-size and has maximum sign-rank, so no nontrivial rank threshold is target-preserving.

## Definitions

- source object: a total truth-table property P_{r,pi} testing real rank of the sign communication matrix of f:{0,1}^n->{0,1}.
- target object: SIZE(n^k) truth tables on the same n input bits, with k>=1 and no promise restriction excluding inner product.
- controlled interface: sign-rank lower bound for SAT_n under fixed partition pi -> natural-proof usefulness audit against SIZE(n^k).
- target-preserving condition: every target circuit C in SIZE(n^k) must have rank_R(A_C)<=r under the same partition pi.
- Let N=2^n, R=2^u, C=2^v, u+v=n, and D=min(R,C).
- Constructivity means P_{r,pi} is decidable in poly(N) time by exact Gaussian elimination over rationals.

## Assumptions

- The partition pi is uniform and independent of the SAT truth table.
- The property is total on all N-bit truth tables, not only SAT encodings.
- Use real rank of A_f[x,y]=(-1)^{f(x,y)}, not F_2 rank of the 0/1 value matrix.
- Natural-proof audit applies when density is at least N^{-O(1)} and usefulness is against the named target class.

## Equations

- sign_matrix_property: `A_f[x,y]=(-1)^{f(x,y)},\quad P_{r,\pi}=\{f:\operatorname{rank}_{\mathbb R}(A_f)>r\}.`. Valid when: Valid when the source lower-bound model fixes a uniform two-block input partition.
- low_rank_count: `\Pr_F[\operatorname{rank}_{\mathbb R}(A_F)\le r]\le 2^{O(r(R+C)\log(RC))-RC}.`. Valid when: Valid when Warren-style sign-pattern counting is applied to R by C sign matrices.
- ip_falsifier_rank: `\operatorname{rank}_{\mathbb R}(A_{IP})=D,\quad \operatorname{size}(IP_n)=O(n).`. Valid when: Valid when IP pairs variables across the same partition and ignores surplus variables.

## Attempted Derivation

- Type the source claim as rank_R(A_SAT)>r for one explicit partition pi of n variables.
- Use the low-rank counting bound to show P_{r,pi} is large, and Gaussian elimination to show poly(N)-constructive.
- If all SIZE(n^k) circuits had rank<=r, P_{r,pi} would be a valid natural property useful against SIZE(n^k).
- But IP_n has O(n) circuit size and rank D; hence any r<D accepts a target function, while r>=D cannot separate SAT.

Blocking gap: No fixed sign-rank threshold is target-preserving for full SIZE(n^k); the route can only address restricted low-rank circuit classes.

## Falsifiers

- Inner product under the same partition has maximum real sign-rank and O(n) circuit size, killing usefulness for SIZE(n^k).
- A partition or rank test with SAT-dependent advice loses uniform constructivity and is invalid as a natural-proof escape.
- A promise-only rank lower bound lacks total density over all truth tables, so the naturalization inference is not valid.
- Using F_2 rank of the 0/1 value matrix makes the IP falsifier false; the lemma is specifically about real sign-rank.

## Learning

Cycle 31 certifies a concrete failure mode: high real sign-rank is a valid dense constructive property, but it cannot be useful against full polynomial-size circuits because IP is easy and maximum-rank. This is route-level barrier progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design concrete thought experiment now as a falsifier probe.`
- Rationale: The route needs a target-preserving audit, not another abstract barrier slogan: sign-rank lower bounds are dense but may accept easy high-rank functions.
- Situation seed: Balanced SAT communication matrix: split n variables into n/2 and n/2, define P_r by real sign-rank > r, and compare SAT_n with IP_n and SIZE(n^k).
- Varied variable: The threshold ratio rho=r/D, where D=2^{n/2} is the maximum balanced sign-rank.
- Held-fixed controls: Uniform balanced partition independent of SAT., Target class SIZE(n^k) with k>=1., Total property over all N-bit truth tables., Exact poly(N)-time rank computation.
- Expected observation: For every rho<1 the property is large, but IP_n lies in P_r and is easy; at rho=1 the property cannot contain SAT. Usefulness collapses before any P-vs-NP transfer.
- Transfer certificate needed: A proof that the actual target class excludes all high sign-rank easy functions, or a reduction from such a restricted class to full SIZE lower bounds without nonuniform leakage.

## Next Experiment

Audit low sign-rank upper bounds for restricted circuit classes such as AC0[2]-free formulas, and test whether any known transfer to general SIZE avoids the IP obstruction.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

If a linear-certificate E-uniform MCSP source has kappa-dense lengths, distinct accepted image entropy D, and some accepted image has MCSP above 2^{epsilon m}, then canonical image multiplexing gives an E language with circuit lower bound exponent every delta<epsilon/(kappa(1+D)).

## Definitions

- source object: E-uniform verifier V(1^m,z) emitting a 2^m-bit truth table; accepted image set I_m={T: exists accepted z emitting T}.
- target object: E language L whose input encodes a canonical image index j, an m-bit point x, and length-balancing padding.
- controlled interface: E-canonical distinct-image unranking sends j to T_j in I_m and defines L(j,x,p)=T_j(x).
- target-preserving condition: source lengths are kappa-dense, certificates are O(m), |I_m|<=2^{D m+o(m)}, epsilon<alpha_V, and source soundness is uniform, no-advice, and non-large.

## Assumptions

- For infinitely or all kappa-dense m, there exists T in I_m with circuit complexity greater than 2^{epsilon m}.
- Duplicate certificates are quotiented by an E-canonical equality test over emitted truth tables.
- D, kappa, epsilon, and the verifier cap alpha_V are constants independent of m.
- The source proof is not a constructive large property over most truth tables.

## Equations

- image_entropy: `\log_2 |I_m| \le Dm+o(m)`. Valid when: Valid when the source family has an E-canonical quotient over distinct emitted truth tables.
- length_budget: `n \le \kappa(1+D)m+o(m)`. Valid when: Applies after image indexing and padding preserve the kappa-dense source length window.
- transfer_threshold: `\delta < \frac{\epsilon}{\kappa(1+D)}`. Valid when: Requires the target-preserving hardwiring argument and the MCSP no-side threshold 2^{epsilon m}.

## Attempted Derivation

- Enumerate all O(m)-bit certificates, run V, compare emitted 2^m-bit tables, and unrank the jth distinct accepted image in 2^{O(m)} time, hence L is in E.
- Pick a hard image T_j in I_m. If L at the padded length n has circuits of size 2^{delta n}, hardwire j and padding to get an m-input circuit for T_j.
- Using n<=kappa(1+D)m+o(m), the hardwired circuit has size below 2^{epsilon m} whenever delta<epsilon/(kappa(1+D)), contradicting the source MCSP no-side claim.
- Barrier audit: the bridge is mostly relativizing; any nonrelativizing or non-natural content must be in the source soundness proof, not in this extraction step.

Blocking gap: No valid construction is known for a bounded-D, cap-compatible, constant-epsilon accepted image family with uniform no-advice MCSP soundness.

## Falsifiers

- falsifier: |I_m|=2^{D_m m} with D_m unbounded or no E-canonical quotient makes the transferred exponent collapse to o(1).
- falsifier: epsilon>=alpha_V, since checkpoint circuits for V already put every emitted table below the claimed MCSP threshold.
- falsifier: the hard image is selected only by nonuniform advice over lengths or indices, yielding no E target language.
- falsifier: source soundness is a constructive large property of truth tables, triggering the natural-proofs obstruction under standard PRG assumptions.

## Learning

Cycle 31 fixes the exact quotient transfer: the exponent loss is D, not certificate count, once E-canonical distinct-image unranking is available. The bridge is valid route progress; the remaining hard task is a bounded-D, cap-compatible, non-natural, no-advice MCSP source theorem.

## Gedanken Experiment Design Seed

- Need decision: `use-now-as-falsifier-probe`
- Rationale: The bridge is valid; the live uncertainty is whether bounded distinct-image entropy can coexist with constant MCSP hardness below the verifier cap without advice or naturalness.
- Situation seed: For each m, imagine a sequential E-uniform verifier whose accepted quotient contains exactly 2^{D m} canonical truth tables, one promised MCSP-hard above 2^{epsilon m}, then pad lengths with factor kappa=2.
- Varied variable: distinct-image entropy rate D
- Held-fixed controls: epsilon<alpha_V is fixed below the checkpoint cap, certificate length is O(m) and enumeration is E-uniform, no advice chooses the hard image or source length, padding density kappa and the MCSP threshold exponent are fixed
- Expected observation: The target exponent should fall as delta<epsilon/(2(1+D)); if D grows with m, the route produces no constant lower-bound exponent.
- Transfer certificate needed: A uniform source theorem proving the promised hard accepted image and the E-canonical quotient, plus a non-large soundness argument outside the natural-proofs barrier.

## Next Experiment

Audit candidate sequential verifiers by computing their alpha_V cap and distinct-image entropy D, then test whether any soundness proof avoids advice and natural largeness.
