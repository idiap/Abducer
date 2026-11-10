---
kb_id: markov-kakutani-fixed-point-theorem
title: Markov-Kakutani Fixed-Point Theorem
domain: mathematics
subdomain: functional-analysis-convex-fixed-point
version: 0.1.0
status: draft
created_utc: 2026-03-12T00:00:00Z
updated_utc: 2026-03-12T00:00:00Z
owners:
  - abducer
source_policy:
  allow_web: true
  allow_local_docs: true
  citation_required: true
---

# Source Index

| source_id | type | citation | locator | reliability | notes |
|---|---|---|---|---|---|
| src.001 | web | https://en.wikipedia.org/wiki/Markov%E2%80%93Kakutani_fixed-point_theorem | sections "Statement" and "Proof sketch" | medium | Concise statement of the commuting affine fixed-point theorem |
| src.002 | book | Aliprantis, C. D.; Border, K. C. (2006). Infinite Dimensional Analysis. Springer. | section on fixed-point theorems in locally convex spaces | high | Standard reference for compact-convex fixed-point arguments |
| src.003 | book | Conway, J. B. (1990). A Course in Functional Analysis. Springer. | sections on locally convex spaces and compactness | high | Background for topological vector space and compactness ingredients |
| src.004 | paper | Markov, A.; Kakutani, S. historical fixed-point theorem lineage | original commuting-family fixed-point theorem lineage | high | Historical source family for the common fixed-point result |

# Symbol Glossary

- `sym.E`: locally convex topological vector space.
- `sym.K`: nonempty compact convex subset of `E`.
- `sym.T`: continuous affine self-map of `K`.
- `sym.F`: commuting family of continuous affine self-maps of `K`.
- `sym.x`: point of `K`.
- `sym.FixT`: fixed-point subset `\operatorname{Fix}(T)`.
- `sym.AN`: Cesaro average operator `A_N`.

# Concept Structure

```yaml
concept_nodes:
  - id: cnc.compact-convex-set
    label: Compact Convex Subset
    type: concept
  - id: cnc.commuting-affine-family
    label: Commuting Family of Continuous Affine Self-Maps
    type: concept
  - id: cnc.invariant-fixed-point-subset
    label: Invariant Fixed-Point Subset
    type: concept
    notes: |
      Hidden bridge object reducing the family fixed-point problem to preserved compact convex subsets.
  - id: cnc.cesaro-averaging
    label: Cesaro Averaging Scheme
    type: concept
  - id: cnc.common-fixed-point
    label: Common Fixed Point
    type: concept
  - id: cnc.finite-intersection-property
    label: Finite Intersection Property
    type: concept
method_nodes:
  - id: mth.affine-averaging
    label: Affine Averaging Route
    type: method
  - id: mth.invariant-subset-reduction
    label: Invariant Fixed-Point Subset Reduction
    type: method
  - id: mth.compactness-intersection
    label: Finite-Intersection Compactness Lift
    type: method
barrier_nodes:
  - id: bar.single-map-fixed-point-extraction
    label: Single-Map Fixed-Point Extraction Barrier
    type: barrier
  - id: bar.invariant-subset-propagation
    label: Invariant Subset Propagation Barrier
    type: barrier
  - id: bar.finite-intersection-compactness
    label: Finite-Intersection Compactness Barrier
    type: barrier
relations:
  - from: st.def.compact-convex-set
    to: cnc.compact-convex-set
    relation: defines
  - from: st.def.commuting-affine-family
    to: cnc.commuting-affine-family
    relation: defines
  - from: st.def.fixed-point-subset
    to: cnc.invariant-fixed-point-subset
    relation: defines
  - from: st.lem.cesaro-averages
    to: cnc.cesaro-averaging
    relation: uses
  - from: st.prop.fixed-point-subset-structure
    to: cnc.invariant-fixed-point-subset
    relation: uses
  - from: st.lem.commuting-preserves-fixed-point-subset
    to: mth.invariant-subset-reduction
    relation: uses
  - from: st.lem.finite-family-common-fixed-point
    to: mth.compactness-intersection
    relation: uses
  - from: st.thm.markov-kakutani
    to: cnc.common-fixed-point
    relation: uses
  - from: bar.single-map-fixed-point-extraction
    to: st.lem.single-map-fixed-point
    relation: obstructs
  - from: bar.invariant-subset-propagation
    to: st.lem.commuting-preserves-fixed-point-subset
    relation: obstructs
  - from: bar.finite-intersection-compactness
    to: st.lem.finite-family-common-fixed-point
    relation: obstructs
```

# Canonical Statements

```yaml
id: st.def.compact-convex-set
kind: definition
status: accepted
latex: 'Let E be a locally convex topological vector space. A subset K \subseteq E
  is compact convex if K is compact in the given topology and

  tx + (1-t)y \in K for all x,y \in K and all t \in [0,1].

  '
informal: 'The theorem lives on a nonempty compact convex subset because averaging
  and compactness both need this ambient geometry.

  '
source_ids:
- src.001
- src.002
- src.003
used_symbols:
- sym.E
- sym.K
- sym.x
depends_on: []
concept_roles:
- cnc.compact-convex-set
statement_phase: foundational-definitions
bridge_roles:
- compact-convex-foundation
method_tags:
- convex-geometry
- compactness-method
barrier_family: ''
confidence: 0.98
proof_sketch: ''
notes: Compactness gives accumulation points for averaging procedures and convexity
  keeps affine combinations inside K.
```





```yaml
id: st.lem.cesaro-averages
kind: lemma
status: accepted
latex: 'For a continuous affine self-map T : K \to K and x \in K, define

  A_N(x) := \frac{1}{N}\sum_{n=0}^{N-1} T^n x.

  Then A_N(x) \in K for every N.

  '
informal: 'Cesaro averages of a single affine orbit stay inside K and provide the
  averaging mechanism behind single-map fixed-point extraction.

  '
source_ids:
- src.001
- src.002
used_symbols:
- sym.T
- sym.K
- sym.x
- sym.AN
depends_on:
- st.def.compact-convex-set
concept_roles:
- cnc.cesaro-averaging
- cnc.compact-convex-set
statement_phase: affine-averaging
bridge_roles:
- affine-averaging-source
method_tags:
- affine-averaging
- convex-geometry
barrier_family: single-map-fixed-point-extraction
confidence: 0.95
proof_sketch: 'Each A_N(x) is a convex combination of points of K, so convexity keeps
  the averages inside K.

  '
notes: Averaging produces approximate fixed points for a single affine map.
```

```yaml
id: st.lem.single-map-fixed-point
kind: lemma
status: accepted
latex: 'If T : K \to K is a continuous affine self-map, then T has a fixed point in
  K.

  '
informal: 'A single continuous affine self-map of a nonempty compact convex set has
  at least one fixed point.

  '
source_ids:
- src.001
- src.002
used_symbols:
- sym.T
- sym.K
- sym.x
depends_on:
- st.def.compact-convex-set
- st.lem.cesaro-averages
concept_roles:
- cnc.cesaro-averaging
- cnc.common-fixed-point
- cnc.compact-convex-set
statement_phase: single-map-fixed-point
bridge_roles:
- single-map-fixed-point
method_tags:
- affine-averaging
- fixed-point-analysis
- separation-method
barrier_family: single-map-fixed-point-extraction
confidence: 0.94
proof_sketch: 'Use Cesaro averages and compactness to obtain an accumulation point,
  then show by continuity and affine cancellation that the limit is fixed.

  '
notes: This is the one-map ingredient from which the family theorem is built.
```

```yaml
id: st.prop.fixed-point-subset-structure
kind: proposition
status: accepted
latex: 'For a continuous affine self-map T : K \to K, the set \operatorname{Fix}(T)
  is nonempty, compact, and convex.

  '
informal: 'The [hidden bridge concept] of a single map is itself a nonempty compact
  convex set.

  '
source_ids:
- src.001
- src.002
used_symbols:
- sym.T
- sym.K
- sym.FixT
- sym.x
depends_on:
- st.lem.single-map-fixed-point
concept_roles: []
statement_phase: invariant-fixed-point-subset
bridge_roles: []
method_tags:
- fixed-point-analysis
- invariant-subset-method
- compactness-method
barrier_family: invariant-subset-propagation
confidence: 0.95
proof_sketch: ''
notes: ''
```

```yaml
id: st.lem.commuting-preserves-fixed-point-subset
kind: lemma
status: accepted
latex: 'Let S,T : K \to K be commuting continuous affine self-maps. Then

  S(\operatorname{Fix}(T)) \subseteq \operatorname{Fix}(T).

  '
informal: 'If two affine maps commute, then one preserves the [hidden bridge concept]
  of the other.

  '
source_ids:
- src.001
- src.002
used_symbols:
- sym.T
- sym.K
- sym.FixT
- sym.x
depends_on:
- st.prop.fixed-point-subset-structure
concept_roles: []
statement_phase: commuting-invariance
bridge_roles: []
method_tags:
- commuting-family-analysis
- invariant-subset-method
barrier_family: invariant-subset-propagation
confidence: 0.95
proof_sketch: ''
notes: ''
```

```yaml
id: st.lem.finite-family-common-fixed-point
kind: lemma
status: accepted
latex: 'Every finite commuting family of continuous affine self-maps of K has a common
  fixed point.

  '
informal: 'One can build a common fixed point for any finite commuting subfamily by
  iteratively restricting to invariant [hidden bridge concept]s.

  '
source_ids:
- src.001
- src.002
used_symbols:
- sym.F
- sym.K
- sym.x
- sym.FixT
depends_on:
- st.prop.fixed-point-subset-structure
- st.lem.commuting-preserves-fixed-point-subset
concept_roles: []
statement_phase: finite-family-lift
bridge_roles: []
method_tags:
- invariant-subset-method
- compactness-method
- induction-on-family-size
barrier_family: finite-intersection-compactness
confidence: 0.94
proof_sketch: ''
notes: ''
```

```yaml
id: st.thm.markov-kakutani
kind: theorem
status: accepted
latex: 'Let K be a nonempty compact convex subset of a locally convex topological
  vector space E.

  If F is a commuting family of continuous affine self-maps of K, then there exists
  x \in K such that

  T x = x \text{ for every } T \in F.

  '
informal: 'A commuting family of continuous affine self-maps on a nonempty compact
  convex set has a common fixed point.

  '
source_ids:
- src.001
- src.002
- src.004
used_symbols:
- sym.E
- sym.K
- sym.F
- sym.T
- sym.x
depends_on:
- st.def.compact-convex-set
- st.lem.finite-family-common-fixed-point
concept_roles: []
statement_phase: common-fixed-point-theorem
bridge_roles: []
method_tags:
- compactness-method
- invariant-subset-method
- fixed-point-analysis
barrier_family: finite-intersection-compactness
confidence: 0.96
proof_sketch: ''
notes: ''
```

```yaml
id: st.ex.interval-commuting-projections
kind: example
status: accepted
latex: 'Let K = [0,1] and let F be a commuting family of continuous affine contractions
  of K.

  Then the Markov-Kakutani theorem yields a common fixed point in [0,1].

  '
informal: 'On a compact interval, commuting affine self-maps illustrate the theorem
  in the simplest convex setting.

  '
source_ids:
- src.001
- src.002
used_symbols:
- sym.K
- sym.F
- sym.T
- sym.x
depends_on:
- st.thm.markov-kakutani
concept_roles:
- cnc.common-fixed-point
- cnc.commuting-affine-family
- cnc.compact-convex-set
statement_phase: examples-and-interpretation
bridge_roles:
- common-fixed-point-example
method_tags:
- fixed-point-analysis
barrier_family: ''
confidence: 0.9
proof_sketch: 'Apply the theorem directly to the interval viewed as a compact convex
  subset of \mathbb{R}.

  '
notes: This example makes the family-level common fixed-point conclusion concrete.
```

# Open Gaps

- How tightly can the invariant fixed-point subset mechanism be generalized beyond compact convex sets?
- Which weakening of commutativity still allows a finite-intersection style proof route?
- What is the minimal averaging argument needed to recover the single-map fixed-point lemma in this setting?

# Evolution Notes

- 2026-03-12: Initialized a discovery-oriented KB for the Markov-Kakutani fixed-point theorem with the invariant fixed-point subset treated as the main hidden bridge concept during simulation.
