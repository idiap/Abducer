# cycle-0059

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: XOR carrier sparse-sketch audit

## Candidate Lemma

For the XOR SAT carrier, an unrestricted sparse quotient-polynomial audit is equivalent, up to sparse-evaluation and point-patching overhead, to the desired general-circuit lower bound for H_N. It is a valid upper-bound falsifier but not an independent source lower-bound certificate.

## Definitions

- source object: H_N(x)=parity over m_N=N^q generated SAT instances of length L_N=(log N)^d, measured against nonuniform fan-in-2 Boolean circuit size C(H_N).
- target object: SAT notin P/poly, obtained only through the separate polylog-query substitution bridge, not from this audit alone.
- controlled interface: barely-superlinear source lower bound C(H_N)>N^{1+epsilon} for infinitely many N versus sparse quotient-polynomial sketches of H_N.
- target-preserving condition: d>1, max{rho,q}<1+epsilon, generator cost C(G_N)<=N^rho, and no nonuniform SAT-label leakage inside the generator.
- Let a_N(x) be the F_2 incidence vector of the generated formula multiset after parity cancellation, and let y_N(f)=SAT(f).
- SQP_all_N(H_N) is the minimum of S_T+A r+E N over arbitrary quotient-respecting transcripts T:{0,1}^N->{0,1}^r of circuit cost S_T and A-sparse F_2 polynomials P with P(T(x))=H_N(x) except on E inputs.

## Assumptions

- Circuit size is nonuniform and may hardwire constants depending on N and on the real SAT label vector y_N, unless explicitly forbidden.
- A point error on an N-bit input can be patched by an equality gate of O(N) size, so E bad inputs cost O(E N).
- The transcript class in SQP_all is unrestricted apart from semantic quotient-respect: a_N(x)=a_N(x') implies T(x)=T(x').

## Equations

- xor-carrier-incidence-form: `H_N(x)=\bigoplus_{j\le m_N} SAT(G_N(x,j))=\langle a_N(x),y_N\rangle_{\mathbb F_2}`. Valid when: Valid when the generator outputs only length L_N SAT formulas and duplicate formulas are counted modulo two.
- sparse-sketch-upper-bound: `C(H_N)\le S_T+O(A r+E N)`. Valid when: Valid when P has A monomials over r transcript bits and differs from H_N on at most E inputs.
- unrestricted-sqp-equivalence: `SQP^{all}_N(H_N)\le C(H_N)+O(1)\quad\text{and}\quad C(H_N)\le O(SQP^{all}_N(H_N))`. Valid when: Valid when the audit permits arbitrary quotient-respecting transcripts, including the one-bit transcript T(x)=H_N(x).

## Attempted Derivation

- Start with the XOR carrier H_N(x)=<a_N(x),y_N> over F_2 and keep the stable target bridge max{rho,q}<1+epsilon.
- Try to replace the direct general-circuit lower bound C(H_N)>N^{1+epsilon} by hardness against sparse quotient-polynomial sketches.
- Any sketch with transcript cost S_T, support A, dimension r, and E errors gives C(H_N)<=S_T+O(A r+E N). This is a valid upper-bound falsifier.
- For the reverse direction, if unrestricted quotient transcripts are allowed, choose T(x)=H_N(x), r=1, and P(z)=z. Then SQP_all_N(H_N)<=C(H_N)+O(1).
- Thus unrestricted sparse-sketch hardness is equivalent to the original source lower bound and does not reduce the proof burden.
- Restricting transcripts to label-free incidence features makes the falsifier meaningful, but the derivation then needs an extraction theorem from arbitrary small H_N circuits to those features.

Blocking gap: No nonrelativizing locality-extraction theorem is known that converts an arbitrary small circuit for the real SAT-XOR carrier into a subthreshold label-free incidence transcript; relativizing planted-control examples block the naive argument.

## Falsifiers

- tautological transcript falsifier: T=H_N, r=1, P(z)=z collapses any unrestricted sparse-sketch audit
- structured sparse-polynomial falsifier: S_T+A r+E N<N^{1+epsilon-o(1)} gives an explicit upper bound for H_N
- nonuniform leakage through SAT-label-dependent transcript features
- relativizing planted-control oracle blocking locality extraction
- threshold collapse if max{rho,q} reaches 1+epsilon
- model mismatch if the source lower bound is proved only for structured sketches but advertised as a general-circuit lower bound

## Learning

Cycle 59 identifies a conservation law for the XOR-carrier audit: unrestricted sparse quotient-polynomial hardness is not a simplification of the source lower bound, since T=H_N is an admissible one-bit quotient transcript. The valid contribution is a sharper quarantine: sparse sketches remain concrete upper-bound falsifiers, while any proof-relevant sketch lower bound now needs a named label-free transcript class plus a nonrelativizing extraction theorem. The main P != NP conjecture is untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and extraction stress test.`
- Rationale: The branch needs to know whether sparse quotient-polynomial hardness is a genuine source simplification or only a disguised C(H_N) lower bound. A concrete leakage interpolation exposes the exact point where the audit becomes tautological.
- Situation seed: Fix d=2, choose q in ((1+epsilon)/2,1+epsilon), and let H_N be the parity of N^q generated 3SAT instances of length (log N)^2 from a total-cost N^rho generator with rho<1+epsilon. Compare local label-free incidence transcripts against an unrestricted quotient transcript family containing H_N itself.
- Varied variable: Transcript leakage class: from local linear incidence projections, to sparse coordinate hash sketches, to arbitrary quotient-respecting circuits.
- Held-fixed controls: polylog query length L_N=(log N)^2, target bridge parameters max{rho,q}<1+epsilon, nonuniform SAT substitution model for the target consequence, generator receives no SAT-label advice, source threshold C(H_N)>N^{1+epsilon}
- Expected observation: Local incidence sketches may require large sparse support on random-looking generators, but the moment the transcript class admits the carrier output, support A=1 and r=1 collapse the audit. This identifies nonuniform transcript leakage as the decisive falsifier.
- Transfer certificate needed: A formal nonrelativizing extraction theorem: every subthreshold general circuit for the real SAT-XOR carrier must induce a label-free structured incidence transcript with total cost below N^{1+epsilon-o(1)}. Without this certificate, the experiment cannot promote sketch hardness to a source lower bound.

## Next Experiment

Formalize the local-linear incidence transcript class for the XOR SAT carrier and compute the minimum sparse F_2 support needed under a random-generator model, while auditing whether any extraction from arbitrary circuits to that class can avoid the planted-control relativization falsifier.

# Barrier-Aware Lower-Bound Route: KW Fanout-Erasure Gate

## Candidate Lemma

A deterministic KW lower bound c(m) for SAT_m gives a valid De Morgan formula lower bound 2^{c(m)}, but it transfers to SIZE(m^k) only if c(m)>log F_SIZE(m^k,m). Since D(KW_f)<=m+1 and F_SIZE(s,m)<=2^{O(s)}, the route cannot prove superlinear polynomial circuit lower bounds.

## Definitions

- source object: deterministic communication lower bound for the Karchmer-Wigderson relation KW_{SAT_m} of the total m-bit SAT encoding predicate.
- target object: De Morgan formula size, or a named circuit class C with an explicit fanout-erasure bound F_C(s,m).
- controlled interface: KW theorem plus circuit-to-formula unfolding; reductions preserve the same input length m and do not add padding or advice.
- target-preserving condition: the source bound must satisfy c(m)>log_2 F_C(m^k,m) before excluding C-size m^k SAT deciders.

## Assumptions

- SAT_m is totalized by rejecting malformed encodings, so KW_{SAT_m} is a standard total-function KW relation.
- The target is nonuniform unless a separate uniform formula-simulation certificate is supplied.
- For unrestricted circuits the only generic fanout-erasure guarantee used is formula size at most 2^{O(s)}.
- The proof object may be non-natural, but fanout leakage is a separate valid obstruction.

## Equations

- KW_exact: `D(KW_f)=\lceil \log_2 L_{form}(f)\rceil \pm O(1)`. Valid when: Valid when f is a total Boolean function and deterministic KW protocols are matched with De Morgan formulas.
- circuit_transfer_threshold: `D(KW_f)>\log_2 F_C(s,m) \;\Rightarrow\; f\notin C[s]`. Valid when: Applies after the reduction names a circuit class C and proves its fanout-erasure bound F_C without advice leakage.
- unrestricted_collapse: `D(KW_f)\le m+1,\quad \log_2 F_{SIZE}(m^k,m)=O(m^k)`. Valid when: Requires unrestricted m-input Boolean circuits and the trivial KW protocol where Alice sends her whole input.

## Attempted Derivation

- Apply the KW theorem to translate a deterministic communication lower bound c(m) into L_form(SAT_m)>=2^{c(m)}.
- To attack SIZE(m^k), compose with a target compiler: every size-s target circuit must have an equivalent formula of size at most F_C(s,m).
- For unrestricted circuits use only F_SIZE(s,m)<=2^{O(s)}, so the needed source threshold is c(m)>O(m^k).
- But KW communication is at most m+1 by sending the whole yes-input; hence the threshold is impossible for every k>1.

Blocking gap: No size-preserving or subexponential fanout-erasure compiler from arbitrary polynomial-size SAT circuits to formulas is known or plausible.

## Falsifiers

- Padding falsifier: L_rho(x,p)=SAT_n(x) on M=n^rho bits has KW cost at most n+1 while the SIZE(M^k) transfer threshold is Omega(M^k).
- Threshold falsifier: even a maximal c(m)=m KW lower bound cannot cross the unrestricted circuit threshold O(m^2) for k=2.
- Compiler falsifier: fanout-sharing DAGs show that a universal polynomial F_SIZE(s,m) would need a semantic miracle, not mere syntactic unfolding.
- Barrier falsifier: converting a KW proof into a dense poly(N)-constructive truth-table property would re-enter the natural-proofs audit; KW syntax alone is not a valid escape.

## Learning

Cycle 59 isolates the KW route exactly: it is a valid formula lower-bound bridge, but direct P-vs-NP transfer collapses because D(KW_f)<=m while eliminating unrestricted fanout from SIZE(m^k) needs KW cost Omega(m^k). Padding gives a concrete target-preserving falsifier.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for KW-to-P transfer claims.`
- Rationale: The route needs a quantitative target-preserving test because KW lower bounds are exact for formulas but lose fanout when aimed at circuits.
- Situation seed: Padded SAT family L_rho on M=n^rho input bits, where the first n bits encode SAT_n and all remaining bits are ignored.
- Varied variable: padding exponent rho.
- Held-fixed controls: The source proof object remains deterministic KW communication for the full M-bit total predicate., The target remains nonuniform SIZE(M^k) with no advice or promise leakage., Malformed encodings are rejected uniformly so the KW relation is total., Only the generic circuit-to-formula unfolding F_SIZE(s,M)<=2^{O(s)} is allowed.
- Expected observation: D(KW_{L_rho})<=n+1=M^{1/rho}+1 while the transfer threshold is Omega(M^k); increasing rho makes the gap polynomially worse.
- Transfer certificate needed: A valid transfer would need log F_C(M^k,M)<=O(M^{1/rho}) for the named target class, or a proof that padding is disallowed by the reduction.

## Next Experiment

Audit branching-program lower bounds through the same compiler lens: name the BP model, its circuit simulation direction, and the exact threshold needed before any SIZE(poly) claim is valid.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Low-image generated anti-ball MCSP carriers are quantitatively non-large under every sublinear Hamming fattening, while any polynomial-time decidable dense projection that still excludes small circuits is exactly a Razborov-Rudich-style natural useful property. Thus projection/locator repair must remain sparse and non-indexed, or it becomes a barrier object rather than a target-preserving carrier.

## Definitions

- source object: a deterministic advice-free generator G_m that emits at most 2^{D m+o(m)} truth tables T_{m,j} of length N=2^m together with generated nonblackbox anti-ball proofs against circuits of size s_m=2^{theta m}.
- target object: the E-uniform multiplexed language L_G whose input encodes a padded length m, a row rank j, and an address x, with desired unrestricted circuit lower bound 2^{delta n}.
- controlled interface: E-canonical unranking of distinct generated rows, sequential proof generation, no subthreshold indexed row decoder, and no nonuniform locator for hard rows.
- target-preserving condition: for kappa-dense source lengths and image entropy D, the transfer is valid only when theta is below the verifier leakage cap and delta<theta/(kappa(1+D)).
- Hamming fattening B_R(F_m) is the union of radius-R Hamming balls around the generated row set F_m in {0,1}^N.
- Natural-size projection means measure at least 2^{-poly(m)} inside {0,1}^N and decidability by circuits polynomial in N.

## Assumptions

- The carrier row set F_m has distinct-image entropy D: |F_m|<=2^{D m+o(m)}.
- Every generated row is proved outside the Hamming ball of every circuit of size below 2^{theta m}; exact MCSP extraction uses the row itself, not the fattened set.
- The generator and unranking are E-uniform and advice-free; proof streams may be exponentially long but are deterministically locatable from m and rank.
- The target consequence is route-level E lower bounds, not a proof of P != NP.

## Equations

- image_entropy: `|F_m| \le 2^{D m+o(m)},\quad N=2^m,\quad s_m=2^{\theta m}.`. Valid when: Valid when the source carrier has E-canonical distinct-image unranking and fixed constant image entropy.
- sublinear_fattening_measure: `\mu(B_R(F_m)) \le 2^{D m+o(m)}\sum_{i\le R}{N\choose i}2^{-N} \le 2^{D m+O(R\log(N/R))-N}.`. Valid when: Valid when 1\le R\le N/2 and the bound is only a union-volume upper estimate.
- rho_radius_specialization: `R=N^{\rho},\ 0<\rho<1 \quad\Rightarrow\quad \mu(B_R(F_m)) \le 2^{-N+O(N^{\rho}m)+O(Dm)}.`. Valid when: Valid when the fattening radius is sublinear in the truth-table length N.
- multiplexed_extraction: `\delta < \frac{\theta}{\kappa(1+D)}.`. Valid when: Applies after the reduction preserves kappa-dense lengths, uniform unranking, and the MCSP threshold theta.
- natural_projection_gate: `\mu(U_m)\ge 2^{-m^a}\ \wedge\ U_m\cap SIZE(2^{\theta m})=\emptyset\ \wedge\ U_m\in P/poly(N) \Rightarrow U_m\text{ is a useful natural property}.`. Valid when: Valid when constructivity is measured on truth tables of length N and largeness is polynomial in m.

## Attempted Derivation

- Let F_m be the generated distinct row set, |F_m|<=2^{D m+o(m)}, N=2^m.
- For radius R, bound the projection measure by the union of Hamming ball volumes: mu(B_R(F_m))<=|F_m| Vol(N,R)/2^N.
- For R=N^rho with rho<1, Vol(N,R)<=2^{O(N^rho log N)}, hence mu<=2^{-N+o(N)}; this is far below 2^{-poly(m)} and therefore non-large.
- The existing multiplexing extraction from an actual generated hard row remains unchanged: padded rank/address inputs give delta<theta/(kappa(1+D)).
- Try to repair locatability by replacing F_m with a dense decidable U_m containing F_m and excluding all small circuits.
- If U_m has measure at least 2^{-poly(m)} and P/poly(N) constructivity, then U_m is a useful natural property against SIZE(2^{theta m}); this collides with the natural-proofs barrier under standard PRF assumptions.
- If U_m is obtained by sublinear fattening, it avoids largeness but still does not provide a selector for a hard center. If it is obtained by near-half fattening, anti-ball soundness for centers does not imply soundness for all of U_m.

Blocking gap: No generated nonblackbox proof currently supplies a sparse, advice-free, non-indexed row source with exact anti-ball soundness and without dense constructive projection.

## Falsifiers

- falsifier: a proposed source whose projection has natural density and poly(N) constructivity while excluding SIZE(2^{theta m}) is a natural-proof object, not a valid hidden carrier.
- falsifier: subthreshold indexed membership, nearest-center recovery, or interval restart gives circuits for generated rows below the claimed MCSP threshold.
- falsifier: using Hamming fattening as the source target is invalid unless every fattened table, not only every center, is proved far from small circuits.
- falsifier: image entropy D growing with m collapses the extracted exponent delta<theta/(kappa(1+D)) to zero.
- falsifier: nonuniform locators for hard rows preserve existential hardness but destroy the E-uniform target consequence.

## Learning

Cycle 59 contributes a quantitative projection dichotomy. Low-D generated anti-ball carriers stay safely non-large under every sublinear Hamming locator repair, with measure 2^{-N+o(N)}, so the natural-proofs barrier is not triggered there. But any repair that makes the projection natural-size and poly(N)-decidable while preserving small-circuit exclusion becomes a useful natural property. Thus the next source theorem must be sparse and generated, not dense and locatable; the carrier-to-E transfer remains valid only conditionally.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The branch needs a concrete quantitative test for the projection/locator obstruction; another abstract anti-ball slogan would not decide whether sparse generated proofs stay outside naturalness while preserving MCSP extraction.
- Situation seed: For each m, imagine a deterministic sequential transducer G producing M=2^{D m} truth tables T_{m,j} of length N=2^m with generated nonblackbox proofs that dist(T_{m,j},SIZE(2^{theta m}))>0. Form U_{m,r}=the Hamming r-neighborhood of all generated rows and ask whether U_{m,r} can serve as the locatable projection.
- Varied variable: The Hamming radius exponent rho in r=N^rho, then the transition to near-half radius r=N/2-t.
- Held-fixed controls: MCSP threshold s_m=2^{theta m} with theta below the verifier leakage cap., Distinct-image entropy D is constant and E-canonical unranking is available., Source lengths are kappa-dense and all locators are advice-free., Target extraction uses exact generated rows, not arbitrary nearby tables., No subthreshold indexed decoder or nearest-center oracle is allowed.
- Expected observation: For every rho<1, U_{m,r} has measure 2^{-N+o(N)}, so it is non-large and does not trigger natural proofs but also gives no dense locator. Near-half radius can reach natural measure, but center anti-ball proofs no longer certify that U_{m,r} excludes small circuits.
- Transfer certificate needed: A formal certificate must prove E-uniform center generation, exact row anti-ball soundness against unrestricted SIZE(2^{theta m}), bounded image entropy D, and absence of any dense poly(N)-decidable useful projection before the intuition may enter the proof queue.

## Next Experiment

Audit nonblackbox circuit-SAT/UNSAT certificate families as generated anti-ball proofs: vary whether the proof reasons symbolically about all SIZE(2^{theta m}) circuits or implicitly enumerates a dense challenge list, and test it against the projection-measure, decoder-leakage, and naturality gates.
