# cycle-0057

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: XOR quotient carrier, low-degree feature-sketch gate

## Candidate Lemma

For the generated XOR carrier, any subthreshold quotient-feature representation of the SAT-induced parity gives a valid upper-bound falsifier for the proposed N^{1+epsilon} source lower bound. Affine-rank and codebook tests are special cases; the next gate is low-degree dependence on a small computable feature vector.

## Definitions

- source object: H_N^{xor}(z)=\oplus_{j\le M_N} SAT(F_{N,j}(z)) on N input bits, with M_N=\lfloor N^q\rfloor and query length L=(\log N)^d, d>1.
- target object: SAT lower bounds against P/poly, hence NP not subset P/poly, obtained only through the XOR carrier substitution bridge.
- controlled interface: a P/poly generator G_N of size N^rho outputs the M_N length-L SAT queries; a SAT circuit of size L^c is substituted independently into every generated query.
- target-preserving condition: max{rho,q}<1+epsilon and L=(\log N)^d ensure every fixed SAT exponent c contributes only N^{o(1)} overhead, with no nonuniform advice depending on z beyond G_N.

## Assumptions

- Circuits are nonuniform Boolean circuits of fan-in two unless a restricted class is explicitly named.
- The quotient universe identifies length-L formulas only by SAT-preserving equivalence relevant to the parity incidence vector; duplicate even multiplicities cancel over F_2.
- A feature sketch consists of a circuit T_N:{0,1}^N -> {0,1}^{r_N} of size S_T and an arbitrary hardwired F_2 polynomial P_N of degree at most t in r_N variables.
- The representation may fail on E_N inputs; equality patches of size O(E_N N) are charged explicitly.

## Equations

- xor_carrier: `H_N^{xor}(z)=\bigoplus_{j=1}^{\lfloor N^q\rfloor} SAT(F_{N,j}(z))`. Valid when: Valid when the carrier is the repaired XOR aggregation route and every generated query has length L=(log N)^d.
- target_substitution: `SAT\in SIZE(n^c)\Rightarrow C(H_N^{xor})\le N^\rho+N^q\,L^{c+O(1)}=N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies after the generator size is N^rho, q is fixed below the threshold, and L is polylogarithmic in N.
- magnification_implication: `C(H_N^{xor})>N^{1+\epsilon}\ \wedge\ \max\{\rho,q\}<1+\epsilon\Rightarrow SAT\notin P/poly`. Valid when: Requires the target-preserving complexity-class transfer for every fixed SAT circuit exponent c with no advice leakage.
- feature_sketch_upper_bound: `C(H_N^{xor})\le S_T+O\!\left(\sum_{i=0}^{t}\binom{r_N}{i}\right)+O(E_NN)`. Valid when: Valid when H_N agrees off E_N inputs with a degree-t polynomial in the computed feature vector T_N(z).
- constant_degree_threshold: `r_N=N^\alpha,\ S_T=N^s,\ E_N=N^\eta\Rightarrow C(H_N^{xor})\le N^{\max\{s,\alpha t,1+\eta\}+o(1)}`. Valid when: Applies for constant t and polynomial-size parameters so the monomial count has exponent alpha times t.

## Attempted Derivation

- Start with the quotient incidence representation H_N(z)=<A_N(z),y_N> over F_2, where y_N is the SAT label vector on generated quotient classes.
- Cycle 56 handled the case A_N(z) lies in a low-rank affine subspace or in a small computable codebook; then hardwired basis parities or table entries compute H_N.
- Generalize: suppose a small circuit T_N computes r_N features and the composed label functional <A_N(z),y_N> equals a degree-t polynomial P_N(T_N(z)) except on E_N inputs.
- Implement T_N once, hardwire all coefficients of P_N, compute all degree-at-most-t monomials, XOR selected monomials, and patch the E_N exceptional inputs by equality tests.
- This yields C(H_N)<=S_T+O(sum_{i<=t} binom(r_N,i))+O(E_NN). Hence for r_N=N^alpha, S_T=N^s, E_N=N^eta, constant t, the source lower bound C(H_N)>N^{1+epsilon} is falsified whenever max{s,alpha t,1+eta}<1+epsilon.

Blocking gap: No method is known to prove that the real SAT-labelled quotient functional avoids all subthreshold low-degree feature sketches. Random-incidence or random-label counting does not transfer to SAT.

## Falsifiers

- A degree-t quotient-feature sketch with r=N^alpha and alpha t<1+epsilon is a concrete falsifier for the source lower bound.
- An error set of size E<N^epsilon is patchable by O(EN) equality gates and cannot be ignored.
- A SAT-label annihilator making <A_N(z),y_N> depend on few nonlinear features defeats high raw quotient rank.
- A proof that only shows random labels avoid the sketch class is not valid for real SAT without a nonrelativizing transfer certificate.
- Any hidden hardwiring of the SAT truth table into T_N is nonuniform leakage and invalidates the claimed source model.

## Learning

Cycle 57 adds a nonlinear conservation law for the XOR carrier. The source lower bound must beat low-degree quotient-feature sketches with threshold S_T+binom(r,<=t)+EN, so high rank or high codebook entropy is not valid evidence. The target-preserving bridge is unchanged, but the source obligation is narrower and more nonrelativizing.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the XOR carrier source lower bound.`
- Rationale: The affine-rank/codebook gate may miss nonlinear compression of the SAT-labelled parity. A concrete feature-sketch experiment tests whether the route is still pretending high incidence entropy is enough.
- Situation seed: Fix q in ((1+epsilon)/2,1+epsilon), rho<1+epsilon, and L=(log N)^d with d>1. Let G_N generate N^q length-L SAT formulas from z. After SAT-preserving parity quotienting, try to express H_N^{xor}(z) as a low-degree polynomial in a computable feature vector T_N(z).
- Varied variable: The feature dimension exponent alpha in r_N=N^alpha, with degree t held constant first and then allowed to grow slowly.
- Held-fixed controls: The target bridge parameters q,rho,d and the threshold max{rho,q}<1+epsilon are held fixed., The source model remains unrestricted nonuniform SIZE on N-bit inputs with claimed lower bound N^{1+epsilon}., The SAT labels are the real SAT truth table on length-L formulas, not random labels., Errors are charged by equality patching at cost O(E_NN), so E_N<N^epsilon is not a safe residual.
- Expected observation: If alpha t<1+epsilon and T_N has subthreshold size, then even a highly ranked quotient incidence map can yield an easy H_N. Random generators should defeat fixed sketches for random labels, but the experiment should expose whether SAT-specific symmetries or formula normal forms create a small feature representation.
- Transfer certificate needed: A valid proof queue may use the intuition only after obtaining a nonrelativizing real-SAT certificate that excludes all subthreshold low-degree quotient-feature sketches, or after proving a direct unrestricted circuit lower bound for H_N.

## Next Experiment

Formalize the degree-2 case: characterize whether Tseitin-style parity, formula-size, variable-incidence, or clause-type features give r=N^alpha with 2alpha<1+epsilon for the generated length-(log N)^d SAT queries.

# Barrier-Aware Lower-Bound Route: Lifted Communication Threshold Collapse

## Candidate Lemma

Two-party gadget lifting is a valid bridge from query lower bounds to communication lower bounds for a target-preserving lifted SAT carrier, but standard communication complexity has only a linear-in-input ceiling and therefore cannot certify SAT notin SIZE(m^k) for any k>1 without an additional nonstandard target compiler.

## Definitions

- source object: an outer Boolean function h:{0,1}^t->{0,1}, preferably a SAT_t encoding containing a projected OR_t slice, with query lower bound q(t).
- target object: the two-party lifted language F_{t,b}=h(g_b(x_1,y_1),...,g_b(x_t,y_t)) under the block partition, and unrestricted Boolean circuits SIZE(m^k) only through an explicit circuit-to-protocol transfer.
- controlled interface: a deterministic or randomized lifting theorem for a gadget g_b such as IP_b or IND_b, plus a separately named compiler turning target circuits into low-communication protocols.
- target-preserving condition: SAT_t must project to F_{t,b} by fixing one side of every gadget, with length m=Theta(tb), polynomial-time uniformity, and no nonuniform advice encoded in the fixed gadget side.

## Assumptions

- Choose b>=C log t for a gadget family where the relevant lifting theorem is known.
- Use a SAT_t encoding that contains a linear-size OR_t projection, giving R_dt(SAT_t)=Omega(t) for the queried slice.
- The reduction SAT_t <=_m^p F_{t,b} fixes gadget inputs uniformly and increases length from t to m=Theta(tb).
- The only attempted transfer to SIZE(m^k) is through ordinary two-party communication complexity under the same input partition.

## Equations

- lifted_input_length_ip: `m(t,b)=2tb`. Valid when: Valid when the inner gadget is IP_b with b bits on each side and the lifted function has exactly t independent gadget blocks.
- query_to_communication_lifting: `R^{cc}_{1/3}(h\circ g_b^t)\ge c\,b\,R^{dt}_{1/3}(h)`. Valid when: Applies when b is at least logarithmic in t and g_b satisfies the hypotheses of a standard randomized lifting theorem.
- sat_slice_query_lower_bound: `R^{dt}_{1/3}(SAT_t)\ge R^{dt}_{1/3}(OR_{\alpha t})=\Omega(t)`. Valid when: Valid when the chosen SAT encoding contains a uniform projected OR slice using alpha t live formula bits.
- communication_ceiling: `R^{cc}_{1/3}(F)\le D^{cc}(F)\le m+1`. Valid when: Valid for every total two-party Boolean function on m input bits because one party may transmit its whole input.
- certified_size_ceiling: `S_{cert}(m)\le O(R^{cc}(F))\le O(m)`. Valid when: Requires that the only circuit lower-bound bridge extracts size lower bounds from ordinary communication lower bounds under a fixed partition.

## Attempted Derivation

- Define F_{t,b}=SAT_t(IP_b(x_1,y_1),...,IP_b(x_t,y_t)) with b>=C log t and total length m=2tb.
- Use the projected OR slice inside SAT_t to obtain R_dt(SAT_t)=Omega(t).
- Apply the lifting theorem to get R_cc(F_{t,b})=Omega(tb)=Omega(m).
- Observe that SAT_t uniformly projects to F_{t,b}, so the lifted carrier is NP-hard and remains in NP.
- Try to infer F_{t,b} notin SIZE(m^k) from the communication lower bound.
- The inference stalls because ordinary two-party communication is always at most m+1, and any lower bound obtained from it is at most linear in the lifted length.

Blocking gap: There is no size-preserving compiler from unrestricted m^k-size Boolean circuits for F_{t,b} to protocols whose cost is below the linear communication ceiling.

## Falsifiers

- falsifier: IP_n is P-easy and has randomized communication complexity Omega(n), so linear communication hardness alone is not evidence against P.
- falsifier: the lifted SAT carrier with b=Theta(log t) is NP-hard and can have R_cc=Theta(m), yet this remains below every target threshold m^k with k>1.
- falsifier: sending one party's entire input gives D_cc(F)<=m+1 for every total lifted language, making any claimed superlinear standard-communication lower bound invalid.
- falsifier: padding the gadget length b increases the circuit lower-bound target to (tb)^k while the lifted communication lower bound increases only to Theta(tb).

## Learning

Cycle 57 isolates a valid bridge and a sharp failure mode: SAT gadget lifting can preserve NP-hardness and give R_cc(F)=Omega(m), but ordinary communication complexity is capped at m and therefore cannot certify SIZE(m^k) lower bounds for k>1. The route-level contribution is the threshold-collapse gate; it is not progress on P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for lifted-communication-to-P-vs-NP routes.`
- Rationale: The route has a concrete NP-hard carrier and a valid lifting theorem, so the decisive issue is quantitative target preservation rather than another abstract barrier citation.
- Situation seed: Take F_{t,b}=SAT_t(IP_b^t), fix one side of every IP gadget to project SAT_t into F_{t,b}, and audit the lower bound obtained from the SAT query lower bound through two-party lifting.
- Varied variable: The gadget length exponent beta in b=t^beta, including the standard beta=0 logarithmic case b=Theta(log t).
- Held-fixed controls: The outer predicate is the same uniform SAT_t encoding with a projected OR slice., The reduction SAT_t <=_m^p F_{t,b} is a projection with no advice leakage., The target circuit threshold is measured in the lifted length m=Theta(tb)., The proof object is ordinary randomized two-party communication complexity under the gadget partition.
- Expected observation: Increasing beta scales both the communication lower bound and the input length by the same factor; the ratio R_cc(F)/m stays Theta(1), so the certificate never approaches m^k for k>1.
- Transfer certificate needed: Before the intuition may affect P-vs-NP proof obligations, one needs a formal nonrelativizing compiler from SIZE(m^k) circuits for the lifted SAT carrier to a protocol model with cost o(m), or a different superlinear measure that still preserves the SAT projection.

## Next Experiment

Audit Karchmer-Wigderson and formula-depth transfers separately: determine whether a lifted SAT communication lower bound can validly certify formula-size or depth lower bounds while still failing for unrestricted SIZE(poly).

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Generated nonblackbox anti-ball proofs preserve the MCSP-carrier extraction. If, on kappa-dense input lengths m, an E-uniform source canonically un-ranks at most 2^{D m} tables T_{m,i} and generated proofs pi_{m,i}, and a sound verifier accepts only tables rho-far from every unrestricted circuit of size 2^{epsilon m}, then the multiplexed E language has circuit lower bound 2^{delta n} for every delta<epsilon/(kappa(1+D)). The radius rho is not charged for exact MCSP hardness when the forbidden centers already have size 2^{epsilon m}.

## Definitions

- source object: an E-uniform low-image family (T_{m,i},pi_{m,i}) with i<2^{D m}, generated or sequentially emitted in 2^{O(m)} time, not merely existentially certified.
- target object: a multiplexed E language L(i,x)=T_{m,i}(x) with final input length n=(1+D)m up to kappa-padding.
- controlled interface: a sound nonblackbox anti-ball verifier V whose acceptance implies distance from all unrestricted circuits at the declared size threshold.
- target-preserving condition: row/proof generation is advice-free, kappa-dense, low-image, and has no subthreshold bit decoder that would itself give circuits below 2^{epsilon m}.
- anti-ball soundness means every accepted row, or at least one canonically hard accepted row used by the multiplexer, is outside the Hamming ball around every small circuit.
- barrier posture: the generated low-image source is non-large, so it is outside the direct natural-proofs template unless the verifier acceptance expands to a dense constructive property.

## Assumptions

- epsilon,D,kappa are fixed positive constants with epsilon<1 and D=O(1).
- The verifier's soundness is mathematical, not just heuristic or average-case over circuits.
- Canonical unranking of distinct rows is E-uniform and does not use nonuniform advice.
- Source lengths are kappa-dense: every sufficiently large target length is padded from some m within factor kappa.
- If proofs have length 2^{mu m}, they are generated or streamed; they are not found by exhaustive proof search.

## Equations

- anti_ball_soundness: `\forall C\in \mathrm{SIZE}(2^{\epsilon m})\quad \Delta(T_{m,i},\mathrm{tt}(C))>2^{\rho m}`. Valid when: Valid when the verifier soundness ranges over unrestricted nonuniform circuits on m-bit inputs.
- multiplex_exponent: `\delta < \frac{\epsilon}{\kappa(1+D)}`. Valid when: Applies after rank multiplexing and kappa-padding preserve uniform source lengths.
- no_radius_charge_for_exact_mcsp: `C(T_{m,i})>2^{\epsilon m}`. Valid when: Valid when the anti-ball excludes centers at the same size threshold, not smaller centers.
- target_time: `\mathrm{Time}_{L}(n)\le 2^{O(n)}`. Valid when: Requires generated row access or sequential emission within exponential time in final input length.

## Attempted Derivation

- Encode AntiBall(T,s,r) by a formula Phi_{m,T,s,r} asserting that there exists a circuit C of size s and an edit set E of size at most r such that C agrees with T outside E.
- Observe that unsatisfiability of Phi_{m,T,2^{epsilon m},2^{rho m}} is exactly the anti-ball condition needed for exact MCSP hardness above 2^{epsilon m}.
- Replace the prior black-box certificate by a generated proof pi of unsatisfiability in a sound proof system P; verification may be exponential in m but remains compatible with E if the row/proof pair is generated rather than searched.
- Use the low-image rank i and data input x to define L(i,x)=T_{m,i}(x). If L has circuits of size 2^{delta(1+D)m}, fixing i gives a circuit for the hard row, contradicting anti-ball soundness when delta<epsilon/(1+D).
- Apply kappa-padding to obtain all target lengths with exponent delta<epsilon/(kappa(1+D)).
- Attempt to drop the generator and rely only on existence of a P-proof; exhaustive search over proof strings of length 2^{mu m} costs 2^{2^{mu m}}, which exceeds E and breaks target preservation.

Blocking gap: No construction is known for an advice-free, low-D, cap-compatible generator of rows and nonblackbox anti-ball proofs. Proof-system soundness and the row generator may hide exactly the lower bound being extracted.

## Falsifiers

- falsifier: anti-ball proofs exist only existentially at length 2^{mu m}; canonical proof search is super-E and the target language is not validly defined.
- falsifier: the verifier is black-box in T and reads q=o(2^{epsilon m}/m) locations, since a zero-fill completion has circuit O(qm).
- falsifier: the row generator gives random access circuits of size 2^{alpha m} with alpha<epsilon, contradicting the claimed MCSP no-side threshold.
- falsifier: the proof or table constants are supplied as nonuniform advice depending on m or on the selected row.
- falsifier: the verifier acceptance expands into a dense P/poly-constructive property rejecting small circuits, triggering the natural-proofs obstruction under pseudorandom functions.
- falsifier: the anti-ball formula forbids only centers below 2^{epsilon m-rho m} while the extraction claims threshold 2^{epsilon m}; this is an invalid radius accounting step.

## Learning

Cycle 57 separates proof length from proof location. A nonblackbox anti-ball proof can be long without harming the MCSP-to-E extraction if the row/proof pair is E-uniformly generated; an existential long proof is not valid because locating it is double-exponential. The route's next hard obligation is a generated, sparse, non-large anti-ball proof family, not another hardness-magnification slogan.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The route has moved from black-box certificates to nonblackbox binding; a concrete proof-complexity carrier test is needed to separate valid generated proofs from invalid existential proof folklore.
- Situation seed: For each m, build the approximate-MCSP unsatisfiability formula Phi_{m,T,2^{epsilon m},2^{rho m}} for a kappa-dense, low-image table family T_{m,i}. Imagine a sound proof system P and a sequential generator that emits (T_{m,i},pi_{m,i}) where pi_{m,i} is a P-proof of unsatisfiability.
- Varied variable: proof-length exponent mu in |pi_{m,i}|=2^{mu m}, comparing generated proofs against merely existential proofs.
- Held-fixed controls: epsilon=0.40 as the forbidden circuit-size exponent over m input bits., rho=0.05 with centers still at size 2^{epsilon m}, so exact MCSP extraction pays no radius loss., D=0.03 distinct-image entropy for the row family., kappa=1 for the first audit before padding losses., unrestricted nonuniform Boolean circuits are the lower-bound target model., the row generator is advice-free and has no random-access circuit exponent below epsilon.
- Expected observation: Generated proofs remain compatible with E extraction for any constant mu because L computes row bits from the generator, while existential proofs become unusable as soon as mu>0. If the verifier degenerates to q low-load table queries, the zero-fill falsifier appears regardless of mu.
- Transfer certificate needed: A formal certificate must include E-uniform row/proof generation, soundness of P for Phi, correctness of the Phi-to-anti-ball encoding, low-D canonical unranking, and a leakage audit proving no subthreshold row decoder or advice channel is present.

## Next Experiment

Instantiate Phi_{m,T,s,r} for one restricted proof system, such as resolution or algebraic IPS with explicit row constants, and test whether any generated low-D family can have short nonblackbox unsat proofs without giving a local decoder for T.
