# Proof Strategy Portfolio

## Stats

- Strategies: 6
- Pathways used: 8
- Bridges used: 20
- Conjectured abstractions used: 36
- Hypotheses used: 32
- Coherence signals used: 32

## Strategies

| strategy_id | name | phase | anchor | score | fertility | anchor_concepts |
|---|---|---|---|---|---|---|
| strat.001 | Cross-Model Strategy around st.thm.markov-kakutani | Current Bridge Agenda | st.thm.markov-kakutani | 0.7421 | 0.8729 | finite-intersection-property-implies-common-fixed-point, commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, nonempty-compact-convex-subset |
| strat.002 | Cross-Model Strategy around st.def.compact-convex-set | Foundational Gauge-Theoretic Definitions | st.def.compact-convex-set | 0.6629 | 0.8662 | nonempty-compact-convex-subset, compact-convex-set-definition, compact-convex-subset, locally-convex-topological-vector-space |
| strat.003 | Cross-Model Strategy around st.lem.commuting-preserves-fixed-point-subset | Additional KB-Specific Phases | st.lem.commuting-preserves-fixed-point-subset | 0.5992 | 0.7666 | commuting-affine-family-on-compact-convex-set, single-affine-self-map-on-compact-convex-set, invariant-fixed-point-subset, invariant-fixed-point-subset-definition |
| strat.004 | Cross-Model Strategy around st.lem.single-map-fixed-point | Current Bridge Agenda | st.lem.single-map-fixed-point | 0.5987 | 0.8846 | single-map-fixed-point-implies-invariant-fixed-point-subset, finite-intersection-property-implies-common-fixed-point, continuous-affine-self-map-on-compact-convex-set, commuting-affine-family-on-compact-convex-set |
| strat.005 | Cross-Model Strategy around st.lem.cesaro-averages | Current Bridge Agenda | st.lem.cesaro-averages | 0.547 | 0.9098 | affine-averaging-implies-single-map-fixed-point, continuous-affine-self-map-on-compact-convex-set, nonempty-compact-convex-subset, affine-orbit-averages-in-compact-convex-set |
| strat.006 | Cross-Model Strategy around st.lem.finite-family-common-fixed-point | Current Bridge Agenda | st.lem.finite-family-common-fixed-point | 0.5319 | 0.7904 | finite-intersection-property-implies-common-fixed-point, commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, common-fixed-point-for-finite-commuting-family |

### strat.001 - Cross-Model Strategy around st.thm.markov-kakutani
- Anchor: st.thm.markov-kakutani
- Phase: Current Bridge Agenda
- Score: 0.7421
- Concept fertility: 0.8729
- Anchor concepts: finite-intersection-property-implies-common-fixed-point, commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, nonempty-compact-convex-subset, common-fixed-point-for-finite-commuting-family
- Bridge concepts: locally-convex-topological-vector-space, topological-vector-space-analysis, finite-intersection-compactness, nonempty-compact-convex-subset, compact-convex-set-definition, invariant-fixed-point-subset, finite-intersection-property-implies-common-fixed-point, common-fixed-point-for-finite-commuting-family
- Abstraction concepts: barrier + finite-intersection-compactness + invariant-subset-propagation evasive representation for common-fixed-point-for-finite-commuting-family, common-fixed-point-for-finite-commuting-family invariant fixed-point subset core in compact-convex-subset, common-fixed-point-for-finite-commuting-family finite-intersection lift in compact-convex-subset, barrier + finite-intersection-compactness + invariant-subset-propagation evasive representation for finite-intersection-property-implies-common-fixed-point, finite-intersection-property-implies-common-fixed-point invariant fixed-point subset core in common-fixed-point-correspondence, finite-intersection-property-implies-common-fixed-point finite-intersection lift in common-fixed-point-correspondence
- Definitional focus: realizes antecedent schema `nonempty-compact-convex-subset`, forces target consequence `common-fixed-point-for-finite-commuting-family`, realizes antecedent schema `commuting-affine-family-on-compact-convex-set`
- Counterfactual focus: Remove `realizes antecedent schema `nonempty-compact-convex-subset`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `nonempty-compact-convex-subset`, preserves `nonempty compact-convex fixed-point subset in locally-convex-topological-vector-space`, provides an explicit transfer law or reduction mechanism, forces target consequence `common-fixed-point-for-finite-commuting-family`, Remove `realizes antecedent schema `commuting-affine-family-on-compact-convex-set`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `commuting-affine-family-on-compact-convex-set`, preserves `finite-intersection lift in common-fixed-point-correspondence`, provides an explicit transfer law or reduction mechanism, forces target consequence `common-fixed-point-for-finite-commuting-family`
- Bridges: bridge.001, bridge.003, bridge.007
- Hypotheses: phyp.markov-kakutani-fixed-point-theorem.018, phyp.markov-kakutani-fixed-point-theorem.001, phyp.markov-kakutani-fixed-point-theorem.025, phyp.markov-kakutani-fixed-point-theorem.003
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.4028, coherence_avg=0.0087
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.thm.markov-kakutani and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.002 - Cross-Model Strategy around st.def.compact-convex-set
- Anchor: st.def.compact-convex-set
- Phase: Foundational Gauge-Theoretic Definitions
- Score: 0.6629
- Concept fertility: 0.8662
- Anchor concepts: nonempty-compact-convex-subset, compact-convex-set-definition, compact-convex-subset, locally-convex-topological-vector-space, affine-self-map
- Bridge concepts: locally-convex-topological-vector-space, topological-vector-space-analysis, finite-intersection-compactness, nonempty-compact-convex-subset, compact-convex-set-definition, invariant-fixed-point-subset, compact-convex-subset, affine-map-analysis
- Abstraction concepts: barrier + finite-intersection-compactness + invariant-subset-propagation evasive representation for common-fixed-point-for-finite-commuting-family, common-fixed-point-for-finite-commuting-family invariant fixed-point subset core in compact-convex-subset, common-fixed-point-for-finite-commuting-family finite-intersection lift in compact-convex-subset, barrier + finite-intersection-compactness + single-map-fixed-point-extraction evasive representation for continuous-affine-self-map-on-compact-convex-set, continuous-affine-self-map-on-compact-convex-set invariant fixed-point subset core in compact-convex-subset, continuous-affine-self-map-on-compact-convex-set affine averaging kernel in compact-convex-subset
- Definitional focus: realizes antecedent schema `nonempty-compact-convex-subset`, forces target consequence `common-fixed-point-for-finite-commuting-family`, forces target consequence `single-map-fixed-point`
- Counterfactual focus: Remove `realizes antecedent schema `nonempty-compact-convex-subset`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `nonempty-compact-convex-subset`, preserves `nonempty compact-convex fixed-point subset in locally-convex-topological-vector-space`, provides an explicit transfer law or reduction mechanism, forces target consequence `common-fixed-point-for-finite-commuting-family`, Assume the first sufficient attribute set is fully realized: realizes antecedent schema `nonempty-compact-convex-subset`, preserves `averaged affine orbit stabilization in compact-convex-subset`, provides an explicit transfer law or reduction mechanism, forces target consequence `single-map-fixed-point`, Assume the first sufficient attribute set is fully realized: realizes antecedent schema `nonempty-compact-convex-subset`, preserves `nonempty compact-convex fixed-point subset in compact-convex-subset`, provides an explicit transfer law or reduction mechanism, forces target consequence `common-fixed-point-for-finite-commuting-family`
- Bridges: bridge.001, bridge.004, bridge.006
- Hypotheses: phyp.markov-kakutani-fixed-point-theorem.023, phyp.markov-kakutani-fixed-point-theorem.001, phyp.markov-kakutani-fixed-point-theorem.025, phyp.markov-kakutani-fixed-point-theorem.004
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.55, lemma_generation=0.25, abstraction_leverage=1.0, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.4663, coherence_avg=0.0024
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.compact-convex-set and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.003 - Cross-Model Strategy around st.lem.commuting-preserves-fixed-point-subset
- Anchor: st.lem.commuting-preserves-fixed-point-subset
- Phase: Additional KB-Specific Phases
- Score: 0.5992
- Concept fertility: 0.7666
- Anchor concepts: commuting-affine-family-on-compact-convex-set, single-affine-self-map-on-compact-convex-set, invariant-fixed-point-subset, invariant-fixed-point-subset-definition, commuting-affine-family-definition
- Bridge concepts: commuting-affine-family-on-compact-convex-set, commuting-affine-family-definition, commuting-affine-self-map-family, invariant-subset-propagation, invariant-fixed-point-subset, commuting-family-analysis, single-affine-self-map-on-compact-convex-set, invariant-fixed-point-subset-definition
- Abstraction concepts: common-fixed-point-for-finite-commuting-family invariant fixed-point subset core in commuting-affine-self-map-family, common-fixed-point-for-finite-commuting-family finite-intersection lift in commuting-affine-self-map-family, barrier + finite-intersection-compactness + invariant-subset-propagation evasive representation for common-fixed-point-for-finite-commuting-family
- Definitional focus: realizes antecedent schema `commuting-affine-family-on-compact-convex-set`, forces target consequence `common-fixed-point-for-finite-commuting-family`
- Counterfactual focus: Remove `realizes antecedent schema `commuting-affine-family-on-compact-convex-set`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `commuting-affine-family-on-compact-convex-set`, preserves `nonempty compact-convex fixed-point subset in commuting-affine-self-map-family`, provides an explicit transfer law or reduction mechanism, forces target consequence `common-fixed-point-for-finite-commuting-family`
- Bridges: bridge.017, bridge.019, bridge.009
- Hypotheses: phyp.markov-kakutani-fixed-point-theorem.024, phyp.markov-kakutani-fixed-point-theorem.009, phyp.markov-kakutani-fixed-point-theorem.013
- Fertility components: unification_gain=0.5, proof_compression=0.5, transfer_power=0.6, barrier_evasion=0.6, lemma_generation=0.0, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.2575, coherence_avg=0.0084
- Hypothesis status summary: unresolved=3
- Execution protocol:
  - Anchor on st.lem.commuting-preserves-fixed-point-subset and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.004 - Cross-Model Strategy around st.lem.single-map-fixed-point
- Anchor: st.lem.single-map-fixed-point
- Phase: Current Bridge Agenda
- Score: 0.5987
- Concept fertility: 0.8846
- Anchor concepts: single-map-fixed-point-implies-invariant-fixed-point-subset, finite-intersection-property-implies-common-fixed-point, continuous-affine-self-map-on-compact-convex-set, commuting-affine-family-on-compact-convex-set, single-affine-self-map-on-compact-convex-set
- Bridge concepts: finite-intersection-compactness, nonempty-compact-convex-subset, compact-convex-set-definition, compact-convex-subset, affine-map-analysis, compactness-method, continuous-affine-self-map-on-compact-convex-set, single-map-fixed-point-extraction
- Abstraction concepts: barrier + finite-intersection-compactness + single-map-fixed-point-extraction evasive representation for continuous-affine-self-map-on-compact-convex-set, continuous-affine-self-map-on-compact-convex-set invariant fixed-point subset core in compact-convex-subset, continuous-affine-self-map-on-compact-convex-set finite-intersection lift in compact-convex-subset, continuous-affine-self-map-on-compact-convex-set invariant fixed-point subset core in cesaro-averaging-scheme, continuous-affine-self-map-on-compact-convex-set finite-intersection lift in cesaro-averaging-scheme
- Definitional focus: realizes antecedent schema `nonempty-compact-convex-subset`, forces target consequence `common-fixed-point-for-finite-commuting-family`, realizes antecedent schema `continuous-affine-self-map-on-compact-convex-set`
- Counterfactual focus: Remove `realizes antecedent schema `nonempty-compact-convex-subset`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `nonempty-compact-convex-subset`, preserves `nonempty compact-convex fixed-point subset in compact-convex-subset`, provides an explicit transfer law or reduction mechanism, forces target consequence `common-fixed-point-for-finite-commuting-family`, Remove `realizes antecedent schema `continuous-affine-self-map-on-compact-convex-set`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `continuous-affine-self-map-on-compact-convex-set`, preserves `averaged affine orbit stabilization in single-affine-self-map`, forces target consequence `common-fixed-point-for-finite-commuting-family`
- Bridges: bridge.006, bridge.008, bridge.018
- Hypotheses: phyp.markov-kakutani-fixed-point-theorem.017, phyp.markov-kakutani-fixed-point-theorem.006, phyp.markov-kakutani-fixed-point-theorem.008, phyp.markov-kakutani-fixed-point-theorem.030
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.5195, coherence_avg=0.0087
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.lem.single-map-fixed-point and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.005 - Cross-Model Strategy around st.lem.cesaro-averages
- Anchor: st.lem.cesaro-averages
- Phase: Current Bridge Agenda
- Score: 0.547
- Concept fertility: 0.9098
- Anchor concepts: affine-averaging-implies-single-map-fixed-point, continuous-affine-self-map-on-compact-convex-set, nonempty-compact-convex-subset, affine-orbit-averages-in-compact-convex-set, single-map-fixed-point
- Bridge concepts: nonempty-compact-convex-subset, compact-convex-set-definition, compact-convex-subset, affine-map-analysis, compactness-method, compact-convex-set, continuous-affine-self-map-on-compact-convex-set, single-map-fixed-point-extraction
- Abstraction concepts: barrier + finite-intersection-compactness + single-map-fixed-point-extraction evasive representation for continuous-affine-self-map-on-compact-convex-set, continuous-affine-self-map-on-compact-convex-set invariant fixed-point subset core in compact-convex-subset, continuous-affine-self-map-on-compact-convex-set affine averaging kernel in compact-convex-subset, continuous-affine-self-map-on-compact-convex-set invariant fixed-point subset core in cesaro-averaging-scheme, continuous-affine-self-map-on-compact-convex-set finite-intersection lift in cesaro-averaging-scheme
- Definitional focus: realizes antecedent schema `nonempty-compact-convex-subset`, forces target consequence `single-map-fixed-point`, realizes antecedent schema `continuous-affine-self-map-on-compact-convex-set`, forces target consequence `common-fixed-point-for-finite-commuting-family`
- Counterfactual focus: Remove `realizes antecedent schema `nonempty-compact-convex-subset`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `nonempty-compact-convex-subset`, preserves `averaged affine orbit stabilization in compact-convex-subset`, provides an explicit transfer law or reduction mechanism, forces target consequence `single-map-fixed-point`, Remove `realizes antecedent schema `continuous-affine-self-map-on-compact-convex-set`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `continuous-affine-self-map-on-compact-convex-set`, preserves `averaged affine orbit stabilization in single-affine-self-map`, forces target consequence `common-fixed-point-for-finite-commuting-family`
- Bridges: bridge.004, bridge.008, bridge.005
- Hypotheses: phyp.markov-kakutani-fixed-point-theorem.021, phyp.markov-kakutani-fixed-point-theorem.004, phyp.markov-kakutani-fixed-point-theorem.008, phyp.markov-kakutani-fixed-point-theorem.028
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=1.0, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.5216, coherence_avg=0.0086
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.lem.cesaro-averages and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.006 - Cross-Model Strategy around st.lem.finite-family-common-fixed-point
- Anchor: st.lem.finite-family-common-fixed-point
- Phase: Current Bridge Agenda
- Score: 0.5319
- Concept fertility: 0.7904
- Anchor concepts: finite-intersection-property-implies-common-fixed-point, commuting-affine-family-on-compact-convex-set, finite-commuting-affine-subfamily, common-fixed-point-for-finite-commuting-family, common-fixed-point-for-commuting-family
- Bridge concepts: finite-intersection-property-implies-common-fixed-point, common-fixed-point-for-finite-commuting-family, commuting-affine-family-on-compact-convex-set, common-fixed-point-for-commuting-family, markov-kakutani-common-fixed-point, commuting-affine-family-definition, commuting-affine-self-map-family, invariant-subset-propagation
- Abstraction concepts: barrier + finite-intersection-compactness + invariant-subset-propagation evasive representation for finite-intersection-property-implies-common-fixed-point, finite-intersection-property-implies-common-fixed-point invariant fixed-point subset core in common-fixed-point-correspondence, finite-intersection-property-implies-common-fixed-point finite-intersection lift in common-fixed-point-correspondence
- Definitional focus: realizes antecedent schema `commuting-affine-family-on-compact-convex-set`, forces target consequence `common-fixed-point-for-finite-commuting-family`
- Counterfactual focus: Remove `realizes antecedent schema `commuting-affine-family-on-compact-convex-set`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `commuting-affine-family-on-compact-convex-set`, preserves `finite-intersection lift in common-fixed-point-correspondence`, provides an explicit transfer law or reduction mechanism, forces target consequence `common-fixed-point-for-finite-commuting-family`
- Bridges: bridge.003, bridge.017
- Hypotheses: phyp.markov-kakutani-fixed-point-theorem.020, phyp.markov-kakutani-fixed-point-theorem.003, phyp.markov-kakutani-fixed-point-theorem.027, phyp.markov-kakutani-fixed-point-theorem.014
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.5, barrier_evasion=0.55, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.3548, coherence_avg=0.006
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.lem.finite-family-common-fixed-point and restate objective as conditional entailment gain.
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
- global_coherence=0.6588
- tension=0.0979
- coherence_negative_hypotheses=5
- risk_mode=off
- top_abstraction_conjectures=conj.001:barrier-escaping-representation:barrier + finite-intersection-compactness + invariant-subset-propagation evasive representation for finite-intersection-property-implies-common-fixed-point; conj.002:invariant-fixed-point-core:finite-intersection-property-implies-common-fixed-point invariant fixed-point subset core in common-fixed-point-correspondence; conj.003:finite-intersection-lift:finite-intersection-property-implies-common-fixed-point finite-intersection lift in common-fixed-point-correspondence
- top_definitional_requirements=conj.001:realizes antecedent schema `commuting-affine-family-on-compact-convex-set`, forces target consequence `common-fixed-point-for-finite-commuting-family`; conj.002:realizes antecedent schema `commuting-affine-family-on-compact-convex-set`, forces target consequence `common-fixed-point-for-finite-commuting-family`; conj.003:realizes antecedent schema `commuting-affine-family-on-compact-convex-set`, forces target consequence `common-fixed-point-for-finite-commuting-family`
- top_counterfactual_probes=conj.001:Remove `realizes antecedent schema `commuting-affine-family-on-compact-convex-set`` from the candidate abstraction.; conj.002:Remove `realizes antecedent schema `commuting-affine-family-on-compact-convex-set`` from the candidate abstraction.; conj.003:Remove `realizes antecedent schema `commuting-affine-family-on-compact-convex-set`` from the candidate abstraction.
Top strategies:
1. strat.001 | anchor=st.thm.markov-kakutani | phase=Current Bridge Agenda | score=0.7421 | fertility=0.8729
2. strat.002 | anchor=st.def.compact-convex-set | phase=Foundational Gauge-Theoretic Definitions | score=0.6629 | fertility=0.8662
3. strat.003 | anchor=st.lem.commuting-preserves-fixed-point-subset | phase=Additional KB-Specific Phases | score=0.5992 | fertility=0.7666
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
