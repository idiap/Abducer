# Macro-Proof State Report for p-vs-np

## Abstract

The current macro-proof does not try to prove P != NP directly. It organizes the search around a stronger nonuniform separation claim, then grounds the main conjecture by the implication NP not in P/poly implies P != NP.
The present state is a conditional macro-proof: the main conjecture is grounded, the leading route is explicit, and the remaining gap is localized in a small set of route-specific obligations.

## Introduction

This document should be read as a mathematical programme note. Its purpose is to explain how the current search state grounds the main conjecture in a sharper nonuniform target and to isolate the minimal theorem package still missing.

## Reduction Strategy

The reduction strategy is deliberately high-level: prove a hardness-magnification route to `NP not in P/poly`, then close the main conjecture through the already available nonuniform implication. The mathematical substance therefore sits in the magnification bridge, not in the final reduction step.

## Main Conjecture

- Core claim: `P != NP`
- Stronger route target: `NP not in P/poly`
- Grounding statement: `st.thm.nonuniform-separation-target`
- Grounding implication: If NP is not contained in P/poly, then P != NP.

## Grounding in the Local KB

### Definition of P

- Statement id: `st.def.item`
- Excerpt: P is the class of languages decidable by deterministic polynomial-time Turing machines.

### Definition of NP

- Statement id: `st.def.item-2`
- Excerpt: NP is the class of languages whose yes instances admit polynomial-size certificates verifiable in polynomial time.

### Definition of NP-completeness

- Statement id: `st.def.np-completeness`
- Excerpt: A language is NP-complete if it lies in NP and every language in NP polynomial-time many-one reduces to it.

### Cook-Levin

- Statement id: `st.thm.cook-levin-sat-is-np-complete-cook1971`
- Excerpt: SAT is NP-complete.

### Definition of P/poly

- Statement id: `st.def.item-5`
- Excerpt: P/poly is the class of languages decided by polynomial-size Boolean circuit families, equivalently polynomial-time computation with polynomial-length advice.

### Nonuniform separation target

- Statement id: `st.thm.nonuniform-separation-target`
- Excerpt: If NP is not contained in P/poly, then P != NP.

## Conditional Macro-Proof

- Proposition: If these assumptions hold and the route-specific lemma `Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.` is discharged, then `NP not in P/poly` follows at `st.thm.oliveira-pich-santhanam-magnification-near-state`.
- Implication chain:
  - Start from the hardness-magnification program: a barely nontrivial lower bound for an explicit MCSP-type problem in a weak model may amplify into a major separation consequence.
  - If these assumptions hold and the route-specific lemma `Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.` is discharged, then `NP not in P/poly` follows at `st.thm.oliveira-pich-santhanam-magnification-near-state`.
  - Invoke the grounding implication from the KB: if NP not in P/poly, then P != NP.
- Status note: This is a conditional macro-proof program. The central unresolved step is the route-specific bridge lemma, not the final grounding implication to P != NP.

## Leading Route

The leading route centers on `bridge.001` and treats `MCSP witness family` as the bridge object intended to carry the source lower-bound regime into the target separation regime. The route is therefore being presented as a conditional theorem programme rather than as a proof. A remaining abstraction defect is the mismatch between the witness-family presentation and the Gap-MCSP operationalization.

- Bridge: `bridge.001`
- Priority: 0.744
- Route synopsis: Move from `st.def.hardness-magnification-phenomenon-programme-leve` on problem `MCSP` in model `nonuniform-circuits` using `A barely-nontrivial lower bound for an explicit problem Q in a weak model` toward `st.thm.oliveira-pich-santhanam-magnification-near-state` in model `nonuniform-circuits` to obtain `major consequences such as NP not in P/poly`.
- Source theorem `st.def.hardness-magnification-phenomenon-programme-leve`: A hardness magnification theorem has the form:"A barely-nontrivial lower bound for an explicit problem Q in a weak model implies a major lower bound/separation in a strong model."Typically, Q is a meta-problem (e.g. a Gap-MCSP variant) and"major"means consequences such as NP not in P/poly.
- Target theorem `st.thm.oliveira-pich-santhanam-magnification-near-state`: In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for suitable promise gaps and input length N=2^n ) imply major consequences such as NP not in P/poly.
- Mathematical delta: A barely-nontrivial lower bound for an explicit problem Q in a weak model -> major consequences such as NP not in P/poly
- Model shift: nonuniform-circuits
- Threshold shift: major separation consequence
- Consequence shift: upgrade `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly`
- Candidate object: MCSP witness family
- Carrier kind: family of instances equipped with a monotone witness measure
- Preserved invariant: MCSP complexity profile in nonuniform-circuits
- Proof family: invariant-lift-through-intermediate-object
- Family rationale: Introduce a conjectured intermediate object or invariant, prove that the source regime induces it, then force the target consequence through that invariant.
- Conditional proposition: If these assumptions hold and the route-specific lemma `Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.` is discharged, then `NP not in P/poly` follows at `st.thm.oliveira-pich-santhanam-magnification-near-state`.
- Cross-stage consistency note: The bridge portfolio names the carrier as `MCSP witness family`, while the selected proof sketch currently operationalizes the route through `Gap-MCSP promise problem`. This is an unresolved representation shift inside the current macro-proof state, not a proved equivalence.

### Leading Route Assumptions

- The source-side content `A barely-nontrivial lower bound for an explicit problem Q in a weak model` is available at `st.def.hardness-magnification-phenomenon-programme-leve`.
- There exists an admissible realization of `MCSP witness family` as a family of instances equipped with a monotone witness measure.
- The realization preserves `MCSP complexity profile in nonuniform-circuits` across nonuniform-circuits.

### Leading Route Obligations

- Prove the source-to-object claim: the source-side content `A barely-nontrivial lower bound for an explicit problem Q in a weak model` available at `st.def.hardness-magnification-phenomenon-programme-leve` can be organized into `Gap-MCSP promise problem` as a promise problem with an explicit yes/no gap and transfer reduction.
- Prove the payoff claim: once `Gap-MCSP promise problem` carries the route data from `A barely-nontrivial lower bound for an explicit problem Q in a weak model` toward `major consequences such as NP not in P/poly`, it forces `NP not in P/poly` at `st.thm.oliveira-pich-santhanam-magnification-near-state`.
- Prove the transport claim: every admissible realization of `Gap-MCSP promise problem` preserves `MCSP complexity profile in nonuniform-circuits` while crossing the route nonuniform-circuits.
- Make the threshold control explicit: `Gap-MCSP promise problem` must realize the shift major separation consequence in a mathematically checkable way.

### Lemma Chain

- Source-to-object lemma: the source-side content `A barely-nontrivial lower bound for an explicit problem Q in a weak model` at `st.def.hardness-magnification-phenomenon-programme-leve` yields a realization of `Gap-MCSP promise problem` as a promise problem with an explicit yes/no gap and transfer reduction, satisfying admits source-side witness data for `A barely-nontrivial lower bound for an explicit problem Q in a weak model`; preserves the route invariant `MCSP complexity profile in nonuniform-circuits`; forces the target-side payoff `NP not in P/poly`.
- Transport lemma: every admissible realization of `Gap-MCSP promise problem` preserves `MCSP complexity profile in nonuniform-circuits` while crossing nonuniform-circuits.
- Payoff lemma: if `Gap-MCSP promise problem` is realized, carries `MCSP complexity profile in nonuniform-circuits`, and discharges the route-specific step from `A barely-nontrivial lower bound for an explicit problem Q in a weak model` to `major consequences such as NP not in P/poly`, then `NP not in P/poly` holds at `st.thm.oliveira-pich-santhanam-magnification-near-state`.
- Reduction lemma: the source-side content `A barely-nontrivial lower bound for an explicit problem Q in a weak model` reduces to the surrogate object encoded by `Gap-MCSP promise problem` without weakening the path to `NP not in P/poly`.

### Proof Outline

- Define `Gap-MCSP promise problem` as a promise problem with an explicit yes/no gap and transfer reduction with the necessary attributes extracted in `conj.003`.
- Show that the source-side content `A barely-nontrivial lower bound for an explicit problem Q in a weak model` induces `MCSP complexity profile in nonuniform-circuits` inside `Gap-MCSP promise problem`.
- Construct the surrogate reduction into `Gap-MCSP promise problem` and verify that it preserves the needed route from `A barely-nontrivial lower bound for an explicit problem Q in a weak model` to `major consequences such as NP not in P/poly`.
- Use the realized bridge object to force `NP not in P/poly`.

### Failure Analysis

- Missing route lemma: Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.
- Negative route: Allow `MCSP witness family` to ignore the source-side content `A barely-nontrivial lower bound for an explicit problem Q in a weak model` and only preserve topical overlap. bridge-degrades-or-fails The bridge object must absorb the actual source-side mathematical content rather than merely name the antecedent.
- Failure diagnosis: Failure mode: `MCSP witness family` never becomes more than topical overlap because the route-specific lemma remains missing. Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.

## Supporting Routes

### bridge.002

- Priority: 0.732
- Route synopsis: Move from `st.def.hardness-magnification-phenomenon-programme-leve` on problem `MCSP` in model `nonuniform-circuits` using `A barely-nontrivial lower bound for an explicit problem Q in a weak model` toward `st.thm.oliveira-santhanam-hardness-magnification-for-na` in model `formula-size` to obtain `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- Candidate object: MCSP witness family
- Carrier kind: family of instances equipped with a monotone witness measure
- Target focus: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...
- Missing route lemma: Prove that a hardness-magnification witness family preserves `MCSP complexity profile in nonuniform-circuits` while transporting the route from the nonuniform-circuits regime to the formula-size regime strongly enough to derive `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.

### bridge.016

- Priority: 0.711
- Route synopsis: Move from `st.def.hardness-magnification-phenomenon-programme-leve` on problem `MCSP` in model `nonuniform-circuits` using `A barely-nontrivial lower bound for an explicit problem Q in a weak model` toward `st.thm.atserias-m-uller-simple-general-magnification-fr` to obtain `There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for...`.
- Candidate object: MCSP witness family
- Carrier kind: family of instances equipped with a monotone witness measure
- Target focus: There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for...
- Missing route lemma: Prove that a hardness-magnification witness family upgrades the route from major separation consequence to exponential lower bound without losing `exponential-lower-bound witness complexity`.

## Proof Frontier

The current frontier should be interpreted as a small family of theorem-sized obligations, not as an execution backlog. Each queued item isolates one mathematically inspectable route conjecture whose proof or failure would materially change the state of the macro-proof.

### proofq.p-vs-np.001

- Title: MCSP witness family: major consequences such as NP not in P/poly
- Priority: 0.779
- Candidate object: MCSP witness family
- Conjecture: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- Missing route lemma: Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.

### proofq.p-vs-np.002

- Title: MCSP witness family: major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...
- Priority: 0.758
- Candidate object: MCSP witness family
- Conjecture: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits across the transfer nonuniform-circuits -> formula-size and yields major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter... for MCSP in formula-size.
- Missing route lemma: Prove that a hardness-magnification witness family preserves `MCSP complexity profile in nonuniform-circuits` while transporting the route from the nonuniform-circuits regime to the formula-size regime strongly enough to derive `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.

### proofq.p-vs-np.003

- Title: MCSP witness family: There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for...
- Priority: 0.722
- Candidate object: MCSP witness family
- Conjecture: There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant exponential-lower-bound witness complexity and yields There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for....
- Missing route lemma: Prove that a hardness-magnification witness family upgrades the route from major separation consequence to exponential lower bound without losing `exponential-lower-bound witness complexity`.

## Status Assessment

- Supported hypotheses: 22
- Inconclusive hypotheses: 22
- External evidence items: 0
- Pending proof-queue items: 6
- Assessment: The macro-proof has a coherent leading route and a grounded implication to the main conjecture, but it remains conditional. The unresolved mass sits in the bridge object, the route lemma, and the absence of external evidence or discharged proof obligations.
- Novelty argument: The novelty is not a claimed proof of P versus NP. It is a theorem-pair-specific research program: a typed witness object, a preserved invariant, an explicit lemma chain, and a falsification route organized around hardness magnification.

## Relevant Local References

- [Reference] `st.def.item` Definition of P
  P is the class of languages decidable by deterministic polynomial-time Turing machines.
- [Reference] `st.def.item-2` Definition of NP
  NP is the class of languages whose yes instances admit polynomial-size certificates verifiable in polynomial time.
- [Reference] `st.def.np-completeness` Definition of NP-completeness
  A language is NP-complete if it lies in NP and every language in NP polynomial-time many-one reduces to it.
- [Reference] `st.thm.cook-levin-sat-is-np-complete-cook1971` Cook-Levin
  SAT is NP-complete.
- [Reference] `st.def.item-5` Definition of P/poly
  P/poly is the class of languages decided by polynomial-size Boolean circuit families, equivalently polynomial-time computation with polynomial-length advice.
- [Reference] `st.thm.nonuniform-separation-target` Nonuniform separation target
  If NP is not contained in P/poly, then P != NP.
- [Leading-route source statement] `st.def.hardness-magnification-phenomenon-programme-leve` Leading-route source
  A hardness magnification theorem has the form:"A barely-nontrivial lower bound for an explicit problem Q in a weak model implies a major lower bound/separation in a strong model."Typically, Q is a meta-problem (e.g. a Gap-MCSP variant) and"major"means consequences such as NP not in P/poly.
- [Leading-route target statement] `st.thm.oliveira-pich-santhanam-magnification-near-state` Leading-route target
  In refined regimes, lower bounds for Gap-MCSP slightly beyond known frontiers (e.g. N^ 1+varepsilon -type circuit lower bounds for suitable promise gaps and input length N=2^n ) imply major consequences such as NP not in P/poly.
- [Supporting-route target statement] `st.thm.oliveira-santhanam-hardness-magnification-for-na` bridge.002
  There exist explicit"meta"problems (including MCSP variants) such that proving certain barely-superlinear lower bounds against restricted models (e.g. formulas) would imply major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter regimes consequences as strong as NP not in P/poly ).
- [Supporting-route target statement] `st.thm.atserias-m-uller-simple-general-magnification-fr` bridge.016
  There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for distinguishers/sparse-code objects can be amplified into stronger circuit/formula lower bounds, achieving magnification thresholds below previously known lower bounds in some settings.
