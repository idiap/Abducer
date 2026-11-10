# cycle-0048

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Relativizing locality-extraction gate for generated-OR carriers

## Candidate Lemma

For high-q polylog generated-OR carriers, one-sided separator hardness is a valid source certificate only after a nonrelativizing locality-extraction theorem. Any relativizing semantic extractor from small H_N circuits to small separator covers has a planted-control oracle falsifier.

## Definitions

- source object: the Boolean carrier H_N(x)=OR_{j<=N^q} SAT(G_N(x,j)) on N-bit x, with generator size N^rho and query length L=(log N)^d.
- target object: the route-level consequence SAT notin P/poly obtained from C(H_N)>N^{1+epsilon} plus the substitution bridge, not the full P != NP conjecture.
- controlled interface: substitute a size L^c SAT circuit into each generated query; the only target cost is N^rho+N^q L^{O(c)}.
- target-preserving condition: d>1, (1+epsilon)/2<q<1+epsilon, rho<1+epsilon, uniform G_N, and no advice or oracle bit outside the generated SAT instances.
- one-sided separator cover: local predicates of size N^sigma that hit at least one positive generated bag and reject every negative bag, with E exceptional bags patchable by equality circuits.

## Assumptions

- epsilon>0 is fixed and all o(1) terms are uniform over fixed SAT exponent c.
- The target bridge is nonuniform P/poly but the generator is uniform or has explicitly charged nonuniformity N^rho.
- A relativizing extractor may inspect H_N, G_N, and oracle SAT labels, but not syntactic facts special to the real Cook-Levin SAT relation.
- Separator covers are charged by D N^sigma log N plus EN, including greedy-cover overhead and exact correction.

## Equations

- carrier: `H_N(x)=\bigvee_{j\le N^q} SAT(G_N(x,j)),\quad |G_N(x,j)|=L=(\log N)^d.`. Valid when: Valid when the carrier generator is uniform and emits length-L CNF instances with no nonuniform advice.
- target-substitution: `SAT\in SIZE(n^c)\Rightarrow C(H_N)\le N^{\rho+o(1)}+N^qL^{O(c)}=N^{\max\{\rho,q\}+o(1)}.`. Valid when: Applies after each generated query is substituted by the assumed SAT circuit and L is polylogarithmic.
- separator-upper-bound: `C(H_N)\le C(G_N)+O(DN^\sigma\log N+EN).`. Valid when: Requires a one-sided separator cover with D local predicates of size N^sigma and E patchable bad bags.

## Attempted Derivation

- Fix d>1 and q,rho<1+epsilon; the substitution equation still gives the desired target consequence from a true C(H_N)>N^{1+epsilon} lower bound.
- Try to replace the direct lower bound by proving every one-sided local separator cover has D N^sigma log N+EN>=N^{1+epsilon-o(1)}.
- For this replacement to be valid, the contrapositive must extract a small separator cover from any arbitrary circuit A computing H_N with size below N^{1+epsilon}.
- A planted-control oracle sets one generated formula to a trivial satisfiable/unsatisfiable control depending on b(x), so H_N=b(x) is easy while unrelated generated SAT ranges keep separator covers hard.

Blocking gap: No known nonrelativizing locality-extraction theorem converts an arbitrary small H_N circuit into local SAT-range separators with only N^{o(1)} loss.

## Falsifiers

- Planted-control oracle falsifier: H_N has O(1) oracle-size circuits although one-sided separators on noncontrol ranges remain hard.
- Normal-form falsifier: an arbitrary H_N circuit may compute the OR globally without exposing any local formula predicate usable as a separator.
- Nonuniform leakage falsifier: advice can name the control coordinate or residual exceptions unless its cost is charged inside rho or EN.
- Threshold falsifier: if max{q,rho}>=1+epsilon, even a valid H_N lower bound no longer magnifies to SAT notin P/poly.

## Learning

Cycle 48 makes the obstruction formal: separator-denominator hardness is only an upper-bound falsifier, not a valid lower-bound certificate for H_N. The surviving route is direct C(H_N) lower bounds or a nonrelativizing locality-extraction theorem with explicit threshold loss.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The branch risks treating separator hardness as a source lower bound. A concrete planted-control oracle tests whether the intended extraction is merely semantic and relativizing.
- Situation seed: Oracle world O: G_N^O outputs N^q length-L CNFs; position 0 is T_{b(x)} where T_1 is trivially satisfiable and T_0 is contradictory, while other positions are hard-looking SAT^O instances.
- Varied variable: control leakage size k: from one oracle bit b(x), to N^alpha advised controls, to no control.
- Held-fixed controls: d>1 polylog query length and high-q window (1+epsilon)/2<q<1+epsilon, rho<1+epsilon and the same target substitution accounting, one-sided separator definition and D N^sigma log N+EN charging
- Expected observation: For k=1, H_N is easy but local separator denominators can stay large; as k goes to zero the obstruction disappears only if real SAT syntax supports extraction.
- Transfer certificate needed: A valid certificate must prove a nonrelativizing extractor using real SAT witnesses or self-reductions, with loss N^{o(1)}, and must explicitly fail in the planted-control oracle.

## Next Experiment

Try to formulate a real-SAT locality extractor using witness self-reducibility: from a small circuit for H_N, isolate a generated satisfiable query and build a one-sided predicate; audit algebrization and N^{o(1)} loss.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

A total-influence lower bound for SAT_m transfers to AC0_d[m^k] only above the Boppana influence ceiling; it cannot transfer to unrestricted SIZE(m^k), since PARITY_m is in SIZE(O(m)) and has maximal influence m.

## Definitions

- source object: Boolean slice f_m=SAT_m:{0,1}^m->{0,1} under a fixed honest total encoding; route claims a lower bound on total influence I(f_m).
- target object: T_{d,k}=AC0 depth d size m^k, or T_k=SIZE(m^k) for the rejected extrapolation.
- controlled interface: every target circuit C in T must satisfy an a priori influence ceiling B_T(m,k,d), with no change of input encoding or padding.
- target-preserving condition: prove I(SAT_m)>B_T on the same m-bit slice; padding, promise restriction, and advice bits must not hide measured coordinates.
- AC0 ceiling uses De Morgan basis, unbounded fan-in, fixed depth d, and size s=m^k.
- For unrestricted circuits, parity is small and maximally influential, so any threshold using only I(f) is not useful.

## Assumptions

- SAT_m is totalized by rejecting malformed encodings; all influence is measured over the resulting m input bits.
- Truth-table constructivity for the audit costs poly(N) with N=2^m; this makes high-influence predicates natural when their density is polynomial.
- The lemma is a target gate, not a claim that the needed SAT influence lower bound is known.

## Equations

- influence_ceiling: `I(f)=\sum_{i=1}^{m}\Pr_x[f(x)\ne f(x\oplus e_i)]\le m`. Valid when: Valid when f is a total Boolean function on exactly m measured input coordinates.
- ac0_boppana_bound: `C\in AC0_d[s]\Rightarrow I(C)\le c_d(\log s)^{d-1}=O_d((k\log m)^{d-1})`. Valid when: Valid for fixed-depth AC0 over the De Morgan basis with unbounded fan-in and size s=m^k.
- restricted_transfer: `I(SAT_m)>c_d(k\log m)^{d-1}\Rightarrow SAT_m\notin AC0_d[m^k]`. Valid when: Applies after the SAT encoding is fixed and the influence ceiling holds for every candidate AC0 circuit on that slice.

## Attempted Derivation

- Fix the total SAT_m encoding and define I on the same m coordinates; a lower bound L_m excludes exactly target classes with B_T(m)<L_m.
- For AC0_d[m^k], use the Boppana average-sensitivity bound B_T=O_d((k log m)^{d-1}); a super-polylog influence lower bound would be a valid restricted lower bound.
- Try T=SIZE(m^k). PARITY_m lies in SIZE(O(m)) subset SIZE(m^k) for k>=1 and has I=m, while every Boolean function has I<=m.
- Thus any influence threshold rejecting all SIZE(m^k) circuits must exceed m, impossible; the route is quarantined for P-vs-NP transfer.

Blocking gap: Need a SAT-specific influence lower bound under an honest encoding for the AC0 consequence; no gap remains for SIZE transfer because parity is the decisive falsifier.

## Falsifiers

- PARITY_m is a falsifier for SIZE transfer: linear-size circuits attain I=m, so high influence cannot be useful against polynomial size.
- Padding falsifier: H(x,z)=SAT_m(x) on M=m+m^beta bits preserves raw core influence but changes normalized influence and size thresholds.
- Encoding falsifier: duplicate, checksum-heavy, or sparse-valid encodings can alter coordinate influence without changing the language.
- Threshold-gate falsifier: MAJ_m has I=Theta(sqrt(m)) in tiny TC0, so influence ceilings must name the target basis precisely.

## Learning

Cycle 48 isolates a valid quantitative target gate: total influence can prove AC0 lower bounds only above O_d((k log m)^{d-1}), while transfer to unrestricted SIZE fails exactly at the universal ceiling m due small parity. This is route-level barrier progress, not P != NP progress.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and threshold calibration.`
- Rationale: Influence arguments are tempting because they are explicit truth-table statistics; the thought experiment tests whether padding preserves the claimed target lower bound.
- Situation seed: Padded SAT family H_{m,beta}(x,z)=SAT_m(x) with z ignored, total length M=m+ceil(m^beta), compared against AC0_d[M^k] and SIZE[M^k].
- Varied variable: Padding exponent beta.
- Held-fixed controls: Fixed total SAT encoding on the core x bits., Fixed AC0 depth d, De Morgan basis, and size exponent k., No advice and no promise restriction; all M coordinates are measured., Target consequence remains a lower bound for circuits on the padded input length M.
- Expected observation: Raw influence stays I(SAT_m), normalized influence falls by m/M, AC0 ceiling becomes O_d((k log M)^{d-1}), and unrestricted SIZE remains killed by PARITY_M.
- Transfer certificate needed: A valid bridge must specify raw versus normalized influence and prove a compiler ceiling B_T(M) on the same coordinates; padding must be removable by projection without exceeding the target threshold.

## Next Experiment

Audit noise-sensitivity or Fourier-tail routes with the same parity, majority, and padding threshold tests before allowing any P-vs-NP transfer claim.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Succinct bit-decoder collapse for explicit selector repairs: let I_m={T_{m,j}:j<M_m} be a low-image MCSP carrier with M_m<=2^{D m} and threshold s_m=2^{epsilon m}. If a bit decoder B_m(j,x)=T_{m,j}(x) has unrestricted circuits of size 2^{gamma m+o(m)} with gamma<epsilon, then every decoded row is below the intended MCSP no-side threshold. Hence standard PRG, k-wise, NW, local-code, or lexicographically unranked selectors with succinct random access are a falsifier for this source route, not a valid source theorem.

## Definitions

- source object: an E-uniform low-image family of truth tables T_{m,j}:{0,1}^m->{0,1}, with j in [M_m] and M_m<=2^{D m}.
- target object: the padded aggregate E language A(j,x,pad)=T_{m,j}(x) on length n=kappa(1+D)m+O(1).
- controlled interface: a bit decoder B_m taking row index j and input x, plus a streaming verifier only if it does not give subthreshold random access.
- target-preserving condition: the same unrestricted circuit model, no advice in length selection, fixed constants D, epsilon, kappa, and padding that preserves the exponent conversion.

## Assumptions

- D, epsilon, gamma, and kappa are fixed positive constants with epsilon<1.
- MCSP size is measured by unrestricted Boolean circuits over m input bits.
- The row index j may be hardwired when upper-bounding the circuit complexity of a single row.
- The decoder family is nonuniform for the upper-bound falsifier; uniformity only strengthens the invalidation.

## Equations

- image_and_threshold: `M_m \le 2^{D m},\qquad s_m=2^{\epsilon m}.`. Valid when: Valid when image entropy D and MCSP threshold epsilon are fixed constants independent of m.
- decoder_to_row_upper_bound: `\operatorname{CKT}(T_{m,j}) \le \operatorname{size}(B_m)+O(Dm+m).`. Valid when: Valid when B_m computes every requested table bit and the row index j may be hardwired as nonuniform constants.
- succinct_decoder_collapse: `\operatorname{size}(B_m)\le 2^{\gamma m+o(m)},\ \gamma<\epsilon \ \Longrightarrow\ \max_j \operatorname{CKT}(T_{m,j})<2^{\epsilon m}\ \text{for large }m.`. Valid when: Applies when the decoder upper bound is measured in the same unrestricted circuit model as the MCSP threshold.
- padded_decoder_ceiling: `n=\kappa(1+D)m+O(1),\qquad q_{\mathrm{ceiling}}=\frac{\gamma}{\kappa(1+D)}.`. Valid when: Requires padded aggregate input length to include the row index and to preserve the declared kappa length balance.

## Attempted Derivation

- Start from the valid random calibration: 2^{D m} independent rows almost surely avoid every sparse-correction ball around circuits of size 2^{epsilon m}/4.
- Try to replace the random rows by a seed-efficient generator G_m:{0,1}^{D m}->{0,1}^{2^m} using k-wise independence, an NW design, or a locally computable code; define T_{m,j}=G_m(j).
- Observe that every standard derandomized generator exposes a bit decoder B_m(j,x)=G_m(j)_x of size poly(m) or at worst 2^{gamma m} with gamma<epsilon.
- Hardwire j into B_m. This gives circuits for every selected row below 2^{epsilon m}, contradicting the intended MCSP no-side claim before extraction starts.
- To avoid the contradiction, demand decoder circuit exponent at least epsilon-o(1). But then proving the generator has a hard row proves the aggregate decoder lower bound, which is exactly the target-preserving E lower bound after padding.

Blocking gap: No known construction supplies an E-uniform low-D selector whose rows are robustly outside all subthreshold correction balls while its indexed bit relation lacks subthreshold circuits. Standard pseudorandomness repairs are too locally explicit; sequential-only repairs still need an E bit algorithm for the aggregate target.

## Falsifiers

- Any k-wise independent, NW, algebraic-code, or PRG selector with bit decoder size 2^{gamma m} for gamma<epsilon is a source falsifier.
- A lex-first table outside the bad-ball union is not valid unless its bit predicate is E-computable without enumerating 2^{Theta(2^{epsilon m})} circuits.
- A dense E-decidable property excluding small circuits would be a natural-proofs barrier interaction, not an acceptable non-large carrier certificate.
- Nonuniform advice choosing a good row destroys the target-preserving condition and yields only a nonuniform leakage statement.
- If D or kappa makes epsilon/(kappa(1+D)) vanish, the extraction threshold collapses even from a valid hard row.
- Aggregate evidence in a restricted or uniform circuit model does not certify MCSP no-side hardness against unrestricted circuits.

## Learning

Cycle 48 identifies the exact failure mode of the tempting repair from random bad-ball avoidance to explicit selectors. The combinatorial carrier exists with overwhelming probability, but derandomizing it by any succinct local decoder makes every row circuit-easy. A valid source must be low-D, no-advice, non-natural, and decoder-hard; otherwise the route either has a concrete falsifier or has already proved the aggregate lower bound it wanted to extract.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The branch has a valid random existence calculation but no explicit selector. A concrete selector experiment tests whether derandomization can preserve MCSP hardness without leaking a small decoder circuit.
- Situation seed: For each m, instantiate a seeded low-image family T_{m,j}=G_m(j) with j in {0,1}^{D m}; require every target row to avoid radius 2^{epsilon m}/Theta(m) correction balls around circuits of size 2^{epsilon m}/4, and extract the padded aggregate A(j,x)=G_m(j)_x.
- Varied variable: The local decoder circuit exponent gamma in size(B_m)<=2^{gamma m+o(m)} for B_m(j,x)=G_m(j)_x.
- Held-fixed controls: MCSP threshold s_m=2^{epsilon m} in unrestricted circuits., Image entropy D and padding loss kappa are fixed constants., No advice and no nonuniform length selector are allowed., The aggregate language must be E-uniform and length-balanced., Robust bad-ball radius remains Theta(2^{epsilon m}/m).
- Expected observation: When gamma<epsilon, every selected row has a subthreshold circuit, so the selector is invalid despite any pseudorandom-looking distribution. Only gamma>=epsilon can survive, and then the decoder itself carries the desired lower bound at exponent epsilon/(kappa(1+D)).
- Transfer certificate needed: A formal proof that the E-uniform aggregate bit relation has no circuits below 2^{epsilon m-o(m)}, obtained by a non-natural and no-advice invariant, or a new interface avoiding random-access leakage while still computing A in E.

## Next Experiment

Analyze sequential emitters whose random access is E-computable only by recomputation: compute their best checkpoint/restart circuit exponent gamma_seq and test whether gamma_seq can exceed the required epsilon while keeping aggregate computation in E.
