# Theorem Discovery Simulation

## Summary

- KB: KB/riesz-markov-kakutani-representation-theorem.kb.md
- Working KB: /Users/user/files/abducer/abducer/artifacts/riesz-markov-kakutani-representation-theorem/discovery-simulation/working-kb/riesz-markov-kakutani-representation-theorem.kb.md
- Target statement: st.thm.riesz-markov-kakutani
- Ground truth source: inferred-from-kb-dependencies
- Knockout profile: bridge-concept
- Iterations requested: 12
- Iterations executed: 8
- Success threshold: 0.9
- Replicated: True
- Best replication score: 0.909717

## Knockout

- Profile: `bridge-concept`
- Blanked fields: 24
- Dropped edges: 4
- Redacted mentions: 5
- Hidden bridge concepts:
  - `cnc.regular-borel-measure`
- Hidden bridge terms:
  - `regular Borel measure`
- Removed statements:
  - `st.def.regular-borel-measure`
  - `st.def.signed-regular-measure`

## Ground Truth

- Target: `st.thm.riesz-markov-kakutani`
- Discovery sequence length: 10
- Sequence:
  - `st.def.lch-space`
  - `st.def.cc-space`
  - `st.def.regular-borel-measure`
  - `st.def.positive-linear-functional`
  - `st.lem.compact-open-approximation`
  - `st.prop.integration-defines-functional`
  - `st.lem.uniqueness-from-cc-separation`
  - `st.thm.positive-functional-implies-measure`
  - `st.thm.riesz-markov-kakutani`
  - `st.cor.c0-dual-representation`

## Iterations

| iter | score | target-rank | edge-hit | bridges | conjectures | sketches | status |
|---|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.8497 | 1.0000 | 0.8125 | 20 | 36 | 6 | ok |
| 2 | 0.8497 | 1.0000 | 0.8125 | 20 | 36 | 6 | ok |
| 3 | 0.8699 | 1.0000 | 0.8750 | 20 | 36 | 6 | ok |
| 4 | 0.8454 | 1.0000 | 0.8125 | 20 | 36 | 6 | ok |
| 5 | 0.8441 | 1.0000 | 0.8125 | 20 | 36 | 6 | ok |
| 6 | 0.8497 | 1.0000 | 0.8125 | 20 | 36 | 6 | ok |
| 7 | 0.8497 | 1.0000 | 0.8125 | 20 | 36 | 6 | ok |
| 8 | 0.9097 | 1.0000 | 1.0000 | 30 | 48 | 6 | ok |

## Best Iteration

- Iteration: 8
- Replication score: 0.909717
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
  - `/Users/user/files/abducer/abducer/artifacts/riesz-markov-kakutani-representation-theorem/discovery-simulation/iter-008`
