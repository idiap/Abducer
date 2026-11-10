# Proof Strategy Portfolio

## Stats

- Strategies: 8
- Pathways used: 8
- Bridges used: 20
- Conjectured abstractions used: 34
- Hypotheses used: 44
- Coherence signals used: 44

## Strategies

| strategy_id | name | phase | anchor | score | fertility | anchor_concepts |
|---|---|---|---|---|---|---|
| strat.001 | Cross-Model Strategy around st.thm.hille-yosida-general | Current Bridge Agenda | st.thm.hille-yosida-general | 0.7987 | 0.8776 | c0-generation-implies-closed-dense-generator, resolvent-approximants-converge-to-generated-semigroup, closed-dense-plus-resolvent-powers-imply-c0-generation, closed-dense-operator-with-resolvent-power-bounds |
| strat.002 | Cross-Model Strategy around st.def.c0-semigroup | Current Bridge Agenda | st.def.c0-semigroup | 0.69 | 0.9859 | c0-semigroup-definition, C0-semigroup-model, operator-theoretic-Banach-space, Banach-space |
| strat.003 | Cross-Model Strategy around st.def.generator | Current Bridge Agenda | st.def.generator | 0.6448 | 0.9022 | c0-semigroup-definition, generator-definition, C0-semigroup-model, operator-theoretic-Banach-space |
| strat.004 | Cross-Model Strategy around st.thm.cauchy-problem-equivalence | Current Bridge Agenda | st.thm.cauchy-problem-equivalence | 0.6357 | 0.8764 | c0-generation-iff-cauchy-well-posedness, closed-operator-or-semigroup-generator, well-posed-abstract-cauchy-problem, cauchy-problem-equivalence |
| strat.005 | Cross-Model Strategy around st.def.resolvent | Foundational Gauge-Theoretic Definitions | st.def.resolvent | 0.6148 | 0.7979 | resolvent-approximants-converge-to-generated-semigroup, resolvent-family-at-large-lambda, bounded-generator-approximation-scheme, yosida-approximation-convergence |
| strat.006 | Cross-Model Strategy around st.prop.generator-closed-dense | Additional KB-Specific Phases | st.prop.generator-closed-dense | 0.6124 | 0.7963 | c0-generation-implies-closed-dense-generator, generator-of-c0-semigroup, closed-densely-defined-generator, generator-closed-dense |
| strat.007 | Cross-Model Strategy around st.thm.hille-yosida-contraction | Current Bridge Agenda | st.thm.hille-yosida-contraction | 0.572 | 0.8693 | c0-generation-implies-closed-dense-generator, closed-dense-plus-first-resolvent-bound-imply-contraction-generation, resolvent-approximants-converge-to-generated-semigroup, closed-dense-operator-with-first-resolvent-bound |
| strat.008 | Cross-Model Strategy around st.thm.lumer-phillips | Current Bridge Agenda | st.thm.lumer-phillips | 0.5574 | 0.8656 | closed-dense-plus-first-resolvent-bound-imply-contraction-generation, dissipativity-plus-range-condition-imply-contraction-generation, densely-defined-dissipative-operator-with-surjective-shift, closed-dense-operator-with-first-resolvent-bound |

### strat.001 - Cross-Model Strategy around st.thm.hille-yosida-general
- Anchor: st.thm.hille-yosida-general
- Phase: Current Bridge Agenda
- Score: 0.7987
- Concept fertility: 0.8776
- Anchor concepts: c0-generation-implies-closed-dense-generator, resolvent-approximants-converge-to-generated-semigroup, closed-dense-plus-resolvent-powers-imply-c0-generation, closed-dense-operator-with-resolvent-power-bounds, resolvent-family-at-large-lambda
- Bridge concepts: unbounded-generator-graph, unbounded-operator-domain-control, operator-theoretic-Banach-space, domain-closure-density, semigroup-generation, generator-analysis, unbounded-operator, C0-semigroup-model
- Abstraction concepts: approximation-limit-control + barrier + domain-closure-density evasive representation for closed-dense-operator-with-resolvent-power-bounds, closed-dense-operator-with-resolvent-power-bounds hitting-set or pseudorandom family, closed-dense-operator-with-resolvent-power-bounds complexity potential in C0-semigroup-model, barrier + domain-closure-density + powers-of-resolvent-verification evasive representation for closed-dense-operator-with-resolvent-power-bounds, barrier + domain-closure-density + powers-of-resolvent-verification evasive representation for c0-generation-implies-closed-dense-generator, c0-generation-implies-closed-dense-generator hitting-set or pseudorandom family
- Definitional focus: realizes antecedent schema `c0-semigroup-definition`, forces target consequence `generator-of-exponentially-bounded-c0-semigroup`, realizes antecedent schema `closed-dense-operator-with-resolvent-power-bounds`, forces target consequence `bounded-generator-approximation-scheme`
- Counterfactual focus: Remove `realizes antecedent schema `c0-semigroup-definition`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `c0-semigroup-definition`, preserves `Yosida approximation convergence in unbounded-generator-graph`, forces target consequence `generator-of-exponentially-bounded-c0-semigroup`, Assume the first sufficient attribute set is fully realized: realizes antecedent schema `c0-semigroup-definition`, preserves `Yosida approximation convergence in operator-theoretic-Banach-space`, forces target consequence `generator-of-exponentially-bounded-c0-semigroup`, Remove `realizes antecedent schema `closed-dense-operator-with-resolvent-power-bounds`` from the candidate abstraction.
- Bridges: bridge.002, bridge.003, bridge.009
- Hypotheses: phyp.hille-yosida-theorem.021, phyp.hille-yosida-theorem.002, phyp.hille-yosida-theorem.003, phyp.hille-yosida-theorem.034
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.4501, coherence_avg=0.0085
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.thm.hille-yosida-general and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.002 - Cross-Model Strategy around st.def.c0-semigroup
- Anchor: st.def.c0-semigroup
- Phase: Current Bridge Agenda
- Score: 0.69
- Concept fertility: 0.9859
- Anchor concepts: c0-semigroup-definition, C0-semigroup-model, operator-theoretic-Banach-space, Banach-space, C0-semigroup
- Bridge concepts: operator-theoretic-Banach-space, semigroup-generation, C0-semigroup-model, laplace-transform, C0-semigroup, Banach-space, unbounded-operator
- Abstraction concepts: unbounded-operator-domain-control evasive representation for closed-operator-or-semigroup-generator, closed-operator-or-semigroup-generator hitting-set or pseudorandom family, closed-operator-or-semigroup-generator normal-form translation across C0-semigroup-model, barrier + domain-closure-density + powers-of-resolvent-verification evasive representation for closed-dense-operator-with-resolvent-power-bounds, closed-dense-operator-with-resolvent-power-bounds hitting-set or pseudorandom family, closed-dense-operator-with-resolvent-power-bounds complexity potential in C0-semigroup-model, barrier + domain-closure-density + unbounded-operator-domain-control evasive representation for densely-defined-dissipative-operator-with-surjective-shift, densely-defined-dissipative-operator-with-surjective-shift hitting-set or pseudorandom family
- Definitional focus: realizes antecedent schema `c0-semigroup-definition`, forces target consequence `well-posed-abstract-cauchy-problem`, forces target consequence `generator-of-exponentially-bounded-c0-semigroup`, forces target consequence `contraction-semigroup-via-dissipativity`
- Counterfactual focus: Remove `realizes antecedent schema `c0-semigroup-definition`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `c0-semigroup-definition`, preserves `generator-to-well-posed-evolution correspondence`, forces target consequence `well-posed-abstract-cauchy-problem`, Assume the first sufficient attribute set is fully realized: realizes antecedent schema `c0-semigroup-definition`, preserves `Yosida approximation convergence in operator-theoretic-Banach-space`, forces target consequence `generator-of-exponentially-bounded-c0-semigroup`, Assume the first sufficient attribute set is fully realized: realizes antecedent schema `c0-semigroup-definition`, preserves `dissipative range-surjectivity criterion`, forces target consequence `contraction-semigroup-via-dissipativity`
- Bridges: bridge.001, bridge.003, bridge.005
- Hypotheses: phyp.hille-yosida-theorem.001, phyp.hille-yosida-theorem.003, phyp.hille-yosida-theorem.033, phyp.hille-yosida-theorem.035
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.8, barrier_evasion=0.8, lemma_generation=0.5, abstraction_leverage=1.0, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.5075, coherence_avg=0.009
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.c0-semigroup and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.003 - Cross-Model Strategy around st.def.generator
- Anchor: st.def.generator
- Phase: Current Bridge Agenda
- Score: 0.6448
- Concept fertility: 0.9022
- Anchor concepts: c0-semigroup-definition, generator-definition, C0-semigroup-model, operator-theoretic-Banach-space, unbounded-generator-graph
- Bridge concepts: unbounded-generator-graph, unbounded-operator-domain-control, operator-theoretic-Banach-space, domain-closure-density, semigroup-generation, generator-analysis, C0-semigroup-model, laplace-transform
- Abstraction concepts: approximation-limit-control + barrier + domain-closure-density evasive representation for closed-dense-operator-with-resolvent-power-bounds, closed-dense-operator-with-resolvent-power-bounds hitting-set or pseudorandom family, closed-dense-operator-with-resolvent-power-bounds complexity potential in C0-semigroup-model, approximation-limit-control + domain-closure-density + unbounded-operator-domain-control evasive representation for closed-operator-or-semigroup-generator, closed-operator-or-semigroup-generator hitting-set or pseudorandom family, closed-operator-or-semigroup-generator normal-form translation across C0-semigroup-model, approximation-limit-control + barrier + domain-closure-density evasive representation for densely-defined-dissipative-operator-with-surjective-shift, densely-defined-dissipative-operator-with-surjective-shift hitting-set or pseudorandom family
- Definitional focus: realizes antecedent schema `c0-semigroup-definition`, forces target consequence `generator-of-exponentially-bounded-c0-semigroup`, forces target consequence `well-posed-abstract-cauchy-problem`, forces target consequence `contraction-semigroup-via-dissipativity`
- Counterfactual focus: Remove `realizes antecedent schema `c0-semigroup-definition`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `c0-semigroup-definition`, preserves `Yosida approximation convergence in unbounded-generator-graph`, forces target consequence `generator-of-exponentially-bounded-c0-semigroup`, Assume the first sufficient attribute set is fully realized: realizes antecedent schema `c0-semigroup-definition`, preserves `generator-to-well-posed-evolution correspondence`, forces target consequence `well-posed-abstract-cauchy-problem`, Assume the first sufficient attribute set is fully realized: realizes antecedent schema `c0-semigroup-definition`, preserves `dissipative range-surjectivity criterion`, forces target consequence `contraction-semigroup-via-dissipativity`
- Bridges: bridge.002, bridge.004, bridge.006
- Hypotheses: phyp.hille-yosida-theorem.002, phyp.hille-yosida-theorem.004, phyp.hille-yosida-theorem.034, phyp.hille-yosida-theorem.024
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=1.0, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.4415, coherence_avg=0.0122
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.generator and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.004 - Cross-Model Strategy around st.thm.cauchy-problem-equivalence
- Anchor: st.thm.cauchy-problem-equivalence
- Phase: Current Bridge Agenda
- Score: 0.6357
- Concept fertility: 0.8764
- Anchor concepts: c0-generation-iff-cauchy-well-posedness, closed-operator-or-semigroup-generator, well-posed-abstract-cauchy-problem, cauchy-problem-equivalence, C0-semigroup-model
- Bridge concepts: operator-theoretic-Banach-space, semigroup-generation, C0-semigroup-model, laplace-transform, C0-semigroup, Banach-space, unbounded-operator-domain-control, domain-regularity
- Abstraction concepts: unbounded-operator-domain-control evasive representation for closed-operator-or-semigroup-generator, closed-operator-or-semigroup-generator hitting-set or pseudorandom family, closed-operator-or-semigroup-generator normal-form translation across C0-semigroup-model, approximation-limit-control + domain-closure-density + unbounded-operator-domain-control evasive representation for closed-operator-or-semigroup-generator
- Definitional focus: realizes antecedent schema `c0-semigroup-definition`, forces target consequence `well-posed-abstract-cauchy-problem`
- Counterfactual focus: Remove `realizes antecedent schema `c0-semigroup-definition`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `c0-semigroup-definition`, preserves `generator-to-well-posed-evolution correspondence`, forces target consequence `well-posed-abstract-cauchy-problem`
- Bridges: bridge.001, bridge.004, bridge.013
- Hypotheses: phyp.hille-yosida-theorem.001, phyp.hille-yosida-theorem.033, phyp.hille-yosida-theorem.023, phyp.hille-yosida-theorem.004
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.4376, coherence_avg=0.0084
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.thm.cauchy-problem-equivalence and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.005 - Cross-Model Strategy around st.def.resolvent
- Anchor: st.def.resolvent
- Phase: Foundational Gauge-Theoretic Definitions
- Score: 0.6148
- Concept fertility: 0.7979
- Anchor concepts: resolvent-approximants-converge-to-generated-semigroup, resolvent-family-at-large-lambda, bounded-generator-approximation-scheme, yosida-approximation-convergence, resolvent-definition
- Bridge concepts: resolvent-approximants-converge-to-generated-semigroup, bounded-generator-approximation-scheme, yosida-approximation-convergence, resolvent-family-at-large-lambda, resolvent-generation-criterion, Yosida-approximation-scheme
- Abstraction concepts: barrier + domain-closure-density + powers-of-resolvent-verification evasive representation for resolvent-approximants-converge-to-generated-semigroup, resolvent-approximants-converge-to-generated-semigroup hitting-set or pseudorandom family, resolvent-approximants-converge-to-generated-semigroup complexity potential in Yosida-approximation-scheme
- Definitional focus: realizes antecedent schema `resolvent-family-at-large-lambda`, forces target consequence `generator-of-exponentially-bounded-c0-semigroup`
- Counterfactual focus: Remove `realizes antecedent schema `resolvent-family-at-large-lambda`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `resolvent-family-at-large-lambda`, preserves `resolvent growth control in resolvent-generation-criterion`, forces target consequence `generator-of-exponentially-bounded-c0-semigroup`
- Bridges: bridge.011
- Hypotheses: phyp.hille-yosida-theorem.011, phyp.hille-yosida-theorem.029, phyp.hille-yosida-theorem.043
- Fertility components: unification_gain=0.5, proof_compression=0.5, transfer_power=0.3333, barrier_evasion=0.7333, lemma_generation=0.3333, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.3376, coherence_avg=0.0078
- Hypothesis status summary: unresolved=3
- Execution protocol:
  - Anchor on st.def.resolvent and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.006 - Cross-Model Strategy around st.prop.generator-closed-dense
- Anchor: st.prop.generator-closed-dense
- Phase: Additional KB-Specific Phases
- Score: 0.6124
- Concept fertility: 0.7963
- Anchor concepts: c0-generation-implies-closed-dense-generator, generator-of-c0-semigroup, closed-densely-defined-generator, generator-closed-dense, C0-semigroup-model
- Bridge concepts: unbounded-generator-graph, unbounded-operator-domain-control, domain-closure-density, semigroup-generation, generator-analysis, C0-semigroup-model, laplace-transform, C0-semigroup
- Abstraction concepts: approximation-limit-control + barrier + domain-closure-density evasive representation for unbounded-operator-domain-control, unbounded-operator-domain-control hitting-set or pseudorandom family
- Definitional focus: realizes antecedent schema `c0-semigroup-definition`, forces target consequence `closed-densely-defined-generator`
- Counterfactual focus: Remove `realizes antecedent schema `c0-semigroup-definition`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `c0-semigroup-definition`, preserves `closed densely defined generator regularity`, forces target consequence `closed-densely-defined-generator`
- Bridges: bridge.012, bridge.019
- Hypotheses: phyp.hille-yosida-theorem.027, phyp.hille-yosida-theorem.012, phyp.hille-yosida-theorem.044, phyp.hille-yosida-theorem.019
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.5, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.5, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.2872, coherence_avg=0.008
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.prop.generator-closed-dense and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.007 - Cross-Model Strategy around st.thm.hille-yosida-contraction
- Anchor: st.thm.hille-yosida-contraction
- Phase: Current Bridge Agenda
- Score: 0.572
- Concept fertility: 0.8693
- Anchor concepts: c0-generation-implies-closed-dense-generator, closed-dense-plus-first-resolvent-bound-imply-contraction-generation, resolvent-approximants-converge-to-generated-semigroup, closed-dense-operator-with-first-resolvent-bound, resolvent-family-at-large-lambda
- Bridge concepts: c0-semigroup-definition, semigroup-generation, C0-semigroup-model, C0-semigroup, generator, unbounded-operator-domain-control, domain-closure-density, domain-regularity
- Abstraction concepts: domain-closure-density + unbounded-operator-domain-control evasive representation for closed-dense-operator-with-first-resolvent-bound, closed-dense-operator-with-first-resolvent-bound hitting-set or pseudorandom family, closed-dense-operator-with-first-resolvent-bound complexity potential in C0-semigroup-model, approximation-limit-control + domain-closure-density + unbounded-operator-domain-control evasive representation for closed-dense-operator-with-first-resolvent-bound, barrier + domain-closure-density + powers-of-resolvent-verification evasive representation for c0-generation-implies-closed-dense-generator, c0-generation-implies-closed-dense-generator hitting-set or pseudorandom family
- Definitional focus: realizes antecedent schema `c0-semigroup-definition`, forces target consequence `bounded-generator-approximation-scheme`, realizes antecedent schema `closed-dense-operator-with-resolvent-power-bounds`
- Counterfactual focus: Remove `realizes antecedent schema `c0-semigroup-definition`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `c0-semigroup-definition`, preserves `Yosida approximation convergence in C0-semigroup-model`, forces target consequence `bounded-generator-approximation-scheme`, Remove `realizes antecedent schema `closed-dense-operator-with-resolvent-power-bounds`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `closed-dense-operator-with-resolvent-power-bounds`, preserves `Yosida approximation convergence in resolvent-generation-criterion`, forces target consequence `bounded-generator-approximation-scheme`
- Bridges: bridge.007, bridge.008, bridge.009
- Hypotheses: phyp.hille-yosida-theorem.022, phyp.hille-yosida-theorem.007, phyp.hille-yosida-theorem.039, phyp.hille-yosida-theorem.008
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.3668, coherence_avg=0.0082
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.thm.hille-yosida-contraction and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.008 - Cross-Model Strategy around st.thm.lumer-phillips
- Anchor: st.thm.lumer-phillips
- Phase: Current Bridge Agenda
- Score: 0.5574
- Concept fertility: 0.8656
- Anchor concepts: closed-dense-plus-first-resolvent-bound-imply-contraction-generation, dissipativity-plus-range-condition-imply-contraction-generation, densely-defined-dissipative-operator-with-surjective-shift, closed-dense-operator-with-first-resolvent-bound, contraction-semigroup-via-dissipativity
- Bridge concepts: operator-theoretic-Banach-space, semigroup-generation, unbounded-operator, C0-semigroup-model, C0-semigroup, Banach-space, unbounded-generator-graph, unbounded-operator-domain-control
- Abstraction concepts: barrier + domain-closure-density + unbounded-operator-domain-control evasive representation for densely-defined-dissipative-operator-with-surjective-shift, densely-defined-dissipative-operator-with-surjective-shift hitting-set or pseudorandom family, densely-defined-dissipative-operator-with-surjective-shift complexity potential in C0-semigroup-model, approximation-limit-control + barrier + domain-closure-density evasive representation for densely-defined-dissipative-operator-with-surjective-shift
- Definitional focus: realizes antecedent schema `c0-semigroup-definition`, forces target consequence `contraction-semigroup-via-dissipativity`
- Counterfactual focus: Remove `realizes antecedent schema `c0-semigroup-definition`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `c0-semigroup-definition`, preserves `dissipative range-surjectivity criterion`, forces target consequence `contraction-semigroup-via-dissipativity`
- Bridges: bridge.005, bridge.006, bridge.013
- Hypotheses: phyp.hille-yosida-theorem.026, phyp.hille-yosida-theorem.005, phyp.hille-yosida-theorem.006, phyp.hille-yosida-theorem.037
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.3294, coherence_avg=0.0082
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.thm.lumer-phillips and restate objective as conditional entailment gain.
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
- global_coherence=0.5873
- tension=0.2484
- coherence_negative_hypotheses=1
- risk_mode=off
- top_abstraction_conjectures=conj.001:barrier-escaping-representation:approximation-limit-control + barrier + domain-closure-density evasive representation for closed-dense-operator-with-resolvent-power-bounds; conj.004:barrier-escaping-representation:barrier + domain-closure-density + powers-of-resolvent-verification evasive representation for closed-dense-operator-with-resolvent-power-bounds; conj.007:barrier-escaping-representation:unbounded-operator-domain-control evasive representation for closed-operator-or-semigroup-generator
- top_definitional_requirements=conj.001:realizes antecedent schema `c0-semigroup-definition`, forces target consequence `generator-of-exponentially-bounded-c0-semigroup`; conj.004:realizes antecedent schema `c0-semigroup-definition`, forces target consequence `generator-of-exponentially-bounded-c0-semigroup`; conj.007:realizes antecedent schema `c0-semigroup-definition`, forces target consequence `well-posed-abstract-cauchy-problem`
- top_counterfactual_probes=conj.001:Remove `realizes antecedent schema `c0-semigroup-definition`` from the candidate abstraction.; conj.004:Remove `realizes antecedent schema `c0-semigroup-definition`` from the candidate abstraction.; conj.007:Remove `realizes antecedent schema `c0-semigroup-definition`` from the candidate abstraction.
Top strategies:
1. strat.001 | anchor=st.thm.hille-yosida-general | phase=Current Bridge Agenda | score=0.7987 | fertility=0.8776
2. strat.002 | anchor=st.def.c0-semigroup | phase=Current Bridge Agenda | score=0.69 | fertility=0.9859
3. strat.003 | anchor=st.def.generator | phase=Current Bridge Agenda | score=0.6448 | fertility=0.9022
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
