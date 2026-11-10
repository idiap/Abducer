# cycle-0148

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Ranked proof-carrying quotient compression for counterfactual declared TSR is a valid TransparentRowSupport_N rule case: the least ranked QCTSR support cone gives a same-model parser-to-circuit upper-bound falsifier, while any first unranked or hidden semantic merge is rejected by a private-row falsifier.

## Definitions

- source object: beta-zero parity carrier H_N^SAT(x)=xor_{j<M_N} SAT(F_{N,x,j}), with M_N=N^{q+o(1)}, formula length L_N=(log N)^d, and generator circuit size N^{rho+o(1)}.
- target object: a nonuniform SIZE_N upper-bound falsifier to the source lower-bound claim LB_N(1+epsilon): C(H_N^SAT)>N^{1+epsilon-o(1)}.
- controlled interface: Psys_sym^QCTSR proof pi with bit-explicit bEF lines, visible FormulaEval row supports, counterfactual TSR child declarations, and ranked same-theory quotient certificates charged before the merge they justify.
- target-preserving condition: beta=0 target queries, advice-free row enumeration, same nonuniform circuit model for source and simulated circuits, strict certificate-rank decrease, and no hidden SAT-semantic row selection.
- K_Q(pi) is the least prefix-closed reachable row set closed under parent pointers, visible FormulaEval influence, counterfactual TSR child expansion, and lower-rank same-theory quotient-certificate dependencies.
- C_Q(pi) is the bit size of same-theory certificate forests used to merge rows; U_Q(pi) is the visible enumerator and selector overhead; B_CTSR(pi) is the counterfactual TSR child-declaration charge.

## Assumptions

- Circuit model is nonuniform Boolean SIZE on N-bit source inputs; proof descriptions may be nonuniformly fixed per N but row influence cannot be hidden in semantic advice.
- Parameters q,rho,kappa,theta,epsilon are fixed constants; L_N=(log N)^d with d>1; rho<1+epsilon is required for any subthreshold falsifier.
- Every quotient certificate proves same-theory equivalence of the two row formulas inside the declared EqSAT/Tseitin/SR theory, and its dependencies have strictly smaller rank than the merge line.
- The closure algorithm sees all verifier bit fields: line id, rule tag, parent pointers, row index, child restriction code, quotient representative, certificate rank, and certificate dependency list.
- This is a restricted parser theorem, not a lower bound for H_N^SAT and not a proof of P != NP.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j<M_N} SAT(F_{N,x,j}),\quad M_N=N^{q+o(1)},\quad |F_{N,x,j}|=(\log N)^d`. Valid when: Valid when N is a valid source length and generator rows are syntactically enumerated.
- least_support_fixed_point: `K_Q(\pi)=\mu K\,[Seed(\pi)\cup Par(K)\cup FE(K)\cup CTSR(K)\cup Cert_Q^{<rank}(K)]`. Valid when: Applies after all proof dependencies, TSR children, and quotient certificates are exposed before use.
- ledger: `\Gamma_{QCTSR}(\pi)=\Gamma_{bEF}^{-}(\pi)+U_Q(\pi)+N|K_Q(\pi)|+B_{CTSR}(\pi)+C_Q(\pi)`. Valid when: Requires visible row enumeration, complete counterfactual child declarations, and charged same-theory certificate forests.
- parser_upper_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{QCTSR}(\pi)+O(E_\pi N)`. Valid when: Requires the target-preserving beta-zero substitution with advice-free row enumeration and same SIZE model.
- subthreshold_falsifier: `N^{\rho+o(1)}+\Gamma_{QCTSR}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Valid when the assumed LB_N threshold is in the identical nonuniform circuit model.
- support_density_pressure: `|K_Q(\pi)|\ge N^{\epsilon-o(1)},\quad |K_Q(\pi)|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Applies when all other ledger terms are subthreshold and every omitted row costs N to patch.

## Attempted Derivation

- Source statement: a Psys_sym^QCTSR proof pi certifies LB_N(1+epsilon) for the beta-zero parity carrier H_N^SAT in the nonuniform SIZE model.
- Target statement: if Gamma_QCTSR(pi) is subthreshold, then construct a same-model SIZE circuit for H_N^SAT of size below N^{1+epsilon-o(1)}, contradicting the certified lower-bound claim but not proving P != NP.
- Model context: source carrier is H_N^SAT, target class is nonuniform SIZE_N, proof model is bit-explicit bEF plus transparent FormulaEval plus counterfactual declared TSR plus ranked same-theory quotient certificates, and the simulation is a parser-to-circuit upper-bound reduction.
- Quantifier context: N ranges over valid source lengths; q,rho,kappa,theta,epsilon,d are fixed; L_N=(log N)^d; beta=0; all row enumerators and certificates are advice-free once pi and N are fixed.
- Closure construction: compute K_Q(pi) by iterating Seed, parent dependencies, visible FormulaEval influence, all counterfactual TSR children, and certificate dependencies of smaller rank until a fixed point is reached.
- Line induction: for bEF and transparent FormulaEval lines use the prior Gamma_bEF and U_Q+N|K_Q| charges; for CTSR lines use complete child declarations; for quotient merges replace rows only after their ranked same-theory certificate forest is in K_Q.
- Upper-bound assembly: combine generator overhead N^{rho+o(1)}, parsed row circuits, certificate verifier circuits, and sparse error correction O(E_pi N) to obtain C(H_N^SAT)<=N^{rho+o(1)}+Gamma_QCTSR(pi)+O(E_pi N).
- Necessity step: if a merge is first unranked, cyclic, advice-chosen, or hidden, keep all visible proof bits fixed and flip the private hidden row label; the transcript remains accepted while the parity carrier changes, so the parser is not extensionally valid.
- Reviewer findings: reduction consistency is valid for beta=0 only; quantifier uniformity is valid after certificate rank and row enumeration are syntax-visible; barrier specificity says the obstruction is a private-row/nonuniform-leakage countermodel, not a generic natural-proofs or relativization citation.

Blocking gap: Full semantic FormulaEval with hidden adaptive pruning remains blocked at RealSATInfluenceRealizer_N^arb: no advice-free nonrelativizing procedure is proved that lists all real SAT influences before the semantic rule is used.

## Falsifiers

- first unranked quotient merge falsifier: two completions agree on charged rows but differ on the hidden representative row
- cyclic or nondecreasing certificate-rank falsifier: the alleged compression is self-justifying and cannot be parsed before use
- advice-chosen representative falsifier: the quotient map carries nonuniform row-selection leakage not charged in Gamma_QCTSR
- hidden adaptive TSR pruning falsifier: an unlisted counterfactual child can be made decisive by a private-row assignment
- positive-beta black-box substitution falsifier remains active outside this beta-zero parser route: q+beta*c caps all-exponent transfer

## Learning

Cycle 148 turns ranked QCTSR from an order-independent closure statement into a representative-stable TransparentRowSupport_N rule case. The valid contribution is a restricted theorem/countermodel pair: proof-carrying quotient compression preserves Gamma line induction, while the first unranked, cyclic, advice-chosen, or hidden semantic merge yields a private-row falsifier. This closes a proof-audit loophole without proving any H_N lower bound or P != NP; full semantic pruning remains exactly at RealSATInfluenceRealizer_N^arb.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The current theorem boundary depends on whether quotient compression is truly proof-carrying or hides semantic row advice; a concrete private-row test is more informative than another abstraction of RealSATInfluenceRealizer_N.
- Situation seed: A four-row QCTSR transcript has rows r0,r1,r2,r3 for generated SAT formulas, declares all counterfactual TSR children for r0 and r1, includes a rank-1 EqSAT certificate merging r0 with r1, and then attempts an unranked hidden merge of r2 with r3 controlled by an unread enable bit e.
- Varied variable: the certificate-rank discipline: strict lower-rank proof-carrying merge versus same-rank/cyclic/unread-enable hidden merge
- Held-fixed controls: H_N^SAT is the beta-zero parity carrier with M_N=N^{q+o(1)} and L_N=(log N)^d., The generator overhead N^{rho+o(1)} and all bEF/CTSR visible charges are held below N^{1+epsilon-o(1)}., The final proof transcript and all visible row labels are held identical in the two worlds., No SAT-truth advice or hidden row selector is allowed outside the displayed QCTSR syntax.
- Expected observation: Strict ranked certificates make the representative choice invariant under both completions, while the unread-enable merge lets two completions preserve the proof transcript and flip the final parity. This isolates exactly why ranked QCTSR is valid and hidden semantic quotienting is not.
- Transfer certificate needed: A finite verifier must check rank decrease, dependency closure, same-theory certificate soundness, and inclusion of every certificate dependency in K_Q before the merge; otherwise the intuition stays only a falsifier probe.

## Next Experiment

Write the finite K_QCTSR verifier on a projected-dDNNF example with one certified duplicate row and one unread-enable hidden merge; compute U_Q,N|K_Q|,B_CTSR,C_Q,E_pi and show exactly where the hidden merge fails the valid support ledger.
