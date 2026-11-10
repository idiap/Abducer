# cycle-0053

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: XOR carrier affine-incidence audit

## Candidate Lemma

For the polylog-query XOR carrier, any subthreshold computable F_2 affine representation of the generated parity-incidence vectors is an upper-bound falsifier for the claimed N^{1+epsilon} source lower bound. Thus the valid source obligation is an arbitrary-circuit lower bound that in particular defeats affine-incidence sketches and sparse corrections.

## Definitions

- source object: H_N^oplus(x)=xor_{j<=M} SAT(G_N(x,j)) on x in {0,1}^N, with M=N^q and query length L=(log N)^d.
- target object: SAT on length-L formulas, with target consequence SAT notin P/poly if the source lower bound survives the polylog substitution bridge.
- controlled interface: nonadaptive generated XOR of M=N^q SAT queries through a shared query-transcript generator G_N of size at most N^rho.
- target-preserving condition: d>1 and max{q,rho}<1+epsilon, so every fixed polynomial SAT circuit exponent contributes only N^{q+o(1)} gates.
- parity incidence vector: p_x(y)=#{j:G_N(x,j)=y} mod 2 over the generated universe U_N.
- affine-incidence sketch: basis vectors b_1,...,b_K in F_2^{U_N} and coefficient functions a_i(x) with total circuit size A_N such that p_x=sum_i a_i(x)b_i outside E_N bad inputs.

## Assumptions

- Circuit model is nonuniform fan-in two Boolean SIZE, with XOR implemented at linear overhead.
- The constants gamma_i=<b_i,SAT|_{U_N}> over F_2 may be hardwired as nonuniform advice.
- Bad inputs are corrected by equality tests of cost O(E_N N).
- The source lower bound being audited is C(H_N^oplus)>N^{1+epsilon-o(1)} for infinitely many N.

## Equations

- xor_carrier: `H_N^{\oplus}(x)=\bigoplus_{j=1}^{M} SAT(G_N(x,j)),\quad M=N^q,\quad L=(\log N)^d.`. Valid when: Valid when G_N outputs length-L SAT instances and the XOR is taken over F_2 with nonadaptive slots.
- incidence_inner_product: `H_N^{\oplus}(x)=\langle p_x,s\rangle_{\mathbb F_2},\quad p_x(y)=|\{j:G_N(x,j)=y\}|\bmod 2.`. Valid when: Valid when U_N is the generated formula universe and s(y) records the real SAT label.
- sketch_representation: `p_x=\sum_{i=1}^{K} a_i(x)b_i \text{ for all } x\notin B_N,\quad |B_N|=E_N.`. Valid when: Valid when coefficient circuits compute a_i and exceptions are measured over N-bit inputs.
- hardwired_basis_parities: `\gamma_i=\langle b_i,s\rangle_{\mathbb F_2},\quad H_N^{\oplus}(x)=\bigoplus_{i:\gamma_i=1} a_i(x) \text{ for } x\notin B_N.`. Valid when: Valid when nonuniform circuits may hardwire the K basis parities as advice constants.
- upper_bound_falsifier: `C(H_N^{\oplus})\le O(A_N+K+E_NN).`. Valid when: Valid when bad inputs are patched by equality tests and fan-in two XOR gates are allowed.
- source_gate: `\forall \text{ affine-incidence sketches }\quad A_N+K+E_NN>N^{1+\epsilon-o(1)}.`. Valid when: Valid when the claimed source lower bound is C(H_N^oplus)>N^{1+epsilon-o(1)} in general nonuniform circuits.

## Attempted Derivation

- Rewrite the XOR carrier as H_N^oplus(x)=<p_x,SAT|_{U_N}> over F_2.
- Observe that a low-cost affine-incidence sketch gives a small circuit by hardwiring basis parities gamma_i.
- Try to prove the contrapositive: if all such sketches have A_N+K+E_NN>N^{1+epsilon}, then C(H_N^oplus)>N^{1+epsilon}.
- Audit the extraction direction from an arbitrary small H circuit to an affine sketch of p_x.

Blocking gap: A small circuit for H_N^oplus computes only the scalar inner product <p_x,s>; it need not reveal p_x, a low-rank coordinate map, or any local SAT separator. The extraction is false in planted-label oracle worlds and would need real-SAT, nonrelativizing content.

## Falsifiers

- affine-incidence sketch with K+A_N+E_NN below N^{1+epsilon-o(1)}
- duplicate or even-multiplicity query generation causing p_x=0 on many inputs
- small generated universe with easy standard-basis coefficients, allowing all SAT labels on U_N to be hardwired
- sparse correction set E_N<N^{epsilon-o(1)} patched by equality tests
- target threshold collapse when max{q,rho}>=1+epsilon
- rank-only or entropy-only argument that ignores the actual SAT label vector
- natural-proof risk if the affine-sketch exclusion is large and efficiently testable over random label tables rather than range-specific to SAT

## Learning

Cycle 53 converts the XOR repair into an exact affine-incidence conservation law. The carrier equals the F_2 inner product of the SAT label vector with a generated parity-incidence vector; low-dimensional computable incidence structure makes the carrier easy by hardwiring basis parities. This is a new concrete falsifier for the source lower bound, while the polylog-query target bridge remains valid.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The XOR pivot removed the OR-specific separator obstruction but introduced a precise linear-algebra leakage mode. A concrete experiment can determine whether the next obstruction is low affine rank, easy coefficients, or only the missing arbitrary-circuit lower bound.
- Situation seed: Construct H_N^oplus from M=N^q slots with q=1+epsilon/2, L=(log N)^2, and a shared generator G_{N,theta} that maps (x,j) into a universe U_N(theta) of SAT instances while the parity-incidence vectors p_x have intended span size about N^theta.
- Varied variable: theta, the exponent log_N of the smallest computable affine-incidence sketch dimension K for {p_x}.
- Held-fixed controls: d=2 so exhaustive SAT lookup costs 2^L=N^{omega(1)} and does not create the old short-query falsifier., q=1+epsilon/2 and rho<1+epsilon/4 so the substitution bridge remains target-preserving., Circuit model remains nonuniform general SIZE with equality patches charged as E_NN., The target consequence remains SAT notin P/poly, not a restatement of P vs NP.
- Expected observation: For theta<1+epsilon, hardwiring basis parities gives an immediate subthreshold upper bound. For theta>1+epsilon, the affine falsifier disappears only if coefficient circuits also cost superthreshold; this still teaches only source plausibility, not a lower bound.
- Transfer certificate needed: Before the intuition affects proof obligations, supply either an explicit subthreshold affine sketch as a falsifier or a nonrelativizing direct lower-bound certificate for C(H_N^oplus)>N^{1+epsilon-o(1)} that is stronger than incidence-rank counting.

## Next Experiment

Instantiate G_{N,theta} with linear, pairwise-independent, and extractor-style query maps; compute K, coefficient-circuit cost A_N, duplicate parity cancellations, and whether any case survives the N^{1+epsilon} affine-sketch falsifier threshold.

# Barrier-Aware Lower-Bound Route: exact-junta threshold audit

## Candidate Lemma

Exact essential-variable or junta-size lower bounds give a valid lower bound only up to the number of variables mentioned by the target circuit. For fan-in-two SIZE(s), the bridge threshold is J>2s; for SAT on m input bits this is vacuous for s=m^k with k>1, since every m-bit function is an m-junta.

## Definitions

- source object: the m-bit truth-table function f_m, with motivating instance f_m=SAT_m or a padded SAT slice, and source measure J_0(f_m)=minimum exact junta size.
- target object: nonuniform fan-in-two Boolean circuits SIZE(s) on the same m-bit input length, or a restricted class C equipped with an explicit junta compiler.
- controlled interface: translate each target circuit of size s into an exact J_C(s)-junta; for unrestricted fan-in-two circuits J_C(s)<=2s because at most two fresh input variables can enter per internal gate.
- target-preserving condition: the source lower bound must prove J_0(f_m)>J_C(m^k) on the unpadded target length; if J_C(m^k)>=m the transfer is nonvacuous only for a restricted target with a smaller certified compiler threshold.

## Assumptions

- Circuit size counts fan-in-two internal gates; changing conventions only changes the constant in 2s.
- The lower-bound claim is exact, not average-case, unless an explicit approximate-junta compiler is separately supplied.
- The SAT slice length used by the source measure is the same length used in the target SIZE(m^k) threshold.

## Equations

- essential_variable_count: `E(f)=|\{i\in[m]:\exists x\ f(x)\ne f(x\oplus e_i)\}|`. Valid when: Valid when f is a total Boolean function on the full m-bit cube and coordinate flips are defined inside that cube.
- exact_junta_identity: `J_0(f)=E(f)\le m`. Valid when: Valid when exact junta size means the minimum number of input coordinates on which f depends.
- circuit_to_junta_bound: `g\in SIZE(s)\Rightarrow E(g)\le 2s`. Valid when: Valid when circuits have fan-in two and size counts internal gates, with constants adjusted for the chosen basis.
- exact_transfer: `J_0(f)>2s\Rightarrow f\notin SIZE(s)`. Valid when: Applies after the circuit-to-junta translation preserves the same input length and target size parameter s.
- polynomial_size_collapse: `2m^k>m\quad(k>1)`. Valid when: Requires the target lower bound to be against SIZE(m^k) on m input bits with k strictly larger than one.

## Attempted Derivation

- Let f_m=SAT_m and attempt to prove SIZE(m^k) lower bounds through exact essential variables.
- The syntactic compiler gives every size-s fan-in-two circuit at most 2s essential input variables.
- Thus a valid transfer would require E(SAT_m)>2m^k.
- But E(SAT_m)<=m for every m-bit function, so the required inequality is impossible for k>1.
- Trying to pad SAT to length n=m^beta only changes the ceiling to E<=m while the target threshold becomes n^k, worsening the mismatch.

Blocking gap: There is no target-preserving compiler from unrestricted SIZE(m^k) to o(m)-juntas; parity supplies a small-circuit falsifier.

## Falsifiers

- Parity_m is computable by O(m) gates, has E=m, and is 1/2-far from every J-junta with J<m; it is the decisive falsifier to any claim that many relevant variables imply P-hardness.
- The addressing function has small circuits and remains far from very small juntas under natural parameter choices, blocking approximate-junta enthusiasm for unrestricted SIZE.
- Padded SAT with core length r and total length n=r^beta preserves NP-hardness while the source ceiling E<=r is measured against the larger target SIZE(n^k) threshold.
- A natural-proof audit is valid here: the property E(f)>J is poly(2^m)-constructive and large for J<m-O(1), but usefulness against SIZE(m^k) collapses when J_C(m^k)>=m.

## Learning

Cycle 53 converts exact-junta and essential-variable lower-bound enthusiasm into a precise target gate: J_0(f)>2s is a valid SIZE(s) bridge, but J_0(f)<=m makes it useless for SIZE(m^k), k>1. Approximate-junta variants are not automatically invalid, but they need a named target compiler such as a low-influence theorem and a nonvacuous J<m threshold. This is route-level progress only, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The route's only apparent bridge is syntactic, so a concrete padded SAT family directly tests whether the essential-variable threshold is target-preserving rather than merely nonzero.
- Situation seed: Define L_beta on n-bit inputs by L_beta(x,0^{n-r})=SAT_r(x) with r=n^{1/beta} and reject all other padded strings; use the full n-bit truth-table function as the source object.
- Varied variable: padding exponent beta>1
- Held-fixed controls: many-one NP-hardness is preserved by the standard padding map x -> x0^{n-r}, target class remains fan-in-two nonuniform SIZE(n^k) on the padded length n, source statistic remains exact essential-variable count or exact junta size, no advice or promise restriction is allowed in the target transfer
- Expected observation: E(L_beta,n)<=r=n^{1/beta}, while the valid circuit-exclusion threshold is greater than 2n^k; increasing beta widens the gap and demonstrates quantitative threshold erosion.
- Transfer certificate needed: A repaired route would need a restricted-class compiler J_C(n^k)=o(n^{1/beta}) or an approximate-junta theorem with explicit epsilon, distribution, and uniformity preservation; without it the intuition cannot enter the proof queue.

## Next Experiment

Audit approximate-junta transfers for low-influence or depth-2 targets: compute when Friedgut's J=exp(O(I/epsilon)) is below m for SIZE(m^k) subclasses, and separate genuine AC0/DNF progress from another unrestricted SIZE collapse.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Rooted edit leakage has max-exponent accounting: if an emitted truth table T differs from an easy root A on R positions, then T has a nonuniform circuit computing A plus hardwired exceptions. Hence any subthreshold rooted ball around any easy center is a valid falsifier for MCSP no-side soundness; the number of possible centers or low-image ranks does not add to the circuit-size exponent for an individual row.

## Definitions

- source object: E-uniform low-image MCSP certificate source S_m emitting truth tables T in {0,1}^{2^m}, with canonical distinct-image rank and no advice.
- target object: unrestricted circuit lower bound for an E language obtained by rank-input multiplexing, with exponent delta after kappa padding.
- controlled interface: canonical unranking plus sequential table evaluation within 2^{O(m)} time; no subthreshold local decoder or nonuniform length selector.
- target-preserving condition: at least one emitted distinct row must satisfy C(T)>2^{epsilon m}; rooted edit descriptions, easy anchors, and rank indices may not themselves give circuits below that threshold.

## Assumptions

- A is a Boolean function on m bits with unrestricted circuit size C(A) <= 2^{xi m+o(m)}.
- T differs from A on at most R <= 2^{eta m+o(m)} input points.
- Circuits are nonuniform, so the nearest root and the edit list may be hardwired for a fixed row.
- MCSP no-side threshold is s_m=2^{epsilon m}, with constant epsilon>0.

## Equations

- rooted_edit_upper_bound: `C(T) <= C(A)+O(mR) <= 2^{max(xi,eta)m+o(m)}`. Valid when: Valid when T is obtained from a fixed easy root by explicitly hardwiring the changed input locations and output overrides.
- subthreshold_root_falsifier: `max(xi,eta) < epsilon  =>  T is not a no-side MCSP witness at threshold 2^{epsilon m}`. Valid when: Applies when the target threshold is an unrestricted circuit-size threshold and the edit list is available nonuniformly for the row.
- multiplexed_extraction_unchanged: `delta < epsilon/(kappa(1+D))`. Valid when: Requires the target-preserving low-image carrier transfer after a genuinely hard row is certified and canonical unranking is E-uniform.

## Attempted Derivation

- Start with a low-D carrier image and a known easy anchor A_m, hoping that large cumulative edit volume along the construction path forces a hard endpoint.
- Construct the nonuniform circuit for an endpoint T by hardwiring A_m and the final symmetric-difference edit set E(T,A_m), giving size C(A_m)+O(m|E|).
- Observe that the number of candidate anchors, ranks, or path branches is irrelevant once the fixed endpoint circuit is chosen.
- Try to rescue the argument by requiring large distance from A_m only.
- Find the gap: T may be close to a different easy circuit B, so hardness requires a global anti-ball statement over all subthreshold B, not a rooted path-volume statement.

Blocking gap: No known E-uniform, sparse, non-natural certificate proves global anti-ball avoidance for a low-D emitted row without effectively solving MCSP or reintroducing a large constructive property.

## Falsifiers

- Subthreshold rooted ball falsifier: T=A plus at most 2^{eta m} edits with C(A)<=2^{xi m} and max(xi,eta)<epsilon.
- Center-count overcharge falsifier: adding beta, D, or rank-search cost to an unrestricted fixed-row circuit is invalid.
- Single-anchor certificate falsifier: distance from the construction root does not rule out closeness to another easy center.
- Smooth path with cancellations falsifier: large cumulative edit count need not imply large final Hamming distance from any easy circuit.
- Lex-first global safe row falsifier: if implemented by dense constructive search over all small circuits, the repair is either outside E or collides with natural-proofs largeness.
- Local or interval decoder falsifier: any subthreshold indexed access profile still yields small circuits for emitted rows.

## Learning

Cycle 53 corrects the rooted-volume accounting: for unrestricted MCSP row hardness, a circuit may hardwire the chosen easy center and final edit list, so the leakage exponent is max(xi,eta), not beta+eta or D+eta. This strengthens the falsifier for proposed sources and identifies the real next obligation as a global anti-ball certificate. The established carrier extraction is still valid only conditionally and gives no direct proof of P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for rooted-volume source proposals.`
- Rationale: The current branch is blocked by explicit source construction, and the new issue is quantitative: whether edit radius, not path length or center count, controls MCSP soundness against unrestricted circuits.
- Situation seed: For each m, take an easy anchor A_m such as parity or 0^N, emit a low-D family of tables T_{m,j}=A_m xor E_{m,j}, where each E_{m,j} flips exactly R=2^{eta m} positions chosen by a sequential certificate; then test whether this can be a no-side GapMCSP carrier at threshold 2^{epsilon m}.
- Varied variable: The edit-radius exponent eta, crossing below and above epsilon while keeping D, kappa, and the verifier budget fixed.
- Held-fixed controls: MCSP threshold s_m=2^{epsilon m} for unrestricted nonuniform circuits., Distinct-image entropy D=O(1) with E-canonical unranking and no advice., Kappa-dense source lengths and the established extraction target delta<epsilon/(kappa(1+D))., No local decoder, no block restart below threshold, and no nonuniform length selector.
- Expected observation: For eta<epsilon, every emitted row is circuit-easy by the hardwired edit circuit, so the carrier is invalid. For eta>epsilon, this specific root leak disappears, but soundness still needs exclusion from all other subthreshold rooted balls.
- Transfer certificate needed: An E-uniform, non-large, non-natural global anti-ball certificate for at least one emitted row, plus canonical low-D unranking, before the thought experiment can support the carrier-to-E lower-bound transfer.

## Next Experiment

Formalize a tiny-D aggregate of candidate rows and test whether pairwise anti-ball constraints can certify one hard row without lex-first search, dense largeness, or subthreshold ranked decoding.
