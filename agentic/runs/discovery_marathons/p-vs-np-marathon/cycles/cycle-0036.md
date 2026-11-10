# cycle-0036

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: position-indexed unary residual gate

## Candidate Lemma

For the generated-OR carrier with M=N^q polylog-length SAT queries and q in ((1+epsilon)/2,1+epsilon), dense tuple-feature leakage of arity at least two is above threshold, but a valid source lower bound must still defeat position-indexed unary transcript decompositions of total local budget below N^{1+epsilon}. Shared-unary audits are insufficient because nonuniform circuits may hardwire a different predicate for each generated slot.

## Definitions

- source object: H_N(x)=OR_{j<=M} SAT(G_{N,j}(x)), where M=N^q, |G_{N,j}(x)|=L=(log N)^d with d>1, and G_N outputs all M formulas using size N^rho.
- target object: SAT on L-bit instances; target consequence is SAT notin SIZE(poly) and hence NP not subset P/poly, conditional only on the stated H_N lower bound and the clean substitution bridge.
- controlled interface: a SAT circuit of size L^c is substituted into every generated query, giving a circuit for H_N of size N^rho+N^q L^c plus wiring overhead.
- target-preserving condition: rho<1+epsilon and q<1+epsilon, with L=(log N)^d so every fixed SAT exponent contributes only N^{o(1)} to the carrier circuit size.
- Position-indexed unary transcript means predicates A_{N,j}:{0,1}^L->{0,1}^{b_j}, an aggregator B_N on the concatenated transcript, and an optional residual corrector R_N on x.
- The total unary leakage budget is U_N=sum_{j<=M} C(A_{N,j}) plus transcript wiring; the decomposition is subthreshold when max{rho,log_N U_N,log_N C(B_N),log_N C(R_N)}<1+epsilon-o(1).

## Assumptions

- Nonuniform Boolean circuit size is the source lower-bound model.
- G_N is explicit enough that its full output circuit has size N^rho and does not hide SAT advice.
- q is chosen with (1+epsilon)/2<q<1+epsilon and rho<1+epsilon.
- Tuple-feature families of arity t have enumeration cost at least N^{tq-o(1)} before local predicate cost.
- Residual correction is allowed, so sparse or structured errors are counted as a falsifier rather than ignored.

## Equations

- target_substitution: `C(H_N) \le N^{\rho+o(1)}+N^q\,L^c = N^{\max\{\rho,q\}+o(1)}`. Valid when: Valid when SAT has nonuniform circuits of size n^c on L-bit inputs and the generator emits all queries with size N^rho.
- high_q_tuple_floor: `tq>1+\epsilon \quad \text{for every } t\ge 2 \text{ if } q>(1+\epsilon)/2`. Valid when: Applies in the high-q parameter regime before charging any predicate or aggregator overhead to tuple features.
- position_unary_upper_bound: `C(H_N) \le N^{\rho+o(1)}+U_N+C(B_N)+C(R_N)`. Valid when: Valid when H_N equals B_N((A_{N,j}(G_{N,j}(x)))_{j\le M}) \oplus R_N(x) as a Boolean function.
- source_obligation: `\inf_{A_{j},B,R}\max\{\rho,\log_N U_N,\log_N C(B),\log_N C(R)\}>1+\epsilon-o(1)`. Valid when: Requires the target-preserving lower-bound claim to survive all nonuniform position-indexed unary transcript decompositions and residual corrections.

## Attempted Derivation

- Start with H_N(x)=OR_{j<=N^q} SAT(G_{N,j}(x)) and assume a putative lower bound C(H_N)>N^{1+epsilon}.
- The target bridge remains valid: SAT in SIZE(n^c) gives H_N circuits of size N^{max{rho,q}+o(1)}, so a valid H_N lower bound with max{rho,q}<1+epsilon implies SAT notin SIZE(poly).
- Use the cycle-35 parameter q>(1+epsilon)/2. Any explicit tuple transcript that enumerates all pairs or higher arity tuples costs at least N^{2q-o(1)}, already above N^{1+epsilon}.
- Try to conclude that only a shared unary predicate A(F) must be ruled out. This fails because the nonuniform circuit for H_N can attach different small predicates A_j to different generated positions without paying the cost of a uniform rule for j.
- Repair the audit by defining total-budget position-indexed unary transcripts and allowing an arbitrary aggregator plus residual corrector.
- Derive the upper bound C(H_N)<=N^{rho+o(1)}+sum_j C(A_j)+C(B)+C(R). Therefore any subthreshold position-indexed decomposition is a concrete falsifier for the claimed source lower bound.

Blocking gap: No lower-bound technique is supplied for the position-indexed unary residual minimax quantity. Proving it for an explicit H_N is essentially a general-circuit lower bound for a highly structured generated OR, not a consequence of the magnification bridge.

## Falsifiers

- position-indexed unary predicates with total budget below N^{1+epsilon}
- an aggregator B_N of size below N^{1+epsilon} whose transcript classes are nearly monochromatic for H_N
- a residual corrector R_N of size below N^{1+epsilon} covering mixed transcript classes
- generator leakage where G_{N,j} makes SAT labels simple for most fixed positions
- threshold collapse if q<=((1+epsilon)/2), since binary tuple features may become subthreshold

## Learning

Cycle 36 repairs the high-q unary reduction: binary and higher tuple features are threshold-blocked when q>(1+epsilon)/2, but shared-unary audits are not sound for general circuits. The valid remaining source obligation is a position-indexed unary transcript plus residual lower bound with total local budget U_N. This is a sharper route-level gate and supplies an explicit falsifier class, without claiming P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the repaired unary gate.`
- Rationale: After high q removes dense tuple leakage, the next real obstruction is whether slot-specific unary advice can still compute the carrier below the claimed lower-bound threshold.
- Situation seed: Take H_N as an OR of M=N^q generated 3SAT instances of length L=(log N)^d, d>1, where positions are partitioned into easy slots with affine-generated formulas and hard-looking slots with pseudorandom formula images.
- Varied variable: Vary the easy-slot density theta, meaning U_easy=N^{theta q} positions admit O(1)-size position-specific SAT-label surrogates while the remaining positions have no assumed surrogate.
- Held-fixed controls: Keep rho<1+epsilon and q in ((1+epsilon)/2,1+epsilon) so the target substitution bridge is valid., Keep L=(log N)^d with d>1 so exhaustive truth-table lookup is superpolynomial in N and not a subthreshold explanation., Keep the target consequence SAT notin SIZE(poly), not merely a restricted-model separation.
- Expected observation: If theta q plus the aggregator and residual costs stays below 1+epsilon, then a small circuit can exploit easy slots and correct the residual unless the hard slots contribute mixed transcript residual complexity above threshold. This tests whether the unary gate is genuinely stronger than label-balance or semantic-cover gates.
- Transfer certificate needed: A formal lower bound on the position-indexed unary residual minimax quantity for every slot partition and every total local budget U_N<N^{1+epsilon-o(1)}; without this certificate the thought experiment remains only a falsifier probe.

## Next Experiment

Formalize Iota_N^{pos} as a minimax transcript-residual measure and test whether expander-style slot mixing can rule out all low-budget position-indexed unary decompositions without becoming a natural-proof argument.

# Barrier-Aware Lower-Bound Route: resolution target gate

## Candidate Lemma

Expander-Tseitin width lower bounds give a valid exponential lower bound for general resolution and DPLL-style proof search, but they are an invalid bridge to P != NP because the same CNF family is uniformly rejected by Gaussian elimination.

## Definitions

- source object: bounded-degree expander Tseitin CNF family T_n(G,chi) encoding an inconsistent F_2 parity system, with N=Theta(n) edge variables/clauses and initial width w0=O(1).
- target object: general resolution, tree-like resolution, and DPLL proof-search models; not arbitrary polynomial-time SAT algorithms or P/poly circuits.
- controlled interface: resolution width/size lower bound -> lower bound on the named proof-search target, with no automatic transfer to full P or nonuniform circuits.
- target-preserving condition: resolution lower bounds are target-preserving only for algorithms whose rejecting computations p-simulate into resolution proofs; full P or P/poly requires an additional universal p-simulation certificate.
- barrier classification: the obstruction is target-model mismatch, not a natural-proof or algebrization escape; the proof object is syntactic and does not define a useful dense property against Boolean circuits.

## Assumptions

- G_n is a uniformly constructible bounded-degree expander family.
- The charge vector chi has odd total parity, so the Tseitin linear system is inconsistent.
- Each vertex parity equation is encoded by a constant-width CNF gadget over incident edge variables.
- The proposed route tries to infer an algorithmic lower bound from fixed-system resolution hardness.

## Equations

- encoding-size: `\operatorname{vars}(T_n)=\Theta(n),\quad w_0(T_n)=O(1)`. Valid when: Valid when graph degree is bounded and each parity constraint is encoded by constant-width CNF clauses without superlinear padding.
- tseitin-width: `W_{\mathrm{Res}}(T_n)=\Omega(n)`. Valid when: Valid when G_n has constant edge expansion and the charge vector has odd total parity, making the Tseitin system inconsistent.
- bsw-size-width: `S_{\mathrm{Res}}(F)\ge \exp\left(\Omega\left((W_{\mathrm{Res}}(F)-w_0(F))^2/N\right)\right)`. Valid when: Valid when F is an N-variable CNF and the Ben-Sasson--Wigderson size-width theorem is applied to unrestricted resolution.
- shortcut-versus-resolution: `T_{\mathrm{GE}}(T_n)=N^{O(1)}\quad\text{and}\quad S_{\mathrm{Res}}(T_n)=2^{\Omega(N)}`. Valid when: Valid when the input encoding exposes or uniformly recovers the F_2 incidence matrix, so Gaussian elimination is an allowed polynomial-time algorithm.
- padding-erosion: `N_\beta=\Theta(n^{1+\beta}),\quad S_{\mathrm{Res}}(T_{n,\beta})\ge 2^{\Omega(n)}=2^{\Omega(N_\beta^{1/(1+\beta)})}`. Valid when: Valid when padding clauses use fresh variables with a fixed satisfying assignment, so restriction of any padded refutation yields an original refutation.

## Attempted Derivation

- Start with uniform expander Tseitin contradictions T_n of constant initial width.
- Use the expander width lower bound W_res(T_n)=Omega(n).
- Apply Ben-Sasson--Wigderson to obtain S_res(T_n)=2^{Omega(n)}.
- Try to infer that UNSAT or SAT has no polynomial-time algorithm.
- Decode T_n as A x=b over F_2 and reject by Gaussian elimination in N^{O(1)} time.

Blocking gap: No theorem converts an arbitrary polynomial-time UNSAT decider into polynomial-size resolution refutations; resolution does not p-simulate all possible semantic or algebraic algorithms.

## Falsifiers

- falsifier: expander Tseitin contradictions are uniformly P-decidable by F_2 Gaussian elimination yet require exponential general resolution size.
- falsifier: pigeonhole-principle CNF families are trivially recognizable as unsatisfiable but can still be exponentially hard for resolution, showing fixed-family proof hardness is not language hardness.
- falsifier: any hypothetical P decider for UNSAT would induce some polynomially bounded Cook-Reckhow system via computation transcripts, but resolution need not p-simulate that system.
- A valid lower-bound claim must name the proof-search target; otherwise the proof-system lower bound loses target preservation.

## Learning

Cycle 36 isolates a quantitative resolution target gate: expander Tseitin gives W_res=Omega(N) and S_res=2^{Omega(N)} by BSW, yet the same formulas are rejected in polynomial time by Gaussian elimination. The formal obstruction is missing p-simulation of P deciders by resolution. This is valid route-level progress and a concrete falsifier for fixed-proof-system-to-P-vs-NP transfers, not progress on P != NP itself.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch has repeatedly found target-model collapse for rank, communication, and LP routes; resolution lower bounds need the same quantitative source-target audit rather than another proof-complexity slogan.
- Situation seed: Take uniform bounded-degree expander Tseitin CNFs T_n, then form T_{n,beta} by appending independent satisfiable padding clauses over fresh variables so the total length is N_beta=Theta(n^{1+beta}) while the F_2 decoder for the Tseitin core remains uniform.
- Varied variable: padding exponent beta in N_beta=Theta(n^{1+beta})
- Held-fixed controls: constant-degree expansion of G_n, odd total Tseitin charge, constant-width CNF encoding of parity constraints, fresh-variable padding with a fixed satisfying assignment, target lower-bound model is general resolution size, not full P
- Expected observation: Resolution hardness measured in padded length erodes to S_res(T_{n,beta})>=2^{Omega(N_beta^{1/(1+beta)})}, while Gaussian elimination remains polynomial in N_beta; proof-search hardness persists but still does not threaten P.
- Transfer certificate needed: Before this intuition may affect P-vs-NP obligations, prove a p-simulation from every polynomial-time UNSAT decider, or from a named restricted algorithm class, into resolution with polynomial overhead; Tseitin plus Gaussian elimination is the falsifier for omitting this certificate.

## Next Experiment

Apply the same audit to Sherali-Adams and SoS degree lower bounds: name the XOR/Tseitin source, degree d threshold, N^{O(d)} hierarchy runtime, and Gaussian-elimination shortcut before allowing any P-vs-NP transfer claim.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For selector-free low-image MCSP carriers, the D-bit rank overhead is information-theoretic and the aggregate row-forcing threshold q_force=(D+epsilon)/(1+D) is exact up to o(1). Any route beating this threshold must name a hard row structurally, not by compressing the aggregate index.

## Definitions

- source object: a kappa-dense E-canonical image family I_r={T_{r,1},...,T_{r,R_r}} of N=2^r-bit truth tables, with R_r<=2^{D r+o(r)} and at least one row intended to be outside SIZE(2^{epsilon r}).
- target object: an all-length E language obtained by canonical unranking of a hard row and kappa-padding, with target lower-bound exponent delta<epsilon/(kappa(1+D)).
- controlled interface: the rank-addressed aggregate decoder A_r(j,x)=T_{r,j}(x), where j ranges over canonical distinct images and x ranges over r-bit inputs.
- target-preserving condition: row recovery is uniform and advice-free; no nonuniform selector, hidden MCSP oracle, or subthreshold ranked random access may identify the hard row.

## Assumptions

- Distinct-image unranking for I_r is computable in 2^{O(r)} time from r and a rank j.
- The aggregate A_r is a standard truth table on (ceil(log R_r)+r) input bits, not an oracle object or promise table.
- The lower bound claimed for A_r is against unrestricted Boolean circuits, or against a named class closed under multiplexing R_r row circuits.
- Circuit size is measured as gates over fan-in two Boolean bases, with polynomial factors absorbed into o(r).

## Equations

- image_entropy: `R_r \le 2^{D r+o(r)}`. Valid when: Valid when the source image family is E-canonically quotiented by distinct emitted truth tables.
- aggregate_length: `|A_r|=2^r R_r=2^{(1+D)r+o(r)}`. Valid when: Applies when every rank address names one recoverable row without collisions or advice.
- easy_rows_give_easy_aggregate: `(\forall j\ C(T_{r,j})\le 2^{\epsilon r})\Rightarrow C(A_r)\le 2^{(D+\epsilon+o(1))r}`. Valid when: Requires the circuit class to permit uniform multiplexing over all canonical row circuits.
- forcing_threshold: `q_{force}=\frac{D+\epsilon}{1+D}`. Valid when: Valid when aggregate hardness is expressed as an exponent in its own input length.
- cap_slack: `q_{force}\le \alpha_A\iff D\le \frac{\alpha_A-\epsilon}{1-\alpha_A}`. Valid when: Applies after the aggregate construction has a declared verifier or checkpoint cap alpha_A.
- extracted_E_exponent: `\delta<\frac{\epsilon}{\kappa(1+D)}`. Valid when: Requires the target-preserving MCSP carrier transfer and kappa-dense source lengths.

## Attempted Derivation

- Start with a kappa-dense family I_r of R_r<=2^{D r+o(r)} canonical emitted truth tables T_{r,j} of length 2^r.
- Form A_r(j,x)=T_{r,j}(x). Its truth table length is 2^{(1+D)r+o(r)}.
- Assume for contradiction that every row has circuits of size at most 2^{epsilon r}. Hardwire all row circuits behind a rank multiplexer. This yields C(A_r)<=2^{(D+epsilon+o(1))r}.
- Therefore an unrestricted aggregate lower bound C(A_r)>2^{(D+epsilon+eta)r} forces at least one row with C(T_{r,j})>2^{epsilon r}.
- Try to repair the D overhead by replacing j with a shorter hash address. If row recovery is deterministic and advice-free, fewer than log R_r addresses collide on two distinct rows, so the aggregate no longer recovers both truth tables.
- If the collision is resolved by a row selector, the selector is nonuniform leakage; if resolved by MCSP postfiltering, the E extraction budget is exceeded.

Blocking gap: The route still lacks a non-natural source theorem proving either a tiny-D hard row directly or an unrestricted aggregate lower bound above q_force within the cap alpha_A.

## Falsifiers

- A proposed carrier with D>(alpha_A-epsilon)/(1-alpha_A) when its only row-hardness evidence is an aggregate lower bound under cap alpha_A.
- A compressed-index aggregate using fewer than log R_r rank bits while claiming to recover all distinct rows without advice.
- A nonuniform selector that names the hard row; this may prove a nonuniform statement but is invalid for the E target.
- An aggregate lower bound only for a restricted circuit class not closed under row multiplexing.
- A natural, dense constructive property over most truth tables; it abandons the sparse carrier interface and meets the natural-proofs falsifier.
- A relativizing oracle construction of high MCSP certificates without uniform canonical unranking; it does not transfer through the controlled interface.

## Learning

Cycle 36 establishes rank-index conservation for low-image MCSP carriers. The D overhead cannot be removed by hashing or compressed aggregates without losing row recovery or adding advice. Thus q_force=(D+epsilon)/(1+D) is an exact aggregate-forcing threshold, while the valid E extraction from an actual hard row remains delta<epsilon/(kappa(1+D)). The viable source search is now tiny-D direct row hardness or a genuine unrestricted aggregate lower bound with declared cap slack.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for aggregate-index repairs.`
- Rationale: The branch is blocked by whether D can be made harmless. A concrete aggregate family tests if index compression preserves the target or only hides nonuniform leakage.
- Situation seed: For each r, take R=2^{D r} canonical MCSP certificate images T_1,...,T_R of length 2^r and form the aggregate truth table A_D(j,x)=T_j(x). Compare the standard rank aggregate with a hashed aggregate H(h,x) using a<Dr address bits.
- Varied variable: Distinct-image entropy D, including the near-cap regime D=(alpha_A-epsilon)/(1-alpha_A)-s.
- Held-fixed controls: MCSP no-side threshold 2^{epsilon r}., kappa-dense source lengths and kappa-padding to the E target., E-canonical distinct-image unranking in time 2^{O(r)}., No advice, no MCSP oracle, and no nonuniform hard-row selector., Aggregate lower bounds are against unrestricted Boolean circuits or a named multiplexing-closed class.
- Expected observation: The standard aggregate forces row hardness exactly above q_force=(D+epsilon)/(1+D), while the hashed aggregate with a<Dr either loses row recovery or smuggles selector advice. As D approaches the cap slack, the valid extracted exponent delta shrinks and the aggregate source becomes nonviable.
- Transfer certificate needed: A formal certificate must prove unrestricted aggregate hardness above 2^{(D+epsilon+eta)r} and deterministic advice-free row recovery, or else replace aggregate forcing by a structural direct hard-row certificate.

## Next Experiment

Audit D=o(1) and D=0 carrier candidates: determine whether a constant-size canonical image family can contain a structurally certified high-MCSP row without using counting, advice, or subthreshold ranked random access.
