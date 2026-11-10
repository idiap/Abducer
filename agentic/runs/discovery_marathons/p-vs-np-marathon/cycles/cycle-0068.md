# cycle-0068

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For the beta=0 XOR carrier with polylogarithmic SAT queries, the all-exponent target bridge remains valid, but label-mediated largeness yields only image-relative naturalness. It becomes a standard Razborov-Rudich style natural property only after a constructive density-preserving extension from the realization image to ambient N-bit truth tables.

## Definitions

- source object: H_N(x)=\oplus_{j\le M} SAT(G_N(x,j)) on N-bit seeds x, with M=N^q and G_N outputting SAT instances of length L=(log N)^d.
- target object: SAT on L-bit formula encodings; the route target is SAT notin SIZE(n^c) for every fixed c, hence NP not subset P/poly only if the carrier lower bound is valid in the same nonuniform circuit model.
- controlled interface: beta=0 XOR substitution where a target SAT circuit of size L^c is inserted into each generated query, with generator cost N^{rho+o(1)} and no extra advice depending on SAT labels.
- target-preserving condition: fixed d>1, q<1+epsilon, rho<1+epsilon, uniform enumeration of G_N, and no nonuniform leakage outside the generator and substituted SAT circuit.
- label universe: U_N is the set of formula strings of length L that can appear as some G_N(x,j); for fixed d, |U_N|<=2^{O(L)}=2^{o(N)}.
- realization map: R_N:{0,1}^{U_N}->Boolean functions on {0,1}^N sends a label vector y to h_y(x)=\oplus_j y(G_N(x,j)).
- ambient largeness: natural-proofs largeness is measured among all N-bit Boolean functions, not merely among Im(R_N).

## Assumptions

- Circuit model is nonuniform Boolean fan-in-two SIZE, and the source lower bound C(H_N)>N^{1+epsilon} is asserted in exactly this model.
- SAT circuits are allowed nonuniformity only as a circuit family for length L; the substitution cannot receive per-seed advice or precomputed SAT labels.
- The query length exponent is beta=0 because L=(log N)^d; positive beta reactivates the q+beta c threshold falsifier.
- The naturalness audit uses standard ambient density at least 2^{-poly(N)} unless an image-relative variant is explicitly named.
- No constructive extension from Im(R_N) to an ambient dense property is assumed; proving such an extension is a separate barrier-triggering obligation.

## Equations

- beta0_target_transfer: `C(H_N) \le N^{\rho+o(1)}+N^q L^c = N^{\max\{\rho,q\}+o(1)}`. Valid when: Valid when beta=0 means L=(log N)^d and SAT circuits of size L^c are substituted independently into the M=N^q generated queries.
- all_exponent_consequence: `C(H_N)>N^{1+\epsilon} \;\wedge\; \max\{\rho,q\}<1+\epsilon \Rightarrow \forall c\; SAT\notin SIZE(n^c)`. Valid when: Applies after the reduction preserves nonuniform circuit model identity, generator overhead rho, query multiplicity q, and the fixed polylogarithmic query length.
- realization_image_density: `\mu_{amb}(Im(R_N)) \le 2^{|U_N|-2^N} \le 2^{-2^N+2^{O((\log N)^d)}}`. Valid when: Requires source functions on N input bits and carriers determined solely by labels on the generated formula universe U_N.
- standard_largeness_failure: `|U_N|=2^{o(N)} \Rightarrow \mu_{amb}(Im(R_N))<2^{-N^a}\quad\text{for every fixed }a`. Valid when: Valid when d is fixed, L=(log N)^d, and natural-proofs largeness is the standard ambient 2^{-poly(N)} threshold.

## Attempted Derivation

- Fix M=N^q, L=(log N)^d with d>1, and let G_N have size N^{rho+o(1)}.
- Assume SAT on L-bit formulas has circuits of size L^c. Substitute that circuit into all M XOR positions and compute G_N uniformly, giving C(H_N)<=N^{max{rho,q}+o(1)}.
- Thus a valid source lower bound C(H_N)>N^{1+epsilon} contradicts SAT in SIZE(n^c) for every fixed c when max{rho,q}<1+epsilon.
- Define U_N as the generated formula universe and R_N(y)(x)=xor_j y(G_N(x,j)). Since formula strings have length L, |U_N|<=2^{O(L)}=2^{o(N)}.
- The image Im(R_N) has at most 2^{|U_N|} carrier functions, while the ambient N-bit function space has size 2^{2^N}; hence any property supported only on Im(R_N) has density at most 2^{|U_N|-2^N}.
- Therefore a label-mediated proof can be image-relative large and still fail standard natural-proofs largeness by an exponential margin.
- For XOR maps, equal fiber sizes show label density transfers to image-relative density, so the exact missing certificate is not density inside the image but a constructive ambient extension preserving soundness.

Blocking gap: No direct lower bound for the real SAT-label carrier H_N is obtained, and no polynomial-time density-preserving extension from Im(R_N) to ambient N-bit truth tables is known.

## Falsifiers

- Positive beta target-query length gives the q+beta c+o(1) substitution cap and blocks all-exponent transfer.
- q>=1+epsilon or rho>=1+epsilon makes the substituted SAT upper bound compatible with the proposed source lower bound.
- A low-cost label-free quotient transcript or affine incidence sketch still gives a direct upper-bound falsifier for the XOR carrier.
- A constructive density-preserving ambient extension turns an image-relative certificate into a standard natural property and triggers the natural-proofs obstruction in the same circuit model.
- Nonuniform leakage through precomputed SAT labels for U_N invalidates the controlled interface.
- If d is not fixed polylogarithmic, the image-density calculation and beta=0 classification must be recomputed before it is valid.

## Learning

Cycle 68 separates two notions previously conflated: label-mediated certificates for the beta=0 XOR carrier are large inside the realization image, but the image has ambient density at most 2^{-2^N+2^{o(N)}}. Thus the valid bridge to SAT notin P/poly survives, while the standard natural-proofs barrier requires a separate constructive ambient extension; this is a sharper route-status theorem, not progress on the main conjecture itself.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and parameter-threshold calibration.`
- Rationale: The branch no longer needs another statement that beta=0 is promising; it needs to know whether proof-mediated certificates are standard-natural, merely image-natural, or blocked by an extension theorem.
- Situation seed: Take an XOR carrier with q=1+epsilon/2, rho=1+epsilon/3, L=(log N)^2, and U_N equal to all formula strings ever output by a uniform generator G_N. Give the imagined prover a searchable certificate that is large over labels on U_N and sound for C(R_N(y))>N^{1+epsilon}.
- Varied variable: The extension-density exponent a in a proposed ambient extension A_N with density 2^{-N^a}, while keeping the label property density fixed inside {0,1}^{U_N}.
- Held-fixed controls: beta=0 polylogarithmic query length and the same nonuniform SIZE model for source and target circuits, q,rho<1+epsilon so the target substitution bridge remains valid for every fixed SAT circuit exponent, no advice leakage beyond G_N and the substituted SAT circuit, soundness must imply hardness of the realized N-bit carrier function, not just hardness of SAT labels
- Expected observation: Without an extension, the property is supported on at most 2^{2^{O((log N)^2)}} realized functions and has ambient density about 2^{-2^N}; with a constructive extension of density 2^{-poly(N)}, the usual natural-proofs obstruction becomes formally relevant.
- Transfer certificate needed: A polynomial-time ambient extension theorem that preserves usefulness against SIZE(N^{1+epsilon}), or a proof that every valid certificate remains nonlarge, nonconstructive, or nonextendable.

## Next Experiment

Formalize the extension problem: given R_N and a sound searchable label certificate, prove either that no poly(N)-time ambient extension of density 2^{-poly(N)} exists for this certificate class, or that such an extension exists and therefore naturalizes the route.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

A proof-mediated local lower-bound route still naturalizes if ordinary soundness is supplemented by a target-side consistency extractor and by a low-support accepting seed cluster. For C_s=SIZE_m(s), s=m^k, these two finite certificates turn the projected-view property into a poly(N)-constructive N^{-a}-large property useful against C_s; hence the route faces the natural-proofs falsifier unless it breaks one certificate.

## Definitions

- source object: A public-coin local proof verifier V for LB(f,s), where f in {0,1}^N is a truth table, N=2^m, s=m^k, randomness length r, truth-table query bound q, proof-view query bound b, and ordinary soundness is against C_s=SIZE_m(s).
- target object: A Razborov-Rudich natural property R_tau subset {0,1}^N that is intended to contain H=TT(SAT_m) and be useful against C_s=SIZE_m(m^k).
- controlled interface: The projected-view predicate A_V(f,rho)=1 iff some b-bit local proof view makes V accept after its q truth-table queries; the repair interface is a K-consistency extractor converting many projected accepting views on an easy f into one global proof.
- target-preserving condition: For every g in C_s, projected acceptance rate at least tau must imply a global proof accepted with probability greater than the ordinary soundness delta, and the accepting SAT seed cluster must query only d=O(log N) truth-table coordinates.

## Assumptions

- Uniformity: V's query addresses and predicate are computable in poly(N), and r+b+q=O(log N), so projected acceptance is decidable by exhaustive local-view enumeration.
- Ordinary soundness: for every g in C_s and every global proof pi, Pr_rho[V^g(pi;rho)=1] <= delta.
- Completeness with cluster: for H=TT(SAT_m) there is a set S of seeds of measure at least tau and local proof views w_rho such that V accepts H on each rho in S, and the union of all truth-table coordinates queried in these accepting transcripts has size d.
- Consistency extractor: for every g in C_s, if Pr_rho[A_V(g,rho)=1] >= tau, then some global proof pi satisfies Pr_rho[V^g(pi;rho)=1] >= tau/K.
- Threshold regime: K delta < tau and d <= a log_2 N for a fixed constant a independent of m.
- Non-claim boundary: the lemma is a route-level barrier gate, not an unconditional proof that SAT lacks circuits of size m^k.

## Equations

- projected_view_predicate: `A_V(f,\rho)=1 \iff \exists w\in\{0,1\}^{b}: V(f|_{Q(\rho,w)},w,\rho)=1`. Valid when: Valid when the verifier transcript is determined by the public seed and the enumerated local proof view, including unfolded adaptive queries.
- threshold_property: `R_{\tau}=\{f\in\{0,1\}^{N}: \Pr_{\rho}[A_V(f,\rho)=1]\ge \tau\}`. Valid when: Valid when r=O(log N), so the seed average is exactly computable in polynomial time from the truth table.
- usefulness_transfer: `R_{\tau}\cap C_s=\varnothing \quad \text{if}\quad K\delta<\tau`. Valid when: Applies after the consistency extractor is proved for the target class C_s and ordinary soundness is against all global proofs.
- constructivity_bound: `T_{dec}(R_{\tau})\le 2^{r+b}\,\mathrm{poly}(N)`. Valid when: Valid when proof-query values are the only nondeterministic local views and all verifier arithmetic is uniform polynomial time.
- largeness_from_cluster: `\mu(R_{\tau})\ge 2^{-d}\ge N^{-a}`. Valid when: Requires a fixed accepting seed cluster for H whose combined truth-table query support has size d at most a log N.

## Attempted Derivation

- Let H=TT(SAT_m) and C_s=SIZE_m(m^k). Start with a public-coin local proof verifier V for LB(H,s) with ordinary soundness delta and completeness c.
- Define A_V(f,rho) by existentially enumerating local proof views, then define R_tau by requiring projected acceptance on at least a tau fraction of seeds.
- Constructivity follows from enumerating 2^r seeds and 2^b local views, provided r+b+q=O(log N) and the verifier is uniform.
- Usefulness does not follow from ordinary soundness: the route needs a K-consistency extractor so that projected acceptance rate tau on an easy table yields a global proof accepted with probability at least tau/K, contradicting K delta < tau.
- Largeness does not follow merely from H in R_tau: the route needs an accepting seed cluster whose combined truth-table support is d=O(log N), giving a cylinder of density 2^{-d}.
- The 3-XOR proof-only verifier shows that ordinary soundness can coexist with projected acceptance on every seed; this is a concrete falsifier for the un-repaired bridge.

Blocking gap: No actual SAT lower-bound proof system in this branch has yet supplied both a target-side consistency extractor and a low-support accepting seed cluster at parameters K delta < tau and d=O(log N).

## Falsifiers

- 3-XOR local-proof falsifier: q=0,b=3 ordinary soundness can be at most 1/2+eta while projected local acceptance is identically one, so usefulness is not target-preserving.
- Expander seed-scatter falsifier: if every tau-measure accepting seed set queries N^{Omega(1)} distinct truth-table coordinates, the cylinder-density derivation of largeness fails.
- PRF falsifier: if the gate produces a poly(N)-constructive N^{-a}-large property useful against SIZE_m(m^k), standard PRF assumptions for that size class contradict the route's intended method.
- Advice-leakage falsifier: if the accepting seed cluster or proof-view selector requires superlogarithmic nonuniform advice, constructivity is no longer valid.

## Learning

Cycle 68 upgrades the long-proof escape into two named finite obligations: a K-consistency extractor for usefulness and a d=O(log N) accepting seed cluster for largeness. Ordinary soundness alone is invalid as a bridge, with 3-XOR giving a compact falsifier. This is valid route-level progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The open long-proof escape depends on two concrete quantities, consistency and accepting-seed support, so a target-preserving thought experiment is more useful than another barrier slogan.
- Situation seed: For each m,k imagine a public-coin local proof verifier V_{m,k} claiming to certify CC(TT(SAT_m))>m^k with r=C log N, q,b<=C log N, ordinary soundness delta=N^{-B}, and completeness c=1/2.
- Varied variable: The accepting seed-cluster support d, parameterized as d=O(log N) versus d=N^alpha for alpha>0, while keeping tau fixed below c.
- Held-fixed controls: Target class remains C_s=SIZE_m(m^k) with no advice leakage., Verifier query/address computation remains uniform poly(N)., Ordinary soundness delta and completeness c are held fixed., Projected local-view enumeration is allowed only for b=O(log N).
- Expected observation: If d=O(log N) and a K-consistency extractor with K delta < tau exists, the route naturalizes with density N^{-O(1)}; if d=N^alpha or the extractor fails, the natural-property transfer is blocked rather than promoted.
- Transfer certificate needed: A formal certificate proving either the extractor-plus-cluster conditions or a scatter/no-extractor theorem for the named verifier before this intuition may alter proof obligations.

## Next Experiment

Instantiate the gate on a concrete local proof or PCP-style verifier for circuit lower-bound statements: compute r,b,q, ordinary delta, candidate K, and the minimum support d of tau-measure accepting SAT seed clusters; run the 3-XOR falsifier against any claimed projection step.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

If a generated MCSP anti-ball carrier has subthreshold skip-ahead circuits to the configuration that emits row bit x, then every emitted row has a matching nonuniform circuit upper bound. Thus a no-side MCSP claim at exponent theta is invalid whenever theta exceeds the skip-ahead opening exponent.

## Definitions

- source object: a deterministic generated anti-ball MCSP carrier G_m emitting truth-table rows T_{m,a} of length N=2^m, with row identifiers a from an E-searchable sparse image family.
- target object: an E language L obtained by canonical row multiplexing and kappa-gap padding, intended to inherit unrestricted circuit lower bounds from hard rows.
- controlled interface: nonuniform or uniform skip-ahead openings J_{m,a}(x) returning the generator configuration immediately before emitting T_{m,a}[x], followed by a decoder B_m for the output bit.
- target-preserving condition: the row family is advice-free and E-canonical, the same emitted rows satisfy the MCSP no-side statement, and hardwiring a linear-size row identifier is negligible relative to 2^{theta m}.
- skip-ahead exponent zeta means |J_{m,a}| <= 2^{zeta m+o(m)} for every accepted row a.
- decoder exponent nu means |B_m| <= 2^{nu m+o(m)} on the opened configuration.

## Assumptions

- Unrestricted Boolean circuit size is the MCSP measure; no uniform-only lower bound is being claimed.
- The row identifier or certificate used to select a is O(m) or otherwise 2^{o(theta m)}, so it cannot hide the row as advice.
- The opening circuit computes the bit indexed by its input x in {0,1}^m, not merely a fixed position.
- The source soundness assertion is universal over accepted emitted rows, or the multiplexed construction canonically selects the row without advice.
- The lemma is a falsifier for a source implementation, not a proof of P != NP.

## Equations

- skip_upper_bound: `C(T_{m,a}) \le |J_{m,a}|+|B_m|+m^{O(1)} \le 2^{(\max\{\zeta,\nu\}+o(1))m}`. Valid when: Valid when the jump circuit outputs the exact pre-bit configuration and the decoder computes the row bit from that configuration.
- source_soundness_necessary_condition: `\theta \le \alpha_{skip}:=\max\{\zeta,\nu\}`. Valid when: Requires the source object to claim unrestricted MCSP no-side hardness for every emitted row at threshold 2^{theta m}.
- conditional_target_transfer_after_skip_audit: `\delta < \frac{\theta}{\kappa(1+D)}`. Valid when: Applies after the reduction preserves uniformity, density, image entropy, and no skip-ahead falsifier invalidates the source threshold.

## Attempted Derivation

- Fix m and an accepted emitted row T_{m,a}. Treat a and the generator descriptor as constants in a nonuniform circuit for the Boolean function x -> T_{m,a}[x].
- Use the skip-ahead circuit J_{m,a}(x) to compute the generator configuration immediately before the x-indexed output position.
- Feed that configuration to the row-bit decoder B_m. The composed circuit computes the full truth-table row as a function on m input bits.
- The composed size is at most 2^{zeta m+o(m)}+2^{nu m+o(m)}+m^{O(1)}, giving exponent max{zeta,nu}.
- Therefore a claimed MCSP no-side threshold 2^{theta m} is contradicted if theta>max{zeta,nu}.
- Combine this with the previous checkpoint cap alpha_chk; any valid source threshold must survive both leakage audits before the already established delta<theta/(kappa(1+D)) extraction is target-preserving.

Blocking gap: The derivation proves only a falsifier for carriers with explicit skip-ahead or iteratable transitions. It does not prove that every generated nonblackbox anti-ball source has such an opener, nor does it construct a skip-hard source.

## Falsifiers

- falsifier: an affine, linear-recurrence, LFSR, or algebraically iteratable row generator gives skip-ahead circuits below the claimed theta.
- falsifier: theta exceeds alpha_chk=max{sigma,nu,(1+sigma+nu)/2}, so checkpoint hardwiring already supplies small circuits for the rows.
- falsifier: theta exceeds alpha_skip=max{zeta,nu} for a direct opener, even if the checkpoint cap alone looked valid.
- falsifier: the row selector or proof skeleton is nonuniform advice rather than E-searchable canonical data.
- falsifier: sparse image entropy is repaired by a dense poly(N)-decidable projection, creating natural-property largeness pressure.
- falsifier: the carrier certifies only aggregate hardness or an advice-selected hard row, not the exact row used by the E-language extraction.

## Learning

Cycle 68 adds a sharper leakage channel than periodic checkpoints. A generated carrier can be globally sequential yet invalid if its transition is algebraically skippable: composing a skip-ahead opener with the bit decoder gives a nonuniform circuit for each row. This creates a finite falsifier for LFSR/affine/iteratable proof streams and upgrades the source obligation to noniteratable, skip-hard, advice-free anti-ball generation. The valid extraction theorem is unchanged and remains conditional route progress only.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe.`
- Rationale: The branch needs a concrete test separating genuine cap evasion from generators that only look sequential but have algebraic skip-ahead openings.
- Situation seed: A padded MCSP anti-ball row family emitted by an LFSR-like or linear cellular-automaton generator with state length 2^{sigma m}, sparse image entropy D, kappa-gap length padding, and claimed row hardness C(T_m)>2^{theta m}.
- Varied variable: state exponent sigma, equivalently the induced skip-ahead exponent zeta_C(sigma) for powering the transition on an m-bit index.
- Held-fixed controls: theta is a fixed positive MCSP no-side exponent for unrestricted circuits., D and kappa are held constant so the target transfer would be delta<theta/(kappa(1+D)) if the source were sound., The row family is advice-free and E-canonical; no nonuniform hard-row selector is allowed., The target remains an E lower-bound transfer, not a direct P vs NP claim.
- Expected observation: For algebraically iteratable generators, powering produces row circuits of exponent max{zeta_C(sigma),nu}; at small sigma this refutes constant theta even though the older checkpoint cap may allow theta up to about 1/2.
- Transfer certificate needed: A formal circuit construction for Pow_{Phi,m}(x) and the output decoder, plus a proof that the composed circuit computes the exact row used in the MCSP source claim.

## Next Experiment

Instantiate the skip-ahead audit for three transition classes: LFSR over poly(m) state, affine map over 2^{sigma m} state, and low-depth cellular automaton with known prediction circuits; compute zeta_C(sigma) and mark the theta ranges falsified.
