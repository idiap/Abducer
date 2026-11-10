# Proof Strategy Portfolio

## Stats

- Strategies: 6
- Pathways used: 8
- Bridges used: 20
- Conjectured abstractions used: 28
- Hypotheses used: 44
- Coherence signals used: 44

## Strategies

| strategy_id | name | phase | anchor | score | fertility | anchor_concepts |
|---|---|---|---|---|---|---|
| strat.001 | Cross-Model Strategy around st.thm.hille-yosida-general | Current Bridge Agenda | st.thm.hille-yosida-general | 0.7519 | 0.9049 | equivalence-schema, local-hypothesis-bundle, equivalence, group-theoretic-structure |
| strat.002 | Cross-Model Strategy around st.prop.generator-closed-dense | Additional KB-Specific Phases | st.prop.generator-closed-dense | 0.5895 | 0.8227 | group-theoretic-structure, laplace-transform, barrier, domain-regularity |
| strat.003 | Cross-Model Strategy around st.def.c0-semigroup | Current Bridge Agenda | st.def.c0-semigroup | 0.588 | 0.8499 | group-theoretic-structure, operator-theoretic-model, laplace-transform |
| strat.004 | Cross-Model Strategy around st.def.resolvent | Foundational Gauge-Theoretic Definitions | st.def.resolvent | 0.577 | 0.7904 | operator-theoretic-model, resolvent-estimate |
| strat.005 | Cross-Model Strategy around st.thm.cauchy-problem-equivalence | Current Bridge Agenda | st.thm.cauchy-problem-equivalence | 0.5601 | 0.8621 | unconditional, equivalence, group-theoretic-structure, operator-theoretic-model |
| strat.006 | Cross-Model Strategy around st.def.generator | Current Bridge Agenda | st.def.generator | 0.5507 | 0.8861 | group-theoretic-structure, laplace-transform |

### strat.001 - Cross-Model Strategy around st.thm.hille-yosida-general
- Anchor: st.thm.hille-yosida-general
- Phase: Current Bridge Agenda
- Score: 0.7519
- Concept fertility: 0.9049
- Anchor concepts: equivalence-schema, local-hypothesis-bundle, equivalence, group-theoretic-structure, operator-theoretic-model
- Bridge concepts: group-theoretic-structure, operator-theoretic-model, laplace-transform, resolvent-estimate, equivalence-schema, equivalence
- Abstraction concepts: barrier + powers-of-resolvent-verification evasive representation for powers-of-resolvent-verification, powers-of-resolvent-verification complexity potential in group-theoretic-structure, powers-of-resolvent-verification reduction gadget family, powers-of-resolvent-verification hitting-set or pseudorandom family
- Definitional focus: forces target consequence `equivalence`, preserves `group-theoretic-structure mathematical structure`, realizes antecedent schema `equivalence-schema`
- Counterfactual focus: Remove `forces target consequence `equivalence`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: preserves `group-theoretic-structure mathematical structure`, provides an explicit transfer law or reduction mechanism, forces target consequence `equivalence`, Remove `realizes antecedent schema `equivalence-schema`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `equivalence-schema`, preserves `consequence schema equivalence`, provides an explicit transfer law or reduction mechanism, forces target consequence `equivalence`
- Bridges: bridge.003, bridge.004, bridge.009
- Hypotheses: phyp.hille-yosida-theorem.021, phyp.hille-yosida-theorem.003, phyp.hille-yosida-theorem.035, phyp.hille-yosida-theorem.004
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=1.0, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.4748, coherence_avg=0.0068
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.thm.hille-yosida-general and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.002 - Cross-Model Strategy around st.prop.generator-closed-dense
- Anchor: st.prop.generator-closed-dense
- Phase: Additional KB-Specific Phases
- Score: 0.5895
- Concept fertility: 0.8227
- Anchor concepts: group-theoretic-structure, laplace-transform, barrier, domain-regularity
- Bridge concepts: group-theoretic-structure, laplace-transform
- Abstraction concepts: barrier + domain-regularity evasive representation for group-theoretic-structure, group-theoretic-structure hitting-set or pseudorandom family, group-theoretic-structure complexity potential in group-theoretic-structure
- Definitional focus: preserves `group-theoretic-structure mathematical structure`, introduces an explicit witness object for `group-theoretic-structure`
- Counterfactual focus: Remove `preserves `group-theoretic-structure mathematical structure`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: introduces an explicit witness object for `group-theoretic-structure`, preserves `group-theoretic-structure mathematical structure`, remains operationalizable on current bridge/pathway anchors
- Bridges: bridge.007, bridge.017
- Hypotheses: phyp.hille-yosida-theorem.007, phyp.hille-yosida-theorem.039, phyp.hille-yosida-theorem.030, phyp.hille-yosida-theorem.017
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.5, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=0.88, counterfactual_avg=1.0, explanatory_avg=0.4224, coherence_avg=0.0065
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.prop.generator-closed-dense and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.003 - Cross-Model Strategy around st.def.c0-semigroup
- Anchor: st.def.c0-semigroup
- Phase: Current Bridge Agenda
- Score: 0.588
- Concept fertility: 0.8499
- Anchor concepts: group-theoretic-structure, operator-theoretic-model, laplace-transform
- Bridge concepts: group-theoretic-structure, operator-theoretic-model, laplace-transform
- Abstraction concepts: group-theoretic-structure complexity potential in group-theoretic-structure, group-theoretic-structure normal-form translation across group-theoretic-structure, barrier + powers-of-resolvent-verification evasive representation for powers-of-resolvent-verification, powers-of-resolvent-verification complexity potential in group-theoretic-structure, powers-of-resolvent-verification reduction gadget family
- Definitional focus: forces target consequence `equivalence`, preserves `group-theoretic-structure mathematical structure`, introduces an explicit witness object for `group-theoretic-structure`
- Counterfactual focus: Remove `forces target consequence `equivalence`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: preserves `group-theoretic-structure mathematical structure`, forces target consequence `equivalence`, Assume the first sufficient attribute set is fully realized: preserves `group-theoretic-structure mathematical structure`, provides an explicit transfer law or reduction mechanism, forces target consequence `equivalence`, Remove `preserves `group-theoretic-structure mathematical structure`` from the candidate abstraction.
- Bridges: bridge.001, bridge.003, bridge.005
- Hypotheses: phyp.hille-yosida-theorem.022, phyp.hille-yosida-theorem.001, phyp.hille-yosida-theorem.033, phyp.hille-yosida-theorem.003
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.55, lemma_generation=0.25, abstraction_leverage=1.0, definitional_avg=0.84, counterfactual_avg=1.0, explanatory_avg=0.4625, coherence_avg=0.0035
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.c0-semigroup and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.004 - Cross-Model Strategy around st.def.resolvent
- Anchor: st.def.resolvent
- Phase: Foundational Gauge-Theoretic Definitions
- Score: 0.577
- Concept fertility: 0.7904
- Anchor concepts: operator-theoretic-model, resolvent-estimate
- Bridge concepts: operator-theoretic-model, resolvent-estimate
- Abstraction concepts: barrier + powers-of-resolvent-verification evasive representation for powers-of-resolvent-verification, powers-of-resolvent-verification complexity potential in operator-theoretic-model, powers-of-resolvent-verification reduction gadget family
- Definitional focus: forces target consequence `equivalence`, preserves `operator-theoretic-model mathematical structure`
- Counterfactual focus: Remove `forces target consequence `equivalence`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: preserves `operator-theoretic-model mathematical structure`, provides an explicit transfer law or reduction mechanism, forces target consequence `equivalence`
- Bridges: bridge.010
- Hypotheses: phyp.hille-yosida-theorem.008, phyp.hille-yosida-theorem.040, phyp.hille-yosida-theorem.010, phyp.hille-yosida-theorem.028
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.3, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.376, coherence_avg=0.0104
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.resolvent and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.005 - Cross-Model Strategy around st.thm.cauchy-problem-equivalence
- Anchor: st.thm.cauchy-problem-equivalence
- Phase: Current Bridge Agenda
- Score: 0.5601
- Concept fertility: 0.8621
- Anchor concepts: unconditional, equivalence, group-theoretic-structure, operator-theoretic-model, laplace-transform
- Bridge concepts: group-theoretic-structure, operator-theoretic-model, laplace-transform, unconditional, equivalence
- Abstraction concepts: group-theoretic-structure complexity potential in group-theoretic-structure, group-theoretic-structure normal-form translation across group-theoretic-structure, barrier + domain-closure-density evasive representation for group-theoretic-structure
- Definitional focus: forces target consequence `equivalence`, preserves `group-theoretic-structure mathematical structure`, realizes antecedent schema `equivalence`
- Counterfactual focus: Remove `forces target consequence `equivalence`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: preserves `group-theoretic-structure mathematical structure`, forces target consequence `equivalence`, Remove `realizes antecedent schema `equivalence`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `equivalence`, preserves `consequence schema equivalence`, forces target consequence `equivalence`
- Bridges: bridge.001, bridge.002, bridge.016
- Hypotheses: phyp.hille-yosida-theorem.026, phyp.hille-yosida-theorem.001, phyp.hille-yosida-theorem.033, phyp.hille-yosida-theorem.002
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=0.904, counterfactual_avg=1.0, explanatory_avg=0.3929, coherence_avg=0.0067
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.thm.cauchy-problem-equivalence and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.006 - Cross-Model Strategy around st.def.generator
- Anchor: st.def.generator
- Phase: Current Bridge Agenda
- Score: 0.5507
- Concept fertility: 0.8861
- Anchor concepts: group-theoretic-structure, laplace-transform
- Bridge concepts: group-theoretic-structure, laplace-transform
- Abstraction concepts: group-theoretic-structure complexity potential in group-theoretic-structure, group-theoretic-structure normal-form translation across group-theoretic-structure, barrier + powers-of-resolvent-verification evasive representation for powers-of-resolvent-verification, powers-of-resolvent-verification hitting-set or pseudorandom family, powers-of-resolvent-verification complexity potential in group-theoretic-structure
- Definitional focus: forces target consequence `equivalence`, preserves `group-theoretic-structure mathematical structure`, introduces an explicit witness object for `group-theoretic-structure`
- Counterfactual focus: Remove `forces target consequence `equivalence`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: preserves `group-theoretic-structure mathematical structure`, forces target consequence `equivalence`, Assume the first sufficient attribute set is fully realized: preserves `group-theoretic-structure mathematical structure`, provides an explicit transfer law or reduction mechanism, forces target consequence `equivalence`, Remove `preserves `group-theoretic-structure mathematical structure`` from the candidate abstraction.
- Bridges: bridge.002, bridge.004, bridge.005
- Hypotheses: phyp.hille-yosida-theorem.025, phyp.hille-yosida-theorem.002, phyp.hille-yosida-theorem.034, phyp.hille-yosida-theorem.004
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=1.0, definitional_avg=0.84, counterfactual_avg=1.0, explanatory_avg=0.446, coherence_avg=0.0067
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.generator and restate objective as conditional entailment gain.
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
- global_coherence=0.6083
- tension=0.1999
- coherence_negative_hypotheses=1
- risk_mode=off
- top_abstraction_conjectures=conj.001:barrier-escaping-representation:barrier + powers-of-resolvent-verification evasive representation for powers-of-resolvent-verification; conj.003:barrier-escaping-representation:barrier + powers-of-resolvent-verification evasive representation for powers-of-resolvent-verification; conj.006:barrier-escaping-representation:barrier + powers-of-resolvent-verification evasive representation for powers-of-resolvent-verification
- top_definitional_requirements=conj.001:realizes antecedent schema `equivalence-schema`, forces target consequence `equivalence`; conj.003:forces target consequence `equivalence`, preserves `group-theoretic-structure mathematical structure`; conj.006:forces target consequence `equivalence`, preserves `group-theoretic-structure mathematical structure`
- top_counterfactual_probes=conj.001:Remove `realizes antecedent schema `equivalence-schema`` from the candidate abstraction.; conj.003:Remove `forces target consequence `equivalence`` from the candidate abstraction.; conj.006:Remove `forces target consequence `equivalence`` from the candidate abstraction.
Top strategies:
1. strat.001 | anchor=st.thm.hille-yosida-general | phase=Current Bridge Agenda | score=0.7519 | fertility=0.9049
2. strat.002 | anchor=st.prop.generator-closed-dense | phase=Additional KB-Specific Phases | score=0.5895 | fertility=0.8227
3. strat.003 | anchor=st.def.c0-semigroup | phase=Current Bridge Agenda | score=0.588 | fertility=0.8499
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
