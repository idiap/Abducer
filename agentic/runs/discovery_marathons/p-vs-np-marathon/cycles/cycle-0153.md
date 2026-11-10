# cycle-0153

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`

## Branch Outputs

# Hardness-Magnification Bridge Realization: prefix-strict Qrep support audit

## Candidate Lemma

In Psys_sym^{dag+Qrep}, proof-carrying quotient compression is a valid TransparentRowSupport_N rule case exactly when every representative dictionary use is preceded, at a strict earlier proof prefix, by a ranked same-theory certificate forest whose dependencies are already charged. Under this condition the Gamma line induction extends with a Qrep dictionary charge; if strict prefix visibility fails, the first unsafe merge gives a private-row falsifier.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, generator cost N^{rho+o(1)}, and formula length L_N=(log N)^d for fixed d>1.
- target object: same-model nonuniform SIZE upper-bound falsifier for the claimed source lower bound LB_N(1+epsilon), not a proof of H_N hardness or P != NP.
- controlled interface: PrefixStrictQrep is a transparent FormulaEval quotient rule whose dictionary entries map row identifiers to representatives only after visible same-theory certificates and all certificate dependencies have been charged.
- target-preserving condition: beta=0 polylog SAT-query substitution, fixed epsilon>0, q,rho<1+epsilon, no hidden advice, and every quotient merge is ranked, acyclic, dependency-closed, and charged before representative use.
- observable: Gamma_Qrep(pi) is the parser ledger formed from bit-explicit EF, SATeq links, bounded SR_h, transparent FormulaEval support, and prefix-strict Qrep dictionary certificates.
- same-theory certificate: a finite syntactic forest proving that two row formulas have identical SAT value within the declared SATeq/TSR theory, without consulting the SAT truth label as advice.

## Assumptions

- Circuit model is nonuniform Boolean SIZE over the same source length N; equality patching a bad source row costs O(N) gates.
- Proof model is restricted Psys_bEF^- plus transparent FormulaEval lines and Qrep quotient lines with verifier-visible row identifiers, parent pointers, and dictionary-entry ranks.
- All row enumerators, support certificates, and Qrep certificates are advice-free functions of N and the proof string pi; no semantic SAT-truth advice selects representatives.
- Each Qrep dictionary entry e has cert_line(e)<first_use_line(e), and every dependency of cert(e) has strictly smaller rank or is already in the prefix-closed support cone.
- The beta-zero transfer uses only polylog-length SAT queries, so substituting SAT circuits of size L_N^c contributes N^{o(1)} per exposed query block and preserves all fixed target exponents.
- Errors E_pi in the parsed transcript are source-row errors, not hidden formula-row errors, so sparse-row patching is charged as O(E_pi N).

## Equations

- Qrep ledger: `Gamma_Qrep(pi)=Gamma_bEF(pi)+U_N(pi)+X_N(pi)+D_Q(pi)`. Valid when: Valid when Psys_sym^{dag+Qrep} exposes row support, FormulaEval expansion, and prefix-strict Qrep certificates before every representative use.
- Dictionary charge: `D_Q(pi)=sum_{e in Dict_Q(pi)} (|desc(e)|+|cert(e)|+sum_{a in dep(e)} row_cost(a))`. Valid when: Valid when dictionary entries are ranked, acyclic, dependency-closed, and no dependency is introduced after the representative is used.
- Parser-to-circuit upper bound: `C_N(H_N^SAT) <= N^{rho+o(1)}+Gamma_Qrep(pi)+O(E_pi N)`. Valid when: Applies after the line induction parses every proof line into charged source-row support in the same nonuniform SIZE model.
- Subthreshold falsifier inequality: `N^{rho+o(1)}+Gamma_Qrep(pi)+O(E_pi N)<N^{1+epsilon-o(1)} => not LB_N(1+epsilon)`. Valid when: Requires LB_N(1+epsilon) to mean a same-model N^{1+epsilon-o(1)} lower bound for the explicit source carrier H_N^SAT.
- Strict-prefix condition: `forall e, cert_line(e)<first_use_line(e) and rank(dep(e))<rank(e)`. Valid when: Valid when Qrep compression is proof-carrying rather than a semantic row-deletion convention or advice-chosen quotient map.

## Attempted Derivation

- Define Dict_Q(pi) as append-only entries e=(row a, representative rep(a), rank r, certificate forest F_e, cert_line, first_use_line). Reject entries with cert_line>=first_use_line, cyclic dependencies, nondecreasing dependency rank, or rebinding of a previously used representative.
- Compute K_Qrep(pi) by the least fixed point from the final LB_N line: add ordinary bit-explicit dependencies, transparent FormulaEval row dependencies, CTSR counterfactual children, and for every Qrep use add the representative row plus all lower-rank certificate dependencies already present in the prefix.
- Induct on proof lines. Ordinary Psys_bEF^- lines use the existing Gamma_bEF parser. Transparent FormulaEval lines contribute U_N+X_N. Qrep lines are simulated by substituting the charged representative expansion and the prior same-theory certificate forest; no new uncharged occurrence neighborhood is introduced.
- The circuit extracted from the parsed transcript evaluates H_N using the generator circuit, charged row support, SAT-substitution for exposed polylog queries, and equality patches for E_pi source-row failures, giving C_N(H_N)<=N^{rho+o(1)}+Gamma_Qrep(pi)+O(E_pi N).
- Contrapose the same-model lower-bound claim LB_N(1+epsilon). If the right side is subthreshold, the proof transcript itself is a valid upper-bound falsifier for the claimed source lower bound.
- For necessity, take the least line u violating strict prefix visibility. Hold all visible prefix bits fixed, flip the hidden private row or unread enable bit, and observe that the transcript before u is unchanged while the representative use can change the selected support or parity. This refutes hidden Qrep as transparent parsing.

Blocking gap: The derivation does not cover arbitrary semantic FormulaEval or adaptive SAT-pruning rules that may realize influence through real SAT semantics without exposing row identifiers; that remains RealSATInfluenceRealizer_N^{arb}.

## Falsifiers

- first representative use before certificate charge is a temporal private-row falsifier
- representative rebinding after prior use destroys prefix stability and invalidates Gamma_Qrep
- cyclic or nondecreasing-rank dictionary dependencies prevent a finite valid verifier
- advice-chosen quotient representatives create nonuniform leakage outside TransparentRowSupport_N
- hidden semantic SAT-pruning remains quarantined unless RealSATInfluenceRealizer_N^{arb} lists and charges the influence rows
- positive target-query exponent beta would reintroduce the black-box transfer cap q+beta c+o(1) and block all-exponent magnification
- subthreshold Gamma_Qrep(pi)+O(E_pi N) is an upper-bound falsifier for any claimed LB_N(1+epsilon) proof transcript

## Learning

Cycle 153 upgrades Qrep from prefix-verifiable syntax to a theorem-shaped TransparentRowSupport_N rule case: quotient compression is valid exactly as strict-prefix, ranked, proof-carrying, dependency-closed dictionary use. The new falsifier is temporal; delayed same-theory evidence is already hidden support. This is a scoped parser/falsifier contribution, not a lower bound for H_N and not P != NP progress.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the prefix-strict Qrep rule.`
- Rationale: The remaining ambiguity is temporal: acyclicity alone does not show that a quotient certificate is available before the proof uses the representative. A concrete private-row experiment separates valid proof-carrying compression from hidden semantic row deletion.
- Situation seed: A beta-zero parity carrier has two generated SAT rows A and B that are same-theory equivalent. A symbolic proof line tries to replace B by representative A in a FormulaEval support cone, either before or after a visible same-theory certificate cert(A,B) is charged.
- Varied variable: certificate lead time Delta=first_use_line(A<-B)-cert_line(A,B).
- Held-fixed controls: M_N=N^{q+o(1)}, q<1+epsilon, and L_N=(log N)^d with d>1 so the target transfer remains beta=0., The generator G_N, source-row equality patching cost O(N), and nonuniform SIZE circuit model are unchanged., The same-theory certificate language is fixed to SATeq/declared CTSR dependencies with ranked acyclic forests., No SAT-truth advice or hidden representative selection is allowed in the transparent case.
- Expected observation: For Delta>=1, the line induction can charge cert(A,B) before representative use. For Delta<=0, two private-row worlds agree on the visible prefix but disagree on the quotient-supported parity, producing an explicit falsifier for hidden Qrep transparency.
- Transfer certificate needed: A finite prefix verifier that records cert_line, first_use_line, ranks, dependency closure, and dictionary append-only status; only this certificate lets the intuition affect Gamma_Qrep proof obligations.

## Next Experiment

Instantiate the strict-prefix Qrep verifier on a two-duplicate projected-dDNNF FormulaEval example and a delayed-certificate counterexample; compute Gamma_bEF, U_N, X_N, D_Q, E_pi, and the q/epsilon support-density consequence line by line.
