# cycle-0129

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For Psys_sym^{dag+declTSR,h}, complete declaration of every bounded Tseitin self-reduction child composes with the least prefix-closed reachable support cone. The resulting charged transcript Gamma_DTSR gives a valid same-model upper-bound falsifier for LB_N(1+epsilon) whenever N^{rho+o(1)}+Gamma_DTSR(pi)+O(E_pi N)<N^{1+epsilon-o(1)}.

## Definitions

- source object: beta-zero parity carrier H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), M_N=N^{q+o(1)}, polylog query length L_N=(log N)^d with d>1, and nonuniform SIZE source lower-bound claim LB_N(1+epsilon).
- target object: same-model nonuniform SIZE upper-bound falsifier for the claimed H_N^SAT lower bound, not a proof of NP not subset P/poly and not a general SAT lower bound.
- controlled interface: bit-explicit Psys_bEF^- plus transparent FormulaEval plus declared bounded TSR lines whose syntax lists parent pointers, row indices, child restriction codes, occurrence-neighborhood certificates, and enable bits before use.
- target-preserving condition: every influencing SAT row belongs to the least reachable support fixed point K_DTSR(pi), is expanded in the same SAT-occurrence theory, is charged in Gamma_DTSR, and no row selection is supplied as hidden semantic advice.

## Assumptions

- Circuit model is nonuniform Boolean SIZE over the same input length N for both the source carrier and the constructed falsifier circuit.
- Length regime has M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, query length L_N=(log N)^d with d>1, and beta=0 target-query exponent.
- The bounded SR_h normal form from the bit-explicit parser is already included in Gamma_bEF(pi), with B_SR(pi)<=N^{q+eta+tau+o(1)} when its local neighborhoods are declared.
- A declared TSR line has D_TSR(pi)=N^{kappa+o(1)} active parent rows and at most C_TSR(N)=N^{theta+o(1)} declared child restrictions per active row; each child row has a verifier-visible occurrence expansion of size N^{1+o(1)}.
- Uniformity is advice-free at the parser level: N and pi determine the enumerator for K_DTSR(pi), the child-row encodings, and the same-theory row expansions.

## Equations

- carrier: `H_N^{\mathrm{SAT}}(x)=\bigoplus_{j\le M_N}\mathrm{SAT}(G_N(x,j)),\quad M_N=N^{q+o(1)}`. Valid when: Valid when the branch is restricted to beta-zero parity carriers with generated polylogarithmic SAT queries and fixed source length N.
- least_support_fixed_point: `K_{t+1}=K_t\cup \mathrm{Par}(K_t)\cup \mathrm{Supp}_{FE}(K_t)\cup \mathrm{Child}_{TSR}(K_t),\quad K_{DTSR}=\mathrm{lfp}(K_0)`. Valid when: Applies after every proof line exposes parent pointers and declared child-row encodings before the line can influence the final LB_N assertion.
- declared_tsr_charge: `X_{TSR}(\pi)\le N^{1+o(1)}D_{TSR}(\pi)C_{TSR}(N)=N^{1+\kappa+\theta+o(1)}`. Valid when: Requires declared TSR lines to list all restriction children and their occurrence-neighborhood expansions with no semantic branch pruning.
- charged_transcript: `\Gamma_{DTSR}(\pi)=\Gamma_{bEF}(\pi)+U(K_{DTSR})+X_{FE}(K_{DTSR})+X_{TSR}(\pi)`. Valid when: Valid when EF dependencies, FormulaEval support, and declared TSR child rows are closed under the least reachable support fixed point.
- source_falsifier_window: `N^{\rho+o(1)}+\Gamma_{DTSR}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Applies after the line induction constructs an explicit same-model circuit for H_N and sparse row errors are equality patched.

## Attempted Derivation

- Fix the source carrier H_N^SAT with M_N=N^{q+o(1)}, L_N=(log N)^d, d>1, and beta=0. Fix Psys_sym^{dag+declTSR,h} over bit-explicit EF lines, transparent FormulaEval lines, and declared TSR lines.
- For each proof line record verifier bit fields: kind, line index, parent pointers, source row a, formula pointer p, restriction code z, child row code r=(a,p,z), enable bit e_r, and an explicit occurrence-neighborhood list Occ(r).
- Initialize K_0 from the final LB_N assertion and compute K_DTSR by the finite fixed point K<-K union parents union FormulaEval supports union declared TSR children. This is implementable because every addition is syntactically listed or full-scan charged.
- Extend the prior Gamma_bEF line induction. EF and SATeq lines use the existing dependency and quotient-link charges; bounded SR_h lines use B_SR(pi); transparent FormulaEval lines use U(K)+X_FE(K); declared TSR lines add exactly N^{1+o(1)} per declared child occurrence expansion.
- For a declared TSR inference, the local verifier recomputes the Tseitin/restriction map on Occ(r), checks child-parent consistency, and charges the child row before the rule can feed any later line. Thus the induction invariant is prefix-closed under later symbolic use.
- At the final LB_N line the parser yields a nonuniform circuit for H_N of size at most N^{rho+o(1)}+Gamma_DTSR(pi)+O(E_pi N). If this is below N^{1+epsilon-o(1)}, the claimed source lower bound is falsified in the same SIZE model.
- For hidden branch pruning, choose the first reachable child row r* not in K_vis. Two row-label worlds agreeing on K_vis and differing at r* pass the same visible transcript while changing a reachable parity bit, so surface occurrence parsing is invalid without RealSATInfluenceRealizer_N^arb.

Blocking gap: No blocking gap for the restricted complete-child declared TSR rule case. The full semantic FormulaEval/TSR system remains blocked exactly at RealSATInfluenceRealizer_N^arb, which must uniformly list and charge semantically influencing rows before use.

## Falsifiers

- First-unlisted-child private-row or unread-enable-bit falsifier for hidden TSR branch pruning.
- Threshold-collapse falsifier kappa+theta>=epsilon: declared TSR expansion is too large to refute LB_N by a subthreshold parser circuit.
- q<epsilon sparse-support falsifier: too few reachable rows allow explicit enumeration and equality patching.
- Nonuniform leakage falsifier: a row selector or semantic pruning decision supplied as advice instead of verifier-visible syntax invalidates Gamma_DTSR.
- Positive-beta substitution falsifier remains quarantined: any black-box target-query exponent beta>0 gives the transfer cap q+beta c+o(1).

## Learning

Cycle 129 turns declared bounded TSR from a semantic-warning slogan into a line-induction rule case for the least support theorem. Complete child declaration adds exactly N^{1+kappa+theta+o(1)} to Gamma_DTSR and is valid below kappa+theta<epsilon; hidden branch pruning is refuted by a first-unlisted-child falsifier unless a nonrelativizing real-SAT influence realizer is supplied.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the declared-TSR threshold.`
- Rationale: The branch has a concrete theorem boundary; varying only the declared child exponent tests whether the new rule case genuinely preserves the subthreshold parser-to-circuit transfer.
- Situation seed: Fix H_N^SAT with M_N=N^{q+o(1)}, q=(1+epsilon)/2, rho<1+epsilon, L_N=(log N)^d for d>1, and a Psys_sym^{dag+declTSR,h} proof using D_TSR=N^{kappa+o(1)} active TSR parent rows, each declaring N^{theta+o(1)} restriction children.
- Varied variable: theta, the exponent for declared TSR children per active parent row.
- Held-fixed controls: beta=0 polylogarithmic target-query length and the same nonuniform SIZE source model., Complete child declarations with occurrence-neighborhood lists and no hidden semantic branch advice., Fixed q, rho, epsilon, kappa, and sparse error budget E_pi<N^{epsilon-o(1)}., Least-support fixed-point computation K_DTSR and same-theory row expansion rules.
- Expected observation: For theta<epsilon-kappa the declared-TSR charge stays subthreshold and the parser yields a valid falsifier circuit; for theta>=epsilon-kappa the route loses this falsifier even though the rule remains transparent.
- Transfer certificate needed: A referee-checkable K_DTSR fixed-point trace plus a line-by-line Gamma_DTSR ledger proving X_TSR=N^{1+kappa+theta+o(1)} and excluding hidden row advice.

## Next Experiment

Write the paper-ready L129 sublemma proof: give pseudocode for K_DTSR fixed-point enumeration, a table of declared TSR bit fields, the local verifier for child occurrence neighborhoods, and the two-world first-unlisted-child countermodel; then run the live inference-quality packet validation.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Annotated bounded-SR_h FormulaEval is a TransparentRowSupport_N instance: if every SR_h line lists all row children and occurrence neighborhoods, then same-theory prefix splicing gives a charged transcript with row-equivalent cost N^{tau+eta+o(1)} and bit debt N^{1+tau+eta+o(1)}. Subthreshold charge yields a same-model SIZE upper-bound falsifier to LB_N(1+epsilon).

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with N=2^n, M_N=N^{q+o(1)}, size(G_N)=N^{rho+o(1)}, and a claimed Psys_sym^{aSR_h} proof pi of LB_N(1+epsilon).
- target object: a same-length nonuniform Boolean SIZE upper bound for H_N^SAT below N^{1+epsilon-o(1)}, used only as a falsifier to the claimed proof-system lower-bound transfer.
- controlled interface: every bounded-SR_h FormulaEval line exposes line id, parent ids, row index, touched child-row list L(a), occurrence-neighborhood hashes, selector code, and a same-theory row-expansion template.
- target-preserving condition: the deterministic no-advice parser prefix-splices each listed row into bEF with fresh extension variables and charges N per row, preserving the nonuniform SIZE target and the beta-zero length regime.
- row-equivalent support: S_hat_aSRh(pi)=S_hat_bEF(pi)+|R_SRh(pi)|+E_rest+ceil(U_rest/N), where R_SRh is the union of listed child rows reachable from the final LB line.
- bit-expansion debt: Gamma_aSRh(pi)=N*S_hat_aSRh(pi)+polylog bookkeeping, excluding the generator circuit cost N^{rho+o(1)}.

## Assumptions

- Model is nonuniform Boolean SIZE over the truth table length N of the x input; the proof system is bit-explicit bEF plus annotated bounded-SR_h FormulaEval.
- Regime is N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, h=N^{eta+o(1)}, and size(G_N)=N^{rho+o(1)} with rho<1+epsilon.
- Uniformity condition is deterministic no-advice parsing from (N,pi); row names and occurrence neighborhoods are verifier-visible and have O(log M_N)+polylog(N) encodings.
- Same-theory condition is prefix splicing: row-expanded FormulaEval material is inserted before its use with fresh extension variables and without semantic SAT oracle calls.
- Naturalness boundary: the lemma is a parser/falsifier theorem; it naturalizes only if the transcript extraction becomes a large constructive useful truth-table property.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j=1}^{M_N} SAT(G_N(x,j))`. Valid when: Valid when the beta-zero SAT-parity source carrier is fixed with visible generator G_N and all row indices range over M_N=N^{q+o(1)}.
- row_touch_bound: `|R_{SR_h}(\pi)|\le \sum_{a\in \pi}|L(a)|\le |\pi|h(\log N)^c=N^{\tau+\eta+o(1)}`. Valid when: Applies when every annotated SR_h line has at most h=N^{eta+o(1)} visible child rows and the proof length is |pi|=N^{tau+o(1)}.
- transcript_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+N\widehat S_{aSR_h}(\pi)+N^{o(1)}`. Valid when: Requires same-theory prefix splicing, no hidden row advice, and a nonuniform circuit construction that hardwires only the charged transcript.
- subthreshold_falsifier: `\widehat S_{aSR_h}(\pi)<N^{\epsilon-o(1)}\Rightarrow C(H_N^{SAT})<N^{1+\epsilon-o(1)}`. Valid when: Valid when rho<1+epsilon and all non-SRh debts are lower than the claimed N^{1+epsilon} lower-bound threshold.

## Attempted Derivation

- Normalize each annotated SR_h FormulaEval line to a tuple (line_id,type,parent_ids,row_j,L(a),occ_hashes,selector_hash,template_hash). The verifier checks parent order, row-index ranges, and that |L(a)|<=h.
- Define K_0 as the final LB_N line support. Run a backward worklist: when an annotated SR_h line enters K, add its parents and every row in L(a); when a bEF line enters K, add only its ordinary bit-DAG parents.
- The worklist is prefix-closed because every listed row expansion is required to occur earlier with fresh extension variables. Thus later lines never depend on an unspliced FormulaEval semantic atom.
- Charge each added SR_h child row by one row-equivalent unit and by N bit-expansion units. Summing over |pi| lines gives |R_SRh(pi)|<=|pi|h polylog(N)=N^{tau+eta+o(1)}.
- Splice the row-expanded bEF derivations in line order. The old Gamma_bEF induction remains valid, and the only new term is N|R_SRh(pi)| plus lower-order encoding overhead.
- Build the same-model nonuniform circuit for H_N^SAT from the generator circuit and the charged transcript. If N^{rho}+Gamma_aSRh<N^{1+epsilon-o(1)}, this is a falsifier to any accepted proof asserting LB_N(1+epsilon).
- For unannotated semantic SR_h, choose the first influencing child row not in K_vis. Flip only that row while preserving all displayed bits; the transcript remains accepted but the parity carrier changes, proving surface parsing invalid.

Blocking gap: No blocking gap remains for annotated bounded-SR_h under the stated bit fields. The remaining gap is exactly RealSATInfluenceRealizer_N for arbitrary unannotated semantic FormulaEval rules.

## Falsifiers

- First omitted child-row falsifier: an SR_h semantic line depends on row j* absent from the visible support list, so two proofs have identical parsed transcripts but opposite carrier parity.
- Unread-enable-bit falsifier: a hidden enable bit selects a private row after the parser has committed to K_vis, defeating occurrence-only FormulaEval completion.
- q<epsilon source-ceiling falsifier: the beta-zero carrier has C(H_N^SAT)<=N^{1+q+o(1)}, so LB_N(1+epsilon) is invalid before proof-system transfer is considered.
- Same-theory-splice falsifier: if row expansions require a semantic SAT oracle rather than bEF material with fresh extension variables, Gamma_aSRh is not a valid target-preserving charge.
- Naturalness falsifier: if the extracted transcript becomes a polynomial-density constructive property useful against the exact SIZE class, the route faces PRF tension rather than escaping by proof syntax.

## Learning

Cycle 129 upgrades the annotated bounded-SR_h result into a TransparentRowSupport_N instance with auditable bit fields and a derived charge: row-equivalent N^{tau+eta+o(1)} and bit debt N^{1+tau+eta+o(1)}. Live packet: source_statement=short Psys_sym^{aSR_h} proof pi of LB_N(1+epsilon) for H_N^SAT; target_statement=same-model SIZE upper-bound falsifier or forced row-equivalent support; model_context=nonuniform Boolean SIZE, beta-zero SAT-parity carrier, bEF plus annotated bounded-SR_h FormulaEval, simulation/extraction rather than many-one reduction; quantifier_context=N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, h=N^{eta+o(1)}, size(G_N)=N^{rho+o(1)}, rho<1+epsilon, deterministic no-advice parser; derivation_status=restricted theorem derived, unannotated semantic FormulaEval blocked at RealSATInfluenceRealizer_N; reviewer_findings=valid only with visible row-touch completeness and same-theory prefix splicing, private-row falsifier blocks occurrence-only lifts, and there is no claim toward P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe_and_threshold_test`
- Rationale: The branch needs a concrete check that annotated SR_h support is genuinely charged, while unannotated semantic influence is not silently treated as valid occurrence support.
- Situation seed: Take H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with an annotated bounded-SR_h proof pi; then create a semantic variant pi' where one child row j* is selected by an unread enable bit but omitted from L(a).
- Varied variable: eta in the row-neighborhood bound h=N^{eta+o(1)}, with tau fixed so the threshold tau+eta crosses epsilon.
- Held-fixed controls: N=2^n and M_N=N^{q+o(1)} for the beta-zero SAT-parity carrier., Generator size N^{rho+o(1)} with rho<1+epsilon., Nonuniform Boolean SIZE target and same-model LB_N(1+epsilon) interpretation., Deterministic no-advice parser and same-theory bEF prefix splicing for visible rows.
- Expected observation: For tau+eta<epsilon, the annotated proof expands to a subthreshold circuit and hence falsifies LB_N(1+epsilon); in the semantic variant, the private row creates bisimilar transcripts with different carrier parity.
- Transfer certificate needed: A RowTouchList completeness certificate plus prefix-splice theorem is required before the intuition can affect proof obligations; otherwise the private-row construction quarantines the semantic rule.

## Next Experiment

Attack RealSATInfluenceRealizer_N for one unannotated semantic rule: Tseitin-extension equality plus bounded self-reduction. Either produce an advice-free row-touch realizer with Gamma ledger entry R_N, or instantiate the first omitted semantic inference as a private-row countermodel.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

QuarantineExitTransparentSupport_N: In a bit-explicit Psys_sym^Q proof, delayed FormulaEval support is valid only inside a sealed syntactic quarantine. If every row that can influence an unquarantined line is enumerated and expanded either before its first unquarantined use or at a sealed exit before any external dependency, then the bEF parser line induction extends with Gamma_QE and yields the same-model upper-bound falsifier for LB_N(1+epsilon). If this prefix/exit condition fails, the first hidden influence gives a private-row or unread-enable-bit countermodel.

## Definitions

- source object: a bit-explicit Psys_sym^Q proof pi of a beta-zero SAT-XOR lower-bound claim for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with FormulaEval lines tagged unquarantined, quarantined-internal, or quarantine-exit.
- target object: a same-theory nonuniform SIZE upper-bound simulation for H_N^SAT and a finite hidden-support countermodel when the simulation interface is violated.
- controlled interface: first-unquarantined-use row support K_QE(pi), computed from proof prefix pi_{<t} or from a syntactic quarantine exit before any external dependency.
- target-preserving condition: all influential FormulaEval rows are advice-free, prefix-visible at first unquarantined use, expanded in the same SAT occurrence theory, and charged before deriving the target lower-bound line.
- bridge observable: Gamma_QE(pi) equals the old bit-explicit Gamma_bEF ledger plus enumerator cost, row-expansion cost, and explicit scan cost for FormulaEval support.
- quarantine semantics: internal semantic lines may depend on delayed support only if no exported line, selector bit, parity bit, or proof parent outside the box reads them before the charged exit.

## Assumptions

- Model: Psys_bEF^- parser rules are already in bounded-SR_h normal form with eta/tau costs charged in Gamma_bEF(pi).
- Regime: M_N=N^{q+o(1)}, each generated SAT instance G_N(x,j) has length N^{1+o(1)} or the declared row-expansion unit, and generator overhead is N^{rho+o(1)}.
- Uniformity: row enumerators, quarantine-exit lists, selector codes, and occurrence expansions are computed from N and proof bits, with no advice-selected hard row or semantic SAT-truth advice.
- Same-theory condition: the parser expands the same SAT occurrences used by the proof rule, not a different oracle or a nonrelativizing semantic shortcut.
- First-use condition: every unquarantined FormulaEval dependency has a charged support certificate in the prefix before the dependent line is checked.
- Sealed-box condition: a quarantined subderivation exports nothing used by the final proof DAG until its exit line has listed and charged all rows that can alter any exported value.
- Non-claim: this is a parser/falsifier theorem for the FormulaEval route, not a proof of P != NP or of an unrestricted circuit lower bound.

## Equations

- SAT-XOR carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)}`. Valid when: Valid when the beta-zero carrier family and generator length regime are fixed before the proof-system simulation begins.
- QE support cone: `K_{QE}(\pi)=\bigcup_{t\in U(\pi)} R_t\ \cup\ \bigcup_{e\in Ex(\pi)} R_e`. Valid when: Valid when U(pi) ranges over unquarantined first uses and Ex(pi) ranges over sealed exits with prefix-visible row lists.
- QE ledger: `\Gamma_{QE}(\pi)=\Gamma_{bEF}(\pi)+\sum_t U_t+N^{1+o(1)}|K_{QE}(\pi)|+F_{scan}N^{1+q+o(1)}`. Valid when: Applies after every FormulaEval row is either enumerated with cost U_t or paid by an explicit full scan.
- same-model simulation: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{QE}(\pi)+O(E_\pi N^{1+o(1)})`. Valid when: Requires the target-preserving same-theory expansion and the bounded-SR_h line induction for all non-FormulaEval rules.
- LB falsifier threshold: `\max\{\rho,\gamma_{QE},1+e_\pi\}<1+\epsilon\ \Longrightarrow\ \neg LB_N(1+\epsilon)`. Valid when: Valid when Gamma_QE(pi)=N^{gamma_QE+o(1)} and proof-overhead exponent e_pi is measured in the same SIZE model.

## Attempted Derivation

- Define a proof DAG order and mark each FormulaEval occurrence as unquarantined, quarantined-internal, or exit. For the final LB_N line, traverse parent pointers backward and build K_QE by adding R_t at each unquarantined first use and R_e at each sealed exit.
- For ordinary bEF and bounded-SR_h lines, reuse the established Gap98-SRhNormalForm induction and add their eta/tau contribution to Gamma_bEF(pi).
- For an unquarantined FormulaEval line t, require pi_{<t} to contain either an advice-free enumerator for every influencing row or a full-scan flag. Add U_t plus N^{1+o(1)}|R_t| or F_scan N^{1+q+o(1)} to the ledger.
- For a quarantined block, check that no external parent pointer, selector output, extension variable, or parity line reads an internal semantic value before the exit. Then commute all semantic dependence to the exit certificate and charge the union R_e there.
- Induct on external proof lines: after each line, every value that may affect the visible transcript is a function of generator bits, bEF local neighborhoods, and charged rows in K_QE. Thus a circuit can hardwire the proof skeleton and compute H_N^SAT with cost N^{rho+o(1)}+Gamma_QE(pi)+O(E_pi N^{1+o(1)}).
- Derive the falsifier inequality: if this cost is below N^{1+epsilon-o(1)}, the proof cannot validly certify LB_N(1+epsilon) in the same nonuniform SIZE model.
- If a minimal line violates prefix or exit visibility, freeze all visible bits before that line and flip the first hidden influential SAT row or enable bit. The transcript remains parser-valid but the semantic value changes, giving the private-row countermodel.

Blocking gap: The restricted derivation is complete for sealed syntactic quarantines. The only remaining full-system gap is ZeroLatencyRealSATInfluenceRealizer_N: real semantic SAT pruning must uniformly list and charge all influencing rows before first external use, or it remains a semantic-oracle escape.

## Falsifiers

- falsifier: an unquarantined FormulaEval line whose semantic value depends on a row absent from K_QE(pi_{<t}).
- falsifier: a quarantine box exporting a selector bit, parity bit, or extension variable before the charged exit line.
- falsifier: an exit row list generated by SAT-truth pruning or nonuniform advice rather than proof-visible syntax.
- falsifier: row batching that claims less than N^{1+o(1)} per SAT row without a same-theory expansion proof.
- valid counterpressure: if q<epsilon and every row is scanned, Gamma_QE is still subthreshold, so the claimed LB_N cannot be certified by this transparent proof route.

## Learning

The new contribution is a timing normal form: delayed FormulaEval support is harmless exactly when it is sealed inside syntactic quarantine and charged at exit before any external dependency. Otherwise the first hidden semantic influence is a same-theory finite falsifier. This upgrades the paper parser obstruction without making any main P vs NP claim.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and proof-audit example.`
- Rationale: The abstract timing invariant is settled; the remaining risk is whether a concrete semantic self-reduction can hide SAT-truth branch pruning while pretending to be a transparent FormulaEval line.
- Situation seed: A Psys_sym^Q proof for H_N^SAT using a Tseitin/self-reduction FormulaEval box. Inside the box, branch rows are generated by explicit syntactic enumeration, except one variant prunes branches using their actual SAT truth before the exit certificate.
- Varied variable: prefix-latency mode lambda in {0, sealed_exit, unsealed_delay}: zero-latency listed rows, delayed rows charged at a sealed exit, or delayed rows used externally before charge.
- Held-fixed controls: M_N=N^{q+o(1)} and generator overhead N^{rho+o(1)}., Same SAT occurrence theory and same nonuniform SIZE target model., No advice-selected rows and no external SAT oracle beyond declared FormulaEval syntax., Bounded-SR_h parser costs eta and tau already included in Gamma_bEF.
- Expected observation: Zero-latency and sealed-exit modes satisfy the Gamma_QE ledger. The unsealed-delay mode exposes a private branch whose SAT value can be flipped while all prefix-visible bits remain fixed, so it is not a valid transparent support certificate.
- Transfer certificate needed: A formal QuarantineExitNormalForm certificate: sealed-box parent-pointer check, prefix-visible row enumerator at exit, same-theory row expansions, and a proof that no exported value depends on uncharged semantic support.

## Next Experiment

Instantiate L129 on the Tseitin/self-reduction FormulaEval rule: compute the explicit branch enumerator charge U_e, row expansion X_e, verify sealed-box parent pointers, and write the unsealed truth-pruned private-branch countermodel.
