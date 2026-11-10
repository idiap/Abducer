# cycle-0088

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For Psys=EF+SATeq+SR, where SAT atoms Y_u may use equality/equisatisfiability axioms and the one-variable self-reduction axiom Y_u <-> Y_{u|z=0} OR Y_{u|z=1}, the EqSAT quotient parser from cycle 87 is sound only for proofs whose SAT-semantic use is equality-generated. If an SR hyperedge is essential, an EqSAT-only or occurrence-only parser is invalid: there are quotient-label spoofs satisfying all EqSAT links but violating the SR axiom. The valid replacement object is a finite semantic-constraint residual code, and source lower-bound certificates must prove row-parity distance inside that constraint system.

## Definitions

- source object: a short EF+SATeq+SR proof pi_N of LB(H_N^SAT,S_N) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)} and L_N=(log N)^d.
- target object: a fork classification of pi_N as a dense functional label property, an occurrence/quotient transcript with residual row distance, or a genuinely SAT-semantic SR-constraint proof.
- controlled interface: proof verifier -> touched formula variables -> EqSAT quotient graph plus SR hyperedges -> induced row-parity residual code.
- target-preserving condition: the classification may affect the SAT lower-bound route only when q,rho<1+epsilon, beta=0, and the extraction does not add advice or assume the desired H_N lower bound.
- Psys syntax: EF over ordinary propositional variables plus extension variables Y_u intended to mean SAT(u), with SATeq axioms Y_u<->Y_v for named equisatisfiable transformations and SR axioms Y_u<->(Y_{u|z=0} OR Y_{u|z=1}).
- essential SR use: deleting or treating an SR axiom as an uninterpreted tautology destroys the derivation of the lower-bound certificate or its verifier acceptance condition.

## Assumptions

- Nonuniform circuit size is measured on the N-bit source input x; all constants hidden in o(1) are uniform in fixed epsilon,c,d,q,rho.
- The generator G_N has circuit size N^{rho+o(1)} and outputs M_N=N^{q+o(1)} formulas of length L_N=(log N)^d.
- The proof pi_N and its verifier have size at most N^{kappa+o(1)} and do not contain advice tables for SAT labels or residual bad rows.
- SATeq links are equality/equisatisfiability links only; they impose equivalence classes but no OR-type semantic relation.
- SR links are real SAT-semantic constraints and are not invariant under independent label flips of quotient classes.
- The lower-bound sentence is about the actual SAT interpretation; spoof labels are used only as parser falsifiers, not as alternate claims about real SAT.

## Equations

- beta0_xor_carrier: `H_N^{SAT}(x)=\oplus_{j=1}^{M_N} SAT(G_N(x,j)), M_N=N^{q+o(1)}, L_N=(log N)^d`. Valid when: Valid when the source object is the beta-zero batched SAT parity carrier with polylogarithmic target formulas and no positive target-query exponent.
- target_substitution_upper_bound: `C(H_N^{SAT}) <= N^{rho+o(1)}+M_N L_N^c = N^{max{rho,q}+o(1)}`. Valid when: Valid when SAT on L_N-bit formulas has nonuniform circuits of size L_N^c and the generator is advice-free with size N^{rho+o(1)}.
- SR_semantic_constraint: `Y_u = Y_{u|z=0} \vee Y_{u|z=1}`. Valid when: Valid when u is a Boolean formula containing variable z and Y_v denotes the satisfiability truth value of formula v under the real SAT interpretation.
- EqSAT_spoof_obstruction: `(Y_u,Y_{u|z=0},Y_{u|z=1})=(0,1,0) satisfies all equality links but violates SR(u,z)`. Valid when: Valid when the parser records only EqSAT quotient information and no additional OR-type self-reduction constraint for the touched formulas.
- constraint_row_distance: `Delta_K(pi)=min_{lambda models K_pi} |{x : \oplus_j lambda(G_N(x,j)) != H_N^{SAT}(x)}|`. Valid when: Valid when K_pi is the finite system of EqSAT and SR constraints touched by the proof and lambda ranges over Boolean assignments to its SAT atoms.

## Attempted Derivation

- Fix Psys=EF+SATeq+SR with SAT atoms Y_u and the source sentence LB(H_N^SAT,N^{1+epsilon-o(1)}).
- Reuse the stable beta-zero transfer: if SAT has L_N^c-size circuits, then H_N^SAT has size N^{max{rho,q}+o(1)}, so q,rho<1+epsilon is the valid target-preserving window.
- For proofs using only SATeq links, contract touched formulas to EqSAT components; the proof verifier is functional over quotient labels, so the cycle-87 quotient residual-code audit applies.
- Insert one essential SR axiom Y_u <-> Y_{u0} OR Y_{u1}. The assignment Y_u=0,Y_{u0}=1,Y_{u1}=0 respects every equality quotient but violates SR, so an EqSAT-only parser accepts a completion that is not SAT-semantic.
- Therefore full EF+SATeq+SR cannot be classified as occurrence/EqSAT-functional unless the parser also records the SR hyperedge or expands it into occurrence children.
- Once SR hyperedges are recorded, the residual object is no longer a linear quotient coset; it is a finite Boolean constraint code K_pi. The correct falsifier is low K_pi-constrained row-parity distance plus the row-patching bound.
- For compressed block-SR, any completion-sound occurrence parser for negative parent labels must expose all 2^t leaves or provide an equivalent semantic OR certificate, giving a tunable threshold 2^t=N^alpha.

Blocking gap: The derivation does not normalize arbitrary EF+SAT_U or arbitrary SAT-semantic reasoning to EqSAT+SR constraints. A stronger proof may use search-to-decision, Cook-Levin witness encodings, or formula minimization principles not represented by the finite SR hypergraph K_pi.

## Falsifiers

- falsifier: an EqSAT-only quotient parser for EF+SATeq+SR is invalid because the spoof labels (0,1,0) satisfy all equality links while violating a used self-reduction axiom.
- falsifier: any constrained predictor D_N with S_D+E_N N<N^{1+epsilon-o(1)} defeats a claimed source certificate for C(H_N^SAT)>N^{1+epsilon-o(1)}.
- falsifier: compressed block-SR with 2^t<N^{epsilon-o(1)} can leave omitted-leaf or omitted-row errors patchable below the source threshold.
- falsifier: reintroducing positive target-query exponent beta gives the older transfer cap q+beta c and cannot imply all-exponent SAT lower bounds.
- falsifier: nonuniform advice listing the residual bad rows or semantic children must be charged; otherwise the certificate leaks the target lower bound into the source object.

## Learning

Cycle 88 identifies the first concrete SAT-semantic escape from the EqSAT quotient parser: self-reduction OR constraints are not invariant under quotient-label spoofing. The valid paper move is not another magnification slogan but a trichotomy repair: equality-only proofs use quotient residual codes, occurrence expansions pay row-forcing cost, and SR proofs require a constrained residual-code audit. Low constrained row distance is a falsifier for source certificates; no main P != NP claim is made.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The abstract EqSAT quotient audit is now too weak for strong proof systems; a concrete self-reduction experiment separates occurrence exposure from genuinely SAT-semantic compression while preserving the beta-zero carrier.
- Situation seed: A padded beta-zero SAT parity carrier where each generated formula F_{x,j} has t distinguished dummy-or-choice variables and the proof system may invoke the compressed axiom SAT(F_{x,j}) <-> OR_{a in {0,1}^t} SAT(F_{x,j}|a).
- Varied variable: t=alpha log_2 N, equivalently the semantic OR fanout 2^t=N^alpha.
- Held-fixed controls: M_N=N^{q+o(1)} with q<1+epsilon., Generator size N^{rho+o(1)} with rho<1+epsilon., Target SAT query length L_N=(log N)^d, so beta=0 in the substitution theorem., No advice tables for SAT labels, bad rows, or omitted self-reduction leaves., Circuit model remains nonuniform SIZE on the N-bit carrier input.
- Expected observation: For alpha<epsilon, omitted semantic leaves or rows are equality-patchable and act as a falsifier for occurrence parsers. For alpha>=epsilon, explicit occurrence expansion pays the full-row scale, so any short proof must be using a real semantic OR certificate rather than the previous quotient parser.
- Transfer certificate needed: A formal parser theorem showing that block-SR either expands to 2^t occurrence leaves with charged overhead or is represented by a K_pi constraint whose constrained row-distance lower bound is proved without assuming the desired H_N lower bound.

## Next Experiment

Instantiate K_pi for local one-step SR only: bound |K_pi| by proof size, define its row-parity constraint-distance Delta_K, and test whether Delta_K can be reduced to a known SAT promise-hardness statement or whether it is target-equivalent to the desired H_N lower bound.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For the concrete proof system EF+SAT_U^subst, any target-preserving parser for beta-zero XOR lower-bound proofs must charge semantic row support, not syntactic SAT-atom occurrence count. The occurrence parser is refuted by a universal-selector SAT atom whose single proof occurrence ranges over all generator rows. Thus the full formula-semantic fork is sharpened to ExtensionRowRealizer: either accepted proofs have large semantic row closure, or sparse semantic closure gives a residual-circuit falsifier to the claimed source lower bound.

## Definitions

- source object: a short EF+SAT_U^subst proof pi of LB_N(s), where LB_N(s) asserts Ckt(H_N^SAT)>s for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)).
- target object: an advice-free extraction map pi -> Q_pi or K_pi that supports either a functional natural-property audit or a row-forcing/residual-patching theorem for H_N^SAT.
- controlled interface: semantic row support Supp_G(A) of a SAT atom A, closed under SAT congruence, Boolean-composition axioms, and extension substitution, written K_pi=SemCl_G(pi).
- target-preserving condition: the parser must preserve the beta-zero parameters M_N<=N^{q+o(1)}, L_N=(log N)^d, generator size N^{rho+o(1)}, and the threshold Ckt(H_N^SAT)>N^{1+epsilon-o(1)} without nonuniform row advice.
- EF+SAT_U^subst has extended Frege reasoning plus atoms SAT(F), Boolean SAT-composition axioms, congruence F equiv F' -> SAT(F)<->SAT(F'), and extension substitution of EF-defined formula terms into SAT atoms.
- Supp_G(A) is the set of rows j for which the formula denoted inside A can, under allowed extension substitutions and fixed x, determine or coincide with G_N(x,j) modulo the SAT congruence rules available to the proof.
- An occurrence parser Q_occ(pi) records only row labels syntactically displayed as G_N(x,j); it ignores universal row-selector atoms SAT(U_N(x,e)) and is therefore not invariant under EF substitution.

## Assumptions

- The generator G_N is uniform and beta-zero: row formulas have length L_N=polylog(N), row count M_N<=N^{q+o(1)}, and the circuit generating G_N has size N^{rho+o(1)}.
- The target circuit model is nonuniform Boolean SIZE(N^a) on the H_N input length, and residual patching may hardwire the exceptional row truth tables but no additional advice outside K_pi.
- The proof verifier and parser are uniform in N and pi; any nonuniform choice of semantic representatives must be counted as advice leakage and fails the target-preserving condition.
- Soundness is ordinary standard-SAT soundness unless DirectClusterSound or SemanticCompletion is separately assumed; ordinary local consistency is not used as a bridge.
- The universal-selector counterexample is a parser countermodel, not a short proof of LB_N(s); it invalidates an extraction method rather than deciding P versus NP.

## Equations

- beta0_xor_carrier: `H_N^{SAT}(x)=\bigoplus_{j=1}^{M_N} SAT(G_N(x,j)),\quad M_N\le N^{q+o(1)},\quad L_N=(\log N)^d.`. Valid when: Valid when G_N is the named uniform beta-zero generator and rows are the parity summands audited by the parser.
- semantic_row_closure: `K_\pi=SemCl_G(\pi)=cl_{subst,cong,comp}\left(\bigcup_{A\in SATAtoms(\pi)} Supp_G(A)\right).`. Valid when: Applies after the proof system's SAT rules and extension substitutions are fixed syntactically and the closure operations are part of the parser specification.
- residual_patching_bound: `Ckt(H_N^{SAT})\le S(D_N)+O(|K_\pi|\,N\,L_N^c)+N^{\rho+o(1)}.`. Valid when: Requires D_N to agree with H_N^{SAT} on all rows outside K_pi and permits nonuniform hardwiring only for the charged exceptional rows.
- forced_semantic_charge: `Ckt(H_N^{SAT})>N^{1+\epsilon-o(1)}\ \wedge\ S(D_N)\le N^{1+\epsilon-\eta}\ \Rightarrow\ |K_\pi|\ge N^{\epsilon-o(1)}.`. Valid when: Valid when residual patching is the only missing computation and eta is bounded away from zero relative to the o(1) losses.
- selector_support_explosion: `Supp_G(SAT(U_N(x,e)))=\{1,\ldots,M_N\},\quad |Supp_G(SAT(U_N(x,e)))|=N^{q+o(1)}.`. Valid when: Holds for a universal row-selector formula U_N whose selector variable e ranges over all row indices allowed by EF extension substitution.

## Attempted Derivation

- Fixed the concrete proof system EF+SAT_U^subst: EF plus SAT atoms, SAT Boolean-composition axioms, congruence for formula equivalence, and extension substitution into SAT atoms.
- Encoded the lower-bound sentence LB_N(s) as the usual circuit-size exclusion for H_N^SAT, preserving the beta-zero carrier parameters q,rho,L_N.
- Tried the occurrence parser Q_occ(pi): collect row indices j for syntactic atoms SAT(G_N(x,j)) appearing in pi and close under displayed formula-DAG equality.
- The induction over pure EF steps is harmless; displayed equality only changes representatives inside the same equality fiber.
- The induction fails at the substitution/congruence rule: a single atom SAT(U_N(x,e)) with an EF extension variable e denoting the row selector has semantic support all M_N rows while Q_occ charges one syntactic occurrence.
- Repaired the invariant by defining K_pi=SemCl_G(pi), the closure of semantic supports under substitution, congruence, and SAT composition.
- Combined K_pi with the sparse residual inequality: if K_pi is subthreshold and a decider D_N handles the uncharged rows, then H_N^SAT has a circuit of size S(D_N)+O(|K_pi|N L_N^c)+N^{rho+o(1)}.
- Derived the conditional forced-charge conclusion |K_pi|>=N^{epsilon-o(1)} under the claimed source lower bound and subthreshold residual decider.
- Ran the naturalness audit: if the same accepted cluster has logarithmic target projection and DirectClusterSound, it induces a valid large constructive useful property; without DCS, odd-charge Tseitin remains a falsifier.

Blocking gap: ExtensionRowRealizer for unrestricted EF+SAT_U^subst: given an arbitrary SAT atom built using extension substitution, compute or certify its generator-row support without row advice and without solving a hard formula-equivalence/SAT-semantic search problem.

## Falsifiers

- Universal-selector atom falsifier: SAT(U_N(x,e)) has one syntactic occurrence but semantic support M_N, so occurrence row count is not a valid parser invariant.
- Shared-DAG equality-fiber falsifier: many generator rows can share a formula-DAG representative, making private occurrence labels invalid outside EF+SAT_U^{occ}.
- SAT-composition falsifier: a composition axiom can relate row formulas through a nonlocal formula term without displaying each row separately.
- Odd-charge Tseitin falsifier: ordinary local consistency can accept all projected views while no global satisfying object exists, so it cannot replace DirectClusterSound.
- Sparse semantic-closure falsifier: if K_pi is small and the route claims a source lower bound above N^{1+epsilon}, residual patching gives an explicit circuit upper bound against the claim.
- Natural-property PRF falsifier: a logarithmic-projection, constructive, useful functional certificate is under standard PRF pressure for the exact SIZE class it separates.

## Learning

Cycle 88 identifies the exact strong-system rule that defeats the occurrence parser: extension substitution into SAT atoms can compress all generator rows into one syntactic atom. The valid invariant for full EF+SAT_U^subst is semantic row support, and the next theorem is no longer a vague formula-semantic gap but the ExtensionRowRealizer dichotomy: certify large support or obtain a sparse-residual falsifier. This is route-level proof-boundary progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and quantitative threshold test for the full EF+SAT_U^subst parser.`
- Rationale: The branch has already isolated generic semantic closure; the missing proof obligation is whether extension substitution secretly charges many rows. A selector-leakage experiment directly measures the semantic-support expansion while preserving the beta-zero target.
- Situation seed: Padded universal-selector SAT parity: define G_N(x,j)=U_N(a_N(x),j) with M_N=N^{q+o(1)} rows and let EF+SAT_U^subst proofs use atoms SAT(U_N(a_N(x),e)) where e is an extension variable for the row selector.
- Varied variable: lambda, the number of row-index bits fixed or certified inside the SAT atom, so the semantic support is approximately M_N/2^lambda.
- Held-fixed controls: H_N^SAT remains the xor over the same M_N SAT rows., Formula length stays L_N=(log N)^d and generator overhead stays N^{rho+o(1)}., The source threshold remains Ckt(H_N^SAT)>N^{1+epsilon-o(1)}., The parser is uniform and advice-free, and residual patching may hardwire only charged rows., The target circuit class is the same nonuniform SIZE class used in the beta-zero transfer.
- Expected observation: Syntactic projection width stays O(1) while semantic support moves from N^{q+o(1)} at lambda=0 to one row at lambda=log M_N. The valid row-forcing threshold occurs near lambda=(q-epsilon)log N; below it, an occurrence parser is falsified by hidden full-row charge, and above it sparse residual patching becomes dangerous.
- Transfer certificate needed: An ExtensionRowRealizer that, for each SAT atom with selector leakage lambda, either outputs a certified support set of size about M_N/2^lambda or proves that the atom must be charged as large semantic support before any extraction theorem affects proof obligations.

## Next Experiment

Formalize the selector-leakage family U_N and prove the support formula |Supp_G|=M_N/2^lambda for balanced generators; then attempt ExtensionRowRealizer for the fragment where SAT atoms are U_N with affine selector restrictions before returning to arbitrary EF+SAT_U^subst atoms.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For the beta-zero SAT parity carrier, any Cook-Reckhow-checkable extensionality step is either witnessed by a parseable certificate with adaptive-cover exponent alpha_ext, in which case the existing low-cover patch upper bound is valid, or it is an unwitnessed SAT-semantic oracle step and must be quarantined as a model change rather than a proof-system certificate carrier.

## Definitions

- source object: a short proof pi in P_CR-wExt for a lower-bound sentence about H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), where extensionality steps must be accepted by a polynomial-time verifier reading an explicit witness w.
- target object: an unrestricted circuit upper-bound falsifier for H_N^SAT at size N^{max{rho,q+alpha_ext,max(f,r)+1}+o(1)}, or a quarantine certificate that the proof formalism uses an unparsed semantic oracle.
- controlled interface: parse pi into occurrence transcripts, formula-equality/extensionality witness graphs, forced rows, residual rows, and adaptive covers for the label-opening mechanism.
- target-preserving condition: the parser, quotient graph, and row generator are uniform and advice-free, query count M_N<=N^{q+o(1)}, generator size N^{rho+o(1)}, and the extracted circuit computes the same H_N^SAT outside explicitly patched rows.

## Assumptions

- Model: unrestricted Boolean circuits measure C_ckt(.) as a function of truth-table length parameter N; no nonuniform hard-row selector is allowed except hardwiring the final falsifying certificate for the negative direction.
- Proof system: P_CR-wExt is EF plus SAT_U atoms, occurrence-local SAT rules, definitional extension variables, and extensionality rules whose side certificates are checked in polynomial time by the proof checker.
- Quantitative regime: M_N<=N^{q+o(1)}, the generator family G_N has circuit size N^{rho+o(1)}, query length is polylogarithmic in N, and the proof/certificate carrier has adaptive-cover exponent alpha_ext.
- Row accounting: ForcedRows(pi) has size at most N^{f+o(1)}, residual disagreement set R_N has size at most N^{r+o(1)}, and each patched row costs O(N) gates by truth-table hardwiring.
- Soundness condition: row-parity binding is evaluated after quotienting formula occurrences by witnessed definitional identity and witnessed SAT-extensionality; local soundness alone is not sufficient.
- Non-claim boundary: the lemma is a route-level falsifier or quarantine theorem for this carrier interface, not a proof of P != NP.

## Equations

- beta_zero_carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\quad M_N\le N^{q+o(1)},\quad |G_N|\le N^{\rho+o(1)}`. Valid when: Valid when the beta-zero SAT parity carrier and its generator family are fixed uniformly and advice-free.
- adaptive_ext_cover: `\alpha_{ext}=\max\{\tau,\max_\ell(a_\ell+\mu_\ell),\max_\ell \omega_\ell\}`. Valid when: Valid when extensionality witnesses are represented by an adaptive transcript with declared summary, multiplicity, and opener exponents.
- low_cover_patch_bound: `C_{ckt}(H_N^{SAT})\le N^{\max\{\rho,q+\alpha_{ext},\max(f,r)+1\}+o(1)}`. Valid when: Applies after the quotient parser preserves SAT row parity and all unparsed forced or residual rows are explicitly patched.
- threshold_falsifier: `\max\{\rho,q+\alpha_{ext},\max(f,r)+1\}<1+\epsilon\;\Rightarrow\; C_{ckt}(H_N^{SAT})\not> N^{1+\epsilon-o(1)}`. Valid when: Requires the claimed source lower bound to be for the same H_N carrier and the same unrestricted circuit model.

## Attempted Derivation

- Fix P_CR-wExt: EF syntax plus SAT_U atoms; each extensionality line carries a witness w, and the polynomial-time checker either verifies w or the line is not Cook-Reckhow-checkable.
- Extract from pi an occurrence transcript Q_pi and a quotient graph E_pi whose edges are definitional identity, witnessed formula equivalence, or witnessed equisatisfiability transformations accepted by the checker.
- Measure E_pi by the adaptive-cover exponent alpha_ext=max{tau,max_l(a_l+mu_l),max_l omega_l}; this gives a circuit opener for all nonpatched SAT labels at cost N^{alpha_ext+o(1)} per query block.
- Apply the private-row spoof lemma: if a row parity is not constant over LocSat(Q_pi/E_pi), then two local completions preserve the proof transcript and flip that row, contradicting row-parity binding; therefore all such rows are charged to ForcedRows.
- Construct D_N: generate all M_N SAT queries using G_N, open their quotient labels using the cover, xor them for nonpatched rows, and hardwire rows in F_pi union R_N. The size is bounded by N^{max{rho,q+alpha_ext,max(f,r)+1}+o(1)}.
- If this exponent is below 1+epsilon, the claimed source lower bound C(H_N^SAT)>N^{1+epsilon-o(1)} is falsified for this carrier. If an extensionality line has no witness, checking its side condition would decide SAT status by comparison with top/bot, so the formalism is a semantic-oracle model.

Blocking gap: The derivation is conditional on extracting alpha_ext for the chosen concrete proof system. For full EF+SAT_U with arbitrary polynomially checkable semantic certificates, we still need either a low-cover extraction theorem or an explicit high-cover witness family.

## Falsifiers

- Low-cover witnessed extensionality with max{rho,q+alpha_ext,max(f,r)+1}<1+epsilon is a valid falsifier for any claimed N^{1+epsilon-o(1)} lower bound certified by that carrier.
- An unwitnessed ExtSat_sem rule is a falsifier for the occurrence-parser proof claim but simultaneously quarantines the system as semantic-oracle or non-Cook-Reckhow.
- A nonuniform table selecting hard rows, formula-equivalence pairs, or canonical quotient representatives invalidates the target-preserving advice-free transfer.
- A proof that only establishes local consistency of SAT labels, without row-parity binding over LocSat(Q_pi/E_pi), is rejected by the private-row spoof falsifier.
- If forced rows or residual rows have exponent at least epsilon above the patch threshold, the upper-bound contradiction disappears and the carrier is not refuted by this packet.

## Learning

Cycle 88 sharpens the formula-semantic fork: witnessed extensionality is harmless only after paying a measurable adaptive-cover exponent, while unwitnessed SAT-extensionality is a named semantic-oracle model change rather than a valid advice-free carrier. The route contribution is a Cook-Reckhow guard plus a finite low-cover falsifier, not progress on the main P != NP conjecture.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the formula-semantic extraction fork.`
- Rationale: The branch needs to separate witnessed extensionality, which should pay an adaptive-cover exponent, from unwitnessed semantic equality, which changes the proof model and blocks occurrence parsing.
- Situation seed: A padded SAT-query family where each G_N(x,j) is replaced in the proof by a padded equisatisfiable formula Pad_b(G_N(x,j)); the proof system may justify each replacement either by an explicit padding witness or by an unwitnessed ExtSat_sem oracle line.
- Varied variable: alpha_ext, the adaptive-cover exponent of the padding/equisatisfiability witnesses, with the limiting case alpha_ext=oracle for unwitnessed semantic extensionality.
- Held-fixed controls: The beta-zero carrier H_N^SAT, query exponent q, and generator overhead rho are unchanged., The target circuit model remains unrestricted nonuniform circuits for the same truth-table family H_N^SAT., No hard-row selector advice or formula-equivalence advice is permitted in the Cook-Reckhow case., Residual and forced-row exponents r and f are recorded separately and patched only by explicit truth-table hardwiring.
- Expected observation: When alpha_ext is below 1+epsilon-q and forced/residual exponents are also subthreshold, the certificate yields a small circuit for H_N^SAT; when the witness is removed, the proof checker must decide SAT-status equality and the experiment exposes the semantic-oracle escape.
- Transfer certificate needed: A formal parser that maps every accepted extensionality line to a quotient edge plus adaptive cover, or a proof that the line uses an uncheckable SAT-semantic side condition outside standard proof complexity.

## Next Experiment

Instantiate Psys as EF+SAT_U with polynomial-size Frege certificates for equisatisfiability transformations; compute alpha_ext for definitional extension, Tseitin introduction, variable renaming, and padding, then test whether any rule remains unparsed without becoming ExtSat_sem.
