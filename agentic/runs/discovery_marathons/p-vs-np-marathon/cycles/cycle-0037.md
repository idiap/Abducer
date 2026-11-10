# cycle-0037

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: approximate witness-cover gate

## Candidate Lemma

For the generated-OR carrier, any small approximate position-indexed assignment cover gives a subthreshold general-circuit upper bound for H_N. Thus a valid N^{1+epsilon-o(1)} source lower bound must defeat all such nonuniform covers, not only global promise SAT solvers or shared unary predicates.

## Definitions

- source object: H_N:{0,1}^N -> {0,1}, H_N(x)=OR_{j<=M_N} SAT(F_{N,j}(x)), M_N=N^q, formula length L_N=(log N)^d, and the full list (F_{N,j}(x))_j is produced by a multioutput generator G_N of size N^{rho+o(1)}.
- target object: SAT on L_N-bit formulas; the target consequence remains SAT notin P/poly if a valid H_N lower bound exceeds N^{1+epsilon-o(1)} while q,rho<1+epsilon.
- controlled interface: target SAT circuits may be substituted only into the generated L_N-bit queries; source-side leakage is charged as position-indexed nonuniform assignment sets A_{N,j} and equality corrections.
- target-preserving condition: d>1, q,rho<1+epsilon, q>(1+epsilon)/2 for the high-q repair, the source model is nonuniform SIZE on N-bit inputs, and all generator, cover, and patching costs are counted before claiming magnification.

## Assumptions

- Each F_{N,j}(x) encodes a standard CNF or verifier instance whose evaluation on a proposed assignment costs L_N^{O(1)} gates after the formula bits are generated.
- There are nonuniform sets A_{N,j} of assignments with total size W_N=sum_j |A_{N,j}|.
- The cover misses at most E_N positive inputs: for all but E_N strings x with H_N(x)=1, some j and some a in A_{N,j} satisfy F_{N,j}(x).
- Equality circuits for the exceptional missed inputs are allowed in the upper-bound falsifier, costing O(N E_N) gates.

## Equations

- carrier: `H_N(x)=\bigvee_{j\le M_N} SAT(F_{N,j}(x)),\quad M_N=N^q,\quad L_N=(\log N)^d.`. Valid when: Valid when the source carrier is the generated-OR family with explicit multioutput generation and fixed polynomially many indexed queries.
- cover_predictor: `B_A(x)=\bigvee_{j\le M_N}\bigvee_{a\in A_{N,j}} Eval(F_{N,j}(x),a).`. Valid when: Valid when A_{N,j} is position indexed and Eval tests satisfaction for the generated formula encoding.
- upper_bound: `SIZE(H_N)\le N^{\rho+o(1)}+N^{q+o(1)}+L_N^{O(1)}W_N+O(NE_N).`. Valid when: Applies when the cover predictor is corrected by hardwired equality tests for all uncovered positive inputs.
- necessary_threshold: `\max\{\rho,q,\omega,1+\eta\}\ge 1+\epsilon-o(1),\quad W_N=N^{\omega+o(1)},\ E_N=N^{\eta+o(1)}.`. Valid when: Requires comparing the explicit upper bound against a claimed N^{1+epsilon-o(1)} lower bound in general circuits.

## Attempted Derivation

- Fix nonuniform assignment sets A_{N,j} and build B_A(x) by evaluating each generated formula F_{N,j}(x) on all assignments in A_{N,j}.
- Use the multioutput generator once, costing N^{rho+o(1)}, and share its formula bits across all assignment evaluations.
- Each assignment evaluation costs L_N^{O(1)}, so the total certificate-test cost is L_N^{O(1)}W_N plus the final OR over M_N positions.
- If B_A misses E_N positive inputs of H_N, add equality tests for those N-bit inputs and OR them into B_A, costing O(N E_N).
- The resulting circuit computes H_N exactly with size N^{rho+o(1)}+N^{q+o(1)}+L_N^{O(1)}W_N+O(N E_N).
- Therefore any claimed N^{1+epsilon-o(1)} lower bound for H_N implies the necessary exponent inequality max{rho,q,omega,1+eta}>=1+epsilon-o(1).

Blocking gap: No explicit generated-OR family is known to have approximate position-indexed witness-cover complexity above this threshold, and defeating witness covers is still weaker than defeating arbitrary position-indexed unary predicates plus residual circuits.

## Falsifiers

- falsifier: exact per-position assignment hitting sets with total W_N<N^{1+epsilon-delta}.
- falsifier: approximate witness covers with W_N<N^{1+epsilon-delta} and fewer than N^{epsilon-delta} missed positive inputs.
- falsifier: planted-solution or low-witness-entropy generated ranges where one small assignment list hits every satisfiable formula in each position range.
- falsifier: nonuniform advice choosing A_{N,j} separately for every N and j; this leakage is valid in the source SIZE model and must be charged.
- falsifier: generator implementation whose full multioutput cost already reaches N^{1+epsilon}, destroying the target-preserving threshold.

## Learning

Cycle 37 sharpens the position-indexed unary residual obligation into an approximate witness-cover threshold. In the high-q generated-OR route, dense tuple leakage is threshold-blocked, but unary assignment covers of total size below N^{1+epsilon} plus fewer than N^epsilon missed positives still give exact circuits for H_N after equality patching. This is route-level progress: a valid candidate source lower bound must first prove high approximate witness-cover complexity, while the main P != NP conjecture remains untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for candidate generated-OR carriers.`
- Rationale: The route now hinges on whether high-q generated SAT bags have large position-indexed witness-cover complexity; another abstract residual restatement would not test the new threshold.
- Situation seed: Take M=N^q generated 3CNF formulas of length L=(log N)^d with d>1. For each position j, the generator ranges over formulas with planted satisfying assignments drawn from a position-dependent set of size N^h, while unsatisfiable formulas are also included to keep label balance.
- Varied variable: The varied variable is h=log_N of the minimum per-position witness hitting set size, equivalently W_N=N^{q+h+o(1)} for the whole generated list.
- Held-fixed controls: q is fixed in ((1+epsilon)/2,1+epsilon) so dense binary tuple leakage is threshold-blocked., rho<1+epsilon and the generator outputs the whole list with no uncharged advice., L=(log N)^d with d>1 so exhaustive truth-table lookup remains superthreshold., The target bridge uses only substitution of fixed-exponent SAT circuits into generated queries.
- Expected observation: If h<1+epsilon-q, the witness-cover circuit computes H_N below the source threshold, giving a concrete falsifier. If h exceeds 1+epsilon-q even after allowing N^{epsilon-o(1)} misses, this carrier passes the new necessary audit but still needs arbitrary unary residual hardness.
- Transfer certificate needed: Before the intuition can affect proof obligations, prove a uniform-to-nonuniform certificate that every position-indexed assignment cover with W_N<N^{1+epsilon-o(1)} leaves at least N^{epsilon-o(1)} unpatchable positive inputs, and then lift the certificate from assignment covers to arbitrary unary formula predicates.

## Next Experiment

Instantiate the thought experiment with a concrete planted/anti-planted CNF generator and compute the minimum position-indexed assignment hitting exponent h for its satisfiable range; compare h to 1+epsilon-q.

# Barrier-Aware Lower-Bound Route: SOS Degree Target Gate

## Candidate Lemma

Linear or superconstant SOS/Lasserre degree lower bounds for explicit unsatisfiable 3-XOR/Tseitin systems are valid lower bounds only for the named semialgebraic hierarchy. They do not transfer to P != NP without an additional uniform p-simulation of polynomial-time refuters by polynomial-size or low-degree SOS proofs.

## Definitions

- source object: an unsatisfiable constant-width XOR/Tseitin CNF or 0-1 polynomial system F_N with N variables/constraints and real SOS degree Deg_SOS(F_N).
- target object: degree-d SOS/Lasserre refutations and the associated SDP algorithms with standard monomial moment matrix, not arbitrary deterministic polynomial-time deciders.
- controlled interface: a claimed bridge from Deg_SOS(F_N)>d(N) to no polynomial-time refutation must supply a uniform p-simulation map from any P refuter to SOS proofs preserving size, degree, and encoding.
- target-preserving condition: the encoding must preserve unsatisfiability, uniform constructibility, degree thresholds, and the target class; replacing P by a weaker SDP hierarchy must be stated explicitly.

## Assumptions

- Use the standard real polynomial encoding x_i^2=1 and XOR constraints x_i x_j x_k=b for b in {+1,-1}.
- Known Grigoriev/Schoenebeck-style pseudoexpectations give Deg_SOS(F_N)=Omega(N) for suitable expander or random constant-density unsatisfiable XOR instances.
- The same XOR instances are refutable in polynomial time by Gaussian elimination over F_2.
- Degree lower bounds are audited separately from proof-size lower bounds; degree-d Lasserre failure is not a lower bound against all P algorithms.

## Equations

- monomial_dimension: `M(N,d)=\sum_{i=0}^{d}\binom{N}{i}\le (eN/d)^d`. Valid when: Valid when the SOS proof is represented in the standard degree-d monomial basis with 1<=d<=N.
- degree_hierarchy_failure: `Deg_{SOS}(F_N)>d \;\Rightarrow\; F_N \text{ has no degree-}d \text{ SOS refutation}`. Valid when: Applies when the target object is exactly degree-d SOS over the stated real polynomial encoding.
- xor_separation: `Deg_{SOS}(X_N)\ge cN \quad\text{and}\quad X_N\in P \text{ by } rank_{F_2}(A|b)`. Valid when: Requires a high-girth expander or random constant-density unsatisfiable XOR instance satisfying known pseudoexpectation lower-bound hypotheses.
- missing_p_simulation_obligation: `UNSAT\in P \;\Rightarrow\; \forall F\in UNSAT_N\;\exists \pi\;[\pi \text{ is SOS and } |\pi|\le N^C]`. Valid when: Valid only as a hypothetical p-boundedness premise; it is not entailed by polynomial-time decision algorithms.

## Attempted Derivation

- Start with an explicit unsatisfiable XOR/Tseitin family X_N with Deg_SOS(X_N)=Omega(N).
- Conclude correctly that level-d Lasserre and degree-d SOS fail for every d<cN.
- Use M(N,d) to infer that standard dense SDP search needs N^{Omega(d)} time when d grows.
- Observe the blocking falsifier: X_N is refutable in polynomial time by Gaussian elimination over F_2.
- Try to lift the hierarchy lower bound to P != NP by asserting that every polynomial-time refutation has a polynomial-size SOS certificate.
- Audit the assertion: no known theorem p-simulates arbitrary P refuters by SOS, and XOR gives evidence against low-degree simulation.

Blocking gap: The missing bridge is a uniform, target-preserving p-simulation from P-time UNSAT refuters to polynomial-size or bounded-degree SOS proofs. Degree lower bounds alone only separate SOS/Lasserre from Gaussian elimination.

## Falsifiers

- falsifier: unsatisfiable constant-density 3-XOR is P-refutable by Gaussian elimination while requiring linear SOS/Lasserre degree in known regimes.
- falsifier: padding X_n to length N=n^alpha preserves the P decider and weakens the exponent to N^{1/alpha}, so exponent tuning cannot create a P lower bound.
- falsifier: a high-degree lower bound may fail to imply polynomial proof-size lower bounds unless the proof-size measure and monomial representation are explicitly fixed.
- falsifier: any route claiming semialgebraic lower bounds against P must explain why Gaussian elimination is not an allowed target algorithm.

## Learning

Cycle 37 certifies a semialgebraic proof-complexity gate: linear SOS/Lasserre degree lower bounds are valid hierarchy separations, but P-easy high-degree XOR instances are a concrete falsifier to any direct transfer to P != NP. The missing object is a uniform p-simulation from P refuters to SOS, not another hardness slogan.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch just audited resolution width; the next concrete barrier-adjacent object is SOS degree. A P-easy high-SOS-degree XOR family directly tests whether the route preserves the target P rather than only a proof hierarchy.
- Situation seed: Take an explicit expander Tseitin or random constant-density unsatisfiable 3-XOR instance X_n, encode it as real {+-1} polynomial constraints, then form Pad_alpha(X_n) of total length N=n^alpha by adding isolated dummy variables and tautologies.
- Varied variable: padding exponent alpha, equivalently the inherited SOS degree exponent delta=1/alpha in the padded length N.
- Held-fixed controls: The XOR core remains uniformly recoverable and unsatisfiable., The target proof model remains standard real degree-d SOS/Lasserre., The polynomial-time Gaussian-elimination refuter is allowed in the ambient P target., No nonuniform advice is introduced by the padding map.
- Expected observation: For every alpha>1, the padded family still has a P refuter but only yields Deg_SOS >= Omega(N^{1/alpha}). This separates Lasserre runtime thresholds from P-time decidability and exposes threshold collapse under padding.
- Transfer certificate needed: Before the intuition may affect P-vs-NP obligations, one needs a uniform p-simulation theorem converting every P refuter for the padded encoding into polynomial-size or low-degree SOS proofs, or a proof that the intended target is only the SOS/Lasserre hierarchy.

## Next Experiment

Audit polynomial calculus and Nullstellensatz over characteristic-mismatched encodings: identify when algebraic degree lower bounds are only field/proof-system separations and find the Gaussian-elimination falsifier threshold.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Low-image aggregate row forcing is valid only for unrestricted nonuniform circuit lower bounds. If every row of a canonical MCSP carrier has circuits of size at most 2^{epsilon m}, then the aggregate ranked decoder has a nonuniform multiplexer circuit of size 2^{(D+epsilon)m+o(m)}. Hence an aggregate lower bound forces an MCSP-hard row only above q_force=(D+epsilon)/(1+D) and only in a circuit model closed under arbitrary row multiplexing.

## Definitions

- source object: an E-uniform low-image MCSP carrier A_m(r,x) with row length 2^m, rank set size R_m<=2^{D m+o(m)}, and claimed row threshold s_m=2^{epsilon m}.
- target object: an E language obtained by padded row/rank multiplexing whose nonuniform circuit lower-bound exponent is any delta<epsilon/(kappa(1+D)) after an actual hard row is forced or directly certified.
- controlled interface: aggregate lower-bound to row-hardness transfer through unrestricted R_m-way nonuniform circuit multiplexing, not through uniform decoder hardness or restricted-model hardness.
- target-preserving condition: the aggregate lower bound must be against unrestricted Boolean circuits and must exceed the all-small-rows multiplexer upper bound; otherwise no MCSP no-side row is forced.

## Assumptions

- Rows T_{m,r}(x)=A_m(r,x) are indexed by a canonical E-uniform distinct-image unranking procedure.
- MCSP hardness means ordinary nonuniform Boolean circuit size, not time-bounded uniform hardness.
- The lower-bound model for A_m permits hardwiring all row circuits and rank equality tests with only O(R_m poly(m)) overhead.
- epsilon>0 is constant, D>=0 is the distinct-image entropy rate, and kappa>=1 is the padding density loss from source lengths to target lengths.
- Any aggregate-forcing argument must respect the verifier/access cap alpha_A; exceeding the cap is a quantitative threshold-collapse falsifier.

## Equations

- image-rate: `R_m \le 2^{D m+o(m)},\quad L_m=m+\lceil \log_2 R_m\rceil=(1+D)m+o(m)`. Valid when: Valid when the carrier image is E-canonically unranked and duplicate certificates have already been quotiented.
- all-small-rows-upper-bound: `[\forall r\ C(T_{m,r})\le 2^{\epsilon m}]\ \Rightarrow\ C(A_m)\le O(R_m(2^{\epsilon m}+\mathrm{poly}(m)))\le 2^{(D+\epsilon)m+o(m)}`. Valid when: Valid when the aggregate circuit model is unrestricted nonuniform Boolean circuits with rank multiplexers available.
- aggregate-forcing-threshold: `q_{\mathrm{force}}=\frac{D+\epsilon}{1+D},\quad C(A_m)>2^{(q_{\mathrm{force}}+\eta)L_m}\Rightarrow \exists r\ C(T_{m,r})>2^{\epsilon m}`. Valid when: Applies after the aggregate lower bound is nonuniform, unrestricted, and has constant slack eta>0.
- cap-feasibility: `q_{\mathrm{force}}\le \alpha_A\ \Longleftrightarrow\ D\le \frac{\alpha_A-\epsilon}{1-\alpha_A}`. Valid when: Requires a declared source-method cap alpha_A below one and epsilon at most alpha_A.
- extracted-E-exponent: `\delta<\frac{\epsilon}{\kappa(1+D)}`. Valid when: Applies after a hard row is found or forced and padding preserves E-uniformity without advice.

## Attempted Derivation

- Assume for contradiction that every distinct row T_{m,r} has an unrestricted circuit C_r of size at most s=2^{epsilon m}.
- Build a nonuniform aggregate circuit: on input (r,x), compute equality to each rank i, evaluate C_i(x), and OR the gated outputs.
- The size is O(R_m(s+poly(m+log R_m)))=2^{(D+epsilon)m+o(m)} under R_m<=2^{Dm+o(m)}.
- Therefore an unrestricted lower bound for A_m above this size forces at least one row with circuit complexity greater than 2^{epsilon m}.
- Measured in aggregate input length L_m=(1+D)m+o(m), the needed exponent is q_force=(D+epsilon)/(1+D).
- Combining with kappa-padding gives target E lower-bound exponent delta<epsilon/(kappa(1+D)) once the hard row is actual, E-canonical, and advice-free.
- The derivation fails for uniform-only lower bounds because the multiplexer hardwires all row circuits and is inherently nonuniform.

Blocking gap: No current source theorem supplies either a direct hard-row MCSP certificate or an unrestricted nonuniform aggregate lower bound above q_force while staying below the declared cap alpha_A.

## Falsifiers

- Uniform aggregate hardness is only rank-index hardness; the index-coded constant-row construction is a falsifier for that shortcut.
- The aggregate lower-bound model is restricted and lacks closure under arbitrary row-circuit multiplexing.
- q_force=(D+epsilon)/(1+D) exceeds the source cap alpha_A, causing quantitative threshold collapse.
- The carrier uses a nonuniform selector for a hard row instead of E-canonical unranking or multiplexing.
- The source restores density by salt or random padding, creating a large constructive property and triggering the natural-proofs obstruction under standard PRF assumptions.
- A ranked random-access decoder below 2^{epsilon m-o(m)} gives small circuits for rows and invalidates MCSP no-side soundness.
- The claimed lower bound is relativizing or oracle-uniform only; it does not contradict the nonuniform all-rows-small multiplexer.

## Learning

Cycle 37 isolates a hidden model mismatch: aggregate row forcing is a nonuniform unrestricted statement. Uniform decoder hardness, restricted-circuit lower bounds, or index hardness do not certify MCSP rows. The exact gate is q_force=(D+epsilon)/(1+D) with cap condition D<=(alpha_A-epsilon)/(1-alpha_A).

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe.`
- Rationale: The branch must distinguish genuine row MCSP hardness from aggregate rank complexity; another abstract bridge restatement would miss the nonuniform leakage point.
- Situation seed: Index-coded aggregate carrier: for each m choose a rank language H_m on d=ceil(Dm) bits hard for a chosen uniform decoder, and define A_m(r,x)=H_m(r). Every row is constant, but the aggregate can look hard to the uniform decoder.
- Varied variable: Distinct-image entropy D, equivalently rank length d=Dm, with epsilon, kappa, and alpha_A fixed.
- Held-fixed controls: MCSP target is unrestricted nonuniform circuit size greater than 2^{epsilon m}., Emitter and distinct-image unranking remain E-uniform and advice-free., Padding loss kappa is constant and target-preserving., No random salt or dense natural property repair is allowed.
- Expected observation: As D grows, uniform aggregate hardness can increase while every row remains O(1)-circuit; only an unrestricted nonuniform aggregate lower bound above q_force can refute all-small rows.
- Transfer certificate needed: A named nonuniform circuit lower bound C(A_m)>2^{(q_force+eta)L_m} with multiplexer closure, or a direct sound row-hardness certificate, plus q_force<=alpha_A and E-canonical row recovery.

## Next Experiment

Audit the D=0 and D=o(1) regimes for direct row certificates: can any sparse non-natural proof object certify one row above 2^{epsilon m} without random access, advice, or a dense constructive property?
