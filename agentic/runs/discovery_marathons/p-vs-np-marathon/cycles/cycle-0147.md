# cycle-0147

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For restricted Psys_sym^{QCTSR} transcripts with bit-explicit bEF lines, declared counterfactual TSR children, and ranked proof-carrying same-theory quotient certificates, the saturation closure K_Q(pi) is order-independent and minimal. The Gamma_QCTSR line induction is valid on this least closure, and any subthreshold ledger gives a same-model upper-bound falsifier for LB_N(1+epsilon) for H_N^{SAT}.

## Definitions

- source object: a Psys_sym^{QCTSR} transcript pi for H_N^{SAT}(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, L_N=(log N)^d, and bit-explicit bEF, declared CTSR, and ranked quotient lines.
- target object: a same-nonuniform-SIZE circuit upper-bound falsifier for the asserted source lower bound LB_N(1+epsilon) for H_N^{SAT}, not a P != NP separation.
- controlled interface: least proof-carrying transparent support closure K_Q(pi) with visible parent pointers, counterfactual child rows, same-theory quotient-certificate forests, rank fields, and charged expansion ledger Gamma_QCTSR(pi).
- target-preserving condition: the parser is advice-free and length-uniform, every quotient certificate is surfaced before use, beta=0 polylog target rows are preserved, and N^{rho+o(1)}+Gamma_QCTSR(pi)+O(E_pi N)<N^{1+epsilon-o(1)}.
- external_anchor: formula-footprints transparent-support parser module; quotient compression is a proof-carrying same-theory support operation, not a named proof-system lower-bound theorem.
- nonvacuity_witness: a toy transcript with two Tseitin-renamed counterfactual child rows merged by a rank-1 EqSAT certificate whose dependencies are already in K_Q.
- sharpness_status: strict rank and dependency closure are sharp; dropping either creates a cyclic or first-unranked-merge falsifier.
- demotion_boundary: row-forcing and quotient-distance claims remain supporting lemmas, and SAT magnification remains conditional calibration.
- paper_claim_status: scoped parser/falsifier theorem candidate only; no H_N lower bound, no proof-system lower-bound theorem, and no P != NP claim.
- closed_objection_ids: pvsnp-ff-referee-003,pvsnp-ff-referee-006,pvsnp-ff-referee-008 preserved by explicit demotion and verifier-visible quotient charges.

## Assumptions

- Circuit model is nonuniform SIZE over Boolean circuits; the parser upper bound and the alleged LB_N are compared in the same model.
- Length regime has M_N=N^{q+o(1)}, generator cost N^{rho+o(1)}, SAT-row length L_N=(log N)^d with d>1, and beta=0 substitution overhead.
- Every FormulaEval or TSR row used by pi has visible row indices, parent pointers, and counterfactual children, or else the hidden-support countermodel applies.
- Each quotient merge carries a same-theory certificate forest whose nodes are syntactic EqSAT/declared-TSR derivations, not SAT-truth advice.
- Each quotient certificate node has a rank r in {0,...,R_N}; dependencies of a rank-r node must have smaller rank or already closed support status before use.
- Representative choice for quotient classes is deterministic from pi,N and the certificate forest; advice-chosen representatives are disallowed.
- The closure operator adds final-line support, proof parents, FormulaEval supports, counterfactual TSR children, quotient representatives, and all lower-rank certificate dependencies.
- The theorem is nonrelativizing only through the surfaced same-theory certificate verifier; it does not realize hidden semantic SAT influence.

## Equations

- closure_operator: `K_{t+1}=K_t\cup Parents(K_t)\cup FE(K_t)\cup CTSR(K_t)\cup QRep(K_t)\cup QCertDeps_{<rank}(K_t)`. Valid when: Valid when pi is a finite ranked QCTSR transcript whose dependency predicates are syntactically decidable from pi and N.
- termination_bound: `K_Q(\pi)=K_T \text{ for some } T\le |Rows(\pi)|+|CertNodes(\pi)|`. Valid when: Valid when every closure insertion is drawn from the explicit finite row and certificate-node universe of the transcript.
- ledger_definition: `\Gamma_{QCTSR}(\pi)=\Gamma_{bEF}(\pi)+U(K_Q)+X(K_Q)+B_{SR}(\pi)+B_{CTSR}(\pi)+B_Q(\pi)`. Valid when: Valid when all transparent FormulaEval, bounded self-reduction, counterfactual child, and quotient-certificate charges are surfaced before line induction uses them.
- parser_upper_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{QCTSR}(\pi)+O(E_\pi N)`. Valid when: Applies after the generator, parsed transcript ledger, and sparse residual-row patching are all circuits in the same nonuniform SIZE model.
- lb_falsifier_window: `N^{\rho+o(1)}+\Gamma_{QCTSR}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Requires that LB_N(1+epsilon) asserts a same-model lower bound for the exact carrier H_N^{SAT} on the same valid lengths.

## Attempted Derivation

- Define the finite universe U(pi) of row nodes, FormulaEval support nodes, counterfactual TSR child nodes, quotient representatives, and quotient-certificate nodes visible in pi.
- Define the monotone operator F(K) by adding proof parents, reachable transparent support, all counterfactual children of active TSR nodes, deterministic quotient representatives, and all lower-rank certificate dependencies for quotient merges touching K.
- Because F is monotone on a finite powerset lattice, iterating from the final LB_N line reaches a least fixed point K_Q independent of enumeration order.
- Strict rank decrease prevents a quotient certificate from validating deletion of a row through itself; every certificate node used in a merge has its dependency cone inserted before the merge can reduce the ledger.
- Minimality follows by induction on closure time: any support set sufficient for the line induction must contain the final line, then must contain each parent, child, same-theory dependency, and quotient representative demanded by the verifier, hence contains K_Q.
- Line induction extends the prior Gamma_bEF proof: bEF steps charge Gamma_bEF, transparent FormulaEval charges U+X, declared CTSR charges B_CTSR, and ranked quotient merges charge B_Q instead of deleting rows for free.
- The circuit simulator hardwires G_N, evaluates only rows in K_Q through the parsed support circuit, applies quotient representatives with their charged certificates, and patches E_pi residual rows by equality tests of cost O(E_pi N).
- If the resulting upper bound is below N^{1+epsilon-o(1)}, it is a valid same-model falsifier of the asserted LB_N(1+epsilon).

Blocking gap: No blocking gap remains for restricted ranked QCTSR syntax. The broader full-semantic FormulaEval system remains blocked exactly at RealSATInfluenceRealizer_N^{arb}, which would have to surface all real SAT-semantic influences with charges before use.

## Falsifiers

- first unranked quotient merge with no lower-rank same-theory certificate
- cyclic quotient-certificate dependency that deletes the row needed to certify itself
- advice-chosen quotient representative not computable from pi and N
- hidden semantic FormulaEval row or unread enable bit outside K_Q(pi)
- threshold-collapse falsifier when N^{rho}+Gamma_QCTSR+E_pi N reaches N^{1+epsilon-o(1)}
- model-mismatch falsifier when LB_N and the constructed circuit are not in the same nonuniform SIZE model
- positive-beta black-box substitution falsifier q+beta c bounding the target exponent window

## Learning

Cycle 147 closes a real proof-audit upgrade: ranked QCTSR quotient compression has a least, order-independent, proof-carrying support closure, so Gamma reduction is valid only after lower-rank same-theory dependencies are charged. The sharp falsifier is the first nondecreasing, cyclic, advice-chosen, or hidden semantic merge. This strengthens the paper parser/countermodel module without proving any H_N lower bound or P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for ranked quotient compression and closure confluence.`
- Rationale: The current branch no longer needs another abstraction of TransparentRowSupport_N; it needs to test whether proof-carrying quotient compression can hide a row while appearing charged. A concrete QCTSR transcript separates valid ranked compression from semantic row deletion.
- Situation seed: A beta-zero parity carrier H_N^{SAT} with M_N=N^{q+o(1)} generated polylog SAT rows; a QCTSR proof contains two counterfactual Tseitin-renamed child rows r and r' and tries to quotient them by an EqSAT same-theory certificate forest before evaluating the final XOR row.
- Varied variable: certificate rank slack delta, where delta>=1 means every dependency has smaller rank, delta=0 allows equal-rank mutual dependencies, and delta<0 represents an advice-chosen or cyclic merge.
- Held-fixed controls: M_N=N^{q+o(1)}, L_N=(log N)^d with d>1, beta=0, and generator overhead N^{rho+o(1)}., The same nonuniform SIZE model is used for the alleged LB_N and the constructed upper-bound falsifier., All non-quotient FormulaEval and counterfactual TSR supports are visible and charged in K_Q., Residual row patching cost remains O(E_pi N) with E_pi<N^{epsilon-o(1)} for the falsifier window.
- Expected observation: For delta>=1 the fixed-point closure is order-independent and the ledger charges the certificate before merge use. For delta=0 or cyclic dependencies, two worlds agree on all surfaced syntax while one private quotient row flips the carrier parity, so the merge is not valid.
- Transfer certificate needed: A finite verifier must check rank decrease, dependency closure, deterministic representatives, same-theory certificate soundness, and inclusion of the certificate forest in Gamma_QCTSR before quotient compression may affect the proof queue.

## Next Experiment

Instantiate the closure verifier on a three-row QCTSR toy transcript: two counterfactual child rows, one EqSAT certificate forest, and one attempted cyclic merge; compute K_Q, Gamma_QCTSR, and the first-rejected-merge private-row falsifier explicitly.
