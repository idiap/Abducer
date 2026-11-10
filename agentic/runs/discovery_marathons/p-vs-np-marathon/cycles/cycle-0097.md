# cycle-0097

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For beta-zero parity carriers parsed by Psys_bEF, avoiding the sparse-row/equality-patching falsifier requires absolute FormulaEval or row/slot support |K_idx(pi)|>=N^{epsilon-o(1)}. Since M_N=N^{q+o(1)}, the required support density is |K_idx(pi)|/M_N>=N^{epsilon-q-o(1)}. Hence q<epsilon gives a full-row-enumeration falsifier under subthreshold auxiliary costs, q=epsilon+o(1) forces near-full semantic contact, and q>epsilon permits vanishing density but still requires N^{epsilon-o(1)} absolute slot contact.

## Definitions

- source object: H_N^SAT is the beta-zero parity carrier on N source rows, H_N(x)=xor_{j<M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, L_N=(log N)^d, and generator size N^{rho+o(1)}.
- target object: LB_N(1+epsilon) is the nonuniform scalar circuit lower-bound claim C(H_N^SAT)>N^{1+epsilon-o(1)}; the target consequence here is only a falsifier for this source claim, not P != NP.
- controlled interface: Psys_bEF is bit-explicit EF+SATeq+bounded-SR_h whose parser outputs K_idx(pi), S_dep, S_link, bounded-SR leaf charge N^{q+eta+tau+o(1)}, and exceptional source-row count E_N.
- target-preserving condition: every SAT semantic use is anchored to explicit row and slot bits or is charged by FormulaEval expansion N|K_idx(pi)|L_N^{O(1)}, with no advice encoding unparsed SAT labels.

## Assumptions

- Circuit model is nonuniform Boolean SIZE; the verifier for Psys_bEF is uniform and reads only the written proof bits.
- Length regime is N -> infinity with fixed epsilon>0, M_N=N^{q+o(1)}, q>=0, rho<1+epsilon, and L_N=polylog(N).
- The parser has already traversed the bit-explicit EF extension-DAG, so extension dependencies are charged in S_dep and SATeq quotient links are charged in S_link.
- bounded-SR_h has explicit leaf addresses; eta and tau are the row-index and leaf-verifier overhead exponents appearing in the audited term N^{q+eta+tau+o(1)}.
- FormulaEval-SAT is not a free semantic oracle in this lemma; if symbolic FormulaEval is present, it must be expanded or the lemma is inapplicable.

## Equations

- slot_expansion_charge: `X_FE(K)=N |K| L_N^{O(1)}=N^{1+kappa+o(1)} for |K|=N^{kappa+o(1)}`. Valid when: Valid when FormulaEval-SAT is expanded over all N source rows for a bit-explicit slot set K of polylogarithmic formula length.
- absolute_support_threshold: `|K_idx(pi)| >= N^{epsilon-o(1)}`. Valid when: Valid when the parsed certificate is intended to avoid the sparse-row equality-patching falsifier below the source lower-bound threshold.
- density_threshold: `|K_idx(pi)|/M_N >= N^{epsilon-q-o(1)}`. Valid when: Applies after M_N=N^{q+o(1)} is fixed and K_idx(pi) counts parity slots in the same beta-zero carrier.
- full_slot_expansion: `X_FE([M_N])=N M_N L_N^{O(1)}=N^{1+q+o(1)}`. Valid when: Valid when every parity slot is surface-expanded over every source row and the generated SAT formulas have polylogarithmic length.
- trichotomy_bound: `q<epsilon => X_FE([M_N])<N^{1+epsilon-o(1)}; q=epsilon+o(1) => X_FE([M_N])=N^{1+epsilon+o(1)}; q>epsilon => |K|/M_N may be N^{epsilon-q-o(1)}`. Valid when: Requires subthreshold dependency, link, generator, and SR overheads so the FormulaEval support term is the decisive threshold variable.

## Attempted Derivation

- Fix H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, L_N=polylog(N), and generator size N^{rho+o(1)}.
- Run the Psys_bEF parser on pi: traverse the EF extension-DAG, charge transitive bit dependencies to S_dep, charge SATeq quotient links to S_link, expand bounded-SR_h leaves into N^{q+eta+tau+o(1)}, and record E_N exceptional source rows.
- For any FormulaEval-SAT component that is not a semantic oracle, expand the selected slot set K_idx(pi) over all N source rows; the bit-level row-index expansion costs X_FE(K)=N|K|L_N^{O(1)}.
- Combine the generator, transcript subcircuits, and equality patches for exceptional rows to obtain C(H_N^SAT)<=N^{rho+o(1)}+Gamma_bEF(pi).
- Compare the FormulaEval expansion term with the source threshold: if |K|=N^{kappa+o(1)}, subthreshold parsing requires kappa<epsilon; therefore any valid nonfalsified certificate needs |K|>=N^{epsilon-o(1)}.
- Substitute M_N=N^{q+o(1)} to get the density threshold |K|/M_N>=N^{epsilon-q-o(1)} and the q-trichotomy: q<epsilon gives full-slot expansion below threshold, q=epsilon is boundary contact, and q>epsilon allows sparse density but not sparse absolute support.
- For Psys_sym without expansion, build the private-row countermodel: keep all charged SATeq/SR/surface labels fixed, flip one unexpanded parity slot at x*, and observe that the transcript is unchanged while H_N(x*) flips.

Blocking gap: The derivation does not prove a parser theorem for Psys_sym when FormulaEval-SAT is a genuine semantic oracle; the named missing lemma is FormulaEval-forcing: real SAT semantics must force every unexpanded row/slot value from the charged transcript with subthreshold overhead.

## Falsifiers

- Subthreshold Gamma_bEF(pi) is a valid falsifier for LB_N(1+epsilon) in the same nonuniform circuit model.
- q<epsilon makes full FormulaEval slot expansion cost N^{1+q+o(1)}, so row/slot enumeration falsifies any claimed need for superthreshold support when other costs are subthreshold.
- A private-row FormulaEval countermodel falsifies surface occurrence completion for Psys_sym semantic-oracle proofs.
- Nonuniform leakage falsifier: advice that encodes SAT labels outside K_idx(pi) invalidates the target-preserving parser interface.
- Threshold-collapse falsifier: if rho, S_dep, S_link, SR overhead, or E_N N already exceed N^{1+epsilon-o(1)}, the route cannot certify a barely-superlinear source contradiction.

## Learning

Cycle 97 closes the support-density subgoal for the Psys_bEF packet: FormulaEval support must have absolute size N^{epsilon-o(1)}, hence density N^{epsilon-q-o(1)} inside M_N=N^{q+o(1)} slots. This yields a sharp q-trichotomy and upgrades the FormulaEval boundary to an expansion-or-private-row-countermodel test. The result is a valid route-level falsifier theorem, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The branch has a theorem-shaped parser but needs a concrete quantitative stress test for the remaining FormulaEval support threshold, not another abstract barrier restatement.
- Situation seed: A Psys_sym proof family for H_N^SAT is allowed one FormulaEval-SAT macro over a slot set K_N of size N^{kappa+o(1)}; the macro either expands over all N source rows or is treated as a semantic oracle.
- Varied variable: kappa=log_N |K_N|, the exponent of the FormulaEval slot support size.
- Held-fixed controls: beta=0 with L_N=(log N)^d and d>1, M_N=N^{q+o(1)} and generator size N^{rho+o(1)} with rho<1+epsilon, same nonuniform SIZE model for LB_N and synthesized upper bounds, no advice containing SAT labels outside the charged transcript, bounded-SR_h and SATeq resources charged exactly as in Gamma_bEF(pi)
- Expected observation: The expansion charge crosses the source lower-bound threshold at kappa=epsilon. For kappa<epsilon it yields a falsifier; for q<epsilon even K_N=[M_N] remains subthreshold; for q>epsilon the required density can vanish but the absolute support N^{epsilon-o(1)} remains mandatory.
- Transfer certificate needed: A formal FormulaEval expansion theorem mapping the macro to N|K_N|L_N^{O(1)} charged occurrences, or a nonrelativizing FormulaEval-forcing lemma; absent either certificate, the private-row countermodel blocks proof promotion.

## Next Experiment

Instantiate Psys_sym in two concrete variants: FormulaEval as an EF extension rule with row-index bits and FormulaEval as a semantic oracle. For each, compute K_idx(pi), X_FE(K), and whether the private-row countermodel survives SATeq and bounded-SR constraints.

# Barrier-Aware Lower-Bound Route, cycle 97: bEF parser charge and FormulaEval boundary

## Candidate Lemma

Restricted parser theorem. For a bit-explicit Psys_bEF proof pi of LB_N(1+epsilon) for H_N^SAT, if every SATeq and bounded-SR_h line is row-faithful at the bit-DAG level, then a deterministic no-advice parser outputs an occurrence transcript T_pi, semantic row set K_idx(pi), and charge Gamma_bEF(pi). The transcript gives the upper-bound falsifier C(H_N^SAT)<=N^{rho+o(1)}+Gamma_bEF(pi); hence a sound proof cannot satisfy the subthreshold inequality.

## Definitions

- source object: an accepted Psys_bEF proof pi of LB_N(1+epsilon), where LB_N(1+epsilon) asserts C(H_N^SAT)>N^{1+epsilon-o(1)} for H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), N=2^n, M_N=N^{q+o(1)}, and G_N has nonuniform generator size N^{rho+o(1)}.
- target object: a parsed occurrence transcript T_pi with row indices K_idx(pi), dependency charge S_dep(pi), link charge S_link(pi), bounded-substitution charge, and exceptional-row charge E_N N, sufficient to build a nonuniform circuit for H_N^SAT when the total charge is small.
- controlled interface: bit-level EF extension definitions, SATeq axioms over displayed formula encodings, and bounded-SR_h rules whose affected generator rows are named by checkable index circuits; no semantic FormulaEval oracle, hidden advice, or opaque SAT table access is allowed.
- target-preserving condition: every proof line that changes a SAT formula either exposes a transitive bit-DAG path to the displayed G_N(x,j) encoding or pays an explicit row-expansion charge, so the parser's transcript is uniform and no-advice in the same nonuniform SIZE target model.
- Psys_bEF: each line is a self-delimiting bit string containing a line type, predecessor pointers, EF gate definitions, formula-bit intervals, SATeq justifications, or a bounded-SR_h certificate; the verifier runs in poly(|pi|,log N) given N and pi.
- K_idx(pi): the set of generator rows j for which the parser finds a row-faithful path from a proof SAT atom to SAT(G_N(.,j)); repeated syntactic occurrences count once for semantic support.
- S_dep(pi), S_link(pi), E_N: respectively the number of formula-bit dependencies traversed, pointer/link traversals checked, and unparsed exceptional generator rows charged by hardwiring their N-bit row truth tables.

## Assumptions

- Model: target circuits are nonuniform Boolean circuits for the n-bit function H_N^SAT, and circuit size is measured as a function of N=2^n.
- Regime: epsilon>0 is fixed, M_N=N^{q+o(1)}, proof length |pi|=N^{tau+o(1)}, bounded-SR fan-in h=N^{eta+o(1)}, and rho<1+epsilon is the generator overhead exponent.
- Uniformity/advice: the parser is deterministic, receives only N and pi, and may not use a row-selection advice string or a nonuniform table of SAT values.
- Bit-realizability: every SATeq instance compares displayed formula encodings or encodings reached through EF extension pointers, not semantic equality of formulas supplied by an oracle.
- Rule cutoff: bounded-SR_h may mention at most h=N^{eta+o(1)} row templates per proof line, with row enumerators checkable from the proof bits.
- Naturalness boundary: the lemma is a route-level parser and falsifier theorem; it induces a natural-property pressure only if the extracted transcript family is also large and poly(N)-constructive.

## Equations

- resource_exponents: `M_N=N^{q+o(1)},\quad |\pi|=N^{\tau+o(1)},\quad h=N^{\eta+o(1)}`. Valid when: Valid when beta-zero generator lengths are polylogarithmic and proof/rule resources are measured as powers of N in Psys_bEF.
- parser_charge: `\Gamma_{bEF}(\pi)=S_{dep}(\pi)+S_{link}(\pi)+N^{q+\eta+\tau+o(1)}+E_N\,N`. Valid when: Valid when bounded-SR_h row templates are explicitly enumerated and exceptional rows are charged by full N-bit hardwiring.
- transcript_size: `|T_\pi|\le \Gamma_{bEF}(\pi)\,N^{o(1)}`. Valid when: Valid when pointer encodings, row indices, and formula-bit intervals have polylogarithmic length and no hidden advice is used.
- circuit_upper_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{bEF}(\pi)\,N^{o(1)}`. Valid when: Applies after the parsed transcript is row-faithful and the generator circuit can feed all charged SAT-row gadgets uniformly.
- subthreshold_falsifier: `N^{\rho+o(1)}+\Gamma_{bEF}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Valid when LB_N is the nonuniform circuit lower-bound sentence for the same H_N^SAT and exponent epsilon.

## Attempted Derivation

- Fix N=2^n, the carrier H_N^SAT, and a self-delimiting Psys_bEF encoding of EF gates, predecessor pointers, formula-bit intervals, SATeq lines, and bounded-SR_h certificates.
- Start from the output clauses of pi proving LB_N(1+epsilon), traverse predecessor pointers backwards, and charge each pointer once to S_link(pi).
- Whenever an EF extension variable is reached, expand its defining gate recursively through the extension DAG; charge the touched formula and gate bits to S_dep(pi).
- For a SATeq line, accept it into the transcript only if both formula encodings are displayed or reachable through the extension DAG; otherwise mark it exceptional and charge the affected row by N gates.
- For a bounded-SR_h line, enumerate its h=N^{eta+o(1)} local row templates for each relevant proof line and generator-row block; the crude worst-case charge is |pi| M_N h=N^{q+eta+tau+o(1)}.
- Collect all row-faithful generator indices into K_idx(pi). Repeated syntactic uses of the same row are merged because residual patching needs semantic support, not occurrence count.
- Build the residual circuit by combining the generator of size N^{rho+o(1)} with the parsed transcript gadgets and hardwired exceptional rows. This yields C(H_N^SAT)<=N^{rho+o(1)}+Gamma_bEF(pi)N^{o(1)}.
- If this upper bound is below N^{1+epsilon-o(1)}, the asserted LB_N(1+epsilon) is false in the same target model; this is the transcript upper-bound falsifier theorem.
- Attempting the identical traversal in Psys_sym stops at an opaque FormulaEval-SAT line: the line has O(1) surface occurrences but may semantically cover all M_N rows, so RowFaithfulFormulaEval_N is the exact missing bridge.

Blocking gap: Full Psys_sym remains blocked at RowFaithfulFormulaEval_N: prove every FormulaEval-SAT use yields checkable row support or pay expansion charge N^{1+q+o(1)}. The restricted Psys_bEF derivation is valid only under the row-faithful bit-DAG assumptions above.

## Falsifiers

- q<epsilon row-enumeration falsifier: all M_N rows hardwired by N-bit truth tables give C(H_N^SAT)<=N^{1+q+o(1)}, so LB_N(1+epsilon) is false in the same nonuniform target model.
- Opaque FormulaEval-SAT falsifier: one proof line asserts a semantic evaluation vector for all SAT(G_N(x,j)); surface occurrence parsing sees O(1) while semantic support is M_N, so occurrence completion is not valid.
- Indexed substitution falsifier: an extension variable names a compressed index-to-formula map rather than displayed row formulas, separating syntactic occurrences from K_idx(pi).
- Advice-leakage falsifier: if the parser chooses K_idx(pi) using a nonuniform row advice string, residual patching no longer certifies a target-preserving no-advice circuit upper bound.
- Naturalness falsifier: if the extracted property is large, poly(N)-constructive, and useful against the same SIZE class, then PRF tension applies; escape requires non-largeness, nonconstructivity, or proof-system specificity that does not induce a truth-table property.

## Learning

Cycle 97 converts the bEF side from a remembered parser slogan into a restricted theorem packet: bit-level Psys_bEF plus row-faithful SATeq/bounded-SR_h yields Gamma_bEF(pi) and the valid transcript upper-bound falsifier. The live inference-quality packet is: source_statement=accepted Psys_bEF proof of LB_N(1+epsilon) for H_N^SAT; target_statement=occurrence transcript, q-trichotomy, and subthreshold circuit-upper-bound falsifier; model_context=nonuniform Boolean SIZE, beta-zero SAT parity carrier, bit-explicit EF+SATeq+bounded-SR_h proof model, simulation/extraction rather than many-one reduction; quantifier_context=N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, h=N^{eta+o(1)}, rho<1+epsilon, deterministic no-advice parser; derivation_status=restricted Psys_bEF charge derived, full Psys_sym blocked at RowFaithfulFormulaEval_N; reviewer findings=occurrence parser valid only for row-faithful bit-DAG syntax, opaque FormulaEval-SAT is a finite semantic countermodel, naturalness pressure triggers only if the transcript induces a large constructive useful property. This is route-level progress, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for Psys_sym, not as evidence for the main conjecture.`
- Rationale: The abstract obstruction is now concentrated in one mechanism, FormulaEval-SAT. A concrete expansion experiment tests whether the semantic rule can be made target-preserving or must be quarantined.
- Situation seed: Take H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)} and insert a single Psys_sym FormulaEval-SAT line FE_N that claims to evaluate the vector (SAT(G_N(x,j)))_{j<M_N} without listing row encodings.
- Varied variable: Expansion fraction alpha, where FE_N exposes K=N^{alpha+o(1)} row-faithful generator indices to the parser while the remaining rows stay semantic and opaque.
- Held-fixed controls: N=2^n, beta-zero polylogarithmic SAT instance length, and the same generator G_N of size N^{rho+o(1)}., The target model remains nonuniform Boolean SIZE for H_N^SAT, with no parser advice and the same LB_N(1+epsilon) sentence., q, rho, epsilon, eta, and tau are held fixed while only alpha varies., Each exposed row costs O(N) gates and each opaque row is forbidden from contributing to a valid transcript unless RowFaithfulFormulaEval_N is proved.
- Expected observation: If alpha<epsilon, residual patching gives a subthreshold upper-bound falsifier; if alpha>=epsilon but alpha<q, density is sparse yet absolute support pressure survives; full row-faithful expansion costs N^{1+q+o(1)} and prevents a cheap occurrence parser.
- Transfer certificate needed: A RowFaithfulFormulaEval_N theorem mapping every FE_N semantic assertion to checkable row indices and dependency DAGs, or a formal oracle countermodel proving that no occurrence transcript is valid for opaque FE_N.

## Next Experiment

Formalize the smallest Psys_sym oracle countermodel FE_N with one FormulaEval-SAT line, prove occ(FE_N)=O(1) and |K_sem(FE_N)|=M_N, then test whether any proposed RowFaithfulFormulaEval_N axiom forces expansion charge N^{1+q+o(1)} without hidden advice.

# MCSP / Meta-Complexity Carrier Transfer supporting bit-explicit parser boundary

## Candidate Lemma

Bit-explicit parser theorem for Psys_bEF^-: every accepted EF+SATeq+bounded-SR_h proof pi for the beta-zero SAT-parity carrier, with only witnessed formula identity, has an advice-free occurrence transcript Q_pi of cost Gamma_bEF(pi); if row-parity binding holds, Q_pi plus the generator gives an unrestricted circuit upper bound for H_N^SAT.

## Definitions

- source object: a Psys_bEF^- proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), where M_N=N^{q+o(1)} and each generated SAT instance has polylogarithmic formula length.
- target object: an occurrence transcript Q_pi containing generator calls, extension-DAG dependencies, SATeq quotient links, bounded-SR_h support rows K_idx(pi), and exceptional rows requiring full N-bit patches.
- controlled interface: bit-level EF extension definitions, SATeq axioms with explicit quotient witnesses, and bounded-SR_h rules whose touched row-label neighborhood is syntactically enumerable; unwitnessed FormulaEval-SAT is excluded.
- target-preserving condition: every formula identity or SAT equality used by pi is witnessed by an advice-free bit quotient whose adaptive-cover cost is charged to S_link or to the bounded-SR_h support term.

## Assumptions

- Length regime: N tends to infinity, M_N=N^{q+o(1)}, generator circuit size is N^{rho+o(1)}, proof line count is N^{tau+o(1)}, and each line encoding is polylog(N) times its listed row-label support.
- Rule regime: every EF extension variable has a unique earlier bit formula definition, every SATeq use carries a checkable equality/renaming witness, and every bounded-SR_h step exposes at most N^{eta+o(1)} row-neighborhood entries per row index.
- Uniformity regime: the parser is deterministic and advice-free, runs in time polynomial in the explicit proof length plus the listed witnesses, and never chooses a hard row nonuniformly.
- Circuit model: target upper bounds are unrestricted Boolean circuits for the N-bit truth table of H_N^SAT; proof-system soundness is used only to justify row-parity binding, not to prove P != NP.
- Same-theory condition: pi reasons about the same encoded G_N, SAT predicate, and lower-bound sentence LB_N(1+epsilon) that define the target function, with no hidden change of carrier.

## Equations

- carrier-definition: `H_N^{SAT}(x)=\bigoplus_{j<M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad |G_N|=N^{\rho+o(1)}`. Valid when: Valid when the beta-zero SAT-parity source family and generator encoding are fixed uniformly for all lengths N.
- proof-resource-regime: `L(\pi)=N^{\tau+o(1)},\quad h_{SR}=N^{\eta+o(1)}`. Valid when: Valid when Psys_bEF^- line count and bounded substitution-row neighborhoods are explicitly parsed from the bit-level proof.
- gamma-ledger: `\Gamma_{bEF}(\pi)=S_{dep}(\pi)+S_{link}(\pi)+N^{q+\eta+\tau+o(1)}+E_N(\pi)N`. Valid when: Applies after EF dependencies, witnessed SATeq links, bounded-SR_h support, and exceptional full-row patches are separately counted.
- transcript-upper-bound: `|Q_\pi|\le \Gamma_{bEF}(\pi),\quad C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{bEF}(\pi)`. Valid when: Requires row-parity binding and an advice-free transcript-to-circuit simulation over the same generated SAT-row family.

## Attempted Derivation

- Define Psys_bEF^- syntax at bit level: proof lines are tagged as EFdef, SATeqWitness, boundedSR_h, BooleanInference, or LBConclusion; each line lists formula-code bit ranges and row-index fields.
- For EFdef lines, add extension-DAG edges from the new variable to earlier bit formulas; charge each edge to S_dep(pi). Acyclicity is checkable by line order.
- For SATeqWitness lines, parse the quotient witness as a bounded map between formula-code DAG nodes; charge each witnessed formula-code identification to S_link(pi).
- For boundedSR_h lines, enumerate the exposed row-label neighborhood: at most M_N*N^{eta+o(1)} entries per N^{tau+o(1)} proof lines, giving the term N^{q+eta+tau+o(1)}.
- For proof lines whose local grammar cannot expose a row neighborhood, mark affected rows exceptional; each such row is charged by a full N-bit patch, giving E_N(pi)N.
- Induct on proof lines: each parsed line preserves the invariant that every occurrence-level SAT label in the line is represented by a transcript node connected to all required dependency and equality witnesses.
- At the LBConclusion line, invoke RowParityBinding_bEF: the local satisfying assignments to Q_pi force the parity value H_N^SAT(x) for each x; this converts the occurrence transcript into a total truth-table computation.
- Build the circuit: compute all generated formula codes with the N^{rho+o(1)} generator, evaluate transcript-local Boolean wiring, and hardwire exceptional/touched row patches. This gives C(H_N^SAT)<=N^{rho+o(1)}+Gamma_bEF(pi).
- Compare the upper bound to N^{1+epsilon-o(1)}. If it is smaller, the alleged lower-bound sentence is semantically false, yielding a route-level falsifier for low-cost Psys_bEF^- carriers.

Blocking gap: The line induction is valid for Psys_bEF^- with witnessed formula identity, but full Psys_sym remains blocked at FormulaEval-SAT: without UExtWitnessability, surface occurrence completion has a two-formula-code countermodel and the parser cannot soundly identify semantic SAT values.

## Falsifiers

- Unwitnessed FormulaEval-SAT line: two formula codes are semantically identified without a quotient witness, so occurrence completion can assign inconsistent SAT labels while satisfying the parsed local transcript.
- Hidden advice in row selection: the proof or parser selects hard rows by nonuniform advice rather than by the bit-level transcript, invalidating the target-preserving transfer.
- Subthreshold row enumeration: q<epsilon and all relevant rows are patchable at cost N^{1+q+o(1)}, contradicting a claimed N^{1+epsilon-o(1)} lower bound.
- Low-cover quotient leakage: S_link or the adaptive-cover exponent is omitted from Gamma_bEF(pi), producing an artificially cheap transcript.
- Exceptional-row explosion: E_NN reaches or exceeds N^{1+epsilon-o(1)}, making the falsifier inequality unavailable.
- Proof-local approximation only: Q_pi determines labels used in pi but not the full H_N^SAT truth table, so the circuit upper bound is not valid.

## Learning

Cycle 97 makes the parser contribution sharper: for Psys_bEF^- the Gamma_bEF ledger follows from a line-induction over bit-level proof rules, while the only full-system obstruction is the named FormulaEval-SAT/UExtWitnessability fork. The valid route-level output is a finite low-cost-transcript falsifier, not progress on the main P != NP conjecture.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The live theorem packet hinges on whether Gamma_bEF(pi) crosses the lower-bound threshold; varying one proof-resource exponent gives a concrete transfer threshold rather than another abstract parser restatement.
- Situation seed: A padded beta-zero SAT-query family H_N^SAT with M_N=N^q polylog-size generated formulas, an advice-free generator of size N^rho, and Psys_bEF^- proofs pi_tau whose only nonlocal formula identities are witnessed SATeq quotient links.
- Varied variable: tau, the proof-line exponent in L(pi_tau)=N^{tau+o(1)} while boundedSR_h radius exponent eta is held fixed.
- Held-fixed controls: q, rho, epsilon, and eta are fixed constants with rho<1+epsilon., FormulaEval-SAT is disabled unless a quotient witness is supplied and charged., The target is the same unrestricted circuit lower-bound sentence LB_N(1+epsilon) for H_N^SAT., No row selector advice or nonuniform hard-row choice is allowed in the parser.
- Expected observation: For tau<1+epsilon-q-eta and subthreshold S_dep,S_link,E_NN, the parsed transcript gives C(H_N^SAT)<N^{1+epsilon-o(1)}, so any claimed proof is falsified; once tau crosses that threshold, the parser may remain valid but no longer refutes the proof.
- Transfer certificate needed: A formal RowParityBinding_bEF lemma plus a bit-level boundedSR_h parser audit showing that every semantic dependency of pi_tau is counted in S_dep, S_link, N^{q+eta+tau+o(1)}, or E_NN.

## Next Experiment

Formalize RowParityBinding_bEF for the LBConclusion line: define LocSat(Q_pi), prove parity constancy for witnessed SATeq quotients, and then test the minimal FormulaEval-SAT two-code countermodel against the exact bit grammar.
