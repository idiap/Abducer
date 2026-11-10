# cycle-0052

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: XOR Carrier Repair

## Candidate Lemma

Parity aggregation over polylog-length generated SAT queries gives a valid target-preserving magnification bridge: an i.o. unrestricted circuit lower bound C(H_N^oplus)>N^{1+epsilon} for a target-clean carrier with max{q,rho}<1+epsilon implies SAT notin P/poly, hence NP not subset P/poly. This is route-level only; the source lower bound is unproved.

## Definitions

- source object: the N-bit carrier H^{oplus}_{N,G}(x)=oplus_{j<=M} SAT(G_{N,j}(x)) with M=N^q and query length L=(log N)^d.
- target object: SAT on length-L inputs and the target consequence SAT notin P/poly, hence NP not subset P/poly by completeness.
- controlled interface: replace each generated SAT query by one length-L SAT circuit and compute the outer XOR with fan-in M.
- target-preserving condition: fixed d,q,rho,epsilon with L=N^{o(1)}, C(G_N)<=N^rho, max{q,rho}<1+epsilon, and no generator advice encoding SAT labels.

## Assumptions

- Source lower-bound model is unrestricted nonuniform Boolean circuits on N input bits.
- The lower bound C(H^{oplus}_{N,G})>N^{1+epsilon} holds for infinitely many N.
- G_N outputs M length-L SAT encodings and is computable by circuits of size at most N^rho.
- The outer XOR tree and fanout are charged in the circuit-size accounting.

## Equations

- carrier_definition: `H^{\oplus}_{N,G}(x)=\bigoplus_{j=1}^{M} SAT(G_{N,j}(x)),\quad M=N^q,\quad L=(\log N)^d.`. Valid when: Valid when G_{N,j} output length-L encodings of SAT instances and the XOR fan-in M is explicitly charged.
- substitution_upper_bound: `C(H^{\oplus}_{N,G})\le C(G_N)+O(M\cdot(s(L)+L)+M).`. Valid when: Applies after one size-s(L) SAT circuit is substituted into every generated query without advice depending on x.
- polylog_transfer: `s(L)\le L^c,\ C(G_N)\le N^{\rho}\ \Rightarrow\ C(H^{\oplus}_{N,G})\le N^{\max\{\rho,q\}+o(1)}.`. Valid when: Valid when d is fixed, c is fixed, and L=(log N)^d remains N^{o(1)}.
- target_consequence: `\big(C(H^{\oplus}_{N,G})>N^{1+\epsilon}\ \mathrm{i.o.}\ \wedge\ \max\{\rho,q\}<1+\epsilon\big)\Rightarrow SAT\notin P/poly.`. Valid when: Requires the lower bound on the source carrier for infinitely many N and the target-preserving threshold gap to be fixed.

## Attempted Derivation

- Kept the polylog query window L=(log N)^d with d>1 so SAT polynomial-size circuits substitute as N^{o(1)} per query and exhaustive lookup is not automatically subthreshold.
- Replaced the generated-OR carrier by H_N^oplus, the parity of M=N^q generated SAT labels.
- Computed the target transfer C(H_N^oplus)<=C(G_N)+O(M(s(L)+L)+M), yielding N^{max{rho,q}+o(1)} under SAT in SIZE(L^c).
- Checked the previous one-sided separator machinery: it decides existential positivity of OR-bags but loses the parity of the number of satisfiable slots, so it cannot certify or refute XOR hardness without extra label information.
- Isolated the new leakage normal form: any small feature or affine sketch plus sparse corrections gives an exact subthreshold circuit for H_N^oplus.

Blocking gap: There is no nonrelativizing theorem extracting a parity sketch, low-rank transcript, or other analyzable normal form from an arbitrary small circuit for H_N^oplus; direct C(H_N^oplus)>N^{1+epsilon} remains unproved.

## Falsifiers

- threshold collapse: max{q,rho}>=1+epsilon destroys the target-preserving gap
- polylog lookup collapse when d<=1 and q plus the lookup exponent falls below 1+epsilon
- nonuniform leakage from G_N that encodes SAT labels instead of generating target-clean queries
- subthreshold affine-sketch or feature-aggregator predictor for H_N^oplus with fewer than N^epsilon patchable errors
- complete per-slot promise solver on the generated range of total size below N^{1+epsilon}
- natural-proof style source argument that is dense and constructive against N^{1+epsilon} circuits under standard pseudorandomness assumptions

## Learning

Cycle 52 contributes a concrete repair: XOR aggregation preserves the valid polylog-query magnification threshold while invalidating the OR-specific one-sided separator obstruction. The new source burden is sharper: prove aggregate parity-carrier hardness or rule out subthreshold parity sketches and sparse corrections. This is route-level progress only, with explicit falsifier tests.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The OR branch is blocked by relativizing one-sided separator extraction. The XOR carrier tests whether that obstruction was an artifact of existential aggregation while preserving the exact SAT-substitution threshold.
- Situation seed: Fix a target-clean generator G_N producing M=N^q SAT instances of length L=(log N)^d with d>1, and study H_N^oplus(x)=oplus_j SAT(G_{N,j}(x)) under unrestricted N-bit circuits.
- Varied variable: affine sketch dimension tau, where A_N(x) has N^tau output bits and B_N(A_N(x)) attempts to predict the parity of the generated SAT labels.
- Held-fixed controls: q<1+epsilon and rho<1+epsilon so the target bridge stays valid, d>1 so exhaustive SAT lookup on length-L queries is not a subthreshold falsifier, G_N has no SAT-label advice and its circuit cost is charged, the source lower-bound target remains exact C(H_N^oplus)>N^{1+epsilon} infinitely often
- Expected observation: If tau and the sketch/postprocessor sizes stay below 1+epsilon with fewer than N^epsilon errors, sparse patching kills the source lower bound. If random-like generators resist all such sketches, the OR separator obstruction is avoided but a direct arbitrary-circuit lower bound is still needed.
- Transfer certificate needed: A non-natural direct lower bound for H_N^oplus, or a nonrelativizing normal-form theorem showing every subthreshold H_N^oplus circuit yields a subthreshold parity sketch with loss below the gap 1+epsilon-max{q,rho}.

## Next Experiment

In the ideal random-label model for G_N, count subthreshold affine sketches of size N^alpha and estimate the tau,alpha,error threshold at which a union bound could certify parity-sketch resistance without pretending to prove the actual explicit carrier lower bound.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Noise sensitivity gives a valid quantitative bridge only to circuit classes with proved low-noise upper bounds. For fixed depth d and size S=m^k AC0 circuits, NS_delta above A_d delta (k log m)^{d-1} separates the same m-bit function from AC0_d[m^k]. The bridge is not a P-vs-NP bridge.

## Definitions

- source object: the full truth table of an m-bit Boolean function f_m, with SAT_m as the intended unpadded source slice and N=2^m.
- target object: unbounded fan-in De Morgan AC0 circuits of fixed depth d and size at most m^k; unrestricted SIZE(m^k) is deliberately not the target.
- controlled interface: the statistic NS_delta(f)=Pr[f(x) != f(y)] under independent delta-bit flips, plus the total-influence upper bound for the named target class.
- target-preserving condition: the high-noise witness must occur on the same unpadded source slice being separated; grafting an easy parity or padding branch onto an NP-complete carrier is not target-preserving.

## Assumptions

- d and k are fixed constants before m grows.
- Noise flips each input coordinate independently with probability delta.
- The AC0 target is the standard constant-depth AND/OR/NOT model with arbitrary fan-in and size counted by gates.
- The source truth table is total; promise or partial-function escapes require a separate totalization audit.

## Equations

- noise-sensitivity-definition: `\operatorname{NS}_{\delta}(f)=\Pr_{x,e}[f(x)\ne f(x\oplus e)],\quad e_i\sim \operatorname{Bernoulli}(\delta)`. Valid when: Valid when f is a total Boolean function on m input coordinates and the noise distribution is product Bernoulli.
- influence-upper-bound: `\operatorname{NS}_{\delta}(f)\le \delta\, I(f),\quad I(f)=\sum_{i=1}^{m}\Pr_x[f(x)\ne f(x\oplus e_i)]`. Valid when: Valid when the noisy input is coupled by sequentially flipping the selected coordinates from a uniform starting point.
- ac0-influence-bound: `C\in AC^0_d[S]\Rightarrow I(C)\le A_d(\log S)^{d-1}`. Valid when: Valid when C is an unbounded fan-in De Morgan circuit of fixed depth d and size S at least two.
- restricted-transfer-threshold: `\operatorname{NS}_{\delta}(f_m)>A_d\delta(k\log m)^{d-1}\Rightarrow f_m\notin AC^0_d[m^k]`. Valid when: Valid when the same m-bit source function is compared against the fixed-depth size m^k target without padding leakage.

## Attempted Derivation

- Start with a hoped-for lower bound NS_delta(SAT_m)>A_d delta(k log m)^{d-1}.
- Using NS_delta(f)<=delta I(f) and the AC0 influence bound, derive SAT_m notin AC0_d[m^k]. This restricted transfer is valid.
- Try to replace AC0_d[m^k] by unrestricted SIZE(m^k) using the same high-noise statistic.
- The replacement fails: PAR_m has O(m)-size circuits and NS_delta close to 1/2 when delta*m is large.
- Try to repair by defining P_{tau,delta}={truth tables with high NS_delta} and requiring usefulness against all SIZE(m^k).
- This repair triggers the natural-proof audit because P_{tau,delta} is constructive and large at random-function thresholds.

Blocking gap: There is no valid low-noise upper bound for unrestricted polynomial-size circuits; XOR fanout gives an explicit leakage channel.

## Falsifiers

- PAR_m has linear-size unrestricted circuits and NS_delta(PAR_m)=(1-(1-2delta)^m)/2, falsifying high-noise-to-SIZE lower-bound claims.
- A parity-branched NP-complete language can inherit high noise sensitivity from an easy slice while preserving many-one NP-hardness.
- If P_{tau,delta} is large and useful against SIZE(poly), it is a valid natural property and collides with PRF-based natural-proof barriers.
- Padding can reduce the SAT core's contribution to the global noise statistic while leaving the measured input length and target size threshold inflated.

## Learning

Cycle 52 converts noise-sensitivity enthusiasm into a precise target gate: NS_delta above A_d delta(k log m)^{d-1} gives a valid AC0_d[m^k] lower bound via total influence, but high noise is useless for unrestricted SIZE because parity is linear-size and maximally noisy. A parity-branched NP-complete carrier is the concrete falsifier for non-target-preserving noise routes.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for noise-sensitivity lower-bound routes.`
- Rationale: The branch needs a concrete target-preserving test because high analytic complexity of an NP-complete carrier can be fabricated by easy noisy padding, so abstract noise-hardness language is not enough.
- Situation seed: Define L_beta on inputs (b,phi,u) with |phi|=m and |u|=r=m^beta: L_beta(0,phi,u)=SAT_m(phi) and L_beta(1,phi,u)=PAR_r(u). The map phi -> (0,phi,0^r) preserves many-one NP-hardness, while the b=1 slice is easy and high-noise.
- Varied variable: beta, the exponent controlling the parity-padding length r=m^beta.
- Held-fixed controls: The SAT core and its many-one reduction into the b=0 slice remain unchanged., The unrestricted target SIZE(n^k) and the fixed-depth restricted target AC0_d[n^k] are named separately., The noise-rate rule is delta_beta=c/r for a fixed constant c, so the parity slice has constant noise contribution., The added parity branch is computable by O(r) unrestricted Boolean gates.
- Expected observation: At delta_beta=c/r, the parity slice contributes about (1/4)(1-exp(-2c)) to global NS_delta, independent of SAT hardness. Thus high NS of an NP-complete carrier is not a valid P-vs-NP certificate unless the statistic is localized to the SAT core and paired with a target-class upper bound.
- Transfer certificate needed: A valid transfer must prove that the measured noise lower bound survives after deleting easy branches and padding, and must provide a low-noise theorem for the exact target class. For unrestricted SIZE(poly), parity shows that certificate cannot exist in this form.

## Next Experiment

Audit whether any non-natural SAT-specific proof can lower-bound NS_delta(SAT_m) at delta=(log m)^{-d} above the AC0 threshold without using a full-truth-table large property useful against SIZE(poly).

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Rooted edit leakage lemma for low-image MCSP carriers: if every emitted table is reachable from a subthreshold easy anchor by paths of cumulative edit exponent below epsilon, then the alleged MCSP no-side source is invalid. For a rank-walk image of entropy D with adjacent update exponent beta, beta+D<epsilon is a concrete falsifier.

## Definitions

- source object: E-uniform canonical low-image MCSP carrier I_m subset {0,1}^{2^m}, |I_m|<=2^{D m+O(1)}, with an alleged row of unrestricted circuit complexity greater than 2^{epsilon m}.
- target object: E language obtained by row-index multiplexing the emitted truth tables and then applying kappa-density padding to all target input lengths.
- controlled interface: map a hard row T_{m,j} to L(j,x,pad)=T_{m,j}(x), with row index length Dm+O(1), E-uniform unranking, and no nonuniform length advice.
- target-preserving condition: row hardness is against unrestricted nonuniform circuits, the source unranking is E-uniform, padding loses only factor kappa, and no easy-rooted low-volume edit certificate undercuts the MCSP threshold.
- easy-rooted edit graph: a graph whose root A has circuits C(A)<=2^{a m+o(m)} and whose edge e changes p_e truth-table positions.
- path-volume exponent: every relevant root-to-row path has at most 2^{eta m+O(1)} edges and each edge changes at most 2^{beta m+O(1)} positions.

## Assumptions

- m is the truth-table input length, N=2^m is the table length, and all circuit bounds are unrestricted Boolean circuit size.
- The edit path may be used nonuniformly for a fixed emitted row; hardwiring changed coordinates is allowed in the upper-bound circuit.
- The carrier claims MCSP no-side threshold s_m=2^{epsilon m} for at least one emitted row, or for all rows in the stronger universal version.
- The extraction theorem uses the existence of one hard row; it does not assert P != NP.

## Equations

- image_entropy: `\lvert I_m\rvert \le 2^{D m+O(1)}`. Valid when: Valid when the source lower-bound model is unrestricted nonuniform circuits and distinct emitted truth tables are canonically quotient-counted.
- path_volume: `P(v)=\sum_{e\in path(A,v)} p_e \le 2^{(\eta+\beta)m+O(1)}`. Valid when: Applies when every path has at most 2^{eta m+O(1)} edges and each edge flips at most 2^{beta m+O(1)} table positions.
- edit_circuit_upper_bound: `C(T_v) \le C(A)+O(mP(v)) \le 2^{\max\{a,\eta+\beta\}m+o(m)}`. Valid when: Valid when the root table A has circuits of size 2^{a m+o(m)} and edited coordinates may be hardwired in a nonuniform circuit.
- rooted_falsifier_threshold: `\max\{a,\eta+\beta\}<\epsilon \Rightarrow T_v \notin \mathrm{MCSPNo}(2^{\epsilon m})`. Valid when: Requires the asserted MCSP no-side threshold to be 2^{epsilon m} against unrestricted circuits for the same truth-table length.
- rank_walk_corollary: `D+\beta<\epsilon \Rightarrow \text{rank-walk carrier from an easy endpoint is invalid}`. Valid when: Applies when canonical rank traversal visits at most 2^{D m+O(1)} rows and each adjacent update has exponent beta.
- target_transfer: `\delta < \epsilon/(\kappa(1+D))`. Valid when: Applies after the reduction preserves E-uniform unranking, kappa-dense padding, and row-index length Dm+O(1).

## Attempted Derivation

- Fix length m, image entropy D, MCSP threshold s_m=2^{epsilon m}, and an easy anchor A with circuit exponent a.
- Assume a candidate selector exposes a root-to-row edit graph with path length exponent eta and edge edit exponent beta.
- For a fixed emitted row T_v, hardwire the root circuit and all edited coordinates along one path; compute T_v(x)=A(x) xor the parity of equality tests hitting x.
- This gives C(T_v)<=C(A)+O(mP(v))<=2^{max(a,eta+beta)m+o(m)}.
- If max(a,eta+beta)<epsilon, the row cannot be a no-side MCSP witness; for canonical rank traversal eta<=D, the falsifier condition is D+beta<epsilon.
- Applying the existing carrier extraction after this audit still gives only the conditional route-level consequence delta<epsilon/(kappa(1+D)).

Blocking gap: The positive source theorem is missing: we need an E-uniform, no-advice, low-D carrier with a hard row and a certificate excluding every easy-rooted low-volume edit explanation, without simply assuming the desired circuit lower bound.

## Falsifiers

- Rooted edit falsifier: an easy anchor plus a covering arborescence with max(a,eta+beta)<epsilon gives small circuits for every covered row.
- Rank-walk falsifier: low-image entropy D and adjacent update exponent beta with D+beta<epsilon invalidate an easy-endpoint iterative carrier.
- Interval-decoder falsifier: indexed block restart or ranked random access below exponent epsilon gives a direct circuit upper bound for emitted tables.
- Sparse-correction falsifier: accepted rows within O(2^{epsilon m}/m) edits of any subthreshold circuit are not valid MCSP no-side witnesses.
- Aggregate-shortcut falsifier: unrestricted aggregate row-forcing below q_force=(D+epsilon)/(1+D) cannot certify an MCSP-hard row.
- Natural-property falsifier: dense constructive postfilters around MCSP hardness re-enter the large constructive property regime; the sparse low-D image avoids largeness only if no dense repair is used.
- Nonuniform-leakage falsifier: advice selecting hard lengths or hard rows does not yield the target E language and breaks the controlled interface.

## Learning

Cycle 52 isolates the exact rooted version of rank-jump leakage. Low-D plus smooth updates is harmful only from a known easy anchor; then beta+eta<epsilon, and in rank order beta+D<epsilon, is a valid source-side falsifier. Unrooted smoothness is not enough. The established MCSP-carrier extraction remains conditional route progress, not a proof of P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design-now-as-falsifier-probe`
- Rationale: The route is bottlenecked by explicit selector leakage, not by the carrier-to-E extraction. A concrete rooted-edit experiment tests whether candidate derandomizations of random robust low-D carriers secretly manufacture subthreshold circuits.
- Situation seed: Start with a random robust low-D MCSP carrier image of M=2^{D m} rows, then try to make it E-uniform by an iterative repair selector beginning at the all-zero truth table and changing at most 2^{beta m} positions per generated row.
- Varied variable: The edge edit exponent beta in the rooted repair transcript.
- Held-fixed controls: MCSP no-side threshold s_m=2^{epsilon m} against unrestricted nonuniform circuits., Distinct-image entropy D and canonical row-index multiplexing with index length Dm+O(1)., No advice and E-uniform unranking of row bits., Padding density kappa for the target E lower-bound transfer.
- Expected observation: For beta+D<epsilon, every row produced before 2^{D m} steps has a nonuniform circuit below 2^{epsilon m}, so the selector is invalid. For beta+D>=epsilon, the rooted-edit leakage certificate disappears, but hardness is still unproved.
- Transfer certificate needed: A formal transcript-to-circuit lemma naming the easy root and edit-volume bound, or conversely a non-natural certificate that the selected hard row has no subthreshold easy-rooted edit explanation before applying delta<epsilon/(kappa(1+D)).

## Next Experiment

Analyze a Merkleized global-constraint selector for random robust low-D carriers: compute its rooted edit exponent beta, check whether beta+D crosses epsilon, and test whether its verification transcript leaks interval access or only supplies a non-natural large-jump certificate.
