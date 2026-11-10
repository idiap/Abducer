# cycle-0055

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For a polylog-query XOR generated-SAT carrier, the target bridge remains valid with threshold max{rho,q}<1+epsilon. The source lower bound is credible only after ruling out every SAT-preserving quotient incidence sketch; any subthreshold quotient sketch plus sparse exceptions is a concrete falsifier for C(H_N)>N^{1+epsilon-o(1)}.

## Definitions

- source object: H_N(x)=xor_{j<=m} SAT(phi_{N,j}(x)), a Boolean function on N-bit seeds, measured in unrestricted nonuniform SIZE.
- target object: SAT on L-bit formula encodings, with target consequence SAT notin P/poly and hence NP not subset P/poly if the bridge source lower bound is valid.
- controlled interface: a SAT-free generator G_N of size N^rho emits m=ceil(N^q) formulas of length L=(log N)^d, and the carrier consumes their SAT labels only through F_2 parity.
- target-preserving condition: L=(log N)^d, d>1, max{rho,q}<1+epsilon, and the claimed source lower bound C(H_N)>N^{1+epsilon-o(1)} holds for infinitely many N without SAT-label advice in G_N.
- quotient incidence: for a SAT-preserving equivalence relation sim_N on L-bit formulas, a_N^sim(x)_C is the parity of generated formulas in class C.
- quotient sketch: QSk_{sim,N}(E) is the minimum total circuit cost of a piecewise affine representation of a_N^sim(x), correct outside E exceptional seeds, with SAT parities of affine basis vectors hardwired nonuniformly.

## Assumptions

- epsilon>0 is fixed; q,rho,d are fixed constants with max{rho,q}<1+epsilon.
- G_N is target-clean: its circuit description does not contain SAT truth-table advice, although upper-bound falsifiers may hardwire finitely many parity constants.
- sim_N is exact SAT-preserving: phi sim_N psi implies SAT(phi)=SAT(psi).
- Exceptional seeds are patched by equality circuits of O(N) size per seed.

## Equations

- xor_incidence_identity: `H_N(x)=\bigoplus_{j=1}^{m}\mathrm{SAT}(\phi_{N,j}(x))=\langle \tau_L,a_N(x)\rangle_{\mathbb F_2}`. Valid when: Valid when G_N outputs syntactic formula encodings and repeated formulas are counted with parity over F_2.
- polylog_substitution_bound: `\mathrm{SAT}\in \mathrm{SIZE}(n^c)\ \Rightarrow\ C(H_N)\le O(C(G_N)+m\,L^c+mL)=N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies after SAT has n^c-size circuits and the generator has N^rho-size circuits with m=N^q polylog-length queries.
- target_magnification_threshold: `\max\{\rho,q\}<1+\epsilon\ \wedge\ C(H_N)>N^{1+\epsilon-o(1)}\ \Rightarrow\ \mathrm{SAT}\notin\mathrm{P/poly}`. Valid when: Valid for infinitely many N against every fixed target exponent c because L=(log N)^d makes L^c=N^{o(1)}.
- sat_preserving_quotient_identity: `H_N(x)=\langle \tau_L^{\sim},a_N^{\sim}(x)\rangle_{\mathbb F_2}`. Valid when: Requires the equivalence relation to preserve SAT labels on every quotient class used by the generated formulas.
- quotient_sketch_upper_bound: `C(H_N)\le O(\mathsf{QSk}_{\sim,N}(E)+E N)`. Valid when: Requires a piecewise affine sketch of the quotient incidence vector correct outside E named seeds and allows nonuniform hardwiring of the resulting SAT parities.

## Attempted Derivation

- Write the XOR carrier as the F_2 inner product of the SAT truth vector tau_L with the generated incidence vector a_N(x).
- Prove the polylog substitution upper bound: SAT circuits of size n^c yield H_N circuits of size N^{max{rho,q}+o(1)}.
- Try to certify C(H_N)>N^{1+epsilon} from high rank or expansion of the incidence map x -> a_N(x).
- Normalize by quotienting formula space under SAT-preserving symmetries and by cancelling even multiplicities.
- Observe that a piecewise affine quotient sketch of cost below N^{1+epsilon} directly computes H_N after hardwiring basis parities and patching sparse exceptions.

Blocking gap: Label-sensitive extraction gap: a small arbitrary circuit for the single function x -> <tau_L,a_N^sim(x)> need not reveal a small quotient-incidence sketch, and high quotient rank alone does not preclude the SAT-labelled linear functional from being simple.

## Falsifiers

- falsifier: an easy SAT-preserving quotient collapses the odd incidence vectors to subthreshold piecewise affine dimension while raw formula range remains high.
- falsifier: fixed-point-free duplicate, variable-renaming, or clause-permutation pairings cancel most XOR slots before any SAT hardness is used.
- falsifier: QSk_{sim,N}(E)+EN<N^{1+epsilon-o(1)} for some E<N^{epsilon-o(1)} gives an explicit nonuniform circuit for H_N.
- falsifier: high quotient rank is aligned with a low-cost SAT-labelled linear functional, so rank-only evidence is not valid source lower-bound evidence.
- falsifier: a proposed quotient relation or sketch uses SAT truth-table advice inside G_N, causing nonuniform leakage and breaking the target-clean interface.

## Learning

Cycle 55 adds the SAT-preserving quotient normal form for XOR carriers. The valid target bridge is still max{rho,q}<1+epsilon, but the source lower bound must beat quotient piecewise-affine incidence sketches, not raw range or rank. Symmetry-pair cancellation is a concrete falsifier that can make a high-entropy generator compute a constant carrier; this is route-level progress only, not a proof of P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The XOR route can be artificially inflated by SAT-equivalent paired queries. A concrete cancellation experiment tests whether the current source audit measures the real odd quotient incidence or only raw slot entropy.
- Situation seed: For each N choose q in ((1+epsilon)/2,1+epsilon) and L=(log N)^d with d>1. Let G_N emit M=N^q formulas; most slots are pairs (psi, rename_pi(psi)) under variable renaming, while R=N^u residual slots are high-entropy target-clean formulas. H_N is the XOR of all generated SAT labels.
- Varied variable: residual exponent u, equivalently the odd quotient incidence mass after SAT-preserving pair cancellation.
- Held-fixed controls: max{rho,q}<1+epsilon so the polylog-query target transfer remains valid., The source model is unrestricted nonuniform SIZE on N-bit seeds., The equivalence relation is exact SAT preservation by syntactic variable renaming and duplicate equality., G_N contains no SAT truth-table advice; only upper-bound falsifier circuits may hardwire parity constants.
- Expected observation: Raw range and slot entropy stay near N^q, but the carrier complexity tracks the residual quotient sketch. When u and the pairing-certificate cost are subthreshold, H_N is easy despite the apparent high-rank generated query family.
- Transfer certificate needed: A formal quotient-incidence sketch bound proving certified pair cancellation, computing the residual quotient incidence below N^{1+epsilon}, and separating target-clean generator information from nonuniform hardwired parity constants.

## Next Experiment

Compute QSk_{sim,N}(E) for quotient relations generated by equality, variable renaming, clause permutation, tautological padding, and duplicate-pair involutions on the current high-q XOR carrier template; record the smallest residual exponent u and pairing-certificate cost.

# Barrier-Aware Lower-Bound Route: SQ-Dimension Target Gate

## Candidate Lemma

SQ dimension gives a valid lower bound only for SQ(q,tau) algorithms. Transfer to SIZE(m^k) requires an explicit circuit-to-SQ simulator on the same distribution; without it, high dimension is not a P-vs-NP route.

## Definitions

- source object: distributional slice L_m with null D_0 and alternatives {D_i}_{i<=M}, density ratios chi_i=dD_i/dD_0-1, and explicit samplers/evaluators.
- target object: SQ(q,tau) distinguishers; audited transfer target is SIZE(m^k) or P algorithms on the same m-bit slice.
- controlled interface: Sim_{k,m} maps every size m^k circuit deciding L_m with advantage eps into q<=Q_k(m) SQ queries of tolerance tau_k and comparable advantage.
- target-preserving condition: the SAT reduction fixes the distributional slice and labels; the statistic cannot be supplied by padding, advice, or an easy tagged branch.

## Assumptions

- All D_i are absolutely continuous with respect to D_0 and queries are bounded in [-1,1].
- Pairwise correlations of likelihood ratios are at most gamma except on the diagonal.
- The SQ lower bound is distributional and black-box; it is relativizing in spirit and not a circuit lower bound by itself.
- Any claimed P-vs-NP use must supply Sim plus a worst-case-to-distributional transfer preserving m,k,eps,tau.

## Equations

- sq_correlation_bound: `\rho_{ij}=\left|\mathbb{E}_{D_0}[\chi_i\chi_j]\right|\le \gamma\quad(i\ne j)`. Valid when: Valid when all planted alternatives share the named null distribution and have bounded likelihood ratios.
- sq_query_threshold: `q\ge \Omega\!\left((\gamma+\tau^2)^{-1}\right)`. Valid when: Valid for standard statistical-dimension lower bounds against bounded SQ distinguishers with tolerance tau.
- conditional_size_transfer: `\mathrm{SIZE}(m^k)\subseteq \mathrm{SQ}(Q_k,\tau_k),\ Q_k<c(\gamma+\tau_k^2)^{-1}\Rightarrow L_m\notin \mathrm{SIZE}(m^k)`. Valid when: Applies after the simulator preserves advantage, distribution, advice bounds, and the m-bit padding threshold.

## Attempted Derivation

- Compute chi_i=dD_i/dD_0-1 for the source family and certify pairwise correlation <=gamma.
- Invoke statistical dimension to rule out SQ(q,tau) distinguishers below q=Theta(1/(gamma+tau^2)).
- Try to convert a size m^k circuit for L_m into an SQ algorithm by estimating its acceptance correlations under D_0 and D_i.
- The conversion has no valid generic form: an arbitrary circuit may use pointwise structure or advice invisible to bounded expectation queries.

Blocking gap: Circuit-to-SQ simulation gap at tolerance tau_k; no uniform, target-preserving map from SIZE(m^k) deciders to few SQ queries is known.

## Falsifiers

- Parity concepts give SQ dimension 2^r under the uniform distribution yet have linear-size XOR circuits; this is the core falsifier.
- Noisy or labeled parity is SQ-hard at inverse-polynomial tolerance but learnable by Gaussian elimination from samples, falsifying SQ-hard implies P-hard.
- A tagged language L(b,x,z)=SAT(x) for b=0 and PARITY(z) for b=1 preserves NP-completeness but lets the SQ statistic live on an easy branch.
- A nonuniform circuit can hardwire the planted index i in a distributional family; SQ search hardness need not imply fixed-language circuit hardness.

## Learning

Cycle 55 isolates the SQ-dimension route exactly: the valid theorem is q=Omega(1/(gamma+tau^2)) for SQ distinguishers. The P-vs-NP transfer is blocked by the absent circuit-to-SQ simulator, with parity and tagged SAT/parity as concrete falsifiers. This is route-level progress only.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The route has a real quantitative lower-bound theorem, but only a concrete padded SAT family reveals whether the SQ threshold survives padding and target transfer.
- Situation seed: Padded SAT-query family P_{m,beta}: a core formula of length n=floor(m^beta) is embedded with inert padding; the many-one map sends phi to pad(phi), and SQ alternatives are planted distributions on the core.
- Varied variable: beta, the core-length exponent n=m^beta.
- Held-fixed controls: The target language remains SAT on the core encoding with deterministic padding., The audited target is SIZE(m^k) on the full m-bit slice., No parity tag, advice tag, or promise-only easy branch is allowed., SQ tolerance tau_k is inverse-polynomial in m and fixed before padding varies.
- Expected observation: As beta decreases, the statistical-dimension threshold may remain large in n but erode relative to Q_k(m); a valid transfer needs Q_k(m)<1/(gamma(m,beta)+tau_k^2).
- Transfer certificate needed: A circuit-to-SQ simulator plus a worst-case-to-distributional reduction preserving beta, advantage, uniformity, and nonuniform advice bounds.

## Next Experiment

Audit low-degree likelihood-ratio methods as SQ subclasses: compute the degree-D to SQ-query conversion and test whether any SAT-preserving simulator beats the same threshold.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Positive-radius anti-ball certificates cannot be mere E-rankable challenge lists. For N=2^m, R=2^{rho m}, and q=epsilon-rho with rho<q, any list L_m of forbidden centers of size below 2^{Omega(m 2^{rho m})} misses an easy sparse truth table T with C(T)=O(Rm)<=2^{q m} and dist(T,L_m)>R. Thus a verifier whose soundness only excludes L_m has an accepted easy row, a route-specific falsifier for the MCSP no-side carrier.

## Definitions

- source object: low-D MCSP carrier row T in {0,1}^{2^m} with a claimed anti-ball certificate excluding radius R=2^{rho m} around subthreshold circuits.
- target object: an E-uniform language obtained by D-multiplexing and kappa-padding, intended to have circuit lower bound exponent delta.
- controlled interface: source row hardness C(T)>2^{q m}, q=epsilon-rho, plus E-canonical distinct-image unranking for at most 2^{D m} rows and no advice.
- target-preserving condition: q>0, rho<q for the sparse-packing falsifier, kappa and D fixed constants, and all length choices uniform rather than nonuniform selectors.
- challenge-list anti-ball certificate: a proof whose only universal lower-bound content is that T is farther than R from every truth table in an explicitly rankable forbidden list L_m.
- sparse easy packing: a family of indicators of 4R-subsets of [N] with pairwise Hamming distance greater than 2R and unrestricted circuit size O(Rm).

## Assumptions

- Unrestricted Boolean circuit size is the MCSP measure.
- The list L_m may be E-rankable or certificate-dependent, but its anti-ball soundness is only list coverage.
- The verifier does not additionally prove a symbolic theorem covering every circuit of size <=2^{q m}.
- rho and q are constants with 0<rho<q<1.

## Equations

- parameters: `N=2^m,\quad R=2^{\rho m},\quad q=\epsilon-\rho`. Valid when: Valid when the source anti-ball radius consumes rho exponent from the claimed MCSP threshold.
- sparse_indicator_upper_bound: `C(1_A)\le O(|A|m)=O(Rm)\le 2^{q m}\quad\text{for } |A|=4R`. Valid when: Valid when rho is strictly below q so polynomial factors are absorbed asymptotically.
- packing_size: `\log_2 P_m\ge \Omega(R\log(N/R))=\Omega((1-\rho)m2^{\rho m})`. Valid when: Valid when constant-weight subsets of size 4R are greedily packed at distance greater than 2R.
- list_soundness_threshold: `|L_m|\ge P_m\ge 2^{\Omega(m2^{\rho m})}`. Valid when: Valid when every easy sparse packed table must be within radius R of some listed center.
- conditional_transfer_after_real_hard_row: `\delta < \frac{q}{\kappa(1+D)}=\frac{\epsilon-\rho}{\kappa(1+D)}`. Valid when: Applies after a genuine hard row, not a challenge-list surrogate, is E-canonically multiplexed and padded.

## Attempted Derivation

- Set N=2^m and R=2^{rho m}. Build a constant-weight code of 4R-subsets of [N] with pairwise symmetric difference greater than 2R by greedy packing in the Johnson space.
- For each support A in the code, the indicator 1_A has an unrestricted DNF/equality-test circuit of size O(Rm). If rho<q, this is below 2^{q m} for large m.
- Because packed tables are pairwise farther than 2R, a single radius-R ball around any listed center can cover at most one packed table.
- The greedy packing has log_2 size Omega(R log(N/R)), hence any challenge list covering all these easy tables needs 2^{Omega(m2^{rho m})} centers.
- An E-rankable list, or any O(m)-certificate naming only 2^{O(m)} challenges, misses a packed easy table. A verifier accepting distance from that list therefore accepts a subthreshold circuit table.

Blocking gap: The derivation does not rule out a genuinely symbolic, non-list proof that quantifies over all circuits of size <=2^{q m}.

## Falsifiers

- challenge-list anti-ball certificate: any E-size list of forbidden centers at positive radius rho<q misses sparse easy packed indicators.
- threshold-collapse falsifier: if q=epsilon-rho<=0 then the extracted exponent delta is nonpositive, and if rho>=q the present sparse-packing audit no longer certifies list failure at the claimed threshold.
- natural-proofs falsifier: replacing the sparse carrier by the dense outside-union anti-ball property makes the property large and constructively dangerous.
- restricted-model falsifier: excluding only uniform algorithms, formulas, AC0, or algebraic circuits does not certify unrestricted MCSP row hardness.
- nonuniform-leakage falsifier: length advice, a nonuniform hard-row selector, or a subthreshold interval decoder invalidates the E target transfer.
- average-soundness falsifier: a proof that most accepted rows are hard is insufficient unless multiplexing canonically isolates an actual hard distinct image.

## Learning

Cycle 55 adds a concrete lower bound against list-based anti-ball sources. Positive-radius anti-ball soundness cannot be certified by enumerating forbidden easy centers: sparse easy indicators form a super-E packing. The valid route narrows to symbolic, no-advice, non-large certificates proving distance from all unrestricted circuits. This is route-level progress and a falsifier for a certificate implementation, not evidence that P != NP is solved.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The branch needs to distinguish a real sparse anti-ball certificate from a disguised finite challenge list; abstract anti-ball language no longer moves the proof obligations.
- Situation seed: Consider a padded GapMCSP source at length N=2^m. The source emits at most 2^{D m} candidate rows and attaches a certificate saying each row is farther than R=2^{rho m} from a rankable list L_m of small-circuit centers. The target is the usual E language obtained by D-multiplexing and kappa-padding.
- Varied variable: rho, the anti-ball radius exponent, while q=epsilon-rho is the claimed row-hardness exponent.
- Held-fixed controls: unrestricted Boolean circuit size as the MCSP measure, E-uniform canonical unranking of the low-D image, no nonuniform length advice or hard-row selector, fixed constants D and kappa in the extraction theorem, target consequence limited to route-level E circuit lower bounds, not a direct P != NP claim
- Expected observation: For 0<rho<q, sparse 4R-support indicators form 2^{Omega(m2^{rho m})} mutually separated easy rows, so every E-size challenge list misses an easy row. As rho increases, the transfer exponent q/(kappa(1+D)) shrinks, and list certificates remain invalid before any useful target lower bound appears.
- Transfer certificate needed: A sound symbolic proof of distance from every unrestricted circuit of size <=2^{q m}, plus E-canonical multiplexing and a proof that the verifier avoids natural-proof largeness, local-decoder leakage, and advice.

## Next Experiment

Audit candidate symbolic proof systems for the anti-ball sentence, starting with algebraic/proof-complexity encodings of 'no size-2^{q m} circuit is within R of T'; compute whether feasible interpolation, low-degree encodings, or proof length force a local decoder or natural large property.
