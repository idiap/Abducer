# cycle-0040

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: sound local certificate cover gate

## Candidate Lemma

Approximate sound-local-certificate covers are exact source-side falsifiers for the high-q generated-OR carrier. If H_N has a subthreshold SLC cover with few missed positive inputs, then H_N has subthreshold general circuits, so an N^{1+epsilon-o(1)} source lower bound must first rule out these covers.

## Definitions

- source object: H_N(x)=OR_{j<=M} SAT(G_N(x)_j), where x in {0,1}^N, M=floor(N^q), G_N emits M length-L 3CNFs, L=(log N)^d with d>1, and the source model is nonuniform fan-in-two Boolean circuits for H_N.
- target object: SAT on length L instances, with target consequence SAT notin P/poly obtained only through the separate substitution bridge when max{rho,q}<1+epsilon.
- controlled interface: a shared multi-output generator G_N of size N^{rho+o(1)} including output routing N^{q+o(1)}, followed either by SAT circuits or by local one-sided certificate predicates applied to generated formulas.
- target-preserving condition: q,rho<1+epsilon, q>(1+epsilon)/2 for dense-tuple blocking, L=(log N)^d with d>1 to avoid lookup collapse, and no nonuniform advice about x except through G_N outputs.
- An (K,E,s)-SLC cover is a family {(j_i,A_i)}_{i<=K} where j_i in [M], A_i is a size-s circuit on length-L 3CNF encodings, A_i(phi)=1 implies phi is satisfiable, and all but E inputs x with H_N(x)=1 have some i with A_i(G_N(x)_{j_i})=1.

## Assumptions

- epsilon>0 is fixed and all o(1) terms are with respect to N.
- C(G_N)<=N^{max{rho,q}+o(1)} as a shared multi-output circuit.
- Each local predicate is one-sided sound for SAT on all length-L 3CNFs, not merely on the generated range.
- Missed positive inputs may be patched nonuniformly by equality gates of size O(EN).

## Equations

- carrier: `H_N(x)=\bigvee_{j=1}^{\lfloor N^q\rfloor} SAT(G_N(x)_j),\qquad L=(\log N)^d.`. Valid when: Valid when the source carrier is the generated-OR family with shared generator outputs and length-L 3CNF instances.
- slc-upper-bound: `C(H_N)\le C(G_N)+O(K(s+L^{O(1)})+EN).`. Valid when: Valid when the SLC predicates are one-sided sound and miss only E positive carrier inputs.
- threshold-collapse-test: `K=N^\sigma,\ E=N^\delta,\ s=N^{o(1)},\ \max\{\rho,q,\sigma,1+\delta\}<1+\epsilon\ \Rightarrow\ C(H_N)<N^{1+\epsilon-o(1)}.`. Valid when: Valid when all four exponent contributions are bounded below the desired source lower-bound threshold.
- necessary-source-gate: `C(H_N)>N^{1+\epsilon-o(1)}\ \Rightarrow\ \text{every }N^{o(1)}\text{-local SLC cover has }K>N^{1+\epsilon-o(1)}\text{ or }E>N^{\epsilon-o(1)}.`. Valid when: Applies after q and rho are already fixed below the magnification threshold.

## Attempted Derivation

- Fix epsilon, q in ((1+epsilon)/2,1+epsilon), rho<1+epsilon, and L=(log N)^d with d>1.
- Define H_N as the OR of N^q generated 3CNF SAT instances and keep C(G_N)<=N^{max{rho,q}+o(1)} as the shared interface cost.
- Assume a (K,E,s)-SLC cover. Build a circuit that computes G_N(x), evaluates every A_i on its indexed formula G_N(x)_{j_i}, and ORs the K one-sided outputs.
- Soundness of A_i prevents false positives on H_N^{-1}(0); completeness except E positives leaves only E missed x values.
- Patch the E missed positive inputs by hardwired equality tests of size O(EN), giving C(H_N)<=C(G_N)+O(K(s+L^{O(1)})+EN).
- Therefore a proposed source lower bound C(H_N)>N^{1+epsilon-o(1)} must imply a superthreshold lower bound against SLC covers, not merely against explicit witnesses or partial terms.
- The old target bridge still works: if SAT has size n^c circuits, each length-L query costs L^c=N^{o(1)}, so H_N has size N^{max{rho,q}+o(1)}.

Blocking gap: No current argument proves that every one-sided local certificate predicate family of total size below N^{1+epsilon-o(1)} misses at least N^{epsilon-o(1)} positive bags on the actual generated range.

## Falsifiers

- falsifier: a subthreshold (K,E,N^{o(1)}) SLC cover with K<N^{1+epsilon-o(1)} and E<N^{epsilon-o(1)} gives an explicit small circuit for H_N.
- Low-width backdoor falsifier: if every positive emitted formula has a satisfying term of width b=alpha log N and q+alpha<1+epsilon, enumerating all such terms collapses the source lower bound.
- Compressed-certificate falsifier: a size-poly(L) one-sided predicate can represent many partial terms, so large term count alone is not a valid source certificate.
- Lookup-boundary falsifier: if L=O(log N) with q+2^L exponent below 1+epsilon, local truth-table predicates replace genuine SAT hardness.
- Generator-bias falsifier: if positives lie in a small easy satisfiable subclass such as Horn, 2-SAT, bounded-width, or bounded-backdoor CNFs, SLC cover size may be subthreshold.
- Nonuniform leakage falsifier: predicates A_i may contain advice tailored to the generated range; the source lower bound must defeat this advice rather than only uniform algorithms.

## Learning

Cycle 40 sharpens the source audit from partial certificate covers to approximate sound local certificate covers. The exact upper bound C(H_N)<=C(G_N)+O(K(s+L^{O(1)})+EN) makes any subthreshold SLC cover a concrete falsifier. The target bridge remains valid, but a contribution now requires a superthreshold lower bound against one-sided local predicates on the generated range, not just high witness or formula entropy.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The branch needs a concrete test for whether the partial-certificate gate is real or collapses through low-width local certificates while the target bridge remains valid.
- Situation seed: High-q generated-OR carrier where each positive emitted 3CNF has a planted satisfying term of width b=alpha log N, while negative emitted formulas are unsatisfiable and the generator size is N^{rho+o(1)}.
- Varied variable: alpha=b/log N, the logarithmic width exponent of the planted local certificate.
- Held-fixed controls: q is fixed in ((1+epsilon)/2,1+epsilon) so dense tuple leakage is threshold-blocked., rho<1+epsilon and C(G_N)<=N^{max{rho,q}+o(1)} are held fixed., L=(log N)^d with d>1 is held fixed to avoid the old exhaustive lookup collapse., The target substitution bridge uses only SAT circuits on length-L formulas and is not allowed extra advice about x.
- Expected observation: Enumerating all planted terms gives K<=N^q2^b=N^{q+alpha+o(1)}. If q+alpha<1+epsilon and missed positives are below N^epsilon, H_N has subthreshold circuits; if alpha crosses 1+epsilon-q, this particular falsifier disappears.
- Transfer certificate needed: A formal certificate that the planted terms are one-sided sound for all emitted formulas, cover all but E positive inputs, and can be checked after the shared generator with only poly(L) overhead; only then may the intuition enter the SLC proof obligations.

## Next Experiment

Compute the SLC cover exponent for generated formulas with bounded backdoor width b=alpha log N and for small semantic classes such as Horn, 2-SAT, and bounded-width CNF; identify whether the threshold alpha>=1+epsilon-q is achievable without destroying the SAT-substitution bridge.

# Barrier-Aware Lower-Bound Route: AC0 Depth-Leakage Gate

## Candidate Lemma

A fixed-depth AC0 lower bound for SAT is a valid restricted-class separation, but it implies SAT notin P only after a target-preserving simulation that compiles the alleged P-time SAT decider into the same fixed-depth AC0 model below the lower-bound threshold.

## Definitions

- source object: length-m Boolean slice SAT_m of a standard SAT encoding, together with a lower bound L_d(m) against depth-d unbounded-fan-in De Morgan circuits of size s.
- target object: SAT notin DTIME(m^k), hence route-level progress toward NP not subset P only after quantifying over every fixed k.
- controlled interface: a uniform depth-preserving compiler Sim_{k,d} mapping any m^k-time SAT decider to depth-d AC0 circuits of size B_{k,d}(m) on the identical length-m encoding.
- target-preserving condition: L_d(m)>B_{k,d}(m) for all sufficiently large m, with no nonuniform advice leakage, promise change, padding change, or replacement of SAT by an easier restricted language.

## Assumptions

- d is fixed independently of m unless explicitly varied.
- The AC0 model is standard De Morgan AC0 with NOT gates at inputs and unbounded fan-in AND/OR gates.
- The lower bound is for the same SAT slice that the alleged polynomial-time algorithm decides.
- The compiler must be uniform enough that a P algorithm cannot hide depth in advice or preprocessing.

## Equations

- conditional_compilation: `SAT \in DTIME(m^k) \ \land\ B_{k,d}(m)\le s(m)\ \Rightarrow\ SAT_m \in AC0_d[s(m)]`. Valid when: Applies after the alleged SAT algorithm is uniformly compiled into depth-d unbounded-fan-in circuits with identical encodings and no advice.
- transfer_threshold: `L^{AC0_d}_{SAT}(m)>B_{k,d}(m)\ \Rightarrow\ SAT \notin DTIME(m^k)`. Valid when: Requires the target-preserving simulation above for this specific SAT language and all sufficiently large input lengths.
- parity_falsifier_bound: `size_{AC0_d}(PARITY_m)\ge 2^{c_d m^{1/(d-1)}}`. Valid when: Valid for each fixed depth d at least two in the standard De Morgan AC0 model with unbounded fan-in gates.
- p_membership_not_ac0_membership: `PARITY\in P\ \land\ PARITY_m\notin AC0_d[2^{o(m^{1/(d-1)})}]`. Valid when: Applies to the same fixed-depth model and shows that P membership need not imply small AC0 circuits.

## Attempted Derivation

- Model the source as a claimed lower bound L_d(m) for SAT_m against AC0_d size s.
- Assume for contradiction that SAT is decidable in time m^k.
- A P-time decider yields P-uniform Boolean circuits of polynomial size and polynomial depth, not fixed depth d.
- To contradict the AC0_d lower bound one must reduce those circuits to depth d with size B_{k,d}(m)<L_d(m).
- No such depth-preserving reduction is known or plausible as a black-box statement; PARITY in P violates any universal version.
- The derivation therefore proves only SAT notin AC0_d[s], a restricted-class separation already outside the P-vs-NP target.

Blocking gap: Missing SAT-specific depth-preserving simulation from DTIME(m^k) to AC0_d below the lower-bound threshold.

## Falsifiers

- PARITY is a concrete falsifier: it lies in P but requires size 2^{Omega(m^{1/(d-1)})} for fixed-depth AC0_d.
- Any proof rule saying superpolynomial AC0 lower bounds imply nonmembership in P would falsely separate PARITY from P.
- The truth-table DNF upper bound O(m2^m) dominates sub-2^m lower bounds, causing quantitative threshold collapse without a sharper SAT-specific compiler.
- A valid AC0 lower bound for SAT remains useful for restricted-circuit complexity but is not evidence for P != NP by itself.

## Learning

Cycle 40 isolates a valid target gate for constant-depth lower-bound routes. Fixed-depth AC0 lower bounds, even exponential ones for explicit P functions, do not transfer to P != NP without a SAT-specific depth-preserving compiler below the lower-bound threshold. Padded parity supplies the falsifier and the quantitative obstruction is B_{k,d}(m), not the lower-bound slogan.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for constant-depth lower-bound transfers.`
- Rationale: Recent cycles audited restricted target models; AC0 is the canonical case where a strong-looking explicit lower bound loses the P target through depth leakage rather than through relativization folklore.
- Situation seed: For each length m, compare SAT_m with PADPAR_{m,beta}(z0^{m-m^beta})=PARITY_{m^beta}(z). PADPAR is in linear time after ignoring padding but inherits a fixed-depth AC0 lower bound from parity on m^beta live variables.
- Varied variable: beta in (0,1], the exponent of the live parity core inside the padded length-m input.
- Held-fixed controls: Fixed depth d De Morgan AC0 with unbounded fan-in and input NOT gates only., Uniform length-m encoding and no nonuniform advice or promise change., Target class remains DTIME(m^k) or P, not AC0., Lower-bound comparison uses size as the only resource threshold.
- Expected observation: PADPAR remains in P for every beta, while size_AC0_d(PADPAR) is at least 2^{Omega(m^{beta/(d-1)})}. Thus arbitrarily large-looking fixed-depth lower bounds coexist with P membership, exposing the invalid transfer.
- Transfer certificate needed: A SAT-specific, nonblack-box compiler showing that if SAT has an m^k-time algorithm then SAT_m has depth-d AC0 circuits of size below L_d(m), while explaining why the padded-parity falsifier is excluded.

## Next Experiment

Audit formula-size and NC1 lower-bound routes next: state the p-simulation needed from P to formulas/NC1, test CVP or another P-complete language as the falsifier, and quantify the depth/size threshold where the transfer collapses.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Restriction-only direct MCSP row certificates cannot be a valid source for the low-D carrier at constant threshold. If a certificate for a row T:{0,1}^m->{0,1} uses only t labeled positions of T as its semantic evidence, then for t << 2^{epsilon m}/m those labels are consistent with some unrestricted circuit of size at most 2^{epsilon m}. Thus such a certificate cannot soundly prove MCSP(T)>2^{epsilon m}.

## Definitions

- source object: a restriction-only direct MCSP row certificate, consisting of a canonical row T_m and t(m) labeled positions (x_j,T_m(x_j)), with no global lower-bound invariant beyond those labels.
- target object: a no-side MCSP claim MCSP_m(T_m)>s_m for unrestricted Boolean circuits of size s_m=2^{epsilon m}.
- controlled interface: the verifier may use the listed labels and E-uniform row emission, but its soundness argument reduces to the nonexistence of a small circuit consistent with those labels.
- target-preserving condition: the source remains O(m)-described, E-time checkable, advice-free, and intended to feed the existing low-D carrier transfer with delta<epsilon/(kappa(1+D)).

## Assumptions

- Unrestricted Boolean circuits over m inputs are the target lower-bound model.
- The certificate is restriction-only: all row-dependent semantic information is a set of labeled examples.
- epsilon>0 is constant and s_m=2^{epsilon m}.
- The carrier may have low distinct-image entropy D, but the falsifier acts before multiplexing.

## Equations

- interpolation_upper_bound: `\operatorname{SIZE}(H,b) \le A\,t\,m+O(t\log t)`. Valid when: Valid when H contains t Boolean inputs of length m and arbitrary labels are interpolated by unrestricted DNF or decision-tree circuits.
- restriction_falsifier_threshold: `t(m) < s_m/(2Am) \;\Rightarrow\; \exists C\;(|C|\le s_m \wedge C|_{H}=b)`. Valid when: Applies when the verifier's only semantic obstruction to small circuits is consistency with the listed labeled positions.
- constant_threshold_sample_cost: `s_m=2^{\epsilon m} \;\Rightarrow\; t_{\min}(m)=\Omega(2^{\epsilon m}/m)`. Valid when: Requires a constant MCSP threshold against unrestricted circuits and a restriction-only source certificate model.

## Attempted Derivation

- Start with a low-image carrier family R_m={T_1,...,T_M}, M<=2^{Dm+o(m)}, and try to certify one hard row by an O(m)-bit seed selecting t sampled inputs H={x_1,...,x_t}.
- Let the certificate provide or derive the labels b_j=T_i(x_j), and let the verifier attempt to use the assertion that no size-s_m circuit matches all pairs (x_j,b_j).
- For any H and labels b, build an interpolating DNF: for each positive labeled point add its m-literal minterm, and set arbitrary values off H. This has size O(tm), with a similar bound for all label patterns.
- If t<s_m/(A m), the interpolating circuit has size below s_m, so the sampled constraints are compatible with a small circuit regardless of the true row complexity.
- For s_m=2^{epsilon m}, any restriction-only certificate must therefore expose Omega(2^{epsilon m}/m) labeled positions, far beyond O(m) certificate length and not compatible with the intended sparse source interface.

Blocking gap: The argument refutes only restriction-only or sampled-label certificates. A genuinely global proof invariant, arithmetized lower-bound certificate, or non-natural proof system is outside this falsifier and remains open.

## Falsifiers

- restriction-only direct row certificates with t<2^{epsilon m}/O(m) labeled examples are falsified by interpolation
- aggregate row-forcing below q_force=(D+epsilon)/(1+D) is a quantitative falsifier for row hardness
- uniform-only or restricted-circuit aggregate lower bounds do not certify unrestricted MCSP no-side rows
- nonuniform row selection or length selection invalidates the target E lower-bound consequence
- ranked random access to rows below exponent epsilon/(1+D) leaks circuits and breaks the source soundness
- dense constructive high-MCSP properties re-enter the natural-proofs falsifier unless sparsity/non-largeness is preserved

## Learning

Cycle 40 adds a concrete source-side no-go theorem: subthreshold point evidence cannot certify a direct hard MCSP row, because arbitrary labels on t positions have unrestricted circuits of size O(tm). Thus the viable low-D route must find a global, non-natural, advice-free proof invariant for unrestricted row hardness; the existing extraction bridge stays valid but gains a sharper falsifier.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for direct-row source proposals.`
- Rationale: The branch must decide whether tiny-D direct row hardness can be certified by short sampled evidence. Interpolation gives a concrete threshold, not another hardness-magnification restatement.
- Situation seed: A canonical low-image MCSP carrier with M=2^{Dm} rows; a proposed O(m)-bit certificate picks sampled positions in one row and claims these samples rule out all circuits of size s=2^{epsilon m}.
- Varied variable: sample exponent theta in t=2^{theta m}/m, ranging from theta=0 for O(m) samples to theta=epsilon at the interpolation threshold.
- Held-fixed controls: epsilon is a fixed constant MCSP threshold for unrestricted circuits, D is tiny and fixed so the existing multiplexing loss is 1+D, kappa-dense source lengths and advice-free E-uniform canonical unranking are preserved, the target consequence remains an E lower bound with delta<epsilon/(kappa(1+D))
- Expected observation: For theta<epsilon, every sampled pattern is interpolable by a circuit of size below 2^{epsilon m}; at theta=epsilon the sample transcript becomes exponentially large and no longer fits the short-certificate carrier interface.
- Transfer certificate needed: Before sampled intuition may affect proof obligations, one must provide a global non-restriction soundness certificate for unrestricted circuit lower bounds, or prove that the verifier uses information not reducible to subthreshold labeled examples.

## Next Experiment

Audit proof-complexity carriers for statements of the form forall size-2^{epsilon m} circuits C, C != T: separate resolution/IPS/arithmetized certificates from restriction-only evidence, and compute whether their verifier leaks row circuits or stays within the low-D E-transfer budget.
