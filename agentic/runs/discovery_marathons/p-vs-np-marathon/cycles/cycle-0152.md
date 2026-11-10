# cycle-0152

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`

## Branch Outputs

# Hardness-Magnification Bridge Realization: prefix-stable Qrep support closure

## Candidate Lemma

For beta-zero parity carrier proofs whose FormulaEval/CTSR quotient compression is implemented by an append-only ranked same-theory dictionary, the least prefix-stable Qrep support closure K_PQ(pi) is a valid TransparentRowSupport_N rule case. The parser line induction gives a same-model upper-bound falsifier for any claimed LB_N(1+epsilon) whenever the charged transcript is subthreshold. The first pre-use, rebinding, rank-cycle, advice-chosen representative, or hidden semantic merge gives a private-row/unread-enable-bit countermodel.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, generator overhead N^{rho+o(1)}, polylog SAT instance length L=(log N)^d, and a Psys_bEF^- plus transparent FormulaEval/CTSR/Qrep proof pi of a source lower-bound line LB_N(1+epsilon).
- target object: a nonuniform SIZE upper-bound circuit for H_N^SAT of size N^{rho+o(1)}+Gamma_PQ(pi)+O(E_pi N), used only as a route-level falsifier of the asserted source lower bound, not as a proof of P != NP.
- controlled interface: visible row support, prefix-closed FormulaEval dependencies, counterfactual TSR child declarations, and append-only ranked Qrep dictionary entries whose same-theory certificates are dependency-closed and charged before representative use.
- target-preserving condition: the simulation stays in the same nonuniform SIZE model, has beta=0 polylog target-query length, uses no hidden SAT-truth advice, and treats every semantic row influence as charged support unless a named RealSATInfluenceRealizer_N^arb is supplied.
- K_PQ(pi) is the least fixed point generated from the final LB_N line by adding parsed EF dependencies, SATeq links, bounded-SR leaves, reachable FormulaEval rows, counterfactual TSR child rows, and lower-rank dictionary-certificate rows needed by each Qrep representative use.
- A dictionary entry e=(r_old,r_new,C_e,a_e) is prefix-stable iff it is appended before its first use, never rebound, has rank a_e below every later dependent quotient use, and its certificate C_e is parsed into K_PQ(pi) before deleting r_old from the charged row set.

## Assumptions

- Model: nonuniform Boolean circuits for H_N and for the simulated generator; proof syntax is finite, bit-explicit, and verifier-visible.
- Length regime: N tends to infinity, M_N=N^{q+o(1)}, L=(log N)^d for fixed d>1, and beta=0 so SAT circuit substitution contributes only N^{o(1)} after generator overhead.
- Exponent regime: rho<1+epsilon and Gamma_PQ(pi)+O(E_pi N)<N^{1+epsilon-o(1)} are the intended falsifier thresholds.
- Uniformity/advice status: the dictionary order, ranks, representatives, and same-theory certificates are in the proof transcript, not selected by nonuniform advice outside pi.
- Same-theory condition: Qrep compression may identify rows only through surfaced EqSAT/TSR same-theory certificates whose dependencies are already in K_PQ(pi).
- Barrier status: the theorem is relativizing as a parser/countermodel statement and deliberately does not claim a nonrelativizing RealSATInfluenceRealizer_N^arb for full semantic pruning.

## Equations

- carrier: `H_N^{SAT}(x)=xor_{j=1}^{M_N} SAT(G_N(x,j)), M_N=N^{q+o(1)}`. Valid when: Valid when the source carrier is the beta-zero parity aggregator with a uniformly parsed generator and visible row indices.
- ledger: `Gamma_PQ(pi)=Gamma_bEF(pi)+U(K_PQ)+X(K_PQ)+D_Q(pi)+B_CTSR(pi)`. Valid when: Valid when K_PQ is the least prefix-stable closure and every dictionary, quotient, and counterfactual TSR dependency is charged before use.
- upper_bound: `C(H_N^{SAT}) <= N^{rho+o(1)}+Gamma_PQ(pi)+O(E_pi N)`. Valid when: Applies after the parser line induction produces a circuit transcript in the same nonuniform SIZE model with all residual bad rows equality-patched.
- falsifier_threshold: `N^{rho+o(1)}+Gamma_PQ(pi)+O(E_pi N)<N^{1+epsilon-o(1)} => not LB_N(1+epsilon)`. Valid when: Requires the asserted LB_N source lower bound to be in the same circuit model and quantified over the same valid lengths.
- q_density_corollary: `|K_idx(pi)|/M_N >= N^{epsilon-q-o(1)} when per-row expansion costs N`. Valid when: Valid when FormulaEval rows are expanded to occurrence rows with unit N charge and M_N=N^{q+o(1)} slots.

## Attempted Derivation

- Define K_PQ^0 as the final LB_N line plus its parsed bit-explicit parents. Iterate: add EF dependencies, SATeq certificate rows, bounded-SR_h leaves, reachable FormulaEval support rows, all counterfactual TSR children, and for each Qrep representative use add the lower-rank same-theory certificate forest and its row dependencies.
- Prove termination by the finite proof DAG size plus a strict lexicographic measure: proof-line index, dictionary append time, and rank. Prefix stability forbids cycles and rebinding, so the fixed point is order-independent.
- For each proof line l, maintain invariant I(l): all rows semantically influencing l through transparent rules are in K_PQ restricted to prefix l, and the circuit transcript for l has size at most the accumulated Gamma_PQ charge plus generator overhead already charged.
- EF and SATeq cases reuse the prior Gamma_bEF parser; bounded-SR_h contributes B_SR<=N^{q+eta+tau+o(1)}; FormulaEval contributes U(K)+X(K); counterfactual TSR contributes N^{1+kappa+theta+o(1)} for complete child declarations.
- Qrep case: replacing r_old by representative r_new is sound because the certificate C_e is same-theory, lower-rank, and already parsed into the prefix closure. The row deletion saves duplicate expansion only after D_Q(pi) has charged the dictionary entry and certificate forest.
- At the final LB_N line, compose the generator circuit, parsed transcript circuit, and equality patches for E_pi exceptional rows to obtain C(H_N)<=N^{rho+o(1)}+Gamma_PQ(pi)+O(E_pi N).
- If this upper bound is below N^{1+epsilon-o(1)}, it is a same-model falsifier for LB_N(1+epsilon). This proves only failure of that proof certificate or lower-bound assertion in the restricted parser model.

Blocking gap: The restricted PrefixStableQrepTransparentSupport proof is theorem-shaped; the unresolved extension remains RealSATInfluenceRealizer_N^arb for hidden full semantic SAT pruning and branch selection.

## Falsifiers

- falsifier: a Qrep representative used before its proof-carrying dictionary certificate is appended invalidates the charged parser and yields a private-row two-world countermodel.
- falsifier: representative rebinding lets two prefixes share the same visible transcript while later quotient meaning changes, so Gamma_PQ is not valid.
- falsifier: a rank cycle in same-theory certificates destroys the least fixed point and blocks line induction.
- falsifier: advice-chosen dictionary compression hides semantic row selection and is outside TransparentRowSupport_N.
- falsifier: full semantic branch pruning without RealSATInfluenceRealizer_N^arb remains quarantined, even if the restricted Qrep ledger is valid.

## Learning

Cycle 152 upgrades Qrep from an append-only convention to a prefix-verifiable rule case: quotient compression preserves the transparent parser only when certificate charge strictly precedes representative use. The exact no-go is temporal, not just acyclicity; delayed same-theory evidence is already a private-row falsifier. This closes a proof-audit loophole while preserving the nonclaim boundary: no H_N lower bound and no P != NP result.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The branch needs to test whether prefix-stable Qrep is genuinely necessary for the theorem pair or merely a cosmetic ledger condition.
- Situation seed: A beta-zero parity carrier H_N^SAT with two quotient-equivalent-looking CTSR child rows r0,r1; the proof deletes r0 using a Qrep dictionary entry whose same-theory certificate is either appended before use or delayed until after the final LB_N line.
- Varied variable: dictionary delay Delta, the number of proof steps between first representative use and the surfaced same-theory certificate; Delta=0 is prefix-stable and Delta>0 is pre-use compression.
- Held-fixed controls: M_N=N^{q+o(1)} with q<1+epsilon and beta=0 polylog SAT instance length., Generator overhead N^{rho+o(1)} with rho<1+epsilon., Same final LB_N line and same visible proof syntax before the first quotient use., No nonuniform SAT-truth advice outside the transcript pi.
- Expected observation: At Delta=0 the closure charges the certificate before deleting r0 and line induction is valid. At Delta>0 a private-row world can flip r0 while preserving all charged prefix information, making the quotient deletion unsound.
- Transfer certificate needed: A finite verifier certificate that every Qrep use references an append-only dictionary entry whose rank decreases, whose same-theory proof forest is already in K_PQ, and whose row expansion cost is included in Gamma_PQ before the use.

## Next Experiment

Write the finite verifier table for PrefixStableQrep entries: fields entry_id, append_time, old_row, rep_row, rank, certificate_root, dependency_list, first_use_time, charge_to_Gamma, and rejection reason; then run it on one EqSAT duplicate-child example and one delayed-certificate private-row counterexample.
