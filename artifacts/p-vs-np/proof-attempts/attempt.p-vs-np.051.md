# Proof Attempt: attempt.p-vs-np.051

- Queue ID: proofq.p-vs-np.105
- Status: in_progress
- Conjecture: For every admissible `MCSP witness family`, the route-side and target-side operationalizations are equivalent in the sense needed to transport `MCSP complexity profile in nonuniform-circuits` toward `There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).`.
- Bridge: disclayer.p-vs-np.family.equivalence-coherence-reframing
- Source statement: st.def.hardness-magnification-phenomenon-programme-leve
- Target statement: st.thm.oliveira-santhanam-hardness-magnification-for-na

## Prompt / Inference Diagnosis

- Context status: well-posed
- Inference status: difficult-but-well-posed
- Blocking defects: 
- Minimal repair: No packet repair is needed; the remaining uncertainty is mathematical rather than prompt-shaped.
- Certainty now: medium
- Certainty if well posed: medium
- Rationale: The packet is explicit enough for proof work, but the remaining uncertainty is mathematical rather than prompt-shaped.

## Local Grounding

- Source excerpt: A hardness magnification theorem has the form:"A barely-nontrivial lower bound for an explicit problem Q in a weak model implies a major lower bound/separation in a strong model."Typically, Q is a meta-problem (e.g. a Gap-MCSP variant) and"major"means consequences such as NP not in P/poly.
- Target excerpt: There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).

## Queue Context

- Candidate object: MCSP witness family
- Invariant: MCSP complexity profile in nonuniform-circuits
- Route synopsis: Start from `st.def.hardness-magnification-phenomenon-programme-leve` with source content `A hardness magnification theorem has the form:"A barely-nontrivial lower bound for an explicit problem Q in a weak model implies a major lower bound/separation in a strong model."Typically, Q is a meta-problem (e.g. a Gap-MCSP variant) and"major"means consequences such as NP not in P/poly.`. Reach `st.thm.oliveira-santhanam-hardness-magnification-for-na` with target content `There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).`. Use `MCSP witness family` as the local bridge object while preserving `MCSP complexity profile in nonuniform-circuits`. Branch move: `Recast the blocked frontier as an identity, equivalence, transport, or coherence problem rather than as a missing brute-force bridge.`.
- Route lemma under test: Equivalence theorem for MCSP witness family

## Expert Theorem Package

- Theorem package ID: conjpkg.disclayer-p-vs-np-family-equivalence-coherence-reframing.08
- Restricted-regime mode: equivalence-theorem
- Quantifier frame: For every admissible `MCSP witness family` attached to the route from `st.def.hardness-magnification-phenomenon-programme-leve` to `st.thm.oliveira-santhanam-hardness-magnification-for-na`, under the discovery branch `Equivalence / Coherence Reframing Prompt`.
- Bridge-object definition: `MCSP witness family` denotes the structured intermediate object required by this branch. It is meant to organize the source-side content `A hardness magnification theorem has the form:"A barely-nontrivial lower bound for an explicit problem Q in a weak model implies a major lower bound/separation in a strong model."Typically, Q is a meta-problem (e.g. a Gap-MCSP variant) and"major"means consequences such as NP not in P/poly.`. It must preserve the invariant `MCSP complexity profile in nonuniform-circuits`. Its operational role is `Recast the blocked frontier as an identity, equivalence, transport, or coherence problem rather than as a missing brute-force bridge.`.
- First nontrivial lemma: Equivalence theorem for MCSP witness family | For every admissible `MCSP witness family`, the target-side operationalization is equivalent to the route-side operationalization in the sense needed to transport `MCSP complexity profile in nonuniform-circuits` toward `There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).`.
- Negative/barrier version: Absent an explicit equivalence witness for `MCSP witness family`, transport toward `There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).` is not licensed. no_equivalence_witness
- Independent value claim: An equivalence theorem for `MCSP witness family` would independently matter because it identifies when two live operationalizations are mathematically interchangeable rather than merely analogous.

## Mathematical Packet

- Quantifier signature: For every admissible `MCSP witness family` on the route from `st.def.hardness-magnification-phenomenon-programme-leve` to `st.thm.oliveira-santhanam-hardness-magnification-for-na`.
- Symbol ledger: W: an admissible MCSP witness family | R(W): the route-side operationalization attached to MCSP witness family | T(W): the target-side operationalization relevant to the queued theorem | BW(W): an equivalence witness between the route-side and target-side operationalizations | Adm(W): W satisfies the local admissibility conditions for MCSP witness family | PresInv(W, w): MCSP complexity profile in nonuniform-circuits
- LaTeX theorem: \forall W,\ \mathrm{Adm}(W) \to \exists w : \mathsf{BW}(W),\ \mathrm{PresInv}(W,w) \wedge \mathrm{RealizesTarget}(W,w).

```lean
-- Lean-style type-theory scaffold.
-- This is a notation-oriented proof packet, not executable Lean.
-- theorem under test: Equivalence theorem for MCSP witness family
-- route synopsis: Move from `st.def.hardness-magnification-phenomenon-programme-leve` in `nonuniform-circuits` toward `st.thm.oliveira-santhanam-hardness-magnification-for-na` in `formula-size`.
-- preserved invariant: MCSP complexity profile in nonuniform-circuits
-- route: st.def.hardness-magnification-phenomenon-programme-leve -> st.thm.oliveira-santhanam-hardness-magnification-for-na
-- admissibility conditions:
--   - `MCSP witness family` is explicitly defined in the current route.
constant MCSPWitnessFamily : Type
constant Admissible : MCSPWitnessFamily -> Prop
constant RouteObj : MCSPWitnessFamily -> Type
constant TargetObj : MCSPWitnessFamily -> Type
-- BridgeWitness W should be read as an equivalence witness between the route-side and target-side operationalizations.
constant BridgeWitness : MCSPWitnessFamily -> Type
constant PresInv : (W : MCSPWitnessFamily) -> BridgeWitness W -> Prop
constant RealizesTarget : (W : MCSPWitnessFamily) -> BridgeWitness W -> Prop

theorem equivalence_theorem_for_mcsp_witness_family
    (W : MCSPWitnessFamily)
    (hW : Admissible W) :
    exists w : BridgeWitness W, PresInv W w /\ RealizesTarget W w

theorem equivalence_theorem_for_mcsp_witness_family
    (W : MCSPWitnessFamily)
    (hW : Admissible W) :
    exists w : BridgeWitness W, PresInv W w

-- barrier variant: No admissible `MCSP witness family` can simultaneously preserve `MCSP complexity profile in nonuniform-circuits` and realize `There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).` under the current route commitments.
theorem equivalence_theorem_for_mcsp_witness_family_barrier
    (W : MCSPWitnessFamily)
    (hW : Admissible W) :
    not (exists w : BridgeWitness W, PresInv W w /\ RealizesTarget W w)
```

Admissibility conditions:
- `MCSP witness family` is explicitly defined on the route from `st.def.hardness-magnification-phenomenon-programme-leve` to `st.thm.oliveira-santhanam-hardness-magnification-for-na`.
- `MCSP witness family` absorbs the source-side theorem content `A hardness magnification theorem has the form:"A barely-nontrivial lower bound for an explicit problem Q in a weak model implies a major lower bound/separation in a strong model."Typically, Q is a meta-problem (e.g. a Gap-MCSP variant) and"major"means consequences such as NP not in P/poly.`.
- `MCSP witness family` preserves `MCSP complexity profile in nonuniform-circuits` across the intended transfer.
- `MCSP witness family` is strong enough to materially address `There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).`.
- `MCSP witness family` supports the branch move `Recast the blocked frontier as an identity, equivalence, transport, or coherence problem rather than as a missing brute-force bridge.`.

- Foundation-search mode: targeted-foundation-search
- Foundation-search recommended: True
- Candidate framework regions: sparse-object and distinguisher frameworks, duality or correspondence theorems, representation-theoretic normal forms, derandomization and generator frameworks, algebraic certificate constructions

## Local InformalMathLib Hits

- `mathlib.p-vs-np.blocked.proofq-p-vs-np-102` | blocked | Equivalence theorem for MCSP witness family | C:\files\projects\abducer\abducer\InformalMathLib\p-vs-np\negative-results\mathlib.p-vs-np.blocked.proofq-p-vs-np-102-equivalence-theorem-for-mcsp-witness-family.md
- `mathlib.p-vs-np.blocked.proofq-p-vs-np-096` | blocked | Transport theorem for MCSP witness family | C:\files\projects\abducer\abducer\InformalMathLib\p-vs-np\negative-results\mathlib.p-vs-np.blocked.proofq-p-vs-np-096-transport-theorem-for-mcsp-witness-family.md
- `mathlib.p-vs-np.blocked.proofq-p-vs-np-076` | blocked | Transport theorem for MCSP witness family | C:\files\projects\abducer\abducer\InformalMathLib\p-vs-np\negative-results\mathlib.p-vs-np.blocked.proofq-p-vs-np-076-transport-theorem-for-mcsp-witness-family.md
- `mathlib.p-vs-np.blocked.proofq-p-vs-np-065` | blocked | Transport theorem for MCSP witness family | C:\files\projects\abducer\abducer\InformalMathLib\p-vs-np\negative-results\mathlib.p-vs-np.blocked.proofq-p-vs-np-065-transport-theorem-for-mcsp-witness-family.md
- `mathlib.p-vs-np.blocked.proofq-p-vs-np-053` | blocked | Transport theorem for MCSP witness family | C:\files\projects\abducer\abducer\InformalMathLib\p-vs-np\negative-results\mathlib.p-vs-np.blocked.proofq-p-vs-np-053-transport-theorem-for-mcsp-witness-family.md

## Web Search Gate

Default policy:
- Do not search the web by default. Exhaust the local KB, current artifacts, and local InformalMathLib first.
- Search only if the missing fact is decisive for a proof step, prior-art check, or exact theorem attribution.
- Search when a named theorem, barrier, paper, or threshold fact is not present locally and materially affects the result.
- Do not search for generic background, motivation, or intuitive exposition.
- If web search is used, record the concrete query, the exact source, and what proof step or novelty decision it informed.

## Knowledge Source Invocation Policy

- Stage: prove
- Target: Equivalence theorem for MCSP witness family
- Target kind: proof target

### Source Order

- `InformalMathLib` | role=local theorem, definition, barrier, and prior-result retrieval | default=query-first
  Invoke when: The current proof target may already be locally grounded for `Equivalence theorem for MCSP witness family`. A named theorem, route lemma, barrier, or prior negative result might already exist locally. Novelty or prior-art status cannot be assessed without checking local memory first.
  Do not use for: inventing a new bridge object by analogy alone claiming closure when the local hit is only topically related
  Success condition: Use InformalMathLib as sufficient local grounding only when a hit matches the exact claim, dependency, or barrier role materially enough to change the proof state.
  Current signal: current_mathlib_hits=5
- `IDE generative search` | role=local candidate generation for bridge objects, invariants, decompositions, and representation shifts | default=use-after-local-grounding
  Invoke when: Local KB and InformalMathLib ground `Equivalence theorem for MCSP witness family`, but the missing move is still conceptual rather than factual. The task is to propose a carrier, invariant, transport law, decomposition, or similar framework candidate. The output can remain conjectural until independently grounded or refuted.
  Do not use for: claiming prior art fabricating exact theorem statements or bibliographic facts promoting analogy directly into InformalMathLib without proof relevance
  Success condition: A generative suggestion is admissible only if it sharpens the theorem shape, negative route, or abstraction type; it is not evidence by itself.
- `web search` | role=external exact theorem, prior-art, or framework retrieval | default=last-resort-decisive-only
  Invoke when: A decisive exact theorem statement, prior-art fact, threshold, or barrier is still missing after local KB and InformalMathLib lookup. A local-search failure has been recorded and materially blocks the proof or novelty decision. The query can be stated concretely as a named theorem, paper, author, framework, or model-specific fact.
  Do not use for: generic background reading decorative references replacing local conceptual search with unbounded browsing
  Success condition: If an external theorem, definition, axiom, or named framework becomes proof-relevant, record the exact query and import the result into InformalMathLib.

### Consistency Rules

- Query local KB and InformalMathLib before any web search.
- Use IDE/generative search only after theorem grounding is explicit enough to state what kind of missing move is under search.
- Do not treat generative candidates as evidence; they remain conjectural until grounded, refuted, or externally validated.
- Do not claim novelty until both local memory and any required decisive prior-art gate have been checked.
- If browsing changes the proof state, record what exact statement changed and import proof-relevant external results into InformalMathLib.

### Escalation Rules

- Stay in InformalMathLib/local mode when the issue is retrieval of a known local dependency.
- Escalate to IDE/generative search when the issue is missing abstraction or representation, not missing factual attribution.
- Escalate to web search only when the issue is exact external prior art, exact theorem text, or a missing external framework foundation that local artifacts cannot settle.

## PDL Program

- Program ID: attempt.p-vs-np.051
- Kind: proof-attempt
- Stage: prove
- Target: For every admissible `MCSP witness family`, the route-side and target-side operationalizations are equivalent in the sense needed to transport `MCSP complexity profile in nonuniform-circuits` toward `There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).`.
- Nexus: Start from `st.def.hardness-magnification-phenomenon-programme-leve` with source content `A hardness magnification theorem has the form:"A barely-nontrivial lower bound for an explicit problem Q in a weak model implies a major lower bound/separation in a strong model."Typically, Q is a meta-problem (e.g. a Gap-MCSP variant) and"major"means consequences such as NP not in P/poly.`. Reach `st.thm.oliveira-santhanam-hardness-magnification-for-na` with target content `There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).`. Use `MCSP witness family` as the local bridge object while preserving `MCSP complexity profile in nonuniform-circuits`. Branch move: `Recast the blocked frontier as an identity, equivalence, transport, or coherence problem rather than as a missing brute-force bridge.`.
- Bridge object: MCSP witness family (family of instances equipped with a monotone witness measure)
- Positive route: For every admissible `MCSP witness family`, the route-side and target-side operationalizations are equivalent in the sense needed to transport `MCSP complexity profile in nonuniform-circuits` toward `There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).`.
- Negative route: Assume no equivalence witness for `MCSP witness family` aligns the route-side and target-side objects.

Anchors:
- source-theorem: st.def.hardness-magnification-phenomenon-programme-leve | A hardness magnification theorem has the form:"A barely-nontrivial lower bound for an explicit problem Q in a weak model implies a major lower bound/separation in a strong model."Typically, Q is a meta-problem (e.g. a Gap-MCSP variant) and"major"means consequences such as NP not in P/poly.
- target-theorem: st.thm.oliveira-santhanam-hardness-magnification-for-na | There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).
- mathlib-result: Equivalence theorem for MCSP witness family | The scaffolded attempt did not discharge `Equivalence theorem for MCSP witness family` for `MCSP witness family` and remains blocked by already-recorded local obstructions. Related local blockers: Transport theorem for MCSP witness family, Transport theorem for MCSP witness family, Transport theorem for MCSP witness family.
- mathlib-result: Transport theorem for MCSP witness family | The scaffolded attempt did not discharge `Transport theorem for MCSP witness family` for `MCSP witness family` and remains blocked by already-recorded local obstructions. Related local blockers: Transport theorem for MCSP witness family, Transport theorem for MCSP witness family, Transport theorem for MCSP witness family.
- mathlib-result: Transport theorem for MCSP witness family | The scaffolded attempt did not discharge `Transport theorem for MCSP witness family` for `MCSP witness family` and remains blocked by already-recorded local obstructions. Related local blockers: Transport theorem for MCSP witness family, Transport theorem for MCSP witness family, Realization theorem for MCSP witness family.
- mathlib-result: Transport theorem for MCSP witness family | The scaffolded attempt did not discharge `Transport theorem for MCSP witness family` for `MCSP witness family` and remains blocked by already-recorded local obstructions. Related local blockers: Transport theorem for MCSP witness family, Realization theorem for MCSP witness family, Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-.
- mathlib-result: Transport theorem for MCSP witness family | The scaffolded attempt did not discharge `Transport theorem for MCSP witness family` for `MCSP witness family` and remains blocked by already-recorded local obstructions. Related local blockers: Realization theorem for MCSP witness family, Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-, Obstruction theorem for MCSP witness family.

Tensions:
- Route lemma under test: Equivalence theorem for MCSP witness family
- Missing route lemma: Equivalence theorem for MCSP witness family
- The obstruction is a transport or representation failure, which is often sharper to test negatively than to keep refining constructively.

Proof debt:
- For every admissible `MCSP witness family`, the target-side operationalization is equivalent to the route-side operationalization in the sense needed to transport `MCSP complexity profile in nonuniform-circuits` toward `There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).`.
- Transport obligation: move the invariant across the proposed equivalence for `carrier-realization` without changing the target claim.
- Transport obligation: move the invariant across the proposed equivalence for `formula-size-transport` without changing the target claim.
- Equivalence claim: determine whether the live carrier for `carrier-realization` is identical to, equivalent to, or only analogous with the target-side object class.
- Equivalence theorem for MCSP witness family
- Equivalence transport lemma for MCSP witness family

Decision gates:
- Web search gate: not-evaluated -> Default stance: do not browse until a decisive local gap or prior-art uncertainty is identified.
- Negative-route heuristic: negative-first -> Apply contradiction/negation/impossibility reasoning only when the route carries a sharp structural obstruction and the negative theorem would compress the search space more than another constructive refinement.
- Final assessment: in_progress -> Continue, block, or finalize according to the current proof state.

Decision: fill this in only if a decisive local gap appears.

## External References To Import Into InformalMathLib

If you use an external theorem, definition, or axiom, record it here in the JSON as an object with:
- `reference_type`: theorem, definition, or axiom
- `title`
- `statement`
- `source_name`
- `source_url`
- `search_query`
- `used_for`
- `notes`

## Informal Proof Or Disproof Attempt

- Theorem statement: For every admissible `MCSP witness family`, the route-side and target-side operationalizations are equivalent in the sense needed to transport `MCSP complexity profile in nonuniform-circuits` toward `There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).`.
- Route lemma under test: Equivalence theorem for MCSP witness family
- Strategy family: equivalence-transport

### Informal Tactic Playbook

- `normalize-goal` | inspired by change, rewrite
  Purpose: Rewrite the target into the exact theorem statement or route-local formulation that should be proved.
  Queue-specific role: Normalize the queued claim so the goal is exactly `st.thm.oliveira-santhanam-hardness-magnification-for-na` rather than a nearby consequence.
- `introduce-assumptions` | inspired by intro, intros, fix
  Purpose: Expose quantifiers, regimes, admissibility conditions, and candidate objects as explicit assumptions.
  Queue-specific role: Expose the source premise `st.def.hardness-magnification-phenomenon-programme-leve` and admissibility of `MCSP witness family`.
- `extract-subgoal` | inspired by have, assert
  Purpose: State the next indispensable intermediate lemma explicitly instead of burying it inside prose.
  Queue-specific role: State `Equivalence theorem for MCSP witness family` as an inspectable intermediate claim.
- `reduce-to-route-lemma` | inspired by suffices, refine
  Purpose: Replace the full theorem by the narrower lemma whose discharge would activate the route.
  Queue-specific role: Reduce the whole route to the narrower obligation `Equivalence theorem for MCSP witness family`.
- `construct-witness` | inspired by obtain, use, existsi
  Purpose: Construct or sharply specify the witness family, obstruction family, reduction gadget, or certificate needed by the route.
  Queue-specific role: Construct or sharply constrain `MCSP witness family` from `st.def.hardness-magnification-phenomenon-programme-leve`.
- `activate-target-theorem` | inspired by apply, exact
  Purpose: Apply the known target theorem and list the exact hypotheses still missing locally.
  Queue-specific role: Treat `st.thm.oliveira-santhanam-hardness-magnification-for-na` as the activation target and list which hypotheses remain open locally.
- `transport-invariant` | inspired by calc, transitivity, rewrite
  Purpose: Track the preserved invariant across model shifts, representation changes, or intermediate objects.
  Queue-specific role: Track how `MCSP complexity profile in nonuniform-circuits` survives the intended route from `st.def.hardness-magnification-phenomenon-programme-leve` to `st.thm.oliveira-santhanam-hardness-magnification-for-na`.
- `case-split` | inspired by cases, rcases, by_cases
  Purpose: Split by regime, threshold, encoding, or obstruction type when one proof line hides multiple burdens.
  Queue-specific role: Split by regime, carrier encoding, or threshold only if one proof line hides multiple real burdens.
- `negate-goal` | inspired by by_contra, by_contradiction, contrapose
  Purpose: State the exact negation of the target theorem, route payoff, or carrier claim that the negative branch will test.
  Queue-specific role: State the exact negation of `st.thm.oliveira-santhanam-hardness-magnification-for-na` before running the negative branch. Heuristic: negative-first.
- `obstruction-probe` | inspired by by_contra, contrapose
  Purpose: Run the designated negative route explicitly and determine whether a barrier, counterexample, or mismatch blocks the claim.
  Queue-specific role: Probe the named negative route `Assume no equivalence witness for `MCSP witness family` aligns the route-side and target-side objects.` before claiming progress. Heuristic: negative-first.
- `derive-contradiction` | inspired by exfalso, have, contradiction
  Purpose: Push the negated branch to a forbidden collapse, barrier violation, or explicit inconsistency with accepted local results.
  Queue-specific role: Push the negative branch to a named forbidden outcome if the route is truly impossible.
- `prove-impossibility-claim` | inspired by suffices, have, exact
  Purpose: Turn a failed constructive route into a theorem-shaped non-realization, barrier, or route-impossibility result.
  Queue-specific role: If the constructive route fails, formulate the strongest theorem-shaped negative result.
- `closure-check` | inspired by done, exact, show
  Purpose: Confirm that the argument established the exact queued claim and not a nearby conditional or weakened statement.
  Queue-specific role: Check that the argument proves exactly `st.thm.oliveira-santhanam-hardness-magnification-for-na` and not a weaker surrogate.

### Informal Tactic Trace

- Step 1: `normalize-goal` | status=completed | goal=Rewrite the task as the exact target `st.thm.oliveira-santhanam-hardness-magnification-for-na`.
  Expected output: One normalized theorem statement under test, with no silent weakening or model drift.
  Note: The theorem statement is already normalized as the local claim under test.
- Step 2: `introduce-assumptions` | status=completed | goal=Make the bridge assumptions explicit: source premise `st.def.hardness-magnification-phenomenon-programme-leve` and admissibility of `MCSP witness family`.
  Expected output: A short explicit list of assumptions and regime declarations.
  Note: The dossier already exposes the local assumptions and admissibility clauses.
- Step 3: `reduce-to-route-lemma` | status=completed | goal=Show that it suffices to prove `Equivalence theorem for MCSP witness family`.
  Expected output: A theorem-shaped reduction from the full claim to the route-local lemma.
  Note: The route lemma `Equivalence theorem for MCSP witness family` is already the explicit prove-time subgoal.
- Step 4: `extract-subgoal` | status=completed | goal=State `Equivalence theorem for MCSP witness family` as the next explicit subgoal.
  Expected output: A named subgoal with dependencies and failure mode.
  Note: The subgoal `Equivalence theorem for MCSP witness family` is already named in the current dossier.
- Step 5: `construct-witness` | status=in_progress | goal=Construct or constrain `MCSP witness family` from `st.def.hardness-magnification-phenomenon-programme-leve`.
  Expected output: An explicit witness, carrier, or clear statement that this construction is blocked.
  Note: Construct a concrete witness `BW(W)` for `MCSP witness family` under `For every admissible `MCSP witness family` on the route from `st.def.hardness-magnification-phenomenon-programme-leve` to `st.thm.oliveira-santhanam-hardness-magnification-for-na`.`.
- Step 6: `transport-invariant` | status=in_progress | goal=Preserve `MCSP complexity profile in nonuniform-circuits` along the route toward `st.thm.oliveira-santhanam-hardness-magnification-for-na`.
  Expected output: A short chain of invariant-preservation steps or a precise transport obstruction.
  Note: Prove that `BW(W)` preserves `MCSP complexity profile in nonuniform-circuits` while mediating from `R(W)` to `T(W)`.
- Step 7: `activate-target-theorem` | status=completed | goal=Activate the target-side theorem package for `st.thm.oliveira-santhanam-hardness-magnification-for-na`.
  Expected output: A list of exact target hypotheses and which ones are already discharged.
  Note: Target activation is reduced to discharging `Equivalence theorem for MCSP witness family` against `st.thm.oliveira-santhanam-hardness-magnification-for-na`.
- Step 8: `negate-goal` | status=completed | goal=State the exact negation of the route toward `st.thm.oliveira-santhanam-hardness-magnification-for-na`.
  Expected output: One explicit negated claim or branch assumption, with no ambiguity about what is being denied.
  Note: The negated branch has been made explicit from the queue packet.
- Step 9: `obstruction-probe` | status=completed | goal=Run the negative route `Assume no equivalence witness for `MCSP witness family` aligns the route-side and target-side objects.` against the argument.
  Expected output: A clear statement that the route survives, or a precise barrier/counterexample diagnosis.
  Note: Local obstruction analogues already exist in InformalMathLib: Equivalence theorem for MCSP witness family, Transport theorem for MCSP witness family, Transport theorem for MCSP witness family.
- Step 10: `derive-contradiction` | status=in_progress | goal=Drive the negated branch to a named forbidden outcome.
  Expected output: A contradiction, forbidden collapse, or barrier violation that discharges the negative branch.
  Note: Any contradiction route must separate the current packet from nearby blockers: Equivalence theorem for MCSP witness family, Transport theorem for MCSP witness family, Transport theorem for MCSP witness family.
- Step 11: `prove-impossibility-claim` | status=pending | goal=State the theorem-shaped impossibility claim implied by the failed constructive route.
  Expected output: A precise negative theorem candidate or route-impossibility formulation.
- Step 12: `closure-check` | status=pending | goal=Verify that the argument closes exactly the queued target `st.thm.oliveira-santhanam-hardness-magnification-for-na`.
  Expected output: A final verdict of proved, disproved, blocked, deferred, or prior_art_found with no claim drift.

### Negative-Route Heuristic

- Decision: negative-first
- Recommended: True
- Use negation: True
- Use contradiction: True
- Use impossibility claim: True
- Score: 7
- Epistemic principle: A negative route is preferred when it targets a structural obstruction sharply enough to compress the search space more than another constructive refinement.
- Decision rule: Apply contradiction/negation/impossibility reasoning only when the route carries a sharp structural obstruction and the negative theorem would compress the search space more than another constructive refinement.
- Rationale: The obstruction is a transport or representation failure, which is often sharper to test negatively than to keep refining constructively.

Triggers:
- The obstruction is a transport or representation failure, which is often sharper to test negatively than to keep refining constructively.
- The current bridge object still risks being only a role-description, so a non-realization theorem would be valuable.

### Contradiction / Impossibility Frame

- Negative mode: 
- Negated claim: Assume no equivalence witness for `MCSP witness family` aligns the route-side and target-side objects.
- Contradiction target: st.thm.oliveira-santhanam-hardness-magnification-for-na
- Forbidden outcome: The route fails if no equivalence witness for `MCSP witness family` transports `MCSP complexity profile in nonuniform-circuits` to the target-side operationalization.
- Impossibility claim template: 

Stepwise argument:

Positive subgoal package:

- Source: mathematical_layers+branch_execution
- Route lemma: Equivalence theorem for MCSP witness family
- Constructive goal: For every admissible `MCSP witness family`, the route-side and target-side operationalizations are equivalent in the sense needed to transport `MCSP complexity profile in nonuniform-circuits` toward `There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).`.
- Quantifier signature: For every admissible `MCSP witness family` on the route from `st.def.hardness-magnification-phenomenon-programme-leve` to `st.thm.oliveira-santhanam-hardness-magnification-for-na`.
- LaTeX theorem: \forall W,\ \mathrm{Adm}(W) \to \exists w : \mathsf{BW}(W),\ \mathrm{PresInv}(W,w) \wedge \mathrm{RealizesTarget}(W,w).
- Lean theorem name: equivalence_theorem_for_mcsp_witness_family
- Witness symbol: BW(W)
- Search shapes: realization, transport, equivalence, obstruction
- Positive shapes: realization, transport, equivalence
- Candidate titles: Equivalence theorem for MCSP witness family
- Candidate obligations:
  - For every admissible `MCSP witness family`, the target-side operationalization is equivalent to the route-side operationalization in the sense needed to transport `MCSP complexity profile in nonuniform-circuits` toward `There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).`.
  - Transport obligation: move the invariant across the proposed equivalence for `carrier-realization` without changing the target claim.
  - Transport obligation: move the invariant across the proposed equivalence for `formula-size-transport` without changing the target claim.
  - Equivalence claim: determine whether the live carrier for `carrier-realization` is identical to, equivalent to, or only analogous with the target-side object class.
  - Equivalence theorem for MCSP witness family
  - Equivalence transport lemma for MCSP witness family
  - Define the route-side and target-side operationalizations as explicit types.
  - Construct the equivalence witness for `MCSP witness family`.
  - Prove transport of `MCSP complexity profile in nonuniform-circuits` across the equivalence.
  - Prove the required coherence or naturality law.
  - Prove transport of `exponential-lower-bound witness complexity` across the equivalence.
- Next constructive steps:
  - Construct a concrete witness `BW(W)` for `MCSP witness family` under `For every admissible `MCSP witness family` on the route from `st.def.hardness-magnification-phenomenon-programme-leve` to `st.thm.oliveira-santhanam-hardness-magnification-for-na`.`.
  - Prove that `BW(W)` preserves `MCSP complexity profile in nonuniform-circuits` while mediating from `R(W)` to `T(W)`.
  - Expose the exact target-activation clause proving `BW(W)` is strong enough to realize `st.thm.oliveira-santhanam-hardness-magnification-for-na`.
  - Realize the positive bridge shape `realization` before revisiting any obstruction conclusion.
  - For every admissible `MCSP witness family`, the target-side operationalization is equivalent to the route-side operationalization in the sense needed to transport `MCSP complexity profile in nonuniform-circuits` toward `There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).`.
  - Transport obligation: move the invariant across the proposed equivalence for `carrier-realization` without changing the target claim.

- Step 1: `MCSP witness family` denotes the structured intermediate object required by this branch. It is meant to organize the source-side content `A hardness magnification theorem has the form:"A barely-nontrivial lower bound for an explicit problem Q in a weak model implies a major lower bound/separation in a strong model."Typically, Q is a meta-problem (e.g. a Gap-MCSP variant) and"major"means consequences such as NP not in P/poly.`. It must preserve the invariant `MCSP complexity profile in nonuniform-circuits`. Its operational role is `Recast the blocked frontier as an identity, equivalence, transport, or coherence problem rather than as a missing brute-force bridge.`.
  Justification: `MCSP witness family` is explicitly defined on the route from `st.def.hardness-magnification-phenomenon-programme-leve` to `st.thm.oliveira-santhanam-hardness-magnification-for-na`.
  Depends on: st.def.hardness-magnification-phenomenon-programme-leve
- Step 2: For every admissible `MCSP witness family`, the target-side operationalization is equivalent to the route-side operationalization in the sense needed to transport `MCSP complexity profile in nonuniform-circuits` toward `There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).`.
  Justification: Equivalence theorem for MCSP witness family
  Depends on: st.def.hardness-magnification-phenomenon-programme-leve, Equivalence theorem for MCSP witness family, Equivalence theorem for MCSP witness family
- Step 3: For every admissible `MCSP witness family`, the route-side and target-side operationalizations are equivalent in the sense needed to transport `MCSP complexity profile in nonuniform-circuits` toward `There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).`.
  Justification: Close the queued conjecture by matching the target theorem excerpt to the hypotheses discharged in the previous steps.
  Depends on: Equivalence theorem for MCSP witness family, st.thm.oliveira-santhanam-hardness-magnification-for-na
- Step 4: Reduce target activation to the explicit route lemma `Equivalence theorem for MCSP witness family` for `MCSP witness family`.
  Justification: Under strategy `equivalence-transport`, the target theorem `st.thm.oliveira-santhanam-hardness-magnification-for-na` activates only after the route-local realization burden is discharged.
  Depends on: Equivalence theorem for MCSP witness family, st.thm.oliveira-santhanam-hardness-magnification-for-na
- Step 5: Construct a concrete witness `BW(W)` for `MCSP witness family` under `For every admissible `MCSP witness family` on the route from `st.def.hardness-magnification-phenomenon-programme-leve` to `st.thm.oliveira-santhanam-hardness-magnification-for-na`.`.
  Justification: The constructive packet exposes `BW(W)` with shapes realization, transport, equivalence and route lemma `Equivalence theorem for MCSP witness family`.
  Depends on: Equivalence theorem for MCSP witness family, equivalence_theorem_for_mcsp_witness_family
- Step 6: For every admissible `MCSP witness family`, the target-side operationalization is equivalent to the route-side operationalization in the sense needed to transport `MCSP complexity profile in nonuniform-circuits` toward `There exist explicit"meta"problems (including MCSP variants) such that proving certain emph barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).`.
  Justification: Lean/math packet evidence now isolates this as an explicit constructive obligation for `MCSP witness family`.
  Depends on: Equivalence theorem for MCSP witness family
- Step 7: Record the nearest local blockers for `Equivalence theorem for MCSP witness family` instead of restarting the same realization pattern.
  Justification: InformalMathLib already records nearby blocked routes: Equivalence theorem for MCSP witness family, Transport theorem for MCSP witness family, Transport theorem for MCSP witness family.
  Depends on: mathlib.p-vs-np.blocked.proofq-p-vs-np-102, mathlib.p-vs-np.blocked.proofq-p-vs-np-096, mathlib.p-vs-np.blocked.proofq-p-vs-np-076
- Step 8: Construct a concrete witness `BW(W)` for `MCSP witness family` under `For every admissible `MCSP witness family` on the route from `st.def.hardness-magnification-phenomenon-programme-leve` to `st.thm.oliveira-santhanam-hardness-magnification-for-na`.`.
  Justification: Branch execution `discexec.p-vs-np.025` keeps `realization` live for `MCSP witness family` rather than collapsing immediately into the obstruction route.
  Depends on: Equivalence theorem for MCSP witness family, equivalence_theorem_for_mcsp_witness_family, mathlib.p-vs-np.blocked.proofq-p-vs-np-102, mathlib.p-vs-np.blocked.proofq-p-vs-np-096, mathlib.p-vs-np.blocked.proofq-p-vs-np-076
- Step 9: Transport obligation: move the invariant across the proposed equivalence for `carrier-realization` without changing the target claim.
  Justification: Lean/branch evidence isolates `transport` as a live positive shape for `MCSP witness family`, so the next local burden is to make the map from `R(W)` to `T(W)` explicit.
  Depends on: Equivalence theorem for MCSP witness family, equivalence_theorem_for_mcsp_witness_family
- Step 10: Construct the equivalence witness for `MCSP witness family`.
  Justification: Lean/branch evidence keeps `equivalence` live for `MCSP witness family`, so the next local burden is to make the witness and its coherence or naturality law explicit.
  Depends on: Equivalence theorem for MCSP witness family, equivalence_theorem_for_mcsp_witness_family
- Step 11: Keep the constructive branch on shapes `realization, transport, equivalence` before promoting the impossibility route.
  Justification: Readiness mode `symbolic-search-ready` with score `11` still supports bounded constructive pressure on `MCSP witness family`.
  Depends on: Equivalence theorem for MCSP witness family, discexec.p-vs-np.025

Local results used:

- Equivalence theorem for MCSP witness family [blocked]
  Role: Local blocker relevant to the current route lemma `Equivalence theorem for MCSP witness family`.
- Transport theorem for MCSP witness family [blocked]
  Role: Local blocker relevant to the current route lemma `Equivalence theorem for MCSP witness family`.
- Transport theorem for MCSP witness family [blocked]
  Role: Local blocker relevant to the current route lemma `Equivalence theorem for MCSP witness family`.

Continuation log:

- Stage 1: Grounded the active proof state against local blockers, target activation, and a constructive subgoal packet.
  Detail: Reduce target activation to the explicit route lemma `Equivalence theorem for MCSP witness family` for `MCSP witness family`.
  Detail: Under strategy `equivalence-transport`, the target theorem `st.thm.oliveira-santhanam-hardness-magnification-for-na` activates only after the route-local realization burden is discharged.
  Detail: Constructive packet shapes: realization, transport, equivalence.
  Detail: Primary constructive witness symbol: `BW(W)`.
  Detail: Imported 3 local InformalMathLib blockers into the dossier.
- Stage 2: Pressed the constructive branch through shape-specific obligations before escalating to obstruction.
  Detail: Positive shapes kept live: realization, transport, equivalence.
  Detail: Readiness mode `symbolic-search-ready` with score `11` comes from branch execution `discexec.p-vs-np.025`.
  Detail: Construct a concrete witness `BW(W)` for `MCSP witness family` under `For every admissible `MCSP witness family` on the route from `st.def.hardness-magnification-phenomenon-programme-leve` to `st.thm.oliveira-santhanam-hardness-magnification-for-na`.`.
  Detail: Branch execution `discexec.p-vs-np.025` keeps `realization` live for `MCSP witness family` rather than collapsing immediately into the obstruction route.
  Detail: Transport obligation: move the invariant across the proposed equivalence for `carrier-realization` without changing the target claim.
  Detail: Lean/branch evidence isolates `transport` as a live positive shape for `MCSP witness family`, so the next local burden is to make the map from `R(W)` to `T(W)` explicit.
  Detail: Construct the equivalence witness for `MCSP witness family`.
  Detail: Lean/branch evidence keeps `equivalence` live for `MCSP witness family`, so the next local burden is to make the witness and its coherence or naturality law explicit.
  Detail: Keep the constructive branch on shapes `realization, transport, equivalence` before promoting the impossibility route.

Negative-route analysis:

- Obstruction candidate: Assume no equivalence witness for `MCSP witness family` aligns the route-side and target-side objects.
- Negated claim: Assume no equivalence witness for `MCSP witness family` aligns the route-side and target-side objects.
- Contradiction target: st.thm.oliveira-santhanam-hardness-magnification-for-na
- Forbidden outcome: The route fails if no equivalence witness for `MCSP witness family` transports `MCSP complexity profile in nonuniform-circuits` to the target-side operationalization.
- Counterexample or barrier: InformalMathLib already records nearby blocked routes: Equivalence theorem for MCSP witness family, Transport theorem for MCSP witness family, Transport theorem for MCSP witness family.
- Impossibility claim: 
- Effect on claim: The route fails if no equivalence witness for `MCSP witness family` transports `MCSP complexity profile in nonuniform-circuits` to the target-side operationalization.

## Critique Judges

### Statement Grounding Judge

- Is the claim under test stated explicitly and does it match the queue item?
- Are source and target statements grounded in local KB statement ids or InformalMathLib entries?
- Does each proof step say what prior local statement or earlier step it depends on?

Verdict: passes
Notes:
- The resumed attempt now grounds the live goal against the named route lemma and target theorem.

### Tactic Goal-Control Judge

- Does `normalize-goal` rewrite the task into the exact theorem or route-local statement under test?
- If `reduce-to-route-lemma` is used, does it preserve sufficiency instead of quietly weakening the original claim?
- Does `closure-check` return to the original queued claim and verify that no goal drift occurred?

Verdict: passes
Notes:
- The prove loop keeps the focus on `Equivalence theorem for MCSP witness family`.

### Inferential Validity Judge

- Does each step follow informally from its stated dependencies?
- Are quantifiers, regimes, and model shifts preserved rather than silently changed?
- Is the conclusion exactly the claimed result rather than a nearby weaker statement?

Verdict: in_progress
Notes:
- The constructive continuation now separates realization, transport, equivalence obligations for `MCSP witness family` instead of collapsing them into a single obstruction summary.

### Assumption Discipline Judge

- Did the proof introduce any hidden assumptions not already declared?
- Are all uses of prior lemmas, barriers, and transfer claims explicit?
- If an extra assumption is necessary, is the outcome downgraded to a conditional result?

Verdict: pending

### Citation Fidelity Judge

- Does every cited theorem, definition, or axiom match the statement actually used in the proof step?
- If web-sourced material appears, is the exact source recorded together with the role it played?
- Does the argument avoid paraphrases that silently alter the mathematical content of a cited result?

Verdict: pending

### Proof Granularity Judge

- Is each proof step small enough for an expert to inspect without guessing hidden intermediate claims?
- Are route lemmas, reductions, and quantifier shifts made explicit rather than buried inside phrases like `it follows`?
- When the proof cannot discharge a burden, is the gap named precisely instead of being glossed over?

Verdict: pending

### Tactic Trace-Discipline Judge

- Is the informal tactic trace updated from template state into a real trace with statuses and notes?
- For each recommended tactic, is there either an execution record, an explicit skip rationale, or a blocked/deferred diagnosis?
- Do tactic-trace statuses agree with the written stepwise argument and the final verdict?

Verdict: passes
Notes:
- The tactic trace was updated from template state into explicit completed and in-progress checkpoints.

### Tactic Subgoal-Exposure Judge

- Do `extract-subgoal` and `activate-target-theorem` expose the exact intermediate claims and missing hypotheses instead of hiding them in prose?
- When `construct-witness` or `transport-invariant` is used, is the witness, carrier, transport law, or obstruction stated explicitly?
- If a tactic fails, is that failure turned into a named blocker or negative result rather than omitted from the dossier?

Verdict: passes
Notes:
- The constructive packet now exposes `BW(W)` and 11 explicit constructive obligation(s).
- Shape-specific constructive obligations are now explicit: realization, transport, equivalence.

### Prior-Art And Novelty Judge

- Can the result already be recovered from local InformalMathLib or KB material?
- If not locally, is a web search required by the search policy before claiming novelty?
- If prior art exists, should the outcome be reclassified as reconstruction or prior_art_found?

Verdict: pending

### Local Counterexample-Search Judge

- Was a local search for counterexamples, model mismatches, or barrier analogs actually attempted before escalation?
- Does the dossier say what was checked locally and what failed to falsify the claim?
- If a nearby failure pattern exists, does the argument explain why it does or does not apply to the current route?

Verdict: in_progress
Notes:
- Nearby blocked local results were imported: Equivalence theorem for MCSP witness family, Transport theorem for MCSP witness family, Transport theorem for MCSP witness family.

### Obstruction And Negative-Route Judge

- Does the current argument survive the designated negative route or obstruction check?
- Is there a counterexample, barrier, or failure mode that blocks the route?
- If the route fails, is the negative result itself clearly formulated?

Verdict: in_progress
Notes:
- The route fails if no equivalence witness for `MCSP witness family` transports `MCSP complexity profile in nonuniform-circuits` to the target-side operationalization.
- Constructive shapes remain live on `MCSP witness family`: realization, transport, equivalence.

### Contradiction And Impossibility Discipline Judge

- If the argument uses negation, is the exact negated claim stated explicitly rather than implied informally?
- If the route uses contradiction, is the forbidden collapse, barrier, or inconsistency named precisely?
- If the constructive route fails, does the dossier formulate a theorem-shaped impossibility or non-realization claim rather than only saying `blocked`?

Verdict: pending
Notes:
- The impossibility branch is intentionally deferred until the shape-specific constructive obligations have been pressed further.

### Closure Judge

- Is the final outcome correctly classified as proved, disproved, blocked, deferred, or prior_art_found?
- Does the written proof or disproof support that classification?
- Is the result statement ready to persist into InformalMathLib if the outcome is terminal?

Verdict: pending

## Final Assessment

- Outcome: in_progress
- Verdict: 
- Novelty assessment: 
- Confidence: 
- Result statement: 
- Result summary: 

## Major Subresult Assessment

Use this only for terminal `proved` or `disproved` outcomes that might warrant a standalone paper in `artifacts/<kb-ref>/produced_papers`.

Mandatory gates:
- Self-contained statement: False
- Mathematical inspectability: False
- Nontrivial frontier relation: False
- Independent value: False

0-3 axis scores:
- Frontier shift: 0
- Independence: 0
- Transferability: 0
- Barrier clarity: 0
- Proof closure: 0
- Search compression: 0

Threshold rule: all mandatory gates pass, total score >= 11, and at least one of frontier shift / independence / barrier clarity is 3.

- Paper candidate title: 
- Paper candidate summary: 
- Overall judgment:
