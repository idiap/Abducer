# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Closed, replayable conceptual ancestry for one theory-N generation.

The v3 ancestry is deliberately independent of the legacy portable literature
production chain. Its literature root is an exact retained UTF-8 capture with
a registered latest-allowed date. A separately bounded adjacent
abstraction-method lane may contribute vocabulary and mechanism questions, but
it cannot support the target claim.

The remaining stages retain producer-native open-world, merit, reflection, and
adjudication artifacts.  Parent and final adjudications are replayed with their
complete systems, rounds, frozen genealogy, candidate bindings, theory digest,
literature digest, portfolio digest, and proposer receipt IDs.  This module
grants local byte/replay authority only; it grants no scientific truth, proof,
experiment, theorem, novelty, or external-evaluator authority.
"""

from __future__ import annotations

import copy
import datetime as dt
import json
from collections.abc import Mapping, Sequence
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .budgets import ResourceBudget, contained_path
from .conceptual_adjudication import (
    validate_adjudication_evidence,
    validate_sealed_preference_authority,
)
from .contracts import (
    ContractError,
    bytes_digest,
    canonical_digest,
    stable_identifier,
    validate_digest,
    validate_identifier,
    validate_payload,
)
from .full_core_reflection_lenses import (
    validate_full_core_reflection_lens_execution_bundle,
    validate_parent_system_materialization_receipt,
)
from .open_world_creativity import (
    DEEP_REFLECTION_LENSES,
    known_taxonomy_commitment,
    validate_non_saturating_conceptual_merit_evaluation,
    validate_open_world_hard_integrity_receipt,
    validate_open_world_maturation_portfolio,
    validate_post_freeze_taxonomy_classification,
    validate_pre_taxonomy_invention_freeze,
)
from .reflection import validate_packet_invariants
from .research_worker_isolation import (
    ResearchWorkerAdapter,
    ResearchWorkerIntegrityError,
    receipt_summary,
    validate_research_worker_receipt,
)


SCHEMA_VERSION = "3.0.0"
LITERATURE_BUNDLE_SCHEMA_VERSION = "3.0.0"
ADJACENT_LANE_SCHEMA_VERSION = "1.0.0"
DEFAULT_MAX_AGE_SECONDS = 30 * 24 * 60 * 60

MANDATORY_STAGE_ORDER: tuple[str, ...] = (
    "current_bounded_literature",
    "literature_only_projection",
    "pre_taxonomy_invention_freeze",
    "post_freeze_taxonomy_classification",
    "isolated_parallel_maturation",
    "hard_integrity_replay",
    "non_saturating_plural_merit_control",
    "six_sibling_full_core_reflections",
    "parent_conceptual_adjudication",
    "theory_only_synthesis",
    "final_conceptual_adjudication",
)

_STAGE_KINDS = {
    "current_bounded_literature": "bounded_current_literature_bundle_v3",
    "literature_only_projection": "literature_only_projection_v3",
    "pre_taxonomy_invention_freeze": (
        "literature_conditioned_pre_taxonomy_invention_freeze"
    ),
    "post_freeze_taxonomy_classification": "post_freeze_taxonomy_replay_context",
    "isolated_parallel_maturation": "open_world_maturation_portfolio",
    "hard_integrity_replay": "open_world_hard_integrity_receipt",
    "non_saturating_plural_merit_control": "non_saturating_conceptual_merit",
    "six_sibling_full_core_reflections": "six_sibling_full_core_reflection_bundle",
    "parent_conceptual_adjudication": "full_conceptual_adjudication_replay",
    "theory_only_synthesis": "reflective_conceptual_discovery_packet",
    "final_conceptual_adjudication": "full_conceptual_adjudication_replay",
}

_PREDECESSOR_STAGE_IDS: dict[str, tuple[str, ...]] = {
    "current_bounded_literature": (),
    "literature_only_projection": ("current_bounded_literature",),
    "pre_taxonomy_invention_freeze": ("literature_only_projection",),
    "post_freeze_taxonomy_classification": ("pre_taxonomy_invention_freeze",),
    "isolated_parallel_maturation": (
        "pre_taxonomy_invention_freeze",
        "post_freeze_taxonomy_classification",
    ),
    "hard_integrity_replay": ("isolated_parallel_maturation",),
    "non_saturating_plural_merit_control": (
        "isolated_parallel_maturation",
        "hard_integrity_replay",
    ),
    "six_sibling_full_core_reflections": (
        "pre_taxonomy_invention_freeze",
        "isolated_parallel_maturation",
        "non_saturating_plural_merit_control",
    ),
    "parent_conceptual_adjudication": (
        "six_sibling_full_core_reflections",
    ),
    "theory_only_synthesis": ("parent_conceptual_adjudication",),
    "final_conceptual_adjudication": (
        "parent_conceptual_adjudication",
        "theory_only_synthesis",
    ),
}

_CAPTURE_FIELDS = frozenset(
    {
        "schema_version",
        "capture_id",
        "target_id",
        "capture_started_at",
        "capture_completed_at",
        "coverage_cutoff",
        "capture_mode",
        "provider",
        "lanes",
        "raw_results",
        "inclusion_policy",
        "exclusion_policy",
        "coverage_limits",
        "exhaustive_coverage_claim",
        "source_correctness_claim",
        "peer_validation_claim",
    }
)
_PROVIDER_FIELDS = frozenset(
    {
        "provider_id",
        "name",
        "index",
        "execution_boundary",
        "raw_payload_retention",
        "receipt_status",
        "executable_replay_status",
    }
)
_LANE_FIELDS = frozenset(
    {
        "lane_id",
        "lane_type",
        "queries",
        "query_policy",
        "status",
        "raw_result_ids",
    }
)
_RESULT_FIELDS = frozenset(
    {
        "result_id",
        "source_id",
        "title",
        "url",
        "retrieval_status",
        "disposition",
        "reason",
        "claim_status",
    }
)
_CURRENT_LITERATURE_BOUNDARY = (
    "This bundle retains one exact caller-supplied provider-normalized capture, "
    "its registered latest-allowed capture date, and a deterministic "
    "consumption deadline. Currentness is local bounded-use status only; "
    "provider ranking payloads and full result HTML may be unavailable, and no "
    "global-latest, exhaustive, source-correctness, peer-validation, proof, "
    "publication, or world authority is granted."
)
_ADJACENT_METHOD_BOUNDARY = (
    "A registered adjacent abstraction-method lane may inform concepts, "
    "vocabulary, typed relations, and mechanism questions only. It provides no "
    "direct target evidence, proof or theorem support, global-latest, "
    "exhaustive, source-truth, novelty, publication, or world authority."
)
_LITERATURE_PROJECTION_BOUNDARY = (
    "This projection contains only exact target-literature capture semantics "
    "and, when registered, one target-separated adjacent abstraction-method "
    "lane. It contains no taxonomy, invention, merit, adjudication, theory, "
    "proof, or experiment artifact and grants no target conclusion."
)
_REFLECTION_BOUNDARY = (
    "Every adjudicated parent system is authored by one registered local "
    "producer consuming the exact matured candidate and six process-authored "
    "lens outputs, with a typed before/after conceptual delta. Every lens "
    "receives the same full candidate core and matched budget in one of six "
    "distinct, mutually overlapping supervised processes. These receipts "
    "establish local process authorship and replay only; hidden-input, "
    "cognitive, semantic, merit, truth, and physics-value authority remain "
    "unavailable."
)
_FINAL_PREFERENCE_BOUNDARY = (
    "The exact sealed set-valued conceptual preference is preserved without "
    "selecting a first member. It authorizes internal target-specific "
    "conceptual preference only, never truth, proof, experiment, physics value, "
    "publication, or world action."
)
_ANCESTRY_BOUNDARY = (
    "This artifact proves one exact ordered local ancestry DAG and replays the "
    "complete frozen adjudication inputs retained at both adjudication stages, "
    "six pre-taxonomy structural corner families or a registered freeze-bounded "
    "shortfall assessment, six process-authored lens transformations, and registered "
    "parent-system materialization receipts. It grants local byte, process-"
    "authorship, causal-order, and validator-replay authority only. "
    "It grants no truth, novelty, creativity efficacy, evaluator separation or "
    "cognitive isolation, theorem, proof, experiment, physics-value, publication, "
    "global-latest, exhaustive-literature, or world authority."
)

AUTHORITY_NULLS = {
    "source_truth_authority": None,
    "global_latestness_authority": None,
    "literature_exhaustiveness_authority": None,
    "literature_benefit_authority": None,
    "taxonomy_exhaustiveness_authority": None,
    "creativity_authority": None,
    "external_merit_authority": None,
    "evaluator_independence": "unavailable",
    "lens_process_isolation": (
        "six_distinct_supervised_local_process_receipts_only"
    ),
    "cognitive_isolation": "unavailable",
    "semantic_isolation": "unavailable",
    "truth_authority": None,
    "philosophical_depth_authority": None,
    "physics_value_authority": None,
    "proof_authority": None,
    "theorem_authority": None,
    "experiment_authority": None,
    "category_hott_advantage_authority": None,
    "generalization_authority": None,
    "publication_authority": None,
    "world_authority": None,
}

_CORNER_STRUCTURAL_CONTRACT_VERSION = "typed-causal-family-contrast.v2"
_CAUSAL_FAMILY_FIELDS = frozenset(
    {
        "invention_id",
        "source_invention_digest",
        "primitive_kind",
        "relation_kind",
        "mechanism_kind",
        "intervention_kind",
        "prediction_direction",
        "correction_kind",
        "target_grounding_paths",
        "literature_causal_input_ids",
    }
)
_CAUSAL_FAMILY_ENUMS = {
    "primitive_kind": frozenset(
        {"entity", "process", "relation", "constraint", "information", "observer"}
    ),
    "relation_kind": frozenset(
        {
            "causal",
            "constitutive",
            "constraint",
            "duality",
            "emergent",
            "operational",
        }
    ),
    "mechanism_kind": frozenset(
        {
            "mediation",
            "symmetry_breaking",
            "coarse_graining",
            "constraint_propagation",
            "topological_obstruction",
            "feedback",
        }
    ),
    "intervention_kind": frozenset(
        {"add", "remove", "hold_fixed", "reverse", "localize", "quotient"}
    ),
    "prediction_direction": frozenset(
        {"increase", "decrease", "invariant", "bifurcate", "obstruct", "permit"}
    ),
    "correction_kind": frozenset(
        {
            "retract",
            "retype",
            "split_scope",
            "add_mediator",
            "change_relation",
            "abandon",
        }
    ),
}
_CORNER_IMPOSSIBILITY_ASSESSOR_REGISTRATION = {
    "assessor_id": "registered-typed-causal-corner-assessor-v2",
    "implementation_entrypoint": (
        "agentic/scripts/run_conceptual_corner_impossibility_assessor_v3.py"
    ),
    "contrast_contract_version": _CORNER_STRUCTURAL_CONTRACT_VERSION,
    "decision_rule": (
        "In a separate supervised process, replay the exact conditioned freeze, "
        "target-grounded typed causal contracts, and semantic literature input; "
        "require a six-member clique satisfying all four causal domains."
    ),
    "authority_scope": (
        "Exact immutable-freeze membership only; no future-generation, semantic, "
        "creative, scientific-benefit, or truth authority."
    ),
}
_CORNER_IMPOSSIBILITY_ASSESSOR_DIGEST = canonical_digest(
    _CORNER_IMPOSSIBILITY_ASSESSOR_REGISTRATION
)

_TOP_FIELDS = frozenset(
    {
        "schema_version",
        "artifact_kind",
        "ancestry_id",
        "target_id",
        "run_id",
        "source_state_version",
        "theory_generation",
        "theory_state_digest",
        "known_taxonomy_commitment_digest",
        "ordered_stage_ids",
        "stages",
        "edge_set_digest",
        "final_preference_authority",
        "same_cycle_support_boundary",
        "authority_nulls",
        "authority_boundary",
        "content_digest",
    }
)
_STAGE_FIELDS = frozenset(
    {
        "stage_index",
        "stage_id",
        "artifact_kind",
        "artifact",
        "artifact_digest",
        "predecessors",
        "stage_digest",
    }
)


class ConceptualAncestryV3Error(ContractError):
    """Carry a stable reason code for ancestry rejection."""

    def __init__(self, reason_code: str, message: str) -> None:
        self.reason_code = reason_code
        super().__init__(f"conceptual_ancestry_v3[{reason_code}]: {message}")


def _fail(reason_code: str, message: str) -> None:
    raise ConceptualAncestryV3Error(reason_code, message)


def _strict(
    value: Mapping[str, Any], expected: frozenset[str] | set[str], label: str
) -> None:
    actual = set(value)
    expected_set = set(expected)
    if actual != expected_set:
        _fail(
            "closed_contract_violation",
            f"{label} fields differ: missing={sorted(expected_set - actual)}, "
            f"extra={sorted(actual - expected_set)}",
        )


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        _fail("object_required", f"{label} must be an object")
    return copy.deepcopy(dict(value))


def _rows(value: Any, label: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        _fail("array_required", f"{label} must be an array")
    return [_object(row, f"{label}[{index}]") for index, row in enumerate(value)]


def _state_version(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        _fail("state_version_invalid", f"{label} must be a non-negative integer")
    return value


def _timestamp(value: Any, label: str) -> dt.datetime:
    if not isinstance(value, str) or not value:
        _fail("timestamp_invalid", f"{label} must be a nonempty timestamp")
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ConceptualAncestryV3Error(
            "timestamp_invalid", f"{label} is not ISO-8601: {value!r}"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        _fail("timestamp_invalid", f"{label} must carry an explicit timezone")
    return parsed.astimezone(dt.UTC)


def _date(value: Any, label: str) -> dt.date:
    if not isinstance(value, str):
        _fail("date_invalid", f"{label} must be an ISO date")
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise ConceptualAncestryV3Error(
            "date_invalid", f"{label} is not an ISO date"
        ) from exc


def _seal(value: Mapping[str, Any], field: str = "content_digest") -> dict[str, Any]:
    sealed = copy.deepcopy(dict(value))
    if field in sealed:
        _fail("seal_field_present", f"{field} must be absent before sealing")
    sealed[field] = canonical_digest(sealed)
    return sealed


def _verify_seal(
    value: Mapping[str, Any], field: str, label: str
) -> None:
    validate_digest(value.get(field))
    unsigned = {
        key: copy.deepcopy(child)
        for key, child in value.items()
        if key != field
    }
    if value[field] != canonical_digest(unsigned):
        _fail("digest_mismatch", f"{label} {field} does not replay")


def _validate_schema(
    value: Mapping[str, Any], schema_name: str, label: str
) -> None:
    try:
        validate_payload(dict(value), schema_name)
    except ContractError as exc:
        raise ConceptualAncestryV3Error(
            "schema_runtime_parity_failure", f"{label}: {exc}"
        ) from exc


def build_registered_adjacent_abstraction_method_lane(
    *,
    target_id: str,
    selection_basis: Mapping[str, Any],
    sources: Sequence[Mapping[str, Any]],
    permitted_uses: Sequence[str],
    forbidden_uses: Sequence[str],
    excluded_target_source_ids: Sequence[str],
    excluded_capture_dates: Sequence[str],
    target_specific_forbidden_claims: Sequence[str],
) -> dict[str, Any]:
    """Build a generic registered lane with no direct-target authority."""

    validate_identifier(target_id, "adjacent lane target_id")
    source_rows = [copy.deepcopy(dict(row)) for row in sources]
    basis = copy.deepcopy(dict(selection_basis))
    core = {
        "schema_version": ADJACENT_LANE_SCHEMA_VERSION,
        "artifact_kind": "adjacent_abstraction_method_literature_lane",
        "lane_id": stable_identifier(
            "adjacent-abstraction-method-lane",
            target_id,
            basis,
            source_rows,
        ),
        "target_id": target_id,
        "selection_basis": basis,
        "sources": source_rows,
        "permitted_uses": [str(value) for value in permitted_uses],
        "forbidden_uses": [str(value) for value in forbidden_uses],
        "target_separation": {
            "relationship": "adjacent_abstraction_method_only",
            "direct_target_source_ids": [],
            "excluded_target_source_ids": [
                str(value) for value in excluded_target_source_ids
            ],
            "excluded_capture_dates": [
                str(value) for value in excluded_capture_dates
            ],
            "target_specific_forbidden_claims": [
                str(value) for value in target_specific_forbidden_claims
            ],
            "target_claim_support": False,
        },
        "authority": {
            "method_context_only": True,
            "direct_target_claim_authority": False,
            "proof_authority": False,
            "global_latestness_authority": False,
            "exhaustiveness_authority": False,
        },
        "authority_boundary": _ADJACENT_METHOD_BOUNDARY,
    }
    return validate_adjacent_abstraction_method_lane(_seal(core))


def validate_adjacent_abstraction_method_lane(
    lane: Mapping[str, Any],
) -> dict[str, Any]:
    """Replay one registered lane and its closed no-target-support boundary."""

    value = _object(lane, "adjacent abstraction-method lane")
    _validate_schema(
        value,
        "adjacent_abstraction_method_literature_lane.schema.json",
        "adjacent abstraction-method lane",
    )
    _verify_seal(value, "content_digest", "adjacent abstraction-method lane")
    sources = _rows(value["sources"], "adjacent sources")
    if (
        value["schema_version"] != ADJACENT_LANE_SCHEMA_VERSION
        or value["artifact_kind"]
        != "adjacent_abstraction_method_literature_lane"
        or not sources
    ):
        _fail(
            "adjacent_lane_source_substitution",
            "registered adjacent sources are absent or the lane kind changed",
        )
    expected_id = stable_identifier(
        "adjacent-abstraction-method-lane",
        value["target_id"],
        value["selection_basis"],
        sources,
    )
    if value["lane_id"] != expected_id:
        _fail("adjacent_lane_identity_mismatch", "adjacent lane ID does not replay")
    observed_at = _timestamp(
        value["selection_basis"]["observed_at"], "adjacent observed_at"
    )
    source_ids = [str(row["source_id"]) for row in sources]
    version_ids = [str(row["version_id"]) for row in sources]
    for row in sources:
        validate_identifier(row["source_id"], "adjacent source_id")
        if (
            not row["version_id"]
            or not row["title"]
            or not row["authors"]
            or not row["url"]
            or not row["method_topic"]
            or not row["method_relevance"]
            or row["target_relevance"]
            != "adjacent_method_only_no_direct_target_support"
        ):
            _fail(
                "adjacent_lane_source_invalid",
                "adjacent source lacks method-only versioned metadata",
            )
        version_date = _date(
            row["version_date"], "adjacent source version_date"
        )
        if version_date > observed_at.date():
            _fail(
                "source_version_after_observation",
                "adjacent source version postdates its metadata observation",
            )
    required_forbidden = {
        "direct_target_support",
        "proof_or_theorem_support",
        "source_truth_inference",
        "global_latestness_claim",
        "exhaustive_coverage_claim",
        "novelty_or_publication_claim",
    }
    target_separation = value["target_separation"]
    for raw_date in target_separation["excluded_capture_dates"]:
        _date(raw_date, "excluded capture date")
    if (
        value["selection_basis"]["record_count"] != len(sources)
        or len(source_ids) != len(set(source_ids))
        or len(version_ids) != len(set(version_ids))
        or not value["permitted_uses"]
        or not required_forbidden.issubset(value["forbidden_uses"])
        or target_separation["relationship"]
        != "adjacent_abstraction_method_only"
        or target_separation["direct_target_source_ids"]
        or target_separation["target_claim_support"] is not False
        or not target_separation["target_specific_forbidden_claims"]
        or value["authority"]
        != {
            "method_context_only": True,
            "direct_target_claim_authority": False,
            "proof_authority": False,
            "global_latestness_authority": False,
            "exhaustiveness_authority": False,
        }
        or value["authority_boundary"] != _ADJACENT_METHOD_BOUNDARY
    ):
        _fail(
            "adjacent_lane_authority_forgery",
            "adjacent literature escaped its method-only/no-target boundary",
        )
    return copy.deepcopy(value)


def _validate_capture(
    capture: Mapping[str, Any], *, target_id: str
) -> dict[str, Any]:
    """Validate the generic frozen-capture envelope and temporal boundary."""

    value = _object(capture, "current literature capture")
    _strict(value, _CAPTURE_FIELDS, "current literature capture")
    if (
        value["schema_version"] != "1.0"
        or value["target_id"] != target_id
        or value["capture_mode"]
        != "live_external_web_search_frozen_for_replay"
    ):
        _fail(
            "current_capture_identity_mismatch",
            "capture version, target, or frozen-response mode changed",
        )
    validate_identifier(value["capture_id"], "capture_id")
    validate_identifier(value["target_id"], "capture target_id")
    started = _timestamp(value["capture_started_at"], "capture_started_at")
    completed = _timestamp(value["capture_completed_at"], "capture_completed_at")
    cutoff = _timestamp(value["coverage_cutoff"], "coverage_cutoff")
    if not started <= completed or cutoff != completed:
        _fail(
            "current_capture_clock_invalid",
            "capture clocks must satisfy started <= completed == cutoff",
        )
    provider = _object(value["provider"], "capture provider")
    _strict(provider, _PROVIDER_FIELDS, "capture provider")
    if (
        not provider["provider_id"]
        or not provider["name"]
        or provider["receipt_status"] != "externally_executed_then_frozen"
        or provider["executable_replay_status"]
        != "frozen_response_adapter_only"
        or not provider["execution_boundary"]
    ):
        _fail(
            "capture_producer_boundary_invalid",
            "capture must retain its externally executed/frozen-response boundary",
        )
    if any(
        value[field] is not False
        for field in (
            "exhaustive_coverage_claim",
            "source_correctness_claim",
            "peer_validation_claim",
        )
    ):
        _fail(
            "capture_authority_forgery",
            "capture cannot claim exhaustive, source-correct, or peer-validated authority",
        )
    lanes = _rows(value["lanes"], "capture lanes")
    if not lanes:
        _fail("capture_lane_incomplete", "at least one completed lane is required")
    lane_ids: list[str] = []
    lane_types: list[str] = []
    referenced_result_ids: set[str] = set()
    for lane in lanes:
        _strict(lane, _LANE_FIELDS, "capture lane")
        validate_identifier(lane["lane_id"], "capture lane_id")
        if (
            lane["status"] != "completed"
            or not lane["queries"]
            or not lane["query_policy"]
            or not lane["raw_result_ids"]
        ):
            _fail("capture_lane_incomplete", "every capture lane must be completed")
        lane_ids.append(lane["lane_id"])
        lane_types.append(lane["lane_type"])
        referenced_result_ids.update(lane["raw_result_ids"])
    if (
        len(set(lane_ids)) != len(lane_ids)
        or len(set(lane_types)) != len(lane_types)
    ):
        _fail(
            "capture_lane_substitution",
            "capture lane identities or semantic lane types repeat",
        )
    results = _rows(value["raw_results"], "capture raw results")
    if not results:
        _fail("capture_result_closure_invalid", "capture has no retained results")
    result_ids: list[str] = []
    for result in results:
        _strict(result, _RESULT_FIELDS, "capture raw result")
        validate_identifier(result["result_id"], "capture result_id")
        validate_identifier(result["source_id"], "capture source_id")
        if not result["title"] or not result["url"] or not result["reason"]:
            _fail("capture_result_invalid", "capture result lacks retained metadata")
        result_ids.append(result["result_id"])
    if (
        len(set(result_ids)) != len(result_ids)
        or referenced_result_ids != set(result_ids)
    ):
        _fail(
            "capture_result_closure_invalid",
            "capture lanes and retained-result closure do not replay",
        )
    return copy.deepcopy(value)


def _expected_literature_manifest(
    *,
    capture: Mapping[str, Any],
    capture_sha256: str,
    capture_byte_length: int,
    adjacent_lane: Mapping[str, Any] | None,
) -> dict[str, Any]:
    entries = [
        {
            "entry_id": "target_current_capture",
            "artifact_kind": "frozen_target_literature_capture",
            "artifact_id": capture["capture_id"],
            "artifact_digest": capture_sha256,
            "byte_length": capture_byte_length,
            "coverage_cutoff": capture["coverage_cutoff"],
            "authority_scope": "target_surveillance_metadata_and_dispositions_only",
        },
    ]
    if adjacent_lane is not None:
        entries.append(
            {
                "entry_id": "adjacent_abstraction_method_lane",
                "artifact_kind": adjacent_lane["artifact_kind"],
                "artifact_id": adjacent_lane["lane_id"],
                "artifact_digest": adjacent_lane["content_digest"],
                "byte_length": None,
                "coverage_cutoff": adjacent_lane["selection_basis"][
                    "observed_at"
                ],
                "authority_scope": "method_context_only_no_target_support",
            }
        )
    core = {
        "manifest_id": stable_identifier(
            "conceptual-ancestry-literature-manifest",
            capture_sha256,
            (
                adjacent_lane["content_digest"]
                if adjacent_lane is not None
                else None
            ),
        ),
        "ordered_entry_ids": [row["entry_id"] for row in entries],
        "entries": entries,
        "producer_limitations": {
            "network_execution": "externally_executed_then_frozen",
            "local_replay": "exact_retained_utf8_and_normalized_metadata_only",
            "provider_ranking_payload": "unavailable",
            "complete_result_html": "unavailable",
            "global_latestness": "unavailable",
            "exhaustive_coverage": "unavailable",
            "source_correctness": "unavailable",
            "peer_validation": "unavailable",
        },
    }
    return {**core, "manifest_digest": canonical_digest(core)}


def build_bounded_current_literature_bundle(
    *,
    capture_bytes: bytes,
    target_id: str,
    run_id: str,
    state_version: int,
    present_use_at: str,
    latest_allowed_capture_date: str,
    adjacent_method_lane: Mapping[str, Any] | None = None,
    max_age_seconds: int = DEFAULT_MAX_AGE_SECONDS,
) -> dict[str, Any]:
    """Retain and bound one caller-supplied frozen capture."""

    if not isinstance(capture_bytes, bytes) or not capture_bytes:
        _fail(
            "capture_bytes_required",
            "the bounded bundle requires exact nonempty capture bytes",
        )
    try:
        retained_utf8 = capture_bytes.decode("utf-8")
        parsed = json.loads(retained_utf8)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ConceptualAncestryV3Error(
            "capture_bytes_invalid", f"capture bytes are not UTF-8 JSON: {exc}"
        ) from exc
    capture = _validate_capture(parsed, target_id=target_id)
    validate_identifier(run_id, "run_id")
    state = _state_version(state_version, "state_version")
    if (
        isinstance(max_age_seconds, bool)
        or not isinstance(max_age_seconds, int)
        or max_age_seconds <= 0
    ):
        _fail("literature_window_invalid", "max_age_seconds must be positive")
    present = _timestamp(present_use_at, "present_use_at")
    completed = _timestamp(capture["capture_completed_at"], "capture_completed_at")
    latest_allowed = _date(
        latest_allowed_capture_date, "latest_allowed_capture_date"
    )
    if completed.date() > latest_allowed:
        _fail(
            "future_dated_capture_forbidden",
            "capture completion exceeds its registered latest-allowed date",
        )
    consume_before = completed + dt.timedelta(seconds=max_age_seconds)
    if not completed <= present <= consume_before:
        _fail(
            "literature_not_current",
            "present use is outside the exact capture consumption window",
        )
    lane = (
        validate_adjacent_abstraction_method_lane(adjacent_method_lane)
        if adjacent_method_lane is not None
        else None
    )
    if lane is not None and lane["target_id"] != target_id:
        _fail(
            "adjacent_lane_target_mismatch",
            "adjacent lane crossed the current target",
        )
    if lane is not None and _timestamp(
        lane["selection_basis"]["observed_at"], "adjacent observed_at"
    ) > present:
        _fail(
            "adjacent_lane_future_observation",
            "adjacent lane observation cannot postdate bundle use",
        )
    if lane is not None and _timestamp(
        lane["selection_basis"]["observed_at"], "adjacent observed_at"
    ) > _timestamp(capture["coverage_cutoff"], "capture coverage cutoff"):
        _fail(
            "adjacent_lane_after_cutoff",
            "adjacent lane observation exceeds the bounded capture cutoff",
        )
    capture_sha256 = bytes_digest(capture_bytes)
    manifest = _expected_literature_manifest(
        capture=capture,
        capture_sha256=capture_sha256,
        capture_byte_length=len(capture_bytes),
        adjacent_lane=lane,
    )
    core = {
        "schema_version": LITERATURE_BUNDLE_SCHEMA_VERSION,
        "artifact_kind": "bounded_current_literature_bundle_v3",
        "bundle_id": stable_identifier(
            "bounded-current-literature-v3",
            target_id,
            run_id,
            state,
            capture_sha256,
            lane["content_digest"] if lane is not None else None,
            latest_allowed_capture_date,
        ),
        "target_id": target_id,
        "run_id": run_id,
        "state_version": state,
        "capture_descriptor": {
            "capture_id": capture["capture_id"],
            "media_type": "application/json; charset=utf-8",
            "sha256": capture_sha256,
            "byte_length": len(capture_bytes),
            "retained_utf8": retained_utf8,
        },
        "capture": capture,
        "adjacent_abstraction_method_lane": lane,
        "manifest": manifest,
        "currentness": {
            "policy": "capture_completion_bounded_consumption_v3",
            "latest_allowed_capture_date": latest_allowed_capture_date,
            "capture_completed_at": capture["capture_completed_at"],
            "coverage_cutoff": capture["coverage_cutoff"],
            "max_age_seconds": max_age_seconds,
            "consume_before": consume_before.isoformat().replace("+00:00", "Z"),
            "present_use_at": present.isoformat().replace("+00:00", "Z"),
            "status": "current_inside_bounded_window",
        },
        "authority_nulls": {
            "clock_attestation_authority": None,
            "global_latestness_authority": None,
            "exhaustiveness_authority": None,
            "source_truth_authority": None,
            "peer_validation_authority": None,
            "literature_benefit_authority": None,
            "proof_authority": None,
            "publication_authority": None,
            "world_authority": None,
        },
        "authority_boundary": _CURRENT_LITERATURE_BOUNDARY,
    }
    bundle = _seal(core)
    return validate_bounded_current_literature_bundle(bundle)


def validate_bounded_current_literature_bundle(
    bundle: Mapping[str, Any],
    *,
    present_use_at: str | None = None,
) -> dict[str, Any]:
    """Replay bytes, manifest, deadline, and target-separated adjacent lane."""

    value = _object(bundle, "bounded current literature bundle")
    _validate_schema(
        value,
        "conceptual_ancestry_literature_bundle_v3.schema.json",
        "bounded current literature bundle",
    )
    _verify_seal(value, "content_digest", "bounded current literature bundle")
    if (
        value["schema_version"] != LITERATURE_BUNDLE_SCHEMA_VERSION
        or value["artifact_kind"] != "bounded_current_literature_bundle_v3"
    ):
        _fail(
            "literature_bundle_substitution",
            "literature bundle version or artifact kind changed",
        )
    retained = value["capture_descriptor"]["retained_utf8"]
    try:
        capture_bytes = retained.encode("utf-8")
        parsed = json.loads(retained)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ConceptualAncestryV3Error(
            "capture_bytes_invalid", f"retained capture does not decode: {exc}"
        ) from exc
    capture = _validate_capture(parsed, target_id=value["target_id"])
    descriptor = value["capture_descriptor"]
    if (
        capture != value["capture"]
        or descriptor["capture_id"] != capture["capture_id"]
        or descriptor["media_type"] != "application/json; charset=utf-8"
        or descriptor["sha256"] != bytes_digest(capture_bytes)
        or descriptor["byte_length"] != len(capture_bytes)
    ):
        _fail(
            "capture_byte_replay_mismatch",
            "retained capture bytes, parsed capture, and descriptor differ",
        )
    raw_lane = value["adjacent_abstraction_method_lane"]
    lane = (
        validate_adjacent_abstraction_method_lane(raw_lane)
        if raw_lane is not None
        else None
    )
    if lane is not None and lane["target_id"] != value["target_id"]:
        _fail("adjacent_lane_target_mismatch", "adjacent lane crossed target")
    expected_manifest = _expected_literature_manifest(
        capture=capture,
        capture_sha256=descriptor["sha256"],
        capture_byte_length=descriptor["byte_length"],
        adjacent_lane=lane,
    )
    if value["manifest"] != expected_manifest:
        _fail(
            "literature_manifest_replay_mismatch",
            "complete literature manifest does not replay",
        )
    currentness = value["currentness"]
    completed = _timestamp(
        currentness["capture_completed_at"], "currentness capture completion"
    )
    cutoff = _timestamp(currentness["coverage_cutoff"], "currentness cutoff")
    recorded_present = _timestamp(
        currentness["present_use_at"], "currentness present use"
    )
    if lane is not None and _timestamp(
        lane["selection_basis"]["observed_at"], "adjacent observed_at"
    ) > recorded_present:
        _fail(
            "adjacent_lane_future_observation",
            "adjacent lane observation postdates the recorded bundle use",
        )
    if lane is not None and _timestamp(
        lane["selection_basis"]["observed_at"], "adjacent observed_at"
    ) > cutoff:
        _fail(
            "adjacent_lane_after_cutoff",
            "adjacent lane observation exceeds the bounded capture cutoff",
        )
    deadline = _timestamp(currentness["consume_before"], "consume_before")
    max_age = currentness["max_age_seconds"]
    latest_allowed = _date(
        currentness["latest_allowed_capture_date"],
        "latest_allowed_capture_date",
    )
    if (
        currentness["policy"]
        != "capture_completion_bounded_consumption_v3"
        or currentness["status"] != "current_inside_bounded_window"
        or completed
        != _timestamp(capture["capture_completed_at"], "capture completion")
        or cutoff != _timestamp(capture["coverage_cutoff"], "capture cutoff")
        or completed.date() > latest_allowed
        or deadline != completed + dt.timedelta(seconds=max_age)
        or not completed <= recorded_present <= deadline
    ):
        _fail(
            "literature_window_invalid",
            "literature deadline or recorded-use currentness does not replay",
        )
    if present_use_at is not None:
        use = _timestamp(present_use_at, "present literature use")
        if not completed <= use <= deadline:
            _fail(
                "literature_not_current",
                "governed present use is outside the v3 consumption deadline",
            )
    expected_id = stable_identifier(
        "bounded-current-literature-v3",
        value["target_id"],
        value["run_id"],
        value["state_version"],
        descriptor["sha256"],
        lane["content_digest"] if lane is not None else None,
        currentness["latest_allowed_capture_date"],
    )
    if value["bundle_id"] != expected_id:
        _fail("literature_bundle_identity_mismatch", "bundle ID does not replay")
    expected_nulls = {
        "clock_attestation_authority": None,
        "global_latestness_authority": None,
        "exhaustiveness_authority": None,
        "source_truth_authority": None,
        "peer_validation_authority": None,
        "literature_benefit_authority": None,
        "proof_authority": None,
        "publication_authority": None,
        "world_authority": None,
    }
    if (
        value["authority_nulls"] != expected_nulls
        or value["authority_boundary"] != _CURRENT_LITERATURE_BOUNDARY
    ):
        _fail(
            "literature_authority_forgery",
            "bounded literature authority boundary changed",
        )
    return copy.deepcopy(value)


def _semantic_assimilation_delta(
    source: Mapping[str, Any], warrants: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    """Derive a bounded correction-aware input event without truth authority."""

    correction = str(source["correction_status"])
    relations = sorted({str(row["relation"]) for row in warrants})
    if correction == "retracted":
        event = "retire"
    elif correction in {"corrected", "superseded"}:
        event = "reframe"
    elif "contradicts" in relations:
        event = "demote"
    elif "leaves_open" in relations:
        event = "new_question"
    elif not relations or relations == ["unresolved"]:
        event = "justified_no_change"
    else:
        event = "reprioritize"
    return {
        "event_type": event,
        "source_correction_status": correction,
        "semantic_relations": relations,
        "correction_or_supersession_active": correction
        in {"corrected", "superseded", "retracted"},
        "authority": "bounded_internal_assimilation_input_only",
    }


def _literature_derived_invention_input(
    *,
    bundle: Mapping[str, Any],
    semantic_snapshot: Mapping[str, Any],
    bridge: Mapping[str, Any],
) -> dict[str, Any]:
    """Close exact semantic claims, warrants, and deltas as invention input."""

    causal_inputs: list[dict[str, Any]] = []
    for source in sorted(
        semantic_snapshot["sources"], key=lambda row: row["source_id"]
    ):
        provenance_by_digest = {
            row["claim_digest"]: copy.deepcopy(dict(row))
            for row in source.get("claim_provenance", [])
        }
        claims = list(source["claims"]) or [None]
        for claim_index, exact_claim in enumerate(claims):
            claim_digest = canonical_digest(exact_claim)
            warrants = sorted(
                (
                    copy.deepcopy(dict(row))
                    for row in source.get("semantic_warrants", [])
                    if row["claim_digest"] == claim_digest
                ),
                key=lambda row: row["warrant_id"],
            )
            input_id = stable_identifier(
                "literature-causal-invention-input",
                source["source_id"],
                source["source_version"],
                source["correction_status"],
                claim_digest,
            )
            core = {
                "causal_input_id": input_id,
                "source_id": source["source_id"],
                "source_content_digest": source["content_digest"],
                "source_version": source["source_version"],
                "source_correction_status": source["correction_status"],
                "claim_index": claim_index if exact_claim is not None else None,
                "exact_claim": exact_claim,
                "claim_digest": claim_digest,
                "claim_provenance": provenance_by_digest.get(claim_digest),
                "semantic_warrants": warrants,
                "semantic_warrant_set_digest": canonical_digest(warrants),
                "assimilation_delta": _semantic_assimilation_delta(
                    source, warrants
                ),
                "limitations": copy.deepcopy(source["limitations"]),
                "lane_ids": copy.deepcopy(source["lane_ids"]),
            }
            causal_inputs.append(
                {**core, "causal_input_digest": canonical_digest(core)}
            )
    input_core = {
        "schema_version": "1.0.0",
        "artifact_kind": "literature_derived_invention_input",
        "input_id": stable_identifier(
            "literature-derived-invention-input",
            bridge["content_digest"],
            semantic_snapshot["content_digest"],
            causal_inputs,
        ),
        "target_id": bundle["target_id"],
        "raw_capture_sha256": bridge["raw_capture_root"]["sha256"],
        "semantic_bridge_id": bridge["bridge_id"],
        "semantic_bridge_digest": bridge["content_digest"],
        "semantic_snapshot_id": semantic_snapshot["snapshot_id"],
        "semantic_snapshot_digest": semantic_snapshot["content_digest"],
        "causal_inputs": causal_inputs,
        "corrected_or_superseded_source_ids": sorted(
            row["source_id"]
            for row in semantic_snapshot["sources"]
            if row["correction_status"] in {"corrected", "superseded"}
        ),
        "retracted_source_ids": sorted(
            row["source_id"]
            for row in semantic_snapshot["sources"]
            if row["correction_status"] == "retracted"
        ),
        "coverage_limits": copy.deepcopy(
            semantic_snapshot["coverage_limits"]
        ),
        "authority_nulls": {
            "source_truth_authority": None,
            "semantic_entailment_authority": None,
            "global_latestness_authority": None,
            "exhaustiveness_authority": None,
            "literature_benefit_authority": None,
            "creativity_authority": None,
        },
    }
    return _seal(input_core)


def build_conceptual_ancestry_literature_projection(
    *,
    literature_bundle: Mapping[str, Any],
    semantic_snapshot: Mapping[str, Any],
    literature_snapshot_capture_bridge: Mapping[str, Any],
    present_use_at: str | None = None,
) -> dict[str, Any]:
    """Build the exact two-root semantic input consumed by ancestry v3."""

    bundle = validate_bounded_current_literature_bundle(
        literature_bundle, present_use_at=present_use_at
    )
    snapshot = copy.deepcopy(dict(semantic_snapshot))
    bridge_candidate = copy.deepcopy(
        dict(literature_snapshot_capture_bridge)
    )
    # Local import avoids the bridge module's intentional ancestry import.
    from .literature_snapshot_capture_bridge import (
        validate_literature_snapshot_capture_bridge,
    )

    bridge = validate_literature_snapshot_capture_bridge(
        bridge_candidate,
        literature_bundle=bundle,
        semantic_snapshot=snapshot,
        present_use_at=present_use_at,
    )
    capture = bundle["capture"]
    results = copy.deepcopy(capture["raw_results"])
    direct = [
        row
        for row in results
        if row["claim_status"] == "unverified_challenger"
    ]
    withdrawn = [
        row
        for row in results
        if row["claim_status"] == "withdrawn_not_support"
    ]
    core = {
        "schema_version": "3.0.0",
        "artifact_kind": "literature_only_projection_v3",
        "projection_id": stable_identifier(
            "semantic-literature-causal-projection-v3",
            bundle["content_digest"],
            bridge["content_digest"],
            snapshot["content_digest"],
        ),
        "target_id": bundle["target_id"],
        "run_id": bundle["run_id"],
        "state_version": bundle["state_version"],
        "source_bundle_id": bundle["bundle_id"],
        "source_bundle_digest": bundle["content_digest"],
        "source_manifest_digest": bundle["manifest"]["manifest_digest"],
        "consumption_deadline": copy.deepcopy(bundle["currentness"]),
        "raw_capture_root": copy.deepcopy(bridge["raw_capture_root"]),
        "semantic_bridge": bridge,
        "semantic_bridge_id": bridge["bridge_id"],
        "semantic_bridge_digest": bridge["content_digest"],
        "semantic_snapshot_root": copy.deepcopy(
            bridge["semantic_snapshot_root"]
        ),
        "semantic_snapshot": snapshot,
        "target_literature": {
            "capture_id": capture["capture_id"],
            "capture_sha256": bundle["capture_descriptor"]["sha256"],
            "capture_byte_length": bundle["capture_descriptor"]["byte_length"],
            "capture_completed_at": capture["capture_completed_at"],
            "coverage_cutoff": capture["coverage_cutoff"],
            "provider_execution_boundary": copy.deepcopy(capture["provider"]),
            "lanes": copy.deepcopy(capture["lanes"]),
            "raw_results": results,
            "direct_unverified_challengers": direct,
            "withdrawn_negative_controls": withdrawn,
            "coverage_limits": copy.deepcopy(capture["coverage_limits"]),
        },
        "adjacent_abstraction_method_lane": copy.deepcopy(
            bundle["adjacent_abstraction_method_lane"]
        ),
        "literature_derived_invention_input": (
            _literature_derived_invention_input(
                bundle=bundle,
                semantic_snapshot=snapshot,
                bridge=bridge,
            )
        ),
        "forbidden_ancestry_kinds": [
            "taxonomy",
            "invention",
            "merit",
            "adjudication",
            "theory",
            "proof",
            "experiment",
        ],
        "authority": {
            "literature_only": True,
            "adjacent_lane_present": (
                bundle["adjacent_abstraction_method_lane"] is not None
            ),
            "adjacent_lane_method_only": (
                bundle["adjacent_abstraction_method_lane"] is not None
            ),
            "target_claim_support_from_adjacent_lane": False,
            "semantic_claim_truth_authority": False,
            "semantic_warrant_entailment_authority": False,
            "literature_benefit_authority": False,
            "creativity_authority": False,
            "proof_authority": False,
            "experiment_authority": False,
        },
        "authority_boundary": _LITERATURE_PROJECTION_BOUNDARY,
    }
    return _seal(core)


def _validate_literature_projection(
    projection: Mapping[str, Any], *, bundle: Mapping[str, Any]
) -> dict[str, Any]:
    value = _object(projection, "literature-only projection")
    _verify_seal(value, "content_digest", "literature-only projection")
    expected = build_conceptual_ancestry_literature_projection(
        literature_bundle=bundle,
        semantic_snapshot=value["semantic_snapshot"],
        literature_snapshot_capture_bridge=value["semantic_bridge"],
    )
    if value != expected:
        _fail(
            "literature_projection_replay_mismatch",
            "literature-only projection differs from the exact bounded bundle",
        )
    if value["forbidden_ancestry_kinds"] != [
        "taxonomy",
        "invention",
        "merit",
        "adjudication",
        "theory",
        "proof",
        "experiment",
    ]:
        _fail(
            "literature_projection_contaminated",
            "non-literature ancestry entered the literature-only stage",
        )
    return copy.deepcopy(value)


def _grounding_value(freeze: Mapping[str, Any], path: str) -> Any:
    """Resolve only the target/protected-success paths allowed as grounding."""

    allowed_root = {
        "/invention_request/target_pressure",
    }
    if path in allowed_root:
        return freeze["invention_request"]["target_pressure"]
    for field in ("root_contradictions", "protected_successes"):
        prefix = f"/invention_request/{field}/"
        if path.startswith(prefix):
            suffix = path.removeprefix(prefix)
            if suffix.isdigit():
                rows = freeze["invention_request"][field]
                index = int(suffix)
                if 0 <= index < len(rows):
                    return rows[index]
    _fail(
        "corner_impossibility_grounding_invalid",
        f"grounding path is outside the frozen target request: {path}",
    )


def _projection_invention_input(
    projection: Mapping[str, Any],
) -> dict[str, Any]:
    value = _object(projection, "semantic literature causal projection")
    _verify_seal(value, "content_digest", "semantic literature causal projection")
    if value.get("artifact_kind") != "literature_only_projection_v3":
        _fail(
            "literature_projection_kind_invalid",
            "conditioned freeze requires the v3 semantic literature projection",
        )
    result = _object(
        value.get("literature_derived_invention_input"),
        "literature-derived invention input",
    )
    _verify_seal(
        result, "content_digest", "literature-derived invention input"
    )
    if result.get("artifact_kind") != "literature_derived_invention_input":
        _fail(
            "literature_invention_input_invalid",
            "projection lacks the exact semantic invention input",
        )
    return copy.deepcopy(result)


def _validated_causal_family_contracts(
    *,
    source_freeze: Mapping[str, Any],
    literature_input: Mapping[str, Any],
    contracts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Validate one closed causal signature per raw invention."""

    raw_by_id = {
        str(row["invention_id"]): copy.deepcopy(dict(row))
        for row in source_freeze["raw_inventions"]
    }
    causal_input_ids = {
        str(row["causal_input_id"])
        for row in literature_input["causal_inputs"]
    }
    rows: list[dict[str, Any]] = []
    for raw_contract in contracts:
        contract = _object(raw_contract, "typed causal-family contract")
        retained_digest = contract.get("contract_digest")
        _strict(
            contract,
            (
                _CAUSAL_FAMILY_FIELDS
                | ({"contract_digest"} if retained_digest is not None else set())
            ),
            "typed causal-family contract",
        )
        invention_id = validate_identifier(
            contract["invention_id"], "causal family invention_id"
        )
        if invention_id not in raw_by_id:
            _fail(
                "causal_family_bijection_invalid",
                "causal-family contract names an unknown invention",
            )
        if contract["source_invention_digest"] != canonical_digest(
            raw_by_id[invention_id]
        ):
            _fail(
                "causal_family_source_mismatch",
                "causal-family contract does not bind the exact raw invention",
            )
        for field, allowed in _CAUSAL_FAMILY_ENUMS.items():
            if contract[field] not in allowed:
                _fail(
                    "causal_family_type_invalid",
                    f"{field} is outside the closed causal vocabulary",
                )
        grounding_paths = contract["target_grounding_paths"]
        if (
            not isinstance(grounding_paths, list)
            or len(grounding_paths) != len(set(grounding_paths))
            or "/invention_request/target_pressure" not in grounding_paths
            or not any(
                str(path).startswith(
                    "/invention_request/protected_successes/"
                )
                for path in grounding_paths
            )
        ):
            _fail(
                "causal_family_grounding_invalid",
                "each causal family must bind target pressure and a protected success",
            )
        for path in grounding_paths:
            _grounding_value(source_freeze, str(path))
        input_ids = contract["literature_causal_input_ids"]
        if (
            not isinstance(input_ids, list)
            or not input_ids
            or len(input_ids) != len(set(input_ids))
            or not set(input_ids) <= causal_input_ids
        ):
            _fail(
                "causal_family_literature_binding_invalid",
                "each family must cite exact semantic claim/warrant/delta inputs",
            )
        normalized = {
            key: copy.deepcopy(contract[key])
            for key in sorted(_CAUSAL_FAMILY_FIELDS)
        }
        if (
            retained_digest is not None
            and retained_digest != canonical_digest(normalized)
        ):
            _fail(
                "causal_family_contract_digest_mismatch",
                "retained causal-family contract digest changed",
            )
        rows.append(
            {
                **normalized,
                "contract_digest": canonical_digest(normalized),
            }
        )
    rows.sort(key=lambda row: row["invention_id"])
    if (
        len(rows) != len(raw_by_id)
        or len({row["invention_id"] for row in rows}) != len(rows)
        or {row["invention_id"] for row in rows} != set(raw_by_id)
    ):
        _fail(
            "causal_family_bijection_invalid",
            "every raw invention requires one distinct causal-family contract",
        )
    return rows


def build_literature_conditioned_invention_freeze(
    source_freeze: Mapping[str, Any],
    *,
    literature_projection: Mapping[str, Any],
    causal_family_contracts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Bind a producer-native freeze to its exact semantic causal input."""

    freeze = _object(source_freeze, "source pre-taxonomy invention freeze")
    _verify_seal(freeze, "content_digest", "source pre-taxonomy invention freeze")
    literature_input = _projection_invention_input(literature_projection)
    contracts = _validated_causal_family_contracts(
        source_freeze=freeze,
        literature_input=literature_input,
        contracts=causal_family_contracts,
    )
    core = {
        "schema_version": "1.0.0",
        "artifact_kind": "literature_conditioned_pre_taxonomy_invention_freeze",
        "conditioned_freeze_id": stable_identifier(
            "literature-conditioned-invention-freeze",
            freeze["content_digest"],
            literature_input["content_digest"],
            contracts,
        ),
        "source_freeze": copy.deepcopy(freeze),
        "source_freeze_digest": freeze["content_digest"],
        "literature_derived_invention_input": literature_input,
        "literature_derived_invention_input_digest": literature_input[
            "content_digest"
        ],
        "causal_family_contracts": contracts,
        "causal_family_contract_set_digest": canonical_digest(contracts),
        "conditioning_relation": (
            "exact_semantic_claim_warrant_assimilation_input_precedes_and_binds_freeze"
        ),
        "authority_nulls": {
            "source_truth_authority": None,
            "literature_benefit_authority": None,
            "creativity_authority": None,
            "semantic_novelty_authority": None,
            "truth_authority": None,
        },
    }
    return _seal(core)


def _validate_literature_conditioned_invention_freeze(
    conditioned_freeze: Mapping[str, Any],
    *,
    literature_projection: Mapping[str, Any],
) -> dict[str, Any]:
    value = _object(conditioned_freeze, "literature-conditioned freeze")
    _verify_seal(value, "content_digest", "literature-conditioned freeze")
    expected = build_literature_conditioned_invention_freeze(
        value["source_freeze"],
        literature_projection=literature_projection,
        causal_family_contracts=value["causal_family_contracts"],
    )
    if value != expected:
        _fail(
            "conditioned_freeze_replay_mismatch",
            "semantic input, raw freeze, or causal-family contracts changed",
        )
    return copy.deepcopy(value)


def _typed_family_contrast(
    left: Mapping[str, Any], right: Mapping[str, Any]
) -> dict[str, Any]:
    """Compare closed causal types, not lexical surface variation."""

    requirements = {
        "primitive_or_relation": (
            left["primitive_kind"],
            left["relation_kind"],
        )
        != (
            right["primitive_kind"],
            right["relation_kind"],
        ),
        "mechanism_dependency": left["mechanism_kind"]
        != right["mechanism_kind"],
        "discriminating_prediction": (
            left["intervention_kind"],
            left["prediction_direction"],
        )
        != (
            right["intervention_kind"],
            right["prediction_direction"],
        ),
        "falsifier_or_correction": left["correction_kind"]
        != right["correction_kind"],
    }
    core = {
        "left_invention_id": left["invention_id"],
        "right_invention_id": right["invention_id"],
        "domain_requirements": requirements,
        "status": (
            "registered_typed_causal_family_contrast"
            if all(requirements.values())
            else "insufficient_typed_causal_contrast"
        ),
    }
    return {**core, "contrast_digest": canonical_digest(core)}


def _largest_registered_family_clique(
    family_ids: Sequence[str],
    contrastive_pairs: set[tuple[str, str]],
) -> list[str]:
    """Find the deterministic largest clique across the exact contract set."""

    ordered = tuple(sorted(family_ids))
    adjacency = {
        family_id: {
            other
            for other in ordered
            if other != family_id
            and tuple(sorted((family_id, other))) in contrastive_pairs
        }
        for family_id in ordered
    }
    best: tuple[str, ...] = ()

    def search(chosen: tuple[str, ...], candidates: tuple[str, ...]) -> None:
        nonlocal best
        if len(chosen) > len(best):
            best = chosen
        if len(chosen) + len(candidates) <= len(best):
            return
        for index, candidate in enumerate(candidates):
            next_candidates = tuple(
                other
                for other in candidates[index + 1 :]
                if other in adjacency[candidate]
            )
            search((*chosen, candidate), next_candidates)
    search((), ordered)
    return list(best)


def _typed_corner_analysis(
    conditioned_freeze: Mapping[str, Any],
) -> dict[str, Any]:
    """Replay the closed typed contrast contract over one exact freeze."""

    family_rows = copy.deepcopy(
        conditioned_freeze["causal_family_contracts"]
    )
    pairwise_contrasts = []
    contrastive_pairs: set[tuple[str, str]] = set()
    for index, left in enumerate(family_rows):
        for right in family_rows[index + 1 :]:
            contrast = _typed_family_contrast(left, right)
            pairwise_contrasts.append(contrast)
            if (
                contrast["status"]
                == "registered_typed_causal_family_contrast"
            ):
                contrastive_pairs.add(
                    (left["invention_id"], right["invention_id"])
                )
    largest_clique = _largest_registered_family_clique(
        [row["invention_id"] for row in family_rows], contrastive_pairs
    )
    core = {
        "schema_version": "1.0.0",
        "artifact_kind": "typed_pre_taxonomy_corner_analysis",
        "contrast_contract": {
            "version": _CORNER_STRUCTURAL_CONTRACT_VERSION,
            "required_family_count": 6,
            "required_pair_domains": [
                "primitive_or_relation",
                "mechanism_dependency",
                "discriminating_prediction",
                "falsifier_or_correction",
            ],
            "comparison_basis": "closed_typed_causal_values_not_lexical_terms",
            "taxonomy_access": False,
        },
        "family_rows": family_rows,
        "pairwise_contrasts": pairwise_contrasts,
        "largest_registered_clique_ids": largest_clique,
        "largest_registered_clique_size": len(largest_clique),
        "six_family_requirement_satisfied": len(largest_clique) >= 6,
        "authority_nulls": {
            "semantic_equivalence_authority": None,
            "semantic_novelty_authority": None,
            "creativity_authority": None,
            "truth_authority": None,
        },
    }
    return _seal(core)


def _corner_grounding_evidence(
    source_freeze: Mapping[str, Any],
) -> list[dict[str, Any]]:
    request = source_freeze["invention_request"]
    paths = [
        "/invention_request/target_pressure",
        *[
            f"/invention_request/root_contradictions/{index}"
            for index, _value in enumerate(request["root_contradictions"])
        ],
        *[
            f"/invention_request/protected_successes/{index}"
            for index, _value in enumerate(request["protected_successes"])
        ],
    ]
    return [
        {
            "path": path,
            "value_digest": canonical_digest(
                _grounding_value(source_freeze, path)
            ),
        }
        for path in paths
    ]


def _corner_assessment_payload(
    conditioned_freeze: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "conditioned_freeze_digest": conditioned_freeze["content_digest"],
        "source_freeze_digest": conditioned_freeze["source_freeze_digest"],
        "literature_derived_invention_input_digest": conditioned_freeze[
            "literature_derived_invention_input_digest"
        ],
        "required_family_count": 6,
        "family_contracts": copy.deepcopy(
            conditioned_freeze["causal_family_contracts"]
        ),
        "grounding_evidence": _corner_grounding_evidence(
            conditioned_freeze["source_freeze"]
        ),
    }


def _expected_corner_assessor_output(
    conditioned_freeze: Mapping[str, Any],
) -> dict[str, Any]:
    analysis = _typed_corner_analysis(conditioned_freeze)
    if analysis["six_family_requirement_satisfied"]:
        _fail(
            "corner_impossibility_unnecessary",
            "the registered typed family requirement is already satisfied",
        )
    payload = _corner_assessment_payload(conditioned_freeze)
    contracts = conditioned_freeze["causal_family_contracts"]
    grounding_paths = sorted(
        {
            path
            for row in contracts
            for path in row["target_grounding_paths"]
        }
    )
    core = {
        "output_kind": "reflection",
        "assessment_kind": "corner_impossibility_assessment",
        "status": "registered_freeze_bounded_impossibility",
        "conditioned_freeze_digest": payload["conditioned_freeze_digest"],
        "source_freeze_digest": payload["source_freeze_digest"],
        "literature_derived_invention_input_digest": payload[
            "literature_derived_invention_input_digest"
        ],
        "required_family_count": 6,
        "observed_family_count": len(contracts),
        "maximum_registered_typed_family_count": analysis[
            "largest_registered_clique_size"
        ],
        "missing_registered_typed_family_count": 6
        - analysis["largest_registered_clique_size"],
        "largest_registered_clique_ids": analysis[
            "largest_registered_clique_ids"
        ],
        "pairwise_contrasts": copy.deepcopy(
            analysis["pairwise_contrasts"]
        ),
        "grounding_evidence": payload["grounding_evidence"],
        "blocking_constraints": [
            {
                "constraint_id": "immutable-freeze-membership",
                "constraint_kind": "sealed_generation_membership",
                "grounding_paths": grounding_paths,
                "witness_digest": conditioned_freeze["content_digest"],
                "statement": (
                    "The exact sealed generation contains no additional family "
                    "bytes that can join the independently replayed clique."
                ),
            },
            {
                "constraint_id": "target-and-literature-binding",
                "constraint_kind": "target_preserving_input_closure",
                "grounding_paths": grounding_paths,
                "witness_digest": conditioned_freeze[
                    "literature_derived_invention_input_digest"
                ],
                "statement": (
                    "Adding a family while preserving the exact target and "
                    "literature input closure requires a new freeze digest."
                ),
            },
        ],
        "scope": "exact_immutable_freeze_only",
        "reopen_condition": (
            "Run and seal a new pre-taxonomy generation against the same or a "
            "newer independently bridged semantic literature input."
        ),
        "authority_nulls": {
            "future_generation_impossibility_authority": None,
            "semantic_impossibility_authority": None,
            "creativity_authority": None,
            "truth_authority": None,
        },
    }
    return {**core, "assessment_digest": canonical_digest(core)}


def _normalized_assessor_budget(
    raw: Mapping[str, Any] | None,
) -> dict[str, Any]:
    candidate = (
        ResearchWorkerAdapter.default_budget()
        if raw is None
        else copy.deepcopy(dict(raw))
    )
    try:
        return asdict(ResourceBudget.from_mapping(candidate))
    except (TypeError, ValueError) as exc:
        raise ConceptualAncestryV3Error(
            "corner_assessor_budget_invalid",
            "assessor budget is not a valid resource budget",
        ) from exc


def _corner_receipt_path(receipt: Mapping[str, Any]) -> Path:
    try:
        return contained_path(
            Path(str(receipt["workspace"]["run_directory"])),
            *Path(str(receipt["receipt_ref"])).parts,
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise ConceptualAncestryV3Error(
            "corner_assessor_receipt_path_invalid",
            "assessor receipt path is absent or escapes its run directory",
        ) from exc


def _corner_assessment_from_receipt(
    conditioned_freeze: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        path = _corner_receipt_path(receipt)
        registered = validate_research_worker_receipt(
            receipt,
            receipt_path=path,
            require_live_authority=True,
        )
        summary = receipt_summary(registered, receipt_path=path)
    except (OSError, ResearchWorkerIntegrityError) as exc:
        raise ConceptualAncestryV3Error(
            "corner_assessor_receipt_replay_failed",
            "registered assessor receipt failed exact replay",
        ) from exc
    payload = _corner_assessment_payload(conditioned_freeze)
    expected_context = {
        "conditioned_freeze_digest": conditioned_freeze["content_digest"],
        "literature_derived_invention_input_digest": conditioned_freeze[
            "literature_derived_invention_input_digest"
        ],
        "assessor_registration_digest": (
            _CORNER_IMPOSSIBILITY_ASSESSOR_DIGEST
        ),
    }
    if (
        registered["role"] != "candidate"
        or registered["operation"] != "reflection"
        or registered["outcome_status"] != "accepted"
        or registered["request_payload"]["payload"] != payload
        or registered["request_payload"]["invocation_context"]
        != expected_context
        or registered["response_payload"]["output"]
        != _expected_corner_assessor_output(conditioned_freeze)
    ):
        _fail(
            "corner_assessor_receipt_binding_mismatch",
            "assessor process changed its freeze, semantic input, or result",
        )
    core = {
        "schema_version": "3.0.0",
        "artifact_kind": (
            "registered_pre_taxonomy_corner_impossibility_assessment"
        ),
        "status": "registered_freeze_bounded_impossibility",
        "conditioned_freeze_digest": conditioned_freeze["content_digest"],
        "source_freeze_digest": conditioned_freeze["source_freeze_digest"],
        "literature_derived_invention_input_digest": conditioned_freeze[
            "literature_derived_invention_input_digest"
        ],
        "assessor_registration": copy.deepcopy(
            _CORNER_IMPOSSIBILITY_ASSESSOR_REGISTRATION
        ),
        "assessor_registration_digest": (
            _CORNER_IMPOSSIBILITY_ASSESSOR_DIGEST
        ),
        "assessment_output": copy.deepcopy(
            registered["response_payload"]["output"]
        ),
        "registered_receipt": copy.deepcopy(registered),
        "receipt_file_sha256": summary["receipt_file_sha256"],
        "receipt_byte_length": summary["receipt_byte_length"],
        "authority_separation": {
            "execution_separation": "distinct_supervised_assessor_process",
            "process_pid": registered["process_event"]["pid"],
            "cognitive_independence": "unavailable",
            "semantic_independence": "unavailable",
        },
        "authority_nulls": {
            "future_generation_impossibility_authority": None,
            "semantic_impossibility_authority": None,
            "creativity_authority": None,
            "truth_authority": None,
        },
    }
    return _seal(core)


def run_registered_corner_impossibility_assessment(
    conditioned_freeze: Mapping[str, Any],
    *,
    run_root: Path | str,
    matched_budget: Mapping[str, Any] | None = None,
    require_kernel_isolation: bool = False,
) -> dict[str, Any]:
    """Execute the freeze-bounded assessment in a distinct supervised process."""

    freeze = _object(conditioned_freeze, "literature-conditioned freeze")
    _verify_seal(freeze, "content_digest", "literature-conditioned freeze")
    _expected_corner_assessor_output(freeze)
    budget = _normalized_assessor_budget(matched_budget)
    worker_script = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "run_conceptual_corner_impossibility_assessor_v3.py"
    )
    adapter = ResearchWorkerAdapter(
        study_id=stable_identifier(
            "typed-corner-impossibility-study",
            freeze["content_digest"],
            _CORNER_IMPOSSIBILITY_ASSESSOR_DIGEST,
        ),
        run_root=run_root,
        worker_script=worker_script,
        approved_dependency_paths=(
            Path(__file__).resolve(),
            worker_script,
        ),
        require_kernel_isolation=require_kernel_isolation,
    )
    receipt = adapter.invoke(
        role="candidate",
        operation="reflection",
        invocation_context={
            "conditioned_freeze_digest": freeze["content_digest"],
            "literature_derived_invention_input_digest": freeze[
                "literature_derived_invention_input_digest"
            ],
            "assessor_registration_digest": (
                _CORNER_IMPOSSIBILITY_ASSESSOR_DIGEST
            ),
        },
        payload=_corner_assessment_payload(freeze),
        budget=budget,
    )
    return _corner_assessment_from_receipt(freeze, receipt)


def build_registered_corner_impossibility_assessment(
    freeze: Mapping[str, Any],
    *,
    run_root: Path | str | None = None,
    matched_budget: Mapping[str, Any] | None = None,
    require_kernel_isolation: bool = False,
) -> dict[str, Any]:
    """Compatibility surface that now requires an actual assessor process."""

    if run_root is None:
        _fail(
            "corner_impossibility_execution_required",
            "a same-module assessment cannot replace a registered process receipt",
        )
    return run_registered_corner_impossibility_assessment(
        freeze,
        run_root=run_root,
        matched_budget=matched_budget,
        require_kernel_isolation=require_kernel_isolation,
    )


def build_grounded_corner_impossibility_record(
    freeze: Mapping[str, Any],
    *,
    grounding_paths: Sequence[str],
    blocking_constraints: Sequence[str],
    reason: str,
    reopen_condition: str,
) -> dict[str, Any]:
    """Reject the legacy caller-authored exception construction surface."""

    del freeze, grounding_paths, blocking_constraints, reason, reopen_condition
    _fail(
        "corner_impossibility_caller_authorship_forbidden",
        "caller prose cannot self-attest a conceptual-corner impossibility",
    )


def _validate_grounded_corner_impossibility(
    record: Mapping[str, Any],
    *,
    freeze: Mapping[str, Any],
) -> dict[str, Any]:
    value = _object(record, "grounded corner impossibility")
    _verify_seal(
        value, "content_digest", "grounded corner impossibility"
    )
    expected = _corner_assessment_from_receipt(
        freeze, value["registered_receipt"]
    )
    if value != expected:
        _fail(
            "corner_impossibility_assessment_replay_mismatch",
            "registered corner assessment differs from exact assessor replay",
        )
    return copy.deepcopy(value)


def build_pre_taxonomy_corner_coverage(
    freeze: Mapping[str, Any],
    *,
    grounded_impossibility: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Require six structurally separated raw families or an exact exception."""

    freeze_value = _object(freeze, "literature-conditioned invention freeze")
    _verify_seal(
        freeze_value, "content_digest", "literature-conditioned invention freeze"
    )
    analysis = _typed_corner_analysis(freeze_value)
    six_families = analysis["six_family_requirement_satisfied"]
    impossibility = (
        _validate_grounded_corner_impossibility(
            grounded_impossibility, freeze=freeze_value
        )
        if grounded_impossibility is not None
        else None
    )
    if six_families and impossibility is not None:
        _fail(
            "corner_impossibility_unnecessary",
            "a grounded exception cannot replace an already satisfied minimum",
        )
    if not six_families and impossibility is None:
        _fail(
            "conceptual_corner_coverage_insufficient",
            "six typed pre-taxonomy families require a registered assessment",
        )
    core = {
        "schema_version": "2.0.0",
        "artifact_kind": "pre_taxonomy_conceptual_corner_coverage",
        "conditioned_freeze_id": freeze_value["conditioned_freeze_id"],
        "freeze_digest": freeze_value["content_digest"],
        "source_freeze_digest": freeze_value["source_freeze_digest"],
        "literature_derived_invention_input_digest": freeze_value[
            "literature_derived_invention_input_digest"
        ],
        "required_family_count": 6,
        "observed_invention_count": len(
            freeze_value["source_freeze"]["raw_inventions"]
        ),
        "registered_typed_family_count": analysis[
            "largest_registered_clique_size"
        ],
        "accepted_family_ids": analysis[
            "largest_registered_clique_ids"
        ],
        "typed_structural_analysis": analysis,
        "status": (
            "six_registered_typed_causal_families"
            if six_families
            else "receipt_bound_freeze_bounded_impossibility_accepted"
        ),
        "grounded_impossibility": impossibility,
        "authority_nulls": {
            "semantic_equivalence_authority": None,
            "semantic_novelty_authority": None,
            "creativity_authority": None,
            "truth_authority": None,
        },
    }
    return _seal(core)


def validate_pre_taxonomy_corner_coverage(
    coverage: Mapping[str, Any],
    *,
    freeze: Mapping[str, Any],
) -> dict[str, Any]:
    """Recompute family axes and the optional exact grounded exception."""

    value = _object(coverage, "pre-taxonomy corner coverage")
    _verify_seal(value, "content_digest", "pre-taxonomy corner coverage")
    expected = build_pre_taxonomy_corner_coverage(
        freeze,
        grounded_impossibility=value.get("grounded_impossibility"),
    )
    if value != expected:
        _fail(
            "conceptual_corner_coverage_replay_mismatch",
            "pre-taxonomy family coverage does not replay",
        )
    return copy.deepcopy(value)


def _taxonomy_replay_context(
    classification: Mapping[str, Any],
    known_taxonomy: Mapping[str, Any],
    corner_coverage: Mapping[str, Any],
) -> dict[str, Any]:
    core = {
        "schema_version": "1.0.0",
        "artifact_kind": "post_freeze_taxonomy_replay_context",
        "known_taxonomy": copy.deepcopy(dict(known_taxonomy)),
        "known_taxonomy_commitment_digest": known_taxonomy_commitment(
            known_taxonomy
        ),
        "pre_taxonomy_corner_coverage": copy.deepcopy(dict(corner_coverage)),
        "classification": copy.deepcopy(dict(classification)),
    }
    return _seal(core)


def build_conceptual_ancestry_literature_basis(
    literature_projection: Mapping[str, Any],
) -> dict[str, Any]:
    """Project exact semantic deltas into the closed reflection-packet shape."""

    projection = _object(
        literature_projection, "semantic literature causal projection"
    )
    _verify_seal(
        projection, "content_digest", "semantic literature causal projection"
    )
    semantic_root = projection["semantic_snapshot_root"]
    literature_input = _projection_invention_input(projection)
    delta_summaries = [
        (
            f"{row['causal_input_id']}:{row['source_id']}:"
            f"{row['assimilation_delta']['event_type']}:"
            f"{row['claim_digest']}"
        )
        for row in literature_input["causal_inputs"]
    ]
    questions = [
        (
            f"Which target-preserving consequence follows from "
            f"{row['causal_input_id']} under "
            f"{row['assimilation_delta']['event_type']}?"
        )
        for row in literature_input["causal_inputs"]
    ]
    return {
        "selected_snapshot_id": semantic_root["snapshot_id"],
        "snapshot_target_id": semantic_root["target_id"],
        "selected_snapshot_digest": semantic_root["content_digest"],
        "search_completed_utc": semantic_root["search_completed_at"],
        "freshness_status": "current",
        "search_receipt_ids": [projection["semantic_bridge_id"]],
        "assimilation_packet_ref": literature_input["input_id"],
        "source_to_theory_delta_summary": delta_summaries,
        "literature_generated_questions": questions,
        "coverage_limitations": copy.deepcopy(
            literature_input["coverage_limits"]
        ),
        "superseded_snapshot_ids": [],
    }


def _validate_reflection_packet(
    packet: Mapping[str, Any],
    *,
    label: str,
    target_id: str,
    run_id: str,
    state_version: int,
    literature_projection: Mapping[str, Any],
) -> dict[str, Any]:
    value = _object(packet, label)
    _validate_schema(
        value,
        "reflective_conceptual_discovery_packet.schema.json",
        label,
    )
    if value["packet_digest"] != canonical_digest(
        value, exclude_keys=("packet_digest",)
    ):
        _fail("reflection_packet_digest_mismatch", f"{label} digest changed")
    validate_packet_invariants(value)
    if (
        value["target_id"] != target_id
        or value["run_id"] != run_id
        or value["state_version"] != state_version
    ):
        _fail(
            "reflection_identity_mismatch",
            f"{label} crossed target, run, or state",
        )
    basis = _object(value["literature_basis"], f"{label} literature basis")
    if basis != build_conceptual_ancestry_literature_basis(
        literature_projection
    ):
        _fail(
            "reflection_literature_mismatch",
            f"{label} does not consume the exact semantic causal projection",
        )
    support = _object(value["support_probe"], f"{label} support probe")
    if support.get("disposition") != "no_probe_needed":
        _fail(
            "same_cycle_support_forbidden",
            f"{label} attempts same-cycle experiment support",
        )
    forbidden_lifecycles = {"proof_ready", "validated", "refuted"}
    if any(
        system.get("lifecycle_state") in forbidden_lifecycles
        for system in value["conceptual_systems"]
    ):
        _fail(
            "same_cycle_proof_forbidden",
            f"{label} promotes a same-cycle proof/result lifecycle",
        )
    return copy.deepcopy(value)


def _system_ids(packet: Mapping[str, Any], label: str) -> list[str]:
    systems = _rows(packet.get("conceptual_systems"), f"{label} systems")
    identifiers = [str(row.get("system_id", "")) for row in systems]
    if (
        not identifiers
        or any(not identifier for identifier in identifiers)
        or len(identifiers) != len(set(identifiers))
    ):
        _fail(
            "conceptual_system_identity_invalid",
            f"{label} systems are empty or repeat identities",
        )
    return identifiers


def _materialization_rows(
    *,
    parent_materialization_receipts: Sequence[Mapping[str, Any]],
    portfolio: Mapping[str, Any],
    merit: Mapping[str, Any],
    parent_packet: Mapping[str, Any],
    lens_execution_bundles: Sequence[Mapping[str, Any]],
    literature_input: Mapping[str, Any],
) -> list[dict[str, Any]]:
    matured = {
        row["invention_id"]: copy.deepcopy(row)
        for row in portfolio["matured_inventions"]
    }
    records = {
        row["invention_id"]: copy.deepcopy(row)
        for row in portfolio["branch_execution_records"]
    }
    execution_rows = [
        validate_full_core_reflection_lens_execution_bundle(
            row,
            candidate=matured.get(str(row.get("candidate_id", "")), {}),
            require_promotion_eligible=True,
        )
        for row in lens_execution_bundles
    ]
    execution_by_candidate = {
        row["candidate_id"]: row for row in execution_rows
    }
    if (
        len(execution_rows) != len(execution_by_candidate)
        or set(execution_by_candidate) != set(matured)
        or any(
            row["literature_derived_invention_input"] != literature_input
            for row in execution_rows
        )
    ):
        _fail(
            "lens_execution_bijection_invalid",
            "every matured candidate requires one distinct six-process lens bundle",
        )
    materialization_records: dict[str, dict[str, Any]] = {}
    for raw_receipt in parent_materialization_receipts:
        receipt = _object(raw_receipt, "parent materialization receipt")
        request = _object(
            receipt.get("request_payload"), "parent materialization request"
        )
        context = _object(
            request.get("invocation_context"),
            "parent materialization context",
        )
        invention_id = str(context.get("candidate_id", ""))
        if invention_id not in matured or invention_id in materialization_records:
            _fail(
                "parent_materialization_receipt_bijection_invalid",
                "parent receipt names an unknown or duplicate candidate",
            )
        materialization_records[invention_id] = (
            validate_parent_system_materialization_receipt(
                receipt,
                candidate=matured[invention_id],
                lens_execution_bundle=execution_by_candidate[invention_id],
            )
        )
    if set(materialization_records) != set(matured):
        _fail(
            "parent_materialization_receipt_bijection_invalid",
            "every matured candidate requires one registered parent producer",
        )
    systems = {
        row["system_id"]: copy.deepcopy(row)
        for row in parent_packet["conceptual_systems"]
    }
    produced_systems = {
        row["parent_conceptual_system"]["system_id"]: copy.deepcopy(
            row["parent_conceptual_system"]
        )
        for row in materialization_records.values()
    }
    if produced_systems != systems:
        _fail(
            "unrelated_parent_system",
            "parent packet systems differ from registered producer output bytes",
        )
    profiles = {
        row["source_id"]: copy.deepcopy(row)
        for row in merit["dimension_profiles"]
        if row["source_kind"] == "invention"
    }
    dispositions = {
        row["invention_id"]: copy.deepcopy(row)
        for row in merit["exploration_dispositions"]
    }
    if set(profiles) != set(matured) or set(dispositions) != set(matured):
        _fail(
            "merit_materialization_incomplete",
            "merit output lacks an exact invention profile/disposition bijection",
        )
    rows: list[dict[str, Any]] = []
    for invention_id in sorted(matured):
        candidate = matured[invention_id]
        record = records[invention_id]
        terminal = record["terminal_receipt"]
        execution_bundle = execution_by_candidate[invention_id]
        materialization = materialization_records[invention_id]
        system_id = materialization["parent_conceptual_system"]["system_id"]
        execution_by_lens = {
            execution["lens_id"]: execution
            for execution in execution_bundle["lens_executions"]
        }
        candidate_core = {
            key: copy.deepcopy(candidate[key])
            for key in (
                "statement",
                "semantic_core",
                "risk_reward",
                "physics_handback",
            )
        }
        lens_units = [
            {
                "lens_id": lens_id,
                "candidate_core": copy.deepcopy(candidate_core),
                "candidate_core_digest": canonical_digest(candidate_core),
                "reflection": copy.deepcopy(
                    execution_by_lens[lens_id]["produced_reflection"]
                ),
                "reflection_digest": canonical_digest(
                    execution_by_lens[lens_id]["produced_reflection"]
                ),
                "physics_handback": copy.deepcopy(
                    candidate["physics_handback"]
                ),
                "lens_execution_receipt": {
                    "execution_record_digest": execution_by_lens[lens_id][
                        "execution_record_digest"
                    ],
                    "receipt_id": execution_by_lens[lens_id][
                        "registered_receipt"
                    ]["receipt_id"],
                    "receipt_ref": execution_by_lens[lens_id][
                        "registered_receipt"
                    ]["receipt_ref"],
                    "receipt_digest": execution_by_lens[lens_id][
                        "registered_receipt"
                    ]["content_digest"],
                    "receipt_file_sha256": execution_by_lens[lens_id][
                        "receipt_file_sha256"
                    ],
                    "process_pid": execution_by_lens[lens_id][
                        "registered_receipt"
                    ]["process_event"]["pid"],
                    "process_started_at": execution_by_lens[lens_id][
                        "registered_receipt"
                    ]["process_event"]["started_at"],
                    "process_completed_at": execution_by_lens[lens_id][
                        "registered_receipt"
                    ]["process_event"]["completed_at"],
                    "matched_budget_digest": execution_by_lens[lens_id][
                        "matched_budget_digest"
                    ],
                },
            }
            for lens_id in DEEP_REFLECTION_LENSES
        ]
        row = {
            "invention_id": invention_id,
            "parent_system_id": system_id,
            "matured_candidate": candidate,
            "matured_candidate_digest": canonical_digest(candidate),
            "literature_derived_invention_input": copy.deepcopy(
                literature_input
            ),
            "literature_derived_invention_input_digest": literature_input[
                "content_digest"
            ],
            "parent_conceptual_system": systems[system_id],
            "parent_conceptual_system_digest": canonical_digest(
                systems[system_id]
            ),
            "materialization_relation": (
                "registered_process_authored_exact_candidate_plus_six_lens_outputs"
            ),
            "parent_materialization_producer": {
                "materialization_record_digest": materialization[
                    "materialization_record_digest"
                ],
                "receipt_id": materialization["registered_receipt"][
                    "receipt_id"
                ],
                "receipt_ref": materialization["registered_receipt"][
                    "receipt_ref"
                ],
                "receipt_digest": materialization["registered_receipt"][
                    "content_digest"
                ],
                "receipt_file_sha256": materialization[
                    "receipt_file_sha256"
                ],
                "receipt_byte_length": materialization[
                    "receipt_byte_length"
                ],
                "conceptual_delta": copy.deepcopy(
                    materialization["conceptual_delta"]
                ),
                "conceptual_delta_digest": materialization[
                    "conceptual_delta_digest"
                ],
                "semantic_authorship": copy.deepcopy(
                    materialization["registered_receipt"][
                        "response_payload"
                    ]["output"]["semantic_authorship"]
                ),
            },
            "merit_dimension_profile": profiles[invention_id],
            "exploration_disposition": dispositions[invention_id],
            "lens_units": lens_units,
            "process_isolation_evidence": {
                "status": "available",
                "evidence_class": "registered_os_process_and_policy_receipt",
                "branch_id": record["branch_id"],
                "branch_record_digest": record["record_digest"],
                "worker_receipt_id": terminal["worker_receipt_id"],
                "worker_receipt_digest": terminal["worker_receipt_digest"],
                "worker_receipt_file_sha256": terminal[
                    "worker_receipt_file_sha256"
                ],
                "isolation_status": terminal["isolation_status"],
                "isolation_backend": terminal["isolation_backend"],
                "network_policy_status": terminal["network_policy_status"],
                "workspace_policy_status": terminal[
                    "workspace_policy_status"
                ],
                "sibling_read_policy_status": terminal[
                    "sibling_read_policy_status"
                ],
                "sibling_write_policy_status": terminal[
                    "sibling_write_policy_status"
                ],
                "process_group_status": terminal["process_group_status"],
                "process_completed_at": terminal["process_completed_at"],
                "registered_response_sha256": terminal["response_sha256"],
                "matured_response_sha256": terminal[
                    "matured_response_sha256"
                ],
            },
            "lens_process_isolation": {
                "status": "available_process_only",
                "evidence_class": (
                    "six_distinct_reopened_registered_process_receipts"
                ),
                "execution_bundle_id": execution_bundle[
                    "execution_bundle_id"
                ],
                "execution_bundle_digest": execution_bundle[
                    "content_digest"
                ],
                "barrier_id": execution_bundle["all_terminal_barrier"][
                    "barrier_id"
                ],
                "barrier_digest": execution_bundle["all_terminal_barrier"][
                    "barrier_digest"
                ],
                "distinct_process_count": execution_bundle[
                    "all_terminal_barrier"
                ]["distinct_process_count"],
                "observed_peak_parallelism": execution_bundle[
                    "all_terminal_barrier"
                ]["observed_peak_parallelism"],
                "all_six_intervals_overlap": execution_bundle[
                    "all_terminal_barrier"
                ]["all_six_intervals_overlap"],
                "reason": (
                    "six local process receipts prove process separation only"
                ),
            },
            "cognitive_isolation": {
                "status": "unavailable",
                "reason": "worker receipts do not attest private cognitive state",
            },
            "semantic_isolation": {
                "status": "unavailable",
                "reason": (
                    "exact content nonredundancy is replayed, not semantic isolation"
                ),
            },
        }
        row["materialization_digest"] = canonical_digest(row)
        rows.append(row)
    return rows


def _reflection_bundle(
    *,
    freeze: Mapping[str, Any],
    portfolio: Mapping[str, Any],
    merit: Mapping[str, Any],
    parent_packet: Mapping[str, Any],
    parent_materialization_receipts: Sequence[Mapping[str, Any]],
    lens_execution_bundles: Sequence[Mapping[str, Any]],
    literature_input: Mapping[str, Any],
) -> dict[str, Any]:
    ordered_execution_bundles = sorted(
        (
            validate_full_core_reflection_lens_execution_bundle(
                row,
                require_promotion_eligible=True,
            )
            for row in lens_execution_bundles
        ),
        key=lambda row: row["candidate_id"],
    )
    materializations = _materialization_rows(
        parent_materialization_receipts=parent_materialization_receipts,
        portfolio=portfolio,
        merit=merit,
        parent_packet=parent_packet,
        lens_execution_bundles=ordered_execution_bundles,
        literature_input=literature_input,
    )
    core = {
        "schema_version": "1.0.0",
        "artifact_kind": "six_sibling_full_core_reflection_bundle",
        "source_pre_taxonomy_freeze": copy.deepcopy(dict(freeze)),
        "source_maturation_portfolio": copy.deepcopy(dict(portfolio)),
        "source_merit_evaluation": copy.deepcopy(dict(merit)),
        "source_literature_derived_invention_input": copy.deepcopy(
            dict(literature_input)
        ),
        "source_literature_derived_invention_input_digest": literature_input[
            "content_digest"
        ],
        "source_lens_execution_bundles": ordered_execution_bundles,
        "source_parent_materialization_receipts": [
            copy.deepcopy(
                next(
                    receipt
                    for receipt in parent_materialization_receipts
                    if receipt["receipt_id"]
                    == row["parent_materialization_producer"]["receipt_id"]
                )
            )
            for row in materializations
        ],
        "parent_reflection_packet": copy.deepcopy(dict(parent_packet)),
        "candidate_materializations": materializations,
        "lens_order": list(DEEP_REFLECTION_LENSES),
        "reflection_protocol": {
            "full_candidate_core_repeated_per_lens": True,
            "lens_transformation_authored_inside_each_process": True,
            "upstream_lens_record_accepted": False,
            "one_lens_output_per_sibling_unit": True,
            "parent_system_registered_producer_required": True,
            "typed_before_after_delta_required": True,
            "parent_candidate_content_materialized_before_adjudication": True,
            "cross_lens_record_inside_one_unit": False,
            "process_evidence_scope": (
                "six_distinct_supervised_local_process_receipts_only"
            ),
            "lens_process_isolation": "available_process_only",
            "all_six_intervals_overlap_required": True,
            "matched_budget_required": True,
            "cognitive_isolation": "unavailable",
            "semantic_isolation": "unavailable",
        },
        "authority_boundary": _REFLECTION_BOUNDARY,
    }
    return _seal(core)


def _candidate_bindings_from_evidence(
    evidence: Mapping[str, Any],
) -> dict[str, str]:
    receipt = _object(
        evidence.get("unblinding_receipt"), "adjudication unblinding receipt"
    )
    rows = _rows(
        receipt.get("candidate_bindings"), "adjudication candidate bindings"
    )
    bindings = {
        str(row.get("candidate_alias", "")): str(row.get("system_id", ""))
        for row in rows
    }
    if (
        len(bindings) != len(rows)
        or any(not alias or not system_id for alias, system_id in bindings.items())
    ):
        _fail(
            "adjudication_candidate_binding_invalid",
            "adjudication candidate bindings are not an exact alias map",
        )
    return bindings


def _worker_receipt_ids(portfolio: Mapping[str, Any]) -> list[str]:
    identifiers = sorted(
        str(row["terminal_receipt"]["worker_receipt_id"])
        for row in portfolio["branch_execution_records"]
    )
    if len(identifiers) != len(set(identifiers)):
        _fail("worker_receipt_identity_invalid", "worker receipt IDs repeat")
    return identifiers


def _adjudication_replay(
    *,
    evidence: Mapping[str, Any],
    packet: Mapping[str, Any],
    frozen_genealogy: Sequence[Mapping[str, Any]],
    theory_state_digest: str,
    literature_snapshot_digest: str,
    high_risk_portfolio_digest: str,
    proposer_receipt_ids: Sequence[str],
    previous_evidence: Mapping[str, Any] | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    systems = [copy.deepcopy(dict(row)) for row in packet["conceptual_systems"]]
    rounds = [copy.deepcopy(dict(row)) for row in packet["reflection_rounds"]]
    genealogy = [copy.deepcopy(dict(row)) for row in frozen_genealogy]
    bindings = _candidate_bindings_from_evidence(evidence)
    proposer_ids = [str(value) for value in proposer_receipt_ids]
    validate_adjudication_evidence(
        evidence,
        systems=systems,
        reflection_rounds=rounds,
        frozen_genealogy=genealogy,
        candidate_bindings=bindings,
        theory_state_digest=theory_state_digest,
        literature_snapshot_digest=literature_snapshot_digest,
        high_risk_portfolio_digest=high_risk_portfolio_digest,
        proposer_receipt_ids=proposer_ids,
        previous_evidence=previous_evidence,
    )
    preference = validate_sealed_preference_authority(
        evidence,
        target_id=str(packet["target_id"]),
        run_id=str(packet["run_id"]),
        state_version=int(packet["state_version"]),
        system_ids=[str(row["system_id"]) for row in systems],
        stage_id=str(evidence["stage_id"]),
        systems=systems,
        reflection_rounds=rounds,
    )
    core = {
        "schema_version": "1.0.0",
        "artifact_kind": "full_conceptual_adjudication_replay",
        "stage_id": evidence["stage_id"],
        "evidence": copy.deepcopy(dict(evidence)),
        "systems": systems,
        "reflection_rounds": rounds,
        "frozen_genealogy": genealogy,
        "candidate_bindings": bindings,
        "theory_state_digest": theory_state_digest,
        "literature_snapshot_digest": literature_snapshot_digest,
        "high_risk_portfolio_digest": high_risk_portfolio_digest,
        "proposer_receipt_ids": proposer_ids,
        "previous_evidence": (
            copy.deepcopy(dict(previous_evidence))
            if previous_evidence is not None
            else None
        ),
        "preference_set": preference,
        "replay_scope": {
            "blind_packet_and_judges": "replayed",
            "unblinding": "replayed",
            "systems": "replayed",
            "reflection_rounds": "replayed",
            "frozen_genealogy": "replayed",
            "semantic_signature_closure": "replayed",
            "typed_unification_closure": "replayed",
            "set_valued_preference": "replayed",
        },
    }
    return _seal(core), preference


def _validate_adjudication_replay(
    replay: Mapping[str, Any],
    *,
    packet: Mapping[str, Any],
    expected_stage_id: str,
    literature_snapshot_digest: str,
    high_risk_portfolio_digest: str,
    proposer_receipt_ids: Sequence[str],
    previous_evidence: Mapping[str, Any] | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    value = _object(replay, "full adjudication replay")
    _verify_seal(value, "content_digest", "full adjudication replay")
    if (
        value["artifact_kind"] != "full_conceptual_adjudication_replay"
        or value["stage_id"] != expected_stage_id
        or value["evidence"]["stage_id"] != expected_stage_id
        or value["systems"] != packet["conceptual_systems"]
        or value["reflection_rounds"] != packet["reflection_rounds"]
        or value["literature_snapshot_digest"] != literature_snapshot_digest
        or value["high_risk_portfolio_digest"] != high_risk_portfolio_digest
        or value["proposer_receipt_ids"] != list(proposer_receipt_ids)
        or value["previous_evidence"]
        != (
            copy.deepcopy(dict(previous_evidence))
            if previous_evidence is not None
            else None
        )
    ):
        _fail(
            "adjudication_replay_binding_mismatch",
            "adjudication replay differs from its exact frozen source closure",
        )
    expected, preference = _adjudication_replay(
        evidence=value["evidence"],
        packet=packet,
        frozen_genealogy=value["frozen_genealogy"],
        theory_state_digest=value["theory_state_digest"],
        literature_snapshot_digest=literature_snapshot_digest,
        high_risk_portfolio_digest=high_risk_portfolio_digest,
        proposer_receipt_ids=proposer_receipt_ids,
        previous_evidence=previous_evidence,
    )
    if value != expected:
        _fail(
            "adjudication_replay_mismatch",
            "complete frozen adjudication genealogy does not replay",
        )
    return copy.deepcopy(value), preference


def _final_preference_authority(
    evidence: Mapping[str, Any], preference: Mapping[str, Any]
) -> dict[str, Any]:
    core = {
        "evidence_id": evidence["evidence_id"],
        "evidence_digest": evidence["evidence_digest"],
        "stage_id": evidence["stage_id"],
        "preference_set": copy.deepcopy(dict(preference)),
        "authority_shape": "set_valued_no_singular_collapse",
        "authority_boundary": _FINAL_PREFERENCE_BOUNDARY,
    }
    return {**core, "authority_digest": canonical_digest(core)}


def _stage_record(
    stage_id: str,
    artifact: Mapping[str, Any],
    prior_stages: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    artifact_value = _object(artifact, f"{stage_id} artifact")
    predecessors = [
        {
            "stage_id": predecessor_id,
            "stage_digest": prior_stages[predecessor_id]["stage_digest"],
        }
        for predecessor_id in _PREDECESSOR_STAGE_IDS[stage_id]
    ]
    core = {
        "stage_index": MANDATORY_STAGE_ORDER.index(stage_id),
        "stage_id": stage_id,
        "artifact_kind": _STAGE_KINDS[stage_id],
        "artifact": artifact_value,
        "artifact_digest": canonical_digest(artifact_value),
        "predecessors": predecessors,
    }
    return {**core, "stage_digest": canonical_digest(core)}


def _edge_material() -> list[dict[str, Any]]:
    return [
        {
            "stage_id": stage_id,
            "predecessor_stage_ids": list(_PREDECESSOR_STAGE_IDS[stage_id]),
        }
        for stage_id in MANDATORY_STAGE_ORDER
    ]


def _same_cycle_support_boundary(
    source_state_version: int,
) -> dict[str, Any]:
    return {
        "status": "theory_descendant_only",
        "theory_generation": source_state_version + 1,
        "earliest_proof_or_experiment_generation": source_state_version + 2,
        "same_cycle_proof_artifact_ids": [],
        "same_cycle_experiment_artifact_ids": [],
        "proof_may_inform_ancestry": False,
        "experiment_may_inform_ancestry": False,
        "boundary": (
            "Proof and experiment artifacts may descend from theory N only "
            "after this ancestry is sealed; they cannot be ancestors or "
            "same-cycle support for theory N."
        ),
    }


def build_conceptual_ancestry_v3(
    *,
    target_id: str,
    run_id: str,
    source_state_version: int,
    theory_state_digest: str,
    present_use_at: str,
    bounded_literature_bundle: Mapping[str, Any],
    semantic_literature_snapshot: Mapping[str, Any],
    literature_snapshot_capture_bridge: Mapping[str, Any],
    known_taxonomy: Mapping[str, Any],
    invention_freeze: Mapping[str, Any],
    causal_family_contracts: Sequence[Mapping[str, Any]],
    taxonomy_classification: Mapping[str, Any],
    maturation_portfolio: Mapping[str, Any],
    hard_integrity_receipt: Mapping[str, Any],
    merit_evaluation: Mapping[str, Any],
    lens_execution_bundles: Sequence[Mapping[str, Any]],
    parent_materialization_receipts: Sequence[Mapping[str, Any]],
    grounded_corner_impossibility: Mapping[str, Any] | None,
    parent_reflection_packet: Mapping[str, Any],
    parent_adjudication_evidence: Mapping[str, Any],
    parent_frozen_genealogy: Sequence[Mapping[str, Any]],
    synthesis_packet: Mapping[str, Any],
    final_adjudication_evidence: Mapping[str, Any],
    final_frozen_genealogy: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Build theory-N ancestry from exact registered semantic producers."""

    validate_identifier(target_id, "target_id")
    validate_identifier(run_id, "run_id")
    state_version = _state_version(
        source_state_version, "source_state_version"
    )
    validate_digest(theory_state_digest)
    literature = validate_bounded_current_literature_bundle(
        bounded_literature_bundle,
        present_use_at=present_use_at,
    )
    if (
        literature["target_id"] != target_id
        or literature["run_id"] != run_id
        or literature["state_version"] != state_version
    ):
        _fail(
            "literature_identity_mismatch",
            "bounded literature crossed ancestry target, run, or state",
        )
    projection = build_conceptual_ancestry_literature_projection(
        literature_bundle=literature,
        semantic_snapshot=semantic_literature_snapshot,
        literature_snapshot_capture_bridge=(
            literature_snapshot_capture_bridge
        ),
        present_use_at=present_use_at,
    )
    freeze = _object(invention_freeze, "pre-taxonomy invention freeze")
    conditioned_freeze = build_literature_conditioned_invention_freeze(
        freeze,
        literature_projection=projection,
        causal_family_contracts=causal_family_contracts,
    )
    classification = _object(
        taxonomy_classification, "post-freeze taxonomy classification"
    )
    portfolio = _object(maturation_portfolio, "maturation portfolio")
    integrity = _object(hard_integrity_receipt, "hard integrity receipt")
    merit = _object(merit_evaluation, "merit evaluation")
    corner_coverage = build_pre_taxonomy_corner_coverage(
        conditioned_freeze,
        grounded_impossibility=grounded_corner_impossibility,
    )
    parent_packet = _validate_reflection_packet(
        parent_reflection_packet,
        label="parent reflection packet",
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
        literature_projection=projection,
    )
    if parent_packet["conceptual_adjudication_evidence"] is not None:
        _fail(
            "adjudication_stage_reordered",
            "parent proposal cannot embed adjudication evidence",
        )
    taxonomy_context = _taxonomy_replay_context(
        classification, known_taxonomy, corner_coverage
    )
    reflection_bundle = _reflection_bundle(
        freeze=conditioned_freeze,
        portfolio=portfolio,
        merit=merit,
        parent_packet=parent_packet,
        parent_materialization_receipts=parent_materialization_receipts,
        lens_execution_bundles=lens_execution_bundles,
        literature_input=projection[
            "literature_derived_invention_input"
        ],
    )
    proposer_receipt_ids = _worker_receipt_ids(portfolio)
    parent_replay, _parent_preference = _adjudication_replay(
        evidence=parent_adjudication_evidence,
        packet=parent_packet,
        frozen_genealogy=parent_frozen_genealogy,
        theory_state_digest=theory_state_digest,
        literature_snapshot_digest=projection[
            "semantic_snapshot_root"
        ]["content_digest"],
        high_risk_portfolio_digest=portfolio["content_digest"],
        proposer_receipt_ids=proposer_receipt_ids,
        previous_evidence=None,
    )
    synthesis = _validate_reflection_packet(
        synthesis_packet,
        label="theory-only synthesis packet",
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
        literature_projection=projection,
    )
    if (
        synthesis["conceptual_adjudication_evidence"]
        != parent_adjudication_evidence
        or synthesis["packet_id"] == parent_packet["packet_id"]
        or synthesis["packet_digest"] == parent_packet["packet_digest"]
    ):
        _fail(
            "synthesis_predecessor_mismatch",
            "synthesis must be distinct and consume exact parent evidence",
        )
    final_replay, final_preference = _adjudication_replay(
        evidence=final_adjudication_evidence,
        packet=synthesis,
        frozen_genealogy=final_frozen_genealogy,
        theory_state_digest=theory_state_digest,
        literature_snapshot_digest=projection[
            "semantic_snapshot_root"
        ]["content_digest"],
        high_risk_portfolio_digest=portfolio["content_digest"],
        proposer_receipt_ids=proposer_receipt_ids,
        previous_evidence=parent_adjudication_evidence,
    )
    artifacts = {
        "current_bounded_literature": literature,
        "literature_only_projection": projection,
        "pre_taxonomy_invention_freeze": conditioned_freeze,
        "post_freeze_taxonomy_classification": taxonomy_context,
        "isolated_parallel_maturation": portfolio,
        "hard_integrity_replay": integrity,
        "non_saturating_plural_merit_control": merit,
        "six_sibling_full_core_reflections": reflection_bundle,
        "parent_conceptual_adjudication": parent_replay,
        "theory_only_synthesis": synthesis,
        "final_conceptual_adjudication": final_replay,
    }
    stage_map: dict[str, dict[str, Any]] = {}
    for stage_id in MANDATORY_STAGE_ORDER:
        stage_map[stage_id] = _stage_record(
            stage_id, artifacts[stage_id], stage_map
        )
    stages = [stage_map[stage_id] for stage_id in MANDATORY_STAGE_ORDER]
    final_authority = _final_preference_authority(
        final_adjudication_evidence, final_preference
    )
    ancestry_id = stable_identifier(
        "conceptual-ancestry-v3",
        target_id,
        run_id,
        state_version,
        [stage["stage_digest"] for stage in stages],
        final_authority["authority_digest"],
    )
    core = {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": "conceptual_ancestry_v3",
        "ancestry_id": ancestry_id,
        "target_id": target_id,
        "run_id": run_id,
        "source_state_version": state_version,
        "theory_generation": state_version + 1,
        "theory_state_digest": theory_state_digest,
        "known_taxonomy_commitment_digest": known_taxonomy_commitment(
            known_taxonomy
        ),
        "ordered_stage_ids": list(MANDATORY_STAGE_ORDER),
        "stages": stages,
        "edge_set_digest": canonical_digest(_edge_material()),
        "final_preference_authority": final_authority,
        "same_cycle_support_boundary": _same_cycle_support_boundary(
            state_version
        ),
        "authority_nulls": copy.deepcopy(AUTHORITY_NULLS),
        "authority_boundary": _ANCESTRY_BOUNDARY,
    }
    ancestry = _seal(core)
    return validate_conceptual_ancestry_v3(ancestry)


def validate_conceptual_ancestry_v3(
    ancestry: Mapping[str, Any],
    *,
    known_taxonomy: Mapping[str, Any] | None = None,
    present_use_at: str | None = None,
) -> dict[str, Any]:
    """Replay the full mandatory DAG from only its retained source closure."""

    value = _object(ancestry, "conceptual ancestry v3")
    _validate_schema(
        value, "conceptual_ancestry_v3.schema.json", "conceptual ancestry v3"
    )
    _strict(value, _TOP_FIELDS, "conceptual ancestry v3")
    _verify_seal(value, "content_digest", "conceptual ancestry v3")
    if (
        value["schema_version"] != SCHEMA_VERSION
        or value["artifact_kind"] != "conceptual_ancestry_v3"
        or value["ordered_stage_ids"] != list(MANDATORY_STAGE_ORDER)
    ):
        _fail(
            "ancestry_contract_substitution",
            "ancestry version, kind, or mandatory stage vector changed",
        )
    target_id = validate_identifier(value["target_id"], "target_id")
    run_id = validate_identifier(value["run_id"], "run_id")
    state_version = _state_version(
        value["source_state_version"], "source_state_version"
    )
    validate_digest(value["theory_state_digest"])
    if value["theory_generation"] != state_version + 1:
        _fail(
            "theory_generation_mismatch",
            "theory generation must be source state plus one",
        )
    if (
        value["edge_set_digest"] != canonical_digest(_edge_material())
        or value["authority_nulls"] != AUTHORITY_NULLS
        or value["authority_boundary"] != _ANCESTRY_BOUNDARY
    ):
        _fail(
            "ancestry_authority_forgery",
            "edge topology, authority nulls, or boundary changed",
        )
    raw_stages = _rows(value["stages"], "ancestry stages")
    if len(raw_stages) != len(MANDATORY_STAGE_ORDER):
        _fail(
            "ancestry_stage_order_invalid",
            "mandatory ancestry stage count changed",
        )
    stage_map: dict[str, dict[str, Any]] = {}
    for index, (expected_stage_id, stage) in enumerate(
        zip(MANDATORY_STAGE_ORDER, raw_stages, strict=True)
    ):
        _strict(stage, _STAGE_FIELDS, f"ancestry stage {expected_stage_id}")
        if (
            stage["stage_index"] != index
            or stage["stage_id"] != expected_stage_id
            or stage["artifact_kind"] != _STAGE_KINDS[expected_stage_id]
        ):
            _fail(
                "ancestry_stage_order_invalid",
                f"{expected_stage_id} was omitted, reordered, or substituted",
            )
        artifact = _object(stage["artifact"], f"{expected_stage_id} artifact")
        if stage["artifact_digest"] != canonical_digest(artifact):
            _fail(
                "ancestry_artifact_digest_mismatch",
                f"{expected_stage_id} artifact digest changed",
            )
        expected_predecessors = [
            {
                "stage_id": predecessor_id,
                "stage_digest": stage_map[predecessor_id]["stage_digest"],
            }
            for predecessor_id in _PREDECESSOR_STAGE_IDS[expected_stage_id]
        ]
        if stage["predecessors"] != expected_predecessors:
            _fail(
                "ancestry_predecessor_mismatch",
                f"{expected_stage_id} lacks exact predecessor digests",
            )
        unsigned = {
            key: copy.deepcopy(child)
            for key, child in stage.items()
            if key != "stage_digest"
        }
        if stage["stage_digest"] != canonical_digest(unsigned):
            _fail(
                "ancestry_stage_digest_mismatch",
                f"{expected_stage_id} stage digest changed",
            )
        stage_map[expected_stage_id] = stage

    literature = validate_bounded_current_literature_bundle(
        stage_map["current_bounded_literature"]["artifact"],
        present_use_at=present_use_at,
    )
    if (
        literature["target_id"] != target_id
        or literature["run_id"] != run_id
        or literature["state_version"] != state_version
    ):
        _fail(
            "literature_identity_mismatch",
            "bounded literature crossed ancestry identity",
        )
    projection = _validate_literature_projection(
        stage_map["literature_only_projection"]["artifact"],
        bundle=literature,
    )
    conditioned_freeze = _validate_literature_conditioned_invention_freeze(
        stage_map["pre_taxonomy_invention_freeze"]["artifact"],
        literature_projection=projection,
    )
    freeze = _object(
        conditioned_freeze["source_freeze"],
        "source pre-taxonomy invention freeze",
    )
    taxonomy_context = _object(
        stage_map["post_freeze_taxonomy_classification"]["artifact"],
        "post-freeze taxonomy replay context",
    )
    _verify_seal(
        taxonomy_context,
        "content_digest",
        "post-freeze taxonomy replay context",
    )
    taxonomy = _object(
        taxonomy_context["known_taxonomy"], "retained known taxonomy"
    )
    classification = _object(
        taxonomy_context["classification"], "taxonomy classification"
    )
    corner_coverage = _object(
        taxonomy_context["pre_taxonomy_corner_coverage"],
        "pre-taxonomy corner coverage",
    )
    taxonomy_digest = known_taxonomy_commitment(taxonomy)
    if (
        taxonomy_context["artifact_kind"]
        != "post_freeze_taxonomy_replay_context"
        or taxonomy_context["known_taxonomy_commitment_digest"]
        != taxonomy_digest
        or value["known_taxonomy_commitment_digest"] != taxonomy_digest
        or (
            known_taxonomy is not None
            and known_taxonomy_commitment(known_taxonomy) != taxonomy_digest
        )
    ):
        _fail(
            "taxonomy_commitment_mismatch",
            "retained post-freeze taxonomy context does not replay",
        )
    validate_pre_taxonomy_invention_freeze(
        freeze, known_taxonomy=taxonomy
    )
    validate_pre_taxonomy_corner_coverage(
        corner_coverage, freeze=conditioned_freeze
    )
    namespace = _object(freeze["namespace"], "invention freeze namespace")
    if namespace != {
        "target_id": target_id,
        "run_id": run_id,
        "state_version": state_version,
    }:
        _fail(
            "open_world_identity_mismatch",
            "pre-taxonomy freeze crossed ancestry identity",
        )
    validate_post_freeze_taxonomy_classification(
        classification,
        freeze=freeze,
        known_taxonomy=taxonomy,
    )
    portfolio = _object(
        stage_map["isolated_parallel_maturation"]["artifact"],
        "maturation portfolio",
    )
    validate_open_world_maturation_portfolio(
        portfolio,
        freeze=freeze,
        classification=classification,
        known_taxonomy=taxonomy,
    )
    if portfolio["target_id"] != target_id:
        _fail(
            "open_world_identity_mismatch",
            "maturation portfolio crossed target",
        )
    integrity = _object(
        stage_map["hard_integrity_replay"]["artifact"],
        "hard integrity receipt",
    )
    validate_open_world_hard_integrity_receipt(
        integrity, portfolio=portfolio
    )
    merit = _object(
        stage_map["non_saturating_plural_merit_control"]["artifact"],
        "merit evaluation",
    )
    validate_non_saturating_conceptual_merit_evaluation(merit)
    if (
        merit["source_portfolio"] != portfolio
        or merit["hard_integrity_receipt"] != integrity
    ):
        _fail(
            "merit_predecessor_mismatch",
            "merit output substituted its portfolio or integrity receipt",
        )
    reflection_bundle = _object(
        stage_map["six_sibling_full_core_reflections"]["artifact"],
        "six-sibling reflection bundle",
    )
    _verify_seal(
        reflection_bundle,
        "content_digest",
        "six-sibling reflection bundle",
    )
    parent_packet = _validate_reflection_packet(
        reflection_bundle["parent_reflection_packet"],
        label="parent reflection packet",
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
        literature_projection=projection,
    )
    if parent_packet["conceptual_adjudication_evidence"] is not None:
        _fail(
            "adjudication_stage_reordered",
            "parent proposal embeds adjudication before its stage",
        )
    if (
        reflection_bundle["source_pre_taxonomy_freeze"]
        != conditioned_freeze
        or reflection_bundle["source_maturation_portfolio"] != portfolio
        or reflection_bundle["source_merit_evaluation"] != merit
        or reflection_bundle[
            "source_literature_derived_invention_input"
        ]
        != projection["literature_derived_invention_input"]
        or reflection_bundle[
            "source_literature_derived_invention_input_digest"
        ]
        != projection["literature_derived_invention_input"]["content_digest"]
        or reflection_bundle["lens_order"] != list(DEEP_REFLECTION_LENSES)
    ):
        _fail(
            "reflection_producer_binding_mismatch",
            "reflection bundle does not retain exact freeze/portfolio/merit outputs",
        )
    expected_reflections = _reflection_bundle(
        freeze=conditioned_freeze,
        portfolio=portfolio,
        merit=merit,
        parent_packet=parent_packet,
        parent_materialization_receipts=reflection_bundle[
            "source_parent_materialization_receipts"
        ],
        lens_execution_bundles=reflection_bundle[
            "source_lens_execution_bundles"
        ],
        literature_input=projection[
            "literature_derived_invention_input"
        ],
    )
    if reflection_bundle != expected_reflections:
        _fail(
            "reflection_bundle_replay_mismatch",
            "candidate materializations or six full-core lens units changed",
        )
    proposer_receipt_ids = _worker_receipt_ids(portfolio)
    parent_replay, _parent_preference = _validate_adjudication_replay(
        stage_map["parent_conceptual_adjudication"]["artifact"],
        packet=parent_packet,
        expected_stage_id="parent-conceptual-adjudication",
        literature_snapshot_digest=projection[
            "semantic_snapshot_root"
        ]["content_digest"],
        high_risk_portfolio_digest=portfolio["content_digest"],
        proposer_receipt_ids=proposer_receipt_ids,
        previous_evidence=None,
    )
    parent_evidence = parent_replay["evidence"]
    synthesis = _validate_reflection_packet(
        stage_map["theory_only_synthesis"]["artifact"],
        label="theory-only synthesis packet",
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
        literature_projection=projection,
    )
    if (
        synthesis["conceptual_adjudication_evidence"] != parent_evidence
        or synthesis["packet_id"] == parent_packet["packet_id"]
        or synthesis["packet_digest"] == parent_packet["packet_digest"]
    ):
        _fail(
            "synthesis_predecessor_mismatch",
            "synthesis is not a distinct exact child of parent adjudication",
        )
    final_replay, final_preference = _validate_adjudication_replay(
        stage_map["final_conceptual_adjudication"]["artifact"],
        packet=synthesis,
        expected_stage_id="synthesis-conceptual-adjudication",
        literature_snapshot_digest=projection[
            "semantic_snapshot_root"
        ]["content_digest"],
        high_risk_portfolio_digest=portfolio["content_digest"],
        proposer_receipt_ids=proposer_receipt_ids,
        previous_evidence=parent_evidence,
    )
    final_evidence = final_replay["evidence"]
    expected_authority = _final_preference_authority(
        final_evidence, final_preference
    )
    if value["final_preference_authority"] != expected_authority:
        _fail(
            "final_preference_authority_mismatch",
            "final set-valued authority changed or collapsed",
        )
    if value["same_cycle_support_boundary"] != _same_cycle_support_boundary(
        state_version
    ):
        _fail(
            "same_cycle_support_forbidden",
            "same-cycle proof/experiment boundary changed",
        )
    expected_id = stable_identifier(
        "conceptual-ancestry-v3",
        target_id,
        run_id,
        state_version,
        [stage["stage_digest"] for stage in raw_stages],
        expected_authority["authority_digest"],
    )
    if value["ancestry_id"] != expected_id:
        _fail("ancestry_identity_mismatch", "ancestry ID does not replay")
    return copy.deepcopy(value)


def validate_conceptual_ancestry_cycle_binding(
    ancestry: Mapping[str, Any],
    *,
    target_id: str,
    run_id: str,
    source_state_version: int,
    parent_reflection_packet: Mapping[str, Any],
    synthesis_packet: Mapping[str, Any],
    parent_adjudication_evidence: Mapping[str, Any],
    final_adjudication_evidence: Mapping[str, Any],
    conceptual_authority: Mapping[str, Any] | None = None,
    present_use_at: str | None = None,
    experiment_specs: Sequence[Mapping[str, Any]] = (),
    experiment_receipts: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Bind a v3 ancestry to the exact current cycle/gate proposal artifacts."""

    value = validate_conceptual_ancestry_v3(
        ancestry, present_use_at=present_use_at
    )
    if (
        value["target_id"] != target_id
        or value["run_id"] != run_id
        or value["source_state_version"] != source_state_version
    ):
        _fail(
            "cycle_binding_identity_mismatch",
            "ancestry crossed current cycle target, run, or source state",
        )
    stage_map = {stage["stage_id"]: stage["artifact"] for stage in value["stages"]}
    reflected_parent = stage_map["six_sibling_full_core_reflections"][
        "parent_reflection_packet"
    ]
    replayed_parent = stage_map["parent_conceptual_adjudication"]["evidence"]
    replayed_synthesis = stage_map["theory_only_synthesis"]
    replayed_final = stage_map["final_conceptual_adjudication"]["evidence"]
    if (
        reflected_parent != dict(parent_reflection_packet)
        or replayed_parent != dict(parent_adjudication_evidence)
        or replayed_synthesis != dict(synthesis_packet)
        or replayed_final != dict(final_adjudication_evidence)
    ):
        _fail(
            "cycle_binding_artifact_mismatch",
            "cycle proposals/adjudications differ from v3 ancestry bytes",
        )
    if experiment_specs or experiment_receipts:
        _fail(
            "same_cycle_experiment_forbidden",
            "experiments are descendants of theory N, never v3 ancestry inputs",
        )
    preference = value["final_preference_authority"]["preference_set"]
    if conceptual_authority is not None and (
        conceptual_authority.get("synthesis_preference_set") != preference
        or conceptual_authority.get("preferred_system_ids")
        != preference["preferred_system_ids"]
        or conceptual_authority.get("preference_authorized")
        != (preference["decision"] in {"prefer_unique", "retain_plural_nondominated"})
    ):
        _fail(
            "cycle_binding_authority_mismatch",
            "cycle conceptual authority differs from final ancestry preference",
        )
    literature_lineage = stage_map["literature_only_projection"]
    projection = {
        "schema_version": "1.0.0",
        "status": "validated_mandatory_predecessor",
        "ancestry_id": value["ancestry_id"],
        "ancestry_digest": value["content_digest"],
        "theory_generation": value["theory_generation"],
        "literature_bundle_digest": stage_map[
            "current_bounded_literature"
        ]["content_digest"],
        "literature_lineage_projection_id": literature_lineage[
            "projection_id"
        ],
        "literature_lineage_projection_digest": literature_lineage[
            "content_digest"
        ],
        "raw_capture_root": copy.deepcopy(
            literature_lineage["raw_capture_root"]
        ),
        "semantic_bridge_id": literature_lineage["semantic_bridge_id"],
        "semantic_bridge_digest": literature_lineage[
            "semantic_bridge_digest"
        ],
        "semantic_snapshot_root": copy.deepcopy(
            literature_lineage["semantic_snapshot_root"]
        ),
        "literature_consume_before": literature_lineage[
            "consumption_deadline"
        ]["consume_before"],
        "literature_derived_invention_input_digest": literature_lineage[
            "literature_derived_invention_input"
        ]["content_digest"],
        "final_evidence_id": replayed_final["evidence_id"],
        "final_evidence_digest": replayed_final["evidence_digest"],
        "preferred_system_ids": copy.deepcopy(
            preference["preferred_system_ids"]
        ),
        "same_cycle_support_status": value[
            "same_cycle_support_boundary"
        ]["status"],
    }
    projection["binding_digest"] = canonical_digest(projection)
    return projection


__all__ = [
    "AUTHORITY_NULLS",
    "ConceptualAncestryV3Error",
    "DEFAULT_MAX_AGE_SECONDS",
    "MANDATORY_STAGE_ORDER",
    "SCHEMA_VERSION",
    "build_bounded_current_literature_bundle",
    "build_conceptual_ancestry_literature_basis",
    "build_conceptual_ancestry_literature_projection",
    "build_conceptual_ancestry_v3",
    "build_grounded_corner_impossibility_record",
    "build_literature_conditioned_invention_freeze",
    "build_pre_taxonomy_corner_coverage",
    "build_registered_corner_impossibility_assessment",
    "build_registered_adjacent_abstraction_method_lane",
    "run_registered_corner_impossibility_assessment",
    "validate_adjacent_abstraction_method_lane",
    "validate_bounded_current_literature_bundle",
    "validate_conceptual_ancestry_cycle_binding",
    "validate_conceptual_ancestry_v3",
    "validate_pre_taxonomy_corner_coverage",
]
