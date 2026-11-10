# Proof Strategy Portfolio

## Stats

- Strategies: 6
- Pathways used: 8
- Bridges used: 20
- Conjectured abstractions used: 36
- Hypotheses used: 34
- Coherence signals used: 34

## Strategies

| strategy_id | name | phase | anchor | score | fertility | anchor_concepts |
|---|---|---|---|---|---|---|
| strat.001 | Cross-Model Strategy around st.thm.positive-functional-implies-measure | Current Bridge Agenda | st.thm.positive-functional-implies-measure | 0.7409 | 0.8947 | regular-measure-implies-positive-functional, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, positive-functional-via-integration |
| strat.002 | Cross-Model Strategy around st.def.lch-space | Foundational Gauge-Theoretic Definitions | st.def.lch-space | 0.6545 | 0.8592 | locally-compact-hausdorff-definition, cc-space-definition, compactly-supported-continuous-functions, locally-compact-Hausdorff-space |
| strat.003 | Cross-Model Strategy around st.def.cc-space | Current Bridge Agenda | st.def.cc-space | 0.6086 | 0.8716 | positive-linear-functional-on-cc-space, locally-compact-hausdorff-definition, positive-functional-definition, cc-space-definition |
| strat.004 | Cross-Model Strategy around st.thm.riesz-markov-kakutani | Current Bridge Agenda | st.thm.riesz-markov-kakutani | 0.604 | 0.8684 | regular-measure-implies-positive-functional, positive-functional-implies-regular-measure, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space |
| strat.005 | Cross-Model Strategy around st.lem.uniqueness-from-cc-separation | Current Bridge Agenda | st.lem.uniqueness-from-cc-separation | 0.5689 | 0.8935 | regular-measure-implies-positive-functional, regular-borel-measure-on-lch-space, positive-functional-via-integration, integration-defines-positive-functional |
| strat.006 | Cross-Model Strategy around st.prop.integration-defines-functional | Current Bridge Agenda | st.prop.integration-defines-functional | 0.5642 | 0.8548 | regular-measure-implies-positive-functional, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, positive-functional-via-integration |

### strat.001 - Cross-Model Strategy around st.thm.positive-functional-implies-measure
- Anchor: st.thm.positive-functional-implies-measure
- Phase: Current Bridge Agenda
- Score: 0.7409
- Concept fertility: 0.8947
- Anchor concepts: regular-measure-implies-positive-functional, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, positive-functional-via-integration, integration-defines-positive-functional
- Bridge concepts: compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positivity-to-sigma-additivity, positive-functional-definition, positive-linear-functional, compact-open-approximation, regular-measure-implies-positive-functional, integration-defines-positive-functional
- Abstraction concepts: compactly-supported-continuous-functions measure-functional interface in compactly-supported-continuous-functions, compactly-supported-continuous-functions regular-Borel envelope in compactly-supported-continuous-functions, compactly-supported-continuous-functions signed-measure normal form in compactly-supported-continuous-functions, barrier + compact-open-approximation + positivity-to-sigma-additivity evasive representation for regular-measure-implies-positive-functional, regular-measure-implies-positive-functional measure-functional interface in compactly-supported-continuous-functions, regular-measure-implies-positive-functional regular-Borel envelope in compactly-supported-continuous-functions
- Definitional focus: realizes antecedent schema `positive-linear-functional-on-cc-space`, forces target consequence `positive-linear-functional-on-cc-space`, realizes antecedent schema `regular-borel-measure-on-lch-space`, realizes antecedent schema `locally-compact-hausdorff-definition`
- Counterfactual focus: Remove `realizes antecedent schema `positive-linear-functional-on-cc-space`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `positive-linear-functional-on-cc-space`, preserves `compact-open regularity control in compactly-supported-continuous-functions`, provides an explicit transfer law or reduction mechanism, forces target consequence `positive-linear-functional-on-cc-space`, Remove `realizes antecedent schema `regular-borel-measure-on-lch-space`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `regular-borel-measure-on-lch-space`, preserves `compact-open regularity control in compactly-supported-continuous-functions`, forces target consequence `positive-linear-functional-on-cc-space`
- Bridges: bridge.001, bridge.004, bridge.005
- Hypotheses: phyp.riesz-markov-kakutani-representation-theorem.018, phyp.riesz-markov-kakutani-representation-theorem.001, phyp.riesz-markov-kakutani-representation-theorem.027, phyp.riesz-markov-kakutani-representation-theorem.004
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=1.0, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.3709, coherence_avg=0.008
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.thm.positive-functional-implies-measure and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.002 - Cross-Model Strategy around st.def.lch-space
- Anchor: st.def.lch-space
- Phase: Foundational Gauge-Theoretic Definitions
- Score: 0.6545
- Concept fertility: 0.8592
- Anchor concepts: locally-compact-hausdorff-definition, cc-space-definition, compactly-supported-continuous-functions, locally-compact-Hausdorff-space, C_c-space
- Bridge concepts: compactly-supported-continuous-functions, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, compact-open-approximation, regularity-reconstruction, topological-regularity, measure-representation, regular-Borel-measure
- Abstraction concepts: compactly-supported-continuous-functions measure-functional interface in compactly-supported-continuous-functions, compactly-supported-continuous-functions regular-Borel envelope in compactly-supported-continuous-functions, compactly-supported-continuous-functions signed-measure normal form in compactly-supported-continuous-functions, barrier + compact-open-approximation evasive representation for compactly-supported-continuous-functions
- Definitional focus: realizes antecedent schema `locally-compact-hausdorff-definition`, forces target consequence `regular-borel-measure-representation`, forces target consequence `positive-linear-functional-on-cc-space`, forces target consequence `locally-compact-hausdorff-definition`
- Counterfactual focus: Remove `realizes antecedent schema `locally-compact-hausdorff-definition`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `locally-compact-hausdorff-definition`, preserves `regular-Borel representation in compactly-supported-continuous-functions`, provides an explicit transfer law or reduction mechanism, forces target consequence `regular-borel-measure-representation`, Assume the first sufficient attribute set is fully realized: realizes antecedent schema `locally-compact-hausdorff-definition`, preserves `compact-open regularity control in compactly-supported-continuous-functions`, provides an explicit transfer law or reduction mechanism, forces target consequence `positive-linear-functional-on-cc-space`, Assume the first sufficient attribute set is fully realized: realizes antecedent schema `locally-compact-hausdorff-definition`, preserves `compact-open regularity control in compactly-supported-continuous-functions`, provides an explicit transfer law or reduction mechanism, forces target consequence `locally-compact-hausdorff-definition`
- Bridges: bridge.003, bridge.005, bridge.007
- Hypotheses: phyp.riesz-markov-kakutani-representation-theorem.023, phyp.riesz-markov-kakutani-representation-theorem.003, phyp.riesz-markov-kakutani-representation-theorem.029, phyp.riesz-markov-kakutani-representation-theorem.005
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.55, lemma_generation=0.25, abstraction_leverage=1.0, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.3965, coherence_avg=0.0029
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.lch-space and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.003 - Cross-Model Strategy around st.def.cc-space
- Anchor: st.def.cc-space
- Phase: Current Bridge Agenda
- Score: 0.6086
- Concept fertility: 0.8716
- Anchor concepts: positive-linear-functional-on-cc-space, locally-compact-hausdorff-definition, positive-functional-definition, cc-space-definition, compactly-supported-continuous-functions
- Bridge concepts: compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, positivity-to-sigma-additivity, positive-functional-definition, positive-linear-functional, compact-open-approximation, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space
- Abstraction concepts: compactly-supported-continuous-functions measure-functional interface in compactly-supported-continuous-functions, compactly-supported-continuous-functions regular-Borel envelope in compactly-supported-continuous-functions, compactly-supported-continuous-functions signed-measure normal form in compactly-supported-continuous-functions
- Definitional focus: realizes antecedent schema `positive-linear-functional-on-cc-space`, forces target consequence `positive-linear-functional-on-cc-space`, forces target consequence `regular-borel-measure-representation`
- Counterfactual focus: Remove `realizes antecedent schema `positive-linear-functional-on-cc-space`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `positive-linear-functional-on-cc-space`, preserves `compact-open regularity control in compactly-supported-continuous-functions`, provides an explicit transfer law or reduction mechanism, forces target consequence `positive-linear-functional-on-cc-space`, Assume the first sufficient attribute set is fully realized: realizes antecedent schema `positive-linear-functional-on-cc-space`, preserves `regular-Borel representation in compactly-supported-continuous-functions`, provides an explicit transfer law or reduction mechanism, forces target consequence `regular-borel-measure-representation`
- Bridges: bridge.001, bridge.002, bridge.011
- Hypotheses: phyp.riesz-markov-kakutani-representation-theorem.021, phyp.riesz-markov-kakutani-representation-theorem.001, phyp.riesz-markov-kakutani-representation-theorem.002, phyp.riesz-markov-kakutani-representation-theorem.027
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.3897, coherence_avg=0.008
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.cc-space and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.004 - Cross-Model Strategy around st.thm.riesz-markov-kakutani
- Anchor: st.thm.riesz-markov-kakutani
- Phase: Current Bridge Agenda
- Score: 0.604
- Concept fertility: 0.8684
- Anchor concepts: regular-measure-implies-positive-functional, positive-functional-implies-regular-measure, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, regular-borel-measure-representation
- Bridge concepts: compactly-supported-continuous-functions, positive-linear-functional-on-cc-space, locally-compact-hausdorff-definition, locally-compact-Hausdorff-space, positive-functional-definition, positive-linear-functional, compact-open-approximation, regularity-reconstruction
- Abstraction concepts: compactly-supported-continuous-functions measure-functional interface in compactly-supported-continuous-functions, compactly-supported-continuous-functions regular-Borel envelope in compactly-supported-continuous-functions, compactly-supported-continuous-functions signed-measure normal form in compactly-supported-continuous-functions, regular-measure-implies-positive-functional measure-functional interface in compactly-supported-continuous-functions, regular-measure-implies-positive-functional regular-Borel envelope in compactly-supported-continuous-functions
- Definitional focus: realizes antecedent schema `positive-linear-functional-on-cc-space`, forces target consequence `regular-borel-measure-representation`, realizes antecedent schema `locally-compact-hausdorff-definition`
- Counterfactual focus: Remove `realizes antecedent schema `positive-linear-functional-on-cc-space`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `positive-linear-functional-on-cc-space`, preserves `regular-Borel representation in compactly-supported-continuous-functions`, provides an explicit transfer law or reduction mechanism, forces target consequence `regular-borel-measure-representation`, Remove `realizes antecedent schema `locally-compact-hausdorff-definition`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `locally-compact-hausdorff-definition`, preserves `regular-Borel representation in compactly-supported-continuous-functions`, provides an explicit transfer law or reduction mechanism, forces target consequence `regular-borel-measure-representation`
- Bridges: bridge.002, bridge.003, bridge.009
- Hypotheses: phyp.riesz-markov-kakutani-representation-theorem.017, phyp.riesz-markov-kakutani-representation-theorem.002, phyp.riesz-markov-kakutani-representation-theorem.003, phyp.riesz-markov-kakutani-representation-theorem.028
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.3577, coherence_avg=0.008
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.thm.riesz-markov-kakutani and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.005 - Cross-Model Strategy around st.lem.uniqueness-from-cc-separation
- Anchor: st.lem.uniqueness-from-cc-separation
- Phase: Current Bridge Agenda
- Score: 0.5689
- Concept fertility: 0.8935
- Anchor concepts: regular-measure-implies-positive-functional, regular-borel-measure-on-lch-space, positive-functional-via-integration, integration-defines-positive-functional, regular-borel-measure-definition
- Bridge concepts: regular-measure-implies-positive-functional, compactly-supported-continuous-functions, integration-defines-positive-functional, topological-regularity-reconstruction, positive-functional-via-integration, regular-borel-measure-on-lch-space, compact-open-approximation, regularity-reconstruction
- Abstraction concepts: barrier + compact-open-approximation + positivity-to-sigma-additivity evasive representation for regular-measure-implies-positive-functional, regular-measure-implies-positive-functional measure-functional interface in compactly-supported-continuous-functions, regular-measure-implies-positive-functional regular-Borel envelope in compactly-supported-continuous-functions, regular-measure-implies-positive-functional signed-measure normal form in compactly-supported-continuous-functions
- Definitional focus: realizes antecedent schema `regular-borel-measure-on-lch-space`, forces target consequence `positive-linear-functional-on-cc-space`, forces target consequence `regular-borel-measure-representation`
- Counterfactual focus: Remove `realizes antecedent schema `regular-borel-measure-on-lch-space`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `regular-borel-measure-on-lch-space`, preserves `compact-open regularity control in compactly-supported-continuous-functions`, forces target consequence `positive-linear-functional-on-cc-space`, Assume the first sufficient attribute set is fully realized: realizes antecedent schema `regular-borel-measure-on-lch-space`, preserves `regular-Borel representation in compactly-supported-continuous-functions`, provides an explicit transfer law or reduction mechanism, forces target consequence `regular-borel-measure-representation`
- Bridges: bridge.004, bridge.013, bridge.016
- Hypotheses: phyp.riesz-markov-kakutani-representation-theorem.020, phyp.riesz-markov-kakutani-representation-theorem.004, phyp.riesz-markov-kakutani-representation-theorem.030, phyp.riesz-markov-kakutani-representation-theorem.013
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=1.0, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.3612, coherence_avg=0.0063
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.lem.uniqueness-from-cc-separation and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.006 - Cross-Model Strategy around st.prop.integration-defines-functional
- Anchor: st.prop.integration-defines-functional
- Phase: Current Bridge Agenda
- Score: 0.5642
- Concept fertility: 0.8548
- Anchor concepts: regular-measure-implies-positive-functional, positive-linear-functional-on-cc-space, regular-borel-measure-on-lch-space, positive-functional-via-integration, integration-defines-positive-functional
- Bridge concepts: regular-measure-implies-positive-functional, compactly-supported-continuous-functions, integration-defines-positive-functional, positive-linear-functional-on-cc-space, topological-regularity-reconstruction, positive-functional-via-integration
- Abstraction concepts: barrier + positivity-to-sigma-additivity + topological-regularity-reconstruction evasive representation for regular-measure-implies-positive-functional, regular-measure-implies-positive-functional measure-functional interface in compactly-supported-continuous-functions, regular-measure-implies-positive-functional regular-Borel envelope in compactly-supported-continuous-functions, regular-measure-implies-positive-functional signed-measure normal form in compactly-supported-continuous-functions
- Definitional focus: realizes antecedent schema `positive-linear-functional-on-cc-space`, forces target consequence `positive-linear-functional-on-cc-space`, forces target consequence `regular-borel-measure-representation`
- Counterfactual focus: Remove `realizes antecedent schema `positive-linear-functional-on-cc-space`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `positive-linear-functional-on-cc-space`, preserves `compact-open regularity control in compactly-supported-continuous-functions`, forces target consequence `positive-linear-functional-on-cc-space`, Assume the first sufficient attribute set is fully realized: realizes antecedent schema `positive-linear-functional-on-cc-space`, preserves `regular-Borel representation in compactly-supported-continuous-functions`, provides an explicit transfer law or reduction mechanism, forces target consequence `regular-borel-measure-representation`
- Bridges: bridge.006, bridge.014
- Hypotheses: phyp.riesz-markov-kakutani-representation-theorem.019, phyp.riesz-markov-kakutani-representation-theorem.006, phyp.riesz-markov-kakutani-representation-theorem.032, phyp.riesz-markov-kakutani-representation-theorem.014
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.5, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=1.0, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.3722, coherence_avg=0.0079
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.prop.integration-defines-functional and restate objective as conditional entailment gain.
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
- global_coherence=0.6434
- tension=0.1465
- coherence_negative_hypotheses=1
- risk_mode=off
- top_abstraction_conjectures=conj.004:barrier-escaping-representation:barrier + compact-open-approximation + positivity-to-sigma-additivity evasive representation for regular-measure-implies-positive-functional; conj.005:measure-functional-interface:regular-measure-implies-positive-functional measure-functional interface in compactly-supported-continuous-functions; conj.006:regular-borel-envelope:regular-measure-implies-positive-functional regular-Borel envelope in compactly-supported-continuous-functions
- top_definitional_requirements=conj.004:realizes antecedent schema `regular-borel-measure-on-lch-space`, forces target consequence `positive-linear-functional-on-cc-space`; conj.005:realizes antecedent schema `regular-borel-measure-on-lch-space`, forces target consequence `positive-linear-functional-on-cc-space`; conj.006:realizes antecedent schema `regular-borel-measure-on-lch-space`, forces target consequence `positive-linear-functional-on-cc-space`
- top_counterfactual_probes=conj.004:Remove `realizes antecedent schema `regular-borel-measure-on-lch-space`` from the candidate abstraction.; conj.005:Remove `realizes antecedent schema `regular-borel-measure-on-lch-space`` from the candidate abstraction.; conj.006:Remove `realizes antecedent schema `regular-borel-measure-on-lch-space`` from the candidate abstraction.
Top strategies:
1. strat.001 | anchor=st.thm.positive-functional-implies-measure | phase=Current Bridge Agenda | score=0.7409 | fertility=0.8947
2. strat.002 | anchor=st.def.lch-space | phase=Foundational Gauge-Theoretic Definitions | score=0.6545 | fertility=0.8592
3. strat.003 | anchor=st.def.cc-space | phase=Current Bridge Agenda | score=0.6086 | fertility=0.8716
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
