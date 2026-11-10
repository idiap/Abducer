# cycle-0051

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization - cycle 51 direct-sum demagnification audit

## Candidate Lemma

For the polylog-query generated-OR carrier, any target-preserving source lower bound that factors through a per-slot SAT_L lower bound with at most linear direct-sum gain is demagnifying: it must prove SAT_L requires g_N=N^{1+epsilon}/M_N=L^{omega(1)} size circuits. Thus this subroute is not a barely-superlinear source route, although the target substitution bridge remains valid.

## Definitions

- source object: H_N(x)=OR_{j<=M_N} SAT(G_{N,j}(x)), where |x|=N, M_N=N^{q_N}, each generated formula has length L=(log N)^d with d>1, and the generator has circuit cost at most N^{rho+o(1)}.
- target object: SAT notin P/poly, inferred only by substituting hypothetical L^c-size SAT circuits into every generated slot of H_N and contradicting C(H_N)>N^{1+epsilon}.
- controlled interface: a source certificate of the form C(H_N)>=M_N b(L)/N^{o(1)}, where b(L) is a lower bound for the length-L SAT predicate or a promise restriction of it on generated slots.
- target-preserving condition: rho<1+epsilon and g_N=N^{1+epsilon}/M_N dominates L^c for every fixed c, with no per-length advice or generator leakage outside the H_N input.

## Assumptions

- Boolean nonuniform circuit size is the source lower-bound model.
- The only target upper bound used is SAT_L in SIZE(L^c) for an arbitrary fixed c.
- The direct-sum certificate pays at most a linear factor M_N for M_N generated SAT slots and no superlinear aggregation theorem is assumed.
- Lower-order generator and wiring costs are N^{o(1)} relative to the named exponents.

## Equations

- target_substitution_upper_bound: `C(H_N) \le N^{\rho+o(1)} + M_N L^{c+O(1)}`. Valid when: Valid when the generator circuit is shared once and each generated SAT query is answered by the same length-L circuit family.
- target_gap: `g_N := \frac{N^{1+\epsilon}}{M_N}=N^{1+\epsilon-q_N}`. Valid when: Applies when the carrier threshold is N^{1+epsilon} and the OR fan-in is M_N=N^{q_N}.
- p_poly_preservation: `\forall c\; M_N L^c=o(N^{1+\epsilon}) \quad\Longleftrightarrow\quad \forall c\; L^c=o(g_N)`. Valid when: Valid when the target consequence is SAT notin P/poly rather than exclusion of only one fixed exponent.
- direct_sum_source_requirement: `M_N b(L)/N^{o(1)} > N^{1+\epsilon} \quad\Rightarrow\quad b(L) > g_N/N^{o(1)}`. Valid when: Requires the proposed source lower bound to factor through M_N local SAT costs with only subpolynomial losses.
- fixed_gap_demagnification: `q_N\le 1+\epsilon-\delta \Rightarrow g_N\ge 2^{\delta L^{1/d}-o(L^{1/d})}`. Valid when: Valid when d>1 is fixed and logarithms define L=(log N)^d up to constant factors.

## Attempted Derivation

- Let M_N=N^{q_N} and L=(log N)^d. Under SAT_L in SIZE(L^c), substitute one SAT circuit into every generated slot; this gives C(H_N)<=N^{rho+o(1)}+M_N L^{c+O(1)}.
- To contradict a source lower bound C(H_N)>N^{1+epsilon}, the carrier must satisfy rho<1+epsilon and M_N L^c=o(N^{1+epsilon}) for each fixed c. Equivalently g_N=N^{1+epsilon}/M_N is L^{omega(1)}.
- Assume the source proof factors through a per-slot SAT lower bound b(L) with at most linear aggregation: C(H_N)>=M_N b(L)/N^{o(1)}.
- For this to exceed N^{1+epsilon}, it must have b(L)>g_N/N^{o(1)}.
- Combining the target-preserving condition with the source requirement forces b(L)=L^{omega(1)}. For fixed q_N<=1+epsilon-delta, it forces b(L)>=2^{Omega(L^{1/d})}.
- Therefore projection-slice proofs and direct-sum-from-SAT proofs do not realize weak hardness magnification for this carrier.

Blocking gap: This proves only a quarantine for factorized source certificates. It does not rule out a genuinely aggregate arbitrary-circuit lower bound for H_N or a nonrelativizing extraction theorem using real SAT structure.

## Falsifiers

- direct-sum demagnification falsifier: a source proof of the form M_N b(L) requires b(L)>g_N, while target preservation requires g_N=L^{omega(1)}.
- projection-slice falsifier: the special case M_N=1 demands a length-L SAT lower bound of size N^{1+epsilon}=2^{Omega(L^{1/d})}.
- near-boundary finite-exponent falsifier: if g_N=L^B, the bridge is valid only against SAT circuits of exponent below B-O(1), not against P/poly.
- relativizing separator falsifier: hard one-sided local separators can coexist with tiny H_N circuits in the planted-control oracle.
- nonuniform sharing falsifier: multiple editable slices do not by themselves yield an M_N-fold lower bound for arbitrary circuits without an explicit direct-sum theorem.

## Learning

Cycle 51 identifies a new quantitative conservation law: the same gap g_N that protects the target transfer against all SAT polynomial exponents becomes the per-slot lower-bound burden for any direct-sum source proof. Hence slot-wise SAT hardness cannot be the weak source; a valid route must prove aggregate H_N hardness or supply a nonrelativizing extraction theorem.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for direct-sum and slice-based source lower bounds.`
- Rationale: The remaining route needs a real source lower bound for H_N. Before searching for one, we must separate valid aggregate lower bounds from demagnifying proofs that merely repackage SAT_L hardness.
- Situation seed: Consider H_N^g with M_N=N^{1+epsilon}/g(L) editable generated slots of length L=(log N)^d, each slot capable of carrying an arbitrary SAT instance while all other slots can be neutralized to fixed unsatisfiable formulas. The generator cost is kept at N^{rho+o(1)}.
- Varied variable: The gap function g(L)=N^{1+epsilon}/M_N, varied from L^B to L^{omega(1)} and to 2^{Theta(L^{1/d})}.
- Held-fixed controls: d>1 and L=(log N)^d remain fixed., rho<1+epsilon so generator cost is below the source threshold., The target substitution uses the same hypothetical SAT_L circuit of size L^c in every slot., No exponent-dependent advice is allowed in the carrier family.
- Expected observation: When g(L)=L^B, the bridge excludes only finitely many SAT circuit exponents. When g(L)=L^{omega(1)}, the bridge is P/poly-preserving, but any slot-wise direct-sum source proof must prove b(L)>g(L), a superpolynomial SAT_L lower bound.
- Transfer certificate needed: A valid next certificate must be an aggregate arbitrary-circuit lower bound for H_N or a nonrelativizing real-SAT extraction theorem with loss below the g(L) gap; a restriction to individual slots is insufficient.

## Next Experiment

Try to formalize an aggregate lower-bound normal form for H_N that distinguishes global OR computation from M_N independent SAT_L copies, and test it against the planted-control oracle before using separator hardness.

# Barrier-Aware Lower-Bound Route: certificate-complexity threshold collapse

## Candidate Lemma

Ordinary coordinate certificate complexity is a valid circuit lower-bound interface only up to linear size; it is an invalid carrier for polynomial-size SAT lower bounds with exponent k>1.

## Definitions

- source object: ordinary Boolean certificate complexity C(f_m) of a total m-bit language slice, including SAT_m or padded SAT variants.
- target object: nonuniform fanin-two Boolean circuit lower bound f_m notin SIZE(m^k) for a fixed k>1.
- controlled interface: convert any size-S circuit and input x into a coordinate certificate of size at most O(S) by following a proof tree for the output value.
- target-preserving condition: the certificate lower bound must exceed m^k on the same length-m encoding without ignoring padding or changing to a promise model.
- C_b(f) is the maximum, over b-inputs x, of the minimum number of input coordinates fixed as in x that force output b.
- C(f)=max(C_0(f),C_1(f)); certificates are input-coordinate restrictions, not NP witnesses or proof-system certificates.

## Assumptions

- Circuits have bounded fanin over a De Morgan basis, with internal negations pushed or handled by value recursion at constant-factor cost.
- The language slice is total on all m-bit strings; no promise restriction may discard hard extensions.
- The intended target is SIZE(m^k) on the actual encoded input length m.

## Equations

- certificate_complexity_definition: `C_b(f)=\max_{x:f(x)=b}\min\{|I|:\forall y\,(y_I=x_I\Rightarrow f(y)=b)\}`. Valid when: Valid when certificates are ordinary fixed-coordinate restrictions of total Boolean functions on the full input cube.
- circuit_to_certificate: `f\in SIZE(S)\ \Longrightarrow\ C(f)\le cS`. Valid when: Valid when the circuit basis has bounded fanin and the proof tree for each gate value is charged to circuit gates or wires.
- universal_ceiling: `C(f)\le m\quad\text{for every total }f:\{0,1\}^m\to\{0,1\}`. Valid when: Valid when all m input coordinates may be fixed, so every point has a trivial full assignment certificate.
- polynomial_threshold_collapse: `C(SAT_m)>m^k\text{ is impossible for every fixed }k>1\text{ and all large }m`. Valid when: Applies when the target lower bound is measured against polynomial circuit size on the same m-bit SAT encoding.

## Attempted Derivation

- Define C_b(f) as the largest minimum coordinate restriction forcing value b on any b-input.
- Given a size-S bounded-fanin circuit and an input x, recursively certify the output gate value: for AND=1 certify both children, for AND=0 certify one false child, and dually for OR; NOT gates only flip the required child value.
- The recursion touches at most O(S) gates or wires, so the reached literals form a valid coordinate certificate consistent with x.
- Therefore C(f)>cS implies f notin SIZE(S), giving a legitimate but quantitatively weak lower-bound bridge.
- Every total m-bit function has the trivial certificate obtained by fixing all m input bits, hence C(f)<=m.
- For target SIZE(m^k) with k>1, the required source inequality C(SAT_m)>m^k contradicts the universal ceiling; padding makes the mismatch worse because ignored padding contributes to M^k but not to C.

Blocking gap: There is no remaining derivation gap for the route lemma; the blocking gap is structural: ordinary coordinate certificates are universally capped by input length and cannot reach polynomial circuit thresholds beyond linear size.

## Falsifiers

- falsifier: PARITY_m has C_0=C_1=m but has linear-size XOR circuits, so maximal ordinary certificate complexity is compatible with P and small nonuniform circuits.
- falsifier: PadSAT_{r,beta} remains NP-hard under padding reductions while C<=r, far below the padded target threshold M^k for beta>1 and fixed k.
- falsifier: every total m-bit function satisfies C<=m, so any claimed ordinary-certificate lower bound above m is not a valid mathematical assertion.
- falsifier: one-sided NP witnesses for satisfiable formulas are not coordinate certificates for the SAT truth-table input encoding; conflating them invalidates the transfer.

## Learning

Cycle 51 converts certificate-complexity enthusiasm into a precise threshold gate. The bridge C(f)>S => f notin SIZE(S) is valid, but ordinary coordinate certificate complexity is always at most the input length m, so it cannot certify SIZE(m^k) lower bounds for k>1. Padding supplies a concrete target-preserving falsifier: NP-hardness survives while the certificate threshold erodes relative to the padded circuit-size parameter. This is route-level progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: Certificate-based routes often look target-preserving because SAT has semantic witnesses; padding exposes whether the source measure is tied to the actual circuit input length or only to the unpadded core.
- Situation seed: For each core length r and exponent beta, define PadSAT_{r,beta}(u,z)=SAT_r(u) on M=r+r^beta bits, with z ignored, and keep the usual padding reduction from SAT to PadSAT.
- Varied variable: padding exponent beta
- Held-fixed controls: The target class remains nonuniform bounded-fanin SIZE(M^k) for a fixed k>1., The source measure remains ordinary coordinate certificate complexity on the total M-bit Boolean function., The reduction preserves NP-hardness only by padding and does not introduce a promise., Circuit size is always measured in the actual padded input length M.
- Expected observation: As beta grows, C(PadSAT_{r,beta})<=r while M^k grows as r^{beta k}; the certificate route loses quantitative contact with the target even though NP-hardness is preserved.
- Transfer certificate needed: A valid repair would need a non-coordinate or compression-resistant certificate notion plus a proven circuit-to-certificate simulator whose bound exceeds M^k without being defeated by ignored padding.

## Next Experiment

Audit essential-variable and junta-dimension lower-bound routes: prove the compiler bound for SIZE(m^k), compute the universal ceiling m, and test padded SAT as the falsifier before considering any P-vs-NP transfer.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Patch smoothness is a valid MCSP-source falsifier only when rooted at a subthreshold row. If T is obtained from an anchor A by a hardwirable patch path of cumulative volume P, then C(T)<=C(A)+O(mP). Thus an accepted row claimed to have MCSP threshold 2^{epsilon m} is invalid when C(A)<=2^{a m}, P<=2^{beta m}, and max(a,beta)<epsilon. Unrooted smooth traversal among unknown-hard rows does not by itself give a circuit upper bound.

## Definitions

- source object: a low-D MCSP carrier image U_m={T_{m,r}:r<2^{D m+O(1)}} of N=2^m bit truth tables, produced by a no-advice E-uniform verifier or sequential enumerator.
- target object: a multiplexed E-language F_m(r,x)=T_{m,r}(x) padded across kappa-dense source lengths, intended to inherit an unrestricted circuit lower bound.
- controlled interface: the rank/certificate-to-row map together with any decoder, restart schedule, edit path, patch tree, or canonical construction transcript used to expose row bits.
- target-preserving condition: distinct-image entropy D, MCSP threshold S_m=2^{epsilon m}, padding loss kappa, and E-uniform length selection are preserved without nonuniform advice.
- patch path: a rooted tree path whose edge labels are coordinate sets on which the truth table is flipped; duplicates cancel mod 2.
- hardwirable volume: the number P of distinct or listed patched m-bit coordinates along the path, since an unrestricted circuit may hardwire them.

## Assumptions

- A and T are Boolean truth tables on m input bits, so equality to a patched coordinate has O(m) circuit cost.
- The anchor A has unrestricted circuit size at most 2^{a m+o(m)}.
- The cumulative patch volume from A to T is at most 2^{beta m+o(m)}.
- The proposed MCSP no-side threshold is S_m=2^{epsilon m}.
- No uniform random access to T is assumed; the circuit upper bound uses hardwired coordinates only.

## Equations

- carrier_parameters: `N_m=2^m,\quad S_m=2^{\epsilon m},\quad |U_m|\le 2^{Dm+O(1)}`. Valid when: Valid when the carrier rows are length N=2^m truth tables and D, epsilon are fixed constants.
- patch_upper_bound: `C(T)\le C(A)+O(mP)`. Valid when: Valid when T differs from A on at most P hardwirable coordinates of the same m-bit domain.
- rooted_leakage_threshold: `C(A)\le 2^{am+o(m)},\ P\le 2^{\beta m+o(m)}\Rightarrow C(T)\le 2^{\max(a,\beta)m+o(m)}`. Valid when: Valid when equality tests to all patched coordinates may be hardwired in unrestricted circuits.
- hardness_propagation_reverse: `C(A)>S_m+O(mP)\Rightarrow C(T)>S_m`. Valid when: Valid when A and T are connected by the same patch list and P is below the threshold slack.
- source_soundness_gate: `\max(a,\beta)\ge \epsilon-o(1)`. Valid when: Valid when the row T is asserted to be on the MCSP no-side at threshold 2^{epsilon m}.

## Attempted Derivation

- Fix m, a candidate row T, and an anchor A on the same m-bit domain.
- Let P be the cumulative patch multiset on a construction path from A to T; T(x)=A(x) xor parity_{y in P}[x=y].
- Build an unrestricted circuit for T by computing A(x), comparing x with every hardwired y in P, and xoring the comparison bits.
- The size is C(A)+O(mP), giving C(T)<=2^{max(a,beta)m+o(m)} when C(A)<=2^{am+o(m)} and P<=2^{beta m+o(m)}.
- Therefore rooted smooth repairs from any easy anchor are formal falsifiers for MCSP no-side soundness above 2^{epsilon m}.
- Conversely, the same inequality gives C(A)<=C(T)+O(mP); hence if A is hard and P is subthreshold, T can remain hard. Smooth unrooted traversal alone was not a valid obstruction.
- Apply the prior multiplex argument only after a separate source certificate supplies at least one row not defeated by rooted edit leakage, interval leakage, or advice leakage.

Blocking gap: No current construction gives a no-advice E-uniform low-D carrier with a hard row and a proof that the row is not reachable from any subthreshold anchor by a subthreshold rooted patch tree.

## Falsifiers

- rooted-edit-tree falsifier: every claimed hard row is reachable from a subthreshold anchor by cumulative patch volume below 2^{epsilon m-o(m)}
- anchor leakage falsifier: the construction starts from zero, one, parity, a small PRG row, or a rankable profile filler and performs fewer than 2^{epsilon m}/poly(m) hardwirable changes
- nonuniform selector falsifier: the only hard row index is supplied as advice rather than by E-uniform canonical unranking or an existential multiplex argument
- dense-naturalization falsifier: the repair gives a large poly(N)-decidable property useful against 2^{epsilon m}-size circuits
- interval decoder falsifier: indexed block restart computes row bits with alpha_int<epsilon
- unbounded image-entropy falsifier: distinct-image entropy D is not constant, collapsing the delta<epsilon/(kappa(1+D)) transfer
- threshold-collapse falsifier: epsilon exceeds the verifier cap alpha_V or tends to zero after padding

## Learning

Cycle 51 repairs the previous rank-jump claim. The exact valid obstruction is rooted edit leakage: C(T)<=C(A)+O(mP). Low-volume edits from an easy anchor falsify MCSP soundness, but unrooted smooth traversal can also propagate hardness from a hard anchor and is not by itself a proof failure. The surviving route now needs a low-D, no-advice, cap-compatible carrier with a hard row and a rooted-edit-hardness certificate.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The branch has a concrete ambiguity: cycle 50 treated rank smoothness as leakage, but the valid obstruction depends on an easy root. A target-preserving thought experiment separates rooted edit leakage from harmless unrooted smoothness.
- Situation seed: Take M=2^{D m} random N=2^m truth tables conditioned to avoid all Hamming balls of radius 2^{epsilon m}/m around circuits of size below 2^{epsilon m}. Try to E-uniformize them by a sequential repair walk either rooted at zero or rooted at an unspecified random seed, then multiplex ranks with inputs.
- Varied variable: rooted cumulative patch exponent beta, where each row is reached from the chosen anchor by at most 2^{beta m} hardwirable coordinate changes.
- Held-fixed controls: MCSP threshold S_m=2^{epsilon m} with constant epsilon below the verifier cap, distinct-image entropy D is constant and rank unranking is no-advice E-uniform, padding density loss kappa is fixed, the target consequence is only the conditional E lower-bound exponent delta<epsilon/(kappa(1+D)), no dense poly(N)-decidable hardness property is introduced
- Expected observation: For beta<epsilon and an easy anchor, every repaired row has small circuits by hardwired patches, so the source is invalid. For an unrooted or hard-anchor walk, smoothness alone should not refute the source; it merely shifts the burden to certifying the anchor's MCSP hardness without advice or naturalization.
- Transfer certificate needed: A formal rooted-edit-hardness certificate: either prove a hard anchor by a non-natural no-advice argument, or prove that every subthreshold-anchor patch tree reaching the selected image has volume at least 2^{epsilon m-o(m)} before invoking the multiplex extraction.

## Next Experiment

Formalize rooted-edit-hardness as a min-cut/cover parameter over subthreshold circuit anchors and test whether random robust low-D carriers have large rooted-edit distance while admitting any E-uniform canonical selector.
