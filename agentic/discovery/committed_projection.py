# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Reconstruct experiment authority from one immutable discovery commit.

The canonical cycle runs against generation ``N-1`` and commits its theory
state as generation ``N``.  A world-matrix commission must therefore use the
verified commit at ``N`` as its base while retaining the original producer
receipts in their honest ``N-1`` namespace.  This module makes that distinction
explicit and prevents callers from supplying replacement reflection, schedule,
source-authority, adjudication, or state objects.

Each cycle persists a deterministic projection-source package.  The public
loader requests the complete package in one ``read_verified_artifacts`` call,
then joins its byte digests to the already verified commit manifest and to the
original producer descriptors sealed in operator evidence.  Runtime paths are
never placed in the resulting authority projection, so relocating the whole
transaction root leaves the projection identity unchanged.
"""

from __future__ import annotations

import copy
import dataclasses
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from agentic.discovery.contracts import (
    ContractError,
    Namespace,
    bytes_digest,
    canonical_digest,
    safe_relative_path,
    validate_payload,
)
from agentic.discovery.receipts import validate_operator_receipt_identity
from agentic.discovery.reflection import validate_packet_invariants
from agentic.discovery.literature_production_commitment import (
    validate_portable_literature_production_input_bundle,
)
from agentic.experiments.world_matrix import (
    build_experiment_authority_projection,
    validate_experiment_authority_projection,
)
from agentic.experiments.world_matrix_commits import build_verified_commit_identity
from agentic.state.discovery_transaction import (
    CommitArtifact,
    DiscoveryTransactionStore,
    VerifiedCommit,
)


PROJECTION_SOURCE_INDEX_SCHEMA = (
    "canonical_cycle_projection_source_index.schema.json"
)
_AUTHORITY_BOUNDARY = (
    "local committed-cycle bytes and exact local producer lineage only; no "
    "external independence, creativity, philosophical depth, truth, theorem, "
    "or physics-result authority"
)
_CORE_SOURCE_PLAN: tuple[tuple[str, str], ...] = (
    ("canonical_cycle", "core/cycle.json"),
    ("finalized_reflection", "core/finalized-reflection.json"),
    ("operator_evidence", "core/operator-evidence.json"),
    ("schedule", "core/schedule.json"),
)
_SEMANTIC_SOURCE_PLAN: tuple[tuple[str, int, str | None], ...] = (
    ("literature_production_input_bundle", 0, None),
    (
        "source_routing_pre_map_policy",
        0,
        "source-routing-pre-map-policy-producer",
    ),
    (
        "source_routing_realization",
        0,
        "source-routing-realization-producer",
    ),
    ("high_risk_portfolio", 0, "high-risk-hypothesis-forger"),
    ("parallel_portfolio", 0, "parallel-hypothesis-portfolio"),
    ("reflective_packets", 0, "reflective-conceptual-discovery"),
    ("reflective_packets", 1, "reflective-theory-synthesizer"),
    (
        "parent_conceptual_adjudication",
        0,
        "blind-conceptual-preference-adjudicator",
    ),
    (
        "synthesis_conceptual_adjudication",
        0,
        "blind-conceptual-preference-adjudicator",
    ),
)
_ROLE_SCHEMAS = {
    "literature_production_input_bundle": "literature_production_input_bundle.schema.json",
    "source_routing_pre_map_policy": "source_routing_pre_map_policy.schema.json",
    "source_routing_realization": "source_routing_realization.schema.json",
    "high_risk_portfolio": "high_risk_hypothesis_portfolio.schema.json",
    "parallel_portfolio": "parallel_hypothesis_portfolio.schema.json",
    "reflective_packets": "reflective_conceptual_discovery_packet.schema.json",
    "parent_conceptual_adjudication": "conceptual_adjudication_evidence.schema.json",
    "synthesis_conceptual_adjudication": "conceptual_adjudication_evidence.schema.json",
}


@dataclasses.dataclass(frozen=True, slots=True)
class CommittedCycleProjectionSources:
    """One manifest-verified, path-independent projection source snapshot."""

    verified_commit: VerifiedCommit
    source_index: Mapping[str, Any]
    canonical_cycle: Mapping[str, Any]
    finalized_reflection: Mapping[str, Any]
    operator_evidence: Mapping[str, Any]
    schedule: Mapping[str, Any]
    literature_production_input_bundle: Mapping[str, Any]
    semantic_payloads: Mapping[tuple[str, int], Mapping[str, Any]]
    producers_by_role: Mapping[str, tuple[Mapping[str, Any], ...]]


@dataclasses.dataclass(frozen=True, slots=True)
class CommittedLiteratureInput:
    """The exact literature bundle reopened through one verified generation."""

    verified_commit: VerifiedCommit
    source_index: Mapping[str, Any]
    bundle: Mapping[str, Any]


def _json_bytes(value: Any) -> bytes:
    """Match the transaction's deterministic human-readable JSON encoding."""

    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False).encode(
            "utf-8"
        )
        + b"\n"
    )


def _package_base(generation: int) -> str:
    if (
        isinstance(generation, bool)
        or not isinstance(generation, int)
        or generation <= 0
    ):
        raise ContractError("verified theory generation must be a positive integer")
    return (
        "branches/root/committed-cycle-projection/"
        f"generation-{generation:012d}"
    )


def _semantic_package_path(generation: int, role: str, index: int) -> str:
    return f"{_package_base(generation)}/semantic/{role}/{index}.json"


def committed_cycle_projection_artifact_paths(generation: int) -> tuple[str, ...]:
    """Return the closed deterministic package path vector for generation N."""

    base = _package_base(generation)
    return (
        f"{base}/projection-source-index.json",
        *(f"{base}/{suffix}" for _, suffix in _CORE_SOURCE_PLAN),
        *(
            _semantic_package_path(generation, role, role_index)
            for role, role_index, _ in _SEMANTIC_SOURCE_PLAN
        ),
    )


def _one_row(
    rows: Sequence[Mapping[str, Any]],
    *,
    label: str,
    predicate: Any,
) -> dict[str, Any] | None:
    matches = [copy.deepcopy(dict(row)) for row in rows if predicate(row)]
    if len(matches) > 1:
        raise ContractError(f"canonical projection source has duplicate {label}")
    return matches[0] if matches else None


def build_committed_cycle_projection_artifacts(
    *,
    target_id: str,
    run_id: str,
    source_cycle_prior_state_version: int,
    cycle_id: str,
    canonical_cycle: Mapping[str, Any],
    finalized_reflection: Mapping[str, Any],
    schedule: Mapping[str, Any],
    operator_evidence: Mapping[str, Any],
    sealed_artifacts: Sequence[CommitArtifact],
    namespace: Namespace,
) -> tuple[list[CommitArtifact], dict[str, str]]:
    """Build the deterministic source package committed with a canonical cycle.

    Role artifacts that lack a real producer are represented by an explicit
    absence record.  This keeps the path vector closed for a one-batch reopen
    without laundering an external file into a producer receipt.
    """

    matrix_base_generation = source_cycle_prior_state_version + 1
    if namespace != Namespace(
        target_id,
        run_id,
        "root",
        source_cycle_prior_state_version,
    ):
        raise ContractError("projection source package namespace is not the cycle namespace")
    cycle_value = copy.deepcopy(dict(canonical_cycle))
    reflection_value = copy.deepcopy(dict(finalized_reflection))
    schedule_value = copy.deepcopy(dict(schedule))
    evidence_value = copy.deepcopy(dict(operator_evidence))
    if (
        cycle_value.get("cycle_id") != cycle_id
        or cycle_value.get("target_id") != target_id
        or cycle_value.get("run_id") != run_id
        or cycle_value.get("prior_state_version")
        != source_cycle_prior_state_version
        or cycle_value.get("next_state_version") != matrix_base_generation
    ):
        raise ContractError("projection source package crossed its canonical cycle")
    validate_payload(evidence_value, "canonical_operator_evidence.schema.json")
    if evidence_value.get("evidence_digest") != canonical_digest(
        evidence_value, exclude_keys=("evidence_digest",)
    ):
        raise ContractError("projection source operator evidence self-digest is invalid")

    sealed_by_path: dict[str, bytes] = {}
    for artifact in sealed_artifacts:
        path = safe_relative_path(artifact.relative_path).as_posix()
        if path in sealed_by_path:
            raise ContractError(f"duplicate sealed source artifact: {path}")
        if not isinstance(artifact.content, bytes):
            raise ContractError(
                "projection source packaging requires already frozen sealed bytes"
            )
        sealed_by_path[path] = artifact.content

    base = _package_base(matrix_base_generation)
    core_payloads = {
        "canonical_cycle": cycle_value,
        "finalized_reflection": reflection_value,
        "operator_evidence": evidence_value,
        "schedule": schedule_value,
    }
    artifacts: list[CommitArtifact] = []
    artifact_roles: dict[str, str] = {}
    core_bindings: list[dict[str, Any]] = []
    for source_name, suffix in _CORE_SOURCE_PLAN:
        path = f"{base}/{suffix}"
        data = _json_bytes(core_payloads[source_name])
        artifacts.append(CommitArtifact(path, data, namespace))
        artifact_roles[f"projection_source.{source_name}"] = path
        core_bindings.append(
            {
                "source_name": source_name,
                "package_path": path,
                "sha256": bytes_digest(data),
                "size_bytes": len(data),
                "origin_kind": "canonical_cycle_reducer",
                "producer_receipt_id": None,
                "producer_request_id": None,
                "producer_operator_id": None,
                "producer_descriptor": None,
            }
        )

    raw_role_bindings = evidence_value.get("role_bindings", [])
    raw_output_bindings = evidence_value.get("output_bindings", [])
    raw_receipts = evidence_value.get("operator_receipts", [])
    if not all(
        isinstance(rows, list)
        for rows in (raw_role_bindings, raw_output_bindings, raw_receipts)
    ):
        raise ContractError("operator evidence projection bindings are not arrays")
    semantic_bindings: list[dict[str, Any]] = []
    for role, role_index, expected_operator in _SEMANTIC_SOURCE_PLAN:
        path = _semantic_package_path(matrix_base_generation, role, role_index)
        role_binding = _one_row(
            raw_role_bindings,
            label=f"role binding {role}[{role_index}]",
            predicate=lambda row, role=role, role_index=role_index: (
                row.get("role") == role and row.get("role_index") == role_index
            ),
        )
        external_source = expected_operator is None
        available = bool(
            role_binding is not None
            and (
                (
                    external_source
                    and role_binding.get("source_kind")
                    == "external_role_artifact"
                    and all(
                        role_binding.get(field) is None
                        for field in (
                            "producer_receipt_id",
                            "producer_request_id",
                            "producer_operator_id",
                        )
                    )
                )
                or (
                    not external_source
                    and role_binding.get("source_kind") == "operator_output"
                    and role_binding.get("producer_receipt_id")
                    and role_binding.get("producer_request_id")
                    and role_binding.get("producer_operator_id")
                    == expected_operator
                )
            )
        )
        if available:
            assert role_binding is not None
            original_path = str(role_binding["sealed_path"])
            data = sealed_by_path.get(original_path)
            if (
                data is None
                or bytes_digest(data) != role_binding.get("sha256")
                or len(data) != role_binding.get("size_bytes")
            ):
                raise ContractError(
                    f"projection role bytes differ from their sealed source: {role}[{role_index}]"
                )
            availability = "available"
            original_sealed_path: str | None = original_path
            commit_artifact_role: str | None = str(
                role_binding["commit_artifact_role"]
            )
            if external_source:
                source_kind = "external_role_artifact"
                producer_receipt_id = None
                producer_request_id = None
                producer_operator_id = None
                producer_descriptor: Mapping[str, Any] | None = None
            else:
                output_binding = _one_row(
                    raw_output_bindings,
                    label=f"producer output {role}[{role_index}]",
                    predicate=lambda row, binding=role_binding: (
                        row.get("sealed_path") == binding.get("sealed_path")
                        and row.get("receipt_id")
                        == binding.get("producer_receipt_id")
                        and row.get("request_id")
                        == binding.get("producer_request_id")
                        and row.get("operator_id")
                        == binding.get("producer_operator_id")
                        and row.get("semantic_role") == binding.get("role")
                        and row.get("status") == "succeeded"
                    ),
                )
                if output_binding is None:
                    raise ContractError(
                        f"operator-bound projection role lacks its output binding: {role}[{role_index}]"
                    )
                receipt = _one_row(
                    raw_receipts,
                    label=f"producer receipt {role}[{role_index}]",
                    predicate=lambda row, binding=role_binding: row.get(
                        "receipt_id"
                    )
                    == binding.get("producer_receipt_id"),
                )
                if receipt is None:
                    raise ContractError(
                        f"operator-bound projection role lacks its receipt: {role}[{role_index}]"
                    )
                validate_operator_receipt_identity(receipt)
                descriptor = copy.deepcopy(output_binding["original_descriptor"])
                if (
                    bytes_digest(data) != output_binding.get("sealed_sha256")
                    or bytes_digest(data) != descriptor.get("sha256")
                    or len(data) != output_binding.get("sealed_size_bytes")
                    or len(data) != descriptor.get("size_bytes")
                    or descriptor not in receipt.get("output_artifacts", [])
                ):
                    raise ContractError(
                        f"projection role bytes differ from their producer descriptor: {role}[{role_index}]"
                    )
                source_kind = "operator_output"
                producer_receipt_id = role_binding["producer_receipt_id"]
                producer_request_id = role_binding["producer_request_id"]
                producer_operator_id = role_binding["producer_operator_id"]
                producer_descriptor = descriptor
        else:
            absence = {
                "schema_version": "1.0.0",
                "source_status": "absent",
                "semantic_role": role,
                "role_index": role_index,
                "source_cycle_prior_state_version": (
                    source_cycle_prior_state_version
                ),
                "reason": "no_operator_bound_projection_source",
            }
            data = _json_bytes(absence)
            availability = "absent"
            source_kind = "absent"
            producer_receipt_id = None
            producer_request_id = None
            producer_operator_id = None
            original_sealed_path = None
            commit_artifact_role = None
            producer_descriptor = None
        artifacts.append(CommitArtifact(path, data, namespace))
        artifact_roles[f"projection_source.{role}.{role_index}"] = path
        semantic_bindings.append(
            {
                "semantic_role": role,
                "role_index": role_index,
                "availability": availability,
                "package_path": path,
                "sha256": bytes_digest(data),
                "size_bytes": len(data),
                "source_kind": source_kind,
                "original_sealed_path": original_sealed_path,
                "commit_artifact_role": commit_artifact_role,
                "producer_receipt_id": producer_receipt_id,
                "producer_request_id": producer_request_id,
                "producer_operator_id": producer_operator_id,
                "producer_descriptor": copy.deepcopy(producer_descriptor),
            }
        )

    source_index: dict[str, Any] = {
        "schema_version": "1.0.0",
        "index_kind": "canonical_committed_cycle_world_projection_sources",
        "cycle_id": cycle_id,
        "target_id": target_id,
        "run_id": run_id,
        "source_cycle_prior_state_version": source_cycle_prior_state_version,
        "matrix_base_generation": matrix_base_generation,
        "core_bindings": core_bindings,
        "semantic_role_bindings": semantic_bindings,
        "authority_boundary": _AUTHORITY_BOUNDARY,
    }
    source_index["index_digest"] = canonical_digest(source_index)
    validate_payload(source_index, PROJECTION_SOURCE_INDEX_SCHEMA)
    index_path = f"{base}/projection-source-index.json"
    artifacts.insert(0, CommitArtifact(index_path, _json_bytes(source_index), namespace))
    artifact_roles["projection_source.index"] = index_path
    return artifacts, artifact_roles


def _decode_object(data: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(data)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"committed projection source {label} is not JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError(f"committed projection source {label} is not an object")
    return value


def _manifest_descriptors(commit: VerifiedCommit) -> dict[str, dict[str, Any]]:
    descriptors: dict[str, dict[str, Any]] = {}
    for raw in commit.manifest.get("artifacts", []):
        if not isinstance(raw, Mapping) or not isinstance(raw.get("path"), str):
            raise ContractError("verified commit carries a malformed artifact descriptor")
        path = str(raw["path"])
        if path in descriptors:
            raise ContractError(f"verified commit repeats artifact path: {path}")
        descriptors[path] = copy.deepcopy(dict(raw))
    return descriptors


def _require_bound_bytes(
    *,
    binding: Mapping[str, Any],
    path: str,
    data: bytes,
    descriptors: Mapping[str, Mapping[str, Any]],
    expected_namespace: Mapping[str, Any],
) -> None:
    descriptor = descriptors.get(path)
    if (
        binding.get("package_path") != path
        or binding.get("sha256") != bytes_digest(data)
        or binding.get("size_bytes") != len(data)
        or descriptor is None
        or descriptor.get("sha256") != bytes_digest(data)
        or descriptor.get("size_bytes") != len(data)
        or descriptor.get("namespace") != expected_namespace
    ):
        raise ContractError(f"committed projection source binding drifted: {path}")


def load_committed_cycle_projection_sources(
    store: DiscoveryTransactionStore,
    verified_theory_generation: int,
) -> CommittedCycleProjectionSources:
    """Load the complete package through exactly one verified artifact batch."""

    paths = committed_cycle_projection_artifact_paths(verified_theory_generation)
    commit, artifact_bytes = store.read_verified_artifacts(
        verified_theory_generation,
        paths,
    )
    index_path = paths[0]
    source_index = _decode_object(artifact_bytes[index_path], "source index")
    validate_payload(source_index, PROJECTION_SOURCE_INDEX_SCHEMA)
    if source_index.get("index_digest") != canonical_digest(
        source_index, exclude_keys=("index_digest",)
    ):
        raise ContractError("committed projection source index self-digest is invalid")
    if (
        source_index.get("target_id") != store.target_id
        or source_index.get("run_id") != store.run_id
        or source_index.get("matrix_base_generation") != commit.generation
        or source_index.get("source_cycle_prior_state_version")
        != commit.prior_generation
        or commit.generation != commit.prior_generation + 1
        or commit.state.get("target_id") != store.target_id
        or commit.state.get("run_id") != store.run_id
        or commit.state.get("generation") != commit.generation
    ):
        raise ContractError("committed projection source index crossed its verified commit")
    descriptors = _manifest_descriptors(commit)
    expected_namespace = Namespace(
        store.target_id,
        store.run_id,
        "root",
        commit.prior_generation,
    ).as_dict()
    index_descriptor = descriptors.get(index_path)
    if (
        index_descriptor is None
        or index_descriptor.get("sha256") != bytes_digest(artifact_bytes[index_path])
        or index_descriptor.get("size_bytes") != len(artifact_bytes[index_path])
        or index_descriptor.get("namespace") != expected_namespace
    ):
        raise ContractError("committed projection source index is not manifest-bound")

    core_values: dict[str, dict[str, Any]] = {}
    core_bindings = source_index["core_bindings"]
    if len(core_bindings) != len(_CORE_SOURCE_PLAN):
        raise ContractError("committed projection core binding cardinality drifted")
    for binding, (source_name, suffix) in zip(
        core_bindings, _CORE_SOURCE_PLAN, strict=True
    ):
        path = f"{_package_base(commit.generation)}/{suffix}"
        data = artifact_bytes[path]
        if binding.get("source_name") != source_name:
            raise ContractError("committed projection core binding order drifted")
        _require_bound_bytes(
            binding=binding,
            path=path,
            data=data,
            descriptors=descriptors,
            expected_namespace=expected_namespace,
        )
        core_values[source_name] = _decode_object(data, source_name)

    cycle_value = core_values["canonical_cycle"]
    reflection_value = core_values["finalized_reflection"]
    evidence_value = core_values["operator_evidence"]
    schedule_value = core_values["schedule"]
    validate_payload(evidence_value, "canonical_operator_evidence.schema.json")
    validate_payload(
        reflection_value, "reflective_conceptual_discovery_packet.schema.json"
    )
    validate_packet_invariants(reflection_value)
    if reflection_value.get("packet_digest") != canonical_digest(
        reflection_value, exclude_keys=("packet_digest",)
    ):
        raise ContractError("committed finalized reflection self-digest is invalid")
    if evidence_value.get("evidence_digest") != canonical_digest(
        evidence_value, exclude_keys=("evidence_digest",)
    ):
        raise ContractError("committed operator evidence self-digest is invalid")
    source_version = commit.prior_generation
    common_identity = (store.target_id, store.run_id, source_version)
    if (
        (
            cycle_value.get("target_id"),
            cycle_value.get("run_id"),
            cycle_value.get("prior_state_version"),
        )
        != common_identity
        or cycle_value.get("next_state_version") != commit.generation
        or cycle_value.get("cycle_id") != source_index.get("cycle_id")
        or cycle_value.get("operator_evidence_digest")
        != evidence_value.get("evidence_digest")
        or (
            evidence_value.get("target_id"),
            evidence_value.get("run_id"),
            evidence_value.get("prior_state_version"),
        )
        != common_identity
        or evidence_value.get("cycle_id") != cycle_value.get("cycle_id")
        or (
            reflection_value.get("target_id"),
            reflection_value.get("run_id"),
            reflection_value.get("state_version"),
        )
        != common_identity
        or reflection_value.get("branch_id") != "root"
        or (
            schedule_value.get("target_id"),
            schedule_value.get("run_id"),
            schedule_value.get("state_version"),
        )
        != common_identity
        or schedule_value.get("schedule_id") != cycle_value.get("schedule_id")
    ):
        raise ContractError("committed projection core sources crossed cycle identity")

    receipts = evidence_value.get("operator_receipts", [])
    role_bindings = evidence_value.get("role_bindings", [])
    output_bindings = evidence_value.get("output_bindings", [])
    if not all(
        isinstance(rows, list) for rows in (receipts, role_bindings, output_bindings)
    ):
        raise ContractError("committed operator evidence bindings are not arrays")
    receipts_by_id: dict[str, dict[str, Any]] = {}
    for raw_receipt in receipts:
        receipt = copy.deepcopy(dict(raw_receipt))
        validate_operator_receipt_identity(receipt)
        receipt_id = str(receipt["receipt_id"])
        if receipt_id in receipts_by_id:
            raise ContractError("committed operator evidence repeats a receipt")
        receipts_by_id[receipt_id] = receipt

    semantic_payloads: dict[tuple[str, int], dict[str, Any]] = {}
    producers_by_role: dict[str, list[dict[str, Any]]] = {}
    semantic_bindings = source_index["semantic_role_bindings"]
    if len(semantic_bindings) != len(_SEMANTIC_SOURCE_PLAN):
        raise ContractError("committed semantic source cardinality drifted")
    for binding, (role, role_index, expected_operator) in zip(
        semantic_bindings, _SEMANTIC_SOURCE_PLAN, strict=True
    ):
        path = _semantic_package_path(commit.generation, role, role_index)
        data = artifact_bytes[path]
        if (
            binding.get("semantic_role") != role
            or binding.get("role_index") != role_index
        ):
            raise ContractError("committed semantic source order drifted")
        _require_bound_bytes(
            binding=binding,
            path=path,
            data=data,
            descriptors=descriptors,
            expected_namespace=expected_namespace,
        )
        if binding.get("availability") != "available":
            raise ContractError(
                f"committed cycle lacks required projection source {role}[{role_index}]"
            )
        original_path = str(binding["original_sealed_path"])
        original_descriptor = descriptors.get(original_path)
        producer_descriptor = binding["producer_descriptor"]
        if (
            original_descriptor is None
            or original_descriptor.get("sha256") != bytes_digest(data)
            or original_descriptor.get("size_bytes") != len(data)
            or original_descriptor.get("namespace") != expected_namespace
        ):
            raise ContractError(
                f"committed semantic copy differs from its original sealed bytes: {role}[{role_index}]"
            )
        role_row = _one_row(
            role_bindings,
            label=f"committed role binding {role}[{role_index}]",
            predicate=lambda row, role=role, role_index=role_index: (
                row.get("role") == role and row.get("role_index") == role_index
            ),
        )
        if expected_operator is None:
            if (
                binding.get("source_kind") != "external_role_artifact"
                or producer_descriptor is not None
                or any(
                    binding.get(field) is not None
                    for field in (
                        "producer_receipt_id",
                        "producer_request_id",
                        "producer_operator_id",
                    )
                )
                or role_row is None
                or role_row.get("source_kind") != "external_role_artifact"
                or role_row.get("sealed_path") != original_path
                or role_row.get("commit_artifact_role")
                != binding.get("commit_artifact_role")
            ):
                raise ContractError(
                    f"committed external semantic source index drifted: {role}[{role_index}]"
                )
            receipt = None
        else:
            if (
                not isinstance(producer_descriptor, Mapping)
                or producer_descriptor.get("sha256") != bytes_digest(data)
                or producer_descriptor.get("size_bytes") != len(data)
                or producer_descriptor.get("namespace") != expected_namespace
            ):
                raise ContractError(
                    f"committed semantic copy differs from its original producer bytes: {role}[{role_index}]"
                )
            receipt_id = str(binding["producer_receipt_id"])
            receipt = receipts_by_id.get(receipt_id)
            if (
                receipt is None
                or receipt.get("request_id")
                != binding.get("producer_request_id")
                or receipt.get("operator", {}).get("operator_id")
                != expected_operator
                or binding.get("producer_operator_id") != expected_operator
                or receipt.get("status") != "succeeded"
                or producer_descriptor not in receipt.get("output_artifacts", [])
            ):
                raise ContractError(
                    f"committed semantic source crossed its original producer: {role}[{role_index}]"
                )
            output_row = _one_row(
                output_bindings,
                label=f"committed output binding {role}[{role_index}]",
                predicate=lambda row, binding=binding: (
                    row.get("sealed_path")
                    == binding.get("original_sealed_path")
                    and row.get("receipt_id")
                    == binding.get("producer_receipt_id")
                    and row.get("request_id")
                    == binding.get("producer_request_id")
                    and row.get("operator_id")
                    == binding.get("producer_operator_id")
                    and row.get("semantic_role")
                    == binding.get("semantic_role")
                    and row.get("status") == "succeeded"
                ),
            )
            if (
                role_row is None
                or output_row is None
                or role_row.get("sealed_path") != original_path
                or role_row.get("commit_artifact_role")
                != binding.get("commit_artifact_role")
                or role_row.get("producer_receipt_id") != receipt_id
                or role_row.get("producer_request_id")
                != binding.get("producer_request_id")
                or role_row.get("producer_operator_id") != expected_operator
                or output_row.get("original_descriptor") != producer_descriptor
                or output_row.get("sealed_sha256") != bytes_digest(data)
                or output_row.get("sealed_size_bytes") != len(data)
            ):
                raise ContractError(
                    f"committed semantic source index differs from operator evidence: {role}[{role_index}]"
                )
        payload = _decode_object(data, f"{role}[{role_index}]")
        validate_payload(payload, _ROLE_SCHEMAS[role])
        if expected_operator is None:
            payload = validate_portable_literature_production_input_bundle(
                payload
            )
        semantic_payloads[(role, role_index)] = payload
        if receipt is not None:
            producers_by_role.setdefault(role, []).append(receipt)

    return CommittedCycleProjectionSources(
        verified_commit=commit,
        source_index=copy.deepcopy(source_index),
        canonical_cycle=copy.deepcopy(cycle_value),
        finalized_reflection=copy.deepcopy(reflection_value),
        operator_evidence=copy.deepcopy(evidence_value),
        schedule=copy.deepcopy(schedule_value),
        literature_production_input_bundle=copy.deepcopy(
            semantic_payloads[("literature_production_input_bundle", 0)]
        ),
        semantic_payloads=copy.deepcopy(semantic_payloads),
        producers_by_role={
            role: tuple(copy.deepcopy(rows))
            for role, rows in producers_by_role.items()
        },
    )


def load_committed_cycle_literature_input(
    store: DiscoveryTransactionStore,
    verified_theory_generation: int,
) -> CommittedLiteratureInput:
    """Reopen only the required literature bundle through ``VerifiedCommit``.

    Unlike the full world-authority loader, this route remains valid for a
    local-incubation cycle whose source-routing or adjudication roles are
    intentionally absent.  It still verifies the complete commit before
    returning the exact package copy and its exact original sealed-role copy.
    """

    index_path = f"{_package_base(verified_theory_generation)}/projection-source-index.json"
    bundle_path = _semantic_package_path(
        verified_theory_generation,
        "literature_production_input_bundle",
        0,
    )
    commit, artifact_bytes = store.read_verified_artifacts(
        verified_theory_generation,
        (index_path, bundle_path),
    )
    source_index = _decode_object(artifact_bytes[index_path], "source index")
    validate_payload(source_index, PROJECTION_SOURCE_INDEX_SCHEMA)
    if source_index.get("index_digest") != canonical_digest(
        source_index, exclude_keys=("index_digest",)
    ):
        raise ContractError("committed projection source index self-digest is invalid")
    if (
        source_index.get("target_id") != store.target_id
        or source_index.get("run_id") != store.run_id
        or source_index.get("matrix_base_generation") != commit.generation
        or source_index.get("source_cycle_prior_state_version")
        != commit.prior_generation
        or commit.generation != commit.prior_generation + 1
    ):
        raise ContractError("committed literature source index crossed its verified commit")
    descriptors = _manifest_descriptors(commit)
    expected_namespace = Namespace(
        store.target_id,
        store.run_id,
        "root",
        commit.prior_generation,
    ).as_dict()
    index_descriptor = descriptors.get(index_path)
    if (
        index_descriptor is None
        or index_descriptor.get("sha256")
        != bytes_digest(artifact_bytes[index_path])
        or index_descriptor.get("size_bytes")
        != len(artifact_bytes[index_path])
        or index_descriptor.get("namespace") != expected_namespace
    ):
        raise ContractError("committed literature source index is not manifest-bound")
    binding = _one_row(
        source_index["semantic_role_bindings"],
        label="literature-production input binding",
        predicate=lambda row: (
            row.get("semantic_role") == "literature_production_input_bundle"
            and row.get("role_index") == 0
        ),
    )
    if binding is None:
        raise ContractError("committed projection omits its literature-production input")
    data = artifact_bytes[bundle_path]
    _require_bound_bytes(
        binding=binding,
        path=bundle_path,
        data=data,
        descriptors=descriptors,
        expected_namespace=expected_namespace,
    )
    original_path = str(binding.get("original_sealed_path", ""))
    original_descriptor = descriptors.get(original_path)
    if (
        binding.get("availability") != "available"
        or binding.get("source_kind") != "external_role_artifact"
        or not original_path
        or binding.get("commit_artifact_role") is None
        or any(
            binding.get(field) is not None
            for field in (
                "producer_receipt_id",
                "producer_request_id",
                "producer_operator_id",
                "producer_descriptor",
            )
        )
        or original_descriptor is None
        or original_descriptor.get("sha256") != bytes_digest(data)
        or original_descriptor.get("size_bytes") != len(data)
        or original_descriptor.get("namespace") != expected_namespace
    ):
        raise ContractError(
            "committed literature package differs from its exact sealed external role bytes"
        )
    bundle = validate_portable_literature_production_input_bundle(
        _decode_object(data, "literature-production input bundle")
    )
    return CommittedLiteratureInput(
        verified_commit=commit,
        source_index=copy.deepcopy(source_index),
        bundle=copy.deepcopy(bundle),
    )


def _component_values(projection: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    values: dict[str, dict[str, Any]] = {}
    for row in projection.get("components", []):
        if not isinstance(row, Mapping) or not isinstance(row.get("value"), Mapping):
            raise ContractError("experiment authority projection component is malformed")
        kind = str(row.get("component_kind", ""))
        if kind in values:
            raise ContractError(f"experiment authority projection repeats {kind!r}")
        values[kind] = copy.deepcopy(dict(row["value"]))
    return values


def derive_committed_cycle_world_authority_projection(
    store: DiscoveryTransactionStore,
    verified_theory_generation: int,
) -> dict[str, Any]:
    """Derive a world authority base from store plus generation, and nothing else."""

    sources = load_committed_cycle_projection_sources(
        store,
        verified_theory_generation,
    )
    commit = sources.verified_commit
    source_version = commit.prior_generation
    cycle_value = copy.deepcopy(dict(sources.canonical_cycle))
    reflection = copy.deepcopy(dict(sources.finalized_reflection))
    conceptual_authority = copy.deepcopy(
        dict(cycle_value.get("conceptual_authority", {}))
    )
    source_pair = {
        "pre_map_policy": copy.deepcopy(
            sources.semantic_payloads[("source_routing_pre_map_policy", 0)]
        ),
        "realization": copy.deepcopy(
            sources.semantic_payloads[("source_routing_realization", 0)]
        ),
    }
    parent_adjudication = copy.deepcopy(
        sources.semantic_payloads[("parent_conceptual_adjudication", 0)]
    )
    synthesis_adjudication = copy.deepcopy(
        sources.semantic_payloads[("synthesis_conceptual_adjudication", 0)]
    )
    literature_bundle = copy.deepcopy(
        dict(sources.literature_production_input_bundle)
    )
    literature_projection = literature_bundle["semantic_consumer_projection"]
    literature_summary = cycle_value.get("literature_production_input", {})
    if (
        cycle_value.get("source_routing_pre_map_policy")
        != source_pair["pre_map_policy"]
        or cycle_value.get("source_routing_realization")
        != source_pair["realization"]
        or conceptual_authority.get("parent_evidence") != parent_adjudication
        or conceptual_authority.get("synthesis_evidence")
        != synthesis_adjudication
        or reflection.get("conceptual_adjudication_evidence")
        != synthesis_adjudication
        or cycle_value.get("literature_production_projection_digest")
        != literature_projection.get("projection_digest")
        or literature_summary.get("bundle_id")
        != literature_bundle.get("bundle_id")
        or literature_summary.get("bundle_digest")
        != literature_bundle.get("bundle_digest")
        or literature_summary.get("production_manifest_descriptor")
        != literature_bundle.get("production_manifest_descriptor")
        or literature_summary.get("commitment_receipt_digest")
        != literature_bundle.get("commitment_receipt", {}).get(
            "receipt_digest"
        )
        or literature_summary.get("semantic_projection_digest")
        != literature_projection.get("projection_digest")
        or literature_summary.get("authority_nulls")
        != literature_projection.get("authority_nulls")
    ):
        raise ContractError(
            "committed cycle authority differs from its exact semantic source bytes"
        )

    # The legacy pure builder remains the single semantic translation for all
    # non-ancestor components.  Its temporary state value is derived from the
    # committed state and used only for its discarded N-1 ancestor component.
    # No caller data enters this route.
    source_cycle_state = copy.deepcopy(dict(commit.state))
    source_cycle_state["generation"] = source_version
    from agentic.discovery.cycle import build_canonical_world_authority_projection

    source_projection = build_canonical_world_authority_projection(
        target_id=store.target_id,
        run_id=store.run_id,
        state_version=source_version,
        prior_state=source_cycle_state,
        final_reflection=reflection,
        conceptual_authority=conceptual_authority,
        source_authority_pair=source_pair,
        literature_production_input_bundle=literature_bundle,
        producers_by_role=sources.producers_by_role,
        schedule=sources.schedule,
    )
    values = _component_values(source_projection)
    verified_identity = build_verified_commit_identity(commit)
    committed_ancestor = {
        "ancestor_kind": "verified_local_committed_state",
        "source_cycle_prior_state_version": source_version,
        "matrix_base_generation": commit.generation,
        "generation": commit.generation,
        "state": copy.deepcopy(dict(commit.state)),
        "state_semantic_digest": commit.state_semantic_digest,
        "verified_commit_identity": verified_identity,
        "authority_boundary": (
            "exact generation-N state and path-free identity reopened from the "
            "local immutable transcript; source producers retain namespace N-1; "
            "no external-state or independence authority"
        ),
    }
    return build_experiment_authority_projection(
        target_id=store.target_id,
        run_id=store.run_id,
        prior_state_version=commit.generation,
        committed_ancestor=committed_ancestor,
        theory_programme=values["theory_programme"],
        reflection_packet=values["reflection_packet"],
        conceptual_systems=values["conceptual_systems"],
        genealogy=values["genealogy"],
        source_authority=values["source_authority"],
        registered_claim=values["registered_claim"],
        generator_authority=values["generator_authority"],
        adjudication_authority=values["adjudication_authority"],
        schedule=values["schedule"],
    )


def replay_committed_cycle_world_authority_projection(
    observed_projection: Mapping[str, Any],
    store: DiscoveryTransactionStore,
    verified_theory_generation: int,
) -> dict[str, Any]:
    """Require literal equality with a fresh store-only committed derivation."""

    observed = validate_experiment_authority_projection(observed_projection)
    expected = derive_committed_cycle_world_authority_projection(
        store,
        verified_theory_generation,
    )
    if observed != expected:
        observed_values = _component_values(observed)
        expected_values = _component_values(expected)
        changed_components = sorted(
            kind
            for kind in set(observed_values) | set(expected_values)
            if observed_values.get(kind) != expected_values.get(kind)
        )
        raise ContractError(
            "observed world authority is not the committed-cycle derivation: "
            f"changed_components={changed_components}"
        )
    return expected


__all__ = [
    "CommittedCycleProjectionSources",
    "CommittedLiteratureInput",
    "PROJECTION_SOURCE_INDEX_SCHEMA",
    "build_committed_cycle_projection_artifacts",
    "committed_cycle_projection_artifact_paths",
    "derive_committed_cycle_world_authority_projection",
    "load_committed_cycle_projection_sources",
    "load_committed_cycle_literature_input",
    "replay_committed_cycle_world_authority_projection",
]
