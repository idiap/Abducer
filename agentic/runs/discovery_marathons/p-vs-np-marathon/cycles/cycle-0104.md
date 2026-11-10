# cycle-0104

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Restricted theorem packet: in Psys_bEF^- every bit-explicit bounded-SR_h line has a row-indexed occurrence-neighborhood normal form whose charged contribution is B_SR(pi)=O(|K_SR(pi)|2^{h_N}W_N polylog N). Hence, for |K_SR(pi)|<=M_N=N^{q+o(1)}, 2^{h_N}=N^{eta+o(1)}, and W_N=N^{tau+o(1)}, SR_h contributes at most N^{q+eta+tau+o(1)} to Gamma_bEF(pi), and the line induction gives the restricted transcript falsifier for LB_N(epsilon).

## Definitions

- source object: beta-zero SAT-parity carrier H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, formula length L_N=(log N)^d, and source lower-bound sentence LB_N(epsilon): C(H_N)>N^{1+epsilon-o(1)}.
- target object: a Psys_bEF^- parser/falsifier theorem producing an occurrence transcript Gamma_bEF(pi) and a circuit upper bound refuting LB_N(epsilon) when the transcript is subthreshold.
- controlled interface: bit-explicit EF+SATeq+bounded-SR_h proof lines are mapped to row-indexed occurrence records, SATeq links, EF dependency supports, SR leaf-neighborhood lists, and sparse residual row patches.
- target-preserving condition: the parser is advice-free, nonuniform only after fixing N, beta=0 SAT queries have polylogarithmic length, and no symbolic FormulaEval-SAT line is used unless RowSet enumeration is charged.

## Assumptions

- Circuit model is nonuniform Boolean circuits over fan-in two AND/OR/NOT with gate-size measure; all constants may depend on fixed epsilon,d,q,rho,eta,tau but not on the input x.
- Psys_bEF^- consists only of bit-explicit EF definitions with acyclic declared support, SATeq links with explicit occurrence bijections, and bounded-SR_h rules with explicit decision variables and leaf occurrence neighborhoods.
- An SR_h record has fields tag, line id, parent pointers, row index j, root formula id, depth h_N, branch word alpha in {0,1}^{h_N}, decision-position vector, leaf formula pointer, neighborhood list Delta_{j,alpha}, and leaf value bit.
- The local SR verifier checks parent pointers, row index encoding, occurrence-map consistency under the h_N restrictions, and the OR/AND self-reduction composition using only the listed Delta_{j,alpha} bits.
- The transcript parser may charge EF dependencies S_dep(pi), SATeq links S_link(pi), SR records B_SR(pi), charged FormulaEval rows if present, and E_N residual rows patched by equality gates of cost O(E_N N).
- Uniformity/advice regime: the parser is a deterministic poly(|pi|,N)-time meta-algorithm; the resulting circuit is nonuniform for each N but receives no hidden row advice beyond the parsed transcript.
- Non-claim boundary: this lemma is a restricted proof-system upper-bound falsifier, not a proof of P != NP and not a source lower bound for H_N.

## Equations

- carrier: `H_N^{\mathrm{SAT}}(x)=\bigoplus_{j=1}^{M_N} \mathrm{SAT}(G_N(x,j)),\qquad M_N=N^{q+o(1)}`. Valid when: Valid when G_N uniformly generates the row formulas at the fixed valid length N and the target-query length is polylogarithmic.
- SR_branch_and_neighborhood_parameters: `A_N=2^{h_N}=N^{\eta+o(1)},\qquad W_N=\max_{j,\alpha}|\Delta_{j,\alpha}|=N^{\tau+o(1)}`. Valid when: Applies when the bounded self-reduction depth and every touched occurrence-neighborhood list are explicitly encoded in the proof line.
- SR_charge: `B_{\mathrm{SR}}(\pi)\le c\,|K_{\mathrm{SR}}(\pi)|A_NW_N\operatorname{polylog}N\le N^{q+\eta+\tau+o(1)}`. Valid when: Requires the SR parser to enumerate all charged rows and all branch leaves without semantic advice or hidden formula evaluation.
- transcript_budget: `\Gamma_{\mathrm{bEF}}(\pi)=S_{\mathrm{dep}}(\pi)+S_{\mathrm{link}}(\pi)+B_{\mathrm{SR}}(\pi)+E_NN`. Valid when: Valid when EF dependencies, SATeq links, bounded-SR records, and sparse residual patches are the only charged proof mechanisms.
- restricted_falsifier_bound: `C(H_N^{\mathrm{SAT}})\le N^{\rho+o(1)}+\Gamma_{\mathrm{bEF}}(\pi)`. Valid when: Applies after the parsed transcript supplies charged row computations and residual rows are corrected by equality patches.
- LB_refutation_threshold: `N^{\rho+o(1)}+\Gamma_{\mathrm{bEF}}(\pi)<N^{1+\epsilon-o(1)}\ \Longrightarrow\ \neg LB_N(\epsilon)`. Valid when: Valid when LB_N(epsilon) is the exact source lower-bound claim C(H_N)>N^{1+epsilon-o(1)} in the same circuit model.

## Attempted Derivation

- Fix valid lengths N and the carrier H_N^SAT with beta=0 polylogarithmic SAT instances. Define Psys_bEF^- as bit-explicit EF+SATeq+bounded-SR_h, excluding symbolic FormulaEval except charged IU_FEExtract lines.
- For each EF extension line, traverse the acyclic definition DAG and append its declared input-bit support to S_dep(pi). Parent pointers are O(log |pi|); support entries are row-indexed occurrence coordinates.
- For each SATeq link, record the pair of formula ids, row index, occurrence bijection, and local equality proof. Charge S_link(pi) by the number of linked occurrence coordinates, not by semantic formula identity.
- For each SR_h line, write records (tag,i,parent0,parent1,j,u,h,alpha,p_1,...,p_h,leaf_id,Delta_{j,alpha},y_alpha). The local verifier checks that Delta_{j,alpha} is exactly the touched occurrence-neighborhood induced by restricting formula u along branch alpha.
- Count one SR leaf record per row and branch. With |K_SR| rows, A_N=2^{h_N}, and W_N maximal listed neighborhood size, the charged bit work is O(|K_SR|A_NW_N polylog N), giving N^{q+eta+tau+o(1)} in the global row regime.
- Run line induction: every proof line has a transcript T_i whose exposed-row semantics matches the line under all row-label assignments agreeing on T_i. EF lines union transcripts, SATeq lines add links, SR_h lines add exactly their leaf neighborhoods, and residual disagreement rows are isolated into E_N.
- Combine S_dep, S_link, B_SR, and E_NN with the generator circuit N^{rho+o(1)} to obtain C(H_N)<=N^{rho+o(1)}+Gamma_bEF(pi). If this is below N^{1+epsilon-o(1)}, the source lower-bound statement LB_N(epsilon) is false in the same circuit model.
- Integrate the already validated interval-union FE_Extract_N fragment by adding B_FE^IU=N|RowSet|+lower-order descriptor charge to Gamma. Do not integrate semantic FormulaEval without FE_Extract_N; the hidden-row flip countermodel blocks occurrence completion.

Blocking gap: Full Psys_sym remains blocked exactly at FE_Extract_N for semantic FormulaEval selectors and at arbitrary extension variables whose row supports are not bit-explicit. The restricted Psys_bEF^- plus interval-union FormulaEval packet is valid; the full semantic proof-system parser is not proved.

## Falsifiers

- Subthreshold transcript falsifier: N^{rho+o(1)}+S_dep+S_link+B_SR+B_FE+E_NN<N^{1+epsilon-o(1)} gives an explicit circuit upper bound for H_N and refutes LB_N(epsilon).
- Private-row falsifier: a semantic FormulaEval line with an unenumerated selected row permits two row-label worlds with identical parsed transcript but opposite carrier parity.
- Threshold-collapse falsifier: if q+eta+tau>=1+epsilon, bounded-SR_h expansion alone reaches the source lower-bound scale and the proof-system audit no longer magnifies a barely-superlinear claim.
- Nonuniform leakage falsifier: any EF extension variable whose support is not bit-explicit can encode row advice outside Gamma_bEF and invalidates the parser theorem.
- Model-mismatch falsifier: an occurrence-local parser theorem cannot be advertised for real SAT-semantic Psys_sym unless the proof object is shown nonrelativizing and FE_Extract_N-valid.

## Learning

Cycle 104 pins the bounded-SR_h normal form to concrete verifier fields rather than an exponent slogan. The restricted Psys_bEF^- plus interval-union FormulaEval theorem packet is now valid as a paper-level parser/falsifier result, while full semantic FormulaEval remains quarantined at FE_Extract_N by a private-row countermodel.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The branch has a restricted parser theorem; the remaining risk is treating semantic FormulaEval intuition as occurrence support. A concrete private-row experiment tests exactly that interface without broadening to new carriers.
- Situation seed: Take H_N^SAT(x)=xor_{j<=N^{q}} SAT(G_N(x,j)) with q<1+epsilon and add one Psys_sym FormulaEval-SAT line whose selector is an interval-union descriptor plus a single hidden private row r controlled by an unread enable bit e.
- Varied variable: selector explicitness kappa: kappa=0 means transparent interval-union enumeration, kappa=1 means one hidden private row, and intermediate kappa allows N^{kappa+o(1)} hidden selected rows.
- Held-fixed controls: beta=0 polylogarithmic SAT formula length and the same generator G_N of size N^{rho+o(1)}, same nonuniform circuit size model and same LB_N(epsilon) source statement, same bit-explicit EF, SATeq, and bounded-SR_h parser charges, no advice to the parser beyond the proof bit string and fixed length N
- Expected observation: At kappa=0 the FE_Extract_N charge is N|RowSet| and the transcript is valid. At kappa>0 a hidden-row label flip leaves all parsed occurrences fixed while changing the parity on selected rows, so the semantic line is outside the occurrence parser unless it pays expansion or supplies a nonrelativizing extraction certificate.
- Transfer certificate needed: A uniform RowSetEnumerator_N with charge N|RowSet| for transparent selectors, or a real-SAT nonrelativizing FE_Extract_N theorem proving that every semantically used row is forced into K_idx(pi) with explicit threshold loss.

## Next Experiment

Instantiate RowSetEnumerator_N for one richer transparent selector class beyond interval-unions, preferably sorted AC0 threshold-free selectors with explicit scan charge, and decide whether it expands at N|RowSet|, collapses to an N^q scan bound, or admits a private-row countermodel.

# Barrier-Aware Lower-Bound Route: FormulaEval selector influence audit

## Candidate Lemma

Restricted FormulaEval-selector dichotomy: in Psys_sym^{FEsel}, a proof-visible selector DAG that contains FormulaEval-SAT leaves admits a target-preserving RowSetEnumerator only after every row on which an unexpanded FormulaEval leaf can affect selection is row-expanded and charged; otherwise an unread-enable-bit semantic-oracle falsifier gives two carriers with the same parsed surface and different selected row sets.

## Definitions

- source object: an accepted Psys_sym^{FEsel} proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with N=2^n, M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)}, and selector atoms S_a(j) of visible size N^{sigma+o(1)}.
- target object: a no-advice occurrence/row transcript Q_pi whose induced circuit upper bound for H_N^SAT is measured against SIZE_N(N^{1+epsilon-o(1)}).
- controlled interface: FormulaEval-SAT leaves inside row selectors are treated either as row-expanded proof lines/extension rules with explicit formula bits and charge, or as semantic oracle leaves with no occurrence support.
- target-preserving condition: every FE-influential row is included in the charged semantic support before RowSet(a) is used in Gamma_sym,FE(pi); otherwise surface occurrence completion is not valid.
- FE-influential row: a row j such that flipping at least one unexpanded FormulaEval-SAT leaf in the Boolean selector computation can change S_a(j).
- E_N^*: the number of FormulaEval row evaluations charged after adding all FE-influential unexpanded rows to the expansion account.

## Assumptions

- Model: finite-N nonuniform Boolean circuits and a bit-explicit proof parser; the result is a proof-system transfer audit, not a P != NP proof.
- Regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, bounded-SR_h parameter h=N^{eta+o(1)}, selector size N^{sigma+o(1)}, and q,rho,tau,eta,sigma are fixed exponents up to o(1).
- Uniformity/advice: the parser is deterministic, advice-free, and may inspect only proof-visible bits, charged row expansions, and the public selector code.
- Semantic status: for pure Boolean/index selector gates the parser may brute-force all j<=M_N; for FormulaEval-SAT leaves it must either expand the row formula or explicitly classify the leaf as a semantic oracle.
- Real-SAT cutoff: the falsifier transfers from semantic-oracle FormulaEval to real SAT only under a RealSATEnableBitRealizer_N giving satisfiable/unsatisfiable completions with identical parsed bits.
- Barrier status: if the charged transcript induces a polynomial-density constructive useful property, natural-proof pressure applies; the uncharged semantic selector is relativizing/oracle-like and not a valid barrier escape.

## Equations

- row_set_semantics: `\mathrm{RowSet}_a=\{j\le M_N:S_a(j)=1\}`. Valid when: Valid when S_a is a proof-visible selector DAG whose nonsemantic gates have fixed finite-N Boolean semantics.
- fe_influence_set: `I_{FE}(a)=\{j\le M_N:\exists g\in FE(S_a)\text{ such that flipping }g(j)\text{ changes }S_a(j)\}`. Valid when: Valid when FormulaEval leaves are abstracted as Boolean inputs before real-SAT realizability is invoked.
- forced_fe_charge: `E_N^{*}=E_N+|I_{FE}(\pi)\setminus K_{FE}(\pi)|`. Valid when: Applies after the parser has identified FE-influential rows and before claiming a target-preserving transcript.
- charged_gamma: `\Gamma_{sym,FE}(\pi)=S_{dep}+S_{link}+N^{q+\eta+\tau+o(1)}+N^{q+\tau+\sigma+o(1)}+N E_N^{*}`. Valid when: Requires bit-explicit bEF parsing, proof-visible selector enumeration, and all FE-influential semantic rows charged.
- upper_bound_falsifier: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{sym,FE}(\pi)`. Valid when: Applies after the reduction preserves generator overhead, row support, and no-advice transcript uniformity.

## Attempted Derivation

- Define Psys_sym^{FEsel} as bit-explicit EF+SATeq+bounded-SR_h plus proof-visible selector DAGs; pure Boolean/index gates are syntactic, FormulaEval-SAT leaves are typed as expanded proof lines, extension rules, or semantic oracle calls.
- Run the existing bEF parser on EF/SATeq/bounded-SR_h lines, retaining S_dep+S_link+N^{q+eta+tau+o(1)} and not upgrading occurrence-local facts to semantic FormulaEval facts.
- For each selector atom S_a, brute-force j<=M_N over the visible selector code. Pure gates cost N^{q+tau+sigma+o(1)} across N^{tau+o(1)} proof atoms.
- Treat each FormulaEval leaf as a Boolean input and compute the row influence set I_FE(a). If a row is influential and not already expanded, add it to E_N^*; this yields the charged Gamma_sym,FE expression.
- If an influential FormulaEval row is not charged, construct two semantic completions differing only in that leaf. They have the same parsed proof surface but different RowSet(a), so any deterministic no-advice RowSetEnumerator is invalid.
- Under RealSATEnableBitRealizer_N, replace the semantic flip by a finite SAT encoding flip using an unread enable bit. This gives a real-SAT falsifier for uncharged FormulaEval selectors in the chosen encoding fragment.
- With all influence charged, the transcript plus generator circuit of size N^{rho+o(1)} simulates H_N^SAT within N^{rho+o(1)}+Gamma_sym,FE(pi). If this is below N^{1+epsilon-o(1)}, the accepted LB_N(1+epsilon) sentence is false.
- Live pvsnp_inference_quality packet: source_statement=accepted Psys_sym^{FEsel} proof of LB_N(1+epsilon) for beta-zero H_N^SAT; target_statement=charged RowSetEnumerator or semantic FormulaEval falsifier; model_context=nonuniform SIZE, bit-explicit proof model, simulation/extraction not many-one reduction; quantifier_context=N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, h=N^{eta+o(1)}, selector size N^{sigma+o(1)}, no parser advice; derivation_status=restricted semantic-oracle theorem proved, real-SAT lift blocked at RealSATEnableBitRealizer_N and FormulaEvalGateInfluenceExtractor_N; reviewer_findings=valid only with charged FE influence, naturalness pressure only after a dense constructive useful property is induced.

Blocking gap: Unrestricted Psys_sym still needs FormulaEvalGateInfluenceExtractor_N for arbitrary semantic selector syntax and RealSATEnableBitRealizer_N for moving the oracle falsifier into ordinary SAT without hidden semantic advice.

## Falsifiers

- Uncharged single-row selector S(j)=1 iff j=j* and FormulaEval-SAT(F_{j*})=1 is a falsifier to surface occurrence completion: the displayed proof atom is fixed while RowSet flips.
- Unread-enable-bit formulas F^0,F^1 with identical parsed bits and opposite SAT values are a real-SAT falsifier whenever the proof parser omits the enable bit.
- If q<epsilon and K_FE^+(pi)<N^{epsilon-o(1)}, the parsed transcript plus generator gives a circuit upper bound below the claimed LB_N threshold, so the source lower-bound statement is invalid.
- A selector whose FormulaEval leaf is a semantic oracle but is counted as proof-visible AC0 code is not a valid transparent selector; it leaks nonuniform row advice.

## Learning

Cycle 104 sharpens the FormulaEval boundary: proof-visible selector syntax is not enough when FormulaEval-SAT leaves influence row choice. The valid route either charges all FE-influential rows in E_N^* and preserves the Gamma transfer, or it is refuted by a semantic-oracle/unread-enable-bit falsifier. This is route-level proof-system certification, not progress on P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for FormulaEvalGateInfluenceExtractor_N and RealSATEnableBitRealizer_N.`
- Rationale: The branch needs a concrete target-preserving test because visible selector code was already handled; the remaining uncertainty is whether semantic FormulaEval leaves can hide row selection without paying N E_N expansion.
- Situation seed: Beta-zero carrier H_N^SAT with M_N=N^{q+o(1)} rows and a selector S_u(j)=A(j) OR (j in T_u and FormulaEval-SAT(F_{u,j})=1), where A is an interval-union selector and T_u is a sparse set of FE-contaminated rows with unread enable-bit formulas.
- Varied variable: alpha where |T_u|=N^{alpha+o(1)} is the number of FE-influential unread rows.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, and the same generator overhead N^{rho+o(1)}., The proof parser is deterministic and advice-free, with the bEF/SATeq/bounded-SR_h part unchanged., The target lower-bound sentence remains LB_N(1+epsilon) for the same H_N^SAT carrier., Pure selector code A is proof-visible and row-enumerable, so only FormulaEval influence is being tested.
- Expected observation: For alpha<epsilon, uncharged FE rows yield either a sparse-patching upper-bound falsifier or an invalid RowSetEnumerator; charging them raises Gamma by N^{1+alpha+o(1)}, exposing exactly when the route loses the claimed subthreshold proof advantage.
- Transfer certificate needed: A formal certificate that every influential FormulaEval row is either expanded and charged or has a real-SAT enable-bit countermodel; without this certificate, intuition about selector transparency cannot enter the proof queue.

## Next Experiment

Instantiate S_u(j)=A(j) OR (j in T_u and SAT(F_{u,j})) with |T_u|=N^{alpha}; write the bit fields for F_{u,j} enable toggles, compute I_FE exactly, and test whether Gamma_sym,FE crosses N^{1+epsilon} at alpha=epsilon.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Certified ordered-BDD FormulaEval lines are transparent: if a Psys_sym FormulaEval selector is an explicitly printed deterministic ordered BDD B_N over row indices [M_N], then RowSet(B_N) is uniformly enumerable with support-sensitive charge, and the FormulaEval contribution to the occurrence transcript is at most S_NN^{o(1)}+T_N(E_N+d_N)N^{o(1)}.

## Definitions

- source object: a Psys_sym FormulaEval-SAT proof line a_N for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), where M_N=N^{q+o(1)}, G_N is the explicit polylog-length SAT-instance generator, and the row selector is a printed deterministic ordered BDD B_N of size S_N over d_N row bits.
- target object: a bit-explicit occurrence transcript Q_pi and Gamma ledger for the beta-zero lower-bound sentence LB_N(1+epsilon) against circuits for H_N^SAT.
- controlled interface: RowSetEnumerator_N reads the printed BDD nodes, emits every selected row index j exactly once, expands the corresponding formula occurrences G_N(x,j), and charges selector storage plus per-emitted-row SAT binding.
- target-preserving condition: the BDD, variable order, terminal labels, and formula template are advice-free proof data or uniformly reconstructible in the same proof model; any selected row used by FormulaEval must be emitted or backed by a UExtWitnessability certificate.
- S_N: number of explicitly addressed BDD nodes in the FormulaEval line, including terminal and internal nodes.
- T_N: cardinality of the accepted row set {j in [M_N] : B_N(j)=1}.
- E_N: occurrence expansion cost for materializing one row formula G_N(x,j), assumed N^{o(1)} for the beta-zero generator regime.

## Assumptions

- Model: Psys_sym^ROBDD is Psys_bEF^- plus FormulaEval lines whose selectors are printed deterministic ordered BDDs with checkable node labels, low/high pointers, and a declared row-bit order.
- Regime: M_N=N^{q+o(1)}, d_N=ceil(log_2 M_N), formula size E_N=N^{o(1)}, and all proof-line encodings are parseable in N^{o(1)} overhead per touched node or row.
- Uniformity/advice: the BDD is part of the proof transcript or generated by a uniform algorithm named inside the proof; no nonuniform row selector or hard row advice is allowed.
- Same-theory condition: FormulaEval may use SAT(G_N(x,j)) only through emitted row formulas or through an explicit quotient witness; otherwise it is classified as a semantic-oracle rule.
- Naturalness boundary: the lemma is sparse and transcript-specific, not a large constructive property of truth tables.

## Equations

- row-bit-length: `d_N=\lceil \log_2 M_N\rceil=(q+o(1))\log N`. Valid when: Valid when the row universe has size M_N=N^{q+o(1)} and row indices are encoded in binary without hidden advice.
- selected-support: `T_N=|\{j\in[M_N]:B_N(j)=1\}|`. Valid when: Valid when B_N is a deterministic ordered BDD with Boolean terminal labels over the declared row-index variables.
- enumeration-time: `\mathrm{EnumTime}(B_N)\le (S_N+T_Nd_N)N^{o(1)}`. Valid when: Applies after the parser verifies node ordering and each accepting assignment is emitted once by deterministic BDD traversal.
- formulaeval-gamma-increment: `\Delta\Gamma_{FE}^{ROBDD}(a_N)\le S_NN^{o(1)}+T_N(E_N+d_N)N^{o(1)}`. Valid when: Requires the target-preserving FormulaEval interface where every selected row is materialized and no semantic SAT shortcut is used.
- low-cost-falsifier-threshold: `N^{\rho+o(1)}+\Gamma_{bEF^-}(\pi)+\sum_{a\in FE(\pi)}\Delta\Gamma_{FE}^{ROBDD}(a)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Applies after the reduction preserves the beta-zero generator, circuit model, proof transcript, and all FormulaEval charges in the same length regime.

## Attempted Derivation

- Fix a FormulaEval line a_N in Psys_sym^ROBDD and parse its BDD node table: node id, queried row-bit level, low pointer, high pointer, and terminal label.
- Verify acyclicity and strict increase of levels along pointers; reject or scan-charge if the check fails.
- Run DFS from the root. For a branch from level ell to level ell', record skipped variables as free coordinates; at a 1-terminal, expand the accumulated partial assignment into the corresponding row indices in [M_N].
- Disjointness proof: if two accepting paths emitted the same row, their first divergent queried bit would require both bit values for that row, contradicting determinism.
- Charge each BDD node and pointer once to selector parsing, and charge each emitted row by d_N for the index plus E_N for materializing G_N(x,j) and its SAT occurrence links.
- Insert these emitted rows into the existing Gamma_bEF line-induction ledger; all non-FormulaEval Psys_bEF^- rules retain their cycle-99 Gamma charges.
- Compose the parsed transcript with the generator circuit of size N^{rho+o(1)}; if the combined circuit upper bound is below N^{1+epsilon-o(1)}, the claimed LB_N(1+epsilon) is falsified for that transcript.

Blocking gap: The derivation is complete for printed deterministic ordered BDD selectors but not for arbitrary AC0, compressed transition systems, or semantic FormulaEval-SAT rules; those need either a support-sensitive enumerator, scan charge, or a private-row countermodel.

## Falsifiers

- A selector B_N is supplied only as nonuniform advice; then the target-preserving uniformity condition fails.
- A compressed BDD transition has a membership oracle but no output-sensitive row enumerator; the valid charge reverts to N^{1+q+o(1)} scan or semantic-oracle status.
- An unordered or nondeterministic BDD emits overlapping subcubes without a disjointness certificate; duplicate-free T_N accounting is invalid.
- FormulaEval-SAT reads an omitted eval-critical row; flipping the private row gives a falsifier to surface occurrence completion.
- The formula generator G_N hides SAT semantics in a table rather than explicit polylog encodings; E_N=N^{o(1)} expansion is invalid.
- The final bound is only nonuniform because row selection or quotient witnesses are hardwired outside the proof transcript.

## Learning

Cycle 104 turns the cycle-103 ROBDD selector promotion into a proof packet: deterministic ordered BDDs yield disjoint accepting subcubes and hence a valid output-sensitive RowSetEnumerator_N. The exact FormulaEval charge is selector size plus emitted-row expansion, while succinct membership-only selectors remain quarantined. This advances the paper obstruction theorem, not the main P vs NP conjecture.

## Gedanken Experiment Design Seed

- Need decision: `use now as a falsifier probe and threshold calibration for the ROBDD FormulaEval subcase`
- Rationale: The branch needs a concrete target-preserving stress test to decide whether the new support-sensitive ROBDD charge really improves on scan charge without importing hidden row advice.
- Situation seed: Consider H_N^SAT(x)=xor_{j<=M_N}SAT(G_N(x,j)) with M_N=N^{q+o(1)} and one FormulaEval line whose selected row set is represented by a printed ordered BDD B_N of size S_N=N^s accepting T_N=N^t row indices.
- Varied variable: the BDD size exponent s, with T_N and q recorded separately to distinguish selector-complexity cost from support-expansion cost
- Held-fixed controls: G_N has advice-free polylog-size formula encodings, so E_N=N^{o(1)}., The proof model is Psys_sym^ROBDD with printed deterministic ordered BDD node tables and no semantic SAT oracle., The target lower-bound sentence is LB_N(1+epsilon) for unrestricted circuits computing H_N^SAT., The generator overhead remains N^{rho+o(1)} and the existing Psys_bEF^- Gamma ledger is unchanged.
- Expected observation: If max{rho,gamma_bEF,s,t}<1+epsilon, the parsed transcript yields a circuit upper-bound falsifier; if the same row set is supplied by a succinct membership predicate with no enumerator, the charge jumps to N^{1+q+o(1)} or a private-row falsifier appears.
- Transfer certificate needed: A formal RowSetEnumerator_N certificate proving duplicate-free output-sensitive enumeration from the printed BDD, plus SAT binding showing every FormulaEval use is among the emitted rows.

## Next Experiment

Run the same RowSetEnumerator_N audit for one minimal non-ROBDD selector class, preferably read-once branching programs with a certified variable order; either prove the disjoint-output charge or exhibit the smallest overlap/private-row countermodel.
