# Theorem Discovery Simulation

## Summary

- KB: KB/stone-one-parameter-unitary-groups.kb.md
- Working KB: /Users/user/files/abducer/abducer/artifacts/stone-one-parameter-unitary-groups/discovery-simulation/working-kb/stone-one-parameter-unitary-groups.kb.md
- Target statement: st.thm.stone-correspondence
- Ground truth source: inferred-from-kb-dependencies
- Knockout profile: bridge-concept
- Iterations requested: 12
- Iterations executed: 5
- Success threshold: 0.9
- Replicated: True
- Best replication score: 0.900999

## Knockout

- Profile: `bridge-concept`
- Blanked fields: 20
- Dropped edges: 3
- Redacted mentions: 1
- Hidden bridge concepts:
  - `cnc.infinitesimal-generator`
- Hidden bridge terms:
  - `infinitesimal generator`
  - `self-adjoint generator`
- Removed statements:
  - `st.def.infinitesimal-generator`

## Ground Truth

- Target: `st.thm.stone-correspondence`
- Discovery sequence length: 9
- Sequence:
  - `st.def.self-adjoint-operator`
  - `st.def.unitary-group`
  - `st.thm.spectral-theorem-functional-calculus`
  - `st.def.infinitesimal-generator`
  - `st.thm.self-adjoint-implies-unitary-group`
  - `st.prop.generator-domain-regularity`
  - `st.prop.generator-symmetry`
  - `st.thm.unitary-group-implies-self-adjoint-generator`
  - `st.thm.stone-correspondence`

## Iterations

| iter | score | target-rank | edge-hit | bridges | conjectures | sketches | status |
|---|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.8964 | 1.0000 | 0.8000 | 20 | 36 | 6 | ok |
| 2 | 0.8964 | 1.0000 | 0.8000 | 20 | 36 | 6 | ok |
| 3 | 0.8966 | 1.0000 | 0.8000 | 20 | 36 | 6 | ok |
| 4 | 0.8956 | 1.0000 | 0.8000 | 20 | 36 | 6 | ok |
| 5 | 0.9010 | 1.0000 | 0.8000 | 20 | 36 | 6 | ok |

## Best Iteration

- Iteration: 5
- Replication score: 0.900999
- Config:
  - `analyze_top_k`: 20
  - `bridge_top_k`: 20
  - `conjecture_top_bridges`: 12
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
  - `top_interventions`: 16
  - `top_links`: 24
- Artifact root:
  - `/Users/user/files/abducer/abducer/artifacts/stone-one-parameter-unitary-groups/discovery-simulation/iter-005`
