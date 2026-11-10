# cycle-0006

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization, Cycle 6: MCSP verifier transfer audit

## Candidate Lemma

For MCSP with threshold s(N)=N^alpha, a source lower bound C(MCSP_s,N)>N^{1+epsilon} transfers through the Cook-Levin verifier only to SAT notin SIZE(n^c) for c<(1+epsilon)/(1+alpha). Thus this nonprojection carrier does not yield NP not subset P/poly from a fixed barely-superlinear lower bound.

## Definitions

- source object: K_{alpha,N}=MCSP_{s(N)} on N-bit truth tables with threshold s(N)=N^alpha, alpha>=0, viewed as a nonprojection NP verifier carrier at valid truth-table lengths.
- target object: SAT circuit lower bound SAT notin SIZE(n^c) for a named exponent c; NP not subset P/poly would require exclusion of every constant c.
- controlled interface: Cook-Levin reduction from K_{alpha,N} to SAT instances of length M(N)=O(N s(N) polylog N), followed by substitution of a hypothesized SAT circuit family.
- target-preserving condition: the reduction is uniform, length-regular, and introduces no advice depending on the N-bit MCSP input beyond the target SAT circuits.

## Assumptions

- The source lower bound is against nonuniform Boolean circuits for infinitely many or all sufficiently large valid lengths N.
- The MCSP verifier guesses a circuit of size at most s(N) and checks its value on all N truth-table entries.
- The SAT circuit hypothesis supplies circuits of size O(m^c) for every relevant formula length m.
- Polylogarithmic Cook-Levin overhead is exponent-negligible in the N^{rho+o(1)} accounting.

## Equations

- verifier_time: `T_\alpha(N)=O(N\,s(N)\,\mathrm{polylog}\,N)=N^{1+\alpha+o(1)}`. Valid when: Valid when MCSP membership is verified by exhaustive truth-table checking of the guessed small circuit.
- induced_upper_bound: `\mathrm{SAT}\in\mathrm{SIZE}(m^c)\Rightarrow C(K_{\alpha,N})\le N^{c(1+\alpha)+o(1)}`. Valid when: Applies after the Cook-Levin reduction preserves uniformity and the SAT circuit is substituted nonuniformly.
- transfer_threshold: `C(K_{\alpha,N})>N^{1+\epsilon}\Rightarrow \mathrm{SAT}\notin\mathrm{SIZE}(n^c)\quad\text{for }c<\frac{1+\epsilon}{1+\alpha}`. Valid when: Requires the source lower bound and the induced SAT-based upper bound to hold on aligned valid lengths.
- major_target_ceiling: `\sup c\ \text{certified by fixed }(\epsilon,\alpha)\le \frac{1+\epsilon}{1+\alpha}\le 1+\epsilon`. Valid when: Valid when alpha is nonnegative, as forced by input-reading verification of N-bit instances.

## Attempted Derivation

- Fix alpha>=0 and K_{alpha,N}=MCSP_{N^alpha} on valid truth-table lengths N.
- Assume for contradiction that SAT has nonuniform circuits of size O(m^c).
- Given an N-bit truth table T, construct the Cook-Levin formula Phi_T expressing that there exists a circuit of size at most N^alpha matching T on all N inputs.
- The construction has length M(N)=O(N^{1+alpha} polylog N) because it enumerates every table position and evaluates the guessed circuit locally.
- A circuit for K_{alpha,N} hardwires the SAT circuit for length M(N), computes Phi_T, and outputs the SAT circuit's answer.
- Therefore C(K_{alpha,N})<=N^{c(1+alpha)+o(1)}.
- A lower bound C(K_{alpha,N})>N^{1+epsilon} contradicts the SAT hypothesis exactly when c(1+alpha)<1+epsilon.

Blocking gap: For NP not subset P/poly one must contradict every constant c, but fixed epsilon and alpha certify only c<(1+epsilon)/(1+alpha). Even alpha=0 leaves the input-reading ceiling c<1+epsilon.

## Falsifiers

- falsifier: choose SAT circuit exponent c>=(1+epsilon)/(1+alpha); then the induced MCSP upper bound is not below N^{1+epsilon}.
- falsifier: any hidden reduction overhead M(N)=N^{beta+o(1)} with beta>1+alpha further shrinks the certified target range to c<(1+epsilon)/beta.
- falsifier: nonuniform leakage occurs if the MCSP-to-SAT construction uses length-specific advice not already present in the hypothesized SAT circuit family.
- falsifier: invoking natural proofs alone is invalid here because the small-threshold MCSP accepted set is not large; the route fails quantitatively.

## Learning

Cycle 6 shows that moving from projection padding to a nonprojection MCSP carrier does not by itself create major magnification. The valid transfer is C(MCSP_{N^alpha},N)<=N^{c(1+alpha)+o(1)} under SAT in SIZE(n^c), so an N^{1+epsilon} source lower bound excludes only c<(1+epsilon)/(1+alpha). The input-reading floor alpha>=0 caps any fixed barely-superlinear bridge below all-exponent P/poly separation. The failure is a concrete threshold falsifier, not barrier folklore.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Test a self-referential meta-complexity carrier, such as Gap-MCSP or MKtP with succinctly generated truth tables, where the target SAT circuit is used nonblack-box. Compute whether the induced carrier upper bound can avoid the multiplicative c factor; if not, quarantine it by the same beta-ceiling lemma.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For nonuniform Boolean-circuit distinguishers, a PRG-to-output-bit lower-bound bridge based on enumerating seeds has a hardwired-range falsifier. If G:{0,1}^r->{0,1}^m δ-fools SIZE(S) with δ<1-2^{r-m}, then necessarily S<O(m2^r). Hence the usual seed-enumeration transfer can certify only t>Ω(S/(m2^r))-O(1), which is non-superconstant in the valid security regime. This refutes the naive route from such a PRG to meaningful P/poly lower bounds for the output-bit function.

## Definitions

- source object: a nonuniform Boolean-circuit PRG family G_n:{0,1}^{r(n)}->{0,1}^{m(n)} with distinguishing error δ(n) against SIZE(S(n)).
- target object: a claimed lower bound B_G notin SIZE(t(n)) for the output-bit relation B_G(n,i,y)=G_n(y)_i, intended as an E or EXP lower-bound carrier rather than as P != NP itself.
- controlled interface: convert small circuits for the output bits into a range-membership distinguisher by enumerating all seeds and testing whether z lies in Range(G_n).
- target-preserving condition: the transfer is valid only if the resulting distinguisher has size at most S(n), its advantage exceeds δ(n), and the derived t(n) remains superconstant after the m(n)2^{r(n)} overhead.

## Assumptions

- The adversary class is nonuniform SIZE(S), so the range table of G_n may be hardwired into the distinguisher.
- The security notion is ordinary statistical distinguishing advantage over U_m versus G(U_r).
- The output length satisfies m>r, otherwise the range test has no large advantage.
- No uniformity restriction is imposed on the distinguisher; this is the precise leakage point.

## Equations

- range_tester: `R_G(z)=\bigvee_{a\in\{0,1\}^{r}}[z=G(a)]`. Valid when: Valid when the source generator length parameters are fixed and nonuniform circuits may hardwire all output strings.
- hardwired_size: `\mathrm{size}(R_G)\le c\,m2^r`. Valid when: Applies when equality to each hardwired m-bit output is implemented by Boolean gates of constant fan-in.
- range_advantage: `\Pr[R_G(G(U_r))=1]-\Pr[R_G(U_m)=1]\ge 1-2^{r-m}`. Valid when: Requires m>r and uses only that the range of G has at most 2^r distinct outputs.
- security_constraint: `c\,m2^r\le S\ \Longrightarrow\ \delta\ge 1-2^{r-m}`. Valid when: Valid when G is claimed to fool every nonuniform circuit of size at most S with error δ.
- collapsed_transfer_threshold: `t>\Omega(S/(m2^r))-O(1)`. Valid when: Applies after the seed-enumeration bridge charges each candidate output-bit circuit inside the range test.

## Attempted Derivation

- Fix n and suppose G_n δ-fools SIZE(S) over m-bit tests.
- Build R_G by hardwiring every output G_n(a) and OR-ing equality tests over all 2^r seeds.
- R_G accepts G(U_r) with probability 1 and accepts U_m with probability at most 2^{r-m}.
- If c m2^r≤S, R_G is an allowed distinguisher with advantage at least 1-2^{r-m}; this contradicts δ<1-2^{r-m}.
- Therefore any valid nonuniform PRG security claim in this regime must have S<c m2^r or much weaker δ.
- A bridge that additionally assumes t-size circuits for the output bits only gives t>Ω(S/(m2^r))-O(1), which is superconstant only outside the valid security window.

Blocking gap: The method cannot both allow unrestricted nonuniform target circuits and forbid the nonuniform range-table distinguisher. That mismatch is the named nonuniform leakage gap.

## Falsifiers

- Hardwired Range(G_n) membership is a falsifier for any claimed nonuniform PRG security with δ<1-2^{r-m} and S≥c m2^r.
- A parameter choice r≤log S-log m-O(1) falsifies the route before any output-bit lower bound can be extracted.
- If the theorem says the range test must be uniform while the target lower bound is against P/poly, advice has leaked across the controlled interface.
- If m-r=O(1), the advantage 1-2^{r-m} is too small for the advertised high-advantage contradiction.
- If the generator construction is merely relativizing, the repair cannot be promoted to a P-vs-NP route without confronting BGS-style oracle separations.

## Learning

Cycle 6 isolates a concrete quantitative failure: seed-enumeration PRG bridges against nonuniform circuits collapse at S≈m2^r. The valid lesson is not a P != NP advance; it is that any derandomization carrier must either work in a uniform/advice-bounded model or provide a different target-preserving interface that prevents range hardwiring.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Audit a uniform-repair variant: source object logspace-uniform hitting generator, target object uniform range-recognition lower bound, threshold T versus 2^r m, and explicit statement of why this still does not imply P != NP.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Constant-gap explicit GapMCSP no-side carriers are target-preserving but not a free source: they are quantitatively equivalent to all-length E circuit lower bounds after padding. Thus the bridge is valid, while the source construction is the hard part.

## Definitions

- source object: a set S of input lengths and truth tables x_m in {0,1}^{2^m} with MCSP complexity K(x_m)>2^{epsilon m}, generated bitwise in time 2^{a m} without advice.
- target object: a language L in E such that every sufficiently large length n has Boolean circuit complexity greater than 2^{delta n}; this is an E lower bound, not P != NP.
- controlled interface: choose m(n) in S with n/kappa <= m(n) <= n and define L on length n by padding or projection from x_{m(n)} while preserving bit-uniformity.
- target-preserving condition: epsilon>0 and kappa<infty are constants, m(n) is uniformly computable, and no nonuniform selector or promise witness is used to choose the carrier.

## Assumptions

- K(x) denotes minimum Boolean circuit size of the truth-table function encoded by x.
- S is eventually kappa-dense: for every sufficiently large n there is m in S with n/kappa <= m <= n.
- The bit generator for x_m runs in 2^{O(m)}, so the padded language remains in E.
- Padding variables may be fixed to recover a circuit for x_m from a circuit for L_n with only O(n) overhead.

## Equations

- MCSP-no-side-threshold: `K(x_m)>2^{\epsilon m}`. Valid when: Valid when the source carrier is a named no-instance sequence for MCSP at exponential-in-m threshold, not a random existence argument.
- padding-transfer: `C_L(n)+O(n) \ge K(x_{m(n)}) > 2^{\epsilon m(n)} \ge 2^{(\epsilon/\kappa)n}`. Valid when: Applies when m(n) is kappa-dense below n and the padding reduction lets circuits for L_n restrict to circuits for x_{m(n)}.
- achievable-exponent: `\forall\delta<\epsilon/\kappa,\quad L\notin \mathrm{i.o.\text{-}SIZE}(2^{\delta n})`. Valid when: Requires constant epsilon and kappa, sufficiently large n, and absorption of the additive padding overhead into the exponent slack.
- uniformity-preservation: `T_L(n)\le 2^{O(m(n))}\mathrm{poly}(n)\le 2^{O(n)}`. Valid when: Valid when the carrier bits are computed uniformly and the length selector m(n) is computable without advice or search witnesses.

## Attempted Derivation

- Start with an E-explicit no-side carrier x_m at threshold 2^{epsilon m} on a kappa-dense length set S.
- For each target length n choose a uniform m(n) in S with n/kappa <= m(n) <= n.
- Define L(z) for |z|=n by evaluating x_{m(n)} on the first m(n) bits of z; dummy variables provide padding to length n.
- If L_n has a circuit of size s, fix the dummy variables to obtain a circuit for x_{m(n)} of size s+O(n).
- Since K(x_{m(n)})>2^{epsilon m(n)}, any circuit for L_n has size greater than 2^{epsilon m(n)}-O(n), hence greater than 2^{delta n} for every delta<epsilon/kappa.
- Conversely, any all-length E language with circuit lower bound 2^{epsilon n} yields an all-length explicit MCSP no-side carrier by taking its length-n truth tables.

Blocking gap: The remaining unsolved obligation is a uniform proof that a specific x_m has K(x_m)>2^{epsilon m}; the MCSP packaging does not weaken this obligation.

## Falsifiers

- falsifier: the carrier sequence is chosen by a nonuniform selector or advice string, so L is not guaranteed to lie in E.
- falsifier: the length set S has superconstant gap kappa(n), causing the transferred exponent epsilon/kappa(n) to collapse to zero.
- falsifier: the MCSP lower bound is against formulas, AC0, or another source model but is stated as unrestricted Boolean circuit complexity.
- falsifier: the reduction lands on MCSP yes-instances or undecided promise instances rather than certified no-side truth tables.
- falsifier: the source proof is natural in the Razborov-Rudich sense for a large useful property, so it cannot coexist with standard pseudorandom-function assumptions without extra non-natural structure.

## Learning

Cycle 6 converts the route into an equivalence audit. The bridge lemma is valid and quantitatively sharp: threshold 2^{epsilon m} plus kappa-density transfers to any E lower-bound exponent delta<epsilon/kappa. The new obstruction is circularity: a uniform constant-gap MCSP no-side carrier is already an E circuit lower bound, so future progress must supply a non-natural, nonuniform-free certificate of high MCSP rather than reuse the carrier as a black box.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Test whether a non-natural certificate such as short refutations of small-circuit encodings, or a derandomization-based hitting-set construction, can certify K(x_m)>2^{epsilon m} for an E-explicit sequence while avoiding advice and preserving constant kappa.
