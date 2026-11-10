# Proof Strategy Portfolio

## Stats

- Strategies: 6
- Pathways used: 8
- Bridges used: 20
- Hypotheses used: 44
- Coherence signals used: 44

## Strategies

| strategy_id | name | phase | anchor | score | fertility |
|---|---|---|---|---|---|
| strat.001 | Cross-Model Strategy around st.def.item | 1) Foundational language of complexity | st.def.item | 0.6883 | 0.687 |
| strat.002 | Proof-Complexity Transfer around st.def.polynomially-bounded-proof-system | Paragraph: Proof complexity. | st.def.polynomially-bounded-proof-system | 0.6634 | 0.6341 |
| strat.003 | Proof-Complexity Transfer around st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 | 8) Proof complexity as a parallel route | st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 | 0.581 | 0.634 |
| strat.004 | Cross-Model Strategy around st.def.item-3 | 1) Foundational language of complexity | st.def.item-3 | 0.5728 | 0.6057 |
| strat.005 | Cross-Model Strategy around st.def.item-2 | 1) Foundational language of complexity | st.def.item-2 | 0.5514 | 0.6068 |
| strat.006 | Cross-Model Strategy around st.def.np-completeness | 1) Foundational language of complexity | st.def.np-completeness | 0.5196 | 0.6046 |

### strat.001 - Cross-Model Strategy around st.def.item
- Anchor: st.def.item
- Phase: 1) Foundational language of complexity
- Score: 0.6883
- Concept fertility: 0.687
- Bridges: bridge.001, bridge.002, bridge.014
- Hypotheses: phyp.p-vs-np.001, phyp.p-vs-np.002, phyp.p-vs-np.033, phyp.p-vs-np.034
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.8, barrier_evasion=0.8, lemma_generation=0.5, explanatory_avg=0.5213, coherence_avg=0.0063
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.item and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.002 - Proof-Complexity Transfer around st.def.polynomially-bounded-proof-system
- Anchor: st.def.polynomially-bounded-proof-system
- Phase: Paragraph: Proof complexity.
- Score: 0.6634
- Concept fertility: 0.6341
- Bridges: bridge.003, bridge.010
- Hypotheses: phyp.p-vs-np.003, phyp.p-vs-np.010, phyp.p-vs-np.035, phyp.p-vs-np.042
- Fertility components: unification_gain=0.375, proof_compression=0.6667, transfer_power=0.6, barrier_evasion=0.8, lemma_generation=0.5, explanatory_avg=0.5115, coherence_avg=0.009
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.polynomially-bounded-proof-system and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.003 - Proof-Complexity Transfer around st.thm.cook-reckhow-proof-systems-and-cookreckhow1979
- Anchor: st.thm.cook-reckhow-proof-systems-and-cookreckhow1979
- Phase: 8) Proof complexity as a parallel route
- Score: 0.581
- Concept fertility: 0.634
- Bridges: bridge.003, bridge.004
- Hypotheses: phyp.p-vs-np.003, phyp.p-vs-np.004, phyp.p-vs-np.035, phyp.p-vs-np.036
- Fertility components: unification_gain=0.375, proof_compression=0.6667, transfer_power=0.6, barrier_evasion=0.8, lemma_generation=0.5, explanatory_avg=0.5153, coherence_avg=0.0035
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.004 - Cross-Model Strategy around st.def.item-3
- Anchor: st.def.item-3
- Phase: 1) Foundational language of complexity
- Score: 0.5728
- Concept fertility: 0.6057
- Bridges: bridge.006, bridge.012, bridge.017
- Hypotheses: phyp.p-vs-np.006, phyp.p-vs-np.012, phyp.p-vs-np.017, phyp.p-vs-np.038
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, explanatory_avg=0.4831, coherence_avg=0.0062
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.item-3 and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.005 - Cross-Model Strategy around st.def.item-2
- Anchor: st.def.item-2
- Phase: 1) Foundational language of complexity
- Score: 0.5514
- Concept fertility: 0.6068
- Bridges: bridge.001, bridge.005, bridge.009
- Hypotheses: phyp.p-vs-np.001, phyp.p-vs-np.005, phyp.p-vs-np.009, phyp.p-vs-np.033
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, explanatory_avg=0.4939, coherence_avg=0.0063
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.item-2 and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.006 - Cross-Model Strategy around st.def.np-completeness
- Anchor: st.def.np-completeness
- Phase: 1) Foundational language of complexity
- Score: 0.5196
- Concept fertility: 0.6046
- Bridges: bridge.007, bridge.017, bridge.018
- Hypotheses: phyp.p-vs-np.017, phyp.p-vs-np.018, phyp.p-vs-np.039, phyp.p-vs-np.007
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, explanatory_avg=0.4725, coherence_avg=0.0061
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.np-completeness and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

## Novelty-Maximizing Prompt

```text
You are a proof-strategy synthesizer optimizing novelty under rigor constraints.
Inputs: KB slice, ranked strategies, bridge programs, hypothesis sets.
Objective: maximize expected proof progress while maximizing conceptual novelty.
Novelty score N = 0.40*phase_diversity + 0.30*bridge_originality + 0.20*hypothesis_nonredundancy + 0.10*minimal_assumption_gain.
Hard constraints:
1. Every proposed step must reference statement IDs.
2. Each strategy round must include at least one bridge from a phase different than the previous round.
3. Reject proposals that only restate existing dependencies without adding new conditional entailment paths.
4. Prefer smallest hypothesis sets that unlock the largest new consequence set.
Procedure:
- Select top strategy by score.
- Generate 3 candidate proof moves; each must combine anchor + bridge + hypothesis.
- Score each move by (validity risk, novelty gain, expected entailment gain).
- Keep the best move, archive the other two, then rotate to a different conceptual phase.
Output format:
### Chosen Strategy
### Candidate Moves (3)
### Scores
### Selected Move and Rationale
### Next-Round Phase Constraint
```
