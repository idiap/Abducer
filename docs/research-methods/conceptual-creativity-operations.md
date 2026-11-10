<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Conceptual Creativity Operations

Abducer treats conceptual creativity as a typed transformation over the hypothesis exploration map. A move is creative only when it changes route options and creates validation obligations.

| Operation | Produces | Validation pressure |
| --- | --- | --- |
| `bridge_invention` | relation, map, invariant, mediator | preservation, non_collapse, source_grounding, proof_queue_readiness |
| `abstraction_formation` | reusable_concept, route_family, compressed_proof_shape | coverage_witness, excluded_cases, entailment_gap |
| `regime_restriction` | narrowed_conjecture, parameter_slice, assumption_slice | lost_generality, route_value, counterfactual_route |
| `theorem_weakening` | weaker_successor_claim, testable_subclaim | parent_relevance, no_hidden_promotion, proof_readiness |
| `theorem_strengthening` | sharper_claim, extra_invariant | barrier_compatibility, stress_test, source_grounding |
| `carrier_introduction` | new_object, state_space, witness_family | definition_sufficiency, construction_evidence, downstream_fit |
| `negative_route_inversion` | failure_derived_hypothesis, counterexample_guided_route | failure_certificate_fidelity, repair_target_specificity |
| `analogy_transport` | transported_pattern, source_target_mapping | source_domain_limits, mismatch_inventory, non_collapse |
| `proof_obligation_factorization` | smaller_lemma, evidence_task, discovery_branch | dependency_graph_update, stop_condition_preservation |
| `representation_shift` | ontology_revision, new_vocabulary, route_reencoding | revision_trace, backward_compatibility, rejected_alternatives |

## Validation Rule

No creative operation can promote itself. It must pass through a validation packet, candidate ranking, Looper graph edge, and release evidence. Missing source grounding or unnamed hard obligations force quarantine or rejection.
