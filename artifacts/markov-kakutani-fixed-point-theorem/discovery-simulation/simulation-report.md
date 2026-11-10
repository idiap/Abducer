# Theorem Discovery Simulation

## Summary

- KB: KB/markov-kakutani-fixed-point-theorem.kb.md
- Working KB: /Users/user/files/abducer/abducer/artifacts/markov-kakutani-fixed-point-theorem/discovery-simulation/working-kb/markov-kakutani-fixed-point-theorem.kb.md
- Target statement: st.thm.markov-kakutani
- Ground truth source: inferred-from-kb-dependencies
- Knockout profile: bridge-concept
- Iterations requested: 12
- Iterations executed: 8
- Success threshold: 0.9
- Replicated: True
- Best replication score: 0.909892

## Knockout

- Profile: `bridge-concept`
- Blanked fields: 16
- Dropped edges: 5
- Redacted mentions: 3
- Hidden bridge concepts:
  - `cnc.invariant-fixed-point-subset`
- Hidden bridge terms:
  - `fixed-point subset`
- Removed statements:
  - `st.def.commuting-affine-family`
  - `st.def.fixed-point-subset`

## Ground Truth

- Target: `st.thm.markov-kakutani`
- Discovery sequence length: 9
- Sequence:
  - `st.def.compact-convex-set`
  - `st.def.commuting-affine-family`
  - `st.def.fixed-point-subset`
  - `st.lem.cesaro-averages`
  - `st.lem.single-map-fixed-point`
  - `st.prop.fixed-point-subset-structure`
  - `st.lem.commuting-preserves-fixed-point-subset`
  - `st.lem.finite-family-common-fixed-point`
  - `st.thm.markov-kakutani`

## Iterations

| iter | score | target-rank | edge-hit | bridges | conjectures | sketches | status |
|---|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.8682 | 1.0000 | 0.8333 | 20 | 35 | 6 | ok |
| 2 | 0.8682 | 1.0000 | 0.8333 | 20 | 35 | 6 | ok |
| 3 | 0.8682 | 1.0000 | 0.8333 | 20 | 35 | 6 | ok |
| 4 | 0.8973 | 1.0000 | 0.9167 | 20 | 35 | 6 | ok |
| 5 | 0.8670 | 1.0000 | 0.8333 | 20 | 35 | 6 | ok |
| 6 | 0.8682 | 1.0000 | 0.8333 | 20 | 35 | 6 | ok |
| 7 | 0.8682 | 1.0000 | 0.8333 | 20 | 35 | 6 | ok |
| 8 | 0.9099 | 1.0000 | 1.0000 | 28 | 47 | 6 | ok |

## Best Iteration

- Iteration: 8
- Replication score: 0.909892
- Config:
  - `analyze_top_k`: 20
  - `bridge_top_k`: 30
  - `conjecture_top_bridges`: 16
  - `entry_top_k`: 20
  - `margin`: 0.06
  - `max_conjectures_per_bridge`: 3
  - `max_connections`: 40
  - `max_hypotheses_per_path`: 4
  - `max_links_per_path`: 3
  - `min_similarity`: 0.12
  - `pathway_top_entrypoints`: 8
  - `refute_threshold`: 0.6
  - `sketch_top_k`: 6
  - `strategies_top_k`: 6
  - `support_threshold`: 0.6
  - `top_conceptual`: 12
  - `top_interventions`: 12
  - `top_links`: 20
- Artifact root:
  - `/Users/user/files/abducer/abducer/artifacts/markov-kakutani-fixed-point-theorem/discovery-simulation/iter-008`
