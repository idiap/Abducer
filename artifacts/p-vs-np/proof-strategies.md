# Proof Strategy Portfolio

## Stats

- Strategies: 6
- Pathways used: 8
- Bridges used: 20
- Conjectured abstractions used: 0
- Hypotheses used: 44
- Coherence signals used: 44

## Strategies

| strategy_id | name | phase | anchor | score | fertility | anchor_concepts |
|---|---|---|---|---|---|---|
| strat.001 | Cross-Model Strategy around st.def.hardness-magnification-phenomenon-programme-leve | Current Bridge Agenda | st.def.hardness-magnification-phenomenon-programme-leve | 0.6964 | 0.5613 | mild-lower-bounds-imply-major-separation, nonuniform-circuit-exponential-lower-bound, MCSP-nonuniform-circuits-lower-bound, NP-not-in-P/poly |
| strat.002 | Cross-Model Strategy around st.thm.karp-many-natural-problems-are-np-complete-karp1 | Additional KB-Specific Phases | st.thm.karp-many-natural-problems-are-np-complete-karp1 | 0.6796 | 0.6425 | unconditional, NP-complete-classification, NP-completeness, many-one-reduction |
| strat.003 | Cross-Model Strategy around st.def.item-5 | Current Bridge Agenda | st.def.item-5 | 0.6074 | 0.5975 | nonuniform-circuit-lower-bound, lower-bound, nonuniform-circuits, E |
| strat.004 | Cross-Model Strategy around st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 | Additional KB-Specific Phases | st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 | 0.5859 | 0.5586 | poly-bounded-proofs-iff-NP-equals-coNP, poly-bounded-proof-system, TAUT-proof-system-characterization, NP-equals-coNP |
| strat.005 | Cross-Model Strategy around st.thm.oliveira-pich-santhanam-magnification-near-state | Current Bridge Agenda | st.thm.oliveira-pich-santhanam-magnification-near-state | 0.5484 | 0.5466 | mild-lower-bounds-imply-major-separation, MCSP-near-threshold-nonuniform-circuit-lower-bound, nonuniform-circuit-exponential-lower-bound, NP-not-in-P/poly |
| strat.006 | Cross-Model Strategy around st.thm.oliveira-santhanam-hardness-magnification-for-na | Current Bridge Agenda | st.thm.oliveira-santhanam-hardness-magnification-for-na | 0.5358 | 0.5568 | mild-lower-bounds-imply-major-separation, MCSP-near-threshold-nonuniform-circuit-lower-bound, nonuniform-circuit-superpolynomial-lower-bound, NP-not-in-P/poly |

### strat.001 - Cross-Model Strategy around st.def.hardness-magnification-phenomenon-programme-leve
- Anchor: st.def.hardness-magnification-phenomenon-programme-leve
- Phase: Current Bridge Agenda
- Score: 0.6964
- Concept fertility: 0.5613
- Anchor concepts: mild-lower-bounds-imply-major-separation, nonuniform-circuit-exponential-lower-bound, MCSP-nonuniform-circuits-lower-bound, NP-not-in-P/poly, major-separation
- Bridge concepts: nonuniform-circuit-exponential-lower-bound, mild-lower-bounds-imply-major-separation, NP-vs-P/poly-separation, NP-not-in-P/poly, MCSP-nonuniform-circuits-lower-bound, nonuniform-circuit-lower-bound, exponential-lower-bound, nonuniform-circuits
- Bridges: bridge.001, bridge.002, bridge.016
- Hypotheses: phyp.p-vs-np.001, phyp.p-vs-np.033, phyp.p-vs-np.002, phyp.p-vs-np.023
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.55, lemma_generation=0.25, abstraction_leverage=0.0, definitional_avg=0.0, counterfactual_avg=0.0, explanatory_avg=0.4094, coherence_avg=0.0104
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.hardness-magnification-phenomenon-programme-leve and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.002 - Cross-Model Strategy around st.thm.karp-many-natural-problems-are-np-complete-karp1
- Anchor: st.thm.karp-many-natural-problems-are-np-complete-karp1
- Phase: Additional KB-Specific Phases
- Score: 0.6796
- Concept fertility: 0.6425
- Anchor concepts: unconditional, NP-complete-classification, NP-completeness, many-one-reduction, E
- Bridge concepts: NP-complete-classification, completeness-framework, reduction-framework, algebraic-method, NP-completeness, NP
- Bridges: bridge.007, bridge.012
- Hypotheses: phyp.p-vs-np.007, phyp.p-vs-np.012, phyp.p-vs-np.039, phyp.p-vs-np.044
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.6, barrier_evasion=0.8, lemma_generation=0.5, abstraction_leverage=0.0, definitional_avg=0.0, counterfactual_avg=0.0, explanatory_avg=0.477, coherence_avg=0.0047
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.thm.karp-many-natural-problems-are-np-complete-karp1 and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.003 - Cross-Model Strategy around st.def.item-5
- Anchor: st.def.item-5
- Phase: Current Bridge Agenda
- Score: 0.6074
- Concept fertility: 0.5975
- Anchor concepts: nonuniform-circuit-lower-bound, lower-bound, nonuniform-circuits, E, P/poly
- Bridge concepts: nonuniform-circuit-lower-bound, nonuniform-circuits, P/poly, circuit-complexity, algebraic-method, lower-bound
- Bridges: bridge.004, bridge.005, bridge.017
- Hypotheses: phyp.p-vs-np.004, phyp.p-vs-np.005, phyp.p-vs-np.036, phyp.p-vs-np.017
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.7, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.0, definitional_avg=0.0, counterfactual_avg=0.0, explanatory_avg=0.3953, coherence_avg=0.0121
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.def.item-5 and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.004 - Cross-Model Strategy around st.thm.cook-reckhow-proof-systems-and-cookreckhow1979
- Anchor: st.thm.cook-reckhow-proof-systems-and-cookreckhow1979
- Phase: Additional KB-Specific Phases
- Score: 0.5859
- Concept fertility: 0.5586
- Anchor concepts: poly-bounded-proofs-iff-NP-equals-coNP, poly-bounded-proof-system, TAUT-proof-system-characterization, NP-equals-coNP, proof-system-characterization
- Bridge concepts: TAUT-proof-system-characterization, TAUT, proof-system-characterization, Cook-Reckhow-proof-system, proof-complexity, algebraic-method
- Bridges: bridge.003, bridge.023
- Hypotheses: phyp.p-vs-np.003, phyp.p-vs-np.035, phyp.p-vs-np.030
- Fertility components: unification_gain=0.375, proof_compression=0.6, transfer_power=0.5333, barrier_evasion=0.7333, lemma_generation=0.3333, abstraction_leverage=0.0, definitional_avg=0.0, counterfactual_avg=0.0, explanatory_avg=0.4116, coherence_avg=0.004
- Hypothesis status summary: unresolved=3
- Execution protocol:
  - Anchor on st.thm.cook-reckhow-proof-systems-and-cookreckhow1979 and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.005 - Cross-Model Strategy around st.thm.oliveira-pich-santhanam-magnification-near-state
- Anchor: st.thm.oliveira-pich-santhanam-magnification-near-state
- Phase: Current Bridge Agenda
- Score: 0.5484
- Concept fertility: 0.5466
- Anchor concepts: mild-lower-bounds-imply-major-separation, MCSP-near-threshold-nonuniform-circuit-lower-bound, nonuniform-circuit-exponential-lower-bound, NP-not-in-P/poly, major-separation
- Bridge concepts: nonuniform-circuit-exponential-lower-bound, mild-lower-bounds-imply-major-separation, NP-vs-P/poly-separation, NP-not-in-P/poly, MCSP-nonuniform-circuits-lower-bound, nonuniform-circuit-lower-bound, MCSP-near-threshold-nonuniform-circuit-lower-bound, near-threshold-lower-bound
- Bridges: bridge.001, bridge.010
- Hypotheses: phyp.p-vs-np.001, phyp.p-vs-np.033, phyp.p-vs-np.022, phyp.p-vs-np.010
- Fertility components: unification_gain=0.375, proof_compression=0.6667, transfer_power=0.5, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.0, definitional_avg=0.0, counterfactual_avg=0.0, explanatory_avg=0.4065, coherence_avg=0.014
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.thm.oliveira-pich-santhanam-magnification-near-state and restate objective as conditional entailment gain.
  - Run kb-abduce with hypothesis seeds from `hypothesis_ids`.
  - Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.
  - Retain only assumptions that increase derivable consequences without contradiction.
  - Record deltas and feed surviving artifacts to next strategy round.

### strat.006 - Cross-Model Strategy around st.thm.oliveira-santhanam-hardness-magnification-for-na
- Anchor: st.thm.oliveira-santhanam-hardness-magnification-for-na
- Phase: Current Bridge Agenda
- Score: 0.5358
- Concept fertility: 0.5568
- Anchor concepts: mild-lower-bounds-imply-major-separation, MCSP-near-threshold-nonuniform-circuit-lower-bound, nonuniform-circuit-superpolynomial-lower-bound, NP-not-in-P/poly, major-separation
- Bridge concepts: mild-lower-bounds-imply-major-separation, NP-vs-P/poly-separation, NP-not-in-P/poly, nonuniform-circuit-lower-bound, exponential-lower-bound, nonuniform-circuits, MCSP-near-threshold-nonuniform-circuit-lower-bound, near-threshold-lower-bound
- Bridges: bridge.002, bridge.010
- Hypotheses: phyp.p-vs-np.021, phyp.p-vs-np.002, phyp.p-vs-np.034, phyp.p-vs-np.010
- Fertility components: unification_gain=0.5, proof_compression=0.5714, transfer_power=0.5, barrier_evasion=0.7, lemma_generation=0.25, abstraction_leverage=0.0, definitional_avg=0.0, counterfactual_avg=0.0, explanatory_avg=0.3933, coherence_avg=0.007
- Hypothesis status summary: unresolved=4
- Execution protocol:
  - Anchor on st.thm.oliveira-santhanam-hardness-magnification-for-na and restate objective as conditional entailment gain.
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
- global_coherence=0.3133
- tension=0.7324
- coherence_negative_hypotheses=2
- risk_mode=on
- top_abstraction_conjectures=none
- top_definitional_requirements=none
- top_counterfactual_probes=none
Top strategies:
1. strat.001 | anchor=st.def.hardness-magnification-phenomenon-programme-leve | phase=Current Bridge Agenda | score=0.6964 | fertility=0.5613
2. strat.002 | anchor=st.thm.karp-many-natural-problems-are-np-complete-karp1 | phase=Additional KB-Specific Phases | score=0.6796 | fertility=0.6425
3. strat.003 | anchor=st.def.item-5 | phase=Current Bridge Agenda | score=0.6074 | fertility=0.5975
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
