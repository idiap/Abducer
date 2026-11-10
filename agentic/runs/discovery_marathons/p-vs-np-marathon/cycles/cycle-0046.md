# cycle-0046

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: normal-form extraction gate

## Candidate Lemma

One-sided formula-local separator covers are a valid sufficient falsifier for the generated-OR source lower bound, but they are not a necessary normal form for arbitrary circuits computing H_N unless a new locality-extraction theorem is proved.

## Definitions

- source object: H_N(x)=OR_{j in [M]} SAT(G_N(x,j)) on N input bits, with M=N^q, query length L=(log N)^d, and shared generator circuit size N^rho.
- target object: SAT notin P/poly, obtained only through the contrapositive substitution bridge from SAT circuits on length L to circuits for H_N.
- controlled interface: shared generated-OR substitution where all SAT calls have length L and the entire query list is produced with size N^rho without position-specific advice.
- target-preserving condition: q<1+epsilon, rho<1+epsilon, d>1, and every conversion of a source upper bound to a target consequence preserves nonuniform circuit size and the exact N^{1+epsilon} threshold.
- Sep_N^{1s}(K,s,E) means K position-indexed predicates of size at most s, sound on the generated universe, hitting all but E positive bags.
- A planted-control carrier has a simple bit b_N(x) such that b_N=1 forces at least one generated satisfiable formula and b_N=0 forces all generated formulas unsatisfiable.

## Assumptions

- Circuit size is nonuniform Boolean size on the N-bit carrier input.
- Local separator predicates see one generated formula and its position, not the whole carrier input x.
- Error sets of size E are patchable by equality gates at cost O(EN).
- The planted-control construction is a formal falsifier in oracle or pseudorandom-label models unless a SAT-specific anti-control certificate is added.

## Equations

- generated_or_carrier: `H_N(x)=vee_{j=1}^{N^q} SAT(G_N(x,j)),  |G_N(x,j)|=L=(log N)^d`. Valid when: Valid when the generated query family has a shared circuit G_N and all positions have the same polylogarithmic target length.
- target_substitution_bridge: `SAT in SIZE(n^c) => C(H_N) <= N^rho + N^q L^c + O(N^q) = N^{max(rho,q)+o(1)}`. Valid when: Applies when SAT on length L has nonuniform circuits of size L^c and G_N is reused without position-specific advice.
- separator_cover_upper_bound: `Sep_N^{1s}(K,s,E) => C(H_N) <= C(G_N)+O(K(s+L^{O(1)})+E N)`. Valid when: Requires K position-indexed one-sided local predicates that hit every positive bag except E explicitly patchable inputs.
- planted_control_collapse: `[(b_N(x)=1 => H_N(x)=1) and (b_N(x)=0 => H_N(x)=0)] => H_N=b_N and C(H_N)<=C(b_N)+O(1)`. Valid when: Valid when the control bit semantically determines the OR label of every generated bag, even if formula labels look locally random.
- subthreshold_separator_falsifier: `K(s+L^{O(1)})+E N = o(N^{1+epsilon}) => the claimed C(H_N)>N^{1+epsilon-o(1)} source lower bound is false`. Valid when: Applies only after the separator family is sound on the generated universe and the residual errors are patchable by equality gates.

## Attempted Derivation

- Assume a circuit C of size S<N^{1+epsilon} computes H_N exactly.
- Try to cover positive inputs x by choosing a witness position j with SAT(G_N(x,j)).
- Attempt to define a local predicate P_{j,C} on y=G_N(x,j) that is one-sided sound and accepts enough chosen witnesses.
- The only available predicate from C is global: it depends on x and on correlations among all generated positions, not on y alone.
- DNF expansion of C gives global accepting regions on x, but conversion to formula-local predicates can cost 2^S or require inverting G_N.
- A planted-control carrier makes the obstruction exact: H_N=b_N is easy, while local formula labels may remain separator-hard.

Blocking gap: No valid locality-extraction theorem maps arbitrary small circuits for H_N into one-sided formula-local separator covers with subthreshold overhead.

## Falsifiers

- planted-control falsifier: a simple global bit determines the OR label while individual generated formulas remain locally hard to separate.
- global-correlation circuit falsifier: C computes a relation among generated positions without identifying any satisfiable formula witness.
- relativization falsifier: random oracle labels can make separator complexity high while H_N remains equal to an easy control bit.
- threshold falsifier: any Sep_N^{1s}(K,s,E) with K(s+L^{O(1)})+EN=o(N^{1+epsilon}) invalidates the source lower bound.
- natural-proof leakage falsifier: a constructive dense separator-hardness certificate for SAT truth tables may fall inside the Razborov-Rudich obstruction.

## Learning

Cycle 46 converts the cycle-45 normal-form warning into a precise obstruction. Greedy cap and separator denominators give valid upper-bound falsifiers, but separator hardness is not by itself a source lower bound. A planted-control generated-OR carrier can have H_N easy while local formula separators remain hard, so the route now needs a nonrelativizing locality-extraction theorem or a direct arbitrary-circuit lower bound for H_N.

## Gedanken Experiment Design Seed

- Need decision: `use now as a falsifier probe`
- Rationale: Cycle 45 left a normal-form gap. A concrete planted-control generated-OR carrier tests whether separator hardness is complete for arbitrary circuit hardness, rather than merely another sufficient upper-bound audit.
- Situation seed: High-q polylog generated-OR with input x in {0,1}^N, b=x_1, M=N^q, L=(log N)^d. If b=1, G_N outputs pseudorandom satisfiable CNFs with hidden assignments; if b=0, it outputs pseudorandom unsatisfiable Tseitin-like CNFs on the same length scale and without an explicit marker. Then H_N(x)=b.
- Varied variable: tau, the local distinguishability exponent controlling the largest residual positive cap of size-N^sigma one-sided predicates after excluding generated negatives.
- Held-fixed controls: q in ((1+epsilon)/2,1+epsilon) so dense tuple leakage stays threshold-blocked., rho<1+epsilon so the target substitution bridge remains valid., d>1 so exhaustive truth-table lookup for length L is superpolynomial in N., No position-specific advice and no syntactic marker revealing the control bit inside individual formulas.
- Expected observation: For small tau, marker-like predicates give a subthreshold separator falsifier. For large tau, separator covers become superthreshold while C(H_N)=O(N), proving that separator lower bounds alone do not imply the source circuit lower bound.
- Transfer certificate needed: A nonrelativizing SAT-specific locality-extraction theorem, or an explicit no-planted-control condition on G_N, is required before separator-hardness intuition may enter the proof queue.

## Next Experiment

Formalize a restricted no-control generator class, such as block-product independent seeds with no shared label bit, and test whether an S-size circuit for OR_j SAT(G(x,j)) can be localized to a one-sided separator cover; compute the exact overhead in q,rho,sigma,E.

# Barrier-Aware Lower-Bound Route: arithmetic PIT target gate

## Candidate Lemma

An arithmetic hitting-set/annihilator argument gives a valid arithmetic circuit lower bound, but it transfers to SAT_m notin SIZE(m^k) only through an explicit Boolean-to-arithmetic simulator whose size and degree stay below the hitting-set thresholds. Without that simulator the route is a target mismatch, not P != NP progress.

## Definitions

- source object: an F-arithmetic hitting set H_v for v-variate circuits of size s(v) and syntactic degree d(v), together with a nonzero low-degree annihilator P_H satisfying P_H|_{H_v}=0.
- target object: the Boolean truth-table family SAT_m and the nonuniform lower bound SAT_m notin SIZE(m^k), not merely an arithmetic VP/VNP or NEXP consequence.
- controlled interface: a uniform map Phi_m sending any Boolean circuit for SAT_m of size m^k to an F-arithmetic circuit computing the named source polynomial or its evaluation table, with bounded size B(m,k) and degree D(m,k).
- target-preserving condition: B(m,k)<=s(v) and D(m,k)<=d(v), with no hidden advice, large-constant encoding, oracle leakage, or padding change between the SAT slice and the source polynomial.

## Assumptions

- The field F, variable count v, size threshold s, and syntactic-degree threshold d are fixed before seeing a putative SAT circuit.
- H_v is explicit enough for the intended construction, but explicitness alone does not identify P_H with SAT_m.
- The hitting-set statement is for arithmetic circuits, while the target lower bound is for Boolean circuits on m input bits.
- The interface Phi_m must be uniform and target-preserving; otherwise a valid arithmetic lower bound remains irrelevant to P vs NP.

## Equations

- hitting_set_property: `\forall Q\in \mathcal{C}_{F}(v,s,d)\setminus\{0\}\;\exists a\in H_v:\;Q(a)\neq 0`. Valid when: Valid when the source lower-bound model names the field, variables, circuit size, and syntactic-degree bound.
- annihilator_lower_bound: `P_H\neq 0\;\wedge\;\deg(P_H)\le d\;\wedge\;P_H|_{H_v}=0\;\Longrightarrow\;P_H\notin \mathcal{C}_{F}(v,s,d)`. Valid when: Applies after H_v is certified to hit every nonzero circuit in the same arithmetic class.
- dimension_annihilator_threshold: `r^v>|H_v|\;\Longrightarrow\;\exists P_H\neq 0:\;P_H|_{H_v}=0,\;\deg(P_H)\le v(r-1)`. Valid when: Valid when the monomial space with individual degrees below r exceeds the number of evaluation constraints.
- boolean_transfer_threshold: `\mathrm{SIZE}_{bool}(SAT_m)\le m^k\;\xrightarrow{\Phi_m}\;\mathrm{SIZE}_{alg}(P_H)\le B(m,k),\;\deg\le D(m,k)`. Valid when: Requires the target-preserving simulator to relate the SAT slice to the same annihilator polynomial.

## Attempted Derivation

- Fix an explicit H_v hitting all nonzero F-arithmetic circuits of size s(v) and syntactic degree d(v).
- Use linear algebra: if r^v>|H_v|, choose a nonzero annihilator P_H of individual degree <r that vanishes on H_v.
- If v(r-1)<=d(v), the hitting-set property implies P_H has arithmetic circuit size greater than s(v). This is a valid arithmetic lower bound.
- Try to infer SAT_m notin SIZE(m^k) by assuming a Boolean circuit C for SAT_m and translating C into an arithmetic circuit for P_H.
- The translation fails unless a uniform Phi_m proves that C computes enough of P_H, not just SAT_m, and preserves B(m,k)<=s(v), D(m,k)<=d(v).

Blocking gap: There is no canonical target-preserving identity between the annihilator polynomial extracted from H_v and the SAT_m truth table. The arithmetic source lower bound can be completely disjoint from the Boolean target language.

## Falsifiers

- BGS collapse oracle A: P^A=NP^A while the unrelativized arithmetic hitting-set statement can remain valid, falsifying relativizing PIT-to-PNP transfers.
- Product-of-hyperplanes sanity check: any H_v with |H_v|<=d is killed by a degree-|H_v| circuit of size O(v|H_v|), falsifying overstrong hitting-set parameters.
- Target-object mismatch: a Boolean circuit for SAT_m need not yield an arithmetic circuit for the annihilator P_H, so the lower bound may concern the wrong function.
- Advice leakage: large constants or nonuniform maps Phi_m can encode H_v or the SAT truth table and destroy any valid lower-bound transfer.
- Padding collapse: for L_{n,beta}(u,w)=SAT_n(u), the padded length m=n^beta can make claimed thresholds refer to m while the algebraic object only sees the n-bit core.

## Learning

Cycle 46 isolates a valid PIT-annihilator bridge to arithmetic lower bounds and a precise quarantine for P-vs-NP extrapolation: the missing object is not a stronger hitting set but a uniform SAT-to-annihilator simulator preserving size, degree, and padding thresholds.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: This branch needs a concrete transfer test because PIT slogans already give arithmetic lower bounds; the open issue is whether a SAT-specific Boolean target is preserved quantitatively.
- Situation seed: Consider the padded language L_{n,beta}(u,w)=SAT_n(u) on m=n^beta bits and a proposed PIT-annihilator route with v=Theta(n), H_v hitting size s(v)=v^a degree d(v)=v^c arithmetic circuits over a fixed field.
- Varied variable: padding exponent beta
- Held-fixed controls: The target claim remains a Boolean nonuniform lower bound against SIZE(m^k) on the padded input length., The field F, degree exponent c, and hitting-set size threshold a are fixed before beta varies., Phi_m must be uniform, advice-free, and forbidden to encode H_v or the SAT truth table in constants., The annihilator P_H must be the same polynomial certified by H_v, not a beta-dependent restatement of SAT.
- Expected observation: As beta grows, any simulator from a size m^k SAT circuit has overhead at least n^{beta k} in the natural accounting; unless a>beta k and P_H is uniformly tied to SAT_n, the threshold collapses or the object mismatch is exposed.
- Transfer certificate needed: A formal projection or evaluation identity showing that every SIZE(m^k) circuit for L_{n,beta} induces an arithmetic circuit for P_H of size <=v^a and degree <=v^c, uniformly and without advice leakage.

## Next Experiment

Audit matrix-rigidity lower-bound routes with the same target gate: source linear-circuit model, target Boolean SIZE(m^k), and the exact compiler threshold needed before rigidity can affect SAT.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Sparse-correction no-side falsifier: let s(m)=2^{epsilon m}. If an accepted MCSP carrier row T differs from some circuit g of size a on t inputs and a+cmt<s(m), then T has unrestricted circuit size below s(m). Hence any valid no-side carrier at threshold 2^{epsilon m} must be far from every small base circuit by more than the exact sparse-patch radius, not merely balanced away from 0 and 1.

## Definitions

- source object: a length-m MCSP carrier cell A_{m,z} of truth tables T:{0,1}^m->{0,1}, produced by a uniform short-certificate verifier and intended to contain only no-instances at threshold s(m)=2^{epsilon m}.
- target object: an unrestricted Boolean circuit lower bound C(T)>2^{epsilon m} for a row used by the carrier-to-E extraction, later yielding E lower bounds after kappa,D losses.
- controlled interface: compare each accepted table with every small base circuit g and account for exact sparse corrections by equality tests on exceptional inputs.
- target-preserving condition: the verifier must guarantee distance from every a-size base circuit exceeds (2^{epsilon m}-a)/(c m); otherwise the accepted row has a small unrestricted circuit and the MCSP no-side claim is invalid.

## Assumptions

- Standard fan-in two Boolean circuit model with constants; an equality test to a hardwired m-bit string has size O(m).
- The carrier soundness target is exact unrestricted circuit complexity, not correlation hardness or average-case distance.
- The accepted row is used as a truth table at input length m, with no advice-dependent choice of the exceptional set.

## Equations

- patch_upper_bound: `C(T) \le C(g)+c m\cdot \Delta(T,g)`. Valid when: Valid when T is obtained from g by flipping exactly the listed exceptional inputs using hardwired equality tests over m input bits.
- necessary_distance: `\forall g\in SIZE(a):\quad \Delta(T,g)>\frac{2^{\epsilon m}-a}{c m}`. Valid when: Valid when the target claim is exact MCSP no-side soundness at threshold 2^{epsilon m} against unrestricted circuits.
- half_threshold_radius: `a\le 2^{\epsilon m-1}\Rightarrow \Delta(T,g)>\Omega(2^{\epsilon m}/m)`. Valid when: Applies after the small base circuit size is bounded below half of the intended MCSP threshold.
- existing_transfer_after_sound_row: `\delta < \frac{\epsilon}{\kappa(1+D)}`. Valid when: Requires an actual hard row satisfying the no-side threshold, kappa-dense source lengths, and E-canonical distinct-image unranking.

## Attempted Derivation

- Start with the valid extraction invariant from earlier cycles: a kappa-dense, bounded-D, E-canonical source containing an actual row of circuit complexity above 2^{epsilon m} yields E lower-bound exponent delta<epsilon/(kappa(1+D)).
- Repair the source-side no-gos by replacing zero/one load constraints with the stronger condition that every accepted row is farther than (2^{epsilon m}-a)/(c m) from every circuit of size a.
- Use the sparse-correction lemma to prove this condition is necessary for exact MCSP no-side soundness and catches balanced perturbations of parity or majority that previous load tests missed.
- Try to define the carrier as a sparse certificate family proving FAR_{a,r}(T) for a=2^{epsilon m-1} and r=Theta(2^{epsilon m}/m).
- The naive verifier must compare T with all a-size circuits, costing 2^{Theta(a log a)} rather than 2^{O(m)}; random sampling gives only average-case evidence and can accept an exact sparse patch of a small circuit.

Blocking gap: No known non-natural, advice-free, bounded-D certificate proves anti-sparse-correction distance from every unrestricted a-size circuit within the E verifier budget.

## Falsifiers

- falsifier: an accepted row differs from parity, majority, an affine function, or any a-size circuit on fewer than (2^{epsilon m}-a)/(c m) inputs.
- falsifier: a balanced-heavy invariant allows sparse corrections of an easy base; balance does not imply exact circuit lower bounds.
- falsifier: the source image is covered by Hamming balls of radius r around small circuits with a+c m r below the MCSP threshold.
- falsifier: the anti-ball condition is certified by brute-force circuit enumeration, exceeding the E-uniform verifier budget.
- falsifier: a randomized distance test is used as exact no-side soundness without a deterministic transfer certificate.

## Learning

Cycle 46 adds a circuit-sensitive sparse-correction falsifier: MCSP soundness at threshold 2^{epsilon m} requires accepted rows to be Omega(2^{epsilon m}/m) far from every subthreshold circuit, not just from zero, one, or rankable profiles. This is valid route-level progress because it rejects balanced perturbation carriers while leaving the existing carrier-to-E extraction intact.

## Gedanken Experiment Design Seed

- Need decision: `use now as a falsifier probe`
- Rationale: The branch needs a concrete test separating genuine circuit-sensitive invariants from predicates that only repair zero-fill or balance failures abstractly.
- Situation seed: Parity-plus-sparse-exception MCSP carrier: at length m the verifier emits truth tables T=PARITY_m xor 1_E, where E is a certificate-described exception set with |E|=2^{beta m}; the image is kept low-D by canonical ranking of exception sets.
- Varied variable: beta, the exception-set exponent in |E|=2^{beta m}.
- Held-fixed controls: MCSP no-side threshold s(m)=2^{epsilon m} for a fixed constant epsilon., No advice and E-uniform canonical unranking of accepted images., The base circuit PARITY_m has polynomial size and remains fixed across the experiment., The carrier-to-E extraction losses kappa and D are held fixed so only source soundness changes.
- Expected observation: For beta<epsilon-o(1), every emitted table has circuit size poly(m)+O(m2^{beta m})<2^{epsilon m}, so the family is an invalid source despite being balanced and high-load. For beta>epsilon, the sparse-correction falsifier no longer applies, but certificate length, image entropy D, and verifier cap constraints likely collapse the transfer.
- Transfer certificate needed: A formal proof that the exception-set representation is E-canonical and bounded-D, plus an unrestricted lower bound not merely showing distance from parity but distance from every circuit of size below 2^{epsilon m}.

## Next Experiment

Audit algebraic-immunity and spectral-invariant carrier candidates for sparse-correction covers around low-degree, parity, majority, and small decision-tree bases; compute the beta threshold where their exception representation exceeds the verifier cap.
