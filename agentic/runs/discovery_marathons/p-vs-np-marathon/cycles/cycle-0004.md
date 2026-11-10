# cycle-0004

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For projection-padded SAT carrier H_g at valid lengths N_m=(m+1)^{g(m+1)}, C(H_g|_{N_m}) is sandwiched by C(SAT_m) up to O(m). Thus an i.o. N^{1+eps} lower bound is an i.o. SAT lower bound m^{(1+eps)g(m+1)}, so unbounded g gives NP not subset P/poly but no weak-source magnification.

## Definitions

- source object: H_g is a projection-padded SAT language with valid lengths N_m=(m+1)^{g(m+1)} and fan-in-two Boolean circuit lower bounds on those slices.
- target object: SAT_m against nonuniform fan-in-two Boolean circuits SIZE(m^c), with target consequence NP not subset P/poly.
- controlled interface: contrapositive projection from a target SAT circuit family to a valid-length H_g circuit family, using only length-dependent wiring.
- target-preserving condition: g(m)->infty on the lower-bound subsequence, and the H_g lower bound is asserted only at valid lengths N_m.

## Assumptions

- C_n(f) denotes minimum fan-in-two Boolean circuit size for the n-bit slice.
- The valid-length sequence is injective and g is unbounded on the claimed lower-bound subsequence.
- On length N_m, H_g depends only on the first m input bits and ignores padding bits.
- The source claim is i.o. C_{N_m}(H_g)>N_m^{1+eps}; invalid lengths are excluded.

## Equations

- valid_length_carrier: `N_m=(m+1)^{g(m+1)},\quad H_g(x)=SAT_m(x_1,\ldots,x_m)\text{ for }|x|=N_m`. Valid when: Valid when the source lower-bound model is explicitly restricted to these padded valid lengths.
- projection_sandwich: `C_m(SAT)\le C_{N_m}(H_g)+O(1),\quad C_{N_m}(H_g)\le C_m(SAT)+O(m)`. Valid when: Valid when the padding map is a projection and circuits may nonuniformly know the length.
- threshold_demagnification: `C_{N_m}(H_g)>N_m^{1+\epsilon}\Rightarrow C_m(SAT)>(m+1)^{(1+\epsilon)g(m+1)}-O(m)`. Valid when: Applies after the reduction preserves the valid length and the lower-bound threshold exactly.

## Attempted Derivation

- Fix a valid length N_m and define H_g by copying the first m input bits into the SAT_m instance; invalid lengths are not part of the source lower-bound claim.
- If SAT_m has a circuit of size m^c, wire the first m inputs into it and ignore all padding bits, giving an H_g circuit of size m^c+O(m).
- If H_g at N_m has a circuit of size s, restrict the padding bits to constants; the resulting m-input circuit decides SAT_m with size s+O(1).
- Substitute N_m=(m+1)^{g(m+1)}. A barely superlinear bound in N is a superpolynomial SAT lower bound when g is unbounded.

Blocking gap: The bridge is valid, but its source obligation is not barely nontrivial in the original SAT length; it already asks for m^{omega(1)} SAT lower bounds.

## Falsifiers

- falsifier: if the lower bound is asserted on all lengths, invalid lengths are constant slices and the statement becomes false.
- falsifier: if the encoding is not a projection and needs an Omega(N) decoder, the O(N) floor collapses the N^{1+eps} threshold.
- falsifier: if g is bounded on the lower-bound subsequence, the consequence excludes only finitely many SAT exponents.
- falsifier: a large constructive proof property would meet the natural-proofs obstruction; this route needs a specific non-natural lower-bound argument.

## Learning

Cycle 4 proves a valid projection-sandwich lemma and demagnifies the sparse-padding route: N^{1+eps} lower bounds for H_g equal m^{(1+eps)g} SAT lower bounds. The bridge is correct but not a weak-source path toward P vs NP.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Test an MCSP or KT-complexity carrier with source model, threshold N^{1+eps}, and target NP not subset P/poly; compute the reduction overhead and state whether the needed proof must be non-natural or non-algebrizing.

# Barrier-Aware Lower-Bound Route: proof-complexity target-preservation audit

## Candidate Lemma

A superpolynomial lower bound for a fixed Cook-Reckhow proof system P0, such as EF or Frege, is not a valid bridge to P != NP unless the route supplies universal p-simulation by P0 or proves lower bounds for every Cook-Reckhow system. The lower bound only refutes P0-p-boundedness; the target NP != coNP requires absence of all p-bounded proof systems.

## Definitions

- source object: a fixed Cook-Reckhow proof system P0 and an explicit tautology family tau_n with claimed proof-size lower bound s_{P0}(tau_n)>|tau_n|^{omega(1)}.
- target object: NP != coNP as the proof-complexity target; this would imply P != NP, but it is stronger and must not be confused with the main conjecture itself.
- controlled interface: the Cook-Reckhow verifier V_P(pi,phi), proof length s_P(phi), and the p-simulation preorder between proof systems.
- target-preserving condition: P0 must p-simulate every polynomial-time Cook-Reckhow proof system, or the lower bound must quantify over every such system; otherwise fixed-system specificity leaks the target.

## Assumptions

- P0 is sound, complete for TAUT, and polynomial-time verifiable.
- The family tau_n is uniformly constructible and each tau_n is a tautology.
- p-simulation means polynomial-time translation with polynomial proof-length overhead.
- No p-optimality theorem for EF, Frege, or another named P0 is assumed for free.

## Equations

- proof_length: `s_P(\varphi)=\min\{|\pi|:V_P(\pi,\varphi)=1\}`. Valid when: Valid when P is a sound and complete Cook-Reckhow propositional proof system with polynomial-time verifier.
- cr_equivalence: `\mathrm{NP}=\mathrm{coNP}\iff \mathrm{TAUT}\in\mathrm{NP}\iff \exists P\in CR\ \exists c\ \forall \varphi\in\mathrm{TAUT}: s_P(\varphi)\le |\varphi|^c`. Valid when: Valid when proof systems range over all Cook-Reckhow systems and TAUT is the coNP-complete language.
- universal_lb_bridge: `[(\forall P\in CR)(\forall c)(\exists\varphi\in\mathrm{TAUT})\ s_P(\varphi)>|\varphi|^c]\Rightarrow \mathrm{NP}\ne\mathrm{coNP}`. Valid when: Applies when the lower bound quantifies over every polynomial-time verifiable proof system, not just one calculus.
- p_optimal_bridge: `[(P_0\ \text{p-simulates all}\ P\in CR)\wedge(\forall c)(\exists n)\ s_{P_0}(\tau_n)>|\tau_n|^c]\Rightarrow \mathrm{NP}\ne\mathrm{coNP}`. Valid when: Requires the target-preserving universal simulation hypothesis and an infinite uniformly constructible tautology family.
- extension_falsifier_system: `V_{P_\tau}(\pi,\varphi)=1\iff V_{P_0}(\pi,\varphi)=1\vee(\pi=(1,n)\wedge\varphi=\tau_n)`. Valid when: Valid when tau_n is uniformly constructible and each tau_n is already known to be a tautology.

## Attempted Derivation

- Start with a claimed source lower bound s_EF(tau_n)>|tau_n|^{omega(1)} for an explicit tautology family.
- Translate the desired target through the standard interface: NP=coNP iff some Cook-Reckhow proof system is polynomially bounded for all tautologies.
- Observe that the EF lower bound proves only that EF is not polynomially bounded on tau_n.
- Try to infer that no Cook-Reckhow system is polynomially bounded; this requires EF p-simulating every Cook-Reckhow system or a universal lower bound over all systems.
- Construct P_tau by adding tau_n as uniformly checkable axiom instances to P0. P_tau remains a valid Cook-Reckhow system and gives tau_n short proofs.
- Therefore the fixed-family, fixed-system lower bound is extension-fragile and cannot be the target-preserving bridge to NP != coNP.

Blocking gap: The missing inference is P0 not p-bounded implies no Cook-Reckhow proof system is p-bounded. This is exactly a p-optimality or universal-system lower-bound obligation, not a barrier slogan.

## Falsifiers

- falsifier: the valid Cook-Reckhow extension P_tau gives O(log n)-size proofs of the allegedly hard family tau_n while preserving soundness and completeness.
- falsifier: a route whose theorem mentions only EF, Frege, Resolution, or Cutting Planes has not reached NP != coNP unless a universal simulation theorem is added.
- falsifier: assuming a p-optimal Cook-Reckhow proof system as an interface condition is invalid unless the route proves it or explicitly makes it a conditional target.

## Learning

Cycle 4 converts proof-complexity enthusiasm into a precise bridge obligation: fixed-system lower bounds are extension-fragile. The P_tau construction is a concrete falsifier for the invalid inference from EF lower bounds to NP != coNP. This is valid route-level progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Audit feasible-interpolation routes: name source proof system, interpolation extraction model, target circuit class, and check whether the extracted circuit lower bound avoids natural-property and extension-fragility falsifiers.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Let GapMCSP have no-threshold t(N)=N^epsilon. If there is an E-uniform explicit sequence of no-side truth tables T_k of lengths N_k=2^{n_k}, with C(T_k)>N_k^epsilon and n_{k+1}/n_k<=gamma for a constant gamma, then there is H in E with all-length lower bound CC(H_r)>2^{delta r} for every fixed delta<epsilon/gamma. Hence the carrier gives the IW derandomization hypothesis, not P != NP.

## Definitions

- source object: an E-uniform sequence (T_k,n_k) of truth tables for n_k-bit Boolean functions, where T_k is a no-instance of GapMCSP_{*,N^epsilon}.
- target object: a language H in E satisfying all-length circuit lower bounds CC(H_r)>2^{delta r} for some positive constant delta.
- controlled interface: for each target length r, choose the largest source log-length n_k<=r and define H on r-bit inputs by evaluating T_k on the first n_k bits.
- target-preserving condition: the source log-length gaps are bounded by a constant gamma and the hard-table selector is uniform, so delta<epsilon/gamma remains positive.

## Assumptions

- Source model is GapMCSP on truth-table inputs of length N=2^n with no-side condition C(T)>N^epsilon.
- The sequence n_k is increasing, computable from r in poly(r), and satisfies sup_k n_{k+1}/n_k<=gamma<infinity.
- Each requested bit of T_k is computable in time 2^{O(n_k)}, or equivalently the full table is generated in E-uniform time 2^{O(n_k)}.
- Target model is deterministic E and nonuniform Boolean circuits measured separately at each input length.

## Equations

- mcsp_no_side_threshold: `N_k=2^{n_k}, C(T_k)>N_k^{epsilon}=2^{epsilon n_k}`. Valid when: Valid when the source carrier outputs GapMCSP no-instances at threshold N^epsilon with explicit log-length n_k.
- constant_gap_padding_window: `n_k <= r < n_{k+1} <= gamma n_k implies n_k > r/gamma`. Valid when: Applies when every sufficiently large target length is padded from the previous source log-length.
- padded_language_definition: `H(w)=T_k(w_1,...,w_{n_k}) for |w|=r and k=max{i:n_i<=r}`. Valid when: Valid when the selector k(r) is uniformly computable and ignored suffix bits are genuine padding.
- target_lower_bound_transfer: `CC(H_r) >= C(T_k)-O(r) > 2^{epsilon r/gamma}-O(r) >= 2^{delta r}`. Valid when: Requires constant gamma and any fixed delta below epsilon divided by gamma for all large r.
- iw_consequence: `H in E and CC(H_r)>2^{delta r} for all large r implies BPP=P by IW`. Valid when: Requires the standard Impagliazzo-Wigderson theorem with uniform all-length exponential circuit hardness.

## Attempted Derivation

- Assume an explicit GapMCSP no-side carrier T_k at log-lengths n_k with C(T_k)>2^{epsilon n_k}.
- For every target length r choose k=max{i:n_i<=r}; bounded gaps give n_k>r/gamma.
- Define H on r-bit inputs by applying T_k to the first n_k bits and ignoring the suffix.
- Uniformity of n_k and the bit generator for T_k puts H in E, since n_k<=r and evaluation costs 2^{O(r)}.
- Any size-s circuit for H_r restricts, after fixing the ignored suffix, to a size s+O(r) circuit for T_k.
- Thus s>2^{epsilon n_k}-O(r)>2^{delta r} for every delta<epsilon/gamma and all large r.
- By IW, this conditional all-length E lower bound yields BPP=P; the route-level consequence is derandomization, not a proof of P != NP.

Blocking gap: The current branch has not constructed an E-uniform explicit no-side MCSP selector with constant log-length gaps. Known density or counting facts do not identify valid tables without solving the meta-complexity problem or using nonuniform advice.

## Falsifiers

- falsifier: source lengths have n_{k+1}/n_k unbounded, causing the transferred exponent epsilon n_k/r to approach zero at intermediate target lengths.
- falsifier: the carrier selects high-MCSP tables by advice, oracle search, or counting, so the constructed target is nonuniform and not a valid E language.
- falsifier: the MCSP reduction is length-balanced only on a sparse subsequence with superconstant gaps, giving sparse lower bounds but no IW all-length premise.
- falsifier: the no-side threshold is t(N)=N^{epsilon(N)} with epsilon(N)->0, so even constant-gap padding yields no fixed positive delta.
- falsifier: the source object is natural in the Razborov-Rudich sense, namely a large polynomial-time decidable useful property against circuits under standard PRF assumptions; the present single-sequence bridge avoids largeness, but a dense constructive proof may not.

## Learning

Cycle 4 sharpens the route: rho-dense all-length carriers are sufficient but not necessary. A constant-gap explicit no-side MCSP sequence already transfers to all-length E hardness with exponent delta<epsilon/gamma. Conversely, superconstant gaps or epsilon(N)->0 create a quantitative threshold collapse, and nonuniform selectors invalidate the target class.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Search for a length-balanced co-side GapMCSP reduction from an explicit E-decidable source with canonical no-instances at every m or at constant-gap m; verify output log-length n=Theta(m), fixed threshold N^epsilon, and an E-uniform bit generator for the produced truth tables.
