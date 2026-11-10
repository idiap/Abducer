# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Fail-closed authority for live literature acquisition artifacts.

The web tool exposes a bounded result representation, not a raw search-provider
HTTP response, index snapshot, or ranking trace.  This module makes that
boundary executable.  It validates both the frozen single-web-call v1 format
and the multi-execution v2 format, reconstructs the normalized source records
that a frontier snapshot is allowed to contain, and checks version/correction
lineages before the literature can route theory work.  The v2 format keeps web
discovery and primary repository API observations causally distinct instead of
laundering both through one fictional provider call.

No function here performs a network call or renews freshness.  A validated
bundle is an immutable acquisition record; later use must enter the existing
non-renewing frozen-response replay path.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import stat
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .contracts import (
    ContractError,
    canonical_digest,
    canonical_json,
    stable_identifier,
    validate_payload,
)
from .literature import LANE_TYPES, _merge_sources, validate_assimilation, validate_snapshot


TOOL_RESPONSE_SCHEMA = "literature_tool_response_artifact.schema.json"
TOOL_RESPONSE_SCHEMA_V2 = "literature_tool_response_artifact_v2.schema.json"
VERSION_GRAPH_SCHEMA = "literature_source_version_graph.schema.json"
CURRENT_CAPTURE_SCHEMA = "ym_current_literature_capture.schema.json"
SOURCE_ROUTING_PRECOMMIT_SCHEMA = "source_routing_precommit_certificate.schema.json"
SOURCE_ROUTING_PRE_MAP_POLICY_SCHEMA = "source_routing_pre_map_policy.schema.json"
SOURCE_ROUTING_WARRANT_VALIDATION_SCHEMA = (
    "source_routing_warrant_validation_packet.schema.json"
)
SOURCE_ROUTING_REALIZATION_SCHEMA = "source_routing_realization.schema.json"
TOOL_RESPONSE_KIND = "codex_tool_visible_search_response"
TOOL_RESPONSE_KIND_V2 = "codex_multi_execution_literature_observation"

IDENTITY_PREDICATES = {
    "record_doi",
    "record_member_of_concept",
    "record_version",
}
ORDERING_PREDICATES = {"record_created_at", "record_updated_at"}
RELATION_PREDICATES = {
    "revision": "successor_revision_of",
    "supersedes": "successor_supersedes_predecessor",
    "corrects": "successor_corrects_predecessor",
    "narrows_scope": "successor_narrows_scope",
    "broadens_scope": "successor_broadens_scope",
    "changes_scope": "successor_changes_scope",
    "changes_architecture": "successor_changes_architecture",
}
SCOPE_DELTA_RULES = {
    "unchanged": ("scope_unchanged", None),
    "narrowed": ("successor_narrows_scope", "narrows_scope"),
    "broadened": ("successor_broadens_scope", "broadens_scope"),
    "changed_other": ("successor_changes_scope", "changes_scope"),
    "unresolved": ("scope_delta_unresolved", None),
}
ARCHITECTURE_DELTA_RULES = {
    "unchanged": ("architecture_unchanged", None),
    "changed": ("successor_changes_architecture", "changes_architecture"),
    "unresolved": ("architecture_delta_unresolved", None),
}

SOURCE_ROUTING_ELIGIBILITIES = {
    "blocked_positive_support",
    "unverified_audit_only",
    "negative_evidence_only",
}
SOURCE_ROUTING_MAPPING_PAIRS = {
    "contradicts": {"demote", "retire"},
    "reframes": {"reframe"},
    "leaves_open": {"new_question", "justified_no_change"},
}
SOURCE_ROUTING_SEMANTIC_RELATIONS = {
    "entails",
    "contradicts",
    "leaves_open",
    "unresolved",
}
SOURCE_ROUTING_POLICY = {
    "eligibility_classes": sorted(SOURCE_ROUTING_ELIGIBILITIES),
    "mapping_pairs": {
        relation: sorted(events)
        for relation, events in sorted(SOURCE_ROUTING_MAPPING_PAIRS.items())
    },
    "blocked_or_unverified_forbidden_relations": ["entails"],
    "negative_only_semantic_relations": ["contradicts", "unresolved"],
    "negative_only_mapping_relations": ["contradicts", "leaves_open"],
    "unknown_policy_source_pair": ["leaves_open", "justified_no_change"],
}
SOURCE_ROUTING_PRECOMMIT_STAGES = (
    ("claim_mapping", "frontier-literature-assimilator"),
    ("warrant_validation", "frontier-literature-assimilator"),
    ("assimilation", "frontier-literature-assimilator"),
    ("high_risk_investment", "high-risk-hypothesis-forger"),
    ("parallel_scheduling", "parallel-hypothesis-portfolio"),
    ("canonical_commit", "canonical-discovery-cycle"),
    ("theory_gate_acceptance", "canonical-theory-gate"),
)
SOURCE_ROUTING_PRECOMMIT_BOUNDARY = (
    "post-assimilation routing realization compatibility only; no pre-map "
    "authority, source truth, positive semantic support, peer review, novelty, "
    "exhaustiveness, creativity efficacy, physics value, or investment authority"
)
SOURCE_ROUTING_PRE_MAP_STAGES = (
    "warrant_validation",
    "claim_mapping",
    "assimilation",
)
SOURCE_ROUTING_POST_ASSIMILATION_STAGES = (
    ("high_risk_investment", "high-risk-hypothesis-forger"),
    ("parallel_scheduling", "parallel-hypothesis-portfolio"),
    ("canonical_commit", "canonical-discovery-cycle"),
    ("theory_gate_acceptance", "canonical-theory-gate"),
)
SOURCE_ROUTING_PRE_MAP_BOUNDARY = (
    "pre-map routing policy only; no source truth, semantic entailment, positive "
    "support, peer review, novelty, exhaustiveness, conceptual merit, creativity "
    "efficacy, physics value, experiment authority, or investment authority"
)
SOURCE_ROUTING_REALIZATION_BOUNDARY = (
    "two-phase source-routing realization only; no source truth, semantic "
    "entailment, positive support, peer review, novelty, exhaustiveness, "
    "conceptual merit, creativity efficacy, physics value, experiment authority, "
    "proof authority, or investment authority"
)
SOURCE_ROUTING_WARRANT_VALIDATION_BOUNDARY = (
    "policy-bound local warrant projection only; no source truth, semantic "
    "entailment, positive support, external authentication, peer review, "
    "novelty, exhaustiveness, conceptual merit, creativity efficacy, physics "
    "value, proof authority, experiment authority, or investment authority"
)
SOURCE_ROUTING_LEGACY_COMPATIBILITY_BOUNDARY = (
    "post-assimilation compatibility artifact only; pre-map policy authority is "
    "false and consumers must migrate to source_routing_pre_map_policy plus "
    "source_routing_realization"
)


class LiteratureAcquisitionError(ContractError):
    """A stable, machine-routable acquisition-integrity failure."""

    def __init__(self, reason_code: str, message: str) -> None:
        self.reason_code = reason_code
        super().__init__(f"literature_acquisition[{reason_code}]: {message}")


def _fail(reason_code: str, message: str) -> None:
    raise LiteratureAcquisitionError(reason_code, message)


def top_level_content_digest(payload: Mapping[str, Any], field: str) -> str:
    """Hash an envelope while removing only its own top-level digest field."""

    body = copy.deepcopy(dict(payload))
    body.pop(field, None)
    return canonical_digest(body)


def _timestamp(value: Any, *, field: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise LiteratureAcquisitionError(
            "invalid_timestamp", f"{field} is not an ISO date-time"
        ) from exc
    if parsed.tzinfo is None:
        _fail("invalid_timestamp", f"{field} lacks an explicit timezone")
    return parsed.astimezone(timezone.utc)


def _unique(values: Sequence[Any], *, reason_code: str, label: str) -> None:
    encoded = [canonical_json(value) for value in values]
    if len(encoded) != len(set(encoded)):
        _fail(reason_code, f"{label} are duplicated")


def _validate_self_digest(
    payload: Mapping[str, Any], field: str, *, reason_code: str, label: str
) -> None:
    if payload.get(field) != top_level_content_digest(payload, field):
        _fail(reason_code, f"{label} content digest mismatch")


def _source_routing_map(authority: Mapping[str, Any]) -> dict[str, str]:
    """Resolve one exact validated source-routing authority map.

    Callers may pass either the strict authority itself or its immutable parent
    binding.  No default eligibility is invented at consumption time: absence,
    an extra source, or an open vocabulary value is a hard authority failure.
    """

    candidate: Any = authority.get("source_routing_eligibility")
    if candidate is None:
        nested = authority.get("validated_acquisition_authority")
        if isinstance(nested, Mapping):
            candidate = nested.get("source_routing_eligibility")
    if not isinstance(candidate, Mapping) or not candidate:
        _fail(
            "source_routing_authority_missing",
            "validated acquisition authority lacks source-routing eligibility",
        )
    routing = {str(source_id): str(value) for source_id, value in candidate.items()}
    if any(not source_id for source_id in routing):
        _fail("source_routing_source_id_invalid", "routing authority contains an empty source id")
    invalid = sorted(set(routing.values()) - SOURCE_ROUTING_ELIGIBILITIES)
    if invalid:
        _fail(
            "source_routing_eligibility_invalid",
            f"routing authority contains unsupported eligibility values {invalid}",
        )
    return dict(sorted(routing.items()))


def validate_source_routing_consumption(
    *,
    authority: Mapping[str, Any],
    sources: Sequence[Mapping[str, Any]] | Sequence[str],
    stage: str,
    theory_mappings: Sequence[Mapping[str, Any]] = (),
    semantic_warrants: Sequence[Mapping[str, Any]] = (),
    require_complete_mapping: bool = False,
) -> dict[str, Any]:
    """Fail closed when version authority is consumed as theory pressure.

    This is the single transition from sealed observation/lineage authority to
    mappings, warrants, assimilation, scheduling, investment, or acceptance.
    It deliberately permits negative, reframing, and open-question pressure,
    while no acquired source is allowed to become positive semantic support.
    Negative-only sources are narrower still: they may only contradict or stay
    unresolved.  The returned certificate is deterministic audit evidence, not
    source truth or an investment authorization.
    """

    normalized_stage = str(stage).strip()
    if not normalized_stage:
        _fail("source_routing_stage_missing", "routing consumption requires a stage")
    routing = _source_routing_map(authority)
    source_ids = {
        str(source["source_id"] if isinstance(source, Mapping) else source)
        for source in sources
    }
    if not source_ids or "" in source_ids:
        _fail("source_routing_source_set_invalid", "routing consumption requires source ids")
    if source_ids != set(routing):
        _fail(
            "source_routing_source_set_mismatch",
            "consumed source set differs from the exact validated routing authority: "
            f"missing={sorted(set(routing) - source_ids)}, extra={sorted(source_ids - set(routing))}",
        )

    mapping_sources: set[str] = set()
    checked_rows: list[dict[str, Any]] = []
    for row in theory_mappings:
        source_id = str(row.get("source_id") or "")
        if source_id not in routing:
            _fail(
                "source_routing_mapping_source_unknown",
                f"mapping consumes an unauthorised source {source_id!r}",
            )
        mapping_sources.add(source_id)
        relation = str(row.get("relation") or "")
        event_type = str(row.get("event_type") or "")
        if relation not in SOURCE_ROUTING_MAPPING_PAIRS or event_type not in SOURCE_ROUTING_MAPPING_PAIRS[relation]:
            _fail(
                "source_routing_relation_event_unsafe",
                f"source {source_id!r} uses unsafe relation/event pair {(relation, event_type)!r}",
            )
        semantic_relation = row.get("semantic_relation")
        if semantic_relation is not None:
            semantic_relation = str(semantic_relation)
            if semantic_relation not in SOURCE_ROUTING_SEMANTIC_RELATIONS:
                _fail(
                    "source_routing_semantic_relation_invalid",
                    f"source {source_id!r} uses unsupported semantic relation {semantic_relation!r}",
                )
        eligibility = routing[source_id]
        if eligibility in {"blocked_positive_support", "unverified_audit_only"} and (
            semantic_relation == "entails"
        ):
            _fail(
                "source_routing_positive_support_forbidden",
                f"{eligibility} source {source_id!r} cannot entail a theory object",
            )
        if eligibility == "negative_evidence_only":
            if relation not in {"contradicts", "leaves_open"} or semantic_relation not in {
                None,
                "contradicts",
                "unresolved",
            }:
                _fail(
                    "source_routing_negative_only_violation",
                    f"negative-only source {source_id!r} was consumed outside contradiction/unresolved routing",
                )
        checked_rows.append(
            {
                "row_kind": "theory_mapping",
                "source_id": source_id,
                "eligibility": eligibility,
                "relation": relation,
                "event_type": event_type,
                "semantic_relation": semantic_relation,
                "row_digest": canonical_digest(row),
            }
        )
    if require_complete_mapping and mapping_sources != source_ids:
        _fail(
            "source_routing_mapping_coverage_incomplete",
            "routing stage does not map every acquired source: "
            f"missing={sorted(source_ids - mapping_sources)}, extra={sorted(mapping_sources - source_ids)}",
        )

    for row in semantic_warrants:
        source_id = str(row.get("source_id") or "")
        if source_id not in routing:
            _fail(
                "source_routing_warrant_source_unknown",
                f"semantic warrant consumes an unauthorised source {source_id!r}",
            )
        relation = str(row.get("relation") or "")
        if relation not in SOURCE_ROUTING_SEMANTIC_RELATIONS:
            _fail(
                "source_routing_semantic_relation_invalid",
                f"source {source_id!r} uses unsupported warrant relation {relation!r}",
            )
        eligibility = routing[source_id]
        if eligibility in {"blocked_positive_support", "unverified_audit_only"} and relation == "entails":
            _fail(
                "source_routing_positive_support_forbidden",
                f"{eligibility} source {source_id!r} cannot carry an entailment warrant",
            )
        if eligibility == "negative_evidence_only" and relation not in {
            "contradicts",
            "unresolved",
        }:
            _fail(
                "source_routing_negative_only_violation",
                f"negative-only source {source_id!r} has warrant relation {relation!r}",
            )
        checked_rows.append(
            {
                "row_kind": "semantic_warrant",
                "source_id": source_id,
                "eligibility": eligibility,
                "relation": relation,
                "row_digest": canonical_digest(row),
            }
        )

    certificate = {
        "certificate_version": "1.0",
        "stage": normalized_stage,
        "source_routing_eligibility": routing,
        "source_ids": sorted(source_ids),
        "mapping_source_ids": sorted(mapping_sources),
        "require_complete_mapping": bool(require_complete_mapping),
        "checked_rows": sorted(
            checked_rows,
            key=lambda item: (
                item["row_kind"],
                item["source_id"],
                item["row_digest"],
            ),
        ),
        "policy_digest": canonical_digest(SOURCE_ROUTING_POLICY),
        "authority_boundary": (
            "version-state routing only; no source truth, positive semantic support, "
            "peer-review, novelty, exhaustiveness, physics value, or investment authority"
        ),
    }
    certificate["content_digest"] = canonical_digest(certificate)
    return certificate


def _strict_acquisition_authority(authority: Mapping[str, Any]) -> dict[str, Any]:
    """Return the closed strict authority projection used by a precommit.

    Target runners commonly carry byte descriptors and other transport fields
    around the validated acquisition authority.  A canonical precommit embeds
    only the closed semantic authority returned by
    :func:`validate_capture_acquisition_bundle`; no eligibility defaults or
    caller-specific extension fields survive this boundary.
    """

    candidate: Any = authority.get("validated_acquisition_authority")
    if candidate is None:
        candidate = authority
    if not isinstance(candidate, Mapping):
        _fail(
            "source_routing_precommit_authority_missing",
            "source-routing precommit requires validated acquisition authority",
        )
    required = {
        "capture_content_digest",
        "acquisition_content_digest",
        "tool_response_content_digests",
        "version_graph_content_digests",
        "source_ids",
        "source_routing_eligibility",
        "authority_boundary",
    }
    if set(candidate) != required:
        _fail(
            "source_routing_precommit_authority_open",
            "validated acquisition authority is missing fields or contains unbound extensions",
        )
    strict = {
        "capture_content_digest": str(candidate["capture_content_digest"]),
        "acquisition_content_digest": str(candidate["acquisition_content_digest"]),
        "tool_response_content_digests": sorted(
            str(value) for value in candidate["tool_response_content_digests"]
        ),
        "version_graph_content_digests": sorted(
            str(value) for value in candidate["version_graph_content_digests"]
        ),
        "source_ids": sorted(str(value) for value in candidate["source_ids"]),
        "source_routing_eligibility": _source_routing_map(candidate),
        "authority_boundary": str(candidate["authority_boundary"]),
    }
    if strict["source_ids"] != sorted(strict["source_routing_eligibility"]):
        _fail(
            "source_routing_precommit_authority_source_mismatch",
            "validated acquisition source index differs from routing eligibility",
        )
    return strict


def _semantic_warrants(snapshot: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Flatten source warrants in a deterministic, source-bound order."""

    warrants: list[dict[str, Any]] = []
    for source in sorted(snapshot.get("sources", []), key=lambda row: str(row["source_id"])):
        source_id = str(source["source_id"])
        for raw in source.get("semantic_warrants", []):
            if not isinstance(raw, Mapping):
                _fail(
                    "source_routing_precommit_warrant_invalid",
                    f"source {source_id!r} contains a non-object semantic warrant",
                )
            if "source_id" in raw:
                _fail(
                    "source_routing_precommit_warrant_source_mismatch",
                    "snapshot semantic warrants must inherit source identity from "
                    f"their enclosing source {source_id!r}",
                )
            # ``source_id`` is intentionally forbidden inside the strict
            # snapshot warrant schema.  Add the already validated enclosing
            # identity only at this routing projection boundary.
            warrant = {
                **copy.deepcopy(dict(raw)),
                "source_id": source_id,
            }
            warrants.append(warrant)
    return sorted(
        warrants,
        key=lambda row: (str(row["source_id"]), canonical_json(row)),
    )


def derive_source_routing_semantic_warrants(
    snapshot: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Reopen the exact source-bound warrants used by routing authority.

    Canonical consumers need a public replay boundary rather than importing an
    implementation helper from this module.  Validation comes first so callers
    cannot use a merely well-shaped, self-authored warrant list as historical
    source authority; the returned order is then the same deterministic order
    consumed by the pre-map policy and post-assimilation realization.
    """

    validate_snapshot(dict(snapshot))
    return _semantic_warrants(snapshot)


def build_source_routing_warrant_validation_packet(
    *,
    policy: Mapping[str, Any],
    snapshot: Mapping[str, Any],
) -> dict[str, Any]:
    """Execute the deterministic policy-bound warrant-validation projection.

    This stage does not accept a caller-supplied warrant list.  It reopens the
    exact snapshot, projects each nested warrant through its enclosing source
    identity, applies the policy's routing restrictions, and seals both empty
    and non-empty warrant coverage explicitly.
    """

    sealed_policy = copy.deepcopy(dict(policy))
    sealed_snapshot = copy.deepcopy(dict(snapshot))
    validate_payload(sealed_policy, SOURCE_ROUTING_PRE_MAP_POLICY_SCHEMA)
    if sealed_policy.get("policy_digest") != top_level_content_digest(
        sealed_policy, "policy_digest"
    ):
        _fail(
            "source_routing_warrant_policy_digest_mismatch",
            "warrant validation received a self-digest-invalid pre-map policy",
        )
    validate_snapshot(sealed_snapshot)
    snapshot_binding = sealed_policy["snapshot_binding"]
    if (
        snapshot_binding["snapshot_id"] != sealed_snapshot["snapshot_id"]
        or snapshot_binding["snapshot_digest"]
        != sealed_snapshot["content_digest"]
        or snapshot_binding["target_id"] != sealed_snapshot["target_id"]
        or snapshot_binding["theory_state_digest"]
        != sealed_snapshot["theory_state_digest"]
    ):
        _fail(
            "source_routing_warrant_snapshot_mismatch",
            "warrant validation snapshot differs from the sealed policy binding",
        )
    expected_source_state = _source_routing_source_state(
        strict_authority=sealed_policy["acquisition_authority"],
        snapshot=sealed_snapshot,
    )
    if sealed_policy["source_state"] != expected_source_state:
        _fail(
            "source_routing_warrant_source_state_mismatch",
            "warrant validation source state does not replay from the snapshot",
        )
    warrant_contracts = [
        row
        for row in sealed_policy["algorithm_contracts"]
        if row["stage"] == "warrant_validation"
    ]
    if len(warrant_contracts) != 1:
        _fail(
            "source_routing_warrant_contract_missing",
            "warrant validation requires one exact policy algorithm contract",
        )
    warrant_contract = warrant_contracts[0]
    warrants = derive_source_routing_semantic_warrants(sealed_snapshot)
    warrant_ids = [str(row["warrant_id"]) for row in warrants]
    if len(warrant_ids) != len(set(warrant_ids)):
        _fail(
            "source_routing_warrant_identity_duplicate",
            "warrant validation produced duplicate warrant identities",
        )
    source_ids = list(expected_source_state["ordered_source_ids"])
    explicit_source_ids = sorted({str(row["source_id"]) for row in warrants})
    sources_without_warrants = sorted(set(source_ids) - set(explicit_source_ids))
    routing_certificate = validate_source_routing_consumption(
        authority=sealed_policy["acquisition_authority"],
        sources=sealed_snapshot["sources"],
        stage="warrant_validation",
        semantic_warrants=warrants,
    )
    semantic_input_digest = canonical_digest(
        {
            "pre_map_policy_digest": sealed_policy["policy_digest"],
            "snapshot_digest": sealed_snapshot["content_digest"],
            "source_state_digest": expected_source_state[
                "source_state_digest"
            ],
        }
    )
    semantic_output_digest = canonical_digest(warrants)
    packet_id = stable_identifier(
        "source-routing-warrant-validation",
        sealed_policy["target_id"],
        sealed_policy["run_id"],
        sealed_policy["state_version"],
        sealed_policy["policy_digest"],
        sealed_snapshot["content_digest"],
        warrant_contract["contract_digest"],
        semantic_output_digest,
    )
    packet = {
        "schema_version": "1.0.0",
        "packet_id": packet_id,
        "target_id": sealed_policy["target_id"],
        "run_id": sealed_policy["run_id"],
        "state_version": sealed_policy["state_version"],
        "policy_binding": {
            "policy_id": sealed_policy["policy_id"],
            "policy_digest": sealed_policy["policy_digest"],
            "snapshot_id": sealed_snapshot["snapshot_id"],
            "snapshot_digest": sealed_snapshot["content_digest"],
            "source_state_digest": expected_source_state[
                "source_state_digest"
            ],
            "warrant_stage_contract_digest": warrant_contract[
                "contract_digest"
            ],
        },
        "ordered_source_ids": source_ids,
        "explicit_warrant_source_ids": explicit_source_ids,
        "sources_without_explicit_warrants": sources_without_warrants,
        "validated_warrants": warrants,
        "warrant_ids": warrant_ids,
        "routing_certificate": routing_certificate,
        "semantic_input_digest": semantic_input_digest,
        "semantic_output_digest": semantic_output_digest,
        "authority_boundary": SOURCE_ROUTING_WARRANT_VALIDATION_BOUNDARY,
    }
    packet["packet_digest"] = canonical_digest(packet)
    validate_payload(packet, SOURCE_ROUTING_WARRANT_VALIDATION_SCHEMA)
    return packet


def validate_source_routing_warrant_validation_packet(
    packet: Mapping[str, Any],
    *,
    policy: Mapping[str, Any],
    snapshot: Mapping[str, Any],
) -> dict[str, Any]:
    """Reject a warrant packet unless exact deterministic execution rebuilds it."""

    observed = copy.deepcopy(dict(packet))
    validate_payload(observed, SOURCE_ROUTING_WARRANT_VALIDATION_SCHEMA)
    if observed.get("packet_digest") != top_level_content_digest(
        observed, "packet_digest"
    ):
        _fail(
            "source_routing_warrant_packet_digest_mismatch",
            "warrant validation packet content digest mismatch",
        )
    expected = build_source_routing_warrant_validation_packet(
        policy=policy,
        snapshot=snapshot,
    )
    if observed != expected:
        _fail(
            "source_routing_warrant_packet_replay_mismatch",
            "warrant validation packet differs from deterministic replay",
        )
    return observed


def _normalize_source_routing_algorithm_contracts(
    algorithm_contracts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Close externally governed mapper, warrant, and assimilation identities.

    Algorithm and configuration identities are not inferred from completed
    output.  The caller must supply the exact three contracts from its approved
    operator/algorithm registry; validators receive that authority again and
    therefore reject a fully rehashed, self-minted replacement.
    """

    if not isinstance(algorithm_contracts, Sequence) or isinstance(
        algorithm_contracts, (str, bytes, bytearray)
    ):
        _fail(
            "source_routing_pre_map_algorithm_contracts_invalid",
            "algorithm contracts must be an ordered three-row sequence",
        )
    base_fields = {
        "stage",
        "component_id",
        "algorithm_id",
        "config_id",
        "config_digest",
        "authority_class",
    }
    normalized: list[dict[str, Any]] = []
    for index, raw in enumerate(algorithm_contracts):
        if not isinstance(raw, Mapping):
            _fail(
                "source_routing_pre_map_algorithm_contract_invalid",
                f"algorithm contract {index} is not an object",
            )
        fields = frozenset(raw)
        if fields not in {
            frozenset(base_fields),
            frozenset(base_fields | {"contract_digest"}),
        }:
            _fail(
                "source_routing_pre_map_algorithm_contract_open",
                f"algorithm contract {index} has unknown or missing fields",
            )
        contract = {field: copy.deepcopy(raw[field]) for field in sorted(base_fields)}
        contract["stage"] = str(contract["stage"])
        for field in (
            "component_id",
            "algorithm_id",
            "config_id",
            "config_digest",
            "authority_class",
        ):
            contract[field] = str(contract[field])
            if not contract[field]:
                _fail(
                    "source_routing_pre_map_algorithm_contract_invalid",
                    f"algorithm contract {index} has an empty {field}",
                )
        contract_digest = canonical_digest(contract)
        if raw.get("contract_digest") not in {None, contract_digest}:
            _fail(
                "source_routing_pre_map_algorithm_contract_digest_mismatch",
                f"algorithm contract {index} has an invalid self-digest",
            )
        contract["contract_digest"] = contract_digest
        normalized.append(contract)
    if [row["stage"] for row in normalized] != list(SOURCE_ROUTING_PRE_MAP_STAGES):
        _fail(
            "source_routing_pre_map_algorithm_stage_order_invalid",
            "algorithm contracts must occur exactly once in warrant, mapping, assimilation order",
        )
    _unique(
        [row["contract_digest"] for row in normalized],
        reason_code="source_routing_pre_map_algorithm_contract_duplicate",
        label="source-routing algorithm contracts",
    )
    return normalized


def _source_routing_effect_permission(source_id: str, eligibility: str) -> dict[str, Any]:
    """Derive the complete allowed-effect row for one acquired source state."""

    if eligibility == "negative_evidence_only":
        semantic_relations = ["contradicts", "unresolved"]
        mapping_effects = [
            {"relation": "contradicts", "event_types": ["demote", "retire"]},
            {
                "relation": "leaves_open",
                "event_types": ["justified_no_change", "new_question"],
            },
        ]
    else:
        semantic_relations = ["contradicts", "leaves_open", "unresolved"]
        mapping_effects = [
            {"relation": "contradicts", "event_types": ["demote", "retire"]},
            {
                "relation": "leaves_open",
                "event_types": ["justified_no_change", "new_question"],
            },
            {"relation": "reframes", "event_types": ["reframe"]},
        ]
    permission = {
        "source_id": source_id,
        "routing_eligibility": eligibility,
        "allowed_semantic_relations": semantic_relations,
        "allowed_mapping_effects": mapping_effects,
        "positive_support_authorized": False,
        "automatic_investment_authorized": False,
        "forbidden_effects": [
            "source_truth",
            "semantic_entailment",
            "positive_theory_support",
            "automatic_preference",
            "automatic_investment",
            "proof_promotion",
            "physics_result_promotion",
        ],
    }
    permission["permission_digest"] = canonical_digest(permission)
    return permission


def _source_routing_source_state(
    *, strict_authority: Mapping[str, Any], snapshot: Mapping[str, Any]
) -> dict[str, Any]:
    """Bind exact work, bytes, version, correction state, and warrant inputs."""

    routing = _source_routing_map(strict_authority)
    records: list[dict[str, Any]] = []
    for source in sorted(snapshot["sources"], key=lambda row: str(row["source_id"])):
        source_id = str(source["source_id"])
        source_warrants = []
        for raw in source.get("semantic_warrants", []):
            if not isinstance(raw, Mapping):
                _fail(
                    "source_routing_pre_map_warrant_input_invalid",
                    f"source {source_id!r} contains a non-object warrant input",
                )
            source_warrants.append(copy.deepcopy(dict(raw)))
        source_warrants.sort(key=canonical_json)
        record = {
            "source_id": source_id,
            "work_identity": str(source["work_identity"]),
            "source_content_digest": str(source["content_digest"]),
            "source_version": str(source["source_version"]),
            "correction_status": str(source["correction_status"]),
            "decision_relevant": bool(source["decision_relevant"]),
            "routing_eligibility": routing[source_id],
            "semantic_warrant_input_digest": canonical_digest(source_warrants),
        }
        record["record_digest"] = canonical_digest(record)
        records.append(record)
    ordered_source_ids = [row["source_id"] for row in records]
    state = {
        "ordered_source_ids": ordered_source_ids,
        "records": records,
        "source_set_digest": canonical_digest(ordered_source_ids),
    }
    state["source_state_digest"] = canonical_digest(state)
    return state


def _closed_acquisition_completion(
    receipt: Mapping[str, Any], *, target_id: str, run_id: str, state_version: int
) -> dict[str, Any]:
    """Project a successful acquisition receipt into the policy trust boundary."""

    if receipt.get("status") != "succeeded":
        _fail(
            "source_routing_pre_map_acquisition_receipt_invalid",
            "pre-map policy requires a successful validated-acquisition receipt",
        )
    identity = receipt.get("identity")
    if not isinstance(identity, Mapping) or (
        identity.get("target_id") != target_id
        or identity.get("run_id") != run_id
        or identity.get("state_version") != state_version
    ):
        _fail(
            "source_routing_pre_map_acquisition_identity_mismatch",
            "validated acquisition receipt crossed target/run/state",
        )
    receipt_id = str(receipt.get("receipt_id") or "")
    completed_at = str(receipt.get("completed_at") or "")
    if not receipt_id:
        _fail(
            "source_routing_pre_map_acquisition_receipt_invalid",
            "validated acquisition receipt lacks a receipt id",
        )
    _timestamp(completed_at, field="validated acquisition completion")
    return {
        "receipt_id": receipt_id,
        "status": "succeeded",
        "identity": {
            "target_id": target_id,
            "run_id": run_id,
            "state_version": state_version,
        },
        "completed_at": completed_at,
    }


def _source_routing_pre_map_policy_payload(
    *,
    authority: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    target_id: str,
    run_id: str,
    state_version: int,
    acquisition_producer_receipt: Mapping[str, Any],
    algorithm_contracts: Sequence[Mapping[str, Any]],
    sealed_at: str,
    freshness_max_age_seconds: int,
) -> dict[str, Any]:
    """Construct the closed pre-map policy before any semantic routing runs."""

    strict = _strict_acquisition_authority(authority)
    validate_snapshot(dict(snapshot))
    if snapshot.get("target_id") != target_id:
        _fail(
            "source_routing_pre_map_target_mismatch",
            "literature snapshot crossed the pre-map target",
        )
    if strict["acquisition_content_digest"] != snapshot.get("content_digest"):
        _fail(
            "source_routing_pre_map_acquisition_snapshot_mismatch",
            "validated acquisition digest does not equal the exact policy snapshot",
        )
    source_ids = sorted(str(source["source_id"]) for source in snapshot["sources"])
    if source_ids != strict["source_ids"]:
        _fail(
            "source_routing_pre_map_source_set_mismatch",
            "policy snapshot sources differ from validated acquisition authority",
        )
    if not isinstance(freshness_max_age_seconds, int) or not (
        1 <= freshness_max_age_seconds <= 2_592_000
    ):
        _fail(
            "source_routing_pre_map_freshness_invalid",
            "freshness_max_age_seconds must be an integer in [1, 2592000]",
        )
    completion = _closed_acquisition_completion(
        acquisition_producer_receipt,
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
    )
    acquisition_completed = _timestamp(
        completion["completed_at"], field="validated acquisition completion"
    )
    search_completed = _timestamp(
        snapshot["search_completed_at"], field="snapshot search completion"
    )
    seal_time = _timestamp(sealed_at, field="source-routing pre-map seal")
    consume_before = search_completed + timedelta(seconds=freshness_max_age_seconds)
    if acquisition_completed < search_completed:
        _fail(
            "source_routing_pre_map_before_acquisition",
            "validated acquisition receipt predates snapshot completion",
        )
    if seal_time < acquisition_completed:
        _fail(
            "source_routing_pre_map_before_acquisition",
            "pre-map policy was sealed before validated acquisition completed",
        )
    if seal_time >= consume_before:
        _fail(
            "source_routing_pre_map_stale",
            "pre-map policy was sealed after its bounded consumption window",
        )
    normalized_algorithms = _normalize_source_routing_algorithm_contracts(
        algorithm_contracts
    )
    source_state = _source_routing_source_state(
        strict_authority=strict, snapshot=snapshot
    )
    permissions = [
        _source_routing_effect_permission(
            source_id, strict["source_routing_eligibility"][source_id]
        )
        for source_id in source_state["ordered_source_ids"]
    ]
    acquisition_authority_digest = canonical_digest(strict)
    snapshot_binding = {
        "snapshot_id": snapshot["snapshot_id"],
        "snapshot_digest": snapshot["content_digest"],
        "target_id": target_id,
        "theory_state_digest": snapshot["theory_state_digest"],
        "search_completed_at": snapshot["search_completed_at"],
        "coverage_cutoff": snapshot["coverage_cutoff"],
    }
    freshness_contract = {
        "policy": "search_completion_bounded_pre_map_use.v1",
        "max_age_seconds": freshness_max_age_seconds,
        "consume_before": consume_before.isoformat().replace("+00:00", "Z"),
        "stale_policy": "reject_policy_or_realization_at_or_after_consume_before",
        "authority_scope": (
            "stage ordering and bounded present use only; freshness does not imply "
            "coverage, novelty, source truth, or relevance"
        ),
    }
    completion_contract = {
        "required_stage_order": list(SOURCE_ROUTING_PRE_MAP_STAGES),
        "exact_receipt_cardinality": {
            stage: 1 for stage in SOURCE_ROUTING_PRE_MAP_STAGES
        },
        "required_realization_inputs": [
            "validated_warrants",
            "claim_mappings",
            "assimilation_packet",
            "stage_receipts",
        ],
        "required_downstream_envelope_fields": [
            "source_routing_pre_map_policy",
            "source_routing_realization",
        ],
        "omission_policy": "fail_closed",
        "substitution_policy": "exact_object_and_digest_only",
        "late_policy": "reject_if_any_mapping_stage_started_before_policy_seal",
    }
    policy_id = stable_identifier(
        "source-routing-pre-map-policy",
        target_id,
        run_id,
        state_version,
        acquisition_authority_digest,
        snapshot["content_digest"],
        source_state["source_state_digest"],
        [row["contract_digest"] for row in normalized_algorithms],
    )
    return {
        "schema_version": "1.0.0",
        "policy_id": policy_id,
        "target_id": target_id,
        "run_id": run_id,
        "state_version": state_version,
        "sealed_at": sealed_at,
        "acquisition_completion": completion,
        "acquisition_authority": strict,
        "acquisition_authority_digest": acquisition_authority_digest,
        "snapshot_binding": snapshot_binding,
        "freshness_contract": freshness_contract,
        "source_state": source_state,
        "algorithm_contracts": normalized_algorithms,
        "effect_permissions": permissions,
        "completion_contract": completion_contract,
        "authority_boundary": SOURCE_ROUTING_PRE_MAP_BOUNDARY,
    }


def build_source_routing_pre_map_policy(
    *,
    authority: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    target_id: str,
    run_id: str,
    state_version: int,
    acquisition_producer_receipt: Mapping[str, Any],
    algorithm_contracts: Sequence[Mapping[str, Any]],
    sealed_at: str | None = None,
    freshness_max_age_seconds: int = 2_592_000,
) -> dict[str, Any]:
    """Seal mapping policy immediately after acquisition and before mapping.

    ``algorithm_contracts`` is deliberately mandatory.  The completed mapper
    may not name its own governing algorithm or configuration after seeing the
    outputs.  A canonical caller should source these three identities from its
    approved registry and put the returned policy into every stage request.
    """

    completion_time = str(acquisition_producer_receipt.get("completed_at") or "")
    payload = _source_routing_pre_map_policy_payload(
        authority=authority,
        snapshot=snapshot,
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
        acquisition_producer_receipt=acquisition_producer_receipt,
        algorithm_contracts=algorithm_contracts,
        sealed_at=sealed_at or completion_time,
        freshness_max_age_seconds=freshness_max_age_seconds,
    )
    payload["policy_digest"] = canonical_digest(payload)
    validate_payload(payload, SOURCE_ROUTING_PRE_MAP_POLICY_SCHEMA)
    return payload


def validate_source_routing_pre_map_policy(
    policy: Mapping[str, Any],
    *,
    authority: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    acquisition_producer_receipt: Mapping[str, Any],
    algorithm_contracts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Replay a policy against external acquisition and algorithm authority."""

    payload = copy.deepcopy(dict(policy))
    validate_payload(payload, SOURCE_ROUTING_PRE_MAP_POLICY_SCHEMA)
    if payload.get("policy_digest") != top_level_content_digest(
        payload, "policy_digest"
    ):
        _fail(
            "source_routing_pre_map_digest_mismatch",
            "pre-map policy content digest mismatch",
        )
    expected = _source_routing_pre_map_policy_payload(
        authority=authority,
        snapshot=snapshot,
        target_id=str(payload["target_id"]),
        run_id=str(payload["run_id"]),
        state_version=int(payload["state_version"]),
        acquisition_producer_receipt=acquisition_producer_receipt,
        algorithm_contracts=algorithm_contracts,
        sealed_at=str(payload["sealed_at"]),
        freshness_max_age_seconds=int(
            payload["freshness_contract"]["max_age_seconds"]
        ),
    )
    expected["policy_digest"] = canonical_digest(expected)
    if payload != expected:
        _fail(
            "source_routing_pre_map_replay_mismatch",
            "pre-map policy does not equal deterministic replay from external authority",
        )
    return payload


def _source_routing_completed_outputs(
    *,
    policy: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    validated_warrants: Sequence[Mapping[str, Any]],
    claim_mappings: Sequence[Mapping[str, Any]],
    assimilation: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    """Validate and summarize exact completed outputs without trusting receipts."""

    validate_snapshot(dict(snapshot))
    validate_assimilation(dict(assimilation), snapshot=dict(snapshot))
    if (
        policy["snapshot_binding"]["snapshot_digest"] != snapshot["content_digest"]
        or policy["snapshot_binding"]["snapshot_id"] != snapshot["snapshot_id"]
    ):
        _fail(
            "source_routing_realization_stale_policy",
            "realization snapshot differs from the sealed pre-map policy",
        )
    warrants = [copy.deepcopy(dict(row)) for row in validated_warrants]
    mappings = [copy.deepcopy(dict(row)) for row in claim_mappings]
    expected_warrants = _semantic_warrants(snapshot)
    if warrants != expected_warrants:
        _fail(
            "source_routing_realization_warrant_output_mismatch",
            "completed warrant output differs from the policy-bound source inputs",
        )
    if mappings != list(assimilation.get("theory_mappings", [])):
        _fail(
            "source_routing_realization_mapping_output_mismatch",
            "completed mapping output differs from the assimilation input",
        )
    if not mappings:
        _fail(
            "source_routing_realization_mapping_missing",
            "realization requires at least one completed source mapping",
        )
    validate_source_routing_consumption(
        authority=policy["acquisition_authority"],
        sources=snapshot["sources"],
        stage="warrant_validation",
        semantic_warrants=warrants,
    )
    validate_source_routing_consumption(
        authority=policy["acquisition_authority"],
        sources=snapshot["sources"],
        stage="claim_mapping",
        theory_mappings=mappings,
        semantic_warrants=warrants,
        require_complete_mapping=True,
    )
    validate_source_routing_consumption(
        authority=policy["acquisition_authority"],
        sources=snapshot["sources"],
        stage="assimilation",
        theory_mappings=mappings,
        semantic_warrants=warrants,
        require_complete_mapping=True,
    )
    mapping_ids = [str(row.get("mapping_id") or "") for row in mappings]
    if any(not item for item in mapping_ids) or len(mapping_ids) != len(set(mapping_ids)):
        _fail(
            "source_routing_realization_mapping_identity_invalid",
            "completed mappings require unique nonempty mapping ids",
        )
    warrant_ids = [str(row.get("warrant_id") or "") for row in warrants]
    if any(not item for item in warrant_ids) or len(warrant_ids) != len(set(warrant_ids)):
        _fail(
            "source_routing_realization_warrant_identity_invalid",
            "completed warrants require unique nonempty warrant ids",
        )
    selected = assimilation["selected_snapshot"]
    mapping_output_digest = canonical_digest(mappings)
    outputs = {
        "warrant_validation": {
            "source_ids": sorted({str(row["source_id"]) for row in warrants}),
            "warrant_ids": warrant_ids,
            "warrant_count": len(warrants),
            "output_digest": canonical_digest(warrants),
        },
        "claim_mapping": {
            "source_ids": sorted({str(row["source_id"]) for row in mappings}),
            "mapping_ids": mapping_ids,
            "mapping_count": len(mappings),
            "output_digest": mapping_output_digest,
        },
        "assimilation": {
            "packet_id": assimilation["packet_id"],
            "packet_digest": assimilation["content_digest"],
            "selected_snapshot_id": selected["snapshot_id"],
            "selected_snapshot_digest": selected["content_digest"],
            "mapping_output_digest": mapping_output_digest,
        },
    }
    return outputs, warrants, mappings


def source_routing_realization_requirements(
    *,
    policy: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    validated_warrants: Sequence[Mapping[str, Any]],
    claim_mappings: Sequence[Mapping[str, Any]],
    assimilation: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Return the exact receipt bindings canonical stage requests must satisfy.

    The helper does not mint receipts.  It exposes deterministic input/output
    digests so independently executed stages can bind the already-sealed policy
    before execution and a later realization can verify their exact chain.
    Full callers must first validate the policy against external acquisition and
    algorithm authority; this helper additionally refuses malformed or
    self-digest-invalid policy bytes.
    """

    validate_payload(dict(policy), SOURCE_ROUTING_PRE_MAP_POLICY_SCHEMA)
    if policy.get("policy_digest") != top_level_content_digest(
        policy, "policy_digest"
    ):
        _fail(
            "source_routing_pre_map_digest_mismatch",
            "pre-map policy content digest mismatch",
        )
    outputs, _warrants, _mappings = _source_routing_completed_outputs(
        policy=policy,
        snapshot=snapshot,
        validated_warrants=validated_warrants,
        claim_mappings=claim_mappings,
        assimilation=assimilation,
    )
    algorithms = {row["stage"]: row for row in policy["algorithm_contracts"]}
    warrant_input = canonical_digest(
        {
            "pre_map_policy_digest": policy["policy_digest"],
            "snapshot_digest": snapshot["content_digest"],
            "source_state_digest": policy["source_state"]["source_state_digest"],
        }
    )
    mapping_input = canonical_digest(
        {
            "pre_map_policy_digest": policy["policy_digest"],
            "snapshot_digest": snapshot["content_digest"],
            "warrant_output_digest": outputs["warrant_validation"]["output_digest"],
        }
    )
    assimilation_input = canonical_digest(
        {
            "pre_map_policy_digest": policy["policy_digest"],
            "snapshot_digest": snapshot["content_digest"],
            "warrant_output_digest": outputs["warrant_validation"]["output_digest"],
            "mapping_output_digest": outputs["claim_mapping"]["output_digest"],
        }
    )
    input_digests = {
        "warrant_validation": warrant_input,
        "claim_mapping": mapping_input,
        "assimilation": assimilation_input,
    }
    output_digests = {
        "warrant_validation": outputs["warrant_validation"]["output_digest"],
        "claim_mapping": outputs["claim_mapping"]["output_digest"],
        "assimilation": outputs["assimilation"]["packet_digest"],
    }
    return [
        {
            "stage": stage,
            "algorithm_contract_digest": algorithms[stage]["contract_digest"],
            "input_digest": input_digests[stage],
            "output_digest": output_digests[stage],
        }
        for stage in SOURCE_ROUTING_PRE_MAP_STAGES
    ]


def _normalize_source_routing_stage_receipts(
    *,
    policy: Mapping[str, Any],
    requirements: Sequence[Mapping[str, Any]],
    stage_receipts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Enforce exact stage cardinality, ordering, identity, and time barriers."""

    if len(stage_receipts) != len(SOURCE_ROUTING_PRE_MAP_STAGES):
        _fail(
            "source_routing_realization_stage_cardinality_invalid",
            "realization requires exactly one receipt for each of three stages",
        )
    required_fields = {
        "receipt_id",
        "stage",
        "status",
        "identity",
        "pre_map_policy_id",
        "pre_map_policy_digest",
        "algorithm_contract_digest",
        "started_at",
        "completed_at",
        "input_digest",
        "output_digest",
    }
    expected_by_stage = {str(row["stage"]): row for row in requirements}
    normalized: list[dict[str, Any]] = []
    previous_completion = _timestamp(
        policy["sealed_at"], field="source-routing pre-map seal"
    )
    for index, raw in enumerate(stage_receipts):
        if not isinstance(raw, Mapping) or set(raw) != required_fields:
            _fail(
                "source_routing_realization_stage_receipt_open",
                f"stage receipt {index} has unknown or missing fields",
            )
        receipt = copy.deepcopy(dict(raw))
        expected_stage = SOURCE_ROUTING_PRE_MAP_STAGES[index]
        if receipt.get("stage") != expected_stage:
            _fail(
                "source_routing_realization_stage_order_invalid",
                "stage receipts are omitted, duplicated, substituted, or out of order",
            )
        if receipt.get("status") != "succeeded":
            _fail(
                "source_routing_realization_stage_not_succeeded",
                f"stage {expected_stage!r} did not succeed",
            )
        identity = receipt.get("identity")
        if not isinstance(identity, Mapping) or dict(identity) != {
            "target_id": policy["target_id"],
            "run_id": policy["run_id"],
            "state_version": policy["state_version"],
        }:
            _fail(
                "source_routing_realization_stage_identity_mismatch",
                f"stage {expected_stage!r} crossed target/run/state",
            )
        if (
            receipt.get("pre_map_policy_id") != policy["policy_id"]
            or receipt.get("pre_map_policy_digest") != policy["policy_digest"]
        ):
            _fail(
                "source_routing_realization_policy_consumption_mismatch",
                f"stage {expected_stage!r} did not consume the exact pre-map policy",
            )
        expected = expected_by_stage[expected_stage]
        for field in (
            "algorithm_contract_digest",
            "input_digest",
            "output_digest",
        ):
            if receipt.get(field) != expected[field]:
                _fail(
                    "source_routing_realization_stage_binding_mismatch",
                    f"stage {expected_stage!r} has a substituted {field}",
                )
        started = _timestamp(
            receipt.get("started_at"), field=f"{expected_stage} started_at"
        )
        completed = _timestamp(
            receipt.get("completed_at"), field=f"{expected_stage} completed_at"
        )
        if started < previous_completion:
            _fail(
                "source_routing_realization_stage_order_invalid",
                f"stage {expected_stage!r} started before its causal predecessor completed",
            )
        if completed < started:
            _fail(
                "source_routing_realization_stage_time_invalid",
                f"stage {expected_stage!r} completed before it started",
            )
        previous_completion = completed
        normalized.append(receipt)
    _unique(
        [row["receipt_id"] for row in normalized],
        reason_code="source_routing_realization_stage_receipt_duplicate",
        label="source-routing stage receipt ids",
    )
    return normalized


def _source_routing_realization_payload(
    *,
    policy: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    validated_warrants: Sequence[Mapping[str, Any]],
    claim_mappings: Sequence[Mapping[str, Any]],
    assimilation: Mapping[str, Any],
    stage_receipts: Sequence[Mapping[str, Any]],
    completed_at: str,
) -> dict[str, Any]:
    """Construct the normalized post-assimilation realization without digest."""

    outputs, _warrants, _mappings = _source_routing_completed_outputs(
        policy=policy,
        snapshot=snapshot,
        validated_warrants=validated_warrants,
        claim_mappings=claim_mappings,
        assimilation=assimilation,
    )
    requirements = source_routing_realization_requirements(
        policy=policy,
        snapshot=snapshot,
        validated_warrants=validated_warrants,
        claim_mappings=claim_mappings,
        assimilation=assimilation,
    )
    receipts = _normalize_source_routing_stage_receipts(
        policy=policy,
        requirements=requirements,
        stage_receipts=stage_receipts,
    )
    final_stage_completion = _timestamp(
        receipts[-1]["completed_at"], field="assimilation stage completion"
    )
    realization_completion = _timestamp(
        completed_at, field="source-routing realization completion"
    )
    consume_before = _timestamp(
        policy["freshness_contract"]["consume_before"],
        field="source-routing policy consume_before",
    )
    if realization_completion < final_stage_completion:
        _fail(
            "source_routing_realization_completion_order_invalid",
            "realization completed before assimilation receipt completion",
        )
    if realization_completion >= consume_before:
        _fail(
            "source_routing_realization_stale",
            "realization completed at or after the policy consumption boundary",
        )
    completed_outputs_digest = canonical_digest(outputs)
    authorizations = []
    for stage, consumer in SOURCE_ROUTING_POST_ASSIMILATION_STAGES:
        authorizations.append(
            {
                "stage": stage,
                "required_consumer": consumer,
                "binding_digest": canonical_digest(
                    {
                        "target_id": policy["target_id"],
                        "run_id": policy["run_id"],
                        "state_version": policy["state_version"],
                        "stage": stage,
                        "required_consumer": consumer,
                        "pre_map_policy_digest": policy["policy_digest"],
                        "completed_outputs_digest": completed_outputs_digest,
                        "stage_receipt_ids": [row["receipt_id"] for row in receipts],
                    }
                ),
            }
        )
    downstream_contract = {
        "required_envelope_fields": [
            "source_routing_pre_map_policy",
            "source_routing_realization",
        ],
        "required_operator_ids": [
            "high-risk-hypothesis-forger",
            "parallel-hypothesis-portfolio",
            "reflective-conceptual-discovery",
            "reflective-theory-synthesizer",
            "blind-conceptual-preference-adjudicator",
            "dynamic-symbolic-simulation-experimenter",
        ],
        "required_internal_consumers": [
            "canonical-discovery-cycle",
            "canonical-theory-gate",
        ],
        "omission_policy": "fail_closed",
        "substitution_policy": "exact_policy_and_realization_objects_only",
        "late_realization_policy": "reject_after_first_downstream_dispatch",
    }
    downstream_contract["content_digest"] = canonical_digest(downstream_contract)
    realization_id = stable_identifier(
        "source-routing-realization",
        policy["policy_id"],
        policy["policy_digest"],
        completed_outputs_digest,
        [row["receipt_id"] for row in receipts],
    )
    return {
        "schema_version": "1.0.0",
        "realization_id": realization_id,
        "target_id": policy["target_id"],
        "run_id": policy["run_id"],
        "state_version": policy["state_version"],
        "completed_at": completed_at,
        "pre_map_policy": copy.deepcopy(dict(policy)),
        "pre_map_policy_id": policy["policy_id"],
        "pre_map_policy_digest": policy["policy_digest"],
        "completed_outputs": outputs,
        "stage_receipts": receipts,
        "post_assimilation_authorizations": authorizations,
        "downstream_consumption_contract": downstream_contract,
        "authority_boundary": SOURCE_ROUTING_REALIZATION_BOUNDARY,
    }


def build_source_routing_realization(
    *,
    policy: Mapping[str, Any],
    authority: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    acquisition_producer_receipt: Mapping[str, Any],
    algorithm_contracts: Sequence[Mapping[str, Any]],
    validated_warrants: Sequence[Mapping[str, Any]],
    claim_mappings: Sequence[Mapping[str, Any]],
    assimilation: Mapping[str, Any],
    stage_receipts: Sequence[Mapping[str, Any]],
    completed_at: str | None = None,
) -> dict[str, Any]:
    """Realize one pre-map policy over exact completed stage outputs.

    Every stage receipt must bind the policy object, externally governed
    algorithm/config contract, exact causal input digest, exact output digest,
    and target/run/state identity.  Only after this succeeds may later theory
    operators consume the policy-realization pair.
    """

    validated_policy = validate_source_routing_pre_map_policy(
        policy,
        authority=authority,
        snapshot=snapshot,
        acquisition_producer_receipt=acquisition_producer_receipt,
        algorithm_contracts=algorithm_contracts,
    )
    if completed_at is None:
        if not stage_receipts:
            _fail(
                "source_routing_realization_stage_cardinality_invalid",
                "realization requires exactly one receipt for each of three stages",
            )
        final_completed_at = str(stage_receipts[-1].get("completed_at") or "")
    else:
        final_completed_at = completed_at
    payload = _source_routing_realization_payload(
        policy=validated_policy,
        snapshot=snapshot,
        validated_warrants=validated_warrants,
        claim_mappings=claim_mappings,
        assimilation=assimilation,
        stage_receipts=stage_receipts,
        completed_at=final_completed_at,
    )
    payload["realization_digest"] = canonical_digest(payload)
    validate_payload(payload, SOURCE_ROUTING_REALIZATION_SCHEMA)
    return payload


def validate_source_routing_realization(
    realization: Mapping[str, Any],
    *,
    policy: Mapping[str, Any],
    authority: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    acquisition_producer_receipt: Mapping[str, Any],
    algorithm_contracts: Sequence[Mapping[str, Any]],
    validated_warrants: Sequence[Mapping[str, Any]],
    claim_mappings: Sequence[Mapping[str, Any]],
    assimilation: Mapping[str, Any],
    stage_receipts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Reopen a realization against its external policy and completed outputs."""

    payload = copy.deepcopy(dict(realization))
    validate_payload(payload, SOURCE_ROUTING_REALIZATION_SCHEMA)
    if payload.get("realization_digest") != top_level_content_digest(
        payload, "realization_digest"
    ):
        _fail(
            "source_routing_realization_digest_mismatch",
            "source-routing realization content digest mismatch",
        )
    validated_policy = validate_source_routing_pre_map_policy(
        policy,
        authority=authority,
        snapshot=snapshot,
        acquisition_producer_receipt=acquisition_producer_receipt,
        algorithm_contracts=algorithm_contracts,
    )
    if payload.get("pre_map_policy") != validated_policy:
        _fail(
            "source_routing_realization_policy_mismatch",
            "realization does not embed the exact externally validated pre-map policy",
        )
    expected = _source_routing_realization_payload(
        policy=validated_policy,
        snapshot=snapshot,
        validated_warrants=validated_warrants,
        claim_mappings=claim_mappings,
        assimilation=assimilation,
        stage_receipts=stage_receipts,
        completed_at=str(payload["completed_at"]),
    )
    expected["realization_digest"] = canonical_digest(expected)
    if payload != expected:
        _fail(
            "source_routing_realization_replay_mismatch",
            "source-routing realization does not equal deterministic replay",
        )
    return payload


def _source_routing_precommit_payload(
    *,
    authority: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    assimilation: Mapping[str, Any],
    target_id: str,
    run_id: str,
    state_version: int,
    assimilation_producer_receipt_id: str,
    assimilation_producer_completed_at: str,
    precommitted_at: str,
) -> dict[str, Any]:
    """Construct the unique normalized precommit payload without self-digest."""

    strict = _strict_acquisition_authority(authority)
    validate_snapshot(dict(snapshot))
    validate_assimilation(dict(assimilation), snapshot=dict(snapshot))
    if snapshot.get("target_id") != target_id or assimilation.get("target_id") != target_id:
        _fail(
            "source_routing_precommit_target_mismatch",
            "snapshot or assimilation crossed the precommit target",
        )
    source_ids = sorted(str(row["source_id"]) for row in snapshot["sources"])
    if source_ids != strict["source_ids"]:
        _fail(
            "source_routing_precommit_source_set_mismatch",
            "snapshot sources differ from validated acquisition authority",
        )
    selected = assimilation.get("selected_snapshot", {})
    if (
        selected.get("snapshot_id") != snapshot.get("snapshot_id")
        or selected.get("content_digest") != snapshot.get("content_digest")
    ):
        _fail(
            "source_routing_precommit_assimilation_snapshot_mismatch",
            "assimilation does not consume the exact precommitted snapshot",
        )
    producer_completed = _timestamp(
        assimilation_producer_completed_at,
        field="assimilation producer completion",
    )
    precommit_time = _timestamp(precommitted_at, field="source-routing precommit time")
    if precommit_time < producer_completed:
        _fail(
            "source_routing_precommit_before_assimilation",
            "source-routing precommit predates completed assimilation",
        )
    mappings = [copy.deepcopy(dict(row)) for row in assimilation.get("theory_mappings", [])]
    if not mappings:
        _fail(
            "source_routing_precommit_mapping_missing",
            "active source routing requires exact assimilation mappings",
        )
    warrants = _semantic_warrants(snapshot)
    acquisition_authority_digest = canonical_digest(strict)
    snapshot_binding = {
        "snapshot_id": snapshot["snapshot_id"],
        "snapshot_digest": snapshot["content_digest"],
        "target_id": target_id,
        "theory_state_digest": snapshot["theory_state_digest"],
        "source_ids": source_ids,
        "source_set_digest": canonical_digest(source_ids),
    }
    assimilation_binding = {
        "packet_id": assimilation["packet_id"],
        "packet_digest": assimilation["content_digest"],
        "producer_receipt_id": assimilation_producer_receipt_id,
        "producer_completed_at": assimilation_producer_completed_at,
        "selected_snapshot_id": selected["snapshot_id"],
        "selected_snapshot_digest": selected["content_digest"],
        "theory_mappings_digest": canonical_digest(mappings),
        "semantic_warrants_digest": canonical_digest(warrants),
    }
    stage_rows: list[dict[str, Any]] = []
    for stage, consumer in SOURCE_ROUTING_PRECOMMIT_STAGES:
        routing_certificate = validate_source_routing_consumption(
            authority=strict,
            sources=snapshot["sources"],
            stage=stage,
            theory_mappings=mappings,
            semantic_warrants=warrants,
            require_complete_mapping=True,
        )
        binding_basis = {
            "target_id": target_id,
            "run_id": run_id,
            "state_version": state_version,
            "stage": stage,
            "required_consumer": consumer,
            "acquisition_authority_digest": acquisition_authority_digest,
            "snapshot_digest": snapshot["content_digest"],
            "assimilation_digest": assimilation["content_digest"],
            "routing_certificate_digest": routing_certificate["content_digest"],
        }
        binding_digest = canonical_digest(binding_basis)
        stage_rows.append(
            {
                "stage": stage,
                "stage_decision_id": stable_identifier(
                    "source-routing-stage", target_id, run_id, state_version, stage, binding_digest
                ),
                "required_consumer": consumer,
                "routing_certificate": routing_certificate,
                "binding_digest": binding_digest,
            }
        )
    downstream_contract = {
        "required_envelope_field": "source_routing_precommit",
        "required_operator_ids": [
            "high-risk-hypothesis-forger",
            "parallel-hypothesis-portfolio",
            "reflective-conceptual-discovery",
            "reflective-theory-synthesizer",
            "blind-conceptual-preference-adjudicator",
            "dynamic-symbolic-simulation-experimenter",
        ],
        "required_internal_consumers": [
            "canonical-discovery-cycle",
            "canonical-theory-gate",
        ],
        "omission_policy": "fail_closed",
        "substitution_policy": "exact_object_and_digest_only",
        "late_certificate_policy": "reject_after_first_downstream_dispatch",
    }
    downstream_contract["content_digest"] = canonical_digest(downstream_contract)
    certificate_id = stable_identifier(
        "source-routing-precommit",
        target_id,
        run_id,
        state_version,
        acquisition_authority_digest,
        snapshot["content_digest"],
        assimilation["content_digest"],
    )
    return {
        "schema_version": "1.0.0",
        "certificate_id": certificate_id,
        "target_id": target_id,
        "run_id": run_id,
        "state_version": state_version,
        "precommitted_at": precommitted_at,
        "acquisition_authority": strict,
        "acquisition_authority_digest": acquisition_authority_digest,
        "snapshot_binding": snapshot_binding,
        "assimilation_binding": assimilation_binding,
        "stage_precommitments": stage_rows,
        "downstream_consumption_contract": downstream_contract,
        "compatibility": {
            "status": "post_assimilation_compatibility_only",
            "pre_map_authority_authorized": False,
            "replacement_envelope_fields": [
                "source_routing_pre_map_policy",
                "source_routing_realization",
            ],
            "boundary": SOURCE_ROUTING_LEGACY_COMPATIBILITY_BOUNDARY,
        },
        "authority_boundary": SOURCE_ROUTING_PRECOMMIT_BOUNDARY,
    }


def build_source_routing_precommit_certificate(
    *,
    authority: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    assimilation: Mapping[str, Any],
    target_id: str,
    run_id: str,
    state_version: int,
    assimilation_producer_receipt: Mapping[str, Any],
    precommitted_at: str | None = None,
) -> dict[str, Any]:
    """Build the legacy post-assimilation compatibility certificate.

    This historical API cannot govern claim mapping because its first possible
    construction point is after assimilation.  It remains available only while
    callers migrate to :func:`build_source_routing_pre_map_policy` and
    :func:`build_source_routing_realization`; the typed compatibility field
    makes ``pre_map_authority_authorized`` false.
    """

    if assimilation_producer_receipt.get("status") != "succeeded":
        _fail(
            "source_routing_precommit_assimilation_receipt_invalid",
            "precommit requires a successful assimilation producer receipt",
        )
    identity = assimilation_producer_receipt.get("identity", {})
    if (
        identity.get("target_id") != target_id
        or identity.get("run_id") != run_id
        or identity.get("state_version") != state_version
    ):
        _fail(
            "source_routing_precommit_receipt_identity_mismatch",
            "assimilation producer receipt crossed target/run/state",
        )
    completed_at = str(assimilation_producer_receipt.get("completed_at") or "")
    payload = _source_routing_precommit_payload(
        authority=authority,
        snapshot=snapshot,
        assimilation=assimilation,
        target_id=target_id,
        run_id=run_id,
        state_version=state_version,
        assimilation_producer_receipt_id=str(
            assimilation_producer_receipt.get("receipt_id") or ""
        ),
        assimilation_producer_completed_at=completed_at,
        precommitted_at=precommitted_at or completed_at,
    )
    payload["certificate_digest"] = canonical_digest(payload)
    validate_payload(payload, SOURCE_ROUTING_PRECOMMIT_SCHEMA)
    return payload


def validate_source_routing_precommit_certificate(
    certificate: Mapping[str, Any],
    *,
    snapshot: Mapping[str, Any],
    assimilation: Mapping[str, Any],
) -> dict[str, Any]:
    """Rebuild a legacy compatibility object from completed outputs."""

    payload = copy.deepcopy(dict(certificate))
    validate_payload(payload, SOURCE_ROUTING_PRECOMMIT_SCHEMA)
    if payload.get("certificate_digest") != top_level_content_digest(
        payload, "certificate_digest"
    ):
        _fail(
            "source_routing_precommit_digest_mismatch",
            "source-routing precommit content digest mismatch",
        )
    expected = _source_routing_precommit_payload(
        authority=payload["acquisition_authority"],
        snapshot=snapshot,
        assimilation=assimilation,
        target_id=str(payload["target_id"]),
        run_id=str(payload["run_id"]),
        state_version=int(payload["state_version"]),
        assimilation_producer_receipt_id=str(
            payload["assimilation_binding"]["producer_receipt_id"]
        ),
        assimilation_producer_completed_at=str(
            payload["assimilation_binding"]["producer_completed_at"]
        ),
        precommitted_at=str(payload["precommitted_at"]),
    )
    expected["certificate_digest"] = canonical_digest(expected)
    if payload != expected:
        _fail(
            "source_routing_precommit_replay_mismatch",
            "source-routing precommit does not equal deterministic replay",
        )
    return payload


def _validate_source_observation(observation: Mapping[str, Any]) -> None:
    _validate_self_digest(
        observation,
        "observation_digest",
        reason_code="source_observation_digest_mismatch",
        label=f"source observation {observation.get('source_id')!r}",
    )
    if len(observation["claims"]) != len(set(observation["claims"])):
        _fail(
            "duplicate_source_claim",
            f"source observation {observation['source_id']!r} repeats a claim",
        )
    if len(observation["authors"]) != len(set(observation["authors"])):
        _fail(
            "duplicate_source_author",
            f"source observation {observation['source_id']!r} repeats an author",
        )
    evidence = list(observation.get("lineage_evidence", []))
    _unique(
        [row["evidence_id"] for row in evidence],
        reason_code="duplicate_lineage_evidence_id",
        label="lineage evidence identifiers",
    )
    claim_digests = {canonical_digest(claim) for claim in observation["claims"]}
    for row in evidence:
        _validate_self_digest(
            row,
            "evidence_digest",
            reason_code="lineage_evidence_digest_mismatch",
            label=f"lineage evidence {row.get('evidence_id')!r}",
        )
        if row["claim_digest"] is not None and row["claim_digest"] not in claim_digests:
            _fail(
                "lineage_evidence_claim_digest_mismatch",
                f"lineage evidence {row['evidence_id']!r} does not bind an exact observed claim",
            )


def _validate_items_and_links(payload: Mapping[str, Any]) -> None:
    """Validate the normalized item surface shared by both artifact versions."""

    items = payload["result_items"]
    links = payload["normalization_links"]
    _unique(
        [item["item_id"] for item in items],
        reason_code="duplicate_tool_item_id",
        label="tool item identifiers",
    )
    _unique(
        [item["provider_rank"] for item in items if item["provider_rank"] is not None],
        reason_code="duplicate_tool_item_rank",
        label="tool item ranks",
    )
    _unique(
        [link["item_id"] for link in links],
        reason_code="duplicate_normalization_link",
        label="normalization item bindings",
    )
    if {item["item_id"] for item in items} != {link["item_id"] for link in links}:
        _fail(
            "tool_item_link_closure_mismatch",
            "each exposed tool item must have exactly one normalization disposition",
        )
    links_by_item = {link["item_id"]: link for link in links}
    for item in items:
        _validate_source_observation(item["source_observation"])
        if item["excerpt_word_count"] != len(item["bounded_excerpt"].split()):
            _fail(
                "excerpt_word_count_mismatch",
                f"tool item {item['item_id']!r} has an incorrect excerpt word count",
            )
        _validate_self_digest(
            item,
            "item_digest",
            reason_code="tool_item_digest_mismatch",
            label=f"tool item {item['item_id']!r}",
        )
        link = links_by_item[item["item_id"]]
        if (
            item["title"] != item["source_observation"]["title"]
            or item["url"] != item["source_observation"]["url"]
        ):
            _fail(
                "tool_item_observation_metadata_mismatch",
                f"tool item {item['item_id']!r} title or URL differs from its source observation",
            )
        if link["source_id"] != item["source_observation"]["source_id"]:
            _fail(
                "tool_item_source_mismatch",
                f"tool item {item['item_id']!r} is linked to another source",
            )
        included = str(link["disposition"]).startswith("included")
        if included != bool(item["source_observation"]["decision_relevant"]):
            _fail(
                "tool_disposition_relevance_mismatch",
                f"tool item {item['item_id']!r} disposition conflicts with decision relevance",
            )
    if payload["response_exposure"]["selected_result_count"] != len(items):
        _fail(
            "tool_result_count_mismatch",
            "response exposure count differs from the sealed result item count",
        )
    if payload.get("schema_version") == "2.0":
        outcome = payload["response_exposure"]["lane_outcome"]
        expected = "completed_with_results" if items else "completed_no_results"
        if outcome != expected:
            _fail(
                "tool_lane_outcome_mismatch",
                "lane outcome differs from its exact sealed result cardinality",
            )


def _primary_search_execution(payload: Mapping[str, Any]) -> dict[str, str]:
    """Project the one lane-defining web search from either artifact version."""

    if payload.get("schema_version") == "1.0":
        return {
            "execution_id": str(payload["execution"]["tool_call_id"]),
            "query": str(payload["request"]["search_query"]["q"]),
            "observed_started_at": str(payload["execution"]["observed_started_at"]),
            "observed_completed_at": str(payload["execution"]["observed_completed_at"]),
        }
    matches = [
        execution
        for execution in payload.get("executions", [])
        if execution.get("tool_name") == "web.run"
        and execution.get("request", {}).get("operation") == "search_query"
    ]
    if len(matches) != 1:
        _fail(
            "tool_primary_search_execution_mismatch",
            "each differentiated lane requires exactly one defining web search execution",
        )
    execution = matches[0]
    return {
        "execution_id": str(execution["execution_id"]),
        "query": str(execution["request"]["locator"]),
        "observed_started_at": str(execution["observed_started_at"]),
        "observed_completed_at": str(execution["observed_completed_at"]),
    }


def _artifact_execution_window(payload: Mapping[str, Any]) -> tuple[str, str]:
    """Return the full observed interval, including every auxiliary API call."""

    if payload.get("schema_version") == "1.0":
        return (
            str(payload["execution"]["observed_started_at"]),
            str(payload["execution"]["observed_completed_at"]),
        )
    executions = list(payload["executions"])
    started = min(
        executions,
        key=lambda row: _timestamp(row["observed_started_at"], field="observed_started_at"),
    )["observed_started_at"]
    completed = max(
        executions,
        key=lambda row: _timestamp(row["observed_completed_at"], field="observed_completed_at"),
    )["observed_completed_at"]
    return str(started), str(completed)


def _validate_multi_execution_artifact(payload: Mapping[str, Any]) -> None:
    """Validate exact execution-to-item/evidence closure for artifact v2."""

    executions = list(payload["executions"])
    bindings = list(payload["execution_bindings"])
    execution_ids = [str(row["execution_id"]) for row in executions]
    _unique(
        execution_ids,
        reason_code="duplicate_tool_execution_id",
        label="tool execution identifiers",
    )
    _unique(
        [str(row["request"]["request_id"]) for row in executions],
        reason_code="duplicate_tool_request_id",
        label="tool request identifiers",
    )
    for execution in executions:
        request = execution["request"]
        _validate_self_digest(
            request,
            "request_digest",
            reason_code="tool_request_digest_mismatch",
            label=f"execution {execution['execution_id']!r} request",
        )
        _validate_self_digest(
            execution,
            "execution_digest",
            reason_code="tool_execution_digest_mismatch",
            label=f"execution {execution['execution_id']!r}",
        )
        started = _timestamp(execution["observed_started_at"], field="observed_started_at")
        completed = _timestamp(execution["observed_completed_at"], field="observed_completed_at")
        if completed < started:
            _fail("tool_execution_time_reversed", "tool completion precedes its start")
    binding_ids = [str(row["execution_id"]) for row in bindings]
    if len(binding_ids) != len(set(binding_ids)) or set(binding_ids) != set(execution_ids):
        _fail(
            "tool_execution_binding_bijection_mismatch",
            "every execution requires exactly one binding and no unexecuted binding is allowed",
        )
    for binding in bindings:
        _validate_self_digest(
            binding,
            "binding_digest",
            reason_code="tool_execution_binding_digest_mismatch",
            label=f"execution binding {binding['execution_id']!r}",
        )

    items = {str(item["item_id"]): item for item in payload["result_items"]}
    evidence_owner: dict[str, str] = {}
    for item_id, item in items.items():
        for atom in item["source_observation"].get("lineage_evidence", []):
            evidence_id = str(atom["evidence_id"])
            if evidence_id in evidence_owner:
                _fail(
                    "duplicate_artifact_lineage_evidence_id",
                    f"lineage evidence {evidence_id!r} appears in multiple items",
                )
            evidence_owner[evidence_id] = item_id
    bound_items: set[str] = set()
    bound_evidence: list[str] = []
    execution_by_id = {str(row["execution_id"]): row for row in executions}
    api_bound_items: set[str] = set()
    for binding in bindings:
        execution_id = str(binding["execution_id"])
        item_ids = {str(value) for value in binding["item_ids"]}
        evidence_ids = [str(value) for value in binding["lineage_evidence_ids"]]
        unknown_items = item_ids - set(items)
        unknown_evidence = set(evidence_ids) - set(evidence_owner)
        if unknown_items or unknown_evidence:
            _fail(
                "tool_execution_binding_reference_unknown",
                f"execution {execution_id!r} binds unknown items/evidence",
            )
        if any(evidence_owner[evidence_id] not in item_ids for evidence_id in evidence_ids):
            _fail(
                "tool_execution_evidence_item_mismatch",
                "lineage evidence is not colocated with an item bound to the same execution",
            )
        execution = execution_by_id[execution_id]
        if execution["tool_name"] == "zenodo.records-api":
            api_bound_items.update(item_ids)
            locator = str(execution["request"]["locator"])
            for evidence_id in evidence_ids:
                owner = items[evidence_owner[evidence_id]]["source_observation"]
                atom = next(
                    row for row in owner.get("lineage_evidence", [])
                    if str(row["evidence_id"]) == evidence_id
                )
                if atom["source_locator"] != locator:
                    _fail(
                        "tool_execution_evidence_locator_mismatch",
                        "API-bound lineage evidence names another observed endpoint",
                    )
        bound_items.update(item_ids)
        bound_evidence.extend(evidence_ids)
    if bound_items != set(items):
        _fail(
            "tool_execution_item_closure_mismatch",
            "every exposed item must be bound to at least one observed execution",
        )
    if len(bound_evidence) != len(set(bound_evidence)) or set(bound_evidence) != set(evidence_owner):
        _fail(
            "tool_execution_evidence_closure_mismatch",
            "every lineage evidence atom must bind exactly one observed execution",
        )
    for item_id, item in items.items():
        if item["retrieval_class"] == "primary_api_metadata" and item_id not in api_bound_items:
            _fail(
                "tool_primary_api_execution_missing",
                f"primary API item {item_id!r} lacks a primary-API execution binding",
            )
    _primary_search_execution(payload)


def validate_tool_response_artifact(payload: Mapping[str, Any]) -> None:
    """Validate one exact bounded single- or multi-execution artifact."""

    version = payload.get("schema_version")
    schema = TOOL_RESPONSE_SCHEMA_V2 if version == "2.0" else TOOL_RESPONSE_SCHEMA
    try:
        validate_payload(payload, schema)
    except Exception as exc:
        raise LiteratureAcquisitionError(
            "tool_response_schema_invalid", str(exc)
        ) from exc
    if version == "1.0":
        request = payload["request"]
        _validate_self_digest(
            request,
            "request_digest",
            reason_code="tool_request_digest_mismatch",
            label=f"lane {payload['lane_id']!r} request",
        )
        started = _timestamp(
            payload["execution"]["observed_started_at"], field="observed_started_at"
        )
        completed = _timestamp(
            payload["execution"]["observed_completed_at"], field="observed_completed_at"
        )
        if completed < started:
            _fail("tool_execution_time_reversed", "tool completion precedes its start")
    else:
        _validate_multi_execution_artifact(payload)
    _validate_items_and_links(payload)
    _validate_self_digest(
        payload,
        "content_digest",
        reason_code="tool_response_digest_mismatch",
        label=f"tool response {payload['lane_id']!r}",
    )


def load_tool_response_artifact(path: Path, *, authority_root: Path) -> tuple[dict[str, Any], bytes]:
    """Load one regular, non-linked artifact inside an explicit authority root."""

    root = authority_root.resolve(strict=True)
    raw_path = path if path.is_absolute() else root / path
    try:
        relative = Path(os.path.abspath(raw_path)).relative_to(root)
    except (OSError, ValueError) as exc:
        raise LiteratureAcquisitionError(
            "tool_response_path_escape", f"response artifact escapes authority root: {path}"
        ) from exc
    cursor = root
    for part in relative.parts[:-1]:
        cursor = cursor / part
        try:
            parent_stat = cursor.stat(follow_symlinks=False)
        except OSError as exc:
            raise LiteratureAcquisitionError(
                "tool_response_unreadable", f"cannot inspect response parent {cursor}: {exc}"
            ) from exc
        if stat.S_ISLNK(parent_stat.st_mode) or not stat.S_ISDIR(parent_stat.st_mode):
            _fail("tool_response_path_escape", f"response parent is not an owned directory: {cursor}")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(root / relative, flags)
        try:
            file_stat = os.fstat(descriptor)
            if not stat.S_ISREG(file_stat.st_mode):
                _fail("tool_response_not_regular", f"response artifact is not a regular file: {path}")
            if file_stat.st_nlink != 1:
                _fail("tool_response_hardlink", f"response artifact has multiple hard links: {path}")
            chunks: list[bytes] = []
            while True:
                chunk = os.read(descriptor, 1024 * 1024)
                if not chunk:
                    break
                chunks.append(chunk)
            data = b"".join(chunks)
        finally:
            os.close(descriptor)
        payload = json.loads(data)
    except (OSError, json.JSONDecodeError) as exc:
        raise LiteratureAcquisitionError(
            "tool_response_unreadable", f"cannot load response artifact {path}: {exc}"
        ) from exc
    if not isinstance(payload, dict):
        _fail("tool_response_not_object", f"response artifact is not an object: {path}")
    validate_tool_response_artifact(payload)
    return payload, data


def _artifact_index(
    artifacts: Iterable[Mapping[str, Any]],
) -> tuple[dict[str, Mapping[str, Any]], dict[tuple[str, str], Mapping[str, Any]]]:
    by_lane: dict[str, Mapping[str, Any]] = {}
    items: dict[tuple[str, str], Mapping[str, Any]] = {}
    artifact_list = list(artifacts)
    for artifact in artifact_list:
        validate_tool_response_artifact(artifact)
        lane_id = str(artifact["lane_id"])
        if lane_id in by_lane:
            _fail("duplicate_tool_lane", f"multiple artifacts claim lane {lane_id!r}")
        by_lane[lane_id] = artifact
        for item in artifact["result_items"]:
            items[(lane_id, str(item["item_id"]))] = item
    if len(by_lane) != len(LANE_TYPES) or {
        artifact["lane_type"] for artifact in artifact_list
    } != set(LANE_TYPES):
        _fail(
            "tool_lane_set_mismatch",
            "the acquisition requires one distinct artifact for every canonical lane",
        )
    targets = {str(artifact["target_id"]) for artifact in artifact_list}
    if len(targets) != 1:
        _fail("tool_target_set_mismatch", "tool artifacts do not share one exact target")
    all_execution_ids = [
        str(execution_id)
        for artifact in artifact_list
        for execution_id in (
            [artifact["execution"]["tool_call_id"]]
            if artifact.get("schema_version") == "1.0"
            else [row["execution_id"] for row in artifact["executions"]]
        )
    ]
    _unique(
        all_execution_ids,
        reason_code="duplicate_tool_call_id",
        label="tool call identifiers",
    )
    _unique(
        [artifact["content_digest"] for artifact in artifact_list],
        reason_code="duplicate_tool_response_body",
        label="tool response content digests",
    )
    return by_lane, items


def validate_source_version_graph(
    payload: Mapping[str, Any],
    *,
    artifacts: Sequence[Mapping[str, Any]],
    sources: Sequence[Mapping[str, Any]] | None = None,
    expected_target_id: str | None = None,
) -> None:
    """Validate an acyclic, contiguous, evidence-bound source lineage."""

    try:
        validate_payload(payload, VERSION_GRAPH_SCHEMA)
    except Exception as exc:
        raise LiteratureAcquisitionError(
            "version_graph_schema_invalid", str(exc)
        ) from exc
    _validate_self_digest(
        payload,
        "content_digest",
        reason_code="version_graph_digest_mismatch",
        label=f"version graph {payload['graph_id']!r}",
    )
    by_lane, item_index = _artifact_index(artifacts)
    artifact_target = next(iter({str(artifact["target_id"]) for artifact in artifacts}))
    if payload["target_id"] != artifact_target or (
        expected_target_id is not None and payload["target_id"] != expected_target_id
    ):
        _fail("version_target_mismatch", "version graph target differs from acquisition authority")
    concept_doi = _canonical_doi(payload["concept_doi"])
    if payload["concept_doi"] != concept_doi or payload["work_identity"] != f"doi:{concept_doi}":
        _fail(
            "version_work_identity_noncanonical",
            "work identity must be the canonical DOI-concept identity",
        )
    versions = payload["versions"]
    source_ids = [str(version["source_id"]) for version in versions]
    record_dois = [str(version["record_doi"]) for version in versions]
    ordinals = [int(version["ordinal"]) for version in versions]
    if len(source_ids) != len(set(source_ids)):
        _fail("duplicate_version_source", "a source appears twice in the version graph")
    if len(record_dois) != len(set(record_dois)):
        _fail("duplicate_version_record_doi", "a record DOI appears twice in the version graph")
    if sorted(ordinals) != list(range(1, len(versions) + 1)):
        _fail("version_ordinal_gap", "version ordinals must be contiguous from one")
    ordered = sorted(versions, key=lambda row: int(row["ordinal"]))
    observed_at = _timestamp(payload["observed_at"], field="version graph observed_at")
    membership = payload["lineage_membership"]
    _validate_self_digest(
        membership,
        "membership_digest",
        reason_code="version_membership_digest_mismatch",
        label="lineage membership",
    )
    membership_atoms = _resolve_evidence_bindings(
        membership["evidence_bindings"],
        by_lane=by_lane,
        item_index=item_index,
        expected_source_id=None,
    )
    expected_record_dois = [str(row["record_doi"]) for row in ordered]
    if membership["ordered_record_dois"] != expected_record_dois:
        _fail(
            "version_lineage_membership_mismatch",
            "lineage membership does not equal the complete ordinal record list",
        )
    if not membership_atoms or any(
        atom["predicate"] != "lineage_ordered_record_dois"
        or atom["subject"] != concept_doi
        or atom["object"] != expected_record_dois
        or atom["authority_class"] != "primary_repository_relation"
        for atom in membership_atoms
    ):
        _fail(
            "version_membership_evidence_mismatch",
            "lineage membership is not bound to the exact repository version list",
        )
    expected_edges: set[tuple[str, str]] = set()
    chronological_keys: list[tuple[datetime, datetime, str]] = []
    for index, version in enumerate(ordered):
        predecessor = ordered[index - 1]["source_id"] if index else None
        successor = ordered[index + 1]["source_id"] if index + 1 < len(ordered) else None
        if (
            version["predecessor_source_id"] != predecessor
            or version["successor_source_id"] != successor
        ):
            _fail(
                "version_neighbor_mismatch",
                f"version {version['source_id']!r} has an asymmetric predecessor/successor",
            )
        if successor is not None:
            expected_edges.add((str(version["source_id"]), str(successor)))
        expected_role = {
            "current": ("current_unverified_claim_audit", "unverified_audit_only"),
            "corrected": ("current_unverified_claim_audit", "unverified_audit_only"),
            "superseded": ("historical_correction_context_only", "blocked_positive_support"),
            "withdrawn": ("negative_withdrawal_evidence", "negative_evidence_only"),
            "retracted": ("negative_withdrawal_evidence", "negative_evidence_only"),
        }[version["status"]]
        if (
            version["decision_role"],
            version["present_investment_eligibility"],
        ) != expected_role:
            _fail(
                "version_routing_role_mismatch",
                f"version {version['source_id']!r} status and routing eligibility disagree",
            )
        if successor is not None and version["status"] != "superseded":
            _fail(
                "version_terminal_status_invalid",
                "only superseded records may have a successor",
            )
        if successor is None and version["status"] == "superseded":
            _fail("version_terminal_status_invalid", "the terminal record is superseded")
        record_doi = _canonical_doi(version["record_doi"])
        if version["record_doi"] != record_doi:
            _fail("version_identity_evidence_mismatch", "record DOI is not canonical")
        publication_time = datetime.fromisoformat(str(version["publication_date"])).replace(
            tzinfo=timezone.utc
        )
        if publication_time > observed_at:
            _fail(
                "version_observed_before_publication",
                f"version {version['source_id']!r} is published after the graph observation",
            )
        identity_atoms = _resolve_evidence_bindings(
            version["identity_evidence_bindings"],
            by_lane=by_lane,
            item_index=item_index,
            expected_source_id=str(version["source_id"]),
        )
        identity_by_predicate = _atoms_by_predicate(
            identity_atoms,
            expected=IDENTITY_PREDICATES,
            reason_code="version_identity_evidence_incomplete",
        )
        expected_identity = {
            "record_doi": (str(version["source_id"]), record_doi),
            "record_member_of_concept": (record_doi, concept_doi),
            "record_version": (record_doi, str(version["source_version"])),
        }
        if any(
            atom["subject"] != expected_identity[predicate][0]
            or atom["object"] != expected_identity[predicate][1]
            for predicate, atom in identity_by_predicate.items()
        ):
            _fail(
                "version_identity_evidence_mismatch",
                f"version {version['source_id']!r} identity differs from repository evidence",
            )
        if (
            identity_by_predicate["record_doi"]["authority_class"]
            != "primary_repository_metadata"
            or identity_by_predicate["record_version"]["authority_class"]
            != "primary_repository_metadata"
            or identity_by_predicate["record_member_of_concept"]["authority_class"]
            not in {"primary_repository_metadata", "primary_repository_relation"}
        ):
            _fail(
                "version_identity_evidence_mismatch",
                "record identity is not backed by primary repository metadata",
            )
        ordering_atoms = _resolve_evidence_bindings(
            version["ordering_evidence_bindings"],
            by_lane=by_lane,
            item_index=item_index,
            expected_source_id=str(version["source_id"]),
        )
        ordering_by_predicate = _atoms_by_predicate(
            ordering_atoms,
            expected=ORDERING_PREDICATES,
            reason_code="version_order_evidence_incomplete",
        )
        created_at = _timestamp(version["repository_created_at"], field="repository_created_at")
        updated_at = _timestamp(version["repository_updated_at"], field="repository_updated_at")
        if created_at > updated_at or updated_at > observed_at:
            _fail("version_record_time_invalid", "repository record times are reversed or future-dated")
        expected_ordering = {
            "record_created_at": version["repository_created_at"],
            "record_updated_at": version["repository_updated_at"],
        }
        if any(
            atom["subject"] != record_doi or atom["object"] != expected_ordering[predicate]
            for predicate, atom in ordering_by_predicate.items()
        ):
            _fail(
                "version_order_evidence_mismatch",
                f"version {version['source_id']!r} ordering fields differ from repository evidence",
            )
        if any(
            atom["authority_class"] != "primary_repository_metadata"
            for atom in ordering_by_predicate.values()
        ):
            _fail(
                "version_order_evidence_mismatch",
                "repository ordering is not backed by primary repository metadata",
            )
        chronological_keys.append((created_at, updated_at, record_doi))
        status_atoms = _resolve_evidence_bindings(
            version["status_evidence_bindings"],
            by_lane=by_lane,
            item_index=item_index,
            expected_source_id=str(version["source_id"]),
        )
        status_by_predicate = _atoms_by_predicate(
            status_atoms,
            expected={"record_status"},
            reason_code="version_status_evidence_mismatch",
        )
        status_atom = status_by_predicate["record_status"]
        if status_atom["subject"] != record_doi or status_atom["object"] != version["status"]:
            _fail(
                "version_status_evidence_mismatch",
                f"version {version['source_id']!r} status differs from repository evidence",
            )
        if version["status"] in {"corrected", "withdrawn", "retracted"} and (
            status_atom["authority_class"]
            not in {"primary_record_note", "publisher_status_notice"}
            or status_atom["claim_digest"] is None
        ):
            _fail(
                "version_status_evidence_mismatch",
                "corrected, withdrawn, and retracted states require an exact primary or publisher notice claim",
            )
        if version["status"] in {"current", "superseded"} and (
            status_atom["authority_class"] != "primary_repository_metadata"
        ):
            _fail(
                "version_status_evidence_mismatch",
                "current and superseded states require primary repository metadata",
            )
    if chronological_keys != sorted(chronological_keys):
        _fail(
            "version_chronology_invalid",
            "version ordinals disagree with repository creation/update order and DOI tie-breaker",
        )
    terminal = ordered[-1]
    if payload["terminal_source_id"] != terminal["source_id"]:
        _fail("version_terminal_source_mismatch", "terminal source does not equal the last ordinal node")
    expected_current = (
        terminal["source_id"] if terminal["status"] in {"current", "corrected"} else None
    )
    if payload["current_source_id"] != expected_current:
        _fail(
            "version_current_source_mismatch",
            "current source conflicts with the terminal administrative state",
        )
    actual_edges: set[tuple[str, str]] = set()
    version_index = {str(row["source_id"]): row for row in versions}
    for edge in payload["edges"]:
        _validate_self_digest(
            edge,
            "edge_digest",
            reason_code="version_edge_digest_mismatch",
            label=f"version edge {edge['edge_id']!r}",
        )
        pair = (str(edge["from_source_id"]), str(edge["to_source_id"]))
        actual_edges.add(pair)
        from_version = version_index.get(pair[0])
        to_version = version_index.get(pair[1])
        if from_version is None or to_version is None:
            _fail("version_edge_endpoint_unknown", "version edge names an unknown endpoint")
        relation_names = [str(row["relation"]) for row in edge["relations"]]
        if len(relation_names) != len(set(relation_names)):
            _fail("version_edge_relation_duplicate", "version edge repeats a relation")
        if not {"revision", "supersedes"}.issubset(relation_names):
            _fail(
                "version_edge_relation_incomplete",
                f"version edge {edge['edge_id']!r} omits revision or supersession",
            )
        from_doi = str(from_version["record_doi"])
        to_doi = str(to_version["record_doi"])
        for relation in edge["relations"]:
            _validate_self_digest(
                relation,
                "relation_digest",
                reason_code="version_relation_digest_mismatch",
                label=f"version relation {relation['relation']!r}",
            )
            atoms = _resolve_evidence_bindings(
                relation["evidence_bindings"],
                by_lane=by_lane,
                item_index=item_index,
                expected_source_id=pair[1],
            )
            expected_predicate = RELATION_PREDICATES[relation["relation"]]
            if any(
                atom["predicate"] != expected_predicate
                or atom["subject"] != to_doi
                or atom["object"] != from_doi
                for atom in atoms
            ):
                _fail(
                    "version_relation_evidence_mismatch",
                    f"relation {relation['relation']!r} is not evidenced for the exact edge",
                )
            expected_authority = (
                "primary_repository_relation"
                if relation["relation"] in {"revision", "supersedes"}
                else "primary_record_note"
            )
            if any(atom["authority_class"] != expected_authority for atom in atoms):
                _fail(
                    "version_relation_evidence_mismatch",
                    f"relation {relation['relation']!r} uses the wrong authority class",
                )
            claims = _bound_claim_digests(atoms)
            if relation["claim_digests"] != claims:
                _fail(
                    "version_relation_evidence_mismatch",
                    f"relation {relation['relation']!r} claim-digest closure differs",
                )
            if relation["relation"] in {
                "corrects",
                "narrows_scope",
                "broadens_scope",
                "changes_scope",
                "changes_architecture",
            } and not claims:
                _fail(
                    "version_relation_evidence_mismatch",
                    f"relation {relation['relation']!r} lacks an exact primary claim digest",
                )
        _validate_delta(
            edge["scope_delta"],
            rules=SCOPE_DELTA_RULES,
            relations=set(relation_names),
            by_lane=by_lane,
            item_index=item_index,
            expected_source_id=pair[1],
            from_doi=from_doi,
            to_doi=to_doi,
            kind="scope",
        )
        _validate_delta(
            edge["architecture_delta"],
            rules=ARCHITECTURE_DELTA_RULES,
            relations=set(relation_names),
            by_lane=by_lane,
            item_index=item_index,
            expected_source_id=pair[1],
            from_doi=from_doi,
            to_doi=to_doi,
            kind="architecture",
        )
    if actual_edges != expected_edges or len(actual_edges) != len(payload["edges"]):
        _fail("version_edge_chain_mismatch", "version edges do not form the exact ordinal chain")
    if sources is not None:
        source_index = {str(source["source_id"]): source for source in sources}
        if not set(source_ids).issubset(source_index):
            _fail("version_source_missing", "a version graph node is absent from the acquisition")
        for version in versions:
            source = source_index[str(version["source_id"])]
            expected_status = "none_known" if version["status"] == "current" else version["status"]
            if (
                source["work_identity"] != payload["work_identity"]
                or source.get("doi") != version["record_doi"]
                or source["source_version"] != version["source_version"]
                or source["publication_date"] != version["publication_date"]
                or source["correction_status"] != expected_status
            ):
                _fail(
                    "version_source_metadata_mismatch",
                    f"version graph metadata disagrees with source {version['source_id']!r}",
                )


def _canonical_doi(value: Any) -> str:
    text = str(value).strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if text.startswith(prefix):
            text = text[len(prefix) :]
            break
    return text


def _resolve_evidence_bindings(
    bindings: Sequence[Mapping[str, Any]],
    *,
    by_lane: Mapping[str, Mapping[str, Any]],
    item_index: Mapping[tuple[str, str], Mapping[str, Any]],
    expected_source_id: str | None,
) -> list[Mapping[str, Any]]:
    _unique(
        list(bindings),
        reason_code="duplicate_version_evidence_binding",
        label="version evidence bindings",
    )
    resolved: list[Mapping[str, Any]] = []
    for binding in bindings:
        lane_id = str(binding["artifact_lane_id"])
        item_id = str(binding["item_id"])
        artifact = by_lane.get(lane_id)
        if artifact is None or binding["artifact_content_digest"] != artifact["content_digest"]:
            _fail("version_artifact_binding_mismatch", "version evidence names the wrong artifact digest")
        item = item_index.get((lane_id, item_id))
        if item is None:
            _fail("version_item_binding_missing", "version evidence names an absent tool result item")
        observation = item["source_observation"]
        if binding["item_digest"] != item["item_digest"]:
            _fail("version_evidence_item_digest_mismatch", "version evidence names the wrong item digest")
        if binding["observation_digest"] != observation["observation_digest"]:
            _fail(
                "version_evidence_observation_digest_mismatch",
                "version evidence names the wrong observation digest",
            )
        if binding["source_id"] != observation["source_id"] or (
            expected_source_id is not None and observation["source_id"] != expected_source_id
        ):
            _fail(
                "version_evidence_source_mismatch",
                "version evidence item describes another source",
            )
        evidence_index = {
            str(row["evidence_id"]): row for row in observation.get("lineage_evidence", [])
        }
        atom = evidence_index.get(str(binding["evidence_id"]))
        if atom is None:
            _fail("version_evidence_reference_missing", "version evidence names an absent evidence atom")
        if binding["evidence_digest"] != atom["evidence_digest"]:
            _fail(
                "version_evidence_reference_digest_mismatch",
                "version evidence names the wrong evidence-atom digest",
            )
        allowed_authorities = {
            "primary_api_metadata": {
                "primary_repository_metadata",
                "primary_repository_relation",
                "primary_record_note",
            },
            "primary_page_metadata": {
                "primary_repository_metadata",
                "primary_repository_relation",
                "primary_record_note",
                "publisher_status_notice",
            },
            "publisher_metadata": {"publisher_status_notice"},
            "search_result_metadata": {"bounded_capture_limitation"},
        }[item["retrieval_class"]]
        if (
            binding["evidence_kind"] != atom["authority_class"]
            or atom["authority_class"] not in allowed_authorities
        ):
            _fail(
                "version_evidence_kind_mismatch",
                "version evidence kind conflicts with the bound item's retrieval class",
            )
        resolved.append(atom)
    return resolved


def _atoms_by_predicate(
    atoms: Sequence[Mapping[str, Any]],
    *,
    expected: set[str],
    reason_code: str,
) -> dict[str, Mapping[str, Any]]:
    predicates = [str(atom["predicate"]) for atom in atoms]
    if set(predicates) != expected or len(predicates) != len(expected):
        _fail(reason_code, "evidence predicates are incomplete, duplicated, or out of scope")
    return {str(atom["predicate"]): atom for atom in atoms}


def _bound_claim_digests(atoms: Sequence[Mapping[str, Any]]) -> list[str]:
    return sorted({str(atom["claim_digest"]) for atom in atoms if atom["claim_digest"] is not None})


def _validate_delta(
    delta: Mapping[str, Any],
    *,
    rules: Mapping[str, tuple[str, str | None]],
    relations: set[str],
    by_lane: Mapping[str, Mapping[str, Any]],
    item_index: Mapping[tuple[str, str], Mapping[str, Any]],
    expected_source_id: str,
    from_doi: str,
    to_doi: str,
    kind: str,
) -> None:
    _validate_self_digest(
        delta,
        "delta_digest",
        reason_code=f"version_{kind}_delta_digest_mismatch",
        label=f"version {kind} delta",
    )
    predicate, required_relation = rules[str(delta["classification"])]
    atoms = _resolve_evidence_bindings(
        delta["evidence_bindings"],
        by_lane=by_lane,
        item_index=item_index,
        expected_source_id=expected_source_id,
    )
    if any(
        atom["predicate"] != predicate
        or atom["subject"] != to_doi
        or atom["object"] != from_doi
        for atom in atoms
    ):
        _fail(
            f"version_{kind}_delta_evidence_mismatch",
            f"{kind} delta is not evidenced for the exact edge",
        )
    claims = _bound_claim_digests(atoms)
    if delta["claim_digests"] != claims:
        _fail(
            f"version_{kind}_delta_evidence_mismatch",
            f"{kind} delta claim-digest closure differs",
        )
    unresolved = str(delta["classification"]) == "unresolved"
    if unresolved:
        if claims or any(atom["authority_class"] != "bounded_capture_limitation" for atom in atoms):
            _fail(
                f"version_{kind}_delta_evidence_mismatch",
                f"unresolved {kind} delta must bind only an explicit capture limitation",
            )
    elif str(delta["classification"]) != "unchanged" and not claims:
        _fail(
            f"version_{kind}_delta_evidence_mismatch",
            f"changed {kind} delta lacks an exact source claim digest",
        )
    elif not unresolved and any(
        atom["authority_class"] not in {"primary_record_note", "primary_repository_metadata"}
        for atom in atoms
    ):
        _fail(
            f"version_{kind}_delta_evidence_mismatch",
            f"{kind} delta uses the wrong authority class",
        )
    correlated_relations = {relation for _predicate, relation in rules.values() if relation}
    if required_relation is None:
        if relations & correlated_relations:
            _fail(
                "version_edge_delta_relation_mismatch",
                f"{kind} relation exists for an unchanged or unresolved delta",
            )
    elif required_relation not in relations or len(relations & correlated_relations) != 1:
        _fail(
            "version_edge_delta_relation_mismatch",
            f"{kind} delta and relation do not encode the same transition",
        )


def _raw_observation(item: Mapping[str, Any]) -> dict[str, Any]:
    observation = copy.deepcopy(dict(item["source_observation"]))
    observation.pop("observation_digest", None)
    return observation


def reconstruct_normalized_sources(
    artifacts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Recreate the exact normalized source set from included tool-visible items."""

    by_lane, _items = _artifact_index(artifacts)
    lane_sources: list[tuple[str, Mapping[str, Any]]] = []
    for lane_id, artifact in by_lane.items():
        item_by_id = {item["item_id"]: item for item in artifact["result_items"]}
        seen_in_lane: set[str] = set()
        for link in artifact["normalization_links"]:
            if not str(link["disposition"]).startswith("included"):
                continue
            item = item_by_id[link["item_id"]]
            source_id = str(link["source_id"])
            if source_id in seen_in_lane:
                _fail(
                    "duplicate_lane_source",
                    f"lane {lane_id!r} includes source {source_id!r} more than once",
                )
            seen_in_lane.add(source_id)
            lane_sources.append((lane_id, _raw_observation(item)))
    sources, duplicate_groups, claim_conflicts, metadata_conflicts = _merge_sources(
        lane_sources
    )
    if duplicate_groups or claim_conflicts or metadata_conflicts:
        _fail(
            "tool_source_observation_conflict",
            "the sealed lane observations disagree for one work/version and require unresolved merging",
        )
    return sources


def validate_capture_acquisition_bundle(
    *,
    capture: Mapping[str, Any],
    acquisition: Mapping[str, Any],
    artifacts_by_path: Mapping[str, tuple[Mapping[str, Any], bytes]],
    version_graphs: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Cross-check capture, transcript bytes, normalized acquisition, and lineages."""

    try:
        validate_payload(capture, CURRENT_CAPTURE_SCHEMA)
        validate_snapshot(acquisition)
    except Exception as exc:
        raise LiteratureAcquisitionError(
            "capture_or_acquisition_schema_invalid", str(exc)
        ) from exc
    _validate_self_digest(
        capture,
        "content_digest",
        reason_code="capture_digest_mismatch",
        label=f"current capture {capture.get('capture_id')!r}",
    )
    target_id = str(capture["target_id"])
    if acquisition["target_id"] != target_id:
        _fail("bundle_target_mismatch", "capture and acquisition targets differ")
    if not version_graphs:
        _fail("version_graph_required", "current acquisition requires a version graph")
    if list(capture["version_lineages"]) != list(version_graphs):
        _fail("capture_version_graph_mismatch", "loaded version graphs differ from capture bytes")
    capture_started = _timestamp(capture["capture_started_at"], field="capture_started_at")
    capture_completed = _timestamp(capture["capture_completed_at"], field="capture_completed_at")
    cutoff = _timestamp(capture["coverage_cutoff"], field="coverage_cutoff")
    if capture_started > capture_completed or capture_completed != cutoff:
        _fail("capture_time_boundary_invalid", "capture interval and coverage cutoff disagree")
    if (
        acquisition["search_started_at"] != capture["capture_started_at"]
        or acquisition["search_completed_at"] != capture["capture_completed_at"]
        or acquisition["coverage_cutoff"] != capture["coverage_cutoff"]
    ):
        _fail("capture_acquisition_time_mismatch", "acquisition timestamps differ from capture")
    descriptors = capture.get("provider_response_artifacts")
    if not isinstance(descriptors, list) or len(descriptors) != len(LANE_TYPES):
        _fail("response_descriptor_count_mismatch", "capture requires exactly six response descriptors")
    artifacts: list[Mapping[str, Any]] = []
    descriptor_lanes: set[str] = set()
    exact_byte_digests: set[str] = set()
    receipt_ids = [str(row["lane_id"]) for row in acquisition["lane_receipts"]]
    capture_lane_ids = [str(row["lane_id"]) for row in capture["lanes"]]
    result_ids = [str(row["result_id"]) for row in capture["raw_results"]]
    if len(receipt_ids) != len(set(receipt_ids)) or len(capture_lane_ids) != len(set(capture_lane_ids)):
        _fail("duplicate_bundle_lane", "capture or acquisition repeats a lane identifier")
    if len(result_ids) != len(set(result_ids)):
        _fail("duplicate_capture_result", "capture repeats a raw-result identifier")
    receipts = {str(row["lane_id"]): row for row in acquisition["lane_receipts"]}
    capture_lanes = {str(row["lane_id"]): row for row in capture["lanes"]}
    raw_results = {str(row["result_id"]): row for row in capture["raw_results"]}
    descriptor_paths = [str(row["path"]) for row in descriptors]
    if len(descriptor_paths) != len(set(descriptor_paths)):
        _fail("duplicate_response_descriptor_path", "two response descriptors share a path")
    if set(descriptor_paths) != set(artifacts_by_path):
        _fail("response_artifact_set_mismatch", "loaded response paths do not exactly match descriptors")
    linked_result_ids: set[str] = set()
    for descriptor in descriptors:
        if set(descriptor) != {
            "lane_id",
            "path",
            "sha256",
            "size_bytes",
            "acquired_at",
            "provider_request_id",
            "source_ids",
        }:
            _fail("response_descriptor_field_drift", "response descriptor has an unknown or missing field")
        path = str(descriptor["path"])
        if path not in artifacts_by_path:
            _fail("response_descriptor_path_missing", f"response descriptor path is not loaded: {path}")
        artifact, data = artifacts_by_path[path]
        validate_tool_response_artifact(artifact)
        if artifact["target_id"] != target_id:
            _fail("bundle_target_mismatch", f"artifact {path!r} names another target")
        artifact_started_raw, artifact_completed_raw = _artifact_execution_window(artifact)
        artifact_started = _timestamp(
            artifact_started_raw, field="artifact observed_started_at"
        )
        artifact_completed = _timestamp(
            artifact_completed_raw, field="artifact observed_completed_at"
        )
        if artifact_started < capture_started or artifact_completed > capture_completed:
            _fail("artifact_time_outside_capture", f"artifact {path!r} lies outside the capture interval")
        lane_id = str(descriptor["lane_id"])
        if lane_id in descriptor_lanes:
            _fail("duplicate_response_descriptor_lane", f"duplicate descriptor for lane {lane_id!r}")
        descriptor_lanes.add(lane_id)
        byte_digest = hashlib.sha256(data).hexdigest()
        if byte_digest in exact_byte_digests:
            _fail("duplicate_response_artifact_bytes", "two lanes reuse identical response bytes")
        exact_byte_digests.add(byte_digest)
        if descriptor["sha256"] != byte_digest or descriptor["size_bytes"] != len(data):
            _fail("response_descriptor_byte_mismatch", f"descriptor bytes drift for lane {lane_id!r}")
        receipt = receipts.get(lane_id)
        lane = capture_lanes.get(lane_id)
        if receipt is None or lane is None:
            _fail("response_lane_missing", f"lane {lane_id!r} is absent from capture or acquisition")
        included_source_ids = sorted(
            link["source_id"]
            for link in artifact["normalization_links"]
            if str(link["disposition"]).startswith("included")
        )
        primary_search = _primary_search_execution(artifact)
        if (
            artifact["lane_id"] != lane_id
            or artifact["lane_type"] != lane["lane_type"]
            or [primary_search["query"]] != lane["queries"]
            or lane["queries"] != receipt["queries"]
            or artifact_completed_raw != descriptor["acquired_at"]
            or descriptor["acquired_at"] != receipt["completed_at"]
            or descriptor["provider_request_id"] != primary_search["execution_id"]
            or sorted(descriptor["source_ids"]) != included_source_ids
            or included_source_ids != sorted(receipt["source_ids"])
        ):
            _fail("response_lane_semantic_mismatch", f"descriptor/transcript/lane/receipt drift for {lane_id!r}")
        artifact_result_ids = {
            str(link["capture_result_id"]) for link in artifact["normalization_links"]
        }
        if artifact_result_ids != {str(item) for item in lane["raw_result_ids"]}:
            _fail("response_result_closure_mismatch", f"lane result closure drift for {lane_id!r}")
        items = {str(item["item_id"]): item for item in artifact["result_items"]}
        for link in artifact["normalization_links"]:
            result_id = str(link["capture_result_id"])
            linked_result_ids.add(result_id)
            result = raw_results.get(result_id)
            item = items[str(link["item_id"])]
            if result is None or (
                result["source_id"] != link["source_id"]
                or result["disposition"] != link["disposition"]
                or result["title"] != item["title"]
                or result["url"] != item["url"]
            ):
                _fail("response_result_semantic_mismatch", f"capture raw result drift for {result_id!r}")
        artifacts.append(artifact)
    if set(raw_results) != linked_result_ids:
        _fail("capture_result_orphan", "capture contains an unbound or missing raw result")
    expected_sources = reconstruct_normalized_sources(artifacts)
    if expected_sources != acquisition["sources"]:
        _fail(
            "acquisition_source_reconstruction_mismatch",
            "normalized acquisition sources do not exactly reconstruct from sealed tool artifacts",
        )
    seen_lineage_sources: set[str] = set()
    seen_lineage_work_identities: set[str] = set()
    for graph in version_graphs:
        validate_source_version_graph(
            graph,
            artifacts=artifacts,
            sources=acquisition["sources"],
            expected_target_id=target_id,
        )
        graph_observed = _timestamp(graph["observed_at"], field="version graph observed_at")
        if not capture_started <= graph_observed <= capture_completed:
            _fail("version_graph_time_outside_capture", "version graph observation lies outside capture")
        graph_sources = {str(row["source_id"]) for row in graph["versions"]}
        work_identity = str(graph["work_identity"])
        if work_identity in seen_lineage_work_identities:
            _fail(
                "version_graph_duplicate_work_identity",
                "one work identity is split across multiple lineage graphs",
            )
        seen_lineage_work_identities.add(work_identity)
        if seen_lineage_sources & graph_sources:
            _fail("version_graph_overlap", "a source occurs in more than one lineage graph")
        seen_lineage_sources.update(graph_sources)
        same_work_sources = {
            str(source["source_id"])
            for source in acquisition["sources"]
            if source["work_identity"] == graph["work_identity"]
        }
        if graph_sources != same_work_sources:
            _fail(
                "version_lineage_coverage_mismatch",
                "version graph does not cover every acquired version of its work identity",
            )
    routing_eligibility = {
        str(version["source_id"]): version["present_investment_eligibility"]
        for graph in version_graphs
        for version in graph["versions"]
    }
    for source in acquisition["sources"]:
        source_id = str(source["source_id"])
        inferred = {
            "superseded": "blocked_positive_support",
            "withdrawn": "negative_evidence_only",
            "retracted": "negative_evidence_only",
        }.get(str(source.get("correction_status")), "unverified_audit_only")
        existing = routing_eligibility.get(source_id)
        if existing is not None and existing != inferred:
            _fail(
                "source_routing_status_conflict",
                f"source {source_id!r} correction state conflicts with lineage routing",
            )
        routing_eligibility[source_id] = inferred
    return {
        "capture_content_digest": capture["content_digest"],
        "acquisition_content_digest": acquisition["content_digest"],
        "tool_response_content_digests": sorted(
            artifact["content_digest"] for artifact in artifacts
        ),
        "version_graph_content_digests": sorted(
            graph["content_digest"] for graph in version_graphs
        ),
        "source_ids": sorted(source["source_id"] for source in expected_sources),
        "source_routing_eligibility": dict(sorted(routing_eligibility.items())),
        "authority_boundary": (
            "sealed Codex tool-visible metadata and primary-record version metadata; "
            "no raw provider, source-truth, peer-review, novelty, or exhaustiveness authority"
        ),
    }


__all__ = [
    "CURRENT_CAPTURE_SCHEMA",
    "LiteratureAcquisitionError",
    "SOURCE_ROUTING_PRE_MAP_POLICY_SCHEMA",
    "SOURCE_ROUTING_PRE_MAP_STAGES",
    "SOURCE_ROUTING_PRECOMMIT_SCHEMA",
    "SOURCE_ROUTING_PRECOMMIT_STAGES",
    "SOURCE_ROUTING_REALIZATION_SCHEMA",
    "SOURCE_ROUTING_WARRANT_VALIDATION_SCHEMA",
    "TOOL_RESPONSE_KIND",
    "TOOL_RESPONSE_KIND_V2",
    "TOOL_RESPONSE_SCHEMA",
    "TOOL_RESPONSE_SCHEMA_V2",
    "VERSION_GRAPH_SCHEMA",
    "build_source_routing_pre_map_policy",
    "build_source_routing_precommit_certificate",
    "build_source_routing_realization",
    "build_source_routing_warrant_validation_packet",
    "derive_source_routing_semantic_warrants",
    "load_tool_response_artifact",
    "reconstruct_normalized_sources",
    "source_routing_realization_requirements",
    "top_level_content_digest",
    "validate_capture_acquisition_bundle",
    "validate_source_routing_consumption",
    "validate_source_routing_pre_map_policy",
    "validate_source_routing_precommit_certificate",
    "validate_source_routing_realization",
    "validate_source_routing_warrant_validation_packet",
    "validate_source_version_graph",
    "validate_tool_response_artifact",
]
