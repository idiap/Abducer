# cycle-0128

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For Psys_sym^{dag+declTSR}, where every bounded Tseitin self-reduction use exposes a complete child-row list before semantic use, the least closed support cone K_TSR(pi) is computable from pi and N; the parser line induction extends with Gamma_TSR(pi)=Gamma_bEF(pi)+U(K_dag)+X(K_dag)+R_TSR(pi). If N^{rho+o(1)}+Gamma_TSR(pi)+O(E_pi N)<N^{1+epsilon-o(1)}, then the claimed LB_N(1+epsilon) for H_N^SAT has a same-model upper-bound falsifier.

## Definitions

- source object: H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, polylog formula length L_N, and generator circuit size N^{rho+o(1)}.
- target object: the nonuniform SIZE lower-bound assertion LB_N(1+epsilon), namely C(H_N^SAT)>N^{1+epsilon-o(1)} on valid lengths.
- controlled interface: Psys_sym^{dag+declTSR} proof lines expose K_dag parent pointers and, for each TSR use, a complete child-row list containing path bits, restriction masks, Tseitin-map id, parent row id, and child row id.
- target-preserving condition: the parser expands only same-theory SAT or Tseitin-equivalent rows, uses no SAT-truth advice, and all rows that can affect the final LB_N line enter the least closed cone before the rule is applied.
- K_TSR(pi) is the least fixed point starting from the final LB line and closing under bit-explicit EF dependencies, SATeq links, transparent FormulaEval supports, and declared TSR child lists.
- A_TSR=N^{kappa+o(1)} is the number of active TSR parent rows in the reachable cone; B_TSR=N^{theta+o(1)} is the declared child branching per active parent row; E_pi is the sparse residual row count patched by equality circuits.

## Assumptions

- Circuit model is nonuniform Boolean SIZE with no hidden advice beyond the proof string pi and declared row encodings.
- Length regime is over valid N with L_N=(log N)^d for fixed d>1, so beta=0 substitution into SAT circuits remains N^{o(1)}.
- Every TSR child formula is syntactically checkable as a bounded Tseitin or restriction child of its parent formula in time poly(L_N) per row.
- The row enumerator for K_TSR is advice-free and emits canonical row ids, so duplicate child declarations are charged once by the fixed-point set representation.
- The same-theory condition forbids replacing undeclared semantic branch pruning by SAT truth-table advice.
- The proof pi is in the restricted declared schema; this lemma does not cover arbitrary semantic FormulaEval or hidden pruning.

## Equations

- Gamma_TSR_ledger: `Gamma_TSR(pi)=Gamma_bEF(pi)+U(K_dag)+X(K_dag)+R_TSR(pi)+O(E_pi N)`. Valid when: Valid when pi belongs to the declared support schema and each dependency edge is surfaced before the parser line induction uses it.
- Declared_TSR_charge: `R_TSR(pi) <= N*A_TSR*B_TSR*L_N^{O(1)} = N^{1+kappa+theta+o(1)}`. Valid when: Applies when active TSR parent rows are N^{kappa+o(1)} and every parent declares N^{theta+o(1)} bounded children of polylog description size.
- Parser_upper_bound: `C(H_N^SAT) <= N^{rho+o(1)}+Gamma_TSR(pi)+O(E_pi N)`. Valid when: Requires the target-preserving fixed-point parser, same-model row expansion, and equality patching for only E_pi residual rows.
- TSR_subthreshold_window: `rho<1+epsilon, kappa+theta<epsilon, and E_pi<N^{epsilon-o(1)} imply a subthreshold LB_N falsifier if other Gamma_dag terms are subthreshold`. Valid when: Valid when the preexisting transparent-support charges are already below N^{1+epsilon-o(1)} and TSR is the only new rule charge.

## Attempted Derivation

- Initialize K_0 with row ids and proof lines reachable from the final LB_N(1+epsilon) line.
- Define closure operator Cl(S): add bit-explicit EF parent dependencies, SATeq quotient links, transparent FormulaEval support rows, and for every TSR parent row in S add every declared child row from its syntactic child list.
- Iterate K_{t+1}=Cl(K_t) until a fixed point. Termination is bounded by the finite proof-size row universe; canonical ids ensure no duplicate charge.
- For non-TSR lines reuse the established Gamma_bEF and Gamma_dag line induction: every reachable line has a local circuit using only previously charged reachable rows.
- For a declared TSR line, verify each child descriptor locally: parent id, path bits, restriction mask, Tseitin map id, and child slot id. Build the parent semantic value by a bounded OR/AND circuit over the declared child row values plus poly(L_N) consistency checks.
- Charge N*poly(L_N) per declared child row expansion. With A_TSR=N^{kappa+o(1)} active parents and B_TSR=N^{theta+o(1)} children per parent, obtain R_TSR<=N^{1+kappa+theta+o(1)}.
- Patch E_pi residual rows by equality tests on the N-bit source input, costing O(E_pi N). Add the generator cost N^{rho+o(1)} to obtain a same-model circuit for H_N^SAT.
- If the resulting size is below N^{1+epsilon-o(1)}, the alleged source lower-bound certificate has a valid upper-bound falsifier.
- For hidden pruning, choose the first child r* used semantically but absent from K_TSR. Flip its SAT label in a two-world oracle while preserving all visible rows; the proof transcript is unchanged but the induced reachable parity can flip.

Blocking gap: The declared complete-child schema has no current derivation gap beyond writing the final syntax checker. The full semantic rule remains blocked exactly at RealSATInfluenceRealizer_N^arb, which must list all influencing rows without SAT-truth advice.

## Falsifiers

- falsifier: first-unlisted TSR child whose SAT label affects a reachable line but is absent from the charged support cone.
- falsifier: kappa+theta>=epsilon, causing declared TSR expansion to lose the subthreshold contradiction window.
- falsifier: semantic branch pruning that depends on real satisfiability before any advice-free row realizer is emitted.
- falsifier: positive beta fallback, where the transfer upper bound q+beta*c+o(1) caps all-exponent P/poly exclusion.
- falsifier: nonuniform child-list advice hidden in extension variables rather than verifier-visible row encodings.

## Learning

Cycle 128 closes a sharper declared-TSR support sublemma: complete child declarations compose with the least support fixed point and cost exactly N^{1+kappa+theta+o(1)}, while hidden branch pruning has a first-unlisted-child private-row falsifier. The contribution remains a scoped parser/falsifier theorem, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for hidden TSR pruning and as a threshold calibration for declared TSR.`
- Rationale: The remaining theorem boundary is concrete: either every TSR child influence is charged in K_TSR, or a single hidden child invalidates the parser. A thought experiment exposes this without broadening into a new carrier.
- Situation seed: Take H_N^SAT with M_N=N^{q+o(1)} polylog SAT rows and a proof pi containing one bounded Tseitin self-reduction line whose visible children are all declared except one branch child r* controlled by an unread enable bit e.
- Varied variable: theta, the exponent for declared children per active TSR parent; in the hidden variant vary whether r* is declared or left behind the unread enable bit.
- Held-fixed controls: beta=0 polylog target-query length and generator cost N^{rho+o(1)}., Same nonuniform SIZE model for source upper bound and target lower-bound audit., Bit-explicit EF, SATeq, bounded SR_h, and transparent FormulaEval charges already included in Gamma_dag., No SAT-truth advice and no hidden row-selection advice in the declared experiment.
- Expected observation: When r* is declared, the ledger grows by N^{1+kappa+theta+o(1)} and the valid threshold is kappa+theta<epsilon. When r* is hidden, two worlds agree on the transcript but differ on the carrier, giving a private-row falsifier.
- Transfer certificate needed: An advice-free RealSATInfluenceRealizer_N^arb or declared-child syntax checker proving that every semantic TSR influence row is uniformly listed, same-theory expanded, and charged before it affects the final LB_N line.

## Next Experiment

Write the paper-ready TSR rule schema table and verify on one toy projected-dDNNF plus TSR line: compute K_TSR, A_TSR, B_TSR, R_TSR, and then flip the first unlisted child in the hidden-pruning variant.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Restricted Gap98-SRhLineInduction_N: for Psys_bEF^- with annotated bounded-SR_h FormulaEval lines, a deterministic no-advice parser computes a Gamma_bEF^SR transcript with SR contribution at most N^{tau+eta+o(1)}. If total row-equivalent support is below N^{epsilon-o(1)} and rho<1+epsilon, then the claimed LB_N(1+epsilon) proof is refuted by a same-model SIZE upper-bound falsifier.

## Definitions

- source object: a Psys_bEF^- proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with annotated bounded-SR_h FormulaEval lines.
- target object: a same-model nonuniform SIZE upper-bound falsifier or a forced row-equivalent support lower bound for H_N^SAT.
- controlled interface: Gap98-SRhNormalForm_N exposes rule tag, parent line ids, row-index encodings, touched occurrence-neighborhoods, and ChildRows lists to the parser.
- target-preserving condition: all SR_h and FormulaEval influence rows are proof-visible, row-cover closed, prefix-spliceable in the same bEF theory, and extracted without advice.
- row-equivalent support means base bEF row support plus listed SR_h child rows plus charged FormulaEval rows plus normalized enumeration debt.
- bounded-SR_h schema means each SR step has at most h=N^{eta+o(1)} child rows and each child row carries O(log M_N) index bits and polylog(N) occurrence-neighborhood data.

## Assumptions

- Length regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, h=N^{eta+o(1)}, and size(G_N)=N^{rho+o(1)}.
- Target class is nonuniform Boolean SIZE on the same N-bit carrier; the reduction type is parser-to-circuit simulation, not a many-one SAT reduction.
- Every bEF axiom, extension line, SATeq line, and bounded-SR_h line is bit-explicit and locally checkable in polylog(N) time per listed occurrence neighborhood.
- The SR_h annotation is extensional: omitting any influencing child row invalidates the rule instance rather than creating an uncharged semantic oracle.
- Same-theory prefix splicing is available with fresh extension variables, so replacing an annotated SR_h line by row-expanded bEF material preserves the proof theory.
- No hidden selector advice, unread enable bit, or semantic FormulaEval oracle may choose an influencing row after the parser has fixed the transcript.

## Equations

- SR-row-charge: `\Gamma_{SR_h}(\pi)=\sum_{\ell\in SR_h(\pi)} |ChildRows(\ell)|\le |\pi|hN^{o(1)}=N^{\tau+\eta+o(1)}`. Valid when: Valid when every SR_h application carries a proof-visible child-row list of length at most h and the proof has N^{tau+o(1)} lines.
- SR-bit-expansion-debt: `BitDebt_{SR_h}(\pi)\le N^{1+o(1)}\Gamma_{SR_h}(\pi)=N^{1+\tau+\eta+o(1)}`. Valid when: Applies after each listed row is expanded by the same-theory bEF row circuit with N^{1+o(1)} bit cost.
- normalized-support-ledger: `\widehat S_{eff}^{SR}(\pi)=\Gamma_{base}(\pi)+\Gamma_{SR_h}(\pi)+E_N^*+\lceil U_N/N\rceil`. Valid when: Valid when the transparent-support ledger normalizes bit-enumeration debt U_N to row-equivalent units before the upper-bound transfer.
- subthreshold-upper-bound-falsifier: `\rho<1+\epsilon\ \wedge\ \widehat S_{eff}^{SR}(\pi)<N^{\epsilon-o(1)}\Rightarrow C(H_N^{SAT})<N^{1+\epsilon-o(1)}`. Valid when: Requires the target-preserving same-model expansion and excludes hidden semantic rows, otherwise the circuit upper bound need not follow.

## Attempted Derivation

- Normalize each annotated bounded-SR_h line to fields (tag, line id, parent ids, output row a, substitution code, ChildRows list, touched occurrence-neighborhood list, local checker hash).
- Run a deterministic worklist from the final LB_N line. For base bEF and SATeq lines, use the existing bit-explicit parser; for SR_h lines, enqueue exactly the listed ChildRows and charge their occurrence neighborhoods.
- Maintain the induction invariant: after processing prefix t, every semantic dependency of every accepted transparent line in the prefix is either in K_t, in the base bEF ledger, or in normalized enumeration debt U_t/N.
- For an SR_h step, the Gap98 normal form makes the local verifier inspect only parent pointers, row-index encodings, and the listed occurrence neighborhoods; hence adding ChildRows(ell) preserves the invariant and increases Gamma by |ChildRows(ell)|N^{o(1)}.
- Prefix-splice each listed row expansion using fresh extension variables. The splice is line-order preserving because the SR_h conclusion is replaced only after its parent rows and local occurrence checks have already appeared in the expanded prefix.
- Summing over at most |pi|=N^{tau+o(1)} SR_h lines, each with h=N^{eta+o(1)} rows, gives Gamma_SR_h<=N^{tau+eta+o(1)} and bit debt N^{1+tau+eta+o(1)}.
- Apply the residual circuit construction: the generator contributes N^{rho+o(1)} gates and each row-equivalent support unit contributes N^{1+o(1)} gates. If the total is below N^{1+epsilon-o(1)}, the alleged LB_N(1+epsilon) has a same-model upper-bound falsifier.

Blocking gap: The derivation is complete only for annotated bounded-SR_h inside transparent Psys_bEF^- or Psys_sym fragments. Arbitrary semantic FormulaEval remains blocked at RealSATInfluenceRealizer_N; the first omitted child row gives the no-go object when no realizer is supplied.

## Falsifiers

- First omitted child row: an unannotated SR_h line has identical visible occurrence data but flips validity through a private row r*, refuting occurrence-only completion.
- Subthreshold charge falsifier: if tau+eta<epsilon and other debts are lower order, FE/SR support yields C(H_N^SAT)<N^{1+epsilon-o(1)}, so LB_N(1+epsilon) is not valid in the same SIZE model.
- q<epsilon ceiling: the carrier upper bound C(H_N^SAT)<=N^{1+q+o(1)} already falsifies any claimed N^{1+epsilon} lower bound before proof-system parsing matters.
- Advice leakage falsifier: a hidden selector choosing one row from M_N without listing or enumeration charge breaks the no-advice transfer certificate.

## Learning

Cycle 128 turns the annotated bounded-SR_h packet into a line-induction charge theorem: the exact new exponent is tau+eta, yielding a valid subthreshold upper-bound falsifier while leaving arbitrary semantic FormulaEval quarantined at RealSATInfluenceRealizer_N.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch now has a concrete SR_h charge formula; varying one exponent tests whether the parser theorem has a real threshold or merely restates semantic visibility.
- Situation seed: A family of annotated bounded-SR_h proofs for H_N^SAT with |pi|=N^{tau+o(1)}, M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and each SR_h rule listing h=N^{eta+o(1)} child rows.
- Varied variable: eta, the exponent of child rows per bounded-SR_h inference.
- Held-fixed controls: rho<1+epsilon and the same nonuniform SIZE target model are held fixed., All child rows are proof-visible, row-cover closed, and prefix-spliceable in Psys_bEF^-., No hidden selector advice or semantic FormulaEval oracle is allowed., Base bEF charge, E_N^*, and U_N/N are held below N^{epsilon-o(1)} unless deliberately tested as debt carriers.
- Expected observation: For tau+eta<epsilon, the proof family becomes self-refuting by a SIZE upper-bound falsifier; near tau+eta=epsilon it must touch a threshold-scale row cone; above the threshold the parser gives no contradiction but still records paid support.
- Transfer certificate needed: A checked Gap98-SRhNormalForm_N plus same-theory prefix-splice proof that every listed child row expansion is valid and that no unlisted semantic row can influence the SR_h conclusion.

## Next Experiment

Write the referee-checkable proof packet for Gamma_bEF^SR: one sample SR_h line with concrete bit fields, one line-induction table, the summation Gamma_SR_h<=N^{tau+eta+o(1)}, and the first-omitted-child-row countermodel for the unannotated variant.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For a bit-explicit Psys_sym^time proof pi of the beta-zero parity lower-bound claim, every FormulaEval value that affects the final LB_N line has a first unquarantined use u. If pi_{<u} contains an advice-free enumerator or full-scan realizer for every SAT row influencing that value, with same-theory row expansion charged before u, then the Gamma_bEF line induction extends to Gamma_use. If some influencing row is absent at its first unquarantined use, a private-row or unread-enable-bit completion is a finite falsifier for the parser. Delayed support is valid only when the FormulaEval value and all descendants remain syntactically quarantined until the charged exit line.

## Definitions

- source object: a bit-explicit Psys_sym^time transcript pi proving LB_N for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with FormulaEval nodes, timestamped dependency edges, row selectors, and optional syntactic quarantine labels.
- target object: a same-model nonuniform SIZE circuit upper-bound falsifier for LB_N(1+epsilon) obtained by parsing pi into a circuit for H_N^SAT.
- controlled interface: the first-use support cone K_use(pi), where each influential row is admitted only by prefix-visible enumeration, full scan, or zero-latency RealSATInfluenceRealizer_N plus charged occurrence expansion before first unquarantined use.
- target-preserving condition: the parser is advice-free, same-theory, bit-explicit, and charges generator overhead, Gamma_bEF proof overhead, row discovery U_use, row expansion X_use, and extension-line cost before deriving the SIZE contradiction.
- first unquarantined use: the least line u on a dependency path from a FormulaEval value to the final LB_N line at which the value is used by a non-quarantined inference or exported extension variable.
- syntactic quarantine: a verifier-visible tag forcing all descendants of the FormulaEval value to be ignored by final-line reconstruction until a charged exit certificate is present.

## Assumptions

- Circuit model is unrestricted nonuniform SIZE on N-bit inputs for H_N^SAT; the result is a same-model parser obstruction, not a P != NP lower bound.
- Length regime has M_N=N^{q+o(1)}, generator cost N^{rho+o(1)}, formula size polylog N, and proof parsing overhead E_pi with all o(1) terms uniform over the proof family.
- Psys_bEF^- rules already satisfy the bit-level Gamma_bEF induction; the only added rules are FormulaEval lines satisfying the visible first-use interface or quarantined delayed-exit normal form.
- Row discovery is advice-free: selector code, enumerator states, BDD/dDNNF witnesses, or full-scan loops are read from pi_{<u} and N, not from nonuniform hard-row choice.
- Influence means two surface occurrence completions agreeing on all charged rows and proof bits can change the FormulaEval value or a row parity used downstream.
- Quarantine is syntactic and prefix-checkable; a semantic promise that a hidden value will be explained later is not a valid transfer certificate.

## Equations

- Gamma_use_ledger: `\Gamma_{use}(\pi)=\Gamma_{bEF}(\pi)+U_{use}(\pi)+X_{use}(\pi)+Q_{exit}(\pi)`. Valid when: Valid when Psys_sym^time exposes first-use timestamps and quarantine exits so every charged FormulaEval dependency has a prefix-visible source in pi.
- parser_upper_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{use}(\pi)+O(E_\pi N)`. Valid when: Applies after the Gamma_bEF induction and every FormulaEval first-use dependency are simulated inside the same nonuniform SIZE model.
- subthreshold_falsifier: `N^{\rho+o(1)}+\Gamma_{use}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \pi\text{ is not a valid proof of }LB_N(1+\epsilon)`. Valid when: Valid when LB_N(1+epsilon) asserts an unrestricted SIZE lower bound for the same H_N^SAT family parsed from pi.
- row_expansion_charge: `X_{use}(\pi)\ge N^{1+o(1)}\,|K^{idx}_{use}(\pi)|`. Valid when: Requires same-theory occurrence expansion for each influential row before its first unquarantined use in the proof transcript.
- first_use_closure: `Infl(v)\subseteq K_{use}(\pi_{<u(v)})\ \lor\ \exists r\in Infl(v)\setminus K_{use}(\pi_{<u(v)})`. Valid when: Valid when u(v) is the first non-quarantined export of FormulaEval value v and influence is tested by occurrence completions.

## Attempted Derivation

- Define a dependency DAG on proof lines; FormulaEval nodes carry their syntactic row selector, semantic value placeholder, and a quarantine bit.
- For each FormulaEval value v, define u(v) as the first line where v or a descendant is used outside a syntactic quarantine cone on a path to the final LB_N line.
- Compute K_use by scanning prefixes: at line u, add rows output by visible enumerators, full scans, or RealSATInfluenceRealizer_N certificates already present in pi_{<u}; add X_use for same-theory occurrence expansions.
- Positive induction: Psys_bEF^- lines use the archived Gamma_bEF invariant; transparent FormulaEval exits are simulated by the charged row list; quarantined internal lines contribute no semantic value to final reconstruction until exit.
- Subthreshold transfer: the parsed generator plus charged transcript gives C(H_N^SAT)<=N^{rho+o(1)}+Gamma_use(pi)+O(E_pi N); if this is below N^{1+epsilon-o(1)}, the claimed LB_N proof is falsified in the same SIZE model.
- Negative induction: choose the least unquarantined use u with an influential row r absent from K_use(pi_{<u}); all earlier lines are identical under two occurrence completions agreeing on charged rows.
- Flip the private row or unread enable bit for r to change the FormulaEval value and downstream parity while preserving the visible transcript, contradicting parser soundness for that proof rule.

Blocking gap: The negative completion argument is a parser countermodel over surface occurrence tables. Full semantic SAT FormulaEval can escape only by a nonrelativizing, advice-free zero-latency RealSATInfluenceRealizer_N for the concrete rule.

## Falsifiers

- First-use falsifier: an influential FormulaEval row is absent from pi_{<u} when the value first exits quarantine.
- Unread-enable-bit falsifier: selector support is hidden behind a membership bit never expanded in the charged transcript.
- Advice-leakage falsifier: row selection uses nonuniform hard-row choice, ranking advice, or SAT-truth pruning rather than prefix-visible proof syntax.
- After-the-fact K_dag falsifier: support is listed only after the value has already influenced a non-quarantined LB_N line.
- Semantic-quarantine falsifier: the proof promises later explanation but lacks verifier-visible syntactic quarantine boundaries.
- Naturalness/advice boundary falsifier: making the realizer dense and polytime-decidable turns it into a large useful property rather than a sparse parser certificate.

## Learning

The valid timing invariant is first unquarantined use. Delayed support is harmless only inside syntactic quarantine and can be commuted to a charged exit; otherwise the first hidden influence is a concrete falsifier. This upgrades the FormulaEval boundary while preserving the non-claim that no main P vs NP lower bound follows.

## Gedanken Experiment Design Seed

- Need decision: `design-now as a falsifier probe for the first-use theorem`
- Rationale: The route is now blocked by a concrete timing question, not by abstract MCSP folklore: can a semantic FormulaEval value affect the proof before its influential rows are charged?
- Situation seed: A bounded-depth Tseitin/SAT self-reduction line computes a branch-pruned FormulaEval value for H_N^SAT, then an extension line exports the branch parity into the final LB_N transcript.
- Varied variable: latency ell between the semantic branch choice and the first unquarantined use or charged realizer exit
- Held-fixed controls: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, bit-explicit Psys_bEF^- parser and same unrestricted nonuniform SIZE target model, generator overhead N^{rho+o(1)} and row expansion cost N^{1+o(1)} per influential row, no advice, no nonuniform hard-row selector, and no semantic SAT-truth oracle inside the parser
- Expected observation: For ell=0 with explicit branch enumeration, Gamma_use pays B_N N^{1+o(1)} and the parser is valid. For ell>0 with the pruned value exported before support is charged, the unread branch acts as a private-row falsifier. For ell>0 inside syntactic quarantine, the cost commutes to the exit line.
- Transfer certificate needed: A zero-latency RealSATInfluenceRealizer_N or a verifier-visible quarantine-exit certificate listing all influential branch rows before any semantic value contributes to the final LB_N reconstruction.

## Next Experiment

Write the fixed-point pseudocode for K_use(pi): scan lines, maintain quarantined cones, compute first exits, enumerate charged rows, and instantiate it on one Tseitin self-reduction with explicit enumeration and one truth-pruned unread-branch countermodel.
