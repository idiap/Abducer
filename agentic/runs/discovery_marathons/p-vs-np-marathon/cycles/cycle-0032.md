# cycle-0032

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Generated-OR magnification: correction-residual separator gate

## Candidate Lemma

Exact correction-residual audit: an N^{1+epsilon} lower bound for a generated-OR carrier is valid only if every small local formula predicate leaves a high-complexity residual correction H_N xor S_A; approximate bad-bag counting is only a sparse-residual corollary.

## Definitions

- source object: H_N:{0,1}^N -> {0,1}, H_N(x)=OR_{j<=M} SAT(G_N(x,j)), where M=N^q and G_N outputs L=(log N)^d bit SAT instances.
- target object: SAT on L-bit instances, with target consequence SAT notin P/poly when the bridge is combined with q,rho<1+epsilon and d>1.
- controlled interface: the whole bag list x -> (G_N(x,1),...,G_N(x,M)) has circuit size N^{rho+o(1)}, and a local predicate A sees only one generated formula.
- target-preserving condition: d>1 and max{rho,q}<1+epsilon, so substituting any fixed polynomial-size SAT circuit costs N^{o(1)} and preserves the lower-bound threshold.
- S_A(x)=OR_{j<=M} A(G_N(x,j)) is the bag decision induced by the local predicate A.
- R_A(x)=H_N(x) xor S_A(x) is the exact correction residual; set log_N C(0)=-infty.

## Assumptions

- General nonuniform Boolean circuits with fan-in two gates are the source lower-bound model.
- M=N^q, L=(log N)^d, d>1, and q,rho are constants independent of SAT circuit exponent c.
- The generator cost N^{rho+o(1)} is charged once for producing or multiplexing all queried formulas.
- The lower-bound claim under audit is C(H_N)>N^{1+epsilon-o(1)}.

## Equations

- carrier: `H_N(x)=\bigvee_{j=1}^{N^q} SAT(G_N(x,j))`. Valid when: Valid when the generated bag interface and SAT encoding are fixed for input length N.
- separator_residual: `S_A(x)=\bigvee_{j=1}^{N^q} A(G_N(x,j)),\qquad R_A=H_N\oplus S_A`. Valid when: Valid when A is any nonuniform predicate on one generated L-bit formula.
- correction_upper_bound: `C(H_N)\le N^{\rho+o(1)}+N^q C(A)+C(R_A)+N^{q+o(1)}`. Valid when: Applies after composing A with every generated query and xoring the residual correction circuit.
- necessary_gate: `C(H_N)>N^{1+\epsilon-o(1)}\Rightarrow \forall A:\max\{\rho,q+\log_N C(A),\log_N C(R_A)\}\ge 1+\epsilon-o(1)`. Valid when: Requires the source lower bound to be against the same nonuniform circuit model used by the correction construction.
- sparse_error_patch: `|\operatorname{supp}(R_A)|\le N^\delta\Rightarrow C(R_A)\le N^{1+\delta+o(1)}`. Valid when: Valid when erroneous bags are patched by equality tests on N-bit source inputs.

## Attempted Derivation

- Start with the previous approximate relaxed bag-separator lemma: if A is correct on all but E source bags, then sparse equality patching gives C(H_N)<=N^{rho+o(1)}+N^q C(A)+O(NE).
- Replace the support-size patch by the exact identity H_N=S_A xor R_A, where R_A=H_N xor S_A. This yields the sharper upper bound in L32.1 without assuming the error set is sparse.
- Try to derive C(R_A)>N^{1+epsilon} from hardness of SAT on the generated range U_N={G_N(x,j)}.
- The derivation fails because R_A is a function of whole source bags x, not a predicate on individual formulas. It can encode global correlations among generated queries and may be small even if every range-restricted SAT predicate is hard.
- Thus promise SAT hardness, semantic range entropy, and label balance do not imply the needed source lower bound unless they also rule out low-complexity residual corrections.

Blocking gap: No known reduction converts a small residual correction R_A into a small SAT solver or separator on the generated formula range. This is the current formal gap.

## Falsifiers

- correction-residual falsifier: exists A with q+log_N C(A)<1+epsilon and C(H_N xor S_A)<N^{1+epsilon-o(1)}.
- structured-error falsifier: the bad-bag set is large but has a simple residual circuit, so counting errors would falsely suggest hardness.
- threshold-collapse falsifier: q>=1+epsilon or rho>=1+epsilon makes the target transfer too expensive.
- nonuniform-leakage falsifier: residual advice about source bags repairs an imperfect local separator without yielding any SAT solver.
- natural-proof obstruction: a large constructive property separating H_N from N^{1+epsilon} circuits would conflict with standard pseudorandom-function barriers unless the proof is carrier-specific and non-large.

## Learning

Cycle 32 converts the approximate bag-separator gate into an exact correction-residual gate. The valid target bridge is unchanged, but the source lower bound must prove Phi_N>1+epsilon-o(1): every small local formula predicate must leave a residual H_N xor S_A of high circuit complexity. Sparse error patching is only one falsifier; structured residual leakage is the stronger obstruction.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for generated-OR carrier proposals.`
- Rationale: The route no longer fails only through sparse bad bags; it fails whenever an imperfect local predicate has a low-complexity residual correction. A concrete experiment tests whether candidate generators accidentally expose such residual structure.
- Situation seed: Take H_N(x)=OR_{j<=N^q} SAT(G_N(x,j)) with L=(log N)^d, d>1. Plant or audit a local predicate A_t on generated formulas, then compute or upper-bound R_t(x)=H_N(x) xor OR_j A_t(G_N(x,j)) for a family of tagged or low-rank bag generators.
- Varied variable: residual circuit exponent r_t=log_N C(R_t), including the sparse case r_t=1+delta when R_t has N^delta exceptional bags.
- Held-fixed controls: q,rho<1+epsilon so the target transfer remains valid., d>1 so exhaustive truth-table lookup is not a subthreshold explanation., The generated strings remain honest SAT encodings of length L(N)., A_t is local to one formula and receives no direct source input x.
- Expected observation: If some t gives q+log_N C(A_t)<1+epsilon and r_t<1+epsilon, then the carrier has a concrete subthreshold circuit despite possibly high semantic range entropy. If all simple A_t leave residuals above threshold, the source audit survives this leakage test.
- Transfer certificate needed: Before the intuition affects proof obligations, exhibit explicit circuits for A_t and R_t or prove lower bounds for every such residual; also certify that the generator cost, query length, and SAT-language honesty are preserved.

## Next Experiment

Instantiate Phi_N for a tagged generated-OR carrier and compute whether simple tag predicates produce subthreshold residual circuits; then test an untagged high-entropy generator for the same residual leakage.

# Barrier-Aware Lower-Bound Route: discrepancy carrier audit

## Candidate Lemma

Uniform two-party discrepancy of a balanced truth-table matrix is not a target-preserving carrier for full polynomial-size circuit lower bounds. The inner-product matrix has optimal low discrepancy but is computed by linear-size circuits, so any route using only low discrepancy must either restrict the target to low-communication models or add a new bridge not implied by discrepancy.

## Definitions

- source object: a sign matrix M_f in {+1,-1}^{2^r x 2^r} obtained from a Boolean truth table f:{0,1}^{2r}-> {0,1} under the fixed split x|y.
- target object: nonuniform Boolean circuits SIZE((2r)^k) for the original 2r-bit function, with fixed k>=1.
- controlled interface: a proposed separator property R_{r,delta} accepts f when Disc_U(M_f)<=delta, and it may transfer only if every function in the target circuit class is rejected.
- target-preserving condition: the matrix measure must exclude all SIZE((2r)^k) functions under the same encoding, not merely exclude low-cost communication protocols for the chosen partition.

## Assumptions

- Discrepancy is rectangle discrepancy under the uniform distribution on [2^r] x [2^r].
- IP_r(x,y)=<x,y> mod 2 is encoded as a 2^r x 2^r Hadamard sign matrix.
- The target is full nonuniform circuit size, not formula size, monotone circuits, AC0, or low-communication circuits.
- A valid route-level transfer must prove usefulness against the named target class before natural-proof or relativization escape claims matter.

## Equations

- matrix_length: `N=2^{2r},\quad n=2^r,\quad M_f\in\{\pm1\}^{n\times n}.`. Valid when: Valid when the source object is a balanced two-party split of a 2r-bit truth table.
- ip_discrepancy: `\operatorname{Disc}_U(M_{IP_r})\le \|M_{IP_r}\|_2/n = n^{-1/2}=N^{-1/4}.`. Valid when: Valid when discrepancy is measured uniformly over rectangles and IP gives a Hadamard matrix.
- ip_circuit_size: `\operatorname{size}(IP_r)=O(r)\le (2r)^k\quad\text{for every fixed }k\ge1\text{ and large }r.`. Valid when: Valid when the target class is ordinary Boolean circuits over the 2r input bits.
- random_largeness_scale: `\Pr_{M\leftarrow\{\pm1\}^{n\times n}}[\operatorname{Disc}_U(M)\le Cn^{-1/2}]\ge 1-\exp(-\Omega(n))\quad(C>\sqrt{4\ln 2}).`. Valid when: Valid when a union bound ranges over all rectangles in an n by n random sign matrix.

## Attempted Derivation

- Encode SAT on 2r-bit instances as a matrix M_SAT under a fixed balanced split.
- Assume a proposed method proves Disc_U(M_SAT)<=N^{-1/4}.
- Try to define R={f: Disc_U(M_f)<=N^{-1/4}} as the separator property for SIZE((2r)^k).
- Use the random-matrix calculation to note that R is large at this threshold.
- Use IP_r as a substitution test for usefulness: IP_r lies in R but has O(r)-size circuits.
- Conclude that the transfer to full circuit lower bounds is invalid unless the method proves an additional theorem excluding all small circuits from low discrepancy, which IP makes impossible.

Blocking gap: Discrepancy lower bounds measure communication under one partition; full circuit size can be small while discrepancy is low. The missing bridge is false for SIZE(poly).

## Falsifiers

- IP_r is a concrete falsifier for usefulness of low-discrepancy properties against full polynomial-size circuits.
- A route that only proves high communication complexity or low discrepancy under one split is invalid for P vs NP unless it names a target-preserving circuit-to-protocol bridge.
- The threshold delta=N^{-1/4} is compatible with random largeness and with an easy O(r)-circuit function, so largeness alone is not the obstruction.
- Exact discrepancy may also lose poly(N) constructivity; however the stronger failure here is lack of usefulness even before constructivity is audited.

## Learning

Cycle 32 separates communication-matrix hardness from circuit hardness. Low uniform discrepancy is dense and can certify lower bounds for low-communication targets, but IP_r is a small-circuit low-discrepancy falsifier for full SIZE(poly). The valid contribution is a target-preservation gate: discrepancy routes must state the circuit-to-protocol threshold c(r), and for arbitrary circuits that threshold collapses to 2^{-Theta(r^k log r)} rather than the random N^{-1/4} scale.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and restricted-transfer calibration.`
- Rationale: The branch needs a concrete target-preserving test because discrepancy looks like a strong lower-bound certificate but may silently change the target from circuits to protocols.
- Situation seed: Compare two matrices under the same x|y split: M_SAT for padded SAT instances of length 2r and M_IP for inner product on r+r bits, while the target remains SIZE((2r)^k).
- Varied variable: The discrepancy threshold delta=N^{-alpha}, varying alpha around 1/4 and around the protocol threshold c(r)=alpha log N.
- Held-fixed controls: The target class is full nonuniform SIZE((2r)^k), not a communication class., The split x|y and uniform rectangle discrepancy definition are fixed., The truth-table length is N=2^{2r}., No advice or promise is allowed to remove IP_r from the target class.
- Expected observation: For alpha<=1/4, IP_r is accepted by the low-discrepancy property while remaining easy for circuits; for alpha>1/4, the route must show SAT has much smaller-than-Hadamard discrepancy and still must explain why all small circuits have larger discrepancy, which IP refutes at the full-circuit level.
- Transfer certificate needed: A valid certificate would be either a restriction of the target to c-bit protocol classes with Disc<2^{-c}, or a new nonblack-box theorem relating full circuit size to discrepancy; the latter is impossible in this form because IP_r is an explicit counterexample.

## Next Experiment

Audit whether discrepancy of SAT under formula-variable splits yields any nontrivial lower bound for a named restricted class such as small-depth circuits with low cross-partition communication, and compute the exact c(r) threshold before considering any broader circuit claim.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Access-profile bridge for bounded-image MCSP carriers: a uniform low-distinct-image MCSP no-side carrier transfers to an E lower bound with exponent loss kappa(1+D), while any subthreshold random-access decoder for the same images is a formal source falsifier.

## Definitions

- source object: a uniform certificate verifier V_m with O(m)-bit certificates whose accepted transcripts emit truth tables f:{0,1}^m -> {0,1}; I_m is the set of distinct emitted tables after an E-canonical quotient.
- target object: the multiplexed E language L_V on inputs (j,x,pad), where j is the canonical rank of an image in I_m and L_V(j,x)=f_j(x).
- controlled interface: E-canonical distinct-image unranking may be sequential and full-table; a separate bit decoder with time 2^{beta m+o(m)} is treated as leakage, not as part of the bridge requirement.
- target-preserving condition: source lengths are kappa-dense, image entropy is D, at least one canonical image at each source length has MCSP complexity above 2^{epsilon m}, epsilon is below the verifier cap alpha_V, and no advice or nonuniform length selector is used.

## Assumptions

- For infinitely many or all kappa-dense source lengths m, some f in I_m has circuit complexity C(f)>2^{epsilon m}.
- The number of distinct canonical images satisfies |I_m| <= 2^{D m+o(m)} for a constant D.
- Canonical unranking and evaluation of L_V run in 2^{O(m)} time uniformly, possibly by sequentially emitting the whole table.
- The padding map from source length m to target input length n preserves uniformity and has gap at most kappa.
- If a proposed source supplies bit access in time 2^{beta m+o(m)}, then beta is declared and audited against epsilon.

## Equations

- image_entropy: `\log_2 |I_m| \le Dm+o(m)`. Valid when: Valid when the source carrier has an E-canonical quotient and distinct images are counted at each source length.
- source_no_side: `\exists f\in I_m\; C(f)>2^{\epsilon m}`. Valid when: Valid when the MCSP no-side claim is existential over the canonical image family and uses the same truth-table length m.
- multiplexed_length: `n=(1+D)m+o(m)`. Valid when: Valid when canonical ranks use Dm+o(m) bits and the queried truth-table input contributes m bits.
- target_lower_bound: `\delta < \frac{\epsilon}{\kappa(1+D)}`. Valid when: Applies after the reduction preserves uniformity, kappa-density, canonical ranking, and the MCSP threshold parameter epsilon.
- random_access_falsifier: `\beta<\epsilon \;\Rightarrow\; C(f_j)\le 2^{\beta m+o(m)}<2^{\epsilon m}`. Valid when: Requires a uniform bit decoder for every canonical image whose running time can be circuitized with only polynomial overhead.

## Attempted Derivation

- Let I_m be the canonical set of distinct accepted images with log |I_m| <= Dm+o(m); rank each image by j of length Dm+o(m).
- Define L_V(j,x,p)=f_j(x), ignoring padding p. Sequential canonical unranking emits f_j and returns the x-th bit in time 2^{O(m)}, so L_V is in E on input length n=(1+D)m+o(m).
- Assume L_V has circuits of size 2^{delta n} on the padded target lengths. Hardwire the rank j* of a source-hard image f_{j*} and the padding convention to obtain circuits for f_{j*} of size 2^{delta(1+D)m+o(m)}.
- With kappa-dense padding, the exponent becomes delta kappa(1+D). If delta<epsilon/(kappa(1+D)), this contradicts C(f_{j*})>2^{epsilon m}.
- Now audit leakage: if the same source gives bit access f_j(x) in time 2^{beta m+o(m)}, standard circuit simulation gives C(f_j)<=2^{beta m+o(m)}. Thus beta<epsilon contradicts the no-side source claim before extraction begins.

Blocking gap: The derivation still assumes a source theorem producing a bounded-D, cap-compatible, no-advice image family with at least one 2^{epsilon m}-hard image; no such theorem is constructed here.

## Falsifiers

- Subthreshold bit-access falsifier: a decoder for canonical images running in 2^{beta m+o(m)} time with beta<epsilon gives small circuits for every emitted table.
- Entropy-collapse falsifier: D_m growing with m makes delta<epsilon/(kappa(1+D_m)) vanish.
- Gap-collapse falsifier: nonconstant kappa in the source-length schedule removes any fixed E lower-bound exponent.
- Advice falsifier: choosing the hard canonical rank j_m nonuniformly without multiplexing or uniform ranking invalidates the target object.
- Cap falsifier: epsilon>alpha_V exceeds the verifier checkpoint/profile upper bound and makes the MCSP source unsound.
- Naturalness falsifier: adding dense random salt to make the image large restores constructivity plus largeness and falls into the natural-proofs obstruction.

## Learning

Cycle 32 isolates the access-profile parameter. Low distinct-image entropy does not itself leak small circuits; subthreshold random access does. The valid bridge is still delta<epsilon/(kappa(1+D)), but the source theorem must be sequentially explicit, bounded-image, cap-compatible, no-advice, and non-counting.

## Gedanken Experiment Design Seed

- Need decision: `design-now-as-falsifier-probe`
- Rationale: The branch needs to distinguish valid sequential explicitness from invalid random-access leakage; otherwise every proposed low-image MCSP carrier is either overrejected or circularly accepted.
- Situation seed: A canonical image carrier V_m with |I_m|=2^{0.1m}, kappa=1, and a claimed hard image of MCSP complexity above 2^{0.4m}; L_V multiplexes the image rank with the truth-table address.
- Varied variable: bit-access exponent beta for computing f_j(x) from (m,j,x), varied from 0.2 to 1.0 while D=0.1 and epsilon=0.4 stay fixed.
- Held-fixed controls: No advice in the rank selection or source-length schedule., Linear certificates and E-canonical distinct-image unranking remain available., The target language is the same multiplexed E language L_V., The claimed MCSP threshold is 2^{0.4m} and the source gap is kappa=1.
- Expected observation: For beta<0.4 the source is refuted because each image has circuits below the claimed threshold; for beta>=0.4 sequential evaluation remains compatible and the extracted lower-bound exponent can approach 0.4/1.1.
- Transfer certificate needed: A uniform proof that canonical unranking is E-computable, D<=0.1, alpha_V>=0.4, and at least one canonical image is 2^{0.4m}-hard without relying on a subthreshold decoder or nonuniform rank advice.

## Next Experiment

Try to construct or refute a toy bounded-D source from time-ordered proof transcripts where bit queries require near-full sequential replay; compute its checkpoint cap alpha_V and test whether any non-counting soundness argument can certify MCSP hardness.
