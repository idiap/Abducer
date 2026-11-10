# Proof Strategy Portfolio

## Stats

- Strategies: 6
- Pathways used: 8
- Bridges used: 20
- Conjectured abstractions used: 34
- Hypotheses used: 44
- Coherence signals used: 44

## Strategies

| strategy_id | name | phase | anchor | score | fertility | anchor_concepts |
|---|---|---|---|---|---|---|
| strat.001 | Cross-Model Strategy around st.def.os-euclidean-qft | Current Bridge Agenda | st.def.os-euclidean-qft | 0.7615 | 0.8936 | OS-axioms-imply-Wightman-QFT, reflection-positivity-and-transfer-matrix, OS-axioms-and-reflection-positivity, positive-self-adjoint-Hamiltonian |
| strat.002 | Cross-Model Strategy around st.def.compact-simple-gauge-group | Foundational Gauge-Theoretic Definitions | st.def.compact-simple-gauge-group | 0.6773 | 0.5992 | compact-simple-gauge-group, Yang-Mills, gauge-theory, geometric-analysis |
| strat.003 | Cross-Model Strategy around st.def.wightman-qft | Current Bridge Agenda | st.def.wightman-qft | 0.6675 | 0.8738 | rigorous-Yang-Mills-construction, constructive-existence, Hamiltonian-mass-gap, Wightman-QFT |
| strat.004 | Cross-Model Strategy around st.thm.reflection-positivity-and-transfer-matrix-for-la | Mass-Gap and Spectral Transfer | st.thm.reflection-positivity-and-transfer-matrix-for-la | 0.6562 | 0.6694 | lattice-continuum-control-implies-constructive-QFT, transfer-matrix-gap-implies-correlator-decay, reflection-positivity-and-transfer-matrix, OS-axioms-and-reflection-positivity |
| strat.005 | Cross-Model Strategy around st.def.mass-gap | Current Bridge Agenda | st.def.mass-gap | 0.6491 | 0.8946 | transfer-matrix-gap-implies-correlator-decay, correlator-decay-signals-mass-gap, reflection-positivity-and-transfer-matrix, positive-self-adjoint-Hamiltonian |
| strat.006 | Cross-Model Strategy around st.thm.os-reconstruction-and-equivalence-with-wightman- | Current Bridge Agenda | st.thm.os-reconstruction-and-equivalence-with-wightman- | 0.6084 | 0.8672 | lattice-continuum-control-implies-constructive-QFT, OS-axioms-imply-Wightman-QFT, reflection-positivity-and-transfer-matrix, OS-axioms-and-reflection-positivity |

### strat.001 - Cross-Model Strategy around st.def.os-euclidean-qft
- Anchor: st.def.os-euclidean-qft
- Phase: Current Bridge Agenda
- Score: 0.7615
- Concept fertility: 0.8936
- Anchor concepts: OS-axioms-imply-Wightman-QFT, reflection-positivity-and-transfer-matrix, OS-axioms-and-reflection-positivity, positive-self-adjoint-Hamiltonian, rigorous-Yang-Mills-construction
- Bridge concepts: reflection-positivity-and-transfer-matrix, reflection-positive-transfer-matrix, OS-axioms-and-reflection-positivity, positive-self-adjoint-Hamiltonian, rigorous-Yang-Mills-construction, reflection-positivity-transfer
- Abstraction concepts: continuum-limit evasive representation for reflection-positivity-and-transfer-matrix, reflection-positivity-and-transfer-matrix continuum-limit construction in OS-Euclidean-QFT, reflection-positivity-and-transfer-matrix mass-gap witness transfer, reflection-positivity-and-transfer-matrix OS reconstruction interface, reflection-positivity-and-transfer-matrix normal-form translation across OS-Euclidean-QFT
- Definitional focus: realizes antecedent schema `reflection-positivity-and-transfer-matrix`, forces target consequence `positive-self-adjoint-Hamiltonian`
- Counterfactual focus: Remove `realizes antecedent schema `reflection-positivity-and-transfer-matrix`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `reflection-positivity-and-transfer-matrix`, preserves `OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap`, forces target consequence `positive-self-adjoint-Hamiltonian`, Assume the first sufficient attribute set is fully realized: realizes antecedent schema `reflection-positivity-and-transfer-matrix`, preserves `correlator-decay mass-gap witness in Schwinger-function-decay`, forces target consequence `positive-self-adjoint-Hamiltonian`, Assume the first sufficient attribute set is fully realized: realizes antecedent schema `reflection-positivity-and-transfer-matrix`, preserves `OS-to-Wightman mass-gap transfer in Wightman-QFT`, forces target consequence `positive-self-adjoint-Hamiltonian`
- Bridges: bridge.001, bridge.003, bridge.009
- Hypotheses: phyp.yang-mills-existence-and-mass-gap.021, phyp.yang-mills-existence-and-mass-gap.001, phyp.yang-mills-existence-and-mass-gap.003, phyp.yang-mills-existence-and-mass-gap.033
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=1.0, definitional_avg=0.985, counterfactual_avg=1.0, explanatory_avg=0.3788, coherence_avg=0.0047
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.os-euclidean-qft and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.002 - Cross-Model Strategy around st.def.compact-simple-gauge-group
- Anchor: st.def.compact-simple-gauge-group
- Phase: Foundational Gauge-Theoretic Definitions
- Score: 0.6773
- Concept fertility: 0.5992
- Anchor concepts: compact-simple-gauge-group, Yang-Mills, gauge-theory, geometric-analysis
- Bridge concepts: geometric-analysis, gauge-theory, Yang-Mills, compact-simple-gauge-group
- Bridges: bridge.002, bridge.007, bridge.008
- Hypotheses: phyp.yang-mills-existence-and-mass-gap.002, phyp.yang-mills-existence-and-mass-gap.007, phyp.yang-mills-existence-and-mass-gap.008, phyp.yang-mills-existence-and-mass-gap.034
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.0, definitional_avg=0.0, counterfactual_avg=0.0, explanatory_avg=0.4125, coherence_avg=0.0116
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.compact-simple-gauge-group and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.003 - Cross-Model Strategy around st.def.wightman-qft
- Anchor: st.def.wightman-qft
- Phase: Current Bridge Agenda
- Score: 0.6675
- Concept fertility: 0.8738
- Anchor concepts: rigorous-Yang-Mills-construction, constructive-existence, Hamiltonian-mass-gap, Wightman-QFT, classical-Yang-Mills-PDE
- Bridge concepts: rigorous-Yang-Mills-construction, constructive-existence, Hamiltonian-mass-gap, constructive-qft, axiomatic-qft, Wightman-QFT, classical-Yang-Mills-PDE, classical-pde-analysis
- Abstraction concepts: ultraviolet-control evasive representation for Hamiltonian-mass-gap, Hamiltonian-mass-gap continuum-limit construction in Hamiltonian-mass-gap, Hamiltonian-mass-gap mass-gap witness transfer, continuum-limit evasive representation for reflection-positivity-and-transfer-matrix, reflection-positivity-and-transfer-matrix continuum-limit construction in Hamiltonian-mass-gap, reflection-positivity-and-transfer-matrix mass-gap witness transfer, open-construction-gap + ultraviolet-control evasive representation for Hamiltonian-mass-gap
- Definitional focus: realizes antecedent schema `constructive-existence`, forces target consequence `rigorous-Yang-Mills-construction`, forces target consequence `positive-self-adjoint-Hamiltonian`
- Counterfactual focus: Remove `realizes antecedent schema `constructive-existence`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `constructive-existence`, preserves `OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap`, forces target consequence `rigorous-Yang-Mills-construction`, Assume the first sufficient attribute set is fully realized: realizes antecedent schema `constructive-existence`, preserves `OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap`, forces target consequence `positive-self-adjoint-Hamiltonian`
- Bridges: bridge.004, bridge.005, bridge.011
- Hypotheses: phyp.yang-mills-existence-and-mass-gap.026, phyp.yang-mills-existence-and-mass-gap.004, phyp.yang-mills-existence-and-mass-gap.005, phyp.yang-mills-existence-and-mass-gap.036
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.4119, coherence_avg=0.0083
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.wightman-qft and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.004 - Cross-Model Strategy around st.thm.reflection-positivity-and-transfer-matrix-for-la
- Anchor: st.thm.reflection-positivity-and-transfer-matrix-for-la
- Phase: Mass-Gap and Spectral Transfer
- Score: 0.6562
- Concept fertility: 0.6694
- Anchor concepts: lattice-continuum-control-implies-constructive-QFT, transfer-matrix-gap-implies-correlator-decay, reflection-positivity-and-transfer-matrix, OS-axioms-and-reflection-positivity, multiscale-renormalization-control
- Bridge concepts: reflection-positivity-and-transfer-matrix, reflection-positive-transfer-matrix, OS-axioms-and-reflection-positivity, positive-self-adjoint-Hamiltonian, rigorous-Yang-Mills-construction, reflection-positivity-transfer
- Abstraction concepts: continuum-limit evasive representation for reflection-positivity-and-transfer-matrix, reflection-positivity-and-transfer-matrix continuum-limit construction in OS-Euclidean-QFT, reflection-positivity-and-transfer-matrix mass-gap witness transfer
- Definitional focus: realizes antecedent schema `reflection-positivity-and-transfer-matrix`, forces target consequence `positive-self-adjoint-Hamiltonian`
- Counterfactual focus: Remove `realizes antecedent schema `reflection-positivity-and-transfer-matrix`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `reflection-positivity-and-transfer-matrix`, preserves `transfer-matrix spectral witness in reflection-positive-transfer-matrix`, provides an explicit transfer law or reduction mechanism, forces target consequence `positive-self-adjoint-Hamiltonian`
- Bridges: bridge.016
- Hypotheses: phyp.yang-mills-existence-and-mass-gap.027, phyp.yang-mills-existence-and-mass-gap.016
- Fertility components: unification_gain=0.5, proof_compression=0.4, transfer_power=0.2, barrier_evasion=0.6, lemma_generation=0.0, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.2885, coherence_avg=0.0053
- Hypothesis status summary: unresolved=2
- Execution protocol:
  - Anchor on st.thm.reflection-positivity-and-transfer-matrix-for-la and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.005 - Cross-Model Strategy around st.def.mass-gap
- Anchor: st.def.mass-gap
- Phase: Current Bridge Agenda
- Score: 0.6491
- Concept fertility: 0.8946
- Anchor concepts: transfer-matrix-gap-implies-correlator-decay, correlator-decay-signals-mass-gap, reflection-positivity-and-transfer-matrix, positive-self-adjoint-Hamiltonian, rigorous-Yang-Mills-construction
- Bridge concepts: transfer-matrix-gap-implies-correlator-decay, exponential-correlation-decay, reflection-positivity-and-transfer-matrix, reflection-positive-transfer-matrix, positive-self-adjoint-Hamiltonian, correlator-decay-signals-mass-gap, rigorous-Yang-Mills-construction, reflection-positivity-transfer
- Abstraction concepts: continuum-limit evasive representation for transfer-matrix-gap-implies-correlator-decay, transfer-matrix-gap-implies-correlator-decay continuum-limit construction in Hamiltonian-mass-gap, transfer-matrix-gap-implies-correlator-decay mass-gap witness transfer, transfer-matrix-gap-implies-correlator-decay OS reconstruction interface, continuum-limit evasive representation for reflection-positivity-and-transfer-matrix, reflection-positivity-and-transfer-matrix continuum-limit construction in Hamiltonian-mass-gap
- Definitional focus: realizes antecedent schema `reflection-positivity-and-transfer-matrix`, forces target consequence `positive-self-adjoint-Hamiltonian`
- Counterfactual focus: Remove `realizes antecedent schema `reflection-positivity-and-transfer-matrix`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `reflection-positivity-and-transfer-matrix`, preserves `transfer-matrix spectral witness in reflection-positive-transfer-matrix`, provides an explicit transfer law or reduction mechanism, forces target consequence `positive-self-adjoint-Hamiltonian`
- Bridges: bridge.006, bridge.012, bridge.014
- Hypotheses: phyp.yang-mills-existence-and-mass-gap.022, phyp.yang-mills-existence-and-mass-gap.006, phyp.yang-mills-existence-and-mass-gap.038, phyp.yang-mills-existence-and-mass-gap.012
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=1.0, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.3702, coherence_avg=0.0076
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.mass-gap and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.006 - Cross-Model Strategy around st.thm.os-reconstruction-and-equivalence-with-wightman-
- Anchor: st.thm.os-reconstruction-and-equivalence-with-wightman-
- Phase: Current Bridge Agenda
- Score: 0.6084
- Concept fertility: 0.8672
- Anchor concepts: lattice-continuum-control-implies-constructive-QFT, OS-axioms-imply-Wightman-QFT, reflection-positivity-and-transfer-matrix, OS-axioms-and-reflection-positivity, multiscale-renormalization-control
- Bridge concepts: reflection-positivity-and-transfer-matrix, reflection-positive-transfer-matrix, OS-axioms-and-reflection-positivity, positive-self-adjoint-Hamiltonian, rigorous-Yang-Mills-construction, reflection-positivity-transfer, classical-Yang-Mills-PDE, constructive-existence
- Abstraction concepts: continuum-limit evasive representation for reflection-positivity-and-transfer-matrix, reflection-positivity-and-transfer-matrix continuum-limit construction in OS-Euclidean-QFT, reflection-positivity-and-transfer-matrix mass-gap witness transfer, reflection-positivity-and-transfer-matrix continuum-limit construction in Hamiltonian-mass-gap
- Definitional focus: realizes antecedent schema `reflection-positivity-and-transfer-matrix`, forces target consequence `positive-self-adjoint-Hamiltonian`, realizes antecedent schema `constructive-existence`
- Counterfactual focus: Remove `realizes antecedent schema `reflection-positivity-and-transfer-matrix`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `reflection-positivity-and-transfer-matrix`, preserves `OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap`, forces target consequence `positive-self-adjoint-Hamiltonian`, Remove `realizes antecedent schema `constructive-existence`` from the candidate abstraction., Assume the first sufficient attribute set is fully realized: realizes antecedent schema `constructive-existence`, preserves `OS-to-Wightman mass-gap transfer in Hamiltonian-mass-gap`, forces target consequence `positive-self-adjoint-Hamiltonian`
- Bridges: bridge.001, bridge.005, bridge.014
- Hypotheses: phyp.yang-mills-existence-and-mass-gap.001, phyp.yang-mills-existence-and-mass-gap.025, phyp.yang-mills-existence-and-mass-gap.005, phyp.yang-mills-existence-and-mass-gap.033
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.75, definitional_avg=1.0, counterfactual_avg=1.0, explanatory_avg=0.3487, coherence_avg=0.0058
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.thm.os-reconstruction-and-equivalence-with-wightman- and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

## Novelty-Maximizing Prompt

```text
You are a proof-strategy synthesizer optimizing novelty under rigor constraints.
Inputs: KB slice, ranked strategies, bridge programs, hypothesis sets, coherence diagnostics.
Objective: maximize expected proof progress while maximizing conceptual novelty.
Novelty score N = 0.30*phase_diversity + 0.22*bridge_originality + 0.18*hypothesis_nonredundancy + 0.10*minimal_assumption_gain + 0.20*coherence_preservation.
Live diagnostics:
- global_coherence=0.3200
- tension=0.7788
- coherence_negative_hypotheses=0
- risk_mode=on
- top_abstraction_conjectures=conj.009:barrier-escaping-representation:continuum-limit evasive representation for transfer-matrix-gap-implies-correlator-decay; conj.003:barrier-escaping-representation:continuum-limit evasive representation for reflection-positivity-and-transfer-matrix; conj.012:barrier-escaping-representation:continuum-limit evasive representation for reflection-positivity-and-transfer-matrix
- top_definitional_requirements=conj.009:realizes antecedent schema `reflection-positivity-and-transfer-matrix`, forces target consequence `positive-self-adjoint-Hamiltonian`; conj.003:realizes antecedent schema `reflection-positivity-and-transfer-matrix`, forces target consequence `positive-self-adjoint-Hamiltonian`; conj.012:realizes antecedent schema `reflection-positivity-and-transfer-matrix`, forces target consequence `positive-self-adjoint-Hamiltonian`
- top_counterfactual_probes=conj.009:Remove `realizes antecedent schema `reflection-positivity-and-transfer-matrix`` from the candidate abstraction.; conj.003:Remove `realizes antecedent schema `reflection-positivity-and-transfer-matrix`` from the candidate abstraction.; conj.012:Remove `realizes antecedent schema `reflection-positivity-and-transfer-matrix`` from the candidate abstraction.
Top strategies:
1. strat.001 | anchor=st.def.os-euclidean-qft | phase=Current Bridge Agenda | score=0.7615 | fertility=0.8936
2. strat.002 | anchor=st.def.compact-simple-gauge-group | phase=Foundational Gauge-Theoretic Definitions | score=0.6773 | fertility=0.5992
3. strat.003 | anchor=st.def.wightman-qft | phase=Current Bridge Agenda | score=0.6675 | fertility=0.8738
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
