# cycle-0014

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: polylog generated-OR carrier

## Candidate Lemma

Let L(N)=(log N)^d with fixed d>1, M(N)=N^q, and let a target-clean generator/consumer pair (G_N,A_N) of circuit size at most N^rho define H_N by consuming M generated SAT instances of length L. If max{rho,q}<1+epsilon and SIZE(H_N)>N^{1+epsilon} for infinitely many valid N, then SAT has no polynomial-size nonuniform circuits; hence NP is not contained in P/poly.

## Definitions

- source object: H_N^{G,A}(x)=A_N(x, SAT_L(G_N(x,1)),...,SAT_L(G_N(x,M))) for x in {0,1}^N, where M=N^q and L=(log N)^d.
- target object: nonuniform Boolean circuits for SAT on length-L encodings, with target consequence SAT notin P/poly and therefore NP not subset P/poly.
- controlled interface: G_N and A_N are uniform or explicitly constructible circuits of total size at most N^rho and use only generated formula bits plus SAT answers.
- target-preserving condition: for some epsilon>0, max{rho,q}<1+epsilon, no SAT-dependent advice is embedded, and the source lower bound holds on infinitely many valid lengths.

## Assumptions

- q,rho,d,epsilon are constants with d>1 and max{rho,q}<1+epsilon.
- G_N(x,i) outputs a valid SAT instance of length L(N), or a fixed padded unsatisfiable instance on malformed indices.
- A_N is deterministic and target-clean; it does not contain the SAT truth table, a hardwired satisfying assignment table, or advice depending on the hypothetical SAT circuit.
- The source lower bound is against unrestricted nonuniform Boolean circuits for the length-N truth table of H_N.
- SAT in P/poly means there is a fixed c such that SAT on all sufficiently large input lengths has circuits of size O(n^c).

## Equations

- carrier_definition: `H_N(x)=A_N\bigl(x,\operatorname{SAT}_L(G_N(x,1)),\ldots,\operatorname{SAT}_L(G_N(x,M))\bigr)`. Valid when: Valid when G_N emits exactly M generated SAT instances and A_N consumes only their SAT bits.
- composition_upper_bound: `\operatorname{SIZE}(H_N)\le O\bigl(N^\rho+M(N)(L(N)^c+L(N))\bigr)`. Valid when: Valid when SAT_L has size O(L^c) circuits and each target call is substituted as a separate subcircuit.
- polylog_amortization: `M(N)L(N)^c=N^q(\log N)^{dc}=N^{q+o(1)}`. Valid when: Valid when c and d are fixed constants and N tends through the chosen valid lengths.
- threshold_contradiction: `\max\{\rho,q\}<1+\epsilon\ \Longrightarrow\ \operatorname{SIZE}(H_N)<N^{1+\epsilon}\text{ for all large valid }N`. Valid when: Applies after choosing a positive margin between max{rho,q} and the claimed source lower-bound exponent.

## Attempted Derivation

- Fix constants d>1, q, rho, epsilon with max{rho,q}<1+epsilon, and define H_N by a target-clean generated OR or more general consumer over M=N^q length-L SAT instances.
- Assume toward contradiction that SAT is in P/poly, so for some c every sufficiently large length l has SAT circuits C_l of size O(l^c).
- For each valid N, copy C_{L(N)} into every generated target slot and wire these copies to A_N; the generator/consumer contributes N^rho gates and the target copies contribute N^q L^c gates.
- Since L=(log N)^d, the copy cost is N^{q+o(1)} for fixed c,d. Hence SIZE(H_N)<=N^{max{rho,q}+o(1)}.
- Choose delta>0 with max{rho,q}+delta<1+epsilon. For all large valid N the composed circuit has size below N^{1+epsilon}, contradicting the i.o. source lower bound.
- Audit the unconditional falsifier: replacing each SAT call by exhaustive search costs N^rho+N^q2^L poly(L), which is N^{q+omega(1)} for d>1, so it does not itself refute an N^{1+epsilon} lower bound.

Blocking gap: The bridge is valid, but no explicit target-clean G_N,A_N is known with a provable unrestricted circuit lower bound SIZE(H_N)>N^{1+epsilon}. A proof of that source bound must also avoid natural-proof density, relativizing oracle, and advice-leakage obstructions.

## Falsifiers

- falsifier: threshold collapse occurs if max{rho,q}>=1+epsilon, because SAT circuits then give no contradiction to the claimed source lower bound.
- falsifier: lookup collapse occurs when N^rho+N^q2^{L(N)}poly(L(N))<N^{1+epsilon} on infinitely many valid lengths.
- falsifier: nonuniform leakage occurs if G_N or A_N encodes SAT_L advice not charged to N^rho.
- falsifier: model mismatch occurs if the source lower bound is for formulas, AC0, or another restricted model while the target substitution requires unrestricted P/poly circuits.
- falsifier: a large constructive natural property proving the source lower bound would collide with pseudorandom-function assumptions at the same N^{1+epsilon} scale.
- falsifier: a fully relativizing source lower-bound proof would be suspect because oracle worlds with NP^O subset P^O/poly should invalidate the target consequence.

## Learning

Cycle 14 identifies a concrete carrier template, H_N=OR of N^q generated SAT instances of length (log N)^d, and computes the exact transfer: SAT in SIZE(n^c) gives H_N in SIZE(N^{max{rho,q}+o(1)}). The valid magnification window is max{rho,q}<1+epsilon plus lookup safety N^rho+N^q2^L not subthreshold. For d>1, exhaustive lookup is N^{q+omega(1)}, so the previous short-query falsifier is avoided, but the source lower bound remains the hard non-natural obligation.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch now needs a concrete carrier and a quantitative lookup-safety test; another statement of hardness magnification would not decide whether the polylog window is real.
- Situation seed: Take a P-uniform near-linear vector generator G_N that maps (x,i), with x in {0,1}^N and i in [N], to a SAT formula Phi_{x,i} of length L=(log N)^d. Define H_N(x)=OR_{i<=N} SAT(Phi_{x,i}).
- Varied variable: The SAT-query length exponent d in L=(log N)^d, varied across d=1, d>1, and slowly growing d(N).
- Held-fixed controls: M(N)=N queries, so q=1 and the target-copy count is exactly linear., Generator and OR consumer size are N^{1+o(1)} and contain no SAT-dependent advice., The asserted source lower bound is unrestricted SIZE(H_N)>N^{1+epsilon} on infinitely many valid lengths., The target assumption tested is SAT in SIZE(n^c) for an arbitrary fixed c.
- Expected observation: For every fixed d>1, SAT-circuit substitution gives H_N circuits of size N^{1+o(1)}, while brute-force lookup costs N^{1+omega(1)} and is not a subthreshold falsifier. At d=1 the lookup boundary becomes N^{1+lambda+o(1)}, exposing the exact constant-margin requirement lambda>=epsilon.
- Transfer certificate needed: A formal certificate must show P-uniformity, near-linear generator size, no advice leakage, valid-length alignment, H_N in NP, and a non-natural unrestricted N^{1+epsilon} lower-bound method before the intuition enters the proof queue.

## Next Experiment

Instantiate G_N as a near-linear Cook-Levin micro-instance generator with M=N and L=(log N)^d; compute exact rho, verify H_N is in NP with poly(N) uniform verification, and test whether any structural simplification gives an N^{1+epsilon} upper-bound falsifier.

# Barrier-Aware Lower-Bound Route: Merlin-Local Naturalization Gate

## Candidate Lemma

Short-witness deterministic Merlin-local SAT truth-table separators are natural properties, so a claimed NP-style local certificate is not a natural-proof escape unless witness enumeration, largeness, or usefulness fails.

## Definitions

- source object: a deterministic Merlin-local separator V for the SAT_n truth table y in {0,1}^N, N=2^n, with witness length a(N), adaptive query bound q(N), and poly(N)-time query computation.
- target object: a Razborov-Rudich natural property P_N of N-bit truth tables that is constructive in poly(N), has density at least 1/poly(N), and is useful against SIZE(n^k).
- controlled interface: define P_N={y in {0,1}^N : exists w in {0,1}^{a(N)} such that V^y(1^N,w)=1}, and transfer separator soundness into usefulness.
- target-preserving condition: V accepts SAT_n for some witness, rejects every truth table computed by every n^k-size circuit for every witness, and has a(N)=O(log N) and q(N)=O(log N).
- adaptive queries are allowed; after fixing the accepting witness and transcript, the accepted inputs contain one cylinder fixing at most q(N) truth-table positions.
- the natural-proof obstruction is invoked only under the standard strong PRF hypothesis; without that hypothesis the lemma is a barrier audit, not a P != NP theorem.

## Assumptions

- Completeness: there exists w* with V^{SAT_n}(1^N,w*)=1.
- Usefulness soundness: for every circuit C of size at most n^k and every witness w, V^{tt(C)}(1^N,w)=0.
- The verifier is deterministic after the witness is fixed; randomized variants require the seed-elimination audit from the previous cycle.
- Witness enumeration is allowed in the constructivity budget only when 2^{a(N)} poly(N) is polynomial in N.

## Equations

- property_from_merlin_separator: `\mathcal{P}_N=\{y\in\{0,1\}^N:\exists w\in\{0,1\}^{a(N)}\; V^y(1^N,w)=1\}.`. Valid when: Valid when the verifier is a black-box truth-table procedure whose witnesses are explicit binary strings.
- constructivity_bound: `T_{decide}(N)\le 2^{a(N)}\,\mathrm{poly}(N).`. Valid when: Valid when each witness simulation makes at most polynomially computable adaptive truth-table queries.
- cylinder_density_lower_bound: `\Pr_{y\leftarrow\{0,1\}^N}[y\in\mathcal{P}_N]\ge 2^{-q(N)}.`. Valid when: Applies when completeness gives one accepting witness and one accepting adaptive transcript fixing q bits.
- natural_threshold: `a(N),q(N)\le c\log N\;\Longrightarrow\; \mathcal{P}_N\text{ is poly}(N)\text{-constructive and }N^{-c}\text{-large}.`. Valid when: Requires logarithmic witness length and logarithmic query complexity in the truth-table length N.

## Attempted Derivation

- Start with a claimed lower-bound route: a deterministic verifier V reads a small number q of locations of a candidate truth table y and accepts SAT_n with some witness w while rejecting all n^k-size circuit truth tables for every witness.
- Define the induced property P_N by existentially quantifying over witnesses.
- Constructivity: decide P_N by enumerating all 2^a witnesses and simulating V; this is poly(N) when a=O(log N).
- Largeness: fix the accepting witness w* for SAT_n and the accepting adaptive transcript. Every table agreeing with the transcript on its queried bits is accepted, giving density at least 2^{-q}.
- Usefulness: universal soundness over all witnesses implies no n^k-size circuit truth table lies in P_N.
- Therefore a short-witness, logarithmic-query Merlin-local SAT separator is a standard natural property and is blocked by the natural-proof falsifier under strong PRFs.

Blocking gap: The derivation does not rule out a(N)=omega(log N) witnesses, nonblack-box syntax checks, or proof objects whose usefulness is not universal over all witnesses.

## Falsifiers

- falsifier for short secret-witness escape: a=O(log N), q=O(log N), and universal small-circuit rejection make the object a valid natural property.
- falsifier for the lemma: if V's witness search is inherently superpolynomial and no equivalent small accepting cylinder is computable, constructivity is not established.
- falsifier for target transfer: if soundness rejects only typical small circuits or only circuits with a fixed encoding, usefulness against SIZE(n^k) is not preserved.
- falsifier for barrier invocation: if the verifier uses nonblack-box SAT syntax or proof-system soundness rather than truth-table black-box queries, the naturalization proof may not apply.

## Learning

Cycle 14 isolates a new valid threshold: existential local certificates with a=O(log N) and q=O(log N) are still natural properties when soundness is universal over all small circuits and witnesses. Merlin secrecy is not a barrier escape at logarithmic witness length. Superlogarithmic witnesses are a possible escape only by breaking poly(N) constructivity, and then the route owes a target-preserving anti-leakage certificate.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The route currently needs a concrete audit of existential local certificates, because short Merlin witnesses are often advertised as non-natural while still being enumerable inside the poly(N) natural-proof constructivity budget.
- Situation seed: Imagine a Merlin-local separator V for SAT_n: Merlin sends a(N) bits, V adaptively queries q(N)=10 log N bits of an N=2^n truth table, accepts SAT_n for one witness, and rejects every truth table computed by n^k-size circuits for every witness.
- Varied variable: witness length exponent alpha in a(N)=(log N)^alpha.
- Held-fixed controls: query bound q(N)=10 log N and deterministic black-box truth-table access, universal soundness against all SIZE(n^k) truth tables for every witness, poly(N)-time computation of queried indices and acceptance predicate, target target remains SAT_n not in SIZE(n^k), not an average-case or promise variant
- Expected observation: For alpha<=1 the induced property is poly(N)-constructive and N^{-10}-large, so the natural-proof barrier applies under PRFs. For alpha>1 largeness remains but enumeration becomes quasipolynomial or worse, so the barrier audit no longer certifies failure without an additional witness-compression argument.
- Transfer certificate needed: A formal witness-elimination, compression, or nonuniform-leakage certificate: either reduce accepting witnesses to O(log N) bits in a target-preserving way, or prove that the long witness is not merely hardwired information about SAT_n.

## Next Experiment

Audit algebraic Merlin-local variants: V queries a low-degree extension of the SAT truth table with a short witness; test whether accepting affine-subspace cylinders give largeness or whether the route instead algebrizes.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Block-seek leakage lemma: an accepted MCSP no-side certificate whose streamed truth table admits subthreshold block access cannot be sound at threshold 2^{epsilon m}. If blocks have length 2^{beta m} and the resume/block circuit has size 2^{sigma m}, then the certified m-bit function has circuits of size 2^{max{beta,sigma}m+o(m)}.

## Definitions

- source object: an O(m)-bit sequential MCSP no-side certificate p whose verifier streams T_p in {0,1}^{2^m} within 2^{c m} time.
- target object: an E-uniform truth-table family yielding SIZE(2^{delta n}) lower bounds on all sufficiently large input lengths after the carrier extraction.
- controlled interface: block-seek access to a certified stream is modeled by circuits A_{m,p} of size 2^{sigma m} outputting blocks of length 2^{beta m}.
- target-preserving condition: the transfer is valid only when no accepted certificate admits subthreshold block access with max{beta,sigma}<epsilon, and the certified lengths remain kappa-dense.

## Assumptions

- For every accepted p, the verifier outputs a full truth table T_p of an m-input Boolean function f_p.
- No-side soundness claims MCSP_m(T_p)>2^{epsilon m} for every accepted p.
- A block-seek implementation may depend on the fixed certificate p but not on additional nonuniform advice beyond the circuit A_{m,p}.
- The within-block bit position can be selected by hardwiring or a multiplexer of size O(2^{beta m} poly(m)).

## Equations

- block_parameters: `N=2^m,\quad L=2^{\beta m},\quad q=N/L=2^{(1-\beta)m}`. Valid when: Applies when the streamed certificate table is partitioned into equal contiguous blocks and beta lies between zero and one.
- block_seek_circuit_upper_bound: `\mathrm{SIZE}(f_p)\le |A_{m,p}|+O(L\,\mathrm{poly}(m))\le 2^{(\max\{\sigma,\beta\}+o(1))m}`. Valid when: Valid when a fixed accepted certificate has a block-seek circuit of size at most 2^{sigma m} and the residual within-block scan is hardwired.
- soundness_threshold_guard: `\mathrm{MCSP}_m(T_p)>2^{\epsilon m}\ \Longrightarrow\ \max\{\sigma,\beta\}\ge \epsilon-o(1)`. Valid when: Requires the no-side soundness threshold to apply to every accepted table and the block-seek simulation to preserve Boolean circuit size.

## Attempted Derivation

- Model a candidate non-enumerative repair as a checkpointed sequential decompressor: certificate p has length O(m), V streams T_p in 2^{c m}, and a resume circuit A_{m,p} outputs any block of length L=2^{beta m}.
- Fix an accepted p and construct a circuit for f_p(x): compute the block index of x, invoke A_{m,p}, and select the bit of x inside that block.
- The resulting circuit size is at most 2^{max{beta,sigma}m+o(m)}, where 2^{sigma m} bounds the resume circuit.
- If max{beta,sigma}<epsilon, this contradicts MCSP_m(T_p)>2^{epsilon m}; therefore fine-grained checkpointing, bit generators, and local transcript proof systems are invalid source implementations.
- Setting beta>=epsilon avoids immediate leakage but destroys the hoped-for local verification advantage; soundness still needs a global non-enumerative invariant.

Blocking gap: No known sparse global invariant proves high general circuit complexity for a 2^{O(m)}-streamed table while also proving that all subthreshold block-seek implementations are impossible.

## Falsifiers

- falsifier: a bit-addressable generator G(p,x) of size 2^{sigma m} with sigma<epsilon makes every accepted table low-MCSP.
- falsifier: checkpointed streaming with block exponent beta<epsilon and resume exponent sigma<epsilon collapses the no-side threshold.
- falsifier: direct enumeration of all size-s circuits inside 2^{O(m)} time only certifies s=O(m/log m), giving epsilon_m=o(1).
- falsifier: an advice-dependent selector for accepted certificates makes the extracted consequence nonuniform rather than an E lower bound.
- falsifier: a dense constructive recognizer for high-MCSP tables would re-enter the natural-proofs obstruction unless the accepted image stays sparse and non-large.
- falsifier: source lengths without kappa-density give at most sparse-length lower bounds and do not preserve the all-length target.

## Learning

Cycle 14 adds an exact locality threshold: any accepted certificate with block access below exponent epsilon yields small circuits for its own table, so it cannot be a sound MCSP no-side carrier. The valid bridge survives, but the remaining source must be sparse, non-enumerative, non-natural in the large-property sense, nonuniform-free, and globally sequential with seek cost at least 2^{epsilon m-o(m)}.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The branch is blocked at source construction, not extraction. Varying the block-seek exponent beta directly tests whether checkpointed or decompressor-style certificates are target-preserving or leak small circuits.
- Situation seed: An O(m)-bit certificate p for an m-input MCSP no-side truth table T_p is verified by a 2^{c m}-time streaming decompressor V. Add optional checkpoints every L=2^{beta m} output bits, with a uniform resume/block circuit R_{m,p} of size 2^{sigma m}.
- Varied variable: The block length exponent beta, with sigma treated as the candidate resume-access exponent and epsilon held as the MCSP threshold.
- Held-fixed controls: No-side threshold MCSP_m(T_p)>2^{epsilon m} for fixed epsilon>0., Certificate length O(m) and total streaming verification time 2^{O(m)}., No nonuniform advice beyond the certificate p., Kappa-dense source lengths for the extraction target., Target extraction exponent requirement delta<epsilon/kappa.
- Expected observation: For beta<epsilon and sigma<epsilon, the accepted table has circuits of size at most 2^{max{beta,sigma}m+o(m)}, contradicting soundness. Around beta=epsilon the obstruction becomes tight, indicating that any valid source must be globally sequential or pay threshold-scale seek cost.
- Transfer certificate needed: A formal block-to-bit circuit simulation plus a density-preserving carrier extraction showing that sequential explicitness is sufficient for E search, while random access, block access, and advice are excluded from the target-preserving interface.

## Next Experiment

Audit one candidate global sequential invariant, such as a time-bounded Kolmogorov/decompression transcript, and test whether its verifier secretly provides beta<epsilon block seek or merely performs forbidden circuit enumeration.
