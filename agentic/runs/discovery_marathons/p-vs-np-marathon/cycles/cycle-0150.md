# cycle-0150

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For beta-zero parity carriers, representative-stable ranked QCTSR quotient compression has an exact batched dictionary ledger. If a Psys_sym^{QrepCTSR} proof pi exposes visible support, counterfactual TSR children, and ranked same-theory quotient certificates before use, then the least closure K_Qrep(pi) yields a same-model nonuniform upper-bound falsifier for LB_N(1+epsilon) whenever N^{rho+o(1)}+Gamma_Qrep(pi)<N^{1+epsilon-o(1)}.

## Definitions

- source object: H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, |G_N(x,j)|=(log N)^d, and generator circuit size N^{rho+o(1)}.
- target object: the route-level lower-bound claim LB_N(1+epsilon) asserting C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)}, not the main P != NP conjecture.
- controlled interface: Psys_sym^{QrepCTSR} proofs whose FormulaEval, counterfactual TSR, and quotient-compression steps expose row support, parent pointers, same-theory certificates, ranks, and representative maps.
- target-preserving condition: beta=0 polylog target formulas, q,rho<1+epsilon, same nonuniform SIZE model throughout, no hidden row advice, and every SAT-semantic influence charged before use.
- K_Qrep(pi): the least fixed point generated from the final LB_N line by bit-explicit EF dependencies, transparent FormulaEval rows, counterfactual TSR child rows, and ranked same-theory certificate dependencies.
- D_Q(pi): the batched representative dictionary containing one representative per certified equivalence class plus all ranked certificate forests used to delete duplicate rows.
- Gamma_Qrep(pi): Gamma_bEF(pi)+U(K_Qrep)+X(K_Qrep)+C_Q(D_Q)+O(E_pi N), where U is row enumeration or full-scan charge, X is occurrence expansion, C_Q is certificate dictionary cost, and E_pi is sparse residual rows.
- inference_quality: source_statement is the existence of a small charged Psys_sym^{QrepCTSR} transcript for LB_N; target_statement is a SIZE upper bound for H_N^SAT refuting that source lower-bound claim in the same model.

## Assumptions

- Circuit model: nonuniform Boolean SIZE over carrier length N; the proof transcript and charged support may be hardwired only through the stated Gamma ledger.
- Length regime: N tends through valid carrier lengths, M_N=N^{q+o(1)}, target SAT formulas have polylog length, and beta=0 so target substitution does not introduce q+beta c threshold collapse.
- Uniformity/advice regime: K_Qrep and D_Q are computed from N and pi by a finite verifier; no row set, representative choice, or quotient certificate may be supplied as semantic advice outside the ledger.
- Same-theory regime: a quotient merge is accepted only if a surfaced certificate proves equality of SAT truth under the allowed Tseitin, EqSAT, and bounded self-reduction transformations, with strictly lower rank dependencies.
- Barrier status: the positive theorem is syntactic and relativizing for exposed support; hidden full SAT pruning is not covered and is quarantined at the nonrelativizing RealSATInfluenceRealizer_N^arb obligation.
- Non-claim: the lemma produces an upper-bound falsifier for a restricted proof-mediated source claim; it neither proves H_N lower bounds nor separates P from NP.

## Equations

- parity_carrier: `H_N^{SAT}(x)=\bigoplus_{j<M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad |G_N(x,j)|=(\log N)^d.`. Valid when: Valid when N is a carrier length and G_N is the fixed beta-zero polylog-query generator used by the proof transcript.
- least_qrep_closure: `K_{t+1}=K_t\cup Dep_{bEF}(K_t)\cup FE(K_t)\cup CTSR_{cf}(K_t)\cup CertDeps_Q(K_t),\quad K_{Qrep}=\bigcup_t K_t.`. Valid when: Valid when the proof syntax exposes parent pointers, counterfactual child lists, and ranked quotient-certificate dependencies before each compressed use.
- qrep_ledger: `\Gamma_{Qrep}(\pi)=\Gamma_{bEF}(\pi)+U(K_{Qrep})+X(K_{Qrep})+C_Q(D_Q)+O(E_\pi N).`. Valid when: Valid when every row enumeration, occurrence expansion, quotient certificate, and sparse residual patch is charged in the same nonuniform SIZE ledger.
- upper_bound_falsifier: `C_{SIZE}(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{Qrep}(\pi)+O(E_\pi N).`. Valid when: Valid when the parsed transcript is hardwired nonuniformly and each SAT influence row is represented by K_Qrep or by a charged same-theory certificate.

## Attempted Derivation

- Initialize K_0 with the final LB_N line and the carrier definition H_N^SAT; add bit-explicit EF dependencies exactly as in Gamma_bEF.
- For each reachable FormulaEval line, insert the visible row selector support and charge either U(K) for uniform enumeration or the full scan charge; add occurrence expansion to X(K).
- For each counterfactual TSR line, insert every reachable child row, not merely the actual branch; this preserves extensional safety under private-row variations.
- For each quotient merge, require a lower-rank same-theory certificate forest proving equality of SAT truth for the merged children; add all certificate dependencies before replacing children by the representative.
- Because ranks strictly decrease along certificate dependencies, the fixed point is finite and order-independent; representative stability follows by choosing the least certified representative in each connected component.
- Line induction: after each proof line, every formula value used by the parsed circuit is either bit-explicit, a charged row in K_Qrep, or a value transported along a charged same-theory certificate, so the line has circuit cost bounded by the accumulated Gamma_Qrep ledger.
- Hardwire pi, the generator G_N, K_Qrep, and D_Q nonuniformly; compute H_N by the generator plus the parsed transcript and sparse residual patches, giving C_SIZE(H_N)<=N^{rho+o(1)}+Gamma_Qrep(pi)+O(E_pi N).
- Contrapose: if LB_N(1+epsilon) asserts C_SIZE(H_N)>N^{1+epsilon-o(1)}, any transcript with N^{rho+o(1)}+Gamma_Qrep(pi)+O(E_pi N)<N^{1+epsilon-o(1)} is a valid same-model falsifier for that claimed source lower-bound certificate.

Blocking gap: The derivation does not cover a semantic pruning step that obtains a quotient or child deletion from real SAT truth without a surfaced same-theory certificate; that remains exactly RealSATInfluenceRealizer_N^arb.

## Falsifiers

- first unranked quotient merge falsifier: an omitted child row varies privately while all charged support stays fixed
- cyclic or nondecreasing rank certificate falsifier: the alleged dictionary is not a finite dependency-closed proof object
- advice-chosen representative falsifier: the representative map encodes hidden SAT-label information outside Gamma_Qrep
- hidden semantic pruning falsifier: actual-branch-only TSR support misses a counterfactual child reachable from the final line
- positive beta black-box substitution falsifier: q+beta c reaches 1+epsilon before all target exponents are excluded
- q<epsilon support-density falsifier: subthreshold reachable support can be equality-patched below the claimed LB_N threshold

## Learning

Cycle 150 closes a proof-delivery upgrade rather than rediscovering magnification: Qrep quotient compression is valid exactly as a batched, ranked, proof-carrying same-theory dictionary charged in Gamma_Qrep. The sharp falsifier is the first unranked, cyclic, advice-chosen, or hidden semantic merge. The result is a scoped parser/falsifier theorem and Formula Footprints supporting lemma; it does not prove H_N lower bounds or P != NP.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The branch needs a concrete check that Qrep compression is proof-carrying rather than semantic row deletion; another abstract statement would not test the exact private-row boundary.
- Situation seed: A batched Tseitin-renaming CTSR family where each of M_N=N^{q+o(1)} slots has several counterfactual child formulas that are SAT-equivalent by short surfaced renaming certificates, plus one deliberately unlisted duplicate child in a single batch.
- Varied variable: the allowed quotient-certificate rank depth R_Q for representative merges
- Held-fixed controls: beta=0 polylog SAT formula length and the same H_N^SAT parity carrier, q,rho,epsilon with q,rho<1+epsilon and the same nonuniform SIZE model, visible generator G_N, visible proof transcript pi, and no hidden row-selection advice, same-theory certificate checker for Tseitin/EqSAT rewrites and counterfactual TSR child syntax
- Expected observation: For R_Q at least the certificate DAG depth, Gamma_Qrep equals representative rows plus certificate forests and the parser remains valid; below that depth, the first unproved merge leaves one private row that flips H_N while the visible transcript is unchanged.
- Transfer certificate needed: A finite verifier proving rank-decreasing dependency closure, representative stability, and charged occurrence expansion before the intuition may enter the Gamma_Qrep line-induction proof.

## Next Experiment

Run the Tseitin-renaming Qrep thought experiment: instantiate two batches with one certified duplicate and one unlisted duplicate, compute K_Qrep, C_Q(D_Q), and Gamma_Qrep explicitly, then verify that the unlisted duplicate yields the first-hidden-row private-row falsifier while the certified duplicate preserves the line induction.
