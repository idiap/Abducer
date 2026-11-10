# cycle-0029

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: one-sided separating-ensemble leakage gate

## Candidate Lemma

One-sided separating-ensemble falsifier for generated-OR magnification. Let H_N(x)=OR_{j<N^q} SAT(G_N(x,j)) with |x|=N, |G_N(x,j)|=L=(log N)^d, and C(G_N)<=N^rho. If positives and negatives of H_N, outside |E_N|<=N^delta exceptions, are separated by R=N^r selector circuits each outputting s=N^ell indices and by selected-image label circuits of size N^b, then C(H_N)<=N^{r+ell+max{a,rho,b}+o(1)}+N^{1+delta+o(1)}. Hence a valid N^{1+epsilon} source lower bound must rule out every such separator with r+ell+max{a,rho,b}<1+epsilon and delta<epsilon.

## Definitions

- source object: generated-OR carrier H_N on N input bits, H_N(x)=OR_{j<N^q} SAT(G_N(x,j)) with output length L=(log N)^d.
- target object: SAT on L-bit formulas and the target consequence SAT notin P/poly, with NP not subset P/poly only after the length-cover transfer is certified.
- controlled interface: replace each generated SAT query by a hypothetical SAT circuit of size L^c, while charging generator size N^rho and fanout M=N^q.
- target-preserving condition: d>1, q<1+epsilon, rho<1+epsilon, no nonuniform advice enters G_N beyond its charged circuit, and N ranges cover all SAT input lengths.
- A_t is a selector circuit of size at most N^a; on input x and list position u<s it outputs an index j<N^q.
- B_t is a selected-image label circuit on L-bit formulas; it need not decide SAT outside formulas actually selected by A_t and G_N.
- Separation means that for every x outside E_N, H_N(x)=1 iff some pair (t,u) has B_t(G_N(x,A_t(x,u)))=1.

## Assumptions

- Constants q,rho,r,ell,a,b,delta,epsilon are fixed independently of N, and d>1 is fixed.
- The generator family G_N has nonuniform circuit size at most N^rho and outputs well-formed SAT instances of length L=(log N)^d.
- There are R<=N^r selectors, each with list length s<=N^ell and circuit size at most N^a.
- The label circuits B_t have size at most N^b and are charged as arbitrary nonuniform leakage, not as valid SAT solvers.
- The exception set E_N is hardwired by equality tests, costing N^{1+delta+o(1)} gates.

## Equations

- carrier-definition: `H_N(x)=\bigvee_{j<N^q} SAT(G_N(x,j)),\qquad L=(\log N)^d.`. Valid when: Valid when the generated carrier and SAT-query length map are fixed before proving any lower bound.
- separator-circuit: `D_N(x)=\bigvee_{t<R}\bigvee_{u<s} B_t(G_N(x,A_t(x,u))).`. Valid when: Valid when the selector ensemble separates H_N correctly outside the explicitly hardwired exception set.
- separator-upper-bound: `C(H_N)\le N^{r+\ell+\max\{a,\rho,b\}+o(1)}+N^{1+\delta+o(1)}.`. Valid when: Applies after all selector, generator, labeler, OR fanin, and exception-correction costs are charged nonuniformly.
- source-audit-threshold: `\Psi_N^{sep}>N^{1+\epsilon-o(1)}.`. Valid when: Required when the advertised source lower bound is meant to survive all one-sided separating-ensemble leakage.

## Attempted Derivation

- Fix an ensemble of R selectors A_t, each producing s indices into the N^q generated SAT queries.
- For each pair (t,u), build a circuit that computes j=A_t(x,u), then y=G_N(x,j), then the selected-image label B_t(y).
- OR all R*s outputs. By the separation promise, this computes H_N on all x outside E_N.
- Hardwire the exceptional inputs by equality gates and override the answer on E_N, with cost N|E_N| up to subpolynomial factors.
- The resulting circuit has size at most R*s*(N^a+N^rho+N^b) plus exception cost, giving N^{r+ell+max{a,rho,b}+o(1)}+N^{1+delta+o(1)}.
- Therefore any claimed N^{1+epsilon} lower bound for H_N is valid only if every such separating ensemble exceeds the same exponent threshold.

Blocking gap: No available lower-bound method rules out arbitrary selected-image separators B_t. These labelers need not be SAT algorithms, so the target SAT hardness hypothesis does not exclude them.

## Falsifiers

- A one-sided separating ensemble with r+ell+max{a,rho,b}<1+epsilon and exception exponent delta<epsilon falsifies the source lower-bound claim.
- A small selected-image labeler B_t that is not a valid SAT solver still leaks enough nonuniform information to collapse H_N.
- If q>=1+epsilon or rho>=1+epsilon, the target bridge has threshold collapse even before source leakage is considered.
- If the length map L=(log N)^d does not cover SAT lengths with controlled rounding, the target-preserving consequence is invalid.

## Learning

Cycle 29 sharpens the generated-OR source audit from ensemble list selectors to one-sided selected-image separators. The valid target bridge still needs only q,rho<1+epsilon, but the source lower bound must now beat Psi_N^{sep}; small local labelers are a concrete falsifier even when they do not solve SAT globally.

## Gedanken Experiment Design Seed

- Need decision: `design now`
- Rationale: The current branch has accumulated selector-cover leakage gates; a concrete separator experiment tests whether the newest gate is stronger than the previous ensemble-list audit or only a renaming.
- Situation seed: Generated-OR carrier where G_N maps (x,j) to high-entropy 3CNF formulas of length L=(log N)^d, with M=N^q queries and q,rho<1+epsilon; selectors try to hit one satisfiable generated formula on positive x, and labelers separate only the selected image.
- Varied variable: ensemble exponent r, with list exponent ell and labeler exponent b recorded so the threshold r+ell+max{a,rho,b}=1+epsilon can be crossed deliberately.
- Held-fixed controls: d>1 so SAT polynomial-size circuits substitute as N^{o(1)} overhead., q<1+epsilon and rho<1+epsilon so the target bridge remains valid., Exception exponent delta is kept below epsilon only when measuring a true falsifier., Label circuits are charged as arbitrary nonuniform selected-image separators, not assumed to be SAT solvers.
- Expected observation: If increasing r lets many weak selectors cover positives while selected negative images remain separable by tiny B_t, the source lower bound fails below the magnification threshold. If no such separator exists, the source obligation becomes the concrete lower bound Psi_N^{sep}>N^{1+epsilon-o(1)}.
- Transfer certificate needed: A formal lower bound against all selected-image separating ensembles, plus a length-cover certificate for L=(log N)^d, is required before this intuition may affect the proof queue.

## Next Experiment

Try to lower-bound or construct Psi_N^{sep} for a random-like generator: estimate whether selected positive and negative images admit N^b-size separators when R=N^r and s=N^ell are below the magnification threshold.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Approximate-degree naturalization gate. Let N=2^m and y_N=tt(SAT_m). If a total poly(N)-constructive Boolean property F_N:{0,1}^N->{0,1} satisfies F_N(y_N)=1, rejects every truth table of every m-input circuit of size at most m^k, and has \widetilde{deg}_{1/3}(F_N)<=t, then R_N=F_N^{-1}(1) is a constructive property useful against SIZE(m^k) with density at least 2^{-O(t^4)}. Thus t=O((log N)^{1/4}) makes the route a valid natural-proof object, subject to the PRF falsifier.

## Definitions

- source object: a total Boolean separator family F_N on truth tables of length N=2^m, decidable in poly(N) time and approximable pointwise within error 1/3 by degree t real polynomials.
- target object: a Razborov-Rudich natural property R_N subset {0,1}^N that contains tt(SAT_m), excludes tt(C) for every m-input circuit C of size m^k, and has density N^{-O(1)}.
- controlled interface: approximate-degree lower-bound method -> total natural property via Nisan-Szegedy approximate-degree/block-sensitivity lower bound and certificate-complexity upper bound.
- target-preserving condition: totality, no advice leakage, poly(N) constructivity, universal rejection of SIZE(m^k) truth tables, and t^4=O(log N) are all preserved in truth-table coordinates.

## Assumptions

- F_N is total on all N-bit strings, not merely defined on SAT and small-circuit truth tables.
- The approximating polynomial has worst-case error at most 1/3 on all of {0,1}^N.
- Constructivity means a uniform algorithm decides F_N(x) in N^{O(1)} time from x alone.
- Usefulness is against the named nonuniform target SIZE(m^k), not an average or heuristic target.
- Known total-function inequalities \widetilde{deg}(F)=Omega(sqrt(bs(F))) and C(F)<=bs(F)^2 are allowed.

## Equations

- truth_table_indexing: `N=2^m,\qquad y_N=\mathrm{tt}(SAT_m)`. Valid when: Valid when the source lower-bound model is indexed by m input bits and truth-table length N.
- approximate_degree_source: `\widetilde{\deg}_{1/3}(F_N)\le t`. Valid when: Valid when F_N is total and the approximating polynomial is accurate on every N-bit input.
- block_sensitivity_transfer: `bs(F_N)\le c_1 t^2`. Valid when: Applies to total Boolean F_N; it is invalid for promise separators or partial extensions.
- certificate_transfer: `C_1(F_N,y_N)\le C(F_N)\le c_2 bs(F_N)^2\le c_3 t^4`. Valid when: Requires totality of F_N and uses the standard certificate-versus-block-sensitivity inequality.
- density_from_certificate: `\mu(R_N)\ge 2^{-C_1(F_N,y_N)}\ge 2^{-c_3 t^4}`. Valid when: Valid when a one-certificate at the SAT truth table defines an accepting subcube contained in R_N.
- natural_density_threshold: `t^4\le a\log_2 N\ \Longrightarrow\ \mu(R_N)\ge N^{-a c_3}`. Valid when: Applies after the approximate-degree threshold is measured in truth-table length N and logarithms are base two.

## Attempted Derivation

- Fix m, N=2^m, y_N=tt(SAT_m), and a total explicit separator F_N for SIZE(m^k).
- Assume \widetilde{deg}_{1/3}(F_N)<=t. For any input with b disjoint sensitive blocks, restrict F_N to those blocks; the induced total b-bit function has approximate degree Omega(sqrt(b)).
- Therefore bs(F_N)<=O(t^2) by the Nisan-Szegedy approximate-degree lower bound for total Boolean functions.
- Use C(F_N)<=bs(F_N)^2, so the SAT input y_N has a one-certificate of size O(t^4).
- The subcube fixed by that certificate lies inside F_N^{-1}(1), giving density at least 2^{-O(t^4)}.
- If t^4=O(log N), F_N^{-1}(1) is poly(N)-constructive, polynomially large, and useful against the same SIZE(m^k) target.

Blocking gap: No gap for total explicit separators; the blocking gap is applying the lemma to partial, advised, oracle, or algebraic-extension carriers that never produce such an F_N.

## Falsifiers

- A promise-only approximant on D_N={tt(SAT_m)} union TT(SIZE(m^k)) has exponentially sparse domain and is a falsifier to any automatic largeness inference.
- A separator with t=(log N)^{1/3} gives only exp(-O((log N)^{4/3})) density by this bridge, so the polynomial-density natural-proof audit is not valid there.
- If F_N is evaluated using the SAT truth table or superpolynomial advice, constructivity fails and the natural-property transfer is invalid.
- If F_N rejects only most small circuits rather than every SIZE(m^k) truth table, usefulness for the named target is lost.
- If the low-degree object lives only over an oracle or algebraic extension and does not define a total Boolean F_N on {0,1}^N, the Nisan-Szegedy step is invalid.

## Learning

Cycle 29 adds a concrete barrier gate: total explicit SAT truth-table separators of approximate degree t naturalize with density 2^{-O(t^4)} via block sensitivity and certificates. The valid natural-proof threshold is t=O((log N)^{1/4}); partial promise low-degree and higher-degree analytic routes remain possible escapes only with separate totalization or density certificates. This is route-level progress, not progress on P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: Approximate degree is a common analytic carrier for lower-bound routes, and this branch needs a quantitative barrier gate rather than another natural-proof slogan.
- Situation seed: For each m, imagine a total N^c-time property F_N on N=2^m bit truth tables with F_N(tt(SAT_m))=1 and F_N(tt(C))=0 for every m-input circuit C of size m^k; also suppose F_N has a 1/3 approximating polynomial of degree t=(log N)^gamma.
- Varied variable: gamma in the exponent t=(log N)^gamma.
- Held-fixed controls: N=2^m and the target class is nonuniform SIZE(m^k)., F_N is total and decidable in N^c time without advice., Usefulness is universal over every target circuit truth table., Approximation error is worst-case 1/3 on all of {0,1}^N.
- Expected observation: For gamma<=1/4 the separator naturalizes with polynomial density; for gamma>1/4 this certificate-density transfer collapses, so a natural-proof falsifier needs an additional density argument.
- Transfer certificate needed: A proof that the analytic method outputs a total explicit F_N with approximate degree preserved in truth-table coordinates and with no promise, advice, oracle, or algebraic-extension leakage.

## Next Experiment

Audit low Fourier-tail or approximate-sparsity separators: determine whether L2 concentration on poly(N) characters forces polynomial density, and identify where coefficient advice or high tail mass blocks the transfer.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Image-entropy bridge: a uniform cap-compatible MCSP source with distinct emitted-image entropy D, kappa-dense source lengths, and an existential 2^{epsilon m}-hard accepted image yields an E language with circuit lower bound 2^{delta n} for every delta<epsilon/(kappa(1+D)).

## Definitions

- source object: uniform MCSP certificate emitter V_m with O(m)-bit certificates, E-time stream emission of m-input truth tables, image entropy D, source threshold 2^{epsilon m}, and verifier cap alpha_V.
- target object: an E-uniform multiplexed and padded language L_D with Boolean circuit lower bound 2^{delta n} at all sufficiently large target lengths.
- controlled interface: canonical distinct-image enumeration maps an image index z and input x to the z-th emitted truth-table value; kappa-padding transfers source lengths to target lengths.
- target-preserving condition: enumeration, length schedule, and padding are uniform; epsilon<=alpha_V; certificate length is O(m); and no advice chooses the hard image.

## Assumptions

- For each source length m in a uniform kappa-dense set S, some accepted emitted table has circuit complexity greater than 2^{epsilon m}.
- The number B_m of distinct emitted accepted tables is at most 2^{D m+o(m)} with constant D.
- Duplicate emitted tables are quotientable by full truth-table equality in 2^{O(m)} time; no nonuniform representative selector is used.
- Circuit lower bounds are against nonuniform fan-in two Boolean circuits; the constructed target language must lie in E.

## Equations

- image_entropy: `B_m=|Im(V_m)| <= 2^{D m+o(m)}`. Valid when: Valid when V_m is uniform, certificates have O(m) bits, and duplicate equality is checked by full truth-table comparison.
- multiplex_length: `n_m=m+ceil(log_2 B_m) <= (1+D)m+o(m)`. Valid when: Applies after canonical distinct-image indexing replaces raw accepted certificate indexing in the multiplexed truth table.
- target_exponent: `C_L(n) > 2^{delta n} for every delta < epsilon/(kappa(1+D))`. Valid when: Requires the source lengths to be uniformly kappa-dense and padding to preserve circuit lower bounds without advice.

## Attempted Derivation

- Enumerate all O(m)-bit accepted certificates, emit their tables, and merge duplicates by exhaustive equality; this stays within 2^{O(m)} time for constant D and linear certificates.
- Define M_m(z,x) as the value of the z-th distinct emitted table on x, using zero for out-of-range z; then M_m has input length at most (1+D)m+o(m).
- If M_m had circuits below 2^{epsilon m-o(m)}, hardwiring the index of a hard emitted image would give a small circuit for that MCSP no-side table, contradiction.
- Use the uniform kappa-dense source schedule and padding by ignored bits to define one E language on all large lengths, losing only the factor kappa in the exponent.

Blocking gap: The bridge is valid, but the route still lacks a constructed low-D, cap-compatible, non-natural MCSP source with sound existential hard images.

## Falsifiers

- falsifier: distinct-image entropy D_m is omega(1) or nonconstant enough that n_m is superlinear, causing the target exponent to collapse to zero.
- falsifier: canonical duplicate quotienting or the kappa-dense length schedule uses advice; then the target language is not validly in E.
- falsifier: verifier cap alpha_V is below epsilon, since checkpoint or block-simulation circuits then realize all emitted tables under the claimed MCSP threshold.
- falsifier: a salt repair makes the image property constructive and large, reintroducing the natural-proofs obstruction under standard PRF assumptions.

## Learning

Cycle 29 finds a sharper transfer parameter: accepted certificates may be numerous if their emitted tables collapse to low distinct-image entropy D by an E-canonical quotient. The valid exponent is delta<epsilon/(kappa(1+D)); the unresolved work is constructing such a source.

## Gedanken Experiment Design Seed

- Need decision: `design-now as a falsifier probe and parameter calibration`
- Rationale: The branch now depends on whether duplicate-heavy certificates can reduce the exponent loss without breaking uniformity; this is a concrete target-preserving transfer issue, not another MCSP slogan.
- Situation seed: A certificate emitter accepts 2^{H m} certificates, but q m bits are duplicate salt, so only 2^{D m} distinct m-input truth tables are emitted; one distinct table is promised MCSP-hard above 2^{epsilon m}.
- Varied variable: duplicate salt rate q=H-D, while D, epsilon, kappa, and alpha_V are monitored.
- Held-fixed controls: certificates remain O(m) bits and the verifier is uniform 2^{O(m)} time, source lengths remain uniformly kappa-dense, epsilon<=alpha_V is enforced, no advice selects representatives or hard images
- Expected observation: With E-canonical duplicate collapse, the lower-bound exponent follows D, not H; without the quotient certificate, the valid transfer reverts to H or fails uniformity.
- Transfer certificate needed: An E-time canonical distinct-image unranking algorithm plus a proof that at least one quotient image at each source length is 2^{epsilon m}-hard.

## Next Experiment

Try to build a cap-compatible low-D emitter from proof-complexity certificates where many syntactic proofs collapse to few truth tables, then audit whether quotienting remains E-uniform and non-large.
