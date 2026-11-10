# cycle-0065

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

In the beta=0 XOR-carrier route, any O(L_N)-searchable, inverse-polynomially large proof-mediated certificate relation for C(H_{N,y})>N^{1+epsilon} becomes a Razborov-Rudich natural property of the length-L_N label function. Hence this proof-mediated escape is invalid under the standard PRF natural-proofs hypothesis unless the certificate family is nonlarge, nonconstructive, not a truth-table property, or explicitly nonrelativizing.

## Definitions

- source object: for an explicit generator G_N and arbitrary label vector y in {0,1}^{M_N}, H_{N,y}(x)=sum_{u in U_N} A_N(x,u)y_u mod 2, where U_N={0,1}^{L_N}, M_N=2^{L_N}, and A_N is the parity incidence of the Q_N generated SAT-query slots.
- target object: the actual label vector y=SAT_{L_N} over formula codes of length L_N=(log N)^d, d>1, with target consequence SAT notin SIZE(n^c) for every fixed c, hence NP not subset P/poly only if the carrier lower bound is valid.
- controlled interface: beta=0 polylog-query substitution with Q_N=N^{q+o(1)}, generator cost N^{rho+o(1)}, source threshold S_N=N^{1+epsilon}, and target transfer cost N^{max{rho,q}+o(1)}.
- target-preserving condition: max{rho,q}<1+epsilon, the substituted SAT circuit uses the same nonuniform circuit model and no extra advice, and the certificate relation R_N(y,pi) is sound for the same source lower-bound model.

## Assumptions

- Nonuniform Boolean SIZE is the source and target model; G_N and the verifier V_N are explicit uniform families but circuits for SAT may be nonuniform.
- Certificate length is at most aL_N bits and V_N runs in M_N^b time on the full truth table y; exhaustive proof search is therefore polynomial in M_N.
- Soundness is same-theory: R_N(y,pi) implies C(H_{N,y})>S_N against unrestricted Boolean circuits on N input bits.
- Largeness means Pr_y[exists pi R_N(y,pi)] >= M_N^{-b'} over all M_N-bit label vectors; without this density the naturalness conclusion is not claimed.
- The barrier use is conditional on standard pseudorandom functions against polynomial-size circuits; the lemma is a route-level no-go, not an unconditional P != NP theorem.

## Equations

- beta_zero_substitution: `C(H_{N,y}) \le N^{\rho+o(1)}+N^{q+o(1)}L_N^c=N^{\max\{\rho,q\}+o(1)}`. Valid when: Valid when G_N is explicit, target queries have length L_N, and the substituted target circuit carries no additional advice.
- rank_counting_large_hardness_property: `\Pr_{y\leftarrow\{0,1\}^{M_N}}[C(H_{N,y})\le S_N]\le 2^{O(S_N\log S_N)-r_N}`. Valid when: Valid when A_N is viewed as an F_2 linear map from label vectors to carrier truth tables and small N-input circuits are counted nonuniformly.
- search_time_for_proofs: `T_{decide}(\mathcal{Q}_N)\le 2^{aL_N}M_N^b=M_N^{a+b}`. Valid when: Valid when certificates have at most aL_N bits, the verifier runs in M_N^b time, and M_N equals 2^{L_N}.
- usefulness_against_target_circuits: `\mathcal{Q}_N\cap SIZE(L_N^c)=\emptyset \quad \text{for every fixed }c`. Valid when: Applies after the beta-zero substitution bridge preserves the same circuit model, the same advice convention, and the threshold S_N=N^{1+epsilon}.

## Attempted Derivation

- Fix the XOR carrier H_{N,y}=A_N y over F_2 and let r_N=rank(A_N). The map y -> H_{N,y} has kernel size 2^{M_N-r_N}.
- Count N-input Boolean functions with circuits of size at most S_N as at most 2^{O(S_N log S_N)}. Therefore the easy-label density is at most 2^{O(S_N log S_N)-r_N}.
- If r_N exceeds O(S_N log S_N)+Omega(log M_N), then the hardness property {y:C(H_{N,y})>S_N} is large. This is evidence of naturalness, not evidence for SAT.
- For a proof relation R_N with |pi|<=aL_N and verifier time M_N^b, the existential property Q_N(y)=exists pi R_N(y,pi) is decidable in M_N^{O(1)} time by exhaustive proof search.
- Soundness R_N=>C(H_{N,y})>S_N plus max{rho,q}<1+epsilon implies Q_N contains no label function y with SIZE(L_N^c) circuits for any fixed c, because substituting such a circuit into G_N yields H_{N,y} of size below S_N.
- Thus any large accepted set Q_N is constructive, large, and useful: exactly a natural property after encoding formula-code labels as length-L_N truth tables.

Blocking gap: The argument is conditional as a barrier diagnosis: it uses the standard PRF-based natural-proofs obstruction and does not rule out nonlarge SAT-specific proofs, omega(L_N)-length proofs, nonconstructive verifiers, or nonrelativizing proof-system semantics.

## Falsifiers

- falsifier: positive beta gives C(H_N)<=N^{q+beta c+o(1)} and caps the claimed all-exponent transfer.
- falsifier: low constructive incidence rank gives C(H_{N,SAT})<=S_T+O(r_N), killing the N^{1+epsilon} source lower bound.
- falsifier: an O(L_N)-searchable inverse-polynomially large proof certificate becomes a natural property, so it is not a valid barrier-escaping proof route under PRF assumptions.
- falsifier: label-dependent transcripts such as T_N=H_N collapse the audit and are nonuniform leakage, not source evidence.

## Learning

Cycle 65 closes a finite validation gap: short searchable proof certificates do not automatically escape natural proofs in the beta=0 XOR carrier. If they are large and sound, they form a valid natural property; if rank is low, there is a separate upper-bound falsifier. The surviving route is narrower: direct H_N lower bounds or nonlarge, nonconstructive, explicitly nonrelativizing proof objects.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The route has moved from black-box substitution to a beta=0 XOR carrier; the remaining claimed escape is proof-mediated, so the next useful test is whether finite certificates naturalize rather than another abstract hardness-magnification restatement.
- Situation seed: Fix a high-rank generated XOR carrier H_{N,y}=sum_u A_N(x,u)y_u mod 2 with L_N=(log N)^d, d>1, Q_N=N^q, max{rho,q}<1+epsilon, and add a Frege-like or IPS-like relation R_N(y,pi) asserting C(H_{N,y})>N^{1+epsilon}.
- Varied variable: Certificate length p_N=tau L_N, varying tau from O(1) through omega(1), while keeping verifier time polynomial in M_N=2^{L_N}.
- Held-fixed controls: The beta=0 target bridge with q,rho<1+epsilon and no extra advice leakage., The full truth-table label model y in {0,1}^{M_N} over formula-code inputs of length L_N., A high-rank incidence regime r_N>>N^{1+epsilon}log N, so random labels make H_{N,y} hard with high probability., Same-model soundness R_N(y,pi)=>C(H_{N,y})>N^{1+epsilon} against unrestricted Boolean circuits.
- Expected observation: For p_N=O(L_N), exhaustive certificate search is polynomial in M_N; if accepted labels have inverse-polynomial density, the certificate family is a natural property. For p_N=omega(L_N) or negligible density, the naturalness extraction breaks but the route loses a finite searchable witness.
- Transfer certificate needed: Prove that accepted certificates define a truth-table property of y and that usefulness transfers through the beta=0 substitution bridge; if the verifier uses proof-system semantics not reducible to y, certify the nonrelativizing feature before it may affect proof obligations.

## Next Experiment

Instantiate R_N with a named proof system, e.g. Extended Frege or IPS, and test whether an LB certificate for C(H_{N,y})>N^{1+epsilon} has O(L_N)-bit searchable descriptions, inverse-polynomial label density, and truth-table soundness; otherwise record the precise escape parameter.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

A uniformly searchable deterministic oracle proof of a truth-table lower bound naturalizes if its verifier reads only O(log N) table bits. Hence a proof-mediated MCSP/HCC route avoids the natural-proofs pressure only by losing all-truth-table soundness, uniform search, or logarithmic-query locality.

## Definitions

- source object: deterministic oracle verifier V^y(1^m,pi) for the statement LB_s(y): CC_m(y)>s, where y in {0,1}^N is an m-bit truth table and N=2^m.
- target object: nonuniform Boolean circuits SIZE_m(s), usually s=m^k, represented by their truth tables on {0,1}^m.
- controlled interface: query budget q(m) to y, verifier runtime poly(N), and a uniform Search(1^m) producing an accepted proof pi_m for y_m=TT(SAT_m).
- target-preserving condition: soundness is universal over all m-bit truth tables y; if CC_m(y)<=s then V^y(1^m,pi) rejects every proof pi.

## Assumptions

- Model is an oracle-proof lower-bound verifier whose input truth table is accessed by random access, not by a compressed SAT promise alone.
- Uniformity regime requires Search to run in poly(N) or an explicit equivalent; otherwise the induced recognizer has nonuniform proof advice.
- The lower-bound target is the same SIZE_m(s) class used in the verifier soundness statement; no padding or advice leakage changes s.
- The verifier is deterministic in this lemma; public randomness requires the separate seed-fixing lemma below.

## Equations

- truth_table_length: `N=2^m`. Valid when: Valid when N=2^m and the truth table lists all m-bit inputs in the fixed order.
- cylinder_density: `\mu(P_m) \ge 2^{-q(m)} \ge N^{-a} \quad \text{if } q(m)\le a\log_2 N`. Valid when: Applies when deterministic V follows one accepting adaptive transcript for y_m and pi_m.
- usefulness: `P_m \cap \{y:CC_m(y)\le s\}=\emptyset`. Valid when: Requires soundness over all truth tables, not merely over SAT encodings or promise instances.
- constructivity: `T_{P_m}(N) \le T_{Search}(N)+poly(N,|\pi_m|,q(m))`. Valid when: Valid when Search outputs the accepted proof family without nonuniform advice leakage.

## Attempted Derivation

- Let y_m=TT(SAT_m), N=2^m, and s=m^k. The proposed source claim is a proof pi_m of LB_s(y_m): CC_m(y_m)>s.
- Assume a deterministic oracle verifier V^y checks LB_s(y) with q queries and is sound for every m-bit truth table y of circuit complexity at most s.
- Assume Search(1^m) outputs an accepted pi_m for y_m in poly(N) time. Define P_m(z)=1 iff V^z(1^m,pi_m) accepts.
- For the accepting run on y_m, fix the adaptive transcript of at most q queried coordinates and answers. Every z matching those answers follows the same accepting path, so P_m has density at least 2^{-q}.
- Soundness gives P_m subseteq {z: CC_m(z)>s}. Thus P_m is useful against SIZE_m(s).
- If q<=a log N and Search is uniform, P_m is a poly(N)-constructive property of density at least N^{-a}. This is a valid natural property and faces the PRF falsifier pressure for the same target class.

Blocking gap: The argument does not rule out proof systems whose verification reads omega(log N) truth-table bits, whose proof family is not uniformly searchable, or whose soundness is only for a promise encoding of SAT rather than all truth tables.

## Falsifiers

- falsifier: a verifier that reads the entire truth table has q=N, so the accepting cylinder may have exponentially tiny density and the naturalness transfer is invalid.
- falsifier: a proof pi_m existing only as nonuniform advice gives at most an advised recognizer, not standard poly(N)-constructive naturalness.
- falsifier: PCP soundness only for syntactically valid SAT encodings does not imply usefulness against arbitrary SIZE_m(s) truth tables.
- falsifier: constant public-coin soundness cannot be union-bounded over 2^{Theta(s log s)} low-circuit truth tables.

## Learning

The new gate is proof-mediated rather than truth-table brute force: a searchable local proof of CC(TT(SAT_m))>m^k is still natural if q=O(log N). Thus the valid escape is not the word proof, but superlogarithmic table access, nonuniform/nonconstructive proof selection, or loss of all-truth-table usefulness.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for proof-mediated MCSP/HCC routes.`
- Rationale: Cycle 64 left open whether proof-mediated certificates avoid constructivity. A concrete oracle-verifier experiment tests whether locality plus uniform search recreates a large constructive useful property.
- Situation seed: For each m, set y_m=TT(SAT_m) and s=m^k. Imagine a Psys verifier V^y that checks a claimed proof of CC_m(y)>s while querying y only on selected formula indices.
- Varied variable: The verifier truth-table query budget q, varied from beta log N to N^beta while proof length and soundness form are held fixed.
- Held-fixed controls: Target class remains SIZE_m(m^k) on the unpadded m-bit input length., Soundness is required over all m-bit truth tables, not only SAT-like encodings., Search(1^m) must output the accepted SAT proof in poly(N) time., No nonuniform advice beyond m and the generated proof is allowed in the property recognizer.
- Expected observation: At q=O(log N), the accepting transcript has polynomial density and yields a valid natural property useful against SIZE_m(m^k). Once q=omega(log N), largeness falls below the standard polynomial threshold, so the natural-proof obstruction no longer follows from this gate alone.
- Transfer certificate needed: A formal certificate must provide all-truth-table soundness, uniform proof search or logarithmic proof enumeration, and seed fixing for randomized verifiers before the intuition may enter the proof queue.

## Next Experiment

Instantiate the gate for an EF/Frege/PCP-style verifier of LB_s(y): CC_m(y)>m^k; determine whether the verifier reads O(log N) table bits, has all-truth-table soundness, and admits poly(N) proof search, or else record the first failed condition as the route falsifier.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Skeleton-opening leakage: a generated anti-ball MCSP carrier claiming CC(T_m)>2^{theta m} is invalid if its proof skeleton A_m of length 2^{mu m+o(m)} and an indexed RAM opener of time 2^{lambda m+o(m)} recover every bit T_m[x] with max{mu,lambda}<theta. Hardwiring A_m and unrolling the opener gives an unrestricted circuit for the row.

## Definitions

- source object: a generated anti-ball MCSP carrier consisting of truth tables T_m of length N=2^m, optional proof streams Pi_m, and a claimed threshold CC(T_m)>2^{theta m} for unrestricted circuits.
- target object: an E-uniform language L obtained by low-D row multiplexing and kappa-gap padding, intended to satisfy circuit lower bounds 2^{delta n} on all large input lengths.
- controlled interface: a skeleton A_m plus opener O_m that, if present, maps (x,A_m) to T_m[x] for every x in {0,1}^m and can be hardwired into nonuniform circuits.
- target-preserving condition: the row/proof generator is advice-free with constant exponential clock, the image entropy D and density gap kappa are constant, and no subthreshold skeleton-opening representation exists.
- CC(T_m) is unrestricted nonuniform Boolean circuit size of the m-input function whose truth table is T_m.
- mu is the skeleton length exponent, lambda is the indexed opening-time exponent, and theta is the asserted MCSP no-side exponent.

## Assumptions

- Circuit model is unrestricted nonuniform Boolean circuits; fixed skeleton bits count through RAM-to-circuit lookup or through explicit hardwiring.
- The opener is correct for all x in {0,1}^m, not merely for verifier queries or sampled locations.
- theta, mu, lambda, D, and kappa are fixed constants on the carrier length sequence, with 0<theta<1.
- The source soundness claim is about the same generated row T_m, not about an advice-selected hard row elsewhere.
- Low-D multiplexing and kappa-padding are E-canonical and introduce no nonuniform length selector.

## Equations

- skeleton-leakage-upper-bound: `\mathrm{CC}(T_m) \le 2^{(\max\{\mu,\lambda\}+o(1))m}`. Valid when: Valid when one fixed skeleton opens all row bits and the RAM-to-circuit simulation hardwires its memory.
- source-falsifier-threshold: `\max\{\mu,\lambda\}<\theta \Longrightarrow \neg(\mathrm{CC}(T_m)>2^{\theta m})`. Valid when: Requires the source threshold to be an unrestricted nonuniform MCSP no-side claim for the same row.
- surviving-conditional-extraction: `\delta < \frac{\theta}{\kappa(1+D)}`. Valid when: Applies after low-image multiplexing, kappa-gap padding, E-canonical unranking, and sound row hardness are all preserved.

## Attempted Derivation

- Fix a carrier length m and a generated row T_m with asserted unrestricted MCSP hardness greater than 2^{theta m}.
- Assume a skeleton A_m of length 2^{mu m+o(m)} and an indexed opener O_m that returns T_m[x] for every m-bit x in time 2^{lambda m+o(m)}.
- Hardwire A_m into a nonuniform circuit and simulate the opener; RAM lookup or direct advice input costs at most 2^{max{mu,lambda}m+o(m)} gates.
- If max{mu,lambda}<theta, this circuit is smaller than the asserted MCSP threshold, so the proposed source is unsound.
- For a surviving source, additionally require a row-bit generator exponent gamma satisfying theta<=gamma=O(1), then the existing low-D multiplexing bridge gives delta<theta/(kappa(1+D)).

Blocking gap: No generated anti-ball source is known that proves unrestricted row hardness while avoiding every subthreshold skeleton-opening representation and maintaining a bounded E clock.

## Falsifiers

- falsifier: a Merkle, checkpoint, PCP, or transcript skeleton with length exponent mu and indexed opening exponent lambda satisfying max{mu,lambda}<theta.
- falsifier: an indexed row-bit generator with gamma<theta on infinitely many carrier lengths, since its own computation unrolls to small circuits.
- falsifier: gamma_m unbounded along carrier lengths, because fixed E-uniform extraction is no longer valid under the same padding map.
- falsifier: a nonuniform selector for the hard row or hard proof location; it supplies row hardness outside the intended uniform target.
- falsifier: easy sparse tables, parity-like rows, or low-complexity fillers accepted by the verifier; these violate universal MCSP no-side soundness.

## Learning

Cycle 65 upgrades the nonuniform-skeleton warning into an exact falsifier: compressed proof skeleton plus indexed opening below theta collapses the claimed MCSP row hardness. A valid generated source must live in the narrow window theta<=gamma=O(1) and avoid every omega<theta opener. This is route-level progress, not evidence that P != NP is solved.

## Gedanken Experiment Design Seed

- Need decision: `design-now-as-falsifier-probe`
- Rationale: The branch now needs to test whether concrete generated anti-ball proof formats secretly contain a low-exponent opening skeleton rather than merely being advice-free streams.
- Situation seed: A Merkle-checkpointed generated anti-ball proof family for kappa-dense rows T_m, where a root plus checkpoint skeleton A_m and deterministic opener O_m return T_m[x] before or during verification of global anti-ball constraints.
- Varied variable: omega=max{mu,lambda}, the skeleton-opening exponent swept below, at, and above the asserted hardness exponent theta.
- Held-fixed controls: unrestricted nonuniform circuit model for MCSP row hardness, fixed threshold CC(T_m)>2^{theta m} with 0<theta<1, fixed image entropy D and density gap kappa, advice-free deterministic generation of the row/proof stream, E-canonical unranking and padding used by the carrier transfer
- Expected observation: For omega<theta the source is invalid by hardwiring; for omega>=theta the leakage falsifier disappears but the source still needs a nonblackbox proof of anti-ball hardness. The extraction exponent remains delta<theta/(kappa(1+D)) only in the valid regime.
- Transfer certificate needed: A formal RAM/advice-to-circuit simulation for skeleton openings, plus a proof that any proposed source has no subthreshold opener while its row-bit computation has bounded constant exponential clock.

## Next Experiment

Instantiate the ledger on three candidate proof formats: Merkle/checkpoint openings, PCP-style local transcripts, and pure sequential generated streams; compute mu, lambda, gamma, and decide whether each is a valid source candidate or a falsifier.
