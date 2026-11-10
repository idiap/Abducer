# cycle-0066

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For the beta-zero XOR carrier, a short searchable proof predicate becomes a standard natural-property obstruction only after an explicit density-preserving label-realization map is supplied. Without that map, largeness in artificial SAT-label space is not by itself a valid natural-proofs barrier; with it, any large sound searchable proof predicate is a natural property useful against the pulled-back function class.

## Definitions

- source object: the parametric XOR carrier H_{N,y}(z)=\bigoplus_{u\in U_N} I_N(z,u)y_u, with real source y=SAT|_{U_N} and source model nonuniform Boolean circuits on N-bit carrier inputs.
- target object: all fixed-polynomial SAT_L circuit lower bounds, hence SAT notin P/poly only through the preserved beta=0 polylog-query bridge, not by restating P != NP.
- controlled interface: a label-free generator G_N creates M_N=N^q SAT instances of length L=(log N)^d, the incidence map I_N is computed with overhead N^{rho+o(1)}, and SAT circuits are substituted only through labels of length L.
- target-preserving condition: max{rho,q}<1+epsilon, d>1, no advice depending on SAT|_{U_N}, and any proof predicate must be sound for the parametric carrier rather than only for the actual SAT label.
- A_N(y)=1 means there exists a Psys proof pi of length at most ell_N accepted by verifier V_N(y,pi), where V_N is searchable in time poly(2^n) or the declared naturalness-constructive bound.
- A label-realization certificate is a computable map R_n from truth tables of n-bit functions to label vectors y in {0,1}^{U_N}, plus an input projection tau_n, such that H_{N,R_n(f)} computes f∘tau_n with overhead chi_N.
- D_N is the pullback distortion satisfying Pr_f[R_n(f) in B]>=D_N^{-1}Pr_y[y in B] for all accepted label sets B under consideration.

## Assumptions

- Circuit model is nonuniform Boolean circuits; uniformity enters only in computing G_N, I_N, V_N, and R_n.
- Psys soundness is same-theory parametric soundness: A_N(y)=1 implies C(H_{N,y})>N^{1+epsilon} for every label vector y, not merely for y=SAT|_{U_N}.
- Constructivity means A_N is decidable by exhaustive proof search within the natural-proofs truth-table time bound after accounting for ell_N.
- Largeness for the pulled-back property is the quantitative condition Pr_f[A_N(R_n(f))=1]>=2^{-O(n)}; label-space density alone is insufficient unless D_N is bounded.
- No nonuniform advice may encode SAT|_{U_N}; otherwise the proof predicate is a target-destroying leakage channel.

## Equations

- beta_zero_substitution: `C(H_N^{SAT}) \le N^{\rho+o(1)}+N^q L^c=N^{\max\{\rho,q\}+o(1)}`. Valid when: Valid when L=(log N)^d, SAT_L has size L^c circuits, and the generator plus incidence computation is label-free with cost N^{rho+o(1)}.
- parametric_carrier: `H_{N,y}(z)=\bigoplus_{u\in U_N} I_N(z,u)y_u`. Valid when: Valid when U_N is the fixed generated formula universe and I_N is computed independently of the SAT label vector y.
- accepted_label_density: `\mu_N=2^{-|U_N|}\left|\{y:\exists \pi, |\pi|\le \ell_N, V_N(y,\pi)=1\}\right|`. Valid when: Valid when the verifier is evaluated over artificial label vectors y and proof length cutoff ell_N is fixed before seeing y.
- pullback_density: `\nu_n=\Pr_f[A_N(R_n(f))=1]\ge D_N^{-1}\mu_N`. Valid when: Applies after a density-distortion certificate R_n,D_N proves that accepted label sets pull back to truth-table functions with bounded loss.
- usefulness_transfer: `A_N(R_n(f))=1\Rightarrow C(f)>N^{1+\epsilon}/\chi_N`. Valid when: Requires parametric soundness for H_{N,y} and a realization certificate showing circuits for f induce circuits for H_{N,R_n(f)} with overhead chi_N.

## Attempted Derivation

- Parameterize the XOR carrier by an arbitrary label vector y so that the real SAT carrier is only the specialization y=SAT|_{U_N}.
- Assume a searchable Psys predicate A_N(y)=exists pi V_N(y,pi) with same-theory parametric soundness A_N(y)=>C(H_{N,y})>N^{1+epsilon}.
- If SAT_L has size L^c circuits, substitute those circuits into the real carrier and obtain C(H_N^{SAT})<=N^{max{rho,q}+o(1)}, preserving the beta=0 target bridge when max{rho,q}<1+epsilon.
- To convert A_N into a standard natural property, introduce a realization map R_n from n-bit function truth tables to label vectors and require H_{N,R_n(f)}=f∘tau_n up to overhead chi_N.
- Constructivity follows from computing R_n and searching pi within the declared truth-table time bound; usefulness follows because a small circuit for f would give a small circuit for H_{N,R_n(f)}.
- Largeness follows only if the pullback density nu_n is at least 2^{-O(n)}, or if a distortion bound D_N transfers label-space density mu_N to nu_n.
- Therefore a large searchable sound proof predicate plus label realization yields a natural property; absence of realization or largeness is an escape condition but also a new source proof burden.

Blocking gap: No explicit density-preserving label-realization map is known for the generated SAT universe U_N, and soundness of plausible proof predicates is usually shown only for the actual SAT label rather than for every artificial label y.

## Falsifiers

- falsifier: positive target-query exponent beta gives the upper bound N^{q+beta c+o(1)} and caps the target exponents before reaching SAT notin P/poly.
- falsifier: low constructive incidence rank or a global label-free codebook yields an explicit small circuit for the XOR carrier.
- falsifier: a large searchable sound proof predicate with density-preserving label realization becomes a natural property and is blocked under standard PRF-style assumptions.
- falsifier: no density-preserving realization map means label-space largeness is not a valid standard natural-proofs argument.
- falsifier: verifier advice or proof advice encoding SAT|_{U_N} destroys the target-preserving condition by nonuniform leakage.

## Learning

Cycle 66 sharpens the proof-mediated XOR route: searchable certificates do not automatically trigger the standard natural-proofs barrier. The valid obstruction needs parametric soundness, constructivity, large pulled-back density, and a density-preserving label-realization map. Without these, the barrier claim is invalid, but the source proof must be direct, nonlarge, nonconstructive, or explicitly nonrelativizing.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch already has the beta=0 transfer; the next uncertainty is whether proof-mediated source lower bounds are genuinely non-natural or only disguised large searchable properties.
- Situation seed: Take H_N(z)=xor_{j<=N^q} SAT(G_N(z,j)) with L=(log N)^2, q,rho<1+epsilon, and define an Extended-Frege-style verifier V_N(y,pi) for the parametric claim C(H_{N,y})>N^{1+epsilon}.
- Varied variable: the pulled-back acceptance density nu_n=Pr_f[exists pi V_N(R_n(f),pi)=1], ranging from 2^{-O(n)} to 2^{-omega(n)}
- Held-fixed controls: beta=0 polylog target queries and the transfer bound N^{max{rho,q}+o(1)}, label-free generator and incidence computation with no SAT-label advice, parametric soundness A_N(y)=>C(H_{N,y})>N^{1+epsilon}, searchable proof length cutoff ell_N within the declared constructivity bound
- Expected observation: If nu_n is large, the verifier defines a constructive useful natural property; if nu_n is tiny, the route can evade naturalness only by proving that the specific SAT label lies in a sparse proof-defined set.
- Transfer certificate needed: An efficient density-preserving realization map R_n and overhead chi_N proving H_{N,R_n(f)} computes f∘tau_n before the naturalness intuition may affect proof obligations.

## Next Experiment

Instantiate R_n for one high-q polylog XOR carrier or prove a finite impossibility: no label-free density-preserving realization can coexist with q,rho<1+epsilon and generator universe U_N of SAT formulas length (log N)^2.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

A public-coin proof-mediated local lower-bound verifier with logarithmic truth-table/proof view and soundness below the circuit-count times proof-count threshold induces a large constructive property useful against the same SIZE_m(s) target; hence the route naturalizes unless it escapes one named hypothesis.

## Definitions

- source object: a public-coin proof-mediated local lower-bound verifier V for f*=TT(SAT_m) claiming CC(f*)>s, with proof pi in {0,1}^ell, seed r in {0,1}^rho, q truth-table probes, and p proof-bit probes.
- target object: nonuniform Boolean circuits SIZE_m(s) over m input bits, identified with their N=2^m-bit truth tables.
- controlled interface: V^f(pi;r) has perfect completeness for f*, and for every C in SIZE_m(s) and every pi, Pr_r[V^{TT(C)}(pi;r)=1] <= delta.
- target-preserving condition: after fixing one valid seed r0, the induced property P_{r0}(f)=1 iff some p-bit local proof view makes V^f accept remains useful against the same SIZE_m(s) class and is decidable in poly(N), with r0 either uniformly found or treated as nonuniform advice.

## Assumptions

- Full truth-table model: the property recognizer receives the entire N-bit table of f and may query any coordinate in polynomial time in N.
- Circuit count model: fan-in-two Boolean circuits over a fixed finite basis are counted up to a constant A in #SIZE_m(s) <= 2^{A s log s}.
- Uniformity/advice regime: a nonconstructive seed r0 gives an advised natural property; a uniform natural property additionally needs a poly(N)-time seed-search or canonicalization procedure.
- Soundness is all-proof soundness in the same verifier model, not only soundness for proofs output by a particular prover.
- Perfect completeness holds for every public seed; otherwise the rejecting-seed union bound must also pay a completeness-error term.

## Equations

- truth_table_length: `N=2^m`. Valid when: Valid when the property is defined on complete truth tables of m-bit Boolean functions.
- circuit_count: `\#\mathrm{SIZE}_m(s)\le 2^{A s\log s}`. Valid when: Valid when circuits are encoded over a fixed finite fan-in basis and A absorbs basis and output-gate choices.
- seed_elimination_threshold: `\delta < 2^{-A s\log s-\ell-1}`. Valid when: Valid when soundness is averaged over the public seed and quantified for every small circuit and every complete proof string.
- largeness_after_fixing_seed: `\mu(P_{r0})\ge 2^{-q}`. Valid when: Applies when the fixed seed accepts the SAT table and the accepting computation path reads at most q distinct truth-table cells.
- constructivity_after_fixing_seed: `T_N(P_{r0})\le 2^p\operatorname{poly}(N)`. Valid when: Requires the seed to be fixed as uniform output or as nonuniform advice and the verifier to inspect only p proof bits.
- naturalness_regime: `p,q=O(\log N)\Rightarrow T_N(P_{r0})=\operatorname{poly}(N)\ \text{and}\ \mu(P_{r0})\ge N^{-O(1)}`. Valid when: Valid when both local access parameters are logarithmic in the truth-table length and the circuit target remains SIZE_m(s).

## Attempted Derivation

- Count bad pairs (C,pi) with C in SIZE_m(s) and pi in {0,1}^ell; there are at most 2^{A s log s+ell}.
- For each bad pair, all-proof soundness gives Pr_r[V^{TT(C)}(pi;r)=1] <= delta.
- If delta < 2^{-A s log s-ell-1}, the expected number of accepting bad pairs for a random seed is below 1/2, so some seed r0 rejects every bad pair.
- Perfect completeness ensures the same r0 accepts f*=TT(SAT_m) with the honest proof pi*.
- Define P_{r0}(f) by existentially enumerating the p proof bits seen by V at seed r0 and accepting iff some local view makes V^f accept.
- Usefulness follows because any accepting local view for TT(C) extends to a full proof pi, contradicting the choice of r0.
- Largeness follows by fixing the q truth-table answers along an accepting computation path for f*; the resulting cylinder has density at least 2^{-q}.
- Constructivity follows by enumerating 2^p local proof views and simulating V on the explicit N-bit table.

Blocking gap: The derivation needs either ultra-low all-proof soundness paying the full ell-bit proof count, or a separate view-soundness theorem. Standard proof-mediated certificates usually provide neither at the required SIZE_m(m^k) threshold.

## Falsifiers

- Constant-soundness PCP-style certificates with ell=poly(N) are a falsifier for naive seed fixing because delta*2^ell*2^{A s log s} is enormous.
- A verifier with q=omega(log N) is a falsifier for polynomial-density naturalization, since the accepting cylinder may be subpolynomially large.
- A verifier with p=omega(log N) is a falsifier for poly(N) constructivity by local-view enumeration.
- Nonuniform hidden advice selecting proof rows is a falsifier for target preservation unless the advice is charged in ell or separately audited.
- A proof-system-specific lower bound whose usefulness does not reject every SIZE_m(s) truth table is not a valid natural-property carrier.

## Learning

The new learning is the proof-length union threshold. A proof-mediated local lower-bound certificate does not escape natural proofs merely by using a proof: if p,q=O(log N) and the public randomness can be fixed against all circuits and proofs, the route yields a valid large constructive useful property. The exact escape is weak soundness, long-proof leakage, absent view-soundness, nonuniform seed advice, or loss of all-truth-table usefulness.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and threshold calibration.`
- Rationale: The branch has repeatedly found that local or proof-mediated slogans hide exact counting thresholds; this thought experiment varies only soundness to expose whether proof mediation truly escapes naturalness.
- Situation seed: For each m, imagine a public-coin local verifier V_m for the statement CC(TT(SAT_m))>m^k. The verifier has seed length rho=c log N, q=C log N truth-table probes, p=C log N proof probes, proof length ell, perfect completeness, and targets nonuniform SIZE_m(m^k).
- Varied variable: The soundness exponent gamma in delta=2^{-gamma}, compared against A m^k log m + ell; in the repair variant, gamma is compared against A m^k log m for view-soundness eta=2^{-gamma}.
- Held-fixed controls: The target class remains SIZE_m(m^k) over the unpadded m-bit SAT slice., The property recognizer receives the full N=2^m-bit truth table and no oracle other than the fixed seed/advice audit., Completeness is perfect for TT(SAT_m) on every public seed., The verifier's local access stays p,q=O(log N), so largeness and constructivity would be valid if a seed can be fixed.
- Expected observation: When gamma>A m^k log m+ell, a global seed produces an advised large constructive useful property; when gamma is below that threshold, proof-length leakage blocks the transfer. If view-soundness is proved, the ell term disappears.
- Transfer certificate needed: A formal certificate that soundness is either all-proof with gamma>A s log s+ell or semantic view-soundness with gamma>A s log s, plus a uniform seed-search certificate if the route wants uniform rather than advised naturalness.

## Next Experiment

Instantiate the lemma with s=m^k and ell in {O(log N), m^k log m, poly(N)}; compute the required gamma and check whether known PCP/amplification transformations can meet it without increasing p or q beyond O(log N).

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Checkpoint-cap falsifier for generated anti-ball MCSP carriers: a deterministic advice-free row/proof generator with small space and small per-output overhead yields nonuniform circuits for its emitted row, so it cannot soundly certify MCSP hardness above the checkpoint exponent theta_chk.

## Definitions

- source object: an advice-free deterministic generated anti-ball carrier G_m that emits a truth-table row T_m in lexicographic order and a nonblackbox proof that T_m is outside every Hamming ball around circuits of size below 2^{theta m}.
- target object: an E-uniform language L whose length-n truth tables are obtained from the accepted rows by distinct-image unranking and kappa-padding, with intended circuit lower bound 2^{delta n}.
- controlled interface: low-D distinct-image unranking plus sequential row/proof generation with declared per-output overhead nu, work-space exponent sigma, density gap kappa, threshold theta, and no advice.
- target-preserving condition: the transfer is valid only if row bits are E-computable, selected lengths are kappa-dense, image indices are E-canonical, and no checkpoint or opening upper bound below theta exists.
- checkpoint profile: after every W=2^{beta m} emitted row bits, a configuration of length 2^{sigma m+o(m)} is hardwired; the circuit selects the preceding checkpoint and simulates at most W outputs.
- row hardness model: CC(T_m)>2^{theta m} means unrestricted Boolean circuits on m input bits need more than 2^{theta m} gates to compute the Boolean function with truth table T_m.

## Assumptions

- Model is nonuniform unrestricted Boolean circuits for row hardness; hence hardwired checkpoint configurations are legal upper-bound witnesses.
- G_m is deterministic and advice-free; the checkpoint table is not an added selector, only a nonuniform circuit upper bound extracted from the actual computation history.
- The row stream has N=2^m bits, per-output overhead 2^{nu m+o(m)}, and work configuration length 2^{sigma m+o(m)} during the portion that emits T_m.
- The anti-ball proof may be long, but the circuit upper bound uses only configurations needed to resume the row-emission computation; proof text not read for target extraction is ignored.
- The lemma is a source-side falsifier only; it does not produce a lower bound or prove P != NP.

## Equations

- checkpoint_upper_bound: `CC(T_m) \le 2^{(\max\{1-\beta+\sigma,\,\beta+\nu\}+o(1))m}`. Valid when: Valid when G_m is a deterministic sequential transducer with restartable configurations of length 2^{sigma m+o(m)} and per-output overhead 2^{nu m+o(m)}.
- optimized_checkpoint_cap: `\theta_{chk}(\sigma,\nu)=\inf_{0\le \beta\le 1}\max\{1-\beta+\sigma,\,\beta+\nu\}`. Valid when: Valid when window checkpoints may be hardwired nonuniformly and beta ranges over all block lengths between one bit and the full table.
- balanced_cap_regime: `\theta_{chk}(\sigma,\nu)=\frac{1+\sigma+\nu}{2}\quad\text{if }0\le \nu\le 1+\sigma`. Valid when: Applies when the balancing block exponent beta=(1+sigma-nu)/2 lies inside the legal interval [0,1].
- soundness_necessary_condition: `\theta \le \theta_{chk}(\sigma,\nu)`. Valid when: Requires the source to claim MCSP no-side soundness CC(T_m)>2^{theta m} against unrestricted nonuniform circuits for every emitted row.

## Attempted Derivation

- Fix m and a deterministic generator G_m emitting T_m[0],...,T_m[N-1], N=2^m, with work configurations of at most 2^{sigma m+o(m)} bits and per-output overhead 2^{nu m+o(m)}.
- Choose a block length W=2^{beta m}. For every block boundary qW, hardwire the complete configuration of G_m at that time into a nonuniform circuit for length m.
- On input x in {0,1}^m, compute the block number q=floor(x/W), select the hardwired boundary configuration by a multiplexer, and simulate G_m from that configuration for at most W outputs until offset x-qW is reached.
- The checkpoint table contributes 2^{(1-beta+sigma)m+o(m)} gates; the within-window simulation contributes 2^{(beta+nu)m+o(m)} gates; selector overhead is lower order.
- Thus CC(T_m)<=2^{max(1-beta+sigma,beta+nu)m+o(m)} for every beta, and optimizing beta gives theta_chk(sigma,nu).
- Therefore a claimed anti-ball source with CC(T_m)>2^{theta m} is inconsistent whenever theta>theta_chk(sigma,nu).

Blocking gap: The derivation is an upper-bound falsifier, not a construction of a hard row. It assumes the generator has standard reproducible configurations; a proposed formalism with nonstandard proof objects must expose an equivalent configuration ledger before the cap is applied.

## Falsifiers

- falsifier: polynomial-space near-linear row/proof generation with claimed theta>1/2 gives a checkpoint circuit upper bound of size 2^{m/2+o(m)}.
- falsifier: any declared checkpoint profile with inf_beta max{1-beta+sigma,beta+nu}<theta contradicts MCSP no-side soundness for the emitted row.
- falsifier: a compressed proof skeleton plus subthreshold indexed opening remains invalid; the new checkpoint test also catches restartable streams without explicit point openings.
- falsifier: nonuniform hard-row choice without E-canonical distinct-image unranking does not transfer to an E language lower bound.
- falsifier: dense poly(N)-decidable projection of the carrier that excludes small circuits would become a useful natural property, so density repairs must be quarantined.

## Learning

Cycle 66 adds a time-space checkpoint cap to the generated anti-ball route. Avoiding indexed openings is not sufficient: a deterministic row/proof generator with small configurations and low per-output overhead gives nonuniform circuits for its own rows by hardwiring periodic configurations. The exact falsifier is theta>inf_beta max{1-beta+sigma,beta+nu}; in particular polynomial-space near-linear generated sources cannot certify MCSP hardness above 2^{m/2+o(m)}. The prior carrier-to-E transfer remains valid only after this cap audit.

## Gedanken Experiment Design Seed

- Need decision: `design now as a falsifier probe`
- Rationale: The live route risk is not another abstract barrier but whether a concrete generated anti-ball source can avoid small circuits induced by its own computation history.
- Situation seed: Consider a padded GapMCSP source family where G_m emits one candidate truth table T_m and a long symbolic anti-ball proof in lexicographic order; T_m is then multiplexed through D=0 and kappa=1 into an E target language.
- Varied variable: The varied variable is the checkpoint window exponent beta, with secondary profiles sigma for configuration size and nu for per-output overhead held as declared generator parameters.
- Held-fixed controls: Unrestricted nonuniform circuit size is the MCSP hardness measure., The generator is deterministic, advice-free, and E-time with constant exponent., The target extraction keeps D=0, kappa=1, and threshold theta fixed., No indexed row opener of exponent below theta is allowed.
- Expected observation: For polynomial-space near-linear G_m, beta=1/2 yields circuits of size 2^{m/2+o(m)}, so any claimed theta>1/2 source is immediately invalid; increasing space or per-output overhead moves the cap upward but may shrink or endanger E-target preservation.
- Transfer certificate needed: A formal checkpoint-to-circuit simulation for the exact generator model plus the existing E-canonical unranking and kappa-padding certificate before the observation may affect proof obligations.

## Next Experiment

Instantiate the checkpoint cap for three generator models: polynomial-space near-linear emitters, exponential-space emitters with sigma=theta/2, and high-overhead emitters with nu close to theta; compute which models still permit a positive extraction exponent delta<theta/(kappa(1+D)).
