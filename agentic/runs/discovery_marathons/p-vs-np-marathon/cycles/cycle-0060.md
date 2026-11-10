# cycle-0060

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Constructive Label-Free Sketch Gate for XOR Magnification

## Candidate Lemma

For the polylog-query XOR-SAT carrier, constructively label-free sparse quotient-polynomial sketches are valid upper-bound falsifiers, while the target bridge remains max{rho,q}<1+epsilon. If such a sketch has S_T+A_N r_N+E_N N<N^{1+epsilon-o(1)}, then the claimed source lower bound C(H_N)>N^{1+epsilon} is false. If the source lower bound is proved directly for infinitely many N under the same parameters, then SAT is not in P/poly.

## Definitions

- source object: H_N:{0,1}^N -> {0,1} is the XOR of m_N=N^q generated SAT instances F_{N,j}(x) of length L_N=(log N)^d; the source model is nonuniform Boolean circuits SIZE and the weak lower bound is C(H_N)>N^{1+epsilon}.
- target object: Boolean SAT on formulas of length n; the target consequence is SAT notin SIZE(n^c) for every constant c, hence NP not subset P/poly by standard nonuniform completeness.
- controlled interface: a generator G_N of size N^{rho+o(1)} produces the m_N query formulas, and target SAT circuits are substituted only at these generated query sites with every N^q, N^rho, and L_N^c cost charged.
- target-preserving condition: d>1 and max{rho,q}<1+epsilon; every transcript used as a source falsifier is constructively label-free, excluding SAT truth labels, a circuit for H_N, or output-dependent advice.
- constructively label-free transcript: T_N is produced by a fixed syntactic compiler from N, G_N, and named quotient/incidence maps; its description is not chosen using the SAT truth vector y_N or the truth table of H_N.
- sparse quotient-polynomial sketch: P_N over F_2 has support A_N in its algebraic normal form and is evaluated on r_N transcript bits; coefficients may be nonuniform advice depending on real SAT labels, making the upper-bound falsifier stronger.

## Assumptions

- G_N outputs m_N=N^q formulas of length L_N=(log N)^d and has circuit size N^{rho+o(1)} including addressing overhead.
- The incidence vector a_N(x) records generated formulas modulo two in the finite generated universe U_N, and y_N is the SAT truth vector on U_N.
- T_N:{0,1}^N -> F_2^{r_N} has total circuit cost S_T and is constructively label-free.
- P_N(T_N(x)) agrees with H_N(x) except on at most E_N seeds, and exceptional seeds may be patched by equality gates of cost O(E_N N).

## Equations

- xor-incidence-form: `H_N(x)=\bigoplus_{j=1}^{m_N}\mathrm{SAT}(F_{N,j}(x))=\langle a_N(x),y_N\rangle_{\mathbb F_2},\quad m_N=N^q,\quad L_N=(\log N)^d.`. Valid when: Valid when G_N outputs m_N length-L_N formulas and a_N records their mod-two incidences in the generated universe.
- label-free-sketch-upper-bound: `C(H_N)\le S_T+O(A_N r_N+E_N N).`. Valid when: Valid when T_N is constructively label-free, P_N has A_N monomials, and equality gates patch exactly E_N exceptional seeds.
- target-substitution-upper-bound: `\mathrm{SAT}\in \mathrm{SIZE}(n^c)\ \Longrightarrow\ C(H_N)\le N^{\rho+o(1)}+N^q L_N^c=N^{\max\{\rho,q\}+o(1)}.`. Valid when: Applies after the generator has size N^{rho+o(1)} and every generated query has polylogarithmic length L_N.
- magnification-threshold: `C(H_N)>N^{1+\epsilon}\ \text{i.o.}\ \land\ \max\{\rho,q\}<1+\epsilon\ \Longrightarrow\ \mathrm{SAT}\notin \mathrm{P/poly}.`. Valid when: Requires the lower bound to hold infinitely often against nonuniform circuits and fixed q,rho below the threshold.

## Attempted Derivation

- Write H_N as the F_2 inner product of the generated incidence vector a_N(x) with the SAT label vector y_N.
- Assume a subthreshold circuit D_N of size N^{1+epsilon-delta} computes H_N and try to use its gate transcript as T_N with P_N equal to the final gate.
- This immediately violates label-freeness: D_N may encode information about y_N or about the carrier truth table, even if it never explicitly queries SAT.
- Try expanding D_N as an algebraic normal form over seed bits or incidence coordinates; the support can blow up to 2^{S} and gives no N^{1+epsilon} threshold preservation.
- Try quotienting incidences by syntactic SAT-preserving symmetries; this gives useful upper-bound falsifiers but not an extraction from arbitrary circuits.

Blocking gap: No theorem converts an arbitrary small circuit for the parity of SAT labels on generated queries into a constructively label-free low-support incidence sketch with subthreshold residual cost.

## Falsifiers

- Output-dependent transcript leakage: T_N=H_N makes sparse-sketch hardness vacuous.
- SAT-label advice in the transcript compiler below the tested threshold invalidates label-freeness.
- Constructively label-free T_N with S_T+A_N r_N+E_N N<N^{1+epsilon-o(1)} is a direct source lower-bound falsifier.
- Symmetry-pair cancellation after SAT-preserving quotienting can make a high-entropy XOR carrier constant or sparse.
- Threshold collapse occurs if max{rho,q}>=1+epsilon, since SAT substitution no longer contradicts the source lower bound.
- Lookup collapse reappears for d<=1 when the generated truth-table cost can fall below the claimed source threshold.
- A relativizing extraction attempt is blocked if small H_N circuits use oracle/advice correlations not recoverable from incidence structure.

## Learning

Cycle 60 separates two notions previously conflated. Sparse quotient-polynomial sketches are valid upper-bound falsifiers only when the transcript is constructively label-free; otherwise T_N=H_N collapses the audit. The target bridge max{rho,q}<1+epsilon survives, but sketch-hardness is not a source lower bound without a nonrelativizing extraction theorem or a direct C(H_N) lower bound.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The route now hinges on whether label-free is a mathematically enforceable interface or just a verbal ban on T=H_N. A concrete leakage experiment tests the exact threshold at which the sketch audit collapses into the original circuit lower bound.
- Situation seed: High-q XOR-SAT carrier with L_N=(log N)^2, q in ((1+epsilon)/2,1+epsilon), rho<1+epsilon, and H_N(x)=xor_j SAT(F_{N,j}(x)); transcripts are generated by a compiler that may receive b_N bits of auxiliary advice.
- Varied variable: Advice leakage exponent alpha where b_N=N^alpha bits may be used by the transcript compiler.
- Held-fixed controls: The SAT substitution bridge is held fixed with d=2 and max{rho,q}<1+epsilon., The source lower-bound target remains C(H_N)>N^{1+epsilon} against general nonuniform circuits., P_N coefficients may hardwire SAT labels after the label-free transcript is fixed., Equality patching costs E_N N gates and must stay below threshold.
- Expected observation: For alpha near 1+epsilon, any subthreshold circuit for H_N can be placed into the transcript advice, recreating the T=H_N collapse. With alpha=0 or polylog-uniform advice, sketches become genuine upper-bound falsifiers, but extraction from arbitrary H_N circuits becomes the missing nonrelativizing step.
- Transfer certificate needed: An advice-accounted label-free sketch lemma plus a formal compiler-independence condition; promotion further needs a real-SAT extraction theorem mapping every small H_N circuit to a low-advice incidence transcript without threshold loss.

## Next Experiment

Define the first concrete compiler class T^{inc-lin}: T_N(x)=B_N a_N(x) for explicit SAT-preserving quotient matrices B_N of row sparsity polylog N, then compute the minimum S_T+A_N r_N for representing H_N by sparse P_N in the high-q, d=2 regime.

# Cycle 60: Unrestricted branching-program threshold-collapse gate

## Candidate Lemma

Unrestricted deterministic branching-program lower bounds for SAT_m cannot transfer to P or SIZE(m^k) through the standard configuration/circuit simulation: for every k>1 the required BP lower bound exceeds the universal decision-tree ceiling.

## Definitions

- source object: BP(f_m), the minimum size of an unrestricted deterministic branching program computing the total m-bit slice f_m=SAT_m or a padded SAT slice.
- target object: DTIME(m^k) or nonuniform SIZE(m^k) lower bounds for SAT_m; polynomial-size BP lower bounds by themselves target L/poly-like models.
- controlled interface: compile a T-time machine or size-s Boolean circuit for f_m into a branching program, then compare the resulting BP upper bound with the claimed source lower bound.
- target-preserving condition: the compiler bound B_T(m) or B_s(m) must be asymptotically below the proved BP lower bound on the same input length and padding slice, with no advice or promise leakage.

## Assumptions

- BP is unrestricted, deterministic, nonuniform, and queries ordinary input bits.
- Circuits are fan-in two Boolean circuits of size s=m^k unless stated otherwise.
- The transfer uses only the known configuration evaluation of a time-bounded machine or circuit.
- No unproved compression from P computations to polynomial-size branching programs is assumed.

## Equations

- decision_tree_ceiling: `BP(f_m) \le 2^{m+1}-1`. Valid when: Valid when BP is unrestricted and the function is total on all m-bit inputs, so the full decision tree may be used.
- time_to_bp: `f_m \in DTIME(T(m)) \Rightarrow BP(f_m) \le 2^{O(T(m))}\,poly(m,T(m))`. Valid when: Valid for a fixed multitape Turing-machine model whose configurations use O(T(m)) work bits and halt within T(m) steps.
- circuit_to_bp: `f_m \in SIZE(s) \Rightarrow BP(f_m) \le 2^{O(s)}poly(m,s)`. Valid when: Applies after a size-s circuit is evaluated by a deterministic configuration process with O(s) stored gate values and hardwired circuit description.
- pnp_threshold_collapse: `2^{O(m^k)} \gg 2^m \ge BP(SAT_m) \quad (k>1)`. Valid when: Requires the target transfer to use the known exponential circuit-to-BP compiler and compares it with the universal m-bit decision-tree ceiling.

## Attempted Derivation

- Let f_m=SAT_m and suppose a source theorem proves BP(f_m)>L(m).
- To refute SIZE(m^k), contraposition must certify that every size-m^k circuit for f_m yields a branching program of size below L(m).
- The known circuit-to-BP conversion gives only BP(f_m)<=2^{O(m^k)}poly(m).
- Therefore the source lower bound would need L(m)>2^{O(m^k)} for the transfer to be valid.
- But every total m-bit function satisfies BP(f_m)<=2^{m+1}-1, so the needed threshold is impossible for k>1.
- The derivation can validly separate SAT from L/poly if L(m) is superpolynomial, but that is not a P != NP consequence.

Blocking gap: Missing target-preserving compiler from polynomial-time or size-m^k SAT deciders to branching programs of size at most 2^{O(m)} or poly(m); such a compiler would be a major P-to-L/poly compression and is not supplied by the route.

## Falsifiers

- Full decision tree falsifier: every total m-bit function has BP size below 2^{m+1}, so no unrestricted BP lower bound can exceed the 2^{Omega(m^k)} threshold needed for k>1 through the standard compiler.
- Target falsifier: a polynomial BP lower bound for SAT is valid against L/poly-like models but says nothing about polynomial-time algorithms with polynomial workspace.
- Padding falsifier: PadSAT_{ell,beta}(x,z)=SAT_ell(x) preserves NP-hardness under padding while its BP ceiling follows the ell-bit core, eroding any padding-insensitive BP transfer.

## Learning

Cycle 60 isolates unrestricted BP size as a valid carrier for small-space or L/poly lower bounds but not for P != NP. The bridge to P/SIZE requires an exponential-in-m^k BP lower bound, while every m-bit function has BP size O(2^m). This is a quantitative threshold-collapse falsifier, not evidence about the main conjecture.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: Unrestricted BP size has a universal 2^m ceiling, while the P/SIZE transfer through configurations asks for a 2^{m^k} lower bound. A concrete padded slice tests whether the route preserves the target parameter or merely proves a small-space separation.
- Situation seed: PadSAT_{ell,beta}(x,z)=SAT_ell(x) on m=ell^beta input bits, with z ignored and the standard reduction x -> (x,0^{m-ell}).
- Varied variable: padding exponent beta>1
- Held-fixed controls: Source measure is unrestricted deterministic BP size on the total m-bit truth table., Target class is SIZE(m^k) or DTIME(m^k) for a fixed k>1., The reduction preserves SAT hardness syntactically and introduces no promise on padding bits., The only allowed transfer is a named BP compiler with explicit size bound and no hidden advice leakage.
- Expected observation: BP(PadSAT_{ell,beta})<=2^{ell+1}+O(m)=2^{m^{1/beta}+O(log m)}, while the known SIZE(m^k)-to-BP transfer would require a lower bound above 2^{Omega(m^k)}. Increasing beta widens the gap and exposes non-target-preservation.
- Transfer certificate needed: A theorem showing that every SIZE(m^k) or DTIME(m^k) decider for the padded slice induces a BP of size below the proved lower bound, preferably poly(m) or 2^{o(m)}. Without this, the experiment is only a valid falsifier for the BP route.

## Next Experiment

Audit read-k and bounded-width branching programs: compute the exact B_C(m,k,w) compiler thresholds for NC1, logspace, and AC0 targets, and reject any unrestricted P claim without such a certificate.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

A low-distinct-image, E-uniform generated anti-ball MCSP carrier with constant-exponential proof generation yields the same E lower-bound exponent as the earlier multiplexing bridge: for every delta < theta/(kappa(1+D)), the induced language L in E has no circuits of size 2^{delta n} on the target padded lengths. This is valid route-level transfer only, not a proof of P != NP.

## Definitions

- source object: an E-uniform generated anti-ball MCSP carrier {T_{m,r}} with N=2^m truth-table length, distinct row entropy Dm+o(m), and at least one generated row having unrestricted circuit complexity greater than 2^{theta m}.
- target object: a language L in E obtained by multiplexing row rank r and address x, with target lower bound against nonuniform SIZE(2^{delta n}) circuits on kappa-dense padded lengths.
- controlled interface: rank-unranking multiplexing computes L(r,x,pad)=T_{m,r}(x), while proof streams witnessing anti-ball soundness are generated deterministically and never supplied as advice.
- target-preserving condition: row generation and proof generation take 2^{O(m)} time, source lengths are kappa-dense, distinct images have entropy Dm+o(m), and anti-ball soundness is against unrestricted Boolean circuits.

## Assumptions

- For each source length m in a kappa-dense sequence, there are at most M_m=2^{D m+o(m)} distinct generated rows after E-canonical quotienting.
- There exists at least one row r* at length m with C(T_{m,r*})>2^{theta m}; easy contamination among other rows is allowed because multiplexing fixes the hard rank after a hypothetical circuit for L is given.
- The generator is uniform and advice-free; any proof object is produced by the generator in constant-exponential time and is not an external witness to be searched for.
- The target circuit model is unrestricted nonuniform Boolean circuits; restricted lower bounds or uniform-only hardness do not certify MCSP no-side soundness.

## Equations

- row-count: `M_m \le 2^{D m+o(m)}`. Valid when: Valid when duplicates are removed by an E-canonical distinct-image unranking procedure.
- target-length: `n_m=\lceil \kappa(1+D)m\rceil+o(m)`. Valid when: Valid when source length gaps are absorbed only by padding and rank bits.
- source-hardness: `C(T_{m,r^*})>2^{\theta m}`. Valid when: Valid when the anti-ball proof excludes every unrestricted circuit of that size.
- extracted-bound: `C_L(n_m)>2^{\delta n_m}\quad\text{for every }\delta<\theta/(\kappa(1+D))`. Valid when: Applies after fixing rank bits preserves circuit size up to polynomial overhead.
- generation-budget: `t_G(m)\le 2^{\lambda m+o(m)}\quad\text{with constant }\lambda`. Valid when: Requires deterministic generated proof streams and no advice for proof locations.

## Attempted Derivation

- Let U_m be the E-canonical list of distinct generated rows with |U_m|=M_m<=2^{D m+o(m)}.
- Define L on padded length n_m by parsing an input as a rank r, an address x in {0,1}^m, and padding, and outputting the generated row bit T_{m,r}(x).
- Because unranking and row/proof generation take 2^{O(m)} time and n_m=Theta(m), L is in E; long but constant-exponential generated proofs only change the hidden E time constant.
- Assume a circuit family for L of size 2^{delta n_m}. Fix the rank bits to a hard row r* certified by the source theorem. The restricted circuit computes T_{m,r*} with size 2^{delta n_m}+poly(n_m).
- If delta<theta/(kappa(1+D)), then for large m this size is below 2^{theta m}, contradicting the anti-ball MCSP soundness of T_{m,r*}.
- If generation time is instead 2^{a(m)m} with a(m)->infinity, keeping L in E requires n_m=Omega(a(m)m), so the same inequality yields only delta=o(1).

Blocking gap: No construction is known for the required generated anti-ball source: it must give a sparse, advice-free, non-natural proof that some generated row is far from every unrestricted circuit of size 2^{theta m}.

## Falsifiers

- falsifier: proof or row location is supplied by nonuniform advice rather than generated uniformly
- falsifier: generated proof time is 2^{omega(m)} and padding makes the extracted exponent vanish
- falsifier: the anti-ball proof excludes only formulas, AC0, or uniform algorithms instead of unrestricted circuits
- falsifier: indexed random access to row bits has circuit size below 2^{theta m-o(m)}
- falsifier: dense polynomial-time projection of accepted rows creates a useful natural property
- falsifier: black-box query certification uses q=o(2^{theta m}/m) table probes and cannot bind all small circuits
- falsifier: source soundness relies on lex-first search through all truth tables, which is not E-uniform at the target length

## Learning

Cycle 60 separates proof length from proof-generation exponent. Generated anti-ball proofs may be exponentially long without weakening the MCSP-to-E transfer, but only with a constant exponent and advice-free generation. Superconstant generation overhead is a valid quantitative falsifier because preserving E then collapses the extracted exponent to o(1). The remaining source obligation is a sparse generated non-natural anti-ball certificate against unrestricted circuits.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for generated anti-ball source proposals.`
- Rationale: The branch has a valid conditional MCSP-to-E bridge; the live uncertainty is whether proof generation overhead secretly destroys E-uniformity or the lower-bound exponent.
- Situation seed: A canonical low-D generated anti-ball family U_m of m-input truth tables, where each row has a sequential proof stream certifying distance from all circuits of size 2^{theta m}; the induced language multiplexes rank and address and pads to length n_m.
- Varied variable: proof-generation exponent lambda in t_G(m)=2^{lambda m+o(m)}, with lambda either constant or slowly growing.
- Held-fixed controls: MCSP threshold theta is a positive constant against unrestricted nonuniform circuits., Distinct-image entropy D and padding density kappa are fixed constants., The generator is deterministic, uniform, and advice-free., The row decoder has no subthreshold indexed random access shortcut., Projection of accepted rows remains sparse and not a natural-size property.
- Expected observation: For constant lambda, L remains in E and the bound delta<theta/(kappa(1+D)) is unchanged; for lambda(m)->infinity, either L leaves E or padding forces delta to o(1).
- Transfer certificate needed: A formal E-uniform bit-generation algorithm for the multiplexed language plus a nonblackbox anti-ball soundness proof for at least one generated row at each kappa-dense source length.

## Next Experiment

Instantiate a toy generated anti-ball proof with D=0 or D=o(1), compute its row-decoder access profile, and test whether its soundness argument is genuinely nonblackbox or secretly a subthreshold challenge-list verifier.
