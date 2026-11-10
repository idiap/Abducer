# cycle-0044

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: residual cap-denominator gate

## Candidate Lemma

Residual cap-denominator lemma for the high-q generated-OR carrier. Fix local predicate size S=N^sigma and exception budget E. If every residual set R of positive inputs with |R|>E has a one-sided sound local predicate hitting at least |R|/D_N of R, then greedy residual covering gives a nonuniform circuit for H_N of size N^{rho+o(1)}+N^{sigma+o(1)}D_N polylog(2^N)+E N^{1+o(1)}. Hence an asserted source lower bound C(H_N)>N^{1+epsilon-o(1)} is falsified whenever D_N<=N^{1+epsilon-sigma-o(1)}/polylog(N) and E<=N^{epsilon-o(1)}.

## Definitions

- source object: H_N(x)=OR_{j<=Q} SAT(G_N(x,j)), with x in {0,1}^N, Q=N^q, query length L=(log N)^d, d>1, and generator circuit size N^{rho+o(1)}.
- target object: exclusion of polynomial-size nonuniform SAT circuits, obtained by substituting SAT circuits into the generated-OR carrier for every fixed target exponent c.
- controlled interface: polylog-length SAT substitution through the generated queries, plus one-sided local predicates used only as source-side upper-bound falsifiers.
- target-preserving condition: q<1+epsilon, rho<1+epsilon, no advice leakage beyond the fixed nonuniform circuits, and the source lower bound must survive all residual one-sided cap covers.
- Positive residual R is a subset of H_N^{-1}(1) not yet covered by prior one-sided predicates.
- A local predicate A is sound on the generated range if A(G_N(x,j),j)=1 implies SAT(G_N(x,j))=1 for every generated pair.
- cap_R(A)=|{x in R: exists j<=Q with A(G_N(x,j),j)=1}|.
- D_N is the reciprocal residual cap fraction forced at every greedy stage.

## Assumptions

- The source lower-bound model is unrestricted Boolean circuits on N input bits for the explicit carrier H_N.
- The local predicates are nonuniform circuits of size at most N^sigma and are allowed position tags but must be one-sided sound on the actual generated range.
- Equality patching of E missed positive inputs costs E N^{1+o(1)} gates and does not use SAT-solving advice.
- The target bridge remains route-level only; it does not assert P != NP without a valid source lower bound.

## Equations

- carrier: `H_N(x)=\bigvee_{j=1}^{N^q} SAT(G_N(x,j)),\qquad |G_N(x,j)|=(\log N)^d.`. Valid when: Valid when the source carrier is the explicit generated-OR family with polylogarithmic SAT queries and fixed q,d parameters.
- target_substitution: `SAT\in SIZE(n^c)\ \Longrightarrow\ C(H_N)\le N^{\max\{\rho,q\}+o(1)}.`. Valid when: Applies after the generator size is N^{rho+o(1)} and each polylogarithmic SAT query receives a size L^c circuit.
- greedy_cover_size: `K\le D_N\log |H_N^{-1}(1)|\le O(D_N N).`. Valid when: Valid when every residual positive set larger than E has a sound predicate covering at least a 1/D_N fraction.
- source_upper_bound: `C(H_N)\le N^{\rho+o(1)}+N^{\sigma+o(1)}D_N\,polylog(2^N)+E N^{1+o(1)}.`. Valid when: Requires that the greedy predicates are one-sided sound on the generated range and missed positives are patched by equality tests.
- falsifier_threshold: `D_N\le N^{1+\epsilon-\sigma-o(1)}/polylog(N),\quad E\le N^{\epsilon-o(1)}\ \Longrightarrow\ C(H_N)\le N^{1+\epsilon-o(1)}.`. Valid when: Valid in the threshold regime where rho is below 1+epsilon and the cover and patching terms dominate the audit.

## Attempted Derivation

- Fix sigma and the family P_sigma^{1s} of size-N^sigma local predicates sound on the generated range.
- Start with R_0=H_N^{-1}(1). While |R_t|>E, choose A_t with cap_{R_t}(A_t)>=|R_t|/D_N and remove the hit positives.
- After K steps, |R_K|<E once K>=D_N log(|H_N^{-1}(1)|/E), so K=O(D_N N) is enough without needing to enumerate the universe uniformly.
- Build the circuit: compute the generator, evaluate all chosen predicates, OR their hits, and patch the E missed positives by equality tests.
- The resulting upper bound is below N^{1+epsilon} when rho<1+epsilon, D_N N^sigma is subthreshold up to logs, and E N is subthreshold.
- Contraposition yields the hard-residual distribution obligation for any valid source lower bound.

Blocking gap: No lower bound is known showing that every residual positive distribution fools all one-sided generated-range predicates of size N^sigma at hit probability N^{-(1+epsilon-sigma)}.

## Falsifiers

- residual cap denominator D_N below N^{1+epsilon-sigma-o(1)} gives a concrete falsifier for the source lower bound
- exception set E below N^{epsilon-o(1)} is patchable by equality gates
- nonuniform leakage through one-sided predicates sound only on the generated range
- threshold collapse if q or rho reaches 1+epsilon before the target substitution is applied
- model mismatch if the cap lower bound is proved only for uniform predicates while the source model is nonuniform circuits
- natural-proof leakage if the residual certificate becomes a large constructive global property

## Learning

Cycle 44 converts the residual cap profile into a greedy cap-denominator theorem. A generated-OR source lower bound must now produce hard residual positive distributions against all one-sided local predicates; otherwise D_N N^sigma and E N give an explicit subthreshold upper-bound falsifier. This is route-level progress, not a main P != NP proof.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The abstract cap profile must be tested against a concrete threshold: whether residual one-sided certificates with moderate size can greedily cover positives before N^{1+epsilon} gates are spent.
- Situation seed: Generated-OR carrier with Q=N^q SAT queries of length L=(log N)^d, d=2, q=0.8(1+epsilon), generator size N^{rho+o(1)} with rho<q, and local predicates that recognize sound partial satisfying certificates on the generated range.
- Varied variable: cap denominator exponent theta where every large residual R has a sound size-N^sigma predicate hitting at least N^{-theta}|R| positives, so D_N=N^theta.
- Held-fixed controls: q<1+epsilon and rho<1+epsilon to preserve the target substitution bridge, d>1 so exhaustive SAT lookup costs N^{omega(1)} and is not a subthreshold falsifier, one-sided soundness on every generated formula, including negative bags, exception budget E=N^eta with eta<epsilon so equality correction remains subthreshold
- Expected observation: If sigma+theta<1+epsilon, the greedy cover constructs a subthreshold circuit for H_N; if sigma+theta>=1+epsilon for all valid sigma, the route survives this particular falsifier and needs an actual residual distribution lower bound.
- Transfer certificate needed: A formal proof that the chosen predicates are nonuniformly evaluable within N^sigma, are sound on the generated range, and that the greedy cover plus equality patching composes with the target-preserving SAT-substitution bridge without adding advice leakage.

## Next Experiment

Instantiate the cap audit for partial-assignment predicates of width w on L=(log N)^2 formulas: compute theta(w,sigma) for random-looking generated ranges, then check whether sigma+theta can stay above 1+epsilon while q,rho remain in the target-preserving window.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

ANF-support lower bounds over F_2 give a valid size lower bound only of order log support; since support is at most 2^m, this route cannot certify SIZE(m^k) lower bounds for any k>1 on m-bit SAT slices.

## Definitions

- source object: L_2(f_m), the support size of the unique multilinear F_2 algebraic normal form of the SAT_m characteristic function.
- target object: nonuniform fanin-two Boolean circuits SIZE(m^k) deciding SAT_m on all m-bit encodings, for fixed k>1.
- controlled interface: expand AND/OR/NOT gates into F_2 ANF and compare support of the computed Boolean function.
- target-preserving condition: the support lower bound must exceed the ANF support envelope of every size-s circuit on the same m-bit slice.

## Assumptions

- Circuit size counts fanin-two gates; NOT gates may be pushed to inputs at constant-factor cost.
- The SAT encoding is fixed and total on m bits, so the truth table has N=2^m entries.
- The lower-bound measure is exactly ANF support, not arithmetic circuit size or degree.

## Equations

- ANF-cap: `L_2(f_m):=|\operatorname{supp}(\operatorname{ANF}_{\mathbb F_2}(f_m))|\le 2^m=N`. Valid when: Valid when f_m is a total Boolean function on m bits and the unique multilinear F_2 ANF is used.
- circuit-support-envelope: `C\in SIZE(s)\Rightarrow L_2(C)\le 2^{c s}`. Valid when: Valid when circuits have fanin-two AND/OR/NOT gates and ANF support is expanded gate by gate.
- transfer-collapse: `L_2(SAT_m)>2^{c s}\Rightarrow SIZE(SAT_m)>s,\quad s\le O(m)\text{ is the largest possible certified range}`. Valid when: Applies after the same encoding and basis are preserved between the SAT slice and the hypothesized target circuit.

## Attempted Derivation

- Define L_2 by the Mobius transform from the full truth table to the unique F_2 ANF coefficients.
- A fanin-two size-s circuit has at most O(s) relevant input leaves in the output sub-DAG, hence its ANF has support at most 2^{O(s)}.
- Thus L_2(SAT_m)>2^{O(s)} would exclude size s circuits, provided the same m-bit slice and F_2 basis are preserved.
- But L_2(SAT_m)<=2^m, so the bridge cannot rule out size m^{1+epsilon}; OR_m has L_2=2^m-1 and linear circuits.

Blocking gap: ANF support is capped by truth-table length and is high for easy P functions, so it is not useful against polynomial-size circuits.

## Falsifiers

- OR_m has L_2=2^m-1 and linear AC0 circuits; it is the falsifier to usefulness against P or SIZE(poly).
- Padded g(x,y)=SAT_t(x) has m=t+t^beta and L_2(g)=L_2(SAT_t); padding collapses any claimed m^k transfer.
- Changing to real polynomials or low-degree representations breaks target preservation; dense F_2 ANF is basis dependent.
- The constructive large test L_2>N/3 is valid as a natural-looking property, but it accepts OR_m, so it is not useful.

## Learning

Cycle 44 proves a compact threshold collapse: ANF support gives only size Omega(log L_2), and L_2<=2^m makes superlinear m-bit lower bounds impossible. OR_m supplies the valid falsifier to usefulness. This is route-level quarantine, not P != NP progress.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for ANF-support routes.`
- Rationale: The route needs a concrete threshold test because abstract algebraic language hides the fact that support can be maximal for easy functions and unchanged by padding.
- Situation seed: Use padded SAT slices g_{t,beta}(x,y)=SAT_t(x) with m=t+t^beta and, separately, OR_m as an easy maximal-support control.
- Varied variable: Padding exponent beta>1.
- Held-fixed controls: F_2 ANF basis and total m-bit truth-table semantics are fixed., Target circuits remain fanin-two AND/OR/NOT nonuniform circuits measured in m., The lower-bound claim may use only L_2 support, not extra semantic promises.
- Expected observation: As beta grows, L_2(g) stays at most 2^t while the claimed target threshold m^k grows; OR_m shows maximal support is compatible with linear circuits.
- Transfer certificate needed: A new measure or compiler bound beating the 2^m cap and rejecting easy dense-ANF functions; otherwise the intuition cannot enter the P-vs-NP proof queue.

## Next Experiment

Audit shifted-partial-derivative and spectral-support measures with the same OR_m plus padded-SAT controls; compute whether their Boolean-circuit envelope exceeds the truth-table cap or merely repeats ANF collapse.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Bicylinder load is a necessary source-side condition for a valid MCSP no-side carrier: if an accepting one-certificate fixes p one-positions and z zero-positions, then both p and z must exceed 2^{epsilon m}/Theta(m), or a zero-fill or one-fill completion gives an accepted table with subthreshold unrestricted circuits.

## Definitions

- source object: an E-uniform family P_m of accepting cylinders over truth tables T in {0,1}^{2^m}, intended as MCSP no-side certificates at threshold S_m=2^{epsilon m}.
- target object: an E language obtained by canonical row extraction or low-image multiplexing, requiring unrestricted circuit lower bound 2^{delta n}.
- controlled interface: a transcript/cylinder profile (p,z,D,kappa) is passed to the carrier transfer only if every accepted row is MCSP-hard or a hard row is uniformly selected or multiplexed.
- target-preserving condition: no advice, E-canonical unranking, constant kappa-density, bounded distinct-image entropy D, and epsilon within the verifier cap alpha_V.
- accepting cylinder: a partial assignment to truth-table coordinates such that every completion is accepted by P_m.
- positive load p and negative load z: the numbers of fixed coordinates assigned 1 and 0 in the accepting cylinder.

## Assumptions

- Circuit model is unrestricted Boolean circuits over a fixed finite basis with equality to an m-bit string implementable in O(m) gates.
- The MCSP threshold is S_m=2^{epsilon m} for constant epsilon>0.
- The certificate is semantic: all completions of its fixed coordinates are accepted, so fill arguments are legitimate.
- No nonuniform advice may choose lengths, completions, or hard rows.

## Equations

- sparse_and_cosparse_completion: `\operatorname{size}(T_{0\text{-fill}})\le Cmp+O(1),\quad \operatorname{size}(T_{1\text{-fill}})\le Cmz+O(1)`. Valid when: Valid when unrestricted circuits compute equality tests explicitly and the cylinder guarantees acceptance of every completion.
- bicylinder_necessary_gate: `p,z>\frac{2^{\epsilon m}-O(1)}{Cm}`. Valid when: Valid when P_m is claimed to certify MCSP no-side soundness against size 2^{epsilon m} circuits.
- exponential_rate_falsifier: `\min\{p,z\}=2^{\theta m+o(m)},\ \theta<\epsilon\ \Rightarrow\ \exists T\in P_m:\operatorname{MCSP}(T)<2^{\epsilon m}`. Valid when: Applies when epsilon is constant and polynomial factors are negligible only at exponential-rate scale.

## Attempted Derivation

- Start with an accepting cylinder C fixing p ones and z zeros for a proposed global MCSP invariant P_m.
- Use zero-fill and one-fill completions to prove the bicylinder necessary gate p,z>2^{epsilon m}/Theta(m).
- Try to repair the source by requiring every accepting transcript to be bicylinder-heavy.
- Observe that this removes sparse and co-sparse completions but still permits balanced easy functions, including parity with polynomial-size circuits.
- Attempt to infer unrestricted circuit hardness from bicylinder heaviness plus low image entropy D; the inference would need a non-natural global invariant excluding all small circuits, not a counting or weight argument.

Blocking gap: No valid implication is known from bicylinder-heavy accepting cylinders to unrestricted MCSP hardness. Weight balance is a large, constructive, circuit-insensitive condition and is falsified by explicit small balanced circuits.

## Falsifiers

- falsifier: an accepting cylinder with fewer than 2^{epsilon m}/poly(m) fixed one-positions gives a zero-filled accepted table with small DNF circuit.
- falsifier: an accepting cylinder with fewer than 2^{epsilon m}/poly(m) fixed zero-positions gives a one-filled accepted table with small co-DNF circuit.
- Balanced-only invariants are invalid because parity and majority are balanced but have polynomial-size unrestricted circuits.
- A constructive large property that accepts only high-MCSP rows would hit the natural-proofs obstruction under standard PRF assumptions; the sparse low-D carrier is outside this only if non-large and advice-free.
- Subthreshold ranked random access to the low-D image family still leaks circuits for rows and invalidates the claimed threshold.
- Nonuniform length or row selection converts the consequence into nonuniform advice and is not a valid E lower-bound transfer.

## Learning

Cycle 44 proves a sharper source-side falsifier: MCSP carrier soundness at threshold 2^{epsilon m} requires every accepting cylinder to have both positive and negative load above 2^{epsilon m}/Theta(m). This is valid route-level progress because it rejects zero-fill and one-fill transcript sources quantitatively. It also shows the repair is only necessary: balanced-heavy predicates still accept polynomial-size functions such as parity, so the missing object is a non-natural, advice-free, circuit-sensitive global invariant, not another balance or density condition.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The next source proposals will likely add balance constraints after the zero-fill attack; a concrete cylinder-load experiment tests exactly when that repair is only a falsifier filter and when it could preserve the target interface.
- Situation seed: A padded GapMCSP carrier P_m whose accepting certificate defines a cylinder fixing b(m) one-coordinates and b(m) zero-coordinates of a truth table of length N=2^m, with all other positions unconstrained, followed by the existing low-image multiplexing extractor.
- Varied variable: The cylinder load exponent theta where b(m)=2^{theta m}.
- Held-fixed controls: MCSP threshold S_m=2^{epsilon m} for unrestricted Boolean circuits., E-uniform canonical enumeration and no nonuniform advice., Distinct-image entropy D and padding gap kappa are fixed constants., The target consequence remains an E lower bound with delta<epsilon/(kappa(1+D)) only if a hard row is independently certified.
- Expected observation: For theta<epsilon the zero-fill or one-fill completion has circuit size 2^{theta m+o(m)}, so the carrier is invalid. For theta>=epsilon the sparse-fill falsifier disappears, but parity-like balanced easy completions show that balance still does not certify MCSP hardness.
- Transfer certificate needed: A valid transfer needs a separate, non-natural, non-large, advice-free proof that the accepted image excludes every unrestricted circuit of size below 2^{epsilon m}, plus E-canonical row recovery preserving D and kappa.

## Next Experiment

Test candidate nonlinear global invariants for bicylinder-heavy certificates and for acceptance of explicit balanced small circuits; first target is any invariant expressible by low-depth symmetric or spectral constraints, since parity/majority should expose whether it is circuit-sensitive or merely balance-sensitive.
