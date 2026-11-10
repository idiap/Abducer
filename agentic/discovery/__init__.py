# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Typed, replayable foundations for Abducer's discovery runtime.

Only the dependency-light contract primitives are imported eagerly.  All
higher-level surfaces are resolved lazily so an experiment adapter can depend
on budgets/contracts without importing the canonical cycle, which itself
depends on the experiment package.
"""

from importlib import import_module
from typing import Any

from .contracts import ContractError, Namespace, canonical_digest, canonical_json


_LAZY_EXPORTS: dict[str, tuple[str, str]] = {
    "AUTHORITY_BOUNDARY": (".cycle", "AUTHORITY_BOUNDARY"),
    "BASE_DOMINANCE_DIMENSIONS": (
        ".open_world_creativity",
        "BASE_DOMINANCE_DIMENSIONS",
    ),
    "CONTROL_KINDS": (".open_world_creativity", "CONTROL_KINDS"),
    "DEEP_REFLECTION_LENSES": (
        ".open_world_creativity",
        "DEEP_REFLECTION_LENSES",
    ),
    "MERIT_DIMENSIONS": (".open_world_creativity", "MERIT_DIMENSIONS"),
    "AggressiveProviderSearchError": (
        ".aggressive_provider_search",
        "AggressiveProviderSearchError",
    ),
    "ConceptualFrontierDeepeningError": (
        ".conceptual_frontier_deepening",
        "ConceptualFrontierDeepeningError",
    ),
    "LiteratureConditionedInventionError": (
        ".literature_conditioned_invention",
        "LiteratureConditionedInventionError",
    ),
    "RouteNeutralSemanticEvaluationError": (
        ".route_neutral_semantic_evaluation",
        "RouteNeutralSemanticEvaluationError",
    ),
    "CentralConceptualReflectionError": (
        ".central_conceptual_reflection",
        "CentralConceptualReflectionError",
    ),
    "OpenWorldCreativityError": (
        ".open_world_creativity",
        "OpenWorldCreativityError",
    ),
    "bind_branch_terminal_receipt": (
        ".open_world_creativity",
        "bind_branch_terminal_receipt",
    ),
    "build_branch_intent_manifest": (
        ".open_world_creativity",
        "build_branch_intent_manifest",
    ),
    "build_aggressive_provider_search_request": (
        ".aggressive_provider_search",
        "build_aggressive_provider_search_request",
    ),
    "build_central_conceptual_reflection_request": (
        ".central_conceptual_reflection",
        "build_central_conceptual_reflection_request",
    ),
    "build_central_conceptual_reflection_commit_binding": (
        ".central_conceptual_reflection",
        "build_central_conceptual_reflection_commit_binding",
    ),
    "build_central_conceptual_reflection_intake_claim": (
        ".central_conceptual_reflection",
        "build_central_conceptual_reflection_intake_claim",
    ),
    "build_central_conceptual_route_reflection_intake": (
        ".central_conceptual_reflection",
        "build_central_conceptual_route_reflection_intake",
    ),
    "build_bounded_current_literature_bundle": (
        ".conceptual_ancestry_v3",
        "build_bounded_current_literature_bundle",
    ),
    "build_conceptual_ancestry_literature_basis": (
        ".conceptual_ancestry_v3",
        "build_conceptual_ancestry_literature_basis",
    ),
    "build_conceptual_ancestry_literature_projection": (
        ".conceptual_ancestry_v3",
        "build_conceptual_ancestry_literature_projection",
    ),
    "build_conceptual_ancestry_v3": (
        ".conceptual_ancestry_v3",
        "build_conceptual_ancestry_v3",
    ),
    "build_literature_conditioned_invention_freeze": (
        ".conceptual_ancestry_v3",
        "build_literature_conditioned_invention_freeze",
    ),
    "build_literature_conditioned_invention_execution": (
        ".literature_conditioned_invention",
        "build_literature_conditioned_invention_execution",
    ),
    "build_literature_conditioned_invention_request": (
        ".literature_conditioned_invention",
        "build_literature_conditioned_invention_request",
    ),
    "build_literature_counterfactual_inputs": (
        ".literature_conditioned_invention",
        "build_literature_counterfactual_inputs",
    ),
    "build_committed_route_input": (
        ".central_conceptual_routes_v3",
        "build_committed_route_input",
    ),
    "build_hidden_elicitation_prompt": (
        ".hypotheses",
        "build_hidden_elicitation_prompt",
    ),
    "build_non_saturating_conceptual_merit_evaluation": (
        ".open_world_creativity",
        "build_non_saturating_conceptual_merit_evaluation",
    ),
    "build_open_world_hard_integrity_receipt": (
        ".open_world_creativity",
        "build_open_world_hard_integrity_receipt",
    ),
    "build_open_world_maturation_portfolio": (
        ".open_world_creativity",
        "build_open_world_maturation_portfolio",
    ),
    "build_parallel_maturation_barrier_receipt": (
        ".open_world_creativity",
        "build_parallel_maturation_barrier_receipt",
    ),
    "build_pre_taxonomy_invention_freeze": (
        ".open_world_creativity",
        "build_pre_taxonomy_invention_freeze",
    ),
    "build_route_neutral_frontier_candidates": (
        ".conceptual_frontier_deepening",
        "build_route_neutral_frontier_candidates",
    ),
    "build_target_predeclared_coverage_problem": (
        ".aggressive_provider_search",
        "build_target_predeclared_coverage_problem",
    ),
    "classify_frozen_inventions": (
        ".open_world_creativity",
        "classify_frozen_inventions",
    ),
    "build_proof_handoff": (".proof", "build_proof_handoff"),
    "build_postcommit_proof_handoff": (
        ".proof",
        "build_postcommit_proof_handoff",
    ),
    "ProofPrelaunchCapability": (
        ".proof",
        "ProofPrelaunchCapability",
    ),
    "ProofV3ActionResult": (
        ".proof_v3_facade",
        "ProofV3ActionResult",
    ),
    "committed_cycle_projection_artifact_paths": (
        ".committed_projection",
        "committed_cycle_projection_artifact_paths",
    ),
    "consume_action": (".scheduler", "consume_action"),
    "consume_action_transaction": (".scheduler", "consume_action_transaction"),
    "consume_proof_result_v3": (
        ".proof_v3_facade",
        "consume_proof_result_v3",
    ),
    "consume_committed_central_conceptual_route_reflection_intake": (
        ".central_conceptual_reflection",
        "consume_committed_central_conceptual_route_reflection_intake",
    ),
    "evaluate_discovery_delta": (".evaluation", "evaluate_discovery_delta"),
    "execute_proof_v3": (".proof_v3_facade", "execute_proof_v3"),
    "derive_committed_cycle_world_authority_projection": (
        ".committed_projection",
        "derive_committed_cycle_world_authority_projection",
    ),
    "decode_central_conceptual_reflection_request": (
        ".central_conceptual_reflection",
        "decode_central_conceptual_reflection_request",
    ),
    "decode_central_conceptual_route_reflection_intake": (
        ".central_conceptual_reflection",
        "decode_central_conceptual_route_reflection_intake",
    ),
    "decode_central_conceptual_route_packet": (
        ".central_conceptual_routes_v3",
        "decode_central_conceptual_route_packet",
    ),
    "load_committed_cycle_projection_sources": (
        ".committed_projection",
        "load_committed_cycle_projection_sources",
    ),
    "load_formal_lens_producer_registry": (
        ".formal_lens_registry",
        "load_formal_lens_producer_registry",
    ),
    "reopen_current_proof_handoff": (
        ".proof",
        "reopen_current_proof_handoff",
    ),
    "reopen_consumed_proof_result_v3": (
        ".proof_v3_facade",
        "reopen_consumed_proof_result_v3",
    ),
    "recover_central_conceptual_reflection_intake_claim": (
        ".central_conceptual_reflection",
        "recover_central_conceptual_reflection_intake_claim",
    ),
    "reopen_authoritative_central_conceptual_route_packet": (
        ".central_conceptual_routes_v3",
        "reopen_authoritative_central_conceptual_route_packet",
    ),
    "issue_proof_prelaunch_capability": (
        ".proof",
        "issue_proof_prelaunch_capability",
    ),
    "known_taxonomy_commitment": (
        ".open_world_creativity",
        "known_taxonomy_commitment",
    ),
    "migrate_seed_free_high_risk_elicitation_v1": (
        ".hypotheses",
        "migrate_seed_free_high_risk_elicitation_v1",
    ),
    "replay_proposal_field_free_high_risk_elicitation": (
        ".hypotheses",
        "replay_proposal_field_free_high_risk_elicitation",
    ),
    "replay_seed_free_high_risk_elicitation": (
        ".hypotheses",
        "replay_seed_free_high_risk_elicitation",
    ),
    "prepare_blinded_conceptual_merit_packet": (
        ".open_world_creativity",
        "prepare_blinded_conceptual_merit_packet",
    ),
    "run_isolated_parallel_maturation_branches": (
        ".open_world_creativity",
        "run_isolated_parallel_maturation_branches",
    ),
    "run_canonical_discovery_cycle": (".cycle", "run_canonical_discovery_cycle"),
    "run_aggressive_provider_search": (
        ".aggressive_provider_search",
        "run_aggressive_provider_search",
    ),
    "run_bounded_killable_request_wave": (
        ".parallel",
        "run_bounded_killable_request_wave",
    ),
    "run_central_conceptual_routes": (
        ".central_conceptual_routes_v3",
        "run_central_conceptual_routes",
    ),
    "run_conceptual_frontier_deepening": (
        ".conceptual_frontier_deepening",
        "run_conceptual_frontier_deepening",
    ),
    "run_registered_corner_impossibility_assessment": (
        ".conceptual_ancestry_v3",
        "run_registered_corner_impossibility_assessment",
    ),
    "run_literature_invention_counterfactual_study": (
        ".literature_conditioned_invention",
        "run_literature_invention_counterfactual_study",
    ),
    "run_registered_literature_conditioned_invention": (
        ".literature_conditioned_invention",
        "run_registered_literature_conditioned_invention",
    ),
    "run_committed_proof_action_v3": (
        ".proof_v3_facade",
        "run_committed_proof_action_v3",
    ),
    "reconcile_committed_proof_action_v3": (
        ".proof_v3_facade",
        "reconcile_committed_proof_action_v3",
    ),
    "run_formal_lens_production": (
        ".formal_lens_production",
        "run_formal_lens_production",
    ),
    "run_parallel_hypothesis_portfolio": (
        ".parallel",
        "run_parallel_hypothesis_portfolio",
    ),
    "run_route_neutral_semantic_evaluation": (
        ".route_neutral_semantic_evaluation",
        "run_route_neutral_semantic_evaluation",
    ),
    "proof_prelaunch_capability_projection": (
        ".proof",
        "proof_prelaunch_capability_projection",
    ),
    "run_proposal_field_free_high_risk_elicitation": (
        ".hypotheses",
        "run_proposal_field_free_high_risk_elicitation",
    ),
    "run_seed_free_high_risk_elicitation": (
        ".hypotheses",
        "run_seed_free_high_risk_elicitation",
    ),
    "replay_committed_cycle_world_authority_projection": (
        ".committed_projection",
        "replay_committed_cycle_world_authority_projection",
    ),
    "schedule_discovery_actions": (".scheduler", "schedule_discovery_actions"),
    "seal_merit_evaluator_report": (
        ".open_world_creativity",
        "seal_merit_evaluator_report",
    ),
    "seal_semantic_evidence": (
        ".route_neutral_semantic_evaluation",
        "seal_semantic_evidence",
    ),
    "semantic_hypothesis_signature": (
        ".hypotheses",
        "semantic_hypothesis_signature",
    ),
    "validate_evaluation_receipt": (
        ".evaluation",
        "validate_evaluation_receipt",
    ),
    "validate_aggressive_provider_search_execution": (
        ".aggressive_provider_search",
        "validate_aggressive_provider_search_execution",
    ),
    "validate_authoritative_central_conceptual_reflection_request": (
        ".central_conceptual_reflection",
        "validate_authoritative_central_conceptual_reflection_request",
    ),
    "validate_active_prefix_central_conceptual_reflection_request": (
        ".central_conceptual_reflection",
        "validate_active_prefix_central_conceptual_reflection_request",
    ),
    "validate_central_conceptual_reflection_consumption_receipt": (
        ".central_conceptual_reflection",
        "validate_central_conceptual_reflection_consumption_receipt",
    ),
    "validate_bounded_current_literature_bundle": (
        ".conceptual_ancestry_v3",
        "validate_bounded_current_literature_bundle",
    ),
    "validate_conceptual_ancestry_cycle_binding": (
        ".conceptual_ancestry_v3",
        "validate_conceptual_ancestry_cycle_binding",
    ),
    "validate_conceptual_ancestry_v3": (
        ".conceptual_ancestry_v3",
        "validate_conceptual_ancestry_v3",
    ),
    "validate_literature_conditioned_invention_execution": (
        ".literature_conditioned_invention",
        "validate_literature_conditioned_invention_execution",
    ),
    "validate_conceptual_frontier_deepening": (
        ".conceptual_frontier_deepening",
        "validate_conceptual_frontier_deepening",
    ),
    "validate_formal_lens_production_bundle": (
        ".formal_lens_production",
        "validate_formal_lens_production_bundle",
    ),
    "validate_formal_lens_production_packet": (
        ".formal_lens_production",
        "validate_formal_lens_production_packet",
    ),
    "validate_formal_lens_production_request": (
        ".formal_lens_production",
        "validate_formal_lens_production_request",
    ),
    "validate_non_saturating_conceptual_merit_evaluation": (
        ".open_world_creativity",
        "validate_non_saturating_conceptual_merit_evaluation",
    ),
    "validate_open_world_hard_integrity_receipt": (
        ".open_world_creativity",
        "validate_open_world_hard_integrity_receipt",
    ),
    "validate_open_world_maturation_portfolio": (
        ".open_world_creativity",
        "validate_open_world_maturation_portfolio",
    ),
    "validate_post_freeze_taxonomy_classification": (
        ".open_world_creativity",
        "validate_post_freeze_taxonomy_classification",
    ),
    "validate_pre_taxonomy_invention_freeze": (
        ".open_world_creativity",
        "validate_pre_taxonomy_invention_freeze",
    ),
    "validate_proposal_field_free_high_risk_elicitation": (
        ".hypotheses",
        "validate_proposal_field_free_high_risk_elicitation",
    ),
    "validate_seed_free_high_risk_elicitation": (
        ".hypotheses",
        "validate_seed_free_high_risk_elicitation",
    ),
    "validate_parallel_portfolio": (
        ".parallel",
        "validate_parallel_portfolio",
    ),
    "validate_route_neutral_semantic_evaluation": (
        ".route_neutral_semantic_evaluation",
        "validate_route_neutral_semantic_evaluation",
    ),
    "verify_target_predeclared_coverage_certificate": (
        ".aggressive_provider_search",
        "verify_target_predeclared_coverage_certificate",
    ),
}


def __getattr__(name: str) -> Any:
    """Resolve one public surface without eagerly loading sibling runtimes."""

    target = _LAZY_EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attribute_name = target
    value = getattr(import_module(module_name, __name__), attribute_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    """Advertise lazy public names to introspection and IDEs."""

    return sorted(set(globals()) | set(__all__))

__all__ = [
    "ContractError",
    "Namespace",
    "AUTHORITY_BOUNDARY",
    "BASE_DOMINANCE_DIMENSIONS",
    "CONTROL_KINDS",
    "DEEP_REFLECTION_LENSES",
    "MERIT_DIMENSIONS",
    "AggressiveProviderSearchError",
    "ConceptualFrontierDeepeningError",
    "LiteratureConditionedInventionError",
    "RouteNeutralSemanticEvaluationError",
    "CentralConceptualReflectionError",
    "OpenWorldCreativityError",
    "ProofPrelaunchCapability",
    "ProofV3ActionResult",
    "bind_branch_terminal_receipt",
    "build_bounded_current_literature_bundle",
    "build_branch_intent_manifest",
    "build_aggressive_provider_search_request",
    "build_central_conceptual_reflection_request",
    "build_central_conceptual_reflection_commit_binding",
    "build_central_conceptual_reflection_intake_claim",
    "build_central_conceptual_route_reflection_intake",
    "build_committed_route_input",
    "build_conceptual_ancestry_literature_basis",
    "build_conceptual_ancestry_literature_projection",
    "build_conceptual_ancestry_v3",
    "build_literature_conditioned_invention_freeze",
    "build_literature_conditioned_invention_execution",
    "build_literature_conditioned_invention_request",
    "build_literature_counterfactual_inputs",
    "build_non_saturating_conceptual_merit_evaluation",
    "build_open_world_hard_integrity_receipt",
    "build_open_world_maturation_portfolio",
    "build_parallel_maturation_barrier_receipt",
    "build_proof_handoff",
    "build_postcommit_proof_handoff",
    "build_hidden_elicitation_prompt",
    "build_pre_taxonomy_invention_freeze",
    "build_route_neutral_frontier_candidates",
    "build_target_predeclared_coverage_problem",
    "canonical_digest",
    "canonical_json",
    "committed_cycle_projection_artifact_paths",
    "consume_action",
    "consume_action_transaction",
    "consume_committed_central_conceptual_route_reflection_intake",
    "consume_proof_result_v3",
    "classify_frozen_inventions",
    "derive_committed_cycle_world_authority_projection",
    "decode_central_conceptual_reflection_request",
    "decode_central_conceptual_route_reflection_intake",
    "decode_central_conceptual_route_packet",
    "evaluate_discovery_delta",
    "execute_proof_v3",
    "load_committed_cycle_projection_sources",
    "load_formal_lens_producer_registry",
    "issue_proof_prelaunch_capability",
    "proof_prelaunch_capability_projection",
    "reopen_current_proof_handoff",
    "reopen_consumed_proof_result_v3",
    "recover_central_conceptual_reflection_intake_claim",
    "reopen_authoritative_central_conceptual_route_packet",
    "known_taxonomy_commitment",
    "migrate_seed_free_high_risk_elicitation_v1",
    "run_canonical_discovery_cycle",
    "run_aggressive_provider_search",
    "run_bounded_killable_request_wave",
    "run_central_conceptual_routes",
    "run_conceptual_frontier_deepening",
    "run_registered_corner_impossibility_assessment",
    "run_literature_invention_counterfactual_study",
    "run_registered_literature_conditioned_invention",
    "run_committed_proof_action_v3",
    "reconcile_committed_proof_action_v3",
    "run_formal_lens_production",
    "run_parallel_hypothesis_portfolio",
    "run_route_neutral_semantic_evaluation",
    "run_proposal_field_free_high_risk_elicitation",
    "run_seed_free_high_risk_elicitation",
    "replay_proposal_field_free_high_risk_elicitation",
    "replay_committed_cycle_world_authority_projection",
    "replay_seed_free_high_risk_elicitation",
    "prepare_blinded_conceptual_merit_packet",
    "run_isolated_parallel_maturation_branches",
    "schedule_discovery_actions",
    "seal_merit_evaluator_report",
    "seal_semantic_evidence",
    "semantic_hypothesis_signature",
    "validate_evaluation_receipt",
    "validate_aggressive_provider_search_execution",
    "validate_authoritative_central_conceptual_reflection_request",
    "validate_active_prefix_central_conceptual_reflection_request",
    "validate_central_conceptual_reflection_consumption_receipt",
    "validate_bounded_current_literature_bundle",
    "validate_conceptual_ancestry_cycle_binding",
    "validate_conceptual_ancestry_v3",
    "validate_literature_conditioned_invention_execution",
    "validate_conceptual_frontier_deepening",
    "validate_formal_lens_production_bundle",
    "validate_formal_lens_production_packet",
    "validate_formal_lens_production_request",
    "validate_non_saturating_conceptual_merit_evaluation",
    "validate_open_world_hard_integrity_receipt",
    "validate_open_world_maturation_portfolio",
    "validate_post_freeze_taxonomy_classification",
    "validate_pre_taxonomy_invention_freeze",
    "validate_proposal_field_free_high_risk_elicitation",
    "validate_seed_free_high_risk_elicitation",
    "validate_parallel_portfolio",
    "validate_route_neutral_semantic_evaluation",
    "verify_target_predeclared_coverage_certificate",
]
