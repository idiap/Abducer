# cycle-0001

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For fixed k>=2 and epsilon>0, a lower bound SIZE(Pad_k(SAT)_N)>N^{1+epsilon} against nonuniform fan-in-2 Boolean circuits implies SAT notin SIZE(n^c) for every c<k(1+epsilon). This is a valid route-level bridge, not a proof of P != NP.

## Definitions

- source object: Pad_k(SAT), the exact-zero k-padding of SAT with total length N=n^k, measured against nonuniform fan-in-2 Boolean circuits of size N^{1+epsilon}.
- target object: SAT_n measured against nonuniform fan-in-2 Boolean circuits of size n^c; the target consequence is SAT notin SIZE(n^c), not P != NP.
- controlled interface: projection to the first n input bits plus an O(N)-size padding-validity checker before running the target circuit.
- target-preserving condition: any O(n^c)-size circuit family for SAT must compose into an O(N+N^{c/k})-size circuit family for Pad_k(SAT) with the same basis and no hidden advice.

## Assumptions

- k and epsilon are fixed constants, and N ranges over legal lengths N=n^k.
- The padding predicate is exact-zero padding, so invalid padded strings are rejected by a linear-size circuit.
- Circuit-size classes are nonuniform and use the same fan-in-2 Boolean basis on source and target.
- The exponent margin is strict: c/k<1+epsilon, absorbing constant factors for sufficiently large n.

## Equations

- E1_padding_length: `N=n^k,\qquad Pad_k(L)_N=\{x0^{N-n}:x\in L_n\}.`. Valid when: Valid when the source lower-bound model is explicitly restricted to legal padded lengths N=n^k.
- E2_composition_upper_bound: `C(Pad_k(L)_N)\le O(N)+C(L_n)\le O(N+N^{c/k})\quad\text{if }C(L_n)\le O(n^c).`. Valid when: Applies after the padding checker and target circuit use the same nonuniform Boolean basis.
- E3_exponent_transfer: `C(Pad_k(SAT)_N)>N^{1+\epsilon}\Longrightarrow SAT\notin SIZE(n^c)\quad\text{for every }c<k(1+\epsilon).`. Valid when: Requires the target-preserving composition bound and a strict exponent gap absorbing constants asymptotically.

## Attempted Derivation

- Fix L=SAT, constants k>=2 and epsilon>0, and legal source length N=n^k.
- Assume toward contradiction that SAT has O(n^c)-size circuits for some c<k(1+epsilon).
- On a padded input y of length N, check that the last N-n bits are zero using O(N) gates and feed the first n bits into the SAT circuit.
- The composed circuit has size O(N+n^c)=O(N+N^{c/k}). Since max(1,c/k)<1+epsilon, this is below N^{1+epsilon} for large N.
- This contradicts the source lower bound for Pad_k(SAT), yielding SAT notin SIZE(n^c).
- Auditing the P/poly target shows that fixed k leaves all exponents c>=k(1+epsilon) untouched.

Blocking gap: The bridge does not reach NP notin P/poly unless one proves a cofinal family of padded lower bounds or finds a non-artificial carrier whose interface compresses every polynomial target exponent below N^{1+epsilon}.

## Falsifiers

- falsifier: threshold collapse occurs when the target exponent c is at least k(1+epsilon), because the induced source circuit may exceed N^{1+epsilon}.
- falsifier: model mismatch occurs if the source lower bound is for AC0, formulas, or uniform circuits while the composed circuit is unrestricted nonuniform P/poly.
- falsifier: nonuniform leakage occurs if the padding parser or length selector uses advice not counted in the source circuit size.
- falsifier: an infinitely-often source lower bound is not valid for excluding eventual SIZE(n^c) target circuits without matching quantifiers.
- falsifier: a natural-proofs-style source argument for unrestricted circuits must explain why it is non-natural or why pseudorandom-function assumptions are avoided.

## Learning

The exact quantitative transfer is C(Pad_k(SAT)_N)<=O(N+N^{c/k}); hence the barely-superlinear lower bound magnifies only up to target exponent k(1+epsilon). The valid bridge is useful as an exponent-calibrated route lemma, while the fixed-k P/poly claim is blocked by a concrete threshold falsifier rather than by vague folklore.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Instantiate the same exponent audit for a padded MKtP or GapMCSP carrier: name the verifier, compute Cook-Levin or direct-composition length blow-up, and test whether assuming SAT in SIZE(n^c) yields source circuits below N^{1+epsilon} without model mismatch or nonuniform leakage.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

A route that proves SAT_n notin SIZE(n^k) only by exhibiting a poly(N)-constructive, N^{-a}-large truth-table property useful against SIZE(n^k) is conditionally blocked by the Razborov-Rudich natural-proof mechanism. Under exponentially secure pseudorandom functions supported inside SIZE(n^k), the same property is a distinguisher with advantage at least N^{-a}.

## Definitions

- source object: a family R_n subset {0,1}^{2^n} deciding properties of n-bit Boolean truth tables in time (2^n)^c and having density at least (2^n)^{-a}.
- target object: the nonuniform slice lower bound SAT_n notin SIZE(n^k) infinitely often, or the same statement for an NP-complete slice under advice-free length-respecting encodings.
- controlled interface: transfer is only R_n(SAT_n)=1 together with R_n cap TT(SIZE(n^k)) empty, with no semantic information about SAT used outside the property test.
- target-preserving condition: the encoding of the target slice must map n-bit inputs to one N=2^n bit truth table and must not add advice, promises, or more than polynomial threshold loss.

## Assumptions

- Constants a,c,k are fixed before the route starts.
- R_n is decidable from the complete truth table in time N^c, where N=2^n.
- R_n is useful at the exact threshold: no n-input function computed by a circuit of size n^k lies in R_n.
- There is a pseudorandom distribution D_n, e.g. from an exponentially secure PRF, supported on functions computed by circuits of size n^k and secure against time N^c+O(N n^k) distinguishers with advantage below N^{-a}/2.

## Equations

- truth-table-regime: `N=2^n,\quad R_n\subseteq\{0,1\}^{N}`. Valid when: Valid when the source object is a property of total n-bit Boolean functions represented by complete truth tables.
- largeness-threshold: `\delta_n=\Pr_{f\leftarrow U_n}[R_n(f)=1]\ge N^{-a}=2^{-an}`. Valid when: Valid when largeness is measured in Razborov-Rudich form as inverse polynomial density in the truth-table length.
- usefulness-threshold: `R_n\cap \mathrm{TT}(\mathrm{SIZE}(n^k))=\emptyset`. Valid when: Valid when the target circuit class is nonuniform SIZE at the named n^k threshold with no hidden advice leakage.
- target-bridge: `R_n(\mathrm{SAT}_n)=1\ \mathrm{i.o.}\Rightarrow \mathrm{SIZE}(\mathrm{SAT}_n)>n^k\ \mathrm{i.o.}`. Valid when: Applies after the reduction preserves uniformity and the n^k circuit-size threshold up to fixed polynomial factors.
- natural-distinguisher: `\mathrm{Adv}(D_R;U_n,D_n)=|\Pr_{U_n}[R_n]-\Pr_{D_n}[R_n]|\ge \delta_n`. Valid when: Requires D_n to be supported on small circuits that the useful property rejects on every sampled function.
- security-collapse: `T(D_R)\le N^c+O(N\cdot n^k),\quad \mathrm{Sec}_{D_n}(T)<\delta_n/2\Rightarrow \bot`. Valid when: Valid when the PRF security notion allows a full-truth-table distinguisher running in polynomial time in N.

## Attempted Derivation

- Set N=2^n and suppose the proposed route supplies R_n with constructivity N^c, largeness delta_n >= N^{-a}, and usefulness against SIZE(n^k).
- The target bridge says R_n(SAT_n)=1 for infinitely many n, hence SAT_n has no size n^k circuit on those n if the interface is target-preserving.
- Let D_n be a pseudorandom distribution supported on n-bit functions computed by circuits of size n^k.
- Because R_n is useful, every sample from D_n is rejected: Pr_{g<-D_n}[R_n(g)=1]=0.
- Because R_n is large, a uniformly random truth table is accepted with probability at least delta_n.
- A distinguisher queries or constructs the full truth table and runs the R_n decider, using time at most N^c+O(N n^k).
- The distinguishing advantage is at least delta_n, contradicting security below delta_n/2.

Blocking gap: The derivation is conditional on a PRF-like distribution secure against full-truth-table time and supported at the same n^k threshold. It also applies only after the route is formalized as a large constructive truth-table property.

## Falsifiers

- falsifier: exhibit a target-preserving certificate of density below every available PRF advantage while still proving SAT_n notin SIZE(n^k).
- falsifier: show the proof object is not decidable from the complete truth table in N^{O(1)} time and the nonconstructivity is essential, not hidden advice.
- falsifier: use a nonrelativizing operation in the actual target transfer, not merely in presentation language.
- falsifier: demonstrate that no PRF or pseudorandom distribution is supported inside the named circuit threshold, making the L1 quarantine only conditional.
- falsifier: expose a reduction that loses the n^k threshold or introduces nonuniform leakage; then the claimed bridge is not valid.

## Learning

The branch obtained a concrete threshold audit: a poly(N)-constructive N^{-a}-dense property useful against SIZE(n^k) yields a full-truth-table distinguisher of advantage N^{-a} against n^k-size PRFs. Therefore a lower-bound route must name a real escape feature: non-large, nonconstructive, non-truth-table, nonrelativizing, or quantitatively below the PRF threshold. This is route-level progress, not progress on P != NP itself.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Try a repaired source object: a sparse or non-truth-table certificate for SAT_n with density bound delta_n << N^{-a}; compute whether it still gives any explicit lower bound s(n) beyond current trivial thresholds without advice leakage.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Fix epsilon>0. If a deterministic uniform generator G outputs, on input 1^n, a truth table y_n in {0,1}^{2^n} within time 2^{O(n)} and y_n has Boolean circuit complexity greater than 2^{epsilon n} for all sufficiently large n, then the induced language L_G is in E and has circuit complexity greater than 2^{epsilon n} on length n. By the Impagliazzo-Wigderson theorem this route-level consequence yields BPP=P, not P != NP.

## Definitions

- source object: an MCSP-type hard-table carrier G with semantic promise CktSize(y_n)>2^{epsilon n} for N=2^n and uniform output time N^{O(1)}.
- target object: an E-language L_G whose length-n truth table is y_n, plus the standard IW derandomization target BPP=P from eventual exponential worst-case hardness.
- controlled interface: map the carrier truth table to the length-n slice of L_G without advice, nonuniform seed choice, promise-dependent decoding, or a reduction that changes N=2^n.
- target-preserving condition: the same threshold 2^{epsilon n}=N^{epsilon} holds for the extracted slice for all sufficiently large n, and G remains deterministic uniform with bit recovery in 2^{O(n)} time.

## Assumptions

- Boolean circuits use a fixed finite basis and nonuniform size is measured on n input variables.
- The generator G is total and uniform; its description is not length-dependent advice.
- The MCSP lower-bound assertion is eventual, not merely infinitely often, when invoking IW.
- IW is used only as a derandomization transfer; no P vs NP separation is claimed.

## Equations

- length-threshold: `N=2^n,\qquad s(n)=2^{\epsilon n}=N^{\epsilon}.`. Valid when: Valid when the source truth table encodes an n-bit Boolean function.
- carrier-hardness: `C_{\mathrm{ckt}}(y_n)>s(n).`. Valid when: Valid when MCSP size is measured for circuits computing the represented n-bit function.
- extracted-language: `L_G(x)=y_{|x|}[\operatorname{bin}(x)],\qquad y_n=G(1^n).`. Valid when: Applies when the table order is canonical and G outputs exactly 2^n bits.
- slice-size-transfer: `C_{\mathrm{ckt}}(L_G\cap\{0,1\}^n)=C_{\mathrm{ckt}}(y_n)>2^{\epsilon n}.`. Valid when: Valid when both sides use the same Boolean basis and input length n.
- uniform-time-transfer: `T_{L_G}(n)\le 2^{O(n)},\qquad L_G\in E.`. Valid when: Valid when recomputing G(1^n) and indexing one bit costs polynomial time in 2^n.
- IW-target: `(\exists L\in E)(\exists \epsilon>0)(\forall^{\ast}n)\ C_{\mathrm{ckt}}(L_n)>2^{\epsilon n}\ \Longrightarrow\ \mathrm{BPP}=\mathrm{P}.`. Valid when: Requires the standard worst-case hardness versus randomness theorem with eventual exponential hardness.

## Attempted Derivation

- Define N=2^n and let the MCSP carrier be a uniform algorithm G producing one N-bit table y_n per input length.
- Assume the semantic carrier property CktSize(y_n)>N^epsilon for all sufficiently large n.
- Construct L_G by taking y_n as the length-n truth table; compute L_G(x) by running G(1^n) and reading the indexed bit.
- The running time is N^{O(1)}=2^{O(n)}, hence L_G is in E.
- The length-n circuit complexity of L_G equals the circuit complexity of y_n, so the threshold N^epsilon is preserved exactly.
- Invoke IW to obtain BPP=P from eventual 2^{epsilon n} hardness in E.
- Audit the source: an MCSP decider, a random high-complexity table, or an advice-selected table does not satisfy the source object definition.

Blocking gap: The missing object is a uniform hard-table carrier G. MCSP as a decision language does not supply G within the E time budget, and a nonuniform seed would leak the lower bound into advice.

## Falsifiers

- falsifier: the carrier outputs tables only for infinitely many n, which is insufficient for the stated IW consequence.
- falsifier: the hard table is chosen by length-dependent advice or an existential seed, causing nonuniform leakage.
- falsifier: the MCSP certificate verifies smallness, not largeness, so the source object is not efficiently checkable in NP.
- falsifier: the extraction changes from N=2^n to N=2^{poly(n)} and collapses the threshold below 2^{epsilon n}.
- falsifier: the claimed consequence is only MCSP not in a weak nonuniform class, while the target statement silently upgrades it to P != NP.

## Learning

The useful carrier transfer is not MCSP-hardness folklore but a precise interface: uniform high-MCSP truth tables at threshold N^epsilon transfer to E lower bounds and IW derandomization. The route currently fails at source construction, not at the extraction step. Nonuniform leakage is the main formal obstruction.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Test known meta-complexity carriers such as MKtP/KT-hard strings, pseudodeterministic constructions, and proof-complexity canonical pairs for a uniform N^{O(1)} hard-table generator; record exact threshold loss and whether largeness is certified or only assumed.
