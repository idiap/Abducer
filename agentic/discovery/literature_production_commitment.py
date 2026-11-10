# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Portable commitment boundary for a literature-production manifest.

The production chain itself proves a bounded local causal statement by
reexecuting exact source, implementation, and dependency bytes.  A later
theory commit needs a narrower object: a root-relative descriptor for the
already validated manifest bytes plus a consumer projection that cannot erase
the chain's authored-fallback, non-material, correlated-panel, or authority
limits.

This module deliberately has no world-commissioning or publication API.  It
does not replay the original source bundle after relocation.  It reopens one
canonical manifest byte string, validates every internal causal seal, and
returns only its bounded pre-commission theory-input projection.
"""

from __future__ import annotations

import copy
import json
import os
import stat
from collections.abc import Mapping
from pathlib import Path, PurePosixPath
from typing import Any

from agentic.discovery.contracts import (
    ContractError,
    bytes_digest,
    canonical_digest,
    canonical_json,
    stable_identifier,
    validate_payload,
)


COMMITMENT_SCHEMA_NAME = "literature_production_manifest_commitment.schema.json"
MANIFEST_SCHEMA_NAME = "literature_production_chain_manifest.schema.json"
BUNDLE_SCHEMA_NAME = "literature_production_input_bundle.schema.json"
LIVE_CHAIN_KIND = "publication_disabled_live_model_literature_to_theory"

ORDERED_STAGE_IDS: tuple[str, ...] = (
    "acquisition_reopen",
    "source_pre_map_policy",
    "warrant_validation",
    "claim_mapping",
    "assimilation",
    "source_routing_realization",
    "high_risk_input",
    "parent_reflection",
    "parent_conceptual_adjudication",
    "theory_only_synthesis",
    "synthesis_conceptual_adjudication",
)

_ADJUDICATION_DERIVATIONS = {
    "parent_conceptual_adjudication": "parent_reflection",
    "synthesis_conceptual_adjudication": "theory_only_synthesis",
}
_RETROSPECTIVE_INPUT_ROLES = frozenset(
    {
        "typed_parent_systems",
        "typed_synthesis_systems",
        "typed_conceptual_systems",
    }
)
_RECEIPT_AUTHORITY_BOUNDARY = (
    "This receipt proves exact portable manifest-byte identity and internal "
    "causal-seal consistency only. It does not rerun the source bundle or code "
    "closure and grants no source truth, latestness, exhaustiveness, literature "
    "benefit, external or independent preference, creativity, philosophical "
    "depth, physics value, theorem, experiment, publication, or world authority."
)
_CONSUMER_AUTHORITY_BOUNDARY = (
    "Pre-commission theory may consume these exact bounded outputs and their "
    "negative authority fields only. The projection preserves authored fallback, "
    "zero material synthesis improvement, internally correlated adjudication, "
    "unavailable external human evidence, and every publication, world, truth, "
    "latestness, exhaustiveness, benefit, creativity, physics, theorem, "
    "independence, and experiment null; it cannot promote any of them."
)
_BUNDLE_AUTHORITY_BOUNDARY = (
    "The bundle carries exact canonical manifest bytes, their replayed commitment "
    "receipt, and bounded semantic stage values for later theory consumption. It "
    "proves only local production identity and causal availability; it grants no "
    "source truth, global latestness, exhaustive coverage, literature benefit, "
    "external or independent preference, creativity, philosophical depth, physics "
    "value, theorem, experiment, publication, or world authority."
)
_SEMANTIC_ROLE_PLAN: tuple[tuple[str, int, str], ...] = (
    ("high_risk_portfolio", 0, "high_risk_input"),
    ("reflective_packets", 0, "parent_reflection"),
    (
        "parent_conceptual_adjudication",
        0,
        "parent_conceptual_adjudication",
    ),
    ("reflective_packets", 1, "theory_only_synthesis"),
    (
        "synthesis_conceptual_adjudication",
        0,
        "synthesis_conceptual_adjudication",
    ),
)
_BUNDLE_AUTHORITY_NULLS = {
    "source_truth_authority": None,
    "global_latestness_authority": None,
    "exhaustiveness_authority": None,
    "literature_benefit_authority": None,
    "external_preference_authority": None,
    "independent_preference_authority": None,
    "creativity_authority": None,
    "philosophical_depth_authority": None,
    "physics_value_authority": None,
    "theorem_authority": None,
    "experiment_authority": None,
    "publication_authority": None,
    "world_authority": None,
}


class LiteratureProductionCommitmentError(ContractError):
    """Stable failure at the portable committed-input boundary."""

    def __init__(self, reason_code: str, message: str) -> None:
        self.reason_code = reason_code
        super().__init__(f"literature_production_commitment[{reason_code}]: {message}")


def _fail(reason_code: str, message: str) -> None:
    raise LiteratureProductionCommitmentError(reason_code, message)


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = copy.deepcopy(dict(value))
    result.pop(field, None)
    return result


def _canonical_relative_path(raw: str) -> PurePosixPath:
    """Return one canonical immutable POSIX child path."""

    if not isinstance(raw, str):
        _fail("manifest_path_invalid", "manifest path must be a string")
    path = PurePosixPath(raw)
    if (
        not raw
        or "\\" in raw
        or path.is_absolute()
        or path.as_posix() != raw
        or any(part in {"", ".", ".."} for part in path.parts)
        or any(
            part.lower() in {"latest", "latest.json", "current"}
            for part in path.parts
        )
    ):
        _fail(
            "manifest_path_invalid",
            f"manifest path is not one immutable canonical child: {raw!r}",
        )
    return path


def _read_exact_regular_file(root: Path, relative_path: str) -> bytes:
    """Read through anchored descriptors and reject link or race substitution."""

    path = _canonical_relative_path(relative_path)
    try:
        resolved_root = root.resolve(strict=True)
    except OSError as exc:
        raise LiteratureProductionCommitmentError(
            "commit_root_unreadable", f"cannot resolve commitment root: {exc}"
        ) from exc
    directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    no_follow = getattr(os, "O_NOFOLLOW", 0)
    descriptors: list[int] = []
    try:
        directory = os.open(resolved_root, directory_flags | no_follow)
        descriptors.append(directory)
        for part in path.parts[:-1]:
            directory = os.open(
                part,
                directory_flags | no_follow,
                dir_fd=directory,
            )
            descriptors.append(directory)
        file_descriptor = os.open(
            path.parts[-1],
            os.O_RDONLY | no_follow,
            dir_fd=descriptors[-1],
        )
        descriptors.append(file_descriptor)
        before = os.fstat(file_descriptor)
        if not stat.S_ISREG(before.st_mode):
            _fail("manifest_not_regular", "manifest is not a regular file")
        if before.st_nlink != 1:
            _fail("manifest_hardlink_rejected", "manifest has multiple hard links")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(file_descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(file_descriptor)
        named_after = os.stat(
            path.parts[-1],
            dir_fd=descriptors[-2],
            follow_symlinks=False,
        )
        identity_fields = (
            "st_dev",
            "st_ino",
            "st_mode",
            "st_nlink",
            "st_size",
            "st_mtime_ns",
            "st_ctime_ns",
        )
        identities = [
            tuple(getattr(row, field) for field in identity_fields)
            for row in (before, after, named_after)
        ]
        if identities[0] != identities[1] or identities[1] != identities[2]:
            _fail(
                "manifest_changed_during_read",
                "manifest identity changed during descriptor-anchored read",
            )
        return b"".join(chunks)
    except LiteratureProductionCommitmentError:
        raise
    except OSError as exc:
        raise LiteratureProductionCommitmentError(
            "manifest_unreadable", f"cannot read committed manifest: {exc}"
        ) from exc
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def _decode_canonical_manifest(data: bytes) -> dict[str, Any]:
    """Require the single canonical UTF-8 JSON plus-LF representation."""

    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LiteratureProductionCommitmentError(
            "manifest_json_invalid", f"manifest is not one UTF-8 JSON value: {exc}"
        ) from exc
    if not isinstance(value, dict):
        _fail("manifest_not_object", "manifest JSON must be one object")
    if canonical_json(value) + b"\n" != data:
        _fail(
            "manifest_bytes_not_canonical",
            "manifest bytes are not canonical JSON UTF-8 with one trailing LF",
        )
    return value


def _validate_derived_intermediates(stage: Mapping[str, Any]) -> None:
    stage_id = str(stage["stage_id"])
    bindings = list(stage["request"]["input_bindings"])
    retrospective = {
        str(row.get("role"))
        for row in bindings
        if str(row.get("role")) in _RETROSPECTIVE_INPUT_ROLES
    }
    if retrospective:
        _fail(
            "derived_intermediate_promoted_to_input",
            f"stage {stage_id} promotes stage-local rows: {sorted(retrospective)}",
        )
    rows = list(stage["derived_intermediates"])
    expected_source_role = _ADJUDICATION_DERIVATIONS.get(stage_id)
    if expected_source_role is None:
        if rows:
            _fail(
                "derived_intermediate_stage_invalid",
                f"non-adjudication stage {stage_id} declares derived intermediates",
            )
        return
    if len(rows) != 1:
        _fail(
            "derived_intermediate_cardinality_invalid",
            f"adjudication stage {stage_id} requires one typed-system derivation",
        )
    row = rows[0]
    if (
        row.get("role") != "typed_conceptual_systems"
        or row.get("derivation_kind")
        != "stage_internal_deterministic_projection"
        or row.get("derived_from_input_roles") != [expected_source_role]
        or row.get("authority_class")
        != "derived_non_authoritative_intermediate"
    ):
        _fail(
            "derived_intermediate_typing_invalid",
            f"adjudication stage {stage_id} mis-types its stage-local projection",
        )
    output = stage["output"]["payload"]
    try:
        evidence_digest = output["input_binding"]["conceptual_systems_digest"]
        blind_digest = output["blind_packet"]["source_bindings"][
            "conceptual_systems_digest"
        ]
        candidate_count = len(output["blind_packet"]["candidates"])
    except (KeyError, TypeError) as exc:
        raise LiteratureProductionCommitmentError(
            "derived_intermediate_evidence_missing",
            f"adjudication stage {stage_id} lacks its typed-system evidence seal",
        ) from exc
    if (
        row.get("content_digest") != evidence_digest
        or row.get("content_digest") != blind_digest
        or row.get("row_count") != candidate_count
        or expected_source_role
        not in {str(binding.get("role")) for binding in bindings}
    ):
        _fail(
            "derived_intermediate_evidence_mismatch",
            f"adjudication stage {stage_id} derived rows differ from stage evidence",
        )


def _validate_manifest_internal(value: Mapping[str, Any]) -> dict[str, Any]:
    """Validate schema and every causal seal available within manifest bytes."""

    manifest = copy.deepcopy(dict(value))
    validate_payload(manifest, MANIFEST_SCHEMA_NAME)
    if manifest["manifest_digest"] != canonical_digest(
        _without(manifest, "manifest_digest")
    ):
        _fail("manifest_digest_mismatch", "manifest self-digest is invalid")
    stages = list(manifest["stages"])
    stage_ids = [str(row["stage_id"]) for row in stages]
    if (
        stage_ids != list(ORDERED_STAGE_IDS)
        or list(manifest["ordered_stage_ids"]) != stage_ids
        or [row["stage_index"] for row in stages] != list(range(len(stage_ids)))
    ):
        _fail("manifest_stage_order_invalid", "manifest stage vector is not exact")

    for stage in stages:
        stage_id = str(stage["stage_id"])
        request = stage["request"]
        receipt = stage["receipt"]
        implementation = stage["implementation"]
        output = stage["output"]
        if (
            request["stage_id"] != stage_id
            or request["target_id"] != manifest["target_id"]
            or request["run_id"] != manifest["run_id"]
            or request["state_version"] != manifest["state_version"]
        ):
            _fail(
                "manifest_stage_identity_mismatch",
                f"stage {stage_id} request crossed manifest identity",
            )
        if request["input_digest"] != canonical_digest(request["input_bindings"]):
            _fail(
                "manifest_stage_input_digest_mismatch",
                f"stage {stage_id} input digest is invalid",
            )
        if request["request_digest"] != canonical_digest(
            _without(request, "request_digest")
        ):
            _fail(
                "manifest_stage_request_digest_mismatch",
                f"stage {stage_id} request self-digest is invalid",
            )
        expected_request_id = stable_identifier(
            "production-request",
            stage_id,
            {
                "target_id": manifest["target_id"],
                "run_id": manifest["run_id"],
                "state_version": manifest["state_version"],
            },
            request["input_digest"],
            request["implementation_digest"],
            request["created_at"],
        )
        if request["request_id"] != expected_request_id:
            _fail(
                "manifest_stage_request_id_mismatch",
                f"stage {stage_id} request ID is not deterministically bound",
            )
        if implementation["dependency_set_digest"] != canonical_digest(
            implementation["dependencies"]
        ) or implementation["implementation_digest"] != canonical_digest(
            _without(implementation, "implementation_digest")
        ):
            _fail(
                "manifest_stage_implementation_digest_mismatch",
                f"stage {stage_id} implementation seal is invalid",
            )
        if (
            request["implementation_digest"]
            != implementation["implementation_digest"]
            or request["dependency_set_digest"]
            != implementation["dependency_set_digest"]
        ):
            _fail(
                "manifest_stage_implementation_binding_mismatch",
                f"stage {stage_id} request does not bind its implementation",
            )
        if output["content_digest"] != canonical_digest(output["payload"]):
            _fail(
                "manifest_stage_output_digest_mismatch",
                f"stage {stage_id} output digest is invalid",
            )
        output_schema = output["schema_path"]
        if output_schema is not None:
            schema_path = _canonical_relative_path(str(output_schema))
            if (
                len(schema_path.parts) != 3
                or schema_path.parts[:2] != ("agentic", "spec")
                or not schema_path.name.endswith(".schema.json")
            ):
                _fail(
                    "manifest_stage_output_schema_path_invalid",
                    f"stage {stage_id} names a non-local output schema",
                )
            validate_payload(output["payload"], schema_path.name)
        if (
            stage["status"] != "succeeded"
            or receipt["status"] != stage["status"]
            or receipt["request_id"] != request["request_id"]
            or receipt["request_digest"] != request["request_digest"]
            or receipt["input_digest"] != request["input_digest"]
            or receipt["output_digest"] != output["content_digest"]
            or receipt["implementation_digest"]
            != implementation["implementation_digest"]
            or receipt["dependency_set_digest"]
            != implementation["dependency_set_digest"]
        ):
            _fail(
                "manifest_stage_receipt_binding_mismatch",
                f"stage {stage_id} receipt does not close request and output",
            )
        expected_receipt_id = stable_identifier(
            "production-receipt",
            request["request_digest"],
            receipt["status"],
            output["content_digest"],
            receipt["completed_at"],
        )
        if (
            receipt["receipt_id"] != expected_receipt_id
            or receipt["started_at"] != request["created_at"]
        ):
            _fail(
                "manifest_stage_receipt_id_mismatch",
                f"stage {stage_id} receipt ID or start time is not deterministic",
            )
        _validate_derived_intermediates(stage)

    order_material = [
        {
            "stage_index": row["stage_index"],
            "stage_id": row["stage_id"],
            "request_id": row["request"]["request_id"],
            "receipt_id": row["receipt"]["receipt_id"],
            "status": row["status"],
            "output_digest": row["output"]["content_digest"],
        }
        for row in stages
    ]
    if manifest["chain_order_digest"] != canonical_digest(order_material):
        _fail("manifest_chain_order_digest_mismatch", "chain-order seal is invalid")
    return manifest


def _stage_map(manifest: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row["stage_id"]): row for row in manifest["stages"]}


def _derive_consumer_projection(manifest: Mapping[str, Any]) -> dict[str, Any]:
    """Project exact theory inputs while preserving every relevant limitation."""

    stages = _stage_map(manifest)
    high_risk_stage = stages["high_risk_input"]
    high_risk = high_risk_stage["output"]["payload"]
    parent_reflection = stages["parent_reflection"]["output"]["payload"]
    parent_evidence = stages["parent_conceptual_adjudication"]["output"]["payload"]
    synthesis = stages["theory_only_synthesis"]["output"]["payload"]
    synthesis_evidence = stages["synthesis_conceptual_adjudication"]["output"][
        "payload"
    ]
    provenance = copy.deepcopy(dict(high_risk["generation_provenance"]))
    reason_codes = list(high_risk_stage["receipt"]["reason_codes"])
    live = manifest["chain_kind"] == LIVE_CHAIN_KIND
    if (
        provenance.get("mode") != "operator_instantiated_from_authored_proposals"
        or provenance.get("proposal_request_digest") is not None
        or "authored_fallback_not_proposal_field_free" not in reason_codes
        or provenance.get("generator_authority_id") != (
            "operator.supplied-proposals" if live else "high-risk-forger.authored-templates.v1")
        or parent_reflection.get("generation_mode") != (
            "operator_generated" if live else "local_structural_fallback")
        or synthesis.get("generation_mode") != "operator_generated"
    ):
        _fail(
            "manifest_generation_provenance_mismatch",
            "manifest no longer exposes the exact authored-fallback generation boundary",
        )

    parent_authority = copy.deepcopy(
        dict(parent_evidence["content_adjudication"]["authority"])
    )
    synthesis_authority = copy.deepcopy(
        dict(synthesis_evidence["content_adjudication"]["authority"])
    )
    for label, authority in (
        ("parent", parent_authority),
        ("synthesis", synthesis_authority),
    ):
        if (
            authority.get("panel_evidence_class")
            != "correlated_internal_critique"
            or authority.get("plural_independent_perspectives") is not False
            or authority.get("external_human_evidence_available") is not False
            or authority.get("external_human_evidence_status") != "unavailable"
            or authority.get("external_generalization_authorized") is not False
        ):
            _fail(
                "manifest_adjudication_authority_mismatch",
                f"{label} adjudication escaped correlated internal authority",
            )

    stage_comparison = copy.deepcopy(
        dict(synthesis_evidence["content_adjudication"]["stage_comparison"])
    )
    semantic_patch = stage_comparison["semantic_patch"]
    if not live and (
        stage_comparison.get("material") is not False
        or stage_comparison.get("new_reflection_rounds") != 0
        or stage_comparison.get("improved_dimensions") != []
        or semantic_patch.get("content_changed") is not False
        or semantic_patch.get("changes") != []
    ):
        _fail(
            "manifest_synthesis_materiality_mismatch",
            "manifest no longer records a non-material synthesis comparison",
        )

    projection: dict[str, Any] = {
        "schema_version": "1.0.0",
        "projection_kind": ("bounded_live_literature_production_theory_input" if live
                            else "bounded_literature_production_theory_input"),
        "input_role": "pre_commission_theory_input",
        "target_id": manifest["target_id"],
        "run_id": manifest["run_id"],
        "state_version": manifest["state_version"],
        "manifest_id": manifest["manifest_id"],
        "manifest_digest": manifest["manifest_digest"],
        "chain_order_digest": manifest["chain_order_digest"],
        "source_bundle_digest": manifest["source_bundle"]["bundle_digest"],
        "stage_output_digests": {
            "high_risk_portfolio": high_risk_stage["output"]["content_digest"],
            "parent_reflection_packet": stages["parent_reflection"]["output"][
                "content_digest"
            ],
            "parent_adjudication_evidence": stages[
                "parent_conceptual_adjudication"
            ]["output"]["content_digest"],
            "theory_only_synthesis_packet": stages["theory_only_synthesis"][
                "output"
            ]["content_digest"],
            "synthesis_adjudication_evidence": stages[
                "synthesis_conceptual_adjudication"
            ]["output"]["content_digest"],
        },
        "theory_generation_provenance": {
            "high_risk": provenance,
            "high_risk_receipt_reason_codes": [
                "authored_fallback_not_proposal_field_free"
            ],
            "proposal_field_free": False,
            "parent_reflection_generation_mode": parent_reflection[
                "generation_mode"
            ],
            "theory_only_synthesis_generation_mode": synthesis[
                "generation_mode"
            ],
        },
        "parent_adjudication_authority": parent_authority,
        "synthesis_adjudication_authority": synthesis_authority,
        "synthesis_materiality": {
            "stage_comparison_digest": canonical_digest(stage_comparison),
            "applicability": stage_comparison["applicability"],
            "material": stage_comparison["material"],
            "current_selected_system_id": stage_comparison[
                "current_selected_system_id"
            ],
            "prior_selected_system_id": stage_comparison[
                "prior_selected_system_id"
            ],
            "improved_dimensions": copy.deepcopy(
                stage_comparison["improved_dimensions"]
            ),
            "new_reflection_rounds": stage_comparison["new_reflection_rounds"],
            "nondegrading_dimension_floors": stage_comparison[
                "nondegrading_dimension_floors"
            ],
            "reflective_resilience_increased": stage_comparison[
                "reflective_resilience_increased"
            ],
            "round_history_prefix_preserved": stage_comparison[
                "round_history_prefix_preserved"
            ],
            "semantic_patch_content_changed": semantic_patch["content_changed"],
            "semantic_patch_change_count": len(semantic_patch["changes"]),
        },
        "claim_boundaries": copy.deepcopy(manifest["claim_boundaries"]),
        "publication_enabled": False,
        "world_commissioning_authorized": False,
        "consumer_authority_boundary": (
            "Pre-commission theory may consume these exact live-acquired and model-authored outputs. "
            "The recorded synthesis comparison is an internal content comparison, not verified improvement "
            "in scientific truth. Proposals are supplied model content, not proposal-field-free elicitation. "
            "All adjudication is internally correlated. No external human, independent preference, source "
            "truth, exhaustiveness, theorem, experiment, publication or world authority is granted."
            if live else _CONSUMER_AUTHORITY_BOUNDARY),
    }
    projection["projection_digest"] = canonical_digest(projection)
    return projection


def _build_descriptor(
    relative_path: str,
    data: bytes,
    manifest: Mapping[str, Any],
) -> dict[str, Any]:
    descriptor: dict[str, Any] = {
        "descriptor_version": "1.0.0",
        "object_kind": "literature_production_chain_manifest",
        "path": _canonical_relative_path(relative_path).as_posix(),
        "sha256": bytes_digest(data),
        "size_bytes": len(data),
        "semantic_digest": canonical_digest(manifest),
        "manifest_schema_version": manifest["schema_version"],
        "manifest_id": manifest["manifest_id"],
        "manifest_digest": manifest["manifest_digest"],
        "chain_order_digest": manifest["chain_order_digest"],
        "serialization": "canonical_json_utf8_lf_v1",
    }
    descriptor["descriptor_digest"] = canonical_digest(descriptor)
    return descriptor


def _build_receipt(
    descriptor: Mapping[str, Any],
    projection: Mapping[str, Any],
) -> dict[str, Any]:
    receipt: dict[str, Any] = {
        "schema_version": "1.0.0",
        "receipt_kind": "portable_literature_production_manifest_receipt",
        "receipt_id": stable_identifier(
            "literature-input-receipt",
            descriptor["descriptor_digest"],
            projection["projection_digest"],
        ),
        "committed_input_role": "pre_commission_theory_input",
        "descriptor": copy.deepcopy(dict(descriptor)),
        "consumer_projection": copy.deepcopy(dict(projection)),
        "validation_scope": {
            "exact_manifest_bytes_reopened": True,
            "canonical_json_utf8_lf_required": True,
            "manifest_internal_causal_invariants_validated": True,
            "source_bundle_reexecution_performed": False,
            "code_dependency_reexecution_performed": False,
            "runtime_root_persisted": False,
        },
        "publication_enabled": False,
        "world_commissioning_authorized": False,
        "authority_boundary": _RECEIPT_AUTHORITY_BOUNDARY,
    }
    receipt["receipt_digest"] = canonical_digest(receipt)
    validate_payload(receipt, COMMITMENT_SCHEMA_NAME)
    return receipt


def _validate_receipt_self(receipt: Mapping[str, Any]) -> dict[str, Any]:
    record = copy.deepcopy(dict(receipt))
    validate_payload(record, COMMITMENT_SCHEMA_NAME)
    descriptor = record["descriptor"]
    projection = record["consumer_projection"]
    if descriptor["descriptor_digest"] != canonical_digest(
        _without(descriptor, "descriptor_digest")
    ):
        _fail("descriptor_digest_mismatch", "manifest descriptor self-digest is invalid")
    if projection["projection_digest"] != canonical_digest(
        _without(projection, "projection_digest")
    ):
        _fail("projection_digest_mismatch", "consumer projection self-digest is invalid")
    expected_receipt_id = stable_identifier(
        "literature-input-receipt",
        descriptor["descriptor_digest"],
        projection["projection_digest"],
    )
    if record["receipt_id"] != expected_receipt_id:
        _fail("receipt_id_mismatch", "receipt identity does not bind descriptor and projection")
    if record["receipt_digest"] != canonical_digest(
        _without(record, "receipt_digest")
    ):
        _fail("receipt_digest_mismatch", "receipt self-digest is invalid")
    if (
        descriptor["manifest_id"] != projection["manifest_id"]
        or descriptor["manifest_digest"] != projection["manifest_digest"]
        or descriptor["chain_order_digest"] != projection["chain_order_digest"]
    ):
        _fail(
            "receipt_projection_identity_mismatch",
            "descriptor and consumer projection name different manifests",
        )
    _canonical_relative_path(descriptor["path"])
    return record


def _snapshot(root: Path, manifest_path: str) -> tuple[bytes, dict[str, Any]]:
    data = _read_exact_regular_file(root, manifest_path)
    manifest = _validate_manifest_internal(_decode_canonical_manifest(data))
    return data, manifest


def build_portable_literature_production_input_receipt(
    root: Path,
    manifest_path: str,
) -> dict[str, Any]:
    """Build one deterministic receipt from a root-relative manifest snapshot."""

    data, manifest = _snapshot(root, manifest_path)
    descriptor = _build_descriptor(manifest_path, data, manifest)
    projection = _derive_consumer_projection(manifest)
    return _build_receipt(descriptor, projection)


def _reopen(
    root: Path,
    receipt: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    record = _validate_receipt_self(receipt)
    descriptor = record["descriptor"]
    data = _read_exact_regular_file(root, descriptor["path"])
    if len(data) != descriptor["size_bytes"]:
        _fail("manifest_bytes_size_mismatch", "committed manifest byte size changed")
    if bytes_digest(data) != descriptor["sha256"]:
        _fail("manifest_bytes_digest_mismatch", "committed manifest bytes changed")
    manifest = _validate_manifest_internal(_decode_canonical_manifest(data))
    expected_descriptor = _build_descriptor(descriptor["path"], data, manifest)
    expected_projection = _derive_consumer_projection(manifest)
    expected_receipt = _build_receipt(expected_descriptor, expected_projection)
    if record != expected_receipt:
        _fail(
            "receipt_replay_mismatch",
            "receipt differs from the exact reopened manifest and projection",
        )
    return record, expected_projection


def validate_portable_literature_production_input_receipt(
    root: Path,
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    """Reopen exact bytes and return the fully replayed receipt."""

    record, _projection = _reopen(root, receipt)
    return record


def reopen_portable_literature_production_input(
    root: Path,
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    """Reopen exact bytes and return only the bounded consumer projection."""

    _record, projection = _reopen(root, receipt)
    return projection


def _derive_semantic_consumer_projection(
    manifest: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    """Carry the exact bounded stage values needed by later theory operators."""

    stages = _stage_map(manifest)
    roles: list[dict[str, Any]] = []
    for role, role_index, stage_id in _SEMANTIC_ROLE_PLAN:
        stage = stages[stage_id]
        roles.append(
            {
                "semantic_role": role,
                "role_index": role_index,
                "production_stage_id": stage_id,
                "production_request_id": stage["request"]["request_id"],
                "production_receipt_id": stage["receipt"]["receipt_id"],
                "content_digest": stage["output"]["content_digest"],
                "value": copy.deepcopy(stage["output"]["payload"]),
            }
        )
    projection: dict[str, Any] = {
        "schema_version": "1.0.0",
        "projection_kind": "bounded_literature_production_semantic_input",
        "input_role": "canonical_theory_generation_input",
        "target_id": manifest["target_id"],
        "producer_run_id": manifest["run_id"],
        "state_version": manifest["state_version"],
        "manifest_id": manifest["manifest_id"],
        "manifest_digest": manifest["manifest_digest"],
        "chain_order_digest": manifest["chain_order_digest"],
        "commitment_receipt_id": receipt["receipt_id"],
        "commitment_receipt_digest": receipt["receipt_digest"],
        "bounded_consumer_projection": copy.deepcopy(
            receipt["consumer_projection"]
        ),
        "semantic_roles": roles,
        "authority_nulls": copy.deepcopy(_BUNDLE_AUTHORITY_NULLS),
        "publication_enabled": False,
        "world_commissioning_authorized": False,
        "authority_boundary": _BUNDLE_AUTHORITY_BOUNDARY,
    }
    projection["projection_digest"] = canonical_digest(projection)
    return projection


def _build_input_bundle(
    manifest: Mapping[str, Any],
    descriptor: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    semantic_projection = _derive_semantic_consumer_projection(manifest, receipt)
    bundle: dict[str, Any] = {
        "schema_version": "1.0.0",
        "bundle_kind": "portable_literature_production_theory_input",
        "bundle_id": stable_identifier(
            "literature-production-input-bundle",
            descriptor["descriptor_digest"],
            receipt["receipt_digest"],
            semantic_projection["projection_digest"],
        ),
        "target_id": manifest["target_id"],
        "producer_run_id": manifest["run_id"],
        "state_version": manifest["state_version"],
        "production_manifest_descriptor": copy.deepcopy(dict(descriptor)),
        "production_manifest": copy.deepcopy(dict(manifest)),
        "commitment_receipt": copy.deepcopy(dict(receipt)),
        "semantic_consumer_projection": semantic_projection,
        "validation_scope": {
            "exact_canonical_manifest_bytes_embedded": True,
            "commitment_receipt_replayed_from_embedded_bytes": True,
            "semantic_stage_values_derived_from_manifest": True,
            "source_bundle_reexecution_performed": False,
            "code_dependency_reexecution_performed": False,
            "runtime_root_persisted": False,
        },
        "publication_enabled": False,
        "world_commissioning_authorized": False,
        "authority_boundary": _BUNDLE_AUTHORITY_BOUNDARY,
    }
    bundle["bundle_digest"] = canonical_digest(bundle)
    validate_payload(bundle, BUNDLE_SCHEMA_NAME)
    return bundle


def build_portable_literature_production_input_bundle(
    root: Path,
    manifest_path: str,
) -> dict[str, Any]:
    """Freeze one self-contained theory input from the exact manifest bytes."""

    data, manifest = _snapshot(root, manifest_path)
    descriptor = _build_descriptor(manifest_path, data, manifest)
    receipt = _build_receipt(descriptor, _derive_consumer_projection(manifest))
    return _build_input_bundle(manifest, descriptor, receipt)


def validate_portable_literature_production_input_bundle(
    bundle: Mapping[str, Any],
) -> dict[str, Any]:
    """Replay a portable bundle without trusting or reopening its old root."""

    record = copy.deepcopy(dict(bundle))
    validate_payload(record, BUNDLE_SCHEMA_NAME)
    manifest = _validate_manifest_internal(record["production_manifest"])
    data = canonical_json(manifest) + b"\n"
    descriptor = record["production_manifest_descriptor"]
    expected_descriptor = _build_descriptor(descriptor["path"], data, manifest)
    expected_receipt = _build_receipt(
        expected_descriptor,
        _derive_consumer_projection(manifest),
    )
    expected = _build_input_bundle(
        manifest,
        expected_descriptor,
        expected_receipt,
    )
    if record != expected:
        _fail(
            "bundle_replay_mismatch",
            "bundle differs from its exact embedded manifest, receipt, or semantic projection",
        )
    return record


__all__ = [
    "BUNDLE_SCHEMA_NAME",
    "COMMITMENT_SCHEMA_NAME",
    "LiteratureProductionCommitmentError",
    "build_portable_literature_production_input_bundle",
    "build_portable_literature_production_input_receipt",
    "reopen_portable_literature_production_input",
    "validate_portable_literature_production_input_bundle",
    "validate_portable_literature_production_input_receipt",
]
