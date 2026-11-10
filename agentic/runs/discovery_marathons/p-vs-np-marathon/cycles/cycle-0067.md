# cycle-0067

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Restriction-naturalization gate for the beta=0 XOR carrier: if a proof-mediated source lower bound factors through a label predicate Q_N on the generated formula universe U_N that is source-sound, constructive, large, and accepts the SAT labels, then Q_N extends with no density loss to a standard natural property useful against SIZE(L^c) for SAT_L. Thus this proof shape is not a valid barrier escape, although the beta=0 target bridge remains valid.

## Definitions

- source object: H_N:{0,1}^N -> {0,1}, H_N(x)=bigoplus_{j<=N^q} SAT(phi_{N,j}(x)), with each query length L=(log N)^d and generator/combiner overhead N^{rho+o(1)}.
- target object: SAT_L as a Boolean function on L-bit encodings, lower bounded against nonuniform SIZE(L^c) for every fixed c on the valid length subsequence.
- controlled interface: beta=0 substitution of a hypothetical SAT_L circuit into all generated XOR queries, plus the incidence map A_N from labels on U_N to source truth tables.
- target-preserving condition: L=(log N)^d with d>1, q,rho<1+epsilon, U_N uniformly enumerable in poly(2^L), Q_N decidable in poly(2^L), and Q_N source-sound in the same nonuniform circuit model.

## Assumptions

- Nonuniform Boolean circuit size is used for both C(H_N) and SIZE(L^c); no extra advice is allowed beyond the fixed generated family.
- U_N is the parity-quotiented set of all query strings phi_{N,j}(x) that appear in the carrier, and y^{SAT}_{U_N} denotes SAT_L restricted to U_N.
- Source soundness means y in Q_N implies C(A_N y)>N^{1+epsilon} in the unrestricted source circuit model, not merely in a restricted proof model.
- Q_N accepts y^{SAT}_{U_N}; density delta_N is measured under the uniform distribution on all labelings of U_N.
- The natural-proofs obstruction is conditional and route-level: under the usual RR-style PRF hypothesis, large constructive useful properties against the target class are not expected to exist.

## Equations

- carrier-linearization: `H_y(x)=\bigoplus_{j\le N^q} y(\phi_{N,j}(x))=(A_N y)(x),\quad H_N=A_N y^{SAT}_{U_N}`. Valid when: Valid when U_N contains every generated query string and duplicate queries are quotient-counted modulo parity.
- beta-zero-transfer: `C(A_N y_D) \le N^{\rho+o(1)}+N^q L^c\,poly(L)=N^{\max\{\rho,q\}+o(1)}`. Valid when: Valid when D is a SIZE(L^c) target circuit, L=(log N)^d, and substitution uses no advice except the fixed generator.
- restriction-density: `\Pr_{F:{0,1}^L\to\{0,1\}}[F|_{U_N}\in Q_N]=|Q_N|/2^{|U_N|}=\delta_N`. Valid when: Valid when full target truth tables are sampled uniformly and U_N is fixed independently of the sampled labels.
- naturalization-gate: `\delta_N\ge 2^{-O(L)},\ T_Q\le 2^{O(L)},\ Q_N\Rightarrow C(A_N y)>N^{1+\epsilon}\ \Longrightarrow\ \widehat Q_N\text{ is constructive and }c\text{-useful}`. Valid when: Valid when source soundness is in the same nonuniform circuit model as the beta-zero transfer.
- magnification-consequence: `C(H_N)>N^{1+\epsilon}\ \wedge\ \max\{\rho,q\}<1+\epsilon\ \Longrightarrow\ SAT_L\notin SIZE(L^c)`. Valid when: Applies after the carrier lower bound holds on the chosen valid lengths and L^c=N^{o(1)} for fixed c.

## Attempted Derivation

- Fix the beta=0 XOR carrier with L=(log N)^d, d>1, N^q generated queries, and overhead N^{rho+o(1)}.
- For any target circuit D of size L^c, substitute D into the generator and XOR combiner to obtain C(A_N y_D)<=N^{max{rho,q}+o(1)}.
- If C(H_N)>N^{1+epsilon} and max{rho,q}<1+epsilon, then no such D computes SAT_L on the valid lengths; this is the route-level target bridge, not P != NP.
- Assume the proposed source proof is mediated by Q_N over labels on U_N, with Q_N(y^{SAT})=1 and Q_N(y)=>C(A_Ny)>N^{1+epsilon}.
- Define the full-target property widehat Q_N(F)=1 iff F restricted to U_N lies in Q_N.
- Uniform random full truth tables restrict to uniform labels on U_N, so density(widehat Q_N)=density(Q_N) with no loss.
- Source soundness plus the beta=0 transfer makes widehat Q_N reject every SIZE(L^c) target circuit, while accepting SAT_L.
- Hence a large constructive Q_N naturalizes; the surviving proof-mediated route must be nonlarge, nonconstructive, not label-factorized, or explicitly nonrelativizing and direct.

Blocking gap: No lower bound for C(H_N) is proved. The derivation only certifies that one dense constructive label-mediated proof shape would collide with natural-proofs methodology, while image-relative and nonlarge certificates remain open.

## Falsifiers

- positive beta falsifier: if target query length is N^beta with beta>0, the transfer N^{q+beta c+o(1)} cannot exclude all polynomial SAT exponents.
- low constructive incidence rank falsifier: a small row-coordinate transcript lets the XOR carrier hardwire basis parities and stay below N^{1+epsilon}.
- label-free codebook falsifier: a compact quotient transcript plus sparse corrections gives C(H_N)<=S_T+S_D+tildeO(U_N+A_N r_N)+E_NN.
- dense constructive label predicate falsifier for barrier-escape claims: if Q_N is large, constructive, and source-sound, restriction extension makes it a natural property.
- image-only density falsifier: largeness of P_N in the full source truth-table cube is irrelevant unless P_N is large on im(A_N).
- nonuniform leakage falsifier: if U_N or Q_N needs hidden advice not charged in poly(2^L), constructivity and target preservation fail.

## Learning

Cycle 67 upgrades the previous label-realization warning into an exact restriction-extension theorem. For beta=0 XOR carriers, dense constructive label-mediated source lower bounds naturalize automatically when U_N is uniformly enumerable and soundness is in the same circuit model. The valid bridge survives, but any proof-mediated route must now be direct, nonlarge, nonconstructive, or explicitly nonrelativizing; ambient source-property largeness is not enough because density must be image-relative.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the proof-mediated beta=0 XOR route.`
- Rationale: The current bottleneck is not the substitution theorem but whether a proposed source certificate naturalizes. Varying label density tests exactly when the certificate is a valid barrier escape.
- Situation seed: Take an XOR carrier with L=(log N)^2, q and rho below 1+epsilon, universe U_N equal to the uniformly enumerable generated query set, and a candidate label predicate Q_N that accepts SAT_L restricted to U_N and is source-sound for A_Ny.
- Varied variable: The label-density exponent lambda in delta_N=2^{-L^lambda}.
- Held-fixed controls: beta=0 and L=(log N)^2 so every fixed SIZE(L^c) substitution costs only N^{o(1)} per query., q,rho<1+epsilon so the target bridge threshold remains below the assumed source lower bound., Q_N is required to reject all small target-circuit restrictions via source soundness and the same circuit model., U_N is uniformly enumerable in poly(2^L) and no uncharged advice is permitted.
- Expected observation: For lambda<=1, Q_N becomes a constructive large useful property and the barrier-escape claim is falsified. For lambda>1, naturalness no longer blocks the route, but the proof must explain how such a nonlarge certificate is found and verified.
- Transfer certificate needed: A formal restriction-extension certificate: enumerate U_N in poly(2^L), decide Q_N in poly(2^L), prove source soundness for all labels, and measure density over uniform labels on U_N rather than only over the carrier image.

## Next Experiment

Instantiate U_N for one explicit polylog-query XOR generator, compute whether U_N is enumerable in poly(2^L), and classify a candidate certificate as dense-label, image-relative, or nonlarge.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Zero-seed view-soundness naturalizes local proof-mediated lower-bound certificates: for N=2^m, if a uniform verifier V has r,q_f,q_pi=O(log N), SAT completeness on at least one seed, and every SIZE_m(m^k) truth table has projected view-acceptance probability <2^{-r}, then P_m^V={f: some seed and local proof-answer view makes V accept f} is a poly(N)-constructive N^{-O(1)}-large property useful against SIZE_m(m^k).

## Definitions

- source object: a uniform local verifier V_m for a proof-mediated claim CC(TT(SAT_m))>m^k, with oracle access to an N-bit truth table f and a proof string pi.
- target object: the nonuniform Boolean circuit class SIZE_m(m^k) over m input bits, represented by its N-bit truth tables.
- controlled interface: the projected local view predicate ViewAcc_V(f,rho), meaning that some assignment to the proof answers queried along seed rho makes V accept f.
- target-preserving condition: view-soundness after existential proof projection, namely every f in SIZE_m(m^k) has Pr_rho[ViewAcc_V(f,rho)=1]<2^{-r(m)}, while TT(SAT_m) has an accepting proof on at least one seed.
- observable: the existential-seed property P_m^V obtained by enumerating all random seeds and local proof-answer transcripts.
- naturalness regime: constructivity is measured in deterministic poly(N) time on the full truth table input, with no nonuniform seed advice.

## Assumptions

- Truth tables have length N=2^m; circuits use a fixed finite basis and size threshold s=m^k for fixed k>1.
- The verifier's transition function and queried addresses are computable in poly(N) time, and r(m)+q_f(m)+q_pi(m)=O(log N).
- View-soundness is stronger than ordinary per-proof soundness: the existential local proof view is already projected before measuring acceptance probability.
- Completeness gives a proof pi* and a seed rho* on which V accepts TT(SAT_m); constant completeness is more than needed.
- The property is uniform because it enumerates all seeds rather than hardwiring a good seed; this avoids the nonuniform seed-advice escape.

## Equations

- view_property: `\mathcal{P}_m^V=\{f\in\{0,1\}^N:\exists \rho\in\{0,1\}^{r(m)}\; \mathrm{ViewAcc}_V(f,\rho)=1\}`. Valid when: Valid when ViewAcc is the projected local-view predicate and all seeds are enumerable within the full truth-table input length.
- density_from_accepting_view: `\mu(\mathcal{P}_m^V)\ge 2^{-q_f(m)}`. Valid when: Valid when a complete accepting execution on TT(SAT_m) queries at most q_f table positions and the same transcript defines a cylinder.
- constructivity_time: `T_{\mathrm{decide}}(N)\le 2^{r(m)+O(q_f(m)+q_\pi(m))}\,\mathrm{poly}(N)`. Valid when: Valid when verifier addresses are polynomial-time computable and all adaptive local table and proof-answer transcripts are explicitly enumerated.
- zero_seed_usefulness: `\Pr_{\rho}[\mathrm{ViewAcc}_V(f,\rho)=1]<2^{-r(m)}\Rightarrow f\notin\mathcal{P}_m^V`. Valid when: Valid when the seed space has exactly 2^{r(m)} points, so one accepting seed would contribute probability at least 2^{-r(m)}.
- natural_threshold: `r(m)+q_f(m)+q_\pi(m)\le c\log N\Rightarrow T_{\mathrm{decide}}=N^{O(1)}\text{ and }\mu(\mathcal{P}_m^V)\ge N^{-c'}`. Valid when: Valid when the verifier remains uniform and the density bound comes from the SAT accepting cylinder rather than from random proof averaging.

## Attempted Derivation

- Fix m, N=2^m, and a uniform verifier V with seed length r and local query bounds q_f,q_pi.
- Define ViewAcc_V(f,rho) by existentially quantifying only the proof answers seen by the local computation on seed rho.
- Let P_m^V be the property that some seed has ViewAcc=1; decide it by enumerating all seeds and all local answer transcripts.
- If f is in SIZE_m(m^k) and f lies in P_m^V, then one accepting seed exists, giving projected acceptance probability at least 2^{-r}; this contradicts zero-seed view-soundness.
- If TT(SAT_m) has one accepting seed, the accepting path fixes at most q_f truth-table coordinates; every table matching those coordinates is also accepted by the same projected view, so density is at least 2^{-q_f}.
- When r+q_f+q_pi=O(log N), the enumeration is poly(N) and the density is inverse-polynomial, yielding a valid natural property useful against the named target class.
- Under exact-target PRF assumptions, the property distinguishes random truth tables from PRF truth tables with inverse-polynomial advantage.

Blocking gap: The missing hard object is a verifier with projected view-soundness below 2^{-r}; standard proof-system soundness is per global proof and leaks through 2^P possible proofs.

## Falsifiers

- A falsifier for usefulness is one SIZE_m(m^k) truth table with a single accepting seed and local proof-answer view.
- A verifier with proof length P=N and ordinary soundness delta=N^{-100} falsifies any transfer that ignores proof projection leakage.
- If q_f=omega(log N), the accepting cylinder may have superpolynomially small density and the natural-proof conclusion is not valid.
- If r+q_pi=omega(log N), exhaustive seed/transcript enumeration may lose poly(N) constructivity.
- If PRF outputs are not computable in the exact SIZE_m(m^k) target, the PRF contradiction carrier is invalid.

## Learning

Cycle 67 isolates a sharper proof-mediated gate: local proofs do not escape natural proofs when projected view-soundness is below one seed. The exact threshold is delta<2^{-r}, not a vague public-coin or proof-length slogan. Long proof length remains an escape only for ordinary per-proof soundness without projected view-soundness.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe and threshold calibration for proof-mediated naturalization.`
- Rationale: The branch has already quarantined searchable local proofs and public-coin union bounds; the remaining ambiguity is whether long proofs escape via proof length or are recaptured by projected view-soundness.
- Situation seed: A PCP-like certificate family for the claim CC(TT(SAT_m))>m^k with proof length P=N^b, seed length r=alpha log N, table queries q_f=c_f log N, proof queries q_pi=c_pi log N, and property P_m^V accepting when some seed has an accepting local proof view.
- Varied variable: The projected view-soundness exponent eta in delta=N^{-eta}, with r=alpha log N fixed.
- Held-fixed controls: Target class remains SIZE_m(m^k) on the original m-bit SAT slice., The property enumerates all seeds and transcripts; no seed advice is allowed., Completeness for TT(SAT_m) supplies at least one accepting seed., Verifier uniformity and address computation remain poly(N).
- Expected observation: If eta>alpha, then delta<2^{-r} and the existential-seed property becomes useful, large, and constructive. If eta<=alpha, an easy truth table may keep one accepting seed, so usefulness fails. Ordinary per-proof soundness with P=N^b is irrelevant unless eta exceeds alpha+P/log N.
- Transfer certificate needed: A formal projected view-soundness theorem for the named verifier, or a counterexample showing an easy circuit with one locally satisfiable accepting view.

## Next Experiment

Instantiate the gate on a named proof system for circuit lower bounds: compute r,q_f,q_pi,P and decide whether its soundness is projected view-soundness, ordinary per-proof soundness, or neither.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Let G_m be a deterministic advice-free sequential generator for a candidate MCSP anti-ball row T_m in {0,1}^{2^m}. If any restorable configuration has length at most 2^{sigma m+o(m)} bits and each emitted bit can be advanced from a configuration with circuit cost 2^{nu m+o(m)}, then T_m has unrestricted circuit size at most 2^{alpha_chk(sigma,nu)m+o(m)}. Therefore a source claim CC(T_m)>2^{theta m} is valid only when theta<=alpha_chk(sigma,nu); theta>alpha_chk is a route-level falsifier.

## Definitions

- source object: a generated anti-ball MCSP carrier row T_m emitted sequentially by an advice-free generator G_m with proof stream ignored except as state evolution.
- target object: an unrestricted Boolean circuit lower bound for the length-2^m truth table T_m, later multiplexed into an E-language lower bound.
- controlled interface: checkpoint hardwiring of generator configurations plus bounded forward simulation from the selected checkpoint to answer one truth-table bit.
- target-preserving condition: the checkpoint circuit must be nonuniform for the same row length m, use no advice beyond hardwired configurations of G_m, and stay below the claimed MCSP threshold 2^{theta m}.

## Assumptions

- Model: unrestricted nonuniform Boolean circuits with constants allowed and fan-in two; polynomial factors are absorbed into o(m) exponents.
- Regime: the generator is deterministic and has a canonical length-m run producing exactly 2^m row bits in order, or a designated row subsequence with the same checkpoint schedule.
- Uniformity/advice: G_m is advice-free, but the falsifying circuit may nonuniformly hardwire checkpoint configurations because MCSP hardness is nonuniform.
- Cutoff: configuration length exponent sigma and per-output transition exponent nu are constants independent of m.
- Same-theory condition: the source threshold theta is meant as an unrestricted circuit lower bound on each emitted MCSP no-side row, not merely a proof-complexity or uniform lower bound.
- Naturalness boundary: the lemma is a negative source-side upper-bound certificate; it does not create a large useful property.

## Equations

- checkpoint_storage_simulation_bound: `C(T_m) \le 2^{(1-\beta+\sigma)m+o(m)}+2^{(\beta+\nu)m+o(m)}`. Valid when: Valid when checkpoints are placed every 2^{beta m} emitted row bits and each checkpoint configuration is restorable by hardwiring.
- clipped_checkpoint_cap: `\alpha_{\rm chk}(\sigma,\nu)=\inf_{0\le \beta\le 1}\max\{1-\beta+\sigma,\beta+\nu\}`. Valid when: Valid when beta ranges over legal checkpoint spacings between one output and the full truth-table length.
- closed_form_cap: `\alpha_{\rm chk}=\begin{cases}\nu,&\nu\ge 1+\sigma,\\ \sigma,&\sigma\ge 1+\nu,\\ (1+\sigma+\nu)/2,&\text{otherwise.}\end{cases}`. Valid when: Applies after the convex minimization has an endpoint or equalizing interior checkpoint spacing.
- source_validity_gate: `\theta\le \alpha_{\rm chk}(\sigma,\nu)`. Valid when: Requires the claimed MCSP source hardness threshold to exceed no checkpoint-derived circuit upper bound.

## Attempted Derivation

- Fix a block length B=2^{beta m}. Hardwire the configurations of G_m at row positions 0,B,2B,...; there are 2^{(1-beta)m+o(m)} such checkpoints.
- The hardwired checkpoint table has total selectable information 2^{(1-beta+sigma)m+o(m)}; a Boolean circuit can select the predecessor checkpoint using the input index with only polynomial overhead in m and the table size.
- From the selected configuration, simulate at most B emitted-bit transitions. If each transition/output step has circuit cost 2^{nu m+o(m)}, this costs 2^{(beta+nu)m+o(m)} gates.
- The resulting circuit computes T_m(i) on input i and has exponent max{1-beta+sigma,beta+nu}+o(1).
- Optimizing over beta in [0,1] gives the clipped formula for alpha_chk. Interior equalization yields (1+sigma+nu)/2; endpoint cases occur when the equalizer lies outside the legal beta interval.
- Therefore any generated carrier claiming CC(T_m)>2^{theta m} with theta>alpha_chk is contradicted by an explicit nonuniform circuit family for the same rows.

Blocking gap: The derivation is a valid falsifier for low-profile generated sources, but it does not construct a cap-compatible anti-ball source. It also needs a formal machine-model lemma that configurations are restorable without hiding advice in the proof stream.

## Falsifiers

- carrier is not explicit
- extraction loses the needed class
- consequence is only nonuniform
- theta exceeds alpha_chk(sigma,nu), giving a checkpoint circuit for the same row
- compressed proof skeleton plus indexed opening has exponent omega<theta
- distinct-image entropy D is unbounded, collapsing delta to o(1)
- source row is generated by polynomial-space near-linear streaming while claiming theta>1/2
- hard row is selected by nonuniform advice rather than E-canonical unranking

## Learning

Cycle 67 closes the checkpoint-profile optimization. A generated row/proof carrier with configuration exponent sigma and per-output exponent nu has a nonuniform self-circuit exponent alpha_chk=inf_beta max{1-beta+sigma,beta+nu}, with clipped closed form. Polynomial-space near-linear generators are capped at 1/2, so theta>1/2 is a valid falsifier for that implementation class. The conditional E-transfer remains delta<theta/(kappa(1+D)) only when theta survives this cap.

## Gedanken Experiment Design Seed

- Need decision: `use now as a falsifier probe`
- Rationale: The live route obstruction is no longer MCSP folklore but whether a generated anti-ball proof stream can avoid nonuniform circuits for its own rows. Varying checkpoint spacing directly tests the source model against the claimed threshold.
- Situation seed: A deterministic generated anti-ball certificate family G_m emits a length-2^m truth table T_m and a long nonblackbox proof that T_m is outside every circuit ball of radius zero at threshold 2^{theta m}.
- Varied variable: checkpoint spacing exponent beta in blocks of 2^{beta m} emitted row bits.
- Held-fixed controls: source threshold theta and unrestricted circuit model, configuration exponent sigma and per-output exponent nu, bounded distinct-image entropy D and kappa-gap source lengths, advice-free canonical generation and no indexed row opener
- Expected observation: The circuit exponent follows max{1-beta+sigma,beta+nu}; the best beta either equalizes storage and replay or lands at an endpoint. If the minimum is below theta, the source is invalid before any extraction theorem is invoked.
- Transfer certificate needed: A formal checkpoint-to-circuit simulation lemma proving that hardwired configurations plus forward replay compute the same target row in unrestricted nonuniform circuits with only 2^{o(m)} overhead.

## Next Experiment

Audit a concrete nonblackbox proof generator candidate by computing its sigma, nu, D, kappa, and opener exponent omega; reject it if theta>alpha_chk or omega<theta, otherwise test whether its anti-ball soundness is non-circular.
