# cycle-0076

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For beta-zero XOR carriers, an EF+SAT_U proof-mediated source lower bound C(H_N)>N^{1+epsilon} is route-valid only if dense functional certificates naturalize or nonfunctional SAT-semantic certificates certify row-residual robustness; otherwise a sparse residual D_N is a falsifier.

## Definitions

- source object: H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)) on N source bits, with M_N<=N^{q+o(1)} and query length L_N=(log N)^d.
- target object: SAT notin P/poly, reached contrapositive to SAT_L in SIZE(L^c) for every fixed c under the same nonuniform Boolean circuit model.
- controlled interface: beta-zero batched substitution through an advice-free generator G_N of size N^{rho+o(1)}; each target call has polylog length and no row-specific advice.
- target-preserving condition: q,rho<1+epsilon, d>1, same SIZE model, fixed c absorbed as L_N^c=N^{o(1)}, and row patches charged O(N) gates each.
- Psys: EF+SAT_U is extended Frege augmented with semantic SAT axioms only for U_N={G_N(x,j)}; functional soundness means validity for all label vectors on U_N.
- Row residual: D_N agrees with H_N except on R_N source rows; robustness requires every subthreshold D_N to leave |R_N| above the equality-patching cutoff.

## Assumptions

- Circuit size is nonuniform fan-in-2 SIZE; all o(1) losses are uniform for fixed epsilon,c,q,rho,d.
- Certificate search/verification for EF+SAT_U is advice-free and at most 2^{O(L_N)} on the generated range, so constructivity is not hidden in advice.
- Dense functional certificates have label density at least 2^{-O(L_N)} and therefore fall under the earlier valid naturalization audit.
- SAT-semantic certificates are sound only for the true SAT label vector; this is the named nonfunctional escape that must prove residual robustness.

## Equations

- carrier_definition: `H_N^{\mathrm{SAT}}(x)=\bigoplus_{j=1}^{M_N} \mathrm{SAT}(G_N(x,j)),\quad M_N\le N^{q+o(1)},\ L_N=(\log N)^d`. Valid when: Valid when the source object is the beta-zero XOR carrier with a uniformly generated polylogarithmic SAT-query family.
- beta0_transfer: `\mathrm{SAT}_{L_N}\in \mathrm{SIZE}(L_N^c)\Rightarrow C(H_N)\le N^{\rho+o(1)}+N^{q+o(1)}L_N^c=N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies after the reduction preserves advice-freeness, fixed target exponent c, and polylogarithmic query length L_N.
- row_residual_patch: `D_N=H_N\text{ off }R_N,\ C(D_N)=N^{s+o(1)},\ |R_N|=N^{e+o(1)}\Rightarrow C(H_N)\le N^{\max\{s,e+1\}+o(1)}`. Valid when: Requires source rows to be N-bit strings so each exceptional row is patchable by an O(N)-gate equality test.

## Attempted Derivation

- Substitute any SIZE(L^c) SAT circuit into every generated query; beta=0 removes the c-dependent exponent and gives the valid target bridge when max{rho,q}<1+epsilon.
- Split EF+SAT_U certificates: dense functional soundness over arbitrary label vectors triggers the prior naturalization audit; SAT-semantic soundness alone avoids that barrier but loses functional control.
- For nonfunctional certificates, impose the row-residual test: any D_N correct off R_N yields an exact H_N circuit by equality patching, with exponent max{s,e+1}.
- Tried to extract from a short EF+SAT_U derivation either a functional label property or an explicit Robust_N certificate; ordinary semantic SAT_U axioms do not force either outcome.

Blocking gap: No extraction/no-extraction theorem yet maps short EF+SAT_U proofs to functional label properties or to row-residual robustness against all subthreshold D_N.

## Falsifiers

- falsifier: a subthreshold D_N with C(D_N)<N^{1+epsilon-eta} and fewer than N^{epsilon-eta} wrong source rows gives C(H_N)<N^{1+epsilon-o(1)}.
- falsifier: a dense searchable EF+SAT_U certificate that is functional over label vectors becomes a valid natural-property object for the label model.
- falsifier: generator or verifier advice that selects exceptional rows nonuniformly breaks the target-preserving condition and invalidates the bridge.
- falsifier: any hidden positive-beta query growth restores the transfer cap q+beta c and cannot exclude all SAT polynomial exponents.

## Learning

Cycle 76 closes the Psys instantiation to EF+SAT_U and isolates the exact missing certificate strength: ordinary SAT-semantic soundness is not valid evidence unless it proves row-residual robustness above the patching threshold.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The abstract EF+SAT_U escape is now too broad; varying only the residual row exponent tests whether semantic certificates carry usable robustness or just ordinary soundness.
- Situation seed: Take H_N as the beta-zero XOR of M_N=N^q generated SAT formulas of length (log N)^d, and give EF+SAT_U a candidate proof that H_N disagrees with every circuit of size N^{1+epsilon-eta}.
- Varied variable: Residual row exponent e in |R_N|=N^e while holding approximator size exponent s=1+epsilon-2eta fixed.
- Held-fixed controls: q,rho<1+epsilon-3eta and d>1, so the beta-zero target transfer remains valid., G_N and the EF+SAT_U verifier are advice-free and use the same nonuniform SIZE accounting., SAT_U axioms are semantic only on the generated range U_N, not on arbitrary label vectors.
- Expected observation: A sharp knee at e=epsilon-2eta: below it, equality patching defeats the source claim; above it, EF+SAT_U must prove genuine residual robustness, not mere SAT soundness.
- Transfer certificate needed: A formal EF+SAT_U extraction/no-extraction theorem showing that accepted certificates either functionalize to label properties or imply Robust_N(s,e) in the source circuit model.

## Next Experiment

Formalize Robust_N(s,e) for EF+SAT_U and test whether a short proof can remain sound after replacing H_N by D_N off a sparse row set.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For a beta-zero XOR lower-bound certificate verifier, logarithmic target projection plus logarithmic proof-view decision width gives a valid natural property exactly when DirectClusterSound(C,s_N) holds. Replacing DirectClusterSound by ordinary proof soundness or local consistency is refuted by odd-charge Tseitin clusters whose projected shadow can accept every target truth table.

## Definitions

- source object: H_N^SAT is the beta-zero XOR function H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N<=N^{q+o(1)}, L_N=(log N)^d, and generator overhead N^{rho+o(1)}.
- target object: SIZE_N(s_N) is the nonuniform Boolean circuit class on N input bits with s_N=N^{1+epsilon} or the named threshold being audited.
- controlled interface: an enumerable local proof cluster C for a verifier V_N, with target projection Q(C), proof-view CSP W(C), and cluster shadow P_C over N-bit truth tables.
- target-preserving condition: DirectClusterSound(C,s_N) says no D in SIZE_N(s_N) and no assignment to the proof-view variables satisfy all checks in C when target labels are D restricted to Q(C).
- cluster shadow: P_C={F: there exists a proof-view assignment making all checks in C accept on F restricted to Q(C)}.
- projection-decision width: w(C) is the treewidth or decision-DP width of the proof-view CSP after the target labels in Q(C) are supplied.

## Assumptions

- Model: V_N is deterministic after fixing public coins, or the seed is fixed uniformly before the naturalness audit.
- Regime: h=|Q(C)| and w=w(C) satisfy h+w<=A log N for an absolute A.
- Uniformity: C and the local predicates of V_N are describable or enumerable in time poly(2^N), with no hidden polynomial advice selecting rows after seeing the target circuit.
- Completeness: H_N^SAT has an accepting global certificate whose restriction to C gives at least one accepting local view.
- Usefulness is against the exact target class SIZE_N(s_N), not against P or NP as a slogan.
- Naturalness pressure is conditional on PRFs computable in the targeted circuit class and secure against poly(2^N)-time truth-table distinguishers.

## Equations

- cluster_shadow: `P_C=\{F\in\{0,1\}^{2^N}:\exists y\; V_C(F|_{Q(C)},y)=1\}`. Valid when: Valid when C is fixed by a uniform enumeration and the verifier exposes only h target labels and a width-w proof-view CSP.
- density_lower_bound: `\mu(P_C)\ge 2^{-h}\ge N^{-A}`. Valid when: Valid when H_N^{SAT} has one accepting local proof view on C and the shadow condition constrains only the h queried target labels.
- constructivity_bound: `T_{decide}(P_C)\le \mathrm{poly}(2^N)\cdot 2^{O(w)}`. Valid when: Valid when the proof-view CSP has decision width w and its local predicates are computable within the stated truth-table time bound.
- usefulness_under_DCS: `P_C\cap TT(SIZE_N(s_N))=\varnothing`. Valid when: Requires DirectClusterSound for the exact target size s_N, with the same cluster C and no extra advice-dependent row selection.
- tseitin_shadow_failure: `\forall F\;\exists y\;V_C(F|_{Q(C)},y)=1\quad\Rightarrow\quad P_C=\{0,1\}^{2^N}`. Valid when: Applies to bounded-neighborhood odd-charge Tseitin clusters where local parity constraints are satisfiable but the global charge is inconsistent.

## Attempted Derivation

- Fix an accepting cluster C from the beta-zero XOR certificate and record h=|Q(C)| and proof-view decision width w.
- Define the shadow P_C by existentially quantifying only the proof-view labels seen by C while leaving all unqueried target labels free.
- Completeness gives H_N^SAT in P_C, so one accepting assignment to the h queried target bits yields density at least 2^{-h}.
- If w=O(log N), dynamic programming over the proof-view CSP decides P_C within poly(2^N) time, so the property is constructive in the natural-proofs sense.
- If DirectClusterSound(C,s_N) holds, no size-s_N circuit truth table lies in P_C, giving usefulness against the exact target class.
- If only ordinary soundness is available, odd-charge Tseitin supplies locally satisfiable clusters whose shadows ignore the target labels, so usefulness collapses.
- Independently, if the certificate leaves a sparse residual row set R_N, nonuniform equality patches give C(H_N^SAT)<=C(D_N)+O(|R_N|N), contradicting any subthreshold source lower bound.

Blocking gap: No named strong certificate system has yet been shown to satisfy DirectClusterSound at logarithmic projection width without also yielding a large constructive useful property. Resolution-style local traces fail the gap by the Tseitin falsifier.

## Falsifiers

- falsifier: odd-charge Tseitin with dummy SAT projection makes bounded local proof shadows satisfiable while global consistency is impossible.
- falsifier: sparse residual rows with |R_N|<N^{epsilon-o(1)} and approximator size below N^{1+epsilon} patch the source function under the claimed lower-bound threshold.
- falsifier: a PRF family in SIZE_N(s_N) secure against poly(2^N)-time distinguishers conflicts with any large constructive useful cluster shadow.
- falsifier: q or rho at least the claimed source exponent makes the beta-zero XOR substitution cap too large for valid target transfer.
- falsifier: nonuniform row-selection advice can encode the hard part unless the certificate proves exact agreement or blocks residual leakage.

## Learning

Cycle 76 sharpens the support branch into a trichotomy: logarithmic cluster projection with DirectClusterSound naturalizes; ordinary local proof soundness is refuted by the odd-charge Tseitin falsifier; and sparse residual leakage collapses the claimed source lower bound by an explicit patching inequality. This is valid route-level certification work, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The branch needs a concrete target-preserving stress test because the remaining distinction is not philosophical barrier status but whether logarithmic proof shadows are useful, natural, or locally fakeable.
- Situation seed: Embed an odd-charge Tseitin graph of girth larger than 10 log N as the proof-view consistency layer of a padded beta-zero XOR SAT-query family H_N^SAT, with SAT labels routed through dummy projections on the sampled cluster.
- Varied variable: projection size h=|Q(C)|, varied from c log N to N^gamma while keeping proof-view decision width O(log N).
- Held-fixed controls: M_N<=N^{q+o(1)} and L_N=(log N)^d for the beta-zero XOR carrier., Generator overhead N^{rho+o(1)} and the same unrestricted nonuniform circuit basis., Target threshold s_N=N^{1+epsilon} and no advice-dependent row selection., Verifier locality and ordinary line-local soundness are held fixed unless DirectClusterSound is explicitly added.
- Expected observation: For h=O(log N), either DirectClusterSound makes P_C a dense constructive useful property, or the Tseitin layer makes P_C density one and not useful. For h=N^gamma, largeness pressure weakens but the route loses the advertised logarithmic certificate advantage.
- Transfer certificate needed: A proof of DirectClusterSound(C,s_N) for the named Psys, or a theorem that dependency closure/global consistency necessarily raises h or w above the naturalization threshold.

## Next Experiment

Instantiate Psys=Resolution-trace and Psys=Polynomial-Calculus-trace: compute the dependency-closure size needed to turn ordinary soundness into DirectClusterSound, and test whether that closure forces h+w=omega(log N) or produces a natural property.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For the beta-zero XOR family H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), any DirectClusterSound-MCSP_beta0 certificate implementation with adaptive-cover exponent alpha_ad and residual exponent r gives C(H_N^SAT)<=N^{max{rho,q+alpha_ad,r+1}+o(1)}. Hence a claimed lower bound C(H_N^SAT)>N^{1+epsilon} is falsified whenever max{rho,q+alpha_ad,r+1}<1+epsilon.

## Definitions

- source object: DirectClusterSound-MCSP_beta0 certificate family Pi_N whose accepted certificate opens putative labels A_N(x,j) for SAT(G_N(x,j)) and optionally carries MCSP/MKtP lower-bound annotations for the induced label rows.
- target object: the unrestricted Boolean circuit lower bound C(H_N^SAT)>N^{1+epsilon} and any length-balanced E-language lower bound extracted from that explicit truth-table family.
- controlled interface: an adaptive certificate opener with setup exponent tau, level-l summary count/width exponents a_l,mu_l, local opener exponents omega_l, and residual set R_N where semantic agreement is not forced.
- target-preserving condition: the verifier, residual enumerator, generator G_N, and any hard-row selector are advice-free and E-uniform; for the no-go direction, even nonuniform hardwiring of a low-cover certificate is enough to refute an unrestricted lower-bound claim.
- Beta-zero regime: M_N<=N^{q+o(1)}, L_N=(log N)^d, and the query generator has circuit overhead N^{rho+o(1)} on the same N scale.
- Residual exponent: |R_N|<=N^{r+o(1)} and D_N(x)=xor_j A_N(x,j) agrees with H_N^SAT outside R_N.

## Assumptions

- Circuit model is unrestricted fan-in-two Boolean circuits; singleton correction for an exceptional x costs O(N) in the packet's size convention.
- Psys soundness is semantic, not merely local: accepted labels equal SAT(G_N(x,j)) for every nonresidual x and all queried j.
- The adaptive cover is a true functional opener for labels, not only a verifier transcript that cannot be used to compute A_N(x,j).
- All exponents q,rho,r,epsilon,tau,a_l,mu_l,omega_l are fixed constants up to o(1) losses.
- Non-claim boundary: the lemma is a route-specific falsifier for this carrier interface, not a proof of P != NP.

## Equations

- adaptive_cover_exponent: `\alpha_{ad}=\max\{\tau,\max_l(a_l+\mu_l),\max_l\omega_l\}.`. Valid when: Valid when the source is DirectClusterSound-MCSP_beta0 and the certificate transcript has the declared adaptive cover parameters.
- xor_approximant_upper_bound: `C(D_N)\le N^{\max\{\rho,q+\alpha_{ad}\}+o(1)}.`. Valid when: Valid when M_N<=N^{q+o(1)} and each opened SAT-label bit is computed by the flattened adaptive cover circuit.
- residual_correction_upper_bound: `C(H_N^{SAT})\le C(D_N)+O(|R_N|N)\le N^{\max\{\rho,q+\alpha_{ad},r+1\}+o(1)}.`. Valid when: Applies after D_N agrees with H_N^SAT outside an enumerated residual set R_N of size N^{r+o(1)}.
- finite_falsifier_threshold: `\max\{\rho,q+\alpha_{ad},r+1\}<1+\epsilon\Rightarrow \neg[C(H_N^{SAT})>N^{1+\epsilon}].`. Valid when: Requires the target lower-bound claim and the constructed upper bound to use the same unrestricted circuit model and N-scale.

## Attempted Derivation

- Fix H_N^SAT with M_N<=N^{q+o(1)} and generator overhead N^{rho+o(1)}.
- Assume an accepted DirectClusterSound-MCSP_beta0 certificate opens labels A_N(x,j) through an adaptive cover of exponent alpha_ad.
- Flatten the adaptive transcript into a nonuniform circuit for each label bit; the largest cost is N^{alpha_ad+o(1)} by the alpha_ad maximum.
- Compute D_N(x)=xor_{j<=M_N} A_N(x,j) using M_N copies of the opener, giving size N^{max{rho,q+alpha_ad}+o(1)}.
- Use semantic soundness outside R_N to identify D_N with H_N^SAT off the residual set.
- Hardwire residual corrections; the branch convention charges O(|R_N|N)=N^{r+1+o(1)} gates.
- Compare with the claimed N^{1+epsilon} lower bound. If max{rho,q+alpha_ad,r+1}<1+epsilon, the certificate carrier proves its own subthreshold upper bound.

Blocking gap: To turn this into a paper-ready theorem for DirectClusterSound(C,k), one must prove that its accepted certificates really provide functional SAT-label openings or else state the alternative no-go: local consistency without functional opening is not a lower-bound certificate.

## Falsifiers

- falsifier: q+alpha_ad below 1+epsilon while residual exponent r<epsilon gives an explicit subthreshold circuit for H_N^SAT.
- falsifier: a sparse residual list with |R_N|<=N^{epsilon-o(1)} converts any approximant into C(H_N^SAT)<=N^{1+epsilon-o(1)}.
- falsifier: a hard-row selector using nonuniform advice yields at most hard strings, not a valid E-uniform language consequence.
- falsifier: DirectClusterSound local consistency without semantic SAT-label forcing cannot support the bridge; it is ordinary soundness only.
- falsifier: Merkle/checkpoint/digest proof streams with alpha_ad<theta are row-circuit upper bounds, not MCSP no-side certificates.

## Learning

Cycle 76 upgrades the prior alpha_ad audit by coupling it to the beta-zero query count and sparse residual correction. The useful theorem-shaped claim is not P != NP; it is a valid finite falsifier: low-cover MCSP/MKtP label certificates imply C(H_N^SAT)<=N^{max{rho,q+alpha_ad,r+1}+o(1)}, so they cannot certify a stronger beta-zero XOR lower bound.

## Gedanken Experiment Design Seed

- Need decision: `design-now-as-falsifier-probe`
- Rationale: The branch needs a concrete exponent phase test for beta-zero XOR certificates, not another abstract hardness-magnification restatement.
- Situation seed: A padded SAT-query family H_N^SAT with M_N=N^q polylog-length queries, together with a DirectClusterSound-MCSP certificate whose Merkle-like label oracle opens SAT labels and leaves a residual set R_N.
- Varied variable: adaptive cover exponent alpha_ad, varied across the threshold 1+epsilon-q while q,rho,r are fixed.
- Held-fixed controls: M_N<=N^{q+o(1)} and L_N=(log N)^d remain beta-zero., Generator overhead remains N^{rho+o(1)}., Residual size remains |R_N|<=N^{r+o(1)}., Target claim remains the unrestricted lower bound C(H_N^SAT)>N^{1+epsilon} with no advice in the positive transfer.
- Expected observation: Below alpha_ad<1+epsilon-q and r<epsilon, the certificate collapses into a small circuit for H_N^SAT; above the threshold, this falsifier stops explaining failure and the route must prove genuine high-cover row hardness.
- Transfer certificate needed: A formal flattening lemma from the adaptive opening transcript to unrestricted circuits, plus a semantic-soundness lemma that D_N agrees with H_N^SAT off the residual list.

## Next Experiment

Instantiate DirectClusterSound(C,k) with explicit certificate size, opening tree, and residual definition; compute tau,a_l,mu_l,omega_l,r and decide whether max{rho,q+alpha_ad,r+1}<1+epsilon or whether the model escapes by lacking functional SAT-label openings.
