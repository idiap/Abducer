# Macro-Strategy Report for p-vs-np

## Abstract

This report should be read as a strategic mathematical note rather than as a project-management checklist. Its purpose is to explain why the current route does not yet close the main conjecture, what theorem package is still missing, and which nearby routes remain mathematically meaningful.

## Executive Answer

The proof is not blocked at the final reduction to P versus NP; it is blocked at the leading magnification bridge.
To complete the proof on the current macro-strategy, one must fix a single bridge operationalization and then prove the source-realization, invariant-transport, route, and payoff lemmas that yield `NP not in P/poly`. Once that theorem is in hand, the final implication to `P != NP` is already available in the KB.

## Strategic Bottleneck

The decisive bottleneck is the leading magnification bridge. The final reduction from the nonuniform target to the main conjecture is already available, so the strategic question is whether the bridge object can be fixed and the source-realization, transport, route, and payoff lemmas can be discharged.

## Current Reduction

- Main conjecture: `P != NP`
- Stronger route target: `NP not in P/poly`
- Grounding implication already available: If NP is not contained in P/poly, then P != NP.
- Leading bridge: `bridge.001`
- Leading route synopsis: Move from `st.def.hardness-magnification-phenomenon-programme-leve` on problem `MCSP` in model `nonuniform-circuits` using `A barely-nontrivial lower bound for an explicit problem Q in a weak model` toward `st.thm.oliveira-pich-santhanam-magnification-near-state` in model `nonuniform-circuits` to obtain `major consequences such as NP not in P/poly`.

## What Is Already Established

- Final grounding to the main conjecture is already available.
  The KB already supplies the implication `NP not in P/poly` => `P != NP` via `st.thm.nonuniform-separation-target`.
- The proof target has been reduced to a sharper nonuniform statement.
  The current macro-plan is to prove `NP not in P/poly` and then conclude `P != NP`.
- A leading theorem pair and invariant have already been isolated.
  The leading route is `bridge.001` with invariant `MCSP complexity profile in nonuniform-circuits` and target consequence `major consequences such as NP not in P/poly`.
- At least one typed bridge operationalization exists.
  The leading bridge currently has 2 operationalization(s): MCSP witness family, Gap-MCSP promise problem.

## Leading Operationalizations

### psk.001

- Object: MCSP witness family
- Score: 0.905
- Carrier kind: family of instances equipped with a monotone witness measure
- Family: invariant-lift-through-intermediate-object
- Route lemma under this operationalization: Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.

### psk.005

- Object: Gap-MCSP promise problem
- Score: 0.871
- Carrier kind: promise problem with an explicit yes/no gap and transfer reduction
- Family: surrogate-reduction-transfer
- Route lemma under this operationalization: Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.

## What Is Missing For Completion

### Choose or prove equivalence between the live bridge operationalizations.

- Why it is missing: The leading bridge currently has more than one concrete realization. A complete proof needs either one fixed carrier or a theorem proving that the two carriers are interchangeable for the route.
- What completion requires: Show that `MCSP witness family` and `Gap-MCSP promise problem` are equivalent for the route, or commit to one and restate all downstream lemmas in that representation.

### Realize the source-side lower-bound content inside the chosen bridge object.

- Why it is missing: Without this statement, the current proof plan remains conditional rather than complete.
- What completion requires: Prove the source-to-object claim: the source-side content `A barely-nontrivial lower bound for an explicit problem Q in a weak model` available at `st.def.hardness-magnification-phenomenon-programme-leve` can be organized into `MCSP witness family` as a family of instances equipped with a monotone witness measure.

### Prove that the bridge object preserves the named invariant along the route.

- Why it is missing: Without this statement, the current proof plan remains conditional rather than complete.
- What completion requires: Prove the transport claim: every admissible realization of `MCSP witness family` preserves `MCSP complexity profile in nonuniform-circuits` while crossing the route nonuniform-circuits.

### Discharge the route-specific magnification lemma.

- Why it is missing: Without this statement, the current proof plan remains conditional rather than complete.
- What completion requires: Discharge the route lemma: Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.

### Convert the realized bridge object into the target nonuniform consequence.

- Why it is missing: Without this statement, the current proof plan remains conditional rather than complete.
- What completion requires: Prove the payoff claim: once `MCSP witness family` carries the route data from `A barely-nontrivial lower bound for an explicit problem Q in a weak model` toward `major consequences such as NP not in P/poly`, it forces `NP-not-in-P/poly` at `st.thm.oliveira-pich-santhanam-magnification-near-state`.

## Completion Checklist

- [ESTABLISHED] Reduction from `NP not in P/poly` to `P != NP`.
  If NP is not contained in P/poly, then P != NP.
- [PARTIAL] Leading bridge object fixed and operationalized.
  A typed object exists, but the route still has multiple operationalizations.
- [OPEN] Source-to-object realization theorem.
  Prove the source-to-object claim: the source-side content `A barely-nontrivial lower bound for an explicit problem Q in a weak model` available at `st.def.hardness-magnification-phenomenon-programme-leve` can be organized into `MCSP witness family` as a family of instances equipped with a monotone witness measure.
- [OPEN] Invariant-preservation transport theorem.
  Prove the transport claim: every admissible realization of `MCSP witness family` preserves `MCSP complexity profile in nonuniform-circuits` while crossing the route nonuniform-circuits.
- [OPEN] Route-specific magnification lemma.
  Discharge the route lemma: Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.
- [OPEN] Payoff theorem yielding the nonuniform separation target.
  Prove the payoff claim: once `MCSP witness family` carries the route data from `A barely-nontrivial lower bound for an explicit problem Q in a weak model` toward `major consequences such as NP not in P/poly`, it forces `NP-not-in-P/poly` at `st.thm.oliveira-pich-santhanam-magnification-near-state`.

## Epistemic Gaps

- No adversarial evidence has yet been accumulated.
  The current run still records `evidence_count = 0`, so the route is structurally articulated but not externally stress-tested.
- No proof item in the queue is resolved yet.
  The current proof queue has `6` pending items and no completed proof attempts.

## Subresult Perspective

Several missing items would already count as mathematically meaningful subresults even if the main conjecture remained open, especially a clean source-to-object realization theorem, a transport theorem for the invariant, or a barrier result ruling out one of the operationalizations.


## Fallback Routes

- `bridge.002`: Move from `st.def.hardness-magnification-phenomenon-programme-leve` on problem `MCSP` in model `nonuniform-circuits` using `A barely-nontrivial lower bound for an explicit problem Q in a weak model` toward `st.thm.oliveira-santhanam-hardness-magnification-for-na` in model `formula-size` to obtain `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
  Missing route lemma: Prove that a hardness-magnification witness family preserves `MCSP complexity profile in nonuniform-circuits` while transporting the route from the nonuniform-circuits regime to the formula-size regime strongly enough to derive `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- `bridge.016`: Move from `st.def.hardness-magnification-phenomenon-programme-leve` on problem `MCSP` in model `nonuniform-circuits` using `A barely-nontrivial lower bound for an explicit problem Q in a weak model` toward `st.thm.atserias-m-uller-simple-general-magnification-fr` to obtain `There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for...`.
  Missing route lemma: Prove that a hardness-magnification witness family upgrades the route from major separation consequence to exponential lower bound without losing `exponential-lower-bound witness complexity`.

## Proof Frontier

- `proofq.p-vs-np.001` (0.779): MCSP witness family: major consequences such as NP not in P/poly
- `proofq.p-vs-np.002` (0.758): MCSP witness family: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...
- `proofq.p-vs-np.003` (0.722): MCSP witness family: There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for...

## Relevant References

- [Grounding implication] `st.thm.nonuniform-separation-target` Nonuniform separation target
  If NP is not contained in P/poly, then P != NP.
- [Leading-route source] `st.def.hardness-magnification-phenomenon-programme-leve` Leading-route source statement
  A hardness magnification theorem has the form:"A barely-nontrivial lower bound for an explicit problem Q in a weak model implies a major lower bound/separation in a strong model."Typically, Q is a meta-problem (e.g. a Gap-MCSP variant) and"major"means consequences such as NP not in P/poly.
- [Leading-route target] `st.thm.oliveira-pich-santhanam-magnification-near-state` Leading-route target statement
  In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for suitable promise gaps and input length N=2^n ) imply major consequences such as NP not in P/poly.
- [Fallback-route target] `` bridge.002
  Move from `st.def.hardness-magnification-phenomenon-programme-leve` on problem `MCSP` in model `nonuniform-circuits` using `A barely-nontrivial lower bound for an explicit problem Q in a weak model` toward `st.thm.oliveira-santhanam-hardness-magnification-for-na` in model `formula-size` to obtain `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- [Fallback-route target] `` bridge.016
  Move from `st.def.hardness-magnification-phenomenon-programme-leve` on problem `MCSP` in model `nonuniform-circuits` using `A barely-nontrivial lower bound for an explicit problem Q in a weak model` toward `st.thm.atserias-m-uller-simple-general-magnification-fr` to obtain `There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for...`.
