# cycle-0133

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Restricted theorem packet: for Psys_bEF^- plus transparent FormulaEval plus declared bounded TSR, a proof pi of LB_N(1+epsilon) for the beta-zero parity carrier yields a same-model circuit of size at most N^{rho+o(1)}+Gamma_DTSR(pi)+O(E_pi N). Thus any subthreshold pi is a valid falsifier for that source lower-bound certificate, not a proof of P != NP.

## Definitions

- source object: H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), where M_N=N^{q+o(1)}, G_N has circuit size N^{rho+o(1)}, and each generated SAT instance has length (log N)^d with d>1.
- target object: the same nonuniform SIZE model upper bound contradicting a claimed source statement LB_N(1+epsilon) for H_N^SAT; the target is not NP not subset P/poly.
- controlled interface: Psys_bEF^- with bit-explicit EF support, least reachable transparent support K_dag(pi), same-theory row expansion, bounded SR_h ledgers, and declared bounded Tseitin self-reduction child rows.
- target-preserving condition: beta=0, no hidden support advice, all FormulaEval and TSR influences are listed before later use, row expansion is charged in Gamma_DTSR, and the circuit/proof model is unchanged.

## Assumptions

- Length regime: N ranges over valid carrier lengths, epsilon>0 is fixed, q,rho,kappa,theta,eta,tau are constants up to o(1) slack, and M_N=N^{q+o(1)}.
- Proof syntax regime: every nonsemantic line exposes line kind, parent pointers, row index x, slot index j, formula address, selector code, occurrence-neighborhood certificate, and extension-variable dependencies.
- K_dag(pi) is computed as the least fixed point from the final LB_N line by adding all visible FormulaEval supports, all parent dependencies, all same-theory row expansions, and all declared TSR children reachable from already-live rows.
- Declared TSR regime: the set of active parent rows has size N^{kappa+o(1)}, each parent lists N^{theta+o(1)} restriction children, and the local verifier checks syntactic Tseitin restriction rather than SAT-truth branch pruning.
- Uniformity and advice status: enumeration of K_dag and DTSR children is proof-bit uniform; no selector may use nonuniform SAT-truth advice unless RealSATInfluenceRealizer_N^arb supplies a charged row set first.
- Error regime: E_pi source rows may be corrected by equality patches of cost O(E_pi N) in the same nonuniform SIZE model.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j<M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)}`. Valid when: Valid when N is in the carrier length set and G_N uniformly outputs polylogarithmic SAT instances with beta equal to zero.
- ledger: `\Gamma_{DTSR}(\pi)=\Gamma_{bEF}(\pi)+U_N(K_{dag})+X_N(K_{dag})+B_{SR_h}(\pi)+B_{DTSR}(\pi)`. Valid when: Applies when every proof line has visible dependencies and K_dag is the least prefix-closed reachable support fixed point.
- DTSR_charge: `B_{DTSR}(\pi)=N\cdot |A_N|\cdot N^{\theta+o(1)}=N^{1+\kappa+\theta+o(1)}`. Valid when: Requires complete child declaration for |A_N|=N^{kappa+o(1)} active parent rows and syntactic same-theory expansion for every child.
- parser_upper_bound: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{DTSR}(\pi)+O(E_\pi N)`. Valid when: Valid after line induction converts the charged transcript into a same-model circuit and only sparse residual rows remain.
- source_falsifier_window: `N^{\rho+o(1)}+\Gamma_{DTSR}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Applies when LB_N asserts a same-model N^{1+epsilon-o(1)} lower bound for the identical carrier H_N^{SAT}.
- beta_zero_target_substitution: `SAT\in SIZE(n^c)\Rightarrow C(H_N^{SAT})\le N^{\max\{\rho,q\}+o(1)}`. Valid when: Valid when query length is polylogarithmic, beta is zero, and the SAT circuit is used only on generated instances.

## Attempted Derivation

- Source statement: LB_N(1+epsilon) claims C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)} for the named beta-zero parity carrier, in the same nonuniform circuit model used by the parser simulation.
- Target statement: under TransparentRowSupport_N^DTSR, a proof pi with subthreshold Gamma_DTSR gives C_SIZE(H_N^SAT)<N^{1+epsilon-o(1)}, hence pi is a route-level falsifier of that source certificate.
- Model context: source carrier is H_N^SAT, target class for the bridge audit is nonuniform SIZE, proof model is Psys_bEF^- plus transparent FormulaEval and declared bounded TSR, and reduction type is parser-to-circuit simulation plus sparse equality patching.
- Quantifier context: constants q,rho,kappa,theta,epsilon are fixed; N tends through valid lengths; beta=0 via polylogarithmic SAT queries; enumeration and row expansion are advice-free except for explicit proof bits.
- Bit fields fixed for DTSR lines: line kind, parent ids, source row x, slot j, formula-node address a, restriction mask r, child id, occurrence-neighborhood interval list, selector program id, and closure pointers into K_dag.
- Closure algorithm: start from final LB_N line; repeatedly add parent dependencies, visible FormulaEval supports, same-theory row expansions, bounded SR_h leaves, and every declared TSR child of every active parent row until no new row appears.
- Line induction: bEF and extension lines charge Gamma_bEF; transparent FormulaEval charges U_N(K_dag)+X_N(K_dag); SR_h charges B_SR_h; declared TSR charges N times the number of active parent-child certificates; sparse failures charge O(E_pi N).
- DTSR rule case: for each active parent row, the verifier recomputes the syntactic Tseitin restriction child and its touched occurrence neighborhood; because all children are declared, later semantic use cannot introduce an uncharged row.
- Countermodel step: if the first later-used child is absent from K_dag, construct two SAT-label environments agreeing on charged rows and differing on that child; the proof transcript is unchanged but the dependent final predicate changes, so the parser theorem is invalid for hidden pruning.
- Barrier status: the positive restricted theorem is relativizing over visible labels and therefore cannot prove a real SAT lower bound; the escape for full semantic pruning must be nonrelativizing through RealSATInfluenceRealizer_N^arb, not a generic natural-proofs or algebrization slogan.

Blocking gap: Full semantic branch pruning remains blocked at RealSATInfluenceRealizer_N^arb: no proof here uniformly lists all real-SAT-influencing rows when the branch choice is determined by semantic satisfiability rather than declared syntax.

## Falsifiers

- first-unlisted-child DTSR private-row falsifier for hidden semantic pruning
- unread-enable-bit FormulaEval falsifier when reachable influence is not prefix-closed
- q<epsilon support-density contradiction for slot-bounded transparent certificates
- positive-beta substitution cap q+beta*c+o(1) for black-box hardness magnification claims
- nonuniform SAT-truth selector hiding eta,tau,kappa,theta outside Gamma_DTSR

## Learning

Cycle 133 upgrades declared bounded TSR from a compatible rule case to a live inference-quality theorem packet: complete child declarations are sufficient for the Gamma_DTSR parser and necessary up to a first-unlisted-child falsifier. The valid contribution is a scoped TransparentRowSupport_N^DTSR theorem/countermodel boundary; full semantic pruning remains exactly blocked at RealSATInfluenceRealizer_N^arb.

## Gedanken Experiment Design Seed

- Need decision: `use_as_falsifier_probe_now`
- Rationale: The branch already has the beta-zero transfer; the remaining uncertainty is whether semantic DTSR pruning can evade the transparent ledger without paying row expansion. A concrete first-hidden-child experiment tests exactly that boundary.
- Situation seed: Construct H_N^SAT with M_N=N^{q+o(1)} polylog SAT slots and a Psys_sym DTSR line where each active parent formula has N^{theta} possible restriction children, but an unread enable bit chooses one child semantically after the declared list is fixed.
- Varied variable: theta, the declared-child fanout exponent per active DTSR parent row.
- Held-fixed controls: beta=0 polylogarithmic SAT query length and generator overhead N^{rho+o(1)}, active parent exponent kappa and lower-bound threshold epsilon, same nonuniform SIZE model for source lower bound and parser upper bound, K_dag least fixed-point closure from the final LB_N line, no SAT-truth advice except through a charged RealSATInfluenceRealizer_N^arb
- Expected observation: If all N^{theta+o(1)} children are declared, the charge is N^{1+kappa+theta+o(1)} and the theorem is valid. If one later-used child is hidden, two visible-equivalent transcripts differ on the final dependent row, giving the first-unlisted-child falsifier.
- Transfer certificate needed: A valid semantic escape must give an advice-free nonrelativizing real-SAT influence realizer that lists the hidden child set before use, proves same-theory row expansion, and inserts its N^{1+kappa+theta+o(1)} charge into Gamma_DTSR.

## Next Experiment

Attack RealSATInfluenceRealizer_N^arb for one concrete semantic pruning rule: bounded Tseitin self-reduction with a SAT-truth branch-elimination premise. Either produce a uniform charged list of all influencing children or formalize the first semantic line where the private-row countermodel survives.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For the concrete unannotated existential-index bounded-SR_h FormulaEval rule, visible enumeration or a visible row-cover certificate is exactly the target-preserving realizer needed to fold the rule into TransparentRowSupport_N; without it the rule is a semantic escape. This discharges one RealSATInfluenceRealizer_N subcase, not full Psys_sym.

## Definitions

- source object: a Psys_sym^{existsSR_h,enum} proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with N=2^n and M_N=N^{q+o(1)}.
- target object: a same-N nonuniform Boolean SIZE upper-bound falsifier or, if the falsifier inequality fails, a forced row-equivalent support lower bound.
- controlled interface: each existential-index FormulaEval line L exposes a proof-visible selector A_L, a local touch map T_L(a) of size at most h, an extensionality certificate, and a same-theory row-expansion template.
- target-preserving condition: the parser is deterministic and advice-free, row expansions use the same SAT/G_N/H_N carrier, and all influencing rows are included in the charged support before the semantic rule is used.
- bridge observable: K_exists(pi) is the least prefix-closed reachable row set generated by bEF rows and by T_L(a) for all reachable visible existential witnesses a.
- charge observable: U_exists(pi) is selector/enumerator verification debt and N|K_exists(pi)| is the row-expansion bit debt.

## Assumptions

- Model is nonuniform Boolean SIZE over the fixed beta-zero SAT-parity carrier, not a many-one reduction from SAT.
- Length regime is N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, h=N^{eta+o(1)}, selector-domain exponent alpha, and generator size N^{rho+o(1)}.
- Uniformity condition is deterministic no-advice parsing from (N,pi); the selector A_L and touch map T_L are proof-visible finite strings or certified row-cover objects.
- Same-theory condition is prefix splicing with fresh extension variables; no semantic oracle line may be imported without its row expansion and charge.
- Naturalness audit is conditional: if the extracted object becomes a large constructive useful truth-table property, the natural-proofs falsifier applies, but this lemma itself is a proof-system parser theorem.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j))`. Valid when: Valid when N=2^n, rows are indexed by j<=M_N, and the generator G_N is the fixed beta-zero SAT-parity carrier.
- least_support: `K_{\exists}(\pi)=\operatorname{lfp}\left(K_{bEF}(\pi)\cup \bigcup_{L\in Reach(\pi)}\bigcup_{a\in A_L}T_L(a)\right)`. Valid when: Requires proof-visible selector and touch-map codes so the closure is computable without SAT-truth advice or hidden witness choice.
- visible_existential_charge: `\Gamma_{\exists}(\pi)=\Gamma_{bEF}(\pi)+U_{\exists}(\pi)+N\cdot |K_{\exists}(\pi)|`. Valid when: Applies after every reachable existential FormulaEval line is replaced by same-theory row-expanded material and charged enumerator debt.
- exponent_bound: `\Gamma_{\exists}(\pi)\le \Gamma_{bEF}(\pi)+N^{\tau+\alpha+\sigma+o(1)}+N^{1+\tau+\alpha+\eta+o(1)}`. Valid when: Valid when each proof has N^{tau+o(1)} relevant lines, each selector domain has size at most N^{alpha+o(1)}, each touch set has h=N^{eta+o(1)} rows, and selector verification costs N^{sigma+o(1)}.
- parser_falsifier: `N^{\rho+o(1)}+\Gamma_{\exists}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow \pi \text{ is not a valid proof of } LB_N(1+\epsilon)`. Valid when: Applies after the transparent expansion preserves the same carrier and the claimed lower bound is against SIZE(N^{1+epsilon-o(1)}).
- forced_support: `\widehat S_{\exists}:=|K_{\exists}|+N^{-1}U_{\exists}+N^{-1}\Gamma_{bEF}\ge N^{\epsilon-o(1)}`. Valid when: Applies to sound accepted proofs when rho<1+epsilon and the subthreshold upper-bound falsifier has been ruled out.

## Attempted Derivation

- Fix the concrete semantic rule UidxSR_h: a FormulaEval line L asserts exists a in A_L such that the bounded SR_h predicate Phi_L(a,H[T_L(a)]) holds, where |T_L(a)|<=h.
- Restrict to the visible-enumeration fragment: A_L, the verifier for A_L, T_L, and an extensionality certificate are encoded in the proof line or in prior extension variables with prefix-scoped definitions.
- Run a deterministic worklist from the final LB_N line. When a reachable UidxSR_h line is popped, enumerate every a in A_L, verify the selector, add T_L(a) to K_exists, and enqueue any bEF dependencies needed by the row-expansion template.
- Prefix-splice the expansion: replace the semantic existential atom by an OR over the enumerated local SR_h predicates, using fresh extension variables and the previously audited bit-level bEF verifier for each touched row.
- Charge selector verification to U_exists and charge each expanded row by N bits, giving Gamma_exists=Gamma_bEF+U_exists+N|K_exists|. For |pi|=N^tau, |A_L|<=N^alpha, h=N^eta, the new exponent is tau+alpha+eta in row-equivalent units.
- Invoke the existing same-model parser-to-circuit lemma: if N^rho+Gamma_exists<N^{1+epsilon-o(1)}, the accepted proof cannot be a valid proof of LB_N(1+epsilon). Otherwise the normalized support inequality Shat_exists>=N^{epsilon-o(1)} follows.
- For the unannotated hidden fragment, choose the first feasible row r* outside the charged support and toggle the private enable bit controlling Phi_L at r*. The displayed transcript and charged rows are unchanged, but the semantic FormulaEval value changes, refuting occurrence completion.

Blocking gap: The proof is complete only for visible-enumeration or visible-row-cover UidxSR_h. Arbitrary semantic FormulaEval remains blocked at HiddenFeasibleSetExtensionality_N: proof syntax must uniformly determine all feasible influencing rows before the rule is charged.

## Falsifiers

- Hidden-enable UidxSR_h line: the proof displays exists a Phi(a) but the only satisfying a is behind an unread enable bit outside K_exists; this is a finite falsifier to surface occurrence parsing.
- Selector-domain exponent alpha with tau+alpha+eta>=epsilon: visible enumeration is valid but no longer subthreshold, so the claimed LB_N falsifier collapses into mere support pressure.
- Semantic SAT advice choosing A_L from the true SAT table: K_exists cannot be computed from (N,pi), violating the no-advice target-preserving condition.
- Projected dDNNF without row-cover certificates: a first omitted reachable row gives the same hidden-row countermodel as the UidxSR_h rule.
- Natural-proof falsifier probe: if the expanded support certificate becomes a poly(N)-constructive large useful truth-table property against the named SIZE class, PRF tension applies to that induced property.

## Learning

Cycle 133 resolves one concrete semantic FormulaEval boundary: existential-index bounded-SR_h is target-preserving exactly when feasible witnesses are visibly enumerated or row-covered. The new quantitative cost is alpha: the subthreshold parser falsifier requires tau+alpha+eta<epsilon, while hidden feasible witnesses give a finite no-realizer countermodel. This is valid route-level proof-system certification, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The abstract RealSATInfluenceRealizer_N gap has been narrowed to one existential-index SR_h rule; varying the visible selector-domain exponent tests whether transparency gives a real subthreshold transfer or only a charged but too-expensive expansion.
- Situation seed: Use H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with one UidxSR_h FormulaEval line whose candidate set A_L has size N^alpha and whose local neighborhood T_L(a) contains h=N^eta rows; compare a visible full-enumeration version with an unread-enable-bit hidden-witness version.
- Varied variable: alpha, the exponent of the proof-visible existential candidate set |A_L|=N^{alpha+o(1)}.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, and the same SAT-parity carrier H_N^SAT are fixed., Proof length exponent tau, local neighborhood exponent eta, generator size exponent rho, and lower-bound target N^{1+epsilon} are fixed., The transparent run uses deterministic no-advice parsing and same-theory prefix splicing., The hidden run keeps the displayed proof syntax and all charged rows identical while toggling only the private enable row.
- Expected observation: For visible enumeration, the transfer threshold is tau+alpha+eta<epsilon up to lower-order debts; at equality the theorem yields near-full row pressure, and above it the expansion is valid but not a lower-bound falsifier. For hidden witnesses, one private row changes the semantic line without changing Gamma_surf.
- Transfer certificate needed: A formal RowCoverOrEnumerate certificate: proof-visible A_L, proof-visible T_L, extensionality forall a in A_L T_L(a) subset K_exists, and a prefix-splice bEF expansion before the FormulaEval line is used.

## Next Experiment

Write the finite checker for K_exists(pi): input a proof line L, enumerate A_L, compute T_L(a), verify the row-cover extensionality clause, update the least prefix-closed support, and run it on two toy instances, one with alpha=0 witness annotation and one with alpha>0 full enumeration plus an unread-enable-bit hidden-row falsifier.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For bit-explicit Psys_sym^QE proofs, a prefix-visible exit-dominator forest plus auditable first-owner row certificates is sufficient for the TransparentRowSupport_N parser simulation: every quarantined FormulaEval influence is charged exactly once before first external use. If an influential row has no prefix-visible owner, the first such line yields a private-row falsifier.

## Definitions

- source object: a Psys_sym^QE proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, generator time N^{rho+o(1)}, and bEF-normal bit fields.
- target object: a same-theory nonuniform SIZE circuit upper bound for H_N^SAT contradicting the asserted LB_N(1+epsilon) when the charged transcript exponent is below 1+epsilon.
- controlled interface: quarantined FormulaEval blocks with visible block_id, parent_block, entry_line, exit_line, external-dependency list, row-set certificate pointer, dominance labels, and first-owner tags for rows.
- target-preserving condition: every SAT row used by FormulaEval is enumerated or fully scanned, expanded in the same SAT-row theory, and charged before first external dependency; no semantic advice or hidden row selector is used.
- K_QE(pi) is the union of row indices owned by prefix-visible exits reachable from the final LB_N line in the dominator forest.
- An exit owns row r at its first prefix occurrence only if a transparent enumerator or RowSetEqualityWitness_N proves r is in the exit row set and not already owned by an earlier visible exit.

## Assumptions

- Model: nonuniform SIZE for the target circuit and Cook-Reckhow style bit-explicit Psys_sym^QE syntax for the source proof transcript.
- Regime: N tends to infinity, M_N=N^{q+o(1)}, formula length is N^{o(1)}, bEF parsing costs eta,tau are already included in Gamma_bEF(pi).
- Uniformity: all dominance labels, row enumerators, and owner tags are computable from N and proof prefix pi_{<=t}; no advice-selected hard row or SAT-truth selector is permitted.
- Same-theory condition: every row expansion uses the same SAT-row formulas G_N(x,j) that define H_N^SAT, not an external semantic oracle.
- Timing condition: a quarantined block may delay support only while sealed; its exit must dominate all later external dependencies and pay the full newly owned support cone.
- Deduplication condition: shared row sets may be charged once only with prefix-visible equality or inclusion witnesses; otherwise each exit pays separately or the hidden symmetric difference is a countermodel.

## Equations

- QE ledger: `\Gamma_{QE}(\pi)=\Gamma_{bEF}(\pi)+U_{QE}(\pi)+X_{QE}(\pi)+D_{QE}(\pi)`. Valid when: Valid when Psys_sym^QE provides prefix-visible dominance certificates, transparent row ownership, and bEF-normal rule parsing for every reachable proof line.
- first-owner enumeration cost: `U_{QE}(\pi)=\sum_{x\in Exits(\pi)} EnumCost(R_x\setminus \bigcup_{y<x}R_y)+DomCert(\pi)`. Valid when: Applies when row-set differences are certified by visible enumerators, scans, or RowSetEqualityWitness_N before the exit is externally used.
- row expansion charge: `X_{QE}(\pi)\ge N^{1+o(1)}\cdot |K_{QE}(\pi)|`. Valid when: Requires beta-zero SAT row expansion where each owned row contributes its full same-theory truth row over N input assignments.
- parser upper bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{QE}(\pi)+O(E_\pi N)`. Valid when: Valid after the line induction converts the charged proof transcript and generator into a same-model nonuniform circuit for H_N^SAT.
- subthreshold falsifier: `N^{\rho+o(1)}+\Gamma_{QE}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Applies only when LB_N is asserted against the identical nonuniform SIZE model simulated by the charged parser circuit.

## Attempted Derivation

- Source statement: pi is a bit-explicit Psys_sym^QE transcript deriving LB_N(1+epsilon) for H_N^SAT with FormulaEval lines possibly sealed inside syntactic quarantine blocks.
- Target statement: construct a same-model nonuniform circuit for H_N^SAT of size N^{rho+o(1)}+Gamma_QE(pi)+O(E_pi N), yielding a falsifier if this is below N^{1+epsilon-o(1)}.
- Define a block graph from proof bits: each block records entry, exit, parent, external dependencies, row-set certificate pointer, and dominance interval labels.
- Compute reachable exits backward from the final LB_N line; discard sealed blocks with no external dependency and require each used block exit to dominate all outgoing edges from its interior.
- At each exit x, run the visible row enumerator or full scan and attach owner tags only for rows not previously owned by prefix-earlier reachable exits, using RowSetEqualityWitness_N for deduplication.
- Maintain invariant I_t: every unquarantined line depending on FormulaEval rows after time t is a function only of bEF-normal bits plus rows already in K_QE(t) and already charged in Gamma_QE(t).
- Base cases and ordinary bEF rules use the archived Gap98-SRhNormalForm ledger and add only Gamma_bEF charges.
- A sealed quarantine interior may contain delayed support, but no external line may depend on it before the exit; the exit commutes to the first external use and pays U_QE plus X_QE for newly owned rows.
- FormulaEval lines outside quarantine are treated as singleton exits, so the older TransparentRowSupport_N theorem is recovered as a special case.
- If invariant I_t first fails, choose the earliest external line and an unowned influential row j; two occurrence completions agree on all charged/read bits but differ on SAT(G_N(x,j)) or its enable bit, contradicting claimed derivability and giving the finite private-row falsifier.

Blocking gap: The restricted theorem still needs a fully formal RowSetEqualityWitness_N grammar for projected/shared row-set deduplication. Without that grammar the proof remains valid only with fallback sum charging or with the private-row countermodel.

## Falsifiers

- A quarantined exit does not dominate every later external dependency on its delayed FormulaEval support.
- First-owner tags are chosen by advice, lexicographic hard-row selection, or SAT-truth pruning rather than by prefix-visible proof bits.
- Two exits claim shared support but provide no RowSetEqualityWitness_N; a private row in the semantic symmetric difference flips the parity line.
- A semantic FormulaEval rule exposes membership but not the row values needed for same-theory expansion, so X_QE is undercharged.
- The charged transcript satisfies N^{rho+o(1)}+Gamma_QE(pi)+O(E_pi N)<N^{1+epsilon-o(1)}, which is a same-model falsifier for LB_N(1+epsilon).
- The support-density corollary is invoked when K_QE is not influence-complete; the first hidden influence invalidates the derivation.

## Learning

Cycle 133 adds a proof-auditable ownership layer to the QE dominator-forest theorem: row sharing is charged by first-owner certificates, not semantic equality. The new finite obstruction is RowSetEqualityWitness_N failure, which forces sum charging or a private-row falsifier. This strengthens the paper parser module and remains route-level support, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The live gap is not another abstract barrier but whether shared quarantined FormulaEval support can be charged once without importing semantic row advice.
- Situation seed: A beta-zero H_N^SAT proof with two nested Psys_sym^QE FormulaEval blocks whose projected-dDNNF selectors have the same projected row support but different auxiliary witnesses.
- Varied variable: The overlap/equality certificate exponent omega, ranging from explicit disjoint supports through witnessed equality to purely semantic equality without RowSetEqualityWitness_N.
- Held-fixed controls: M_N=N^{q+o(1)} and generator overhead N^{rho+o(1)} are fixed., Both exits are prefix-visible and dominate all external dependencies., SAT-row expansion remains same-theory and costs N^{1+o(1)} per owned row., No nonuniform row selector, SAT-truth pruning, or post-hoc support discovery is allowed.
- Expected observation: With a valid equality witness, the parser charges N^{1+o(1)} times the union size; without it, either the sum charge is necessary or an unread enable/private-row completion changes the final parity while preserving all charged proof bits.
- Transfer certificate needed: A prefix-visible dominator label system plus RowSetEqualityWitness_N proving row-set equality, inclusion, or certified difference before first external use; otherwise the intuition is quarantined as a falsifier probe.

## Next Experiment

Write the RowSetEqualityWitness_N grammar for one projected-dDNNF shared-support example: either certify equality/inclusion with prefix-visible decomposition and compute union charge, or exhibit the smallest semantic symmetric-difference private-row countermodel.
