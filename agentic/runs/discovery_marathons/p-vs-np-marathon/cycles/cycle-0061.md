# cycle-0061

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For a polylog-query XOR-SAT carrier, any constructively label-free global-codebook sparse quotient sketch below N^{1+epsilon} gives an explicit nonuniform upper bound for H_N and is therefore a valid falsifier for the proposed barely-superlinear source lower bound. The target bridge remains C(H_N)>N^{1+epsilon} i.o. plus max{rho,q}<1+epsilon implies SAT notin P/poly, but sketch hardness is not itself a source lower bound.

## Definitions

- source object: H_N^{xor}:{0,1}^N -> {0,1} is H_N(x)=\oplus_{j\le M_N} SAT(\Phi_{N,j}(x)), with M_N=N^q, query length L_N=(\log N)^d, d>1, and a label-free generator circuit for all \Phi_{N,j} of size N^rho.
- target object: SAT on formulas of length L_N, measured by nonuniform Boolean circuits; the intended target consequence is SAT notin SIZE(n^c) for every fixed c, hence NP not subset P/poly only through this SAT complete problem.
- controlled interface: substitute a size L_N^c SAT circuit into each generated query slot and combine by XOR, paying generator overhead N^rho and slot overhead N^q L_N^c polylog(N).
- target-preserving condition: max{rho,q}<1+epsilon, L_N=(log N)^d is subpolynomial, the generator and transcript are independent of SAT labels, and the source lower bound holds on infinitely many valid N.

## Assumptions

- Circuit model is nonuniform fan-in-two Boolean circuits with equality patches charged O(N) gates per exceptional source input.
- Generator uniformity is only size-bounded nonuniform constructibility; no hidden advice bit may encode SAT labels or H_N values.
- A constructively label-free codebook B_N is an explicitly enumerable list of U_N formulas of length L_N computed without SAT-label queries.
- The sparse quotient decoder, from transcript T_N(x), produces at most A_N monomials over at most r_N named codebook coordinates and never uses the SAT value of a generated formula as a control bit.
- The sketch may fail on E_N source inputs; those are patched by nonuniform equality tests and therefore cost O(E_N N).

## Equations

- xor_carrier_definition: `H_N(x)=\bigoplus_{j=1}^{N^q} SAT(\Phi_{N,j}(x)),\qquad |\Phi_{N,j}(x)|=L_N=(\log N)^d.`. Valid when: Valid when the source object is the generated XOR-SAT carrier with fixed q,d and generator outputs well-formed SAT instances for every valid N.
- polylog_target_substitution: `SAT\in SIZE(n^c)\ \Longrightarrow\ C(H_N)\le N^\rho+N^q L_N^c\,polylog(N)=N^{\max\{\rho,q\}+o(1)}.`. Valid when: Applies after the controlled interface substitutes one nonuniform SAT circuit of length L_N into every generated query slot with L_N subpolynomial.
- magnification_window: `C(H_N)>N^{1+\epsilon}\ i.o.\ \wedge\ \max\{\rho,q\}<1+\epsilon\ \Longrightarrow\ \forall c\ C(SAT_n)\not\le n^c.`. Valid when: Requires the target-preserving condition, cofinal valid source lengths, and a source lower bound exceeding the substitution upper bound for each fixed c.
- label_free_codebook_upper_bound: `C(H_N)\le S_T+S_D+\widetilde O(U_N+A_N r_N)+O(E_NN).`. Valid when: Valid when a constructively label-free transcript and decoder express H_N outside E_N bad inputs as a sparse polynomial in hardwired SAT labels of the enumerated codebook.
- source_falsifier_threshold: `S_T+S_D+\widetilde O(U_N+A_Nr_N)+E_NN<N^{1+\epsilon-o(1)}\ \Longrightarrow\ C(H_N)<N^{1+\epsilon}.`. Valid when: Valid in the nonuniform source model where codebook labels may be hardwired but the transcript construction itself contains no SAT-label advice.

## Attempted Derivation

- Fix the surviving escape regime L_N=(log N)^d with d>1, M_N=N^q, and max{rho,q}<1+epsilon.
- Substitute a hypothetical size n^c SAT circuit into all N^q query slots; since L_N^c=N^{o(1)}, obtain C(H_N)<=N^{max{rho,q}+o(1)}.
- Define LFSketch_N by an explicit codebook of U_N length-L_N formulas, a label-free transcript T_N, and a decoder producing a sparse polynomial in hardwired SAT labels of codebook entries.
- Build a nonuniform circuit for H_N by computing T_N, evaluating the decoder, looking up hardwired codebook labels, evaluating at most A_N monomials, and patching E_N exceptional source inputs.
- Conclude that any LFSketch_N with S_T+S_D+tildeO(U_N+A_Nr_N)+E_NN<N^{1+epsilon} is a concrete upper-bound falsifier for the desired source lower bound.
- Attempt to prove the converse: small arbitrary circuits for H_N should yield small label-free sketches, making LFSketch hardness a source lower-bound certificate.

Blocking gap: No extraction theorem converts arbitrary H_N circuits into constructively label-free codebook sketches. The trivial transcript T_N=H_N is small whenever H_N is small but is not label-free and may encode SAT-label information semantically.

## Falsifiers

- label-dependent one-bit transcript falsifier: omitting label-freeness admits T_N(x)=H_N(x) and destroys the sketch audit.
- small global codebook falsifier: U_N=N^{1+epsilon-omega(1)} with cheap decoder lets the circuit hardwire all relevant SAT labels.
- patchable-error falsifier: E_N<N^{epsilon-o(1)} bad source inputs cost only E_NN<N^{1+epsilon-o(1)} gates.
- positive-beta rollback falsifier: if L_N=N^beta with beta>0 then SAT in SIZE(n^c) gives C(H_N)<=N^{q+beta c+o(1)}, so only bounded c are excluded.
- nonuniform leakage falsifier: generator or transcript advice that depends on SAT labels can compress the carrier while preserving apparent range entropy.

## Learning

Cycle 61 upgrades the XOR-carrier audit from vague label-free transcripts to a costed global-codebook normal form. The valid new contribution is an explicit upper-bound falsifier C(H_N)<=S_T+S_D+tildeO(U_N+A_Nr_N)+E_NN. This closes a leakage loophole in sparse quotient sketches, while exposing the exact remaining gap: absence of label-free sketches is not a general-circuit lower bound without a nonrelativizing extraction theorem.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch has isolated a structured upper-bound class; varying codebook entropy gives a concrete phase boundary before attempting any abstract lower-bound claim.
- Situation seed: A high-q XOR-SAT carrier with q=1+epsilon-3eta, rho=1+epsilon-4eta, L_N=(log N)^2, and a label-free generator whose generated formulas are projected onto an explicitly enumerable quotient codebook B_N.
- Varied variable: b=log_N U_N, the exponent of the constructively enumerable global codebook size; keep sparse decoder arity r_N=polylog(N) and monomial count A_N=N^a as secondary measured outputs.
- Held-fixed controls: Nonuniform Boolean circuit size model for both H_N and SAT., Subpolynomial query length L_N=(log N)^2, so target substitution has beta=0 in exponent accounting., No SAT-label advice in the generator, transcript, or decoder., Exact XOR aggregation over N^q slots, with equality patching charged O(N) per bad source input., Target bridge threshold max{rho,q}<1+epsilon held fixed.
- Expected observation: If b+max{a,0}+error_exponent<1+epsilon, the hardwired-codebook circuit beats the claimed source lower bound; if b crosses 1+epsilon, the falsifier disappears but no lower bound follows.
- Transfer certificate needed: A formal certificate must list the codebook enumerator, transcript circuit, decoder cost, sparse support size, and error set size; only a separate nonrelativizing extraction theorem may transfer absence of such certificates into C(H_N)>N^{1+epsilon}.

## Next Experiment

Instantiate a candidate generator and compute U_N,A_N,r_N,E_N for its SAT-preserving quotient codebook; if the cost is subthreshold, quarantine that generator, otherwise formulate the exact extraction theorem it would require.
