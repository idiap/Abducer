# cycle-0009

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: subpolynomial-interface demagnification

## Candidate Lemma

For a carrier K_N decided by a near-linear circuit reduction making Q(N) SAT queries of length L(N)=N^{o(1)}, an N^{1+epsilon} lower bound in the same nonuniform SIZE model is not a weak magnification source. Read contrapositively, it already implies a superpolynomial lower bound for SAT at the query length. The bridge is valid as a target transfer but fails as a same-model weak-source route.

## Definitions

- source object: an explicit Boolean family K_N on N input bits with a DLOGTIME-uniform reduction circuit R_N of size s_R(N), making Q(N) oracle calls to SAT instances of length at most L(N).
- target object: SAT restricted to encodings of length at most L(N), measured in nonuniform SIZE; if lower bounds hold for unbounded L(N), the target consequence is SAT notin P/poly, hence NP not subset P/poly.
- controlled interface: substitute a size-T circuit for each SAT query in R_N, preserving query count Q(N), reduction overhead s_R(N), and postprocessing fan-in without hidden advice.
- target-preserving condition: the reduction family is uniform or explicitly constructible, L(N)=N^{o(1)}, s_R(N)<N^{1+epsilon}, Q(N)<N^{1+epsilon}, and the same SIZE model is used on source and target.

## Assumptions

- Circuit model is nonuniform Boolean SIZE with ordinary closure under composition.
- All query strings have length at most L(N), and the SAT circuit substituted is a single circuit family correct on all valid encodings up to that length.
- Q(N)>=1 and L(N) is unbounded on infinitely many N when deriving a P/poly separation consequence.
- The source lower bound is against the same general circuit model, not a weaker class such as AC0 or bounded-depth formulas.

## Equations

- upper_transfer: `C_{\mathrm{SIZE}}(K_N) \le s_R(N)+Q(N)\,C_{\mathrm{SIZE}}(\mathrm{SAT}_{\le L(N)})+O(Q(N)L(N))`. Valid when: Applies when every oracle answer is replaced by a target SAT circuit and the reduction overhead is counted explicitly.
- contrapositive_demagnification: `C_{\mathrm{SIZE}}(K_N)>N^{1+\epsilon} \Rightarrow C_{\mathrm{SIZE}}(\mathrm{SAT}_{\le L(N)})>\frac{N^{1+\epsilon}-s_R(N)-O(Q(N)L(N))}{Q(N)}`. Valid when: Valid when the source lower bound exceeds the complete substituted reduction size threshold in the same circuit model.
- subpoly_query_consequence: `L(N)=N^{o(1)},\ Q(N)\le N^q,\ s_R(N)\le N^a,\ a,q<1+\epsilon \Rightarrow C_{\mathrm{SIZE}}(\mathrm{SAT}_{\le L(N)})\ge N^{1+\epsilon-q-o(1)}=L(N)^{\omega(1)}`. Valid when: Requires the subpolynomial query-length regime and polynomially bounded query count below the claimed source threshold.
- lookup_falsifier_bound: `C_{\mathrm{SIZE}}(K_N)\le s_R(N)+O(Q(N)L(N)2^{L(N)})`. Valid when: Valid when the source model is unrestricted nonuniform circuits and lookup tables may encode SAT truth tables.

## Attempted Derivation

- Start from the repaired cycle-8 interface: reduction overhead exponent a, query-count exponent q, and SAT query length L(N)=N^{o(1)} with max(a,q)<1+epsilon.
- Inline a hypothetical size-L^c SAT circuit into every SAT oracle gate of the carrier reduction, obtaining C(K_N)<=s_R(N)+Q(N)L(N)^c+O(Q(N)L(N)).
- Observe that this proves the valid target transfer: an eventual N^{1+epsilon} lower bound for K_N excludes every fixed c because L(N)^c=N^{o(1)}.
- Read the same inequality contrapositively: the source lower bound implies C(SAT_{<=L(N)})>(N^{1+epsilon}-s_R-O(QL))/Q.
- For Q<=N^q with q<1+epsilon and L=N^{o(1)}, the induced SAT lower bound is N^{1+epsilon-q-o(1)}=L^{omega(1)}, already superpolynomial at the target query length.
- Add the unconditional lookup upper bound C(K_N)<=s_R+O(QL2^L), yielding a lower-edge falsifier L >= (1+epsilon-q-o(1))log_2 N for any possible N^{1+epsilon} source lower bound.

Blocking gap: The branch has no concrete carrier that is simultaneously a weak same-model source lower bound and target-preserving. Same-model sources demagnify; restricted sources need an unproved substitution-closure theorem.

## Falsifiers

- same-model demagnification falsifier: an N^{1+epsilon} lower bound for K_N entails SAT_{<=L(N)} lower bounds of size L(N)^{omega(1)}, so the source is not barely nontrivial relative to the target.
- lookup-table falsifier: if Q(N)L(N)2^{L(N)}=o(N^{1+epsilon}) after reduction overhead, unrestricted nonuniform circuits decide K_N below the claimed threshold.
- model-mismatch falsifier: replacing the source model by AC0, formulas, or another restricted class invalidates the transfer unless a quantitative substitution-closure lemma Phi_M is proved.
- nonuniform leakage falsifier: if R_N or the compressor is chosen with advice encoding a hard truth table, the carrier lower bound is not target-preserving.
- relativizing-interface falsifier: a proof using only black-box oracle substitution remains within a relativizing interface and cannot by itself overcome the known oracle barrier for the main P vs NP conjecture.

## Learning

Cycle 9 converts the cycle-8 repair into a route failure certificate. Subpolynomial SAT queries remove the c-dependent upper-bound term, but the same transfer read backward says that proving the source N^{1+epsilon} lower bound in general SIZE already proves SAT_{<=L} has L^{omega(1)} circuits lower bounds. The remaining valid work is not carrier search inside this black-box same-model interface; it is either a restricted-model closure theorem or a nonblackbox carrier.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Pivot to a nonblackbox object: test a proof-complexity or derandomization carrier where SAT in P/poly yields the required source upper bound through a named nonrelativizing theorem rather than through black-box SAT-query substitution.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

If an NP source language L on length N has a nonuniform lower bound L_N notin SIZE(N^k) and reduces to SAT by a length-N^lambda, circuit-N^rho many-one map, then SAT_m notin SIZE(m^d) only for exponents with max{rho,lambda d}<k. Thus a fixed barely-nontrivial source lower bound transfers only to a fixed eroded SAT lower bound, not to P != NP.

## Definitions

- source object: L_N in NP, instantiated by MCSP_s on input length N with threshold s<=N^beta and a claimed lower bound L_N notin SIZE(N^k).
- target object: SAT_m as the NP-complete target language, measured against nonuniform Boolean circuits of size m^d.
- controlled interface: a uniform many-one reduction R_N from L_N to SAT with output length m(N)<=N^lambda polylog N and nonuniform circuit complexity |R_N|<=N^rho polylog N.
- target-preserving condition: max{rho,lambda d}<k, so a target circuit for SAT composes with R_N without exceeding the forbidden source size.

## Assumptions

- The source lower bound is worst-case and nonuniform on infinitely many or all relevant lengths, matching the target quantifier.
- The reduction is length-regular enough that SAT circuits for lengths up to m(N) can be selected without advice depending on the input x.
- Polylogarithmic factors are absorbed by a positive exponent slack eta>0.
- No claim is made that the source lower-bound proof itself avoids relativization, natural proofs, or algebrization.

## Equations

- composition_bound: `\operatorname{size}(C_{m(N)}\circ R_N) \le O(N^{\rho}\operatorname{polylog}N)+O(m(N)^d) \le N^{\max\{\rho,\lambda d\}+o(1)}.`. Valid when: Valid when the reduction is length-regular and compilable into nonuniform circuits with the stated exponent bounds.
- transfer_threshold: `\text{SAT}\notin \operatorname{SIZE}(m^d)\quad\text{for every }d\text{ with }\exists\eta>0:\rho\le k-\eta\text{ and }\lambda d\le k-\eta.`. Valid when: Valid when the source lower bound excludes N^k-size circuits with enough slack to absorb lower-order factors.
- mcsp_cook_parameters: `T_{\mathrm{MCSP}}(N,s)=\widetilde O(Ns),\quad m(N)=\widetilde O(Ns),\quad s=N^\beta\Rightarrow \lambda=\rho=1+\beta+o(1).`. Valid when: Applies when MCSP verification enumerates all truth-table positions and Cook-Levin is near-linear up to logarithmic factors.
- mcsp_to_sat_exponent: `\mathrm{MCSP}_{N^\beta}\notin \operatorname{SIZE}(N^k)\Rightarrow \mathrm{SAT}\notin \operatorname{SIZE}(m^d)\text{ only for }d<k/(1+\beta)-o(1).`. Valid when: Requires the MCSP verifier size and output length to dominate no more than N to the one plus beta.

## Attempted Derivation

- Instantiate L with MCSP_s on truth-table length N and threshold s=N^beta; MCSP_s is in NP via guessing an s-size circuit and checking all N truth-table positions.
- Compile the verifier and Cook-Levin reduction to get m(N)=~O(Ns)=N^{1+beta+o(1)} and reduction circuits of comparable size.
- Assume a source lower bound MCSP_s notin SIZE(N^k). If SAT has m^d-size circuits, composition gives MCSP_s circuits of size N^{max{1+beta,(1+beta)d}+o(1)}.
- Contradiction occurs only when k>max{1+beta,(1+beta)d}. For d>=1 this is d<k/(1+beta)-o(1).
- For s=polylog N and k=1+epsilon, the valid conclusion is only SAT notin SIZE(m^{1+epsilon-o(1)}). This is not P != NP and not SAT notin P/poly.

Blocking gap: The route needs lower bound exponents k exceeding (1+beta)d for every desired SAT exponent d, but a fixed barely-nontrivial MCSP lower bound supplies only one eroded exponent window.

## Falsifiers

- Concrete falsifier: MCSP_s notin SIZE(N^1.1) together with SAT in SIZE(m^2) violates no displayed inequality when lambda is about 1.
- Concrete falsifier: if the Cook-Levin or verifier interface has lambda>=k, no nontrivial d>=1 SAT lower bound transfers.
- Concrete falsifier: if the source lower bound is only average-case with advantage N^{-a}, the worst-case SAT lower bound is invalid without a separate worst-case-to-average-case bridge.
- Concrete falsifier: if the MCSP lower-bound proof is poly(N)-constructive, large, and useful against SIZE(N^k), the natural-proof audit from cycle 1 applies under standard PRF assumptions.
- Concrete falsifier: a fully relativizing proof of the unbounded source lower-bound family would be incompatible with oracle collapses where P^O=NP^O.

## Learning

Cycle 9 turns weak-source-to-SAT enthusiasm into an explicit exponent accounting lemma. A lower bound N^k for MCSP_s with s=N^beta transfers through Cook-Levin only to SAT exponents d<k/(1+beta)-o(1). This is valid route-level progress and a falsifier for claims that one barely-superlinear source lower bound by itself implies P != NP.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Instantiate the same audit for MKtP and time-bounded Kolmogorov carriers: compute verifier time, Cook-Levin length lambda, and decide whether any known magnification theorem genuinely supplies unbounded exponents rather than a fixed eroded SAT lower bound.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

A certificate verifier over externally supplied truth tables is not enough. If the source is a uniform certificate-expander pair (G,V) whose accepted O(m)-bit certificates generate truth tables of MCSP greater than 2^{epsilon m} on kappa-dense source lengths, then exhaustive uniform search defines a language in E with all-length circuit lower bound 2^{delta n} for every fixed delta<epsilon/kappa. This is a valid route bridge, not a proof of P != NP.

## Definitions

- source object: uniform certificate-expander pair (G,V) with |pi|<=c m, G(m,pi,i) outputting the i-th bit of an m-input truth table in 2^{q m} time, V(m,pi) running in 2^{d m} time, and soundness V(m,pi)=1 implies MCSP(tt(G_{m,pi}))>2^{epsilon m}.
- target object: deterministic E language L_{G,V} whose n-bit slice pads the latest accepted source length m<=n and has Boolean circuit complexity at least 2^{delta n} for each fixed delta<epsilon/kappa.
- controlled interface: choose the lexicographically first accepted pi_m by exhaustive uniform search, set m=M(n) to the largest accepted source length at most n, and compute L(x)=G(m,pi_m,prefix_m(x)) without advice.
- target-preserving condition: accepted source lengths are kappa-dense, V is sound at threshold 2^{epsilon m}, G and V have 2^{O(m)} uniform algorithms, and no nonuniform selector chooses pi_m.

## Assumptions

- Constants epsilon>0, kappa>=1, c,d,q<infinity are fixed independently of m.
- For every sufficiently large n there is an accepted source length m in [n/kappa-O(1), n].
- Circuit size C_m(f) is measured for m-input Boolean circuits with a fixed finite gate basis.
- The verifier's soundness is semantic: every accepted generated table is outside circuits of size 2^{epsilon m}.

## Equations

- source truth-table length: `N_m=2^m`. Valid when: Valid when the MCSP object is the full truth table of an m-bit Boolean function.
- canonical accepted length: `M(n)=\max\{m\le n:\exists \pi\in\{0,1\}^{\le c m}\; V(m,\pi)=1\}`. Valid when: Applies after accepted source lengths are uniformly searchable and kappa-dense below every large n.
- canonical slice: `L(x)=G(M(|x|),\pi_{M(|x|)},x_1\ldots x_{M(|x|)})`. Valid when: Valid when pi_m is the lexicographically first accepted certificate found by uniform exhaustive search.
- E-time search bound: `T_L(n)\le \sum_{m\le n}2^{c m}\,2^{d m}+2^{q n}=2^{O(n)}`. Valid when: Requires certificate length O(m) and verifier and generator running times bounded by 2^{O(m)}.
- source soundness threshold: `V(m,\pi_m)=1\Rightarrow C_m(G_{m,\pi_m})>2^{\epsilon m}`. Valid when: Requires the verifier soundness to certify high MCSP for the generated table, not for an external witness.
- all-length transfer: `C_n(L_n)\ge C_{M(n)}(G_{M(n),\pi_{M(n)}})>2^{\epsilon M(n)}\ge 2^{\delta n}\quad(\delta<\epsilon/\kappa)`. Valid when: Applies after padding from the latest accepted source length preserves circuits by fixing unused inputs.

## Attempted Derivation

- Start with the previous certificate bridge and separate two notions: external verification V(T,pi) versus generated verification V(m,pi) for T=tt(G_{m,pi}).
- For the generated model, enumerate all O(m)-bit pi and all m<=n to find the largest accepted source length M(n) and its lexicographically first certificate pi_M.
- Define L on length n by padding down to the accepted hard slice: L(x)=G(M(n),pi_M,prefix_M(x)). The search and evaluation cost 2^{O(n)}, so L is in E.
- If a size s circuit computes L_n, then fixing the last n-M(n) inputs gives a size s circuit for G_{M,pi_M}. Soundness gives s>2^{epsilon M(n)}.
- Kappa-density gives M(n)>=n/kappa-O(1), hence for every fixed delta<epsilon/kappa and all large n, C_n(L_n)>2^{delta n}.
- For the external model without G, the search over T ranges over 2^{2^m} truth tables and cannot be performed in E; thus the old formulation had a witness-location gap.

Blocking gap: The bridge is now valid only after adding a uniform expander/selector. The unsolved gap is constructing such a sparse sound certificate-expander without already proving the desired circuit lower bound by another route.

## Falsifiers

- falsifier: certificates verify an externally supplied truth table T but provide no uniform expander G or E-time selector for T.
- falsifier: accepted source lengths have unbounded multiplicative gaps, yielding only infinitely-often lower bounds or exponent collapse.
- falsifier: the certificate selector pi_m is advice or depends on nonuniform choices, so the target consequence becomes nonuniform leakage rather than an E language.
- falsifier: the accepted external truth-table property has inverse-polynomial density, making it a natural property and triggering the PRF obstruction.
- falsifier: soundness is checked by enumerating all circuits of size 2^{epsilon m}, which costs 2^{Omega(m2^{epsilon m})} and is not valid for the 2^{O(m)} source budget.

## Learning

Cycle 9 finds a hidden witness-location gap. The valid bridge needs a uniform certificate-expander, not merely short certificates for externally supplied truth tables. With this repair, the transfer to E lower bounds is clean: threshold 2^{epsilon m} on kappa-dense source lengths gives exponent delta<epsilon/kappa. Dense external repairs are natural-proof falsifiers; brute-force soundness has a quantitative threshold collapse.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Formalize candidate sparse expander sources: a seed pi of length O(m) generates one of at most 2^{O(m)} truth tables, V checks a nontrivial proof of MCSP>N^epsilon in 2^{O(m)}, and the acceptance set is kappa-dense. First audit each candidate against three tests: no external-T witness-location gap, no inverse-polynomial largeness, and no hidden 2^{Omega(m2^{epsilon m})} circuit enumeration.
