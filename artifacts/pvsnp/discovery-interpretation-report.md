# Discovery Interpretation Report

This report narrates the discovery state in human-readable terms.

## Context

- Generated (UTC): 2026-03-11T11:48:42.971931+00:00
- KB: KB/p-vs-np.kb.md
- Artifacts directory: /Users/user/files/abducer/abducer/artifacts/pvsnp

## Current Discovery Posture

- Statement coverage in reasoning graph: 64
- Candidate conceptual/bridge links: 40
- Global coherence baseline: 0.2140
- Open hypotheses after loop: 44

## Highest-Informative Intervention Points

- `st.def.item` (score 0.1500): cross-component lexical bridge with st.def.item-2
- `st.def.item-2` (score 0.1500): cross-component lexical bridge with st.def.item
- `st.def.item-4` (score 0.1436): cross-component lexical bridge with st.def.item
- `st.def.item-3` (score 0.1412): cross-component lexical bridge with st.def.item-2
- `st.def.exponential-time-classes` (score 0.1385): cross-component lexical bridge with st.def.item-2
- `st.def.polynomial-time-many-one-karp-reduction` (score 0.1295): cross-component lexical bridge with st.def.item-2

## Coherence-Sensitive Hypothesis Readout

Positive contributions (good retention candidates):
- `phyp.p-vs-np.019` [bridge-link] coh_delta=0.0173, expl=0.4500
- `phyp.p-vs-np.021` [intervention-focus] coh_delta=0.0152, expl=0.1020
- `phyp.p-vs-np.008` [bridge-link] coh_delta=0.0146, expl=0.4635
- `phyp.p-vs-np.010` [bridge-link] coh_delta=0.0146, expl=0.4596
- `phyp.p-vs-np.040` [definition-introduction] coh_delta=0.0145, expl=0.5553

Negative contributions (reformulate or demote):
- `phyp.p-vs-np.031` [intervention-focus] coh_delta=-0.0045, expl=0.0943
- `phyp.p-vs-np.027` [intervention-focus] coh_delta=-0.0045, expl=0.0949
- `phyp.p-vs-np.025` [intervention-focus] coh_delta=-0.0018, expl=0.0981

## Bridge and Strategy Interpretation

- `bridge.001`: `st.def.item` -> `st.def.item-2` (structural support bridge, score 0.5345).
- `bridge.005`: `st.def.item-2` -> `st.def.item-4` (structural support bridge, score 0.5221).
- `bridge.009`: `st.def.item-2` -> `st.def.polynomial-time-many-one-karp-reduction` (structural support bridge, score 0.5200).
- `bridge.011`: `st.def.item-2` -> `st.def.polynomial-hierarchy` (structural support bridge, score 0.5164).
- `bridge.002`: `st.def.item` -> `st.def.item-4` (structural support bridge, score 0.5157).

Most promising strategy anchors:
- `strat.001` around `st.def.item`: score 0.6883, concept fertility 0.6870.
- `strat.002` around `st.def.polynomially-bounded-proof-system`: score 0.6634, concept fertility 0.6341.
- `strat.003` around `st.thm.cook-reckhow-proof-systems-and-cookreckhow1979`: score 0.5810, concept fertility 0.6340.
- `strat.004` around `st.def.item-3`: score 0.5728, concept fertility 0.6057.

## Hardness and Barrier Interpretation

- Sparse Explicit Dependency Structure (high, score 1.0000): Most canonical statements are not yet wired by formal depends_on links, so proof navigation is underdetermined.
- Asymmetric Lower-Bound Evidence (medium, score 0.6667): The KB has strong restricted-model lower bounds but relatively fewer direct bridges to full separation targets.
- Bridge-Hypothesis Dependence (medium, score 0.6562): Progress currently depends on conjectural bridges/hypotheses to connect otherwise weakly linked conceptual regions.
- Plural, Underdetermined Strategy Space (moderate, score 0.3750): Top entry points span multiple conceptual phases, indicating no single dominant route and high epistemic underdetermination.

Anti-barrier programs to test:
- relativization: Introduce intermediate invariant that is not preserved by the barrier regime.; Search for representation-shift that maps target to a non-barrier proof model.
- natural-proofs: Introduce intermediate invariant that is not preserved by the barrier regime.; Search for representation-shift that maps target to a non-barrier proof model.
- algebrization: Introduce intermediate invariant that is not preserved by the barrier regime.; Search for representation-shift that maps target to a non-barrier proof model.

## Hypothesis-State Interpretation

- Immediate verdict profile: {"inconclusive": 42, "supported": 2}
- Loop final state: supported=0, refuted=0, open=44.
- Revision loop suggests these high-priority conceptual repairs:
  - `rev.001` [concept-splitting]: Split overloaded target concepts into finer-grained definitions and rerun connector + abduce.
  - `rev.002` [regime-switch]: Switch to alternate proof regimes suggested by anti-barrier programs and re-encode targets.
  - `rev.003` [representation-rotation]: Rotate representation/normal-form assumptions for unresolved conceptual hypotheses.

## Suggested Next Moves (Human Workflow)

1. Keep only hypotheses with non-negative coherence delta unless there is strong external evidence.
2. Execute top bridge programs in recommended order and log outcome against target theorem IDs.
3. Use anti-barrier programs as explicit experimental tracks, not just commentary.
4. If open hypotheses remain high after one more round, apply revision-loop actions before re-running abduction/deduction.
