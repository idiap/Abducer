# cycle-0146

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For the beta-zero parity carrier, a Psys_sym^{QCTSR} proof with transparent FormulaEval, complete counterfactual TSR children, and ranked dependency-closed same-theory quotient certificates has a valid finite parser ledger Gamma_QCTSR. If N^{rho+o(1)}+Gamma_QCTSR(pi)<N^{1+epsilon-o(1)}, the claimed LB_N(1+epsilon) is falsified in the same nonuniform circuit model. This is a scoped parser/falsifier theorem, not a lower bound and not P != NP.

## Definitions

- source object: H_N^{SAT}(x)=xor_{j<M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, polylog SAT instances, generator circuit size N^{rho+o(1)}, and source lower-bound claim LB_N(1+epsilon) against SIZE(N^{1+epsilon-o(1)}).
- target object: a same-model upper-bound falsifier for LB_N(1+epsilon), obtained from a parsed proof transcript and sparse residual row patching; the target is not NP not subset P/poly.
- controlled interface: Psys_sym^{QCTSR} consists of bit-explicit EF lines, transparent FormulaEval support, counterfactual declared bounded-TSR children, and quotient compression only through ranked acyclic same-theory certificate forests.
- target-preserving condition: every influence row used by the proof is uniformly enumerable or fully scanned before use, every quotient deletion has a charged same-theory certificate in the current closure, query length has beta=0, and no semantic SAT-truth advice selects rows.
- K_Q(pi) is the least fixed point seeded by the final LB_N line and closed under EF parents, FormulaEval influence rows, all counterfactual TSR children, same-theory certificate dependencies, and accepted quotient representatives.
- A quotient merge r -> r' is accepted only if the verifier sees a certificate forest proving same-theory equivalence of r and r', all certificate leaves already lie in K_Q(pi), and the certificate rank strictly decreases along dependency edges.
- Gamma_QCTSR(pi) is the charged parser ledger Gamma_bEF(pi)+U_Q(pi)+X_Q(pi)+B_CTSR(pi)+C_Q(pi)+O(E_pi N), where E_pi is the residual row-error count patched by equality gates.

## Assumptions

- Circuit model is nonuniform Boolean SIZE over length N; the source upper bound and the falsified LB_N claim are interpreted in the same model.
- Length regime has M_N=N^{q+o(1)}, SAT instance length L_N=(log N)^d with d>1 or any beta=0 polylog regime, and generator overhead N^{rho+o(1)}.
- Proof syntax is advice-free: K_Q(pi), ranks, certificates, and row indices are computable from N and the displayed proof pi, not from SAT truth labels.
- FormulaEval is restricted to transparent extensional support or a full-scan charge; full hidden semantic FormulaEval remains quarantined at RealSATInfluenceRealizer_N^{arb}.
- Counterfactual TSR is complete: for every reachable restriction node, all children in the bounded rule schema are declared before pruning or quotienting.
- Same-theory certificates are syntactic objects checked inside the parser; semantic equality of SAT values without a certificate is not admissible.
- Residual errors satisfy E_pi<N^{epsilon-o(1)} when invoking the sparse-row patching falsifier.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j<M_N} SAT(G_N(x,j)), \quad M_N=N^{q+o(1)}.`. Valid when: Valid when the source carrier is the beta-zero generated parity construction and the generator outputs polylogarithmic SAT instances.
- ledger: `\Gamma_{QCTSR}(\pi)=\Gamma_{bEF}(\pi)+U_Q(\pi)+X_Q(\pi)+B_{CTSR}(\pi)+C_Q(\pi)+O(E_\pi N).`. Valid when: Valid when every proof rule is parsed through visible support, complete counterfactual children, and ranked same-theory quotient certificates.
- ctsr_charge: `B_{CTSR}(\pi)\le N^{1+\kappa+\theta+o(1)} \text{ for } N^{\kappa+o(1)} \text{ frontier rows and } N^{\theta+o(1)} \text{ children per row}.`. Valid when: Applies when the bounded TSR schema declares all counterfactual children uniformly before adaptive pruning or quotient compression occurs.
- falsifier_window: `N^{\rho+o(1)}+\Gamma_{QCTSR}(\pi)<N^{1+\epsilon-o(1)} \Rightarrow \neg LB_N(1+\epsilon).`. Valid when: Requires the parser-to-circuit construction, same nonuniform SIZE model, and residual row patching below the N^epsilon threshold.
- density_corollary: `|K_Q(\pi)|\ge N^{\epsilon-o(1)} \quad \text{or} \quad |K_Q(\pi)|/M_N\ge N^{\epsilon-q-o(1)}.`. Valid when: Valid when each surfaced row has N-cost expansion and the claimed lower-bound proof is not already falsified by Gamma_QCTSR.

## Attempted Derivation

- Define K_Q^0(pi) as the row, proof-line, and certificate seeds syntactically referenced by the final LB_N assertion.
- Iterate closure: add EF parent rows and extension-support rows; for FormulaEval lines add the enumerated RowSet or charge the full scan; for CTSR lines add every counterfactual child row in the bounded rule schema.
- For each quotient deletion r -> r', require a displayed same-theory certificate forest F_{r,r'} with a rank label. Add every leaf and internal dependency of F_{r,r'} to K_Q before accepting the deletion.
- Check acyclicity by requiring rank(child)<rank(parent) along certificate-dependency edges. This makes the verifier finite and prevents cyclic quotient justification.
- Define Gamma_QCTSR as the sum of existing Gamma_bEF charges, support-enumeration cost U_Q, row-expansion cost X_Q=N|K_Q| up to encoding overhead, complete CTSR child cost, certificate-checking cost C_Q, and residual patch cost O(E_pi N).
- Prove the line invariant: after line t, the partial circuit using only rows in K_Q^{<=t} agrees with the proof transcript on all surfaced influences; quotient representatives are safe because same-theory certificates are already available and ranked.
- At the final line, compose the generator circuit for G_N with the parsed transcript circuit and add equality patches for E_pi residual source rows. The total size is N^{rho+o(1)}+Gamma_QCTSR(pi)+O(E_pi N).
- If this total is below N^{1+epsilon-o(1)}, the asserted LB_N(1+epsilon) is false in the same nonuniform SIZE model; this is the route-level falsifier conclusion.
- For necessity, take the first quotient merge that fails the finite verifier. Create two private-row worlds agreeing on K_Q and all accepted certificates but differing on the uncharged deleted row. The proof sees the same transcript while carrier parity can differ, so unranked compression is not a valid parser rule.

Blocking gap: The derivation does not fold arbitrary hidden semantic FormulaEval or adaptive SAT branch pruning into K_Q. That remains the named RealSATInfluenceRealizer_N^{arb} problem.

## Falsifiers

- first unranked quotient merge: a private row can be flipped while all charged rows and verifier bits stay fixed
- cyclic certificate forest: rank check fails, allowing circular deletion with no same-theory support
- advice-chosen quotient representative: nonuniform leakage selects the surviving row without paying K_Q or C_Q
- actual-branch-only TSR declaration: a hidden counterfactual child yields the first-hidden-child falsifier
- semantic FormulaEval without RealSATInfluenceRealizer_N^{arb}: unread-enable-bit row affects the proof but is absent from Gamma_QCTSR
- positive beta black-box interface: q+beta*c+o(1) caps all-exponent transfer and invalidates P/poly conclusions

## Learning

Cycle 146 upgrades ranked QCTSR from a finite local verifier to a composable fixed-point line-induction theorem: quotient compression is valid only when proof-carrying same-theory certificates are ranked, acyclic, dependency-closed, and charged before use. The first rejected merge is a concrete private-row falsifier. This strengthens the transparent-support parser/countermodel paper module while preserving all nonclaims: no H_N lower bound, no P != NP result, and no free hidden semantic FormulaEval.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The current proof packet hinges on whether quotient compression is proof-carrying or semantic. A concrete thought experiment tests the exact boundary without broadening into MCSP or generic barriers.
- Situation seed: Take H_N^{SAT}(x)=xor_{j<N^q} SAT(G_N(x,j)) with polylog formulas. Build a counterfactual TSR proof tree where many children are syntactically duplicate after Tseitin renaming. Allow quotient compression by merging rows claimed to be same-theory equivalent.
- Varied variable: alpha, the exponent of quotient merges that lack ranked same-theory certificates before use, with alpha=0 meaning fully certified QCTSR and alpha>0 meaning hidden semantic compression.
- Held-fixed controls: M_N=N^{q+o(1)} and beta=0 polylog query length are fixed., Generator overhead remains N^{rho+o(1)} and uses no SAT-truth advice., The verifier may inspect only proof syntax, charged rows, ranks, and displayed same-theory certificate bits., Residual patching threshold remains E_pi<N^{epsilon-o(1)}.
- Expected observation: At alpha=0, Gamma_QCTSR accounts for every remaining influence and the line induction is valid. For any first alpha>0 unranked merge, two private-row worlds agree on the charged transcript but differ on the deleted row, producing a falsifier for semantic quotient compression.
- Transfer certificate needed: A finite rank verifier plus dependency-closed certificate ledger showing every quotient deletion is justified before use; otherwise a nonrelativizing RealSATInfluenceRealizer_N^{arb} must replace the private-row model.

## Next Experiment

Run the finite verifier on one projected-dDNNF/Tseitin-renaming example: list K_Q seeds, accepted quotient certificates, rank labels, computed Gamma_QCTSR, and then delete one certificate to exhibit the first-rejected-merge private-row falsifier.
