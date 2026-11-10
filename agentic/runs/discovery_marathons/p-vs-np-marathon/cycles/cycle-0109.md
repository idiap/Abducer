# cycle-0109

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: TransparentRowSupport theorem pair

## Candidate Lemma

For the beta-zero SAT-parity carrier, every Psys_sym proof whose FormulaEval mechanisms satisfy TransparentRowSupport_N has a charged transcript Gamma_trans(pi). If N^{rho+o(1)}+Gamma_trans(pi)+E_N N^{1+o(1)}<N^{1+epsilon-o(1)}, then the asserted source lower bound LB_N(1+epsilon) is false in the same nonuniform SIZE model.

## Definitions

- source object: H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), with |x|=N, M_N=N^{q+o(1)}, |G_N(x,j)|=(log N)^d, and source statement LB_N(1+epsilon): C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)}.
- target object: a nonuniform SIZE circuit for H_N^SAT of size below N^{1+epsilon-o(1)}, used only as a parser-to-circuit falsifier of LB_N, not as a proof of P != NP.
- controlled interface: TransparentRowSupport_N for Psys_sym FormulaEval lines: visible selector code, advice-free RowSet enumeration or full scan, influence closure, same-theory occurrence expansion, and no hidden semantic support advice.
- target-preserving condition: the generator, parser, FormulaEval expansion, and sparse-row correction are all interpreted in the same nonuniform SIZE model, with beta=0 polylog target formula length and no upgrade from occurrence-local claims to full semantic EF+SAT.

## Assumptions

- Circuit model is nonuniform Boolean SIZE over source length N; proof parsing may be uniform polynomial time but supplies no extra advice beyond pi and fixed G_N.
- Generator G_N has circuit size N^{rho+o(1)} and outputs SAT instances of length L_N=(log N)^d, so target SAT substitution has beta=0 and costs N^{o(1)} per queried instance under any fixed polynomial SAT upper bound.
- Psys_bEF^- lines already have bit-explicit verifier fields, parent pointers, occurrence neighborhoods, and bounded-SR_h charges included in Gamma_bEF(pi).
- Each transparent FormulaEval line ell has a syntactic selector S_ell, a certified enumerator Enum_ell or certified full-scan bit, and an influence-closed RowSet_ell that contains every row whose SAT label can change the line value in the same theory.
- Sparse residual errors E_N are literal source rows whose equality patches cost E_N N^{1+o(1)}; no semantic advice may choose them after seeing the SAT labels.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j<M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad |G_N(x,j)|=(\log N)^d`. Valid when: Valid when the source carrier is the fixed beta-zero batched SAT parity family with uniformly generated polylogarithmic formulas.
- transparent-charge: `\Gamma_{trans}(\pi)=\Gamma_{bEF}(\pi)+U_N(\pi)+X_N(\pi),\quad X_N=N^{1+o(1)}\sum_{\ell\in FE(\pi)} |K_{idx}(\ell)|`. Valid when: Valid when every FormulaEval line satisfies TransparentRowSupport_N and each charged row expansion is same-theory occurrence explicit.
- full-scan-bound: `X_N(\pi)\le F_{FE}(\pi)\,N^{1+q+o(1)}\quad\text{for certified full-scan FormulaEval lines}`. Valid when: Applies when FormulaEval support is transparent but no output-sensitive enumerator is used, so all M_N rows are syntactically scanned.
- parser-falsifier: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{trans}(\pi)+E_NN^{1+o(1)}`. Valid when: Requires the target-preserving parser simulation, fixed generator circuits, charged FormulaEval support, and explicit equality patches for residual rows.
- subthreshold-contradiction: `N^{\rho+o(1)}+\Gamma_{trans}(\pi)+E_NN^{1+o(1)}<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Valid when LB_N is stated in the same nonuniform SIZE model and the constructed circuit exactly computes the source carrier.

## Attempted Derivation

- Fix H_N^SAT, M_N=N^{q+o(1)}, L_N=(log N)^d, generator size N^{rho+o(1)}, and the source lower-bound statement LB_N(1+epsilon) in nonuniform SIZE.
- Define TransparentRowSupport_N as five checkable clauses: visible selector code, advice-free row enumeration or certified full scan, influence closure, same-theory occurrence expansion, and no hidden semantic advice.
- Run the existing Psys_bEF^- line induction for bit-explicit EF, SATeq links, bounded-SR_h verifier fields, and sparse-row equality patches; this yields Gamma_bEF(pi).
- For each transparent FormulaEval line, append either U_ell plus N^{1+o(1)}|K_ell| for enumerated rows or the full-scan bound N^{1+q+o(1)}; influence closure justifies replacing semantic use by explicit occurrence rows.
- Union row-index charges across FormulaEval lines and obtain Gamma_trans(pi)=Gamma_bEF(pi)+U_N+X_N without adding a new selector-specific theorem.
- Compose the generator circuit, charged transcript circuits, expanded FormulaEval rows, and E_N equality patches to build a SIZE circuit for H_N^SAT of size N^{rho+o(1)}+Gamma_trans(pi)+E_NN^{1+o(1)}.
- Contrapose the construction: if that size is below N^{1+epsilon-o(1)}, any accepted proof/certificate of LB_N(1+epsilon) has a valid small-circuit falsifier.
- For hidden FormulaEval, construct two oracle-label states agreeing on all charged rows but differing on a private row or unread enable bit; the same surface transcript cannot be a valid occurrence parser in both states.
- Therefore transparent FormulaEval is promoted as a theorem pair, while full semantic FormulaEval is blocked exactly at RealSATInfluenceRealizer_N.

Blocking gap: RealSATInfluenceRealizer_N remains open for genuine real-SAT semantic FormulaEval rules; the private-row countermodel proves that a relativizing or surface-occurrence parser cannot fill this gap.

## Falsifiers

- Subthreshold Gamma_trans(pi) is a valid falsifier for LB_N(1+epsilon) in the same SIZE model.
- Private-row hidden support is a falsifier for uncharged FormulaEval occurrence completion.
- Unread-enable-bit semantic access is a falsifier for selector extensionality and influence closure.
- For q<epsilon, certified full scan costs only N^{1+q+o(1)} and becomes a quantitative falsifier when other charges are subthreshold.
- Any tau/eta/SR_h overhead hidden in semantic advice invalidates the charged transcript theorem.
- Positive beta black-box substitution remains quarantined by the old q+beta c threshold-collapse falsifier.

## Learning

Cycle 109 upgrades the theorem pair from selector consolidation to a proof-audited interface: TransparentRowSupport_N is a finite checkable condition, Gamma_trans is derived by line induction, hidden semantic support has a concrete private-row/unread-enable-bit falsifier, and the only full Psys_sym escape is the nonrelativizing RealSATInfluenceRealizer_N. This is paper-level route certification, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The branch already has the transparent theorem shape; the remaining risk is silently treating hidden semantic FormulaEval as transparent support. A concrete private-row test distinguishes a valid charged parser from an invalid semantic oracle escape.
- Situation seed: Unread-enable-bit FormulaEval over H_N^SAT: the proof line evaluates SAT(G_N(x,r*)) only when a hidden bit b=1, while the visible selector enumerator lists K_idx not containing r*.
- Varied variable: h, the exponent in the number N^h of hidden enabled rows, with h=0 giving one private row and h<epsilon giving patchable sparse hidden support.
- Held-fixed controls: M_N=N^{q+o(1)} and L_N=(log N)^d, so the carrier stays beta-zero and target-preserving., Generator size remains N^{rho+o(1)} with rho<1+epsilon., The visible proof syntax, selector code, and charged RowSet are held identical in the two oracle-label states., The circuit model is the same nonuniform SIZE model used by LB_N(1+epsilon).
- Expected observation: For any h not charged into X_N, two transcripts agree on visible support while the carrier or FormulaEval line differs on an input x*. Thus hidden support cannot be soundly surfaced by a transparent parser; if h<epsilon it is also equality-patchable after realization.
- Transfer certificate needed: A RealSATInfluenceRealizer_N certificate: a nonrelativizing, advice-free map from real SAT semantic influence to charged row indices and occurrence neighborhoods, with U_N+N^{1+o(1)}|K_idx| recorded before the Gamma line induction.

## Next Experiment

Referee-check one projected-dDNNF FormulaEval rule against the five TransparentRowSupport_N clauses, compute its U_N and X_N charges, and verify that any projected hidden variable is either influence-closed or triggers the unread-enable-bit countermodel.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For Psys_sym restricted by TransparentRowSupport_N, every accepted proof pi of LB_N(1+epsilon) for H_N^SAT has an advice-free occurrence transcript of charge Gamma_trans(pi)=Gamma_bEF(pi)+U_N+X_N. If N^{rho+o(1)}+Gamma_trans(pi)<N^{1+epsilon-o(1)}, the parsed transcript gives a same-model upper-bound falsifier to the claimed lower bound. Consequently a valid proof must satisfy Gamma_trans(pi)>=N^{1+epsilon-o(1)}-N^{rho+o(1)} and |K_idx(pi)|+E_N^*(pi)>=N^{epsilon-o(1)} in the beta-zero regime.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with N=2^n, M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and polylogarithmic SAT instances.
- target object: LB_N(1+epsilon) is the formal statement C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)} against nonuniform Boolean circuits on the N-point truth-table domain.
- controlled interface: TransparentRowSupport_N is the FormulaEval interface requiring visible selector code, proof-visible row enumeration or full scan, selector extensionality, influence closure, same-theory occurrence expansion, and no hidden row advice.
- target-preserving condition: the parser must remain in the same nonuniform SIZE target model and produce an advice-free transcript whose row charges are sufficient for the existing beta-zero residual-patching upper-bound falsifier.

## Assumptions

- Model: Psys_sym^TRS consists of bit-explicit EF+SATeq+bounded-SR_h plus FormulaEval lines satisfying TransparentRowSupport_N.
- Length regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, bounded-SR_h width h=N^{eta+o(1)}, and selector code size at most N^{sigma+o(1)}.
- Uniformity/advice regime: the parser, enumerators, extensionality checks, and influence-closure checks are deterministic and receive no hidden nonuniform advice beyond pi and the public generator G_N.
- Same-theory condition: every charged FormulaEval row can be expanded into the same proof language as the bEF occurrence parser, rather than into an external semantic oracle call.
- Naturalness boundary: the theorem is a proof-system transfer obstruction; it becomes natural-proof pressure only if the transcript search induces a large constructive property of truth tables useful against the same SIZE class.

## Equations

- TRS-charge: `\Gamma_{\mathrm{trans}}(\pi)=\Gamma_{\mathrm{bEF}}(\pi)+U_N(\pi)+X_N(\pi)`. Valid when: Valid when every FormulaEval line satisfies visible enumeration, extensionality, influence closure, and same-theory expansion clauses.
- enumerator-bound: `U_N(\pi)\le N^{q+\tau+\sigma+o(1)}`. Valid when: Applies when all selector codes have size N^{sigma+o(1)} and the proof has N^{tau+o(1)} FormulaEval opportunities.
- row-expansion-bound: `X_N(\pi)=N\,E_N^*(\pi)\cdot N^{o(1)}`. Valid when: Requires that each FE-influential row is expanded over all N carrier inputs with only polylogarithmic local overhead.
- upper-bound-falsifier: `N^{\rho+o(1)}+\Gamma_{\mathrm{trans}}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Applies after the beta-zero residual-patching lemma preserves the same nonuniform SIZE target and no advice leakage.
- support-density: `\frac{|K_{idx}(\pi)|+E_N^*(\pi)}{M_N}\ge N^{\epsilon-q-o(1)}`. Valid when: Valid when the claimed source lower bound survives the transcript upper-bound falsifier and M_N=N^{q+o(1)}.

## Attempted Derivation

- Fix an accepted Psys_sym^TRS proof pi of LB_N(1+epsilon) for H_N^SAT in the regime N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}.
- Parse non-FormulaEval EF+SATeq+bounded-SR_h lines using the existing bit-explicit bEF parser, charging Gamma_bEF(pi) with row-index encodings, parent pointers, and local verifier overhead.
- For each FormulaEval line ell, read its visible selector code c_ell and either enumerate RowSet(ell) by brute force over M_N rows or invoke the declared full-scan charge; summing over proof lines gives U_N<=N^{q+tau+sigma+o(1)} in the visible-code case.
- Use selector extensionality to prove that the enumerated RowSet(ell) is the semantic support actually used by ell, not merely a syntactic overapproximation chosen by the parser.
- Use influence closure to add every row whose value can affect ell or any extension variable downstream of ell; call the resulting total E_N^*(pi).
- Replace each charged FormulaEval dependency by same-theory occurrence expansions across N carrier inputs, charging X_N=N E_N^* N^{o(1)}.
- Induct over proof lines: after each line, the transcript Q_i contains every source row and SAT occurrence needed to validate that line under any carrier agreeing on K_idx^+(Q_i). Thus the final transcript has charge Gamma_trans=Gamma_bEF+U_N+X_N.
- Invoke the beta-zero residual-patching lemma in the same nonuniform SIZE model: if N^{rho+o(1)}+Gamma_trans<N^{1+epsilon-o(1)}, then the purported LB_N proof is contradicted by a circuit upper-bound falsifier.
- Contrapose to get the support-pressure corollary |K_idx|+E_N^*>=N^{epsilon-o(1)}, and divide by M_N=N^{q+o(1)} for the q-density trichotomy.
- For omitted TRS clauses, instantiate the private-row/unread-enable-bit pair: two displayed transcripts are identical, but one semantic FE atom depends on row r_*; any surface parser gives the same Q while one carrier changes the FE truth or H parity, so uncharged semantic FormulaEval is invalid.

Blocking gap: The restricted TRS theorem is derivable modulo the previously named beta-zero residual-patching lemma. The full Psys_sym lift remains blocked exactly at RealSATInfluenceRealizer_N for real semantic SAT atoms.

## Falsifiers

- Private-row semantic FormulaEval: a hidden row r_* affects FE truth while no visible selector code names r_*, falsifying surface occurrence completion.
- Unread-enable-bit FormulaEval: an extension bit e toggles inclusion of a row without being read by the enumerator, so two valid-looking transcripts get identical Gamma but different semantic support.
- q<epsilon source-ceiling falsifier: C(H_N^SAT)<=N^{1+q+o(1)} blocks any claimed N^{1+epsilon-o(1)} lower bound before proof-system transfer is relevant.
- Opaque selector advice falsifier: a polynomial-size proof can name a short semantic handle whose extensional row set has no advice-free enumerator within U_N, invalidating TransparentRowSupport_N.

## Learning

Cycle 109 turns cycle 108's consolidation into a proof-delivery packet: TransparentRowSupport_N is a finite checkable interface, Gamma_trans is derived by a line induction with explicit U_N and X_N charges, hidden semantic FormulaEval has a concrete private-row/unread-enable-bit falsifier, and the only full-system gap is RealSATInfluenceRealizer_N. This is valid route-level certification, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The theorem boundary is no longer abstract; it turns on whether hidden semantic row influence can be charged. A concrete private-row experiment tests exactly the TRS visibility and influence-closure clauses.
- Situation seed: Construct H_N^SAT with M_N=N^{q+o(1)} rows and add one FormulaEval atom FE_e(a) whose displayed selector is empty but whose real semantics includes row r_* iff an unread extension bit e=1. Compare carriers with SAT(G_N(x,r_*)) flipped on one x and all displayed proof fields fixed.
- Varied variable: lambda=number of hidden FE-influential rows enabled by unread bits, from 0 to N^{epsilon-o(1)}.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and the same H_N^SAT target statement LB_N(1+epsilon)., The parser is deterministic, advice-free, and sees only proof-visible selector code and same-theory expansion certificates., The target class remains nonuniform Boolean SIZE; no oracle or many-one target change is allowed., All bEF and bounded-SR_h lines are kept bit-explicit and already charged by Gamma_bEF.
- Expected observation: For lambda=0 the transparent parser charge is unchanged and valid. For lambda>0 the semantic proof surface can remain fixed while the true influence set grows; unless RealSATInfluenceRealizer_N exposes those rows, Gamma_trans undercounts by N lambda and the hidden-support countermodel applies.
- Transfer certificate needed: A uniform RealSATInfluenceRealizer_N proving complete influence support for FE_e(a), or a same-theory proof that e and r_* are noninfluential; without it the thought experiment is a formal falsifier, not positive evidence.

## Next Experiment

Write the referee-check version of TRS109 with explicit line types: bEF, SATeq, bounded-SR_h, FormulaEval-axiom, FormulaEval-proof-line, and FormulaEval-extension-rule; verify each contributes exactly Gamma_bEF, U_N, or X_N, then test one real-SAT atom against the private-row countermodel.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

TransparentRowSupport_N gives a valid theorem pair for the paper packet: every bit-explicit Psys_sym proof pi of LB_N(1+epsilon) whose FormulaEval lines expose all influential rows extends the Psys_bEF parser ledger, and a subthreshold Gamma_trans(pi) is a same-model circuit upper-bound falsifier for LB_N(1+epsilon).

## Definitions

- source object: a Psys_sym proof pi of LB_N(1+epsilon) containing FormulaEval lines over H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)} and generator circuit overhead N^{rho+o(1)}.
- target object: a nonuniform SIZE_N circuit for H_N^SAT below N^{1+epsilon-o(1)} in the same input-length and SAT-generator model; this refutes only that finite lower-bound claim, not P != NP.
- controlled interface: TransparentRowSupport_N consists of visible selector code, advice-free RowSetEnumerator_N or full-scan charge, influence closure for every row whose SAT value can change a FormulaEval line, same-theory occurrence expansion, and no hidden support advice.
- target-preserving condition: every charged FormulaEval occurrence is expanded into the Psys_bEF transcript over the same generator G_N and row-index space, with parser cost U_N(pi) and row-expansion cost X_N(pi) included before exponent comparison.
- RowSetEnumerator_N(l) outputs K_l subseteq [M_N] plus witnesses that every SAT-influential row for line l is in K_l; if no such enumerator is provided, K_l is charged as the full scan [M_N].
- X_N(pi) is the sum over FormulaEval lines of |K_l| N E_N, where E_N=N^{o(1)} is the bit-explicit same-theory expansion overhead per row over all N input positions.

## Assumptions

- Circuit model: target upper bound is unrestricted nonuniform SIZE on the N-bit truth-table row H_N^SAT; no uniform language lower bound is inferred.
- Length and exponent regime: M_N=N^{q+o(1)}, |G_N(x,j)|=(log N)^{O(1)}, generator size is N^{rho+o(1)}, and E_N=N^{o(1)}.
- Uniformity and advice regime: selector code, enumerator code, and row-expansion witnesses are parsed from pi or generated uniformly from N; no nonuniform hard-row choice or hidden semantic selector is allowed.
- Same-theory condition: FormulaEval expansion uses the same SAT predicate and the same generator G_N that appear in H_N^SAT, so the circuit simulation preserves the target statement.
- Proof-system condition: all non-FormulaEval lines are already handled by the Gap98-SRhNormalForm/Psys_bEF^- line induction and contribute Gamma_bEF(pi).

## Equations

- Gamma transparent ledger: `\Gamma_{trans}(\pi)=\Gamma_{bEF}(\pi)+U_N(\pi)+X_N(\pi)`. Valid when: Valid when every FormulaEval line satisfies TransparentRowSupport_N and every non-FormulaEval rule is parsed by the existing Psys_bEF line induction.
- Row expansion charge: `X_N(\pi)=\sum_{\ell\in FE(\pi)} |K_\ell|\,N\,E_N`. Valid when: Applies when K_l is either advice-free enumerated support or the charged full row set for FormulaEval line l.
- Circuit simulation bound: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{trans}(\pi)`. Valid when: Requires the generator circuit for G_N and the parsed transcript circuit to be combined in the same nonuniform SIZE_N target model.
- Lower-bound falsifier inequality: `N^{\rho+o(1)}+\Gamma_{trans}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Valid when LB_N(1+epsilon) asserts unrestricted SIZE_N lower bound for exactly H_N^SAT at the same length N.

## Attempted Derivation

- Define TransparentRowSupport_N for a FormulaEval line L as the tuple (visible selector code, RowSetEnumerator_N or full scan, influence-closure certificate, same-theory occurrence expansion, no-hidden-advice certificate).
- For each transparent line L, run the enumerator to obtain K_L; if the enumerator is absent, set K_L=[M_N]. Charge U_L for discovery and |K_L| N E_N for expanding SAT(G_N(x,j)) across all N input positions and occurrence neighborhoods.
- Reuse the completed Gap98-SRhNormalForm/Psys_bEF^- line induction for every non-FormulaEval inference; add the transparent FormulaEval charge as an extension case, giving Gamma_trans(pi)=Gamma_bEF(pi)+U_N(pi)+X_N(pi).
- Compose the N^{rho+o(1)} generator circuit for G_N with the expanded transcript circuit. Because the expansion is same-theory and advice-free, the resulting nonuniform SIZE_N circuit computes H_N^SAT, not an auxiliary carrier.
- Compare N^{rho+o(1)}+Gamma_trans(pi) with the claimed lower-bound threshold N^{1+epsilon-o(1)}. If it is smaller, the proof pi cannot be a valid proof of LB_N(1+epsilon) in that same model.
- For hidden-support rules, choose r* in Inf(L)\K_L. Construct two surface occurrence completions agreeing on all parsed fields but differing on the SAT value or enable bit of r*. The transcript is identical but the FormulaEval value changes, so the parser theorem fails unless r* is realized and charged.
- Derive the support-density corollary by contrapositive: if rho and base costs are subthreshold and |K_idx(pi)|<N^{epsilon-o(1)}, then X_N(pi)<N^{1+epsilon-o(1)} and the Gamma_trans falsifier applies.

Blocking gap: The transparent theorem is derivable under its stated interface. Full Psys_sym promotion is blocked exactly at RealSATInfluenceRealizer_N: arbitrary semantic FormulaEval-SAT must either output advice-free real influence witnesses or be classified as a semantic-oracle/private-row countermodel case.

## Falsifiers

- Hidden support falsifier: a FormulaEval row influences SAT value but is absent from every charged K_l and no full scan is paid.
- Unread-enable-bit falsifier: the proof reads selector surface bits but an uncharged enable bit can activate a private row with different parity.
- Advice leakage falsifier: RowSetEnumerator_N uses nonuniform advice to choose support or hard rows, so the target upper-bound transfer is not valid.
- Projection fiber falsifier: a projected dDNNF selector pays only projected support T_N while hiding witness multiplicity W_N or missing certified deduplication.
- Membership-only selector falsifier: a succinct AC0 or DNNF membership test has no output-sensitive enumerator and must pay scan charge N^{1+q+o(1)} or become semantic oracle.
- Amortization falsifier: any claimed row expansion below N^{1-o(1)} must supply a same-theory circuit construction; otherwise the q-trichotomy is invalid.
- Barrier-specific falsifier: an occurrence-relativizing parser cannot distinguish two SAT-oracle completions that agree on all read occurrences but differ on a private row.

## Learning

Cycle 109 upgrades the selector-zoo consolidation into a theorem/countermodel pair. The positive side is a valid transparent-support parser-to-circuit simulation with Gamma_trans=Gamma_bEF+U_N+X_N. The negative side is not generic barrier folklore: hidden semantic support creates two occurrence completions agreeing on every read bit while changing a FormulaEval value, so the parser is invalid unless RealSATInfluenceRealizer_N supplies nonrelativizing, advice-free influence witnesses. The q-trichotomy follows as a corollary, not as a new route to P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design-now-as-falsifier-probe`
- Rationale: The branch needs a concrete target-preserving countermodel to decide whether semantic FormulaEval is charged transparency or an oracle escape, rather than another abstract selector restatement.
- Situation seed: Fix H_N^SAT(x)=xor_{j<=N^{q}} SAT(G_N(x,j)). Build one FormulaEval line with visible ROBDD selector K plus a hidden gate e_{r*} controlling a row r* not in K; the transcript never reads e_{r*} or the row formula at r*.
- Varied variable: hidden influence exponent beta, where the number of uncharged gated rows is |R_hidden|=N^{beta+o(1)}, ranging from beta=0 for one private row to beta=q for full hidden support.
- Held-fixed controls: The generator G_N, row universe [M_N], and target lower-bound claim LB_N(1+epsilon) are fixed., The Psys_bEF occurrence parser, same-theory SAT expansion cost N E_N, and nonuniform SIZE_N target model are fixed., No advice is allowed in row selection; any realizer must be parsed from the proof or uniformly generated from N., rho, q, epsilon, and E_N=N^{o(1)} are held fixed while only hidden support mass varies.
- Expected observation: At beta=0 a single private row already falsifies occurrence parsing if it is truly influential and uncharged. If a RealSATInfluenceRealizer lists the hidden rows at cost N^{beta+o(1)}, the positive theorem absorbs the cost and restores a valid Gamma_trans ledger.
- Transfer certificate needed: A formal completion lemma showing Q_pi(A)=Q_pi(A') while FormulaEval differs, or an advice-free RealSATInfluenceRealizer_N certificate enumerating R_hidden with same-theory witnesses and charge R_N+|R_hidden|N E_N.

## Next Experiment

Write the paper-ready theorem pair: Definition TransparentRowSupport_N; Theorem Gamma_trans parser-to-circuit falsifier; Theorem hidden-support private-row/unread-enable-bit countermodel; Corollary q-trichotomy; Open Problem RealSATInfluenceRealizer_N with exact cost R_N.
