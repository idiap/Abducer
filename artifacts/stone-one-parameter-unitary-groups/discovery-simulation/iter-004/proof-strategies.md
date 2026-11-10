# Proof Strategy Portfolio

## Stats

- Strategies: 6
- Pathways used: 8
- Bridges used: 20
- Conjectured abstractions used: 36
- Hypotheses used: 58
- Coherence signals used: 58

## Strategies

| strategy_id | name | phase | anchor | score | fertility | anchor_concepts |
|---|---|---|---|---|---|---|
| strat.001 | Cross-Model Strategy around st.thm.stone-correspondence | Current Bridge Agenda | st.thm.stone-correspondence | 0.7478 | 0.8766 | unitary-group-implies-unique-self-adjoint-generator, unitary-group-implies-self-adjoint-generator, self-adjoint-operator-implies-unitary-group, spectral-theorem-enables-unitary-functional-calculus |
| strat.002 | Cross-Model Strategy around st.def.unitary-group | Foundational Gauge-Theoretic Definitions | st.def.unitary-group | 0.6375 | 0.8368 | strongly-continuous-unitary-group, unitary-group-definition, operator-theoretic-Hilbert-space, Hilbert-space |
| strat.003 | Cross-Model Strategy around st.thm.self-adjoint-implies-unitary-group | Current Bridge Agenda | st.thm.self-adjoint-implies-unitary-group | 0.6255 | 0.8774 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group |
| strat.004 | Cross-Model Strategy around st.def.self-adjoint-operator | Current Bridge Agenda | st.def.self-adjoint-operator | 0.5848 | 0.879 | self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group, stone-self-adjoint-correspondence |
| strat.005 | Cross-Model Strategy around st.thm.unitary-group-implies-self-adjoint-generator | Current Bridge Agenda | st.thm.unitary-group-implies-self-adjoint-generator | 0.5584 | 0.7976 | spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero |
| strat.006 | Cross-Model Strategy around st.prop.generator-domain-regularity | Current Bridge Agenda | st.prop.generator-domain-regularity | 0.5481 | 0.7957 | c0-generation-implies-closed-dense-generator, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group, generator-of-c0-semigroup |

### strat.001 - Cross-Model Strategy around st.thm.stone-correspondence
- Anchor: st.thm.stone-correspondence
- Phase: Current Bridge Agenda
- Score: 0.7478
- Concept fertility: 0.8766
- Anchor concepts: unitary-group-implies-unique-self-adjoint-generator, unitary-group-implies-self-adjoint-generator, self-adjoint-operator-implies-unitary-group, spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus
- Bridge concepts: unbounded-generator-graph, spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-generator-characterization, self-adjoint-operator-on-hilbert-space, unitary-group-via-functional-calculus, strongly-continuous-unitary-group, unitary-group-definition
- Abstraction concepts: barrier + orbit-differentiability-control + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-enables-unitary-functional-calculus self-adjoint generator core, spectral-theorem-enables-unitary-functional-calculus functional-calculus normal form in self-adjoint-spectral-calculus, spectral-theorem-and-functional-calculus self-adjoint generator core, spectral-calculus-interface evasive representation for spectral-theorem-and-functional-calculus, spectral-theorem-and-functional-calculus functional-calculus normal form in operator-theoretic-Hilbert-space, spectral-calculus-interface + unbounded-operator-domain-control evasive representation for spectral-theorem-and-functional-calculus
- Definitional focus: realizes antecedent schema `spectral-theorem-and-functional-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`, realizes antecedent schema `strongly-continuous-unitary-group`, realizes antecedent schema `self-adjoint-operator-on-hilbert-space`
- Counterfactual focus: Remove `realizes antecedent schema `spectral-theorem-and-functional-calculus`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `spectral-theorem-and-functional-calculus`, preserves `self-adjoint generator recovery in unbounded-generator-graph`, forces target consequence `self-adjoint-operator-on-hilbert-space`, Remove `realizes antecedent schema `strongly-continuous-unitary-group`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `strongly-continuous-unitary-group`, preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`
- Bridges: bridge.004, bridge.006, bridge.008
- Hypotheses: phyp.stone-one-parameter-unitary-groups.031, phyp.stone-one-parameter-unitary-groups.004, phyp.stone-one-parameter-unitary-groups.006, phyp.stone-one-parameter-unitary-groups.044
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.4425, coherence_avg=0.0058
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.thm.stone-correspondence and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.002 - Cross-Model Strategy around st.def.unitary-group
- Anchor: st.def.unitary-group
- Phase: Foundational Gauge-Theoretic Definitions
- Score: 0.6375
- Concept fertility: 0.8368
- Anchor concepts: strongly-continuous-unitary-group, unitary-group-definition, operator-theoretic-Hilbert-space, Hilbert-space, Stone-correspondence
- Bridge concepts: strongly-continuous-unitary-group, unitary-group-definition, unitary-group-analysis, stone-correspondence, Stone-correspondence, unitary-group
- Abstraction concepts: spectral-theorem-and-functional-calculus self-adjoint generator core, barrier + orbit-differentiability-control + unbounded-operator-domain-control evasive representation for spectral-theorem-and-functional-calculus, spectral-theorem-and-functional-calculus functional-calculus normal form in operator-theoretic-Hilbert-space, spectral-calculus-interface evasive representation for spectral-theorem-and-functional-calculus
- Definitional focus: realizes antecedent schema `strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`
- Counterfactual focus: Remove `realizes antecedent schema `strongly-continuous-unitary-group`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `strongly-continuous-unitary-group`, preserves `unitary orbit infinitesimal control in strongly-continuous-unitary-group`, forces target consequence `self-adjoint-operator-on-hilbert-space`
- Bridges: bridge.002, bridge.005, bridge.006
- Hypotheses: phyp.stone-one-parameter-unitary-groups.038, phyp.stone-one-parameter-unitary-groups.002, phyp.stone-one-parameter-unitary-groups.005, phyp.stone-one-parameter-unitary-groups.042
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.55, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.4227, coherence_avg=0.0022
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.unitary-group and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.003 - Cross-Model Strategy around st.thm.self-adjoint-implies-unitary-group
- Anchor: st.thm.self-adjoint-implies-unitary-group
- Phase: Current Bridge Agenda
- Score: 0.6255
- Concept fertility: 0.8774
- Anchor concepts: spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group, unitary-group-via-functional-calculus
- Bridge concepts: self-adjoint-operator-on-hilbert-space, stone-unitary-group-correspondence, strongly-continuous-unitary-group, stone-self-adjoint-correspondence, self-adjoint-operator-definition, self-adjoint-spectral-calculus, unitary-group-definition, unitary-group-analysis
- Abstraction concepts: spectral-theorem-and-functional-calculus self-adjoint generator core, barrier + spectral-calculus-interface + unbounded-operator-domain-control evasive representation for spectral-theorem-and-functional-calculus, spectral-theorem-and-functional-calculus functional-calculus normal form in operator-theoretic-Banach-space, barrier + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-enables-unitary-functional-calculus functional-calculus normal form in Yosida-approximation-scheme, spectral-theorem-enables-unitary-functional-calculus self-adjoint generator core
- Definitional focus: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, forces target consequence `self-adjoint-operator-on-hilbert-space`, realizes antecedent schema `spectral-theorem-and-functional-calculus`
- Counterfactual focus: Remove `realizes antecedent schema `self-adjoint-operator-on-hilbert-space`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`, Remove `realizes antecedent schema `spectral-theorem-and-functional-calculus`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `spectral-theorem-and-functional-calculus`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`
- Bridges: bridge.001, bridge.002, bridge.007
- Hypotheses: phyp.stone-one-parameter-unitary-groups.033, phyp.stone-one-parameter-unitary-groups.001, phyp.stone-one-parameter-unitary-groups.002, phyp.stone-one-parameter-unitary-groups.041
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.4484, coherence_avg=0.0073
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.thm.self-adjoint-implies-unitary-group and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.004 - Cross-Model Strategy around st.def.self-adjoint-operator
- Anchor: st.def.self-adjoint-operator
- Phase: Current Bridge Agenda
- Score: 0.5848
- Concept fertility: 0.879
- Anchor concepts: self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group, stone-self-adjoint-correspondence, symmetric-generator
- Bridge concepts: self-adjoint-operator-on-hilbert-space, stone-unitary-group-correspondence, strongly-continuous-unitary-group, stone-self-adjoint-correspondence, self-adjoint-operator-definition, self-adjoint-spectral-calculus, differentiable-unitary-orbit-at-zero, unbounded-operator-domain-control
- Abstraction concepts: spectral-theorem-and-functional-calculus self-adjoint generator core, barrier + spectral-calculus-interface + unbounded-operator-domain-control evasive representation for spectral-theorem-and-functional-calculus, spectral-theorem-and-functional-calculus functional-calculus normal form in operator-theoretic-Banach-space, barrier + orbit-differentiability-control + unbounded-operator-domain-control evasive representation for spectral-theorem-and-functional-calculus, spectral-calculus-interface + unbounded-operator-domain-control evasive representation for spectral-theorem-and-functional-calculus
- Definitional focus: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, forces target consequence `self-adjoint-operator-on-hilbert-space`
- Counterfactual focus: Remove `realizes antecedent schema `self-adjoint-operator-on-hilbert-space`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, preserves `spectral functional-calculus realization in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`, Assume the first sufficient attribute set is fully realized: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`
- Bridges: bridge.001, bridge.003, bridge.008
- Hypotheses: phyp.stone-one-parameter-unitary-groups.035, phyp.stone-one-parameter-unitary-groups.001, phyp.stone-one-parameter-unitary-groups.003, phyp.stone-one-parameter-unitary-groups.041
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.4651, coherence_avg=0.0072
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.self-adjoint-operator and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.005 - Cross-Model Strategy around st.thm.unitary-group-implies-self-adjoint-generator
- Anchor: st.thm.unitary-group-implies-self-adjoint-generator
- Phase: Current Bridge Agenda
- Score: 0.5584
- Concept fertility: 0.7976
- Anchor concepts: spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-and-functional-calculus, self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, strongly-continuous-unitary-group
- Bridge concepts: self-adjoint-operator-on-hilbert-space, differentiable-unitary-orbit-at-zero, unbounded-operator-domain-control, strongly-continuous-unitary-group, self-adjoint-operator-definition, self-adjoint-spectral-calculus, unbounded-generator-graph, spectral-theorem-enables-unitary-functional-calculus
- Abstraction concepts: spectral-theorem-and-functional-calculus self-adjoint generator core, barrier + orbit-differentiability-control + unbounded-operator-domain-control evasive representation for spectral-theorem-and-functional-calculus, spectral-theorem-and-functional-calculus functional-calculus normal form in operator-theoretic-Banach-space, barrier + orbit-differentiability-control + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus, spectral-theorem-enables-unitary-functional-calculus self-adjoint generator core, spectral-theorem-enables-unitary-functional-calculus functional-calculus normal form in self-adjoint-spectral-calculus
- Definitional focus: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, forces target consequence `self-adjoint-operator-on-hilbert-space`, realizes antecedent schema `spectral-theorem-and-functional-calculus`, realizes antecedent schema `strongly-continuous-unitary-group`
- Counterfactual focus: Remove `realizes antecedent schema `self-adjoint-operator-on-hilbert-space`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, preserves `self-adjoint generator recovery in self-adjoint-spectral-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`, Remove `realizes antecedent schema `spectral-theorem-and-functional-calculus`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `spectral-theorem-and-functional-calculus`, preserves `self-adjoint generator recovery in unbounded-generator-graph`, forces target consequence `self-adjoint-operator-on-hilbert-space`
- Bridges: bridge.003, bridge.004, bridge.005
- Hypotheses: phyp.stone-one-parameter-unitary-groups.032, phyp.stone-one-parameter-unitary-groups.003, phyp.stone-one-parameter-unitary-groups.004, phyp.stone-one-parameter-unitary-groups.005
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.6, barrier_evasion=0.6, lemma_generation=0.0, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.4263, coherence_avg=0.0073
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.thm.unitary-group-implies-self-adjoint-generator and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.006 - Cross-Model Strategy around st.prop.generator-domain-regularity
- Anchor: st.prop.generator-domain-regularity
- Phase: Current Bridge Agenda
- Score: 0.5481
- Concept fertility: 0.7957
- Anchor concepts: c0-generation-implies-closed-dense-generator, self-adjoint-operator-on-hilbert-space, strongly-continuous-unitary-group, generator-of-c0-semigroup, closed-densely-defined-generator
- Bridge concepts: unbounded-generator-graph, self-adjoint-operator-on-hilbert-space, unbounded-operator-domain-control, strongly-continuous-unitary-group, self-adjoint-operator-definition, orbit-differentiability-control
- Abstraction concepts: barrier + domain-closure-density + orbit-differentiability-control evasive representation for spectral-theorem-and-functional-calculus, spectral-theorem-and-functional-calculus self-adjoint generator core, spectral-theorem-and-functional-calculus functional-calculus normal form in self-adjoint-spectral-calculus
- Definitional focus: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, forces target consequence `self-adjoint-operator-on-hilbert-space`
- Counterfactual focus: Remove `realizes antecedent schema `self-adjoint-operator-on-hilbert-space`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `self-adjoint-operator-on-hilbert-space`, preserves `self-adjoint generator recovery in unbounded-generator-graph`, forces target consequence `self-adjoint-operator-on-hilbert-space`
- Bridges: bridge.016
- Hypotheses: phyp.stone-one-parameter-unitary-groups.036, phyp.stone-one-parameter-unitary-groups.016, phyp.stone-one-parameter-unitary-groups.056, phyp.stone-one-parameter-unitary-groups.026
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.3, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.4334, coherence_avg=0.0057
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.prop.generator-domain-regularity and restate objective as conditional entailment gain.
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
- global_coherence=0.5946
- tension=0.2191
- coherence_negative_hypotheses=1
- risk_mode=off
- top_abstraction_conjectures=conj.001:barrier-escaping-representation:barrier + orbit-differentiability-control + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus; conj.002:self-adjoint-generator-core:spectral-theorem-enables-unitary-functional-calculus self-adjoint generator core; conj.007:barrier-escaping-representation:barrier + spectral-calculus-interface evasive representation for spectral-theorem-enables-unitary-functional-calculus
- top_definitional_requirements=conj.001:realizes antecedent schema `spectral-theorem-and-functional-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`; conj.002:realizes antecedent schema `spectral-theorem-and-functional-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`; conj.007:realizes antecedent schema `spectral-theorem-and-functional-calculus`, forces target consequence `self-adjoint-operator-on-hilbert-space`
- top_counterfactual_probes=conj.001:Remove `realizes antecedent schema `spectral-theorem-and-functional-calculus`` from the candidate abstraction.; conj.002:Remove `realizes antecedent schema `spectral-theorem-and-functional-calculus`` from the candidate abstraction.; conj.007:Remove `realizes antecedent schema `spectral-theorem-and-functional-calculus`` from the candidate abstraction.
Top strategies:
1. strat.001 | anchor=st.thm.stone-correspondence | phase=Current Bridge Agenda | score=0.7478 | fertility=0.8766
2. strat.002 | anchor=st.def.unitary-group | phase=Foundational Gauge-Theoretic Definitions | score=0.6375 | fertility=0.8368
3. strat.003 | anchor=st.thm.self-adjoint-implies-unitary-group | phase=Current Bridge Agenda | score=0.6255 | fertility=0.8774
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
