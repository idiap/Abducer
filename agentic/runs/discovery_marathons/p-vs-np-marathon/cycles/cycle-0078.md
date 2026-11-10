# cycle-0078

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For the beta-zero XOR carrier at source threshold s_N=N^{1+epsilon-o(1)}, any accepted certificate that is functional over arbitrary row functions, sound for C(h)>s_N in general SIZE, and whose acceptance depends on at most T_N source rows must have T_N=Omega(s_N/N)=N^{epsilon-o(1)}. Thus a proof-mediated EF+SAT_U route that does not certify row-residual robustness has a concrete sparse-row falsifier unless it is genuinely SAT-semantic and nonrelativizing.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) on N-bit rows, with M_N<=N^{q+o(1)}, L_N=(log N)^d, and a batched generator of size N^{rho+o(1)}.
- target object: SAT on L_N-bit instances and the nonuniform target consequence SAT notin P/poly obtained only after excluding every fixed polynomial SAT circuit exponent.
- controlled interface: substitute a length-L_N SAT circuit into all generated occurrences using one batched generator and no advice beyond the hypothesized SAT circuit.
- target-preserving condition: d>1, beta=0, max{rho,q}<1+epsilon, same nonuniform SIZE model on source and target, and the source claim is C(H_N^SAT)>N^{1+epsilon-o(1)}.
- row-value certificate: a relation A_N(pi,h) whose acceptance depends on h only through a touched row set R_pi subset {0,1}^N.
- functional soundness: for every Boolean row function h, A_N(pi,h)=1 implies C(h)>s_N in the same circuit model.

## Assumptions

- SIZE means fan-in-two Boolean circuits with nonuniformity allowed only through the circuit itself, not through a separate row-advice string.
- The generator is batched: all M_N formulas G_N(x,j) are produced with total circuit cost N^{rho+o(1)}, not M_N independent copies of that cost.
- The row-touch model abstracts only functional or relativizing proof certificates; SAT-semantic EF proofs are not covered unless an extraction theorem makes them functional over rows.
- The equality patch for E rows uses O(EN) gates and is valid for unrestricted nonuniform circuits.

## Equations

- beta_zero_xor_carrier: `H_N^SAT(x)=bigoplus_{j<=M_N} SAT(G_N(x,j))`. Valid when: Valid when G_N is the named batched generator and every query length is L_N=(log N)^d.
- target_substitution_upper_bound: `C(H_N^SAT) <= N^{rho+o(1)} + N^{q+o(1)} L_N^c = N^{max{rho,q}+o(1)}`. Valid when: Valid when SAT on L_N-bit inputs has circuits of size L_N^c and beta equals zero.
- row_residual_patching: `C(H_N^SAT) <= S_D + O(|R_N| N)`. Valid when: Applies when D_N agrees with H_N^SAT outside R_N and row equality tests are available nonuniformly.
- functional_touch_lower_bound: `T_N >= Omega(s_N/N) = N^{epsilon-o(1)} for s_N=N^{1+epsilon-o(1)}`. Valid when: Requires functional soundness over arbitrary row functions and acceptance depending on only T_N row values.

## Attempted Derivation

- Assume a row-value certificate A_N(pi,h) is functional and s_N-sound: A_N(pi,h)=1 implies C(h)>s_N for all Boolean h on N-bit rows.
- Let R_pi be the set of rows whose h-values can affect acceptance, with |R_pi|=T_N, and suppose A_N(pi,H_N^SAT)=1.
- Define h_R to agree with H_N^SAT on R_pi and to be zero outside R_pi. Acceptance is unchanged because A_N only sees rows in R_pi.
- Build h_R by OR-ing equality tests for the rows in R_pi and hardwiring the corresponding bits, giving C(h_R)<=O(T_N N).
- If T_N=o(s_N/N), then C(h_R)<s_N, contradicting functional soundness. Hence functional certificates proving the source threshold must touch N^{epsilon-o(1)} rows.
- Combine with the beta-zero bridge: a valid source lower bound still transfers to SAT notin P/poly when max{rho,q}<1+epsilon, but the proof-mediated route must now pass the row-touch or SAT-semantic extraction fork.

Blocking gap: The derivation is complete only for functional row-value certificates. EF+SAT_U proofs are SAT-semantic over formula labels, so a nonrelativizing extraction theorem or a private-row no-go formalization is still needed.

## Falsifiers

- A subthreshold residual circuit D_N with fewer than N^{epsilon-o(1)} wrong rows is a falsifier for the claimed source lower bound.
- An accepted functional certificate touching o(N^{epsilon}) rows is a falsifier for proof-mediated soundness at threshold N^{1+epsilon-o(1)}.
- A relativizing occurrence-local EF+SAT_U argument that survives the private-row oracle is a falsifier for the claimed SAT-semantic escape.
- A positive target-query exponent beta reintroduces the transfer cap q+beta c and falsifies all-exponent target exclusion.
- Any hidden nonuniform list of exceptional rows larger than the accounted proof size is advice leakage and invalidates the route certificate.

## Learning

Cycle 78 converts the row-residual audit into a theorem-shaped no-go: functional row-local certificates for the beta-zero XOR carrier require N^{epsilon-o(1)} touched rows at source threshold N^{1+epsilon-o(1)}. This sharpens the EF+SAT_U obstruction from ordinary soundness to a concrete extraction fork: either the proof is direct or nonlarge/nonconstructive, or it must use real SAT semantics in a nonrelativizing way that defeats the private-row falsifier.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch already has the beta-zero transfer; the live uncertainty is whether EF+SAT_U certificates are genuinely SAT-semantic or merely functional row-local arguments in disguise.
- Situation seed: Private-row beta-zero XOR carrier: for each source row x and position j, generate a unique padded SAT_U occurrence p_{x,j} of length L_N=(log N)^d, assign oracle labels so xor_j p_{x,j}=h(x), and compare any accepted certificate with the real H_N^SAT certificate.
- Varied variable: Row-touch exponent tau in T_N=N^tau for the verifier or extracted proof object.
- Held-fixed controls: M_N<=N^{q+o(1)} with q<1+epsilon., Batched generator overhead N^{rho+o(1)} with rho<1+epsilon., Target query length L_N=(log N)^d with d>1, so beta=0., Source threshold s_N=N^{1+epsilon-o(1)} in unrestricted nonuniform SIZE., No separate advice for exceptional rows or SAT labels.
- Expected observation: For tau<epsilon, every functional or private-row-relativizing certificate can be fooled by a sparse-support row function of circuit size O(N^{1+tau}); tau>=epsilon is the first valid touch threshold.
- Transfer certificate needed: A formal extraction from EF+SAT_U occurrence proofs to row-value functional certificates, or a proof that the accepted certificates use real SAT constraints in a nonrelativizing way absent from the private-row oracle.

## Next Experiment

Instantiate EF+SAT_U row occurrence access formally: define the touched-row set of a proof verifier, test whether standard EF reflection over SAT_U extracts to row-value functionality, and if not construct the private-row oracle countermodel as a finite theorem.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Let H_N^SAT be the beta-zero XOR source and let V_N be a proof-mediated row-cluster verifier. If a cluster C has Q_C=O(log N) target-label projection, projection-decision width W_C=O(log N), uniform enumeration in poly(N), actual acceptance for H_N^SAT, and DirectClusterSound(C,k) against SIZE_m(m^k), then the existential shadow P_C is a valid N^{-O(1)}-large poly(N)-constructive natural property useful against SIZE_m(m^k). Thus such a certificate route either naturalizes or must explicitly escape by non-largeness, nonconstructivity, or failure of DCS.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N<=N^{q+o(1)}, query length L_N=(log N)^d, and generator overhead N^{rho+o(1)}; its truth table has length N=2^m.
- target object: C_{m,k}=SIZE_m(m^k), the nonuniform Boolean circuits of size m^k on m=log_2 N inputs, compared against truth tables T in {0,1}^N.
- controlled interface: a uniform proof-mediated cluster verifier V_N(C,T,pi) whose cluster C reads Q_C target labels and a proof-view CSP of projection-decision width W_C.
- target-preserving condition: DirectClusterSound(C,k) means no truth table T of any f in C_{m,k} has any proof-view assignment pi accepted by the cluster C.

## Assumptions

- Uniformity regime: C, its target projection, and the width-W_C decision procedure are listable in time N^{O(1)} without advice depending on the target truth table.
- Naturalness regime: the induced property P_C(T)=1 iff there exists a proof-view assignment pi accepted by V_N(C,T,pi) is decided by enumerating the width-W_C projected proof-view states.
- Completeness regime: the intended beta-zero XOR certificate supplies at least one accepting proof-view assignment for T=TT(H_N^SAT).
- Soundness regime: usefulness is not ordinary proof-system soundness; it is exactly the same-theory DirectClusterSound(C,k) condition for the target circuit class.
- Non-claim boundary: this proves a route-level barrier transfer, not P != NP and not an unconditional lower bound for SAT.

## Equations

- projection_bound: `Q_C <= A log N`. Valid when: Valid when the row cluster has logarithmic target projection after all proof-view and row-selection queries are unfolded uniformly.
- shadow_density: `mu(P_C) >= 2^{-Q_C} >= N^{-A}`. Valid when: Valid when one accepting transcript for H_N^SAT fixes only Q_C target labels and existentially hides all proof labels.
- constructivity_bound: `Time(P_C) <= N^{O(1)} 2^{O(W_C)} = N^{O(1)}`. Valid when: Valid when the projected proof-view CSP has width W_C=O(log N) and its bags are uniformly enumerable.
- usefulness_from_DCS: `P_C cap TT(C_{m,k}) = emptyset`. Valid when: Requires DirectClusterSound(C,k) for exactly the target circuit class SIZE_m(m^k), not merely ordinary verifier soundness.
- beta0_transfer_upper_bound: `C(H_N^SAT) <= N^{rho+o(1)} + N^{q+o(1)} L_N^c = N^{max(rho,q)+o(1)}`. Valid when: Applies when SAT on L_N-bit instances has circuits of size L_N^c and G_N is implemented with overhead N^{rho+o(1)}.

## Attempted Derivation

- Define P_C(T)=1 iff some proof-view assignment pi makes the logarithmic cluster C accept T.
- Completeness for H_N^SAT gives one accepting transcript, fixing at most Q_C target labels; all truth tables agreeing on those labels also lie in P_C, giving density at least 2^{-Q_C}.
- Width W_C=O(log N) lets the existential proof-view shadow be decided by dynamic programming over the projected view in N^{O(1)} time.
- If DirectClusterSound(C,k) holds, no SIZE_m(m^k) truth table is accepted; P_C is useful against the exact target class.
- Instantiate the competing support claim with an odd-charge Tseitin F2 proof-view. Every local boundary view queried by a logarithmic cluster is satisfiable, yet the global system is inconsistent.
- Therefore ordinary local consistency or ordinary proof soundness cannot replace DCS; otherwise P_C may equal all truth tables and usefulness collapses.

Blocking gap: No named proof system in the current packet has yet supplied DirectClusterSound(C,k) for beta-zero XOR certificates while preserving logarithmic target projection, logarithmic decision width, and advice-free uniformity.

## Falsifiers

- Odd-charge Tseitin over F2 is a falsifier for replacing DirectClusterSound by ordinary local consistency at logarithmic projection width.
- Sparse-row residual patching is a falsifier for certificate routes that leak a subthreshold set of hard rows through advice or nonfunctional proof choices.
- A valid PRF family inside SIZE_m(m^k) is a natural-proofs conflict target for any large constructive useful shadow property obtained from DCS.
- A named proof system whose cluster acceptance ignores target labels yields density one and no usefulness, invalidating promotion even if global proofs are sound.

## Learning

Cycle 78 closes a sharper support-branch no-go: bounded local F2/Tseitin consistency cannot provide DirectClusterSound for logarithmic proof-mediated beta-zero XOR clusters. The valid fork is now explicit: DCS naturalizes the carrier, while ordinary local consistency is refuted by a finite falsifier and sparse residual leakage remains a separate quantitative collapse test.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe.`
- Rationale: The branch needs a concrete target-preserving test because the abstract DCS gap has stabilized; the next learning comes from showing which proof-view carriers fail before attempting promotion.
- Situation seed: Attach to each beta-zero XOR certificate row a dummy odd-charge Tseitin F2 system on a graph G_N of size N^a and girth gamma log N; the cluster verifier reads the original O(log N) SAT-target labels and checks only local proof-view consistency in G_N.
- Varied variable: projection-decision width W, increased from c log N to above the minimum closed parity witness size in the Tseitin component.
- Held-fixed controls: Keep H_N^SAT, M_N<=N^{q+o(1)}, L_N=(log N)^d, and generator overhead N^{rho+o(1)} unchanged., Keep the target class fixed as SIZE_m(m^k) on m=log N inputs., Charge all row-selection and proof-view enumeration costs to the certificate, with no nonuniform advice., Keep target projection Q_C=O(log N) so any successful certificate would still naturalize.
- Expected observation: For W below the closed parity witness threshold, every queried Tseitin view is satisfiable and the projected property accepts essentially every truth table; when W crosses the global parity witness, usefulness may return but constructivity or logarithmic-width naturalization must be reaudited.
- Transfer certificate needed: A formal DirectClusterSound(C,k) theorem for the named proof system, or a proof that detecting the odd Tseitin charge necessarily forces superlogarithmic projection width or nonconstructive search.

## Next Experiment

Instantiate one nonlocal named Psys, preferably polynomial calculus or IPS over F2 with an explicit global parity certificate, and test whether its cluster acceptance proves DirectClusterSound(C,k) without increasing Q_C or W_C beyond O(log N).

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Low adaptive-cover DCS-LC/MCSP label certificates for the beta-zero XOR family are route-invalid as lower-bound carriers: if the accepted certificate is SAT-semantically bound outside a sparse residual, then it yields C(H_N^SAT)<=N^{max{rho,q+alpha_ad,r+1}+o(1)}. Thus any claimed certificate of C(H_N^SAT)>N^theta with theta above this maximum has a finite falsifier.

## Definitions

- source object: DCS-LC_N(pi_N), a fixed accepted DirectClusterSound-style MCSP/MKtP label certificate for the beta-zero XOR SAT-query family, with query count M_N<=N^{q+o(1)}, generator overhead N^{rho+o(1)}, and residual set R_N.
- target object: H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)) on N-bit inputs, measured by unrestricted nonuniform Boolean circuit size C(H_N^SAT).
- controlled interface: the certificate opens query labels through an adaptive block cover with exponent alpha_ad=max{tau,max_l(a_l+mu_l),max_l omega_l}, and the opened label for (x,j) is hardwired into a circuit when pi_N is fixed.
- target-preserving condition: accepted labels equal SAT(G_N(x,j)) for all x not in R_N and all j, residual corrections are charged on the same N-bit input model, and no change of target language or circuit model is allowed.

## Assumptions

- Model: unrestricted nonuniform Boolean circuits; hardwiring the accepted certificate, cover summaries, and residual list is allowed for the negative upper-bound contradiction.
- Regime: M_N<=N^{q+o(1)}, the generator G_N has circuit size N^{rho+o(1)}, and formula lengths L_N=(log N)^d do not add a polynomial-in-N cost.
- Uniformity/advice cutoff: advice-free generation is still required for positive extraction to E, but the falsifier direction only needs existence of one fixed low-cover accepted certificate at each N.
- Semantic condition: DCS-LC acceptance must certify actual SAT labels outside R_N; ordinary local consistency or cluster soundness alone is not target-preserving.
- Residual condition: |R_N|<=N^{r+o(1)} and the exceptional inputs are usable as hardwired equality-test corrections in the nonuniform circuit.
- Non-claim boundary: this is a valid route-level obstruction, not a proof of P != NP or of any SAT lower bound.

## Equations

- beta0_xor_family: `H_N^{SAT}(x)=\bigoplus_{j<M_N} SAT(G_N(x,j)),\qquad M_N\le N^{q+o(1)}`. Valid when: Valid when H_N is the same N-bit beta-zero XOR family named in the source object.
- adaptive_cover_exponent: `\alpha_{ad}=\max\{\tau,\max_l(a_l+\mu_l),\max_l\omega_l\}`. Valid when: Valid when adaptive openings are charged in unrestricted circuits after hardwiring the fixed certificate.
- covered_label_xor_upper_bound: `C(D_N)\le N^{\max\{\rho,q+\alpha_{ad}\}+o(1)}`. Valid when: Applies when SAT-semantic binding holds outside the residual set and all query labels use the same cover.
- sparse_residual_correction: `C(H_N^{SAT})\le C(D_N)+O(|R_N|N)\le N^{\max\{\rho,q+\alpha_{ad},r+1\}+o(1)}`. Valid when: Requires residual positions on N-bit inputs to be hardwired as equality tests in unrestricted circuits.
- certificate_collapse_gate: `\theta>\max\{\rho,q+\alpha_{ad},r+1\}\quad\Rightarrow\quad \text{low-cover certificate cannot prove }C(H_N^{SAT})>N^\theta`. Valid when: Valid when the intended lower bound and upper-bound exponents are measured in the same N parameter.

## Attempted Derivation

- Fix N and a DCS-LC accepted certificate pi_N with adaptive cover parameters tau,a_l,mu_l,omega_l and residual R_N.
- Hardwire pi_N and the cover summaries into an unrestricted circuit A_N(x,j) computing the opened label for query (x,j), with size N^{alpha_ad+o(1)} per queried label family.
- Use the generator circuit for G_N only as the semantic index ledger; the cover computes labels, and SAT-semantic binding asserts A_N(x,j)=SAT(G_N(x,j)) for x outside R_N.
- Build D_N(x)=xor_{j<M_N} A_N(x,j). The fanout over M_N<=N^{q+o(1)} queries gives C(D_N)<=N^{max{rho,q+alpha_ad}+o(1)}.
- For each x in R_N, hardwire an equality test on the N input bits and flip D_N(x) when needed. This costs O(|R_N|N)=N^{r+1+o(1)}.
- Compare the resulting upper bound with any claimed beta-zero XOR lower bound exponent theta. If theta exceeds max{rho,q+alpha_ad,r+1}, the certificate route contradicts itself.

Blocking gap: The derivation still depends on a concrete DCS-LC syntax audit: accepted certificates must be shown either to provide SAT-semantic labels outside R_N or to fail target preservation. The exact alpha_ad parameters must be computed from the actual opener protocol, not assigned abstractly.

## Falsifiers

- falsifier: an accepted all-zero or parity-only label assignment passes local cluster checks on a mixed SAT/UNSAT query set, showing that ordinary consistency is not SAT semantics.
- falsifier: alpha_ad<theta-q together with r+1<theta yields an explicit unrestricted circuit below the claimed lower-bound exponent.
- falsifier: a residual set of size N^{r+o(1)} with r+1 below theta compresses the alleged hard part by equality-test corrections.
- falsifier: a certificate whose row opener has indexed block summaries with exponent omega<theta-q naturalizes into a low-cover circuit for the XOR labels.
- falsifier: positive extraction using a nonuniform hard-row selector is invalid even though the same selector can be hardwired for the negative upper-bound theorem.
- falsifier: changing the target from H_N^SAT to the verifier's surrogate label XOR destroys the target-preserving condition.

## Learning

Cycle 78 converts the beta-zero MCSP/MKtP audit into a named DCS-LC falsifier theorem: SAT-semantic low-cover labels plus sparse residuals imply C(H_N^SAT)<=N^{max{rho,q+alpha_ad,r+1}+o(1)}. The new decisive gate is semantic binding, not selector advice or generic barrier folklore.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch needs a concrete target-preserving audit of one certificate carrier, because the remaining uncertainty is not abstract hardness magnification but whether DCS-LC labels are SAT-semantic and low-cover enough to collapse the claimed beta-zero lower bound.
- Situation seed: A padded beta-zero SAT-query family H_N^SAT with M_N=N^q, L_N=(log N)^d, generator overhead N^rho, and a DirectClusterSound-style certificate that opens SAT labels through adaptive block summaries while allowing a residual set R_N.
- Varied variable: adaptive opener exponent omega, varied through the block-opening width while tau, a_l+mu_l, q, rho, and r are held fixed; equivalently alpha_ad changes only through omega.
- Held-fixed controls: The target function remains H_N^SAT on N-bit inputs, not a verifier-defined surrogate., The circuit model remains unrestricted nonuniform Boolean circuits for the falsifier., Query count exponent q and generator overhead rho are fixed., Residual size exponent r is fixed and charged as r+1., SAT-semantic binding outside R_N is required before any upper-bound conclusion is declared valid.
- Expected observation: When q+alpha_ad and r+1 are both below theta, the thought experiment must exhibit a circuit of size N^{max{rho,q+alpha_ad,r+1}+o(1)}, refuting the certificate as a lower-bound carrier. When alpha_ad crosses theta-q, the falsifier no longer fires but no positive lower bound is obtained.
- Transfer certificate needed: A formal DCS-LC semantic-binding lemma proving that every accepted opened label equals SAT(G_N(x,j)) outside the charged residual, plus a syntax-level computation of tau,a_l,mu_l,omega_l for the actual opener protocol.

## Next Experiment

Instantiate DirectClusterSound(C,k) with k=O(log N) on the padded beta-zero SAT-query family; compute tau,a_l,mu_l,omega_l from its proof-opening syntax, run the all-zero/odd-charge Tseitin semantic falsifier, and record whether accepted labels are SAT-semantic outside a residual R_N of known exponent r.
