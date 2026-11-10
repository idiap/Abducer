# cycle-0154

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Strict-prefix ranked Qrep quotient compression is a valid TransparentRowSupport_N rule case: every quotient representative used in a proof line can be replayed to an explicit same-theory row plus a previously charged certificate forest, so Gamma_Qrep supports the same parser-to-circuit falsifier as the uncompressed transparent proof.

## Definitions

- source object: beta-zero parity carrier H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, polylog formula length, generator size N^{rho+o(1)}, and proof transcript pi in Psys_sym^{Qrep}.
- target object: same-model nonuniform SIZE upper-bound falsifier for LB_N(1+epsilon) obtained from a charged proof parser, not a proof of H_N lower bounds or P != NP.
- controlled interface: TransparentRowSupport_N with bit-explicit bEF lines, bounded SR_h rows, FormulaEval support cone K, counterfactual TSR rows, and ranked proof-carrying Qrep dictionary entries charged before representative use.
- target-preserving condition: the replay must preserve the carrier rows, the nonuniform SIZE model, q,rho,epsilon thresholds, advice-freeness of row selection, and same-theory SAT equivalence certificates before any quotient use.

## Assumptions

- Length regime: N grows through valid carrier lengths; M_N=N^{q+o(1)} with q<1+epsilon; generator overhead is N^{rho+o(1)} with rho<1+epsilon.
- Proof-system regime: pi is a finite Psys_sym^{Qrep} transcript whose Qrep entry e=(r_e,rep_e,sigma_e,rank_e,t_e) is syntactically declared at line t_e before any line using rep_e for r_e.
- Uniformity/advice regime: K_Qrep(pi) and every same-theory certificate forest are computable from N and pi; no SAT-truth advice, hidden selector advice, or post-use rebinding is allowed.
- Barrier status: the lemma is syntactic and label-relativizing; it deliberately does not realize full real-SAT semantic pruning. The nonrelativizing RealSATInfluenceRealizer_N^{arb} remains outside the claim.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad |G_N(x,j)|=(\log N)^d.`. Valid when: Valid when the beta-zero parity carrier has explicit generator G_N, polylog target formulas, and all slots are indexed without advice.
- qrep_ledger: `\Gamma_{Qrep}(\pi)=\Gamma_{bEF}(\pi)+U(K_{Qrep})+X(K_{Qrep})+\sum_{e\in Dict(\pi)}(|\sigma_e|+|row(e)|)\,N^{o(1)}.`. Valid when: Valid when K_Qrep(pi) is the least strict-prefix support closure and every dictionary certificate is charged before representative use.
- parser_upper_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{Qrep}(\pi)+O(E_\pi N).`. Valid when: Valid when the line induction is performed in the same nonuniform SIZE model and equality patches charge every residual bad row.
- lb_falsifier_window: `N^{\rho+o(1)}+\Gamma_{Qrep}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon).`. Valid when: Applies when LB_N(1+epsilon) asserts a same-model N^{1+epsilon-o(1)} lower bound for the named carrier.
- support_density_corollary: `LB_N(1+\epsilon)\wedge \rho<1+\epsilon\Rightarrow |K_{idx}(\pi)|\ge N^{\epsilon-o(1)},\quad |K_{idx}|/M_N\ge N^{\epsilon-q-o(1)}.`. Valid when: Requires the claimed LB_N(1+epsilon) to survive the parser upper bound and M_N=N^{q+o(1)} slots.

## Attempted Derivation

- Define K_Qrep^t by prefix recursion: start with bEF, SR_h, FormulaEval, and CTSR visible supports; when a Qrep dictionary entry e appears, add its row endpoints and certificate footprint only if every dependency is already in K_Qrep^{<t} and every rank decreases.
- For non-Qrep lines, reuse the existing Gamma_bEF/Gamma_dag/CTSR line-induction invariant: each parsed proof dependency either contributes a charged row or is already in the support cone.
- For a Qrep use at line t, replace the quotient representative by the row rep_e plus the strict-prefix same-theory certificate forest sigma_e. Since sigma_e is already charged, the replay adds no post-hoc support and preserves the carrier row semantics used by the parser.
- Compose all replays in line order. Rank decrease and prefix ordering prevent cycles and representative rebinding, so the expanded proof has the same final LB_N line and total support bounded by Gamma_Qrep.
- Build the nonuniform circuit for H_N from the generator circuit, parsed row computations, charged FormulaEval/TSR/Qrep support, and equality patches for E_pi residual rows, obtaining C(H_N)<=N^{rho+o(1)}+Gamma_Qrep+O(E_pi N).
- Contrapose the claimed source lower bound LB_N(1+epsilon): if the displayed upper bound is below N^{1+epsilon-o(1)}, the claimed proof-mediated lower-bound certificate is falsified in the same model.
- For necessity, choose the first unsafe quotient use. Keep the visible prefix fixed, toggle an uncharged private row or unread enable bit that controls same-theory status, and obtain two worlds with identical accepted prefix but different uncovered parity or certificate truth.

Blocking gap: The derivation does not cover arbitrary semantic SAT branch pruning or FormulaEval rules whose influencing rows are not determined by proof syntax before use; this is exactly RealSATInfluenceRealizer_N^{arb}.

## Falsifiers

- First late Qrep merge: representative used before its same-theory certificate is charged, producing a private-row falsifier.
- Rank cycle or representative rebinding: replay is not well-founded, so Gamma reduction is invalid.
- Advice-chosen dictionary: K_Qrep is not determined by N and pi, causing nonuniform leakage.
- Hidden semantic pruning: the proof uses real SAT structure without listing influencing rows, blocked at RealSATInfluenceRealizer_N^{arb}.
- Positive beta black-box substitution remains a separate threshold-collapse falsifier: q+beta c can exceed 1+epsilon before all SAT exponents are excluded.

## Learning

Cycle 154 converts strict-prefix Qrep from a syntax convention into a replay theorem with a matching temporal falsifier. The valid contribution is a restricted TransparentRowSupport_N rule case and Formula Footprints supporting lemma: charged, ranked, dependency-closed dictionary compression preserves Gamma line induction; delayed or hidden compression is exactly hidden support. This is route-level certification only, not a lower bound for H_N and not P vs NP progress.

## Gedanken Experiment Design Seed

- Need decision: `use_concrete_thought_experiment_now`
- Rationale: The branch is no longer testing a broad magnification slogan; it must decide whether temporal quotient compression is a valid transparent support rule or a hidden-support leak.
- Situation seed: A beta-zero XOR carrier with M_N=N^{q+o(1)} generated SAT rows and a Psys_sym proof whose CTSR frontier creates two syntactically different but same-theory child rows r0,r1; Qrep may merge r1 into representative r0.
- Varied variable: certificate delay Delta, the number of proof lines between first representative use and the line where the same-theory certificate for r1~r0 is surfaced and charged.
- Held-fixed controls: M_N=N^{q+o(1)}, rho<1+epsilon, and polylog SAT formula length are fixed., The visible proof prefix, generator G_N, charged bEF/SR_h/FormulaEval/CTSR supports, and nonuniform SIZE model are fixed., No SAT-truth advice or advice-chosen row selector is allowed., The final LB_N(1+epsilon) assertion and residual patch budget E_pi are fixed.
- Expected observation: For Delta=0 with strict-prefix charging, replay preserves Gamma_Qrep and the parser upper bound is valid. For any Delta>0 at the first use, a private-row or unread-enable-bit world can agree on the visible prefix while changing the uncharged merge, so free compression is invalid.
- Transfer certificate needed: A strict-prefix RealSATInfluence certificate: before representative use, proof syntax must uniformly list the merged rows, a same-theory certificate forest, rank-decreasing dependencies, and the exact Gamma charge.

## Next Experiment

Run the prefix-scan verifier on one minimal proof with a valid two-row strict-prefix Qrep merge and on one identical proof with the certificate delayed by one line; compute Gamma_Qrep in both cases and export the rejected line as the private-row falsifier pivot.
