# cycle-0130

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Declared bounded Tseitin self-reduction lines are absorbed by the least prefix-closed transparent support parser. If a Psys_sym^{dag,DTSR} proof pi of LB_N(1+epsilon) exposes every FormulaEval influence and every TSR restriction child, then the parser line induction yields a same-model SIZE upper bound for H_N^{SAT}; any subthreshold Gamma_DTSR(pi) is therefore a valid falsifier of that source lower-bound certificate.

## Definitions

- source object: the beta-zero parity carrier H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and SAT instances of length L_N=(log N)^d.
- target object: a same-nonuniform-SIZE upper-bound falsifier for a claimed source statement LB_N(1+epsilon), not a proof of P != NP or NP not subset P/poly.
- controlled interface: Psys_sym^{dag,DTSR} proofs whose bit-explicit EF, SATeq, bounded-SR_h, FormulaEval, and declared TSR lines expose parent pointers, row indices, row enumerators, and complete child-restriction lists.
- target-preserving condition: all influencing rows are uniformly listed without advice, expanded inside the same SAT-row theory, beta=0 is preserved by polylog query length, and Gamma_DTSR stays below the N^{1+epsilon} lower-bound threshold.
- DTSR rule schema: for each active parent formula row a, the proof lists all restriction children b in Child(a) used in the Tseitin/self-reduction identity before any semantic pruning is applied.
- least support object: K_DTSR(pi) is the least fixed point obtained from final LB_N rows by repeatedly adding proof parents, FormulaEval dependency rows, SATeq links, bounded-SR leaves, and declared TSR children.

## Assumptions

- source_statement: pi purports to certify that H_N^{SAT} has no SIZE circuits of size N^{1+epsilon-o(1)} in the same nonuniform circuit model used by the parser upper bound.
- target_statement: the theorem constructs a circuit for H_N^{SAT} of size below N^{1+epsilon-o(1)} when the charged ledger is subthreshold, thereby refuting the certificate rather than separating complexity classes.
- model_context: source carrier is beta-zero parity magnification over SAT rows, proof model is Psys_sym^{dag,DTSR}, target class is nonuniform SIZE, and the simulation is parser-to-circuit compilation.
- quantifier_context: N ranges over valid carrier lengths, q,rho,kappa,theta,epsilon are fixed constants, d>1 is fixed, all o(1) terms are uniform over proofs of polynomially bounded length, and no row-selection advice is allowed.
- DTSR declaration regime: active row descriptors are uniformly enumerable in A_N=N^{theta+o(1)} total positions, each active descriptor has fanout F_N=N^{kappa+o(1)}, and each child row has a bit-level certificate of the restricted formula.
- same-theory condition: every expanded FormulaEval or TSR child is represented as an ordinary row of the same SAT-row proof language, so the final compiled circuit does not query a stronger semantic oracle.
- barrier status: the positive theorem is relativizing only for exposed rows and deliberately does not cover hidden semantic pruning; the escape RealSATInfluenceRealizer_N^{arb} would have to be nonrelativizing and advice-free.

## Equations

- carrier_parameters: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad |G_N|=N^{\rho+o(1)},\quad L_N=(\log N)^d`. Valid when: Valid when the source carrier is the beta-zero generated parity carrier with uniformly computable generator and fixed polylogarithmic SAT row length.
- least_fixed_point: `K_{t+1}=K_t\cup Par(K_t)\cup FE(K_t)\cup SR_h(K_t)\cup DTSR_{decl}(K_t),\quad K_{DTSR}(\pi)=\bigcup_{t\le |\pi|}K_t`. Valid when: Applies when every proof line has verifier-visible parent pointers and every semantic dependency class is either empty or listed as a charged row set.
- ledger: `\Gamma_{DTSR}(\pi)=\Gamma_{bEF}(\pi)+U(K_{DTSR})+X_{FE}(K_{DTSR})+X_{DTSR}(K_{DTSR})+O(E_\pi N)`. Valid when: Valid when the parser induction charges bit-explicit proof dependencies, FormulaEval enumeration, declared TSR expansions, and residual sparse-row patching in the same SIZE model.
- declared_tsr_charge: `X_{DTSR}(K_{DTSR})\le N\cdot A_N\cdot F_N\cdot L_N^{O(1)}=N^{1+\theta+\kappa+o(1)}`. Valid when: Requires the declared TSR schema where A_N active row descriptors and F_N restriction children are uniformly listed before semantic use.
- parser_upper_bound: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{DTSR}(\pi)+O(E_\pi N)`. Valid when: Applies after the line induction compiles every charged support row into a same-theory circuit and no hidden semantic row remains reachable.
- subthreshold_falsifier: `\rho<1+\epsilon\ \wedge\ \Gamma_{DTSR}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Valid when LB_N is a same-model N^{1+epsilon-o(1)} circuit lower-bound claim for the carrier H_N^{SAT}.
- declared_tsr_window: `\theta+\kappa<\epsilon \Rightarrow X_{DTSR}(K_{DTSR})=o(N^{1+\epsilon})`. Valid when: Applies in the fixed-exponent regime where declared TSR fanout and active-row exponents are independent of N and all polylog factors are absorbed.

## Attempted Derivation

- Define DTSR-TransparentSupport_N: every rule line has a bit-level tag, parent line numbers, row-index fields, local formula identifiers, enumerator code, and for each active TSR row a complete list of restriction-child descriptors before the line is used.
- Compute K_DTSR(pi) by a monotone fixed point from the final LB_N line: add proof parents, EF extension support, SATeq links, bounded-SR_h leaves, FormulaEval dependencies, and declared TSR children until no new row descriptor appears.
- Maintain induction invariant I(l): after processing line l, every row label that can affect l is in K_DTSR restricted to the prefix, and the compiled same-model circuit cost is at most the corresponding prefix ledger.
- Base cases are inherited from the bit-explicit Psys_bEF^- parser: literal rows, EF definitions, SATeq quotient links, and bounded-SR_h leaves contribute exactly their Gamma_bEF charges.
- FormulaEval lines use either a visible enumerator charge U(K) or a full-scan charge, then pay same-theory row-expansion X_FE(K); hidden FormulaEval is not admitted.
- For a declared TSR line, enumerate A_N active descriptors and F_N children per descriptor, write each restricted child as an ordinary SAT row, and charge N A_N F_N L_N^{O(1)}=N^{1+theta+kappa+o(1)}.
- The induction composes because later symbolic uses can reach only rows already in the prefix-closed fixed point; hence no last-unsafe-line remains under the declared interface.
- At the final LB_N line, the compiled circuit plus residual equality patches has size N^{rho+o(1)}+Gamma_DTSR(pi)+O(E_pi N).
- If rho<1+epsilon and the ledger is below N^{1+epsilon-o(1)}, the constructed circuit contradicts the claimed source lower bound LB_N(1+epsilon), giving a route-level falsifier.

Blocking gap: Full semantic branch pruning remains blocked at RealSATInfluenceRealizer_N^{arb}: the derivation does not show that real SAT semantics can uniformly list all influential pruned children without advice and before use.

## Falsifiers

- first-unlisted-child private-row falsifier for hidden TSR pruning
- unread-enable-bit falsifier for FormulaEval influence not in K_DTSR(pi)
- threshold-collapse falsifier when rho or Gamma_DTSR reaches N^{1+epsilon-o(1)}
- nonuniform row-selection advice falsifier for claimed transparent enumeration
- positive-beta black-box substitution falsifier q+beta*c against all-exponent target transfer

## Learning

Cycle 130 closes a real proof-delivery subcase: declared bounded TSR is not merely compatible with transparent support but is an explicit fixed-point rule with charge N^{1+kappa+theta+o(1)}. The exact boundary is now complete declaration versus first-unlisted-child falsifier; full semantic pruning remains open only through the nonrelativizing RealSATInfluenceRealizer_N^{arb}.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The branch no longer needs another abstract support slogan; it needs to test whether declared TSR closure is genuinely minimal and whether one omitted child invalidates the parser theorem.
- Situation seed: Construct a Psys_sym^{dag,DTSR} transcript for the beta-zero parity carrier where one Tseitin self-reduction line has A_N=N^{theta} active rows and F_N=N^{kappa} restriction children, then create a variant transcript with exactly one downstream influential child hidden behind an unread enable bit.
- Varied variable: the hidden-child budget h_N, varying from h_N=0 complete declaration to h_N=1 first-unlisted-child omission while holding kappa and theta fixed.
- Held-fixed controls: M_N=N^{q+o(1)}, L_N=(log N)^d, and generator overhead N^{rho+o(1)} remain fixed with beta=0., The proof checker, visible parent pointers, public row enumerator, and same-theory row-expansion syntax are identical in both transcripts., No nonuniform SAT-truth advice is allowed in the selector or child-list code., The target lower-bound threshold LB_N(1+epsilon) and residual patching budget O(E_pi N) are unchanged.
- Expected observation: At h_N=0 the line induction charges N^{1+kappa+theta+o(1)} and is valid below kappa+theta<epsilon; at h_N=1 two visible transcripts agree while the final parity can flip, so hidden pruning is a concrete falsifier.
- Transfer certificate needed: A proof-quality certificate must show either a complete advice-free child enumerator included in K_DTSR(pi), or a nonrelativizing RealSATInfluenceRealizer_N^{arb} that derives the omitted child influence as a charged same-theory row before semantic use.

## Next Experiment

Run the bit-field audit for one concrete DTSR verifier line: list parent row id, active descriptor id, restriction mask, child row id, Tseitin extension map, local identity tag, and downstream use pointer; verify that K_DTSR reaches every used child and compute the exact theta+kappa ledger for the example.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

TransparentRowSupport_N is a sufficient and finite interface for FormulaEval in the beta-zero SAT-parity proof route: every Psys_sym^TRS proof pi of LB_N(1+epsilon) yields a same-theory row-expanded bEF transcript of charge Gamma_TRS(pi); if the charge is subthreshold, it gives a same-model SIZE upper-bound falsifier to the claimed lower bound, otherwise it forces row-equivalent support at least N^{epsilon-o(1)}.

## Definitions

- source object: a Psys_sym^TRS proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), with N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, and size(G_N)=N^{rho+o(1)}.
- target object: a nonuniform Boolean SIZE_N upper bound for H_N^SAT in the same length regime, contradicting the asserted source lower bound when the derived size is below N^{1+epsilon-o(1)}.
- controlled interface: TransparentRowSupport_N, consisting of visible selector code, advice-free RowSet enumeration or full scan charge, influence-closed reachable row set K_idx(pi), same-theory row expansion, prefix-scoped fresh extension variables, and no hidden semantic row advice.
- target-preserving condition: every FormulaEval line that can affect the final LB_N line has its influencing rows listed or fully scanned and charged before use, so the parser simulates the original proof rather than adding semantic oracle power.
- Gamma_bEF(pi) is the already validated bit-explicit bEF/SATeq/bounded-SR_h charge.
- U_N(pi) is visible enumeration debt for row selectors and cover certificates.
- X_N(pi) is same-theory row-expansion debt, including N times the charged row count plus local link and verifier bits.
- K_idx(pi) is the least prefix-closed reachable support cone computed from the final lower-bound line through visible FormulaEval dependencies.

## Assumptions

- Model: nonuniform Boolean circuits for H_N^SAT on N input bits, with proof-to-circuit extraction rather than many-one reduction.
- Regime: rho<1+epsilon and all exponents q,tau,eta,rho are measured on the same N=2^n family.
- Uniformity: the parser receives N, pi, and proof-visible selector codes only; no advice string may name rows or SAT values.
- Same-theory condition: every FormulaEval expansion is spliced into the same bEF-style theory with fresh prefix-scoped extension variables and line-order preservation.
- Soundness condition: LB_N(1+epsilon) asserts C_SIZE_N(H_N^SAT)>N^{1+epsilon-o(1)} in exactly the circuit model used by the extracted upper bound.
- Barrier status: the object is proof-mediated and not automatically a natural property; if it induces a dense constructive truth-table property, the natural-proofs falsifier audit applies.

## Equations

- beta_zero_lengths: `M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, size(G_N)=N^{rho+o(1)}`. Valid when: Valid when the length family is beta-zero with N=2^n and all exponent parameters are measured along the same subsequence.
- carrier: `H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j))`. Valid when: Applies when the source carrier is the beta-zero SAT-parity construction and G_N is fixed uniformly without advice.
- transparent_charge: `Gamma_TRS(pi)=Gamma_bEF(pi)+U_N(pi)+X_N(pi)`. Valid when: Valid when every FormulaEval line satisfies TransparentRowSupport_N and all reachable influencing rows are enumerated, scanned, or row-expanded before use.
- parser_upper_bound: `C_SIZE_N(H_N^SAT) <= N^{rho+o(1)} + Gamma_TRS(pi) + polylog(N)`. Valid when: Requires the same-theory prefix splice and the already validated bEF parser so the extracted circuit computes the identical H_N^SAT.
- subthreshold_falsifier: `N^{rho+o(1)}+Gamma_TRS(pi)<N^{1+epsilon-o(1)} => not LB_N(1+epsilon)`. Valid when: Valid when LB_N is stated as a lower bound against the same nonuniform SIZE_N model used by the extracted circuit.
- forced_support: `widehat_S_eff(pi):=|K_idx(pi)|+ceil(U_N(pi)/N)+Gamma_bEF(pi)/N >= N^{epsilon-o(1)}`. Valid when: Applies after the subthreshold upper-bound falsifier is excluded and row-expansion debt is normalized into row-equivalent support units.
- q_density_corollary: `if U_N+Gamma_bEF=o(N^{1+epsilon}) then |K_idx(pi)|/M_N >= N^{epsilon-q-o(1)}`. Valid when: Requires M_N=N^{q+o(1)} and lower-order non-FormulaEval debts, so visible FormulaEval rows carry the forced support.

## Attempted Derivation

- Define K_idx(pi) by a backward worklist from the final LB_N line: add parent proof lines, displayed FormulaEval dependencies, selector rows, row-cover children, and extension variables until a prefix-closed fixed point is reached.
- For each transparent FormulaEval line A, run its visible enumerator or row-cover verifier. Charge U_A for finding rows and X_A for replacing A by row-expanded same-theory bEF material over those rows.
- Prefix-splice the row-expanded replacement before the first use of A, using fresh extension variables scoped to that prefix; line-order preservation prevents later semantic facts from leaking backward.
- Induct over proof lines: bEF/SATeq/bounded-SR_h lines preserve Gamma_bEF, transparent FormulaEval lines add U_A+X_A, and no line outside K_idx(pi) can affect the final LB_N line by influence closure.
- Compose the parsed transcript with the generator circuit G_N to obtain a nonuniform circuit for H_N^SAT of size at most N^{rho+o(1)}+Gamma_TRS(pi)+polylog(N).
- If this size is below N^{1+epsilon-o(1)}, the asserted LB_N(1+epsilon) is false in the same model; if not, normalize Gamma_TRS by N to get forced row-equivalent support and the q-density corollary.
- For any failed TRS clause, construct pi_0,pi_1 agreeing on all visible charged material but differing on a private row or unread enable bit; this blocks occurrence completion and quarantines the rule unless RealSATInfluenceRealizer_N is proved.

Blocking gap: The proof is complete only for rules satisfying TransparentRowSupport_N. Arbitrary semantic FormulaEval remains blocked at RealSATInfluenceRealizer_N: proof syntax and N must uniformly determine an influence-closed row set, same-theory expansions, and a charged overhead before semantic evaluation.

## Falsifiers

- private-row falsifier: a hidden row r* changes a FormulaEval value while all displayed occurrence support and charged rows are identical.
- unread-enable-bit falsifier: the selector syntax lists a harmless support set until a semantic enable bit activates one uncharged row.
- subthreshold-charge falsifier: N^{rho+o(1)}+Gamma_TRS(pi)<N^{1+epsilon-o(1)} gives a same-model SIZE upper bound and invalidates LB_N(1+epsilon).
- q<epsilon ceiling falsifier: C(H_N^SAT)<=N^{1+q+o(1)} already blocks a claimed N^{1+epsilon} lower bound when q<epsilon-o(1).
- projected-dDNNF no-cover falsifier: the first projected row not covered by a visible certificate separates semantic projection from TRS enumeration.

## Learning

Cycle 130 consolidates the FormulaEval selector zoo into a theorem/countermodel pair. Transparent FormulaEval has a derived charge Gamma_TRS=Gamma_bEF+U_N+X_N and yields either a same-model upper-bound falsifier or N^{epsilon-o(1)} row-equivalent support. Hidden semantic influence is not a valid occurrence parser; it is quarantined by the private-row/unread-enable-bit falsifier unless RealSATInfluenceRealizer_N is supplied. This is route-level proof-system certification, not evidence for P != NP.

## Gedanken Experiment Design Seed

- Need decision: `use_as_falsifier_probe_now`
- Rationale: The remaining risk is not another abstract barrier slogan but hidden semantic row influence. A concrete unread-enable experiment tests whether the proposed FormulaEval rule supplies a valid target-preserving transfer certificate or merely hides advice.
- Situation seed: A beta-zero family H_N^SAT with M_N=N^{q+o(1)} rows, a proof-visible selector listing all rows except r*, and a semantic FormulaEval atom whose value additionally depends on an unread enable bit e_{r*} controlling SAT(G_N(x,r*)).
- Varied variable: lambda, the exponent in the number N^{lambda} of hidden enable-controlled rows omitted from the visible row-cover certificate.
- Held-fixed controls: N=2^n, M_N=N^{q+o(1)}, and the same generator G_N with overhead N^{rho+o(1)}., The target lower-bound statement LB_N(1+epsilon) and the nonuniform SIZE_N circuit model., The proof-visible selector code, surface proof length |pi|=N^{tau+o(1)}, and all charged TRS rows outside the hidden set., No external advice is allowed to identify hidden enabled rows.
- Expected observation: For lambda>0 the surface Gamma charge can remain unchanged while the semantic value and parity carrier vary on hidden rows; TRS succeeds only if the rule forces an added charge N^{1+lambda+o(1)} or enumerates the hidden rows.
- Transfer certificate needed: A RealSATInfluenceRealizer_N certificate proving that proof syntax uniformly lists every enable-influential row and supplies same-theory row expansions with charge included in Gamma_TRS before the semantic FormulaEval line is used.

## Next Experiment

Run the finite proof audit on one projected-dDNNF FormulaEval line with a visible row-cover certificate and one without it: compute K_idx, U_N, X_N, Gamma_TRS, then exhibit the first omitted reachable row as the falsifier in the no-cover case.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Restricted theorem packet: for Psys_sym^QE, delayed FormulaEval support is harmless exactly when it is sealed inside a syntactic quarantine block and the exit line exposes an advice-free, influence-closed row set before any external dependency. Then the transcript parses as a prefix-visible transparent proof with Gamma_QE, giving the same-model upper-bound falsifier for LB_N(1+epsilon). If the first external use sees an uncharged semantic influence, the private-row/unread-enable-bit falsifier applies.

## Definitions

- source object: a bit-explicit Psys_sym^QE transcript pi_N proving LB_N(1+epsilon) about H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), where M_N=N^{q+o(1)} and FormulaEval lines may be open transparent lines or quarantined internal lines.
- target object: a nonuniform SIZE circuit for the same H_N^SAT truth-table family with size below N^{1+epsilon-o(1)}, refuting only that transcript-level LB_N claim and not proving P != NP.
- controlled interface: the parser computes a time-stamped support cone K_QE from proof-prefix bit fields, open FormulaEval selectors, quarantine-exit certificates, row expansions, and Psys_bEF parent pointers; its cost ledger is Gamma_QE.
- target-preserving condition: every unquarantined dependency has its influential rows enumerated and expanded in the same SAT occurrence theory before first external use, with no SAT-truth advice, hidden selector advice, or post-hoc semantic pruning.
- A quarantine block Q=[a,e] is syntactically sealed when no line outside Q cites an internal line before the exit e, and e carries row-selector code, enumerator transcript, row-index list, and same-theory expansion witnesses for every internal FormulaEval value exported from Q.
- U_e denotes charged row-discovery or selector-unranking cost at exit e; X_e denotes charged same-theory row-expansion cost; E_pi denotes ordinary bEF expansion overhead already covered by Gap98-SRhNormalForm.

## Assumptions

- Proof model: Psys_bEF^- line rules are bit-explicit and already satisfy the Gamma_bEF induction; Psys_sym^QE adds only FormulaEval lines with open transparency or syntactic quarantine exits.
- Length and exponent regime: N tends to infinity, M_N=N^{q+o(1)}, generator overhead is N^{rho+o(1)}, formula length is polylogarithmic, epsilon>0 is fixed, and all o(1) terms are uniform over the transcript family.
- Uniformity and advice regime: K_QE, row enumerators, exit certificates, and parent pointers are computable from N and pi_N without nonuniform row-selection advice; pi_N itself may be hardwired only because the target circuit model is nonuniform SIZE.
- Same-theory condition: row expansions are occurrence-level SAT instances for the same formulas G_N(x,j); semantic SAT pruning is excluded unless RealSATInfluenceRealizer_N supplies zero-latency influence witnesses.
- Timing condition: a hidden row used inside quarantine is valid only if it has no external dependency until the exit line that enumerates and charges it.
- Non-claim boundary: the theorem is a restricted parser/falsifier theorem for a proof-system interface, not a lower bound and not a proof of P != NP.

## Equations

- Gamma_QE_ledger: `\Gamma_{QE}(\pi)=\Gamma_{bEF}(\pi)+\sum_{e\in Exit(\pi)}(U_e+X_e)+\sum_{t\in OpenFE(\pi)}(U_t+X_t)`. Valid when: Valid when pi is a Psys_sym^QE transcript whose quarantine exits expose advice-free enumerators and same-theory row expansions before external use.
- QE_parser_upper_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{QE}(\pi)+O(E_\pi N\operatorname{polylog}N)`. Valid when: Applies when H_N^SAT uses M_N=N^{q+o(1)} rows, generator overhead is N^{rho+o(1)}, and every charged row expansion is in the target SIZE model.
- subthreshold_falsifier: `N^{\rho+o(1)}+\Gamma_{QE}(\pi)+O(E_\pi N\operatorname{polylog}N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Requires that the target LB_N(1+epsilon) asserts no circuits of size N^{1+epsilon-o(1)} in the same nonuniform model.
- support_pressure_corollary: `\text{avoid falsifier}\Rightarrow |K_{idx}(\pi)|\ge N^{\epsilon-o(1)}\quad\text{if nonrow costs are }o(N^{1+\epsilon})`. Valid when: Valid when all non-FormulaEval costs are subthreshold and the proof avoids the first-hidden-influence countermodel by charging enough rows.

## Attempted Derivation

- Fix N and the target family H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)); treat pi_N as a nonuniform object only for constructing the target SIZE circuit.
- Define dependency edges for ordinary bEF lines from parent pointers and for FormulaEval lines from visible selector code or quarantine-exit certificates.
- Compute K_QE(i) by prefix fixed point: add open visible FormulaEval rows at line i; ignore sealed internal lines; at an exit line add the exit-certified row set and close under row-expansion parent pointers.
- Maintain invariant I(i): every unquarantined line among the first i lines is determined by the charged support K_QE(i), and has a same-theory circuit simulation with cost N^{rho+o(1)}+Gamma_QE(i)+O(E_i N polylog N).
- Ordinary bEF rules preserve I(i) by the archived Gap98-SRhNormalForm line induction.
- Open transparent FormulaEval lines preserve I(i) after paying U_t+X_t because the enumerator exposes all influential rows before the line is used.
- Sealed quarantine blocks need not satisfy external determinacy internally; their exit line pays U_e+X_e and commutes the support charge to before the first external citation, because no outside line depends on internal values earlier.
- If a first external hidden influence exists, construct omega_0, omega_1 agreeing on all charged prefix bits but differing on the hidden FormulaEval value; this is the private-row falsifier and terminates the induction.
- At the final LB_N line, I(final) gives the displayed SIZE upper bound; if subthreshold, the transcript-level lower-bound claim is invalid in the same target model.

Blocking gap: No blocking gap for the restricted syntactic Psys_sym^QE interface as defined. The named unresolved gap is QE-PurityParser_N/RealSATInfluenceRealizer_N for full semantic FormulaEval rules that use SAT truth to choose or prune rows without a prefix-visible exit certificate.

## Falsifiers

- A quarantined FormulaEval value has an external citation before its row-support exit certificate; first hidden influence gives a private-row falsifier.
- The exit row set is selected by SAT truth pruning rather than proof-prefix syntax; this is a semantic-oracle escape, not a valid transparent carrier.
- A projected selector hides witness-fiber or enable-bit influence and pays only projected support cost; an unread-enable-bit completion falsifies the parser.
- The proof imports nonuniform row advice or a hard-row selector; the target-preserving condition fails even if the selected row is hard.
- Nonrow overhead N^{rho}+U_N+E_pi N already exceeds N^{1+epsilon}; the row-support trichotomy is not the active obstruction.

## Learning

Cycle 130 adds a commutation theorem for delayed support: delay is valid only behind a syntactic quarantine whose exit is prefix-visible and charged before first external dependency. This strengthens the TransparentRowSupport_N packet by making timing, not selector type, the decisive invariant; full semantic FormulaEval remains quarantined at RealSATInfluenceRealizer_N.

## Gedanken Experiment Design Seed

- Need decision: `design now as a falsifier probe for the QE timing normal form`
- Rationale: The branch needs a concrete target-preserving test because the only remaining distinction is temporal: delayed support is valid inside quarantine but invalid after first external use. An abstract restatement would not expose the private row.
- Situation seed: A Tseitin/self-reduction FormulaEval block for H_N^SAT contains two candidate SAT rows controlled by an enable bit. The proof either enumerates both branches at a quarantine exit or truth-prunes one branch and cites the pruned value externally before listing the omitted row.
- Varied variable: exit latency ell, the number of external proof dependencies occurring before the influencing row set is enumerated and charged
- Held-fixed controls: M_N=N^{q+o(1)} and generator overhead N^{rho+o(1)} are fixed., The proof grammar is Psys_sym^QE with bit-explicit bEF parent pointers and same-theory SAT occurrence expansions., No nonuniform row advice, SAT-truth branch advice, or post-hoc selector explanation is allowed., The target circuit model remains the same nonuniform SIZE model used by LB_N(1+epsilon).
- Expected observation: For ell=0 with explicit branch enumeration, Gamma_QE pays the row-expansion charge and the parser simulation is valid. For ell>0 or truth-pruned hidden support, two occurrence completions agree on all charged prefix data but flip the externally used FormulaEval value, producing the falsifier.
- Transfer certificate needed: A zero-latency QE exit certificate or RealSATInfluenceRealizer_N: proof-prefix computable row enumeration, influence closure, same-theory row expansions, and ledger charge before any external dependency.

## Next Experiment

Write QE-PurityParser_N for one concrete Tseitin/self-reduction FormulaEval rule: list proof-bit fields, quarantine block delimiters, exit row-index encodings, enumerator transcript, same-theory expansion witnesses, eta/tau overhead, and the first-hidden-row counterexample when exit latency ell>0.
