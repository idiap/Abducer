# cycle-0056

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: XOR quotient codebook gate

## Candidate Lemma

Quotient codebook-or-rank sketch upper bound for generated XOR carriers. Let H_N(x)=xor_{j<=M} SAT(phi_{N,j}(x)) with M=N^q, formula length L=(log N)^d, and generator size N^rho. After odd-multiplicity cancellation in a SAT-preserving quotient Q_N, write H_N(x)=<lambda_N,a_N(x)> over F_2. If all but E inputs are covered by cells whose quotient-incidence vectors have either affine coordinate dimension r_i or exact transcript codebook size R_i, with total locator/decoder circuit size S, then C(H_N)<=O(S+sum_i min{r_i,R_i log R_i}+EN). Hence any N^{1+epsilon} source lower bound must rule out all subthreshold quotient codebook-or-rank sketches; such a sketch is a concrete falsifier, not merely weak evidence.

## Definitions

- source object: the generated XOR carrier H_N on N-bit seeds, using M=N^q generated SAT instances of length L=(log N)^d and normalized quotient-incidence vector a_N(x) in F_2^{Q_N}.
- target object: nonuniform circuits for SAT on length-L formulas, with the intended target consequence SAT notin SIZE(n^c) for every fixed c, hence SAT notin P/poly if the source lower bound holds for unbounded N.
- controlled interface: substitute a hypothesized SAT circuit for each generated query, compute the generator and parity incidence, and charge only N^rho+N^q L^c+lower-order wiring.
- target-preserving condition: the quotient must preserve SAT labels and only cancel even multiplicities; source-side transcript advice may be used as an upper-bound falsifier but must not be smuggled into the target substitution bridge.

## Assumptions

- L=(log N)^d for a fixed d>1, M=N^q, and q,rho<1+epsilon.
- The generator outputs formulas and parity positions by circuits of size at most N^rho.
- The quotient relation on generated formulas is SAT-preserving, so every quotient class has a well-defined label lambda_N(u)=SAT(u).
- A sketch consists of a cell locator, optional affine coordinate decoders, optional exact codebook transcripts, and an error set of at most E seeds.

## Equations

- xor-quotient-normal-form: `H_N(x)=\langle \lambda_N,a_N(x)\rangle_{\mathbb F_2},\qquad a_N(x)\in\mathbb F_2^{Q_N}.`. Valid when: Valid when generated formulas are reduced only by odd parity cancellation and by a quotient preserving SAT labels.
- codebook-rank-upper-bound: `C(H_N)\le O\!\left(S+\sum_i \min\{r_i, R_i\log R_i\}+EN\right).`. Valid when: Applies when the sketch covers all but E seeds and each bad seed is patchable by an equality circuit of size O(N).
- target-substitution-bound: `SAT\in SIZE(n^c)\Rightarrow C(H_N)\le N^\rho+N^q L^c+N^q\operatorname{polylog}L=N^{\max\{\rho,q\}+o(1)}.`. Valid when: Requires polylogarithmic query length, fixed target exponent c, and a generator circuit of size N^rho.
- magnification-threshold: `C(H_N)>N^{1+\epsilon}\ \wedge\ \max\{\rho,q\}<1+\epsilon\Rightarrow \forall c\; SAT\notin SIZE(n^c).`. Valid when: Valid when the source lower bound holds for infinitely many large N and the query lengths L tend to infinity.

## Attempted Derivation

- Normalize each generated multiset by deleting pairs with equal SAT-preserving quotient class; the remaining parity-incidence vector is a_N(x).
- For an affine cell, fix a basis b_{i,1},...,b_{i,r_i} and hardwire the bits <lambda_N,b_{i,l}> plus the affine offset bit; compute the coordinate decoder and XOR the selected constants.
- For a codebook cell, hardwire p_{i,t}=<lambda_N,v_{i,t}> for every transcript value t in [R_i]; compute t_i(x) and evaluate a table circuit of size O(R_i log R_i).
- Use the cheaper implementation on each cell, multiplex by the cell locator, and patch each of the E uncovered seeds by an equality test on the N-bit input.
- The resulting circuit size is O(S+sum_i min{r_i,R_i log R_i}+EN), so any sketch below N^{1+epsilon} contradicts the desired source lower bound.

Blocking gap: The derivation does not show that every small arbitrary circuit for H_N yields such a quotient sketch. It is an upper-bound falsifier, not a lower-bound certificate.

## Falsifiers

- Subthreshold quotient codebook sketch: S+sum_i R_i log R_i+EN<N^{1+epsilon-o(1)} makes H_N easy by hardwired parity values.
- Low affine rank after SAT-preserving quotient: S+sum_i r_i+EN<N^{1+epsilon-o(1)} makes H_N easy by hardwired basis parities.
- Symmetry-pair cancellation: most generated SAT instances cancel modulo 2 inside Q_N, causing constant or low-transcript carriers despite high raw formula entropy.
- Target threshold collapse: max{rho,q}>=1+epsilon invalidates the magnification implication even if the source lower bound is true.
- Model mismatch falsifier: quotienting formulas by a relation that is not SAT-preserving breaks the identity H_N=<lambda_N,a_N>.
- Nonuniform leakage through a short transcript table may decide H_N without computing SAT on any new formula.
- Natural-proof falsifier: a proof using only random-label hardness of lambda_N would not identify real SAT and is not valid route evidence under standard pseudorandomness barriers.

## Learning

Cycle 56 adds a sharper conservation law for XOR carriers: after SAT-preserving parity quotienting, H_N is easy whenever the incidence map has either low affine rank or a low-cardinality computable transcript, with patchable errors charged by EN. Thus high quotient entropy or high rank alone is not valid source evidence; the source obligation is a combined codebook-or-rank minimax lower bound, while the target bridge remains unchanged.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the XOR quotient carrier.`
- Rationale: The branch has a valid target bridge; the live uncertainty is whether aggregate parity hardness survives nonuniform transcript leakage rather than merely high rank or high formula entropy.
- Situation seed: Take H_N(x)=xor_{j<=N^q} SAT(phi_{j}(x)) with L=(log N)^d, d>1, q in ((1+epsilon)/2,1+epsilon), and let the generator choose formulas from a high-entropy range but with normalized odd supports depending on a seed feature tau(x).
- Varied variable: The transcript-image exponent theta where |range(tau)|=N^theta after SAT-preserving odd-support quotienting.
- Held-fixed controls: Keep q,rho<1+epsilon so the target substitution bridge remains valid., Keep L=(log N)^d with d>1 to avoid short-query truth-table collapse., Keep the quotient SAT-preserving and allow only modulo-2 cancellations of duplicate classes., Keep the source circuit model as general nonuniform SIZE on N-bit inputs.
- Expected observation: If theta<1+epsilon and tau is computable below the threshold, then H_N has a table circuit below N^{1+epsilon}; if theta is large but affine rank is small, the affine sketch still falsifies the source lower bound.
- Transfer certificate needed: Before intuition can enter the proof queue, prove a lower bound that every SAT-preserving quotient transcript-or-rank sketch has cost N^{1+epsilon-o(1)}, or prove a nonrelativizing extraction from arbitrary small H_N circuits to such sketches.

## Next Experiment

Instantiate a candidate high-q generator and compute the exponent of its SAT-preserving odd-support transcript range versus affine span rank; reject it if min{theta,rank-exponent}+locator-cost falls below 1+epsilon.

# Barrier audit for shifted-partial-derivative arithmetic lower-bound routes

## Candidate Lemma

A shifted-partial-derivative lower bound is a valid bridge to a named bounded-depth arithmetic target, but not to P != NP unless a size-preserving Boolean-to-arithmetic compiler for the SAT multilinear extension is supplied.

## Definitions

- source object: a polynomial family P_m over a fixed field F, typically the multilinear extension MLE(SAT_m) or an algebraic benchmark such as Det_n.
- target object: low-support homogeneous depth-4 arithmetic circuits SigmaPiSigmaPi_F(S,D,t) of size S, formal product fan-in D, and bottom support at most t.
- controlled interface: compare SPD_{k,l}^F(P_m) with the standard upper bound U_{k,l}(m,S,D,t) for the named arithmetic model.
- target-preserving condition: for P-vs-NP use, the polynomial must be the canonical SAT truth-table extension and Boolean size m^c must imply a circuit inside the same SigmaPiSigmaPi_F(S,D,t) threshold after padding and multilinearization.
- SPD_{k,l} is the dimension of shifted k-th partial derivatives after multilinear projection.
- The route is algebraic and may be algebraically natural; this is harmless for restricted arithmetic lower bounds but invalid as a Boolean lower-bound transfer without the missing compiler.

## Assumptions

- F is fixed before the lower-bound statement and is not chosen from the input.
- The upper-bound theorem for SigmaPiSigmaPi_F(S,D,t) is invoked with explicit k,l,D,t.
- The source polynomial is given explicitly enough that the SPD witness is not merely a nonuniform truth-table artifact.
- Boolean arithmetization by gate replacement is allowed only as cube agreement, not as computation of the unique multilinear extension.

## Equations

- spd_definition: `\operatorname{SPD}_{k,\ell}^{F}(P)=\dim_F \operatorname{span}\{\operatorname{ml}(x^a\partial^\alpha P): |\alpha|=k, |a|=\ell\}`. Valid when: Valid when P is over a fixed field and multilinear projection is applied after shifting monomials.
- depth4_low_support_upper_bound: `\operatorname{SPD}_{k,\ell}^{F}(C)\le S\binom{D}{k}\binom{m}{\ell+kt}=:U_{k,\ell}(m,S,D,t)`. Valid when: Valid when every bottom factor has support at most t and each product gate has fan-in at most D.
- restricted_arithmetic_transfer: `\operatorname{SPD}_{k,\ell}^{F}(P_m)>U_{k,\ell}(m,S,D,t)\;\Rightarrow\;P_m\notin\Sigma\Pi\Sigma\Pi_F(S,D,t)`. Valid when: Valid after the source polynomial and target arithmetic class use the same field, variables, and degree parameters.
- boolean_gate_arithmetization_gap: `C_{bool}\text{ of size }S\Rightarrow A_C\text{ of size }O(S),\; A_C|_{\{0,1\}^m}=f,\; \deg(A_C)\le 2^S`. Valid when: Valid when Boolean gates are translated arithmetically on the cube, without claiming the unique multilinear extension is computed.

## Attempted Derivation

- Start with P_m=MLE(SAT_m) over F and choose k,l,D,t,S=m^c after a proposed depth-reduction interface.
- Assume a lower bound SPD_{k,l}^F(P_m)>S binom(D,k) binom(m,l+kt).
- By the low-support depth-4 upper bound, conclude P_m is not computed by SigmaPiSigmaPi_F(S,D,t); this is a valid restricted arithmetic consequence.
- Try to convert SAT in P, witnessed by Boolean circuits of size m^c, into such a depth-4 circuit for P_m.
- Gate arithmetization gives a small arithmetic circuit agreeing with SAT on the Boolean cube, but it need not compute MLE(SAT_m), may have degree 2^{m^c}, and depth reduction can destroy the D,t threshold.
- Determinant supplies the sanity check: strong depth-4 arithmetic lower bounds can hold for a polynomial-time computable family.

Blocking gap: No size-preserving, padding-stable compiler from Boolean SIZE(m^c) deciders for SAT_m to low-support depth-4 circuits computing MLE(SAT_m) within the same SPD threshold.

## Falsifiers

- Determinant is P/VP yet has nontrivial shifted-partial lower bounds against restricted depth-4 arithmetic circuits.
- The tagged carrier F_{m,n}(z,x,Y) preserves SAT hardness at z=0 while allowing a P-easy determinant branch to dominate the global SPD measure.
- Boolean gate arithmetization computes a representing polynomial on the cube, not necessarily the unique multilinear extension used by the measure.
- Depth reduction may increase formal degree or bottom support until U_{k,l}(m,S,D,t) exceeds the claimed lower bound.
- A claimed P-vs-NP consequence is invalid if the field, arithmetization, or padding parameters are changed after the lower-bound threshold is set.

## Learning

Cycle 56 isolates the shifted-partial-derivative route as a valid restricted arithmetic lower-bound bridge with explicit S,D,t,k,l thresholds. The same route is not P-vs-NP progress: determinant and tagged determinant/SAT carriers are falsifier objects, and the missing formal object is a size-preserving compiler from Boolean SAT deciders to low-support depth-4 circuits for MLE(SAT).

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for arithmetic-measure routes.`
- Rationale: The branch needs to test whether high shifted-partial complexity is tied to the SAT core or can be imported from a P-easy algebraic component while preserving NP-hardness.
- Situation seed: Consider F_{m,n}(z,x,Y)=(1-z)MLE(SAT_m)(x)+z Det_n(Y), with the many-one SAT reduction x -> (0,x,0) fixed and the global SPD measure evaluated on all variables.
- Varied variable: The determinant dimension n=m^beta, equivalently the relative number of P-easy algebraic variables added to the SAT carrier.
- Held-fixed controls: The SAT core and reduction through the z=0 slice are fixed., The field F and SPD parameters k,l are fixed before beta varies., The target model remains SigmaPiSigmaPi_F(S,D,t), not unrestricted Boolean circuits., No nonuniform advice is allowed in the determinant tag or in parameter selection.
- Expected observation: For sufficiently large beta, the measured SPD lower bound can be dominated by the determinant branch while the SAT slice is unchanged; this demonstrates that global arithmetic hardness of an NP-complete carrier is not target-preserving.
- Transfer certificate needed: A projection or branch-isolation lemma proving that the lower bound remains above U_{k,l} on MLE(SAT_m) itself, plus a Boolean-to-low-support-depth4 compiler preserving S,D,t under padding.

## Next Experiment

Compute the exact depth-reduction blowup for a hypothetical Boolean SAT circuit of size m^c under multilinearization, and check whether any nonvacuous k,l,t setting keeps U_{k,l} below the desired SAT-MLE lower bound.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Transcript-load no-go for black-box symbolic anti-ball certificates: if a deterministic verifier V^T(pi) accepts after reading q truth-table bits and soundness requires every accepted T to have circuit complexity greater than 2^{epsilon m}, then q=Omega(2^{epsilon m}/m). Otherwise the same transcript accepts a zero-filled table of size O(qm), a direct falsifier for the source relation.

## Definitions

- source object: black-box symbolic anti-ball verifier V^T(pi) for T in {0,1}^{2^m}, with transcript query set Q and claimed soundness against circuits of size 2^{epsilon m}.
- target object: an E-uniform low-D MCSP carrier whose accepted hard rows multiplex to an E truth-table lower bound.
- controlled interface: accepted certificate plus universal soundness -> MCSP no-side row -> low-D multiplexing -> all-length E circuit lower bound.
- target-preserving condition: no advice, E-canonical row selection, kappa-dense lengths, distinct-image entropy D, and transcript binding strong enough to avoid easy zero-fill replays.
- q_V(m,pi) is the number of T-bit queries made on the accepting transcript after fixing the deterministic verifier and certificate.
- A_Q is the table agreeing with T on queried positions Q and equal to 0 outside Q.

## Assumptions

- V has no nonuniform advice and accesses the row T only by adaptive bit queries; proof bits may be arbitrary but cannot change T-query answers.
- The source relation claims universal soundness: every accepted pair (T,pi) is an MCSP no-side row at threshold 2^{epsilon m}.
- The target extraction uses exact row hardness; existential hard rows require the earlier multiplexing repair and do not license a black-box soundness claim.

## Equations

- filler_circuit_bound: `\mathrm{size}(A_Q) \le c q m + O(1)`. Valid when: Valid when Q is the complete set of truth-table positions read by one deterministic accepting transcript and the filler table is zero outside Q.
- transcript_soundness_load: `q_V(m,\pi) \ge \Omega(2^{\epsilon m}/m)`. Valid when: Valid for black-box universal-sound verifiers whose acceptance can be replayed after changing all unread truth-table bits.
- short_black_box_collapse: `|\pi|=O(m),\ q_V\le \mathrm{poly}(m) \Rightarrow \text{no constant-}\epsilon\ \text{black-box anti-ball soundness}`. Valid when: Applies when the verifier reads only polynomially many row bits from a linear-size symbolic certificate.
- exact_antiball_transfer: `\delta < \epsilon/(\kappa(1+D))`. Valid when: Applies after the anti-ball certificate quantifies over centers of size 2^{epsilon m} and multiplexing preserves uniformity.
- debited_center_transfer: `\delta < (\epsilon-\rho)/(\kappa(1+D))`. Valid when: Requires the weaker certificate to exclude only centers of size 2^{(epsilon-rho)m}, so radius is spent as edit budget.

## Attempted Derivation

- Fix a deterministic accepting computation of V^T(pi) and let Q be the adaptive set of row positions queried on that computation.
- Define A_Q to agree with T on Q and to be zero outside Q. A_Q is computed by an OR of equality tests for the queried positive positions, so size(A_Q)=O(|Q|m).
- Run V^{A_Q}(pi). Every adaptive query receives the same answer as in the original transcript, hence the verifier follows the same path and accepts.
- If |Q|m=o(2^{epsilon m}), then A_Q is an accepted row with unrestricted circuits below the claimed MCSP threshold.
- Therefore a black-box relation claiming universal anti-ball soundness must either read Omega(2^{epsilon m}/m) row bits or use a separately specified non-black-box binding mechanism.

Blocking gap: The argument does not rule out genuinely non-black-box proof systems or algebraic commitments that bind all N row bits without replayable T-query transcripts; those mechanisms must be named and audited for naturalness, algebrization, and advice leakage.

## Falsifiers

- Sparse T-query symbolic certificates with q=2^{theta m} for theta<epsilon are a falsifier for universal MCSP no-side soundness, by zero-fill replay.
- A certificate proving anti-ball exclusion only for centers of size 2^{(epsilon-rho)m) but claiming delta near epsilon/(kappa(1+D)) fails the valid quantitative transfer test.
- Nonuniform advice that selects the hard row or the proof transcript destroys the target-preserving E-uniform extraction.
- A dense constructive predicate accepting many anti-ball rows revives the natural-proofs falsifier unless it is non-large or circuit-sensitive in a declared way.
- A relativizing or algebrizing proof that treats T only as an oracle is blocked by the transcript-load obstruction unless it binds unread truth-table bits nonrelativizingly.

## Learning

Cycle 56 contributes a concrete no-go: black-box symbolic anti-ball certification has a transcript-load threshold q=Omega(2^{epsilon m}/m). This invalidates short query-based proofs as a falsifier while preserving a valid conditional bridge for non-black-box binding certificates. It also repairs radius accounting: rho is not charged to exact MCSP extraction unless the source only forbids smaller centers or spends a sparse edit list.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The branch has narrowed to symbolic anti-ball certificates; the next decision is whether such certificates can be short and black-box or must contain a non-black-box binding theorem.
- Situation seed: For each m, form the CNF Near_{m,2^{epsilon m},2^{rho m}}(T_m) asserting that T_m is within radius 2^{rho m} of a size-2^{epsilon m} circuit. A proposed proof checker verifies a symbolic UNSAT certificate while accessing T_m only through queried truth-table positions, and the resulting row is fed into the low-D multiplexed E target.
- Varied variable: theta where the verifier reads q=2^{theta m} T-bits on an accepting transcript.
- Held-fixed controls: epsilon, rho, kappa, and D are fixed positive constants with the intended exact-center transfer delta<epsilon/(kappa(1+D))., The proof-system soundness claim is universal over accepted rows and uses no nonuniform advice., The target remains an E-uniform all-length lower-bound extraction, not a nonuniform hard truth-table statement., The source row length is N=2^m and the carrier image remains low-D after canonical unranking.
- Expected observation: For theta<epsilon, zero-fill replay should manufacture an accepted easy row of size about 2^{theta m}m, invalidating black-box soundness. At theta>=epsilon, the replay falsifier disappears but the source is no longer a short black-box certificate and needs explicit E-uniform generation.
- Transfer certificate needed: A formal non-black-box binding certificate showing that unread T-bits are fixed by proof soundness, or else a transcript-load lower bound q=Omega(2^{epsilon m}/m), before the symbolic anti-ball intuition may enter the carrier extraction proof queue.

## Next Experiment

Formalize the NearCircuit CNF and test extended-Frege, IPS, and PCP-style commitments for whether their verification binds all 2^m T-bits non-black-box while preserving E-uniform low-D extraction and avoiding the natural-proofs largeness condition.
