# cycle-0123

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For Psys_sym^dag proofs with visible FormulaEval parent pointers and advice-free row support certificates, the least prefix-closed reachable support cone K_dag(pi) is the minimal charged object for the parser-to-circuit falsifier. If N^{rho+o(1)}+Gamma_dag(pi)+O(E_pi N)<N^{1+epsilon-o(1)}, then the claimed LB_N(1+epsilon) for H_N^SAT is invalid in the same nonuniform SIZE model. If a reachable extensional row is omitted from K_dag(pi), a private-row or unread-enable-bit two-world construction is a valid falsifier to occurrence completion.

## Definitions

- source object: H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, L_N=(log N)^d, d>1, generator cost N^{rho+o(1)}, and source claim LB_N(1+epsilon): C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)}.
- target object: a same-model nonuniform SIZE upper-bound falsifier for LB_N(1+epsilon), not a proof of NP not subset P/poly and not a proof of P != NP.
- controlled interface: Psys_sym^dag FormulaEval lines whose visible selector code, parent pointers, row certificates, same-theory occurrence expansions, and bounded-SR_h leaves generate the least prefix-closed reachable support cone K_dag(pi).
- target-preserving condition: beta=0 polylog target instances, advice-free row enumeration or full-scan charge, same source and simulator circuit model, no hidden SAT-truth advice, and every semantic influence row realized before later use.
- A row atom a=(ell,r) means that proof line ell can influence the final LB_N line through source row or parity slot r.
- The closure operator adds parent FormulaEval rows, selector dependencies, SR_h leaves, Tseitin/equality links already declared in Psys_bEF^-, and every row used by a later reachable line.
- U_N(K) is the cost of uniformly enumerating reachable rows in K; X_N(K) is the same-theory occurrence-expansion charge, normally tilde O(N|K|).

## Assumptions

- Quantifiers are asymptotic over valid lengths N with fixed epsilon>0, fixed q,rho, and fixed polylog exponent d>1.
- Psys_bEF^- bit-explicit EF, SATeq links, and bounded-SR_h rules have already been parsed with Gamma_bEF(pi) as in cycles 100-122.
- FormulaEval is extensional and transparent: its syntactic data determines RowSet(a) or pays a full scan over M_N rows; no nonuniform hidden selector is allowed.
- Every later symbolic use of a FormulaEval value must point to a row already in the prefix-closed reachable cone before the line induction charges it.
- The simulator and the lower-bound claim use the same nonuniform SIZE model; advice introduced only by the original proof transcript or charged row certificates is counted in Gamma_dag.
- Full real SAT-semantic FormulaEval is excluded unless RealSATInfluenceRealizer_N uniformly lists and charges all influencing rows before the semantic rule is used.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j<M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad L_N=(\log N)^d`. Valid when: Valid when the source carrier is the beta-zero parity carrier with uniformly generated polylogarithmic SAT instances.
- least_closure: `K_0=Reach(final),\quad K_{t+1}=K_t\cup Parents(K_t)\cup SupportRows(K_t),\quad K_{dag}(\pi)=\bigcup_t K_t`. Valid when: Valid when every dependency edge and support certificate is visible in the proof syntax and uses no semantic row advice.
- charged_gamma: `\Gamma_{dag}(\pi)=\Gamma_{bEF}(\pi)+U_N(K_{dag})+X_N(K_{dag})`. Valid when: Applies after the fixed-point closure terminates on the finite proof DAG and all transparent rows are charged.
- row_expansion: `X_N(K_{dag})\le \widetilde O(N\cdot |K_{dag}|)`. Valid when: Requires same-theory occurrence expansion where each surfaced row is materialized at N-bit source cost.
- same_model_upper_bound: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{dag}(\pi)+O(E_\pi N)`. Valid when: Applies after the reduction preserves the same nonuniform SIZE model, beta-zero query length, and charged support parameters.
- lb_falsifier_window: `N^{\rho+o(1)}+\Gamma_{dag}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Valid when LB_N(1+epsilon) denotes an asserted same-model lower bound above the displayed threshold.
- support_density_corollary: `LB_N(1+\epsilon)\Rightarrow |K_{dag}|\ge N^{\epsilon-o(1)},\quad |K_{dag}|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Requires the row-expansion term to dominate uncharged support cost and M_N=N^{q+o(1)} slots.

## Attempted Derivation

- Instantiate the source statement as LB_N(1+epsilon) for H_N^SAT in nonuniform SIZE, with M_N=N^{q+o(1)}, L_N=(log N)^d, beta=0, and generator overhead N^{rho+o(1)}.
- Parse all Psys_bEF^- lines first; EF dependencies, SATeq links, and bounded-SR_h leaves contribute Gamma_bEF(pi) exactly as in the restricted bit-explicit theorem packet.
- Define row atoms for FormulaEval lines and run the verifier-visible fixed point: start from rows reachable from the final LB_N line, repeatedly add parent rows, selector rows, same-theory expansion rows, and earlier rows used by later reachable lines.
- Charge each closure addition either by U_N(K_dag), an advice-free enumerator/full-scan cost, or by X_N(K_dag), the N-per-row occurrence expansion; reject any row whose selector is only semantic advice.
- For the projected-dDNNF example, gate pointers and projection maps give the enumerator. The reachable cone follows output-gate dependencies, so irrelevant dDNNF components are not charged.
- Extend the line induction: every proof line whose reachable rows are in K_dag has a simulator circuit of cost bounded by the prior simulator plus the charged local rule cost; the final line yields C(H_N^SAT)<=N^{rho+o(1)}+Gamma_dag(pi)+O(E_pi N).
- Contrapose the lower-bound claim: if this upper bound is below N^{1+epsilon-o(1)}, the proof transcript is a same-model falsifier for LB_N(1+epsilon).
- Prove minimality for extensional FormulaEval by choosing the first later-used row r* omitted from K_dag; two transcripts agree on charged rows and all syntax but differ on r*, so the parser cannot be valid for both.
- Derive the q-trichotomy from X_N(K)=tilde O(N|K|): a valid LB_N certificate must force |K_dag|>=N^{epsilon-o(1)}, hence density at least N^{epsilon-q-o(1)} inside M_N slots.

Blocking gap: RealSATInfluenceRealizer_N remains unproved for full semantic FormulaEval: a real SAT-semantic rule might force r* nonrelativizingly from charged rows even when no extensional support certificate lists it.

## Falsifiers

- first-hidden-reachable-row falsifier for extensional FormulaEval without charged support
- unread-enable-bit falsifier for projected or guarded FormulaEval whose selector is not surfaced before later use
- private-row two-world falsifier for symbolic FormulaEval that treats row influence as semantic oracle advice
- q<epsilon total-slot falsifier: M_N=N^{q+o(1)} cannot supply N^{epsilon-o(1)} charged rows
- positive-beta black-box substitution falsifier: SAT in SIZE(n^c) gives source upper bound N^{q+beta c+o(1)} before all-exponent exclusion
- nonuniform row-selection leakage falsifier when RowSet(a) is supplied by advice rather than proof syntax
- semantic RealSAT escape falsifier probe: if no advice-free influence realizer exists, full FormulaEval stays outside the valid parser theorem

## Learning

Cycle 123 closes a proof-audit gap rather than repeating the magnification slogan: K_dag is an implementable least fixed point, projected-dDNNF gives a concrete transparent positive case, and the unread-enable-bit/private-row construction gives a precise necessity falsifier. The valid result is a scoped parser/falsifier theorem for beta-zero parity magnification; full semantic FormulaEval is still blocked exactly at RealSATInfluenceRealizer_N.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch already has an abstract K_dag theorem; the remaining proof-quality risk is whether projected-dDNNF-style FormulaEval genuinely surfaces every later influence or hides a semantic selector row. A concrete thought experiment tests the theorem boundary without broadening carriers.
- Situation seed: A beta-zero parity carrier H_N^SAT with M_N=N^q slots and a projected-dDNNF FormulaEval line whose output gate computes over exposed child rows, except one optional projection gate has an unread enable bit that can route a private row r* into the final LB_N proof use.
- Varied variable: h=number of hidden reachable rows controlled by unread enable bits, with h ranging from 0 through N^{epsilon-o(1)}.
- Held-fixed controls: M_N=N^{q+o(1)}, L_N=(log N)^d with d>1, and generator cost N^{rho+o(1)} remain fixed., The proof system below FormulaEval is Psys_bEF^- with bounded-SR_h and the same Gamma_bEF ledger., The target simulator remains the same nonuniform SIZE model used by LB_N; no SAT-truth advice is added., Every visible projected-dDNNF edge, projection map, and row selector is charged by U_N or full scan., The target consequence remains only a same-carrier LB_N falsifier, not NP not subset P/poly.
- Expected observation: At h=0 the projected-dDNNF example satisfies TransparentRowSupport_N and the Gamma_dag induction is valid. For 0<h<N^{epsilon-o(1)}, the unread-enable-bit row gives a subthreshold private-row falsifier. For h>=N^{epsilon-o(1)}, the rows must be surfaced and the support-density trichotomy becomes visible.
- Transfer certificate needed: A finite audit certificate consisting of the K_dag fixed-point trace, enumerator code for visible rows, same-theory row-expansion receipts, and, for any semantic row, a nonrelativizing RealSATInfluenceRealizer_N proof before the row may enter Gamma_dag.

## Next Experiment

Write the referee-checkable trace for the projected-dDNNF example: list gate fields, parent pointers, projection maps, RowSet certificates, K_0,K_1,... closure additions, U_N and X_N charges, then flip one unread enable bit to exhibit the first-hidden-row countermodel and verify the Gamma_dag threshold numerically for q<epsilon, q=epsilon, and q>epsilon.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For Psys_sym^dag with projected-dDNNF FormulaEval, proof-visible RowCoverCertificate_N makes the FE line transparent: K_rc is the least prefix-closed reachable row support and Gamma_rc prefix-splices to bEF. If a reachable row is not covered, that row is a private-row falsifier to surface parsing.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) and a Psys_sym^dag proof pi of LB_N(1+epsilon) using projected-dDNNF FormulaEval lines.
- target object: same-model nonuniform SIZE upper-bound falsifier or forced row-equivalent support for LB_N; no claim toward P != NP.
- controlled interface: RowCoverCertificate_N supplies visible dDNNF DAG, projection map, row-id covers, parent pointers, decomposability/determinism checks, and an enumerator for every reachable row.
- target-preserving condition: N and pi determine all rows and expansions without semantic advice; row-expanded bEF material is prefix-spliced in the same theory before the FE line is used.

## Assumptions

- Model context: nonuniform Boolean SIZE, beta-zero SAT-parity carrier, bEF plus transparent projected-dDNNF FormulaEval, simulation/extraction rather than many-one reduction.
- Quantifier regime: N=2^n, M_N=N^{q+o(1)}, |pi|=N^{tau+o(1)}, generator overhead N^{rho+o(1)}, rho<1+epsilon, deterministic no-advice closure.
- The projected-dDNNF certificate is syntactic: AND gates are decomposable, OR gates deterministic or disjointly covered, and projection never hides a row that can affect FormulaEval.
- Same-theory expansion is available for every covered row; otherwise the rule is classified as semantic FormulaEval and routed to RealSATInfluenceRealizer_N.

## Equations

- Krc_fixed_point: `$K_{rc}^{0}=\{L_{final}\}; K_{rc}^{t+1}=K_{rc}^{t}\cup Par(K_{rc}^{t})\cup\bigcup_{A\in FE(K_{rc}^{t})} RowCover(A)$`. Valid when: Valid when FE nodes expose parent pointers and RowCoverCertificate_N is verified before the worklist closes.
- Gamma_rc_charge: `$\Gamma_{rc}(\pi)=\Gamma_{bEF}(\pi)+U_{rc}(\pi)+N\cdot |K_{rows}^{rc}(\pi)|+O(E_{\pi}N)$`. Valid when: Applies after each covered row is prefix-spliced into bEF with fresh extensions and no hidden advice.
- subthreshold_upper_bound_falsifier: `$N^{\rho+o(1)}+\Gamma_{rc}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow CC(H_N^{SAT})<N^{1+\epsilon-o(1)}$`. Valid when: Requires the same nonuniform SIZE model, rho<1+epsilon, and charged expansion below the lower-bound threshold.

## Attempted Derivation

- Parse each projected-dDNNF FE line. Verify node types, projection map, row-tag leaves, parent pointers, decomposable ANDs, deterministic ORs, and an output-sensitive row enumerator or full-scan declaration.
- Run the monotone worklist from the final LB line. For every reachable FE node, add its certified RowCover rows and syntactic parents. Tarski monotonicity gives termination and least prefix-closed visible support.
- Prefix-splice each covered row before the FE line using fresh extension variables. The line induction adds exactly U_rc plus N per expanded row, yielding Gamma_rc rather than charging the full selector zoo.
- If a row r is semantically influential but absent from RowCover, freeze all visible syntax and charged rows, flip the private enable or SAT value at r, and obtain identical parser transcript with different FE value: the hidden-row falsifier.

Blocking gap: The packet proves the projected-dDNNF case only for certificate-bearing RowCoverCertificate_N. It does not realize arbitrary RealSAT FormulaEval or prove compact covers exist for every projected-dDNNF.

## Falsifiers

- Uncovered-row falsifier: a projected auxiliary bit enables row r while the visible cover omits r; flipping SAT(G_N(x,r)) changes FormulaEval but not K_rc.
- Nondeterministic OR falsifier: overlapping children make a bottom-up row cover undercount reachable rows unless determinism or disjoint cover witnesses are checked.
- SAT-advice cover falsifier: listing only rows whose SAT value is 1 preserves short syntax but loses constructivity and is semantic, not transparent.
- Threshold falsifier: full-scan fallback with M_N=N^{q+o(1)} and q>=epsilon can be validly charged yet too large to contradict LB_N(1+epsilon).

## Learning

Cycle 123 upgrades projected-dDNNF from an example to a dichotomy: visible row covers are transparent and charged by Gamma_rc, while a first omitted reachable row is a finite falsifier. This is valid route-level parser certification, not P vs NP evidence.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and threshold calculator for the projected-dDNNF FormulaEval boundary.`
- Rationale: The abstract TRS theorem is already stable; the remaining paper risk is whether projected-dDNNF support is genuinely visible or hides rows through projection variables.
- Situation seed: A padded SAT-parity family where each FE line uses a projected-dDNNF selector over M_N=N^q rows; one version carries interval row covers, another hides one row behind an unread enable bit.
- Varied variable: Cover output exponent chi where |RowCover|=N^{chi+o(1)}, including chi<epsilon, chi=epsilon, and hidden-row chi undefined.
- Held-fixed controls: N=2^n, generator overhead N^{rho+o(1)} with rho<1+epsilon., Same Psys_sym^dag proof syntax, same bEF row expansion, and no SAT-truth advice., M_N=N^{q+o(1)} and the target LB_N(1+epsilon) in nonuniform SIZE.
- Expected observation: Certified covers with chi<epsilon keep Gamma_rc potentially subthreshold; chi>=epsilon causes support pressure; an omitted enabled row yields transcript equality with changed carrier parity.
- Transfer certificate needed: A verified RowCoverCertificate_N plus same-theory prefix splice; without it the intuition may only enter as the private-row falsifier, not as a valid parser proof.

## Next Experiment

Work one projected-dDNNF FE line: compute RowCover, K_rc, U_rc, and Gamma_rc; then delete one enabled row from the cover and verify transcript-preserving private-row failure.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For Psys_sym^dag proofs with visible FormulaEval dependencies, the least reachable cone K_dag is proof-bit computable and gives Gamma_dag=Gamma_bEF+U_K+X_K. If the transcript is subthreshold it is a same-SIZE falsifier for LB_N(1+epsilon); hidden projection influence gives a private-row countermodel.

## Definitions

- source object: a bit-explicit Psys_sym^dag proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)).
- target object: a nonuniform SIZE circuit for H_N^SAT at exponent below 1+epsilon, used only as a falsifier of that proof-route lower-bound claim.
- controlled interface: FormulaEval lines expose parent pointers, row-support certificates, projected-support enumerators or full-scan charges, and same-theory row expansions.
- target-preserving condition: N, G_N, SAT encoding, row index set, and nonuniform SIZE model are unchanged; all influencing rows are enumerated or charged before use, with no hidden advice.
- K_dag(pi) is the least fixed point of rows and proof lines reachable backward from the final LB_N line through visible syntactic and FormulaEval dependencies.
- For projected-dDNNF support, U_K is certified projected-row discovery cost after deduplication or witness-support scan; X_K is the same-theory SAT expansion cost for emitted rows.

## Assumptions

- Length regime: M_N=N^{q+o(1)}, generator overhead is N^{rho+o(1)}, formulas have polylog N size, and o(1) losses are uniform over proof length.
- Proof model: Psys_bEF^- parsing and bounded SR_h normal form are already valid; FormulaEval is the only added mechanism audited here.
- Uniformity/advice: the fixed-point closure algorithm reads pi and N only; no SAT-truth advice, hard-row selector advice, or nonuniform witness choice may enter U_K.
- Same-theory condition: expanded rows are the actual G_N(x,j) SAT instances used in H_N^SAT, not surrogate semantic labels or oracle answers.
- Boundary condition: full semantic FormulaEval is excluded unless RealSATInfluenceRealizer_N gives advice-free influence rows and a charged R_N before the rule is applied.

## Equations

- fixed_point_closure: `K_{t+1}=K_t \cup Dep_{syn}(K_t,\pi) \cup Dep_{FE}^{vis}(K_t,\pi),\quad K_{dag}=\mu K_t`. Valid when: Valid when every dependency operator is computed from proof bits and visible support certificates, not from SAT-truth advice.
- ledger: `\Gamma_{dag}(\pi)=\Gamma_{bEF}(\pi)+U_K(N,\\pi)+X_K(N,\pi)`. Valid when: Applies after bounded-SR_h parser costs are established and each FormulaEval influence row is enumerated or fully scanned.
- same_model_falsifier: `N^{\rho+o(1)}+\Gamma_{dag}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Requires the target-preserving same-SIZE simulation for H_N^SAT and a claimed lower-bound threshold N^{1+epsilon-o(1)}.

## Attempted Derivation

- Initialize K with the final LB_N line; iteratively add syntactic parents, SR_h occurrence neighborhoods, and visible FormulaEval row dependencies until no proof-bit-visible item remains.
- For a projected-dDNNF FormulaEval line, charge row discovery by certified projected enumeration U_K or by witness-support scan; then charge X_K for expanding each emitted row into the same SAT instance used by H_N^SAT.
- Run line induction: every line outside K_dag is irrelevant to the final claim, while every line inside K_dag has its parsed circuit contribution bounded by Gamma_bEF plus the accumulated U_K and X_K charges.
- At the first FormulaEval line whose value depends on a nonenumerated projected witness or unread enable bit, produce two occurrence completions agreeing on all read bits but flipping the row value; this is the finite hidden-support falsifier.

Blocking gap: RealSATInfluenceRealizer_N for full semantic SAT is still unproved; the restricted projected-dDNNF case is valid only when influence closure is syntactic and charged.

## Falsifiers

- Projected witness advice falsifier: if dedup chooses rows using SAT truth or nonuniform witness selection, K_dag is not proof-bit computable and the target language transfer is invalid.
- Unread-enable-bit falsifier: a hidden row flag e_r can be flipped in two completions that agree on all parsed occurrences, changing FormulaEval without changing the transcript.
- Charge-collapse falsifier: if U_K+X_K >= N^{1+epsilon-o(1)}, the construction may be valid but gives no contradiction to LB_N(1+epsilon).
- Semantic-oracle falsifier: unwitnessed SAT extensionality can determine influence without listing rows, placing the rule outside the controlled interface unless RealSATInfluenceRealizer_N is supplied.

## Learning

Cycle 123 adds proof-audit content rather than a new route: projected-dDNNF FormulaEval is valid only through certified K_dag discovery cost, while hidden projection or enable influence is a finite same-theory falsifier. The result strengthens the paper parser obstruction, not P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and validation example for L123.`
- Rationale: The branch already has the K_dag abstraction; the missing proof-audit value is a concrete projected-support case that either pays U_K+X_K or exposes hidden semantic influence.
- Situation seed: A projected-dDNNF FormulaEval line for H_N^SAT where auxiliary witness y selects row j, plus an optional unread enable bit e_j that gates the SAT value of one private row.
- Varied variable: Projection fiber entropy ell, equivalently whether projected rows are deduplicated by a certified enumerator U_K=N^{ell+o(1)} or only by hidden SAT-semantic witnesses.
- Held-fixed controls: Keep G_N, M_N=N^{q+o(1)}, H_N^SAT, and the nonuniform SIZE target model fixed., Keep bounded-SR_h parsing, same-theory row expansion, and generator overhead N^{rho+o(1)} fixed., Forbid SAT-truth advice and nonuniform hard-row selection in the row enumerator.
- Expected observation: When ell is certified, Gamma_dag pays U_K+X_K and the transcript falsifier threshold is auditable; when ell is hidden, the unread-enable row gives two valid completions with opposite FormulaEval values.
- Transfer certificate needed: An advice-free projected-row enumerator or RealSATInfluenceRealizer_N that lists all influential rows before use and records its cost in Gamma_dag.

## Next Experiment

Write the referee-checkable K_dag pseudocode for one projected-dDNNF FormulaEval line, compute U_K and X_K on the example, then instantiate the unread-enable-bit countermodel as the first bad line.
