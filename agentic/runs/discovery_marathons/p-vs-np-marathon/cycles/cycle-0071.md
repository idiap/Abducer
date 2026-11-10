# cycle-0071

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For the beta=0 XOR carrier, any dense, 2^{O(L)}-constructive, functionally sound label-certificate source lower bound cylinder-extends to a valid classical natural property useful against L^c-size circuits. Thus this proof-mediated route is blocked unless it is nonlarge, nonconstructive, SAT-only/nonrelativizing, advice-leaking, or a direct H_N lower bound.

## Definitions

- source object: H_N^y(x)=<a_N(x),y> mod 2, where y labels the uniformly enumerable generated SAT-query set U_N subset {0,1}^L and a_N is the quotient incidence generator.
- target object: Boolean functions f:{0,1}^L->{0,1}, especially SAT_L, measured against nonuniform SIZE(L^c) circuits for every fixed c.
- controlled interface: beta=0 target substitution for the XOR carrier, with generator overhead N^rho, query-count overhead N^q, and polylog target length L=(log N)^d.
- target-preserving condition: q,rho<1+epsilon, U_N is distinct and advice-free enumerable in 2^{O(L)}, and certificate soundness is in the same nonuniform circuit model for every label vector y, not only for SAT labels.
- A_N={y in {0,1}^{U_N}: exists pi V_N(y,pi)=1}; delta_N=|A_N|/2^{|U_N|}.
- P_N(f)=1 iff f restricted to U_N lies in A_N; this is the cylinder pullback tested from the full truth table of f.

## Assumptions

- Circuit model is nonuniform Boolean SIZE with fan-in two; all constants c are fixed before N tends to infinity.
- Target length is polylogarithmic, L=(log N)^d with fixed d>1, so L^c=N^{o(1)}.
- The verifier/search relation for A_N is 2^{O(L)}-constructive and uses no advice beyond N and the uniform enumeration of U_N.
- Functional soundness: y in A_N implies C(H_N^y)>N^{1+epsilon} for arbitrary y in {0,1}^{U_N}.
- Classical largeness is measured as density at least 2^{-O(L)} among all Boolean functions on L input bits.

## Equations

- xor_carrier: `H_N^y(x)=\bigoplus_{u\in U_N} a_N(x,u)y_u`. Valid when: Valid when U_N is the distinct generated query set and a_N is the advice-free quotient incidence predicate.
- beta_zero_substitution: `C(H_N^{f|U_N}) \le N^{\max\{\rho,q\}+o(1)} \quad \text{if } C(f)\le L^c`. Valid when: Applies when target queries have length L=polylog(N) and beta=0 removes the c-dependent exponent term.
- density_pullback: `\Pr_F[P_N(F)=1]=\delta_N=|A_N|/2^{|U_N|}`. Valid when: Valid when F is a uniformly random L-bit Boolean function and U_N contains distinct query strings.
- naturalness_cutoff: `\delta_N\ge 2^{-K L},\; T_V\le 2^{K L} \Rightarrow P_N \text{ is classically large and constructive}`. Valid when: Requires the usual truth-table constructivity scale and the density cutoff measured over all L-bit functions.
- usefulness_contradiction: `P_N(f)=1 \wedge C(f)\le L^c \Rightarrow N^{1+\epsilon}<C(H_N^{f|U_N})\le N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies after functional soundness and the beta-zero transfer hold with max{rho,q}<1+epsilon.

## Attempted Derivation

- Fix f with C(f)<=L^c and set y=f|U_N.
- Substitute the f-circuit into every generated query of the XOR carrier; since L=polylog(N), the substituted target-circuit cost is N^{q+o(1)} and the generator cost is N^{rho+o(1)}.
- If y is accepted by a functionally sound certificate, then C(H_N^y)>N^{1+epsilon}.
- When max{rho,q}<1+epsilon, the previous two inequalities contradict each other, so no SIZE(L^c) function lies in the pullback property P_N.
- For uniformly random f, f|U_N is uniform on {0,1}^{U_N}; hence the pullback density equals delta_N.
- If delta_N>=2^{-O(L)} and the verifier is 2^{O(L)}-constructive, P_N is a classical natural property useful against SIZE(L^c).

Blocking gap: This derivation needs functional soundness for all label vectors and a real accepted-label density estimate. SAT-only certificates and nonlarge accepted sets are outside the no-go.

## Falsifiers

- falsifier: positive beta in a black-box target substitution revives the q+beta*c threshold cap and prevents all-exponent transfer.
- falsifier: low constructive quotient rank or a small label-free codebook gives an explicit upper bound for the XOR carrier.
- falsifier: functional soundness plus accepted-label density at least 2^{-O(L)} and 2^{O(L)} constructivity naturalizes the proof certificate.
- falsifier: nonuniform row selection or advice-dependent U_N invalidates the density pullback and the target-preserving bridge.
- falsifier: SAT-only soundness without a nonrelativizing invariant gives no natural property and no certified source lower bound.

## Learning

Cycle 71 upgrades the beta=0 XOR naturalness audit: density alone is not the decisive condition. Dense searchable certificates naturalize only when their soundness is functional over arbitrary label vectors. Therefore the surviving proof-mediated route must be sparse, nonconstructive, SAT-semantic/nonrelativizing, advice-free in a stronger sense, or a direct H_N lower bound.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch has reduced the beta=0 XOR route to certificate density and soundness type; a concrete density-threshold experiment can separate a valid naturalization no-go from a possible SAT-only escape.
- Situation seed: Take U_N to be M=N^q uniformly generated 3CNF encodings of length L=(log N)^d with d>1, define H_N^y as the XOR of SAT labels selected by a quotient incidence generator of cost N^rho, and let V_N(y,pi) claim C(H_N^y)>N^{1+epsilon}.
- Varied variable: kappa in accepted-label density delta_N=2^{-kappa L}, while keeping beta=0 fixed.
- Held-fixed controls: q,rho<1+epsilon so the target substitution bridge remains valid., U_N is distinct, advice-free, and enumerable in 2^{O(L)}., Verifier constructivity is at most 2^{O(L)}., Functional soundness is either enforced for all y or explicitly denied as SAT-only.
- Expected observation: For bounded kappa, any functionally sound certificate becomes a classical natural property; for kappa growing with N, largeness fails and the route must supply a sparse SAT-specific proof rather than a generic label certificate.
- Transfer certificate needed: A formal proof that V_N is functionally sound over all labels and that restriction to U_N is density-preserving; if functional soundness fails, a nonrelativizing SAT-semantic certificate must replace the natural-property transfer.

## Next Experiment

Instantiate V_N with one concrete proof-system or MCSP-style certificate, compute kappa_N for accepted labels, and decide whether soundness is functional over arbitrary y or essentially SAT-semantic.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Searchable row-view shadow gate: a proof-mediated local lower-bound verifier whose row advice, local proof-view transcript, and target-query union are logarithmic yields a valid natural property, provided soundness holds directly for every row advice and every local view transcript, not merely for global proofs.

## Definitions

- source object: a uniform deterministic cluster verifier V_N for LB(T): CC_m(T)>s, obtained after fixing a d-seed public-coin cluster; on each seed it makes at most q target truth-table queries and b proof-bit queries.
- target object: truth tables of m-bit Boolean functions computed by SIZE_m(s), with N=2^m and s=m^k fixed on the same length slice.
- controlled interface: row advice a of length A selects or decodes the seed cluster and query schedule; a local proof-view transcript y of length at most B supplies all proof answers seen inside the cluster.
- target-preserving condition: direct row-view soundness says no T in TT(SIZE_m(s)) has any row advice a and any locally consistent transcript y making the whole cluster accept.
- P_N={T in {0,1}^N : exists a,y such that ClusterAccept_V(T,a,y)=1}.
- h(a,y) is the number of distinct target truth-table coordinates queried along the accepting transcript; h_* is this number for one complete SAT transcript.

## Assumptions

- Uniformity model: V_N, the row-advice decoder, and cluster simulation run in poly(N) time with random access to the N-bit truth table.
- Transcript model: adaptivity is allowed, but a fixed accepting transcript determines at most qd target answers and at most B proof answers; repeated proof-cell queries must be locally consistent.
- Completeness regime: TT(SAT_m) has at least one accepting pair (a_*,y_*) for the cluster verifier.
- Soundness regime: the route proves direct row-view soundness against TT(SIZE_m(s)); ordinary global proof soundness is explicitly insufficient.
- Naturalness cutoff: h_*=O(log N) and A+B=O(log N), with constants independent of m.
- Target model: no padding or advice leakage changes the target class between SIZE_m(s) and the truth-table property.

## Equations

- target_query_union: `h(a,y) \le qd`. Valid when: Valid when the fixed row advice a determines a d-seed cluster and each seed causes at most q target truth-table queries under the uniform verifier.
- cylinder_density: `\mu(P_N) \ge 2^{-h_*}`. Valid when: Valid when completeness supplies an accepted row advice and local proof view for SAT, so agreeing on those queried target coordinates preserves acceptance.
- constructivity_time: `T_{decide}(P_N) \le 2^{A+B} d\,\mathrm{poly}(q,b,m)`. Valid when: Valid when row advice and proof-view coordinates are uniformly decodable and exhaustive enumeration over all searchable choices is allowed.
- natural_threshold: `h_* \le c\log N,\ A+B \le c'\log N \Rightarrow P_N\text{ is }N^{-c}\text{-dense and poly}(N)\text{-constructive}`. Valid when: Valid when the density and constructivity inequalities above hold and row-view soundness excludes every target-circuit truth table.
- prf_pressure: `\mathrm{Adv}_{P_N}(F) \ge \mu(P_N)`. Valid when: Valid when the PRF family lies inside the targeted circuit class and the constructive property is used as the truth-table distinguisher.

## Attempted Derivation

- Fix a cluster verifier V_N and define P_N by existentially quantifying only over searchable row advice a and the local proof-view transcript y seen by the cluster.
- Completeness for TT(SAT_m) gives one accepted pair (a_*,y_*). The same transcript accepts every table agreeing with SAT on the h_* queried target coordinates, giving density at least 2^{-h_*}.
- If A+B=O(log N), enumerate all row advice strings and local proof-view transcripts to decide P_N in poly(N) time; full proof length is irrelevant unless it enters B or the decoder.
- Direct row-view soundness implies P_N excludes every truth table of SIZE_m(s), so the property is useful against exactly the named target class.
- Under h_*=O(log N), P_N is large, constructive, and useful; therefore the route is a natural-property route and faces the PRF falsifier for SIZE_m(s).

Blocking gap: The missing theorem is direct row-view soundness or a consistency extractor. Ordinary soundness against global proofs leaves alpha_C(T) uncontrolled and is invalid for usefulness.

## Falsifiers

- 3-XOR local satisfiability falsifier: every logarithmic cluster can have a locally satisfying proof view although no global assignment satisfies many constraints.
- Nonuniform row-selection leakage: the accepting cluster is specified by superlogarithmic advice depending on TT(SAT_m), so constructivity of P_N is lost.
- High-query escape: h_*=qd=omega(log N) makes the accepting cylinder exponentially too small for a natural-property contradiction.
- Weak-soundness escape: ordinary max_pi soundness allows alpha_C(T)=1 for small-circuit T, so usefulness of the shadow property is false.
- PRF falsifier: if the target class contains N^{-c}-secure truth-table PRFs of size m^k, any large constructive useful P_N with density N^{-c} is cryptographically invalid.

## Learning

Cycle 71 isolates the row-view shadow gate: long proofs and row selection do not escape natural proofs when the actual searched shadow has logarithmic target-query union and logarithmic row/proof-view enumeration. The valid escape must be nonlarge, nonconstructive, or backed by a direct consistency theorem; ordinary soundness has a 3-XOR-style falsifier. This is route-level progress only, not progress on P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch needs a concrete row-selection leakage test to distinguish a genuine proof-mediated escape from another searchable natural property.
- Situation seed: A padded-SAT lower-bound proof verifier for the claim CC(TT(SAT_m))>m^k uses q=2 target-table queries and b=O(1) proof-bit queries per seed; a cluster of d=c log N seeds is checked, and row advice a selects the cluster.
- Varied variable: row advice length A, while B=bd and h=qd are monitored as induced transcript budgets.
- Held-fixed controls: Target class is SIZE_m(m^k) on the unpadded m-bit truth-table slice N=2^m., The verifier and row decoder are uniform and enumerable in poly(N) time., Completeness for TT(SAT_m) is held fixed for one accepted cluster transcript., Direct row-view soundness is required for every small-circuit truth table, every row advice, and every local proof-view transcript.
- Expected observation: For A+B=O(log N) and h=O(log N), the verifier induces an N^{-O(1)}-dense poly(N)-constructive useful property; increasing A beyond logarithmic is the first possible constructivity escape, but it becomes a nonuniform leakage obligation rather than a proof of hardness.
- Transfer certificate needed: A formal cluster-soundness or K-consistency extractor proving that accepted local row views for any target-circuit truth table cannot exist, plus a uniform cluster decoder with all advice length counted.

## Next Experiment

Instantiate the gate on a toy PCP/IOP lower-bound verifier: compute h, A, B for d=c log N clusters and test whether any known consistency check proves direct row-view soundness rather than only ordinary soundness.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Semantic-cover dimension is an exact normal form for unrestricted MCSP row hardness up to o(1) in the exponent. If a generated carrier row T has a semantic cover of exponent alpha<theta, this is a valid falsifier for the claimed MCSP no-side threshold 2^{theta m}; conversely, proving semantic-cover dimension above theta already implies the needed unrestricted row lower bound.

## Definitions

- source object: An advice-free generated anti-ball MCSP carrier G_m whose accepted image contains at most 2^{D m+o(m)} distinct truth-table rows T in {0,1}^{2^m} and claims row hardness above 2^{theta m}.
- target object: An E-uniform language L extracted from kappa-dense source lengths, with target consequence SIZE_L(n)>2^{delta n} against unrestricted Boolean circuits.
- controlled interface: A semantic cover is a rankable block decomposition of {0,1}^m, per-block hardwirable summaries of total volume 2^{v m+o(m)}, and a shared opener/locator circuit of size 2^{omega m+o(m)} outputting T(x).
- target-preserving condition: The extraction is valid only when generation and canonical image unranking are E-uniform and advice-free, the image entropy is D, source lengths are kappa-dense, and every accepted row has semantic-cover exponent at least theta-o(1).

## Assumptions

- MCSP hardness is measured in the unrestricted nonuniform circuit model; hardwiring summaries is allowed when deriving an upper-bound falsifier.
- The opener includes block location, summary addressing, and bit decoding; its exponent omega absorbs polynomial and polylogarithmic overheads.
- The cover family may use one block whose summary is a circuit description; hence ordinary circuits embed into the semantic-cover model.
- The E extraction uses only canonical low-D image enumeration and does not use advice, nonuniform length selection, or a hard-row oracle.

## Equations

- semantic_cover_exponent: `\mathrm{SCov}_m(T)=\inf_{\mathcal C}\max\{v(\mathcal C),\omega(\mathcal C)\}`. Valid when: Valid when semantic covers include a rankable block locator and measure total hardwirable summary volume exponentially in m.
- cover_to_circuit_upper_bound: `C(T)\le 2^{(\mathrm{SCov}_m(T)+o(1))m}`. Valid when: Valid when summaries are hardwired nonuniformly and the opener includes all addressing and block-location logic.
- circuit_to_one_block_cover: `\mathrm{SCov}_m(T)\le \frac{\log_2 C(T)}{m}+o(1)`. Valid when: Valid when the cover model permits the one-block universal-evaluation cover with the circuit description as summary.
- mcsp_gate: `C(T)>2^{\theta m}\Rightarrow \mathrm{SCov}_m(T)\ge \theta-o(1),\quad \mathrm{SCov}_m(T)<\theta-o(1)\Rightarrow \text{source falsified}`. Valid when: Valid when MCSP no-side hardness is measured against unrestricted nonuniform circuits at threshold 2^{theta m}.
- post_gate_extraction: `\delta<\frac{\theta}{\kappa(1+D)}`. Valid when: Applies after kappa-dense source lengths and D-entropy canonical unranking preserve E-uniformity without advice.

## Attempted Derivation

- Define SCov_m(T) as the minimum exponent alpha over semantic covers with total summary volume and shared opener/locator size at most 2^{alpha m+o(m)}.
- Cover-to-circuit direction: hardwire all summaries, use the rankable block locator to select the relevant summary, and run the opener; the unrestricted circuit size is 2^{max(v,omega)m+o(m)}.
- Circuit-to-cover direction: use a one-block cover whose summary is a size-s circuit for T and whose opener is a universal circuit evaluator; this gives SCov_m(T)<=log_2(s)/m+o(1).
- Thus SCov_m(T)=log_2 C(T)/m+o(1) for the route's unrestricted circuit model, assuming locator overhead is included in the opener.
- Plugging the MCSP no-side threshold C(T)>2^{theta m} into the existing low-D, kappa-dense carrier extraction gives the already valid transfer delta<theta/(kappa(1+D)), but only after the SCov gate is passed.
- Therefore semantic-cover leakage is not an auxiliary nuisance: any subthreshold cover is a finite falsifier, while a high-SCov certificate is essentially the row lower-bound certificate the route still lacks.

Blocking gap: SCov-source theorem gap: no explicit advice-free generated row/proof family is known that proves SCov_m(T)>theta on kappa-dense lengths with bounded D and without becoming a large constructive property.

## Falsifiers

- A one-block universal-circuit cover of exponent alpha<theta is an immediate falsifier for the claimed MCSP no-side row.
- Any rankable block-summary cover with total summary volume 2^{v m} and opener size 2^{omega m}, max(v,omega)<theta, invalidates the source.
- A compressed proof skeleton with an indexed row opener below theta is a nonuniform circuit upper bound, not a valid carrier.
- A dense poly(N)-decidable projection that excludes small circuits is a natural-property barrier object unless a non-natural escape is formally supplied.
- A hard-row selector using advice, nonuniform length choice, or an unsearchable proof location fails the target-preserving E extraction.

## Learning

Cycle 71 turns semantic block-cover leakage into an exponent-normal-form statement: avoiding all such covers is equivalent, up to o(1), to the unrestricted MCSP row lower bound. This sharpens the route by converting many leakage checks into one finite falsifier gate, while preserving the distinction between a valid conditional carrier transfer and an actual proof of P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design-now-as-falsifier-probe`
- Rationale: The branch now needs a concrete semantic-cover stress test because sequential and skip-hard generation alone no longer certify row hardness; the decisive issue is whether the row has any hardwirable cover below theta.
- Situation seed: Take a generated anti-ball carrier row T_m and impose a rankable partition into 2^{(1-lambda)m} intervals, each with a semantic summary of length 2^{mu m}, plus a shared opener of size 2^{omega m}.
- Varied variable: lambda, the block-length exponent, varied while optimizing the induced cover exponent alpha(lambda)=max{1-lambda+mu(lambda),omega(lambda)}.
- Held-fixed controls: The claimed MCSP threshold remains 2^{theta m} against unrestricted nonuniform circuits., The extracted language must remain E-uniform, advice-free, kappa-dense, and have distinct-image entropy D., The row/proof generator is not allowed to introduce a separate indexed opener below theta., The target consequence remains only the conditional E lower bound delta<theta/(kappa(1+D)).
- Expected observation: If some lambda gives alpha(lambda)<theta, the row has a small unrestricted circuit and the carrier is falsified. If no such lambda is found, the observation is only evidence for high semantic-cover dimension, not a proof of MCSP hardness.
- Transfer certificate needed: A formal cover-to-circuit construction including locator overhead, plus a proof that the same row family passes low-D canonical unranking and kappa-density without advice.

## Next Experiment

Instantiate SCov on three source classes: affine/LFSR streams, algebraic proof-transcript generators, and cellular-automaton sequential carriers; compute the best one-block or block-summary exponent alpha and falsify any claimed theta>alpha.
