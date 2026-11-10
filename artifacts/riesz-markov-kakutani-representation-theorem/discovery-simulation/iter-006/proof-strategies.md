# Proof Strategy Portfolio

## Stats

- Strategies: 6
- Pathways used: 10
- Bridges used: 20
- Conjectured abstractions used: 36
- Hypotheses used: 42
- Coherence signals used: 42

## Strategies

| strategy_id | name | phase | anchor | score | fertility | anchor_concepts |
|---|---|---|---|---|---|---|
| strat.001 | Cross-Model Strategy around st.thm.riesz-markov-kakutani | Current Bridge Agenda | st.thm.riesz-markov-kakutani | 0.7509 | 0.8686 | positive-functional-implies-regular-measure, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, regular-borel-measure-representation |
| strat.002 | Cross-Model Strategy around st.def.lch-space | Foundational Gauge-Theoretic Definitions | st.def.lch-space | 0.653 | 0.8345 | locally-compact-hausdorff-definition, cc-space-definition, compactly-supported-continuous-functions, locally-compact-Hausdorff-space |
| strat.003 | Cross-Model Strategy around st.lem.compact-open-approximation | Additional KB-Specific Phases | st.lem.compact-open-approximation | 0.6178 | 0.7985 | compact-open-approximation-supports-regularity, compact-open-approximation-on-lch-space, compact-open-regularity-witness, locally-compact-hausdorff-definition |
| strat.004 | Cross-Model Strategy around st.thm.positive-functional-implies-measure | Current Bridge Agenda | st.thm.positive-functional-implies-measure | 0.6099 | 0.8949 | positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, regular-borel-measure-definition, positive-functional-definition |
| strat.005 | Cross-Model Strategy around st.def.cc-space | Current Bridge Agenda | st.def.cc-space | 0.5948 | 0.8719 | positive-linear-functional-on-cc-space, locally-compact-hausdorff-definition, positive-functional-definition, cc-space-definition |
| strat.006 | Cross-Model Strategy around st.lem.uniqueness-from-cc-separation | Current Bridge Agenda | st.lem.uniqueness-from-cc-separation | 0.575 | 0.8329 | function-separation-implies-measure-uniqueness, compact-open-approximation-on-lch-space, regular-borel-measure-on-lch-space, unique-representing-measure |

### strat.001 - Cross-Model Strategy around st.thm.riesz-markov-kakutani
- Anchor: st.thm.riesz-markov-kakutani
- Phase: Current Bridge Agenda
- Score: 0.7509
- Concept fertility: 0.8686
- Anchor concepts: positive-functional-implies-regular-measure, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, regular-borel-measure-representation, functional-measure-correspondence
- Bridge concepts: compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, positive-functional-definition, positive-linear-functional, compact-open-approximation, regularity-reconstruction
- Abstraction concepts: compactly-supported-continuous-functions measure-functional interface in compactly-supported-continuous-functions, compactly-supported-continuous-functions regular-Borel envelope in compactly-supported-continuous-functions, compact-open-approximation + positivity-to-sigma-additivity + topological-regularity-reconstruction evasive representation for compactly-supported-continuous-functions, compact-open-approximation + topological-regularity-reconstruction evasive representation for compactly-supported-continuous-functions, positive-functional-implies-regular-measure measure-functional interface in compactly-supported-continuous-functions, positive-functional-implies-regular-measure regular-Borel envelope in compactly-supported-continuous-functions
- Definitional focus: realizes antecedent schema `positive-linear-functional-on-cc-space`, forces target consequence `regular-borel-measure-representation`, realizes antecedent schema `locally-compact-hausdorff-definition`
- Counterfactual focus: Remove `realizes antecedent schema `positive-linear-functional-on-cc-space`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `positive-linear-functional-on-cc-space`, preserves `regular-Borel representation in compactly-supported-continuous-functions`, provides an explicit transfer law or reduction mechanism, forces target consequence `regular-borel-measure-representation`, Remove `realizes antecedent schema `locally-compact-hausdorff-definition`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `locally-compact-hausdorff-definition`, preserves `regular-Borel representation in compactly-supported-continuous-functions`, provides an explicit transfer law or reduction mechanism, forces target consequence `regular-borel-measure-representation`
- Bridges: bridge.002, bridge.003, bridge.005
- Hypotheses: phyp.riesz-markov-kakutani-representation-theorem.021, phyp.riesz-markov-kakutani-representation-theorem.002, phyp.riesz-markov-kakutani-representation-theorem.003, phyp.riesz-markov-kakutani-representation-theorem.032
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.3613, coherence_avg=0.0072
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.thm.riesz-markov-kakutani and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.002 - Cross-Model Strategy around st.def.lch-space
- Anchor: st.def.lch-space
- Phase: Foundational Gauge-Theoretic Definitions
- Score: 0.653
- Concept fertility: 0.8345
- Anchor concepts: locally-compact-hausdorff-definition, cc-space-definition, compactly-supported-continuous-functions, locally-compact-Hausdorff-space, C_c-space
- Bridge concepts: compactly-supported-continuous-functions, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, compact-open-approximation, regularity-reconstruction, topological-regularity, measure-representation, regular-Borel-measure
- Abstraction concepts: compactly-supported-continuous-functions measure-functional interface in compactly-supported-continuous-functions, compactly-supported-continuous-functions regular-Borel envelope in compactly-supported-continuous-functions, compact-open-approximation + topological-regularity-reconstruction evasive representation for compactly-supported-continuous-functions
- Definitional focus: realizes antecedent schema `locally-compact-hausdorff-definition`, forces target consequence `regular-borel-measure-representation`
- Counterfactual focus: Remove `realizes antecedent schema `locally-compact-hausdorff-definition`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `locally-compact-hausdorff-definition`, preserves `regular-Borel representation in compactly-supported-continuous-functions`, provides an explicit transfer law or reduction mechanism, forces target consequence `regular-borel-measure-representation`
- Bridges: bridge.003, bridge.004, bridge.008
- Hypotheses: phyp.riesz-markov-kakutani-representation-theorem.028, phyp.riesz-markov-kakutani-representation-theorem.003, phyp.riesz-markov-kakutani-representation-theorem.033, phyp.riesz-markov-kakutani-representation-theorem.004
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.55, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.4002, coherence_avg=0.0021
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.lch-space and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.003 - Cross-Model Strategy around st.lem.compact-open-approximation
- Anchor: st.lem.compact-open-approximation
- Phase: Additional KB-Specific Phases
- Score: 0.6178
- Concept fertility: 0.7985
- Anchor concepts: compact-open-approximation-supports-regularity, compact-open-approximation-on-lch-space, compact-open-regularity-witness, locally-compact-hausdorff-definition, compact-open-approximation-lemma
- Bridge concepts: compactly-supported-continuous-functions, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, compact-open-approximation, regularity-reconstruction, topological-regularity, cc-space-definition, C_c-space
- Abstraction concepts: barrier + compact-open-approximation + positivity-to-sigma-additivity evasive representation for compactly-supported-continuous-functions, compactly-supported-continuous-functions measure-functional interface in compactly-supported-continuous-functions, compactly-supported-continuous-functions regular-Borel envelope in compactly-supported-continuous-functions
- Definitional focus: realizes antecedent schema `positive-linear-functional-on-cc-space`, forces target consequence `compact-open-regularity-witness`
- Counterfactual focus: Remove `realizes antecedent schema `positive-linear-functional-on-cc-space`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `positive-linear-functional-on-cc-space`, preserves `compact-open regularity control in compactly-supported-continuous-functions`, provides an explicit transfer law or reduction mechanism, forces target consequence `compact-open-regularity-witness`
- Bridges: bridge.008, bridge.012, bridge.017
- Hypotheses: phyp.riesz-markov-kakutani-representation-theorem.027, phyp.riesz-markov-kakutani-representation-theorem.008, phyp.riesz-markov-kakutani-representation-theorem.012, phyp.riesz-markov-kakutani-representation-theorem.017
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.6, barrier_evasion=0.6, lemma_generation=0.0, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.4349, coherence_avg=0.0071
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.lem.compact-open-approximation and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.004 - Cross-Model Strategy around st.thm.positive-functional-implies-measure
- Anchor: st.thm.positive-functional-implies-measure
- Phase: Current Bridge Agenda
- Score: 0.6099
- Concept fertility: 0.8949
- Anchor concepts: positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, regular-borel-measure-definition, positive-functional-definition, cc-space-definition
- Bridge concepts: compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positivity-to-sigma-additivity, positive-functional-definition, positive-linear-functional, compact-open-approximation, regularity-reconstruction, measure-representation
- Abstraction concepts: compactly-supported-continuous-functions measure-functional interface in compactly-supported-continuous-functions, compactly-supported-continuous-functions regular-Borel envelope in compactly-supported-continuous-functions, barrier + compact-open-approximation + positivity-to-sigma-additivity evasive representation for compactly-supported-continuous-functions, barrier + positivity-to-sigma-additivity + topological-regularity-reconstruction evasive representation for compactly-supported-continuous-functions, compactly-supported-continuous-functions OS reconstruction interface
- Definitional focus: realizes antecedent schema `positive-linear-functional-on-cc-space`, forces target consequence `positive-linear-functional-on-cc-space`
- Counterfactual focus: Remove `realizes antecedent schema `positive-linear-functional-on-cc-space`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `positive-linear-functional-on-cc-space`, preserves `compact-open regularity control in compactly-supported-continuous-functions`, provides an explicit transfer law or reduction mechanism, forces target consequence `positive-linear-functional-on-cc-space`, Assume the first sufficient attribute set is fully realized: realizes antecedent schema `positive-linear-functional-on-cc-space`, preserves `regular-Borel representation in compactly-supported-continuous-functions`, forces target consequence `positive-linear-functional-on-cc-space`
- Bridges: bridge.001, bridge.004, bridge.006
- Hypotheses: phyp.riesz-markov-kakutani-representation-theorem.024, phyp.riesz-markov-kakutani-representation-theorem.001, phyp.riesz-markov-kakutani-representation-theorem.031, phyp.riesz-markov-kakutani-representation-theorem.004
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=1.0, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.3743, coherence_avg=0.0071
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.thm.positive-functional-implies-measure and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.005 - Cross-Model Strategy around st.def.cc-space
- Anchor: st.def.cc-space
- Phase: Current Bridge Agenda
- Score: 0.5948
- Concept fertility: 0.8719
- Anchor concepts: positive-linear-functional-on-cc-space, locally-compact-hausdorff-definition, positive-functional-definition, cc-space-definition, compactly-supported-continuous-functions
- Bridge concepts: compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positivity-to-sigma-additivity, positive-functional-definition, positive-linear-functional, compact-open-approximation, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space
- Abstraction concepts: compactly-supported-continuous-functions measure-functional interface in compactly-supported-continuous-functions, compactly-supported-continuous-functions regular-Borel envelope in compactly-supported-continuous-functions, barrier + compact-open-approximation + positivity-to-sigma-additivity evasive representation for compactly-supported-continuous-functions, compact-open-approximation + positivity-to-sigma-additivity + topological-regularity-reconstruction evasive representation for compactly-supported-continuous-functions
- Definitional focus: realizes antecedent schema `positive-linear-functional-on-cc-space`, forces target consequence `positive-linear-functional-on-cc-space`, forces target consequence `regular-borel-measure-representation`
- Counterfactual focus: Remove `realizes antecedent schema `positive-linear-functional-on-cc-space`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `positive-linear-functional-on-cc-space`, preserves `compact-open regularity control in compactly-supported-continuous-functions`, provides an explicit transfer law or reduction mechanism, forces target consequence `positive-linear-functional-on-cc-space`, Assume the first sufficient attribute set is fully realized: realizes antecedent schema `positive-linear-functional-on-cc-space`, preserves `regular-Borel representation in compactly-supported-continuous-functions`, provides an explicit transfer law or reduction mechanism, forces target consequence `regular-borel-measure-representation`
- Bridges: bridge.001, bridge.002, bridge.009
- Hypotheses: phyp.riesz-markov-kakutani-representation-theorem.023, phyp.riesz-markov-kakutani-representation-theorem.001, phyp.riesz-markov-kakutani-representation-theorem.031, phyp.riesz-markov-kakutani-representation-theorem.002
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.3942, coherence_avg=0.0071
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.cc-space and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.006 - Cross-Model Strategy around st.lem.uniqueness-from-cc-separation
- Anchor: st.lem.uniqueness-from-cc-separation
- Phase: Current Bridge Agenda
- Score: 0.575
- Concept fertility: 0.8329
- Anchor concepts: function-separation-implies-measure-uniqueness, compact-open-approximation-on-lch-space, regular-borel-measure-on-lch-space, unique-representing-measure, uniqueness-from-cc-separation
- Bridge concepts: compactly-supported-continuous-functions, topological-regularity-reconstruction, regular-borel-measure-on-lch-space, regular-borel-measure-definition, unique-representing-measure, regular-Borel-measure-model, compact-open-approximation, measure-representation
- Abstraction concepts: barrier + compact-open-approximation + topological-regularity-reconstruction evasive representation for uniqueness-from-cc-separation, uniqueness-from-cc-separation measure-functional interface in compactly-supported-continuous-functions, uniqueness-from-cc-separation OS reconstruction interface
- Definitional focus: realizes antecedent schema `compact-open-approximation-on-lch-space`, forces target consequence `regular-borel-measure-representation`
- Counterfactual focus: Remove `realizes antecedent schema `compact-open-approximation-on-lch-space`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `compact-open-approximation-on-lch-space`, preserves `regular-Borel representation in compactly-supported-continuous-functions`, provides an explicit transfer law or reduction mechanism, forces target consequence `regular-borel-measure-representation`
- Bridges: bridge.011, bridge.014
- Hypotheses: phyp.riesz-markov-kakutani-representation-theorem.025, phyp.riesz-markov-kakutani-representation-theorem.011, phyp.riesz-markov-kakutani-representation-theorem.014, phyp.riesz-markov-kakutani-representation-theorem.041
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.5, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.4052, coherence_avg=0.0055
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.lem.uniqueness-from-cc-separation and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

## Novelty-Maximizing Prompt

```text
You are a proof-strategy synthesizer optimizing novelty under rigor constraints.
Inputs: KB slice, ranked strategies, bridge programs, hypothesis sets, coherence diagnostics.
Objective: maximize expected proof progress while maximizing conceptual novelty.
Novelty score N = 0.38*phase_diversity + 0.28*bridge_originality + 0.20*hypothesis_nonredundancy + 0.14*minimal_assumption_gain.
Live diagnostics:
- global_coherence=0.6389
- tension=0.1407
- coherence_negative_hypotheses=1
- risk_mode=off
- top_abstraction_conjectures=conj.004:measure-functional-interface:positive-functional-implies-regular-measure measure-functional interface in compactly-supported-continuous-functions; conj.005:regular-borel-envelope:positive-functional-implies-regular-measure regular-Borel envelope in compactly-supported-continuous-functions; conj.007:measure-functional-interface:compactly-supported-continuous-functions measure-functional interface in compactly-supported-continuous-functions
- top_definitional_requirements=conj.004:realizes antecedent schema `positive-linear-functional-on-cc-space`, forces target consequence `regular-borel-measure-representation`; conj.005:realizes antecedent schema `positive-linear-functional-on-cc-space`, forces target consequence `regular-borel-measure-representation`; conj.007:realizes antecedent schema `positive-linear-functional-on-cc-space`, forces target consequence `regular-borel-measure-representation`
- top_counterfactual_probes=conj.004:Remove `realizes antecedent schema `positive-linear-functional-on-cc-space`` from the candidate abstraction.; conj.005:Remove `realizes antecedent schema `positive-linear-functional-on-cc-space`` from the candidate abstraction.; conj.007:Remove `realizes antecedent schema `positive-linear-functional-on-cc-space`` from the candidate abstraction.
Top strategies:
1. strat.001 | anchor=st.thm.riesz-markov-kakutani | phase=Current Bridge Agenda | score=0.7509 | fertility=0.8686
2. strat.002 | anchor=st.def.lch-space | phase=Foundational Gauge-Theoretic Definitions | score=0.653 | fertility=0.8345
3. strat.003 | anchor=st.lem.compact-open-approximation | phase=Additional KB-Specific Phases | score=0.6178 | fertility=0.7985
Hard constraints:
1. Every proposed step must reference statement IDs.
2. Each round must include at least one bridge from a phase different from the previous round.
3. Reject moves that only restate existing dependencies without adding new conditional entailment paths.
4. Prefer smallest hypothesis sets that unlock the largest new consequence set.
5. If risk_mode=on, reject any move whose expected coherence impact is negative.
6. Every selected move must state which necessary abstraction attribute it is instantiating.
7. Every selected move must include one counterfactual probe that could falsify the bridge concept.
Procedure:
- Start from strategy 1; generate 3 candidate proof moves (anchor + bridge + hypothesis).
- Score each move by (validity risk, novelty gain, expected entailment gain, coherence impact, definitional adequacy, counterfactual informativeness).
- Keep one move, archive two alternatives, then rotate to another phase for next round.
Output format:
### Chosen Strategy
### Candidate Moves (3)
### Scores
### Definitional Attribute Used
### Counterfactual Probe
### Selected Move and Rationale
### Next-Round Phase Constraint
```
