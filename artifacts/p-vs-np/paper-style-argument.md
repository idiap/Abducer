# Paper-Style Argument

## Route

- Selected sketch: `psk.001`
- Strategy: `strat.001` (Cross-Model Strategy around st.def.hardness-magnification-phenomenon-programme-leve)
- Bridge: `bridge.001`
- Conjecture: `conj.001`
- Strategy family: `invariant-lift-through-intermediate-object`
- Target consequence: `NP-not-in-P/poly`
- Antecedent schema: `nonuniform-circuit-exponential-lower-bound`
- Preserved invariant: `MCSP complexity profile in nonuniform-circuits`
- Carrier kind: `family of instances equipped with a monotone witness measure`
- Typing status: `typed`

## Mathematical Context

Source theorem (`st.def.hardness-magnification-phenomenon-programme-leve`):

> A hardness magnification theorem has the form:"A barely-nontrivial lower bound for an explicit problem Q in a weak model implies a major lower bound/separation in a strong model."Typically, Q is a meta-problem (e.g. a Gap-MCSP variant) and"major"means consequences such as NP not in P/poly.

Target theorem (`st.thm.oliveira-pich-santhanam-magnification-near-state`):

> In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for suitable promise gaps and input length N=2^n ) imply major consequences such as NP not in P/poly.

The selected route interprets the theorem pair as a transport from `A barely-nontrivial lower bound for an explicit problem Q in a weak model` to `major consequences such as NP not in P/poly` through the invariant `MCSP complexity profile in nonuniform-circuits`.

## Mathematical Delta

- Model shift: nonuniform-circuits
- Threshold shift: major separation consequence
- Consequence shift: upgrade `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly`
- Missing route lemma: Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.

## Candidate Bridge Object

Let $\mathcal{B}$ denote the conjectured bridge object called `MCSP witness family`. It is intended to encode the minimal mathematical structure needed to carry `A barely-nontrivial lower bound for an explicit problem Q in a weak model` from `st.def.hardness-magnification-phenomenon-programme-leve` to `major consequences such as NP not in P/poly` at `st.thm.oliveira-pich-santhanam-magnification-near-state` while preserving `MCSP complexity profile in nonuniform-circuits`.

Treat `MCSP witness family` as a `intermediate-complexity-measure` attached to the route `st.def.hardness-magnification-phenomenon-programme-leve` -> `st.thm.oliveira-pich-santhanam-magnification-near-state` and typed as a family of instances equipped with a monotone witness measure, playing the role of `An explicit family of instances equipped with a monotone witness measure that records enough of `A barely-nontrivial lower bound for an explicit problem Q in a weak model` to test whether the route can reach `NP-not-in-P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.`, carrying the source-side content `A barely-nontrivial lower bound for an explicit problem Q in a weak model` across nonuniform-circuits toward `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`. Minimal admissibility conditions: admits source-side witness data for `A barely-nontrivial lower bound for an explicit problem Q in a weak model`; preserves the route invariant `MCSP complexity profile in nonuniform-circuits`; forces the target-side payoff `NP-not-in-P/poly`.

We take the attribute set `transport set` as the minimal working specification of $\mathcal{B}$:

1. admits source-side witness data for `A barely-nontrivial lower bound for an explicit problem Q in a weak model`
2. preserves the route invariant `MCSP complexity profile in nonuniform-circuits`
3. forces the target-side payoff `NP-not-in-P/poly`

## Admissibility Conditions

Minimal admissibility conditions:

1. The source-side content `A barely-nontrivial lower bound for an explicit problem Q in a weak model` is available at `st.def.hardness-magnification-phenomenon-programme-leve`.
2. There exists an admissible realization of `MCSP witness family` as a family of instances equipped with a monotone witness measure.
3. The realization preserves `MCSP complexity profile in nonuniform-circuits` across nonuniform-circuits.

## Proposition (Conditional NP-not-in-P/poly via invariant-lift-through-intermediate-object)

If these assumptions hold and the route-specific lemma `Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.` is discharged, then `NP-not-in-P/poly` follows at `st.thm.oliveira-pich-santhanam-magnification-near-state`.

## Lemma Chain

### Lemma 1 (Source-to-object lemma)

Source-to-object lemma: the source-side content `A barely-nontrivial lower bound for an explicit problem Q in a weak model` at `st.def.hardness-magnification-phenomenon-programme-leve` yields a realization of `MCSP witness family` as a family of instances equipped with a monotone witness measure, satisfying admits source-side witness data for `A barely-nontrivial lower bound for an explicit problem Q in a weak model`; preserves the route invariant `MCSP complexity profile in nonuniform-circuits`; forces the target-side payoff `NP-not-in-P/poly`.

This lemma isolates the point at which the source theorem content `A barely-nontrivial lower bound for an explicit problem Q in a weak model` yields an explicit realization of the bridge object.

### Lemma 2 (Transport lemma)

Transport lemma: every admissible realization of `MCSP witness family` preserves `MCSP complexity profile in nonuniform-circuits` while crossing nonuniform-circuits.

This lemma is the transport step: it prevents the route from collapsing into topical similarity by forcing preservation of `MCSP complexity profile in nonuniform-circuits`.

### Lemma 3 (Payoff lemma)

Payoff lemma: if `MCSP witness family` is realized, carries `MCSP complexity profile in nonuniform-circuits`, and discharges the route-specific step from `A barely-nontrivial lower bound for an explicit problem Q in a weak model` to `major consequences such as NP not in P/poly`, then `NP-not-in-P/poly` holds at `st.thm.oliveira-pich-santhanam-magnification-near-state`.

This lemma is the payoff step: the bridge is only allowed to claim the theorem-family consequence `NP-not-in-P/poly` here.

### Lemma 4 (Route lemma 4)

Route lemma: Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.

This additional lemma localizes the theorem-pair-specific obstruction `Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.`.

## Proof

Work in the `Cross-Model Strategy around st.def.hardness-magnification-phenomenon-programme-leve` regime.
The source theorem at `st.def.hardness-magnification-phenomenon-programme-leve` supplies the route content `A barely-nontrivial lower bound for an explicit problem Q in a weak model`. By the source-to-object lemma, that content yields an admissible realization of the bridge object $\mathcal{B}$ on the route from `st.def.hardness-magnification-phenomenon-programme-leve` to `st.thm.oliveira-pich-santhanam-magnification-near-state`.
By the transport lemma, this realization preserves `MCSP complexity profile in nonuniform-circuits` in exactly the form needed to cross nonuniform-circuits.
The route-specific step `Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.` is then the only remaining nonformal insertion. Once discharged, the payoff lemma converts the realized bridge object, together with the transported invariant, into the target consequence `NP-not-in-P/poly`.
This matches the target theorem at `st.thm.oliveira-pich-santhanam-magnification-near-state`: In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for suitable promise gaps and input length N=2^n ) imply major consequences such as NP not in P/poly.
Therefore `NP-not-in-P/poly` follows conditionally on the stated bridge lemmas. $\square$

## Remaining Obligations

The present framework has not solved the problem; it has isolated the obligations that a real proof would still have to discharge:

- `obl.01`: Prove the source-to-object claim: the source-side content `A barely-nontrivial lower bound for an explicit problem Q in a weak model` available at `st.def.hardness-magnification-phenomenon-programme-leve` can be organized into `MCSP witness family` as a family of instances equipped with a monotone witness measure. (The bridge object must absorb the actual source-side mathematical content rather than merely name the antecedent.)
- `obl.02`: Prove the payoff claim: once `MCSP witness family` carries the route data from `A barely-nontrivial lower bound for an explicit problem Q in a weak model` toward `major consequences such as NP not in P/poly`, it forces `NP-not-in-P/poly` at `st.thm.oliveira-pich-santhanam-magnification-near-state`. (A bridging concept is not sufficient unless it materially contributes to the target theorem-family payoff.)
- `obl.03`: Prove the transport claim: every admissible realization of `MCSP witness family` preserves `MCSP complexity profile in nonuniform-circuits` while crossing the route nonuniform-circuits. (The bridge must keep the core mathematical quantity or structure stable across the source-target move.)
- `obl.04`: Discharge the route lemma: Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`. (The abstraction should be realizable on the current theorem pair, not only in an abstract future theory.)
- `obl.05`: Show that every admissible realization of `MCSP witness family` preserves `MCSP complexity profile in nonuniform-circuits` across nonuniform-circuits. (Without invariant preservation, the bridge concept does not carry the relevant mathematical structure.)
- `obl.06`: Prove that any admissible realization of `MCSP witness family` forces `NP-not-in-P/poly` once the route-specific lemma `Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.` is discharged. (This is the theorem-family payoff that justifies introducing the bridge concept.)
- `obl.07`: Keep the argument faithful to the `Current Bridge Agenda` regime while linking `st.def.hardness-magnification-phenomenon-programme-leve` to `st.thm.oliveira-pich-santhanam-magnification-near-state`. (Prevents the sketch from drifting into a different regime than the selected strategy anchor.)

## Failure Diagnosis

Allow `MCSP witness family` to ignore the source-side content `A barely-nontrivial lower bound for an explicit problem Q in a weak model` and only preserve topical overlap. bridge-degrades-or-fails The bridge object must absorb the actual source-side mathematical content rather than merely name the antecedent.

## Counterfactual Check

If one performs the intervention `Allow `MCSP witness family` to ignore the source-side content `A barely-nontrivial lower bound for an explicit problem Q in a weak model` and only preserve topical overlap.`, the expected effect is `bridge-degrades-or-fails`.
This is the structural necessity test for the bridge concept: if the route survives the intervention unchanged, then the proposed object was not mathematically essential.

Failure mode summary: Allow `MCSP witness family` to ignore the source-side content `A barely-nontrivial lower bound for an explicit problem Q in a weak model` and only preserve topical overlap. bridge-degrades-or-fails The bridge object must absorb the actual source-side mathematical content rather than merely name the antecedent.

## Provenance

- sketch_id: `psk.001`
- conjecture_id: `conj.001`
- strategy_id: `strat.001`
- bridge_id: `bridge.001`
- anchor_statement_id: `st.def.hardness-magnification-phenomenon-programme-leve`
- target_statement_id: `st.thm.oliveira-pich-santhanam-magnification-near-state`
