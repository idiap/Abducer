# cycle-0100

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For explicit SR_h^bit inside Psys_bEF^-, every accepted proof pi has an advice-free parser whose bounded-SR contribution is the declared neighborhood sum B_SR(pi), hence the SR summand in Gamma_bEF is at most |K_idx(pi)|N^{eta+tau+o(1)}.

## Definitions

- source object: Psys_bEF^- proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), M_N=N^{q+o(1)}, L=(log N)^d, with bit-explicit EF, SATeq links, and one bounded-SR_h^bit rule.
- target object: advice-free occurrence transcript Q_pi and the induced nonuniform circuit upper bound for H_N^SAT over N-bit inputs.
- controlled interface: each SR_h^bit line has fields (tag,row j,parent p,node u,split mask z,child pointers c_b,formula-bit interval list I,node-neighborhood Nbr) verified syntactically.
- target-preserving condition: beta=0 polylog SAT instances, generator size N^{rho+o(1)}, no unexpanded FormulaEval-SAT, enumerable K_idx(pi), and extension supports traced through the EF DAG.
- observable: Nbr(j,u) is the list of generator-output bit positions needed to verify the local restriction from the parent formula at SR node u to its children.

## Assumptions

- Source model: Psys_bEF^- verifier is uniform and accepts only binary row indices, explicit formula-bit addresses, declared EF dependency pointers, and SATeq links between named encodings.
- SR regime: per row, the SR forest has at most N^{eta+o(1)} nodes and each node exposes at most N^{tau+o(1)} formula, pointer, and leaf-solver bits; fixed h or h=N^{o(1)} is absorbed in tau.
- Advice status: pi and Q_pi may be hardwired into the resulting circuit, but hidden SAT labels, private row answers, and semantic FormulaEval witnesses are not allowed.
- FormulaEval status: symbolic FormulaEval-SAT is excluded from Psys_bEF^- unless its RowSet and touched neighborhoods are expanded and charged outside B_SR(pi).

## Equations

- SR-neighborhood-charge: `B_{\mathrm{SR}}(\pi):=\sum_{(j,u)\in SR(\pi)}(|Nbr(j,u)|+|ptr(j,u)|+|leaf(j,u)|)\le |K_{idx}(\pi)|N^{\eta+\tau+o(1)}\le N^{q+\eta+\tau+o(1)}`. Valid when: Valid when Psys_bEF^- uses only bit-explicit SR_h lines, K_idx(pi) is explicitly enumerable, and each row has at most N^{eta+o(1)} SR nodes with N^{tau+o(1)} exposed bits.
- Gamma-bEF-split: `\Gamma_{\mathrm{bEF}}(\pi)=S_{dep}(\pi)+S_{link}(\pi)+B_{\mathrm{SR}}(\pi)+E_NN`. Valid when: Valid when EF dependencies, SATeq links, bounded-SR nodes, and sparse residual rows are disjoint charged transcript classes in the parsed proof.
- LB-falsifier-inequality: `N^{\rho+o(1)}+\Gamma_{\mathrm{bEF}}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow C(H_N^{SAT})<N^{1+\epsilon-o(1)}`. Valid when: Valid when the parsed transcript plus generator computes H_N^SAT except on E_N explicitly patched rows and no hidden semantic advice is used.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Hardness-Magnification Bridge Realization; source object: the branch-local proof object or transfer carrier named by this cycle; target object: the target theorem, obstruction, or upper-bound/countermodel handoff named by this cycle; validity regime/model condition: Source model: Psys_bEF^- verifier is uniform and accepts only binary row indices, explicit formula-bit addresses, declared EF dependency pointers, and SATeq links between named encodings.; SR regime: per row, the SR forest has at most N^{eta+o(1)} nodes and each node exposes at most N^{tau+o(1)} formula, pointer, and leaf-solver bits; fixed h or h=N^{o(1)} is absorbed in tau.; Advice status: pi and Q_pi may be hardwired into the resulting circuit, but hidden SAT labels, private row answers, and semantic FormulaEval witnesses are not allowed.; FormulaEval status: symbolic FormulaEval-SAT is excluded from Psys_bEF^- unless its RowSet and touched neighborhoods are expanded and charged outside B_SR(pi)..
- Fix the SR_h^bit line encoding: j uses ceil(log M_N) bits, node u uses eta log N+o(log N) bits, child pointers are proof-line indices, and every interval in I names generator-output bit positions.
- The parser traverses the transitive EF DAG, recomputes each local restriction map from the public generator bits, and appends (j,u,Nbr,ptr,leaf) to Q_pi only after syntactic verification.
- Line induction: EF lines add S_dep, SATeq lines add S_link, SR_h^bit lines add exactly their declared B_SR tuples, and sparse row failures are delayed to the E_NN equality-patching term.
- The generator circuit of size N^{rho+o(1)} plus hardwired Q_pi evaluates all charged rows and patches E_N residual rows, giving the displayed LB_N falsifier inequality.

Blocking gap: The derivation is valid only for Psys_bEF^-. Full Psys_sym remains blocked at FE_Extract_N: a symbolic FormulaEval-SAT line may select rows without exposing K_idx(pi) or Nbr(j,u).

## Falsifiers

- falsifier: a row selector stored as a circuit for RowSet rather than enumerated j values invalidates the valid SR charge and triggers FE_Extract_N.
- falsifier: a child formula produced by semantic FormulaEval-SAT rather than local restriction has the private-row countermodel and is outside Psys_bEF^-.
- falsifier: q+eta+tau>=1+epsilon causes threshold collapse, so the charged transcript no longer refutes LB_N(1+epsilon).
- falsifier: an EF extension variable with undeclared transitive support leaks advice; the parser must quarantine the proof instead of charging Gamma_bEF.

## Learning

Cycle 100 isolates the bounded-SR_h normal form at bit level: SR contributes exactly B_SR(pi) to Gamma_bEF for Psys_bEF^-. The remaining full-system obstruction is not generic soundness but FE_Extract_N for symbolic FormulaEval rows.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The top theorem now depends on whether symbolic FormulaEval can be converted to enumerated row neighborhoods; varying one selector density tests expansion charge versus private-row escape.
- Situation seed: For H_N^SAT, add one Psys_sym FormulaEval-SAT line over RowSet_a selected by an AC0 interval-union circuit, and compare its expanded row list with an unexpanded semantic line.
- Varied variable: alpha where |RowSet_a|=N^{alpha+o(1)}.
- Held-fixed controls: beta=0 polylog SAT instance length L=(log N)^d, M_N=N^{q+o(1)} and generator size N^{rho+o(1)}, SR_h^bit bounds eta,tau and no hidden SAT-label advice, the target lower-bound sentence LB_N(1+epsilon) and nonuniform circuit model
- Expected observation: Expansion costs N^{1+alpha+o(1)} row-bit slots; unexpanded use permits a private row flip with unchanged surface occurrences, separating semantic oracle power from valid occurrence parsing.
- Transfer certificate needed: A uniform RowSetEnumerator_N plus neighborhood extractor with the N^{1+alpha+o(1)} charge, or a nonrelativizing FE_Extract_N theorem; otherwise the line is quarantined as semantic-oracle escape.

## Next Experiment

Prove RowSetEnumerator_N for an interval-union or AC0 FormulaEval selector and compute alpha-charge; if enumeration fails, emit the minimal private-row countermodel.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For transparent Psys_sym^sel, FormulaEval-SAT row-expands with charge N E_N. Hence LB_N(1+epsilon) is falsified if the transcript bound is <N^{1+epsilon-o(1)}; with residual extraction, |K_idx|+E_N>=N^{epsilon-o(1)}.

## Definitions

- source object: accepted Psys_sym^sel proof pi of LB_N(1+epsilon) for H_N^SAT with FormulaEval-SAT selectors.
- target object: nonuniform SIZE upper-bound falsifier or forced row-support theorem for H_N^SAT.
- controlled interface: deterministic RowSetEnumerator_N outputs row indices for every FormulaEval selector and charges E_N.
- target-preserving condition: enumeration is uniform, advice-free, bit-explicit, and every emitted row expands into row-faithful SATeq/bounded-SR_h syntax.
- Sel_N consists of interval-union lists or DLOGTIME-uniform AC0 row predicates over [M_N]; AC0 without an output certificate is charged by full scan M_N.

## Assumptions

- N=2^n, M_N=N^{q+o(1)}, generator overhead is N^{rho+o(1)}, and row formulas have polylog N length.
- Proof length |pi|=N^{tau+o(1)} and bounded-SR_h arity/resource h=N^{eta+o(1)} are explicit in the verifier input.
- No semantic oracle is allowed: FormulaEval-SAT is an axiom schema, proof line, or extension rule only after RowSet(a) is enumerable from its bits.
- NoAdviceSemanticResidualExtractor_N is assumed only for the support corollary; the transcript upper-bound falsifier does not depend on it.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j<M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)},\quad |G_N|=(\log N)^{O(1)}`. Valid when: Valid when the beta-zero SAT parity carrier is fixed with explicit generator overhead N^{rho+o(1)}.
- selector_charge: `K_{idx}^+(\pi)=K_{idx}(\pi)\cup\bigcup_{a\in FE(\pi)} RowSet(a),\quad E_N=\sum_a charge(a),\quad |K_{idx}^+|\le |K_{idx}|+E_N`. Valid when: Applies after every FormulaEval selector is typed as transparent or charged by full enumeration.
- transcript_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+S_{dep}+S_{link}+N^{q+\eta+\tau+o(1)}+N E_N`. Valid when: Requires the row-expanded transcript, bEF line induction, and no-advice generator composition in the same length regime.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Barrier-Aware Lower-Bound Route; source object: the branch-local proof object or transfer carrier named by this cycle; target object: the target theorem, obstruction, or upper-bound/countermodel handoff named by this cycle; validity regime/model condition: N=2^n, M_N=N^{q+o(1)}, generator overhead is N^{rho+o(1)}, and row formulas have polylog N length.; Proof length |pi|=N^{tau+o(1)} and bounded-SR_h arity/resource h=N^{eta+o(1)} are explicit in the verifier input.; No semantic oracle is allowed: FormulaEval-SAT is an axiom schema, proof line, or extension rule only after RowSet(a) is enumerable from its bits.; NoAdviceSemanticResidualExtractor_N is assumed only for the support corollary; the transcript upper-bound falsifier does not depend on it..
- Selector typing: interval-union atoms list endpoints; AC0 atoms are DLOGTIME-uniform predicates over [M_N] and are charged by full scan M_N unless an output list certificate is present.
- Expansion: replace FormulaEval(a) by row-instantiated SATeq/bounded-SR_h lines for all j in RowSet(a). Each emitted row has explicit bit fields and occurrence neighborhoods.
- Circuit falsifier: compose the generator circuit of size N^rho with the row-expanded transcript. Dependency and link costs remain in Gamma_bEF; every new row costs O(N).
- Threshold: if the bound is below N^{1+epsilon-o(1)}, the alleged LB_N is false. If residual extraction is valid, small |K_idx|+E_N patches remaining rows.

Blocking gap: Unrestricted Psys_sym still allows FormulaEval(a) with semantic RowSet(a) not computable from bits of a; SelectorTransparency_N remains open.

## Falsifiers

- falsifier: a single semantic FormulaEval atom whose hidden selector is all [M_N] has displayed support 1 but requires E_N=M_N, so surface occurrence parsing is invalid.
- falsifier: a private-row selector with an unread enable bit changes one row of H_N without changing the surface proof, refuting a no-advice enumerator.
- falsifier: output-sensitive AC0 enumeration without a list or density certificate undercharges sparse predicates; the valid fallback is full M_N scan charge.
- falsifier: if q<epsilon and |K_idx|+E_N<N^{epsilon-o(1)}, the constructed circuit is below N^{1+epsilon}, so the source LB_N collapses.

## Learning

Cycle 100 adds a valid restricted RowSetEnumerator theorem: transparent FormulaEval is harmless only with explicit row enumeration and N E_N charge. Opaque FormulaEval remains a semantic falsifier, not a parser theorem.

## Gedanken Experiment Design Seed

- Need decision: `design_now_as_falsifier_probe`
- Rationale: The RowSetEnumerator gap is finite: varying one selector length exponent tests exactly when FormulaEval becomes charged support rather than semantic leakage.
- Situation seed: A Psys_sym^sel proof uses one FormulaEval selector S_b naming an interval block of L=N^beta rows among M_N=N^{q+o(1)} beta-zero SAT-parity rows.
- Varied variable: beta, the exponent of the selected row block length L=N^beta.
- Held-fixed controls: H_N^SAT carrier, generator overhead rho, and target SIZE lower-bound threshold N^{1+epsilon}., No-advice bit-explicit verifier and row-faithful SATeq/bounded-SR_h expansion., Proof exponents tau, eta, q and uniform interval endpoint encoding.
- Expected observation: Expansion costs N^{1+beta}; beta<epsilon gives a subthreshold falsifier if other charges are small, while beta>=epsilon supplies the forced support mass.
- Transfer certificate needed: A formal line-induction proof that interval endpoints enumerate exactly RowSet(S_b) and that each emitted row contributes one N-scale transcript charge.

## Next Experiment

Write the Psys_sym^sel verifier fields for interval-union FormulaEval, prove row-by-row line induction, and compute the exact Gamma_sym^sel threshold for beta<epsilon, beta=epsilon, and beta>epsilon.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For transparent Psys_sym^sel, each FormulaEval-SAT mechanism either has an advice-free RowSetEnumerator_N and pays N E_N expansion in Gamma, or it is a semantic-oracle escape with a private unread eval-critical bit countermodel.

## Definitions

- source object: accepted Psys_sym^sel proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)).
- target object: same-model nonuniform circuit upper bound for H_N^SAT, yielding a falsifier to LB_N when below N^{1+epsilon-o(1)}.
- controlled interface: FE_Extract_N maps each FormulaEval line to RowSet(a) of exposed (x,j,bit) occurrences, or marks the line semantic-oracle.
- target-preserving condition: extraction is uniform, advice-free, preserves G_N, M_N=N^{q+o(1)}, formula encoding, and the target circuit model.
- source statement: pi uses bit-explicit bEF/SATeq/bounded-SR_h plus classified FormulaEval-SAT lines.
- target statement: parsed transcript plus generator simulates H_N^SAT with cost N^{rho+o(1)}+Gamma_sym(pi).

## Assumptions

- Length regime N->infty; M_N=N^{q+o(1)}; each G_N(x,j) has log^{O(1)} N bits; rho,q,epsilon are fixed constants.
- Gap98-SRhNormalForm is inherited for Psys_bEF^-; Gamma_bEF(pi) is a valid line-induction ledger for non-FormulaEval rules.
- Transparent FormulaEval means the verifier uniformly enumerates every eval-critical occurrence used to bind row parity, with no advice or hardwired row selector.
- Semantic FormulaEval without UExtWitnessability is quarantined as a proof-system oracle, not a target-preserving MCSP/proof-certificate carrier.
- Barrier status: the parsed transcript is sparse and non-large; the obstruction is semantic oracle/advice leakage, not generic natural-proofs folklore.

## Equations

- FE-ledger: `\Gamma_{sym}(\pi)=\Gamma_{bEF}(\pi)+N\,E_N(\pi)`. Valid when: Valid when Psys_sym^sel uses transparent selectors and FE_Extract_N enumerates every eval-critical occurrence without advice.
- expansion-scale: `E_N(\pi)\ge M_N\log^{O(1)}N=N^{q+o(1)},\quad N E_N(\pi)\ge N^{1+q+o(1)}`. Valid when: Applies after row-parity binding forces all M_N generated SAT instances per row to be exposed in the parser.
- upper-bound-falsifier: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{sym}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Requires same nonuniform circuit model, uniform generator G_N, and parsed transcript implementing every SAT parity row.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside MCSP / Meta-Complexity Carrier Transfer; source object: the branch-local proof object or transfer carrier named by this cycle; target object: the target theorem, obstruction, or upper-bound/countermodel handoff named by this cycle; validity regime/model condition: Length regime N->infty; M_N=N^{q+o(1)}; each G_N(x,j) has log^{O(1)} N bits; rho,q,epsilon are fixed constants.; Gap98-SRhNormalForm is inherited for Psys_bEF^-; Gamma_bEF(pi) is a valid line-induction ledger for non-FormulaEval rules.; Transparent FormulaEval means the verifier uniformly enumerates every eval-critical occurrence used to bind row parity, with no advice or hardwired row selector.; Semantic FormulaEval without UExtWitnessability is quarantined as a proof-system oracle, not a target-preserving MCSP/proof-certificate carrier..
- Start with the proved Psys_bEF^- parser: every EF, SATeq, and bounded-SR_h line contributes to Gamma_bEF by bit-field and dependency traversal.
- For a FormulaEval line a, require RowSet(a) to list all formula bits whose variation can change SAT(G_N(x,j)) in any row parity used by pi.
- If RowSet omits an eval-critical bit for some (x*,j*), build two formula completions agreeing on the transcript but with opposite SAT value, so occurrence completion is not sound.
- If no such omission exists, the parser has exposed M_N polylog bits for each x, adding N^{1+q+o(1)} expansion and enabling the upper-bound falsifier when q<epsilon.

Blocking gap: RowSetEnumerator_N is still unproved for full Psys_sym; it is ready only for transparent selector fragments such as interval-union or AC0 row selectors.

## Falsifiers

- Private-row falsifier: an unread eval-critical formula bit at (x*,j*) gives two completions with identical transcript and different row parity.
- Advice leakage falsifier: RowSet chosen by a hardwired hard row set is not uniform and cannot transfer to the target language class.
- Threshold falsifier: if q>=epsilon, the N^{1+q+o(1)} expansion no longer gives a subthreshold refutation of LB_N(1+epsilon).
- Semantic-oracle falsifier: FormulaEval returning SAT truth without occurrence exposure is outside the controlled interface unless witnessed by an advice-free quotient.

## Learning

Cycle 100 converts the remaining FormulaEval-SAT fork into a finite theorem packet: transparent mechanisms pay N^{1+q+o(1)} expansion, while nontransparent ones face a private-row falsifier unless UExtWitnessability is valid. This supports the paper obstruction theorem only.

## Gedanken Experiment Design Seed

- Need decision: `design now`
- Rationale: The branch needs a concrete FormulaEval boundary test, not another MCSP slogan, because the remaining proof gap is exactly expansion versus private unread bit.
- Situation seed: A padded SAT-query family G_N^beta where H_N(x)=xor_{j<=N^q} SAT(G_N(x,j)); Psys_sym has a FormulaEval rule exposing only N^beta row-query occurrence records and semantically answering the rest.
- Varied variable: beta, the exponent of exposed row-query occurrence records, from beta<1+q to beta=1+q.
- Held-fixed controls: M_N=N^{q+o(1)} and each formula has polylogarithmic length., The target lower-bound sentence LB_N(1+epsilon) and nonuniform circuit model are unchanged., The generator G_N is uniform with overhead N^{rho+o(1)} and no advice., SATeq and bounded-SR_h subrules remain within the proved Psys_bEF^- parser.
- Expected observation: For beta<1+q an unread eval-critical pair should yield a private-row countermodel; at beta=1+q the parser pays full expansion and the low-cost proof claim loses its escape.
- Transfer certificate needed: A uniform RowSetEnumerator_N plus an eval-critical-bit lemma, or a formal UExtWitnessability certificate showing semantic equality is advice-free and target-preserving.

## Next Experiment

Instantiate RowSetEnumerator_N for interval-union selectors: write bit fields for row intervals, enumerate all (x,j,bit) contacts, prove E_N=N^{q+o(1)}, or exhibit the smallest unread eval-critical formula bit.
