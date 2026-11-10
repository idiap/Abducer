# Theorem Discovery Simulation

## Summary

- KB: KB/hille-yosida-theorem.kb.md
- Working KB: /Users/user/files/abducer/abducer/artifacts/hille-yosida-theorem/discovery-simulation/working-kb/hille-yosida-theorem.kb.md
- Target statement: st.thm.hille-yosida-general
- Ground truth source: inferred-from-kb-dependencies
- Knockout profile: proof-structure
- Iterations requested: 20
- Iterations executed: 8
- Success threshold: 0.9
- Replicated: True
- Best replication score: 0.946818

## Knockout

- Profile: `proof-structure`
- Blanked fields: 30
- Dropped edges: 0

## Ground Truth

- Target: `st.thm.hille-yosida-general`
- Discovery sequence length: 7
- Sequence:
  - `st.def.c0-semigroup`
  - `st.def.resolvent`
  - `st.def.generator`
  - `st.prop.generator-closed-dense`
  - `st.thm.hille-yosida-general`
  - `st.der.yosida-approximation`
  - `st.thm.hille-yosida-contraction`

## Iterations

| iter | score | target-rank | edge-hit | bridges | conjectures | sketches | status |
|---|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.8413 | 1.0000 | 0.6667 | 20 | 34 | 6 | ok |
| 2 | 0.8413 | 1.0000 | 0.6667 | 20 | 34 | 6 | ok |
| 3 | 0.8432 | 1.0000 | 0.6667 | 20 | 34 | 6 | ok |
| 4 | 0.8594 | 1.0000 | 0.7778 | 20 | 34 | 6 | ok |
| 5 | 0.8858 | 1.0000 | 0.8889 | 20 | 34 | 6 | ok |
| 6 | 0.8413 | 1.0000 | 0.6667 | 20 | 34 | 6 | ok |
| 7 | 0.8413 | 1.0000 | 0.6667 | 20 | 34 | 6 | ok |
| 8 | 0.9468 | 1.0000 | 1.0000 | 30 | 42 | 6 | ok |

## Best Iteration

- Iteration: 8
- Replication score: 0.946818
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
  - `/Users/user/files/abducer/abducer/artifacts/hille-yosida-theorem/discovery-simulation/iter-008`
