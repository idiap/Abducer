# High-risk conceptual portfolio for P versus NP

- Date: 2026-07-21
- Portfolio status: `literature_blind_incubation`
- Truth status: every hypothesis is conjectural and unproved
- Novelty status: not assessed; a current target-scoped literature refresh is required

## Charter and non-claim boundary

The portfolio asks whether repeated lower-bound barriers arise because proof
methods erase the distinctions that would have to carry hardness. Preserve the
standard definitions of `P` and `NP`, worst-case semantics, uniformity,
quantifier order, nontriviality, reductions, and the exact scope of known
barriers. No primitive may be defined using “is hard,” “not in P,” SAT truth
labels, or access to the desired conclusion.

The central intuition is **distinction-carrying coherence**:

> Hardness may be located not in a static property of one Boolean function but
> in the failure of locally adequate computational views to cohere into one
> uniform polynomial-time algorithm. Relativization, broad natural properties,
> algebraic completion, averaging, or quotienting may preserve local pieces
> while deleting their decisive transition data.

This is a theory-generating frame, not a separation result.

## Aggressive hypotheses

### H1 — Computational descent defect

- **Corner:** ontology inversion and local-to-global emergence.
- **Leap:** treat hardness as a nonzero gluing defect among locally consistent
  solver fragments rather than a scalar property of a truth table.
- **New objects:** a syntactically defined cover of instance space, partial
  solver sections, overlap maps, and a cocycle-like defect.
- **If right:** locality, representation dependence, and several barrier
  phenomena become forms of lost descent data; nonvanishing could obstruct a
  global uniform solver.
- **Primary risk:** “global section exists” or “defect is nonzero” may simply
  restate the target.
- **Learning if false:** identifies which computational local-to-global
  formulations are tautological.
- **First action:** define the cover and defect in a restricted circuit or proof
  model without truth labels, then prove nontriviality or exhibit collapse.

### H2 — Proof-observable quotient theory

- **Corner:** missing mediator and observer–realizer split.
- **Leap:** insert an explicit distinction channel between computational objects
  and what a proof method can observe.
- **New objects:** an observation map, its kernel equivalence, and a distinction
  capacity measuring which relations survive.
- **If right:** barrier theorems become a common theory of proof-method
  information loss, and an escape route becomes a minimal enrichment of the
  observable language.
- **Primary risk:** redescribing each known barrier after the fact.
- **Learning if false:** shows that the barrier families do not share one
  independently motivated information-loss principle.
- **First action:** seek one kernel axiom that derives consequences in at least
  two barrier regimes and predicts a new observable.

### H3 — Algorithm-indexed adversarial obstruction

- **Corner:** relation/process primacy and counter-consensus.
- **Leap:** stop seeking one broad property shared by hard functions; construct
  a distinct but uniformly generated obstruction for each candidate
  polynomial-time machine and exponent.
- **New objects:** a verifier-grounded adversarial transformation game indexed
  by an algorithm and resource bound.
- **If right:** the quantifier order of separation becomes the organizing
  principle and may avoid the breadth condition exploited by natural proofs.
- **Primary risk:** the adversary uses unknown truth values, hidden unbounded
  advice, or diagonalizes outside `NP`.
- **Learning if false:** sharply characterizes why per-algorithm witnesses do
  not compose into a uniform lower bound.
- **First action:** specify a label-free move rule and a winning condition whose
  restricted-model version implies actual algorithm error.

### H4 — Cross-scale coherence spectrum

- **Corner:** scale reversal and noncommuting limits.
- **Leap:** distinguish “there is a good solver at every input length” from “one
  fixed, uniformly describable polynomial-time machine works at every length.”
- **New objects:** a landscape of finite-scale solvers and a transition cost
  between near-optimal solvers at adjacent scales.
- **If right:** unavoidable transition complexity could expose the information
  lost by per-length and finite-size approximations.
- **Primary risk:** collapse to the known distinction between uniform and
  nonuniform computation without a route from transition cost to runtime.
- **Learning if false:** yields a compactness or extraction theorem explaining
  when cross-scale coherence is automatic.
- **First action:** prove or refute a restricted solver-path compactness lemma.

### H5 — Worst-case computational renormalization

- **Corner:** cross-field mechanism transfer; protected wildcard.
- **Leap:** let exact reductions and restrictions induce a scale flow in which
  tractable problems reach finite-complexity fixed points while an `NP`-complete
  constraint system retains a relevant obstruction.
- **New objects:** a semantics-preserving worst-case coarse-graining operator,
  fixed points, and relevant directions.
- **If right:** self-reduction, restrictions, multiscale behavior, and lower
  bounds acquire one explanatory mechanism.
- **Primary risk:** a physics metaphor that smuggles in average-case ensembles,
  changes the language, or renames hardness.
- **Learning if false:** identifies which renormalization assumptions cannot
  transport to worst-case computation.
- **First action:** construct an exact compositional coarse-graining on a
  canonical SAT encoding and search for one nontrivial restricted-model invariant.

### H6 — Barrier-completeness no-go theory

- **Corner:** negative theory and unification conjecture.
- **Leap:** treat relativization, largeness/constructivity, and algebraic
  completion as shadows of a shared closure principle for
  distinction-erasing proof observables.
- **New objects:** axioms for closure, completion, and sensitivity to the target
  distinction.
- **If right:** a meta-theorem explains several recurring failures and an
  escape lemma identifies the smallest closure axiom a successful route must
  violate.
- **Primary risk:** concatenating known barriers under new terminology.
- **Learning if false:** proves that the barriers protect materially different
  information and should not be unified.
- **First action:** derive two barrier-like consequences from one independently
  motivated completion operation or demote the hypothesis.

### H7 — Dual obstruction certificates

- **Corner:** duality and completion; protected wildcard.
- **Leap:** pair every candidate efficient algorithm with a finite dual witness
  of a violated global consistency condition.
- **New objects:** primal algorithm space, constraint space, a pairing, and a
  dual obstruction rank.
- **If right:** lower bounds become composable certificates of gluing failure
  without requiring a broad natural property of functions.
- **Primary risk:** the separation theorem is nonconstructive, exponentially
  large, truth-table dependent, or equivalent to the desired conclusion.
- **Learning if false:** isolates why useful duality stops at restricted models.
- **First action:** find a finite circuit model in which dual rank exactly
  characterizes a nontrivial coherence failure and can be lower-bounded directly.

### H8 — Sparse canonical invariant control

- **Corner:** conservative control.
- **Leap:** retain conventional lower-bound development but target a sparse,
  representation-sensitive invariant of a canonical `NP`-complete encoding.
- **New objects:** a non-large property bound to uniform circuit descriptions
  and explicit reduction data.
- **If right:** supplies a lower-distance route and a control against which the
  conceptual leaps can be judged.
- **Primary risk:** encoding dependence or failure to scale beyond a restricted
  model.
- **Learning if false:** provides a clean negative result about the chosen
  representation and invariant.
- **First action:** identify the weakest circuit class where the invariant is
  nontrivial, provable, and audited against the applicable barriers.

## Portfolio structure

| ID | Primary object | Mechanism | Reward | Collapse risk |
|---|---|---|---|---|
| H1 | Local sections and overlaps | Nonzero gluing defect | Very high | Tautological restatement |
| H2 | Observation map and kernel | Recover a lost distinction | High | Post-hoc barrier vocabulary |
| H3 | Machine-indexed game | Uniform adversarial witness | Very high | Hidden labels or advice |
| H4 | Solver path over scales | Transition/compactness failure | High | Merely `P/poly` versus `P` |
| H5 | Exact scale flow | Persistent relevant direction | Very high | Analogy without transport |
| H6 | Proof-method closure axioms | No-go plus escape lemma | High | List of known barriers |
| H7 | Primal/dual spaces | Finite obstruction certificate | Very high | Nonconstructive duality |
| H8 | Sparse canonical invariant | Restricted lower-bound induction | Medium | Representation fragility |

H5 and H7 are protected wildcards. H8 is the control. H1/H7, H2/H6, and H3/H4
have medium overlap but distinct primitives, mechanisms, and maturation
questions; they should not be merged before producing independent deltas.

## Literature status and required rebase

The repository does not currently provide an admissible recent P-vs-NP search
snapshot. The shared target-literature `latest` artifact identifies Yang–Mills,
while the local P-vs-NP prior-art packet is bounded evidence without the search
queries, coverage cutoff, inclusion policy, content digest, and validator
receipts required by `frontier-literature-assimilator`.

Therefore every hypothesis has literature relation `pending_rebase`. Local
prior-art can guide targeted queries, but none of H1–H8 may claim novelty,
receive proof-scale investment, or enter a preferred synthesis until a current
target-scoped snapshot classifies it as apparently open, anticipated, absorbed,
contradicted, independent, or a genuine cross-field bridge.

## Parallel maturation manifest

The eight hypotheses are designed for one blind-divergence wave with at most
eight workers, reusing the existing marathon worker pool only after the
`DWF-015` adapter enforces the following contract:

- immutable P-vs-NP target, theory-state, and literature digests;
- one distinct mechanism, maturation question, namespace, budget, and
  invocation ID per branch;
- no worker reads a global `latest`, sibling output, or shared mutable state;
- each attempt returns a typed receipt, including timeout or failure;
- every branch is validated independently and valid siblings survive failure;
- a new literature snapshot marks every survivor `literature_superseded` and
  forces rebase before cross-pollination or synthesis;
- optional second-wave pairings are H1↔H7, H2↔H6, and H3↔H4, with H8 auditing
  target and model preservation across all radical branches;
- one single-writer compare-and-swap reducer retains opposition, duplicates,
  synthesis ancestry, the control, and at least one serious dissenter.

Execution disposition: `planned_not_executed`. The current API parallel runner
already provides worker concurrency, but it does not yet provide the required
partial-success recovery, target-scoped literature rebase, typed conceptual
merge, or transactional reducer. Those are the acceptance boundary of
`DWF-015`.
