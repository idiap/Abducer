# cycle-0120

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization: least-closed transparent FormulaEval support

## Candidate Lemma

LeastClosedTransparentSupport_N: for Psys_sym^dag proofs whose FormulaEval lines expose a syntactic dependency DAG, it is enough and necessary to charge the least prefix-closed reachable support cone K_dag(pi) from the final LB_N line; line induction then gives a same-model parser-to-circuit falsifier, while any reachable uncharged influence has a private-row countermodel.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}, |G_N|<=N^{rho+o(1)}, and each generated formula length L_N=(log N)^{d+O(1)} so beta=0.
- target object: the proof-system claim LB_N(1+epsilon), asserting C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)} in the same nonuniform Boolean circuit model used by the parser falsifier.
- controlled interface: a Psys_sym^dag transcript pi with bit-explicit bEF lines, bounded-SR_h rules, and FormulaEval nodes carrying visible selector code plus dependency edges from later symbolic uses to earlier row supports.
- target-preserving condition: every charged support row is realized advice-free in the same proof theory, the dependency cone is prefix-closed before use, SAT circuits are substituted only through beta=0 polylog queries, and no hidden semantic advice enters K_dag(pi).
- K_dag(pi) is the least fixed point containing all FormulaEval support tokens reachable from the final LB_N assertion through dependency edges, closed under earlier rows needed to justify each token.
- U(K) is the certified enumeration or full-scan cost for producing the row indices in K; X(K) is the occurrence-expansion cost for the corresponding generated SAT rows.

## Assumptions

- Circuit model is nonuniform SIZE over fan-in two Boolean circuits; equality patches for E bad N-bit source rows cost O(E N) gates.
- Length regime is N -> infinity, M_N=N^{q+o(1)}, L_N=polylog N, q,rho<1+epsilon, and all o(1) losses are uniform over fixed epsilon,q,rho,d,h.
- Psys_sym^dag has explicit parent pointers and same-theory verification of row enumerators; FormulaEval is extensional only over surfaced row tokens, not over arbitrary real-SAT semantic consequences.
- Bounded-SR_h contributes eta,tau overhead through the previously proved SR_h bit-normal form; no step upgrades this theorem to full EF+SAT without RealSATInfluenceRealizer_N.
- The necessity direction is valid for extensional or oracle-style FormulaEval worlds; for real SAT semantics it becomes a no-go test unless a nonrelativizing realizer supplies charged supports.

## Equations

- carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)}`. Valid when: Valid when the source object is the beta-zero generated parity carrier with uniformly computable generator slots.
- least_closed_cost: `\Gamma_{dag}(\pi)=\Gamma_{bEF}(\pi)+U(K_{dag}(\pi))+X(K_{dag}(\pi))+O(|\pi|\,\mathrm{polylog}\,N)`. Valid when: Valid when Psys_sym^dag exposes parent pointers, dependency edges, and advice-free row enumeration certificates.
- falsifier_upper_bound: `C(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{dag}(\pi)+O(E_\pi N)`. Valid when: Applies after the line induction preserves same-model circuits and sparse row errors are equality patched.
- subthreshold_negation: `N^{\rho+o(1)}+\Gamma_{dag}(\pi)+O(E_\pi N)<N^{1+\epsilon-o(1)}\Rightarrow \neg LB_N(1+\epsilon)`. Valid when: Requires the target-preserving same-model transfer and the claimed LB_N threshold in nonuniform SIZE.
- support_density_corollary: `|K_{dag}(\pi)|\ge N^{\epsilon-o(1)},\quad |K_{dag}(\pi)|/M_N\ge N^{\epsilon-q-o(1)}`. Valid when: Valid when each complete surfaced parity row costs N^{1+o(1)} to realize and rho is subthreshold.

## Attempted Derivation

- Define the live inference source statement: Psys_sym^dag proves LB_N(1+epsilon) for H_N^SAT with beta=0, q,rho<1+epsilon, bit-explicit bEF support, bounded-SR_h normal form, and FormulaEval dependency DAGs.
- Define the live inference target statement: if pi has N^{rho+o(1)}+Gamma_dag(pi)+O(E_pi N)<N^{1+epsilon-o(1)}, then the same nonuniform SIZE model has circuits for H_N^SAT below the claimed lower-bound threshold; hence that pi is a falsifier for LB_N(1+epsilon), not evidence for P != NP.
- Build K_dag(pi) as a least fixed point: seed with FormulaEval tokens used by the final LB_N line, close under explicit parent pointers, row enumerator certificates, SR_h leaf rows, and symbolic aliases that feed any retained line.
- Run line induction only on the retained cone. Bit-explicit bEF lines use the existing Gamma_bEF charge; bounded-SR_h lines add eta/tau-normalized row costs; transparent FormulaEval lines add U(K)+X(K). Unreachable FormulaEval rows are ignored by UnreachableSupportDeletion_N.
- Substitute a hypothetical SAT circuit of size L_N^c into each generated formula. Because L_N=polylog N, every fixed c contributes N^{o(1)} per surfaced row; generator plus transcript costs give C(H_N)<=N^{rho+o(1)}+Gamma_dag(pi)+O(E_pi N).
- Derive the density corollary: any valid proof certificate for LB_N(1+epsilon) inside this parser model must force at least N^{epsilon-o(1)} reachable complete parity rows, equivalently density N^{epsilon-q-o(1)} among M_N=N^{q+o(1)} slots when q is fixed.
- Prove necessity for the extensional case by choosing the earliest reachable uncharged influence. Flip its private row or unread enable bit while keeping charged transcript data fixed; the verifier sees the same prior cone but the final induced parity differs, contradicting sound surface occurrence completion.
- Reviewer packet status: reduction consistency is valid for beta=0 same-model substitution; quantifier uniformity is fixed over q,rho,epsilon,h,d; barrier specificity says the countermodel relativizes only for extensional/oracle FormulaEval, while the real SAT escape is the named nonrelativizing RealSATInfluenceRealizer_N.

Blocking gap: Full semantic FormulaEval over real SAT is still blocked at RealSATInfluenceRealizer_N: no proof currently converts semantic influence of an uncharged formula row into an advice-free, prefix-closed, charged support certificate.

## Falsifiers

- Reachable hidden support falsifier: an uncharged row in the final dependency cone permits two extensional transcripts agreeing on all charged data while differing on the induced parity carrier.
- Unread-enable-bit falsifier: a selector bit that can activate a row after its enumerator certificate is checked invalidates Gamma_dag unless the activation edge is prefix-closed and charged.
- Subthreshold transcript falsifier: N^{rho+o(1)}+Gamma_dag(pi)+O(E_pi N)<N^{1+epsilon-o(1)} gives an explicit small circuit for H_N^SAT in the same model, refuting the source LB_N certificate.
- q<epsilon support-density falsifier: if fewer than N^{epsilon-o(1)} reachable complete rows are forced among M_N=N^{q+o(1)} slots, equality patching and the transcript circuit stay below the claimed threshold.
- Semantic-realizer falsifier probe: if a claimed full FormulaEval rule influences a proof without producing RealSATInfluenceRealizer_N rows, the branch treats it as outside the valid parser theorem rather than as transparent support.

## Learning

Cycle 120 strengthens the promoted theorem pair by identifying the minimal valid charged object: the least prefix-closed reachable FormulaEval support cone K_dag(pi), not the full selector zoo. The positive line induction uses Gamma_dag=Gamma_bEF+U(K_dag)+X(K_dag), and the necessity side is a first-hidden-reachable-row falsifier. Full semantic FormulaEval remains quarantined exactly at RealSATInfluenceRealizer_N; this is a scoped parser/falsifier contribution, not progress toward proving P != NP.

## Gedanken Experiment Design Seed

- Need decision: `Design and use now as a falsifier probe for the necessity half of the theorem pair.`
- Rationale: The branch already has a positive transparent-support theorem; the remaining risk is hidden compositional influence. A concrete dependency-cone experiment tests whether least-closed support is the right charged object rather than another abstract support slogan.
- Situation seed: Take H_N^SAT with M_N=N^{q+o(1)} polylog SAT slots and a Psys_sym^dag proof whose final LB_N line depends on a FormulaEval node e. Let e read a selector output for slot r only through a later symbolic alias, with r absent from the current charged cone.
- Varied variable: Closure radius a in the dependency DAG, from a=0 at the final LB_N line to the first radius a* where the hidden row r becomes reachable.
- Held-fixed controls: Keep beta=0, L_N=polylog N, q,rho<1+epsilon, and the same nonuniform SIZE target model fixed., Keep the generator G_N, all charged row labels, all bEF and bounded-SR_h verifier fields, and the equality-patching budget E_pi fixed., Keep FormulaEval extensional rather than real-SAT semantic, so private-row flips are legitimate until a RealSATInfluenceRealizer_N certificate is supplied.
- Expected observation: For a<a*, two worlds agree on every charged transcript item but can differ on the final parity assertion; at a=a*, charging r restores line-induction validity and increases Gamma_dag by the certified row-realization cost.
- Transfer certificate needed: A formal last-unsafe-line lemma for extensional FormulaEval, plus a separate nonrelativizing RealSATInfluenceRealizer_N theorem before the same intuition may be applied to full real-SAT semantic FormulaEval.

## Next Experiment

Write the proof-audit version of L120.1: formalize the fixed-point computation of K_dag(pi), give pseudocode for the verifier-visible dependency closure, and check one projected-dDNNF FormulaEval example plus one unread-enable-bit counterexample against the Gamma_dag inequality.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

Prefix-scoped TransparentRowSupport_N expansion theorem: every accepted Psys_sym proof whose FormulaEval lines satisfy the finite TRS interface can be conservatively spliced into a row-expanded Psys_bEF transcript with canonical charge Gamma_trans, yielding the same-model parser-to-circuit falsifier and the debt-or-density lower bound on visible support.

## Definitions

- source object: an accepted Psys_sym^TRS proof pi of LB_N(1+epsilon) for H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)), with N=2^n, M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, and bit-explicit bEF base rules.
- target object: a row-expanded Psys_bEF transcript pi^exp plus a nonuniform SIZE upper-bound certificate for H_N^SAT in the same Boolean circuit model targeted by LB_N.
- controlled interface: each FormulaEval line a carries visible selector code c_a, a deterministic row enumerator Enum_a, selector extensionality proof, influence-closure list I_a, same-theory row-expansion templates E(a,j), and no hidden support advice.
- target-preserving condition: expansion uses only bEF/SATeq/bounded-SR_h rules with fresh extension variables tagged by (line,row,occurrence), preserves row-index bits and parent pointers, and is produced by a deterministic no-advice parser.

## Assumptions

- Circuit model is nonuniform Boolean SIZE; the proof-to-circuit step is simulation/extraction, not a many-one reduction and not a proof of P != NP.
- LB_N(1+epsilon) means the proof asserts C_SIZE(H_N^SAT)>N^{1+epsilon-o(1)} on the same length regime used by the generator and transcript.
- Every bEF line has the existing bit-explicit parser charge Gamma_bEF(pi), including SATeq and bounded-SR_h row-occurrence neighborhoods.
- For every FormulaEval line a, Enum_a lists exactly RowSet(a); every row capable of changing the line value is in I_a subseteq RowSet(a).
- Same-theory expansion is prefix-spliced immediately before line a; fresh extension-variable hygiene forbids aliasing between different row expansions or earlier proof lines.
- Uniformity/advice condition: the parser, enumerators, row templates, and charge accounting are computable from pi and N with no semantic advice about SAT truth values.

## Equations

- canonical_charge: `Gamma_trans(pi)=Gamma_bEF(pi)+U_N(pi)+X_N(pi)`. Valid when: Valid when every FormulaEval line carries a TRS certificate whose enumerator and row-expansion costs are explicitly charged.
- row_equivalent_support: `S_hat_eff(pi)=ceil(Gamma_trans(pi)/N)`. Valid when: Valid when one charged row expansion costs N^{1+o(1)} bits in the beta-zero carrier normalization.
- same_model_upper_bound: `C_SIZE(H_N^SAT)<=N^{rho+o(1)}+O(Gamma_trans(pi) polylog N)`. Valid when: Applies after the row-expanded transcript is produced in the same Boolean SIZE model without hidden advice.
- forced_debt: `LB_N(1+epsilon) and rho<1+epsilon imply S_hat_eff(pi)>=N^{epsilon-o(1)}`. Valid when: Requires the lower-bound statement and the extracted upper-bound falsifier to use identical length and circuit-size parameters.
- visible_density: `if M_N=N^{q+o(1)} and Gamma_bEF+U_N=o(N^{1+epsilon}), then |K_idx_FE(pi)|/M_N>=N^{epsilon-q-o(1)}`. Valid when: Valid when FormulaEval expansion charge is X_N=N^{1+o(1)}|K_idx_FE(pi)| and non-FE debt is subthreshold.

## Attempted Derivation

- Linearly scan pi. Copy ordinary bEF, SATeq, and bounded-SR_h lines into pi^exp with their existing Gamma_bEF charge and parent pointers.
- For each FormulaEval line a, verify the TRS fields: visible selector code, RowSet enumerator, selector extensionality, influence closure, same-theory expansion template, and no-hidden-advice flag.
- Run Enum_a and insert, immediately before line a, row blocks E(a,j) for j in RowSet(a), using fresh extension variables tagged by (a,j,local_occurrence).
- Add a short link block proving that the original FormulaEval conclusion follows from the expanded row blocks; charge enumeration time to U_N and row material to X_N.
- Maintain prefix derivability by retargeting later parent pointers to the endpoint of the inserted link block; freshness prevents accidental semantic sharing between row blocks.
- Apply the existing bEF parser-to-circuit lemma to pi^exp. This gives C_SIZE(H_N^SAT)<=N^{rho+o(1)}+O(Gamma_trans polylog N).
- If pi proves LB_N(1+epsilon), rho<1+epsilon, and Gamma_trans<N^{1+epsilon-o(1)}, the extracted circuit is a same-model falsifier to the asserted lower bound.
- Dividing Gamma_trans by the N-per-row normalization yields S_hat_eff>=N^{epsilon-o(1)}. If bEF and enumeration debt are lower order, the visible FormulaEval row density is at least N^{epsilon-q-o(1)}.
- For a non-TRS semantic line, instantiate the unread-enable-bit construction: two proofs have identical visible transcript and charge, but the hidden row changes the FormulaEval value or carrier parity, so no surface parser is valid.

Blocking gap: The restricted TRS expansion is derivable modulo the already accepted bEF parser-to-circuit lemma. The unrestricted semantic lift is blocked exactly at RealSATInfluenceRealizer_N.

## Falsifiers

- Subthreshold-charge falsifier: Gamma_trans<N^{1+epsilon-o(1)} with rho<1+epsilon yields a same-model SIZE upper bound contradicting LB_N(1+epsilon).
- Private-row/unread-enable-bit falsifier: a hidden influencing row changes FormulaEval while the visible transcript and Gamma_surface remain fixed.
- Extension-aliasing falsifier: if row blocks reuse extension variables, the prefix splice may prove non-conservative equalities not present in row-expanded bEF.
- Selector-extensionality falsifier: two selector codes with the same displayed surface but different RowSet values break the valid charge equation unless extensionality is proved.

## Learning

Cycle 120 adds a proof-hygiene closure: TRS expansion must be prefix-scoped with fresh extension variables, after which Gamma_trans is a valid same-theory charge and yields the forced row-equivalent support theorem. The unrestricted semantic case is not broadened; it is blocked at RealSATInfluenceRealizer_N and refuted by the private-row falsifier when that bridge is absent.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe for the unrestricted semantic FormulaEval lift.`
- Rationale: The top proof item is blocked only if hidden semantic support can affect FormulaEval without charged rows; a concrete private-row experiment tests exactly that target-preserving condition.
- Situation seed: Build a Psys_sym semantic FormulaEval atom A_e that evaluates the same displayed SAT formula family but includes one private enable bit e_b selecting row b of H_N^SAT; the visible proof, selector code, and parent pointers never mention b.
- Varied variable: The number t of hidden enabled rows, starting with t=1 and increasing to t=N^{alpha}.
- Held-fixed controls: Carrier H_N^SAT(x)=xor_{j<M_N} SAT(G_N(x,j)) with M_N=N^{q+o(1)}., Target lower-bound claim LB_N(1+epsilon) in nonuniform Boolean SIZE., Generator size N^{rho+o(1)} and beta-zero row length regime., Deterministic no-advice parser and identical visible proof transcript., TRS charge definition counting only verifier-visible row support.
- Expected observation: For t=1 the visible charge is unchanged while the semantic value can flip; for t=N^{alpha} the gap between true influence and charged support grows polynomially, showing surface occurrence parsing is invalid without a realizer.
- Transfer certificate needed: A RealSATInfluenceRealizer_N certificate that outputs all t hidden rows, proves their influence closure, and charges either enumeration debt U_N or full row expansion X_N before the intuition may enter the proof queue.

## Next Experiment

Write the paper-ready prefix-splice proof with explicit row-block syntax, fresh extension-variable tags, parent-pointer retargeting, and then run the t-hidden-row thought experiment to validate the private-row countermodel at t=1 and t=N^{alpha}.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Minimal-bad-line TransparentRowSupport_N theorem. For Psys_sym^TRS extending the bit-explicit Psys_bEF^- parser by transparent FormulaEval lines, every accepted proof pi has an occurrence transcript Q_pi with cost Gamma_trans(pi). Therefore a purported proof of LB_N(1+epsilon) is falsified in the same nonuniform SIZE model whenever N^{rho+o(1)}+Gamma_trans(pi)<N^{1+epsilon-o(1)}. If transparency first fails at a FormulaEval line, Lemma HiddenInfluence gives the finite private-row falsifier instead.

## Definitions

- source object: Psys_sym^TRS proof pi over H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)}, generator size N^{rho+o(1)}, polylog SAT instances, and base Psys_bEF^- rules already parsed by Gap98-SRhNormalForm.
- target object: the nonuniform SIZE lower-bound claim LB_N(1+epsilon), meaning Ckt(H_N^SAT)>N^{1+epsilon-o(1)} on the same length-N truth-table family and the same circuit basis used by the upper-bound simulation.
- controlled interface: TransparentRowSupport_N for every FormulaEval line, consisting of visible selector code, advice-free row or query-index enumeration or full-scan charge, same-theory SAT occurrence expansion, influence closure, and incremental duplicate-free support charging.
- target-preserving condition: the parser never replaces real SAT semantics by advice, oracle labels, or a different circuit model; every charged FormulaEval value is expanded inside the same occurrence theory before being used in the SIZE upper-bound falsifier.
- Gamma_bEF(pi) is the cost from the already validated bounded-SR_h line induction for Psys_bEF^-.
- For FormulaEval line l, K_l is its visible influence-closed support, Delta K_l is the newly charged support not charged by earlier lines, U_l is row-discovery cost, and X_l is same-theory expansion cost for Delta K_l.

## Assumptions

- Length regime: N ranges over the explicit lengths for the SAT-parity carrier, M_N=N^{q+o(1)}, formula size is polylog N, and all o(1) terms are uniform over the proof family.
- Base-model assumption: Gap98-SRhNormalForm is already valid for the chosen bounded-SR_h Psys_bEF^- rule schema, including bit fields, parent pointers, row-index encodings, eta overhead, and tau overhead.
- Uniformity/advice assumption: visible support enumerators and expansion routines are deterministic and advice-free; nonuniformity enters only in the final SIZE upper-bound circuit, not in selecting hidden hard rows.
- Same-theory assumption: FormulaEval expansion uses the same SAT formulas G_N(x,j) and occurrence labels as the lower-bound statement; no semantic FormulaEval oracle is silently introduced.
- Influence-closure assumption: changing any uncharged row, query index, or enable bit while preserving all read occurrences cannot change the value of the FormulaEval line.
- Incremental ledger assumption: once a row or query-index expansion has been paid, later lines may reference it for free only by an explicit pointer to the charged occurrence transcript.
- Non-claim boundary: the lemma is a restricted parser-to-circuit obstruction theorem, not a proof of P != NP and not a general lower-bound method.

## Equations

- gamma_trans_ledger: `\Gamma_{trans}(\pi)=\Gamma_{bEF}(\pi)+U_N+X_N,\quad U_N=\sum_{l\in FE}U_l,\quad X_N=\sum_{l\in FE}X_l`. Valid when: Valid when the base Psys_bEF^- parser has Gap98-SRhNormalForm and every FormulaEval line satisfies TransparentRowSupport_N with duplicate rows charged once.
- same_model_upper_bound: `Ckt(H_N^{SAT})\le N^{\rho+o(1)}+\Gamma_{trans}(\pi)`. Valid when: Applies when H_N^SAT uses a uniform generator of size N^{rho+o(1)} and the transcript simulates only same-theory SAT occurrence expansions.
- subthreshold_falsifier: `N^{\rho+o(1)}+\Gamma_{trans}(\pi)<N^{1+\epsilon-o(1)}\Rightarrow \pi\text{ is not a valid proof of }LB_N(1+\epsilon)`. Valid when: Requires the target lower-bound claim and the constructed upper bound to use the identical nonuniform SIZE model and length-N carrier family.
- support_density_corollary: `X_N\ge N^{1+o(1)}|K_{idx}(\pi)|,\quad \Gamma_{trans}<N^{1+\epsilon-o(1)}\Rightarrow |K_{idx}(\pi)|/M_N<N^{\epsilon-q-o(1)}`. Valid when: Valid when K_idx counts incrementally charged influential query indices and each realized index expands over all N rows with M_N=N^{q+o(1)}.

## Attempted Derivation

- Fix a proof pi and order its lines. Maintain a transcript Q_i and a ledger Gamma_i after line i.
- For Psys_bEF^- lines, invoke the already validated Gap98-SRhNormalForm line induction; these lines add exactly their Gamma_bEF contribution.
- For a transparent FormulaEval line l, run its visible support enumerator or full scan, charge U_l, compute Delta K_l against the incremental union of earlier supports, and append same-theory SAT occurrence expansions for Delta K_l, charging X_l.
- Influence closure proves semantic stability: any two occurrence completions agreeing on Q_{<l} and the charged Delta K_l give the same value to line l. Hence no uncharged row can be the first disagreement.
- Inductively all proof lines have transcript realizations, so the final asserted LB_N(1+epsilon) coexists with a circuit of size N^{rho+o(1)}+Gamma_trans(pi) for the same H_N^SAT if the ledger is subthreshold.
- If a first disagreement exists, it must be a FormulaEval line violating visibility, extensionality, or influence closure. Choose the private row or unread enable bit b*, build two completions agreeing on all read occurrences and previous lines, and obtain the HiddenInfluence falsifier.
- The support-density corollary follows because each realized query index costs N^{1+o(1)} row occurrences, so subthreshold proofs cannot contact a fraction at least N^{epsilon-q-o(1)} of the M_N query indices.

Blocking gap: The positive theorem is restricted to TransparentRowSupport_N or to semantic FormulaEval lines equipped with RealSATInfluenceRealizer_N. Full real SAT extensionality without an advice-free influence realizer remains a named semantic escape, not an unproved step hidden inside the derivation.

## Falsifiers

- falsifier: a FormulaEval line has an uncharged influential row or unread enable bit, yielding two occurrence completions that agree on the transcript but change the line value.
- falsifier: support enumeration uses nonuniform advice or a hardwired row selector, so the claimed source proof no longer transfers to a uniform same-theory parser.
- falsifier: RealSATInfluenceRealizer_N exists only as a semantic oracle with hidden influence advice, placing the proof outside the controlled interface.
- falsifier: N^{rho+o(1)}+Gamma_trans(pi)<N^{1+epsilon-o(1)} in the same SIZE model, contradicting the asserted LB_N(1+epsilon).
- falsifier: q<epsilon with full lower-bound pressure would require |K_idx|/M_N>1-o(1), so any low-cost transcript must be missing influential support.
- falsifier: changing the target circuit basis, length convention, or SAT carrier after parsing invalidates the same-model upper-bound comparison.

## Learning

Cycle 120 converts the TransparentRowSupport_N theorem pair into a minimal-bad-line induction: transparent FormulaEval lines are valid exactly when their influence is enumerated and charged, while the first hidden semantic influence is a finite private-row falsifier. The q-trichotomy is derived from X_N>=N^{1+o(1)}|K_idx|. Full semantic FormulaEval is not promoted; it is quarantined at RealSATInfluenceRealizer_N. This is paper-level parser obstruction progress only, not progress on P vs NP itself.

## Gedanken Experiment Design Seed

- Need decision: `use-now-as-falsifier-probe`
- Rationale: The theorem pair is now formal enough that a concrete beta-zero SAT-parity instance tests whether the Gamma ledger, q-trichotomy, and private-row countermodel are target-preserving rather than another abstract restatement.
- Situation seed: Take H_N^SAT(x)=xor_{j<=M_N}SAT(G_N(x,j)) with M_N=N^q and a Psys_sym proof containing one FormulaEval line whose selector either visibly enumerates K_idx or hides one enable bit e_{j*}. Compare the transparent transcript with the hidden-enable transcript for the same lower-bound assertion LB_N(1+epsilon).
- Varied variable: query exponent q in M_N=N^q, sampled below, at, and above epsilon while holding the proof grammar fixed
- Held-fixed controls: generator overhead rho and formula length polylog N, target claim LB_N(1+epsilon) in the same nonuniform SIZE model, Psys_bEF^- bounded-SR_h parser and eta/tau overhead ledger, advice-free support enumeration and same-theory SAT occurrence expansion for transparent lines
- Expected observation: For q<epsilon, transparent contact sufficient to support the lower-bound proof forces near-impossible full query-index coverage, so a low-cost proof is a falsifier. For q=epsilon, near-full contact is the boundary. For q>epsilon, partial support can survive numerically but still must be influence-complete or the hidden enable bit gives the private-row countermodel.
- Transfer certificate needed: A checked Gamma_trans line induction plus either an explicit RealSATInfluenceRealizer_N for real semantic SAT or a verified private-row/unread-enable-bit pair showing that the semantic influence was not charged.

## Next Experiment

Write the paper-ready theorem pair in two columns: left column proves Gamma_trans by minimal-bad-line induction for TransparentRowSupport_N; right column states the first-hidden-influence private-row countermodel and the RealSATInfluenceRealizer_N escape, then run the q<epsilon, q=epsilon, q>epsilon support-density corollary as a checked example.
